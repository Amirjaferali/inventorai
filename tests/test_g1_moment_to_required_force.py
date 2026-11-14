# -*- coding: utf-8 -*-
"""G1-MOMENT-TO-REQUIRED-FORCE-01 - a saved moment as the target of ONE required-force use.

Owner-authorized (two corrections). From ONE CURRENT saved planar-moment
configuration, the exact product P of its saved F and d_perp (the moment
consumer's read-only exact-input-product consequence, moment contract §12C) is
offered as the target moment of the UNCHANGED required-force calculation on the
same component, after two explicit confirmations (same point and plane; size
only). Synthetic data only. What is pinned:
  * numerical integrity (correction A): the four quantities stay distinct -
    P (exact decimal product of the saved inputs), M (the method's binary64
    moment), F_exact = P / d_perp (exact rational) and F_display (the existing
    12-significant-digit presentation); F_exact x d_perp = P in rational
    arithmetic, while a rounded display is never asked to reproduce P; the
    integrity bound is the proven (1 + 2**-53)**2 (1 + 2**-52) - 1 and is
    checked against the real owner;
  * lossless transfer only: P is passed as exact text through the required-force
    consumer's own strict capture and grammar, and refused (never rounded or
    shortened) when it does not fit; an integrity failure or a no-longer-admitted
    input passes nothing on;
  * backward compatibility (correction B): the planar-moment method identity,
    its artifact and its SHA-256 are unchanged, so a configuration saved under
    that identity stays CURRENT with the identical displayed moment; the
    required-force artifact and the shared owner artifact are byte-identical
    and the standalone page is unchanged;
  * the saved configuration is re-read on every request: a stale revision, a
    correction, a withdrawal or a changed component gives no number; nothing is
    persisted; the report / PDF saved-moment section is unchanged;
  * both confirmations and every declaration / screen item are the inventor's
    own; nothing is pre-selected; EN / AR.
"""
import hashlib
import html as _html
import json
import os
import random
import re
from fractions import Fraction

import pytest

import web.app as webapp
from engine import cap13_planar_moment as moment
from engine import cap13_planar_moment_method as moment_method
from engine import cap13_planar_required_force as force
from engine import deterministic_calculation as dc
from engine import record_store
from tests.test_cap13_planar_required_force import _form as _force_form
from tests.test_component_inventory_correct_withdraw import _correct as _correct_component
from tests.test_g1_planar_moment_saved_declaration import (  # noqa: F401  (fixture)
    EXPECTED, URL, _evaluate, _items, _page, _save, _state, _value, mech_client)
from web import ui_text

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STEP = "/session/%s/planar-moment/%s/required-force"

# The planar-moment identity every saved configuration binds, exactly as the base commit
# (46bf2ad) stamps it. Unchanged by this increment.
BASE_MOMENT_IDENTITY = ("cap13:planar_single_force_moment", "1.0", "1",
                        "687c6d6ce65f57489d9c952eae8e02558f95b6bd58bffe3f9e7982b03349ea62")
# Raw-file SHA-256 of the three governed artifacts at the base commit: none is touched.
BASE_FILE_SHA256 = {
    "docs/governance/cap13_content_config/planar_single_force_moment_v1.json":
        "6036f70dca7283fb40dd9c4623e5395a98054efa57853f83cdc692ec62887954",
    "docs/governance/cap13_content_config/planar_required_force_v1.json":
        "ece5162c2f977e91c5e9688ecd39712c8aee68d98f966e85f86f59b0c1c24968",
    "docs/governance/deterministic_calculation_config/deterministic_calculation_owner_v1.json":
        "eb283b821f66b7b8c2e697ca2efb353b123cc85c11333ad64d9d32c1cf5702f5",
}


def _raw_sha(path):
    with open(os.path.join(ROOT, path), "rb") as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def _moment(F, d):
    """The real moment consumer through the app's ONE trusted binding."""
    captured = moment.capture_form({k: [v] for k, v in {
        **{moment.DECLARATION_FIELD % x: moment.ANSWER_APPLIES for x in moment.DECLARATION_IDS},
        **{moment.SCREEN_FIELD % x: moment.SCREEN_NO for x in moment.SCREEN_ITEMS},
        moment.VALUE_FIELD % "F": F, moment.VALUE_FIELD % "d_perp": d}.items()})
    ev = moment.evaluate(captured, webapp._CAP13_MOMENT_BINDING)
    assert ev["outcome"] == moment.OUTCOME_SUCCESS
    return ev["result"]["outputs"]["M"]["value"]


# ==========================================================================
# 1. the proven bound and the four distinct quantities (correction A)
# ==========================================================================
def test_n01_the_bound_is_the_proven_expression_from_the_real_rules():
    u = Fraction(1, 2 ** 53)
    assert moment.UNIT_ROUNDOFF == u
    # the method adapter's own acceptance rule, restated (never imported by the consumer)
    assert moment.METHOD_ACCEPTANCE_BOUND == moment_method.RELATIVE_ERROR_BOUND == Fraction(1, 2 ** 52)
    assert moment.INPUT_PRODUCT_INTEGRITY_BOUND == (1 + u) ** 2 * (1 + Fraction(1, 2 ** 52)) - 1
    # the lower side is covered too: 1 - (1 - u)**2 (1 - 2u) <= (1 + u)**2 (1 + 2u) - 1
    assert 1 - (1 - u) ** 2 * (1 - 2 * u) <= moment.INPUT_PRODUCT_INTEGRITY_BOUND
    # every admitted input is a NORMAL binary64 number (64 characters at most), so one
    # correctly rounded conversion has relative error at most u
    limit = moment.MAX_VALUE_CHARS
    smallest, largest = "0." + "0" * (limit - 3) + "1", "9" * limit
    assert len(smallest) == len(largest) == limit
    assert moment.parse_number("0." + "0" * (limit - 2) + "1") is None     # one character too long
    for text in (smallest, largest):
        assert moment.parse_number(text) is not None
        value = float(text)
        assert 2.2250738585072014e-308 <= value < float("inf")
        assert abs(Fraction(value) - Fraction(text)) <= Fraction(text) * u


@pytest.mark.parametrize("F, d, product, binary_equals_product", [
    ("12.5", "80", "1000", True),
    ("9.81", "37.5", "367.875", True),
    ("40", "250", "10000", True),
    ("1.23456", "7.89012", "9.7408265472", False),    # M is one ulp away from P
    ("0.0001", "0.00001", "0.000000001", False),       # 10**-9 has no exact binary64 value
])
def test_n02_p_is_the_exact_input_product_and_stays_distinct_from_m(F, d, product, binary_equals_product):
    M = _moment(F, d)
    result = moment.exact_input_product({"F": F, "d_perp": d}, M)
    assert result["status"] == moment.PRODUCT_AVAILABLE
    assert result["value"] == Fraction(F) * Fraction(d)
    assert result["text"] == product and Fraction(result["text"]) == result["value"]
    assert (Fraction(M) == result["value"]) is binary_equals_product
    assert abs(Fraction(M) - result["value"]) <= result["value"] * moment.INPUT_PRODUCT_INTEGRITY_BOUND


def test_n03_supporting_evidence_the_real_owner_stays_inside_the_bound():
    rng = random.Random(20261114)
    worst = Fraction(0)
    for fd, dd in ((0, 0), (2, 1), (3, 2), (4, 4), (6, 6)):
        for _ in range(300):
            F = "%.*f" % (fd, rng.randint(1, 500 * 10 ** fd) / 10 ** fd)
            d = "%.*f" % (dd, rng.randint(1, 1000 * 10 ** dd) / 10 ** dd)
            M, P = Fraction(_moment(F, d)), Fraction(F) * Fraction(d)
            worst = max(worst, abs(M - P) / P)
            assert moment.exact_input_product({"F": F, "d_perp": d}, float(M))["status"] \
                == moment.PRODUCT_AVAILABLE
    assert worst <= moment.INPUT_PRODUCT_INTEGRITY_BOUND


def test_n04_a_moment_outside_the_bound_is_an_integrity_failure():
    values = {"F": "12.5", "d_perp": "80"}
    P = Fraction(1000)
    outside = float(P * (1 + moment.INPUT_PRODUCT_INTEGRITY_BOUND * 4))
    assert outside != 1000.0
    for bad in (outside, 0.0, -1000.0, float("inf"), float("nan"), 1000, "1000", None):
        result = moment.exact_input_product(values, bad)
        assert result == {"status": moment.PRODUCT_INTEGRITY_FAILURE, "text": None, "value": None}


@pytest.mark.parametrize("values", [
    {"F": "0", "d_perp": "80"}, {"F": "12.5", "d_perp": "-1"}, {"F": "1e3", "d_perp": "80"},
    {"F": "12,5", "d_perp": "80"}, {"F": "٨", "d_perp": "80"}, {"F": "1" * 65, "d_perp": "1"},
    {"F": "12.5"}, {}, None, {"F": 12.5, "d_perp": 80},
])
def test_n05_inputs_the_method_does_not_admit_pass_nothing(values):
    result = moment.exact_input_product(values, 1000.0)
    assert result == {"status": moment.PRODUCT_NOT_ADMITTED, "text": None, "value": None}


def test_n06_plain_decimal_is_exact_and_refuses_anything_else():
    for text in ("1000", "367.875", "0.000000001", "9.7408265472", "100", "0.5"):
        assert moment.plain_decimal(Fraction(text)) == text
    for bad in (Fraction(1, 3), Fraction(0), Fraction(-1), 1.5, "1"):
        with pytest.raises((ValueError, TypeError)):
            moment.plain_decimal(bad)


@pytest.mark.parametrize("P, d, exact", [
    ("1000", "80", True),            # 12.5 N, exact display
    ("1000", "3", False),            # 333.333... N, rounded display
    ("9.7408265472", "7", True),     # 1.3915466496 N: terminating, 11 significant digits
    ("10", "3", False),              # 3.333... N: never terminates
])
def test_n07_f_exact_times_d_is_p_and_a_rounded_display_never_has_to_be(P, d, exact):
    F_exact = force.exact_force(Fraction(P), Fraction(d))
    assert F_exact * Fraction(d) == Fraction(P)                 # rational identity, always
    F_display, display_exact = force.format_force(F_exact)
    assert display_exact is exact
    assert (Fraction(F_display) * Fraction(d) == Fraction(P)) is exact


# ==========================================================================
# 2. backward compatibility and non-interference (correction B)
# ==========================================================================
def test_c01_the_moment_identity_and_every_governed_artifact_are_unchanged():
    assert record_store.planar_moment_method_identity() == BASE_MOMENT_IDENTITY
    assert (moment.METHOD_ID, moment.METHOD_VERSION) == BASE_MOMENT_IDENTITY[:2]
    assert moment.load_artifact()["artifact_version"] == "1"
    assert force.load_artifact()["artifact_version"] == "1"
    assert dc.load_artifact()["artifact_version"] == "14"
    for path, digest in BASE_FILE_SHA256.items():
        assert _raw_sha(path) == digest, path


def test_c02_a_configuration_saved_under_the_base_identity_stays_current(mech_client):
    c, sid = mech_client
    _save(c, sid, _evaluate(c, sid))
    row = webapp._get_store()._conn.execute(
        "SELECT * FROM planar_moment_revisions").fetchone()
    assert all(str(part) in json.dumps(list(row), default=str) for part in BASE_MOMENT_IDENTITY)
    status, raw = _page(c, sid)
    assert status == 200 and _state(raw) == ["CURRENT"] and _value(raw) == EXPECTED


def test_c03_the_standalone_required_force_page_is_unchanged(mech_client):
    c, sid = mech_client
    r = c.post("/session/%s/planar-required-force" % sid, data=_force_form(M_target="1000", d_perp="80"))
    body = r.get_data(as_text=True)
    assert r.status_code == 200 and "12.5 N" in body
    assert ui_text.text("UI_CAP13F_DECL_TARGET_MOMENT", "en") in _html.unescape(body)
    assert ui_text.text("UI_PMF_DECL_TARGET_MOMENT", "en") not in _html.unescape(body)
    assert "data-pmf" not in body
    # the standalone form still takes M_target from the inventor
    assert 'name="value_M_target"' in c.get("/session/%s/planar-required-force" % sid).get_data(as_text=True)


# ==========================================================================
# 3. the web step
# ==========================================================================
def _step_link(raw):
    m = re.search(r'href="([^"]*/required-force\?head=[0-9]+)" data-pm-required-force', raw)
    return _html.unescape(m.group(1)) if m else None


def _saved(c, sid, **over):
    assert _save(c, sid, _evaluate(c, sid, **over)).status_code == 200
    status, raw = _page(c, sid)
    return _items(raw)[0], raw


def _step_form(body):
    block = body.split("data-pmf-form", 1)[1].split("</form>", 1)[0]
    hidden = {n: _html.unescape(v) for n, v in re.findall(
        r'<input type="hidden" name="([^"]+)" value="([^"]*)"', block)}
    hidden.pop("csrf_token", None)
    return hidden


def _answers(d_perp="250", confirm=("confirm_same_point", "confirm_size_only"), **over):
    data = {k: v for k, v in _force_form(d_perp=d_perp).items() if k != "value_M_target"}
    for field in confirm:
        data[field] = "yes"
    data.update(over)
    return data


def _post(c, sid, declaration_id, body, **kw):
    data = dict(_step_form(body), **_answers(**kw))
    return c.post(STEP % (sid, declaration_id), data=data)


def _result(body):
    m = re.search(r'data-pmf-result-value><bdi dir="ltr">([^<]*)</bdi>', body)
    return m.group(1) if m else None


def test_w01_the_step_is_offered_for_a_current_item_and_shows_p_and_m_apart(mech_client):
    c, sid = mech_client
    declaration_id, raw = _saved(c, sid, F="1.23456", d_perp="7.89012")
    link = _step_link(raw)
    assert link == STEP % (sid, declaration_id) + "?head=0"
    r = c.get(link)
    body = _html.unescape(r.get_data(as_text=True))
    assert r.status_code == 200
    assert re.search(r"data-pmf-product>9\.7408265472 N·mm<", body)
    assert re.search(r"data-pmf-computed-moment>9\.740826547200001 N·mm<", body)
    assert ui_text.text("UI_PMF_P_MEANING", "en") in body
    assert moment.EXACT_INPUT_PRODUCT_ID in body
    # P exceeds the unchanged M_target grammar (10 fraction digits): refused, no form
    assert 'data-pmf-refusal="UI_PMF_MSG_NOT_REPRESENTABLE"' in body and "data-pmf-form" not in body


def test_w02_a_lossless_transfer_equals_the_standalone_page_given_p(mech_client):
    c, sid = mech_client
    declaration_id, raw = _saved(c, sid)                  # 12.5 N x 80 mm -> P = 1000
    page = c.get(_step_link(raw)).get_data(as_text=True)
    form = page.split("data-pmf-form", 1)[1].split("</form>", 1)[0]
    assert "checked" not in form and 'name="value_M_target"' not in form
    assert re.search(r"data-pmf-product>1000 N·mm<", page)
    before = webapp._get_store()._conn.execute("SELECT COUNT(*) FROM planar_moment_revisions").fetchone()
    for d_perp, shown in (("250", "4 N"), ("3", "333.333333333 N")):
        r = _post(c, sid, declaration_id, page, d_perp=d_perp)
        body = r.get_data(as_text=True)
        assert r.status_code == 200 and _result(body) == shown
        twin = c.post("/session/%s/planar-required-force" % sid,
                      data=_force_form(M_target="1000", d_perp=d_perp)).get_data(as_text=True)
        assert re.search(r'data-cap13f-result-value><bdi dir="ltr">([^<]*)<', twin).group(1) == shown
        exactness = re.search(r'data-pmf-exactness="(\w+)"', body).group(1)
        assert exactness == re.search(r'data-cap13f-exactness="(\w+)"', twin).group(1)
        assert ui_text.text("UI_PMF_TRANSFER_DISCLOSURE", "en") in _html.unescape(body)
    after = webapp._get_store()._conn.execute("SELECT COUNT(*) FROM planar_moment_revisions").fetchone()
    assert before == after                                  # nothing persisted


@pytest.mark.parametrize("confirm", [(), ("confirm_same_point",), ("confirm_size_only",)])
def test_w03_both_confirmations_are_needed(mech_client, confirm):
    c, sid = mech_client
    declaration_id, raw = _saved(c, sid)
    page = c.get(_step_link(raw)).get_data(as_text=True)
    r = _post(c, sid, declaration_id, page, confirm=confirm)
    body = r.get_data(as_text=True)
    assert r.status_code == 200 and _result(body) is None
    assert 'data-pmf-error="UI_PMF_MSG_NOT_CONFIRMED"' in body


@pytest.mark.parametrize("over", [
    {"value_M_target": "1000"},                  # the target is never taken from the client
    {"surprise": "x"},
    {"confirm_same_point": "on"},
    {"expected_head": "forged"},
    {"decl_planar": "maybe"},
])
def test_w04_a_malformed_submission_is_refused_and_calculates_nothing(mech_client, over):
    c, sid = mech_client
    declaration_id, raw = _saved(c, sid)
    page = c.get(_step_link(raw)).get_data(as_text=True)
    r = _post(c, sid, declaration_id, page, **over)
    assert r.status_code == 400 and _result(r.get_data(as_text=True)) is None


def test_w05_a_declaration_or_screen_answer_still_decides(mech_client):
    c, sid = mech_client
    declaration_id, raw = _saved(c, sid)
    page = c.get(_step_link(raw)).get_data(as_text=True)
    body = _post(c, sid, declaration_id, page,
                 decl_target_moment=force.ANSWER_DOES_NOT_APPLY).get_data(as_text=True)
    assert _result(body) is None and "UI_CAP13F_OUTCOME_MODEL_NOT_SUPPORTED" in body
    body = _post(c, sid, declaration_id, page, screen_children=force.SCREEN_YES).get_data(as_text=True)
    assert _result(body) is None and "UI_CAP13F_OUTCOME_ENGINEERING_REVIEW_REQUIRED" in body
    body = _post(c, sid, declaration_id, page, d_perp="0").get_data(as_text=True)
    assert _result(body) is None and "UI_CAP13F_OUTCOME_DISTANCE_NOT_POSITIVE" in body


def test_w06_a_correction_makes_the_open_page_stale(mech_client):
    c, sid = mech_client
    declaration_id, raw = _saved(c, sid)
    page = c.get(_step_link(raw)).get_data(as_text=True)
    corrected = _evaluate(c, sid, correct=declaration_id, F="25")
    assert _save(c, sid, corrected).status_code == 200
    r = _post(c, sid, declaration_id, page)
    assert r.status_code == 409 and _result(r.get_data(as_text=True)) is None
    assert 'data-pmf-error="UI_PMF_MSG_STALE"' in r.get_data(as_text=True)
    # the new revision has its own link and its own P
    status, raw = _page(c, sid)
    fresh = c.get(_step_link(raw)).get_data(as_text=True)
    assert re.search(r"data-pmf-product>2000 N·mm<", fresh)
    assert c.get(STEP % (sid, declaration_id) + "?head=0").status_code == 409


def test_w07_a_withdrawn_configuration_gives_no_number_and_no_link(mech_client):
    c, sid = mech_client
    declaration_id, raw = _saved(c, sid)
    page = c.get(_step_link(raw)).get_data(as_text=True)
    block = raw.split("data-pm-withdraw-form", 1)[1].split("</form>", 1)[0]
    data = {n: _html.unescape(v) for n, v in re.findall(
        r'<input type="hidden" name="([^"]+)" value="([^"]*)"', block)}
    data.pop("csrf_token")
    assert c.post(URL % sid + "/withdraw", data=dict(data, withdraw_confirm="yes")).status_code == 200
    status, raw = _page(c, sid)
    assert _step_link(raw) is None
    r = _post(c, sid, declaration_id, page)
    assert r.status_code == 409 and _result(r.get_data(as_text=True)) is None


def test_w08_a_changed_component_gives_no_number_and_no_link(mech_client):
    c, sid = mech_client
    declaration_id, raw = _saved(c, sid)
    page = c.get(_step_link(raw)).get_data(as_text=True)
    store = webapp._get_store()
    comp = store.load_component_inventory_record(sid)[1].records[0]
    _correct_component(store, sid, comp.component_id, 0, "Folding flap, longer")
    status, raw = _page(c, sid)
    assert _state(raw) == ["NEEDS_RECONFIRMATION"] and _step_link(raw) is None
    r = _post(c, sid, declaration_id, page)
    assert r.status_code == 409
    assert 'data-pmf-error="UI_PMF_MSG_NOT_CURRENT"' in r.get_data(as_text=True)


def test_w09_a_changed_method_identity_gives_no_number(mech_client, monkeypatch):
    c, sid = mech_client
    declaration_id, raw = _saved(c, sid)
    real = record_store.planar_moment_method_identity()
    monkeypatch.setattr(record_store, "planar_moment_method_identity",
                        lambda: real[:3] + ("f" * 64,))
    r = c.get(STEP % (sid, declaration_id) + "?head=0")
    assert r.status_code == 409 and "data-pmf-product>" not in r.get_data(as_text=True)


@pytest.mark.parametrize("status_, key", [
    (moment.PRODUCT_INTEGRITY_FAILURE, "UI_PMF_MSG_INTEGRITY"),
    (moment.PRODUCT_NOT_ADMITTED, "UI_PMF_MSG_NOT_ADMITTED"),
])
def test_w10_an_integrity_failure_or_unadmitted_input_passes_nothing_on(mech_client, monkeypatch,
                                                                        status_, key):
    c, sid = mech_client
    declaration_id, raw = _saved(c, sid)
    page = c.get(_step_link(raw)).get_data(as_text=True)
    monkeypatch.setattr(webapp._cap13m, "exact_input_product",
                        lambda values, m: {"status": status_, "text": None, "value": None})
    for r in (c.get(STEP % (sid, declaration_id) + "?head=0"), _post(c, sid, declaration_id, page)):
        body = r.get_data(as_text=True)
        assert 'data-pmf-refusal="%s"' % key in body and "data-pmf-form" not in body
        assert _result(body) is None


@pytest.mark.parametrize("F, d", [("999999999", "99999"), ("0.0000001", "0.0001")])
def test_w11_a_product_outside_the_target_grammar_is_refused_not_rounded(mech_client, F, d):
    c, sid = mech_client
    declaration_id, raw = _saved(c, sid, F=F, d_perp=d)
    body = c.get(_step_link(raw)).get_data(as_text=True)
    assert 'data-pmf-refusal="UI_PMF_MSG_NOT_REPRESENTABLE"' in body
    product = moment.plain_decimal(Fraction(F) * Fraction(d))
    assert ("data-pmf-product>%s N·mm<" % product) in _html.unescape(body)     # shown, never shortened
    assert force.parse_value(product, "M_target") is None


@pytest.mark.parametrize("path, status_", [
    (STEP % ("{sid}", "pmd-" + "0" * 32) + "?head=0", 404),
    (STEP % ("{sid}", "not-an-id") + "?head=0", 400),
    (STEP % ("{sid}", "{decl}") + "?head=x", 400),
    (STEP % ("{sid}", "{decl}"), 400),
])
def test_w12_unknown_or_malformed_targets_are_refused(mech_client, path, status_):
    c, sid = mech_client
    declaration_id, raw = _saved(c, sid)
    r = c.get(path.format(sid=sid, decl=declaration_id))
    assert r.status_code == status_ and "data-pmf-form" not in r.get_data(as_text=True)


def test_w13_another_project_cannot_use_the_step(mech_client):
    c, sid = mech_client
    declaration_id, raw = _saved(c, sid)
    from tests.test_g1_planar_moment_saved_declaration import _client
    other = _client("intruder")
    r = other.get(_step_link(raw))
    assert r.status_code in (302, 403, 404) and "data-pmf" not in r.get_data(as_text=True)


def test_w14_arabic_page(mech_client):
    c, sid = mech_client
    declaration_id, raw = _saved(c, sid)
    assert c.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    body = c.get(_step_link(raw)).get_data(as_text=True)
    # Latin runs are wrapped in <bdi dir="ltr"> on an Arabic page; compare the plain text
    text = " ".join(_html.unescape(re.sub(r"<[^>]+>", "", body)).split())
    assert 'dir="rtl"' in body
    for key in ("UI_PMF_TITLE", "UI_PMF_P_MEANING", "UI_PMF_CONFIRM_SAME_POINT",
                "UI_PMF_CONFIRM_SIZE_ONLY", "UI_PMF_TRANSFER_DISCLOSURE"):
        assert " ".join(ui_text.text(key, "ar").split()) in text, key
    assert re.search(r'<bdi dir="ltr" data-pmf-product>1000 N·mm</bdi>', body)


def test_w15_every_new_string_exists_in_both_languages():
    keys = [k for k in ui_text.UI_STRINGS if k.startswith("UI_PMF_")]
    assert len(keys) == 26
    for key in keys:
        assert ui_text.UI_STRINGS[key]["en"].strip() and ui_text.UI_STRINGS[key]["ar"].strip()
        assert re.search(r"[؀-ۿ]", ui_text.UI_STRINGS[key]["ar"])


def test_w16_the_report_section_is_unchanged(mech_client, monkeypatch):
    c, sid = mech_client
    _saved(c, sid)
    report = c.get("/session/%s/deliverable" % sid)
    body = report.get_data(as_text=True)
    assert report.status_code == 200 and "data-pm-required-force" not in body and "data-pmf" not in body
    assert ui_text.text("UI_PM_REPORT_HEADING", "en") in _html.unescape(body)   # the section is there
    assert ui_text.text("UI_PMF_LINK", "en") not in _html.unescape(body)


def test_w17_the_contracts_quote_the_governed_english_wording():
    def read(name):
        with open(os.path.join(ROOT, "docs", "governance", name), encoding="utf-8") as h:
            return " ".join(h.read().split())
    moment_contract = read("STAGE25_CAP13_PLANAR_SINGLE_FORCE_MOMENT_METHOD_CONTRACT.md")
    force_contract = read("STAGE25_CAP13_PLANAR_REQUIRED_FORCE_METHOD_CONTRACT.md")
    owner_contract = read("SHARED_DETERMINISTIC_CALCULATION_AND_UNITS_OWNER_BOUNDARY_CONTRACT.md")
    assert moment.EXACT_INPUT_PRODUCT_ID in moment_contract
    assert "## 12C. Derived consequence: the exact input product" in moment_contract
    for key in ("UI_PMF_DECL_TARGET_MOMENT", "UI_PMF_CONFIRM_SAME_POINT", "UI_PMF_CONFIRM_SIZE_ONLY",
                "UI_PMF_TRANSFER_DISCLOSURE"):
        assert ui_text.text(key, "en") in force_contract, key
    assert ui_text.text("UI_PMF_P_MEANING", "en") in moment_contract
    assert "G1-MOMENT-TO-REQUIRED-FORCE-01" in owner_contract


def test_w18_more_refusals_and_cross_project_posts(mech_client, monkeypatch):
    c, sid = mech_client
    declaration_id, raw = _saved(c, sid)
    page = c.get(_step_link(raw)).get_data(as_text=True)
    # a duplicated field, a duplicated head, a head with a trailing newline
    data = dict(_step_form(page), **_answers())
    from werkzeug.datastructures import MultiDict
    pairs = MultiDict(list(data.items()) + [("decl_planar", force.ANSWER_APPLIES)])
    assert c.post(STEP % (sid, declaration_id), data=pairs).status_code == 400
    assert c.get(STEP % (sid, declaration_id) + "?head=0&head=0").status_code == 400
    assert c.get(STEP % (sid, declaration_id), query_string={"head": "0\n"}).status_code == 400
    # a malformed confirmation is refused before anything else, even when P would be refused
    assert c.post(STEP % (sid, declaration_id),
                  data=dict(data, confirm_size_only="on")).status_code == 400
    # another account's POST is denied and calculates nothing
    from tests.test_g1_planar_moment_saved_declaration import _client
    intruder = _client("intruder-post")
    r = intruder.post(STEP % (sid, declaration_id), data=data)
    assert r.status_code in (302, 403, 404) and "data-pmf" not in r.get_data(as_text=True)


def test_w19_an_unreadable_history_is_unavailable(mech_client, monkeypatch):
    c, sid = mech_client
    declaration_id, raw = _saved(c, sid)
    store = webapp._get_store()

    def broken(project_id):
        raise RuntimeError("unreadable")
    monkeypatch.setattr(store, "load_planar_moments", broken)
    r = c.get(STEP % (sid, declaration_id) + "?head=0")
    body = r.get_data(as_text=True)
    assert r.status_code == 503 and 'data-pmf-error="UI_PMF_MSG_UNAVAILABLE"' in body
    assert "data-pmf-product>" not in body


def test_w20_a_result_unavailable_configuration_gives_no_number(mech_client, monkeypatch):
    c, sid = mech_client
    declaration_id, raw = _saved(c, sid)
    monkeypatch.setattr(moment, "evaluate",
                        lambda captured, binding, **kw: {"outcome": moment.KNOWLEDGE_UNAVAILABLE,
                                                         "owner_state": None,
                                                         "owner_reason": None, "result": None})
    status, raw = _page(c, sid)
    assert _state(raw) == ["RESULT_UNAVAILABLE"] and _step_link(raw) is None
    r = c.get(STEP % (sid, declaration_id) + "?head=0")
    assert r.status_code == 409 and 'data-pmf-error="UI_PMF_MSG_NOT_CURRENT"' in r.get_data(as_text=True)


def test_w21_the_integrity_check_runs_end_to_end_on_the_real_consequence(mech_client, monkeypatch):
    c, sid = mech_client
    declaration_id, raw = _saved(c, sid)
    page = c.get(_step_link(raw)).get_data(as_text=True)
    real = webapp._pm_saved_view

    def drifted(*args, **kwargs):
        view = real(*args, **kwargs)
        for item in view["items"]:
            if item["moment_value"] is not None:
                item["moment_value"] *= 1 + 1e-12              # far outside the proven bound
        return view
    monkeypatch.setattr(webapp, "_pm_saved_view", drifted)
    for r in (c.get(STEP % (sid, declaration_id) + "?head=0"), _post(c, sid, declaration_id, page)):
        body = r.get_data(as_text=True)
        assert 'data-pmf-refusal="UI_PMF_MSG_INTEGRITY"' in body and _result(body) is None
        assert "data-pmf-product>" not in body                       # no P is shown
