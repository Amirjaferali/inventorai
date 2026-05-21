# InventorAI — Next Session Notes

## Last Completed Phase
**Phase F-C — Medical Device Domain (Scalability Proof)**
Commit: `3ad2014`

## Goal
Add a structurally different third domain to prove the architecture
scales beyond electronics and mechanical without engine modification.

## Domain Added
medical_device — implemented in engine/domain_rules.py only.

## Implementation Details
- MEDICAL_SIGNALS added to domain_rules.py
- MEDICAL_QUESTIONS added to domain_rules.py
- get_active_rules() extended with medical_device branch
- _DOMAIN_QUESTIONS registry updated with medical_device questions
- infer_domain() refactored to specificity scoring:
    scores counted per domain, highest wins
    tie-breaker: medical_device > electronics_electrical > mechanical

## Evidence
- Medical examples: 4/4 PASS
- Electronics examples: 3/3 PASS
- Mechanical examples: 2/2 PASS
- Negative examples: 4/4 PASS
- progression_loop.py: UNCHANGED — zero diff
- scoring.py: UNCHANGED — zero diff
- summary.py: UNCHANGED — zero diff
- Replay benchmark: 19/22, 0% variance
- Files changed: engine/domain_rules.py only

## Architecture Issue Discovered and Resolved
Domain conflict: "Non-invasive glucose monitoring sensor" was classified
as electronics_electrical because "sensor" matched first.

Root cause: first-match ordering gave electronics priority over medical.
Resolution: specificity scoring — domain with most matched signals wins.
This is domain layer logic only — engine was not touched.

Technical debt noted: keyword-based scoring is MVP-only.
Future replacement: ML/LLM classifier (Phase G+).

## Conclusion
Three structurally different domains — electronics, mechanical, and
medical device — now work through the same domain-layer architecture
without modifying the core engine.

This confirms progression_loop.py is functioning as a framework engine,
not a domain-specific engine.

The architecture guardrail (Section 4 — Architectural Acceptance Rule)
has been validated across three independent domain additions.

## Next Phase
**Phase F-D — Software Domain**
Goal: prove architecture handles non-physical invention domain.
Key question: do generic gap types (MECHANISM_COMPLETENESS etc.)
apply meaningfully to software inventions?
This may require architectural discussion before implementation.

## Technical Debt (carried forward)
- _SUBSTANCE_SIGNALS keyword-based — Phase G replacement needed
- Keyword-based domain inference — MVP only
- QUESTIONS bank still in progression_loop.py — future refactor
- Specificity scoring is MVP-only — Phase G+ ML/LLM replacement
- Medical domain: no regulatory/compliance/safety scope — intentional MVP limit
