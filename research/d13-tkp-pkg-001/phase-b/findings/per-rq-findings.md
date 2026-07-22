# D13-TKP-PKG-001 — Phase B Per-RQ Bounded Research Findings

**Method:** DOCUMENT REVIEW / DATASHEET COMPARISON. **Field order (technology-first, per Phase B decision §3):**
unresolved technical subproblem · missing technical information · required technology/research topic · suggested
technical search terms · required measurements/documents/tests · what InventorAI can verify · what InventorAI cannot
verify · risk/uncertainty · specialist category (category label only, when genuinely necessary).

Each finding records *what the authoritative technical literature establishes about the governing parameters* for the
subproblem. **No engineering conclusion is asserted for any specific device or idea**; device-specific numeric fits are
abstained (see `evidence/abstention-log.md`). Source keys `[Sn]` resolve in `evidence/source-provenance-register.md`;
grades resolve in `evidence/evidence-quality-assessment.md`.

---

## PB-RQ-1 — Sensor-output classification (→ RQ-01; from CG-01)

- **Unresolved technical subproblem:** Deterministically classify a sensor's output as analog-voltage /
  single-ended-digital / pulse-frequency.
- **Missing technical information:** A typed output-classification field (or the datasheet's output-signal
  specification). Free-text descriptions do not structurally encode the signal type.
- **Required technology/research topic:** Sensor output-signal typing.
- **Suggested technical search terms:** "sensor output signal type", "analog vs digital sensor interface".
- **Required measurements/documents/tests:** The sensor's governing-parameter documentation (datasheet "output"
  section) stating output form and range.
- **Evidence established (governing parameters):** Authoritative interfacing literature classifies sensor outputs as
  either **analog** (a continuously variable voltage proportional to the measurand) or **digital** (discrete levels or
  a serial protocol). Within the Gate 2 concept class the single-signal types are: **analog-voltage**,
  **single-ended-digital** (a logic-level line), and **pulse-frequency** (a variable-frequency/pulse-rate line).
  Serial-protocol digital outputs (I²C/SPI/1-Wire/UART) are a *different* class and are **out of scope** here. `[S1][S6][S7]`
- **What InventorAI can verify:** The presence/absence of a free-text output description in the idea record.
- **What InventorAI cannot verify:** The true signal type *structurally* from free text alone — classification requires
  the typed field or the datasheet output specification. **Confirms CG-01.**
- **Risk/uncertainty:** Low–moderate. Corroborated across multiple authoritative sources; the boundary between
  single-ended-digital and pulse-frequency can itself require the datasheet.
- **Specialist category:** Not necessary.

---

## PB-RQ-2 — Voltage-range compatibility (→ RQ-02/03; from CG-02)

- **Unresolved technical subproblem:** Indicate whether the sensor output voltage range is compatible with the target
  input voltage range (mismatch indication).
- **Missing technical information:** The sensor output voltage range **and** the target input voltage range (both
  governing values).
- **Required technology/research topic:** Voltage-range compatibility and absolute-maximum input ratings.
- **Suggested technical search terms:** "sensor output voltage range", "MCU input voltage range", "absolute maximum
  input rating".
- **Required measurements/documents/tests:** Governing-parameter documents (both source and target) with output range,
  input operating range, and absolute-maximum input rating.
- **Evidence established (governing parameters):** The convertible/acceptable input range is bounded by the device's
  operating input range, and the **absolute-maximum input rating** is commonly of the form **−0.5 V to VCC+0.5 V**
  (equivalently ≈ VDD+0.3 V on many parts). Exceeding it "may immediately and permanently" damage the input. Applying a
  higher-voltage output (e.g. 5 V to a 3.3 V-rated input) can cause permanent damage **unless** the specific pin is
  datasheet-stated **"5 V tolerant."** Mismatch mitigations named in the literature: resistive **voltage divider**
  (one-directional signals only), clamping, or a dedicated translator. `[S2][S8][S9]`
- **What InventorAI can verify:** The presence/absence of free-text power/voltage notes in the idea record.
- **What InventorAI cannot verify:** The *numeric* mismatch relationship — no calculation is asserted as a product
  output in scope, and both governing ranges are required and typically absent. **Confirms CG-02.**
- **Risk/uncertainty:** Moderate. The −0.5 V…VCC+0.5 V convention is widely corroborated but the **exact** per-device
  value and any "5 V-tolerant" exception are device-specific → **abstained**.
- **Specialist category:** Not necessary.

---

## PB-RQ-3 — ADC-reference / single-ended digital logic-level compatibility (→ RQ-05/06; from CG-03)

- **Unresolved technical subproblem:** (a) Whether an analog output fits the target ADC input range; (b) whether a
  single-ended-digital output meets the target digital-input logic levels.
- **Missing technical information:** Target-device input attributes — ADC reference/input range; digital VIH/VIL (and
  driver VOH/VOL on the source side).
- **Required technology/research topic:** ADC reference & input range; single-ended logic-level compatibility.
- **Suggested technical search terms:** "ADC reference input range", "logic level compatibility", "VIH VIL VOH VOL".
- **Required measurements/documents/tests:** Device governing parameters — ADC VREF and input-range spec; digital-input
  threshold spec (VIH/VIL) and source driver output levels (VOH/VOL).
- **Evidence established (governing parameters):**
  - *ADC:* The convertible range for a single-ended input is bounded by the reference (≈ 0 … VREF); resolution =
    VREF / 2ⁿ (n = bit width; e.g. 3.3 V / 1024 ≈ 3.22 mV for 10-bit). The absolute input range is separately bounded
    near the supply rails (illustrative authoritative datasheet limits: buffered inputs "GND+100 mV … VDD−100 mV" on
    one part; "AVSS−300 mV … AVDD+300 mV" absolute on another). Reference voltage and input range are distinct from
    absolute-maximum ratings. `[S2][S10]`
  - *Digital logic level:* Compatibility is governed by **VIH** (min voltage read as HIGH), **VIL** (max voltage read
    as LOW), driver **VOH/VOL**, and the resulting **noise margin**. A named incompatibility: a TTL driver's VOH(min)
    ≈ 2.7 V may fail a 74HC input's VIH(min) ≈ 3.5 V; the standard fix is a TTL-threshold input (74HCT, VIH ≈ 2.0 V).
    Classic CMOS thresholds are ≈ 0.3·VDD (VIL) and 0.7·VDD (VIH). `[S3][S11][S12]`
- **What InventorAI can verify:** The presence/absence of relevant descriptors in the idea record.
- **What InventorAI cannot verify:** The *fit* without the target input attributes (VREF/input-range; VIH/VIL). These
  are typically absent. **Confirms CG-03.**
- **Risk/uncertainty:** Moderate. Governing parameters are well-corroborated; specific device values are
  device-specific → **abstained**.
- **Specialist category:** Not necessary.

---

## PB-RQ-4 — Pulse/frequency compatibility (→ RQ-07; from CG-04)

- **Unresolved technical subproblem:** Whether a pulse/frequency output can be interfaced to the target and read.
- **Missing technical information:** A pulse/frequency descriptor (frequency range, pulse form/level) and the target's
  timer/counter input capability.
- **Required technology/research topic:** Frequency-output interfacing (timer input-capture / pulse counting).
- **Suggested technical search terms:** "frequency output sensor interfacing", "pulse counting input", "timer input
  capture".
- **Required measurements/documents/tests:** Governing-parameter documents — sensor frequency/pulse range and level;
  target timer input-capture / pulse-accumulator spec and input logic thresholds.
- **Evidence established (governing parameters):** Frequency/pulse outputs are read with a **hardware timer
  input-capture** channel or a **pulse-accumulator/counter**; the reading is governed by the timer clock, prescaler,
  edge selection, and capture register (frequency ≈ timer_clock / captured_count, adjusted for prescaler). Crucially,
  the pulse line must **first meet the target digital-input logic thresholds** (same VIH/VIL governance as PB-RQ-3)
  before frequency can be counted. `[S4][S12]`
- **What InventorAI can verify:** The presence/absence of a pulse/frequency descriptor in the idea record.
- **What InventorAI cannot verify:** Whether the frequency range and logic level fit the target timer/input, without
  the governing parameters. **Confirms CG-04.**
- **Risk/uncertainty:** Moderate.
- **Specialist category:** Not necessary.

---

## PB-RQ-5 — Impedance/loading relevance (→ RQ-04; from CG-05)

- **Unresolved technical subproblem:** When source/load impedance is a relevant interfacing concern.
- **Missing technical information:** The sensor output (source) impedance and the target input (load) characteristics.
- **Required technology/research topic:** Source/load impedance in low-voltage interfacing; ADC sample-and-hold loading.
- **Suggested technical search terms:** "sensor output impedance loading", "ADC maximum recommended source impedance",
  "input impedance loading effect".
- **Required measurements/documents/tests:** Governing-parameter documents — sensor output impedance; target ADC
  acquisition-time / max-recommended-source-impedance spec.
- **Evidence established (governing parameters):** For SAR ADCs the input is a switched-capacitor sample-and-hold; the
  **source impedance (RSOURCE)** must charge the hold capacitor within the acquisition window, so **higher source
  impedance increases required acquisition time** and, if unmet, produces a settling/charge error. Authoritative
  guidance gives **maximum recommended source impedance ≈ 10 kΩ for 8/10-bit** ADCs and **≈ 2.5 kΩ for 12-bit**, with
  the device-specific value in the datasheet. The named mitigation is an **op-amp buffer**, recommended especially when
  the sensor source impedance exceeds ~10 kΩ. Impedance/loading is therefore a **genuine judgment** that matters
  precisely when a high-impedance source meets a switched-cap/low-impedance load. `[S5][S13][S14]`
- **What InventorAI can verify:** The presence/absence of impedance context in the idea record.
- **What InventorAI cannot verify:** Whether loading is a problem for a specific pairing, without the governing values.
  **Confirms CG-05.**
- **Risk/uncertainty:** Moderate. The qualitative governing relationship is strongly corroborated; the specific
  max-source-impedance value is resolution- and device-dependent → **abstained** on the exact device figure.
- **Specialist category:** **Electronics-interfacing reviewer** — *category label only*, invoked **only** when a genuine
  impedance/loading judgment is required. No person or company is named or implied.

---

## PB-RQ-6 — Datasheet sufficiency / abstention (→ RQ-09/11; from CG-06)

- **Unresolved technical subproblem:** Whether the available governing parameters are sufficient to advise, and when to
  **abstain**.
- **Missing technical information:** A parameter-availability indicator, plus a governance-reviewed abstention rule.
- **Required technology/research topic:** Datasheet/governing-parameter sufficiency; abstention criteria.
- **Suggested technical search terms:** "datasheet key parameters interface", "electrical characteristics table",
  "abstention criteria technical advice".
- **Required measurements/documents/tests:** Governing-parameter documents; **and** a governance-reviewed abstention
  rule (governance decision, not adopted in Phase B).
- **Evidence established (governing parameters):** The literature identifies the **electrical-characteristics** set an
  interfacing decision depends on: output signal type; output voltage/level range; for digital, VIH/VIL/VOH/VOL; for
  analog into an ADC, the target VREF/input range; source impedance; and, for pulse, the frequency range — plus timing
  diagrams and manufacturer reference circuits. On sufficiency, established engineering practice is explicit: **when the
  datasheet information is inadequate, abstain from the design decision** and instead obtain complete specifications /
  consult application notes / seek a better-documented alternative — rather than assert a conclusion. `[S15][S16]`
- **What InventorAI can verify:** Whether the named governing parameters are present or absent in the idea record.
- **What InventorAI cannot verify:** Correctness of any advice when the governing parameters are absent — the
  evidence-supported response is to **abstain**. **Confirms CG-06 and supports RQ-11 (abstention).**
- **Risk/uncertainty:** Moderate–high (abstention correctness). The abstention *practice* is corroborated; **adopting a
  specific abstention rule for the product is a governance decision and is NOT made here** (out of Phase B scope).
- **Specialist category:** **Governance/technical reviewer** — *category label only*, to validate any abstention rule
  before adoption. No person or company named.

---

## PB-RQ-7 — Conditioning-need & method-routing indication (→ RQ-08/10; from CG-07)

- **Unresolved technical subproblem:** (a) Signal a signal-conditioning **need** diagnostically; (b) record a
  **method-routing** decision as distinct from executing it.
- **Missing technical information:** A diagnostic conditioning-need field and a routing-decision field.
- **Required technology/research topic:** Signal-conditioning need indication; decision routing.
- **Suggested technical search terms:** "signal conditioning need", "analog front end", "decision routing rules".
- **Required measurements/documents/tests:** Governing-parameter documents sufficient to detect a mismatch that implies
  a conditioning need.
- **Evidence established (governing parameters):** Authoritative signal-conditioning references define conditioning as
  the operations that prepare a sensor signal for the target input — **level change, attenuation, amplification,
  filtering, impedance matching, linearization.** A conditioning **need is indicated** when the raw output does not
  directly fit the target input window, e.g.: output range outside the ADC range → attenuation/amplification/level-shift;
  high source impedance → buffer (PB-RQ-5); logic-level mismatch → level shift (PB-RQ-3); signal-type mismatch →
  conversion (PB-RQ-1). Detecting that a need **exists** is a **diagnostic indication**; **choosing** which method to
  apply is a **routing decision** that is distinct from **executing** that method. This separation maps RQ-08 (indicate
  need) and RQ-10 (record routing, distinct from execution). `[S17][S18]`
- **What InventorAI can verify:** Whether a mismatch pattern is present/absent given available governing parameters, and
  can *record* a routing decision separately from execution.
- **What InventorAI cannot verify:** The correct conditioning method for a specific pairing without the governing
  parameters; and it must not *execute* conditioning (out of scope). **Confirms CG-07.**
- **Risk/uncertainty:** Moderate.
- **Specialist category:** Not necessary (the impedance sub-case defers to PB-RQ-5's category label only when a genuine
  judgment is required).
