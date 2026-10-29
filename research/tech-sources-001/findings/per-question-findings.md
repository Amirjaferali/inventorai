# TECH-SOURCES-001 — per question findings

Append-only. A finding is at most `QUALIFIED-CANDIDATE`: never admitted, adopted or a closure of any gate.

## Q-01 — CAP-13 D-7 method-regime qualification (run 1, 2026-10-27) — IN_PROGRESS / EVIDENCE INSUFFICIENT for closure
PCRA: the 2026-10-14 scout leads in the stiffness contract §12 were reused; this run inspected them directly instead of re-discovering.
- NACA Report 180 (SRC-001), the lead already named "strong": inspected. It is the experimental lineage of the method's shear-inclusive form —
  its Table I formula Δ = Pl³/48EI + 0.3Pl/AF has the same shear term as Equation 9-2 with A′ = 5bh/6 (Lead algebra, not a source statement) —
  and also the origin of the "+10 % modulus" practice the contract's D5-3 record cites from the Wood Handbook. It shows the shear-inclusive
  formula agreeing closely with tests on solid rectangular Douglas-fir beams over spans of 2 ft to 14 ft (nominal 2¾ × 5 in). Its span-depth
  numbers (12–28 ×, 20–25 ×) concern only when the bending-only formula may neglect shear. It states no lower validity limit for the
  shear-inclusive formula, no small-deflection limit and no proportional-limit condition.
- NASA TN D-7572 (SRC-002): its length-to-depth statements are for resins with unequal tension / compression moduli and an isotropic G;
  not transferable to clear wood (abstained).
- NASA TM-86442 (SRC-003): the small-deflection condition exists only qualitatively ("small with respect to beam length").
- FPL-RN-0210 (Orosz 1970): SOURCE ACCESS BLOCKED (USDA host refused); per its catalogue abstract it addresses whether shear deflection is
  important — the same shear-significance question, not a validity regime.
Result: the regime question is sharper, not closed. Candidate governing conditions remain (i) small deflection, (ii) a short-span limit for the
shear-inclusive formula, (iii) an elastic / proportional-limit condition; no machine-checkable criterion from a qualified source has been found
for any of them. Next action: one source-targeted search for an explicit small-deflection limit for a simply supported beam, and for a stated
lower span / depth applicability limit of the Timoshenko-type (shear-inclusive) deflection formula in a federal / open source.

## Q-02 — Preliminary motion requirements: load characteristics that govern whether a motor can drive a mechanism (run 1) — QUALIFIED-CANDIDATE
- Directly inspected motor-type-neutral source: NASA TM X-68244 (SRC-004). Class-level claims: a motor drives a mechanism only if its torque
  can meet the load's torque requirement over the whole speed range from start to operating speed — breakaway, accelerating (inertia and
  permissible start time) and running torque; steady speed means supplied torque equals demanded torque, and changing speed means upsetting
  that balance (rotary Newton's second law); horsepower alone does not establish it; inertia referred through a speed reduction divides by
  the ratio squared.
- Supporting, DC-only: DOE-HDBK-1011/2-92 ES-06 (SRC-005) — steady DC-motor speed where developed torque falls to the load requirement;
  continuous nameplate rating is a thermal rating. Recorded as DC-specific only, as (g1) step 3 requires.
- Integration framing (Motor requirements → interface conditions → Mechanism requirements → verification): motor torque–speed capability and
  thermal (continuous) rating → shaft speed, torque and reflected inertia across the transmission → mechanism breakaway, accelerating and
  running torque over its speed range → verification needs the load's torque at start and across speeds (measurement or documentation) and
  the motor's torque–speed and thermal data. Sources describe each side; none establishes compatibility for a particular pairing.
- Overlap: the delivered CAP-13 linear speed-dependent rotational load method evaluates one declared running-load model and explicitly does not
  discharge this blocker; SRC-004 adds the breakaway / accelerating categories and the torque-balance condition it lacks. No re-sourcing of it.
- Still open, not research: the Mechanical vs Electrical / Electronics host decision (Owner) and any method admission. Not inspected:
  DOE AMO motor sourcebook, NTRS 19770020365 (SOURCE CANDIDATE).

## Q-03 — Embedded 28-T2 execution-facing output (run 1) — QUESTION UNCLEAR / AUTHORITY BLOCKED
No exact scientific claim is defined: "execution-facing output" covers program logic, timing and settings, which CLAUDE.md (e)/(h) defers until a
specialist owner, source and authorization exist; sourcing it now would amount to choosing the owner or path. No query spent. The electrically
defined part (a logic output's voltage / current capability versus a driver's input) is registered separately as Q-05. Reopening trigger:
an Owner / Lead definition of the exact claim, or a specialist owner for 28-T2 output.

## Q-01 — run 2 (2026-10-27) — BLOCKED (terminal for this campaign until a trigger below)
- Searched (principle + source-targeted): no federal / open source states a lower validity limit for a shear-inclusive (Timoshenko-type)
  deflection formula or a numeric small-deflection limit for a simply supported beam. Journal / thesis thresholds found are not wood-specific,
  have unverified rights and would be arbitrary for D-7 (abstained).
- New lead: the method's property basis. Search snippets attribute a minimum span-to-depth ratio of 14 to the ASTM D143 centre-loaded
  small-clear bending test from which tabulated bending moduli are derived; the Wood Handbook's "+10 %" shear correction (D5-3) would then be
  tied to that geometry. Not inspected: ASTM is protected (mirrors only) and the Wood Handbook host is refused.
- Reopening triggers (any one): (1) a Lead-supplied direct inspection of FPL-GTR-190 Chapter 5 (Table 5-3a notes / page 5-2 test basis) and
  of FPL-RN-0210, following the D-5 precedent; (2) egress to research.fs.usda.gov; (3) the Owner / Lead choosing which governing condition D-7
  must address (small deflection, short-span limit of the shear-inclusive form, elastic limit, or consistency with the property test geometry).
- Queries used on Q-01: 5 of 20.

## Q-04 — Verification of a simply supported midspan deflection estimate (run 2) — QUALIFIED-CANDIDATE (class-level)
Measurements and conditions that federal test reports record before a measured deflection is compared with a model:
1. Midspan deflection measured relative to the supports, i.e. support / end movement removed (NBS Report 10568, p. 39; NACA 180, pp. 5–6).
2. The actual span, cross-section and the loading arrangement (centre load) for each test (NACA 180).
3. The applied load from a calibrated testing machine, read with the deflection (NACA 180).
4. Moisture content of the tested wood determined (NACA 180) — the method's property basis is stated at about 12 % (stiffness contract §7).
5. Loads kept well within the elastic limit (NACA 180).
6. Where the shear term matters, the modulus of rigidity determined separately (torsion tests) rather than assumed (NACA 180).
7. Lateral restraint where the beam tends to buckle (NACA 180).
Limits: 1924 / 1970s federal test practice, not a current test standard; current protected standards (ASTM D198 / D143) exist but were not
inspected (IP). Temperature and loading-rate effects on wood stiffness are not sourced here (Wood Handbook host blocked). None of this
validates the stiffness estimate; it lists what a comparison would need to record.

## Q-05 — Logic output ↔ driver / load (run 2) — SOURCE ACCESS BLOCKED (terminal until trigger)
- Discovered candidates that state the claim directly: NXP (Freescale) AN2434 *Input/Output Pin Drivers on HCS12 Family MCUs* (output levels
  are guaranteed only within a specified pin current; heavier loads cannot hold the logic level; absolute-maximum source / sink limits) and
  AN2433 (driver input logic-high threshold must sit below the MCU's minimum output high, otherwise a level shifter is needed). Also
  Kuphaldt, *Lessons in Electric Circuits* Vol. IV (CC BY 4.0 online edition, same series as admitted PR026 / PR027 — licence not
  transferable to another volume without checking its own appendix).
- Not inspected: www.nxp.com and www.ibiblio.org refused by the egress proxy. Federal hosts returned only 1960s circuit-specific material.
- Reopening triggers: host access, or a Lead-supplied inspection of one of the candidates with its rights basis (manufacturer terms of use are
  IP UNRESOLVED; the Kuphaldt Vol. IV appendix must be read for its own licence).

## Q-06 — Battery delivered capacity vs discharge rate and temperature (run 3) — QUALIFIED-CANDIDATE (class-level, two chemistries)
- Directly inspected: NASA/TM-2009-215751 (Li-ion) and DOE-HDBK-1084-95 (lead-acid); supporting DOE-HDBK-1011/2-92 ES-04.
- Claim supported: a battery's rated capacity is defined at stated conditions — discharge rate (C-rate), temperature and cutoff voltage; at a
  higher rate or lower temperature the delivered capacity is lower (falling off fastest with both together); internal resistance lowers the
  terminal voltage under load. Therefore runtime = rated A·h ÷ load current holds only approximately and only near the rating conditions.
- Integration framing (battery → interface → load → verification): battery rating conditions → load current profile, ambient temperature and the
  load's minimum operating voltage (which sets the effective cutoff) → load requirement for duration → verification needs the discharge data at
  the actual current and temperature to the load's cutoff. Not established: any specific runtime, chemistry choice or BMS behaviour.
- Overlap respected: PR #802 (Q = I·t; A·h is charge) is not re-sourced; one DOE sentence conflicts with it (logged).

## Q-07 — PLC discrete I/O ↔ field device (run 3) — SOURCE ACCESS BLOCKED (terminal until trigger)
- The claim (a sourcing input / output must pair with a sinking device and vice versa; levels must match) is stated in Kuphaldt's PLC course
  material (ibiblio, refused) and an NRC document (nrc.gov, refused); OSTI / NTRS searches found no federal statement.
- Reopening triggers: host access, or a Lead-supplied inspection with the licence of the exact file.

## Q-08 — Sampled-data control: sample rate vs controlled-process dynamics (run 3) — QUALIFIED-CANDIDATE (class-level)
- Directly inspected: NASA TM-88346 (Tischler, 1987). Supported: the sample rate of a digital control loop is chosen relative to the desired
  closed-loop bandwidth; sampling plus hold adds an effective delay of about half a sample period, plus computational delay, which appears as
  phase lag; content above half the sample rate aliases into lower frequencies unless an analog anti-aliasing filter precedes the sampler;
  too-low rates cause roughness, actuator limiting and intersample ripple.
- Not adopted: any numeric ratio — the NASA documents found give different rules of thumb (logged).
- Overlap: fills only the gap the admitted `control_loop` pack explicitly excludes ("no claim about the controller's action or update rate");
  nothing is admitted or added to that pack.

## Q-09 — Verifying a single-path conduction temperature-difference estimate (run 4) — QUALIFIED-CANDIDATE (class-level)
- Directly inspected: NIST SP 400-86 (1990). What a measurement of a thermal resistance needs: the dissipated power measured where the heat is
  generated (lead / contact voltage drop can overstate it); the reference temperature held constant at a stated, fixed location (surfaces are not
  isothermal); the temperature indicator calibrated over the range used; and awareness that the single-number definition assumes a uniform
  heated region and operating-condition independence, which real devices do not strictly meet.
- Fit with THERM-01: consistent with its declarations D-1 to D-6 and its UNVALIDATED result; it adds what physical validation (WS-PFV-001) would
  have to record. Nothing is admitted; no number adopted.

## Q-10 — Fits and tolerances ↔ manufacturing process (run 4) — QUALIFIED-CANDIDATE (class-level, one indirect point)
- Directly inspected: NISTIR 4509 (1991). Supported: every process yields dimensional variation, so a tolerance zone must be specified; tolerancing
  should permit the most efficient production method; variation arises from process errors (machining, set-up, alignment); the resulting fit
  (clearance / transition / interference) depends on the actual mating features.
- Indirect: "the achievable tolerance depends on the chosen process" is implied rather than stated outright. Protected limits-and-fits tables
  (ASME / ISO) not used. CAP-12 claims not re-sourced.

## Tier 2 portfolio check (run 4) — no further questions derivable under current obligations
Per the README, every remaining Tier-2 label was checked against the roadmap, the Capability Enrichment Register and the Deferred Obligations
Register: none carries a claim-level open obligation (they are routing directions to existing owners). No question was invented.

## Run 5 (2026-10-27) — Owner-directed search for legal official alternatives (Q-01, Q-05, Q-07)
Reachable authoritative hosts this session: ntrs.nasa.gov, osti.gov, nvlpubs.nist.gov / nist.gov, energy.gov (and github.com, used only to
look for an author-published original). Every other candidate host was refused by the environment's network policy (blocked-host log).

- **Q-01 — still BLOCKED.** Searched NTRS, OSTI and NIST for (a) any edition of the USDA *Wood Handbook* or a federal report stating the
  small-clear bending test geometry (span-to-depth 14) behind its moduli, and (b) a source stating a numeric small-deflection limit for a simply
  supported beam. Found only reports that cite ASTM D143 without stating the geometry, and large-deflection studies of other configurations.
  **UNVERIFIED:** "the tabulated bending moduli rest on centre-loaded tests at span-to-depth 14" and any numeric small-deflection limit.
- **Q-05 — still SOURCE ACCESS BLOCKED.** The author publishes *Lessons in Electric Circuits* / ModEL only on ibiblio (CC BY 4.0 per the
  author's index page); the Open Book Project and archive.org copies are refused and the archive.org copies are third-party older-licence mirrors.
  Federal hosts give no class-level statement. **UNVERIFIED:** the logic-output-drive claim.
- **Q-07 — partially supported, otherwise UNVERIFIED.** NISTIR 5331 (SRC-013) supports only that 0–24 V points are the typical discrete I/O
  interface. **UNVERIFIED:** that a sourcing I/O point must be paired with a sinking device and vice versa, and the level-matching rule.
- **Q-03 — not executable:** needs an exact claim definition (Owner / Lead), not a source.

## Run 6 (2026-10-27) — resumed after source access verification

### Q-01 — D-7 applicability: what the original USDA sources establish (SRC-014, SRC-015, SRC-016; NACA 180 and TM-86442 reused)
| Candidate condition | What the inspected sources establish | Machine-checkable criterion? |
|---|---|---|
| Small-deflection assumption | Not stated in Ch. 5, Ch. 9 or FPL-0210. Only NASA TM-86442 (run 1): linear beam theory holds when deflections are small relative to length. | **No** — UNVERIFIED as a numeric limit |
| Elastic-material condition | Ch. 9: Eq. 9–2 is for *elastically stressed* beams; stress equations assume Hooke's law. Ch. 5: elastic = low-stress, fully recoverable; higher stress → plastic deformation or failure; the MOR formula is valid only to the elastic limit. FPL-0210 also rests on Hooke's law. | **No** numeric bending elastic or proportional limit in these chapters (Table 5–3 gives MOR, not a bending proportional-limit stress) |
| Span-to-depth / shear | Eq. 9–2 already includes the shear term (k_s; A′ = 5bh/6, consistent with FPL-0210's k = 6/5 for a rectangle — Lead algebra). NACA 180 (run 1): shear may be neglected in the bending-only formula above about 20–25× depth; the shear-inclusive formula matched tests on spans of 2–14 ft. FPL-0210: no numeric threshold. | **No** validity limit for the shear-inclusive formula |
| Material-property test geometry | **VERIFIED:** Table 5–3a/b footnote c — E measured on a simply supported, centre-loaded beam at span-to-depth **14/1**; +10 % approximately removes the shear effect (p. 5–8). Static tests reach maximum load in about 5 min (p. 5–38); clear, straight-grained specimens, green or 12 % moisture. | Yes as a *property basis fact*; it is not stated as a limit on where Eq. 9–2 may be used |
| Other source-stated validity conditions of the method | Straight beam; constant cross-section (holes / notches change it); initial bow / twist amplified; lateral / torsional restraint may be needed; creep adds time-dependent deflection; properties change with moisture and temperature. | Qualitative conditions only |
Result: QUALIFIED-CANDIDATE for the facts above (direct inspection, federal-work basis). **The sources do not supply a machine-checkable validity criterion for any candidate condition.** The four conditions are distinct and are not interchangeable. Choosing which governs D-7 — or whether qualitative declarations can satisfy it — is the Owner's decision (see decision record D-7).

### Q-04 — supplement (gap from run 2 filled)
Ch. 5 (SRC-014) supplies what run 2 could not source: moisture content (properties rise as moisture falls below fibre saturation, 5–34), temperature (properties fall when heated and rise when cooled, reversibly below about 150 °C at constant moisture, 5–35), rate of loading (tabulated values are static, about 5 min to maximum load, 5–38) and creep (deflection grows with time under load, 5–38/39; Ch. 9 p. 9–2). A comparison of a measured deflection with the estimate must therefore also record moisture content, temperature, load duration / rate and specimen condition. Q-04 stays QUALIFIED-CANDIDATE, now complete for these conditions.

### Q-05 — Logic output ↔ driver input — SOURCE ACCESS BLOCKED (new cause: TLS trust), claim UNVERIFIED
The Vol. IV contents page (index) was read at the morning access check (it lists Chapter 3 "Logic Gates" and Appendix 3 "CC BY License"); the chapter and licence pages now fail certificate verification (blocked-host log). No passage inspected, so nothing is qualified. NXP AN2434 stays blocked by NXP's own server (404 page).

### Q-07 — PLC I/O ↔ field devices — PARTIAL (improved)
Supported now (SRC-017, CC BY 4.0, directly inspected): an output may sink current rather than source it; DC I/O uses optocoupled inputs and transistor outputs, AC I/O uses rectified optocoupled inputs and TRIAC outputs; the I/O datasheet's channel count, voltage and current limits and sourcing / sinking capability must be checked before connection (with NISTIR 5331: 0–24 V typical discrete levels). **Still UNVERIFIED:** the explicit pairing rule (sourcing ↔ sinking) as stated text — this module presents it only as exercises; the instructor worksheet that states it is on the same ibiblio host (TLS-blocked). Verification needed before connecting devices (source-supported): the module's datasheet limits and its sourcing / sinking designation versus the field device's.

### Q-03 — exact claim still undefined
The only record naming "execution-facing output" is CLAUDE.md (e) ("Embedded 28-T2 execution-facing output: DEFER pending a specialist owner, source and authorization"). Roadmap 28-T2 lists candidate concerns (execution states, timing, interrupts, ADC / PWM, UART / SPI / I²C / CAN, watchdogs, start-up / shutdown, fault handling, memory / power modes, bare-metal vs RTOS) — concerns, not a claim. Missing definition: which concern, and what exact statement, the "output" is.

## Run 7 (2026-10-27) — portfolio questions Q-11, Q-12, Q-13

### Q-11 — PWM average voltage (28-T3) — PARTIAL QUALIFIED-CANDIDATE
SRC-018 (NASA MSFC, 1969) supports: the PWM period must be much shorter than the winding's electrical time constant; with a free-wheeling
path the inductance keeps current continuous and smooth; switches are fully on or off (low dissipation); average supply current is much
lower than motor current at small duty cycles. **Implied, not stated:** average applied voltage = duty × supply (worked example only).
Verification a design would need: switching frequency vs electrical time constant, current ripple, free-wheeling path. No numbers adopted.

### Q-12 — Two-link planar forward kinematics (28-T5) — PARTIAL QUALIFIED-CANDIDATE
SRC-019 (NBS, 1988) supports the general principle: end-effector position / orientation follows from joint angles through successive
coordinate transformations with constant link lengths. **UNVERIFIED on a clean-rights source:** the explicit planar two-link formula and its
stated assumptions (found only in contractor / lab documents with unresolved rights). Kinematics stays checked against Mechanical first
(roadmap 28-T5); no Robotics owner implied.

### Q-13 — Free-space path loss (Wireless / RF) — PARTIAL QUALIFIED-CANDIDATE
SRC-020 (NASA Ames) supports: free-space loss arises from beam spreading with distance; the link budget combines transmit power, antenna
gains, free-space loss and other losses; field losses exceed theory, so large margins are needed. **UNVERIFIED:** the explicit
inverse-square / far-field conditions — the NTIA definitions host is refused and the NIST mmWave paper (path-loss exponent 2 in free space)
has unresolved rights. No link-budget numbers executed (roadmap exclusion).

## Run 8 (2026-10-27, Owner-authorized early run)

### Q-14 — Cells in series / parallel and balancing — QUALIFIED-CANDIDATE (reuse only; no new query or fetch)
DOE ES-04 pp. 10–11 (SRC-007): series → voltages add, same current; parallel → same voltage, greater current-carrying capability.
NASA/TM-2009-215751 pp. 9, 11, 12 (SRC-009): series strings need voltage control so the weakest cell is not reversed; cycling unbalances
cells; cell protective devices behave differently in series / parallel designs. IP: NASA part clean; DOE part carries the handbook-series
contractor caveat (as SRC-005). Verification a design would need: cell matching and per-cell voltage monitoring for series strings.

### Q-15 — Imaging spatial resolution — SOURCE CANDIDATE, IP UNRESOLVED
The only inspected statement (SRC-021: ground sampling distance is the pixel size and depends on IFOV and altitude; in-track and cross-track
may differ for wide fields) comes from a mixed NASA / contractor preprint. USGS host refused. Claim stays UNVERIFIED on a clean-rights source.

### Q-16 — Duty-cycled average current — SOURCE CANDIDATE, IP UNRESOLVED
NIST-hosted papers (SRC-022, SRC-023) state that capacity ÷ current lifetime does not hold for real batteries, that equal average currents
need not give equal lifetimes, and that sleep modes and short transmissions extend life. The explicit time-weighted-average statement was
not found in an inspected clean-rights source → UNVERIFIED. The caveat itself is consistent with qualified Q-06 sources (SRC-008, SRC-009).
Stage 31 IoT remains not authorized.

## Run 9 (2026-10-27, scheduled wake-up)

### Q-17 — Multirotor hover thrust and margin — QUALIFIED-CANDIDATE (class-level)
NASA Ames papers (SRC-024, SRC-025): in hover, thrust depends on (is set by) the aircraft weight; the torque / speed margin left after trim is
what allows climbing and manoeuvring, and sizing at full installed power would leave no control margin; climb-rate agility depends strongly on
motor torque margin. Verification a design would need: thrust and torque margins at the actual weight. No numeric margin adopted.
Overlap noted: the torque-margin point connects to Q-02 (motor ↔ load, DR-1 Option C split).

### Q-18 — PV rating conditions — PARTIAL QUALIFIED-CANDIDATE
DOE FEMP (SRC-026): module ratings are measured at standard test conditions (1,000 W/m², 25 °C cell temperature); real sunlight is usually lower
and cells hotter. **Not yet sourced on clean rights:** the explicit statement that output falls as cell temperature rises (temperature
coefficient) — the documents stating it are NREL / Sandia (contractor-operated laboratories).

### Q-19 — Vacuum outgassing screening — QUALIFIED-CANDIDATE
NASA PT-TE-1410 (SRC-027): ASTM E-595 screening [standard-defined conditions and pass values redacted 2026-10-29 — IP-UNRESOLVED, do not reuse]; approval against those values unless the application
dictates otherwise; product-by-product qualification, lot testing when variation is suspected. These are NASA's screening criteria, recorded
as source facts, not InventorAI thresholds.

## Run 10 (2026-10-28, scheduled wake-up)

### Q-20 — Double-acting cylinder forces — PARTIAL
DOE-HDBK-1018/2-93 ME-05 (SRC-028): Pascal's law; pressure applied on either side of the piston moves the load either way; force goes through
the piston rod; a relief valve guards against overpressure. F = P × A is already delivered (mechanical:PR006–PR011). **Not found on a clean-rights
source:** that the rod reduces the effective area on the retract side (so retract force is lower at equal pressure), and that piston speed equals
flow ÷ effective area → UNVERIFIED. DOE contractor caveat applies.

### Q-21 — Inverse-square irradiance — QUALIFIED-CANDIDATE (conditions)
NIST SP 250-95 (SRC-030): the measurement distance must exceed a minimum at which deviation from the inverse square law is negligible; for large
lamps the law does not hold well at close distances. This sources the far-field / small-source condition. The law's statement itself is used in
that document as the working relation; no minimum distance value is adopted.

### Q-22 — Thermal expansion and mismatch — QUALIFIED-CANDIDATE
NBS Circular 486 (SRC-031): materials change dimensions with temperature; the change depends on original length and temperature range; average
and instantaneous linear-expansion coefficients are defined; differential expansion of two materials is used in thermostats. NASA TP-2226
(SRC-032): differential expansion between dissimilar joined materials produces thermal stress. DOE-HDBK-1017/1-93 (SRC-029) supports.
Verification a design would need: the actual materials' coefficients over the actual temperature range and the joint's constraint. No data adopted.

## Run 11 (2026-10-28, scheduled wake-up; first run under the 2026-10-28 selection correction)

### Q-13 — Free-space path loss conditions — QUALIFIED-CANDIDATE (residual closed)
NBS TN 12 (SRC-037): an isotropic source's power density is p / 4πd² provided d ≫ λ, and free-space energy density falls with the square of distance.
NBS TN 101 Vol. 2 (SRC-038): far-field condition r > 2D²/λ (general rule); loss minimized with oriented beams and matched polarization; free-space
loss assumes loss-free, matched antennas. With SRC-020 (field losses exceed theory). Dimensions: D1, D2, D3 established; D5 not sought. FCC hosts refused.

### Q-24 — IoT device cybersecurity baseline — QUALIFIED-CANDIDATE
NIST blog (SRC-034, NIST staff): six capabilities — device identification, device configuration, data protection, logical access to interfaces,
software update, cybersecurity state awareness. NIST FAQ (SRC-035): a generic starting point tailored to market / product needs (applicability).
NISTIR 8259A (SRC-033) adds detail but is mixed-authorship → cross-check only. Dimensions: D1, D3, D4 (asset / vulnerability management links),
D7 established. Not a compliance statement; Stage 31 stays not authorized; H-04 untouched.

### Q-25 — Firmware update integrity and recovery — QUALIFIED-CANDIDATE
NIST SP 800-193 (SRC-036): protect / detect / recover; authenticated updates through a root of trust; recoverable even after power loss during
an update; preventing updates to an earlier vulnerable version; recovery to an authentic firmware version; critical data to factory defaults or last
known good; watchdog timers as an additional detection aid (also relevant later to Q-34); stated as broadly applicable to IoT and embedded devices.
Dimensions: D1, D3, D5 (corruption detection), D7 established. Rollback nuance recorded in the unresolved-issues log.

## Run 12 (2026-10-28, scheduled wake-up)

### Q-26 — IoT power and failure modes — PARTIAL
Clean-rights restatement found for most of the claim: NIST TN 1604 (SRC-039) — sleep mode, short transmissions and less data extend battery
life; lifetime depends on acquisition / transmission frequency, transmit power and network design; battery nodes need an estimate of overall energy
consumption over time to set battery-change intervals; a reliable network tolerates the failure of a node or link. With SRC-022's caveat (equal
average currents need not give equal lifetimes). **Residual:** the explicit time-weighted average of active and sleep currents, and a source
statement that device behaviour on power or connectivity loss must be defined — both UNVERIFIED. Dimensions: D1 partial, D2, D3, D7.

### Q-28 — Real radio channels — QUALIFIED-CANDIDATE
NIST TN 1604 (SRC-039): open-field ranges are optimistic; walls, floors and furnishings attenuate (metal blocks); layout changes alter coverage;
devices sharing unlicensed ISM bands can interfere. NISTIR 8243 (SRC-040): reflection, absorption and interference limit range, reliability and
timeliness; free-space path-loss exponent 2, higher when occluded; multipath fading modeled as Rician / Rayleigh. NBS TN 101 (SRC-038) on
multipath coupling loss. SRC-041 cross-check only. Dimensions: D1, D3, D5 (measure in the real environment) established. No link-budget values.

### Q-30 — Battery limits and BMS functions — QUALIFIED-CANDIDATE
Re-read of NASA/TM-2009-215751 (SRC-009, no new fetch): abuse conditions (overcharge, overdischarge, shorts, high temperature beyond the
manufacturer's limit, structural damage); cell-level voltage / mid-string monitoring and control against string imbalance; protection against
overcharge, overdischarge, over-current and over-temperature with at least two levels of safety; abuse tests. **UNVERIFIED:** state-of-charge
*estimation* as a BMS function (only the SOC definition is stated). Dimensions: D1, D2, D3, D5, D7. Lead noted for Q-31 (storage / cycling
effects on capacity), not worked this run.

## Run 13 (2026-10-28, scheduled wake-up)

### Q-26 — IoT power and failure modes — PARTIAL (residual narrowed)
NASA MSFC EPS slides (SRC-043): average power from the equipment list and peak power from the profile; power with margin for average and peak loads;
energy drained = load × time; health / status monitoring and protection against bus and load faults. **Still UNVERIFIED on a clean source:** the
explicit time-weighted average of active and sleep current (SRC-022 implies it but is IP UNRESOLVED), and a statement that device behaviour on
power or connectivity loss must be defined. Two residual searches spent; next attempt, if none succeeds, marks it EXHAUSTED.

### Q-31 — Battery ageing — QUALIFIED-CANDIDATE (no new search)
Re-read SRC-009 / SRC-008: storage state of charge and temperature drive irreversible capacity loss; cycling temperature and depth of discharge
affect deliverable capacity over life; voltage falls faster with longer cycle life; manufacturers add capacity margin for expected life losses;
real-time and accelerated life tests evaluate degradation; discharge rate and temperature strongly affect capacity and life (lead-acid source).
Dimensions: D1, D3, D5, D7. Not adopted: the storage-loss example figures.

### Q-11 — PWM average voltage — QUALIFIED-CANDIDATE (residual closed)
NASA TN D-5643 (SRC-042): a periodic voltage equal to E for Δt and zero otherwise has an average proportional to the duty cycle Δt/T; filtered
output is proportional to input voltage × duty cycle; filtering removes ripple; output impedance limits load independence. With SRC-018 (switching
period much shorter than the winding's electrical time constant; free-wheeling path keeps current continuous). Dimensions: D1, D2, D3.

## Run 14 (2026-10-28, early run on the Owner's direction relayed by the Lead session; residual-only)

### Q-26 — residual — EXHAUSTED
Third residual search: candidates state duty cycles or on/off ratios but not the explicit time-weighted average of active and sleep current, and no
clean source states that device behaviour on power / connectivity loss must be defined. Both residual points stay **UNVERIFIED**; the points
established in runs 12–13 (SRC-039, SRC-043) stand. Use: calc (average current) remains unsupported; cond / verif points stand. No further work.

### Q-20 — residual — PARTIAL — WAITING (access)
A clean federal candidate exists — USACE EM 1110-2-2610 (2025) states the reduced working area on the rod side and the smaller rod-end volume —
but its host is refused by proxy policy; the DTIC handbook (Flow = Velocity × Area) is refused too. NASA NTRS alternatives are contractor or mixed
authorship. Rod-side area and speed = flow ÷ area stay **UNVERIFIED**. Reopens on host access or a Lead-supplied inspection of EM 1110-2-2610.

### Q-12 — residual — IP UNRESOLVED (terminal for the residual)
The explicit two-link formula appears in two NTRS documents, both outside the rights screen (university paper with possible copyright; RIACS
contractor report). The general principle (SRC-019) stands; the explicit formula stays **UNVERIFIED** on a clean source. No further work.

## Run 15 (2026-10-28, early run on Owner direction; GitHub-first)

### Q-18 — PV output falls with cell temperature — PARTIAL → QUALIFIED-CANDIDATE
Repository reuse: SRC-026 (D1 / D2: standard test conditions, field conditions differ) and SRC-043 slides 28 / 41 (array power vs temperature
plotted; temperature factor in array sizing — IMPLIED only). Base-branch domains / method artifacts hold no PV material. Residual searched: an
explicit clean-rights statement of the temperature effect (1 query). New: SRC-044 (NASA Glenn, sole author). D1 EXPLICIT (κ = dη/dT generally
negative; P = (η₃₀₀ₖ + κΔT)·I by linear extrapolation); D2 EXPLICIT (first-level analysis; κ varies slightly with intensity and temperature);
D3 (η, κ, T in K, intensity I); D6 EXPLICIT (κ nonlinear in general; Voc term dominant). D5 / D4 / D7 not sought. Use: cond, calc (first-level).

### Q-23 — Spring–mass natural frequency and resonance — QUEUED → QUALIFIED-CANDIDATE
Repository reuse: none (no vibration / resonance material in this package or the base-branch domains, method artifacts or engine). Residual
searched: the whole claim (1 query). New: SRC-045 (NBS SP 615). D1 EXPLICIT (equation of motion; ω₀ = √(k/m), verified on the page image);
D2 EXPLICIT (SDOF assumption must be checked — multi-DOF and mounting stiffness); D3 (k, m, c, ω₀ in rad/s, damping ratio); D5 EXPLICIT
(natural frequency measured as the 90° phase point; resonant frequency as the maximum-amplitude point); D6 EXPLICIT (resonance amplitude governed
by damping; flat-response limits depend on damping). Context: stated for sensor dynamics. Use: calc, cond, verif.

### Q-29 — Shannon–Hartley capacity bound — QUEUED → QUALIFIED-CANDIDATE
Repository reuse: none relevant (SRC-037 / SRC-038 cover propagation, not capacity). Residual searched: the whole claim (1 query). New: SRC-046
(NASA/TM—2018-219754). D1 EXPLICIT (C = B log₂(1 + P / (N₀B)), verified on the page image); D2 EXPLICIT (AWGN, bandwidth-limited channel,
average power constraint; R ≤ C achievable with arbitrarily small error); D3 (P, N₀, B; bits / s); D6 EXPLICIT (fading, channel side information
and interference change or leave open the capacity). D7: a theoretical bound only, no design criterion. Use: calc (upper bound), cond.

## IP-hygiene audit (2026-10-29; no research run)
Scientific findings above are unchanged. Product-use IP fitness per source is in `evidence/ip-and-reuse-register.md` (claim-level audit) and per
question in `state/question-register.md` and `owner-readable-summary.md`. Standard-derived values (SRC-027 ASTM E595 conditions and pass values;
SRC-045 flat-response band figures) were redacted from the active library; the Wood Handbook footnote (SRC-014) is paraphrased, not quoted.

## Run 16 (2026-10-29, scheduled wake-up; restoration backlog, GitHub-first)

### R-02 (Q-23) — PARTIALLY RESTORED
Repository reuse: base-branch PR #900 (MECHANICAL-NATURAL-FREQUENCY-01, merged after the IP audit) relies on NBS TN 487 and NIST SP 330, LEAD-SUPPLIED
there; zero external queries here. Old source SRC-045 (ANSI B88.1-based) stays IP-UNRESOLVED. New: SRC-047 (NBS TN 487), DIRECTLY INSPECTED,
own analysis, U.S. Government work, CALCULATION-GRADE, independent (no standard cited). Restored: D1 EXPLICIT (√(k/m) undamped natural frequency of
a single mass on a spring to a large mass), D5 EXPLICIT (resonance = lowest drive frequency of maximum relative motion), D6 EXPLICIT (coupled-mass
models depart from the single-mass value by mass-ratio-dependent amounts). **Not restored:** damping governing the resonance amplitude (TN 487 is
undamped) — stays IP-UNRESOLVED. Material for the Execution Lead: the LEAD-SUPPLIED TN 487 basis of PR #900 is now directly inspected here.

### R-01 (Q-02) — IP-UNRESOLVED (bounded search done)
Old sources SRC-004 (author employee status unconfirmed) and SRC-005 (DOE series) unchanged. Families searched: NASA NTRS, NASA technical standards,
DOE, NIST (2 queries). Candidates failed: NASA-STD-5017B (SRC-048; torque-margin section aligned with AIAA S-114A-2020, motor section adapted from a
third-party book), a contractor stepper-motor report, DOE / JPL / university items. Fastest route to restoration: a recorded confirmation that the
SRC-004 author was a U.S. Army employee (which would clear SRC-004 itself) — an Owner / Lead item, not a search.

### R-03 (Q-04) — IP-UNRESOLVED (bounded search done)
Old source SRC-006 (ASTM C393) unchanged. Families searched: USDA FPL / Treesearch, NIST, NASA (1 query). Every FPL test report found measures
deflection relative to the supports as part of ASTM D 198 testing, so none is independent of the standard; the one reachable non-standard statement
(SRC-049) is a proceedings paper with unclear rights and only implies the principle; FPL RP-264 host refused.
