# SentinelCore Cyber Backgrounds

Added self-contained cyber-themed backgrounds for Dashboard, Network, Threat Detection,
AI Security, Incident Response, SOC, Forensics, Vulnerability Management, Assets and Reports.

Usage:

```python
from sentinelcore.ui_backgrounds import set_background, cyber_header

set_background("network")
cyber_header("NETWORK SECURITY", "NETWORK MONITORING")
```

Available sections:
`dashboard`, `network`, `threats`, `ai`, `incidents`, `soc`, `forensics`,
`vulnerability`, `assets`, `reports`.

The SVG backgrounds are stored locally in `assets/`, so no external image URL is required.
