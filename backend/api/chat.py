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


# ==================================================
# ACTIVE DIAGNOSTIC SESSIONS
# ==================================================

sessions = {}


# ==================================================
# PROBLEM IDENTIFICATION
# ==================================================

def identify_problem(message: str):

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


# ==================================================
# BUILD DIAGNOSIS RESPONSE
# ==================================================

def build_diagnosis_response(
    result: dict,
    session_id: str,
    device: str,
    problem: str,
):

    action = result.get("action")

    if action == "stop":

        action_type = ActionType.STOP

    elif action == "technician_referral":

        action_type = ActionType.TECHNICIAN_REFERRAL

    elif action == "solved":

        action_type = ActionType.SOLVED

    else:

        action_type = ActionType.ASK_QUESTION

    confidence = result.get("confidence")

    if confidence:

        confidence = ConfidenceLevel(confidence)

    status_value = result.get(
        "status",
        "diagnosing"
    )

    status = DiagnosticStatus(status_value)

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


# ==================================================
# VERIFICATION
# ==================================================

def process_verification(
    session: dict,
    session_id: str,
    device: str,
    problem: str,
    user_message: str,
):

    answer = normalize_answer(
        "verification",
        user_message,
    )

    pending_result = session.get(
        "pending_result"
    )

    # ==================================================
    # USER CONFIRMS THE FIX WORKED
    # ==================================================

    if answer == "yes":

        session["verification_pending"] = False
        session["pending_result"] = None
        session["current_step"] = None

        confidence = None

        if pending_result:

            confidence_value = pending_result.get(
                "confidence"
            )

            if confidence_value:

                confidence = ConfidenceLevel(
                    confidence_value
                )

        return ChatResponse(

            response=(
                "Great! The problem appears to be solved. "
                "The fan is working normally now."
            ),

            session_id=session_id,

            diagnosis=DiagnosisResult(

                device=device,

                problem=problem,

                likely_cause=(
                    pending_result.get("cause")
                    if pending_result
                    else None
                ),

                confidence=confidence,

                status=DiagnosticStatus.SOLVED,

                action=ActionType.SOLVED,

            ),
        )

    # ==================================================
    # USER SAYS THE PROBLEM IS STILL THERE
    # ==================================================

    if answer == "no":

        session["verification_pending"] = False
        session["pending_result"] = None

        # Restart the diagnostic process.
        # This gives the session a valid diagnostic
        # path instead of leaving it on the old step.

        result = start_diagnosis(
            device,
            problem
        )

        session["safety_pending"] = True
        session["current_step"] = None

        return ChatResponse(

            response=(
                "Thanks for confirming. "
                "Since the problem is still present, "
                "let's go through the checks again "
                "to look for another possible cause.\n\n"
                + result["question"]
            ),

            session_id=session_id,

            diagnosis=DiagnosisResult(

                device=device,

                problem=problem,

                status=DiagnosticStatus.DIAGNOSING,

                action=ActionType.ASK_QUESTION,

            ),
        )

    # ==================================================
    # UNCLEAR ANSWER
    # ==================================================

    return ChatResponse(

        response=(
            "Please let me know whether the fan is "
            "working normally now. You can answer "
            "yes or no."
        ),

        session_id=session_id,

        diagnosis=DiagnosisResult(

            device=device,

            problem=problem,

            status=DiagnosticStatus.DIAGNOSING,

            action=ActionType.ASK_QUESTION,

        ),
    )


# ==================================================
# CHAT ENDPOINT
# ==================================================

@router.post(
    "/chat",
    response_model=ChatResponse
)
def chat(request: ChatRequest):

    # ==================================================
    # START NEW SESSION
    # ==================================================

    if (
        request.session_id is None
        or request.session_id == "string"
    ):

        # ----------------------------------------------
        # SAFETY ENGINE
        # ----------------------------------------------

        safety_result = check_safety(
            request.message
        )

        if not safety_result.is_safe:

            session_id = str(uuid4())

            return ChatResponse(

                response=safety_result.message,

                session_id=session_id,

                diagnosis=DiagnosisResult(

                    status=DiagnosticStatus.UNSAFE,

                    action=ActionType.STOP,

                ),
            )

        # ----------------------------------------------
        # IDENTIFY DEVICE / PROBLEM
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
        # START DIAGNOSIS
        # ----------------------------------------------

        result = start_diagnosis(
            device,
            problem
        )

        session_id = str(uuid4())

        # ----------------------------------------------
        # CREATE SESSION
        # ----------------------------------------------

        sessions[session_id] = {

            "device": device,

            "problem": problem,

            "safety_pending": True,

            "current_step": None,

            "verification_pending": False,

            "pending_result": None,

        }

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
    # EXISTING SESSION
    # ==================================================

    session_id = request.session_id

    session = sessions.get(
        session_id
    )

    if not session:

        return ChatResponse(

            response=(
                "This diagnostic session could not "
                "be found. Please start a new "
                "troubleshooting session."
            )

        )

    device = session["device"]

    problem = session["problem"]

    # ==================================================
    # VERIFICATION HAS PRIORITY
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
    # SAFETY QUESTION
    # ==================================================

    if session["safety_pending"]:

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
        # UNSAFE
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
        # MOVE TO FIRST DIAGNOSTIC STEP
        # ----------------------------------------------

        if result.get("step_id"):

            session["safety_pending"] = False

            session["current_step"] = (
                result["step_id"]
            )

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
    # NORMAL DIAGNOSTIC STEP
    # ==================================================

    current_step = session["current_step"]

    answer = normalize_answer(

        current_step,

        request.message,

    )

    result = process_answer(

        device,

        problem,

        current_step,

        answer

    )

    # ==================================================
    # STILL DIAGNOSING
    # ==================================================

    if result.get("status") == "diagnosing":

        if result.get("step_id"):

            session["current_step"] = (
                result["step_id"]
            )

    # ==================================================
    # POSSIBLE SOLUTION FOUND
    # ==================================================

    elif result.get("status") == "solved":

        # ----------------------------------------------
        # DO NOT MARK AS SOLVED YET
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

                likely_cause=result.get(
                    "cause"
                ),

                confidence=(

                    ConfidenceLevel(
                        result["confidence"]
                    )

                    if result.get("confidence")

                    else None

                ),

                status=DiagnosticStatus.DIAGNOSING,

                action=ActionType.ASK_QUESTION,

            ),
        )

    # ==================================================
    # TECHNICIAN REFERRAL
    # ==================================================

    elif result.get("status") == "escalated":

        session["current_step"] = None

    # ==================================================
    # RETURN RESPONSE
    # ==================================================

    return build_diagnosis_response(

        result,

        session_id,

        device,

        problem,

    )