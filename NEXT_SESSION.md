# InventorAI — Next Session Notes

## Phase G-A — CLOSED
**AI Advisory Layer (Question Generation Only)**
Commit: af02e64

### What was built:
- engine/ai_advisor.py: all AI logic lives here
- AI_ADVISORY_ENABLED = False by default
- One call site in progression_loop.py only
- Fallback chain: AI -> domain questions -> generic questions
- Benchmark assertion: AI must be disabled during benchmark

### Evidence:
- idea_state.py: UNCHANGED
- scoring.py: UNCHANGED
- summary.py: UNCHANGED
- domain_rules.py: UNCHANGED
- Replay benchmark: 19/22, variance 0%
- AI authority: question generation only — no gates, no scoring, no progression

---

## Phase G-B — DEFERRED
**Reason: ANTHROPIC_API_KEY not found in Codespace environment**

Verified:
    python3 -c "import os; print(os.environ.get(ANTHROPIC_API_KEY))"
    Result: NOT FOUND | length: 0

Decision:
- No API key will be added now
- No secrets or environment changes now
- G-B deferred until API key is available in environment

When G-B resumes:
- No changes to progression_loop.py
- No changes to any engine file except ai_advisor.py
- Tests in tests/ only
- API key read from environment only — never stored in repo
- benchmark must remain: 19/22, variance 0%
- AI_ADVISORY_ENABLED stays False in production and benchmark

---

## AI Governance — Permanent Rule
AI authority in this system = question generation only.

AI MAY: generate contextual question string
AI MAY NOT:
- classify domain
- assess response quality
- evaluate transitions
- close gaps
- issue PASS/BLOCK
- decide maturity level
- control progression state

This rule does not change in G-B or any future phase.

---

## Next: Phase H — Web Interface
Phase H is independent of G-B.
G-B deferred does not block Phase H.

Before Phase H implementation, architecture discussion required:
- What framework? (Flask, FastAPI, other)
- Does web layer touch engine directly or via API?
- How does session state persist across HTTP requests?
- How does image intake (Phase H+) integrate?
- What changes in engine files, if any?

Phase H must not modify:
- progression_loop.py (unless framework-level change)
- scoring.py
- summary.py
- domain_rules.py
- ai_advisor.py

---

## Technical Debt (carried forward)
- _SUBSTANCE_SIGNALS keyword-based — Phase G+ replacement
- Keyword-based domain inference — MVP only
- QUESTIONS bank in progression_loop.py — future refactor
- Software gap taxonomy subset only — future richer taxonomy
- AI_ADVISORY_ENABLED = False — pending G-B when API key available
- Specificity scoring MVP-only — Phase G+ ML/LLM replacement
