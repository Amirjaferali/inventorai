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
# PROVIDER-DEPENDENT rows: explicit machine-readable state, by immutable ID,
# read only from the CURRENT-TRUTH region.
#
# DESIGN RESET (v1.32). Earlier versions of this guard tried to infer a row's
# state from its English prose — first by keyword, then by stripping Markdown
# shapes, then with a semantic claim classifier. Each attempt was over-
# engineered and still unsafe: free prose has synonyms, negation scope,
# subjects and conjunctions, and a guard that must understand all of that is
# a guard that will be wrong. The prose is no longer authority for anything.
#
# Each owned row now carries two structured elements and they ARE the row's
# machine truth: one CURRENT STATE marker from a bounded vocabulary, and one
# {…} field block of six YES/NO/N/A fields. Deterministic invariants bind
# marker to fields. The prose after them is explanatory only and is not read
# for state. History lives outside the region and is never read at all.
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

_FIELD_NAMES = ("SELECTED", "PROVISIONED", "IMPLEMENTED", "DEPLOYED",
                "LIVE_ACTIVATED", "COMPLETE")
_FIELD_VALUES = ("YES", "NO", "N/A")

_CURRENT_STATE = re.compile(r"CURRENT STATE: ([A-Z][A-Z /]*[A-Z])\.")
_FIELD_BLOCK = re.compile(r"\{([^{}]*)\}")
_FIELD = re.compile(r"^\s*([A-Z_]+)\s*:\s*(\S+)\s*$")
_GATE = re.compile(r"(INFRA-G1-R1|OD-INFRA-\d|OD-CJ1|P8-I4|OD-J2|OD-DR1|P10-BR1)")

# Deterministic marker → field invariants. Each entry names the values a
# field MAY take under that state; a field not listed is unconstrained.
# COMPLETE is constrained to NO under every state because no completion
# state exists in the vocabulary.
_INVARIANTS = {
    "NOT SELECTED": {
        "SELECTED": ("NO",),
        "PROVISIONED": ("NO", "N/A"),
        "IMPLEMENTED": ("NO", "N/A"),
        "DEPLOYED": ("NO", "N/A"),
        "LIVE_ACTIVATED": ("NO", "N/A"),
        "COMPLETE": ("NO",),
    },
    "SELECTED / NOT PROVISIONED": {
        "SELECTED": ("YES",),
        "PROVISIONED": ("NO",),
        "DEPLOYED": ("NO",),
        "LIVE_ACTIVATED": ("NO",),
        "COMPLETE": ("NO",),
    },
    "PROVISIONED / NOT COMPLETE": {
        "SELECTED": ("YES", "N/A"),
        "PROVISIONED": ("YES",),
        # deployment fields reflect actual evidence, not implication — but a
        # live-activated subject would belong under a later state
        "LIVE_ACTIVATED": ("NO", "N/A"),
        "COMPLETE": ("NO",),
    },
    "IMPLEMENTED / NOT DEPLOYED": {
        "SELECTED": ("YES", "N/A"),
        "IMPLEMENTED": ("YES",),
        "DEPLOYED": ("NO",),
        "LIVE_ACTIVATED": ("NO",),
        "COMPLETE": ("NO",),
    },
    "DEPLOYED / NOT COMPLETE": {
        "SELECTED": ("YES", "N/A"),
        "PROVISIONED": ("YES", "N/A"),
        "IMPLEMENTED": ("YES", "N/A"),
        "DEPLOYED": ("YES",),
        # LIVE_ACTIVATED reflects actual truth independently
        "COMPLETE": ("NO",),
    },
}


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
    """The row's own CURRENT TRUTH cell — where its machine state lives."""
    return _cells(row)[5]


def _row_state(row_id):
    """The row's CURRENT STATE marker — exactly one, or the row fails."""
    states = _CURRENT_STATE.findall(_row_truth(_row(row_id)))
    assert len(states) == 1, (
        "%s needs exactly one CURRENT STATE marker in its current-truth cell, "
        "found %d" % (row_id, len(states)))
    return states[0]


def _row_fields(row_id):
    """The row's {…} field block, parsed strictly.

    Exactly one block; exactly the six known fields, each exactly once; each
    value YES, NO or N/A. Anything else fails here, before any invariant is
    consulted, so a malformed block can never be read as a valid state.
    """
    cell = _row_truth(_row(row_id))
    blocks = _FIELD_BLOCK.findall(cell)
    assert len(blocks) == 1, (
        "%s needs exactly one {…} field block, found %d" % (row_id, len(blocks)))
    fields = {}
    for entry in blocks[0].split(";"):
        match = _FIELD.match(entry)
        assert match, (row_id, "malformed field entry", entry.strip())
        name, value = match.group(1), match.group(2)
        assert name in _FIELD_NAMES, (row_id, "unknown field", name)
        assert name not in fields, (row_id, "duplicate field", name)
        assert value in _FIELD_VALUES, (row_id, name, "invalid value", value)
        fields[name] = value
    missing = [name for name in _FIELD_NAMES if name not in fields]
    assert not missing, (row_id, "missing fields", missing)
    return fields


def test_release_current_truth_region_is_well_formed():
    """Missing, duplicated or malformed region = failure, never a silent pass."""
    assert _release_current_truth().strip()


def test_owned_rows_are_found_by_immutable_id_not_by_label():
    """Relabelling a row must not remove it from this guard's inventory."""
    for row_id in _PROVIDER_ROW_IDS:
        assert _row(row_id).startswith("| %s |" % row_id)


def test_every_owned_row_declares_one_bounded_current_state():
    for row_id in _PROVIDER_ROW_IDS:
        assert _row_state(row_id) in _PD_CURRENT_STATES, row_id


def test_every_owned_row_carries_a_well_formed_field_block():
    for row_id in _PROVIDER_ROW_IDS:
        fields = _row_fields(row_id)
        assert set(fields) == set(_FIELD_NAMES), (row_id, fields)


def test_no_owned_row_can_claim_completion():
    """No completion state exists, and COMPLETE is NO on every owned row."""
    for row_id in _PROVIDER_ROW_IDS:
        state = _row_state(row_id)
        for word in ("COMPLETE", "COMPLETED", "DONE", "FINISHED"):
            assert not re.search(r"(?<!NOT )\b%s\b" % word, state), (row_id, state)
        assert _row_fields(row_id)["COMPLETE"] == "NO", row_id


def test_row_fields_satisfy_their_state_invariants():
    """The deterministic marker → field contract, per state.

    This is the whole guard: a CURRENT STATE marker whose fields say
    something else fails here, and nothing in the explanatory prose can
    rescue or undermine it.
    """
    for row_id in _PROVIDER_ROW_IDS:
        state = _row_state(row_id)
        fields = _row_fields(row_id)
        # an out-of-vocabulary marker (e.g. "COMPLETE") is a failure in its
        # own right, reported as one rather than as a lookup error
        assert state in _INVARIANTS, (row_id, "unknown CURRENT STATE", state)
        for name, allowed in _INVARIANTS[state].items():
            assert fields[name] in allowed, (
                row_id, state, name, fields[name], "allowed:", allowed)


def test_states_beyond_selection_cite_their_gate():
    """Anything past NOT SELECTED must name the decision that authorized it."""
    for row_id in _PROVIDER_ROW_IDS:
        if _row_state(row_id) == "NOT SELECTED":
            continue
        assert _GATE.search(_row(row_id)), row_id


def test_selected_rows_record_selection_in_fields_not_only_prose():
    """A SELECTED field must be YES wherever the marker says selected.

    The structured field is the truth; a provider name in prose is not.
    """
    for row_id in _PROVIDER_ROW_IDS:
        state = _row_state(row_id)
        fields = _row_fields(row_id)
        if state == "NOT SELECTED":
            assert fields["SELECTED"] == "NO", row_id
        elif state in ("SELECTED / NOT PROVISIONED", "IMPLEMENTED / NOT DEPLOYED"):
            assert fields["SELECTED"] in ("YES", "N/A"), row_id


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
