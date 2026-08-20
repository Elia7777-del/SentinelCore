
from datetime import datetime
from pydantic import BaseModel, Field

class IncidentCreate(BaseModel):
    title: str = Field(min_length=3, max_length=255)
    severity: str = Field(pattern="^(critical|high|medium|low|informational)$")
    organization_id: str

class IncidentOut(IncidentCreate):
    id: str
    status: str
    created_at: datetime
    model_config = {"from_attributes": True}
