"""
test_e2_exact_matcher.py

Behavioral tests for scripts/e2_exact_matcher.py (Gate B, B-1).

9 tests covering:
  1. approved exact match
  2. valid nonmatch
  3. missing SID
  4. missing transcript
  5. empty transcript
  6. malformed JSONL (invalid JSON + invalid UTF-8)
  7. missing artifact fixture
  8. malformed artifact fixture (missing gaps + invalid UTF-8)
  9. CLI parse failure (unknown flag + missing option value)

Every test asserts stdout, stderr, and exit code.
All fixtures use tmp_path. No committed file is modified.
"""

import json
import subprocess
import sys
from pathlib import Path

MATCHER = Path(__file__).parent.parent / "scripts" / "e2_exact_matcher.py"
PYTHON = sys.executable

APPROVED_QID = "N-MC-1"
APPROVED_TEXT = (
    "Explain in everyday words how you imagine the system would notice "
    "the problem and respond."
)


def _artifact(tmp_path: Path, questions=None) -> Path:
    if questions is None:
        questions = [
            {"question_id": APPROVED_QID, "text": APPROVED_TEXT},
            {"question_id": "N-MC-2", "text": "What are the main parts?"},
        ]
    data = {
        "metadata": {"runtime_integrated": False},
        "gaps": {
            "MECHANISM_COMPLETENESS": questions,
        },
    }
    p = tmp_path / "artifact.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    return p


def _transcript(tmp_path: Path, question: str) -> Path:
    record = {
        "session_id": "test-sid",
        "iteration": 1,
        "question": question,
        "response": "some response",
        "domain": "electronics_electrical",
        "timestamp": "2026-01-01T00:00:00Z",
    }
    p = tmp_path / "transcript.jsonl"
    p.write_text(json.dumps(record) + "\n", encoding="utf-8")
    return p


def _run(args: list, env: dict = None) -> tuple:
    import os
    base_env = os.environ.copy()
    for key in ("SID", "E2_TRANSCRIPT_PATH", "E2_ARTIFACT_PATH"):
        base_env.pop(key, None)
    if env:
        base_env.update(env)
    result = subprocess.run(
        [PYTHON, str(MATCHER)] + args,
        capture_output=True,
        text=True,
        env=base_env,
    )
    return result.stdout.strip(), result.stderr.strip(), result.returncode


def test_approved_exact_match(tmp_path):
    art = _artifact(tmp_path)
    tr = _transcript(tmp_path, APPROVED_TEXT)
    stdout, stderr, code = _run(
        ["--sid", "test-sid",
         "--transcript-path", str(tr),
         "--artifact-path", str(art)]
    )
    assert stdout == f"MATCH {APPROVED_QID}"
    assert stderr == ""
    assert code == 0


def test_valid_nonmatch(tmp_path):
    art = _artifact(tmp_path)
    tr = _transcript(tmp_path, "This question is not in the artifact at all.")
    stdout, stderr, code = _run(
        ["--sid", "test-sid",
         "--transcript-path", str(tr),
         "--artifact-path", str(art)]
    )
    assert stdout == "NO_MATCH"
    assert stderr == ""
    assert code == 0


def test_missing_sid(tmp_path):
    art = _artifact(tmp_path)
    tr = _transcript(tmp_path, APPROVED_TEXT)
    stdout, stderr, code = _run(
        ["--transcript-path", str(tr),
         "--artifact-path", str(art)]
    )
    assert stdout == "STOP: SID not provided"
    assert stderr == ""
    assert code != 0


def test_missing_transcript(tmp_path):
    art = _artifact(tmp_path)
    missing = tmp_path / "does_not_exist.jsonl"
    stdout, stderr, code = _run(
        ["--sid", "test-sid",
         "--transcript-path", str(missing),
         "--artifact-path", str(art)]
    )
    assert stdout == "STOP: transcript file not found"
    assert stderr == ""
    assert code != 0


def test_empty_transcript(tmp_path):
    art = _artifact(tmp_path)
    tr = tmp_path / "empty.jsonl"
    tr.write_text("", encoding="utf-8")
    stdout, stderr, code = _run(
        ["--sid", "test-sid",
         "--transcript-path", str(tr),
         "--artifact-path", str(art)]
    )
    assert stdout == "STOP: transcript file is empty"
    assert stderr == ""
    assert code != 0


def test_malformed_jsonl(tmp_path):
    art = _artifact(tmp_path)

    # Case A: invalid JSON text
    tr_bad_json = tmp_path / "bad_json.jsonl"
    tr_bad_json.write_text("not valid json\n", encoding="utf-8")
    stdout_a, stderr_a, code_a = _run(
        ["--sid", "test-sid",
         "--transcript-path", str(tr_bad_json),
         "--artifact-path", str(art)]
    )
    assert stdout_a == "STOP: malformed JSONL in latest record"
    assert stderr_a == ""
    assert code_a != 0

    # Case B: invalid UTF-8 bytes
    tr_bad_utf8 = tmp_path / "bad_utf8.jsonl"
    tr_bad_utf8.write_bytes(b"\xff\xfe invalid utf-8\n")
    stdout_b, stderr_b, code_b = _run(
        ["--sid", "test-sid",
         "--transcript-path", str(tr_bad_utf8),
         "--artifact-path", str(art)]
    )
    assert stdout_b == "STOP: malformed JSONL in latest record"
    assert stderr_b == ""
    assert code_b != 0


def test_missing_artifact(tmp_path):
    tr = _transcript(tmp_path, APPROVED_TEXT)
    missing_art = tmp_path / "no_artifact.json"
    stdout, stderr, code = _run(
        ["--sid", "test-sid",
         "--transcript-path", str(tr),
         "--artifact-path", str(missing_art)]
    )
    assert stdout == "STOP: artifact file not found"
    assert stderr == ""
    assert code != 0


def test_malformed_artifact(tmp_path):
    tr = _transcript(tmp_path, APPROVED_TEXT)

    # Case A: valid JSON but missing "gaps" key
    bad_art = tmp_path / "bad_artifact.json"
    bad_art.write_text('{"metadata": {}}', encoding="utf-8")
    stdout_a, stderr_a, code_a = _run(
        ["--sid", "test-sid",
         "--transcript-path", str(tr),
         "--artifact-path", str(bad_art)]
    )
    assert stdout_a == "STOP: artifact schema unexpected"
    assert stderr_a == ""
    assert code_a != 0

    # Case B: invalid UTF-8 bytes
    bad_art_utf8 = tmp_path / "bad_artifact_utf8.json"
    bad_art_utf8.write_bytes(b"\xff\xfe not utf-8 json\n")
    stdout_b, stderr_b, code_b = _run(
        ["--sid", "test-sid",
         "--transcript-path", str(tr),
         "--artifact-path", str(bad_art_utf8)]
    )
    assert stdout_b == "STOP: artifact schema unexpected"
    assert stderr_b == ""
    assert code_b != 0


def test_cli_parse_failure(tmp_path):
    # Case A: unknown flag
    stdout_a, stderr_a, code_a = _run(["--unknown-flag", "value"])
    assert stdout_a == "STOP: invalid argument"
    assert stderr_a == ""
    assert code_a != 0

    # Case B: recognized flag with missing value (--sid with no argument)
    stdout_b, stderr_b, code_b = _run(["--sid"])
    assert stdout_b == "STOP: invalid argument"
    assert stderr_b == ""
    assert code_b != 0
