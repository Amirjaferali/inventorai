# P8-I2 — Commercial Usage Quotas / Limits — FORMAL CLOSURE RECORD

**Status of THIS record:** governance/documentation-only **closure candidate** — authoritative if/when
independently reviewed, Owner-accepted, and merged. It records an **increment closure only** within Phase 8
(Subscription, Billing and Entitlements). It does **not** close Phase 8, does **not** start P8-I3/P8-I4, does
**not** enable public paid activation, and registers/executes no PSRR. **DOCUMENTED NO-VALID-RED** (governance/
documentation-only closure after an already-tested merged implementation).

## 1. Gate identity & closure verdict

- **Gate:** P8-I2 — Commercial Usage Quotas / Limits — Formal Closure / Current-Truth Sync.
- **Verdict:** **P8-I2 — FORMALLY CLOSED / AUTHORITATIVE** (increment closure only; authoritative if/when this
  governance candidate is merged).

## 2. Identity & lineage (verified live, read-only at the merged tip)

- **Accepted bounded contract:** P8-I2-C (`docs/governance/PHASE_8_I2_COMMERCIAL_USAGE_QUOTAS_INCREMENT_CONTRACT.md`)
  — merged **PR #419** (`d3e950cb5b34ee7fc0dd8522264fc412252236d3`).
- **Implementation review history:** initial implementation candidate `1490548324e72bb6667b1594d3831ef077f1125d`
  (tree `e8d79d0b8fc88f2f50a0d8f047a8c83965f690ed`) received **independent review verdict B — ACCEPT WITH
  REQUIRED PRE-MERGE CORRECTIONS** (material fail-open `evaluate_quota` at exhaustion). It is **INVALIDATED /
  SUPERSEDED / EVIDENCE-ONLY / NOT MERGED**.
- **Corrected (accepted) implementation candidate:** **`6f269acb2ebda129d220d0387693a659db48bd1a`** (parent
  `d3e950c`; tree **`65d1a660b61f975d5d9614452aeefc97f300212e`**) — the fail-open defect corrected (R1),
  docstring corrected (R2), plus two adjacent cleanups; **independent re-review verdict A**; Owner
  exact-candidate acceptance; SHA-preserving bundle publication.
- **Merge:** **PR #420** — merge **`e3c65afcee1127d3dd75e4860ccb9480f7223f16`** (parent 1
  `d3e950cb5b34ee7fc0dd8522264fc412252236d3`; parent 2 `6f269acb2ebda129d220d0387693a659db48bd1a`; **merged
  tree `65d1a660b61f975d5d9614452aeefc97f300212e` == accepted candidate tree → post-merge verified**).
- **Changed implementation paths (exactly 8):** `engine/quota_service.py` (NEW) + `engine/plan_catalog.py`
  (additive quota policy) + `engine/account_store.py` (additive `commercial_usage`/`commercial_usage_idempotency`
  + atomic method) + `tests/test_p8_i2_commercial_quota.py` (NEW) + `tests/test_p8_i1_plan_entitlement_foundation.py`
  (engine-wide OD-N guard extended to the quota seam) + the three current-truth docs
  (`ACTIVE_INCREMENT_CONTRACT.md`, `CURRENT_PROJECT_STATE.md`, `ACTIVE_EXECUTION_ROADMAP.md`). **Diffstat: 8
  files changed, 897 insertions(+), 8 deletions(-).**

## 3. RED → GREEN evidence

- **Initial RED:** the P8-I2 test module was RED on the accepted base (`ImportError: cannot import name
  'quota_service' from 'engine'`).
- **Corrected-candidate RED-first (R1 defect):** two discriminating tests
  (`test_evaluate_quota_denies_when_finite_limit_reached`, `test_evaluate_quota_denies_zero_limit_from_start`)
  **FAILED against the invalid implementation** (the read-only `evaluate_quota` returned `allowed=True` for an
  exhausted / explicit zero-limit quota) and **PASSED after the R1 fix**; a third pins UNLIMITED unchanged.
- **GREEN (pre-merge):** P8-I2 focused **32 passed**; directly-impacted regressions **141 passed**; full suite
  **2123 passed / 3 skipped / 1 xfailed / 0 failed** (same-environment base 2091 + 32; no regression).

## 4. Post-merge evidence (reproduced at `e3c65af`)

- **Post-merge focused:** `PYTHONPATH=. pytest tests/test_p8_i2_commercial_quota.py -q` → **32 passed / 0 failed**.
- **Post-merge full suite:** `PYTHONPATH=. pytest -q` → **2123 passed / 3 skipped / 1 xfailed / 0 failed**.

## 5. Process-deviation record (truthful; not hidden)

**PR #420 was merged BEFORE the planned Pre-Merge Safety Check was executed — a process deviation.** The
pre-merge safety check did **not** occur; this record does **not** claim it did. The deviation was **mitigated
by an expanded post-merge identity verification** proving: exact merge **parent 1** `d3e950c`; the exact
accepted candidate as **parent 2** `6f269ac`; **merged tree `65d1a66` == accepted candidate tree**; exactly the
**8 changed paths**; the exact **diffstat** (897/−8); a clean diff-check; **post-merge focused tests green (32)**;
and **post-merge full suite green (2123/0 failed)**. The deviation is a **process** matter, **not** a code
defect. Recorded proportionately; history is not rewritten.

## 6. Non-blocking observations (preserved; NOT fixed here)

1. **`iot_electronics` domain-pack skipped-warning** — the full suite emits a recurring independent
   domain-registry warning: `domains/iot_electronics/domain.json` is skipped because `schema_version=None`
   (expected `'1.0'`). **NOT a P8-I2 closure blocker; NOT fixed in this gate.** **Preserved for the forthcoming
   G-MPR-01 Domain Pack Inventory & Activation Audit.**
2. **Prior P8-I1 closure-record status** — P8-I1 was closed via current-truth/roadmap synchronization **without
   a dedicated formal closure record** (unlike P7-I*/S5-I*). Recorded as a formal-closure-record ambiguity to be
   dispositioned by **G-MPR-01**; not remediated here.
3. **Neutral internal proof surface** — P8-I2 proves the architecture through an internal proof meter only; no
   repository-authorized user-facing capability may yet be quota-restricted (reported at implementation).

## 7. Delivered capabilities (P8-I2 delivered ONLY these)

Provider-neutral commercial **quota foundation**; **account-oriented** quota subject `(account_id, meter)`;
**entitlement/quota separation** (entitlement first, then quota; distinct seams); **security-rate-limit /
quota separation** (`record_rate_attempt` untouched; a paid customer is still security-rate-limited);
**atomic hard-cap consumption** (one `BEGIN IMMEDIATE`; concurrent final-slot cannot oversubscribe);
**idempotent retry**; **same-key/different-amount explicit conflict** (no second consumption); **quota policy
derived from the versioned declarative plan catalog** (no per-account snapshot); **bounded technical quota
windows** (lifetime / fixed-seconds via an injectable clock — explicitly NOT final billing cadence); **true
prior-schema additive migration** (idempotent `CREATE TABLE IF NOT EXISTS`; P8-I1 tables not rewritten);
**anti-lock-in / existing-data access preservation** (quota exhaustion never blocks read/export/delete of
already-owned data); **OD-N technical-truth isolation** (behavioral + engine-wide static + commercial
dynamic-import guards); **no public quota surface; no real paywall.** Credential revocation stays
plan/quota-independent; API scope unchanged; domain activation unchanged.

## 8. Explicit exclusions (P8-I2 did NOT deliver)

Payment-provider integration; checkout; cards; charges; invoices; refunds; tax; payment webhooks; billing
reconciliation; subscription lifecycle; renewal; downgrade; cancellation; failed-payment handling; proration;
grandfathering; trial implementation; overage; top-ups; rollover; public pricing; pricing UI; usage dashboard;
subscription UI; **public paid activation**. These remain **outside P8-I2**.

## 9. Remaining Phase-8 obligations (still open)

- **P8-I3 — Subscription Lifecycle** — NOT STARTED (renewal / upgrade / downgrade / cancellation /
  failed-payment / expiry / grandfathering mechanics; lifecycle-state schema-evolution choice; period
  boundaries).
- **P8-I4 — Payment Provider Boundary** — NOT STARTED (provider-neutral boundary; idempotency; webhook
  security; invoices/refunds/taxes attach here; no provider selected).
- **P8-CLOSE** — NOT STARTED (Phase-8 exit review; public paid activation still gated behind Phase-10 legal/
  readiness + PSRR = GO/PASS + Deployment Gate + explicit Owner deployment authorization).

## 10. Mandatory next gate & P8-I3 status

**NEXT GOVERNANCE GATE AFTER P8-I2 CLOSURE: `G-MPR-01` — Master Phase & Roadmap Completeness Review (read-only)
— MANDATORY / NOT YET EXECUTED.** Execution **STOPS before P8-I3**: **P8-I3 is NOT STARTED** and remains pending
until G-MPR-01 is completed and any resulting Owner-approved roadmap changes are resolved. G-MPR-01 is
**registered only** here (not executed); it will later cover, among other items: all phases / sub-phases /
gates; phase ordering; dependencies; missing / duplicated / misplaced work; orphan obligations; deferred
capabilities; a production-readiness reverse review; a **Domain Pack Inventory & Activation Audit**; Mechanical
Engineering expansion; Cross-Domain / Multi-Disciplinary Engineering Integration; future-engineering-domain
extensibility; the recurring `iot_electronics` skipped-pack warning; the prior P8-I1 closure-record ambiguity;
and final classification of findings as **KEEP / CLARIFY / MOVE / MERGE / ADD**.

## 11. Boundary — what this closure does NOT do

- **Phase 8 is NOT closed** — NOT complete; NOT billing-live; NOT paid-active.
- **P8-I3 / P8-I4 / P8-CLOSE — NOT STARTED.** **G-MPR-01 — NOT EXECUTED** (registered as mandatory next gate).
- **Public paid activation: BLOCKED / NOT ENABLED.** **Payment provider: NOT INTEGRATED.** **Production: NOT
  AUTHORIZED.** **PSRR: separately governed; not executed here.**
- **`OWNER_DECISION_REGISTER.md`: UNCHANGED** — this increment closure registers no new durable Owner decision
  (consistent with the P7-I*/increment-closure precedent of leaving ODR unchanged for routine closure).

## 12. Result

**P8-I2 — Commercial Usage Quotas / Limits: CONTRACT ESTABLISHED (PR #419) / IMPLEMENTED (RED→GREEN) /
INDEPENDENTLY REVIEWED (initial B → corrected candidate re-reviewed A) / OWNER-ACCEPTED / MERGED (PR #420,
`e3c65af`) / POST-MERGE VERIFIED / FORMALLY ACCEPTED AND CLOSED** (increment closure only; authoritative if/when
this governance candidate is merged). There is no active implementation increment. **Next-eligible: `G-MPR-01`
(mandatory, read-only) — NOT STARTED. P8-I3 NOT STARTED. Phase 8 remains OPEN.**
