# SentinelCore Production Go-Live Checklist

A company should not put SentinelCore into production until the responsible security owner
signs off each applicable control.

## Identity
- [ ] MFA enabled for privileged users
- [ ] RBAC tested
- [ ] Tenant/organization isolation tested
- [ ] Session timeout and logout verified
- [ ] Break-glass account protected and audited

## Infrastructure
- [ ] HTTPS/TLS certificate installed
- [ ] PostgreSQL not Internet-exposed
- [ ] Firewall rules reviewed
- [ ] Secrets stored in approved secret manager
- [ ] OS/container patching process established
- [ ] Monitoring and alerting configured

## Data
- [ ] Encryption at rest enabled where required
- [ ] Backup schedule configured
- [ ] Restore test completed
- [ ] Retention policy approved
- [ ] Privacy/data-processing review completed

## Detection and response
- [ ] Detection rules validated with controlled tests
- [ ] False-positive review completed
- [ ] Response playbooks approved
- [ ] High-impact actions require correct approval
- [ ] Endpoint isolation tested safely
- [ ] Evidence integrity tested

## Assurance
- [ ] Dependency scan completed
- [ ] SAST completed
- [ ] DAST completed
- [ ] Penetration test completed
- [ ] Incident-response exercise completed
- [ ] Disaster-recovery exercise completed
- [ ] Independent security review completed where required

## Operational acceptance
- [ ] SOC ownership defined
- [ ] On-call/escalation contacts defined
- [ ] SLAs/SLOs defined
- [ ] User training completed
- [ ] Change-management process approved
