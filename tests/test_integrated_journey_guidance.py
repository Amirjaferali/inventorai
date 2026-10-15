# -*- coding: utf-8 -*-
"""INTEGRATED-JOURNEY-GUIDANCE-01 — the Project Compass "What to do now" for a valid
integrated Mechanical + Electrical / Electronics invention, once every existing
higher-priority primary action is exhausted, offers ONE optional inventor-owned step
across the recorded parts and declared interactions, read only from the existing
Stage-15 owners:

1. the required part outside the initial analysis focus while either of its governed
   question families is not fully recorded (link to that part's question page);
2. otherwise a declared interaction whose optional verification-preparation inputs
   are not all recorded (link to the preparation page);
3. otherwise the existing review-handoff fallback, unchanged.

Proves: the order; that no interaction is ever invented (no declared interaction ->
no preparation step); the review handoff stays one click away; exactly one primary
action; the existing branch order and single-domain journeys are unchanged; unreadable
or inconsistent inputs fall back to the handoff; a GET writes nothing; a cold resume
keeps the behaviour; EN / AR copy states that nothing is assessed or validated.
Synthetic data only.
"""
import html as _html
import os
import pickle
import re
import sqlite3

import pytest

import web.app as appmod
from engine import subsystem_model as sm
from tests.test_stage15_integrated_invention_entry import ELEC, MECH, TIE_IDEA, _compose, _created, _live
from tests.test_stage28_control_loop_optional_part_slice1 import client  # noqa: F401  (fixture)
from tests.test_28t5_nonfocused_required_part_questions import _ids, _part, _save as _save_part
from tests.test_stage15_subsystem_interface_declaration import _declare
from tests.test_stage15_interface_preparation import _save as _save_prep, COND, ACCEPT, EVID
from tests.test_safe_question_routing_pf_q2 import MECH as MECH_ANSWER, PF_STRONG, BA_1, BA_2, _start
from web import ui_text

KEYS = ("UI_IJG_PART_NOTE_MECH", "UI_IJG_PART_NOTE_ELEC", "UI_IJG_PART_CTA_MECH",
        "UI_IJG_PART_CTA_ELEC", "UI_IJG_PREP_NOTE", "UI_IJG_PREP_CTA", "UI_IJG_HANDOFF_NOTE")


def _raw(c, sid):
    r = c.get(f"/session/{sid}")
    assert r.status_code == 200, r.status_code
    return r.get_data(as_text=True)


def _do_row(page):
    i = page.index('data-pc-row="do"')
    return page[i:page.index("</section>", i)]


def _primary(page):
    found = re.findall(r'<(?:a|button) class="journey-primary" data-primary-action[^>]*>', page)
    assert len(found) == 1, found
    return found[0]


def _answer(c, sid, text):
    raw = _raw(c, sid)
    token = re.search(r'name="answer_token" value="([^"]*)"', raw).group(1)
    assert c.post(f"/session/{sid}", data={"response": text, "answer_token": token}).status_code == 302


def _finished_focus(c, lang=None):
    """An integrated invention, Mechanical focus, whose focus questioning has no
    question left: the point where the Compass used to fall back to the handoff."""
    sid = _created(_compose(c, TIE_IDEA, focus=MECH, lang=lang))
    for value in (MECH_ANSWER, MECH_ANSWER, PF_STRONG, BA_1, BA_2):
        _answer(c, sid, value)
    assert 'href="#response"' not in _primary(_raw(c, sid))
    return sid


def _answer_all_part_questions(c, sid):
    part_id = _part(sid, ELEC)
    r = _save_part(c, sid, part_id, {q: "My own words about it." for q in _ids(ELEC)})
    assert r.status_code == 200 and ui_text.text("UI_PQ_MSG_SAVED", "en") in _html.unescape(r.get_data(as_text=True))
    return part_id


def _dump():
    with sqlite3.connect(os.environ["INVENTORAI_DB_PATH"]) as connection:
        return list(connection.iterdump())


# ---------------------------------------------------------------------------
# 1. the order: other part -> declared interaction preparation -> handoff
# ---------------------------------------------------------------------------
def test_01_the_other_part_is_offered_first_with_the_handoff_one_click_away(client):
    sid = _finished_focus(client)
    page = _raw(client, sid)
    primary = _primary(page)
    assert 'data-ijg-action="part_questions"' in primary
    assert f'href="/session/{sid}/part-questions?part={_part(sid, ELEC)}"' in primary
    do = _do_row(page)
    assert _html.unescape(ui_text.text("UI_IJG_PART_CTA_ELEC", "en")) in _html.unescape(do)
    assert _html.unescape(ui_text.text("UI_IJG_PART_NOTE_ELEC", "en")) in _html.unescape(do)
    # the review handoff stays one click away (a plain link, not a second primary)
    handoff = re.search(r'<p class="journey-note" data-ijg-handoff>.*?</p>', do, re.S).group(0)
    assert f'href="/session/{sid}/deliverable"' in handoff and "data-primary-action" not in handoff
    assert ui_text.text("UI_A1_REVIEW_HANDOFF", "en") in handoff


def test_02_some_answers_keep_the_other_part_step(client):
    sid = _finished_focus(client)
    part_id = _part(sid, ELEC)
    first = _ids(ELEC)[0]
    r = _save_part(client, sid, part_id, {first: "Only this one so far."})
    assert r.status_code == 200 and ui_text.text("UI_PQ_MSG_SAVED", "en") in _html.unescape(r.get_data(as_text=True))
    assert 'data-ijg-action="part_questions"' in _primary(_raw(client, sid))


def test_03_no_declared_interaction_is_never_invented_the_handoff_returns(client):
    sid = _finished_focus(client)
    _answer_all_part_questions(client, sid)
    page = _raw(client, sid)
    primary = _primary(page)
    assert "data-ijg-action" not in primary
    assert f'href="/session/{sid}/deliverable"' in primary
    assert "data-ijg-handoff" not in page and "data-ijg-note" not in page


def test_04_a_declared_interaction_offers_its_optional_preparation_then_the_handoff(client):
    sid = _finished_focus(client)
    _answer_all_part_questions(client, sid)
    assert _declare(client, sid, "The motor turns the hinge arm.").status_code == 302
    page = _raw(client, sid)
    primary = _primary(page)
    assert 'data-ijg-action="interface_preparation"' in primary
    assert f'href="/session/{sid}/interface-preparation"' in primary
    do = _html.unescape(_do_row(page))
    assert _html.unescape(ui_text.text("UI_IJG_PREP_NOTE", "en")) in do
    assert "data-ijg-handoff" in page
    [ifc] = appmod._get_store().load_subsystem_interfaces(sid)
    iid = ifc.interface_id
    # partly recorded -> still offered
    r = _save_prep(client, sid, {("operating_conditions", iid): COND})
    assert appmod.S15_PREP_SAVED_MESSAGE in _html.unescape(r.get_data(as_text=True))
    assert 'data-ijg-action="interface_preparation"' in _primary(_raw(client, sid))
    # all recorded -> the existing handoff fallback
    r = _save_prep(client, sid, {("acceptance_criterion", iid): ACCEPT,
                                 ("evidence_needed", iid): EVID})
    assert appmod.S15_PREP_SAVED_MESSAGE in _html.unescape(r.get_data(as_text=True))
    primary = _primary(_raw(client, sid))
    assert "data-ijg-action" not in primary and f'href="/session/{sid}/deliverable"' in primary


# ---------------------------------------------------------------------------
# 2. existing precedence and single-domain journeys are unchanged
# ---------------------------------------------------------------------------
def test_05_a_waiting_question_stays_the_primary_action(client):
    sid = _created(_compose(client, TIE_IDEA, focus=MECH))
    page = _raw(client, sid)
    assert 'href="#response"' in _primary(page)
    assert "data-ijg" not in page


def test_06_single_domain_projects_never_see_the_guidance(client):
    sid = _start(client)
    for value in (MECH_ANSWER, MECH_ANSWER, PF_STRONG, BA_1, BA_2):
        _answer(client, sid, value)
    page = _raw(client, sid)
    assert f'href="/session/{sid}/deliverable"' in _primary(page)
    assert "data-ijg" not in page
    assert appmod._integrated_journey_guidance(sid, appmod._integrated_scope_context(_live(sid))) is None


def test_07_the_branch_sits_after_every_existing_branch_and_before_the_fallback():
    with open("web/templates/session.html", encoding="utf-8") as fh:
        tpl = fh.read()
    do = tpl[tpl.index('data-pc-row="do"'):tpl.index("</section>", tpl.index('data-pc-row="do"'))]
    crit = do.index("{% elif criticality_step %}")
    part = do.index("{% elif integrated_guidance and integrated_guidance.kind == 'part_questions' %}")
    prep = do.index("{% elif integrated_guidance and integrated_guidance.kind == 'interface_preparation' %}")
    fallback = do.index("{% else %}", prep)
    assert crit < part < prep < fallback
    assert "UI_A1_REVIEW_HANDOFF" in do[fallback:]


# ---------------------------------------------------------------------------
# 3. fail closed; nothing written; cold resume
# ---------------------------------------------------------------------------
def test_08_an_unreadable_part_record_falls_back_to_the_handoff(client, monkeypatch):
    sid = _finished_focus(client)
    store = appmod._get_store()

    def boom(*_a, **_k):
        raise RuntimeError("unreadable")
    monkeypatch.setattr(type(store), "load_nonfocused_part_record", boom)
    page = _raw(client, sid)
    assert f'href="/session/{sid}/deliverable"' in _primary(page)
    assert "data-ijg" not in page


def test_09_an_inconsistent_part_identity_falls_back(client, monkeypatch):
    sid = _finished_focus(client)
    scope = appmod._integrated_scope_context(_live(sid))
    scope["nonfocused_questions"]["part_id"] = "sub-not-this-part"
    assert appmod._integrated_journey_guidance(sid, scope) is None


def test_10_a_read_only_part_or_an_unattached_preparation_offers_nothing():
    scope = {"nonfocused_questions": {"part": "electrical", "part_id": "x", "editable": False},
             "interfaces": [{"a": "A", "b": "B", "description": "d", "preparation": None}]}
    assert appmod._integrated_journey_guidance("no-such-project", scope) is None
    assert appmod._integrated_journey_guidance("no-such-project", None) is None


def test_11_viewing_the_page_writes_nothing(client):
    sid = _finished_focus(client)
    before = (_dump(), pickle.dumps(_live(sid)))
    for _ in range(2):
        assert 'data-ijg-action="part_questions"' in _primary(_raw(client, sid))
    assert (_dump(), pickle.dumps(_live(sid))) == before


def test_12_a_cold_resume_keeps_the_guidance(client):
    sid = _finished_focus(client)
    state = _live(sid)
    gaps = [(g.gap_type, g.status) for g in state.gaps]
    maturity = state.maturity_level
    appmod.SESSION_STORE.pop(sid)
    assert 'id="resume-project"' in _primary(_raw(client, sid))
    assert client.post(f"/session/{sid}/resume").status_code == 302
    page = _raw(client, sid)
    assert 'data-ijg-action="part_questions"' in _primary(page)
    resumed = _live(sid)
    assert [(g.gap_type, g.status) for g in resumed.gaps] == gaps
    assert resumed.maturity_level == maturity


# ---------------------------------------------------------------------------
# 4. EN / AR copy: optional, recording only, no assessment
# ---------------------------------------------------------------------------
def test_13_arabic_journey_renders_the_arabic_guidance(client):
    sid = _finished_focus(client, lang="ar")
    page = _raw(client, sid)
    assert 'dir="rtl"' in page
    do = _html.unescape(_do_row(page))
    assert ui_text.text("UI_IJG_PART_CTA_ELEC", "ar") in do
    assert ui_text.text("UI_IJG_PART_NOTE_ELEC", "ar") in do
    assert ui_text.text("UI_IJG_HANDOFF_NOTE", "ar") in do


def test_14_copy_is_bilingual_optional_and_claims_no_validation():
    for key in KEYS:
        for lang in ("en", "ar"):
            assert ui_text.has_string(key) and ui_text.text(key, lang).strip(), (key, lang)
    for key in ("UI_IJG_PART_NOTE_MECH", "UI_IJG_PART_NOTE_ELEC", "UI_IJG_PREP_NOTE"):
        en = ui_text.text(key, "en").lower()
        assert "optional" in en and ("does not" in en)
        for word in ("validated", "verified", "compatible ", "safe ", "required", "must "):
            assert word not in en.replace("does not assess or validate", "").replace(
                "does not check", ""), (key, word)
    assert "اختيار" in ui_text.text("UI_IJG_PART_NOTE_ELEC", "ar")
    assert "اختيار" in ui_text.text("UI_IJG_PREP_NOTE", "ar")


def test_15_constants_reuse_the_existing_owners():
    assert sm.PART_QUESTION_GAP_TYPES == ("MECHANISM_COMPLETENESS", "BOUNDARY_AMBIGUITY")
    src = open(appmod.__file__, encoding="utf-8").read()
    body = src[src.index("def _integrated_journey_guidance"):]
    body = body[:body.index("\n\n\n")]
    for owner in ("load_nonfocused_part_record", "part_family_presence", "get_domain_questions",
                  "PREPARATION_ALL_RECORDED"):
        assert owner in body, owner
    for forbidden in ("_write", "append_", "set_", "save_", "request."):
        assert forbidden not in body, forbidden
