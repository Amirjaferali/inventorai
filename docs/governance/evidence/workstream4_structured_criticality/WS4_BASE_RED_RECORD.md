# WS4_BASE_RED_RECORD — the Workstream 4 RED gate

- BASE RED commit: `dd591353cbf513108e37d1db86b35c33420f402e` (single parent
  `9825ae0b012e59ed96e843a86390dee5088bb0a9`; tree
  `754519bf69c7e6d35c614cf84090e3b883b743ed`; exactly one added file,
  `tests/test_structured_criticality.py`, 466 lines, file SHA-256
  `f3f8bd67cf47ef7728c81d98b24c5c43d3d356b96421881c3aee4c0eb7686790`).
- **No source implementation existed at BASE RED** — the commit is tests-only
  on a base whose product surface was byte-identical to the contract-pinned
  base (see WS4_HEAD_IDENTITY.md §3).
- BASE result (owner-verified before commit, re-verified at commit):
  `8 failed, 5 passed, 1 skipped, 1 warning`
  - **5 protected invariants passed** (P1–P5: AI-Q2 free text never
    classifies; iteration-7 statement recorded verbatim; §13 never-interacted
    public wordings; rendering changes nothing; no raw tokens inventor-facing).
  - **8 genuine RED tests failed** (R1–R8), each on an obligation-specific
    missing-behavior assertion — never an import/fixture/route defect.
  - **1 GREEN-only journey placeholder skipped** by explicit owner decision
    (owner final RED-suite review), recorded as mandatory GREEN work and
    fully replaced at HEAD GREEN by the real journey tests G1–G5 (the final
    suite contains zero skips and zero xfails).
- RED suite lifecycle: proposed → owner bounded revision (removed the
  duplicative deferral-zero-delta BASE test; de-duplicated cascading
  failures; un-pinned the recorder call shape) → owner final revision
  (removed the label-scanning R9; recorded the GREEN-only obligations) →
  owner commit authorization.
- Independent BASE RED review result: **PASS** (owner-communicated;
  "the truly independent review of Draft PR #183 has completed with PASS").
