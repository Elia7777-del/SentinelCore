# SentinelCore Company Onboarding Runbook

## Phase 1 — Preparation
- Define the organization's legal/administrative owner.
- Define security administrators and SOC roles.
- Identify critical assets and data classifications.
- Define incident severity and response approval levels.
- Define retention, privacy and regulatory requirements.

## Phase 2 — Deployment
1. Provision a dedicated production host/cluster.
2. Configure a private database network.
3. Configure HTTPS/TLS and DNS.
4. Configure production secrets using an approved secret manager.
5. Start API/database/web services.
6. Verify `/api/v1/health`.
7. Configure backup and restoration.
8. Configure monitoring.

## Phase 3 — Endpoint onboarding
1. Create an organization.
2. Generate a short-lived enrollment token.
3. Install a signed SentinelCore agent.
4. Enroll the endpoint.
5. Verify heartbeat and telemetry.
6. Assign asset owner/criticality.
7. Apply security policy.

## Phase 4 — Security operations
- Monitor the incident queue.
- Review critical/high alerts.
- Investigate correlated events.
- Approve or execute containment according to policy.
- Record evidence and analyst actions.
- Close incidents only after validation.

## Production rule
Do not connect production endpoints until the agent package, update mechanism,
authentication, logging, isolation controls and response playbooks have been
security tested and approved by the deploying organization.
