from sqlalchemy import Column, String, Boolean, DateTime, Text
from datetime import datetime
from app.db.session import Base

class Organization(Base):
    __tablename__ = "organizations"
    id = Column(String(36), primary_key=True)
    name = Column(String(200), nullable=False, unique=True)
    active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Per-org AI Security Analyst provider config. If ai_api_url is unset,
    # analysis falls back to the deployment-wide default provider (or to
    # deterministic-only output if that isn't configured either).
    # ai_api_key_encrypted is never stored or returned in plaintext --
    # see app.services.secrets_crypto.
    ai_enabled = Column(Boolean, default=True, nullable=False)
    ai_api_url = Column(String(500), nullable=True)
    ai_api_key_encrypted = Column(Text, nullable=True)
    ai_model = Column(String(200), nullable=True)

    # Per-org detection tuning: which rule IDs are disabled, and
    # threshold overrides (e.g. failed-login count for credential
    # stuffing). Stored as JSON text, same convention as
    # SecurityEvent.payload_json. See app.services.org_detection_config.
    detection_config_json = Column(Text, nullable=True)

class Agent(Base):
    __tablename__ = "agents"
    id = Column(String(36), primary_key=True)
    organization_id = Column(String(36), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    token_hash = Column(String(255), nullable=False)
    token_expires_at = Column(DateTime, nullable=True)
    active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
