"""InventorAI Universal Core Guardrail Smoke runner (P10-UG1).

File-creation contract:
  Path: scripts/run_universal_smoke.py
  Purpose: the ONE canonical entry point for the universal guardrail smoke:
    load the machine-checkable guard inventory
    (`tests/universal_guardrail_manifest.py`), verify every canonical guard
    test is still collectable (inventory integrity), execute the BLOCKING
    guards, execute the NON-BLOCKING observation guards, and print the
    standardized verdict.
  Input contract: no arguments. Environment:
    `INVENTORAI_UG_MANIFEST` — optional filesystem path to an alternate
    manifest module (tooling/test seam ONLY, mirroring the
    `INVENTORAI_AUDIT_TOOL_MODULE` precedent from P10-DEP1; the governed
    smoke always uses the default manifest).
  Output contract: stdout report ending in exactly one of
    `UNIVERSAL GUARDRAIL SMOKE: PASS` / `UNIVERSAL GUARDRAIL SMOKE: BLOCK`.
    Exit codes: 0 = PASS (observations, if any, are listed but do not
    block); 1 = BLOCK (a blocking guard failed/was skipped, or ANY canonical
    test — blocking or observation — is missing/uncollectable); 2 = framework
    error (manifest missing/invalid, pytest unavailable).
  Prohibited behaviors: no network access; no paid provider; no mutation of
    any repository or database state beyond what the canonical tests
    themselves do under the governed conftest DB isolation; NEVER converts a
    blocking failure into an observation; NEVER reports PASS with ambiguous
    success language.

PASS means ONLY: CORE INVARIANTS PRESERVED UNDER THIS SUITE.
It does NOT mean: secure; production ready; legally compliant; PSRR
complete; deployment approved; or bug-free. Deployment, PSRR, release, and
paid activation remain separately governed.
"""
import importlib.util
import os
import re
import subprocess
import sys
import time

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_MANIFEST = os.path.join(REPO, "tests", "universal_guardrail_manifest.py")

PASS_LINE = "UNIVERSAL GUARDRAIL SMOKE: PASS"
BLOCK_LINE = "UNIVERSAL GUARDRAIL SMOKE: BLOCK"
MEANING_LINE = ("PASS means ONLY: CORE INVARIANTS PRESERVED UNDER THIS SUITE. "
                "NOT secure / production ready / legally compliant / "
                "PSRR complete / deployment approved / bug-free.")


def _load_manifest():
    path = os.environ.get("INVENTORAI_UG_MANIFEST", DEFAULT_MANIFEST)
    if not os.path.exists(path):
        print("FRAMEWORK ERROR: guard manifest not found: %s" % path)
        return None
    spec = importlib.util.spec_from_file_location("ug_manifest_runtime", path)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
        guards = list(mod.GUARDS)
    except Exception as exc:
        print("FRAMEWORK ERROR: manifest unloadable: %s" % exc.__class__.__name__)
        return None
    for g in guards:
        if not g.get("guard_id") or not g.get("canonical_tests"):
            print("FRAMEWORK ERROR: malformed guard entry in manifest")
            return None
    return guards


def _pytest(args):
    return subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *args],
        capture_output=True, text=True, cwd=REPO)


def _collectable(nodes):
    r = _pytest(["--collect-only", *nodes])
    return r.returncode == 0, r


def _node_matches(node, canon):
    """True when a pytest-reported node id belongs to a canonical node.
    Compared by file BASENAME + node remainder, because pytest reports node
    ids relative to its rootdir while the manifest may carry a different
    path form (governed manifest entries are repo-relative; the tooling/test
    seam may pass absolute tmp paths). A class canonical node matches any
    member test beneath it."""
    c_path, _, c_rest = canon.partition("::")
    n_path, _, n_rest = node.partition("::")
    if os.path.basename(n_path) != os.path.basename(c_path):
        return False
    return (not c_rest) or n_rest == c_rest or n_rest.startswith(c_rest + "::")


def _attribute(guards, failed_output):
    """Map pytest 'FAILED <nodeid>' lines back to guard ids."""
    failed_nodes = re.findall(r"^(?:FAILED|ERROR) (\S+)", failed_output, re.M)
    hit = {}
    for node in failed_nodes:
        for g in guards:
            for canon in g["canonical_tests"]:
                if _node_matches(node, canon):
                    hit.setdefault(g["guard_id"], []).append(node)
    return hit, failed_nodes


def _summary_counts(output):
    tail = output.strip().splitlines()[-1] if output.strip() else ""
    def count(word):
        m = re.search(r"(\d+) %s" % word, tail)
        return int(m.group(1)) if m else 0
    return {w: count(w) for w in ("passed", "failed", "error", "skipped")}


def main():
    started = time.time()
    guards = _load_manifest()
    if guards is None:
        return 2

    blocking = [g for g in guards if g["blocking"]]
    observation = [g for g in guards if not g["blocking"]]
    all_nodes = [n for g in guards for n in g["canonical_tests"]]
    blocking_nodes = [n for g in blocking for n in g["canonical_tests"]]
    observation_nodes = [n for g in observation for n in g["canonical_tests"]]

    print("InventorAI Universal Core Guardrail Smoke")
    print("guards: %d blocking, %d observation; canonical test nodes: %d"
          % (len(blocking), len(observation), len(all_nodes)))

    # 1) Inventory integrity: EVERY canonical test must still be collectable.
    #    A deleted/renamed/moved guard test is always BLOCK — never a skip.
    ok, r = _collectable(all_nodes)
    if not ok:
        print("INVENTORY INTEGRITY FAILURE — canonical guard test(s) missing/uncollectable:")
        for g in guards:
            g_ok, _ = _collectable(g["canonical_tests"])
            if not g_ok:
                print("  GUARD %s BLOCK — canonical test missing: %s"
                      % (g["guard_id"], ", ".join(g["canonical_tests"])))
                print("    invariant: %s" % g["invariant"])
                print("    owner: %s" % g["owner"])
                print("    remedy: restore the canonical test, or make a governed"
                      " framework change to the guard inventory")
        print(MEANING_LINE)
        print(BLOCK_LINE)
        return 1

    verdict_block = False

    # 2) Blocking guards: any failure, error, or skip among their canonical
    #    tests is a BLOCK (a skip would be a silent self-weakening channel).
    rb = _pytest(blocking_nodes)
    counts = _summary_counts(rb.stdout)
    if rb.returncode != 0 or counts["failed"] or counts["error"] or counts["skipped"]:
        verdict_block = True
        hit, failed_nodes = _attribute(blocking, rb.stdout)
        print("BLOCKING GUARD FAILURE(S):")
        for gid, nodes in sorted(hit.items()):
            g = next(x for x in blocking if x["guard_id"] == gid)
            print("  GUARD %s BLOCK" % gid)
            print("    invariant: %s" % g["invariant"])
            print("    owner: %s" % g["owner"])
            print("    failing test(s): %s" % ", ".join(nodes))
            print("    remedy: correct or redesign the candidate; a change to"
                  " this invariant itself requires separate authorization")
        if counts["skipped"]:
            print("  BLOCK: %d blocking canonical test(s) were SKIPPED — "
                  "skipping a blocking guard is treated as a violation"
                  % counts["skipped"])
        if not hit and rb.returncode != 0 and not counts["failed"]:
            print("  BLOCK: blocking selection did not run cleanly (exit %d)"
                  % rb.returncode)
    else:
        print("blocking guards: %d canonical tests passed" % counts["passed"])

    # 3) Observation guards: failures are reported, never block.
    obs_counts = {"passed": 0}
    if observation_nodes:
        ro = _pytest(observation_nodes)
        obs_counts = _summary_counts(ro.stdout)
        if ro.returncode != 0 or obs_counts["failed"] or obs_counts["error"]:
            hit, _ = _attribute(observation, ro.stdout)
            for gid, nodes in sorted(hit.items()):
                g = next(x for x in observation if x["guard_id"] == gid)
                print("  GUARD %s OBSERVATION (non-blocking) — %s"
                      % (gid, ", ".join(nodes)))
                print("    invariant: %s" % g["invariant"])
                print("    note: proceed to gate-specific review; do not treat"
                      " as PASS-clean")
        else:
            print("observation guards: %d canonical tests passed"
                  % obs_counts["passed"])

    elapsed = time.time() - started
    print("smoke runtime: %.1fs" % elapsed)
    print(MEANING_LINE)
    if verdict_block:
        print(BLOCK_LINE)
        return 1
    print(PASS_LINE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
