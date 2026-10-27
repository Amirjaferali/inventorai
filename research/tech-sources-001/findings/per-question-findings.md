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
