# E-2 SAFE RETRY DESIGN AUTHORIZATION
# Gate A of three — DESIGN ONLY
# Status: AUTHORIZATION DOCUMENT
# Authoring baseline: 4779b51

## 1. Purpose

This document is Gate A of the three-gate safe-retry governance
sequence. It authorizes safe-retry design work only.

It does NOT authorize implementation, script creation, server
startup, SID creation, or E-2 execution.

## 2. Background

Session 830054a4 was declared INVALID (a684aba). The E-2
evidence objective from db2c46e remains unmet. The failure
cause was operator/tooling defect — indentation-destructive
normalization of the §7.4 Markdown block. The committed
E2_OPERATIONAL_PROCEDURE.md was NOT ESTABLISHED as defective.

## 3. Authorization scope — DESIGN ONLY

This document authorizes safe-retry design work only.

Authorized:
- Freeze the proposed matcher/runner architecture.
- Define interfaces, gates, tests, evidence outputs, and STOP
  rules.
- Prepare an implementation-authorization draft.
- Prepare code drafts for review without writing repository
  files.

Not authorized by this document:
- Create or modify scripts.
- Commit implementation.
- Start the server.
- Create a SID.
- Execute E-2.
- Declare the E-2 STOP resolved.

## 4. Three-gate authorization sequence

Gate A — this document:
  Safe Retry Design Authorization
  Authorizes: design, interface definition, draft preparation
  Does not authorize: implementation, execution

Gate B — separate document, separate commit (later):
  Safe Retry Implementation Authorization
  Authorizes: creation and commit of matcher, tests, runner,
  preflight, and implementation closure/readiness record
  Does not authorize: server startup, SID creation, execution

Gate C — separate document, separate commit (later):
  One-Session Retry Execution Authorization
  Authorizes: one new E-2 smoke session via committed scripts
  only
  Does not authorize: more than one session, Phase 3
  completion, runtime_integrated=true

## 5. Proposed architecture (frozen for design — not yet
   implemented)

scripts/e2_exact_matcher.py

  Standalone Python file.
  No imports from engine/.
  SID source precedence:
    --sid <value> takes precedence over the SID environment
    variable. If neither --sid nor SID is provided:
      print STOP: SID not provided
      exit non-zero
  Reads transcript from:
    Production default:
      /tmp/ilt002_transcript_<SID>.jsonl
    Override for testing (CLI or env):
      --transcript-path <path>  or  E2_TRANSCRIPT_PATH=<path>
  Loads approved artifact from:
    Production default:
      docs/governance/path_n_content_config/
      electronics_electrical_path_n_questions.json
    Override for testing (CLI or env):
      --artifact-path <path>  or  E2_ARTIFACT_PATH=<path>
  Validates artifact schema (top-level "gaps" dict;
    list of {"question_id", "text"} objects).
  Performs exact string comparison.
  Prints exactly:
    MATCH <qid>    — exit 0
    NO_MATCH       — exit 0
    STOP: <reason> — exit non-zero
  Modifies no file.
  Committed approved artifact is never removed, renamed,
  rewritten, or temporarily replaced.

scripts/e2_path_n_smoke_runner.sh

  Standalone Bash file.
  No executable code extracted from Markdown.
  Defines five fixed responses as a Bash array.
  Does NOT start or stop the Flask server.
  Server startup remains a separately controlled Gate C
  operation.
  The runner verifies server availability before creating a
  session, then performs session creation, GET/POST cycles,
  matcher invocation, and artifact capture.
  Gate B must later determine a non-mutating readiness check
  that does not create or change session state. No readiness
  endpoint is assumed (none confirmed in committed web/app.py).
  Submits idea via POST to
    /start_ilt002_combination_lock_path_n.
  Extracts SID exclusively from the Location header returned
  by the authorized Path N start route.
  Validates SID as UUID.
  Implements an executable SID rejection function that rejects
  the prior invalid SID
  830054a4-f9cb-43fb-ab1c-f5d5f3cfb314
  with non-zero exit before any session cycle can run.
  Gate B behavioral tests must prove this rejection.
  Provides no resume-existing-session mode.
  Does not accept a user-supplied SID for a new retry.
  Executes GET-before-POST loop, maximum five cycles.
  Calls python3 scripts/e2_exact_matcher.py as a subprocess
    (not via heredoc or extraction).
  Stops immediately on first MATCH.
  Captures all HTML GET files and final state HTML.
  Includes --preflight mode (see §8).

## 6. Syntax and behavioral validation gates

V-1 — Python syntax:
  python3 -m py_compile scripts/e2_exact_matcher.py
  Required: exit 0, no output

V-2 — Shell syntax:
  bash -n scripts/e2_path_n_smoke_runner.sh
  Required: exit 0, no output

V-3 — Matcher behavioral tests:
  A committed test suite must pass before Gate B closes.
  Required test cases (see §7).
  All tests must pass with exit 0.

V-4 — Runner preflight:
  scripts/e2_path_n_smoke_runner.sh --preflight
  Required: all checks pass, exit 0 (see §8)

V-5 — Clean tree before any execution:
  git status --short returns empty

V-6 — HEAD equals origin/main before any execution:
  git rev-parse HEAD == git rev-parse origin/main

## 7. Required matcher behavioral tests

All tests must use temporary fixture files only.
The committed approved Path N artifact must never be removed,
renamed, rewritten, or temporarily replaced by any test.
Tests requiring non-default paths must use --artifact-path or
E2_ARTIFACT_PATH to point to temporary test fixtures.

Test 1 — approved exact match:
  Inject a transcript record whose "question" field equals an
  approved artifact text verbatim.
  Expected output: MATCH <correct_qid>
  Expected exit: 0

Test 2 — valid nonmatch:
  Inject a transcript record whose "question" does not match
  any approved text.
  Expected output: NO_MATCH
  Expected exit: 0

Test 3 — missing SID:
  Omit both --sid argument and SID environment variable.
  Expected output: STOP: SID not provided
  Expected exit: non-zero

Test 4 — missing transcript:
  Use --transcript-path pointing to a non-existent path.
  Expected output: STOP: transcript file not found
  Expected exit: non-zero

Test 5 — empty transcript:
  Use --transcript-path pointing to an empty temporary file.
  Expected output: STOP: transcript file is empty
  Expected exit: non-zero

Test 6 — malformed JSONL:
  Use --transcript-path pointing to a temporary file whose
  last line is not valid JSON.
  Expected output: STOP: malformed JSONL in latest record
  Expected exit: non-zero

Test 7 — missing test artifact fixture:
  Use --artifact-path pointing to a non-existent path.
  Expected output: STOP: artifact file not found
  Expected exit: non-zero

Test 8 — malformed test artifact fixture:
  Use --artifact-path pointing to a temporary JSON file
  lacking the "gaps" key.
  Expected output: STOP: artifact schema unexpected
  Expected exit: non-zero

## 8. Runner preflight design

Command:
  scripts/e2_path_n_smoke_runner.sh --preflight

Preflight must NOT:
  Start the server.
  Create a SID.
  Issue any GET or POST request.
  Mutate any file.

Preflight checks:

  CHECK 1: Working directory is repository root
    (presence of docs/governance/ and engine/)
  CHECK 2: git status --short is empty (clean tree)
  CHECK 3: git rev-parse HEAD equals git rev-parse origin/main
  CHECK 4: scripts/e2_exact_matcher.py exists
  CHECK 5: python3 -m py_compile scripts/e2_exact_matcher.py
           exits 0
  CHECK 6: Approved artifact exists at committed path:
    docs/governance/path_n_content_config/
    electronics_electrical_path_n_questions.json
  CHECK 7: Five fixed responses are defined and non-empty
  CHECK 8: The executable SID rejection function is configured
    and can be invoked. Preflight confirms the mechanism is
    present and callable. Behavioral proof that the prior
    invalid SID 830054a4-f9cb-43fb-ab1c-f5d5f3cfb314 is
    rejected with non-zero exit is required by Gate B
    behavioral tests — a comment or grep result is not
    sufficient proof.
  CHECK 9: /tmp is writable

  On all checks pass: print PREFLIGHT OK — exit 0
  On any check fail: print PREFLIGHT FAIL: <check> — exit 1

## 9. STOP conditions (for later execution authorization)

1. Any gate V-1 through V-6 fails before execution.
2. Preflight reports any failure.
3. Server not available at expected address before session
   creation (readiness check design deferred to Gate B;
   no readiness endpoint confirmed in committed web/app.py).
4. SID empty or not a valid UUID after session creation.
5. SID equals 830054a4-f9cb-43fb-ab1c-f5d5f3cfb314.
6. Any POST returns non-302 status.
7. Match command exits non-zero or prints unexpected output.
8. No MATCH within five responses — E-2 NOT ACCEPTED.
9. Progression review inconsistent with deterministic engine
   rules.
10. Transcript missing or empty after session.
11. Any pressure to treat retry as Phase 3 completion or as
    making runtime_integrated=true eligible.

On any STOP: preserve all output files; do not create a
successful evidence commit; report to owner for ruling.

## 10. Evidence-preservation requirements
     (for later execution authorization)

On ACCEPTED outcome only:
  docs/governance/evidence/E2_PATH_N_SMOKE_SESSION_<SID>.md
  docs/governance/evidence/E2_TRANSCRIPT_<SID>.jsonl
  docs/governance/evidence/E2_SESSION_GET_ITER_<n>_<SID>.html
  docs/governance/evidence/E2_SESSION_FINAL_STATE_<SID>.html

SHA-256 source/destination verification required for all
copied files before evidence commit.

On STOP/NOT ACCEPTED outcome:
  Preserve in a named failed-attempt directory.
  Do not create a successful evidence commit.

## 11. What a successful retry does NOT authorize

A successful E-2 retry does NOT automatically:
- set runtime_integrated=true
  (requires separate authorization, JSON metadata update,
  re-testing, recorded re-approval per d2b2a9a §6)
- release R2 (HELD — D-B, ccd1ecd §6.1)
- authorize FORM T
- classify S-6
- release AA-5
- complete Phase 3
  (Phase 3 requires a committed runtime test suite per
  d2b2a9a §6 table — not a smoke session)

Each requires its own separate authorization.
Nothing moves automatically after an evidence commit.

## 12. Relationship with E2_OPERATIONAL_PROCEDURE.md

The later execution authorization (Gate C) must explicitly
determine whether the committed retry scripts supersede the
manual execution portion of E2_OPERATIONAL_PROCEDURE.md for
one retry, or whether a narrow procedure amendment is required.

No parallel or ambiguous execution authority is permitted.
This question is flagged here but not decided or implemented
by this design authorization.

## 13. Commit and roadmap sequence

Commit 1 — this document:
  docs/governance/E2_SAFE_RETRY_DESIGN_AUTHORIZATION.md
  Message: governance: E-2 safe retry design authorization
           (Gate A)

Commit 2 — immediately after Commit 1:
  docs/governance/ACTIVE_EXECUTION_ROADMAP.md
  (§4, §5, §6, §7 only — reflecting design authorization)
  Message: governance: roadmap sync after E-2 safe retry
           design authorization

Later, only after owner review:
Commit 3:
  docs/governance/E2_SAFE_RETRY_IMPLEMENTATION_AUTHORIZATION.md
  Message: governance: E-2 safe retry implementation
           authorization (Gate B)

Later implementation commits (Gate B scope only):
  scripts/e2_exact_matcher.py and matcher tests
  scripts/e2_path_n_smoke_runner.sh and preflight
  implementation closure/readiness record
  roadmap synchronization

Later, separately:
Commit N:
  docs/governance/E2_SAFE_RETRY_EXECUTION_AUTHORIZATION.md
  Message: governance: E-2 safe retry execution authorization
           (Gate C)

Roadmap must be synchronized after each of:
  design authorization
  implementation authorization
  implementation closure/readiness
  execution authorization
  retry acceptance or STOP

## 14. Status

E-2 STOP:           DECLARED AND RECORDED (a684aba)
E-2:                NOT ACCEPTED
E-2 retry:          NOT AUTHORIZED
Implementation:     NOT AUTHORIZED
runtime_integrated: false
R2:                 HELD
FORM T:             BLOCKED
S-6:                UNCLASSIFIED
AA-5:               BLOCKED
