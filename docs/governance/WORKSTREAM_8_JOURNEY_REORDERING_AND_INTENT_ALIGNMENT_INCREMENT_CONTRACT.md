# Workstream 8 — Journey Reordering and Intent Alignment: Increment Contract

**Status:** INCREMENT CONTRACT — **docs-only, non-implementing.** Recording (and merging) this contract records the
Workstream 8 scope and gates only; it authorizes **no** BASE RED, tests, code, or implementation. Prepared under the
risk-based execution and review model (PR #220), on authoritative tip `c47b98ea` (Merge PR #229). This is the first gate
of the Workstream 8 lifecycle (Contract → status canonicalization → BASE RED → implementation → HEAD GREEN → evidence →
independent reviews → owner closure).

## 0. Grounding (committed repository evidence only)
- Remediation plan `docs/governance/DELIVERABLE_STABILIZATION_REMEDIATION_PLAN.md` §5/§15: Workstream 8 = **"Journey
  Reordering and Intent Alignment" (P2)**, **NOT STARTED**; Workstreams 1–7 are **CLOSED / CANONICAL**.
- The journey is stage-ordered with a fixed gap-priority sequence: `engine/progression_loop.py`
  (`GAP_PRIORITY`, `STAGE3_GAP_PRIORITY`, `active_gap_priority()`, `current_stage` transitions 2→3), and approved
  question content served by `engine/path_n_questions.py` from
  `docs/governance/path_n_content_config/electronics_electrical_path_n_questions.json` (READ-ONLY config).
- No unrecorded session narrative is used. Where this contract asserts a problem, it references the ordering mechanism in
  the files above; it does **not** invent defects or assert fixes.

## 1. Current user-journey ordering and the specific intent-alignment problems
**Current ordering (as committed):** the progression loop advances the inventor through **Stage 2 gaps** in the fixed
`GAP_PRIORITY` order, then, once the required Stage 2 gaps are CLOSED, transitions to `current_stage = 3` and serves
**Stage 3 gaps** in `STAGE3_GAP_PRIORITY` order. Within a stage, the next question is the highest-priority OPEN/PARTIAL
gap; Path N supplies the approved question text for Stage 2 gaps, with Stage 3 gaps using their own question set.

**Intent-alignment problems in scope (P2 defect class):**
- **P8-1 Ordering vs. intent:** the fixed gap-priority sequence can present questions in an order that does not match the
  inventor's current intent or the information they have already volunteered, producing a journey that feels
  mis-sequenced relative to what the user is trying to express.
- **P8-2 Transition legibility:** the Stage 2→Stage 3 transition is driven by internal gap state; the *intent* of each
  stage and of the transition is not always made legible to the user in the presentation order.
- **P8-3 Presentation ordering:** the order in which prompts/sections are surfaced to the user may not reflect the
  priority the user's stated intent implies, even when the underlying gap set is correct.

**Explicitly:** identifying these ordering/intent-alignment problems does **not** authorize changing question *content*,
evaluation logic, or gap taxonomy (those are Workstreams 9–15 — see §4).

## 2. Exact bounded scope of Workstream 8
Workstream 8 is bounded to **the ordering and intent-alignment of the existing journey**: the *sequence* in which
existing stages, existing questions, existing transitions, and existing presentation elements are surfaced to the
inventor, and the *legibility of intent* of that sequence. It **reorders and aligns**; it does **not** add, remove,
reword, re-evaluate, or re-taxonomize questions or gaps.

## 3. In-scope journey stages, questions, transitions, and presentation ordering
- **Stages:** the existing Stage 2 and Stage 3 progression (`engine/progression_loop.py`) — their *ordering* and the
  *intent legibility* of the 2→3 transition only.
- **Questions:** the *ordering* in which existing approved questions are presented (Path N Stage 2 set; existing Stage 3
  set) — **not** their wording or content.
- **Transitions:** the *sequencing and intent-signalling* of existing stage/gap transitions — **not** the conditions
  that define a gap as OPEN/PARTIAL/CLOSED.
- **Presentation ordering:** the *order* in which existing prompts/sections are surfaced — **not** their content,
  styling beyond ordering, or evaluation.

## 4. Out-of-scope (must not be silently absorbed)
This contract does **not** cover, and Workstream 8 work must not absorb:
- **Workstream 9 — Single-Intent Question Design** (question *design*/content);
- **Workstream 10 — Question Intent Registry** (a registry of question intents);
- **Workstream 11 — Question-Aware Evaluation** (evaluation logic);
- **Workstream 12 — Controlled Unknown Progression** (unknown-handling progression);
- **Workstream 13 — Guided Answer Support** (answer assistance);
- **Workstream 14 — Adaptive Follow-Up and Completion Logic** (adaptive follow-ups/completion);
- **Workstream 15 — Guidance Consolidation** (guidance consolidation);
- **Workstream 16 — Final Deliverable Completion** (final deliverable/E2E validation);
- **Structured Technical Guidance** (D13 product implementation);
- **WS-PFV-001** (Prototype Feasibility and Validation);
- **Structured Invention Disclosure or Patent Export** implementation.
It also excludes anything outside the electronics/electrical MVP scope, and the frozen persistence paths.

## 5. Protected behavior from Workstreams 1–7 (must not regress)
- **WS1** Evidence Lock baseline (canonical evidence tree `a49a51338aaefd82d0f060308464c90dbe68b14c`) — immutable.
- **WS2** Safety Signal Stabilization — inventor-stated safety signals, benign-failover zero-signal, harmful-continuation
  detection (`engine/safety_signal.py`) preserved.
- **WS3** Deliverable Hygiene — preserved.
- **WS4** Structured Criticality Capture — criticality capture/dispositions preserved.
- **WS5** Unified Risk and Safety Presentation — unified risk/safety presentation preserved.
- **WS6** Requirement Landscape Synthesis — landscape synthesis preserved (`engine/requirement_landscape.py`).
- **WS7** Actionable Validation Plan — validation-plan output preserved (`engine/validation_plan.py`).
Reordering must change **sequence/intent legibility only**, never the substance, scoring, safety, or deliverable content
these workstreams established. The known pre-existing `tests/test_domain_registry.py` baseline (31 failures) is **not**
in scope and must be neither fixed nor worsened.

## 6. Required user-visible outcomes
- The journey presents existing stages/questions/transitions in an order that **matches the inventor's expressed
  intent** and the information already provided, without changing question content.
- Each stage and the Stage 2→3 transition **communicates its intent** legibly in presentation order.
- No safety, criticality, risk, landscape, or validation-plan output is altered in substance by the reordering.

## 7. Deterministic acceptance criteria
- **AC-1:** For a fixed inventor input, the reordered journey yields the **same set** of stages/questions/gaps as the
  committed baseline (no additions/removals) — only their **order** and intent-signalling differ. (Set-equality,
  deterministic.)
- **AC-2:** The Stage 2→Stage 3 transition fires under the **same gap-state conditions** as the committed baseline
  (`progression_loop.py`), with no change to gap OPEN/PARTIAL/CLOSED semantics.
- **AC-3:** All WS1–WS7 protected outputs (safety signals, criticality, unified risk/safety, landscape, validation plan)
  are **byte-for-byte unchanged** in substance for the protected fixtures.
- **AC-4:** Reordering is **deterministic** — identical input yields identical order.
- **AC-5:** No out-of-scope artifact (WS9–16, STG, WS-PFV-001, SID) is introduced.
- **AC-6:** The known `tests/test_domain_registry.py` baseline is unchanged (still exactly its pre-existing failures).

## 8. Proposed BASE RED test classes (NOT created here)
Proposed for a **later, separately authorized** BASE RED increment (this contract creates **no** tests):
- **RED-8-Ordering:** asserts the target intent-aligned order for representative inventor inputs (fails on the current
  fixed order).
- **RED-8-SetEquality:** asserts stage/question/gap **set-equality** with baseline (guards AC-1).
- **RED-8-Transition:** asserts the 2→3 transition conditions are unchanged (guards AC-2).
- **RED-8-Protected:** asserts WS1–7 protected outputs unchanged under reordering (guards AC-3).
- **RED-8-Determinism:** asserts identical input → identical order (guards AC-4).

## 9. Evidence and regression requirements
- A dedicated evidence directory `docs/governance/evidence/workstream8_journey_reordering/` (created only in the later
  evidence increment), with a manifest and validator PASS, mirroring WS6/WS7 evidence practice.
- Focused suite GREEN; affected-compatibility suite GREEN; WS1–7 protected battery GREEN; full suite unchanged except the
  known `tests/test_domain_registry.py` baseline.
- Independent implementation review and independent evidence review, both PASS, before owner closure.

## 10. Arabic/English and RTL preservation
Where the journey surfaces bilingual content (e.g. Arabic fields such as `power_observations_ar`), reordering must
**preserve** Arabic/English content and **RTL** presentation semantics unchanged; only sequence/intent-legibility may
change. English digits are preserved where already required in generated output. No translation, rewording, or
directionality change is in scope.

## 11. Safety, uncertainty, persistence, and deliverable-integrity boundaries
- **Safety:** WS2/WS5 safety and risk signals must not be reordered in a way that suppresses, delays past decision
  points, or de-emphasizes a safety signal; safety presentation integrity is protected.
- **Uncertainty:** existing uncertainty/abstention and criticality states (WS4) are preserved and not masked by
  reordering.
- **Persistence:** the frozen persistence worktree and paths remain **untouched**; no persistence/schema change.
- **Deliverable integrity:** WS3/WS6/WS7 deliverable content is unchanged in substance.

## 12. Explicit non-authorization of implementation
This contract authorizes **none** of: BASE RED creation; UI changes; schema changes; prompt or AI-logic changes;
database or persistence changes; tests; code or implementation; integration; Workstream 9 or later work; Structured
Technical Guidance implementation; WS-PFV-001 implementation; Structured Invention Disclosure or Patent Export
implementation. Each subsequent Workstream 8 gate (BASE RED, implementation, evidence, reviews, closure) requires its own
separate owner authorization.

## 13. Locks and non-interference
Phase A branch `research/d13-tkp-pkg-001-phase-a-read-only-analysis` remains fixed at
`57e2fac837f333224b2f985be285fe9e0a9f6243`. PR #167 (`74ea297f…`) and PR #162 (`088ab884…`) remain OPEN/DRAFT, outside
scope, and untouched. No product / code / test / schema / prompt / database / UI / persistence / research / TKP file is
changed by this contract. No `.bundle` is part of it. Official product state remains `DEMO_READY_WITH_LIMITATIONS`; MVP
scope remains electronics/electrical-only; the AI Coach (WS17) remains BLOCKED until Workstreams 1–16 are owner-closed.
