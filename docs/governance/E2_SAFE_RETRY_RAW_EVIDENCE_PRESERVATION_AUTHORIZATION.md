# E2_SAFE_RETRY_RAW_EVIDENCE_PRESERVATION_AUTHORIZATION.md
# Status: PROPOSED -- NOT YET AUTHORIZED FOR EXECUTION

---

## 1. Record Identity

Record type: E-2 Safe Retry Raw Evidence Preservation Authorization (DRAFT)
Selected option: ROADMAP §7 Option A -- byte-identical durable preservation
Authoritative baseline HEAD: aef888ee4268e636c892d3107f7c5cb44c5193bb

This draft authorizes nothing by itself. It proposes a governed preservation
method for separate owner review. No copy, stage, commit, push, or deletion is
authorized by this document.

---

## 2. Authoritative Baseline

HEAD / origin/main:                aef888ee4268e636c892d3107f7c5cb44c5193bb
Gate C authorization:              d4140d4
E-2 evidence acceptance record:    d130256
Post-acceptance roadmap sync:      aef888e
E-2 result:                        LIMITED TECHNICAL ACCEPTED
Gate C:                            CONSUMED
Second attempt:                    NOT AUTHORIZED

Holds (unchanged):
runtime_integrated: false
R2:                 HELD
FORM T:             BLOCKED
S-6:                UNCLASSIFIED
AA-5:               BLOCKED

---

## 3. Evidence Governed by This Draft

Execution SID: d39526ce-92a5-469a-9c93-5e6d23f7a31b

Source files and authoritative SHA-256 hashes (from accepted record d130256):

| Source path | SHA-256 |
|-------------|---------|
| /tmp/ilt002_transcript_d39526ce-92a5-469a-9c93-5e6d23f7a31b.jsonl | c28936ed89c8bde8c11dc54237873315ca2cad02bba528b749dbf815f3bbe5b9 |
| /tmp/e2_session_get_iter_1.html | f6c033081037324482e1477c632108cb2ccd7204df32f1c91584c88dc943fe0d |
| /tmp/e2_session_final_state.html | d98a3ba0fbddec4bd34780896bfc7eb2787e5f1199dec92652d1fbe99c1abc35 |

---

## 4. Proposed Governed Destination

Destination directory (exact):

  docs/governance/evidence/e2_safe_retry/d39526ce-92a5-469a-9c93-5e6d23f7a31b/

Destination filenames (exact):

  ilt002_transcript_d39526ce-92a5-469a-9c93-5e6d23f7a31b.jsonl
  e2_session_get_iter_1.html
  e2_session_final_state.html
  SHA256SUMS

The SHA256SUMS manifest is newly generated governance metadata. It is NOT one of
the three raw captured artifacts. It is produced after copying, from the
destination files, as an integrity manifest. It must never be counted as captured
evidence.

---

## 5. Required Preservation Method

When (and only when) separately authorized for execution, the preservation must:

1. Reverify all three source hashes before copying; each must match section 3 exactly.
2. Create only the approved SID-specific destination directory. No other directory.
3. Copy the three files without transforming their contents.
4. Do not pretty-print, normalize, reserialize, re-encode, redact, truncate, or
   rewrite any raw artifact.
5. Preserve the exact filenames listed in section 4.
6. Generate SHA256SUMS only after copying, from the destination files.
7. Recompute destination hashes independently.
8. Compare each destination hash to its accepted source hash.
9. Require source-to-destination byte comparison using `cmp -s`.
10. Stop immediately if any source hash, destination hash, filename, byte
    comparison, or file count differs.
11. Do not delete the /tmp originals during the preservation operation.
12. Do not perform any live request, runner execution, SID creation, or Flask restart.

---

## 6. Authority Boundaries

Evidence acceptance
!=
Evidence preservation
!=
Execution authorization
!=
Project-status movement

Preservation must NOT:

- reopen or repeat E-2
- create another SID
- change the accepted result
- strengthen the result beyond LIMITED TECHNICAL ACCEPTED
- establish repeatability
- establish inventor development
- establish improved understanding
- establish idea growth
- establish Stage 3 completion
- set runtime_integrated=true
- release R2
- unblock FORM T
- classify S-6
- unblock AA-5

Preservation makes the reviewed bytes durable. It adds nothing to their meaning.

---

## 7. Chain of Custody

The preservation operation, when executed, must record:

- the execution SID: d39526ce-92a5-469a-9c93-5e6d23f7a31b
- the source /tmp paths (section 3)
- the destination paths (section 4)
- source hashes (reverified immediately before copy)
- destination hashes (recomputed independently after copy)
- byte-comparison results (cmp -s for each file)
- repository baseline before preservation (must be aef888e, clean tree)
- repository state after copying (untracked destination files only)
- the evidence acceptance record commit: d130256
- the roadmap baseline: aef888e

Custody notes:

- The files were copied AFTER evidence acceptance, not captured directly into Git
  during execution. The original capture was to /tmp during the authorized run.
- Git preservation makes the reviewed bytes durable but does not retroactively alter
  their original capture context. The bytes preserved are the same bytes that were
  reviewed and accepted; Git does not and cannot certify the original /tmp capture
  process itself.

---

## 8. STOP Conditions

Any of the following requires immediate halt:

- source file missing
- source hash mismatch
- unexpected source filename
- destination already exists
- destination directory contains unexpected files
- copy failure
- destination hash mismatch
- cmp failure
- manifest mismatch
- repository baseline mismatch
- working tree not clean before preservation
- any attempt to edit or normalize evidence

On STOP:

- Do not stage or commit.
- Preserve all outputs.
- Do not repair within the same operation.
- Return to owner review.

---

## 9. Proposed Preservation Sequence (proposed, NOT executed by this draft)

  Verify clean HEAD == origin/main
  Reverify source files and hashes
  Create SID-specific destination directory
  Copy exactly three raw files
  Verify destination hashes
  Verify byte identity using cmp
  Generate SHA256SUMS
  Verify exactly four destination files
  Review repository diff and status
  Return for owner review

---

## 10. Final Determination

E-2 RAW EVIDENCE PRESERVATION:
PROPOSED -- NOT YET AUTHORIZED FOR EXECUTION

No evidence copy, staging, commit, push, deletion, or project-status movement is
authorized by this draft.

---

## 11. Critical Analysis

### Assumptions

- The three /tmp files are the exact byte sequences reviewed and accepted under
  record d130256, evidenced by hash equality.
- The Codespace filesystem has not silently altered the files between acceptance and
  the eventual preservation run. Hash reverification immediately before copy is the
  guard against this.

### Hidden Assumptions

- It is assumed that `cmp -s` and `sha256sum` in this environment behave correctly.
  Two independent integrity checks (hash equality and byte comparison) are required
  to reduce reliance on any single tool.
- It is assumed the destination directory does not already exist. The method requires
  STOP if it does, to avoid silent overwrite.

### Alternative Preservation Approaches

- A single combined archive (tar) could preserve the three files together, but would
  obscure per-file byte identity and complicate independent verification. Per-file
  copy with a manifest is preferred for transparency.
- Embedding the evidence as base64 inside a Markdown record was considered and
  rejected: it would re-encode the bytes and break byte-identity verification.

### How Preservation Could Falsely Appear Successful

- If both source and destination were corrupted identically, hashes would match yet
  not reflect the original capture. This is mitigated by reverifying against the
  accepted hashes recorded at execution time, not against freshly computed values.
- If the manifest were generated from the source rather than the destination, it
  could mask a copy error. The method requires generating SHA256SUMS from the
  destination after copy.

### Evidence That Would Invalidate the Preservation

- Any destination hash differing from its accepted source hash.
- Any `cmp -s` returning nonzero.
- A destination file count other than four (three artifacts + SHA256SUMS).
- A repository baseline other than aef888e at the time of preservation.

### Red-Team Critique

Matching hashes strongly support byte identity but do not prove the original /tmp
capture process independently.

Git preservation protects the reviewed bytes from environment loss, but does not
prove general E-2 repeatability.

The HTML files may contain environment-specific or debug-generated content; they
must be preserved unchanged rather than interpreted as product evidence.

The transcript contains inventor-response content and must not be promoted into
claims about inventor development.
