# STAGE 25 / CAP-13 — LINEAR SPEED-DEPENDENT ROTATIONAL LOAD METHOD CONTRACT

STATUS: OWNER-AUTHORIZED BOUNDED METHOD CONTRACT — written with, and governing, the one bounded implementation increment
`ROTATIONAL-LOAD-SLICE-01` (MECHANICAL — LINEAR SPEED-DEPENDENT ROTATIONAL LOAD — SLICE 1), which the Owner authorized as
ONE bounded implementation and ONE pull request. Applicability: this contract governs the delivered method only on the
verified merge of that pull request into `feature/atomic-json-session-persistence`; on its proposal branch it describes an
Owner-authorized proposed method, not a merged or delivered capability. Merge, deployment, external dependency admission,
Modelica integration and Motion / Mechatronics activation are NOT authorized by it.
AUTHORITY LEVEL: subordinate to the CAP-13 entry of the
[Capability Enrichment Register](INVENTORAI_CAPABILITY_ENRICHMENT_REGISTER.md) and to the accepted
[shared deterministic calculation and units owner boundary contract](SHARED_DETERMINISTIC_CALCULATION_AND_UNITS_OWNER_BOUNDARY_CONTRACT.md)
(the "calc/units contract", with its Correction 04, §13C, added by the same increment). It amends neither the Register nor
any other method contract; the two-support reactions, THERM-01 and planar-moment methods stay unchanged. Where this
document and the calc/units contract differ, the calc/units contract wins and the difference is a defect of this document.

---

## 0. Preserved truth (binding)

- `ACTIVE CONTRACT: NONE` describes the state before and after this increment; this contract fills no active-contract slot
  after delivery and is not a delivery record. Current-truth delivery records belong to a later closure sync.
- Stage 25 stays ENTERED / PARTIAL and its checkbox stays UNTICKED; this method enters, completes or reopens no Stage and
  changes no roadmap count. `FULL CAP-13: NOT AUTHORIZED`; D-7 stays OPEN.
- The preliminary-motion blocker (CLAUDE.md block (h)) is NOT discharged: this method evaluates one declared load model at
  one speed; it does not say whether any motor can drive a mechanism, and it adds no motor characteristic.
- Motion / Mechatronics, Power Electronics / Motion (28-T3), D4 and T6 stay as recorded; nothing here activates them.

## 1. Purpose and scope

ONE optional, advisory, non-binding, request-local calculation: the SIGNED torque that ONE inventor-declared resisting load,
proportional to shaft speed and zero at zero speed, applies at ONE shaft at ONE signed operating speed. It lets an inventor
who knows one point of such a load — the torque at one speed, from their own measurement or documentation — see the
torque that same declared load gives at another speed, in either direction of rotation, with the sign made explicit. A
typical load class is a linear viscous damper; the page names no device and supplies no value.

Eligibility: the SAME rule as the other CAP-13 calculations (`_calc_gate` / `_calc_declared_part` in `web/app.py`): a
project whose trusted durable root domain is exactly `mechanical`, or, whatever the initial analysis focus, the ONE
inventor-declared Mechanical part of a valid durable Stage-15 integrated composition, read only through the store-validated
composition and never from the request; the page names that part with the existing CAP-13 attribution wording. The Stage 15
exception in `engine/subsystem_model.py` names this method. A declared part makes the calculation OFFERED only: it
establishes no applicability, suitability, validation or safety and supplies no value, declaration or screen answer. A
missing, malformed, corrupt or unreadable composition grants nothing beyond the root rule (fail closed). The session link,
the page and the submission read the same one decision.

## 2. Method identity and version

Identity `cap13:linear_speed_dependent_rotational_load`, version `1.0`. Method-authority artifact
`docs/governance/cap13_content_config/linear_speed_dependent_rotational_load_v1.json`
(`cap13_linear_speed_dependent_rotational_load`, artifact version `1`), separate from every other artifact; none loads
another. Adapter `engine/cap13_rotational_load_method.evaluate`; consumer `engine/cap13_rotational_load.py`.

## 3. Method definition

`τ = τ_nominal × (ω / ω_nominal)`, the relation of Modelica Standard Library v4.1.0
`Modelica.Mechanics.Rotational.Sources.LinearSpeedDependentTorque` with `TorqueDirection=false` ONLY (§11). There:

- `ω` is the angular velocity of the flange with respect to its support (`= der(phi)`);
- `τ` is the accelerating torque acting at the flange (`= -flange.tau`): positive in the positive direction of rotation;
- a negative `τ_nominal` acts as a load in the positive direction of rotation.

With `τ_nominal < 0` and `ω_nominal > 0` the torque opposes the rotation in BOTH directions: for positive `ω` the resisting
`τ` is negative, for negative `ω` it is positive, and at `ω = 0` it is exactly zero. The `TorqueDirection=true` variant
(`τ_nominal × |ω / ω_nominal|`) is NOT admitted and `abs(ω)` is never used. The relation is restated independently; no
Modelica code is copied or executed, and InventorAI does not show that the model describes the inventor's mechanism.

## 4. Roles, quantity kinds and exact unit tokens

| Role | Meaning | Quantity kind | Exact unit token |
|---|---|---|---|
| `tau_nominal` (`τ_nominal`) | nominal torque of the declared load at the nominal speed; strictly negative | `torque` | `N·m` |
| `w_nominal` (`ω_nominal`) | nominal speed at which `τ_nominal` is known; strictly positive | `angular_velocity` | `rad/s` |
| `w` (`ω`) | signed operating speed relative to the support; zero valid | `angular_velocity` | `rad/s` |
| `tau` (`τ`) | signed accelerating torque the load applies at the shaft (`-flange.tau`) | `torque` | `N·m` |

The units are fixed and shown, never chosen; no unit is converted. `torque` is a quantity kind of its own, distinct from
the planar method's `moment` (`N·mm`); the owner composes no dimensional equivalence between them.

## 5. Applicability declarations

Each is shown as its own statement and answered «applies» or «does not apply», none pre-selected. A missing answer is
`NOT_DECLARED`; «does not apply» is `MODEL_NOT_SUPPORTED`. InventorAI infers none of them.

| Ref | Id | Accepted statement |
|---|---|---|
| D-1 | `linear_through_zero` | the load's torque is proportional to the shaft speed and zero at zero speed, over every speed considered, including the operating speed entered |
| D-2 | `nominal_point` | tau_nominal at w_nominal is one known point of exactly this load, taken from the inventor's own measurement or documentation; InventorAI does not estimate or check it |
| D-3 | `single_axis` | one shaft rotating about one fixed axis, with every speed measured relative to the stationary support and the same positive direction of rotation used for all of them |
| D-4 | `load_only` | only this one speed-dependent load is considered: no acceleration, inertia, friction, backlash, other load or motor behaviour is included |
| D-5 | `sign_convention` | the result is the torque the load applies at the shaft, positive in the positive direction of rotation, so a resisting load is negative for positive rotation and positive for negative rotation |

## 6. Numeric domain and numerical acceptance

- **Grammar.** Strict ASCII decimals (digits with an optional single fractional part); ONE leading minus sign is allowed for
  `τ_nominal` and `ω` only; no plus sign, exponent, separator, Unicode digit, unit suffix or normalization; each field capped
  at 64 characters for abuse protection only — a NON-PHYSICAL bound, never a range of valid torques or speeds.
- **Signs.** `τ_nominal < 0`, `ω_nominal > 0`, `ω` any finite value including zero (a typed `-0` is zero). A wrong sign, a
  zero `τ_nominal` or `ω_nominal`, or a malformed or non-finite value is `INVALID_NUMERIC_INPUT`, resolved before the owner;
  the owner's own applicability (`less_than_zero` / `greater_than_zero`) refuses a wrong-signed nominal value it receives
  as `INPUT_OUTSIDE_ADMITTED_RANGE`.
- **No physical limits.** No magnitude limit exists for any input. Whether the linear model applies at a speed is the
  inventor's declaration (D-1), never a numeric range.
- **Arrangement.** The exact rational value `τ_nominal × ω / ω_nominal` of the three actual binary inputs is formed and
  rounded ONCE to binary64 (round half to even), so no intermediate product or quotient can overflow, underflow or round.
- **Acceptance.** A zero `ω` gives the exact rational zero and returns exactly `0.0` — never confused with an underflow. A
  nonzero exact result is accepted only when the rounded value is finite, nonzero, of the exact result's sign and
  `|τ − exact| ≤ 2^-52 · |exact|`. A correctly rounded normal result always meets this (its error is at most `2^-53`
  relative), so the bound is feasible at every normal boundary; a subnormal result is accepted only when it meets the same
  bound and is otherwise refused.
- **Failures.** Overflow, underflow to zero of a nonzero exact result, a changed sign or an out-of-bound result is
  `FAILURE / EXECUTION_INTEGRITY_FAILURE` with no numerical payload, displayed as `KNOWLEDGE_UNAVAILABLE`, never rewritten
  as a refusal. These cases are unreachable from the page grammar and are proven at owner and adapter level.
- This acceptance rule belongs to this method only; it is not a generic owner numerical policy.
- **Display.** The shortest round-trip binary64 decimal (`repr`); no rounding policy and no `abs()`.

## 7. Refusal and abstention semantics

Order after request integrity (CSRF), project authorization, eligibility and strict capture (a malformed request — an
unknown or repeated field, or an answer outside its closed choices — is a bare 400 with no reason token): (1) completeness —
every declaration and screen item answered, else `NOT_DECLARED`; (2) screen — any YES is `ENGINEERING_REVIEW_REQUIRED` and
the owner is not invoked; (3) declarations — any «does not apply» is `MODEL_NOT_SUPPORTED`; (4) numeric (§6) —
`INVALID_NUMERIC_INPUT`; (5) the shared owner. The first failing stage alone decides. Owner correspondence:
`REFUSAL / INVALID_NUMERIC_INPUT` → `INVALID_NUMERIC_INPUT`; `REFUSAL / UNIT_NOT_ADMITTED` or `UNKNOWN_UNIT` →
`UNIT_NOT_SUPPORTED`; `REFUSAL / METHOD_NOT_REGISTERED` or `VERSION_MISMATCH`, `UNABLE / SOURCE_UNAVAILABLE` and
`FAILURE / EXECUTION_INTEGRITY_FAILURE` → `KNOWLEDGE_UNAVAILABLE`; any other owner state → the neutral
`UNMAPPED_OWNER_OUTCOME`. The owner state and token are preserved, never rewritten.

## 8. High-risk screen (declared; not a safety engine)

The same nine items as the other CAP-13 screens, in the same order and with the same copy: supports people; overhead or
falling hazard; use by or for children; safety-critical load path; pressure; high temperature; battery containment; medical
use; food contact. All NO answers only allow this bounded calculation to proceed and never mean safe. The screen neither
reads nor feeds SafetySignal.

## 9. Result, provenance and fixed disclosure

On success the page shows `τ` in N·m exactly as produced with its sign, the explicit sign convention, the labels
`UNVALIDATED` and `NOT EVIDENCE`, the method identity and version, the method source and unit records the owner carried,
the inputs echoed and this fixed disclosure (English; pinned equal to the artifact):

1. This is the torque that the one speed-dependent load you declared applies at the shaft at the speed ω you entered, using your own nominal torque τ_nominal at your own nominal speed ω_nominal.
2. Sign convention: τ is positive in the positive direction of rotation, so this resisting load gives a negative τ for positive ω, a positive τ for negative ω and exactly zero at ω = 0.
3. It assumes the load torque stays proportional to speed and is zero at zero speed; InventorAI does not check that your load behaves this way at any speed.
4. It includes no acceleration, inertia, friction, starting torque or other load, and it does not tell whether any motor, gearbox, shaft or part can drive or carry this load.
5. It is preliminary, advisory, UNVALIDATED and not evidence, and it must be confirmed by measurement or a qualified engineer before any reliance; it says nothing about suitability or safety.
6. InventorAI does not check your values or that your declarations match the real mechanism.
7. Reference source material: Modelica Standard Library v4.1.0 (Modelica Association and contributors, BSD 3-Clause License); the relation is restated by InventorAI, and no Modelica code is used.

## 9A. Arabic disclosure and UX wording

**A-1 Fixed disclosure (Arabic rendering of the seven §9 items, item by item; no meaning added, removed or softened).**

> 1. هذا هو العزم الذي يؤثر به الحمل الواحد المعتمد على السرعة الذي صرّحت به على العمود، عند السرعة ω التي أدخلتها، باستخدام عزمك الاسمي τ_nominal عند سرعتك الاسمية ω_nominal.
> 2. اصطلاح الإشارة: تكون τ موجبة في الاتجاه الموجب للدوران، لذلك يعطي هذا الحمل المقاوم قيمة τ سالبة عندما تكون ω موجبة، وقيمة موجبة عندما تكون ω سالبة، وصفرًا تمامًا عند ω = 0.
> 3. يفترض هذا الحساب أن عزم الحمل يبقى متناسبًا مع السرعة ويساوي صفرًا عند السرعة صفر؛ ولا يتحقق InventorAI من أن حملك يسلك هذا السلوك عند أي سرعة.
> 4. لا يتضمن الحساب أي تسارع أو قصور ذاتي أو احتكاك أو عزم بدء أو حمل آخر، ولا يبيّن ما إذا كان أي محرك أو صندوق تروس أو عمود أو جزء قادرًا على إدارة هذا الحمل أو تحمّله.
> 5. هذه النتيجة أولية وإرشادية، وغير مُتحقَّق منها (UNVALIDATED)، وليست دليلًا، ويجب تأكيدها بالقياس أو بمراجعة مهندس مؤهل قبل الاعتماد عليها؛ ولا تقول شيئًا عن الملاءمة أو السلامة.
> 6. لا يتحقق InventorAI من قيمك، ولا من مطابقة تصريحاتك للآلية الفعلية.
> 7. المراجع: مكتبة Modelica Standard Library الإصدار v4.1.0 (Modelica Association والمساهمون، رخصة BSD 3-Clause)؛ والعلاقة معاد صياغتها من InventorAI، ولا يُستخدم أي كود من Modelica.

**A-2 Applicability declarations (§5).** The inventor answers «ينطبق على حالتي» or «لا ينطبق على حالتي», none pre-selected.

| §5 | Arabic statement |
|---|---|
| D-1 linear_through_zero | عزم الحمل يتناسب مع سرعة العمود ويساوي صفرًا عند السرعة صفر، وذلك لكل سرعة معنيّة، بما فيها سرعة التشغيل المُدخلة. |
| D-2 nominal_point | قيمة τ_nominal عند ω_nominal نقطة واحدة معروفة لهذا الحمل تحديدًا، مأخوذة من قياسك أنت أو من وثائقك؛ ولا يقدّرها InventorAI ولا يتحقق منها. |
| D-3 single_axis | عمود واحد يدور حول محور ثابت واحد، وكل سرعة تُقاس بالنسبة إلى المسند الثابت، مع اعتماد الاتجاه الموجب نفسه للدوران في جميعها. |
| D-4 load_only | لا يُؤخذ في الحسبان إلا هذا الحمل الواحد المعتمد على السرعة: لا تسارع، ولا قصور ذاتي، ولا احتكاك، ولا خلوص، ولا حمل آخر، ولا سلوك للمحرك. |
| D-5 sign_convention | الناتج هو العزم الذي يؤثر به الحمل على العمود، موجبًا في الاتجاه الموجب للدوران؛ لذلك يكون الحمل المقاوم سالبًا للدوران الموجب وموجبًا للدوران السالب. |

**A-3 Screen (§8).** The existing CAP-13 screen copy (`UI_CAP13_SCREEN_*`), reused unchanged.

**A-4 Right-to-left rendering.** Numbers, the role symbols `τ_nominal`, `ω_nominal`, `ω` and `τ`, the unit tokens `N·m`
and `rad/s`, the method identity and `UNVALIDATED` / `NOT EVIDENCE` are each direction-isolated on the Arabic page; the
inventor's typed values are shown left-to-right.

## 10. Exclusions (binding)

No dynamics, acceleration, inertia, simulation, friction model, starting or breakaway torque, power or energy; no
`TorqueDirection=true` variant and no `abs(ω)`; no motor, actuator, gearbox or drive selection, sizing or rating; no torque
capacity, strength, compatibility, suitability, stability or safety conclusion; no inference of any declaration, value or
load type, and no device measurement supplied by InventorAI; no unit conversion; no Modelica code, runtime, FMU or external
dependency; no persistence, report, PDF, Structured Export, API, evidence, readiness, progression, gap or SafetySignal
effect; no AI or provider call; no eligibility for any part other than the one declared Mechanical part (§1).

## 11. Source and IP status

- **MODELICA-S1** — Modelica Standard Library v4.1.0, `Modelica/Mechanics/Rotational/Sources/LinearSpeedDependentTorque.mo`,
  git tag `v4.1.0`, commit `8ae3d35c24e519cb2996cab20f3b13daf2b0c50a`
  (<https://github.com/modelica/ModelicaStandardLibrary/blob/v4.1.0/Modelica/Mechanics/Rotational/Sources/LinearSpeedDependentTorque.mo>).
  Supports only the §3 relation for `TorqueDirection=false`, the meaning of `ω` and `τ` (`-flange.tau`), the load meaning of
  a negative `τ_nominal` and `w_nominal(min = Modelica.Constants.eps)`.
- **Units** — `Modelica/Units.mo`, package `SI`: `Torque` in `N.m` (written `N·m`; consistent with the NIST SP 811
  Appendix B.9 identification recorded as `mechanical:PR009`) and `AngularVelocity` in `rad/s` (`dcu:U007`, `dcu:U008`).
- **Provenance and licence** (not a legal opinion): Copyright (c) 1998-2025, Modelica Association and contributors; BSD
  3-Clause License (`LICENSE` at the same tag). Use is a factual reference only: the relation, its sign meaning and two SI
  unit identifications are restated independently in InventorAI's own words. No Modelica source code, annotation, icon,
  diagram, documentation text or runtime is copied, redistributed or executed, so no code-redistribution obligation
  arises; attribution is given as acknowledgement (`cap13r:SU001`; owner snapshot `dcu:SU007`). The names of the Modelica
  Association and contributors are used only to identify the source, never to imply endorsement; Modelica is a registered
  trademark of the Modelica Association.
- **Inspection basis.** The Lead / Owner supplied the file, version, relation and unit tokens in the authorizing brief; the
  executor confirmed each directly against the tag above on 2026-10-24. No other source is relied upon.

## 12. Implementation boundary

The one existing shared owner executes the method through ONE additional immutable binding created by application wiring
(`_CAP13_ROTATIONAL_LOAD_BINDING` in `web/app.py`), beside the three existing bindings; there is no registry, discovery,
dynamic module path or request-selected method (calc/units contract §13C). Routes: `GET` / `POST
/session/<sid>/rotational-load`, behind the central project authorization and the global CSRF guard; the session page shows
one optional link on an eligible project. Nothing is persisted; the POST renders its result directly.

## 13. Verification

Focused tests (`tests/test_cap13_rotational_load.py`, `tests/test_cap13_rotational_load_browser.py`): the reference pairs
for `τ_nominal = -2 N·m`, `ω_nominal = 10 rad/s` — `(ω, τ)` = `(-10, +2)`, `(-5, +1)`, `(0, 0)`, `(+5, -1)`, `(+10, -2)`;
an independent exact-rational reference; overflow; underflow to zero; exact and inexact subnormal results; zero speed
versus underflow; sign violations; zero and negative nominal speed; grammar; unit / method / version / adapter integrity;
owner artifact v4 and method artifact tamper; the §7 order and owner correspondence; root and integrated-part eligibility
and fail-closed composition; the three existing methods unchanged; EN / AR fidelity; and real-browser EN / AR journeys.
Hosted required CI is the merge gate.

## 14. STOP conditions

Stop and return to the Owner on a source or IP deficiency, a need to incorporate external code, a contract
incompatibility, unprovable numerical acceptance, an unqualified operating claim or any scope expansion (another method,
consumer, unit, conversion, motor or dynamics capability, persistence or report surface).
