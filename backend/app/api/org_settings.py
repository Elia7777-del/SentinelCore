import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import current_user, require_roles
from app.db.session import get_db
from app.models.tenant import Organization
from app.models.user import User
from app.schemas.org_settings import (
    OrgAIConfigIn,
    OrgAIConfigOut,
    OrgDetectionConfigIn,
    OrgDetectionConfigOut,
)
from app.services.secrets_crypto import SecretEncryptionNotConfigured, encrypt_secret
from sentinelcore.detection.engine import ALL_RULE_IDS, DetectionConfig

router = APIRouter(prefix="/api/v1/org", tags=["org-settings"])


def _get_org(user: User, db: Session) -> Organization:
    org = db.query(Organization).filter(Organization.id == user.organization_id).first()
    if org is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org


# ---- AI provider config ----
# Every org gets deterministic detections regardless of this config (see
# sentinelcore.analysis.analyst); this only controls where the narrative
# layer's AI calls go and whether they happen at all for this org.

@router.get("/ai-config", response_model=OrgAIConfigOut)
def get_org_ai_config(
    user: User = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
):
    org = _get_org(user, db)
    return OrgAIConfigOut(
        ai_enabled=org.ai_enabled,
        ai_api_url=org.ai_api_url,
        ai_model=org.ai_model,
        has_api_key=bool(org.ai_api_key_encrypted),
    )


@router.put("/ai-config", response_model=OrgAIConfigOut)
def set_org_ai_config(
    body: OrgAIConfigIn,
    user: User = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
):
    org = _get_org(user, db)

    org.ai_enabled = body.ai_enabled
    org.ai_api_url = body.ai_api_url or None
    org.ai_model = body.ai_model or None

    # Only touch the stored key if a new one was actually supplied, so
    # toggling ai_enabled or changing the URL doesn't force re-entering
    # the key every time.
    if body.ai_api_key:
        try:
            org.ai_api_key_encrypted = encrypt_secret(body.ai_api_key)
        except SecretEncryptionNotConfigured as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc

    db.commit()
    db.refresh(org)
    return OrgAIConfigOut(
        ai_enabled=org.ai_enabled,
        ai_api_url=org.ai_api_url,
        ai_model=org.ai_model,
        has_api_key=bool(org.ai_api_key_encrypted),
    )


@router.delete("/ai-config/api-key", response_model=OrgAIConfigOut)
def clear_org_ai_api_key(
    user: User = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
):
    """Removes the stored key without touching the rest of the config
    (e.g. to fall back to the deployment-wide default provider)."""
    org = _get_org(user, db)
    org.ai_api_key_encrypted = None
    db.commit()
    db.refresh(org)
    return OrgAIConfigOut(
        ai_enabled=org.ai_enabled,
        ai_api_url=org.ai_api_url,
        ai_model=org.ai_model,
        has_api_key=False,
    )


# ---- Detection tuning ----

@router.get("/detection-config", response_model=OrgDetectionConfigOut)
def get_org_detection_config(
    user: User = Depends(current_user),
    db: Session = Depends(get_db),
):
    org = _get_org(user, db)
    parsed = json.loads(org.detection_config_json) if org.detection_config_json else None
    config = DetectionConfig.from_dict(parsed)
    return OrgDetectionConfigOut(
        disabled_rules=sorted(config.disabled_rules),
        cred_stuffing_failed_attempts=config.cred_stuffing_failed_attempts,
        exfil_bytes_out_threshold=config.exfil_bytes_out_threshold,
        available_rules=list(ALL_RULE_IDS),
    )


@router.put("/detection-config", response_model=OrgDetectionConfigOut)
def set_org_detection_config(
    body: OrgDetectionConfigIn,
    user: User = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
):
    unknown = [r for r in body.disabled_rules if r not in ALL_RULE_IDS]
    if unknown:
        raise HTTPException(status_code=400, detail=f"Unknown rule id(s): {unknown}")

    org = _get_org(user, db)
    org.detection_config_json = json.dumps(
        {
            "disabled_rules": body.disabled_rules,
            "thresholds": {
                "cred_stuffing_failed_attempts": body.cred_stuffing_failed_attempts,
                "exfil_bytes_out_threshold": body.exfil_bytes_out_threshold,
            },
        }
    )
    db.commit()
    db.refresh(org)
    return OrgDetectionConfigOut(
        disabled_rules=sorted(body.disabled_rules),
        cred_stuffing_failed_attempts=body.cred_stuffing_failed_attempts,
        exfil_bytes_out_threshold=body.exfil_bytes_out_threshold,
        available_rules=list(ALL_RULE_IDS),
    )
