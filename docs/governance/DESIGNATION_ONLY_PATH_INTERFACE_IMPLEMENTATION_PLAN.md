# DESIGNATION-ONLY PATH INTERFACE IMPLEMENTATION PLAN

## 1. Status

COMMITTED IMPLEMENTATION PLAN — NO IMPLEMENTATION AUTHORIZED

Date: 2026-06-10

Drafted under owner authorization: AUTHORIZE DESIGNATION-ONLY PATH INTERFACE IMPLEMENTATION PLAN ONLY.

This plan is the deliverable. Nothing in it is executable until separately authorized.

## 2. Source Governance

- NON_SPECIALIST_PATH_SEPARATION_SCOPE_REVIEW.md — commit 110f4b1
- NON_SPECIALIST_MODE_SEPARATION_DESIGN_PLAN.md — commit d3b2349
- Characterization tests — commit 72b5f11
- NON_SPECIALIST_QUESTIONING_POLICY.md — commit a31010a
- R-2_R1_PRODUCT_ALIGNMENT_DRIFT_RECORD.md — commit 10d6876

This plan follows the scope-safe ceiling from 110f4b1: designation-only, no new content, no functional behavior.

## 3. Purpose

This plan is not Functional Path N.

It does not create non-specialist-safe questions.
It does not change runtime question selection.
It does not alter what any participant experiences in a session.

It only plans a future minimal path designation interface so that tests and later governance can distinguish Path N from Path T as addressable objects.

After designation-only implementation, a session would carry a path label and still ask exactly the same questions it asks today.

## 4. Allowed Future Implementation Shape

The minimal designation-only interface, if later authorized:

| Element | Specification |
|---|---|
| Designation field | A path field in session state or route initialization |
| Explicit values | path_n_non_specialist, path_t_technical |
| Legacy default | legacy_undesignated_current_behavior |
| Question bank | No new bank; no modified bank |
| Engine | No decision change; no path-aware selection |
| Stages | No Stage 4 / Engineering Translation |
| Workspace | No Professional Workspace / Mode B |

Default rule:

Existing behavior remains legacy_undesignated_current_behavior. It must not be automatically labeled Path T. Path N or Path T designation must be explicit through a later owner-authorized route, config, or session initialization decision.

Designation guard:

Designation-only implementation does not retroactively reclassify R1, existing sessions, or current default behavior as Path T evidence. Any evidentiary relabeling of R1/R2 remains governed by D-B.

The implementation surface is limited to one field, three values, and one guard. Nothing reads the field to change behavior.

## 5. Non-Goals

- No Functional Path N
- No new non-specialist question content
- No modification of domains/electronics_electrical/domain.json
- No modification of deterministic gate logic
- No mode auto-classification
- No user-facing professional workspace
- No R2 restart
- No FORM T
- No S-6
- No AA-5

## 6. Files Likely Affected Later — Planning Only

Possible future files, all NOT AUTHORIZED now:

- web/app.py — only if route/session path designation is later authorized
- session state structure — only to carry the path field
- tests/test_non_specialist_questioning_policy.py — only if tests are later updated to target path fields
- small constants/helper file — only if owner authorizes

Explicit exclusions:

- domains/electronics_electrical/domain.json must not be touched for designation-only implementation.
- engine/progression_loop.py must not be touched unless a later owner decision authorizes path-aware question selection.

Path-aware question selection is Functional Path N territory and is outside this plan.

## 7. Test Implication

The current xfail test remains xfail.

Designation-only implementation may allow future tests to ask whether a Path N session exists as a distinct target.

It does not make the non-specialist-safe question test pass, because no Path N question content exists yet.

The strict=True xfail in 72b5f11 is protected by design: designation-only cannot accidentally flip it because the question bank is untouched.

If the xfail ever passes after designation-only implementation, that is a defect signal, not progress.

## 8. Risks

1. False sense of completion.
2. Creating a label without functional safety.
3. Later agents treating designation-only as Functional Path N.
4. Accidentally opening Mode B / Professional Workspace.
5. Touching engine logic too early.
6. Using designation-only as justification to run R2 too soon.
7. Default-value drift.

The legacy default exists precisely so no session is silently classified as Path T.

## 9. Governance Effect

- R2 remains HELD
- FORM T remains blocked
- S-6 remains unclassified
- AA-5 remains blocked
- code changes are not authorized
- prompt changes are not authorized
- question-bank changes are not authorized
- tests are not modified
- implementation is not authorized by this plan

## 10. Required Next Owner Decision

The owner must decide:

1. Whether to commit this implementation plan.
2. Whether to authorize designation-only implementation.
3. Whether to keep Functional Path N blocked pending MVP scope revision.
4. Whether R2 remains held until Functional Path N exists.
5. Whether later tests should target designation-only or wait for Functional Path N.

Decision 4 is the same open decision as D-B from 10d6876, d3b2349, and 110f4b1.

One decision, one answer, recorded once.

## 11. Boundary Statement

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
