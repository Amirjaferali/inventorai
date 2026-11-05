"""G1-PCC-LITERAL-SOURCE-AID-01 — reuse ONE literal board pair from the original idea.

Synthetic data only. What is pinned:
  * the recognizer (``web/planar_clearance.py`` ``literal_board_pair``) locates exactly one literal
    ``A x B mm`` pair whose sentence names a board, and refuses every uncertain, hypothetical,
    alternative, negated, conflicting, unit-less, other-unit, other-digit or extra-number case;
  * the numbers are the method's own strict grammar, copied verbatim; no axis is implied;
  * the page SHOWS the passage and both explicit assignments with none chosen; it selects no
    component, answers no declaration and fills no field (the script fills EMPTY fields only);
  * the save path is the existing one and never parses the board basis note: the note stays the
    inventor's documentary, editable text; correction and withdrawal are unchanged; the same values
    give the same result as manual entry;
  * rendering the aid writes nothing and changes no progression, readiness or answer state.
"""
import html as _html
import os
import re
import sqlite3

import pytest

import web.app as appmod
from engine import mechanical_planar_clearance as pcc
from tests.csrf_client import csrf_client
from tests.test_board_enclosure_planar_clearance import APPLIES, _fields, _outcome, _margin_cells
from tests.test_component_interface_participation import _form as _icp_form, _post as _icp_post
from tests.test_component_inventory_declare_list import _declare as _declare_component
from tests.test_stage15_integrated_invention_entry import _compose, _created
from tests.test_stage15_subsystem_interface_declaration import _declare as _declare_interface
from web import planar_clearance as aid
from web import ui_text

IDEA = ("A smart planter that opens its lid on a hinge when the soil is dry. "
        "My circuit board is 85 x 56 mm.")
IDEA_AR = "حوض نباتات ذكي يفتح غطاءه على مفصّلة عندما تجف التربة. مقاس اللوحة 85 × 56 mm."
NOTE_X = "From my original idea: “85 x 56 mm”; I entered 85 as board X and 56 as board Y."
NOTE_Y = "From my original idea: “85 x 56 mm”; I entered 56 as board X and 85 as board Y."


# ==========================================================================
# 1. recognizer — bounded scope, verbatim numbers, refusal outside it
# ==========================================================================
@pytest.mark.parametrize("idea,first,second,span", [
    ("My board is 85 x 56 mm.", "85", "56", "85 x 56 mm"),
    ("My board is 85×56 mm.", "85", "56", "85×56 mm"),
    ("The PCB is 85.5 X 56.25mm", "85.5", "56.25", "85.5 X 56.25mm"),
    ("The board size is 80 x 50 mm.", "80", "50", "80 x 50 mm"),
    ("Board dimensions: 80 x 50 mm", "80", "50", "80 x 50 mm"),
    ("The board measures 80 x 50 mm and it is green.", "80", "50", "80 x 50 mm"),
    ("A weather station with an 85 x 56 mm board.", "85", "56", "85 x 56 mm"),
    ("اللوحة مقاسها 85 × 56 mm.", "85", "56", "85 × 56 mm"),
    ("لوحة بمقاس 85 × 56 mm.", "85", "56", "85 × 56 mm"),
    ("A lamp. The board: 70 * 30 mm. It is bright.", "70", "30", "70 * 30 mm"),
    ("مقاس اللوحة 85 × 56 mm. وأريد علبة لها.", "85", "56", "85 × 56 mm"),
    ("The board is 999999.9999 x 0.0001 mm.", "999999.9999", "0.0001", "999999.9999 x 0.0001 mm"),
])
def test_r01_one_literal_board_pair_is_located_verbatim(idea, first, second, span):
    pair = aid.literal_board_pair(idea)
    assert pair == {"passage": pair["passage"], "span": span, "first": first,
                    "second": second, "unit": "mm"}
    assert span in pair["passage"] and pair["passage"] in idea


@pytest.mark.parametrize("idea", [
    "Maybe the board is 85 x 56 mm.",                             # hypothetical
    "The board might be 85 x 56 mm.",
    "If the board is 85 x 56 mm it fits.",
    "The board is about 85 x 56 mm.",                             # approximate
    "The board is roughly 85 x 56 mm.",
    "The board is ~85 x 56 mm.",
    "The board is not 85 x 56 mm.",                               # negated
    "The board isn't 85 x 56 mm.",
    "The board is 85 x 56 mm or 90 x 60 mm.",                     # alternatives
    "The board is 85 x 56 mm. Later the board is 90 x 60 mm.",    # contradictory passages
    "The board is 85 x 56 mm. The box is 120 x 80 mm.",           # a second pair anywhere
    "The board is 85 x 56 mm. A 3x4 grid of LEDs.",
    "The board is 85 x 56 cm.",                                   # another unit
    "The board is 85 x 56.",                                      # no unit
    "The board is 85 x 56 in.",
    "The board is 85 x 56 mm².",
    "The board is ٨٥ × ٥٦ mm.",                                   # another digit system
    "The board is 85,5 x 56 mm.",                                 # comma decimal
    "The board is 85٫5 x 56 mm.",
    "The board is 1/85 x 56 mm.",
    "The board is -85 x 56 mm.",
    "The board is +85 x 56 mm.",
    "A 85 x 56 mm board inside a box.",                           # another object in the sentence
    "The case is 85 x 56 mm.",                                    # no board named
    "The lid is 85 x 56 mm.",
    "It is 85 x 56 mm.",
    "The ESP32 board is 85 x 56 mm.",                             # a third number
    "The board is 85 x 56 mm and 1.6 mm thick.",
    "The board is 85-90 x 56 mm.",                                # a range
    "The board is 0 x 56 mm.",                                    # outside the strict grammar
    "The board is 1234567 x 56 mm.",
    "The board is 85.12345 x 56 mm.",
    "ربما اللوحة 85 × 56 mm.",                                    # Arabic hypothetical
    "اللوحة ليست 85 × 56 mm.",                                    # Arabic negation
    "اللوحة حوالي 85 × 56 mm.",                                   # Arabic approximate
    "اللوحة 85 × 56 mm أو 90 × 60 mm.",
    "اللوحة مقاسها 85 × 56 mm وتوضع داخل علبة.",                  # Arabic other object
    # Lead finding: a board mentioned in the sentence does not bind another object's size
    "The board carries a camera that is 80 x 50 mm.",
    "The board holds an 80 x 50 mm camera.",
    "On the board, a 80 x 50 mm display.",
    "The board is fixed and the lens is 80 x 50 mm.",
    "The board is 80 x 50 mm camera.",
    "My board drives a fan; the fan is 80 x 50 mm.",
    "The board sits next to 80 x 50 mm.",
    "اللوحة تحمل كاميرا 80 × 50 mm.",
    "اللوحة متصلة بعدسة مقاسها 80 × 50 mm.",
    # review findings: limits, comparisons, past or unsure statements, other objects
    "The board must be smaller than 80 x 50 mm.",
    "The board is at most 80 x 50 mm.",
    "The board is up to 80 x 50 mm.",
    "The board is between 70 x 40 mm and something else.",
    "The board is 80 x 50 mm minimum.",
    "اللوحة أقل من 80 x 50 mm.",
    "The board used to be 80 x 50 mm, now it is bigger.",
    "The board is 80 x 50 mm, I think.",
    "A small board drives a 40 x 30 mm screen.",
    "The board needs a 80 x 50 mm battery.",
    "The board's mounting holes are 70 x 40 mm apart.",
    "لوحة شمسية مقاسها 80 x 50 mm.",
    "لوحة المفاتيح مقاسها 80 x 50 mm.",
    "Two boards, each 80 x 50 mm.",
    "The board is 80\nx 50 mm.",                                   # a line break in the pair
    "The board is 80" + " " * 250 + "x 50 mm.",                    # unbounded spacing
    "The board is ٣80 x 50 mm.",                                   # another digit system before it
    "",
    None,
    "The board is 85 x 56 mm. " + "x" * 2000,                     # longer than the bound
])
def test_r02_everything_outside_the_bounded_scope_is_refused(idea):
    assert aid.literal_board_pair(idea) is None


def test_r03_the_numbers_pass_the_methods_own_grammar_unchanged():
    pair = aid.literal_board_pair("My board is 85.50 x 056 mm.")
    assert (pair["first"], pair["second"]) == ("85.50", "056")
    for text in (pair["first"], pair["second"]):
        assert pcc.is_admitted_value("board_x", text) and pcc.is_admitted_value("board_y", text)


def test_r04_the_assignment_is_only_the_inventors_explicit_choice():
    pair = aid.literal_board_pair("My board is 85 x 56 mm.")
    assert aid.aid_assignment(pair, "first_x") == ("85", "56")
    assert aid.aid_assignment(pair, "first_y") == ("56", "85")
    for forged in (None, "", "x", "auto", "first_X"):
        assert aid.aid_assignment(pair, forged) is None
    offer = aid.aid_offer(pair, "en")
    assert [o["order"] for o in offer["orders"]] == list(aid.AID_ORDERS)
    assert "checked" not in str(offer) and "selected" not in str(offer)
    assert aid.aid_offer(None, "en") is None


def test_r05_the_note_states_only_the_source_and_the_inventors_assignment():
    pair = aid.literal_board_pair(IDEA)
    assert aid.aid_note(pair, "first_x", "en") == NOTE_X
    assert aid.aid_note(pair, "first_y", "en") == NOTE_Y
    ar = aid.aid_note(pair, "first_x", "ar")
    assert ar.startswith(aid.AID_NOTE_PREFIX["ar"]) and "85 x 56 mm" in ar
    for note in (NOTE_X, NOTE_Y, ar):
        assert len(note) <= 300
        for claim in ("verified", "checked", "correct", "validated", "measured"):
            assert claim not in note.lower()


# ==========================================================================
# 2. web — the existing page, form and save path
# ==========================================================================
@pytest.fixture
def client():
    appmod.app.config["TESTING"] = True
    with csrf_client(appmod.app) as c:
        yield c


def _project(c, idea=IDEA, lang=None):
    if lang == "ar":
        assert c.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    sid = _created(_compose(c, idea))
    assert _declare_interface(c, sid, "The board sits inside the case").status_code == 302
    for name in ("Driver board", "Plastic case"):
        assert _declare_component(c, sid, name=name, function="Does its job").status_code in (200, 302)
    form = _icp_form(c, sid)
    ids = [o[0] for o in form["options"]]
    assert _icp_post(c, sid, form, ids).status_code in (200, 302)
    ifc = appmod._get_store().load_planar_clearance(sid)["interfaces"][0].interface_id
    return sid, ifc, ids


def _url(sid, ifc):
    return "/session/%s/interface-clearance/%s" % (sid, ifc)


def _body(resp):
    return resp.get_data(as_text=True)


def _form_chunk(body):
    return re.search(r"<form[^>]*data-pcc-form>.*?</form>", body, re.S).group(0)


def _aid_chunk(body):
    m = re.search(r"<div class=\"pcc-box\" data-pcc-aid>.*?</div>\s*</div>|"
                  r"<div class=\"pcc-box\" data-pcc-aid>.*?data-pcc-aid-manual>[^<]*</p>\s*</div>",
                  body, re.S)
    return m.group(0) if m else None


def _submit(c, sid, ifc, ids, bx, by, note, page=None, extra=None):
    data = _fields(_body(page or c.get(_url(sid, ifc))))
    data.update({"board_component_id": ids[0], "enclosure_component_id": ids[1],
                 "region_description": "Inner floor between the four posts",
                 "basis_board": note})
    for role, value in zip(pcc.VALUE_ROLES, (bx, by, "90", "60", "2")):
        data["value_" + role] = value
    for d, a in zip(pcc.DECLARATION_IDS, APPLIES):
        data["decl_" + d] = a
    data.update(extra or {})
    return c.post(_url(sid, ifc), data=data)


def _dump():
    appmod._get_store()
    conn = sqlite3.connect(os.environ["INVENTORAI_DB_PATH"])
    try:
        return "\n".join(conn.iterdump())
    finally:
        conn.close()


def test_w01_the_page_shows_the_passage_and_chooses_nothing(client):
    sid, ifc, _ids = _project(client)
    before = _dump()
    body = _body(client.get(_url(sid, ifc)))
    assert _dump() == before                                   # rendering writes nothing
    chunk = _aid_chunk(body)
    assert chunk is not None
    assert "My circuit board is 85 x 56 mm" in _html.unescape(chunk)
    assert re.search(r"<div data-pcc-aid-controls hidden>", chunk)   # script-only controls
    assert 'name="pcc_aid_order"' in chunk and not re.search(r"<input[^>]*\bchecked\b", chunk)
    assert re.findall(r'value="(first_[xy])"', chunk) == ["first_x", "first_y"]
    assert ui_text.text("UI_PCC_AID_BOUNDARY", "en") in _html.unescape(chunk)
    form = _form_chunk(body)
    assert "pcc_aid_order" not in form                          # nothing is submitted with the save
    assert not re.search(r"<input[^>]*\bchecked\b", form) and not re.search(r"<option[^>]*\bselected\b", form)
    assert re.search(r'id="pcc-v-board_x"[^>]*value=""', form)
    assert re.search(r'id="pcc-basis_board"[^>]*value=""', form)
    assert "js/pcc_literal_aid.js" in body


def test_w02_no_aid_without_exactly_one_literal_pair(client):
    for idea in ("A smart planter that opens its lid on a hinge.",
                 "A smart planter on a hinge. Maybe the board is 85 x 56 mm.",
                 "A planter on a hinge. The board is 85 x 56 mm. The lid is 120 x 80 mm."):
        sid, ifc, _ = _project(client, idea)
        body = _body(client.get(_url(sid, ifc)))
        assert "data-pcc-aid" not in body and "pcc_literal_aid.js" not in body


def test_w03_the_passage_is_escaped(client):
    idea = 'A planter on a hinge. <b onclick="x()"> My board is 85 x 56 mm.'
    sid, ifc, _ = _project(client, idea)
    body = _body(client.get(_url(sid, ifc)))
    chunk = _aid_chunk(body)
    assert chunk is not None and "<b onclick" not in chunk
    assert "&lt;b onclick=" in chunk


def test_w04_the_aid_values_save_exactly_like_manual_entry(client):
    sid, ifc, ids = _project(client)
    r = _submit(client, sid, ifc, ids, "85", "56", NOTE_X)
    assert r.status_code == 200, _body(r)
    via_aid = (_outcome(_body(r)), _margin_cells(_body(r)))
    sid2, ifc2, ids2 = _project(client, "A smart planter that opens its lid on a hinge.")
    r2 = _submit(client, sid2, ifc2, ids2, "85", "56", "Measured with calipers")
    manual = (_outcome(_body(r2)), _margin_cells(_body(r2)))
    assert via_aid == manual and via_aid[0] == ["MET"]
    m = appmod._get_store().load_planar_clearance(sid)["ledger"].active_for(ifc).current
    assert m.values_map()["board_x"] == "85" and m.values_map()["board_y"] == "56"
    assert m.basis_map()["basis_board"] == NOTE_X
    assert m.board_component_id == ids[0] and m.enclosure_component_id == ids[1]


def test_w05_a_swapped_assignment_is_saved_as_the_inventor_chose(client):
    sid, ifc, ids = _project(client)
    r = _submit(client, sid, ifc, ids, "56", "85", NOTE_Y)
    assert r.status_code == 200
    m = appmod._get_store().load_planar_clearance(sid)["ledger"].active_for(ifc).current
    assert (m.values_map()["board_x"], m.values_map()["board_y"]) == ("56", "85")


def test_w06_the_note_is_documentary_and_never_parsed_by_the_save(client, monkeypatch):
    """Any note saves verbatim through the existing path, including notes in the aid's wording
    whose values no longer match and notes beginning with similar words; the save never reads
    the original idea."""
    sid, ifc, ids = _project(client)
    def no_read(_sid):
        raise AssertionError("the save path read the original idea")
    page = client.get(_url(sid, ifc))
    monkeypatch.setattr(appmod, "_original_idea_text", no_read)
    for bx, by, note in (
            ("56", "85", NOTE_X),                                      # stale proposal, kept as written
            ("85", "57", NOTE_X + " I later re-measured Y."),
            ("85", "56", aid.AID_NOTE_PREFIX["en"] + "the sketch on page 2"),
            ("85", "56", "From my original idea and a caliper check"),
            ("85", "56", aid.AID_NOTE_PREFIX["ar"] + "رسم يدوي")):
        r = _submit(client, sid, ifc, ids, bx, by, note, page=page)
        assert r.status_code == 200, note
        m = appmod._get_store().load_planar_clearance(sid)["ledger"].active_for(ifc).current
        assert (m.values_map()["board_x"], m.values_map()["board_y"]) == (bx, by)
        assert m.basis_map()["basis_board"] == note
        page = client.get(_url(sid, ifc))


def test_w07_no_note_check_or_aid_owner_exists_on_the_save_path():
    import inspect
    src = inspect.getsource(appmod.planar_clearance_save) + inspect.getsource(appmod._pcc_write)
    assert "_pcc_view" not in src and "_original_idea_text" not in src
    assert not hasattr(aid, "aid_note_consistent") and not hasattr(aid, "aid_note_claimed")
    assert not ui_text.has_string("UI_PCC_AID_MSG_NOTE_MISMATCH")


def test_w08_correction_and_withdrawal_are_the_unchanged_paths(client):
    sid, ifc, ids = _project(client)
    assert _submit(client, sid, ifc, ids, "85", "56", NOTE_X).status_code == 200
    page = client.get(_url(sid, ifc))
    body = _body(page)
    form = _form_chunk(body)
    assert re.search(r'id="pcc-v-board_x"[^>]*value="85"', form)   # existing values shown
    assert "data-pcc-aid" in body                                   # the passage is still shown
    head = appmod._get_store().load_planar_clearance(sid)["ledger"].active_for(ifc).head_revision_no
    r = _submit(client, sid, ifc, ids, "86", "56", "Re-measured with calipers", page=page)
    assert r.status_code == 200
    rec = appmod._get_store().load_planar_clearance(sid)["ledger"].active_for(ifc)
    assert rec.head_revision_no == head + 1
    assert rec.current.basis_map()["basis_board"] == "Re-measured with calipers"
    data = _fields(_body(client.get(_url(sid, ifc))), form="data-pcc-withdraw-form")
    data["withdraw_confirm"] = "yes"
    r = client.post(_url(sid, ifc) + "/withdraw", data=data)
    assert r.status_code == 200
    assert appmod._get_store().load_planar_clearance(sid)["ledger"].active_for(ifc) is None


def test_w09_a_stale_form_is_still_refused_by_the_existing_path(client):
    sid, ifc, ids = _project(client)
    page = client.get(_url(sid, ifc))
    assert _submit(client, sid, ifc, ids, "85", "56", NOTE_X, page=page).status_code == 200
    before = _dump()
    # the same, now stale, page (expected head "none") with a fresh aid note
    r = _submit(client, sid, ifc, ids, "56", "85", NOTE_Y, page=page,
                extra={"pcc_submission": _fields(_body(client.get(_url(sid, ifc))))["pcc_submission"]})
    assert r.status_code == 409
    assert _dump() == before


def test_w10_forged_aid_fields_are_ignored_by_the_save(client):
    sid, ifc, ids = _project(client)
    r = _submit(client, sid, ifc, ids, "85", "56", "Measured",
                extra={"pcc_aid_order": "first_y", "aid": "1"})
    assert r.status_code == 200
    m = appmod._get_store().load_planar_clearance(sid)["ledger"].active_for(ifc).current
    assert (m.values_map()["board_x"], m.values_map()["board_y"]) == ("85", "56")


def test_w11_arabic_page_and_note(client):
    sid, ifc, ids = _project(client, IDEA_AR, lang="ar")
    body = _body(client.get(_url(sid, ifc)))
    chunk = _aid_chunk(body)
    assert chunk is not None
    text = _html.unescape(chunk)
    assert ui_text.text("UI_PCC_AID_BOUNDARY", "ar") in text
    assert 'data-pcc-aid-first>85</bdi>' in chunk and '<bdi dir="ltr" data-pcc-aid-first>' in chunk
    pair = aid.literal_board_pair(IDEA_AR)
    note = aid.aid_note(pair, "first_x", "ar")
    assert _html.escape(note, quote=True) in chunk
    r = _submit(client, sid, ifc, ids, "85", "56", note)
    assert r.status_code == 200
    m = appmod._get_store().load_planar_clearance(sid)["ledger"].active_for(ifc).current
    assert m.basis_map()["basis_board"] == note


def test_w12_no_progression_readiness_or_answer_credit(client):
    sid, ifc, ids = _project(client)
    state = appmod.SESSION_STORE[sid]["state"]
    gaps = [(g.gap_type, g.status) for g in state.gaps]
    answers = len(state.assertions)
    client.get(_url(sid, ifc))
    assert _submit(client, sid, ifc, ids, "85", "56", NOTE_X).status_code == 200
    state = appmod.SESSION_STORE[sid]["state"]
    assert [(g.gap_type, g.status) for g in state.gaps] == gaps
    assert len(state.assertions) == answers


def test_w13_every_aid_string_exists_in_both_languages():
    keys = [k for k in ui_text.__dict__.get("_STRINGS", {}) if k.startswith("UI_PCC_AID_")] or [
        "UI_PCC_AID_HEADING", "UI_PCC_AID_INTRO", "UI_PCC_AID_NUMBERS", "UI_PCC_AID_BOUNDARY",
        "UI_PCC_AID_ORDER_PROMPT", "UI_PCC_AID_AS_X", "UI_PCC_AID_AS_Y", "UI_PCC_AID_APPLY",
        "UI_PCC_AID_APPLY_NOTE", "UI_PCC_AID_MANUAL", "UI_PCC_AID_MSG_CHOOSE",
        "UI_PCC_AID_MSG_OCCUPIED", "UI_PCC_AID_MSG_DONE", "UI_PCC_AID_MSG_BOARD_FIRST",
        "UI_PCC_AID_MSG_NOTE_CLEARED", "UI_PCC_AID_MSG_NOTE_REVIEW"]
    for key in keys:
        assert ui_text.has_string(key)
        en, ar = ui_text.text(key, "en"), ui_text.text(key, "ar")
        assert en and ar and en != ar


def test_w14_one_component_as_both_board_and_enclosure_is_still_refused(client):
    sid, ifc, ids = _project(client)
    before = _dump()
    r = _submit(client, sid, ifc, ids, "85", "56", NOTE_X,
                extra={"enclosure_component_id": ids[0]})
    assert r.status_code in (400, 409) and _dump() == before


def test_w15_an_inventors_own_words_after_the_proposed_note_save(client):
    sid, ifc, ids = _project(client)
    r = _submit(client, sid, ifc, ids, "85", "56", NOTE_X + " Measured with calipers.")
    assert r.status_code == 200
    m = appmod._get_store().load_planar_clearance(sid)["ledger"].active_for(ifc).current
    assert m.basis_map()["basis_board"] == NOTE_X + " Measured with calipers."
