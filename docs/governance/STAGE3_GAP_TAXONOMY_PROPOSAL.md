# STAGE3_GAP_TAXONOMY_PROPOSAL.md
## Stage 3 Gap Taxonomy Proposal

**Document ID:** STAGE3_GAP_TAXONOMY_PROPOSAL
**Type:** Design Proposal
**Governance Level:** Level 3
**Status:** PROPOSED -- PENDING OWNER ADMISSION DECISION
**Date:** 2026-06-03
**Provenance:** Owner Authorization -- STAGE3_DESIGN_AUTHORIZATION b209027
**Depends on:** SA-001A §6, STAGE3_PURPOSE_CLARIFICATION, STAGE3_GAP_FOUNDATION_ANALYSIS

---

## PURPOSE OF THIS PROPOSAL

This document proposes the Stage 3 gap taxonomy. It defines the three canonical gap types confirmed in SA-001A §6, establishes their precise definitions, records their relationships and ordering, and applies the minimal canonical foundation philosophy established in STAGE3_GAP_FOUNDATION_ANALYSIS.

No questions are authored here. No evaluation model is designed. No exit conditions are specified. No implementation is proposed.

The taxonomy defines what is assessed in Stage 3. How it is assessed comes later.

---

## 1. FOUNDATION

### 1.1 Canonical Gap Types -- Confirmed by SA-001A §6

Three gap types are confirmed as canonical Stage 3 members per STAGE3_GAP_FOUNDATION_ANALYSIS §1.3.

| Gap Type | SA-001A §6 Confirmation |
|---|---|
| PROBLEM_MECHANISM_FIT | Does the mechanism address the intended problem? |
| ASSUMPTION_INVENTORY | Which underlying assumptions are unvalidated? |
| EXPERTISE_GAP_AWARENESS | What domain expertise does the inventor lack? |

### 1.2 Governing Philosophy

Per STAGE3_GAP_FOUNDATION_ANALYSIS §4.3: minimal canonical foundation with governed expansion. This proposal defines the three canonical types precisely and does not propose additions. Expansion is subject to the five criteria in STAGE3_GAP_FOUNDATION_ANALYSIS §2.

### 1.3 What Gap Types Are and Are Not

A gap type defines a category of inventor capability being assessed. It is not a question, not an evaluation criterion, not a substance signal. It is the named dimension of understanding that Stage 3 probes.

Stage 3 gap types are qualitatively different from Stage 2 gap types per STAGE3_PURPOSE_CLARIFICATION §2. Stage 2 gap types assess mechanism knowledge. Stage 3 gap types assess implementation-oriented reasoning capability.

---

## 2. GAP TYPE DEFINITIONS

### 2.1 PROBLEM_MECHANISM_FIT

**Definition:**
The gap between what the inventor's mechanism does and what problem the inventor intends it to solve. An inventor with complete mechanism understanding may still have an unexamined assumption that their mechanism addresses their intended problem. PROBLEM_MECHANISM_FIT surfaces and evaluates this alignment.

**What it assesses:**
Whether the inventor can articulate the problem they are solving, the mechanism they are using to solve it, and a reasoned justification for why this mechanism addresses this problem rather than a different mechanism or a different problem.

**What it does not assess:**
Whether the problem is worth solving (outside platform scope per SPV §4). Whether the mechanism is the best solution. Whether the market wants the solution.

**Distinction from Stage 2:**
Stage 2 MECHANISM_COMPLETENESS asks: is the mechanism well-described? PROBLEM_MECHANISM_FIT asks: does the mechanism address the intended problem? An inventor can have a complete mechanism description that solves a different problem than intended. Stage 2 does not detect this. Stage 3 does.

**Relationship to Stage 3 exit characterization:**
Contributes to: ability to identify prioritized next action with justification (SA-001A §6). An inventor who cannot confirm problem-mechanism fit cannot justify why any next action is prioritized.

**Stage placement justification:**
SA-001A §6 confirms Problem-Mechanism Fit belongs to Stage 1 (surfacing) and Stage 3 (reassessment). In Stage 3 it is reassessed with implementation orientation.

---

### 2.2 ASSUMPTION_INVENTORY

**Definition:**
The set of unvalidated assumptions underlying the inventor's mechanism and implementation path. Every invention rests on assumptions the inventor has not yet tested. ASSUMPTION_INVENTORY develops the inventor's ability to name, classify, and prioritize these assumptions.

**What it assesses:**
Whether the inventor can articulate what they are assuming about their mechanism, materials, environment, users, and implementation path -- and which assumptions are load-bearing (invention fails if wrong) versus peripheral (invention continues if wrong).

**What it does not assess:**
Whether the assumptions are correct. Whether the assumptions can be validated. Whether the invention is feasible (outside platform scope per SPV §4).

**Distinction from Stage 2:**
Stage 2 PHYSICAL_FEASIBILITY asks: are there physical constraints the inventor has not accounted for? ASSUMPTION_INVENTORY asks: what is the inventor assuming, whether or not they have recognized those assumptions? PHYSICAL_FEASIBILITY surfaces known gaps. ASSUMPTION_INVENTORY surfaces unknown assumptions. The epistemic act is different.

**Relationship to Stage 3 exit characterization:**
Contributes to: naming remaining unknowns with precision (SA-001A §6). An inventor who cannot name their assumptions cannot name what remains unknown.

**Stage placement justification:**
SA-001A §6 confirms Assumption Inventory belongs to Stage 1 (surfacing) and Stage 3 (reassessment). In Stage 3 it is reassessed with implementation orientation.

---

### 2.3 EXPERTISE_GAP_AWARENESS

**Definition:**
The inventor's awareness of what domain expertise they lack and why they lack it. An inventor can understand their mechanism completely and still be unaware that implementing it requires expertise outside their current knowledge. EXPERTISE_GAP_AWARENESS develops the inventor's ability to identify, name, and prioritize these expertise gaps.

**What it assesses:**
Whether the inventor can articulate what technical domains are required to implement their mechanism, which they have sufficient knowledge in, which they do not, and what kind of expertise would be needed to fill the gaps they cannot fill themselves.

**What it does not assess:**
Whether the inventor can acquire the expertise. Whether experts are available. Whether the invention is technically achievable (outside platform scope per SPV §4).

**Distinction from Stage 2:**
Stage 2 BOUNDARY_AMBIGUITY asks: where does the mechanism scope end? EXPERTISE_GAP_AWARENESS asks: what expertise does the inventor lack to implement the mechanism? A well-bounded mechanism may require expertise the inventor has not identified. Stage 2 does not detect this. Stage 3 does.

**Relationship to Stage 3 exit characterization:**
Contributes to: articulating how uncertainty has reduced since Stage 2 entry, and defining a proof-of-concept objective (SA-001A §6).

**Stage placement justification:**
SA-001A §6 confirms Expertise-Gap Awareness belongs to Stage 3. Unlike the other two gap types, it does not appear in Stage 1 characterization. It requires the implementation-oriented perspective that Stage 3 develops.

---

## 3. RELATIONSHIPS BETWEEN GAP TYPES

### 3.1 Logical Dependencies

The three gap types are not independent. They have a logical progression:

PROBLEM_MECHANISM_FIT must be assessed before ASSUMPTION_INVENTORY can be fully productive. An inventor who has not confirmed problem-mechanism fit may be inventorying assumptions about the wrong mechanism-problem relationship.

ASSUMPTION_INVENTORY informs EXPERTISE_GAP_AWARENESS. Once the inventor has named their assumptions, they can identify which assumptions require expertise to validate.

Proposed assessment order: PROBLEM_MECHANISM_FIT then ASSUMPTION_INVENTORY then EXPERTISE_GAP_AWARENESS.

This is a design proposal, not a governance constraint. The ordering is logically motivated but may be refined during evaluation model design.

### 3.2 Relationship to Stage 2 Exit State

Stage 3 entry presupposes Stage 2 exit. Stage 3 gap types build on Stage 2 foundation without reassessing Stage 2 content.

PROBLEM_MECHANISM_FIT reassesses mechanism purpose (not mechanism completeness).
ASSUMPTION_INVENTORY reassesses what was assumed during Stage 2 (not what was demonstrated).
EXPERTISE_GAP_AWARENESS assesses implementation requirements (which Stage 2 does not address).

### 3.3 Joint Contribution to Exit Characterization

| SA-001A §6 Exit Requirement | Primary Gap Type | Supporting Gap Type |
|---|---|---|
| Prioritized next action with justification | PROBLEM_MECHANISM_FIT | ASSUMPTION_INVENTORY |
| Remaining unknowns named with precision | ASSUMPTION_INVENTORY | EXPERTISE_GAP_AWARENESS |
| Proof-of-concept objective defined | EXPERTISE_GAP_AWARENESS | ASSUMPTION_INVENTORY |
| Uncertainty reduction articulated | EXPERTISE_GAP_AWARENESS | PROBLEM_MECHANISM_FIT |

All four exit requirements are covered by the three canonical gap types jointly.

---

## 4. TAXONOMY COMPLETENESS ASSESSMENT

### 4.1 Does the Canonical Taxonomy Cover the Stage 3 Purpose?

From STAGE3_PURPOSE_CLARIFICATION §1: Stage 3 primary purpose is developing the inventor's ability to bridge mechanism understanding and implementation orientation.

PROBLEM_MECHANISM_FIT: bridges mechanism description to problem-solution fit. Covered.
ASSUMPTION_INVENTORY: bridges mechanism understanding to implementation prerequisite awareness. Covered.
EXPERTISE_GAP_AWARENESS: bridges implementation orientation to concrete next-step capability. Covered.

The three canonical gap types jointly cover the Stage 3 purpose as defined.

### 4.2 Is Expansion Currently Justified?

No additional gap type is proposed in this document. The evidence base does not currently support identifying a fourth gap type satisfying all five expansion criteria in STAGE3_GAP_FOUNDATION_ANALYSIS §2 simultaneously.

---

## 5. WHAT THIS PROPOSAL DOES NOT DEFINE

- No questions are authored for any gap type
- No evaluation model is proposed
- No substance signals are defined
- No exit conditions are specified
- No ordering is finalized (§3.1 is a design proposal subject to refinement)
- No implementation is authorized
- No domain expansion is authorized

---

## 6. NEXT DESIGN ARTIFACTS

If this taxonomy is accepted, the correct sequence is:

1. Stage 3 Evidence Definition -- defining what constitutes valid evidence for each gap type
2. Stage 3 Evaluation Model -- defining REASONED quality criteria for each gap type
3. Stage 3 Question Design -- authoring questions for each gap type
4. Stage 3 Exit Criteria -- defining exit conditions compatible with SR-001 §4 evidence standard

Evidence definition precedes evaluation design because Stage 3 evaluates inventor capability through demonstrated evidence rather than procedural compliance.

Each step requires separate owner authorization per STAGE3_DESIGN_AUTHORIZATION §2.

**Design Risk 1 -- Taxonomy must not silently become an evaluation model.**
Defining gap types is not the same as defining evidence, evaluation logic, signals, scoring, or progression rules. A common failure mode is moving directly from taxonomy to questions and scoring before establishing what constitutes valid evidence. This conflicts with the Evidence First principles established throughout the governance chain.

**Design Risk 2 -- Protocol Learning must be explicitly addressed in evidence design.**
The evidence model must distinguish between genuine inventor development, protocol familiarity, and answer-pattern optimization. Procedural compliance must not be treated as evidence of inventor growth. SR-001 §3.7 (Transfer of Reasoning) establishes this as the primary test for distinguishing genuine development from protocol learning.

---

*This proposal is produced to be accurate, not reassuring.*
*Taxonomy defines what is assessed. It does not define how.*
*The minimal canonical foundation is sufficient for the Stage 3 purpose as currently defined.*
*Expansion requires evidence, not anticipation.*
