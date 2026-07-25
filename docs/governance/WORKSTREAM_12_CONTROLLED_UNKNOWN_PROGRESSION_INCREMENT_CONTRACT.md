# Workstream 12 — Controlled Unknown Progression — Increment Contract (Fresh)

> Documentation-only governance draft. This document defines a proposed
> increment-contract boundary for a **future** Workstream 12. It authorizes no
> implementation. It is drafted fresh from the current authoritative repository
> tip; it does not inherit, preserve, or presume the findings or decision IDs of
> the earlier superseded WS12 artifact.

---

## 1. Authority and non-activation statement

- This is a **governance document only**. Creating or merging it does **not**
  start Workstream 12 and does **not** authorize any BASE RED, GREEN, code,
  test, schema, persistence, UI, prompt/AI, database, question-content,
  scoring, or progression-state change.
- Workstream 12 remains **NOT STARTED**.
- This document is subordinate to the committed governance anchors, the
  `MVP_SCOPE_FREEZE.md`, `GOVERNANCE_MODEL.md`, `CLAUDE.md`, the
  `DELIVERABLE_STABILIZATION_REMEDIATION_PLAN.md` §15 status table, and the
  `INVENTORAI_CAPABILITY_ENRICHMENT_REGISTER.md`. Where any conflict arises,
  those committed authorities and the latest `ACTIVE_EXECUTION_ROADMAP.md`
  control.
- No capability in the Capability Enrichment Register is activated by this
  document. **CAP-04, CAP-08, CAP-10, CAP-12, CAP-13, and CAP-14 remain
  `RECORDED — NOT AUTHORIZED FOR IMPLEMENTATION`.** D13 (CAP-01 / Structured
  Technical Guidance), Patent Export, and WS-PFV-001 remain **separately gated
  and inactive**.
- Nothing here re-derives, reopens, or supersedes any owner-closed workstream.

---

## 2. Evidence lock

| Item | Value |
|---|---|
| Repository | `Amirjaferali/inventorai` |
| Authoritative branch | `feature/atomic-json-session-persistence` |
| Authoritative tip (this analysis) | `b4e38c0fae6be4c9a95e9bb92bdb75bf8e9ba656` |
| Tip subject | `Merge pull request #267 from Amirjaferali/docs/capability-register-cap12-cap13-cap14-amendment` |
| Tip parents | `d524bf29bf7914e796a822d0fe4dd3319ffea101` (base) · `cb2ceb78fb3ee7423e68a4f378f7e14859c908bf` (CAP-12/13/14 amendment) |
| Tip tree | `e7882e4c8d736cd8267960e83ab57351e8458dc5` |
| Capability register | `docs/governance/INVENTORAI_CAPABILITY_ENRICHMENT_REGISTER.md` — CAP-01 … CAP-14 present |
| WS9 / WS10 / WS11 | FORMALLY CLOSED (remediation plan §15) |
| WS12 | NOT STARTED |
| WS13 / WS14 / WS15 / WS16 | NOT STARTED |
| WS17 (AI Coach) | NOT STARTED — BLOCKED until WS1–WS16 owner-closed |

**Superseded prior artifact (non-authoritative research input only):**

| Item | Value |
|---|---|
| Branch | `docs/workstream-12-increment-contract` |
| Commit | `12dbad13b699ed5fea5b9eaa70fe00139dfd4fa7` |
| Parent | `2775242c415cd9f26947a454938900a1b5b303ec` |
| Bundle | `ws12-increment-contract.bundle` (reported SHA-256 `e56ce3115809ddc9aa1a57d96d94e4ad9d6805b8a72542b58aae4f1ce9d366e1`) |
| Classification | **SUPERSEDED / PREMATURE — DO NOT USE** |

That artifact was authored from a stale parent (`2775242…`), predating PR #266
and PR #267 (CAP-01…CAP-14). Its D-A through D-P analysis is **not** carried
forward. Every finding in this document is re-derived from the current
authoritative tip.

---

## 3. Source-review inventory

Read directly from the authoritative tip `b4e38c0`:

**Governance / anchors**
- `CLAUDE.md`, `docs/governance/DELIVERABLE_STABILIZATION_REMEDIATION_PLAN.md`
  (§15 status table), `docs/governance/INVENTORAI_CAPABILITY_ENRICHMENT_REGISTER.md`
  (CAP-01…CAP-14), `docs/governance/ACTIVE_EXECUTION_ROADMAP.md`.
- Referenced authorities: `MVP_SCOPE_FREEZE.md`, `GOVERNANCE_MODEL.md`,
  D13 records, `PROTOTYPE_FEASIBILITY_AND_VALIDATION_FUTURE_WORKSTREAM_OWNER_DECISION.md`
  (WS-PFV-001), `STRUCTURED_INVENTION_DISCLOSURE_AND_PATENT_EXPORT_OWNER_DECISION.md`.

**Engine source (unknown-handling seams)**
- `engine/idea_state.py` (469 lines) — dispositions, ledger, unknowns, gap status.
- `engine/progression_loop.py` (1005 lines) — `integrate_response`,
  `evaluate_transition`, acknowledged-unknown parallel track.
- `engine/decision_workspace.py` (1136 lines) — candidate/decision blocker model.
- `engine/deliverable_assembler.py` (1400 lines) — unknown registry and
  disposition-anchored labels in the final deliverable.
- `engine/question_intent_registry.py` (425 lines, WS10) — read-only registry.
- `engine/question_aware_evaluation.py` (147 lines, WS11) — observation-only
  structural evaluation.
- `engine/path_n_questions.py` (109 lines, WS11) — atomic `ServedQuestion`.
- `engine/scoring.py` — scoring surface (protected; unchanged).

**Tests (protected boundaries)**
- `tests/test_workstream_9_single_intent_question_design.py:301`
  `test_PROTECTED_no_workstream_13_to_14_capability_introduced` — asserts
  `engine.guided_answer_support` (WS13) and `engine.adaptive_follow_up` (WS14)
  remain absent.

---

## 4. Current deterministic behavior (re-derived)

1. **Maturity transitions are deterministic and AI-free.**
   `evaluate_transition(state)` (`engine/progression_loop.py:764`) advances
   `maturity_level` 0→1→2 purely from `known_problem` / `known_mechanism`
   evidence quality and the CLOSED status of the three required Stage-2 gaps
   (`MECHANISM_COMPLETENESS`, `PHYSICAL_FEASIBILITY`, `BOUNDARY_AMBIGUITY`).
   No unknown record participates in this computation.

2. **Response integration is quality-tiered.**
   `integrate_response(...)` (`:690`) assigns an evidence quality tier
   (`ASSERTED` / `REASONED` / `DEMONSTRATED`) and maps it to `Gap.status`
   (`OPEN` / `PARTIAL` / `CLOSED`), returning `PASS` / `WARN` (there is no
   `BLOCK` emitted from unknowns).

3. **Scope.** MVP is electronics/electrical, LEVEL 0–2, Stage 2 (three gap
   types). `MVP_SCOPE_FREEZE.md` remains an active freeze.

---

## 5. Current unknown-handling seams (re-derived)

1. **Acknowledged-unknown parallel track.** `AcknowledgedUnknown`
   (`idea_state.py:242`) records `iteration`, `gap_context`, `verbatim`,
   `category_basis`. Populated by `_detect_acknowledged_unknown` and appended
   at `progression_loop.py:728`. It **has no effect on `gap.status`, quality,
   transition, or any return value** (explicit comment at `:725`). Surfaced in
   the deliverable as the `unknown_registry` (`UNK-00N`,
   `deliverable_assembler.py:704`).

2. **Append-only interaction/assertion ledger.** `AssertionRecord`
   (`idea_state.py:171`) recorded via `record_interaction(action, …)` (`:313`)
   for exactly the **six** `INTERACTION_DISPOSITIONS` (`:111`): `answered`,
   `unknown`, `deferred`, `provisional_assumption`, `specialist_requested`,
   `evidence_requested`. **`resolves_gap` is hard-wired `False`** (`:191`,
   `:341`) — a disposition never resolves a gap. The two request dispositions
   carry a durable `pending` value (`"specialist"` / `"evidence"`,
   `_PENDING_BY_DISPOSITION`). The ledger has **no effect on maturity,
   lifecycle, gaps, transitions, or the transcript**.

3. **Non-destructive contradiction / supersession graph.**
   `mark_contradiction`, `mark_supersession`, `has_unresolved_contradiction`
   (`idea_state.py:359–469`) maintain an append-only, acyclic, retained-history
   graph over ledger records. Provenance is preserved; nothing is deleted.

4. **Provenance / validation axes (Increment-2).** `Evidence` and
   `AssertionRecord` carry orthogonal `provenance`
   (`LEGACY_UNSPECIFIED / OWNER_STATED / SYSTEM_INFERRED / EXPERT_SUPPLIED /
   EXTERNAL_EVIDENCE`) and `validation_status`
   (`UNVALIDATED / SPECIALIST_REVIEWED / EMPIRICALLY_DEMONSTRATED /
   INDEPENDENTLY_VERIFIED`). Never inferred from text; defaults are the
   truthful "unknown" values.

5. **Latent `ACCEPTED_RISK` closure-path seam.** `Gap.status` defines
   `ACCEPTED_RISK` (`idea_state.py:36`, `:155`) and it has a deliverable label
   (`deliverable_assembler.py:176` "Accepted risk"), but **no engine logic ever
   writes it** (verified: zero assignments across `engine/*.py`). It is a
   defined-but-unused closure state — a genuine seam whose activation would be a
   progression-state mutation and therefore an owner decision.

6. **Separate decision-workspace blocker model.** `engine/decision_workspace.py`
   maintains an independent candidate-decision lane with `DEFERRED` / `BLOCKED`
   / `BLOCKED_BY_EVIDENCE_GAP` codes, `disposition_basis`, `gap_blocker_code`
   (`:602`), and FDC-002 `BLOCKER_CLEARING_GUIDANCE` (`:159`). This is a
   distinct subsystem from the progression lane and from the unknown ledger.

7. **WS11 observation-only evaluation.** `evaluate_question_intent(...)`
   (`question_aware_evaluation.py`) returns a structural outcome
   (`SATISFIED / PARTIALLY_SATISFIED / NOT_SATISFIED / INVALID_INPUT`) that
   explicitly does **not** prove semantic fulfilment and mutates nothing.

---

## 6. Valid implementation seams (proposed, for a FUTURE gate only)

These are candidate seams a future owner-authorized WS12 increment *could*
build on. Listing them authorizes nothing.

- **VS-1 — Read-only unknown view.** A deterministic, observation-only reader
  over the existing `acknowledged_unknowns` track and the six-disposition
  ledger, exposing the current unknown/deferred/provisional/evidence-requested/
  specialist-requested state **without** mutating any of them.
- **VS-2 — Deterministic blocker *classification* (observation-only).** A pure
  function that *reports* whether a given unknown would block progression under
  an explicit, owner-ratified rule — **without** itself changing `maturity_level`
  or `Gap.status`. Whether such a classifier may ever gate progression is an
  owner decision (see OD-4).
- **VS-3 — Governed closure-path representation.** A deterministic mapping from
  an unknown to a valid closure path (answer-later, accept-risk, request
  evidence, request specialist), consuming the already-existing `pending` and
  supersession primitives. Writing any progression-affecting closure (e.g.
  `ACCEPTED_RISK`) is gated by OD-6/OD-11.
- **VS-4 — Provenance & supersession preservation.** Reuse the existing
  append-only, non-destructive ledger and supersession graph so no unknown's
  history is lost.
- **VS-5 — Interface-only boundaries to CAP-04 / CAP-08 / CAP-10.** Define the
  seam where a future action pack (CAP-04), assumption record (CAP-08), or
  contradiction (CAP-10) *would attach* to an unknown — as a typed boundary,
  not an implementation.

---

## 7. Invalid implementation seams (prohibited without separate authorization)

- **IS-1** Mutating `evaluate_transition` or `Gap.status` from unknown records
  (would let unknowns falsely advance maturity, or silently block it).
- **IS-2** Setting `resolves_gap = True`, or otherwise letting a disposition
  resolve a gap.
- **IS-3** Giving the acknowledged-unknown parallel track any progression
  effect without an explicit owner decision.
- **IS-4** Any AI / LLM / embedding / keyword-approximation classification of
  unknowns (deterministic only).
- **IS-5** Implementing CAP-04, CAP-08, or CAP-10 in full under the WS12 label.
- **IS-6** Any CAP-12 / CAP-13 / CAP-14 behavior (materials, thickness/safety,
  image/drawing interpretation).
- **IS-7** Any D13, WS-PFV-001, Patent Export, WS13, WS14, or AI Coach behavior.
- **IS-8** Any scoring, persistence-format, UI, prompt, database, or
  question-content change.

---

## 8. Protected boundaries

- `resolves_gap` remains `False` for every disposition.
- The acknowledged-unknown parallel track remains progression-neutral unless an
  owner decision (OD-1) changes it.
- `evaluate_transition` and `engine/scoring.py` remain unchanged.
- WS13 (`engine.guided_answer_support`) and WS14 (`engine.adaptive_follow_up`)
  remain **absent** — protected by
  `test_PROTECTED_no_workstream_13_to_14_capability_introduced`
  (`tests/test_workstream_9_single_intent_question_design.py:301`).
- MVP scope (electronics/electrical, LEVEL 0–2) and `MVP_SCOPE_FREEZE.md`
  remain in force.
- The append-only, non-destructive nature of the ledger and supersession graph
  is preserved (no deletion, no in-place mutation of prior records).

---

## 9. Capability-register overlap analysis (mandatory review)

For each required capability: does WS12 overlap it; does WS12 create a
prerequisite for it; does it remain deferred; does separate owner authorization
remain required; which protected boundary prevents silent absorption; does WS12
need only an interface boundary rather than implementation.

| Capability | WS12 overlap? | WS12 a prerequisite? | Deferred? | Separate owner auth still required? | Protected boundary preventing silent absorption | WS12 needs only an interface boundary? |
|---|---|---|---|---|---|---|
| **CAP-04 Gap Action Packs** | Yes — action packs attach to WS12 closure paths | Yes — CAP-04 lists "WS12 closure paths" as a dependency | Yes | Yes | "an action pack is never Evidence and never closes a gap" | **Yes** — interface only (IS-5) |
| **CAP-08 Assumption Register** | Partial — `provisional_assumption` disposition & ledger overlap | Yes — CAP-08 depends on the append-only ledger + WS12 | Yes | Yes | "assumptions are never Evidence; append-only, non-destructive history" | **Yes** — interface only (IS-5) |
| **CAP-10 Contradiction Detector** | Partial — reuses `mark_contradiction` / `has_unresolved_contradiction` | Possibly — shares the contradiction graph | Yes | Yes | "report-only with provenance; never auto-resolve or pick a winner" | **Yes** — interface only (IS-5) |
| **CAP-12 Prototype Materials & Manufacturing** | No | No | Yes | Yes (dedicated feasibility gate) | "distinct capability … must not be consolidated"; "must not infer material solely from visual appearance" | No implementation; no interface required by WS12 |
| **CAP-13 Thickness, Specification & Safety** | No | No | Yes | Yes (dedicated feasibility gate) | "distinct capability … must not be consolidated"; "must not infer a reliable thickness solely from an image" | No implementation; no interface required by WS12 |
| **CAP-14 2D Drawing / Static Image / Multi-View** | No | No | Yes | Yes (dedicated feasibility gate) | "VIDEO IS EXPLICITLY EXCLUDED"; "no inferred component … may enter canonical invention state until the user confirms it" | No implementation; no interface required by WS12 |
| **CAP-01 / D13 Structured Technical Guidance** | No (technical answers are D13's authority) | No | Yes | Yes (D13 authority) | D13 status language; "must not invent a technical answer" | No — technical content routes to D13 (OD-13) |
| **WS-PFV-001 Prototype Feasibility & Validation** | No | No | Yes | Yes | separate future-workstream owner decision | No |
| **Patent Export** | No | No | Yes | Yes | separate owner decision (PR #229) | No |

**Net finding:** WS12 overlaps CAP-04, CAP-08, and CAP-10 only at the *boundary*
(they consume WS12's unknown/closure model). WS12 must therefore define **typed
interface boundaries** to them and must **not** implement any of them. CAP-12,
CAP-13, CAP-14, D13, WS-PFV-001, and Patent Export are **out of scope** and each
retains its own separate gate.

---

## 10. Scope and non-goals

**In scope (documentation of a future deterministic, governed capability):**
represent acknowledged unknowns; distinguish unknown / deferred / provisional /
evidence-requested / specialist-requested states where already supported or
where an owner decision is required; determine (under an owner-ratified rule)
whether an unknown blocks progression; define explicit closure paths; preserve
provenance and supersession; prevent unsupported answers from falsely advancing
maturity; expose observation-only or deterministic decisions.

**Out of scope / non-goals:** CAP-04 in full; CAP-08 in full; CAP-10 in full;
CAP-12; CAP-13; CAP-14; D13; WS13; WS14; WS-PFV-001; Patent Export; AI Coach;
any AI/LLM behavior; any scoring, persistence, UI, prompt, database, or
question-content change.

---

## 11. Proposed deterministic contract boundaries (non-binding)

A future WS12 increment, if authorized, should:

- Be **deterministic** and **AI-free**.
- Default to **observation-only** unless an owner decision (OD-4/OD-6) grants a
  specific, bounded state-affecting behavior.
- Reuse the existing append-only ledger, `pending` semantics, provenance/
  validation axes, and supersession graph rather than introducing a parallel
  store.
- Keep `resolves_gap = False` and leave `evaluate_transition` / `scoring.py`
  untouched unless an owner decision explicitly authorizes a bounded change.
- Expose CAP-04 / CAP-08 / CAP-10 only as **typed interface boundaries**.
- Fail loud on invalid input; never silently coerce or infer.

---

## 12. Required owner decisions (re-derived; fresh IDs; not decided here)

Each decision is surfaced, not decided. Old D-A…D-P IDs are **not** reused; an
issue appears below only because fresh evidence shows it is still open.

Every decision lists: (1) Decision ID · (2) Question · (3) Current repository
evidence · (4) Options · (5) Trade-offs · (6) Recommendation · (7) Consequence
of deferring · (8) Protected surfaces affected · (9) Capability-register overlap
· (10) Required before BASE RED?

- **OD-1 — Observation-only vs state-mutating.**
  (2) May WS12 mutate progression state, or is it strictly observation-only?
  (3) Today unknowns are progression-neutral (`progression_loop.py:725`);
  ledger `resolves_gap=False`. (4) Observation-only / bounded owner-gated
  mutation. (5) Observation-only is safest but less powerful; mutation risks
  false maturity movement. (6) **Observation-only for v1.** (7) Deferring blocks
  the whole contract shape. (8) `evaluate_transition`, `Gap.status`, ledger.
  (9) CAP-04/08/10. (10) **Yes.**

- **OD-2 — Unknown record identity & lifecycle.**
  (2) Do WS12 unknowns reuse `AcknowledgedUnknown` + the ledger, or a new
  record type? (3) Two existing tracks already exist. (4) Reuse / new type.
  (5) Reuse preserves history & avoids drift; new type risks duplication.
  (6) **Reuse existing tracks.** (7) Ambiguous identity blocks BASE RED design.
  (8) `idea_state.py`. (9) CAP-08. (10) **Yes.**

- **OD-3 — Unknown classification vocabulary.**
  (2) Is the vocabulary exactly the six existing dispositions, or extended?
  (3) `INTERACTION_DISPOSITIONS` (`:111`) has six values. (4) Freeze at six /
  extend. (5) Freezing preserves parity; extending needs migration. (6)
  **Freeze at the six existing dispositions for v1.** (7) Vocabulary drift.
  (8) ledger. (9) CAP-08/10. (10) **Yes.**

- **OD-4 — Blocker authority.**
  (2) May an unknown ever block a maturity transition, and under what
  deterministic rule? (3) Today unknowns never block (`evaluate_transition`
  ignores them). (4) Never-block (report-only) / owner-ratified blocking rule.
  (5) Never-block keeps determinism simple but may let unsupported ideas
  advance; a blocking rule must be exact to avoid silent gating. (6)
  **Report-only for v1; any blocking rule is a separate later decision.**
  (7) Core behavior undefined. (8) `evaluate_transition`. (9) CAP-04. (10)
  **Yes.**

- **OD-5 — Importance / criticality source.**
  (2) Does WS12 read WS4 `CriticalityConfirmation` to weight unknowns? (3) WS4
  criticality history exists (`idea_state.py:405`). (4) Ignore / read-only
  consume. (5) Consuming adds signal but couples WS12 to WS4 semantics. (6)
  **Read-only consume at most; no new criticality authoring.** (7) Prioritization
  undefined. (8) criticality history. (9) CAP-05/06. (10) No (can defer).

- **OD-6 — Closure-path representation & the latent `ACCEPTED_RISK` seam.**
  (2) Which closure paths are valid, and may WS12 write `ACCEPTED_RISK`?
  (3) `ACCEPTED_RISK` is defined but **never written** by any engine logic.
  (4) Keep read-only / allow owner-gated `ACCEPTED_RISK` writing. (5) Writing it
  is a progression-state mutation (ties to OD-1). (6) **Do not write
  `ACCEPTED_RISK` in v1; document it as a future closure path.** (7) Closure
  model undefined. (8) `Gap.status`, deliverable. (9) CAP-04. (10) **Yes.**

- **OD-7 — Evidence requirements for closure.**
  (2) What evidence quality (if any) is required to close an unknown vs accept
  its risk? (3) `pending="evidence"` exists but has no closure workflow. (4)
  None / REASONED+ / specialist. (5) Higher bars are safer but slower. (6)
  **Define per closure path in the increment, not here.** (7) — (8) ledger.
  (9) CAP-11. (10) No.

- **OD-8 — Answer-later & supersession behavior.**
  (2) How does answering a previously-unknown item interact with supersession?
  (3) `mark_supersession` is acyclic, non-destructive. (4) Supersede / append.
  (5) Supersession preserves history cleanly. (6) **Reuse supersession.**
  (7) — (8) ledger graph. (9) CAP-08/10. (10) No.

- **OD-9 — Multiplicity of unknown records.**
  (2) May multiple unknown records coexist for one gap context? (3) The ledger
  already allows multiple records per `gap_context`. (4) One / many. (5) Many
  reflects reality; needs dedup rules. (6) **Allow many (as today).** (7) —
  (8) ledger. (9) CAP-10. (10) No.

- **OD-10 — Technical-user sufficiency.**
  (2) Does a technically sufficient answer bypass unknown capture? (3)
  `assess_response` sufficiency is deterministic; CAP-03 warns against
  expertise→unknown reinterpretation. (4) Yes / no. (5) — (6) **Follow existing
  deterministic sufficiency; no per-user relaxation.** (7) — (8) sufficiency
  gate. (9) CAP-03. (10) No.

- **OD-11 — Safety-critical unknowns.**
  (2) Are safety-critical unknowns handled specially (never silently accepted)?
  (3) WS4 `FEASIBILITY-THREATENING` category exists. (4) Uniform / special-case.
  (5) Special-casing safety is prudent but must stay deterministic. (6)
  **Never silently accept a safety-critical unknown; surface explicitly.** (7)
  Safety exposure. (8) criticality, closure paths. (9) CAP-13 (safety advisory
  is separate). (10) **Yes.**

- **OD-12 — Export & persistence boundaries.**
  (2) Are WS12 unknown states persisted or exported, or in-memory only? (3)
  Ledger is explicitly in-memory; persistence is frozen. (4) In-memory / persist.
  (5) Persisting crosses the persistence freeze. (6) **In-memory only for v1.**
  (7) — (8) persistence boundary. (9) CAP-05/07. (10) **Yes.**

- **OD-13 — D13 routing.**
  (2) When an unknown is a technical knowledge gap, does WS12 route to D13
  rather than answering it? (3) D13 owns technical guidance; CAP-01 must not be
  satisfied by generic referral. (4) Route / answer. (5) Answering would breach
  D13's authority. (6) **Route to D13 as a boundary; never answer technical
  content in WS12.** (7) D13-boundary breach risk. (8) — (9) CAP-01/D13. (10)
  **Yes.**

- **OD-14 — WS13 / WS14 separation.**
  (2) How does WS12 avoid drifting into guided-answer (WS13) or adaptive
  follow-up (WS14)? (3) Both modules are guarded absent (`:301`). (4) Strict
  separation / shared code. (5) Strict separation preserves the guard. (6)
  **Strict separation; no WS13/WS14 module introduced.** (7) Guard breach.
  (8) WS13/WS14 absence guard. (9) CAP-03. (10) **Yes.**

- **OD-15 — CAP-04 / CAP-08 / CAP-10 interaction depth.**
  (2) Interface boundary only, or partial implementation? (3) Each CAP depends
  on WS12 but is separately gated. (4) Interface-only / partial. (5) Partial
  implementation would silently absorb a separately-gated capability. (6)
  **Interface boundary only.** (7) Silent absorption risk. (8) — (9)
  CAP-04/08/10. (10) **Yes.**

- **OD-16 — CAP-12 / CAP-13 / CAP-14 prohibition.**
  (2) Confirm WS12 implements none of CAP-12/13/14. (3) All three are
  `RECORDED — NOT AUTHORIZED`, each a distinct gate. (4) — (5) — (6) **WS12
  implements none of CAP-12/13/14.** (7) Scope breach. (8) — (9)
  CAP-12/13/14. (10) **Yes (as a standing prohibition).**

---

## 13. BASE RED prerequisites

Before any WS12 BASE RED could be authorized (each is a separate owner action):

1. Resolution of the **"required before BASE RED"** owner decisions above
   (OD-1, OD-2, OD-3, OD-4, OD-6, OD-11, OD-12, OD-13, OD-14, OD-15, OD-16).
2. Owner ratification of the observation-only-vs-mutating boundary (OD-1) and
   the blocker-authority rule (OD-4).
3. A separate owner authorization explicitly starting WS12 BASE RED.
4. Confirmation that the WS13/WS14 absence guard and `MVP_SCOPE_FREEZE.md`
   remain in force.
5. A deterministic, AI-free test design with no scoring/persistence/UI/prompt/
   question-content change.

---

## 14. Acceptance criteria for the CONTRACT gate only

This contract gate is satisfied when:

- Exactly one new file
  (`docs/governance/WORKSTREAM_12_CONTROLLED_UNKNOWN_PROGRESSION_INCREMENT_CONTRACT.md`)
  is added; no other file changes.
- No code, test, roadmap, remediation-plan, or register file changes.
- The evidence lock, source review, current-behavior inventory, seam analysis,
  protected boundaries, capability-register review, and unresolved owner
  decisions are all present and traceable to the authoritative tip.
- WS12 status remains **NOT STARTED**; no later gate begins.

Acceptance of this contract gate does **not** authorize BASE RED or any
implementation.

---

## 15. Explicit status statement

**Workstream 12 (Controlled Unknown Progression) remains NOT STARTED.**

---

## 16. Explicit non-implementation statement

**No implementation is authorized by this document.** No BASE RED, GREEN,
production code, test, schema, persistence, UI, prompt/AI, database,
question-content, scoring, or progression-state change is authorized.

---

## 17. Capability recording statement

**CAP-12, CAP-13, and CAP-14 remain recorded only and unimplemented**
(`RECORDED — NOT AUTHORIZED FOR IMPLEMENTATION`). CAP-04, CAP-08, and CAP-10
likewise remain recorded and unimplemented; WS12 defines at most a typed
interface boundary to them.

---

## 18. Separate-gate statement

**D13 (Structured Technical Guidance / CAP-01), Patent Export, and WS-PFV-001
remain separately gated and inactive.** Each retains its own owner-authorization
chain and is not activated, started, or made prerequisite by this document.
