# InventorAI

Private repository — active development.

## Status
Replay stabilization and governance infrastructure phase.
MVP progression engine: electronics/electrical domain, LEVEL 0-2.

## Key Documents
- `CLAUDE.md` — engineering rules and governance contract
- `GOVERNANCE_MODEL.md` — authority hierarchy and known violations
- `MVP_SCOPE_FREEZE.md` — active scope freeze (read before any code change)
- `DECISION_PROGRESSION_MODEL.md` — proposed progression architecture (not implemented)

## Do Not
- Modify scoring without provenance proof
- Patch replay without classification
- Expand MVP scope without updating MVP_SCOPE_FREEZE.md

## Run and Verify

Reproducible test baseline (G-IRB Implementation-Readiness Baseline). This installs
the pinned dependencies into an **isolated** virtual environment (never the global
environment) and runs the governed test suite (the `tests/` directory):

```
./verify_baseline.sh
```

Pin the virtualenv location with `GIRB_VENV=/path/to/venv ./verify_baseline.sh`.
The runner uses strict shell behavior, records the Python/pip versions and the
resolved dependency set (`pip freeze`), and exits non-zero on any ungoverned test
failure or unexpected pass. The single accepted `ADR-003` expected failure
(`tests/test_f011_progression_quality_gate.py`) must remain `xfailed`.

This baseline is infrastructure only: it changes no application, engine, or product
behavior and remediates no security risk.

