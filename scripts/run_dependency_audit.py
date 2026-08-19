"""P10-DEP1 — provider-neutral local dependency-audit wrapper.

File path: ``scripts/run_dependency_audit.py``
Purpose:   the smallest local, provider-neutral wrapper for auditing the
           repository's single authoritative dependency input
           (``requirements.txt``) against current public vulnerability
           advisories via ``pip-audit`` (OSV / PyPI advisory sources).
           Prints a deterministic evidence header (repository SHA,
           dependency-input SHA-256, UTC timestamp, tool identity), then runs
           the audit and preserves the tool's exit status verbatim.

Input contract:
  * no arguments required; any extra CLI arguments are forwarded to the tool
    (e.g. ``-f json``);
  * ``INVENTORAI_AUDIT_TOOL_MODULE`` (tooling/test seam only; default
    ``pip_audit``) selects the module invoked with ``python -m`` — it exists
    so the wrapper's failure semantics are testable offline and is never
    consulted by application runtime code.

Output contract / exit codes:
  * 2 before tool invocation — authoritative ``requirements.txt`` missing;
  * 3 before tool invocation — audit tool missing (clear ``TOOL MISSING``
    message; installing pip-audit is an ENVIRONMENT/TOOLING step, never a
    runtime dependency);
  * otherwise the AUDIT TOOL'S OWN exit code, verbatim: 0 = zero known
    findings AT EXECUTION TIME (printed with an explicit POINT-IN-TIME
    label — advisory databases change, so a clean run is never a permanent
    or production-readiness claim); non-zero (findings, advisory-network
    failure, tool error) is NEVER converted into success.

Prohibited behaviors (binding, per the P10-DEP1 authorization):
  * NO automatic remediation of any kind — no upgrades, no pin changes, no
    package replacement (findings are evidence for a separate governed gate);
  * NO hosted/vendor scanning service, NO CI enforcement claim, NO
    continuous-scanning claim;
  * NO echo of environment variables or secrets;
  * NO coupling to application runtime (nothing under ``web/`` or ``engine/``
    may import this script or the audit tool).
"""
import hashlib
import os
import subprocess
import sys
from datetime import datetime, timezone

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REQUIREMENTS = os.path.join(REPO_ROOT, "requirements.txt")


def _repo_sha():
    try:
        out = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO_ROOT,
                             capture_output=True, text=True, timeout=30)
        return out.stdout.strip() or "unknown"
    except Exception:
        return "unknown"


def main(argv):
    if not os.path.isfile(REQUIREMENTS):
        print("ERROR: authoritative dependency input not found: %s"
              % REQUIREMENTS, file=sys.stderr)
        return 2

    with open(REQUIREMENTS, "rb") as fh:
        req_hash = hashlib.sha256(fh.read()).hexdigest()
    tool_module = os.environ.get("INVENTORAI_AUDIT_TOOL_MODULE", "pip_audit")

    print("P10-DEP1 local dependency audit (POINT-IN-TIME; advisory data "
          "changes over time — a clean run is never a permanent result)")
    print("repository sha:      %s" % _repo_sha())
    print("dependency input:    %s" % REQUIREMENTS)
    print("dependency sha256:   %s" % req_hash)
    print("utc timestamp:       %s"
          % datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    print("audit tool module:   %s (via %s -m)" % (tool_module, sys.executable))

    probe = subprocess.run(
        [sys.executable, "-c", "import importlib,sys; "
         "importlib.import_module(sys.argv[1])", tool_module],
        capture_output=True, text=True)
    if probe.returncode != 0:
        print("TOOL MISSING: audit module %r is not installed in this "
              "environment. Install it as TOOLING ONLY (e.g. "
              "'python -m pip install pip-audit') - it is never a runtime "
              "dependency of the application." % tool_module, file=sys.stderr)
        return 3

    command = [sys.executable, "-m", tool_module, "-r", REQUIREMENTS] + argv
    print("command:             %s" % " ".join(command))
    sys.stdout.flush()
    result = subprocess.run(command, cwd=REPO_ROOT)
    if result.returncode == 0:
        print("POINT-IN-TIME AUDIT: ZERO KNOWN FINDINGS AT EXECUTION TIME "
              "(not a permanent or production-readiness claim; formal "
              "dependency review remains PSRR-time).")
    else:
        print("AUDIT DID NOT PASS CLEANLY (exit %d): findings or errors "
              "above are preserved verbatim and are NEVER converted into a "
              "clean result. Remediation requires a separate governed gate."
              % result.returncode, file=sys.stderr)
    return result.returncode


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
