# MORE DETAIL NEEDED / GUIDED ANSWER SCAFFOLDING — INCREMENT CONTRACT (DRAFT)

## 1. Contract title and status

**More Detail Needed / Guided Answer Scaffolding — Increment Contract.**

Status: `INCREMENT CONTRACT DRAFT — MORE DETAIL NEEDED / GUIDED ANSWER
SCAFFOLDING; NOT IMPLEMENTED; NOT ACTIVATED; IMPLEMENTATION REQUIRES SEPARATE
OWNER AUTHORIZATION`

This document is a planning artifact only. It defines a *possible future
implementation increment*. It does NOT authorize execution, code, schema, UI,
template, runtime, session-flow, scoring, deliverable-generation, or persistence
change; it activates no feature and no domain. Implementation requires a
separate, explicit owner authorization after this contract is reviewed and
accepted.

---

## 2. Repository / branch / authoritative tip

- Repository: `Amirjaferali/inventorai`
- Authoritative branch: `feature/atomic-json-session-persistence`
- Authoritative tip at drafting: `c523b67f984b00faeee3f8edc2a7e9e26a308191`
  (PR #105 roadmap-synchronization true merge)
- Current official state remains: `DEMO_READY_WITH_LIMITATIONS`
- `main` remains separate and unchanged
  (`0e89e4636399760965c9ff8086b465c90dbadf8e`); no `main` sync occurred or is
  authorized.
- The frozen persistence worktree remains paused and untouched
  (`aec9cf6409efc18e125b6745762002f59e529654`); no paused persistence path is
  modified or authorized.
- The MVP remains electronics/electrical-only (`MVP_SCOPE_FREEZE.md`).

---

## 3. Evidence basis (PR #104 and PR #105)

Governing source chain:

- **PR #98** made the post-PR97 demo evidence record official
  (`docs/governance/DEMO_EVIDENCE_FINDINGS_POST_PR97.md`), which recorded the
  Repeated More Detail Needed Loop / Feedback UX Limitation (Demo 3B; §5; §6.B).
- **PR #101 / PR #102** implemented and closed the Domain Gate / Entry UX
  increment (the entry blocker), leaving the in-session "More detail needed"
  loop as the next blocker a non-specialist meets.
- **PR #104** made the More Detail Needed / Guided Answer Scaffolding owner
  scope decision official
  (`docs/governance/MORE_DETAIL_NEEDED_GUIDED_SCAFFOLDING_SCOPE_DECISION_POST_PR103.md`),
  admitting this candidate for Increment Contract preparation only (true-merge
  `7f8a72e3147f99c969c3a8829d9f5a6ebdab14c0`).
- **PR #105** synchronized the roadmap to record PR #104 as official (true-merge
  `c523b67f984b00faeee3f8edc2a7e9e26a308191`, the current authoritative tip).

This Increment Contract is the next planning artifact in that chain and
authorizes no implementation.

### 3.1 Carry-forward attribution corrections (mandatory)

Independent review of PR #104 identified two NON-BLOCKING §11 attribution
inaccuracies in the scope-decision document. PR #104's merged document is NOT
amended; the corrected attributions are recorded here, in this contract's
evidence section, and are the authoritative attributions for implementation-time
inspection:

1. **WARN reason strings** are produced by `integrate_response` (in
   `engine/progression_loop.py`), NOT by `evaluate_transition`. The scope
   decision's §11 phrase "the WARN `reason` strings in `evaluate_transition`" is
   corrected to attribute the WARN `reason` strings (e.g. "partially addressed —
   needs more depth" / "asserted only — reasoning required") to
   `integrate_response`.
2. **The session-view "Direction:" text** is surfaced from the
   `engine/progression_loop.py` result carried on the web layer's `last_result`
   (via `web/app.py`), NOT from `engine/summary.py`. The scope decision's §11
   phrase "the direction text from `engine/summary.py`" is corrected
   accordingly.

Implementation-time read-only inspection (see §11 below) must confirm these
corrected attributions against the code before any change is designed, and must
record any residual discrepancy for owner review rather than silently proceeding.

---

## 4. Problem statement

After a non-specialist inventor enters the session, the deterministic engine can
correctly determine that an answer is insufficient — it returns a WARN
transition and the session view shows the "More detail needed" badge — but the
bare/generic message does not tell the inventor **what kind of missing detail to
add**. The committed evidence (Demo 3B) shows detailed plain-language answers
about mechanism, safe working conditions, and operating boundaries repeatedly
receiving "More detail needed" without naming the missing dimension, which
reduces idea-development value and can loop.

The deterministic cause is already recorded as evidence (not as a change target
for this increment): `assess_response` scores plain-language answers as
`ASSERTED` (the generic-verb trap), gaps stay `PARTIAL`, and this is compounded
by a two-`REASONED`-answers-per-gap close requirement. This contract does NOT
change that scoring behavior (see §8); it improves only the *feedback* the
inventor sees when a WARN-class insufficiency is already determined.

---

## 5. User-value objective

Help the inventor understand what kind of missing detail to add — turning a bare
"More detail needed" into clear, bounded, non-inventive direction — so a
non-specialist can progress their own idea inside the session.

The inventor always remains the sole source of every fact. The system supplies
structure and direction only, never content. The objective is NOT to validate
feasibility, safety, compliance, buildability, or patentability, and NOT to
write, rewrite, correct, complete, or improve the inventor's answer.

---

## 6. Explicit distinction from Inventor Answer Clarification / Improve Wording Assistant

These are two different future candidates and must never be conflated:

- **Guided Answer Scaffolding (this contract)** asks the inventor *what to add*.
  When an answer is insufficient, it names missing detail *categories* and asks
  bounded, neutral questions. It never reads back, rewrites, or proposes edits to
  the inventor's text.
- **Answer Clarification / Improve Wording Assistant (separate, NOT activated)**
  operates on the answer *content* — it would rewrite/clarify the inventor's own
  text for approval before saving, using an
  `original_user_answer` → `suggested_clarified_answer` → `user_approved_answer`
  approval flow. That candidate is out of scope here and requires its own
  separate owner scope decision, Increment Contract, tests, review, and
  owner-gated true merge.

Both are also distinct from the already-implemented Increment 1B **question-level**
clarification (`web/clarification_labels.py`, `web/responsibility_labels.py`, the
"Help me understand this question" expander), which explains the *current
question before answering*. That material is display-only, must be preserved, and
must not be semantically overwritten by any answer-insufficiency guidance added
by this increment.

---

## 7. Authorized future implementation scope (only after a separate implementation authorization)

If separately authorized later, the increment would be limited to:

- Improving the user-facing feedback shown for WARN-class answer insufficiency:
  replacing or augmenting the bare "More detail needed" badge with specific,
  bounded, neutral direction.
- Naming missing detail **categories** (mechanism sequence, part/function
  mapping, trigger condition, operating boundary, assumption, unknown, supporting
  evidence or observation) — categories only, never suggested answer content.
- Showing bounded neutral prompts that ask the inventor for missing mechanism,
  context, constraint, or evidence detail (e.g. "What condition triggers the
  action?", "What does the device sense or detect?", "What output or response
  happens?").
- Deterministic, display-only derivation of the guidance from the *already
  computed* WARN outcome and the current gap context, added at render time.
- Preserving the original inventor answer exactly as given; guidance is additive
  display, not answer mutation.
- Adding tests covering guided and non-guided (sufficient-answer) behavior.
- Preserving unsupported-domain handling exactly as governed by the merged
  PR #101 domain-gate behavior.

The guidance is system structure, not inventor evidence. It must never be stored
as an owner answer, never close a gap, never advance maturity, never satisfy a
transition gate, never create an Evidence record, and never alter the
deterministic PASS/WARN/BLOCK outcome it accompanies.

---

## 8. Non-goals and prohibitions

The increment must NOT:

- implement anything under this contract (drafting only);
- write, rewrite, correct, complete, paraphrase, or "improve" any inventor
  answer;
- activate the Inventor Answer Clarification / Improve Wording Assistant;
- introduce a `suggested_clarified_answer` / `user_approved_answer` /
  `original_user_answer` / `clarification_status` data model or any equivalent;
- add any fact, component, number, value, mechanism, or engineering certainty
  the inventor did not provide;
- change the scoring algorithm (`assess_response`, `integrate_response`,
  `evaluate_transition`, the ASSERTED/REASONED rules, the generic-verb trap, the
  substance signals, or the two-`REASONED` gap-close requirement) — any scoring
  change is a SEPARATE future owner decision, not authorized or implied here;
- change deliverable generation (`engine/deliverable_assembler.py`) or the
  deliverable content/sections;
- change persistence or schema (any persistence/schema change is explicitly
  DEFERRED and NOT authorized; the frozen persistence lane stays paused);
- claim safety, feasibility, compliance, buildability, or patentability
  validation, or that the idea is valid/ready;
- perform engineering translation or risk generation;
- introduce a professional/specialist workspace;
- expand supported domains or activate IoT, robotics, drone, solar,
  `medical_device`, software-domain, mechanical-domain, or a multi-technology
  router;
- weaken or bypass the PR #101 domain-gate boundaries;
- sync `main`;
- touch the frozen persistence worktree;
- change the current official state from `DEMO_READY_WITH_LIMITATIONS`.

---

## 9. Expected user-facing behavior (conceptual level only — not implementation)

Described conceptually, not as design authority or implementation. When the
engine has already returned a WARN-class insufficiency for the current answer:

- show a specific, bounded guidance message instead of (or alongside) the bare
  "More detail needed" badge;
- name one or more missing detail *categories* relevant to the current gap;
- optionally show bounded neutral prompts (category-level questions), for
  example:
  - "What physical part or mechanism does this use?"
  - "What condition triggers the action?"
  - "What does the device sense or detect?"
  - "What output or response happens?"
  - "What evidence or observation supports this?"
- never suggest the answer content, never add facts, and never state the idea is
  valid, feasible, safe, patentable, or ready;
- when the answer is sufficient, continue normally with no unnecessary
  scaffolding loop.

Illustrative acceptance examples (to be refined at implementation time): "It
alerts people" → ask what condition triggers the alert and what mechanism detects
it; "It saves energy" → ask what behavior or measurement supports the claim; "It
uses a sensor" → ask what the sensor detects and what happens next. Illustrative
rejections: the system must not rewrite "It alerts people" into a complete
technical answer, must not invent "current sensor" (or any component/value/
mechanism), must not say the idea is feasible/safe, must not generate a
professional design, and must not admit an unsupported domain through
scaffolding.

---

## 10. Expected implementation boundaries

- **Additive, display-only.** Guidance is derived at render time from the already
  computed WARN result and current gap; it introduces no new stored state.
- **Engine outcome unchanged.** The deterministic PASS/WARN/BLOCK result, the gap
  lifecycle, maturity, transition gates, transcript, Evidence records, and the
  deliverable are all unchanged.
- **Answer text untouched.** The inventor's original answer is preserved
  byte-for-byte; no mutation, no read-back proposal.
- **Bounded surface.** The change is expected to be confined to the session
  presentation layer plus a small deterministic guidance provider, analogous in
  spirit to the Increment 1B display-only clarification and the PR #101
  render-path reuse — no scoring, persistence, schema, deliverable, or domain
  change.
- **Preserve prior increments.** PR #101 domain-gate behavior and the Increment
  1B question-level clarification/responsibility display must remain intact and
  clearly distinguished from the new answer-insufficiency guidance.

---

## 11. Candidate files to inspect later (read-only; DO NOT modify now)

File names below are **candidate future inspection areas only**; NO file change
is authorized by this contract draft, and actual paths must be re-confirmed
against the repository at implementation time under separate authorization.
Inspection must confirm the §3.1 corrected attributions before any change is
designed.

- `web/app.py` — session routes (`show_session`, `submit_answer`) and the
  surfaced `last_result` that carries the WARN outcome and its "Direction:" text
  to the view (corrected attribution: the direction/`last_result` originates in
  `engine/progression_loop.py`, surfaced via `web/app.py` — NOT
  `engine/summary.py`).
- `engine/progression_loop.py` — `assess_response`, `integrate_response` (which
  produces the WARN `reason` strings — corrected attribution, NOT
  `evaluate_transition`), `evaluate_transition`, `select_next_gap`,
  `get_display_question`. Interaction surface to UNDERSTAND, not an authorized
  change target (scoring is out of scope, §8).
- `web/templates/session.html` — where the WARN "More detail needed" badge and
  related feedback render today.
- `web/gap_labels.py` — existing gap labelling used by the session surface.
- `web/clarification_labels.py`, `web/responsibility_labels.py` — the Increment
  1B question-level clarification/responsibility material to preserve and clearly
  distinguish.
- `engine/idea_state.py` — gap/evidence state model (read-only understanding of
  what is stored vs display-only).
- `engine/deliverable_assembler.py` — acknowledged-unknowns handling (read-only;
  NOT a change target — deliverable generation is out of scope, §8).
- Tests to understand and keep green:
  `tests/test_assess_response_adversarial.py`,
  `tests/test_assess_response_replay.py`, transition/cascade tests
  (`tests/test_cascade_regression.py`), `tests/test_web_app.py`,
  `tests/test_domain_gate_entry_ux.py` (PR #101 regression),
  `tests/test_increment_1b_clarification_routing.py`,
  `tests/test_increment_1b_responsibility_guidance.py`.

---

## 12. Testing requirements for the future implementation

The future implementation (under separate authorization) must include at least:

- an insufficient (WARN-class) answer receives specific, category-level guidance,
  not a bare/generic refusal;
- a sufficient answer continues normally with no unnecessary scaffolding loop;
- guidance creates no session facts (no stored answer, no Evidence, no gap
  closure, no maturity change, no transition-gate satisfaction);
- guidance does not change the stored inventor answer (byte-for-byte preserved);
- the deterministic PASS/WARN/BLOCK outcome is identical with and without the
  guidance surface;
- no safety / feasibility / compliance / buildability / patentability claim
  appears in any guidance text;
- no domain expansion occurs through guidance;
- no Answer Clarification / Improve Wording activation occurs, and none of the
  prohibited `*_answer` / `clarification_status` fields are introduced;
- unsupported-domain answers remain rejected/bounded per the current domain-gate
  rules;
- regression: `tests/test_domain_gate_entry_ux.py` (PR #101) remains green;
- regression: Increment 1B clarification/responsibility display tests remain
  green;
- tests asserting no persistence file is changed and no `main` sync occurs.

---

## 13. Governance gates required before implementation

Before any implementation of this increment, in order:

1. This Increment Contract is independently reviewed and owner-accepted.
2. A SEPARATE explicit owner **implementation authorization** is granted for the
   exact bounded scope in §7.
3. Implementation happens in a dedicated branch/worktree created from the
   authoritative tip (not from `main`, not from the quarantined scratch branch).
4. Tests are authored (tests-first or with-source per the implementation
   authorization) and run; new-vs-baseline failures are distinguished honestly.
5. Scope is verified: only the authorized display-layer/guidance-provider paths
   are changed; no scoring, persistence, schema, deliverable, or domain change.

No scoring change, persistence change, deliverable change, or Answer Clarification
activation may be bundled into this increment; each is a separate future owner
decision.

---

## 14. Required independent review after implementation

After implementation and before any merge:

- a fresh, non-authoring independent review must verify the acceptance and
  regression behavior in §12, confirm the §8 prohibitions hold, and confirm the
  §10 boundaries (additive/display-only, engine outcome unchanged, answer text
  untouched);
- findings are resolved or owner-ruled;
- only then may an owner-gated **true merge** (no squash, no rebase) integrate the
  increment into `feature/atomic-json-session-persistence`.

---

## 15. This contract implements nothing by itself

This document is a contract draft only. It changes no code, test, template,
runtime, session flow, scoring, deliverable, schema, or persistence behavior. It
adds exactly one governance document to the repository and alters no product
behavior.

---

## 16. Owner implementation authorization still required

Implementation of More Detail Needed / Guided Answer Scaffolding is NOT
authorized by this contract. After this contract is reviewed and accepted, the
owner must SEPARATELY authorize implementation for the exact bounded scope in §7.
Until then, the app remains electronics/electrical-only for the MVP and the
current official state remains `DEMO_READY_WITH_LIMITATIONS`.

---

## 17. Final classification

`INCREMENT CONTRACT DRAFT ONLY — NO IMPLEMENTATION AUTHORIZED`
