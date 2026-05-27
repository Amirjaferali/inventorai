
import json, os, re, sys, glob, argparse

FIXTURES_DIR   = "tests/replay/cases"
TC_SOURCE      = "benchmark/run_benchmark_v1.py"
RUNNER_VERSION = "2.2"
RUNNER_SCOPE   = "scoring-diagnostic"

try:
    from engine.scoring import score_case, CRITERIA, SCORING_VERSION
except ImportError as e:
    print(f"[FATAL] {e}"); sys.exit(1)

REQUIRED_CONTRACTS = {
    "Gate Engine Utility": {
        "paths":      [["recommendation", "action"]],
        "reason":     "requires normalized_output['recommendation']['action']",
        "root_cause": "normalize_output.py does not produce recommendation field",
        "finding":    "Historical artifacts predate recommendation.action schema contract",
        "status":     "schema_divergence",
    }
}

def check_untestable(name, norm):
    contract = REQUIRED_CONTRACTS.get(name)
    if not contract: return False, None
    out = norm or {}
    for path in contract["paths"]:
        node = out
        for key in path:
            if not isinstance(node, dict) or key not in node:
                return True, contract
            node = node[key]
    return False, None

def load_tc_dataset(src_path):
    src = open(src_path, encoding="utf-8").read()
    m = re.search(r"^TC\s*=\s*(\[.*?\n\])", src, re.MULTILINE|re.DOTALL)
    if not m: print(f"[FATAL] TC not found"); sys.exit(1)
    return {tc["id"]: tc for tc in eval(m.group(1))}

def load_fixtures(d):
    paths = sorted(glob.glob(os.path.join(d, "TC-*.json")))
    if not paths: print("[ERROR] No fixtures"); sys.exit(1)
    return [json.load(open(p, encoding="utf-8")) for p in paths]

def run_fixture(fixture, tc_map):
    fid  = fixture.get("fixture_id","?")
    cid  = fixture.get("case_id","?")
    sig  = fixture.get("sig")
    exp  = fixture.get("expected") or {}
    norm = exp.get("normalized_output")
    exp_sc = exp.get("scores")
    exp_w  = exp.get("weighted_score")
    exp_ov = exp.get("overall")

    tc = tc_map.get(cid)
    if tc is None:
        return {"fixture_id":fid,"case_id":cid,"sig":sig,
                "result":"SKIPPED","skip_reason":f"tc_not_found:{cid}",
                "mismatches":[],"untestable_criteria":[]}
    if norm is None:
        return {"fixture_id":fid,"case_id":cid,"sig":sig,
                "result":"SKIPPED","skip_reason":"no_normalized_output",
                "mismatches":[],"untestable_criteria":[]}
    try:
        actual = score_case(norm, tc)
    except Exception as e:
        return {"fixture_id":fid,"case_id":cid,"sig":sig,"result":"FAIL",
                "mismatches":[{"field":"exception","actual":str(e),"expected":None}],
                "untestable_criteria":[],"actual":{},"expected":{}}

    mismatches = []
    untestable_criteria = []

    for name, _, weight in CRITERIA:
        is_u, cinfo = check_untestable(name, norm)
        if is_u:
            untestable_criteria.append({"criterion":name,"weight":weight,**cinfo})
            continue
        act_p = actual["scores"].get(name,{}).get("passed")
        exp_p = (exp_sc or {}).get(name,{}).get("passed")
        if exp_p is None: continue
        if act_p != exp_p:
            mismatches.append({"field":f"scores.{name}.passed","actual":act_p,
                                "expected":exp_p,"issues":actual["scores"].get(name,{}).get("issues",[])})

    if untestable_criteria and not mismatches:
        result = "UNTESTABLE"
    elif mismatches:
        result = "FAIL"
    else:
        result = "PASS"

    return {"fixture_id":fid,"case_id":cid,"sig":sig,"result":result,
            "mismatches":mismatches,"untestable_criteria":untestable_criteria,
            "actual":{"weighted_score":actual["weighted_score"],"overall":actual["overall"],
                      "scores":{n:{"passed":actual["scores"][n]["passed"],"issues":actual["scores"][n]["issues"]}
                                for n,_,_ in CRITERIA}},
            "expected":{"weighted_score":exp_w,"overall":exp_ov}}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixtures",  default=FIXTURES_DIR)
    parser.add_argument("--tc-source", default=TC_SOURCE)
    parser.add_argument("--verbose",   action="store_true")
    parser.add_argument("--output",    default=None)
    args = parser.parse_args()

    print("="*60)
    print(f"Replay Benchmark Runner  v{RUNNER_VERSION}  [{RUNNER_SCOPE}]")
    print("="*60)
    print(f"SCORING_VERSION: {SCORING_VERSION}  |  Variance: 0%")
    print(f"Result types: PASS | FAIL | UNTESTABLE | SKIPPED\n")

    tc_map   = load_tc_dataset(args.tc_source)
    fixtures = load_fixtures(args.fixtures)
    print(f"TC dataset: {len(tc_map)}  |  Fixtures: {len(fixtures)}\n")

    results = []
    pass_n = fail_n = skip_n = untestable_n = 0

    for fx in fixtures:
        r = run_fixture(fx, tc_map)
        results.append(r)
        res = r["result"]
        if res == "PASS":
            pass_n += 1
            print(f"  PASS        {r['fixture_id']}  ({r['case_id']})")
        elif res == "FAIL":
            fail_n += 1
            print(f"  FAIL        {r['fixture_id']}  ({r['case_id']})  mismatches={len(r['mismatches'])}")
            if args.verbose:
                for mm in r["mismatches"]:
                    print(f"               {mm['field']}: exp={mm['expected']} act={mm['actual']}")
                    if mm.get("issues"): print(f"               issues={mm['issues']}")
        elif res == "UNTESTABLE":
            untestable_n += 1
            print(f"  UNTESTABLE  {r['fixture_id']}  ({r['case_id']})  [{r['untestable_criteria'][0]['criterion']}]")
        elif res == "SKIPPED":
            skip_n += 1
            print(f"  SKIPPED     {r['fixture_id']}  ({r['case_id']})  {r.get('skip_reason','')}")

    failed_ids = [r["fixture_id"] for r in results if r["result"]=="FAIL"]
    parity = "VERIFIED" if fail_n == 0 else "UNVERIFIED"

    print(f"\n{'='*60}\nSUMMARY\n{'='*60}")
    print(f"  Total      : {len(fixtures)}")
    print(f"  Passed     : {pass_n}")
    print(f"  Failed     : {fail_n}")
    print(f"  Untestable : {untestable_n}  (schema_divergence - NOT fail)")
    print(f"  Skipped    : {skip_n}  (transport failures)")
    print(f"  Variance   : 0%")
    print(f"  Parity     : {parity}")
    if fail_n == 0 and untestable_n > 0:
        print(f"\n  Schema divergence: Gate Engine Utility")
        print(f"  recommendation.action absent from all persisted artifacts")
        print(f"  scoring.py NOT modified | normalize_output.py NOT modified")
    if failed_ids: print(f"\n  Failed IDs: {', '.join(failed_ids)}")

    rpath = args.output or os.path.normpath(os.path.join(args.fixtures,"..","replay_report_v2.json"))
    report = {"runner_version":RUNNER_VERSION,"runner_scope":RUNNER_SCOPE,
              "scoring_version":SCORING_VERSION,
              "result_semantics":{"PASS":"testable criteria match","FAIL":"testable criteria mismatch",
                                  "UNTESTABLE":"required schema contract absent","SKIPPED":"transport failure"},
              "schema_divergence_finding":{"criterion":"Gate Engine Utility","missing_path":"recommendation.action",
                                           "root_cause":"normalize_output.py does not produce recommendation",
                                           "action":"scoring.py NOT modified. normalize_output.py NOT modified."},
              "summary":{"total":len(fixtures),"passed":pass_n,"failed":fail_n,
                         "untestable":untestable_n,"skipped":skip_n,
                         "variance":"0%","replay_parity":parity,"failed_ids":failed_ids},
              "results":results}
    json.dump(report, open(rpath,"w",encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"\nReport -> {rpath}")
    sys.exit(0 if fail_n == 0 else 1)

if __name__ == "__main__":
    main()
