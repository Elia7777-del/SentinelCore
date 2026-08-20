# SentinelCore Remote & Multi-Organization Architecture

## Goal

SentinelCore is structured so the web interface and central security services can run on a
secured server/cloud environment instead of only on the developer's PC or one local network.

## High-level flow

Internet / Private Connectivity
        |
      HTTPS
        |
   API Gateway / WAF
        |
   SentinelCore API
        |
  Event / Detection Pipeline
        |
     Database
        |
     SOC UI

Authorized organizations connect through a SentinelCore agent or other explicitly configured
integration. The agent should make an authenticated outbound connection to the central service.

## Multi-tenant isolation

Every security event and agent record is associated with an `organization_id`.

Production implementation must enforce tenant filtering at every read/write boundary, not merely
at the user-interface layer. Recommended production controls include:

- Database row-level security where supported.
- Separate encryption keys or key scopes for tenants where appropriate.
- Organization-scoped RBAC.
- Centralized authorization middleware.
- Audit logs for tenant access.
- Automated authorization tests.
- No cross-tenant identifiers exposed to clients unless necessary.

## Remote access

The central web/API endpoint should be exposed through HTTPS with:

- TLS certificates issued by a trusted authority.
- Firewall rules.
- WAF/API gateway.
- MFA for human users.
- Short-lived access tokens.
- Agent token rotation and revocation.
- Rate limiting.
- Central audit logging.
- Secure secret management.

Do not expose the database directly to the Internet.

## Agent model

Agents collect only authorized telemetry and send it over an authenticated encrypted channel.
The agent should not open inbound ports merely to report events.

The reference agent in this repository is intentionally small. Production agents require:

- Signed packages.
- Secure update mechanism.
- Local tamper resistance.
- Device identity.
- Token/certificate rotation.
- Offline buffering.
- Retry/backoff.
- Resource limits.
- Privacy controls.
- Organization-approved collection policies.

## Important production boundary

The included code is a development foundation, not a claim that the platform is already a
production national SOC. Before real deployment, complete security review, penetration testing,
privacy/legal review, load testing, backup/restore testing, high-availability design, secret
management, independent assessment, and applicable certification/compliance processes.
