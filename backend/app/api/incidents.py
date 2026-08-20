from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.auth import current_user
from app.models.incident import Incident
from app.models.user import User
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/incidents", tags=["incidents"])

class IncidentCreate(BaseModel):
    title: str = Field(min_length=3, max_length=300)
    severity: int = Field(default=1, ge=1, le=10)
    description: str | None = None

@router.post("", status_code=201)
def create_incident(
    data: IncidentCreate,
    user: User = Depends(current_user),
    db: Session = Depends(get_db),
):
    row = Incident(
        id=str(uuid4()),
        organization_id=user.organization_id,
        title=data.title,
        severity=data.severity,
        description=data.description,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return {
        "id": row.id,
        "organization_id": row.organization_id,
        "title": row.title,
        "severity": row.severity,
        "status": row.status,
    }

@router.get("")
def list_incidents(
    user: User = Depends(current_user),
    db: Session = Depends(get_db),
):
    rows = db.query(Incident).filter(
        Incident.organization_id == user.organization_id
    ).order_by(Incident.updated_at.desc()).limit(200).all()
    return [
        {
            "id": x.id,
            "title": x.title,
            "severity": x.severity,
            "status": x.status,
            "created_at": x.created_at,
            "updated_at": x.updated_at,
        } for x in rows
    ]
