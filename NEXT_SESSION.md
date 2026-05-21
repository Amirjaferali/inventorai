# InventorAI — Next Session Notes

## Last Completed Phase
**Phase F-D — Software Domain**
Commit: `9d417aa`

## Files Changed
- engine/domain_rules.py — CHANGED (software domain added)
- engine/progression_loop.py — UNCHANGED / zero diff
- engine/scoring.py — UNCHANGED / zero diff
- engine/summary.py — UNCHANGED / zero diff

## Software Domain Evidence
Software examples 4/4 PASS:
- Algorithm for real-time data compression -> software PASS
- Mobile app for tracking medication schedules -> software PASS
- API gateway with rate limiting logic -> software PASS
- Web platform for project management -> software PASS

Negative examples (no false positives):
- HR recruitment platform -> None PASS
- Marketing campaign tool -> None PASS
- Restaurant menu idea -> None PASS

All existing domains unaffected:
- Electronics 2/2 PASS
- Mechanical 1/1 PASS
- Medical 2/2 PASS

## Replay Benchmark
Total: 22 | Passed: 19 | Failed: 0 | Skipped: 3 | Variance: 0%

## Gap Taxonomy Used for Software (MVP subset)
INCLUDED:
- MECHANISM_COMPLETENESS (interpreted as: software logic/workflow/algorithm)
- BOUNDARY_AMBIGUITY (scope and what the system does NOT do)

EXCLUDED:
- PHYSICAL_FEASIBILITY — assumes physical constraints, not applicable to software

This is an MVP interpretation. Future richer taxonomy requires framework review.

## Architectural Note
Phase F-D proved that a non-physical invention domain (software) was added
without modifying the core progression engine.

This confirms the framework engine hypothesis:
progression_loop.py does not need to know domain details.
Domain behavior — signals, questions, rules, gap subsets — lives entirely
in the domain layer (domain_rules.py).

Four structurally different domains now operate through the same engine:
- electronics_electrical (physical, electronic)
- mechanical (physical, motion-based)
- medical_device (biological + physical + regulatory context)
- software (non-physical, logic-based)

All added via domain_rules.py only. Engine untouched across all four.

## Phase F — Complete Summary

| Sub-phase | Achievement                          | Engine changed |
|-----------|--------------------------------------|----------------|
| F-A       | Mechanical domain — architecture proof | No            |
| F-B       | Domain-owned questions via registry  | Framework only |
| F-C       | Medical device + specificity scoring | No             |
| F-D       | Software + subset gap taxonomy       | No             |

## Next: Phase G — Architecture Discussion Required

Before implementation, Phase G needs architectural clarity:

GOAL:
Phase G introduces AI-advisory capabilities.
AI may advise, classify, summarize, recommend.
AI may NOT decide maturity, close gaps, issue PASS/BLOCK.

EXPECTED FILES TO CHANGE:
- engine/progression_loop.py — possible advisory integration point
- engine/domain_rules.py — possible AI-enhanced classification
- New file: engine/ai_advisor.py or similar boundary layer

FILES THAT MUST NOT CHANGE BEHAVIOR:
- evaluate_transition() — must remain deterministic
- integrate_response() — must remain deterministic
- assess_response() — must remain deterministic

RISKS:
- AI boundary violation: AI leaking into gate decisions
- Latency: AI calls slowing progression loop
- Determinism: AI responses introducing variance in benchmarks
- Scope creep: Phase G expanding beyond advisory role

MUST DISCUSS BEFORE PHASE G:
1. What exactly does AI advise on?
2. Where in the flow does AI advisory fit?
3. How do we prevent AI from touching gate logic?
4. How do we test AI advisory without breaking deterministic benchmarks?

## Technical Debt (carried forward)
- _SUBSTANCE_SIGNALS keyword-based — Phase G replacement needed
- Keyword-based domain inference — MVP only (Phase G+ ML/LLM)
- QUESTIONS bank still in progression_loop.py — future refactor
- Specificity scoring is MVP-only — Phase G+ replacement
- Software gap taxonomy is subset only — future richer taxonomy
- Medical domain: no regulatory/compliance/safety scope — MVP limit
