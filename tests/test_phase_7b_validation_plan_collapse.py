"""Phase 7B — Section 14 template-only collapse of identical validation checks.

Within each Phase 7A responsibility group, byte-for-byte identical rendered rows
(statement + responsibility + evidence + closure + provenance + confidence) are
displayed once with a visible count; rows that differ in any visible field still
render separately. Presentation-only: the section_14_validation_plan data shape
and steps list are unchanged, confidence stays UNDETERMINED, and the advisory
"proposals, not results" framing is preserved. Sections 6/10/11/13 are unchanged.
"""
import json, os, sys, uuid
import re
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.deliverable_assembler import assemble_deliverable
from engine.idea_state import (
    IdeaState, DISPOSITION_PROVISIONAL_ASSUMPTION,
    OWNER_INPUT, SPECIALIST_INPUT, EMPIRICAL_EVIDENCE,
)
from web.app import app, SESSION_STORE

_GENERIC = "Validate the recorded answer against the available evidence."
_FORBIDDEN = ["validated", "verified", "feasible", "certified", "guaranteed",
              "pass/fail", "criticality", "market-ready", "build-ready"]


def _state(responsibilities):
    s = IdeaState(idea_id="p7b-" + uuid.uuid4().hex[:8])
    for i, resp in enumerate(responsibilities):
        s.record_interaction(DISPOSITION_PROVISIONAL_ASSUMPTION, iteration=0,
                             content=f"answer {i}", responsibility=resp)
    return s


def _render(state):
    sid = "p7b-render-" + uuid.uuid4().hex[:8]
    SESSION_STORE[sid] = {"state": state, "last_result": None, "transcript": []}
    try:
        resp = app.test_client().get(f"/session/{sid}/deliverable")
        return resp.status_code, resp.get_data(as_text=True)
    finally:
        SESSION_STORE.pop(sid, None)


def _section14(body):
    i = body.find("<h3>Validation Plan</h3>")
    j = body.find("back-link", i)
    return body[i:(j if j > i else len(body))]


# --- identical rows collapse with a count -----------------------------------

def test_identical_rows_collapse_to_one_with_count():
    state = _state([OWNER_INPUT] * 5)
    vp = assemble_deliverable(state)["section_14_validation_plan"]
    # sanity: the underlying data really is 5 identical steps
    assert len(vp["steps"]) == 5
    assert len({(st["statement"], st["responsibility_label"], st["evidence_category"],
                 st["closure_condition"], st["provenance"], st["confidence_label"])
                for st in vp["steps"]}) == 1
    _, body = _render(state)
    sec = _section14(body)
    # rendered once
    assert sec.count(_GENERIC) == 1
    # visible count equal to the number of underlying identical steps
    assert "(applies to 5 recorded answers)" in sec


def test_count_matches_number_of_identical_steps():
    for n in (2, 3, 7):
        state = _state([OWNER_INPUT] * n)
        _, body = _render(state)
        sec = _section14(body)
        assert sec.count(_GENERIC) == 1
        assert f"(applies to {n} recorded answers)" in sec


# --- distinct rows are NOT collapsed ----------------------------------------

def test_rows_with_different_metadata_not_collapsed():
    # different responsibilities -> different rendered rows in different groups
    state = _state([SPECIALIST_INPUT, EMPIRICAL_EVIDENCE])
    _, body = _render(state)
    sec = _section14(body)
    assert "Specialist input required" in sec
    assert "Empirical evidence required" in sec
    # two distinct rows -> the generic statement appears once per distinct row
    assert sec.count(_GENERIC) == 2
    # singletons carry no count annotation
    assert "(applies to" not in sec


# --- preserved framing / metadata / data ------------------------------------

def test_group_headers_and_intro_preserved():
    # Provisional-assumption answers classify as "Responsibility undetermined",
    # which lands in the Phase 7A catch-all group "Other suggested checks".
    _, body = _render(_state([OWNER_INPUT] * 3))
    sec = _section14(body)
    assert "these are proposals, not results" in sec
    assert '<h4 class="vp-group">Other suggested checks</h4>' in sec


def test_metadata_and_confidence_visible():
    _, body = _render(_state([OWNER_INPUT] * 3))
    sec = _section14(body)
    for k in ("Responsibility:", "Evidence needed:", "Closure:", "Provenance:", "Confidence:"):
        assert k in sec
    assert "Confidence undetermined" in sec


def test_underlying_data_shape_and_steps_unchanged():
    state = _state([OWNER_INPUT] * 5)
    vp = assemble_deliverable(state)["section_14_validation_plan"]
    # data shape unchanged (no fields added by this template-only change)
    assert set(vp) == {"title", "outcome", "steps", "blocked_items", "empty_statement"}
    # steps list still holds every underlying step (collapse is display-only)
    assert len(vp["steps"]) == 5


def test_no_forbidden_wording_introduced():
    _, body = _render(_state([OWNER_INPUT] * 5))
    sec = _section14(body).lower()
    for w in _FORBIDDEN:
        assert w not in sec, f"forbidden wording in Section 14: {w!r}"


def test_no_raw_step_id_exposed():
    _, body = _render(_state([OWNER_INPUT] * 5))
    sec = _section14(body)
    assert "vstep:" not in sec


# --- other sections unchanged -----------------------------------------------

def test_sections_6_10_11_13_and_contract_unchanged():
    pkg = assemble_deliverable(_state([OWNER_INPUT] * 3))
    assert len([k for k in pkg if k.startswith("section_")]) == 14
    assert "section_6_risks" in pkg
    assert "section_10_recommended_next_steps" in pkg
    assert "section_11_prototype_test_plan" in pkg
    for r in pkg["section_13_requirement_landscape"]["requirements"]:
        assert r["criticality"] == "UNDETERMINED"
        assert r["criticality_authority"] == "system-derived"
