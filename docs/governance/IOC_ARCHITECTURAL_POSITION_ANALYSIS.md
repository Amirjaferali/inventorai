# IOC_ARCHITECTURAL_POSITION_ANALYSIS.md
## Implementation-Orientation Capability -- Architectural Position Analysis

**Document ID:** IOC_ARCHITECTURAL_POSITION_ANALYSIS
**Type:** Design Analysis Paper
**Governance Level:** Level 3
**Status:** PROPOSED -- PENDING OWNER ADMISSION DECISION
**Date:** 2026-06-03
**Provenance:** Owner Request -- post STAGE3_EVALUATION_MODEL admission
**Depends on:** STAGE3_CAPABILITY_MODEL, STAGE3_GAP_RESOLUTION_MODEL, STAGE3_EVALUATION_MODEL

---

## PURPOSE OF THIS DOCUMENT

This document determines the architectural status of the Implementation-Orientation Capability (IOC) before any modification to existing artifacts or introduction of new capabilities.

IOC was identified during Risk M analysis as a possible integrated capability formed by PMF-CAP, AI-CAP, and EGA-CAP working together. Its architectural status is currently undetermined. This analysis determines what IOC is before deciding how it should be governed.

No modifications to STAGE3_CAPABILITY_MODEL are made here. No new capabilities are introduced. No question design begins.

---

## 1. THE FIVE INTERPRETATIONS

Five possible architectural positions for IOC are evaluated:

Interpretation A -- IOC is a true independent capability, distinct from and not reducible to PMF-CAP, AI-CAP, and EGA-CAP.
Interpretation B -- IOC is an emergent capability created by integration of the three component capabilities.
Interpretation C -- IOC is a Stage-Level property, not a capability at all.
Interpretation D -- IOC is part of Exit Characterization, not Capability Architecture.
Interpretation E -- IOC is an explanatory abstraction with no independent architectural status.

---

## 2. EVIDENCE FROM THE GOVERNANCE CHAIN

### 2.1 Evidence Supporting Interpretation A -- True Independent Capability

For IOC to be a true independent capability, it must:
- Assess a dimension of inventor ability not covered by PMF-CAP, AI-CAP, or EGA-CAP
- Have evidence items that are distinct from those in STAGE3_GAP_EVIDENCE_MODEL
- Be demonstrable independently of the three component capabilities

Evidence review: No governance artifact defines a dimension of Stage 3 inventor ability that falls outside PMF-CAP, AI-CAP, and EGA-CAP. STAGE3_PURPOSE_CLARIFICATION §2 defines four Stage 3 capabilities that Stage 2 cannot provide -- all four map to the three canonical gap types. STAGE3_GAP_TAXONOMY_PROPOSAL §4.1 confirms the minimal taxonomy covers the Stage 3 purpose completely.

**Verdict: Evidence does not support Interpretation A.** IOC does not assess a dimension of inventor ability beyond the three component capabilities. Introducing it as an independent capability would create Risk X -- capability duplication.

### 2.2 Evidence Supporting Interpretation B -- Emergent Capability

For IOC to be emergent, the combination of PMF-CAP, AI-CAP, and EGA-CAP must produce something that none of them produces individually and that cannot be reduced to their sum.

Evidence review: STAGE3_CAPABILITY_MODEL §5.2 states: an inventor who demonstrates PMF-CAP, AI-CAP, and EGA-CAP independently but produces contradictions between them has not demonstrated the integrated Stage 3 epistemic state. This explicitly states that successful component demonstration does not imply the integrated state. SA-001A §6 exit characterization requires synthesis -- identifying a prioritized next action from the combined picture -- which no single component capability can produce.

This is the definition of emergence: a property of the whole not present in the parts.

**Verdict: Evidence strongly supports Interpretation B.** The integrated Stage 3 epistemic state is real, is required by SA-001A §6, and cannot be derived from component capabilities in isolation.

### 2.3 Evidence Supporting Interpretation C -- Stage-Level Property

For IOC to be a Stage-Level property, it must be a property of stage completion rather than a capability of the inventor.

Evidence review: STAGE3_GAP_RESOLUTION_MODEL SL-R2 and SL-R3 are stage-level resolution conditions that require the integrated epistemic state. They assess whether the stage has been completed, not whether the inventor has a capability. However, SL-R3 specifically requires the inventor to demonstrate synthesis -- identifying a next action, naming unknowns, defining proof-of-concept. This is something the inventor does, not a property of a stage.

**Verdict: Evidence partially supports Interpretation C.** IOC has stage-level effects -- it is required for stage-level resolution. But it manifests as inventor behavior, not as a stage property. Interpretation C captures part of the truth but is not the complete picture.

### 2.4 Evidence Supporting Interpretation D -- Part of Exit Characterization

For IOC to be part of Exit Characterization, it must be fully described by the SA-001A §6 exit characterization conditions.

Evidence review: SA-001A §6 exit characterization requires: prioritized next action with justification, remaining unknowns named with precision, proof-of-concept objective defined, uncertainty reduction articulated. These four elements together describe what an inventor with IOC can do at Stage 3 exit. STAGE3_EVALUATION_MODEL §6.3 evaluates SL-R3 by assessing these four elements.

The exit characterization does not define IOC -- it describes its observable outputs. IOC is what produces those outputs; the exit characterization is what those outputs look like.

**Verdict: Evidence supports Interpretation D as a partial description.** The exit characterization describes IOC outputs, not IOC itself. IOC is the underlying capability that produces the exit characterization outputs.

### 2.5 Evidence Supporting Interpretation E -- Explanatory Abstraction

For IOC to be merely an explanatory abstraction, removing it from the governance chain should produce no loss of evaluable content.

Evidence review: if IOC is removed, the governance chain retains: nine evidence items, three capabilities, twelve resolution conditions, and the exit characterization. The gap is SL-R2 -- cross-gap coherence. Without IOC as a concept, SL-R2 becomes three contradiction tests without a governing principle explaining why they matter. The CCTs become disconnected checks rather than expressions of a coherent requirement.

More critically: the question of why an inventor who passes all per-gap evaluations might still not have reached Stage 3 readiness cannot be answered without IOC. The concept is doing real explanatory work.

**Verdict: Evidence does not support Interpretation E.** IOC is not merely explanatory -- it governs the coherence requirement and explains why stage-level resolution is not reducible to per-gap resolution.

---

## 3. RISK X EVALUATION -- CAPABILITY DUPLICATION

Risk X: IOC becomes a formal capability that merely duplicates PMF-CAP, AI-CAP, and EGA-CAP combined.

Analysis: if IOC were formalized as IOC-CAP with its own evidence items, those evidence items would either:
- Duplicate existing evidence items (duplication confirmed), or
- Require new evidence items not in STAGE3_GAP_EVIDENCE_MODEL (evidence proliferation)

The exit characterization in SA-001A §6 is already captured in SL-R3 and evaluated in STAGE3_EVALUATION_MODEL §6.3. Formalizing IOC as a fourth capability with its own evaluation layer would recreate SL-R3 at the capability level -- duplication.

**Risk X conclusion:** Formalizing IOC as IOC-CAP with independent evidence items and evaluation mechanics would create capability duplication. The content IOC represents is already governed by SL-R2 and SL-R3. Formalization adds governance overhead without adding evaluable content.

---

## 4. RISK Y EVALUATION -- EMERGENT CAPABILITY AMBIGUITY

Risk Y: IOC influences Stage-Level Resolution without having a clearly defined architectural status.

This risk is currently active. IOC was named in Risk M analysis but has no formal definition in any committed artifact. SL-R2 and SL-R3 depend on the IOC concept without referencing it by name. The CCTs in STAGE3_EVALUATION_MODEL are expressions of IOC coherence without naming IOC as their governing principle.

**Risk Y conclusion:** IOC currently influences stage-level resolution implicitly. This creates governance ambiguity -- the concept is doing architectural work without having an architectural address. The risk is not eliminated by formalizing IOC as a capability (that creates Risk X) but must be resolved by giving IOC a defined architectural status.

---

## 5. ARCHITECTURAL POSITION DETERMINATION

From the evidence review:

Interpretation A: Not supported -- no independent evaluable content.
Interpretation B: Strongly supported -- IOC is emergent, not reducible to components.
Interpretation C: Partially supported -- IOC has stage-level effects but manifests as inventor behavior.
Interpretation D: Partially supported -- exit characterization describes IOC outputs, not IOC itself.
Interpretation E: Not supported -- IOC does real architectural work.

**Determined position: IOC is an emergent Stage-Level property that manifests as inventor behavior.**

More precisely: IOC is the integrated epistemic state that emerges when PMF-CAP, AI-CAP, and EGA-CAP are demonstrated coherently. It is not a fourth capability because it has no independent evidence items. It is not merely a stage property because it is demonstrated by the inventor, not implied by stage completion. It is the governing concept behind SL-R2 and SL-R3 -- the principle that explains why those conditions exist and why they cannot be reduced to per-gap aggregation.

---

## 6. RECOMMENDED ARCHITECTURAL TREATMENT

Given the determined position, the appropriate treatment for IOC is:

**Option 1 -- Name IOC explicitly in STAGE3_GAP_RESOLUTION_MODEL and STAGE3_EVALUATION_MODEL.**
Add a brief section to each document naming IOC as the governing concept behind SL-R2 and SL-R3. No new evidence items. No new capability definition. No modification to STAGE3_CAPABILITY_MODEL.

This resolves Risk Y (ambiguity) without creating Risk X (duplication).

**Option 2 -- Leave IOC unnamed but bounded by the CCTs.**
Accept that IOC operates as an unnamed governing concept, fully expressed through CCT-1, CCT-2, and CCT-3. Risk Y remains present but bounded -- the concept influences only SL-R2 and SL-R3, which are auditable.

**Option 3 -- Define IOC as a formal architectural concept in a standalone document.**
Create a brief document naming IOC as an emergent stage-level property, defining its relationship to the three component capabilities, and establishing it as the governing concept behind coherence evaluation. No capability definition, no evidence items, no evaluation mechanics.

**Recommendation: Option 1 or Option 3.**
Option 2 leaves Risk Y unresolved. Option 1 is lower overhead. Option 3 provides cleaner architectural documentation. The choice depends on whether IOC requires its own governance address or whether naming it within existing documents is sufficient.

---

## 7. WHAT THIS DOCUMENT DOES NOT DECIDE

- No modification to STAGE3_CAPABILITY_MODEL
- No introduction of IOC-CAP
- No new evidence items
- No question design
- No evaluation mechanics
- No scoring
- No implementation

---

*This document is produced to be accurate, not reassuring.*
*IOC is real. It is not a fourth capability. It is the emergent stage-level property that explains why stage-level resolution is not reducible to per-gap resolution.*
*Its architectural status must be explicit before Stage 3 design proceeds.*
