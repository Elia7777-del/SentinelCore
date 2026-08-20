from sqlalchemy import Column, String, Text, DateTime, Integer
from datetime import datetime
from app.db.session import Base

class SecurityEvent(Base):
    __tablename__ = "security_events"
    id = Column(String(36), primary_key=True)
    organization_id = Column(String(36), nullable=False, index=True)
    agent_id = Column(String(36), nullable=True, index=True)
    event_type = Column(String(100), nullable=False)
    severity = Column(Integer, default=1, nullable=False)
    source = Column(String(200), nullable=True)
    summary = Column(String(500), nullable=False)
    payload_json = Column(Text, nullable=False)
    received_at = Column(DateTime, default=datetime.utcnow, nullable=False)
