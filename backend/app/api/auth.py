from datetime import datetime, timedelta
from uuid import uuid4
import pyotp
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.auth import current_user
from app.core.rate_limit import enforce_rate_limit
from app.db.session import get_db
from app.models.user import User
from app.models.session import RefreshSession
from app.schemas.auth import (
    LoginRequest, TokenResponse, RefreshRequest, UserOut,
    MFASetupResponse, MFAVerifyRequest
)
from app.services.security import (
    verify_password, create_access_token, generate_refresh_token,
    hash_token, create_mfa_secret, verify_mfa_code
)

router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])

@router.post("/login", response_model=TokenResponse)
def login(request: Request, data: LoginRequest, db: Session = Depends(get_db)):
    client = request.client.host if request.client else "unknown"
    enforce_rate_limit(f"login-ip:{client}", 10, 60)
    enforce_rate_limit(f"login-account:{data.email.lower()}", 10, 60)

    user = db.query(User).filter(User.email == data.email, User.active == True).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if user.mfa_enabled:
        if not data.mfa_code or not verify_mfa_code(user.mfa_secret, data.mfa_code):
            raise HTTPException(status_code=401, detail="Valid MFA code required")

    access = create_access_token(user.id, user.organization_id, user.role)
    refresh = generate_refresh_token()
    session = RefreshSession(
        id=str(uuid4()),
        user_id=user.id,
        organization_id=user.organization_id,
        token_hash=hash_token(refresh),
        expires_at=datetime.utcnow() + timedelta(days=settings.refresh_token_days),
    )
    db.add(session)
    db.commit()
    return TokenResponse(access_token=access, refresh_token=refresh)

@router.post("/refresh", response_model=TokenResponse)
def refresh(data: RefreshRequest, db: Session = Depends(get_db)):
    session = db.query(RefreshSession).filter(
        RefreshSession.token_hash == hash_token(data.refresh_token),
        RefreshSession.revoked == False,
    ).first()

    if not session or session.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    user = db.query(User).filter(
        User.id == session.user_id,
        User.organization_id == session.organization_id,
        User.active == True,
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    # Rotate refresh token.
    session.revoked = True
    new_refresh = generate_refresh_token()
    new_session = RefreshSession(
        id=str(uuid4()),
        user_id=user.id,
        organization_id=user.organization_id,
        token_hash=hash_token(new_refresh),
        expires_at=datetime.utcnow() + timedelta(days=settings.refresh_token_days),
    )
    db.add(new_session)
    db.commit()

    return TokenResponse(
        access_token=create_access_token(user.id, user.organization_id, user.role),
        refresh_token=new_refresh,
    )

@router.post("/logout")
def logout(data: RefreshRequest, db: Session = Depends(get_db)):
    session = db.query(RefreshSession).filter(
        RefreshSession.token_hash == hash_token(data.refresh_token)
    ).first()
    if session:
        session.revoked = True
        db.commit()
    return {"status": "logged_out"}

@router.post("/mfa/setup", response_model=MFASetupResponse)
def mfa_setup(user: User = Depends(current_user), db: Session = Depends(get_db)):
    secret = create_mfa_secret()
    user.mfa_secret = secret
    db.commit()
    uri = pyotp.TOTP(secret).provisioning_uri(
        name=user.email,
        issuer_name="SentinelCore",
    )
    return MFASetupResponse(secret=secret, otpauth_uri=uri)

@router.post("/mfa/enable")
def mfa_enable(
    data: MFAVerifyRequest,
    user: User = Depends(current_user),
    db: Session = Depends(get_db),
):
    if not user.mfa_secret or not verify_mfa_code(user.mfa_secret, data.code):
        raise HTTPException(status_code=400, detail="Invalid MFA code")
    user.mfa_enabled = True
    db.commit()
    return {"status": "mfa_enabled"}

@router.get("/me", response_model=UserOut)
def me(user: User = Depends(current_user)):
    return UserOut(
        id=user.id,
        organization_id=user.organization_id,
        email=user.email,
        role=user.role,
        mfa_enabled=user.mfa_enabled,
    )
