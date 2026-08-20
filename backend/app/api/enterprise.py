import secrets
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from app.core.auth import current_user

router = APIRouter(prefix="/api/v1/enterprise", tags=["enterprise"])

class OrganizationCreate(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    sector: str = Field(min_length=2, max_length=100)

class EnrollmentRequest(BaseModel):
    label: str = Field(min_length=1, max_length=120)
    expires_hours: int = Field(default=24, ge=1, le=168)

@router.post("/organizations")
def create_organization(data: OrganizationCreate, user=Depends(current_user)):
    # Production implementation must persist the organization and enforce
    # authorization for who can create organizations.
    return {
        "status": "accepted",
        "organization": data.model_dump(),
        "note": "Connect this contract to the production Organization model and audit creation."
    }

@router.post("/agents/enrollment-token")
def create_enrollment_token(data: EnrollmentRequest, user=Depends(current_user)):
    token = secrets.token_urlsafe(32)
    # Never log the returned token. Production should persist only a hash,
    # bind it to organization/issuer/expiry and make it single-use.
    return {
        "token": token,
        "expires_hours": data.expires_hours,
        "label": data.label,
        "warning": "Display once. Store only a hash server-side."
    }
