# D13-TKP-PKG-001 — Phase B Contradictions & Unresolved Issues

## A. Scope-boundary exclusions (not contradictions — Gate 2 concept-class boundary)
1. **Bus / serial-protocol interfacing (I²C, SPI, 1-Wire, UART, CAN).** Surfaced repeatedly in search (S6, S8, and
   others) but is a **different signal class** than single-signal analog-voltage / single-ended-digital /
   pulse-frequency. **Excluded** from all findings.
2. **Bidirectional MOSFET level shifters (e.g. BSS138 modules).** Surfaced for bidirectional bus lines; **excluded** —
   only one-directional single-signal mitigations (divider/clamp/translator/buffer) are in scope for PB-RQ-2/PB-RQ-3.
3. **Differential, wireless, mains, high-power, and safety-critical interfaces.** Not researched; out of the Gate 2
   concept class by definition.

## B. Resolution-/device-dependent parameters (recorded with uncertainty, not conflicting)
1. **Maximum recommended source impedance** is stated as ≈ 10 kΩ (8/10-bit) and ≈ 2.5 kΩ (12-bit), with device-specific
   values in the datasheet (S5, S13, S18). This is **resolution-dependent guidance**, not a contradiction; the exact
   value is DEVICE-SPECIFIC-ABSTAINED.
2. **Absolute-maximum input rating** appears as "−0.5 V…VCC+0.5 V" and as "≈ VDD+0.3 V" across sources (S2, S8). These
   are the **same convention** at different rounding/margin; the exact per-device value is abstained.
3. **Absolute input range near rails** differs by part (GND+100 mV…VDD−100 mV buffered, S9; AVSS−300 mV…AVDD+300 mV,
   S10). These are **per-part specifications**, correctly different — not a conflict.

## C. Conditional exceptions (must be resolved per-device)
1. **"5 V-tolerant" pins** (S8) are an explicit exception to the overvoltage-damage rule of PB-RQ-2, valid **only** for
   the specific pins the datasheet marks tolerant. Cannot be assumed; requires the target datasheet.

## D. Genuine unresolved issues (open; not resolvable in Phase B)
1. **Device-specific numeric fit** for any given idea (voltage-range fit, ADC-range fit, logic-level fit, frequency
   fit, impedance fit) is **not resolvable without the target governing-parameter documents** — consistent with Phase A
   CG-01…CG-05. Phase B confirms *which* parameters govern; it does not (and in scope must not) compute a specific fit.
2. **Adoption of a product abstention rule** (PB-RQ-6 / RQ-11) is **unresolved by design** — it is a governance
   decision, explicitly outside Phase B authority. Phase B records the evidence supporting abstention as sound practice;
   it does **not** adopt a rule.
3. **Primary-source exact-quotation verification** is unresolved: the session egress policy blocked primary vendor PDF
   fetches. Governing parameters are corroborated across sources but not primary-verified. A future retrieval channel
   with access to those hosts would let the DEMONSTRATED-analogue items be upgraded to primary-verified.

## E. No true contradictions detected
No two authoritative sources were found to assert **mutually incompatible** governing parameters within the concept
class. All apparent differences resolve to (i) scope boundaries, (ii) resolution/device dependence, or (iii)
per-device conditional exceptions, as itemized above.
