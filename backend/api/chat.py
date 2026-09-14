
from uuid import uuid4

from fastapi import APIRouter

from ai.answer_normalizer import normalize_answer

from models.schemas import (
    ChatRequest,
    ChatResponse,
    DiagnosisResult,
    DiagnosticStatus,
    ActionType,
    ConfidenceLevel,
)

from safety.safety_engine import check_safety

from diagnosis.engine import (
    start_diagnosis,
    process_safety_answer,
    process_answer,
)


router = APIRouter()


# --------------------------------------------------
# Temporary in-memory diagnostic sessions
# --------------------------------------------------

sessions = {}


# --------------------------------------------------
# Identify the first demo problem
# --------------------------------------------------

def identify_problem(message: str):
    """
    Temporarily identifies the device and problem
    using simple keyword matching.

    Later, the LLM will perform this job.
    """

    message = message.lower()

    fan_keywords = [
        "fan",
        "standing fan",
    ]

    not_working_keywords = [
        "not working",
        "doesn't work",
        "doesnt work",
        "not turning on",
        "doesn't turn on",
        "doesnt turn on",
        "won't turn on",
        "wont turn on",
        "not coming on",
        "doesn't come on",
        "doesnt come on",
        "won't start",
        "wont start",
    ]

    has_fan = any(
        keyword in message
        for keyword in fan_keywords
    )

    has_not_working = any(
        keyword in message
        for keyword in not_working_keywords
    )

    if has_fan and has_not_working:
        return {
            "device": "standing_fan",
            "problem": "fan_not_turning_on",
        }

    return None


# --------------------------------------------------
# Convert engine result into API response
# --------------------------------------------------

def build_diagnosis_response(
    result: dict,
    session_id: str,
    device: str,
    problem: str,
):
    """
    Converts the diagnostic engine result
    into the format expected by the API.
    """

    action = result.get("action")

    if action == "stop":
        action_type = ActionType.STOP

    elif action == "technician_referral":
        action_type = ActionType.TECHNICIAN_REFERRAL

    elif action == "solved":
        action_type = ActionType.SOLVED

    else:
        action_type = ActionType.ASK_QUESTION

    # ----------------------------------------------
    # Convert confidence string to enum
    # ----------------------------------------------

    confidence = result.get("confidence")

    if confidence:
        confidence = ConfidenceLevel(confidence)

    # ----------------------------------------------
    # Convert status string to enum
    # ----------------------------------------------

    status_value = result.get(
        "status",
        "diagnosing"
    )

    status = DiagnosticStatus(status_value)

    # ----------------------------------------------
    # Choose response text
    # ----------------------------------------------

    question = result.get("question")
    message = result.get("message")

    if question:
        response_text = question

    elif message:
        response_text = message

    else:
        response_text = (
            "Let's continue troubleshooting the device."
        )

    return ChatResponse(
        response=response_text,
        session_id=session_id,
        diagnosis=DiagnosisResult(
            device=device,
            problem=problem,
            likely_cause=result.get("cause"),
            confidence=confidence,
            status=status,
            action=action_type,
        ),
    )


# --------------------------------------------------
# Handle verification
# --------------------------------------------------

def process_verification(
    session: dict,
    session_id: str,
    device: str,
    problem: str,
    user_message: str,
):
    """
    Handles the user's answer after Fix-Mate
    proposes that the problem has been solved.
    """

    answer = normalize_answer(
        "verification",
        user_message,
    )

    pending_result = session.get("pending_result")

    # --------------------------------------------------
    # User confirms that the problem is solved
    # --------------------------------------------------

    if answer == "yes":

        session["verification_pending"] = False
        session["pending_result"] = None
        session["current_step"] = None

        confidence = pending_result.get("confidence")

        if confidence:
            confidence = ConfidenceLevel(confidence)

        return ChatResponse(
            response=(
                "Great! The problem appears to be solved. "
                "The fan is working normally now."
            ),
            session_id=session_id,
            diagnosis=DiagnosisResult(
                device=device,
                problem=problem,
                likely_cause=pending_result.get("cause"),
                confidence=confidence,
                status=DiagnosticStatus.SOLVED,
                action=ActionType.SOLVED,
            ),
        )

    # --------------------------------------------------
    # User says the problem is NOT solved
    # --------------------------------------------------

    if answer == "no":

        session["verification_pending"] = False
        session["pending_result"] = None

        return ChatResponse(
            response=(
                "Thanks for confirming. "
                "The problem is not fully resolved, "
                "so let's continue troubleshooting."
            ),
            session_id=session_id,
            diagnosis=DiagnosisResult(
                device=device,
                problem=problem,
                status=DiagnosticStatus.DIAGNOSING,
                action=ActionType.ASK_QUESTION,
            ),
        )

    # --------------------------------------------------
    # User gave an unclear verification answer
    # --------------------------------------------------

    return ChatResponse(
        response=(
            "Please let me know whether the fan is working "
            "normally now. You can answer yes or no."
        ),
        session_id=session_id,
        diagnosis=DiagnosisResult(
            device=device,
            problem=problem,
            status=DiagnosticStatus.DIAGNOSING,
            action=ActionType.ASK_QUESTION,
        ),
    )


# --------------------------------------------------
# Chat endpoint
# --------------------------------------------------

@router.post(
    "/chat",
    response_model=ChatResponse
)
def chat(request: ChatRequest):

    # ==================================================
    # STEP 1
    # Start a new conversation
    # ==================================================

    if (
        request.session_id is None
        or request.session_id == "string"
    ):

        # ----------------------------------------------
        # First check for immediate safety problems
        # ----------------------------------------------

        safety_result = check_safety(
            request.message
        )

        if not safety_result.is_safe:

            session_id = str(uuid4())

            # Save unsafe session too
            sessions[session_id] = {
                "device": None,
                "problem": None,
                "safety_pending": False,
                "current_step": None,
                "verification_pending": False,
                "pending_result": None,
            }

            return ChatResponse(
                response=safety_result.message,
                session_id=session_id,
                diagnosis=DiagnosisResult(
                    status=DiagnosticStatus.UNSAFE,
                    action=ActionType.STOP,
                ),
            )

        # ----------------------------------------------
        # Identify device and problem
        # ----------------------------------------------

        identified_problem = identify_problem(
            request.message
        )

        if not identified_problem:

            return ChatResponse(
                response=(
                    "I can help you troubleshoot that. "
                    "For this demo, let's start with a "
                    "standing fan that is not turning on."
                )
            )

        device = identified_problem["device"]
        problem = identified_problem["problem"]

        # ----------------------------------------------
        # Start diagnostic engine
        # ----------------------------------------------

        result = start_diagnosis(
            device,
            problem
        )

        session_id = str(uuid4())

        # ----------------------------------------------
        # Save diagnostic session
        # ----------------------------------------------

        sessions[session_id] = {
            "device": device,
            "problem": problem,

            # Safety state
            "safety_pending": True,

            # Current diagnostic step
            "current_step": None,

            # Verification state
            "verification_pending": False,
            "pending_result": None,
        }

        # ----------------------------------------------
        # Return first safety question
        # ----------------------------------------------

        return ChatResponse(
            response=result["question"],
            session_id=session_id,
            diagnosis=DiagnosisResult(
                device=device,
                problem=problem,
                status=DiagnosticStatus.DIAGNOSING,
                action=ActionType.ASK_QUESTION,
            ),
        )

    # ==================================================
    # STEP 2
    # Continue existing conversation
    # ==================================================

    session_id = request.session_id

    session = sessions.get(session_id)

    if not session:

        return ChatResponse(
            response=(
                "This diagnostic session could not be found. "
                "Please start a new troubleshooting session."
            )
        )

    device = session["device"]
    problem = session["problem"]

    # ==================================================
    # STEP 3
    # Process verification answer
    # ==================================================

    if session.get("verification_pending"):

        return process_verification(
            session,
            session_id,
            device,
            problem,
            request.message,
        )

    # ==================================================
    # STEP 4
    # Process safety answer
    # ==================================================

    if session.get("safety_pending"):

        answer = normalize_answer(
            "safety_check",
            request.message,
        )

        result = process_safety_answer(
            device,
            problem,
            answer,
        )

        # ----------------------------------------------
        # Safety problem detected
        # ----------------------------------------------

        if result.get("status") == "unsafe":

            session["safety_pending"] = False

            return build_diagnosis_response(
                result,
                session_id,
                device,
                problem,
            )

        # ----------------------------------------------
        # Safety check passed
        # Move to first diagnostic step
        # ----------------------------------------------

        if result.get("step_id"):

            session["safety_pending"] = False

            session["current_step"] = result["step_id"]

            return build_diagnosis_response(
                result,
                session_id,
                device,
                problem,
            )

        return build_diagnosis_response(
            result,
            session_id,
            device,
            problem,
        )

    # ==================================================
    # STEP 5
    # Process normal diagnostic answer
    # ==================================================

    current_step = session.get("current_step")

    # Safety protection:
    # We should never process an answer if there
    # is no diagnostic step available.

    if not current_step:

        return ChatResponse(
            response=(
                "I'm not sure which diagnostic step "
                "we are currently on. Please start "
                "a new troubleshooting session."
            ),
            session_id=session_id,
        )

    # ----------------------------------------------
    # Normalize natural-language answer
    # ----------------------------------------------

    answer = normalize_answer(
        current_step,
        request.message,
    )

    # ----------------------------------------------
    # Send normalized answer to diagnostic engine
    # ----------------------------------------------

    result = process_answer(
        device,
        problem,
        current_step,
        answer,
    )

    # ==================================================
    # STEP 6
    # Move to next diagnostic step
    # ==================================================

    if result.get("status") == "diagnosing":

        if result.get("step_id"):

            session["current_step"] = result["step_id"]

        return build_diagnosis_response(
            result,
            session_id,
            device,
            problem,
        )

    # ==================================================
    # STEP 7
    # A possible solution was found
    # ==================================================

    if result.get("status") == "solved":

        # ----------------------------------------------
        # DO NOT immediately mark the problem solved.
        #
        # Store the proposed result and ask the user
        # to verify it.
        # ----------------------------------------------

        session["verification_pending"] = True

        session["pending_result"] = result

        return ChatResponse(
            response=(
                result.get("message", "")
                + "\n\n"
                + "Does the fan work normally now?"
            ),
            session_id=session_id,
            diagnosis=DiagnosisResult(
                device=device,
                problem=problem,
                likely_cause=result.get("cause"),
                confidence=(
                    ConfidenceLevel(result["confidence"])
                    if result.get("confidence")
                    else None
                ),
                # Important:
                # It is NOT solved yet.
                status=DiagnosticStatus.DIAGNOSING,
                action=ActionType.ASK_QUESTION,
            ),
        )

    # ==================================================
    # STEP 8
    # Technician escalation
    # ==================================================

    if result.get("status") == "escalated":

        session["current_step"] = None

        return build_diagnosis_response(
            result,
            session_id,
            device,
            problem,
        )

    # ==================================================
    # STEP 9
    # Fallback
    # ==================================================

    return build_diagnosis_response(
        result,
        session_id,
        device,
        problem,
    )