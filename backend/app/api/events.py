import json
from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.tenant import Agent
from app.models.event import SecurityEvent
from app.schemas.events import EventIn, EventOut
from app.services.security import verify_token
from app.core.auth import current_user

router = APIRouter(prefix="/api/v1/events", tags=["events"])

def authenticate_agent(
    x_sentinel_agent_token: str | None = Header(default=None),
    db: Session = Depends(get_db),
):
    if not x_sentinel_agent_token:
        raise HTTPException(status_code=401, detail="Missing agent token")
    agents = db.query(Agent).filter(Agent.active == True).all()
    now = datetime.utcnow()
    for agent in agents:
        if agent.token_expires_at and agent.token_expires_at < now:
            continue
        if verify_token(x_sentinel_agent_token, agent.token_hash):
            return agent
    raise HTTPException(status_code=401, detail="Invalid or expired agent token")

@router.post("", response_model=EventOut, status_code=201)
def ingest_event(
    event: EventIn,
    agent: Agent = Depends(authenticate_agent),
    db: Session = Depends(get_db),
):
    row = SecurityEvent(
        id=str(uuid4()),
        organization_id=agent.organization_id,
        agent_id=agent.id,
        event_type=event.event_type,
        severity=event.severity,
        source=event.source,
        summary=event.summary,
        payload_json=json.dumps(event.payload),
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return EventOut(
        id=row.id,
        organization_id=row.organization_id,
        agent_id=row.agent_id,
        event_type=event.event_type,
        severity=event.severity,
        source=event.source,
        summary=event.summary,
        payload=event.payload,
        received_at=row.received_at,
    )

@router.get("", response_model=list[EventOut])
def list_events(
    user=Depends(current_user),
    db: Session = Depends(get_db),
):
    rows = db.query(SecurityEvent).filter(
        SecurityEvent.organization_id == user.organization_id
    ).order_by(SecurityEvent.received_at.desc()).limit(500).all()

    return [
        EventOut(
            id=row.id,
            organization_id=row.organization_id,
            agent_id=row.agent_id,
            event_type=row.event_type,
            severity=row.severity,
            source=row.source,
            summary=row.summary,
            payload=json.loads(row.payload_json),
            received_at=row.received_at,
        ) for row in rows
    ]
