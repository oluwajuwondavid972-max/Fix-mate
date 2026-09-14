
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class DiagnosticStatus(str, Enum):
    DIAGNOSING = "diagnosing"
    SOLVED = "solved"
    ESCALATED = "escalated"
    UNSAFE = "unsafe"


class ConfidenceLevel(str, Enum):
    HIGH = "high"
    MODERATE = "moderate"
    LOW = "low"


class ActionType(str, Enum):
    ASK_QUESTION = "ask_question"
    GUIDE_REPAIR = "guide_repair"
    TECHNICIAN_REFERRAL = "technician_referral"
    STOP = "stop"
    SOLVED = "solved"


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


class DiagnosisResult(BaseModel):
    device: Optional[str] = None
    problem: Optional[str] = None
    likely_cause: Optional[str] = None
    confidence: Optional[ConfidenceLevel] = None
    status: DiagnosticStatus = DiagnosticStatus.DIAGNOSING
    action: ActionType = ActionType.ASK_QUESTION


class ChatResponse(BaseModel):
    response: str
    diagnosis: Optional[DiagnosisResult] = None
    session_id: Optional[str] = None