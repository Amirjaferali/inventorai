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

## Runtime security configuration

The web runtime (`web/app.py`) reads its security-sensitive settings from
environment variables with safe defaults (G-SC0 Bounded Security Containment). No
secret value is hard-coded in source, and debug is off by default.

| Variable | Purpose | Accepted values | Default |
|---|---|---|---|
| `INVENTORAI_SECRET_KEY` | Flask session secret | any non-empty string | (see below) |
| `INVENTORAI_ENV` | explicit runtime mode | `production` enables production mode; anything else is development | development |
| `INVENTORAI_DEBUG` | enable the dev-server debugger | explicit truthy: `1`, `true`, `yes`, `on` (case-insensitive) enable it; every other or unknown value keeps it off | off |
| `INVENTORAI_HOST` | dev-server bind host | any host string | `127.0.0.1` |

Secret behavior:

- In **production** mode (`INVENTORAI_ENV=production`), `INVENTORAI_SECRET_KEY`
  must be set to a non-empty value; otherwise configuration fails clearly.
- In **local development** (the default), if `INVENTORAI_SECRET_KEY` is not set, an
  **ephemeral random** secret is generated per process; it is never persisted or
  logged. This is a development convenience only.

Debug defaults to **off** and is enabled only by an explicit recognized truthy
value; ambiguous or unknown values never enable it. The dev server binds to
`127.0.0.1` unless `INVENTORAI_HOST` is set.

This section documents runtime configuration only. It is not deployment guidance
and makes no production-readiness claim.

