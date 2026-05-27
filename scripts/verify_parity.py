"""
scripts/verify_parity.py
Benchmark parity verifier — hardened, fail-safe.
Usage: python3 scripts/verify_parity.py <new_results.json>
"""
import json, sys, os

CANONICAL = 'benchmarks/baseline_canonical_score93.json'
GOLDEN_DIR = 'tests/golden'

FORBIDDEN_IN_ENGINE = [
    'os.environ', 'urllib', 'requests', 'open(',
    'sys.exit', 'subprocess', 'socket', 'threading',
    'asyncio', 'multiprocessing'
]

def load(path):
    if not os.path.exists(path):
        raise SystemExit(f"PARITY ERROR: file not found: {path}")
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def verify(new_path):
    new_path = os.path.normpath(new_path)
    canon = load(CANONICAL)
    new   = load(new_path)
    errors = []

    # 1. Score parity
    c_score = canon["meta"]["avg_weighted"]
    n_score = new["meta"]["avg_weighted"]
    if c_score != n_score:
        errors.append(f"SCORE MISMATCH: canonical={c_score} new={n_score}")

    # 2. Valid count parity
    c_valid = canon["meta"]["valid"]
    n_valid = new["meta"]["valid"]
    if c_valid != n_valid:
        errors.append(f"VALID COUNT MISMATCH: canonical={c_valid} new={n_valid}")

    # 3. Schema compliance parity
    c_schema = canon["meta"]["schema_pct"]
    n_schema = new["meta"]["schema_pct"]
    if c_schema != n_schema:
        errors.append(f"SCHEMA PCT MISMATCH: canonical={c_schema} new={n_schema}")

    # 4. Per-case decision parity
    canon_map = {c["id"]: c for c in canon["cases"]}
    new_map   = {c["id"]: c for c in new["cases"]}

    for cid, cc in canon_map.items():
        nc = new_map.get(cid)
        if not nc:
            errors.append(f"MISSING CASE: {cid}")
            continue
        c_out = cc.get("parsed_output") or {}
        n_out = nc.get("parsed_output") or {}
        for field in ["schema_version", "domain"]:
            cv = c_out.get(field)
            nv = n_out.get(field)
            if cv and nv and cv != nv:
                errors.append(f"FIELD MISMATCH {cid}.{field}: canonical={cv} new={nv}")
        c_sig = (c_out.get("feasibility") or {}).get("feasibility_signal")
        n_sig = (n_out.get("feasibility") or {}).get("feasibility_signal")
        if c_sig and n_sig and c_sig != n_sig:
            errors.append(f"SIGNAL MISMATCH {cid}: canonical={c_sig} new={n_sig}")

    # 5. Golden snapshot comparison
    if os.path.exists(GOLDEN_DIR):
        for fname in sorted(os.listdir(GOLDEN_DIR)):
            if not fname.endswith("_expected.json"):
                continue
            cid = fname.split("_")[0]
            golden = load(f"{GOLDEN_DIR}/{fname}")
            nc = new_map.get(cid)
            if not nc:
                errors.append(f"GOLDEN MISSING IN NEW: {cid}")
                continue
            g_scores = golden.get("scores", {})
            n_scores = {k: v.get("passed") for k, v in nc.get("scores", {}).items() if isinstance(v, dict)}
            for criterion, expected in g_scores.items():
                actual = n_scores.get(criterion)
                if expected != actual:
                    errors.append(f"GOLDEN SCORE MISMATCH {cid}.{criterion}: expected={expected} actual={actual}")

    # Report
    if errors:
        print("PARITY FAILED:")
        for e in errors:
            print(f"  ERROR: {e}")
        sys.exit(1)
    else:
        print(f"PARITY OK: score={n_score}, valid={n_valid}, schema={n_schema}%")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/verify_parity.py <new_results.json>")
        sys.exit(1)
    verify(sys.argv[1])
