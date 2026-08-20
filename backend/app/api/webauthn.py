from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from app.core.auth import current_user

router = APIRouter(prefix="/api/v1/auth/webauthn", tags=["webauthn"])

class RegistrationStart(BaseModel):
    display_name: str = Field(min_length=1, max_length=100)

class AssertionFinish(BaseModel):
    credential_id: str = Field(min_length=1, max_length=512)
    client_data_json: str = Field(min_length=1)
    authenticator_data: str = Field(min_length=1)
    signature: str = Field(min_length=1)

@router.post("/registration/start")
def registration_start(data: RegistrationStart, user=Depends(current_user)):
    # The complete WebAuthn ceremony requires browser credential APIs,
    # challenge persistence, origin/RP-ID validation and authenticator storage.
    raise HTTPException(
        status_code=501,
        detail="WebAuthn ceremony endpoint contract is defined; integrate a vetted WebAuthn library before production."
    )

@router.post("/assertion/finish")
def assertion_finish(data: AssertionFinish, user=Depends(current_user)):
    raise HTTPException(
        status_code=501,
        detail="WebAuthn verification requires a vetted server-side WebAuthn implementation and persisted credential metadata."
    )
