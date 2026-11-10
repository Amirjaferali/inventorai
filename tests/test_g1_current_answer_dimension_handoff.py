"""G1-CURRENT-ANSWER-DIMENSION-HANDOFF-01 — the literal board aid also reads CURRENT answers.

Synthetic data only. What is pinned:
  * the unchanged recognizer (``literal_board_pair``) runs on the original idea and on each
    CURRENT answered inventor record on its own; superseded records, provisional assumptions and
    every non-answer record are never a source;
  * one located pair, or several holding the same two numbers, give ONE offer: from the original
    idea when it holds one, otherwise from the most recent current answer, labelled by source;
    different numbers give a neutral conflict notice and no offer, never a chosen pair;
  * an unreadable history gives no aid at all, never an offer read from part of it;
  * the proposal is the existing one: nothing is chosen or stored on render, the existing save
    records exactly what the inventor submits, the note is documentary and within its bound, and
    a later correction of the answer never changes saved values;
  * EN / AR, no progression, readiness or answer-state change.
"""
import html as _html
import re
from types import SimpleNamespace

import pytest

import web.app as appmod
from engine import idea_state as ledger
from tests.test_board_enclosure_planar_clearance import _margin_cells, _outcome
from tests.test_g1_pcc_literal_source_aid import (
    _aid_chunk, _body, _dump, _form_chunk, _project, _submit, _url, client)  # noqa: F401
from tests.test_t2g_versioned_journey import _answer, _correct
from web import planar_clearance as aid
from web import ui_text

PLAIN = "A smart planter that opens its lid on a hinge when the soil is dry."
IDEA_85 = PLAIN + " My circuit board is 85 x 56 mm."


def _rec(content, disposition=ledger.DISPOSITION_ANSWERED, provenance=ledger.OWNER_STATED,
         superseded_by=None):
    return SimpleNamespace(content=content, disposition=disposition, provenance=provenance,
                           superseded_by=superseded_by)


# ==========================================================================
# 1. source selection — pure
# ==========================================================================
def test_s01_only_current_answered_inventor_records_are_sources():
    records = [
        _rec("My board is 10 x 20 mm.", superseded_by="r9"),                       # superseded
        _rec("My board is 11 x 21 mm.", ledger.DISPOSITION_PROVISIONAL_ASSUMPTION),
        _rec("My board is 12 x 22 mm.", ledger.DISPOSITION_UNKNOWN),
        _rec("My board is 13 x 23 mm.", ledger.DISPOSITION_DEFERRED),
        _rec("My board is 14 x 24 mm.", "specialist_requested"),
        _rec("My board is 15 x 25 mm.", provenance="SYSTEM_INFERRED"),           # not the inventor's
        _rec("   "),
        _rec("My board is 85 x 56 mm."),
        _rec("My board is 85 x 56 mm.", provenance=ledger.LEGACY_UNSPECIFIED),
    ]
    assert aid.current_answer_texts(records) == ["My board is 85 x 56 mm."] * 2
    pair = aid.current_board_pair(PLAIN, records)
    assert (pair["first"], pair["second"], pair["source"]) == ("85", "56", aid.AID_SOURCE_ANSWER)


@pytest.mark.parametrize("records", [
    None, "My board is 85 x 56 mm.", [object()],
    [SimpleNamespace(content="x", disposition="answered", provenance="OWNER_STATED")],
    [_rec(None)], [_rec(42)],
])
def test_s02_an_unreadable_history_raises_and_is_never_read_as_empty(records):
    with pytest.raises(ValueError):
        aid.current_board_pair(IDEA_85, records)


def test_s03_the_original_idea_behaves_exactly_as_before_when_no_answer_holds_a_pair():
    pair = aid.current_board_pair(IDEA_85, [_rec("The lid opens slowly.")])
    assert pair == dict(aid.literal_board_pair(IDEA_85), source=aid.AID_SOURCE_IDEA)
    assert aid.current_board_pair(PLAIN, []) is None
    assert aid.current_board_pair(None, []) is None


def test_s04_identical_numbers_give_one_pair_from_the_preferred_source():
    # the original idea wins when it holds the pair, whatever the answers' order
    pair = aid.current_board_pair(IDEA_85, [_rec("My board is 56 x 85 mm.")])
    assert (pair["source"], pair["first"], pair["second"]) == ("idea", "85", "56")
    # otherwise the MOST RECENT current answer, with its own passage and order
    pair = aid.current_board_pair(PLAIN, [_rec("The board is 85 x 56 mm."),
                                          _rec("My board is 56 x 85 mm.")])
    assert (pair["source"], pair["first"], pair["second"]) == ("answer", "56", "85")
    assert pair["passage"] == "My board is 56 x 85 mm"


@pytest.mark.parametrize("idea,texts", [
    (IDEA_85, ["My board is 90 x 60 mm."]),
    (PLAIN, ["My board is 85 x 56 mm.", "My board is 90 x 60 mm."]),
    (PLAIN, ["My board is 85 x 56 mm.", "My board is 85.0 x 56 mm."]),     # verbatim, never coerced
])
def test_s05_different_numbers_are_a_conflict_and_no_pair_is_chosen(idea, texts):
    assert aid.current_board_pair(idea, [_rec(t) for t in texts]) == {"conflict": True}


@pytest.mark.parametrize("text", [
    "Maybe the board is 85 x 56 mm.", "The board is about 85 x 56 mm.",
    "I use an 85 x 56 mm board with a microcontroller.",
    "The board is 85 x 56 mm. The lid is 120 x 80 mm.",
    "ربما اللوحة 85 × 56 mm.",
    "My board is 85 x 56 mm. " + "x" * aid.AID_MAX_IDEA_CHARS,
])
def test_s06_the_unchanged_grammar_refuses_answers_outside_its_scope(text):
    assert aid.current_board_pair(PLAIN, [_rec(text)]) is None


def test_s07_the_answer_note_names_its_source_and_stays_within_its_bound():
    pair = aid.current_board_pair(PLAIN, [_rec("My circuit board is 85 x 56 mm.")])
    en = aid.aid_note(pair, "first_x", "en")
    ar = aid.aid_note(pair, "first_y", "ar")
    assert en == "From my recorded answer: “85 x 56 mm”; I entered 85 as board X and 56 as board Y."
    assert ar.startswith(aid.AID_ANSWER_NOTE_PREFIX["ar"]) and "56 لـ X" in ar
    for note in (en, ar):
        assert len(note) <= 300
        for claim in ("verified", "checked", "correct", "validated", "measured", "linked"):
            assert claim not in note.lower()
    # a note that would exceed the field is never proposed, and never truncated
    long_pair = dict(pair, span="9" * 290)
    assert aid.aid_note(long_pair, "first_x", "en") is None
    assert aid.aid_offer(long_pair, "en") is None
    # the original-idea note is unchanged
    assert aid.aid_note(aid.literal_board_pair(IDEA_85), "first_x", "en").startswith(
        "From my original idea: ")


# ==========================================================================
# 2. web — the real answer, correction and save paths
# ==========================================================================
def _ledger(sid):
    return appmod._get_store().load_contract(sid).assertions


def _answered(c, sid, text, action=None):
    extra = {"action": action} if action else None
    assert _answer(c, sid, text, extra).status_code in (200, 302)
    return _ledger(sid)[-1]


def test_w01_a_current_answer_reaches_the_existing_form_and_comparison(client):
    sid, ifc, ids = _project(client, PLAIN)
    record = _answered(client, sid, "My circuit board is 85 x 56 mm.")
    assert record.disposition == ledger.DISPOSITION_ANSWERED and record.superseded_by is None
    state = appmod.SESSION_STORE[sid]["state"]
    progress = ([(g.gap_type, g.status) for g in state.gaps], len(state.assertions),
                state.maturity_level)
    before = _dump()
    body = _body(client.get(_url(sid, ifc)))
    assert _dump() == before                                       # rendering writes nothing
    chunk = _aid_chunk(body)
    assert chunk is not None and 'data-pcc-aid-source="answer"' in chunk
    text = _html.unescape(chunk)
    assert ui_text.text("UI_PCC_AID_HEADING_ANSWER", "en") in text
    assert ui_text.text("UI_PCC_AID_HEADING", "en") not in text
    assert "My circuit board is 85 x 56 mm" in text
    assert not re.search(r"<input[^>]*\bchecked\b", chunk)       # no axis chosen
    form = _form_chunk(body)
    assert not re.search(r"<option[^>]*\bselected\b", form)      # no component chosen
    assert re.search(r'id="pcc-v-board_x"[^>]*value=""', form)  # nothing filled
    assert 'data-pcc-freshness' in form
    assert "data-pcc-aid-conflict" not in body
    note = aid.aid_note(aid.current_board_pair(None, _ledger(sid)), "first_x", "en")
    assert _html.escape(note, quote=True) in chunk
    r = _submit(client, sid, ifc, ids, "85", "56", note)
    assert r.status_code == 200, _body(r)
    assert _outcome(_body(r)) == ["MET"]
    manual_sid, manual_ifc, manual_ids = _project(client, PLAIN)
    manual = _submit(client, manual_sid, manual_ifc, manual_ids, "85", "56", "Measured")
    assert _margin_cells(_body(r)) == _margin_cells(_body(manual))
    m = appmod._get_store().load_planar_clearance(sid)["ledger"].active_for(ifc).current
    assert (m.values_map()["board_x"], m.values_map()["board_y"]) == ("85", "56")
    assert m.basis_map()["basis_board"] == note
    assert m.board_component_id == ids[0] and m.enclosure_component_id == ids[1]
    state = appmod.SESSION_STORE[sid]["state"]
    assert ([(g.gap_type, g.status) for g in state.gaps], len(state.assertions),
            state.maturity_level) == progress


def test_w02_a_correction_replaces_the_source_and_never_changes_saved_values(client):
    sid, ifc, ids = _project(client, PLAIN)
    first = _answered(client, sid, "My circuit board is 85 x 56 mm.")
    note = aid.aid_note(aid.current_board_pair(None, _ledger(sid)), "first_x", "en")
    assert _submit(client, sid, ifc, ids, "85", "56", note).status_code == 200
    assert _correct(client, sid, first.record_id,
                    "My circuit board is 90 x 60 mm.").status_code in (200, 302)
    assert any(r.record_id == first.record_id and r.superseded_by for r in _ledger(sid))
    body = _body(client.get(_url(sid, ifc)))
    chunk = _html.unescape(_aid_chunk(body))
    assert "90 x 60 mm" in chunk and "85 x 56 mm" not in chunk      # the superseded text is gone
    assert "data-pcc-aid-conflict" not in body
    m = appmod._get_store().load_planar_clearance(sid)["ledger"].active_for(ifc).current
    assert (m.values_map()["board_x"], m.values_map()["board_y"]) == ("85", "56")
    assert m.basis_map()["basis_board"] == note                       # nothing re-bound
    assert re.search(r'id="pcc-v-board_x"[^>]*value="85"', _form_chunk(body))
    assert ui_text.text("UI_PCC_VALUES_FRESHNESS", "en") in _html.unescape(_form_chunk(body))


def test_w03_different_current_numbers_show_the_conflict_and_no_offer(client):
    sid, ifc, _ids = _project(client, IDEA_85)
    _answered(client, sid, "My circuit board is 90 x 60 mm.")
    body = _body(client.get(_url(sid, ifc)))
    assert "data-pcc-aid-conflict" in body
    assert ui_text.text("UI_PCC_AID_CONFLICT", "en") in _html.unescape(body)
    assert _aid_chunk(body) is None and "pcc_literal_aid.js" not in body
    assert "85 x 56" not in _html.unescape(body) and "90 x 60" not in _html.unescape(body)


def test_w04_identical_numbers_keep_the_original_idea_as_the_source(client):
    sid, ifc, _ids = _project(client, IDEA_85)
    _answered(client, sid, "My circuit board is 56 x 85 mm.")
    chunk = _aid_chunk(_body(client.get(_url(sid, ifc))))
    assert 'data-pcc-aid-source="idea"' in chunk
    assert "My circuit board is 85 x 56 mm" in _html.unescape(chunk)


@pytest.mark.parametrize("action", ["unknown", "deferred", "provisional_assumption",
                                    "specialist_requested", "evidence_requested"])
def test_w05_non_answer_records_are_never_a_source(client, action):
    sid, ifc, _ids = _project(client, PLAIN)
    record = _answered(client, sid, "My circuit board is 85 x 56 mm.", action=action)
    assert record.disposition != ledger.DISPOSITION_ANSWERED
    body = _body(client.get(_url(sid, ifc)))
    assert "data-pcc-aid" not in body


def test_w06_an_unreadable_history_shows_no_aid_and_the_page_still_renders(client, monkeypatch):
    sid, ifc, _ids = _project(client, IDEA_85)
    store = appmod._get_store()

    def broken(_sid):
        raise RuntimeError("ledger unreadable")
    monkeypatch.setattr(store, "load_contract", broken)
    resp = client.get(_url(sid, ifc))
    body = _body(resp)
    assert resp.status_code == 200 and "data-pcc-form" in body
    assert "data-pcc-aid" not in body                     # not even the original idea's pair


def test_w07_arabic_answer_offer_and_note(client):
    sid, ifc, ids = _project(client, "حوض نباتات ذكي يفتح غطاءه على مفصّلة.", lang="ar")
    _answered(client, sid, "مقاس اللوحة 85 × 56 mm.")
    body = _body(client.get(_url(sid, ifc)))
    chunk = _aid_chunk(body)
    assert chunk is not None
    text = _html.unescape(chunk)
    assert ui_text.text("UI_PCC_AID_HEADING_ANSWER", "ar") in text
    assert ui_text.text("UI_PCC_AID_INTRO_ANSWER", "ar") in text
    assert ui_text.text("UI_PCC_VALUES_FRESHNESS", "ar") in _html.unescape(_form_chunk(body))
    note = aid.aid_note(aid.current_board_pair(None, _ledger(sid)), "first_x", "ar")
    assert note.startswith("من إجابتي المسجّلة: ") and _html.escape(note, quote=True) in chunk
    assert _submit(client, sid, ifc, ids, "85", "56", note).status_code == 200
    m = appmod._get_store().load_planar_clearance(sid)["ledger"].active_for(ifc).current
    assert m.basis_map()["basis_board"] == note


def test_w08_the_conflict_notice_is_arabic_on_the_arabic_page(client):
    sid, ifc, _ids = _project(client, "حوض نباتات ذكي. مقاس اللوحة 85 × 56 mm.", lang="ar")
    _answered(client, sid, "مقاس اللوحة 90 × 60 mm.")
    body = _html.unescape(_body(client.get(_url(sid, ifc))))
    assert ui_text.text("UI_PCC_AID_CONFLICT", "ar") in body


def test_w09_a_foreign_interaction_is_denied_and_shows_no_answer(client):
    """The page's existing authorization is unchanged: another project's interaction reached
    through this project is the same non-enumerating denial, and no answer text leaks."""
    sid, _ifc, _ids = _project(client, PLAIN)
    other_sid, other_ifc, _other_ids = _project(client, PLAIN)
    _answered(client, other_sid, "My circuit board is 85 x 56 mm.")
    resp = client.get(_url(sid, other_ifc))
    assert resp.status_code == 302
    assert "85 x 56" not in resp.get_data(as_text=True)


def test_w10_the_save_path_still_reads_no_source():
    import inspect
    src = inspect.getsource(appmod.planar_clearance_save) + inspect.getsource(appmod._pcc_write)
    for name in ("_pcc_view", "load_contract", "current_board_pair", "_original_idea_text"):
        assert name not in src
