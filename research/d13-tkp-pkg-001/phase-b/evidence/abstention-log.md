# D13-TKP-PKG-001 — Phase B Abstention Log

Abstentions are recorded where evidence is insufficient to assert a conclusion, or where asserting one would exceed
Phase B authority. Abstaining is the evidence-supported response (PB-RQ-6 / RQ-11), not a failure.

| # | Abstention | Applies to | Basis | Would require |
|---|---|---|---|---|
| AB-1 | The **exact absolute-maximum input voltage** of a target device | PB-RQ-2 (RQ-02/03) | Device-specific; only the general −0.5V…VCC+0.5V convention is corroborated | The target device datasheet |
| AB-2 | Whether a specific pin is **"5 V-tolerant"** | PB-RQ-2 | Per-pin datasheet exception; not generalizable | The target device datasheet (pin table) |
| AB-3 | The **exact ADC VREF / input range** and any specific analog-fit conclusion | PB-RQ-3 (RQ-05) | Device-specific; only the 0…VREF governance + resolution formula corroborated | The target ADC/MCU datasheet |
| AB-4 | The **exact digital VIH/VIL/VOH/VOL** and any specific logic-level-fit conclusion | PB-RQ-3 (RQ-06) | Device-specific; only family-level thresholds corroborated | Source driver + target input datasheets |
| AB-5 | Whether a specific **frequency/pulse** output fits a specific timer/input | PB-RQ-4 (RQ-07) | Requires both the frequency range and the target timer/logic spec | Both governing-parameter documents |
| AB-6 | The **exact maximum recommended source impedance** for a target ADC and any specific loading conclusion | PB-RQ-5 (RQ-04) | Resolution-/device-dependent (≈10kΩ 8-10bit, ≈2.5kΩ 12-bit are guidance only) | The target ADC datasheet (acquisition spec) |
| AB-7 | **Any numeric compatibility calculation** presented as a product output | PB-RQ-2…5 | No calculation is asserted as a product output in Phase B scope | A separate, later authorized scope |
| AB-8 | **Adoption of a product abstention rule** for RQ-11 | PB-RQ-6 (RQ-11) | Governance decision, explicitly outside Phase B authority | A separate owner/governance decision |
| AB-9 | **Primary-source exact quotations** from vendor PDFs | All RQs | Session egress policy returned HTTP 403 for those hosts | A retrieval channel with access to those hosts |
| AB-10 | The **correct conditioning method** for a specific pairing, and any execution of conditioning | PB-RQ-7 (RQ-08/10) | Requires governing parameters; execution is out of scope | Governing-parameter documents; a separate authorized scope |

## No-candidate / no-appointment (preserved)
No abstention above, and no finding anywhere in this package, names, searches, screens, ranks, selects, recommends,
appoints, or implies any person or company as a provider or candidate. "Specialist category" labels
(electronics-interfacing reviewer; governance/technical reviewer) are **category labels only**.
