# E-2 SAFE RETRY IMPLEMENTATION AUTHORIZATION
# Gate B of three — IMPLEMENTATION ONLY
# Status: AUTHORIZATION DOCUMENT
# Authoring baseline: c2406f2
# Gate A reference: 1cb08cb

## 1. Purpose

This document is Gate B of the three-gate safe-retry governance
sequence. It authorizes implementation only.

It does NOT authorize Flask startup, SID creation, live retry
execution, STOP resolution, runtime_integrated=true, or any
hold movement.

Gate A (1cb08cb) froze the architecture and defined all
interfaces. Gate B implements that frozen design exactly.
No design changes are permitted during Gate B.

No implementation file may be created before B-0B is committed
and the working tree is clean.

## 2. Relationship with Gate A

Gate A authorized:
- Architecture freeze
- Interface definitions
- Gate, test, and STOP specifications

Gate B authorizes:
- Creation of the five committed implementation files only
- All files must conform exactly to Gate A §5 interfaces
- Any deviation from Gate A interfaces requires a new
  design amendment before implementation may proceed

## 3. Exact implementation scope

Gate B authorizes creation and commit of exactly five files:

  scripts/e2_exact_matcher.py
  scripts/e2_path_n_smoke_runner.sh
  tests/test_e2_exact_matcher.py
  tests/test_e2_runner_preflight.py
  docs/governance/E2_SAFE_RETRY_IMPLEMENTATION_CLOSURE_RECORD.md

One later roadmap synchronization (B-4) modifies only:
  docs/governance/ACTIVE_EXECUTION_ROADMAP.md

No other files may be created or modified.

## 4. Exact files authorized for creation

| File | Purpose |
|------|---------|
| `scripts/e2_exact_matcher.py` | Standalone Python matcher per Gate A §5 |
| `scripts/e2_path_n_smoke_runner.sh` | Standalone Bash runner per Gate A §5 |
| `tests/test_e2_exact_matcher.py` | Nine behavioral tests including CLI contract |
| `tests/test_e2_runner_preflight.py` | Five isolated preflight tests in bare-origin fixture repos |
| `docs/governance/E2_SAFE_RETRY_IMPLEMENTATION_CLOSURE_RECORD.md` | Closure evidence after all gates pass |

## 5. Exact prohibited files

No modification to:
  web/app.py
  engine/ (any file)
  domains/ (any file)
  docs/governance/path_n_content_config/ (any file)
  docs/governance/E2_OPERATIONAL_PROCEDURE.md
  docs/governance/E2_SAFE_RETRY_DESIGN_AUTHORIZATION.md
  docs/governance/evidence/ (any existing file)
  tests/test_wps001_invariants.py
  tests/test_phase2_path_n_selection.py
  tests/test_phase1_path_designation.py
  tests/test_web_app.py
  Any other existing file

No creation of any file not listed in §3.

## 6. Matcher interface and CLI contract

File: scripts/e2_exact_matcher.py

Invocation:
  python3 scripts/e2_exact_matcher.py [--sid <value>]
    [--transcript-path <path>] [--artifact-path <path>]

SID resolution (precedence order):
  1. --sid <value>
  2. SID environment variable
  3. Neither provided:
     stdout: "STOP: SID not provided"
     stderr: empty
     exit: non-zero

Transcript path resolution:
  Default: /tmp/ilt002_transcript_<SID>.jsonl
  Override: --transcript-path <path>
            or E2_TRANSCRIPT_PATH=<path>

Artifact path resolution:
  Default:
    docs/governance/path_n_content_config/
    electronics_electrical_path_n_questions.json
  Override: --artifact-path <path>
            or E2_ARTIFACT_PATH=<path>

Required process-output contract:

  For MATCH <qid> and NO_MATCH:
  - stdout: exactly one line
  - stderr: empty
  - exit: 0

  For any STOP:
  - stdout: exactly one line beginning with "STOP: "
  - stderr: empty
  - exit: non-zero

  No traceback, argparse usage text, warning, debug line,
  or additional output is permitted under any condition.
  All CLI parse failures must be caught and converted into
  the controlled STOP contract rather than default argparse
  stderr output.

Required STOP: <reason> values:
  STOP: SID not provided
  STOP: transcript file not found
  STOP: transcript file is empty
  STOP: malformed JSONL in latest record
  STOP: artifact file not found
  STOP: artifact schema unexpected
  STOP: invalid argument

Modifies no file.
Committed approved artifact never removed or mutated.

## 7. Runner interface, --preflight, and --validate-sid

File: scripts/e2_path_n_smoke_runner.sh

Invocation modes:
  scripts/e2_path_n_smoke_runner.sh             — execution mode
  scripts/e2_path_n_smoke_runner.sh --preflight — preflight mode
  scripts/e2_path_n_smoke_runner.sh \
    --validate-sid <candidate>                  — validation mode

### --validate-sid contract

Validation only. No Flask startup, no session creation,
no GET, no POST, no artifact mutation.

  valid non-denied UUID: exit 0
  malformed UUID:
    stdout: "STOP: invalid SID format"
    exit non-zero
  prior invalid SID
  830054a4-f9cb-43fb-ab1c-f5d5f3cfb314:
    stdout: "STOP: denied prior SID"
    exit non-zero

The runner accepts no user-supplied SID in normal execution
mode. --validate-sid exists only as a non-mutating validation
and test interface.

### Server readiness check

Repository evidence: web/app.py lines 17-19:
  @app.route("/", methods=["GET"])
  def index():
      return render_template("index.html")

This route creates no session, does not mutate SESSION_STORE,
and does not call run_iteration. It is the authorized
non-mutating readiness check.

Readiness command:
  curl -s -o /dev/null -w "%{http_code}" \
    http://127.0.0.1:5000/
  Required: exactly "200"

Readiness failure handling:
  Any timeout, connection failure, curl non-zero exit,
  status "000", or non-200 response:
    stdout: "STOP: server not ready"
    exit non-zero

Do not add or modify any Flask route.

### Execution mode behavior

Does NOT start or stop Flask.
Verifies server availability via readiness check above.
Submits idea via POST to
  /start_ilt002_combination_lock_path_n.
Extracts SID from Location header only.
Validates extracted SID via --validate-sid mechanism.
Exits non-zero if extracted SID equals
  830054a4-f9cb-43fb-ab1c-f5d5f3cfb314.
Provides no resume-existing-session mode.
Does not accept user-supplied SID.
Executes GET-before-POST loop, maximum five cycles.
Calls python3 scripts/e2_exact_matcher.py as subprocess.
Stops on first MATCH.
Captures:
  /tmp/e2_session_get_iter_<n>.html per cycle
  /tmp/e2_session_final_state.html after loop
Prints cycle status per iteration.
Exits 0 on ACCEPTED (MATCH found).
Exits 1 on any STOP condition.

### --preflight mode

CHECK 1: Working directory is repository root
         (docs/governance/ and engine/ both present)
CHECK 2: git status --short is empty
CHECK 3: git rev-parse HEAD equals git rev-parse origin/main
CHECK 4: scripts/e2_exact_matcher.py exists
CHECK 5: python3 -m py_compile scripts/e2_exact_matcher.py
         exits 0
CHECK 6: Approved artifact exists at committed path:
         docs/governance/path_n_content_config/
         electronics_electrical_path_n_questions.json
CHECK 7: Five fixed responses are defined and non-empty
CHECK 8: --validate-sid 830054a4-f9cb-43fb-ab1c-f5d5f3cfb314
         returns "STOP: denied prior SID" and exits non-zero
CHECK 9: /tmp is writable

On all pass: print "PREFLIGHT OK" — exit 0
On any fail: print "PREFLIGHT FAIL: <check>" — exit 1
Must NOT start server, create SID, or issue GET/POST.

## 8. Required matcher behavioral tests

File: tests/test_e2_exact_matcher.py

All tests use temporary fixture files only via pytest tmp_path.
The committed approved artifact is never removed, renamed,
rewritten, or temporarily replaced.
Every test asserts stdout, stderr, and exit code.

| # | Test | Fixture method | stdout | stderr | exit |
|---|------|---------------|--------|--------|------|
| 1 | approved exact match | tmp_path: valid artifact fixture + matching transcript | MATCH <correct_qid> | empty | 0 |
| 2 | valid nonmatch | tmp_path: valid artifact fixture + non-matching transcript | NO_MATCH | empty | 0 |
| 3 | missing SID | omit --sid; unset SID env | STOP: SID not provided | empty | non-zero |
| 4 | missing transcript | --transcript-path=<non-existent in tmp_path> | STOP: transcript file not found | empty | non-zero |
| 5 | empty transcript | --transcript-path=<empty file in tmp_path> | STOP: transcript file is empty | empty | non-zero |
| 6 | malformed JSONL | --transcript-path=<invalid JSON in tmp_path> | STOP: malformed JSONL in latest record | empty | non-zero |
| 7 | missing artifact fixture | --artifact-path=<non-existent in tmp_path> | STOP: artifact file not found | empty | non-zero |
| 8 | malformed artifact fixture | --artifact-path=<JSON lacking gaps key in tmp_path> | STOP: artifact schema unexpected | empty | non-zero |
| 9 | CLI parse failure | invalid flag e.g. --unknown-arg | STOP: invalid argument | empty | non-zero |

## 9. Isolated preflight test design

File: tests/test_e2_runner_preflight.py

All P-1 through P-5 tests run inside an isolated temporary
fixture repository created under pytest tmp_path.

### Fixture repository layout

  tmp_path/
    remote.git/     — bare Git repository used as origin
    worktree/       — isolated fixture working repository

### Required setup design

  remote = tmp_path / "remote.git"
  repo   = tmp_path / "worktree"

  subprocess.run(["git", "init", "--bare", str(remote)],
                 check=True)
  subprocess.run(["git", "init", str(repo)], check=True)
  subprocess.run(["git", "checkout", "-b", "main"],
                 cwd=repo, check=True)

  # Create test-specific fixture state before committing.

  subprocess.run(["git", "add", "."], cwd=repo, check=True)
  subprocess.run(
      [
          "git",
          "-c", "user.name=Test",
          "-c", "user.email=test@example.invalid",
          "commit", "-m", "fixture",
      ],
      cwd=repo,
      check=True,
  )
  subprocess.run(
      ["git", "remote", "add", "origin", str(remote)],
      cwd=repo, check=True,
  )
  subprocess.run(
      ["git", "push", "-u", "origin", "main"],
      cwd=repo, check=True,
  )

This produces a real clean fixture state where:
  git rev-parse HEAD == git rev-parse origin/main

Do not push a checked-out branch into the same working
repository. Do not configure the fixture repository itself
as its own origin.

### Negative fixture state construction

P-2, P-3, and P-5 must construct their negative states
BEFORE the fixture commit, not by mutating files after commit.

P-2 (missing matcher):
  Create worktree/ without scripts/e2_exact_matcher.py.
  Commit that state, push to bare remote.
  Run --preflight in worktree/. Expected: PREFLIGHT FAIL: CHECK 4

P-3 (invalid matcher):
  Create worktree/ with a syntactically invalid matcher fixture
  at scripts/e2_exact_matcher.py (e.g. bare "if True:" with no
  body).
  Commit that state, push to bare remote.
  Run --preflight in worktree/. Expected: PREFLIGHT FAIL: CHECK 5

P-5 (missing artifact):
  Create worktree/ without the artifact at CHECK 6 path.
  Commit that state, push to bare remote.
  Run --preflight in worktree/. Expected: PREFLIGHT FAIL: CHECK 6

Each negative fixture must still have clean working tree and
HEAD == origin/main at the time --preflight runs.

No test deletes, renames, or overwrites fixture files after
commit. No test modifies, renames, overwrites, or restores
any tracked repository file. No test depends on cleanup
restoring the authoritative checkout.

### Preflight test matrix

| # | Test | Fixture state | Expected output | Exit |
|---|------|--------------|-----------------|------|
| P-1 | all checks pass | Full valid worktree, clean, HEAD==origin/main | PREFLIGHT OK | 0 |
| P-2 | missing matcher | No matcher file committed | PREFLIGHT FAIL: CHECK 4 | 1 |
| P-3 | invalid matcher syntax | Syntactically invalid matcher committed | PREFLIGHT FAIL: CHECK 5 | 1 |
| P-4 | prior SID rejected | --validate-sid 830054a4-f9cb-43fb-ab1c-f5d5f3cfb314 | STOP: denied prior SID | non-zero |
| P-5 | missing artifact | No artifact at CHECK 6 path committed | PREFLIGHT FAIL: CHECK 6 | 1 |

## 10. Per-commit gates

### Matcher commit gates (before B-1)

  python3 -m py_compile scripts/e2_exact_matcher.py
    Required: exit 0, no output
  pytest tests/test_e2_exact_matcher.py -q
    Required: 9 passed, 0 failed
  git diff --check
    Required: no output
  Authorized-file scope check:
    Only scripts/e2_exact_matcher.py and
    tests/test_e2_exact_matcher.py in staged diff

### Runner commit gates (before B-2)

  bash -n scripts/e2_path_n_smoke_runner.sh
    Required: exit 0, no output
  pytest tests/test_e2_runner_preflight.py -q
    Required: 5 passed, 0 failed
  pytest tests/test_e2_exact_matcher.py -q
    Required: 9 passed, 0 failed (regression)
  git diff --check
    Required: no output
  Authorized-file scope check:
    Only scripts/e2_path_n_smoke_runner.sh and
    tests/test_e2_runner_preflight.py in staged diff

## 11. Gate B closure gates

After B-1 and B-2 are pushed and tree is clean:

  V-1: python3 -m py_compile scripts/e2_exact_matcher.py
       Required: exit 0, no output

  V-2: bash -n scripts/e2_path_n_smoke_runner.sh
       Required: exit 0, no output

  V-3: pytest tests/test_e2_exact_matcher.py -q
       Required: 9 passed, 0 failed

  V-4: pytest tests/test_e2_runner_preflight.py -q
       Required: 5 passed, 0 failed

  V-5: scripts/e2_path_n_smoke_runner.sh --preflight
       (against real repository after B-1 and B-2 committed)
       Required: PREFLIGHT OK, exit 0

  V-6: pytest tests/test_wps001_invariants.py -q
       Required: 20 passed, 0 failed

  V-7: pytest tests/test_phase1_path_designation.py
              tests/test_phase2_path_n_selection.py -q
       Required: all passed, 0 failed

  V-8: git status --short returns empty

  V-9: git rev-parse HEAD == git rev-parse origin/main

All gate outputs must appear verbatim in
E2_SAFE_RETRY_IMPLEMENTATION_CLOSURE_RECORD.md
before that document is committed.

## 12. Commit sequence

B-0A — this document:
  docs/governance/E2_SAFE_RETRY_IMPLEMENTATION_AUTHORIZATION.md
  Message: governance: E-2 safe retry implementation
           authorization (Gate B)

B-0B — immediately after B-0A, before any implementation:
  docs/governance/ACTIVE_EXECUTION_ROADMAP.md
  (§4, §5, §6, §7 only — Gate B authorized; implementation
  authorized; execution still not authorized; STOP declared)
  Message: governance: roadmap sync after Gate B authorization

B-1 — only after B-0B committed and tree clean:
  scripts/e2_exact_matcher.py
  tests/test_e2_exact_matcher.py
  (inseparable — implementation and verification together)
  Message: scripts+tests: add E-2 Path N exact matcher
           and behavioral tests (Gate B)
  Gates: matcher commit gates (§10) must pass

B-2:
  scripts/e2_path_n_smoke_runner.sh
  tests/test_e2_runner_preflight.py
  (inseparable — implementation and verification together)
  Message: scripts+tests: add E-2 Path N smoke runner
           and preflight tests (Gate B)
  Gates: runner commit gates (§10) must pass

B-3 — only after all V-1 through V-9 pass:
  docs/governance/E2_SAFE_RETRY_IMPLEMENTATION_CLOSURE_RECORD.md
  Message: governance: E-2 safe retry implementation
           closure record (Gate B complete)

B-4 — immediately after B-3:
  docs/governance/ACTIVE_EXECUTION_ROADMAP.md
  Message: governance: roadmap sync after Gate B closure

## 13. Roadmap update points

Roadmap synchronized after:
  B-0B: Gate B authorized
  B-4:  Gate B closure confirmed
  Gate C authorized
  Retry accepted or STOP declared

## 14. Relationship with E2_OPERATIONAL_PROCEDURE.md

Gate C must explicitly determine whether the committed retry
scripts supersede the manual execution portion of
E2_OPERATIONAL_PROCEDURE.md for one retry, or whether a
narrow procedure amendment is required.

No parallel or ambiguous execution authority is permitted.
Not decided or implemented by Gate B.

## 15. What Gate B does NOT authorize

Gate B does NOT authorize:
- Flask startup
- SID creation
- Live retry execution
- E-2 STOP resolution
- runtime_integrated=true
- R2 release
- FORM T movement
- S-6 classification
- AA-5 release
- Phase 3 completion
- Any file not listed in §3
- Any implementation before B-0B is committed and clean

## 16. Status

E-2 STOP:                  DECLARED AND RECORDED (a684aba)
E-2:                       NOT ACCEPTED
E-2 retry execution:       NOT AUTHORIZED (Gate C required)
Safe-retry design:         AUTHORIZED (Gate A, 1cb08cb)
Safe-retry implementation: AUTHORIZED BY THIS DOCUMENT
                           pending commitment of B-0A and B-0B
runtime_integrated:        false
R2:                        HELD
FORM T:                    BLOCKED
S-6:                       UNCLASSIFIED
AA-5:                      BLOCKED
