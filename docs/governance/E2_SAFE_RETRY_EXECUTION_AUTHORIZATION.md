# E2_SAFE_RETRY_EXECUTION_AUTHORIZATION.md
# Gate C -- E-2 Safe Retry Execution Authorization
# Status: PROPOSED DRAFT -- NOT YET EFFECTIVE

---

## 1. Record Identity and Authority

Record type: Gate C Execution Authorization -- DRAFT
Gate B closure: `2a33763` -- Gate B implementation CLOSED
Authoritative baseline HEAD: `b5701ab83c40035099bfb7b3fff3276be1030148`
Draft prepared after: Post-Gate-B Authorization Review (Determination A)

### Authority chain (subordinate to all of the following)

- ILT-002_GOVERNANCE_ANCHOR.md
- PATH_N_CURRENT_EXECUTION_ANCHOR.md
- DUAL_PATH_PRODUCT_ANCHOR.md
- ACTIVE_EXECUTION_ROADMAP.md
- E2_SAFE_RETRY_DESIGN_AUTHORIZATION.md
- E2_SAFE_RETRY_IMPLEMENTATION_AUTHORIZATION.md
- E2_SAFE_RETRY_IMPLEMENTATION_CLOSURE_RECORD.md
- E2_OPERATIONAL_PROCEDURE.md
- Prior STOP incident committed at a684aba

Any conflict between this document and the above sources is
resolved in favour of those sources.

---

## 2. Scope and Explicit Exclusions

### In scope

Gate C authorizes one tightly controlled E-2 safe-retry execution
attempt using the committed runner against a newly created Path N
session.

### Explicitly excluded

- Any execution of the denied prior SID 830054a4-f9cb-43fb-ab1c-f5d5f3cfb314
- Any user-supplied SID
- Any second attempt without a new authorization
- Any code, test, artifact, or domain.json modification
- Any claim about inventor development or idea growth
- Any automatic status movement
- runtime_integrated=true
- R2 release, FORM T unblocking, S-6 classification, AA-5 unblocking
- Any subsequent gate (each requires separate authorization)

---

## 3. Authoritative Baseline

HEAD / origin/main: b5701ab83c40035099bfb7b3fff3276be1030148

Gate B: COMPLETE
B-1 matcher:     654ce07
B-2 runner:      d12db64
B-2 mode fix:    d631439
B-3 closure:     2a33763
B-4 roadmap:     b5701ab

E-2 STOP:           DECLARED AND RECORDED (a684aba)
E-2 retry:          NOT AUTHORIZED until this document is committed
runtime_integrated: false
R2:                 HELD
FORM T:             BLOCKED
S-6:                UNCLASSIFIED
AA-5:               BLOCKED

---

## 4. Gate B Readiness Facts

The following are FACTS from the committed closure record (2a33763):

- V-1 PASS: python3 -m py_compile scripts/e2_exact_matcher.py -- exit 0, no output
- V-2 PASS: bash -n scripts/e2_path_n_smoke_runner.sh -- exit 0, no output
- V-3 PASS: matcher behavioral tests -- 9 passed
- V-4 PASS: preflight tests -- 5 passed
- V-5 PASS: scripts/e2_path_n_smoke_runner.sh --preflight -- PREFLIGHT OK
- V-6 PASS: WPS001 invariants -- 20 passed
- V-7 PASS: path designation and selection tests -- 17 passed
- V-8 PASS: working tree clean
- V-9 PASS: HEAD equals origin/main

These facts establish implementation readiness only. They do not
establish that a live retry will succeed.

---

## 5. Execution Model Ruling

Gate C authorizes exactly one new E-2 retry attempt.

### Runner authority ruling

scripts/e2_path_n_smoke_runner.sh is the authoritative execution
mechanism for this retry. The manual command blocks in
E2_OPERATIONAL_PROCEDURE.md sections 7.2-7.4 must not be executed
in parallel or as an alternative. The operational procedure remains
the governing intent and evidence contract.

No dual execution. No fallback to manual blocks during the
five-cycle sequence.

### SID policy

A new SID must originate exclusively from the Location header
returned by a POST to /start_ilt002_combination_lock_path_n.
The runner validates the extracted SID as a UUID and rejects the
denied prior SID before any session cycle.

---

## 6. Flask Startup Ruling

Flask startup is a separately controlled human operator action
performed in a dedicated terminal before runner invocation.

### Authoritative startup command

Source: E2_OPERATIONAL_PROCEDURE.md section 7.1

    Terminal A -- from the repository root:
    PYTHONPATH=. python web/app.py

Required confirmation: server output includes
    Running on http://127.0.0.1:5000

Leave Terminal A running until the runner completes.

### Constraints

- Flask must be started by the human operator, not by the runner.
- The runner does not start or stop Flask.
- The runner verifies server availability via GET / before
  creating a session.
- If Flask fails to start or does not report port 5000: STOP.

---

## 7. Pre-Execution Gates

All four conditions must be satisfied immediately before invoking
the runner. If any fails: STOP -- no SID creation and no retry.

CHECK 1: git status --short is empty
CHECK 2: git rev-parse HEAD equals git rev-parse origin/main
CHECK 3: scripts/e2_path_n_smoke_runner.sh --preflight
         prints exactly "PREFLIGHT OK" and exits 0
CHECK 4: curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:5000/
         returns exactly "200"

---

## 8. Authorized Execution Sequence

The following is the exact authorized order. No step may be
skipped, reordered, or repeated within this authorization.

Step 1 -- Verify repository baseline
  git status --short must be empty
  git rev-parse HEAD must equal git rev-parse origin/main

Step 2 -- Run runner --preflight
  scripts/e2_path_n_smoke_runner.sh --preflight
  Required: PREFLIGHT OK, exit 0
  On failure: STOP

Step 3 -- Start Flask (Terminal A, human operator)
  PYTHONPATH=. python web/app.py
  Required: "Running on http://127.0.0.1:5000" visible
  On failure: STOP

Step 4 -- Verify server readiness (Terminal B)
  curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:5000/
  Required: exactly "200"
  On failure: STOP

Step 5 -- Invoke runner normal mode exactly once (Terminal B)
  scripts/e2_path_n_smoke_runner.sh
  Capture complete stdout and exit code
  Do not interrupt; do not manually substitute responses

Step 6 -- Capture exit code and complete stdout
  Preserve verbatim terminal output

Step 7 -- Stop and preserve evidence
  Stop Flask (Terminal A)
  Preserve all output files per section 9
  Return to owner review -- no automatic action

No manual intervention inside the five-cycle sequence.

---

## 9. Evidence-Preservation Requirements

The following must be preserved verbatim before any commit or review:

- Complete terminal output (Terminal A and Terminal B)
- New SID value
- Runner exit code
- All /tmp/e2_session_get_iter_N.html files created
- /tmp/e2_session_final_state.html
- New JSONL transcript: /tmp/ilt002_transcript_<SID>.jsonl
- Server terminal output (Terminal A)
- git rev-parse HEAD and git rev-parse origin/main at time of run
- git status --short after run
- SHA-256 or byte-preserved copy of the JSONL transcript

No evidence may be rewritten, cleaned, normalized, or replaced
before owner review.

---

## 10. STOP Conditions

Any of the following requires immediate halt. On any STOP:

  E-2 NOT ACCEPTED for this attempt.
  No success-evidence commit.
  Preserve all outputs.
  Return to owner for ruling.
  No same-session repair or rerun.

STOP conditions:

1.  Repository not clean (git status --short non-empty)
2.  HEAD differs from origin/main
3.  Preflight failure (--preflight exit non-zero or not PREFLIGHT OK)
4.  Server not ready (curl does not return exactly "200")
5.  Session-creation transport failure (curl exits non-zero)
6.  Missing Location header in session-creation response
7.  Missing or malformed SID (not a valid UUID)
8.  Denied prior SID (830054a4-f9cb-43fb-ab1c-f5d5f3cfb314 extracted)
9.  GET failure on any cycle (curl exits non-zero)
10. POST failure on any cycle (curl exits non-zero)
11. Unexpected HTTP status on any iteration POST (not 302)
12. Matcher operational failure (exit non-zero)
13. Unexpected matcher output (not "MATCH <qid>" or "NO_MATCH")
14. No MATCH within five submitted responses
15. Artifact or transcript failure (missing, empty, or malformed)
16. Any attempted manual substitution or continuation after a STOP
17. Any pressure to interpret partial progress as E-2 acceptance

---

## 11. Acceptance Criterion

E-2 is ACCEPTED if and only if:

A newly created valid Path N session (new SID, not the denied
prior SID) produced an exact approved Path N question MATCH
within at most five fixed responses, and the runner completed
with exit 0.

Acceptance does NOT mean:

- inventor development proven
- understanding improved
- idea growth proven
- Stage 3 completion
- runtime integration complete
- runtime_integrated = true
- R2 released
- FORM T unblocked
- S-6 classified
- AA-5 unblocked
- a second attempt authorized

---

## 12. Single-Attempt Consumption Rule

Once the session-creation POST to
/start_ilt002_combination_lock_path_n is issued, Gate C is
consumed regardless of outcome.

A new attempt requires a new authorization document.

Boundary definition:
  Pre-execution (Gate C NOT consumed): Steps 1-4 failures
  Gate C consumed: Step 5 -- the session-creation POST is issued

Failures before SID creation are pre-execution STOPs. They do
not consume Gate C and require owner review before another
invocation may proceed.

---

## 13. Explicit Non-Claims and Unchanged Statuses

This document does not claim, establish, or imply:

- E-2 will succeed
- The runner will produce a MATCH
- The engine will behave as expected in live conditions
- Any implementation gap has been resolved
- Any inventor outcome has been measured

The following statuses remain unchanged by this document and
must not move as a result of Gate C execution alone:

E-2 STOP:           DECLARED AND RECORDED
runtime_integrated: false
R2:                 HELD
FORM T:             BLOCKED
S-6:                UNCLASSIFIED
AA-5:               BLOCKED

No status moves automatically after the execution run.
Owner review is mandatory before any status movement is considered.

---

## 14. Post-Execution Owner-Review Requirement

After the run -- whether ACCEPTED or STOP:

1. Paste complete verbatim output for owner review.
2. Do not commit any evidence record until the owner reviews
   and approves the complete output.
3. Do not modify any code, test, or governance document.
4. Do not start a second attempt.
5. Do not interpret acceptance as authorizing status movement.
6. Do not update the roadmap beyond what its section 11 rule requires.
7. Owner ruling is required before any evidence commit,
   incident record commit, or next-step authorization.

---

## 15. Final Authorization Determination

GATE C EXECUTION AUTHORIZATION: PROPOSED -- NOT YET EFFECTIVE

Gate C commit records execution authorization, but execution
remains blocked until all of the following occur in order:

1. Independent owner review of this draft.
2. Explicit owner approval.
3. Gate C commit and push to origin/main.
4. Post-Gate-C roadmap synchronization committed (mandatory --
   not optional).
5. Clean-tree and HEAD-equals-origin/main verification after
   the roadmap synchronization commit.
6. A separate explicit owner instruction to perform the single
   attempt -- this document alone does not trigger execution.

Until all six conditions are satisfied:
E-2 retry remains NOT AUTHORIZED.
All holds remain unchanged.
No Flask startup is authorized.
No SID creation is authorized.
No runner execution mode is authorized.
