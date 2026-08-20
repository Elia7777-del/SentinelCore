from __future__ import annotations

from pydantic import BaseModel, Field


class AIAnalysisRequest(BaseModel):
    asset_criticality: str = Field(default="Medium")
    create_incident: bool = Field(default=False)


class AIAnalysisOut(BaseModel):
    event_id: str
    matched: bool
    incident_id: str | None = None

    schema_version: str | None = None
    threat: str | None = None
    vulnerability: str | None = None
    cve: str | None = None
    cwe: str | None = None
    severity: str | None = None
    confidence: int | None = None
    evidence: list[str] | None = None
    impact: str | None = None
    immediate_containment: str | None = None
    recommended_remediation: list[str] | None = None
    mitre_attack: list[dict[str, str]] | None = None
    verification: str | None = None
    risk_score: int | None = None
    risk_level: str | None = None
    ai_assisted: bool | None = None
    source_rules: list[str] | None = None
