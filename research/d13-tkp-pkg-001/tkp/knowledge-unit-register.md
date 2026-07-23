# D13-TKP-PKG-001 — Canonical Knowledge-Unit Register

Seven canonical knowledge units (KU-01…KU-07) for the approved single-signal sensor→microcontroller concept class. Each
unit is stated in the **technology-first order** and carries a `Traces-to:` citation into accepted Phase A / Phase B
evidence. **No evidence grade is upgraded; no device-specific numeric conclusion is invented; abstentions are explicit.**
Grades and source keys `[Sn]` resolve in `evidence-and-provenance-register.md`; abstentions `AB-n` in
`uncertainty-and-abstention-register.md`.

**Technology-first order (fixed):** technology & unresolved problem → missing information → verification method &
required evidence → what InventorAI can verify → what InventorAI cannot verify → uncertainty & risk → specialist
category only when genuinely necessary.

---

## KU-01 — Sensor-output classification
- **Traces-to:** Phase A CG-01, MF-01; Phase B PB-RQ-1 (→ RQ-01).
- **Technology & unresolved problem:** deterministically classify a sensor output as **analog-voltage /
  single-ended-digital / pulse-frequency**. Free text does not structurally encode the signal type.
- **Missing information:** a typed sensor-output classification field (MF-01), and the classification rule that consumes it.
- **Verification method & required evidence:** DOCUMENT REVIEW of the sensor's governing-parameter documentation
  (datasheet "output" section). Evidence established: outputs classify as analog vs digital; in-scope single-signal
  types are analog-voltage, single-ended-digital, pulse-frequency; serial-protocol outputs are a different (excluded)
  class. Grade **REASONED** (SEARCH-SURFACED, CORROBORATED) `[S1][S6][S7]`.
- **What InventorAI can verify:** presence/absence of a free-text output description in the idea record.
- **What InventorAI cannot verify:** the true signal type *structurally* from free text alone (needs the typed field or
  datasheet).
- **Uncertainty & risk:** low–moderate; the single-ended-digital vs pulse-frequency boundary can itself require the
  datasheet.
- **Specialist category:** not necessary.

## KU-02 — Voltage-range compatibility
- **Traces-to:** Phase A CG-02, MF-02, MF-03; Phase B PB-RQ-2 (→ RQ-02/03).
- **Technology & unresolved problem:** indicate whether the sensor output voltage range is compatible with the target
  input range (mismatch indication).
- **Missing information:** structured sensor output voltage range (MF-02) and target MCU input range (MF-03).
- **Verification method & required evidence:** DOCUMENT REVIEW of both governing-parameter documents. Evidence
  established: acceptable input is bounded by the operating input range; the **absolute-maximum input rating** is
  commonly of the form **−0.5 V…VCC+0.5 V** (≈ VDD+0.3 V); overvoltage can permanently damage the input unless the pin
  is datasheet-stated **"5 V tolerant."** Mitigations: voltage divider (one-directional only), clamp, translator.
  Grade **REASONED** (SEARCH-SURFACED, CORROBORATED) `[S2][S8][S9]`.
- **What InventorAI can verify:** presence/absence of free-text power/voltage notes.
- **What InventorAI cannot verify:** the numeric mismatch relationship — no calculation is a product output in scope, and
  both governing ranges are required and typically absent.
- **Uncertainty & risk:** moderate. Exact per-device absolute-max value and any "5 V-tolerant" exception are
  **DEVICE-SPECIFIC-ABSTAINED** (AB-1, AB-2, AB-7).
- **Specialist category:** not necessary.

## KU-03 — ADC-reference / single-ended digital logic-level compatibility
- **Traces-to:** Phase A CG-03, MF-01, MF-03; Phase B PB-RQ-3 (→ RQ-05/06).
- **Technology & unresolved problem:** (a) whether an analog output fits the target ADC input range; (b) whether a
  single-ended-digital output meets the target digital-input logic levels.
- **Missing information:** target-device input attributes — ADC reference/input range; digital VIH/VIL (and source
  VOH/VOL).
- **Verification method & required evidence:** DOCUMENT REVIEW of device governing parameters. Evidence established:
  *ADC* — single-ended convertible range ≈ 0…VREF; resolution = VREF/2ⁿ (e.g. 3.3 V/1024 ≈ 3.22 mV for 10-bit);
  absolute input separately bounded near supply rails (illustrative part limits "GND+100 mV…VDD−100 mV";
  "AVSS−300 mV…AVDD+300 mV"). *Digital* — governed by VIH/VIL/VOH/VOL and noise margin; named incompatibility TTL
  VOH(min) ≈ 2.7 V vs 74HC VIH(min) ≈ 3.5 V, fixed by 74HCT (VIH ≈ 2.0 V); CMOS ≈ 0.3·VDD / 0.7·VDD. Grade
  **DEMONSTRATED-analogue** for the quantified items (SEARCH-SURFACED) `[S1][S2][S3][S9][S10][S11][S12]`.
- **What InventorAI can verify:** presence/absence of relevant descriptors in the idea record.
- **What InventorAI cannot verify:** the fit without the target input attributes (VREF/input-range; VIH/VIL).
- **Uncertainty & risk:** moderate. All specific device values are **DEVICE-SPECIFIC-ABSTAINED** (AB-3, AB-4).
- **Specialist category:** not necessary.

## KU-04 — Pulse/frequency compatibility
- **Traces-to:** Phase A CG-04, MF-04; Phase B PB-RQ-4 (→ RQ-07).
- **Technology & unresolved problem:** whether a pulse/frequency output can be interfaced to the target and read.
- **Missing information:** a pulse/frequency descriptor (MF-04) and the target's timer/counter input capability.
- **Verification method & required evidence:** DOCUMENT REVIEW of governing-parameter documents. Evidence established:
  frequency/pulse outputs are read via a hardware timer **input-capture** channel or a **pulse-accumulator/counter**
  (frequency ≈ timer_clock / captured_count, prescaler-adjusted); the pulse line must **first meet the target
  digital-input logic thresholds** (links KU-03). Grade **REASONED** (SEARCH-SURFACED, CORROBORATED) `[S4][S12]`.
- **What InventorAI can verify:** presence/absence of a pulse/frequency descriptor.
- **What InventorAI cannot verify:** whether the frequency range and logic level fit the target timer/input, without the
  governing parameters.
- **Uncertainty & risk:** moderate. Specific fit is **DEVICE-SPECIFIC-ABSTAINED** (AB-5).
- **Specialist category:** not necessary.

## KU-05 — Impedance/loading relevance
- **Traces-to:** Phase A CG-05, MF-05; Phase B PB-RQ-5 (→ RQ-04).
- **Technology & unresolved problem:** when source/load impedance is a relevant interfacing concern.
- **Missing information:** sensor output (source) impedance and target input (load) characteristics (MF-05).
- **Verification method & required evidence:** DOCUMENT REVIEW of governing-parameter documents. Evidence established:
  for SAR ADCs the input is a switched-capacitor sample-and-hold, so higher **source impedance** increases required
  acquisition time and, if unmet, causes a settling/charge error; guidance gives max recommended source impedance
  ≈ 10 kΩ (8/10-bit), ≈ 2.5 kΩ (12-bit), with the device value in the datasheet; mitigation is an op-amp buffer,
  especially when source impedance > ~10 kΩ. Grade **DEMONSTRATED-analogue** for the quantified guidance; **REASONED**
  for the qualitative relationship (SEARCH-SURFACED) `[S5][S13][S14][S18]`.
- **What InventorAI can verify:** presence/absence of impedance context.
- **What InventorAI cannot verify:** whether loading is a problem for a specific pairing, without the governing values.
- **Uncertainty & risk:** moderate. The exact device max-source-impedance is **DEVICE-SPECIFIC-ABSTAINED** (AB-6).
- **Specialist category:** **electronics-interfacing reviewer** — *category label only*, invoked only when a genuine
  impedance/loading judgment is required. No person or company named or implied.

## KU-06 — Datasheet sufficiency / abstention
- **Traces-to:** Phase A CG-06, MF-06, MF-09; Phase B PB-RQ-6 (→ RQ-09/11).
- **Technology & unresolved problem:** whether the available governing parameters are sufficient to advise, and when to
  **abstain**.
- **Missing information:** a governing-parameter availability indicator (MF-06) and an interfacing-specific abstention
  field (MF-09), plus a governance-reviewed abstention rule.
- **Verification method & required evidence:** DOCUMENT REVIEW of governing-parameter documents; **and** a
  governance-reviewed abstention rule (governance decision). Evidence established: the interfacing decision depends on a
  named electrical-characteristics set (output type; output voltage/level range; digital VIH/VIL/VOH/VOL; ADC
  VREF/input range; source impedance; pulse frequency range) plus timing and reference circuits; established practice is
  that **when datasheet information is inadequate, abstain** rather than assert a conclusion. Grade **REASONED**
  (SEARCH-SURFACED) `[S15][S16]`.
- **What InventorAI can verify:** whether the named governing parameters are present or absent in the idea record.
- **What InventorAI cannot verify:** correctness of any advice when the governing parameters are absent — the
  evidence-supported response is to **abstain**.
- **Uncertainty & risk:** moderate–high (abstention correctness). The abstention *practice* is corroborated; **adopting a
  product abstention rule is a governance decision and is NOT made here** (AB-8).
- **Specialist category:** **governance/technical reviewer** — *category label only*, to validate any abstention rule
  before adoption. No person or company named.

## KU-07 — Conditioning-need & method-routing indication
- **Traces-to:** Phase A CG-07, MF-07, MF-08; Phase B PB-RQ-7 (→ RQ-08/10).
- **Technology & unresolved problem:** (a) signal a signal-conditioning **need** diagnostically; (b) record a
  **method-routing** decision distinct from executing it.
- **Missing information:** a diagnostic conditioning-need field (MF-07) and a method-routing field (MF-08).
- **Verification method & required evidence:** DOCUMENT REVIEW of governing-parameter documents sufficient to detect a
  mismatch that implies a conditioning need. Evidence established: conditioning = level change / attenuation /
  amplification / filtering / impedance matching / linearization; a need is indicated when the raw output does not fit
  the target input window (range outside ADC → attenuate/amplify/level-shift; high source impedance → buffer, per KU-05;
  logic-level mismatch → level shift, per KU-03; signal-type mismatch → conversion, per KU-01). Detecting that a need
  **exists** is a **diagnostic indication**; **choosing** the method is a **routing decision** distinct from
  **executing** it (RQ-08 vs RQ-10). Grade **REASONED** (SEARCH-SURFACED, CORROBORATED) `[S17][S18]`.
- **What InventorAI can verify:** whether a mismatch pattern is present/absent given available governing parameters; and
  can *record* a routing decision separately from execution.
- **What InventorAI cannot verify:** the correct conditioning method for a specific pairing without the governing
  parameters; and it must not *execute* conditioning (out of scope).
- **Uncertainty & risk:** moderate. Method choice + execution are **abstained/out-of-scope** (AB-10).
- **Specialist category:** not necessary (the impedance sub-case defers to KU-05's category label only when a genuine
  judgment is required).

---

**Cross-unit note.** KU-01…KU-07 map one-to-one to Phase A capability gaps CG-01…CG-07 and Phase B research questions
PB-RQ-1…PB-RQ-7. Out-of-scope classes (buses, differential, wireless, mains, high-power, safety-critical) are **not**
knowledge units and are excluded — see `contradiction-and-unresolved-issue-register.md`.
