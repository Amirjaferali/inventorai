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
