from pydantic import BaseModel, EmailStr, constr
from typing import Dict, Optional
from datetime import datetime

class ModerateTextRequest(BaseModel):
    email: EmailStr
    text: constr(min_length=1, max_length=1000)


class ModerateTextResponse(BaseModel):
    classification: str
    confidence: float
    reasoning: str

class ModerateImageResponse(BaseModel):
    classification: str
    confidence: float
    reasoning: str

class AnalyticsSummaryResponse(BaseModel):
    email: str
    total_requests: int
    classification_counts: Dict[str, int]
    last_request_at: Optional[datetime]