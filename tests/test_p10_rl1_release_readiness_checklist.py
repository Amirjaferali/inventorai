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


def test_psrr_states_distinct_and_current():
    """The four PSRR states stay distinct, and the CURRENT one is stated.

    REPAIRED (v1.32). This guard previously pinned `PSRR TRIGGERED: NO`. That
    was true before OD-FR1 and before the application-layer tranche was
    authorized and executed; afterwards the pin forced the truth surface to
    keep asserting something false, and collapsed the three genuinely separate
    facts — trigger condition, execution progress, and GO — into one flag. It
    now requires each to be stated separately and truthfully, and confines the
    old pin to superseded context (see the test below).
    """
    text = _norm()
    for state in ("PSRR REGISTERED", "PSRR TRIGGERED", "PSRR EXECUTED",
                  "PSRR GO/NO-GO"):
        assert state in text, state
    # trigger condition: met — an event that happened, not an authorization
    assert "PSRR TRIGGER CONDITION: MET (OD-FR1)" in text
    # execution: begun but bounded — never stated as complete
    assert "PSRR EXECUTION: BEGUN — APPLICATION-LAYER TRANCHE ONLY" in text
    assert "PSRR REMAINING:" in text
    # completion and GO remain separate, and neither is established
    assert "PSRR NOT COMPLETE" in text
    assert "PSRR GO ELIGIBLE: NOT ESTABLISHED" in text
    assert "PSRR = GO: NOT ESTABLISHED — no GO and no NO-GO exists" in text
    # and the checklist still owns no part of the gate
    assert "this checklist does not trigger it" in text


def test_old_psrr_untriggered_pin_only_survives_as_labeled_history():
    """`PSRR TRIGGERED: NO` may no longer be stated as present truth."""
    text = _norm()
    for match in re.finditer(r"PSRR TRIGGERED: NO", text):
        window = text[max(0, match.start() - 400):match.start()]
        assert "SUPERSEDED" in window, (
            "this pin may appear ONLY inside preserved superseded text: %s"
            % text[max(0, match.start() - 200):match.end() + 80])


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


# --------------------------------------------------------------------------
# PROVIDER-DEPENDENT rows: current state is read from the row's own marker.
#
# REPAIRED (v1.32). The earlier guard scanned the whole row for tokens. Once
# rows began carrying preserved historical quotations, a "NOT COMPLETE" or a
# "NOT PROVISIONED" surviving anywhere in the row could satisfy a check while
# the row's live claim said something else entirely — history standing in for
# current truth. Each provider-dependent row now opens its current-truth cell
# with exactly one `CURRENT STATE:` marker drawn from a bounded vocabulary.
# The state is parsed from that marker alone. No completion state exists in
# the vocabulary, so completion cannot be claimed at all on such a row.
# --------------------------------------------------------------------------
_PD_CURRENT_STATES = (
    "NOT SELECTED",
    "SELECTED / NOT PROVISIONED",
    "PROVISIONED / NOT COMPLETE",
    "IMPLEMENTED / NOT DEPLOYED",
    "DEPLOYED / NOT COMPLETE",
)

_CURRENT_STATE = re.compile(r"CURRENT STATE: ([A-Z][A-Z /]*[A-Z])\.")
# a preserved quotation of prior wording: **SUPERSEDED …** (was: "…").
_SUPERSEDED_SPAN = re.compile(
    r"\*\*SUPERSEDED[^*]*\*\*\s*\(was:.*?\)\.", re.S)


def _cells(row):
    """`| ID | Item | Status | Source | Current truth | …` → cell list."""
    cells = row.split("|")
    assert len(cells) >= 7, row
    return cells


def _provider_rows():
    """Rows whose STATUS column carries the provider dependency.

    Read from the status cell, not the whole line: RL-B9 mentions
    PROVIDER-DEPENDENT in its Blocks column as a downstream note, and is not
    itself a provider row.
    """
    rows = [line for line in _text().splitlines()
            if line.startswith("| RL-")
            and "PROVIDER-DEPENDENT" in _cells(line)[3]]
    assert len(rows) >= 10, "expected the provider-dependent inventory"
    return rows


def _row_truth(row):
    """The row's own CURRENT TRUTH cell — where its live claim lives."""
    return _cells(row)[5]


def _row_state(row):
    """The row's CURRENT STATE marker — exactly one, or the row fails."""
    states = _CURRENT_STATE.findall(_row_truth(row))
    assert len(states) == 1, (
        "every PROVIDER-DEPENDENT row needs exactly one CURRENT STATE marker "
        "in its current-truth cell, found %d: %s" % (len(states), row))
    return states[0]


def _row_prose(row):
    """The current-truth cell minus its marker and its preserved quotations.

    What remains is the row's own live prose, which is what the wording rules
    below are allowed to see. History is excluded on purpose: a quotation of a
    prior claim must never satisfy — or violate — a check about today.
    """
    return _CURRENT_STATE.sub("", _SUPERSEDED_SPAN.sub("", _row_truth(row)))


def test_every_provider_row_declares_one_bounded_current_state():
    for row in _provider_rows():
        state = _row_state(row)
        assert state in _PD_CURRENT_STATES, (state, row)


def test_no_provider_row_can_claim_completion():
    """Completion is absent from the state vocabulary, and forbidden in prose.

    This is the check that makes a false "COMPLETE"/"COMPLETED" fail even when
    a correct "NOT COMPLETE" survives elsewhere in the same row.
    """
    for row in _provider_rows():
        state = _row_state(row)
        for word in ("COMPLETE", "COMPLETED", "DONE", "FINISHED"):
            assert not re.search(r"(?<!NOT )\b%s\b" % word, state), (state, row)
        assert not re.search(r"(?<!NOT )\bCOMPLETED?\b", _row_prose(row)), row


def test_provider_row_states_beyond_selection_cite_their_gate():
    """A row may only claim provisioning/implementation/deployment under a gate.

    Dependency labels cannot neutralize this: the state comes from the marker,
    and anything past NOT SELECTED must name the decision that authorized it.
    """
    for row in _provider_rows():
        state = _row_state(row)
        if state == "NOT SELECTED":
            continue
        assert re.search(r"(INFRA-G1-R1|OD-INFRA-\d|OD-CJ1|P8-I4)", row), row


def test_provider_row_prose_matches_its_declared_state():
    """The live prose may not contradict the marker.

    Selection, provisioning and completion stay separate: a row declaring
    SELECTED / NOT PROVISIONED may not also assert provisioning as fact, and a
    row declaring NOT SELECTED may not name a provider as chosen.
    """
    for row in _provider_rows():
        state = _row_state(row)
        prose = _row_prose(row)
        bare_selected = re.search(r"(?<!NOT )(?<!Owner-)\bSELECTED\b", prose)
        provisioned = re.search(r"(?<!NOT )\bPROVISIONED\b", prose)
        configured = re.search(r"(?<!NOT )\bCONFIGURED\b", prose)
        assert not bare_selected, row
        if state == "NOT SELECTED":
            assert "Owner-SELECTED" not in prose, row
            assert not provisioned, row
            assert not configured, row
        if state == "SELECTED / NOT PROVISIONED":
            assert "NOT PROVISIONED" in prose, row
            assert not provisioned, row
        if "Owner-SELECTED" in prose:
            assert re.search(r"(INFRA-G1-R1|OD-INFRA-\d)", row), row


def test_current_state_marker_never_lives_inside_preserved_history():
    """Stripping the historical quotations must leave the marker standing."""
    for row in _provider_rows():
        assert "CURRENT STATE:" in _SUPERSEDED_SPAN.sub("", _row_truth(row)), row


def test_adviser_items_not_marked_done():
    for line in _text().splitlines():
        if "DEFERRED — EXTERNAL ADVISER REQUIRED" in line:
            assert not re.search(
                r"\|\s*IMPLEMENTED LOCAL FOUNDATION\s*\+?\s*\|", line), line
    assert "NOT SELECTED" in _text()          # provider truth stated plainly
