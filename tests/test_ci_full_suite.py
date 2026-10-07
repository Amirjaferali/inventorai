"""Sharded FULL-suite authority — scripts/ci_full_suite.py and the CI workflow.

Pins the adopted contract (Pilot-02 partition, evidence and audit, now authoritative):
  * the deterministic whole-file partition over exactly three shards: the static
    performance-only BROWSER_SHARD placement, else the SHA-256 rule;
  * the shard plugin: normal full collection, deselection of other shards'
    files only, per-node outcomes, collection errors, exit status;
  * the fail-closed central audit, including every adversarial case the pilot
    must reject;
  * the audit's mandatory skip / xfail / browser / real-Gunicorn constants,
    pinned independently on their one permanent owner (no inline workflow copy);
  * the workflow topology: an always-running `scope` job with the unchanged
    six-path SMOKE exemption and fail-closed FULL fallback; SMOKE decided by
    `verify`; FULL decided by the three-shard matrix plus the fail-closed audit,
    which runs inside the protected `CI required` job (no separate audit job);
    the scope-aware `CI required` verdict over the job results and the audit /
    cleanliness step outcomes (executed over its whole truth table, never
    accepting a generic skip); RIG and the advisory `fast` lane outside the
    required dependency chain; no monolithic FULL job; and every external action
    pinned to a full SHA.

Synthetic data only; temporary directories only; the real repository is read,
never modified.
"""
import ast
import concurrent.futures
import copy
import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys
import textwrap
import xml.etree.ElementTree as ET

import pytest

from scripts import ci_full_suite as cfs

ROOT = pathlib.Path(__file__).resolve().parent.parent
WORKFLOW = ROOT / ".github" / "workflows" / "ci.yml"

BASE, HEAD, MERGE, TREE = "a" * 40, "b" * 40, "c" * 40, "d" * 40
EXPECTED = {"run_id": "1001", "run_attempt": "2", "expected_base": BASE, "expected_head": HEAD,
            "tested_merge": MERGE, "tested_tree": TREE}


# ==========================================================================
# partition
# ==========================================================================
@pytest.mark.parametrize("path, prefix, shard", [
    ("tests/test_draft_l2_local_continuity.py", "6f282c7c", 2),
    ("tests/test_p5_2_draft_account_switch.py", "67b345c2", 3),
    ("tests/test_email_h1_access_log_token_redaction.py", "94a42cf2", 2),
    ("tests/test_delta.py", "88c1a4e0", 1),
])
def test_known_sha256_vectors(path, prefix, shard):
    assert hashlib.sha256(path.encode("utf-8")).hexdigest()[:8] == prefix
    assert cfs.hash_shard(path) == shard == 1 + int(prefix, 16) % 3
    assert cfs.shard_of(path) == cfs.BROWSER_SHARD.get(path, shard)


def test_partition_is_deterministic_across_interpreters_and_hash_seeds():
    paths = sorted(str(p.relative_to(ROOT).as_posix()) for p in (ROOT / "tests").glob("test_*.py"))
    here = [cfs.shard_of(p) for p in paths]
    code = ("import json, sys; sys.path.insert(0, %r); from scripts import ci_full_suite as c; "
            "print(json.dumps([c.shard_of(p) for p in json.load(sys.stdin)]))" % str(ROOT))
    for seed in ("0", "1", "12345"):
        out = subprocess.run([sys.executable, "-c", code], input=json.dumps(paths), capture_output=True,
                             text=True, env=dict(os.environ, PYTHONHASHSEED=seed), check=True).stdout
        assert json.loads(out) == here
    assert set(here) == {1, 2, 3}
    assert set(cfs.BROWSER_SHARD) <= set(paths)


def test_shard_range_is_one_to_three():
    for i in range(2000):
        assert 1 <= cfs.shard_of(f"tests/test_{i}.py") <= 3
    assert set(cfs.BROWSER_SHARD.values()) == {1, 2, 3}
    assert all(type(v) is int for v in cfs.BROWSER_SHARD.values())


def _browser_shard_literal():
    tree = ast.parse((ROOT / "scripts" / "ci_full_suite.py").read_text(encoding="utf-8"))
    (node,) = [n for n in tree.body if isinstance(n, ast.Assign)
               and [t.id for t in n.targets if isinstance(t, ast.Name)] == ["BROWSER_SHARD"]]
    return node.value


def test_browser_override_is_one_immutable_static_literal_without_duplicates():
    call = _browser_shard_literal()
    assert isinstance(call, ast.Call) and call.func.id == "MappingProxyType" and len(call.args) == 1
    literal = call.args[0]
    assert isinstance(literal, ast.Dict)
    assert all(isinstance(k, ast.Constant) and isinstance(v, ast.Constant)
               for k, v in zip(literal.keys, literal.values))              # no runtime / timing input
    keys = [k.value for k in literal.keys]
    assert len(keys) == len(set(keys)) == len(cfs.BROWSER_SHARD)           # no path listed twice
    assert keys == sorted(keys)
    with pytest.raises(TypeError):
        cfs.BROWSER_SHARD["tests/test_alpha.py"] = 1


def test_browser_override_lists_only_current_real_browser_files():
    for path in cfs.BROWSER_SHARD:
        assert re.fullmatch(r"tests/test_[a-z0-9_]+\.py", path), path
        source = (ROOT / path).read_text(encoding="utf-8")
        assert ("playwright" in source                                      # drives Chromium itself
                or "from tests.test_draft_l2_local_continuity import" in source), path   # or its fixture


@pytest.mark.parametrize("path", sorted(cfs.BROWSER_SHARD))
def test_browser_override_files_map_to_their_intended_shard(path):
    assert cfs.shard_of(path) == cfs.BROWSER_SHARD[path]
    assert cfs.shard_of(path) == cfs.shard_of(path)


def test_every_other_file_keeps_the_sha256_rule():
    paths = sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / "tests").glob("test_*.py"))
    others = [p for p in paths if p not in cfs.BROWSER_SHARD]
    assert len(others) == len(paths) - len(cfs.BROWSER_SHARD) > 0
    for p in others + [f"tests/test_{i}.py" for i in range(500)]:
        assert cfs.shard_of(p) == cfs.hash_shard(p) == 1 + int(hashlib.sha256(p.encode()).hexdigest()[:8], 16) % 3


def test_a_new_or_unlisted_browser_file_falls_back_to_hashing():
    for path in ("tests/test_brand_new_feature_browser.py", "tests/test_cap99_future_browser.py",
                 "tests/../tests/test_draft_preview_browser.py", "tests/test_draft_preview_browser.py ",
                 "Tests/test_draft_preview_browser.py"):
        assert path not in cfs.BROWSER_SHARD
        assert cfs.shard_of(path) == cfs.hash_shard(path)


def test_browser_override_applies_only_to_the_three_shard_pilot():
    for path in cfs.BROWSER_SHARD:
        for count in (1, 2, 4, 5):
            assert cfs.shard_of(path, count) == cfs.hash_shard(path, count)


def test_override_placement_keeps_whole_files_and_the_assignment_complete_and_disjoint():
    paths = sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / "tests").glob("test_*.py"))
    nodes = [f"{p}::{n}" for p in paths
             for n in ("test_a", "TestX::test_b[1]", "TestX::test_b[two words-2]", "test_c[a::b]")]
    shards = {s: cfs.assigned_for(nodes, s) for s in (1, 2, 3)}
    assert sorted(sum(shards.values(), [])) == sorted(nodes)                # complete
    for a, b in ((1, 2), (1, 3), (2, 3)):
        assert not set(shards[a]) & set(shards[b])                           # disjoint
    for s, assigned in shards.items():
        assert {cfs.shard_of(cfs.file_of(n)) for n in assigned} == {s}       # whole files only
    for path, s in cfs.BROWSER_SHARD.items():
        assert {n for n in nodes if cfs.file_of(n) == path} <= set(shards[s])


def test_whole_file_placement_keeps_classes_and_parameterizations_together():
    nodes = ["tests/test_gamma.py::test_a", "tests/test_gamma.py::TestX::test_b[1]",
             "tests/test_gamma.py::TestX::test_b[two words-2]", "tests/test_delta.py::test_c[x]",
             "tests/test_delta.py::TestY::test_d", "tests/test_alpha.py::test_e"]
    shards = {s: cfs.assigned_for(nodes, s) for s in (1, 2, 3)}
    assert sorted(sum(shards.values(), [])) == sorted(nodes)
    for s, assigned in shards.items():
        assert {cfs.shard_of(cfs.file_of(n)) for n in assigned} <= {s}
    assert shards[2] == sorted(n for n in nodes if n.startswith("tests/test_gamma.py"))
    assert cfs.file_of("tests/test_gamma.py::TestX::test_b[a::b]") == "tests/test_gamma.py"


def test_builtin_hash_is_never_used():
    tree = ast.parse((ROOT / "scripts" / "ci_full_suite.py").read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            assert node.func.id != "hash"
        for word in ("random", "rig", "repository_intelligence"):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                names = [a.name for a in node.names] + [getattr(node, "module", "") or ""]
                assert not any(word in n for n in names), names


# ==========================================================================
# shard plugin (real pytest subprocess on a synthetic project)
# ==========================================================================
_PROJECT = {
    "pytest.ini": "[pytest]\ntestpaths = tests\nxfail_strict = true\n",
    "tests/test_gamma.py": textwrap.dedent("""\
        import pytest

        @pytest.mark.parametrize("v", [1, 2, 3])
        def test_param(v):
            assert v

        class TestK:
            def test_one(self):
                pass
    """),
    "tests/test_delta.py": textwrap.dedent("""\
        import pytest

        def test_ok():
            pass

        def test_skip():
            pytest.skip("synthetic reason")

        @pytest.mark.xfail(reason="synthetic xfail")
        def test_xf():
            assert False
    """),
    "tests/test_alpha.py": "def test_alpha():\n    pass\n",
}


def _project(root, files=_PROJECT):
    for rel, text in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return root


def _shard_run(project, shard, raw):
    env = dict(os.environ, INVENTORAI_CI_SHARD=str(shard), INVENTORAI_CI_SHARD_COUNT="3",
               INVENTORAI_CI_SHARD_RAW=str(raw), PYTHONPATH=str(ROOT), PYTHONDONTWRITEBYTECODE="1")
    proc = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                           "-p", "scripts.ci_full_suite", "--junitxml=" + str(raw.with_suffix(".xml"))],
                          cwd=project, env=env, capture_output=True, text=True)
    return proc.returncode, json.loads(raw.read_text(encoding="utf-8"))


def test_each_shard_collects_everything_and_runs_only_its_own_files(tmp_path):
    project = _project(tmp_path / "p")
    records = {s: _shard_run(project, s, tmp_path / f"raw{s}.json") for s in (1, 2, 3)}
    full = records[1][1]["collected"]
    assert len(full) == 8
    union = set()
    for s, (code, rec) in records.items():
        assert code == 0 and rec["session_exitstatus"] == 0
        assert rec["collected"] == full                                # normal FULL collection everywhere
        assert rec["assigned"] == cfs.assigned_for(full, s)
        assert [o["nodeid"] for o in rec["outcomes"]] == rec["assigned"]  # only assigned nodes executed
        assert all(o["reports"] == 1 for o in rec["outcomes"])
        cases = cfs.junit_cases(tmp_path / f"raw{s}.xml")
        assert len(cases) == len(rec["assigned"])
        union |= set(rec["assigned"])
    assert union == set(full)
    delta = {o["nodeid"].split("::")[-1]: o for o in records[1][1]["outcomes"]}
    assert delta["test_ok"]["outcome"] == "passed"
    assert (delta["test_skip"]["outcome"], delta["test_skip"]["reason"]) == ("skipped", "synthetic reason")
    assert (delta["test_xf"]["outcome"], delta["test_xf"]["reason"]) == ("xfailed", "synthetic xfail")
    assert len(records[2][1]["assigned"]) == 4 and len(records[3][1]["assigned"]) == 1


def test_plugin_is_inert_without_the_shard_environment(tmp_path):
    project = _project(tmp_path / "p")
    env = {k: v for k, v in os.environ.items() if not k.startswith("INVENTORAI_CI_SHARD")}
    proc = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                           "-p", "scripts.ci_full_suite"], cwd=project, capture_output=True, text=True,
                          env=dict(env, PYTHONPATH=str(ROOT), PYTHONDONTWRITEBYTECODE="1"))
    assert proc.returncode == 0 and "6 passed, 1 skipped, 1 xfailed" in proc.stdout
    assert "deselected" not in proc.stdout


def test_failure_exit_status_and_outcome_are_preserved(tmp_path):
    files = dict(_PROJECT, **{"tests/test_gamma.py": "def test_bad():\n    assert False\n"})
    code, rec = _shard_run(_project(tmp_path / "p", files), 2, tmp_path / "raw.json")
    assert code == 1 and rec["session_exitstatus"] == 1
    assert [o["outcome"] for o in rec["outcomes"]] == ["failed"]


def test_collection_failure_is_surfaced(tmp_path):
    files = dict(_PROJECT, **{"tests/test_delta.py": "def broken(:\n"})
    code, rec = _shard_run(_project(tmp_path / "p", files), 2, tmp_path / "raw.json")
    assert code != 0
    assert [e["nodeid"] for e in rec["collection_errors"]] == ["tests/test_delta.py"]


def _git(repo, *args):
    subprocess.run(["git", "-c", "commit.gpgsign=false", *args], cwd=repo, check=True, capture_output=True,
                   env=dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@e", GIT_COMMITTER_NAME="t",
                            GIT_COMMITTER_EMAIL="t@e"))
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo).decode().strip() \
        if args[0] in ("commit", "merge") else None


def _merge_repo(root):
    repo = _project(root, dict(_PROJECT, **{".gitignore": "__pycache__/\n"}))
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "add", "-A")
    base = _git(repo, "commit", "-q", "-m", "base")
    _git(repo, "checkout", "-q", "-b", "pr")
    (repo / "tests" / "test_alpha.py").write_text("def test_alpha():\n    assert 1\n", encoding="utf-8")
    _git(repo, "commit", "-q", "-am", "head")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo).decode().strip()
    _git(repo, "checkout", "-q", "main")
    merge = _git(repo, "merge", "-q", "--no-ff", "-m", "merge", "pr")
    return repo, {"run_id": "7", "run_attempt": "1", "expected_base": base, "expected_head": head,
                  "tested_merge": merge}


def test_run_shard_writes_complete_evidence_and_the_audit_accepts_it(tmp_path, monkeypatch):
    repo, ident = _merge_repo(tmp_path / "repo")
    monkeypatch.setenv("PYTHONPATH", str(ROOT))
    monkeypatch.setenv("PYTHONDONTWRITEBYTECODE", "1")
    for s in (1, 2, 3):
        assert cfs.run_shard(repo, tmp_path / "ev" / f"a{s}", s, 3, ident) == 0
    packages = cfs.load_evidence(tmp_path / "ev")
    ev = packages[0][1]
    for key in ("run_id", "run_attempt", "shard", "shard_count", "expected_base", "expected_head", "tested_merge",
                "tested_tree", "collected", "collection_sha256", "assigned", "outcomes", "collection_errors",
                "pytest_exit_status", "repository_clean"):
        assert key in ev, key
    tree = subprocess.check_output(["git", "rev-parse", "HEAD^{tree}"], cwd=repo).decode().strip()
    problems = cfs.audit(packages, dict(ident, tested_tree=tree))
    # complete and consistent: the only findings are the synthetic project's own (correctly
    # unpermitted) skip / xfail and the absent real-repository mandatory proofs
    assert sorted(problems) == sorted(
        ["shard 1: unexpected skip/xfail: ('tests.test_delta', 'test_skip'): synthetic reason",
         "shard 1: unexpected skip/xfail: ('tests.test_delta', 'test_xf'): synthetic xfail"]
        + [f"mandatory browser module did not pass: {m}" for m in cfs.MANDATORY_BROWSER_MODULES]
        + ["real server security proof missing"])
    assert cfs.repository_clean(repo)


def test_run_shard_refuses_a_wrong_identity_or_evidence_inside_the_checkout(tmp_path):
    repo, ident = _merge_repo(tmp_path / "repo")
    with pytest.raises(ValueError, match="exact PR head"):
        cfs.run_shard(repo, tmp_path / "ev", 1, 3, dict(ident, expected_head="e" * 40))
    with pytest.raises(ValueError, match="outside the repository"):
        cfs.run_shard(repo, repo / "ev", 1, 3, ident)


@pytest.mark.parametrize("env", [
    {}, {"GITHUB_RUN_ID": "x"},
    {"GITHUB_RUN_ID": "1", "GITHUB_RUN_ATTEMPT": "1", "EXPECTED_BASE": "a" * 40, "EXPECTED_HEAD": "b" * 40,
     "EXPECTED_MERGE": "short"},
])
def test_missing_or_malformed_environment_inputs_are_rejected(env):
    with pytest.raises(ValueError):
        cfs.expected_identity(env)


# ==========================================================================
# audit (synthetic evidence)
# ==========================================================================
_MANDATORY_NODES = {
    "tests/test_draft_l2_local_continuity.py::test_browser_draft": "pass",
    "tests/test_p5_2_draft_account_switch.py::test_switch": "pass",
    "tests/test_email_h1_access_log_token_redaction.py::test_real_gunicorn_access_log_contains_no_raw_token": "pass",
    "tests/test_f011_progression_quality_gate.py::test_f011_hall_sensor_alone_does_not_advance_level_0": "xfail",
    "tests/test_wps001_invariants.py::TestWPS001_INV004_GapLifecycle::test_closed_gap_does_not_reopen": "skip",
}
_PLAIN = [f"tests/test_{n}.py::test_{i}" for n in ("alpha", "beta", "gamma", "delta") for i in range(2)]


def _junit_case(nodeid, kind):
    parts = nodeid.split("::")
    classname = ".".join([parts[0][:-3].replace("/", ".")] + parts[1:-1])
    case = ET.Element("testcase", classname=classname, name=parts[-1])
    if kind == "xfail":
        ET.SubElement(case, "skipped", type="pytest.xfail", message=cfs.KNOWN_XFAIL_REASON)
    elif kind == "skip":
        ET.SubElement(case, "skipped", type="pytest.skip", message="No gaps reached CLOSED — cannot test forward-only")
    elif kind in ("failure", "error"):
        ET.SubElement(case, kind, message="x")
    elif kind.startswith("skip:") or kind.startswith("xfail:"):
        typ, reason = kind.split(":", 1)
        ET.SubElement(case, "skipped", type="pytest." + typ, message=reason)
    return case


def _packages(omit=()):
    kinds = dict(_MANDATORY_NODES, **{n: "pass" for n in _PLAIN})
    for n in omit:
        kinds.pop(n)
    full = sorted(kinds)
    packages = []
    for s in (1, 2, 3):
        assigned = cfs.assigned_for(full, s)
        outcome = {"pass": "passed", "xfail": "xfailed", "skip": "skipped"}
        ev = dict(EXPECTED, schema=cfs.SCHEMA, shard=s, shard_count=3, collected=list(full),
                  collection_sha256=cfs.collection_digest(full), assigned=assigned,
                  outcomes=[{"nodeid": n, "outcome": outcome[kinds[n]], "reports": 1} for n in assigned],
                  collection_errors=[], pytest_exit_status=0, repository_clean=True, plugin_record_present=True)
        packages.append((pathlib.Path(f"shard{s}") / cfs.EVIDENCE_FILE, ev,
                         [_junit_case(n, kinds[n]) for n in assigned]))
    assert all(p[1]["assigned"] for p in packages)                     # every shard is non-empty
    return packages


def _shard(packages, s):
    return next(p for p in packages if p[1]["shard"] == s)


def _audit(packages):
    return "\n".join(cfs.audit(packages, EXPECTED))


def test_complete_valid_evidence_passes():
    assert cfs.audit(_packages(), EXPECTED) == []


def test_missing_shard_is_rejected():
    assert "exactly [1, 2, 3] required" in _audit([p for p in _packages() if p[1]["shard"] != 3])


def test_no_evidence_at_all_is_rejected(tmp_path):
    assert "exactly [1, 2, 3] required" in "\n".join(cfs.audit(cfs.load_evidence(tmp_path), EXPECTED))


def test_duplicate_shard_is_rejected():
    packages = _packages()
    packages.append(copy.deepcopy(_shard(packages, 2)))
    assert "shard 2: 2 evidence packages" in _audit(packages)


def test_wrong_shard_count_is_rejected():
    packages = _packages()
    _shard(packages, 1)[1]["shard_count"] = 4
    assert "shard count 4" in _audit(packages)


def test_collection_manifest_mismatch_is_rejected():
    packages = _packages()
    _shard(packages, 2)[1]["collected"] = _shard(packages, 2)[1]["collected"][1:]
    assert "shard 2: full-collection manifest differs" in _audit(packages)


def _move(packages, node, src, dst):
    for s, add in ((src, False), (dst, True)):
        _p, ev, cases = _shard(packages, s)
        if add:
            ev["assigned"] = sorted(ev["assigned"] + [node])
            ev["outcomes"].append({"nodeid": node, "outcome": "passed", "reports": 1})
            cases.append(_junit_case(node, "pass"))
        else:
            ev["assigned"].remove(node)
            ev["outcomes"] = [o for o in ev["outcomes"] if o["nodeid"] != node]
            cases[:] = [c for c in cases if cfs.file_of(node).replace("/", ".")[:-3] != c.get("classname")
                        or c.get("name") != node.split("::")[-1]]


def test_assignment_under_the_pilot_01_hash_only_rule_is_rejected():
    packages = _packages()
    node = "tests/test_draft_l2_local_continuity.py::test_browser_draft"
    canonical, hashed = cfs.shard_of(cfs.file_of(node)), cfs.hash_shard(cfs.file_of(node))
    assert canonical != hashed and node in _shard(packages, canonical)[1]["assigned"]
    _move(packages, node, canonical, hashed)
    text = _audit(packages)
    assert f"shard {canonical}: assignment differs" in text and f"shard {hashed}: assignment differs" in text


def test_wrong_deterministic_assignment_is_rejected():
    packages = _packages()
    node = _shard(packages, 1)[1]["assigned"][0]
    _move(packages, node, 1, 2)
    text = _audit(packages)
    assert "shard 1: assignment differs" in text and "shard 2: assignment differs" in text


def test_overlapping_assignment_is_rejected():
    packages = _packages()
    node = _shard(packages, 1)[1]["assigned"][0]
    _move(packages, node, 1, 2)
    _p, ev1, cases1 = _shard(packages, 1)
    ev1["assigned"] = sorted(ev1["assigned"] + [node])              # now in shard 1 AND shard 2
    ev1["outcomes"].append({"nodeid": node, "outcome": "passed", "reports": 1})
    cases1.append(_junit_case(node, "pass"))
    assert "assignment overlaps another shard" in _audit(packages)


def test_assignment_gap_is_rejected():
    packages = _packages()
    node = _shard(packages, 3)[1]["assigned"][0]
    _p, ev, cases = _shard(packages, 3)
    ev["assigned"].remove(node)
    ev["outcomes"] = [o for o in ev["outcomes"] if o["nodeid"] != node]
    del cases[0]
    assert "assignment union differs from the full collection (1 missing)" in _audit(packages)


def test_missing_result_is_rejected():
    packages = _packages()
    _shard(packages, 1)[1]["outcomes"].pop()
    assert "shard 1: 1 assigned nodes have no result" in _audit(packages)


def test_extra_result_is_rejected():
    packages = _packages()
    stranger = _shard(packages, 2)[1]["assigned"][0]
    _shard(packages, 1)[1]["outcomes"].append({"nodeid": stranger, "outcome": "passed", "reports": 1})
    assert "shard 1: 1 unassigned nodes executed" in _audit(packages)


def test_double_reported_node_is_rejected():
    packages = _packages()
    _shard(packages, 1)[1]["outcomes"][0]["reports"] = 2
    assert "has 2 execution outcomes" in _audit(packages)


def _replace_case(packages, node, kind, outcome):
    for _p, ev, cases in packages:
        if node in ev["assigned"]:
            idx = next(i for i, c in enumerate(cases) if c.get("name") == node.split("::")[-1])
            cases[idx] = _junit_case(node, kind)
            next(o for o in ev["outcomes"] if o["nodeid"] == node)["outcome"] = outcome
            return


@pytest.mark.parametrize("kind, outcome, expected", [
    ("skip:not an allowed reason", "skipped", "unexpected skip/xfail"),
    ("xfail:not the known xfail", "xfailed", "unexpected skip/xfail"),
    ("failure", "failed", "failure/error"),
    ("error", "error", "failure/error"),
])
def test_unexpected_skip_xfail_failure_and_error_are_rejected(kind, outcome, expected):
    packages = _packages()
    _replace_case(packages, _PLAIN[0], kind, outcome)
    text = _audit(packages)
    assert expected in text
    if outcome in ("failed", "error"):
        assert f"{_PLAIN[0]} {outcome}" in text


def test_allowed_skip_with_the_wrong_type_is_rejected():
    packages = _packages()
    node = "tests/test_wps001_invariants.py::TestWPS001_INV004_GapLifecycle::test_closed_gap_does_not_reopen"
    _replace_case(packages, node, "xfail:No gaps reached CLOSED — cannot test forward-only", "xfailed")
    assert "unexpected skip/xfail" in _audit(packages)


def test_strict_xpass_is_rejected():
    packages = _packages()
    _replace_case(packages, _PLAIN[1], "pass", "xpassed")
    assert f"{_PLAIN[1]} xpassed" in _audit(packages)


@pytest.mark.parametrize("field, value, expected", [
    ("collection_errors", [{"nodeid": "tests/test_x.py", "detail": "boom"}], "collection errors"),
    ("pytest_exit_status", 1, "pytest exit status 1"),
    ("repository_clean", False, "repository-clean check did not pass"),
    ("plugin_record_present", False, "shard plugin record missing"),
    ("schema", "other", "unknown evidence schema"),
])
def test_shard_level_failures_are_rejected(field, value, expected):
    packages = _packages()
    _shard(packages, 2)[1][field] = value
    assert expected in _audit(packages)


@pytest.mark.parametrize("key", ["run_id", "run_attempt", "expected_base", "expected_head", "tested_merge",
                                 "tested_tree"])
def test_stale_mixed_or_foreign_identity_is_rejected(key):
    packages = _packages()
    _shard(packages, 3)[1][key] = "9" if key.startswith("run") else "f" * 40
    assert f"shard 3: {key}" in _audit(packages) and "does not match the audit run" in _audit(packages)


def test_missing_junit_evidence_is_rejected():
    packages = _packages()
    p, ev, _cases = _shard(packages, 1)
    packages[packages.index(_shard(packages, 1))] = (p, ev, None)
    assert "shard 1: JUnit evidence missing" in _audit(packages)


def test_junit_case_count_mismatch_is_rejected():
    packages = _packages()
    _shard(packages, 2)[2].append(_junit_case("tests/test_zzz.py::test_ghost", "pass"))
    assert "JUnit has" in _audit(packages)


@pytest.mark.parametrize("node", ["tests/test_draft_l2_local_continuity.py::test_browser_draft",
                                  "tests/test_p5_2_draft_account_switch.py::test_switch"])
def test_missing_mandatory_browser_evidence_is_rejected(node):
    problems = cfs.audit(_packages(omit=(node,)), EXPECTED)
    module = cfs.file_of(node)[:-3].replace("/", ".")
    assert problems == [f"mandatory browser module did not pass: {module}"]


def test_missing_mandatory_gunicorn_evidence_is_rejected():
    node = "tests/test_email_h1_access_log_token_redaction.py::test_real_gunicorn_access_log_contains_no_raw_token"
    assert cfs.audit(_packages(omit=(node,)), EXPECTED) == ["real server security proof missing"]
    packages = _packages()
    _replace_case(packages, node, "skip:not allowed", "skipped")
    assert "real server security proof missing" in _audit(packages)


def test_load_evidence_reads_every_downloaded_package(tmp_path):
    for s, (_p, ev, cases) in zip((1, 2, 3), _packages()):
        d = tmp_path / f"full-shard-evidence-1001-2-shard-{s}"
        d.mkdir()
        (d / cfs.EVIDENCE_FILE).write_text(json.dumps(ev), encoding="utf-8")
        suite = ET.Element("testsuite")
        suite.extend(cases)
        root = ET.Element("testsuites")
        root.append(suite)
        (d / cfs.JUNIT_FILE).write_bytes(ET.tostring(root))
    packages = cfs.load_evidence(tmp_path)
    assert [p[1]["shard"] for p in packages] == [1, 2, 3]
    assert cfs.audit(packages, EXPECTED) == []


# ==========================================================================
# workflow helpers (text, no YAML parser)
# ==========================================================================
def _workflow():
    return WORKFLOW.read_text(encoding="utf-8")


def _jobs(text=None):
    text = _workflow() if text is None else text
    body = text[text.index("\njobs:\n") + 7:]
    starts = [(m.group(1), m.start()) for m in re.finditer(r"^  ([a-z_]+):\n", body, re.M)]
    return {name: body[pos:(starts[i + 1][1] if i + 1 < len(starts) else len(body))]
            for i, (name, pos) in enumerate(starts)}


def _step(job, name):
    start = job.index(f"      - name: {name}")
    nxt = job.find("\n      - name: ", start + 1)
    return job[start:] if nxt == -1 else job[start:nxt]


def _code(job):
    return "\n".join(line for line in job.splitlines() if not line.lstrip().startswith("#"))


def _header(job):
    return job.split("    steps:\n")[0]


def _needs(job):
    found = re.findall(r"^    needs: \[(.*)\]$", _header(job), re.M)
    return [n.strip() for n in found[0].split(",")] if found else []


def _job_if(job):
    found = re.findall(r"^    if: (.+)$", _header(job), re.M)
    return found[0] if found else None


def _heredoc(block):
    return textwrap.dedent(block[block.index("<<'PY'\n") + 7:block.rindex("\n          PY")])


GATE = ("scope", "verify", "full_shard", "required")
PASSIVE_SIX = frozenset({
    "CLAUDE.md",
    "docs/governance/LEAN_GOVERNANCE_AND_AGENT_CONTINUITY_PROTOCOL.md",
    "docs/governance/ACCELERATED_HIGH_ASSURANCE_EXECUTION_PROTOCOL.md",
    "docs/governance/ACTIVE_INCREMENT_CONTRACT.md",
    "docs/governance/ACTIVE_EXECUTION_ROADMAP.md",
    "docs/governance/CURRENT_PROJECT_STATE.md",
})


# ==========================================================================
# the permanent owner of the mandatory FULL-audit semantics
# ==========================================================================
# Independently pinned expected values: a material change to any of them in
# scripts/ci_full_suite.py must come with an intentional change here.
EXPECTED_ALLOWED_SKIPS = {
    ("tests.test_fdc001_contract.TestFDC001_S7_CategoriesBC_Deferred", "test_category_b_deferred"):
        {"ODS-001 exists"},
    ("tests.test_fdc001_contract.TestFDC001_S7_CategoriesBC_Deferred", "test_category_c_deferred"):
        {"ODS-001 exists"},
    ("tests.test_fdc001_contract.TestFDC001_S7_CategoriesBC_Deferred", "test_category_b_note_references_ods001"):
        {"ODS-001 exists"},
    ("tests.test_wps001_invariants.TestWPS001_INV004_GapLifecycle", "test_closed_gap_does_not_reopen"):
        {"No gaps reached CLOSED — cannot test forward-only"},
    ("tests.test_w2c_rvr6b_web", "test_electronics_covered_intent_suppressed"):
        {"electronics journey did not open MECHANISM first",
         "journey advanced differently — covered elsewhere"},
}
EXPECTED_KNOWN_XFAIL = ("tests.test_f011_progression_quality_gate",
                        "test_f011_hall_sensor_alone_does_not_advance_level_0")
EXPECTED_KNOWN_XFAIL_REASON = "ADR-003 Step 6: component label only — no claim/basis/relationship"
EXPECTED_BROWSER_MODULES = ("tests.test_draft_l2_local_continuity", "tests.test_p5_2_draft_account_switch")
EXPECTED_SERVER_PROOF = ("tests.test_email_h1_access_log_token_redaction",
                         "test_real_gunicorn_access_log_contains_no_raw_token")


def test_mandatory_constants_are_pinned_on_the_permanent_owner():
    assert cfs.ALLOWED_SKIPS == EXPECTED_ALLOWED_SKIPS
    assert cfs.KNOWN_XFAIL == EXPECTED_KNOWN_XFAIL
    assert cfs.KNOWN_XFAIL_REASON == EXPECTED_KNOWN_XFAIL_REASON
    assert cfs.MANDATORY_BROWSER_MODULES == EXPECTED_BROWSER_MODULES
    assert cfs.MANDATORY_SERVER_PROOF == EXPECTED_SERVER_PROOF


def test_the_mandatory_semantics_have_one_owner_and_no_inline_workflow_copy():
    text = _workflow()
    for literal in (EXPECTED_KNOWN_XFAIL_REASON, EXPECTED_KNOWN_XFAIL[1], EXPECTED_SERVER_PROOF[1],
                    *EXPECTED_BROWSER_MODULES, "ODS-001 exists"):
        assert literal not in text, literal
    jobs = _jobs()
    assert "python scripts/ci_full_suite.py --mode audit" in jobs["required"]
    assert text.count("--mode audit") == 1                     # the audit owner runs only in `required`
    for name, body in jobs.items():
        if name != "required":
            assert "--mode audit" not in body, name


# ==========================================================================
# topology and the protected gate
# ==========================================================================
def test_job_set_and_the_exact_protected_gate():
    jobs = _jobs()
    assert set(jobs) == {"scope", "verify", "fast", "full_shard", "required"}
    assert "full_audit" not in _code(_workflow()) and "Sharded FULL audit" not in _workflow()
    assert "full_monolithic_telemetry" not in _workflow() and "monolithic" not in _workflow().lower()
    required = jobs["required"]
    assert re.findall(r"^    name: (.+)$", required, re.M) == ["CI required"]
    assert _job_if(required) == "always()"
    assert _needs(required) == ["scope", "verify", "full_shard"]
    head = _header(required)
    assert re.findall(r"^    permissions:\n((?:      .*\n)*)", head, re.M) == ["      contents: read\n"]
    assert "write" not in head and "permissions: {}" not in head
    assert re.findall(r"^    timeout-minutes: (\d+)$", head, re.M) == ["15"]  # former audit 10 + verdict 5
    assert "continue-on-error" not in _code(required)


def test_the_required_dependency_chain_excludes_rig_fast():
    jobs = _jobs()
    closure, frontier = set(), ["required"]
    while frontier:
        job = frontier.pop()
        for dep in _needs(jobs[job]):
            assert dep in jobs, dep
            if dep not in closure:
                closure.add(dep)
                frontier.append(dep)
    assert closure == {"scope", "verify", "full_shard"}
    for name in GATE:
        assert "fast" not in _needs(jobs[name]), name
    assert _needs(jobs["fast"]) == []
    for name in jobs:                                   # nothing may wait on the advisory lane
        assert "fast" not in _needs(jobs[name]), name


def test_rig_cannot_influence_scope_shards_audit_or_verdict():
    jobs = _jobs()
    for name in GATE:
        body = _code(jobs[name]).lower().replace("fail-fast", "").replace("name: verify candidate (smoke route)", "")
        for word in (r"\brig\b", "repository_intelligence", "candidate", r"\bfast\b", "shadow", "telemetry",
                     "continue-on-error", "run_fast"):
            assert re.search(word, body) is None, (name, word)
        for ref in re.findall(r"needs\.([a-z_]+)\.", body):
            assert ref in GATE, (name, ref)
    source = (ROOT / "scripts" / "ci_full_suite.py").read_text(encoding="utf-8")
    assert "repository_intelligence" not in source and "rig-shadow" not in source


# ==========================================================================
# scope: the existing minimum-scope rule, moved unchanged
# ==========================================================================
def _scope_step():
    return _step(_jobs()["scope"], "Verify identity and select the minimum test scope")


def test_scope_always_runs_first_and_exposes_only_its_selection():
    scope = _jobs()["scope"]
    assert _needs(scope) == [] and _job_if(scope) is None
    assert "    outputs:\n      scope: ${{ steps.scope.outputs.scope }}\n" in scope
    assert "        id: scope\n" in _scope_step() and "ref: ${{ github.sha }}" in scope
    source = _heredoc(_scope_step())
    for line in ("assert git('rev-list', '--parents', '-n', '1', 'HEAD').decode().split() == [merge, base, head]",
                 "assert paths, 'An empty or unavailable diff cannot receive a green result'",
                 "if entry and not entry.startswith('100644 blob '):",
                 "scope = 'smoke' if all(map(documentation_only, paths)) else 'full'",
                 "output.write('scope=' + scope + '\\n')"):
        assert line in source, line
    for word in ("label", "github.event.pull_request.body", "workflow_dispatch", "inputs."):
        assert word not in _code(scope), word


def test_the_smoke_exemption_is_exactly_the_existing_six_passive_paths():
    tree = ast.parse(_heredoc(_scope_step()))
    sets = [node for node in ast.walk(tree) if isinstance(node, ast.Assign)
            and getattr(node.targets[0], "id", "") == "passive_authority"]
    assert len(sets) == 1
    assert frozenset(ast.literal_eval(sets[0].value)) == PASSIVE_SIX


def _scope_repo(root, changes, modes=()):
    root.mkdir(parents=True)
    _git(root, "init", "-q", "-b", "main")
    for path in sorted(PASSIVE_SIX) + ["engine/x.py", "docs/governance/OTHER.md"]:
        (root / path).parent.mkdir(parents=True, exist_ok=True)
        (root / path).write_text("base\n", encoding="utf-8")
    _git(root, "add", "-A")
    base = _git(root, "commit", "-q", "-m", "base")
    _git(root, "checkout", "-q", "-b", "pr")
    for path in changes:
        (root / path).parent.mkdir(parents=True, exist_ok=True)
        (root / path).write_text("changed\n", encoding="utf-8")
    for path in modes:
        (root / path).chmod(0o755)
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "--allow-empty", "-m", "head")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root).decode().strip()
    _git(root, "checkout", "-q", "main")
    merge = _git(root, "merge", "-q", "--no-ff", "-m", "merge", "pr")
    return base, head, merge


def _run_scope(tmp_path, base, head, merge, repo):
    out, summary = tmp_path / "out.txt", tmp_path / "summary.md"
    out.write_text("", encoding="utf-8")
    env = dict(os.environ, EXPECTED_BASE=base, EXPECTED_HEAD=head, EXPECTED_MERGE=merge,
               GITHUB_OUTPUT=str(out), GITHUB_STEP_SUMMARY=str(summary))
    proc = subprocess.run([sys.executable, "-c", _heredoc(_scope_step())], cwd=repo, env=env,
                          capture_output=True, text=True)
    return proc.returncode, out.read_text(encoding="utf-8")


@pytest.mark.parametrize("changes, expected", [
    (["CLAUDE.md"], "smoke"),
    (sorted(PASSIVE_SIX), "smoke"),
    (["engine/x.py"], "full"),
    (["docs/governance/OTHER.md"], "full"),
    (["docs/governance/INVENTORAI_MASTER_EXECUTION_ROADMAP.md"], "full"),
    ([".github/workflows/ci.yml"], "full"),
    (["scripts/ci_full_suite.py"], "full"),
    (["CLAUDE.md", "engine/x.py"], "full"),
    (["claude.md"], "full"),
    (["docs/governance/CURRENT_PROJECT_STATE.md.bak"], "full"),
])
def test_scope_selection_is_smoke_only_for_the_six_paths_and_otherwise_full(tmp_path, changes, expected):
    repo = tmp_path / "repo"
    base, head, merge = _scope_repo(repo, changes)
    code, out = _run_scope(tmp_path, base, head, merge, repo)
    assert code == 0 and out == f"scope={expected}\n"


def test_an_executable_passive_path_falls_back_to_full(tmp_path):
    repo = tmp_path / "repo"
    base, head, merge = _scope_repo(repo, ["CLAUDE.md"], modes=["CLAUDE.md"])
    code, out = _run_scope(tmp_path, base, head, merge, repo)
    assert code == 0 and out == "scope=full\n"


def test_an_empty_diff_or_a_wrong_identity_fails_closed_without_a_scope(tmp_path):
    repo = tmp_path / "repo"
    base, head, merge = _scope_repo(repo, [])
    code, out = _run_scope(tmp_path, base, head, merge, repo)
    assert code != 0 and out == ""
    repo2 = tmp_path / "repo2"
    base, head, merge = _scope_repo(repo2, ["CLAUDE.md"])
    for bad in ((base, "e" * 40, merge), (head, base, merge), (base, head, "short")):
        code, out = _run_scope(tmp_path, *bad, repo2)
        assert code != 0 and out == "", bad


# ==========================================================================
# the scope-aware `CI required` verdict, executed over its whole truth table
# ==========================================================================
_RESULTS = ("success", "failure", "cancelled", "skipped", "")
_SCOPES = ("smoke", "full", "", "SMOKE", "Full", "fullx", "smoke ")


def _gate_script():
    block = _step(_jobs()["required"], "Require the complete authoritative route for the selected scope")
    lines = block[block.index("        run: |\n") + len("        run: |\n"):].splitlines()
    body = []
    for line in lines:                                  # the literal block ends at the first dedent
        if line and not line.startswith("          "):
            break
        body.append(line)
    return textwrap.dedent("\n".join(body)).strip() + "\n"


def _gate(rows):
    """Run the literal `CI required` script (bash -e, as GitHub does) for each row:
    (scope result, scope, verify result, shard result, audit outcome, cleanliness outcome)."""
    script = _gate_script()
    lines = [f"( export SCOPE_RESULT='{r[0]}' SCOPE='{r[1]}' VERIFY_RESULT='{r[2]}' SHARD_RESULT='{r[3]}' "
             f"AUDIT_OUTCOME='{r[4]}' CLEAN_OUTCOME='{r[5]}'; "
             f"bash --noprofile --norc -eo pipefail -c \"$GATE\" >/dev/null 2>&1 ) "
             f"&& echo P || echo F" for r in rows]

    def drive(chunk):                                   # one fresh bash per row, as before
        return subprocess.run(["bash", "-s"], input="\n".join(chunk), env=dict(os.environ, GATE=script),
                              capture_output=True, text=True, check=True).stdout.split()

    size = -(-len(lines) // (os.cpu_count() or 1))      # contiguous chunks keep the row order
    with concurrent.futures.ThreadPoolExecutor() as pool:
        out = [o for part in pool.map(drive, [lines[i:i + size] for i in range(0, len(lines), size)])
               for o in part]
    assert len(out) == len(rows)
    return dict(zip(rows, (o == "P" for o in out)))


def test_gate_truth_table_passes_only_the_complete_selected_route():
    rows = [(sr, sc, v, s, a, c) for sr in _RESULTS for sc in _SCOPES
            for v in _RESULTS for s in _RESULTS for a in _RESULTS for c in _RESULTS]
    passing = {row for row, ok in _gate(rows).items() if ok}
    assert passing == {("success", "smoke", "success", "skipped", "skipped", "skipped"),
                       ("success", "full", "skipped", "success", "success", "success")}


@pytest.mark.parametrize("row, ok", [
    (("success", "smoke", "success", "skipped", "skipped", "skipped"), True),
    (("success", "full", "skipped", "success", "success", "success"), True),
    (("success", "full", "skipped", "failure", "failure", "success"), False),     # a shard failed; audit fails closed
    (("success", "full", "skipped", "failure", "success", "success"), False),     # evidence never masks a failed shard
    (("success", "full", "skipped", "cancelled", "success", "success"), False),   # nor a cancelled shard
    (("success", "full", "skipped", "cancelled", "failure", "success"), False),   # missing shard evidence
    (("success", "full", "skipped", "success", "failure", "success"), False),     # audit failure
    (("success", "full", "skipped", "success", "skipped", "success"), False),     # checkout / setup / download failed
    (("success", "full", "skipped", "success", "skipped", "failure"), False),     # checkout failed
    (("success", "full", "skipped", "success", "cancelled", "success"), False),   # audit cancelled
    (("success", "full", "skipped", "success", "success", "failure"), False),     # dirty checkout
    (("success", "full", "skipped", "success", "success", "skipped"), False),     # cleanliness never checked
    (("success", "full", "skipped", "success", "failure", "failure"), False),
    (("success", "full", "skipped", "skipped", "skipped", "skipped"), False),     # FULL route skipped
    (("success", "full", "success", "success", "success", "success"), False),     # SMOKE route ran on a FULL change
    (("success", "smoke", "skipped", "skipped", "skipped", "skipped"), False),    # SMOKE route skipped
    (("success", "smoke", "success", "success", "skipped", "skipped"), False),    # FULL route ran on a SMOKE change
    (("success", "smoke", "success", "skipped", "success", "success"), False),    # the audit ran on a SMOKE change
    (("success", "smoke", "success", "skipped", "skipped", "success"), False),
    (("success", "smoke", "failure", "skipped", "skipped", "skipped"), False),
    (("failure", "smoke", "success", "skipped", "skipped", "skipped"), False),    # failed scope job
    (("failure", "full", "skipped", "success", "success", "success"), False),
    (("cancelled", "full", "skipped", "success", "success", "success"), False),
    (("skipped", "", "skipped", "skipped", "skipped", "skipped"), False),         # everything skipped
    (("success", "", "skipped", "skipped", "skipped", "skipped"), False),         # missing scope
    (("success", "unknown", "success", "success", "success", "success"), False),  # invalid scope
])
def test_gate_named_rows(row, ok):
    assert _gate([row])[row] is ok


def test_the_gate_never_accepts_skipped_generically():
    script = _gate_script()
    assert script.count("= skipped") == 4 and "!= skipped" not in script and "|| true" not in script
    assert "verdict=fail\n" in script and script.rstrip().endswith('test "$verdict" = pass')
    env = _step(_jobs()["required"], "Require the complete authoritative route for the selected scope")
    assert "        if: always()\n" in env
    for line in ("SCOPE_RESULT: ${{ needs.scope.result }}", "SCOPE: ${{ needs.scope.outputs.scope }}",
                 "VERIFY_RESULT: ${{ needs.verify.result }}", "SHARD_RESULT: ${{ needs.full_shard.result }}",
                 "AUDIT_OUTCOME: ${{ steps.audit.outcome }}", "CLEAN_OUTCOME: ${{ steps.audit_clean.outcome }}"):
        assert line in env, line
    assert "needs.full_audit" not in _workflow()


# ==========================================================================
# the two routes
# ==========================================================================
_ENV_STEPS = ("Set up the repository-required Python", "Install the matching Chromium and Linux prerequisites",
              "Require a working interpreter, server and real browser", "Universal guardrail smoke",
              "Confirm repository data was not changed")


def test_smoke_route_keeps_the_existing_smoke_behaviour_only_for_smoke():
    verify = _jobs()["verify"]
    assert _needs(verify) == ["scope"]
    assert _job_if(verify) == "needs.scope.result == 'success' && needs.scope.outputs.scope == 'smoke'"
    steps = re.findall(r"^      - name: (.+)$", verify, re.M)
    assert steps == ["Check out the exact proposed merge", "Verify the tested-merge identity",
                     "Set up the repository-required Python",
                     "Install existing pinned inputs into an isolated environment",
                     "Install the matching Chromium and Linux prerequisites",
                     "Require a working interpreter, server and real browser", "Universal guardrail smoke",
                     "Confirm repository data was not changed"]
    assert "python scripts/run_universal_smoke.py" in verify and "INVENTORAI_DRAFT_L2_REQUIRE_BROWSER: '1'" in verify
    assert "'-m', 'pytest'" not in verify and "ci_full_suite" not in verify
    assert "assert parents == [merge, base, head]" in verify and "ref: ${{ github.sha }}" in verify
    proof = _step(verify, "Require a working interpreter, server and real browser")
    for line in ("assert server, 'Mandatory Gunicorn prerequisite missing'", "playwright.chromium.launch(headless=True)"):
        assert line in proof, line


def test_full_route_is_the_unmasked_three_shard_matrix_after_scope():
    shard = _jobs()["full_shard"]
    head = _header(shard)
    assert _needs(shard) == ["scope"]
    assert _job_if(shard) == "needs.scope.result == 'success' && needs.scope.outputs.scope == 'full'"
    assert "      fail-fast: false\n" in head and "        shard: [1, 2, 3]\n" in head
    assert "runs-on: ubuntu-24.04" in head
    for name in ("full_shard", "required"):
        assert "continue-on-error" not in _code(_jobs()[name]), name
    run = _step(shard, "Run this shard of the FULL suite")
    assert "python scripts/ci_full_suite.py --mode shard --shard ${{ matrix.shard }} --count 3" in run
    for word in ("-k", "-m ", "--deselect", "--lf", "xdist", "pytest-split", "rig"):
        assert word not in run, word


def test_every_shard_keeps_the_verify_environment_and_mandatory_proofs():
    jobs = _jobs()
    shard, verify = jobs["full_shard"], jobs["verify"]
    assert "INVENTORAI_DRAFT_L2_REQUIRE_BROWSER: '1'" in shard
    for name in _ENV_STEPS + ("Verify the tested-merge identity",):
        assert _code(_step(shard, name)).strip() == _code(_step(verify, name)).strip(), name
    install = _code(_step(shard, "Install existing pinned inputs into an isolated environment"))
    assert install == _code(_step(verify, "Install existing pinned inputs into an isolated environment"))
    assert "ref: ${{ github.sha }}" in shard and "assert parents == [merge, base, head]" in shard


def test_chromium_prerequisite_install_is_bounded_and_fail_closed():
    # CI Correction 01: an unbounded apt-get update inside `--with-deps` hung a runner
    # for the whole job. Every lane installs the same packages and browser with hard
    # deadlines, a fixed try budget, apt-lock cleanup and a visible failure.
    jobs = _jobs()
    name = "Install the matching Chromium and Linux prerequisites"
    authoritative = _code(_step(jobs["full_shard"], name))
    assert "python -m playwright install --with-deps" not in _workflow()
    for line in ("        timeout-minutes: 20",
                 'sudo timeout --kill-after=20s 240s env LD_LIBRARY_PATH="${LD_LIBRARY_PATH:-}"',
                 '"$PY" -m playwright install-deps chromium || rc=$?',
                 "timeout --kill-after=20s 180s python -m playwright install chromium || rc=$?",
                 "for try in 1 2 3; do", "for try in 1 2; do", "release_apt",
                 "::error::Linux prerequisites for Chromium were not installed after 3 bounded tries",
                 "::error::Chromium was not installed after 2 bounded tries"):
        assert line in authoritative, line
    assert "continue-on-error" not in authoritative and "|| true\n          done" not in authoritative
    fast = _code(_step(jobs["fast"], name + " (fast lane)"))
    assert fast.replace("        if: steps.fastplan.outputs.run_fast == 'true'\n", "").replace(
        " (fast lane)", "") == authoritative


_FULL_ONLY = "needs.scope.result == 'success' && needs.scope.outputs.scope == 'full'"
_REQUIRED_STEPS = ("Check out the exact proposed merge", "Set up the repository-required Python",
                   "Download the current attempt's shard evidence only",
                   "Audit FULL-suite completeness and mandatory semantics", "Confirm repository data was not changed",
                   "Require the complete authoritative route for the selected scope")


def test_the_full_audit_in_required_runs_for_full_even_after_a_shard_failure_and_is_fail_closed():
    required = _jobs()["required"]
    assert _job_if(required) == "always()"              # runs after a failed or cancelled shard
    assert re.findall(r"^      - name: (.+)$", required, re.M) == list(_REQUIRED_STEPS)
    # The FULL-only steps depend on the selected scope only, never on the shard
    # result, and keep the implicit success(): a failed checkout, setup or
    # download leaves the audit `skipped`, which the verdict rejects.
    for name in _REQUIRED_STEPS[:4]:
        step = _step(required, name)
        assert re.findall(r"^        if: (.+)$", step, re.M) == [_FULL_ONLY], name
        assert "full_shard" not in step and "always()" not in step, name
    audit = _step(required, "Audit FULL-suite completeness and mandatory semantics")
    assert "        id: audit\n" in audit
    assert "python scripts/ci_full_suite.py --mode audit --evidence-dir" in audit
    assert "|| true" not in audit and "|| echo" not in audit
    clean = _step(required, "Confirm repository data was not changed")
    assert "        id: audit_clean\n" in clean
    assert f"        if: always() && {_FULL_ONLY}\n" in clean     # a failed audit cannot hide the cleanliness state
    assert _code(clean).split("run: |\n")[1] == _code(
        _step(_jobs()["full_shard"], "Confirm repository data was not changed")).split("run: |\n")[1]
    checkout = _step(required, "Check out the exact proposed merge")
    for line in ("ref: ${{ github.sha }}", "fetch-depth: 0", "persist-credentials: false"):
        assert line in checkout, line
    head = _header(required)                            # the audit's run / attempt / merge identity inputs
    for line in ("EXPECTED_BASE: ${{ github.event.pull_request.base.sha }}",
                 "EXPECTED_HEAD: ${{ github.event.pull_request.head.sha }}", "EXPECTED_MERGE: ${{ github.sha }}"):
        assert line in head, line


def test_evidence_transfer_is_scoped_to_the_current_run_and_attempt():
    jobs = _jobs()
    upload = _step(jobs["full_shard"], "Upload this shard's evidence (current run and attempt only)")
    assert "if: always()" in upload and "if-no-files-found: error" in upload
    assert "name: full-shard-evidence-${{ github.run_id }}-${{ github.run_attempt }}-shard-${{ matrix.shard }}" \
        in upload
    download = _step(jobs["required"], "Download the current attempt's shard evidence only")
    assert "pattern: full-shard-evidence-${{ github.run_id }}-${{ github.run_attempt }}-shard-*" in download
    assert "merge-multiple" not in download and "run-id" not in download and "github-token" not in download


def test_every_external_action_is_pinned_to_a_full_commit_sha():
    uses = re.findall(r"^\s+uses: (\S+)", _workflow(), re.M)
    assert uses
    for ref in uses:
        assert re.fullmatch(r"[\w.-]+/[\w.-]+@[0-9a-f]{40}", ref), ref
    assert "actions/upload-artifact@043fb46d1a93c77aae656e7c1c64a875d1fc6a0a" in uses
    assert "actions/download-artifact@3e5f45b2cfb9172054b4087a40e8e0b5a5461e7c" in uses
