# INFRA-G1-P1 — Render Provisioning & Non-Public Verification Contract

## 0. Record identity (file-creation rules)

```text
File path:        docs/governance/INFRA_G1_P1_RENDER_PROVISIONING_NON_PUBLIC_VERIFICATION_CONTRACT.md
Purpose:          define EXACTLY what the Owner will configure for the FIRST real
                  Render resource, and EXACTLY what evidence must be captured
                  afterward, for a NON-PUBLICLY-RELEASED provisioning verification.
Input contract:   INFRA-G1-C (surface coordination + OPS-SM1 registration);
                  INFRA-G1-R1 (OD-INFRA-1 RENDER / OD-INFRA-2 FRANKFURT; bounded
                  deployment-preparation contracts); INFRA-G1-R2 (authoritative
                  serving implementation); PSRR registration §4/§5/§7/§9/§10;
                  PSRR-C1 §5.1/§5.2/§6/§7/§8; the authoritative PSRR
                  application-layer execution record; P10-RL1 checklist;
                  P10-SEC1 / P10-OB1 / P10-BR1 / RL-C1 boundary owners; OD-P;
                  D-PSRR-01; D-P8-PL-01 class C; OD-A.
Output contract:  a provisioning SPECIFICATION and a verification PROCEDURE.
                  Creates NO resource, configures NOTHING, executes NOTHING,
                  closes NO PSRR item, authorizes NO deployment.
Prohibited:       creating any Render resource or disk; DNS; custom TLS;
                  production secrets; production email; payment/MoR; runtime or
                  database change; SQLite migration; multi-worker/multi-thread/
                  horizontal scaling; ProxyFix; HSTS; OPS-SM1 execution; PSRR
                  completion or GO; public deployment; paid activation;
                  presenting any provider mechanic as verified without an
                  official source.
Status:           GOVERNANCE-ONLY CANDIDATE (authoritative only if/when merged
                  and post-merge verified).
Base:             5e68a59cefe8fa47b5fbc201387b1e785820a86a (PR #544 merge —
                  INFRA-G1-R2, authoritative).
```

**Execution boundary (binding).** This contract is a specification. Creating the Render
service, the disk, or any environment variable requires a SEPARATE Owner execution
authorization issued against this frozen contract.

## 1. Fixed Owner decisions (not reopened)

`OD-INFRA-1 HOSTING PROVIDER: RENDER` · `OD-INFRA-2 PRODUCTION REGION: FRANKFURT`
(durably recorded in INFRA-G1-R1; carried here unchanged). Fly.io remains the recorded
fallback only. The Frankfurt selection implies NO legal, tax, data-residency, sovereignty,
compliance, or commercial conclusion.

## 2. Authoritative runtime posture (VERIFIED — REPOSITORY/RUNTIME, re-read at this base)

| Fact | Value | Source (verified at `5e68a59c…`) |
|---|---|---|
| WSGI server | `gunicorn==26.1.0` (pinned) | `requirements.txt` |
| Start command | `gunicorn -c gunicorn.conf.py web.app:app` | `gunicorn.conf.py` docstring; test-pinned target |
| Workers / threads | `workers = 1` / `threads = 1` | `gunicorn.conf.py` |
| Preload / reload | `preload_app = False` / `reload = False` | `gunicorn.conf.py` |
| Port | `bind = "0.0.0.0:%s" % os.environ.get("PORT", "10000")` | `gunicorn.conf.py` |
| Python | `3.11` pin; tested on 3.11.15 | `.python-version`; test pins agreement with the running interpreter |
| Database | one SQLite file resolved solely from `INVENTORAI_DB_PATH`; production hard-fail when unset | `web/app.py` `_resolve_db_path` |
| Secret | `INVENTORAI_SECRET_KEY`; production hard-fail when unset | `web/app.py` `_resolve_secret_key` |
| Production flag | `INVENTORAI_ENV=production` enables hard-fails and `SESSION_COOKIE_SECURE` | `web/app.py` `_is_production` |
| Health surface | `/health` — unauthenticated, side-effect-free, two bounded enum fields; 200 healthy / 503 on real DB failure | `web/app.py health()` |
| Forwarded-header trust | NONE (deliberate) | `web/app.py`; P10-SEC1 §12 |
| Logging | structured JSON to stdout/stderr | `web/observability.py` |

`web/` and `engine/` are NOT modified by this gate.

## 3. Current PSRR provider/production mapping (RECONSTRUCTED from authority, not assumed)

Reconstructed from PSRR-C1 §5.2 and the authoritative application-layer execution record
§6, both re-read at this base. The current mapping is: **items 9, 10, 17, 18, 19, 21, 22,
26, 28, 31, 32, 34(environment)**, plus the **production halves of 7, 8, 14, 23, 24, 25**,
plus the **HSTS reassessment under item 11**. (This reconstruction reproduces the earlier
list exactly; it was re-derived from source rather than carried forward on trust.)

| PSRR item | Provable during INFRA-G1-P1 execution | Provable only after additional provider configuration | Deferred to a later PSRR gate |
|---|---|---|---|
| 9 production configuration | Partially — the real service configuration exists and can be reviewed | Full posture once monitoring/backup config exist | — |
| 10 TLS / secure transport | Partially — platform-terminated HTTPS observable on the service URL | Custom-domain TLS at the deployment lane | — |
| 11 HSTS reassessment | Reassessment INPUT only (a trusted HTTPS context exists) | Adoption decision + implementation (separately authorized) | Adoption |
| 14-prod datastore topology | Yes — the real disk-backed topology is observable | — | — |
| 7-prod / 8-prod secrets ops | Partially — env/secret store in use; rotation procedure drafted | Rotation drill + emergency procedure evidence | — |
| 17 backup verification | Partially — application-level backup can be produced on the instance | Provider snapshot capability + scheduling | — |
| 18 restore verification | Yes — restore into a scratch path + parity report | Provider-snapshot-based restore | — |
| 19 DR readiness | Partially — a first DR assessment against the real topology | Full DR with provider capabilities | — |
| 21 monitoring / 22 alerting | Platform-native visibility only, recorded honestly | Monitoring/alerting configuration + routing | Dedicated provider decision |
| 23–25-prod abuse/rate-limit posture | Observation of the current floor in production context | Edge/WAF posture once configured | Broad abuse controls |
| 26 audit-retention operations | NO — mechanism absent and retention substance is policy-open | Mechanism after design | Policy substance (adviser lane) |
| 28 production logging | Partially — log stream + sensitive-data review on real output | Retention/export sink | Retention substance |
| 31 infra/deployment configuration | Partially — build/deploy/rollback observed | CI/deploy pipeline at the deployment lane | — |
| 32 environment/secrets separation | Partially — one production environment exists | Separate non-production environment | — |
| 34 penetration testing | NO — only the risk determination | Production-like environment + testers | Testing itself |

**No PSRR item is closed by this contract.** Evidence produced under it is recorded as
provider-tranche evidence and assessed at items 35–37.

## 4. Render provisioning specification (Owner-configured; nothing created here)

**Provider-fact verification status (§5 discipline).** Official Render documentation is
**NOT reachable from the authoring environment** — the session egress proxy blocks
`render.com`, and a direct fetch was attempted and refused at authoring time. Therefore
**no Render mechanic below is classified `VERIFIED — OFFICIAL RENDER SOURCE`.** Everything
provider-specific is either `OWNER CONFIGURATION REQUIRED` (a value the Owner sets, derived
from repository truth) or `TO BE CONFIRMED DURING PROVISIONING` (a provider behaviour to be
observed and recorded). Indirect/secondary knowledge is NOT promoted to verified truth.

| # | Setting | Intended value | Classification |
|---|---|---|---|
| 1 | Service type | one Web Service, single instance | OWNER CONFIGURATION REQUIRED |
| 2 | Repository / branch | `Amirjaferali/inventorai`, branch `feature/atomic-json-session-persistence` (the authoritative governing branch; `main` is STALE/UNRECONCILED per OD-Q) | OWNER CONFIGURATION REQUIRED |
| 3 | Region | Frankfurt | OWNER CONFIGURATION REQUIRED (region immutability after creation: TO BE CONFIRMED DURING PROVISIONING) |
| 4 | Runtime | native Python | OWNER CONFIGURATION REQUIRED |
| 5 | Python version | `3.11` via the repository `.python-version` file | REPOSITORY/RUNTIME verified; platform acceptance of the major.minor form: TO BE CONFIRMED DURING PROVISIONING |
| 6 | Build command | `pip install -r requirements.txt` | OWNER CONFIGURATION REQUIRED |
| 7 | Start command | `gunicorn -c gunicorn.conf.py web.app:app` | REPOSITORY/RUNTIME verified (command); entry into the dashboard: OWNER CONFIGURATION REQUIRED |
| 8 | Health-check path | `/health` | REPOSITORY/RUNTIME verified |
| 9 | Persistent disk | attach one disk | OWNER CONFIGURATION REQUIRED (minimum/maximum size, resize semantics: TO BE CONFIRMED DURING PROVISIONING) |
| 10 | Disk mount path | `/var/data` (architecture target) | OWNER CONFIGURATION REQUIRED; final path CONFIRMED AT PROVISIONING and recorded |
| 11 | `INVENTORAI_DB_PATH` | `<mount>/inventorai.sqlite` — expected `/var/data/inventorai.sqlite`; MUST equal the actual mount | OWNER CONFIGURATION REQUIRED (blocking check §5) |
| 12 | `INVENTORAI_ENV` | `production` | REPOSITORY/RUNTIME verified requirement |
| 13 | `INVENTORAI_SECRET_KEY` | Owner-generated high-entropy value, platform secret store only | OWNER CONFIGURATION REQUIRED (value never in the repository) |
| 14 | Instance size | the smallest paid instance sufficient for the governed single-worker posture; **free tier excluded** (free-tier disks are not usable for production per the accepted evaluation) | OWNER CONFIGURATION REQUIRED (exact tier + price: TO BE CONFIRMED DURING PROVISIONING) |
| 15 | Auto-deploy | **OFF** (see §8) | OWNER CONFIGURATION REQUIRED |
| 16 | TLS termination | platform edge | TO BE CONFIRMED DURING PROVISIONING (observed, not assumed) |
| 17 | Proxy / forwarded headers | application trusts NONE; no proxy trust configured | REPOSITORY/RUNTIME verified (P10-SEC1 §12 preserved) |
| 18 | Custom domain / DNS | **NOT configured in this gate** | OUT OF SCOPE |
| 19 | Logging surface | platform log stream consuming stdout/stderr | TO BE CONFIRMED DURING PROVISIONING (retention/export: owed) |
| 20 | Snapshot/backup capability | unknown to this contract | TO BE CONFIRMED DURING PROVISIONING (never assumed from disk existence — §6) |
| 21 | Restart / redeploy behaviour | disk expected to persist; deploys of disk-backed services expected to interrupt briefly | TO BE CONFIRMED DURING PROVISIONING (§5 blocking checks) |
| 22 | Rollback / redeploy | previous-build redeploy | TO BE CONFIRMED DURING PROVISIONING |

Nothing above is `UNRESOLVED / BLOCKING` at specification time; items 3, 5, 9, 20, 21 become
blocking only if provisioning observation contradicts the intended posture (§5, §6).

## 5. SQLite persistence contract (high-scrutiny; BLOCKING conditions)

Execution MUST verify, and record evidence for, every one of the following. **Any violation
is BLOCKING: stop, record, and do not proceed to further verification or to any release
consideration.**

1. the persistent disk is actually mounted at the configured path;
2. `INVENTORAI_DB_PATH` resolves INSIDE that mounted path (exact string recorded);
3. the database file is physically created at that path (not elsewhere);
4. data written before a controlled restart is present after it;
5. data written before a controlled redeploy is present after it (subject to the provider's
   own persistence guarantee, which is itself recorded as observed);
6. exactly ONE application worker process;
7. exactly ONE worker thread;
8. NO horizontal scaling and NO second replica of the service;
9. NO production database path on an ephemeral filesystem;
10. NO second/stray database file created outside the persistent mount (filesystem check).

The application's own production hard-fail (missing `INVENTORAI_DB_PATH` under
`INVENTORAI_ENV=production`) must remain intact and is not to be worked around.

## 6. Backup / restore boundary (P10-BR1 remains the canonical owner)

A persistent disk is **not** backup readiness and must never be recorded as such.
Provisioning-time evidence obtainable: (a) disk persistence across restart/redeploy (§5);
(b) an application-level backup produced on the instance with the governed
`engine/backup_service.py` (consistent copy + `quick_check` validation) and a parity report;
(c) a restore into a scratch path on the instance; (d) an OBSERVED statement of the
provider's snapshot capability (or its absence). NOT obtainable here and still owed:
scheduled backups, off-provider copies, encrypted backup storage, retention values (policy
lane — none invented), and a full production DR drill.

## 7. Monitoring / observability boundary (P10-OB1 remains the canonical owner)

Record only what is natively observed (health-check behaviour, platform metrics/log stream)
and state plainly what remains owed: alert thresholds, alert routing into the P10-IR1
escalation path, an external uptime check, log retention/export. **PSRR items 21–22 remain
OPEN.** No monitoring provider is selected or activated. **OPS-SM1 remains REGISTERED ONLY —
NOT EXECUTED**; no cron job, schedule, or automated alert is created by this gate.

## 8. Auto-deploy decision

**AUTO-DEPLOY: OFF** for this governed provisioning gate. Rationale from repository
governance: every change reaches an environment only through an Owner-authorized, reviewed,
SHA-frozen lifecycle; automatic application of future commits would bypass that control and
would also conflict with the OPS-SM1 principle that no production change occurs without
validation. Deploys are therefore manual/explicit during INFRA-G1-P1. Any future change to
this posture requires its own Owner decision.

## 9. Environment variable / secret matrix

| Variable | Classification | Note |
|---|---|---|
| `INVENTORAI_ENV=production` | REQUIRED BEFORE FIRST BOOT | enables hard-fails + Secure cookie |
| `INVENTORAI_SECRET_KEY` | REQUIRED BEFORE FIRST BOOT — **Owner must generate** | high-entropy; platform secret store only; never in the repository, never in logs, never in this document |
| `INVENTORAI_DB_PATH` | REQUIRED BEFORE FIRST BOOT | must resolve inside the mounted disk (§5) |
| `PORT` | PLATFORM-SUPPLIED | consumed by `gunicorn.conf.py`; not set by the Owner |
| Email provider key + sender identity + public base URL | REQUIRED BEFORE PUBLIC RELEASE | separate gate (§10); NOT required for this gate |
| Monitoring/alerting credentials | NOT REQUIRED FOR THIS GATE | separate decision |
| Payment/MoR credentials | NOT REQUIRED — OUT OF SCOPE | commercial lane |

No secret value is created, recorded, or transported by this contract.

## 10. Email boundary

Production email is NOT selected, configured, or claimed here. Dependency recorded: the
released product's verified-email flows (registration verification, recovery,
verified-email-gated export) cannot function publicly on the in-memory development sink.
**Blocking point: BEFORE FIRST PUBLIC RELEASE — not before provisioning and not before the
§11 verification.** During INFRA-G1-P1 the dev sink remains in place and no email-dependent
behaviour may be presented as production-ready.

## 11. Non-public verification procedure (DEFINED HERE; NOT EXECUTED)

Prerequisite: a separate Owner execution authorization. Every step records evidence
(command/observation + result); any BLOCKING failure stops the sequence.

1. Build succeeds; record the resolved Python version actually used (compare to `3.11`).
2. Gunicorn starts; record the start command actually configured.
3. Service responds on the platform-assigned URL over HTTPS; record the TLS observation.
4. `GET /health` → 200 with the two bounded enum fields.
5. `GET /` → 200.
6. `Content-Security-Policy` present on responses.
7. `Strict-Transport-Security` **absent** — record truthfully (HSTS remains deferred).
8. Record `INVENTORAI_DB_PATH` and prove the file exists inside the mounted disk.
9. Write data through the application; read it back.
10. Controlled restart → data still present (§5.4).
11. Controlled redeploy → data still present (§5.5), and record the observed interruption.
12. Process check: exactly one worker; exactly one worker thread.
13. No Flask development server anywhere in the process tree; no auto-reload.
14. No ProxyFix / forwarded-header trust introduced (configuration + behaviour).
15. Log inspection: no secret, token, password, or raw verification token in output.
16. Filesystem check: no stray database outside the persistent mount.
17. Application-level backup + parity report + scratch-path restore (§6).
18. Record the observed provider snapshot capability (or its absence).
19. Record platform-native monitoring/log visibility and what remains owed.
20. Explicitly record: **NOT publicly released; no DNS; no announcement; no PSRR GO; no
    deployment authorization; no paid activation.**

## 12. Public-access boundary (load-bearing)

Render may assign a service URL automatically at provisioning. **A platform-assigned URL is
NOT public production deployment, NOT first public release, and NOT PSRR GO.** During
INFRA-G1-P1 the service must not be announced, promoted, linked, indexed intentionally,
pointed at production DNS, or described anywhere as released. The public-production block
(PSRR registration §5 / D-PSRR-01) and OD-P's two-part deployment control remain fully in
force; `D-P8-PL-01 class C` continues to hard-block paid activation.

## 13. Carry-forward register (none silently closed)

INFRA-G1-R2 review: **NB-1** superseded-candidate remote-comparison limitation (bounded, not
a blocker); **NB-2** the historical "159 targeted regressions" figure has no reconstructable
set membership and must NOT be relied on as durable proof — the focused, broader targeted,
smoke and full-suite evidence are authoritative; **NB-3** the dependency-audit runner must
detect and report **TOOL MISSING** rather than emit false-clean evidence when `pip_audit` is
unavailable (owed at the next audit-touching gate); **NB-4** the production-config AST helper
intentionally excludes module docstrings — behavioural/code assertions remain the runtime
guard. **R2-REV-NB-START-COMMAND:** the dashboard start command must be verified during
provisioning (§11.2). **Render external facts** not independently verified (snapshot
schedule/retention, minimum disk size, bandwidth, cron billing, workspace fees,
`.python-version` acceptance form, region immutability) — OWED AT PROVISIONING; §4 marks each.
**OD-INFRA-1/2 Owner-Decision-Register rows — STILL OWED** (`OWNER_DECISION_REGISTER.md`
untouched by this gate). Also preserved: PSRR-C1-N1/N2/N3; REV-REC-O1/O2/O3;
INFRA-REV-O1/O2/O3; application-layer OBS-1…OBS-4 and the nine tranche residual risks;
GAP-SYNC-01-NB1/NB2; PC3-N2.

## 14. Review path

LEVEL 2 governance-only candidate (zero runtime/test/schema/guardrail diff) under LEAN
§3/§4; Independent External Review mandatory per §5B.13 including the mandatory independent
Universal Guardrail Smoke; no mechanical full-suite rerun absent a §5B.6 trigger.
