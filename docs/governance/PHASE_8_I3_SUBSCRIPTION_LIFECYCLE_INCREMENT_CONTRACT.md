# P8-I3-C — Subscription Lifecycle — Bounded Implementation Contract (CORRECTED — verdict-B remediation)

**Status of THIS record:** governance/documentation-only **contract candidate** (P8-I3-C, CORRECTED), authoritative if/when
independently reviewed, Owner-accepted, merged, and post-merge verified. It **defines** the smallest safe technical contract
for **P8-I3 — Subscription Lifecycle**; it **implements nothing**. **DOCUMENTED NO-VALID-RED — CONTRACT-CORRECTION-ONLY GATE.**
No runtime/test/Domain-Pack/schema/prompt/benchmark file is changed by this gate; no payment provider is selected; P8-I4 /
Phase 9 / Phase 10 / PSRR / deployment are not begun.

**Supersession (review history preserved).** This CORRECTED candidate **supersedes the prior candidate
`ead186d88747a33ff04d69768041efdcb51615bb`**, which received independent review verdict **B — ACCEPT WITH REQUIRED PRE-MERGE
CORRECTIONS** and is therefore **INVALIDATED / NOT MERGEABLE / EVIDENCE-ONLY / NOT MERGED**. The prior candidate is preserved
as a git object + delivered bundle (evidence); it is not deleted and is not pretended away. This record applies the required
corrections **RC-1** (`none` entitlement-neutral), **RC-2** (canonical `past_due` exit events), **RC-3** (unique
cancellation-request event mapping), and the two recommended clarifications (due-scheduled-transition materialization;
equal-`effective_at` tie-break), and preserves every property that independently passed review.

**Authoritative base:** `0a19daf74c344f2f497ccebac2440dd1f9d42b2d` (PR #422; tree `843e2ee854e4514724c7c9fbaf7c5dbe83f43bd1`),
verified read-only before editing; boot OK; clean.

**Lineage / authority.** Derived from and subordinate to the accepted Phase-8 contract **P8-C**
(`PHASE_8_SUBSCRIPTION_BILLING_ENTITLEMENTS_P8C_CONTRACT.md`, §6 P8-I3), the closed foundations **P8-I1** (Plan &
Entitlement — `engine/plan_catalog.py`, `engine/entitlement_service.py`, `commercial_assignments`/`commercial_audit`) and
**P8-I2** (Commercial Usage Quotas — `engine/quota_service.py`, `commercial_usage`/`commercial_usage_idempotency`), the
Phase-5 account/ownership foundation (`engine/account_store.py`, `ACCOUNT_STATUSES = {active, disabled, deleted}`), and the
binding **G-MPR-01-D D2** persistence rule. **D-FPC-MAP-06:** consume/extend the existing seams; introduce only the one
bounded lifecycle seam + additive tables — no new store, registry, or parallel identity system.

---

## 1. Objective (smallest safe increment)

Establish the **deterministic, account-scoped, provider-neutral subscription-lifecycle state model and its persistence /
service boundaries** — the mechanics of subscription-start / renewal / upgrade / downgrade / cancellation (requested vs
effective) / failed-payment / expiry / scheduled transitions — needed **before** P8-I4 (Payment Provider Boundary), with
entitlement recomputation and **data preservation on decrease**. It proves the chain **Account → Assigned Plan Identity
(P8-I1) → Lifecycle State (P8-I3) → Derived Effective Entitlement → Governed Capability Access / Quota (P8-I2)** with **no
external payment processing**. Business *policy values* are Owner decisions (§9) and are NOT decided here.

## 2. Binding invariants carried forward (unchanged)

OD-I (no paid activation before persistence[P4]+accounts[P5] — both CLOSED); **OD-N** (commercial/lifecycle state MUST NEVER
alter deterministic technical evaluation, safety gates, evidence requirements, scoring, or progression — engine imports no
commercial module); **OD-O** (data preserved on entitlement decrease; never silently deleted); **OD-K** (core/service/API/
adapter separation); **D-P8-PL-01** (entry-level design vs Phase-10 final legal); **D-PSRR-01 / OD-P** (public paid
activation & production blocked until Phase-10 legal/readiness + PSRR=GO/PASS + Deployment Gate + explicit Owner
authorization); **anti-lock-in** (existing-data read/export/delete never blocked by commercial state). **Fail-closed** for
every non-authoritative state.

## 3. Concepts kept strictly distinct (MUST NOT be conflated)

1. **Lifecycle state** — the subscription's technical status (this increment).
2. **Assigned plan** — the plan identity in P8-I1 `commercial_assignments` (plan_id, plan_version).
3. **Effective entitlement** — DERIVED at evaluation from **(lifecycle state + assigned plan identity)** via the P8-I1
   `evaluate_entitlement` seam; never stored as a snapshot.
4. **Quota allowance** — P8-I2 derived quota policy + counters; P8-I2 remains the sole quota authority.
A lifecycle transition may change (1) without changing (2); (3) and (4) are recomputed deterministically, never rewritten.

## 4. Lifecycle state machine (bounded; TECHNICAL state, not business policy)

**Canonical technical states (finite, minimal — 5 stored + 1 implicit):**
- `none` *(implicit — no lifecycle row exists)* — the **pre-P8-I3 / legacy** condition. **ENTITLEMENT-NEUTRAL (RC-1):** it
  changes nothing — effective entitlement is exactly the existing P8-I1 resolution (assigned plan if a valid commercial
  assignment exists, else `default_plan_identity()`). It is **NOT** forced to the free/default plan. See §6.
- `trialing` — technical trial state (trial *availability/duration* = Owner policy §9).
- `active` — subscription current; entitled per assigned plan.
- `past_due` — failed-payment / delinquent technical state (grace *length/behavior* = Owner policy §9).
- `canceled` — **terminal**; cancellation became **effective**; lifecycle ended by cancellation.
- `expired` — **terminal**; term ended without renewal / otherwise ended.

**Derived projections (NOT stored states; computed from the event log + injectable clock):**
- `cancellation_pending` — true when a `cancellation_requested` event has recorded a future `effective_at` not yet reached and
  not yet materialized (the requested↔effective distinction; current stored state stays `active`/`trialing` until the
  cancellation is materialized as `subscription_cancelled`).
- `entitlement_active` — whether the current lifecycle state grants the assigned plan's entitlement (see §6).

**Allowed transitions** (each driven by exactly ONE canonical event from §8; each idempotent; each appended to the event log):
| From | To | Canonical event | Note |
|---|---|---|---|
| `none` | `trialing` \| `active` | `subscription_started` (+`trial_started` if trial) | first lifecycle epoch |
| `trialing` | `active` | `trial_converted` | trial→paid conversion |
| `trialing` | `expired` | `trial_ended` | no conversion |
| `trialing`\|`active` | (scheduled **plan change**) | `subscription_change_scheduled` | future-effective **PLAN change ONLY — NOT cancellation** (RC-3) |
| (scheduled plan change) | applied | `subscription_changed` | materialized at `effective_at` (§5) |
| `trialing`\|`active` | (cancellation pending) | `cancellation_requested` | records the cancellation **request** + optional future `effective_at`; stored state unchanged until effective (RC-3) |
| `trialing`\|`active`\|(cancellation pending)\|`past_due` | `canceled` | `subscription_cancelled` | the **effective** cancellation transition (immediate, or materialized at the requested `effective_at`) (RC-2/RC-3) |
| `active` | `active` | `subscription_renewed` | renewal; may bump plan_version / period |
| `active` | `past_due` | `payment_status_changed` (status=failed) | delinquent |
| `past_due` | `active` | `payment_status_changed` (status=recovered) | recovery |
| `past_due` | `expired` | `subscription_expired` | grace/term exhausted — the *grace-exhausted* condition is a **reason/provenance field on the event, not an event name** (RC-2) |
| `active` | `expired` | `subscription_expired` | term end, no renewal |
| `canceled`\|`expired` | `trialing` \| `active` | `subscription_started` (new epoch) | reactivation/resubscribe, if supported |

**Upgrade/downgrade** = a change of the P8-I1 assigned plan identity (`set_commercial_assignment`) **coordinated in the same
transaction** with a lifecycle event (`subscription_changed` immediate, or `subscription_change_scheduled` at period end —
timing = policy §9). Plan change and lifecycle transition are orthogonal but atomically coordinated. `subscription_change_scheduled`
is **reserved for scheduled PLAN changes and MUST NOT alias a cancellation request** (RC-3).

**Invalid transitions (fail closed, no mutation):** any transition not in the table above (e.g. `canceled`→`past_due`,
`expired`→`past_due`, `none`→`canceled`); any state reached by an event other than its single canonical event; any transition
from/into an unknown or malformed state; any event with an unrecognized `event_type`; any transition on a
missing/disabled/deleted account.

**Event semantics:** monotonic append-only ordering by a **durable event sequence** (`event_id`); **idempotent** by
`(account_id, idempotency_key)` (replay returns the prior recorded outcome, no re-apply); **duplicate event** = no-op returning
the same result; **out-of-order event** — ordering is by the durable sequence with an explicit `effective_at`; an event whose
`effective_at` precedes the current derived state or contradicts the allowed-transition table is **rejected fail-closed**
(never silently reorders history); **equal-`effective_at` tie-break (Clarification 2):** two otherwise-valid events sharing an
identical `effective_at` are ordered **deterministically by the durable event sequence (`event_id`)** — never ambiguously;
**future-effective** transitions are stored and only change the derived current state when the injectable clock reaches
`effective_at` (deterministic; no wall-clock in the engine — clock injected, mirroring P8-I2 `_window_key`). **State explosion
avoided:** requested-cancellation and scheduled plan changes are represented as events + one scheduled transition, not as extra
stored states.

## 5. Persistence (additive; append-only event log + derived current state)

**Strategy (binding, per G-MPR-01-D D2):** two NEW additive tables appended to `SqliteAccountStore._SCHEMA` as
`CREATE TABLE IF NOT EXISTS` (idempotent, applied under the existing `BEGIN IMMEDIATE` construction path). **No `ALTER TABLE`;
no destructive migration; no implicit rewrite; existing DBs remain readable; existing `commercial_assignments`,
`commercial_usage`, `commercial_usage_idempotency`, `commercial_audit`, `accounts`, `api_credentials`, `access_audit` tables
are NOT altered; no back-fill.** Rollback/recovery reasoning is required in the implementation increment.

- **`subscription_lifecycle_events`** *(append-only; the SOURCE OF TRUTH and the lifecycle audit)* — at least:
  `event_id` (PK, monotonic durable sequence — also the tie-break authority), `account_id` (FK→accounts), `event_type`
  (canonical, validated), `from_state`, `to_state`, `effective_at`, `recorded_at`, `reason` (nullable policy/provenance,
  e.g. `grace_exhausted` — NOT an event name), `source` (provenance slug), `external_reference` (nullable opaque — NO provider
  payload), `idempotency_key`, with **UNIQUE (account_id, idempotency_key)**.
- **`subscription_lifecycle_state`** *(derived current-state cache; one row per account)* — at least: `account_id` (PK,
  FK→accounts), `current_state`, `current_since`, `scheduled_to_state` (nullable), `scheduled_effective_at` (nullable),
  `updated_at`. **The current-state row MUST be a deterministic function of the event log** (reconstructable/replayable); the
  event log is authoritative, the state row is a read-efficient derivation.

**Due-scheduled-transition materialization (Clarification 1 — binding).** A future-effective transition (scheduled plan change
via `subscription_change_scheduled`, or pending cancellation via `cancellation_requested`) becomes durable ONLY when an
**authorized lifecycle-processing operation** materializes it — at/after `effective_at` it MUST append the corresponding
canonical event (`subscription_changed` / `subscription_cancelled`) **and** update the derived state in **one `BEGIN IMMEDIATE`
transaction**. **A read/projection operation MUST NOT silently write:** it MAY *project* a due transition for display (report
that the effective time has passed) but MUST NOT mutate the event log or the derived-state row; it may not leave the append-only
event log behind the projected current state. **The event log remains the single source of truth; the derived state and the
event log MUST be equivalent after any materialization.** Read/projection and authorized materialization are explicitly
separate operations. (Any future scheduler/provider-driven execution of materialization is out of scope for this contract and
deferred; P8-I3 requires only that materialization is an authorized, durable, atomic lifecycle operation — not a read-time side
effect.)

**Transactional rules:** event append + derived-state update (+ any coordinated plan-assignment change / materialization) occur
in **one `BEGIN IMMEDIATE` critical section** (RLock-guarded, as today) — no partial/unaudited mutation; safe concurrent
updates; read-after-write consistency; deterministic current-state derivation; restart/reopen durability. **No silent loss of
lifecycle history** (append-only; corrections are new events, never edits/deletes).

## 6. Entitlement interaction (with P8-I1) — RC-1 corrected

Effective entitlement is **DERIVED**: `effective_entitlement = f(lifecycle_state, assigned_plan_identity)` through the P8-I1
`evaluate_entitlement` seam (no stored entitlement snapshot; no `if plan==`/`if state==` business branching in the engine).

- **`none` (legacy / pre-P8-I3) → ENTITLEMENT-NEUTRAL (RC-1).** Lifecycle `none` **changes nothing**: the existing P8-I1
  entitlement resolution is preserved **exactly** — **if a valid commercial assignment exists, the assigned plan is used; if
  none exists, the existing `default_plan_identity()` fallback is used.** Lifecycle `none` is **NEVER** forced to the
  free/default plan; it never reassigns, downgrades, or rewrites a pre-existing assignment. **This is a TECHNICAL
  BACKWARD-COMPATIBILITY RULE — NOT COMMERCIAL POLICY.**
- **`active`** → entitled per assigned plan.
- **`trialing`** → entitled per assigned plan during trial (trial gating specifics = policy §9).
- **`past_due`** → **TECHNICAL SAFETY DEFAULT: entitlement RETAINED (fail-safe, non-destructive) until an explicit effective
  transition** — silent mid-flight revocation is riskier; actual grace length / during-grace entitlement are Owner policy §9.
- **`canceled` / `expired` (TERMINAL only)** → **MAY project to the default technical entitlement**, subject to the
  anti-lock-in / data-rights rules below. Only these terminal states project to default; `none` does not.
- **A lifecycle state change may occur without a plan-assignment change** (e.g. `active`↔`past_due` keeps the same assigned
  plan).
- **Anti-lock-in (binding):** in **every** lifecycle state, **read / export / delete of already-owned data MUST remain
  available**. Lifecycle state may gate only **new mutation/creation** capabilities — never existing-data access. Entitlement
  is projected deterministically from lifecycle + plan.

## 7. Quota interaction (with P8-I2) — boundary, not rewrite

- **P8-I2 remains the sole authority** for quota counters, idempotency, and windows (`commercial_usage`,
  `commercial_usage_idempotency`). **P8-I3 does NOT read, write, reshape, or reset these tables.**
- Lifecycle may determine **whether quota consumption is permitted**, but only through the existing composition:
  `quota_service` evaluates **entitlement FIRST** (already), and entitlement now factors lifecycle (§6); a non-entitled
  lifecycle state therefore denies consumption via the existing entitlement-first path — **no new quota coupling, no new
  quota code in P8-I3.**
- **Lifecycle transitions MUST NOT silently reset quota.** Any reset semantics remain **explicitly governed** and are **NOT
  introduced here.**
- **Plan change + quota:** changing the assigned plan changes the P8-I2 **derived** quota policy (P8-I2 derives policy from
  plan identity) but **does NOT reset the counter** (counters stay keyed by `(account, meter, window)`) — deterministic and
  auditable.

## 8. Provider-neutral lifecycle-event boundary (for later P8-I4)

Canonical, vendor-neutral event vocabulary (exactly one canonical event per semantic; **no aliasing** — RC-3):
`subscription_started`, `trial_started`, `trial_converted`, `trial_ended`, `subscription_renewed`,
`subscription_change_scheduled` *(scheduled PLAN change ONLY)*, `subscription_changed`, `cancellation_requested` *(the single
canonical cancellation-request event; may carry a future `effective_at`)*, `subscription_cancelled` *(the effective cancellation
transition)*, `subscription_expired` *(the canonical `past_due`/`active`→`expired` exit; grace-exhaustion is a `reason` field)*,
`payment_status_changed`. Events carry an optional opaque `external_reference` and a `source`/`reason` provenance **without**
persisting any provider payload and **without** binding an event name to a vendor. **P8-I4 owns the real provider→canonical
mapping, webhook security, signature verification, and reconciliation.** No provider SDK/credentials/payloads in P8-I3.

## 9. Owner / business decisions — MUST REMAIN OWNER-OWNED (not decided here)

Recorded **REQUIRED — OWNER/BUSINESS DECISION** (subordinate to and not duplicating P8-C §8): marketed **plan names**;
**price / currency / billing cadence**; **trial** availability / duration / card-required; **grace period** length &
during-grace entitlement; **cancellation timing** (immediate vs period-end); **proration** policy; **downgrade / upgrade
effective timing**; **grandfathering**; **refunds**; **tax / jurisdiction**; **enterprise packaging**; **over-limit-on-
downgrade** behavior; **whether/when to select a payment provider**. The technical model supports each **without** deciding it.

**Technical safety / backward-compatibility defaults (NOT commercial policy; each justified as non-destructive / no-lockout):**
- **TCR-0** *(TECHNICAL BACKWARD-COMPATIBILITY RULE — RC-1)* absent lifecycle row = `none` = **existing P8-I1 entitlement
  preserved unchanged** (assigned plan if assigned, else default). **No silent downgrade / reassignment / rewrite of legacy
  accounts.**
- **TSD-2** `past_due` retains entitlement until an explicit effective transition (silent revocation riskier).
- **TSD-3** cancellation defaults to the requested/scheduled effective representation (period-end-style); the model also
  supports immediate; actual timing = Owner policy.
- **TSD-4** over-limit-on-downgrade = **preserve existing data + block new** (P8-C default; OD-O).
- **TSD-5** terminal `canceled`/`expired` project to default entitlement but **never** block existing-data read/export/delete.

## 10. Account-state interaction

`missing` / `disabled` / `deleted` account → **fail closed** (deny lifecycle read & mutation), consistent with
`evaluate_entitlement` (a missing account is never defaulted). A **re-enabled** account (disabled→active) retains its durable
lifecycle state (re-derived on read). All operations are **account-scoped** via the Phase-5 `owner_account_id` foundation; no
cross-account lifecycle references; **no parallel identity system**.

## 11. Service boundary (implementation-time; NOT created in this gate)

One Flask-free, fail-closed commercial seam **`engine/subscription_lifecycle_service.py`** (to be created by the P8-I3
implementation gate), e.g. `apply_lifecycle_event(...)`, `materialize_due_transitions(...)` *(authorized materialization;
Clarification 1)*, `get_lifecycle_state(...)` *(read/projection; never mutates)*, `project_effective_entitlement(...)`,
composing `engine.entitlement_service` and `engine.account_store`; no Flask, no network, no provider. **OD-N/OD-K:** the
deterministic engine imports no commercial module; the lifecycle seam is a commercial module (like `quota_service`). The
engine-wide inverted-allowlist static import guard in `tests/test_p8_i1_plan_entitlement_foundation.py` MUST be **extended to
allowlist `subscription_lifecycle_service`** as an authorized seam (a bounded, declared cross-increment test amendment — see
RED matrix R00/R29).

## 12. Security / integrity requirements

Account authorization enforced at callers/boundaries; **fail-closed** canonical state/event parsing (reject arbitrary external
strings — strict canonical validation); **replay protection** + **idempotency**; **safe concurrency** (`BEGIN IMMEDIATE`);
**auditability** (append-only event log; distinct from `access_audit` and `commercial_audit`); **no privilege escalation** by
lifecycle mutation; **no lifecycle mutation through read/export/projection endpoints** (Clarification 1); **no cross-account**
lifecycle references; **no provider payload persistence**; **no secrets / provider credentials** in P8-I3.

## 13. Future implementation RED matrix (documented here; NOT implemented in this gate)

Genuine RED-first on the exact base, then GREEN, for the P8-I3 implementation increment:
1. **R00** missing lifecycle subsystem — `ImportError`/absent tables on base (also: OD-N guard extended to the seam).
2. additive schema migration from an existing P8-I1/P8-I2 DB (new tables created; old untouched).
3. migration **idempotency** (re-open existing DB → no error, no rewrite).
4. existing account/entitlement/quota/durable records **preserved** after migration.
5. create initial lifecycle state (`none`→`active`/`trialing`).
6. valid transition applied + derived state updated.
7. **invalid transition denied** (fail closed, no mutation).
8. **duplicate event idempotent** (same idempotency_key → no re-apply).
9. **replay returns same result**.
10. **out-of-order / stale-`effective_at` event** handled fail-closed.
11. malformed/unknown state or event_type **fail closed**.
12. **missing account** denied.
13. **disabled account** denied.
14. **deleted account** denied.
15. **cross-account mutation denied**.
16. **concurrent same-event race** (one applies, others idempotent; no oversubscription).
17. **concurrent different-event race** (serialized deterministically).
18. **scheduled future transition** stored; applies only at/after `effective_at` (injectable clock).
19. **cancellation requested vs effective** distinction — `cancellation_requested` records the request (state unchanged);
    `subscription_cancelled` is the effective transition; `cancellation_pending` projection true only until materialized (RC-3).
20. **renewal** (`active`→`active`, plan_version/period bump; no data change).
21. **plan-change (upgrade/downgrade) interaction** — coordinated assignment + lifecycle in one transaction;
    `subscription_change_scheduled` drives a PLAN change and **does not** alias cancellation (RC-3).
22. **entitlement projection** deterministic from lifecycle + plan — **`none` preserves the existing assigned-plan
    entitlement; `none` falls back to `default_plan_identity()` ONLY if no assignment exists; terminal `canceled`/`expired`
    project to default** (RC-1).
23. **quota not silently reset** on any transition / plan change.
24. **read/export/delete NOT locked out** in any lifecycle state (anti-lock-in).
25. **external reference vendor-neutral** (opaque; no provider payload persisted).
26. **audit/history preserved** (append-only; corrections are new events).
27. **restart/reopen durability** (state reconstructable from the event log).
28. **rollback/recovery scenario** (interrupted write leaves consistent state; forced-failure rolls back both event + derived
    row + any coordinated assignment/materialization).
29. **no provider dependency** (no import of any vendor; OD-N static + dynamic-import guards hold; seam allowlisted only).
30. **regression / no silent legacy downgrade (RC-1)** against P8-I1/P8-I2 — **a legacy/pre-P8-I3 account with lifecycle
    `none` and an existing non-default commercial assignment retains EXACTLY its existing P8-I1 entitlement** (its assigned
    plan), and a `none` account with no assignment keeps the default; no silent downgrade, no implicit reassignment, no data
    rewrite; full suite green; entitlement + quota behavior unchanged for `none`/legacy accounts.
- **R31** derived current-state == event-log replay (equivalence test), **including after a due-scheduled-transition is
  materialized** (event log and current state remain equivalent — Clarification 1).
- **R32** plan-neutrality preserved (identical deterministic technical evaluation across lifecycle states — OD-N behavioral guard).
- **R33** injectable-clock determinism (no wall-clock in the engine, mirroring P8-I2 `_window_key`).
- **R34** canonical `past_due` exits (RC-2): `past_due`→`expired` is driven by `subscription_expired`; `past_due`→`canceled`
  by `subscription_cancelled`; no free-form/pseudo-event drives a transition; grace-exhaustion is a `reason` field only.
- **R35** equal-`effective_at` tie-break (Clarification 2): two valid events with identical `effective_at` are ordered
  deterministically by the durable event sequence (`event_id`) — no ambiguous ordering.
- **R36** due-scheduled-transition materialization (Clarification 1): a due transition is materialized only by an authorized
  lifecycle-processing operation (durable canonical event + derived-state update in one `BEGIN IMMEDIATE`); a read/projection
  observing a due transition **does not** write; the event log never falls behind the projected current state.

## 14. Acceptance criteria (P8-I3-C contract)

Governance/documentation-only; provider-neutral; additive-persistence rule (§5) honored; states/transitions bounded & explicit
with **exactly one canonical event per transition** (§4/§8; RC-2/RC-3); **`none` entitlement-neutral / no legacy downgrade**
(§6; RC-1); due-scheduled-transition materialization vs read/projection separated (§5/§11; Clarification 1); equal-`effective_at`
tie-break deterministic (§4; Clarification 2); technical state separated from business policy (§9); entitlement (§6) / quota
(§7) / account-state (§10) boundaries defined without conflation; anti-lock-in & OD-N/OD-O preserved; RED matrix complete
(§13); Owner business decisions preserved unresolved (§9); security/integrity defined (§12); D-FPC-MAP-06 (one new seam +
additive tables, no duplicate framework); Phase-8 order preserved; **no implementation authorization conferred** — a separate
Owner-authorized **P8-I3 implementation gate** is required. The contract self-activates nothing.

## 15. Exclusions / boundary (what P8-I3 / this contract does NOT do)

Payment-provider SDK / webhooks / signature verification / checkout / card / payment-method storage; invoices; tax; refunds;
receipts; pricing UI; plan-marketing UI; public paid activation; Phase-9 domains / Domain-Neutrality implementation;
Cross-Domain implementation; QTA; Output-Language implementation; ACV; PDF; Email; PSRR execution; deployment; any
scheduler/background execution of due transitions (deferred — §5). **P8-I4** owns the real provider boundary. This contract
**implements nothing**, selects no provider, sets no prices, starts no increment.

## 16. Result

**P8-I3 — Subscription Lifecycle is DEFINED by a governance-only CORRECTED CONTRACT CANDIDATE (P8-I3-C)** — provider-neutral,
additive, backward-compatible, deterministic, auditable, account-scoped; superseding the verdict-B candidate `ead186d`
(evidence-only, NOT merged). **P8-I3 remains NOT STARTED / NOT IMPLEMENTED / NOT AUTHORIZED** until this contract is
independently re-reviewed, Owner-accepted, merged, post-merge verified, **and** a separate Owner-authorized P8-I3
implementation gate is granted. Phase 8 remains OPEN; P8-I4 / P8-CLOSE NOT STARTED; Phase 9 / Phase 10 NOT AUTHORIZED; PSRR
EXECUTION NOT STARTED; public paid activation / production BLOCKED / NOT AUTHORIZED.
