"""
Replay Fixture Collector  v2.1
CORPUS MODE: diagnostic (prefer failed cases)

Fixture schema — strict layer separation:
  input:      frozen replay boundary
  expected:   case-level truth only (no run aggregates)
  trace:      extraction + transport telemetry
  provenance: origin metadata only
"""

import json
import os
import glob
from datetime import datetime, timezone
from collections import Counter

RESULTS_DIR  = "benchmark"
OUTPUT_DIR   = "tests/replay/cases"
RESULTS_GLOB = os.path.join(RESULTS_DIR, "results_*.json")
CORPUS_MODE  = "diagnostic"

TIMEOUT_SIGNALS = {"timeout", "timedout", "timeouterror", "readtimeout", "connecttimeout"}
TRANSPORT_CODES = {408, 429, 500, 502, 503, 504}


def resolve_failure_type(case):
    if case.get("overall") is True:
        return None
    ec = case.get("error_category")
    if ec:
        ec_norm = str(ec).lower().replace(" ", "").replace("_", "")
        if any(t in ec_norm for t in TIMEOUT_SIGNALS):
            return "timeout"
        return str(ec)
    http_status = case.get("http_status")
    if http_status and int(http_status) in TRANSPORT_CODES:
        return "timeout"
    ef = case.get("extraction_failure")
    if ef and str(ef).strip().lower() not in ("", "none", "false"):
        return "extraction"
    scores = case.get("scores") or {}
    failed = [
        name for name, result in scores.items()
        if isinstance(result, dict) and result.get("passed") is False
    ]
    if failed:
        names = " ".join(failed).lower()
        if "schema" in names:
            return "schema"
        if "restraint" in names or "logic" in names:
            return "logic"
        return "logic"
    return "unknown"


def recorded_at_from_filename(filename):
    stem = os.path.basename(filename).replace("results_", "").replace(".json", "")
    try:
        dt = datetime.strptime(stem, "%Y%m%d_%H%M%S")
        return dt.replace(tzinfo=timezone.utc).isoformat()
    except ValueError:
        return datetime.now(timezone.utc).isoformat()


def extract_fixtures(results_path):
    with open(results_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict):
        cases_raw = data.get("cases") or []
        meta      = data.get("meta") or {}
    elif isinstance(data, list):
        cases_raw = data
        meta      = {}
    else:
        print(f"  [SKIP] Unrecognized format: {results_path}")
        return []
    source_file    = os.path.basename(results_path)
    recorded_at    = recorded_at_from_filename(results_path)
    model          = meta.get("model")
    schema_version = meta.get("schema_version")
    fixtures = []
    for case in cases_raw:
        if not isinstance(case, dict):
            continue
        case_id = case.get("id")
        if not case_id:
            continue
        failure_type = resolve_failure_type(case)
        fixture = {
            "fixture_id": None,
            "case_id":    case_id,
            "sig":        case.get("sig"),
            "input": {
                "raw_text":    case.get("raw_text"),
                "http_status": case.get("http_status"),
            },
            "expected": {
                "overall":           case.get("overall"),
                "failure_type":      failure_type,
                "weighted_score":    case.get("weighted_score"),
                "scores":            case.get("scores"),
                "normalized_output": case.get("normalized_output"),
            },
            "trace": {
                "extraction_method":  case.get("extraction_method"),
                "extraction_failure": case.get("extraction_failure"),
                "parsed_output":      case.get("parsed_output"),
                "http_error_body":    case.get("http_error_body"),
                "error_category":     case.get("error_category"),
                "error_detail":       case.get("error_detail"),
                "error":              case.get("error"),
            },
            "provenance": {
                "source_results_file": source_file,
                "recorded_at":         recorded_at,
                "corpus_mode":         CORPUS_MODE,
                "model":               model,
                "schema_version":      schema_version,
            },
        }
        fixtures.append(fixture)
    return fixtures


def deduplicate_diagnostic(all_fixtures):
    by_id = {}
    for fx in all_fixtures:
        cid      = fx["case_id"]
        existing = by_id.get(cid)
        if existing is None:
            by_id[cid] = fx
            continue
        fx_failed = fx["expected"]["overall"] is False
        ex_failed = existing["expected"]["overall"] is False
        if fx_failed and not ex_failed:
            by_id[cid] = fx
        elif ex_failed and not fx_failed:
            continue
        elif fx["provenance"]["recorded_at"] > existing["provenance"]["recorded_at"]:
            by_id[cid] = fx
    return list(by_id.values())


def write_fixtures(fixtures, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    ordered = sorted(
        fixtures,
        key=lambda f: (0 if f["expected"]["overall"] is False else 1, str(f.get("case_id", "")))
    )
    for idx, fixture in enumerate(ordered, start=1):
        fixture["fixture_id"] = f"TC-{idx:02d}"
        path = os.path.join(output_dir, f"TC-{idx:02d}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(fixture, f, indent=2, ensure_ascii=False)
    return ordered


def write_index(ordered, output_dir):
    index = []
    for fx in ordered:
        index.append({
            "fixture_id":        fx.get("fixture_id"),
            "case_id":           fx.get("case_id"),
            "sig":               fx.get("sig"),
            "overall":           fx["expected"]["overall"],
            "failure_type":      fx["expected"]["failure_type"],
            "weighted_score":    fx["expected"]["weighted_score"],
            "extraction_method": fx["trace"]["extraction_method"],
            "corpus_mode":       fx["provenance"]["corpus_mode"],
            "source":            fx["provenance"]["source_results_file"],
            "recorded_at":       fx["provenance"]["recorded_at"],
        })
    index_path = os.path.join(output_dir, "INDEX.json")
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump({"corpus_mode": CORPUS_MODE, "fixtures": index}, f, indent=2, ensure_ascii=False)
    print(f"  INDEX  -> {index_path}")


def main():
    print("=" * 60)
    print(f"Replay Fixture Collector  v2.1  [mode={CORPUS_MODE}]")
    print("=" * 60)
    print("WARNING: corpus_mode=diagnostic")
    print("  Failed cases preferred. Not a latest-state corpus.")

    results_files = sorted(glob.glob(RESULTS_GLOB))
    if not results_files:
        print(f"\n[ERROR] No files found: {RESULTS_GLOB}")
        return

    print(f"\nResults files: {len(results_files)}")
    for rf in results_files:
        print(f"  {rf}")

    all_fixtures = []
    for rf in results_files:
        print(f"\nProcessing: {os.path.basename(rf)}")
        try:
            fx = extract_fixtures(rf)
            print(f"  Cases: {len(fx)}")
            all_fixtures.extend(fx)
        except Exception as e:
            print(f"  [ERROR] {e}")

    if not all_fixtures:
        print("\n[ERROR] No cases extracted.")
        return

    print(f"\nTotal raw     : {len(all_fixtures)}")
    unique = deduplicate_diagnostic(all_fixtures)
    print(f"After dedup   : {len(unique)}")

    passed = sum(1 for f in unique if f["expected"]["overall"] is True)
    failed = sum(1 for f in unique if f["expected"]["overall"] is False)
    ft_ctr = Counter(f["expected"]["failure_type"] for f in unique if f["expected"]["overall"] is False)
    em_ctr = Counter(f["trace"]["extraction_method"] for f in unique)

    print(f"\nVerdict:")
    print(f"  overall=True  : {passed}")
    print(f"  overall=False : {failed}")
    if ft_ctr:
        print(f"  failure_type:")
        for ft, n in sorted(ft_ctr.items(), key=lambda x: str(x[0])):
            print(f"    {str(ft):15s}: {n}")
    print(f"\nExtraction method:")
    for em, n in sorted(em_ctr.items(), key=lambda x: str(x[0])):
        print(f"  {str(em):20s}: {n}")

    ordered = write_fixtures(unique, OUTPUT_DIR)
    write_index(ordered, OUTPUT_DIR)

    print(f"\n{'=' * 60}")
    print(f"Done. {len(ordered)} fixture(s) -> {OUTPUT_DIR}/")
    print(f"{'=' * 60}")
    print(f"\nNext step:")
    print(f"  python3 scripts/run_replay_benchmark.py")


if __name__ == "__main__":
    main()
