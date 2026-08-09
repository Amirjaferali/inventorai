# P8-I1 — Plan & Entitlement Foundation — BOUNDED IMPLEMENTATION CONTRACT (CORRECTED)

**Status of THIS record:** governance/documentation-only **bounded implementation-contract CANDIDATE
(corrected; verdict-B remediation)** — authoritative if/when independently reviewed, Owner-accepted, merged,
and post-merge verified. **It confers NO implementation authority and does NOT implement P8-I1.** This corrected
candidate supersedes the prior P8-I1-C candidate `2a4b65b` (tree `a166e43`), which is **evidence only — NOT
accepted, NOT merged**. It incorporates the required corrections **R1 (explicit P8-C refinement/deviation
record), R2 (engine-wide OD-N static guard), R3 (complete fail-closed state/RED matrix + account-status
semantics), R4 (atomic assignment+audit)** plus the review cleanups. **DOCUMENTED NO-VALID-RED for this contract
gate** (documentation-only; the contract defines the future P8-I1 RED tests).

## 1. Authority and verified base (read-only)

- **Authoritative branch/tip (verified live, unchanged):** `feature/atomic-json-session-persistence` @
  **`5db47a2959507fa0cb8a4c717d32e617f23a08f0`** (PR #416 merge of accepted P8-C candidate `1aed84a`; merged
  tree `d3ae4a5` == accepted P8-C tree; prior P8-I1-C candidate `2a4b65b` NOT merged). Boot OK; clean.
- **Contract-of-record:** P8-C (`docs/governance/PHASE_8_SUBSCRIPTION_BILLING_ENTITLEMENTS_P8C_CONTRACT.md`).
- **Binding governance:** OD-I, OD-N, OD-O, OD-K, D-P8-PL-01, OD-P/Phase-10, D-PSRR-01. A separate P8-I1
  implementation authorization/gate is required before any code.

## 2. Fixed purpose (only this)

Prove, end-to-end, **Account → Commercial Plan Identity → Entitlement Evaluation → Governed Capability Access**,
**WITHOUT external payment processing.** P8-I1 is **NOT "billing"** — it is the provider-neutral commercial
identity + entitlement foundation and the smallest meaningful implementation slice.

## 3. R1 — EXPLICIT, BOUNDED REFINEMENT / DEVIATION FROM P8-C (surfaced for Owner acceptance; NOT a silent supersession)

This corrected P8-I1-C records an **explicit, bounded refinement** of three P8-C provisions **for the P8-I1
increment only**. **This is NOT a silent reinterpretation or supersession of P8-C**; the accepted P8-C contract
history is preserved and unedited. The refinement is **conditional** — it becomes authoritative only if/when
this candidate is independently reviewed, Owner-accepted, merged, and post-merge verified.

**Provision 1 — plan-catalog persistence/storage model.**
- *P8-C stated:* the plan catalog is durable/versioned data, **durable via the existing SqliteAccountStore
  schema lifecycle** (P8-C §18), and "plans are data, not code" (P8-C §5 Q1).
- *P8-I1 refinement:* the plan catalog is a **code-resident, immutable, versioned declarative data structure**
  (`engine/plan_catalog.py`) — still declarative *data* (capability-flag values, not imperative logic), but
  resident in a reviewed, versioned code module rather than durable DB rows.
- *Why safer/smaller for P8-I1 (repository evidence):* the repo has **no admin CRUD, no config-management
  surface, and no DB-driven catalog machinery**; domain packs / label tiers are already code/config-resident
  data by convention. A DB-backed catalog in P8-I1 would require catalog-management code that P8-I1 explicitly
  excludes. A code-resident catalog is smaller, fully reviewable, and **evolvable without per-account
  entitlement snapshots or schema migrations**.

**Provision 2 — P8-I1 subscription/assignment shape.**
- *P8-C stated:* the canonical subscription-state model includes `free / active / past_due / canceled /
  expired / grandfathered` (P8-C §5 Q2) and period boundaries belong to the Phase-8 model.
- *P8-I1 refinement:* the P8-I1 durable `commercial_assignments` row carries **only the plan identity binding**
  (`account_id → plan_id, plan_version` + timestamps). It carries **no lifecycle-state column and no period
  boundaries.**
- *Why:* P8-C's own increment decomposition assigns **Subscription Lifecycle to P8-I3**; the full lifecycle
  state machine + period boundaries are lifecycle concerns. P8-I1 proves identity + evaluation only.

**Provision 3 — lifecycle-state / period-boundary timing.**
- *Refinement:* lifecycle states (`past_due / canceled / expired / grandfathered`), period boundaries, and
  grandfathering/lifecycle mechanics are **deferred to P8-I3** (consistent with P8-C's decomposition).

**What remains BINDING from P8-C (unchanged):** the canonical plan-identity concept `(plan_id, plan_version)`;
the **hybrid entitlement model — derived at evaluation, no stored snapshot**; entitlement evaluated through one
canonical seam (no scattered plan-name branching); durable commercial state via the account-store schema
lifecycle (assignment table); all §2 invariants (OD-I/OD-N/OD-O/OD-K/D-P8-PL-01/OD-P/D-PSRR-01); all critical
distinctions; provider neutrality; no public paid activation; the full canonical subscription-state model and
period boundaries **remain the Phase-8 target, owned by P8-I3**.

**Future schema-evolution path (honest; no over-claim).** The repository currently uses **additive idempotent
`CREATE TABLE IF NOT EXISTS`** and has **no established `ALTER TABLE` migration framework.** Therefore this
contract does **NOT** imply lifecycle columns can later be added to `commercial_assignments` "for free." **P8-I3
MUST choose, under its own separately-reviewed contract, between (a) a new additive lifecycle/state table, or
(b) a specifically-designed idempotent schema-evolution mechanism if in-place column addition is later
justified.** That future design is **not decided here.**

## 4. Canonical model (P8-I1, live-code-grounded)

1. **Commercial Plan Identity** = `(plan_id: str, plan_version: str)`.
2. **Versioned Plan Catalog** = code-resident immutable versioned declarative data (`engine/plan_catalog.py`):
   `plan_id@plan_version → entitlement descriptor` (capability-flag values). Includes the neutral technical
   default identity (§7).
3. **Commercial Assignment (P8-I1)** = additive durable `commercial_assignments` (plan identity only; §3/§14).
4. **Entitlement Definition** = the per-plan capability descriptor in the catalog, versioned with the plan.
5. **Effective Entitlement Evaluation** = **DERIVED at evaluation** from durable assignment → plan identity →
   catalog descriptor; **no stored effective-entitlement snapshot** (P8-C-binding).
6. **Governed Capability Access** = one **Flask-free, fail-closed** seam
   `evaluate_entitlement(account_store, account_id, capability) -> Decision{allow, reason, plan_identity}`
   (`engine/entitlement_service.py`, mirroring `engine/read_export_service.py` + `EntitlementError`). Callers
   ask a **capability-level** question — never `if plan == "..."`.

## 5. R3 — Fail-closed commercial-state model + account-status semantics

**Six commercial states (all materially covered by RED §9):**

| State | Meaning | Behavior |
|---|---|---|
| A. Legitimate legacy/default | **valid active account, no assignment row** | → **technical default identity** → default/free entitlements (**NOT** an error) |
| B. Explicit valid plan | active account; row; plan_id@version in catalog | → deterministic derived entitlements |
| C. Unknown explicit plan reference | row; plan_id/version NOT in catalog | **FAIL CLOSED for every capability** |
| D. Malformed/corrupt commercial assignment | invalid/corrupt row | **FAIL CLOSED for every capability** |
| E. Catalog/descriptor failure | malformed descriptor / invalid or unresolvable catalog entry | **FAIL CLOSED for every capability** |
| F. Missing/nonexistent account | no such `account_id` | **FAIL CLOSED**; **MUST NOT receive the legacy/default identity** |

**Account-status semantics (use EXISTING Phase-5 truth; invent nothing).** Canonical
`ACCOUNT_STATUSES = {"active", "disabled", "deleted"}` (`engine/account_store.py`). The entitlement seam:
**active** account → evaluate per states A/B (or C/D/E/F fail-closed); **disabled** or **deleted** account →
**FAIL CLOSED** (no commercial capability for a non-active account), consistent with the existing web policy
that gated actions require an active account. The seam introduces **no new account-status semantics** and does
not contradict Phase 5.

**No user-visible behavior change / no real paywall.** P8-I1 introduces **no Owner-approved user-facing
paywall**; therefore the fail-closed rules for states C/D/E/F and non-active accounts **must not change any
current user-visible behavior outside the neutral P8-I1 proof seam** (§7). Existing default/free flows for valid
active accounts are unchanged (state A).

## 6. R2 — Engine-wide OD-N static guard (inverted allowlist) + behavioral guard (complementary)

**Static guard (engine-wide, inverted allowlist).** **No module under `engine/` may import** `plan_catalog`,
`entitlement_service`, or any other commercial-plan/entitlement implementation symbol — **except** an explicit
minimum allowlist. The allowlist may contain **only** modules genuinely required by the bounded P8-I1 design:
- `engine/entitlement_service.py` (the seam itself);
- `engine/account_store.py` **only if technically necessary** (durable assignment access);
- the single specific neutral service-seam file **only if it is actually touched** by the P8-I1 proof.

**No wildcard exceptions.** The implementation test **AST-scans all relevant `engine/*.py` modules** (the
established static-import-guard precedent, P7-I3) and asserts no commercial import appears outside the allowlist.
This replaces the prior narrow five-module guard (reformulated RED §9 #8).

**Behavioral guard (separate, complementary).** The **same technical inputs evaluated under differing
commercial identities produce identical technical evaluation** (scoring/progression/evidence/safety outputs
identical). Static + behavioral guards are complementary and both required.

## 7. Capability enforcement target + neutral identifiers (cleanups 1 & 3)

P8-I1 proves the seam through a **minimum neutral/internal governed-capability path** — it does **NOT** paywall
any existing user-facing capability (no Owner packaging decision). **Repository limitation (reported):** there
is no repository-authorized user-facing capability that may yet be restricted by plan. The **technical default
plan identifier is unmistakably internal** (e.g. `__default_technical__` — clearly not a marketable plan name)
and the neutral proof capability is an internal capability key. **The internal technical default plan
identifier and the neutral proof capability MUST NOT be exposed through any public API or UI in P8-I1**
(no route/template/response surface). User-facing paywalling is deferred to a later increment gated behind an
accepted Owner packaging decision.

## 8. R4 — Atomic assignment + audit (assignment IS mutable in P8-I1)

P8-I1 **permits mutation** of the commercial assignment (the neutral proof requires setting a non-default
assignment). Therefore: **the assignment change AND its `commercial_audit` event MUST be committed in the SAME
`BEGIN IMMEDIATE` transaction** (the store's `_write()` critical section). **No two-step** (assignment commit
then audit commit) is acceptable; a crash between the two must be impossible — **no unaudited commercial
mutation may exist.** The RED matrix includes a meaningful **atomicity/rollback** test (§9 #12). The
`commercial_audit` is **minimal** (assignment set/change events only; append-only; distinct from the security
`access_audit`) — **not** an elaborate billing-event system.

## 9. Corrected future RED-test matrix (all genuinely RED on base `5db47a2`)

In **`tests/test_p8_i1_plan_entitlement_foundation.py`** (the engine-wide OD-N import guard may be a sibling
test). RED on base because `engine/plan_catalog.py`, `engine/entitlement_service.py`, and `commercial_assignments`
do not exist.

| # | Observable behavior | Why RED now | Expected GREEN | Protected risk |
|---|---|---|---|---|
| 1 | State A: valid active account, no row → technical default identity → default/free entitlements | seam/table absent | absence resolves to default; free capabilities allowed | legacy accounts losing access |
| 2 | State B: explicit valid plan → deterministic derived entitlements | seam absent | catalog-derived entitlements | broken plan resolution |
| 3 | State C: unknown explicit plan reference → fail closed (every capability) | seam absent | seam denies | silent grant on unknown plan |
| 4 | State D: malformed/corrupt assignment → fail closed | seam absent | seam denies | silent grant on corrupt state |
| 5 | State E: catalog/descriptor failure → fail closed | seam absent | seam denies | silent grant on catalog error |
| 6 | State F: missing/nonexistent account → fail closed AND does NOT get default identity | seam absent | seam denies; not defaulted | privilege via nonexistent account |
| 7 | Disabled/deleted account → fail closed | seam absent | seam denies for non-active status | commercial capability for inactive account |
| 8 | **Derived-not-snapshot (risk-protective):** changing the catalog descriptor for an already-assigned plan changes the effective entitlement with **no per-account write/migration** | no derivation exists | effective entitlement follows the versioned catalog, not a stored copy | stale-entitlement drift |
| 9 | Governed capability answered via `evaluate_entitlement`, not direct plan-name comparison; **no plan-name branching outside the canonical commercial layer** (grep/AST invariant) | no seam / no commercial layer | capability question via the seam only | scattered `if plan==` logic |
| 10 | **OD-N behavioral:** identical technical input under differing commercial identities → identical technical evaluation | no commercial identity to vary | technical outputs invariant to plan | paid "favorable truth" |
| 11 | **OD-N static (engine-wide inverted allowlist):** no `engine/*.py` imports a commercial symbol except the minimal allowlist | no commercial module exists | AST scan finds none outside allowlist | commercial coupling into core |
| 12 | **R4 atomicity:** a forced failure during an assignment change rolls back BOTH the assignment and its audit (no unaudited mutation; no partial write) | no assignment/audit path exists | assignment+audit commit or roll back together | unaudited/partial commercial mutation |
| 13 | Additive migration on an existing (pre-P8) DB — new table(s) created idempotently; project/account data untouched | table absent | idempotent create; data intact | destructive migration |
| 14 | Fresh DB initializes all tables incl. commercial | table absent | fresh store has new table(s) | init breakage |
| 15 | Account ownership/auth semantics unchanged; credential revocation plan-independent | n/a → asserts no regression | Phase-5/Phase-7 semantics identical; a revoked credential stays revoked regardless of plan | authz/revocation regression |

Each test is behavioral or enforces a named architectural invariant (engine-wide import prohibition;
no-plan-name-branching); no test merely asserts a file exists or a single table shape for its own sake. None is
fabricated for ceremony.

## 10. Implementation allowlist (re-evaluated after R1–R4; narrowly bounded)

- **REQUIRED (create/extend):** `engine/plan_catalog.py` (NEW — code-resident versioned catalog + entitlement
  descriptors + internal technical default identity); `engine/entitlement_service.py` (NEW — Flask-free
  fail-closed `evaluate_entitlement` + `EntitlementError`; six-state + account-status handling);
  `engine/account_store.py` (EXTEND — additive `commercial_assignments` + minimal `commercial_audit` tables in
  `_SCHEMA`; `get_commercial_assignment`; `set_commercial_assignment` writing assignment **and** audit in ONE
  `_write()` transaction; `record_commercial_audit` internal to that transaction);
  `tests/test_p8_i1_plan_entitlement_foundation.py` (NEW — §9 matrix).
- **LIKELY:** the engine-wide OD-N import-guard test (may be a sibling test file); a single neutral service-seam
  touch **only if** the neutral governed-capability proof genuinely requires it (prefer an internal capability
  constant; no route/UI).
- **PROHIBITED:** `web/api_v1.py` scope semantics; `web/app.py` routes/packaging; any templates/UI; exposing the
  internal technical default plan id or neutral capability via any public API/UI; domain registry/activation;
  `record_rate_attempt` repurposing; engine scoring/progression/safety modules (must stay commercial-free);
  any payment/provider code; any quota/metering code; any lifecycle (renewal/downgrade/cancel/expiry/
  proration/cancellation-timing) code; any dependency/CI change; any change to Phase-7 credential/scope/
  revocation semantics.

## 11. Distinctions carried forward (binding)

- **CREDENTIAL REVOCATION IS PLAN-INDEPENDENT** — a revoked/expired Phase-7 credential stays revoked/expired
  regardless of plan; plan status never revokes or un-revokes a credential; P8-I1 changes no credential/scope
  semantics.
- **Security rate limit ≠ commercial quota** — `record_rate_attempt` stays security/abuse; quotas are P8-I2.
- **API scope ≠ paid entitlement** — P8-I1 establishes only the entitlement side; not wired into the API path
  (later increment; when wired, entitlement is ADDITIONAL to, never replacing, scope).
- **Plan/domain-pack entitlement ≠ domain activation authority** — commercial identity never activates a domain.

## 12. Data / downgrade anti-lock-in (retained; cleanups 4 & 5)

P8-I1 implements no lifecycle and **no proration/cancellation timing** (those remain later Owner/business
decisions). The derived-entitlement design (no per-account snapshot) keeps future safe downgrade possible.
**Retained anti-lock-in obligation (non-blocking):** future **P8-I2/P8-I3/Phase-10** gates MUST explicitly
address continued **access/export of owner-existing data after a commercial downgrade**; **commercial
entitlement decrease must never silently delete owner data** (OD-O). P8-I1 does not solve future lifecycle
policy prematurely.

## 13. Schema / migration (exact; per repository convention)

- **`commercial_assignments`** — `account_id TEXT PRIMARY KEY, plan_id TEXT NOT NULL, plan_version TEXT NOT
  NULL, assigned_at TEXT NOT NULL, updated_at TEXT NOT NULL, FOREIGN KEY(account_id) REFERENCES
  accounts(account_id)` (one assignment/account; **no lifecycle/period columns** — §3).
- **`commercial_audit`** (minimal, append-only) — `event_id INTEGER PRIMARY KEY, account_id TEXT NOT NULL,
  event_type TEXT NOT NULL, from_plan TEXT, to_plan TEXT, created_at TEXT NOT NULL`.
- **Additive strategy:** append `CREATE TABLE IF NOT EXISTS …` to `_SCHEMA`; applied idempotently in the
  existing `__init__` `BEGIN IMMEDIATE` loop. **Assignment mutation** uses the store's `_write()` (`BEGIN
  IMMEDIATE`) and writes assignment + audit **atomically** (R4). **Concurrency:** single shared connection +
  `RLock`. **Fresh DB:** created. **Existing DB:** added, data untouched. **Rollback:** older binary ignores
  the new tables (no destructive change). **No `ALTER TABLE` is used or implied** (§3 future path).

## 14. D-FPC-MAP-06

Reuses `engine/account_store.py` (durable assignment + account identity), Phase-5 identity/authorization/
ownership, `engine/record_store.py` (unchanged). The **new** bounded seams (`plan_catalog` +
`entitlement_service`) are justified — entitlement evaluation is a distinct responsibility not owned by account
identity, authorization, ownership, API credentials, security rate-limiting, access audit, or record storage.
**P8-I1 must NOT become a generic BillingService.**

## 15. Test scope (implementation candidate)

Focused `tests/test_p8_i1_plan_entitlement_foundation.py` (+ OD-N import-guard); account-store/schema-migration
regressions (`tests/test_p5_1_account_credential_foundation.py`, `tests/test_p4_1a_record_store.py`);
authorization/account regressions (`tests/test_p5_3_project_ownership_authorization.py`,
`tests/test_p5_2_auth_sessions_verification_recovery.py`); directly-impacted service tests
(`tests/test_p7_i1_read_export_service.py`). **Full-suite verification is MANDATORY** for the implementation
candidate per current governance precedent (green baseline **2105 passed / 1 skipped / 1 xfailed / 0 failed**);
the candidate must show 0 failures.

## 16. No UI

P8-I1 adds **no** pricing page, plan selector, subscription page, admin commercial UI, or checkout UI.

## 17. Owner / business decisions

**None blocks P8-I1.** The technical default identity is an internal engineering constant, not a marketed name.
Standing deferred Owner/business decisions — plan names, prices, trial policy, packaging, enterprise packaging,
grandfathering, refund, tax, **proration/cancellation timing**, provider choice — are **NOT required** for the
foundation and are invented by none of this contract. **R1 refinement acceptance:** the bounded P8-C refinement
(§3) is surfaced for Owner acceptance **as part of accepting this corrected candidate** (its independent review
+ Owner acceptance + merge + post-merge verification); it is recorded here as **conditional/candidate**, not as
an authoritative pre-merge decision. **No `OWNER_DECISION_REGISTER.md` entry is added** — the refinement is an
implementation-architecture refinement of an existing accepted contract, surfaced via this candidate and
accepted at its merge (consistent with the P7-I* increment-contract precedent of leaving ODR unchanged); it is
**not** a separate standing Owner-level decision distinct from accepting this contract.

## 18. Acceptance criteria (for the later P8-I1 implementation candidate)

Candidate based on this accepted corrected P8-I1 contract; **exact RED evidence** (§9 genuinely failing on the
verified base for the intended reasons) **before** implementation; **GREEN** after; additive migration
compatible with existing DBs + correct fresh-DB init (§9 #13/#14); **no regression** to existing/default
accounts (§9 #1; full suite 0 failures); deterministic entitlement evaluation (§9 #2); **derived-not-snapshot**
proven against genuine stale-entitlement risk (§9 #8); **centralized entitlement seam — no direct plan-name
branching outside the canonical commercial layer** (§9 #9); **plan-neutrality proven** behaviorally + the
**engine-wide** static guard (§9 #10/#11; no scoring/progression/safety commercial coupling); all fail-closed
states + non-active-account + missing-account covered (§9 #3–#7); **atomic assignment+audit** (§9 #12);
credential revocation plan-independent + ownership/auth unchanged (§9 #15); **no payment/provider code; no
quota; no lifecycle; no Phase-10 leakage; no public paid activation; provider-neutral; internal identifiers not
publicly exposed**; documentation/current-truth sync appropriate to implementation status. No criterion may be
false-greenable (no exception-swallowing; RED must fail for the intended reason).

## 19. Result

**P8-I1 — Plan & Entitlement Foundation: BOUNDED IMPLEMENTATION CONTRACT CANDIDATE (CORRECTED).** Supersedes the
prior candidate `2a4b65b` (evidence only). Records the explicit bounded P8-C refinement (§3, surfaced for Owner
acceptance; honest future schema-evolution path), the engine-wide OD-N static guard (§6), the complete
fail-closed six-state + account-status model and 15-test RED matrix (§5/§9), and the atomic assignment+audit
rule (§8) — preserving OD-I/OD-N/OD-O/OD-K/D-P8-PL-01 and all §11 distinctions, provider-neutral, no public paid
activation, no user-facing paywall. **P8-I1 is NOT implemented; this is a contract candidate only.** No
implementation begins until this corrected candidate → independent review → Owner exact-candidate acceptance →
merge → post-merge verification → a separate P8-I1 implementation authorization/gate.
