# TECH-SOURCES-001 — Question register

Reconstructed 2026-10-27 against live merged evidence at `7eeb085` (PR #888). Statuses: `QUEUED`, `IN_PROGRESS`, `QUESTION UNCLEAR`, `EVIDENCE INSUFFICIENT`, `SOURCE CANDIDATE`, `SOURCE ACCESS BLOCKED`, `IP UNRESOLVED`, `METHOD UNQUALIFIED`, `AUTHORITY BLOCKED`,
`QUALIFIED-CANDIDATE`, `BLOCKED`, `ABSTAINED`, `HELD` (not researchable under current authority), `EXCLUDED`.
A question is worked only within its exact claim; findings never decide the owner, host, method admission or activation.

## Tier 1 — existing open engineering questions

| ID | Kind | Exact claim to source | Existing owner / obligation | Must not duplicate | Status | Queries used |
|---|---|---|---|---|---|---|
| Q-01 | Individual (Mechanical) | CAP-13 D-7 METHOD-REGIME QUALIFICATION: from a technically authoritative, lawfully reusable source, whether the governing applicability issue for the bounded stiffness method is small-deflection validity, short / deep-member applicability or another source-defined regime condition, and the exact machine-checkable criterion if one exists. | `docs/governance/STAGE25_CAP13_BOUNDED_STIFFNESS_METHOD_CONTRACT.md` D-7 (OPEN); CLAUDE.md (e)/(h) | Its D-1 / D-5 records (CLOSED); no arbitrary threshold | BLOCKED (run 2) — SOURCE ACCESS BLOCKED + AUTHORITY BLOCKED: no qualified limit found; next lead (property test basis, span/depth 14) needs FPL-GTR-190 Ch. 5 (host refused). Reopens on a Lead-supplied inspection, host access or an Owner/Lead choice of governing condition | 5 |
| Q-02 | Integration (motor ↔ mechanism) | Preliminary motion requirements: a qualified class-level statement of the load characteristics that govern whether a motor can drive a mechanism. First uninspected candidate: DOE-HDBK-1011/2-92, Volume 2, DC-motor module. | CLAUDE.md (g1) step 3 and (h) "Preliminary motion requirements: BLOCKED"; the Mechanical vs Electrical / Electronics host decision stays with the Owner | Delivered CAP-13 linear speed-dependent rotational load method (`STAGE25_CAP13_LINEAR_SPEED_DEPENDENT_ROTATIONAL_LOAD_METHOD_CONTRACT.md`) and CAP-13 planar required force; record any overlap instead of re-sourcing it | QUALIFIED-CANDIDATE (run 1: SRC-004 class-level, SRC-005 DC-only). Owner host decision still required (AUTHORITY BLOCKED for any adoption) | 2 |
| Q-03 | Integration (controller → output) | Embedded 28-T2 execution-facing output: class-level authoritative, reusable sources only — no owner, method or path selection. | CLAUDE.md (e)/(h) "Embedded 28-T2 output … DEFER pending a specialist owner, source and authorization" | Delivered 28-T2 controller input / logic / output reference (PR #795), control-loop handoff (PR #825), 28-T4 control-cycle evaluation and TEMPERATURE-TO-CONTROL-CONDITION-01; the sensor-to-controller path stays an unauthorized recommendation | QUESTION UNCLEAR / AUTHORITY BLOCKED (run 1). Reopens on an exact claim definition or a 28-T2 specialist owner; electrical part split to Q-05 | 0 |

## Tier 1b — extracted 2026-10-27 at activation (integration B / verification C); reconciled against live `7eeb085`
Category: A individual · B integration (A requirements → interface conditions → B requirements → verification) · C verification.
A source on one technology never establishes compatibility between two; a declared interaction never establishes compatibility, feasibility or safety.

| ID | Cat. | Exact claim to source | Existing owner / obligation | Must not duplicate | Status | Queries used |
|---|---|---|---|---|---|---|
| Q-04 | C (Mechanical) | Verification of a simply supported midspan-load deflection estimate: which measured quantities and test conditions (span, support / load-point geometry, load rate, moisture / temperature) a primary test-method source requires before a model estimate may be compared with an observation. | Stiffness contract §8 (estimate UNVALIDATED) and WS-PFV-001 validation boundary; companion to Q-01 | Q-01 regime criterion; D-5 property records | QUALIFIED-CANDIDATE (run 2: SRC-006, SRC-001 re-read) | 1 |
| Q-05 | B (controller output → driver / load) | Class-level: a logic output drives a load or driver only within its specified output voltage levels and source / sink current; when the load exceeds them an interposed driver stage is required, and the driver's input requirements must be met by the logic output. | 28-T2 / 28-T3 (CLAUDE.md (h)); interface home Stage 15 | E-01 transistor load-switching principle (PR #885); Q-03 output path | SOURCE ACCESS BLOCKED (run 2: NXP AN2434/AN2433 and Kuphaldt Vol. IV hosts refused). Reopens on access or a Lead-supplied inspection | 2 |
| Q-06 | B (power source → load) | Battery / BMS: delivered capacity of a battery depends on discharge rate and temperature, so runtime is not in general rated capacity divided by load current; the conditions under which a simple capacity / current estimate is stated to apply. | Battery / BMS R2 (RECORDED only); charge reference PR #802 | PR #802 Q = I × t and A·h ↔ C reference | QUEUED (Tier 2 order) | 0 |
| Q-07 | B (PLC I/O ↔ field device) | Vendor-neutral class-level: digital input / output electrical types (current sinking vs sourcing, nominal DC levels) and the condition that a field device's output type and levels must match the PLC input type. | 28-T4 (RECORDED — NOT AUTHORIZED) | 28-T4 control-cycle evaluation already delivered | QUEUED (Tier 2 order) | 0 |
| Q-08 | B (feedback ↔ timing) | Sampled-data control: the class-level relation between sampling rate and the bandwidth / dynamics of the controlled process, and the stated conditions for its use. | `control_loop` bounded concept scope; 28-T5 | `control_loop` pack PR001–PR007 concept claims | QUEUED (Tier 2 order) | 0 |
| Q-09 | C (thermal) | Verification of a single-path conduction temperature-difference estimate: which measurements (heat input, two temperatures, contact conditions) a primary source requires to determine a thermal resistance experimentally. | THERM-01 contract validation boundary (WS-PFV-001) | THERM-01 method and its DOE / NIST source records | QUEUED (Tier 2 order) | 0 |
| Q-10 | B (mechanical interface ↔ manufacturing) | Class-level: fits and tolerances between mating parts depend on the chosen manufacturing process capability; source the authoritative, reusable statement of that dependency only. | CAP-12 / CAP-13 Knowledge, Data and Feasibility Boundary | CAP-12 NASA form mock-up claims | QUEUED (Tier 2 order) | 0 |

Reconciled out at extraction (not new questions): sensor output ↔ ADC reference / input impedance / sampling → covered by H-01 (D13 PAUSED);
power dissipation → temperature rise single path → delivered (THERM-01 + DC resistive load power, E-04 / E-05); embedded ↔ IoT data exchange → Stage 31 NOT AUTHORIZED (H-04);
motor torque / speed ↔ mechanical load → Q-02 (verification part recorded inside Q-02).

## Held / excluded (recorded so they are not re-derived)

| ID | Item | Status | Reason |
|---|---|---|---|
| H-01 | X-3 sensor ↔ controller interfacing (D13 TKP-PKG-001 primary-source quotation, AB-1…AB-6, AB-9) | HELD | D13 PAUSED; separate Owner authorization required |
| H-02 | Sensors C3 further source research | HELD | Reopens only with D13 research resumed by the Owner (CLAUDE.md (h)) |
| H-03 | Stage 15 interface characterisation sources | HELD | D4 not activated; reopens only with an authorized interface-characterisation scope |
| E-01 | 28-T3 transistor load-switching principle | EXCLUDED | Delivered (PR #885, 28-T3-LOAD-SWITCHING-PRINCIPLE-REFERENCE-01); no distinct unresolved claim evidenced |
| E-02 | T2-G / R2, MSNL | EXCLUDED | Owner trust / method decision, not source research |
| E-03 | T6 quantity / BOM, calculation-result retention, repeated-units wording | EXCLUDED | Activation / convention decisions, not source research |
| H-04 | Embedded ↔ IoT communication / data exchange | HELD | Stage 31 IoT architecture NOT AUTHORIZED |
| E-05 | Power dissipation → single-path temperature rise | EXCLUDED | Delivered (THERM-01 slice + DC resistive load power) |
| E-04 | Delivered DC resistive load current / power / energy, TMP36 voltage-to-temperature, CAP-13 planar moment / required force / rotational load | EXCLUDED | Delivered |

## Tier 2 — preserved portfolio (preparation only; one at a time, only after Tier 1 is terminal)
Derived one at a time in (g1) step-3 order, each from an existing obligation only (no new owner):
PLC / Automation → Mechatronics / Robotics → Wireless / RF → Battery / BMS → Perception / Edge → IoT → Drone / UAV → Renewables →
Space / Satellite → hydraulics / pneumatics → optics / photonics → materials → acoustics / vibration.
Before working one, add its row here with its exact claim and the existing obligation it comes from; skip any technology with no evidenced open claim.
Source findings for 28-T3 Power Electronics / Motion beyond E-01 enter only if a distinct unresolved claim is evidenced.
