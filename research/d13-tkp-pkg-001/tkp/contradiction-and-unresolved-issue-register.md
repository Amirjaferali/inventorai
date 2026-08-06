# D13-TKP-PKG-001 — Contradiction and Unresolved-Issue Register

Carries forward, **verbatim**, the Phase B contradictions/unresolved issues
(`research/d13-tkp-pkg-001/phase-b/evidence/contradictions-and-unresolved-issues.md`) and binds them to the knowledge
units. **Nothing here is resolved by construction; contradictions and unresolved issues remain visible.**

## A. Scope-boundary exclusions (not contradictions — Gate 2 boundary; must remain excluded)
1. **Bus / serial-protocol interfacing (I²C, SPI, 1-Wire, UART, CAN)** — a different signal class than single-signal
   analog-voltage / single-ended-digital / pulse-frequency. Excluded from all knowledge units.
2. **Bidirectional MOSFET level shifters (e.g. BSS138 modules)** — for bidirectional bus lines; excluded. Only
   one-directional single-signal mitigations (divider / clamp / translator / buffer) are in scope for KU-02 / KU-03.
3. **Differential, wireless, mains, high-power, and safety-critical interfaces** — outside the Gate 2 concept class by
   definition; not researched, not represented.

## B. Resolution-/device-dependent parameters (recorded with uncertainty, not conflicting)
1. **Maximum recommended source impedance** — ≈ 10 kΩ (8/10-bit) and ≈ 2.5 kΩ (12-bit); device-specific value in the
   datasheet (KU-05). Resolution-dependent guidance, not a contradiction; exact value DEVICE-SPECIFIC-ABSTAINED (AB-6).
2. **Absolute-maximum input rating** — "−0.5 V…VCC+0.5 V" and "≈ VDD+0.3 V" are the same convention at different
   rounding/margin (KU-02); exact per-device value abstained (AB-1).
3. **Absolute input range near rails** — differs by part (GND+100 mV…VDD−100 mV buffered; AVSS−300 mV…AVDD+300 mV);
   per-part specifications, correctly different, not a conflict (KU-03).

## C. Conditional exceptions (must be resolved per-device)
1. **"5 V-tolerant" pins** are an explicit exception to the overvoltage-damage rule of KU-02, valid only for the pins the
   datasheet marks tolerant. Cannot be assumed; requires the target datasheet (AB-2).

## D. Genuine unresolved issues (open; not resolvable by this package)
1. **Device-specific numeric fit** for any given idea (voltage, ADC range, logic level, frequency, impedance) is not
   resolvable without the target governing-parameter documents — consistent with Phase A CG-01…CG-05. The TKP records
   *which* parameters govern; it does not compute a specific fit.
2. **Adoption of a product abstention rule** (KU-06 / RQ-11) is unresolved by design — a governance decision outside this
   authorization (AB-8).
3. **Primary-source exact-quotation verification** is unresolved: the authoring-environment egress policy blocked primary
   vendor PDF fetches (AB-9). A future retrieval channel with access to those hosts could upgrade DEMONSTRATED-analogue
   items toward primary-verified.

## E. No true contradictions detected
No two authoritative sources were found to assert mutually incompatible governing parameters within the concept class.
All apparent differences resolve to (i) scope boundaries, (ii) resolution/device dependence, or (iii) per-device
conditional exceptions, as itemized above. This finding is carried verbatim from Phase B and is **not** an upgrade.
