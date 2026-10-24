# -*- coding: utf-8 -*-
"""CAP12-ELECTRONICS-ROOT-01 — the existing CAP-12 form mock-up advisory for a
confirmed single-domain Electrical / Electronics project.

Owner-authorized bounded increment: the governed artifact (schema 2.0) admits
exactly the closed pair ``mechanical`` and ``electronics_electrical`` for the
``form_mockup`` role, with every claim identity, wording, limitation, source
binding and family order unchanged; ``_cap12_gate`` uses the Electronics root
only when the durable composition reads successfully as empty, keeps the
Mechanical-part path for an integrated project in both focus directions, and
offers nothing when the composition is corrupt or unreadable. The component
descriptions stay display-only and nothing is persisted. Synthetic data only.
"""
import copy
import hashlib
import json

import pytest

import web.app as webapp
from engine import cap12_form_mockup as cap12
from engine.cap12_form_mockup import (
    Cap12KnowledgeError, load_artifact, resolve_advisory, validate_artifact)
from tests.test_cap12_form_mockup_advisory import (
    ADV, ELEC_FORM, OK_FORM, SEED, _client_for, _new_client, _page, _post,
    _snapshot, _start, _text_of)
from tests.test_cap13_therm01_integrated_part_eligibility import (
    CTRL, ELEC, MECH, PARTS, _client, _corrupt, _integrated, _part_line)
from web import ui_text

HOSTILE = '<script>alert("x")</script> ‮Enclosure'

# SHA-256 of the claims (without their applicability key) and the source
# records of the schema 1.0 artifact this increment replaced: the wording,
# limitations, source bindings and order are byte-for-byte unchanged.
_CLAIMS_AND_SOURCES_DIGEST = (
    "d1ab0536c6a2e49b227198a58fd39d16bf154c9576c657997651d55cc2dec2a1")


@pytest.fixture
def elec():
    c, _aid = _client_for("cap12-elec-root@example.com")
    return c, _start(c, ELEC_FORM)


def _artifact():
    return json.loads(json.dumps(load_artifact()))


def _advice(body):
    """The advisory result, without the echoed (display-only) descriptors."""
    start = body.index('data-cap12-result="available"')
    section = body[start:body.index("data-cap12-ack", start)]
    if "data-cap12-shown" in section:
        cut = section.index("data-cap12-shown")
        section = section[:cut] + section[section.index("</p>", cut):]
    return _text_of(section)


def _resolver_spy(monkeypatch):
    calls = []
    real = cap12.resolve_advisory

    def spy(domain, role, artifact=None):
        calls.append((domain, role))
        return real(domain, role, artifact)
    monkeypatch.setattr(cap12, "resolve_advisory", spy)
    return calls


# ==========================================================================
# 1. the governed artifact: closed pair, schema 2.0, claims unchanged
# ==========================================================================
def test_the_applicability_is_exactly_the_closed_pair():
    assert cap12.SUPPORTED_APPLICABILITY == (
        ("mechanical", "form_mockup"), ("electronics_electrical", "form_mockup"))
    data = load_artifact()
    assert data["schema_version"] == cap12.ARTIFACT_SCHEMA_VERSION == "2.0"
    assert data["artifact_version"] == "2.0.0"
    pair = ["mechanical", "electronics_electrical"]
    assert data["scope"] == {"role_category": "form_mockup", "applicable_domains": pair}
    assert all(c["applicable_domains"] == pair for c in data["claims"])
    for domain in ("software", "control_loop", "medical_device", "Mechanical", None):
        assert cap12.supports(domain) is False


def test_claims_sources_and_order_are_unchanged():
    data = load_artifact()
    claims = [{k: v for k, v in c.items() if k != "applicable_domains"}
              for c in data["claims"]]
    blob = json.dumps({"claims": claims, "sources": data["sources"],
                       "source_use_policies": data.get("source_use_policies")},
                      sort_keys=True, ensure_ascii=False)
    assert hashlib.sha256(blob.encode()).hexdigest() == _CLAIMS_AND_SOURCES_DIGEST
    assert [c["claim_id"] for c in data["claims"]] == [
        "cap12:FM:C001", "cap12:FM:C002", "cap12:FM:C003", "cap12:FM:C004",
        "cap12:FM:C005"]


def test_both_admitted_domains_get_identical_advice():
    mech = resolve_advisory("mechanical", "form_mockup")
    elec = resolve_advisory("electronics_electrical", "form_mockup")
    assert mech["state"] == elec["state"] == cap12.STATE_AVAILABLE
    strip = lambda a: {k: v for k, v in a.items() if k != "root_domain"}
    assert strip(mech) == strip(elec)
    assert [a["family_token"] for a in elec["alternatives"]] == [
        "foam_core", "thermoplastic"]


def _mut_old_key(d):
    for c in d["claims"]:
        c["applicable_domain"] = c.pop("applicable_domains")[0]


def _mut_old_scope(d):
    d["scope"] = {"role_category": "form_mockup", "applicable_domain": "mechanical"}


def _mut_old_schema(d): d["schema_version"] = "1.0"
def _mut_reordered_scope(d): d["scope"]["applicable_domains"].reverse()
def _mut_scope_one_domain(d): d["scope"]["applicable_domains"] = ["mechanical"]
def _mut_scope_extra_domain(d): d["scope"]["applicable_domains"].append("software")
def _mut_claim_missing_domain(d): d["claims"][1]["applicable_domains"] = ["mechanical"]
def _mut_claim_extra_domain(d): d["claims"][4]["applicable_domains"].append("software")
def _mut_claim_domain_string(d): d["claims"][0]["applicable_domains"] = "mechanical"
def _mut_scope_extra_key(d): d["scope"]["applicable_domain"] = "mechanical"


TAMPERS = [v for k, v in sorted(globals().items()) if k.startswith("_mut_")]


@pytest.mark.parametrize("mutate", TAMPERS, ids=lambda f: f.__name__[5:])
def test_a_structure_change_fails_closed(mutate):
    data = _artifact()
    mutate(data)
    with pytest.raises(Cap12KnowledgeError):
        validate_artifact(copy.deepcopy(data))
    for domain in ("mechanical", "electronics_electrical"):
        assert resolve_advisory(domain, "form_mockup", artifact=data) == {
            "state": cap12.STATE_UNABLE, "reason": "KNOWLEDGE_UNAVAILABLE"}


# ==========================================================================
# 2. a confirmed single-domain Electronics project gets the advice
# ==========================================================================
def test_a_single_domain_electronics_project_is_offered_the_advice(elec, monkeypatch):
    c, sid = elec
    assert webapp._get_store().load_project_subsystems(sid) == ()
    assert webapp._cap12_gate(sid) == (ELEC, None)
    assert webapp._cap12_link_offered(sid) is True
    page = _page(c, sid)
    assert "data-cap12-link" in page and (ADV % sid) in page
    get = c.get(ADV % sid).get_data(as_text=True)
    assert "data-cap12-part" not in get
    calls = _resolver_spy(monkeypatch)
    r = _post(c, sid)
    body = r.get_data(as_text=True)
    assert r.status_code == 200 and r.headers["Cache-Control"] == "no-store"
    assert 'data-cap12-result="available"' in body
    assert body.count("data-cap12-alternative") == 2
    assert "data-cap12-part" not in body
    assert calls == [(ELEC, "form_mockup")]


def test_the_electronics_advice_equals_the_mechanical_advice(elec):
    c, sid = elec
    mc, _aid = _client_for("cap12-elec-root-mech@example.com")
    msid = _start(mc, {"idea": SEED, "domain_confirm": MECH})
    assert _advice(_post(c, sid).get_data(as_text=True)) == _advice(
        _post(mc, msid).get_data(as_text=True))


def test_descriptions_never_change_the_advice(elec, monkeypatch):
    c, sid = elec
    calls = _resolver_spy(monkeypatch)
    bodies = [_post(c, sid, component_name=name, component_function=fn)
              .get_data(as_text=True) for name, fn in (
        ("Sensor enclosure", "Shows the outer shape of the sensor box."),
        ("Battery pack", "A working lithium cell holder with a heating element."),
        ("Steel bracket", "Choose aluminium, ABS and a 3 mm wall."),
        ("غلاف الدائرة", "يعرض الشكل الخارجي للجهاز."))]
    advice = [_advice(b) for b in bodies]
    assert all(a == advice[0] for a in advice)
    assert calls == [(ELEC, "form_mockup")] * 4
    for word in ("lithium", "heating", "aluminium", "ABS", "3 mm"):
        assert word not in advice[0]


def test_the_name_is_escaped_and_the_page_is_bilingual(elec):
    c, sid = elec
    body = _post(c, sid, component_name=HOSTILE).get_data(as_text=True)
    assert "<script>alert" not in body and "&lt;script&gt;" in body
    assert 'data-cap12-result="available"' in body
    assert c.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    ar = _post(c, sid).get_data(as_text=True)
    assert 'dir="rtl"' in ar and 'data-cap12-result="available"' in ar
    assert ui_text.text("UI_CAP12_BOUNDARY", "ar") in _text_of(ar)


def test_nothing_is_persisted(elec):
    c, sid = elec
    before = _snapshot(c)
    c.get(ADV % sid)
    _post(c, sid)
    _post(c, sid, role_category="")
    assert _snapshot(c) == before


def test_another_account_anonymous_and_csrf_are_denied(elec, monkeypatch):
    _c, sid = elec
    calls = _resolver_spy(monkeypatch)
    other, _aid = _client_for("cap12-elec-root-other@example.com")
    for client in (other, _new_client()):
        for r in (client.get(ADV % sid), client.post(ADV % sid, data=OK_FORM)):
            assert r.status_code == 302
            assert "data-cap12" not in r.get_data(as_text=True)
    assert webapp.app.test_client().post(ADV % sid, data=OK_FORM).status_code == 403
    assert calls == []


# ==========================================================================
# 3. integrated projects keep the Mechanical-part path in both directions
# ==========================================================================
def test_integrated_projects_keep_their_behaviour_and_attribution():
    ec = _client("cap12-elec-root-int-e")
    esid = _integrated(ec, ELEC)
    domain, part = webapp._cap12_gate(esid)
    assert domain == MECH and part.display_name == PARTS["mech_part_name"]
    assert _part_line(_post(ec, esid).get_data(as_text=True), "cap12") == \
        PARTS["mech_part_name"]
    mc = _client("cap12-elec-root-int-m")
    msid = _integrated(mc, MECH)
    assert webapp._cap12_gate(msid) == (MECH, None)
    assert "data-cap12-part" not in _post(mc, msid).get_data(as_text=True)
    tc = _client("cap12-elec-root-int-3")
    tsid = _integrated(tc, ELEC, **CTRL)
    domain, part = webapp._cap12_gate(tsid)
    assert domain == MECH and part.display_name == PARTS["mech_part_name"]


def test_the_root_allowance_never_bypasses_the_mechanical_part(monkeypatch):
    c = _client("cap12-elec-root-bypass")
    sid = _integrated(c, ELEC)
    monkeypatch.setattr(webapp, "_calc_declared_part", lambda *_a: None)
    assert webapp._cap12_gate(sid) == (None, None)
    assert webapp._cap12_link_offered(sid) is False
    body = _post(c, sid).get_data(as_text=True)
    assert 'data-cap12-result="unable"' in body and "data-cap12-alternative" not in body


@pytest.mark.parametrize("sql", (
    "UPDATE project_subsystems SET domain = 'software' WHERE subsystem_seq = 0",
    "DELETE FROM project_subsystems WHERE subsystem_seq = 0",
))
def test_a_corrupt_composition_is_not_the_single_domain_state(sql, monkeypatch):
    c = _client("cap12-elec-root-corrupt")
    sid = _integrated(c, ELEC)
    _corrupt(sql)
    calls = _resolver_spy(monkeypatch)
    assert webapp._cap12_gate(sid) == (None, None)
    assert webapp._cap12_link_offered(sid) is False
    body = _post(c, sid).get_data(as_text=True)
    assert 'data-cap12-result="unable"' in body and "data-cap12-alternative" not in body
    assert ui_text.text("UI_CAP12_REASON_APPLICABILITY_NOT_ESTABLISHED", "en") in \
        _text_of(body)
    assert calls == [(None, "form_mockup")]


def test_an_unreadable_composition_offers_nothing(elec, monkeypatch):
    c, sid = elec

    def broken(_sid):
        raise OSError("disk I/O error")
    monkeypatch.setattr(webapp._get_store(), "load_project_subsystems", broken)
    assert webapp._cap12_gate(sid) == (None, None)
    assert webapp._cap12_link_offered(sid) is False
    assert 'data-cap12-result="unable"' in _post(c, sid).get_data(as_text=True)


# ==========================================================================
# 4. an unadmitted root reads the approved copy
# ==========================================================================
def test_the_unsupported_domain_copy_is_the_approved_row(elec, monkeypatch):
    assert ui_text.text("UI_CAP12_REASON_UNSUPPORTED_DOMAIN", "en") == \
        "This advisory is not available for this project's domain."
    assert ui_text.text("UI_CAP12_REASON_UNSUPPORTED_DOMAIN", "ar") == \
        "هذه الإرشادات غير متاحة لمجال هذا المشروع."
    c, sid = elec
    store = webapp._get_store()
    real = store.load_reconstruction_inputs
    monkeypatch.setattr(store, "load_reconstruction_inputs", lambda s: dict(
        real(s), confirmed_domain="software"))
    assert webapp._cap12_gate(sid) == ("software", None)
    body = _post(c, sid).get_data(as_text=True)
    assert 'data-cap12-result="unable"' in body
    assert "This advisory is not available for this project&#39;s domain." in body \
        or "This advisory is not available for this project's domain." in _text_of(body)
