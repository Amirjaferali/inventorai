# D13-TKP-PKG-001 — Uncertainty and Abstention Register

Consolidates the explicit uncertainties and abstentions for KU-01…KU-07, carried **verbatim** from the accepted Phase B
abstention log (`research/d13-tkp-pkg-001/phase-b/evidence/abstention-log.md`). **Abstentions remain explicit and are
not resolved by this package.** Abstaining is the evidence-supported response (KU-06 / RQ-11), not a defect.

## 1. Abstentions (AB-1…AB-10, verbatim mapping to knowledge units)
| # | Abstention | Knowledge unit(s) | Basis | Would require |
|---|---|---|---|---|
| AB-1 | Exact **absolute-maximum input voltage** of a target device | KU-02 | Device-specific; only the −0.5 V…VCC+0.5 V convention is corroborated | The target device datasheet |
| AB-2 | Whether a specific pin is **"5 V-tolerant"** | KU-02 | Per-pin datasheet exception; not generalizable | The target device datasheet (pin table) |
| AB-3 | Exact **ADC VREF / input range** and any specific analog-fit conclusion | KU-03 | Device-specific; only 0…VREF governance + resolution formula corroborated | The target ADC/MCU datasheet |
| AB-4 | Exact **digital VIH/VIL/VOH/VOL** and any specific logic-level-fit conclusion | KU-03 | Device-specific; only family-level thresholds corroborated | Source driver + target input datasheets |
| AB-5 | Whether a specific **frequency/pulse** output fits a specific timer/input | KU-04 | Requires both the frequency range and the target timer/logic spec | Both governing-parameter documents |
| AB-6 | Exact **maximum recommended source impedance** for a target ADC and any specific loading conclusion | KU-05 | Resolution-/device-dependent (≈10 kΩ 8–10-bit, ≈2.5 kΩ 12-bit are guidance only) | The target ADC datasheet (acquisition spec) |
| AB-7 | **Any numeric compatibility calculation** presented as a product output | KU-02…KU-05 | No calculation is asserted as a product output in scope | A separate, later authorized scope |
| AB-8 | **Adoption of a product abstention rule** for RQ-11 | KU-06 | Governance decision, outside this authorization | A separate owner/governance decision |
| AB-9 | **Primary-source exact quotations** from vendor PDFs | All KUs | Authoring-environment egress policy returned HTTP 403 for those hosts | A retrieval channel with access to those hosts |
| AB-10 | The **correct conditioning method** for a specific pairing, and any execution of conditioning | KU-07 | Requires governing parameters; execution is out of scope | Governing-parameter documents; a separate authorized scope |

## 2. Standing uncertainty statements
- **Evidence is not primary-verified.** All governing parameters are SEARCH-SURFACED (corroborated), never
  PRIMARY-VERIFIED — a direct consequence of AB-9. Grades cap at REASONED / DEMONSTRATED-analogue.
- **Device-specific numerics are unresolved by design.** Every specific-fit question (voltage, ADC range, logic level,
  frequency, impedance) is DEVICE-SPECIFIC-ABSTAINED and needs the actual target datasheet — none is present in the
  accepted evidence basis, so none is resolved here.
- **The product abstention rule is not adopted** (AB-8); this package records only the evidence that abstention is sound
  practice.

## 3. No-candidate / no-appointment (preserved)
No abstention above — and no unit anywhere in this package — names, searches, screens, ranks, selects, recommends,
appoints, or implies any person or company as a provider or candidate. The two specialist references
(electronics-interfacing reviewer, KU-05; governance/technical reviewer, KU-06) are **category labels only**.
