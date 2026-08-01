"""G-IRB Implementation-Readiness Baseline — neutral readiness checks.

These tests assert only that the reproducible-baseline *infrastructure* is present
and internally consistent. They are deliberately NEUTRAL:

  * They do NOT launch pytest recursively or run the full suite from inside a test
    (repeatability is demonstrated externally by running verify_baseline.sh twice).
  * They do NOT change or exercise any application/engine/product behavior.
  * They do NOT implement or test R6 / R16. Those remain VERIFIED OPEN RISKS,
    NOT REMEDIATED OR TEST-IMPLEMENTED BY G-IRB, and are reserved for the separately
    authorized G-SC0 increment.

Reading the AI advisory flag below is a neutral environment characterization (it
confirms the deterministic default is unchanged), not a security remediation.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_requirements_present_and_pins_only_proven_deps():
    reqs = _read("requirements.txt")
    lines = [
        ln.strip()
        for ln in reqs.splitlines()
        if ln.strip() and not ln.strip().startswith("#")
    ]
    assert lines, "requirements.txt has no dependency lines"
    # Only the two proven-necessary third-party imports, exactly pinned with '=='.
    assert any(ln.startswith("Flask==") for ln in lines), lines
    assert any(ln.startswith("pytest==") for ln in lines), lines
    assert all("==" in ln for ln in lines), (
        "every dependency must be exactly pinned with '=='"
    )


def test_pytest_config_present_and_governed():
    cfg = _read("pytest.ini")
    assert "[pytest]" in cfg
    assert "testpaths = tests" in cfg, "governed suite must be scoped to tests/"
    assert "xfail_strict = true" in cfg, (
        "unexpected xfail passes must be governed as failures"
    )


def test_verify_runner_present_and_strict():
    script = _read("verify_baseline.sh")
    assert script.startswith("#!/usr/bin/env bash"), "runner needs a bash shebang"
    assert "set -euo pipefail" in script, "runner must use strict shell behavior"
    # The runner must not install into the system/global environment.
    assert "venv" in script, "runner must use an isolated virtual environment"


def test_ai_advisory_default_remains_disabled():
    # Neutral characterization: the deterministic default is unchanged by G-IRB.
    from engine.ai_advisor import AI_ADVISORY_ENABLED

    assert AI_ADVISORY_ENABLED is False


def test_readme_documents_run_and_verify():
    readme = _read("README.md")
    assert "Run and Verify" in readme, "README must document the verification command"
    assert "verify_baseline.sh" in readme
