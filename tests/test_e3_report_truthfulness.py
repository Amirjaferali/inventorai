# -*- coding: utf-8 -*-
"""E-3 — report truthfulness of a CLOSED gap (report Section 4 only).

A CLOSED gap means the inventor's answers met InventorAI's question checks; it
never means the area is resolved or that engineering feasibility is shown. The
report row says so, and when the Requirement Landscape still carries an active
pending specialist / evidence request for that gap's area the row says that too.
The engine's gap status, quality, relevance, routing, maturity and the Section 4
ids / types / counts are unchanged; only the row's display wording changes.
"""
import copy
import html as _html
import re
import uuid

import pytest

import web.app as appmod
from engine import need_routing
from engine.deliverable_assembler import assemble_deliverable
from engine.idea_state import (
    CLOSED, OPEN, PARTIAL, PHYSICAL_FEASIBILITY, MECHANISM_COMPLETENESS,
    BOUNDARY_AMBIGUITY, AssertionRecord, Gap, IdeaState,
    DISPOSITION_SPECIALIST_REQUESTED, DISPOSITION_EVIDENCE_REQUESTED,
)
from engine.requirement_landscape import derive_requirement_landscape
from engine.session_reconstruction import CURRENT_ENGINE_CONTRACT_VERSION
from tests.csrf_client import csrf_client

ELEC = "electronics_electrical"
IDEA = ("I want a device that waters my plants automatically when they need it, "
        "but I don't know how it would know.")
ANSWERS = (
    "Something would check whether the soil in each pot has become dry, and when "
    "it is dry it lets water flow into that pot until it is wet again, then stops.",
    "The main parts are: something that checks if the soil is dry, a water "
    "container, a way to move the water to the pots, and something that decides "
    "when to start and stop.",
    "First the soil dries out during the day. The checking part notices the soil "
    "is dry. It tells the deciding part, which starts the water. When the soil is "
    "wet again the water stops. I would notice because the plants stay healthy.",
    "I am unsure how the checking part can tell that soil is dry, and how the "
    "water would be moved without me pouring it.",
    "I know the plants need water when the soil is dry and that six pots are on "
    "my balcony. I would need someone who knows about soil moisture sensing and "
    "small pumps to help with the rest.",
)
ANSWERED_ROW = ("Physical Feasibility answered under InventorAI's question checks "
                "(not independently verified; engineering feasibility has not been "
                "established)")
SPECIALIST_NOTE = "Your request for specialist input on this area is still pending."
EVIDENCE_NOTE = "Your request for evidence on this area is still pending."


# --------------------------------------------------------------------------
# route helpers
# --------------------------------------------------------------------------
@pytest.fixture
def client():
    return csrf_client(appmod.app)


def _start(c):
    r = c.post("/start", data={"idea": IDEA, "domain_choice": ELEC, "domain_confirm": ELEC})
    assert r.status_code == 302, r.status_code
    return r.headers["Location"].rsplit("/", 1)[-1]


def _token(c, sid):
    raw = c.get(f"/session/{sid}").get_data(as_text=True)
    m = re.search(r'name="answer_token" value="([^"]*)"', raw)
    return _html.unescape(m.group(1))


def _answer(c, sid, text, action="answered"):
    data = {"response": text, "action": action}
    if action == "answered":
        data["answer_token"] = _token(c, sid)
    r = c.post(f"/session/{sid}", data=data)
    assert r.status_code == 302, r.status_code


def _state(sid):
    return appmod.SESSION_STORE[sid]["state"]


def _e3_journey(c, specialist_first=False):
    sid = _start(c)
    for i, text in enumerate(ANSWERS):
        if specialist_first and i == 3:
            _answer(c, sid, "I need a specialist for this part.",
                    action="specialist_requested")
        _answer(c, sid, text)
    if specialist_first:
        _answer(c, sid, ANSWERS[4])
    return sid


def _section4(page):
    m = re.search(r'id="report-needs".*?</ul>', page, re.S)
    assert m, "Section 4 must render"
    return re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", " ", m.group(0))))


def _report(c, sid, lang="en"):
    if lang == "ar":
        assert c.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    return c.get(f"/session/{sid}/deliverable").get_data(as_text=True)


def _gaps(sid):
    return [(g.gap_type, g.status) for g in _state(sid).gaps]


# --------------------------------------------------------------------------
# the E-3 journey
# --------------------------------------------------------------------------
def test_e3_closed_gap_is_no_longer_reported_as_resolved(client):
    sid = _e3_journey(client)
    # the engine's own outcome is exactly what it was before this change
    assert _gaps(sid) == [(MECHANISM_COMPLETENESS, CLOSED), (PHYSICAL_FEASIBILITY, CLOSED),
                          (BOUNDARY_AMBIGUITY, OPEN)]
    assert _state(sid).maturity_level == 1
    s4 = _section4(_report(client, sid))
    assert "REQ-004 — " + ANSWERED_ROW in s4
    assert "resolved" not in s4
    assert "addressed" not in s4
    assert SPECIALIST_NOTE not in s4 and EVIDENCE_NOTE not in s4


def test_e3_section4_identity_and_data_contract_are_unchanged(client):
    sid = _e3_journey(client)
    s4 = assemble_deliverable(_state(sid))["section_4_requirements"]
    assert [r["id"] for r in s4["requirements"]] == ["REQ-001", "REQ-002", "REQ-003", "REQ-004"]
    assert s4["total"] == 4
    closed = s4["requirements"][2:]
    for row in closed:
        assert row["type"] == "constraint"
        assert row["source"] == "gap_resolution"
        assert row["evidence_quality"] == "Reasoned"
        assert row["note"] is None and row["pending_note"] is None
    assert closed[1]["statement"] == "Physical Feasibility answered under InventorAI's question checks"


def test_an_active_specialist_request_is_disclosed_beside_the_closed_gap(client):
    sid = _e3_journey(client, specialist_first=True)
    # the pending request does not block closure (WS12 OD-4, unchanged)
    assert (PHYSICAL_FEASIBILITY, CLOSED) in _gaps(sid)
    kinds = {r.primary_anchor.anchor_kind
             for r in derive_requirement_landscape(_state(sid)).requirements}
    assert "pending_specialist" in kinds          # the landscape still reports it
    s4 = _section4(_report(client, sid))
    assert "REQ-004 — " + ANSWERED_ROW + " " + SPECIALIST_NOTE in s4
    assert s4.count(SPECIALIST_NOTE) == 1          # only on the gap it concerns
    assert "resolved" not in s4


def test_arabic_report_carries_the_same_generated_row(client):
    sid = _e3_journey(client, specialist_first=True)
    s4 = _section4(_report(client, sid, lang="ar"))
    # Section 4 rows are generated content kept in English in both locales,
    # exactly like REQ-001 / REQ-002; the wording is the same and never "resolved".
    assert ANSWERED_ROW in s4 and SPECIALIST_NOTE in s4
    assert "Stated by the inventor (not yet verified)" in s4
    assert "resolved" not in s4


def test_pdf_source_matches_the_html_row(client, monkeypatch):
    sid = _e3_journey(client, specialist_first=True)
    seen = {}
    real = appmod._render_pdf_bytes

    def spy(source):
        seen["source"] = source
        return real(source)
    monkeypatch.setattr(appmod, "_render_pdf_bytes", spy)
    r = client.post(f"/session/{sid}/deliverable.pdf", data={})
    assert r.status_code == 200 and r.data[:5] == b"%PDF-"
    s4 = _section4(seen["source"])
    assert ANSWERED_ROW in s4 and SPECIALIST_NOTE in s4 and "resolved" not in s4


def test_rendering_the_report_changes_no_state(client):
    sid = _e3_journey(client, specialist_first=True)
    before = copy.deepcopy(_state(sid))
    _report(client, sid)
    after = _state(sid)
    assert [(g.gap_type, g.status, g.closed_at) for g in after.gaps] == \
        [(g.gap_type, g.status, g.closed_at) for g in before.gaps]
    assert [(r.record_id, r.disposition, r.superseded_by) for r in after.assertions] == \
        [(r.record_id, r.disposition, r.superseded_by) for r in before.assertions]
    assert after.maturity_level == before.maturity_level


# --------------------------------------------------------------------------
# pending-request disclosure (state level)
# --------------------------------------------------------------------------
def _closed_state(*records, gaps=(PHYSICAL_FEASIBILITY,)):
    s = IdeaState(idea_id="e3-" + uuid.uuid4().hex[:8])
    s.gaps = [Gap(gap_type=g, status=CLOSED, opened_at=1, closed_at=2) for g in gaps]
    s.assertions = list(records)
    return s


def _request(rid, disposition, gap, superseded_by=None):
    return AssertionRecord(record_id=rid, disposition=disposition, content="",
                           gap_context=gap, iteration=1, superseded_by=superseded_by)


def _rows(state):
    return assemble_deliverable(state)["section_4_requirements"]["requirements"]


def test_no_note_without_a_request():
    [row] = _rows(_closed_state())
    assert row["pending_note"] is None
    assert row["resolution_status"] == ("not independently verified; engineering "
                                        "feasibility has not been established")


def test_a_superseded_request_gives_no_note():
    rec = _request("rec_1", DISPOSITION_SPECIALIST_REQUESTED, PHYSICAL_FEASIBILITY,
                   superseded_by="rec_2")
    [row] = _rows(_closed_state(rec))
    assert row["pending_note"] is None


def test_evidence_and_specialist_requests_are_each_disclosed():
    recs = (_request("rec_1", DISPOSITION_EVIDENCE_REQUESTED, PHYSICAL_FEASIBILITY),
            _request("rec_2", DISPOSITION_SPECIALIST_REQUESTED, PHYSICAL_FEASIBILITY))
    [row] = _rows(_closed_state(*recs))
    assert row["pending_note"] == SPECIALIST_NOTE + " " + EVIDENCE_NOTE


def test_a_request_for_another_gap_stays_on_that_gap():
    rec = _request("rec_1", DISPOSITION_SPECIALIST_REQUESTED, MECHANISM_COMPLETENESS)
    rows = _rows(_closed_state(rec, gaps=(MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY)))
    assert [r["pending_note"] for r in rows] == [SPECIALIST_NOTE, None]


def test_an_outstanding_routed_need_is_disclosed_through_the_landscape():
    # An outstanding routed need normally keeps its gap from closing (closure
    # guard); if the two ever coexist, the row still discloses it.
    s = _closed_state()
    for rev in need_routing.creation_revisions(
            "p-e3", "mechanical", "N", CURRENT_ENGINE_CONTRACT_VERSION):
        need_routing.apply_revision(s, rev)
    assert any(rev.gap_type == PHYSICAL_FEASIBILITY for rev in s.need_routing)
    [row] = _rows(s)
    assert row["pending_note"] == SPECIALIST_NOTE


def test_open_and_partial_gaps_still_produce_no_section4_row():
    s = _closed_state()
    s.gaps = [Gap(gap_type=PHYSICAL_FEASIBILITY, status=PARTIAL, opened_at=1),
              Gap(gap_type=BOUNDARY_AMBIGUITY, status=OPEN, opened_at=1)]
    assert _rows(s) == []
