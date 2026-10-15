# -*- coding: utf-8 -*-
"""EXPERIMENT-PLANNING-JOURNEY-GUIDANCE-01 — the Project Compass "What to do now" leads the inventor to the
EXISTING experiment-planning page once every earlier primary action (the two integrated-journey steps
included) is exhausted, while a CURRENT proposed Section-11 experiment has no SAVED success criterion or no
SAVED measurement method.

Proves: the branch sits after every existing branch and before the handoff; exactly ONE primary action; the
current experiments come from the canonical Section-11 owner (``current_experiment_ids``); the step needs a
missing criterion OR method and disappears once every experiment has both; recorded execution results play
no part; no experiment / no durable planning storage / anything unreadable keeps the unchanged handoff; the
step is evaluated lazily (an earlier primary action never pays for it); the handoff stays one click away; a
GET writes nothing and the report is untouched; EN / AR copy says planning is optional and nothing is
checked or validated. Synthetic data only.
"""
import html as _html
import re
import sqlite3

import pytest

import web.app as appmod
from engine.deliverable_assembler import assemble_deliverable, current_experiment_ids
from tests.test_safe_question_routing_pf_q2 import (  # noqa: F401  (fixture)
    BA_1, BA_2, MECH, PF_STRONG, _answer, _live, _start, client)
from tests.test_stage19_durable_success_criteria import PREFIX
from web import ui_text

METHOD = "method__"
KEYS = ("UI_EPG_NOTE", "UI_EPG_CTA")


def _raw(c, sid):
    r = c.get(f"/session/{sid}")
    assert r.status_code == 200, r.status_code
    return r.get_data(as_text=True)


def _primary(page):
    found = re.findall(r'<(?:a|button) class="journey-primary" data-primary-action[^>]*>', page)
    assert len(found) == 1, found
    return found[0]


def _finished(c, lang="en"):
    """A single-domain Mechanical journey whose questions are exhausted; its Section-11 plan proposes
    experiments and nothing is planned yet."""
    sid = _start(c, lang=lang)
    for value in (MECH, MECH, PF_STRONG, BA_1, BA_2):
        _answer(c, sid, value)
    return sid


def _ids(sid):
    return current_experiment_ids(_live(sid))


def _plan(c, sid, criteria=None, methods=None):
    data = {PREFIX + k: v for k, v in (criteria or {}).items()}
    data.update({METHOD + k: v for k, v in (methods or {}).items()})
    r = c.post(f"/session/{sid}/success-criteria", data=data)
    assert r.status_code == 302, r.status_code


def _is_planning_step(page, sid):
    primary = _primary(page)
    if "data-epg-action" not in primary:
        return False
    assert f'href="/session/{sid}/success-criteria"' in primary
    handoff = re.search(r'<p class="journey-note" data-epg-handoff>.*?</p>', page, re.S).group(0)
    assert f'href="/session/{sid}/deliverable"' in handoff and "data-primary-action" not in handoff
    return True


def _is_handoff(page, sid):
    primary = _primary(page)
    return (f'href="/session/{sid}/deliverable"' in primary and "data-epg" not in page)


# ---------------------------------------------------------------------------
# 1. the canonical owner and the step itself
# ---------------------------------------------------------------------------
def test_01_current_experiments_come_from_the_canonical_section_11_owner(client):
    sid = _finished(client)
    ids = _ids(sid)
    assert ids and len(set(ids)) == len(ids)
    plan = assemble_deliverable(_live(sid))["section_11_prototype_test_plan"]
    assert ids == tuple(item["experiment_id"] for item in plan["items"])


def test_02_unplanned_experiments_make_the_planning_step_the_one_primary_action(client):
    sid = _finished(client)
    page = _raw(client, sid)
    assert _is_planning_step(page, sid)
    do = _html.unescape(page[page.index('data-pc-row="do"'):page.index("</section>", page.index('data-pc-row="do"'))])
    assert ui_text.text("UI_EPG_CTA", "en") in do and ui_text.text("UI_EPG_NOTE", "en") in do
    assert do.count("data-primary-action") == 1
    r = client.get(f"/session/{sid}/success-criteria")                # the existing page, unchanged
    assert r.status_code == 200


def test_03_a_missing_criterion_or_method_keeps_the_step_until_every_experiment_has_both(client):
    sid = _finished(client)
    ids = _ids(sid)
    _plan(client, sid, criteria={eid: "It holds for one minute" for eid in ids})
    assert _is_planning_step(_raw(client, sid), sid)                 # methods still missing
    _plan(client, sid, methods={eid: "Time it with a stopwatch" for eid in ids[:-1]})
    assert _is_planning_step(_raw(client, sid), sid)                 # the last method missing
    _plan(client, sid, methods={ids[-1]: "Watch it for one minute"})
    assert _is_handoff(_raw(client, sid), sid)                       # all planned: unchanged handoff
    _plan(client, sid, criteria={ids[0]: ""})                        # a criterion cleared again
    assert _is_planning_step(_raw(client, sid), sid)


def test_04_recorded_execution_results_play_no_part(client):
    sid = _finished(client)
    ids = _ids(sid)
    _plan(client, sid, criteria={eid: "It holds" for eid in ids}, methods={eid: "Watch it" for eid in ids})
    assert _is_handoff(_raw(client, sid), sid)                       # no result recorded, no nudge


# ---------------------------------------------------------------------------
# 2. precedence and laziness
# ---------------------------------------------------------------------------
def test_05_an_earlier_primary_action_wins_and_never_evaluates_the_step(client, monkeypatch):
    calls = []
    real = appmod._experiment_planning_guidance

    def spy(sid, state):
        calls.append(sid)
        return real(sid, state)
    monkeypatch.setattr(appmod, "_experiment_planning_guidance", spy)
    sid = _start(client)
    page = _raw(client, sid)
    assert 'href="#response"' in _primary(page) and "data-epg" not in page
    assert calls == []                                               # lazy: never reached
    for value in (MECH, MECH, PF_STRONG, BA_1, BA_2):
        _answer(client, sid, value)
    assert _is_planning_step(_raw(client, sid), sid)
    assert calls                                                      # evaluated at the end of the chain


def test_06_integrated_steps_come_first(client):
    from tests.test_integrated_journey_guidance import _finished_focus
    sid = _finished_focus(client)
    assert _ids(sid)                                                  # unplanned experiments exist ...
    page = _raw(client, sid)
    assert 'data-ijg-action="part_questions"' in _primary(page)      # ... yet the integrated step leads
    assert "data-epg" not in page


def test_07_the_branch_sits_after_the_integrated_branches_and_before_the_handoff():
    with open("web/templates/session.html", encoding="utf-8") as fh:
        tpl = fh.read()
    do = tpl[tpl.index('data-pc-row="do"'):tpl.index("</section>", tpl.index('data-pc-row="do"'))]
    prep = do.index("{% elif integrated_guidance and integrated_guidance.kind == 'interface_preparation' %}")
    epg = do.index("{% elif experiment_planning_step is defined and experiment_planning_step() %}")
    fallback = do.index("{% else %}", epg)
    assert prep < epg < fallback and "UI_A1_REVIEW_HANDOFF" in do[fallback:]


# ---------------------------------------------------------------------------
# 3. fail closed
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("target", ["_current_experiment_ids", "_durable_success_criteria",
                                    "_durable_measurement_methods"])
def test_08_anything_unreadable_keeps_the_unchanged_handoff(client, monkeypatch, target):
    sid = _finished(client)

    def boom(*_a, **_k):
        raise RuntimeError("unreadable")
    monkeypatch.setattr(appmod, target, boom)
    page = _raw(client, sid)
    assert _is_handoff(page, sid)


def test_09_no_experiment_or_no_durable_planning_storage_keeps_the_handoff(client, monkeypatch):
    sid = _finished(client)
    monkeypatch.setattr(appmod, "_current_experiment_ids", lambda state: ())
    assert _is_handoff(_raw(client, sid), sid)
    monkeypatch.undo()
    monkeypatch.setattr(appmod, "_durable_success_criteria", lambda sid: None)
    assert _is_handoff(_raw(client, sid), sid)
    assert appmod._experiment_planning_guidance(sid, _live(sid)) is False


# ---------------------------------------------------------------------------
# 4. nothing written; report untouched; copy
# ---------------------------------------------------------------------------
def test_10_a_get_writes_nothing_and_the_report_carries_no_step(client):
    sid = _finished(client)
    _raw(client, sid)
    con = sqlite3.connect(appmod.os.environ["INVENTORAI_DB_PATH"])
    try:
        before = list(con.iterdump())
        page = _raw(client, sid)
        assert _is_planning_step(page, sid)
        assert list(con.iterdump()) == before
    finally:
        con.close()
    report = client.get(f"/session/{sid}/deliverable").get_data(as_text=True)
    assert "data-epg" not in report and ui_text.text("UI_EPG_CTA", "en") not in _html.unescape(report)


def test_11_arabic_page_is_rtl_with_the_same_step(client):
    sid = _finished(client, lang="ar")
    page = _raw(client, sid)
    assert 'dir="rtl"' in page and _is_planning_step(page, sid)
    text = _html.unescape(page)
    assert ui_text.text("UI_EPG_CTA", "ar") in text and ui_text.text("UI_EPG_NOTE", "ar") in text


def test_12_the_copy_is_bilingual_optional_and_claims_nothing():
    for key in KEYS:
        assert ui_text.has_string(key), key
    note = ui_text.text("UI_EPG_NOTE", "en").lower()
    for phrase in ("optional", "has not checked or validated", "does not show that the idea works"):
        assert phrase in note
    for word in ("verified", "feasible", "recommend", "ready", "safe"):
        assert word not in note
