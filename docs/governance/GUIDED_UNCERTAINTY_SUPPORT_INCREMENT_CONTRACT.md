# GUIDED UNCERTAINTY SUPPORT — INCREMENT CONTRACT

## 0. Status

`GUIDED UNCERTAINTY SUPPORT INCREMENT CONTRACT — DOCS-ONLY — NO IMPLEMENTATION
AUTHORIZED`

This document defines a **minimal, safe, owner-gated future implementation
contract** for **Guided Uncertainty Support**, derived from the merged
Inventor Supportive Guidance & Non-Exam UX scope decision
(`INVENTOR_SUPPORTIVE_GUIDANCE_NON_EXAM_UX_SCOPE_DECISION.md`, PR #132;
roadmap-recorded by PR #133). It is **contract documentation only**. It authorizes
NO implementation, code, test, schema, UI, route, template, runtime, session,
scoring, maturity, readiness, criticality, persistence, or domain change; no
roadmap change in this step; and no `main` synchronization or MVP activation of
any kind. It is NOT source-review authorization.

File-creation record (per `CLAUDE.md` File Creation Rules):
- File path: `docs/governance/GUIDED_UNCERTAINTY_SUPPORT_INCREMENT_CONTRACT.md`
- Purpose: define the smallest future Guided Uncertainty Support increment and its
  hard boundaries, so a later — separately authorized — implementation has an
  evidence-grounded, anti-drift contract to build against.
- Input contract: the merged scope decision
  (`INVENTOR_SUPPORTIVE_GUIDANCE_NON_EXAM_UX_SCOPE_DECISION.md`), the committed
  dual-path product intent (`DUAL_PATH_PRODUCT_ANCHOR.md`), `MVP_SCOPE_FREEZE.md`,
  and the evidence-locked state at authoritative tip
  `cd5aa8f3861d4ddf180487dfbaf75ed796a3ae60`.
- Output contract: a single future-implementation contract draft (§17
  classification) with its objective, supported inputs, boundaries, required
  future tests, manual-demo expectations, governance gates, and stop conditions;
  nothing executable, nothing activating.
- Prohibited behaviors: this file must never be read as implementation
  authorization, source-review authorization, scoring authorization, activation
  of the Inventor Answer Clarification / Improve Wording feature, a roadmap
  update, or a `main`/frozen/quarantined branch change.

---

## 1. Current state (evidence-locked)

- Repository: `Amirjaferali/inventorai`.
- Authoritative branch: `feature/atomic-json-session-persistence`.
- Authoritative tip: `cd5aa8f3861d4ddf180487dfbaf75ed796a3ae60`.
- Latest merged PR: **#133**.
- Official state: **`DEMO_READY_WITH_LIMITATIONS`**.
- MVP scope: **electronics/electrical-only** (`MVP_SCOPE_FREEZE.md`).
- The **Inventor Supportive Guidance & Non-Exam UX scope decision** (PR #132) is
  **merged**, and its **roadmap sync** (PR #133) is **merged**; Guided
  Uncertainty Support is a **FUTURE OWNER-GATED INCREMENT CANDIDATE ONLY**.
- The Guided Answer Co-Authoring Increment 1 lineage (PR #125–#131) is closed and
  recorded.
- **No implementation is authorized yet.** No product-execution lane is open; per
  roadmap §8, no lane may be inferred, and a separate explicit owner
  authorization is required before any working-tree write or product
  implementation.
- `main` remains separate and unchanged
  (`0e89e4636399760965c9ff8086b465c90dbadf8e`); the frozen persistence worktree
  remains paused and untouched (`aec9cf6409efc18e125b6745762002f59e529654`); the
  quarantined scratch branch remains untouched
  (`02586747c902d5e1ebb78adde54ddd4ecd1c174a`).

---

## 2. Contract objective

Define the **smallest future increment** that **supports uncertainty-style user
answers** — helping the user find a way forward when they are stuck — **without
making the user feel tested, judged, or blocked**, and **without writing the
answer for the user**. The increment realizes the merged principle: **InventorAI
is a supportive idea-development assistant, not an exam-like evaluator**. Its
value is **idea development** (reducing drop-off for non-specialist inventors) —
not inventor education, and not answer generation. The inventor remains the sole
author and source of any saved answer.

---

## 3. Supported uncertainty inputs

A future implementation should recognize uncertainty-style expressions, for
example (illustrative, not exhaustive):

English:
- "I don't know";
- "I'm not sure";
- "I don't understand the question";
- "I don't know the technical term";
- "I don't know how it works".

Arabic equivalents:
- "لا أعرف";
- "غير متأكد";
- "لا أفهم السؤال";
- "لا أعرف المصطلح التقني";
- "لا أعرف كيف تعمل".

The existing journey already offers a structured **"I do not know this yet"**
owner action (Increment 1A) and honest non-answer actions (deferred, provisional
assumption, specialist requested, evidence requested). Detection of
uncertainty-style *free-text* is a candidate signal for the supportive response
and must be treated as **display context only** — it must never recompute or
alter any scored outcome, and Arabic/English handling must remain within the
electronics/electrical MVP.

---

## 4. Intended future behavior

A later — separately authorized — implementation **may** display supportive,
optional guidance such as:

- "That's okay — start with what you know.";
- "You do not need technical terms yet.";
- "Describe the result you want.";
- "Tell us which part is unclear.";
- "What do you imagine happens first?";
- "What part do you already know?"

These are candidate, content-free, category-level prompts that invite the
inventor to express what they *do* know. They are illustrative only; none is
implemented or authorized by this contract.

---

## 5. UX contract

Any future implementation must be:

- **supportive** — reduces anxiety, never scolds;
- **non-judgmental** — no "wrong" / "failed" / "insufficient" / "you did not
  answer correctly" framing;
- **optional** — the inventor may ignore it entirely;
- **advisory** — it guides, it does not decide;
- **user-authored** — the inventor writes the answer;
- **non-exam-like** — supportive wording (scope-decision §9);
- **safe for non-technical users** — no demand for engineering parameters a
  non-specialist cannot supply (`DUAL_PATH_PRODUCT_ANCHOR.md` §3.3).

Supportive wording must remain **truthful**: it may not convert an open gap into
a closed one, imply an answer is validated, or hide a known-unknown.

---

## 6. Authorship contract

The system must **never**:

- write the answer for the user;
- replace user text (silently or otherwise);
- save generated guidance as the answer;
- imply that generated guidance is user-authored;
- invent components, numbers, mechanisms, materials, safety facts, or domain
  details on the user's behalf.

The inventor remains the **sole author and source** of any saved answer; the
saved answer is the inventor's verbatim text.

---

## 7. Boundary with Guided Answer Co-Authoring

- **Guided Answer Co-Authoring (Increment 1, merged PR #129)** gives **optional
  prompts near normal questions** — "what you could include".
- **Guided Uncertainty Support (this candidate)** handles **uncertainty / "I
  don't know" situations** — helping a stuck user find a way forward.
- **Both remain advisory and display-only** and preserve inventor authorship.
- **Neither may become Answer Clarification.** The two surfaces must remain
  visibly distinct; this increment must not remove, degrade, or duplicate the
  existing Co-Authoring surface.

---

## 8. Boundary with Answer Clarification / Improve Wording

The increment **must not** introduce:

- `original_user_answer`;
- `suggested_clarified_answer`;
- `user_approved_answer`;
- `clarification_status`;
- (or any equivalent field);
- an approval/save clarified-answer flow;
- rewrite / apply / save suggestion controls.

The separate **Inventor Answer Clarification / Improve Wording** feature remains
**SEPARATE and NOT ACTIVATED**. Any drift toward rewriting/approving/saving a
clarified answer is that (non-authorized) feature by another name and is out of
scope.

---

## 9. Boundary with scoring and engine state

The increment **must not**:

- change scoring thresholds (`assess_response` / `integrate_response` /
  `evaluate_transition` / generic-verb trap / causal tokens);
- change maturity / readiness / criticality (the Increment-4 `criticality` field
  stays `UNDETERMINED` / system-derived);
- close gaps automatically;
- mark an uncertainty answer as sufficient;
- change Section 6 risks;
- populate `RequirementLandscape.risks` (stays `()`);
- claim feasibility, correctness, safety, compliance, patent readiness, or
  engineering readiness.

An uncertainty answer must remain a truthful, still-open state; supportive
guidance changes tone, never epistemic state.

---

## 10. Boundary with persistence / schema

The increment **must not**:

- add database fields;
- add session schema fields;
- add transcript schema fields;
- persist generated guidance as answer content;
- modify saved-answer provenance.

The persistence lane stays PAUSED and untouched; the supportive surface is a
render-time display only.

---

## 11. MVP boundary

The increment must remain **electronics/electrical-only**. No domain expansion;
no general writing assistant; no generic tutor mode (supportive guidance is not
tutor mode; scope-decision §3).

---

## 12. Likely future source-review surfaces (inspect only — do not change now)

The following are **candidate surfaces to inspect during a later read-only source
review** — named from present repository evidence, not prescribed as edit
targets. No file below may be changed by this contract; the exact, minimal change
set must be established by that later review:

- **Existing display-only guidance precedent to mirror:**
  - `web/answer_coauthoring_prompts.py` (Guided Answer Co-Authoring Increment 1 —
    the pure, deterministic, display-only pattern)
  - `web/clarification_labels.py`, `web/scaffolding_guidance.py`
- **Render + (read-only) uncertainty-context surfaces:**
  - `web/app.py` — `show_session` render context; and the existing non-answer /
    "I do not know this yet" action handling in `submit_answer` (referenced
    **read-only** to confirm supportive guidance needs no persistence change)
  - `web/templates/session.html` (where a bounded supportive panel could later
    render, near the question/answer area)
- **Response/gap classification** — inspected **only if needed** and **only
  read-only** to derive a display signal; no scoring/classification change is in
  scope.
- **Tests** — a new dedicated test module for uncertainty guidance behavior.

A **later read-only source review is required before any implementation** to (a)
confirm the minimal increment can be delivered purely as display-only/advisory
guidance with **no** persistence/session-schema field, **no** approval/save flow,
and **no** Answer-Clarification interaction; (b) fix the exact, minimal surface;
and (c) prove the §6/§8/§9/§10 forbidden sets are untouched. Until that review,
no surface is committed and no code change is prescribed.

---

## 13. Required later implementation evidence (tests)

A future implementation must include tests proving:

1. **Uncertainty input triggers supportive guidance** for eligible
   electronics/electrical questions.
2. **Guidance is optional/advisory** and visibly labeled as such.
3. **The user answer is preserved verbatim** — the saved answer equals the
   inventor's own entered text.
4. **No generated guidance is saved as answer content** (guidance text never
   becomes stored answer content).
5. **No hidden fields or approval/save controls are introduced.**
6. **No scoring/schema/Safety-Signals behavior changed** — the locked scoring
   suites (`tests/test_assess_response_replay.py`,
   `tests/test_assess_response_adversarial.py`), the Increment-6 top-level
   contract (`test_traceability_no_orphan_toplevel_keys`), and
   `tests/test_safety_signal.py` remain green (baseline: failures confined to
   `tests/test_domain_registry.py`; zero new failures).
7. **Arabic and English uncertainty examples are handled** if feasible within the
   electronics/electrical MVP.
8. **The Guided Answer Co-Authoring and clarification/scaffolding surfaces remain
   present and distinct.**

---

## 14. Manual demo expectations (future)

A future manual demo should show:

- the user writes "I don't know" or "لا أعرف";
- the UI responds **supportively** (non-exam wording);
- the user is invited to **describe what they do know**;
- **no answer is auto-written**;
- the **saved answer remains user-authored** (verbatim);
- **no exam-like wording** ("wrong" / "failed" / "insufficient") appears.

---

## 15. Governance path

This contract authorizes **no implementation**. If accepted (independently
reviewed and owner-gated true-merged), the future sequence is:

roadmap sync (separate, if required) → **read-only source review** → **separate
implementation authorization** → implementation PR → tests → independent review →
owner-gated true merge → **separate manual demo verification** → **separate
roadmap synchronization**.

Any implementation must be **separately owner-gated**, and a read-only source
review must precede it. No step beyond this contract is authorized here, and none
may be inferred (roadmap §8.1–§8.2).

---

## 16. Stop conditions

Stop and report — do not proceed under this contract — if the contract (or any
reading of it) would:

- authorize implementation or source review;
- change the roadmap;
- activate Answer Clarification / Improve Wording;
- introduce answer rewriting;
- introduce approval/save clarified-answer flows;
- introduce persistence/session/transcript schema fields;
- change scoring / readiness / maturity / criticality;
- reopen Safety Signals;
- expand MVP scope beyond electronics/electrical;
- imply the system may write the user's answer;
- imply an uncertainty answer can close a gap by itself;
- touch any file outside the one new `docs/governance/` contract.

---

## 17. Final classification

`GUIDED UNCERTAINTY SUPPORT INCREMENT CONTRACT — DOCS-ONLY — NO IMPLEMENTATION
AUTHORIZED`
