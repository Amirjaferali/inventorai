# WS2 BASE RED → IMPLEMENTATION → HEAD GREEN Test Record

**Document ID:** WS2_RED_GREEN_TEST_RECORD
**Type:** Evidence record (contract §13)
**Date:** 2026-07-12

## 1. BASE RED (Phase A)

- **Exact focused command against the authoritative base after adding ONLY the new tests:**
  `python3 -m pytest tests/test_safety_signal_stabilization.py -q`
- **Raw result:** `9 failed, 5 passed`
- **Confirmation that no extraction code had yet changed:** the RED commit
  `4303682f4301b3e9dd09d2b8c90236060ba91171` touches exactly
  `tests/test_safety_signal_stabilization.py` (1 file, 317 insertions); the
  `engine/` diff at that commit was empty (verified before committing).
- **Expected failing tests and failure reasons:**

| Failing test | Reason on unchanged base |
|---|---|
| test_positive_standalone_statements_signal | exact-substring cue conjunction derives 0 signals for the WS1 dangerous-consequence statements (missing failure/subject/consequence variants) |
| test_positive_adjacent_pairs_signal | no sentence bounding or pairing in the base matcher |
| test_metamorphic_groups_stable_classification_and_invariants | variant forms (fail to / failed to, isolate / remove power / remain energized, passive voice, plural, reorder, split, paraphrase) derive no signal |
| test_exact_duplicates_across_sources_collapse_to_one_signal | base statement derives no signal, and no dedup exists |
| test_materially_different_statements_are_not_deduplicated | same (0 signals ≠ 2 expected) |
| test_whitespace_only_variants_are_deduplicated | same (0 ≠ 1) |
| test_unicode_nfc_variants_are_deduplicated_with_excerpt_integrity | same (0 ≠ 1) |
| test_public_shape_and_constants_unchanged | base statement derives no signal to inspect |
| test_derivation_read_only_and_deterministic_ordering_across_sources | only one of two dangerous statements signals on base (1 ≠ 2) |

(The 5 passing-on-base tests are the negative/fragment/cross-record/_WARNING/
repeatability checks, which the defective base happens to satisfy trivially.)

## 2. Implementation

- **Implementation commit identity:** `3db477cd2779803f771f59d078046a5e8d459d75`
  (parent = RED commit `4303682f…`), changing exactly `engine/safety_signal.py`
  (`1 file changed, 147 insertions(+), 20 deletions(-)`).

## 3. HEAD GREEN

- **Exact focused command and result at head:**
  `python3 -m pytest tests/test_safety_signal_stabilization.py -q` → `14 passed`

## 4. Full verification battery at head

| Suite / command | Result | Baseline comparison |
|---|---|---|
| `python3 -m pytest tests/test_safety_signal.py -q` (UNCHANGED file) | `18 passed` | identical |
| Deliverable/landscape/validation focused set (7 files incl. both safety files) | `168 passed` | +14 new, others identical |
| `python3 -m pytest tests/test_assess_response_replay.py tests/test_assess_response_adversarial.py -q` | `26 passed, 18 xpassed` | identical |
| `python3 -m pytest tests/test_wps001_invariants.py -q` | `20 passed, 1 skipped` | identical |
| `python3 -m pytest tests/test_progression_benchmark.py -q` | `27 passed, 6 xpassed` | identical |
| `python3 -m pytest tests/test_causal_connective_substance_gate.py -q` | `177 passed` | identical |
| `python3 -m pytest tests/ -q` (full regression) | `31 failed, 1338 passed, 1 skipped, 1 xfailed, 24 xpassed` | baseline `31 failed, 1324 passed, …`; delta = exactly the +14 new fixtures; **0 failures outside `tests/test_domain_registry.py`** (verified by ID filter) |

Regression interpretation (contract §11): no new failures; no failure outside
the previously known `tests/test_domain_registry.py` set; no prohibited
regression in replay, benchmark, WPS-001, causal-gate, or focused safety
results; prior-failure count unchanged (31).

## 4A. Owner-ordered benign-failover correction (post-review)

The PR #172 independent review disclosed one residual false positive outside
the contracted matrix: "If the battery fails to charge, operation could
continue on mains power." produced a signal (`fails to` + subject `mains` +
bare consequence modal `could continue`). The owner ordered correction
before merge.

- **Corrective RED:** commit `291f5d478396012aa3f072bdf39a97d86e7f3c05`
  (tests only; `engine/` diff empty). Command
  `python3 -m pytest tests/test_safety_signal_stabilization.py -q` →
  `2 failed, 13 passed`: the benign-failover negative failed by producing a
  signal, and the harmful-continuation counterpart positives
  ("If isolation fails, overheating could continue." / "If protection
  fails, damage could continue.") failed by producing none.
- **Correction:** commit `b2888238339f5da311eeb43f246df0c2389f466e`
  (`engine/safety_signal.py` only, `16 insertions, 1 deletion`): the bare
  modal `could continue` was removed from the consequence family and
  replaced by explicit harmful-continuation phrases (risk / fire risk /
  damage / overheating / danger / exposure / hazard could continue);
  failure family gained the finite phrases `isolation fails` /
  `protection fails`; subject family gained `protection`. No sentence
  blacklist, no removal of harmful-continuation detection, no schema or
  architecture change.
- **Corrective GREEN:** same command → `15 passed`. Paired checks: the
  three benign-failover statements derive 0 signals; the three
  harmful-continuation statements each derive exactly 1.
- **Battery at corrected head:** unchanged `tests/test_safety_signal.py`
  `18 passed`; replay+adversarial `26 passed, 18 xpassed`; WPS-001
  `20 passed, 1 skipped`; benchmark `27 passed, 6 xpassed`; causal gate
  `177 passed`; full suite `31 failed, 1339 passed, 1 skipped, 1 xfailed,
  24 xpassed` — 0 failures outside `tests/test_domain_registry.py`
  (+1 passed = the new paired test).
- **Regenerated artifacts:** byte-identical to the §4 run (the journey
  signals' cue selections are unaffected by the correction); verified by a
  clean git tree after re-running the committed harness.

## 5. F3 loud-failure demonstration

With the iteration bound temporarily reduced to 3 in an in-memory import
(file on disk untouched), the harness printed
`JOURNEY INCOMPLETE — completion branch not reached within 3 iterations; no
artifact written (contract §7 / F3).` and exited with code 2, writing zero
artifacts (directory inspected before the real runs).
