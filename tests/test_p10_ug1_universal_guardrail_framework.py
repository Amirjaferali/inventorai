"""P10-UG1 — Universal Core Guardrail & Smoke Framework (framework guards).

File-creation contract:
  Path: tests/test_p10_ug1_universal_guardrail_framework.py
  Purpose: enforce the Universal Core Guardrail & Smoke Framework itself —
    the machine-checkable guard inventory (`tests/universal_guardrail_manifest.py`),
    the canonical smoke runner (`scripts/run_universal_smoke.py`), and the
    governance standard
    (`docs/governance/INVENTORAI_UNIVERSAL_CORE_GUARDRAIL_SMOKE_STANDARD.md`).
    These tests run in the FULL governed suite, so deleting a blocking guard,
    downgrading BLOCK → observation, renaming a canonical test out from under
    its guard, or stripping the runner's canonical output contract fails the
    suite — the framework's primary self-protection.
  Input contract: the manifest module loaded BY PATH (no package import), the
    runner script source and its subprocess behavior against hermetic
    tmp-manifest/tmp-test fixtures, and the standard document text.
  Output contract: pass/fail evidence only; tmp fixtures live under pytest
    tmp_path; no durable artifact is left behind.
  Prohibited behaviors: NO duplication of any canonical guard's assertions
    (guards are composed by node-id reference, never re-implemented here);
    NO network access; NO self-hashing of files (deliberately avoided —
    governed review owns byte-level change control).
"""
import importlib.util
import os
import re
import subprocess
import sys
import textwrap

_REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
_MANIFEST = os.path.join(_REPO, "tests", "universal_guardrail_manifest.py")
_RUNNER = os.path.join(_REPO, "scripts", "run_universal_smoke.py")
_STANDARD = os.path.join(
    _REPO, "docs", "governance",
    "INVENTORAI_UNIVERSAL_CORE_GUARDRAIL_SMOKE_STANDARD.md")

_REQUIRED_FIELDS = (
    "guard_id", "owner", "invariant", "blocking", "blocking_condition",
    "canonical_tests", "rationale", "introduced_by",
)

# The pinned blocking inventory: removing any of these guard ids, or
# downgrading one to non-blocking, fails the governed full suite.
_REQUIRED_BLOCKING_IDS = (
    "UG-CORE-01", "UG-CORE-02", "UG-CORE-03", "UG-CORE-04", "UG-CORE-05",
    "UG-CORE-06", "UG-CORE-07", "UG-CORE-08", "UG-CORE-09", "UG-CORE-10",
    "UG-CORE-11", "UG-CORE-12", "UG-CORE-13", "UG-CORE-14", "UG-CORE-15",
    # P10-PC3 governed framework change (contract §12; pinned in the same
    # candidate per the UG standard §6): UG-CORE-08 superseded in place by
    # its establishment-boundary successor; UG-CORE-16 (resume integrity)
    # added; UG-CORE-07 preserved unchanged (reviewer O1 disposition).
    "UG-CORE-16",
    "UG-META-01",
)
_REQUIRED_OBSERVATION_IDS = ("UG-OBS-01",)


def _load_manifest(path=_MANIFEST):
    spec = importlib.util.spec_from_file_location("ug_manifest_under_test", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _run_runner(env_extra=None, cwd=_REPO):
    env = dict(os.environ)
    env.update(env_extra or {})
    return subprocess.run(
        [sys.executable, _RUNNER], capture_output=True, text=True,
        env=env, cwd=cwd)


# ==========================================================================
# Machine-checkable guard inventory
# ==========================================================================
def test_manifest_module_exists_and_structure():
    assert os.path.exists(_MANIFEST), "universal guard manifest missing"
    mod = _load_manifest()
    guards = mod.GUARDS
    assert isinstance(guards, (list, tuple)) and guards
    seen = set()
    for g in guards:
        for field in _REQUIRED_FIELDS:
            assert field in g, "guard %r missing field %r" % (g.get("guard_id"), field)
        assert re.match(r"^UG-[A-Z]+-\d{2}$", g["guard_id"]), g["guard_id"]
        assert g["guard_id"] not in seen, "duplicate guard id"
        seen.add(g["guard_id"])
        assert isinstance(g["blocking"], bool)
        assert isinstance(g["canonical_tests"], (list, tuple)) and g["canonical_tests"]
        for node in g["canonical_tests"]:
            assert node.startswith("tests/"), (
                "canonical tests must live in the governed suite: %r" % node)


def test_core_blocking_inventory_pinned():
    """Self-protection: the required blocking guards exist AND stay blocking.
    A candidate cannot delete a guard or turn BLOCK into observation without
    editing THIS pinned inventory — an explicit governed framework change."""
    mod = _load_manifest()
    by_id = {g["guard_id"]: g for g in mod.GUARDS}
    for gid in _REQUIRED_BLOCKING_IDS:
        assert gid in by_id, "blocking guard %s was removed" % gid
        assert by_id[gid]["blocking"] is True, (
            "blocking guard %s was downgraded to non-blocking" % gid)
    for gid in _REQUIRED_OBSERVATION_IDS:
        assert gid in by_id, "observation guard %s was removed" % gid
        assert by_id[gid]["blocking"] is False


def test_all_canonical_tests_collectable():
    """Self-protection: every canonical test in the manifest must still be
    collectable — renaming or deleting one out from under its guard fails
    here (and the runner independently BLOCKs on it)."""
    mod = _load_manifest()
    nodes = [n for g in mod.GUARDS for n in g["canonical_tests"]]
    r = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "-q",
         "-p", "no:cacheprovider", *nodes],
        capture_output=True, text=True, cwd=_REPO)
    assert r.returncode == 0, (
        "canonical guard tests failed to collect:\n" + r.stdout[-2000:] + r.stderr[-500:])
    assert "error" not in r.stdout.lower().split("=")[-1]


# ==========================================================================
# Canonical runner semantics (hermetic — tmp manifests + tmp tests)
# ==========================================================================
def _write_tmp_fixture(tmp_path, blocking_node, observation_node):
    manifest = tmp_path / "tmp_manifest.py"
    manifest.write_text(textwrap.dedent("""
        GUARDS = [
            {"guard_id": "UG-TMP-01", "owner": "tmp", "invariant": "tmp blocking",
             "blocking": True, "blocking_condition": "test fails",
             "canonical_tests": [%r], "rationale": "probe", "introduced_by": "probe"},
            {"guard_id": "UG-TMP-02", "owner": "tmp", "invariant": "tmp observation",
             "blocking": False, "blocking_condition": "never blocks",
             "canonical_tests": [%r], "rationale": "probe", "introduced_by": "probe"},
        ]
    """ % (blocking_node, observation_node)), encoding="utf-8")
    return str(manifest)


def test_runner_pass_with_observation_failure_does_not_block(tmp_path):
    """A failing NON-BLOCKING observation must be REPORTED but must not BLOCK."""
    probe = tmp_path / "probe_obs_test.py"
    probe.write_text(
        "def test_ok():\n    assert True\n\n"
        "def test_obs_fails():\n    assert False, 'observation-only failure'\n",
        encoding="utf-8")
    manifest = _write_tmp_fixture(
        tmp_path, str(probe) + "::test_ok", str(probe) + "::test_obs_fails")
    r = _run_runner({"INVENTORAI_UG_MANIFEST": manifest})
    assert r.returncode == 0, r.stdout + r.stderr
    assert "UNIVERSAL GUARDRAIL SMOKE: PASS" in r.stdout
    assert "OBSERVATION" in r.stdout and "UG-TMP-02" in r.stdout


def test_runner_blocks_on_blocking_failure(tmp_path):
    probe = tmp_path / "probe_block_test.py"
    probe.write_text(
        "def test_core_broken():\n    assert False, 'invariant violated'\n\n"
        "def test_obs_ok():\n    assert True\n",
        encoding="utf-8")
    manifest = _write_tmp_fixture(
        tmp_path, str(probe) + "::test_core_broken", str(probe) + "::test_obs_ok")
    r = _run_runner({"INVENTORAI_UG_MANIFEST": manifest})
    assert r.returncode == 1
    assert "UNIVERSAL GUARDRAIL SMOKE: BLOCK" in r.stdout
    assert "UG-TMP-01" in r.stdout                       # guard attribution


def test_runner_blocks_on_missing_canonical_test(tmp_path):
    """Self-protection: a guard whose canonical test no longer exists (deleted,
    renamed, moved) is a BLOCK — never a silent skip."""
    probe = tmp_path / "probe_missing_test.py"
    probe.write_text("def test_ok():\n    assert True\n", encoding="utf-8")
    manifest = _write_tmp_fixture(
        tmp_path, str(probe) + "::test_DOES_NOT_EXIST", str(probe) + "::test_ok")
    r = _run_runner({"INVENTORAI_UG_MANIFEST": manifest})
    assert r.returncode == 1
    assert "UNIVERSAL GUARDRAIL SMOKE: BLOCK" in r.stdout
    assert "UG-TMP-01" in r.stdout


def test_runner_source_contract():
    assert os.path.exists(_RUNNER), "canonical smoke runner missing"
    src = open(_RUNNER, encoding="utf-8").read()
    assert "UNIVERSAL GUARDRAIL SMOKE: PASS" in src
    assert "UNIVERSAL GUARDRAIL SMOKE: BLOCK" in src
    assert "CORE INVARIANTS PRESERVED UNDER THIS SUITE" in src
    # deterministic and offline: the runner spawns pytest only
    assert "requests" not in src and "urllib" not in src


# ==========================================================================
# Governance standard document
# ==========================================================================
def test_standard_document_structure():
    assert os.path.exists(_STANDARD), "guardrail smoke standard missing"
    text = open(_STANDARD, encoding="utf-8").read()
    norm = re.sub(r"\s+", " ", text)
    # canonical execution command
    assert "scripts/run_universal_smoke.py" in norm
    # blocking semantics + prohibited interpretations (each must be denied)
    for phrase in ("UNIVERSAL GUARDRAIL SMOKE: PASS",
                   "UNIVERSAL GUARDRAIL SMOKE: BLOCK",
                   "CORE INVARIANTS PRESERVED UNDER THIS SUITE"):
        assert phrase in norm
    for denied in ("secure", "production ready", "legally compliant",
                   "PSRR complete", "deployment approved", "bug-free"):
        assert denied in norm, "prohibited interpretation %r not addressed" % denied
    # extension process fields
    for field in ("GUARD ID", "OWNER", "INVARIANT", "BLOCKING CONDITION",
                  "CANONICAL TEST", "RATIONALE", "INTRODUCED BY GATE"):
        assert field in norm
    # review escalation must defer to the standing protocol, never weaken it
    assert "LEAN_GOVERNANCE_AND_AGENT_CONTINUITY_PROTOCOL.md" in norm
    assert "OWNER DECISION REQUIRED" in norm


def test_smoke_selection_is_subset_of_governed_suite():
    mod = _load_manifest()
    for g in mod.GUARDS:
        for node in g["canonical_tests"]:
            path = node.split("::", 1)[0]
            assert os.path.exists(os.path.join(_REPO, path)), node
