# P7-C — Formal Phase-7 (API and Integration Foundation) Contract & Acceptance Criteria

**Status:** OWNER-ACCEPTED CONTRACT OF RECORD — DEFINITION ONLY. Governance/documentation-only.
The **P7-C contract itself confers no implementation authorization.** Implementation of **P7-I1** and
the successive Phase-7 increments proceeds under the **separate Standing Phase-7 Authorization**
(`D-P7-STANDING-01`) — a distinct, later owner decision that authorizes remaining Phase-7 work through
formal Phase-7 closure **subject to** this contract's boundaries, per-gate bounded scope, accepted
evidence triggers, tests where applicable, Lean minimum-path, independent review where required, and the
mandatory §25 Remaining-Obligation / Exit-Criteria Review. **Phases 8/9/10 and separately governed
capabilities remain out of scope / unauthorized.** All frozen P7-B/P7-C architectural constraints remain
binding.

**Owner gate:** `G-P7C-FORMAL-PHASE-7-CONTRACT-PUBLICATION-01`. **Owner decisions:** `D-P7C-01` (contract
acceptance) and the distinct `D-P7-STANDING-01` (Standing Phase-7 Authorization — recorded separately,
not part of this contract's meaning). **Authoritative basis tip:**
`f82b18b4b871b4ce5f8e7d85e603889962ba56b3` (`feature/atomic-json-session-persistence`; PR #400 §5-CLOSE
merge; tree `ff1e55f`). **Canonical Phase-7 authority:**
`PRODUCT_FOUNDATION_AND_COMMERCIAL_READINESS_REMEDIATION_PLAN.md` §5 — *Phase 7 — API and Integration
Foundation* (`Core Engine → Internal Service Layer → Versioned API Contracts → Integration Adapters →
External Applications`). **D-FPC-MAP-06** is binding.

This document is subordinate to the committed governance anchors, `ACTIVE_EXECUTION_ROADMAP.md`, the
Master Obligation Index, and `OWNER_DECISION_REGISTER.md`. It formalizes the owner-accepted, frozen
**P7-A** discovery and **P7-B** architecture decisions (including the accepted **P7-B correction
addendum** — 8 corrections — and the accepted **P7-C contract correction addendum** — 8 corrections).
The correction addenda supersede any conflicting earlier wording; where they conflict, the correction
addenda govern.

---

## 1. Authority / baseline

Repository `Amirjaferali/inventorai`; authoritative branch `feature/atomic-json-session-persistence`;
live tip verified read-only at publication = `f82b18b` (byte-identical to the accepted P7-A/P7-B
baseline). Product-Foundation §5 is FORMALLY ACCEPTED AND CLOSED. Phase 7 is the active phase under the
Standing Phase-7 Authorization. This contract carries no implementation authority of its own.

## 2. Purpose

Convert the frozen P7-B architecture/resource/API decisions into a bounded, observable, testable
Phase-7 contract with per-gate acceptance criteria and a complete original-obligation register, so that
the Lean read/export-first API-and-integration foundation can be executed under the Standing Phase-7
Authorization without displacing any original Phase-7 obligation.

## 3. Scope

Phase-7 API and Integration Foundation intent only: the initial read/export-first public surface; a Lean
internal read/export service seam; a distinct machine/API identity concept; a first-public-exposure
security baseline; the outbound canonical→adapter boundary; the inbound-result trust invariant; and the
deferral rules for subsystem identity, async, writes/imports, inbound persistence, and vendor
integration. It defines contract requirements and acceptance criteria, not implementation.

## 4. Explicit exclusions

This contract, of itself, authorizes no code: publishing it does not modify application code or tests,
implement any API/service/identity/adapter/import/write/async/webhook/vendor behavior, activate a domain,
establish any bounded increment contract, deploy, or release. Implementation is governed by the separate
Standing Phase-7 Authorization and by each increment's own bounded contract established from this
document. This contract freezes **no** endpoint names, URL paths, HTTP method inventory, JSON field
names, DB schemas, migrations, Python class/module designs, token/credential formats, error codes, vendor
schemas, or async resource names. A successful first proof is **never** a trigger for P7-CLOSE (§25). The
`P7-I1/I2/I3` labels are conceptual future gates, not standing activation.

## 5. Frozen P7-B decisions (formalized, not reopened)

- **D1** Initial independently addressable product contract surface = Project read representation +
  Versioned Structured Output/Export only; Domain support-state and Evidence/Provenance ride within them
  as governed concepts; Gap/Risk/Validation/Subsystem standalone resources deferred; internal
  serialization ≠ public contract; FDC-001 = precedent/foundation only; ProjectRecordContract =
  design/serialization/provenance foundation, not automatically the public wire contract.
- **D2** Lean internal service/use-case boundary required before public exposure; first slice = retrieve
  authorized project read representation + produce versioned structured export; no
  session/refinement/progression/write; no mandatory full web-route migration; not
  microservices/mesh/plugin-platform/orchestrator/ESB/second engine.
- **D3** Subsystem public API + durable identity DEFERRED; trigger = a real integration needing
  independent persistent subsystem addressing; later subsystem domain metadata consumes the canonical
  Domain Registry + §5 support-state; root `confirmed_domain` preserved.
- **D4** Distinct machine/API principal via canonical authz/ownership; least privilege;
  revocation/expiration/rotation/auditability; browser session auth never reused; principal↔account
  taxonomy and credential representation deferred.
- **D5** Security baseline from first public exposure (incl. read-only); idempotency + mutation audit +
  concurrency before writes; pagination/quotas/async/advanced-retry deferred; no obligation silently deleted.
- **D6** Read/export-first; no public state mutation in v1; no privileged path around
  ownership/progression/evidence/Keep-Refine/full re-evaluation.
- **D7** Outbound canonical→adapter→vendor; InventorAI = central context authority; external tools =
  specialized processors; no orchestrator/vendor-shaped-core/routing engine.
- **D8** External results untrusted by default; never auto-mutate progression / prove feasibility-safety /
  satisfy validation / activate domain / become trusted evidence / replace review; persistence mechanics
  not decided here.
- **D9** Async/job infrastructure DEFERRED; no ExternalProcessingRequest/Result/Job/Task reserved; trigger
  = a bounded integration proving a genuinely async lifecycle; separate gate required.
- **D10** First integration proof = outbound-only, non-mutating, vendor-neutral; Wokwi NOT SELECTED.
- **D11** No absorption of CAP-15…18 / AISR / Project Technology Profile / WS-PFV-001 / WS17 / STG / ACV /
  QTA / PDF Download / Email Delivery / Output Language / Phase-9 Domain Activation; reusability ≠
  authorization; no second Domain Registry / Technology Capability Registry / orchestrator / routing engine.
- **D12** Lean sequence P7-C → P7-I1 (internal seam) → P7-I2 (public API + security baseline) → P7-I3
  (outbound adapter proof); further work evidence-gated; labels are conceptual, not standing activation.

## 6. Canonical architectural boundaries

Layering (consumes the canonical Phase-7 architecture; introduces no new architecture): **Deterministic
Core Engine** (scoring, progression, validation, domain activation — unchanged) → **Internal
Application/Use-Case Service Boundary** (governed operations; enforces ownership + progression + Keep/Refine
invariants) → **Versioned Public API Contracts** (transport, versioning, authn/authz, error envelope,
correlation, audit, rate-limit) → **Integration Adapters** (canonical↔vendor translation; vendor specifics
isolated) → **External Applications**. Persistence/store sits beneath the service boundary and is never
exposed directly. No orchestrator, mesh, ESB, plugin platform, routing engine, or second engine.

## 7. Public v1 resource / contract boundary

**Initial independently addressable product contract surface:** (1) Project read representation; (2)
Versioned Structured Output/Export. Domain, Evidence, Gap, Risk, Validation, and Subsystem are **not**
independent top-level product resources in initial v1; canonical Domain identity/support-state and
Evidence/Provenance ride within the two contracts as governed concepts/projections. **Transport/security
metadata needed to operate the API** does **not** constitute a new product resource. Additional independent
product resources require a demonstrated use case and a separate contract decision. The number "two" is the
current minimal surface, **not** a permanent numeric architectural invariant. Never public contracts:
presentation/template-shaped structures, `SESSION_STORE` shapes, SQLite row/schema shapes, raw engine
internals, dataclass field layouts. FDC-001 = precedent/foundation only. ProjectRecordContract = design/
serialization/provenance foundation, not automatically the public wire contract. *(No field names/paths frozen.)*

## 8. Internal service boundary

Required before public exposure. First slice = two read-side operations: retrieve an authorized project/read
representation; produce a governed/versioned structured export. Enforces project ownership; performs no
mutation. Excluded from the first slice: start/advance session, refinement, progression mutation, writes.
Engine keeps scoring/progression/validation/activation; persistence keeps atomic
storage/record-store/session-reconstruction; API/adapters own wire (de)serialization, versioning,
authn/authz, errors, adapter translation. Web-route migration is staged, not a prerequisite. Prohibited:
microservices, distributed architecture, service mesh, plugin platform, Integration Orchestrator, ESB,
second business/domain engine. *(No class/module/file design frozen.)*

## 9. Machine/API identity + authorization principles

A distinct machine/API principal receives explicit least-privilege authorization grants/scopes over
permitted project resources through the canonical ownership/authorization model (consuming Phase-5 project
ownership). Firm requirements: least privilege; project-scoped authorization; revocation; expiration;
rotation; auditability; strict separation from browser signed-cookie/session auth (never reused, directly or
indirectly, as a machine credential). Not frozen (deferred): token format, credential wire representation,
OAuth-vs-API-key choice, principal taxonomy beyond the minimum, principal↔human-account relationship.
Possible future principal forms (user-delegated client / service principal / organization-partner) remain
open. Contract minimum for v1: every public request is attributable to an authenticated machine/API
principal whose authorization is evaluated through the canonical model before any project data is returned.
*(No token/credential format frozen.)*

## 10. First-public-exposure security baseline

Required from the first public exposure, **including read-only**: public-contract version identity;
authentication; authorization; stable error envelope; request/correlation identity; basic API
access/security audit; basic protective rate limiting; request provenance where applicable; export/public-contract
version identity. **Import contract/version identity is NOT part of the initial read-only contract** — it
activates only if a separate Import gate is later authorized. **Before write operations, additionally:**
API/HTTP idempotency; mutation-specific audit semantics; write concurrency/conflict rules where applicable.
**Deferred until demonstrated need** (ownership/reason/trigger recorded, §18): pagination where no unbounded
collection exists; quotas beyond the protective rate-limit floor; async job lifecycle; advanced async retry.
**Audit is not Monitoring; the basic rate-limit floor is not all Abuse Controls** — Monitoring and broader
Abuse Controls remain distinct preserved obligations (§18).

## 11. Read/export-only initial mutation boundary

Initial public API direction is **read/export-first**; **no public state mutation** is part of the v1
contract. No privileged API path may bypass project ownership, deterministic progression, evidence/provenance,
Keep-Current-Snapshot / Refine-This-Idea semantics, or full re-evaluation after material revision. Any future
material external write, if separately authorized, re-enters the identical governed product rules — external
origin grants no exemption and no partial re-evaluation unless a future deterministic dependency model
explicitly authorizes it.

## 12. Outbound export / adapter rules

Preserve **InventorAI Canonical Contract → Integration Adapter → External Tool/Vendor Representation.**
InventorAI remains the central project/context authority; external tools remain specialized processors.
Outbound envelope (conceptual): project identity + version/revision; canonical domain identity +
support-state; selectable, minimized evidence/provenance/assumptions/gaps/requirements; **optional subsystem
context metadata only where current source data can represent it truthfully without implying durable subsystem
identity, independently addressable subsystem resources, stable subsystem API semantics, or domain activation
beyond canonical support-state truth** — if current subsystem context is not sufficiently stable for a public
export contract, it is omitted from initial v1 rather than inventing durability (a future demonstrated
subsystem-integration need triggers the separately governed subsystem gate, §14). Vendor-specific schemas,
credentials, quirks, error formats, and protocols stay in adapters, outside core canonical contracts.
Prohibited: Integration Orchestrator, vendor-shaped core, second integration architecture, tool-routing
engine. *(No wire/vendor schema frozen.)*

## 13. Inbound trust invariants

External results are **untrusted by default**. An **explicit governed review/acceptance status or mechanism
is required before any authorized project-state effect.** External results must **never automatically**:
mutate deterministic progression; prove feasibility; prove safety; satisfy validation; activate a domain;
become trusted evidence; replace human/expert review. Minimum inbound provenance concepts (source/processor
identity, request linkage to project version/revision, result type, timestamp) are formalized as invariants
only. **Exact state names, number of states, transitions, persistence representation, storage location,
retention, deletion lifecycle, and record schema are NOT frozen in P7-C.** If later inbound work is
authorized, it uses a governed untrusted/staging representation by **minimally extending** existing
`ProjectRecordContract` provenance/validation concepts (D-FPC-MAP-06) — no new registry unless future evidence
proves existing ownership cannot be extended safely.

## 14. Subsystem deferral rule

Subsystem public API and durable identity are **DEFERRED**; not a mandatory Phase-7 prerequisite; not
implemented or frozen proactively. Trigger: a real integration requires independent persistent
addressing/round-trip of a specific subsystem. Any later subsystem domain metadata consumes the canonical
Domain Registry + §5 support-state; project/root `confirmed_domain` semantics preserved.

## 15. Async deferral rule

Async/job infrastructure is **DEFERRED**; no canonical `ExternalProcessingRequest` / `ExternalProcessingResult`
/ `Job` / `Task` reserved. Trigger: a real bounded integration proves a materially asynchronous lifecycle that
cannot safely use synchronous/local/file handling. Async/webhook work requires a separate evidence-triggered
gate under the Standing Phase-7 Authorization. Adapter-boundary retries/timeouts remain an integration concern
and do not force async infrastructure.

## 16. First integration proof contract

The first proof is **outbound-only, non-mutating, vendor-neutral**: *Canonical InventorAI Export →
Local/Reference Adapter → External/Transformed Representation → Validation and optional inverse-transform/
equivalence checking performed entirely OUTSIDE governed project-state mutation.* It must prove canonical
contract stability, project version/revision identity, adapter isolation, vendor neutrality, data
minimization, and provenance preservation. It must **not** import back into live project state, mutate
progression, require a public write path, or select a vendor. **WOKWI: NOT SELECTED.**

## 17. Ownership / D-FPC-MAP-06 non-duplication rules

Phase 7 builds infrastructure others may later consume but builds none of their logic and absorbs none of
them. Separate ownership preserved for: CAP-15, CAP-16, CAP-17, CAP-18, AISR, Project Technology Profile
(where separately governed), WS-PFV-001, WS17, STG, ACV, QTA, PDF Download, Email Delivery, Output Language,
Phase-9 Domain Activation. Reusable Phase-7 infrastructure authorizes none of them. Prohibited: second Domain
Registry; Technology Capability Registry without new evidence; Integration Orchestrator; AI routing engine;
tool recommendation engine. Before proposing any new Service/Registry/Resource/Orchestrator/Job/Capability/
Integration model, classify per D-FPC-MAP-06 (ALREADY OWNED-CONSUME / PARTIALLY OWNED-EXTEND MINIMALLY /
PHASE-7 CANONICAL / FUTURE-OTHER OWNER / GENUINELY NEW-AND-REQUIRED); new terminology is not evidence of new
architecture.

## 18. Original Phase-7 obligation register

Every obligation is retained; none is deleted or silently superseded. For each: **STATUS / OWNER / DEFERRAL
REASON / ACTIVATION-OR-REVIEW TRIGGER / CLOSURE EFFECT.** Owner = "Phase 7" unless noted.

**Register rules.** (A) No row may state or imply that a deferred obligation is a non-blocker (or blocker) for
Phase-7 closure; every deferred/partial row's CLOSURE EFFECT = **TO BE DETERMINED BY §25 EXIT REVIEW**. (B)
Obligations slated for delivery keep STATUS `IN P7-Ix`; §25 verifies delivery. (C) Distinct obligations stay
distinct — Audit, Monitoring, and Abuse Controls are three separate rows; Reference/Test Harness and
Partner/External-Integration Sandbox are two separate rows; no row's delivery is represented as satisfying
another. (D) Every deferred/partial row carries owner, current deferral reason, activation/review trigger, and
CLOSURE EFFECT = TO BE DETERMINED BY §25.

| Obligation | Status | Deferral reason (if any) | Activation / review trigger | Closure effect |
|---|---|---|---|---|
| Resource model (v1) | IN P7-I2 | — | — | Verified delivery assessed at §25 |
| Service boundary | IN P7-I1 | — | — | Verified delivery assessed at §25 |
| Public API boundary | IN P7-I2 | — | — | Verified delivery assessed at §25 |
| API versioning | IN P7-I2 | — | — | Verified delivery assessed at §25 |
| Authentication | IN P7-I2 | — | — | Verified delivery assessed at §25 |
| Machine/API identity | IN P7-I2 | — | — | Verified delivery assessed at §25 |
| Authorization/scopes | IN P7-I2 | — | — | Verified delivery assessed at §25 |
| Stable errors | IN P7-I2 | — | — | Verified delivery assessed at §25 |
| Request/correlation tracing | IN P7-I2 | — | — | Verified delivery assessed at §25 |
| Audit (access/security) | IN P7-I2 | — | — | Verified delivery assessed at §25 |
| Rate limits (protective floor) | IN P7-I2 | — | — | Verified delivery assessed at §25 |
| Export contracts | IN P7-I2/I3 | — | — | Verified delivery assessed at §25 |
| Adapter contract | IN P7-I3 | — | — | Verified delivery assessed at §25 |
| Outbound API (export) | IN P7-I2/I3 | — | — | Verified delivery assessed at §25 |
| Reference/Test Harness | IN P7-I3 (local, outbound, non-mutating) | — | — | Verified delivery assessed at §25 |
| Secrets | IN P7-I2 (identity) | — | — | Verified delivery assessed at §25 |
| Revocation | IN P7-I2 | — | — | Verified delivery assessed at §25 |
| Compatibility | POLICY FROM v1 (§23) | — | — | Standing policy; assessed at §25 |
| **Monitoring** | PRESERVED ORIGINAL OBLIGATION / CURRENT MINIMUM NOT YET FROZEN | Initial read/export has not yet established the minimum operational-monitoring requirement | P7-I2 public exposure and/or §25 review | TO BE DETERMINED BY §25 |
| **Abuse controls (broad)** | PRESERVED ORIGINAL OBLIGATION (rate-limit floor is one component, not fulfillment) | Advanced controls not yet scoped | Abuse evidence and/or §25 review | TO BE DETERMINED BY §25 |
| **Partner/External-Integration Sandbox** | PRESERVED ORIGINAL OBLIGATION (distinct; not delivered by the reference adapter) | No partner/external integration selected | Real partner/external-integration need | TO BE DETERMINED BY §25 |
| External-submission provenance | INVARIANT (§13); persistence deferred | Persistence not decided | Inbound gate authorized | Invariant holds; mechanics TO BE DETERMINED BY §25 |
| Deprecation | POLICY FROM v1; event deferred | No deprecation event yet | First deprecation | TO BE DETERMINED BY §25 |
| HTTP idempotency | DEFERRED IN CURRENT INITIAL SCOPE | No v1 public writes | Write gate authorized | TO BE DETERMINED BY §25 |
| Quotas (beyond floor) | DEFERRED IN CURRENT INITIAL SCOPE | No demonstrated need | Abuse/scale evidence | TO BE DETERMINED BY §25 |
| Retries/timeouts | DEFERRED IN CURRENT INITIAL SCOPE | No vendor/async yet | Real adapter/integration | TO BE DETERMINED BY §25 |
| Import contracts | DEFERRED IN CURRENT INITIAL SCOPE | Read/export-first | Import gate authorized | TO BE DETERMINED BY §25 |
| Inbound API | DEFERRED IN CURRENT INITIAL SCOPE | Untrusted-result caution | Inbound gate authorized | TO BE DETERMINED BY §25 |
| File exchange (governed import) | DEFERRED IN CURRENT INITIAL SCOPE | No import path in v1 | Import/integration gate | TO BE DETERMINED BY §25 |
| Embedded integration | DEFERRED IN CURRENT INITIAL SCOPE | No use case | Demonstrated need | TO BE DETERMINED BY §25 |
| Partner connectors | DEFERRED IN CURRENT INITIAL SCOPE | No partner selected | Partner use case | TO BE DETERMINED BY §25 |
| Webhooks | DEFERRED IN CURRENT INITIAL SCOPE | Async deferred | Async/webhook gate | TO BE DETERMINED BY §25 |
| Subsystem durable identity/API | DEFERRED IN CURRENT INITIAL SCOPE (§14) | Owner-accepted, unproven | Real subsystem integration | TO BE DETERMINED BY §25 |
| Async/job model | DEFERRED IN CURRENT INITIAL SCOPE (§15) | No async lifecycle proven | Async-lifecycle evidence | TO BE DETERMINED BY §25 |
| Pagination | DEFERRED IN CURRENT INITIAL SCOPE | No unbounded v1 collection | First unbounded collection | TO BE DETERMINED BY §25 |

Any obligation later classified **STILL REQUIRED BEFORE PHASE-7 CLOSURE** blocks closure (§25).

## 19. Proposed future implementation gates

*(Conceptual sequence under the Standing Phase-7 Authorization; each increment still requires its own bounded
contract established from this document, a verified live base, acceptance criteria, evidence, tests where
applicable, Lean minimum-path, and independent review where required — no repeated top-level owner
authorization is needed, but no gate self-activates.)*

- **P7-I1 — Internal Read/Export Service Boundary.** Smallest internal read/export seam. EXCLUSIONS: public
  exposure, writes, identity, vendor, async, subsystem. DEPENDENCIES: P7-C accepted + bounded P7-I1 contract established.
- **P7-I2 — Versioned Read/Export Public API + Security Baseline.** Expose read/export contracts with the §10
  security baseline (machine identity, authz, versioning, stable errors, correlation, audit, rate-limit; no
  writes). EXCLUSIONS: writes, vendor, async, subsystem, inbound ingestion. DEPENDENCIES: P7-I1.
- **P7-I3 — Canonical Export + Local/Reference Adapter Proof.** Outbound-only non-mutating vendor-neutral proof
  (§16). EXCLUSIONS: vendor, state-mutating import. DEPENDENCIES: P7-I2.
- **Evidence-triggered separate gates:** write/import; inbound-result persistence/review; subsystem durable
  identity/public API; async/webhook; real-vendor integration — each executable only when its accepted trigger
  is actually met.
- **P7-CLOSE** — only after the §25 Remaining-Obligation / Exit-Criteria Review and satisfaction of closure criteria.

## 20. Acceptance criteria per future gate

- **P7-I1:** RED-first tests prove the two read-side operations absent, then GREEN; the seam performs **no
  governed project/business-state mutation and no project revision/content change** (evidence: canonical
  persisted-state equality/hash or another reliable semantic comparison; audit/access metadata separately
  emitted by the security layer does not count as project-state mutation); ownership enforced at the seam
  (authorized vs unauthorized project → allow/deny); full existing suite regresses clean; no public route added.
- **P7-I2:** unauthenticated request denied; authenticated-but-unauthorized principal denied
  (authorization-denial + ownership-isolation: principal A cannot read principal B's project); response carries
  public-contract version identity; malformed/error paths return the stable error envelope; every request emits
  a correlation id captured in audit; rate-limit floor returns a deterministic throttled response beyond
  threshold; browser-session credential rejected on the machine/API path; no write endpoint exists.
- **P7-I3:** canonical export → adapter → external representation → inverse/equivalence check runs entirely
  outside governed state (no governed project/business-state mutation and no revision/content change, by
  semantic comparison); adapter contains all vendor-shaped translation (no vendor-specific symbol imported by
  core); data-minimization honored; provenance preserved across the round-trip; no vendor selected.
- **Cross-gate:** no criterion may be false-greenable (no `pytest.raises(Exception)` swallowing setup errors;
  RED must fail for the intended reason).

## 21. Test / evidence expectations

Per implementation gate: genuine RED-first focused tests on the exact base; GREEN focused tests; regression
tests (full suite); authorization-denial tests; ownership-isolation tests; stable-error tests;
correlation/audit evidence; rate-limit evidence; canonical-contract round-trip/equivalence evidence;
adapter-isolation evidence; proof of no vendor-specific core dependency; proof of no governed project-state
mutation in the first proof; proof of no trust bypass. Exact test file names are not frozen unless live
repository structure requires them at implementation time.

## 22. Security acceptance criteria

From first public exposure: (a) no project data returned without an authenticated machine/API principal; (b)
authorization evaluated through the canonical ownership model — cross-owner access denied and evidenced by an
ownership-isolation test; (c) credentials support revocation and expiration, demonstrated by a revoked/expired
credential being denied; (d) browser session mechanisms not accepted as machine credentials, demonstrated by a
rejection test; (e) errors never leak internal engine/store/stack detail; (f) every request attributable via
correlation id in the audit trail; (g) rate-limit floor enforced deterministically. Before writes:
idempotency-key replay yields a single effect; mutation audit records actor/target/outcome; concurrent
conflicting writes resolve by the defined rule. Vague criteria ("robust", "adequate", "works") are prohibited.

## 23. Non-functional / compatibility rules

Public-contract version identity present from v1; compatibility policy stands from v1 (additive changes
preferred; breaking changes require a new version); deprecation policy exists from v1 even before any
deprecation event (documented deprecation path required before removing a public element). Core-engine
determinism preserved (public exposure adds no nondeterminism to progression/validation/activation).
Performance/scale targets (pagination, quotas) activate only on demonstrated need (§18).

## 24. Stop conditions

STOP and report at the owner decision boundary if, during any future gate: drafting/implementation exposes a
genuine contradiction with a frozen P7-B decision or an impossible acceptance criterion; a schema/endpoint/token/class
freeze appears **necessary** to accept the contract (raise as OWNER DECISION REQUIRED, do not decide silently);
the read/export scope would displace an original obligation; an external result would gain any automatic effect;
a proposed new registry/orchestrator/routing engine appears; an evidence-triggered gate is reached without its
accepted trigger actually met; or Git history shows a state-change not reflected in the roadmap. Diagnosis is
preferred over speculative resolution.

## 25. Remaining-obligation / exit-criteria review requirement

**A successful P7-I3 does NOT make Phase 7 eligible for P7-CLOSE.** Before Phase-7 closure can be considered, a
**separate PHASE-7 REMAINING-OBLIGATION / EXIT-CRITERIA REVIEW** must classify **every** obligation in §18 as
exactly one of: **DELIVERED AND VERIFIED**; **INTENTIONALLY DEFERRED WITH CANONICAL OWNER/REASON/TRIGGER**; **NOT
APPLICABLE TO THE ACCEPTED V1 SCOPE — OWNER ACCEPTED**; **STILL REQUIRED BEFORE PHASE-7 CLOSURE.** If any
obligation remains **STILL REQUIRED BEFORE PHASE-7 CLOSURE**, Phase 7 MUST NOT be formally closed. This §25
review holds exclusive authority over each obligation's final closure classification; §18 pre-judges none. The
Standing Phase-7 Authorization authorizes P7-CLOSE only if this review's closure criteria are satisfied.

## 26. Explicitly deferred items

Subsystem public API/durable identity; async/job/webhook infrastructure and naming; write/import surfaces and
import contract/version identity; inbound-result persistence/review and its schema/location/retention/deletion/record-type;
pagination; quotas beyond the protective floor; advanced async retry; real-vendor/sandbox integration and vendor
selection; embedded integration; partner connectors; file exchange as a governed import; extended monitoring/abuse
controls; final endpoint/route/method/JSON/DB/class/module/token/error-code/vendor schemas. Each retains canonical
owner + reason + activation trigger + closure effect reserved for §25 (§18).

## 27. Owner authorization matrix

Column "Authorized by the P7-C contract itself?" answers whether *this document* confers the authorization;
implementation authority for Phase-7 gates flows from the separate Standing Phase-7 Authorization (`D-P7-STANDING-01`).

| Item | Authorized by the P7-C contract itself? | Authorizing source |
|---|---|---|
| Publish P7-C as governance contract-of-record | YES (this gate) | `G-P7C-FORMAL-PHASE-7-CONTRACT-PUBLICATION-01` / `D-P7C-01` |
| P7-I1 internal seam | NO | Standing Phase-7 Authorization (`D-P7-STANDING-01`) + bounded P7-I1 contract |
| P7-I2 public API + security | NO | Standing Phase-7 Authorization + bounded contract |
| P7-I3 adapter proof | NO | Standing Phase-7 Authorization + bounded contract |
| Write/import gate | NO | Standing Phase-7 Authorization, on accepted trigger |
| Inbound-result persistence/review | NO | Standing Phase-7 Authorization, on accepted trigger |
| Subsystem durable identity/API | NO | Standing Phase-7 Authorization, on accepted trigger |
| Async/webhook | NO | Standing Phase-7 Authorization, on accepted trigger |
| Real-vendor integration | NO | Standing Phase-7 Authorization, on accepted trigger |
| P7-CLOSE | NO | Standing Phase-7 Authorization, after §25 exit-criteria review |
| Phase 8 / 9 / 10; separately governed CAP/AISR/QTA/ACV/WS17/STG/PDF/Email/Output-Language; domain activation outside Phase-7 scope | NO | Not authorized by any current decision |

## 28. Material risks

UI-shaped API (mitigated §7/§8); vendor-shaped core (§12); browser-auth-as-machine-auth (§9/§22d); premature
subsystem freeze (§14/§12 guard); premature async (§15); premature import/write contract (§11/§16); external-result
trust bypass (§13); security under-design (§10/§22); unnecessary public-resource expansion (§7); schema/endpoint
freeze (§4 freeze-limit); duplicated architecture (§17); CAP/workstream absorption (§17); original-obligation
displacement (§18/§25); false closure readiness (§25); standing-authorization treated as active increment (§29);
Phase-8/9/10 scope creep (§4/§27). Each bounded by the cited section; none unmitigated.

## 29. Owner decision status

**OPEN ARCHITECTURAL DECISIONS: NONE.** The owner has **ACCEPTED** this contract (`D-P7C-01`) and has separately
granted a **Standing Phase-7 Authorization** (`D-P7-STANDING-01`) to complete remaining Phase-7 work through formal
closure, subject to this contract's boundaries, per-gate bounded scope, accepted evidence triggers, tests, Lean
minimum-path, independent review where required, and the §25 exit review. **Standing authorization ≠ active
implementation increment:** implementation of P7-I1 begins only once its bounded increment contract/scope has been
established from this document and its live base verified. Current active implementation = **NONE**; the bounded
P7-I1 increment contract is **NOT YET ESTABLISHED**; P7-I1 implementation is **NOT STARTED**.

## 30. Verdict

This contract formalizes the frozen P7-B decisions and both accepted correction addenda, preserves every original
Phase-7 obligation with §25-reserved closure classification, defines observable/testable per-gate acceptance and
security criteria, enforces the §25 exit-criteria review to prevent false closure, freezes no implementation detail,
and confers no implementation authority of its own.

**P7-C STATUS:** OWNER ACCEPTED — PUBLISHED AS CONTRACT OF RECORD. **MATERIAL CONTRADICTIONS:** NONE.
**LATEST OWNER AUTHORIZATION:** Standing Phase-7 Authorization through formal closure (`D-P7-STANDING-01`), subject to
contract boundaries and evidence conditions. **P7-I1:** authorized under standing authority; bounded increment contract
NOT YET ESTABLISHED; implementation NOT STARTED. **CURRENT ACTIVE IMPLEMENTATION:** NONE. **PHASE 8/9/10 / DEPLOYMENT /
SEPARATELY GOVERNED CAPABILITIES:** NOT AUTHORIZED. **MANDATORY STOP:** P7-C PUBLICATION / OWNER MERGE BOUNDARY.
