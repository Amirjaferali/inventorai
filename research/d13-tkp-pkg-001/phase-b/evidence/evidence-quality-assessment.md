# D13-TKP-PKG-001 — Phase B Evidence-Quality Assessment

**Grades (per Phase B decision §5):**
- **ASSERTED** — stated by a source without corroboration or demonstration surfaced.
- **REASONED** — a governing relationship corroborated across multiple authoritative sources and consistent with
  established engineering practice, but **not** verified here against a primary-source exact quotation.
- **DEMONSTRATED-analogue** — supported by a concrete, quantified example in an authoritative primary source
  (as surfaced), standing in for direct demonstration.

**Validation-status markers:** `PRIMARY-VERIFIED` (primary PDF opened and quote confirmed) · `SEARCH-SURFACED`
(attributed to a named authoritative source via search; primary fetch blocked by egress policy) · `CORROBORATED`
(≥2 independent sources agree) · `DEVICE-SPECIFIC-ABSTAINED` (governing category recorded; exact value abstained).

**Global validation note:** No item is `PRIMARY-VERIFIED` — primary vendor PDFs returned HTTP 403 under the session
egress policy (see provenance register). Grades therefore cap at **REASONED** (or **DEMONSTRATED-analogue** where an
authoritative source surfaced a concrete quantified figure), never full primary-verified DEMONSTRATED.

| RQ | Evidence item (governing parameter) | Grade | Validation status | Uncertainty / abstention note |
|---|---|---|---|---|
| PB-RQ-1 | Sensor outputs classify as analog vs digital; in-scope single-signal types = analog-voltage / single-ended-digital / pulse-frequency | REASONED | SEARCH-SURFACED · CORROBORATED (S1,S6,S7) | Type boundary can require the datasheet; free text is insufficient. |
| PB-RQ-2 | Absolute-max input rating ≈ −0.5 V…VCC+0.5 V (≈ VDD+0.3 V); overvoltage → permanent damage | REASONED | SEARCH-SURFACED · CORROBORATED (S2,S8) | Exact per-device value DEVICE-SPECIFIC-ABSTAINED. |
| PB-RQ-2 | "5 V-tolerant" pins are a datasheet-stated exception | REASONED | SEARCH-SURFACED (S8) | Per-pin; requires the specific datasheet → abstained. |
| PB-RQ-2 | Mitigations: voltage divider (one-directional), clamp, translator | REASONED | SEARCH-SURFACED · CORROBORATED (S2,S8) | Divider unsuitable for bidirectional/bus lines (out of scope). |
| PB-RQ-3 | ADC single-ended convertible range ≈ 0…VREF; resolution = VREF/2ⁿ (e.g. 3.3V/1024 ≈ 3.22 mV) | DEMONSTRATED-analogue | SEARCH-SURFACED (S1,S2) | Quantified example surfaced; exact VREF DEVICE-SPECIFIC-ABSTAINED. |
| PB-RQ-3 | Absolute input near rails (e.g. GND+100mV…VDD−100mV; AVSS−300mV…AVDD+300mV) | DEMONSTRATED-analogue | SEARCH-SURFACED (S9,S10) | Part-specific figures; not the target device → abstained for any specific idea. |
| PB-RQ-3 | Logic-level governance VIH/VIL/VOH/VOL + noise margin; TTL VOH 2.7V vs 74HC VIH 3.5V; 74HCT VIH 2.0V; CMOS 0.3/0.7·VDD | DEMONSTRATED-analogue | SEARCH-SURFACED · CORROBORATED (S3,S11,S12) | Family-level quantified; exact device VIH/VIL DEVICE-SPECIFIC-ABSTAINED. |
| PB-RQ-4 | Pulse/frequency read via timer input-capture / pulse-accumulator; f ≈ timer_clock/count | REASONED | SEARCH-SURFACED · CORROBORATED (S4,S12) | Requires input logic-level compliance first (links PB-RQ-3). |
| PB-RQ-5 | SAR sample-and-hold: higher RSOURCE → longer acquisition; unmet → error | REASONED | SEARCH-SURFACED · CORROBORATED (S5,S13,S14) | Qualitative relationship robust. |
| PB-RQ-5 | Max recommended source impedance ≈ 10 kΩ (8/10-bit), ≈ 2.5 kΩ (12-bit); buffer if Zsource > ~10 kΩ | DEMONSTRATED-analogue | SEARCH-SURFACED (S5,S18) | Resolution-/device-dependent; exact device value DEVICE-SPECIFIC-ABSTAINED. |
| PB-RQ-6 | Interfacing depends on electrical-characteristics set (type, ranges, VIH/VIL, VREF, Zsource, freq) + timing + reference circuits | REASONED | SEARCH-SURFACED · CORROBORATED (S15,S16) | Enumerates required governing parameters. |
| PB-RQ-6 | Established practice: insufficient datasheet info → abstain / seek specs | REASONED | SEARCH-SURFACED (S16) | Practice corroborated; **product abstention rule NOT adopted** (governance decision). |
| PB-RQ-7 | Conditioning = level/attenuate/amplify/filter/impedance-match/linearize; need indicated by fit failure | REASONED | SEARCH-SURFACED · CORROBORATED (S17,S18) | — |
| PB-RQ-7 | Need-indication (diagnostic) is distinct from method-routing, which is distinct from execution | REASONED | SEARCH-SURFACED (S17) + governance framing | Execution out of scope; separation is the recorded finding. |

## Summary
- 0 items `PRIMARY-VERIFIED`; **13** governing-parameter items recorded, all `SEARCH-SURFACED`, **11 CORROBORATED**
  across ≥2 sources.
- **4** items graded **DEMONSTRATED-analogue** (a quantified figure surfaced from an authoritative source); the rest
  **REASONED**. No item claims full primary-verified DEMONSTRATED.
- **6** governing categories carry **DEVICE-SPECIFIC-ABSTAINED** on their exact numeric value — see
  `evidence/abstention-log.md`.
