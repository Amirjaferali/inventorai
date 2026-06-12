# PHASE 2 AUTHORIZATION — PATH N CONTENT SELECTION
# (Minimal content-selection layer consuming IdeaState.path)

## 1. Status

- PHASE 2 AUTHORIZATION — PATH N CONTENT SELECTION
- AUTHORIZATION DOCUMENT ONLY — no implementation occurs under this
  document until the owner issues the explicit "implement Phase 2"
  instruction after this document is committed
- Defines the exact, bounded implementation scope for Phase 2

## 2. Authority chain

| Commit | Artifact | Role |
|--------|----------|------|
| `1982e2b` | `ACTIVE_EXECUTION_ROADMAP.md` | §7: this draft is the single next authorized step |
| `60c809b` | `DUAL_PATH_PRODUCT_ANCHOR.md` | Product intent; §4 boundary (no orchestration, Stage 4+, Workspace, Mode B) |
| `3c15c32` | Phase 1 implementation closure record | Closure precondition satisfied (anchor §9.1) |
| `aa068fd` | `PATH_N_CURRENT_EXECUTION_ANCHOR.md` | Execution state; §9 sequence |
| `5084110` | Phase 1 implementation | `IdeaState.path` carrier exists |
| `bd1019c` | Integration plan Amendment 1 | §4.5 question-selection plumbing zone (consumed by THIS phase) |
| `2f6720d` | Conditional STOP owner ruling | R-A, R-C, R-D, R-E, R-F |
| `26fa3e1` | Path N content config artifact approval | Approved content source |
| `8ceb5d4` | Path N JSON artifact | THE content (N-MC-1→4, N-PF-1→4, N-BA-1→3) |

## 3. Exact purpose of Phase 2

Make `state.path == "N"` select approved Path N question content,
and nothing else. After Phase 2: Path N-designated sessions receive
N-* questions from the approved artifact; legacy/undesignated
sessions receive byte-identical current behavior. No gate, scoring,
maturity, or transition behavior changes for any session.

## 4. Authorized files (exhaustive)

| File | Permitted change |
|------|------------------|
| `engine/path_n_questions.py` (NEW) | Single-purpose loader: reads the approved JSON artifact read-only; exposes lookup by gap_type + iterations_open; no other behavior. File contract per §5. |
| `engine/progression_loop.py` | Amendment 1 zone ONLY: (a) additive optional `path` parameter on `get_question()` (default preserves current behavior for all existing callers); (b) `run_iteration()` question call sites pass `state.path` and apply the R-E rule (§9). Nothing else in this file. |
| `web/app.py` | EXACTLY ONE LINE in `show_session()`: the existing `get_question(...)` call gains the path argument from the session state. No other change to any function. This is a narrow, explicit exception to the no-existing-body-modification rule, required by ruling R-D (dual call-site consistency). |
| `tests/test_phase2_path_n_selection.py` (NEW) | Phase 2 test suite per §10. |

Any diff outside these four files is a violation and rollback trigger.

## 5. New-file contract (per CLAUDE.md file creation rules)

- Path: `engine/path_n_questions.py`
- Purpose: load and serve approved Path N question content.
- Input contract: gap_type (str), iterations_open (int).
- Output contract: question text (str) or None if the gap_type has
  no Path N mapping (None triggers the §11 STOP for Stage 2 gap
  types — it must not happen for MECHANISM_COMPLETENESS,
  PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY).
- Source: `docs/governance/path_n_content_config/electronics_electrical_path_n_questions.json`
  loaded READ-ONLY from its committed location. Rationale: the
  artifact's content and location are pinned by tests (`806a3c6`)
  and approval (`26fa3e1`); relocation would reopen approval and is
  NOT authorized here.
- Prohibited behaviors: no mutation of the artifact; no fallback to
  Path T content on partial data (fail loudly — no hidden fallback
  logic); no AI calls; no caching semantics beyond load-once
  consistent with the `_REGISTRY` precedent.

## 6. Selection mechanics

- `get_question()` remains the ONE shared selection function
  (ruling R-D). With the additive path parameter:
  - `path == "N"` → resolve from `engine/path_n_questions.py`.
  - any other value or default → existing behavior, unchanged:
    domain layer first, generic `QUESTIONS` fallback.
- Legacy continuity: existing callers that do not pass the
  parameter get the default, which is current behavior —
  byte-identical content for legacy sessions.
- No domain literals, no domain-specific branching, no gate logic
  anywhere in the new code paths (Amendment 1 bounds e–g).

## 7. Dual call-site consistency (ruling R-D)

Both call sites resolve through `get_question()` with the same
inputs including the path from `state`:
- `web/app.py::show_session()` — the one-line change (§4).
- `engine/progression_loop.py::run_iteration()` — call-site changes
  within the Amendment 1 zone.
No site-local path logic anywhere. The §10 consistency test proves
no mixed-path questions.

## 8. Path N content coverage rule

The approved artifact covers MECHANISM_COMPLETENESS (N-MC-1→4),
PHYSICAL_FEASIBILITY (N-PF-1→4), BOUNDARY_AMBIGUITY (N-BA-1→3).
Stage 3 gap types are NOT covered by the artifact; for a Path N
session reaching Stage 3, selection falls through to existing
Stage 3 behavior (generic QUESTIONS). This fallthrough is explicit,
documented, and tested — not hidden.

## 9. AI advisor exclusion (ruling R-E)

For `state.path == "N"`, the `get_ai_question(...) or
get_question(...)` precedence pattern is bypassed: the question is
resolved deterministically from the approved artifact regardless of
`AI_ADVISORY_ENABLED`. Implemented at the `run_iteration()` call
sites within the Amendment 1 zone. A §10 negative test proves an
AI-provided question cannot displace Path N content. Legacy
sessions keep the existing precedence pattern unchanged.

## 10. Tests required before any implementation commit (gate)

New file `tests/test_phase2_path_n_selection.py`, covering:

1. Path N selection: a `path = "N"` session receives only question
   text matching the approved artifact's N-* entries for Stage 2
   gap types, across iterations_open progression.
2. Legacy byte-identity: legacy/undesignated sessions receive
   identical question text to pre-Phase-2 behavior (Path T bank +
   generic fallback untouched).
3. Dual call-site consistency: for the same session state,
   display-time question == iteration-returned question (Path N
   session AND legacy session).
4. AI exclusion: with AI advisory mocked to return text, a Path N
   session's question is unaffected; a legacy session keeps
   existing precedence.
5. Negative control: unknown path values (`""`, `"X"`, default)
   resolve to legacy behavior, never Path N.
6. Disallowed-term scan: questions actually served in a Path N
   session contain no disallowed terms (per `a31010a`/`56343d6`
   term list, N-* lines scope per `68293bd`).
7. Stage 3 fallthrough: documented behavior per §8.
8. Determinism: same idea twice on the Path N route → identical
   question sequence and IdeaState.

Required green gates before commit — exact commands, output pasted
by owner, in order:

    pytest tests/test_phase2_path_n_selection.py -q
    pytest tests/test_phase1_path_designation.py -q
    pytest tests/test_web_app.py -q
    pytest tests/test_wps001_invariants.py tests/test_path_n_content_config_artifact.py tests/test_non_specialist_questioning_policy.py -q

Expected: Phase 2 suite all passed; Phase 1 suite 7 passed;
web suite green; final gate 34 passed, 1 skipped, 1 xfailed.
The strict xfail of `72b5f11` is NOT converted in Phase 2 — its
conversion is a separate, later authorization (plan Phase 5).
Any deviation: STOP, paste output, no commit.

## 11. STOP conditions for Phase 2 implementation

STOP, paste evidence, await ruling if:

1. Selection cannot be achieved without touching anything in
   `progression_loop.py` outside the Amendment 1 zone, or without
   touching `evaluate_transition()`, `assess_response()`,
   `integrate_response()`, or PASS/WARN/BLOCK logic.
2. `show_session()` requires more than the single authorized line.
3. The artifact is missing a question for any Stage 2 gap type
   reached in testing.
4. Legacy byte-identity (test 2) cannot pass without modifying
   forbidden files.
5. Loading the artifact from `docs/governance/` proves technically
   unworkable (would trigger a relocation decision — owner only).
6. Any temptation arises to mutate the artifact, add fallbacks, or
   convert the xfail.

## 12. Rollback rule

- Phase 2 lands as one commit (or code/tests split, owner's choice).
- Rollback = `git revert`: removing the loader and the additive
  parameter restores pre-Phase-2 behavior exactly; no data
  migration. Phase 1 designation remains intact after rollback.

## 13. Explicit non-authorizations

Phase 2 does NOT authorize:
- R2 execution (remains HELD until runtime-integrated Path N
  evidence exists AND a separate R2 authorization is granted —
  Phase 2 implementation alone does not constitute that grant).
- FORM T (remains BLOCKED). S-6 (remains UNCLASSIFIED).
  AA-5 (remains BLOCKED).
- `runtime_integrated = true` — the flag stays `false` through
  Phase 2; flipping it is the plan Phase 4 process (separate
  authorization, JSON metadata update, re-testing, recorded
  re-approval).
- Deterministic gate changes of any kind.
- PASS/WARN/BLOCK changes of any kind.
- Path T / `domain.json` changes — none, unless explicitly
  justified and separately authorized in a future document.
- Full orchestration. Phase 2 is content selection only (product
  anchor `60c809b` §4.7); it must not become implementation
  orchestration.
- Stage 4+ work of any kind.
- Professional Workspace.
- Mode B (prohibited designation per `d3b2349`).
- Conversion of the `72b5f11` strict xfail.
- Artifact relocation or modification.

## 14. Required next owner decisions

1. Whether to commit this Phase 2 authorization.
2. Artifact runtime source location is accepted for Phase 2 only:
   `docs/governance/path_n_content_config/electronics_electrical_path_n_questions.json`.
   Any future relocation requires separate authorization.
3. Whether to then issue the explicit "implement Phase 2"
   instruction — a separate gate after commit.