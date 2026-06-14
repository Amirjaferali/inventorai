"""
e2_exact_matcher.py

Standalone exact-text matcher for E-2 safe retry (Gate B, B-1).

Contract:
  stdout: exactly one line
  stderr: empty (guaranteed — no argparse, no traceback)
  exit 0  on MATCH or NO_MATCH
  exit non-zero on STOP

No engine/ imports. Modifies no files.
"""

import json
import os
import sys

DEFAULT_ARTIFACT_PATH = (
    "docs/governance/path_n_content_config/"
    "electronics_electrical_path_n_questions.json"
)


def _stop(message: str) -> None:
    print(f"STOP: {message}")
    sys.exit(1)


def _parse_args(argv: list) -> dict:
    """
    Silent manual parser — never writes to stderr.
    Returns dict with keys: sid, transcript_path, artifact_path (all may be None).
    Calls _stop("invalid argument") on any parse error.
    """
    result = {"sid": None, "transcript_path": None, "artifact_path": None}
    _flag_map = {
        "--sid": "sid",
        "--transcript-path": "transcript_path",
        "--artifact-path": "artifact_path",
    }
    i = 0
    while i < len(argv):
        token = argv[i]
        if token in _flag_map:
            key = _flag_map[token]
            i += 1
            if i >= len(argv) or argv[i].startswith("--"):
                _stop("invalid argument")
            result[key] = argv[i]
        elif token.startswith("--"):
            _stop("invalid argument")
        else:
            _stop("invalid argument")
        i += 1
    return result


def _resolve_sid(args: dict) -> str:
    if args["sid"]:
        return args["sid"]
    env_sid = os.environ.get("SID", "")
    if env_sid:
        return env_sid
    _stop("SID not provided")


def _resolve_transcript_path(args: dict, sid: str) -> str:
    if args["transcript_path"]:
        return args["transcript_path"]
    env_path = os.environ.get("E2_TRANSCRIPT_PATH", "")
    if env_path:
        return env_path
    return f"/tmp/ilt002_transcript_{sid}.jsonl"


def _resolve_artifact_path(args: dict) -> str:
    if args["artifact_path"]:
        return args["artifact_path"]
    env_path = os.environ.get("E2_ARTIFACT_PATH", "")
    if env_path:
        return env_path
    return DEFAULT_ARTIFACT_PATH


def _read_latest_question(transcript_path: str) -> str:
    if not os.path.exists(transcript_path):
        _stop("transcript file not found")

    try:
        with open(transcript_path, "r", encoding="utf-8") as fh:
            lines = [ln for ln in fh.read().splitlines() if ln.strip()]
    except (OSError, UnicodeDecodeError):
        _stop("malformed JSONL in latest record")

    if not lines:
        _stop("transcript file is empty")

    last_line = lines[-1]
    try:
        record = json.loads(last_line)
    except json.JSONDecodeError:
        _stop("malformed JSONL in latest record")

    if not isinstance(record, dict):
        _stop("malformed JSONL in latest record")

    question = record.get("question")
    if question is None or not isinstance(question, str):
        _stop("malformed JSONL in latest record")

    return question


def _load_artifact(artifact_path: str) -> dict:
    if not os.path.exists(artifact_path):
        _stop("artifact file not found")

    try:
        with open(artifact_path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        _stop("artifact schema unexpected")

    if not isinstance(data, dict):
        _stop("artifact schema unexpected")

    if "gaps" not in data or not isinstance(data["gaps"], dict):
        _stop("artifact schema unexpected")

    return data


def _collect_questions(artifact: dict) -> list:
    """Return list of (question_id, text) from all gaps."""
    questions = []
    for gap_questions in artifact["gaps"].values():
        if not isinstance(gap_questions, list):
            _stop("artifact schema unexpected")
        for item in gap_questions:
            if not isinstance(item, dict):
                _stop("artifact schema unexpected")
            qid = item.get("question_id")
            text = item.get("text")
            if not isinstance(qid, str) or not qid:
                _stop("artifact schema unexpected")
            if not isinstance(text, str):
                _stop("artifact schema unexpected")
            questions.append((qid, text))
    return questions


def main() -> None:
    args = _parse_args(sys.argv[1:])

    sid = _resolve_sid(args)
    transcript_path = _resolve_transcript_path(args, sid)
    artifact_path = _resolve_artifact_path(args)

    latest_question = _read_latest_question(transcript_path)
    artifact = _load_artifact(artifact_path)
    questions = _collect_questions(artifact)

    for qid, text in questions:
        if latest_question == text:
            print(f"MATCH {qid}")
            sys.exit(0)

    print("NO_MATCH")
    sys.exit(0)


if __name__ == "__main__":
    main()
