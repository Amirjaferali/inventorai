# STAGE 28 / 28-T4 — SINGLE VENDOR-NEUTRAL CONTROL-CYCLE EVALUATION — SLICE 1 CONTRACT

STATUS: OWNER-AUTHORIZED BOUNDED CONTRACT — written with, and governing, the one bounded implementation increment
`28-T4 CONTROL-CYCLE-SLICE-01`, which the Owner authorized as ONE bounded implementation and ONE pull request.
Applicability: this contract governs the delivered evaluation only on the verified merge of that pull request into
`feature/atomic-json-session-persistence`; on its proposal branch it describes an Owner-authorized proposed capability, not
a merged or delivered one. Merge, deployment, PLC activation, industrial runtime integration, any method admission to the
shared deterministic calculation owner and any safety-function authorization are NOT authorized by it.
AUTHORITY LEVEL: an Owner-authorized bounded slice under the Stage 28 subitem 28-T4 (PLC / Industrial Automation & Control)
of the Master Execution Roadmap, which stays `RECORDED — PLANNING / NAVIGATION ONLY` for everything outside this slice. It
amends no other contract and changes no existing calculation, `control_loop` or Stage 15 behaviour.

---

## 0. Preserved truth (binding)

- `ACTIVE CONTRACT: NONE` describes the state before and after this increment; this contract fills no active-contract slot
  after delivery and is not a delivery record. Current-truth delivery records belong to a later closure sync.
- No Stage is entered, completed or reopened; the roadmap count is unchanged (27 of 45 complete). 28-T4 is NOT a qualified
  technical owner and is NOT activated: this slice adds no Domain Pack, part, pack question, root or part-only activation,
  so the Stage 30 new-domain-activation trigger recorded for 28-T4 does not fire. Any broader 28-T4 capability — custom state
  programs, sequences, timers, interlocks, I/O engineering, ladder or function-block logic, HMI / SCADA, vendor layers or
  safety PLCs — stays NOT AUTHORIZED and keeps its recorded preconditions.
- `control_loop` stays exactly as it is (PART-ONLY, one optional part, NOT root-activated); this slice neither reads nor
  writes it, grants it nothing and is not the "control-loop owner".
- The four admitted calculations (CAP-13 reactions, THERM-01, CAP-13 planar moment, CAP-13 rotational load) and the TMP36
  nominal temperature are unchanged; this evaluation is NOT a method of the shared deterministic calculation owner.

## 1. Purpose and scope

ONE optional, advisory, non-binding, request-local evaluation of ONE fixed, fully declared, non-safety control-state
transition. It lets an inventor who is thinking through simple start logic see, step by step, what one control cycle does
with one input: which state follows and what the one logical output is — and see that "nothing happened" is a normal result.

Eligibility: a project whose trusted durable root domain is exactly `electronics_electrical`, read as the other
request-local calculations read it (`_cap12_root_domain` in `web/app.py`) and never from the request. A declared Stage 15
part grants NOTHING here: no integrated-part exception is added, so an integrated project is eligible only through its
Electrical / Electronics root focus. A missing or unreadable root domain grants nothing (fail closed). The session link,
the page and the submission read the same one decision.

**Amended by CONTROL-CYCLE-INTEGRATED-PART-01 (Owner-authorized; effective only on the verified merge of its pull
request; the preceding paragraph is preserved as the superseded wording).** Eligibility is the ONE shared rule the admitted
calculations use (`_calc_gate` in `web/app.py`, applied to this module's `ELIGIBLE_ROOT_DOMAIN` / `is_eligible`): the
trusted durable root domain exactly `electronics_electrical` — unchanged, and never dependent on any composition — OR the
ONE inventor-declared Electrical / Electronics part of a valid durable Stage 15 integrated composition, whatever the
initial analysis focus. The part is read only from the store-validated durable composition on the request being served
(session link, GET and POST alike), never from the request; a missing, replaced, stale, malformed, corrupt or unreadable
composition grants nothing beyond the root rule; no request-supplied part id or domain can establish eligibility. On an
integrated project the page names the declared part (escaped, direction-isolated) with a fixed attribution note. A
declared part establishes no control requirement, actuation, PLC runtime semantics, timing, compatibility, suitability,
validation or safety; the fixed definition, confirmations, screen, cycle, output map, outcomes, refusals, artifact, source
basis, disclosure and request-local / no-persistence behaviour are unchanged. The narrow Stage 15 exception is recorded in
`engine/subsystem_model.py`; `control_loop` is still neither read nor touched, and no D4, PLC, Mechatronics or domain
activation follows.

## 2. Identity and version

Identity `control_cycle:ready_running_single_transition`, version `1.0` (the semantic version of the fixed definition).
Governed artifact `docs/governance/control_cycle_content_config/ready_running_single_transition_v1.json`
(`control_cycle_ready_running_single_transition`, artifact version `1`). Module `engine/control_cycle.py` (ONE bounded
module: artifact validation, capture, the pre-evaluation order and the evaluation). No registry, framework, scheduler or
rule engine.

## 3. Fixed definition and cycle order

Closed vocabulary: two states, `READY` and `RUNNING`; one Boolean input, `start_input`; one Boolean output, `output`.

- **One transition:** source `READY`, condition `start_input == true`, target `RUNNING`.
- **Output map:** `READY → false`, `RUNNING → true`.

One cycle, in this order:

1. freeze the one Boolean input `start_input` (read once, held for the cycle);
2. read the one previous state;
3. evaluate the one transition against the previous state and the frozen input;
4. select the next state: the target when the previous state is the source AND the condition holds, otherwise the previous
   state;
5. calculate the one Boolean output as `output_map[next_state]`.

Reference cases (binding):

| Previous | Input | Transition | Next | Output |
|---|---|---|---|---|
| READY | true | APPLIED | RUNNING | true |
| READY | false | NOT_APPLIED_CONDITION_FALSE | READY | false |
| RUNNING | true | NOT_APPLICABLE_FROM_STATE | RUNNING | true |
| RUNNING | false | NOT_APPLICABLE_FROM_STATE | RUNNING | true |

For `RUNNING` the transition is not applicable (its source is `READY`): the state is kept and no transition fires. A false
condition is a valid no-transition result, not a refusal. **The output is read from the NEXT state, never the previous
state — InventorAI's own design decision for this evaluation, NOT a claimed OpenPLC, PLC or IEC 61131-3 execution
semantic.** No state is persisted or advanced between requests.

## 4. Result

On success: the previous state, the frozen input, the transition status (`APPLIED`, `NOT_APPLIED_CONDITION_FALSE` or
`NOT_APPLICABLE_FROM_STATE`) and whether it was applied, the next state, the Boolean output, the identity and semantic
version, the confirmed assumptions (echoed), `UNVALIDATED` / `NOT EVIDENCE` and the fixed disclosure (§9).

## 5. Confirmations (the inventor declares the definition applies)

Each is shown as its own statement and answered «applies» or «does not apply», none pre-selected. A missing answer is
`NOT_DECLARED`; «does not apply» is `MODEL_NOT_SUPPORTED`. InventorAI infers none of them, and infers no component, current
state, electrical signal or process condition.

| Ref | Id | Accepted statement |
|---|---|---|
| D-1 | `two_states` | the logic considered has exactly two states, READY and RUNNING, and the previous state entered is the one it was in before this cycle |
| D-2 | `one_transition` | its only transition goes from READY to RUNNING when start_input is true; there is no way back to READY and no other transition, timer, counter or fault state |
| D-3 | `output_meaning` | the one Boolean output is false in READY and true in RUNNING, and it is read from the state after this cycle |
| D-4 | `one_frozen_input` | start_input is the only input, its value is read once and held unchanged for the whole cycle, and nothing else (power-up, reset, other signals or the passage of time) is considered |
| D-5 | `logical_only` | the states, the input and the output are logical values only; whether any real device, signal or piece of equipment is switched, started, stopped or energized is not decided here |

## 6. Inputs

The previous state is chosen from `READY` / `RUNNING` and the input from `true` / `false`, none pre-selected. They are the
inventor's own statements of one hypothetical cycle, not readings of any system.

## 6A. Named consumer with a derived input (TEMPERATURE-TO-CONTROL-CONDITION-01) — narrow exception

Owner-authorized with that increment, and effective only on the verified merge of its pull request: within ONE named
request-local consumer, the
[temperature-to-control-condition composition](TEMPERATURE_TO_CONTROL_CONDITION_COMPOSITION_CONTRACT.md)
(`engine/temperature_control_condition.py`), `start_input` is not chosen directly by the inventor but derived in the same
request from one fixed comparison of two inventor-declared values (the TMP36 nominal temperature of a declared voltage and
a declared threshold); the client can never submit it there. The previous state stays the inventor's own choice. The
derived Boolean is not a reading or inference of any real signal, component or process condition. This exception names
that consumer only; the fixed definition, the confirmations, the screen, the five-step cycle, the output map, the refusals
and the §1 eligibility rule (root-only at delivery; as amended by CONTROL-CYCLE-INTEGRATED-PART-01, the same shared
root-or-declared-part rule, which the consumer must satisfy for the SAME current part on both of its sides) are unchanged
by this exception, and a refusal here gives that consumer no state or output.

## 7. Outcomes and refusal semantics

Order after request integrity (CSRF), project authorization, eligibility and strict capture: (0) governed definition —
invalid, ambiguous or tampered is `DEFINITION_UNAVAILABLE`; (1) completeness — every confirmation, screen item, the previous
state and the input answered, else `NOT_DECLARED`; (2) screen — any YES is `ENGINEERING_REVIEW_REQUIRED`; (3) confirmations
— any «does not apply» is `MODEL_NOT_SUPPORTED`; (4) the cycle (§3) — `SUCCESS` with one of the three transition statuses.
The first failing stage alone decides; no state or output accompanies a refusal.

**Malformed or contradictory requests** are refused as a bare 400 with no evaluation: an unknown field — including any
attempt to supply a state, a transition, a condition, a target, an output value or an output map — a field sent more than
once, a previous state outside the closed vocabulary or an input other than `true` / `false`. The definition is fixed by
the application, so an attempted override is refused, never evaluated as if it were a rule. At the module level an unknown
previous state is `UNKNOWN_STATE` and an input that is not exactly a Boolean is `INVALID_INPUT_SNAPSHOT`.

**Definition integrity.** The governed definition is refused (`DEFINITION_UNAVAILABLE`) when a key appears twice in any
object (for example two output-map entries for one state), a key is unknown or missing, the state vocabulary differs or
repeats, there is not exactly one transition, its source or target is unknown or equal, its condition does not read
`start_input` against a Boolean, the output map lacks or adds a state or holds a non-Boolean, the definition differs from
the definition pinned in the module, or any governed section differs from its pinned digest.

Routine no-transition results (`NOT_APPLIED_CONDITION_FALSE`, `NOT_APPLICABLE_FROM_STATE`) are successes and are shown as
such; they are never mixed with refusals.

## 8. High-risk screen (declared; not a safety engine)

Six items, answered yes or no, none pre-selected — whether the logic is for, or the output would affect: a safety function,
interlock, emergency stop or protective shut-off; moving machinery or parts that could injure someone; mains or high
voltage; heating, fire or ignition risk; medical or life-supporting use; vehicle or aerospace use. Any YES is
`ENGINEERING_REVIEW_REQUIRED` and nothing is evaluated. All NO answers only allow this bounded evaluation to proceed and
never mean safe. The screen neither reads nor feeds SafetySignal.

## 9. Fixed disclosure

English (pinned equal to the artifact):

1. This is one evaluation of the fixed READY / RUNNING logic you confirmed, for the previous state and the start_input value you entered: start_input is read once and held, the one transition is checked, the next state is chosen and the output is read from the next state.
2. If the transition does not apply, the state stays as it was; that is a normal result, not an error.
3. The output is a logical value (true or false) only. It does not mean that any real device is switched, started, stopped or energized, and nothing is sent to any device.
4. Nothing is stored between evaluations: each one starts from the previous state you enter, and InventorAI does not track the state of your system.
5. Reading the output from the next state is InventorAI's own design choice for this evaluation. It is not a claim about how any PLC, OpenPLC or IEC 61131-3 runtime executes a program, and no timing, scan time or electrical behaviour is implied.
6. It is not a safety function, interlock or emergency stop. It is preliminary, advisory, UNVALIDATED and not evidence, and any real control logic must be designed and checked by a qualified engineer.
7. Reference: OpenPLC Runtime (Autonomy, MIT License), source commit 8d69d935, used only as a factual reference for separating input reading, program logic and output update in a control cycle; no OpenPLC code or text is used, and no endorsement is implied.

## 9A. Arabic wording

**A-1 Fixed disclosure (Arabic rendering of the seven §9 items, item by item; no meaning added, removed or softened).**

> 1. هذا تقييم واحد لمنطق READY / RUNNING الثابت الذي أكّدته، للحالة السابقة ولقيمة start_input اللتين أدخلتهما: تُقرأ start_input مرة واحدة وتُثبَّت، ويُفحص الانتقال الوحيد، وتُختار الحالة التالية، ويُقرأ الخرج من الحالة التالية.
> 2. إذا لم ينطبق الانتقال، تبقى الحالة كما كانت؛ وهذه نتيجة عادية، وليست خطأ.
> 3. الخرج قيمة منطقية فقط (true أو false). ولا يعني أن أي جهاز حقيقي قد شُغِّل أو بدأ أو توقف أو أُمِدَّ بالطاقة، ولا يُرسَل أي شيء إلى أي جهاز.
> 4. لا يُحفَظ شيء بين التقييمات: يبدأ كل تقييم من الحالة السابقة التي تدخلها، ولا يتتبّع InventorAI حالة نظامك.
> 5. قراءة الخرج من الحالة التالية خيار تصميمي خاص بـ InventorAI في هذا التقييم. وليست ادعاءً بشأن كيفية تنفيذ أي PLC أو OpenPLC أو بيئة تشغيل IEC 61131-3 لبرنامج، ولا يُقصد بها أي توقيت أو زمن مسح (scan time) أو سلوك كهربائي.
> 6. هذا ليس وظيفة سلامة ولا تعشيقًا (interlock) ولا إيقافًا طارئًا. وهو أولي وإرشادي، وغير مُتحقَّق منه (UNVALIDATED)، وليس دليلًا، ويجب أن يصمّم مهندس مؤهل أي منطق تحكم حقيقي ويتحقق منه.
> 7. المرجع: OpenPLC Runtime (Autonomy، رخصة MIT)، الإيداع 8d69d935، ويُستخدم مرجعًا واقعيًا فقط للفصل بين قراءة المدخلات ومنطق البرنامج وتحديث المخرجات في دورة التحكم؛ ولا يُستخدم أي كود أو نص من OpenPLC، ولا يُقصد أي تأييد.

**A-2 Confirmations (§5).** The inventor answers «ينطبق على حالتي» or «لا ينطبق على حالتي», none pre-selected.

| §5 | Arabic statement |
|---|---|
| D-1 two_states | المنطق المعني له حالتان فقط، READY وRUNNING، والحالة السابقة المُدخلة هي الحالة التي كان فيها قبل هذه الدورة. |
| D-2 one_transition | انتقاله الوحيد من READY إلى RUNNING عندما تكون start_input صحيحة (true)؛ ولا رجوع إلى READY، ولا انتقال آخر، ولا مؤقّت أو عدّاد أو حالة عطل. |
| D-3 output_meaning | الخرج المنطقي الوحيد false في READY وtrue في RUNNING، ويُقرأ من الحالة بعد هذه الدورة. |
| D-4 one_frozen_input | start_input هي المدخل الوحيد، وتُقرأ قيمتها مرة واحدة وتبقى ثابتة طوال الدورة، ولا يُؤخذ في الحسبان أي شيء آخر (بدء التشغيل أو إعادة الضبط أو إشارات أخرى أو مرور الزمن). |
| D-5 logical_only | الحالات والمدخل والخرج قيم منطقية فقط؛ ولا يُحسم هنا ما إذا كان أي جهاز أو إشارة أو معدّة حقيقية تُشغَّل أو تبدأ أو تتوقف أو تُمَدّ بالطاقة. |

**A-3 Screen (§8).**

| §8 | Arabic item |
|---|---|
| safety_function | وظيفة سلامة، أو تعشيق (interlock)، أو إيقاف طارئ، أو فصل وقائي |
| machinery_motion | آلات أو أجزاء متحركة قد تؤذي أحدًا |
| mains_or_high_voltage | جهد الشبكة الكهربائية (mains) أو جهد عالٍ |
| heating_or_fire | تسخين أو خطر حريق أو اشتعال |
| medical_or_life_supporting | استخدام طبي أو داعم للحياة |
| vehicle_or_aerospace | استخدام في المركبات أو في الطيران والفضاء (aerospace) |

**A-4 Right-to-left rendering.** The state names `READY` / `RUNNING`, `start_input`, `output`, the Boolean values `true` /
`false`, the identity, `OpenPLC`, `PLC`, `IEC 61131-3` and `UNVALIDATED` / `NOT EVIDENCE` are each direction-isolated on the
Arabic page.

## 10. Exclusions (binding)

No custom or client-supplied states, transitions, conditions, expressions, callbacks, tables or output maps; no generic
state-machine framework, scheduler, rule engine or second control owner; no PLC, IEC 61131-3, ladder, function-block or
scan-cycle execution, timing, scan time or determinism guarantee; no I/O, electrical, wiring, controller or vendor
statement; no safety function, SIL / PL, interlock or emergency stop; no device command; no inference of components, current
state, signals or process conditions; no `control_loop`, Stage 15 part, domain or 28-T4 owner activation; no persistence,
state carried between requests, report, PDF, Structured Export, API, evidence, readiness, progression, gap or SafetySignal
effect; no AI or provider call; no external dependency.

## 11. Source and IP status

- **OPENPLC-S1** — OpenPLC Runtime, examined source commit `8d69d935a7915bef9b67bbea46cf87c68d112246`, repository
  <https://github.com/Autonomy-Logic/openplc-runtime/tree/8d69d935a7915bef9b67bbea46cf87c68d112246> (Lead-supplied and Lead-verified). Used ONLY as a factual reference for the documented runtime separation
  of a repeated control cycle into reading the inputs, executing the program logic and updating the outputs (cycle
  boundaries). It is NOT cited for, and does not support, the READY / RUNNING definition, the single transition, the
  frozen-input rule or reading the output from the next state, which are InventorAI's own design semantics.
- **Licence and use** (not a legal opinion): the examined OpenPLC core files are MIT-licensed under the repository's
  applicable file-level notices, Copyright (c) 2026 Autonomy, as supplied by the Lead (`oplc:SU001`). No OpenPLC, Beremiz or
  IEC source code, text, diagram or table is copied, redistributed or executed, so no notice-retention obligation is
  triggered; attribution is given as acknowledgement. No endorsement by Autonomy, the OpenPLC project or any contributor is
  stated or implied. No conformity with IEC 61131-3, PLC scan equivalence, timing, electrical compatibility or industrial
  safety is claimed.
- **Inspection basis.** Lead-supplied identification of the project, the examined commit and the licence in the authorizing
  brief, and the repository URL independently verified by the Lead in the PR #864 source-provenance correction; not
  re-inspected by the executor, because the Owner instructed that PLC source research not be restarted.

## 12. Implementation boundary

Routes: `GET` / `POST /session/<sid>/control-cycle`, behind the central project authorization and the global CSRF guard; the
session page shows one optional link on an eligible project. The evaluation runs inside the request and renders its result
directly; nothing is persisted and no state is kept between requests.

## 13. Verification

Focused tests (`tests/test_control_cycle.py`, `tests/test_control_cycle_browser.py`): the four reference cases at module,
consumer and page level; next-state versus previous-state output; request isolation; malformed, duplicate, unknown and
override fields; unknown state and non-Boolean input; duplicate-key, conflicting, incomplete and unsupported definitions and
artifact tampering; eligibility (Electronics root; a Mechanical root without a declared Electrical / Electronics part
grants nothing; since CONTROL-CYCLE-INTEGRATED-PART-01, `tests/test_control_cycle_integrated_part.py` and its browser
companion prove the declared-part path, the unchanged root behaviour, GET / POST re-validation and the fail-closed
replaced / corrupt / unreadable composition); CSRF,
authorization and no persistence; the existing calculations, `control_loop` and Stage 15 unchanged; EN / AR fidelity and
real-browser EN / AR journeys. Hosted required CI is the merge gate.

## 14. STOP conditions

Stop and return to the Owner if the intended value requires arbitrary custom state programs, a new execution engine, a
safety interlock, PLC runtime semantics, a declared-part or domain activation, or any other expansion of existing authority.
