# STAGE3_CAPABILITY_MODEL.md
## Stage 3 Capability Model

**Document ID:** STAGE3_CAPABILITY_MODEL
**Type:** Design Artifact
**Governance Level:** Level 3
**Status:** PROPOSED -- PENDING OWNER ADMISSION DECISION
**Date:** 2026-06-03
**Provenance:** Owner Authorization -- post STAGE3_GAP_EVIDENCE_MODEL admission
**Depends on:** SR-001, STAGE3_GAP_EVIDENCE_MODEL, STAGE3_PURPOSE_CLARIFICATION

---

## PURPOSE OF THIS DOCUMENT

This document defines what capability means in Stage 3 -- what the inventor can now do that could not be demonstrated before Stage 3 began.

Capability is defined independently of gap resolution and progression decisions. This separation is intentional and governed by Risk K below. A capability is a demonstrated inventor ability. Whether that ability is sufficient to resolve a gap is a separate question addressed in STAGE3_GAP_RESOLUTION_MODEL.

No evaluation logic is proposed here. No gap resolution criteria are defined. No progression rules are introduced. No scoring is proposed.

---

## 1. WHAT CAPABILITY MEANS IN STAGE 3

### 1.1 Governing Definition

A Stage 3 capability is a demonstrated inventor ability that:
- Was not required to be demonstrated in Stage 2
- Reflects implementation-oriented reasoning rather than mechanism description
- Can be observed through evidence items defined in STAGE3_GAP_EVIDENCE_MODEL
- Belongs to the inventor -- it is not platform-supplied structure

Capability answers: what can the inventor now do that could not be demonstrated before?

Capability does not answer: has the inventor done enough to proceed? That is gap resolution.

### 1.2 The Capability Layer in the Architecture

The emerging architecture is:

Gap Types -- what is assessed
Evidence Items -- what is observed
Capabilities -- what the inventor can do (this document)
Gap Resolution -- whether demonstrated capability is sufficient (STAGE3_GAP_RESOLUTION_MODEL)
Progression -- whether resolved gaps justify stage transition (SA-001A §11, transition mechanism TBD)

Each layer is distinct. Capability sits between evidence and resolution. It is not reducible to evidence accumulation and it does not imply resolution.

### 1.3 Risk K -- Resolution Leakage

Risk K is the risk that capability definitions begin to include progression or resolution language -- collapsing the distinction between demonstrating capability, resolving a gap, and progressing to a new stage.

Mitigation in this document: every capability definition is stated in terms of what the inventor can do, not in terms of what the inventor has completed or whether they are ready to proceed. Resolution language is explicitly excluded from capability definitions.

---

## 2. CAPABILITY MODEL: PROBLEM_MECHANISM_FIT

### 2.1 Capability Name

PMF-CAP: Problem-Mechanism Fit Reasoning

### 2.2 Capability Definition

The inventor can reason about the relationship between their mechanism and the problem it is intended to solve -- articulating the problem independently, providing causal justification for the fit, and identifying the conditions under which the fit holds and where it does not.

### 2.3 What This Capability Looks Like When Present

An inventor with PMF-CAP demonstrated:
- States the problem in terms that are distinguishable from the mechanism description
- Provides a reasoned account of why the mechanism addresses the problem
- Identifies at least one condition where the fit is limited or absent
- Maintains consistency between problem articulation, mechanism description, and fit reasoning across the conversation

### 2.4 What This Capability Looks Like When Absent

An inventor without PMF-CAP:
- Restates the mechanism when asked to describe the problem
- Asserts fit without providing causal reasoning
- Cannot identify any condition under which the mechanism would not address the problem
- Produces internally inconsistent fit reasoning when probed from different angles

### 2.5 Relationship to Evidence Items

PMF-CAP is supported by PMF-E1 (independent problem articulation), PMF-E2 (causal fit justification), and PMF-E3 (fit boundary awareness) from STAGE3_GAP_EVIDENCE_MODEL.

The capability is more than the sum of the evidence items. An inventor who produces PMF-E1, PMF-E2, and PMF-E3 in isolation but cannot connect them coherently has not demonstrated PMF-CAP. The capability requires that the evidence items are consistent with and support each other as an integrated reasoning act.

### 2.6 Stage 3 Specificity

PMF-CAP is Stage 3-specific because Stage 2 does not require the inventor to reason about the problem independently of the mechanism. Stage 2 evaluates whether the mechanism is well-described. PMF-CAP evaluates whether the inventor can reason about what the mechanism is for -- a qualitatively different epistemic act.

### 2.7 Risk K Check

PMF-CAP is defined as a reasoning ability, not a completion state. It does not contain resolution language. Whether PMF-CAP is sufficient to resolve the PROBLEM_MECHANISM_FIT gap is determined by STAGE3_GAP_RESOLUTION_MODEL, not by this definition.

---

## 3. CAPABILITY MODEL: ASSUMPTION_INVENTORY

### 3.1 Capability Name

AI-CAP: Assumption Identification and Classification

### 3.2 Capability Definition

The inventor can identify assumptions underlying their mechanism and implementation path that were not previously recognized as assumptions, classify those assumptions by their criticality to implementation success, and distinguish between assumptions they are making and gaps they have already identified.

### 3.3 What This Capability Looks Like When Present

An inventor with AI-CAP demonstrated:
- Names assumptions that were not surfaced as gaps in Stage 2
- Distinguishes load-bearing assumptions from peripheral ones with reasoning
- Identifies at least one assumption they were not aware of making before Stage 3
- Maintains consistency between named assumptions and their stated mechanism

### 3.4 What This Capability Looks Like When Absent

An inventor without AI-CAP:
- Produces a list of Stage 2 gaps relabeled as assumptions
- Cannot distinguish between load-bearing and peripheral assumptions
- Names only assumptions they had already acknowledged in Stage 2
- Produces assumption lists that are disconnected from their specific mechanism

### 3.5 Relationship to Evidence Items

AI-CAP is supported by AI-E1 (named assumptions beyond known gaps), AI-E2 (load-bearing classification with reasoning), and AI-E3 (assumption provenance awareness) from STAGE3_GAP_EVIDENCE_MODEL.

The capability requires integration: the inventor must demonstrate that they can identify, classify, and trace assumptions as a connected reasoning act -- not produce three separate correct responses to three separate questions.

### 3.6 Stage 3 Specificity

AI-CAP is Stage 3-specific because Stage 2 asks the inventor to identify what they do not know. AI-CAP asks the inventor to identify what they are assuming -- a different epistemic act. An inventor can identify zero gaps and still be making load-bearing assumptions. Stage 2 does not surface this. Stage 3 does.

### 3.7 Risk K Check

AI-CAP is defined as an identification and classification ability, not a completion state. Whether AI-CAP is sufficient to resolve the ASSUMPTION_INVENTORY gap is determined by STAGE3_GAP_RESOLUTION_MODEL.

---

## 4. CAPABILITY MODEL: EXPERTISE_GAP_AWARENESS

### 4.1 Capability Name

EGA-CAP: Expertise Gap Identification and Consequence Reasoning

### 4.2 Capability Definition

The inventor can identify the domain expertise their implementation requires that they do not currently possess, assess their own knowledge relative to those requirements, and reason about the consequences of those gaps for their specific implementation path.

### 4.3 What This Capability Looks Like When Present

An inventor with EGA-CAP demonstrated:
- Names expertise domains required for implementation with justification
- Distinguishes domains where they have working knowledge from those where they do not
- Articulates what would happen to their specific implementation if an expertise gap were not resolved
- Connects expertise gaps to the assumptions identified in AI-CAP

### 4.4 What This Capability Looks Like When Absent

An inventor without EGA-CAP:
- Lists expertise areas without connecting them to implementation requirements
- Cannot distinguish between domains they know and domains they do not
- Produces generic statements about the importance of expertise without specificity to their mechanism
- Reproduces Stage 2 boundary ambiguity content relabeled as expertise gaps

### 4.5 Relationship to Evidence Items

EGA-CAP is supported by EGA-E1 (named expertise with implementation justification), EGA-E2 (self-assessment with reasoning), and EGA-E3 (consequence awareness specific to mechanism) from STAGE3_GAP_EVIDENCE_MODEL.

The capability requires that the inventor connects expertise identification, self-assessment, and consequence reasoning as an integrated act directed at their specific implementation path -- not as three independent responses.

### 4.6 Stage 3 Specificity

EGA-CAP is Stage 3-specific and has no Stage 1 equivalent per SA-001A §6. It requires the implementation-oriented perspective that Stage 3 develops. An inventor cannot meaningfully evaluate expertise gaps until they have sufficient mechanism understanding to know what implementation requires -- which Stage 2 establishes.

### 4.7 Risk K Check

EGA-CAP is defined as an identification and reasoning ability, not a completion state. Whether EGA-CAP is sufficient to resolve the EXPERTISE_GAP_AWARENESS gap is determined by STAGE3_GAP_RESOLUTION_MODEL.

---

## 5. CROSS-CAPABILITY RELATIONSHIPS

### 5.1 Capability Integration

The three capabilities are not independent. They form a coherent picture of the Stage 3 epistemic state:

PMF-CAP establishes what the invention is for. This scopes AI-CAP -- assumptions are about a mechanism intended to solve a specific problem. AI-CAP surfaces what is being assumed. This informs EGA-CAP -- expertise gaps are those required to validate or resolve the load-bearing assumptions about an invention intended to solve a specific problem.

An inventor who demonstrates all three capabilities coherently has reached the Stage 3 epistemic state described in STAGE3_PURPOSE_CLARIFICATION §1: the ability to bridge mechanism understanding and implementation orientation.

### 5.2 Capability Coherence Requirement

Capabilities must be coherent across gap types, not merely present in each. An inventor who demonstrates PMF-CAP, AI-CAP, and EGA-CAP independently but produces contradictions between them -- naming fit boundaries that contradict their assumption inventory, or identifying expertise gaps unrelated to their load-bearing assumptions -- has not demonstrated the integrated Stage 3 epistemic state.

This is a capability-level requirement, not an evidence-item requirement. It cannot be satisfied by checklist completion.

### 5.3 Protocol Learning Detection

Risk B (protocol learning) at the capability level: an inventor who produces correct capability demonstrations for familiar aspects of their mechanism but fails to maintain coherence when probed on unfamiliar aspects has demonstrated protocol familiarity, not genuine Stage 3 capability.

The Transfer of Reasoning test from SR-001 §3.7 applies at the capability level: genuine capability transfers across different aspects of the same invention. Protocol learning produces correct isolated responses but fails under integration probing.

---

## 6. CAPABILITY SUMMARY

| Capability ID | Name | Core Ability | Stage 3 Specific |
|---|---|---|---|
| PMF-CAP | Problem-Mechanism Fit Reasoning | Reason about mechanism-problem relationship | Yes -- Stage 2 does not require it |
| AI-CAP | Assumption Identification and Classification | Identify and classify unrecognized assumptions | Yes -- different from identifying known gaps |
| EGA-CAP | Expertise Gap Identification and Consequence Reasoning | Identify expertise gaps and reason about consequences | Yes -- no Stage 1 or Stage 2 equivalent |

Three capabilities. Each Stage 3-specific. Each defined independently of resolution and progression.

---

## 7. WHAT THIS DOCUMENT DOES NOT DEFINE

- No gap resolution criteria
- No sufficiency thresholds
- No evaluation model
- No scoring
- No questions
- No progression rules
- No implementation
- No domain expansion

---

## 8. NEXT DESIGN ARTIFACT

STAGE3_GAP_RESOLUTION_MODEL.md -- defining when demonstrated capability is sufficient to consider a gap no longer an obstacle.

Gap resolution must not be defined inside this document. It is a separate governance question.

Owner authorization required before gap resolution model design begins.

---

*This document is produced to be accurate, not reassuring.*
*Capability is what the inventor can do. Resolution is whether it is enough. Progression is whether resolved gaps justify transition.*
*These are three distinct questions. This document answers only the first.*
