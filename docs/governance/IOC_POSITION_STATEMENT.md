# IOC_POSITION_STATEMENT.md
## Implementation-Orientation Capability -- Architectural Position Statement

**Document ID:** IOC_POSITION_STATEMENT
**Type:** Architectural Position Statement
**Governance Level:** Level 3
**Status:** PROPOSED -- PENDING OWNER ADMISSION DECISION
**Date:** 2026-06-03
**Provenance:** Owner Request -- post IOC_ARCHITECTURAL_POSITION_ANALYSIS admission
**Depends on:** IOC_ARCHITECTURAL_POSITION_ANALYSIS, STAGE3_CAPABILITY_MODEL, STAGE3_GAP_RESOLUTION_MODEL, STAGE3_EVALUATION_MODEL

---

## PURPOSE OF THIS DOCUMENT

This document formally establishes the architectural position of the Implementation-Orientation Capability (IOC). It stabilizes IOC before it influences subsequent Stage 3 design artifacts.

IOC is currently doing architectural work -- governing SL-R2 and SL-R3 -- without an explicit architectural address. This document gives it that address. It does not redesign any existing artifact. It does not introduce new capabilities, evidence items, or evaluation mechanics.

---

## 1. WHAT IOC IS

IOC is the emergent Stage-Level property that arises when PMF-CAP, AI-CAP, and EGA-CAP are demonstrated coherently as an integrated whole.

It is the integrated epistemic state that Stage 3 is designed to develop: the ability to reason about an invention from an implementation-oriented perspective -- knowing what the invention is for (PMF-CAP), what is being assumed about it (AI-CAP), and what expertise is required to advance it (EGA-CAP) -- as a coherent, mutually consistent picture.

IOC is what makes it possible for an inventor to produce the Stage 3 exit characterization (SA-001A §6): a prioritized next action with justification, remaining unknowns named with precision, a proof-of-concept objective, and articulated uncertainty reduction. These outputs require all three component capabilities working together. IOC is the governing concept that explains why.

---

## 2. WHAT IOC IS NOT

### 2.1 IOC Is Not a Fourth Capability

A capability has independent evidence items and can be assessed independently of other capabilities. IOC has no evidence items that are not already present in STAGE3_GAP_EVIDENCE_MODEL. IOC cannot be demonstrated without demonstrating PMF-CAP, AI-CAP, and EGA-CAP -- it has no independent demonstration path.

Introducing IOC-CAP as a fourth formal capability would duplicate the content of the three component capabilities (Risk X). IOC is assessed through the coherence of its components, not through additional evidence.

### 2.2 IOC Is Not a Resolution Condition

A resolution condition defines a specific state that must be satisfied for a gap to be considered no longer an obstacle. IOC is not a condition -- it is the concept that explains why SL-R2 and SL-R3 exist as conditions. Resolution conditions are derived from IOC; they are not IOC itself.

Adding IOC as a resolution condition would be circular: IOC governs the conditions; the conditions do not govern IOC.

### 2.3 IOC Is Not Merely an Explanatory Abstraction

An explanatory abstraction can be removed without architectural loss. IOC cannot. Without IOC as a governing concept:
- SL-R2 (cross-gap coherence) has no governing principle -- it becomes three disconnected tests
- SL-R3 (exit characterization) has no explanation for why it cannot be satisfied by per-gap aggregation
- The distinction between stage-level resolution and per-gap resolution has no theoretical basis

IOC does real architectural work. It is not decorative.

### 2.4 IOC Is Not a Progression Requirement

Progression is governed by SA-001A §11 and the transition authorization mechanism (deferred per STAGE_EVOLUTION_POSITION §5.1). IOC governs resolution, not progression. Stage-level resolution (which IOC governs) is a necessary but not sufficient condition for progression -- progression requires transition authorization that is separately defined.

### 2.5 IOC Is Not an Evaluation Mechanic

IOC is not evaluated directly. It is assessed indirectly through the three Auditable Contradiction Tests (CCT-1, CCT-2, CCT-3) in STAGE3_EVALUATION_MODEL. The CCTs are expressions of IOC coherence -- they are not IOC itself. Embedding IOC inside evaluation logic would violate Risk P (resolution saturation).

---

## 3. HOW IOC RELATES TO STAGE-LEVEL RESOLUTION

IOC is the governing concept behind SL-R2 and SL-R3 in STAGE3_GAP_RESOLUTION_MODEL.

**SL-R2 (Cross-gap coherence):** exists because IOC requires that the three component capabilities be demonstrated coherently, not independently. The three Auditable Contradiction Tests (CCT-1, CCT-2, CCT-3) are the operational expression of IOC coherence.

**SL-R3 (Exit characterization reached):** exists because IOC is what makes the SA-001A §6 exit characterization achievable. The four exit characterization elements cannot be produced by any single component capability. They require the integrated implementation-oriented perspective that IOC represents.

**Why stage-level resolution is not the sum of per-gap resolutions:** an inventor who satisfies all nine per-gap resolution conditions (PMF-R1/R2/R3, AI-R1/R2/R3, EGA-R1/R2/R3) has demonstrated each component capability sufficiently. But if those demonstrations are contradictory or disconnected, IOC has not emerged. SL-R2 and SL-R3 exist to verify that IOC has emerged -- not merely that components are present.

---

## 4. HOW IOC RELATES TO EXIT CHARACTERIZATION

The SA-001A §6 exit characterization is the observable output of IOC, not IOC itself.

An inventor who has developed IOC can produce the exit characterization because they have the integrated implementation-oriented perspective required to:
- Identify a prioritized next action (requires PMF-CAP + AI-CAP + EGA-CAP synthesis)
- Name remaining unknowns with precision (requires AI-CAP + EGA-CAP coherence)
- Define a proof-of-concept objective (requires AI-CAP load-bearing classification + EGA-CAP consequence reasoning)
- Articulate uncertainty reduction (requires PMF-CAP + AI-CAP + EGA-CAP integrated picture)

The exit characterization is how IOC is made visible. It is not IOC's definition. An inventor who produces exit characterization outputs without the underlying integrated capability has performed the outputs, not developed the capability.

---

## 5. CONSTRAINTS GOVERNING FUTURE EMERGENT PROPERTIES

IOC is the first emergent property recognized in the Stage 3 architecture. Its recognition establishes a precedent. To prevent Risk AA (emergent property proliferation), any future emergent property must satisfy the following admission criteria before recognition:

**Criterion 1 -- Architectural work requirement:**
The proposed emergent property must be doing real architectural work that cannot be removed without loss. If removing the concept leaves the architecture intact, it is an abstraction, not an emergent property.

**Criterion 2 -- Non-reducibility:**
The proposed emergent property must not be reducible to the sum of its components. If it can be fully expressed by combining existing definitions, it is a derived concept, not an emergent one.

**Criterion 3 -- No independent evidence requirement:**
An emergent property must not require independent evidence items. If it requires new evidence to assess, it is a capability, not an emergent property.

**Criterion 4 -- Existing artifact derivation:**
The emergent property must be derivable from and consistent with existing committed artifacts. A property that requires modifying existing artifacts to accommodate it is a design change, not an emergent recognition.

**Criterion 5 -- Owner authorization:**
No emergent property may be recognized without explicit owner decision. IOC was authorized through the IOC_ARCHITECTURAL_POSITION_ANALYSIS admission.

---

## 6. ARCHITECTURAL STATUS SUMMARY

| Question | Answer |
|---|---|
| Is IOC a capability? | No -- no independent evidence items, no independent demonstration path |
| Is IOC a resolution condition? | No -- it governs conditions, not a condition itself |
| Is IOC an explanatory abstraction? | No -- it does real architectural work |
| Is IOC a progression requirement? | No -- progression is separately governed |
| Is IOC an evaluation mechanic? | No -- it is assessed through CCTs, not directly evaluated |
| What is IOC? | Emergent Stage-Level property arising from coherent PMF-CAP + AI-CAP + EGA-CAP demonstration |
| Where does IOC appear in the architecture? | As the governing concept behind SL-R2 and SL-R3 |
| How is IOC assessed? | Indirectly, through CCT-1, CCT-2, and CCT-3 |
| What are IOC outputs? | The SA-001A §6 exit characterization elements |

---

## 7. WHAT THIS DOCUMENT DOES NOT CHANGE

- STAGE3_CAPABILITY_MODEL is unchanged
- STAGE3_GAP_RESOLUTION_MODEL is unchanged
- STAGE3_EVALUATION_MODEL is unchanged
- No new capabilities introduced
- No new evidence items introduced
- No new resolution conditions introduced
- No scoring introduced
- No progression rules introduced
- No implementation authorized

---

*This document is produced to be accurate, not reassuring.*
*IOC is real. It is emergent. It is not a capability, a condition, an abstraction, or a mechanic.*
*It is the governing concept that explains why stage-level resolution is not reducible to per-gap resolution.*
*This document gives it an architectural address without distorting the architecture to accommodate it.*
