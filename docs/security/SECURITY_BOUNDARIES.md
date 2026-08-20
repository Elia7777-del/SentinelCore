# SentinelCore Security Boundaries

SentinelCore is a defensive cybersecurity platform.

## Authorized use
Only monitor, assess, isolate, block, or investigate assets for which the deploying
organization has authorization.

## Important boundaries
- No credential theft functionality.
- No unauthorized exploitation functionality.
- No persistence or evasion functionality.
- No destructive response by default.
- High-impact response requires explicit policy and, where configured, human approval.
- AI recommendations are advisory unless an organization explicitly enables a validated playbook.

## Production readiness
The repository is a development foundation. Production deployment requires threat modeling,
secure-code review, dependency scanning, penetration testing, performance testing, access-control
review, backup/recovery testing, privacy review, and applicable regulatory/security assessment.
