# P8-I4-C — Payment Provider Boundary — Bounded Contract & Architecture

**Status of THIS record:** governance/documentation-only **contract candidate** (P8-I4-C), authoritative if/when
independently reviewed, Owner-accepted, merged, and post-merge verified. It **defines** the smallest provider-neutral payment
boundary for **P8-I4 — Payment Provider Boundary**; it **implements nothing**, adds no provider SDK, creates no checkout/webhook
endpoint, and selects no provider. **DOCUMENTED NO-VALID-RED — CONTRACT-ONLY GOVERNANCE GATE.** No runtime/test/Domain-Pack/
schema/prompt/benchmark/web/CI/provider-config file is changed by this gate; Phase 9 is not begun.

**Authoritative base:** `f66ea96c77e64deea8ebc1b4bb9766df985e703e` (PR #425; tree `c676228681a0f74285d8f64645ecbb0e643d5e49`),
verified read-only before editing; boot OK; clean.

**Lineage / authority.** Subordinate to the accepted Phase-8 contract **P8-C** (§6 P8-I4; §5 Q-decisions) and the CLOSED
foundations **P8-I1** (Plan & Entitlement — authority for entitlement), **P8-I2** (Commercial Usage Quotas — authority for
quota), **P8-I3** (Subscription Lifecycle — authority for lifecycle state/events). Reuses the proven **P7-I3** adapter
precedent (`engine/export_adapter.py`: canonical → adapter → vendor; **UNTRUSTED BY DEFAULT**; `adapter_id`/`output_type`/
`source_version`; semantic validation independent of the transform). **D-FPC-MAP-06:** consume/extend existing seams; introduce
only a bounded provider-boundary port + adapter + additive mapping/dedupe persistence — no new store, no second lifecycle/quota/
entitlement authority. **P8-I4 (commercial payment-provider boundary) is DISTINCT from CAP-15 (AI Provider Abstraction)** —
different domains, different future gates (G-MPR-01-D D7); this contract does not touch CAP-15.

---

## 1. Objective (smallest safe provider boundary)

Define the smallest stable, provider-neutral boundary that lets InventorAI, later and under a **separate implementation gate**,
integrate one or more external payment/billing providers **without coupling the core commercial domain to any vendor**. Target
architecture (Integration-Ready Platform principle preserved):

```
InventorAI Core (deterministic engine — no commercial import; OD-N)
   → Commercial / Subscription Domain (P8-I1 entitlement · P8-I2 quota · P8-I3 lifecycle — the AUTHORITIES)
      → Canonical Payment Provider Boundary  (PaymentProviderPort + canonical operations/vocabulary — THIS increment)
         → Provider Adapter                  (translates provider ⇄ canonical; UNTRUSTED BY DEFAULT)
            → External Payment Provider       (NOT selected; NOT integrated here)
```

Adapters translate external reality into **canonical operations**; the core consumes only canonical operations. Adapters are
**never** the business-rule authority.

## 2. Binding invariants carried forward (unchanged)

OD-I (no paid activation before persistence[P4]+accounts[P5] — CLOSED); **OD-N** (deterministic core imports no commercial/
provider module; provider state can never influence technical truth); **OD-O** (data preserved on entitlement decrease);
**OD-K** (core/service/API/adapter separation); **D-P8-PL-01** (entry-level design vs Phase-10 final legal); **D-PSRR-01 /
OD-P** (public paid activation & production blocked until Phase-10 legal/readiness + PSRR = GO/PASS + Deployment Gate + explicit
Owner authorization); **anti-lock-in**; **fail-closed** for every non-authoritative state. **P8-I1/P8-I2/P8-I3 authorities are
NOT replaced or duplicated.**

## 3. Canonical domain vs provider domain (strict separation)

**A. Canonical InventorAI commercial/payment vocabulary** (owned here + by P8-I1/I2/I3): internal `account_id`; internal
commercial/lifecycle identity; canonical lifecycle events (P8-I3: `subscription_started`, `trial_started`, `trial_converted`,
`trial_ended`, `subscription_renewed`, `subscription_change_scheduled`, `subscription_changed`, `cancellation_requested`,
`subscription_cancelled`, `subscription_expired`, `payment_status_changed`); canonical states (`trialing`/`active`/`past_due`/
`canceled`/`expired` + implicit `none`); canonical payment-boundary operations (§5).

**B. Provider-specific external vocabulary** (owned only by an adapter): SDK objects, payloads, signatures, provider status
names, customer/price/product/subscription/invoice IDs, provider event names, provider retry rules, provider error types.

**Rule.** No item of (B) may leak into the core commercial domain. A provider adapter is the **only** place (B) exists; it
maps (B) → (A). **A raw provider event name must NEVER become a lifecycle state/event directly** — it must be mapped to a
canonical P8-I3 operation, preserving the accepted distinctions (esp. `cancellation_requested` [request] vs
`subscription_cancelled` [effective] vs `subscription_change_scheduled` [scheduled PLAN change]).

## 4. Canonical identities (opaque; no coupling)

Distinct, non-conflated identities; every external reference is an **opaque string** to core logic and **never** becomes the
internal primary identity:
- `account_id` — internal durable account key (Phase-5). Primary identity.
- internal commercial/lifecycle identity — P8-I1 assignment + P8-I3 lifecycle (internal).
- `provider` — a provider-neutral key/slug naming an adapter (e.g. an internal registry key), NOT a vendor SDK handle.
- `external_customer_ref` — opaque provider customer reference.
- `external_subscription_ref` — opaque provider subscription reference.
- `external_transaction_ref` / `external_payment_ref` — opaque provider payment reference.
- `provider_event_id` — opaque provider event reference (dedupe key; §7).
- internal `idempotency_key` — canonical-operation idempotency identity (§7).

## 5. PaymentProviderPort — the smallest stable interface (contractual, NOT implemented)

A minimal, reversible port between core and adapter. **Names are indicative; the P8-I4 implementation derives the exact
minimal surface from repository need and must not add methods that encode a future product/business decision.** Candidate
operations (a superset — implement only what a fake/reference adapter + the accepted canonical operations require):
- `create_customer_context(account_id, ...) -> external_customer_ref` (opaque).
- `create_checkout_session(account_id, plan_identity, ...) -> opaque session handle` (hosted/tokenized; no card data on-platform, §13).
- `retrieve_subscription(external_subscription_ref) -> canonical subscription snapshot`.
- `cancel_subscription(external_subscription_ref, ...) -> canonical result` (maps to `cancellation_requested`/`subscription_cancelled` per §8).
- `create_billing_portal_session(...) -> opaque handle` (RESERVED; only if evidence requires — otherwise deferred).
- `verify_and_parse_provider_event(raw, secret_context) -> parsed provider event | reject` (authenticity + parse; §9).
- `map_provider_event_to_canonical_operation(parsed) -> canonical operation | reject` (§8).
The port returns **canonical** results/operations; provider SDK objects never cross it. The core invokes canonical operations
only. **Minimality + reversibility are acceptance criteria.**

## 6. Provider-boundary decomposition (derived from evidence; smallest safe path)

Preferred incremental decomposition (mirrors the P7-I3 reference-adapter-first precedent; **B — fake/reference adapter first**):
- **P8-I4-I1 — Provider-neutral port + fake/reference adapter + mapping/dedupe persistence** (NO real vendor, NO real
  network, NO real secrets). Proves the port, canonical mapping, opacity, additive persistence, idempotency, fail-closed, and
  replaceability with an in-memory fake adapter.
- **P8-I4-I2 (evidence-triggered) — Verified webhook/external-event ingestion seam** (transport/auth + signature verification
  isolated in the adapter). Async/webhook remains **evidence-triggered / separately gated** per Phase-7 §25 + P8-C — NOT
  authorized by this contract.
- **P8-I4-I3 (evidence-triggered) — Reconciliation seam** (uncertain-outcome resolution; §12).
- **Real-provider selection/integration sub-gate** — requires a **separate Owner/provider-selection decision** (§10) BEFORE
  any real adapter work.
- **P8-I4-CLOSE** — Payment-provider-boundary exit review.
Each sub-increment requires its own bounded contract, RED-first tests, GREEN, independent review, and separate Owner
authorization. **Nothing self-activates.**

## 7. Idempotency / replay (HIGH PRIORITY — stricter than the P8-I3 replay default)

Carries forward and **resolves** the P8-I3 non-blocking observation (idempotency-key replay returned the prior outcome without
payload-equality validation). For **provider events**, the boundary MUST distinguish:
- **provider event identity** — `(provider, provider_event_id)` (durable dedupe key).
- **canonical operation idempotency identity** — the internal `idempotency_key` passed to the P8-I3 seam (derived from the
  provider event so retries are safe).
- **duplicate delivery** — same `(provider, provider_event_id)` re-delivered → **idempotent no-op** returning the prior
  canonical outcome (no second mutation).
- **conflicting duplicate payload** — same `(provider, provider_event_id)` but a **materially different** parsed content →
  **FAIL CLOSED** (integrity error; do NOT silently return the prior outcome; do NOT mutate). *(This is the stricter decision;
  provider-event integrity requires it — the weaker P8-I3 replay semantic is NOT inherited for provider events.)*
- **retry after timeout** — idempotent via the durable dedupe/idempotency identity (an uncertain send is retried safely, §12).
- **replay after process restart** — the dedupe record is **durable** (survives restart); no in-memory-only dedupe.
A durable `(provider, provider_event_id)` uniqueness constraint is the enforcement authority.

## 8. Canonical event mapping (P8-I3 remains authoritative)

Adapters map provider events to **canonical P8-I3 lifecycle operations**, invoked through the accepted P8-I3 seam
(`subscription_lifecycle_service.apply_event` / `materialize_due`) — adapters do **not** mutate lifecycle/quota/assignment
tables directly. Examples (indicative, not exhaustive):
- provider "invoice/payment failed" → canonical `payment_status_changed(status=failed)` (→ `past_due`).
- provider "payment recovered" → canonical `payment_status_changed(status=recovered)` (→ `active`).
- provider "subscription canceled (effective now)" → canonical `subscription_cancelled` (effective).
- provider "cancel at period end" → canonical `cancellation_requested` (with future `effective_at`); later `subscription_cancelled`
  via authorized materialization.
- provider "plan change scheduled" → canonical `subscription_change_scheduled` (PLAN change, NOT cancellation).
- provider "subscription expired/ended" → canonical `subscription_expired`.
An **ambiguous or unmappable** provider event **fails closed** (§11); an invalid resulting lifecycle transition is **rejected
by the P8-I3 authority** (unchanged). Provider event names never become canonical events directly.

## 9. Event authenticity & secrets boundary (conceptual; NOT implemented)

- Provider events MUST pass provider **authenticity/signature verification** (adapter-isolated) **before** any canonical
  mutation. The contract defines the boundary; it selects **no** algorithm and **no** provider and implements **no**
  verification. The P8-I4 implementation exposes a testable adapter boundary keeping provider-specific verification isolated.
- **Secrets boundary (hard):** provider secrets/credentials MUST NOT be stored in `accounts`, lifecycle/event tables,
  `commercial_assignments`, quota tables, user-owned data, Domain Packs, or source-controlled configuration. The implementation
  may define a config/secrets **abstraction**; **production secret management/verification belongs to later PSRR/Phase-10/
  release readiness** and is NOT implemented here. **No card/payment credentials and no raw provider payloads are persisted by
  default** (§10).

## 10. Provider mapping persistence (additive; contractual)

The P8-I4 implementation will require additive durable tables (appended as `CREATE TABLE IF NOT EXISTS` in the existing
`SqliteAccountStore` lifecycle; **no `ALTER TABLE`, no destructive migration, no back-fill**; existing P8-I1/P8-I2/P8-I3 tables
untouched; existing DBs reopen cleanly):
- **provider mapping** — account-scoped; provider-neutral `provider` key; opaque `external_customer_ref` /
  `external_subscription_ref`; uniquely constrained where appropriate (e.g. one active mapping per (account, provider); a
  unique `(provider, external_subscription_ref)`); durable; replay-safe.
- **provider-event dedupe** — durable `(provider, provider_event_id)` UNIQUE; records the canonical-operation outcome +
  enough integrity material (e.g. a content hash) to detect a **conflicting duplicate payload** (§7); survives restart.
**No full provider payloads by default; no secrets; no card details.** Any content retained for integrity is a bounded
hash/reference, not the raw payload.

## 11. Fail-closed behavior (no silent acceptance)

Fail closed for at least: unknown provider; malformed external reference; invalid/failed event authenticity; unsupported/
unknown provider event type; missing account↔provider mapping; disabled/deleted account (§ account boundary); conflicting
duplicate provider event (§7); invalid lifecycle transition (P8-I3 rejects); stale provider event (P8-I3 in-txn stale guard);
provider adapter exception; ambiguous mapping. None reaches canonical mutation.

## 12. Provider outage / timeout / reconciliation (technical, not commercial policy)

- A provider **timeout/outage MUST NOT silently mutate canonical state**.
- Retries MUST be **idempotent** (via §7 identities).
- **Uncertain external outcomes require reconciliation, not guessing** — a reserved future reconciliation seam (P8-I4-I3,
  evidence-triggered) resolves them; not implemented here.
- The core MUST **distinguish a provider failure** (retry/reconcile) **from a canonical business rejection** (a legitimate
  fail-closed decision). No commercial policy is invented.

## 13. Atomicity

Provider-event ingestion that both dedupes and mutates canonical state MUST coordinate — in **one transaction boundary where
the repository SQLite model supports it** — the **provider-event dedupe record**, the **canonical lifecycle mutation** (via the
P8-I3 store primitive), and any **provider-mapping update**, so no provider event is half-applied. The implementation decides
the exact mechanism (e.g. composing within one `BEGIN IMMEDIATE`); it is **not implemented here**.

## 14. Replaceability (acceptance property — binding)

Switching from a Provider-A adapter to a Provider-B adapter MUST NOT require changing: the **P8-I1 entitlement engine**, the
**P8-I2 quota engine**, the **P8-I3 lifecycle engine**, **Domain Packs**, the **deterministic evaluation engine**, or the
**public canonical data model**. Only the adapter / configuration / provider-mapping layers may change (except where a
separately-accepted migration contract is required). A **fake second provider adapter must be able to satisfy the same
`PaymentProviderPort`.**

## 15. Security / PCI boundary (architectural avoidance; NO compliance claim)

InventorAI SHOULD NOT receive/store raw payment-card credentials where a **hosted / provider-tokenized checkout** flow can keep
them off-platform. **This contract makes NO PCI-compliance claim.** Actual PCI/legal/security certification belongs to later
PSRR / Phase-10 / release gates. The system is **NOT** marked PCI compliant.

## 16. Public API / UI boundary

P8-I4 focuses on the **backend provider abstraction**. It does **NOT** implement pricing pages, checkout UI, billing-portal
UI, subscription-management UI, invoices, or receipts. No provider-specific field is exposed to public UI/API unless a
separate gate explicitly accepts a minimal boundary.

## 17. Future implementation RED matrix (documented; NOT implemented here)

For the future P8-I4-I1 (fake/reference adapter) implementation, genuine RED-first → GREEN, at minimum:
1. `PaymentProviderPort` interface exists. 2. no provider SDK required for core tests. 3. an in-memory fake adapter satisfies
the port. 4. external identifiers remain opaque to core. 5. account↔provider mapping durable. 6. unknown provider fails
closed. 7. unmapped customer/subscription fails closed. 8. duplicate provider event idempotent (no second mutation).
9. **conflicting duplicate payload fails closed** (§7 strict decision). 10. adapter exception does not mutate core. 11. provider
timeout does not mutate core. 12. invalid/failed authenticity rejected **before** canonical mutation. 13. unsupported provider
event rejected. 14. canonical-mapping-only (provider vocabulary never reaches core). 15. raw provider event name never becomes
a lifecycle event directly. 16. a valid canonical mapping reaches the P8-I3 seam and applies. 17. an invalid lifecycle
transition remains rejected by P8-I3. 18. quota (P8-I2) unchanged / not reset. 19. entitlement (P8-I1) authority unchanged.
20. disabled/deleted account fails closed. 21. provider-event dedupe survives restart (durable). 22. provider-event record +
lifecycle mutation atomic where required. 23. cross-account mapping isolation. 24. no provider secret persisted. 25. no card/
payment credential persisted. 26. no raw provider payload persisted unless explicitly allowed. 27. no provider import leaks
into the core domain. 28. provider swap requires adapter/config change, not core rewrite. 29. a fake SECOND provider satisfies
the same port. 30. **OD-N / import-boundary guards remain strong** (the engine-wide inverted-allowlist guard extends to a
payment-provider seam allowlist; the deterministic core still imports no commercial/provider module).

## 18. Owner / business decisions — MUST REMAIN OPEN (not decided here)

Recorded **OPEN — REQUIRED OWNER/BUSINESS(/TECHNICAL) DECISION** (subordinate to P8-C §8 + P8-I3-C §9; not duplicated):
**payment-provider selection** (no provider chosen); marketed plan names; prices; currency; billing cadence; trial policy;
grace period; proration; refunds; tax treatment / supported jurisdictions; cancellation effective timing; grandfathering;
enterprise billing; over-limit-downgrade policy; invoice requirements; payment methods; dunning behavior. **Technical
provider-boundary decisions (this contract) are separated from commercial policy.** **Dependency registered truthfully:** real
(non-fake) adapter work is BLOCKED until a **separate Owner provider-selection decision** is accepted.

## 19. Exclusions / non-goals (what P8-I4 / this contract does NOT do)

No provider SDK; no real provider integration; no provider selection; no checkout implementation; no webhook endpoints; no
webhook signature-verification implementation; no invoices/refunds/tax/receipts implementation; no pricing/checkout/portal/
subscription UI; no reconciliation worker; no public paid activation; no Phase-9/10 work; no PSRR; no deployment; no PCI-
compliance claim. This contract **implements nothing** and selects no provider.

## 20. Acceptance / closure criteria (P8-I4-C contract)

Governance/documentation-only; provider-neutral; adapter boundary defined (§1/§5); canonical vs provider separation (§3);
canonical opaque identities (§4); additive mapping/dedupe persistence rule (§10); event-authenticity + secrets boundary
(§9); **strict provider-event idempotency incl. conflicting-payload fail-closed (§7)**; atomicity requirement (§13); lifecycle
mapping authority preserved (§8, P8-I3 authoritative); fail-closed catalogue (§11); outage/reconciliation rules (§12);
replaceability acceptance property (§14); PCI architectural-avoidance without a compliance claim (§15); RED matrix complete
(§17); Owner/business decisions (incl. provider selection) preserved OPEN (§18); D-FPC-MAP-06 (one port + adapter + additive
tables; no duplicate authority); Phase-8 order preserved; **no implementation authorization conferred** — a separate
Owner-authorized P8-I4 implementation gate is required. The contract self-activates nothing.

## 21. Result

**P8-I4 — Payment Provider Boundary is DEFINED by a governance-only CONTRACT CANDIDATE (P8-I4-C)** — provider-neutral,
adapter-bounded, additive, deterministic, auditable, replaceable, fail-closed, with no provider selected. **P8-I4 remains NOT
STARTED / NOT IMPLEMENTED / NOT AUTHORIZED** until this contract is independently reviewed, Owner-accepted, merged, post-merge
verified, **and** a separate Owner-authorized P8-I4 implementation gate (starting with the fake/reference-adapter P8-I4-I1) is
granted; real-provider work additionally requires a separate Owner provider-selection decision. Phase 8 remains OPEN; P8-CLOSE
NOT STARTED; Phase 9 / Phase 10 NOT AUTHORIZED; PSRR EXECUTION NOT STARTED; public paid activation / production BLOCKED / NOT
AUTHORIZED.
