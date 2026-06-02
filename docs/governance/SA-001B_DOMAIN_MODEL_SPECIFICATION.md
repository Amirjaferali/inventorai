# SA-001B — Domain Model Specification

**Document ID:** SA-001B
**Governance Level:** Level 1
**Status:** APPROVED
**Prepared during:** SA-001 Strategic Architecture Phase
**Date:** 2026-06-02
**Provenance:** Owner Authorization — SA-001B authorized 2026-06-02

---

## PROVENANCE RECORD

| Section | Classification |
|---------|---------------|
| 1. Document Authority | Owner Authorization — SA-001 |
| 2. Inherited Level 0 Constraints | Level 0 Derived — STRATEGIC_PRODUCT_VISION.md |
| 3. Domain Model Fundamentals | Owner Authorization — SA-001B 2026-06-02 |
| 4. Domain Family Model | Owner Authorization — SA-001B 2026-06-02 |
| 5. Electronics Domain Family | Owner Decision — electronics approved as first parent 2026-06-02 |
| 6. Other Domain Families | Repository Derived — current implementation |
| 7. Coverage Declaration Schema | Level 0 Derived — SPV §4 |
| 8. Domain Pack Schema Requirements | Owner Authorization — SA-001B revised 2026-06-02 |
| 9. Multi-Domain Composition | Owner Authorization — Stage 4 placement 2026-06-02 |
| 10. AB-006-B Governing Position | Owner Authorization — SA-001B 2026-06-02 |
| 11. Domain Expansion Governance | Owner Authorization — SA-001B 2026-06-02 |
| 12. Open Questions | SA-001B scope boundary |

---

## 1. DOCUMENT AUTHORITY

### 1.1 Governance Level and Placement

Level 1 governance document under SPV §12. Sits alongside
DOMAIN_PACK_GOVERNANCE_STANDARD_v1.md and SA-001A at Level 1.
No document at this level subordinates another unless SPV §12
explicitly records a precedence relationship. All three are
permanent peer authorities governing distinct architectural domains.

### 1.2 Relationship to DOMAIN_PACK_GOVERNANCE_STANDARD_v1.md

These two documents govern distinct concerns and must not be merged.
SA-001B defines the domain model: what domains are, how they relate,
what families they belong to, and what inheritance means.
DOMAIN_PACK_GOVERNANCE_STANDARD_v1.md defines domain pack governance:
what a valid domain pack contains, how packs are validated, and what
maintenance standards apply.
SA-001B does not supersede or demote the existing standard. Both remain
active Level 1 authorities. Where they address the same artifact (a
domain pack), SA-001B governs structural relationships and
DOMAIN_PACK_GOVERNANCE_STANDARD_v1.md governs content and validation.

### 1.3 Documents This Constrains

DOMAIN_PACK_GOVERNANCE_STANDARD_v1.md — pack schemas must accommodate
the inheritance and coverage declaration requirements defined here.
SA-001A §3.4 — that section deferred multi-domain stage placement to
this document; it must be updated once this document is committed.
All existing domain packs — must satisfy the coverage declaration
schema defined in §7.
All future domain packs — no pack may be created without satisfying
§11 domain expansion governance conditions.
GOVERNANCE-ROADMAP.md Priority 6 — multi-domain scalability sequencing
is governed by §9 and §11 of this document.
AB-006-B — the electronics question gap fix depends on §5 and §10.

### 1.4 Documents That Constrain This

STRATEGIC_PRODUCT_VISION.md (Level 0) — §7 Principle 3 (Multi-Domain
Integration Vision), §4 Coverage Declaration Principle, §1
Four-Objective Filter and Substitution Prohibition, §11 Commercial
Architecture Preservation.
SA-001A (Level 1 peer) — stage architecture constrains what the domain
model must support across stages. Domain model decisions that conflict
with stage boundaries in SA-001A require a formal resolution.
ADR-001-domain-assignment-and-multi-domain-strategy.md — existing ADR
decisions on domain assignment are peer constraints. This document must
be consistent with ADR-001 or formally supersede it with owner
authorization.
ADR-002-gap-taxonomy-strategy.md — gap types are Stage 2-frozen by
GD-001. This document governs domain structure, not gap types.

### 1.5 Modification Protocol

Requires owner authorization referencing the section to be modified,
evidence basis, and contradiction check against Level 0 and Level 1
peers. Sections 5 and 10 carry highest modification cost — changes to
electronics family position or AB-006-B governing position require
re-assessment of all downstream domain expansion work.

---

## 2. INHERITED LEVEL 0 CONSTRAINTS

### 2.1 Multi-Domain Integration Vision (SPV §7 Principle 3)

The long-term platform vision requires integrated cross-domain
understanding of one product — not parallel single-domain analyses.
This constrains the domain model to eventually support cross-domain
composition. Any domain model decision that permanently prevents
cross-domain gap identification violates this principle.

### 2.2 Coverage Declaration Principle (SPV §4)

Every domain pack must declare covered areas, not-covered areas, and
known limitations explicitly. No domain pack may imply coverage it does
not provide. This applies to parent packs, child packs, and standalone
packs equally. SA-001B formalizes the schema for this declaration.

### 2.3 Four-Objective Filter (SPV §1)

The domain model must serve at least one of the four platform
objectives: reasoning quality, ownership depth, gap precision,
implementation readiness proximity. Domain structure decisions that
serve none of these objectives have no governance basis.

### 2.4 Substitution Prohibition (SPV §1)

The domain model must not introduce domain knowledge into the engine.
Domain families, inheritance rules, and composition models are
structural — they define relationships between domains, not domain
content. Domain content (signals, questions, rules) remains in domain
packs. The engine remains domain-agnostic.

### 2.5 Commercial Architecture Preservation (SPV §11)

No domain model decision may structurally foreclose individual user
accounts, organizational hierarchy, subscription access, or enterprise
adoption with data isolation. Domain expansion plans must not assume
single-user or single-organization deployment.

---

## 3. DOMAIN MODEL FUNDAMENTALS

### 3.1 What a Domain Is

A domain is a named technical discipline that defines the knowledge
space relevant to evaluating an inventor's mechanism. A domain
determines which substance signals constitute REASONED quality, which
questions address mechanism gaps, and which evaluation rules apply.
Domains are not topics, industries, or markets. Electronics/Electrical
is a domain. Consumer electronics is not.

### 3.2 What a Domain Is Not

A domain is not a stage. Stage 2 can operate across any domain.
A domain is not a gap type. Gap types are Stage 2-frozen and
domain-agnostic. A domain is not a product category or market segment.
A domain is not a user persona or inventor background.

### 3.3 Domain vs Gap Type — The Distinction

Gap types define what kind of knowledge gap is being probed.
Domains define what domain-specific knowledge is relevant to probing
that gap. MECHANISM_COMPLETENESS is a gap type. The substance signals
that constitute a REASONED response to a mechanism completeness
question in electronics differ from those in mechanical engineering.
The gap type is universal; the evaluation criteria are domain-specific.

### 3.4 Domain vs Stage — The Distinction

Stages define where an inventor is in their journey. Domains define
what technical space their invention occupies. An inventor in Stage 2
working on an electronics invention uses the electronics domain pack.
The same inventor advancing to Stage 3 remains in the electronics
domain — but Stage 3 will require different domain-specific evaluation
criteria. Domain identity is persistent across stages; evaluation
content per domain may vary by stage.

### 3.5 Single-Domain vs Multi-Domain Assignment

Current architecture supports single-domain assignment per IdeaState.
This is implementation state, not permanent architecture. SPV §7
Principle 3 requires eventual multi-domain support. The transition
point is defined in §9. Until that transition, single-domain
assignment is the authorized model.

---

## 4. DOMAIN FAMILY MODEL

### 4.1 Definition of a Domain Family

A domain family is a group of related domains sharing a common
knowledge foundation. Within a family, child domains inherit the
parent's substance signals, gap type mappings, and evaluation rules
as a baseline, and may extend or override them with child-specific
content. A family exists to enable governed inheritance and prevent
content duplication — not as a taxonomy exercise.

### 4.2 Parent Domain — Definition and Criteria

A parent domain is a domain that:
1. Has an existing validated domain pack at the current maturity level
2. Has substance signals, gap type mappings, and evaluation rules
   sufficient to evaluate inventions in the broader family
3. Has identified child domains that share a knowledge foundation
4. Has resolved question authority (for electronics: AB-006-B)

A domain may not be designated a parent until its own pack is
complete. A parent with 0 questions in gap_type_mappings cannot
govern child domain inheritance of questions.

### 4.3 Child Domain — Definition and Inheritance Rules

A child domain is a domain that:
1. Belongs to an established family with a valid parent
2. Shares the parent's core knowledge foundation
3. Requires additional or different signals, questions, or rules
   beyond what the parent provides

Inheritance rules:
- A child domain inherits the parent's substance signals by default
- A child domain may extend parent signals with child-specific signals
- A child domain may override parent signals where stricter or
  different evaluation criteria are required
- A child domain must explicitly declare what it inherits and what
  it overrides — silent inheritance is not permitted
- A child domain's gap_type_mappings may extend but may not remove
  parent gap type entries without explicit justification

### 4.4 Standalone Domain — Definition and Criteria

A standalone domain has no parent and no children. It governs a
technical discipline that does not share a knowledge foundation with
any other current domain. Mechanical, medical_device, and software
are currently standalone domains. They may become parents if child
domains are identified and authorized.

### 4.5 Cross-Domain Composition

Cross-domain composition occurs when a single invention spans multiple
domain families and requires evaluation criteria from more than one
parent domain. This is architecturally anticipated by SPV §7 Principle 3
but is not yet implemented. The composition model is deferred to the
stage at which it first becomes relevant (§9). This document records
that composition is required and establishes the stage placement.

---

## 5. ELECTRONICS DOMAIN FAMILY

### 5.1 Electronics/Electrical — Approved as First Parent Domain

Electronics/Electrical is approved as the first parent domain.
This is an owner decision recorded in this document.

Justification: The electronics/electrical domain pack is the most
mature pack in the repository — the only validated domain with
rule_nuances defined. The candidate child domains listed in §5.2
all share the electronics knowledge foundation: circuit behavior,
signal integrity, power management, and component interaction.
None can be correctly evaluated without first establishing
electronics-level mechanism understanding. Inheritance is
architecturally sound, not merely administrative.

Constraint: Electronics/Electrical may not function as a parent
domain in practice until AB-006-B resolves the 0-question gap in
gap_type_mappings. The designation is approved; the authority
maturity precondition is not yet satisfied.

### 5.2 Authorized Child Domain Candidates — Electronics Family

The following are architecturally authorized candidates. None are
approved for creation. All remain blocked by §11 conditions,
primarily AB-006-B resolution.

| Candidate | Knowledge Basis for Inheritance |
|-----------|--------------------------------|
| PCB Design | Circuit layout, signal integrity, power distribution |
| Embedded Systems | Firmware, hardware-software interface, real-time constraints |
| IoT / Connected Devices | Embedded + networking, power, data protocols |
| Power Electronics | Energy conversion, thermal management, efficiency |
| Solar / Renewable Energy Systems | Power electronics + environmental interface |
| Robotics and Automation | Mechanical + electronics + control systems |
| Industrial Control Systems | Embedded + power + safety-critical constraints |

Note: Robotics and Automation and Industrial Control Systems span
mechanical and electronics knowledge. Their family placement requires
a cross-family decision not resolved by this document.

### 5.3 What Child Domains Inherit from Electronics Parent

Subject to AB-006-B resolution:
- Classification signals (electronics_electrical baseline)
- Substance signals (electronics_electrical baseline)
- Gap type mappings (once question authority is established)
- Rule nuances (electronics baseline)

### 5.4 What Child Domains Must Define Independently

- Child-specific substance signals not present in the parent
- Child-specific questions where parent questions are insufficient
- Child-specific rule nuances where parent rules do not apply
- Coverage declaration — every child pack declares independently

### 5.5 O-11 Constraint Application

No child domain in the electronics family may author
gap_type_mappings questions until the parent's question authority
is resolved. AB-006-B resolution is the precondition. The O-11
constraint is lifted only when AB-006-B is closed with a verified,
committed parent-level question set.

---

## 6. OTHER DOMAIN FAMILIES

### 6.1 Mechanical

Standalone domain. 19 classification signals, 17 substance signals,
3 gap types, 10 questions, 0 rule nuances. No child domains identified.
Mechanical may become a parent if domains sharing its knowledge
foundation are proposed and authorized. No expansion authorized here.

### 6.2 Medical Device

Standalone domain. 26 classification signals, 10 substance signals,
3 gap types, 10 questions, 0 rule nuances. No child domains identified.
Regulatory and compliance scope creates a distinct knowledge boundary
that future child domains would need to respect. No expansion
authorized here.

### 6.3 Software

Standalone domain. 21 classification signals, 15 substance signals,
2 gap types, 9 questions, 0 rule nuances. No child domains identified.
Software's 2-gap-type schema is a known architectural difference any
future child domain would need to account for. No expansion authorized.

### 6.4 Future Domain Families

Domains not yet in the registry are not governed by this document.
Any new domain proposal must satisfy §11 conditions before entering
the governance process.

---

## 7. COVERAGE DECLARATION SCHEMA

### 7.1 Required Fields for All Domain Packs

Every domain pack — parent, child, or standalone — must contain a
coverage declaration with three required fields:

covered_areas: An explicit list of the technical sub-disciplines
and problem types the domain pack evaluates. Claims must be backed
by substance signals and questions in the pack.

not_covered_areas: An explicit list of technically adjacent areas
the pack does not evaluate. Prevents inventors from inferring
coverage the pack does not provide.

known_limitations: An explicit list of known gaps in the pack's
current evaluation capability — areas covered in principle but
where the current signal or question set is incomplete.

No domain pack is complete without all three fields populated.

### 7.2 Application to Existing Domain Packs

The four existing packs do not currently contain coverage
declarations. They must be updated to satisfy this requirement.
This update adds declaration fields only — no evaluation logic
changes. It is a governance compliance requirement derivable from
SPV §4, not AB-006 work. It should be included in AB-006 pack
work or performed as a separate governance commit before AB-006-B
closes.

### 7.3 Application to Child Domains

A child domain must provide its own independent coverage declaration.
Inheriting parent substance signals does not imply inheriting parent
coverage declarations. A child specializing in PCB design must
declare PCB-specific covered areas, not-covered areas, and known
limitations. The parent's coverage declaration is not a substitute.

---

## 8. DOMAIN PACK SCHEMA REQUIREMENTS

### 8.1 Requirements at Parent Level

A parent domain pack must represent, in addition to all fields
required by DOMAIN_PACK_GOVERNANCE_STANDARD_v1.md:

- Its role in the domain family — the pack must be identifiable
  as a parent, not a standalone or child, by any consuming system
  or governance review
- The set of authorized child domains — even if empty at creation,
  the parent pack must carry a record of which child domains are
  sanctioned under it
- A complete coverage declaration per §7.1

The exact schema fields used to represent these requirements are
an implementation decision governed by
DOMAIN_PACK_GOVERNANCE_STANDARD_v1.md, which must be updated to
validate them. SA-001B governs what must be represented, not how.

### 8.2 Requirements at Child Level

A child domain pack must represent:

- Its role in the domain family — identifiable as a child
- Its parent domain — the relationship to the parent must be
  explicitly recorded and verifiable
- What it inherits from the parent — the child must explicitly
  declare which parent fields it uses without modification
- What it overrides — any parent field the child replaces or
  extends must be explicitly declared with justification
- A complete and independent coverage declaration per §7.3

Silent inheritance is not permitted. A child pack that uses parent
signals or questions without declaring the inheritance relationship
fails governance review regardless of content quality.

### 8.3 Inheritance Declaration Obligation

The following content categories may be inherited, extended,
or overridden by a child domain:

- Substance signals
- Gap type mappings and questions
- Evaluation rule nuances

For each category, the child must declare one of three positions:
inherited without modification, extended with additions, or
overridden with replacement. A category not addressed in the
child's inheritance declaration is assumed inherited without
modification — this assumption must be made explicit, not silent.

Classification signals must be declared independently by the child.
A child domain occupies a distinct technical sub-space and must
define its own classification vocabulary. Inheriting parent
classification signals wholesale causes misclassification of
inventions belonging to the child domain specifically.

### 8.4 Relationship to DOMAIN_PACK_GOVERNANCE_STANDARD_v1.md

The governance requirements in §8.1, §8.2, and §8.3 extend the
existing pack standard. DOMAIN_PACK_GOVERNANCE_STANDARD_v1.md
must be updated to validate family role representation,
parent-child relationship recording, and inheritance declaration
completeness. That update requires owner authorization and a
separate commit — it is not authorized by this document.

Until the standard is updated, requirements in this section are
enforced through governance review rather than automated validation.
No pack claiming parent or child status may be committed without
a governance review confirming §8.1 and §8.2 compliance.

---

## 9. MULTI-DOMAIN COMPOSITION

### 9.1 When an Invention Spans Multiple Domains

Some inventions cannot be correctly evaluated by a single domain
pack. A solar-powered IoT irrigation controller spans power
electronics, embedded systems, and potentially mechanical domains.
Evaluating only the electronics mechanism misses the cross-domain
gaps where the invention is most likely to fail.

### 9.2 Current Architecture Limitation

Current architecture assigns one domain per IdeaState. This is
implementation state, not permanent architecture, as confirmed
by SA-001A §3.4.

### 9.3 Future Requirement — Cross-Domain Gap Identification

SPV §7 Principle 3 requires that the platform eventually identify
gaps at domain intersections. This requires: multi-domain assignment
per IdeaState, cross-domain gap evaluation, and a composition model
for combining domain-specific substance signals.

### 9.4 Stage Placement for Multi-Domain Reasoning

Owner-authorized position: multi-domain reasoning first becomes
architecturally relevant at Stage 4 (Engineering Readiness).

Rationale: Stage 2 focuses on mechanism understanding within a
single domain — single-domain evaluation is sufficient. Stage 3
evaluates whether the inventor can identify concrete next actions —
still primarily single-domain. Stage 4 requires specifying what
must be built. For multi-domain inventions, this requires reasoning
about cross-domain interfaces and constraints — the point at which
single-domain evaluation becomes architecturally insufficient.

SA-001A §3.4 must be updated to record Stage 4 as the multi-domain
stage placement. That amendment requires a separate commit.

This records stage placement only. Multi-domain architecture design,
multi-domain IdeaState implementation, and cross-domain gap type
definition are deferred — none are authorized by this document.

---

## 10. AB-006-B GOVERNING POSITION

### 10.1 The Electronics Question Gap

The electronics_electrical domain pack has 0 questions in
gap_type_mappings. The three gap types are present but contain no
questions. get_domain_question() cannot surface electronics-specific
questions for any gap type.

### 10.2 What the Correct Fix Requires

Electronics/Electrical is now approved as a parent domain (§5.1).
AB-006-B must therefore proceed on Path A.

Path A — Parent-scoped question authoring:
AB-006-B must author gap_type_mappings questions at the parent level,
covering the core electronics/electrical knowledge space. Questions
must be scoped to the parent — general enough to apply across the
electronics family, specific enough to be meaningfully different from
questions in mechanical or medical_device domains. Child-domain-specific
questions (PCB, IoT, etc.) are not AB-006-B scope and remain blocked
by O-11 until the parent question set is established.

### 10.3 What AB-006-B Must Produce

- gap_type_mappings questions for MECHANISM_COMPLETENESS,
  PHYSICAL_FEASIBILITY, and BOUNDARY_AMBIGUITY at parent level
- Coverage declaration for the electronics_electrical pack (§7.2)
- Parent role representation and authorized child domain record
  per §8.1, using schema fields to be defined when
  DOMAIN_PACK_GOVERNANCE_STANDARD_v1.md is updated

### 10.4 What AB-006-B Must Not Do

- Author child-domain-specific questions in the parent pack
- Add new gap types (GD-001 frozen)
- Change substance signals (AB-006-A scope)
- Create any child domain packs
- Modify engine code

### 10.5 O-11 Application

Until AB-006-B is closed with a verified committed parent-level
question set, no electronics family child domain may author
gap_type_mappings questions. The O-11 constraint is not lifted by
this document — it is lifted only by AB-006-B closure.

---

## 11. DOMAIN EXPANSION GOVERNANCE

### 11.1 Conditions for Adding a New Standalone Domain

1. Proposed pack passes schema validation per
   DOMAIN_PACK_GOVERNANCE_STANDARD_v1.md
2. Pack includes complete coverage declaration (§7.1)
3. Domain classified as standalone, child, or parent with
   justification
4. Owner explicitly authorizes the new domain
5. WPS001 and Architecture Guardrails pass after addition

### 11.2 Conditions for Adding a Child Domain

In addition to §11.1:
1. Parent domain formally designated (owner decision on record)
2. Parent pack satisfies Level 1 schema requirements including
   coverage declaration and family role representation
3. Parent question authority resolved (for electronics: AB-006-B
   must be closed)
4. Child pack explicitly declares inherited and overridden content
   per §8.2
5. O-11 satisfied — child authority maturity does not exceed parent

### 11.3 O-11 Restated

No expansion domain may exceed its parent's authority maturity.
A parent with 0 questions in gap_type_mappings has zero question
authority maturity. No child domain may author questions until the
parent has established question authority.

### 11.4 Authorization Sequence for New Domain Packs