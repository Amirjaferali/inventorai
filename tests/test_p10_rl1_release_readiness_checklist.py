"""P10-RL1 — Release-Readiness Checklist: structural invariants.

File: tests/test_p10_rl1_release_readiness_checklist.py
Purpose: keep `docs/governance/PHASE_10_RELEASE_READINESS_CHECKLIST.md` — the
readiness TRUTH SURFACE — from silently regressing into an approval artifact
or an overclaiming one. Governance doc-invariant tests in the established
repository convention (P10-RL1 changes no runtime code).
Output contract: the canonical artifact exists exactly once; the status
vocabulary is bounded and defined; every checklist row carries source
traceability; the load-bearing distinctions stay visible (foundations ≠
production readiness; PSRR registered/triggered/executed/GO distinct;
deployment distinct; paid activation blocked; adviser/provider/commercial
items never marked implemented/selected; SEC2 residual gaps and the DEP1
point-in-time + test-only-dependency nuances preserved).
Prohibited: weakening to pass; fabricating readiness.
"""
import glob
import os
import re

CHECKLIST = os.path.join("docs", "governance",
                         "PHASE_10_RELEASE_READINESS_CHECKLIST.md")

STATUSES = ("IMPLEMENTED LOCAL FOUNDATION", "OPEN",
            "DEFERRED — EXTERNAL ADVISER REQUIRED", "PROVIDER-DEPENDENT",
            "COMMERCIAL DECISION REQUIRED", "PSRR-TIME", "DEPLOYMENT-TIME",
            "BLOCKED")


def _text():
    with open(CHECKLIST, encoding="utf-8") as fh:
        return fh.read()


def _norm():
    return re.sub(r"\s+", " ", _text())


def test_canonical_checklist_exists_exactly_once():
    assert os.path.isfile(CHECKLIST)
    rivals = [p for p in glob.glob(os.path.join("docs", "**", "*.md"),
                                   recursive=True)
              if re.search(r"(RELEASE|LAUNCH|GO_?LIVE).*CHECKLIST",
                           os.path.basename(p), re.I)]
    assert rivals == [CHECKLIST.replace(os.sep, "/")] or rivals == [CHECKLIST]


def test_not_an_approval_gate():
    text = _norm()
    assert "RELEASE READINESS CHECKLIST FOUNDATION ≠ RELEASE APPROVAL" in text
    assert ("PSRR GO/NO-GO remains a separate future gate before first "
            "public production deployment." in text)
    assert "owns no decision" in text            # truth index, not policy owner


def test_status_vocabulary_defined_and_bounded():
    text = _text()
    for status in STATUSES:
        assert status in text, status
    for vague in ("mostly ready", "nearly complete", "almost done",
                  "low risk", "probably ready"):
        assert vague not in text.lower(), vague


def test_every_checklist_row_has_source_traceability():
    """Every table row (RL-* item) must cite at least one repository path or
    a registered governance identifier in its source column."""
    rows = [l for l in _text().splitlines() if re.match(r"\| RL-[A-G]\d", l)]
    assert len(rows) >= 40, "expected the full obligation inventory"
    for row in rows:
        assert re.search(
            r"(docs/|web/|engine/|scripts/|tests/|P10-|P8-|P5-|P7-|OD-|PSRR|"
            r"D-P8-PL-01|D-PSRR-01|LQ-|TQ-)", row), row


def test_psrr_states_distinct_and_untriggered():
    text = _norm()
    for state in ("PSRR REGISTERED", "PSRR TRIGGERED", "PSRR EXECUTED",
                  "PSRR GO/NO-GO"):
        assert state in text, state
    assert "PSRR TRIGGERED: NO" in text
    assert "this checklist does not trigger it" in text
    assert "PSRR = GO" in text


def test_deployment_and_paid_activation_remain_blocked():
    text = _norm()
    assert "DEPLOYMENT AUTHORIZED: NO" in text
    assert "PAID ACTIVATION AUTHORIZED: NO" in text
    # Narrow pin update (Phase-10 formal closure gate): the original
    # "PHASE 10 CLOSURE ELIGIBLE NOW: NO" pin was factually superseded by the
    # Owner-accepted P10-CL0 eligibility determination and the OD-P10-CL0-STRUCTURE
    # Option-2 decision (PR #538). The protective purpose is preserved by pinning
    # the closure-truth line that still forbids reading closure as approval.
    assert "PHASE-10 CLOSURE ≠ RELEASE APPROVAL" in text


def test_foundations_never_imply_production_readiness():
    text = _norm()
    assert ("does NOT imply production readiness" in text)
    assert "local ≠ production backup readiness" in text
    for forbidden in ("release ready", "production ready", "launch ready",
                      "all security complete", "all legal complete",
                      "PSRR complete", "privacy compliant", "GDPR compliant",
                      "tax compliant", "dependencies secure",
                      "all vulnerabilities resolved", "monitoring active"):
        assert forbidden.lower() not in text.lower(), forbidden


def test_sec2_residual_gaps_visible():
    text = _norm()
    assert "transport-bounded ONLY" in text
    assert 'NOT "all inputs fully hardened"' in text


def test_dep1_point_in_time_and_test_only_dependency_visible():
    text = _norm()
    assert "POINT-IN-TIME ONLY" in text
    assert "NO continuous scanning" in text
    assert "NO auto-remediation" in text
    assert "tests/requirements-draft-l2.txt" in text
    assert "NOT covered by that audit run" in text


def test_adviser_and_provider_items_not_marked_done():
    """No row carrying an adviser/provider dependency may simultaneously be
    marked as a completed implementation or selection."""
    for line in _text().splitlines():
        if "DEFERRED — EXTERNAL ADVISER REQUIRED" in line:
            assert not re.search(
                r"\|\s*IMPLEMENTED LOCAL FOUNDATION\s*\+?\s*\|", line), line
        if "PROVIDER-DEPENDENT" in line and "| RL-" in line:
            # A provider-dependent row may state EITHER "NOT SELECTED" or an
            # Owner selection recorded under a governing gate ("Owner-SELECTED"
            # + an INFRA-/OD- citation). Any other bare "SELECTED", any
            # completion claim, and any un-negated provisioning claim remain
            # forbidden — selection is never provisioning or completion.
            for match in re.finditer(r"(?<!NOT )(?<!Owner-)\bSELECTED\b", line):
                raise AssertionError(line)
            if "Owner-SELECTED" in line:
                assert re.search(r"(INFRA-G1-R1|OD-INFRA-\d)", line), line
                assert "NOT PROVISIONED" in line, line
            assert "COMPLETE" not in line, line
            assert not re.search(r"(?<!NOT )\bPROVISIONED\b", line), line
            assert not re.search(r"(?<!NOT )\bCONFIGURED\b", line), line
    assert "NOT SELECTED" in _text()          # provider truth stated plainly
