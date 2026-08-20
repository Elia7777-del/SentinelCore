from fastapi import HTTPException
from app.core.tenant import assert_same_organization

def test_same_tenant_is_allowed():
    assert_same_organization("org-a", "org-a")

def test_cross_tenant_is_denied():
    try:
        assert_same_organization("org-a", "org-b")
        assert False, "Expected cross-tenant access to be denied"
    except HTTPException as exc:
        assert exc.status_code == 404
