
import json
from pathlib import Path
from typing import Any, Optional


# --------------------------------------------------
# Load diagnostic knowledge
# --------------------------------------------------

KNOWLEDGE_FILE = (
    Path(__file__).resolve().parent.parent
    / "knowledge"
    / "diagnostics.json"
)


def load_knowledge() -> dict:
    """
    Loads the diagnostic knowledge from diagnostics.json.
    """

    with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


KNOWLEDGE_BASE = load_knowledge()


# --------------------------------------------------
# Find a device
# --------------------------------------------------

def get_device(device: str) -> Optional[dict]:
    """
    Returns the knowledge for a specific device.
    """

    return KNOWLEDGE_BASE.get("devices", {}).get(device)


# --------------------------------------------------
# Find a problem
# --------------------------------------------------

def get_problem(device: str, problem: str) -> Optional[dict]:
    """
    Returns the knowledge for a specific problem
    belonging to a device.
    """

    device_data = get_device(device)

    if not device_data:
        return None

    return device_data.get("problems", {}).get(problem)


# --------------------------------------------------
# Find a diagnostic step
# --------------------------------------------------

def get_step(
    device: str,
    problem: str,
    step_id: str
) -> Optional[dict]:
    """
    Finds a diagnostic step by its ID.
    """

    problem_data = get_problem(device, problem)

    if not problem_data:
        return None

    for step in problem_data.get("diagnostic_steps", []):
        if step.get("id") == step_id:
            return step

    return None


# --------------------------------------------------
# Start a diagnosis
# --------------------------------------------------

def start_diagnosis(
    device: str,
    problem: str
) -> dict:
    """
    Starts a new diagnostic session.

    Returns the first safety question.
    """

    problem_data = get_problem(device, problem)

    if not problem_data:
        return {
            "success": False,
            "message": "I don't have diagnostic information for this problem yet."
        }

    safety_check = problem_data.get("safety_check")

    return {
        "success": True,
        "device": device,
        "problem": problem,
        "status": "diagnosing",
        "step_type": "safety_check",
        "question": safety_check.get("question"),
        "options": safety_check.get("options", [])
    }


# --------------------------------------------------
# Process safety answer
# --------------------------------------------------

def process_safety_answer(
    device: str,
    problem: str,
    answer: str
) -> dict:
    """
    Processes the user's answer to the safety question.

    Safety takes priority over diagnosis.
    """

    normalized_answer = answer.lower().strip()

    if normalized_answer == "yes":
        return {
            "success": True,
            "status": "unsafe",
            "action": "stop",
            "message": (
                "I detected a potential safety issue. "
                "Please stop using the device and do not attempt "
                "to open or repair it yourself. "
                "A qualified technician should inspect it."
            )
        }

    if normalized_answer == "not sure":
        return {
            "success": True,
            "status": "unsafe",
            "action": "stop",
            "message": (
                "Because you're not sure whether there is a safety issue, "
                "I don't recommend continuing with the repair yourself. "
                "Please have a qualified technician inspect the device."
            )
        }

    if normalized_answer == "no":
        problem_data = get_problem(device, problem)

        first_step = problem_data["diagnostic_steps"][0]

        return {
            "success": True,
            "status": "diagnosing",
            "step_type": first_step["type"],
            "step_id": first_step["id"],
            "question": first_step.get("question"),
        }

    return {
        "success": False,
        "status": "diagnosing",
        "message": (
            "I couldn't understand that safety answer. "
            "Please answer yes, no, or I'm not sure."
        )
    }


# --------------------------------------------------
# Process diagnostic answer
# --------------------------------------------------

def process_answer(
    device: str,
    problem: str,
    step_id: str,
    answer: str
) -> dict:
    """
    Processes an answer to a diagnostic question and determines
    what should happen next.
    """

    step = get_step(device, problem, step_id)

    if not step:
        return {
            "success": False,
            "message": "Diagnostic step not found."
        }

    normalized_answer = answer.lower().strip()

    answers = step.get("answers", {})

    result = answers.get(normalized_answer)

    if not result:
        return {
            "success": False,
            "status": "diagnosing",
            "message": (
                "I couldn't match that answer to the available "
                "diagnostic options."
            )
        }

    # --------------------------------------------------
    # Diagnosis completed
    # --------------------------------------------------

    if "cause" in result:

        return {
            "success": True,
            "status": (
                "solved"
                if result.get("action") == "solved"
                else "escalated"
            ),
            "cause": result.get("cause"),
            "confidence": result.get("confidence"),
            "action": result.get("action"),
            "message": result.get("message")
        }

    # --------------------------------------------------
    # Move to next diagnostic step
    # --------------------------------------------------

    next_step_id = result.get("next_step")

    if not next_step_id:
        return {
            "success": False,
            "message": "No next diagnostic step was defined."
        }

    next_step = get_step(
        device,
        problem,
        next_step_id
    )

    if not next_step:
        return {
            "success": False,
            "message": "Next diagnostic step could not be found."
        }

    # --------------------------------------------------
    # Handle steps with a predefined result
    # --------------------------------------------------

    if next_step.get("result"):

        final_result = next_step["result"]

        return {
            "success": True,
            "status": "escalated",
            "cause": final_result.get("cause"),
            "confidence": final_result.get("confidence"),
            "action": final_result.get("action"),
            "message": final_result.get("message")
        }

    # --------------------------------------------------
    # Continue diagnosis
    # --------------------------------------------------

    return {
        "success": True,
        "status": "diagnosing",
        "step_type": next_step.get("type"),
        "step_id": next_step.get("id"),
        "question": next_step.get("question"),
    }

