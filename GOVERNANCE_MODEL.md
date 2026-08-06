# INVENTORAI REPLAY GOVERNANCE MODEL
# Generated: 2026-05-20T14:23:45.833766
# Status: PROPOSED — pending review

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
