# SentinelCore Disaster Recovery

Define organizational RPO/RTO before deployment.

Minimum controls:
1. Encrypted daily database backups.
2. Frequent point-in-time recovery where supported.
3. Backup integrity verification.
4. Off-site/independent backup copy.
5. Tested restoration procedure.
6. Documented emergency administrator access.
7. Agent reconnect/retry behavior after central outage.
8. Incident/event buffering at the collection layer.
9. Quarterly restore exercises or a frequency mandated by policy.
10. Record recovery test results.

Never claim disaster recovery is operational until restoration has actually been tested.
