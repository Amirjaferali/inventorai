# TECH-SOURCES-001 — Question register

Reconstructed 2026-10-27 against live merged evidence at `7eeb085` (PR #888). Statuses: `QUEUED`, `IN_PROGRESS`, `QUESTION UNCLEAR`, `EVIDENCE INSUFFICIENT`, `SOURCE CANDIDATE`, `SOURCE ACCESS BLOCKED`, `IP UNRESOLVED`, `METHOD UNQUALIFIED`, `AUTHORITY BLOCKED`,
`QUALIFIED-CANDIDATE`, `BLOCKED`, `ABSTAINED`, `HELD` (not researchable under current authority), `EXCLUDED`;
added 2026-10-28: `PARTIAL` (non-terminal: some points established, a researchable residual remains; `PARTIAL — WAITING: <reason>` is terminal until the reason clears) and `EXHAUSTED` (terminal: residual has no reachable lawful source after the recorded lenses, or the 20-query cap is reached).
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
| Q-07 | B (PLC I/O ↔ field device) | Vendor-neutral class-level: digital input / output electrical types (current sinking vs sourcing, nominal DC levels) and the condition that a field device's output type and levels must match the PLC input type. | 28-T4 (RECORDED — NOT AUTHORIZED) | 28-T4 control-cycle evaluation already delivered | PARTIAL (run 5: SRC-013 levels; run 6: SRC-017 sinking/sourcing concept, I/O circuit types, datasheet limits); explicit pairing rule UNVERIFIED — WAITING: access to ibiblio / nrc.gov or a Lead-supplied inspection | 2 |
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
| Q-11 | Power electronics / motion — roadmap 28-T3 (PWM, drives, switching) | For an idealised switch driven by PWM, the average voltage delivered to a load is the duty cycle times the supply voltage; the conditions (switching frequency relative to the load's electrical / mechanical time constants, ripple, ideal-switch assumptions) under which this average describes the load's response | E-01 transistor switching principle (PR #885) | QUALIFIED-CANDIDATE (run 7: SRC-018; run 13: SRC-042 average ∝ duty cycle; claim since covered by delivered PWM-AVERAGE-VOLTAGE-01, PR #898) | 2 |
| Q-12 | Mechatronics / robotics — roadmap 28-T5 (kinematics checked against Mechanical first) | Planar two-link serial manipulator forward kinematics (end-point position from link lengths and joint angles) and its stated assumptions (rigid links, planar motion, ideal joints) | CAP-13 methods; no Robotics owner implied | IP UNRESOLVED for the residual (run 7: SRC-019 general principle stands; run 14: explicit 2-link formula found only in rights-excluded NTRS documents) | 2 |
| Q-13 | Wireless / RF — roadmap Stage-F named assessment | Free-space received power falls with the square of distance (Friis free-space relation) and the stated conditions (far field, free space, matched antennas, no obstruction / multipath) | No link-budget numerical execution (roadmap exclusion) | QUALIFIED-CANDIDATE (run 7: SRC-020; run 11: SRC-037, SRC-038 far-field / inverse-square conditions) | 3 |
| Q-14 | Battery / BMS — R2 recorded | Cells in series add voltage at the same capacity; cells in parallel add capacity at the same voltage; and the stated reason series strings need cell matching / balancing | Q-06; PR #802 | QUALIFIED-CANDIDATE (run 8: SRC-007, SRC-009 re-read; DOE contractor caveat) | 0 |
| Q-15 | Perception / edge — named assessment | The spatial resolution of an imaging sensor at a given distance follows from field of view and pixel count (projected pixel size), with its stated conditions | Must not absorb 28-T1 sensor acquisition / calibration | SOURCE CANDIDATE — IP UNRESOLVED (run 8: SRC-021 mixed authorship; USGS refused); claim UNVERIFIED | 1 |
| Q-16 | IoT — Stage 31 (NOT AUTHORIZED; research preparation only) | The average current of a duty-cycled device is the time-weighted average of its active and sleep currents, and the stated conditions | Q-06 battery capacity claim; H-01 / D13 sensor ↔ controller stays held | SOURCE CANDIDATE — IP UNRESOLVED (run 8: SRC-022/023); explicit averaging claim UNVERIFIED | 1 |
| Q-17 | Drone / UAV | A hovering multirotor's total thrust equals its weight; thrust margin is needed to climb / manoeuvre; stated conditions | Q-02 motor ↔ load | QUALIFIED-CANDIDATE (run 9: SRC-024, SRC-025) | 1 |
| Q-18 | Renewables | A photovoltaic module's rated power is specified at standard test conditions (irradiance, cell temperature, spectrum); output falls with lower irradiance and higher cell temperature | Q-06 | PARTIAL QUALIFIED-CANDIDATE (run 9: SRC-026; temperature-coefficient statement not yet on clean rights) | 1 |
| Q-19 | Space / satellite | Materials for vacuum use are screened for outgassing (total mass loss / collected volatile condensable material) and the stated screening basis | CAP-12 materials claims | QUALIFIED-CANDIDATE (run 9: SRC-027) | 1 |
| Q-20 | Hydraulics / pneumatics | A double-acting cylinder's retract force is lower than its extend force at equal pressure because the rod reduces the effective area; speed relates to flow and area | Delivered F = pA reference (mechanical:PR006–PR011) | PARTIAL — WAITING: access to publications.usace.army.mil (EM 1110-2-2610) or a Lead-supplied inspection (SRC-028; rod-side area and speed–flow UNVERIFIED) | 3 |
| Q-21 | Optics / photonics | Irradiance from a point-like source falls with the inverse square of distance, with the stated far-field / point-source conditions | Q-13 (different physics domain) | QUALIFIED-CANDIDATE (SRC-030 conditions) | 1 |
| Q-22 | Materials | Thermal expansion: free length change is proportional to the coefficient of expansion, length and temperature change; mismatch between joined materials causes stress / fit change | Q-10 tolerances | QUALIFIED-CANDIDATE (SRC-031, SRC-032; SRC-029 supporting) | 1 |
| Q-23 | Acoustics / vibration (Mechanical extension first) | A single-degree-of-freedom spring–mass system has a natural frequency set by stiffness and mass; excitation near it amplifies response (resonance); stated damping conditions | — | QUEUED | 0 |

## Tier 2 — preserved portfolio (preparation only; one at a time, only after Tier 1 is terminal)
Derived one at a time in (g1) step-3 order, each from an existing obligation only (no new owner):
PLC / Automation → Mechatronics / Robotics → Wireless / RF → Battery / BMS → Perception / Edge → IoT → Drone / UAV → Renewables →
Space / Satellite → hydraulics / pneumatics → optics / photonics → materials → acoustics / vibration.
Before working one, add its row here with its exact claim and the existing obligation it comes from; skip any technology with no evidenced open claim.
Source findings for 28-T3 Power Electronics / Motion beyond E-01 enter only if a distinct unresolved claim is evidenced.
Run 4 (2026-10-27): every remaining label checked — no claim-level open obligation found; no row added (abstention log).


## Selection and depth rules (Owner correction 2026-10-28 — extends Tier 2; supersedes the run-4 "evidenced open claim only" reading)

**Corrected interpretation.** The original mandate authorized preparation for future technologies, integration and verification. Tier 2 rows may
therefore be derived from the concerns already recorded for each future technology in the Master Execution Roadmap — 28-T1…28-T5 entries, the named
assessments (Wireless / RF, Battery / BMS, Perception / Edge), Stage 31 IoT (row 31 and its numbered note), secondary notes C4–C7, and the Satellite
Technology subitem — not only from claims already open in an implementation obligation. A row quotes the roadmap concern it comes from. The roadmap,
its owners and its "must NOT absorb" boundaries are unchanged; a derived row creates no owner, method, activation or authorization.

**Derivation limits.** Each row is ONE class-level engineering claim. Excluded: anything the roadmap entry says the responsibility must not absorb;
legal, certification, regulatory-compliance or safety-approval conclusions; numerical execution (e.g. link budgets, sizing); vendor-specific
material; anything under H-01, H-02, H-03, H-04 or another explicit hold. At most 3 rows derived per run, P1 before P2 before P3.

**Priority.** P1 = material missing evidence for a technology whose recorded concerns are otherwise uncovered or whose existing evidence is only one
introductory point; P2 = deepens a technology with some qualified evidence; P3 = useful but lower product value or near a deferred / premature note.
A wake-up text that names questions is a hint only; this order governs (run 11's text predates the correction).
Existing Tier 2b priorities: Q-13 P1; Q-11, Q-20, Q-23 P2; Q-12, Q-18 P3. Q-15 and Q-16 stay `IP UNRESOLVED` (terminal); their claims are
re-approached only through the new rows below that need a clean-rights source anyway.

**Depth dimensions** (assessment checklist, not separate questions; findings state which apply and which are established):
D1 governing model / equation / relationship · D2 inputs, outputs, units, operating conditions · D3 applicability limits, uncertainty, failure
conditions · D4 integration with other owners / systems · D5 measurement, experiment, validation needs · D6 reusable models, reference
implementations, libraries (with licence) · D7 safety and reliability considerations. Not every dimension applies to every claim; a dimension that
applies but has no lawful source is recorded `UNVERIFIED`, never invented.

**Remaining-run depth discipline (Owner 2026-10-28; binding for the rest of the campaign).** REUSE → RESIDUAL ONLY → STOP. Each finding states,
per applicable D1–D7 dimension, what is sourced: the claim (D1); applicability / assumptions; inputs, outputs, units (D2); limits / failure
conditions (D3); the integration boundary (D4); the measurement / validation need (D5); the IP / reuse basis (IP register). A dimension that
future product use materially needs but no lawful source supports is recorded `UNVERIFIED`; no dimension is invented for completeness. Each
qualified claim carries a usefulness note — calculation, engineering condition, verification / measurement step, bounded decision, existing-owner
handoff, or explanatory / reference only — as research metadata that selects no product work. Every source records whether it was inspected
directly or Lead-supplied, and every supported statement whether it is explicit or only implied; implied is never upgraded to explicit and rights
findings never move between works. Status is reported per question, never per technology or domain. A qualified claim is prepared for later Lead
assessment only — it admits no technology, activates no domain, completes no capability, method or roadmap obligation. Before working a queued
question, confirm its exact recorded claim and obligation and do not widen it; a question with no clean primary source within its bounded effort is
recorded with its blocker and the run moves on (NEXT-LOOP). Do not open an adjacent question because a source mentions it.

**Premature (not derived now; reassess on the named trigger):** Robotics localization / path planning (roadmap 28-T5 reassessment); Perception
dataset / model provenance and edge-inference trade-offs (a concrete perception case); PLC vendor reference layers (separate source / IP review);
Optics, Materials beyond Q-21 / Q-22 (C5 / C6 DEFER); Software and Medical packs (future-domain reassessment pool); thermal beyond THERM-01
(separate authorization). Sensors (28-T1) and sensor ↔ controller research stay HELD (H-01 / H-02); IoT ↔ embedded data exchange stays HELD (H-04).

## Tier 2c — derived 2026-10-28 from recorded future-technology concerns (Owner correction)

| ID | Technology / recorded concern (roadmap) | Exact claim to source (class-level) | Dims | Must not duplicate | P | Status | Queries used |
|---|---|---|---|---|---|---|---|
| Q-24 | IoT — Stage 31 "identity, security, updates" | Baseline device cybersecurity capabilities expected of a connected device (device identification, configuration, data protection, logical access to interfaces, secure software / firmware update, cybersecurity state awareness) and the stated conditions under which a baseline applies | D1 D3 D4 D7 | H-04 data exchange; no compliance conclusion | P1 | QUALIFIED-CANDIDATE (run 11: SRC-034, SRC-035; SRC-033 cross-check only) | 1 |
| Q-25 | IoT — Stage 31 "updates, failure modes" | Firmware / software update integrity and recovery: an update should be authenticated and verified before use, and a device should be able to recover to a known-good state after a failed or corrupted update | D1 D3 D5 D7 | Q-24; 28-T2 output (DR-3) | P1 | QUALIFIED-CANDIDATE (run 11: SRC-036) | 1 |
| Q-26 | IoT — Stage 31 "power, failure modes" | Connected battery-powered devices: sleep / active duty cycling sets average current and so battery life (clean-rights restatement of Q-16), and loss of power or connectivity are failure modes whose device behaviour must be defined | D1 D2 D3 D7 | Q-06, Q-14, Q-16 | P1 | EXHAUSTED (runs 12–14: SRC-039, SRC-043 points stand; explicit time-weighted average and defined power / connectivity-loss behaviour UNVERIFIED) | 3 |
| Q-27 | IoT — Stage 31 "privacy" | Class-level privacy considerations for devices that collect data: data minimisation and protection of data at rest / in transit, stated as considerations, not requirements | D3 D4 D7 | Q-24 | P2 | QUEUED | 0 |
| Q-28 | Wireless / RF — "propagation / channel assumptions; range / interference / coexistence" | Real links depart from free space: obstruction, reflection and multipath fading increase path loss and vary the received signal; devices sharing a band can interfere; the stated conditions under which free-space (Q-13) understates loss | D1 D3 D5 | Q-13 Friis; no link-budget execution | P1 | QUALIFIED-CANDIDATE (run 12: SRC-039, SRC-040, SRC-038; SRC-041 cross-check) | 1 |
| Q-29 | Wireless / RF — "bandwidth / latency concepts" | The channel-capacity relation (Shannon–Hartley, C = B log₂(1 + S/N)) as an upper bound on error-free data rate for a band-limited noisy channel, and its stated assumptions | D1 D2 D3 | Q-28 | P2 | QUEUED | 0 |
| Q-30 | Battery / BMS — "charge / discharge envelopes; BMS functions; battery-specific protection" | Cells must be kept within stated voltage, current and temperature limits during charge and discharge; a BMS monitors these, protects (disconnects) on violation, balances series cells and estimates state of charge | D1 D2 D3 D7 | Q-06, Q-14; 28-T3 charger design; 28-T2 BMS firmware | P1 | QUALIFIED-CANDIDATE (run 12: SRC-009 re-read; SOC-estimation function UNVERIFIED) | 0 |
| Q-31 | Battery / BMS — "cycle-life / degradation concepts" | Capacity fades with cycling and age; depth of discharge, temperature and charge / discharge rate affect cycle life; stated conditions | D1 D3 D5 D7 | Q-06 | P1 | QUALIFIED-CANDIDATE (run 13: SRC-009, SRC-008 re-read) | 0 |
| Q-32 | Power electronics (28-T3) — "power conversion, PWM" | Ideal switching converters in continuous conduction: buck V_out = D·V_in, boost V_out = V_in / (1 − D); the conditions (ideal components, continuous conduction, steady state) and the stated loss / efficiency departures | D1 D2 D3 | Q-11; E-01 | P2 | QUEUED | 0 |
| Q-33 | Power electronics (28-T3) — "motor / actuator class concepts; BLDC / stepper / servo contexts" | Class-level distinctions: a stepper run open-loop can lose steps when load torque exceeds its available torque; a servo uses position feedback; a brushless DC motor needs electronic commutation | D1 D3 D4 D5 | Q-02 (DR-1 Option C split) | P2 | QUEUED | 0 |
| Q-34 | Embedded (28-T2) — "watchdogs, startup / shutdown, fault handling" | A watchdog timer resets or safes a processor when software fails to service it within its timeout; defined startup and fault states | D1 D3 D7 | Q-03 / DR-3 output path; H-01 sensor ↔ controller | P2 | QUEUED | 0 |
| Q-35 | PLC (28-T4) — "interlocks; states / sequences" | An interlock prevents an actuator / output from operating unless defined conditions are met; sequences advance on defined transition conditions | D1 D3 D7 | Delivered 28-T4 control-cycle evaluation; Q-07 | P2 | QUEUED | 0 |
| Q-36 | Satellite — preferred first slice "mission / use-case need, Earth-observation data" | Earth-observation mission parameters trade against each other: spatial resolution, swath / coverage and revisit time depend on orbit altitude and sensor design | D1 D2 D3 | Q-15 (re-approached on clean rights) | P2 | QUEUED | 0 |
| Q-37 | Drone / UAV (Stage 28) | Ideal hover power from momentum theory, P = T^(3/2) / √(2ρA), so endurance depends on weight, rotor disk area and stored energy; stated ideal-rotor assumptions | D1 D2 D3 | Q-17 | P3 | QUEUED | 0 |
| Q-38 | Renewables (Stage 28) | A PV array's current–voltage curve has a maximum power point that shifts with irradiance and temperature; maximum-power-point tracking keeps operation near it | D1 D2 D3 | Q-18 | P3 | QUEUED | 0 |
| Q-39 | Satellite — "power and eclipse / margins" | During eclipse a spacecraft runs on stored energy, so array and battery are sized for the sunlit load plus recharge; stated assumptions | D1 D2 D3 D7 | Q-19, Q-30 | P3 | QUEUED | 0 |
| Q-40 | Acoustics / vibration (C7, Mechanical first) | Vibration isolation / transmissibility: transmitted force is reduced only above √2 times the natural frequency; damping trades resonance amplification against high-frequency isolation | D1 D3 D5 | Q-23 | P3 | QUEUED | 0 |
