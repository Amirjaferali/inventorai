# STAGE 25 / CAP-13 — PLANAR SINGLE-FORCE MOMENT METHOD CONTRACT

STATUS: OWNER-AUTHORIZED BOUNDED METHOD CONTRACT — written with, and governing, the one bounded implementation increment
`CAP-13 PLANAR SINGLE-FORCE MOMENT — SLICE 1`, which the Owner authorized as ONE bounded Wave-3 implementation increment
(code, existing-contract amendments, focused verification and one pull request). Applicability: this contract governs the
delivered method only on the verified merge of that pull request into `feature/atomic-json-session-persistence`; on its
proposal branch it describes an Owner-authorized proposed method, not a merged or delivered capability. Merge,
deployment, production activation and any broader capability admission are NOT authorized by it.
AUTHORITY LEVEL: subordinate to the CAP-13 entry of the
[Capability Enrichment Register](INVENTORAI_CAPABILITY_ENRICHMENT_REGISTER.md) and to the accepted
[shared deterministic calculation and units owner boundary contract](SHARED_DETERMINISTIC_CALCULATION_AND_UNITS_OWNER_BOUNDARY_CONTRACT.md)
(the "calc/units contract", with its Correction 03, §13B, added by the same increment). It amends neither the Register nor
the accepted [CAP-13 two-support static reactions method contract](STAGE25_CAP13_TWO_SUPPORT_STATIC_REACTIONS_METHOD_CONTRACT.md),
whose method, artifact and behaviour stay unchanged. Where this document and the calc/units contract differ, the calc/units
contract wins and the difference is a defect of this document.
INTEGRATED-PART ELIGIBILITY AMENDMENT: `CAP13-PLANAR-MOMENT-INTEGRATED-PART-01 — OWNER-AUTHORIZED AMENDMENT`. The Owner
authorized ONE bounded increment extending this method's eligibility to the declared Mechanical part of a valid durable
Stage-15 integrated composition, whatever the initial analysis focus, and the matching narrow extension of the Stage 15
exception recorded in `engine/subsystem_model.py`. Applicability: it takes effect only on the verified merge of that
increment's pull request into `feature/atomic-json-session-persistence`. It amends §0 (fourth bullet), §1 (eligibility),
§10 (last exclusion), §12 and §13 only; the superseded wording is preserved beside each change. The method, its version,
equation, roles, units, declarations, screen, numeric domain and numerical acceptance, §7 order, disclosure, sources, the
method-authority artifact and the shared owner are unchanged.

---

## 0. Preserved truth (binding)

- `ACTIVE CONTRACT: NONE` describes the state before and after this increment; this contract fills no active-contract slot
  after delivery and is not a delivery record. Current-truth delivery records belong to the post-merge closure sync.
- Stage 25 stays ENTERED / PARTIAL and its checkbox stays UNTICKED; this method enters, completes or reopens no Stage and
  changes no roadmap count. `FULL CAP-13: NOT AUTHORIZED`. D-7 stays OPEN and the bounded stiffness method stays NOT ADMITTED.
- The two-support static reactions method `cap13:static_reactions_two_support` 1.0 and the THERM-01 method
  `therm01:conduction_temperature_difference_single_path` 1.0 keep their identities, artifacts, semantic pins, units and
  behaviour.
- The Stage 15 integrated-part exception (`engine/subsystem_model.py`) names its calculations; it is extended to this
  method by name only, for the declared Mechanical part (§1, as amended). *(Superseded by the integrated-part eligibility
  amendment, preserved — was: "names its calculations and is NOT extended by this contract (§1).")*

## 1. Purpose and scope

ONE optional, advisory, non-binding, request-local calculation: the MAGNITUDE of the moment (turning effect) produced by
ONE force about ONE point the inventor chooses, in ONE plane. It helps a nontechnical inventor turn a stated force and a
stated perpendicular distance into one moment figure for a pivot, joint or fixing they already have in mind — for example
to describe to an engineer how hard a handle, lever or bracket is being turned — without inferring anything else.

Eligibility (as amended): a project whose trusted durable root domain (`confirmed_domain`, read as the CAP-12 gate reads
it) is exactly `mechanical`; or, whatever the initial analysis focus, the ONE inventor-declared Mechanical part of a valid
durable Stage-15 integrated composition, read only through the store-validated composition (`_calc_gate` /
`_calc_declared_part`, the rule the two-support reactions use) and never from the request. On an integrated project the
page names that part with the existing CAP-13 attribution wording. A declared part makes the calculation OFFERED only: it
establishes no applicability, suitability, validation or safety, and supplies no force, distance, declaration or screen
answer — the inventor still enters all of them. A missing, malformed, corrupt or unreadable composition grants nothing
beyond the root rule, and an unreadable root domain offers nothing (fail closed). The session link, the page and the
submission read the same one decision. *(Superseded by the integrated-part eligibility amendment, preserved — was: "Root
only: a declared Mechanical part outside an integrated project's initial analysis focus is NOT offered this method,
because extending the Stage 15 exception needs its own Owner authorization.")*

## 2. Method identity and version

Identity `cap13:planar_single_force_moment`, version `1.0`. Method-authority artifact
`docs/governance/cap13_content_config/planar_single_force_moment_v1.json` (`cap13_planar_single_force_moment`, artifact
version `1`), separate from the two-support artifact; neither loads the other. Adapter
`engine/cap13_planar_moment_method.evaluate`; consumer `engine/cap13_planar_moment.py`.

## 3. Method definition and derivation

`M = F × d⊥`. The moment of a force about a point is the force multiplied by the perpendicular distance from the point to
the force's line of action (NASA-S1, NASA-T1; §11). With `F` in N and `d⊥` in mm the product is directly in N·mm; no
conversion factor is applied. The magnitude form, the planar restriction and the declarations are InventorAI's own bounded
restatement; NASA does not publish this method. One multiplication is executed; there is no subtraction, sign convention,
resultant, rounding, clamping or magnitude ceiling.

## 4. Roles, quantity kinds and exact unit tokens

| Role | Meaning | Quantity kind | Exact unit token |
|---|---|---|---|
| `F` | magnitude of the one declared force | `force` | `N` |
| `d_perp` (`d⊥`) | perpendicular distance from the chosen point to the force's line of action | `length` | `mm` |
| `M` | magnitude of the moment of that force about that point | `moment` | `N·mm` |

The units are fixed and shown, never chosen. `N·mm` is never converted to `N·m` or any other unit. `d_perp` and `M` are
ASCII role identifiers, never aliases.

## 5. Applicability declarations

Each is shown as its own statement and answered «applies» or «does not apply», none pre-selected. A missing answer is
`NOT_DECLARED`; «does not apply» is `MODEL_NOT_SUPPORTED`. InventorAI infers none of them.

| Ref | Id | Accepted statement |
|---|---|---|
| D-1 | `planar` | planar: the force and the chosen point lie in one plane, and only the turning effect about the axis through the point at right angles to that plane is wanted |
| D-2 | `single_force` | ONE force only: no other force, couple, spread-out load or weight is included in this calculation |
| D-3 | `perpendicular_distance` | the distance d_perp is the shortest (perpendicular) distance from the chosen point to the line along which the force acts, not a length along a lever, arm or part unless that length is itself at right angles to the force; InventorAI does not check it |
| D-4 | `chosen_point` | the point is the inventor's own choice (for example a pivot, joint or fixing); InventorAI does not choose it, check it or decide that it is the right point |
| D-5 | `static_magnitude` | the force is treated as steady (static), and only the size of the moment is wanted, not its turning direction; no motion, impact, vibration or repeated loading is considered |

## 6. Numeric domain and numerical acceptance

- `F` and `d⊥` are finite numbers strictly greater than zero, typed as strict unsigned ASCII decimals (digits with an
  optional single fractional part; no sign, exponent, separator, Unicode digit, unit suffix or normalization), each capped
  at 64 characters for abuse protection only — a NON-PHYSICAL bound, never a range of valid forces or distances. Anything
  else, including a zero, is `INVALID_NUMERIC_INPUT`, resolved before the shared owner is called. A zero input is refused,
  never computed; this is distinct from an arithmetic underflow (below).
- No physical magnitude ceiling exists.
- **Numerical acceptance.** The computed binary64 `M` is accepted ONLY when it is finite, strictly positive and
  `|M − F·d⊥| ≤ 2^-52 · F·d⊥`, where `F·d⊥` is the EXACT mathematical product of the two actual binary input values,
  checked with exact rational arithmetic in the adapter. A correctly rounded product meets this bound for every normal
  result. A subnormal `M` is accepted when it meets the bound — an exact subnormal product always does — and is never
  refused merely for being subnormal; an inexact subnormal whose rounding error exceeds the bound is refused.
- Overflow to infinity, underflow to zero from positive inputs, and a result outside the accepted relative error are
  `FAILURE / EXECUTION_INTEGRITY_FAILURE` with no numerical payload, displayed as `KNOWLEDGE_UNAVAILABLE`, never rewritten
  as a refusal. These cases are unreachable from the page grammar and are proven at owner and adapter level.
- Display is the shortest round-trip binary64 decimal (`repr`); no rounding or significant-figure policy is applied.

## 7. Refusal and abstention semantics

Order after request integrity (CSRF), project authorization, eligibility and strict capture (a malformed request — an
unknown or repeated field, or an answer outside its closed choices — is a bare 400 with no reason token): (1) completeness —
every declaration and screen item answered, else `NOT_DECLARED`; (2) screen — any YES is `ENGINEERING_REVIEW_REQUIRED` and
the owner is not invoked; (3) declarations — any «does not apply» is `MODEL_NOT_SUPPORTED`; (4) numeric (§6) —
`INVALID_NUMERIC_INPUT`; (5) the shared owner. The first failing stage alone decides; no stage after it is evaluated.
Owner correspondence: `REFUSAL / INVALID_NUMERIC_INPUT` → `INVALID_NUMERIC_INPUT`; `REFUSAL / UNIT_NOT_ADMITTED` or
`UNKNOWN_UNIT` → `UNIT_NOT_SUPPORTED`; `REFUSAL / METHOD_NOT_REGISTERED` or `VERSION_MISMATCH`, `UNABLE / SOURCE_UNAVAILABLE`
and `FAILURE / EXECUTION_INTEGRITY_FAILURE` → `KNOWLEDGE_UNAVAILABLE`; any other owner state → the neutral
`UNMAPPED_OWNER_OUTCOME`. The owner state and token are preserved, never rewritten.

## 8. High-risk screen (declared; not a safety engine)

The same nine items as the two-support screen, in the same order and with the same copy: supports people; overhead or
falling hazard; use by or for children; safety-critical load path; pressure; high temperature; battery containment; medical
use; food contact. All NO answers only allow this bounded calculation to proceed and never mean safe. The screen neither
reads nor feeds SafetySignal.

## 9. Result, provenance and fixed disclosure

On success the page shows `M` in N·mm exactly as produced, labelled `UNVALIDATED` and `NOT EVIDENCE`, with the method
identity and version, the method sources and unit records the owner carried, the inputs echoed and this fixed disclosure
(English; pinned equal to the artifact):

1. This is the size of the turning effect (moment) of the one force you declared about the one point you chose, in one plane, using your own force F and your own perpendicular distance d⊥.
2. It does not show that anything is balanced or held in place, and it gives no support reaction, turning direction or combined effect of several forces.
3. It does not tell whether a joint, fixing, shaft, part, motor or material can carry this moment, and it is not compared with any rating, strength or limit.
4. It is preliminary, advisory, UNVALIDATED and not evidence, and it must be confirmed by measurement or a qualified engineer before any reliance; it says nothing about whether the design is suitable or safe.
5. InventorAI does not check your force, your distance, your chosen point or that your declarations match the real configuration.
6. Three-dimensional effects, several forces, motion, impact, vibration and repeated loading are outside this calculation.
7. Reference source material: NASA Glenn Research Center (equilibrium and torque / moment principles); the moment form is InventorAI's own restatement.

## 9A. Arabic disclosure and UX wording

**A-1 Fixed disclosure (Arabic rendering of the seven §9 items, item by item; no meaning added, removed or softened).**

> 1. هذا هو مقدار أثر الدوران (العزم) للقوة الواحدة التي صرّحت بها حول النقطة الواحدة التي اخترتها، في مستوى واحد، باستخدام قيمتي القوة F والمسافة العمودية d⊥ اللتين أدخلتهما أنت.
> 2. لا يبيّن هذا الناتج أن أي شيء متوازن أو مثبّت في مكانه، ولا يعطي أي رد فعل لمسند، ولا اتجاه دوران، ولا الأثر المجمَّع لعدة قوى.
> 3. لا يبيّن هذا الناتج ما إذا كان أي مفصل أو تثبيت أو عمود أو جزء أو محرك أو مادة قادرًا على تحمّل هذا العزم، ولا يُقارَن بأي تصنيف أو مقاومة أو حدّ.
> 4. هذه النتيجة أولية وإرشادية، وغير مُتحقَّق منها (UNVALIDATED)، وليست دليلًا، ويجب تأكيدها بالقياس أو بمراجعة مهندس مؤهل قبل الاعتماد عليها؛ ولا تقول شيئًا عن ملاءمة التصميم أو سلامته.
> 5. لا يتحقق InventorAI من قيمة القوة ولا من المسافة ولا من النقطة التي اخترتها، ولا من مطابقة تصريحاتك للتكوين الفعلي.
> 6. التأثيرات ثلاثية الأبعاد، وتعدد القوى، والحركة، والصدمات، والاهتزاز، والتحميل المتكرر كلها خارج نطاق هذا الحساب.
> 7. المراجع: مركز غلين للأبحاث التابع لوكالة ناسا (NASA Glenn Research Center) — مبادئ الاتزان والعزم. أما صيغة العزم هنا فهي إعادة صياغة خاصة بـInventorAI.

**A-2 Applicability declarations (§5).** The inventor answers «ينطبق على حالتي» or «لا ينطبق على حالتي», none pre-selected.

| §5 | Arabic statement |
|---|---|
| D-1 planar | مستوى واحد: القوة والنقطة التي اخترتها تقعان في مستوى واحد، والمطلوب فقط أثر الدوران حول المحور المارّ بالنقطة عموديًا على ذلك المستوى. |
| D-2 single_force | قوة واحدة فقط: لا تدخل في هذا الحساب أي قوة أخرى، ولا ازدواج (couple)، ولا حمل موزَّع، ولا وزن. |
| D-3 perpendicular_distance | d⊥ هي أقصر مسافة (المسافة العمودية) من النقطة المختارة إلى الخط الذي تؤثر على امتداده القوة، وليست طولًا على امتداد ذراع أو رافعة أو جزء ما لم يكن ذلك الطول نفسه عموديًا على القوة؛ ولا يتحقق InventorAI منها. |
| D-4 chosen_point | النقطة من اختيارك أنت (مثل محور دوران أو مفصل أو نقطة تثبيت)؛ لا يختارها InventorAI ولا يتحقق منها ولا يقرر أنها النقطة الصحيحة. |
| D-5 static_magnitude | القوة تُعامَل على أنها ثابتة (ساكنة)، والمطلوب مقدار العزم فقط لا اتجاه دورانه؛ ولا تؤخذ في الحسبان أي حركة أو صدمة أو اهتزاز أو تحميل متكرر. |

**A-3 Screen (§8).** The Arabic screen stem, items, answers and note are the existing two-support screen copy
(`UI_CAP13_SCREEN_*`), reused unchanged.

**A-4 Right-to-left rendering.** Numbers, the role symbols `F`, `d⊥` and `M`, the unit tokens `N`, `mm` and `N·mm`, the
method identity and `UNVALIDATED` / `NOT EVIDENCE` are each direction-isolated (`<bdi dir="ltr">`) on the Arabic page; the
inventor's typed values are shown left-to-right.

## 10. Exclusions (binding)

No static equilibrium, moment balance, resultant, support reaction or sign / turning-direction convention; no joint,
fastener, shaft, bearing, weld or member capacity, strength, stress, deflection, fatigue or failure check; no torque rating,
motor or actuator sizing; no thickness, material or specification; no design suitability, stability or safety conclusion;
no three-dimensional moment, several forces, couples, spread-out loads, friction, motion, impact, vibration or repeated
loading; no inference of any force, distance, point or declaration; no unit conversion; no persistence, report, PDF,
Structured Export, API, evidence, readiness, progression, gap or SafetySignal effect; no AI or provider call; no
eligibility for any part other than the one declared Mechanical part (§1), and no inference from a part's name or
function. *(Superseded by the integrated-part eligibility amendment, preserved — was: "no integrated-part eligibility
(§1).")*

## 11. Source and source-use status

- **NASA-S1** — NASA Glenn Research Center, Beginners Guide to Aeronautics, *Equilibrium*
  (<https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/equilibrium/>). Supports, for this method, only: torque /
  moment is force multiplied by perpendicular distance. Reuses the Lead-supplied inspection of 2026-10-07 already recorded
  for the two-support method; that record's scope is not changed.
- **NASA-T1** — NASA Glenn Research Center, Beginners Guide to Aeronautics, *Torque (Moment)*
  (<https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/torque-moment/>). Supports only the same relation (textual
  statement). Reuses the Lead-level inspection of 2026-09-28 recorded as `mechanical:PR006`, whose disposition stays scoped
  to its own records.
- **Units** — NIST SP 811: N (Chapter 4, Table 3) and mm (Tables 1 and 5) as already recorded by `dcu:U001` / `dcu:U002`;
  N·m as the SI unit of moment of force (Appendix B.9, Lead-level inspection of 2026-09-28 recorded as `mechanical:PR009`).
  N·mm is InventorAI's own formation from these facts (`dcu:U006`).
- **Source use** (not legal opinions): NASA STI terms (`cap13m:SU001`; owner snapshot `dcu:SU005`) — U.S. Government works
  generally not protected by copyright in the U.S., NASA-hosted pages may contain third-party content, no endorsement; and
  NIST Technical Series terms (`cap13m:SU002`; owner snapshot `dcu:SU006`) — NIST acknowledgement, third-party material
  excluded. Use is factual paraphrase and unit identification only; no NASA or NIST prose, image, table, figure, branding
  or conversion factor is reproduced. All inspections are Lead-supplied and not independently re-inspected by the executor;
  existing records (`cap13:SU001`, `dcu:SU001` to `dcu:SU004`, `mechanical:PR006` to `PR011`) keep their own scopes.

## 12. Implementation boundary

The one existing shared owner executes the method through ONE additional immutable binding created by application wiring
(`_CAP13_MOMENT_BINDING` in `web/app.py`), beside the two existing bindings; there is no registry, discovery, dynamic
module path or request-selected method (calc/units contract §13B). Routes: `GET` / `POST /session/<sid>/planar-moment`,
behind the central project authorization and the global CSRF guard; the session page shows one optional link on an eligible
project. Eligibility reuses `_calc_gate(sid, consumer)` (§1). Nothing is persisted; the POST renders its result
directly.

## 13. Verification

Focused tests (`tests/test_cap13_planar_moment.py`, `tests/test_cap13_planar_moment_browser.py`): exact-rational reference
products for normal and boundary values; overflow; underflow to zero; exact and inexact subnormal results; zero-input
refusal versus underflow; non-finite, invalid and out-of-scope input; unit / method / version / adapter integrity failing
closed; owner artifact v3 and moment artifact tamper; the §7 order and owner correspondence; the Mechanical-root and
integrated Mechanical-part gate (`tests/test_cap13_planar_moment_integrated_part.py`); the two-support and THERM-01
methods unchanged; EN / AR fidelity; and real-browser EN / AR journeys. Hosted required CI is the
merge gate.

## 14. STOP conditions

Stop and return to the Owner on a source or IP deficiency, a contract incompatibility, unprovable numerical integrity or any
scope expansion (another method, consumer, unit, conversion, eligibility beyond §1, persistence or report surface).
