# Plain-Language Result Feedback Increment Contract

## 1. Title

Plain-Language Result Feedback Increment Contract.

## 2. Contract status

Accepted only if this PR is later merged. **No implementation is authorized by
this contract PR itself.** This document defines the display-only future
implementation boundary; each downstream step remains separately owner-gated
(see Section 14).

## 3. Source review basis

The completed read-only source review (authoritative tip
`61443cff3abdab74282f06a18fbe354ace8f78f1`) found:

- The raw result **reason is produced in `engine/progression_loop.py`** —
  `integrate_response()` / `evaluate_transition()` / `run_iteration()` return a
  `result` dict whose `reason` string embeds the raw `gap_type` token (e.g.
  `"{gap_type} asserted only — reasoning required"`).
- The raw reason is **stored / pass-through in `last_result.reason`**
  (`SESSION_STORE[sid]["last_result"]`, in-memory only).
- The raw reason is **rendered in `web/templates/session.html`** via
  `{{ last_result.get('reason') }}` (the primary feedback line); the
  WARN/PASS/BLOCK badge is driven separately by `last_result.transition`.
- The raw reason is **ephemeral render state**. It **does not affect** scoring,
  persistence, transcript (the ILT-002 transcript record stores
  `session_id / iteration / question / response / domain / timestamp` — not the
  reason), deliverable, report, benchmark, or replay.
- **`score_case()` is a separate surface** (benchmark/replay scorer in
  `engine/scoring.py`) and must remain untouched.
- **Display-only implementation is feasible** and low-risk.

## 4. Critical de-risking finding

The raw `last_result.reason` **must remain preserved byte-for-byte.** This is
required both for governance / reporting integrity **and** because existing code
depends on raw-reason substrings, including:

- `web/scaffolding_guidance.py` (matches "stable substrings of the WARN reason
  string" to select its friendly category); and
- `web/app.py` WARN-detection logic (reads a `last_result.reason` substring).

Mutating the raw reason would silently break both consumers. The future
increment must therefore add a **parallel** friendly display and must never
change the raw reason.

## 5. Allowed production files for future implementation

- **NEW** `web/result_feedback.py` — a pure, deterministic, display-only helper
  (no engine / scoring / persistence / Safety-Signals imports; no I/O; no state)
  that maps the already-computed `(transition, gap_type)` (and, read-only, the
  raw reason) to friendly, content-free explanation text.
- `web/app.py` — **only** for one narrow render-context variable in
  `show_session` (e.g. `current_result_feedback=get_result_feedback(last_result, gap_type)`),
  mirroring the existing `current_scaffolding_guidance` variable. No other
  `web/app.py` change.
- `web/templates/session.html` — **only** to render the friendly feedback text
  while preserving the WARN/PASS/BLOCK badge and keeping the raw reason available
  for provenance (Section 9).

## 6. Allowed test files for future implementation

- **NEW** `tests/test_plain_language_result_feedback.py`
- `tests/test_web_app.py`

Only allow other tests if strictly necessary and justified in the implementation
PR report.

## 7. Forbidden files

- `engine/*`
- `engine/progression_loop.py`
- `engine/scoring.py`
- the `score_case()` surface
- `schemas/*`
- persistence / session store (`engine/session_store.py`)
- transcript behavior
- `engine/deliverable_assembler.py`
- deliverable / report behavior
- domain gate
- `engine/safety_signal.py`
- unrelated display helpers (`web/gap_labels.py`, `web/scaffolding_guidance.py`,
  `web/uncertainty_guidance.py`, `web/answer_coauthoring_prompts.py`,
  `web/clarification_labels.py`, `web/responsibility_labels.py`)
- `CLAUDE.md`
- governance anchors
- `ACTIVE_EXECUTION_ROADMAP.md`
- Arabic / RTL docs
- `main` / frozen / quarantined refs

## 8. Required future behavior

- Show friendly, plain-language result feedback in the visible session feedback
  line.
- Preserve the truthful WARN / PASS / BLOCK badge.
- Preserve the raw `last_result.reason` unchanged (byte-for-byte).
- Preserve failed criteria / issues (nothing dropped, recomputed, or reinterpreted).
- Preserve scaffolding guidance behavior (its raw-reason substring matching still works).
- Preserve existing WARN-detection behavior (`web/app.py`).
- Preserve saved user answers verbatim; no guidance text may be persisted as
  answer content.
- No change to score, transition, gap state, maturity state, deliverable,
  transcript, report, or domain gate.

## 9. Required provenance mechanism

The future implementation must keep the raw reason **available for provenance**
without showing raw internal jargon as the primary user-facing feedback. The
contract allows exactly one of these mechanisms, to be chosen and justified in
the implementation PR:

- a collapsed detail (`<details>`), or
- a tooltip / `title` attribute, or
- a `data-*` attribute, or
- another explicitly reviewed non-primary provenance display.

The implementation PR must state which mechanism was used and prove it does not
confuse the primary user feedback (i.e. the friendly text is the primary line;
the raw reason is secondary/on-demand).

## 10. Friendly-copy requirements

The implementation must pin exact friendly display strings (or exact string
patterns) for at least:

- WARN asserted-only reason;
- WARN partially-addressed reason;
- PASS demonstrated-evidence reason;
- PASS reasoned-follow-up reason;
- BLOCK / failed transition (if applicable);
- initial / no-result case (if applicable).

Friendly copy MUST:

- be supportive and plain-language;
- not hide the transition state;
- not imply readiness;
- not imply validation;
- not imply safety approval;
- not imply compliance approval;
- not imply patent-readiness;
- not imply feasibility validation;
- not write or suggest the user's answer;
- not instruct the user to invent unsupported facts.

**Pinned friendly-copy direction** (the implementation may refine wording but
must keep it content-free and non-validating; exact final strings are pinned in
the implementation PR for owner approval):

- WARN asserted-only:
  `You gave a starting answer, but the reasoning still needs more support.`
- WARN partially addressed:
  `You addressed part of this, but more detail is still needed.`
- PASS demonstrated evidence:
  `This point is supported well enough to move forward in the current demo flow.`
- PASS reasoned follow-up:
  `Your follow-up added enough reasoning to continue in the current demo flow.`
- BLOCK / not established:
  `This point is not established yet, so the idea cannot move forward on this item.`
- Initial / no-result:
  No feedback message renders until there is a result.

## 11. Required tests for future implementation

The implementation PR must test:

- raw `last_result.reason` preserved byte-for-byte;
- friendly feedback text rendered in the session UI;
- the raw internal token is **not** shown as the primary feedback line;
- WARN / PASS / BLOCK badge remains visible;
- failed criteria / issues remain visible or otherwise preserved;
- scaffolding guidance still triggers correctly;
- existing WARN-detection behavior still works;
- `score_case()` unchanged;
- scoring criteria unchanged;
- stage transitions unchanged;
- gap detection unchanged;
- transcript unchanged;
- deliverable unchanged;
- report behavior unchanged;
- saved answers remain verbatim;
- Answer Clarification remains inactive;
- Safety Signals remain closed;
- no forbidden readiness / validation / safety / compliance / feasibility /
  patent claims (forbidden-claim-word scan);
- six honest actions remain unchanged;
- no schema / persistence / domain-gate changes.

## 12. Required implementation PR evidence

Any future implementation PR must report:

- changed files;
- exact helper behavior;
- exact friendly strings;
- raw-reason preservation proof;
- provenance mechanism used;
- tests run and exact results;
- confirmation that engine / scoring / persistence / transcript / deliverable /
  report / domain gate were untouched;
- confirmation that Answer Clarification remains inactive;
- confirmation that Safety Signals remain closed;
- confirmation that official state remains `DEMO_READY_WITH_LIMITATIONS`;
- confirmation that MVP remains electronics/electrical-only.

## 13. Explicit non-goals

- no scoring rewrite;
- no `score_case()` change;
- no engine reason mutation;
- no hidden scoring truth;
- no Answer Clarification;
- no answer rewriting;
- no generated answer suggestions;
- no Safety Signals reopening;
- no readiness / validation / safety / compliance / patent claims;
- no full localization;
- no domain expansion;
- no persistence / session-store work;
- no `main` sync.

## 14. Required future governance sequence

Each step is separately owner-gated; this contract performs and authorizes none
of them:

1. Increment contract PR (this document).
2. Independent docs review.
3. Owner-gated true merge.
4. Roadmap sync PR.
5. Read-only implementation authorization.
6. Implementation PR.
7. Independent implementation review.
8. Owner-gated true merge.
9. Manual demo evidence PR.
10. Roadmap sync PR.

## 15. Boundary preservation

- Official state remains `DEMO_READY_WITH_LIMITATIONS`.
- MVP remains electronics/electrical-only.
- Answer Clarification remains inactive.
- Safety Signals remain closed.
- Saved answers remain verbatim; the inventor remains the sole author.
- **No implementation is authorized by this contract PR.**
- `main` remains `0e89e4636399760965c9ff8086b465c90dbadf8e` and is not
  synchronized; the frozen persistence lane remains PRESERVE UNMODIFIED AND PAUSE
  at `aec9cf6409efc18e125b6745762002f59e529654`; the quarantined scratch branch
  remains untouched at `02586747c902d5e1ebb78adde54ddd4ecd1c174a`.

## 16. Final classification

`PLAIN-LANGUAGE RESULT FEEDBACK INCREMENT CONTRACT CREATED — DOCS-ONLY — NO IMPLEMENTATION AUTHORIZED`
