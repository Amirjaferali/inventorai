# PATH N RUNTIME INTEGRATION AUTHORIZATION PLAN — AMENDMENT 1
# Narrow admissibility of question-selection plumbing in progression_loop.py

## 1. Status

- AMENDMENT 1 TO `PATH_N_RUNTIME_INTEGRATION_AUTHORIZATION_PLAN.md`
- AMENDMENT ONLY — this document authorizes NO implementation
- Phase 1 remains non-authorizable until this amendment is committed
  AND a separate Phase 1 authorization is granted

## 2. Authority for this amendment

| Commit | Artifact | Role |
|--------|----------|------|
| `2f6720d` | `PHASE_0_CONDITIONAL_STOP_OWNER_RULING.md` | R-C and R-G: narrow plumbing admissible only via formal amendment; STOP resolved only through this amendment |
| `2c0d2a5` | `PHASE_0_PATH_N_RUNTIME_DISCOVERY_REPORT.md` | Evidence basis: no safe zero-engine-change path identified |
| `d2b2a9a` | `PATH_N_RUNTIME_INTEGRATION_AUTHORIZATION_PLAN.md` | The amended document |

Per the "No silent amendment" clause (`2f6720d` §11), this amendment
is the separate committed document that R-C/R-G require.

## 3. Amendment text

### 3.1 — Plan §4, invariant 5

REPLACE:

> `engine/progression_loop.py`: zero net changes. Any discovered
> necessity to modify it is a STOP condition (see §9).

WITH:

> `engine/progression_loop.py`: changes are prohibited EXCEPT
> narrowly authorized question-selection plumbing, defined as:
> passing a session path designation from `IdeaState` into the
> question-selection mechanism (`get_question()` and/or its call
> sites, and/or a shared selection function per ruling R-D).
> Hard bounds on this exception:
> (a) `evaluate_transition()` untouched;
> (b) `assess_response()` untouched;
> (c) `integrate_response()` untouched;
> (d) PASS/WARN/BLOCK logic unchanged in behavior and in code;
> (e) no domain literals;
> (f) no domain-specific branching;
> (g) no gate behavior changes of any kind;
> (h) additive/optional signature changes only — existing callers
>     must work unchanged;
> (i) every change in this zone requires its own implementation
>     authorization and tests per plan §7.
> Any change outside this defined zone remains a STOP condition.

### 3.2 — Plan §9, first STOP condition (consequential)

REPLACE:

> Path N selection cannot be achieved without modifying
> `engine/progression_loop.py`, `evaluate_transition()`,
> `assess_response()`, or `integrate_response()`.

WITH:

> Path N selection cannot be achieved within the amended §4.5
> question-selection plumbing zone — i.e., it would require touching
> `evaluate_transition()`, `assess_response()`,
> `integrate_response()`, PASS/WARN/BLOCK logic, or any
> `progression_loop.py` code outside question selection.

### 3.3 — Plan §10, fourth bullet (consequential)

REPLACE:

> No modification of `domain.json`, `engine/progression_loop.py`,
> or the Path T bank, in any phase, ever, under this plan.

WITH:

> No modification of `domain.json` or the Path T bank, in any phase,
> ever, under this plan. No modification of
> `engine/progression_loop.py` outside the §4.5 question-selection
> plumbing zone; changes inside that zone require their own separate
> implementation authorization.

### 3.4 — No other text of the plan is amended

All other invariants (§4.1–§4.4, §4.6–§4.11), phases, tests,
rollback rules, and boundaries remain in force unchanged.

## 4. What this amendment explicitly preserves (restated, binding)

- `evaluate_transition()` untouched.
- `assess_response()` untouched.
- `integrate_response()` untouched.
- PASS/WARN/BLOCK logic unchanged.
- No domain literals; no domain-specific branching.
- No gate behavior changes.
- No `domain.json` modification.
- Path T technical bank untouched, byte-identical.
- `runtime_integrated` remains `false` (plan §4.7 unchanged).
- Strict xfail `72b5f11` unchanged (plan §4.8 unchanged).
- Session path default = `legacy_undesignated_current_behavior`
  (plan §4.6 unchanged).
- AI advisory must not override Path N content (ruling R-E;
  enforcement enters via plan §7 tests at implementation time).

## 5. What this amendment does NOT do

- Authorizes NO implementation. Not one line of code.
- Does NOT authorize Phase 1. After this amendment is committed,
  Phase 1 still requires its own separate authorization.
- Does NOT modify `engine/progression_loop.py`,
  `engine/idea_state.py`, `web/app.py`, `domain.json`, tests,
  prompts, or any runtime behavior. It amends planning text only.
- Does NOT start R2, FORM T, S-6 classification, or AA-5.

## 6. Governance effect (upon commit)

- Plan §4.5, §9, §10 amended as specified in §3.
- The Phase 0 conditional STOP's blocking effect is lifted ONLY with
  respect to making Phase 1 authorizable; everything else stays
  blocked pending its own authorization.
- R2: remains HELD. FORM T: remains BLOCKED.
- S-6: remains UNCLASSIFIED. AA-5: remains BLOCKED.

## 7. Required next owner decision

1. Whether to authorize Phase 1 (additive `IdeaState.path` field +
   dedicated designation route + zero-behavior-change tests), as a
   separate authorization after this amendment is committed.