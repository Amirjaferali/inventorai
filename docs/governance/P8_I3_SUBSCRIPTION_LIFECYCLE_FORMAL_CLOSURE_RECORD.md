# P8-I3 — Subscription Lifecycle — FORMAL CLOSURE RECORD

**Status of THIS record:** governance/documentation-only **closure candidate** — authoritative if/when independently
reviewed, Owner-accepted, and merged. It records an **increment closure only** within Phase 8 (Subscription, Billing and
Entitlements). It does **not** close Phase 8, does **not** start P8-I4, does **not** select a payment provider, does **not**
enable public paid activation, and registers/executes no PSRR. **DOCUMENTED NO-VALID-RED — GOVERNANCE-ONLY FORMAL CLOSURE
GATE** (no runtime behavior is created here; the P8-I3 RED→GREEN occurred at implementation time and is cited, not re-run).

## 1. Gate identity & closure verdict

- **Gate:** P8-I3 — Subscription Lifecycle — Formal Closure / Current-Truth Synchronization.
- **Verdict:** **P8-I3 — FORMALLY CLOSED / AUTHORITATIVE** (increment closure only; authoritative if/when this governance
  candidate is merged).

## 2. Identity & lineage (verified live, read-only at the merged tip)

- **Accepted bounded contract:** P8-I3-C (CORRECTED — verdict-B remediation)
  (`docs/governance/PHASE_8_I3_SUBSCRIPTION_LIFECYCLE_INCREMENT_CONTRACT.md`) — corrected contract candidate
  `a9ddcce73c9fbb8c3fbddaac4ad5cf2883581378`, merged **PR #423** (`09743b91b764e5ac2956401d7a88c91df48d3d8b`). The prior
  verdict-B contract candidate `ead186d88747a33ff04d69768041efdcb51615bb` remains SUPERSEDED / INVALIDATED FOR MERGE /
  EVIDENCE-ONLY / NOT MERGED.
- **Implementation review history:** initial implementation candidate `4385a33cdcec692fcee233c3f02abbfa13b4b828` received
  **independent review verdict B — ACCEPT WITH REQUIRED PRE-MERGE CORRECTIONS** (six defects: scheduling-race /
  in-txn-stale / conflict-guard-coverage / event-log-target-plan / materialization-key-collision / read-fail-open). It is
  **INVALIDATED / SUPERSEDED / EVIDENCE-ONLY / NOT MERGED** and must not be rewritten as accepted history.
- **Corrected (accepted) implementation candidate:** **`8e600c0674bfeb7be96fd6875b68de1da02eae2f`** (parent
  `09743b91b764e5ac2956401d7a88c91df48d3d8b`; tree **`3d1586e4076f3b2cbd3fe6e1ff1b7f9799085f7a`**) — the six defects
  corrected (RC-I1…RC-I6), each **independently re-reviewed verdict A — ACCEPT**; Owner exact-candidate acceptance;
  SHA-preserving bundle publication.
- **Merge:** **PR #424** — merge **`cef9a522dfae53493ceb1b47bd9faf409617e13e`** (parent 1
  `09743b91b764e5ac2956401d7a88c91df48d3d8b`; parent 2 `8e600c0674bfeb7be96fd6875b68de1da02eae2f`; **merged tree
  `3d1586e4076f3b2cbd3fe6e1ff1b7f9799085f7a` == accepted candidate tree → post-merge verified**). Create-a-merge-commit
  lineage; **Pre-Merge Safety Check: PASS**; **Post-Merge Verification: PASS**.
- **Changed implementation paths (exactly 8):** `engine/subscription_lifecycle_service.py` (NEW seam) +
  `engine/account_store.py` (additive lifecycle tables/methods) + `tests/test_p8_i3_subscription_lifecycle.py` (NEW, 45
  tests) + `tests/test_p8_i1_plan_entitlement_foundation.py` + `tests/test_p8_i2_commercial_quota.py` (the contract-declared
  OD-N engine-wide guard extension allowlisting the lifecycle seam) + the three current-truth docs
  (`ACTIVE_INCREMENT_CONTRACT.md`, `CURRENT_PROJECT_STATE.md`, `ACTIVE_EXECUTION_ROADMAP.md`). **Diffstat: 8 files changed,
  1416 insertions(+), 10 deletions(-); `git diff --check` clean.**

## 3. RED → GREEN evidence (historical; cited, not re-run)

- **Corrected-candidate behavioral RED (not ImportError):** new tests reproduced the six independently-confirmed defects on
  the prior implementation — a stale `effective_at` was durably appended (no in-txn check); the scheduled target plan was
  absent from the event log; the `materialize:<effective_at>` key collided across epochs; lifecycle reads returned
  `none`/data for missing/disabled accounts; the scheduling-race and conflict-guard gaps were demonstrated deterministically
  by the mutation probes. They **PASSED after the RC-I1…RC-I6 fixes**.
- **GREEN:** **P8-I3 focused 45 passed**; directly-impacted Phase-8 regressions **94 passed**; **full suite 2168 passed /
  3 skipped / 1 xfailed / 0 failed** (2123 P8-I2 baseline + 45 new P8-I3 tests; no regression).
- **Concurrency determinism:** the two-thread race tests (scheduling exclusivity; cancel-vs-expire different-transition)
  passed across repeated runs. **Six correction mutation probes** each turned a targeted test RED and were fully restored
  (files byte-identical; no mutation remains).

## 4. Post-merge evidence (verified at `cef9a52`)

- Merge lineage verified: parents `09743b9` + `8e600c0`; merged tree `3d1586e` == accepted candidate tree.
- Diffstat 8 files / 1416 insertions / 10 deletions; `git diff --check` clean; exactly the 8 accepted changed paths; prior
  invalid candidate `4385a33` confirmed **absent from official ancestry**.

## 5. Delivered capabilities (P8-I3 delivered ONLY these)

A deterministic, account-scoped, **provider-neutral** subscription-lifecycle foundation: a bounded 5-state machine
(`trialing`/`active`/`past_due`/`canceled`/`expired`) + implicit `none` (legacy/default, no back-fill); canonical
provider-neutral events (exactly one per semantic; RC-3 unique cancellation mapping; RC-2 canonical `past_due` exits); an
additive **append-only event log = source of truth** (carrying the scheduled target plan, RC-I4) + a derived current-state
cache reconstructable from the log alone; **one-`BEGIN IMMEDIATE`** atomicity with rollback, with **in-transaction**
stale-`effective_at` (RC-I2) + pending-schedule exclusivity (RC-I1) + optimistic from-state (RC-I3) guards; durable
account-scoped idempotency/replay; equal-`effective_at` `event_id` tie-break; an injected clock; read/projection that never
writes vs authorized durable materialization (materialization idempotency bound to the scheduling `event_id`, RC-I5);
derived effective entitlement via the P8-I1 seam (**RC-1 `none` entitlement-neutral — no silent legacy downgrade**; terminal
→ default; `past_due` retains — technical safety default); **P8-I2 remains the sole quota authority** (never read/written/
reset by P8-I3); **anti-lock-in** (existing-data read/export/delete never blocked); §10 **lifecycle read/mutation fail-closed**
for missing/disabled/deleted accounts (RC-I6); OD-N preserved (engine core imports no commercial module; guard extended to
the seam). No payment processing; `external_reference` opaque; no provider payload/secrets.

## 6. Explicit exclusions (P8-I3 did NOT deliver)

Payment-provider integration/selection; checkout; cards; charges; invoices; refunds; tax; payment webhooks; webhook
signature verification; billing reconciliation; pricing; pricing/subscription/checkout UI; public subscriptions activation;
scheduler/background execution of due transitions; **public paid activation**. These remain outside P8-I3 (P8-I4 owns the
real provider boundary).

## 7. Non-blocking observations (preserved; NOT reopening P8-I3)

1. **Idempotency-key replay payload semantics** — lifecycle idempotency replay returns the prior recorded outcome without
   payload-equality validation. It is account-scoped, no conflicting replay write occurs, and it is **accepted as
   non-blocking under P8-I3** (the accepted contract permits prior-result replay). It is documented in `find_lifecycle_event`
   and is **explicitly carried to P8-I4** for provider-event-mapping review.
2. **RC-I3 conflict-guard verification** — the from-state guard is independently verified correct and product behavior
   passed; a direct deterministic store-level stale-expected-state test may be useful future coverage. **Do not reopen P8-I3**
   unless repository precedent requires it.
3. **Prior invalid implementation candidate** `4385a33cdcec692fcee233c3f02abbfa13b4b828` remains **EVIDENCE-ONLY** and must
   not be rewritten as accepted history.
4. **`iot_electronics` skipped-pack warning** — the recurring domain-registry warning is unchanged and preserved for the
   G-MPR-01 Domain Pack Inventory & Activation Audit (not a P8-I3 concern).

## 8. Boundary — what this closure does NOT do

- **Phase 8 is NOT closed** — NOT complete; NOT billing-live; NOT paid-active.
- **P8-I4 / P8-CLOSE — NOT STARTED.** **Phase 9 / Phase 10 — NOT AUTHORIZED.** **PSRR EXECUTION — NOT STARTED.**
  **Production — NOT AUTHORIZED.** **Public paid activation — BLOCKED** until applicable Phase-10 legal/readiness +
  PSRR = GO/PASS + governing separate Deployment Gate + explicit Owner deployment authorization.
- No payment provider selected; no checkout / webhook / pricing / refund / tax decision made.
- **`OWNER_DECISION_REGISTER.md`: UNCHANGED** — this increment closure registers no new durable Owner decision, consistent
  with the P8-I1 / P8-I2 increment-closure precedent (purely evidentiary closure leaves the ODR unchanged; the P8-I3-C
  contract's still-open Owner/business decisions remain recorded under the earlier P8-I3-C register entry).

## 9. Mandatory next gate & P8-I4 status

**NEXT PHASE-8 GATE AFTER P8-I3 CLOSURE: `P8-I4` — Payment Provider Boundary — NOT STARTED.** It is a provider-neutral
payment-boundary interface + idempotency + webhook security + reconciliation (invoices/refunds/taxes attach there); **no
provider is selected** — provider selection is a separate justified gate. It is **registered as the next Phase-8 gate only**
here (not started, not authorized to begin by this closure). P8-CLOSE (Phase-8 exit review) remains after the increments,
with public paid activation still gated behind Phase-10 + PSRR + Deployment Gate + explicit Owner authorization.

## 10. Result

**P8-I3 — Subscription Lifecycle: CONTRACT ESTABLISHED (corrected P8-I3-C, PR #423) / IMPLEMENTED (RED→GREEN) /
INDEPENDENTLY REVIEWED (initial B → corrected candidate re-reviewed A) / OWNER-ACCEPTED / MERGED (PR #424, `cef9a52`) /
POST-MERGE VERIFIED / FORMALLY ACCEPTED AND CLOSED** (increment closure only; authoritative if/when this governance candidate
is merged). There is no active implementation increment. **Next-eligible: `P8-I4` — Payment Provider Boundary — NOT STARTED.
Phase 8 remains OPEN.**
