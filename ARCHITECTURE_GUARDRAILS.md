# InventorAI — Architecture Guardrails

This document defines permanent architectural constraints.
It is not a roadmap. Future development must respect these guardrails.

## 1. Engine Independence

progression_loop.py must remain domain-agnostic.
No domain-specific branching permitted inside the progression engine.

FORBIDDEN inside progression_loop.py:
    if domain == "electronics": ...
    elif domain == "mechanical": ...

REQUIRED pattern:
    rules = get_active_rules(domain)

## 2. Domain Plug-in Model

New domains added via domain_rules.py only.
progression_loop.py must not be modified when adding a domain.

## 3. Architectural Acceptance Rule

If adding a new domain requires changes to progression_loop.py,
architecture review is mandatory before proceeding.

## 4. Registry-Based Rule Loading

Engine requests rules via get_active_rules(domain).
No domain logic embedded in engine.

Stable interface:
    def get_active_rules(domain: str) -> list

## 5. Generic Gap Taxonomy

ALLOWED: PROBLEM_DEFINITION, MECHANISM_COMPLETENESS,
         BOUNDARY_DEFINITION, EVIDENCE_STRENGTH, VALIDATION_STATUS

FORBIDDEN: ELECTRONICS_GAP, MEDICAL_GAP, CHEMICAL_GAP

## 6. AI Governance Boundary — Deterministic Gate Ownership

AI MAY: classify, summarize, recommend, explain
AI MAY NOT: decide maturity, close gaps, issue PASS/BLOCK, control state

evaluate_transition(), integrate_response(), assess_response()
must remain pure and deterministic. No AI calls permitted inside them.

## 7. Multi-Domain Architecture Readiness

Architecture must not assume single domain per idea.
Future: idea.domains = ["electronics", "ai"]

## 8. Classification Independence

infer_domain() signature must remain stable:
    def infer_domain(idea_text: str) -> str | None

Internal implementation may change. Signature must not.

## 9. Technical Debt Register

| Shortcut | Location | Until | Replacement |
|---|---|---|---|
| Keyword domain inference | domain_rules.py | Phase F | ML/LLM classifier |
| Static ELECTRONICS_SIGNALS | domain_rules.py | Phase F | Dynamic registry |
| Static _SUBSTANCE_SIGNALS | progression_loop.py | Phase G | AI-advisory assessment |
| Single-domain classification | domain_rules.py | Phase F | Multi-domain composition |

## 10. Phase G Review Requirement

Before Phase G begins, verify:
- AI boundary (Section 6) enforced in implementation
- No deterministic gate function calls AI
- Registry interface stable for AI-driven classification

## 11. Guardrail Test Plan

TEST 1: progression_loop.py contains no domain name string literals in conditionals.
TEST 2: Mock domain added to domain_rules.py — engine tests pass, loop unchanged.
TEST 3: No gap type constant contains a domain name.
TEST 4: No AI calls inside evaluate_transition(), integrate_response(), assess_response().
TEST 5: infer_domain() signature matches (idea_text: str) -> str | None.

---
Document owner: architecture
Review required before: any new domain, Phase G start.
