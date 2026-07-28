# Phase 1 — Owner Decisions OD-I and OD-N — Commercial Sequencing and Non-Interference

**Phase:** Phase 1 — Owner Product Decisions
(of `docs/governance/PRODUCT_FOUNDATION_AND_COMMERCIAL_READINESS_REMEDIATION_PLAN.md`).
**Decision IDs:** OD-I (persistence before paid subscription) and OD-N (commercial
plan non-interference) — recorded together because both are Phase 8 commercial
boundary rules: one gates *when* commerce may activate, the other bounds *what*
commerce may influence.
**Scope:** documentation-only durable record of two linked accepted owner
decisions. **No persistence, payment, subscription, billing, pricing, plan,
quota, entitlement, invoice, checkout, payment-provider, or plan-enforcement
implementation; no change to scoring/safety/evidence/progression/technical
conclusions; no runtime/UI/schema/API change. No downstream activation.**
**Authoritative branch:** `feature/atomic-json-session-persistence`.
**Verified official base at authoring:** `74144aee46fc929d42ecc85bc975064cb6537dcd`
(official tip after PR #298, which merged the corrected OD-J/OD-O increment).

---

## 1. Decision status

```
OD-I — OWNER DECISION ACCEPTED
OD-N — OWNER DECISION ACCEPTED
```

Both are forward-looking confirmation decisions consistent with current behavior;
neither authorizes any commercial or technical change. No other open owner
decision is resolved, and no downstream phase is activated.

## 2. Accepted owner decisions (verbatim)

### OD-I — Persistence Before Paid Subscription

> **OD-I — OWNER DECISION ACCEPTED**
>
> PAID SUBSCRIPTION, BILLING, OR COMMERCIAL ACCESS TIERS MUST NOT BE ACTIVATED
> UNTIL THE DURABLE DATA AND EVIDENCE FOUNDATION IS FORMALLY COMPLETED,
> INDEPENDENTLY REVIEWED, OWNER-ACCEPTED, MERGED, AND CLOSED.

Required meaning:
- No paid plan may rely on temporary, in-memory, or non-production storage.
- No billing or subscription capability may be activated before Phase 4 is
  formally closed.
- Durable project, evidence, transcript, provenance, contribution, and
  ownership-claims storage must exist first.
- Required privacy, retention, deletion, audit, migration, recovery, and
  access-control foundations must be established before paid commercial use.
- Phase 5 account and authorization prerequisites must also be formally satisfied
  before paid activation.
- A prototype or demo may remain non-commercial under its current limitations.
- Pricing documentation, commercial concepts, or UI mockups do not authorize
  billing.
- No payment, subscription, billing, entitlement, quota, invoice, checkout,
  payment-provider integration, plan enforcement, or commercial activation is
  authorized now.

### OD-N — Commercial Plan Non-Interference

> **OD-N — OWNER DECISION ACCEPTED**
>
> SUBSCRIPTION PLAN, PRICE, BILLING STATUS, COMMERCIAL TIER, OR CUSTOMER VALUE
> MUST NOT ALTER THE PRODUCT'S TECHNICAL EVALUATION, SAFETY GATES, EVIDENCE
> REQUIREMENTS, TECHNICAL CONCLUSIONS, OR INVENTION-PROGRESSION DECISIONS.

Required meaning:
- Technical evaluation must remain plan-neutral.
- Safety gates must remain plan-neutral.
- Evidence thresholds and completeness requirements must remain plan-neutral.
- Technical uncertainty must not be hidden, reduced, reclassified, or omitted
  because of plan level.
- Paid users must not receive weaker safety gates, fabricated confidence, or more
  favorable technical conclusions.
- Free users must not receive intentionally degraded truthfulness, fabricated
  limitations, or technically inferior conclusions.
- Commercial plans may govern only separately authorized service features such as
  storage capacity, collaboration limits, support level, export availability,
  usage quotas, and future service entitlements — provided they do not alter
  technical truth, safety, evidence, correctness, or decision integrity.
- Commercial segmentation must not change: scoring logic; transition gates;
  readiness determinations; safety warnings; uncertainty disclosure;
  missing-information detection; evidence requirements; technical
  recommendations; specialist-escalation criteria.
- No pricing, billing, entitlement, quota, subscription, or plan-enforcement
  implementation is authorized now.

## 3. Distinguished status (must be read exactly)

```
CURRENT PERSISTENCE:                          IN-MEMORY / TEMPORARY / NON-PRODUCTION
DURABLE DATA FOUNDATION:                      NOT IMPLEMENTED
PAID SUBSCRIPTION BEFORE PHASE 4 FORMAL CLOSURE: PROHIBITED
PHASE 5 ACCOUNT / AUTHORIZATION PREREQUISITE: REQUIRED BEFORE PAID ACTIVATION
BILLING ACTIVATION:                           NOT AUTHORIZED
COMMERCIAL PLAN ACTIVATION:                   NOT AUTHORIZED
TECHNICAL EVALUATION:                         PLAN-NEUTRAL
SAFETY GATES:                                 PLAN-NEUTRAL
EVIDENCE REQUIREMENTS:                        PLAN-NEUTRAL
TECHNICAL CONCLUSIONS:                        PLAN-NEUTRAL
COMMERCIAL NON-INTERFERENCE RULE:             OWNER-APPROVED
PHASE 4:                                      NOT STARTED — NOT AUTHORIZED
PHASE 5:                                      NOT STARTED — NOT AUTHORIZED
PHASE 8:                                      NOT STARTED — NOT AUTHORIZED
CURRENT IMPLEMENTATION AUTHORITY:             NONE
CURRENT DEPLOYMENT AUTHORITY:                 NONE
```

## 4. Why OD-I and OD-N are recorded together

Both are commercial-boundary rules owned by Phase 8: OD-I is the **sequencing**
gate (no paid activation until durable data — Phase 4 — is formally closed, and
Phase 5 accounts/authorization satisfied); OD-N is the **integrity** rule (plan
level must never influence technical truth, safety, or evidence). Together they
bound commercialization on both sides — when it may start and what it may touch.
Recording them in one combined artifact keeps the linked decision coherent and is
the smallest durable increment. Each decision retains its own identifier and
status.

## 5. Prior Phase 0 recommendation status (context, not authority)

In the Phase 0 Open Owner Decisions Register both were recorded only as
`RECOMMENDATION — NOT OWNER DECISION`:
- OD-I recommendation: "confirm hard sequencing."
- OD-N recommendation: "confirm independence."

This record now converts those recommendations into **accepted decisions**. The
closed Phase 0 registers are unchanged by this record.

## 6. Canonical evidence references (repository truth)

- Plan **Phase 4 hard rule** (L279): "paid subscription activation is prohibited
  until this phase is formally closed and independently verified." (OD-I)
- Plan **Phase 8 — Subscription, Billing and Entitlements** — entry prerequisites:
  "durable persistence formally closed; accounts and authorization formally
  closed; API identity boundaries established where API access will be sold;
  privacy and legal prerequisites accepted." (OD-I)
- Plan **L319**: "Progression scoring and technical decisions must remain
  independent of commercial plan level." (OD-N); SPV §11 L360–382.
- Runtime reality: `web/app.py` `SESSION_STORE = {}` ("in-memory, non-production,
  temporary"); **no** subscription/billing/pricing/payment/checkout/entitlement/
  quota code in `web/` or `engine/`; **no** commercial routes; scoring/safety/
  progression logic contains **no** plan/tier/paid/subscription input (plan-
  neutral by construction).
- Non-activating future-commercial documentation:
  `docs/governance/INVENTORAI_COMMERCIAL_DIFFERENTIATION_DIRECTION.md` and plan
  Phase 8 (documentation of future work; authorizes nothing).
- `docs/governance/evidence/phase0_evidence_lock/OPEN_OWNER_DECISIONS_REGISTER.md`
  — OD-I and OD-N entries.

## 7. Accepted interpretation

1. **Paid subscription/billing/commercial tiers are prohibited** until the
   durable data and evidence foundation (Phase 4) is formally completed,
   independently reviewed, owner-accepted, merged, and closed, and the Phase 5
   account/authorization prerequisites are satisfied.
2. **Technical evaluation, safety gates, evidence requirements, technical
   conclusions, and progression decisions are plan-neutral** and must never be
   altered by plan, price, billing status, tier, or customer value.
3. Commercial plans may later govern only **separately authorized service
   features** (storage, collaboration, support, export, quotas, entitlements)
   that do not touch technical truth/safety/evidence.
4. These are **forward-looking rules**; the product currently has no billing and
   is plan-neutral by construction.

## 8. Rejected alternatives and reasons

| Alternative | Rejected because |
|---|---|
| Activate paid subscription/billing on in-memory storage | Data-loss/commercial risk; violates Phase 4 hard rule and Phase 8 entry prereq. |
| Let plan level influence scoring/safety/evidence/conclusions | Destroys technical integrity and truthfulness; violates L319/SPV §11. |
| Give paid users weaker gates / more favorable conclusions | Same integrity violation; rejected. |
| Give free users degraded truthfulness / fabricated limitations | Dishonest; rejected. |
| Treat pricing documentation or differentiation docs as activation | False — documentation authorizes nothing. |
| Implement billing/plans now | Out of scope; owned by Phase 8 after Phase 4/5 closure, all NOT STARTED. |

## 9. Current persistence reality

`SESSION_STORE = {}` — **in-memory, temporary, non-production**; **no durable
persistence**. No paid plan could rely on this storage; durable data (Phase 4)
must exist first.

## 10. Current absence of commercial capabilities

There is **no** subscription, billing, pricing, entitlement, quota, invoice,
checkout, or payment-provider capability in the runtime (no such code or routes).
These are future Phase 8 capabilities.

## 11. Phase 4 prerequisite and formal-closure requirement

Paid activation requires **Phase 4 — Durable Data and Evidence Foundation** to be
**formally completed, independently reviewed, owner-accepted, merged, and
closed** first (Phase 4 hard rule). Phase 4 remains **NOT STARTED / NOT
AUTHORIZED**.

## 12. Phase 5 account/authorization prerequisite

Paid activation also requires **Phase 5 — Accounts, Authentication, Authorization
and Sharing** prerequisites to be formally satisfied (Phase 8 entry prereq:
"accounts and authorization formally closed"). Phase 5 remains **NOT STARTED /
NOT AUTHORIZED**.

## 13. Phase 8 commercial implementation ownership

**Phase 8 — Subscription, Billing and Entitlements** owns plans, prices, payment,
renewal, upgrade/downgrade, cancellation, invoices, refunds, feature
entitlements, quotas, and enterprise controls — under its entry prerequisites.
Phase 8 remains **NOT STARTED / NOT AUTHORIZED**.

## 14. Commercial planning vs commercial activation (explicit distinction)

```
COMMERCIAL PLANNING:    pricing/differentiation documentation and Phase 8 design — authorizes nothing.
COMMERCIAL ACTIVATION:  live billing/subscription/entitlement enforcement — PROHIBITED until Phase 4 closed and Phase 5 satisfied.
```

The existence of commercial planning documentation is never activation.

## 15. Plan-neutrality rules (OD-N)

- **Technical evaluation:** PLAN-NEUTRAL.
- **Safety gates:** PLAN-NEUTRAL.
- **Evidence requirements/thresholds:** PLAN-NEUTRAL.
- **Technical conclusions and progression decisions:** PLAN-NEUTRAL.
Plan, price, billing status, tier, or customer value must never alter any of
these.

## 16. Allowed future service-level differences

Commercial plans may later govern only: storage capacity; collaboration limits;
support level; export availability; usage quotas; future service entitlements —
provided they do not alter technical truth, safety, evidence, correctness, or
decision integrity.

## 17. Prohibited commercial influence on technical truth

Commercial segmentation must not change scoring logic, transition gates,
readiness determinations, safety warnings, uncertainty disclosure,
missing-information detection, evidence requirements, technical recommendations,
or specialist-escalation criteria. Technical uncertainty must not be hidden,
reduced, reclassified, or omitted for any plan level.

## 18. Current honest limitations (recorded, not resolved)

No durable persistence; in-memory/temporary/non-production storage; no real
accounts; no authentication; no authorization; no payment; no subscription; no
billing; no pricing enforcement; no entitlements; no quotas; no invoices; no
checkout; no payment-provider integration; no commercial readiness;
`DEMO_READY_WITH_LIMITATIONS`; NOT PRODUCTION READY. Future pricing or
differentiation documentation does not activate any commercial capability.

## 19. What this record authorizes

- Recording OD-I and OD-N as accepted owner decisions (documentation only).
- The smallest plan status synchronization and one appended roadmap record.

## 20. What this record prohibits

- Implementing persistence; payment, subscription, billing, pricing, plans,
  quotas, entitlements, invoices, checkout, or payment-provider integration;
  commercial access tiers.
- Modifying technical evaluation, scoring, progression, readiness, safety gates,
  evidence thresholds, uncertainty, prioritization, or technical conclusions; or
  altering truthfulness/safety by plan level.
- Modifying runtime, UI, schemas, APIs, tests, templates, exports, accounts,
  authentication, authorization, or permissions.
- Claiming commercial readiness or implying documentation constitutes activation.
- Modifying Phase 0 evidence, the OD-A…OD-O records, or
  `OWNER_PRODUCT_IDENTITY_CORRECTION.md`.
- Beginning OD-K, OD-P, or OD-Q.
- Activating Phase 2, Phase 4, Phase 5, or Phase 8.
- Any implementation or deployment authority.

## 21. Immediate effect

- The persistence-before-subscription sequencing (OD-I) and plan-neutrality rule
  (OD-N) are owner-ratified and bind future Phase 4/5/8 implementation.
- No document text changes beyond this durable record, the smallest plan status
  synchronization, and one appended roadmap record. No runtime/scoring/commercial
  change.

## 22. Deferred effect

- **Durable data foundation** → Phase 4 under separate authorization (its formal
  closure is the OD-I gate).
- **Accounts/authorization** → Phase 5 under separate authorization (an OD-I
  prerequisite).
- **Subscription/billing/entitlements** → Phase 8 under separate authorization,
  after Phase 4/5, bound by OD-N plan-neutrality.

## 23. Remaining owner decisions

`OD-K, OD-P, OD-Q` remain **OPEN and unresolved**. **OD-A, OD-B, OD-C, OD-D,
OD-E, OD-F, OD-G, OD-H, OD-J, OD-L, OD-M, OD-O** remain previously accepted and
merged and are **unchanged** by this record. Only OD-I and OD-N are decided here.

## 24. Implementation and deployment authority

```
IMPLEMENTATION AUTHORITY: NONE
DEPLOYMENT AUTHORITY:     NONE
```

Product remains `DEMO_READY_WITH_LIMITATIONS`; storage is in-memory / temporary /
non-production; there is no billing; the product is NOT PRODUCTION READY.

## 25. Evidence classification

This is a **Phase 1 owner-decision evidence artifact** (documentation only). It
is authoritative as a record of the owner's accepted OD-I and OD-N decisions once
independently reviewed, owner-accepted, merged, and post-merge verified. Its
authority is that of a decision record; it grants no implementation or deployment
authority. No commercial capability exists or is implemented; technical
evaluation, safety, evidence, and conclusions are plan-neutral; paid activation
is prohibited until Phase 4 is formally closed and Phase 5 satisfied.
