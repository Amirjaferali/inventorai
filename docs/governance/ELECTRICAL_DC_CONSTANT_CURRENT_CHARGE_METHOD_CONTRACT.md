# ELECTRICAL / ELECTRONICS — DC CONSTANT-CURRENT CHARGE METHOD CONTRACT

STATUS: OWNER-AUTHORIZED BOUNDED METHOD CONTRACT — written with, and governing, the one bounded implementation increment
`DC-CONSTANT-CURRENT-CHARGE-01` (Slice 1), which the Owner authorized as ONE bounded implementation and ONE pull request
(Option A of the g1-3 NEXT-LOOP recommendation after PR #896). Applicability: this contract governs the delivered method
only on the verified merge of that pull request into `feature/atomic-json-session-persistence`; on its proposal branch it
describes an Owner-authorized proposed method, not a merged or delivered capability. Merge, deployment, Battery / BMS
capability, Power Electronics / Motion (28-T3), D4 or T6 activation, any battery sizing, selection, runtime or rating
comparison and any persistence or sharing of calculation results are NOT authorized by it.
AUTHORITY LEVEL: subordinate to the accepted
[shared deterministic calculation and units owner boundary contract](SHARED_DETERMINISTIC_CALCULATION_AND_UNITS_OWNER_BOUNDARY_CONTRACT.md)
(the "calc/units contract", with its Correction 10, §13I, added by the same increment). It amends no other method contract;
the two-support reactions, THERM-01, planar-moment, rotational-load, TMP36, DC resistive load current, DC resistive load
power, DC resistive load energy and planar required force methods stay unchanged. Where this document and the calc/units
contract differ, the calc/units contract wins and the difference is a defect of this document.

---

## 0. Preserved truth (binding)

- `ACTIVE CONTRACT: NONE` describes the state before and after this increment; this contract fills no active-contract slot
  after delivery and is not a delivery record. Current-truth delivery records belong to a later closure sync.
- This method enters, completes or reopens no Stage and changes no roadmap count (27 of 45 complete). Power Electronics /
  Motion (28-T3) stays BLOCKED, Battery / BMS stays R2 and RECORDED only, D4 and T6 stay inactive, and the Stage 15
  composition authority is unchanged except for the one narrow eligibility exception of §1.
- The Electrical / Electronics pack claims `charge_current_time_reference`, `charge_unit_discipline` and
  `ampere_hour_charge_unit`, their reference-fundamentals group `electric_charge_reference_v1` and the provenance records
  `electronics_electrical:PR018` to `PR021` are unchanged and keep their own scope (§11). The DC resistive load current,
  power and energy methods are unchanged; this method neither imports nor amends them, and it shares no result with them.

## 1. Purpose and scope

ONE optional, advisory, non-binding, request-local calculation: the electric charge that flows through ONE explicitly
declared load while ONE declared DC current stays constant for ONE declared duration, `Q = I × t`, given in ampere hours.
It lets an inventor who knows, from their own reading, documentation or plan, the constant current one load draws and how
long it flows see the charge the ideal relation gives, in the unit battery ratings are written in, together with its limits
and the engineering checks that still remain — above all that this charge is not an energy, not a battery capacity, not a
runtime, not a state of charge and not a comparison with any rating. Nothing is inferred: InventorAI never decides that a
project has such a load, that a current is constant or how long it flows, and asks no generic question about loads or
batteries.

Eligibility (method-specific): the SAME `_calc_gate` / `_calc_declared_part` rule as the DC resistive load current, power
and energy methods in `web/app.py`: a project whose trusted durable root domain is exactly `electronics_electrical`, read
as the other calculation gates read it (`_cap12_root_domain`), or, whatever the initial analysis focus, the ONE
inventor-declared Electrical / Electronics part of a valid durable Stage-15 integrated composition (two- or three-part),
read only through the store-validated composition and never from the request; the page names that part with the existing
Electrical / Electronics attribution wording. The Stage 15 exception in `engine/subsystem_model.py` names this method. A
declared part makes the calculation OFFERED only: it establishes no load, no current constancy, no applicability,
suitability, validation or safety and supplies no value, declaration or screen answer. A missing, malformed, corrupt or
unreadable composition, or an unreadable root domain, grants nothing beyond the root rule. The decision is recomputed from
the current durable state on every request; the session link, the page and the submission read the same one decision, so
an earlier rendered page grants nothing once that state no longer admits the project. Nothing is inferred from inventor
text, classifier signals, component names or any project value.

## 2. Method identity and version

Identity `electrical:dc_constant_current_charge`, version `1.0`. Method-authority artifact
`docs/governance/electrical_content_config/dc_constant_current_charge_v1.json`
(`electrical_dc_constant_current_charge`, artifact version `1`), separate from every other artifact; none loads another.
Adapter `engine/dc_constant_current_charge_method.evaluate`; consumer `engine/dc_constant_current_charge.py` (the one
named Electrical / Electronics consumer of this method).

## 3. Method definition

`Q = I × t`, with `I` in A, `t` in h and `Q` in A·h, for `I ≥ 0` and `t ≥ 0`, ONLY for a current that stays constant
throughout `t`. Electric current is the flow of electric charge, one ampere being one coulomb of charge passing a point per
second (the DOE Electrical Science handbook, §11); InventorAI restates that identification as current being the rate of
electric charge flow and, for a constant current only, as the algebraic product `Q = I × t`. The handbook is not claimed to
print `Q = I × t` (the integrated form), and no varying-current, average-current, duty-cycle or integration treatment is
derived. With `I` in amperes and `t` in hours the product is in ampere hours, the unit the request declares and the owner
returns; no conversion is performed anywhere.

**Constant-current assumption (fixed, documented).** `Q = I × t` holds only when the current stays the same for the whole
declared duration (D-1, D-2, D-4). InventorAI does not establish constancy: a current that changes, duty cycling, standby or
sleep phases, start-up or inrush current, switching and AC are outside the method.

**Non-negativity (fixed, documented).** `I ≥ 0` and `t ≥ 0`; the charge is never negative, exactly zero for `I = 0` or
`t = 0`, and a negative zero current or duration gives exactly `+0` A·h, never `−0`.

The result is the charge of that ideal relation only — the charge that flows through the declared load during the declared
constant-current duration: a charge and not an energy; never a measured, rated, stored, available or deliverable charge;
never a battery capacity, a statement of what any battery must hold, a runtime, a state of charge, a battery or source sizing, selection or
suitability, and never compared with any rating. The ampere hour is a unit of electric charge that battery ratings also use;
naming that fact is the whole of what this method says about batteries.

## 4. Roles, quantity kinds and exact unit tokens

| Role | Meaning | Quantity kind | Exact unit token |
|---|---|---|---|
| `i_load` (`I`) | the constant DC current through the load, as declared; not negative | `electric_current` | `A` |
| `t_duration` (`t`) | the duration at that constant current, as declared, in hours; not negative | `time` | `h` |
| `q_load` (`Q`) | the charge that flows through the load during the declared duration; never negative | `electric_charge` | `A·h` (A, U+00B7, h) |

`electric_current` / `A` already exists in the shared owner (calc/units §13E, record `dcu:U013`). `electric_charge` /
`A·h` (record `dcu:U017`) is the ONE kind added, and `h` (record `dcu:U016`) is the ONE further token of the EXISTING
`time` kind, beside the DC resistive load energy's `s`, under the second named token exception of calc/units Correction 10
(§13I): each role binds exactly one token, a request in the other is refused, and nothing maps `h` to `s`. No unit is
converted: `A·h` is not related to `C`, `mA·h`, `Ah`, `J` or `W·h` (the NIST factor `1 A · h = 3.6 × 10³ C` is recorded
for unit identification only and is never applied), and `h` to no second, minute or day.

## 5. Applicability declarations (the model-applicability confirmation)

Each is shown as its own statement and answered «applies» or «does not apply», none pre-selected. A missing answer is
`NOT_DECLARED`; «does not apply» is `MODEL_NOT_SUPPORTED`. InventorAI infers none of them; D-1 is the explicit confirmation
that the current is constant for the whole duration, D-2 that the values are the inventor's own and that InventorAI does
not establish constancy, D-3 that the quantity wanted is a charge and not a battery or energy result, and D-4 that one load
and one continuous period are described.

| Ref | Id | Accepted statement |
|---|---|---|
| D-1 | `constant_dc_current` | the current through the load is a DC current that stays at the one value entered for the whole declared duration; no changing, pulsed, duty-cycled, intermittent, start-up, inrush, switching or AC current is being calculated |
| D-2 | `declared_values` | the current and the duration entered are the inventor's own values for this one load, taken from their own reading, documentation or plan; InventorAI did not measure or check them and does not establish that the current is constant |
| D-3 | `charge_through_load` | the quantity wanted is the electric charge that flows through this one load during that one duration, not a battery capacity, a runtime, a state of charge, an energy or a choice of battery or source |
| D-4 | `single_load_single_period` | one load and one continuous period at that one current are being described; several loads, several periods, standby or sleep phases and any other current are not combined into this value |

## 6. Numeric domain and numerical acceptance

- **Grammar (strict capture).** For `I` and `t` alike: an optional single leading minus, then one to nine integer digits
  and an optional single fractional part of one to nine digits. No plus sign, exponent, separator, space, Unicode digit,
  unit suffix, `inf`, `nan` or normalization. A field sent twice, an unknown field or a declaration / screen answer outside
  its closed choices makes the whole request malformed (a bare 400). An omitted, malformed or over-length value is
  `INVALID_NUMERIC_INPUT`.
- **Representation limits are not physical limits.** `I` from `0` to below `10^9` A; `t` from `0` to below `10^9` h; steps
  of `10^-9`. They are NOT physical limits, equipment ratings, operating times or a claim that such values are realistic.
  The 64-character field cap is abuse protection only — a NON-PHYSICAL bound.
- **Current not negative, then duration not negative.** The EXACT decimal value of `I` must not be negative, decided before
  any binary rounding; a negative value is `CURRENT_NEGATIVE` with no number. Then the EXACT decimal value of `t` must not
  be negative; a negative value is `DURATION_NEGATIVE` with no number. A zero current or a zero duration (including `-0`)
  is admitted and gives exactly `0` A·h.
- **Binary bridge.** Each admitted decimal is converted ONCE to the correctly rounded binary64 value (round half to even)
  and handed to the owner as a typed number; the owner parses no string (calc/units §10). Every admitted nonzero value lies
  between `10^-9` and `10^9` in magnitude, so it is a normal binary64 number with relative rounding error at most `2^-53`;
  an exact zero converts to `+0.0`.
- **Owner applicability.** The method record declares NO owner condition: the condition vocabulary has no not-negative
  condition and none is added. A negative `i_load` or `t_duration` that reaches the adapter is refused there as
  `FAILURE / EXECUTION_INTEGRITY_FAILURE` (unreachable from the page). No result range is declared.
- **Binary acceptance (adapter).** The exact rational product `i_load × t_duration` of the binary inputs is rounded ONCE
  to binary64. A zero current or a zero duration (`0.0` or `-0.0`) gives exactly `+0.0`. A nonzero exact result is
  accepted only when the rounded value is finite, positive and `|Q − exact| ≤ 2^-52 · exact` (one correct rounding gives
  at most `2^-53`). Overflow, underflow of a nonzero result or any failed check is `FAILURE / EXECUTION_INTEGRITY_FAILURE`
  with no numerical payload, displayed as `KNOWLEDGE_UNAVAILABLE`, never rewritten as a refusal. Representability: inside
  the representation limits every nonzero result lies between `10^-18` A·h and `10^18` A·h, well inside the normal
  binary64 range, so neither overflow nor underflow can occur from the page; the guards stay in place for direct owner use.
- **Decimal-reference acceptance (consumer).** A successful owner result is shown only when it agrees with the exact
  decimal product `I × t` of the ENTERED decimals: exactly `+0` when, and only when, `I` or `t` is exactly zero; otherwise
  positive and within a relative error of `2^-51`. Proof that the bound always holds: with `u = 2^-53`, the binary inputs
  are `I(1 + e₁)` and `t(1 + e₂)` with `|e₁|, |e₂| ≤ u`, so the exact binary-input product is `(I × t)(1 + e₁)(1 + e₂)`,
  and the single rounding multiplies it by `(1 + e₃)`, `|e₃| ≤ u`. The total relative error is at most
  `(1 + u)³ − 1 = 3u + O(u²) < 3.0000001 · u < 4u = 2^-51` (the lower side, `1 − (1 − u)³`, is smaller). Both sides are
  checked exactly in rational arithmetic by the focused tests. A failed check is `KNOWLEDGE_UNAVAILABLE` with no number.
- **Display.** The shown value is derived from the exact decimal value, never from the binary value: rounded ONCE to 12
  significant digits, round half to even, with trailing zeros removed. It is labelled **exact** when that rounding changes
  nothing and **rounded to 12 significant digits** otherwise (`0.5 A`, `4 h` shows `2`, exact; `1 A`, `0.333333333 h` shows
  `0.333333333`, exact; `0.1 A`, `0.3 h` shows `0.03`, exact; `1.234567891 A`, `1.234567891 h` shows `1.52415787749`,
  rounded). Plain decimal notation is used for `10^-6 ≤ Q < 10^12` A·h and the form `m × 10^e` otherwise, so a tiny
  nonzero charge is never shown as `0` (`0.000000001 A` for `0.000000001 h` shows `1 × 10^-18`, exact). The digits shown
  imply no measurement resolution, precision or accuracy.
- These rules belong to this method only; none is a generic owner numerical policy.

## 7. Refusal and abstention semantics

Order after request integrity (CSRF), project authorization, eligibility and strict capture (a malformed request is a bare
400 with no reason token): (1) completeness — every declaration and screen item answered, else `NOT_DECLARED`; (2) screen
— any YES is `ENGINEERING_REVIEW_REQUIRED` and the owner is not invoked; (3) declarations — any «does not apply» is
`MODEL_NOT_SUPPORTED`; (4) numeric grammar — `INVALID_NUMERIC_INPUT`; (5) current not negative — `CURRENT_NEGATIVE`;
(6) duration not negative — `DURATION_NEGATIVE`; (7) the shared owner; (8) the decimal-reference acceptance —
`KNOWLEDGE_UNAVAILABLE`. A method artifact that is missing, unreadable or changed is `KNOWLEDGE_UNAVAILABLE` before any of
these. The first failing stage alone decides; no refusal carries a number. Owner correspondence:
`REFUSAL / INVALID_NUMERIC_INPUT` → `INVALID_NUMERIC_INPUT`; `REFUSAL / UNIT_NOT_ADMITTED` or `UNKNOWN_UNIT` →
`UNIT_NOT_SUPPORTED`; `REFUSAL / METHOD_NOT_REGISTERED` or `VERSION_MISMATCH`, `UNABLE / SOURCE_UNAVAILABLE` and
`FAILURE / EXECUTION_INTEGRITY_FAILURE` → `KNOWLEDGE_UNAVAILABLE`; any other owner state → the neutral
`UNMAPPED_OWNER_OUTCOME`. The owner state and token are preserved, never rewritten.

## 8. High-risk screen (declared; not a safety engine)

Six items, answered yes or no, none pre-selected — whether the load is, is powered by or is part of: mains or high
voltage; a battery or energy-storage cell; fire, ignition or overheating risk; medical or life-supporting use; vehicle or
aerospace use; a safety function, alarm, protection or shut-off. The items and their wording are those of the DC resistive
load current, power and energy methods. A load powered by a battery is therefore screened out for specialist review: this
method gives no battery result of any kind, and naming the ampere hour as a battery-rating unit is not such a result. All
NO answers only allow this bounded calculation to proceed and never mean safe. The screen neither reads nor feeds
SafetySignal.

## 9. Result, provenance and fixed disclosure

On success the page shows `Q` in A·h with its exact / rounded label, the declared inputs as entered with their units, the
stated assumptions (D-1 to D-4), the labels `UNVALIDATED` and `NOT EVIDENCE`, the statement that the result is a charge and
not an energy, the statement that it is not a battery capacity, runtime, state of charge or battery choice and is compared
with no rating, the method identity and version, the method source and unit records the owner carried, and this fixed
disclosure (English; pinned equal to the artifact). Item 6 is the next engineering need. The wording "the charge that
flows through the declared load during the declared constant-current duration" is the result's meaning; the phrases
"battery capacity needed", "battery requirement", "required capacity", "runtime requirement" and "battery size" never
appear on any surface of this method.

1. This is the electric charge that flows through one load while the DC current I you declared stays constant for the whole duration t you declared: Q = I × t, given in ampere hours (A·h).
2. The current and the duration are your own declared values. InventorAI did not measure them and does not establish that the current is constant: a current that changes, on-off or duty-cycled use, standby or sleep phases, start-up or inrush current, switching, AC behaviour and any load whose current varies are not included, and no average current is substituted.
3. Q is a charge, not an energy. The ampere hour is a unit of electric charge that is also used in battery ratings, but this value is not compared with any rating: it is not a battery capacity, a runtime, a state of charge, a battery choice or a sizing, selection or suitability statement for any battery or source.
4. No unit is converted: the current is read in amperes, the duration in hours and the charge is given in ampere hours only, with no milliampere hours, coulombs, seconds or minutes.
5. The value is shown exactly when it can be; otherwise it is rounded to 12 significant digits and labelled rounded. The digits follow from your entry; they are not the precision of any measurement.
6. Next engineering need: a charge value alone cannot determine how long a real battery lasts. Whether the current really stays constant, what the load draws over its whole use with every phase included, which source or battery could supply it and how that source behaves as it discharges, and whether the load, its wiring, source and any switch are rated for the current all remain unverified, and must be checked by measurement or a qualified person before any reliance. The result is preliminary, advisory, UNVALIDATED and not evidence.
7. Reference source material: U.S. Department of Energy — Electrical Science, DOE-HDBK-1011/1-92 (archived; historical fundamentals reference only); the coulomb and the ampere hour as identified in NIST Special Publication 811. Q = I × t is InventorAI's own restatement for a constant current, and no handbook or NIST text, example, table or figure is reproduced.

## 9A. Arabic disclosure and UX wording

**A-1 Fixed disclosure (Arabic rendering of the seven §9 items, item by item; no meaning added, removed or softened).**

> 1. هذه هي الشحنة الكهربائية التي تمرّ في حِمل واحد ما دام التيار المستمر I الذي صرّحت به ثابتًا طوال المدة t التي صرّحت بها كلها: Q = I × t، بالأمبير ساعة (A·h).
> 2. التيار والمدة قيم صرّحت بها أنت. لم يقسهما InventorAI ولا يثبت أن التيار ثابت: لا يُدرج التيار الذي يتغير، ولا الاستخدام المتقطع أو بدورة تشغيل (duty cycle)، ولا أطوار الاستعداد أو السكون (standby/sleep)، ولا تيار بدء التشغيل أو التيار الاندفاعي (inrush)، ولا التبديل، ولا سلوك التيار المتردد (AC)، ولا أي حِمل يتغير تياره، ولا يُستبدل أي تيار متوسط.
> 3. Q شحنة وليست طاقة. الأمبير ساعة وحدة للشحنة الكهربائية تُستخدم أيضًا في القيم الاسمية (ratings) للبطاريات، لكن هذه القيمة لا تُقارن بأي قيمة اسمية: فهي ليست سعة بطارية ولا زمن تشغيل (runtime) ولا حالة شحن (state of charge) ولا اختيارًا لبطارية ولا تحديدًا لحجم (sizing) أو اختيارًا أو حكمًا بملاءمة أي بطارية أو مصدر.
> 4. لا تُحوَّل أي وحدة: يُقرأ التيار بالأمبير، والمدة بالساعات، وتُعطى الشحنة بالأمبير ساعة فقط، دون مللي أمبير ساعة ولا كولوم ولا ثوانٍ ولا دقائق.
> 5. تُعرض القيمة بدقة حين يمكن ذلك؛ وإلا تُقرَّب إلى 12 رقمًا معنويًا ويُشار إلى أنها مقرَّبة. الأرقام ناتجة عن إدخالك؛ وليست دقة أي قياس.
> 6. الحاجة الهندسية التالية: قيمة الشحنة وحدها لا تحدد كم تدوم بطارية حقيقية. ما إذا كان التيار يبقى ثابتًا فعلًا، وما يسحبه الحِمل على مدى استخدامه كله بكل أطواره، وأي مصدر أو بطارية يمكنه تزويده وكيف يتصرف ذلك المصدر مع تفريغه، وما إذا كان الحِمل وأسلاكه ومصدره وأي مفتاح مُصنَّفًا لهذا التيار — كلها تبقى غير مُتحقَّق منها، ويجب فحصها بالقياس أو بواسطة شخص مؤهل قبل أي اعتماد. هذه النتيجة أولية وإرشادية، وغير مُتحقَّق منها (UNVALIDATED)، وليست دليلًا.
> 7. المراجع: وزارة الطاقة الأمريكية — Electrical Science، ‏DOE-HDBK-1011/1-92 (مؤرشف؛ مرجع تاريخي للأساسيات فقط)؛ والكولوم والأمبير ساعة كما يحددهما NIST Special Publication 811. وQ = I × t إعادة صياغة من InventorAI لتيار ثابت، ولا يُستنسخ أي نص أو مثال أو جدول أو شكل من الدليل أو من NIST.

**A-2 Applicability declarations (§5).** The inventor answers «ينطبق على حالتي» or «لا ينطبق على حالتي», none pre-selected.

| §5 | Arabic statement |
|---|---|
| D-1 constant_dc_current | التيار المارّ في الحِمل تيار مستمر (DC) يبقى عند القيمة الواحدة المُدخلة طوال المدة المصرّح بها كلها؛ ولا يُحسب أي تيار متغير أو نبضي أو بدورة تشغيل (duty cycle) أو متقطع أو تيار بدء تشغيل أو تيار اندفاعي (inrush) أو تبديل أو تيار متردد (AC). |
| D-2 declared_values | التيار والمدة المُدخلان قيمك أنت لهذا الحِمل الواحد، مأخوذان من قراءتك أو من وثائقك أو من خطتك؛ ولم يقسهما InventorAI ولم يتحقق منهما، ولا يثبت أن التيار ثابت. |
| D-3 charge_through_load | الكمية المطلوبة هي الشحنة الكهربائية التي تمرّ في هذا الحِمل الواحد خلال تلك المدة الواحدة، وليست سعة بطارية ولا زمن تشغيل (runtime) ولا حالة شحن (state of charge) ولا طاقة ولا اختيارًا لبطارية أو مصدر. |
| D-4 single_load_single_period | الموصوف حِمل واحد وفترة واحدة متصلة عند ذلك التيار الواحد؛ ولا تُدمج في هذه القيمة عدة أحمال أو عدة فترات أو أطوار الاستعداد أو السكون (standby/sleep) أو أي تيار آخر. |

**A-3 Screen (§8).**

| §8 | Arabic item |
|---|---|
| mains_or_high_voltage | جهد الشبكة الكهربائية (mains) أو جهد عالٍ |
| battery_or_storage_cell | بطارية أو خلية لتخزين الطاقة |
| fire_or_overheating | خطر حريق أو اشتعال أو سخونة زائدة |
| medical_or_life_supporting | استخدام طبي أو داعم للحياة |
| vehicle_or_aerospace | استخدام في المركبات أو في الطيران والفضاء (aerospace) |
| safety_function | وظيفة سلامة أو إنذار أو حماية أو إيقاف |

**A-4 Right-to-left rendering.** Numbers, the role symbols `I`, `t` and `Q`, the unit tokens `A`, `h` and `A·h`, the
relation `Q = I × t`, the method identity and `UNVALIDATED` / `NOT EVIDENCE` are each direction-isolated on the Arabic page;
the inventor's typed values are shown left-to-right, so a leading minus stays attached to its number. The result line keeps
`A·h` as one left-to-right run with its middle dot.

## 10. Exclusions (binding)

No battery capacity, statement of what any battery must hold, runtime, state of charge, charging, discharge, chemistry, BMS, sizing, selection,
suitability or Battery / BMS result; no comparison of the charge with any rating or with any battery; no statement that any
battery or source can supply this charge or this current; no energy, power, voltage, resistance, temperature or thermal
result from this method and no duplication of the DC resistive load energy method; no varying-current, average-current,
duty-cycle, standby-phase or integrated charge; no multi-load or multi-period combination; no AC, transient, inrush or
switching analysis; no Kirchhoff, network or circuit solving; no inference of the load, the current, its constancy, the
duration or any declaration, and no generic load or battery question; no unit conversion (no `mA`, `mA·h`, `mAh`, `Ah`,
`C`, `s`, `min`, `W·h`, `Wh` or `J`; no `A·h` ↔ `C` and no `h` ↔ `s`); no alias or conversion table; no persistence,
result retention, report, PDF, Structured Export, API, evidence, readiness, progression, gap or SafetySignal effect; no AI
or provider call; Stage 15 part eligibility only as stated in §1; no 28-T3, Battery / BMS, D4 or T6 activation.

## 11. Source and IP status

- **DOE-CHG-S1** — U.S. Department of Energy, *DOE Fundamentals Handbook: Electrical Science*, Volume 1 of 4, Module ES-01
  — Basic Electrical Theory (DOE-HDBK-1011/1-92), section "Electrical Terminology", subsection "Current", printed page ES-01
  page 10 (PDF page index 33): the identification of electric current with the flow of electric charge and the definition of
  one ampere as one coulomb passing a given point per second. Official DOE record status ARCHIVE — Canceled, effective April
  2016: used ONLY as a historical / fundamentals reference for this one factual relationship, never as current regulatory,
  safety or compliance guidance. "Current is the rate of electric charge flow" is InventorAI's own paraphrase and
  `Q = I × t` is InventorAI's own algebraic restatement for a constant current; it is NOT claimed that DOE prints the
  integrated formula. This record reuses the Lead-level direct primary-source inspection recorded as
  `electronics_electrical:PR018` (2026-10-12; executor egress to the source host was blocked), with its passage-level
  observations, which are not a blanket authorship determination.
- **NIST-AH-S1** — NIST Special Publication 811, online edition: Chapter 4, Table 3 (electric charge — coulomb, C,
  expressed in SI base units as s · A) and Appendix B.9, Electricity and Magnetism, ampere hour row
  (`1 A · h = 3.6 × 10³ C`): the coulomb as the SI unit of electric charge and the ampere hour as a unit of electric charge,
  from which the hour is identified as the ampere hour's time factor (`1 h = 3600 s` being InventorAI's arithmetic,
  recorded for identification only and never applied). This record reuses the Lead-level direct primary-source inspection
  recorded as `electronics_electrical:PR020` (2026-10-12), cited from the online edition as inspected and not attributed to
  the 2008 PDF edition. **Not relied upon:** a separate NIST statement that the hour is accepted for use with the SI
  (SP 811 Chapter 5) is NOT recorded as an inspected location in any repository provenance record and is therefore not
  asserted by this method; identification of `h` rests on the inspected ampere hour row alone. Supplying that inspection is
  an open Lead / Owner item, not a defect of the delivered records.
- **Pack scope note.** `electronics_electrical:PR018` and `PR020`, the pack claims `charge_current_time_reference`,
  `charge_unit_discipline` and `ampere_hour_charge_unit` and their reference-fundamentals group say "no project-specific
  calculation" and that `A · h`, `mA · h` and `C` are reference text only and NOT added as owner units. They are unchanged
  and keep that scope: this method is a separately Owner-authorized method with its own method authority, source records
  and source-use records, as the DC resistive load current, power and energy methods are; the owner admits `h` and `A·h`
  only through its own records `dcu:U016` and `dcu:U017` under calc/units Correction 10, and still admits no `C` or
  `mA·h`.
- **Units** — `A`: the owner record `dcu:U013` (NIST SP 811 Appendix B.9, as recorded in `electronics_electrical:PR005`;
  owner source use `dcu:SU011`). `h` and `A·h`: the owner records `dcu:U016` and `dcu:U017` (NIST SP 811 Appendix B.9
  ampere hour row read with Chapter 4, Table 3; the Lead-level inspection recorded as `electronics_electrical:PR020`,
  2026-10-12; owner source use `dcu:SU017`, the snapshot of this method's own `dcq:SU002`). The method artifact's
  unit-role record is `NIST-AH-S1`.
- **Source use** (not a legal opinion): the `electronics_electrical:PR019` disposition applied to this method
  (`dcq:SU001`; owner snapshot `dcu:SU018`) — DOE website government information is public domain with DOE
  acknowledgement requested; contractor- or privately contributed material may remain protected, so no blanket
  public-domain claim is made for the handbook's expressive content and no comprehensive authorship verification is
  claimed — and the `electronics_electrical:PR021` NIST disposition, read with `PR011` (`dcq:SU002`; owner snapshot
  `dcu:SU017`). Use is the one factual relationship and the two unit identifications only, restated in InventorAI's own
  words; the product form, the not-negative domain and the constant-current restriction are InventorAI's own statement;
  the mathematics is implemented independently; no handbook or NIST prose, worked example, table, figure, diagram,
  photograph or logo is copied; no textbook material is reproduced or relied on; no external modelling library or code is
  used; DOE and NIST are acknowledged neutrally and no endorsement is stated or implied. `electronics_electrical:PR019`
  and `PR021` are not broadened beyond this method.

## 12. Implementation boundary

The one existing shared owner executes the method through ONE additional immutable binding created by application wiring
(`_DC_CHARGE_BINDING` in `web/app.py`), beside the nine existing bindings; there is no registry, discovery, dynamic module
path or request-selected method (calc/units contract §13I). Routes: `GET` / `POST
/session/<sid>/dc-constant-current-charge`, behind the central project authorization and the global CSRF guard; the
session page shows one optional link on an eligible project. Nothing is persisted; the POST renders its result directly.
The owner change is bounded to the data of its existing named-exception mechanism (`KIND_TOKEN_EXCEPTIONS` gains the
`time` entry) and its closed inventories; no owner rule, validation path or architecture is changed.

## 13. Verification

Focused tests (`tests/test_dc_constant_current_charge.py`, `tests/test_dc_constant_current_charge_browser.py`): the
reference vectors `0.5 A / 4 h = 2 A·h`, `2 A / 1.5 h = 3 A·h`, `0.25 A / 0.5 h = 0.125 A·h` and `1.2 A / 10 h = 12 A·h`;
zero and negative-zero current and duration giving exactly `+0` A·h; exact and rounded results; negative current and
negative duration refused before the owner, each with its own reason and no number; non-finite and non-numeric inputs
refused; overflow and underflow failing closed in the adapter; representation-limit values; an independent
exact-rational oracle over a random sample; the exact rational check of the `2^-51` proof; missing, malformed, duplicate
and contradictory declarations; grammar; unit, method, version, adapter and artifact integrity, with no number on any
refusal and no `C`, `mA·h`, `s` or `min` accepted; owner artifact content version 10 with every content-version-9 record
unchanged; the §7 order and owner correspondence; eligibility (root and declared part; a Mechanical root ineligible);
CSRF, authorization, request isolation and no persistence; the nine existing methods unchanged; the absence of the five
forbidden battery phrases on every surface; EN / AR fidelity; and real-browser EN / AR success and refusal journeys. Hosted
required CI is the merge gate.

## 14. STOP conditions

Stop and return to the Owner on a source or IP deficiency, a need to incorporate external code or content, a contract
incompatibility, unprovable numerical integrity, an unqualified battery, runtime, capacity, rating, suitability or safety
claim, any owner change beyond the data of its existing named-exception mechanism and closed inventories, or any scope
expansion (another method, consumer, unit, conversion, varying-current or integrated charge, battery analysis, energy
duplication, circuit analysis, persistence or report surface).
