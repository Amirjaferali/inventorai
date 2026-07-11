# WS1 Baseline Tests and Commands Record

**Document ID:** WS1_BASELINE_TESTS
**Type:** Evidence-lock test baseline (Workstream 1, plan §7 item E)
**Status:** RECORDED — immutable evidence
**Date:** 2026-07-11
**Code under test:** authoritative tip `f1286c3d9f6dc027de09095eacc41437e405b9a4`
**Environment:** Python 3.11.15; pytest 9.1.1; Flask 3.1.3 (container-installed; no requirements manifest in the repository). Run from the repository root.

## Focused tests currently available (relevant areas)

| Area | Test file(s) |
|---|---|
| Safety-signal extraction | `tests/test_safety_signal.py` |
| Deliverable assembly | `tests/test_deliverable_assembler.py`, `tests/test_increment_6_deliverable_redesign.py`, `tests/test_stage3_evidence_deliverable.py` |
| Requirement landscape / criticality | `tests/test_increment_4_requirement_landscape.py`, `tests/test_phase_7c_requirement_landscape_collapse.py` |
| Validation plan | `tests/test_increment_5_validation_plan.py`, `tests/test_phase_7a_validation_plan_grouping.py`, `tests/test_phase_7b_validation_plan_collapse.py` |
| Scoring gate (locked) | `tests/test_causal_connective_substance_gate.py` (includes the 100-case `_REVIEW_MATRIX` with 1 disclosed FP / 14 disclosed FN) |
| Replay / adversarial (locked) | `tests/test_assess_response_replay.py`, `tests/test_assess_response_adversarial.py` |
| WPS-001 invariants | `tests/test_wps001_invariants.py` |
| Benchmark | `tests/test_progression_benchmark.py` (historical truth source: `benchmark/run_benchmark_v1.py`) |

## Commands and current results at `f1286c3d`

| Command | Result |
|---|---|
| `python3 -m pytest tests/test_safety_signal.py tests/test_deliverable_assembler.py tests/test_increment_4_requirement_landscape.py tests/test_increment_5_validation_plan.py tests/test_increment_6_deliverable_redesign.py tests/test_phase_7a_validation_plan_grouping.py tests/test_phase_7b_validation_plan_collapse.py tests/test_phase_7c_requirement_landscape_collapse.py tests/test_stage3_evidence_deliverable.py -q` | `179 passed` |
| `python3 -m pytest tests/test_assess_response_replay.py tests/test_assess_response_adversarial.py -q` | `26 passed, 18 xpassed` |
| `python3 -m pytest tests/test_wps001_invariants.py -q` | `20 passed, 1 skipped` |
| `python3 -m pytest tests/test_progression_benchmark.py -q` | `27 passed, 6 xpassed` |
| `python3 -m pytest tests/test_causal_connective_substance_gate.py -q` | `177 passed` |
| `python3 -m pytest tests/ -q` (full regression) | `31 failed, 1324 passed, 1 skipped, 1 xfailed, 24 xpassed` |

The 31 full-suite failures are ALL confined to `tests/test_domain_registry.py`
(verified by ID filter: 31 there, 0 elsewhere) and are the documented
pre-existing baseline caused by `domains/iot_electronics/domain.json`
(`schema_version=None`). Any remediation regression comparison must use this
exact failure baseline.

## Missing fixtures / coverage (recorded, NOT added in Workstream 1)

1. **No test reproduces the safety-signal false negative**: `tests/test_safety_signal.py` covers the cue-conjunction positive/negative paths but has no fixture for meaning-equivalent dangerous-consequence statements that miss the cue lists (defects 1–2). Positive, negative, AND metamorphic fixtures are required by plan §12 before Workstream 2 acceptance.
2. **No cross-section consistency test** for requirement counts (defect 4).
3. **No deliverable-hygiene test** asserting the absence of raw internal enums in the rendered deliverable (defect 3).
4. **No committed full-deliverable fixtures existed before this evidence lock** — the artifacts in this directory are the first.
5. **No test pins the unknown-path behavior** documented at journey iteration 5 (defect 18).

## Determinism

Reproduction is deterministic: two full runs of `reproduce_baseline.py` in
different wall-clock seconds produced byte-identical normalized artifacts
(SHA-256 table in `WS1_BASELINE_IDENTITY.md`). No test was added or modified
in Workstream 1.
