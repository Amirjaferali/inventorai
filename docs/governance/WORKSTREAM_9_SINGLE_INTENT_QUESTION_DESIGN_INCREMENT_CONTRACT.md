# Workstream 9 — Single-Intent Question Design: Increment Contract

**Status:** INCREMENT CONTRACT — **docs-only, non-implementing.** Recording (and merging) this contract records the
Workstream 9 scope and gates only; it authorizes **no** BASE RED, tests, code, question-text change, or implementation.
Prepared under the risk-based execution and review model (PR #220), on authoritative tip `1d4b7da9` (Merge PR #234).
First gate of the Workstream 9 lifecycle (Contract → status canonicalization → BASE RED → implementation → HEAD GREEN →
evidence → independent reviews → owner closure).

## 0. Grounding (committed repository evidence only)
- Remediation plan §5/§15: Workstream 9 = **"Single-Intent Question Design" (P2)**, currently **NOT STARTED**;
  Workstreams 1–8 are closed (WS8 closed via PR #234 as no-valid-RED / expressed-intent objectives deferred to WS9/10/11/14).
- Committed question content is served **verbatim** from `docs/governance/path_n_content_config/electronics_electrical_path_n_questions.json`
  via `engine/path_n_questions.py:get_path_n_question(gap_type, iterations_open)` (index into the per-gap variant list).
- Stage 3 questions are sourced verbatim from `STAGE3_QUESTION_SET.md` and embedded in `engine/progression_loop.py`
  (each annotated with a single "Primary Evidence Target", e.g. PMF-E1).
- No unrecorded session narrative is used. Every multi-intent finding below quotes committed question text.

## 1. Current-state problem statement
Several committed user-facing questions bundle **multiple independent intents** into one prompt, so a single answer can
satisfy one part while leaving another unresolved, and the question text, answer expectation, and evaluation target are
not one-to-one. This is confirmed defect class §3.C-13 "Multi-intent questions". Committed multi-intent evidence
(Path N Stage 2 set, quoted verbatim):
- **MI-1 · N-MC-2:** "What are the main parts of your idea … **and** what does each part do?" — (a) enumerate parts, (b) describe each part's function.
- **MI-2 · N-PF-1:** "What would need to be true for this system to work safely, **and** what information would you need later to confirm it?" — (a) safe-operation conditions, (b) future confirmation information.
- **MI-3 · N-PF-2:** "What do you think would keep the system running, **and** what do you not know yet about that?" — (a) sustaining factors, (b) acknowledged unknowns.
- **MI-4 · N-PF-3:** "Are there real-world conditions … that might stop it from working? **Which ones worry you most?**" — (a) enumerate conditions, (b) rank/prioritise.
- **MI-5 · N-BA-1:** "When should the system work, when should it not work, **and** what situations might confuse it?" — three intents (operate / not-operate / confusion cases).
Borderline (bundled but potentially one atomic answer; flagged, not asserted as defects): N-MC-1 ("notice … and respond"),
N-BA-2 ("your idea responsible for … and … someone/something else's job"), N-BA-3 (react-example and stay-quiet example).
Stage 3 candidates (in the WS8-protected Stage 3 set; noted, not primary WS9 targets): PMF-Q1 ("What is happening … and
why does it matter"), EGA-Q2 ("which ones … to proceed, and which ones represent genuine gaps").

## 2. Exact bounded scope
Workstream 9 is bounded to the **single-intent design of existing user-facing questions**: ensuring each question has one
primary intent, one answer expectation, and one observable completion purpose, by **splitting or re-scoping** multi-intent
questions (content-level). It does **not** change journey ordering (WS8), evaluation logic (WS11), unknown-progression
policy (WS12), guided answers (WS13), or follow-up/completion algorithms (WS14), and does **not** build a registry (WS10).

## 3. Definition of a single-intent question
A question is **single-intent** when it has: one primary user decision or information request; one answer objective; one
observable completion condition; one gap/issue context; no hidden secondary task; no combined "describe, compare, justify,
and measure" bundle unless the combined parts are **inseparable for one atomic answer**; and no requirement for the user
to answer **unrelated** technical dimensions in one response.

## 4. In-scope question types and journey stages
- **Stage 2** Path N approved question content (`electronics_electrical_path_n_questions.json`) for gaps
  MECHANISM_COMPLETENESS / PHYSICAL_FEASIBILITY / BOUNDARY_AMBIGUITY.
- **Stage 3** questions (from `STAGE3_QUESTION_SET.md`) **only** to the extent of single-intent conformance analysis,
  respecting each question's existing Primary Evidence Target; any change to Stage 3 content that WS8 protected requires
  the protected-behavior guard (§6).
- Scope is the **content/intent structure** of these questions, not their ordering, evaluation, or rendering.

## 5. Out-of-scope behavior
Not in scope, and must not be silently absorbed: journey ordering / transitions (**WS8**, closed); a question-intent
registry / taxonomy / identifier system / persistent mapping (**WS10**); scoring, semantic evaluation, or answer-quality
redesign beyond the minimum needed to state the question contract (**WS11**); unknown/incomplete-answer progression policy
(**WS12**); guided technical answer generation / specialist guidance (**WS13**); adaptive follow-up / completion algorithm
(**WS14**); guidance consolidation (**WS15**); final deliverable/E2E (**WS16**); **Structured Technical Guidance** (D13
product implementation — no unresolved-subproblem diagnosis, research-term generation, evidence recommendation,
verification-boundary output, or specialist-category logic); **WS-PFV-001**; **Structured Invention Disclosure / Patent
Export**. Also excluded: anything outside the electronics/electrical MVP scope, and the frozen persistence paths.

## 6. Protected behavior from Workstreams 1–8 (must not regress)
WS1 Evidence Lock baseline (tree `a49a51338aaefd82d0f060308464c90dbe68b14c`); WS2 safety signals
(`engine/safety_signal.py`); WS3 deliverable hygiene; WS4 structured criticality; WS5 unified risk/safety; WS6
requirement landscape (`engine/requirement_landscape.py`); WS7 validation plan (`engine/validation_plan.py`); WS8
deterministic ordering / transition coherence / selection-presentation consistency (its retained observable residue).
The known pre-existing `tests/test_domain_registry.py` baseline (31 failures) is out of scope and must be neither fixed
nor worsened. Splitting a multi-intent question must not alter gap taxonomy, scoring, safety extraction, or the WS8
ordering contract.

## 7. Required user-visible outcomes
- Every in-scope question presents **one** primary intent with one answer expectation and one completion purpose.
- A user answering the single asked intent **completes** that question; no hidden second requirement silently remains.
- No safety, criticality, risk, landscape, validation-plan, or ordering behavior changes in substance.

## 8. Deterministic acceptance criteria
- **AC-1:** Each in-scope committed question maps to **exactly one** primary intent (one answer objective, one completion
  condition, one gap context). Deterministic, checkable against committed/redesigned content.
- **AC-2:** No in-scope question requires **two independently answerable** requests or **two unrelated evidence types**
  for a single completion event.
- **AC-3:** Question text ↔ answer expectation ↔ completion target are **one-to-one** for each in-scope question.
- **AC-4:** The identified committed multi-intent questions (MI-1…MI-5) are demonstrably **non-compliant** until
  corrected; already-single-intent questions (e.g. N-MC-3, N-MC-4, N-PF-4) remain compliant.
- **AC-5:** WS1–8 protected outputs are unchanged in substance for protected fixtures.
- **AC-6:** No out-of-scope artifact (WS10–16, STG, WS-PFV-001, SID) is introduced; the `test_domain_registry.py`
  baseline is unchanged.
- **AC-7:** Language variants (where committed/added) preserve the same primary intent and answer objective (§10).

## 9. Proposed BASE RED test classes (NOT created here)
Proposed for a later, separately authorized BASE RED increment (this contract creates **no** tests; final RED count is
derived from source analysis, not fixed here):
- **R1:** a question with two independently answerable requests is rejected / must be split into atomic questions.
- **R2:** a question must not require two unrelated evidence types for one completion event.
- **R3:** surfaced question, expected answer, and completion target align to one primary intent.
- **R4:** Arabic and English variants preserve the same primary intent and answer objective.
- **R5:** a partial answer does not falsely complete a multi-part question.
- **R6:** the committed multi-intent questions (MI-1…MI-5) remain demonstrably non-compliant until corrected.
**Protected classes:** P1 existing valid single-intent questions; P2 WS1–8 safety/risk/requirement/validation/ordering
behavior; P3 unknown/deferred/provisional/abstention states; P4 persistence/resume behavior; P5 bilingual & RTL behavior;
P6 no WS10–16 capability introduced.

## 10. Arabic/English and RTL requirements
The committed Path N content is currently English-only; no Arabic question variants exist in
`electronics_electrical_path_n_questions.json`. Where bilingual variants exist or are added, each variant must carry the
**same single primary intent and answer objective**, preserve RTL presentation semantics, and keep English digits where
already required in generated output. Workstream 9 adds no translation and no directionality change; it only constrains
intent parity across variants.

## 11. Unknown / deferred / provisional / abstention / partial-answer handling
Single-intent redesign must preserve existing acknowledged-unknown capture (`AcknowledgedUnknown`), deferred/provisional
dispositions, and abstention states. A **partial** answer to a (now single-intent) question must not be treated as full
completion, and splitting a formerly multi-intent question must not convert a previously-captured unknown into a silent
completion. WS9 defines no new unknown-progression policy (that is WS12).

## 12. Persistence and resumed-session boundaries
No persistence/schema change. The frozen persistence worktree and paths remain untouched. Resumed-session behavior must
remain stable: the same committed state yields the same served question deterministically
(`get_path_n_question` indexes by `iterations_open`).

## 13. Safety and criticality preservation
Safety-signal extraction (WS2) and structured criticality (WS4) must be unchanged in substance by any single-intent
redesign. A safety-relevant question must not lose its safety-relevant intent through splitting; safety presentation
integrity (WS5) is protected.

## 14. Evidence and regression requirements
A later evidence increment (separately authorized) will use a dedicated directory
`docs/governance/evidence/workstream9_single_intent_question_design/` with a manifest and validator PASS (mirroring
WS6/WS7). Regression: focused suite GREEN; affected-compatibility GREEN; WS1–8 protected battery GREEN; full suite
unchanged except the known `test_domain_registry.py` baseline. Independent implementation + evidence reviews (PASS)
precede owner closure.

## 15. Explicit non-authorization of implementation
This contract authorizes **none** of: tests; BASE RED; production-code change; question-text change; UI change; a
registry or schema; prompt or AI-logic change; database or persistence change; evaluation-behavior implementation;
adaptive follow-up; Workstream 10-or-later work; Structured Technical Guidance implementation; WS-PFV-001 implementation;
Structured Invention Disclosure / Patent Export implementation. It does not build the Workstream 10 Question Intent
Registry; it may describe a **conceptual** primary intent for contract/testing purposes only, without implementing or
prescribing a registry schema. Each later Workstream 9 gate requires its own separate owner authorization. Phase A branch
remains fixed at `57e2fac8`; PR #167 (`74ea297f…`) / PR #162 (`088ab884…`) untouched; product state
`DEMO_READY_WITH_LIMITATIONS`; MVP electronics/electrical-only; AI Coach (WS17) BLOCKED until Workstreams 1–16 owner-closed.
