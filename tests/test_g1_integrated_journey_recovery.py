# -*- coding: utf-8 -*-
"""G1-INTEGRATED-JOURNEY-RECOVERY-01 — an inventor whose board-inside-enclosure idea entered as an
ordinary single-focus project may start a SEPARATE, NEW integrated project from the exact durable
original idea, through the EXISTING /start integrated-invention flow.

Synthetic ideas only. What is pinned:
  * the idea classifies SINGLE, is admitted as an ordinary project, and that project's session page
    offers ONE secondary recovery form (never a primary action) whose body carries no idea text;
  * following it with the explicit acknowledgement opens the EXISTING composition clarification with
    the FULL durable seed and writes nothing; the existing complete YES then creates a new project
    whose seed is the full idea and whose declared parts are exactly the inventor's;
  * the new project has its own identity and inherits no answer, and the original project's rows are
    byte-identical before and after; the new project reaches the existing #919 continuation;
  * negative controls: no acknowledgement, unknown / foreign project, CSRF, an already integrated
    project, an unreadable seed, inactive composition domains, an unsupported classification,
    NO / NOT SURE and a missing answer create nothing;
  * EN / AR copy, RTL page, and the idea never travels in a URL.
"""
import html as _html
import os
import re
import sqlite3

import pytest

import web.app as appmod
from engine import domain_activation
from engine.domain_rules import DomainClassification, DomainResultKind, classify_domain
from tests.csrf_client import csrf_client
from tests.test_stage15_integrated_invention_entry import (  # noqa: F401  (fixture)
    ELEC, MECH, _compose, _created, _project_count, _store, _subsystem_rows, client)
from tests.test_g1_integrated_engineering_continuation import (
    PARTS, _answer, _kind, _raw)
from tests.test_28t5_nonfocused_required_part_questions import _ids, _part, _save as _save_part
from tests.test_safe_question_routing_pf_q2 import MECH as MECH_ANSWER, PF_STRONG, BA_1, BA_2
from tests.test_p10_d3a_self_service_project_export import _client_for
from web import ui_text

BOARD_IDEA = ("I want to develop a small electronic device with a circuit board inside an enclosure. I want "
              "the board to fit with enough clearance, but I have not decided the components or dimensions "
              "yet. " + "The board reads a temperature sensor and lights a small LED when it gets warm. " * 3
              ).strip()
NEW_KEYS = ("UI_IJR_TITLE", "UI_IJR_NOTE", "UI_IJR_STEP_NOTE", "UI_IJR_ACK", "UI_IJR_BUTTON",
            "UI_IJR_UNAVAILABLE")


def _single(c, idea=BOARD_IDEA, lang=None):
    if lang == "ar":
        assert c.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    return _created(c.post("/start", data={"idea": idea, "domain_confirm": ELEC}))


def _section(page):
    m = re.search(r'<section class="integrated-restart".*?</section>', page, re.S)
    return m.group(0) if m else None


def _restart(c, sid, ack=True):
    data = {"integrated_restart_ack": "yes"} if ack else {}
    return c.post(f"/session/{sid}/integrated-restart", data=data, follow_redirects=False)


def _hidden_idea(page):
    m = re.search(r'<form method="POST" action="/start" class="composition-form".*?'
                  r'<input type="hidden" name="idea" value="([^"]*)">', page, re.S)
    assert m, "the existing composition form must carry the idea"
    return _html.unescape(m.group(1))


def _project_rows(sid):
    with sqlite3.connect(os.environ["INVENTORAI_DB_PATH"]) as connection:
        rows = []
        for (table,) in connection.execute(
                "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"):
            columns = [r[1] for r in connection.execute(f"PRAGMA table_info('{table}')")]
            if "project_id" in columns:
                rows.append((table, sorted(map(repr, connection.execute(
                    f"SELECT * FROM '{table}' WHERE project_id = ?", (sid,))))))
        return rows


def _record_count(sid):
    with sqlite3.connect(os.environ["INVENTORAI_DB_PATH"]) as connection:
        return connection.execute("SELECT COUNT(*) FROM records WHERE project_id = ?",
                                  (sid,)).fetchone()[0]


# ==========================================================================
# 1. the single entry and the offered action
# ==========================================================================
def test_r01_board_idea_enters_single_and_the_page_offers_one_secondary_action(client):
    result = classify_domain(BOARD_IDEA)
    assert result.kind is DomainResultKind.SINGLE and result.selected_domain == ELEC
    sid = _single(client)
    assert _subsystem_rows(sid) == []
    page = _raw(client, sid)
    section = _section(page)
    assert section is not None and page.count("data-integrated-restart") == 1
    text = _html.unescape(section)
    for key in ("UI_IJR_TITLE", "UI_IJR_NOTE", "UI_IJR_STEP_NOTE", "UI_IJR_ACK", "UI_IJR_BUTTON"):
        assert ui_text.text(key, "en") in text
    assert f'action="/session/{sid}/integrated-restart"' in section
    assert re.search(r'name="integrated_restart_ack" value="yes" required', section)
    assert "data-primary-action" not in section and "journey-primary" not in section
    # The form sends only the CSRF token and the acknowledgement: never the idea.
    assert set(re.findall(r'name="([^"]+)"', section)) == {"csrf_token", "integrated_restart_ack"}
    assert "?" not in re.search(r'action="([^"]*)"', section).group(1)


def test_r02_recovery_opens_the_existing_clarification_with_the_full_seed_and_writes_nothing(client):
    sid = _single(client)
    before_rows, before_count = _project_rows(sid), _project_count()
    resp = _restart(client, sid)
    assert resp.status_code == 200
    page = resp.get_data(as_text=True)
    assert "data-composition-form" in page and 'name="composition_step" value="1"' in page
    assert _hidden_idea(page) == BOARD_IDEA                 # the full durable seed, not a summary
    assert len(BOARD_IDEA) > 180                            # longer than the trimmed identification
    assert re.search(r'name="composition_answer" value="(yes|no|not_sure)" required(?! checked)', page)
    assert "checked" not in re.search(r'<form method="POST" action="/start" class="composition-form"'
                                      r'.*?</form>', page, re.S).group(0)
    assert _project_count() == before_count and _project_rows(sid) == before_rows


def test_r03_yes_creates_a_separate_project_with_the_full_idea_and_declared_parts_only(client):
    sid = _single(client)
    _answer(client, sid, MECH_ANSWER)                       # the original has its own history
    before_rows, before_records = _project_rows(sid), _record_count(sid)
    assert before_records >= 1
    idea = _hidden_idea(_restart(client, sid).get_data(as_text=True))
    new = _created(_compose(client, idea, focus=MECH, **PARTS))
    assert new != sid
    inputs = _store().load_reconstruction_inputs(new)
    assert inputs["seed_idea_text"] == BOARD_IDEA and inputs["confirmed_domain"] == MECH
    declared = {(s.domain, s.display_name, s.function_text) for s in _store().load_project_subsystems(new)}
    assert declared == {(MECH, PARTS["mech_part_name"], PARTS["mech_part_function"]),
                        (ELEC, PARTS["elec_part_name"], PARTS["elec_part_function"])}
    assert _record_count(new) == 0                          # nothing inherited: no answer, no record
    assert _project_rows(sid) == before_rows                # the original is byte-identical
    assert _store().load_project_subsystems(sid) == ()
    new_page = _raw(client, new)
    assert "data-integrated-scope" in new_page and _section(new_page) is None
    assert _section(_raw(client, sid)) is not None          # the original keeps its offer


def test_r04_the_new_project_reaches_the_existing_919_continuation(client):
    sid = _single(client)
    new = _created(_compose(client, _hidden_idea(_restart(client, sid).get_data(as_text=True)),
                            focus=MECH, **PARTS))
    for value in (MECH_ANSWER, MECH_ANSWER, PF_STRONG, BA_1, BA_2):
        _answer(client, new, value)
    assert _save_part(client, new, _part(new, ELEC),
                      {q: "My own words about it." for q in _ids(ELEC)}).status_code == 200
    assert _kind(_raw(client, new)) == "declare_interaction"


# ==========================================================================
# 2. negative controls — nothing is created
# ==========================================================================
def test_r05_missing_acknowledgement_changes_nothing(client):
    sid = _single(client)
    before = _project_count()
    resp = _restart(client, sid, ack=False)
    assert resp.status_code == 302 and resp.headers["Location"].endswith(
        f"/session/{sid}#integrated-restart")
    assert _project_count() == before


def test_r06_unknown_or_foreign_project_is_denied_generically(client):
    before = _project_count()
    unknown = _restart(client, "00000000-0000-4000-8000-000000000000")
    owner, _aid = _client_for("ijr-owner@example.com")
    owned = _single(owner)
    stranger, _ = _client_for("ijr-stranger@example.com")
    foreign = _restart(stranger, owned)
    anonymous = _restart(client, owned)
    for resp in (unknown, foreign, anonymous):
        assert resp.status_code == 302 and resp.headers["Location"].endswith("/")
        assert "/session/" not in resp.headers["Location"]
        assert b"data-composition-form" not in resp.data
    assert _project_count() == before + 1                   # only the owner's own project
    assert _restart(owner, owned).status_code == 200        # the owner may follow it


def test_r07_a_request_without_the_csrf_token_is_rejected(client):
    sid = _single(client)
    before = _project_count()
    raw = appmod.app.test_client()
    resp = raw.post(f"/session/{sid}/integrated-restart", data={"integrated_restart_ack": "yes"})
    assert resp.status_code in (400, 403) and b"data-composition-form" not in resp.data
    assert _project_count() == before


def test_r08_an_integrated_project_has_no_offer_and_the_route_refuses(client):
    sid = _created(_compose(client, BOARD_IDEA, focus=MECH, **PARTS))
    assert _section(_raw(client, sid)) is None
    before = _project_count()
    resp = _restart(client, sid)
    assert resp.status_code == 409
    assert ui_text.text("UI_IJR_UNAVAILABLE", "en") in _html.unescape(resp.get_data(as_text=True))
    assert b"data-composition-form" not in resp.data and _project_count() == before


@pytest.mark.parametrize("cause", ["seed", "store", "inactive"])
def test_r09_no_eligible_source_offers_nothing_and_refuses(client, monkeypatch, cause):
    sid = _single(client)
    if cause == "seed":
        monkeypatch.setattr(appmod, "_original_idea_text", lambda _sid: None)
    elif cause == "store":
        def _boom(_sid):
            raise RuntimeError("unreadable")
        monkeypatch.setattr(_store(), "load_project_subsystems", _boom)
    else:
        monkeypatch.setattr(domain_activation, "_ACTIVATED_DOMAINS", frozenset({ELEC}))
    if cause != "store":
        assert _section(_raw(client, sid)) is None
    before = _project_count()
    resp = _restart(client, sid)
    assert resp.status_code == 409 and b"data-composition-form" not in resp.data
    assert _project_count() == before


def test_r10_an_unsupported_classification_keeps_the_existing_refusal(client, monkeypatch):
    sid = _single(client)
    monkeypatch.setattr(appmod, "classify_domain", lambda _idea: DomainClassification(
        kind=DomainResultKind.SINGLE, selected_domain="medical_device"))
    before = _project_count()
    resp = _restart(client, sid)
    page = resp.get_data(as_text=True)
    assert "data-composition-form" not in page
    assert _project_count() == before


@pytest.mark.parametrize("answer", ["no", "not_sure", None])
def test_r11_no_not_sure_or_a_missing_answer_creates_nothing(client, answer):
    sid = _single(client)
    idea = _hidden_idea(_restart(client, sid).get_data(as_text=True))
    before, rows = _project_count(), _project_rows(sid)
    resp = _compose(client, idea, answer=answer, focus=MECH, **PARTS)
    assert resp.status_code in (200, 400)
    assert _project_count() == before and _project_rows(sid) == rows
    if answer is not None:
        key = "UI_S15_GUIDE_NO" if answer == "no" else "UI_S15_GUIDE_NOT_SURE"
        assert ui_text.text(key, "en") in _html.unescape(resp.get_data(as_text=True))


def test_r12_a_missing_part_or_focus_creates_nothing(client):
    sid = _single(client)
    idea = _hidden_idea(_restart(client, sid).get_data(as_text=True))
    before = _project_count()
    assert _compose(client, idea, focus=None, **PARTS).status_code == 400
    assert _compose(client, idea, focus=MECH, **dict(PARTS, elec_part_name="")).status_code == 400
    assert _project_count() == before


# ==========================================================================
# 3. Arabic presentation and copy
# ==========================================================================
def test_r13_arabic_page_is_rtl_and_uses_the_arabic_copy(client):
    sid = _single(client, lang="ar")
    page = _raw(client, sid)
    assert re.search(r'<html[^>]*dir="rtl"', page)
    text = _html.unescape(_section(page))
    for key in ("UI_IJR_TITLE", "UI_IJR_NOTE", "UI_IJR_ACK", "UI_IJR_BUTTON"):
        assert ui_text.text(key, "ar") in text
    resp = _restart(client, sid)
    assert resp.status_code == 200 and _hidden_idea(resp.get_data(as_text=True)) == BOARD_IDEA
    assert re.search(r'<html[^>]*dir="rtl"', resp.get_data(as_text=True))


def test_r14_copy_is_bilingual_and_claims_nothing():
    for key in NEW_KEYS:
        assert ui_text.text(key, "en") and ui_text.text(key, "ar")
        assert ui_text.text(key, "en") != ui_text.text(key, "ar")
    note = ui_text.text("UI_IJR_NOTE", "en")
    assert "separate, new integrated project" in note and "none of the answers" in note
    assert "stay exactly as they are" in note
    for word in ("compatib", "validat", "safe", "recommend"):
        assert word not in " ".join(ui_text.text(k, "en") for k in NEW_KEYS).lower()
