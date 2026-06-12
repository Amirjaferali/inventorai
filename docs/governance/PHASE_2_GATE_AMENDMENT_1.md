# PHASE 2 GATE AMENDMENT 1 — PHASE 1 TEST EXPECTATION CORRECTION

## 1. Status

- Owner ruling, amending PHASE_2_PATH_N_CONTENT_SELECTION_AUTHORIZATION.md
  (`b3a5fba`) §4 (authorized files) and §10 (gate expectations).
- Issued during Phase 2 implementation, before any implementation commit.
- This document authorizes exactly one test amendment and nothing else.

## 2. Problem (evidence)

During Phase 2 gate execution, gate
`pytest tests/test_phase1_path_designation.py -q` failed:

    FAILED tests/test_phase1_path_designation.py::
    test_path_n_session_receives_same_question_as_legacy

The test encodes the Phase 1 designation-only invariant
(`aa068fd` §5: "The designation is carried but not consumed").
Phase 2's committed purpose (`b3a5fba` §3) is to consume the
designation: `state.path == "N"` selects approved N-* content.
The two commitments are mutually exclusive by design. The defect is
in the §10 gate expectation, which was written without registering
that one of the 7 Phase 1 tests asserts the pre-Phase-2 world.
The implementation is correct; semantic masking to satisfy the old
assertion is forbidden (CLAUDE.md).

## 3. Ruling

1. `tests/test_phase1_path_designation.py` is ADDED to the Phase 2
   authorized file list (`b3a5fba` §4) for EXACTLY ONE permitted
   change: amend `test_path_n_session_receives_same_question_as_legacy`.
2. The amended test must:
   - no longer assert Path N equals legacy after Phase 2;
   - assert the Path N question DIFFERS from the legacy question;
   - assert the Path N question MATCHES approved artifact N-* content.
3. All other tests in that file remain byte-untouched.
4. Gate expectation correction: the §10 expectation "Phase 1 suite
   7 passed" stands numerically; the MEANING of one test changes
   from a designation-only invariant to a Phase 2 regression guard
   against returning to legacy content.
5. Supersession note: `aa068fd` §5 ("carried but not consumed")
   describes the state as of `5084110` and is superseded for
   post-Phase-2 state. The Phase 2 closure record will restate the
   current execution state.

## 4. Non-authorizations (unchanged)

This amendment does NOT authorize: `runtime_integrated=true`, R2,
FORM T, S-6 classification, AA-5, deterministic gate changes,
PASS/WARN/BLOCK changes, `domain.json` changes, artifact mutation,
xfail conversion, or any diff beyond §3 of this document.

## 5. Rollback

Reverting the eventual implementation commit plus this amendment's
test change restores the pre-Phase-2 world exactly.
