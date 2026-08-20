# SentinelCore Production Security Checklist

This repository is a development/architecture foundation. Complete and verify the following
before connecting real organizational environments.

## Identity
- [ ] MFA implemented and enforced for administrators.
- [ ] RBAC reviewed and tested.
- [ ] Password policy and account lockout/rate limiting implemented.
- [ ] Access-token rotation/revocation implemented.
- [ ] Session/device management implemented.

## Tenant isolation
- [ ] Every API query is organization-scoped.
- [ ] Cross-tenant access tests exist.
- [ ] Database-level isolation controls are considered.
- [ ] Organization-specific encryption/key management is designed where required.

## Agent security
- [ ] Unique identity per agent.
- [ ] Token/certificate rotation.
- [ ] Revocation.
- [ ] Signed agent packages.
- [ ] Secure update mechanism.
- [ ] Offline buffering and retry.
- [ ] Local tamper protection.
- [ ] Least-privilege execution.

## Infrastructure
- [ ] HTTPS only.
- [ ] Trusted TLS certificates.
- [ ] Database not Internet-facing.
- [ ] Firewall/WAF/API gateway.
- [ ] Secrets stored in a dedicated secret manager.
- [ ] Network segmentation.
- [ ] Centralized monitoring.

## Data protection
- [ ] Encryption at rest.
- [ ] Encryption in transit.
- [ ] Data retention policy.
- [ ] Privacy/legal review.
- [ ] Secure deletion.
- [ ] Evidence integrity controls.

## Resilience
- [ ] Automated backups.
- [ ] Tested restore procedure.
- [ ] High-availability architecture.
- [ ] Disaster recovery plan.
- [ ] Recovery time/recovery point objectives defined.

## Assurance
- [ ] Unit/integration/security tests.
- [ ] Dependency scanning.
- [ ] Static analysis.
- [ ] Container scanning.
- [ ] Penetration test.
- [ ] Independent security assessment.
- [ ] Applicable regulatory/certification review.

## Important
Do not interpret the presence of these files as evidence that every control is already implemented.
The checklist is a release gate for the engineering team.
