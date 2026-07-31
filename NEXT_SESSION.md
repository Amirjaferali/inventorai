# InventorAI — Next Session Notes

> **STATUS BANNER (added by the Audit-Disposition & Lean-Governance gate):**
> **HISTORICAL — NOT CURRENT EXECUTION AUTHORITY.** These are session-time notes and do not
> govern current work. Resolve current authority from `CLAUDE.md`,
> `docs/governance/CURRENT_PROJECT_STATE.md`, the current anchors, the canonical plan, the
> latest append-only `ACTIVE_EXECUTION_ROADMAP.md` records, and current owner decisions
> (`docs/governance/OWNER_DECISION_REGISTER.md`). Body preserved unchanged below. (See
> stale-document register SD-7.)

## Architecture Status Snapshot
Date: 2026-05-22
Current state: Multi-domain engine with web interface shell.
Core engine stable. Web layer thin. AI advisory layer built but disabled.

---

## Closed Phases

| Phase | Commit   | Achievement                                      |
|-------|----------|--------------------------------------------------|
| E     | ceb9d25  | Quality gate — weak answers blocked              |
| F-A   | 86dcba5  | Mechanical domain — architecture proof           |
| F-B   | 338d85b  | Domain-owned questions via registry              |
| F-C   | 3ad2014  | Medical device — specificity scoring             |
| F-D   | 9d417aa  | Software domain — subset gap taxonomy            |
| G-A   | af02e64  | AI advisory layer — disabled by default          |
| H-A   | b4519d7  | Thin web shell — engine as library               |

---

## Deferred Phases

| Phase | Reason                                  | Blocker                     |
|-------|-----------------------------------------|-----------------------------|
| G-B   | AI activation                           | ANTHROPIC_API_KEY not found |
| H-B   | Web UX improvements                     | Pending discussion          |
| H+    | Image/sketch intake                     | After H stable              |
| I     | Domain Capability Profile               | After multi-domain stable   |

---

## Architectural Invariants (must never change)

1. progression_loop.py must not contain domain-specific branching.
2. Domain behavior lives in domain_rules.py only.
3. AI must not decide maturity, close gaps, or issue PASS/BLOCK.
4. evaluate_transition(), assess_response(), integrate_response() must remain deterministic.
5. Adding a new domain must not require engine modification.
6. Web layer must call engine as library only — no business logic in routes.
7. AI_ADVISORY_ENABLED = False in production and benchmark.
8. Replay benchmark must remain 19/22, variance 0% across all phases.

---

## Evidence Summary

### Replay Benchmark
- Total: 22 | Passed: 19 | Failed: 0 | Skipped: 3
- Variance: 0%
- AI assertion: AI disabled during benchmark — verified

### Engine Integrity
- git diff -- engine/: EMPTY across all phases after F-B framework change
- scoring.py: unchanged since project start
- summary.py: unchanged since project start
- idea_state.py: unchanged since project start

### Domain Layer
- 4 domains active: electronics_electrical, mechanical, medical_device, software
- All added via domain_rules.py only
- Specificity scoring in infer_domain() — MVP keyword-based

### Web Shell (H-A)
- web/app.py calls engine as library only
- No business logic in routes
- No AI dependency
- SESSION_STORE: in-memory, non-production, temporary
- CLI and Web produce identical engine output for same inputs

---

## Current Technical Debt

| Debt                              | Location            | Until   |
|-----------------------------------|---------------------|---------|
| Keyword domain inference          | domain_rules.py     | Phase G+|
| Static _SUBSTANCE_SIGNALS         | progression_loop.py | Phase G |
| QUESTIONS bank in engine          | progression_loop.py | Future  |
| Software gap subset only          | domain_rules.py     | Future  |
| SESSION_STORE non-production      | web/app.py          | Phase H+|
| AI_ADVISORY_ENABLED = False       | ai_advisor.py       | G-B     |

---

## Next Discussion: Phase H-B

Before any H-B implementation, discuss:
1. What is the goal of H-B?
2. What value does it add over H-A?
3. What files would change?
4. Would any engine file be touched?
5. What are the acceptance criteria?

H-B must not modify engine files.
H-B must not activate AI.
H-B must not add authentication or database.
H-B is web layer only.
