# ELECTRICAL / ELECTRONICS — DC RESISTIVE LOAD ENERGY METHOD CONTRACT

STATUS: OWNER-AUTHORIZED BOUNDED METHOD CONTRACT — written with, and governing, the one bounded implementation increment
`DC-RESISTIVE-LOAD-ENERGY-01` (Slice 1), which the Owner authorized as ONE bounded implementation and ONE pull request,
with the method assessment accepted by the Owner. Applicability: this contract governs the delivered method only on the
verified merge of that pull request into `feature/atomic-json-session-persistence`; on its proposal branch it describes an
Owner-authorized proposed method, not a merged or delivered capability. Merge, deployment, Battery / BMS capability, Power
Electronics / Motion (28-T3), D4 or T6 activation, thermal compatibility and any persistence or sharing of calculation
results are NOT authorized by it.
AUTHORITY LEVEL: subordinate to the accepted
[shared deterministic calculation and units owner boundary contract](SHARED_DETERMINISTIC_CALCULATION_AND_UNITS_OWNER_BOUNDARY_CONTRACT.md)
(the "calc/units contract", with its Correction 08, §13G, added by the same increment). It amends no other method contract;
the two-support reactions, THERM-01, planar-moment, rotational-load, TMP36, DC resistive load current and DC resistive
load power methods stay unchanged. Where this document and the calc/units contract differ, the calc/units contract wins and
the difference is a defect of this document.

---

## 0. Preserved truth (binding)

- `ACTIVE CONTRACT: NONE` describes the state before and after this increment; this contract fills no active-contract slot
  after delivery and is not a delivery record. Current-truth delivery records belong to a later closure sync.
- This method enters, completes or reopens no Stage and changes no roadmap count (27 of 45 complete). Power Electronics /
  Motion (28-T3) stays BLOCKED, Battery / BMS stays R2 and RECORDED only, D4 and T6 stay inactive, and the Stage 15
  composition authority is unchanged.
- The Electrical / Electronics pack claims `ohms_law_reference`, `electrical_power_vi_reference`,
  `constant_power_energy_reference` and `energy_time_unit_discipline`, their reference-fundamentals groups and the
  provenance records `electronics_electrical:PR004` to `PR011` are unchanged and keep their own scope (§11). The DC
  resistive load current and power methods are unchanged; this method neither imports nor amends them.

## 1. Purpose and scope

ONE optional, advisory, non-binding, request-local calculation: the theoretical electrical energy that ONE explicitly
declared ideal steady-state DC resistive load absorbs at ONE declared voltage over ONE declared duration during which its
power stays constant. It lets an inventor who knows, from their own reading, documentation or plan, the voltage across one
load, its resistance and how long it stays on see the energy the ideal relation gives, with its sign convention, its limits
and the engineering checks that still remain — above all that this energy is not a battery capacity, a runtime or a
temperature. Nothing is inferred: InventorAI never decides that a project has a resistive load or how long it runs, and
asks no generic question about loads or batteries.

Eligibility (method-specific): a project whose trusted durable root domain is exactly `electronics_electrical`, read as
the other calculation gates read it (`_cap12_root_domain` in `web/app.py`). Root only: no declared Stage 15 part grants this
method, and the Stage 15 exception in `engine/subsystem_model.py` does not name it. An unreadable domain grants nothing.
The session link, the page and the submission read the same one decision.

## 2. Method identity and version

Identity `electrical:dc_resistive_load_energy`, version `1.0`. Method-authority artifact
`docs/governance/electrical_content_config/dc_resistive_load_energy_v1.json`
(`electrical_dc_resistive_load_energy`, artifact version `1`), separate from every other artifact; none loads another.
Adapter `engine/dc_resistive_load_energy_method.evaluate`; consumer `engine/dc_resistive_load_energy.py` (the one named
Electrical / Electronics consumer of this method).

## 3. Method definition

`E = V² × t / R = P × t`, with `P = V² / R`, `V` in V, `R` in Ω, `t` in s and `E` in J, for `R > 0` and `t ≥ 0`, ONLY
for a power that stays constant throughout `t`. It is InventorAI's combination of two relationships the DOE Electrical
Science handbook writes as `E = I × R` (Ohm's law) and `P = I × E` (electric power), and of the definition, in the DOE
Classical Physics handbook, of power as the rate at which energy is transferred or used, which InventorAI restates as
`E = P × t` for a constant power (§11). Neither handbook is claimed to print the combined forms or the sign convention, and
no varying-power, average-power or integration treatment is derived.

**Sign convention (fixed, documented; passive sign convention).** `V` is the voltage across the load measured from the load
terminal the inventor calls `+` to the terminal they call `−`; the current is taken through the load from `+` to `−`. The
load then absorbs the power `V × (V / R) = V² / R` and, over the duration, the energy `V² × t / R`: never negative for
`R > 0` and `t ≥ 0`, exactly zero for `V = 0` or `t = 0` and the same for `+V` and `−V`. A negative zero voltage or
duration gives exactly `+0` J, never `−0`.

**Constant-power assumption (fixed, documented).** `E = P × t` holds only when the power stays the same for the whole
declared duration. With a constant resistance this is a constant voltage across the load throughout `t` (D-1, D-2, D-5).

The result is the theoretical absorbed energy of the ideal relation only: never a measured, rated, stored, available or
guaranteed energy, never a battery capacity, charge, state of charge, runtime or sizing, never a statement that any source
can supply it, and never a temperature or a thermal result.

## 4. Roles, quantity kinds and exact unit tokens

| Role | Meaning | Quantity kind | Exact unit token |
|---|---|---|---|
| `v_load` (`V`) | the steady DC voltage across the load, `+` to `−`, as declared; signed | `voltage` | `V` |
| `r_load` (`R`) | the constant resistance of the load, as declared; strictly positive | `electric_resistance` | `Ω` (U+03A9) |
| `t_duration` (`t`) | the duration at that constant power, as declared; not negative | `time` | `s` |
| `e_load` (`E`) | the theoretical energy the load absorbs over the duration; never negative | `energy` | `J` |

`voltage` / `V` and `electric_resistance` / `Ω` already exist in the shared owner (calc/units §13E). `time` / `s` and
`energy` / `J` are the ONLY additions, made by calc/units Correction 08 (§13G) with their own owner unit records
`dcu:U015` (s) and `dcu:U014` (J). No unit is converted: `J` is not related to `W`, `N·m`, `Wh`, `kWh` or `mAh`, and `s`
to no minute or hour.

## 5. Applicability declarations (the model-applicability confirmation)

Each is shown as its own statement and answered «applies» or «does not apply», none pre-selected. A missing answer is
`NOT_DECLARED`; «does not apply» is `MODEL_NOT_SUPPORTED`. InventorAI infers none of them; D-2 is the explicit confirmation
that the load is resistive, D-4 the explicit confirmation of the absorbed-energy convention and D-5 the explicit
confirmation that the power stays constant throughout the declared duration.

| Ref | Id | Accepted statement |
|---|---|---|
| D-1 | `steady_state_dc` | the voltage across the load is a steady DC voltage that stays constant throughout the declared duration; no AC, pulsed, switching, start-up or inrush condition is being calculated |
| D-2 | `resistive_load` | the load behaves as one resistance that stays constant at this voltage throughout the declared duration (a resistive, ohmic load), not a motor, lamp, LED, battery, electronic circuit or other load whose current does not follow V / R; InventorAI does not determine that the load is resistive |
| D-3 | `declared_values` | the voltage, resistance and duration entered are the inventor's own values for this one load, taken from their own reading, documentation or plan; InventorAI did not measure or check them |
| D-4 | `absorbed_energy_convention` | the energy wanted is the electrical energy this load absorbs, with the voltage taken from the load terminal the inventor calls + to the terminal they call − and the current through the load in the same direction (the passive sign convention); for a positive resistance it is never negative and is the same for a positive and a negative voltage |
| D-5 | `constant_power_duration` | the power the load absorbs stays constant for the whole declared duration, so the energy is that power multiplied by the duration; no varying, average, intermittent or duty-cycled power is being calculated, and the duration is not a battery runtime or an expected operating time worked out by InventorAI |

## 6. Numeric domain and numerical acceptance

- **Grammar (strict capture).** For `V` and `R` the DC resistive load current grammar, reused unchanged: an optional single
  leading minus, then one to nine integer digits for `V` or one to twelve for `R`, and an optional single fractional part
  of one to nine digits. For `t` the same form with one to nine integer digits. No plus sign, exponent, separator, space,
  Unicode digit, unit suffix, `inf`, `nan` or normalization. A field sent twice, an unknown field or a declaration / screen
  answer outside its closed choices makes the whole request malformed (a bare 400). An omitted, malformed or over-length
  value is `INVALID_NUMERIC_INPUT`.
- **Representation limits are not physical limits.** `|V| < 10^9` V; `R` from `10^-9` to below `10^12` Ω; `t` from `0`
  to below `10^9` s; steps of `10^-9`. They are NOT physical limits, equipment ratings, operating times or a claim that such
  values are realistic. The 64-character field cap is abuse protection only — a NON-PHYSICAL bound.
- **Positive resistance, then duration not negative.** The EXACT decimal value of `R` must be greater than zero, decided
  before any binary rounding; zero (including `-0`) or a negative value is `RESISTANCE_NOT_POSITIVE` with no number. Then
  the EXACT decimal value of `t` must not be negative; a negative value is `DURATION_NEGATIVE` with no number. A zero
  voltage or a zero duration (including `-0`) is admitted and gives exactly `0` J.
- **Binary bridge.** Each admitted decimal is converted ONCE to the correctly rounded binary64 value (round half to even)
  and handed to the owner as a typed number; the owner parses no string (calc/units §10). Every admitted nonzero value lies
  between `10^-9` and `10^12` in magnitude, so it is a normal binary64 number with relative rounding error at most `2^-53`;
  an exact zero converts to `+0.0`.
- **Owner applicability.** The method record declares the existing `greater_than_zero` on `r_load`; a non-positive value
  that reaches the owner is `UNABLE_TO_DETERMINE / INPUT_OUTSIDE_ADMITTED_RANGE`, shown as the neutral
  `UNMAPPED_OWNER_OUTCOME` (unreachable from the page). The condition vocabulary has no not-negative condition and none is
  added: a negative `t_duration` that reaches the adapter is refused there as `FAILURE / EXECUTION_INTEGRITY_FAILURE`
  (unreachable from the page). No result range is declared.
- **Binary acceptance (adapter).** The exact rational value `v_load² × t_duration / r_load` of the binary inputs is rounded
  ONCE to binary64. A zero voltage or a zero duration (`0.0` or `-0.0`) gives exactly `+0.0`. A nonzero exact result is
  accepted only when the rounded value is finite, positive and `|E − exact| ≤ 2^-52 · exact` (one correct rounding gives at
  most `2^-53`). Overflow, underflow of a nonzero result or any failed check is `FAILURE / EXECUTION_INTEGRITY_FAILURE`
  with no numerical payload, displayed as `KNOWLEDGE_UNAVAILABLE`, never rewritten as a refusal. Representability: inside
  the representation limits every nonzero result lies between `10^-39` J (`(10^-9)² × 10^-9 / 10^12`) and `10^36` J
  (`(10^9)² × 10^9 / 10^-9`), well inside the normal binary64 range (about `2.2 × 10^-308` to `1.8 × 10^308`), so neither
  overflow nor underflow can occur from the page; the guards stay in place for direct owner use.
- **Decimal-reference acceptance (consumer).** A successful owner result is shown only when it agrees with the exact
  decimal value `V² × t / R` of the ENTERED decimals: exactly `+0` when, and only when, `V` or `t` is exactly zero;
  otherwise positive and within a relative error of `2^-50`. Proof that the bound always holds: with `u = 2^-53`, the
  binary inputs are `V(1 + e₁)`, `R(1 + e₂)` and `t(1 + e₃)` with `|e₁|, |e₂|, |e₃| ≤ u`, so the exact binary-input result
  is `(V² × t / R) · (1 + e₁)² (1 + e₃) / (1 + e₂)`, and the single rounding multiplies it by `(1 + e₄)`, `|e₄| ≤ u`. The
  total relative error is at most `(1 + u)⁴ / (1 − u) − 1 = 5u + O(u²) < 5.0000001 · u < 8u = 2^-50` (the lower side,
  `1 − (1 − u)⁴ / (1 + u)`, is smaller). Both sides are checked exactly in rational arithmetic by the focused tests. A
  failed check is `KNOWLEDGE_UNAVAILABLE` with no number.
- **Display.** The shown value is derived from the exact decimal value, never from the binary value: rounded ONCE to 12
  significant digits, round half to even, with trailing zeros removed. It is labelled **exact** when that rounding changes
  nothing and **rounded to 12 significant digits** otherwise (`12 V`, `24 Ω`, `3600 s` shows `21600`, exact; `1 V`, `3 Ω`,
  `1 s` shows `0.333333333333`, rounded). Plain decimal notation is used for `10^-6 ≤ E < 10^12` J and the form
  `m × 10^e` otherwise, so a tiny nonzero energy is never shown as `0` (`0.000000001 V` across `999999999999.999999999 Ω`
  for `0.000000001 s` shows `1 × 10^-39`, rounded). The digits shown imply no measurement resolution, precision or
  accuracy.
- These rules belong to this method only; none is a generic owner numerical policy.

## 7. Refusal and abstention semantics

Order after request integrity (CSRF), project authorization, eligibility and strict capture (a malformed request is a bare
400 with no reason token): (1) completeness — every declaration and screen item answered, else `NOT_DECLARED`; (2) screen
— any YES is `ENGINEERING_REVIEW_REQUIRED` and the owner is not invoked; (3) declarations — any «does not apply» is
`MODEL_NOT_SUPPORTED`; (4) numeric grammar — `INVALID_NUMERIC_INPUT`; (5) positive resistance — `RESISTANCE_NOT_POSITIVE`;
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
aerospace use; a safety function, alarm, protection or shut-off. The items and their wording are those of the DC
resistive load current and power methods. A load powered by a battery is therefore screened out for specialist review:
this method gives no battery result of any kind. All NO answers only allow this bounded calculation to proceed and never
mean safe. The screen neither reads nor feeds SafetySignal.

## 9. Result, provenance and fixed disclosure

On success the page shows `E` in J with its exact / rounded label, the declared inputs as entered with their units, the
stated assumptions (D-1 to D-5), the labels `UNVALIDATED` and `NOT EVIDENCE`, the method identity and version, the method
source and unit records the owner carried, and this fixed disclosure (English; pinned equal to the artifact). Item 6 is the
next engineering need.

1. This is the theoretical electrical energy that one resistive load absorbs over the duration t you declared, at the steady DC voltage V and with the resistance R you declared, while its power stays constant: E = V² × t / R = P × t, where P = V² / R.
2. Sign: V is the voltage across the load from the terminal you called + to the terminal you called −, and the current is taken through the load in the same direction. The load then absorbs E, which is never negative, is the same for a positive or a negative V, and is zero when V or t is zero.
3. The voltage, resistance and duration are your own declared values. InventorAI did not measure them and does not check that the load is resistive, that its resistance and voltage stay constant or that the power stays constant for the whole duration.
4. It is the ideal steady-state, constant-power relation only: a power that changes during the duration, on-off or duty-cycled use, wiring and contact resistance, the source's internal resistance and voltage drop, a battery voltage that falls as it discharges, temperature change of the resistance, start-up or inrush current, switching, AC behaviour, conversion losses and non-resistive loads such as motors, lamps, LEDs or electronics are not included.
5. The value is shown exactly when it can be; otherwise it is rounded to 12 significant digits and labelled rounded. The digits follow from your entry; they are not the precision of any measurement.
6. Next engineering need: this energy is not a battery capacity, a runtime or a temperature. Whether any battery or source can supply this energy and this power, how long a real source would last, how hot the load or its surroundings become, whether the load, its resistor, wiring, source and any driver or switch are rated for it, and what protection the circuit needs all remain unverified, and must be checked by measurement or a qualified person before any reliance. The result is preliminary, advisory, UNVALIDATED and not evidence.
7. Reference source material: U.S. Department of Energy — Electrical Science, DOE-HDBK-1011/1-92, and Classical Physics, DOE-HDBK-1010-92 (archived; historical fundamentals references only); the joule and the second as identified in NIST Special Publication 811. The relations are restated by InventorAI, and no handbook text, example or figure is reproduced.

## 9A. Arabic disclosure and UX wording

**A-1 Fixed disclosure (Arabic rendering of the seven §9 items, item by item; no meaning added, removed or softened).**

> 1. هذه هي الطاقة الكهربائية النظرية التي يمتصها حِمل مقاوم واحد خلال المدة t التي صرّحت بها، عند الجهد المستمر الثابت V ومع المقاومة R اللذين صرّحت بهما، ما دامت قدرته ثابتة: E = V² × t / R = P × t، حيث P = V² / R.
> 2. الإشارة: V هو الجهد على الحِمل من الطرف الذي سمّيته + إلى الطرف الذي سمّيته −، ويُؤخذ التيار عبر الحِمل في الاتجاه نفسه. عندها يمتص الحِمل الطاقة E، وهي لا تكون سالبة أبدًا، وتبقى نفسها للجهد V الموجب والسالب، وتساوي صفرًا حين يكون V أو t صفرًا.
> 3. الجهد والمقاومة والمدة قيم صرّحت بها أنت. لم يقسها InventorAI، ولا يتحقق من أن الحِمل مقاوم، ولا من أن مقاومته وجهده يبقيان ثابتين، ولا من أن القدرة تبقى ثابتة طوال المدة كلها.
> 4. هذه هي العلاقة المثالية في الحالة المستقرة وبقدرة ثابتة فقط: لا تُدرج القدرة التي تتغير خلال المدة، ولا الاستخدام المتقطع أو بدورة تشغيل (duty cycle)، ولا مقاومة الأسلاك والتلامس، ولا المقاومة الداخلية للمصدر وهبوط جهده، ولا جهد البطارية الذي ينخفض مع تفريغها، ولا تغيّر المقاومة مع الحرارة، ولا تيار بدء التشغيل أو التيار الاندفاعي (inrush)، ولا التبديل، ولا سلوك التيار المتردد (AC)، ولا فواقد التحويل، ولا الأحمال غير المقاومة مثل المحركات والمصابيح والثنائيات الباعثة للضوء (LED) والدوائر الإلكترونية.
> 5. تُعرض القيمة بدقة حين يمكن ذلك؛ وإلا تُقرَّب إلى 12 رقمًا معنويًا ويُشار إلى أنها مقرَّبة. الأرقام ناتجة عن إدخالك؛ وليست دقة أي قياس.
> 6. الحاجة الهندسية التالية: هذه الطاقة ليست سعة بطارية ولا زمن تشغيل (runtime) ولا درجة حرارة. ما إذا كانت أي بطارية أو مصدر يستطيع تزويد هذه الطاقة وهذه القدرة، وكم سيدوم مصدر حقيقي، ومدى سخونة الحِمل أو ما حوله، وما إذا كان الحِمل ومقاومه وأسلاكه ومصدره وأي مُشغِّل (driver) أو مفتاح مُصنَّفًا لها، والحماية التي تحتاجها الدائرة — كلها تبقى غير مُتحقَّق منها، ويجب فحصها بالقياس أو بواسطة شخص مؤهل قبل أي اعتماد. هذه النتيجة أولية وإرشادية، وغير مُتحقَّق منها (UNVALIDATED)، وليست دليلًا.
> 7. المراجع: وزارة الطاقة الأمريكية — Electrical Science، ‏DOE-HDBK-1011/1-92، وClassical Physics، ‏DOE-HDBK-1010-92 (مؤرشفان؛ مرجعان تاريخيان للأساسيات فقط)؛ والجول والثانية كما يحددهما NIST Special Publication 811. والعلاقات معاد صياغتها من InventorAI، ولا يُستنسخ أي نص أو مثال أو شكل من الدليلين.

**A-2 Applicability declarations (§5).** The inventor answers «ينطبق على حالتي» or «لا ينطبق على حالتي», none pre-selected.

| §5 | Arabic statement |
|---|---|
| D-1 steady_state_dc | الجهد على الحِمل جهد مستمر (DC) ثابت يبقى كما هو طوال المدة المصرّح بها؛ ولا يُحسب أي تيار متردد (AC) أو نبضي أو تبديل أو بدء تشغيل أو تيار اندفاعي. |
| D-2 resistive_load | يتصرف الحِمل كمقاومة واحدة تبقى ثابتة عند هذا الجهد طوال المدة المصرّح بها (حِمل مقاوم أومي)، وليس محركًا أو مصباحًا أو ثنائيًا باعثًا للضوء (LED) أو بطارية أو دائرة إلكترونية أو أي حِمل آخر لا يتبع تياره V / R؛ ولا يحدد InventorAI أن الحِمل مقاوم. |
| D-3 declared_values | الجهد والمقاومة والمدة المُدخلة قيمك أنت لهذا الحِمل الواحد، مأخوذة من قراءتك أو من وثائقك أو من خطتك؛ ولم يقسها InventorAI ولم يتحقق منها. |
| D-4 absorbed_energy_convention | الطاقة المطلوبة هي الطاقة الكهربائية التي يمتصها هذا الحِمل، مع أخذ الجهد من طرف الحِمل الذي تسمّيه + إلى الطرف الذي تسمّيه − والتيار عبر الحِمل في الاتجاه نفسه (اصطلاح الإشارة السلبي، passive sign convention)؛ وهي مع مقاومة موجبة لا تكون سالبة أبدًا، وتبقى نفسها للجهد الموجب والسالب. |
| D-5 constant_power_duration | تبقى القدرة التي يمتصها الحِمل ثابتة طوال المدة المصرّح بها كلها، فتكون الطاقة هي تلك القدرة مضروبة في المدة؛ ولا تُحسب أي قدرة متغيرة أو متوسطة أو متقطعة أو بدورة تشغيل (duty cycle)، وليست المدة زمن تشغيل بطارية (runtime) ولا زمن تشغيل متوقعًا يحسبه InventorAI. |

**A-3 Screen (§8).**

| §8 | Arabic item |
|---|---|
| mains_or_high_voltage | جهد الشبكة الكهربائية (mains) أو جهد عالٍ |
| battery_or_storage_cell | بطارية أو خلية لتخزين الطاقة |
| fire_or_overheating | خطر حريق أو اشتعال أو سخونة زائدة |
| medical_or_life_supporting | استخدام طبي أو داعم للحياة |
| vehicle_or_aerospace | استخدام في المركبات أو في الطيران والفضاء (aerospace) |
| safety_function | وظيفة سلامة أو إنذار أو حماية أو إيقاف |

**A-4 Right-to-left rendering.** Numbers, the role symbols `V`, `R`, `t`, `P` and `E`, the unit tokens `V`, `Ω`, `s` and
`J`, the relation, the method identity and `UNVALIDATED` / `NOT EVIDENCE` are each direction-isolated on the Arabic page;
the inventor's typed values are shown left-to-right, so a leading minus stays attached to its number.

## 10. Exclusions (binding)

No battery capacity, charge, state of charge, runtime, sizing or Battery / BMS result; no statement that any source,
power supply or battery can supply this energy or this power; no temperature, heating, thermal or cooling result and no
thermal compatibility; no power, energy, current or voltage rating, capability or selection of any source, power supply,
battery, driver, switch, transistor, relay, wire, connector, fuse, resistor or component; no protection design; no
efficiency or loss result; no varying-power, average-power, duty-cycle or integrated energy; no Kirchhoff, network, series
/ parallel or circuit solving; no AC, transient, inrush or switching analysis; no motor, lamp, LED, battery or other
non-resistive load; no compatibility, suitability or safety conclusion; no inference of the load type, the voltage, the
resistance, the duration or any declaration, and no generic load or battery question; no unit conversion (no `mV`, `kΩ`,
`min`, `h`, `Wh`, `kWh`, `kJ` or `mAh`); no persistence, result retention, report, PDF, Structured Export, API, evidence,
readiness, progression, gap or SafetySignal effect; no AI or provider call; no Stage 15 part eligibility (§1); no 28-T3,
D4 or T6 activation.

## 11. Source and IP status

- **DOE-ENG-S1** — U.S. Department of Energy, *DOE Fundamentals Handbook: Electrical Science*, Volume 1 of 4, Module 1 —
  Basic Electrical Theory (DOE-HDBK-1011/1-92): Ohm's Law, handbook page 14 (`E = I × R`) and Electric Power, handbook page
  16 (`P = I × E`), with `E` the voltage in volts, `I` the current in amperes, `R` the resistance in ohms and `P` the power
  in watts. Official DOE record status ARCHIVE — Canceled, effective April 2016: used ONLY as a historical / fundamentals
  reference for these two factual relationships, never as current regulatory, safety or compliance guidance. This record
  reuses the Lead-level inspection recorded as `electronics_electrical:PR004` (2026-09-28; executor egress was blocked).
- **DOE-ENG-S2** — U.S. Department of Energy, *DOE Fundamentals Handbook: Classical Physics* (DOE-HDBK-1010-92), Module
  CP-05, "Power", printed page 8 (PDF page 138): the definition of power as the rate at which energy is transferred or
  used. `E = P × t` is InventorAI's own restatement of that definition for a power that stays constant throughout `t`; it
  is not claimed that DOE wrote it, and no varying-power, average-power or integration treatment is derived. The page's
  other unit examples and thermal-power wording are not imported. Official DOE publication-status record: Archive; used ONLY
  as a fundamentals reference. This record reuses the Lead-level textual source check recorded as
  `electronics_electrical:PR008` (2026-10-10).
- **Pack scope note.** `electronics_electrical:PR004` and `PR008`, the pack claims `ohms_law_reference`,
  `electrical_power_vi_reference` and `constant_power_energy_reference`, and their reference-fundamentals groups say "no
  project-specific calculation" for the groups they serve. They are unchanged and keep that scope: this method is a
  separately Owner-authorized method with its own method authority, source records and source-use records, as the DC
  resistive load current and power methods and THERM-01 are. Likewise `electronics_electrical:PR009` says that `J` and `s`
  are reference text of its reference group and NOT owner units: that statement stays true of that pack record, and the
  owner admits `J` and `s` only through its own records `dcu:U014` and `dcu:U015` under calc/units Correction 08.
- **Units** — `V` and `Ω`: the owner records `dcu:U011` and `dcu:U012` (NIST SP 811 Appendix B.9, as recorded in
  `electronics_electrical:PR005`; owner source use `dcu:SU011`). `J` and `s`: the owner records `dcu:U014` and `dcu:U015`
  (NIST SP 811 Chapter 4, Table 3 — joule, J, with the watt as J/s — and Table 1 — second, s; the Lead-level textual source
  check recorded as `electronics_electrical:PR009`, 2026-10-10; owner source use `dcu:SU014`, the snapshot of this method's
  own `dcenergy:SU002`). The method artifact's unit-role record is `NIST-JS-S1`.
- **Source use** (not a legal opinion): the `electronics_electrical:PR006` and `PR010` dispositions applied to this method
  (`dcenergy:SU001`; owner snapshot `dcu:SU015`) — DOE website government information is public domain with DOE
  acknowledgement requested; contractor- or privately contributed material may remain protected, so no blanket
  public-domain claim is made for either handbook's expressive content — and the `electronics_electrical:PR011` NIST
  disposition (`dcenergy:SU002`; owner snapshot `dcu:SU014`). Use is the three factual relationships and the two unit
  identifications only, restated in InventorAI's own words with `V` for voltage (notation normalization only); the
  combined forms, the positive-resistance and not-negative-duration domain, the constant-power restriction and the passive
  sign convention are InventorAI's own statement; the mathematics is implemented independently; no handbook prose, worked
  example, table, figure, diagram, photograph or logo is copied; no textbook material is reproduced or relied on; no
  external modelling library or code is used; DOE and NIST are acknowledged neutrally and no endorsement is stated or
  implied. `electronics_electrical:PR006`, `PR010` and `PR011` are not broadened beyond this method.

## 12. Implementation boundary

The one existing shared owner executes the method through ONE additional immutable binding created by application wiring
(`_DC_LOAD_ENERGY_BINDING` in `web/app.py`), beside the seven existing bindings; there is no registry, discovery, dynamic
module path or request-selected method (calc/units contract §13G). Routes: `GET` / `POST /session/<sid>/dc-load-energy`,
behind the central project authorization and the global CSRF guard; the session page shows one optional link on an
eligible project. Nothing is persisted; the POST renders its result directly.

## 13. Verification

Focused tests (`tests/test_dc_resistive_load_energy.py`, `tests/test_dc_resistive_load_energy_browser.py`): the reference
vectors `12 V / 24 Ω / 3600 s = 21600 J` and `5 V / 10 Ω / 60 s = 150 J`; a negative voltage giving the same nonnegative
energy; zero and negative-zero voltage and duration giving exactly `+0` J; exact and rounded results; zero, `-0` and
negative resistance; negative duration; duration and resistance boundaries; tiny, large and representation-limit values;
an independent exact-rational oracle over a random sample; the exact rational check of the `2^-50` proof; missing,
malformed, duplicate and contradictory declarations; grammar; unit, method, version, adapter and artifact integrity, with
no number on any refusal; owner artifact v8; the §7 order and owner correspondence; eligibility; CSRF, authorization,
request isolation and no persistence; the seven existing methods unchanged; EN / AR fidelity; and real-browser EN / AR
success and refusal journeys. Hosted required CI is the merge gate.

## 14. STOP conditions

Stop and return to the Owner on a source or IP deficiency, a need to incorporate external code or content, a contract
incompatibility, unprovable numerical integrity, an unqualified battery, runtime, temperature, rating, capability or
safety claim, or any scope expansion (another load type, method, consumer, unit, conversion, varying-power or integrated
energy, battery analysis, thermal analysis, circuit analysis, persistence or report surface).
