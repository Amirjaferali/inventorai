# TECH-SOURCES-001 — Question register

Reconstructed 2026-10-27 against live merged evidence at `7eeb085` (PR #888). Statuses: `QUEUED`, `IN_PROGRESS`,
`QUALIFIED-CANDIDATE`, `BLOCKED`, `ABSTAINED`, `HELD` (not researchable under current authority), `EXCLUDED`.
A question is worked only within its exact claim; findings never decide the owner, host, method admission or activation.

## Tier 1 — existing open engineering questions

| ID | Kind | Exact claim to source | Existing owner / obligation | Must not duplicate | Status | Queries used |
|---|---|---|---|---|---|---|
| Q-01 | Individual (Mechanical) | CAP-13 D-7 METHOD-REGIME QUALIFICATION: from a technically authoritative, lawfully reusable source, whether the governing applicability issue for the bounded stiffness method is small-deflection validity, short / deep-member applicability or another source-defined regime condition, and the exact machine-checkable criterion if one exists. | `docs/governance/STAGE25_CAP13_BOUNDED_STIFFNESS_METHOD_CONTRACT.md` D-7 (OPEN); CLAUDE.md (e)/(h) | Its D-1 / D-5 records (CLOSED); no arbitrary threshold | QUEUED | 0 |
| Q-02 | Integration (motor ↔ mechanism) | Preliminary motion requirements: a qualified class-level statement of the load characteristics that govern whether a motor can drive a mechanism. First uninspected candidate: DOE-HDBK-1011/2-92, Volume 2, DC-motor module. | CLAUDE.md (g1) step 3 and (h) "Preliminary motion requirements: BLOCKED"; the Mechanical vs Electrical / Electronics host decision stays with the Owner | Delivered CAP-13 linear speed-dependent rotational load method (`STAGE25_CAP13_LINEAR_SPEED_DEPENDENT_ROTATIONAL_LOAD_METHOD_CONTRACT.md`) and CAP-13 planar required force; record any overlap instead of re-sourcing it | QUEUED | 0 |
| Q-03 | Integration (controller → output) | Embedded 28-T2 execution-facing output: class-level authoritative, reusable sources only — no owner, method or path selection. | CLAUDE.md (e)/(h) "Embedded 28-T2 output … DEFER pending a specialist owner, source and authorization" | Delivered 28-T2 controller input / logic / output reference (PR #795), control-loop handoff (PR #825), 28-T4 control-cycle evaluation and TEMPERATURE-TO-CONTROL-CONDITION-01; the sensor-to-controller path stays an unauthorized recommendation | QUEUED | 0 |

## Held / excluded (recorded so they are not re-derived)

| ID | Item | Status | Reason |
|---|---|---|---|
| H-01 | X-3 sensor ↔ controller interfacing (D13 TKP-PKG-001 primary-source quotation, AB-1…AB-6, AB-9) | HELD | D13 PAUSED; separate Owner authorization required |
| H-02 | Sensors C3 further source research | HELD | Reopens only with D13 research resumed by the Owner (CLAUDE.md (h)) |
| H-03 | Stage 15 interface characterisation sources | HELD | D4 not activated; reopens only with an authorized interface-characterisation scope |
| E-01 | 28-T3 transistor load-switching principle | EXCLUDED | Delivered (PR #885, 28-T3-LOAD-SWITCHING-PRINCIPLE-REFERENCE-01); no distinct unresolved claim evidenced |
| E-02 | T2-G / R2, MSNL | EXCLUDED | Owner trust / method decision, not source research |
| E-03 | T6 quantity / BOM, calculation-result retention, repeated-units wording | EXCLUDED | Activation / convention decisions, not source research |
| E-04 | Delivered DC resistive load current / power / energy, TMP36 voltage-to-temperature, CAP-13 planar moment / required force / rotational load | EXCLUDED | Delivered |

## Tier 2 — preserved portfolio (preparation only; one at a time, only after Tier 1 is terminal)
Derived one at a time in (g1) step-3 order, each from an existing obligation only (no new owner):
PLC / Automation → Mechatronics / Robotics → Wireless / RF → Battery / BMS → Perception / Edge → IoT → Drone / UAV → Renewables →
Space / Satellite → hydraulics / pneumatics → optics / photonics → materials → acoustics / vibration.
Before working one, add its row here with its exact claim and the existing obligation it comes from; skip any technology with no evidenced open claim.
Source findings for 28-T3 Power Electronics / Motion beyond E-01 enter only if a distinct unresolved claim is evidenced.
