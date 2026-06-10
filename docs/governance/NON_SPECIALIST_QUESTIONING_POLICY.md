# NON-SPECIALIST QUESTIONING POLICY

## 1. Status

COMMITTED GOVERNANCE POLICY — NOT IMPLEMENTED

Date: 2026-06-10

This policy is created after the product-alignment drift record in commit 10d6876.

Approval of this policy does not authorize code changes, prompt changes, tests, routing changes, FORM T, S-6, AA-5, or R2 execution.

## 2. Problem Statement

R1 exposed a product-alignment risk.

The committed R1 transcript showed that the electronics_electrical flow asked engineering-heavy questions early, including:

- circuit function
- electronic components
- signal or energy transformation
- power source
- voltage/current/frequency requirements
- electrical constraints

Iterations 7 to 9 repeated the same electrical-constraints question while the non-specialist participant was stalled.

This may be unsuitable for the non-specialist guided inventor path.

## 3. Product Principle

InventorAI has two distinct paths.

Path 1: Non-specialist guided inventor path.

The user enters an idea and answers accessible questions about:

- what the idea is
- what problem it solves
- who is affected
- where or when the problem occurs
- what happens if the problem is not solved
- what outcome is desired
- what the rough solution is
- what the user believes may make the solution work
- what the user does not know yet
- what help the user needs from the platform

The platform leads the journey and acts as an orchestration layer toward execution.

The non-specialist user must not be blocked early for lacking engineering knowledge.

Path 2: Specialist / technical path.

Technical users may answer engineering or domain-specific questions about:

- components
- circuits
- voltage/current/frequency
- calculations
- physical constraints
- materials
- manufacturing details
- implementation tradeoffs

These questions belong to the specialist path or later Engineering Translation stages.

## 4. Allowed Question Types for Non-Specialist Path

Early-stage non-specialist questions may address:

- idea description
- problem description
- affected user or beneficiary
- context of use
- current failure or pain point
- desired outcome
- rough mechanism in plain language
- user assumptions in plain language
- known unknowns
- what the user needs help understanding
- evidence the user has observed
- what would make the idea useful or not useful

## 5. Disallowed-as-Gate Question Types

The following must not be used as early participation gates for non-specialist users:

- exact voltage
- exact current
- frequency requirements
- circuit architecture
- component-level selection
- signal transformation details
- quantitative physical constraints
- engineering calculations
- datasheet-level requirements
- manufacturing tolerances

These are not forbidden forever.

They are disallowed as early gates in the non-specialist path.

They remain valid in the specialist path or later Engineering Translation stages.

## 6. Translation / Deferral / Routing Rule

For any engineering-heavy issue encountered in the non-specialist path, the platform must choose one of:

1. Translate into accessible language.
2. Record as a known unknown.
3. Defer to the Engineering Translation stage.
4. Route to the specialist / technical path if the user declares technical competence.
5. Ask what information the user would need instead of asking for the engineering answer.

Bad early non-specialist question:

"Do you know the voltage/current/frequency requirements?"

Better non-specialist version:

"What parts of the system do you think would need power, and what information would you need later to choose the right power source?"

This policy treats "what information would you need?" as the preferred primary strategy for non-specialist users, rather than embedding it as a fallback after an engineering-gated question.

## 7. Stall Handling Rule

If the non-specialist user stalls on an engineering-heavy question:

- do not repeat the same engineering question verbatim
- reframe the question in plain language
- record the missing engineering knowledge as a gap
- ask what the user does know
- ask what support or information would be needed to continue
- do not treat missing engineering knowledge as immediate journey failure

R1 iterations 7 to 9 are the documented counter-example.

## 8. Relationship to Existing Gap Taxonomy

This policy preserves the existing gap taxonomy.

The gap still exists.

Examples:

- PHYSICAL_FEASIBILITY gaps may be recorded
- electrical constraint gaps may be recorded
- MECHANISM_COMPLETENESS gaps may be recorded

What changes is the asking strategy.

The non-specialist path must not require the user to resolve engineering gaps before the platform can continue guiding the journey.

This policy operates in the question layer.

Deterministic gates, maturity transitions, stall detection, and PASS/WARN/BLOCK logic remain unchanged unless separately authorized.

## 9. Enforcement Requirements

This policy must later become enforceable through:

- prompt/question review
- route or mode separation
- prompt guard
- tests that fail if engineering-heavy terms appear too early in the non-specialist path

Terms that should trigger review if used too early include:

- voltage
- current
- frequency
- circuit
- component
- signal transformation
- electrical constraints
- datasheet
- calculation

Term-list matching is a review trigger, not a final verdict.

The enforcement design must distinguish platform-asked questions from user-volunteered vocabulary.

## 10. Governance Effect

Until implementation is separately reviewed and authorized:

- R2 remains HELD
- FORM T remains blocked
- S-6 remains unclassified
- AA-5 remains blocked
- code modification is not authorized
- prompt modification is not authorized
- architecture redesign is not authorized
- tests are not authorized
- prompt guards are not authorized

## 11. Required Next Decision

The owner must decide:

1. Whether to approve this policy as governing the non-specialist path.
2. Whether to turn this policy into tests or prompt guards.
3. Whether R2 should rerun only after the policy is implemented.
4. Whether the current electronics_electrical flow should be treated as specialist-path evidence only.

Policy approval itself does not modify MVP scope. Any later implementation that changes question banks, routing, mode separation, prompt behavior, tests, or runtime behavior requires separate scope review against MVP_SCOPE_FREEZE.md before code or prompt changes.

## 12. Boundary Statement

No code was modified by this policy.

No prompts were modified by this policy.

No FORM T comparison has been performed.

No S-6 classification has been performed.

No AA-5 verdict has been started.

R2 remains HELD.

AA-4 final S-6 classification has NOT been performed.
