# Phase 1 — Owner Decision OD-K — API Exposure Model and Core-to-Adapter Separation

**Phase:** Phase 1 — Owner Product Decisions
(of `docs/governance/PRODUCT_FOUNDATION_AND_COMMERCIAL_READINESS_REMEDIATION_PLAN.md`).
**Decision ID:** OD-K (API exposure model and core-to-adapter separation).
**Scope:** documentation-only durable record of one accepted owner decision. **No
engine, `ai_advisor`, service-layer, API, adapter, route, schema, export,
template, test, client, authentication, permission, commercial, deployment, or
integration change. No downstream activation.**
**Authoritative branch:** `feature/atomic-json-session-persistence`.
**Verified official base at authoring:** `8e2854ff27048d6e9cf3d84e84b4dbe4e609940e`
(official tip after PR #299, which merged the OD-I/OD-N increment).

---

## 1. Decision status

```
OD-K — OWNER DECISION ACCEPTED
```

This is a forward-looking architectural boundary confirmation, largely consistent
with the current architecture. It authorizes no code change. No other open owner
decision is resolved, no nuance is remediated, and no downstream phase is
activated.

## 2. Accepted owner decision (verbatim)

> **OD-K — OWNER DECISION ACCEPTED**
>
> THE PRODUCT SHALL PRESERVE A STRICT SEPARATION BETWEEN: (1) THE DETERMINISTIC
> CORE ENGINE; (2) INTERNAL APPLICATION OR SERVICE ORCHESTRATION; (3) VERSIONED
> EXTERNAL APIs; (4) DELIVERY ADAPTERS AND CHANNEL-SPECIFIC INTEGRATIONS. EXTERNAL
> API, CLIENT, UI, MOBILE, PARTNER, COMMERCIAL, AUTHENTICATION, DEPLOYMENT, OR
> VENDOR-SPECIFIC CONCERNS MUST NOT BE EMBEDDED DIRECTLY INTO THE DETERMINISTIC
> TECHNICAL-EVALUATION CORE.

## 3. Distinguished status (must be read exactly)

```
DETERMINISTIC CORE SEPARATION:            OWNER-APPROVED
INTERNAL SERVICE / ORCHESTRATION BOUNDARY: OWNER-APPROVED
VERSIONED EXTERNAL API MODEL:             OWNER-APPROVED
INTEGRATION ADAPTER SEPARATION:           OWNER-APPROVED
AUTHENTICATION / AUTHORIZATION / PERMISSIONS: OUTSIDE DETERMINISTIC CORE
COMMERCIAL PLAN / ENTITLEMENT CHECKS:     OUTSIDE DETERMINISTIC CORE
VENDOR-SPECIFIC TRANSPORT:                OUTSIDE DETERMINISTIC CORE
CURRENT INTERNAL SERVICE LAYER:           NOT IMPLEMENTED
CURRENT VERSIONED EXTERNAL API:           NOT IMPLEMENTED
CURRENT INTEGRATION ADAPTER FOUNDATION:   NOT IMPLEMENTED
AI ADVISOR VENDOR HTTP BOUNDARY:          LOW ARCHITECTURAL NUANCE / RECORDED / UNRESOLVED / NOT REMEDIATED BY THIS INCREMENT
CR-1:                                     LOW / RECORDED / UNRESOLVED / NOT REMEDIATED BY THIS INCREMENT
PHASE 6:                                  NOT STARTED — NOT AUTHORIZED
PHASE 7:                                  NOT STARTED — NOT AUTHORIZED
CURRENT IMPLEMENTATION AUTHORITY:         NONE
CURRENT DEPLOYMENT AUTHORITY:             NONE
```

## 4. Prior Phase 0 recommendation status (context, not authority)

In the Phase 0 Open Owner Decisions Register OD-K was recorded only as a
`RECOMMENDATION — NOT OWNER DECISION`: "confirm core→adapter separation." This
record now converts that recommendation into an **accepted decision**. The closed
Phase 0 registers are unchanged by this record.

## 5. Canonical evidence references (repository truth)

- Plan **§3.7 API interoperability** L181–185: "…**separation between the core
  engine and external adapters**" (versioned contracts, authentication,
  authorization scopes, auditability, rate limiting, etc.).
- Plan **Phase 7 architecture** L305: **"Core Engine → Internal Service Layer →
  Versioned API Contracts → Integration Adapters → External Applications."**
- Plan **Phase 6** — Domain Registry / Technology Capability Registry / domain-pack
  and capability-pack contracts; "no core branching on domain names."
- Current code: `web/app.py` imports **from `engine`** (correct dependency
  direction); the deterministic evaluation modules (`engine/scoring.py`,
  `engine/progression_loop.py`, `engine/idea_state.py`,
  `engine/normalize_output.py` — "no HTTP, no env vars") are transport-free;
  `engine/domain_registry.py` + `engine/domain_rules.py` modularize domain logic.
- `docs/governance/evidence/phase0_evidence_lock/OPEN_OWNER_DECISIONS_REGISTER.md`
  — OD-K entry.

## 6. Accepted interpretation

The product must preserve a strict four-layer separation — deterministic core →
internal service/orchestration → versioned external API → delivery adapters —
with external/transport/commercial/auth/vendor concerns kept out of the
deterministic technical-evaluation core. This ratifies the intended architecture;
it does not describe or authorize present API/service/adapter capabilities.

## 7. Rejected alternatives and reasons

| Alternative | Rejected because |
|---|---|
| Couple external apps/UI/partners directly to the core | Violates §3.7 core-vs-adapter separation; makes the deterministic engine fragile and vendor-bound. |
| Let commercial plan / auth checks run inside the core | Violates OD-N plan-neutrality; mixes commerce/identity with technical truth. |
| Let adapters override/fabricate core outcomes | Destroys deterministic integrity and truthfulness. |
| Hard-code domain branching in the core | Violates Phase 6 "no core branching on domain names"; use governed registries/packs. |
| Refactor `engine/ai_advisor.py` here | Out of scope; this is documentation-only and the nuance is deferred to Phase 6/7. |

## 8. Deterministic core responsibilities

The deterministic core owns: technical evaluation; progression logic; state
transitions; deterministic question-selection behavior; evidence requirements;
safety gates; uncertainty handling; readiness determinations; and technical
conclusions.

## 9. Orchestration / service responsibilities

Internal application or service orchestration may coordinate deterministic-core
invocation, persistence, accounts and permissions, evidence storage, exports,
notifications, workflows, and API request handling — but must **not** rewrite,
bypass, fabricate, or override deterministic technical rules.

## 10. External API responsibilities

External APIs must be explicit, versioned, contract-governed,
compatibility-governed, independently testable, and separated from
transport-specific adapters.

## 11. Adapter responsibilities

Delivery and integration adapters may translate transport, serialization,
presentation, authentication context, and channel-specific inputs/outputs — but
must **not** change technical truth, safety, evidence requirements, uncertainty,
or conclusions.

## 12. Dependency-direction rule

The web/presentation and adapter layers depend on the core; the deterministic
core must not depend on HTTP frameworks, web routes, templates, mobile clients,
account/identity/auth providers, payment/subscription providers, deployment
environments, analytics/observability vendors, third-party channels, or
vendor-specific AI/external-service transports.

## 13. Versioning and contract-governance rule

External APIs must carry explicit versioned contracts with published
compatibility commitments, stable error contracts, and independent testability —
distinct from transport adapters.

## 14. Domain / capability interface rule

Domain registries, domain packs, and capability packs must be consumed through
governed interfaces (e.g. `engine/domain_registry.py`), not scattered hard-coded
domain branching inside the deterministic core.

## 15. Authentication and permission boundary

Authentication, authorization, permissions, quotas, and entitlements must remain
**outside** the deterministic evaluation core (consistent with OD-J's role model
and OD-I/OD-N's commercial boundaries).

## 16. Commercial non-interference boundary

Commercial plan level must not alter technical conclusions, progression, safety
gates, evidence thresholds, readiness, uncertainty, or specialist-escalation
criteria (consistent with OD-N). Billing/commercial-plan checks belong outside the
core.

## 17. Vendor-integration boundary

Vendor-specific transports (AI or other external services) must sit behind a
governed adapter/service boundary, not inside the deterministic evaluation core.

## 18. Current architecture reality

The product is a single Flask app (`web/app.py`) that imports and orchestrates the
`engine/` package directly. The dependency direction is correct (web → engine);
the deterministic evaluation core is transport-free; the web layer does **not**
re-implement or override engine scoring/progression decisions.

## 19. Current missing capabilities

There is **no internal service layer**, **no versioned external API**, and **no
integration adapter foundation**. These are future Phase 7 capabilities (built on
the Phase 6 foundation).

## 20. `engine/ai_advisor.py` LOW boundary nuance (recorded, not resolved)

`engine/ai_advisor.py` currently contains a vendor-specific outbound HTTP call
(to `https://api.anthropic.com/v1/messages`). That module is **advisory-only** and
does **not** control deterministic scoring, safety gates, progression, or
technical conclusions. Its location inside the `engine/` package is a **LOW
architectural boundary nuance**; future Phase 6/Phase 7 work should place vendor
transport behind a governed adapter or service boundary. **This increment does not
move, refactor, or modify that code, and does not claim the nuance is resolved.**

```
AI ADVISOR VENDOR HTTP BOUNDARY: LOW / RECORDED / UNRESOLVED / NOT REMEDIATED BY THIS INCREMENT
```

## 21. CR-1 preservation

```
CR-1: LOW / RECORDED / UNRESOLVED / NOT REMEDIATED BY THIS INCREMENT
```

CR-1 (latent multi-domain `infer_domain` vs electronics-only admission) remains a
recorded Phase 2 reconciliation item. This record neither resolves nor
reclassifies it.

## 22. Phase 6 dependency (textually supported)

The domain/capability registry and pack interfaces that OD-K's core→adapter
consumption relies on are owned by **Phase 6 — Multi-Domain and Technology
Capability Foundation** ("no core branching on domain names"). Phase 6 remains
**NOT STARTED / NOT AUTHORIZED**.

## 23. Phase 7 implementation ownership (textually supported)

The internal service layer, versioned API contracts, and integration adapters are
owned by **Phase 7 — API and Integration Foundation** ("Core Engine → Internal
Service Layer → Versioned API Contracts → Integration Adapters → External
Applications"). Phase 7 remains **NOT STARTED / NOT AUTHORIZED**.

## 24. What this record authorizes

- Recording OD-K as an accepted owner decision (documentation only).
- The smallest plan status synchronization and one appended roadmap record.

## 25. What this record prohibits

- Modifying engine code (including `engine/ai_advisor.py`); moving vendor HTTP
  calls.
- Implementing an internal service layer, external APIs, API versioning/contracts,
  or adapters.
- Modifying routes, schemas, exports, templates, tests, clients, or mobile code.
- Implementing authentication, authorization, permissions, quotas, entitlements,
  or billing.
- Modifying deterministic scoring, progression, gates, evidence, readiness,
  safety, uncertainty, or conclusions.
- Resolving or reclassifying CR-1; claiming the AI-advisor nuance is resolved.
- Modifying Phase 0 evidence, the OD-A…OD-O records, or
  `OWNER_PRODUCT_IDENTITY_CORRECTION.md`.
- Beginning OD-P or OD-Q; beginning Phase 1 closure.
- Activating Phase 2, Phase 6, or Phase 7.
- Any implementation or deployment authority.

## 26. Immediate effect

- The four-layer separation (core / service / versioned API / adapter) is
  owner-ratified and binds future Phase 6/7 implementation.
- No document text changes beyond this durable record, the smallest plan status
  synchronization, and one appended roadmap record. No engine/web/API change.

## 27. Deferred effect

- **Domain/capability registry and pack interfaces** → Phase 6 under separate
  authorization.
- **Internal service layer, versioned external API, integration adapters, and the
  `engine/ai_advisor.py` vendor-transport relocation** → Phase 7 (on the Phase 6
  foundation) under separate authorization.

## 28. Remaining owner decisions

`OD-P, OD-Q` remain **OPEN and unresolved**. **OD-A, OD-B, OD-C, OD-D, OD-E, OD-F,
OD-G, OD-H, OD-I, OD-J, OD-L, OD-M, OD-N, OD-O** remain previously accepted and
merged and are **unchanged** by this record. Only OD-K is decided here.

## 29. Implementation and deployment authority

```
IMPLEMENTATION AUTHORITY: NONE
DEPLOYMENT AUTHORITY:     NONE
```

Product remains `DEMO_READY_WITH_LIMITATIONS`; the deterministic core is currently
transport-free; there is no service layer, versioned API, or adapter foundation;
the product is NOT PRODUCTION READY.

## 30. Evidence classification

This is a **Phase 1 owner-decision evidence artifact** (documentation only). It is
authoritative as a record of the owner's accepted OD-K decision once independently
reviewed, owner-accepted, merged, and post-merge verified. Its authority is that
of a decision record; it grants no implementation or deployment authority. No
service/API/adapter/auth/commercial capability exists or is implemented; the
`engine/ai_advisor.py` vendor-HTTP nuance and CR-1 remain recorded and unresolved.
