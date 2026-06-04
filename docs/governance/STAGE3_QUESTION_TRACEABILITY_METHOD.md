# STAGE3_QUESTION_TRACEABILITY_METHOD.md
## Stage 3 Question Traceability Method

**Document ID:** STAGE3_QUESTION_TRACEABILITY_METHOD
**Type:** Governance Method Artifact
**Governance Level:** Level 3
**Status:** ADMITTED
**Date:** 2026-06-03
**Provenance:** Owner Authorization -- pre-Question Design
**Depends on:** STAGE3_QUESTION_DESIGN_AUTHORIZATION, STAGE3_GAP_EVIDENCE_MODEL, STAGE3_CAPABILITY_MODEL, STAGE3_GAP_RESOLUTION_MODEL

---

## PURPOSE OF THIS DOCUMENT

This document defines the traceability method that every Stage 3 question must satisfy before being admitted.

Every question must declare:
- One Primary Evidence Target
- One Associated Capability
- One Associated Resolution Condition
- Question type (Primary or Conditional Probe)
- If Conditional Probe: the trigger condition

No question may be admitted without a complete traceability record. No question may declare more than one Primary Evidence Target.

---

## 1. RISK AJ MITIGATION

Risk AJ (Evidence Overlap): multiple questions appear distinct but evaluate the same evidence item.

Mitigation: the one-primary-evidence-target constraint. If two questions share the same Primary Evidence Target, one of them is either:
- A Conditional Probe of the other (permitted, with trigger condition declared), or
- Redundant (not permitted without owner justification)

A question that targets multiple evidence items does not have architectural clarity. Split it or escalate.

---

## 2. THE TRACEABILITY CHAIN

Every question occupies one position in a four-level chain:

Question
  targets one Primary Evidence Target (from STAGE3_GAP_EVIDENCE_MODEL)
    demonstrates one Associated Capability (from STAGE3_CAPABILITY_MODEL)
      satisfies one Associated Resolution Condition (from STAGE3_GAP_RESOLUTION_MODEL)

The chain is deterministic. Given a question, its architectural purpose must be unambiguous.

---

## 3. TRACEABILITY RECORD SCHEMA

Every question must be documented with the following fields:

**Q-ID:** Unique question identifier. Format: [GAP_TYPE]-Q[NUMBER]. Example: PMF-Q1, AI-Q2, EGA-Q3.

**Question Text:** The question as presented to the inventor.

**Question Type:** One of:
- PRIMARY -- stands alone, elicits evidence directly
- CONDITIONAL_PROBE -- follows a primary question, triggered by a defined condition

**Trigger Condition (Conditional Probe only):** The specific condition in the primary question response that activates this probe. Must be a defined absence or ambiguity in evidence, not an evaluator judgment.

**Primary Evidence Target:** One evidence item ID from STAGE3_GAP_EVIDENCE_MODEL. Format: [GAP_TYPE]-E[NUMBER]. Example: PMF-E1, AI-E2, EGA-E3.

**Associated Capability:** One capability ID from STAGE3_CAPABILITY_MODEL. Format: [GAP_TYPE]-CAP. Example: PMF-CAP, AI-CAP, EGA-CAP.

**Associated Resolution Condition:** One resolution condition ID from STAGE3_GAP_RESOLUTION_MODEL. Format: [GAP_TYPE]-R[NUMBER]. Example: PMF-R1, AI-R2, EGA-R3.

**Domain-Agnostic Validation:** Confirmation that the question applies without modification to at least two domain contexts. Required per SC-5 in STAGE3_QUESTION_DESIGN_AUTHORIZATION.

**Protocol Learning Resistance Note:** A brief statement of why this question is unlikely to be answered correctly through pattern matching alone.

---

## 4. COMPLETE TRACEABILITY MAP

The following table defines the complete authorized traceability space for Stage 3 questions.
Every admitted question must map to one row in this table as its Primary Evidence Target.

| Evidence Item | Capability | Resolution Condition | Gap Type |
|---|---|---|---|
| PMF-E1 | PMF-CAP | PMF-R1 | PROBLEM_MECHANISM_FIT |
| PMF-E2 | PMF-CAP | PMF-R2 | PROBLEM_MECHANISM_FIT |
| PMF-E3 | PMF-CAP | PMF-R3 | PROBLEM_MECHANISM_FIT |
| AI-E1  | AI-CAP  | AI-R1  | ASSUMPTION_INVENTORY |
| AI-E2  | AI-CAP  | AI-R2  | ASSUMPTION_INVENTORY |
| AI-E3  | AI-CAP  | AI-R3  | ASSUMPTION_INVENTORY |
| EGA-E1 | EGA-CAP | EGA-R1 | EXPERTISE_GAP_AWARENESS |
| EGA-E2 | EGA-CAP | EGA-R2 | EXPERTISE_GAP_AWARENESS |
| EGA-E3 | EGA-CAP | EGA-R3 | EXPERTISE_GAP_AWARENESS |

Nine rows. Nine authorized Primary Evidence Targets. A question outside this table has no architectural authorization.

---

## 5. QUESTION TYPE GOVERNANCE

### 5.1 PRIMARY Questions

- One per evidence item minimum (required for SC-1 coverage completeness)
- Stand alone -- do not depend on prior question responses
- Must be answerable by any inventor regardless of prior Stage 3 experience
- Must be domain-agnostic

### 5.2 CONDITIONAL_PROBE Questions

- One per evidence item maximum without owner justification
- Trigger condition must be defined as a specific observable absence in the primary question response
- Must not expand the evidence target -- probes the same evidence item as the primary question
- Maximum probing depth: 2 levels (primary → probe). No probe of a probe.
- Must not be evaluator-driven. Trigger condition is pre-defined, not discretionary.

### 5.3 Coherence Questions

- Authorized under QD-A5 (STAGE3_QUESTION_DESIGN_AUTHORIZATION)
- Target cross-gap coherence per CCT-1, CCT-2, CCT-3
- Traceability record modified for coherence questions:
  -- Primary Evidence Target: replaced by Coherence Test Target (CCT-1, CCT-2, or CCT-3)
  -- Associated Capability: IOC (per IOC_POSITION_STATEMENT)
  -- Associated Resolution Condition: SL-R2
- Maximum: one primary coherence question per CCT (three total)
- Conditional Probe permitted for coherence questions under same depth limit

---

## 6. VALIDATION RULES

Before a question is admitted to the Stage 3 question set:

**VR-1: Traceability record complete.**
All required fields in §3 are populated.

**VR-2: Primary Evidence Target is unique within question type.**
No two PRIMARY questions share the same Primary Evidence Target. If two candidates share a target, one must be designated as CONDITIONAL_PROBE or one must be eliminated.

**VR-3: Trigger condition is defined for all probes.**
No CONDITIONAL_PROBE is admitted without an explicit, pre-defined trigger condition that does not require evaluator judgment.

**VR-4: Probing depth limit respected.**
No probe targets a question that is itself a probe.

**VR-5: Domain-agnostic validation completed.**
The question has been reviewed against at least two domain contexts.

**VR-6: No prohibited content.**
Question text contains no scoring language, no progression language, no capability definitions, no resolution conditions. Questions elicit -- they do not evaluate.

---

## 7. EXAMPLE TRACEABILITY RECORD

The following is a structural example only. It demonstrates the record format. It is not an authorized question.

Q-ID: PMF-Q1
Question Type: PRIMARY
Trigger Condition: N/A
Primary Evidence Target: PMF-E1
Associated Capability: PMF-CAP
Associated Resolution Condition: PMF-R1
Domain-Agnostic Validation: Applicable to electronics (capacitive sensor), solar (collection mechanism), medical (device mechanism) without modification
Protocol Learning Resistance Note: Requires inventor to articulate problem independently -- cannot be answered by restating mechanism description

---

## 8. WHAT THIS DOCUMENT DOES NOT AUTHORIZE

- No actual questions are authored here
- No evaluation mechanics
- No scoring
- No progression logic
- No implementation
- No new architecture layers

---

*This document is produced to be accurate, not reassuring.*
*Every question must know its architectural purpose before it is written.*
*Traceability is not bureaucracy -- it is the mechanism that prevents question inflation, evidence overlap, and protocol drift.*
