"""Phase 7C — Section 13 Requirement Landscape template-only metadata collapse.

Requirement-landscape entries that share the exact same full metadata tuple
(provenance + status + criticality + authority + rationale + resolving action +
supporting references + linked risk) render their shared metadata once, with all
distinct statements listed in full; entries whose metadata differs in any field
render separately. Presentation-only: the section_13_requirement_landscape data
and its requirements list/count are unchanged, no statement is dropped or
truncated, and the criticality authority stays visible (C4-R5).
"""
import os, sys, uuid
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.deliverable_assembler import assemble_deliverable
from engine.idea_state import (
    IdeaState, DISPOSITION_PROVISIONAL_ASSUMPTION, OWNER_INPUT,
    Gap, OPEN, PROBLEM_MECHANISM_FIT,
)
from web.app import app, SESSION_STORE

STMTS = [
    "heart-rate sensing works reliably on cattle in the field",
    "the collar strap stays comfortable over long periods",
    "the onboard battery lasts a full week between charges",
    "wireless alerts reach the farmer's phone reliably across the farm",
    "the sensor stays correctly positioned on a moving animal",
]
_FORBIDDEN = ["validated", "feasible", "certified", "patentable",
              "market-ready", "build-ready", "guaranteed"]


def _state_identical(stmts=STMTS):
    s = IdeaState(idea_id="p7c-" + uuid.uuid4().hex[:8])
    for c in stmts:
        s.record_interaction(DISPOSITION_PROVISIONAL_ASSUMPTION, iteration=0,
                             content=c, responsibility=OWNER_INPUT)
    return s


def _state_mixed():
    # two recorded answers (provenance "Recorded answer"/status "recorded") plus an
    # open-gap requirement (different provenance/status) -> two metadata groups.
    s = IdeaState(idea_id="p7c-mix-" + uuid.uuid4().hex[:8])
    s.record_interaction(DISPOSITION_PROVISIONAL_ASSUMPTION, iteration=0,
                         content="recorded answer alpha", responsibility=OWNER_INPUT)
    s.record_interaction(DISPOSITION_PROVISIONAL_ASSUMPTION, iteration=0,
                         content="recorded answer beta", responsibility=OWNER_INPUT)
    s.gaps.append(Gap(gap_type=PROBLEM_MECHANISM_FIT, status=OPEN, opened_at=0))
    return s


def _render(state):
    sid = "p7c-render-" + uuid.uuid4().hex[:8]
    SESSION_STORE[sid] = {"state": state, "last_result": None, "transcript": []}
    try:
        resp = app.test_client().get(f"/session/{sid}/deliverable")
        return resp.status_code, resp.get_data(as_text=True)
    finally:
        SESSION_STORE.pop(sid, None)


def _section13(body):
    i = body.find("<h3>Requirement Landscape</h3>")
    j = body.find("What is assumed", i)
    return body[i:(j if j > i else len(body))]


# --- identical-metadata entries collapse ------------------------------------

def test_identical_metadata_collapses_to_one_shared_block():
    state = _state_identical()
    rl = assemble_deliverable(state)["section_13_requirement_landscape"]
    # sanity: all five entries share one metadata tuple
    keys = {(r["provenance"], r["status"], r["criticality"], r["criticality_authority"],
             r["criticality_rationale"], r["resolving_action"],
             tuple(r["supporting_references"]), r["has_linked_risk"]) for r in rl["requirements"]}
    assert len(rl["requirements"]) == 5 and len(keys) == 1
    _, body = _render(state)
    sec = _section13(body)
    # metadata rendered once for the group
    assert sec.count("<strong>Provenance:</strong>") == 1
    assert sec.count("<strong>Status:</strong>") == 1
    assert sec.count("<strong>Resolving action:</strong>") == 1
    # a visible count for the collapsed group
    assert "(shared by 5 entries)" in sec


def test_every_statement_present_in_full_untruncated():
    import html
    state = _state_identical()
    _, body = _render(state)
    sec = html.unescape(_section13(body))   # undo Jinja autoescape (e.g. &#39; -> ')
    for stmt in STMTS:
        assert stmt in sec            # exact, full statement — not truncated/paraphrased


def test_criticality_authority_and_metadata_visible():
    _, body = _render(_state_identical())
    sec = _section13(body)
    assert "Criticality:</strong> Not yet determined (assigned automatically by the system; not yet reviewed)" in sec
    assert "<strong>Provenance:</strong>" in sec
    assert "<strong>Status:</strong>" in sec
    assert "<strong>Resolving action:</strong>" in sec


# --- differing metadata is NOT collapsed ------------------------------------

def test_entries_with_differing_metadata_render_separately():
    state = _state_mixed()
    rl = assemble_deliverable(state)["section_13_requirement_landscape"]
    provs = {r["provenance"] for r in rl["requirements"]}
    stats = {r["status"] for r in rl["requirements"]}
    # the fixture genuinely produces >1 metadata group (different provenance/status)
    assert len(provs) > 1 or len(stats) > 1
    _, body = _render(state)
    sec = _section13(body)
    # more than one metadata block -> not collapsed into a single group
    assert sec.count("<strong>Provenance:</strong>") >= 2
    assert "recorded answer alpha" in sec and "recorded answer beta" in sec


# --- data preserved / no forbidden wording ----------------------------------

def test_section13_data_and_requirements_unchanged():
    state = _state_identical()
    rl = assemble_deliverable(state)["section_13_requirement_landscape"]
    assert set(rl) == {"title", "requirements", "total", "count_basis",
                       "count_relationship", "empty_statement",
                       "risks", "has_risks", "risk_disclaimer"}
    assert len(rl["requirements"]) == 5          # collapse is display-only
    for r in rl["requirements"]:
        assert r["criticality"] == "Not yet determined"
        assert r["criticality_authority"] == "assigned automatically by the system; not yet reviewed"


def test_no_forbidden_wording_introduced_by_collapse():
    # scan only the collapsed statement/metadata region, not the pre-existing
    # advisory risk_disclaimer (which legitimately negates "safe/verified").
    _, body = _render(_state_identical())
    sec = _section13(body)
    cut = sec.find("No structurally grounded risks")
    added_region = (sec[:cut] if cut >= 0 else sec).lower()
    for w in _FORBIDDEN:
        assert w not in added_region, f"forbidden wording in Section 13 body: {w!r}"


def test_contract_intact():
    pkg = assemble_deliverable(_state_identical())
    assert len([k for k in pkg if k.startswith("section_")]) == 14
