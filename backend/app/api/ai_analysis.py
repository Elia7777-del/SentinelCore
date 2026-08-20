import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import current_user
from app.db.session import get_db
from app.models.event import SecurityEvent
from app.models.incident import Incident
from app.models.tenant import Organization
from app.models.user import User
from app.schemas.ai_analysis import AIAnalysisOut, AIAnalysisRequest
from app.services.ai_security_analyst import analyze_event

router = APIRouter(prefix="/api/v1/ai-analysis", tags=["ai-analysis"])

_SEVERITY_TO_INT = {"Info": 1, "Low": 3, "Medium": 5, "High": 7, "Critical": 10}


@router.post("/events/{event_id}", response_model=AIAnalysisOut)
def analyze_security_event(
    event_id: str,
    body: AIAnalysisRequest = AIAnalysisRequest(),
    user: User = Depends(current_user),
    db: Session = Depends(get_db),
):
    """Runs Detection Engine -> Threat/Vulnerability Intelligence ->
    AI Security Analyst -> Risk Score for a stored event, scoped to the
    caller's organization. Uses that organization's own AI credentials
    and detection tuning if configured (see /api/v1/org/*). Optionally
    opens an Incident from the result.
    """
    row = (
        db.query(SecurityEvent)
        .filter(
            SecurityEvent.id == event_id,
            SecurityEvent.organization_id == user.organization_id,
        )
        .first()
    )
    if row is None:
        raise HTTPException(status_code=404, detail="Event not found")

    org = db.query(Organization).filter(Organization.id == user.organization_id).first()

    result = analyze_event(row, org=org, asset_criticality=body.asset_criticality)
    if result is None:
        return AIAnalysisOut(event_id=event_id, matched=False)

    incident_id = None
    if body.create_incident:
        mitre_ids = ", ".join(t["id"] for t in result["mitre_attack"]) or "N/A"
        incident = Incident(
            id=str(uuid.uuid4()),
            organization_id=user.organization_id,
            title=f"{result['threat']} ({result['severity']})",
            severity=_SEVERITY_TO_INT.get(result["severity"], 5),
            status="detected",
            description=(
                f"{result['vulnerability']}\n\n"
                f"Impact: {result['impact']}\n"
                f"Immediate containment: {result['immediate_containment']}\n"
                f"CWE: {result['cwe']} | CVE: {result['cve']}\n"
                f"MITRE ATT&CK: {mitre_ids}\n"
                f"Confidence: {result['confidence']}% | Risk score: {result['risk_score']}"
            ),
        )
        db.add(incident)
        db.commit()
        db.refresh(incident)
        incident_id = incident.id

    result_fields = {k: v for k, v in result.items() if k != "event_id"}
    return AIAnalysisOut(
        event_id=event_id, matched=True, incident_id=incident_id, **result_fields
    )
