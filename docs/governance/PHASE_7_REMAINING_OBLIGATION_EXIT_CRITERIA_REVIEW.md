# Phase-7 §25 Remaining-Obligation / Exit-Criteria Review

**Status of THIS record:** governance/documentation-only **§25 review candidate** — authoritative if/when
independently reviewed, Owner-accepted, and merged. It performs the mandatory **P7-C §25 Phase-7
Remaining-Obligation / Exit-Criteria Review**: it classifies **every** original Phase-7 obligation in the
P7-C §18 register into exactly one of the four §25 labels and computes the exit verdict. It does **NOT** close
Phase 7, does **NOT** create a Phase-7 formal closure record, implements nothing, and registers/executes no
PSRR. Phase 7 remains **OPEN / IN PROGRESS**.

## 1. Authority and verified base (read-only)

- **Authoritative branch/tip (verified live):** `feature/atomic-json-session-persistence` @
  **`7fda709209f9c97d67bdaf752de7bda3a951ce15`** (PR #410 P7-I3-closure merge; parents
  `2ee60ec018d3816c47ad20ac2136e61aa1f9d3b9` + `24dbe0f69e6cfd9cebf4e5ca58aec6904679f534`; tree
  `e77d475508f53c6360a5a1b990f3e974842e7455`). Boot check: **BOOT OK**. Working tree clean at review start.
- **Authority:** P7-C §25 (`docs/governance/PHASE_7_API_AND_INTEGRATION_FOUNDATION_P7C_CONTRACT.md`,
  `D-P7C-01`); Standing Phase-7 Authorization `D-P7-STANDING-01`. This §25 review holds **exclusive authority
  over each obligation's final closure classification**; §18 pre-judges none.
- **Increment closures reviewed:** P7-I1 (`P7_I1_…_FORMAL_CLOSURE_RECORD.md`), P7-I2
  (`P7_I2_…_FORMAL_CLOSURE_RECORD.md`), P7-I3 (`P7_I3_…_FORMAL_CLOSURE_RECORD.md`).
- **Evidence reproduced live at `7fda709`:** P7-I1 + P7-I2 + P7-I3 focused **80 passed** (22 + 37 + 21); full
  suite **2105 passed / 1 skipped / 1 xfailed / 0 failed**; delivered modules present
  (`engine/read_export_service.py`, `web/api_v1.py`, `engine/account_store.py`, `engine/export_adapter.py`).

## 2. §25 classification rule (applied)

Every obligation receives EXACTLY ONE of: **A. DELIVERED AND VERIFIED**; **B. INTENTIONALLY DEFERRED WITH
OWNER-REASON-TRIGGER** (OWNER BASIS + REASON + TRIGGER all recorded, else invalid); **C. NOT APPLICABLE TO
ACCEPTED V1 — OWNER ACCEPTED**; **D. STILL REQUIRED BEFORE PHASE-7 CLOSURE**. `PARTIALLY DELIVERED` /
`NON-BLOCKING` / `FUTURE` / `LATER` / `N/A` are NOT final labels — they appear only as explanation beneath a
canonical label. Any single **D** blocks Phase-7 closure.

The obligation set is reconstructed from the **P7-C §18 register itself** (35 rows), not from the gate prompt.

## 3. A — DELIVERED AND VERIFIED (18)

Delivered by P7-I1 / P7-I2 / P7-I3, independently reviewed (A), merged, post-merge verified, and reproduced
live at `7fda709`.

| # | §18 obligation | Delivering increment | Evidence |
|---|---|---|---|
| 1 | Resource model (v1) | P7-I2 | Exactly two GET product surfaces (Project Read + Structured Export) |
| 2 | Service boundary | P7-I1 | Flask-free internal read/export seam `engine/read_export_service.py` |
| 3 | Public API boundary | P7-I2 | `web/api_v1.py` blueprint `/api/v1`, consumes the seam |
| 4 | API versioning | P7-I2 | `api_version` on every response |
| 5 | Authentication | P7-I2 | `Authorization`-header machine credential; browser session rejected |
| 6 | Machine/API identity | P7-I2 | Distinct principal bound to one `owner_account_id`; hash-only secret |
| 7 | Authorization / scopes | P7-I2 | Canonical owner-bound authz; single `project:read` scope; cross-owner isolation |
| 8 | Stable errors | P7-I2 | Non-enumerating `{error:{code,message,request_id}}` (cross-owner ≡ missing) |
| 9 | Request / correlation tracing | P7-I2 | `request_id` resolved/emitted; malformed caller value replaced |
| 10 | Audit (access/security) | P7-I2 | Durable `access_audit`; fail-closed on audit-write failure |
| 11 | Rate limits (protective floor) | P7-I2 | Two-tier (pre-auth bounded-subject + post-auth `api_read`), fail-closed |
| 12 | Export contracts | P7-I2 / I3 | `export_contract_version`; canonical Structured Export |
| 13 | Adapter contract | P7-I3 | `engine/export_adapter.py` `ReferenceExportAdapter` + `validate_equivalence` |
| 14 | Outbound API (export) | P7-I2 / I3 | Export endpoint + canonical→adapter outbound projection |
| 15 | Reference / Test Harness | P7-I3 | Local, deterministic, network-free, vendor-neutral reference adapter proof |
| 16 | Secrets | P7-I2 | Token-style **hash-only** credential secret (never stored in clear) |
| 17 | Revocation | P7-I2 | `revoke_api_credential` + expiry + rotation + bound-account-status enforcement |
| 18 | Compatibility | POLICY FROM v1 (§23) | Public/export **version identity** in force; additive-compatibility policy standing; no breaking change made in v1 |

## 4. B — INTENTIONALLY DEFERRED WITH OWNER-REASON-TRIGGER (17)

Each row records OWNER BASIS / REASON / TRIGGER and confirms the trigger has **NOT** fired. All bases are
pre-existing accepted decisions (no invented decision). Frozen P7-B decisions referenced: D1–D12
(`D-P7C-01`).

| # | §18 obligation | OWNER BASIS | REASON (deferred, not required for accepted v1) | TRIGGER (reactivation) | Fired? |
|---|---|---|---|---|---|
| 19 | **Monitoring** | `D-P7C-01` §10 (**Audit ≠ Monitoring**; monitoring is a distinct preserved obligation, explicitly **not** in the accepted first-public-exposure security baseline; "current minimum not yet frozen") + §18 | Accepted v1 is read/export-first with **no live public-production exposure**; §10 froze basic audit + basic rate-limit as the first-exposure floor (both DELIVERED) and did not freeze an operational-monitoring minimum for v1; delivered audit truthfully covers the accepted surface | Actual public-production exposure establishing the operational-monitoring minimum (and/or the operational-readiness review before first Public Production Deployment) | NO — API not live to the public |
| 20 | **Abuse controls (broad)** | `D-P7C-01` §10 (**basic rate-limit floor ≠ all Abuse Controls**; broad abuse controls a distinct preserved obligation) + §18 | Protective rate-limit floor DELIVERED; advanced/distributed abuse controls not scoped and not needed at the accepted non-live read/export surface | Abuse evidence and/or real public-production exposure | NO |
| 21 | **Partner / External-Integration Sandbox** | `D-P7C-01` §16 / D10 (first proof is **local/reference**, outbound-only); §18 (Reference/Test Harness ≠ Partner Sandbox — two distinct rows) | Reference harness DELIVERED (P7-I3); no partner/external integration selected; a partner sandbox is a separate, un-triggered obligation | A real partner/external-integration need | NO |
| 22 | External-submission provenance (inbound) | `D-P7C-01` §13 / D8 (inbound untrusted-by-default **INVARIANT**; persistence mechanics not frozen) | The untrusted-by-default invariant **holds** (read/export-first v1 has **no inbound surface**, so nothing can violate it); only the provenance-**persistence** mechanics are deferred | An inbound gate is authorized | NO |
| 23 | Deprecation | `D-P7C-01` §23 (compatibility/deprecation **policy from v1**; event deferred) | Read-only v1 has made no breaking change; no deprecation **event** has occurred | First deprecation event | NO |
| 24 | HTTP idempotency | `D-P7C-01` §10 / D5 (idempotency required **before writes**) | Accepted v1 has **no public write surface** (read/export-first, §11) | A write gate is authorized | NO |
| 25 | Quotas (beyond floor) | `D-P7C-01` §10 / §18 (quotas beyond the protective floor deferred until demonstrated need) | Rate-limit floor DELIVERED; no demonstrated need beyond the floor | Abuse / scale evidence | NO |
| 26 | Retries / timeouts | `D-P7C-01` §15 / §18 (adapter-boundary retries/timeouts are an integration concern) | No real vendor/async external boundary exists (P7-I3 is local, synchronous, network-free) | A real adapter / external integration | NO |
| 27 | Import contracts | `D-P7C-01` §10 / §11 / D5 (import contract/version identity **not** part of the read-only contract) | Read/export-first; no import path in v1 | An import gate is authorized | NO |
| 28 | Inbound API | `D-P7C-01` §13 / D8 (external results untrusted; inbound deferred) | Untrusted-result caution; read/export-first; no inbound surface | An inbound gate is authorized | NO |
| 29 | File exchange (governed import) | `D-P7C-01` §26 / §18 (file exchange as governed import deferred) | No import path in v1; an in-memory DTO is **not** file exchange | An import / integration gate | NO |
| 30 | Embedded integration | `D-P7C-01` D11 / §18 | No use case | Demonstrated need | NO |
| 31 | Partner connectors | `D-P7C-01` §18 | No partner selected | A partner use case | NO |
| 32 | Webhooks | `D-P7C-01` §15 / D9 (async/webhook deferred; no Job/Task reserved) | Async deferred; no async lifecycle proven (P7-I3 is synchronous/local) | An async / webhook gate on proven async need | NO |
| 33 | Subsystem durable identity / API | `D-P7C-01` §14 / D3 (subsystem public API + durable identity DEFERRED) | Owner-accepted deferral; **P7-I3 did NOT fire this trigger** — the reference adapter is outbound-only and non-mutating and needs no independent persistent subsystem addressing; root `confirmed_domain` preserved | A real integration requiring independent persistent subsystem addressing | NO |
| 34 | Async / job model | `D-P7C-01` §15 / D9 | No materially asynchronous lifecycle proven; P7-I3 is synchronous/local | Async-lifecycle evidence from a bounded integration | NO |
| 35 | Pagination | `D-P7C-01` §10 / §18 (pagination required only where an unbounded collection exists) | The two v1 surfaces are single-project GET-by-id; **no unbounded/collection surface exists** | The first unbounded collection surface | NO |

## 5. C — NOT APPLICABLE TO ACCEPTED V1 — OWNER ACCEPTED (0)

None. Every deferred §18 obligation carries a canonical activation/review **trigger** (§18 register rule D),
which makes **B** the precise label; none is permanently non-applicable to v1.

## 6. D — STILL REQUIRED BEFORE PHASE-7 CLOSURE (0)

None. No obligation lacks an accepted deferral basis; no deferral trigger has fired; closing on this basis
drops no obligation (every deferred row stays preserved with owner basis + reason + trigger, and public
production remains standing-blocked until PSRR = GO, which re-requires the operational obligations at real
exposure).

## 7. Mandatory focused reviews

- **SECURITY / OPERATIONS DISPLACEMENT CHECK.** P7-C §10 exact text fixes the accepted first-public-exposure
  security floor as **basic access/security audit + basic protective rate limiting** (plus authn, authz,
  version identity, stable errors, correlation, provenance) — **all DELIVERED** — and **explicitly separates**
  Monitoring and broad Abuse Controls out as distinct preserved obligations ("Audit is not Monitoring; the
  basic rate-limit floor is not all Abuse Controls"). Classifying monitoring or broad abuse controls as **D**
  would **add** a requirement the owner-accepted contract did not impose on v1; the honest label is **B**.
  No original security obligation is displaced or hidden.
- **WRITE / IMPORT CHECK.** Accepted v1 has **no public write surface** (§11 read/export-first). PUBLIC WRITE
  API = **B** (trigger: write gate). INBOUND IMPORT = **B** (trigger: inbound/import gate). IDEMPOTENCY = **B**
  (required before writes). MUTATION AUDIT = **B** (required before writes; the general access audit is
  delivered, mutation-specific audit attaches to the write gate). CONCURRENCY CONTROL = **B** (write
  concurrency/conflict rules attach to the write gate). None marked N/A: each is explicitly trigger-deferred to
  "before any write/import capability."
- **SUBSYSTEM CHECK.** Trigger = a real integration requiring independent persistent subsystem addressing. The
  P7-I3 reference adapter is outbound-only, non-mutating, and requires no such addressing → trigger **NOT**
  fired → **B**.
- **ASYNC CHECK.** No accepted use case requires an asynchronous lifecycle; P7-I3 is synchronous/local →
  trigger **NOT** fired → **B**.
- **WEBHOOK CHECK.** No accepted use case requires webhook delivery → **B**.
- **REAL-VENDOR CHECK.** The reference adapter is vendor-neutral and created **no** requirement for a real
  vendor; **WOKWI NOT SELECTED**; no vendor selected here → real-vendor integration remains **B**.
- **FILE EXCHANGE CHECK.** P7-I3 did not implement file exchange; an in-memory DTO is not file exchange; no v1
  import path → **B** (trigger: import/integration gate). Not called delivered.
- **PARTNER SANDBOX CHECK.** Reference/Test Harness (delivered) and Partner/External-Integration Sandbox are
  two distinct §18 rows; the sandbox is classified independently as **B** (trigger: real partner/external
  integration).
- **MONITORING / ABUSE / AUDIT-RETENTION CHECK.** Monitoring = **B**; broad Abuse Controls (incl. distributed
  guessing / fake-id rotation) = **B**. **Access-audit retention/cleanup:** the *basic audit* obligation is
  DELIVERED; retention/cleanup is an operational data-lifecycle concern that P7-C §10 did **not** freeze as a
  v1 obligation and that maps to **no distinct §18 obligation row** — it is preserved as a P7-I2 non-blocking
  observation and belongs to operational readiness (PSRR / operations), so it creates **no D**. It is recorded
  here explicitly rather than buried. PSRR is not used to escape any Phase-7 obligation: every operational
  obligation above is preserved with an owner basis and re-triggers at real public-production exposure.
- **PSRR BOUNDARY.** PRESERVED. PSRR is **not** registered or executed here; it is **not** a substitute for
  §25. Standing rule unchanged: PSRR governance registration after formal Phase-7 closure; PSRR full execution
  before first Public Production Deployment; **public production BLOCKED until PSRR = GO.**
- **OUTSIDE-PHASE-7 CAPABILITIES.** CAP-15…18, AISR, QTA, WS17, STG, ACV, PDF, Email, Output Language, Phase-9
  domain activation, Phase-8 billing, Phase-10 commercial/legal/security/ops are **OUTSIDE the Phase-7
  obligation register** (D11 / §17 / §27) — not classified as one of the four §25 statuses.

## 8. Reassessed prior non-blocking observations

- **P7-I2:** post-auth limiter ordering; unknown-id micro-timing; inert `API_CREDENTIAL_STATUSES`;
  no-presented-id pre-auth-limiter limitation; fake-credential-id rotation / distributed abuse → all map to
  **Monitoring / broad Abuse Controls (B)** or are residual hardening within the DELIVERED rate-limit floor;
  none maps to an undelivered §18 obligation. `access_audit` append-only / no retention → operational
  lifecycle, no §18 row (see §7); **no D**.
- **P7-I3:** static import guard makes no dynamic-import claim (a truthful scope statement, not an unmet
  obligation); reference harness ≠ partner sandbox (row 21 = B); file exchange not implemented (row 29 = B);
  superseded evidence tags absent remotely (recorded truthfully; no obligation).

No material obligation is concealed inside a "non-blocking observation."

## 9. Exit decision

**STILL REQUIRED COUNT: 0.**

**PHASE-7 EXIT VERDICT: PASS — ELIGIBLE FOR A SEPARATE FORMAL PHASE-7 CLOSURE GATE.**

Scope of this verdict: under the owner-accepted **read/export-first v1** scope, **no** P7-C §18 obligation is
STILL REQUIRED before a separate formal Phase-7 closure gate. This verdict is an **eligibility** finding only;
it does **NOT** close Phase 7, does **NOT** assert production readiness, and does **NOT** authorize public
production. Monitoring, broad abuse controls, audit retention, partner sandbox, write/import, inbound,
subsystem durable identity, async/webhook, and real-vendor integration remain **preserved obligations** that
re-trigger at real public-production exposure / real integration, enforced by the standing **PSRR = GO** block
on public production and by each obligation's recorded trigger.

**NEXT MINIMUM GATE:** a separate **P7-CLOSE — Formal Phase-7 Closure gate** (owner-run under
`D-P7-STANDING-01` §25 closure criteria) — **NOT STARTED**, and **not** performed in this gate.

## 10. Adversarial self-review (20 checks)

1. Every §18 obligation exactly one canonical status — **YES** (35 rows: 18 A + 17 B + 0 C + 0 D = 35).
2. No obligation disappeared — **YES** (all 35 §18 rows present).
3. Audit conflated with monitoring — **NO** (audit A row 10; monitoring B row 19; kept distinct).
4. Rate limit conflated with abuse controls — **NO** (floor A row 11; broad abuse B row 20).
5. Reference harness conflated with partner sandbox — **NO** (harness A row 15; sandbox B row 21).
6. DTO called file exchange — **NO** (row 29 B; explicitly rejected).
7. Writes marked N/A — **NO** (write/import/idempotency/mutation-audit/concurrency all B, trigger-deferred).
8. Idempotency / mutation-audit / concurrency before-write rules ignored — **NO** (all B; §7 WRITE check).
9. Import version identity ignored — **NO** (import contracts B row 27; §10 excludes it from read-only v1).
10. Subsystem trigger fired — **NO** (row 33; P7-I3 outbound-only, non-mutating).
11. Async trigger fired — **NO** (row 34).
12. Webhook trigger fired — **NO** (row 32).
13. Real-vendor trigger fired — **NO** (vendor-neutral; Wokwi not selected).
14. PSRR used to bury a Phase-7 obligation — **NO** (each operational obligation preserved with owner basis +
    trigger; §7 PSRR boundary).
15. Phase-8/9/10 / CAP capabilities pulled into Phase 7 — **NO** (recorded OUTSIDE the register, §7).
16. A STILL-REQUIRED item mislabeled deferred — **NO** (no trigger has fired; each B has an accepted basis).
17. Each B row has Owner basis + reason + trigger — **YES** (§4 table).
18. Phase 7 accidentally closed — **NO** (Phase 7 OPEN; this is a review candidate; no closure record created).
19. D-FPC-MAP-06 — **PASS** (consumes existing canonical authorities; no new registry/orchestrator/service/
    tracker; governance-only synchronization).
20. Lean — **PASS** (one new review doc + three current-truth syncs; ODR unchanged; no code/test change).

## 11. Boundary — what this review does NOT do

- Does **NOT** close Phase 7 (remains OPEN / IN PROGRESS).
- Does **NOT** create a Phase-7 formal closure record (that is the separate P7-CLOSE gate).
- Implements nothing; modifies no application code or tests.
- Does **NOT** register or execute PSRR; does **NOT** start Phase 8/9/10; authorizes no deployment/release.
- `OWNER_DECISION_REGISTER.md` **UNCHANGED** — every classification grounds in existing accepted decisions
  (`D-P7C-01` §§7–27, `D-P7-STANDING-01`, frozen P7-B D1–D12); no new durable Owner decision is required.

## 12. Result

**PHASE-7 §25 REMAINING-OBLIGATION / EXIT-CRITERIA REVIEW: COMPLETE (candidate).** 35 obligations classified
(18 DELIVERED AND VERIFIED; 17 INTENTIONALLY DEFERRED WITH OWNER-REASON-TRIGGER; 0 NOT APPLICABLE; **0 STILL
REQUIRED**). **PHASE-7 EXIT VERDICT: PASS — ELIGIBLE FOR A SEPARATE FORMAL PHASE-7 CLOSURE GATE.** Phase 7
remains **OPEN**; P7-CLOSE is **NOT STARTED**; PSRR remains a future registration (public production blocked
until PSRR = GO). Authoritative if/when this governance candidate is independently reviewed, Owner-accepted,
and merged.
