# PATH N OPTION A CONTENT CONFIG ARTIFACT PLAN

## 1. Status

COMMITTED OPTION A PATH N CONTENT CONFIG ARTIFACT PLAN — NO IMPLEMENTATION AUTHORIZED

Date: 2026-06-11

This plan specifies the first Option A step from integration plan fa26744: the content/config artifact as a standalone deliverable before any domain-file, runtime, routing, or engine contact.

## 2. Source Governance

- PATH_N_INTEGRATION_PLAN.md — commit fa26744
- PATH_N_CONTENT_APPROVAL_RECORD.md — commit effd040
- tests/test_path_n_question_content_specification.py — commit 221d848
- PATH_N_QUESTION_CONTENT_SPECIFICATION.md — commit e2e6234
- FUNCTIONAL_PATH_N_IMPLEMENTATION_PLAN.md — commit cf63f13

## 3. Objective

Approved Path N content should be represented as a separate content/config artifact before runtime integration.

The artifact is independent from:

- domains/electronics_electrical/domain.json
- web/app.py
- engine/progression_loop.py
- runtime session flow

Nothing reads this artifact at runtime.

Its existence changes no behavior.

It is approved content in machine-readable form, staged for a future separately-authorized integration step.

## 4. Proposed Artifact

Proposed location:

docs/governance/path_n_content_config/electronics_electrical_path_n_questions.json

Location rationale:

The artifact remains under docs/governance and outside domains, so no registry loader, test, or runtime path should accidentally discover it.

Proposed structure:

- metadata
- gaps
- question_id
- text

Metadata should include:

- path: Path N
- domain: electronics_electrical
- status: approved_governance_content_not_runtime_integrated
- source_spec: e2e6234
- approval_record: effd040
- runtime_integrated: false

The artifact should contain the approved eleven questions:

- N-MC-1 through N-MC-4
- N-PF-1 through N-PF-4
- N-BA-1 through N-BA-3

## 5. Representation Rules

The artifact must:

- preserve approved question text exactly
- preserve question IDs exactly
- separate gap types clearly
- avoid engineering-gated terms in Path N question text
- avoid runtime hooks
- avoid domain bank mutation
- avoid prompt mutation

JSON must preserve the committed specification text as UTF-8.

Any divergence from approved question text reopens approval and requires re-testing and recorded re-approval.

## 6. Test Strategy After Artifact Creation

Future tests, separately authorized, should verify:

1. Artifact exists and parses as JSON.
2. All eleven IDs exist.
3. Question text matches approved specification exactly.
4. No disallowed early-gate terms appear.
5. metadata.runtime_integrated is false.
6. domain.json remains untouched.
7. Path T technical bank remains untouched.

## 7. Governance Effect

- code changes are not authorized
- prompt changes are not authorized
- domain bank changes are not authorized
- runtime integration is not authorized
- tests are not created by this plan
- R2 remains HELD
- FORM T remains blocked
- S-6 remains unclassified
- AA-5 remains blocked

## 8. Required Next Owner Decision

The owner must decide:

1. Whether to authorize creation of the separate Path N content/config artifact.
2. Whether the artifact should be JSON, Markdown, or YAML.
3. Whether tests against the artifact should be created immediately after artifact commit.
4. Whether R2 remains held until runtime-integrated Path N evidence exists.

Recommendation:

Use JSON.

Reason:

JSON mirrors question/config structure, is easy to test mechanically, and avoids introducing YAML parser dependency.

## 9. Boundary Statement

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
