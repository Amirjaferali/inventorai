"""Repository Intelligence (RIG) — shadow comparator and fast-feedback planner (RIG-2A).

File-creation contract:
  Path: scripts/repository_intelligence_shadow.py
  Purpose: ADVISORY telemetry around the authoritative FULL CI. Three modes:
    `compare` (default) — after the authoritative FULL pytest run, compare
      RIG's proposal (`scripts/repository_intelligence.py` JSON) with the FULL
      JUnit XML: failing identities, whether each failing test's file was in
      RIG's candidate set, omitted and unmappable failures, and failure recall
      ONLY when failure evidence exists.
    `fast-plan` — for the separate, non-required fast-feedback job: analyse
      EXPECTED_BASE → EXPECTED_MERGE with RIG and, only for an
      AFFECTED-CANDIDATE proposal whose every candidate is a tracked test file
      at the tested merge, write the validated candidate list to a plan file.
    `fast-report` — turn the fast lane's pytest exit code + JUnit into
      FAST_FEEDBACK_PASS / FAIL / UNAVAILABLE / NOT_APPLICABLE and a summary
      that says NOT A MERGE GATE; FULL CI REMAINS AUTHORITATIVE.
  Input contract: see `--help`. Missing or unreadable inputs are reported as
    unavailable, never guessed.
  Output contract: deterministic JSON on stdout; optional Markdown appended to
    `--summary`; optional `key=value` lines appended to `--outputs`. Exit code
    is ALWAYS 0: nothing here has authority over CI status.
  Prohibited behaviors: this tool never runs pytest and never selects, skips
    or reorders the authoritative FULL regression; the fast lane's selected
    run happens only in its own advisory job. No writes inside the
    repository, no network, no LLM, no credential, no third-party package.
    A green FULL run is never reported as 100% recall.
"""
import argparse
import json
import os
import posixpath
import sys
import xml.etree.ElementTree as ET

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

SHADOW_VERSION = "rig-shadow-2a.2"
AUTHORITY = "advisory-only: FULL pytest in 'Verify candidate' decides CI status; RIG selected and skipped nothing there"

# Shadow comparison statuses (closed vocabulary).
NO_FAILURE_EVIDENCE = "NO_FAILURE_EVIDENCE"
FULL_ADVISORY = "FULL_ADVISORY"
AFFECTED_CANDIDATE_GREEN_FULL = "AFFECTED_CANDIDATE_GREEN_FULL"
AFFECTED_CANDIDATE_FAILURES_COVERED = "AFFECTED_CANDIDATE_FAILURES_COVERED"
SHADOW_MISS = "SHADOW_MISS"
RIG_UNAVAILABLE = "RIG_UNAVAILABLE"
FULL_EVIDENCE_UNAVAILABLE = "FULL_EVIDENCE_UNAVAILABLE"
STATUSES = (NO_FAILURE_EVIDENCE, FULL_ADVISORY, AFFECTED_CANDIDATE_GREEN_FULL,
            AFFECTED_CANDIDATE_FAILURES_COVERED, SHADOW_MISS, RIG_UNAVAILABLE, FULL_EVIDENCE_UNAVAILABLE)

# Fast-feedback statuses (closed vocabulary, advisory only).
FAST_PASS = "FAST_FEEDBACK_PASS"
FAST_FAIL = "FAST_FEEDBACK_FAIL"
FAST_UNAVAILABLE = "FAST_FEEDBACK_UNAVAILABLE"
FAST_NOT_APPLICABLE = "FAST_FEEDBACK_NOT_APPLICABLE"
FAST_STATUSES = (FAST_PASS, FAST_FAIL, FAST_UNAVAILABLE, FAST_NOT_APPLICABLE)
FAST_PLANNED = "PLANNED"                     # internal plan state only: selected tests MAY run; not a result


# ─────────────────────────────────────────────────────────────────────────────
# inputs
# ─────────────────────────────────────────────────────────────────────────────

def load_rig(path):
    """Returns (report or None, reason)."""
    if not path or not os.path.isfile(path):
        return None, "rig report missing"
    try:
        with open(path, encoding="utf-8") as fh:
            report = json.load(fh)
    except (OSError, ValueError) as exc:
        return None, f"rig report unreadable: {type(exc).__name__}"
    if not isinstance(report, dict) or report.get("analysis_status") == "unavailable" or "advisory_scope" not in report:
        reason = report.get("reason", "no advisory scope") if isinstance(report, dict) else "not an object"
        return None, f"rig analysis unavailable: {reason}"
    return report, "ok"


def map_to_test_file(classname, name, repo):
    """Deterministic JUnit classname -> tracked test file: `tests.test_mod` and
    `tests.test_mod.TestClass` both map to `tests/test_mod.py`; a collection
    error (empty classname, module in `name`) maps the same way. None when no
    existing test module can be established."""
    parts = [p for p in (classname or name or "").split(".") if p]
    for k in range(len(parts), 0, -1):
        rel = "/".join(parts[:k]) + ".py"
        if rel.startswith("tests/") and os.path.isfile(os.path.join(repo, rel)):
            return rel
    return None


def load_junit(path, repo):
    """Returns (cases or None, reason)."""
    if not path or not os.path.isfile(path):
        return None, "junit report missing"
    try:
        root = ET.parse(path).getroot()
    except (OSError, ET.ParseError) as exc:
        return None, f"junit report unreadable: {type(exc).__name__}"
    cases = []
    for case in root.iter("testcase"):
        classname, name = case.get("classname") or "", case.get("name") or ""
        if case.find("error") is not None:
            outcome = "error"
        elif case.find("failure") is not None:
            outcome = "failure"
        elif case.find("skipped") is not None:
            outcome = "skipped"
        else:
            outcome = "passed"
        cases.append({"identity": f"{classname}::{name}" if classname else name,
                      "file": map_to_test_file(classname, name, repo), "outcome": outcome})
    if not cases:
        return None, "junit report has no test cases"
    return cases, "ok"


def _identity(rig, pr_head, tested_merge):
    ident = (rig or {}).get("identity", {})
    return {"pr_head": pr_head, "tested_merge": tested_merge,
            "analysis_base": ident.get("base"), "analysis_head": ident.get("head")}


# ─────────────────────────────────────────────────────────────────────────────
# compare (post-FULL shadow evidence)
# ─────────────────────────────────────────────────────────────────────────────

def compare(rig, rig_reason, cases, junit_reason, pr_head=None, tested_merge=None):
    failing = [c for c in cases if c["outcome"] in ("failure", "error")] if cases else []
    full_files = sorted({c["file"] for c in cases if c["file"]}) if cases else []
    out = {
        "shadow_version": SHADOW_VERSION, "authority": AUTHORITY,
        **_identity(rig, pr_head, tested_merge),
        "rig_status": "available" if rig else "unavailable", "rig_reason": rig_reason,
        "full_evidence": "available" if cases else "unavailable", "full_evidence_reason": junit_reason,
        "full_test_cases": len(cases) if cases else 0, "full_test_files": len(full_files),
        "failures_total": len(failing),
        "failing_tests": sorted(c["identity"] for c in failing),
        "unmapped_failures": sorted(c["identity"] for c in failing if not c["file"]),
    }
    if rig:
        candidates = set(rig.get("candidate_tests", ()))
        out.update({
            "contract_version": rig.get("rig", {}).get("contract_version"),
            "tool_version": rig.get("rig", {}).get("tool_version"),
            "analysis_status": rig.get("analysis_health", {}).get("head", {}).get("status", "unknown"),
            "advisory_scope": rig["advisory_scope"],
            "policy_reasons": sorted(rig.get("policy_reasons", ())),
            "candidate_tests": len(candidates),
            "evidence_tests": len(rig.get("evidence_tests", ())),
            "observer_tests_added": rig.get("scope_widening", {}).get("observer_tests_added"),
            "uncertainty_count": len(rig.get("uncertainties_in_scope", ())),
            "central_or_shared": rig.get("central_or_shared"),
            "selection_ratio": round(len(candidates) / len(full_files), 4) if full_files else None,
        })
        omitted = [c for c in failing if not (c["file"] and c["file"] in candidates)]
        out["failures_in_candidate"] = len(failing) - len(omitted)
        out["failures_omitted"] = len(omitted)
        out["omitted_failing_tests"] = sorted(f"{c['identity']} [{c['file'] or 'UNMAPPED FAILURE'}]" for c in omitted)
    if not cases:
        status = FULL_EVIDENCE_UNAVAILABLE
    elif not rig:
        status = RIG_UNAVAILABLE
    elif rig["advisory_scope"] == "FULL":
        status = FULL_ADVISORY
    elif out["failures_omitted"]:
        status = SHADOW_MISS
    elif rig["advisory_scope"] == "AFFECTED-CANDIDATE":
        status = AFFECTED_CANDIDATE_FAILURES_COVERED if failing else AFFECTED_CANDIDATE_GREEN_FULL
    else:
        status = NO_FAILURE_EVIDENCE
    out["shadow_status"] = status
    if rig and failing and rig["advisory_scope"] != "FULL":
        out["failure_recall"] = round(out["failures_in_candidate"] / len(failing), 4)
        out["failure_recall_evidence"] = "PRESENT"
    else:
        out["failure_recall"] = None
        out["failure_recall_evidence"] = ("NOT_APPLICABLE (advisory FULL)"
                                          if rig and failing and rig["advisory_scope"] == "FULL" else "NONE")
    return out


def compare_summary(r):
    keys = ("pr_head", "tested_merge", "analysis_base", "analysis_head", "analysis_status", "advisory_scope",
            "candidate_tests", "evidence_tests", "observer_tests_added", "full_test_files", "selection_ratio",
            "uncertainty_count", "failures_total", "failures_in_candidate", "failures_omitted",
            "failure_recall", "failure_recall_evidence", "shadow_status")
    lines = ["", "### RIG SHADOW — ADVISORY ONLY", "",
             "FULL pytest is authoritative; RIG selected and skipped nothing in this job.", "",
             "| field | value |", "|---|---|"]
    lines += [f"| {k} | `{r.get(k)}` |" for k in keys if k in r]
    if r.get("rig_status") != "available":
        lines.append(f"| rig_reason | `{r.get('rig_reason')}` |")
    if r.get("shadow_status") == SHADOW_MISS:
        lines += ["", "**SHADOW_MISS** — FULL failures outside the RIG proposal:", ""]
        lines += [f"- `{t}`" for t in r.get("omitted_failing_tests", ())]
    return "\n".join(lines) + "\n"


# ─────────────────────────────────────────────────────────────────────────────
# fast-plan / fast-report (separate advisory fast-feedback job)
# ─────────────────────────────────────────────────────────────────────────────

def plan_fast(report, tracked_paths):
    """Pure decision: returns (status, validated candidate list, reason).
    Only a valid AFFECTED-CANDIDATE proposal yields a non-empty list."""
    if not isinstance(report, dict) or report.get("analysis_status") == "unavailable" or "advisory_scope" not in report:
        return FAST_UNAVAILABLE, [], "rig analysis unavailable"
    scope = report["advisory_scope"]
    if scope != "AFFECTED-CANDIDATE":
        return FAST_NOT_APPLICABLE, [], f"advisory scope is {scope}: no affected subset is proposed"
    cands = report.get("candidate_tests")
    if not isinstance(cands, list) or not cands:
        return FAST_UNAVAILABLE, [], "candidate list missing or empty"
    for c in cands:
        if not isinstance(c, str) or not c or c.startswith(("/", "-")) or "\\" in c or "\0" in c:
            return FAST_UNAVAILABLE, [], f"invalid candidate entry: {c!r}"
        if posixpath.normpath(c) != c or not c.startswith("tests/") or not c.endswith(".py") \
                or not posixpath.basename(c).startswith("test_"):
            return FAST_UNAVAILABLE, [], f"candidate is not a repository test file: {c!r}"
        if c not in tracked_paths:
            return FAST_UNAVAILABLE, [], f"candidate not tracked at the tested merge: {c!r}"
    return FAST_PLANNED, sorted(set(cands)), "validated"


def fast_plan(repo, base, merge, pr_head):
    from scripts import repository_intelligence as rig
    try:
        report = rig.analyse(repo, base, merge)
        tracked = rig.Snapshot(repo, merge).paths
    except Exception as exc:                                  # advisory lane: never guess
        return {"fast_status": FAST_UNAVAILABLE, "run_fast": False, "reason": f"rig unavailable: {type(exc).__name__}",
                "pr_head": pr_head, "tested_merge": merge, "analysis_base": base, "analysis_head": merge,
                "candidates": []}
    status, cands, reason = plan_fast(report, tracked)
    run = status == FAST_PLANNED
    return {"fast_status": status, "run_fast": run, "reason": reason,
            "pr_head": pr_head, "tested_merge": merge, "analysis_base": base, "analysis_head": merge,
            "advisory_scope": report.get("advisory_scope"), "policy_reasons": report.get("policy_reasons", []),
            "candidates": cands, "candidate_tests": len(cands),
            "total_tests": sum(1 for t in tracked if t.startswith("tests/") and t.endswith(".py")
                               and posixpath.basename(t).startswith("test_"))}


def fast_report(plan, exit_code, cases):
    if not plan or not plan.get("run_fast"):
        status = (plan or {}).get("fast_status", FAST_UNAVAILABLE)
        pytest_outcome = "not run"
    elif exit_code is None or cases is None:
        status, pytest_outcome = FAST_UNAVAILABLE, "no fast pytest evidence"
    elif exit_code == 0:
        status, pytest_outcome = FAST_PASS, "selected candidate tests passed"
    else:
        status, pytest_outcome = FAST_FAIL, f"selected candidate tests failed (pytest exit {exit_code})"
    failing = sorted(c["identity"] for c in (cases or []) if c["outcome"] in ("failure", "error"))
    total = (plan or {}).get("total_tests") or 0
    return {"shadow_version": SHADOW_VERSION, "lane": "fast-feedback (advisory, NOT A MERGE GATE)",
            "fast_status": status, "pytest_outcome": pytest_outcome, "failing_tests": failing,
            "pr_head": (plan or {}).get("pr_head"), "tested_merge": (plan or {}).get("tested_merge"),
            "advisory_scope": (plan or {}).get("advisory_scope"), "candidate_tests": (plan or {}).get("candidate_tests", 0),
            "selection_ratio": round((plan or {}).get("candidate_tests", 0) / total, 4) if total else None,
            "meaning": ("candidate tests only; not a safety or completeness claim — FULL CI remains authoritative")}


def fast_summary(r):
    lines = ["", "### RIG FAST FEEDBACK — NON-BLOCKING", "",
             "**NOT A MERGE GATE — FULL CI REMAINS AUTHORITATIVE.**", "",
             "| field | value |", "|---|---|"]
    for k in ("pr_head", "tested_merge", "advisory_scope", "candidate_tests", "selection_ratio", "pytest_outcome", "fast_status"):
        lines.append(f"| {k} | `{r.get(k)}` |")
    if r.get("fast_status") == FAST_FAIL:
        lines += ["", "**FAST_FEEDBACK_FAIL** — failing candidate tests (early feedback only):", ""]
        lines += [f"- `{t}`" for t in r.get("failing_tests", ())]
    return "\n".join(lines) + "\n"


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def _append(path, text):
    if path:
        try:
            with open(path, "a", encoding="utf-8") as fh:
                fh.write(text)
        except OSError:
            pass


def main(argv=None):
    p = argparse.ArgumentParser(description="RIG shadow/fast-feedback telemetry (advisory only; always exits 0).")
    p.add_argument("--mode", choices=("compare", "fast-plan", "fast-report"), default="compare")
    p.add_argument("--rig")
    p.add_argument("--junit")
    p.add_argument("--repo", default=os.getcwd())
    p.add_argument("--summary")
    p.add_argument("--outputs", help="file to append key=value lines to (GITHUB_OUTPUT)")
    p.add_argument("--pr-head")
    p.add_argument("--tested-merge")
    p.add_argument("--base")
    p.add_argument("--plan")
    p.add_argument("--exit-code")
    args = p.parse_args(argv)
    try:
        if args.mode == "compare":
            rig, rig_reason = load_rig(args.rig)
            cases, junit_reason = load_junit(args.junit, args.repo)
            report = compare(rig, rig_reason, cases, junit_reason, args.pr_head, args.tested_merge)
            _append(args.summary, compare_summary(report))
        elif args.mode == "fast-plan":
            report = fast_plan(args.repo, args.base, args.tested_merge, args.pr_head)
            if args.plan:
                with open(args.plan, "w", encoding="utf-8") as fh:
                    json.dump(report, fh, indent=2, sort_keys=True)
            _append(args.outputs, f"run_fast={'true' if report['run_fast'] else 'false'}\n")
            if not report["run_fast"]:
                _append(args.summary, fast_summary(fast_report(report, None, None)))
        else:
            plan = None
            if args.plan and os.path.isfile(args.plan):
                with open(args.plan, encoding="utf-8") as fh:
                    plan = json.load(fh)
            cases, _ = load_junit(args.junit, args.repo)
            code = int(args.exit_code) if args.exit_code not in (None, "") else None
            report = fast_report(plan, code, cases)
            _append(args.summary, fast_summary(report))
    except Exception as exc:                                   # telemetry never breaks a job
        report = {"shadow_version": SHADOW_VERSION, "authority": AUTHORITY, "error": type(exc).__name__,
                  "shadow_status": RIG_UNAVAILABLE, "fast_status": FAST_UNAVAILABLE}
        if args.mode == "fast-plan":
            _append(args.outputs, "run_fast=false\n")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
