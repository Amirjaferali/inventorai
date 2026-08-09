# P8-I2 — Commercial Usage Quotas / Limits — BOUNDED IMPLEMENTATION CONTRACT

**Status of THIS record:** governance/documentation-only **bounded implementation-contract CANDIDATE** —
authoritative if/when independently reviewed, Owner-accepted, merged, and post-merge verified. **It confers NO
implementation authority and does NOT implement P8-I2.** It defines the smallest bounded P8-I2 increment: the
commercial usage-limit architecture, the quota subject/policy/window models, atomic evaluate-and-consume,
idempotency, the anti-lock-in data-access boundary, the security/API/OD-N separations, the future RED matrix,
the anticipated-file allowlist, and acceptance criteria. **DOCUMENTED NO-VALID-RED for this contract gate.**

## 1. Authority and verified base (read-only)

- **Authoritative branch/tip (verified live):** `feature/atomic-json-session-persistence` @
  **`2bf389ddaa16b6f92a9dd505e65987686f0531fa`** (PR #418 merge of the accepted P8-I1 implementation `f55ce02`;
  parent 2 `f55ce02`; merged tree `814d15da…` == accepted P8-I1 impl tree → post-merge verified). Boot OK; clean.
- **Contracts of record:** P8-C; P8-I1 bounded contract; **P8-I1 implementation merged** (`engine/plan_catalog.py`,
  `engine/entitlement_service.py`, `engine/account_store.py` commercial tables, `tests/test_p8_i1_plan_entitlement_foundation.py`).
- **Binding governance:** OD-I, OD-N, OD-O, OD-K, D-P8-PL-01, OD-P/Phase-10, D-PSRR-01. A separate P8-I2
  implementation authorization/gate is required before any code.

## 2. Fixed purpose (only this)

Establish a **provider-neutral commercial usage-limit foundation** that can later answer: has this commercial
principal consumed N units of governed commercial capability X? is another use of X allowed under the effective
quota policy? when does the applicable quota window begin/end/reset? how is usage recorded atomically and
audibly? how are retries/replays prevented from double-charging where idempotency applies? — **WITHOUT** inventing
final packaging, real limit values, production paid activation, changing technical truth, or replacing security
rate limits. Smallest meaningful next increment after P8-I1.

## 3. Hard separations (binding; never conflated)

- **SECURITY RATE LIMIT ≠ COMMERCIAL USAGE QUOTA.** `record_rate_attempt` and every security/abuse mechanism
  stay **security-only**. P8-I2 MUST NOT: reuse security counters for commercial accounting; infer entitlement
  from rate-limit state; weaken/disable security or abuse controls for higher-tier/enterprise customers; or make
  security limits configurable by commercial plan. **A paid customer can still be security-rate-limited.**
- **QUOTA ≠ ENTITLEMENT.** Entitlement (P8-I1): *may this commercial identity use X at all?* Quota (P8-I2): *if
  entitled, how much/how often may X be consumed within the applicable window?* Kept as distinct evaluations,
  never one ambiguous boolean. Canonical flow: **Account/Principal → Commercial Plan Identity → Entitlement
  Evaluation → Commercial Quota Evaluation → Governed Capability Access.**
- **API SCOPE ≠ COMMERCIAL QUOTA; CREDENTIAL ≠ QUOTA SUBJECT.** A request may need ALL of: valid credential AND
  authorized API scope AND commercial entitlement AND available quota — never collapsed. **CREDENTIAL REVOCATION
  IS PLAN/QUOTA-INDEPENDENT** (revoked stays revoked). Phase-7 credential/scope semantics unchanged.
- **DOMAIN ENTITLEMENT ≠ DOMAIN ACTIVATION.** Quota state never activates an engineering domain and domain
  activation is not metered.

## 4. Proposed architecture (D-FPC-MAP-06; live-code-grounded)

**Reused (not duplicated):** the P8-I1 entitlement seam `engine.entitlement_service.evaluate_entitlement`
(entitlement is checked FIRST); the P8-I1 code-resident versioned plan catalog `engine.plan_catalog`; the durable
`SqliteAccountStore` schema lifecycle + `_write()` (`BEGIN IMMEDIATE`) atomic critical section; account identity
+ `ACCOUNT_STATUSES`.

**New bounded seam (justified — usage accounting/enforcement is a distinct responsibility not owned by
entitlement, identity, security rate-limiting, API credentials, ownership, records, or the commercial-assignment
audit):** `engine/quota_service.py` — a Flask-free seam mirroring the entitlement-service pattern:
`consume_quota(account_store, account_id, meter, amount=1, now=None, idempotency_key=None) -> QuotaDecision`
and a read-only `evaluate_quota(account_store, account_id, meter, now=None) -> QuotaDecision`. **NOT** a
`BillingService` / `CommercialPlatform` / `SubscriptionManager` / generic policy engine.

## 5. Quota subject model

The P8-I1 commercial identity is **account-oriented**, so the canonical quota subject is **(account_id, meter)** —
the commercial **account principal**, **never** the browser session and **never** the API credential id. When API
usage is later sold, the Phase-7 machine/API credential resolves to its existing `owner_account_id` binding and
quota is charged to **that account principal** (P8-I2 does not change Phase-7 credential semantics and does not
bind quota to credential or browser identity).

## 6. Quota policy model + source of truth (11 required answers)

Quota policy is **declarative data in the same versioned P8-I1 code catalog** (a parallel `quota_descriptor` on
the plan identity), consumed derived-at-evaluation — **no per-account policy snapshot**, no DB plan-admin, no
generic policy engine; changing packaging is a reviewed catalog code change, never an account-row rewrite.

1. **Quota Policy Identity** = `(plan_id, plan_version, meter)`.
2. **Meter identity** = a **stable canonical meter string** constant (for the proof: an internal
   `__quota_proof_meter__`); never a vague "activity"/"usage".
3. **Quota unit** = one governed commercial operation (unit increment; §13 amount rules).
4. **Quota amount/ceiling** = declarative integer; **`UNLIMITED` sentinel** (a named marker, NOT a magic huge
   int); **`0` is a valid explicit policy** (deny all) distinct from missing/malformed (fail closed).
5. **Usage window** = smallest **technical** window (§7).
6. **Current usage** = durable counter per `(account_id, meter, window_key)`.
7. **Remaining allowance** = **derived** `max(0, limit − used)` (fail-safe when `used > limit`, §12).
8. **Decision** = one of `allowed` / `denied_not_entitled` / `denied_quota_exhausted` /
   `denied_invalid_account_or_commercial_state` / `internal_fail_closed` (machine-level only; §10). No public API
   response contract.
9. **Consumption mutation** = **atomic evaluate-and-consume** in ONE `BEGIN IMMEDIATE` (§9).
10. **Auditability** = the durable counter is the **single canonical enforcement source**; retry-safety uses a
    keyed idempotency record written in the SAME transaction (no second competing truth source; §8/§11).
11. **Idempotency / duplicate protection** = optional `idempotency_key` (§11).

## 7. Quota-window model (explicit technical window; NOT final billing cadence)

P8-I2 defines the **smallest technical window** only: a policy window is either **`{"kind": "lifetime"}`** (no
reset) or **`{"kind": "fixed", "seconds": N}`** (a fixed-length technical reset window). The durable
`window_key` is derived deterministically from an **injectable time source** (§8) for fixed windows, and a
constant for lifetime. **Explicit bounded refinement note (surfaced, not silent):** this technical window is
**NOT** the final marketed subscription billing period — **P8-I3 owns subscription lifecycle + period-boundary
mechanics**; if quota policy later binds to real billing periods, P8-I3 integrates it under its own gate. P8-I2
must not silently depend on final billing cadence.

## 8. Time source

Window-key derivation for fixed windows uses an **injectable clock** (`now` passed into `consume_quota` /
`evaluate_quota`, consistent with the account-store convention of callers passing `now_iso`) — **no scattered
`datetime.now()` in quota logic**, and no generic time framework. Lifetime windows need no clock.

## 9. Atomic evaluate-and-consume (critical — no oversubscription)

`consume_quota` performs, inside ONE `_write()` (`BEGIN IMMEDIATE` — the store's RESERVED-lock critical
section): (a) if `idempotency_key` supplied and already recorded for `(account_id, meter, key)` → return the
prior `allowed` outcome **without a second increment**; (b) read the current counter for
`(account_id, meter, window_key)`; (c) if `used + amount > limit` → `denied_quota_exhausted` (**no increment**);
(d) else increment the counter by `amount` **and** insert the idempotency row (if a key was supplied)
atomically → `allowed`. Because the increment and the exhaustion check share the RESERVED-lock transaction,
concurrent writers **cannot** oversubscribe a hard cap (no `N+1`). **Entitlement is evaluated first** (P8-I1
seam, read-only) and a non-entitled/invalid/non-active/missing subject → deny **before** any counter write.
Guarantees are exactly SQLite `BEGIN IMMEDIATE` + the store's single-connection + `RLock` (as P8-I1) — **no
over-claim** of stronger multi-process semantics.

## 10. Decision outcomes (machine-level only; no UI, no public API)

`allowed`, `denied_not_entitled`, `denied_quota_exhausted`, `denied_invalid_account_or_commercial_state`,
`internal_fail_closed`. **No** quota dashboard / usage bar / plan-usage screen / pricing / upgrade prompt /
"buy more" / subscription page. **No** public API response contract (if a public surface ever becomes
unavoidable → STOP for contract/Owner review).

## 11. Idempotency / retry safety

An optional `idempotency_key` makes a repeated identical logical consumption a **no-op** that returns the prior
decision (a UNIQUE `(account_id, meter, idempotency_key)` record enforces single consumption across HTTP/worker/
client retries and replays). This is a **bounded key table**, **not** a generic payments-idempotency framework
and **not** provider-linked. If a particular bounded proof operation cannot be retried, idempotency may be
omitted for it with a stated reason; the proof seam itself supports the key for the retry-safety RED test.

## 12. Denied / failed / security-failure semantics (never over-consume)

- **Entitlement denial → NO consumption.** **Invalid/missing/disabled/deleted account or commercial state → fail
  closed, NO consumption.** **Quota-exhausted → deny, NO increment** (no "attempt" charge). **Technical
  evaluation failure → NO commercial consumption.** Commercial usage represents **accepted governed
  consumption**, not arbitrary attempts.
- **Security-first:** invalid/revoked credential, failed authorization, security rate-limit rejection, CSRF/auth
  failure must be rejected **before** `consume_quota` is ever reached (caller/web/API layer) and therefore never
  consume commercial quota.
- **Failed-operation semantics:** quota represents **accepted governed consumption**; failed technical
  operations are **not** charged. The neutral proof operation has **no external side effect**, so P8-I2 consumes
  atomically at the governed decision point and **defers cross-resource (operation↔meter) atomicity** to a real
  integration — no distributed-transaction architecture is invented.

## 13. Integer / amount safety; zero; unlimited

Counters are non-negative integers. **Prohibit** negative consumption and negative quota; **validate** the
`amount` as a bounded **positive** integer (default `+1`; a zero/negative amount is rejected as malformed, not a
silent no-op that could mask bugs). `remaining = max(0, limit − used)` avoids negative/overflow. **`0`** is a
valid explicit deny-all policy (distinct from missing → fail closed). **`UNLIMITED`** is a named sentinel
(never a magic integer) that skips the ceiling check while still recording usage. Prefer the smallest model
(unit `+1`); a general positive bounded `amount` is supported and validated (no weighted token metering unless
later justified).

## 14. Anti-lock-in / data-access boundary (HIGH PRIORITY)

**Commercial creation/consumption limits ≠ Owner data access/control rights.** A commercial quota MAY gate the
CREATE/CONSUME of a governed **commercial** operation; it MUST NOT block **reading, exporting, or deleting
already-owned records**, nor any privacy/data-rights operation. **Quota reduction below already-consumed usage**
is fail-safe: `remaining = max(0, limit − used)`, no negative/overflow, **no deletion/truncation/corruption of
existing Owner data**, no counter reset-fraud, no crash — the subject is simply at/over cap and further
**creation** is denied while existing data stays fully accessible/deletable. Final portability/privacy/legal
policy remains Phase-10-owned; P8-I2 must not design a quota system that makes anti-lock-in impossible.

## 15. OD-N — commercial quota must not change technical truth (hard invariant)

Quota state MUST NOT influence scoring, evidence standards, progression, safety, engineering conclusions, or any
deterministic technical evaluation. **Explicitly prohibited:** lower scoring accuracy, weaker evidence
validation, reduced safety checks, inferior deterministic evaluation, or altered thresholds based on quota/plan
state ("no lower quality for free users"). Quota may only decide whether a separately governed **commercial**
operation is permitted. **Guards (both carried forward + strengthened):** (1) the **engine-wide inverted-allowlist
static import guard** extended so `quota_service` joins `plan_catalog`/`entitlement_service` as commercial
modules no `engine/*.py` may import except the seams (`entitlement_service` may import `plan_catalog`;
`quota_service` may import `plan_catalog` + `entitlement_service`); (2) additionally **prohibit commercial
dynamic imports under `engine/`** (a guard rejecting string-based `importlib`/`__import__` of the commercial
modules from core — carrying forward the P8-I1 dynamic-import observation); (3) the **behavioral neutrality**
guard. **Observation carried forward:** technical evaluation is not account-aware, so the **static guard remains
authoritative**; P8-I2 does **not** fabricate an account-aware integration path merely to make the behavioral
test causal, and does **not** make technical evaluation account-aware. If any future account-aware composition
approaches technical evaluation, the behavioral test must be strengthened against the real path.

## 16. Schema / migration (additive; per repository convention)

Additive idempotent `CREATE TABLE IF NOT EXISTS` appended to `SqliteAccountStore._SCHEMA` (applied in the
existing `__init__` `BEGIN IMMEDIATE` loop); **P8-I1 tables are not rewritten**:
- **`commercial_usage`** (canonical counter) — `account_id TEXT NOT NULL, meter TEXT NOT NULL, window_key TEXT
  NOT NULL, used_count INTEGER NOT NULL DEFAULT 0, updated_at TEXT NOT NULL, PRIMARY KEY(account_id, meter,
  window_key), FOREIGN KEY(account_id) REFERENCES accounts(account_id)`.
- **`commercial_usage_idempotency`** (retry safety) — `account_id TEXT NOT NULL, meter TEXT NOT NULL,
  idempotency_key TEXT NOT NULL, consumed_at TEXT NOT NULL, PRIMARY KEY(account_id, meter, idempotency_key),
  FOREIGN KEY(account_id) REFERENCES accounts(account_id)`.
- **Source of truth:** the counter (single canonical enforcement source); the idempotency table is auxiliary and
  transactionally consistent (written in the same transaction) — **no drift, no competing truth source**.
- **Atomic update:** `_write()` (`BEGIN IMMEDIATE`). **Fresh DB:** created. **Existing DB:** added, data
  untouched. **Rollback:** older binary ignores the new tables (no `ALTER TABLE`; no destructive change).
  **Account-status/deletion:** counter/idempotency rows are account-scoped (FK); a deleted account fails closed
  at evaluation regardless of residual rows.
- **Bounded-growth honesty:** the counter is bounded (one row per subject+window); the idempotency table grows
  with distinct consumed operations — **retention/aggregation is a documented boundary owned by Phase-10 / a
  later gate**, not solved here (no premature retention implementation, but the boundary is stated, not hidden).

## 17. True prior-schema migration test (carried-forward P8-I1 observation → stronger convention)

The P8-I2 additive-migration RED/GREEN test MUST use a **genuine prior-schema fixture** (a DB containing only the
pre-P8-I2 tables, built via raw SQL or a faithful equivalent), **not** merely "create with new store → reopen
with same new store", and assert the new tables are added while existing account/commercial-assignment data is
intact.

## 18. Future P8-I2 RED-test matrix (in `tests/test_p8_i2_commercial_quota.py`; genuinely RED on base)

RED on base because `engine/quota_service.py`, the `quota_descriptor` catalog additions, and the
`commercial_usage`/`commercial_usage_idempotency` tables do not exist. Each test asserts a **distinct behavioral
outcome** a correct GREEN must satisfy (discriminating / mutation-probeable), not mere file existence.

| # | Observable behavior | Intended RED reason on base | Expected GREEN | Protected risk |
|---|---|---|---|---|
| 1 | entitled + quota available → `allowed`, consumes exactly once | seam/tables absent | counter +1 once | under/over count |
| 2 | entitled + quota exhausted → `denied_quota_exhausted`, no increment | absent | deny, counter unchanged | fail-open exhaustion |
| 3 | not entitled → `denied_not_entitled`, no consumption | absent | deny before counter | consume-on-denial |
| 4 | missing account/principal → fail closed, no consumption | absent | `denied_invalid…`/error, no write | privilege/consume via ghost |
| 5 | disabled/deleted account → fail closed, no consumption | absent | deny, no write | inactive-account consumption |
| 6 | invalid/malformed assignment or missing/malformed policy → fail closed | absent | deny, no write | silent grant on bad state |
| 7 | security rate-limit counters independent from commercial quota | absent | `record_rate_attempt` unaffected by quota and vice-versa | rate-limit/quota conflation |
| 8 | API scope/credential semantics unchanged & independent | absent | Phase-7 unchanged | scope↔quota collapse |
| 9 | credential revocation remains plan/quota-independent | absent | revoked stays revoked | plan-coupled revocation |
| 10 | repeated identical idempotent consumption does not double-count | absent | same key → single count | retry double-charge |
| 11 | concurrent final-slot consumption cannot oversubscribe hard cap | absent | serialized; exactly `limit` consumed | race oversubscription |
| 12 | invalid/negative/zero `amount` rejected; `+1` and bounded positive validated | absent | malformed rejected; valid consumes | integer/amount abuse |
| 13 | quota policy change requires no per-account snapshot rewrite | absent | catalog change reflected via derivation | stale per-account policy |
| 14 | quota decrease below already-consumed → safe, non-destructive (`remaining=0`, no delete/negative/crash) | absent | fail-safe evaluation | reduction corruption/lock-in |
| 15 | existing Owner data remains readable/deletable when creation quota exhausted | absent | data-access unaffected by quota | data lockout |
| 16 | usage accounting cannot affect scoring/progression/safety/conclusions | absent | technical output invariant | truth coupling |
| 17 | engine-wide commercial isolation (incl. quota_service) enforced; no commercial dynamic import in core | absent | AST + dynamic-import guard pass | commercial leak into core |
| 18 | true prior-schema → P8-I2 additive migration; existing data intact | absent | tables added, data untouched | destructive/false migration |
| 19 | fresh DB initializes commercial usage tables | absent | tables present | init breakage |
| 20 | rollback if consumption counter/idempotency persistence fails | absent | whole consume rolls back atomically | partial/unaudited consumption |
| 21 | failed governed operation does not create incorrect quota accounting (per accepted-consumption semantics) | absent | no charge for a failed op in the proof semantics | phantom consumption |

**Mutation-testability:** the matrix is designed so a reviewer can meaningfully mutation-probe double-consumption
(#1/#10), fail-open exhaustion (#2), rate-limit/quota conflation (#7), concurrent oversubscription (#11),
consume-on-denial (#3), non-atomic usage (#20), and data lockout (#15). Collection-level RED is unavoidable
(new modules absent); discrimination is proven by each test's distinct outcome assertions rather than base
behavior.

## 19. Implementation allowlist (narrowly bounded)

- **REQUIRED:** `engine/quota_service.py` (NEW — `consume_quota`/`evaluate_quota`, `QuotaDecision`, fail-closed);
  `engine/plan_catalog.py` (EXTEND — declarative `quota_descriptor` + meter/`UNLIMITED` constants; no runtime
  mutation/admin CRUD); `engine/account_store.py` (ADDITIVE — `commercial_usage` + `commercial_usage_idempotency`
  tables + atomic `evaluate_and_consume`/`get_usage` methods); `tests/test_p8_i2_commercial_quota.py` (NEW).
- **LIKELY:** extension of the engine-wide OD-N/static + dynamic-import guard (in the P8-I2 test or a sibling).
- **PROHIBITED:** `record_rate_attempt` repurposing or security-limit weakening; API scope changes; credential
  revocation changes; domain activation / metering domain activation; scoring/progression/safety edits; any
  payment/provider code; any subscription lifecycle/proration/period-rollover code; pricing/plan/usage/checkout
  UI; any public web/API surface (if unavoidable → STOP); overage/top-up/rollover; public paid activation;
  Phase 9/10; PSRR; deployment; dependency/CI changes; rewriting P8-I1 tables.

## 20. Owner / business decisions

**None blocks P8-I2** — unmistakably-internal technical quota fixtures (`__quota_proof_meter__`, internal
technical policies) let the architecture be proven without any final commercial value. **Deferred / REQUIRED
LATER (invented by none of this contract):** real quota counts; reset cadence/day/time-zone; public meter
names; plan packaging; overage/top-up/rollover policy; trial/grace allowances; enterprise-unlimited marketed
semantics; billing cadence. No technical fixture may become a public marketed quota.

## 21. Acceptance criteria (for the later P8-I2 implementation candidate)

Based on this accepted contract; genuine RED evidence (§18) before implementation; minimum GREEN; **security
rate limit remains independent**; **entitlement and quota distinct**; **atomic hard-cap consumption**;
**concurrency-safe final-slot** (no oversubscription); **idempotency where applicable**; **no denied/failed
operation consumes**; **no data deletion/lock-out** (existing data readable/deletable when quota exhausted);
**no technical-truth coupling** (behavioral + engine-wide static + dynamic-import guards); **no per-account plan
policy snapshot**; **additive migration proven against a true prior-schema fixture**; **no provider/payment/
lifecycle/proration/UI code**; **no production paid activation**; provider-neutral; credential revocation
plan/quota-independent; API scope unchanged; exact focused/regression/full-suite evidence
(`tests/test_p8_i2_commercial_quota.py` + P8-I1 + account-store/schema + auth/security + P7 API-credential/scope
+ OD-N guards; full suite mandatory, 0 failures); independent review before Owner acceptance; candidate-only
current-truth sync. No criterion false-greenable (RED fails for the intended reason).

## 22. Carried-forward non-blocking observations

(1) true prior-schema migration fixture now REQUIRED (§17); (2) OD-N behavioral test causality limited while the
core is not account-aware → static guard authoritative, do not fabricate a path (§15); (3) engine-wide guard now
also prohibits **commercial dynamic imports** (§15); (4) identifier-leak scan — P8-I2 adds no web/public surface,
so `web/` stays untouched and no new public leak guard is needed (add one only if a public surface is ever
introduced, which would itself require STOP/Owner review); (5) `_CATALOG` mutability — P8-I2 adds no runtime
catalog/quota mutation or admin CRUD path.

## 23. Result

**P8-I2 — Commercial Usage Quotas / Limits: BOUNDED IMPLEMENTATION CONTRACT CANDIDATE.** Defines a provider-
neutral usage-limit foundation — quota subject `(account_id, meter)`; declarative versioned quota policy in the
P8-I1 catalog (derived, no per-account snapshot); a smallest technical window (explicitly not final billing
cadence — P8-I3 owns that); atomic evaluate-and-consume with no oversubscription; optional idempotency; a strong
anti-lock-in data-access boundary; security-rate-limit / API-scope / credential-revocation / domain-activation
separations; OD-N static + dynamic-import + behavioral guards; additive schema with a true prior-schema
migration convention; a 21-test genuinely-RED matrix; a narrow allowlist; §21 acceptance criteria — preserving
all invariants, inventing no commercial values, and adding no UI/public surface/provider/lifecycle code.
**P8-I2 is NOT implemented; this is a contract candidate only.** No implementation begins until this candidate →
independent review → Owner exact-candidate acceptance → merge → post-merge verification → a separate P8-I2
implementation authorization/gate.
