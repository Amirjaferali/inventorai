"""v1.32 derived-navigation truth guards: roadmap + operating checklist.

File: tests/test_v132_derived_navigation_truth.py
Purpose: keep the two DERIVED navigation artifacts —
`docs/governance/INVENTORAI_MASTER_EXECUTION_ROADMAP.md` and
`docs/governance/INVENTORAI_MASTER_ROADMAP_EXECUTION_CHECKLIST.md` — from
regressing into authority, losing their structure, or teaching a successor a
procedure that yields a wrong answer. These are repository doc-invariant
checks in the established convention; no runtime code is involved.
Input contract: run under pytest from the repository root; reads the two
artifacts, plus a repository-wide scan for one withdrawn SHA literal.
Output contract: 45 Stage IDs and 28 tracking IDs survive with no duplicates
and no renumbering; nine groups survive; both artifacts declare themselves
non-authoritative; the scheduler is never described as deployed or activated;
the historical FCORA FAIL and its separate differential clearance both
survive and no FCORA PASS is invented; the live-tip procedure resolves the
fetched authoritative ref rather than trusting local HEAD; no external
engineering provider is named as adopted; and the withdrawn spliced deployed
SHA appears nowhere in the repository.
Prohibited behaviors: MUST NOT weaken to pass; MUST NOT grant either artifact
authority it does not have.
"""
import os
import re

ROADMAP = os.path.join("docs", "governance",
                       "INVENTORAI_MASTER_EXECUTION_ROADMAP.md")
CHECKLIST = os.path.join("docs", "governance",
                         "INVENTORAI_MASTER_ROADMAP_EXECUTION_CHECKLIST.md")

# The withdrawn literal is assembled at runtime so that this guard does not
# itself reintroduce the thing it forbids.
_WITHDRAWN_DEPLOYED_SHA = "06bf3632ae9914732e945" + "5965f551955c5d4a8c1"
_REAL_PR663_MERGE = "06bf3632ae9914732e945f00f5ff9f130aea57a0"


def _read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


# ==========================================================================
# Structure: 9 groups / 45 stages / 28 tracking IDs
# ==========================================================================
def test_roadmap_preserves_nine_groups():
    groups = re.findall(r"^### Group (\d) — Stages", _read(ROADMAP), re.M)
    assert groups == [str(n) for n in range(1, 10)], groups


def test_roadmap_preserves_forty_five_stage_ids():
    ids = [int(x) for x in
           re.findall(r"^- \[[ x]\] \*\*(\d+) —", _read(ROADMAP), re.M)]
    assert len(ids) == 45, len(ids)
    assert sorted(ids) == list(range(1, 46)), sorted(ids)   # no gaps, no dupes


def test_roadmap_preserves_twenty_eight_tracking_ids():
    section = _read(ROADMAP).split("## 9. Current Master Checklist")[1]
    section = section.split("## 10.")[0]
    ids = [int(x) for x in re.findall(r"^\| *(\d+) \|", section, re.M)]
    assert len(ids) == 28, len(ids)
    assert sorted(ids) == list(range(1, 29)), sorted(ids)


# ==========================================================================
# Neither artifact may become authority
# ==========================================================================
def test_checklist_declares_itself_non_authoritative():
    text = _read(CHECKLIST)
    assert "DERIVED OPERATING CHECKLIST — NOT EXECUTION AUTHORITY" in text
    assert "does not replace Git" in text
    assert "does not replace Owner decisions" in text
    # the hierarchy must place this file at the bottom, not the top
    assert "Git / live repository state" in text
    assert "conflicts resolve upward" in re.sub(r"\s+", " ", text).lower()


def test_roadmap_declares_itself_non_authoritative():
    text = _read(ROADMAP)
    assert "DERIVED NAVIGATION — NOT EXECUTION AUTHORITY" in text
    assert "control and this file is the stale one" in \
        re.sub(r"\s+", " ", text).lower()


# ==========================================================================
# Live-tip procedure: resolve the fetched ref, never trust local HEAD
# ==========================================================================
def test_live_tip_procedure_resolves_the_fetched_authoritative_ref():
    """A successful fetch does not move the checkout.

    The earlier procedure ran `git fetch` and then `git rev-parse HEAD`, which
    reports the local checkout and can silently be reported as the live tip.
    The corrected procedure must resolve the remote-tracking ref explicitly and
    compare it against HEAD.
    """
    text = _read(CHECKLIST)
    branch = "feature/atomic-json-session-persistence"
    assert "git fetch origin %s" % branch in text
    assert "git rev-parse refs/remotes/origin/%s" % branch in text
    assert "git rev-parse refs/remotes/origin/%s^{tree}" % branch in text
    assert "git rev-list --left-right --count" in text
    normalized = re.sub(r"\s+", " ", text)
    assert ("The fetched authoritative ref is the current authority" in
            normalized)
    assert "never report a local HEAD as the live tip" in normalized
    assert "A successful fetch does not change your checkout" in normalized


def test_recorded_baseline_is_not_presented_as_a_permanent_pin():
    normalized = re.sub(r"\s+", " ", _read(CHECKLIST))
    assert ("This is evidence of one moment and is expected to go stale. It is "
            "not a permanent pin" in normalized)


# ==========================================================================
# Truth boundaries that must never collapse
# ==========================================================================
def test_scheduler_never_described_as_deployed_or_activated():
    for path in (ROADMAP, CHECKLIST):
        normalized = re.sub(r"\s+", " ", _read(path))
        assert "NOT DEPLOYED" in normalized, path
        assert "NOT LIVE-ACTIVATED" in normalized, path
        for claim in ("scheduler is deployed", "scheduler is live",
                      "scheduler is running", "scheduled backup is running",
                      "backups run daily"):
            assert claim not in normalized.lower(), (path, claim)


def test_fcora_history_and_clearance_both_survive_without_a_pass():
    for path in (ROADMAP, CHECKLIST):
        normalized = re.sub(r"\s+", " ", _read(path))
        assert "C — FCORA FAIL" in normalized, path
        assert "DIFFERENTIAL RECHECK PASS" in normalized, path
        assert "No FCORA PASS exists" in normalized or \
            "no FCORA PASS exists" in normalized, path


def test_no_external_engineering_provider_named_as_adopted():
    text = _read(ROADMAP).lower()
    for vendor in ("ansys", "solidworks", "matlab", "comsol", "altium",
                   "kicad", "autodesk", "siemens nx", "simulink", "abaqus",
                   "ltspice", "fusion 360"):
        assert vendor not in text, vendor


# ==========================================================================
# Deployed-SHA hygiene: the withdrawn literal stays out of the repository
# ==========================================================================
def test_withdrawn_spliced_deployed_sha_absent_from_repository():
    """The spliced SHA exists nowhere in Git and must not be reintroduced.

    It was relayed once as an exact full deployed SHA, having been formed by
    widening an abbreviated provider identity. Repository identity and provider
    identity are separate evidence classes; a literal produced by mixing them
    is not evidence of anything and is not preserved even as a quotation.
    """
    hits = []
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs
                   if d not in (".git", "__pycache__", "node_modules")]
        for name in files:
            path = os.path.join(root, name)
            try:
                with open(path, encoding="utf-8") as fh:
                    if _WITHDRAWN_DEPLOYED_SHA in fh.read():
                        hits.append(path)
            except (UnicodeDecodeError, OSError):
                continue
    assert hits == [], hits


def test_repository_merge_sha_is_labeled_as_repository_evidence():
    state = os.path.join("docs", "governance", "CURRENT_PROJECT_STATE.md")
    normalized = re.sub(r"\s+", " ", _read(state))
    assert "**Repository PR #663 merge SHA:** `%s`" % _REAL_PR663_MERGE in normalized
    assert "Provider exact deployed SHA: NOT VERIFIED IN THIS SESSION" in normalized
    assert "Never infer an exact full provider SHA" in normalized
