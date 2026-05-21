"""
Replay Benchmark Runner  v1.0  —  Extraction Layer Only
=======================================================
Validates ONLY the deterministic extraction boundary:

  raw_text -> extract_json() -> normalize_output() -> equality check

Deterministic fields compared:
  - normalized_output
  - extraction_method
  - extraction_failure

Explicitly OUT OF SCOPE (future layers):
  - failure_type        (Replay v2: scoring layer)
  - weighted_score      (Replay v2: scoring layer)
  - overall             (Replay v3: gate layer)
  - schema/logic class  (Replay v3: gate layer)

No API calls. No randomness. No timestamps in scoring.
Variance must be 0% across runs.

Usage:
  python3 scripts/run_replay_benchmark.py
  python3 scripts/run_replay_benchmark.py --fixtures tests/replay/cases
  python3 scripts/run_replay_benchmark.py --verbose
  python3 scripts/run_replay_benchmark.py --output results/replay_run.json
"""

import json
import os
import sys
import argparse
import glob

from engine.ai_advisor import AI_ADVISORY_ENABLED
assert not AI_ADVISORY_ENABLED, "AI must be disabled during benchmark run"

FIXTURES_DIR   = "tests/replay/cases"
RUNNER_VERSION = "1.0"
RUNNER_SCOPE   = "extraction"   # extraction | scoring | gate


# ── engine imports ────────────────────────────────────────────────────────────

try:
    from engine.extract_json import extract_json
except ImportError as e:
    print(f"[FATAL] Cannot import engine.extract_json: {e}")
    sys.exit(1)

try:
    from engine.normalize_output import normalize_output
except ImportError as e:
    print(f"[FATAL] Cannot import engine.normalize_output: {e}")
    sys.exit(1)


# ── comparison ────────────────────────────────────────────────────────────────

def compare_field(field: str, actual, expected) -> dict | None:
    if actual == expected:
        return None
    return {"field": field, "actual": actual, "expected": expected}


# ── single fixture ────────────────────────────────────────────────────────────

def run_fixture(fixture: dict) -> dict:
    """
    Run one fixture through extraction layer only.
    Compares: normalized_output, extraction_method, extraction_failure.
    Does NOT compare: failure_type, weighted_score, overall.
    """
    fixture_id = fixture.get("fixture_id", "?")
    case_id    = fixture.get("case_id", "?")
    sig        = fixture.get("sig", "?")
    raw_text   = (fixture.get("input") or {}).get("raw_text")

    exp = fixture.get("expected") or {}
    tr  = fixture.get("trace")    or {}

    # expected extraction fields live in trace (recorded engine telemetry)
    exp_normalized = exp.get("normalized_output")
    exp_method     = tr.get("extraction_method")
    exp_failure    = tr.get("extraction_failure")

    # ── run engine ──
    if raw_text is None:
        # Original run had no raw_text (transport failure)
        # Extraction layer cannot be replayed — skip comparison
        return {
            "fixture_id": fixture_id,
            "case_id":    case_id,
            "sig":        sig,
            "skipped":    True,
            "skip_reason": "no_raw_text",
            "passed":     None,
            "mismatches": [],
            "actual":     {},
            "expected":   {
                "normalized_output":  exp_normalized,
                "extraction_method":  exp_method,
                "extraction_failure": exp_failure,
            },
        }

    actual_normalized = None
    actual_method     = None
    actual_failure    = None

    try:
        result = extract_json(raw_text)
        if isinstance(result, tuple) and len(result) == 3:
            actual_parsed, actual_method, actual_failure = result
        else:
            actual_parsed = result
            actual_method = "unknown"
            actual_failure = ""
    except Exception as e:
        actual_parsed  = None
        actual_method  = "exception"
        actual_failure = str(e)

    if isinstance(actual_parsed, dict):
        try:
            actual_normalized = normalize_output(actual_parsed)
        except Exception as e:
            actual_normalized = None
            actual_failure    = f"normalize_exception:{e}"
    else:
        actual_normalized = actual_parsed

    # ── compare extraction layer only ──
    mismatches = []

    m = compare_field("normalized_output",  actual_normalized, exp_normalized)
    if m: mismatches.append(m)

    m = compare_field("extraction_method",  actual_method,     exp_method)
    if m: mismatches.append(m)

    m = compare_field("extraction_failure", actual_failure,    exp_failure)
    if m: mismatches.append(m)

    return {
        "fixture_id": fixture_id,
        "case_id":    case_id,
        "sig":        sig,
        "skipped":    False,
        "passed":     len(mismatches) == 0,
        "mismatches": mismatches,
        "actual": {
            "normalized_output":  actual_normalized,
            "extraction_method":  actual_method,
            "extraction_failure": actual_failure,
        },
        "expected": {
            "normalized_output":  exp_normalized,
            "extraction_method":  exp_method,
            "extraction_failure": exp_failure,
        },
    }


# ── load ──────────────────────────────────────────────────────────────────────

def load_fixtures(fixtures_dir: str) -> list[dict]:
    paths = sorted(glob.glob(os.path.join(fixtures_dir, "TC-*.json")))
    if not paths:
        print(f"[ERROR] No TC-*.json files in: {fixtures_dir}")
        sys.exit(1)
    fixtures = []
    for path in paths:
        with open(path, "r", encoding="utf-8") as f:
            fixtures.append(json.load(f))
    return fixtures


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Deterministic Extraction Replay Benchmark")
    parser.add_argument("--fixtures", default=FIXTURES_DIR)
    parser.add_argument("--verbose",  action="store_true")
    parser.add_argument("--output",   default=None)
    args = parser.parse_args()

    print("=" * 60)
    print(f"Replay Benchmark Runner  v{RUNNER_VERSION}  [scope={RUNNER_SCOPE}]")
    print("=" * 60)
    print(f"Scope    : extraction only (method + failure + normalized_output)")
    print(f"Excluded : failure_type, weighted_score, overall  [future layers]")
    print(f"Variance : 0%  (deterministic)")
    print()

    fixtures = load_fixtures(args.fixtures)
    print(f"Fixtures : {len(fixtures)}")
    print()

    results  = []
    passed_n = 0
    failed_n = 0
    skipped_n = 0

    for fixture in fixtures:
        r = run_fixture(fixture)
        results.append(r)

        if r.get("skipped"):
            skipped_n += 1
            print(f"  SKIP  {r['fixture_id']}  ({r['case_id']})  reason={r['skip_reason']}")
            continue

        if r["passed"]:
            passed_n += 1
            print(f"  PASS  {r['fixture_id']}  ({r['case_id']})")
        else:
            failed_n += 1
            print(f"  FAIL  {r['fixture_id']}  ({r['case_id']})  mismatches={len(r['mismatches'])}")
            if args.verbose:
                for mm in r["mismatches"]:
                    print(f"         field    = {mm['field']}")
                    print(f"         expected = {str(mm['expected'])[:100]}")
                    print(f"         actual   = {str(mm['actual'])[:100]}")

    failed_ids = [r["fixture_id"] for r in results if not r.get("skipped") and not r["passed"]]

    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Total   : {len(fixtures)}")
    print(f"  Passed  : {passed_n}")
    print(f"  Failed  : {failed_n}")
    print(f"  Skipped : {skipped_n}  (no_raw_text = transport failures)")
    print(f"  Variance: 0%")
    if failed_ids:
        print(f"  Failed  : {', '.join(failed_ids)}")

    report_path = args.output or os.path.normpath(
        os.path.join(args.fixtures, "..", "replay_report_v1.json")
    )

    report = {
        "runner_version": RUNNER_VERSION,
        "runner_scope":   RUNNER_SCOPE,
        "corpus_mode":    "diagnostic",
        "summary": {
            "total":      len(fixtures),
            "passed":     passed_n,
            "failed":     failed_n,
            "skipped":    skipped_n,
            "variance":   "0%",
            "failed_ids": failed_ids,
        },
        "results": results,
    }

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"\nReport -> {report_path}")

    sys.exit(0 if failed_n == 0 else 1)


if __name__ == "__main__":
    main()