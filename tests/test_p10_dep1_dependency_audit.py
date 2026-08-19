"""P10-DEP1 — Local Dependency-Audit Foundation: tooling tests (RED/GREEN).

File: tests/test_p10_dep1_dependency_audit.py
Purpose: deterministic validation of `scripts/run_dependency_audit.py` — the
smallest provider-neutral local wrapper around an OSV/PyPI-advisory audit tool
(pip-audit) for the single authoritative dependency input `requirements.txt`.
No test here performs a live network audit: tool behavior is simulated with
fake audit modules injected via PYTHONPATH and the wrapper's documented
tooling-only override `INVENTORAI_AUDIT_TOOL_MODULE`, so the suite stays
deterministic offline. The wrapper's load-bearing truths:
  * it audits the AUTHORITATIVE dependency input (repo-root requirements.txt),
    from any working directory;
  * a missing tool fails CLEARLY (exit 3, never success);
  * the tool's exit code is preserved verbatim — findings (exit 1) and
    advisory-network errors are NEVER converted into a clean PASS;
  * evidence header carries the repository SHA and the dependency-input
    SHA-256; no environment secrets are echoed;
  * the wrapper never mutates dependencies (audit only — no remediation).
Prohibited behaviors: no fabricated vulnerability claims; no live-network
assumption; no weakening to pass.
"""
import hashlib
import os
import subprocess
import sys
import textwrap

import pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WRAPPER = os.path.join(REPO_ROOT, "scripts", "run_dependency_audit.py")
REQUIREMENTS = os.path.join(REPO_ROOT, "requirements.txt")


def _fake_tool(tmp_path, name, body):
    pkg = tmp_path / name
    pkg.mkdir()
    (pkg / "__init__.py").write_text("")
    (pkg / "__main__.py").write_text(textwrap.dedent(body))
    return str(tmp_path)


def _run(tool_module, pythonpath=None, cwd=REPO_ROOT, extra_env=None):
    env = dict(os.environ)
    if pythonpath:
        env["PYTHONPATH"] = pythonpath + os.pathsep + env.get("PYTHONPATH", "")
    env["INVENTORAI_AUDIT_TOOL_MODULE"] = tool_module
    if extra_env:
        env.update(extra_env)
    return subprocess.run([sys.executable, WRAPPER], cwd=cwd, env=env,
                          capture_output=True, text=True, timeout=120)


OK_TOOL = """
import sys
print("FAKE-AUDIT argv:", sys.argv[1:])
print("No known vulnerabilities found")
sys.exit(0)
"""

VULN_TOOL = """
import sys
print("FAKE-FINDING: examplepkg 1.0 VULN-2026-0001 fix: 1.1")
sys.exit(1)
"""

NETFAIL_TOOL = """
import sys
sys.stderr.write("connection error: advisory service unreachable\\n")
sys.exit(2)
"""


def test_wrapper_exists_and_is_a_script():
    assert os.path.isfile(WRAPPER)


def test_wrapper_audits_authoritative_requirements(tmp_path):
    path = _fake_tool(tmp_path, "fake_audit_ok", OK_TOOL)
    result = _run("fake_audit_ok", pythonpath=path)
    assert result.returncode == 0, result.stderr
    # the tool was pointed at the repo-root requirements.txt
    assert "requirements.txt" in result.stdout
    assert "-r" in result.stdout
    # evidence header: repo SHA + dependency-input hash
    sha = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO_ROOT,
                         capture_output=True, text=True).stdout.strip()
    assert sha in result.stdout
    with open(REQUIREMENTS, "rb") as fh:
        req_hash = hashlib.sha256(fh.read()).hexdigest()
    assert req_hash in result.stdout
    # point-in-time boundary is stated on success
    assert "POINT-IN-TIME" in result.stdout


def test_wrapper_works_from_any_cwd(tmp_path):
    path = _fake_tool(tmp_path, "fake_audit_ok", OK_TOOL)
    result = _run("fake_audit_ok", pythonpath=path, cwd=str(tmp_path))
    assert result.returncode == 0, result.stderr
    assert "requirements.txt" in result.stdout


def test_tool_missing_fails_clearly_never_success(tmp_path):
    result = _run("definitely_no_such_audit_module_p10dep1")
    assert result.returncode == 3
    combined = result.stdout + result.stderr
    assert "TOOL MISSING" in combined
    assert "No known vulnerabilities" not in combined


def test_findings_exit_code_preserved_not_converted(tmp_path):
    path = _fake_tool(tmp_path, "fake_audit_vuln", VULN_TOOL)
    result = _run("fake_audit_vuln", pythonpath=path)
    assert result.returncode == 1                      # verbatim propagation
    assert "FAKE-FINDING" in result.stdout             # findings not suppressed
    combined = result.stdout + result.stderr
    assert "POINT-IN-TIME AUDIT: ZERO" not in combined # never a clean PASS


def test_network_failure_not_converted_to_clean_pass(tmp_path):
    path = _fake_tool(tmp_path, "fake_audit_netfail", NETFAIL_TOOL)
    result = _run("fake_audit_netfail", pythonpath=path)
    assert result.returncode == 2                      # tool's code preserved
    combined = result.stdout + result.stderr
    assert "connection error" in combined
    assert "ZERO KNOWN FINDINGS" not in combined
    assert "No known vulnerabilities" not in combined


def test_no_environment_secret_leakage(tmp_path):
    path = _fake_tool(tmp_path, "fake_audit_ok", OK_TOOL)
    secret = "p10dep1-super-secret-value-abc123"
    result = _run("fake_audit_ok", pythonpath=path,
                  extra_env={"INVENTORAI_SECRET_KEY": secret,
                             "SOME_API_TOKEN": secret})
    assert result.returncode == 0
    assert secret not in result.stdout + result.stderr


def test_wrapper_never_modifies_dependencies(tmp_path):
    with open(REQUIREMENTS, "rb") as fh:
        before = hashlib.sha256(fh.read()).hexdigest()
    path = _fake_tool(tmp_path, "fake_audit_vuln", VULN_TOOL)
    _run("fake_audit_vuln", pythonpath=path)
    with open(REQUIREMENTS, "rb") as fh:
        assert hashlib.sha256(fh.read()).hexdigest() == before
    # and the wrapper source contains no remediation verbs
    with open(WRAPPER, encoding="utf-8") as fh:
        source = fh.read()
    for forbidden in ("pip install --upgrade", "pip_install", "--fix"):
        assert forbidden not in source, forbidden


def test_audit_tool_not_a_runtime_dependency():
    """pip-audit is environment tooling only: it must not appear in the
    authoritative runtime dependency declaration, and no application module
    may import it."""
    with open(REQUIREMENTS, encoding="utf-8") as fh:
        assert "pip-audit" not in fh.read().lower().replace("_", "-")
    for folder in ("web", "engine"):
        for root, _dirs, files in os.walk(os.path.join(REPO_ROOT, folder)):
            for name in files:
                if name.endswith(".py"):
                    with open(os.path.join(root, name),
                              encoding="utf-8") as fh:
                        assert "pip_audit" not in fh.read(), (root, name)
