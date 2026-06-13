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
