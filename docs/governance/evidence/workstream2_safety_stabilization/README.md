# Workstream 2 Safety Signal Stabilization — Evidence Directory

**Directory:** `docs/governance/evidence/workstream2_safety_stabilization/`
**Governed by:** `docs/governance/SAFETY_SIGNAL_STABILIZATION_INCREMENT_CONTRACT.md` (APPROVED AND CANONICAL; blob `3db597c77d14aa8f39f7a624c7c32d4984e4f3a3`)
**Status:** EVIDENCE ARTIFACTS — immutable once committed. The Workstream 1 baseline directory (`../workstream1_deliverable_baseline/`) was never modified (F4); all regenerated outputs live only here.

| File | Purpose |
|---|---|
| `regenerate_and_compare.py` | COPY of the immutable WS1 harness (F4 copied-script convention) with the F3 loud-failure gate (`JOURNEY INCOMPLETE`, exit 2, no artifact on incomplete journey). Inputs byte-identical to WS1. |
| `inputs_false_negative_journey.json` | Journey inputs — **byte-identical to the WS1 baseline** (same SHA-256 `d177db5a…`). |
| `journey_log_false_negative.json` | Journey log — **byte-identical to the WS1 baseline** (same SHA-256 `328a4f0e…`): the journey, scoring, transitions, and reasons are UNCHANGED by this workstream. |
| `deliverable_false_negative.json` / `.html` | Regenerated deliverable at the implementation head: the previously false-negative journey now carries 3 inventor-stated safety signals. |
| `safety_signals_false_negative.json` | Head signal derivation: 3 signals (base: `[]`). |
| `inputs_positive_baseline.json` | Byte-identical to WS1 (`e88fc36a…`). |
| `deliverable_positive_regenerated.json` / `.html` | Positive baseline at head: 1 signal (exact-duplicate dedup collapsed the base's 3 duplicate-source signals; ≥1 required, "exactly three" explicitly not required — contract closure 5–6). |
| `safety_signals_positive_regenerated.json` | Head positive signals (1). |
| `WS2_HEAD_IDENTITY.md` | Head identity, environment, artifact hashes, determinism proof. |
| `WS2_RED_GREEN_TEST_RECORD.md` | BASE RED → IMPLEMENTATION → HEAD GREEN evidence (contract §13) + full verification battery + F3 demonstration. |
| `WS2_BASE_HEAD_COMPARISON.md` | Base-versus-head comparison: defect-absence proof, allowed-change list, prohibited-regression checks. |

Nothing here authorizes a merge, closure, or any safety/feasibility/compliance determination.
