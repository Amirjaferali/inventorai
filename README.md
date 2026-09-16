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
| `INVENTORAI_DB_PATH` | path to the one SQLite database holding every durable table | any writable filesystem path | production: **required, no default**; development: an app-namespaced temporary path |
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

Database-path behavior:

- In **production** mode, `INVENTORAI_DB_PATH` must be set to a writable path;
  otherwise startup fails clearly. There is deliberately **no** production
  fallback: a silent fallback would put the database on container-local storage,
  where it looks durable and is destroyed on the next restart or redeploy.
- In **local development**, an app-namespaced path under the system temporary
  directory is used. It is never a repository-tracked file.

This section documents runtime configuration only. It is not deployment guidance
and makes no production-readiness claim.

## Production deployment contract (operator-facing)

This section is the single operator-facing description of what the application
requires to run in production. It describes configuration; it authorizes no
deployment and makes no production-readiness claim. The governing records remain
`docs/governance/INFRA_G1_R1_HOSTING_REGION_SELECTION_AND_RENDER_DEPLOYMENT_PREPARATION_CONTRACT.md`
(hosting/region selection) and
`docs/governance/INFRA_G1_P1_RENDER_PROVISIONING_NON_PUBLIC_VERIFICATION_CONTRACT.md`
(provisioning specification and verification).

### Required before first boot

| Variable | Value | Notes |
|---|---|---|
| `INVENTORAI_ENV` | `production` | enables the production hard-fails and the `Secure` session cookie |
| `INVENTORAI_SECRET_KEY` | operator-generated high-entropy value | platform secret store only — never in the repository, never in logs |
| `INVENTORAI_DB_PATH` | `<persistent-disk mount>/inventorai.sqlite` | **must** resolve inside the mounted persistent disk |
| `PORT` | supplied by the platform | read by `gunicorn.conf.py`; the operator does not set it |

No email variable is required to boot. Production email is a separate, not yet
taken decision; see "Email" below.

### Runtime

Build the image from the repository `Dockerfile`. Its default command is the
governed production start command, which can also be run directly:

```
gunicorn -c gunicorn.conf.py web.app:app
```

The health-check path is `/health`. It answers `200` while the local runtime
dependencies are usable and `503` on a real local dependency failure.

### Production invariants

- **Exactly one service instance.** No horizontal autoscaling, and no second
  instance may run against the same database.
- **One worker, one thread.** `gunicorn.conf.py` pins `workers = 1`,
  `threads = 1` and `preload_app = False`. These exist because the application
  uses one thread-bound SQLite connection; a second worker or thread would mean
  concurrent writers to a single SQLite file.
- **The database lives only on persistent storage.** Never point
  `INVENTORAI_DB_PATH` at a path inside the container filesystem: that storage is
  destroyed on restart, redeploy and instance replacement.
- **No second writer**, including during deploys. A deploy of a disk-backed
  service must stop the old instance before starting the new one.
- **Direct Output PDF needs OS packages**, not pip packages: Pango, HarfBuzz,
  Fontconfig and a font covering both Latin and Arabic (`fonts-dejavu-core`
  provides the "DejaVu Sans" family the PDF template selects). The `Dockerfile`
  installs them; any other image must too, or PDF rendering fails.
- **TLS terminates at the platform edge.** The application adds no TLS and
  trusts no forwarded header.

### Email

Production selects the sender by environment. Development and test use the
in-memory sink; production never does. Until a transactional-email provider is
selected and configured, production uses a sender that cannot deliver, and the
email-dependent account actions (registration, verification resend, password
recovery) **refuse with `503` rather than claiming that a message was sent**.
Everything else, including the whole anonymous journey, is unaffected. The
provider variables will be defined by that provider's adapter when it is chosen.

### Backup and restore

`scripts/inventorai_backup.py` is the operator entry point over the existing
backup service. Every path is explicit and nothing is inferred from the
environment:

```
python scripts/inventorai_backup.py validate <database>
python scripts/inventorai_backup.py backup  <source> <backup>
python scripts/inventorai_backup.py restore <backup> <new-target>
python scripts/inventorai_backup.py parity  <first> <second>
```

`restore` writes to a **separate** target and never overwrites an existing file
without an explicit `--overwrite`. Repointing `INVENTORAI_DB_PATH` at a verified
restore is a deliberate, separate step — see `docs/DISASTER_RECOVERY_PLAN.md`
Scenario 7 for the full procedure. A backup produced this way is a portable
SQLite file and is independent of any hosting provider's own snapshots.

