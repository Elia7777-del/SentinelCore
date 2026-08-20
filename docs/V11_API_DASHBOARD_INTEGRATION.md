# SentinelCore v11 — API-connected Dashboard

The dashboard now attempts to use the authenticated SentinelCore API first.

## API endpoints

- `GET /api/v1/dashboard/metrics`
- `GET /api/v1/incidents?limit=10`
- `GET /api/v1/events?limit=20`
- `GET /api/v1/agents?limit=20`
- `GET /api/v1/health`

The browser sends a Bearer access token when one has been configured in the local
dashboard session. The API must enforce authentication, RBAC and organization/tenant
scope on every endpoint.

## API configuration

Use the `API` button in the dashboard to set the API base URL.

For same-origin deployment, `/api/v1` is the recommended base.

## Important

The dashboard has a safe demo fallback when the API is unavailable. This is useful for
presentation/development, but real production dashboards must use authenticated APIs and
must never treat demo data as real security telemetry.

Before production:
- Replace placeholder aggregate queries with real database queries.
- Add organization-scoped authorization to every endpoint.
- Add pagination and server-side filtering.
- Apply rate limiting.
- Use HTTPS.
- Do not store long-lived privileged credentials in browser localStorage.
- Prefer secure, short-lived sessions and appropriate cookie protections.
