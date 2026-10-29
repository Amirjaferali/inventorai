# -*- coding: utf-8 -*-
"""CAP13-PLANAR-MOMENT-INTEGRATED-PART-01 — integrated-part eligibility for the
CAP-13 planar single-force moment (Owner-authorized).

Authority: the planar-moment method contract §1 (as amended) and the narrow
Stage 15 exception recorded in ``engine/subsystem_model.py``. The existing
``cap13:planar_single_force_moment`` 1.0 calculation may be offered for the ONE
declared Mechanical part of a valid durable integrated composition, whatever
the initial analysis focus, through the SAME ``_calc_gate`` the two-support
reactions use. Root eligibility is unchanged; a missing, corrupt or unreadable
composition grants nothing beyond it; nothing is taken from the request; the
inventor still supplies every value, declaration and screen answer; the
method, units, numeric policy and owner request are identical; nothing is
persisted; the declared part is named, escaped, in EN and AR. Synthetic data.
"""
import html as _html
import sqlite3
from pathlib import Path

import pytest

import web.app as webapp
from web import ui_text
from engine import deterministic_calculation as dc
from engine import cap13_planar_moment as moment
from engine import cap13_planar_moment_method as method
from engine import cap13_static_reactions as cap13
from engine import therm01_temperature_difference as therm
from tests.test_cap12_form_mockup_advisory import (
    _client_for, _new_client, _start, _page, _snapshot, SEED, ELEC_FORM)
from tests.test_cap13_therm01_integrated_part_eligibility import (
    _integrated, _corrupt, _owner_spy, _part_line, MECH, ELEC, PARTS, CTRL, HOSTILE)
from tests.test_cap13_planar_moment import _form
from tests.test_cap13_static_reactions import _form as _cap13_form
from tests.test_therm01_temperature_difference import _form as _therm_form

URL = "/session/%s/planar-moment"
ROOT = Path(__file__).resolve().parent.parent


def _client(tag):
    client, _aid = _client_for("cap13m-part-%s@example.com" % tag)
    return client


def _value(body):
    marker = 'data-cap13m-result-value><bdi dir="ltr">'
    return body.split(marker, 1)[1].split("</bdi>", 1)[0] if marker in body else None


@pytest.fixture
def elec_focus():
    c = _client("elec-focus")
    return c, _integrated(c, ELEC)


@pytest.fixture
def mech_focus():
    c = _client("mech-focus")
    return c, _integrated(c, MECH)


# ==========================================================================
# 1. root eligibility unchanged; the integrated part is offered in both focuses
# ==========================================================================
def test_single_domain_projects_keep_exactly_the_root_rule():
    c = _client("single")
    mech = _start(c, {"idea": SEED, "domain_confirm": MECH})
    elec = _start(c, ELEC_FORM)
    assert webapp._calc_gate(mech, moment) == (True, None)
    assert webapp._calc_gate(elec, moment) == (False, None)
    assert "data-cap13m-link" in _page(c, mech)
    assert "data-cap13m-link" not in _page(c, elec)
    body = c.post(URL % mech, data=_form()).get_data(as_text=True)
    assert _value(body) == "1000.0 N·mm" and "data-cap13m-part" not in body
    body = c.post(URL % elec, data=_form()).get_data(as_text=True)
    assert "data-cap13m-form" not in body and _value(body) is None


@pytest.mark.parametrize("focus", (ELEC, MECH))
def test_integrated_mechanical_part_is_offered_in_either_focus(focus):
    c = _client("focus-%s" % focus)
    sid = _integrated(c, focus)
    eligible, part = webapp._calc_gate(sid, moment)
    assert eligible and part.domain == MECH
    assert part.display_name == PARTS["mech_part_name"]
    # the link, the GET and the POST read the same one decision
    assert webapp._cap13m_link_offered(sid) is True
    assert "data-cap13m-link" in _page(c, sid)
    get_body = c.get(URL % sid).get_data(as_text=True)
    assert "data-cap13m-form" in get_body
    assert _part_line(get_body, "cap13m") == PARTS["mech_part_name"]
    body = c.post(URL % sid, data=_form()).get_data(as_text=True)
    assert _value(body) == "1000.0 N·mm"
    assert _part_line(body, "cap13m") == PARTS["mech_part_name"]
    assert PARTS["elec_part_name"] not in body
    assert "UNVALIDATED" in body


def test_three_part_composition_names_only_the_mechanical_part():
    c = _client("three")
    sid = _integrated(c, ELEC, **CTRL)
    body = c.post(URL % sid, data=_form()).get_data(as_text=True)
    assert _part_line(body, "cap13m") == PARTS["mech_part_name"]
    assert CTRL["ctrl_part_name"] not in body and PARTS["elec_part_name"] not in body


def test_the_gate_is_the_shared_calc_gate_for_every_surface():
    src = Path(webapp.__file__).read_text(encoding="utf-8")
    start = src.index("# Stage 25 / CAP-13 — Planar Single-Force Moment")
    section = src[start:src.index("# Stage 27 / THERM-01 — Single-Path", start)]
    assert section.count("_calc_gate(sid, _cap13m)") == 3      # eligible / GET / POST
    for access in ("request.args", "request.values", "request.json",
                   "load_project_subsystems", "_get_store()"):
        assert access not in section, access


# ==========================================================================
# 2. fail closed: nothing beyond the root rule from a bad composition
# ==========================================================================
@pytest.mark.parametrize("sql", (
    "UPDATE project_subsystems SET domain = 'software' WHERE subsystem_seq = 0",
    "DELETE FROM project_subsystems WHERE subsystem_seq = 0",
    "UPDATE project_subsystems SET display_name = ' padded' WHERE subsystem_seq = 0",
    "UPDATE project_subsystems SET subsystem_seq = 7 WHERE subsystem_seq = 0",
))
def test_corrupt_composition_grants_nothing(elec_focus, monkeypatch, sql):
    c, sid = elec_focus
    _corrupt(sql)
    calls = _owner_spy(monkeypatch)
    evaluated = []
    monkeypatch.setattr(webapp._cap13m, "evaluate",
                        lambda *a, **k: evaluated.append(1))
    assert webapp._calc_gate(sid, moment) == (False, None)
    assert webapp._cap13m_link_offered(sid) is False
    for r in (c.get(URL % sid), c.post(URL % sid, data=_form())):
        assert r.status_code == 200
        body = r.get_data(as_text=True)
        assert "data-cap13m-scope-note" in body
        assert "data-cap13m-form" not in body and "data-cap13m-part" not in body
        assert _value(body) is None and "data-cap13m-outcome" not in body
    assert not evaluated and not calls


def test_unreadable_composition_grants_nothing(elec_focus, monkeypatch):
    c, sid = elec_focus

    def broken(_sid):
        raise sqlite3.OperationalError("disk I/O error")
    monkeypatch.setattr(webapp._get_store(), "load_project_subsystems", broken)
    calls = _owner_spy(monkeypatch)
    assert webapp._calc_gate(sid, moment) == (False, None)
    body = c.post(URL % sid, data=_form()).get_data(as_text=True)
    assert _value(body) is None and "data-cap13m-form" not in body
    assert not calls


def test_missing_or_invalid_composition_keeps_only_the_root_rule(monkeypatch):
    c = _client("missing")
    elec = _integrated(c, ELEC)
    mech = _integrated(c, MECH)
    monkeypatch.setattr(webapp._get_store(), "load_project_subsystems", lambda _sid: ())
    assert webapp._calc_gate(elec, moment) == (False, None)
    assert webapp._calc_gate(mech, moment) == (True, None)      # root rule only
    body = c.post(URL % mech, data=_form()).get_data(as_text=True)
    assert _value(body) == "1000.0 N·mm" and "data-cap13m-part" not in body


def test_the_request_can_never_supply_a_part_or_domain():
    c = _client("request")
    elec = _start(c, ELEC_FORM)
    for extra in ({"part_domain": MECH}, {"subsystem_id": "sub-" + "0" * 32},
                  {"confirmed_domain": MECH}, {"part": "mechanical"}):
        body = c.post(URL % elec, data=dict(_form(), **extra)).get_data(as_text=True)
        assert "data-cap13m-form" not in body and _value(body) is None


# ==========================================================================
# 3. authorization, CSRF, strict capture and the inventor's own inputs
# ==========================================================================
def test_another_account_anonymous_and_csrf_are_denied(elec_focus):
    _c, sid = elec_focus
    assert webapp.app.test_client().post(URL % sid, data=_form()).status_code == 403
    other, _ = _client_for("cap13m-part-other@example.com")
    for client in (other, _new_client()):
        for r in (client.get(URL % sid), client.post(URL % sid, data=_form())):
            assert r.status_code == 302
            body = r.get_data(as_text=True)
            assert "data-cap13m" not in body and PARTS["mech_part_name"] not in body


@pytest.mark.parametrize("over,outcome", [
    ({"decl": {"planar": ""}}, "NOT_DECLARED"),
    ({"screen": {"food_contact": ""}}, "NOT_DECLARED"),
    ({"screen": {"supports_people": "yes"}}, "ENGINEERING_REVIEW_REQUIRED"),
    ({"decl": {"chosen_point": "does_not_apply"}}, "MODEL_NOT_SUPPORTED"),
    ({"F": ""}, "INVALID_NUMERIC_INPUT"),
    ({"d_perp": "0"}, "INVALID_NUMERIC_INPUT"),
])
def test_declarations_screen_and_values_are_still_required(elec_focus, over, outcome):
    c, sid = elec_focus
    body = c.post(URL % sid, data=_form(**over)).get_data(as_text=True)
    assert _html.escape(ui_text.text("UI_CAP13M_OUTCOME_" + outcome, "en"),
                        quote=False) in body
    assert _value(body) is None
    assert _part_line(body, "cap13m") == PARTS["mech_part_name"]


def test_nothing_is_inferred_or_preselected_for_the_part(elec_focus):
    c, sid = elec_focus
    body = c.get(URL % sid).get_data(as_text=True)
    assert "checked" not in body
    for role in ("F", "d_perp"):
        assert 'name="value_%s"' % role in body
        assert body.split('name="value_%s"' % role, 1)[1].split(">", 1)[0] \
            .rstrip().endswith('value=""')


def test_malformed_request_is_400_with_attribution(elec_focus):
    c, sid = elec_focus
    r = c.post(URL % sid, data=dict(_form(), unexpected="1"))
    assert r.status_code == 400
    body = r.get_data(as_text=True)
    assert ui_text.text("UI_CAP13M_ERR_REQUEST", "en") in body
    assert _value(body) is None


# ==========================================================================
# 4. the method, units, numbers and owner request are unchanged by the path
# ==========================================================================
def test_numbers_and_owner_requests_are_identical_irrespective_of_path(monkeypatch):
    c = _client("identical")
    root = _start(c, {"idea": SEED, "domain_confirm": MECH})
    part = _integrated(c, ELEC)
    calls = _owner_spy(monkeypatch)
    bodies = [c.post(URL % sid, data=_form(F="7.25", d_perp="13"))
              .get_data(as_text=True) for sid in (root, part)]
    assert [_value(b) for b in bodies] == ["94.25 N·mm"] * 2
    (req_root, res_root), (req_part, res_part) = calls
    assert req_root == req_part == {
        "method_id": method.METHOD_ID, "method_version": "1.0",
        "inputs": {"F": {"value": 7.25, "unit": "N"},
                   "d_perp": {"value": 13.0, "unit": "mm"}},
        "subject_ref": None}
    assert res_root["result_identity"] == res_part["result_identity"]
    assert (res_part["artifact_version"], res_part["implementation_version"]) \
        == ("13", "1.12.0")
    assert res_part["outputs"]["M"]["unit"] == "N·mm"


def test_method_owner_and_artifacts_are_untouched_by_this_increment():
    assert (method.METHOD_ID, method.METHOD_VERSION) == (
        "cap13:planar_single_force_moment", "1.0")
    assert dc.IMPLEMENTATION_VERSION == "1.12.0"
    assert dc.load_artifact()["artifact_version"] == "13"
    assert moment.load_artifact()["artifact_version"] == "1"
    assert moment.ELIGIBLE_ROOT_DOMAIN == MECH


@pytest.mark.parametrize("over", [{}, {"F": "-1"}, {"screen": {"children": "yes"}}])
def test_nothing_is_persisted_on_the_integrated_part_path(elec_focus, over):
    c, sid = elec_focus
    _page(c, sid)
    before = _snapshot(c)
    c.post(URL % sid, data=_form(**over))
    c.get(URL % sid)
    assert _snapshot(c) == before


def test_existing_calculations_keep_their_integrated_behaviour(elec_focus):
    c, sid = elec_focus
    assert webapp._calc_gate(sid, cap13)[0] is True
    assert webapp._calc_gate(sid, therm)[0] is True
    body = c.post("/session/%s/support-reactions" % sid,
                  data=_cap13_form()).get_data(as_text=True)
    assert '<bdi dir="ltr">750.0 N</bdi>' in body
    assert _part_line(body, "cap13") == PARTS["mech_part_name"]
    body = c.post("/session/%s/temperature-difference" % sid,
                  data=_therm_form()).get_data(as_text=True)
    assert '<bdi dir="ltr">25.0 K</bdi>' in body


# ==========================================================================
# 5. attribution and wording: escaped, isolated, bilingual, no claim
# ==========================================================================
@pytest.mark.parametrize("lang", ("en", "ar"))
def test_attribution_is_escaped_isolated_and_bilingual(lang):
    c = _client("hostile-%s" % lang)
    sid = _integrated(c, ELEC, mech_part_name=HOSTILE)
    if lang == "ar":
        assert c.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    body = c.post(URL % sid, data=_form()).get_data(as_text=True)
    assert "<script>alert" not in body
    raw_name = _part_line(body, "cap13m")
    assert raw_name is not None and "&lt;script&gt;" in raw_name
    assert _html.unescape(raw_name) == HOSTILE
    assert '<bdi dir="auto" data-cap13m-part-name>' in body
    text = _html.unescape(body)
    for key in ("UI_CAP13_PART_LABEL", "UI_CAP13_PART_NOTE", "UI_CAP13M_SCOPE_NOTE"):
        assert ui_text.text(key, lang) in _html.unescape(
            __import__("re").sub(r"<[^>]+>", "", body)), key
    if lang == "ar":
        assert 'dir="rtl"' in body
        assert '(<bdi dir="ltr">UNVALIDATED</bdi>)' in body
        assert '<bdi dir="ltr">1000.0 N·mm</bdi>' in body
    assert "UNVALIDATED" in text


def test_scope_wording_names_the_part_and_carries_no_applicability_claim():
    en = ui_text.text("UI_CAP13M_SCOPE_NOTE", "en")
    assert "declared Mechanical part" in en
    assert "establishes that the planar single-force model applies" in en
    assert en.startswith("This optional calculation") and "Neither" in en
    for word in ("is suitable", "is safe", "is adequate", "approved", "compatible"):
        assert word not in en.lower(), word
    assert "الميكانيكي المصرّح به" in ui_text.text("UI_CAP13M_SCOPE_NOTE", "ar")


def test_contract_and_stage15_exception_name_this_method():
    contract = (ROOT / "docs" / "governance"
                / "STAGE25_CAP13_PLANAR_SINGLE_FORCE_MOMENT_METHOD_CONTRACT.md"
                ).read_text(encoding="utf-8")
    assert "CAP13-PLANAR-MOMENT-INTEGRATED-PART-01" in contract
    s1 = contract[contract.index("## 1. Purpose"):contract.index("## 2.")]
    assert "the ONE inventor-declared Mechanical part" in s1 and "_calc_gate" in s1
    source = (ROOT / "engine" / "subsystem_model.py").read_text(encoding="utf-8")
    assert "CAP13-PLANAR-MOMENT-INTEGRATED-PART-01" in source
    assert "``cap13:planar_single_force_moment`` v1.0" in source
    assert "No other specialist\nbehaviour is granted by these exceptions." in source
