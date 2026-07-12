# WS2 Base-versus-Head Comparison Record

**Document ID:** WS2_BASE_HEAD_COMPARISON
**Type:** Evidence record (WS1_CLOSURE_COMPARISON_REQUIREMENTS.md conformance)
**Date:** 2026-07-12
**Base:** WS1 baseline artifacts (immutable; `../workstream1_deliverable_baseline/`, regenerated at `f1286c3d…`)
**Head:** artifacts in this directory (regenerated at implementation commit `3db477cd…` on base `71ace556…`)

## 1. Like-for-like proof

`inputs_false_negative_journey.json`, `journey_log_false_negative.json`, and
`inputs_positive_baseline.json` are **byte-identical** between base and head
(same SHA-256: `d177db5a…`, `328a4f0e…`, `e88fc36a…`). The scripted journey,
every question, every transition, every raw reason string, gap lifecycle, and
maturity progression are unchanged — the workstream touched only safety-signal
derivation.

## 2. Target defect absence (manifest defect 1, quoted)

- **Base:** `safety_signals_false_negative.json` = `[]`; deliverable meta block
  `"has_signals": false, "total": 0` with "No inventor-stated safety signals
  were derived from the recorded statements."
- **Head:** 3 signals, each traceable to its dangerous-consequence statement's
  assertion record:

| Signal | Source | Failure cue | Subject cue | Consequence cue | Dangerous statement (within the recorded answer) |
|---|---|---|---|---|---|
| SIG-001 | `assertion:rec_2` (iteration-3 answer) | `sensing is wrong` | `dangerous` | `could remain powered` | "If the sensing is wrong, the dangerous appliance could remain powered." |
| SIG-002 | `assertion:rec_3` (iteration-4 answer) | `fail to` | `danger` | `danger` | "…the wrong appliance could be disconnected and it would fail to isolate the actual source of danger." |
| SIG-003 | `assertion:rec_5` (iteration-6 answer) | `sticks` | `fire` | `damage` | "If the relay sticks, damage or overheating could continue and the fire risk could continue…" |

- **Head HTML:** the rendered deliverable shows 3 "Potential safety-critical
  assumption (inventor-stated)" entries (base HTML showed only the neutral
  empty statement).
- Provenance remains `inventor_stated`; validation status remains
  `requires_independent_validation`; every excerpt is the raw recorded answer
  under the documented whitespace handling (no statement rewritten).

## 3. Positive baseline (manifest defect 2 / regression guard)

- **Base:** 3 signals — the SAME statement duplicated across
  `assertion:rec_1`, `known_problem`, `known_mechanism`.
- **Head:** 1 signal (`assertion:rec_1`, deterministic source precedence) —
  the exact-duplicate dedup approved by contract §4. Contract closure criteria
  5–6: ≥1 valid signal required, "exactly three" explicitly NOT required.
  The PR #122 wording still detects.

## 4. Allowed-change enumeration (complete)

Unified diff of base vs head `deliverable_false_negative.json`: **46 changed
lines, ALL within `_session_meta.inventor_stated_safety_signals`** — the
`has_signals`/`total` values, the 3 added signal objects (including their
structural bracket lines), and the removal of the empty-statement rendering
condition. Zero changed lines elsewhere in the deliverable (verified by
filtering the diff for non-safety-block content: only the added objects'
brackets remain, which belong to the signal entries themselves). The HTML
diff is likewise confined to the safety-signals panel. The positive-baseline
diffs are confined to the same block (3 duplicate signals → 1).

## 5. Prohibited-regression checks

- Full-suite failure set unchanged: 31, all in `tests/test_domain_registry.py` (0 elsewhere).
- Replay/adversarial, WPS-001, benchmark, causal-gate: identical results (see WS2_RED_GREEN_TEST_RECORD.md).
- `tests/test_safety_signal.py`: UNCHANGED file, 18 passed.
- Positive safety baseline did not lose detection (≥1 signal).
- No previously-correct deliverable content disappeared or was reworded: proven by the diff confinement in §4 and the byte-identical journey log.
- No Workstream 1 artifact was modified (F4): the WS1 directory is untouched by every commit on this branch.

## 6. Disclosed-risk status (updated after owner-ordered correction)

The single residual false positive disclosed by the PR #172 independent
review (benign failover: "If the battery fails to charge, operation could
continue on mains power.") was CORRECTED by commits `291f5d47` (corrective
RED) and `b2888238` (bounded fix): bare `could continue` is no longer a
consequence cue; continuation counts only when explicitly harmful (risk /
fire risk / damage / overheating / danger / exposure / hazard could
continue). The paired harmful-continuation positives remain detected. The
regenerated artifacts in this directory are byte-identical before and after
the correction (the journey's signal cues were unaffected). No other
residual risk is currently disclosed.
