"""Repository Intelligence (RIG) — frozen historical replay verifier.

File-creation contract:
  Path: scripts/verify_repository_intelligence_replay.py
  Purpose: replay the fixed RIG-1B acceptance suite
    (`tests/fixtures/repository_intelligence_replay_v1.json`) through
    `scripts/repository_intelligence.py`. Every case is rebuilt only from its
    recorded historical BASE and HEAD git objects, and the verifier DERIVES
    each advisory scope; the analyzer contains no knowledge of these cases.
  Input contract: optional `--repo PATH` (default: this repository) and
    `--manifest PATH` (default: the committed manifest). Needs the full git
    history of the recorded commits.
  Output contract: deterministic JSON on stdout. Exit 0 = every case
    reproduces its frozen scope, required tests and reason class; exit 1 = at
    least one mismatch; exit 2 = replay unavailable (manifest or history
    missing).
  Prohibited behaviors: explicit acceptance tool only — it is NOT collected
    by pytest and grants RIG no CI authority. No network, no writes.
"""
import argparse
import json
import os
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from scripts import repository_intelligence as rig  # noqa: E402

MANIFEST = os.path.join(_ROOT, "tests", "fixtures", "repository_intelligence_replay_v1.json")


def verify(repo, manifest_path):
    with open(manifest_path, encoding="utf-8") as fh:
        manifest = json.load(fh)
    results, totals = [], {}
    for case in manifest["cases"]:
        parents = rig._git(repo, "rev-parse", f"{case['head']}^1").decode().strip()
        if parents != case["base"]:
            raise rig.AnalysisUnavailable(f"PR #{case['pr']}: recorded base is not the head's first parent")
        report = rig.analyse(repo, case["base"], case["head"])
        scope = report["advisory_scope"]
        totals[scope] = totals.get(scope, 0) + 1
        problems = []
        if scope != case["expected_scope"]:
            problems.append(f"scope {scope} != expected {case['expected_scope']}")
        missing = sorted(set(case.get("required_tests", ())) - set(report["candidate_tests"]))
        if missing:
            problems.append(f"required tests not proposed: {missing}")
        if case.get("expected_reason") and not any(r.startswith(case["expected_reason"]) for r in report["policy_reasons"]):
            problems.append(f"expected reason class {case['expected_reason']!r} absent")
        results.append({
            "pr": case["pr"], "label": case["label"], "base": case["base"], "head": case["head"],
            "expected_scope": case["expected_scope"], "derived_scope": scope,
            "candidate_tests": len(report["candidate_tests"]), "evidence_tests": len(report["evidence_tests"]),
            "observer_tests_added": report["scope_widening"]["observer_tests_added"],
            "policy_reasons": report["policy_reasons"], "ok": not problems, "problems": problems,
        })
    ok = all(r["ok"] for r in results) and totals == manifest["expected_totals"]
    return {"manifest_id": manifest["manifest_id"], "contract_version": rig.CONTRACT_VERSION,
            "tool_version": rig.TOOL_VERSION, "authority": "advisory-only", "ok": ok,
            "derived_totals": dict(sorted(totals.items())), "expected_totals": manifest["expected_totals"],
            "cases": results}


def main(argv=None):
    p = argparse.ArgumentParser(description="Verify the frozen RIG historical replay (advisory evidence only).")
    p.add_argument("--repo", default=_ROOT)
    p.add_argument("--manifest", default=MANIFEST)
    args = p.parse_args(argv)
    try:
        out = verify(args.repo, args.manifest)
    except (OSError, ValueError, rig.AnalysisUnavailable) as exc:
        print(json.dumps({"ok": False, "replay_status": "unavailable", "reason": str(exc)}, indent=2, sort_keys=True))
        return 2
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0 if out["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
