# Phase 8 — Subscription, Billing and Entitlements — P8-C — FORMAL CONTRACT & ACCEPTANCE CRITERIA

**Status of THIS record:** governance/documentation-only **Phase-8 contract CANDIDATE** — authoritative if/when
independently reviewed, Owner-accepted, merged, and post-merge verified. **It confers NO implementation
authority.** It defines scope, boundaries, architecture ownership, sequencing, invariants, acceptance criteria,
exclusions, the bounded implementation-increment decomposition, and the Owner/business decisions required.
Phase 8 remains **CONTRACT CANDIDATE ONLY** — **not** implementation-started, **not** billing-live, **not**
paid-subscriptions-active. No payment provider is selected; no prices are set; no public paid activation is
authorized.

## 1. Authority and verified base (read-only)

- **Authoritative branch/tip (verified live):** `feature/atomic-json-session-persistence` @
  **`053a079b82154d40c6eb5bd9980a8f6204fd8348`** (PR #415 merge of D-P8-PL-01 clarification `178473f`; boot OK;
  working tree clean at authoring).
- **Prerequisite foundations (all FORMALLY CLOSED, verified):** Phase 4 (durable data/persistence), Phase 5
  (accounts/authentication/ownership/authorization), Phase 6 (executed domain-specialization lane), Phase 7
  (internal service seam + versioned public API + machine/API identity).
- **Binding governance consumed:** OD-I, OD-N, OD-O (ODR + phase1 evidence); **D-P8-PL-01** (Phase-8
  privacy/legal entry boundary); OD-P + Phase-10 ownership; **D-PSRR-01** (production block); OD-K
  (core/service/API/adapter separation). **This contract itself confers no implementation authorization** and a
  separate P8-implementation authorization/gate is required before any code.

## 2. Mandatory invariants (binding on every Phase-8 increment)

- **OD-I:** no paid subscription/billing **activation** before durable persistence + account/authorization
  foundations — those are now CLOSED, but OD-I remains binding (no paid plan on non-durable state).
- **OD-N (plan-neutral technical truth):** commercial plan/subscription/tier/price status MUST NOT alter
  technical evaluation, safety gates, evidence requirements, technical conclusions, or invention progression.
  **Paid users never receive "more favorable truth."** Enforced architecturally (§7, §20).
- **OD-O (privacy/data):** commercial data is private-by-default; entitlement decrease MUST NOT silently
  delete user data (§11); retention/deletion remains explicit/authorized and Phase-4/Phase-10-governed.
- **D-P8-PL-01:** Phase-8 entry-level privacy/legal *design* prerequisites are distinct from Phase-10 final
  public legal/release artifacts; **Phase 10 retains ownership** of final Privacy Policy / Terms / payment terms
  / refund policy / consent / production legal-privacy readiness / deployment authorization.
- **Public paid activation is BLOCKED** (D-P8-PL-01 class C / D-PSRR-01 / OD-P) until **all** of: applicable
  Phase-10 legal/readiness satisfied; **PSRR = GO/PASS**; the governing separate Deployment Gate passes; and
  explicit Owner deployment authorization. **Implementing Phase 8 authorizes none of these.**
- **OD-K separation:** commercial concerns live in the service/web layer ABOVE the deterministic core; the core
  engine (scoring/progression/safety/evidence) imports no commercial module.
- **Provider neutrality:** no payment/billing provider (Stripe/PayPal/Paddle/Adyen/Braintree/…) is selected;
  selection is a separate, later, separately-justified gate.

## 3. Critical distinctions (contract-binding; never conflated)

| Distinct A | ≠ | Distinct B |
|---|---|---|
| Security rate limiting (`record_rate_attempt`; abuse throttle; short window) | ≠ | Commercial usage quota (billing-period metered allowance) |
| API scope (Phase-7 `project:read`; capability authorization) | ≠ | Paid entitlement (commercial access level) |
| Commercial plan access to a domain-pack | ≠ | Domain activation authority (Phase-9 / registry support-state) |
| Subscription active | ≠ | Production/deployment authorization |
| Payment success | ≠ | Technical progression / evaluation outcome |
| Enterprise customer | ≠ | Relaxed safety / evidence / technical truth |
| Billing/commercial audit | ≠ | Security monitoring / `access_audit` |

## 4. Architectural ownership (D-FPC-MAP-06 — consume existing seams; add only the genuinely-new bounded abstraction)

**Reused canonical seams (NOT duplicated):** `engine/account_store.py` (durable account identity + additive
schema lifecycle; `api_credentials`, `access_audit`, `record_rate_attempt`); `engine/record_store.py`
(durable project persistence + `owner_account_id` ownership + `load_owner`); central web authorization
`_project_authorized` (`web/app.py`); the Flask-free authorized service seam
`engine/read_export_service.py`; the versioned public API `web/api_v1.py`.

**Genuinely-new bounded abstraction (justified, minimal):** a **Commercial Entitlement seam** — a durable
**plan/subscription state** (additive tables in the existing `SqliteAccountStore` schema lifecycle, no new
store) plus a **Flask-free entitlement-evaluation function** (mirroring the `read_export_service` seam
pattern): `evaluate_entitlement(account_id, capability, context) -> Decision{allow, reason, plan_identity}`,
**fail-closed**. This is NOT a new registry/manager framework — it is one thin evaluation seam + additive
durable state consuming the account foundation. No `BillingService` / `SubscriptionRegistry` /
`EntitlementRegistry` / `QuotaManager` / `CommercialPlanManager` / `UsageMeter` / `PaymentAdapter` /
invoice-subsystem is created by this contract; where such an abstraction is later genuinely required (e.g., a
provider boundary in P8-I4) it is introduced by its own bounded increment, provider-neutral.

## 5. The 25 required contract answers

1. **Canonical commercial-plan model:** a durable, versioned **plan catalog** — a plan is
   `{plan_id, plan_version, entitlement_descriptor}` where the entitlement descriptor is declarative data
   (capability flags + limit values). Plans are data, not code; plan-neutral (OD-N). Plan *names/prices* are
   Owner/business decisions (§8), not set here.
2. **Canonical subscription-state model:** a durable subscription bound to one Phase-5 `account_id`, with a
   deterministic state set — **`free`/none (default)**, **`active`**, **`past_due`** (failed payment),
   **`canceled`**, **`expired`**, **`grandfathered`** — plus `current_plan_id`, `plan_version`, period
   boundaries. State is durable in the account-store schema lifecycle.
3. **Canonical entitlement model:** **HYBRID** — the *authoritative source* is durable subscription-state +
   the plan catalog; the *effective entitlement* is **DERIVED (computed) at evaluation time**, never a stale
   stored copy. (Avoids drift when a plan definition changes; §6.)
4. **How entitlements are evaluated:** through the single Flask-free `evaluate_entitlement` seam (§4),
   fail-closed, consuming durable subscription-state + plan catalog; returns allow/deny + reason + plan
   identity. Callers (web routes / API) enforce the decision; the deterministic core never calls it.
5. **Stored, derived, or hybrid:** **hybrid** — subscription-state + plan catalog stored durably; entitlements
   derived at evaluation time.
6. **Plan change:** update durable subscription `current_plan_id`/`plan_version`; entitlements are recomputed
   on next evaluation (no stored-entitlement migration needed); an immutable commercial-audit event is written.
7. **Downgrade:** access to now-ungranted gated capabilities is reduced **fail-closed** from the effective
   date; **existing user DATA is preserved** (never deleted by downgrade; §11); over-limit existing resources
   are handled by an Owner-decided policy (block-new vs read-only-existing — §8), defaulting to *preserve +
   block-new*.
8. **Cancellation:** subscription → `canceled`; entitlements revert to `free` at period end (or immediately per
   Owner policy); data preserved (§11); commercial-audit event written.
9. **Failed payment:** subscription → `past_due`; a bounded grace policy (Owner-decided) governs whether
   entitlements hold during grace; on grace expiry → `expired`/`free`. No technical-truth effect (OD-N).
10. **Expiry:** subscription → `expired`; entitlements revert to `free` fail-closed; data preserved.
11. **Existing data when entitlement decreases:** **DATA IS PRESERVED** — entitlement/quota decrease reduces
    *access to gated capabilities*, never deletes or corrupts stored projects/evidence (OD-O). Any actual
    deletion/retention is a separate explicit, authorized, Phase-4/Phase-10-governed action — NOT a side effect
    of downgrade.
12. **Quota exceeded:** the gated commercial operation (e.g., create-project-beyond-limit) **fails closed**
    (denied with a clear reason); it **never** alters scoring/evidence/progression of existing work (OD-N).
13. **Fail-closed operations:** all entitlement/quota checks fail closed (deny on error, missing state, or
    ambiguity). Conversely, the **deterministic technical evaluation never fails due to commercial state** —
    commercial denial blocks a *commercial capability*, not the technical truth of already-permitted work.
14. **Grandfathering:** supported by a `grandfathered` subscription state carrying a pinned entitlement
    descriptor; **which** capabilities are grandfathered and **when** is an Owner/business policy decision (§8).
15. **API entitlements vs scopes:** two separate layers — a public-API request must pass **BOTH** the Phase-7
    security **scope** check (`project:read`, machine-credential authz) **AND** the commercial **entitlement**
    check. Scope = security capability; entitlement = commercial access. Neither substitutes for the other.
16. **Usage quotas vs security rate limiting:** **distinct primitives.** `record_rate_attempt` remains a
    security/abuse throttle (short window, fail-closed). A commercial **usage quota** is a billing-period
    metered allowance in its own durable table with its own semantics; it MAY reuse the atomic-counter *pattern*
    but is never conflated with the security limiter and never repurposes the security limiter's data.
17. **Billing-event audit:** a **distinct** durable, append-only **commercial/billing audit** (plan changes,
    subscription transitions, entitlement grants/revocations, quota decisions) — separate from `access_audit`
    (security) and from any future security monitoring. Billing Audit ≠ Security Monitoring.
18. **Durable data:** plan catalog; subscription-state; effective grandfather pins; commercial usage counters;
    commercial audit — all durable via the existing `SqliteAccountStore` schema lifecycle (additive tables; no
    handler-owned DDL/migration).
19. **Commercial data with retention/deletion implications:** subscription history, commercial audit, usage
    records — flagged as carrying retention/deletion obligations coordinated with OD-O + Phase-4 durable-data +
    **Phase-10 legal (retention/deletion policy)**; **retention/deletion policy is NOT solved by this contract.**
20. **Plan-neutral technical truth enforcement:** architectural + tested — the engine scoring/progression/
    safety/evidence modules import **no** commercial module (OD-K); a plan-neutrality guard test asserts
    identical technical outputs across plan levels for identical inputs; entitlement checks live strictly in the
    web/service layer above the core.
21. **Domain-pack commercial entitlement vs domain activation authority:** a plan may grant **commercial
    access** to a domain-pack, but domain **activation authority** stays Phase-9 / registry support-state
    governed. Commercial access never activates a domain and never overrides support-state truth.
22. **Enterprise controls vs core evaluation:** enterprise features (org/team management, admin, SSO if later
    approved) are commercial/service-layer features that **never** relax safety, evidence, or technical truth
    (OD-N); they add access management, not evaluation influence.
23. **Before integrating a real payment provider (P8-I4 prerequisites):** a provider-neutral payment-boundary
    interface; idempotency for money-moving operations; webhook authentication/verification; reconciliation +
    commercial-audit; secrets handling; PCI-scope minimization (no card data in core); and a separate,
    justified **provider-selection gate**. No provider is selected here.
24. **Before public paid activation:** ALL of — applicable **Phase-10** legal/readiness (Privacy Policy, Terms,
    payment terms, refund policy, consent, tax) ; **PSRR = GO/PASS**; the governing **separate Deployment
    Gate**; and **explicit Owner deployment authorization** (D-P8-PL-01 class C / OD-P / D-PSRR-01).
25. **Explicitly deferred to Phase 10:** final public Privacy Policy / Terms / payment terms / refund policy /
    consent/legal notices; production legal/privacy/security review; release readiness; deployment
    authorization; production monitoring/observability/backup-restore. Phase 10 retains ownership.

## 6. Phase-8 implementation decomposition (smallest evidence-supported sequence)

- **P8-I1 — Plan & Entitlement Foundation** *(recommended first increment; NO payment provider / checkout /
  card processing / live charges / invoices / tax)*. Delivers the durable plan catalog + subscription-state
  model + hybrid `evaluate_entitlement` seam + fail-closed governed capability access + commercial audit +
  the plan-neutrality guard. **Proves the core chain: Account → Commercial Plan Identity → Entitlement
  Evaluation → Governed Capability Access — with no external payment processing.**
- **P8-I2 — Commercial Usage Quotas / Limits** — project/storage/evidence-export/collaboration/API-usage
  metered allowances over the entitlement model; distinct from security rate limiting (§16); fail-closed;
  plan-neutral.
- **P8-I3 — Subscription Lifecycle** — deterministic renewal / upgrade / downgrade / cancellation /
  failed-payment(`past_due`) / expiry / grandfathering **mechanics** (business *policy* values are Owner
  decisions, §8), with entitlement recomputation and data-preservation on decrease.
- **P8-I4 — Payment Provider Boundary** — a **provider-neutral** payment-boundary interface + idempotency +
  webhook security + reconciliation; invoices/refunds/taxes attach here. **No provider selected** — provider
  selection is a separate justified gate; this increment is a boundary, not a vendor integration.
- **P8-CLOSE** — a Phase-8 remaining-obligation / exit review after the increments; public paid activation
  still gated behind Phase-10 + PSRR + Deployment Gate + Owner deployment authorization.

Each increment requires its own bounded contract established from this document, a verified live base,
RED-first behavioral tests, GREEN, regression, Lean minimum-path, independent review where required, and
separate Owner authorization. No increment self-activates; labels are conceptual, not standing activation.

## 7. Acceptance criteria

- **Contract publication (P8-C):** governance/documentation-only; answers §5 Q1–Q25; preserves §2 invariants
  and §3 distinctions; provider-neutral; Phase 8 recorded CONTRACT CANDIDATE ONLY; ODR carries no accepted
  implementation authorization; D-FPC-MAP-06 honored (reuse seams; only the one bounded entitlement seam is
  new); independent review.
- **Each implementation increment:** genuine RED-first behavioral tests on the exact base, then GREEN; additive
  schema only in the existing account-store lifecycle (no handler-owned DDL/migration; forward-compatible;
  rollback-safe); every entitlement/quota check **fail-closed**; **plan-neutrality proven** (identical
  technical outputs across plan levels for identical inputs; engine imports no commercial module);
  **downgrade/cancellation/expiry preserve user data** (§11); **quota-exceeded fails closed without altering
  technical truth**; commercial/billing audit written and **distinct** from `access_audit`; API entitlement
  enforced **in addition to** (not replacing) Phase-7 scope; **no regression** to existing free/current
  behavior (full suite green); **no provider lock-in**; **no Phase-10 legal/release leakage**; **no
  PSRR/deployment overclaim**; no public paid activation.
- **Cross-increment:** no criterion false-greenable (no exception-swallowing; RED fails for the intended
  reason); ownership always via the Phase-5 account/`owner_account_id` foundation; commercial state never read
  by the deterministic core.

## 8. Owner / business decisions REQUIRED (not technical; not decided here)

Recorded as **REQUIRED — OWNER/BUSINESS DECISION**, none set by this contract: actual **plan names**; actual
**prices / currency / billing period** (monthly/annual); **trial policy** (offered? length? card-required?);
**free-vs-paid feature packaging** (which capabilities are gated); **enterprise packaging**; **grandfathering
policy** (which capabilities, when); **refund business policy**; **tax handling / jurisdictions**;
**failed-payment grace policy** (grace length, entitlement-during-grace); **over-limit-on-downgrade policy**
(preserve+block-new [default] vs read-only-existing); **whether/when to select a payment provider**. Pricing
architecture/plan-identity semantics are defined (technical); **actual prices are NOT set** (no accepted Owner
pricing decision in the repository).

## 9. Technical decisions taken by this contract (within contract authority)

Plan = versioned catalog data; subscription = durable account-bound deterministic state machine; entitlement =
hybrid (stored state + plan catalog, derived at evaluation); one Flask-free fail-closed `evaluate_entitlement`
seam; additive account-store schema lifecycle (no new store); commercial usage-quota primitive distinct from
security rate-limiting; distinct commercial/billing audit; entitlement enforced in addition to API scope;
plan-neutral core (no commercial import in engine); data preserved on entitlement decrease; provider-neutral
payment boundary deferred to P8-I4.

## 10. Exclusions / boundary (what P8-C does NOT do)

Implements nothing; starts no increment; selects no payment provider; sets no prices; creates no
BillingService/registry/manager/adapter/invoice subsystem; activates no public paid subscription; performs no
Phase-9/Phase-10/PSRR work; authorizes no deployment; pulls no Phase-10 final public legal/release artifact
into Phase 8; alters no OD-I/OD-N/OD-O substance; grants no "more favorable truth" to paid users. **DOCUMENTED
NO-VALID-RED** (governance/documentation-only; future implementation gates must define legitimate behavioral
RED before GREEN).

## 11. Result

**Phase 8 — Subscription, Billing and Entitlements: CONTRACT CANDIDATE (P8-C).** Defines the plan/subscription/
entitlement architecture, the §3 distinctions, the §2 invariants, the §6 increment decomposition (recommended
first increment **P8-I1 — Plan & Entitlement Foundation**, no payment provider), §7 acceptance criteria, and
the §8 Owner/business decisions required. **Phase 8 remains CONTRACT CANDIDATE ONLY — not implementation-
started, not billing-live, not paid-active.** No implementation begins until: this candidate → independent
review → Owner exact-candidate acceptance → merge → post-merge verification → a **separate P8 implementation
authorization/gate**. Public paid activation remains blocked until Phase-10 legal/readiness + PSRR = GO/PASS +
Deployment Gate + explicit Owner deployment authorization.
