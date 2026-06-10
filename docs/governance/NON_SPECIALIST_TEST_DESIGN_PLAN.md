# NON-SPECIALIST TEST DESIGN PLAN

## 1. Status

COMMITTED TEST DESIGN PLAN — NO TESTS CREATED

No implementation authorized.

Date: 2026-06-10

This plan was created under owner authorization: AUTHORIZE TEST DESIGN PLAN ONLY.

## 2. Source Governance

Source records:

- QUESTION_FLOW_DISCOVERY_REPORT.md — commit e1095c6
- NON_SPECIALIST_POLICY_ENFORCEMENT_PLAN.md — commit f271f35
- NON_SPECIALIST_QUESTIONING_POLICY.md — commit a31010a
- R-2_R1_PRODUCT_ALIGNMENT_DRIFT_RECORD.md — commit 10d6876

Discovery baseline:

The question flow discovery found that R1 questions come from:

domains/electronics_electrical/domain.json

and that no governed non-specialist vs specialist mode separation currently exists.

## 3. Test Objective

The tests should eventually prevent early engineering-gated platform questions in the non-specialist path.

They must not ban engineering terms globally.

They must preserve engineering-heavy questioning for owner-authorized specialist or Engineering Translation contexts.

Because no mode separation exists today, non-specialist path tests cannot meaningfully pass against the current runtime. Test design must anticipate the mode concept without presuming its implementation shape.

## 4. Proposed Test Categories

### TC-1 Question inventory test

Reads platform-askable questions from domain files.

Confirms questions can be enumerated.

This establishes the testable surface.

### TC-2 Non-specialist early-gate policy test

Fails if early non-specialist platform questions include engineering-gated terms.

Depends on:

- owner-defined early-stage threshold
- existence of a governed mode/path concept

### TC-3 Attribution-aware vocabulary test

Ensures user-volunteered engineering terms do not fail the test.

Only platform-asked question text is evaluated.

User response text is excluded from term matching.

### TC-4 Specialist / Engineering Translation allowance test

Engineering-gated questions are allowed only in owner-authorized specialist or Engineering Translation contexts.

This proves the tests encode path policy, not a blanket term ban.

### TC-5 R1 regression test

Uses the R1 question sequence from transcript commit 072e5c0 as the canonical regression example of what must not recur in the non-specialist path.

R1 regression indicators:

- circuit function
- components
- signal or energy transformation
- voltage/current/frequency
- repeated electrical constraints

### TC-6 Stall repetition test design

Not implemented.

Design placeholder only.

Flags that repeated identical engineering-gated questions after user stall should be reviewed.

Must not assume exact reframe-after-3-stalls behavior until deeper stall-logic discovery is separately authorized.

## 5. Candidate Disallowed Early-Gate Terms

Candidate review-trigger terms:

- voltage
- current
- frequency
- circuit
- component
- signal transformation
- electrical constraints
- datasheet
- calculation
- manufacturing tolerance

These are review triggers, not automatic semantic violations.

Final term list, matching rules, word-boundary behavior, case handling, phrase matching, and whitelist exceptions require separate implementation authorization.

## 6. Early-Stage Definition

No final numeric threshold is selected by this plan.

"Early" must be owner-defined before implementation.

Options:

- O-1: first N iterations
- O-2: before MECHANISM_COMPLETENESS closes
- O-3: before Level 1 / Stage 2 completion
- O-4: before Engineering Translation stage

No option is selected by this plan.

## 7. Files Likely Involved Later — NOT AUTHORIZED

Likely future files:

- domains/electronics_electrical/domain.json
- future test file under tests/
- possible helper/classifier file if owner authorizes
- web/app.py only if route/mode separation is later authorized
- engine/progression_loop.py only if runtime question-selection changes are later authorized

Any engine touch additionally triggers ARCHITECTURE_GUARDRAILS review.

No file modification is authorized by this plan.

## 8. Test Design Risks

Risks:

1. False positives from user-volunteered terms.
2. Blanket-ban drift where term tests become global prohibition.
3. Unclear early-stage boundary.
4. No current mode separation.
5. Risk of modifying domain questions before scope review.
6. Risk of changing deterministic gate logic unintentionally.
7. Replay or benchmark interaction if question-bank changes alter expected outputs.

## 9. Scope Review Requirement

Any implementation of these tests or guards requires separate scope review against MVP_SCOPE_FREEZE.md before code or prompt changes.

Approval of this design plan does not constitute that review.

## 10. Governance Effect

- R2 remains HELD
- FORM T remains blocked
- S-6 remains unclassified
- AA-5 remains blocked
- code changes are not authorized
- prompt changes are not authorized
- tests are not created
- prompt guards are not implemented

## 11. Required Next Owner Decision

The owner must decide separately whether to:

1. Accept this corrective content commit.
2. Authorize test specification drafting.
3. Authorize scope review before test implementation.
4. Define the early-stage threshold.
5. Authorize any mode or route separation design later.

These decisions are independent and sequential.

## 12. Correction Note

Commit 9736b79 created this file as an empty placeholder by mistake.

This document fills the intended test design plan content in a later corrective commit.

## 13. Boundary Statement

No code was modified by this plan.

No prompts were modified by this plan.

No tests were created by this plan.

No prompt guards were implemented by this plan.

No FORM T comparison has been performed.

No S-6 classification has been performed.

No AA-5 verdict has been started.

R2 remains HELD.

AA-4 final S-6 classification has NOT been performed.
