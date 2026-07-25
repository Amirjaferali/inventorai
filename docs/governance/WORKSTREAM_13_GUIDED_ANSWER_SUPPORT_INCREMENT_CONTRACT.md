# Workstream 13 — Guided Answer Support — Increment Contract (Fresh)

> Documentation-only governance draft. It defines the proposed increment-contract
> boundary for a **future** Workstream 13. **Creating or merging this contract
> does not start WS13** and does not authorize BASE RED, GREEN, implementation,
> status canonicalization beyond the existing canonicalization, closure, or any
> later Workstream or Capability. Every later gate is separately owner-gated.

---

## 1. Authoritative base and evidence lock

| Item | Value |
|---|---|
| Repository | `Amirjaferali/inventorai` |
| Authoritative branch | `feature/atomic-json-session-persistence` |
| Authoritative base (this contract) | `8f08fbe0f2649b10f90545814bc02fe67fae714e` |
| Base subject | `Merge pull request #274 from Amirjaferali/docs/workstream-13-owner-decisions-status-canonicalization` |
| Base parents | `26b39e7f49b702030882feb50a5ba457558254cc` · `95276917878877570bc6eb44b98aa9d479512a73` |
| Base tree | `a33c9419143a9d623162e66b3cbde65cb838cfc6` |

**Mandatory inputs (verified present at the base):**
1. The accepted **WS13 Evidence Lock and Fresh Source Review** (read-only, on tip `8184c7e`).
2. The merged **Owner Decisions OD-1 … OD-14** in
   `docs/governance/WORKSTREAM_13_GUIDED_ANSWER_SUPPORT_OWNER_DECISIONS.md`.
3. The canonical WS13 status recorded by PR #274:
   `WS13 EVIDENCE LOCK AND FRESH SOURCE REVIEW ACCEPTED — OWNER DECISIONS MERGED
   AND POST-MERGE VERIFIED — INCREMENT CONTRACT NOT STARTED — WS13 NOT STARTED —
   BASE RED AND IMPLEMENTATION NOT AUTHORIZED`.
4. The current production and test behavior at the authoritative base (§2–§3).

This contract is re-derived from current repository truth at the base; it copies
no contract from memory, conversation, or an earlier branch.

---

## 2. Fresh source inventory (current verified behavior)

**WS13 engine module — ABSENT (protected).** `engine.guided_answer_support`
does not exist (`import` raises `ModuleNotFoundError`).

**Existing display-layer WS13-like seams** (deterministic, display-only,
content-free; wired in `web/app.py:28–32`, rendered `:579–618`):

| Seam | Public entry | Behavior | Language |
|---|---|---|---|
| `web/answer_coauthoring_prompts.py` | `get_answer_coauthoring_prompts(gap_type)` (`:109`) | Category-level "what you could include in your answer" prompts; never authors/rewrites/completes/grades the answer | **English-only** |
| `web/scaffolding_guidance.py` | `get_scaffolding_guidance(last_result, gap_type=None)` (`:196`) | Names the KIND of missing detail after a WARN insufficiency | **English-only** |
| `web/uncertainty_guidance.py` | `get_uncertainty_guidance(text)` (`:174`), `is_uncertainty_text(text)` (`:144`) | Supportive prompts on explicit uncertainty | **Bilingual (EN + AR)** |
| `web/clarification_labels.py` | `get_clarification(gap_type)` (`:171`) | Plain-language explanation of the current question | **English-only** |
| `web/result_feedback.py` | `get_result_feedback(last_result)` (`:86`) | Plain-language result feedback | **English-only** |

**Engine seams WS13 must observe but not disturb:**
- Question serving: `engine/path_n_questions.py::get_served_question` (`:70`),
  `ServedQuestion` (`:55`); `engine/progression_loop.py::get_question` (`:213`).
- Answer assessment / integration: `assess_response` (`:615`),
  `integrate_response` (`:690`, returns `PASS/WARN`, maps tier→`Gap.status`).
- Append-only ledger: `IdeaState.record_interaction` (`idea_state.py:313`), six
  `INTERACTION_DISPOSITIONS`.
- WS12 observation-only unknown handling:
  `engine/controlled_unknown_progression.py` (`:140`/`:176`).
- WS10 registry (`question_intent_registry.py:184`/`:377`) and WS11 evaluation
  (`question_aware_evaluation.py:95`).

**Repository-supported EN/AR coverage finding:** only
`web/uncertainty_guidance.py` is bilingual; the four other WS13-like seams are
English-only. Under OD-11 this is a **committed-coverage gap to report**, not a
license to substitute Arabic content.

---

## 3. Existing display-layer seams — protected and prohibited surfaces

**Protected surfaces (WS13 must not change behavior):**
- `assess_response`, `integrate_response`, `engine/scoring.py`,
  `evaluate_transition`, `Gap.status`, `maturity_level` — no assessment,
  scoring, progression, gap-status, maturity, completion, transition, or
  follow-up-selection effect.
- The six `INTERACTION_DISPOSITIONS`; `resolves_gap` stays `False`.
- WS9 single-intent question content; WS10 registry; WS11 evaluation
  (observation-only); WS12 `controlled_unknown_progression` (observation-only).
- Absence guards: `test_PROTECTED_no_workstream_13_to_14_capability_introduced`
  (`tests/test_workstream_9_single_intent_question_design.py:301`, asserting
  `engine.guided_answer_support` (WS13) and `engine.adaptive_follow_up` (WS14)
  absent) and the re-assertion in
  `tests/test_workstream_12_controlled_unknown_progression_base_red.py:462`.

**Prohibited surfaces (WS13 must never introduce):**
- Any `engine.guided_answer_support` module (OD-2/OD-3).
- Any answer generation/rewriting/completion, or submit/persist without explicit
  user confirmation (OD-5).
- Any second independent request, question split, or new iteration (OD-6).
- Any D13 technical content — research/measurement/test plan, document list,
  risk analysis, specialist category (OD-7).
- Any WS12 unknown mutation (OD-8), WS14 follow-up/completion (OD-9), or WS15
  cross-module consolidation (OD-10).

---

## 4. Ratified Owner Decisions OD-1 … OD-14 (binding invariants)

The merged Owner Decisions (`WORKSTREAM_13_GUIDED_ANSWER_SUPPORT_OWNER_DECISIONS.md`)
are binding invariants for this contract and any later gate. In brief:
OD-1 govern-not-absent; OD-2 web/display-layer only, no engine module; OD-3
absence guard preserved; OD-4 read-only inputs (served question,
`question_id`/`design_gap_id`, `gap_type`, `last_result`, explicit uncertainty)
with no influence on assessment/scoring/progression/gap/maturity/completion/
follow-up; OD-5 help-not-author, explicit confirm before submit/persist; OD-6
single-intent preserved; OD-7 D13 boundary; OD-8 WS12 boundary; OD-9 WS14
boundary; OD-10 WS15 boundary; OD-11 EN/AR parity where committed, missing
Arabic reported as a gap; OD-12 deterministic provenance; OD-13 defect-driven
minimal increment; OD-14 governed no-valid-RED closure path. This contract does
not restate them normatively beyond this reference; the Owner Decisions document
remains the source of record.

---

## 5. Proposed deterministic contract boundary

WS13 v1 is a **deterministic, display-only, content-free governance envelope**
over the existing web-layer guided-answer support (§2). It:
- reads ONLY OD-4 inputs, at render time, and is pure/deterministic (no engine
  call, AI/LLM/generative call, network, persistence, or hidden state);
- helps the user formulate **their own** answer via prompts, sentence starters,
  bounded examples, and categories of useful information;
- carries deterministic provenance traceable to the current `gap_type`,
  `ServedQuestion`, uncertainty state, or prior WARN `last_result` (OD-12);
- changes no engine outcome and introduces no engine module (OD-2/OD-4).

Any implementation increment under this boundary must be justified by a **proven
observable defect** (OD-13); absent one, WS13 closes via the no-valid-RED path
(§11).

---

## 6. In-scope behavior

- Bounded, deterministic, display-only guided-answer/scaffolding/uncertainty/
  clarification support derived from OD-4 inputs.
- Fixing a **proven observable defect** in that existing display-layer behavior
  (e.g., an incorrect/missing deterministic mapping, a provenance break, or a
  committed EN/AR parity defect surfaced under OD-11), with a minimal change to
  the relevant `web/` module(s) only.
- Reporting committed-coverage gaps (e.g., English-only seams) as gaps.

## 6a. Out-of-scope behavior

Answer generation/rewriting/completion; any change to assessment, scoring,
progression, gap status, maturity, completion, transition, or follow-up
selection; new questions/splits/iterations (WS9/WS14); adaptive follow-up or
completion logic (WS14); cross-module guidance consolidation (WS15); D13
technical content; WS12 unknown mutation; any `engine.guided_answer_support`
module; persistence/schema/export; Patent Export, WS-PFV-001, CAP-12/13/14;
WS16/WS17; adding Arabic content by silent substitution.

---

## 7. Observable acceptance criteria

A future WS13 increment is acceptable only if, deterministically and
observably at the display layer:
1. Guidance is a pure function of OD-4 inputs (identical inputs → identical
   output); no engine/AI/network/persistence call.
2. No engine outcome changes: `assess_response`, `integrate_response`, scoring,
   `evaluate_transition`, gap status, maturity, dispositions are byte-for-byte
   unchanged for the same inputs (protected regression, §12).
3. The guidance never contains an invented project fact, a purported final
   factual answer, a silent rewrite, a completion mark, or an auto-submit/persist
   without explicit user confirmation.
4. Single-intent is preserved (no second request / split / new iteration).
5. Provenance is visible or deterministically traceable (OD-12).
6. `engine.guided_answer_support` and `engine.adaptive_follow_up` remain absent
   (absence guards green).
7. Where both language surfaces are committed, EN/AR parity holds; any missing
   Arabic is reported as a gap, not substituted (OD-11).

---

## 8. Valid BASE RED seams

A later, separately-authorized BASE RED may encode ONLY display-layer,
deterministic failing tests that target a **proven observable defect**, e.g.:
- **VR-1** A deterministic mapping defect in a `web/` guidance entry point
  (`get_answer_coauthoring_prompts` / `get_scaffolding_guidance` /
  `get_uncertainty_guidance` / `get_clarification` / `get_result_feedback`) —
  wrong/missing bounded output for a specific committed `gap_type` / `last_result`
  / uncertainty input.
- **VR-2** A provenance-traceability defect (guidance not deterministically
  traceable to its OD-4 input).
- **VR-3** A committed EN/AR parity defect where BOTH surfaces already exist for
  a seam (today only `uncertainty_guidance` is bilingual — a parity RED is valid
  only where committed Arabic exists; English-only seams yield a reported gap,
  not a fabricated parity RED).
Each RED test must import only stdlib + existing modules, collect cleanly, and
fail solely because of the targeted display-layer defect.

## 9. Invalid / prohibited RED seams

- Any test requiring `engine.guided_answer_support` (would breach OD-2/OD-3).
- Any test asserting a change to assessment/scoring/progression/gap/maturity/
  transition/follow-up (breaches OD-4/OD-9).
- Any test of answer generation/rewriting/completion/auto-submit (breaches OD-5).
- Any test of D13 technical content (OD-7), WS12 mutation (OD-8), or WS15
  consolidation (OD-10).
- Any parity RED fabricated from absent committed Arabic content (OD-11) — this
  is a reported gap, never a RED.

---

## 10. Protected regression set

Any WS13 gate must keep these green (or preserve their established intentional
state exactly):
- Absence guards: `test_workstream_9_single_intent_question_design.py`
  (`:301`) and `test_workstream_12_controlled_unknown_progression_base_red.py`
  (`:462`).
- Existing display-layer tests: `test_guided_answer_coauthoring_increment_1.py`,
  `test_more_detail_needed_scaffolding.py`, `test_guided_uncertainty_support.py`,
  `test_increment_1b_clarification_routing.py`,
  `test_phase_8a_section4_clarification.py`, `test_layer1_feedback_wording.py`,
  `test_plain_language_result_feedback.py`, `test_advisory_panel_precedence.py`.
- The WS9/Path-N protected regression and the WS10/WS11/WS12 suites.
- The known `tests/test_domain_registry.py` baseline (31 failures) — neither
  fixed nor worsened.

## 11. No-valid-RED decision procedure (OD-14)

If fresh contract-time analysis finds **no proven observable failing WS13
behavior**, WS13 closes via the governed no-valid-RED path:
1. Produce a durable evidence package demonstrating the search for an observable
   defect across the five display-layer seams (inputs exercised, outputs
   verified, provenance checked, committed EN/AR parity checked).
2. Explicitly record that no valid RED seam exists at the authoritative base and
   that creating code would violate OD-13 (existing functionality is not a
   reason to create code).
3. Obtain **independent evidence review and explicit owner acceptance**.
4. Only then record a WS13 closure as "no-valid-RED — closed without
   implementation" via a separate owner-authorized status canonicalization.
No BASE RED, GREEN, or implementation is created on this path.

## 12. EN/AR verification requirements

- For every seam that commits BOTH languages (today: `uncertainty_guidance.py`),
  EN and AR outputs must be behaviorally at parity (same triggering, same
  bounded structure) and verified as such.
- For English-only seams (`answer_coauthoring_prompts`, `scaffolding_guidance`,
  `clarification_labels`, `result_feedback`), the absence of Arabic is a
  **reported committed-coverage gap** (OD-11); it must not be counted as parity
  and must not be silently filled.

## 13. Risks, assumptions, and unresolved repository-supported gaps

- **R-1 (overlap with WS15).** The five display-layer seams are exactly the
  fragmented guidance WS15 would later consolidate; WS13 must fix defects
  in-place without consolidating (OD-10).
- **R-2 (EN/AR gap).** Four of five seams are English-only; whether closing that
  gap is WS13 scope or a separate localization gate is an unresolved
  owner-supported gap (see UG-1).
- **R-3 (no-valid-RED likelihood).** The existing behavior is already governed
  and tested; a genuine observable defect may not exist, making §11 the likely
  path — this must be proven, not assumed.
- **A-1.** Guidance remains display-only and deterministic; no engine/AI/network
  dependency is introduced.
- **Unresolved repository-supported gaps (surfaced, not decided):**
  - **UG-1** Is closing the English-only EN/AR coverage gap in scope for WS13, or
    a separate localization workstream? (Ties to OD-11/R-2.)
  - **UG-2** If independent analysis finds no observable defect, is the
    no-valid-RED closure (§11) the intended WS13 outcome, or does the owner want
    a specific defect-hunt scope defined first?
  - **UG-3** Confirmation of the exact protected display-layer test set that must
    remain green before any WS13 RED.

---

## 14. Non-authorization statement

**Creating this contract does not start Workstream 13.** WS13 remains **NOT
STARTED**. It does not authorize BASE RED, GREEN, implementation, status
canonicalization beyond the existing canonicalization, or closure, and it
activates no later Workstream or Capability. `engine.guided_answer_support`
remains absent and the WS13/WS14 absence guards remain unchanged. WS14, WS15,
WS16, WS17, D13 (Structured Technical Guidance), Patent Export, and WS-PFV-001
remain inactive, blocked, separately gated, or unauthorized; CAP-12, CAP-13, and
CAP-14 remain `RECORDED — NOT AUTHORIZED FOR IMPLEMENTATION`. The AI Coach
(WS17) remains BLOCKED until Workstreams 1–16 are owner-closed. Each later WS13
gate requires a separate explicit owner authorization.
