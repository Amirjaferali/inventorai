# ELECTRICAL / ELECTRONICS — DC RESISTIVE LOAD CURRENT METHOD CONTRACT

STATUS: OWNER-AUTHORIZED BOUNDED METHOD CONTRACT — written with, and governing, the one bounded implementation increment
`DC-RESISTIVE-LOAD-CURRENT-01` (Slice 1), which the Owner authorized as ONE bounded implementation and ONE pull request.
Applicability: this contract governs the delivered method only on the verified merge of that pull request into
`feature/atomic-json-session-persistence`; on its proposal branch it describes an Owner-authorized proposed method, not a
merged or delivered capability. Merge, deployment, Power Electronics / Motion (28-T3), D4 or T6 activation and any
persistence or sharing of calculation results are NOT authorized by it.
AUTHORITY LEVEL: subordinate to the accepted
[shared deterministic calculation and units owner boundary contract](SHARED_DETERMINISTIC_CALCULATION_AND_UNITS_OWNER_BOUNDARY_CONTRACT.md)
(the "calc/units contract", with its Correction 06, §13E, added by the same increment). It amends no other method contract;
the two-support reactions, THERM-01, planar-moment, rotational-load and TMP36 methods stay unchanged. Where this document
and the calc/units contract differ, the calc/units contract wins and the difference is a defect of this document.

---

## 0. Preserved truth (binding)

- `ACTIVE CONTRACT: NONE` describes the state before and after this increment; this contract fills no active-contract slot
  after delivery and is not a delivery record. Current-truth delivery records belong to a later closure sync.
- This method enters, completes or reopens no Stage and changes no roadmap count (27 of 45 complete). Power Electronics /
  Motion (28-T3) stays BLOCKED, D4 and T6 stay inactive, and the Stage 15 composition authority is unchanged.
- The Electrical / Electronics pack claim `ohms_law_reference` and the provenance records `electronics_electrical:PR004` to
  `PR007` are unchanged and keep their own scope (§11).

## 1. Purpose and scope

ONE optional, advisory, non-binding, request-local calculation: the theoretical steady current that ONE explicitly
declared DC resistive load draws at ONE declared voltage. It lets an inventor who knows, from their own reading or
documentation, the voltage across one load and its resistance see the current Ohm's law gives, with its sign convention,
its limits and the engineering checks that still remain. Nothing is inferred: InventorAI never decides that a project has
an ohmic load, and asks no generic question about loads.

Eligibility (method-specific): a project whose trusted durable root domain is exactly `electronics_electrical`, read as
the other calculation gates read it (`_cap12_root_domain` in `web/app.py`). Root only: no declared Stage 15 part grants this
method, and the Stage 15 exception in `engine/subsystem_model.py` does not name it. An unreadable domain grants nothing.
The session link, the page and the submission read the same one decision.

## 2. Method identity and version

Identity `electrical:dc_resistive_load_current`, version `1.0`. Method-authority artifact
`docs/governance/electrical_content_config/dc_resistive_load_current_v1.json`
(`electrical_dc_resistive_load_current`, artifact version `1`), separate from every other artifact; none loads another.
Adapter `engine/dc_resistive_load_current_method.evaluate`; consumer `engine/dc_resistive_load_current.py` (the one named
Electrical / Electronics consumer).

## 3. Method definition

`I = V / R`, with `V` in V, `R` in Ω and `I` in A, for `R > 0`. It is InventorAI's solved form of Ohm's law for a
resistive element, `V = I × R` (written `E = I × R` in the DOE handbook, §11); the handbook is not claimed to print the
solved form or the sign convention.

**Sign convention (fixed, documented).** `V` is the voltage across the load measured from the load terminal the inventor
calls `+` to the terminal they call `−`. `I` is the current through the load, positive when it flows through the load from
the `+` terminal to the `−` terminal (the passive reference direction). A negative `V` therefore gives a negative `I`,
flowing the opposite way. The signed value is always shown; it is never silently replaced by its magnitude. When `I` is
negative, its magnitude is shown on its own line, separately labelled as the magnitude.

The result is the theoretical current of the ideal relation only: never a measured, rated, maximum or guaranteed current.

## 4. Roles, quantity kinds and exact unit tokens

| Role | Meaning | Quantity kind | Exact unit token |
|---|---|---|---|
| `v_load` (`V`) | the steady DC voltage across the load, `+` to `−`, as declared; signed | `voltage` | `V` |
| `r_load` (`R`) | the constant resistance of the load, as declared; strictly positive | `electric_resistance` | `Ω` (U+03A9) |
| `i_load` (`I`) | the theoretical steady current through the load; signed | `electric_current` | `A` |

The units are fixed and shown, never chosen; no unit is converted. `V` is a second exact token of the `voltage` kind beside
the TMP36 method's `mV` (calc/units §13E); nothing relates the two, and a value in `mV` is not accepted here.

## 5. Applicability declarations (the model-applicability confirmation)

Each is shown as its own statement and answered «applies» or «does not apply», none pre-selected. A missing answer is
`NOT_DECLARED`; «does not apply» is `MODEL_NOT_SUPPORTED`. InventorAI infers none of them; D-2 is the explicit confirmation
that the load is resistive and D-4 the explicit confirmation of the sign convention.

| Ref | Id | Accepted statement |
|---|---|---|
| D-1 | `steady_state_dc` | the voltage across the load is a steady DC voltage that stays constant during the period of interest; no AC, pulsed, switching, start-up or inrush condition is being calculated |
| D-2 | `resistive_load` | the load behaves as one resistance that stays constant at this voltage (a resistive, ohmic load), not a motor, lamp, LED, battery, electronic circuit or other load whose current does not follow V / R; InventorAI does not determine that the load is resistive |
| D-3 | `declared_values` | the voltage and resistance entered are the inventor's own values for this one load, taken from their own reading or documentation; InventorAI did not measure or check them |
| D-4 | `sign_convention` | the voltage is entered with the stated reference direction, from the load terminal the inventor calls + to the terminal they call −; a positive current then flows through the load from + to −, and a negative voltage gives a current in the opposite direction |

## 6. Numeric domain and numerical acceptance

- **Grammar (strict capture).** Strict ASCII decimal: an optional single leading minus, then one to nine integer digits
  for `V` or one to twelve for `R`, and an optional single fractional part of one to nine digits. No plus sign, exponent,
  separator, space, Unicode digit, unit suffix, `inf`, `nan` or normalization. A field sent twice, an unknown field or a
  declaration / screen answer outside its closed choices makes the whole request malformed (a bare 400). An omitted,
  malformed or over-length value is `INVALID_NUMERIC_INPUT`.
- **Representation limits are not physical limits.** The digit limits bound what can be typed: `|V| < 10^9` V; `R` from
  `10^-9` to below `10^12` Ω; steps of `10^-9`. They are NOT physical limits, equipment ratings or a claim that such values
  are realistic. The 64-character field cap is abuse protection only — a NON-PHYSICAL bound.
- **Positive resistance.** The EXACT decimal value of `R` must be greater than zero, decided before any binary rounding;
  zero (including `-0`) or a negative value is `RESISTANCE_NOT_POSITIVE` with no number. A zero voltage (including `-0`) is
  admitted and gives exactly `0` A.
- **Binary bridge.** Each admitted decimal is converted ONCE to the correctly rounded binary64 value (round half to even)
  and handed to the owner as a typed number; the owner parses no string (calc/units §10). Every admitted nonzero value lies
  between `10^-9` and `10^12` in magnitude, so it is a normal binary64 number with relative rounding error at most `2^-53`;
  a positive `R` stays positive and a zero `V` stays exactly zero.
- **Owner applicability.** The method record declares the existing `greater_than_zero` on `r_load`; a non-positive value
  that reaches the owner is `UNABLE_TO_DETERMINE / INPUT_OUTSIDE_ADMITTED_RANGE`, shown as the neutral
  `UNMAPPED_OWNER_OUTCOME` (unreachable from the page). No result range is declared: the current is signed.
- **Binary acceptance (adapter).** The exact rational value `v_load / r_load` of the binary inputs is rounded ONCE to
  binary64. A zero voltage gives exactly `0.0`. A nonzero exact result is accepted only when the rounded value is finite,
  nonzero, of the exact result's sign and `|I − exact| ≤ 2^-52 · |exact|`. Overflow, underflow of a nonzero result to zero
  or any failed check is `FAILURE / EXECUTION_INTEGRITY_FAILURE` with no numerical payload, displayed as
  `KNOWLEDGE_UNAVAILABLE`, never rewritten as a refusal. Representability: inside the representation limits every nonzero
  result lies between `10^-21` and `10^18` A in magnitude, well inside the normal binary64 range, so neither overflow nor
  underflow can occur from the page; the guards stay in place for direct owner use.
- **Decimal-reference acceptance (consumer).** A successful owner result is shown only when it agrees with the exact
  decimal quotient `V / R` of the ENTERED decimals: exactly zero when, and only when, `V` is exactly zero; otherwise of the
  same sign and within a relative error of `2^-51`. Proof that the bound always holds: with `u = 2^-53`, each binary input
  carries a relative error of at most `u`, so the exact quotient of the binary inputs lies within `(1+u)/(1−u) − 1` of the
  decimal quotient, and the single rounding adds at most `u`; the total is at most `(1+u)²/(1−u) − 1 < 3.0000001 · u <
  2^-51`. A failed check is `KNOWLEDGE_UNAVAILABLE` with no number.
- **Display.** The shown value is derived from the exact decimal quotient, never from the binary value: rounded ONCE to 12
  significant digits, round half to even, with trailing zeros removed. It is labelled **exact** when that rounding changes
  nothing and **rounded to 12 significant digits** otherwise, so exactness is never silently asserted (`12 / 24` shows
  `0.5`, exact; `1 / 3` shows `0.333333333333`, rounded). Plain decimal notation is used for `10^-6 ≤ |I| < 10^12` A and
  the form `m × 10^e` otherwise, so a tiny nonzero current is never shown as `0` (`0.000000001 V` across
  `999999999999.999999999 Ω` shows `1 × 10^-21`, rounded). The digits shown imply no measurement resolution, precision or
  accuracy.
- These rules belong to this method only; none is a generic owner numerical policy.

## 7. Refusal and abstention semantics

Order after request integrity (CSRF), project authorization, eligibility and strict capture (a malformed request is a bare
400 with no reason token): (1) completeness — every declaration and screen item answered, else `NOT_DECLARED`; (2) screen
— any YES is `ENGINEERING_REVIEW_REQUIRED` and the owner is not invoked; (3) declarations — any «does not apply» is
`MODEL_NOT_SUPPORTED`; (4) numeric grammar — `INVALID_NUMERIC_INPUT`; (5) positive resistance — `RESISTANCE_NOT_POSITIVE`;
(6) the shared owner; (7) the decimal-reference acceptance — `KNOWLEDGE_UNAVAILABLE`. A method artifact that is missing,
unreadable or changed is `KNOWLEDGE_UNAVAILABLE` before any of these. The first failing stage alone decides; no refusal
carries a number. Owner correspondence: `REFUSAL / INVALID_NUMERIC_INPUT` → `INVALID_NUMERIC_INPUT`;
`REFUSAL / UNIT_NOT_ADMITTED` or `UNKNOWN_UNIT` → `UNIT_NOT_SUPPORTED`; `REFUSAL / METHOD_NOT_REGISTERED` or
`VERSION_MISMATCH`, `UNABLE / SOURCE_UNAVAILABLE` and `FAILURE / EXECUTION_INTEGRITY_FAILURE` → `KNOWLEDGE_UNAVAILABLE`;
any other owner state → the neutral `UNMAPPED_OWNER_OUTCOME`. The owner state and token are preserved, never rewritten.

## 8. High-risk screen (declared; not a safety engine)

Six items, answered yes or no, none pre-selected — whether the load is, is powered by or is part of: mains or high
voltage; a battery or energy-storage cell; fire, ignition or overheating risk; medical or life-supporting use; vehicle or
aerospace use; a safety function, alarm, protection or shut-off. All NO answers only allow this bounded calculation to
proceed and never mean safe. The screen neither reads nor feeds SafetySignal.

## 9. Result, provenance and fixed disclosure

On success the page shows `I` in A with its sign and its exact / rounded label, the magnitude separately when `I` is
negative, the declared inputs as entered with their units, the stated assumptions (D-1 to D-4), the labels `UNVALIDATED`
and `NOT EVIDENCE`, the method identity and version, the method source and unit records the owner carried, and this fixed
disclosure (English; pinned equal to the artifact). Item 6 is the next engineering need.

1. This is the theoretical current that Ohm's law gives for the steady DC voltage V across one resistive load and its resistance R that you declared: I = V / R.
2. Sign: V is the voltage across the load from the terminal you called + to the terminal you called −. A positive I flows through the load from + to −; a negative V gives a negative I, flowing the opposite way.
3. The voltage and resistance are your own declared values. InventorAI did not measure them and does not check that the load is resistive, that its resistance stays constant or that the voltage is steady.
4. It is the ideal steady-state relation only: wiring and contact resistance, the source's internal resistance and voltage drop, temperature change of the resistance, start-up or inrush current, switching, AC behaviour and non-resistive loads such as motors, lamps, LEDs or electronics are not included.
5. The value is shown exactly when it can be; otherwise it is rounded to 12 significant digits and labelled rounded. The digits follow from your entry; they are not the precision of any measurement.
6. Next engineering need: whether your source and any driver or switch can supply this current, what protection the circuit needs and whether the load and its wiring are suitable all remain unverified, and must be checked by measurement or a qualified person before any reliance. The result is preliminary, advisory, UNVALIDATED and not evidence.
7. Reference source material: U.S. Department of Energy — Electrical Science, DOE-HDBK-1011/1-92 (archived; historical fundamentals reference only); the relation is restated by InventorAI, and no handbook text, example or figure is reproduced.

## 9A. Arabic disclosure and UX wording

**A-1 Fixed disclosure (Arabic rendering of the seven §9 items, item by item; no meaning added, removed or softened).**

> 1. هذا هو التيار النظري الذي يعطيه قانون أوم (Ohm's law) لجهد مستمر ثابت V على حِمل مقاوم واحد ولمقاومته R اللذين صرّحت بهما: I = V / R.
> 2. الإشارة: V هو الجهد على الحِمل من الطرف الذي سمّيته + إلى الطرف الذي سمّيته −. التيار I الموجب يسري عبر الحِمل من + إلى −؛ والجهد V السالب يعطي تيارًا I سالبًا يسري في الاتجاه المعاكس.
> 3. الجهد والمقاومة قيمتان صرّحت بهما أنت. لم يقسهما InventorAI، ولا يتحقق من أن الحِمل مقاوم، ولا من أن مقاومته تبقى ثابتة، ولا من أن الجهد ثابت.
> 4. هذه هي العلاقة المثالية في الحالة المستقرة فقط: لا تُدرج مقاومة الأسلاك والتلامس، ولا المقاومة الداخلية للمصدر وهبوط جهده، ولا تغيّر المقاومة مع الحرارة، ولا تيار بدء التشغيل أو التيار الاندفاعي (inrush)، ولا التبديل، ولا سلوك التيار المتردد (AC)، ولا الأحمال غير المقاومة مثل المحركات والمصابيح والثنائيات الباعثة للضوء (LED) والدوائر الإلكترونية.
> 5. تُعرض القيمة بدقة حين يمكن ذلك؛ وإلا تُقرَّب إلى 12 رقمًا معنويًا ويُشار إلى أنها مقرَّبة. الأرقام ناتجة عن إدخالك؛ وليست دقة أي قياس.
> 6. الحاجة الهندسية التالية: قدرة مصدرك وأي مُشغِّل (driver) أو مفتاح على توفير هذا التيار، والحماية التي تحتاجها الدائرة، وملاءمة الحِمل وأسلاكه — كلها تبقى غير مُتحقَّق منها، ويجب فحصها بالقياس أو بواسطة شخص مؤهل قبل أي اعتماد. هذه النتيجة أولية وإرشادية، وغير مُتحقَّق منها (UNVALIDATED)، وليست دليلًا.
> 7. المراجع: وزارة الطاقة الأمريكية — Electrical Science، ‏DOE-HDBK-1011/1-92 (مؤرشف؛ مرجع تاريخي للأساسيات فقط)؛ والعلاقة معاد صياغتها من InventorAI، ولا يُستنسخ أي نص أو مثال أو شكل من الدليل.

**A-2 Applicability declarations (§5).** The inventor answers «ينطبق على حالتي» or «لا ينطبق على حالتي», none pre-selected.

| §5 | Arabic statement |
|---|---|
| D-1 steady_state_dc | الجهد على الحِمل جهد مستمر (DC) ثابت يبقى كما هو خلال الفترة المعنية؛ ولا يُحسب أي تيار متردد (AC) أو نبضي أو تبديل أو بدء تشغيل أو تيار اندفاعي. |
| D-2 resistive_load | يتصرف الحِمل كمقاومة واحدة تبقى ثابتة عند هذا الجهد (حِمل مقاوم أومي)، وليس محركًا أو مصباحًا أو ثنائيًا باعثًا للضوء (LED) أو بطارية أو دائرة إلكترونية أو أي حِمل آخر لا يتبع تياره V / R؛ ولا يحدد InventorAI أن الحِمل مقاوم. |
| D-3 declared_values | الجهد والمقاومة المُدخلان قيمتاك أنت لهذا الحِمل الواحد، مأخوذتان من قراءتك أو من وثائقك؛ ولم يقسهما InventorAI ولم يتحقق منهما. |
| D-4 sign_convention | أُدخل الجهد باتجاه المرجع المذكور — من طرف الحِمل الذي تسمّيه + إلى الطرف الذي تسمّيه − — فيسري التيار الموجب عبر الحِمل من + إلى −، ويعطي الجهد السالب تيارًا في الاتجاه المعاكس. |

**A-3 Screen (§8).**

| §8 | Arabic item |
|---|---|
| mains_or_high_voltage | جهد الشبكة الكهربائية (mains) أو جهد عالٍ |
| battery_or_storage_cell | بطارية أو خلية لتخزين الطاقة |
| fire_or_overheating | خطر حريق أو اشتعال أو سخونة زائدة |
| medical_or_life_supporting | استخدام طبي أو داعم للحياة |
| vehicle_or_aerospace | استخدام في المركبات أو في الطيران والفضاء (aerospace) |
| safety_function | وظيفة سلامة أو إنذار أو حماية أو إيقاف |

**A-4 Right-to-left rendering.** Numbers, the role symbols `V`, `R` and `I`, the unit tokens `V`, `Ω` and `A`, the relation,
the method identity and `UNVALIDATED` / `NOT EVIDENCE` are each direction-isolated on the Arabic page; the inventor's typed
values are shown left-to-right, so a leading minus stays attached to its number.

## 10. Exclusions (binding)

No source, power-supply, driver, switch, transistor, relay, wire, connector, fuse or component capability, rating or
selection; no protection design; no power, heating or energy result; no Kirchhoff, network, series / parallel or circuit
solving; no AC, transient, inrush or switching analysis; no motor, lamp, LED, battery or other non-resistive load; no
compatibility, suitability or safety conclusion; no inference of the load type, the voltage, the resistance or any
declaration, and no generic load question; no unit conversion (no `mV`, `mA` or `kΩ`); no persistence, report, PDF,
Structured Export, API, evidence, readiness, progression, gap or SafetySignal effect; no AI or provider call; no Stage 15
part eligibility (§1); no 28-T3, D4 or T6 activation.

## 11. Source and IP status

- **DOE-OHM-S1** — U.S. Department of Energy, *DOE Fundamentals Handbook: Electrical Science*, Volume 1 of 4, Module 1 —
  Basic Electrical Theory (DOE-HDBK-1011/1-92), Ohm's Law, handbook page 14: `E = I × R`, with `E` the voltage in volts,
  `I` the current in amperes and `R` the resistance in ohms. Official DOE record status ARCHIVE — Canceled, effective April
  2016: used ONLY as a historical / fundamentals reference for this one factual relationship, never as current regulatory,
  safety or compliance guidance. This record reuses the Lead-level inspection recorded as `electronics_electrical:PR004`
  (2026-09-28; executor egress was blocked); no new source research was performed and the executor did not re-inspect it.
- **Pack scope note.** `electronics_electrical:PR004` and the pack claim `ohms_law_reference` say "no project-specific
  calculation" for the reference-fundamentals group they serve. They are unchanged and keep that scope: this method is a
  separately Owner-authorized method with its own method authority, source record and source-use record (the same pattern
  as THERM-01's own DOE records beside its pack references), not an extension of the pack claim.
- **Units** — `V`, `Ω` and `A`: NIST SP 811 Appendix B.9, as recorded in `electronics_electrical:PR005` (Lead-level
  inspection, 2026-09-28; owner records `dcu:U011` to `dcu:U013`, source use `dcu:SU011`, the NIST policy recorded as
  `electronics_electrical:PR007`).
- **Source use** (not a legal opinion): the `electronics_electrical:PR006` disposition applied to this method
  (`dcload:SU001`; owner snapshot `dcu:SU012`) — DOE website government information is public domain with DOE
  acknowledgement requested; contractor- or privately contributed material may remain protected, so no blanket
  public-domain claim is made for the handbook's expressive content. Use is the one factual relationship only, restated in
  InventorAI's own words with `V` for voltage (notation normalization only); the solved form, the positive-resistance domain
  and the sign convention are InventorAI's own statement; the mathematics is implemented independently; no handbook prose,
  worked example, figure, diagram, photograph or logo is copied; DOE is acknowledged neutrally and no endorsement is stated
  or implied. `electronics_electrical:PR006` is not broadened beyond this method.

## 12. Implementation boundary

The one existing shared owner executes the method through ONE additional immutable binding created by application wiring
(`_DC_LOAD_CURRENT_BINDING` in `web/app.py`), beside the five existing bindings; there is no registry, discovery, dynamic
module path or request-selected method (calc/units contract §13E). Routes: `GET` / `POST /session/<sid>/dc-load-current`,
behind the central project authorization and the global CSRF guard; the session page shows one optional link on an
eligible project. Nothing is persisted; the POST renders its result directly.

## 13. Verification

Focused tests (`tests/test_dc_resistive_load_current.py`, `tests/test_dc_resistive_load_current_browser.py`): the reference
vectors `12 V / 24 Ω = +0.5 A` and `5 V / 10 Ω = +0.5 A`; a negative voltage giving a signed negative current with its
separate magnitude; exact decimal quotients and nonterminating ones (`1 / 3`); zero voltage; zero, `-0` and negative
resistance; tiny, large and representation-limit values; an independent exact-rational oracle over a random sample;
missing, malformed, duplicate and contradictory declarations; grammar; unit, method, version, adapter and artifact
integrity, with no number on any refusal; owner artifact v6 and the voltage token exception; the §7 order and owner
correspondence; eligibility; CSRF, authorization, request isolation and no persistence; the five existing methods
unchanged; EN / AR fidelity; and real-browser EN / AR success and refusal journeys. Hosted required CI is the merge gate.

## 14. STOP conditions

Stop and return to the Owner on a source or IP deficiency, a need to incorporate external code or content, a contract
incompatibility, unprovable numerical integrity, an unqualified rating, capability or safety claim, or any scope expansion
(another load type, method, consumer, unit, conversion, circuit analysis, persistence or report surface).
