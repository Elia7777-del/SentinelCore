from datetime import datetime, timedelta
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.core.auth import require_roles
from app.db.session import get_db
from app.models.tenant import Agent
from app.models.user import User
from app.services.security import generate_agent_token, hash_token

router = APIRouter(prefix="/api/v1/agents", tags=["agents"])

class AgentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=200)

@router.post("", status_code=201)
def create_agent(
    data: AgentCreate,
    user: User = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
):
    token = generate_agent_token()
    row = Agent(
        id=str(uuid4()),
        organization_id=user.organization_id,
        name=data.name,
        token_hash=hash_token(token),
        token_expires_at=datetime.utcnow() + timedelta(days=30),
    )
    db.add(row)
    db.commit()
    return {
        "id": row.id,
        "name": row.name,
        "organization_id": row.organization_id,
        "agent_token": token,
        "expires_at": row.token_expires_at,
        "warning": "Store this token securely. It is returned only during provisioning.",
    }
