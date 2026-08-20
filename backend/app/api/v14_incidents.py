
from fastapi import APIRouter, Depends, HTTPException
from app.core.auth import current_user
from app.schemas.v14 import IncidentCreate

router = APIRouter(prefix="/api/v1/incidents", tags=["incidents"])

@router.post("", status_code=201)
def create_incident(payload: IncidentCreate, user=Depends(current_user)):
    # Production: persist through the repository's DB session and verify the
    # authenticated user belongs to payload.organization_id before writing.
    return {
        "id": "pending-persistence",
        "title": payload.title,
        "severity": payload.severity,
        "organization_id": payload.organization_id,
        "status": "detected"
    }
