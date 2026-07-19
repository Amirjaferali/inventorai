# D13-TKP-PKG-001 — Limited Phase A Operational Start Authorization Proposal

**Proposal ID:** `D13-TKP-PKG-001-PHASE-A-START-PROP-001`
**Proposed (reserved) future start-authorization ID:** `D13-TKP-PKG-001-PHASE-A-START-AUTH-001`

**Status:**
PROPOSED · NOT CANONICAL · OWNER REVIEW REQUIRED · NO START AUTHORIZATION ISSUED · GATE 3A OPERATIONAL ACTIVATION NOT EFFECTIVE · PHASE A NOT STARTED · PHASE B INACTIVE / NOT AUTHORIZED · PHASE A BRANCH CREATED BUT NOT AUTHORIZED FOR USE · WORKSPACE NOT CREATED · EVIDENCE-STORAGE PATH NOT CREATED · OPERATIONAL WINDOW NOT STARTED · JOURNEY DATA EXCLUDED · NO RESEARCH METHOD ACTIVATED · NO RESEARCH EXECUTION AUTHORIZED

## 1. Status and purpose
This is a governance-only proposal describing the exact terms under which the owner **could later** issue a single explicit authorization to start a limited, read-only Phase A. It is proposal-only: it starts nothing, creates nothing, uses nothing, and activates nothing. It does not operationally activate Gate 3A, does not begin Phase A or Phase B, does not create or use the Phase A branch/workspace/evidence path, does not start the operational window, and issues no start authorization. Its function is to let the owner review and approve the complete operational terms in one place, and reserve the future start-authorization identity, before a separate start decision.

## 2. Governing identities
- **Package ID:** `D13-TKP-PKG-001` (canonical `0.1-proposed`, PR #209).
- **Gate 3 authorization ID:** `D13-TKP-PKG-001-G3-ISS-001` (CANONICAL / OWNER-ISSUED, PR #210; effective 2026-07-18; expires 2026-10-16 23:59 Asia/Kuwait).
- **Gate 3A proposal ID:** `D13-TKP-PKG-001-G3A-PROP-001` (CANONICAL, PR #211).
- **Gate 3A owner decision ID:** `D13-TKP-PKG-001-G3A-ACT-001-PHASE-A` (CANONICAL / OWNER-ISSUED / NOT OPERATIONALLY STARTED, PR #211).
- **Phase A prerequisite proposal ID:** `D13-TKP-PKG-001-PHASE-A-PREREQ-PROP-001` (CANONICAL, PR #212).
- **Phase A prerequisite owner decision ID:** `D13-TKP-PKG-001-PHASE-A-PREREQ-DEC-001` (CANONICAL / OWNER-APPROVED, PR #212).
- **This proposal ID:** `D13-TKP-PKG-001-PHASE-A-START-PROP-001`.
- **Reserved future start-authorization ID:** `D13-TKP-PKG-001-PHASE-A-START-AUTH-001`.

## 3. Canonical basis
Subordinate to and consistent with, and amending none of: the Gate 3 authorization (§§4–20, incl. §10 prerequisites, §20 termination cascade); the Phase-A-only Gate 3A proposal and owner decision; the Phase A prerequisite proposal (§§1–25) and its owner decision (thirteen decisions); the package definition; the no-candidate/no-appointment decision; Gate 2 (§4 phases, §5 sources, §6 authority, §8 Domain Registry read-only isolation); the Research Contract; the technology-first guidance and Structured Technical Guidance Output Model; the TKP clarification; `MVP_SCOPE_FREEZE` (ACTIVE FREEZE, LEVEL 0–2, electronics/electrical); and `CLAUDE.md`.

## 4. Current lifecycle state
- Phase A prerequisite proposal: **CANONICAL** (PR #212).
- Phase A prerequisite owner decision + thirteen decisions: **CANONICAL / OWNER-APPROVED** (PR #212).
- Phase A branch `research/d13-tkp-pkg-001-phase-a-read-only-analysis`: **CREATED / IDENTITY ESTABLISHED / NOT AUTHORIZED FOR USE / NO PHASE A START AUTHORITY**.
- Gate 3A operational activation: **NOT EFFECTIVE**.
- Phase A: **NOT STARTED**. Phase B: **INACTIVE / NOT AUTHORIZED**.
- Workspace and evidence-storage paths: **NOT CREATED / NOT AUTHORIZED FOR USE**.
- Operational window: **NOT STARTED / NO DATES FIXED**.
- Post-recording Phase A start authorization: **NOT ISSUED**. Research execution: **NOT AUTHORIZED**.

## 5. Non-authorization statement
This proposal authorizes nothing. It does not activate Gate 3A; does not start Phase A or Phase B; does not authorize use of the Phase A branch; does not create or use the workspace or evidence-storage path; does not start the operational window; does not fix any timestamp; does not access journey, personal, production, or external data; retrieves no datasheet; executes no DOCUMENT REVIEW or DATASHEET COMPARISON; researches or answers no RQ; performs no calculation, measurement, test, simulation, or external technical validation; produces no engineering conclusion; begins no architecture, circuit design/sizing, RED, implementation, integration, or Workstream 8; and performs no candidate or appointment activity. Owner review or approval of this proposal is not a start authorization.

## 6. Existing Phase A branch
The branch identity `research/d13-tkp-pkg-001-phase-a-read-only-analysis` now exists locally and remotely at tip `c960b29cdd5d531a5d298aa9a2bfe46703cb2dbf`. Its status is **CREATED · IDENTITY ESTABLISHED · NOT AUTHORIZED FOR USE · NO PHASE A START AUTHORITY**. Existence of the branch confers no authority to check it out for work, commit to it, create the workspace inside it, or perform any analysis. Use requires the separate future start authorization (§25, step 7). If the authoritative branch advances beyond `c960b29c` before the start authorization is issued, the branch and lock must be re-verified against the then-current authoritative state, and any divergence is a stop condition.

## 7. Repository-state lock (to be fixed by the future start authorization)
The future start authorization `D13-TKP-PKG-001-PHASE-A-START-AUTH-001` must fix and contemporaneously record exactly:

| Lock field | Value |
|---|---|
| Authoritative branch | `feature/atomic-json-session-persistence` |
| Authoritative commit | `c960b29cdd5d531a5d298aa9a2bfe46703cb2dbf` |
| Authoritative tree | `e1c7c898e6834ed13bdc7bd72e19983dac1966f9` |
| Ordered parents | `669bfe3ce7a4b65cca4a3e9c41f36e92b0370073`, `fa7929375cf5fb28d5f70fb7f1095721cc45275e` |
| Phase A branch | `research/d13-tkp-pkg-001-phase-a-read-only-analysis` |
| Phase A branch starting commit | `c960b29cdd5d531a5d298aa9a2bfe46703cb2dbf` |
| Workspace path | `research/d13-tkp-pkg-001/phase-a/` |
| Evidence-storage path | `research/d13-tkp-pkg-001/phase-a/evidence/` |
| Start-authorization ID | `D13-TKP-PKG-001-PHASE-A-START-AUTH-001` |
| Operational start | NOT YET FIXED |
| Operational end | NOT YET FIXED |

Any mismatch between this lock and the actual repository state — before or during Phase A — immediately stops Phase A (§20). If the authoritative branch has advanced when the owner issues the start authorization, the lock must be re-fixed to the then-current re-verified state before any activity, and the Phase A branch must be confirmed to descend from that state.

## 8. Recommended operational window
Recommended operational period: **14 calendar days**. The period must:
- begin **only** when the owner later issues the explicit start authorization;
- use an **exact start timestamp and exact end timestamp in Asia/Kuwait**, fixed in that separate start authorization (§25, step 7);
- **not** begin from proposal drafting, review, recording, merge, branch creation, workspace preparation, or any implied event;
- end **no later than 14 calendar days** after the owner-issued start;
- end **no later than Gate 3 expiration, 2026-10-16 23:59 Asia/Kuwait** (if fewer than 14 days remain at start, the window ends at Gate 3 expiration);
- **terminate immediately** if Gate 3 or Gate 3A is suspended, invalidated, revoked, or expires;
- require a **new owner decision** for any extension.

**START TIMESTAMP: NOT YET FIXED — OWNER DECISION REQUIRED.**
**END TIMESTAMP: NOT YET FIXED — OWNER DECISION REQUIRED.**
(No actual start timestamp is invented here.) This 14-day recommendation is within, and narrower than, the ≤30-day maximum approved in prerequisite Decision 4; it does not amend that maximum.

## 9. Allowed internal inputs (after a separate owner start authorization only)
Read-only: repository files at the locked authoritative commit `c960b29c`; canonical governance and product documentation; existing field definitions; existing application-state structures, read-only. No input may be treated as authorization to mutate it. **Not authorized:** external-source access; web research; datasheet retrieval; vendor APIs; paid or restricted sources; confidential or uncertain-access sources; new user outreach; candidate or appointment activity; and journey/personal/production data (§10).

## 10. Journey-data exclusion
**JOURNEY-DATA ACCESS EXCLUDED FROM INITIAL PHASE A — NOT VERIFIED — SEPARATE OWNER DECISION REQUIRED.** Availability is not assumed. Initial Phase A proceeds on repository and governance/product documentation only. No personal or production user data may be accessed. Journey data may enter scope only through a separate owner decision preceded by lawful-access, privacy, security, and data-minimization confirmation. Any emergent need for journey, personal, or production data during Phase A is a stop condition (§20).

## 11. Workspace and evidence paths
The future start authorization may permit creation of exactly two directories inside the approved Phase A branch:
- `research/d13-tkp-pkg-001/phase-a/`
- `research/d13-tkp-pkg-001/phase-a/evidence/`

The proposal makes clear that: they **do not exist now**; **this drafting task does not create them**; they may be created **only after** the future explicit owner start authorization; they are **documentation and analysis paths only**; creation of the directories does **not** authorize substantive analysis beyond the fixed Phase A scope; and **no** application code, prompts, schemas, databases, UI, tests, configuration, persistence, production state, or Domain Registry files may be created or modified there. Creating the workspace/evidence structure after a later start authorization is an **administrative precondition** for Phase A, not application implementation.

## 12. Initial administrative file structure (recommended; not created)
Recommended layout (identities only — nothing is created by this proposal):
```
research/d13-tkp-pkg-001/phase-a/
  README.md
  repository-state-lock.md
  session-log.md
  stop-condition-log.md
  unresolved-issues.md
  evidence/
    field-coverage-map.md
    missing-field-list.md
    capability-gap-list.md
    unverified-proposed-rq-manifest.md
    analysis-provenance.md
    completion-attestation.md
```
Purpose of each file:
- **README.md** — scope statement, identities (package, Gate 3, Gate 3A decision, prerequisite decision, reserved start-authorization ID), the fixed four-output limit, and the non-authorization boundary; orientation only.
- **repository-state-lock.md** — the §7 lock record (branch, commit, tree, ordered parents, Phase A branch + starting commit, workspace/evidence paths, window start/end, start-authorization ID) as fixed at start.
- **session-log.md** — append-only per-session entries: session identity, timestamp, files inspected, limitations/contradictions/abstentions, pre/post clean-tree confirmation.
- **stop-condition-log.md** — append-only record of any triggered stop condition and the escalation taken.
- **unresolved-issues.md** — append-only list of open questions/ambiguities carried to independent review.
- **evidence/field-coverage-map.md** — substantive output 1 (§13.1 schema).
- **evidence/missing-field-list.md** — substantive output 2 (§13.2 schema).
- **evidence/capability-gap-list.md** — substantive output 3 (§13.3 / §14 schema).
- **evidence/unverified-proposed-rq-manifest.md** — substantive output 4 (§13.4 schema).
- **evidence/analysis-provenance.md** — the §17 provenance record for every output.
- **evidence/completion-attestation.md** — the §22 completion-criteria attestation, created only when/if Phase A is later declared complete.

The README and administrative control files (`repository-state-lock.md`, `session-log.md`, `stop-condition-log.md`, `unresolved-issues.md`, `analysis-provenance.md`, `completion-attestation.md`) are governance/administrative records and **do not expand** the four-substantive-output limit.

## 13. Four substantive outputs
Phase A remains limited to read-only internal analysis producing **only**:
1. **field-coverage map** — per field: identifier; current location; user journey stage; present/absent status; data type; required/optional state; validation state; downstream dependency; evidence reference; limitation.
2. **missing-field list** — per item: missing field; affected journey stage; why needed; information currently unavailable; consequence of absence; whether absence blocks a future RQ; proposed acquisition method; authorization required; status.
3. **capability-gap list** — per §14 schema.
4. **unverified proposed research-question manifest** — per item: proposed RQ ID; exact question; originating capability gap; required evidence; suggested method; current authorization status; whether it fits RQ-01…RQ-11; whether it requires a proposed addition; owner-decision dependency; status = **`UNVERIFIED PROPOSED RQ — NOT AUTHORIZED FOR RESEARCH`**.

**No additional output may arise by implication.** No proposed RQ enters the authorized set automatically (Gate 3 §4: PROPOSED ADDITION — OWNER DECISION REQUIRED).

## 14. Capability-gap schema
Every capability-gap record must identify: the exact unresolved technical subproblem; the affected user outcome; missing information or evidence; what InventorAI can currently verify; what InventorAI cannot currently verify; the precise technology, research topic, or subdomain; suggested search terms; required validation, measurements, documents, tests, or tools; uncertainty or abstention; specialist category only when necessary; **no named person or company**. This output identifies **future needs only**. It does **not** authorize the suggested research, testing, validation, specialist involvement, or implementation.

## 15. Proposed-RQ boundary
Every proposed research question produced in Phase A is **`UNVERIFIED PROPOSED RQ — NOT AUTHORIZED FOR RESEARCH`**. Proposing an RQ authorizes no research, no source access, and no method execution. Whether a proposed RQ maps to the existing authorized set (RQ-01…RQ-11) or requires a proposed addition is recorded as a question for a **separate** owner decision; nothing is added to the authorized research set by drafting or by Phase A output.

## 16. Session controls
For every future Phase A session (all read-only, within the fixed window):
1. verify authoritative commit and tree; 2. verify Phase A branch; 3. verify workspace and evidence paths; 4. verify operational window remains valid; 5. verify Gate 3 and Gate 3A remain valid; 6. verify journey data remains excluded; 7. verify no external source or datasheet access; 8. verify clean tracked working state **before** analysis; 9. record session identity and timestamp; 10. record exact files inspected; 11. record limitations, contradictions, and abstentions; 12. verify no prohibited mutation occurred; 13. verify clean tracked working state **after** the session; 14. append the session result and stop-condition status.

Unrelated pre-existing untracked local files must not be staged, modified, deleted, relied upon, or represented as Phase A evidence.

## 17. Provenance requirements
Every Phase A output must carry: package ID; Gate 3 ID; Gate 3A decision ID; Phase A prerequisite proposal ID; Phase A prerequisite decision ID; future start-authorization ID; authoritative commit inspected; exact file reference; date and time (Asia/Kuwait); analyst/session identity; activity type; scope; limitations; contradictions; abstention marker; no-external-source attestation; no-method-execution attestation; no-state-mutation attestation. Append-only where practical; any non-append-only exception must be documented with justification in the provenance record.

## 18. Permitted future repository changes
After a separate owner start authorization only, repository changes are permitted **exclusively** under `research/d13-tkp-pkg-001/phase-a/`. Those changes must be: documentation and analysis records only; package-specific; provenance-linked; append-only where practical; committed **only** to the Phase A branch `research/d13-tkp-pkg-001-phase-a-read-only-analysis`; and reviewed before any merge proposal. **No Phase A artifact may be merged automatically.** No change may touch any path outside the workspace.

## 19. Prohibited activity
Explicitly prohibited: external-source access; datasheet retrieval or comparison; DOCUMENT REVIEW; DATASHEET COMPARISON; research or answering any RQ; calculations; measurements; tests; simulations; external technical validation; engineering conclusions; architecture; circuit selection, design, or sizing; RED; implementation; integration; Workstream 8; AI Coach; schema/prompt/database/UI/test/configuration/application-code/production-state/persistence/Domain Registry mutation; journey/personal/production-data access; candidate search, identification, screening, ranking, outreach, selection, or appointment; interference with PR #167 or PR #162; scope expansion.

## 20. Stop conditions
All canonical stop conditions (prerequisite proposal §15; Gate 3 §20) apply, and Phase A must additionally suspend immediately for: repository-state-lock mismatch; authoritative-branch advancement after the lock; Phase A branch mismatch or unexpected commit; unapproved workspace or evidence path; start- or end-timestamp ambiguity; expired operational window; missing session provenance; unexpected tracked mutation; attempted staging of unrelated files; journey-data need; personal- or production-data exposure; external-source or datasheet need; method-execution need; RQ research or answer generation; engineering-conclusion need; Phase B content; candidate or appointment activity; architecture, RED, implementation, integration, or Workstream 8; confidentiality, lawful-access, privacy, or data-minimization uncertainty. Any trigger suspends activity immediately and requires owner escalation; no authority survives a stop condition by implication.

## 21. Suspension and termination
Gate 3A terminates immediately if Gate 3 expires or is suspended, invalidated, or revoked; the operational window terminates with it. On termination every capability ceases at once and no analysis may continue. Reactivation requires a **new** explicit owner decision. No authority survives termination by implication.

## 22. Completion boundary
Phase A cannot later be declared complete unless **all** canonical completion criteria (prerequisite proposal §17) are satisfied: the four approved outputs; complete provenance; repository-state-lock record; start-authorization identity; operational-window compliance; required attestations (no-external-source, no-method-execution, no-state-mutation, no-candidate/no-appointment, no-implementation); stop-condition log; unresolved-issue list; owner-readable summary; and readiness for non-authoring independent governance review. Completion does **not** authorize Phase B, research, architecture, implementation, integration, Workstream 8, or any production mutation.

## 23. Independent-review boundary
The Phase A completion record must receive a **non-authoring** independent governance review before any later Phase B owner decision. The reviewer must not have authored, materially edited, controlled, or predetermined the Phase A completion record, this start proposal, or the prerequisite proposal. Independence failure → `INDEPENDENCE FAILURE — RE-REVIEW REQUIRED`. Governance review is not technical certification, and a later separate owner decision remains required regardless of review outcome.

## 24. Owner approvals required and future-ID reservation
Section 24 contains **fourteen owner approvals of operational terms** and **one reservation of the future start-authorization identity**. These are fifteen items in total, but they are **not** fifteen issued operational decisions: fourteen approve operational terms, and the fifteenth reserves an identity and issues nothing. Approving these items starts no operational window, activates Gate 3A in no way, authorizes no branch/workspace/evidence use, and issues no start authorization.

**Fourteen operational-term approvals:**
1. approve the 14-calendar-day operational period;
2. approve that the operational window's exact **start** timestamp is fixed only in the separate future start authorization (§25, step 7), not during proposal or owner-decision approval;
3. approve that the operational window's exact **end** timestamp is fixed only in the separate future start authorization (§25, step 7), not during proposal or owner-decision approval;
4. approve the complete repository-state lock (§7);
5. approve that use of the already-created Phase A branch is permitted only under the separate future start authorization;
6. approve that creation and use of the workspace path is permitted only under the separate future start authorization;
7. approve that creation and use of the evidence-storage path is permitted only under the separate future start authorization;
8. confirm journey data remains excluded;
9. approve the allowed internal inputs;
10. approve the initial administrative file structure;
11. approve the session-control protocol;
12. approve permitted future repository changes under the workspace;
13. approve all stop conditions;
14. approve the Phase A completion and review boundary.

**One reservation of the future start-authorization identity:**

15. approve and reserve the future start-authorization ID:

    `D13-TKP-PKG-001-PHASE-A-START-AUTH-001`

    The ID is reserved only.

    No start authorization is issued by approving this proposal, by recording the proposal, or by recording the owner decision on the preceding fourteen terms.

**No start authorization is issued by approving these terms, by recording the proposal, or by recording the owner decision.** The fourteen approvals fix operational terms only; item 15 reserves an identity only. The complete §7 repository-state lock is carried by the **separate future start authorization** (§25, steps 6–7), not by any §24 item. No item may be satisfied by implication.

## 25. Recommended next step
1. author review of this complete proposal;
2. non-authoring independent governance review;
3. correction integration and targeted re-review if required;
4. owner approval of the fourteen operational terms and reservation of the future start-authorization ID;
5. governance-only canonical recording of the proposal and owner decision, with Phase A still **NOT STARTED**;
6. re-verification of the complete repository-state lock and all prerequisite checklist items;
7. only then, a separate explicit owner issuance of:

   `D13-TKP-PKG-001-PHASE-A-START-AUTH-001`

   containing the exact operational start and end timestamps.

Phase A begins only at the exact effective timestamp stated in that separate owner-issued authorization.

## 26. Final non-execution statement
This proposal performs nothing. It creates no branch, workspace, evidence-storage path, file, or record; uses no branch; accesses no journey, personal, production, or external data; retrieves no datasheet; executes no method; researches or answers no RQ; performs no calculation, measurement, test, simulation, or external technical validation; mutates no application/schema/prompt/database/UI/test/configuration/persistence/production/Domain-Registry state; identifies or appoints no candidate; begins no architecture, RED, implementation, integration, or Workstream 8; touches no PR. Gate 3A operational activation is **NOT YET EFFECTIVE**; Phase A is **NOT STARTED**; Phase B is **INACTIVE / NOT AUTHORIZED**; the post-recording Phase A start authorization is **NOT ISSUED**; the future start-authorization identity is **RESERVED ONLY**.
