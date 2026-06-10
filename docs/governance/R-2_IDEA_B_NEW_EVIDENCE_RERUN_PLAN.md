# R-2 IDEA B NEW EVIDENCE RERUN PLAN

**Status:** GOVERNANCE PLAN — COMMITTED BEFORE EXECUTION
**Date:** 2026-06-10
**Repository HEAD at drafting:** 03dfc62 governance: record R-1A Idea B transcript search result

## 1. Purpose

This plan governs a future rerun of Idea B, Water Leak Detection, as NEW evidence.

It does not restore the lost Idea B Sessions 3/4. Any rerun sessions will have new SIDs, new timestamps, new transcript files, and new evidentiary status.

New sessions must be named:

- Idea B Rerun Session R1
- Idea B Rerun Session R2

They must never be called Session 3 or Session 4.

## 2. Required Preconditions

Before execution, all of the following must hold:

1. Repository is clean.
2. Fixed-domain Idea B route exists: /start_ilt002_water_leak.
3. Transcript persistence is active.
4. JSONL path pattern is confirmed from current source code.
5. Same participant availability is confirmed by owner.
6. Owner explicitly authorizes execution using: R-2 EXECUTION AUTHORIZED.

## 3. Read-Only Checks Before Rerun

Before any rerun, execute read-only checks for:

- git status
- latest commits
- water leak route existence
- JSONL persistence code
- transcript path pattern
- absence of stale /tmp ILT002 JSONL files

Any failed check stops execution.

## 4. Execution Rules

When owner authorizes execution:

1. Start Flask from repository root.
2. Use only /start_ilt002_water_leak.
3. Do not use the standard /start route.
4. Record the issued SID immediately.
5. Conduct the session under ILT002_EXECUTION_GUIDE.md.
6. On session end, verify /tmp/ilt002_transcript_{SID}.jsonl exists.
7. Validate JSONL before copying:
   - file exists
   - record count greater than zero
   - every row has the same SID
   - domain is electronics_electrical
   - iterations are sequential or gaps documented
   - transcript contains responses, not only questions
8. Copy validated JSONL into docs/governance immediately.
9. Commit each rerun transcript separately.
10. Repeat separately for R2.

## 5. Evidence Requirements

Transcript path pattern:

docs/governance/ILT002_IDEA_B_RERUN_SESSION_R{N}_TRANSCRIPT_{SID}.jsonl

Commit message pattern:

evidence: ILT-002 Idea B Rerun Session R{N} transcript SID {SID}

Each evidence commit must state:

- SID
- JSONL path
- record count
- iteration range
- domain verification result

## 6. Governance Boundaries

New rerun sessions are NEW evidence.

They must not be merged with, substituted for, or treated as the lost Sessions 3/4.

SESSION4_CLASSIFICATION_CORRECTION_NOTE.md does not substitute for missing primary transcript evidence.

No S-6 classification is allowed during rerun.

No FORM T is allowed until:
1. Idea B rerun evidence is committed.
2. Idea A Emergence Timing Table is populated and locked.
3. AA-4A is rerun and reaches READY status.

Protocol learning risk must be carried into later FORM T analysis because the participant has already completed prior sessions.

This plan does not modify FORM T, the Emergence Timing Table, code, campaign scope, or final verdict rules.

## 7. Owner Approval Checkpoint

Execution requires separate owner authorization.

The required authorization phrase is:

R-2 EXECUTION AUTHORIZED

Without that phrase, this plan is documentation only.

## 8. Current Boundary Statement

Nothing is executed by this plan.

No Flask app has been started.

No rerun session has been conducted.

No transcript has been created.

No FORM T has been performed.

No S-6 classification has been performed.

No AA-5 verdict has been started.

AA-4 final S-6 classification has NOT been performed.
