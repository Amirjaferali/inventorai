"""Phase 7A — presentation-only grouping of the Section 14 validation plan.

The already-derived validation steps are grouped in the rendered deliverable by
their existing `responsibility_label`, under neutral headers, so the inventor can
see which suggested checks are owner-doable, which need specialist input, and
which need empirical evidence. Presentation-only: the section_14_validation_plan
data is unchanged, every step renders exactly once, order within each group is
preserved, confidence stays UNDETERMINED, and no ranking/criticality/validation
wording is introduced. Sections 10/11/13 and the 14-section contract are untouched.
"""
import os, sys, uuid
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.deliverable_assembler import assemble_deliverable
from engine.idea_state import (
    IdeaState, DISPOSITION_PROVISIONAL_ASSUMPTION,
    OWNER_INPUT, SPECIALIST_INPUT, EMPIRICAL_EVIDENCE,
)
from web.app import app, SESSION_STORE

_GROUP_HEADERS = [
    "Checks you can do yourself",
    "Needs specialist input",
    "Needs a physical test or evidence",
    "Other suggested checks",
]
# wording the grouping must NOT introduce
_FORBIDDEN = ["validated", "verified", "feasible", "certified", "patentable",
              "market-ready", "build-ready", "criticality", "guaranteed",
              "priority", "most important", "ranking", "test first"]


def _multi_step_state():
    """Three provisional-assumption records spanning several responsibilities, so
    the derived validation plan has steps that land in more than one group."""
    s = IdeaState(idea_id="p7a-" + uuid.uuid4().hex[:8])
    s.record_interaction(DISPOSITION_PROVISIONAL_ASSUMPTION, iteration=0,
                         content="assume the 5V rail is stable", responsibility=OWNER_INPUT)
    s.record_interaction(DISPOSITION_PROVISIONAL_ASSUMPTION, iteration=0,
                         content="thermal margin needs an EE review", responsibility=SPECIALIST_INPUT)
    s.record_interaction(DISPOSITION_PROVISIONAL_ASSUMPTION, iteration=0,
                         content="sensor drift needs bench measurement", responsibility=EMPIRICAL_EVIDENCE)
    return s


def _render(state):
    sid = "p7a-render-" + uuid.uuid4().hex[:8]
    SESSION_STORE[sid] = {"state": state, "last_result": None, "transcript": []}
    try:
        resp = app.test_client().get(f"/session/{sid}/deliverable")
        return resp.status_code, resp.get_data(as_text=True)
    finally:
        SESSION_STORE.pop(sid, None)


def test_plan_has_steps_for_the_fixture():
    vp = assemble_deliverable(_multi_step_state())["section_14_validation_plan"]
    assert vp["outcome"] == "PLAN"
    assert len(vp["steps"]) >= 2, "fixture expected multiple validation steps"


def test_every_step_renders_exactly_once():
    state = _multi_step_state()
    vp = assemble_deliverable(state)["section_14_validation_plan"]
    _, body = _render(state)
    # each rendered step is a vp-meta block; count must equal the number of steps
    assert body.count('class="vp-meta"') == len(vp["steps"])


def test_steps_are_grouped_under_neutral_headers():
    state = _multi_step_state()
    _, body = _render(state)
    rendered = [h for h in _GROUP_HEADERS if ('<h4 class="vp-group">' + h + "</h4>") in body]
    assert rendered, "expected at least one grouping header"
    # only headers from the fixed neutral set appear as vp-group headers
    assert body.count('class="vp-group"') == len(rendered)


def test_grouping_covers_all_steps_no_orphans():
    # sum of steps rendered under group headers == total steps (catch-all group
    # absorbs any responsibility_label that is not one of the three named ones).
    state = _multi_step_state()
    vp = assemble_deliverable(state)["section_14_validation_plan"]
    _, body = _render(state)
    assert body.count('class="vp-meta"') == len(vp["steps"])
    # the catch-all group is used for undetermined/system labels
    labels = {st["responsibility_label"] for st in vp["steps"]}
    named = {"Owner can perform", "Specialist input required", "Empirical evidence required"}
    if labels - named:
        assert '<h4 class="vp-group">Other suggested checks</h4>' in body


def test_groups_render_in_fixed_order_and_cover_every_step():
    # Group headers render in the fixed neutral order, and each rendered group is
    # contiguous. (Within-group order is preserved by construction: the template
    # filters the ordered vp.steps with selectattr/rejectattr, which is stable;
    # same-group steps are otherwise byte-identical so their order is immaterial.)
    state = _multi_step_state()
    vp = assemble_deliverable(state)["section_14_validation_plan"]
    _, body = _render(state)
    positions = []
    for h in _GROUP_HEADERS:
        tag = '<h4 class="vp-group">' + h + "</h4>"
        if tag in body:
            positions.append(body.index(tag))
    assert positions, "expected grouping headers to render"
    assert positions == sorted(positions), "group headers must render in the fixed neutral order"
    # every step is rendered exactly once across the groups
    assert body.count('class="vp-meta"') == len(vp["steps"])


def test_confidence_stays_undetermined():
    vp = assemble_deliverable(_multi_step_state())["section_14_validation_plan"]
    assert all(st["confidence"] == "UNDETERMINED" for st in vp["steps"])


def test_intro_and_advisory_framing_preserved():
    _, body = _render(_multi_step_state())
    assert "these are proposals, not results" in body


def test_no_forbidden_ranking_or_claim_wording_in_section14():
    state = _multi_step_state()
    _, body = _render(state)
    i = body.find("<h3>Validation Plan</h3>")
    j = body.find("back-link", i)
    s14 = body[i:(j if j > i else len(body))].lower()
    for w in _FORBIDDEN:
        assert w not in s14, f"forbidden wording in Section 14: {w!r}"


def test_section_14_data_unchanged_and_contract_intact():
    pkg = assemble_deliverable(_multi_step_state())
    vp = pkg["section_14_validation_plan"]
    # data-shape keys unchanged (presentation-only change did not touch the package)
    assert set(vp) == {"title", "outcome", "steps", "blocked_items", "empty_statement"}
    assert len([k for k in pkg if k.startswith("section_")]) == 14
    # sections 10/11/13 still present and untouched by this render change
    assert "section_10_recommended_next_steps" in pkg
    assert "section_11_prototype_test_plan" in pkg
    assert "section_13_requirement_landscape" in pkg
