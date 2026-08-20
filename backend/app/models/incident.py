from sqlalchemy import Column, String, Integer, Text, DateTime
from datetime import datetime
from app.db.session import Base

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(String(36), primary_key=True)
    organization_id = Column(String(36), nullable=False, index=True)
    title = Column(String(300), nullable=False)
    severity = Column(Integer, default=1, nullable=False)
    status = Column(String(40), default="detected", nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
