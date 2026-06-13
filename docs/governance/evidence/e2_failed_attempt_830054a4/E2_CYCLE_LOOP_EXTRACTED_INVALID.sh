
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

