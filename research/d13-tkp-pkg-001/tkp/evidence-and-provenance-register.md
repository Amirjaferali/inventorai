# D13-TKP-PKG-001 — Evidence and Provenance Register

Consolidates the evidence underlying KU-01…KU-07, tracing each item to the accepted Phase B evidence package and its
sources. **Grades are copied verbatim from Phase B and are not upgraded.** Source keys `[Sn]` are the Phase B source
register identities (`research/d13-tkp-pkg-001/phase-b/evidence/source-provenance-register.md`).

## 1. Provenance chain (accepted & merged records only)
```
Phase A read-only analysis (57e2fac8; preserved PR #218, closed PR #219)
    → CG-01..CG-07 (capability-gap-list.md), MF-01..MF-10 (missing-field-list.md)
Phase B research (commit 0c779999; merged PR #222; accepted/closed PR #223)
    → per-rq-findings.md (PB-RQ-1..7), evidence-quality-assessment.md (grades),
      source-provenance-register.md (S1..S18), abstention-log.md (AB-1..AB-10),
      contradictions-and-unresolved-issues.md
TKP construction decision (a4055934; merged PR #224)
    → this package (research/d13-tkp-pkg-001/tkp/)
```
No unrecorded session narrative, memory, or conversation history is used as technical evidence.

## 2. Material access limitation (carried forward, remains visible)
Phase B could **search** authoritative sources but **could not fetch** primary vendor PDFs (Analog Devices, Microchip,
TI, and reference hosts): those hosts returned **HTTP 403** under the authoring environment's organization egress
policy. Consequently **no evidence item is PRIMARY-VERIFIED**; governing parameters are graded on cross-source
corroboration (**REASONED**) or on a surfaced quantified figure (**DEMONSTRATED-analogue**). This limitation **must not
be misrepresented as primary-source verification.**

## 3. Evidence items (traced, graded — verbatim from Phase B)
| KU | Evidence item (governing parameter) | Grade | Validation status | Sources |
|---|---|---|---|---|
| KU-01 | Outputs classify analog vs digital; in-scope single-signal types = analog-voltage / single-ended-digital / pulse-frequency | REASONED | SEARCH-SURFACED · CORROBORATED | S1, S6, S7 |
| KU-02 | Absolute-max input rating ≈ −0.5 V…VCC+0.5 V (≈ VDD+0.3 V); overvoltage → permanent damage | REASONED | SEARCH-SURFACED · CORROBORATED | S2, S8 |
| KU-02 | "5 V-tolerant" pins are a datasheet-stated exception | REASONED | SEARCH-SURFACED | S8 |
| KU-02 | Mitigations: voltage divider (one-directional), clamp, translator | REASONED | SEARCH-SURFACED · CORROBORATED | S2, S8 |
| KU-03 | ADC single-ended convertible range ≈ 0…VREF; resolution = VREF/2ⁿ (e.g. 3.3 V/1024 ≈ 3.22 mV) | DEMONSTRATED-analogue | SEARCH-SURFACED | S1, S2 |
| KU-03 | Absolute input near rails (e.g. GND+100 mV…VDD−100 mV; AVSS−300 mV…AVDD+300 mV) | DEMONSTRATED-analogue | SEARCH-SURFACED | S9, S10 |
| KU-03 | Logic-level governance VIH/VIL/VOH/VOL + noise margin; TTL 2.7 V vs 74HC 3.5 V; 74HCT 2.0 V; CMOS 0.3/0.7·VDD | DEMONSTRATED-analogue | SEARCH-SURFACED · CORROBORATED | S3, S11, S12 |
| KU-04 | Pulse/frequency read via timer input-capture / pulse-accumulator; f ≈ timer_clock/count | REASONED | SEARCH-SURFACED · CORROBORATED | S4, S12 |
| KU-05 | SAR sample-and-hold: higher RSOURCE → longer acquisition; unmet → error | REASONED | SEARCH-SURFACED · CORROBORATED | S5, S13, S14 |
| KU-05 | Max recommended source impedance ≈ 10 kΩ (8/10-bit), ≈ 2.5 kΩ (12-bit); buffer if Zsource > ~10 kΩ | DEMONSTRATED-analogue | SEARCH-SURFACED | S5, S18 |
| KU-06 | Interfacing depends on electrical-characteristics set (type, ranges, VIH/VIL, VREF, Zsource, freq) + timing + reference circuits | REASONED | SEARCH-SURFACED · CORROBORATED | S15, S16 |
| KU-06 | Established practice: insufficient datasheet info → abstain / seek specs | REASONED | SEARCH-SURFACED | S16 |
| KU-07 | Conditioning = level/attenuate/amplify/filter/impedance-match/linearize; need indicated by fit failure | REASONED | SEARCH-SURFACED · CORROBORATED | S17, S18 |
| KU-07 | Need-indication (diagnostic) is distinct from method-routing, which is distinct from execution | REASONED | SEARCH-SURFACED + governance framing | S17 |

## 4. Source identities (Phase B register S1…S18)
The full source table — publisher/authority class, URLs, retrieval basis, and per-host 403 notes — is preserved at
`research/d13-tkp-pkg-001/phase-b/evidence/source-provenance-register.md` (retrieval date 2026-07-22). Authority
classes: vendor-primary (datasheets/app notes: S1, S3, S4, S5, S9, S10, S13, S14, S17), vendor support forums (S2, S10),
independent technical references (S6, S7, S8, S11, S12, S15, S16, S18). This TKP does not restate the URLs to avoid
divergence; the Phase B register is authoritative.

## 5. Provenance guarantees
- No production/journey/personal data used; no paid/restricted/confidential source; no unbounded retrieval.
- Grade distribution (verbatim from Phase B): **0** PRIMARY-VERIFIED; **4** DEMONSTRATED-analogue; **9** REASONED; **11**
  of the items CORROBORATED across ≥2 sources.
- Out-of-scope material encountered in Phase B search (I²C/SPI/1-Wire, bidirectional MOSFET shifters) was excluded — see
  `contradiction-and-unresolved-issue-register.md`.
