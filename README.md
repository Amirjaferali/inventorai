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

No email variable is required to boot: the application starts, serves and stays
healthy with no email provider configured. Configuring one is optional at boot
and required before public use — see "Email" below.

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
in-memory sink; production never does, under any configuration.

Production email is **Resend over its HTTPS API** (OD-INFRA-6), reached through
the standard library only — there is no provider SDK and no extra runtime
dependency. All four variables below are required together:

| Variable | Value | Notes |
|---|---|---|
| `INVENTORAI_EMAIL_PROVIDER` | `resend` | any other value selects no provider |
| `INVENTORAI_RESEND_API_KEY` | provider API key | platform secret store only — never in the repository, never in a log, never on a command line |
| `INVENTORAI_EMAIL_FROM` | verified sender identity, e.g. `InventorAI <no-reply@your-domain>` | must be a sender the provider has verified for your domain |
| `INVENTORAI_PUBLIC_BASE_URL` | absolute `https://` origin of the public service | the ONLY source of the links in verification and reset messages |

`INVENTORAI_PUBLIC_BASE_URL` is a required part of the email configuration
because a verification message whose link is relative is not a usable message.
It must be an absolute `https://` **origin** — scheme, host and optional port,
nothing more. A trailing slash is normalized away; a path prefix
(`https://host/app`) is rejected, because the application is served at the root
and such a value would silently generate links that 404 for every user.
It is never derived from a request: no request host and no proxy-supplied
forwarded header can influence an emailed link, because a caller-controlled host
would let an attacker mint a verification link pointing at their own origin.

**Partial configuration fails closed.** If any of the four is missing, blank or
malformed, production uses a sender that cannot deliver, and the email-dependent
account actions (registration, verification resend, password recovery) refuse
with `503` rather than claiming a message was sent. There is no fallback to the
development sink. Everything else, including the whole anonymous journey, is
unaffected.

**A configured provider that fails is different.** Delivery is available, so the
request proceeds and the account is still created — a provider outage must not
cost a user their registration. The anonymous surfaces then say only that an
attempt was made, never that a message was delivered, and their response stays
byte-identical for every address. The signed-in resend surface reports the
outcome truthfully, because the caller's own identity is already known there.

**Known limitation — response TIMING is not yet constant.** The byte-identical
response above hides account existence from the response *content*, but not from
how long the request takes: the provider is contacted only on the branch where a
message is actually due, so a request for an address that exists takes about one
provider round trip longer than one for an address that does not. Measured with
a 200 ms simulated provider: `/recover` answers in ~205 ms for a known active
address and ~2 ms for an unknown one. Treat the anonymous surfaces as protecting
account existence against response *inspection*, not against *timing analysis*.

Closing it is an architectural decision, not a small fix, and is open rather than
silently accepted. Padding every anonymous response to a fixed deadline is the
only purely synchronous option, and it is self-defeating here: `gunicorn.conf.py`
pins `workers = 1` and `threads = 1`, so a deadline long enough to mask a
provider round trip (let alone a timeout) would hold the single request thread
for that whole period on an unauthenticated route — trading an information leak
for an availability one. The alternatives (moving delivery off the request path,
or contacting the provider on every branch) need their own decision: the first
introduces asynchronous delivery, and the second would send mail to addresses
that have no account.

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

### Off-provider backup (Cloudflare R2)

A backup that lives only on the hosting provider's disk does not survive losing
that provider or that account. `scripts/inventorai_offsite_backup.py` copies one
off, composed from the same backup service plus an HTTPS uploader — no second
backup engine, and the standard library only (no `boto3`):

```
python scripts/inventorai_offsite_backup.py daily  <live-database>
python scripts/inventorai_offsite_backup.py upload <existing-backup> [--key KEY]
```

`daily` is the schedulable command: it takes a consistent backup of the live
database (read-only), validates it, uploads it, and removes the temporary local
copy in every outcome, including failure — so a repeating schedule cannot fill
the disk. It exits `0` only when the provider accepted the object; `3` on a
backup failure and `4` on a configuration or upload failure.

| Variable | Value |
|---|---|
| `INVENTORAI_R2_ACCOUNT_ID` | Cloudflare account id (forms the endpoint host) |
| `INVENTORAI_R2_BUCKET` | destination bucket |
| `INVENTORAI_R2_ACCESS_KEY_ID` | R2 access key id |
| `INVENTORAI_R2_SECRET_ACCESS_KEY` | R2 secret access key |
| `INVENTORAI_R2_PREFIX` | optional object-key prefix |

Credentials come from the environment only — never a file, never an argument, so
none reaches shell history or the process list. Absent configuration fails closed
and names only the missing variable.

**No retention, and no deletion.** There is no code path anywhere in this tool
that can remove, expire or overwrite a stored object: retention duration is an
unresolved policy question, and inventing one here would be a policy decision
this repository has no authority to make. Objects therefore accumulate until a
retention decision exists. **A provider snapshot is also not this**: a persistent
disk snapshot is provider-local and proves nothing about surviving loss of the
provider or the account.

Not activated by this repository: no schedule, cron job, bucket or credential is
created here. Turning the daily run on is a separate operator action.

### Auditing the dependencies actually installed in the image

`scripts/run_dependency_audit.py` audits `requirements.txt`. That resolves the
latest versions compatible with the pins, which are not necessarily the
transitive versions baked into a built image. To audit the deployed artifact
itself, capture its installed set from the running container and audit that:

```
# 1. capture the exact installed set from the image/container
docker exec <container> python -m pip freeze > image-requirements.txt

# 2. audit that captured set (pip-audit is TOOLING, never a runtime dependency)
python -m pip install pip-audit           # in a throwaway environment
python -m pip_audit -r image-requirements.txt
```

Two limitations, stated rather than implied: the captured file is evidence of
one point in time, because advisory databases change; and this covers Python
packages only — the image's operating-system packages (the Pango/HarfBuzz/
Fontconfig stack and the base image itself) are outside its scope and are not
audited by it.

