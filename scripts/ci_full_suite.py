"""CI FULL-suite sharding pilot — partition, shard evidence and central audit.

Owner of ONE bounded contract: the governed FULL pytest suite split over exactly
three independent runners, proven complete by a fail-closed central audit.

  * ``--mode shard``: verify the tested-merge identity, run the NORMAL full
    pytest collection, keep only the whole test files deterministically assigned
    to this shard (the static ``BROWSER_SHARD`` placement for the current
    real-browser files, else ``1 + int(SHA256(repo-relative POSIX path)[:8], 16) % 3``),
    execute them serially and write JUnit plus a structured evidence JSON.
  * ``--mode audit``: accept the three shard evidence packages only when they
    prove, for the current run / attempt / tested merge / tree, that the three
    assignments exactly partition ONE identical full collection, that every
    assigned node ran exactly once, and that the existing authoritative skip /
    xfail / browser / real-Gunicorn / cleanliness semantics hold.

Pilot status: NON-AUTHORITATIVE. The monolithic ``verify`` job stays the only
input to the protected ``CI required`` check. Nothing here reads repository
intelligence (RIG) output, a changed-file list, ``-k`` or markers: every shard
collects the whole suite and the partition depends on the file path alone.

The pytest plugin half of this module is loaded into the shard's pytest process
with ``-p scripts.ci_full_suite`` and is inert unless ``INVENTORAI_CI_SHARD`` is
set. The module imports only the standard library at import time, so the audit
runs on a bare interpreter.
"""
import argparse
import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from types import MappingProxyType

SHARD_COUNT = 3
SCHEMA = "inventorai-ci-full-suite-shard-v1"
EVIDENCE_FILE = "shard-evidence.json"
JUNIT_FILE = "shard-junit.xml"
_RAW_FILE = "shard-raw.json"
_SHA_RE = re.compile(r"[0-9a-f]{40}")
_RUN_RE = re.compile(r"[1-9][0-9]*")

# ---------------------------------------------------------------------------
# The authoritative mandatory semantics, mirrored from the inline audit in the
# `verify` job of .github/workflows/ci.yml. tests/test_ci_full_suite.py parses
# that inline step and fails if these constants drift from it.
# ---------------------------------------------------------------------------
ALLOWED_SKIPS = {
    ('tests.test_fdc001_contract.TestFDC001_S7_CategoriesBC_Deferred', name): {'ODS-001 exists'}
    for name in ('test_category_b_deferred', 'test_category_c_deferred',
                 'test_category_b_note_references_ods001')
}
ALLOWED_SKIPS[('tests.test_wps001_invariants.TestWPS001_INV004_GapLifecycle',
               'test_closed_gap_does_not_reopen')] = {'No gaps reached CLOSED — cannot test forward-only'}
ALLOWED_SKIPS[('tests.test_w2c_rvr6b_web', 'test_electronics_covered_intent_suppressed')] = {
    'electronics journey did not open MECHANISM first',
    'journey advanced differently — covered elsewhere'}
KNOWN_XFAIL = ('tests.test_f011_progression_quality_gate',
               'test_f011_hall_sensor_alone_does_not_advance_level_0')
KNOWN_XFAIL_REASON = 'ADR-003 Step 6: component label only — no claim/basis/relationship'
MANDATORY_BROWSER_MODULES = ('tests.test_draft_l2_local_continuity', 'tests.test_p5_2_draft_account_switch')
MANDATORY_SERVER_PROOF = ('tests.test_email_h1_access_log_token_redaction',
                          'test_real_gunicorn_access_log_contains_no_raw_token')


# ---------------------------------------------------------------------------
# Partition
# ---------------------------------------------------------------------------
def file_of(nodeid):
    """The repo-relative POSIX test-file path of a pytest node id."""
    return nodeid.split("::", 1)[0]


# Performance-only placement of the current real-browser test files (each drives
# Playwright Chromium itself or through the fixtures of
# tests/test_draft_l2_local_continuity.py), chosen once from the Pilot-01 hosted
# timings so the three shards carry similar wall time. It never decides WHETHER a
# file runs: a file missing from this mapping (a new browser file included) falls
# back to the SHA-256 rule, and completeness is proven by the audit either way.
BROWSER_SHARD = MappingProxyType({
    "tests/test_a1_saved_journey_browser.py": 3,
    "tests/test_cap02_project_compass_browser.py": 3,
    "tests/test_cap04_gap_action_pack_browser.py": 1,
    "tests/test_cap08_assumption_dependency_browser.py": 1,
    "tests/test_cap09_slice3_test_hypothesis_browser.py": 1,
    "tests/test_cap09_slice4_test_variable_browser.py": 3,
    "tests/test_cap10_declared_contradiction_browser.py": 1,
    "tests/test_cap11_evidence_details_browser.py": 1,
    "tests/test_correction_preview_browser.py": 2,
    "tests/test_deliverable_navigation_browser.py": 3,
    "tests/test_draft_l2_local_continuity.py": 3,
    "tests/test_draft_preview_browser.py": 3,
    "tests/test_f09_planning_form_draft_recovery.py": 2,
    "tests/test_p5_2_draft_account_switch.py": 1,
    "tests/test_r05_browser_request_integrity.py": 3,
    "tests/test_safe_question_routing_pf_q2_weak_recovery_browser.py": 3,
    "tests/test_saved_project_filter_browser.py": 2,
    "tests/test_stage22_action_summary_browser.py": 2,
    "tests/test_stage22_decision_trace_browser.py": 2,
    "tests/test_success_criteria_workflow_browser.py": 1,
    "tests/test_uqtr01_core_serving.py": 3,
    "tests/test_uqtr01_mechanical_path_n_owner_friendly.py": 2,
    "tests/test_uqtr01_target_binding_browser.py": 3,
})


def hash_shard(path, count=SHARD_COUNT):
    """The default whole-file shard (1..count) from the SHA-256 of the path alone."""
    return 1 + int(hashlib.sha256(path.encode("utf-8")).hexdigest()[:8], 16) % count


def shard_of(path, count=SHARD_COUNT):
    """The canonical whole-file shard (1..count): BROWSER_SHARD, else hash_shard."""
    if count == SHARD_COUNT and path in BROWSER_SHARD:
        return BROWSER_SHARD[path]
    return hash_shard(path, count)


def collection_digest(nodeids):
    return hashlib.sha256(("\n".join(sorted(nodeids)) + "\n").encode("utf-8")).hexdigest()


def assigned_for(collected, shard, count=SHARD_COUNT):
    return sorted(n for n in collected if shard_of(file_of(n), count) == shard)


# ---------------------------------------------------------------------------
# pytest plugin (shard process only)
# ---------------------------------------------------------------------------
def _skip_reason(report):
    longrepr = report.longrepr
    if isinstance(longrepr, tuple) and len(longrepr) == 3:
        text = str(longrepr[2])
        return text[len("Skipped: "):] if text.startswith("Skipped: ") else text
    return str(longrepr) if longrepr is not None else ""


def _make_plugin(shard, count, raw_path):
    import pytest

    class _ShardPlugin:
        def __init__(self):
            self.t0 = time.monotonic()
            self.collection_seconds = None
            self.collected = []
            self.assigned = []
            self.outcomes = {}
            self.collection_errors = []

        def pytest_collectreport(self, report):
            if report.failed:
                self.collection_errors.append({"nodeid": report.nodeid, "detail": str(report.longrepr)[-2000:]})

        @pytest.hookimpl(trylast=True)
        def pytest_collection_modifyitems(self, session, config, items):
            self.collected = sorted(item.nodeid for item in items)
            keep, drop = [], []
            for item in items:
                (keep if shard_of(file_of(item.nodeid), count) == shard else drop).append(item)
            items[:] = keep
            if drop:
                config.hook.pytest_deselected(items=drop)
            self.assigned = sorted(item.nodeid for item in keep)
            self.collection_seconds = round(time.monotonic() - self.t0, 3)

        def pytest_runtest_logreport(self, report):
            rec = self.outcomes.setdefault(report.nodeid, {"nodeid": report.nodeid, "reports": 0})
            if report.when == "call" or (report.when == "setup" and not report.passed):
                rec["reports"] += 1
                if hasattr(report, "wasxfail"):
                    rec["outcome"] = "xfailed" if report.skipped else ("xpassed" if report.passed else "failed")
                    rec["reason"] = report.wasxfail
                elif report.skipped:
                    rec["outcome"], rec["reason"] = "skipped", _skip_reason(report)
                elif report.failed:
                    rec["outcome"] = "failed" if report.when == "call" else "error"
                else:
                    rec["outcome"] = "passed"
            elif report.when == "teardown" and report.failed:
                rec["outcome"] = "error"

        def pytest_sessionfinish(self, session, exitstatus):
            pathlib.Path(raw_path).write_text(json.dumps({
                "collected": self.collected, "assigned": self.assigned,
                "outcomes": [self.outcomes[k] for k in sorted(self.outcomes)],
                "collection_errors": self.collection_errors,
                "collection_seconds": self.collection_seconds,
                "session_exitstatus": int(exitstatus),
            }, sort_keys=True), encoding="utf-8")

    return _ShardPlugin()


def pytest_configure(config):
    """Register the shard plugin only inside a shard run (inert otherwise)."""
    shard = os.environ.get("INVENTORAI_CI_SHARD")
    if not shard:
        return
    count = int(os.environ["INVENTORAI_CI_SHARD_COUNT"])
    config.pluginmanager.register(
        _make_plugin(int(shard), count, os.environ["INVENTORAI_CI_SHARD_RAW"]), "inventorai-ci-shard")


# ---------------------------------------------------------------------------
# Identity / cleanliness
# ---------------------------------------------------------------------------
def _git(repo, *args):
    return subprocess.check_output(["git", *args], cwd=repo).decode()


def expected_identity(env=os.environ):
    """(run_id, run_attempt, base, head, merge) from the workflow environment;
    ValueError on any missing or malformed value."""
    ident = {"run_id": env.get("GITHUB_RUN_ID", ""), "run_attempt": env.get("GITHUB_RUN_ATTEMPT", ""),
             "expected_base": env.get("EXPECTED_BASE", ""), "expected_head": env.get("EXPECTED_HEAD", ""),
             "tested_merge": env.get("EXPECTED_MERGE", "")}
    for key in ("run_id", "run_attempt"):
        if not _RUN_RE.fullmatch(ident[key]):
            raise ValueError(f"missing or malformed {key}")
    for key in ("expected_base", "expected_head", "tested_merge"):
        if not _SHA_RE.fullmatch(ident[key]):
            raise ValueError(f"missing or malformed {key}")
    return ident


def verified_tree(repo, ident):
    """The checked-out tree after requiring HEAD == tested merge with parents
    exactly [base, head] (the same proof as the authoritative `verify` job)."""
    parents = _git(repo, "rev-list", "--parents", "-n", "1", "HEAD").split()
    if parents != [ident["tested_merge"], ident["expected_base"], ident["expected_head"]]:
        raise ValueError("the checked-out merge must contain the event base and exact PR head")
    return _git(repo, "rev-parse", "HEAD^{tree}").strip()


def repository_clean(repo):
    """The existing tracked / staged / untracked cleanliness check."""
    tracked = subprocess.run(["git", "diff", "--exit-code", "--quiet"], cwd=repo).returncode == 0
    staged = subprocess.run(["git", "diff", "--cached", "--exit-code", "--quiet"], cwd=repo).returncode == 0
    untracked = _git(repo, "ls-files", "--others", "--exclude-standard").strip() == ""
    return tracked and staged and untracked


# ---------------------------------------------------------------------------
# Shard mode
# ---------------------------------------------------------------------------
def run_shard(repo, out_dir, shard, count, ident):
    repo, out_dir = pathlib.Path(repo).resolve(), pathlib.Path(out_dir).resolve()
    if out_dir == repo or repo in out_dir.parents:
        raise ValueError("evidence must be written outside the repository checkout")
    if not 1 <= shard <= count:
        raise ValueError("shard out of range")
    tree = verified_tree(repo, ident)
    out_dir.mkdir(parents=True, exist_ok=True)
    raw, junit = out_dir / _RAW_FILE, out_dir / JUNIT_FILE
    for stale in (raw, junit, out_dir / EVIDENCE_FILE):
        if stale.exists():
            stale.unlink()
    env = dict(os.environ, INVENTORAI_CI_SHARD=str(shard), INVENTORAI_CI_SHARD_COUNT=str(count),
               INVENTORAI_CI_SHARD_RAW=str(raw))
    started = time.monotonic()
    code = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                           "-p", "scripts.ci_full_suite", "--junitxml=" + str(junit)],
                          cwd=repo, env=env).returncode
    pytest_seconds = round(time.monotonic() - started, 3)
    record = json.loads(raw.read_text(encoding="utf-8")) if raw.is_file() else None
    evidence = dict(ident, schema=SCHEMA, shard=shard, shard_count=count, tested_tree=tree,
                    pytest_exit_status=code, repository_clean=repository_clean(repo),
                    junit=JUNIT_FILE, plugin_record_present=record is not None,
                    timing={"pytest_seconds": pytest_seconds,
                            "collection_seconds": (record or {}).get("collection_seconds")})
    record = record or {"collected": [], "assigned": [], "outcomes": [], "collection_errors": []}
    evidence.update(collected=record["collected"], collection_sha256=collection_digest(record["collected"]),
                    assigned=record["assigned"], outcomes=record["outcomes"],
                    collection_errors=record["collection_errors"])
    (out_dir / EVIDENCE_FILE).write_text(json.dumps(evidence, indent=1, sort_keys=True), encoding="utf-8")
    ok = code == 0 and evidence["repository_clean"] and evidence["plugin_record_present"]
    print(f"shard {shard}/{count}: collected {len(evidence['collected'])}, assigned {len(evidence['assigned'])}, "
          f"pytest exit {code}, clean {evidence['repository_clean']}, pytest {pytest_seconds}s")
    return 0 if ok else 1


# ---------------------------------------------------------------------------
# Audit mode
# ---------------------------------------------------------------------------
def junit_cases(path):
    return ET.parse(path).findall(".//testcase")


def junit_problems(cases):
    """The authoritative inline `verify` semantics over JUnit test cases:
    (problems, passed keys)."""
    problems, passed = [], set()
    for case in cases:
        key = (case.get("classname"), case.get("name"))
        skipped = case.find("skipped")
        if skipped is not None:
            reason = skipped.get("message", "")
            expected = (key == KNOWN_XFAIL and skipped.get("type") == "pytest.xfail" and
                        reason == KNOWN_XFAIL_REASON)
            expected = expected or (skipped.get("type") == "pytest.skip" and reason in ALLOWED_SKIPS.get(key, set()))
            if not expected:
                problems.append(f"unexpected skip/xfail: {key}: {reason}")
        elif case.find("failure") is None and case.find("error") is None:
            passed.add(key)
        else:
            problems.append(f"failure/error: {key}")
    return problems, passed


def load_evidence(evidence_dir):
    """Every evidence package (JSON + its JUnit) found under the downloaded
    artifact directory: [(path, evidence, junit_cases_or_None)]."""
    packages = []
    for path in sorted(pathlib.Path(evidence_dir).rglob(EVIDENCE_FILE)):
        evidence = json.loads(path.read_text(encoding="utf-8"))
        junit = path.parent / JUNIT_FILE
        packages.append((path, evidence, junit_cases(junit) if junit.is_file() else None))
    return packages


def audit(packages, expected):
    """Fail-closed completeness + mandatory-semantics audit; returns problems."""
    problems = []
    by_shard = {}
    for path, ev, _cases in packages:
        if ev.get("schema") != SCHEMA:
            problems.append(f"{path}: unknown evidence schema")
        by_shard.setdefault(ev.get("shard"), []).append(ev)
    if sorted(by_shard) != list(range(1, SHARD_COUNT + 1)):
        problems.append(f"shards present {sorted(by_shard, key=str)}; exactly {list(range(1, SHARD_COUNT + 1))} required")
    for shard, evs in sorted(by_shard.items(), key=lambda kv: str(kv[0])):
        if len(evs) != 1:
            problems.append(f"shard {shard}: {len(evs)} evidence packages; exactly one required")
    if problems:
        return problems

    evs = {s: by_shard[s][0] for s in by_shard}
    cases = {ev["shard"]: c for _p, ev, c in packages}
    for s, ev in sorted(evs.items()):
        if ev.get("shard_count") != SHARD_COUNT:
            problems.append(f"shard {s}: shard count {ev.get('shard_count')}; exactly {SHARD_COUNT} required")
        for key in ("run_id", "run_attempt", "expected_base", "expected_head", "tested_merge", "tested_tree"):
            if ev.get(key) != expected[key]:
                problems.append(f"shard {s}: {key} {ev.get(key)!r} does not match the audit run ({expected[key]!r})")
        if ev.get("collection_errors"):
            problems.append(f"shard {s}: collection errors {[e.get('nodeid') for e in ev['collection_errors']]}")
        if ev.get("pytest_exit_status") != 0:
            problems.append(f"shard {s}: pytest exit status {ev.get('pytest_exit_status')}")
        if ev.get("repository_clean") is not True:
            problems.append(f"shard {s}: repository-clean check did not pass")
        if not ev.get("plugin_record_present"):
            problems.append(f"shard {s}: shard plugin record missing")

    collections = {s: ev.get("collected") or [] for s, ev in evs.items()}
    full = collections[1]
    if not full:
        problems.append("empty full collection")
    for s, col in sorted(collections.items()):
        if col != sorted(set(col)):
            problems.append(f"shard {s}: collection manifest is not a sorted set of unique node ids")
        if col != full or evs[s].get("collection_sha256") != collection_digest(full):
            problems.append(f"shard {s}: full-collection manifest differs from shard 1")

    union = set()
    for s, ev in sorted(evs.items()):
        assigned = ev.get("assigned") or []
        if assigned != assigned_for(full, s):
            problems.append(f"shard {s}: assignment differs from the deterministic partition")
        overlap = union & set(assigned)
        if overlap:
            problems.append(f"shard {s}: assignment overlaps another shard ({len(overlap)} nodes)")
        union |= set(assigned)
        outcomes = ev.get("outcomes") or []
        ids = [o.get("nodeid") for o in outcomes]
        if len(ids) != len(set(ids)):
            problems.append(f"shard {s}: duplicate execution outcome")
        missing, extra = set(assigned) - set(ids), set(ids) - set(assigned)
        if missing:
            problems.append(f"shard {s}: {len(missing)} assigned nodes have no result, e.g. {sorted(missing)[:3]}")
        if extra:
            problems.append(f"shard {s}: {len(extra)} unassigned nodes executed, e.g. {sorted(extra)[:3]}")
        for o in outcomes:
            if o.get("reports") != 1:
                problems.append(f"shard {s}: {o.get('nodeid')} has {o.get('reports')} execution outcomes")
            if o.get("outcome") in ("failed", "error", "xpassed", None):
                problems.append(f"shard {s}: {o.get('nodeid')} {o.get('outcome')}")
        junit = cases.get(s)
        if junit is None:
            problems.append(f"shard {s}: JUnit evidence missing")
        elif len(junit) != len(assigned):
            problems.append(f"shard {s}: JUnit has {len(junit)} cases for {len(assigned)} assigned nodes")
    if union != set(full):
        problems.append(f"assignment union differs from the full collection ({len(set(full) - union)} missing)")

    passed = set()
    for s in sorted(cases):
        if cases[s] is not None:
            shard_problems, shard_passed = junit_problems(cases[s])
            problems.extend(f"shard {s}: {p}" for p in shard_problems)
            passed |= shard_passed
    for module in MANDATORY_BROWSER_MODULES:
        if not any(key[0] == module for key in passed):
            problems.append(f"mandatory browser module did not pass: {module}")
    if MANDATORY_SERVER_PROOF not in passed:
        problems.append("real server security proof missing")
    return problems


def _summary(packages, problems):
    lines = ["### Sharded FULL pilot audit (non-authoritative)", "",
             "| shard | collected | assigned | pytest exit | pytest s | collection s |", "|---|---|---|---|---|---|"]
    for _p, ev, _c in sorted(packages, key=lambda p: str(p[1].get("shard"))):
        t = ev.get("timing") or {}
        lines.append(f"| {ev.get('shard')} | {len(ev.get('collected') or [])} | {len(ev.get('assigned') or [])} | "
                     f"{ev.get('pytest_exit_status')} | {t.get('pytest_seconds')} | {t.get('collection_seconds')} |")
    lines += ["", "**PASS**" if not problems else "**FAIL**"] + [f"- {p}" for p in problems[:50]]
    return "\n".join(lines) + "\n"


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--mode", choices=("shard", "audit"), required=True)
    p.add_argument("--shard", type=int)
    p.add_argument("--count", type=int, default=SHARD_COUNT)
    p.add_argument("--out", help="shard mode: evidence directory (outside the checkout)")
    p.add_argument("--evidence-dir", help="audit mode: downloaded evidence directory")
    p.add_argument("--repo", default=".")
    p.add_argument("--summary")
    args = p.parse_args(argv)
    ident = expected_identity()
    if args.mode == "shard":
        if args.count != SHARD_COUNT or args.shard is None or not args.out:
            p.error("shard mode requires --shard, --out and --count 3")
        return run_shard(args.repo, args.out, args.shard, args.count, ident)
    if not args.evidence_dir:
        p.error("audit mode requires --evidence-dir")
    expected = dict(ident, tested_tree=verified_tree(args.repo, ident))
    packages = load_evidence(args.evidence_dir)
    problems = audit(packages, expected)
    if not repository_clean(args.repo):
        problems.append("audit checkout is not clean")
    print(_summary(packages, problems))
    if args.summary:
        with open(args.summary, "a", encoding="utf-8") as fh:
            fh.write(_summary(packages, problems))
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
