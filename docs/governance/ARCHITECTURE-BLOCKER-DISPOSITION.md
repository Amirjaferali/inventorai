# ARCHITECTURE-BLOCKER-DISPOSITION.md

**Status:** ACTIVE
**Date:** 2026-05-30
**No code was modified. This artifact is committed as documentation only.**

---

## AUTHORIZATION BOUNDARY

No implementation is authorized as a result of this document.
Resolution of AB-001 or AB-005 requires owner explicit authorization,
evidence-based design proposal, benchmark verification, and committed documentation.

---

## AB-001 SUMMARY

ID: AB-001
Title: _SUBSTANCE_SIGNALS in progression_loop.py rather than domain_rules.py
Location: engine/progression_loop.py lines 146-171

What it is: _SUBSTANCE_SIGNALS governs whether assess_response() classifies
an answer as REASONED. Contains tokens for electronics, mechanical, software,
and medical. Lives in the engine, not the domain layer.

Why it is a blocker: For any domain not in this list, substantive answers may
be classified ASSERTED. Quality classifier is domain-biased even when question
delegation via get_domain_question() is working correctly.

Architectural impact: Violates Architectural Invariant 1 - domain behavior
must live in domain_rules.py only.

Governance impact: Domain pack validation Criterion V-4 may pass
question-selection testing while failing at quality-classification level.

Future path: Owner authorizes proposal, agent proposes migration,
owner reviews, benchmark before and after, commit with rationale.

Current status: OPEN - not authorized for resolution

---

## AB-005 SUMMARY

ID: AB-005
Title: Registry loader inactive - domain_rules.py is runtime source
Location: Architecture split between domain_registry.py, domain_rules.py,
and domains/iot_electronics/domain.json

What it is: domain_registry.py and domain.json exist but domain_rules.py
is the active runtime source. Registry loader is never called.

Evidence from domain.json: Hardcoded content in engine/domain_rules.py
remains the active runtime source until Phase 5 Step 3 registry loader
is implemented.

Why it is a blocker: domain.json packs cannot be used at runtime.
Validating domain.json validates a file that does not run.
Any future domain still requires additions to domain_rules.py.

Architectural impact: Stage 3 Domain Validation cannot be meaningfully
executed until registry loader is active.

Governance impact: Noted in DOMAIN_PACK_GOVERNANCE_STANDARD_v1.md Section 8.

Future path: Stage 2 commit first, owner authorizes Stage 3, activate
registry loader, benchmark verification, owner authorization before any change.

Current status: OPEN - not authorized for resolution

---

## RELATIONSHIP BETWEEN AB-001 AND AB-005

These blockers are independent but related.
AB-005 must be resolved before Stage 3 domain validation is meaningful.
AB-001 must be resolved before quality classification works for non-electronics.

Potential future sequence if Stage 3 is authorized: AB-005 first
(registry activation), then AB-001 (substance signals migration).
This sequence is conditional and not yet approved.

---

## WHAT DOES NOT REQUIRE RESOLUTION BEFORE STAGE 3

Gap taxonomy, maturity gating, IterationLog, IdeaState,
evaluate_transition(), BOUNDARY_AMBIGUITY fallback questions,
get_domain_question() delegation pattern.

---

| Field | Value |
|-------|-------|
| Artifact name | ARCHITECTURE-BLOCKER-DISPOSITION.md |
| Status | ACTIVE |
| Committed | YES - committed 2026-05-30 |
| Related artifacts | ARCHITECTURE-DOMAIN-AGNOSTICISM-REVIEW.md |

Document version: v1 - Date: 2026-05-30
