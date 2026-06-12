# PHASE 1 AUTHORIZATION — PATH DESIGNATION FIELD AND ROUTE
# (Designation-only; no content selection)

## 1. Status

- PHASE 1 AUTHORIZATION — PATH DESIGNATION FIELD AND ROUTE
- Defines the exact, bounded implementation scope for Phase 1
- Implementation begins ONLY after this authorization is committed
  and the owner issues the explicit "implement Phase 1" instruction

## 2. Authority chain

| Commit | Artifact | Role |
|--------|----------|------|
| `bd1019c` | Plan Amendment 1 | §4.5 plumbing zone defined; Phase 1 made eligible |
| `2f6720d` | Conditional STOP owner ruling | R-A (carrier), R-B (IdeaState.path admissible), R-F (I-A′ direction) |
| `2c0d2a5` | Phase 0 discovery report | Evidence basis |
| `d2b2a9a` | Integration plan (as amended by `bd1019c`) | Phase definitions, §7 test targets |
| `4f0ce81` | Designation-only path interface plan | Default value rule |

## 3. Phase 1 scope — what it IS

Exactly two deliverables:

**D1 — Additive `IdeaState.path` field**
- File: `engine/idea_state.py`
- One new field on `IdeaState`:
  `path: str = "legacy_undesignated_current_behavior"`
- No other change to the class. No behavior reads this field
  anywhere in Phase 1.

**D2 — Dedicated designation-only session creation route**
- File: `web/app.py`
- Route name (owner-specified, fixed):
  `/start_ilt002_combination_lock_path_n`
- Scope rationale: Phase 1 stays bounded to the ILT-002 /
  combination-lock evidence path and must not imply general Path N
  availability across domains or routes.
- The route does exactly what `start_ilt002_combination_lock()`
  does (same fixed domain, same idea intake, same SESSION_STORE
  entry shape), plus sets `state.path = "N"` at session creation.
  No other logic.
- Route modification boundary: No existing route function body may
  be modified. Phase 1 may add one new dedicated route only.
  Existing routes `start()`, `start_ilt002_water_leak()`,
  `start_ilt002_combination_lock()`, `show_session()`, and
  `submit_answer()` must preserve current behavior.

Explicit consequence (must be understood before authorizing):
in Phase 1, a `path = "N"` session still receives legacy question
content. The designation is carried, not consumed. Content
selection is Phase 2. Phase 1 implements no loader and no shared
selection function.

## 4. Authorized files (exhaustive)

| File | Permitted change |
|------|------------------|
| `engine/idea_state.py` | D1 only: one additive field with the specified default |
| `web/app.py` | D2 only: one new dedicated route `/start_ilt002_combination_lock_path_n`; no existing route function body modified |
| `tests/test_phase1_path_designation.py` (new) | Phase 1 test suite per §6 |

No other file may change. Any diff outside these three is a
violation and a rollback trigger.

## 5. Forbidden files and functions (exhaustive restatement)

- `engine/progression_loop.py` — NOT touched in Phase 1. The
  Amendment 1 plumbing zone exists but is consumed by Phase 2,
  not Phase 1.
- `evaluate_transition()`, `assess_response()`,
  `integrate_response()` — untouched (frozen gates).
- PASS/WARN/BLOCK logic — unchanged.
- `engine/domain_rules.py`, `engine/domain_registry.py` — untouched.
- `domains/electronics_electrical/domain.json` (Path T) — untouched,
  byte-identical.
- Path N JSON artifact (`8ceb5d4`) — untouched; `runtime_integrated`
  stays `false`.
- `tests/test_non_specialist_questioning_policy.py` — xfail stays
  xfail.
- All existing tests — unmodified.
- No prompts, no AI advisor changes, no SESSION_STORE schema changes
  beyond what `state` already carries.
- No Path N content loader. No shared selection function. Both are
  Phase 2.

## 6. Tests required before commit (gate)

New file `tests/test_phase1_path_designation.py`, covering:

1. Default proof: `IdeaState()` has
   `path == "legacy_undesignated_current_behavior"`.
2. Zero-behavior-change proof: a full legacy session driven through
   `run_iteration()` produces identical results (questions,
   transitions, maturity, gaps) with the field present.
3. Content identity proof (Phase 1 designation-only rule):
   For the same idea, same fixed/inferred domain, same gap_type,
   and same iterations_open, the Path N-designated session receives
   the same question text as the corresponding legacy session
   during Phase 1.
4. Route designation proof: `/start_ilt002_combination_lock_path_n`
   creates a session whose `state.path == "N"`.
5. Existing-routes regression: `start()`, `start_ilt002_water_leak()`,
   and `start_ilt002_combination_lock()` sessions carry the default
   path value.
6. Serialization/equality safety: the additive field does not break
   determinism ("same idea twice = identical IdeaState").

Required green gates before commit — these exact commands, output
pasted by owner, in this order:

    pytest tests/test_phase1_path_designation.py -q
    pytest tests/test_web_app.py -q
    pytest tests/test_wps001_invariants.py tests/test_path_n_content_config_artifact.py tests/test_non_specialist_questioning_policy.py -q

Expected: Phase 1 suite all passed; web app suite green;
WPS001 green unmodified; artifact suite 10 passed; policy suite
4 passed + 1 xfailed (unchanged). Any deviation: STOP, paste
output, no commit.

## 7. Rollback rule

- Phase 1 lands as ONE commit (or two: code + tests, owner's choice
  at implementation time).
- Rollback = `git revert` of the Phase 1 commit(s). Additive-only
  changes guarantee no data migration and no follow-up edits needed.
- If any non-authorized file appears in `git status` during
  implementation: discard, report, do not commit.

## 8. STOP conditions for Phase 1 implementation

STOP, paste evidence, and await ruling if:

1. The additive field breaks any existing test (suggests hidden
   equality/serialization coupling not visible in Phase 0).
2. The new route cannot set `state.path` without touching any
   existing function body.
3. The content identity proof (§6.3) cannot be made to pass
   without modifying anything outside the authorized files.
4. Any temptation arises to "pre-wire" content selection — that is
   Phase 2; doing it now is a violation.

## 9. Explicit confirmations

- Phase 1 does NOT implement Path N content selection. No loader,
  no shared selection function.
- Phase 1 does NOT set `runtime_integrated = true`. The artifact
  metadata is untouched; any future flag change follows the plan
  Phase 4 process (separate authorization, re-testing, recorded
  re-approval).
- Phase 1 does NOT make Path N runtime-complete. After Phase 1,
  Path N sessions exist as designated sessions only and receive
  legacy content. Runtime completeness requires Phase 2 (loader +
  shared selection) and Phase 3 (runtime test suite) at minimum.
- No `domain.json` modification. No Path T modification.
- No deterministic gate changes. No PASS/WARN/BLOCK changes.
- Phase 1 does NOT authorize R2. R2 remains HELD until
  runtime-integrated Path N evidence exists (D-B, `ccd1ecd` §6.1).
- FORM T remains BLOCKED. S-6 remains UNCLASSIFIED.
  AA-5 remains BLOCKED.

## 10. Required next owner decisions

1. Whether D1+D2 land as one commit or code/tests split.
2. Whether to issue the explicit "implement Phase 1" instruction
   after this authorization is committed.