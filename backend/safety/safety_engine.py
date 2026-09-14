
from typing import List

from models.schemas import ActionType


# --------------------------------------------------
# Safety red flags
# --------------------------------------------------

SAFETY_RED_FLAGS = {
    "sparks": [
        "spark",
        "sparks",
        "sparking",
    ],
    "smoke": [
        "smoke",
        "smoking",
    ],
    "burning_smell": [
        "burning smell",
        "burnt smell",
        "smells burnt",
        "smell of burning",
    ],
    "electric_shock": [
        "electric shock",
        "got shocked",
        "shocked me",
        "shock",
    ],
    "exposed_wires": [
        "exposed wire",
        "exposed wires",
        "bare wire",
        "bare wires",
    ],
    "damaged_cable": [
        "damaged cable",
        "cut cable",
        "cut wire",
        "broken cable",
        "frayed cable",
    ],
    "burnt_plug": [
        "burnt plug",
        "burned plug",
        "melted plug",
    ],
    "burnt_socket": [
        "burnt socket",
        "burned socket",
        "melted socket",
    ],
    "overheating": [
        "overheating",
        "extremely hot",
        "very hot",
    ],
}


# --------------------------------------------------
# Safety result
# --------------------------------------------------

class SafetyResult:
    """
    Represents the result of the safety check.
    """

    def __init__(
        self,
        is_safe: bool,
        detected_risks: List[str] | None = None,
        action: ActionType = ActionType.ASK_QUESTION,
        message: str = "",
    ):
        self.is_safe = is_safe
        self.detected_risks = detected_risks or []
        self.action = action
        self.message = message


# --------------------------------------------------
# Safety engine
# --------------------------------------------------

def check_safety(user_message: str) -> SafetyResult:
    """
    Checks a user's message for known safety red flags.

    Returns:
        SafetyResult containing:
        - whether it is safe to continue
        - detected risks
        - recommended action
        - safety message
    """

    message = user_message.lower()

    detected_risks = []

    for risk, keywords in SAFETY_RED_FLAGS.items():
        for keyword in keywords:
            if keyword in message:
                detected_risks.append(risk)
                break

    # --------------------------------------------------
    # Dangerous situation detected
    # --------------------------------------------------

    if detected_risks:
        return SafetyResult(
            is_safe=False,
            detected_risks=detected_risks,
            action=ActionType.STOP,
            message=(
                "I detected a potential safety issue. "
                "Please stop using the device and do not attempt "
                "to open or repair it yourself. "
                "A qualified technician should inspect it."
            ),
        )

    # --------------------------------------------------
    # No immediate safety risk detected
    # --------------------------------------------------

    return SafetyResult(
        is_safe=True,
        detected_risks=[],
        action=ActionType.ASK_QUESTION,
        message="No immediate safety risk was detected.",
    )

### How this fits into Fix-Mate

