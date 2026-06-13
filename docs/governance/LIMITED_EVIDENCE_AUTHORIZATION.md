# LIMITED EVIDENCE AUTHORIZATION — E-1 / E-2 / E-3

## 1. Status and scope

- AUTHORIZATION DOCUMENT ONLY. Authorizes exactly E-1, E-2, E-3.
  Nothing else.
- Source: POST_PHASE_2_AUTHORIZATION_REVIEW.md (`7a3350c`) §9–§10;
  roadmap §7 at `ad49fe1`.
- Evidence collection may begin ONLY AFTER this document is
  committed AND the required strict-compliance roadmap refresh is
  committed as a separate governance-only commit. Evidence execution
  baseline is the verified clean HEAD after that roadmap refresh.
- E-2 execution is additionally blocked until a separately committed
  and owner-authorized `E2_OPERATIONAL_PROCEDURE.md` exists (§6.3).
  This document authorizes the E-2 evidence objective and acceptance
  boundaries only — not E-2 execution.

## 2. Baseline and preconditions

- Authoring baseline: `ad49fe1` — the HEAD at which this document
  was drafted.
- Authorization commit baseline: the HEAD produced by committing
  this document (assigned at commit time; recorded in roadmap
  refresh).
- Evidence execution baseline: the verified clean HEAD after the
  required strict-compliance roadmap refresh commit. Evidence must
  not run against a stale or dirty tree.
- Precondition before each evidence item: `git status --short`
  returns empty. Any dirty tree or HEAD mismatch: STOP.

## 3. Execution order (mandatory)

Steps 1–3 may begin only after the evidence execution baseline is
confirmed (this document committed + roadmap refreshed + clean tree
verified):

1. E-3 first — read-only recovery; constrains E-2 understanding.
2. E-1 — gate re-run.
3. E-2 — one smoke session; BLOCKED pending separately committed
   `E2_OPERATIONAL_PROCEDURE.md` (§6.3); do not attempt before
   that document is committed and owner-authorized.
4. E-3 and E-1 evidence artifacts assembled and committed together
   as one governance-only evidence commit; reviewed by owner.
5. E-2 evidence committed separately, only after E-2 is unblocked
   and executed.
6. No roadmap or status movement occurs automatically after either
   evidence commit.

## 4. E-3 — Integration-plan evidence recovery

### 4.1 Objective
Recover verbatim Phase 3 and Phase 4 text from the committed
integration plan. Establish what the flag-flip process actually
requires so that no downstream authorization misrepresents it.

### 4.2 File
`docs/governance/PATH_N_RUNTIME_INTEGRATION_AUTHORIZATION_PLAN.md`
(established by commit `d2b2a9a`).

### 4.3 Commands (read-only; run only after evidence execution
baseline is confirmed)

    git show --stat --oneline d2b2a9a
    sed -n '90,175p' docs/governance/PATH_N_RUNTIME_INTEGRATION_AUTHORIZATION_PLAN.md

### 4.4 Committed Phase 3 and Phase 4 summary (from committed plan §6 table)

- Phase 3: runtime test suite committed and green; touches `tests/`
  only; gate is owner review of full results.
- Phase 4: eligibility for `runtime_integrated` metadata update
  after approved runtime tests pass. The actual flag change
  requires: (a) separate owner authorization; (b) JSON metadata
  update; (c) re-testing; (d) recorded re-approval. Nothing
  automatic. No phase may be merged with another.

### 4.5 Acceptance
Phase 3 and Phase 4 text recovered verbatim and legible in
terminal output. Confirms E-2 is limited supplemental live runtime
smoke evidence — it does not constitute Phase 3 and cannot satisfy
Phase 3, and does not make `runtime_integrated=true` eligible.

### 4.6 Evidence artifact
E-3 evidence is terminal-output evidence only until owner review.
The owner pastes the full output of the §4.3 commands into the
session. After owner review and explicit instruction, a
`docs/governance/evidence/E3_INTEGRATION_PLAN_PHASE_3_4_EXCERPT.md`
artifact may be assembled from that pasted output and committed as
part of the E-3/E-1 evidence commit. No artifact is created before
the owner reviews the terminal output.

## 5. E-1 — Gate re-run at evidence execution baseline

### 5.1 Objective
Re-run the four Phase 2 gate commands at the evidence execution
baseline HEAD. Confirms Phase 2 green state persists. No code
changes.

### 5.2 HEAD capture (read-only; run immediately before E-1 commands)

    git log --oneline -1

The short hash from this output is used as the artifact filename
suffix. Do not hardcode a hash.

### 5.3 Commands (verbatim from `b3a5fba` §10;
run only after evidence execution baseline is confirmed)

    pytest tests/test_phase2_path_n_selection.py -q
    pytest tests/test_phase1_path_designation.py -q
    pytest tests/test_web_app.py -q
    pytest tests/test_wps001_invariants.py tests/test_path_n_content_config_artifact.py tests/test_non_specialist_questioning_policy.py -q

### 5.4 Accepted results
Per closure record (`ffaab93`) §4 (warnings accepted):

- Phase 2 selection suite: 10 passed, 1 warning
- Phase 1 designation suite: 7 passed, 1 warning
- Web app suite: 2 passed, 1 warning
- Final governance gate: 34 passed, 1 skipped, 1 xfailed, 3 warnings

Any deviation: STOP.

### 5.5 Evidence artifact
`docs/governance/evidence/E1_GATE_RERUN_<short-HEAD>.txt`
where `<short-HEAD>` is the hash captured in §5.2.
Full terminal output of all four commands, appended via `tee`.
Committed with E-3 artifact in the first evidence commit.

## 6. E-2 — One internal Path N runtime smoke session

### 6.1 Objective
Obtain limited supplemental live runtime smoke evidence that Path
N-designated sessions serve approved N-* artifact content outside
pytest. Confirms `state.path == "N"` is carried and consumed
end-to-end in the live web interface.

### 6.2 What E-2 is NOT
- NOT R2 (the ILT-002 water-leak idea re-run).
- NOT FORM T.
- NOT an S-6 classification run.
- NOT inventor-outcome evidence (SR-001 measurement).
- NOT Phase 3 (which requires a committed runtime test suite,
  not a manual smoke session, per `d2b2a9a` §6 table).
- NOT evidence that makes `runtime_integrated=true` eligible alone
  or in combination with E-1/E-3.

### 6.3 Operational procedure gate — E-2 EXECUTION BLOCKED

No committed operational procedure content has yet been verified
for the required E-2 invocation steps:
(a) starting the Flask server in the Codespace environment;
(b) submitting the idea via POST to
    `/start_ilt002_combination_lock_path_n`;
(c) extracting the SID from the Location redirect header;
(d) submitting iteration responses via POST to `/session/<sid>`;
(e) the authorized number of smoke iterations;
(f) retrieving `/tmp/ilt002_transcript_<sid>.jsonl`.

Committed `web/app.py` confirms routes, form fields, SESSION_STORE
structure, and transcript disk path. This document authorizes the
E-2 evidence objective and acceptance boundaries defined in
§6.4–§6.5 only. E-2 execution is not authorized by this document.
E-2 execution requires a separately committed and owner-authorized
`E2_OPERATIONAL_PROCEDURE.md` specifying items (a)–(f) from a
committed or owner-verified source.

### 6.4 Evidence to preserve (governs what E2_OPERATIONAL_PROCEDURE
must capture once unblocked)

- Session ID (UUID).
- Full question sequence as served, per iteration.
- `state.path` value confirmed as `"N"` throughout.
- Transition, gap type/status, and maturity level per iteration.
- Complete transcript artifact from
  `/tmp/ilt002_transcript_<sid>.jsonl`.

### 6.5 Acceptance criteria (governs E2_OPERATIONAL_PROCEDURE
and the eventual E-2 evidence commit)

(a) Every Stage 2 gap question served matches a `text` entry in
    the approved artifact
    (`docs/governance/path_n_content_config/
    electronics_electrical_path_n_questions.json`) byte-for-byte.
(b) Transitions, gaps, and maturity progress per deterministic
    engine rules; no gate anomaly.
(c) `state.path == "N"` confirmed in session state.

### 6.6 Evidence artifacts (created only after E-2 is unblocked
and executed)

`docs/governance/evidence/E2_PATH_N_SMOKE_SESSION_<SID>.md`
— session metadata, question sequence, state trace.
`docs/governance/evidence/E2_TRANSCRIPT_<SID>.jsonl`
— raw transcript from `/tmp/ilt002_transcript_<sid>.jsonl`.
Committed in a separate evidence commit from E-3/E-1.

## 7. Evidence commits

- First evidence commit (E-3 and E-1 only): committed after owner
  review of E-3 terminal output and E-1 gate output. Commit
  message: `evidence: E-3 integration plan recovery and E-1 gate
  re-run results`.
- Second evidence commit (E-2 only): committed separately, only
  after E-2 is unblocked by committed `E2_OPERATIONAL_PROCEDURE.md`
  and executed. Commit message: `evidence: E-2 Path N smoke
  session results`.
- No existing file is modified by either evidence commit.
- No automatic roadmap or status movement after either commit.

## 8. STOP conditions

1. Dirty tree or HEAD mismatch before any step.
2. Roadmap refresh not yet committed when evidence execution is
   attempted.
3. E-3 file absent at the recorded path or Phase 3/4 sections
   missing.
4. E-1 output deviates from §5.4 in any count or result type.
5. E-2 attempted before `E2_OPERATIONAL_PROCEDURE.md` is committed
   and owner-authorized — this is a hard gate, not a warning.
6. E-2 serves any Stage 2 question not byte-matching the approved
   artifact, or any gate anomaly appears.
7. E-2 transcript missing or empty after session.
8. Any announced evidence arrives empty or truncated.
9. Any pressure to treat E-2 as Phase 3 completion, or as making
   `runtime_integrated=true` eligible without the full Phase 4
   process (`d2b2a9a` §6: separate authorization, JSON metadata
   update, re-testing, recorded re-approval).

## 9. Rollback / no-mutation statement

E-1 and E-3 are read-only. E-2 creates only runtime session state
and evidence artifacts; no committed file is mutated. Each evidence
commit adds new files only; rollback = revert that commit. No
existing file is modified by any action authorized here.

## 10. Non-authorizations

No code modification. No test modification. No approved content
artifact mutation. No `domain.json` change. No
`runtime_integrated=true`. No R2. No FORM T movement. No S-6
classification. No AA-5. No Path T. No Professional Workspace.
No Stage 4–7 expansion. No xfail conversion. No evidence collection
before this document and its roadmap refresh are committed. No E-2
execution before `E2_OPERATIONAL_PROCEDURE.md` is separately
committed and owner-authorized. No automatic roadmap or status
movement after either evidence commit.
