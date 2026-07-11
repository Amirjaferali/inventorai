# Workstream 1 Evidence Lock — Deliverable Baseline Directory

**Directory:** `docs/governance/evidence/workstream1_deliverable_baseline/`
**Governed by:** `docs/governance/DELIVERABLE_STABILIZATION_REMEDIATION_PLAN.md` §7 (Workstream 1)
**Status:** EVIDENCE ARTIFACTS — immutable once committed (CLAUDE.md fixture rules apply). Do NOT edit, regenerate-in-place, normalize, or "clean up" these files. Superseding evidence requires new files plus owner authorization.

Every artifact was produced by the committed script `reproduce_baseline.py`
run from the repository root at authoritative tip
`f1286c3d9f6dc027de09095eacc41437e405b9a4`, and is byte-reproducible after the
disclosed identifier normalization (see `WS1_BASELINE_IDENTITY.md`).

| File | Purpose |
|---|---|
| `reproduce_baseline.py` | Deterministic reproduction script (exact commands/inputs; §7.3). |
| `WS1_BASELINE_IDENTITY.md` | Baseline identity record (A): repo, branch, tip, timestamps, environment, hashes, normalization disclosure. |
| `inputs_false_negative_journey.json` | Verbatim scripted inventor inputs for the false-negative journey (C). |
| `journey_log_false_negative.json` | Per-iteration question order, actions, transitions, raw reasons, gap states, unknown-path behavior, completion observation (evidence items 11–12). |
| `deliverable_false_negative.json` / `.html` | **Current safety-signal FALSE-NEGATIVE baseline** deliverable (B) — raw engine package + rendered page. |
| `safety_signals_false_negative.json` | Derived safety signals for the false-negative journey (empty tuple → `[]`). |
| `inputs_positive_baseline.json` | Verbatim input for the positive baseline (the exact PR #122 statement) (C). |
| `deliverable_positive_regenerated.json` / `.html` | **Safety-signal POSITIVE baseline** (B), regenerated at the current tip from the PR #122 wording. Canonical historical record: `docs/governance/PR122_INVENTOR_STATED_SAFETY_SIGNALS_MANUAL_DEMO_VERIFICATION.md`. |
| `safety_signals_positive_regenerated.json` | Derived safety signals for the positive baseline (3 signals). |
| `WS1_DEFECT_MANIFEST.md` | Defect manifest (D): confirmed defect → artifact, section, quote, expected/observed, severity, target workstream. |
| `WS1_BASELINE_TESTS.md` | Baseline tests and commands record (E). |
| `WS1_CLOSURE_COMPARISON_REQUIREMENTS.md` | Mandatory future closure comparison definition (F). |

These artifacts document the CURRENT DEFECTIVE STATE. Nothing here claims any
defect is fixed, authorizes implementation, or makes a safety, feasibility,
compliance, or engineering determination.
