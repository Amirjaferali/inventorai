# ADR — Engine Extraction from Benchmark Runner
Date: 2026-05-20
Status: IN PROGRESS
Parent: ADR_20260519_product_decision_contract.md

## Why
run_benchmark_v1.py currently contains:
- transport logic (HTTP to Anthropic)
- JSON extraction
- output normalization
- schema validation
- scoring/benchmark logic
- test harness

This violates separation of concerns and prevents reuse in product API.

## Goal
Extract reusable engine/ modules that benchmark imports.
Direction must remain: benchmark → engine (never reversed).

## Modules to Extract
engine/
  __init__.py
  call_anthropic.py     — HTTP transport only
  extract_json.py       — JSON parsing/extraction only
  normalize_output.py   — schema normalization, idempotent
  compute_decision.py   — pure deterministic PASS/WARN/BLOCK mapping

## Invariants (must hold before/after extraction)
- benchmark score unchanged (canonical ref: benchmarks/baseline_canonical_score93.json)
- Schema Compliance remains 100%
- normalize_output is idempotent: normalize(normalize(x)) == normalize(x)
- compute_decision is pure: no HTTP, no env, no filesystem, no randomness
- DECISION_CONTRACT_VERSION = "v1" embedded in compute_decision.py
- No internal enums leaked to frontend
- Transport failures separated from evaluation failures

## Forbidden During Extraction
- No behavior changes
- No prompt edits
- No schema edits
- No scoring logic changes
- No API or frontend work
- No shared mutable globals inside engine/
- No env var access inside engine/ (pass explicitly)

## Rollback Condition
If benchmark score deviates from canonical baseline after import replacement → stop, revert, treat as regression.

## Error Taxonomy (separation required)
anthropic_timeout     — transport failure
invalid_json          — extraction failure
normalization_failure — normalization failure
decision_blocked      — valid evaluation result (not an error)


## Dependency Graph (enforced)
call_anthropic.py    → NO imports from benchmark/ or engine/compute_decision
extract_json.py      → NO imports from benchmark/ or transport layer
normalize_output.py  → NO imports from Anthropic client or transport layer
compute_decision.py  → NO imports from transport layer or benchmark/

Allowed:
  benchmark/run_benchmark_v1.py → imports engine/*
  engine/* → imports stdlib only + each other (one direction only)
  No circular imports permitted.

## Completion Criteria
1. All 4 engine/ modules exist and are importable
2. run_benchmark_v1.py imports from engine/ instead of defining locally
3. Benchmark produces same score as canonical baseline
4. Idempotency test passes for normalize_output
5. compute_decision determinism test passes
