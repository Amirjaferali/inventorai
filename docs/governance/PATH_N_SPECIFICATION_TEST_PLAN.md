# PATH N SPECIFICATION TEST PLAN

## 1. Status

COMMITTED PATH N SPECIFICATION TEST PLAN — NO TESTS CREATED

Date: 2026-06-11

This plan defines how to test the committed Path N question content specification as a governance artifact before runtime integration.

No tests are created by this plan.

No implementation is authorized.

## 2. Source Governance

- PATH_N_QUESTION_CONTENT_SPECIFICATION.md — commit e2e6234
- FUNCTIONAL_PATH_N_IMPLEMENTATION_PLAN.md — commit cf63f13
- Characterization tests — commit 72b5f11
- NON_SPECIALIST_QUESTIONING_POLICY.md — commit a31010a
- R-2_R1_PRODUCT_ALIGNMENT_DRIFT_RECORD.md — commit 10d6876

## 3. Test Objective

The tests should validate the Path N specification artifact, not runtime behavior.

They should confirm:

- proposed Path N questions exist in the specification
- disallowed engineering-gated terms are not used as early gates in the proposed Path N question set
- the R1 regression pattern does not recur in the Path N question set
- known-unknown language is present
- no domain file or runtime behavior is touched

## 4. Proposed Test File

Proposed only:

tests/test_path_n_question_content_specification.py

## 5. Proposed Test Categories

### TC-1 Specification file exists and is readable

Load docs/governance/PATH_N_QUESTION_CONTENT_SPECIFICATION.md.

Assert non-empty UTF-8 content.

### TC-2 Path N question IDs exist

Assert the specification contains:

- N-MC-1 through N-MC-4
- N-PF-1 through N-PF-4
- N-BA-1 through N-BA-3

### TC-3 Disallowed early-gate terms do not appear inside proposed question text

Check proposed question text only, not the whole document.

The whole document intentionally mentions disallowed terms in explanatory sections.

### TC-4 Known-unknown capture is present

Confirm the question set includes language such as:

- unsure
- what information would you need
- what do you not know yet
- ask an engineer to check

### TC-5 R1 regression prevention

Confirm the proposed Path N question set does not reproduce the R1 markers:

- electronic circuit achieves
- electronic components
- signal or energy transformation
- voltage/current/frequency
- electrical constraints

### TC-6 No runtime or domain dependency

The test module must not import Flask.

It must not run sessions.

It must not read domain.json.

It must inspect only the specification file.

## 6. Section-Scoped Parsing Rule

The specification document necessarily mentions disallowed terms.

Therefore, tests must parse only the proposed question set.

Preferred approach:

Extract only lines whose IDs match:

N-MC-*
N-PF-*
N-BA-*

Then evaluate only the question text on those lines.

Do not scan the whole markdown file for disallowed terms.

A whole-file scan would false-fail because voltage, current, and similar terms appear in explanatory sections.

## 7. Governance Effect

- tests are not created by this plan
- code changes are not authorized
- prompt changes are not authorized
- question-bank changes are not authorized
- runtime behavior changes are not authorized
- R2 remains HELD
- FORM T remains blocked
- S-6 remains unclassified
- AA-5 remains blocked

## 8. Required Next Owner Decision

The owner must decide:

1. Whether to authorize creation of tests/test_path_n_question_content_specification.py.
2. Whether these tests should run before any domain integration.
3. Whether successful spec tests are required before any runtime implementation.
4. Whether R2 remains held until integrated Path N evidence exists.

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
