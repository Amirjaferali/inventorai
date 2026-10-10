"""CAP13-THERM01-INTEGRATED-PART-01 — integrated-part eligibility for the two
admitted request-local calculations (Owner-authorized, 2026-10-10).

Authority: the CAP-13 contract §12A / §12B and the THERM-01 contract §1 / §9A /
§10, as amended, and the narrow Stage 15 exception recorded in
``engine/subsystem_model.py``. CAP-13 may be offered for the declared Mechanical
part and THERM-01 for the declared Electrical / Electronics part of a valid
durable integrated composition, whatever the initial analysis focus. Root
eligibility is unchanged; a missing, corrupt or unreadable composition grants
nothing beyond it; nothing is taken from the request; the numbers, the request
the shared owner receives and the persistence boundary are identical; the
declared part is named, escaped, in EN and AR. Synthetic invention data only.
"""
import html as _html
import os
import sqlite3

import pytest

import web.app as webapp
from web import ui_text
from engine import deterministic_calculation as dc
from engine import cap13_static_reactions as cap13
from engine import therm01_temperature_difference as therm
from tests.test_cap12_form_mockup_advisory import (
    _client_for, _new_client, _start, _page, _snapshot, SEED, ELEC_FORM)
from tests.test_cap13_static_reactions import _form as _cap13_form
from tests.test_therm01_temperature_difference import _form as _therm_form

CAP13_URL = "/session/%s/support-reactions"
THERM_URL = "/session/%s/temperature-difference"
MECH = "mechanical"
ELEC = "electronics_electrical"
TIE_IDEA = "circuit and hinge"
PARTS = {
    "mech_part_name": "Hinge arm",
    "mech_part_function": "Swings the window open and closed",
    "elec_part_name": "Motor driver board",
    "elec_part_function": "Switches battery power to the motor",
}
CTRL = {"ctrl_part_name": "Thermostat logic",
        "ctrl_part_function": "Compares the temperature with the target"}


# --------------------------------------------------------------------------
# harness
# --------------------------------------------------------------------------
def _integrated(client, focus, **over):
    data = {"idea": TIE_IDEA, "composition_step": "1",
            "integrated_invention": "yes", "composition_answer": "yes",
            "initial_focus": focus}
    data.update(PARTS)
    data.update(over)
    sid = _start(client, data)
    domains = [s.domain for s in webapp._get_store().load_project_subsystems(sid)]
    assert domains[:2] == [MECH, ELEC]
    assert webapp._get_store().load_reconstruction_inputs(sid)["confirmed_domain"] == focus
    return sid


def _client(tag):
    client, _aid = _client_for("integrated-part-%s@example.com" % tag)
    return client


def _corrupt(sql):
    with sqlite3.connect(os.environ["INVENTORAI_DB_PATH"]) as connection:
        connection.execute(sql)


def _owner_spy(monkeypatch):
    calls = []
    real = dc.execute

    def spy(binding, request, artifact_path=None):
        result = real(binding, request, artifact_path=artifact_path)
        calls.append((request, result))
        return result
    monkeypatch.setattr(dc, "execute", spy)
    return calls


def _reactions(body):
    """The displayed reaction values only (``"750.0 N"``), in page order."""
    return [chunk.split("</bdi>", 1)[0]
            for chunk in body.split('data-cap13-reaction><bdi dir="ltr">')[1:]]


def _part_line(body, prefix):
    marker = "data-%s-part-name>" % prefix
    if marker not in body:
        return None
    return body.split(marker, 1)[1].split("</bdi>", 1)[0]


@pytest.fixture
def elec_focus():
    c = _client("elec-focus")
    return c, _integrated(c, ELEC)


@pytest.fixture
def mech_focus():
    c = _client("mech-focus")
    return c, _integrated(c, MECH)


# ==========================================================================
# 1. root eligibility and single-domain projects are unchanged
# ==========================================================================
def test_single_domain_projects_keep_exactly_the_root_rule():
    c = _client("single")
    mech = _start(c, {"idea": SEED, "domain_confirm": MECH})
    elec = _start(c, ELEC_FORM)
    assert webapp._get_store().load_project_subsystems(mech) == ()
    assert webapp._calc_gate(mech, cap13) == (True, None)
    assert webapp._calc_gate(mech, therm) == (False, None)
    assert webapp._calc_gate(elec, therm) == (True, None)
    assert webapp._calc_gate(elec, cap13) == (False, None)
    page_m, page_e = _page(c, mech), _page(c, elec)
    assert "data-cap13-link" in page_m and "data-therm01-link" not in page_m
    assert "data-therm01-link" in page_e and "data-cap13-link" not in page_e
    for url, sid, prefix in ((CAP13_URL, mech, "cap13"), (THERM_URL, elec, "therm01")):
        body = c.get(url % sid).get_data(as_text=True)
        assert "data-%s-form" % prefix in body
        assert "data-%s-part" % prefix not in body
    for url, sid, prefix in ((CAP13_URL, elec, "cap13"), (THERM_URL, mech, "therm01")):
        body = c.get(url % sid).get_data(as_text=True)
        assert "data-%s-form" % prefix not in body
        assert "data-%s-part" % prefix not in body


def test_root_eligibility_never_depends_on_the_composition(monkeypatch):
    c = _client("root-independent")
    mech = _start(c, {"idea": SEED, "domain_confirm": MECH})

    def broken(_sid):
        raise RuntimeError("unreadable")
    monkeypatch.setattr(webapp._get_store(), "load_project_subsystems", broken)
    assert webapp._calc_gate(mech, cap13) == (True, None)
    assert webapp._cap13_link_offered(mech) is True
    body = c.post(CAP13_URL % mech, data=_cap13_form()).get_data(as_text=True)
    assert len(_reactions(body)) == 2


# ==========================================================================
# 2. / 3. each focus reaches the other part's calculation, named by its part
# ==========================================================================
def test_electrical_focus_is_offered_cap13_for_its_mechanical_part(elec_focus):
    c, sid = elec_focus
    eligible, part = webapp._calc_gate(sid, cap13)
    assert eligible and part.domain == MECH and part.display_name == PARTS["mech_part_name"]
    page = _page(c, sid)
    assert "data-cap13-link" in page and "data-therm01-link" in page
    get = c.get(CAP13_URL % sid).get_data(as_text=True)
    assert "data-cap13-form" in get
    assert _part_line(get, "cap13") == PARTS["mech_part_name"]
    post = c.post(CAP13_URL % sid, data=_cap13_form()).get_data(as_text=True)
    assert _reactions(post) == ["750.0 N", "250.0 N"]
    assert _part_line(post, "cap13") == PARTS["mech_part_name"]
    # the root calculation keeps working and names the focus part
    root = c.get(THERM_URL % sid).get_data(as_text=True)
    assert "data-therm01-form" in root
    assert _part_line(root, "therm01") == PARTS["elec_part_name"]


def test_mechanical_focus_is_offered_therm01_for_its_electrical_part(mech_focus):
    c, sid = mech_focus
    eligible, part = webapp._calc_gate(sid, therm)
    assert eligible and part.domain == ELEC and part.display_name == PARTS["elec_part_name"]
    page = _page(c, sid)
    assert "data-therm01-link" in page and "data-cap13-link" in page
    post = c.post(THERM_URL % sid, data=_therm_form()).get_data(as_text=True)
    assert "data-therm01-result-value><bdi dir=\"ltr\">25.0 K</bdi>" in post
    assert _part_line(post, "therm01") == PARTS["elec_part_name"]
    root = c.get(CAP13_URL % sid).get_data(as_text=True)
    assert _part_line(root, "cap13") == PARTS["mech_part_name"]


@pytest.mark.parametrize("focus", (MECH, ELEC))
def test_three_part_composition_offers_only_the_matching_parts(focus):
    c = _client("three-%s" % focus)
    sid = _integrated(c, focus, **CTRL)
    domains = [s.domain for s in webapp._get_store().load_project_subsystems(sid)]
    assert domains == [MECH, ELEC, "control_loop"]
    eligible_c, part_c = webapp._calc_gate(sid, cap13)
    eligible_t, part_t = webapp._calc_gate(sid, therm)
    assert eligible_c and part_c.domain == MECH
    assert eligible_t and part_t.domain == ELEC
    for url, form, prefix, name in (
            (CAP13_URL, _cap13_form(), "cap13", PARTS["mech_part_name"]),
            (THERM_URL, _therm_form(), "therm01", PARTS["elec_part_name"])):
        body = c.post(url % sid, data=form).get_data(as_text=True)
        assert _part_line(body, prefix) == name
        assert CTRL["ctrl_part_name"] not in body


# ==========================================================================
# 4. / 5. / 6. fail closed: nothing beyond the root rule from a bad composition
# ==========================================================================
@pytest.mark.parametrize("sql", (
    "UPDATE project_subsystems SET domain = 'software' WHERE subsystem_seq = 0",
    "DELETE FROM project_subsystems WHERE subsystem_seq = 0",
    "UPDATE project_subsystems SET display_name = ' padded' WHERE subsystem_seq = 0",
    "UPDATE project_subsystems SET subsystem_seq = 7 WHERE subsystem_seq = 0",
))
def test_corrupt_composition_grants_no_non_root_calculation(elec_focus, monkeypatch, sql):
    c, sid = elec_focus
    _corrupt(sql)
    calls = _owner_spy(monkeypatch)
    evaluated = []
    real_evaluate = webapp._cap13.evaluate
    monkeypatch.setattr(webapp._cap13, "evaluate",
                        lambda *a, **k: evaluated.append(1) or real_evaluate(*a, **k))
    assert webapp._calc_gate(sid, cap13) == (False, None)
    assert webapp._cap13_link_offered(sid) is False
    for r in (c.get(CAP13_URL % sid), c.post(CAP13_URL % sid, data=_cap13_form())):
        assert r.status_code == 200
        body = r.get_data(as_text=True)
        assert "data-cap13-form" not in body and "data-cap13-outcome" not in body
        assert "data-cap13-reaction" not in body and "data-cap13-part" not in body
    assert not evaluated and not calls
    # the root calculation stays exactly root-eligible, with no attribution
    assert webapp._calc_gate(sid, therm) == (True, None)


def test_unreadable_composition_grants_no_non_root_calculation(elec_focus, monkeypatch):
    c, sid = elec_focus

    def broken(_sid):
        raise sqlite3.OperationalError("disk I/O error")
    monkeypatch.setattr(webapp._get_store(), "load_project_subsystems", broken)
    calls = _owner_spy(monkeypatch)
    assert webapp._calc_gate(sid, cap13) == (False, None)
    body = c.post(CAP13_URL % sid, data=_cap13_form()).get_data(as_text=True)
    assert "data-cap13-reaction" not in body and "data-cap13-outcome" not in body
    assert not calls


def test_a_composition_without_the_matching_part_grants_nothing(elec_focus, monkeypatch):
    _c, sid = elec_focus
    monkeypatch.setattr(webapp._get_store(), "load_project_subsystems", lambda _sid: ())
    assert webapp._calc_gate(sid, cap13) == (False, None)
    assert webapp._calc_gate(sid, therm) == (True, None)


def test_the_request_can_never_supply_a_part_or_domain():
    c = _client("request-supplied")
    elec = _start(c, ELEC_FORM)
    for extra in ({"part_domain": MECH}, {"subsystem_id": "sub-" + "0" * 32},
                  {"confirmed_domain": MECH}, {"part": "mechanical"}):
        body = c.post(CAP13_URL % elec, data=dict(_cap13_form(), **extra)).get_data(as_text=True)
        assert "data-cap13-form" not in body and "data-cap13-reaction" not in body
    src = open(webapp.__file__, encoding="utf-8").read()
    gate = src[src.index("def _calc_declared_part"):src.index("def _cap13_link_offered")]
    for access in ("request.form", "request.args", "request.values", "request.json"):
        assert access not in gate, access


# ==========================================================================
# 7. authorization, CSRF, strict capture and refusal semantics are intact
# ==========================================================================
def test_another_account_anonymous_and_csrf_are_denied(elec_focus):
    _c, sid = elec_focus
    other = _client("other")
    anon = _new_client()
    for client in (other, anon):
        for url, form in ((CAP13_URL, _cap13_form()), (THERM_URL, _therm_form())):
            for r in (client.get(url % sid), client.post(url % sid, data=form)):
                assert r.status_code == 302
                assert "data-cap13" not in r.get_data(as_text=True)
                assert "data-therm01" not in r.get_data(as_text=True)
    raw = webapp.app.test_client()
    assert raw.post(CAP13_URL % sid, data=_cap13_form()).status_code == 403
    assert raw.post(THERM_URL % sid, data=_therm_form()).status_code == 403


def test_strict_capture_and_refusals_keep_their_semantics_and_attribution(elec_focus, monkeypatch):
    c, sid = elec_focus
    calls = _owner_spy(monkeypatch)
    malformed = c.post(CAP13_URL % sid, data=dict(_cap13_form(), extra="1"))
    assert malformed.status_code == 400
    body = malformed.get_data(as_text=True)
    assert "data-cap13-error" in body and "data-cap13-outcome" not in body
    assert _part_line(body, "cap13") == PARTS["mech_part_name"]
    for over, outcome in (({"x": "2500"}, cap13.CG_OUTSIDE_SUPPORT_SPAN),
                          ({"screen": {"pressure": "yes"}}, cap13.ENGINEERING_REVIEW_REQUIRED),
                          ({"P": "abc"}, cap13.INVALID_NUMERIC_INPUT)):
        r = c.post(CAP13_URL % sid, data=_cap13_form(**over))
        body = r.get_data(as_text=True)
        assert r.status_code == 200
        assert _html.unescape(ui_text.text("UI_CAP13_OUTCOME_%s" % outcome, "en")) \
            in _html.unescape(body)
        assert "data-cap13-reaction" not in body
        assert _part_line(body, "cap13") == PARTS["mech_part_name"]
    assert not calls          # none of these reached the shared owner


# ==========================================================================
# 8. identical numbers and identical owner requests, whatever the focus
# ==========================================================================
def test_numbers_and_owner_requests_are_identical_irrespective_of_focus(monkeypatch):
    c = _client("parity")
    mech_root = _start(c, {"idea": SEED, "domain_confirm": MECH})
    elec_root = _start(c, ELEC_FORM)
    elec_focus = _integrated(c, ELEC)
    mech_focus = _integrated(c, MECH)
    calls = _owner_spy(monkeypatch)
    pages = {}
    for sid in (mech_root, elec_focus, mech_focus):
        pages[sid] = c.post(CAP13_URL % sid, data=_cap13_form(P="1234.5", L="987", x="12.25"))
    for sid in (elec_root, mech_focus, elec_focus):
        pages[sid, "t"] = c.post(THERM_URL % sid, data=_therm_form(P="3.75", R_theta="0.4"))
    assert len(calls) == 6
    cap13_calls, therm_calls = calls[:3], calls[3:]
    for group in (cap13_calls, therm_calls):
        first_request, first_result = group[0]
        assert first_request["subject_ref"] is None
        for request, result in group[1:]:
            assert request == first_request
            assert result == first_result
            assert result["subject_ref"] is None
    reactions = [_reactions(pages[s].get_data(as_text=True))
                 for s in (mech_root, elec_focus, mech_focus)]
    assert reactions[0] == reactions[1] == reactions[2] and len(reactions[0]) == 2


# ==========================================================================
# 9. nothing is persisted and no project state moves
# ==========================================================================
@pytest.mark.parametrize("over", [{}, {"x": "-3"}, {"screen": {"pressure": "yes"}}])
def test_nothing_is_persisted_on_the_integrated_part_path(elec_focus, over):
    c, sid = elec_focus
    _page(c, sid)
    before = _snapshot(c)
    c.post(CAP13_URL % sid, data=_cap13_form(**over))
    c.get(CAP13_URL % sid)
    assert _snapshot(c) == before


# ==========================================================================
# 10. EN / AR attribution, escaped, with hostile and bidirectional names
# ==========================================================================
HOSTILE = "<script>alert('x')</script> ‮evil‬ ذراع"


@pytest.mark.parametrize("lang", ("en", "ar"))
def test_attribution_is_escaped_isolated_and_bilingual(lang):
    c = _client("hostile-%s" % lang)
    sid = _integrated(c, ELEC, mech_part_name=HOSTILE)
    if lang == "ar":
        assert c.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    body = c.post(CAP13_URL % sid, data=_cap13_form()).get_data(as_text=True)
    assert "<script>alert" not in body
    raw_name = _part_line(body, "cap13")
    assert raw_name is not None and "&lt;script&gt;" in raw_name
    assert _html.unescape(raw_name) == HOSTILE
    assert '<bdi dir="auto" data-cap13-part-name>' in body
    text = _html.unescape(body)
    assert ui_text.text("UI_CAP13_PART_LABEL", lang) in text
    assert ui_text.text("UI_CAP13_PART_NOTE", lang) in text
    assert ui_text.text("UI_CAP13_SCOPE_NOTE", lang) in text


def test_attribution_and_scope_wording_carry_no_applicability_claim():
    for key in ("UI_CAP13_SCOPE_NOTE", "UI_CAP13_PART_NOTE",
                "UI_THERM01_SCOPE_NOTE", "UI_THERM01_PART_NOTE"):
        en = ui_text.text(key, "en")
        assert "does not establish" in en, key
        for word in ("applies to your", "is suitable", "is safe", "validated",
                     "is adequate", "approved"):
            assert word not in en.lower().replace("unvalidated", ""), (key, word)
