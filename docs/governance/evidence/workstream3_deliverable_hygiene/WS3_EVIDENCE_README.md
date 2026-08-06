# Workstream 3 Deliverable Hygiene — Evidence Package

Canonical basis: repository `Amirjaferali/inventorai`, branch
`feature/atomic-json-session-persistence`, merged tip
`0b04021d99290f8f747ee24d46b93c1dda69d66f` (PR #178 true two-parent merge).
Environment: Python 3.11.15, pytest 9.1.1, Linux 6.18.5. All artifacts were
generated from a clean checkout of the canonical tip.

## Purpose of each artifact

| File | Purpose |
|---|---|
| `WS3_HEAD_IDENTITY.md` | Canonical merge identity (commit, ordered parents, tree, timestamp, cumulative scope) |
| `WS3_SCOPE_RECORD.md` | Cumulative 11-file scope; per-commit 10-file / 2-file scope; production-scope confinement |
| `WS3_TEST_RECORD.md` | Exact commands + complete raw outputs for the five required test batteries |
| `WS3_FAILURE_CONFINEMENT.md` | Machine-verifiable proof that all 31 full-suite failures are pre-existing `tests/test_domain_registry.py` failures |
| `WS3_PROTECTED_FILES.md` | Git-diff / tree-id proof that every protected file and both prior evidence trees are unchanged |
| `WS3_DEFECT3_EVIDENCE.md` | Verified inventor-facing hygiene behavior across the five journeys, all six open-gap types, provider/gap public values, verbatim preservation |
| `WS3_DEFECT4_EVIDENCE.md` | Exact machine-checkable §4/§13/§14 count values, `count_relationship`, and the bound arithmetic |
| `generate_ws3_artifacts.py` | Deterministic generation harness for the ten representative artifacts (F3 loud failure; writes only into this directory; disclosed SESSION_ID/IDEA_ID/GENERATED_AT_UTC normalization) |
| `*_deliverable.json` / `*_deliverable.html` (10 files) | Representative inventor-facing Final Deliverable JSON+HTML for the five journeys (`ws1_completed`, `no_answer`, `unknown_action`, `safety_signal`, `legacy_provenance`); generated, never hand-edited |
| `WS3_ARTIFACT_MANIFEST.sha256` | SHA-256 of every evidence file (sorted by filename; manifest excluded) |

## Reproduction commands (from the repository root at the canonical tip)

```
python3 docs/governance/evidence/workstream3_deliverable_hygiene/generate_ws3_artifacts.py
python3 -m pytest -q tests/test_deliverable_hygiene.py            # 21 passed
python3 -m pytest -q tests/test_safety_signal.py                  # 18 passed
python3 -m pytest -q tests/test_safety_signal_stabilization.py    # 15 passed
# fixed 17-file focused suite (exact file list in WS3_TEST_RECORD.md): 297 passed
python3 -m pytest tests/ -q -p no:cacheprovider                   # 31 failed / 1360 passed / 1 skipped / 1 xfailed / 24 xpassed / 111 warnings
```

The harness normalization is disclosed and bounded: each run's random Flask
session id, IdeaState idea id, and generation timestamp are replaced by the
placeholders `SESSION_ID`, `IDEA_ID`, and `GENERATED_AT_UTC`; no other byte of
any generated artifact is altered. Regeneration was run twice with identical
normalized SHA-256 values (determinism proof).

## Known baseline failure statement

The full repository suite fails 31 tests, all in `tests/test_domain_registry.py`;
`WS3_FAILURE_CONFINEMENT.md` proves the identical 31 failures pre-exist at the
pre-Workstream-3 base `c64bd9206ef620078906831109562875055106de`. They are the
long-standing repository baseline and are unrelated to Workstream 3. The full
suite also emits 111 warnings (pre-existing; counted in the raw outputs).

## Claim boundaries

- This evidence claims exactly what its artifacts and cited passing tests
  prove — no more. No manual browser validation was performed or is claimed;
  HTML evidence is the committed Flask test-client render. No production
  deployment validation is claimed.
- This evidence package does NOT itself close Workstream 3. Evidence review,
  roadmap/§15 synchronization, and Workstream 3 closure remain separate,
  owner-gated actions.
