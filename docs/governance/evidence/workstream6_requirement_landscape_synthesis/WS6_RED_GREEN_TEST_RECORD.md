# WS6 Evidence — RED/GREEN Test Record

Focused file: tests/test_requirement_landscape_synthesis.py
(12 tests: P1-P6 protected invariants; R1-R5 RED-to-GREEN).

Canonical BASE RED (recorded at the PR #191 merge 721b4613..., reproduced at
that tip post-merge): 12 collected; 6 failed / 6 passed / 0 errors /
0 skipped / 0 xfailed. The six semantic failures:
- R1: "the byte-identical statement must be presented once (found 8
  standalone renderings)" + missing owner sentence;
- R2: "Section 13 provenance must use the owner-approved wording 'Recorded
  unknown'; found 'Recorded answer'";
- R3 (deferred): "... 'Deferred decision'; found 'Recorded answer'";
- R3 (provisional): "... 'Provisional assumption'; found 'Recorded answer'";
- R4: "_session_meta.requirement_landscape_synthesis does not exist";
- R5: "empty-content placeholder must use the owner-approved wording; found
  'Recorded answer awaiting restatement.'".

HEAD GREEN at 4f89d1ae... :
  python3 -m pytest tests/test_requirement_landscape_synthesis.py
  -> 12 passed, 0 failed, 0 skipped, 0 xfailed.
R4 was strengthened at GREEN (commit 4f89d1ae) with direct machine
parity — see WS6_METADATA_PARITY_RECORD.md. No P/R test was deleted,
skipped, xfailed, weakened, or converted to a non-asserting check.
