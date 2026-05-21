# InventorAI — Next Session Notes

## Last Completed Phase
**Phase G-A — AI Advisory Layer (Question Generation Only)**
Commit: `af02e64`

## Files Changed in G-A

### New files:
- engine/ai_advisor.py — AI advisory layer (all AI logic lives here)
- scripts/run_replay_benchmark.py — benchmark utility (was untracked, now committed)

### Modified files:
- engine/progression_loop.py — one call site only (question retrieval)

### Unchanged files (confirmed zero diff):
- engine/idea_state.py — UNCHANGED
- engine/scoring.py — UNCHANGED
- engine/summary.py — UNCHANGED
- engine/domain_rules.py — UNCHANGED
- engine/normalize_output.py — UNCHANGED

## scripts/run_replay_benchmark.py — Purpose Clarification

This file existed before G-A but was untracked in git.
It was committed in G-A because we added one assertion to it:

    from engine.ai_advisor import AI_ADVISORY_ENABLED
    assert not AI_ADVISORY_ENABLED, "AI must be disabled during benchmark run"

Purpose of the file:
- Benchmark utility / verification runner
- Validates deterministic extraction boundary only
- NOT part of the decision engine
- NOT part of AI advisory layer
- Does not contain progression logic, scoring, or gate decisions

## AI Authority — G-A Scope

AI MAY (in G-A):
- Generate one contextual question string

AI MAY NOT (permanently):
- Decide maturity level
- Close gaps
- Issue PASS / BLOCK
- Control progression state
- Modify scoring
- Touch gate decisions

AI_ADVISORY_ENABLED = False by default.
System works fully without AI. Fallback chain:
    get_ai_question() -> None
        -> get_question(domain, gap_type, iterations_open)  [domain layer]
            -> QUESTIONS[gap_type]  [generic fallback]

## Benchmark Determinism

Replay benchmark: 19/22 PASS | Failed: 0 | Variance: 0%
AI assertion verified: AI_ADVISORY_ENABLED = False during benchmark.
Benchmark is unaffected by AI advisory layer.

## Context Dict (no state changes)

_ai_context built from existing fields only:
    {
        domain: state.domain,          # existing field
        gap_type: gap_type,            # local variable
        idea_summary: getattr(state, idea_summary, None),  # safe fallback
        last_response: response[:200], # run_iteration() parameter
        iteration: state.iteration,    # existing field
    }

No new fields added to IdeaState.
No migration required.
No serialization changes.

## Next Phase: G-B (when ready)
Options for G-B:
- Enable AI_ADVISORY_ENABLED and test with real API call
- Add AI-enhanced domain classification (advisory only)
- Add AI response quality advisory (no gate authority)

Must discuss before implementing G-B.
AI boundary (ARCHITECTURE_GUARDRAILS.md Section 6) must be reviewed first.

## Technical Debt (carried forward)
- _SUBSTANCE_SIGNALS keyword-based — Phase G replacement needed
- Keyword-based domain inference — MVP only
- QUESTIONS bank still in progression_loop.py — future refactor
- Software gap taxonomy is subset only — future richer taxonomy
- AI_ADVISORY_ENABLED = False — needs controlled test environment for G-B
