# PATH N INTEGRATION PLAN

## 1. Status

COMMITTED PATH N INTEGRATION PLAN — NO IMPLEMENTATION AUTHORIZED

Date: 2026-06-11

This plan defines how approved Path N content may later enter the project.

It does not implement anything.

## 2. Source Governance

- PATH_N_CONTENT_APPROVAL_RECORD.md — commit effd040
- tests/test_path_n_question_content_specification.py — commit 221d848
- PATH_N_QUESTION_CONTENT_SPECIFICATION.md — commit e2e6234
- FUNCTIONAL_PATH_N_IMPLEMENTATION_PLAN.md — commit cf63f13
- MVP_SCOPE_FREEZE_AMENDMENT_FUNCTIONAL_PATH_N.md — commit cdcd079
- MVP_SCOPE_REVISION_DECISION_RECORD.md — commit ccd1ecd
- DESIGNATION_ONLY_PATH_INTERFACE_IMPLEMENTATION_PLAN.md — commit 4f0ce81

## 3. Integration Objective

Define the safest future path for integrating approved Path N content into the app.

Functional Path N must become available as a non-specialist-safe questioning path while preserving:

- existing gap taxonomy
- deterministic gates
- Stage 1-3 boundary
- Path T technical bank
- R2 held status until verified evidence exists

## 4. Candidate Integration Options

Option A — Content-file-first integration.

Create a separate Path N question content file or config. Leave the existing technical domain bank untouched.

Option B — Add Path N variants inside domains/electronics_electrical/domain.json.

This is riskier because it edits the existing domain bank.

Option C — Designation-only path field plus separate Path N content.

This combines the earlier designation-only interface with separate Path N content, but should happen only after Option A is proven.

Option D — Runtime path-aware question selection.

This is highest-risk because it may touch runtime question-selection logic or engine/progression_loop.py.

## 5. Recommended Approach

Start with Option A.

Create a separate Path N content/config artifact first.

Reasons:

- avoids modifying the existing Path T technical bank
- keeps technical evidence interpretable
- allows content tests before runtime integration
- avoids engine changes
- avoids broad domain.json restructuring
- preserves rollback clarity

After tests and review, decide whether to connect the separate Path N content through route, config, or session path designation.

A-then-C as two separately-authorized steps is preferred over bundling both together.

## 6. Implementation Boundaries

Allowed later only if separately authorized:

- adding a separate Path N question content file or config
- adding tests against that file or config
- adding minimal routing/config/session path selection
- integrating Path N into session flow after tests

Not allowed by this plan:

- editing domain.json
- editing web/app.py
- editing engine/progression_loop.py
- changing prompts
- changing deterministic gate rules
- running R2
- FORM T
- S-6 classification
- AA-5

## 7. Test Strategy

Future test gates:

1. Current spec tests remain passing.
2. New integration-content tests verify approved Path N content is represented exactly.
3. No disallowed early-gate terms appear in Path N question content.
4. Existing Path T technical questions remain available.
5. Runtime tests only after integration authorization.
6. The existing 72b5f11 xfail must not be converted until Path N is integrated and verified.

## 8. R2 / AA-4 Implications

- R2 remains HELD
- FORM T remains blocked
- S-6 remains unclassified
- AA-5 remains blocked
- this integration plan alone does not unblock R2
- R2 may restart only after Path N is integrated, tested, and verified to produce non-specialist-safe evidence

The chain remains:

content approved -> integration plan -> integration authorization -> implementation -> verification -> R2 authorization

## 9. Governance Effect

- code changes are not authorized
- prompt changes are not authorized
- question-bank changes are not authorized
- test changes are not authorized
- runtime integration is not authorized
- R2 remains HELD
- FORM T remains blocked
- S-6 remains unclassified
- AA-5 remains blocked

## 10. Required Next Owner Decision

The owner must decide:

1. Whether to authorize Option A as the first integration step.
2. Whether a separate Path N content/config file should be created before touching domain files.
3. Whether tests should be created before any runtime wiring.
4. Whether R2 remains held until integrated Path N evidence exists.

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
