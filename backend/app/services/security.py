from datetime import datetime, timedelta, timezone
import hashlib
import secrets
import jwt
import pyotp
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)

def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()

def verify_token(token: str, token_hash: str) -> bool:
    return secrets.compare_digest(hash_token(token), token_hash)

def generate_agent_token() -> str:
    return secrets.token_urlsafe(48)

def generate_refresh_token() -> str:
    return secrets.token_urlsafe(64)

def create_mfa_secret() -> str:
    return pyotp.random_base32()

def verify_mfa_code(secret: str, code: str) -> bool:
    return bool(secret and pyotp.TOTP(secret).verify(code, valid_window=1))

def create_access_token(user_id: str, organization_id: str, role: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": user_id,
        "org": organization_id,
        "role": role,
        "type": "access",
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=settings.access_token_minutes)).timestamp()),
    }
    return jwt.encode(payload, settings.secret_key, algorithm="HS256")

def decode_access_token(token: str) -> dict:
    return jwt.decode(token, settings.secret_key, algorithms=["HS256"])
