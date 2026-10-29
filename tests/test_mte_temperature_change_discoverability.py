# -*- coding: utf-8 -*-
"""MTE-TEMPERATURE-CHANGE-DISCOVERABILITY-01 (Increment C) — directly owning tests.

The session page presents the free linear thermal-expansion contract §1A
relevance beside the inventor's CURRENT part temperature-change statement, and
moves the ONE existing link to that method there, only while the statement and
the method's own gate (``_calc_gate(sid, _mte)``) name the exact same
``subsystem_id``. Otherwise the existing general link behaves exactly as
before. The link carries no value; the method page and its submission re-read
their own gate. Synthetic data only.
"""
import html
import os
import re
import sqlite3

import pytest

import web.app as webapp
from web import ui_text
from engine import mechanical_thermal_expansion as te
from engine import subsystem_model as sm
from tests.test_cap12_form_mockup_advisory import _client_for, _start, _page, SEED
from tests.test_cap13_therm01_integrated_part_eligibility import (
    _integrated, MECH, ELEC, CTRL)
from tests.test_part_temperature_change_declaration import (
    _declare, _withdraw, _parts)

DEST = "/session/%s/thermal-expansion"
CONTEXT = re.compile(r'<dd[^>]*data-part-tc=.*?</dd>', re.S)


def _links(body, sid):
    """Every link to the free-expansion page, with its exact href."""
    return re.findall(r'href="(/session/%s/thermal-expansion[^"]*)"' % re.escape(sid), body)


def _view(body, sid):
    links = _links(body, sid)
    block = CONTEXT.search(body)
    block = block.group(0) if block else ""
    return {"links": links,
            "relevance": "data-mte-tc-relevance" in body,
            "in_block": "data-mte-tc-relevance" in block and "data-mte-link-context" in block,
            "general": bool(re.search(r'<p class="journey-note" data-mte-link ', body))}


def _sql(statement, foreign_keys=True):
    with sqlite3.connect(os.environ["INVENTORAI_DB_PATH"]) as connection:
        if not foreign_keys:
            connection.execute("PRAGMA foreign_keys = OFF")
        connection.execute(statement)


# ==========================================================================
# 1. the journey: one link, moved while the relevance holds
# ==========================================================================
@pytest.mark.parametrize("focus", (ELEC, MECH))
def test_relevance_appears_only_while_the_statement_is_current(focus):
    c, _aid = _client_for("mte-tc-journey-%s@example.com" % focus)
    sid = _integrated(c, focus)
    mech = _parts(sid)[MECH]

    before = _view(_page(c, sid), sid)
    assert before == {"links": [DEST % sid], "relevance": False,
                      "in_block": False, "general": True}

    _declare(c, sid, mech)
    declared = _view(_page(c, sid), sid)
    assert declared == {"links": [DEST % sid], "relevance": True,
                        "in_block": True, "general": False}

    _withdraw(c, sid, mech)
    assert _view(_page(c, sid), sid) == before


def test_three_part_composition_still_shows_exactly_one_link():
    c, _aid = _client_for("mte-tc-three@example.com")
    sid = _integrated(c, ELEC, **CTRL)
    _declare(c, sid, _parts(sid)[MECH])
    view = _view(_page(c, sid), sid)
    assert view["links"] == [DEST % sid] and view["in_block"] and not view["general"]


def test_mechanical_root_project_keeps_the_general_link_unchanged():
    c, _aid = _client_for("mte-tc-root@example.com")
    sid = _start(c, {"idea": SEED, "domain_confirm": MECH})
    body = _page(c, sid)
    assert "data-part-tc" not in body
    assert _view(body, sid) == {"links": [DEST % sid], "relevance": False,
                                "in_block": False, "general": True}


# ==========================================================================
# 2. exact identity and fail-closed cases
# ==========================================================================
def test_another_projects_statement_creates_no_relevance():
    c, _aid = _client_for("mte-tc-cross@example.com")
    a = _integrated(c, ELEC)
    b = _integrated(c, ELEC)
    _declare(c, a, _parts(a)[MECH])
    assert _view(_page(c, b), b)["relevance"] is False
    # a's statement never matches b's gate part
    view_a = webapp._part_temperature_change_context(a, {})
    assert view_a["declared"] is True
    assert webapp._mte_tc_relevance(view_a, webapp._calc_gate(b, te)) is False
    assert webapp._mte_tc_relevance(view_a, webapp._calc_gate(a, te)) is True


def test_unavailable_statement_gives_no_relevance_and_keeps_the_general_link():
    c, _aid = _client_for("mte-tc-unavailable@example.com")
    sid = _integrated(c, ELEC)
    parts = _parts(sid)
    _declare(c, sid, parts[MECH])
    # a non-Mechanical row makes the whole statement collection unreadable
    _sql("INSERT INTO subsystem_temperature_change_declarations VALUES ('%s', '%s')"
         % (sid, parts[ELEC]))
    body = _page(c, sid)
    assert 'data-part-tc="unavailable"' in body
    assert _view(body, sid) == {"links": [DEST % sid], "relevance": False,
                                "in_block": False, "general": True}


def test_corrupt_composition_gives_no_relevance_and_no_link():
    c, _aid = _client_for("mte-tc-corrupt@example.com")
    sid = _integrated(c, ELEC)
    _declare(c, sid, _parts(sid)[MECH])
    _sql("UPDATE project_subsystems SET display_name = ' padded' WHERE subsystem_seq = 0")
    assert webapp._calc_gate(sid, te) == (False, None)
    assert webapp._mte_tc_relevance(
        webapp._part_temperature_change_context(sid, {}), webapp._calc_gate(sid, te)) is False
    r = c.get("/session/%s" % sid)
    body = r.get_data(as_text=True)
    assert "data-mte-tc-relevance" not in body and not _links(body, sid)


def test_the_helper_requires_exact_identity_and_a_current_statement():
    mech = sm.declared_subsystem(MECH, "Hinge", "Swings the window")
    elec = sm.declared_subsystem(ELEC, "Driver", "Switches power")
    other = sm.declared_subsystem(MECH, "Hinge", "Swings the window")
    ok = {"status": "ok", "part_id": mech.subsystem_id, "declared": True}
    assert webapp._mte_tc_relevance(ok, (True, mech)) is True
    for part_tc, gate in (
            (dict(ok, declared=False), (True, mech)),              # not declared / withdrawn
            ({"status": "unavailable"}, (True, mech)),             # unreadable statement
            (None, (True, mech)),                                  # no Stage-15 parts
            (ok, (False, mech)),                                   # gate refuses
            (ok, (True, None)),                                    # gate names no part
            (ok, (1, mech)),                                       # never truthy-coerced
            (ok, (True, other)),                                   # same domain, other part
            (ok, (True, elec)),                                    # non-Mechanical part
            (dict(ok, part_id=elec.subsystem_id), (True, elec)),   # non-Mechanical target
            (dict(ok, part_id=mech.display_name), (True, mech)),   # a name is not an identity
            (dict(ok, part_id=""), (True, mech)),
            (ok, None), (ok, (True,)), ("declared", (True, mech))):
        assert webapp._mte_tc_relevance(part_tc, gate) is False


# ==========================================================================
# 3. the destination: no value carried, its own gate re-read
# ==========================================================================
def test_the_link_carries_nothing_and_the_destination_revalidates():
    c, _aid = _client_for("mte-tc-destination@example.com")
    sid = _integrated(c, ELEC)
    _declare(c, sid, _parts(sid)[MECH])
    body = _page(c, sid)
    assert _links(body, sid) == [DEST % sid]          # no query string, no part id
    page = c.get(DEST % sid).get_data(as_text=True)
    assert "data-mte-form" in page and "data-part-tc" not in page
    # nothing is pre-filled or pre-selected by the relevance
    assert not re.search(r'name="value_[a-zA-Z_]+"[^>]*value="[^"]+"', page)
    assert not re.search(r'<input[^>]*type="radio"[^>]*checked', page)
    # a later composition defect: the stale session page grants nothing there
    _sql("UPDATE project_subsystems SET display_name = ' padded' WHERE subsystem_seq = 0")
    for r in (c.get(DEST % sid), c.post(DEST % sid, data={})):
        assert "data-mte-form" not in r.get_data(as_text=True)


# ==========================================================================
# 4. wording
# ==========================================================================
@pytest.mark.parametrize("lang", ("en", "ar"))
def test_relevance_wording_in_both_languages(lang):
    c, _aid = _client_for("mte-tc-lang-%s@example.com" % lang)
    sid = _integrated(c, ELEC)
    if lang == "ar":
        c.post("/ui-language", data={"lang": "ar"})
    _declare(c, sid, _parts(sid)[MECH])
    body = _page(c, sid)
    text = html.unescape(CONTEXT.search(body).group(0))
    assert ui_text.text("UI_MTE_TC_RELEVANCE", lang) in text
    assert ui_text.text("UI_MTE_LINK_TEXT", lang) in text
    if lang == "ar":
        assert 'dir="rtl"' in body


def test_wording_keeps_relevance_apart_from_applicability():
    en = ui_text.text("UI_MTE_TC_RELEVANCE", "en")
    ar = ui_text.text("UI_MTE_TC_RELEVANCE", "ar")
    for phrase in ("Because you stated", "may help", "possible free change",
                   "only from your own statement", "InventorAI has not checked",
                   "does not mean that the calculation's model applies",
                   "its own conditions", "only values you enter",
                   "not a recommendation of a design solution"):
        assert phrase in en, phrase
    for phrase in ("لأنك صرّحت", "قد يساعدك", "محتمل", "من تصريحك أنت فقط",
                   "ولم يتحقق منه InventorAI", "لا يعني ذلك أن نموذج الحساب ينطبق",
                   "شروطه الخاصة", "إلا القيم التي تُدخلها أنت", "ليس توصية"):
        assert phrase in ar, phrase
    lowered = en.lower()
    for banned in ("you should", "will expand", "applies to your part.", "is suitable",
                   "needs a gap", "clearance", "is safe", "validated"):
        assert banned not in lowered, banned


# ==========================================================================
# 5. scope: no other owner gains the relationship
# ==========================================================================
def test_only_the_session_surface_presents_the_relationship():
    from pathlib import Path
    root = Path(__file__).resolve().parent.parent
    for path in sorted((root / "engine").glob("*.py")):
        assert "_mte_tc_relevance" not in path.read_text(encoding="utf-8"), path.name
        assert "UI_MTE_TC_RELEVANCE" not in path.read_text(encoding="utf-8"), path.name
    templates = [p.name for p in (root / "web" / "templates").glob("*.html")
                 if "mte_tc_relevance" in p.read_text(encoding="utf-8")]
    assert templates == ["session.html"]
    handoff = (root / "engine" / "functional_need_handoff.py").read_text(encoding="utf-8")
    assert "THERMAL" not in handoff and "_mte" not in handoff
