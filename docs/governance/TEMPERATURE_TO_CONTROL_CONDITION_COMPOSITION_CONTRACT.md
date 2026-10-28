# TEMPERATURE-TO-CONTROL-CONDITION-01 — TMP36 NOMINAL TEMPERATURE → THRESHOLD → READY / RUNNING CYCLE — SLICE 1 CONTRACT

STATUS: OWNER-AUTHORIZED BOUNDED CONTRACT — written with, and governing, the one bounded implementation increment
`TEMPERATURE-TO-CONTROL-CONDITION-01` (Slice 1), which the Owner authorized as ONE bounded product increment and ONE pull
request. Applicability: this contract governs the delivered composition only on the verified merge of that pull request
into `feature/atomic-json-session-persistence`; on its proposal branch it describes an Owner-authorized proposed
capability, not a merged or delivered one. Merge, deployment, D4 activation, general PLC / Mechatronics activation and
wider cross-consumer integration are NOT authorized by it.
AUTHORITY LEVEL: subordinate to the
[TMP36 nominal voltage-to-temperature method contract](SENSORS_C3_TMP36_NOMINAL_VOLTAGE_TO_TEMPERATURE_METHOD_CONTRACT.md)
(the "TMP36 contract") and the
[28-T4 control-cycle contract](STAGE28_T4_CONTROL_CYCLE_READY_RUNNING_CONTRACT.md) (the "28-T4 contract"), each of which
records ONE named consumer exception for this composition (TMP36 contract §1A; 28-T4 contract §6A) and is otherwise
unchanged. Where this document and either contract differ, that contract wins and the difference is a defect of this one.

---

## 0. Preserved truth (binding)

- `ACTIVE CONTRACT: NONE` describes the state before and after this increment; this contract fills no active-contract slot
  after delivery and is not a delivery record.
- No Stage is entered, completed or reopened (27 of 45 complete). No domain, part, pack, D4 gate, PLC or Mechatronics
  capability is activated. The shared deterministic calculation owner is unchanged (five methods, five bindings): this
  composition reaches it only through the unchanged TMP36 consumer and its existing binding.
- The TMP36 equation, declarations, screen, interval, numerical acceptance, refusals and display, and the 28-T4 fixed
  definition, confirmations, screen, cycle, output map and refusals, are unchanged. The standalone TMP36 and 28-T4 pages,
  routes, input contracts, outputs and authority are unchanged.

## 1. Purpose, scope and eligibility

ONE optional, advisory, non-safety, request-local composition: an inventor who has declared a TMP36 output voltage and a
Celsius threshold sees, in one step, the nominal temperature, whether it is at or above the threshold, and what one
READY / RUNNING control cycle does when that condition is its `start_input`.

Eligibility is the INTERSECTION of the two existing gates: the TMP36 gate (`_calc_gate` with the TMP36 consumer) AND the
28-T4 gate (the trusted durable root domain exactly `electronics_electrical`). Because the 28-T4 gate admits the root only,
the composition is offered on an Electrical / Electronics-root project only; no Mechanical-root and no declared-part
eligibility is added, and a declared Stage 15 part grants nothing here. Anything unreadable grants nothing (fail closed).

**Amended by CONTROL-CYCLE-INTEGRATED-PART-01 (Owner-authorized; effective only on the verified merge of its pull
request; the preceding paragraph is preserved as the superseded wording).** The rule is still the INTERSECTION of the two
existing gates, each now the shared root-or-declared-part rule (`_calc_gate` with the TMP36 consumer, and with the 28-T4
module). On an Electrical / Electronics ROOT project the root alone admits the composition, independent of any
composition, exactly as before. Where the root does not admit it, both gates must have resolved — on the request being
served, from the store-validated durable composition, never from the request — to the SAME current validated Electrical /
Electronics part: the same durable `subsystem_id` and domain. Two separate `True` results never establish that: TMP36
eligibility alone, 28-T4 eligibility alone, a part on one side only, two different parts, or a withdrawn, replaced, stale,
malformed, corrupt or unreadable composition grants nothing. No second composition-selection engine exists: the one web
gate (`_tcc_gate`) compares the two results and is read by the session link, the GET and the POST alike. The page names
that part (escaped, direction-isolated) with a fixed attribution note; a declared part establishes no sensor choice,
control requirement, actuation, timing, compatibility, suitability, validation or safety. The TMP36 evaluation, the
threshold grammar and range, the exact comparison, the derived Boolean, the control-cycle evaluation, the refusal layering
and the no-partial-success rule are unchanged.

## 2. Identity

Identity `temperature_control_condition:tmp36_threshold_ready_running`, version `1.0`. Module
`engine/temperature_control_condition.py` — a thin composition wrapper: it owns capture of the combined form, the threshold
grammar and range, the one comparison, its own confirmation and the stage order, and nothing else. It holds no equation,
state table, output map or refusal rule of either part.

## 3. Fixed composition, in one request

1. The EXISTING TMP36 consumer evaluates the inventor-declared output voltage with all its own declarations, screen,
   nominal-model interval, binary and decimal-reference acceptance and refusals (TMP36 contract §§5–8).
2. The inventor-declared threshold is read as an EXACT decimal.
3. The ONE fixed condition `nominal_temperature_C >= threshold_C` is evaluated on EXACT decimal values: the accepted exact
   nominal temperature the TMP36 consumer returns with its success (the same value it shows, never a binary float and never
   parsed from display text) and the exact threshold.
4. Only the resulting Boolean is passed as `start_input` to the EXISTING 28-T4 evaluator, which runs its own confirmations,
   screen and five-step cycle unchanged (28-T4 contract §§3–8). `RUNNING` stays `RUNNING` whatever `start_input` is.

There is no generic comparator, no other operator, no second state engine, no orchestrator, no persistence and no result
carried between requests.

## 4. Threshold

Strict ASCII decimal: an optional single leading minus, digits and at most four fractional digits (the resolution of an
admitted nominal temperature; a representation rule only, implying no precision). Capped at 64 characters (non-physical).
The exact value must lie in −40 °C to +125 °C inclusive (the TMP36 nominal-model temperature range). Omitted is
`NOT_DECLARED`; malformed is `INVALID_THRESHOLD`; outside the range is `THRESHOLD_OUTSIDE_RANGE`. `-0` is zero.

## 5. Confirmation

One statement, answered «applies» or «does not apply», none pre-selected (missing: `NOT_DECLARED`; «does not apply»:
`MODEL_NOT_SUPPORTED`), in addition to every declaration and confirmation of the two parts:

| Ref | Id | Accepted statement |
|---|---|---|
| D-1 | `condition_meaning` | start_input is taken to be true exactly when the nominal temperature is at or above the threshold entered, and false otherwise; nothing else sets it, and the threshold is the inventor's own value |

## 6. Inputs and provenance

The voltage, the threshold, every declaration and confirmation, the screens and the previous state are the inventor's own
statements; the result echoes the declared voltage and threshold as entered and labels them as such. `start_input` is never
a client field: any submitted `start_input` is an unknown field and the request is refused (§7).

## 7. Outcomes and refusal semantics

Order after request integrity (CSRF), project authorization, eligibility (§1) and strict capture: (1) completeness of the
composition's own fields (confirmation and threshold) — `NOT_DECLARED`; (2) the confirmation — `MODEL_NOT_SUPPORTED`;
(3) threshold grammar — `INVALID_THRESHOLD`; (4) threshold range — `THRESHOLD_OUTSIDE_RANGE`; (5) the TMP36 consumer with
its own full order — any non-success is `TMP36_REFUSED` carrying the TMP36 outcome token unchanged; (6) the condition;
(7) the 28-T4 evaluator with its own full order — any non-success is `CONTROL_CYCLE_REFUSED` carrying the 28-T4 outcome
token unchanged. The first failing stage alone decides.

A refusal at any stage carries NO temperature, condition, `start_input`, state or output: there is no partial success.
Malformed requests — an unknown field (including `start_input`, an unprefixed part field or any attempt to supply a
transition, state, output or comparator), a field sent more than once, or a value outside a part's closed choices — are a
bare 400 with no evaluation.

## 8. Result

On success: the declared voltage (as entered), the nominal temperature (the TMP36 exact decimal display) in °C, the
declared threshold (as entered), the condition, the `start_input` passed, the previous state, the transition status, the
next state, the logical output, the TMP36, 28-T4 and composition identities and versions, `UNVALIDATED` / `NOT EVIDENCE`,
this contract's disclosure (§9) and both parts' own fixed disclosures.

## 9. Fixed disclosure

1. This joins two existing advisory evaluations in one request: the TMP36 nominal temperature for the voltage you declared, and one READY / RUNNING control cycle.
2. start_input is true exactly when the nominal temperature is at or above the threshold you entered, and false otherwise; the comparison uses the exact decimal values, and nothing else sets start_input.
3. The temperature is the TMP36 nominal relation applied to your declared voltage, not a measured or accurate temperature; a real sensor can differ by several degrees, so the condition can differ from what a real system would see.
4. If either evaluation refuses, nothing is shown from the other: there is no temperature-only, condition-only or cycle-only partial result.
5. Nothing is stored or carried to the next request, and the output is a logical value only: nothing is switched, started or energized, and this is not a thermostat, controller, safety function or interlock.
6. It is preliminary, advisory, UNVALIDATED and not evidence; the threshold is your own value, and InventorAI does not check that it suits your design.
7. Reference sources stay as for the two evaluations: the Analog Devices TMP35/TMP36/TMP37 data sheet, Rev. H, and OpenPLC Runtime (reference only); no manufacturer or runtime code is used.

## 9A. Arabic wording

**A-1 Fixed disclosure (Arabic rendering of the seven §9 items, item by item; no meaning added, removed or softened).**

> 1. يجمع هذا الحساب تقييمين إرشاديين قائمين في طلب واحد: درجة الحرارة الاسمية لحسّاس TMP36 للجهد الذي صرّحت به، ودورة تحكم واحدة READY / RUNNING.
> 2. تكون start_input صحيحة (true) فقط عندما تكون درجة الحرارة الاسمية مساوية للعتبة التي أدخلتها أو أعلى منها، وخاطئة (false) في غير ذلك؛ وتُجرى المقارنة على القيم العشرية الدقيقة، ولا يحدد start_input أي شيء آخر.
> 3. درجة الحرارة هي العلاقة الاسمية لحسّاس TMP36 مطبّقة على الجهد الذي صرّحت به، وليست درجة حرارة مَقيسة أو دقيقة؛ وقد يختلف حسّاس حقيقي بعدة درجات، لذلك قد يختلف الشرط عمّا قد يراه نظام حقيقي.
> 4. إذا رفض أيٌّ من التقييمين، فلا يُعرض شيء من الآخر: لا توجد نتيجة جزئية لدرجة الحرارة وحدها أو للشرط وحده أو للدورة وحدها.
> 5. لا يُحفَظ شيء ولا يُنقل إلى الطلب التالي، والخرج قيمة منطقية فقط: لا يُشغَّل أي شيء ولا يُبدأ ولا يُمَدّ بالطاقة، وهذا ليس منظِّم حرارة (thermostat) ولا جهاز تحكم ولا وظيفة سلامة ولا تعشيقًا (interlock).
> 6. هذه النتيجة أولية وإرشادية، وغير مُتحقَّق منها (UNVALIDATED)، وليست دليلًا؛ والعتبة قيمتك أنت، ولا يتحقق InventorAI من ملاءمتها لتصميمك.
> 7. تبقى المراجع كما هي للتقييمين: ورقة بيانات Analog Devices لـ TMP35/TMP36/TMP37، المراجعة Rev. H، وOpenPLC Runtime (مرجعًا فقط)؛ ولا يُستخدم أي كود من الشركة المصنّعة أو من بيئة التشغيل.

**A-2 Confirmation (§5).** The inventor answers «ينطبق على حالتي» or «لا ينطبق على حالتي», none pre-selected.

| §5 | Arabic statement |
|---|---|
| D-1 condition_meaning | تُعدّ start_input صحيحة (true) فقط عندما تكون درجة الحرارة الاسمية مساوية للعتبة المُدخلة أو أعلى منها، وخاطئة (false) في غير ذلك؛ ولا يحددها شيء آخر، والعتبة قيمتك أنت. |

**A-3 Right-to-left rendering.** Numbers, `mV`, `°C`, `TMP36`, `start_input`, `READY` / `RUNNING`, `true` / `false`, the
identities and `UNVALIDATED` / `NOT EVIDENCE` are direction-isolated on the Arabic page; typed values are shown
left-to-right.

## 10. Exclusions (binding)

No control command, physical actuation, thermostat or controller behaviour, compatibility inference, verified measurement,
accuracy claim, safety function, interlock or real-time execution; no other operator, comparator, threshold set,
hysteresis, timer or sequence; no change to either part's semantics; no persistence, result transfer between requests,
report, PDF, Structured Export, API, evidence, readiness, progression, gap or SafetySignal effect; no D4, PLC, Mechatronics,
domain, part or Stage 15 activation; no AI or provider call; no external dependency.

## 11. Source and IP status

No new source. The TMP36 nominal relation keeps its Analog Devices TMP35/TMP36/TMP37 Rev. H source and source-use records
(`ADI-S1`, `tmp36:SU001`) and their conditions; the control cycle keeps its OpenPLC Runtime reference-only record
(`OPENPLC-S1`, `oplc:SU001`, commit `8d69d935a7915bef9b67bbea46cf87c68d112246`) and its limitations. The threshold
comparison and the composition order are InventorAI's own design. No manufacturer or runtime code, protected source or new
library is used.

## 12. Implementation boundary

Routes: `GET` / `POST /session/<sid>/temperature-control-condition`, behind the central project authorization and the
global CSRF guard; one optional session-page link on an eligible project. The TMP36 consumer exposes, on success only, the
exact decimal nominal temperature it accepted (`nominal_temperature`, a behaviour-preserving addition to its outcome); the
standalone TMP36 page does not read it. Nothing is persisted; the POST renders its result directly.

## 13. Verification

Focused tests (`tests/test_temperature_control_condition.py`, `tests/test_temperature_control_condition_browser.py`):
below, equal and above the threshold against an independent exact-decimal oracle; thresholds −40 and +125; nominal
temperatures −40, 0 and +125; decimal-adjacent comparisons at equality where binary arithmetic would differ; READY and
RUNNING with true and false (`RUNNING` with false stays `RUNNING`); missing, malformed, out-of-range and contradictory
inputs and declarations; every TMP36 refusal path and every 28-T4 refusal path with no partial result; authorization,
eligibility, CSRF, request isolation and no persistence; EN / AR; and regression of the standalone TMP36 and 28-T4
evaluations. Since CONTROL-CYCLE-INTEGRATED-PART-01, `tests/test_control_cycle_integrated_part.py` and its browser
companion prove the same-part identity rule (two separate `True` results insufficient; a part on one side only or two
different parts refused), the unchanged root behaviour, GET / POST re-validation and the fail-closed replaced / corrupt /
unreadable composition. Hosted required CI is the merge gate.

## 14. STOP conditions

Stop and return to the Owner if reuse would require reproducing the TMP36 equation or the 28-T4 state engine, changing
either part's semantics, widening activation or eligibility, or weakening refusal, provenance, authorization or numerical
integrity.
