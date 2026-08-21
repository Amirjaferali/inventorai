# INFRA-G1-R1 — Hosting/Region Selection Recording + Bounded Render Deployment-Preparation Contract

## 0. Record identity (file-creation rules)

```text
File path:        docs/governance/INFRA_G1_R1_HOSTING_REGION_SELECTION_AND_RENDER_DEPLOYMENT_PREPARATION_CONTRACT.md
Purpose:          (A) durably record the Owner's hosting-provider and
                  production-region selections made under the authoritative
                  INFRA-G1-C contract; (B) define the exact bounded FUTURE
                  implementation/configuration contract for Render deployment
                  preparation.
Input contract:   INFRA_G1_C_PRODUCTION_INFRASTRUCTURE_PROVIDER_SELECTION_CONTRACT.md
                  (authoritative; per-surface Owner-decision mechanism §2; hosting
                  criteria §3; possible-code gates §9); the Owner-accepted Provider
                  Evaluation (read-only) and Render Implementation Diagnosis
                  (read-only); repository truth verified live for every recorded
                  technical fact (web/app.py `_resolve_db_path` / `_resolve_secret_key`
                  / `_is_production` / `_run_config` / `/health`;
                  engine/backup_service.py; web/observability.py;
                  engine/email_sender.py; requirements.txt; scripts/run_dependency_audit.py).
Output contract:  a durable selection record + a bounded future-implementation
                  contract. Provisions NOTHING; authorizes NO implementation, NO
                  deployment, NO PSRR item PASS, NO OPS-SM1 execution, NO
                  email/payment selection.
Prohibited:       implementing WSGI/dependencies/render.yaml; provisioning any
                  Render resource; DNS/TLS work; creating production secrets or
                  recording secret values; SQLite migration; inferring any
                  legal/tax/data-residency/sovereignty/compliance/commercial
                  conclusion from the Frankfurt selection; marking PSRR items PASS;
                  selecting email/payment providers; executing OPS-SM1.
Status:           GOVERNANCE-ONLY CANDIDATE (authoritative only if/when merged and
                  post-merge verified).
Base:             9b3bc28ebeea68963b836bb508141dc3228092f7 (PR #542 merge —
                  INFRA-G1-C, authoritative).
```

## 1. Durable Owner selection record (mechanism: INFRA-G1-C §2 per-surface Owner decisions)

```text
OD-INFRA-1 — HOSTING PROVIDER:    RENDER          — OWNER SELECTED
OD-INFRA-2 — PRODUCTION REGION:   FRANKFURT       — OWNER SELECTED
FALLBACK (recorded, NOT selected): Fly.io remains the preferred fallback /
secondary option only, if portability or platform requirements later justify
migration. Its mention selects nothing.
```

Recorded Owner rationale (verbatim substance): compatibility with the current
Flask architecture and the current SQLite architecture via a persistent disk (no
database redesign); native Python support; managed HTTPS/TLS; lower operational
burden than a self-managed VM/cloud path; acceptable portability; Frankfurt as the
preferred currently available Render region for the intended global/GCC-first
launch context. **No legal, tax, data-residency, sovereignty, compliance, or
commercial conclusion is drawn or implied by the Frankfurt selection** (OD-J1/J2
data-location neutrality preserved). The decision mechanism is INFRA-G1-C §2
(per-surface separate Owner decisions under the contract); the OD-INFRA-* labels
adopt the Owner's naming; `OWNER_DECISION_REGISTER.md` row additions remain the
established future housekeeping pattern (NB8) — the selections are binding from
this durable record upon merge. Remaining INFRA-G1-C surface decisions
(OD-INFRA-3 TLS/proxy approach, OD-INFRA-4 monitoring, OD-INFRA-5 backup,
OD-INFRA-6 production email) remain OPEN.

## 2. Exact authority of INFRA-G1-R1

This record does ONLY (A) the §1 recording and (B) the §5–§10 bounded
future-contract definition. Its existence does NOT provision infrastructure,
authorize implementation or deployment, mark any PSRR item PASS, complete PSRR,
activate OPS-SM1, activate email, or touch payment/MoR.

## 3. SQLite / persistent-disk contract (accepted diagnosis, repository-verified)

```text
CURRENT DB PATH OWNER:                    INVENTORAI_DB_PATH (web/app.py
                                          _resolve_db_path; production hard-fail
                                          when unset under INVENTORAI_ENV=production;
                                          both stores share the one file)
PLANNED RENDER MOUNT (planning value):    /var/data
PLANNED PRODUCTION DB PATH (planning):    /var/data/inventorai.sqlite
SQLITE ON RENDER:                         SUPPORTED
APP DATABASE MIGRATION REQUIRED:          NO
APPLICATION LOGIC CHANGE REQUIRED (SQLite): NO
```

The actual production value is NOT set here. The future provisioning gate MUST
verify: the DB file is physically inside the persistent mount; a write survives
restart; a write survives redeploy; single-instance behavior is preserved; no
second durable DB path exists; the production hard-fail on a missing
`INVENTORAI_DB_PATH` remains.

## 4. Production serving / WSGI contract (diagnosis truth recorded)

The current start path (`app.run(**_run_config())`, Flask built-in server,
`threaded=False` by governed decision, whose own docstring records it is not a
production deployment architecture) is **NOT acceptable as the public production
serving architecture** (PSRR item 9). Required future production posture: single
application instance; single worker; single thread; bind to the Render-provided
`PORT`; preserve the current SQLite concurrency assumptions exactly; no
application-logic redesign (`web.app:app` is importable as-is). The future
implementation gate MAY evaluate Gunicorn or another repository-justified
equivalent; **no specific dependency is pre-authorized here**. If Gunicorn is
selected there, that gate requires: a pinned dependency; the exact start command;
single-worker; single-thread; focused RED→GREEN evidence; and full governed
regression evidence where GOV-RBR1 requires it.
**RUNTIME IMPLEMENTATION: NOT AUTHORIZED BY THIS CANDIDATE.**

## 5. Render infrastructure artifacts (future; none created now)

| Artifact | Classification |
|---|---|
| Python version pin artifact (repo runs 3.11) | REQUIRED (at the implementation gate) |
| Start-command declaration (dashboard and/or artifact) | REQUIRED (at the implementation gate) |
| `render.yaml` infrastructure-as-code capture | OPTIONAL (recommended for portability/review; justify at the gate) |
| Infrastructure configuration documentation | REQUIRED (provisioning-gate evidence) |

No provider-specific coupling beyond infrastructure configuration is permitted;
application code remains provider-neutral.

## 6. Trusted proxy / TLS contract (diagnosis truth recorded)

```text
CURRENT FORWARDED-HEADER TRUST:      NONE (deliberate P10-SEC1 §12 posture)
CURRENT NEED FOR ProxyFix:           NO (no absolute-URL generation; no
                                     scheme/IP/host-dependent behavior; relative
                                     verification/reset links; no IP-keyed logic)
TRUSTED-PROXY CODE CHANGE REQUIRED:  NO
SECURE-COOKIE BEHAVIOR:              production-config driven
                                     (SESSION_COOKIE_SECURE=_is_production());
                                     compatible with platform-edge TLS
HSTS:                                REASSESSMENT ONLY after a trusted HTTPS
                                     context exists (RL-C4 trigger)
```

No ProxyFix, no HSTS, no TLS implementation in this candidate. Any future
forwarded-header trust requires a separate diagnosis if application behavior ever
starts depending on forwarded scheme/IP/host information (e.g., the future email
adapter's absolute base URL is to be served by explicit configuration, not proxy
trust).

## 7. Required production configuration (defined; NOT populated; no secret values recorded)

```text
REQUIRED:  INVENTORAI_ENV=production
           INVENTORAI_SECRET_KEY=<platform secret — value never recorded in the repository>
           INVENTORAI_DB_PATH=<persistent-disk path>
HEALTH CHECK: /health
REGION:       Frankfurt
SERVICE TYPE: single Render Web Service
PERSISTENT DISK: required (free-tier disks are excluded — evaluation-verified
                 30-day expiry makes them unusable for production)
DEFERRED:  email provider API key + sender identity; public base URL for email
           links (both at the future email gate); monitoring keys if a dedicated
           service is later chosen.
```

## 8. Health-check contract

`/health` (P10-OB1) is acceptable as the Render health-check path as-is: it
provides liveness plus local-database readiness, is unauthenticated,
side-effect-free and data-minimized (two bounded enum fields; no secrets, paths,
versions, or stack traces). No code change currently required. Future
provisioning evidence must prove HTTP 200 under the healthy state and 503 under a
real datastore failure where safe to test.

## 9. Backup / restore contract

Render-native snapshots are NOT claimed sufficient for PSRR (their capability and
schedule/retention remain UNVERIFIED against official documentation and must be
confirmed at provisioning). Future provider-tranche evidence MUST include: the
existing governed application backup capability (`engine/backup_service.py` —
consistent copy + `quick_check` validation, restore, parity report); an
off-provider backup copy; a production restore drill; parity/integrity
validation; provider snapshot capability confirmation; and retention values
consumed ONLY from the policy lane (no retention period is invented here).

## 10. Monitoring / alerting / logging contracts

**Monitoring (P10-OB1 ownership preserved):** future Render preparation must
establish evidence for `/health` monitoring, platform metrics/log visibility, an
external uptime check if required, alert routing, and the P10-IR1 escalation
path. No external monitoring provider is selected here. **PSRR ITEMS 21–22:
REMAIN OPEN.** **Logging:** the current structured JSON stdout/stderr logging
(`web/observability.py`) is compatible with Render log streams; platform logs
are NOT durable and are not called durable; future evidence must determine actual
retention, export path, sensitive-data handling, policy dependency, and any
off-platform sink requirement. **PSRR items 26/28 remain open.**

## 11. Email separation

```text
EMAIL PROVIDER REQUIRED BEFORE INITIAL INFRASTRUCTURE PROVISIONING: NO
EMAIL PROVIDER REQUIRED BEFORE PUBLIC RELEASE:                      YES
    (the released product includes the verified-email account flows —
     registration verification, recovery, verified-email-gated export —
     which cannot operate publicly on the in-memory dev sink)
```

Production email remains a separate Owner decision/gate (OD-INFRA-6). No
provider (Resend/SES/Postmark/other) is selected; no adapter change is made.

## 12. OPS-SM1 relationship

OPS-SM1 remains **REGISTERED ONLY** (INFRA-G1-C §10). Render appears structurally
capable of supporting scheduled dependency/security scans, and
`scripts/run_dependency_audit.py` does NOT require access to the persistent
application disk (it reads `requirements.txt` from the repository checkout and
the network) — so the platform cron/no-disk limitation is irrelevant to it. No
cron jobs are created, nothing is scheduled, no automated alerts are enabled, no
automatic production updates are authorized. OPS-SM1 execution remains a later
gate.

## 13. Future bounded implementation scope (the NEXT implementation candidate boundary)

IN SCOPE (each under GOV-RBR1 with focused evidence): the production WSGI
dependency (evaluated and pinned per §4); exact start-command support; the Python
runtime/version pin if required; the minimum infrastructure artifact if required;
focused tests/evidence proving import/start assumptions; no application-logic
redesign. EXPLICITLY EXCLUDED: database migration; domain-model changes; auth
redesign; payment; tax; email-provider implementation; monitoring-provider
implementation; backup-provider implementation; HSTS; ProxyFix unless a new
diagnosis proves necessity; public deployment.

## 14. Future provisioning scope (after the §13 gate is separately accepted and authoritative)

Render Web Service creation; Frankfurt region; paid production-capable instance;
persistent disk; production environment variables; health check; build/start
configuration; **non-public verification deployment** (no DNS, no announcement);
persistence tests (restart + redeploy); TLS/Secure-cookie verification;
backup/restore evidence; monitoring evidence. **This candidate does NOT authorize
that provisioning** — it requires its own Owner authorization.

## 15. PSRR mapping (nothing marked PASS)

This gate + the §13/§14 successors feed, without passing, the remaining items:
9 (posture resolved at the §13 gate), 10 and 11-reassessment (platform TLS at
provisioning), 17–19 (backup/restore/DR evidence at provisioning), 21–22
(monitoring evidence), 26/28 (ops + policy), 31–32 (infrastructure/deployment
configuration + environment separation), 34-environment, and the production
halves of 7/8/14/23/24/25. Preserved verbatim: **APPLICATION-LAYER TRANCHE:
AUTHORITATIVE EVIDENCE; PSRR COMPLETE: NO; PSRR GO ELIGIBLE: NO.**

## 16. Observation carry-forward (none silently resolved)

INFRA-REV-O1 / INFRA-REV-O2 / INFRA-REV-O3 (INFRA-G1-C Independent-Review
non-blocking observations — carried by identifier as received); PSRR-C1-N1/N2/N3;
REV-REC-O1/O2/O3; application-layer OBS-1…OBS-4 residuals; GAP-SYNC-01-NB1/NB2;
PC3-N2; the nine application-tranche residual-risk entries.

## 17. Review path

LEVEL 2 governance-only candidate (zero runtime/test/schema/guardrail diff) under
LEAN §3/§4; Independent External Review mandatory per §5B.13 (incl. the mandatory
independent Universal Guardrail Smoke); no mechanical full-suite rerun absent a
§5B.6 trigger; no silent tier change (§5B.14).
