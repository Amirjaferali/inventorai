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

from tests import current_truth_contract as contract

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
# PROVIDER-DEPENDENT rows: a bounded current-state machine, anchored by
# IMMUTABLE row IDs and read only from the CURRENT-TRUTH region.
#
# REPAIRED AGAIN (v1.32 contract hardening). Two earlier designs failed.
# The first scanned whole rows for tokens, so a preserved "NOT COMPLETE"
# anywhere in a row could satisfy a check while the row's live claim said
# otherwise. The second stripped particular Markdown shapes to separate
# history, which only moved the leak to shapes it did not anticipate. Now:
# history lives OUTSIDE an explicitly delimited region and is never read;
# rows are located by their immutable RL- identifier, so relabelling a row's
# status or category cannot make it drop out of validation; and each row's
# state comes from one marker with a bounded vocabulary that contains no
# completion state at all.
# --------------------------------------------------------------------------
_PD_CURRENT_STATES = (
    "NOT SELECTED",
    "SELECTED / NOT PROVISIONED",
    "PROVISIONED / NOT COMPLETE",
    "IMPLEMENTED / NOT DEPLOYED",
    "DEPLOYED / NOT COMPLETE",
)

# The provider-dependent inventory this guard owns, by IMMUTABLE row ID.
# Enumerated on purpose: a row may not escape validation by having its
# dependency label, status text or category text edited.
_PROVIDER_ROW_IDS = (
    "RL-B2", "RL-B3", "RL-B4", "RL-B6",
    "RL-C2", "RL-C3", "RL-C5",
    "RL-E4", "RL-E5", "RL-E7",
    "RL-F1", "RL-F2", "RL-F3", "RL-F4", "RL-F5", "RL-F6",
)

_CURRENT_STATE = re.compile(r"CURRENT STATE: ([A-Z][A-Z /]*[A-Z])\.")
_GATE = re.compile(r"(INFRA-G1-R1|OD-INFRA-\d|OD-CJ1|P8-I4|OD-J2|OD-DR1|P10-BR1)")


def _release_current_truth():
    """The explicit CURRENT-TRUTH:RELEASE-READINESS region."""
    return contract.region(_text(), "RELEASE-READINESS")


def _row(row_id):
    """Locate a row by its IMMUTABLE ID, inside the current-truth region."""
    prefix = "| %s |" % row_id
    matches = [line for line in _release_current_truth().splitlines()
               if line.startswith(prefix)]
    assert len(matches) == 1, (
        "row %s must appear exactly once inside the CURRENT-TRUTH region, "
        "found %d" % (row_id, len(matches)))
    return matches[0]


def _cells(row):
    cells = row.split("|")
    assert len(cells) >= 7, row
    return cells


def _row_truth(row):
    """The row's own CURRENT TRUTH cell — where its live claim lives."""
    return _cells(row)[5]


def _row_state(row_id):
    """The row's CURRENT STATE marker — exactly one, or the row fails."""
    states = _CURRENT_STATE.findall(_row_truth(_row(row_id)))
    assert len(states) == 1, (
        "%s needs exactly one CURRENT STATE marker in its current-truth cell, "
        "found %d" % (row_id, len(states)))
    return states[0]


def _row_prose(row_id):
    """The current-truth cell with the marker removed: the row's live prose."""
    return _CURRENT_STATE.sub("", _row_truth(_row(row_id)))


def test_release_current_truth_region_is_well_formed():
    """Missing, duplicated or malformed region = failure, never a silent pass."""
    assert _release_current_truth().strip()


def test_every_owned_row_declares_one_bounded_current_state():
    for row_id in _PROVIDER_ROW_IDS:
        state = _row_state(row_id)
        assert state in _PD_CURRENT_STATES, (row_id, state)


def test_owned_rows_are_found_by_immutable_id_not_by_label():
    """Relabelling a row must not remove it from this guard's inventory.

    The rows are enumerated by ID above. This test states the contract
    explicitly: every enumerated ID resolves to exactly one row inside the
    region, whatever its status or category column happens to say.
    """
    for row_id in _PROVIDER_ROW_IDS:
        assert _row(row_id).startswith("| %s |" % row_id)


def test_no_owned_row_can_claim_completion():
    """Completion is absent from the vocabulary, and forbidden in prose.

    The prose half is read case-insensitively (see the contradiction section
    below), so "completed" in sentence case fails exactly as "COMPLETED" does.
    """
    for row_id in _PROVIDER_ROW_IDS:
        state = _row_state(row_id)
        for word in ("COMPLETE", "COMPLETED", "DONE", "FINISHED"):
            assert not re.search(r"(?<!NOT )\b%s\b" % word, state), (row_id, state)
        claimed = _claims(_row_prose(row_id), _COMPLETION_CLAIMS + ("done", "finished"))
        assert not claimed, (row_id, claimed)


def test_states_beyond_selection_cite_their_gate():
    """Anything past NOT SELECTED must name the decision that authorized it."""
    for row_id in _PROVIDER_ROW_IDS:
        if _row_state(row_id) == "NOT SELECTED":
            continue
        assert _GATE.search(_row(row_id)), row_id


# --------------------------------------------------------------------------
# Contradiction detection: CASE-INSENSITIVE and negation-aware.
#
# REPAIRED (v1.32 final single-defect pass). The previous scan matched only
# upper-case tokens, so false prose in ordinary sentence case slipped past it
# entirely — "the scheduler is deployed, live and activated" under an
# IMPLEMENTED / NOT DEPLOYED marker, or "current provider work is completed"
# under a non-complete one. Case was never part of the contract; the claim is.
#
# Prose is casefolded once (Unicode-safe) and claims are recognised as bounded
# terms. A claim is NOT a contradiction when it is genuinely negated, so the
# truthful wordings the rows depend on — "not deployed", "not activated",
# "NOT LIVE-ACTIVATED", "not complete" — keep passing. Negation is read from a
# bounded window immediately before the term, which may contain only
# whitespace, markup, punctuation, hyphenation and a short list of connecting
# words; anything else ends the window and the claim counts as asserted.
# The CURRENT STATE marker keeps its exact upper-case vocabulary.
# --------------------------------------------------------------------------
_NEGATOR = re.compile(
    r"\b(?:not|never|no|nor)\b"
    r"(?:[\s*_`()\[\],;:.—–/\"'-]"
    r"|\b(?:yet|longer|still|be|been|being|is|are|it|currently|any)\b)*$")

# Terms that assert deployment/activation, and terms that assert completion.
_DEPLOYMENT_CLAIMS = ("live-activated", "deployed", "activated", "is live",
                      "now live", "goes live", "went live", "in production")
_COMPLETION_CLAIMS = ("completed", "complete")
_PROVISION_CLAIMS = ("provisioned", "provisioning")
_SELECTION_CLAIMS = ("selected",)


def _claims(prose, terms, allow_owner_selected=False):
    """Un-negated occurrences of any term, read case-insensitively.

    Returns the matched terms, so a failure message names what was asserted.
    """
    text = prose.casefold()
    found = []
    for term in terms:
        pattern = r"(?<![\w-])%s\b" % re.escape(term)
        for match in re.finditer(pattern, text):
            before = text[max(0, match.start() - 90):match.start()]
            if _NEGATOR.search(before):
                continue                      # "not deployed" is not a claim
            if allow_owner_selected and before.endswith("owner-"):
                continue                      # a recorded Owner selection
            found.append(term)
    return found


def _negated_phrase(prose, term):
    """True when the prose explicitly states the negated form of `term`."""
    return bool(re.search(r"\bnot\s+%s\b" % re.escape(term), prose.casefold()))


def test_row_prose_never_contradicts_its_state():
    """The state machine's contradiction rules, enforced per state.

    Every check below reads casefolded prose, so capitalisation cannot be used
    to smuggle a false current claim past the guard.
    """
    for row_id in _PROVIDER_ROW_IDS:
        state = _row_state(row_id)
        prose = _row_prose(row_id)
        row = _row(row_id)

        deployed = _claims(prose, _DEPLOYMENT_CLAIMS)
        completed = _claims(prose, _COMPLETION_CLAIMS)
        provisioned = _claims(prose, _PROVISION_CLAIMS)
        selected = _claims(prose, _SELECTION_CLAIMS, allow_owner_selected=True)

        # No provider-dependent row may assert completion, in any state.
        assert not completed, (row_id, state, completed)

        if state == "NOT SELECTED":
            # must not name an adopted provider, approach or decision
            assert "owner-selected" not in prose.casefold(), row_id
            assert not selected, (row_id, selected)
            assert not provisioned, (row_id, provisioned)
            assert not deployed, (row_id, deployed)
            assert "DECISION: SATISFIED" not in prose, row_id
        else:
            # a bare selection is only permissible under a cited gate; every
            # non-NOT-SELECTED state already has to cite one, so this states
            # the dependency rather than adding a second rule
            if selected:
                assert _GATE.search(row), (row_id, selected)

        if state == "SELECTED / NOT PROVISIONED":
            # may name the selection; must not claim it is provisioned or live
            assert _negated_phrase(prose, "provisioned"), row_id
            assert not provisioned, (row_id, provisioned)
            assert not deployed, (row_id, deployed)

        if state == "PROVISIONED / NOT COMPLETE":
            # provisioning evidence required; must not deny provisioning
            assert provisioned, row_id
            assert not _negated_phrase(prose, "provisioned"), row_id
            assert _GATE.search(row), row_id
            assert not deployed, (row_id, deployed)

        if state == "IMPLEMENTED / NOT DEPLOYED":
            assert _negated_phrase(prose, "deployed"), row_id
            assert not deployed, (row_id, deployed)

        if state == "DEPLOYED / NOT COMPLETE":
            assert deployed, row_id
            # must still say what remains: the negated completion, explicitly
            assert _negated_phrase(prose, "complete") or \
                _negated_phrase(prose, "completed"), row_id


def test_owned_row_history_lives_outside_the_region():
    """Superseded row wording is preserved — and never inside current truth."""
    region = _release_current_truth()
    outside = contract.outside(_text(), "RELEASE-READINESS")
    assert "## Superseded row wording" in outside
    assert "SUPERSEDED v1.32" not in region, (
        "a preserved quotation must not sit inside the current-truth region")
    # and the history is genuinely retained, not deleted
    for row_id in ("RL-F1", "RL-F5", "RL-F6", "RL-G3"):
        assert "**%s**" % row_id in outside, row_id


def test_od_infra_4_recorded_as_decided_not_open():
    """A settled selection decision must not be reported as still open."""
    region = re.sub(r"\s+", " ", _release_current_truth())
    assert "OD-INFRA-4 DECISION: SATISFIED AS A SELECTION DECISION" in region
    assert "no dedicated third-party monitoring provider was adopted" in region
    # the remaining operations work must stay visible and separate
    assert "Nobody is notified when something breaks" in region
    # and OD-INFRA-4 must not be described as open anywhere current
    for stale in ("OD-INFRA-4 OPEN", "OD-INFRA-4 stays OPEN",
                  "OD-INFRA-4 remains OPEN"):
        assert stale not in region, stale


def test_adviser_items_not_marked_done():
    for line in _text().splitlines():
        if "DEFERRED — EXTERNAL ADVISER REQUIRED" in line:
            assert not re.search(
                r"\|\s*IMPLEMENTED LOCAL FOUNDATION\s*\+?\s*\|", line), line
    assert "NOT SELECTED" in _text()          # provider truth stated plainly
