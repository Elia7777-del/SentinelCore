# SentinelCore v10.0 Web Platform

## Added
- Responsive cybersecurity command-center dashboard
- Cyber/grid visual background generated with CSS
- Overview metrics
- Threat activity visualization
- Priority incident panel
- Asset risk panel
- Live-style security event stream
- Responsive desktop/tablet/mobile layout
- Theme toggle
- Static web deployment instructions

## Security boundary
The dashboard currently contains demo presentation data. Before production use:
- Connect it to authenticated SentinelCore APIs.
- Enforce RBAC on every API request.
- Do not expose sensitive evidence to unauthorized browser users.
- Apply CSP and production security headers at the reverse proxy.
- Use HTTPS only.
- Add CSRF protection where cookie authentication is used.
- Implement session timeout and secure logout.
