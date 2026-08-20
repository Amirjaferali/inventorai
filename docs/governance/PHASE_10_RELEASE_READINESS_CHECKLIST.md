# Phase 10 — Release-Readiness Checklist (P10-RL1)

**Status:** READINESS TRUTH SURFACE (candidate until merged and post-merge verified).
**Base at authoring:** `b1a0196aaf1f6892996c618c69cb341872ecaf52` (PR #526 merge — P10-DEP1, authoritative).
**Point-in-time refresh (P10-CL0):** stale point-in-time values refreshed at base
`2f77e8e8b633497adee6ea32a6002a7c5860979e` (PR #537 merge — GAP-SYNC-01, authoritative): RL-A1 suite
counts (fresh live run at that base) and new row RL-A10 (product-completion gates merged after this
checklist's authoring base: P10-DBT1/PC1/UG1/PC2/PC3, PRs #530–#535; plus governance GOV-RBR1 PR #536
and GAP-SYNC-01 PR #537). No gate status changed by the refresh: PSRR remains NOT TRIGGERED / NOT
EXECUTED; deployment remains not authorized; paid activation remains hard-blocked; all legal/tax rows
remain DEFERRED — EXTERNAL ADVISER REQUIRED; all provider rows remain NOT SELECTED. The Phase-10
closure-disposition matrix lives at
`docs/governance/P10_CL0_PHASE10_CLOSURE_PRECONDITION_CONSOLIDATION_GATE.md` (dispositions PROPOSED,
Owner-decidable; this checklist remains the per-row truth surface and owns no decision).
**Structural invariants:** enforced by `tests/test_p10_rl1_release_readiness_checklist.py`.

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
* `PROVIDER-DEPENDENT` — requires selecting/configuring a production provider (none is selected).
* `COMMERCIAL DECISION REQUIRED` — needs an explicit Owner commercial-policy decision.
* `PSRR-TIME` — must be reassessed/executed at the formal PSRR gate.
* `DEPLOYMENT-TIME` — cannot be completed before a real deployment configuration/environment exists.
* `BLOCKED` — downstream action cannot proceed while a prerequisite remains unresolved.

## A. Technical / application

| ID | Item | Status | Source (section) | Current truth / boundary | Blocks |
|---|---|---|---|---|---|
| RL-A1 | Full application test suite | IMPLEMENTED LOCAL FOUNDATION | `tests/` (full suite) | 2951 passed / 3 skipped / 1 xfailed / 0 failures at the P10-CL0 refresh base `2f77e8e8…` (fresh live run; earlier authoring-base value 2854/3/1/0 superseded as point-in-time) | — |
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
| RL-B2 | Production backup scheduling | PROVIDER-DEPENDENT | OD-J2 §3.2 (delegated infrastructure gate) | does not exist | first production deployment |
| RL-B3 | Offsite backup | PROVIDER-DEPENDENT | OD-J2 §3.2 | does not exist; never claimed | first production deployment |
| RL-B4 | Backup retention | DEFERRED — EXTERNAL ADVISER REQUIRED + PROVIDER-DEPENDENT | P10-DOC1 `docs/DATA_RETENTION_POLICY.md`; OD-DR1 | no retention rule exists or is decided | production backup design |
| RL-B5 | Observability foundation | IMPLEMENTED LOCAL FOUNDATION | P10-OB1; `/health`; `web/observability.py` | local health surface + data-minimized JSON logging seam | — |
| RL-B6 | Production monitoring/alerting/dashboards | PROVIDER-DEPENDENT | P10-OB1 boundaries; `docs/OBSERVABILITY_ARCHITECTURE.md` | none exists; P10-C §4 row = PARTIAL — foundation only | PSRR items 21–22 |
| RL-B7 | Internal technical incident response | IMPLEMENTED LOCAL FOUNDATION | P10-IR1 runbook | internal foundation; informs PSRR item 27, does not satisfy it | — |
| RL-B8 | Customer-facing support model | OPEN + COMMERCIAL DECISION REQUIRED | P10-IR1 §17; P10-C §4 | no support channel/commitments; wording legally sensitive (LQ-03) | paid activation |
| RL-B9 | Escalation/runbooks (technical) | IMPLEMENTED LOCAL FOUNDATION | P10-IR1; `docs/DISASTER_RECOVERY_PLAN.md` Scenario 7 | IR coordinates, DR recovers | production on-call: PROVIDER-DEPENDENT |

## C. Security / infrastructure

| ID | Item | Status | Source | Current truth / boundary | Blocks |
|---|---|---|---|---|---|
| RL-C1 | Production secrets/configuration operations | PSRR-TIME + DEPLOYMENT-TIME | PSRR §7 item 8; `web/app.py` env-based fail-closed secret | local foundation exists; rotation/ops process does not | deployment |
| RL-C2 | TLS | PROVIDER-DEPENDENT + DEPLOYMENT-TIME | P10-SEC1 record; `docs/SECURITY_ARCHITECTURE.md` | no TLS termination exists anywhere | HSTS (RL-C4); deployment |
| RL-C3 | Reverse proxy / trusted-forwarding | PROVIDER-DEPENDENT | P10-SEC1 §12 boundary | no proxy trust configured (deliberate) | HSTS |
| RL-C4 | HSTS reassessment | DEPLOYMENT-TIME | `docs/SECURITY_ARCHITECTURE.md` "HSTS — DEFERRED" | intentionally deferred pending trusted HTTPS/proxy context | — |
| RL-C5 | Provider-specific security configuration | PROVIDER-DEPENDENT | PSRR §7 items 29–32 | no provider exists | PSRR |
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
| RL-E4 | Payment provider | PROVIDER-DEPENDENT | OD-CJ1 §8–§9; P8-I4 `PaymentProviderPort` | NOT SELECTED; provider-neutral boundary exists |
| RL-E5 | Merchant of Record | PROVIDER-DEPENDENT + DEFERRED — EXTERNAL ADVISER REQUIRED | OD-CJ1 §9; TQ-12/TQ-13 | NOT SELECTED; fact needs registered |
| RL-E6 | Pricing / billing frequency / trial / renewal / cancellation / refunds / dunning | COMMERCIAL DECISION REQUIRED | P10-LT1 §10 (counsel-needed assumptions = OWNER INPUT REQUIRED) | none decided (only USD base currency + recurring direction are accepted strategy) |
| RL-E7 | Final payment methods | COMMERCIAL DECISION REQUIRED + PROVIDER-DEPENDENT | OD-CJ1 §8A | compatibility direction only (Visa/MC/Apple Pay/KNET-where-applicable); per-method recurring capability at the provider gate |
| RL-E8 | Public paid activation | BLOCKED | `D-P8-PL-01 class C` (ODR) | hard-blocked until legal/readiness + PSRR GO + deployment gate + Owner authorization |

## F. Provider / production

| ID | Item | Status | Source | Current truth |
|---|---|---|---|---|
| RL-F1 | Hosting provider | PROVIDER-DEPENDENT | OD-J2 §3.2 | NOT SELECTED (delegated gate) |
| RL-F2 | Deployment region | PROVIDER-DEPENDENT | OD-J2 §3.2 | NOT SELECTED |
| RL-F3 | Reverse-proxy/TLS provider | PROVIDER-DEPENDENT | P10-SEC1 boundaries | NOT SELECTED |
| RL-F4 | Monitoring provider | PROVIDER-DEPENDENT | P10-OB1 boundaries | NOT SELECTED |
| RL-F5 | Backup provider | PROVIDER-DEPENDENT | P10-BR1 boundaries | NOT SELECTED |
| RL-F6 | Email provider | PROVIDER-DEPENDENT | `engine/email_sender.py` (dev sink) | NOT SELECTED (dev-sink only) |
| RL-F7 | Production environment | DEPLOYMENT-TIME | OD-P; `web/app.py` `_run_config` (bounded single-threaded MVP serving) | none exists |

## G. Gates (sequence truth)

| ID | Gate | Status | Source | Current truth |
|---|---|---|---|---|
| RL-G1 | Phase 10 closure | FORMAL CLOSURE RECORD CREATED (authoritative on merge) | `docs/governance/PHASE_10_FORMAL_CLOSURE_RECORD.md`; P10-CL0 (PR #538, `OD-P10-CL0-STRUCTURE` Option 2) | PHASE 10 FORMALLY CLOSED under Option 2 when the closure record is merged and post-merge verified; closure binds every open obligation to its hard-blocking lane and converts NOTHING to complete; PHASE-10 CLOSURE ≠ RELEASE APPROVAL |
| RL-G2 | PSRR REGISTERED | IMPLEMENTED LOCAL FOUNDATION (registration only) | `PSRR_..._REGISTRATION.md` | registered; 37-item minimum scope |
| RL-G3 | PSRR TRIGGERED | TRIGGER CONDITION MET (OD-FR1) — EXECUTION NOT AUTHORIZED / NOT STARTED | PSRR registration §4; OD-FR1 (durably recorded in `docs/governance/PSRR_C1_PSRR_EXECUTION_CONTRACT.md` §2) | trigger = intent to reach FIRST PUBLIC PRODUCTION DEPLOYMENT; OD-FR1 (Owner intent = YES) establishes that fact; execution remains separately authorized; this checklist does not trigger it |
| RL-G4 | PSRR EXECUTED | PARTIALLY EXECUTED — APPLICATION-LAYER TRANCHE ONLY | `docs/governance/PSRR_APPLICATION_LAYER_TRANCHE_EXECUTION_RECORD.md`; PSRR-C1 §5.1 | application-layer tranche EXECUTED and independently accepted (21 distinct item numbers, app halves only for split items); provider-dependent tranche, policy substance, and items 35–37 remain; PSRR NOT COMPLETE; NO GO exists |
| RL-G5 | PSRR GO/NO-GO | OPEN (NO GO EXISTS) | same §5–§6 | public production BLOCKED until PSRR = GO |
| RL-G6 | Deployment authorization | BLOCKED | OD-P (ODR) | separate deployment gate + explicit Owner authorization, both required |
| RL-G7 | First public production deployment | BLOCKED | D-PSRR-01; OD-P | requires RL-G5 + RL-G6 |
| RL-G8 | Paid activation | BLOCKED | `D-P8-PL-01 class C` | see RL-E8 |

Sequence: Phase-10 obligations → (Owner intent to deploy publicly) → PSRR trigger → PSRR execution →
PSRR GO + OD-P deployment gate + Owner authorization → first public production deployment → (all
commercial/legal prerequisites) → paid activation. This checklist sits BEFORE all of those gates and
approves none of them.

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
PAID ACTIVATION AUTHORIZED: NO        PSRR TRIGGERED: NO        DEPLOYMENT AUTHORIZED: NO
("PSRR TRIGGERED: NO" = PSRR gate execution has NOT begun and is NOT authorized. Per RL-G3, the §4
trigger CONDITION is now met by the OD-FR1 Owner intent; execution requires separate authorization.)
```
