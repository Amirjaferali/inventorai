# MORE DETAIL NEEDED / GUIDED ANSWER SCAFFOLDING — OWNER SCOPE DECISION (POST-PR #103)

## 1. Status

`OWNER SCOPE DECISION — MORE DETAIL NEEDED / GUIDED ANSWER SCAFFOLDING ADMITTED
FOR FUTURE INCREMENT CONTRACT ONLY; NO IMPLEMENTATION AUTHORIZED`

This document records an owner scope decision only. It admits the More Detail
Needed / Guided Answer Scaffolding candidate for future Increment Contract
preparation. It authorizes NO implementation, code, test, schema, UI, template,
runtime, session, scoring, persistence, or domain change, no Increment Contract
in this step, no roadmap change, no `main` synchronization, and no MVP
activation of any kind.

---

## 2. Authoritative state

- Repository: `Amirjaferali/inventorai`
- Authoritative branch: `feature/atomic-json-session-persistence`
- Current authoritative tip: `ed8512aa95e6d2a4e0cb42e1feb5d9d2a969d567`
  (PR #103 roadmap-synchronization true merge)
- Current official state remains: `DEMO_READY_WITH_LIMITATIONS`
- `main` remains separate and unchanged
  (`0e89e4636399760965c9ff8086b465c90dbadf8e`); no `main` sync occurred or is
  authorized.
- The frozen persistence worktree remains paused and untouched
  (`aec9cf6409efc18e125b6745762002f59e529654`); no paused persistence path is
  modified or authorized.
- PR #101 (Domain Gate / Entry UX implementation), PR #102 (PR #101
  implementation closure record), and PR #103 (minimal roadmap synchronization)
  are official and closed.
- The MVP remains electronics/electrical-only (`MVP_SCOPE_FREEZE.md`).

---

## 3. Problem statement

The product can identify that a user answer is insufficient — the deterministic
engine returns a WARN transition and the session view shows the "More detail
needed" badge — but the user may not know what kind of detail to add. A bare or
generic "More Detail Needed" response can reduce idea-development value because
the inventor is not guided toward evidence-grounded improvement of their own
answer.

Committed source evidence (`docs/governance/DEMO_EVIDENCE_FINDINGS_POST_PR97.md`,
Demo 3B and §5, §6.B):

- After entering the session flow, the app repeatedly returned "More detail
  needed" after detailed owner answers about the step-by-step mechanism, safe
  working conditions, and operating boundaries.
- The read-only diagnostic recorded the deterministic cause: `assess_response`
  scores plain-language answers as `ASSERTED` (the generic-verb trap penalizes
  natural verbs such as "detects"/"sends" unless paired with a fixed
  causal-structure keyword), gaps therefore remain `PARTIAL`, this is compounded
  by a two-`REASONED`-answers-per-gap close requirement, and the WARN message
  does not name the missing dimension.
- The evidence record classifies this as the **Repeated More Detail Needed
  Loop / Feedback UX Limitation** and ranks it as improvement candidate #2,
  immediately after the Domain Gate / Entry UX limitation that PR #101 has now
  addressed.

With PR #101 official, the entry blocker is improved, and this feedback
limitation is the next blocker a non-specialist user meets inside the session.

---

## 4. Owner intent

The owner wants visible idea-development value, not governance overhead.

The system should help the inventor progress the idea by asking for missing
details in a clear, bounded, non-inventive way. The inventor must always remain
the source of every fact; the system supplies structure and direction, never
content.

---

## 5. Candidate admitted scope (future Increment Contract only)

The following is admitted for a future Increment Contract only. Nothing in this
list is authorized for implementation by this document:

- User-facing guidance shown when an answer is insufficient (WARN-class
  outcomes), replacing or augmenting the bare "More detail needed" experience
  with specific, bounded direction.
- Neutral prompts that ask the user for missing mechanism, context, constraint,
  or evidence detail.
- Optional examples of detail *categories* (mechanism sequence, part/function
  mapping, trigger condition, operating boundary, assumption, unknown,
  supporting evidence or observation) — categories only, never suggested answer
  content.
- Preserving the original user answer exactly as given; guidance is additive
  display, not answer mutation.
- No invention by the system.
- No factual additions by the system.
- No validation or readiness claims of any kind.
- No rewriting of user answers.
- No domain expansion.

---

## 6. Explicit non-goals

This scope decision does NOT authorize any of the following, and the future
Increment Contract must preserve these exclusions unless a separate owner
decision states otherwise:

- No implementation in this decision.
- No answer rewriting.
- No Inventor Answer Clarification / Improve Wording Assistant activation.
- No `suggested_clarified_answer` / `user_approved_answer` /
  `original_user_answer` / `clarification_status` data model.
- No persistence or schema changes.
- No deliverable generation changes.
- No scoring algorithm change (`assess_response`, `evaluate_transition`,
  gap-close rules) unless separately authorized by its own owner decision.
- No engineering translation.
- No risk generation.
- No feasibility / safety / compliance / buildability / patentability
  validation.
- No professional workspace.
- No domain expansion.
- No IoT / robotics / drone / solar / medical / software / mechanical support.
- No multi-technology router.
- No `main` sync.

---

## 7. Boundary from Answer Clarification / Improve Wording

These are two different future candidates and must never be conflated:

- **Guided Answer Scaffolding (this candidate)** asks the user *what to add*.
  When an answer is insufficient, it names the missing detail categories and
  asks bounded, neutral questions. It never touches the user's text.
- **Answer Clarification / Improve Wording Assistant (separate candidate)**
  rewrites or clarifies the user's own text for approval before saving. It
  operates on the answer content itself and requires the
  `original_user_answer` → `suggested_clarified_answer` → `user_approved_answer`
  approval flow described in `DEMO_EVIDENCE_FINDINGS_POST_PR97.md` §3 and the
  backlog note `docs/product/INVENTOR_ANSWER_CLARIFICATION_FEATURE_BACKLOG.md`.

Only the first candidate — Guided Answer Scaffolding — is under scope decision
here. The second remains a future, non-activated candidate and requires its own
separate owner scope decision, Increment Contract, tests, review, and
owner-gated true merge before any implementation.

Both candidates are also distinct from the already-implemented Increment 1B
**question-level** clarification (`web/clarification_labels.py`,
`web/responsibility_labels.py`, the "Help me understand this question"
expander), which explains the current question before answering. That material
is display-only, must be preserved, and must not be semantically overwritten by
any future answer-level feature.

---

## 8. Potential future behavior model (candidate behavior only — not implementation)

Described only as future candidate behavior, not as implementation or design
authority. When an answer is insufficient:

- show a specific, bounded guidance message instead of (or alongside) the bare
  "More detail needed" badge;
- ask for one or more missing detail categories;
- examples of bounded neutral prompts:
  - "What physical part or mechanism does this use?"
  - "What condition triggers the action?"
  - "What does the device sense or detect?"
  - "What output or response happens?"
  - "What evidence or observation supports this?"
- avoid suggesting the answer content;
- avoid adding facts;
- avoid saying the idea is valid, feasible, safe, patentable, or ready.

The guidance is system structure, not user evidence: it must never be stored as
an owner answer, never close a gap, never advance maturity, and never alter the
deterministic PASS/WARN/BLOCK outcome it accompanies.

---

## 9. Acceptance examples for the future contract

Illustrative acceptance examples the future Increment Contract should refine:

- If the user says "It alerts people", the system asks what condition triggers
  the alert and what device or mechanism detects that condition.
- If the user says "It saves energy", the system asks what behavior or
  measurement supports that claim.
- If the user says "It uses a sensor", the system asks what the sensor detects
  and what happens next.
- If the user provides enough mechanism detail, the system should not loop
  unnecessarily — sufficient answers continue normally without repeated
  scaffolding.

---

## 10. Rejection / out-of-scope examples

The future contract must treat the following as violations:

- The system must not rewrite "It alerts people" into a complete technical
  answer.
- The system must not invent "current sensor" (or any component, value, or
  mechanism) unless the user provided it.
- The system must not say the idea is feasible or safe.
- The system must not generate a professional engineering design.
- The system must not activate non-electronics domains.
- The system must not treat an unsupported domain as accepted through
  scaffolding — unsupported-domain handling remains governed by the PR #101
  domain-gate behavior and its boundaries.

---

## 11. Evidence to gather before the Increment Contract

A future Increment Contract must inspect and record, read-only first:

- the current question/answer flow (`web/app.py` session routes,
  `web/templates/session.html`, `engine/progression_loop.py`);
- the existing insufficiency detection logic (`assess_response` at
  `engine/progression_loop.py`, the ASSERTED/REASONED rules, the generic-verb
  trap, substance signals, and the two-`REASONED` gap-close requirement) — as
  interaction surface to understand, not as an authorized change target;
- where "More Detail Needed" appears to the user today (the WARN badge in
  `web/templates/session.html`, the WARN `reason` strings in
  `evaluate_transition` such as "partially addressed — needs more depth" /
  "asserted only — reasoning required", and the direction text from
  `engine/summary.py`);
- how session state handles answers (what is stored, what is display-only,
  what reaches the transcript and deliverable);
- where deliverable unknowns are generated (acknowledged-unknowns handling,
  `engine/deliverable_assembler.py`);
- tests covering insufficient answers (`tests/test_assess_response_adversarial.py`,
  `tests/test_assess_response_replay.py`, and related transition/cascade tests);
- any existing user-facing messages that already provide partial guidance;
- interaction with the PR #101 domain-gate behavior in `web/app.py`
  (`tests/test_domain_gate_entry_ux.py` must remain green);
- interaction with the Increment 1B question-level clarification material
  (`web/clarification_labels.py`, `web/responsibility_labels.py`,
  `tests/test_increment_1b_clarification_routing.py`,
  `tests/test_increment_1b_responsibility_guidance.py`), which must be
  preserved and clearly distinguished from any new answer-insufficiency
  guidance.

---

## 12. Testing expectations for the future contract

Future tests should include at least:

- an insufficient answer gets specific guidance, not a generic refusal;
- a sufficient answer continues normally with no unnecessary scaffolding loop;
- guidance does not create session facts;
- guidance does not change the stored answer;
- no safety / feasibility / compliance claims appear in any guidance text;
- no domain expansion occurs through guidance;
- no answer-clarification (Improve Wording) activation occurs;
- unsupported-domain answers remain rejected or bounded according to the
  current domain-gate rules;
- regression tests for PR #101 behavior (`tests/test_domain_gate_entry_ux.py`)
  remain green;
- regression tests for Increment 1B clarification/responsibility display
  remain green.

---

## 13. Product impact

This is likely the next highest-value candidate because it improves the user's
ability to progress inside the demo after entry, while preserving MVP
boundaries. PR #101 improved the entry experience; the committed demo evidence
shows the "More detail needed" loop is the next point where a non-specialist
loses idea-development value.

But it remains only a candidate until an Increment Contract and a separate
implementation authorization are approved.

---

## 14. Decision

**ADMITTED FOR FUTURE INCREMENT CONTRACT PREPARATION ONLY.**

**NO IMPLEMENTATION AUTHORIZED.**

---

## 15. Next step

Recommended next step: prepare a formal Increment Contract for More Detail
Needed / Guided Answer Scaffolding, subject to owner approval. Drafting that
Increment Contract is NOT authorized by this document and requires its own
separate owner authorization. Any subsequent work must proceed, in order,
through: this scope decision (admission only); a separately authorized
Increment Contract; a separate implementation authorization; tests; independent
review; and an owner-gated true merge. The app remains
electronics/electrical-only for the MVP, and the current official state remains
`DEMO_READY_WITH_LIMITATIONS`, until separate governed decisions state
otherwise.
