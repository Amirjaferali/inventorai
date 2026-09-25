"""Repository Intelligence (RIG) — advisory analyzer, policy and fault contract.

File-creation contract:
  Path: tests/test_repository_intelligence.py
  Purpose: prove the RIG-1B contract (`rig-contract-1b.0`) as implemented by
    `scripts/repository_intelligence.py`: strict import resolution, the closed
    evidence vocabulary, pytest/fixture evidence, literal and artifact
    evidence, source-anchored uncertainty, BASE ∪ HEAD impact, the separate
    advisory policy (FULL triggers, centrality, self-certification, SMOKE /
    AFFECTED-CANDIDATE qualification) and deterministic output. Fault cases
    run against throwaway git repositories under `tmp_path`; a few read-only
    checks run against this repository's HEAD.
  Input contract: git on PATH; no network; the real repository is only read.
  Output contract: pass/fail evidence only. The 15-case historical replay is
    deliberately NOT run here (explicit tool:
    `scripts/verify_repository_intelligence_replay.py`).
  Prohibited behaviors: no mutation of the real repository, no network, no
    claim that RIG may skip any CI test.
"""
import json
import os
import subprocess

import pytest

from scripts import repository_intelligence as rig

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ─────────────────────────────────────────────────────────────────────────────
# throwaway repositories
# ─────────────────────────────────────────────────────────────────────────────

def _git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), "-c", "user.email=rig@test", "-c", "user.name=rig",
                           "-c", "commit.gpgsign=false", *args], capture_output=True, text=True, check=True).stdout


class Repo:
    def __init__(self, path):
        self.path = str(path)
        os.makedirs(self.path, exist_ok=True)
        _git(path, "init", "-q")

    def write(self, files):
        for rel, content in files.items():
            full = os.path.join(self.path, rel)
            if content is None:
                if os.path.exists(full):
                    os.remove(full)
                continue
            os.makedirs(os.path.dirname(full), exist_ok=True)
            with open(full, "w", encoding="utf-8") as fh:
                fh.write(content)

    def commit(self, files=None, message="c"):
        if files:
            self.write(files)
        _git(self.path, "add", "-A")
        _git(self.path, "commit", "-q", "--allow-empty", "-m", message)
        return _git(self.path, "rev-parse", "HEAD").strip()

    def mv(self, old, new):
        _git(self.path, "mv", old, new)

    def analyse(self, base, head):
        return rig.analyse(self.path, base, head)

    def graph(self, rev):
        return rig.EvidenceGraph(rig.Snapshot(self.path, rev))


def _tests(prefix, n, body):
    return {f"tests/test_{prefix}_{i}.py": body + f"\n\ndef test_{prefix}_{i}():\n    assert True\n" for i in range(n)}


BASELINE = {
    "engine/__init__.py": "",
    "engine/core.py": "def shared():\n    return 1\n",
    "engine/iso.py": "def isolated():\n    return 2\n",
    "engine/helper.py": "def get():\n    return 3\n\ndef read():\n    return 4\n",
    "web/app.py": "from flask import Flask\nfrom engine import core\napp = Flask(__name__)\n",
    "gunicorn.conf.py": "workers = 1\n",
    "Dockerfile": 'FROM python:3.11\nCOPY requirements.txt ./\nCOPY . .\nCMD ["gunicorn", "-c", "gunicorn.conf.py", "web.app:app"]\n',
    ".dockerignore": ".git\n",
    "requirements.txt": "flask==3.1.3\n",
    "pytest.ini": "[pytest]\ntestpaths = tests\n",
    ".github/workflows/ci.yml": "jobs:\n  t:\n    steps:\n      - run: pip install -r requirements.txt\n      - run: python -m pytest\n",
    "docs/readme_note.md": "passive note\n",
    "docs/read_by_test.md": "consumed\n",
    "engine/record_store.py": "SCHEMA = 'CREATE TABLE t (x)'\n",
    "database/schema.sql": "CREATE TABLE t (x);\n",
    "tests/test_iso.py": "from engine.iso import isolated\n\ndef test_iso():\n    assert isolated() == 2\n",
    "tests/test_doc.py": "from pathlib import Path\nROOT = Path(__file__).resolve().parents[1]\n\n"
                         "def test_doc():\n    assert (ROOT / 'docs' / 'read_by_test.md').exists()\n",
    **_tests("core", 6, "from engine.core import shared"),
    **_tests("plain", 6, "import os"),
}


@pytest.fixture
def repo(tmp_path):
    r = Repo(tmp_path / "r")
    r.base = r.commit(BASELINE, "baseline")
    return r


def _scope(report):
    return report["advisory_scope"]


# ─────────────────────────────────────────────────────────────────────────────
# 1. strict import resolution and the evidence model
# ─────────────────────────────────────────────────────────────────────────────

def test_parent_package_never_stands_in_for_a_missing_module(repo):
    head = repo.commit({"tests/test_broken.py": "from engine.missing_module import X\n\ndef test_b():\n    assert X\n"})
    g = repo.graph(head)
    assert {"location": "tests/test_broken.py:1", "module": "engine.missing_module"} in g.unresolved_imports
    assert not any(e["source"] == "tests/test_broken.py" and e["target"] == "engine/__init__.py"
                   and e["derivation_rule"] == "ast-import" for e in g.edges)
    assert g.completeness()["status"] == "complete-with-reported-gaps"
    report = repo.analyse(repo.base, head)
    assert _scope(report) == "FULL"
    assert any(r.startswith("analysis-incomplete: unresolved repository import") for r in report["policy_reasons"])


def test_namespace_package_and_submodule_resolve_exactly(repo):
    g = repo.graph(repo.base)
    assert g.is_namespace_package("web") and g.module_file("web.app") == "web/app.py"
    assert g.module_file("engine") == "engine/__init__.py" and g.module_file("engine.missing") is None


def test_every_edge_carries_the_contract_fields_and_closed_vocabulary(repo):
    g = repo.graph(repo.base)
    assert g.edges
    for e in g.edges:
        assert set(e) == {"source", "target", "type", "source_location", "derivation_rule", "resolution_status"}
        assert e["type"] in rig.EDGE_TYPES
    assert rig.EDGE_TYPES == ("import", "fixture_use", "literal_path", "artifact_reference")


def test_no_edge_from_generic_method_name_equality(repo):
    head = repo.commit({"engine/consumer.py": "def use(d, fh, s):\n    d.get('x')\n    fh.read()\n    s.update()\n    return 1\n"})
    g = repo.graph(head)
    assert not [e for e in g.edges if e["source"] == "engine/consumer.py"]


def test_nested_conditional_relative_and_bare_test_imports(repo):
    head = repo.commit({
        "engine/nested.py": "def f():\n    from engine import iso\n    return iso\n\nif True:\n    from . import core\n",
        "tests/helpers_x.py": "VALUE = 1\n",
        "tests/test_bare.py": "from helpers_x import VALUE\n\ndef test_bare():\n    assert VALUE\n",
    })
    g = repo.graph(head)
    targets = {(e["source"], e["target"]) for e in g.edges if e["type"] == "import"}
    assert ("engine/nested.py", "engine/iso.py") in targets
    assert ("engine/nested.py", "engine/core.py") in targets
    assert ("tests/test_bare.py", "tests/helpers_x.py") in targets


# ─────────────────────────────────────────────────────────────────────────────
# 2. pytest evidence
# ─────────────────────────────────────────────────────────────────────────────

def test_fixture_requests_dependencies_shadowing_and_lookup(repo):
    prep = repo.commit({
        "tests/fx/conftest.py": "import pytest\n\n@pytest.fixture\ndef dep():\n    return 1\n\n"
                                "@pytest.fixture\ndef top(dep):\n    return dep\n\n@pytest.fixture\ndef by_mark():\n    return 1\n\n"
                                "@pytest.fixture\ndef by_param(request):\n    return request.param\n",
        "tests/fx/test_use.py": "def test_top(top):\n    assert top\n",
        "tests/fx/test_mark.py": "import pytest\n\n@pytest.mark.usefixtures('by_mark')\ndef test_m():\n    assert True\n",
        "tests/fx/test_indirect.py": "import pytest\n\n@pytest.mark.parametrize('by_param', [1], indirect=True)\ndef test_i(by_param):\n    assert by_param\n",
        "tests/fx/test_lookup.py": "def test_l(request):\n    assert request.getfixturevalue('dep')\n",
        "tests/fx/test_computed.py": "def test_c(request):\n    name = 'dep'\n    assert request.getfixturevalue(name)\n",
        "tests/fx/test_shadow.py": "import pytest\n\n@pytest.fixture\ndef top():\n    return 9\n\ndef test_s(top):\n    assert top == 9\n",
    })
    g = repo.graph(prep)
    users = {e["source"] for e in g.edges if e["type"] == "fixture_use" and e["target"] == "tests/fx/conftest.py"}
    assert {"tests/fx/test_use.py", "tests/fx/test_mark.py", "tests/fx/test_indirect.py", "tests/fx/test_lookup.py"} <= users
    assert "tests/fx/test_shadow.py" not in users                          # local definition shadows conftest
    assert any(u["kind"] == "dynamic-fixture-lookup" and u["source"] == "tests/fx/test_computed.py" for u in g.uncertainties)
    # fixture-dependency change inside a non-autouse sub-conftest stays bounded
    head = repo.commit({"tests/fx/conftest.py": g.snap.text["tests/fx/conftest.py"].replace("return 1\n\n\n@pytest.fixture\ndef top", "return 5\n\n\n@pytest.fixture\ndef top")
                        .replace("def dep():\n    return 1", "def dep():\n    return 5")})
    report = repo.analyse(prep, head)
    assert _scope(report) == "AFFECTED-CANDIDATE"
    assert "tests/fx/test_use.py" in report["candidate_tests"]


def test_root_autouse_conftest_change_is_protected_full(repo):
    prep = repo.commit({"tests/conftest.py": "import pytest\n\n@pytest.fixture(autouse=True)\ndef iso_db():\n    yield\n"})
    head = repo.commit({"tests/conftest.py": "import pytest\n\n@pytest.fixture(autouse=True)\ndef iso_db():\n    yield 1\n"})
    report = repo.analyse(prep, head)
    assert _scope(report) == "FULL"
    assert "protected:autouse-or-hook-conftest: tests/conftest.py" in report["policy_reasons"]


def test_pytest_hooks_and_plugins_are_protected(repo):
    prep = repo.commit({"tests/conftest.py": "pytest_plugins = ['x']\n\ndef pytest_collection_modifyitems(items):\n    pass\n"})
    head = repo.commit({"tests/conftest.py": "pytest_plugins = ['y']\n\ndef pytest_collection_modifyitems(items):\n    pass\n"})
    reasons = repo.analyse(prep, head)["policy_reasons"]
    assert "protected:autouse-or-hook-conftest: tests/conftest.py" in reasons
    assert "protected:pytest-plugins: tests/conftest.py" in reasons


def test_monkeypatch_literal_target_links_the_module(repo):
    prep = repo.commit({"engine/knob.py": "VALUE = 1\n",
                        "tests/test_knob.py": "def test_k(monkeypatch):\n    monkeypatch.setattr('engine.knob.VALUE', 2)\n"})
    head = repo.commit({"engine/knob.py": "VALUE = 3\n"})
    report = repo.analyse(prep, head)
    assert _scope(report) == "AFFECTED-CANDIDATE" and "tests/test_knob.py" in report["evidence_tests"]


# ─────────────────────────────────────────────────────────────────────────────
# 3. literal, document and artifact evidence
# ─────────────────────────────────────────────────────────────────────────────

def test_literal_path_consumer_and_comments_docstrings_are_not_consumers(repo):
    head = repo.commit({"engine/reader.py": '"""Reads docs/readme_note.md in its docstring only."""\n'
                                            "# docs/readme_note.md mentioned in a comment\n"
                                            "def load():\n    return open('docs/read_by_test.md').read()\n"})
    g = repo.graph(head)
    targets = {e["target"] for e in g.edges if e["source"] == "engine/reader.py"}
    assert "docs/read_by_test.md" in targets
    assert "docs/readme_note.md" not in targets


def test_artifact_references_are_deterministic(repo):
    g = repo.graph(repo.base)
    rules = {(e["source"], e["target"], e["derivation_rule"]) for e in g.edges if e["type"] == "artifact_reference"}
    assert (".github/workflows/ci.yml", "requirements.txt", "pip-install-r") in rules
    assert (".github/workflows/ci.yml", "tests/test_iso.py", "pytest-invocation") in rules
    assert ("Dockerfile", "gunicorn.conf.py", "gunicorn-config") in rules
    assert ("Dockerfile", "web/app.py", "runtime-entrypoint") in rules
    assert ("Dockerfile", "requirements.txt", "docker-copy") in rules
    assert ("tests/test_iso.py", "pytest.ini", "pytest-testpaths") in rules
    assert any(u["kind"] == "broad-build-input" and u["source"] == "Dockerfile" for u in g.uncertainties)


def test_passive_markdown_is_smoke_and_consumed_markdown_is_not(repo):
    passive = repo.analyse(repo.base, repo.commit({"docs/readme_note.md": "changed\n"}))
    assert _scope(passive) == "SMOKE" and passive["passive_documents"] == ["docs/readme_note.md"]
    base2 = _git(repo.path, "rev-parse", "HEAD").strip()
    consumed = repo.analyse(base2, repo.commit({"docs/read_by_test.md": "changed\n"}))
    assert _scope(consumed) == "AFFECTED-CANDIDATE" and "tests/test_doc.py" in consumed["evidence_tests"]


def test_module_constant_directory_binds_runtime_discovery(repo):
    head = repo.commit({"tests/test_scan.py": "import os\nfrom pathlib import Path\nROOT = Path(__file__).resolve().parents[1]\n"
                                              "DATA = ROOT / 'docs'\n\ndef test_s():\n    assert os.listdir(DATA)\n"})
    g = repo.graph(head)
    [u] = [u for u in g.uncertainties if u["source"] == "tests/test_scan.py" and u["kind"] == "runtime-discovery"]
    assert u["scope"] == "dir:docs" and u["binding"] == "evaluated-literal"


# ─────────────────────────────────────────────────────────────────────────────
# 4. BASE ∪ HEAD impact and dynamic imports
# ─────────────────────────────────────────────────────────────────────────────

def test_deleted_file_keeps_its_observer_through_the_base_graph(repo):
    prep = repo.commit({"engine/gone.py": "Y = 1\n", "tests/test_gone.py": "from engine.gone import Y\n\ndef test_y():\n    assert Y\n"})
    head = repo.commit({"engine/gone.py": None})
    assert "tests/test_gone.py" not in repo.graph(head).dependents("engine/gone.py")    # head alone misses it
    report = repo.analyse(prep, head)
    assert _scope(report) == "AFFECTED-CANDIDATE" and "tests/test_gone.py" in report["candidate_tests"]


def test_renamed_file_keeps_its_observer_through_the_base_graph(repo):
    prep = repo.commit({"engine/old_name.py": "Z = 1\n", "tests/test_named.py": "from engine.old_name import Z\n\ndef test_z():\n    assert Z\n"})
    repo.mv("engine/old_name.py", "engine/new_name.py")
    head = repo.commit()
    report = repo.analyse(prep, head)
    assert {"new": "engine/new_name.py", "old": "engine/old_name.py", "status": "R"} in report["changed_paths"]
    assert _scope(report) == "AFFECTED-CANDIDATE" and "tests/test_named.py" in report["candidate_tests"]


def test_removed_import_uses_the_union(repo):
    prep = repo.commit({"engine/lib.py": "X = 1\n", "engine/user.py": "from engine import lib\n\ndef v():\n    return lib.X\n",
                        "tests/test_user.py": "from engine import user\n\ndef test_v():\n    assert user.v()\n"})
    head = repo.commit({"engine/lib.py": "X = 2\n", "engine/user.py": "def v():\n    return 1\n"})
    report = repo.analyse(prep, head)
    assert "tests/test_user.py" in report["candidate_tests"] and _scope(report) == "AFFECTED-CANDIDATE"


def test_nested_import_added_and_new_module_with_new_test(repo):
    added = repo.analyse(repo.base, repo.commit({"engine/iso.py": "def isolated():\n    from engine import helper\n    return 2\n"}))
    assert _scope(added) == "AFFECTED-CANDIDATE" and "tests/test_iso.py" in added["evidence_tests"]
    b2 = _git(repo.path, "rev-parse", "HEAD").strip()
    new = repo.analyse(b2, repo.commit({"engine/fresh.py": "def f():\n    return 3\n",
                                        "tests/test_fresh.py": "from engine.fresh import f\n\ndef test_f():\n    assert f() == 3\n"}))
    assert _scope(new) == "AFFECTED-CANDIDATE" and "tests/test_fresh.py" in new["candidate_tests"]


def test_literal_and_computed_dynamic_imports(repo):
    prep = repo.commit({"engine/dyn.py": "V = 1\n",
                        "tests/test_lit.py": "import importlib\n\ndef test_h():\n    assert importlib.import_module('engine.dyn').V\n",
                        "tests/test_comp.py": "import importlib\nNAME = 'dyn'\n\ndef test_i():\n    assert importlib.import_module('engine.' + NAME)\n"})
    g = repo.graph(prep)
    assert any(e["source"] == "tests/test_lit.py" and e["target"] == "engine/dyn.py" for e in g.edges)
    assert any(u["source"] == "tests/test_comp.py" and u["kind"] == "computed-dynamic-import" and u["scope"] == "prefix:engine."
               for u in g.uncertainties)
    report = repo.analyse(prep, repo.commit({"engine/dyn.py": "V = 2\n"}))
    assert _scope(report) == "AFFECTED-CANDIDATE"
    assert "tests/test_lit.py" in report["evidence_tests"] and "tests/test_comp.py" in report["candidate_tests"]


def test_computed_dynamic_import_in_central_code_is_material(repo):
    prep = repo.commit({"engine/core.py": "import importlib\n\ndef shared():\n    return 1\n\ndef load(n):\n    return importlib.import_module('engine.' + n)\n"})
    report = repo.analyse(prep, repo.commit({"engine/iso.py": "def isolated():\n    return 22\n"}))
    assert _scope(report) == "FULL"
    assert any(r.startswith("material-uncertainty: computed-dynamic-import in engine/core.py") for r in report["policy_reasons"])


def test_new_file_under_a_central_directory_loader_is_full(repo):
    prep = repo.commit({"engine/registry.py": "import os\n\ndef load(d):\n    return sorted(os.scandir(d))\n",
                        "engine/core.py": "from engine import registry\nREG = registry.load('domains/')\n\ndef shared():\n    return 1\n",
                        "domains/a/domain.json": "{}\n"})
    report = repo.analyse(prep, repo.commit({"domains/b/domain.json": "{}\n"}))
    assert _scope(report) == "FULL"
    assert any(r.startswith("material-uncertainty") for r in report["policy_reasons"])


# ─────────────────────────────────────────────────────────────────────────────
# 5. policy: protected triggers, centrality, self-certification
# ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("path, content, reason", [
    ("requirements.txt", "flask==3.1.4\n", "protected:dependency-manifest: requirements.txt"),
    ("tests/requirements-extra.txt", "x==1\n", "protected:dependency-manifest: tests/requirements-extra.txt"),
    ("Dockerfile", BASELINE["Dockerfile"] + "# x\n", "protected:container-build: Dockerfile"),
    (".dockerignore", ".git\n*.log\n", "protected:container-build: .dockerignore"),
    ("gunicorn.conf.py", "workers = 2\n", "protected:runtime-entrypoint-config: gunicorn.conf.py"),
    ("web/app.py", BASELINE["web/app.py"] + "# x\n", "protected:runtime-entrypoint: web/app.py"),
    ("engine/record_store.py", "SCHEMA = 'CREATE TABLE t (y)'\n", "protected:state/record/persistence-contract: engine/record_store.py"),
    ("database/schema.sql", "CREATE TABLE t (y);\n", "protected:database-schema: database/schema.sql"),
    (".github/workflows/ci.yml", BASELINE[".github/workflows/ci.yml"] + "# x\n", "protected:ci-workflow: .github/workflows/ci.yml"),
    ("pytest.ini", "[pytest]\ntestpaths = tests\nxfail_strict = true\n", "protected:test-runner-config: pytest.ini"),
    (".python-version", "3.11\n", "protected:interpreter-config: .python-version"),
    ("engine/__init__.py", "X = 1\n", "protected:package-initializer: engine/__init__.py"),
    ("scripts/run_universal_smoke.py", "print(1)\n", "protected:mandatory-guardrail: scripts/run_universal_smoke.py"),
])
def test_protected_full_triggers(repo, path, content, reason):
    report = repo.analyse(repo.base, repo.commit({path: content}))
    assert _scope(report) == "FULL" and reason in report["policy_reasons"], report["policy_reasons"]


def test_persistence_ddl_module_is_protected_even_when_undeclared(repo):
    prep = repo.commit({"engine/audit_store.py": "DDL = 'CREATE TABLE audit (x)'\n",
                        "tests/test_audit.py": "from engine import audit_store\n\ndef test_a():\n    assert audit_store.DDL\n"})
    report = repo.analyse(prep, repo.commit({"engine/audit_store.py": "DDL = 'CREATE TABLE audit (y)'\n"}))
    assert "protected:persistence-ddl: engine/audit_store.py" in report["policy_reasons"]


def test_centrality_constant_is_named_provisional_and_escalates(repo):
    assert rig.CENTRALITY_ESCALATION_SHARE == 0.25
    report = repo.analyse(repo.base, repo.commit({"engine/core.py": "def shared():\n    return 11\n"}))
    assert _scope(report) == "FULL"
    assert any(r.startswith("centrality-escalation: engine/core.py") and "provisional advisory constant" in r
               for r in report["policy_reasons"])


@pytest.mark.parametrize("path", rig.RIG_SELF_PATHS)
def test_rig_never_certifies_its_own_trust_rules(repo, path):
    report = repo.analyse(repo.base, repo.commit({path: "# changed\n"}))
    assert _scope(report) == "FULL"
    assert f"protected:rig-self-certification: {path}" in report["policy_reasons"]


def test_unclassified_path_and_unconsumed_data_are_full(repo):
    binary = repo.analyse(repo.base, repo.commit({"assets/logo.png": "not really png\n"}))
    assert "unclassified-changed-path: assets/logo.png" in binary["policy_reasons"]
    b2 = _git(repo.path, "rev-parse", "HEAD").strip()
    data = repo.analyse(b2, repo.commit({"data/orphan.json": "{}\n"}))
    assert _scope(data) == "FULL" and any(r.startswith("no-positive-evidence: no test is proven to exercise data/orphan.json")
                                          for r in data["policy_reasons"])


# ─────────────────────────────────────────────────────────────────────────────
# 6. output contract: determinism, health vs unavailable, wording
# ─────────────────────────────────────────────────────────────────────────────

def test_output_is_deterministic_and_advisory(repo, capsys):
    head = repo.commit({"engine/iso.py": "def isolated():\n    return 7\n"})
    first = json.dumps(repo.analyse(repo.base, head), sort_keys=True)
    second = json.dumps(repo.analyse(repo.base, head), sort_keys=True)
    assert first == second
    assert rig.main(["--repo", repo.path, "--base", repo.base, "--head", head]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["rig"]["authority"] == "advisory-only"
    assert out["advisory_scope"] == "AFFECTED-CANDIDATE" and out["candidate_tests"] == sorted(out["candidate_tests"])
    ctx = out["agent_context"]
    assert set(ctx) >= {"revision", "changed_paths", "relevant_source", "candidate_tests", "upstream_dependencies",
                        "downstream_dependents", "artifact_consumers", "central_or_shared", "uncertainties",
                        "suggested_files_to_read_first", "not_claimed"}
    assert "skipped" not in json.dumps({k: v for k, v in out.items() if k != "disclaimer"}).lower()
    assert "nothing was skipped" in out["disclaimer"]


def test_unavailable_analysis_is_distinct_and_full(tmp_path, capsys):
    assert rig.main(["--repo", str(tmp_path), "--base", "HEAD~1", "--head", "HEAD"]) == 2
    out = json.loads(capsys.readouterr().out)
    assert out["analysis_status"] == "unavailable" and out["advisory_scope"] == "FULL"


# ─────────────────────────────────────────────────────────────────────────────
# 7. this repository (read-only, HEAD)
# ─────────────────────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def head_graph():
    return rig.EvidenceGraph(rig.Snapshot(ROOT, "HEAD"))


def test_every_tracked_test_is_discovered_and_parsed(head_graph):
    tracked = subprocess.run(["git", "-C", ROOT, "ls-files", "tests/"], capture_output=True, text=True, check=True).stdout.split()
    expected = sorted(p for p in tracked if p.endswith(".py") and p.split("/")[-1].startswith("test_"))
    assert head_graph.tests == expected
    health = head_graph.completeness()
    assert health["tracked_tests"] == health["parsed_tests"] == len(expected)
    assert health["unresolved_imports"] == []
    assert health["contract_version"] == rig.CONTRACT_VERSION


def test_orchestration_area_is_bounded_and_central_files_are_not(head_graph):
    tests = set(head_graph.tests)
    orch = {d for d in head_graph.dependents("engine/technical_orchestration_openai.py") if d in tests}
    required = {"tests/test_technical_orchestration_eval.py", "tests/test_technical_orchestration_shadow.py"}
    assert required <= orch                                                   # known evidence present
    assert len(orch) <= rig.CENTRALITY_ESCALATION_SHARE * len(tests)          # still bounded, not central
    assert "engine/idea_state.py" in head_graph.forward["engine/technical_orchestration_shadow.py"]
    for central in ("engine/idea_state.py", "engine/record_contract.py", "web/app.py"):
        reach = {d for d in head_graph.dependents(central) if d in tests}
        assert len(reach) > rig.CENTRALITY_ESCALATION_SHARE * len(tests), central
