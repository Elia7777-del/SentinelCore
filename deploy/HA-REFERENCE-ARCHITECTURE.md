# SentinelCore High-Availability Reference Architecture

Recommended production topology:

Internet / private WAN
        |
   WAF / DDoS protection
        |
   Load Balancer
      /   \
   API-1  API-2
      \   /
   PostgreSQL HA
   + encrypted backups
        |
   Redis/queue cluster
        |
  Detection workers
        |
 Agent fleet / security integrations

Requirements:
- At least two API instances.
- Load balancer health checks.
- Database replication/failover appropriate to the organization's RTO/RPO.
- Queue durability for security events.
- Separate management plane from public ingress where practical.
- Centralized monitoring of SentinelCore itself.
- Infrastructure-as-code and repeatable recovery.
- No public database exposure.
