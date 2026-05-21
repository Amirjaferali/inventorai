# InventorAI — Next Session Notes

## Last Completed Phase
**Phase F-B — Domain-Owned Questions via Registry**
Commit: `338d85b`

## Goal
Move question ownership from the progression engine to the domain layer.
Prove that domain-specific questions can be served without engine branching.

## Result
Mechanical-specific questions now live in domain_rules.py.
progression_loop.py change: framework-level delegation only.
No if domain == ... branching inside progression engine.

## Engine Change (framework-level only)
- get_question() now accepts domain parameter
- Delegates to get_domain_question() in domain layer
- Falls back to generic QUESTIONS if domain returns None
- Call site updated: get_question(state.domain, gap_type, iterations_open)
- Zero domain-specific logic added to engine

## Evidence
- Mechanical question retrieval: PASS
- Electronics fallback: PASS
- Unknown domain fallback: PASS
- Replay benchmark: 19/22, 0% variance
- git diff progression_loop.py: 3 deletions, framework lines only

## Guardrail Preserved
Engine requests questions. Domain layer owns questions.
Architecture guardrail Section 2 and Section 3 confirmed in practice.

## Phase F-C Warning
Phase F-C must prove scalability with a third domain.
Goal: prove the system is not designed only around mechanical.

Phase F-C success criteria:
- Third domain added via domain layer only
- progression_loop.py diff: zero lines changed
- Domain questions served via existing registry interface
- Replay benchmark remains 19/22, 0% variance

If F-C requires any engine change, it must be framework-level
and requires explicit architecture review before proceeding.

## Next Phase
**Phase F-C — Third Domain (Scalability Proof)**
Recommended: software or chemical domain
Goal: prove architecture scales to N domains without engine modification.

## Technical Debt (carried forward)
- _SUBSTANCE_SIGNALS is keyword-based — acceptable for MVP only.
- Phase G should replace/supplement with AI-advisory assessment.
- Deterministic gate ownership must remain outside AI.
- Keyword-based domain inference is MVP-only (Phase G+ replacement).
- QUESTIONS bank still lives in progression_loop.py — future refactor
  should move it to domain layer or generic registry.
