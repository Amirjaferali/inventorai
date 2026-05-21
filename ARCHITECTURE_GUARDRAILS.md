# InventorAI — Architecture Guardrails

This document defines permanent architectural constraints.
It is not a roadmap. Future development must respect these guardrails.
Violations require explicit architectural review before proceeding.

## 1. Engine Independence — Core Must Remain Generic

progression_loop.py must not know domain names directly.

FORBIDDEN inside progression_loop.py:
    if domain == "electronics": ...
    elif domain == "mechanical": ...
    elif domain == "medical": ...

This pattern is permanently forbidden.
If it appears in a PR touching progression_loop.py, block and review.

REQUIRED pattern:
    rules = get_active_rules(domain)

## 2. Domain Layer Ownership

Adding a new domain must be done through the domain layer only.
progression_loop.py must NOT be modified when adding a domain.

Current MVP: engine/domain_rules.py (single file — acceptable for MVP)

Preferred future direction:
    domains/
        electronics/
        mechanical/
        medical/
        software/
    registry.py

## 3. Engine Requests Rules — Domain Layer Owns Rules

Allowed inside progression_loop.py:
    rules = get_active_rules(domain)

Stable interface that must be preserved:
    def get_active_rules(domain: str) -> list

Internal implementation may change. Signature must not.

## 4. Architectural Acceptance Rule

If adding a new domain requires modifications to progression_loop.py,
the change must be BLOCKED and reviewed architecturally.

Adding a domain should require changes only in the domain layer.
Any modification to the engine must be justified as a framework-level
change, not a domain-specific change.

This rule applies permanently.

## 5. Multi-Domain Future Support

Architecture must not assume one idea belongs to one domain only.
Current MVP single-domain is acceptable for now.

Future examples must be supportable without engine restructuring:
    idea.domains = ["electronics", "ai"]
    idea.domains = ["robotics", "software"]
    idea.domains = ["medical", "iot"]

## 6. Phase F Warning

Phase F must NOT become a long list of if/elif domain branches.

The goal of Phase F is to PROVE the architecture accepts new domains
without touching core progression logic.

Phase F success criteria:
    - New domain added via domain layer only
    - progression_loop.py diff: ZERO lines changed
    - Full engine test suite passes without modification

If Phase F requires modifying progression_loop.py to support a new domain,
Phase F has FAILED architecturally, even if it works functionally.

## 7. Generic Gap Taxonomy

ALLOWED: PROBLEM_DEFINITION, MECHANISM_COMPLETENESS,
         BOUNDARY_DEFINITION, EVIDENCE_STRENGTH, VALIDATION_STATUS

FORBIDDEN: ELECTRONICS_GAP, MEDICAL_GAP, CHEMICAL_GAP
           Any gap type containing a domain name.

## 8. AI Governance Boundary — Deterministic Gate Ownership

AI MAY: classify, summarize, recommend, explain
AI MAY NOT: decide maturity, close gaps, issue PASS/BLOCK, control state

evaluate_transition(), integrate_response(), assess_response()
must remain pure and deterministic. No AI calls permitted. Ever.

## 9. Classification Independence

infer_domain() signature must remain stable:
    def infer_domain(idea_text: str) -> str | None

Current keyword-based implementation is MVP-only.
Future ML/LLM replacement must not require changes to progression_loop.py.

## 10. Technical Debt Register

| Shortcut                       | Location            | Until   | Replacement                     |
|--------------------------------|---------------------|---------|---------------------------------|
| Keyword domain inference       | domain_rules.py     | Phase F | ML/LLM classifier               |
| Static ELECTRONICS_SIGNALS     | domain_rules.py     | Phase F | Dynamic signal registry         |
| Static _SUBSTANCE_SIGNALS      | progression_loop.py | Phase G | AI-advisory assessment          |
| Single-domain classification   | domain_rules.py     | Phase F | Multi-domain composition        |
| Single-file domain registry    | domain_rules.py     | Phase F | domains/ plugin structure       |

## 11. Phase G Review Requirement

Before Phase G begins, verify:
    - AI boundary (Section 8) enforced in implementation
    - No deterministic gate function calls AI
    - Registry interface (Section 3) stable
    - This document reviewed and updated

## 12. Guardrail Test Plan

TEST 1: progression_loop.py has no domain name string literals in conditionals.
TEST 2: Mock domain added to domain layer only — engine tests pass, loop unchanged.
TEST 3: No gap type constant contains a domain name substring.
TEST 4: No AI calls inside evaluate_transition(), integrate_response(), assess_response().
TEST 5: infer_domain() signature matches (idea_text: str) -> str | None.
TEST 6: After Phase F — progression_loop.py has zero net domain-logic line changes.

---
Document owner: architecture
Review required before: any new domain added, Phase G start.
Violations require explicit architectural review before proceeding.
