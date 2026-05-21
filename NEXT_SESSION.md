# InventorAI — Next Session Notes

## Last Completed Phase
**Phase F-A — Mechanical Domain (Architecture Proof)**
Commit: `86dcba5`

## Goal
Add exactly one new domain as architecture proof.
Prove that a new domain can be added without touching the core progression engine.

## Result
Mechanical domain added in domain layer only.
progression_loop.py: UNCHANGED — zero diff confirmed.

## Evidence
- Mechanical examples: 4/4 PASS
- Electronics examples: 3/3 PASS
- Negative examples: 4/4 PASS
- Replay benchmark: 19/22, 0% variance
- Files changed: engine/domain_rules.py only
- git diff -- engine/progression_loop.py: empty

## Guardrail Confirmed
New domain added without touching core progression engine.
Architecture guardrail (Section 4 — Architectural Acceptance Rule) verified in practice.

## Phase F-B Warning
Phase F-B must NOT introduce domain-specific branches inside progression_loop.py.

If mechanical-specific questions are added, they must come from the domain layer
or registry, not from hardcoded engine logic.

Forbidden in progression_loop.py:
    if domain == "mechanical":
        questions = MECHANICAL_QUESTIONS
    elif domain == "electronics_electrical":
        questions = ELECTRONICS_QUESTIONS

Required: questions fetched from domain layer via registry interface.

## Next Phase
**Phase F-B — Domain-Specific Questions via Domain Layer**
Goal: mechanical-specific questions served from domain_rules.py or registry.
progression_loop.py must remain unchanged.
Success criterion: engine fetches questions generically — domain layer owns them.

## Technical Debt (carried forward)
- _SUBSTANCE_SIGNALS is keyword-based — acceptable for MVP only.
- Phase G should replace/supplement with AI-advisory assessment.
- Deterministic gate ownership must remain outside AI.
- Keyword-based domain inference is MVP-only (Phase G+ replacement).
