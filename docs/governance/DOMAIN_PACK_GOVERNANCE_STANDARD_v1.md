# DOMAIN_PACK_GOVERNANCE_STANDARD_v1.md

**Document type:** Domain governance standard — Level 1 Authority
**Version:** 1.0 Final
**Date:** 2026-05-31
**Status:** APPROVED FOR REPOSITORY ADMISSION
**Prepared by:** Agent (Phase C)

---

## STAGE 2 CLOSURE SUMMARY

This document establishes what a valid domain pack is, how it must be structured, what governance risks must be managed, and what questions are deferred to v1.1. Once committed alongside STRATEGIC_PRODUCT_VISION.md, Stage 2 governance is complete and Stage 3 planning is unblocked — subject to AB-001 and AB-005 resolution before any Stage 3 execution begins.

---

## PROVENANCE RECORD

| Section | Classification |
|---------|---------------|
| 1. Purpose | Repository Derived |
| 2. Domain-Agnosticism Requirement | Repository Derived |
| 3. Response Quality Framework | Repository Derived |
| 4. Non-Participation Taxonomy | Repository Derived |
| 5. Governance Risk Register | Repository Derived + Owner Extension |
| 6. Domain Pack Structure Requirements | Repository Derived + Owner Extension |
| 7. Activation Gate | Repository Derived + Owner Extension |
| 8. Deferred Open Questions (OQ-S2) | Owner Decision (2026-05-31) |
| 9. Configuration Constraints | Repository Derived |
| 10. Deprecation Policy | Deferred to v1.1 |

---

## 1. PURPOSE

*Provenance: Repository Derived*

This document defines the governance standard for domain packs in InventorAI. A domain pack is a configuration artifact that extends the engine to a new domain without modifying the core engine.

**The engine is domain-agnostic. Domain packs are domain-specific. These two layers must never be merged.**

No domain expansion may be authorized until both architectural blockers are resolved:

- **AB-001:** Domain-specific signal detection currently resides in `progression_loop.py` rather than the domain configuration layer — violating the domain-agnosticism invariant
- **AB-005:** Registry loader inactive — `domain_rules.py` is runtime authority, not `domain.json` — making domain expansion architecturally unsafe

No domain pack may be activated until AB-001 and AB-005 are formally resolved, implemented, and validated against the benchmark. Resolution requires explicit owner approval.

---

## 2. DOMAIN-AGNOSTICISM REQUIREMENT

*Provenance: Repository Derived — ARCHITECTURE-DOMAIN-AGNOSTICISM-REVIEW, STATE_FREEZE*

The core engine operates on Evidence, Gaps, Mechanisms, Reasoning Quality, and Progression Logic — not on domain-specific concepts.

**What domain-agnosticism requires:**
- The engine must produce valid output for any domain pack that conforms to this standard
- No domain vocabulary, signal list, or terminology may exist in `progression_loop.py`
- Domain content is a configuration layer, not an engine concern
- The Participation Floor must remain stable as new domains are added — per-domain tuning violates this requirement
- Any governance approach must be validated against non-specialist response fixtures from at least two domains before adoption

**What domain-agnosticism forbids:**
- Domain-specific branching in `progression_loop.py`
- Signal lists, keyword filters, or vocabulary checks in the core engine
- Domain classification that permanently assigns one domain label to a multi-domain invention
- Multi-domain implementation that produces separate domain reports rather than integrated cross-domain gap analysis

---

## 3. RESPONSE QUALITY FRAMEWORK

*Provenance: Repository Derived — RESPONSE-QUALITY-GOVERNANCE-ASSESSMENT*

### Two Distinct Problems

**Problem 1 (Solved):** Does this response contain genuine causal reasoning, or does it merely assert outcomes?
Addressed by `assess_response()` — ASSERTED vs. REASONED classification.

**Problem 2 (Governance Pending):** Does this response represent a genuine attempt to engage, or is it noise, filler, repetition, or non-participation that should not advance the session at all?
Requires a Participation Floor — not yet implemented.

### Two Distinct Floors

**Quality Floor:** Is the response ASSERTED or REASONED? A quality gradient applied after participation is confirmed. Currently implemented.

**Participation Floor:** Did the inventor make a genuine attempt to respond? Binary — either genuine or not. Currently absent. Any string of 40+ characters passes into the classifier regardless of whether it represents genuine participation.

### Governing Constraint

The Participation Floor must remain a participation gate only. It must never become a correctness gate or an expertise gate. InventorAI supports non-specialist inventors. A floor that penalizes domain-naive language, informal reasoning style, or non-technical vocabulary would contradict the core product purpose defined in the Owner Vision Lock.

---

## 4. NON-PARTICIPATION TAXONOMY

*Provenance: Repository Derived — RESPONSE-QUALITY-GOVERNANCE-ASSESSMENT Section 4*

| Category | Description | Example |
|----------|-------------|---------|
| 1 — Keyboard noise | Random character sequences. No words, syntax, or semantic content | 444444444, asdfasdf |
| 2 — Filler repetition | Repeated words or phrases. Linguistic tokens present, zero information density | "I don't know I don't know I don't know" |
| 3 — Off-topic response | Valid text with no connection to the question asked | — |
| 4 — Content-free acknowledgment | Acknowledges the question without answering it | "I understand", "okay", "yes that sounds right" |
| 5 — Restated question | The inventor reflects the question back as an answer | Platform asks about physical principle; inventor responds "the physical principle my mechanism relies on is important" |
| 6 — AI Echo Response | The inventor copies or paraphrases platform-provided guidance without contributing original reasoning | Near-verbatim restatement of platform explanation of a technical concept |

**Note on Category 6:** AI Echo responses are not detectable without provenance tracking — comparing the inventor response against prior platform output. This requires a mechanism not appropriate for current architecture and must be assessed separately as part of GD-002 Technical Guidance layer design.

---

## 5. GOVERNANCE RISK REGISTER

*Provenance: Repository Derived + Owner Extension — R-7 (RD-007), R-8 (RD-008)*

| Risk ID | Description | Severity | Mitigation |
|---------|-------------|----------|-----------|
| R-1 | False rejection of non-specialist inventors | HIGH — primary risk | Floor calibrated on participation intent, not domain vocabulary |
| R-2 | Gaming by surface compliance | MEDIUM | Floor must detect Category 5 (restated question) |
| R-3 | Stall interaction conflict | MEDIUM | Floor and stall detection must be coordinated before implementation |
| R-4 | Classifier boundary creep | HIGH | Implementation must be a pre-classifier gate only — not a modification to `assess_response()` |
| R-5 | Inventor experience degradation | MEDIUM | Rejection must be accompanied by clear non-technical guidance — floor cannot be a silent barrier |
| R-6 | AI Echo amplification under Technical Guidance | HIGH | AI Echo governance must be explicitly revisited before any Technical Guidance layer is deployed |
| R-7 | Knowledge Currency Risk | MEDIUM | Domain pack content may become outdated as domain knowledge evolves. Each pack must declare its knowledge_baseline_date and review_interval_days. Packs not reviewed within their declared interval must be flagged before activation in any new session |
| R-8 | Decision Traceability Risk | MEDIUM | Future agents or developers may not know why a domain pack was designed the way it was. Each pack must include a design_decisions log recording rationale for non-obvious design choices |

---

## 6. DOMAIN PACK STRUCTURE REQUIREMENTS

*Provenance: Repository Derived + Owner Extension*

A conformant domain pack must contain all required fields. A pack missing any required field fails validation and may not be activated.

### Core Identity Fields

| Field | Required | Description |
|-------|----------|-------------|
| domain_id | YES | Unique identifier string |
| domain_name | YES | Human-readable display name |
| version | YES | Semantic version string (e.g. 1.0.0) |
| created_at | YES | ISO-8601 date of initial creation |
| last_reviewed_at | YES | ISO-8601 date — must be updated on any content change |
| review_interval_days | YES | Maximum days between mandatory content reviews |
| knowledge_baseline_date | YES | Date the domain knowledge in this pack was current — addresses R-7 |

### Content Fields

| Field | Required | Description |
|-------|----------|-------------|
| gap_types | YES | List of gap types this domain supports |
| questions | YES | Question bank per gap type |
| substance_signals | YES | Domain-specific substance signal list — currently blocked by AB-001; must migrate from `domain_rules.py` before activation |

### Coverage Declaration Fields

*Provenance: Owner Decision (2026-05-31)*

| Field | Required | Description |
|-------|----------|-------------|
| covered_areas | YES | Explicit list of what this pack actively evaluates |
| not_covered_areas | YES | Explicit list of what is outside this pack's scope. A pack with an empty not_covered_areas field fails validation |
| known_limitations | YES | Explicit list of areas the pack addresses but with acknowledged constraints or simplifying assumptions |

**Example not_covered_areas entries:**
- Regulatory approval
- Certification requirements
- EMC / electromagnetic compatibility
- Manufacturing readiness
- Supply chain viability
- Commercial viability
- Build readiness

**Example known_limitations entries:**
- Educational-stage assumptions (pack designed for early-concept inventors, not production engineers)
- Early-concept assumptions (pack assumes pre-prototype stage)
- Incomplete regulatory coverage (pack references compliance considerations but does not fully assess them)
- Limited domain breadth (pack covers one sub-domain within a broader field)

### Coverage Declaration Validation Rules

*Provenance: AB-006-A Step 2 — Owner Decision (2026-06-02)*

Coverage declarations define authority boundaries, not capability claims.

The following rules govern coverage declarations for all domain packs. They apply
before any parent domain coverage is authored.

**Required field behavior:**
- `covered_areas`: must be a non-empty explicit list. Vague entries such as
  "general electronics" or "most hardware concepts" are not acceptable.
- `not_covered_areas`: must require explicit consideration and documentation.
  A pack that has not documented what it does not cover has not completed its
  coverage declaration.
- `known_limitations`: must be a non-empty explicit list. Simplifying assumptions
  and scope boundaries must be stated, not implied.

**Validation criteria:**
- Coverage claims must be bounded. A claim that implies unlimited scope fails.
- Exclusions must be visible. A pack that does not declare what it does not cover
  cannot be treated as authoritative for unlisted areas.
- Known limitations must be preserved as governance-visible constraints, not
  buried in design notes or omitted entirely.

**Scope constraints for this declaration:**
- A coverage declaration does not authorize child domain creation.
- A coverage declaration does not authorize multi-domain reasoning.
- A coverage declaration does not modify runtime behavior.
- A parent domain coverage declaration alone does not authorize child-domain
  question authoring or coverage declaration. Separate governance authorization
  is required.

### Domain Family Role Fields

*Provenance: AB-006-B Step 3d — Owner Decision (2026-06-03)*

These fields define a domain pack's position within a domain family. They are
required for any pack that acts as a parent domain. Standalone packs should
explicitly declare domain_family_role: "standalone" unless backward-compatibility
constraints require omission.

| Field | Required | Description |
|-------|----------|-------------|
| domain_family_role | YES for parent/child packs | Declares the pack's role in the domain family. Allowed values: "parent", "child", "standalone". A pack without this field is treated as standalone. |
| authorized_child_domains | YES if domain_family_role is "parent" | List of child domain IDs explicitly authorized under this parent. An empty list is permitted — it means no child domains have been authorized yet. |

**domain_family_role behavior:**
- A pack with `domain_family_role: "parent"` establishes the family authority
  boundary for its domain. It does not automatically grant authority to any
  child domain.
- A pack with `domain_family_role: "child"` must explicitly declare its parent
  domain and its inheritance position per §8.2 of SA-001B.
- A pack with `domain_family_role: "standalone"` has no family relationships.
  Standalone packs may not inherit from or authorize child domains.

**authorized_child_domains behavior:**
- An empty list means no child domains have been authorized. This is the correct
  initial state for a newly designated parent domain.
- A non-empty list records which child domain IDs have received explicit
  governance authorization. Presence in this list does not trigger any runtime
  behavior — it is a governance record only.
- Adding a domain ID to authorized_child_domains does not authorize that domain
  to author questions, declare coverage, or participate in multi-domain
  reasoning. Each of those capabilities requires separate governance
  authorization.

**Validation expectations:**
- A pack declaring `domain_family_role: "parent"` must also carry a complete
  coverage declaration per §6 Coverage Declaration Fields.
- A child pack must identify its governing parent domain. The exact schema
  representation of that relationship will be defined when the first
  child-domain pack is authorized.
- authorized_child_domains must be an explicit list. A null value is not
  acceptable for a parent domain — use an empty list to represent zero
  authorized children.

**Relationship to parent-domain authority:**
- Parent role establishes the family authority boundary only.
- Child domains require separate governance authorization regardless of their
  presence in authorized_child_domains.
- authorized_child_domains is a record of authorization status, not an
  implementation trigger.
- No runtime behavior changes when authorized_child_domains is updated.

### Validation and Traceability Fields

*Provenance: Owner Decision (2026-05-31)*

| Field | Required | Description |
|-------|----------|-------------|
| benchmark_validated_domains | YES | List of domains against which this pack has been validated using the engine benchmark. Must show 27 passed (or higher), 0 failed per domain |
| expert_reviewed_by | NO (nullable) | Name or description of the domain expert who reviewed pack content, if any. Null is acceptable for v1.0 packs |
| design_decisions | YES | Log of rationale for non-obvious design choices — addresses R-8 |

---

## 7. ACTIVATION GATE

*Provenance: Repository Derived + Owner Extension*

No domain pack may be activated until all gates are met:

| Gate | Status |
|------|--------|
| AB-001 resolved and committed | NOT MET |
| AB-005 resolved and committed | NOT MET |
| Benchmark green after AB-001 and AB-005 resolution | NOT VERIFIED |
| STRATEGIC_PRODUCT_VISION.md committed | NOT MET |
| DOMAIN_PACK_GOVERNANCE_STANDARD_v1.md committed (this document) | NOT MET |
| Domain pack schema conforms to Section 6 | NOT MET |
| covered_areas populated | NOT MET |
| not_covered_areas populated (non-empty) | NOT MET |
| known_limitations populated | NOT MET |
| benchmark_validated_domains populated | NOT MET |
| Owner explicit authorization | NOT MET |

**Sandbox validation environment:**
Deferred to v1.1 (DF-007). Before any domain pack is activated in a production environment, a sandbox validation process must be defined and documented. Specification is deferred pending Stage 3 planning.

**Multi-domain expansion** additionally requires:
- Technical Guidance layer design approved (GD-002)
- AI Echo governance resolved
- Knowledge source separation defined

---

## 8. DEFERRED OPEN QUESTIONS (OQ-S2)

*Provenance: Owner Decision (2026-05-31)*

| ID | Question | Deferral Basis | Must Resolve Before |
|----|----------|----------------|---------------------|
| OQ-S2-001 | Minimum question count per gap type | No runtime constant found in codebase — tuning decision | v1.1 |
| OQ-S2-002 | Discrimination test methodology | No code dependency — methodology undefined | v1.1 |
| OQ-S2-003 | Progression evidence threshold | No runtime constant found in codebase — tuning decision | v1.1 |
| OQ-S2-004 | Who qualifies as domain expert reviewer | Operational decision — no current technical dependency | v1.1 |
| OQ-S2-005 | Deprecation policy for domain packs | No active domain packs — premature | v1.1 |

These questions do not block v1.0 adoption. All five must be resolved before v1.1 is committed.

---

## 9. CONFIGURATION CONSTRAINTS

*Provenance: Repository Derived — STATE_FREEZE Section 12*

| Constant | Current Value | Location | Governance Constraint |
|----------|--------------|----------|----------------------|
| STALL_THRESHOLD | 3 | domain_rules.py line 35 | Must not change before D-006 is investigated and fix verified in a live session |
| GAP_PRIORITY order | MECHANISM_COMPLETENESS then PHYSICAL_FEASIBILITY then BOUNDARY_AMBIGUITY | domain_rules.py | Must not change — defines entire progression sequence |

---

## 10. DEPRECATION POLICY

*Provenance: Deferred to v1.1 — DF-001*

No active domain packs exist at time of this document's creation. A deprecation policy will be defined in v1.1 when at least one domain pack has been activated and validated. The policy must address at minimum:

- Criteria for marking a pack as deprecated
- Migration path for in-progress sessions using a deprecated pack
- Archive requirements for deprecated pack versions
- Owner authorization requirements for any deprecation decision

---

*This document is produced to be accurate, not reassuring.*
*No domain expansion is authorized until all gates in Section 7 are met.*
*Repository evidence takes precedence over chat history at all times.*
*No implementation without evidence. No evidence without repository inspection.*