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
