# NON-SPECIALIST POLICY ENFORCEMENT PLAN

## 1. Status

ENFORCEMENT PLAN — COMMITTED GOVERNANCE RECORD

Date: 2026-06-10

This plan defines how enforcement could work. It authorizes no discovery, no tests, no code changes, no prompt changes, no prompt guards, and no runtime implementation.

## 2. Source Governance

Source records:

- NON_SPECIALIST_QUESTIONING_POLICY.md — commit a31010a
- R-2_R1_PRODUCT_ALIGNMENT_DRIFT_RECORD.md — commit 10d6876

The non-specialist questioning policy is committed as governance but not implemented. The platform runtime behavior remains unchanged.

## 3. Problem to Solve

The current app may still ask engineering-heavy questions too early in the non-specialist path.

R1 showed that documentation alone does not prevent prompt or question drift. Without enforcement, violations may only appear during live participant evidence, which is the most expensive and risky detection point.

## 4. Enforcement Goals

1. Prevent early engineering-gated questions in the non-specialist path.
2. Preserve technical questioning for owner-authorized specialist paths or later Engineering Translation stages.
3. Preserve existing gap taxonomy unchanged.
4. Change asking strategy only, not deterministic gate logic, unless separately authorized.
5. Keep PASS/WARN/BLOCK, maturity transitions, and stall detection intact unless a later owner decision authorizes changes.

## 5. Discovery Step

Discovery is read-only and requires separate owner authorization before execution.

Discovery targets:

1. Locate where current platform questions come from.
2. Identify files controlling the electronics_electrical flow.
3. Identify whether any non-specialist / specialist mode distinction exists today.
4. Identify current tests related to question flow.
5. Map question strings to source files, stages, and trigger conditions.

Likely read-only methods include:

- grep for question dictionaries or question text
- inspect domains/electronics_electrical
- inspect engine/progression_loop.py
- inspect web/app.py routes
- inspect tests for current question-flow coverage

Discovery output: a draft QUESTION_FLOW_DISCOVERY_REPORT.md for owner review, mapping every question string to its file, its stage, and its trigger condition. Commit requires separate owner approval.

## 6. Proposed Enforcement Layers

Layer 1 — Question inventory:
Complete list of platform-askable questions with source locations.

Layer 2 — Question classification:
Each platform question labeled as one of:
- NON_SPECIALIST_SAFE
- ENGINEERING_GATED
- TRANSLATION_CANDIDATE
- SPECIALIST_ONLY
- ENGINEERING_TRANSLATION_STAGE

Layer 3 — Non-specialist prompt guard:
Prevent ENGINEERING_GATED questions from being asked early in the non-specialist path.

Layer 4 — Specialist / engineering allowance:
Allow engineering-heavy questions only in owner-authorized specialist or engineering-translation contexts.

Layer 5 — Term-based tests:
Detect disallowed early engineering terms in platform-asked non-specialist questions.

Layer 6 — Attribution-aware tests:
Distinguish platform-asked questions from user-volunteered vocabulary.

## 7. Proposed Tests

Fail conditions:

An early non-specialist platform question contains engineering-gated terms such as:

- voltage
- current
- frequency
- circuit
- component
- signal transformation
- electrical constraints
- datasheet
- calculation

Explicit non-failure conditions:

- The user voluntarily uses those terms in a response.
- The question belongs to an owner-authorized specialist path.
- The question belongs to a later Engineering Translation stage.
- The term appears in documentation, comments, or evidence transcripts rather than in a platform-asked non-specialist question.

Design notes:

1. "Early" requires a governed definition before test implementation.
2. Term matching is a review trigger, not a semantic verdict.
3. Tests must not create a blanket ban on engineering terms. They must allow engineering-heavy questions only in owner-authorized specialist or engineering-translation contexts.

## 8. Scope Review Requirement

Any implementation that changes question banks, routing, mode separation, prompt behavior, tests, or runtime behavior requires separate scope review against MVP_SCOPE_FREEZE.md before code or prompt changes.

Approval of this plan does not constitute that review.

## 9. Governance Effect

Until separately authorized:

- R2 remains HELD
- FORM T remains blocked
- S-6 remains unclassified
- AA-5 remains blocked
- code changes are not authorized
- prompt changes are not authorized
- test creation is not authorized
- prompt guard implementation is not authorized
- QUESTION_FLOW_DISCOVERY_REPORT.md is not authorized for creation or commit by this plan alone
- architecture redesign is not authorized

## 10. Required Next Owner Decisions

The owner must decide separately whether to:

1. Approve this enforcement plan as governance.
2. Authorize discovery only.
3. Authorize test design.
4. Authorize implementation after scope review.
5. Authorize any route or mode separation.
6. Authorize any prompt guard.

These decisions are sequential. Approval of one does not imply approval of the next.

## 11. Boundary Statement

No code was modified by this plan.

No prompts were modified by this plan.

No tests were created by this plan.

No prompt guards were implemented by this plan.

No FORM T comparison has been performed.

No S-6 classification has been performed.

No AA-5 verdict has been started.

R2 remains HELD.

AA-4 final S-6 classification has NOT been performed.
