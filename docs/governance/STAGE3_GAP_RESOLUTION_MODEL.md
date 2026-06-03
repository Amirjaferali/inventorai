# STAGE3_GAP_RESOLUTION_MODEL.md
## Stage 3 Gap Resolution Model

**Document ID:** STAGE3_GAP_RESOLUTION_MODEL
**Type:** Design Artifact
**Governance Level:** Level 3
**Status:** PROPOSED -- PENDING OWNER ADMISSION DECISION
**Date:** 2026-06-03
**Provenance:** Owner Authorization -- post STAGE3_CAPABILITY_MODEL admission
**Depends on:** SR-001, STAGE3_CAPABILITY_MODEL, STAGE3_GAP_EVIDENCE_MODEL

---

## PURPOSE OF THIS DOCUMENT

This document defines what it means for a Stage 3 gap to be considered resolved -- and what it means for Stage 3 as a whole to be resolved.

Gap resolution is distinct from capability demonstration. An inventor can demonstrate a capability without that capability being sufficient to resolve the gap. Resolution is the judgment that the demonstrated capability has reduced the gap sufficiently that it is no longer an obstacle to the inventor's implementation-oriented reasoning.

This document does not define evaluation mechanics, scoring, or progression rules. It defines the concept of resolution and the conditions under which it applies.

---

## 1. GOVERNING DISTINCTIONS

### 1.1 The Three-Layer Distinction

From Risk G, Risk H, and the capability model analysis, three layers must remain distinct:

**Capability** -- what the inventor can do. Defined in STAGE3_CAPABILITY_MODEL.
**Gap Resolution** -- whether the demonstrated capability is sufficient to consider the gap no longer an obstacle. Defined in this document.
**Progression** -- whether resolved gaps justify stage transition. Governed by SA-001A §11 and the transition authorization mechanism (STAGE_EVOLUTION_POSITION §5.1, deferred).

None of these implies the next. Capability does not imply resolution. Resolution does not imply progression.

### 1.2 What Resolution Is Not

Gap resolution is not:
- Completion of evidence items (Risk H -- checklist progression)
- Demonstration of capability in isolation (Risk M -- capability isolation)
- Achievement of implementation success (Risk N -- resolution escalation)
- Automatic aggregation of per-gap resolutions into stage resolution (Risk O -- stage-level collapse)

### 1.3 What Resolution Is

A gap is resolved when the inventor has demonstrated sufficient capability that the gap no longer represents an obstacle to their implementation-oriented reasoning -- and when that demonstration is coherent with the capabilities demonstrated for the other gaps in Stage 3.

Resolution is a judgment, not a count. It requires evaluating whether the capability demonstrated is genuine, integrated, and sufficient -- not whether evidence items have been collected.

---

## 2. ACTIVE RISK REGISTER

**Risk G -- Evidence Fragmentation:** evidence items treated as independent achievements. Mitigated by requiring capability coherence before resolution.

**Risk H -- Checklist Progression:** E1+E2+E3 automatically implies gap resolved. Mitigated by §1.2 and the resolution judgment requirement in §3-5.

**Risk K -- Resolution Leakage:** resolution language entering capability definitions. Mitigated by keeping resolution definitions in this document, not in STAGE3_CAPABILITY_MODEL.

**Risk L -- Capability Equivalence:** capabilities treated as equally weighted. Mitigated by §6.1 which preserves the foundational/enabling/dependent structure.

**Risk M -- Capability Isolation:** capabilities evaluated independently. Mitigated by §6.2 stage-level resolution requiring integration coherence.

**Risk N -- Resolution Escalation:** resolution becomes equivalent to implementation success. Mitigated by §1.2 and the explicit scope boundaries in §3-5.

**Risk O -- Stage-Level Collapse:** stage resolution becomes aggregation of per-gap resolutions. Mitigated by §6 which explicitly separates per-gap from stage-level resolution.

---

## 3. PER-GAP RESOLUTION: PROBLEM_MECHANISM_FIT

### 3.1 Resolution Definition

The PROBLEM_MECHANISM_FIT gap is resolved when the inventor has demonstrated PMF-CAP sufficiently that the relationship between their mechanism and their intended problem is no longer an unexamined assumption -- the inventor has reasoned about it, articulated it, and identified its limits.

### 3.2 Resolution Conditions

PMF resolution requires all three of the following:

**PMF-R1: Independent problem articulation is stable.**
The inventor's problem statement holds independently of the mechanism description and remains consistent when probed from different angles. A problem statement that collapses back into mechanism description under probing has not been established.

**PMF-R2: Fit reasoning is causal and inventor-owned.**
The inventor's justification for why the mechanism addresses the problem is causal, specific to their mechanism, and demonstrably theirs -- not a restatement of platform questions or generic domain knowledge. An inventor who produces fit language without connecting it to their specific mechanism has not resolved this gap.

**PMF-R3: Fit limits are acknowledged.**
The inventor has identified at least one condition under which the fit is limited or does not hold. An inventor who cannot name any fit limit has not demonstrated genuine fit reasoning -- they have demonstrated fit assertion.

### 3.3 What Does Not Constitute Resolution

- Producing PMF-E1, PMF-E2, PMF-E3 sequentially without coherence between them
- Asserting fit without causal reasoning
- Acknowledging fit limits in generic terms not specific to their mechanism
- Demonstrating PMF-CAP in isolation while producing contradictions with AI-CAP or EGA-CAP

### 3.4 Risk N Check

PMF resolution does not require the mechanism to be correct, feasible, or implementable. It requires the inventor to have reasoned about the relationship between mechanism and problem. Implementation success is outside platform scope (SPV §4). Resolution is scoped to reasoning capability.

---

## 4. PER-GAP RESOLUTION: ASSUMPTION_INVENTORY

### 4.1 Resolution Definition

The ASSUMPTION_INVENTORY gap is resolved when the inventor has demonstrated AI-CAP sufficiently that their load-bearing assumptions are no longer invisible -- the inventor has named them, classified them, and identified at least one they were not previously aware of making.

### 4.2 Resolution Conditions

AI resolution requires all three of the following:

**AI-R1: Named assumptions are distinct from Stage 2 gaps.**
The inventor has named at least one assumption that was not already identified as a gap in Stage 2. An assumption inventory that consists entirely of relabeled Stage 2 gaps has not resolved this gap.

**AI-R2: Load-bearing classification is reasoned and stable.**
The inventor has classified their assumptions by criticality with reasoning, and that classification holds under probing. A classification that changes when questioned or that cannot be justified has not been established.

**AI-R3: Assumption provenance is demonstrated.**
The inventor has identified at least one assumption they were not aware of making before Stage 3. This is the primary evidence that assumption awareness has genuinely developed rather than been performed.

### 4.3 What Does Not Constitute Resolution

- Listing Stage 2 gaps relabeled as assumptions
- Producing a long list of assumptions without load-bearing classification
- Acknowledging that assumptions exist without naming them specifically
- Demonstrating AI-CAP in isolation while producing contradictions with PMF-CAP

### 4.4 Risk N Check

AI resolution does not require assumptions to be validated or resolved. It requires the inventor to have identified and classified them. Assumption validation is outside platform scope. Resolution is scoped to the inventor's awareness and classification capability.

---

## 5. PER-GAP RESOLUTION: EXPERTISE_GAP_AWARENESS

### 5.1 Resolution Definition

The EXPERTISE_GAP_AWARENESS gap is resolved when the inventor has demonstrated EGA-CAP sufficiently that the expertise required for their implementation path is no longer unacknowledged -- the inventor has named it, assessed their own knowledge relative to it, and understood its consequences for their specific mechanism.

### 5.2 Resolution Conditions

EGA resolution requires all three of the following:

**EGA-R1: Named expertise is connected to implementation requirements.**
The inventor has named expertise domains with justification for why their specific implementation requires them. Generic expertise acknowledgment without connection to the inventor's mechanism does not satisfy this condition.

**EGA-R2: Self-assessment is reasoned and specific.**
The inventor has distinguished between expertise domains where they have working knowledge and those where they do not, with reasoning specific to their mechanism and implementation path. Unqualified self-assessment does not satisfy this condition.

**EGA-R3: Consequence reasoning is mechanism-specific.**
The inventor has articulated what would happen to their specific implementation if the identified expertise gaps were not resolved. Generic statements about the importance of expertise do not satisfy this condition.

### 5.3 What Does Not Constitute Resolution

- Listing expertise areas without connecting them to implementation requirements
- Reproducing Stage 2 boundary ambiguity content as expertise gaps
- Acknowledging expertise gaps without consequence reasoning
- Demonstrating EGA-CAP in isolation while producing contradictions with AI-CAP

### 5.4 Risk N Check

EGA resolution does not require expertise gaps to be filled or implementation to be feasible. It requires the inventor to have identified, assessed, and reasoned about their expertise gaps. Expertise acquisition is outside platform scope. Resolution is scoped to awareness and consequence reasoning.

---

## 6. STAGE-LEVEL RESOLUTION

### 6.1 Why Stage-Level Resolution Is Not the Sum of Per-Gap Resolutions

Risk O identifies the failure mode: PMF resolved + AI resolved + EGA resolved automatically implies Stage 3 resolved.

This is incorrect for two reasons grounded in committed artifacts:

**Reason 1 -- Capability coherence requirement (STAGE3_CAPABILITY_MODEL §5.2).**
The three capabilities must be coherent across gap types. An inventor who resolves each gap independently but produces contradictions between them has not demonstrated the integrated Stage 3 epistemic state. Per-gap resolution does not verify cross-gap coherence. Stage-level resolution must.

**Reason 2 -- Implementation-Orientation Capability (from Risk M analysis).**
The three capabilities together form a larger integrated capability: the ability to reason about an invention from an implementation-oriented perspective. Stage-level resolution requires that this integrated capability is demonstrated -- not merely that its components are present.

### 6.2 Stage-Level Resolution Definition

Stage 3 is resolved at the stage level when:

**SL-R1: All three per-gap resolutions are satisfied.**
PMF-R1/R2/R3, AI-R1/R2/R3, and EGA-R1/R2/R3 are all met.

**SL-R2: Cross-gap coherence is demonstrated.**
The inventor's problem articulation, assumption inventory, and expertise gap identification are mutually consistent and reinforce each other. Contradictions between gap type responses that were not resolved during Stage 3 indicate that the integrated Stage 3 epistemic state has not been reached.

**SL-R3: Stage 3 exit characterization is reached.**
Per SA-001A §6, the inventor can: identify a prioritized next action with justification, name remaining unknowns with precision, define a proof-of-concept objective, and articulate how uncertainty has reduced since Stage 2 entry. This requires all three capabilities working together -- it cannot be satisfied by any single gap type resolution.

### 6.3 Why SL-R3 Cannot Be Derived from Per-Gap Resolutions

The Stage 3 exit characterization in SA-001A §6 requires synthesis, not aggregation. Identifying a prioritized next action requires knowing what problem is being solved (PMF-CAP), what is being assumed (AI-CAP), and what expertise is required (EGA-CAP) -- and reasoning about which next action addresses the most critical uncertainty given all three. This is a synthesis act that cannot be performed by summing per-gap resolutions.

### 6.4 Risk N Check at Stage Level

Stage-level resolution does not require implementation to have begun, expertise to be acquired, or assumptions to be validated. It requires the inventor to have reached the epistemic state where they can reason coherently about their invention from an implementation-oriented perspective. Stage 4 begins where Stage 3 ends -- it does not begin inside Stage 3.

---

## 7. RESOLUTION SUMMARY

| Level | Resolution ID | Condition |
|---|---|---|
| Per-Gap | PMF-R1 | Problem articulation stable under probing |
| Per-Gap | PMF-R2 | Fit reasoning causal and inventor-owned |
| Per-Gap | PMF-R3 | Fit limits acknowledged |
| Per-Gap | AI-R1 | Named assumptions distinct from Stage 2 gaps |
| Per-Gap | AI-R2 | Load-bearing classification reasoned and stable |
| Per-Gap | AI-R3 | Assumption provenance demonstrated |
| Per-Gap | EGA-R1 | Named expertise connected to implementation requirements |
| Per-Gap | EGA-R2 | Self-assessment reasoned and specific |
| Per-Gap | EGA-R3 | Consequence reasoning mechanism-specific |
| Stage-Level | SL-R1 | All nine per-gap conditions met |
| Stage-Level | SL-R2 | Cross-gap coherence demonstrated |
| Stage-Level | SL-R3 | SA-001A §6 exit characterization reached |

Twelve resolution conditions total. Nine per-gap. Three stage-level. Stage-level resolution requires all twelve.

---

## 8. WHAT THIS DOCUMENT DOES NOT DEFINE

- No evaluation model
- No scoring
- No questions
- No substance signals
- No progression rules
- No transition authorization mechanism (deferred per STAGE_EVOLUTION_POSITION §5.1)
- No implementation
- No domain expansion

---

## 9. NEXT DESIGN ARTIFACT

STAGE3_EVALUATION_MODEL.md -- defining evaluation mechanics for the resolution conditions established here.

The evaluation model must not introduce new resolution conditions. It must define how the conditions in this document are assessed.

Owner authorization required before evaluation model design begins.

---

*This document is produced to be accurate, not reassuring.*
*Capability is what the inventor can do.*
*Resolution is whether it is enough.*
*Stage-level resolution is not the sum of per-gap resolutions.*
*Progression is a separate question governed by SA-001A §11 and the transition authorization mechanism.*
