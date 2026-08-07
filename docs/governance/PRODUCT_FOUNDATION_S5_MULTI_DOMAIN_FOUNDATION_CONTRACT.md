# Product-Foundation §5 — Multi-Domain and Technology Capability Foundation — Contract of Record (§5-C1)

Gate: `G-S5-C1-MULTI-DOMAIN-FOUNDATION-CONTRACT-01` — **governance / documentation only**.
Status: **CONTRACT OF RECORD — DEFINITION ONLY. AUTHORIZES NO IMPLEMENTATION.**

Classification: documentation-only contract-definition + owner-decision record. It records
owner decisions and a bounded future plan; it makes no runtime/code/web/test/schema/migration/
dependency/CI change, activates no domain, and starts no implementation increment. Recording a
future increment here authorizes nothing — each future increment requires separate explicit owner
authorization.

Repository truth overrides conversation, handover, memory, inference, and proposal.

Authoritative integration branch: `feature/atomic-json-session-persistence`
Contract basis tip: `a9bead4b4eec6568613211d77f6d6e80a2eae752` (PR #391 — Phase-6 formal closure
merge; parents `9665413` + `0254240`; tree `ed6786b`). `main` is out of scope.

---

## 0. Naming discipline (mandatory — read first)

Three historically overlapping "Phase 6" concepts exist and must never be conflated:

- **(A) Executed Phase-6 lane — Domain Specialization / Truthful Specialist Labeling (Option A):
  FORMALLY CLOSED** (`PHASE_6_DOMAIN_SPECIALIZATION_FORMAL_CLOSURE_RECORD.md`; D-P6-CLOSE).
- **(B) Product-Foundation §5 — Multi-Domain and Technology Capability Foundation:** the program
  THIS contract scopes. Distinct future program; **not** activated by this contract.
- **(C) Historical registry-parity "Phase 6"** (`docs/GOVERNANCE_DOCUMENTS.md`, 23/23 parity):
  a distinct historical/registry-reconciliation track. Per D-P6-00, none of these authorizes the
  others.

This contract governs (B) only.

## 1. Purpose

Give InventorAI a **truthful, extensible multi-domain and technology-capability foundation** — so
the platform can *later* support additional domains and cross-cutting technology capabilities
without core rewrites — **before** any new domain is activated. Foundation only: extensibility,
contracts, and resource boundaries. It builds the ability to extend; it does **not** turn on any
new domain.

## 2. Scope

Definition of: the canonical Domain Registry role; the domain-pack contract; the capability model;
the project↔domain relationship and subsystem model; the domain-specific evidence/risk/validation
contract boundary; the specialist-category boundary; unsupported-domain semantics; activation-status
semantics; compatibility expectations; the no-core-domain-name-branching principle; the D-P6-14
relationship; the Phase-7 handoff boundary; migration/back-compat principles; and the sequenced,
independently-reviewable future implementation increments (§5-I1 … §5-CLOSE).

## 3. Exclusions (this contract does NONE of these; each is separately gated)

No implementation of anything; no Domain Registry hardening (D-P6-14); no Technology Capability
Registry; no activation-status logic; no cross-domain project or subsystem code; no domain-specific
schema/evaluator; no capability packs; no activation of `mechanical` / `medical_device` /
`software` / `iot_electronics` / IoT / any new domain; no Phase 7 / API definition beyond the §5
handoff boundary; no QTA, WS17/AI Coach, Output-Language, STG, ACV, PDF/download, output email, or
CAP-01…CAP-14; no schema/migration/dependency/CI/test change; no new tracker/roadmap/matrix/taxonomy
(D-FPC-MAP-06). Permitted repository paths for the §5-C1 candidate: `docs/governance/**` only.

## 4. Architecture principles (binding on every future §5 increment)

FOUNDATION ≠ ACTIVATION · REGISTERED ≠ USER-ACTIVE · DOMAIN PACK ≠ AUTOMATIC DOMAIN ENABLEMENT ·
CONTRACT ACCEPTANCE ≠ IMPLEMENTATION AUTHORIZATION · PHASE-7 HANDOFF ≠ PHASE-7 START · DISCOVERY ≠
IMPLEMENTATION · RECORDED ≠ AUTHORIZED. Reuse existing canonical architecture (the working Domain
Registry and v1.0 packs); introduce no parallel abstraction framework; keep changes additive and
backward-compatible; keep only `electronics_electrical` user-active until a separate Phase-9
activation gate says otherwise; preserve product identity (structured reasoning assistance, **not**
professional/licensed certification).

## 5. Owner decisions (recorded; `D-S5-01 … D-S5-09`)

Recorded via the §5-C1 owner-decision gate (decision package + explicit owner selection). Full
option/benefit/risk analysis is in the ODR and the roadmap entry; the chosen positions:

- **D-S5-01 — Registry authority = Option C.** One canonical **Domain Registry**
  (`engine/domain_registry.py`) remains the runtime domain authority. Capability definitions live
  **inside domain packs** (a reserved capability-reference slot), with **no** separate global
  capability registry now; promotion to a separate registry (Option B) stays an additive, reversible
  future step gated by D-S5-02.
- **D-S5-02 — Technology Capability model = references now, registry later (Option C→B, evidence-
  gated).** Represent capabilities as a **thin normalized reference vocabulary** referenced by packs;
  build a separate Technology Capability Registry or capability packs **only** when a second
  activated domain genuinely reuses a capability. No capability ontology is built now.
- **D-S5-03 — Activation-status semantics = Option A + separate activation policy.** Pack `status`
  denotes **loader/lifecycle validity only** (`registered` / `deprecated`), **not** user activation.
  Runtime user-activation becomes an **explicit, separate, server-side activation policy**
  (allowlist). `mechanical` / `medical_device` / `software` remain **registered-but-not-user-active**;
  the current electronics-only behavior **must not be silently broadened**.
- **D-S5-04 — Cross-domain project model = Option D.** The project stays **generic** with today's
  single primary `confirmed_domain` preserved as the default/back-compat; **multi-domain lives at the
  subsystem grain** (D-S5-05). Multiple peer root domains (Option C) are rejected (breaks
  deterministic single-domain evaluation; no evidenced need). This is the extensible target,
  implemented **additively**.
- **D-S5-05 — Subsystem model (required by D-S5-04).** Conceptual contract only: a subsystem =
  `{ immutable system-generated subsystem_id, user-defined display name, parent project, one primary
  domain, optional capability references, its own evidence / gaps / risks / validation }`. Both an
  immutable id and a display name; deterministic id. No schema/code here.
- **D-S5-06 — Unsupported / partial domain behavior = preserve + formalize truthfully.**
  not-registered → **General idea review** fallback; registered-but-not-activated → General review +
  a truthful "not yet supported for specialized review" notice (capture allowed, no specialist
  claim); experimental/partial or missing-capability → bounded general analysis, **never** a
  specialist/professional claim. Preserves the non-certifier identity and the P6-1 "never silently
  electronics" rule.
- **D-S5-07 — Specialist-category model = pack metadata + presentation.** Specialist category is
  **domain-pack metadata consumed by the presentation layer** (reuse the P6-1 `web/domain_label.py`
  seam). **No** separate specialist registry. **Tier 3 (Specialist) / Tier 4 (Licensed) remain
  PROHIBITED**; Tier 0–1 only, per the closed executed lane.
- **D-S5-08 — Phase-7 handoff boundary.** §5 must stabilize accepted **resource-boundary contracts
  (not endpoints)** for: project identity, domain identity, capability identity/reference, subsystem
  identity, evidence, gaps, risks, validation requirements, activation/support status, and
  unsupported-domain states. §5 does **not** define API endpoints or start Phase 7.
- **D-S5-09 — Phase-6 naming seam.** Smallest documentation correction only: add explicit
  supersession/context labels (no history rewrite) where the three "Phase 6" concepts could be
  confused — the Product-Foundation plan (§5 header + stale §11/§12 status) and
  `docs/GOVERNANCE_DOCUMENTS.md` (registry-parity annotation). A bounded, separately-tracked future
  documentation-sync; not a broad plan rewrite.

## 6. Canonical Domain Registry role (D-S5-01)

`engine/domain_registry.py` is the single runtime domain authority: it loads v1.0 domain packs from
`domains/`, validates them, and exposes `get_domain` / `list_domains`. It is authoritative
configuration consumed via `engine/domain_rules.py` for classification / substance signals / rules /
domain-specific questions. §5 extends this registry; it does not replace or duplicate it.

## 7. Capability model (D-S5-01 / D-S5-02)

Capabilities are **referenced from domain packs** via a normalized reference vocabulary. No global
Technology Capability Registry and no capability packs are built now (**capability-pack policy: B/C
— optional/future; references sufficient**). The pack contract (§8) reserves an optional
`capability_refs` slot so a future registry is additive.

## 8. Domain-pack contract (formalizes the existing v1.0 packs; backward compatible)

Do **not** replace the existing v1.0 format. Formalize it:

- **Required fields:** `schema_version`, `pack_id`, `version`, `status`, `display_name`,
  `classification_signals`, `substance_signals`, `gap_type_mappings`, `rule_nuances`, **and a
  governance/provenance block** (`source`, `license`, `owner`, `review_date`, `version`,
  `deprecation_status`) — currently **absent** on all four active packs (this is the concrete
  D-P6-14 gap).
- **Optional fields:** `aliases`, `parent_pack_id`, `authorized_child_domains`, `domain_family_role`,
  `coverage_declaration`, `journey_extension`, `capability_refs` (D-S5-02), specialist-category
  metadata (D-S5-07).
- **Identity rules:** `pack_id` unique and collision-checked; `aliases` unique across packs.
- **Versioning rules:** pack `version` semver; governance `version` semver; `review_date` ISO-8601.
- **Status rules (D-S5-03):** `status ∈ {registered, deprecated}` = loader/lifecycle validity only;
  **not** activation. Allowed-value enforcement is added in §5-I1.
- **Alias rules:** aliases resolve to exactly one `pack_id`; collisions rejected.
- **Parent/child rules:** `parent_pack_id` / `authorized_child_domains` / `domain_family_role`
  describe family structure only; they activate nothing.
- **Capability references:** optional `capability_refs` naming normalized capability tokens.
- **Domain-specific extension fields:** namespaced, additive, non-breaking.
- **Provenance / governance metadata:** required (above).
- **Backward compatibility:** existing v1.0 packs remain valid after additive `governance`/optional
  fields are supplied; the legacy `iot_electronics` pack (`schema_version` ≠ "1.0") stays
  evidence-only — skipped by the loader, neither migrated nor activated here.

## 9. Project ↔ domain relationship & subsystem model (D-S5-04 / D-S5-05)

Project stays generic; single primary `confirmed_domain` preserved (back-compat, deterministic).
Multi-domain is expressed by **subsystems** (conceptual contract in D-S5-05), added additively in a
future increment with a schema-gated, legacy-safe migration. No peer root domains.

## 10. Domain-specific evidence/risk/validation contract boundary

Packs already carry domain-specific questions (`gap_type_mappings`), rule modifiers
(`rule_nuances`), and signals. §5 defines the **generic contract boundary** for domain-specific
evidence/risk/validation so the deterministic engine stays domain-agnostic (reads pack data, no
domain names in core). Concrete schemas are later, evidence-gated increments — not defined here.

## 11. Unsupported-domain & activation-status semantics

Per D-S5-06 and D-S5-03: activation is an explicit separate policy; unsupported/partial states are
truthful and never overclaim. Compatibility expectations (§15): a registry-parity/compatibility test
suite must prove packs load, validate, resolve, and that activation policy gates correctly, with no
silent activation.

## 12. No-core-domain-name-branching principle (migration principle, not implementation)

- **ALLOWED:** presentation labels (P6-1); domain-owned pack content; explicit bounded adapter/
  boundary logic where justified; tests/fixtures.
- **DISALLOWED (to be reduced over §5 increments):** central orchestration branching that should
  resolve via registry metadata; capability selection via repeated hard-coded domain switches;
  hidden activation decisions outside the canonical registry/activation policy.
- Current hard-coded electronics branching (web activation layer, `safety_signal._MVP_DOMAIN`,
  `path_n_questions` electronics file, the `infer_domain` priority list) is **legitimate MVP
  electronics-only activation today**; §5-I2 migrates the activation decisions to the registry/policy.
  No remediation in this contract.

## 13. D-P6-14 relationship & sequencing

D-P6-14 = **Domain Registry validation hardening** — it is **registry hardening, not domain
activation**; a **prerequisite before new-domain activation** (ODR:703); and **separately authorized
implementation**. **D-P6-14 first-implementation recommendation: YES** — §5-I1 is the first
implementation gate after this contract is accepted (bounded, RED-testable, prerequisite). It is
**not** authorized by this contract.

## 14. Phase-7 handoff boundary (D-S5-08) & future domain-activation boundary

Phase 7 may freeze public API contracts only after the §5 resource-boundary contracts in D-S5-08 are
accepted. §5 does not define endpoints or start Phase 7. **New-domain activation is Phase-9/future
work**, gated per domain (owner decision + domain contract + safety/tests/review), and is **not**
authorized by §5 foundation.

## 15. Compatibility, migration & security/privacy boundary

**Compatibility:** future increments must keep existing single-domain projects valid; a
compatibility/parity test suite proves load/validate/resolve/activation-gating. **Migration:**
additive evolution only; nullable/new fields; legacy read-compatibility; deterministic
interpretation of old records; **no destructive migration without separate authorization** (no
migration designed here). **Security/privacy:** no new sensitive-data surface; activation policy is
server-side and never derived from client input; no raw invention text in logs/telemetry.

## 16. RED/GREEN expectations for future implementation

Each implementation increment is **RED-first** on the exact live parent: a genuine failing test that
encodes the missing behavior (e.g. §5-I1: packs lacking a governance block / invalid `status` /
alias collision are currently accepted → must be rejected), then focused GREEN + full-suite green,
with provenance evidence. Documentation-only gates (this one) are NO-VALID-RED.

## 17. Independent-review requirements

Every future §5 implementation increment requires independent review (A/B to publish; C blocks) with,
at minimum: no domain silently activated; registration ≠ activation preserved; no core domain-name
branching introduced; back-compat preserved; no schema change beyond the increment's authorization;
no specialist/professional overclaim; deterministic engine behavior unchanged unless explicitly
scoped; no material false-green.

## 18. Sequenced §5 implementation plan (RECORDED — each NOT AUTHORIZED; separate owner authorization required)

1. **§5-I1 — Domain Registry validation hardening (D-P6-14).** TYPE: hardening. DEPS: §5-C1
   accepted. PURPOSE: enforce required governance/provenance block, allowed `status` values,
   version-format, `gap_type_mappings`/`rule_nuances` element completeness/types, pack-id + alias
   collision detection. SCOPE: `engine/domain_registry.py`, `domains/*/domain.json` (metadata only),
   `tests/`. EXCLUSIONS: no activation, no new domain, no engine-evaluation change. RED: invalid
   packs currently accepted. GREEN: invalid packs rejected; valid packs load. INDEPENDENT REVIEW:
   YES. ROLLBACK: revert the bounded validator/metadata commit; no data migration. OWNER
   AUTHORIZATION REQUIRED: YES.
2. **§5-I2 — Activation-status policy + explicit unsupported-domain model.** TYPE: implementation
   (foundation; activates nothing new). DEPS: §5-I1. PURPOSE: introduce the server-side activation
   policy (electronics-only allowlist preserved) and the truthful unsupported/partial states (D-S5-03
   / D-S5-06); migrate hard-coded web activation to the policy. SCOPE: `engine/` activation helper,
   `web/app.py`, `tests/`. EXCLUSIONS: no new domain activated. RED/GREEN: feasible. INDEPENDENT
   REVIEW: YES. ROLLBACK: revert; policy defaults to current electronics-only. OWNER AUTHORIZATION
   REQUIRED: YES.
3. **§5-I3 — Subsystem + cross-domain project model (D-S5-04 / D-S5-05).** TYPE: implementation,
   additive + schema-gated migration. DEPS: §5-I2. PURPOSE: additive subsystem entity + subsystem↔
   domain assignment; single primary `confirmed_domain` preserved. SCOPE: `engine/record_store.py`,
   `engine/idea_state.py` / `record_contract.py`, `tests/` (+ a legacy-safe migration only if owner-
   authorized). EXCLUSIONS: no peer root domains; no destructive migration. RED/GREEN: feasible.
   INDEPENDENT REVIEW: YES. ROLLBACK: additive columns/fields; legacy read-compatible. OWNER
   AUTHORIZATION REQUIRED: YES.
4. **§5-I4 — Capability references / Technology Capability Registry (only if D-S5-02 evidence
   supports).** TYPE: implementation, evidence-gated. DEPS: §5-I3 + a second reusing domain need.
   PURPOSE: normalized capability references; promote to a registry only if justified. INDEPENDENT
   REVIEW: YES. OWNER AUTHORIZATION REQUIRED: YES. (May be skipped if unneeded.)
5. **§5-CLOSE — Multi-Domain Foundation formal closure.** TYPE: closure. DEPS: the accepted
   increments above. INDEPENDENT REVIEW: YES. OWNER AUTHORIZATION REQUIRED: YES.

## 19. §5 closure criteria (evidence-based; do NOT depend on new-domain activation)

§5 may be formally closed when the accepted-and-tested foundation contracts exist: registry
validation hardening (§5-I1); activation/support + unsupported-domain model (§5-I2); the formalized
extensible pack contract; the project/domain/subsystem resource model (§5-I3); the capability model
(references, or §5-I4 if approved); compatibility tests passing; measurable reduction of prohibited
central domain-name branching; and Phase-7-safe resource boundaries (D-S5-08) accepted. Closure
**must not** require activating any new domain.

## 20. Lean test

§5 completes **without** QTA, WS17/AI Coach, Output-Language, STG, ACV, PDF/download, output email,
CAP-01…CAP-14, Phase 7, or new-domain activation — no canonical evidence makes any of them a §5
prerequisite; each is separately gated/deferred. **PASS.**

## 21. Displacement guard

§5 is the on-critical-path original-program obligation; no owner-added capability may be inserted
ahead of it. QTA, WS17, CAP items, ACV, PDF/email, Output-Language remain separately gated. **PASS.**

## 22. Successor non-authorization

This contract authorizes **no** implementation and **no** successor gate. §5-I1 becomes eligible only
after this contract is owner-accepted and merged, and still requires separate explicit owner
authorization. No downstream activation is implied. Phase 4 & Phase 5 remain FORMALLY CLOSED; the
executed Phase-6 lane remains FORMALLY CLOSED; Decision D17 and the AISR seven-owner model are
preserved.
