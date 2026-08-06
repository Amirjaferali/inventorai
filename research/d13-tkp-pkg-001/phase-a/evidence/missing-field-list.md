# Phase A Output 2 — Missing-Field List

**Purpose (bounded).** Identify structured fields the existing journey/application-state does **not** capture that would be
needed to populate the `D13-TKP-PKG-001` sensor→microcontroller interfacing guidance (RQ-01…RQ-11 concept class). Read-only
identification of missing structure only. "Why needed" references the authorized RQ envelope; it does **not** answer any RQ,
assert any electrical fact, or recommend acquisition. "Authorization required" flags that acquiring/using the field is a
separate owner decision. No named person or company appears.

| # | Missing field | Affected journey stage | Why needed (RQ linkage) | Information currently unavailable | Consequence of absence | Blocks a future RQ? | Proposed acquisition method (unauthorized) | Authorization required | Status |
|---|---|---|---|---|---|---|---|---|---|
| MF-01 | Sensor output signal type (analog-voltage / single-ended-digital / pulse-frequency) as a typed field | Capture / Stage 2 | Governs which RQ path applies (RQ-01 classification) | Only free-text component/description exists; no typed classification | Cannot deterministically route interfacing guidance | RQ-01, RQ-10 | structured capture field in journey input | Owner decision (schema change is out of Phase A scope) | IDENTIFIED — NOT ACQUIRED |
| MF-02 | Sensor output voltage range (min/max) | Capture / analysis | Needed to indicate voltage-range compatibility (RQ-02, RQ-03) | No numeric voltage field; power_observations is free text with "no assumed values" | Cannot indicate voltage-range mismatch | RQ-02, RQ-03 | structured numeric capture (owner-provided) | Owner decision | IDENTIFIED — NOT ACQUIRED |
| MF-03 | Target MCU input characteristics (logic family, ADC reference, input voltage range) | Capture / analysis | Needed for ADC-reference and digital-level compatibility (RQ-05, RQ-06) | No target-MCU input field | Cannot indicate ADC/logic-level compatibility | RQ-05, RQ-06 | structured target-device capture field | Owner decision | IDENTIFIED — NOT ACQUIRED |
| MF-04 | Signal pulse/frequency characteristics (rate/edge type) | Capture / analysis | Needed for pulse/frequency compatibility (RQ-07) | No typed pulse/frequency field | Cannot address pulse/frequency interfacing | RQ-07 | structured capture field | Owner decision | IDENTIFIED — NOT ACQUIRED |
| MF-05 | Source/load impedance context | Capture / analysis | Needed to indicate impedance/loading relevance (RQ-04) | No impedance field | Cannot indicate loading relevance | RQ-04 | structured capture field | Owner decision | IDENTIFIED — NOT ACQUIRED |
| MF-06 | Governing-parameter availability indicator (datasheet parameters present/absent) | Analysis | Needed for datasheet-sufficiency signalling (RQ-09) and abstention (RQ-11) | No field recording whether governing parameters are available | Cannot signal datasheet sufficiency or a principled abstention | RQ-09, RQ-11 | structured presence flag | Owner decision | IDENTIFIED — NOT ACQUIRED |
| MF-07 | Conditioning-need indicator (diagnostic flag) | Analysis output | Needed for conditioning-need indication (RQ-08) | No structured diagnostic flag; only free-text concerns | Cannot surface a structured conditioning-need signal | RQ-08 | structured diagnostic output field | Owner decision | IDENTIFIED — NOT ACQUIRED |
| MF-08 | Method-routing trigger field (which method a case would require, if authorized) | Analysis | Needed for method-routing trigger (RQ-10) | No field mapping a case to a (future) method route | Cannot record a routing decision distinct from execution | RQ-10 | structured routing field | Owner decision | IDENTIFIED — NOT ACQUIRED |
| MF-09 | Abstention-condition field (explicit "insufficient to advise" state for interfacing) | Analysis output | Needed for abstention condition (RQ-11) | `feasibility_signal=INSUFFICIENT_INPUT` exists but is generic, not interfacing-parameter-specific | Cannot record an interfacing-specific abstention | RQ-11 | structured abstention field | Owner decision | IDENTIFIED — NOT ACQUIRED |
| MF-10 | Non-safety-critical / low-voltage scope confirmation flag | Capture | Needed to confirm a case is inside the D13-TKP-PKG-001 concept class before interfacing guidance | Domain signal exists but no explicit concept-class in-scope flag | Cannot deterministically confirm concept-class membership | RQ-10, RQ-11 | structured scope flag | Owner decision | IDENTIFIED — NOT ACQUIRED |

**Notes.** (a) Every "proposed acquisition method" is an identification of a *possible* future structure only; Phase A neither
creates nor recommends it — schema/UI/application changes are outside Phase A scope. (b) "Blocks a future RQ?" indicates a
dependency of the authorized RQ envelope on the missing structure; it does not answer the RQ. (c) This list is bounded to the
concept class; broader product-wide missing fields (e.g., multi-signal, bus, differential, wireless) are out of the
D13-TKP-PKG-001 concept class and are intentionally excluded (see `unresolved-issues.md`, UI-2).
