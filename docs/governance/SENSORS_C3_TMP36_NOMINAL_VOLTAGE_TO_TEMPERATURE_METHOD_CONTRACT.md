# SENSORS / INSTRUMENTATION C3 — TMP36 NOMINAL VOLTAGE-TO-TEMPERATURE METHOD CONTRACT

STATUS: OWNER-AUTHORIZED BOUNDED METHOD CONTRACT — written with, and governing, the one bounded implementation increment
`TMP36-NOMINAL-VOLTAGE-TEMPERATURE-01` (Slice 1), which the Owner authorized as ONE bounded implementation and ONE pull
request. Applicability: this contract governs the delivered method only on the verified merge of that pull request into
`feature/atomic-json-session-persistence`; on its proposal branch it describes an Owner-authorized proposed method, not a
merged or delivered capability. Merge, deployment, broad Sensors / Instrumentation activation, resumption of the paused D13
research and external dependency admission are NOT authorized by it.
AUTHORITY LEVEL: subordinate to the accepted
[shared deterministic calculation and units owner boundary contract](SHARED_DETERMINISTIC_CALCULATION_AND_UNITS_OWNER_BOUNDARY_CONTRACT.md)
(the "calc/units contract", with its Correction 05, §13D, added by the same increment). It amends no other method contract;
the two-support reactions, THERM-01, planar-moment and rotational-load methods stay unchanged. Where this document and the
calc/units contract differ, the calc/units contract wins and the difference is a defect of this document.

---

## 0. Preserved truth (binding)

- `ACTIVE CONTRACT: NONE` describes the state before and after this increment; this contract fills no active-contract slot
  after delivery and is not a delivery record. Current-truth delivery records belong to a later closure sync.
- This method enters, completes or reopens no Stage and changes no roadmap count (27 of 45 complete). Sensors /
  Instrumentation and 28-T1 are NOT complete; the CAP-09 measurement-planning C3 environmental-condition guidance stays
  SOURCE-BLOCKED and the paused D13 research stays paused. This is ONE device-specific method under the Sensors /
  Instrumentation C3 heading, not a sensor capability.
- No sensor selection, ADC, sampling, calibration, accuracy, compatibility or safety capability is added.

## 1. Purpose and scope

ONE optional, advisory, non-binding, request-local calculation: the NOMINAL temperature, on the Celsius scale, that the
nominal output characteristic of ONE explicitly declared Analog Devices TMP36 gives for ONE output voltage the inventor
declares. It lets an inventor who has read a voltage from a TMP36 — with their own instrument, or from their own
documentation — see what temperature the device's nominal relation assigns to it, with its limits stated. The voltage is
the inventor's declaration: InventorAI never reads, samples or measures the sensor.

Eligibility: the SAME `_calc_gate` / `_calc_declared_part` rule as THERM-01 in `web/app.py`: a project whose trusted durable
root domain is exactly `electronics_electrical`, or, whatever the initial analysis focus, the ONE inventor-declared
Electrical / Electronics part of a valid durable Stage-15 integrated composition, read only through the store-validated
composition and never from the request; the page names that part with the existing Electrical / Electronics attribution
wording. The Stage 15 exception in `engine/subsystem_model.py` names this method. A declared part makes the calculation
OFFERED only: it establishes no sensor choice, applicability, suitability, validation or safety and supplies no value,
declaration or screen answer. A missing, malformed, corrupt or unreadable composition grants nothing beyond the root rule
(fail closed). The session link, the page and the submission read the same one decision.

## 1A. Named downstream consumer (TEMPERATURE-TO-CONTROL-CONDITION-01) — narrow exception

Owner-authorized with that increment, and effective only on the verified merge of its pull request: ONE named
request-local consumer, the
[temperature-to-control-condition composition](TEMPERATURE_TO_CONTROL_CONDITION_COMPOSITION_CONTRACT.md)
(`engine/temperature_control_condition.py`), may invoke this method's consumer within one request and use the result of a
SUCCESS — the exact decimal nominal temperature this consumer accepted, returned with the success as `nominal_temperature`
— as the left-hand value of its one fixed comparison with an inventor-declared threshold. A refusal gives that consumer
nothing. This exception names that consumer only; it changes no equation, declaration, screen, interval, numerical or
decimal-reference acceptance, refusal, display, eligibility or source record of this method, adds no consumer or binding
to the shared deterministic calculation owner (the composition reaches the owner only through this consumer and its
existing binding), and authorizes no other consumer, persistence, report, export or transfer between requests.

## 2. Method identity and version

Identity `tmp36:nominal_voltage_to_temperature`, version `1.0`. Method-authority artifact
`docs/governance/tmp36_content_config/nominal_voltage_to_temperature_v1.json`
(`tmp36_nominal_voltage_to_temperature`, artifact version `1`), separate from every other artifact; none loads another.
Adapter `engine/tmp36_nominal_temperature_method.evaluate`; consumer `engine/tmp36_nominal_temperature.py`.

## 3. Method definition

`T = (V_OUT − 500) / 10`, with `V_OUT` in mV and `T` in °C. It is InventorAI's own solved form of the nominal TMP36 output
characteristic `V_OUT = 500 mV + (10 mV/°C) × T` (§11): an offset of 500 mV at 0 °C and a scale factor of 10 mV/°C, which
also gives the data sheet's 750 mV at 25 °C. The data sheet is not claimed to print the solved form. `T` is signed and is
exactly zero at exactly 500 mV. The result is the NOMINAL temperature of the relation: never a measured, calibrated,
accurate or guaranteed device temperature. The relation is restated independently; no data-sheet text, table, figure,
model or code is copied, and InventorAI does not show that the relation describes the inventor's device.

## 4. Roles, quantity kinds and exact unit tokens

| Role | Meaning | Quantity kind | Exact unit token |
|---|---|---|---|
| `v_out` (`V_OUT`) | the TMP36 output voltage relative to its ground pin, as declared by the inventor | `voltage` | `mV` |
| `t_celsius` (`T`) | the nominal temperature on the Celsius scale given by the relation; signed | `celsius_temperature` | `°C` |

The units are fixed and shown, never chosen; no unit is converted. `celsius_temperature` is admitted for this method's
output only (calc/units §13D): it is never converted to or from `K` and never related to THERM-01's temperature difference.

## 5. Applicability declarations (the TMP36 / model-applicability acknowledgement)

Each is shown as its own statement and answered «applies» or «does not apply», none pre-selected. A missing answer is
`NOT_DECLARED`; «does not apply» is `MODEL_NOT_SUPPORTED`. InventorAI infers none of them; D-1 is the explicit TMP36
acknowledgement and D-4 the explicit nominal-model acknowledgement.

| Ref | Id | Accepted statement |
|---|---|---|
| D-1 | `device_tmp36` | the sensor is an Analog Devices TMP36, not a TMP35, a TMP37 or any other sensor, as the inventor declares; InventorAI does not identify or check the device |
| D-2 | `declared_voltage` | the voltage entered is the inventor's own value for this TMP36's output pin relative to its ground pin, taken from their own reading or documentation; InventorAI did not sample, measure or check it |
| D-3 | `datasheet_conditions` | the sensor is powered and loaded as its data sheet specifies, and the voltage was read with the sensor in steady conditions within its specified temperature range |
| D-4 | `nominal_only` | only the nominal relation is wanted: the device's accuracy and linearity errors, self-heating, calibration, the measuring instrument or ADC and every other error are not included |

## 6. Numeric domain and numerical acceptance

- **Grammar.** Strict unsigned ASCII decimal: digits with an optional single fractional part of one to three digits; no sign,
  plus sign, exponent, separator, Unicode digit, unit suffix, `inf`, `nan` or normalization. The three-digit limit is a
  representation rule (every admitted value is a whole number of thousandths of a millivolt); it implies no measurement
  resolution. The field is capped at 64 characters for abuse protection only — a NON-PHYSICAL bound. An omitted, malformed
  or over-length value is `INVALID_NUMERIC_INPUT`.
- **Nominal-model interval.** The EXACT decimal value of `V_OUT` must lie in 100 mV to 1750 mV inclusive, decided before any
  binary rounding (`100` and `1750` inside; `99.999` and `1750.001` outside); otherwise `OUTSIDE_NOMINAL_MODEL_RANGE` with no
  number. The interval is the nominal relation applied to the stated TMP36 specified range of −40 °C to +125 °C. It is NOT
  the data sheet's electrical Output Voltage Range specification (a separate Table 1 entry, 100 mV to 2000 mV) and NOT a
  claim of guaranteed device accuracy.
- **Binary bridge (the smallest sound bridge to the shared owner).** The admitted decimal is converted ONCE to the correctly
  rounded binary64 value (round half to even) and handed to the owner as a typed number; the owner still parses no string
  (calc/units §10). Because `100` and `1750` are exact in binary64 and rounding is monotonic, an admitted value stays inside
  the interval, and exactly `500` stays exactly `500`.
- **Owner applicability.** The method record declares the existing `greater_than_zero` on `v_out`; a non-positive value that
  reaches the owner is `UNABLE_TO_DETERMINE / INPUT_OUTSIDE_ADMITTED_RANGE`, shown as the neutral `UNMAPPED_OWNER_OUTCOME`
  (unreachable from the page). The interval itself is never an owner range policy.
- **Binary acceptance (adapter).** The exact rational value `(V_OUT − 500) / 10` of the binary input is rounded ONCE to
  binary64. Exactly 500 mV gives exactly `0.0`. A nonzero exact result is accepted only when the rounded value is finite,
  nonzero, of the exact result's sign, `|T − exact| ≤ 2^-52 · |exact|` and inside −40 to 125. A value outside the interval
  that reaches the adapter, or any failed check, is `FAILURE / EXECUTION_INTEGRITY_FAILURE` with no numerical payload,
  displayed as `KNOWLEDGE_UNAVAILABLE`, never rewritten as a refusal. Overflow and underflow cannot occur: every operand and
  result is bounded (|`V_OUT`| ≤ 1750, |`T`| ≤ 125) and every nonzero exact result has magnitude at least `10^-4`.
- **Decimal-reference acceptance (consumer).** A successful owner result is shown only when it agrees with the exact decimal
  relation of the ENTERED decimal: exactly zero when, and only when, `V_OUT` is exactly 500; otherwise of the same sign and
  within `2^-45` °C. Proof that the bound always holds: `|V − D| ≤ 2^-43` mV for the rounded input `V` of a decimal `D <
  2048`, so the relation moves by at most `2^-43 / 10` °C; the single rounding of `T` (|`T`| < 128) adds at most `2^-47`
  °C; the total is at most `1.3 × 2^-46 < 2^-45` °C. Because every nonzero exact result is at least `10^-4` °C from zero,
  sign and zero are preserved. A failed check is `KNOWLEDGE_UNAVAILABLE` with no number.
- **Display.** The accepted result is shown as the exact decimal value of the nominal relation for the entered decimal, with
  at least one and at most four digits after the decimal point (every admitted input gives a whole number of
  ten-thousandths of a degree, so no rounding is needed or applied; `750.1` mV shows `25.01 °C`, `500` shows `0.0 °C`). The
  number of digits shown implies no measurement resolution, precision or accuracy.
- These rules belong to this method only; none is a generic owner numerical policy.

## 7. Refusal and abstention semantics

Order after request integrity (CSRF), project authorization, eligibility and strict capture (a malformed request — an
unknown or repeated field, or an answer outside its closed choices — is a bare 400 with no reason token): (1) completeness —
every declaration and screen item answered, else `NOT_DECLARED`; (2) screen — any YES is `ENGINEERING_REVIEW_REQUIRED` and
the owner is not invoked; (3) declarations — any «does not apply» is `MODEL_NOT_SUPPORTED`; (4) numeric grammar —
`INVALID_NUMERIC_INPUT`; (5) nominal-model interval — `OUTSIDE_NOMINAL_MODEL_RANGE`; (6) the shared owner; (7) the
decimal-reference acceptance — `KNOWLEDGE_UNAVAILABLE`. The first failing stage alone decides. Owner correspondence:
`REFUSAL / INVALID_NUMERIC_INPUT` → `INVALID_NUMERIC_INPUT`; `REFUSAL / UNIT_NOT_ADMITTED` or `UNKNOWN_UNIT` →
`UNIT_NOT_SUPPORTED`; `REFUSAL / METHOD_NOT_REGISTERED` or `VERSION_MISMATCH`, `UNABLE / SOURCE_UNAVAILABLE` and
`FAILURE / EXECUTION_INTEGRITY_FAILURE` → `KNOWLEDGE_UNAVAILABLE`; any other owner state → the neutral
`UNMAPPED_OWNER_OUTCOME`. The owner state and token are preserved, never rewritten.

## 8. High-risk screen (declared; not a safety engine)

Seven items, answered yes or no, none pre-selected, about uses where relying on a nominal temperature could put people or
property at risk — whether the temperature will be relied on for, or the sensor sits in or on: a battery or energy-storage
cell; mains or high voltage; fire or ignition risk; body temperature, skin contact or medical use; a safety-critical or
life-supporting function, alarm or shut-off; aerospace or vehicle use; food safety or storage-temperature decisions. The
first six item identities are THERM-01's, and the first, second, third and sixth also keep THERM-01's wording; the fourth
and fifth are reworded for a temperature reading and `food_safety` is this method's own. All
NO answers only allow this bounded calculation to proceed and never mean safe. The screen neither reads nor feeds
SafetySignal.

## 9. Result, provenance and fixed disclosure

On success the page shows `T` in °C as the exact decimal value (§6) with its sign, the declared voltage as entered, the
labels `UNVALIDATED` and `NOT EVIDENCE`, the method identity and version, the method source and unit records the owner
carried, the inputs echoed and this fixed disclosure (English; pinned equal to the artifact):

1. This is the nominal temperature that the TMP36 relation gives for the output voltage V_OUT you entered: T = (V_OUT − 500 mV) / (10 mV/°C).
2. The voltage is your own declared value. InventorAI did not read, sample or measure your sensor and does not check the value or that the sensor is a TMP36.
3. It is the nominal relation only. A real TMP36 can differ from it by several degrees, as its data sheet specifies, and no accuracy, linearity, self-heating, calibration, instrument or ADC error is included.
4. The accepted voltage interval, 100 mV to 1750 mV, is the nominal relation applied to the sensor's specified range of −40 °C to +125 °C. It is not the data sheet's output-voltage specification and does not mean the device is accurate inside it.
5. The number of digits shown follows from your entry; it is not the precision of the sensor or of any measurement.
6. It is preliminary, advisory, UNVALIDATED and not evidence, and it must be confirmed by measurement before any reliance; it says nothing about sensor choice, suitability or safety.
7. Reference source material: Analog Devices TMP35/TMP36/TMP37 data sheet, Rev. H (© Analog Devices, Inc.); the relation is restated by InventorAI, and no data-sheet text, table or figure is reproduced.

## 9A. Arabic disclosure and UX wording

**A-1 Fixed disclosure (Arabic rendering of the seven §9 items, item by item; no meaning added, removed or softened).**

> 1. هذه هي درجة الحرارة الاسمية التي تعطيها علاقة TMP36 لجهد الخرج V_OUT الذي أدخلته: T = (V_OUT − 500 mV) / (10 mV/°C).
> 2. الجهد قيمة صرّحت بها أنت. لم يقرأ InventorAI حسّاسك ولم يأخذ منه عينات ولم يقسه، ولا يتحقق من القيمة ولا من أن الحسّاس من طراز TMP36.
> 3. هذه هي العلاقة الاسمية فقط. قد تختلف قراءة حسّاس TMP36 حقيقي عنها بعدة درجات، كما تنص ورقة بياناته، ولا يتضمن الحساب أي خطأ في الدقة أو الخطية أو التسخين الذاتي أو المعايرة أو أداة القياس أو المحوّل التناظري الرقمي (ADC).
> 4. مجال الجهد المقبول، من 100 mV إلى 1750 mV، هو ناتج تطبيق العلاقة الاسمية على المدى المحدد للحسّاس من −40 °C إلى +125 °C. وهو ليس مواصفة جهد الخرج في ورقة البيانات، ولا يعني أن الجهاز دقيق داخله.
> 5. عدد الأرقام المعروضة ناتج عن إدخالك؛ وليس دقة الحسّاس أو دقة أي قياس.
> 6. هذه النتيجة أولية وإرشادية، وغير مُتحقَّق منها (UNVALIDATED)، وليست دليلًا، ويجب تأكيدها بالقياس قبل الاعتماد عليها؛ ولا تقول شيئًا عن اختيار الحسّاس أو الملاءمة أو السلامة.
> 7. المراجع: ورقة بيانات Analog Devices لـ TMP35/TMP36/TMP37، المراجعة Rev. H (© Analog Devices, Inc.)؛ والعلاقة معاد صياغتها من InventorAI، ولا يُستنسخ أي نص أو جدول أو شكل من ورقة البيانات.

**A-2 Applicability declarations (§5).** The inventor answers «ينطبق على حالتي» or «لا ينطبق على حالتي», none pre-selected.

| §5 | Arabic statement |
|---|---|
| D-1 device_tmp36 | الحسّاس من طراز Analog Devices TMP36، وليس TMP35 ولا TMP37 ولا أي حسّاس آخر، بحسب تصريحك؛ ولا يتعرّف InventorAI على الجهاز ولا يتحقق منه. |
| D-2 declared_voltage | الجهد المُدخل قيمتك أنت لطرف الخرج في هذا الحسّاس بالنسبة إلى طرف الأرضي فيه، مأخوذة من قراءتك أو من وثائقك؛ ولم يأخذ InventorAI منها عينة ولم يقسها ولم يتحقق منها. |
| D-3 datasheet_conditions | الحسّاس مغذّى ومحمَّل كما تحدد ورقة بياناته، وقُرئ الجهد والحسّاس في ظروف مستقرة ضمن مداه الحراري المحدد. |
| D-4 nominal_only | المطلوب العلاقة الاسمية فقط: لا تُدرج أخطاء الدقة والخطية في الجهاز، ولا التسخين الذاتي، ولا المعايرة، ولا أداة القياس أو المحوّل التناظري الرقمي (ADC)، ولا أي خطأ آخر. |

**A-3 Screen (§8).**

| §8 | Arabic item |
|---|---|
| battery_or_storage_cell | بطارية أو خلية لتخزين الطاقة |
| mains_or_high_voltage | جهد الشبكة الكهربائية (mains) أو جهد عالٍ |
| fire_or_ignition | خطر حريق أو اشتعال |
| touch_skin_or_medical | حرارة الجسم، أو تلامس مع الجلد، أو استخدام طبي |
| safety_critical_or_life_supporting | وظيفة حرجة للسلامة أو داعمة للحياة، أو إنذار أو إيقاف |
| aerospace_or_vehicle | استخدام في الطيران والفضاء (aerospace) أو في المركبات |
| food_safety | قرارات سلامة الغذاء أو درجات حرارة التخزين |

**A-4 Right-to-left rendering.** Numbers, the role symbols `V_OUT` and `T`, the unit tokens `mV` and `°C`, the relation, the
method identity, `TMP36` and `UNVALIDATED` / `NOT EVIDENCE` are each direction-isolated on the Arabic page; the inventor's
typed value is shown left-to-right.

## 9B. Verification-preparation block (amendment `TMP36-NOMINAL-TEMPERATURE-VERIFICATION-PREPARATION-01`, 2026-10-29)

Presentation only; it changes no method identity, version, calculation, declaration, screen, numerical rule, refusal,
output, disclosure or source-use record.

- **Where and when.** ONE read-only block, "How to prepare to check this nominal temperature", is rendered only after a
  successful §9 result on the standalone TMP36 page. It is absent on a plain GET and on every refusal, abstention,
  malformed request or ineligible project / part, and it is not part of the `TEMPERATURE-TO-CONTROL-CONDITION-01`
  composition (§1A), whose behaviour is unchanged. Showing it validates nothing: the result stays `UNVALIDATED` and
  `NOT EVIDENCE`.
- **Purpose.** It lists what information may need to be available for an independently justified check; it is not a
  measurement or calibration procedure, a verdict or an instruction to perform a test. Its five items are InventorAI's own
  restatement of the admitted boundaries: (A) the sensor's identity and whether it is stated to be the TMP36 the
  calculation assumes (D-1); (B) the `V_OUT` used and whether it came from an independently obtained reading or from
  documentation or another inventor-supplied source, never presented as a measurement by InventorAI (D-2, §9 item 2);
  (C) the information showing whether the real supply, loading, steady conditions and temperature range correspond to the
  declared conditions (D-3); (D) what independent temperature measurement or reference, if any, would be available, with
  its target, location, conditions and relationship to the sensor clear enough for a qualified reviewer to judge
  comparability — an arbitrary room-temperature reading or one taken elsewhere is not assumed to represent the sensor's
  temperature; (E) the effects outside the nominal calculation — accuracy, linearity, self-heating, calibration,
  instrument error and, where applicable, ADC error (D-4, §9 item 3) — as factors for that check, none calculated here.
- **Distinction.** The declared `V_OUT`, the nominal temperature, an independently measured or referenced temperature, the
  device's accuracy and calibration, and engineering verification or validation are kept apart. Agreement with a reference
  does not by itself establish accuracy, calibration, suitability, safety or a validated design; disagreement does not by
  itself identify the source of error. Nothing is compared automatically.
- **Authority / source integrity.** No new scientific claim is admitted. The artifact
  `tmp36_content_config/nominal_voltage_to_temperature_v1.json` (version `1`), its pinned `ADI-S1` and `tmp36:SU001`
  records and every other source-use boundary stay byte-for-byte unchanged.
- **Boundary.** The §10 exclusions apply in full: no calibration procedure, sensor, instrument, ADC or reference
  recommendation, sampling, signal conditioning, reference-voltage procedure, accuracy, uncertainty, error budget,
  self-heating or response-time calculation, tolerance, pass / fail, automatic comparison, measured-value input or record,
  suitability or safety conclusion, and no persistence, report, PDF, export, evidence, readiness, progression, gap, CAP-09
  or SafetySignal effect.
- **Arabic.** The EN / AR block has the same meaning; `V_OUT`, `TMP36`, `ADC`, `UNVALIDATED` and `NOT EVIDENCE` are
  direction-isolated under the existing A-4 rule.

## 10. Exclusions (binding)

No sensor selection, recommendation or comparison; no ADC, sampling, signal conditioning, reference voltage or code
conversion; no calibration, offset or gain correction; no accuracy, linearity, uncertainty, self-heating, response-time or
error budget; no TMP35, TMP37 or other device; no supply, load or wiring check; no compatibility, suitability or safety
conclusion; no inference of the device, the voltage or any declaration, and no device measurement supplied by InventorAI;
no unit conversion, no Kelvin, Fahrenheit or temperature-difference result; no persistence, report, PDF, Structured
Export, API, evidence, readiness, progression, gap, CAP-09 or SafetySignal effect; no AI or provider call; no eligibility
for any part other than the one declared Electrical / Electronics part (§1).

## 11. Source and IP status

- **ADI-S1** — Analog Devices, Inc., *TMP35/TMP36/TMP37 Low Voltage Temperature Sensors*, data sheet, Rev. H (revision
  history entry 5/15 — Rev. G to Rev. H; ©1996–2015 Analog Devices, Inc.), canonical location
  <https://www.analog.com/media/en/technical-documentation/data-sheets/TMP35_36_37.pdf>. Claim-level support:
  - Table 4, *TMP35/TMP36/TMP37 Output Characteristics* (Theory of Operation, printed page 8 of 19): TMP36 offset voltage
    0.5 V, output voltage scaling 10 mV/°C, output voltage 750 mV at 25 °C — the nominal output characteristic (§3);
  - Table 1, *Specifications* (printed page 3 of 19; VS = 2.7 V to 5.5 V and −40 °C to +125 °C unless noted): scale factor
    of the TMP36 10 mV/°C (typical) over −40 °C to +125 °C, and TMP36 output voltage 750 mV (typical) at 25 °C;
  - page 1 (Features and General Description): the TMP36 is specified from −40 °C to +125 °C — the basis of the
    nominal-model interval (§6).
  - **Nominal model versus electrical specification.** Table 1 also specifies accuracy (±1 °C to ±4 °C, typical and maximum,
    by grade and temperature), linearity (0.5 °C typical), long-term stability, the supply range (2.7 V to 5.5 V), a separate
    Output Voltage Range (100 mV to 2000 mV) and, in its note 1, that the specifications do not consider self-heating
    errors. These are recorded as limits of the nominal model and are NOT applied or claimed: the result is the nominal
    relation only, and the method's 100–1750 mV interval is derived from the nominal relation, not from the Output Voltage
    Range specification.
- **Units** — `mV`: the volt (V) of NIST SP 811 Appendix B.9 with the prefix milli (m, 10⁻³) of Chapter 4, Table 5, as
  recorded in `electronics_electrical:PR005` and `electronics_electrical:PR020` (Lead-level inspections; owner record
  `dcu:U009`, source use `dcu:SU008`). `°C`: the degree Celsius, identified from `Modelica.Units` v4.1.0
  (`NonSI.Temperature_degC`, unit `degC`; `SI.ThermodynamicTemperature`, display unit `degC`; owner record `dcu:U010`,
  source use `dcu:SU009`, BSD 3-Clause, facts only).
- **Copyright and source use** (not a legal opinion): the data sheet is © Analog Devices, Inc., all rights reserved; it
  grants no patent licence by implication and no reproduction right is assumed. Use is a factual reference only: the
  nominal characteristic (an offset and a scale factor) and the stated specified range are restated independently in
  InventorAI's own words, with the publication identified and Analog Devices acknowledged. No data-sheet prose, table,
  figure, diagram, model or code is reproduced or redistributed, and no copy of the document enters the repository
  (`tmp36:SU001`; owner snapshot `dcu:SU010`). Analog Devices and TMP36 are named only to identify the device and the
  source; no endorsement is stated or implied. The Analog Devices website terms of use were not inspected (the host was not
  reachable from the executor environment) and no right beyond this factual reference is assumed.
- **Inspection basis.** The Lead / Owner supplied the publication, revision, relation and interval in the authorizing brief.
  The executor confirmed each claim and location on 2026-10-24 against a copy of the Rev. H document obtained from a public
  GitHub repository, because the Analog Devices host was not reachable; the copy was identified as Rev. H by its embedded
  document title, its printed page footers and its revision history (SHA-256
  `6ce062fb73f0bebb61f82775aca0be56903c2b8484a7fc89a0cf71961189f8ee`). No other source is relied upon.

## 12. Implementation boundary

The one existing shared owner executes the method through ONE additional immutable binding created by application wiring
(`_TMP36_TEMPERATURE_BINDING` in `web/app.py`), beside the four existing bindings; there is no registry, discovery, dynamic
module path or request-selected method (calc/units contract §13D). Routes: `GET` / `POST /session/<sid>/tmp36-temperature`,
behind the central project authorization and the global CSRF guard; the session page shows one optional link on an
eligible project. Nothing is persisted; the POST renders its result directly.

## 13. Verification

Focused tests (`tests/test_tmp36_nominal_temperature.py`, `tests/test_tmp36_nominal_temperature_browser.py`): the reference
vectors `(mV → °C)` `100 → −40`, `400 → −10`, `500 → 0`, `750 → 25`, `1000 → 50`, `1750 → 125`; just-inside and
just-outside boundaries; decimal fractions; the zero crossing; an independent exact-decimal reference over every admitted
thousandth of a millivolt near the boundaries and a random sample; overflow / underflow resistance; grammar; unit, method,
version and adapter integrity; owner artifact v5 and method artifact tamper; the §7 order and owner correspondence; root and
integrated-part eligibility and fail-closed composition; CSRF, authorization and no persistence; the four existing methods
unchanged; EN / AR fidelity; and real-browser EN / AR journeys. Hosted required CI is the merge gate.

## 14. STOP conditions

Stop and return to the Owner on a source or IP deficiency, a need to incorporate external code or content, a contract
incompatibility, unprovable numerical integrity, an unqualified accuracy or measurement claim or any scope expansion
(another device, method, consumer, unit, conversion, calibration or ADC capability, persistence or report surface).
