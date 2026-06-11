# NON-SPECIALIST PATH SEPARATION DESIGN PLAN

## 1. Status

COMMITTED PATH SEPARATION DESIGN PLAN — NO IMPLEMENTATION AUTHORIZED

Date: 2026-06-10

Drafted under owner authorization: AUTHORIZE MODE SEPARATION DESIGN PLAN ONLY.

## 2. Source Governance

Source records:

- Characterization tests — commit 72b5f11
- NON_SPECIALIST_TEST_DESIGN_PLAN.md — commit 56343d6
- QUESTION_FLOW_DISCOVERY_REPORT.md — commit e1095c6
- NON_SPECIALIST_POLICY_ENFORCEMENT_PLAN.md — commit f271f35
- NON_SPECIALIST_QUESTIONING_POLICY.md — commit a31010a
- R-2_R1_PRODUCT_ALIGNMENT_DRIFT_RECORD.md — commit 10d6876

Baseline fact:

The current runtime has domain routes (/start, /start_ilt002_water_leak, /start_ilt002_combination_lock) but no governed non-specialist vs technical path separation.

## 3. Problem Statement

The current app can fix or infer domain, but it does not know the user path.

As a result, non-specialist participants can receive engineering-heavy domain questions too early, as documented in the R1 evidence and drift record.

The issue is not merely bad wording. It is missing path separation: the platform has one questioning strategy per domain, applied identically to every user regardless of technical competence.

## 4. Design Goals

The design must:

1. Preserve the non-specialist guided inventor path.
2. Preserve technical questioning for appropriate users or later stages.
3. Preserve the existing gap taxonomy unchanged.
4. Avoid changing deterministic gate logic unless separately authorized.
5. Avoid modifying domain question banks until scope review and implementation authorization.
6. Make the future tests from 72b5f11 meaningful by giving them a path target.

## 5. Proposed Path Concepts

### Path N — Non-specialist guided path

For users who do not claim technical competence.

Allowed early question strategy:

- idea
- problem
- beneficiary
- context
- desired outcome
- rough solution
- what the user believes may make it work
- what the user does not know
- what information the user would need

Engineering-heavy questions are translated, deferred, or recorded as known unknowns.

### Path T — Technical questioning context

For users who explicitly declare technical competence or enter a technical workflow.

Engineering-heavy questions may be allowed.

Terminology guard:

Path T is not Mode B / Professional Workspace. It does not authorize a professional workspace, specialist product mode, or Mode B implementation. It only names the current technical questioning context for design clarity.

### Future Engineering Translation Context — future placeholder only

This is a future placeholder concept entirely outside the current MVP.

It is not part of the GD-001 frozen three-stage journey, not an approved stage, and not an extension or modification of current Stage 3.

It is named here solely to clarify where engineering questions would eventually be routed if the owner authorizes such a context in the future.

No structure, content, or timing is defined or implied by this plan.

## 6. Entry Decision

Possible future ways to determine path:

1. Explicit user choice at start.
2. Entry question: guided non-technical path or technical engineering path.
3. Owner/admin configured route.
4. Deferred auto-routing based on answers, only after governance approval.

No option is selected by this plan.

## 7. Question Selection Principle

The same gap can exist in both paths; the question wording differs by path.

The gap taxonomy remains identical. What changes is the asking strategy.

Example:

PHYSICAL_FEASIBILITY exists in both paths.

Path N wording:

"What would need to be true for this system to work safely, and what information would you need later to confirm it?"

Path T wording:

"What voltage/current/frequency constraints must the circuit stay within?"

Documented finding:

The technical-style wording already exists in domains/electronics_electrical/domain.json. Path T does not necessarily require inventing a new technical question bank initially; the current electronics_electrical bank is already closest to technical questioning.

This does not authorize Mode B / Professional Workspace.

The primary future build is Path N's non-specialist-safe path, not the removal of technical questions from the project.

## 8. Relationship to Tests

tests/test_non_specialist_questioning_policy.py currently carries an xfail future enforcement target.

That xfail cannot become a normal passing test until a governed non-specialist path exists.

Path separation provides the target interface for future enforcement tests.

Once Path N exists, the test evaluates Path N's question set.

Path T remains exempt by design.

No test modification is authorized by this plan.

## 9. Files Likely Involved Later — NOT AUTHORIZED

Likely future files:

- web/app.py — only if route/path entry is authorized
- domains/electronics_electrical/domain.json — only if question variants or path metadata are authorized
- engine/progression_loop.py — only if runtime question selection becomes path-aware
- tests/test_non_specialist_questioning_policy.py — only if tests are later updated from xfail to enforced behavior
- possible new helper/config file — only if owner authorizes

No file modification is authorized by this design plan.

## 10. Risks

1. Overengineering path separation too early.
2. Accidentally creating a full professional workspace.
3. Weakening the deterministic engine while wiring path awareness.
4. Treating missing engineering knowledge as success instead of a recorded gap.
5. Breaking WPS001 / replay assumptions.
6. Creating a user-facing path without scope review.
7. Hiding engineering constraints instead of deferring them properly.

## 11. Scope Review Requirement

Any implementation of path separation requires separate scope review against MVP_SCOPE_FREEZE.md.

This draft does not authorize implementation.

Path separation as a user-facing concept is a candidate scope expansion and must be treated as such in that review.

## 12. Governance Effect

- R2 remains HELD
- FORM T remains blocked
- S-6 remains unclassified
- AA-5 remains blocked
- code changes are not authorized
- prompt changes are not authorized
- question-bank changes are not authorized
- tests are not modified
- route/path implementation is not authorized

## 13. Required Next Owner Decision

The owner must decide:

1. Whether to commit this path separation design plan.
2. Whether to authorize a scope review for path separation.
3. Whether non-specialist/technical path separation belongs inside current MVP scope.
4. Whether path should be route-based, user-choice-based, or configuration-based.
5. Whether to keep R2 held until a non-specialist-safe path exists.

Decision 5 linkage:

Decision 5 is not a new decision. It is the same open decision D-B from the drift record 10d6876, continued here.

It asks whether R2 remains held until a non-specialist-safe path exists, or is reclassified as technical-path evidence with permanent interpretive constraints.

Resolving Decision 5 here resolves D-B. They must not be answered differently in two documents.

## 14. Boundary Statement

No code was modified by this plan.

No prompts were modified by this plan.

No domain question bank was modified by this plan.

No routes were modified by this plan.

No engine logic was modified by this plan.

No tests were modified by this plan.

No FORM T comparison has been performed.

No S-6 classification has been performed.

No AA-5 verdict has been started.

R2 remains HELD.

AA-4 final S-6 classification has NOT been performed.
