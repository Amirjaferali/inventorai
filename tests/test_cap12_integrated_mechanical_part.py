"""CAP12-INTEGRATED-MECHANICAL-PART-01 — the CAP-12 form mock-up advisory for the
inventor-declared Mechanical part of a valid durable integrated invention.

Authority: the Owner-authorized CAP-12 slice recorded in
``docs/governance/ACTIVE_INCREMENT_CONTRACT.md`` and the narrow Stage 15
exception it records. Root eligibility is unchanged; on an integrated
Mechanical + Electrical / Electronics invention whose initial focus is NOT
Mechanical the advisory is offered for the declared Mechanical part, read only
through the PR #785 composition reader and never from the request; the session
link, the advisory page and the POST read ONE decision (``_cap12_gate``); a
missing, corrupt or unreadable composition grants nothing beyond the root
rule; the resolver, its applicability key, its claims and its sources are
unchanged; the part is named, escaped and direction-isolated in EN / AR; the
CAP-09 measurement-planning eligibility stays root-only. Synthetic data only.
"""
import html as _html
import inspect

import pytest

import web.app as webapp
from engine import cap12_form_mockup as cap12
from tests.test_cap12_form_mockup_advisory import (
    ADV, ELEC_FORM, OK_FORM, SEED, _new_client, _page, _post, _snapshot, _start,
    _text_of)
from tests.test_cap13_therm01_integrated_part_eligibility import (
    CTRL, ELEC, HOSTILE, MECH, PARTS, _client, _corrupt, _integrated, _part_line)
from web import ui_text

SC = "/session/%s/success-criteria"


@pytest.fixture
def elec_focus():
    c = _client("cap12-elec-focus")
    return c, _integrated(c, ELEC)


@pytest.fixture
def mech_focus():
    c = _client("cap12-mech-focus")
    return c, _integrated(c, MECH)


def _resolver_spy(monkeypatch):
    calls = []
    real = cap12.resolve_advisory

    def spy(domain, role, artifact=None):
        calls.append((domain, role))
        return real(domain, role, artifact)
    monkeypatch.setattr(cap12, "resolve_advisory", spy)
    return calls


def _advice(body):
    """The advisory result section of a rendered answer (the attribution notice
    sits above it and is not part of the advice)."""
    start = body.index('data-cap12-result="available"')
    return _text_of(body[start:body.index("data-cap12-ack", start)])


# ==========================================================================
# 1. the declared Mechanical part of an Electronics-focus integrated invention
# ==========================================================================
def test_electronics_focus_is_offered_the_advisory_for_its_mechanical_part(elec_focus, monkeypatch):
    c, sid = elec_focus
    domain, part = webapp._cap12_gate(sid)
    assert domain == MECH and part is not None and part.domain == MECH
    assert part.display_name == PARTS["mech_part_name"]
    assert webapp._cap12_root_domain(sid) == ELEC              # the root is unchanged
    assert webapp._cap12_link_offered(sid) is True
    page = _page(c, sid)
    assert "data-cap12-link" in page and (ADV % sid) in page
    get = c.get(ADV % sid).get_data(as_text=True)
    assert _part_line(get, "cap12") == PARTS["mech_part_name"]
    calls = _resolver_spy(monkeypatch)
    r = _post(c, sid)
    body = r.get_data(as_text=True)
    assert r.status_code == 200 and 'data-cap12-result="available"' in body
    assert _part_line(body, "cap12") == PARTS["mech_part_name"]
    assert calls == [(MECH, cap12.ROLE_FORM_MOCKUP)]


def test_the_advice_is_identical_to_the_mechanical_root_advice(elec_focus):
    c, sid = elec_focus
    root_c = _client("cap12-root-compare")
    root_sid = _start(root_c, {"idea": SEED, "domain_confirm": MECH})
    integrated = _post(c, sid).get_data(as_text=True)
    root = _post(root_c, root_sid).get_data(as_text=True)
    assert 'data-cap12-result="available"' in root and "data-cap12-part" not in root
    assert _advice(integrated) == _advice(root)
    assert cap12.resolve_advisory(MECH, cap12.ROLE_FORM_MOCKUP) == cap12.resolve_advisory(
        webapp._cap12_gate(sid)[0], cap12.ROLE_FORM_MOCKUP)


# ==========================================================================
# 2. root eligibility and every other project are unchanged
# ==========================================================================
def test_mechanical_root_projects_keep_exactly_the_root_rule(mech_focus):
    c = _client("cap12-single")
    single = _start(c, {"idea": SEED, "domain_confirm": MECH})
    assert webapp._cap12_gate(single) == (MECH, None)
    mc, msid = mech_focus
    assert webapp._cap12_gate(msid) == (MECH, None)       # root path: no attribution
    for client, sid in ((c, single), (mc, msid)):
        assert webapp._cap12_link_offered(sid) is True
        for body in (client.get(ADV % sid).get_data(as_text=True),
                     _post(client, sid).get_data(as_text=True)):
            assert "data-cap12-part" not in body
        assert 'data-cap12-result="available"' in _post(client, sid).get_data(as_text=True)


def test_a_single_domain_electronics_project_gets_the_root_advice_without_attribution():
    # CAP12-ELECTRONICS-ROOT-01 supersedes the earlier Electronics refusal: a
    # confirmed single-domain Electronics project is offered the same advice on
    # its root, with no part attribution.
    c = _client("cap12-single-elec")
    sid = _start(c, ELEC_FORM)
    assert webapp._cap12_gate(sid) == (ELEC, None)
    assert webapp._cap12_link_offered(sid) is True
    assert "data-cap12-link" in _page(c, sid)
    body = _post(c, sid).get_data(as_text=True)
    assert 'data-cap12-result="available"' in body and "data-cap12-part" not in body


def test_a_three_part_composition_offers_it_for_the_mechanical_part_only():
    c = _client("cap12-three")
    sid = _integrated(c, ELEC, **CTRL)
    domain, part = webapp._cap12_gate(sid)
    assert domain == MECH and part.display_name == PARTS["mech_part_name"]


# ==========================================================================
# 3. fail closed: corrupt, unreadable or missing composition
# ==========================================================================
@pytest.mark.parametrize("sql", (
    "UPDATE project_subsystems SET domain = 'software' WHERE subsystem_seq = 0",
    "DELETE FROM project_subsystems WHERE subsystem_seq = 0",
    "UPDATE project_subsystems SET display_name = ' padded' WHERE subsystem_seq = 0",
    "UPDATE project_subsystems SET subsystem_seq = 7 WHERE subsystem_seq = 0",
))
def test_a_corrupt_composition_grants_no_advice(elec_focus, monkeypatch, sql):
    c, sid = elec_focus
    _corrupt(sql)
    calls = _resolver_spy(monkeypatch)
    # CAP12-ELECTRONICS-ROOT-01: a corrupt composition is NOT the confirmed
    # single-domain state, so the now-admitted Electronics root is not used.
    assert webapp._cap12_gate(sid) == (None, None)
    assert webapp._cap12_link_offered(sid) is False
    get = c.get(ADV % sid).get_data(as_text=True)
    assert "data-cap12-part" not in get
    body = _post(c, sid).get_data(as_text=True)
    assert 'data-cap12-result="unable"' in body and "data-cap12-alternative" not in body
    assert "data-cap12-part" not in body
    assert calls == [(None, cap12.ROLE_FORM_MOCKUP)]      # applicability not established


def test_an_unreadable_composition_grants_no_advice(elec_focus, monkeypatch):
    c, sid = elec_focus

    def broken(_sid):
        raise OSError("disk I/O error")
    monkeypatch.setattr(webapp._get_store(), "load_project_subsystems", broken)
    assert webapp._cap12_gate(sid) == (None, None)
    assert webapp._cap12_link_offered(sid) is False
    body = _post(c, sid).get_data(as_text=True)
    assert 'data-cap12-result="unable"' in body and "data-cap12-part" not in body


def test_parts_without_a_readable_mechanical_part_grant_no_advice(elec_focus, monkeypatch):
    c, sid = elec_focus
    # the composition holds parts, so the project is not single-domain; with no
    # Mechanical part to name, the Electronics root is not a fallback
    monkeypatch.setattr(webapp, "_calc_declared_part", lambda *_a: None)
    assert webapp._cap12_gate(sid) == (None, None)
    assert webapp._cap12_link_offered(sid) is False
    assert 'data-cap12-result="unable"' in _post(c, sid).get_data(as_text=True)


def test_an_empty_composition_read_is_the_single_domain_state(elec_focus, monkeypatch):
    _c, sid = elec_focus
    # the store reads zero rows as an ordinary project; the gate trusts that
    # validated read and nothing else
    monkeypatch.setattr(webapp._get_store(), "load_project_subsystems", lambda _sid: ())
    assert webapp._cap12_gate(sid) == (ELEC, None)
    assert webapp._cap12_link_offered(sid) is True


def test_an_unreadable_root_domain_grants_nothing(elec_focus, monkeypatch):
    c, sid = elec_focus

    def broken(_sid):
        raise OSError("disk I/O error")
    monkeypatch.setattr(webapp._get_store(), "load_reconstruction_inputs", broken)
    domain, part = webapp._cap12_gate(sid)
    # the root is unreadable; only the validated composition can still name the part
    assert domain == MECH and part.display_name == PARTS["mech_part_name"]
    monkeypatch.setattr(webapp, "_calc_declared_part", lambda *_a: None)
    assert webapp._cap12_gate(sid) == (None, None)
    assert webapp._cap12_link_offered(sid) is False


# ==========================================================================
# 4. the request can never supply a part or a domain; authorization; CSRF
# ==========================================================================
def test_the_request_can_never_supply_a_part_or_domain(monkeypatch):
    c = _client("cap12-request-supplied")
    sid = _start(c, ELEC_FORM)
    calls = _resolver_spy(monkeypatch)
    for extra in ({"part_domain": MECH}, {"subsystem_id": "sub-" + "0" * 32},
                  {"confirmed_domain": MECH}, {"domain": MECH}):
        r = c.post(ADV % sid, data=dict(OK_FORM, **extra))
        body = r.get_data(as_text=True)
        assert r.status_code == 400 and "data-cap12-result" not in body
    assert calls == []
    for url in (ADV % sid + "?domain=mechanical", ADV % sid + "?part=mechanical"):
        assert "data-cap12-part" not in c.get(url).get_data(as_text=True)
    src = inspect.getsource(webapp._cap12_gate)
    for access in ("request.form", "request.args", "request.values", "request.json"):
        assert access not in src, access
    assert list(inspect.signature(webapp._cap12_gate).parameters) == ["sid"]


def test_another_account_anonymous_and_csrf_are_denied(elec_focus, monkeypatch):
    _c, sid = elec_focus
    calls = _resolver_spy(monkeypatch)
    for client in (_client("cap12-other"), _new_client()):
        for r in (client.get(ADV % sid), client.post(ADV % sid, data=OK_FORM)):
            assert r.status_code == 302
            assert "data-cap12" not in r.get_data(as_text=True)
            assert PARTS["mech_part_name"] not in r.get_data(as_text=True)
    assert webapp.app.test_client().post(ADV % sid, data=OK_FORM).status_code == 403
    assert calls == []


def test_strict_capture_keeps_its_semantics_and_its_attribution(elec_focus, monkeypatch):
    c, sid = elec_focus
    calls = _resolver_spy(monkeypatch)
    r = c.post(ADV % sid, data=dict(OK_FORM, extra="1"))
    assert r.status_code == 400 and _part_line(r.get_data(as_text=True), "cap12") == \
        PARTS["mech_part_name"]
    r = _post(c, sid, component_name="")
    assert r.status_code == 400 and _part_line(r.get_data(as_text=True), "cap12") == \
        PARTS["mech_part_name"]
    r = _post(c, sid, role_category="")
    body = r.get_data(as_text=True)
    assert 'data-cap12-result="unable"' in body
    assert ui_text.text("UI_CAP12_REASON_NO_CATEGORY", "en") in _text_of(body)
    assert calls == [(MECH, "")]


# ==========================================================================
# 5. nothing persisted; CAP-09 measurement planning keeps its own gate
# ==========================================================================
def test_nothing_is_persisted_on_the_integrated_part_path(elec_focus):
    c, sid = elec_focus
    before = _snapshot(c)
    c.get(ADV % sid)
    _post(c, sid)
    assert _snapshot(c) == before


def test_cap09_measurement_planning_keeps_its_own_gate(elec_focus, mech_focus):
    ec, esid = elec_focus
    mc, msid = mech_focus
    # the Electronics-root integrated project keeps the Electronics measurement guidance ...
    assert webapp._measurement_planning_guidance(esid) is not None
    # ... and, since MEASUREMENT-PLANNING-INTEGRATED-PART-01 (Owner-authorized), the
    # Mechanical-root one shows it for its declared Electronics part, through the
    # measurement-planning gate, never the CAP-12 gate
    assert webapp._measurement_planning_guidance(msid) is not None
    assert webapp._measurement_planning_references(msid) is not None
    src = inspect.getsource(webapp._measurement_planning_domain)
    assert "_cap12_gate" not in src and "_cap12_root_domain" in src


# ==========================================================================
# 6. EN / AR attribution, escaped and direction-isolated
# ==========================================================================
@pytest.mark.parametrize("lang", ("en", "ar"))
def test_attribution_is_escaped_isolated_and_bilingual(lang):
    c = _client("cap12-hostile-%s" % lang)
    sid = _integrated(c, ELEC, mech_part_name=HOSTILE)
    if lang == "ar":
        assert c.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    for body in (c.get(ADV % sid).get_data(as_text=True),
                 _post(c, sid).get_data(as_text=True)):
        assert "<script>alert" not in body
        raw_name = _part_line(body, "cap12")
        assert raw_name is not None and "&lt;script&gt;" in raw_name
        assert _html.unescape(raw_name) == HOSTILE
        assert '<bdi dir="auto" data-cap12-part-name>' in body
        text = _html.unescape(body)
        assert ui_text.text("UI_CAP12_PART_LABEL", lang) in text
        assert ui_text.text("UI_CAP12_PART_NOTE", lang) in text
    if lang == "ar":
        assert 'dir="rtl"' in body


def test_attribution_wording_carries_no_suitability_claim():
    en = ui_text.text("UI_CAP12_PART_NOTE", "en")
    assert "does not establish" in en
    for word in ("is suitable", "is safe", "validated", "is adequate", "approved",
                 "recommended for your"):
        assert word not in en.lower(), word
    assert ui_text.text("UI_CAP12_PART_NOTE", "ar").strip()


def test_the_governed_knowledge_is_unchanged_except_the_governance_note():
    # CAP12-ELECTRONICS-ROOT-01 (schema 2.0) adds the single-domain Electronics
    # root to the closed applicability; the Mechanical key is kept first and
    # the claims are pinned in tests/test_cap12_electronics_root.py.
    data = cap12.load_artifact()
    assert data["scope"] == {"role_category": "form_mockup",
                             "applicable_domains": ["mechanical", "electronics_electrical"]}
    assert cap12.SUPPORTED_APPLICABILITY[0] == ("mechanical", cap12.ROLE_FORM_MOCKUP)
    assert [c["claim_id"] for c in data["claims"]] == [
        "cap12:FM:C001", "cap12:FM:C002", "cap12:FM:C003", "cap12:FM:C004", "cap12:FM:C005"]
    assert "CAP12-INTEGRATED-MECHANICAL-PART-01" in data["governance_note"]
    assert "CAP12-ELECTRONICS-ROOT-01" in data["governance_note"]
