"""
Stage 3 evidence capture + FDC-001 deliverable surfacing.

Covers: per-gap accepted-evidence capture in integrate_response(), backward
compatibility of the new optional Gap.evidence field, and Stage 3 surfacing in
the FDC-001 deliverable (human labels, captured evidence, honest missing-evidence
state, no raw enum in rendered output, Stage 2 output unchanged).
"""
import os, sys, uuid, dataclasses
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from engine.idea_state import (
    IdeaState, Gap, Evidence, OPEN, PARTIAL, CLOSED, ASSERTED, REASONED,
    MECHANISM_COMPLETENESS,
    PROBLEM_MECHANISM_FIT, ASSUMPTION_INVENTORY, EXPERTISE_GAP_AWARENESS,
)
from engine.progression_loop import integrate_response
from engine.deliverable_assembler import assemble_deliverable
from web.app import app, SESSION_STORE

# REASONED response: causal structure ("measures", "when ", "causes"), len >= 40.
REASONED_RESP = (
    "The mechanism measures the soil moisture continuously, and when the reading "
    "drops below the set threshold it causes the relay to switch the pump on."
)


def _state(stage3=True):
    s = IdeaState(idea_id="s3-" + uuid.uuid4().hex[:8])
    s.domain = "electronics_electrical"
    s.domain_signal = "electronics_electrical"
    if stage3:
        s.maturity_level = 2
        s.current_stage = 3
    return s


def _add_gap(s, gap_type, status=OPEN):
    g = Gap(gap_type=gap_type, status=status, opened_at=0)
    s.gaps.append(g)
    return g


# --- A. Evidence capture ----------------------------------------------------

def test_1_pmf_reasoned_response_stored_on_pmf_gap():
    s = _state(); _add_gap(s, PROBLEM_MECHANISM_FIT)
    integrate_response(s, PROBLEM_MECHANISM_FIT, "q", REASONED_RESP)
    g = s.get_gap(PROBLEM_MECHANISM_FIT)
    assert len(g.evidence) == 1
    assert g.evidence[0].quality == REASONED
    assert g.evidence[0].content == REASONED_RESP


def test_2_assumption_inventory_response_stored_on_ai_gap():
    s = _state(); _add_gap(s, ASSUMPTION_INVENTORY)
    integrate_response(s, ASSUMPTION_INVENTORY, "q", REASONED_RESP)
    g = s.get_gap(ASSUMPTION_INVENTORY)
    assert len(g.evidence) == 1 and g.evidence[0].content == REASONED_RESP


def test_3_expertise_gap_response_stored_on_ega_gap():
    s = _state(); _add_gap(s, EXPERTISE_GAP_AWARENESS)
    integrate_response(s, EXPERTISE_GAP_AWARENESS, "q", REASONED_RESP)
    g = s.get_gap(EXPERTISE_GAP_AWARENESS)
    assert len(g.evidence) == 1 and g.evidence[0].content == REASONED_RESP


def test_4_evidence_does_not_leak_across_gaps():
    s = _state()
    _add_gap(s, PROBLEM_MECHANISM_FIT)
    _add_gap(s, ASSUMPTION_INVENTORY)
    integrate_response(s, PROBLEM_MECHANISM_FIT, "q", REASONED_RESP)
    assert len(s.get_gap(PROBLEM_MECHANISM_FIT).evidence) == 1
    assert len(s.get_gap(ASSUMPTION_INVENTORY).evidence) == 0


def test_5_asserted_and_empty_not_stored_as_evidence():
    s = _state(); _add_gap(s, PROBLEM_MECHANISM_FIT)
    # weak answer -> ASSERTED -> not accepted evidence
    integrate_response(s, PROBLEM_MECHANISM_FIT, "q", "maybe")
    assert len(s.get_gap(PROBLEM_MECHANISM_FIT).evidence) == 0
    # whitespace-only -> not accepted evidence
    integrate_response(s, PROBLEM_MECHANISM_FIT, "q", "    ")
    assert len(s.get_gap(PROBLEM_MECHANISM_FIT).evidence) == 0


# --- B. Evidence preservation / backward compatibility ----------------------

def test_6_evidence_survives_dataclass_roundtrip():
    s = _state(); _add_gap(s, PROBLEM_MECHANISM_FIT)
    integrate_response(s, PROBLEM_MECHANISM_FIT, "q", REASONED_RESP)
    d = dataclasses.asdict(s)  # models any serialization round-trip
    assert d["gaps"][0]["evidence"][0]["content"] == REASONED_RESP
    # reconstruct (deserialize) into dataclasses
    raw = d["gaps"][0]
    g2 = Gap(
        gap_type=raw["gap_type"], status=raw["status"], opened_at=raw["opened_at"],
        iterations_open=raw["iterations_open"], closed_at=raw["closed_at"],
        evidence=[Evidence(**e) for e in raw["evidence"]],
    )
    assert g2.evidence[0].quality == REASONED


def test_7_gap_without_evidence_field_loads_backward_compatible():
    # Older/archived gap data lacking the new 'evidence' field must still load.
    legacy = {"gap_type": PROBLEM_MECHANISM_FIT, "status": OPEN, "opened_at": 0,
              "iterations_open": 0, "closed_at": None}
    g = Gap(**legacy)            # constructs without 'evidence'
    assert g.evidence == []      # defaults to empty list
    s = _state(); s.gaps.append(g)
    pkg = assemble_deliverable(s)  # must not error on legacy-shaped gap
    assert pkg["section_9_stage3_reasoning"]["stage3_gap_count"] == 1


# --- C. Deliverable surfacing -----------------------------------------------

def test_8_deliverable_uses_all_three_stage3_labels():
    s = _state()
    _add_gap(s, PROBLEM_MECHANISM_FIT, CLOSED)
    _add_gap(s, ASSUMPTION_INVENTORY, PARTIAL)
    _add_gap(s, EXPERTISE_GAP_AWARENESS, OPEN)
    labels = {i["gap_label"] for i in assemble_deliverable(s)["section_9_stage3_reasoning"]["items"]}
    assert "Problem–Mechanism Fit" in labels
    assert "Assumption Inventory" in labels
    assert "Expertise-Gap Awareness" in labels


def test_9_deliverable_surfaces_captured_evidence():
    s = _state(); _add_gap(s, PROBLEM_MECHANISM_FIT)
    integrate_response(s, PROBLEM_MECHANISM_FIT, "q", REASONED_RESP)
    items = assemble_deliverable(s)["section_9_stage3_reasoning"]["items"]
    item = [i for i in items if i["gap_label"] == "Problem–Mechanism Fit"][0]
    assert item["evidence"] and item["evidence"][0]["content"] == REASONED_RESP
    assert item["missing_evidence_statement"] is None


def test_10_deliverable_shows_missing_evidence_when_absent():
    s = _state(); _add_gap(s, EXPERTISE_GAP_AWARENESS, OPEN)
    item = assemble_deliverable(s)["section_9_stage3_reasoning"]["items"][0]
    assert item["evidence"] == []
    assert item["missing_evidence_statement"]
    # honest: makes no validation / feasibility / completeness claim
    low = item["missing_evidence_statement"].lower()
    assert "valid" not in low and "feasib" not in low and "complete" not in low


def test_11_rendered_deliverable_has_no_raw_stage3_enum():
    s = _state()
    _add_gap(s, PROBLEM_MECHANISM_FIT)
    integrate_response(s, PROBLEM_MECHANISM_FIT, "q", REASONED_RESP)
    _add_gap(s, ASSUMPTION_INVENTORY, OPEN)
    _add_gap(s, EXPERTISE_GAP_AWARENESS, OPEN)
    sid = "render-" + uuid.uuid4().hex[:8]
    SESSION_STORE[sid] = {"state": s, "last_result": None, "transcript": []}
    try:
        body = app.test_client().get(f"/session/{sid}/deliverable").get_data(as_text=True)
        for enum in (PROBLEM_MECHANISM_FIT, ASSUMPTION_INVENTORY, EXPERTISE_GAP_AWARENESS):
            assert enum not in body, f"raw enum leaked: {enum}"
        assert "Stage 3 Reasoning" in body
        assert "Problem–Mechanism Fit" in body
        assert REASONED_RESP[:30] in body  # captured evidence is rendered
    finally:
        SESSION_STORE.pop(sid, None)


def test_12_stage2_deliverable_unchanged():
    s = _state(stage3=False)
    _add_gap(s, MECHANISM_COMPLETENESS, CLOSED)  # Stage 2 gap only
    pkg = assemble_deliverable(s)
    assert pkg["section_9_stage3_reasoning"]["items"] == []
    assert pkg["section_9_stage3_reasoning"]["stage3_gap_count"] == 0
    sid = "s2-" + uuid.uuid4().hex[:8]
    SESSION_STORE[sid] = {"state": s, "last_result": None, "transcript": []}
    try:
        body = app.test_client().get(f"/session/{sid}/deliverable").get_data(as_text=True)
        assert "Stage 3 Reasoning" not in body  # section hidden for Stage 2
    finally:
        SESSION_STORE.pop(sid, None)
