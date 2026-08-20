from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field

class EventIn(BaseModel):
    event_type: str = Field(min_length=1, max_length=100)
    severity: int = Field(default=1, ge=1, le=10)
    source: str | None = Field(default=None, max_length=200)
    summary: str = Field(min_length=1, max_length=500)
    payload: dict[str, Any] = Field(default_factory=dict)

class EventOut(EventIn):
    id: str
    organization_id: str
    agent_id: str | None
    received_at: datetime
