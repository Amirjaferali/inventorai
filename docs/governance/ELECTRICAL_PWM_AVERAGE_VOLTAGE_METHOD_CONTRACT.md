# ELECTRICAL / ELECTRONICS — PWM AVERAGE VOLTAGE METHOD CONTRACT

STATUS: OWNER-AUTHORIZED BOUNDED METHOD CONTRACT — written with, and governing, the one bounded implementation increment
`PWM-AVERAGE-VOLTAGE-01` (Slice 1), which the Owner authorized as ONE bounded implementation and ONE pull request after the
g1-3 NEXT-LOOP selection that followed PR #897. Applicability: this contract governs the delivered method only on the
verified merge of that pull request into `feature/atomic-json-session-persistence`; on its proposal branch it describes an
Owner-authorized proposed method, not a merged or delivered capability. Merge, deployment, general Power Electronics /
Motion (28-T3) activation, any converter, motor-drive, current, ripple, filter, switching-device or actuator capability and
any persistence or sharing of calculation results are NOT authorized by it.
AUTHORITY LEVEL: subordinate to the accepted
[shared deterministic calculation and units owner boundary contract](SHARED_DETERMINISTIC_CALCULATION_AND_UNITS_OWNER_BOUNDARY_CONTRACT.md)
(the "calc/units contract", with its Correction 11, §13J, added by the same increment). It amends no other method contract;
the two-support reactions, THERM-01, planar-moment, rotational-load, TMP36, DC resistive load current, DC resistive load
power, DC resistive load energy, planar required force and DC constant-current charge methods stay unchanged. Where this
document and the calc/units contract differ, the calc/units contract wins and the difference is a defect of this document.

---

## 0. Preserved truth (binding)

- `ACTIVE CONTRACT: NONE` describes the state before and after this increment; this contract fills no active-contract slot
  after delivery and is not a delivery record. Current-truth delivery records belong to a later closure sync.
- This method enters, completes or reopens no Stage and changes no roadmap count (27 of 45 complete). General Power
  Electronics / Motion (28-T3) stays BLOCKED: this increment admits exactly ONE claim-level average-waveform relation
  through the existing owner and creates no 28-T3 owner. D4 and T6 stay inactive, and the Stage 15 composition authority
  is unchanged except for the one narrow eligibility exception of §1.
- The Electrical / Electronics pack, its reference groups (the transistor load-switching reference included) and every
  provenance record in `domains/domain_provenance.json` are unchanged. The DC resistive load current, power and energy
  methods and the DC constant-current charge method are unchanged; this method neither imports nor amends them, shares no
  result with them and reuses none of their sign conventions.

## 1. Purpose and scope

ONE optional, advisory, non-binding, request-local calculation: the arithmetic time-average, over one period, of ONE
explicitly declared ideal periodic two-level voltage waveform — the declared supply level during the on-interval, zero for
the rest of the period, repeating with a fixed period and a fixed on-time. It lets an inventor who knows, from their own
reading, documentation or plan, the supply level, the on-time and the period of such a waveform see its average and the
boundary of what that average means. Nothing is inferred: InventorAI never decides that a project has a switched waveform,
never infers PWM applicability from words such as motor, LED, heater, transistor or switching, from component names or from
project text, and asks no generic question about switching.

Eligibility (method-specific): the SAME `_calc_gate` / `_calc_declared_part` rule as the DC load methods in `web/app.py`: a
project whose trusted durable root domain is exactly `electronics_electrical`, read as the other calculation gates read it
(`_cap12_root_domain`), or, whatever the initial analysis focus, the ONE inventor-declared Electrical / Electronics part of a
valid durable Stage-15 integrated composition (two- or three-part), read only through the store-validated composition and
never from the request; the page names that part with the existing Electrical / Electronics attribution wording. The Stage
15 exception in `engine/subsystem_model.py` names this method. A declared part makes the calculation OFFERED only: it
establishes no waveform, load response, applicability, suitability, validation or safety and supplies no value,
declaration or screen answer. A missing, malformed, corrupt or unreadable composition, or an unreadable root domain, grants
nothing beyond the root rule. The decision is recomputed from the current durable state on every request; the session
link, the page and the submission read the same one decision, so an earlier rendered page grants nothing once that state
no longer admits the project. The inventor explicitly chooses the calculation and supplies its declarations.

## 2. Method identity and version

Identity `electrical:pwm_average_voltage`, version `1.0`. Method-authority artifact
`docs/governance/electrical_content_config/pwm_average_voltage_v1.json` (`electrical_pwm_average_voltage`, artifact
version `1`), separate from every other artifact; none loads another. Adapter `engine/pwm_average_voltage_method.evaluate`;
consumer `engine/pwm_average_voltage.py` (the one named Electrical / Electronics consumer of this method).

## 3. Method definition

`V_avg = V_supply × t_on / T`, with `V_supply` in V, `t_on` and `T` in s and `V_avg` in V, for `V_supply ≥ 0`, `T > 0`
and `0 ≤ t_on ≤ T`, all inputs finite. The waveform equals `V_supply` during `t_on` and zero for the remainder of `T`, and
repeats periodically; the result is ONLY the arithmetic time-average of that declared ideal waveform over one period. NASA
TN D-5643 records that a periodic voltage equal to E for an interval Δt and zero otherwise has an average proportional to
the duty cycle Δt / T (§11); `V_avg = V_supply × t_on / T` is InventorAI's algebraic restatement of that proportionality,
and NASA is not claimed to print InventorAI's method wording.

**Nonnegative-voltage convention (fixed, documented).** `V_supply ≥ 0` only: the admitted waveform switches between `0 V`
and `V_supply`. No signed or bipolar PWM waveform is admitted, a negative `V_supply` is refused, there is no polarity
inference, no reference-direction model and no reuse of another DC method's sign convention. A signed or bipolar waveform
would need its own separate bounded qualification.

**Boundary cases (fixed).** `V_supply = 0` → exactly `+0` V; `t_on = 0` → exactly `+0` V; `t_on = T` → exactly
`V_supply`; the result is never negative, never a negative zero and never above `V_supply`.

**Critical scientific boundary (binding).** `V_avg` is NOT presented as an equivalent steady DC voltage, the voltage a
physical load necessarily experiences, a motor speed, a heating effect, an average power, an RMS voltage, a current, a
torque, a ripple, a filtered output or proof of any load response. Whether a physical load responds approximately according
to the waveform average depends on its dynamics and implementation and is NOT established by this method. The ratio
`t_on / T` exists only inside the product: no duty-cycle quantity, percentage or conversion exists.

## 4. Roles, quantity kinds and exact unit tokens

| Role | Meaning | Quantity kind | Exact unit token |
|---|---|---|---|
| `v_supply` (`V_supply`) | the supply level during the on-interval, as declared; not negative | `voltage` | `V` |
| `t_on` (`t_on`) | the on-interval of each period, as declared; within zero and the period inclusive | `time` | `s` |
| `t_period` (`T`) | the fixed repeating period, as declared; strictly positive | `time` | `s` |
| `v_avg` (`V_avg`) | the arithmetic time-average of the declared waveform over one period; never negative, never above `V_supply` | `voltage` | `V` |

All four roles use existing owner records: `voltage` / `V` (`dcu:U011`) and `time` / `s` (`dcu:U015`). Calc/units
Correction 11 (§13J) adds NO quantity kind, unit token, dimensionless or duty-cycle quantity, percentage, alias or
conversion: `mV`, `kV`, `ms`, `µs`, `Hz`, `kHz` and `%` are unknown tokens, and `h` (the DC constant-current charge token)
is not admitted for this method.

## 5. Applicability declarations (the model-applicability confirmation)

Each is shown as its own statement and answered «applies» or «does not apply», none pre-selected. A missing answer is
`NOT_DECLARED`; «does not apply» is `MODEL_NOT_SUPPORTED`. InventorAI infers none of them; D-1 is the explicit confirmation
of the ideal two-level nonnegative waveform, D-2 of the fixed period and on-time, D-3 that the values are the inventor's own
and inferred from nothing, and D-4 that the quantity wanted is the waveform average and not a load response, DC equivalent,
power, RMS value or current.

| Ref | Id | Accepted statement |
|---|---|---|
| D-1 | `ideal_two_level_waveform` | the waveform being averaged is an ideal two-level voltage: during the on-interval it equals the declared supply level exactly, and for the rest of the period it equals zero exactly; the switch is treated as fully on or fully off, with no rise, fall, dead time, drop, overshoot, ringing or negative excursion; the declared supply level is zero or positive and the waveform never goes below zero |
| D-2 | `fixed_period_and_on_time` | the waveform repeats with one fixed period and one fixed on-time, both the same in every cycle; no varying, modulated, bursting, drifting or one-off timing is being averaged |
| D-3 | `declared_values` | the supply level, on-time and period entered are the inventor's own values for this one waveform, taken from their own reading, documentation or plan; InventorAI did not measure or check them and infers none of them from any component, circuit or project text |
| D-4 | `waveform_average_wanted` | the quantity wanted is the arithmetic time-average of that declared waveform over one cycle, and nothing more: not an equivalent steady DC voltage, not the voltage a load experiences, not a motor speed, heating effect, average power, RMS voltage, current, torque, ripple or filtered output, and not a statement about how any load responds |

## 6. Numeric domain and numerical acceptance (method-specific, explicit)

- **Grammar (strict capture).** For `V_supply`, `t_on` and `T` alike: an optional single leading minus, then one to nine
  integer digits and an optional single fractional part of one to nine digits. No plus sign, exponent, separator, space,
  Unicode digit, unit suffix, percentage, `inf`, `nan` or normalization. A field sent twice, an unknown field or a
  declaration / screen answer outside its closed choices makes the whole request malformed (a bare 400). An omitted,
  malformed or over-length value is `INVALID_NUMERIC_INPUT`.
- **Representation limits are not physical limits.** `V_supply` from `0` to below `10^9` V; `t_on` and `T` from `0` to
  below `10^9` s; steps of `10^-9`. They are NOT physical limits, equipment ratings, switching-frequency limits or a claim
  that such values are realistic. The 64-character field cap is abuse protection only — a NON-PHYSICAL bound.
- **Exact-decimal screening before binary conversion, in this order, each with no number.** The EXACT decimal value of
  `V_supply` must not be negative (`VOLTAGE_NEGATIVE`); then the EXACT decimal value of `T` must be greater than zero
  (`PERIOD_NOT_POSITIVE`); then the EXACT decimal value of `t_on` must not be negative (`ON_TIME_NEGATIVE`); then the EXACT
  decimal value of `t_on` must not exceed `T` (`ON_TIME_EXCEEDS_PERIOD`). A zero `V_supply` or `t_on` (including `-0`) is
  admitted and gives exactly `0` V; `t_on = T` is admitted and gives exactly `V_supply`.
- **Binary bridge (one conversion per input).** Each admitted decimal is converted ONCE to the correctly rounded binary64
  value (round half to even) and handed to the owner as a typed number; the owner parses no string (calc/units §10). Every
  admitted nonzero value lies between `10^-9` and `10^9` in magnitude, so it is a normal binary64 number with relative
  rounding error at most `2^-53`; an exact zero converts to `+0.0`; equal decimals (`t_on = T`) convert to equal binary64
  values.
- **Owner applicability.** The method record declares the existing `greater_than_zero` on `t_period` and the existing
  `within_zero_and_role` on `t_on` bound to `t_period` (inclusive at both ends); a value that reaches the owner outside them
  is `UNABLE_TO_DETERMINE / INPUT_OUTSIDE_ADMITTED_RANGE`, shown as the neutral `UNMAPPED_OWNER_OUTCOME` (unreachable from
  the page). The vocabulary has no not-negative condition and none is added: a negative `v_supply` that reaches the adapter
  is refused there as `FAILURE / EXECUTION_INTEGRITY_FAILURE` (unreachable from the page). No result range is declared.
- **Binary acceptance (adapter).** The exact rational value `v_supply × t_on / t_period` of the binary inputs is rounded
  ONCE to binary64. A zero `v_supply` or `t_on` (`0.0` or `-0.0`) gives exactly `+0.0`; `t_on = t_period` gives the exact
  rational `v_supply`, hence exactly the binary64 `v_supply`. A nonzero exact result is accepted only when the rounded
  value is finite, positive and `|V_avg − exact| ≤ 2^-52 · exact` (one correct rounding gives at most `2^-53`). Overflow,
  underflow of a nonzero result or any failed check is `FAILURE / EXECUTION_INTEGRITY_FAILURE` with no numerical payload,
  displayed as `KNOWLEDGE_UNAVAILABLE`, never rewritten as a refusal. Representability: inside the representation limits
  every nonzero result lies between `10^-27` V (`10^-9 × 10^-9 / 10^9`) and `10^9` V, well inside the normal binary64
  range, so neither overflow nor underflow can occur from the page; the guards stay in place for direct owner use.
- **Decimal-reference acceptance (consumer; independent oracle).** A successful owner result is shown only when its echoed
  output token is the method's own `V` (§4) and it agrees with the exact decimal value `V_supply × t_on / T` of the ENTERED decimals: exactly `+0` when, and only when, `V_supply`
  or `t_on` is exactly zero; otherwise positive, not above the binary64 `V_supply`, and within a relative error of `2^-50`.
  Proof that the bound always holds: with `u = 2^-53`, the binary inputs are `V(1 + e₁)`, `t_on(1 + e₂)` and `T(1 + e₃)`
  with `|eᵢ| ≤ u`, so the exact binary-input result is `(V × t_on / T) · (1 + e₁)(1 + e₂) / (1 + e₃)`, and the single
  rounding multiplies it by `(1 + e₄)`, `|e₄| ≤ u`. The total relative error is at most `(1 + u)³ / (1 − u) − 1 = 4u + O(u²)
  < 4.0000001 · u < 8u = 2^-50` (the lower side, `1 − (1 − u)³ / (1 + u)`, is smaller). Both sides are checked exactly in
  rational arithmetic by the focused tests. A failed check is `KNOWLEDGE_UNAVAILABLE` with no number.
- **Negative zero.** A negative zero is never displayed: the adapter returns `+0.0` for a zero factor and the consumer's
  acceptance rejects any value whose sign bit is set.
- **Non-finite.** A non-finite or non-numeric typed value is refused by the owner (`REFUSAL / INVALID_NUMERIC_INPUT`) and by
  the adapter (`ArithmeticError` → integrity failure); from the page the grammar already refuses `inf` and `nan`.
- **Display.** The shown value is derived from the exact decimal value, never from the binary value: rounded ONCE to 12
  significant digits, round half to even, with trailing zeros removed. It is labelled **exact** when that rounding changes
  nothing and **rounded to 12 significant digits** otherwise (`12 V`, `0.25 s`, `1 s` shows `3`, exact; `12 V`, `1 s`,
  `1 s` shows `12`, exact; `12 V`, `1 s`, `3 s` shows `4`, exact; `5 V`, `1 s`, `3 s` shows `1.66666666667`, rounded).
  Plain decimal notation is used for `10^-6 ≤ V_avg < 10^12` V and the form `m × 10^e` otherwise, so a tiny nonzero average
  is never shown as `0` (`0.000000001 V` for `0.000000001 s` of `999999999.999999999 s` shows `1 × 10^-27`, rounded). The digits shown imply no measurement resolution, precision or accuracy.
- These rules belong to this method only; none is a generic owner numerical policy. The contract, the consumer, the
  adapter and the focused tests agree exactly on each of them.

## 7. Refusal and abstention semantics

Order after request integrity (CSRF), project authorization, eligibility and strict capture (a malformed request is a bare
400 with no reason token): (1) completeness — every declaration and screen item answered, else `NOT_DECLARED`; (2) screen
— any YES is `ENGINEERING_REVIEW_REQUIRED` and the owner is not invoked; (3) declarations — any «does not apply» is
`MODEL_NOT_SUPPORTED`; (4) numeric grammar — `INVALID_NUMERIC_INPUT`; (5) supply level not negative — `VOLTAGE_NEGATIVE`;
(6) period positive — `PERIOD_NOT_POSITIVE`; (7) on-time not negative — `ON_TIME_NEGATIVE`; (8) on-time not above the
period — `ON_TIME_EXCEEDS_PERIOD`; (9) the shared owner; (10) the decimal-reference acceptance — `KNOWLEDGE_UNAVAILABLE`.
A method artifact that is missing, unreadable or changed is `KNOWLEDGE_UNAVAILABLE` before any of these. The first failing
stage alone decides; no refusal carries a number. Owner correspondence: `REFUSAL / INVALID_NUMERIC_INPUT` →
`INVALID_NUMERIC_INPUT`; `REFUSAL / UNIT_NOT_ADMITTED` or `UNKNOWN_UNIT` → `UNIT_NOT_SUPPORTED`;
`REFUSAL / METHOD_NOT_REGISTERED` or `VERSION_MISMATCH`, `UNABLE / SOURCE_UNAVAILABLE` and
`FAILURE / EXECUTION_INTEGRITY_FAILURE` → `KNOWLEDGE_UNAVAILABLE`; any other owner state → the neutral
`UNMAPPED_OWNER_OUTCOME`. The owner state and token are preserved, never rewritten.

## 8. High-risk screen (declared; not a safety engine)

Six items, answered yes or no, none pre-selected — whether the switched circuit, its power source or the load it drives is
or is part of: mains or high voltage; a battery or energy-storage cell; fire, ignition or overheating risk; medical or
life-supporting use; vehicle or aerospace use; a safety function, alarm, protection or shut-off. The items and their
wording are those of the DC load methods. All NO answers only allow this bounded calculation to proceed and never mean safe.
The screen neither reads nor feeds SafetySignal.

## 9. Result, provenance and fixed disclosure

On success the page shows `V_avg` in V with its exact / rounded label under the heading "Average of this PWM voltage
waveform", the declared inputs as entered with their units, the stated assumptions (D-1 to D-4), the labels `UNVALIDATED`
and `NOT EVIDENCE`, the statement that the result is the waveform average only and not an equivalent DC voltage or a load
response, the statement that `V_avg` is not to be entered into the DC resistive load calculations as a steady voltage, the
method identity and version, the method source and unit records the owner carried, and this fixed disclosure (English;
pinned equal to the artifact). Item 6 carries the next engineering need.

1. For the ideal repeating voltage waveform you declared, InventorAI calculated its time-average over one cycle: V_avg = V_supply × t_on / T, in volts. This is the average of this PWM voltage waveform and nothing more.
2. The supply level, on-time and period are your own declared values. InventorAI did not measure them. The waveform is taken as an ideal switch: either exactly your declared supply level or exactly zero, with one fixed period and one fixed on-time in every cycle, and it never goes below zero.
3. No physical load response is inferred. Whether a load responds approximately to this average depends on that load's dynamics and on how the switching is implemented, which InventorAI has not established. For an inductive load such as a motor winding, the recorded context is that the switching period must be much shorter than the winding's electrical time constant and that a free-wheeling path keeps the current continuous; that is context for inductive loads only, not a condition of this average.
4. No current, ripple, average power, RMS voltage, torque, speed, heating or temperature is calculated, and no switching frequency, filter, free-wheeling component, driver or switching device is recommended or checked.
5. Do not enter V_avg into the DC resistive load current, power or energy calculations as though it were a steady DC voltage: for a switched resistive load this method does not establish the average power as V_avg² / R, and no result is carried from one calculation into another.
6. The value is shown exactly when it can be; otherwise it is rounded to 12 significant digits and labelled rounded. The digits follow from your entry; they are not the precision of any measurement. Next engineering need: whether this average means anything for your load, what current, power, ripple and heating actually result, and whether the switch, wiring and supply are rated for them all remain unverified, and must be checked by measurement or a qualified person before any reliance. The result is preliminary, advisory, UNVALIDATED and not evidence.
7. Reference source material: NASA TN D-5643, Design and Performance Analysis of a Medium-Power DC-DC Converter (NASA Lewis Research Center, 1970), for the average value of a periodic two-level voltage, and NASA Marshall Space Flight Center, Traction Drive System Design Considerations for a Lunar Roving Vehicle (1969), for the inductive-load context only. V_avg = V_supply × t_on / T is InventorAI's own restatement, and no NASA text, figure, circuit or example is reproduced. NASA does not endorse InventorAI or this calculation.

## 9A. Arabic disclosure and UX wording

**A-1 Fixed disclosure (Arabic rendering of the seven §9 items, item by item; no meaning added, removed or softened).**

> 1. لموجة الجهد المتكررة المثالية التي صرّحت بها، حسب InventorAI متوسطها الزمني على مدى دورة واحدة: V_avg = V_supply × t_on / T، بالفولت. هذا هو متوسط موجة جهد PWM هذه ولا شيء أكثر.
> 2. مستوى التغذية وفترة التشغيل والدورة قيم صرّحت بها أنت. لم يقسها InventorAI. وتُؤخذ الموجة على أنها مفتاح مثالي: إما مستوى التغذية الذي صرّحت به تمامًا وإما الصفر تمامًا، بدورة واحدة ثابتة وفترة تشغيل واحدة ثابتة في كل دورة، ولا تنزل أبدًا تحت الصفر.
> 3. لا تُستنتج أي استجابة لحِمل فيزيائي. وما إذا كان حِمل يستجيب تقريبًا لهذا المتوسط يعتمد على ديناميكيات ذلك الحِمل وعلى كيفية تنفيذ التبديل، وهو ما لم يثبته InventorAI. وللحِمل الحثّي مثل ملف محرك، السياق المسجَّل هو أن دورة التبديل يجب أن تكون أقصر بكثير من الثابت الزمني الكهربائي للملف، وأن مسار الدوران الحر (free-wheeling) يُبقي التيار متصلًا؛ وهذا سياق للأحمال الحثّية فقط، وليس شرطًا لهذا المتوسط.
> 4. لا يُحسب أي تيار ولا تموّج (ripple) ولا متوسط قدرة ولا جهد فعّال (RMS) ولا عزم ولا سرعة ولا تسخين ولا درجة حرارة، ولا يُوصى بأي تردد تبديل أو مرشِّح أو مكوّن دوران حر أو مُشغِّل (driver) أو عنصر تبديل ولا يُفحص.
> 5. لا تُدخل V_avg في حسابات تيار الحِمل المقاوم على جهد مستمر أو قدرته أو طاقته كما لو كان جهدًا مستمرًا ثابتًا: فللحِمل المقاوم المبدَّل بـ PWM لا تثبت هذه الطريقة أن متوسط القدرة يساوي V_avg² / R، ولا تُنقل أي نتيجة من حساب إلى آخر.
> 6. تُعرض القيمة بدقة حين يمكن ذلك؛ وإلا تُقرَّب إلى 12 رقمًا معنويًا ويُشار إلى أنها مقرَّبة. الأرقام ناتجة عن إدخالك؛ وليست دقة أي قياس. الحاجة الهندسية التالية: ما إذا كان هذا المتوسط يعني شيئًا لحِملك، وما التيار والقدرة والتموّج والتسخين الناتجة فعلًا، وما إذا كان المفتاح والأسلاك والتغذية مُصنَّفة لها — كلها تبقى غير مُتحقَّق منها، ويجب فحصها بالقياس أو بواسطة شخص مؤهل قبل أي اعتماد. هذه النتيجة أولية وإرشادية، وغير مُتحقَّق منها (UNVALIDATED)، وليست دليلًا.
> 7. المراجع: NASA TN D-5643، ‏Design and Performance Analysis of a Medium-Power DC-DC Converter ‏(NASA Lewis Research Center، 1970)، للقيمة المتوسطة لجهد دوري ذي مستويين؛ وNASA Marshall Space Flight Center، ‏Traction Drive System Design Considerations for a Lunar Roving Vehicle ‏(1969)، لسياق الحِمل الحثّي فقط. وV_avg = V_supply × t_on / T إعادة صياغة من InventorAI، ولا يُستنسخ أي نص أو شكل أو دائرة أو مثال من NASA. لا تؤيّد NASA InventorAI ولا هذا الحساب.

**A-2 Applicability declarations (§5).** The inventor answers «ينطبق على حالتي» or «لا ينطبق على حالتي», none pre-selected.

| §5 | Arabic statement |
|---|---|
| D-1 ideal_two_level_waveform | الموجة التي يُحسب متوسطها جهد مثالي ذو مستويين: خلال فترة التشغيل تساوي مستوى التغذية المصرّح به تمامًا، وفي بقية الدورة تساوي الصفر تمامًا؛ ويُعامل المفتاح على أنه في وضع التشغيل التام أو الإيقاف التام، دون زمن صعود أو هبوط أو زمن ميت (dead time) أو هبوط جهد أو تجاوز أو رنين أو انحراف سالب؛ ومستوى التغذية المصرّح به صفر أو موجب، ولا تنزل الموجة أبدًا تحت الصفر. |
| D-2 fixed_period_and_on_time | تتكرر الموجة بدورة واحدة ثابتة وفترة تشغيل واحدة ثابتة، وكلتاهما نفسها في كل دورة؛ ولا يُحسب متوسط أي توقيت متغير أو مُعدَّل أو متقطع أو منحرف أو غير متكرر. |
| D-3 declared_values | مستوى التغذية وفترة التشغيل والدورة المُدخلة قيمك أنت لهذه الموجة الواحدة، مأخوذة من قراءتك أو من وثائقك أو من خطتك؛ ولم يقسها InventorAI ولم يتحقق منها، ولا يستنتج أيًّا منها من أي مكوّن أو دائرة أو نص في المشروع. |
| D-4 waveform_average_wanted | الكمية المطلوبة هي المتوسط الزمني الحسابي لتلك الموجة المصرّح بها على مدى دورة واحدة، ولا شيء أكثر: ليست جهدًا مستمرًا مكافئًا ثابتًا، ولا الجهد الذي يتعرض له حِمل، ولا سرعة محرك ولا أثر تسخين ولا متوسط قدرة ولا جهدًا فعّالًا (RMS) ولا تيارًا ولا عزمًا ولا تموّجًا (ripple) ولا خرجًا مرشَّحًا، ولا عبارة عن كيفية استجابة أي حِمل. |

**A-3 Screen (§8).**

| §8 | Arabic item |
|---|---|
| mains_or_high_voltage | جهد الشبكة الكهربائية (mains) أو جهد عالٍ |
| battery_or_storage_cell | بطارية أو خلية لتخزين الطاقة |
| fire_or_overheating | خطر حريق أو اشتعال أو سخونة زائدة |
| medical_or_life_supporting | استخدام طبي أو داعم للحياة |
| vehicle_or_aerospace | استخدام في المركبات أو في الطيران والفضاء (aerospace) |
| safety_function | وظيفة سلامة أو إنذار أو حماية أو إيقاف |

**A-4 Right-to-left rendering.** Numbers, the role symbols `V_supply`, `t_on`, `T` and `V_avg`, the unit tokens `V` and
`s`, the relation `V_avg = V_supply × t_on / T`, the expression `V_avg² / R`, the method identity and `UNVALIDATED` /
`NOT EVIDENCE` are each direction-isolated on the Arabic page; the inventor's typed values are shown left-to-right, so a
leading minus stays attached to its number.

## 10. Exclusions (binding)

No general Power Electronics / Motion (28-T3) activation and no 28-T3 owner; no converter (buck, boost or other), motor-drive,
motor-speed, torque, actuator or actuator-selection result; no current, average power, RMS voltage, ripple magnitude,
heating or temperature result; no equivalent steady DC voltage and no statement that any load experiences or responds to
the average; no switching-frequency recommendation, automatic time-constant comparison, filter, free-wheeling component
selection, driver design, switching-device sizing, switching loss or dead time; no duty-cycle quantity, percentage input or
unit conversion (`mV`, `kV`, `ms`, `µs`, `Hz`, `kHz`, `%`); no signed or bipolar waveform; no inference of the waveform, its
levels, its timing or any declaration from any component, circuit or project text, and no generic switching question; no
result handoff to the DC resistive load current, power or energy calculations or to any other calculation; no persistence,
result retention, report, PDF, Structured Export, API, evidence, readiness, progression, gap or SafetySignal effect; no AI
or provider call; Stage 15 part eligibility only as stated in §1.

## 11. Source and IP status

- **NASA-PWM-S1 — numerical relation basis.** NASA TN D-5643, *Design and Performance Analysis of a Medium-Power DC-DC
  Converter* (A. G. Birchenough and F. Gourash, NASA Lewis Research Center, February 1970; NTRS 19700009882; printed
  pages 3, 4 and 6, PDF pages 5, 6 and 8): a periodic voltage equal to E for an interval Δt and zero for the rest of the
  period has an average value proportional to the duty cycle Δt / T. `V_avg = V_supply × t_on / T` is InventorAI's
  algebraic restatement of that relationship; it is not claimed that NASA prints InventorAI's exact method wording. The
  report's filtered-output, ripple, output-impedance and circuit statements are NOT used. This record reuses the direct
  primary-source inspection of the TECH-SOURCES-001 research stream (run 13, 2026-10-28; research record SRC-042: NTRS
  `GOV_PUBLIC_USE_PERMITTED`, no contractor or third-party material, NASA Lewis authors), recorded as Lead-supplied for this
  method; not re-inspected by the executor (NTRS egress is not available from the execution environment).
- **NASA-PWM-S2 — inductive-load applicability context only.** NASA Marshall Space Flight Center, *Traction Drive System
  Design Considerations for a Lunar Roving Vehicle* (C. S. Jones Jr., B. J. Doran and F. J. Nola, 25 November 1969; NTRS
  19700009492; printed pages 14 to 17, PDF pages 21 to 24): in its motor-winding context, the switching period must be much
  shorter than the winding's electrical time constant, and a free-wheeling path allows inductive current continuity and
  smoothing. The report's worked example only implies, and does not state, average voltage = duty × supply, so it is NOT
  the numerical basis. These statements are surfaced to the inventor explicitly as inductive-load context, are NOT
  generalised as conditions for computing the waveform average, and no time-constant comparison, free-wheeling component,
  motor, drive or current statement is derived from them. This record reuses the research-stream inspection of run 7,
  2026-10-27 (SRC-018: NTRS `GOV_PUBLIC_USE_PERMITTED`, no contractor or third-party material, NASA MSFC authors), recorded
  as Lead-supplied for this method; not re-inspected by the executor.
- **Units** — `V` and `s`: the owner records `dcu:U011` (NIST SP 811 Appendix B.9, as recorded in
  `electronics_electrical:PR005`; owner source use `dcu:SU011`) and `dcu:U015` (NIST SP 811 Chapter 4, Table 1; owner source
  use `dcu:SU014`), unchanged. No new unit record is created.
- **Source use** (not a legal opinion): `pwm:SU001` (owner snapshot `dcu:SU019`) — U.S. Government works are generally not
  protected by copyright in the United States (17 U.S.C. 105); NASA-hosted material may contain privately created content,
  assessed separately; NASA material may not be used to imply endorsement; the NTRS records of both reports carry
  `GOV_PUBLIC_USE_PERMITTED` with no contractor or third-party material (TECH-SOURCES-001 IP and reuse register rows
  SRC-042 and SRC-018). Use is one factual relationship and two context statements only, restated in InventorAI's own
  words; the product form, the nonnegative-voltage convention, the ordered screening and the boundary cases are
  InventorAI's own statement; the mathematics is implemented independently; no NASA prose, worked example, figure, circuit
  diagram, table, photograph or logo is copied; no external modelling library or code is used; NASA is acknowledged
  neutrally and no endorsement is stated or implied. No patent, freedom-to-operate, trademark or contractual clearance is
  claimed. The CAP-13 NASA STI snapshots `dcu:SU002`, `dcu:SU005` and `dcu:SU016` are not extended to this method.

## 12. Implementation boundary

The one existing shared owner executes the method through ONE additional immutable binding created by application wiring
(`_PWM_AVERAGE_VOLTAGE_BINDING` in `web/app.py`), beside the ten existing bindings; there is no registry, discovery, dynamic
module path or request-selected method (calc/units contract §13J). Routes: `GET` / `POST /session/<sid>/pwm-average-voltage`,
behind the central project authorization and the global CSRF guard; the session page shows one optional link on an eligible
project. Nothing is persisted; the POST renders its result directly. The owner change is one ordinary method record and one
source-use snapshot in its artifact plus one entry in its closed method inventory; no owner rule, kind, token, exception or
validation path is changed.

## 13. Verification

Focused tests (`tests/test_pwm_average_voltage.py`, `tests/test_pwm_average_voltage_browser.py`): the reference vectors
`12 V / 0.25 s / 1 s = 3 V`, `5 V / 0.5 s / 2 s = 1.25 V`, `3.3 V / 0.001 s / 0.004 s = 0.825 V` and `24 V / 1 s / 1 s =
24 V`; `V_supply = 0` and `t_on = 0` (and their negative zeros) giving exactly `+0` V; `t_on = T` giving exactly `V_supply`;
exact and rounded results; `V_supply < 0`, `T ≤ 0`, `t_on < 0` and `t_on > T` refused before the owner, each with its own
reason and no number, in the contracted order; negative and out-of-range inputs failing closed in the adapter and owner;
non-finite and non-numeric inputs refused; overflow and underflow failing closed in the adapter; representation-limit
values; an independent exact-rational oracle over a random sample; the exact rational check of the `2^-50` proof; the
negative-zero guard; missing, malformed, duplicate and contradictory declarations; grammar (no percentage, frequency or
unit suffix); unit, method, version, adapter and artifact integrity with no new kind, token or conversion; owner artifact
content version 11 with every content-version-10 record unchanged; the §7 order and owner correspondence; eligibility
(root and declared part; a Mechanical root ineligible; nothing inferred from the request); CSRF, authorization, request
isolation and no persistence; the ten existing methods unchanged; the explicit no-equivalent-DC and no-power-substitution
wording on every surface; EN / AR fidelity; and real-browser EN / AR success and refusal journeys. Hosted required CI is
the merge gate.

## 14. STOP conditions

Stop and return to the Owner on a source or IP deficiency, a need to incorporate external code or content, a contract
incompatibility, unprovable numerical integrity, any owner change beyond one ordinary method record and binding, an
unqualified load-response, equivalent-DC, power, RMS, current, ripple, motor, filter, frequency, suitability or safety
claim, or any scope expansion (bipolar waveform, converter, drive, current, ripple, filter, percentage or duty-cycle
quantity, result transfer, persistence or report surface).
