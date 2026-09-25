"""Repository Intelligence (RIG) — RIG-2A shadow validation and fast-feedback contract.

File-creation contract:
  Path: tests/test_repository_intelligence_shadow.py
  Purpose: prove that `scripts/repository_intelligence_shadow.py` produces
    honest ADVISORY evidence — shadow comparison of RIG's proposal against the
    authoritative FULL JUnit (failure recall only with failure evidence,
    SHADOW_MISS for omitted or unmappable failures, FULL advisory never
    scored) and the fast-feedback plan/report (only a validated
    AFFECTED-CANDIDATE proposal may run, PASS/FAIL carry no merge claim) —
    and that `.github/workflows/ci.yml` keeps RIG strictly non-authoritative:
    the smoke/full floor and FULL regression are unchanged and never read RIG
    output, RIG analyses EXPECTED_BASE -> EXPECTED_MERGE, candidate tests run
    only in the separate advisory fast job, and `CI required` still depends on
    `verify` alone. Also exercises RIG's self-certification for the shadow files.
  Input contract: synthetic JUnit/RIG files and throwaway git repositories
    under `tmp_path`; the workflow is read as text (no YAML parser).
  Output contract: pass/fail evidence only.
  Prohibited behaviors: no network; no candidate test is executed by this file;
    no mutation of the real repository.
"""
import json
import os
import re
import subprocess

import pytest

from scripts import repository_intelligence as rig
from scripts import repository_intelligence_shadow as shadow

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKFLOW = os.path.join(ROOT, ".github", "workflows", "ci.yml")
SHADOW_SCRIPT = os.path.join(ROOT, "scripts", "repository_intelligence_shadow.py")


# ─────────────────────────────────────────────────────────────────────────────
# helpers
# ─────────────────────────────────────────────────────────────────────────────

@pytest.fixture
def repo(tmp_path):
    for rel in ("tests/test_alpha.py", "tests/test_beta.py", "tests/test_gamma.py", "tests/sub/test_delta.py"):
        full = tmp_path / rel
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_text("def test_x():\n    pass\n", encoding="utf-8")
    return tmp_path


def _junit(path, cases):
    body = []
    for classname, name, outcome in cases:
        inner = {"passed": "", "failure": '<failure message="boom"/>', "error": '<error message="collection failure"/>',
                 "skipped": '<skipped type="pytest.skip" message="s"/>'}[outcome]
        body.append(f'<testcase classname="{classname}" name="{name}">{inner}</testcase>')
    path.write_text('<?xml version="1.0"?><testsuites><testsuite name="pytest">' + "".join(body)
                    + "</testsuite></testsuites>", encoding="utf-8")
    return str(path)


def _rig(path, scope, candidates, evidence=None, **extra):
    report = {"rig": {"contract_version": "rig-contract-1b.0", "tool_version": "rig-1c.1", "authority": "advisory-only"},
              "identity": {"base": "b" * 40, "head": "m" * 40},
              "analysis_health": {"head": {"status": "complete"}},
              "advisory_scope": scope, "candidate_tests": sorted(candidates),
              "evidence_tests": sorted(evidence if evidence is not None else candidates),
              "policy_reasons": extra.get("reasons", []), "uncertainties_in_scope": extra.get("uncertainties", []),
              "scope_widening": {"observer_tests_added": extra.get("observers", 0)}, "central_or_shared": False}
    path.write_text(json.dumps(report), encoding="utf-8")
    return str(path)


def _compare(repo, rig_path, junit_path, capsys, summary=None):
    argv = ["--mode", "compare", "--rig", rig_path, "--junit", junit_path, "--repo", str(repo),
            "--pr-head", "h" * 40, "--tested-merge", "m" * 40]
    if summary:
        argv += ["--summary", summary]
    assert shadow.main(argv) == 0                      # never controls CI status
    return json.loads(capsys.readouterr().out)


GREEN = [("tests.test_alpha", "test_a", "passed"), ("tests.test_beta.TestB", "test_b", "passed"),
         ("tests.test_gamma", "test_g", "passed"), ("tests.sub.test_delta", "test_d", "passed")]


def _git(path, *args):
    return subprocess.run(["git", "-C", str(path), "-c", "user.email=rig@test", "-c", "user.name=rig",
                           "-c", "commit.gpgsign=false", *args], capture_output=True, text=True, check=True).stdout


def _mini_repo(path):
    files = {"engine/__init__.py": "", "engine/iso.py": "def iso():\n    return 1\n",
             "engine/core.py": "def core():\n    return 2\n", "requirements.txt": "flask==3.1.3\n",
             "docs/passive.md": "note\n",
             "tests/test_iso.py": "from engine.iso import iso\n\ndef test_iso():\n    assert iso() == 1\n"}
    for i in range(6):
        files[f"tests/test_core_{i}.py"] = f"from engine.core import core\n\ndef test_c{i}():\n    assert core()\n"
    os.makedirs(path, exist_ok=True)
    _git(path, "init", "-q")
    for rel, text in files.items():
        full = os.path.join(path, rel)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as fh:
            fh.write(text)
    _git(path, "add", "-A")
    _git(path, "commit", "-q", "-m", "base")
    return _git(path, "rev-parse", "HEAD").strip()


def _commit(path, files):
    for rel, text in files.items():
        full = os.path.join(path, rel)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as fh:
            fh.write(text)
    _git(path, "add", "-A")
    _git(path, "commit", "-q", "-m", "change")
    return _git(path, "rev-parse", "HEAD").strip()


def _fast_plan(tmp_path, repo_path, base, merge):
    plan, outputs, summary = tmp_path / "plan.json", tmp_path / "out.txt", tmp_path / "sum.md"
    assert shadow.main(["--mode", "fast-plan", "--repo", str(repo_path), "--base", base, "--tested-merge", merge,
                        "--pr-head", "h" * 40, "--plan", str(plan), "--outputs", str(outputs),
                        "--summary", str(summary)]) == 0
    return (json.loads(plan.read_text()) if plan.exists() else None,
            outputs.read_text() if outputs.exists() else "", summary.read_text() if summary.exists() else "")


# ─────────────────────────────────────────────────────────────────────────────
# shadow comparison (post-FULL)
# ─────────────────────────────────────────────────────────────────────────────

def test_green_full_run_is_never_reported_as_perfect_recall(repo, tmp_path, capsys):
    r = _compare(repo, _rig(tmp_path / "r.json", "AFFECTED-CANDIDATE", ["tests/test_alpha.py"]),
                 _junit(tmp_path / "j.xml", GREEN), capsys)
    assert r["failures_total"] == 0 and r["failure_recall"] is None and r["failure_recall_evidence"] == "NONE"
    assert r["shadow_status"] == "AFFECTED_CANDIDATE_GREEN_FULL"
    assert r["selection_ratio"] == 0.25 and r["full_test_files"] == 4
    assert (r["pr_head"], r["tested_merge"], r["analysis_head"]) == ("h" * 40, "m" * 40, "m" * 40)


def test_smoke_advisory_green_is_no_failure_evidence(repo, tmp_path, capsys):
    r = _compare(repo, _rig(tmp_path / "r.json", "SMOKE", []), _junit(tmp_path / "j.xml", GREEN), capsys)
    assert r["shadow_status"] == "NO_FAILURE_EVIDENCE" and r["failure_recall"] is None


def test_failure_inside_candidates_gives_full_recall(repo, tmp_path, capsys):
    cases = GREEN[:1] + [("tests.test_beta.TestB", "test_b", "failure")] + GREEN[2:]
    r = _compare(repo, _rig(tmp_path / "r.json", "AFFECTED-CANDIDATE", ["tests/test_beta.py"]),
                 _junit(tmp_path / "j.xml", cases), capsys)
    assert (r["failures_total"], r["failures_in_candidate"], r["failures_omitted"]) == (1, 1, 0)
    assert r["failure_recall"] == 1.0 and r["failure_recall_evidence"] == "PRESENT"
    assert r["shadow_status"] == "AFFECTED_CANDIDATE_FAILURES_COVERED"


def test_failure_outside_candidates_is_a_shadow_miss(repo, tmp_path, capsys):
    cases = GREEN[:2] + [("tests.test_gamma", "test_g", "failure")] + GREEN[3:]
    summary = tmp_path / "summary.md"
    r = _compare(repo, _rig(tmp_path / "r.json", "AFFECTED-CANDIDATE", ["tests/test_alpha.py"]),
                 _junit(tmp_path / "j.xml", cases), capsys, summary=str(summary))
    assert r["shadow_status"] == "SHADOW_MISS" and r["failure_recall"] == 0.0
    assert r["omitted_failing_tests"] == ["tests.test_gamma::test_g [tests/test_gamma.py]"]
    text = summary.read_text(encoding="utf-8")
    assert "RIG SHADOW — ADVISORY ONLY" in text and "**SHADOW_MISS**" in text and "tested_merge" in text


def test_partial_coverage_gives_the_exact_fraction(repo, tmp_path, capsys):
    cases = [("tests.test_alpha", "test_a", "failure"), ("tests.test_beta.TestB", "test_b", "failure"),
             ("tests.test_gamma", "test_g", "failure"), ("tests.sub.test_delta", "test_d", "passed")]
    r = _compare(repo, _rig(tmp_path / "r.json", "AFFECTED-CANDIDATE", ["tests/test_alpha.py", "tests/test_beta.py"]),
                 _junit(tmp_path / "j.xml", cases), capsys)
    assert (r["failures_total"], r["failures_in_candidate"], r["failures_omitted"]) == (3, 2, 1)
    assert r["failure_recall"] == round(2 / 3, 4) and r["shadow_status"] == "SHADOW_MISS"


def test_junit_error_and_collection_failure_count_as_failure_evidence(repo, tmp_path, capsys):
    cases = GREEN[:3] + [("", "tests.sub.test_delta", "error")]
    r = _compare(repo, _rig(tmp_path / "r.json", "AFFECTED-CANDIDATE", ["tests/sub/test_delta.py"]),
                 _junit(tmp_path / "j.xml", cases), capsys)
    assert r["failures_total"] == 1 and r["failures_in_candidate"] == 1 and r["failure_recall"] == 1.0


def test_class_based_classnames_map_to_their_module_file(repo):
    assert shadow.map_to_test_file("tests.test_beta.TestB", "test_b", str(repo)) == "tests/test_beta.py"
    assert shadow.map_to_test_file("tests.test_beta.TestB.TestInner", "t", str(repo)) == "tests/test_beta.py"
    assert shadow.map_to_test_file("tests.sub.test_delta", "t", str(repo)) == "tests/sub/test_delta.py"
    assert shadow.map_to_test_file("", "tests.test_alpha", str(repo)) == "tests/test_alpha.py"
    assert shadow.map_to_test_file("somewhere.else", "t", str(repo)) is None


def test_unmappable_failure_is_never_ignored(repo, tmp_path, capsys):
    every = ["tests/test_alpha.py", "tests/test_beta.py", "tests/test_gamma.py", "tests/sub/test_delta.py"]
    r = _compare(repo, _rig(tmp_path / "r.json", "AFFECTED-CANDIDATE", every),
                 _junit(tmp_path / "j.xml", GREEN + [("plugins.external_suite", "test_x", "failure")]), capsys)
    assert r["unmapped_failures"] == ["plugins.external_suite::test_x"] and r["shadow_status"] == "SHADOW_MISS"
    assert r["omitted_failing_tests"] == ["plugins.external_suite::test_x [UNMAPPED FAILURE]"]


@pytest.mark.parametrize("content", [None, "not json", json.dumps({"analysis_status": "unavailable", "advisory_scope": "FULL",
                                                                    "reason": "git failed"})])
def test_rig_unavailable_leaves_full_evidence_standing(repo, tmp_path, capsys, content):
    rig_path = tmp_path / "missing.json"
    if content is not None:
        rig_path.write_text(content, encoding="utf-8")
    cases = GREEN[:1] + [("tests.test_beta.TestB", "test_b", "failure")] + GREEN[2:]
    r = _compare(repo, str(rig_path), _junit(tmp_path / "j.xml", cases), capsys)
    assert r["shadow_status"] == "RIG_UNAVAILABLE" and r["rig_status"] == "unavailable"
    assert r["failures_total"] == 1 and r["failing_tests"] == ["tests.test_beta.TestB::test_b"]
    assert r["failure_recall"] is None


def test_missing_full_evidence_is_reported_not_guessed(repo, tmp_path, capsys):
    r = _compare(repo, _rig(tmp_path / "r.json", "AFFECTED-CANDIDATE", ["tests/test_alpha.py"]), str(tmp_path / "no.xml"), capsys)
    assert r["shadow_status"] == "FULL_EVIDENCE_UNAVAILABLE" and r["full_evidence"] == "unavailable"


def test_advisory_full_makes_no_selection_claim(repo, tmp_path, capsys):
    cases = GREEN[:2] + [("tests.test_gamma", "test_g", "failure")] + GREEN[3:]
    r = _compare(repo, _rig(tmp_path / "r.json", "FULL", ["tests/test_alpha.py"], reasons=["protected:ci-workflow: x"]),
                 _junit(tmp_path / "j.xml", cases), capsys)
    assert r["shadow_status"] == "FULL_ADVISORY" and r["policy_reasons"] == ["protected:ci-workflow: x"]
    assert r["failure_recall"] is None and r["failure_recall_evidence"] == "NOT_APPLICABLE (advisory FULL)"


def test_output_is_deterministic(repo, tmp_path, capsys):
    rig_path = _rig(tmp_path / "r.json", "AFFECTED-CANDIDATE", ["tests/test_beta.py", "tests/test_alpha.py"])
    junit = _junit(tmp_path / "j.xml", [("tests.test_gamma", "z", "failure"), ("tests.test_alpha", "a", "failure")] + GREEN)
    first, second = _compare(repo, rig_path, junit, capsys), _compare(repo, rig_path, junit, capsys)
    assert first == second and first["failing_tests"] == sorted(first["failing_tests"])
    assert first["shadow_status"] in shadow.STATUSES


def test_comparator_never_executes_tests_and_never_edits_evidence(repo, tmp_path, capsys):
    source = open(SHADOW_SCRIPT, encoding="utf-8").read()
    assert not re.search(r"^\s*(import|from)\s+(subprocess|pytest)\b", source, re.M)
    assert "pytest.main" not in source and "os.system" not in source
    junit = _junit(tmp_path / "j.xml", [("tests.test_gamma", "test_g", "failure")] + GREEN)
    before = open(junit, "rb").read()
    assert _compare(repo, _rig(tmp_path / "r.json", "AFFECTED-CANDIDATE", ["tests/test_alpha.py"]), junit,
                    capsys)["shadow_status"] == "SHADOW_MISS"
    assert open(junit, "rb").read() == before
    assert shadow.main(["--rig", "/nonexistent", "--junit", "/nonexistent"]) == 0     # cannot turn red green
    capsys.readouterr()


# ─────────────────────────────────────────────────────────────────────────────
# fast-feedback lane (plan + report)
# ─────────────────────────────────────────────────────────────────────────────

TRACKED = frozenset({"tests/test_alpha.py", "tests/test_beta.py", "engine/x.py"})


@pytest.mark.parametrize("candidates, reason_part", [
    ([], "missing or empty"),
    (["../tests/test_alpha.py"], "not a repository test file"),
    (["/tests/test_alpha.py"], "invalid candidate entry"),
    (["-k", "tests/test_alpha.py"], "invalid candidate entry"),
    (["engine/x.py"], "not a repository test file"),
    (["tests/./test_alpha.py"], "not a repository test file"),
    (["tests/test_missing.py"], "not tracked at the tested merge"),
    ([7], "invalid candidate entry"),
])
def test_invalid_candidates_never_reach_pytest(candidates, reason_part):
    status, cands, reason = shadow.plan_fast({"advisory_scope": "AFFECTED-CANDIDATE", "candidate_tests": candidates}, TRACKED)
    assert status == shadow.FAST_UNAVAILABLE and cands == [] and reason_part in reason


@pytest.mark.parametrize("scope", ["FULL", "SMOKE"])
def test_full_and_smoke_advisories_run_no_subset(scope):
    status, cands, _ = shadow.plan_fast({"advisory_scope": scope, "candidate_tests": ["tests/test_alpha.py"]}, TRACKED)
    assert status == shadow.FAST_NOT_APPLICABLE and cands == []


def test_unavailable_rig_runs_no_subset():
    for report in (None, {"analysis_status": "unavailable", "advisory_scope": "FULL"}, {"no": "scope"}):
        status, cands, _ = shadow.plan_fast(report, TRACKED)
        assert status == shadow.FAST_UNAVAILABLE and cands == []


def test_valid_affected_candidate_is_planned_not_passed():
    status, cands, _ = shadow.plan_fast({"advisory_scope": "AFFECTED-CANDIDATE",
                                         "candidate_tests": ["tests/test_beta.py", "tests/test_alpha.py"]}, TRACKED)
    assert status == shadow.FAST_PLANNED and status not in shadow.FAST_STATUSES
    assert cands == ["tests/test_alpha.py", "tests/test_beta.py"]


def test_fast_plan_on_a_real_git_history(tmp_path):
    path = tmp_path / "mini"
    base = _mini_repo(str(path))
    iso = _commit(str(path), {"engine/iso.py": "def iso():\n    return 1  # changed\n"})
    plan, outputs, _ = _fast_plan(tmp_path, path, base, iso)
    assert "run_fast=true" in outputs and plan["fast_status"] == shadow.FAST_PLANNED
    assert "tests/test_iso.py" in plan["candidates"] and plan["analysis_head"] == iso == plan["tested_merge"]
    full = _commit(str(path), {"requirements.txt": "flask==3.1.4\n"})
    plan, outputs, summary = _fast_plan(tmp_path, path, iso, full)
    assert "run_fast=false" in outputs and plan["fast_status"] == shadow.FAST_NOT_APPLICABLE and plan["candidates"] == []
    assert "NOT A MERGE GATE" in summary
    smoke = _commit(str(path), {"docs/passive.md": "changed\n"})
    plan, outputs, _ = _fast_plan(tmp_path, path, full, smoke)
    assert "run_fast=false" in outputs and plan["advisory_scope"] == "SMOKE"
    plan, outputs, _ = _fast_plan(tmp_path, path, "0" * 40, smoke)
    assert "run_fast=false" in outputs and plan["fast_status"] == shadow.FAST_UNAVAILABLE


def test_fast_report_pass_and_fail_carry_no_merge_claim(repo, tmp_path, capsys):
    plan = {"run_fast": True, "fast_status": shadow.FAST_PLANNED, "pr_head": "h" * 40, "tested_merge": "m" * 40,
            "advisory_scope": "AFFECTED-CANDIDATE", "candidate_tests": 2, "total_tests": 8}
    plan_path = tmp_path / "plan.json"
    plan_path.write_text(json.dumps(plan))
    for code, cases, expected in ((0, GREEN, shadow.FAST_PASS),
                                  (1, GREEN[:1] + [("tests.test_beta.TestB", "test_b", "failure")], shadow.FAST_FAIL)):
        summary = tmp_path / f"s{code}.md"
        assert shadow.main(["--mode", "fast-report", "--plan", str(plan_path), "--junit", _junit(tmp_path / f"f{code}.xml", cases),
                            "--repo", str(repo), "--exit-code", str(code), "--summary", str(summary)]) == 0
        out = json.loads(capsys.readouterr().out)
        assert out["fast_status"] == expected and out["selection_ratio"] == 0.25
        text = summary.read_text()
        assert "NOT A MERGE GATE — FULL CI REMAINS AUTHORITATIVE" in text
        assert "not a safety or completeness claim" in out["meaning"]
    assert out["failing_tests"] == ["tests.test_beta.TestB::test_b"] and "**FAST_FEEDBACK_FAIL**" in text


# ─────────────────────────────────────────────────────────────────────────────
# RIG self-certification for the shadow files (actual policy)
# ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("path", ["scripts/repository_intelligence_shadow.py", "tests/test_repository_intelligence_shadow.py",
                                  ".github/workflows/ci.yml"])
def test_shadow_files_and_workflow_are_protected_full(tmp_path, path):
    repo_path = tmp_path / "mini"
    base = _mini_repo(str(repo_path))
    head = _commit(str(repo_path), {path: "# changed\n"})
    report = rig.analyse(str(repo_path), base, head)
    assert report["advisory_scope"] == "FULL"
    expected = "ci-workflow" if path.startswith(".github/") else "rig-self-certification"
    assert f"protected:{expected}: {path}" in report["policy_reasons"]


# ─────────────────────────────────────────────────────────────────────────────
# workflow contract (text assertions, no YAML parser)
# ─────────────────────────────────────────────────────────────────────────────

def _workflow():
    with open(WORKFLOW, encoding="utf-8") as fh:
        return fh.read()


def _jobs(text):
    body = text[text.index("\njobs:\n") + 7:]
    starts = [(m.group(1), m.start()) for m in re.finditer(r"^  ([a-z_]+):\n", body, re.M)]
    return {name: body[pos:(starts[i + 1][1] if i + 1 < len(starts) else len(body))] for i, (name, pos) in enumerate(starts)}


def _step(job, name):
    start = job.index(f"      - name: {name}")
    nxt = job.find("\n      - name: ", start + 1)
    return job[start:] if nxt == -1 else job[start:nxt]


def test_smoke_full_floor_authority_is_unchanged():
    verify = _jobs(_workflow())["verify"]
    assert "scope = 'smoke' if all(map(documentation_only, paths)) else 'full'" in verify
    assert "output.write('scope=' + scope + '\\n')" in verify
    assert "rig" not in _step(verify, "Verify identity and select the minimum test scope").lower()


def test_full_regression_runs_only_on_the_existing_floor_and_never_reads_rig():
    block = _step(_jobs(_workflow())["verify"], "Full regression and mandatory-check audit")
    assert re.findall(r"^\s+if: (.+)$", block, re.M) == ["steps.scope.outputs.scope == 'full'"]
    for word in ("rig", "candidate", "shadow", "fast"):
        assert word not in block.lower(), word
    assert "result = subprocess.run([sys.executable, '-m', 'pytest', '-q', '-p', 'no:cacheprovider'," in block
    assert "'--junitxml=' + str(report)])" in block
    assert "assert result.returncode == 0, f'pytest failed: exit {result.returncode}'" in block


def test_rig_analyses_the_tested_merge_and_head_is_identity_only():
    text = _workflow()
    assert "merge-base" not in text
    assert '--head "$EXPECTED_HEAD"' not in text and "--head $EXPECTED_HEAD" not in text
    plan = _step(_jobs(text)["verify"], "RIG shadow plan (advisory only; selects nothing)")
    assert '--base "$EXPECTED_BASE" --head "$EXPECTED_MERGE"' in plan
    fast = _step(_jobs(text)["fast"], "RIG fast plan (advisory; decides only whether this lane runs)")
    assert '--base "$EXPECTED_BASE" --tested-merge "$EXPECTED_MERGE" --pr-head "$EXPECTED_HEAD"' in fast
    for line in text.splitlines():                                # EXPECTED_HEAD: identity / reporting only
        if "$EXPECTED_HEAD" in line:
            assert "--pr-head" in line or "PR head" in line, line


def test_shadow_steps_are_advisory_fail_open_and_ordered():
    verify = _jobs(_workflow())["verify"]
    plan = _step(verify, "RIG shadow plan (advisory only; selects nothing)")
    comp = _step(verify, "RIG shadow comparison (advisory only; never affects CI status)")
    assert "continue-on-error: true" in plan and "continue-on-error: true" in comp
    assert "if: steps.scope.outputs.scope == 'full'" in plan
    assert "if: always() && steps.scope.outputs.scope == 'full'" in comp
    assert '"$RUNNER_TEMP/rig-shadow.json"' in plan and "FULL regression still runs" in plan
    assert verify.index("RIG shadow plan") < verify.index("- name: Full regression and mandatory-check audit") \
        < verify.index("RIG shadow comparison") < verify.index("- name: Confirm repository data was not changed")
    for block in (plan, comp):
        assert "id:" not in block and "pytest" not in block.replace("inventorai-pytest.xml", "")


def test_candidate_tests_run_only_in_the_advisory_fast_job():
    jobs = _jobs(_workflow())
    assert "candidates" not in jobs["verify"] and "rig-fast" not in jobs["verify"]
    assert jobs["verify"].count("'-m', 'pytest'") == 1                 # the unchanged FULL run only
    assert "candidates" not in jobs["required"]
    run = _step(jobs["fast"], "Run RIG candidate tests early (advisory; NOT A MERGE GATE)")
    assert "if: steps.fastplan.outputs.run_fast == 'true'" in run
    assert "argv = [sys.executable, '-m', 'pytest'" in run and "'--', *candidates]" in run
    assert "shell=True" not in run and "sys.exit(code)" not in run    # a failure never fails the lane
    for name in ("Install the governed test environment (fast lane)",
                 "Install the matching Chromium and Linux prerequisites (fast lane)"):
        assert "if: steps.fastplan.outputs.run_fast == 'true'" in _step(jobs["fast"], name)
    assert "-r requirements.txt -r tests/requirements-draft-l2.txt" in jobs["fast"]
    assert "INVENTORAI_DRAFT_L2_REQUIRE_BROWSER: '1'" in jobs["fast"]


def test_fast_job_is_parallel_non_required_and_cannot_control_verify():
    jobs = _jobs(_workflow())
    assert set(jobs) == {"verify", "fast", "required"}
    assert "needs:" not in jobs["verify"] and "needs:" not in jobs["fast"]
    assert "continue-on-error: true" in jobs["fast"].split("steps:")[0]
    assert "fast" not in jobs["verify"].lower().replace("fail-open", "")
    required = jobs["required"]
    assert re.findall(r"needs: \[(.*)\]", required) == ["verify"]
    assert 'test "$VERIFY_RESULT" = success' in required and "fast" not in required.lower()


def test_unavailable_rig_cannot_prevent_the_full_regression():
    verify = _jobs(_workflow())["verify"]
    plan = _step(verify, "RIG shadow plan (advisory only; selects nothing)")
    assert "|| echo" in plan and "continue-on-error: true" in plan
    assert "steps.rig" not in _workflow() and "outputs.run_fast" not in verify
