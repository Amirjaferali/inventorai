# Workstream 13 — Guided Answer Support — Owner Decisions

> Documentation-only governance record. It ratifies the owner decisions that
> will bound a **future** WS13 Increment Contract. It authorizes **no**
> Increment Contract, BASE RED, implementation, GREEN, status canonicalization,
> or closure, and it changes no production code, test, or absence guard.

---

## 1. Authority and non-activation

- This document records ratified owner decisions only. It does not start
  Workstream 13, does not authorize an Increment Contract, BASE RED, GREEN,
  implementation, status canonicalization, or closure, and activates no later
  Workstream or Capability.
- It is grounded in the accepted **WS13 Evidence Lock and Fresh Source Review**
  performed on authoritative tip `8184c7ed66b076596d1f2ef0bc102cf95f6559c9`
  (PR #272 merge). It is subordinate to the committed governance anchors,
  `MVP_SCOPE_FREEZE.md`, `GOVERNANCE_MODEL.md`, `CLAUDE.md`, the
  `DELIVERABLE_STABILIZATION_REMEDIATION_PLAN.md` §15 status table, and the
  Capability Enrichment Register.
- Official product state remains `DEMO_READY_WITH_LIMITATIONS`; MVP scope
  remains electronics/electrical, LEVEL 0–2; Phase A remains fixed at
  `57e2fac8`.

---

## 2. Accepted evidence baseline (from the Evidence Lock)

The decisions below are grounded in these accepted findings:

- **The WS13 engine module is absent and protected.** `engine.guided_answer_support`
  does not exist; the absence guard
  `test_PROTECTED_no_workstream_13_to_14_capability_introduced`
  (`tests/test_workstream_9_single_intent_question_design.py:301`, asserting
  `engine.guided_answer_support` (WS13) and `engine.adaptive_follow_up` (WS14)
  absent at lines 315–316) and the re-assertion in
  `tests/test_workstream_12_controlled_unknown_progression_base_red.py:462`
  remain intact.
- **Substantial WS13-like behavior already exists in the web/display layer**
  (deterministic, display-only, content-free; all wired in `web/app.py:28–32`,
  rendered at `:579–618`):
  - `web/answer_coauthoring_prompts.py` — `get_answer_coauthoring_prompts(gap_type)`
    (`:109`): category-level "what you could include in your answer" prompts;
    "does not author, rewrite, complete, grade, or replace the answer".
  - `web/scaffolding_guidance.py` — `get_scaffolding_guidance(last_result, gap_type)`
    (`:196`): names the KIND of missing detail after a WARN insufficiency.
  - `web/uncertainty_guidance.py` — `get_uncertainty_guidance(text)` (`:174`),
    `is_uncertainty_text(text)` (`:144`): supportive prompts on explicit
    uncertainty (English and Arabic).
  - `web/clarification_labels.py` — `get_clarification(gap_type)` (`:171`):
    plain-language explanation of the current question.
  - `web/result_feedback.py` — `get_result_feedback(last_result)` (`:86`):
    plain-language result feedback.
- **Engine seams WS13 must not disturb:** question serving
  (`engine/path_n_questions.py::get_served_question` `:70`, `ServedQuestion`
  `:55`; `engine/progression_loop.py::get_question` `:213`); answer assessment
  and response integration (`assess_response` `:615`, `integrate_response`
  `:690`, returning `PASS/WARN` and mapping to `Gap.status`); the append-only
  six-`INTERACTION_DISPOSITIONS` ledger (`engine/idea_state.py::record_interaction`
  `:313`); WS12 observation-only unknown handling
  (`engine/controlled_unknown_progression.py` `:140`/`:176`); WS10 registry
  (`:184`/`:377`) and WS11 evaluation (`:95`).

**Consequence:** WS13 is **not wholly absent**. It governs and boundedly
improves the existing display-layer guided-answer support; it does not create a
capability from nothing.

---

## 3. Owner Decisions (OD-1 … OD-14) — ratified

Each decision is `OWNER DECISION — RATIFIED`. The "Binding invariant?" column
marks whether the decision is a binding invariant for a later WS13 Increment
Contract (§4 lists the full set).

- **OD-1 — Govern, do not treat as absent.** `OWNER DECISION — RATIFIED`.
  WS13 shall govern and boundedly improve the existing display-layer
  guided-answer support (§2). It shall not be treated as wholly absent, and it
  shall not re-create existing behavior as if new. *Binding invariant: yes.*

- **OD-2 — Web/display-layer only (v1).** `OWNER DECISION — RATIFIED`.
  WS13 v1 shall remain web/display-layer only. **No `engine.guided_answer_support`
  module shall be introduced.** *Binding invariant: yes.*

- **OD-3 — Absence guard preserved.** `OWNER DECISION — RATIFIED`.
  The existing WS13 engine-module absence guard shall remain intact and
  meaningful; WS13 v1 shall not require amending or weakening it. *Binding
  invariant: yes.*

- **OD-4 — Read-only inputs; no influence on engine outcomes.**
  `OWNER DECISION — RATIFIED`. WS13 **may read**: the currently served question;
  `question_id` and `design_gap_id`; `gap_type`; the already-computed
  `last_result`; and explicit user uncertainty. WS13 **may not change or
  influence**: assessment, scoring, progression, gap status, maturity,
  completion, or follow-up selection. *Binding invariant: yes.*

- **OD-5 — Help the user write their own answer; never author it.**
  `OWNER DECISION — RATIFIED`. WS13 shall help the user formulate **their own**
  answer through prompts, sentence starters, bounded examples, and categories of
  information that may be useful. It shall **never** invent project facts,
  generate a purported final factual answer, rewrite the answer silently, mark
  the answer complete, or submit/persist an answer without explicit user
  confirmation. *Binding invariant: yes.*

- **OD-6 — Preserve single-intent.** `OWNER DECISION — RATIFIED`.
  WS13 must preserve the single-intent boundary of the currently served question
  (WS9) and must not introduce a second independent request, split the question,
  or add a new iteration. *Binding invariant: yes.*

- **OD-7 — D13 boundary.** `OWNER DECISION — RATIFIED`.
  WS13 may explain the *type* of missing detail, but may not identify a technical
  research plan, measurement plan, test plan, document list, risk analysis, or
  specialist category. Those remain D13 (Structured Technical Guidance)
  boundaries and remain inactive. *Binding invariant: yes.*

- **OD-8 — WS12 boundary.** `OWNER DECISION — RATIFIED`.
  WS13 may display uncertainty-oriented help but must not classify, resolve,
  supersede, close, or mutate WS12 unknown records (it may read explicit
  uncertainty state only, per OD-4). *Binding invariant: yes.*

- **OD-9 — WS14 boundary.** `OWNER DECISION — RATIFIED`.
  WS13 shall not implement adaptive follow-up, question selection, completion
  logic, or decide what question comes next. Those remain WS14; the
  `engine.adaptive_follow_up` absence guard stays intact. *Binding invariant:
  yes.*

- **OD-10 — WS15 boundary.** `OWNER DECISION — RATIFIED`.
  WS13 shall not consolidate the existing guidance modules
  (`answer_coauthoring_prompts`, `scaffolding_guidance`, `uncertainty_guidance`,
  `clarification_labels`, `result_feedback`) into a new unified guidance
  architecture. Cross-module consolidation remains WS15. *Binding invariant:
  yes.*

- **OD-11 — EN/AR parity where both surfaces are committed.**
  `OWNER DECISION — RATIFIED`. Arabic and English behavioral parity is mandatory
  where both language surfaces are committed. Missing Arabic content must be
  reported as a gap, not falsely counted as parity. *Binding invariant: yes
  (conditional on committed bilingual surfaces).*

- **OD-12 — Deterministic provenance.** `OWNER DECISION — RATIFIED`.
  Guidance provenance must be visible or deterministically traceable to the
  current question, gap type, uncertainty state, or prior WARN `last_result`. No
  invented or non-traceable guidance. *Binding invariant: yes.*

- **OD-13 — Defect-driven minimal increment.** `OWNER DECISION — RATIFIED`.
  The smallest valid WS13 implementation increment must target a **proven,
  observable defect** in the existing display-layer behavior. Existing
  functionality alone is not sufficient reason to create code. *Binding
  invariant: yes (gate condition for any RED).*

- **OD-14 — No-valid-RED closure path.** `OWNER DECISION — RATIFIED`.
  If fresh contract analysis finds no observable failing WS13 behavior, WS13 may
  close through a documented **no-valid-RED disposition** — but only after
  independent evidence and explicit owner acceptance. *Binding invariant: yes
  (governs closure).*

---

## 4. Binding invariants for a later WS13 Increment Contract

The following are binding invariants any future WS13 Increment Contract must
carry unchanged: **OD-1, OD-2, OD-3, OD-4, OD-5, OD-6, OD-7, OD-8, OD-9, OD-10,
OD-11, OD-12, OD-13, OD-14.** In short: web/display-layer only; absence guard
preserved; read-only over the listed inputs with no influence on engine
outcomes; help-not-author with explicit user confirmation before submit/persist;
single-intent preserved; strict D13 / WS12 / WS14 / WS15 separation;
deterministic provenance; EN/AR parity where committed; defect-driven minimal
scope; and a governed no-valid-RED closure path.

---

## 5. Existing behavior vs formally-governed WS13 behavior

- **Existing (merged, display-layer):** the five `web/` modules in §2 already
  provide category-level answer prompts, WARN scaffolding, uncertainty support,
  question clarification, and plain-language feedback. This behavior exists and
  is wired into the app today; it is **not** attributed to a formally governed
  WS13.
- **Formally-governed WS13 (future):** a bounded governance envelope over that
  existing display-layer support — defined by OD-1…OD-14 — that may boundedly
  improve it only to fix a proven observable defect (OD-13), or close via the
  no-valid-RED path (OD-14). WS13 adds no engine module (OD-2/OD-3) and changes
  no engine outcome (OD-4).

---

## 6. Non-authorization statement

These Owner Decisions **do not authorize** a WS13 Increment Contract, BASE RED,
implementation, GREEN, status canonicalization, or closure. Each of those
remains a separate, explicitly owner-authorized gate. WS13 remains **NOT
STARTED**. WS14, WS15, WS16, WS17, D13 (Structured Technical Guidance), Patent
Export, WS-PFV-001, and CAP-12/CAP-13/CAP-14 remain inactive, separately gated,
or unauthorized, and are not activated by this document. The AI Coach (WS17)
remains BLOCKED until Workstreams 1–16 are owner-closed.
