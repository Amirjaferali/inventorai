# E-2 OPERATIONAL PROCEDURE — PATH N SMOKE SESSION

## 1. Status and scope

- AUTHORIZATION AND PROCEDURE DOCUMENT. Authorizes E-2 execution
  as defined in LIMITED_EVIDENCE_AUTHORIZATION.md (`db2c46e`) §6.
- This document satisfies the §6.3 operational procedure gate.
  E-2 execution may begin only after this document is committed,
  its roadmap refresh is committed, the working tree is clean,
  and the evidence execution baseline HEAD is recorded.
- Authoring baseline: `aae15bd`.

## 2. What E-2 is and is not

E-2 is limited supplemental live runtime smoke evidence only.

E-2 is NOT:
- R2 (the ILT-002 water-leak idea re-run).
- FORM T.
- An S-6 classification run.
- Inventor-outcome evidence (SR-001 measurement).
- Phase 3 (which requires a committed runtime test suite per
  `d2b2a9a` §6 table — a committed-test-suite phase, not a
  smoke session).
- Evidence that makes `runtime_integrated=true` eligible alone
  or in combination with E-1/E-3.

## 3. Operational basis (committed sources)

All commands and behaviors derive from committed repository
evidence at `aae15bd`:

- Server start: `web/app.py` `if __name__ == "__main__":
  app.run(debug=True, port=5000)`.
- Route and path assignment: `start_ilt002_combination_lock_path_n()`
  in `web/app.py` line 71 contains the only production
  assignment `state.path = "N"`. All other occurrences in
  `engine/progression_loop.py` (lines 544, 584, 619) are
  read-only comparisons. No production code mutates `state.path`
  after session creation (confirmed at `aae15bd`).
- Route provenance proof of criterion (c): a SID produced by
  POST to `/start_ilt002_combination_lock_path_n` belongs to a
  session with `state.path == "N"` throughout. No runtime
  state inspection is required.
- Response submission: `submit_answer()` POST `/session/<sid>`,
  field `response`, in `web/app.py`.
- Question capture: `show_session()` sets `entry["last_question"]`
  during each GET; `submit_answer()` writes that value into the
  JSONL `question` field during the subsequent POST. A mandatory
  GET before each POST is required so that the correct question
  is captured in the transcript.
- Transcript disk path:
  `/tmp/ilt002_transcript_<sid>.jsonl` — `web/app.py` line 144.
- Approved artifact schema (commit `8ceb5d4`): top-level key
  `"gaps"` maps gap-type strings
  (`MECHANISM_COMPLETENESS`, `PHYSICAL_FEASIBILITY`,
  `BOUNDARY_AMBIGUITY`) to lists of objects each containing
  `"question_id"` and `"text"`. Confirmed from the committed
  artifact; no assumption is made about it.
- State fields observable from HTML after each GET:
  `maturity_level`, `maturity_label`, current `gap_type`,
  `g.status` per gap, `last_result.get("transition")` —
  confirmed from `templates/session.html`.
- `iterations_open` is not required by any acceptance criterion
  and is not captured.

## 4. Preconditions before execution

1. This document is committed and owner-authorized.
2. Required roadmap refresh after this document's commit is
   committed.
3. `git status --short` returns empty.
4. `git log --oneline -1` output recorded as evidence execution
   baseline HEAD.
5. E-1 and E-3 evidence commits confirmed at `cfcc95f`.
6. No code, test, or route changes since `aae15bd`.

## 5. Owner-authorized stopping rule (D-1)

Run GET-before-POST cycles using the D-2 response array until
the first Stage 2 Path N question is captured and confirmed
byte-for-byte against the approved artifact via the exact match
command (§7.3). Stop immediately after the first confirmed MATCH.
Maximum: five submitted responses.
If no qualifying MATCH appears within five responses: STOP
(§10 condition 5) — E-2 is NOT ACCEPTED.
This stopping rule is an owner-authorized smoke-test boundary,
not a claim about guaranteed engine behavior.

## 6. Owner-authorized fixed response array (D-2)

Defined as a Bash array in §7.2 and referenced by index in
§7.4. No manual substitution is required or permitted.

## 7. Execution procedure

All steps in Terminal B must be completed without stopping the
server in Terminal A.

### 7.1 Terminal A — start the Flask server

From the repository root:

    PYTHONPATH=. python web/app.py

Confirm: output includes `Running on http://127.0.0.1:5000`.
Leave running until §7.7.

### 7.2 Terminal B — initialise session

Define the response array, submit the idea, and extract SID:

    RESPONSES=(
      "The keypad detects each key press and sends the entered sequence to a microcontroller for comparison with a stored access code."
      "The main components are a keypad, a microcontroller, a motor driver, a motor, and a mechanical bolt that locks or unlocks the door."
      "When the entered sequence matches the stored code, the controller activates the motor driver, turns the motor, and retracts the bolt."
      "If the code is incorrect, the controller keeps the bolt locked and rejects the attempt without activating the motor."
      "The system needs limits for motor travel, power loss handling, repeated failed attempts, and manual emergency access."
    )

    HEADERS=$(mktemp)

    curl -s -o /dev/null -D "$HEADERS" \
      -X POST \
      http://127.0.0.1:5000/start_ilt002_combination_lock_path_n \
      --data-urlencode \
      "idea=An electronic combination lock that uses a keypad and a motor to control a bolt for a household door."

    SID=$(
      tr -d '\r' < "$HEADERS" |
      sed -nE \
        's#^[Ll]ocation:[[:space:]]*/session/([^[:space:]]+).*#\1#p'
    )

    test -n "$SID" || { echo "STOP: SID missing"; exit 1; }

    printf '%s\n' "$SID" |
    grep -Eq \
      '^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$' \
      || { echo "STOP: SID is not a UUID"; exit 1; }

    export SID
    rm -f "$HEADERS"

    printf 'SID=%s\n' "$SID"

If either STOP line prints: do not proceed (§10 condition 2).
SID is exported; no further manual export is required.

### 7.3 Exact match command — normative contract

The exact match command is a Python block executed via command
substitution inside the §7.4 loop. It is defined once in §7.4
only; this section states its contract.

Contract:
- Reads the SID from the environment variable `SID`.
- Reads the latest record from
  `/tmp/ilt002_transcript_<SID>.jsonl`.
- Loads the approved artifact from
  `docs/governance/path_n_content_config/
  electronics_electrical_path_n_questions.json`.
- Validates the committed artifact schema: top-level `"gaps"`
  dict; each value a list of `{"question_id", "text"}` objects.
- Performs exact string comparison between the latest JSONL
  `question` field and every approved `"text"` value.
- Prints exactly `MATCH <question-id>` and exits zero if a
  match is found.
- Prints exactly `NO_MATCH` and exits zero if the question is
  valid but matches no approved entry.
- Prints `STOP: <reason>` and exits non-zero for any
  operational or schema failure: missing SID, missing or empty
  transcript, malformed JSONL, empty question field, missing
  artifact, unexpected schema.
- Modifies no file.

### 7.4 Cycle loop — GET / POST / match

    MATCH_CYCLE=""
    MATCH_QID=""

    for n in 1 2 3 4 5; do

      # Step 1 — mandatory GET before POST
      curl -s \
        "http://127.0.0.1:5000/session/$SID" \
        > "/tmp/e2_session_get_iter_${n}.html"

      # Step 2 — POST fixed response for this cycle
      RESPONSE="${RESPONSES[$((n-1))]}"

      STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
        -X POST "http://127.0.0.1:5000/session/$SID" \
        --data-urlencode "response=$RESPONSE")

      printf 'cycle=%d http_status=%s\n' "$n" "$STATUS"

      if [ "$STATUS" != "302" ]; then
        echo "STOP: unexpected HTTP status $STATUS on cycle $n"
        exit 1
      fi

      # Step 3 — run exact match command via command substitution
      MATCH_RESULT=$(python3 << 'MATCHEOF'
import json, os, sys
from pathlib import Path

SID = os.environ.get("SID", "")
if not SID:
    print("STOP: SID environment variable not set")
    sys.exit(1)

transcript = Path(f"/tmp/ilt002_transcript_{SID}.jsonl")
if not transcript.exists():
    print("STOP: transcript file not found")
    sys.exit(1)

raw = transcript.read_text(encoding="utf-8")
lines = [l for l in raw.splitlines() if l.strip()]
if not lines:
    print("STOP: transcript file is empty")
    sys.exit(1)

try:
    latest = json.loads(lines[-1])
except json.JSONDecodeError as e:
    print(f"STOP: malformed JSONL in latest record — {e}")
    sys.exit(1)

question = latest.get("question", "")
if not question:
    print("STOP: question field empty in latest JSONL record")
    sys.exit(1)

artifact_path = Path(
    "docs/governance/path_n_content_config/"
    "electronics_electrical_path_n_questions.json"
)
if not artifact_path.exists():
    print("STOP: artifact not found at committed path")
    sys.exit(1)

try:
    data = json.loads(artifact_path.read_text(encoding="utf-8"))
except json.JSONDecodeError as e:
    print(f"STOP: artifact JSON malformed — {e}")
    sys.exit(1)

gaps = data.get("gaps")
if not isinstance(gaps, dict) or not gaps:
    print("STOP: artifact schema unexpected — "
          "'gaps' key missing or not a dict")
    sys.exit(1)

approved = {}
for gap_type, variants in gaps.items():
    if not isinstance(variants, list):
        print(f"STOP: artifact schema unexpected — "
              f"'{gap_type}' value is not a list")
        sys.exit(1)
    for entry in variants:
        if not isinstance(entry, dict) \
           or "question_id" not in entry \
           or "text" not in entry:
            print("STOP: artifact schema unexpected — "
                  "entry missing question_id or text")
            sys.exit(1)
        approved[entry["question_id"]] = entry["text"]

for qid, text in approved.items():
    if question == text:
        print(f"MATCH {qid}")
        sys.exit(0)

print("NO_MATCH")
MATCHEOF
      )
      MATCH_RC=$?

      printf '%s\n' "$MATCH_RESULT"

      test "$MATCH_RC" -eq 0 || {
        echo "STOP: match command exited non-zero on cycle $n"
        exit 1
      }

      case "$MATCH_RESULT" in
        MATCH\ *)
          MATCH_CYCLE="$n"
          MATCH_QID="${MATCH_RESULT#MATCH }"
          break
          ;;
        NO_MATCH)
          ;;
        *)
          echo "STOP: unexpected match result on cycle $n: $MATCH_RESULT"
          exit 1
          ;;
      esac

    done

### 7.5 Post-loop handling

Always capture the final session state regardless of loop outcome:

    curl -s \
      "http://127.0.0.1:5000/session/$SID" \
      > /tmp/e2_session_final_state.html

Evaluate outcome:

    if [ -z "$MATCH_CYCLE" ]; then
      echo "STOP: no MATCH within five responses — E-2 NOT ACCEPTED"
      echo "Preserve all output files for owner review."
      echo "Do not create a successful E-2 evidence commit."
      exit 1
    else
      printf 'E-2 ACCEPTED: first MATCH at cycle=%s qid=%s\n' \
        "$MATCH_CYCLE" "$MATCH_QID"
    fi

### 7.6 Progression evidence review

Criterion (b) is assessed from the ordered sequence of saved
HTML files:

    /tmp/e2_session_get_iter_1.html
    /tmp/e2_session_get_iter_2.html
    ... through last executed cycle ...
    /tmp/e2_session_final_state.html

Maturity level, gap type, gap status, and transition value must
be reviewed across this full ordered sequence. The final HTML
alone is not sufficient to establish progression.

### 7.7 Stop the server

Terminal A: Ctrl-C. No further action.

## 8. Evidence to assemble (on ACCEPTED outcome only)

Assemble in one governance-only evidence commit:

`docs/governance/evidence/E2_PATH_N_SMOKE_SESSION_<SID>.md`
containing:
- Evidence execution baseline HEAD (§4 step 4).
- SID and route-provenance statement (§3).
- Per-cycle record for each cycle executed:
  - GET HTML filename.
  - HTTP status of POST.
  - Response text submitted (D-2 array, index n-1).
  - Exact match result printed.
  - Whether stopping condition was met this cycle.
- Cycle number and question ID of first MATCH
  (values of MATCH_CYCLE and MATCH_QID).
- Progression review summary: maturity, gap type, gap status,
  and transition extracted from each saved HTML in order through
  `e2_session_final_state.html`.
- Acceptance criterion check results (§9 a–c).

`docs/governance/evidence/E2_TRANSCRIPT_<SID>.jsonl`
— verbatim copy of `/tmp/ilt002_transcript_<SID>.jsonl`.

`docs/governance/evidence/E2_SESSION_GET_ITER_<n>_<SID>.html`
— one file per executed cycle, copied from
`/tmp/e2_session_get_iter_<n>.html`.

`docs/governance/evidence/E2_SESSION_FINAL_STATE_<SID>.html`
— copied from `/tmp/e2_session_final_state.html`.

Commit message: `evidence: E-2 Path N smoke session <SID>`.
No automatic roadmap or status movement after this commit.

## 9. Acceptance criteria

(a) MATCH_CYCLE is non-empty after the loop: at least one cycle
    produced `MATCH <question-id>`, confirming a Stage 2 gap
    question served byte-for-byte matches an approved N-*
    artifact text. Artifact schema (commit `8ceb5d4`): top-level
    `"gaps"` maps gap-type strings to lists of
    `{"question_id": ..., "text": ...}` objects.
(b) All executed iteration POSTs return HTTP 302; the ordered
    sequence of saved HTML files (§7.6) shows maturity, gap
    state, and transition consistent with deterministic engine
    rules; no anomaly observed across the sequence.
(c) SID was produced by POST to
    `/start_ilt002_combination_lock_path_n`. Committed
    `web/app.py` line 71 sets `state.path = "N"`
    unconditionally in this route. No production code mutates
    `state.path` after session creation (confirmed at `aae15bd`,
    `engine/progression_loop.py` lines 544/584/619 are
    comparisons only). Route provenance is the complete proof
    of this criterion.

## 10. STOP conditions

1. Server fails to start or does not report port 5000.
2. SID empty or not a valid UUID after extraction.
3. Any iteration POST returns a non-302 status.
4. Match command exits non-zero or prints output not equal to
   `MATCH <qid>` or `NO_MATCH` — operational failure; halt;
   paste all output for owner ruling.
5. MATCH_CYCLE empty after five responses — E-2 NOT ACCEPTED;
   do not create a successful evidence commit; preserve all
   output and paste for owner ruling.
6. Progression review reveals maturity or gap state inconsistent
   with deterministic engine rules across the saved HTML sequence.
7. Any pressure to interpret E-2 as Phase 3 completion or as
   making `runtime_integrated=true` eligible without the full
   Phase 4 process (`d2b2a9a` §6: separate owner authorization,
   JSON metadata update, re-testing, recorded re-approval).

## 11. Non-authorizations

No code modification. No test modification. No approved content
artifact mutation. No `domain.json` change. No
`runtime_integrated=true`. No R2. No FORM T movement. No S-6
classification. No AA-5. No Path T. No Professional Workspace.
No Stage 4–7 expansion. No xfail conversion. No automatic
roadmap or status movement after the E-2 evidence commit.