# -*- coding: utf-8 -*-
"""G1-UQTR-INTEGRATED-CONTINUATION-01 — while the inventor's own recorded non-answer suppresses
the automatic re-ask of the current point (UQTR-01), an integrated invention is offered the
integrated step the EXISTING guidance owner already derived as ONE secondary link, through the
SAME template rule as the routed-recovery link (G1-ROUTED-RECOVERY-CONTINUATION-01).

Synthetic board-in-enclosure data only, answered in ordinary on-topic words. What is pinned:
  * the UQTR primary action ("Review what is still needed") is unchanged and stays the ONLY
    primary action; the secondary link appears for each suppressing non-answer actually observed
    (specialist / provisional assumption / evidence requested);
  * unknown and deferred keep their existing pause-and-continue behaviour and get no link;
  * eligibility is the rendered suppressed-question state itself, not an action list;
  * no link while an ordinary question is served, on a single-domain project, or when the owner
    derives nothing usable; every target equals the routed-recovery link's for the same step;
  * the voluntary revisit restores ordinary serving; correction keeps its existing semantics;
  * following the steps reaches the existing planar-clearance check and CAD bundle while
    Physical Feasibility stays OPEN with no gap, maturity or record credit;
  * EN / AR copy states the boundary; the Arabic page is RTL.
"""
import html as _html
import re

import pytest

import web.app as appmod
from engine.idea_state import (MECHANISM_COMPLETENESS as MC, PHYSICAL_FEASIBILITY as PF,
                               BOUNDARY_AMBIGUITY as BA)
from engine.progression_loop import compute_non_answer_suppression, deferred_open_gap
from tests.test_stage15_integrated_invention_entry import ELEC, MECH, _compose, _created, _live
from tests.test_g1_integrated_engineering_continuation import (
    IDEA, PARTS, _ifc, _kind, _participate, _primary, _raw, _to_participation, client)  # noqa: F401
from tests.test_28t5_nonfocused_required_part_questions import _ids, _part, _save as _save_part
from tests.test_g1_routed_recovery_continuation import (
    LINK_RE as RRC_LINK_RE, _integrated as _routed_integrated, _to_routed_recovery)
from tests.test_safe_question_routing_pf_q2 import _start as _single_domain
from web import ui_text

UQC_LINK_RE = re.compile(r'<a data-uqc-link data-uqc-kind="([^"]+)" href="([^"]*)"')
SUPPRESSING = ("specialist_requested", "provisional_assumption", "evidence_requested")
PAUSING = ("unknown", "deferred")
# The inventor's own ordinary words about THIS board-in-enclosure idea, cycled per served question.
ORDINARY = (
    "The board sits on four small posts inside the plastic box and is held down with screws, so it "
    "cannot move or rattle.",
    "The plastic box carries the weight of the board. The posts take the load from the board and pass "
    "it to the bottom of the box.",
    "When the box is dropped the posts and screws keep the board from hitting the walls, and there is a "
    "gap all around it.",
    "The board must not touch the walls. I want a few millimetres of space on every side and a hole for "
    "the LED.",
    "The device sits on a desk indoors at room temperature. It is not meant to get wet or be used outside.",
    "The temperature sensor is on the board and measures the air in the box; when it gets warm the board "
    "turns the LED on.",
    "It runs from a USB cable plugged into the side of the box. Nothing in the box moves.",
)


def _token(page):
    return _html.unescape(re.search(r'name="answer_token" value="([^"]*)"', page).group(1))


def _post(c, sid, **data):
    page = _raw(c, sid)
    data.setdefault("answer_token", _token(page))
    return c.post(f"/session/{sid}", data=data)


def _href(page):
    return _html.unescape(re.search(r'data-primary-action[^>]*href="([^"]*)"', _primary(page)).group(1))


def _links(page):
    return [(k, _html.unescape(h)) for k, h in UQC_LINK_RE.findall(page)]


def _integrated(c, focus=ELEC, lang=None):
    return _created(_compose(c, IDEA, focus=focus, lang=lang, **PARTS))


def _to_open_pf(c, sid):
    """Answer the served questions in ordinary words until Physical Feasibility is the open point."""
    for text in ORDINARY * 2:
        state = _live(sid)
        if state.get_gap(PF) is not None:
            break
        assert _post(c, sid, response=text).status_code == 302
    state = _live(sid)
    assert state.get_gap(MC).status == "CLOSED" and state.get_gap(PF).status == "OPEN"
    return state


def _suppressed(c, sid, action):
    _to_open_pf(c, sid)
    assert _post(c, sid, action=action, response="I need to find out more about this.").status_code == 302
    suppression = compute_non_answer_suppression(_live(sid))
    assert suppression is not None and suppression.gap_type == PF and suppression.disposition == action
    return _raw(c, sid)


def _snapshot(sid):
    state = _live(sid)
    return (state.maturity_level, [(g.gap_type, g.status) for g in state.gaps],
            tuple(r.record_id for r in state.assertions),
            len(appmod._get_store().load_contract(sid).assertions))


def _deliverable(sid):
    return f"/session/{sid}/deliverable"


# ==========================================================================
# 1-2. each suppressing non-answer: the unchanged primary plus ONE secondary link
# ==========================================================================
@pytest.mark.parametrize("action", SUPPRESSING)
def test_01_each_suppressing_non_answer_keeps_its_primary_and_gets_one_secondary_step(client, action):
    sid = _integrated(client)
    page = _suppressed(client, sid, action)
    assert _href(page) == _deliverable(sid)                         # the unchanged UQTR primary
    text = _html.unescape(page)
    assert ui_text.text("UI_UQTR_JOURNEY_NOTE", "en") in text
    assert ui_text.text("UI_UQTR_CTA", "en") in text
    expected = "/session/%s/part-questions?part=%s" % (sid, _part(sid, MECH))
    assert _links(page) == [("part_questions", expected)]
    assert ui_text.text("UI_UQC_NOTE", "en") in text
    assert ui_text.text("UI_IJG_PART_CTA_MECH", "en") in text
    assert page.count("data-uqc-link") == 1 and "data-uqc-link data-primary-action" not in page
    assert "data-rrc" not in page and "data-ijg-action" not in page
    assert 'class="uqtr-revisit"' in page                           # the question stays revisitable
    assert _live(sid).get_gap(PF).status == "OPEN"


@pytest.mark.parametrize("action", PAUSING)
def test_02_unknown_and_deferred_keep_pause_and_continue_and_get_no_link(client, action):
    sid = _integrated(client)
    _to_open_pf(client, sid)
    assert _post(client, sid, action=action, response="").status_code == 302
    state = _live(sid)
    assert compute_non_answer_suppression(state) is None             # paused, not suppressed
    page = _raw(client, sid)
    assert _href(page) == "#response" and "data-uqc" not in page      # the next point is served
    assert deferred_open_gap(state) == BA and state.get_gap(PF).status == "OPEN"
    # pausing the next point too reaches the existing integrated primary step, still with no link
    assert _post(client, sid, action=action, response="").status_code == 302
    page = _raw(client, sid)
    assert _kind(page) == "part_questions" and "data-uqc" not in page


def test_03_eligibility_is_the_rendered_suppressed_state_not_an_action_list(client, monkeypatch):
    """A recorded state that suppresses with another disposition (e.g. an older project where
    unknown suppresses) is served by the same branch and gets the same link."""
    sid = _integrated(client)
    page = _suppressed(client, sid, "specialist_requested")
    expected = _links(page)
    from engine.progression_loop import NonAnswerSuppression
    monkeypatch.setattr(appmod, "compute_non_answer_suppression",
                        lambda _s: NonAnswerSuppression(gap_type=PF, disposition="unknown",
                                                        record_id="rec_x"))
    page = _raw(client, sid)
    assert _href(page) == _deliverable(sid) and _links(page) == expected


# ==========================================================================
# 3. no link where nothing is suppressed or the owner offers nothing usable
# ==========================================================================
def test_04_no_link_while_an_ordinary_question_is_served(client):
    sid = _integrated(client)
    page = _raw(client, sid)
    assert 'id="answer-form"' in page and _href(page) == "#response"
    assert "data-uqc" not in page
    _to_open_pf(client, sid)
    page = _raw(client, sid)
    assert _href(page) == "#response" and "data-uqc" not in page


@pytest.mark.parametrize("forced", [None, "declare_interaction"])
def test_05_single_domain_suppressed_question_gets_no_link(client, monkeypatch, forced):
    sid = _single_domain(client)
    assert _post(client, sid, action="specialist_requested", response="").status_code == 302
    assert compute_non_answer_suppression(_live(sid)) is not None
    if forced:   # even a forced kind finds no interaction form on a single-domain page
        monkeypatch.setattr(appmod, "_integrated_journey_guidance",
                            lambda *_a, **_k: {"kind": forced, "clearance": []})
    page = _raw(client, sid)
    assert _href(page) == _deliverable(sid)
    assert "data-uqc" not in page


@pytest.mark.parametrize("derived", [None, {"kind": None, "clearance": []},
                                     {"kind": "unknown_kind", "clearance": []}])
def test_06_nothing_usable_from_the_owner_means_no_link(client, monkeypatch, derived):
    sid = _integrated(client)
    _suppressed(client, sid, "specialist_requested")
    monkeypatch.setattr(appmod, "_integrated_journey_guidance", lambda *_a, **_k: derived)
    page = _raw(client, sid)
    assert _href(page) == _deliverable(sid)
    assert "data-uqc" not in page


def test_07_no_component_link_when_the_inventory_cannot_take_another(client, monkeypatch):
    sid = _integrated(client)
    _suppressed(client, sid, "specialist_requested")
    monkeypatch.setattr(appmod, "_integrated_journey_guidance",
                        lambda *_a, **_k: {"kind": "component_inventory", "clearance": []})
    original = appmod._component_inventory_context

    def full(*a, **k):
        view = original(*a, **k)
        return dict(view, can_add=False) if view else view
    monkeypatch.setattr(appmod, "_component_inventory_context", full)
    page = _raw(client, sid)
    assert _href(page) == _deliverable(sid) and "data-uqc" not in page


@pytest.mark.parametrize("kind", ["part_questions", "declare_interaction", "component_inventory",
                                  "participation", "interface_preparation"])
def test_08_each_target_equals_the_routed_recovery_link_for_the_same_step(client, monkeypatch, kind):
    """One selection rule: the UQTR link and the #946 routed-recovery link are the same macro, so
    for the same derived step they carry the same kind and target (the routed link's parity with
    each step's own primary branch is pinned by the #946 tests)."""
    uqtr_sid = _integrated(client, focus=MECH)
    _suppressed(client, uqtr_sid, "specialist_requested")
    routed_sid = _routed_integrated(client)
    _to_routed_recovery(client, routed_sid)

    def rendered(sid, pattern):
        real = appmod._integrated_journey_guidance(sid, appmod._integrated_scope_context(_live(sid)))
        guidance = dict(real) if kind == "part_questions" else {"kind": kind, "clearance": []}
        with monkeypatch.context() as m:
            m.setattr(appmod, "_integrated_journey_guidance", lambda *_a, **_k: guidance)
            [(k, h)] = pattern.findall(_raw(client, sid))
        return k, re.sub(r"part=sub-[0-9a-f]+", "part=<part>", _html.unescape(h).replace(sid, "<sid>"))

    assert rendered(uqtr_sid, UQC_LINK_RE) == rendered(routed_sid, RRC_LINK_RE)


def test_09_the_routed_recovery_branch_is_unchanged(client):
    sid = _routed_integrated(client)
    _to_routed_recovery(client, sid)
    page = _raw(client, sid)
    assert _href(page) == "#routed-recovery"
    assert len(RRC_LINK_RE.findall(page)) == 1 and "data-uqc" not in page
    assert ui_text.text("UI_RRC_NOTE", "en") in _html.unescape(page)


# ==========================================================================
# 4. revisit and correction keep their existing semantics
# ==========================================================================
def test_10_the_voluntary_revisit_restores_ordinary_serving_and_removes_the_link(client):
    sid = _integrated(client)
    assert _links(_suppressed(client, sid, "specialist_requested"))
    assert _post(client, sid, action="answered", response=ORDINARY[4]).status_code == 302
    assert compute_non_answer_suppression(_live(sid)) is None
    page = _raw(client, sid)
    assert _href(page) == "#response" and "data-uqc" not in page
    # the revisit answer goes through the canonical answered path, whatever it earns there
    assert _live(sid).get_gap(PF).status != "CLOSED"


def test_11_correction_keeps_its_existing_replay_and_the_link_follows_the_replayed_state(client):
    """Correcting an earlier answer runs the EXISTING full deterministic replay; whatever state it
    derives, the link is shown exactly when the suppressed-question branch is."""
    sid = _integrated(client)
    _suppressed(client, sid, "specialist_requested")
    earlier = [r for r in _live(sid).assertions if r.disposition == "answered"
               and r.superseded_by is None][-1]
    response = client.post(f"/session/{sid}/correct", data={
        "supersedes_record_id": earlier.record_id, "response": ORDINARY[6],
        "answer_token": _token(_raw(client, sid))})
    assert response.status_code == 302
    state = _live(sid)
    assert state.assertions[[r.record_id for r in state.assertions].index(earlier.record_id)].superseded_by
    page = _raw(client, sid)
    if compute_non_answer_suppression(state) is None:
        assert _href(page) != _deliverable(sid) and "data-uqc" not in page
    else:
        assert _href(page) == _deliverable(sid) and len(_links(page)) == 1


# ==========================================================================
# 5. the existing engineering journey, reached while the point stays open
# ==========================================================================
def test_12_following_the_steps_reaches_clearance_and_cad_while_pf_stays_open(client):
    from tests.test_board_enclosure_planar_clearance import _save as save_clearance
    from tests.test_board_enclosure_cad_download import _bundle as cad_bundle, _link as cad_link

    sid = _integrated(client)
    page = _suppressed(client, sid, "specialist_requested")
    pf_before = (_live(sid).get_gap(PF).status, _live(sid).maturity_level)
    record_ids_before = tuple(r.record_id for r in _live(sid).assertions)

    [(kind, href)] = _links(page)
    assert kind == "part_questions" and client.get(href).status_code == 200
    seen = [kind]
    assert _save_part(client, sid, _part(sid, MECH),
                      {q: "My own words about it." for q in _ids(MECH)}).status_code == 200
    seen.append(_links(_raw(client, sid))[0][0])
    _to_participation(client, sid)
    seen.append(_links(_raw(client, sid))[0][0])
    ids = _participate(client, sid)
    [(kind, href)] = _links(_raw(client, sid))
    seen.append(kind)
    assert seen == ["part_questions", "declare_interaction", "participation", "interface_preparation"]

    preparation = client.get(href).get_data(as_text=True)
    interface_id = _ifc(sid)
    assert f"/session/{sid}/interface-clearance/{interface_id}" in preparation
    saved = save_clearance(client, sid, interface_id, ids)
    assert saved.status_code == 200
    url = cad_link(saved.get_data(as_text=True))
    assert url
    files, _ = cad_bundle(client.get(url))
    assert set(files) == {"geometry.dxf", "companion.json", "README.txt"}

    page = _raw(client, sid)
    assert _href(page) == _deliverable(sid)
    state = _live(sid)
    assert (state.get_gap(PF).status, state.maturity_level) == pf_before == ("OPEN", pf_before[1])
    assert tuple(r.record_id for r in state.assertions) == record_ids_before
    assert compute_non_answer_suppression(state).disposition == "specialist_requested"


def test_13_rendering_and_following_the_link_change_nothing(client):
    sid = _integrated(client)
    page = _suppressed(client, sid, "provisional_assumption")
    before = _snapshot(sid)
    [(kind, href)] = _links(page)
    assert client.get(href).status_code == 200
    _raw(client, sid)
    assert _snapshot(sid) == before


# ==========================================================================
# 6. copy and Arabic
# ==========================================================================
def test_14_copy_is_bilingual_and_states_the_boundary():
    en, ar = ui_text.text("UI_UQC_NOTE", "en"), ui_text.text("UI_UQC_NOTE", "ar")
    assert en and ar and en != ar
    for phrase in ("Optional", "does not answer or resolve the point",
                   "return to its question at any time", "stays your own statement",
                   "none of it validates the design", "shows that the idea is ready"):
        assert phrase in en, phrase
    for word in ("specialist", "risk", "recommend", "safe"):
        assert word not in en.lower(), word
    for phrase in ("اختياري", "لا يجيب عن النقطة ولا يحلّها", "العودة إلى سؤالها", "تصريحك أنت",
                   "صحة التصميم", "توافق الأجزاء", "جاهزة"):
        assert phrase in ar, phrase
    assert not re.search(r"[A-Za-z]", ar)


def test_15_arabic_page_is_rtl_with_the_arabic_link(client):
    sid = _integrated(client, lang="ar")
    page = _suppressed(client, sid, "evidence_requested")
    assert re.search(r'<html[^>]*dir="rtl"', page)
    text = _html.unescape(page)
    assert ui_text.text("UI_UQC_NOTE", "ar") in text
    assert ui_text.text("UI_IJG_PART_CTA_MECH", "ar") in text
    assert ui_text.text("UI_UQTR_CTA", "ar") in text
    assert len(_links(page)) == 1
