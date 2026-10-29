# MECHANICAL — FREE LINEAR THERMAL EXPANSION METHOD CONTRACT

STATUS: OWNER-AUTHORIZED BOUNDED METHOD CONTRACT — written with, and governing, the one bounded implementation increment
`MECHANICAL-FREE-LINEAR-THERMAL-EXPANSION-01`, which the Owner authorized as ONE bounded (g1) step-3 engineering-depth
increment (method / source admission from the existing Q-22 qualified basis, the minimum calc / units owner Correction 13,
implementation, focused tests and one pull request). Applicability: this contract governs the delivered method only on the
verified merge of that pull request into `feature/atomic-json-session-persistence`; on its proposal branch it describes an
Owner-authorized proposed method, not a merged or delivered capability. Merge, deployment, production activation, a (g1)
step-4 transition, a Materials domain and any broader capability admission are NOT authorized by it.
AUTHORITY LEVEL: subordinate to the accepted
[shared deterministic calculation and units owner boundary contract](SHARED_DETERMINISTIC_CALCULATION_AND_UNITS_OWNER_BOUNDARY_CONTRACT.md)
(the "calc/units contract", with its Correction 13, §13L, added by the same increment) and to the Mechanical Domain Pack's
governed authority. It amends no other method contract. Where this document and the calc/units contract differ, the
calc/units contract wins and the difference is a defect of this document.

---

## 0. Preserved truth (binding)

- `ACTIVE CONTRACT: NONE` describes the state before and after this increment; this contract fills no active-contract slot
  after delivery and is not a delivery record. Current-truth delivery records belong to the post-merge closure sync.
- This method enters, completes or reopens no Stage and changes no roadmap count (27 of 45 complete); it stays within
  (g1) step 3. No Materials domain is activated or created; no Domain Pack, `domains/domain_provenance.json` entry or
  domain-activation state changes.
- The twelve existing admitted methods keep their identities, artifacts, semantic pins, units and behaviour. The existing
  `length` / `mm` record (`dcu:U002`) and the existing `temperature_difference` / `K` record (`dcu:U005`) are reused
  unchanged; THERM-01's meaning of `K` (a difference ACROSS one heat path) is neither changed nor shared (§4).
- The research candidate DC resistive-load power → THERM-01 stays `BLOCKED — RELATIONSHIP AUTHORITY`; nothing here
  touches it, and no result of any calculation is transferred into or out of this method.
- `SRC-029` (DOE-HDBK-1017/1-93) is `IP-UNRESOLVED` and is relied upon by nothing here.
- The Stage 15 integrated-part exception (`engine/subsystem_model.py`) is extended to this method by name only, for the
  declared Mechanical part (§1).

## 1. Purpose and scope

ONE optional, advisory, non-binding, request-local calculation: the FREE change in length `ΔL` of ONE length of ONE
material that the inventor declares free to expand and contract, from the inventor's own average coefficient of linear
thermal expansion `α_avg`, the reference length `L_ref` that coefficient refers to and a temperature change `ΔT`. It lets a
nontechnical inventor see how much that length would move if nothing held it, so that they can see how much movement may
need to be accommodated where the part is held, joined or fitted, and what still has to be checked — without InventorAI
choosing a material, a coefficient, a gap or a mounting.

Eligibility: a project whose trusted durable root domain (`confirmed_domain`, read as the CAP-12 gate reads it) is exactly
`mechanical`; or, whatever the initial analysis focus, the ONE inventor-declared Mechanical part of a valid durable
Stage-15 integrated composition, read only through the store-validated composition (`_calc_gate` / `_calc_declared_part`,
the rule the other Mechanical calculations use) and never from the request. On an integrated project the page names that
part with the existing CAP-13 attribution wording. A declared part makes the calculation OFFERED only: it establishes
neither that the project has a length that changes with temperature, nor that the free-expansion model applies, nor that
the entered coefficient, length or temperature change is correct, and it supplies no value, declaration or screen answer.
A missing, malformed, corrupt or unreadable composition grants nothing beyond the root rule, and an unreadable root domain
offers nothing (fail closed). The session link, the page and the submission read the same one decision. Applicability
comes only from the method's explicit declarations (§5).

## 2. Method identity and version

Identity `mechanical:free_linear_thermal_expansion`, version `1.0`. Method-authority artifact
`docs/governance/mechanical_content_config/free_linear_thermal_expansion_v1.json`
(`mechanical_free_linear_thermal_expansion`, artifact version `1`), separate from every other method artifact; none loads
another. Adapter `engine/mechanical_thermal_expansion_method.evaluate`; consumer `engine/mechanical_thermal_expansion.py`.

## 3. Method definition and derivation

`ΔL = α_avg × L_ref × ΔT`.

1. **Source claim (SRC-031, recorded as `NBS-TE-S1`, §11).** NBS Circular 486, *Thermal Expansion of Solids* (Hidnert and
   Souder, 1950), PDF pages 7 and 31, as directly inspected by the TECH-SOURCES-001 research stream (run 10, 2026-10-28):
   practically all materials change dimensions when heated or cooled; the change in length depends on the original length
   and on the temperature range; an AVERAGE and an INSTANTANEOUS coefficient of linear expansion are defined. The research
   stream's claim mapping records that the product form follows from that definition.
2. **InventorAI's restatement (NOT a quotation).** The average coefficient over a temperature interval is the change in
   length per unit of the length it refers to, per degree of that interval. Rearranged for exactly that interval and that
   reference length, `ΔL = α_avg × L_ref × ΔT` — an identity under the definition, not an approximation, provided the
   coefficient really is the average over exactly the declared interval (D-5) and `L_ref` really is the length it refers
   to (D-6).
3. **What is NOT claimed from the source.** The recorded inspection does not quote the defining equation or state which
   length the coefficient refers to (the length at the start of the interval, or at a stated reference temperature).
   InventorAI therefore states NO convention of its own: the inventor declares that `L_ref` is the length their
   coefficient refers to under that coefficient's own definition (D-6). An arbitrary length is never substituted for
   `L_ref`.
4. **Average versus instantaneous.** Only the average coefficient over exactly the declared interval is admitted (D-5).
   An instantaneous coefficient, or a coefficient stated for one temperature or for a different interval, used across this
   interval would be a constant-coefficient assumption that the source does not establish, and the method refuses it.
5. **Sign.** `ΔT` is the final minus the initial temperature; with `α_avg > 0` and `L_ref > 0` the sign of `ΔL` is the
   sign of `ΔT` (heating lengthens, cooling shortens; D-7). Reversibility is declared, not established (D-8).

No NBS text, data table, figure or example is reproduced; the compiled data tables of the Circular, drawn from other
authors' publications, are not used, and no coefficient value is supplied or suggested.

## 4. Roles, quantity kinds and exact unit tokens

| Role | Meaning | Quantity kind | Exact unit token |
|---|---|---|---|
| `alpha_avg` (`α_avg`) | the inventor's own average coefficient of linear thermal expansion of the declared material, in the declared direction, over exactly the declared temperature interval; strictly positive | `linear_thermal_expansion_coefficient` | `1/K` |
| `L_ref` | the length to which that coefficient refers under its own definition; strictly positive | `length` | `mm` |
| `delta_T` (`ΔT`) | the change in the length's uniform temperature over time, final minus initial; signed | `temperature_difference` | `K` |
| `delta_L` (`ΔL`) | the free change in length; signed (positive lengthens, negative shortens) | `length` | `mm` |

The units are fixed and shown, never chosen. `1/K` is ONE NEW owner record (calc/units §13L, `dcu:U021`), the one token of
ONE NEW quantity kind `linear_thermal_expansion_coefficient` (dimension `Theta^-1`); it is InventorAI's bounded quantity
usage of the coherent SI quotient of one over the kelvin. `mm` (`dcu:U002`) and `K` (`dcu:U005`) are reused unchanged.
**`ΔT` here is a temporal change of ONE part's uniform temperature; THERM-01's `ΔT` is a difference ACROSS a heat path at
steady state.** They share a quantity kind and token only; nothing transfers one into the other, and the page says so
(§9 item 5). No conversion exists: `1/°C`, `°C⁻¹`, `K⁻¹`, `ppm/K`, `µm/(m·K)`, `10⁻⁶/K`, `/K`, `m`, `cm`, `µm`, `in`, `°C`
and `°F` are not admitted, aliased or normalised. A coefficient stated per degree Celsius has the same number per kelvin
(a difference of 1 °C equals a difference of 1 K, NIST SP 330, §11); the page may say so, and the inventor types the number
in `1/K`. `alpha_avg`, `L_ref`, `delta_T` and `delta_L` are ASCII role identifiers, never aliases.

## 5. Applicability declarations

Each is shown as its own statement and answered «applies» or «does not apply», none pre-selected. A missing answer is
`NOT_DECLARED`; «does not apply» is `MODEL_NOT_SUPPORTED`. InventorAI infers none of them. No numeric validity threshold
is stated or invented: a declaration only makes the bounded model applicable; it does not validate the physical product.

| Ref | Id | Accepted statement |
|---|---|---|
| D-1 | `free_unrestrained` | the length considered is free to expand and contract: nothing clamps, joins, holds or restrains it along this length during the change, so only its free change in length is calculated |
| D-2 | `one_material_uniform_temperature` | the length is ONE homogeneous material, at ONE uniform temperature at the start and ONE uniform temperature at the end, with no temperature difference along or across it |
| D-3 | `own_coefficient` | α_avg is the inventor's own value for this material; InventorAI did not select, look up, infer or check it, and does not decide that it is right |
| D-4 | `coefficient_direction` | α_avg applies in the direction of the length considered; for a material whose expansion depends on direction (for example wood, fibre composites or single crystals) it is the coefficient in this direction |
| D-5 | `average_over_interval` | α_avg is the AVERAGE coefficient of linear thermal expansion of this material over exactly the temperature interval considered, from the initial to the final temperature; it is not a value at one temperature applied to a wider interval and not a coefficient defined for another interval |
| D-6 | `reference_length` | L_ref is the length to which α_avg refers under the coefficient's own definition (its reference-temperature convention, for example the length at the temperature where the coefficient's interval starts, or at the reference temperature stated with the coefficient); InventorAI does not decide which length that is |
| D-7 | `signed_change` | ΔT is the final temperature minus the initial temperature, positive for heating and negative for cooling; the result ΔL is then positive for lengthening and negative for shortening |
| D-8 | `reversible_thermal_change_only` | only reversible thermal change of length occurs over the interval: no phase or material transformation, no permanent set, no hysteresis and no change caused by moisture, curing, ageing or load is included |

## 6. Numeric domain and numerical acceptance

- **Grammar (strict capture).** `α_avg`: a strict unsigned ASCII decimal of one to twelve integer digits and an optional
  fractional part of one to twelve digits. `L_ref`: unsigned, one to twelve integer digits and up to nine fractional
  digits. `ΔT`: an optional single leading minus, one to nine integer digits and up to nine fractional digits. No plus sign,
  exponent, separator, space, Unicode digit, unit suffix, `inf`, `nan` or normalization. Each field is also capped at 64
  characters for abuse protection only. A field sent twice, an unknown field or a declaration / screen answer outside its
  closed choices makes the whole request malformed (a bare 400). An omitted, malformed or over-length value is
  `INVALID_NUMERIC_INPUT`.
- **Representation limits are not physical limits.** `α_avg` from `10^-12` to below `10^12` 1/K; `L_ref` from `10^-9` to
  below `10^12` mm; `|ΔT| < 10^9` K. They are NOT physical limits, material ranges or a claim that such values are
  realistic; no physical magnitude ceiling exists.
- **Positive coefficient and length.** The EXACT decimal values of `α_avg` and `L_ref` must be greater than zero, decided
  before any binary rounding; a zero is `INVALID_NUMERIC_INPUT` with no number. A coefficient that is zero or negative is
  outside this slice: this is a limit of this calculation, not a statement that no material has one. A zero temperature
  change (including `-0`) is admitted and gives exactly `0` mm.
- **Binary bridge.** Each admitted decimal is converted ONCE to the correctly rounded binary64 value (round half to even)
  and handed to the owner as a typed number; the owner parses no string (calc/units §10). Every admitted nonzero value lies
  between `10^-12` and `10^12` in magnitude, so it is a normal binary64 number with relative rounding error at most `2^-53`.
- **Owner applicability.** The method record declares the existing `greater_than_zero` on `alpha_avg` and on `L_ref`; a
  non-positive value that reaches the owner is `UNABLE_TO_DETERMINE / INPUT_OUTSIDE_ADMITTED_RANGE`, shown as the neutral
  `UNMAPPED_OWNER_OUTCOME` (unreachable from the page). No result range is declared: `ΔL` is signed.
- **Binary acceptance (adapter).** The exact rational value `alpha_avg × L_ref × delta_T` of the three binary inputs is
  rounded ONCE to binary64. A zero temperature change (`0.0` or `-0.0`) gives exactly `+0.0`, never a negative zero. A
  nonzero exact result is accepted only when the rounded value is finite, nonzero, of the same sign as the exact value and
  `|ΔL − exact| ≤ 2^-52 · |exact|` (one correct rounding gives at most `2^-53`). Overflow, underflow of a nonzero result or
  any failed check is `FAILURE / EXECUTION_INTEGRITY_FAILURE` with no numerical payload, displayed as
  `KNOWLEDGE_UNAVAILABLE`, never rewritten as a refusal. Representability: inside the representation limits every nonzero
  result lies between `10^-30` mm (`10^-12 × 10^-9 × 10^-9`) and `10^33` mm (`10^12 × 10^12 × 10^9`) in magnitude, well
  inside the normal binary64 range, so neither overflow nor underflow can occur from the page; the guards stay in place for
  direct owner use.
- **Decimal-reference acceptance (consumer; the independent oracle).** A successful owner result is shown only when it
  agrees with the exact decimal value `α_avg × L_ref × ΔT` of the ENTERED decimals (an exact rational product, computed
  without binary arithmetic): exactly `+0` when, and only when, `ΔT` is exactly zero; otherwise of the same sign and within
  a relative error of `2^-50`. Proof that the bound always holds: with `u = 2^-53` the three binary inputs carry relative
  errors `|e₁|, |e₂|, |e₃| ≤ u` and the single rounding `|e₄| ≤ u`, so the total relative error is at most
  `(1 + u)⁴ − 1 = 4u + O(u²) < 4.0000001 · u < 8u = 2^-50` (the lower side, `1 − (1 − u)⁴`, is smaller), and no error
  changes the sign. A failed check is `KNOWLEDGE_UNAVAILABLE` with no number.
- **Display.** The shown value is derived from the exact decimal value, never from the binary value: rounded ONCE to 12
  significant digits, round half to even, trailing zeros removed, with its sign. It is labelled **exact** when that
  rounding changes nothing and **rounded to 12 significant digits** otherwise (`0.0000231` 1/K, `1000` mm, `50` K shows
  `1.155`, exact). Plain decimal notation is used for `10^-6 ≤ |ΔL| < 10^12` mm and the form `m × 10^e` otherwise, so a tiny
  nonzero change is never shown as `0`. The digits shown imply no measurement resolution, precision or accuracy.
- These rules belong to this method only; none is a generic owner numerical policy.

## 7. Refusal and abstention semantics

Order after request integrity (CSRF), project authorization, eligibility and strict capture (a malformed request is a bare
400 with no reason token): (1) completeness — every declaration and screen item answered, else `NOT_DECLARED`; (2) screen
— any YES is `ENGINEERING_REVIEW_REQUIRED` and the owner is not invoked; (3) declarations — any «does not apply» is
`MODEL_NOT_SUPPORTED`; (4) numeric (§6) — grammar, representation limits and strictly positive exact `α_avg` and `L_ref`,
else `INVALID_NUMERIC_INPUT`; (5) the shared owner; (6) the decimal-reference acceptance; (7) the display. The first
failing stage alone decides; no stage after it is evaluated. Owner correspondence: `REFUSAL / INVALID_NUMERIC_INPUT` →
`INVALID_NUMERIC_INPUT`; `REFUSAL / UNIT_NOT_ADMITTED` or `UNKNOWN_UNIT` → `UNIT_NOT_SUPPORTED`;
`REFUSAL / METHOD_NOT_REGISTERED` or `VERSION_MISMATCH`, `UNABLE / SOURCE_UNAVAILABLE` and
`FAILURE / EXECUTION_INTEGRITY_FAILURE` → `KNOWLEDGE_UNAVAILABLE`; any other owner state → the neutral
`UNMAPPED_OWNER_OUTCOME`. The owner state and token are preserved, never rewritten.

## 8. High-risk screen (declared; not a safety engine)

The same nine items as the other Mechanical calculation screens, in the same order and with the same copy: supports
people; overhead or falling hazard; use by or for children; safety-critical load path; pressure; high temperature;
battery containment; medical use; food contact. All NO answers only allow this bounded calculation to proceed and never
mean safe. The screen neither reads nor feeds SafetySignal.

## 9. Result, provenance and fixed disclosure

On success the page shows the inventor-declared `α_avg`, `L_ref` and `ΔT` (echoed verbatim), the calculated `ΔL` in mm
with its exact / rounded label and the sign note, labelled `UNVALIDATED` and `NOT EVIDENCE`, the bounded next-step
wording, the method identity and version, the method sources and unit records the owner carried, the declarations echoed
and this fixed disclosure (English; pinned equal to the artifact):

1. This is the free change in length ΔL that the declared model gives: ΔL = α_avg × L_ref × ΔT, using your own average coefficient α_avg, the reference length L_ref that coefficient refers to, and the temperature change ΔT you declared.
2. It is the change of a length that nothing holds. If the part is clamped, joined or held, or is joined to a part of a different material, the parts try to change length differently, and where that movement is restrained thermal stress can arise. This calculation does not calculate any stress, joint force or deformation.
3. It does not say that any gap, slot, clearance, fit, tolerance or flexible mounting is needed, enough or acceptable, and it says nothing about failure, suitability or safety.
4. The coefficient is your own value. InventorAI did not choose it, look it up or check that it belongs to your material, applies in this direction, is the average over your temperature interval or refers to the length you entered.
5. Only reversible thermal change is included: phase or material changes, permanent set, hysteresis, swelling or shrinking from moisture, and temperature differences within the part are not. ΔT here is a change of the part's temperature over time; it is not the temperature difference across a heat path from another calculation, and no result is carried between calculations.
6. The value is shown exactly when it can be; otherwise it is rounded to 12 significant digits and labelled rounded. The digits follow from your entry; they are not the precision of any measurement. The result is preliminary, advisory, UNVALIDATED and not evidence: check the real movement by measurement or qualified engineering review before any reliance.
7. Reference source material: National Bureau of Standards Circular 486, Thermal Expansion of Solids (Hidnert and Souder, 1950), for the average coefficient of linear thermal expansion and the dependence of the change in length on the original length and the temperature range; NASA Technical Paper 2226 (Blosser and McWithey, 1983) for the point that restrained differential thermal expansion between dissimilar joined materials produces thermal stress; NIST Special Publication 330 for the kelvin and the unit 1/K. The relation as offered here is InventorAI's own restatement, and no data table is used.

**Bounded next-step wording.** The only allowed meaning: this is how much the declared length would change if it were
completely free to move, under the declared model and values; it shows how much movement may need to be accommodated where
the part is held, joined or fitted, and what still has to be checked (the real material's average coefficient over the
real interval, how the part is held or joined, and the real movement by measurement or qualified engineering review). The
page never states that a particular gap, slot, clearance, fit or flexible mounting is required or sufficient.

**Joined-material mismatch boundary.** SRC-032 (`NASA-TE-S2`, §11) supports ONE qualitative disclosure only (item 2):
restrained differential thermal expansion between dissimilar joined materials produces thermal stress. It authorizes no
stress, joint-force, fit, clearance, tolerance or deformation calculation, no difference of two free expansions and no
second material input. The free-expansion method stands without it: removing item 2's second sentence changes no
calculation.

## 9A. Arabic disclosure and UX wording

**A-1 Fixed disclosure (Arabic rendering of the seven §9 items, item by item; no meaning added, removed or softened).**

> 1. هذا هو التغير الحر في الطول ΔL الذي يعطيه النموذج المصرَّح به: ΔL = α_avg × L_ref × ΔT، باستخدام معامل التمدد المتوسط α_avg الذي أدخلته أنت، وطول المرجع L_ref الذي يشير إليه ذلك المعامل، وتغير درجة الحرارة ΔT الذي صرّحت به.
> 2. هذا هو تغير طول لا يقيّده شيء. فإذا كان الجزء مثبّتًا أو موصولًا أو محمولًا، أو موصولًا بجزء من مادة مختلفة، فإن الأجزاء تميل إلى تغيير أطوالها بمقادير مختلفة، وحيث تُقيَّد هذه الحركة قد ينشأ إجهاد حراري (thermal stress). لا يحسب هذا الحساب أي إجهاد أو قوة وصلة أو تشوّه.
> 3. لا يقول هذا الناتج إن أي فجوة أو شق أو خلوص أو توافق أو تفاوت أو تثبيت مرن مطلوب أو كافٍ أو مقبول، ولا يقول شيئًا عن الانهيار أو الملاءمة أو السلامة.
> 4. المعامل قيمتك أنت. لم يختره InventorAI ولم يبحث عنه، ولم يتحقق من أنه يخص مادتك، أو ينطبق في هذا الاتجاه، أو أنه المتوسط على مدى درجات الحرارة لديك، أو أنه يشير إلى الطول الذي أدخلته.
> 5. يُدرَج التغير الحراري القابل للانعكاس فقط: لا تُدرَج تحولات الطور أو المادة، ولا التشوه الدائم، ولا التخلف (hysteresis)، ولا الانتفاخ أو الانكماش بسبب الرطوبة، ولا فروق درجات الحرارة داخل الجزء. ΔT هنا تغير في درجة حرارة الجزء مع الزمن؛ وليس فرق درجة الحرارة عبر مسار حراري من حساب آخر، ولا تُنقَل أي نتيجة بين الحسابات.
> 6. تُعرَض القيمة بدقة عندما يمكن ذلك؛ وإلا تُقرَّب إلى 12 رقمًا معنويًا ويُشار إلى أنها مقرَّبة. تنتج الأرقام من إدخالك؛ وليست دقة أي قياس. النتيجة أولية وإرشادية، وغير مُتحقَّق منها (UNVALIDATED)، وليست دليلًا: تحقق من الحركة الحقيقية بالقياس أو بمراجعة هندسية مؤهلة قبل أي اعتماد عليها.
> 7. المراجع: النشرة رقم 486 للمكتب الوطني للمعايير، التمدد الحراري للمواد الصلبة (NBS Circular 486، هيدنرت وسودر، 1950) لمعامل التمدد الطولي الحراري المتوسط ولاعتماد تغير الطول على الطول الأصلي ومدى درجات الحرارة؛ والورقة الفنية رقم 2226 لوكالة ناسا (NASA Technical Paper 2226، بلوسر وماكويذي، 1983) لكون التمدد الحراري المتباين المقيَّد بين مواد مختلفة موصولة يولّد إجهادًا حراريًا؛ والمنشور الخاص رقم 330 للمعهد الوطني للمعايير والتقنية (NIST SP 330) للكلفن وللوحدة 1/K. أما العلاقة بالصورة المقدَّمة هنا فهي إعادة صياغة خاصة بـInventorAI، ولا يُستخدَم أي جدول بيانات.

**A-2 Applicability declarations (§5).** The inventor answers «ينطبق على حالتي» or «لا ينطبق على حالتي», none pre-selected.

| §5 | Arabic statement |
|---|---|
| D-1 free_unrestrained | الطول المعني حرّ في التمدد والانكماش: لا يثبّته أو يصله أو يحمله أو يقيّده شيء على امتداد هذا الطول أثناء التغير، لذلك يُحسَب تغير طوله الحر فقط. |
| D-2 one_material_uniform_temperature | الطول مادة واحدة متجانسة، بدرجة حرارة واحدة منتظمة في البداية ودرجة حرارة واحدة منتظمة في النهاية، دون فرق في درجة الحرارة على امتداده أو عبره. |
| D-3 own_coefficient | α_avg قيمة المخترع نفسه لهذه المادة؛ لم يختره InventorAI ولم يبحث عنه ولم يستنتجه ولم يتحقق منه، ولا يقرر أنه صحيح. |
| D-4 coefficient_direction | ينطبق α_avg في اتجاه الطول المعني؛ وبالنسبة إلى مادة يعتمد تمددها على الاتجاه (مثل الخشب أو المواد المركّبة الليفية أو البلورات المفردة) فهو المعامل في هذا الاتجاه. |
| D-5 average_over_interval | α_avg هو معامل التمدد الطولي الحراري المتوسط لهذه المادة على مدى درجات الحرارة المعني نفسه تمامًا، من درجة الحرارة الابتدائية إلى النهائية؛ وليس قيمة عند درجة حرارة واحدة تُطبَّق على مدى أوسع، ولا معاملًا معرَّفًا لمدى آخر. |
| D-6 reference_length | L_ref هو الطول الذي يشير إليه α_avg وفق تعريف المعامل نفسه (اصطلاح درجة حرارة المرجع الخاص به، مثل الطول عند درجة الحرارة التي يبدأ عندها مدى المعامل، أو عند درجة حرارة المرجع المذكورة مع المعامل)؛ ولا يقرر InventorAI أي طول هو. |
| D-7 signed_change | ΔT هو درجة الحرارة النهائية مطروحًا منها درجة الحرارة الابتدائية، موجب عند التسخين وسالب عند التبريد؛ وتكون النتيجة ΔL عندئذ موجبة عند الاستطالة وسالبة عند القِصَر. |
| D-8 reversible_thermal_change_only | لا يحدث على هذا المدى إلا تغير حراري في الطول قابل للانعكاس: لا يُدرَج أي تحول في الطور أو المادة، ولا تشوه دائم، ولا تخلف (hysteresis)، ولا تغير بسبب الرطوبة أو المعالجة أو التقادم أو الحمل. |

**A-3 Screen (§8).** The Arabic screen stem, items, answers and note are the existing Mechanical screen copy
(`UI_CAP13_SCREEN_*`), reused unchanged; the integrated-part attribution is the existing `UI_CAP13_PART_*` copy.

**A-4 Right-to-left rendering.** Numbers, the role symbols `α_avg`, `L_ref`, `ΔT` and `ΔL`, the unit tokens `1/K`, `mm` and
`K`, the relation, the method identity and `UNVALIDATED` / `NOT EVIDENCE` are each direction-isolated (`<bdi dir="ltr">`)
on the Arabic page; the inventor's typed values are shown left-to-right.

## 10. Exclusions (binding)

No thermal stress, joint force, fit or tolerance evaluation, clearance adequacy, required gap or slot, flexible-mounting
recommendation, deformation, buckling, failure prediction, suitability or safety conclusion; no difference of two free
expansions and no second material; no material selection, material-property lookup, database, default, example or
prefilled coefficient; no inference of any declaration, coefficient, length or temperature; no instantaneous coefficient,
temperature-dependent coefficient, area or volume expansion, anisotropic tensor, moisture expansion or phase change; no
absolute temperature, no °C entry and no unit conversion; no FEA; no result persistence, result transfer into or from
another calculation (THERM-01 included), report, PDF, Structured Export, API, evidence, readiness, progression, gap or
SafetySignal effect; no AI or provider effect; no Materials domain; no eligibility for any part other than the one declared
Mechanical part (§1), and no inference from a part's name or function. No Stage is entered, completed or reopened.

## 11. Source and source-use status

- **NBS-TE-S1 (SRC-031)** — National Bureau of Standards Circular 486, *Thermal Expansion of Solids*, P. Hidnert and
  W. Souder, issued 15 March 1950 (<https://nvlpubs.nist.gov/nistpubs/Legacy/circ/nbscircular486.pdf>), PDF pages 7
  and 31. Supports, for this method, only the claim of §3 item 1. Directly inspected by the TECH-SOURCES-001 research
  stream (run 10, 2026-10-28; `research/tech-sources-001` at `730fb7b`, source-provenance register row SRC-031 with its
  recorded content hash `64b4f0b841093e50b8edb88dcf15599b9fee28708af976b672f6d721b76ac883`; IP grade `CALCULATION-GRADE`), and supplied for this increment by the
  Owner-authorized MECHANICAL-FREE-LINEAR-THERMAL-EXPANSION-01 brief (2026-10-29). Not independently re-inspected by the
  executor: egress to `nvlpubs.nist.gov` was refused by the environment proxy (2026-10-29). Not reused: the compiled data
  tables (drawn from other authors' publications), figures, examples and every numeric value.
- **NASA-TE-S2 (SRC-032)** — NASA Technical Paper 2226, *Theoretical Basis for Design of Thermal-Stress-Free Fasteners*,
  M. L. Blosser and R. R. McWithey, NASA Langley Research Center, December 1983, NTRS 19840005546
  (<https://ntrs.nasa.gov/citations/19840005546>), abstract. Supports, for this method, only the qualitative disclosure of
  §9 item 2: thermal stress results from differential thermal expansion between dissimilar fastener and sheet materials,
  and a joint stays stress-free only under special conditions (uniform temperature, no friction, a suitably shaped
  fastener). The fastener-shape design method is NOT adopted. Same research-stream inspection (run 10, 2026-10-28; IP grade
  `CALCULATION-GRADE`), same supply, not re-inspected by the executor.
- **NIST-TE-U** — NIST Special Publication 330 (2019 Edition), *The International System of Units (SI)*, Section 2
  (<https://www.nist.gov/pml/special-publication-330/sp-330-section-2>). Supports only the unit facts: the kelvin, symbol
  `K`, is the SI base unit of thermodynamic temperature; a temperature difference may be expressed in kelvin, a difference
  of one kelvin equalling a difference of one degree Celsius; coherent derived units are formed as products and quotients
  of SI units, hence the reciprocal kelvin, written `1/K` — its use for the coefficient of linear thermal expansion is
  InventorAI's own bounded quantity usage of that coherent quotient. Rests on the existing Lead-supplied SP 330 Section 2
  inspections recorded for THERM-01 (THERM-U1, THERM-U3, THERM-U4; 2026-10-08) and for the natural-frequency method
  (NIST-NF-U; 2026-10-29), applied here as this method's own record; location recorded at section level.
- **Source use** (not legal opinions): `mte:SU001` (NBS-TE-S1) — NBS staff-authored publication, a U.S. Government work in
  the United States as recorded by the TECH-SOURCES-001 IP register, used under the NIST Technical Series rights statement
  already recorded in the repository (not subject to U.S. copyright protection; attribution preserved; third-party
  material excluded; no endorsement implied); `mte:SU002` (NASA-TE-S2) — NTRS copyright determination
  `GOV_PUBLIC_USE_PERMITTED`, NASA Langley authors, not contractor-authored, as recorded by the same register (attribution
  preserved; no endorsement implied); `mte:SU003` (NIST-TE-U) — the NIST Technical Series rights statement for SP 330, with
  BIPM-originated material excluded. Owner snapshots: `dcu:SU022` (of `mte:SU001`) and `dcu:SU023` (of `mte:SU003`). Use
  is factual paraphrase and unit identification only. Existing records (`dcu:SU001`, `dcu:SU003`, `dcu:SU021`,
  `THERM-SU-NIST`, `mnf:SU002`) keep their own scopes and are not extended. `SRC-029` is relied upon by nothing.
  TECH-SOURCES-001 is neither waited for nor mutated.

## 12. Implementation boundary

The one existing shared owner executes the method through ONE additional immutable binding created by application wiring
(`_MTE_BINDING` in `web/app.py`), beside the twelve existing bindings; there is no registry, discovery, dynamic module
path or request-selected method (calc/units §13L). Routes: `GET` / `POST /session/<sid>/thermal-expansion`, behind the
central project authorization and the global CSRF guard; the session page shows one optional link on an eligible project.
Eligibility reuses `_calc_gate(sid, consumer)` (§1). The consumer imports no other consumer. Nothing is persisted; the POST
renders its result directly.

## 13. Verification

Focused tests (`tests/test_mechanical_thermal_expansion.py`, `tests/test_mechanical_thermal_expansion_browser.py`): the
adapter against an independent exact-rational oracle and a `decimal`-module oracle for normal, boundary, signed and zero
values and a random sample; the identity `ΔL / (L_ref × ΔT) = α_avg` on the exact decimals; sign preservation; negative
zero; overflow and underflow guards at owner and adapter level; non-finite, invalid and out-of-scope input; unit / method /
version / adapter integrity failing closed; owner artifact v13 integrity (every content-version-12 record unchanged) and
method-artifact tamper; the §7 order and owner correspondence; the exact / rounded display; the Mechanical-root and
declared-Mechanical-part gate with malformed, stale and corrupt compositions failing closed; request integrity, isolation
and no persistence; the twelve existing methods unchanged; EN / AR fidelity, RTL isolation and real-browser EN / AR
journeys at phone width. Hosted required CI on the final PR head is the merge gate.

## 14. STOP conditions

Stop and return to the Owner on a source or IP deficiency, a contract incompatibility, unprovable numerical integrity, a
required broad owner redesign, property framework or generic conversion mechanism, or any scope expansion (another method,
consumer, unit, conversion, material input, eligibility beyond §1, persistence, result transfer or report surface).
