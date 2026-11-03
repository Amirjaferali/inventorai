"""G1-START-PATH-LOCKOUT-01 — the creation-time disclosure beside the integrated-invention box.

Synthetic ideas only. What is pinned:
  * ONE static note sits immediately after the existing, optional, unticked box wherever it is offered — for
    an idea the classifier reads as a single domain, for a no-match idea and for an unrelated idea — with the
    SAME text in every case (no recognition, highlighting, preselection or inference from the idea);
  * the note says that fixed mechanical parts count, pairs the board (electronic) with its enclosure
    (mechanical), asks the inventor to tick only if both really work together, discloses that the declaration
    is available only at project creation (adding it later needs a new project), and promises no tool, CAD
    output, component selection or compatibility;
  * EN / AR rendering, escaping, RTL-safe indentation and the accessible description;
  * the existing "Not sure" guidance no longer implies that a mechanical part must move;
  * nothing is created by viewing the page or declining the box; ticking it alone creates parts only, never a
    component, interaction, clearance declaration or DXF; a bound clearance declaration with an unknown
    dimension stays MISSING_INFORMATION with no DXF, while NO declaration stays NONE (never relabelled).
"""
import html as _html
import re

import pytest

import web.app as appmod
from engine import mechanical_planar_clearance as pcc
from engine.domain_rules import DomainResultKind, classify_domain
from tests.csrf_client import csrf_client
from tests.test_stage15_integrated_invention_entry import (  # noqa: F401  (fixture)
    ELEC, MECH, NONE_IDEA, _compose, _created, _live, _project_count, _store, _subsystem_rows, client)
from web import planar_clearance as view_mod
from web import ui_text

BOARD_IDEA = ("I want to develop a small electronic device with a circuit board inside an enclosure. I want "
              "the board to fit with enough clearance, but I have not decided the components or dimensions yet.")
UNRELATED_IDEA = "A battery powered LED torch with a dimmer circuit and a rechargeable cell."
NOTE_ATTR = "data-integrated-offer-note"


def _box_and_note(body):
    m = re.search(r'(<input type="checkbox" name="integrated_invention"[^>]*>).*?</label>\s*'
                  r'(<p id="integrated-offer-note"[^>]*' + NOTE_ATTR + r'[^>]*>(.*?)</p>)', body, re.S)
    assert m, "the note must follow the integrated box immediately"
    return m.group(1), m.group(2), _html.unescape(m.group(3))


def _start(c, idea, lang=None):
    if lang == "ar":
        assert c.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    return c.post("/start", data={"idea": idea})


# ==========================================================================
# 1. the same static note wherever the box is offered
# ==========================================================================
def test_l01_single_classified_board_enclosure_idea_gets_the_box_and_the_note(client):
    result = classify_domain(BOARD_IDEA)
    assert result.kind is DomainResultKind.SINGLE and result.selected_domain == ELEC   # unchanged classifier
    resp = _start(client, BOARD_IDEA)
    body = resp.get_data(as_text=True)
    assert resp.status_code == 200 and 'name="domain_confirm"' in body
    box, note_tag, note = _box_and_note(body)
    assert "checked" not in box and "required" not in box
    assert 'aria-describedby="integrated-offer-note"' in box
    assert note == ui_text.text("UI_S15_OFFER_NOTE", "en")


def test_l02_no_match_entry_gets_the_same_note(client):
    assert classify_domain(NONE_IDEA).kind is DomainResultKind.NONE
    body = _start(client, NONE_IDEA).get_data(as_text=True)
    assert 'name="domain_choice"' in body
    _box, _tag, note = _box_and_note(body)
    assert note == ui_text.text("UI_S15_OFFER_NOTE", "en")


def test_l03_the_note_is_static_and_implies_no_reading_of_the_idea(client):
    notes = set()
    for idea in (BOARD_IDEA, UNRELATED_IDEA, NONE_IDEA):
        body = _start(client, idea).get_data(as_text=True)
        notes.add(_box_and_note(body)[2])
        assert body.count(NOTE_ATTR) == 1
    notes.add(_box_and_note(client.get("/").get_data(as_text=True))[2])     # the empty start page
    assert notes == {ui_text.text("UI_S15_OFFER_NOTE", "en")}
    # it never reports a recognition, a suggestion or a highlight
    note = ui_text.text("UI_S15_OFFER_NOTE", "en")
    for word in ("your idea mentions", "we detected", "recognised", "recognized", "suggest", "appears"):
        assert word not in note.lower()


def test_l04_the_note_discloses_the_irreversible_choice_and_promises_no_tool():
    en = ui_text.text("UI_S15_OFFER_NOTE", "en")
    for phrase in ("Fixed mechanical parts, such as an enclosure or mount, count too",
                   "a circuit board can be the electronic part and its enclosure the mechanical part",
                   "Tick this only if both types of parts really work together in your invention",
                   "available only at project creation", "adding it later currently requires a new project",
                   "require this declaration and further information"):
        assert phrase in en, phrase
    lowered = en.lower()
    for word in ("cad", "dxf", "verified", "compatib", "automatic", "select", "guarantee", "fit"):
        assert word not in lowered, word
    ar = ui_text.text("UI_S15_OFFER_NOTE", "ar")
    for phrase in ("ولو كانت ثابتة", "لوحة الدارة الجزء الإلكتروني", "العلبة المحيطة بها الجزء الميكانيكي",
                   "ضع علامة في هذا المربع فقط", "إلا عند إنشاء المشروع", "تتطلب مشروعًا جديدًا",
                   "تتطلب هذا التصريح ومعلومات إضافية"):
        assert phrase in ar, phrase


def test_l05_arabic_rendering_is_escaped_rtl_safe_and_placed(client):
    body = _start(client, BOARD_IDEA, lang="ar").get_data(as_text=True)
    box, tag, note = _box_and_note(body)
    assert note == ui_text.text("UI_S15_OFFER_NOTE", "ar")
    assert "margin-inline-start" in tag and "24px" in tag                 # indents on the start side
    assert 'dir="rtl"' in body[:2000]
    assert "checked" not in box


def test_l06_not_sure_guidance_no_longer_implies_movement():
    en = ui_text.text("UI_S15_GUIDE_NOT_SURE", "en")
    assert "which part moves and which part uses electricity" not in en
    assert "holds, protects or moves it" in en and "enclosure" in en and "mounting" in en
    ar = ui_text.text("UI_S15_GUIDE_NOT_SURE", "ar")
    assert "أيّ جزء يتحرك وأيّ جزء يستخدم الكهرباء" not in ar
    assert "يحمله أو يحميه أو يحرّكه" in ar and "علبة" in ar


# ==========================================================================
# 2. nothing is created or credited by the disclosure
# ==========================================================================
def test_l07_viewing_and_declining_create_no_project_fact(client):
    before, sessions = _project_count(), set(appmod.SESSION_STORE)
    _start(client, BOARD_IDEA)                                      # view only
    assert _project_count() == before and set(appmod.SESSION_STORE) == sessions
    sid = _created(client.post("/start", data={"idea": BOARD_IDEA, "domain_confirm": ELEC}))
    state = _live(sid)
    assert state.domain == ELEC and state.subsystems == [] and _subsystem_rows(sid) == []
    assert list(state.assertions) == []                            # no answer, credit or progression
    with csrf_client(appmod.app) as fresh:                          # the same project without the page view
        other = _created(fresh.post("/start", data={"idea": BOARD_IDEA, "domain_confirm": ELEC}))
    assert [(g.gap_type, g.status) for g in _live(other).gaps] == \
        [(g.gap_type, g.status) for g in state.gaps]


def test_l08_ticking_integration_alone_creates_parts_only(client):
    sid = _created(_compose(client, BOARD_IDEA, focus=ELEC))
    assert len(_subsystem_rows(sid)) == 2
    snapshot = _store().load_planar_clearance(sid)
    assert snapshot["interfaces"] == () or list(snapshot["interfaces"]) == []
    assert list(snapshot["inventory"].active) == []
    assert list(snapshot["ledger"].records) == []
    page = client.get("/session/%s" % sid).get_data(as_text=True)
    assert "data-pcc-link" not in page and "cad.zip" not in page


def test_l09_unknown_dimension_stays_missing_information_and_absence_stays_none():
    from tests.test_board_enclosure_planar_clearance import BINDING, _declare, _setup
    from engine.record_store import SqliteRecordStore
    import tempfile, os
    with tempfile.TemporaryDirectory() as tmp:
        store = SqliteRecordStore(os.path.join(tmp, "l09.db"))
        pid, _subs, ifc, b, e, _x = _setup(store, idea="i-l09")
        none_view = view_mod.clearance_view(store.load_planar_clearance(pid), ifc, BINDING)
        assert none_view["state"] == view_mod.STATE_NONE and none_view["evaluation"] is None
        assert not view_mod.cad_eligible(none_view)
        _declare(store, pid, ifc, b, e, values=("84", "50", "86", "56", pcc.VALUE_UNKNOWN))
        view = view_mod.clearance_view(store.load_planar_clearance(pid), ifc, BINDING)
        assert view["state"] == view_mod.STATE_CURRENT
        assert view["evaluation"]["outcome"] == pcc.OUTCOME_MISSING
        assert not view_mod.cad_eligible(view)
