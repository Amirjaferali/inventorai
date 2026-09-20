# Phase 10 — Release-Readiness Checklist (P10-RL1)

**Status:** READINESS TRUTH SURFACE (candidate until merged and post-merge verified).
**Base at authoring:** `b1a0196aaf1f6892996c618c69cb341872ecaf52` (PR #526 merge — P10-DEP1, authoritative).
**Point-in-time refresh (P10-CL0):** stale point-in-time values refreshed at base
`2f77e8e8b633497adee6ea32a6002a7c5860979e` (PR #537 merge — GAP-SYNC-01, authoritative): RL-A1 suite
counts (fresh live run at that base) and new row RL-A10 (product-completion gates merged after this
checklist's authoring base: P10-DBT1/PC1/UG1/PC2/PC3, PRs #530–#535; plus governance GOV-RBR1 PR #536
and GAP-SYNC-01 PR #537). *(The rest of this paragraph is time-scoped to that 2026 P10-CL0 refresh and
is NOT current truth — PSRR and the provider rows have since moved; read the region below.)* No gate
status changed by the refresh: PSRR remains NOT TRIGGERED / NOT
EXECUTED; deployment remains not authorized; paid activation remains hard-blocked; all legal/tax rows
remain DEFERRED — EXTERNAL ADVISER REQUIRED; all provider rows remain NOT SELECTED. The Phase-10
closure-disposition matrix lives at
`docs/governance/P10_CL0_PHASE10_CLOSURE_PRECONDITION_CONSOLIDATION_GATE.md` (dispositions PROPOSED,
Owner-decidable; this checklist remains the per-row truth surface and owns no decision).
**Structural invariants:** enforced by `tests/test_p10_rl1_release_readiness_checklist.py`.

**Current-state synchronization (v1.32, 2026-09-19) — documentation only.** Fourteen rows
carried point-in-time absence claims that later merged and provisioned infrastructure made
false: **RL-B2**, **RL-B3**, **RL-B6**, **RL-C2**, **RL-C3**, **RL-C5**, **RL-F1**, **RL-F2**,
**RL-F3**, **RL-F4**, **RL-F5**, **RL-F6**, **RL-F7** and **RL-G3**. Each now states current
truth only, and its prior wording is preserved verbatim under **Superseded row wording**
below. Nothing was deleted.

**Only the delimited `CURRENT-TRUTH:RELEASE-READINESS` region states current truth.**
Everything outside it — in this file or any other — is history, plan or commentary, whatever
its formatting, and states nothing about today. Do not put a current claim outside the
markers, and do not quote a past claim inside them.

**Machine-readable state contract.** Every guarded provider-dependent row (located by its
immutable `RL-` identifier, never by a mutable label) opens its current-truth cell with two
structured elements, and **those two elements alone are the machine truth of the row**:

1. exactly one `CURRENT STATE:` marker from the bounded vocabulary — `NOT SELECTED` ·
   `SELECTED / NOT PROVISIONED` · `PROVISIONED / NOT COMPLETE` · `IMPLEMENTED / NOT DEPLOYED` ·
   `DEPLOYED / NOT COMPLETE` — with **no completion state in the vocabulary**; and
2. exactly one field block `{SELECTED: …; PROVISIONED: …; IMPLEMENTED: …; DEPLOYED: …;
   LIVE_ACTIVATED: …; COMPLETE: …}`, each value `YES`, `NO` or `N/A` (`N/A` = the field does not
   apply to this row's subject), with `COMPLETE` always `NO`.

**The prose after them is explanatory only.** It may name providers, describe backup objects,
use "live" as an adjective, and carry human context; none of that determines machine state, and
the guard does not read it for state. Deterministic invariants bind the state marker to its
fields (for example `IMPLEMENTED / NOT DEPLOYED` requires `IMPLEMENTED: YES; DEPLOYED: NO;
LIVE_ACTIVATED: NO`), so a marker and its fields cannot silently disagree. The distinctions are
enforced structurally: **selection ≠ provisioning ≠ implementation ≠ deployment ≠
completion**, and **merged ≠ deployed**. If prose is materially wrong, that is a documentation
review matter, not a parser's.

**OD-INFRA-4 — monitoring selection.** `OD-INFRA-4 DECISION: SATISFIED AS A SELECTION
DECISION.` The selected approach is the hosting platform's own metrics and logs plus `/health`
and the P10-OB1 seam; no dedicated third-party monitoring provider was adopted, and that is a
decision rather than a gap. **The decision being settled is not operational monitoring
readiness** — alerting, paging, dashboards beyond the platform's own, and any future dedicated
provider remain OPEN operations work (RL-B6, RL-F4). Nobody is notified when something breaks.

**PSRR current truth, corrected — the following pins are SUPERSEDED v1.32 and quoted here
only as history.** The earlier pins `PSRR TRIGGERED: NO` and "execution has
NOT begun and is NOT authorized" were true before the OD-FR1 trigger and before the
application-layer tranche was authorized and executed. They are **no longer current truth**
and survive only as labelled history in RL-G3. Current: **trigger condition MET (OD-FR1)**;
**execution BEGUN — application-layer tranche only**, 21 of 37 items, independently
accepted; provider-dependent tranche, policy substance and items 35–37 outstanding;
**PSRR NOT COMPLETE**; **PSRR GO ELIGIBLE: NOT ESTABLISHED**; no GO and no NO-GO exists.

**No status changed to a completed one; no gate was opened; no obligation was discharged.**
`DEPLOYMENT AUTHORIZED: NO` and `PAID ACTIVATION AUTHORIZED: NO` are unchanged, every
legal/tax row stays `DEFERRED — EXTERNAL ADVISER REQUIRED`, and the daily off-provider
backup scheduler is **MERGED, NOT DEPLOYED and NOT LIVE-ACTIVATED**. The structural guard
named above enforces all of this against the region and the per-row markers, with its reasons
written into its own docstrings. See `INVENTORAI_MASTER_EXECUTION_ROADMAP.md` §6 Stage 38 for
the operational lane this reconciles against.

```
RELEASE READINESS CHECKLIST FOUNDATION ≠ RELEASE APPROVAL
PSRR GO/NO-GO remains a separate future gate before first public production deployment.
```

This checklist is a deterministic INDEX of current repository truth. It owns no decision: PSRR scope/
trigger/GO belongs to `PSRR_PRODUCTION_SECURITY_RELEASE_READINESS_REGISTRATION.md`; the obligation
inventory belongs to the P10-C contract §4 and the remediation plan; authorization gates belong to the
Owner Decision Register (`OD-P`, `D-PSRR-01`, `D-P8-PL-01`); each foundation belongs to its merged gate
record. Nothing here creates a legal requirement, tax conclusion, provider selection, commercial policy,
security standard, or release authority.

## Status vocabulary (exact semantics)

* `IMPLEMENTED LOCAL FOUNDATION` — a bounded local foundation exists and is authoritative; it does NOT
  imply production readiness.
* `OPEN` — known obligation, currently unresolved.
* `DEFERRED — EXTERNAL ADVISER REQUIRED` — cannot be truthfully concluded without qualified external
  legal/tax input (registers OPEN; no adviser engaged).
* `PROVIDER-DEPENDENT` — requires selecting and/or configuring a production provider. The label says
  what the row *depends on*; it says nothing about how far that dependency has been met. Each such row
  carries its own `CURRENT STATE:` marker and `{…}` field block inside the region below, and those are
  the only place its position is recorded. Selection is never provisioning, provisioning is never implementation,
  implementation is never deployment, and none of them is completion. *(The earlier sentence "Nothing
  is provisioned or configured anywhere" was true when this vocabulary was written and is not true
  now — see the per-row markers.)*
* `COMMERCIAL DECISION REQUIRED` — needs an explicit Owner commercial-policy decision.
* `PSRR-TIME` — must be reassessed/executed at the formal PSRR gate.
* `DEPLOYMENT-TIME` — cannot be completed before a real deployment configuration/environment exists.
* `BLOCKED` — downstream action cannot proceed while a prerequisite remains unresolved.

<!-- CURRENT-TRUTH:RELEASE-READINESS:BEGIN -->

## A. Technical / application

| ID | Item | Status | Source (section) | Current truth / boundary | Blocks |
|---|---|---|---|---|---|
| RL-A1 | Full application test suite | IMPLEMENTED LOCAL FOUNDATION | `tests/` (full suite) | 2969 passed / 3 skipped / 1 xfailed / 0 failures at the INFRA-G1-R2 implementation candidate over base `306f3499…` (fresh live run; the +18 are the production-serving contract tests; earlier point-in-time values 2951/3/1/0 and 2854/3/1/0 superseded) | — |
| RL-A2 | Authentication/session foundations | IMPLEMENTED LOCAL FOUNDATION | `web/app.py`; `engine/account_store.py`; `engine/auth_session.py` | register/login/verify/recover/reset/logout-all; scrypt; epoch revocation; HttpOnly/SameSite/production-gated Secure | production auth posture: PSRR-TIME |
| RL-A3 | Authorization/ownership isolation | IMPLEMENTED LOCAL FOUNDATION | P5-3; P7-I2; `web/api_v1.py` | owner-only project access; non-enumerating denials | formal review: PSRR-TIME (items 4–5) |
| RL-A4 | CSRF protection | IMPLEMENTED LOCAL FOUNDATION | `web/app.py` `_csrf_valid` | token check on state-changing routes | — |
| RL-A5 | Security headers | IMPLEMENTED LOCAL FOUNDATION | P10-SEC1; `web/app.py` `_SECURITY_HEADERS` | CSP/nosniff/X-Frame-Options/Referrer-Policy on every response | HSTS: see RL-C4 |
| RL-A6 | Bounded input hardening | IMPLEMENTED LOCAL FOUNDATION | P10-SEC2 + P10-SEC3; `web/app.py` `MAX_FREE_TEXT_CHARS`, `MAX_CONTENT_LENGTH`, `_dw_free_text_reject` | 128 KiB transport bound + 20,000-char cap + NUL rejection on the two primary free-text surfaces AND (P10-SEC3) all seven Decision Workspace POST free-text surfaces; residual gaps remain: legacy ILT-002 start routes and the criticality rationale are transport-bounded ONLY; NOT "all inputs fully hardened" | production abuse/input review: PSRR-TIME (item 1) |
| RL-A7 | Dependency-audit foundation | IMPLEMENTED LOCAL FOUNDATION | P10-DEP1; `scripts/run_dependency_audit.py`; evidence `docs/governance/evidence/phase10_p10_dep1/` | POINT-IN-TIME ONLY: pip-audit 2.10.1, 11 packages from `requirements.txt`, 0 findings at 2026-08-19T21:24:47Z — advisory data changes; NO continuous scanning; NO auto-remediation; NOTE: `tests/requirements-draft-l2.txt` is a separate TEST-ONLY declaration (playwright pins) NOT covered by that audit run | formal review: PSRR-TIME (items 12–13) |
| RL-A8 | Project/export/deactivation behavior | IMPLEMENTED LOCAL FOUNDATION | P10-D3a/P10-D3b (merged PRs #511/#513) | project-scoped export; deactivation = status tombstone, NOT physical erasure | account-wide export / erasure: RL-D4/RL-D5 |
| RL-A9 | Persistence/integrity safeguards | IMPLEMENTED LOCAL FOUNDATION | `engine/account_store.py`; `engine/record_store.py` | durable SQLite, BEGIN IMMEDIATE transactions, fail-closed stores | production datastore topology: DEPLOYMENT-TIME |
| RL-A10 | Product completion (restart story) + universal guardrails + Phase-9 debts | IMPLEMENTED LOCAL FOUNDATION | P10-DBT1/P10-PC1/P10-UG1/P10-PC2/P10-PC3 (PRs #530–#535); `scripts/run_universal_smoke.py`; `tests/universal_guardrail_manifest.py` | read-only reconstructed review state, truthful cold-load deliverable, governed explicit writable resume; universal guardrail smoke (blocking guards + attribution); Phase-9 registered debts remediated; capability truth only — does NOT imply production readiness | — |

## B. Operational

| ID | Item | Status | Source | Current truth / boundary | Blocks |
|---|---|---|---|---|---|
| RL-B1 | Local backup/restore + drill | IMPLEMENTED LOCAL FOUNDATION | P10-BR1; `engine/backup_service.py`; drill evidence | local capability, drill-verified; local ≠ production backup readiness | — |
| RL-B2 | Production backup scheduling | PROVIDER-DEPENDENT | OD-J2 §3.2 (delegated infrastructure gate); OD-INFRA-5; `engine/offsite_backup_scheduler.py` (PR #664) | CURRENT STATE: IMPLEMENTED / NOT DEPLOYED. {SELECTED: YES; PROVISIONED: N/A; IMPLEMENTED: YES; DEPLOYED: NO; LIVE_ACTIVATED: NO; COMPLETE: NO} ONE bounded in-process daily off-provider scheduler is **MERGED** under OD-INFRA-5 — and is **NOT DEPLOYED and NOT LIVE-ACTIVATED**; no scheduled run has occurred. Merged is not deployed; implemented is not activated; NOT COMPLETE | first production deployment |
| RL-B3 | Offsite backup | PROVIDER-DEPENDENT | OD-J2 §3.2; OD-INFRA-5; `engine/r2_object_upload.py`; `scripts/inventorai_offsite_backup.py` | CURRENT STATE: PROVISIONED / NOT COMPLETE. {SELECTED: YES; PROVISIONED: YES; IMPLEMENTED: YES; DEPLOYED: N/A; LIVE_ACTIVATED: N/A; COMPLETE: NO} An off-provider destination is PROVISIONED under OD-INFRA-5 (private bucket, create-only writes, scoped token) and **one live off-provider backup object exists**; a full-loss disaster-recovery drill passed end to end and the temporary DR service was decommissioned. **Backup recency is not established by this row** — read it from the stored object's own metadata, never from scheduler state. Recurrence belongs to RL-B2 and retention to RL-B4: NOT COMPLETE | first production deployment |
| RL-B4 | Backup retention | DEFERRED — EXTERNAL ADVISER REQUIRED + PROVIDER-DEPENDENT | P10-DOC1 `docs/DATA_RETENTION_POLICY.md`; OD-DR1 | CURRENT STATE: NOT SELECTED. {SELECTED: NO; PROVISIONED: N/A; IMPLEMENTED: N/A; DEPLOYED: N/A; LIVE_ACTIVATED: N/A; COMPLETE: NO} No retention rule exists or is decided | production backup design |
| RL-B5 | Observability foundation | IMPLEMENTED LOCAL FOUNDATION | P10-OB1; `/health`; `web/observability.py` | local health surface + data-minimized JSON logging seam | — |
| RL-B6 | Production monitoring/alerting/dashboards | PROVIDER-DEPENDENT | P10-OB1 boundaries; `docs/OBSERVABILITY_ARCHITECTURE.md`; OD-INFRA-1; OD-INFRA-4 | CURRENT STATE: PROVISIONED / NOT COMPLETE. {SELECTED: YES; PROVISIONED: YES; IMPLEMENTED: N/A; DEPLOYED: N/A; LIVE_ACTIVATED: N/A; COMPLETE: NO} The hosting platform's own metrics and log surface exists under OD-INFRA-1, alongside `/health` and the P10-OB1 bounded logging seam — so a monitoring stack does exist and is PROVISIONED under OD-INFRA-1. `OD-INFRA-4 DECISION: SATISFIED AS A SELECTION DECISION` — that platform stack **is** the selected approach and no dedicated third-party monitoring provider was adopted. **A settled selection is not operational monitoring readiness.** Still OPEN as operations work: alerting, paging and notification behaviour, dashboards beyond the platform's own, and any future dedicated provider if one is separately chosen. Nobody is notified when something breaks. P10-C §4 row = PARTIAL: NOT COMPLETE | PSRR items 21–22 |
| RL-B7 | Internal technical incident response | IMPLEMENTED LOCAL FOUNDATION | P10-IR1 runbook | internal foundation; informs PSRR item 27, does not satisfy it | — |
| RL-B8 | Customer-facing support model | OPEN + COMMERCIAL DECISION REQUIRED | P10-IR1 §17; P10-C §4 | no support channel/commitments; wording legally sensitive (LQ-03) | paid activation |
| RL-B9 | Escalation/runbooks (technical) | IMPLEMENTED LOCAL FOUNDATION | P10-IR1; `docs/DISASTER_RECOVERY_PLAN.md` Scenario 7 | IR coordinates, DR recovers | production on-call: PROVIDER-DEPENDENT |

## C. Security / infrastructure

| ID | Item | Status | Source | Current truth / boundary | Blocks |
|---|---|---|---|---|---|
| RL-C1 | Production secrets/configuration operations | PSRR-TIME + DEPLOYMENT-TIME | PSRR §7 item 8; `web/app.py` env-based fail-closed secret | local foundation exists; rotation/ops process does not | deployment |
| RL-C2 | TLS | PROVIDER-DEPENDENT + DEPLOYMENT-TIME | P10-SEC1 record; `docs/SECURITY_ARCHITECTURE.md`; OD-INFRA-1 | CURRENT STATE: PROVISIONED / NOT COMPLETE. {SELECTED: YES; PROVISIONED: YES; IMPLEMENTED: N/A; DEPLOYED: N/A; LIVE_ACTIVATED: N/A; COMPLETE: NO} TLS terminates at the hosting platform edge, PROVISIONED under OD-INFRA-1 — **that is the approach in force, not an absence**. What is missing is the recorded instrument, not the capability: no separate OD-INFRA-3 decision artifact exists for the TLS/proxy approach, application-side forwarded-header trust stays deliberately off (RL-C3), HSTS stays deferred (RL-C4), and the production TLS posture is unreviewed: NOT COMPLETE | HSTS (RL-C4); deployment |
| RL-C3 | Reverse proxy / trusted-forwarding | PROVIDER-DEPENDENT | P10-SEC1 §12 boundary; OD-INFRA-1 | CURRENT STATE: PROVISIONED / NOT COMPLETE. {SELECTED: YES; PROVISIONED: YES; IMPLEMENTED: N/A; DEPLOYED: N/A; LIVE_ACTIVATED: N/A; COMPLETE: NO} A platform-edge reverse proxy exists and is PROVISIONED under OD-INFRA-1. **Application-side trusted-forwarding remains deliberately off** — `web/app.py` trusts no forwarded literals — which is a decision, not a gap: NOT COMPLETE | HSTS |
| RL-C4 | HSTS reassessment | DEPLOYMENT-TIME | `docs/SECURITY_ARCHITECTURE.md` "HSTS — DEFERRED" | intentionally deferred pending trusted HTTPS/proxy context | — |
| RL-C5 | Provider-specific security configuration | PROVIDER-DEPENDENT | PSRR §7 items 29–32; OD-INFRA-1 | CURRENT STATE: PROVISIONED / NOT COMPLETE. {SELECTED: YES; PROVISIONED: YES; IMPLEMENTED: N/A; DEPLOYED: N/A; LIVE_ACTIVATED: N/A; COMPLETE: NO} Providers now exist: hosting (OD-INFRA-1) and object storage (OD-INFRA-5) are PROVISIONED, and an email adapter is merged under OD-INFRA-6. **Their provider-specific security configuration has never been reviewed**, and PSRR §7 items 29–32 are unreached: NOT COMPLETE | PSRR |
| RL-C6 | Dependency/vulnerability review freshness | PSRR-TIME | PSRR §7 items 12–13; P10-DEP1 evidence | re-run the local audit at PSRR; point-in-time results expire | PSRR GO |
| RL-C7 | Production authorization/security review | PSRR-TIME | PSRR §7 items 1–5, 33–36 | not executed | PSRR GO |
| RL-C8 | Abuse/rate-limit review | PSRR-TIME | PSRR §8 ("broad abuse controls NOT CLAIMED DELIVERED") | auth-surface floor only | PSRR items 23–25 |
| RL-C9 | Audit/logging review (`access_audit` lifecycle) | PSRR-TIME | PSRR §8 open observation | no retention/cleanup for access_audit | PSRR items 20, 26, 28 |
| RL-C10 | Deployment/release controls (technical) | DEPLOYMENT-TIME + PSRR-TIME | P10-C §4; PSRR §7 items 31–37 | governance layer exists (hard blocks); no CI/deploy/rollback tech exists | deployment |

## D. Legal / privacy / data rights — ALL DEFERRED — EXTERNAL ADVISER REQUIRED (registers OPEN; no adviser engaged)

| ID | Item | Status | Source | Current truth |
|---|---|---|---|---|
| RL-D1 | Privacy Policy, Terms, consent/legal notices | DEFERRED — EXTERNAL ADVISER REQUIRED | P10-LT1 §9; `web/ui_text.py` `UI_SENS_DATA_07` | none exists; absence disclosed on the live trust page; draftable only after accepted external input |
| RL-D2 | Jurisdiction-specific privacy obligations | DEFERRED — EXTERNAL ADVISER REQUIRED | P10-LT1 LQ-04…LQ-07 | open questions; no regime claimed applicable |
| RL-D3 | GDPR / national PDPL applicability | DEFERRED — EXTERNAL ADVISER REQUIRED | P10-LT1 LQ-05/LQ-06 | open questions only |
| RL-D4 | Data-subject rights scope (access/export) | DEFERRED — EXTERNAL ADVISER REQUIRED | OD-DR2; P10-LT1 LQ-08/LQ-11/LQ-12 | project-scoped export implemented; account-wide DEFERRED; escalation rule in force |
| RL-D5 | Physical deletion/erasure policy | DEFERRED — EXTERNAL ADVISER REQUIRED | OD-DR1; P10-D3b | deactivation tombstone only ("deleted" status ≠ physical deletion); erasure deferred + separate Owner authorization |
| RL-D6 | Retention policy substance | DEFERRED — EXTERNAL ADVISER REQUIRED | P10-DOC1 `docs/DATA_RETENTION_POLICY.md` banner | documentation truthful; no duration decided anywhere |
| RL-D7 | Legal request handling | IMPLEMENTED LOCAL FOUNDATION (escalation rules) + DEFERRED for substance | OD-DR1 §6 / OD-DR2 §6; P10-IR1 §10 | escalation-to-Owner+counsel rules recorded; no legal determination capability |

## E. Commercial / tax / payments

| ID | Item | Status | Source | Current truth |
|---|---|---|---|---|
| RL-E1 | Legal/commercial entity readiness | DEFERRED — EXTERNAL ADVISER REQUIRED | OD-CJ1 §1; P10-LT1 LQ-01/LQ-02 | Kuwait = intent fact only; no entity exists/decided |
| RL-E2 | Tax / VAT / GST / registrations | DEFERRED — EXTERNAL ADVISER REQUIRED | P10-LT1 TQ-01…TQ-05, TQ-11 | open questions; no conclusion |
| RL-E3 | Invoicing / receipts | DEFERRED — EXTERNAL ADVISER REQUIRED + COMMERCIAL DECISION REQUIRED | TQ-06/TQ-09/TQ-10 | nothing decided or built |
| RL-E4 | Payment provider | PROVIDER-DEPENDENT | OD-CJ1 §8–§9; P8-I4 `PaymentProviderPort` | CURRENT STATE: NOT SELECTED. {SELECTED: NO; PROVISIONED: NO; IMPLEMENTED: N/A; DEPLOYED: N/A; LIVE_ACTIVATED: N/A; COMPLETE: NO} No payment provider; the provider-neutral boundary exists |
| RL-E5 | Merchant of Record | PROVIDER-DEPENDENT + DEFERRED — EXTERNAL ADVISER REQUIRED | OD-CJ1 §9; TQ-12/TQ-13 | CURRENT STATE: NOT SELECTED. {SELECTED: NO; PROVISIONED: N/A; IMPLEMENTED: N/A; DEPLOYED: N/A; LIVE_ACTIVATED: N/A; COMPLETE: NO} No Merchant of Record; fact needs registered |
| RL-E6 | Pricing / billing frequency / trial / renewal / cancellation / refunds / dunning | COMMERCIAL DECISION REQUIRED | P10-LT1 §10 (counsel-needed assumptions = OWNER INPUT REQUIRED) | none decided (only USD base currency + recurring direction are accepted strategy) |
| RL-E7 | Final payment methods | COMMERCIAL DECISION REQUIRED + PROVIDER-DEPENDENT | OD-CJ1 §8A | CURRENT STATE: NOT SELECTED. {SELECTED: NO; PROVISIONED: N/A; IMPLEMENTED: N/A; DEPLOYED: N/A; LIVE_ACTIVATED: N/A; COMPLETE: NO} Compatibility direction only (Visa/MC/Apple Pay/KNET-where-applicable); per-method recurring capability at the provider gate |
| RL-E8 | Public paid activation | BLOCKED | `D-P8-PL-01 class C` (ODR) | hard-blocked until legal/readiness + PSRR GO + deployment gate + Owner authorization |

## F. Provider / production

| ID | Item | Status | Source | Current truth |
|---|---|---|---|---|
| RL-F1 | Hosting provider | PROVIDER-DEPENDENT | OD-J2 §3.2; INFRA-G1-R1 (OD-INFRA-1); INFRA-G1-P1 | CURRENT STATE: PROVISIONED / NOT COMPLETE. {SELECTED: YES; PROVISIONED: YES; IMPLEMENTED: N/A; DEPLOYED: YES; LIVE_ACTIVATED: NO; COMPLETE: NO} Owner-SELECTED: Render (OD-INFRA-1, INFRA-G1-R1), and now PROVISIONED and CONFIGURED as ONE non-public web service — Docker runtime, one instance, one worker, one thread, one persistent disk at `/var/data` carrying the canonical SQLite, platform-environment secrets, `/health`. Provisioning is not completion and not release: NOT COMPLETE |
| RL-F2 | Deployment region | PROVIDER-DEPENDENT | OD-J2 §3.2; INFRA-G1-R1 (OD-INFRA-2) | CURRENT STATE: PROVISIONED / NOT COMPLETE. {SELECTED: YES; PROVISIONED: YES; IMPLEMENTED: N/A; DEPLOYED: YES; LIVE_ACTIVATED: NO; COMPLETE: NO} Owner-SELECTED: Frankfurt (OD-INFRA-2, INFRA-G1-R1), and the service is PROVISIONED in that region. **No legal, tax or data-residency conclusion is implied or available** — RL-D2/RL-D3/RL-E2 remain adviser-dependent: NOT COMPLETE |
| RL-F3 | Reverse-proxy/TLS provider | PROVIDER-DEPENDENT | P10-SEC1 boundaries; OD-INFRA-1 | CURRENT STATE: PROVISIONED / NOT COMPLETE. {SELECTED: YES; PROVISIONED: YES; IMPLEMENTED: N/A; DEPLOYED: N/A; LIVE_ACTIVATED: N/A; COMPLETE: NO} Reverse proxy and TLS come from the hosting platform edge, PROVISIONED and decided in fact by the OD-INFRA-1 selection — so this is **not an open provider choice and not an absent capability**. No separate third-party proxy/TLS provider is selected and none is required at this posture. **The gap is documentary: no OD-INFRA-3 decision artifact records the approach**: NOT COMPLETE |
| RL-F4 | Monitoring provider | PROVIDER-DEPENDENT | P10-OB1 boundaries; OD-INFRA-1; OD-INFRA-4 | CURRENT STATE: PROVISIONED / NOT COMPLETE. {SELECTED: YES; PROVISIONED: YES; IMPLEMENTED: N/A; DEPLOYED: N/A; LIVE_ACTIVATED: N/A; COMPLETE: NO} `OD-INFRA-4 DECISION: SATISFIED AS A SELECTION DECISION` — the selected approach is the hosting platform's own metrics and log surface, PROVISIONED under OD-INFRA-1, plus `/health` and the P10-OB1 seam, and **no dedicated third-party monitoring provider was adopted. That is the decision, not an open choice.** What remains is separate operations work, not a selection: **no alerting, no paging, no dashboards beyond the platform's own** (RL-B6), and any future dedicated provider would need its own decision: NOT COMPLETE |
| RL-F5 | Backup provider | PROVIDER-DEPENDENT | P10-BR1 boundaries; OD-INFRA-5 | CURRENT STATE: PROVISIONED / NOT COMPLETE. {SELECTED: YES; PROVISIONED: YES; IMPLEMENTED: N/A; DEPLOYED: N/A; LIVE_ACTIVATED: N/A; COMPLETE: NO} Owner-SELECTED: Cloudflare R2 as the off-provider backup destination (OD-INFRA-5), PROVISIONED as a private bucket with create-only writes and a scoped token. Retention (RL-B4) and recurrence (RL-B2) stay unresolved: NOT COMPLETE |
| RL-F6 | Email provider | PROVIDER-DEPENDENT | `engine/email_sender.py` (`ResendEmailSender`, OD-INFRA-6); PR #663 | CURRENT STATE: SELECTED / NOT PROVISIONED. {SELECTED: YES; PROVISIONED: NO; IMPLEMENTED: YES; DEPLOYED: NO; LIVE_ACTIVATED: NO; COMPLETE: NO} Owner-SELECTED: Resend for transactional account email (OD-INFRA-6), with the adapter, a durable SQLite outbox, one bounded dispatcher and a trusted public base URL merged. The sending identity is **NOT PROVISIONED** and live sending is NOT ACTIVATED: **production email identity and Resend activation are DEFERRED TO FINAL PRE-RELEASE — NOT CANCELLED**; the email retry-budget P1 must be revisited before live activation; artifact delivery is a separate capability: NOT COMPLETE |
| RL-F7 | Production environment | DEPLOYMENT-TIME | OD-P; `web/app.py` `_run_config` (bounded single-threaded MVP serving); INFRA-G1-P1 | A non-public production-shaped environment exists and persists across restart and redeploy; it sits behind Maintenance Mode and has never served the public. First public production deployment stays BLOCKED on RL-G5 + RL-G6 |

## G. Gates (sequence truth)

| ID | Gate | Status | Source | Current truth |
|---|---|---|---|---|
| RL-G1 | Phase 10 closure | FORMAL CLOSURE RECORD CREATED (authoritative on merge) | `docs/governance/PHASE_10_FORMAL_CLOSURE_RECORD.md`; P10-CL0 (PR #538, `OD-P10-CL0-STRUCTURE` Option 2) | PHASE 10 FORMALLY CLOSED under Option 2 when the closure record is merged and post-merge verified; closure binds every open obligation to its hard-blocking lane and converts NOTHING to complete; PHASE-10 CLOSURE ≠ RELEASE APPROVAL |
| RL-G2 | PSRR REGISTERED | IMPLEMENTED LOCAL FOUNDATION (registration only) | `PSRR_..._REGISTRATION.md` | registered; 37-item minimum scope |
| RL-G3 | PSRR TRIGGERED | TRIGGER CONDITION MET (OD-FR1) — EXECUTION BEGUN, PSRR NOT COMPLETE | PSRR registration §4; OD-FR1 (durably recorded in `docs/governance/PSRR_C1_PSRR_EXECUTION_CONTRACT.md` §2); PSRR-C1 §5.1 | Trigger = intent to reach FIRST PUBLIC PRODUCTION DEPLOYMENT; OD-FR1 (Owner intent = YES) established that fact, so the **trigger condition is MET**. **PSRR execution has since BEGUN**: the application-layer tranche was separately authorized, executed and independently accepted (RL-G4). Still outstanding: the provider-dependent tranche, policy substance and items 35–37. This checklist does not trigger it |
| RL-G4 | PSRR EXECUTED | PARTIALLY EXECUTED — APPLICATION-LAYER TRANCHE ONLY | `docs/governance/PSRR_APPLICATION_LAYER_TRANCHE_EXECUTION_RECORD.md`; PSRR-C1 §5.1 | application-layer tranche EXECUTED and independently accepted (21 distinct item numbers, app halves only for split items); provider-dependent tranche, policy substance, and items 35–37 remain; PSRR NOT COMPLETE; NO GO exists |
| RL-G5 | PSRR GO/NO-GO | OPEN (NO GO EXISTS) | same §5–§6 | public production BLOCKED until PSRR = GO |
| RL-G6 | Deployment authorization | BLOCKED | OD-P (ODR) | separate deployment gate + explicit Owner authorization, both required |
| RL-G7 | First public production deployment | BLOCKED | D-PSRR-01; OD-P | requires RL-G5 + RL-G6 |
| RL-G8 | Paid activation | BLOCKED | `D-P8-PL-01 class C` | see RL-E8 |

Sequence: Phase-10 obligations → (Owner intent to deploy publicly) → PSRR trigger → PSRR execution →
PSRR GO + OD-P deployment gate + Owner authorization → first public production deployment → (all
commercial/legal prerequisites) → paid activation. This checklist sits BEFORE all of those gates and
approves none of them.


<!-- CURRENT-TRUTH:RELEASE-READINESS:END -->

## Superseded row wording — history, not current truth

The rows above once read as quoted here. Each quotation is preserved so the change is
visible rather than silent. **None of it states anything about today** — current truth is
only what sits inside the `CURRENT-TRUTH:RELEASE-READINESS` region above.

* **RL-B2** — **SUPERSEDED v1.32** (was: "does not exist").
* **RL-B3** — **SUPERSEDED v1.32** (was: "does not exist; never claimed").
* **RL-B6** — **SUPERSEDED v1.32** (was: "none exists").
* **RL-C2** — **SUPERSEDED v1.32** (was: "no TLS termination exists anywhere").
* **RL-C3** — **SUPERSEDED v1.32** (was: "no proxy trust configured (deliberate)" — read at the time as "no proxy exists").
* **RL-C5** — **SUPERSEDED v1.32** (was: "no provider exists").
* **RL-F1** — **SUPERSEDED v1.32** (was: "NOT PROVISIONED, NOT CONFIGURED, no account/resource exists").
* **RL-F2** — **SUPERSEDED v1.32** (was: "NOT PROVISIONED").
* **RL-F3** — **SUPERSEDED v1.32** (was: "NOT SELECTED (OD-INFRA-3 OPEN)").
* **RL-F4** — **SUPERSEDED v1.32** (was: "NOT SELECTED (OD-INFRA-4 OPEN)").
* **RL-F5** — **SUPERSEDED v1.32** (was: "NOT SELECTED").
* **RL-F6** — **SUPERSEDED v1.32** (was: "NOT SELECTED (dev-sink only)").
* **RL-F7** — **SUPERSEDED v1.32** (was: "none exists").
* **RL-G3** — **SUPERSEDED v1.32** (was: "EXECUTION NOT AUTHORIZED / NOT STARTED", and the pin "PSRR TRIGGERED: NO" — both were truth before the trigger and before the tranche, and are preserved here as history, not as current state).

## Blocking summary

`BLOCKING RELEASE / PAID ACTIVATION`: every DEFERRED — EXTERNAL ADVISER REQUIRED item (RL-D1…D7,
RL-E1…E3, RL-E5); every COMMERCIAL DECISION REQUIRED item (RL-B8, RL-E3, RL-E6, RL-E7); every
PROVIDER-DEPENDENT item needed for production (RL-B2/B3, RL-C2/C3/C5, RL-E4/E5, RL-F1…F7); all
PSRR-TIME items (RL-C1, C6…C10); the gate chain RL-G3…G8.

```
PHASE 10: FORMALLY CLOSED UNDER OD-P10-CL0-STRUCTURE OPTION 2 (on merge of the closure record).
PHASE-10 CLOSURE ≠ RELEASE APPROVAL — every deferred obligation stays in its hard-blocking lane.
(The earlier "PHASE 10 CLOSURE ELIGIBLE NOW: NO" line was superseded by the Owner-accepted P10-CL0
eligibility determination and Option-2 structure decision, PR #538.)
PAID ACTIVATION AUTHORIZED: NO        DEPLOYMENT AUTHORIZED: NO
PSRR TRIGGER CONDITION: MET (OD-FR1)
PSRR EXECUTION: BEGUN — APPLICATION-LAYER TRANCHE ONLY (21 of 37 items, independently accepted)
PSRR REMAINING: provider-dependent tranche + policy substance + items 35–37
PSRR NOT COMPLETE                     PSRR GO ELIGIBLE: NOT ESTABLISHED
PSRR = GO: NOT ESTABLISHED — no GO and no NO-GO exists
(SUPERSEDED v1.32: the earlier pins "PSRR TRIGGERED: NO" and "PSRR gate execution has NOT begun and
is NOT authorized" were truth before the OD-FR1 trigger and before the tranche was authorized and
executed. They are preserved as history in RL-G3 and are NOT current truth. Nothing here advances the
gate: this checklist does not trigger it, and public production stays BLOCKED until PSRR = GO.)
```
