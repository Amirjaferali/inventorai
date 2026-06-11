# NON-SPECIALIST PATH SEPARATION SCOPE REVIEW

## 1. Status

COMMITTED PATH SEPARATION SCOPE REVIEW — NO IMPLEMENTATION AUTHORIZED

Date: 2026-06-10

Drafted under owner authorization: AUTHORIZE PATH SEPARATION SCOPE REVIEW ONLY.

## 2. Source Governance

Source records:

- NON_SPECIALIST_MODE_SEPARATION_DESIGN_PLAN.md — commit d3b2349
- Characterization tests — commit 72b5f11
- NON_SPECIALIST_TEST_DESIGN_PLAN.md — commit 56343d6
- QUESTION_FLOW_DISCOVERY_REPORT.md — commit e1095c6
- NON_SPECIALIST_QUESTIONING_POLICY.md — commit a31010a
- R-2_R1_PRODUCT_ALIGNMENT_DRIFT_RECORD.md — commit 10d6876
- MVP_SCOPE_FREEZE.md — active freeze authority

## 3. Scope Question

Does minimal path separation belong inside the current MVP as a correction to the non-specialist guided inventor path, or does it constitute scope expansion requiring formal MVP scope revision?

Assessment:

Reading 1 — correction within scope:

The MVP freeze protects structured progression and inventor clarity. R1 evidence showed that the current single-path questioning can block a non-specialist inventor from progressing because the system asks engineering-heavy questions too early. Under this reading, minimal path distinction restores the intended non-specialist guided path.

Reading 2 — expansion requiring revision:

A user-facing path concept, alternate question wording, and path entry mechanism are new product surface. The freeze revision protocol should govern any functional Path N implementation.

Conclusion:

Reading 2 governs for any functional Path N implementation. Functional Path N requires formal MVP scope revision before implementation.

However, a narrow designation-only path interface may be scope-safe if it creates a testable path label without changing runtime behavior, question content, domain banks, routes, prompts, or engine logic.

## 4. Candidate Implementation Options

Scope evaluation only:

1. Route-based Path N / Path T separation.
2. User-choice entry question.
3. Owner/admin configured route.
4. Metadata-based question-bank separation.
5. Runtime path-aware question selection.

No option is selected for implementation by this review.

## 5. Scope Assessment

O-1 route-based distinction:

Borderline scope-safe only if designation-only and not user-facing in a product-expanding way.

O-2 user-choice entry question:

Visible product change. Requires scope review and likely freeze revision.

O-3 owner/admin configured route:

Closest to existing fixed-domain route pattern. Potentially the least disruptive designation-only option.

O-4 metadata-based question-bank separation:

Requires domain/question-bank changes. This is scope expansion and needs MVP scope revision.

O-5 runtime path-aware question selection:

Touches runtime selection and possibly engine logic. Highest risk; requires formal scope review and guardrail review.

## 6. Recommended Scope-Safe Path

The smallest safe next step is designation-only Path N / Path T interface or configuration.

This is scope-safe only if it:

- does not create Professional Workspace
- does not add Engineering Translation stage
- does not change deterministic gate logic
- does not modify the existing technical question bank
- does not create new non-specialist question content yet
- creates only a path distinction needed to make already-committed tests meaningful

Functional Path N cannot be built without non-specialist-safe question content. Authoring that content requires formal MVP scope revision.

Therefore:

Designation-only path interface may proceed to implementation planning.

Functional Path N requires MVP scope revision first.

## 7. Governance Effect

- R2 remains HELD
- FORM T remains blocked
- S-6 remains unclassified
- AA-5 remains blocked
- code changes are not authorized by this review
- prompt changes are not authorized by this review
- question-bank changes are not authorized by this review
- test changes are not authorized by this review
- route/path implementation is not authorized by this review

## 8. Required Next Owner Decision

The owner must decide:

1. Whether to commit this scope review.
2. Whether minimal designation-only Path N / Path T separation is scope-safe.
3. Whether formal MVP scope revision is required for functional Path N.
4. Whether to authorize an implementation plan for designation-only path interface.
5. Whether R2 remains held until Path N exists.

Decision 5 is the same open D-B decision from drift record 10d6876 and design plan d3b2349. It must not be answered differently across documents.

## 9. Boundary Statement

No code was modified by this review.

No prompts were modified by this review.

No domain question bank was modified by this review.

No routes were modified by this review.

No engine logic was modified by this review.

No tests were modified by this review.

No FORM T comparison has been performed.

No S-6 classification has been performed.

No AA-5 verdict has been started.

R2 remains HELD.

AA-4 final S-6 classification has NOT been performed.
