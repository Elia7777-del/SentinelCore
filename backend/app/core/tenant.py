from fastapi import HTTPException

def assert_same_organization(resource_org_id: str, actor_org_id: str):
    if resource_org_id != actor_org_id:
        raise HTTPException(status_code=404, detail="Resource not found")

def scoped_query(query, model, organization_id: str):
    return query.filter(model.organization_id == organization_id)
