# D13-TKP-PKG-001 — Validation-Status Matrix

Per-unit validation and acceptance status. **Validation status is descriptive of the evidence as accepted in Phase B; it
does not upgrade any grade.** "Highest grade present" is the strongest grade among a unit's evidence items and is **not**
a claim that the unit as a whole is that strong.

## 1. Knowledge-unit matrix
| KU | Concept-class subproblem | Traces-to | Highest grade present | Primary-verified? | Device-specific numerics | Abstentions | Unit status |
|---|---|---|---|---|---|---|---|
| KU-01 | Sensor-output classification | CG-01, MF-01; PB-RQ-1 | REASONED | No | — (structural, not numeric) | — | RECORDED — CORROBORATED |
| KU-02 | Voltage-range compatibility | CG-02, MF-02/03; PB-RQ-2 | REASONED | No | ABSTAINED | AB-1, AB-2, AB-7 | RECORDED — ABSTAINED ON DEVICE NUMERICS |
| KU-03 | ADC-ref / logic-level compatibility | CG-03, MF-01/03; PB-RQ-3 | DEMONSTRATED-analogue | No | ABSTAINED | AB-3, AB-4 | RECORDED — ABSTAINED ON DEVICE NUMERICS |
| KU-04 | Pulse/frequency compatibility | CG-04, MF-04; PB-RQ-4 | REASONED | No | ABSTAINED | AB-5 | RECORDED — ABSTAINED ON DEVICE NUMERICS |
| KU-05 | Impedance/loading relevance | CG-05, MF-05; PB-RQ-5 | DEMONSTRATED-analogue | No | ABSTAINED | AB-6 | RECORDED — ABSTAINED ON DEVICE NUMERICS |
| KU-06 | Datasheet sufficiency / abstention | CG-06, MF-06/09; PB-RQ-6 | REASONED | No | n/a | AB-8 | RECORDED — RULE NOT ADOPTED (governance) |
| KU-07 | Conditioning-need & method-routing | CG-07, MF-07/08; PB-RQ-7 | REASONED | No | n/a | AB-10 | RECORDED — EXECUTION OUT OF SCOPE |

## 2. Traceability check (every unit → accepted evidence)
| KU | Phase A source (accepted) | Phase B source (accepted) |
|---|---|---|
| KU-01 | capability-gap-list.md CG-01; missing-field-list.md MF-01 | per-rq-findings.md PB-RQ-1; evidence-quality-assessment.md |
| KU-02 | CG-02; MF-02, MF-03 | PB-RQ-2; evidence-quality-assessment.md; abstention-log.md |
| KU-03 | CG-03; MF-01, MF-03 | PB-RQ-3; evidence-quality-assessment.md; abstention-log.md |
| KU-04 | CG-04; MF-04 | PB-RQ-4; abstention-log.md |
| KU-05 | CG-05; MF-05 | PB-RQ-5; evidence-quality-assessment.md; abstention-log.md |
| KU-06 | CG-06; MF-06, MF-09 | PB-RQ-6; abstention-log.md |
| KU-07 | CG-07; MF-07, MF-08 | PB-RQ-7; abstention-log.md |

**Result:** 7/7 knowledge units trace to accepted Phase A **and** Phase B evidence. No unit relies on unrecorded
narrative.

## 3. Package-level validation flags
| Check | Status |
|---|---|
| Every knowledge unit traces to accepted Phase A or Phase B evidence | ✅ 7/7 |
| No evidence grade upgraded vs. Phase B | ✅ (grades copied verbatim; 0 PRIMARY-VERIFIED) |
| Abstentions explicit | ✅ AB-1…AB-10 preserved |
| Device-specific numerics not invented | ✅ all ABSTAINED |
| Primary-source access limitation visible | ✅ recorded in README §5, evidence register §2 |
| Out-of-scope topics excluded | ✅ buses/differential/wireless/mains/high-power/safety-critical excluded |
| No candidate/appointment; specialists are category labels only | ✅ |
| Technology-first order in every unit | ✅ 7/7 |

## 4. Acceptance status
**CONSTRUCTED — PENDING INDEPENDENT (NON-AUTHORING) REVIEW AND SEPARATE OWNER ACCEPTANCE.** Construction completeness is
asserted against the decision's acceptance criteria in `construction-completion-and-acceptance.md`; final acceptance of
the completed TKP remains a separate owner decision.
