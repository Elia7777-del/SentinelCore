# SentinelCore v12.0 — Enterprise Deployment Edition

## Goal

Provide a repeatable deployment foundation for a real organization, including web/API,
private database, organization onboarding, agent enrollment workflow, health checks,
deployment scripts and operational runbooks.

## Reference topology

Users/SOC
   |
HTTPS + MFA/SSO
   |
WAF / Load Balancer
   |
SentinelCore Web/API
   |
Internal network
   +---- PostgreSQL
   +---- Detection workers
   +---- Audit storage
   +---- Queue
   |
Authorized endpoints / network/security integrations

## v12 additions

- Enterprise Docker Compose reference deployment
- Database kept off the public host interface
- Health endpoint for operations/load balancers
- Organization onboarding API contract
- Short-lived agent enrollment token contract
- Linux and Windows agent onboarding helpers
- Prometheus monitoring configuration
- Company onboarding runbook
- Production installation script
- Explicit production security gates

## What still requires implementation/validation

This release is a deployment foundation, not a certified finished security product.
Before real company use, complete and validate:
- persistent organization and enrollment-token database models
- full RBAC and tenant isolation on every endpoint
- signed production agent binaries
- single-use hashed enrollment tokens
- full endpoint telemetry collection
- real detection rules and tested response playbooks
- WebAuthn/SSO integration as required
- centralized secrets management
- immutable audit storage
- HA database and queue
- backup/restore tests
- penetration testing and independent assessment
- privacy, regulatory and procurement review
