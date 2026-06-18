# STRATEGIC_PRODUCT_VISION.md

**Document type:** Strategic governance — Level 0 Authority
**Version:** 1.0 Final
**Date:** 2026-05-31
**Status:** APPROVED FOR REPOSITORY ADMISSION
**Prepared by:** Agent (Phase C)

---

## STAGE 2 CLOSURE SUMMARY

**What Stage 2 established:**
Stage 2 produced the governance foundation required before domain expansion can proceed. It established the strategic identity of InventorAI, defined what the platform measures and what it must never become, locked the owner's vision as a binding governance constraint, classified the four dimensions of inventor progression, defined how domain packs must be structured and governed, and recorded all open questions that were deferred with explicit basis.

**What Stage 2 intentionally deferred:**
Stage 2 deferred all OQ-S2 questions to v1.1 after evidence review confirmed no runtime constants correspond to those questions. It deferred the sandbox validation environment, the deprecation policy, and all commercial architecture implementation. It did not defer the commercial architecture preservation constraint — that constraint is active from this document forward.

**Why Stage 3 is now unblocked:**
Stage 3 (Domain Validation) requires two things before it can proceed: committed governance documents that define what a valid domain pack is, and resolution of AB-001 and AB-005. Stage 2 produces the first requirement. AB-001 and AB-005 remain open and must be resolved with explicit owner authorization before any domain expansion begins. Stage 3 planning may now begin. Stage 3 execution remains blocked until AB-001 and AB-005 are resolved.

---

## PROVENANCE RECORD

| Section | Classification |
|---------|---------------|
| 1. Platform Identity | Repository Derived |
| 2. Owner Vision Lock | Owner Decision (2026-05-31) |
| 3. Owner Vision Statement | Repository Derived |
| 4. What InventorAI Is Not | Repository Derived + Owner Extension |
| 5A. Platform Success Definition | Repository Derived |
| 5B. FDC-001 Classification | Repository Derived + Owner Extension |
| 6. Layered Evolution Model | Repository Derived + Owner Extension |
| 7. Core Governance Principles | Repository Derived |
| 8. Current Scope and Frozen Decisions | Repository Derived |
| 9. Deferred Scope | Repository Derived + Owner Extension |
| 10. Evidence and Ownership as Strategic Differentiator | Owner Decision (2026-05-31) |
| 11. Commercial Architecture Preservation | Owner Decision (2026-05-31) |
| 12. Authority Hierarchy | Repository Derived + Owner Extension |

---

## 1. PLATFORM IDENTITY

> **GOVERNING EFFECT AMENDED**
> The governing effect of this section has been amended by the active
> Level 0 Owner Amendment: `docs/governance/OWNER_PRODUCT_IDENTITY_CORRECTION.md`.
> Read that document before relying on the wording below. Where wording
> conflicts, the Owner Amendment governs. The original text is retained
> for historical provenance. This notice does not modify execution gates,
> holds, or authorization status.

*Provenance: Repository Derived*

**InventorAI is not an idea evaluator.**
**InventorAI is not an AI assistant.**
**InventorAI is not a product generator or business plan tool.**
**InventorAI is a deterministic inventor progression platform.**
**InventorAI is a domain-agnostic structured reasoning engine.**

Primary objective: Help inventors and students avoid technical and conceptual dead ends by providing a structured reasoning process that surfaces missing knowledge, measures reasoning quality, and tracks evidence of genuine understanding.

The engine is **deterministic and replayable.**
AI is **advisory only** — it cannot gate, classify, score, or advance state.

---

## 2. OWNER VISION LOCK

> **GOVERNING EFFECT AMENDED**
> The governing effect of this section has been amended by the active
> Level 0 Owner Amendment: `docs/governance/OWNER_PRODUCT_IDENTITY_CORRECTION.md`.
> Read that document before relying on the wording below. Where wording
> conflicts, the Owner Amendment governs. The original text is retained
> for historical provenance. This notice does not modify execution gates,
> holds, or authorization status.

*Provenance: Owner Decision (2026-05-31)*

> **This section records the owner's locked strategic intent. It may not be modified by any agent, developer, or reviewer without explicit owner authorization. It exists to prevent strategic drift across development sessions.**

InventorAI's purpose is to measure and grow four things in an inventor:

1. The quality of their reasoning about why their mechanism works
2. The depth of their ownership of their own idea
3. The precision and resolvability of their identified knowledge gaps
4. Their proximity to implementation readiness

Any feature, workflow, architectural decision, or AI behavior that does not serve one of these four objectives is outside scope. Any feature that substitutes platform capability for inventor capability is a violation of this vision, regardless of its technical merit.

This vision is not a product aspiration. It is a governance constraint.

---

## 3. OWNER VISION STATEMENT

> **GOVERNING EFFECT AMENDED**
> The governing effect of this section has been amended by the active
> Level 0 Owner Amendment: `docs/governance/OWNER_PRODUCT_IDENTITY_CORRECTION.md`.
> Read that document before relying on the wording below. Where wording
> conflicts, the Owner Amendment governs. The original text is retained
> for historical provenance. This notice does not modify execution gates,
> holds, or authorization status.

*Provenance: Repository Derived — STATE_FREEZE Section 11, GOVERNANCE-ROADMAP Priority 7*

The long-term objective is not to build a session completion tool.

The objective is to build a **structured inventor reasoning platform** that helps inventors progressively develop understanding, identify knowledge gaps, acquire evidence, and reach implementation readiness through a deterministic progression journey.

The platform measures four dimensions of inventor progression:

1. **Reasoning evidence growth** — the inventor's ability to articulate *why* their approach works
2. **Ownership evidence growth** — the inventor's demonstrated understanding of their own idea
3. **Gap evolution** — how identified knowledge gaps are surfaced, tracked, and closed over time
4. **Progressive knowledge acquisition** — measurable deepening of domain understanding across iterations

The long-term goal is to help inventors think more clearly, define ideas more rigorously, and make better decisions over time — not simply to complete sessions.

A platform that helps inventors complete sessions is different from a platform that helps inventors become better inventors. InventorAI must be the second.

---

## 4. WHAT INVENTORAI IS NOT

*Provenance: Repository Derived + Owner Extension*

| False Description | Correct Description |
|------------------|---------------------|
| Idea scoring tool | Progression quality measurement engine |
| AI assistant | Deterministic structured reasoning platform |
| Idea generator | Inventor reasoning mirror |
| Session completion system | Evidence and ownership growth tracker |
| Domain expert | Gap identification and tracking layer |
| Feasibility oracle | Knowledge gap surface engine |
| Implementation readiness certifier | Reasoning quality assessor |
| Regulatory or compliance guide | Structured reasoning journey engine |

### Coverage Declaration Principle

*Provenance: Owner Decision (2026-05-31)*

InventorAI evaluates the quality of an inventor's reasoning about their mechanism. It does not evaluate, certify, or assess:

- Regulatory approval or compliance
- Certification requirements
- EMC or electromagnetic compatibility
- Manufacturing readiness
- Supply chain viability
- Commercial viability
- Build readiness
- Any domain-specific execution requirement outside structured reasoning quality

Completing an InventorAI session does not constitute validation of an invention for any purpose outside the platform. Domain packs must declare their covered areas, not-covered areas, and known limitations explicitly. No domain pack may imply coverage it does not provide.

---

## 5A. PLATFORM SUCCESS DEFINITION

> **GOVERNING EFFECT AMENDED**
> The governing effect of this section has been amended by the active
> Level 0 Owner Amendment: `docs/governance/OWNER_PRODUCT_IDENTITY_CORRECTION.md`.
> Read that document before relying on the wording below. Where wording
> conflicts, the Owner Amendment governs. The original text is retained
> for historical provenance. This notice does not modify execution gates,
> holds, or authorization status.

*Provenance: Repository Derived — STATE_FREEZE Section 11, GOVERNANCE-ROADMAP Priority 7*

A successful InventorAI journey is **not** defined by:
- Idea approval
- Positive scoring
- Domain completion
- Protocol completion
- Session completion rate

A successful journey is defined by **measurable growth** in:

- **Reasoning Evidence** — demonstrable improvement in the inventor's ability to justify their approach
- **Ownership Evidence** — demonstrable improvement in the inventor's understanding of their own idea
- **Gap Quality** — identified gaps become more precise, actionable, and resolvable over time
- **Implementation Readiness** — the inventor moves closer to a state where they can act on their idea

**The platform evaluates progression quality, not idea quality.**

---

## 5B. FDC-001 CLASSIFICATION

*Provenance: Repository Derived + Owner Extension — STATE_FREEZE: "ILT-001 proved session progression. It did not prove inventor development."*

FDC-001 is the deliverable produced at the end of a completed InventorAI session. Its scope is explicitly bounded.

| Dimension | Status | Basis |
|-----------|--------|-------|
| Protocol Completion | PROVES | Inventor traversed all gaps in sequence |
| Response Quality per Gap | PROVES | ASSERTED vs REASONED classification per iteration |
| Inventor's Own Words | PROVES | idea_summary not AI-generated or overwritten after first capture |
| Domain Validation | DOES NOT PROVE | Not validated against real domain expert review |
| Inventor Development | DOES NOT PROVE | Session completion does not equal inventor improvement |
| Implementation Readiness | DOES NOT PROVE | No connection between FDC-001 and ability to build |
| Build Readiness | DOES NOT PROVE | Outside platform scope |
| Regulatory Compliance | DOES NOT PROVE | Outside platform scope |
| Knowledge Ownership (full) | PARTIAL | Record is inventor's words; AI Echo not yet detectable |

FDC-001 is an honest evidence record of what was demonstrated in one session. It is not a validation certificate, a feasibility report, or an implementation plan.

---

## 6. LAYERED EVOLUTION MODEL

*Provenance: Repository Derived + Owner Extension. Layer taxonomy is Owner Extension (2026-05-31). Layer 4 reclassified per RD-001. Layer 3 clarified per FR-001. Layer 5 clarified per FR-002.*

InventorAI's value proposition evolves across five layers. The layers are not strictly sequential — Layer 4 is implemented before Layer 3 is fully defined.

| Layer | Name | Description | Current Status |
|-------|------|-------------|---------------|
| 1 | Protocol Completion | Inventor can complete a structured gap progression session | IMPLEMENTED |
| 2 | Domain Validation | Session outcome reflects genuine domain knowledge, not surface compliance | IN PROGRESS — blocked AB-001, AB-005 |
| 3 | Implementation Readiness | Inventor reaches a state where they can act on their idea | NOT STARTED |
| 4 | Evidence and Ownership | Inventor's progression record is verifiably theirs and measures genuine growth | IMPLEMENTED IN ENGINE — governance documentation pending (this document) |
| 5 | Institutional / Commercial Ecosystem | Platform adopted within organizations and inventor development pipelines | NOT STARTED — Stage 6 |

**Layer 3 — Implementation Readiness Characterization:**
Layer 3 is reached when an inventor can: identify at least one concrete next action, name their remaining unknowns with precision, define a proof-of-concept objective that would validate or refute their core mechanism assumption, and articulate how their uncertainty has reduced since the session began. Layer 3 is not implied by Layer 1 completion alone.

Reaching Layer 3 also requires that the inventor can articulate *why* their identified next action takes priority over alternative actions — not only what the action is. Without this, implementation readiness remains fragile and subject to technical and conceptual drift at the first obstacle.

**Layer 4 — Note:**
The engine enforces ownership principles today — `idea_summary` is not AI-generated, progression credit belongs to the inventor, replay is deterministic, and FDC-001 records only the inventor's own expressed reasoning. What was absent is committed governance documentation. This document, once committed, closes the governance gap for Layer 4.

**Layer 5 — Scope Clarification:**
Layer 5 concerns the adoption of InventorAI as a platform within organizations, institutions, and inventor development pipelines. It does not constitute validation of inventions for commercial, regulatory, or investment purposes. InventorAI at Layer 5 remains a reasoning journey platform. The institutional context changes who uses it and how it is deployed — not what it measures or what it proves about any invention.

**Current milestone:** Stage 2 Governance Stabilization — establishing the standards that enable Layers 2 and 4 to be formally declared complete.

---

## 7. CORE GOVERNANCE PRINCIPLES

*Provenance: Repository Derived — STATE_FREEZE Section 11*

These principles are permanent governance constraints. Any agent, developer, architect, or reviewer working on InventorAI must treat these principles as binding. A proposed change that violates any of these principles must be rejected regardless of its apparent technical merit.

### Principle 1 — Inventor Ownership

**The inventor owns the idea and the reasoning. The platform owns the structure and the questions. These two ownership domains must never be merged.**

The platform may question, challenge, structure, and identify gaps in an inventor's expressed reasoning. It may not fill those gaps on the inventor's behalf. It may not invent missing knowledge, supply missing mechanism steps, generate plausible-sounding explanations, or complete partial reasoning to make an inventor appear more advanced than they demonstrated.

Progression credit belongs exclusively to the inventor. It is awarded when, and only when, the inventor's own expressed words satisfy the quality threshold the protocol defines.

**What this principle forbids:**
- The AI suggesting mechanism steps the inventor has not articulated
- The platform completing a gap on behalf of an inventor who cannot answer
- Advancement credit awarded based on iteration count rather than demonstrated quality
- Any framing that presents AI-generated content as inventor-demonstrated understanding

### Principle 2 — Improvement, Not Generation

**InventorAI improves inventors. It does not generate inventions, mechanisms, products, or technical answers for inventors who cannot provide them.**

The platform is a structured mirror that reflects the inventor's own reasoning back to them at increasing levels of precision. It is not a creativity tool, product design tool, business plan generator, or substitute for engineering knowledge.

**What this principle forbids:**
- Using InventorAI as an idea generation tool
- Using InventorAI as a product generator or business plan generator
- Platform-generated technical content being presented as session progress
- Completion experiences that do not reflect actual demonstrated quality

**The correct success state:** The platform succeeds when an inventor leaves with a more precise articulation of what they understand, a clear identification of what they do not yet understand, and an honest record of what was demonstrated.

### Principle 3 — Multi-Domain Integration Vision

**The long-term vision is integrated cross-domain understanding of one product — not parallel single-domain analyses of separate components.**

Real inventions span multiple domains. The intended vision is to help an inventor understand how multiple domains contribute to one integrated product and identify the gaps at those intersections.

**What this principle requires of future architectural decisions:**
- Multi-domain architecture must reason about domain intersections, not only domain membership
- The gap discovery layer must eventually identify gaps that exist between domains
- The FDC-001 deliverable must eventually represent a cross-domain concept
- Domain classification must eventually support multi-domain assignment

---

## 8. CURRENT SCOPE AND FROZEN DECISIONS

*Provenance: Repository Derived — STATE_FREEZE Sections 13 and 16, GD-001*

### Frozen In — MVP Scope

- Electronics/electrical domain — the only validated domain
- LEVEL 0, 1, 2 maturity progression only
- Three gap types: MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY
- Deterministic progression engine — no AI advancement decisions
- FDC-001 deliverable with honest deferred sections
- In-memory session storage

### Frozen Decisions — Must Not Be Reopened Without New Evidence

**GD-001 (Adopted 2026-05-29):** The inventor journey is a three-stage architecture. The three-gap mechanism knowledge assessment is Stage Two and must not be modified to absorb situational knowledge. This decision is frozen and must not be reopened without new evidence.

Three situational knowledge concepts are explicitly excluded from Stage Two gap types:

| Concept | Correct Location |
|---------|----------------|
| Problem-Mechanism Fit | Stage One and Stage Three |
| Assumption Inventory | Stage One (surfacing); Stage Three (reassessment) |
| Expertise-Gap Awareness | Stage Three |

**What GD-001 forbids:**
- Adding PROBLEM_MECHANISM_FIT, ASSUMPTION_INVENTORY, EXPERTISE_GAP as Stage Two gap types
- Modifying the gap architecture to ask situational knowledge questions
- Any future gap type addition that does not assess a dimension of mechanism knowledge

---

## 9. DEFERRED SCOPE

*Provenance: Repository Derived + Owner Extension — STATE_FREEZE Section 15, RD-003*

| Item | Deferral Reason |
|------|----------------|
| ODS-001 | Options Database — post-MVP |
| Component Summary | Requires ODS-001 |
| Second Domain | MVP is electronics/electrical only |
| Web and Supabase Persistence | In-memory sufficient for MVP |
| Production Hardening | Post-MVP |
| CI Pipeline | Post-MVP |
| Stage One — Situational Orientation | Design post-MVP |
| Stage Three — Deliverable Reflection | Full implementation post-MVP; FDC-001 basic output is MVP-required |
| Structured Review Lifecycle | Not implemented, not validated |
| Expert Review Flow | Not implemented, not validated |
| Feedback-to-Revision Loop | Not implemented, not validated |
| Sandbox / Simulation Experience | Strategic visibility only — not scoped for v1.0. Relevant to Layer 3 planning and domain pack sandbox validation environment. To be specified in v1.1 |
| Institutional / Commercial Ecosystem | Stage 6 — NOT STARTED. Commercial architecture preservation constraint is active now (see Section 11) |

---

## 10. EVIDENCE AND OWNERSHIP AS STRATEGIC DIFFERENTIATOR

*Provenance: Owner Decision (2026-05-31)*

General-purpose AI systems optimize for response quality and user satisfaction. InventorAI optimizes for verified growth in inventor understanding, ownership, and readiness.

| Dimension | General-Purpose AI | InventorAI |
|-----------|-------------------|------------|
| Success metric | Response quality | Inventor progression quality |
| Content ownership | AI-generated | Inventor-demonstrated |
| Advancement criterion | Engagement | Demonstrated understanding |
| Session outcome | Completed interaction | Verifiable evidence record |
| Knowledge source | AI knowledge base | Inventor's own expressed reasoning |

This distinction is a governance contract. Any implementation that blurs the boundary between AI-generated content and inventor-demonstrated understanding violates Principle 1 and must be rejected regardless of its apparent benefit.

---

## 11. COMMERCIAL ARCHITECTURE PRESERVATION

*Provenance: Owner Decision (2026-05-31)*

Commercial architecture is intentionally deferred to Stage 6. This deferral is a sequencing decision, not an architectural exclusion.

**No architectural decision may be made that structurally forecloses:**
- Individual user accounts
- Organizational or team hierarchy
- Subscription-based or usage-based access models
- Enterprise adoption with data isolation requirements

Any architectural proposal that would require significant re-engineering to support these capabilities must flag this risk explicitly before owner approval is sought. This requirement is active from this document forward. It does not require immediate implementation of any commercial feature.

**Separation of commercial requirements from progression integrity:**

Commercial architecture requirements — including subscription models, organizational tiers, enterprise customization, or usage metrics — may not influence:
- Reasoning quality assessment
- Progression scoring or advancement criteria
- Ownership attribution
- Any governance decision

Monetization pressure is not a valid basis for altering how the platform measures inventor progression. A commercial deployment that requires softening quality thresholds, adjusting advancement criteria, or attributing platform-generated content to inventors is incompatible with this platform's governance and must be rejected.

---

## 12. AUTHORITY HIERARCHY

*Provenance: Repository Derived + Owner Extension*

```
Level 0 — Strategic Vision (this document)
  STRATEGIC_PRODUCT_VISION.md
  Defines what InventorAI is, what it measures, and what it must never become

Level 1 — Domain Governance Standard
  DOMAIN_PACK_GOVERNANCE_STANDARD_v1.md
  Defines how domains are validated and maintained

Level 1 — Journey Architecture
  SA-001A_JOURNEY_ARCHITECTURE_SPECIFICATION.md
  Defines platform stage model, stage boundaries, evaluation
  rule governance across stages, and AB-006-A architectural
  direction
  Added: 2026-06-02, SA-001 authorization

Level 1 — Governance Note
  Level 1 documents are permanent peer authorities. Each governs
  a distinct architectural domain. A new Level 1 document requires
  explicit owner authorization and must govern a domain not already
  covered by an existing Level 1 document. Level 1 documents do not
  subordinate each other unless this section explicitly records a
  precedence relationship. Conflicts between Level 1 documents that
  cannot be resolved by reference to Level 0 require an explicit
  owner decision before any implementation proceeds.
  Level 1 — Domain Model
  SA-001B_DOMAIN_MODEL_SPECIFICATION.md
  Defines domain family model, parent/child inheritance,
  coverage declaration governance, electronics as first
  parent domain, and AB-006-B governing position
  Added: 2026-06-02, SA-001 authorization
Level 2 — Master Reference
  MASTER-HANDOVER.md
  Defines current repository state and authorized work

Level 3 — Committed Governance Artifacts
  All documents in docs/governance/ with ACTIVE status

Level 4 — Repository Evidence
  git history, benchmark results, engine code

Level 5 — Chat Discussions
  Non-authoritative
```

---

*This document is produced to be accurate, not reassuring.*
*Repository evidence takes precedence over chat history at all times.*
*No implementation without evidence. No evidence without repository inspection.*
