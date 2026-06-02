# SA-001A — Journey Architecture Specification

**Document ID:** SA-001A
**Governance Level:** Level 1
**Status:** APPROVED
**Prepared during:** SA-001 Strategic Architecture Phase
**Date:** 2026-06-02
**Provenance:** Owner Authorization — SA-001 granted 2026-06-02, SA-001-P0 accepted 2026-06-02

---

## STAGE 2 CLOSURE SUMMARY

Produced after AB-005 closure (commit b3ccfc8) and SA-001-P0 authority mapping completion.
Does not modify any existing governance document. Extends the Level 1 authority layer with
journey architecture decisions required before AB-006 may open.

---

## PROVENANCE RECORD

| Section | Classification |
|---------|---------------|
| 1. Document Authority | Owner Authorization — SA-001 |
| 2. Inherited Level 0 Constraints | Level 0 Derived — STRATEGIC_PRODUCT_VISION.md |
| 3. Platform Stage Model | Owner Authorization — SA-001 stage naming 2026-06-02 |
| 4. Stage 1 | Repository Derived — SPV §9 Deferred Scope |
| 5. Stage 2 | Repository Derived — GD-001, SPV §8, current implementation |
| 6. Stage 3 | Repository Derived + Owner Authorization — SPV §6 Layer 3, SA-001 |
| 7. Stage 4 | Owner Authorization — SA-001 stage naming 2026-06-02 |
| 8. Stage 5 | Owner Authorization — SA-001 stage naming 2026-06-02 |
| 9. Stage 6 | Repository Derived — SPV §9, §11 |
| 10. Evaluation Rule Governance | Owner Authorization — SA-001 AB-006-A governing position 2026-06-02 |
| 11. Stage Transition Governance | Level 0 Derived — SPV §5A, §3 |
| 12. Open Questions | SA-001 scope boundary |

---

## 1. DOCUMENT AUTHORITY

### 1.1 Governance Level and Placement

Level 1 governance document under SPV §12. Sits alongside
DOMAIN_PACK_GOVERNANCE_STANDARD_v1.md at Level 1. Neither subordinates the other.
Both constrain Level 2 and below.

### 1.2 Documents This Constrains

DOMAIN_PACK_GOVERNANCE_STANDARD_v1.md — pack schemas must conform to stage architecture.
GOVERNANCE-ROADMAP.md — roadmap priorities sequenced against stage architecture.
All ADRs — no ADR may contradict stage boundaries established here.
AB-006 work items — all four decisions downstream of this document.
All future stage design documents — no stage designed without entry in this specification.

### 1.3 Documents That Constrain This

STRATEGIC_PRODUCT_VISION.md (Level 0) — §1 four-objective filter, §2 Owner Vision Lock,
§3 growth dimensions, §4 coverage declaration, §5A success definition, §7 core principles,
§8 GD-001 frozen decisions, §11 commercial architecture preservation.
ADR-002-gap-taxonomy-strategy.md and ADR-001-domain-assignment-and-multi-domain-strategy.md
are peer constraints.

### 1.4 Modification Protocol

Requires: owner authorization referencing section to be modified, evidence basis,
contradiction check against all Level 0 sections. Sections 2 and 10 carry highest
modification cost — changes require re-assessment of all downstream AB-006 decisions.

---

## 2. INHERITED LEVEL 0 CONSTRAINTS

### 2.1 Four-Objective Filter (SPV §1)

Every stage must serve at least one of: reasoning quality, ownership depth, gap precision,
implementation readiness proximity. A stage serving none has no governance basis.

### 2.2 Substitution Prohibition (SPV §1)

No stage design may substitute platform reasoning for inventor reasoning. Test: does the
capability improve the inventor's ability to reason, or does it reason on their behalf?
The second is a governance violation regardless of technical merit.

### 2.3 Session vs Development Distinction (SPV §3)

Stage exit conditions must be expressed as measurable growth in: reasoning evidence,
ownership evidence, gap evolution, progressive knowledge acquisition. Not session
completion, iteration count, or mechanical protocol closure.

### 2.4 Coverage Declaration Obligation (SPV §4)

Every domain pack must declare covered areas, not-covered areas, and known limitations
explicitly. No domain pack may imply coverage it does not provide. Applies at every stage.

### 2.5 Frozen Decisions from GD-001 (SPV §8)

Three-gap schema is Stage 2-permanent and must not be modified. Excluded from Stage 2:
Problem-Mechanism Fit, Assumption Inventory, Expertise-Gap Awareness. This document
does not reopen GD-001.

### 2.6 Commercial Architecture Preservation (SPV §11)

No stage design may foreclose: individual user accounts, organizational hierarchy,
subscription or usage-based access, enterprise adoption with data isolation.
Flag any design requiring significant re-engineering before owner approval.

---

## 3. PLATFORM STAGE MODEL

### 3.1 Stage Overview

| Stage | Name | Primary Objective Served | Status |
|-------|------|--------------------------|--------|
| 1 | Situational Orientation | Ownership depth, gap precision | Deferred post-MVP |
| 2 | Gap Discovery | Reasoning quality, gap precision | Implemented |
| 3 | Implementation Readiness | Reasoning quality, implementation readiness | Not yet designed |
| 4 | Engineering Readiness | Implementation readiness proximity | Not yet designed |
| 5 | Prototype Readiness | Implementation readiness proximity | Not yet designed |
| 6 | Commercialization and Institutional Ecosystem | All four — platform adoption context | Not started |

### 3.2 Relationship to Layered Evolution Model (SPV §6)

Stages and layers are not the same structure. Layers describe value delivered; stages
describe the inventor journey. Stage 2 maps to Layers 1-2. Stage 3 maps to Layer 3.
Stages 4-5 map to Layer 3 extended and Layer 4. Stage 6 maps to Layer 5.
Layer 4 (Evidence and Ownership) is cross-cutting — implemented in the engine at
Stage 2 and carries forward. It is not a standalone stage.

### 3.3 What Stages Are and Are Not

Stages are architectural boundaries defining what the platform evaluates, what the
inventor must demonstrate, and what governance authority applies. Not product releases,
UI flows, or session types. Stage placement is determined by demonstrated growth.

### 3.4 Multi-Domain Reasoning — Stage Placement

SPV §7 Principle 3 requires integrated cross-domain understanding as the long-term vision.
This document intentionally defers the stage placement decision for multi-domain reasoning.
Deferral basis: requires SA-001B (Domain Model Specification) which does not yet exist.
Confirmed: multi-domain reasoning is not a Stage 2 capability. Current single-domain
assignment per IdeaState is implementation state, not permanent architecture.
SA-001B owns the decision of when multi-domain reasoning enters the journey. This section
must be updated once SA-001B is committed.

---

## 4. STAGE 1 — SITUATIONAL ORIENTATION

**Purpose:** Surfaces inventor's existing situational knowledge before structured gap
discovery. Establishes baseline for measuring growth across subsequent stages.
**Objectives served:** Ownership depth, gap precision.
**Entry:** Inventor presents an invention concept. No prior interaction required.
**Exit (growth terms):** Inventor demonstrates sufficient ownership of problem context
and mechanism concept to enter domain-specific gap discovery. Not defined by idea
quality or fixed question completion.
**Status:** Deferred post-MVP per SPV §9. Characterization only — no implementation
authorized by this document.

---

## 5. STAGE 2 — GAP DISCOVERY

**Purpose:** Develops structured understanding of mechanism knowledge gaps through
domain-specific questioning. Produces verifiable evidence record.
**Objectives served:** Reasoning quality, gap precision.
**Entry:** Mechanism concept presented; domain classification performed by engine.

**Gap Type Schema — Frozen (GD-001, adopted 2026-05-29):**

- MECHANISM_COMPLETENESS — gaps in mechanism articulation
- PHYSICAL_FEASIBILITY — gaps in physical constraint understanding
- BOUNDARY_AMBIGUITY — gaps in mechanism scope definition

Excluded from Stage 2 by GD-001 — must not be added:

- Problem-Mechanism Fit — belongs to Stage 1 (surfacing) and Stage 3 (reassessment)
- Assumption Inventory — belongs to Stage 1 (surfacing) and Stage 3 (reassessment)
- Expertise-Gap Awareness — belongs to Stage 3

**Maturity Level Model:** maturity_level 0-3 is Stage 2-specific. Measures gap closure
progress within Stage 2 only. Does not represent journey stage. Must not be extended
to Stage 3+ without a new governance decision.

**Evaluation Rules:** Domain-specific. Authority in _REGISTRY[domain][substance_signals]
and _REGISTRY[domain][rule_nuances] (electronics only; others hardcoded — AB-006-A).
No stage context parameter — Stage 2 is the only implemented stage.
Current-state description, not permanent architecture.

**Exit (growth terms):** Inventor demonstrates measurable growth in reasoning quality,
ownership depth, and gap precision sufficient to indicate readiness for
implementation-oriented evaluation. Not defined by iteration count, completion metrics,
or mechanical closure of all identified gaps.

**Implementation status:** Fully implemented. AB-005 closed at b3ccfc8.
WPS001: 20 passed, 1 skipped. Guardrails: 14 passed, 1 warning.
AB-006 deferred pending SA-001 completion.

---

## 6. STAGE 3 — IMPLEMENTATION READINESS

**Purpose:** Moves inventor from structured gap awareness to implementation-oriented
evaluation. Reassesses assumptions, identifies expertise gaps, evaluates readiness
for concrete next actions.
**Objectives served:** Reasoning quality, implementation readiness proximity.
**Entry:** Derives from Stage 2 exit — demonstrated measurable growth in reasoning,
ownership, and gap precision.

**What Stage 3 must accomplish that Stage 2 does not:**

1. Problem-Mechanism Fit — does the mechanism address the intended problem?
2. Assumption Inventory — which underlying assumptions are unvalidated?
3. Expertise-Gap Awareness — what domain expertise does the inventor lack?

Must produce SPV §6 Layer 3 characterization: inventor identifies a prioritized next
action with justification, names remaining unknowns with precision, defines a
proof-of-concept objective, articulates how uncertainty has reduced.

**Gap types at Stage 3:** Not yet defined. Confirmed: Problem-Mechanism Fit,
Assumption Inventory, Expertise-Gap Awareness. Complete set requires Stage 3 design
authorization.

**Evaluation Rules — AB-006-A Governing Position:**

Evaluation rules are stage-specific in principle. The concepts excluded from Stage 2
by GD-001 imply different reasoning structures at different stages. Substance signals
constituting REASONED quality for Stage 2 gap types are not necessarily sufficient
for Stage 3 gap types. Therefore: stage-aware evaluation governance is expected in
the future architecture.

**Exit (growth terms):** Inventor demonstrates SPV §6 Layer 3 characterization —
prioritized next action with justification, remaining unknowns named, uncertainty
reduction articulated since Stage 2 entry. Not defined by fixed question completion.
**Status:** Not yet designed. Characterization only — no implementation authorized.

---

## 7. STAGE 4 — ENGINEERING READINESS

**Purpose:** Evaluates whether mechanism understanding is sufficient to make engineering
design decisions. Bridges implementation intent and prototype planning.
**Objective served:** Implementation readiness proximity.
**Characterization:** Stage 4 is complete when the inventor can articulate what
engineering decisions are required and provide justified reasoning for each.
Does not require that engineering work has begun.
**Boundary with Stage 5:** Stage 4 ends when the inventor knows what must be built.
Stage 5 begins when the inventor must demonstrate what a first build must prove.
Specifying engineering decisions does not imply precision to define testable prototype
success criteria — that is the Stage 5 threshold.
**Constraint:** No Stage 4 design may foreclose commercial capabilities per SPV §11.
**Status:** Not yet designed. Characterization only.

---

## 8. STAGE 5 — PROTOTYPE READINESS

**Purpose:** Evaluates whether the inventor can plan a meaningful proof-of-concept
prototype.
**Objective served:** Implementation readiness proximity.
**Characterization:** Stage 5 is complete when the inventor can define a
proof-of-concept objective with explicit success criteria that would validate or
refute the core mechanism assumption. Does not require a prototype has been built.
**Boundary with Stage 4:** Stage 4 ends when the inventor knows what must be built.
Stage 5 ends when the inventor knows what a prototype must prove. Distinct epistemic
states — specifying what to build does not imply precision to define testable success
criteria.
**Evidence Architecture Note:** Evidence Architecture is a cross-cutting capability,
not a platform stage. Design deferred pending Priority 3 (Project vs Session)
resolution per GOVERNANCE-ROADMAP.md. Dependency for Stage 5 and later stages.
**Status:** Not yet designed. Characterization only.

---

## 9. STAGE 6 — COMMERCIALIZATION AND INSTITUTIONAL ECOSYSTEM

**Purpose:** Concerns deployment of InventorAI as an institutional platform — within
organizations, accelerators, and inventor development pipelines. Does not concern
commercialization of inventions. Invention commercialization is outside platform scope
per SPV §4. The word Commercialization in this stage name refers to the platform's
commercial deployment model, not any inventor's invention pathway.
Stage name inherited from SPV §9 and §11 language. Any renaming requires explicit
owner decision and SPV update.
**Objectives served:** All four — within institutional deployment context. Stage 6
does not change the measurement model. It changes the deployment model.
**Status:** NOT STARTED. SPV §11 commercial architecture constraints active now.
No Stage 6 design authorized until owner explicitly opens Stage 6 design work.

---

## 10. EVALUATION RULE GOVERNANCE ACROSS STAGES

**Definition:** Evaluation rules are domain-specific and stage-specific criteria
determining REASONED vs ASSERTED quality for a given inventor response. Distinct from
gap types (what is assessed) and substance signals (token-level evidence).

**Stage 2 current state:** Domain-specific. Registry authority for electronics
(rule_nuances). Mechanical, medical_device, software remain hardcoded in
domain_rules.py — this is AB-006-A. No stage context parameter.

**Are evaluation rules stage-specific?** Yes, in principle. The exclusion of
Problem-Mechanism Fit, Assumption Inventory, and Expertise-Gap Awareness from Stage 2
implies different reasoning structures at different stages. Rules sufficient for
Stage 2 are not necessarily sufficient for Stage 3.

**get_active_rules() stage awareness requirement:** Does not currently require stage
awareness because Stage 3 is not designed. When Stage 3 is designed, stage context
will be required. Current signature get_active_rules(domain) is consistent with the
single-stage architecture and does not need modification until Stage 3 design is
authorized.

Architectural implication for AB-006-A: registry migration for mechanical,
medical_device, and software may use the current domain-only signature without
creating architectural debt. The stage parameter is a Stage 3 design concern.
Introducing it before Stage 3 is designed would be implementing ahead of governing
authority. AB-006-A implementation decisions remain subject to AB-006 authorization —
this document records architectural context only.

**Migration path:** Intended future signature get_active_rules(domain, stage) with
stage defaulting to stage_2. Architectural direction only — not an implementation
instruction for AB-006.

---

## 11. STAGE TRANSITION GOVERNANCE

Stage transitions are authorized when the inventor demonstrates measurable growth
against exit criteria defined in this document. May not be authorized by: iteration
count, mechanical gap closure, session completion metrics, or owner override without
evidence basis.

Per SPV §5A: a stage is not complete because an inventor traversed the questions.
A stage is complete when growth is demonstrable.

**Prerequisites before Stage 3 design begins:**

1. This document (SA-001A) committed and owner-approved
2. SA-001B (Domain Model Specification) committed and owner-approved
3. AB-006-A and AB-006-B resolved — registry migration complete for all four domains
4. Owner explicit authorization of Stage 3 design work

---

## 12. OPEN QUESTIONS AND DEFERRED DECISIONS

**Requiring owner decision before relevant stage design begins:**

- Stage 3 gap type schema — complete set beyond three confirmed entries
- Stage 3 exit condition — specific growth thresholds
- Stage 4 and Stage 5 gap types and evaluation models
- Multi-domain assignment stage placement (deferred to SA-001B per §3.4)

**Blocked by other dependencies:**

- Evidence Architecture Specification — blocked by Priority 3 per GOVERNANCE-ROADMAP.md
- Stage 5 full design — depends on Evidence Architecture
- Stage 6 design — owner authorization required; SPV §11 constraints active now
- Multi-domain stage placement — depends on SA-001B

---

*This document is produced to be accurate, not reassuring.*
*Repository evidence takes precedence over chat history at all times.*
*No implementation authorized by this document except as explicitly stated in §10.*