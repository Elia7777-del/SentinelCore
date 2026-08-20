from __future__ import annotations

from pydantic import BaseModel, Field


class OrgAIConfigIn(BaseModel):
    ai_enabled: bool = True
    ai_api_url: str | None = Field(default=None, max_length=500)
    # Plaintext on the wire (over HTTPS, admin-only) -- encrypted before
    # it ever touches the database. See app.services.secrets_crypto.
    ai_api_key: str | None = Field(default=None, max_length=2000)
    ai_model: str | None = Field(default=None, max_length=200)


class OrgAIConfigOut(BaseModel):
    ai_enabled: bool
    ai_api_url: str | None
    ai_model: str | None
    has_api_key: bool  # the key itself is never returned once stored


class OrgDetectionConfigIn(BaseModel):
    disabled_rules: list[str] = Field(default_factory=list)
    cred_stuffing_failed_attempts: int = Field(default=5, ge=1, le=1000)
    exfil_bytes_out_threshold: int = Field(default=500_000_000, ge=1)


class OrgDetectionConfigOut(BaseModel):
    disabled_rules: list[str]
    cred_stuffing_failed_attempts: int
    exfil_bytes_out_threshold: int
    available_rules: list[str]
