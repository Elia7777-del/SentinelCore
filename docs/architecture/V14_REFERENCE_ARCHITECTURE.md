# V14 Reference Architecture

Internet/Corporate Network
        |
   WAF / Load Balancer
        |
   Web Dashboard
        |
   Authenticated API
   /      |       \
 DB   Event Queue   Detection/Correlation
 |         |             |
Audit   Workers       Threat Intel
 |
Backup / Recovery

Endpoints and authorized security devices send telemetry through authenticated,
short-lived enrollment and mutually authenticated transport where implemented.

Every organization-scoped operation must enforce authorization at the API/database layer.
