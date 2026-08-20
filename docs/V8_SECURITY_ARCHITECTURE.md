# SentinelCore v8.0 Security Architecture

## Newly added foundations

### 1. Tenant isolation
Centralized helper and automated cross-tenant authorization tests prevent accidental
resource disclosure at the application layer. Every organization-owned query must be
scoped to the authenticated organization.

### 2. Tamper-evident audit chain
Audit events can be linked with SHA-256 hashes. For high assurance, the chain should be
periodically anchored into an immutable/WORM logging system controlled separately from the
SentinelCore application.

### 3. Signed agent releases
Ed25519 signature verification is provided for release manifests. The trusted public key
must be distributed out-of-band and protected from replacement.

### 4. Strong authentication path
TOTP MFA is implemented in v7. WebAuthn/security-key integration is now explicitly defined
as a high-assurance extension. The placeholder endpoints intentionally return 501 rather
than pretending a secure WebAuthn ceremony exists.

### 5. HA and disaster recovery
Reference topologies and recovery procedures are included. These become operational only
after deployment-specific testing.

## Production gate

Before real deployment:
- Complete WebAuthn with a vetted library.
- Perform application, API, infrastructure and agent penetration testing.
- Test tenant isolation with automated and manual tests.
- Deploy centralized secrets management.
- Configure immutable audit storage.
- Implement HA and verify failover.
- Execute and document disaster-recovery tests.
- Implement signed updater end-to-end.
- Conduct privacy, legal, regulatory and organizational security review.
