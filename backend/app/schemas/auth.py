from pydantic import BaseModel, EmailStr, Field

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=12, max_length=200)
    mfa_code: str | None = Field(default=None, min_length=6, max_length=8)

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshRequest(BaseModel):
    refresh_token: str = Field(min_length=20)

class MFASetupResponse(BaseModel):
    secret: str
    otpauth_uri: str

class MFAVerifyRequest(BaseModel):
    code: str = Field(min_length=6, max_length=8)

class UserOut(BaseModel):
    id: str
    organization_id: str
    email: EmailStr
    role: str
    mfa_enabled: bool
