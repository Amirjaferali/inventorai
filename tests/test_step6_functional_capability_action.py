# -*- coding: utf-8 -*-
"""Step 6 (current six-step plan) — functional-to-qualified-engineering action
continuity on the existing FUNCTIONAL-NEED-TO-CAPABILITY-HANDOFF-01 view.

A PROPOSED provisional reading may show ONE plain link to the EXISTING page of a
related owner, only when that owner's OWN gate (read by
``_handoff_capabilities``) already permits the workflow for the project's
durable state: CAP-13 support reactions for SCREEN_SUPPORT when ``_calc_gate``
is eligible, CAP-09 experiment planning for WATERING / FAN when the canonical
Section-11 owner has current experiments. The link carries nothing; the
destination re-reads its gate on arrival; no value, answer or declaration comes
from the reading. Synthetic invention data only.
"""
import html
import re

import pytest

import web.app as webapp
from engine import cap13_static_reactions as cap13
from engine import functional_need_handoff as fh
from tests.test_cap12_form_mockup_advisory import _client_for, _page
from tests.test_cap13_static_reactions import _form as _cap13_form
from tests.test_cap13_therm01_integrated_part_eligibility import (
    ELEC, MECH, _corrupt, _integrated, _reactions)
from tests.test_functional_need_handoff import _section, _start
from tests.test_safe_question_routing_pf_q2 import (  # noqa: F401  (fixture)
    BA_1, BA_2, MECH as MECH_ANSWER, PF_STRONG, SEED, _answer, _live,
    _start as _start_mech, client)
from web import ui_text

SCREEN_EN = "I want a stand that holds my monitor above my desk."
SCREEN_AR = ("أريد حاملًا خشبيًا يرفع شاشة الحاسوب فوق مكتبي حتى تكون "
             "في مستوى النظر بدون براغي")
WATER_EN = "I want a device that waters my plants automatically."
CAP13_URL = "/session/%s/support-reactions"
CAP13_ACTION = 'data-fh-action="CAP13_CONDITIONAL_REACTIONS"'
CAP09_ACTION = 'data-fh-action="CAP09_EXPERIMENT_PLANNING"'


def _actions(section):
    return re.findall(r'<a data-fh-action="([A-Z0-9_]+)" href="([^"]*)"', section or "")


# ==========================================================================
# 1. the action rule itself
# ==========================================================================
def test_action_only_for_a_proposed_role_and_a_permitting_owner_state():
    cases = [
        (fh.PROPOSED, fh.CAP13_CONDITIONAL_REACTIONS, "CONDITIONAL", "cap13_support_reactions"),
        (fh.PROPOSED, fh.CAP09_EXPERIMENT_PLANNING, "AVAILABLE", "success_criteria"),
        (fh.PROPOSED, fh.CAP13_CONDITIONAL_REACTIONS, "NOT_FOR_PROJECT", None),
        (fh.PROPOSED, fh.CAP13_CONDITIONAL_REACTIONS, "UNAVAILABLE", None),
        (fh.PROPOSED, fh.CAP09_EXPERIMENT_PLANNING, "NO_EXPERIMENTS", None),
        (fh.PROPOSED, fh.CAP09_EXPERIMENT_PLANNING, "UNAVAILABLE", None),
        (fh.CONFLICTING, fh.CAP13_CONDITIONAL_REACTIONS, "CONDITIONAL", None),
        (fh.CONFLICTING, fh.CAP09_EXPERIMENT_PLANNING, "AVAILABLE", None),
        (fh.PROPOSED, "SOMETHING_ELSE", "CONDITIONAL", None),
    ]
    for status, ref, state, expected in cases:
        items = webapp._handoff_actions(status, [{"ref": ref, "state": state, "count": None}])
        assert items[0]["action"] == expected, (status, ref, state)


def test_every_action_key_has_en_and_ar_copy():
    for ref, _state in webapp._HANDOFF_ACTION_ENDPOINTS:
        for lang in ("en", "ar"):
            assert ui_text.text("UI_FH_ACTION_" + ref, lang)
    assert ui_text.text("UI_FH_ACTION_NOTE", "en") != ui_text.text("UI_FH_ACTION_NOTE", "ar")


# ==========================================================================
# 2. CAP-13: positive journey; the destination keeps its own inputs and gate
# ==========================================================================
def test_screen_support_on_a_mechanical_project_links_to_the_existing_cap13_page():
    c, _aid = _client_for("s6-screen@example.com")
    sid = _start(c, SCREEN_EN, MECH)
    section = _section(_page(c, sid))
    assert 'data-fh-role="SCREEN_SUPPORT"' in section
    assert SCREEN_EN in html.unescape(section)
    assert _actions(section) == [("CAP13_CONDITIONAL_REACTIONS", CAP13_URL % sid)]
    assert ui_text.text("UI_FH_ACTION_NOTE", "en") in html.unescape(section)
    assert 'data-fh-status="PROPOSED"' in section          # stays visibly provisional
    # follow the link: the existing form, nothing pre-selected or pre-filled
    page = c.get(CAP13_URL % sid).get_data(as_text=True)
    assert "data-cap13-form" in page and " checked" not in page
    for name in ("P", "L", "x"):
        tag = re.search(r'<input[^>]*id="cap13-%s"[^>]*>' % name, page).group(0)
        assert 'value="' not in tag or 'value=""' in tag
    # the inventor's own inputs produce the existing deterministic result
    r = c.post(CAP13_URL % sid, data=_cap13_form())
    body = r.get_data(as_text=True)
    assert r.status_code == 200 and _reactions(body) == ["750.0 N", "250.0 N"]
    assert "UNVALIDATED" in body and "cap13:static_reactions_two_support" in body


def test_the_reading_never_reaches_the_cap13_request(monkeypatch):
    c, _aid = _client_for("s6-screen-spy@example.com")
    sid = _start(c, SCREEN_EN, MECH)
    seen = []
    real = webapp._cap13.capture_form
    monkeypatch.setattr(webapp._cap13, "capture_form",
                        lambda form: seen.append(dict(form)) or real(form))
    c.post(CAP13_URL % sid, data=_cap13_form())
    assert seen and set(seen[0]) - {"csrf_token"} == set(_cap13_form())
    assert all("monitor" not in v[0] and "desk" not in v[0] for v in seen[0].values())


def test_no_action_when_cap13_is_not_eligible():
    c, _aid = _client_for("s6-screen-elec@example.com")
    sid = _start(c, SCREEN_EN, ELEC)
    section = _section(_page(c, sid))
    assert 'data-fh-capability-state="NOT_FOR_PROJECT"' in section
    assert _actions(section) == []


def test_request_parameters_cannot_create_an_action_or_eligibility():
    c, _aid = _client_for("s6-screen-tamper@example.com")
    sid = _start(c, SCREEN_EN, ELEC)
    tamper = ("?domain=mechanical&root_domain=mechanical&part=x&role=SCREEN_SUPPORT"
              "&capability=CAP13_CONDITIONAL_REACTIONS&eligible=1&eligibility=yes")
    body = c.get("/session/%s%s" % (sid, tamper)).get_data(as_text=True)
    assert _actions(_section(body)) == []
    for r in (c.get(CAP13_URL % sid + tamper),
              c.post(CAP13_URL % sid + tamper, data=_cap13_form())):
        page = r.get_data(as_text=True)
        assert "data-cap13-form" not in page and "data-cap13-reaction" not in page


def test_eligible_at_render_then_ineligible_at_the_destination_refuses():
    """The link is rendered from a valid integrated composition; the durable
    composition then changes; the destination re-reads its gate and refuses."""
    c, _aid = _client_for("s6-stale@example.com")
    sid = _integrated(c, ELEC, idea=SCREEN_EN)
    section = _section(_page(c, sid))
    assert _actions(section) == [("CAP13_CONDITIONAL_REACTIONS", CAP13_URL % sid)]
    _corrupt("UPDATE project_subsystems SET domain = 'software' WHERE subsystem_seq = 0")
    for r in (c.get(CAP13_URL % sid), c.post(CAP13_URL % sid, data=_cap13_form())):
        page = r.get_data(as_text=True)
        assert "data-cap13-form" not in page and "data-cap13-reaction" not in page
    # and the session page no longer offers it (it may not render at all)
    assert CAP13_ACTION not in c.get("/session/%s" % sid).get_data(as_text=True)


@pytest.mark.parametrize("sql", (
    "UPDATE project_subsystems SET domain = 'software' WHERE subsystem_seq = 0",
    "UPDATE project_subsystems SET subsystem_seq = 7 WHERE subsystem_seq = 0",
))
def test_corrupt_composition_offers_nothing(sql):
    c, _aid = _client_for("s6-corrupt-%d@example.com" % len(sql))
    sid = _integrated(c, ELEC, idea=SCREEN_EN)
    _corrupt(sql)
    assert CAP13_ACTION not in c.get("/session/%s" % sid).get_data(as_text=True)


def test_integrated_project_reaches_the_same_workflow_from_the_declared_part():
    c, _aid = _client_for("s6-integrated@example.com")
    sid = _integrated(c, ELEC, idea=SCREEN_EN)
    before = webapp._get_store().load_project_subsystems(sid)
    section = _section(_page(c, sid))
    assert 'data-fh-role="SCREEN_SUPPORT"' in section
    assert _actions(section) == [("CAP13_CONDITIONAL_REACTIONS", CAP13_URL % sid)]
    page = c.get(CAP13_URL % sid).get_data(as_text=True)
    assert "data-cap13-part-name>" in page and "Hinge arm" in page   # the durable part
    r = c.post(CAP13_URL % sid, data=_cap13_form())
    assert _reactions(r.get_data(as_text=True)) == ["750.0 N", "250.0 N"]
    assert webapp._get_store().load_project_subsystems(sid) == before   # nothing created


# ==========================================================================
# 3. no action from anything but a clear proposed reading
# ==========================================================================
@pytest.mark.parametrize("idea", (
    "I don't want a stand for my monitor.",                 # negated
    "Maybe someday I would want a stand for my monitor?",   # abstained / question
    "A folding mechanical wheelchair ramp with a spring latch.",   # no role
))
def test_negated_abstained_or_absent_roles_give_no_action(idea):
    c, _aid = _client_for("s6-none-%d@example.com" % len(idea))
    sid = _start(c, idea, MECH)
    assert _actions(_section(_page(c, sid))) == []


def test_conflicting_reading_gives_no_action(monkeypatch):
    real = fh.project_functional_roles

    def conflicting(statements):
        out = real(statements)
        roles = tuple(r.__class__(**dict(r.__dict__, status=fh.CONFLICTING))
                      for r in out.roles)
        return out.__class__(**dict(out.__dict__, roles=roles))
    monkeypatch.setattr(webapp._handoff, "project_functional_roles", conflicting)
    c, _aid = _client_for("s6-conflict@example.com")
    sid = _start(c, SCREEN_EN, MECH)
    section = _section(_page(c, sid))
    assert 'data-fh-status="CONFLICTING"' in section and _actions(section) == []


def test_handoff_failure_or_unreadable_owner_gives_no_action(monkeypatch):
    def broken(*_a):
        raise OSError("disk I/O error")
    monkeypatch.setattr(webapp, "_cap13_eligible", broken)
    monkeypatch.setattr(webapp, "_current_experiment_ids", broken)
    for role in fh.ROLES:
        items = webapp._handoff_actions(
            fh.PROPOSED, webapp._handoff_capabilities("sid", object(), role))
        assert items and all(i["state"] == "UNAVAILABLE" and i["action"] is None
                             for i in items)
    monkeypatch.undo()
    c, _aid = _client_for("s6-fail@example.com")
    sid = _start(c, SCREEN_EN, MECH)
    monkeypatch.setattr(webapp._handoff, "project_functional_roles", broken)
    section = _section(_page(c, sid))
    assert "data-fh-unavailable" in section and _actions(section) == []


def test_an_unrelated_role_never_links_to_cap13():
    c, _aid = _client_for("s6-fan-mech@example.com")
    sid = _start(c, "I want an automatic fan that turns on when my room gets hot.", MECH)
    section = _section(_page(c, sid))
    assert 'data-fh-role="FAN"' in section and CAP13_ACTION not in section


def test_direct_cap13_link_and_page_are_unchanged():
    c, _aid = _client_for("s6-direct@example.com")
    sid = _start(c, SCREEN_EN, MECH)
    body = _page(c, sid)
    assert "data-cap13-link" in body                         # the existing link stays
    assert c.get(CAP13_URL % sid).status_code == 200


# ==========================================================================
# 4. CAP-09: watering / fan link to the existing planning page when available
# ==========================================================================
def test_watering_links_to_experiment_planning_only_with_current_experiments(client):
    sid = _start_mech(client, seed=SEED + ". " + WATER_EN)
    section = _section(client.get("/session/%s" % sid).get_data(as_text=True))
    assert 'data-fh-capability-state="NO_EXPERIMENTS"' in section and _actions(section) == []
    for value in (MECH_ANSWER, MECH_ANSWER, PF_STRONG, BA_1, BA_2):
        _answer(client, sid, value)
    assert webapp._current_experiment_ids(_live(sid))
    section = _section(client.get("/session/%s" % sid).get_data(as_text=True))
    assert _actions(section) == [("CAP09_EXPERIMENT_PLANNING",
                                  "/session/%s/success-criteria" % sid)]
    r = client.get("/session/%s/success-criteria" % sid)
    assert r.status_code == 200
    # the existing planning page: no field is pre-filled from the reading
    for content in re.findall(r"<textarea[^>]*>(.*?)</textarea>", r.get_data(as_text=True), re.S):
        assert "plants" not in content


# ==========================================================================
# 5. Arabic / RTL
# ==========================================================================
def test_arabic_action_copy_and_rtl():
    c, _aid = _client_for("s6-ar@example.com")
    sid = _start(c, SCREEN_AR, MECH)
    assert c.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    body = _page(c, sid)
    section = _section(body)
    assert 'dir="rtl"' in body
    assert _actions(section) == [("CAP13_CONDITIONAL_REACTIONS", CAP13_URL % sid)]
    text = html.unescape(section)
    assert ui_text.text("UI_FH_ACTION_CAP13_CONDITIONAL_REACTIONS", "ar") in text
    assert ui_text.text("UI_FH_ACTION_NOTE", "ar") in text
