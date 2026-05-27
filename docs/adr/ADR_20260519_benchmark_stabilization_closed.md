# ADR — Benchmark Stabilization Closed

Date: 2026-05-19
Status: CLOSED
Author: Engineering session with Claude

## Context
IoT Electronics feasibility analyzer required schema-compliant JSON output
validated against a strict benchmark runner with 7 evaluation criteria.

## Problem
Starting state: Schema Compliance 0%, JSON parse failures 15/22, score ~76/100.

## Decision
Stabilize prompt layer to canonical baseline. Defer contradiction detection.

## Solved via Prompt Layer
- schema_normalization      100%
- grounding                 100%
- missing_info_recovery     100%
- gate_engine_utility       100%
- json_serialization        100%

## Deferred — Architecture Layer Required
- contradiction_detection   (restraint_check 68%)
- confidence_calibration    (86%, prompt ceiling confirmed)

## Architectural Findings
1. Schema SSOT must be read directly from file, never reconstructed from screenshots
2. max_tokens=2000 caused truncation — raised to 4096
3. apparent_components_ar is array of objects, not strings (nested schema excavation required)
4. Prompt entanglement instability confirmed empirically via failed_regression
5. Prompt ceiling exists: serialization/grounding solvable, semantic reasoning not

## Prompt Layer Responsibilities (confirmed)
- JSON serialization
- schema normalization
- grounding / no hallucination
- missing info recovery
- feasibility calibration

## Outside Prompt Layer Scope
- contradiction detection (constraint graph problem)
- multi-condition semantic consistency
- symbolic validation

## Canonical Baseline
baseline_20260518_1809_score93
SHA256: stored in benchmarks/index.json

## Reopen Trigger
contradiction_detection becomes business-critical product requirement.

## Next Phase
- real-world input telemetry
- failure taxonomy from production users
- edge-case harvesting
- dataset evolution
- operational monitoring
