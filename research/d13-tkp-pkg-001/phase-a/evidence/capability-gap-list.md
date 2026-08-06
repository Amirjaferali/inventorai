# Phase A Output 3 — Capability-Gap List

**Purpose (bounded, future-needs only).** Identify capability gaps between what InventorAI can currently do (read-only,
from repository structure) and what the `D13-TKP-PKG-001` sensor→microcontroller interfacing guidance would require. Each
entry follows the approved capability-gap schema. **This output identifies future needs only. It authorizes no research,
testing, validation, specialist involvement, or implementation.** No engineering fact is asserted; no RQ is answered; no
external source was accessed. No named person or company appears — where expertise is referenced it is by evidence
category/specialist *category* only, and only when necessary.

---

### CG-01 — No structured sensor-output classification
- **Exact unresolved technical subproblem:** the platform cannot deterministically classify a case's sensor output as analog-voltage / single-ended-digital / pulse-frequency from a typed field.
- **Affected user outcome:** the inventor cannot receive routed interfacing guidance keyed to their signal type.
- **Missing information or evidence:** a typed sensor-output classification field (MF-01) and the classification logic that would consume it.
- **What InventorAI can currently verify:** that a component/description was captured as free text; domain classification signals (`domains/electronics_electrical/domain.json`).
- **What InventorAI cannot currently verify:** the actual signal type of a given case, in a structured/deterministic way.
- **Precise technology / research topic / subdomain:** low-voltage single-signal sensor output typing (analog vs single-ended digital vs pulse/frequency).
- **Suggested search terms:** "sensor output signal type classification", "analog vs digital sensor interface", "pulse/frequency sensor output".
- **Required validation / measurements / documents / tests / tools (future, unauthorized):** governing-parameter documentation review under an authorized method; no measurement in scope.
- **Uncertainty / abstention:** classification method is not defined in the repository; abstention appropriate until a field + rule exist.
- **Specialist category (only if necessary):** not necessary at this stage (structural, not judgment-bound).
- **Status:** IDENTIFIED — FUTURE NEED — NOT AUTHORIZED.

### CG-02 — No voltage-range compatibility indication
- **Exact unresolved technical subproblem:** the platform cannot indicate whether a sensor output voltage range is compatible with a target input range.
- **Affected user outcome:** the inventor is not alerted to a potential voltage-range mismatch.
- **Missing information or evidence:** structured sensor output voltage range (MF-02) and target MCU input range (MF-03).
- **What InventorAI can currently verify:** presence of free-text power observations (`power_observations_ar`, "no assumed values").
- **What InventorAI cannot currently verify:** any numeric voltage relationship (explicitly out of scope — no calculation permitted).
- **Precise technology / research topic / subdomain:** electrical voltage-range compatibility (RQ-02, RQ-03 subject area).
- **Suggested search terms:** "sensor output voltage range", "microcontroller input voltage range", "voltage level compatibility".
- **Required validation / measurements / documents / tests / tools (future, unauthorized):** governing-parameter documentation (voltage ranges) under an authorized DOCUMENT REVIEW method; no calculation/measurement now.
- **Uncertainty / abstention:** high; no numeric fields exist; abstention appropriate.
- **Specialist category (only if necessary):** not necessary at this structural stage.
- **Status:** IDENTIFIED — FUTURE NEED — NOT AUTHORIZED.

### CG-03 — No ADC-reference / digital-logic-level compatibility capability
- **Exact unresolved technical subproblem:** the platform cannot indicate ADC-reference/input-range fit or single-ended digital logic-level compatibility.
- **Affected user outcome:** no guidance on whether a signal is readable by the target MCU's ADC or digital input.
- **Missing information or evidence:** target MCU input characteristics (MF-03), signal type (MF-01).
- **What InventorAI can currently verify:** nothing structured about the target device's input stage.
- **What InventorAI cannot currently verify:** ADC reference/input-range fit; logic-level thresholds (RQ-05, RQ-06 subject area).
- **Precise technology / research topic / subdomain:** ADC reference/input range; single-ended digital logic-level compatibility.
- **Suggested search terms:** "ADC reference voltage input range", "logic level compatibility CMOS TTL", "single-ended digital input threshold".
- **Required validation / measurements / documents / tests / tools (future, unauthorized):** governing-parameter documentation under an authorized method; no test/measurement now.
- **Uncertainty / abstention:** high; abstention appropriate.
- **Specialist category (only if necessary):** not necessary at this structural stage.
- **Status:** IDENTIFIED — FUTURE NEED — NOT AUTHORIZED.

### CG-04 — No pulse/frequency compatibility capability
- **Exact unresolved technical subproblem:** the platform cannot address pulse/frequency signal compatibility with a target input.
- **Affected user outcome:** no guidance for pulse/frequency-output sensors.
- **Missing information or evidence:** pulse/frequency characteristics field (MF-04); target input capability.
- **What InventorAI can currently verify:** nothing structured about pulse/frequency signals.
- **What InventorAI cannot currently verify:** pulse/frequency interfacing suitability (RQ-07 subject area).
- **Precise technology / research topic / subdomain:** pulse/frequency signal interfacing to microcontroller inputs.
- **Suggested search terms:** "frequency output sensor interfacing", "pulse counting microcontroller input", "frequency-to-digital input".
- **Required validation / measurements / documents / tests / tools (future, unauthorized):** governing-parameter documentation under an authorized method.
- **Uncertainty / abstention:** high; abstention appropriate.
- **Specialist category (only if necessary):** not necessary at this structural stage.
- **Status:** IDENTIFIED — FUTURE NEED — NOT AUTHORIZED.

### CG-05 — No impedance/loading relevance capability
- **Exact unresolved technical subproblem:** the platform cannot indicate when source/load impedance is relevant to a case.
- **Affected user outcome:** no signal about loading effects that could affect signal integrity.
- **Missing information or evidence:** impedance context field (MF-05).
- **What InventorAI can currently verify:** nothing structured about impedance.
- **What InventorAI cannot currently verify:** loading relevance (RQ-04 subject area).
- **Precise technology / research topic / subdomain:** source/load impedance and loading effects in low-voltage sensor interfacing.
- **Suggested search terms:** "sensor output impedance loading", "input impedance ADC loading effect", "buffer amplifier high impedance sensor".
- **Required validation / measurements / documents / tests / tools (future, unauthorized):** governing-parameter documentation under an authorized method.
- **Uncertainty / abstention:** moderate–high; abstention appropriate.
- **Specialist category (only if necessary):** not necessary at this structural stage.
- **Status:** IDENTIFIED — FUTURE NEED — NOT AUTHORIZED.

### CG-06 — No datasheet-sufficiency / abstention capability for interfacing
- **Exact unresolved technical subproblem:** the platform cannot signal whether governing parameters are sufficiently available, nor produce a principled interfacing-specific abstention.
- **Affected user outcome:** the inventor is not told when the input is insufficient to advise on interfacing specifically.
- **Missing information or evidence:** governing-parameter availability indicator (MF-06); interfacing abstention field (MF-09).
- **What InventorAI can currently verify:** a generic `feasibility_signal=INSUFFICIENT_INPUT` and a generic `missing_information` section.
- **What InventorAI cannot currently verify:** interfacing-parameter sufficiency specifically (RQ-09, RQ-11 subject area).
- **Precise technology / research topic / subdomain:** datasheet/governing-parameter sufficiency; principled abstention.
- **Suggested search terms:** "datasheet key parameters sensor interface", "sufficient information to specify interface", "abstention criteria technical advice".
- **Required validation / measurements / documents / tests / tools (future, unauthorized):** governing-parameter documentation review under an authorized method; independent governance review of the abstention rule.
- **Uncertainty / abstention:** this gap is itself about abstention; abstention appropriate.
- **Specialist category (only if necessary):** governance/technical reviewer category may be needed later to validate an abstention rule — recorded as a category only, no person/company.
- **Status:** IDENTIFIED — FUTURE NEED — NOT AUTHORIZED.

### CG-07 — No structured method-routing capability (routing distinct from execution)
- **Exact unresolved technical subproblem:** the platform cannot record which method a case would route to (DOCUMENT REVIEW vs DATASHEET COMPARISON vs abstention) without executing it.
- **Affected user outcome:** no transparent routing decision separate from (still-unauthorized) execution.
- **Missing information or evidence:** method-routing trigger field (MF-08); signal type (MF-01); parameter-availability indicator (MF-06).
- **What InventorAI can currently verify:** the authorized RQ envelope names a method-routing trigger (RQ-10) but the repository defines no routing field.
- **What InventorAI cannot currently verify:** the routing outcome for a given case.
- **Precise technology / research topic / subdomain:** decision routing for single-signal interfacing guidance.
- **Suggested search terms:** "decision routing rules technical guidance", "method selection criteria", "diagnostic routing without execution".
- **Required validation / measurements / documents / tests / tools (future, unauthorized):** owner/governance definition of routing rules; no method executed now.
- **Uncertainty / abstention:** moderate; routing rule undefined; abstention appropriate.
- **Specialist category (only if necessary):** not necessary at this structural stage.
- **Status:** IDENTIFIED — FUTURE NEED — NOT AUTHORIZED.

---

**Bounding note.** CG-01…CG-07 correspond to the authorized RQ-01…RQ-11 envelope's structural prerequisites; they are the
capability gaps most directly implied by the concept class. Capability gaps outside the concept class (multi-signal, bus,
differential, wireless, mains, high-power, safety-critical) are intentionally excluded (see `unresolved-issues.md`, UI-2).
This list is a future-needs record; it authorizes nothing.
