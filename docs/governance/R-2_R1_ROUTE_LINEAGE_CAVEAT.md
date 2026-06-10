# R-2 R1 ROUTE LINEAGE CAVEAT

Status: GOVERNANCE CAVEAT
Date: 2026-06-10
Scope: Idea B Rerun Session R1 evidence lineage only

## 1. Transcript Preserved

Idea B Rerun Session R1 transcript was preserved and committed.

Commit:

072e5c0 evidence: ILT-002 Idea B Rerun Session R1 transcript SID cb616515-8ccd-4989-8a77-34cccdd1e5d9

Transcript path:

docs/governance/ILT002_IDEA_B_RERUN_SESSION_R1_TRANSCRIPT_cb616515-8ccd-4989-8a77-34cccdd1e5d9.jsonl

Verified properties from terminal output:

- Record count: 8
- Iterations: 2 through 9
- Domain: electronics_electrical
- Empty responses: 0
- Transcript copied from /tmp before environment shutdown

## 2. Route-Lineage Caveat

During execution, two SIDs appeared:

- SID from the explicit POST to /start_ilt002_water_leak:
  44b3acbb-88a2-4cf9-a4c4-52f1bd0dea4e

- SID of the session actually answered and preserved:
  cb616515-8ccd-4989-8a77-34cccdd1e5d9

This creates a route-lineage caveat.

The preserved transcript is valid as a captured session artifact, but its admissibility as clean R-2 Idea B rerun evidence is not automatically granted.

## 3. Governance Effect

Until explicitly reviewed and accepted by the owner:

- R1 must not be used for FORM T.
- R1 must not be used for S-6 classification.
- R1 must not be treated as clean replacement evidence for lost Idea B Sessions 3/4.
- R2 must not start on the assumption that R1 is fully admissible.

## 4. Required Future Decision

Before any FORM T or S-6 work, the owner must decide whether:

1. R1 is accepted with this route-lineage caveat, or
2. R1 is preserved but excluded from FORM T evidence, requiring a cleaner rerun session.

## 5. Boundary

No FORM T comparison has been performed.

No S-6 classification has been performed.

No AA-5 verdict has been started.

AA-4 final S-6 classification has NOT been performed.
