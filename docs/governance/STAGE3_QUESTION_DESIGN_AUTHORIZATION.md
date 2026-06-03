# STAGE3_QUESTION_DESIGN_AUTHORIZATION.md
## Stage 3 Question Design Authorization

**Document ID:** STAGE3_QUESTION_DESIGN_AUTHORIZATION
**Type:** Governance Authorization Artifact
**Governance Level:** Level 3
**Status:** AUTHORIZED
**Date:** 2026-06-03
**Provenance:** Owner Authorization -- post Design Readiness Gate closure
**Depends on:** STAGE3_EVALUATION_MODEL, STAGE3_GAP_EVIDENCE_MODEL, STAGE3_CAPABILITY_MODEL

---

## 1. BASIS FOR AUTHORIZATION

Question Design is authorized because the Design Readiness Gate is closed.

| Gate Criterion | Status |
|---|---|
| QD-T1: IOC_POSITION_STATEMENT admitted | Satisfied -- 2993479 |
| QD-T2: STAGE3_ARCHITECTURE_COMPLETION_CRITERIA admitted | Satisfied -- 2993479 |
| QD-T3: STAGE3_READINESS_DECISION naming update completed | Satisfied -- e31b631 |
| QD-T4: No open architecture blocker | Satisfied |

Architecture Completion Gate is closed (AC-1 through AC-5 satisfied).
No active JC trigger exists.
No unresolved architectural question has been identified.

The burden of proof has shifted. Question Design does not require further justification to proceed. Any proposal for additional architectural work must pass the AE Test and identify a blocked design decision.

---

## 2. SCOPE OF QUESTION DESIGN

Question Design is authorized to produce questions for each of the three Stage 3 canonical gap types:

- PROBLEM_MECHANISM_FIT
- ASSUMPTION_INVENTORY
- EXPERTISE_GAP_AWARENESS

Questions must be designed to elicit the evidence items defined in STAGE3_GAP_EVIDENCE_MODEL. Each question must be traceable to at least one evidence item.

Question Design operates within the seven-layer architecture already established. It does not modify any layer.

---

## 3. WHAT QUESTION DESIGN IS AUTHORIZED TO CREATE

**QD-A1: Questions for PROBLEM_MECHANISM_FIT.**
Questions designed to elicit PMF-E1 (independent problem articulation), PMF-E2 (causal fit justification), and PMF-E3 (fit boundary awareness). Questions must target the underlying capability PMF-CAP, not the surface form of a correct answer.

**QD-A2: Questions for ASSUMPTION_INVENTORY.**
Questions designed to elicit AI-E1 (named assumptions beyond known gaps), AI-E2 (load-bearing classification with reasoning), and AI-E3 (assumption provenance awareness). Questions must be designed to surface assumptions the inventor had not previously recognized.

**QD-A3: Questions for EXPERTISE_GAP_AWARENESS.**
Questions designed to elicit EGA-E1 (named expertise with implementation justification), EGA-E2 (self-assessment with reasoning), and EGA-E3 (consequence awareness specific to mechanism). Questions must connect expertise identification to the inventor's specific implementation path.

**QD-A4: Follow-up probing questions.**
Questions designed to test whether initial responses represent genuine capability or protocol familiarity. Must be traceable to the Transfer of Reasoning test (SR-001 §3.7) and the Capability Coherence Requirement (STAGE3_CAPABILITY_MODEL §5.2).

**QD-A5: Coherence probing questions.**
Questions designed to assess cross-gap coherence per CCT-1, CCT-2, and CCT-3 (STAGE3_EVALUATION_MODEL §1.5). These questions probe whether the inventor's PMF-CAP, AI-CAP, and EGA-CAP demonstrations are mutually consistent.

---

## 4. WHAT QUESTION DESIGN IS PROHIBITED FROM CREATING

**QD-P1: No new gap types.**
Question Design may not introduce gap types beyond the three canonical types. New gap types require STAGE3_GAP_TAXONOMY_PROPOSAL amendment and owner authorization.

**QD-P2: No new evidence items.**
Question Design may not introduce evidence items beyond those in STAGE3_GAP_EVIDENCE_MODEL. If a question appears to require a new evidence item, this must be escalated per STAGE3_EVALUATION_MODEL §7.

**QD-P3: No new capabilities.**
Question Design may not define new capabilities. Capabilities are defined in STAGE3_CAPABILITY_MODEL.

**QD-P4: No new resolution conditions.**
Question Design may not introduce resolution conditions. Resolution conditions are defined in STAGE3_GAP_RESOLUTION_MODEL.

**QD-P5: No scoring.**
Question Design may not introduce scoring, weighting, ranking, confidence levels, or any evaluation metric. Scoring Design is not authorized.

**QD-P6: No progression logic.**
Question Design may not define when gaps are considered closed, when stage transitions occur, or how progression is triggered. Progression Logic is not authorized.

**QD-P7: No implementation.**
Question Design produces governance artifacts only. No engine changes, no evaluation logic changes, no platform changes.

**QD-P8: No new architectural layers.**
Question Design may not introduce new conceptual layers to the Stage 3 architecture. The seven-layer architecture is complete. Architecture Relapse (Risk AG) applies.

**QD-P9: No evaluation model extensions.**
Question Design may not extend or modify STAGE3_EVALUATION_MODEL. If evaluation mechanics appear insufficient, this is an escalation trigger, not a Question Design scope item.

---

## 5. RELATIONSHIP BETWEEN QUESTION DESIGN AND EXISTING ARTIFACTS

Question Design is downstream of all seven architectural layers. It consumes definitions; it does not produce them.

| Artifact | Relationship to Question Design |
|---|---|
| STAGE3_GAP_TAXONOMY_PROPOSAL | Defines the gap types questions address |
| STAGE3_GAP_EVIDENCE_MODEL | Defines the evidence items questions must elicit |
| STAGE3_CAPABILITY_MODEL | Defines the capabilities questions must develop |
| STAGE3_GAP_RESOLUTION_MODEL | Defines the resolution conditions questions must enable |
| STAGE3_EVALUATION_MODEL | Defines how question responses are assessed |
| IOC_POSITION_STATEMENT | Governs coherence probing question design |
| STAGE3_ARCHITECTURE_COMPLETION_CRITERIA | Governs scope boundaries for Question Design |

If a question cannot be traced to an evidence item in STAGE3_GAP_EVIDENCE_MODEL, it does not belong in Stage 3 Question Design.

If a question appears to require a new evidence item, it is an escalation trigger per STAGE3_EVALUATION_MODEL §7 -- not a justification for expanding question scope.

---

## 6. SUCCESS CRITERIA FOR QUESTION DESIGN COMPLETION

Question Design is considered complete when all of the following are satisfied:

**SC-1: Coverage completeness.**
At least one question exists for each of the nine evidence items (PMF-E1/E2/E3, AI-E1/E2/E3, EGA-E1/E2/E3).

**SC-2: Capability traceability.**
Every question can be traced to at least one evidence item and through that to at least one capability.

**SC-3: Protocol learning resistance.**
For each gap type, at least one probing question exists that tests whether improvement transfers to an unfamiliar aspect of the same mechanism (Transfer of Reasoning test, SR-001 §3.7).

**SC-4: Coherence coverage.**
At least one question exists for each of the three Auditable Contradiction Tests (CCT-1, CCT-2, CCT-3).

**SC-5: Domain-agnostic validity.**
All questions are reviewed against at least two domain contexts (electronics and one other) to confirm domain-agnostic applicability per SA-001B §2.4.

**SC-6: No prohibited content.**
No question introduces scoring, progression logic, new evidence items, new capabilities, or new resolution conditions.

**SC-7: Owner review completed.**
The question set is reviewed and explicitly authorized by the owner before any implementation work begins.

---

## 7. ESCALATION PROTOCOL

If during Question Design any of the following are discovered, they must be escalated -- not resolved inline:

- A required evidence item not in STAGE3_GAP_EVIDENCE_MODEL
- A capability dimension not covered by PMF-CAP, AI-CAP, or EGA-CAP
- A coherence requirement not covered by CCT-1, CCT-2, or CCT-3
- A domain context in which questions systematically fail domain-agnostic validity

Escalation means: record the finding, reference the artifact that should govern it, and seek owner authorization before proceeding.

---

## 8. EXPLICIT PROHIBITIONS SUMMARY

The following work remains unauthorized after this authorization:

- Scoring Design
- Progression Logic Design
- Stage 3 Implementation
- New architectural layers
- New gap types
- New evidence items
- New capabilities
- New resolution conditions
- Evaluation model extensions
- Exit Criteria Design (requires separate authorization)
- Stage 4 Design (requires separate authorization)

---

## 9. RISK REGISTER FOR QUESTION DESIGN PHASE

**Risk AG -- Architecture Relapse:** architecture artifacts proposed during Question Design without AE Test and blocked decision identification. Mitigation: QD-P8 prohibition. Any architecture proposal during this phase is rejected unless it passes AE Test.

**Risk U -- Hidden Scoring Emergence:** scoring concepts appearing implicitly in question language. Mitigation: QD-P5 prohibition. Questions are reviewed for scoring language before admission.

**Risk B -- Protocol Learning:** questions that train pattern recognition rather than develop capability. Mitigation: SC-3 probing question requirement and Transfer of Reasoning test.

**Risk D -- Evidence Overfitting:** questions implicitly tied to electronics domain. Mitigation: SC-5 domain-agnostic validation requirement.

---

*This document authorizes Question Design.*
*It does not authorize scoring, progression logic, implementation, or new architectural layers.*
*Question Design consumes architectural definitions. It does not produce them.*
*The seven-layer Stage 3 architecture is complete. The burden of proof has shifted.*
