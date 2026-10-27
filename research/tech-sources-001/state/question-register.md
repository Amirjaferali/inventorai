# TECH-SOURCES-001 — Question register

Reconstructed 2026-10-27 against live merged evidence at `7eeb085` (PR #888). Statuses: `QUEUED`, `IN_PROGRESS`, `QUESTION UNCLEAR`, `EVIDENCE INSUFFICIENT`, `SOURCE CANDIDATE`, `SOURCE ACCESS BLOCKED`, `IP UNRESOLVED`, `METHOD UNQUALIFIED`, `AUTHORITY BLOCKED`,
`QUALIFIED-CANDIDATE`, `BLOCKED`, `ABSTAINED`, `HELD` (not researchable under current authority), `EXCLUDED`.
A question is worked only within its exact claim; findings never decide the owner, host, method admission or activation.

## Tier 1 — existing open engineering questions

| ID | Kind | Exact claim to source | Existing owner / obligation | Must not duplicate | Status | Queries used |
|---|---|---|---|---|---|---|
| Q-01 | Individual (Mechanical) | CAP-13 D-7 METHOD-REGIME QUALIFICATION: from a technically authoritative, lawfully reusable source, whether the governing applicability issue for the bounded stiffness method is small-deflection validity, short / deep-member applicability or another source-defined regime condition, and the exact machine-checkable criterion if one exists. | `docs/governance/STAGE25_CAP13_BOUNDED_STIFFNESS_METHOD_CONTRACT.md` D-7 (OPEN); CLAUDE.md (e)/(h) | Its D-1 / D-5 records (CLOSED); no arbitrary threshold | QUALIFIED-CANDIDATE for the inspected facts (run 6: SRC-014/015/016 — test geometry span/depth 14 VERIFIED; no machine-checkable criterion exists in them) + AUTHORITY BLOCKED (DR-2). Earlier: BLOCKED (run 2) — SOURCE ACCESS BLOCKED + AUTHORITY BLOCKED: no qualified limit found; next lead (property test basis, span/depth 14) needs FPL-GTR-190 Ch. 5 (host refused). Reopens on a Lead-supplied inspection, host access or an Owner/Lead choice of governing condition. Run 5: no legal alternative on reachable hosts; property-basis and small-deflection claims UNVERIFIED | 7 |
| Q-02 | Integration (motor ↔ mechanism) | Preliminary motion requirements: a qualified class-level statement of the load characteristics that govern whether a motor can drive a mechanism. First uninspected candidate: DOE-HDBK-1011/2-92, Volume 2, DC-motor module. | CLAUDE.md (g1) step 3 and (h) "Preliminary motion requirements: BLOCKED"; the Mechanical vs Electrical / Electronics host decision stays with the Owner | Delivered CAP-13 linear speed-dependent rotational load method (`STAGE25_CAP13_LINEAR_SPEED_DEPENDENT_ROTATIONAL_LOAD_METHOD_CONTRACT.md`) and CAP-13 planar required force; record any overlap instead of re-sourcing it | QUALIFIED-CANDIDATE (run 1: SRC-004 class-level, SRC-005 DC-only). Ownership decided by the Owner (DR-1 Option C, base 692c2d9); no adoption implied | 2 |
| Q-03 | Integration (controller → output) | Embedded 28-T2 execution-facing output: class-level authoritative, reusable sources only — no owner, method or path selection. | CLAUDE.md (e)/(h) "Embedded 28-T2 output … DEFER pending a specialist owner, source and authorization" | Delivered 28-T2 controller input / logic / output reference (PR #795), control-loop handoff (PR #825), 28-T4 control-cycle evaluation and TEMPERATURE-TO-CONTROL-CONDITION-01; the sensor-to-controller path stays an unauthorized recommendation | QUESTION UNCLEAR / AUTHORITY BLOCKED (run 1; run 6: no exact claim in any record — DR-3). Reopens on an exact claim definition or a 28-T2 specialist owner; electrical part split to Q-05 | 0 |

## Tier 1b — extracted 2026-10-27 at activation (integration B / verification C); reconciled against live `7eeb085`
Category: A individual · B integration (A requirements → interface conditions → B requirements → verification) · C verification.
A source on one technology never establishes compatibility between two; a declared interaction never establishes compatibility, feasibility or safety.

| ID | Cat. | Exact claim to source | Existing owner / obligation | Must not duplicate | Status | Queries used |
|---|---|---|---|---|---|---|
| Q-04 | C (Mechanical) | Verification of a simply supported midspan-load deflection estimate: which measured quantities and test conditions (span, support / load-point geometry, load rate, moisture / temperature) a primary test-method source requires before a model estimate may be compared with an observation. | Stiffness contract §8 (estimate UNVALIDATED) and WS-PFV-001 validation boundary; companion to Q-01 | Q-01 regime criterion; D-5 property records | QUALIFIED-CANDIDATE (run 2: SRC-006, SRC-001 re-read; run 6: moisture / temperature / rate / creep from SRC-014) | 1 |
| Q-05 | B (controller output → driver / load) | Class-level: a logic output drives a load or driver only within its specified output voltage levels and source / sink current; when the load exceeds them an interposed driver stage is required, and the driver's input requirements must be met by the logic output. | 28-T2 / 28-T3 (CLAUDE.md (h)); interface home Stage 15 | E-01 transistor load-switching principle (PR #885); Q-03 output path | SOURCE ACCESS BLOCKED (run 2: NXP AN2434/AN2433 and Kuphaldt Vol. IV hosts refused). Reopens on access or a Lead-supplied inspection. Run 5: no legal alternative reachable; run 6: ibiblio now fails TLS trust (emSign root absent) — claim UNVERIFIED | 4 |
| Q-06 | B (power source → load) | Battery / BMS: delivered capacity of a battery depends on discharge rate and temperature, so runtime is not in general rated capacity divided by load current; the conditions under which a simple capacity / current estimate is stated to apply. | Battery / BMS R2 (RECORDED only); charge reference PR #802 | PR #802 Q = I × t and A·h ↔ C reference | QUALIFIED-CANDIDATE (run 3: SRC-008, SRC-009, SRC-007) | 1 |
| Q-07 | B (PLC I/O ↔ field device) | Vendor-neutral class-level: digital input / output electrical types (current sinking vs sourcing, nominal DC levels) and the condition that a field device's output type and levels must match the PLC input type. | 28-T4 (RECORDED — NOT AUTHORIZED) | 28-T4 control-cycle evaluation already delivered | PARTIAL (run 5: SRC-013 levels; run 6: SRC-017 sinking/sourcing concept, I/O circuit types, datasheet limits); explicit pairing rule UNVERIFIED — reopens on access to ibiblio / nrc.gov or a Lead-supplied inspection | 2 |
| Q-08 | B (feedback ↔ timing) | Sampled-data control: the class-level relation between sampling rate and the bandwidth / dynamics of the controlled process, and the stated conditions for its use. | `control_loop` bounded concept scope; 28-T5 | `control_loop` pack PR001–PR007 concept claims | QUALIFIED-CANDIDATE (run 3: SRC-010) | 1 |
| Q-09 | C (thermal) | Verification of a single-path conduction temperature-difference estimate: which measurements (heat input, two temperatures, contact conditions) a primary source requires to determine a thermal resistance experimentally. | THERM-01 contract validation boundary (WS-PFV-001) | THERM-01 method and its DOE / NIST source records | QUALIFIED-CANDIDATE (run 4: SRC-011) | 1 |
| Q-10 | B (mechanical interface ↔ manufacturing) | Class-level: fits and tolerances between mating parts depend on the chosen manufacturing process capability; source the authoritative, reusable statement of that dependency only. | CAP-12 / CAP-13 Knowledge, Data and Feasibility Boundary | CAP-12 NASA form mock-up claims | QUALIFIED-CANDIDATE (run 4: SRC-012; process-dependence point indirect) | 1 |

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


## Tier 2b — portfolio preparation questions (derived 2026-10-27, run 6, on the Owner's instruction to cover every recorded technology)
Order follows (g1) step 3. Research preparation only: no method admission, implementation or activation; D13 PAUSED, D4 NOT ACTIVATED,
28-T* items stay RECORDED — NOT AUTHORIZED. Each is a class-level principle with its applicability conditions and verification needs.

| ID | Technology / obligation | Exact claim to source (class-level) | Must not duplicate | Status | Queries used |
|---|---|---|---|---|---|
| Q-11 | Power electronics / motion — roadmap 28-T3 (PWM, drives, switching) | For an idealised switch driven by PWM, the average voltage delivered to a load is the duty cycle times the supply voltage; the conditions (switching frequency relative to the load's electrical / mechanical time constants, ripple, ideal-switch assumptions) under which this average describes the load's response | E-01 transistor switching principle (PR #885) | PARTIAL QUALIFIED-CANDIDATE (run 7: SRC-018; duty × supply implied only) | 1 |
| Q-12 | Mechatronics / robotics — roadmap 28-T5 (kinematics checked against Mechanical first) | Planar two-link serial manipulator forward kinematics (end-point position from link lengths and joint angles) and its stated assumptions (rigid links, planar motion, ideal joints) | CAP-13 methods; no Robotics owner implied | PARTIAL QUALIFIED-CANDIDATE (run 7: SRC-019 general principle; explicit 2-link formula UNVERIFIED — IP) | 1 |
| Q-13 | Wireless / RF — roadmap Stage-F named assessment | Free-space received power falls with the square of distance (Friis free-space relation) and the stated conditions (far field, free space, matched antennas, no obstruction / multipath) | No link-budget numerical execution (roadmap exclusion) | PARTIAL QUALIFIED-CANDIDATE (run 7: SRC-020; far-field / inverse-square conditions UNVERIFIED — NTIA host refused) | 1 |
| Q-14 | Battery / BMS — R2 recorded | Cells in series add voltage at the same capacity; cells in parallel add capacity at the same voltage; and the stated reason series strings need cell matching / balancing | Q-06; PR #802 | QUALIFIED-CANDIDATE (run 8: SRC-007, SRC-009 re-read; DOE contractor caveat) | 0 |
| Q-15 | Perception / edge — named assessment | The spatial resolution of an imaging sensor at a given distance follows from field of view and pixel count (projected pixel size), with its stated conditions | Must not absorb 28-T1 sensor acquisition / calibration | SOURCE CANDIDATE — IP UNRESOLVED (run 8: SRC-021 mixed authorship; USGS refused); claim UNVERIFIED | 1 |
| Q-16 | IoT — Stage 31 (NOT AUTHORIZED; research preparation only) | The average current of a duty-cycled device is the time-weighted average of its active and sleep currents, and the stated conditions | Q-06 battery capacity claim; H-01 / D13 sensor ↔ controller stays held | SOURCE CANDIDATE — IP UNRESOLVED (run 8: SRC-022/023); explicit averaging claim UNVERIFIED | 1 |
| Q-17 | Drone / UAV | A hovering multirotor's total thrust equals its weight; thrust margin is needed to climb / manoeuvre; stated conditions | Q-02 motor ↔ load | QUALIFIED-CANDIDATE (run 9: SRC-024, SRC-025) | 1 |
| Q-18 | Renewables | A photovoltaic module's rated power is specified at standard test conditions (irradiance, cell temperature, spectrum); output falls with lower irradiance and higher cell temperature | Q-06 | PARTIAL QUALIFIED-CANDIDATE (run 9: SRC-026; temperature-coefficient statement not yet on clean rights) | 1 |
| Q-19 | Space / satellite | Materials for vacuum use are screened for outgassing (total mass loss / collected volatile condensable material) and the stated screening basis | CAP-12 materials claims | QUALIFIED-CANDIDATE (run 9: SRC-027) | 1 |
| Q-20 | Hydraulics / pneumatics | A double-acting cylinder's retract force is lower than its extend force at equal pressure because the rod reduces the effective area; speed relates to flow and area | Delivered F = pA reference (mechanical:PR006–PR011) | QUEUED | 0 |
| Q-21 | Optics / photonics | Irradiance from a point-like source falls with the inverse square of distance, with the stated far-field / point-source conditions | Q-13 (different physics domain) | QUEUED | 0 |
| Q-22 | Materials | Thermal expansion: free length change is proportional to the coefficient of expansion, length and temperature change; mismatch between joined materials causes stress / fit change | Q-10 tolerances | QUEUED | 0 |
| Q-23 | Acoustics / vibration (Mechanical extension first) | A single-degree-of-freedom spring–mass system has a natural frequency set by stiffness and mass; excitation near it amplifies response (resonance); stated damping conditions | — | QUEUED | 0 |

## Tier 2 — preserved portfolio (preparation only; one at a time, only after Tier 1 is terminal)
Derived one at a time in (g1) step-3 order, each from an existing obligation only (no new owner):
PLC / Automation → Mechatronics / Robotics → Wireless / RF → Battery / BMS → Perception / Edge → IoT → Drone / UAV → Renewables →
Space / Satellite → hydraulics / pneumatics → optics / photonics → materials → acoustics / vibration.
Before working one, add its row here with its exact claim and the existing obligation it comes from; skip any technology with no evidenced open claim.
Source findings for 28-T3 Power Electronics / Motion beyond E-01 enter only if a distinct unresolved claim is evidenced.
Run 4 (2026-10-27): every remaining label checked — no claim-level open obligation found; no row added (abstention log).
