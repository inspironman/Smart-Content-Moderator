from sqlmodel import SQLModel, Field
import datetime

class ModerationRequest(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_email: str  # new field for user email
    content_type: str
    content_hash: str
    status: str
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)


class ModerationResult(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    request_id: int = Field(foreign_key="moderationrequest.id")
    classification: str
    confidence: float
    reasoning: str
    llm_response: str

class NotificationLog(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    request_id: int = Field(foreign_key="moderationrequest.id")
    channel: str
    status: str
    sent_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
