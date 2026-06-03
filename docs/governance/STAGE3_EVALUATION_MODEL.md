# STAGE3_EVALUATION_MODEL.md
## Stage 3 Evaluation Model

**Document ID:** STAGE3_EVALUATION_MODEL
**Type:** Design Artifact
**Governance Level:** Level 3
**Status:** PROPOSED -- PENDING OWNER ADMISSION DECISION
**Date:** 2026-06-03
**Provenance:** Owner Authorization -- post STAGE3_GAP_RESOLUTION_MODEL admission
**Depends on:** STAGE3_GAP_RESOLUTION_MODEL, STAGE3_CAPABILITY_MODEL, STAGE3_GAP_EVIDENCE_MODEL

---

## PURPOSE OF THIS DOCUMENT

This document defines how Stage 3 evidence, capabilities, and resolution conditions are evaluated. It does not define new gap types, evidence items, capabilities, or resolution conditions. All of those are defined in prior artifacts in the Stage 3 design chain.

The Evaluation Model sits between resolution definitions and evaluation mechanics. It answers: given the evidence items, capabilities, and resolution conditions already defined, how do we assess whether they have been demonstrated?

No scoring is proposed. No progression rules are introduced. No questions are authored.

---

## 1. GOVERNING CONSTRAINTS

### 1.1 What This Document Does Not Define

This document explicitly does not define:
- Gap types (defined in STAGE3_GAP_TAXONOMY_PROPOSAL)
- Evidence items (defined in STAGE3_GAP_EVIDENCE_MODEL)
- Capabilities (defined in STAGE3_CAPABILITY_MODEL)
- Resolution conditions (defined in STAGE3_GAP_RESOLUTION_MODEL)

Any evaluation mechanic that appears to introduce a new capability or resolution condition must be escalated back to the appropriate governing artifact. The Evaluation Model evaluates existing definitions -- it does not extend them.

### 1.2 Risk P -- Resolution Saturation Constraint

Every evaluation mechanic in this document references a specific resolution condition from STAGE3_GAP_RESOLUTION_MODEL. If an evaluation mechanic cannot be traced to an existing resolution condition, it does not belong in this document.

### 1.3 Risk R -- Evaluation Leakage Constraint

If the evaluation process surfaces a gap not covered by existing definitions -- a capability not defined, a resolution condition not established -- that observation must be recorded as an open item and escalated to the appropriate artifact. It must not be resolved inline within evaluation mechanics.

### 1.4 Risk S -- Detection/Capability Distinction

Four layers remain distinct throughout this document:

Detection Signals -- observable patterns in inventor responses that suggest evidence may be present.
Evidence -- demonstrated instances of inventor capability as defined in STAGE3_GAP_EVIDENCE_MODEL.
Capability -- integrated inventor ability as defined in STAGE3_CAPABILITY_MODEL.
Resolution -- judgment that demonstrated capability satisfies resolution conditions in STAGE3_GAP_RESOLUTION_MODEL.

Detection signals are not evidence. Evidence is not capability. Capability is not resolution. Each layer requires a distinct assessment act.

### 1.5 Risk Q -- Coherence as Auditable Contradiction Tests

Cross-gap coherence (SL-R2) is evaluated through three auditable contradiction tests, not through open-ended qualitative judgment:

CCT-1: Internal consistency -- does the problem statement in PMF-CAP align with the assumptions in AI-CAP?
CCT-2: Dependency alignment -- are the expertise gaps in EGA-CAP connected to the load-bearing assumptions in AI-CAP?
CCT-3: Problem-path alignment -- does the exit characterization next action follow logically from PMF-CAP, AI-CAP, and EGA-CAP combined?

A coherence failure requires at least one auditable contradiction. Uncertainty, partial knowledge, and acknowledged unknowns are not coherence failures.

---

## 2. EVALUATION ARCHITECTURE

### 2.1 Four Evaluation Acts

Stage 3 evaluation requires four distinct acts, in sequence:

**Act 1 -- Evidence Detection:** identifying observable patterns in inventor responses that suggest evidence items may be present. Detection is not confirmation.

**Act 2 -- Evidence Confirmation:** determining whether detected patterns constitute genuine evidence items as defined in STAGE3_GAP_EVIDENCE_MODEL. Evidence is confirmed when the inventor's response demonstrates the underlying capability indicator -- not merely produces the expected surface form.

**Act 3 -- Capability Assessment:** determining whether confirmed evidence items, taken together, demonstrate the capability as defined in STAGE3_CAPABILITY_MODEL. Capability assessment is an integration judgment -- it cannot be performed on evidence items in isolation.

**Act 4 -- Resolution Judgment:** determining whether demonstrated capabilities satisfy the resolution conditions in STAGE3_GAP_RESOLUTION_MODEL. Resolution judgment is applied per-gap first, then at stage level.

### 2.2 Why the Sequence Cannot Be Collapsed

Act 1 without Act 2 produces false positives -- detection signals mistaken for evidence.
Act 2 without Act 3 produces fragmentation -- evidence items collected without capability integration (Risk G).
Act 3 without Act 4 produces capability isolation -- capability demonstrated without resolution judgment (Risk M).
Act 4 without Acts 1-3 produces checklist progression -- resolution claimed without evidence or capability (Risk H).

---

## 3. EVIDENCE EVALUATION: PROBLEM_MECHANISM_FIT

### 3.1 Detection Signals for PMF Evidence

The following patterns suggest PMF evidence may be present. They are detection signals, not confirmation:
- Inventor uses language that distinguishes problem context from mechanism operation
- Inventor provides a reason why the mechanism addresses the problem rather than asserting it
- Inventor acknowledges a scenario where the mechanism would not solve the problem

### 3.2 Evidence Confirmation Criteria

**PMF-E1 confirmed when:** the inventor's problem statement remains stable and independent when the mechanism description is set aside. Test: ask the inventor to describe the problem without reference to their mechanism. If the problem description collapses, PMF-E1 is not confirmed.

**PMF-E2 confirmed when:** the inventor provides a causal chain from a mechanism property to a problem requirement that is specific to their mechanism. Generic fit assertions or domain-standard explanations do not confirm PMF-E2. Test: the causal chain must be traceable to the inventor's specific mechanism, not to category-level knowledge.

**PMF-E3 confirmed when:** the inventor identifies a fit limit that is specific to their mechanism-problem relationship -- not a generic limitation of the technology category. Test: the fit limit must reference the inventor's specific context, not a textbook limitation.

### 3.3 PMF-CAP Assessment

PMF-CAP is assessed as demonstrated when PMF-E1, PMF-E2, and PMF-E3 are all confirmed AND are internally consistent. Consistency test: the problem articulation in PMF-E1 must be compatible with the fit reasoning in PMF-E2 and the fit limits in PMF-E3. An inventor who produces correct isolated responses but whose problem statement contradicts their fit limits has not demonstrated PMF-CAP.

### 3.4 PMF Resolution Evaluation

PMF-R1 evaluated by: confirming PMF-E1 stability under probing.
PMF-R2 evaluated by: confirming PMF-E2 causal specificity and inventor ownership.
PMF-R3 evaluated by: confirming PMF-E3 mechanism-specificity.

PMF gap resolved when PMF-R1, PMF-R2, and PMF-R3 are all satisfied and PMF-CAP coherence is confirmed.

---

## 4. EVIDENCE EVALUATION: ASSUMPTION_INVENTORY

### 4.1 Detection Signals for AI Evidence

- Inventor uses conditional language about their mechanism (if X is true, then...)
- Inventor distinguishes between what they know and what they are taking as given
- Inventor identifies something they had not previously considered as an assumption

### 4.2 Evidence Confirmation Criteria

**AI-E1 confirmed when:** the named assumption is not a restatement of a Stage 2 gap and is specific to the inventor's mechanism-problem relationship established in PMF-CAP. Test: compare named assumptions against Stage 2 gap records. Assumptions that map directly to known Stage 2 gaps do not confirm AI-E1.

**AI-E2 confirmed when:** the inventor provides a reason for classifying an assumption as load-bearing or peripheral that references their specific implementation path. Test: the justification must connect the assumption to a consequence -- what would happen to the implementation if this assumption were wrong.

**AI-E3 confirmed when:** the inventor names an assumption and acknowledges it was not previously recognized as an assumption. Test: the assumption must be absent from Stage 2 gap records and from prior Stage 3 responses -- it must be genuinely new to the inventor's awareness.

### 4.3 AI-CAP Assessment

AI-CAP is assessed as demonstrated when AI-E1, AI-E2, and AI-E3 are all confirmed AND are scoped to the problem-mechanism relationship established in PMF-CAP. An assumption inventory that is disconnected from the PMF-CAP problem articulation has not demonstrated AI-CAP -- it has demonstrated generic assumption awareness.

### 4.4 AI Resolution Evaluation

AI-R1 evaluated by: confirming AI-E1 distinction from Stage 2 gaps.
AI-R2 evaluated by: confirming AI-E2 load-bearing justification specificity.
AI-R3 evaluated by: confirming AI-E3 provenance novelty.

AI gap resolved when AI-R1, AI-R2, and AI-R3 are all satisfied and AI-CAP coherence with PMF-CAP is confirmed.

---

## 5. EVIDENCE EVALUATION: EXPERTISE_GAP_AWARENESS

### 5.1 Detection Signals for EGA Evidence

- Inventor distinguishes between domains they understand and domains they do not
- Inventor connects an expertise requirement to a specific implementation step
- Inventor articulates a consequence of an expertise gap for their specific mechanism

### 5.2 Evidence Confirmation Criteria

**EGA-E1 confirmed when:** the named expertise domain is connected to a specific implementation requirement that follows from the inventor's mechanism and assumptions. Test: the expertise-implementation connection must reference the inventor's specific mechanism, not a generic implementation of the technology category.

**EGA-E2 confirmed when:** the inventor's self-assessment distinguishes known from unknown with reasoning that references their specific background and their specific implementation requirements. Test: a self-assessment that could apply to any inventor in the domain is not specific enough to confirm EGA-E2.

**EGA-E3 confirmed when:** the inventor articulates a consequence of an expertise gap that is specific to their implementation path -- what would specifically happen to their mechanism or their implementation timeline if the gap were not resolved. Test: generic consequences about implementation difficulty do not confirm EGA-E3.

### 5.3 EGA-CAP Assessment

EGA-CAP is assessed as demonstrated when EGA-E1, EGA-E2, and EGA-E3 are all confirmed AND are connected to the load-bearing assumptions identified in AI-CAP. An expertise gap identification that is disconnected from the assumption inventory has not demonstrated EGA-CAP -- it has demonstrated generic expertise awareness.

### 5.4 EGA Resolution Evaluation

EGA-R1 evaluated by: confirming EGA-E1 implementation specificity.
EGA-R2 evaluated by: confirming EGA-E2 self-assessment specificity.
EGA-R3 evaluated by: confirming EGA-E3 consequence mechanism-specificity.

EGA gap resolved when EGA-R1, EGA-R2, and EGA-R3 are all satisfied and EGA-CAP coherence with AI-CAP is confirmed.

---

## 6. STAGE-LEVEL EVALUATION

### 6.1 SL-R1 Evaluation

All nine per-gap resolution conditions satisfied. This is verified by completing §3.4, §4.4, and §5.4.

### 6.2 SL-R2 Evaluation -- Coherence via Auditable Contradiction Tests

**CCT-1 -- Internal consistency:**
Compare the problem statement from PMF-E1 with the assumptions from AI-E1 and AI-E2.
Contradiction present if: the problem articulation assumes something that the assumption inventory identifies as load-bearing and unvalidated without acknowledgment.
Contradiction absent if: the assumption inventory is scoped to the problem-mechanism relationship established in PMF-CAP.

**CCT-2 -- Dependency alignment:**
Compare the load-bearing assumptions from AI-E2 with the expertise gaps from EGA-E1.
Contradiction present if: a load-bearing assumption requires domain expertise to validate, but that expertise domain is not identified in EGA-CAP.
Contradiction absent if: every load-bearing assumption has a corresponding expertise gap or the inventor has demonstrated sufficient knowledge to not require external expertise for that assumption.

**CCT-3 -- Problem-path alignment:**
Assess whether the inventor can identify a prioritized next action that follows logically from PMF-CAP + AI-CAP + EGA-CAP combined.
Contradiction present if: the proposed next action addresses a peripheral assumption while load-bearing assumptions with identified expertise gaps remain unaddressed.
Contradiction absent if: the next action addresses the most critical uncertainty given the combined capability picture.

SL-R2 satisfied when all three CCTs pass -- no auditable contradictions found.

### 6.3 SL-R3 Evaluation -- Exit Characterization

SA-001A §6 exit characterization requires four elements. Each is evaluated as follows:

**Prioritized next action with justification:**
The inventor identifies one next action AND provides a justification that references their PMF-CAP problem articulation, AI-CAP load-bearing assumptions, and EGA-CAP expertise gaps. A next action without justification tracing to all three capabilities does not satisfy this element.

**Remaining unknowns named with precision:**
The inventor names remaining unknowns that are specific and bounded -- not generic statements of uncertainty. The unknowns must be traceable to unresolved assumptions from AI-CAP or unresolved expertise gaps from EGA-CAP.

**Proof-of-concept objective defined:**
The inventor defines what a proof-of-concept would test -- specifically which load-bearing assumption it would validate or refute. A proof-of-concept objective that does not connect to a specific load-bearing assumption does not satisfy this element.

**Uncertainty reduction articulated:**
The inventor articulates how their uncertainty has reduced since Stage 2 entry. This requires comparing their current state (post-Stage 3) with their Stage 2 exit state. Reduction must be specific -- naming what was uncertain before and what is now better understood.

SL-R3 satisfied when all four exit characterization elements are demonstrated with the specificity described above.

---

## 7. ESCALATION PROTOCOL

If during evaluation any of the following are discovered, they must be escalated -- not resolved inline:

- A capability required for evaluation not defined in STAGE3_CAPABILITY_MODEL
- A resolution condition implicitly required but not in STAGE3_GAP_RESOLUTION_MODEL
- A coherence test that cannot be expressed as an auditable contradiction
- An evidence item that appears necessary but is not in STAGE3_GAP_EVIDENCE_MODEL

Escalation means: record the finding as an open item, reference the artifact that should govern it, and do not proceed with evaluation of the affected condition until the governing artifact is updated.

---

## 8. WHAT THIS DOCUMENT DOES NOT DEFINE

- No new gap types
- No new evidence items
- No new capabilities
- No new resolution conditions
- No scoring
- No questions
- No progression rules
- No transition authorization mechanism
- No implementation
- No domain expansion

---

## 9. NEXT DESIGN ARTIFACT

STAGE3_QUESTION_DESIGN.md -- authoring questions for each gap type, grounded in the evidence items and evaluation mechanics established in this document.

Questions must be designed to elicit the evidence items defined in STAGE3_GAP_EVIDENCE_MODEL. They must not introduce new evidence requirements or resolution conditions.

Owner authorization required before question design begins.

---

*This document is produced to be accurate, not reassuring.*
*Detection signals are not evidence. Evidence is not capability. Capability is not resolution.*
*The Evaluation Model assesses existing definitions. It does not extend them.*
*Coherence is bounded by three auditable contradiction tests, not by open-ended judgment.*
