# SentinelCore AI Repository Index

## Identity
- Name: SentinelCore
- Version: 4.0.0
- Proposal version: 4.0
- Author: ERICKSON KENEDY TENGA
- Primary entry point: app.py
- Web UI: streamlit_app.py

## Source-of-truth documents
- `docs/PROJECT_PROPOSAL.md` — comprehensive project proposal
- `docs/architecture/SYSTEM_ARCHITECTURE.md` — architecture
- `docs/security/SECURITY_BOUNDARIES.md` — security boundaries

## Main modules
- `sentinelcore/core/models.py` — domain models
- `sentinelcore/core/risk.py` — contextual risk scoring
- `sentinelcore/security/rbac.py` — roles and authorization
- `sentinelcore/security/audit.py` — append-only audit records
- `sentinelcore/collectors/events.py` — event normalization
- `sentinelcore/detection/engine.py` — defensive detections
- `sentinelcore/incidents/manager.py` — incident lifecycle
- `sentinelcore/response/policy.py` — response governance
- `sentinelcore/intelligence/feeds.py` — threat-intelligence primitives
- `sentinelcore/forensics/evidence.py` — evidence hashing
- `sentinelcore/reporting/security_report.py` — report generation
- `scanner/` — authorized network/local assessment foundation

## Development rule
When adding a feature, update the relevant module, tests, documentation and this index.
Do not enable destructive or high-impact automated actions without explicit policy, authorization,
testing and human-approval controls where appropriate.
