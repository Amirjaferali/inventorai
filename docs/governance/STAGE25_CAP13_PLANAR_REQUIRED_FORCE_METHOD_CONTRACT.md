# STAGE 25 / CAP-13 — PLANAR REQUIRED FORCE METHOD CONTRACT

STATUS: OWNER-AUTHORIZED BOUNDED METHOD CONTRACT — written with, and governing, the one bounded implementation increment
`CAP13-PLANAR-REQUIRED-FORCE-01`, which the Owner authorized as ONE implementation increment (code, the narrow shared-owner
amendment, focused verification and one pull request). Applicability: this contract governs the delivered method only on
the verified merge of that pull request into `feature/atomic-json-session-persistence`; on its proposal branch it describes
an Owner-authorized proposed method, not a merged or delivered capability. Merge, deployment, production activation and any
broader capability admission are NOT authorized by it.
AUTHORITY LEVEL: subordinate to the CAP-13 entry of the
[Capability Enrichment Register](INVENTORAI_CAPABILITY_ENRICHMENT_REGISTER.md) and to the accepted
[shared deterministic calculation and units owner boundary contract](SHARED_DETERMINISTIC_CALCULATION_AND_UNITS_OWNER_BOUNDARY_CONTRACT.md)
(the "calc/units contract", with its Correction 09, §13H, added by the same increment). It amends neither the Register nor
the accepted [planar single-force moment method contract](STAGE25_CAP13_PLANAR_SINGLE_FORCE_MOMENT_METHOD_CONTRACT.md), whose
method, artifact and behaviour stay unchanged; it reuses that method's scientific evidence (§11) by restating it in its own
records, never by loading its artifact. Where this document and the calc/units contract differ, the calc/units contract
wins and the difference is a defect of this document.

---

## 0. Preserved truth (binding)

- `ACTIVE CONTRACT: NONE` describes the state before and after this increment; this contract fills no active-contract slot
  after delivery and is not a delivery record.
- Stage 25 stays ENTERED / PARTIAL and its checkbox stays UNTICKED; this method enters, completes or reopens no Stage and
  changes no roadmap count. `FULL CAP-13: NOT AUTHORIZED`. D-7 stays OPEN and the bounded stiffness method stays NOT ADMITTED.
- The eight admitted methods keep their identities, artifacts, semantic pins, units and behaviour.
- Preliminary motion requirements stay BLOCKED and Motion is NOT activated: this method sizes nothing, selects no actuator
  and supplies no motion requirement.
- The Stage 15 integrated-part exception (`engine/subsystem_model.py`) names its calculations; it is extended to this method
  by name only, for the declared Mechanical part (§1).

## 1. Purpose and scope

ONE optional, advisory, non-binding, request-local calculation: the MAGNITUDE of the ONE force that, acting at a
perpendicular distance the inventor states from ONE point the inventor chooses, in ONE plane, would produce a target moment
(turning effect) the inventor states about that point. It helps a nontechnical inventor who already has a turning effect in
mind — for example the turning effect they want a handle, lever or arm to produce about its pivot — express it as one force
figure to discuss with an engineer, without inferring anything else.

Eligibility: a project whose trusted durable root domain (`confirmed_domain`, read as the CAP-12 gate reads it) is exactly
`mechanical`; or, whatever the initial analysis focus, the ONE inventor-declared Mechanical part of a valid durable Stage-15
integrated composition, read only through the store-validated composition (`_calc_gate` / `_calc_declared_part`, the rule
the other CAP-13 calculations use) and never from the request. On an integrated project the page names that part with the
existing CAP-13 attribution wording. A declared part makes the calculation OFFERED only: it establishes no applicability,
suitability, validation or safety, and supplies no moment, distance, declaration or screen answer. A missing, malformed,
corrupt or unreadable composition grants nothing beyond the root rule, and an unreadable root domain offers nothing (fail
closed). The session link, the page and the submission read the same one decision.

## 2. Method identity and version

Identity `cap13:planar_required_force`, version `1.0`. Method-authority artifact
`docs/governance/cap13_content_config/planar_required_force_v1.json` (`cap13_planar_required_force`, artifact version `1`),
separate from every other artifact; it loads none and is loaded by none. Adapter
`engine/cap13_planar_required_force_method.evaluate`; consumer `engine/cap13_planar_required_force.py`.

## 3. Method definition and derivation

`F = M_target / d⊥`. The moment of a force about a point is the force multiplied by the perpendicular distance from the
point to the force's line of action (NASA-S1, NASA-T1; §11): `M = F × d⊥`. For a strictly positive `d⊥` this is solved
exactly for the force. With `M_target` in N·mm and `d⊥` in mm the quotient is directly in N; no conversion factor is applied.
The rearranged form, the magnitude form, the planar restriction and the declarations are InventorAI's own bounded
restatement; NASA does not publish this method. One division is executed; there is no subtraction, sign convention,
resultant, allowance, margin, clamping or magnitude ceiling.

## 4. Roles, quantity kinds and exact unit tokens

| Role | Meaning | Quantity kind | Exact unit token |
|---|---|---|---|
| `M_target` | magnitude of the target moment the inventor wants the one force to produce about the chosen point | `moment` | `N·mm` |
| `d_perp` (`d⊥`) | perpendicular distance from the chosen point to the line along which the force will act | `length` | `mm` |
| `F` | magnitude of the one force that would produce that moment at that distance | `force` | `N` |

The units are fixed and shown, never chosen. Nothing is converted to N·m, m or any other unit. `M_target` and `d_perp` are
ASCII role identifiers, never aliases. The three kinds and tokens are already admitted (calc/units §13B); none is added.

## 5. Applicability declarations

Each is shown as its own statement and answered «applies» or «does not apply», none pre-selected. A missing answer is
`NOT_DECLARED`; «does not apply» is `MODEL_NOT_SUPPORTED`. InventorAI infers none of them.

| Ref | Id | Accepted statement |
|---|---|---|
| D-1 | `planar` | planar: the force and the chosen point lie in one plane, and only the turning effect about the axis through the point at right angles to that plane is wanted |
| D-2 | `single_force` | ONE force only is to produce the target moment: no other force, couple, spread-out load or weight is included in this calculation |
| D-3 | `perpendicular_distance` | the distance d_perp is the shortest (perpendicular) distance from the chosen point to the line along which the force will act, not a length along a lever, arm or part unless that length is itself at right angles to the force; InventorAI does not check it |
| D-4 | `chosen_point` | the point is the inventor's own choice (for example a pivot, joint or fixing); InventorAI does not choose it, check it or decide that it is the right point |
| D-5 | `target_moment` | the target moment M_target is your own figure for the turning effect you want this one force to produce; InventorAI does not work it out, check it or decide that it is enough, and it adds nothing for friction, losses, starting or holding, or any margin |
| D-6 | `static_magnitude` | the force is treated as steady (static), and only its size is wanted, not its direction or the turning direction; no motion, acceleration, impact, vibration or repeated loading is considered |

## 6. Numeric domain and numerical acceptance

- **Grammar (strict capture).** Strict unsigned ASCII decimal: one to twelve integer digits for `M_target` or one to nine for
  `d⊥`, and an optional single fractional part of one to nine digits. No sign, exponent, separator, space, Unicode digit,
  unit suffix, `inf`, `nan` or normalization. A field sent twice, an unknown field or a declaration / screen answer outside
  its closed choices makes the whole request malformed (a bare 400). An omitted, malformed or over-length value is
  `INVALID_NUMERIC_INPUT`.
- **Representation limits are not physical limits.** The digit limits bound what can be typed: `M_target` from `0` to below
  `10^12` N·mm; `d⊥` below `10^9` mm; steps of `10^-9`. They are NOT physical limits, ratings or a claim that such values
  are realistic. The 64-character field cap is abuse protection only — a NON-PHYSICAL bound.
- **Positive distance.** The EXACT decimal value of `d⊥` must be greater than zero, decided before any binary rounding; a
  zero distance (`0`, `0.000`, …) is `DISTANCE_NOT_POSITIVE` with no number — a force whose line of action passes through the
  point produces no moment about it, so no force produces a nonzero target there. A zero target moment is admitted and gives
  exactly `0` N; that is a value, not an underflow and not a refusal.
- **Binary bridge.** Each admitted decimal is converted ONCE to the correctly rounded binary64 value (round half to even) and
  handed to the owner as a typed number; the owner parses no string (calc/units §10). Every admitted nonzero value lies
  between `10^-9` and `10^12` in magnitude, so it is a normal binary64 number with relative rounding error at most `2^-53`; a
  positive `d⊥` stays positive and a zero `M_target` stays exactly zero.
- **Owner applicability.** The method record declares the existing `greater_than_zero` on `d_perp`; a non-positive value
  that reaches the owner is `UNABLE_TO_DETERMINE / INPUT_OUTSIDE_ADMITTED_RANGE`, shown as the neutral
  `UNMAPPED_OWNER_OUTCOME` (unreachable from the page). No condition is declared on `M_target` (zero is admitted) and no
  result range is declared (a zero force is admitted).
- **Binary acceptance (adapter).** The exact rational value `M_target / d_perp` of the binary inputs is rounded ONCE to
  binary64. A zero target moment gives exactly `0.0`. A nonzero exact result is accepted only when the rounded value is
  finite, strictly positive and `|F − exact| ≤ 2^-52 · exact`. Overflow, underflow of a nonzero result to zero, a subnormal
  result outside that bound, a negative or non-finite input, or any failed check is `FAILURE /
  EXECUTION_INTEGRITY_FAILURE` with no numerical payload, displayed as `KNOWLEDGE_UNAVAILABLE`, never rewritten as a
  refusal. Exact zero (a zero target moment) and nonzero underflow are therefore distinct: the first is `0.0` exactly, the
  second is a failure. Representability: inside the representation limits every nonzero result lies between `10^-18` and
  `10^21` N, well inside the normal binary64 range, so neither overflow nor underflow can occur from the page; the guards
  stay in place for direct owner use and are proven at adapter and owner level.
- **Decimal-reference acceptance (consumer).** A successful owner result is shown only when it agrees with the exact decimal
  quotient `M_target / d⊥` of the ENTERED decimals: exactly zero when, and only when, `M_target` is exactly zero; otherwise
  strictly positive and within a relative error of `2^-51`. Proof that the bound always holds: with `u = 2^-53`, each binary
  input carries a relative error of at most `u`, so the exact quotient of the binary inputs lies within `(1+u)/(1−u) − 1` of
  the decimal quotient, and the single rounding adds at most `u`; the total is at most `(1+u)²/(1−u) − 1 < 3.0000001 · u <
  2^-51`. A failed check is `KNOWLEDGE_UNAVAILABLE` with no number.
- **Display.** The shown value is derived from the exact decimal quotient, never from the binary value: rounded ONCE to 12
  significant digits, round half to even, with trailing zeros removed. It is labelled **exact** when that rounding changes
  nothing and **rounded to 12 significant digits** otherwise, so exactness is never silently asserted (`5000 / 250` shows
  `20`, exact; `1000 / 3` shows `333.333333333`, rounded; `10 / 7` shows `1.42857142857`, rounded). Plain decimal notation is
  used for `10^-6 ≤ F < 10^12` N and the form `m × 10^e` otherwise, so a tiny nonzero force is never shown as `0`
  (`0.000000001 N·mm` at `999999999.999999999 mm` shows `1 × 10^-18`, rounded). A zero target moment shows `0`, exact, with
  a note that no force is needed for no turning effect, which says nothing about holding anything in place. The digits shown
  imply no measurement resolution, precision or accuracy.
- These rules belong to this method only; none is a generic owner numerical policy.

## 7. Refusal and abstention semantics

Order after request integrity (CSRF), project authorization, eligibility and strict capture (a malformed request is a bare
400 with no reason token): (1) completeness — every declaration and screen item answered, else `NOT_DECLARED`; (2) screen —
any YES is `ENGINEERING_REVIEW_REQUIRED` and the owner is not invoked; (3) declarations — any «does not apply» is
`MODEL_NOT_SUPPORTED`; (4) numeric grammar — `INVALID_NUMERIC_INPUT`; (5) positive distance — `DISTANCE_NOT_POSITIVE`; (6) the
shared owner; (7) the decimal-reference acceptance — `KNOWLEDGE_UNAVAILABLE`. A method artifact that is missing, unreadable
or changed is `KNOWLEDGE_UNAVAILABLE` before any of these. The first failing stage alone decides; no refusal carries a
number. Owner correspondence: `REFUSAL / INVALID_NUMERIC_INPUT` → `INVALID_NUMERIC_INPUT`; `REFUSAL / UNIT_NOT_ADMITTED` or
`UNKNOWN_UNIT` → `UNIT_NOT_SUPPORTED`; `REFUSAL / METHOD_NOT_REGISTERED` or `VERSION_MISMATCH`, `UNABLE / SOURCE_UNAVAILABLE`
and `FAILURE / EXECUTION_INTEGRITY_FAILURE` → `KNOWLEDGE_UNAVAILABLE`; any other owner state → the neutral
`UNMAPPED_OWNER_OUTCOME`. The owner state and token are preserved, never rewritten.

## 8. High-risk screen (declared; not a safety engine)

The same nine items as the other CAP-13 screens, in the same order and with the same copy: supports people; overhead or
falling hazard; use by or for children; safety-critical load path; pressure; high temperature; battery containment; medical
use; food contact. All NO answers only allow this bounded calculation to proceed and never mean safe. The screen neither
reads nor feeds SafetySignal.

## 9. Result, provenance and fixed disclosure

On success the page shows `F` in N as described in §6, labelled `UNVALIDATED` and `NOT EVIDENCE`, with its exact / rounded
label, the method identity and version, the method sources and unit records the owner carried, the inputs echoed and this
fixed disclosure (English; pinned equal to the artifact):

1. This is the size of the one steady force that, acting at your perpendicular distance d⊥ from the one point you chose, in one plane, would produce your own target moment M_target about that point: F = M_target / d⊥.
2. It does not work out, check or justify your target moment, and it adds nothing for friction, losses, starting or holding, efficiency or any margin.
3. It does not tell whether a person, motor, actuator, spring or mechanism can apply this force, or whether a joint, fixing, shaft, part or material can carry it, and it is not compared with any rating, strength or limit.
4. It is preliminary, advisory, UNVALIDATED and not evidence, and it must be confirmed by measurement or a qualified engineer before any reliance; it says nothing about whether the design is suitable or safe.
5. InventorAI does not check your target moment, your distance, your chosen point or that your declarations match the real configuration.
6. Three-dimensional effects, several forces, motion, impact, vibration and repeated loading are outside this calculation.
7. Reference source material: NASA Glenn Research Center (equilibrium and torque / moment principles); the rearranged form F = M / d⊥ is InventorAI's own restatement.

## 9A. Arabic disclosure and UX wording

**A-1 Fixed disclosure (Arabic rendering of the seven §9 items, item by item; no meaning added, removed or softened).**

> 1. هذا هو مقدار القوة الثابتة الواحدة التي، إذا أثّرت على المسافة العمودية d⊥ التي أدخلتها من النقطة الواحدة التي اخترتها، في مستوى واحد، أحدثت العزم المستهدف M_target الذي أدخلته أنت حول تلك النقطة: F = M_target / d⊥.
> 2. لا يحسب هذا الناتج العزم المستهدف الذي أدخلته ولا يتحقق منه ولا يبرّره، ولا يضيف شيئًا للاحتكاك أو الفقد أو بدء الحركة أو التثبيت أو الكفاءة أو أي هامش.
> 3. لا يبيّن هذا الناتج ما إذا كان شخص أو محرك أو مُشغِّل (actuator) أو نابض أو آلية قادرًا على تطبيق هذه القوة، ولا ما إذا كان أي مفصل أو تثبيت أو عمود أو جزء أو مادة قادرًا على تحمّلها، ولا يُقارَن بأي تصنيف أو مقاومة أو حدّ.
> 4. هذه النتيجة أولية وإرشادية، وغير مُتحقَّق منها (UNVALIDATED)، وليست دليلًا، ويجب تأكيدها بالقياس أو بمراجعة مهندس مؤهل قبل الاعتماد عليها؛ ولا تقول شيئًا عن ملاءمة التصميم أو سلامته.
> 5. لا يتحقق InventorAI من العزم المستهدف ولا من المسافة ولا من النقطة التي اخترتها، ولا من مطابقة تصريحاتك للتكوين الفعلي.
> 6. التأثيرات ثلاثية الأبعاد، وتعدد القوى، والحركة، والصدمات، والاهتزاز، والتحميل المتكرر كلها خارج نطاق هذا الحساب.
> 7. المراجع: مركز غلين للأبحاث التابع لوكالة ناسا (NASA Glenn Research Center) — مبادئ الاتزان والعزم. أما الصيغة المُعاد ترتيبها F = M / d⊥ فهي إعادة صياغة خاصة بـInventorAI.

**A-2 Applicability declarations (§5).** The inventor answers «ينطبق على حالتي» or «لا ينطبق على حالتي», none pre-selected.

| §5 | Arabic statement |
|---|---|
| D-1 planar | مستوى واحد: القوة والنقطة التي اخترتها تقعان في مستوى واحد، والمطلوب فقط أثر الدوران حول المحور المارّ بالنقطة عموديًا على ذلك المستوى. |
| D-2 single_force | قوة واحدة فقط هي التي ستُحدث العزم المستهدف: لا تدخل في هذا الحساب أي قوة أخرى، ولا ازدواج (couple)، ولا حمل موزَّع، ولا وزن. |
| D-3 perpendicular_distance | d⊥ هي أقصر مسافة (المسافة العمودية) من النقطة المختارة إلى الخط الذي ستؤثر على امتداده القوة، وليست طولًا على امتداد ذراع أو رافعة أو جزء ما لم يكن ذلك الطول نفسه عموديًا على القوة؛ ولا يتحقق InventorAI منها. |
| D-4 chosen_point | النقطة من اختيارك أنت (مثل محور دوران أو مفصل أو نقطة تثبيت)؛ لا يختارها InventorAI ولا يتحقق منها ولا يقرر أنها النقطة الصحيحة. |
| D-5 target_moment | العزم المستهدف M_target قيمتك أنت لأثر الدوران الذي تريد أن تُحدثه هذه القوة الواحدة؛ لا يحسبه InventorAI ولا يتحقق منه ولا يقرر أنه كافٍ، ولا يضيف إليه شيئًا للاحتكاك أو الفقد أو بدء الحركة أو التثبيت أو أي هامش. |
| D-6 static_magnitude | القوة تُعامَل على أنها ثابتة (ساكنة)، والمطلوب مقدارها فقط لا اتجاهها ولا اتجاه الدوران؛ ولا تؤخذ في الحسبان أي حركة أو تسارع أو صدمة أو اهتزاز أو تحميل متكرر. |

**A-3 Screen (§8).** The Arabic screen stem, items, answers and note are the existing two-support screen copy
(`UI_CAP13_SCREEN_*`), reused unchanged.

**A-4 Right-to-left rendering.** Numbers, the role symbols `F`, `M_target` and `d⊥`, the unit tokens `N`, `mm` and `N·mm`,
the expression `F = M_target / d⊥`, the method identity and `UNVALIDATED` / `NOT EVIDENCE` are each direction-isolated
(`<bdi dir="ltr">`) on the Arabic page; the inventor's typed values are shown left-to-right.

## 10. Exclusions (binding)

No working out, estimate, check or justification of the target moment; no friction, losses, efficiency, starting, holding,
breakaway, dynamic or safety allowance and no margin; no static equilibrium, moment balance, resultant, support reaction or
sign / turning-direction convention; no actuator, motor, spring, mechanism or human-effort capability, selection or sizing;
no joint, fastener, shaft, bearing, weld or member capacity, strength, stress, deflection, fatigue or failure check; no force
or torque rating; no thickness, material or specification; no design suitability, stability or safety conclusion; no
three-dimensional moment, several forces, couples, spread-out loads, motion, acceleration, impact, vibration or repeated
loading; no inference of any moment, distance, point, geometry or declaration; no unit conversion; no transfer of a result
from or to the planar-moment method or any other calculation; no persistence, report, PDF, Structured Export, API, evidence,
readiness, progression, gap or SafetySignal effect; no Motion activation; no AI or provider call; no eligibility for any part
other than the one declared Mechanical part (§1), and no inference from a part's name or function.

## 11. Source and source-use status

The scientific evidence is the planar-moment method's, reused without widening its claim: the one relation `M = F × d⊥`,
rearranged here by exact algebra for a strictly positive `d⊥`.

- **NASA-S1** — NASA Glenn Research Center, Beginners Guide to Aeronautics, *Equilibrium*
  (<https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/equilibrium/>). Supports, for this method, only: torque /
  moment is force multiplied by perpendicular distance. Reuses the Lead-supplied inspection of 2026-10-07 already recorded
  for the two-support and planar-moment methods; those records' scopes are not changed.
- **NASA-T1** — NASA Glenn Research Center, Beginners Guide to Aeronautics, *Torque (Moment)*
  (<https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/torque-moment/>). Supports only the same relation (textual
  statement). Reuses the Lead-level inspection of 2026-09-28 recorded as `mechanical:PR006`.
- **Units** — NIST SP 811: N (Chapter 4, Table 3) and mm (Tables 1 and 5) as already recorded by `dcu:U001` / `dcu:U002`;
  N·m as the SI unit of moment of force (Appendix B.9, recorded as `mechanical:PR009`). N·mm is InventorAI's own formation
  from these facts (`dcu:U006`); a value in N·mm divided by a value in mm is directly in N.
- **Source use** (not legal opinions): NASA STI terms (`cap13f:SU001`; owner snapshot `dcu:SU016`) and NIST Technical Series
  terms (`cap13f:SU002`; the existing owner unit records keep their own source-use records). Use is factual paraphrase and
  unit identification only; no NASA or NIST prose, image, table, figure, branding or conversion factor is reproduced. All
  inspections are Lead-supplied and not independently re-inspected by the executor; no new source is introduced, and the
  existing records (`cap13:SU001`, `cap13m:SU001`, `cap13m:SU002`, `dcu:SU001` to `dcu:SU015`, `mechanical:PR006` to
  `PR011`) keep their own scopes.

## 12. Implementation boundary

The one existing shared owner executes the method through ONE additional immutable binding created by application wiring
(`_CAP13_REQUIRED_FORCE_BINDING` in `web/app.py`), beside the eight existing bindings; there is no registry, discovery,
dynamic module path or request-selected method (calc/units contract §13H). Routes: `GET` / `POST
/session/<sid>/planar-required-force`, behind the central project authorization and the global CSRF guard; the session page
shows one optional link on an eligible project. Eligibility reuses `_calc_gate(sid, consumer)` (§1). Nothing is persisted;
the POST renders its result directly.

## 13. Verification

Focused tests (`tests/test_cap13_planar_required_force.py`, `tests/test_cap13_planar_required_force_browser.py`): exact and
nonterminating quotients; zero target moment (exactly `0`, distinct from underflow); zero and invalid distance; tiny, large
and representation-limit values; an independent exact-rational oracle over a sample; adapter overflow, nonzero underflow,
subnormal and invalid input; grammar; unit, method, version, adapter and artifact integrity, with no number on any refusal;
owner artifact v9; the §7 order and owner correspondence; Mechanical-root and integrated Mechanical-part eligibility and the
refusal elsewhere; CSRF, authorization, request isolation and no persistence; the eight existing methods unchanged; EN / AR
fidelity; and real-browser EN / AR journeys. Hosted required CI is the merge gate.

## 14. STOP conditions

Stop and return to the Owner on a source or IP deficiency, a contract incompatibility, unprovable numerical integrity, an
unqualified actuation, capability or safety claim, or any scope expansion (another method, consumer, unit, conversion,
allowance, motion requirement, eligibility beyond §1, persistence, result transfer or report surface).
