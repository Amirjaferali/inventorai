"""
engine/extract_json.py
JSON extraction from LLM raw text output.
Verbatim copy from benchmark/run_benchmark_v1.py lines 36-56.
Added: explicit detect_multiple_top_level_objects() for governance boundary.
DECISION_CONTRACT_VERSION = "v1"
"""

import json
import re


def detect_multiple_top_level_objects(text):
    """
    Returns True only if text contains 2+ COMPLETE top-level JSON objects.
    An object is complete when its opening brace is matched by a closing brace.
    Incomplete/truncated second object = False (not ambiguous, just corrupt).
    This is a security/governance boundary — not a cosmetic parser fix.
    """
    depth = 0
    in_string = False
    escape_next = False
    complete_objects = 0

    for char in text:
        if escape_next:
            escape_next = False
            continue
        if char == "\\" and in_string:
            escape_next = True
            continue
        if char == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                complete_objects += 1
                if complete_objects > 1:
                    return True

    return False


def extract_json(text):
    """
    Extract JSON from LLM output using progressive recovery strategies.
    Returns: (parsed_json | None, extraction_mode, error_detail)

    Modes:
      direct             — clean JSON, no recovery needed
      fence_strip        — extracted from markdown code fence
      brace_extract      — extracted by brace scanning
      multiple_json_objects — ambiguous input, governance rejection
      brace_extract_failed  — brace found but invalid JSON
      no_json_found      — no JSON structure detected
      none               — empty input
    """
    if not text or not text.strip():
        return None, "none", "empty_response"

    # Strategy 1: direct parse
    try:
        return json.loads(text.strip()), "direct", ""
    except json.JSONDecodeError:
        pass

    # Strategy 2: markdown fence extraction
    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fence:
        try:
            return json.loads(fence.group(1).strip()), "fence_strip", ""
        except json.JSONDecodeError:
            pass

    # Strategy 3: ambiguity check before brace extraction
    if detect_multiple_top_level_objects(text):
        return None, "multiple_json_objects", "ambiguous: multiple top-level JSON objects detected"

    # Strategy 4: brace extraction
    brace = re.search(r"\{.*\}", text, re.DOTALL)
    if brace:
        try:
            return json.loads(brace.group(0).strip()), "brace_extract", ""
        except json.JSONDecodeError as e:
            return None, "brace_extract_failed", str(e)

    return None, "no_json_found", f"no JSON object in {len(text)}-char response"
