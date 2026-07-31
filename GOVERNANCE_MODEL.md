# INVENTORAI REPLAY GOVERNANCE MODEL
# Generated: 2026-05-20T14:23:45.833766
# Status: PROPOSED — pending review

> **BOUNDED-PURPOSE CLARIFICATION (added by the Audit-Disposition & Lean-Governance gate):**
> This file is **PARTIALLY CURRENT — NOT SOLE CURRENT AUTHORITY.** Its authority-hierarchy /
> boot-model principles remain referenced by the governance boot sequence, but this file is
> **not** the current execution authority and its replay-era `Status: PROPOSED — pending
> review` header and some sections are **historical**. It is **not** marked entirely obsolete.
> Future agents must resolve current authority from `CLAUDE.md`, the current anchors, the
> canonical plan (`docs/governance/PRODUCT_FOUNDATION_AND_COMMERCIAL_READINESS_REMEDIATION_PLAN.md`),
> the latest append-only `ACTIVE_EXECUTION_ROADMAP.md` records, and current owner decisions
> (`docs/governance/OWNER_DECISION_REGISTER.md`). Where this file conflicts with those, they
> govern. Body preserved unchanged below. (Stale-document register SD-11; DISC-017.)

## AUTHORITY HIERARCHY

### TIER 1 — SEMANTIC AUTHORITY
Source: benchmark/run_benchmark_v1.py
Authoritative for: exp_conf, exp_sig, exp_gaps

### TIER 2 — EXECUTION EVIDENCE
Source: tests/replay/cases/TC-*.json
NOT authoritative for semantic expectations

### TIER 3 — REGRESSION BASELINE
Source: tests/golden/ — NOT semantic authority
TC-02 golden = CONTAMINATED

## VIOLATIONS

VIOLATION-01: Semantic authority not in fixtures — PENDING DESIGN DECISION
VIOLATION-02: TC-02 golden contaminated — NOT regenerated
VIOLATION-03: verify_parity uses golden not benchmark — PENDING

## STEPS

STEP 1: Define authority injection path (A or B) — PENDING
STEP 2: Rebuild golden — PENDING Step 1
STEP 3: Fix parity gate — PENDING Steps 1+2

## SIGN-OFF
# Reviewer:
# Date:
# Approved:
