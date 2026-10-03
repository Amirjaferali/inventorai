# -*- coding: utf-8 -*-
"""Stage 24 / CAP-12 - Form Mock-up Advisory, Slice 1 (directly owning tests).

ONE optional, advisory, non-binding, request-local capability: for ONE explicitly
declared NON-FUNCTIONAL form mock-up component on a Mechanical-root project, the
CAP-12 owner lists the prototype material families and building-method families
that NASA material describes, or it declines.

The tests press on the boundaries rather than on the happy path alone:
  * the resolver's only inputs are the trusted root domain and the selected role,
    so component text can never steer a material or process;
  * nothing is persisted, no evidence row is written and no project state moves;
  * the governed artifact fails closed when any reference is broken or any
    unexpected field (a grade, a rating) appears;
  * no ranking, no grade or subtype, no number and no suitability claim reaches
    the page in either language;
  * ignoring the capability costs the inventor nothing.
"""
import copy
import inspect
import json
import os
import pickle
import re
import sqlite3

import pytest

from tests.csrf_client import csrf_client
import web.app as webapp
from web.app import app, SESSION_STORE
from web import ui_text
from engine import account_credentials as _acct
from engine import cap12_form_mockup as cap12
from engine.cap12_form_mockup import (
    Cap12KnowledgeError, resolve_advisory, validate_artifact, load_artifact,
    STATE_AVAILABLE, STATE_UNABLE)

PW = "correct horse battery staple"
SEED = ("a manually foldable wheelchair ramp for a home doorway - the inventor "
        "wants the ramp to stay reliably locked in the flat, load-bearing "
        "position and to fold away without tools")
ELEC_FORM = {"idea": "ESP32 microcontroller circuit with a voltage sensor",
             "domain_confirm": "electronics_electrical"}
PROBLEM = (
    "The problem is that cyclists have no reliable brake light. My circuit senses "
    "deceleration with an accelerometer because sudden voltage change on the sensor "
    "indicates braking, so the microcontroller switches the LED because riders "
    "behind need warning.")
ADV = "/session/%s/form-mockup-advisory"
SESSION = "/session/%s"

OK_FORM = {"component_name": "Ramp handle shell",
           "component_function": "Shows the shape of the grip for review.",
           "role_category": "form_mockup"}


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def _new_client():
    app.config["TESTING"] = True
    return csrf_client(app)


def _client_for(email):
    store = webapp._get_account_store()
    aid = _acct.new_account_id()
    store.create_account(aid, _acct.normalize_email(email), _acct.hash_password(PW),
                         "2026-01-01T00:00:00.000000Z", status="active")
    store.mark_email_verified(aid, "2026-01-01T00:00:00.000000Z")
    c = _new_client()
    c.post("/login", data={"email": email, "password": PW})
    return c, aid


def _start(client, form):
    return client.post("/start", data=form).headers["Location"].rsplit("/session/", 1)[-1]


def _page(client, sid):
    r = client.get(SESSION % sid)
    assert r.status_code == 200, r.status_code
    return r.get_data(as_text=True)


def _post(client, sid, **over):
    data = dict(OK_FORM)
    data.update(over)
    return client.post(ADV % sid, data=data)


def _text_of(html):
    """Visible text only: style / script blocks and tags (so attribute values)
    removed."""
    html = re.sub(r"(?is)<(style|script)\b.*?</\1>", " ", html)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html))


def _content_text(html):
    """The page's own content, after the h1: the shared shell (language switch,
    skip link) is not CAP-12 copy."""
    return _text_of(html[html.index("<h1"):])


def _snapshot(client):
    with sqlite3.connect(os.environ["INVENTORAI_DB_PATH"]) as connection:
        database = list(connection.iterdump())
    memory = pickle.dumps(SESSION_STORE)
    return database, memory


@pytest.fixture
def mech():
    c, aid = _client_for("cap12-mech@example.com")
    return c, aid, _start(c, {"idea": SEED, "domain_confirm": "mechanical"})


@pytest.fixture
def elec():
    c, aid = _client_for("cap12-elec@example.com")
    return c, aid, _start(c, ELEC_FORM)


def _artifact():
    return json.loads(json.dumps(load_artifact()))


# ==========================================================================
# 1-2. Mechanical + form_mockup reaches the governed advisory, with at least
#      two independently source-qualified material alternatives
# ==========================================================================
def test_mechanical_form_mockup_reaches_the_governed_advisory():
    result = resolve_advisory("mechanical", "form_mockup")
    assert result["state"] == STATE_AVAILABLE
    assert result["reason"] is None
    assert result["role_category"] == "form_mockup"
    assert result["role_boundary"]["advisory_type"] == "limitation"


def test_at_least_two_source_qualified_material_alternatives_exist():
    result = resolve_advisory("mechanical", "form_mockup")
    alternatives = result["alternatives"]
    assert len(alternatives) >= cap12.MIN_MATERIAL_ALTERNATIVES
    assert [a["family_token"] for a in alternatives] == ["foam_core", "thermoplastic"]
    sources = {s["record_id"]: s for s in load_artifact()["sources"]}
    for alt in alternatives:
        assert alt["processes"], alt["family_token"]
        material = alt["material"]
        source = sources[material["source_ref"]]
        assert source["record_type"] == "source"
        assert source["report_number"] and source["ntrs_document_id"]
        assert sources[source["source_use_policy_ref"]]["record_type"] == "source_use_policy"
        # a pairing is only implied when ONE source supports both halves
        for proc in alt["processes"]:
            assert proc["source_ref"] == material["source_ref"]
    # the two alternatives are supported by two DIFFERENT inspected sources
    assert len({a["material"]["source_ref"] for a in alternatives}) == 2


def test_exactly_the_admitted_families_exist_and_nothing_wider():
    data = load_artifact()
    fams = sorted((c["advisory_type"], c["family_token"]) for c in data["claims"]
                  if c["advisory_type"] != "limitation")
    assert fams == [("material_family", "foam_core"),
                    ("material_family", "thermoplastic"),
                    ("process_family", "additive_fff_fdm"),
                    ("process_family", "manual_cut_and_join")]
    assert cap12.MATERIAL_FAMILY_TOKENS == ("foam_core", "thermoplastic")
    assert cap12.ROLE_CATEGORIES == ("form_mockup",)
    blob = json.dumps(data).lower()
    for absent in ("wood", "mdf", "plywood", "metal family"):
        assert absent not in json.dumps(data["claims"]).lower(), absent


def test_the_route_serves_the_advisory_for_a_mechanical_project(mech):
    c, _aid, sid = mech
    r = _post(c, sid)
    assert r.status_code == 200
    assert r.headers["Cache-Control"] == "no-store"
    body = r.get_data(as_text=True)
    assert 'data-cap12-result="available"' in body
    assert body.count("data-cap12-alternative") >= 2


# ==========================================================================
# 3-4. Abstention: unsupported root domain; missing / invalid category
# ==========================================================================
@pytest.mark.parametrize("domain", ["electronics_electrical", "control_loop",
                                    "software", "medical_device", "unknown"])
def test_an_unsupported_root_domain_abstains(domain):
    result = resolve_advisory(domain, "form_mockup")
    assert result == {"state": STATE_UNABLE, "reason": "UNSUPPORTED_DOMAIN"}


@pytest.mark.parametrize("domain", [None, "", "   ", 5])
def test_an_unestablished_root_domain_abstains(domain):
    assert resolve_advisory(domain, "form_mockup") == {
        "state": STATE_UNABLE, "reason": "APPLICABILITY_NOT_ESTABLISHED"}


@pytest.mark.parametrize("role,reason", [
    (None, "NO_CATEGORY"), ("", "NO_CATEGORY"),
    ("foam_core", "INVALID_CATEGORY"), ("FORM_MOCKUP", "INVALID_CATEGORY"),
    (" form_mockup", "INVALID_CATEGORY"), ("thermoplastic", "INVALID_CATEGORY"),
    (5, "INVALID_CATEGORY"), (["form_mockup"], "INVALID_CATEGORY")])
def test_a_missing_or_invalid_category_abstains(role, reason):
    assert resolve_advisory("mechanical", role) == {
        "state": STATE_UNABLE, "reason": reason}


def test_an_electronics_project_gets_the_unable_page_not_advice(elec):
    c, _aid, sid = elec
    body = _post(c, sid).get_data(as_text=True)
    assert 'data-cap12-result="unable"' in body
    assert "data-cap12-alternative" not in body
    assert ui_text.text("UI_CAP12_REASON_UNSUPPORTED_DOMAIN", "en") in _text_of(body)


def test_the_route_abstains_when_no_category_is_selected(mech):
    c, _aid, sid = mech
    body = _post(c, sid, role_category="").get_data(as_text=True)
    assert 'data-cap12-result="unable"' in body
    assert "data-cap12-alternative" not in body
    assert ui_text.text("UI_CAP12_REASON_NO_CATEGORY", "en") in _text_of(body)


def test_the_route_abstains_on_an_invented_category(mech):
    c, _aid, sid = mech
    body = _post(c, sid, role_category="metal_bracket").get_data(as_text=True)
    assert 'data-cap12-result="unable"' in body
    assert "data-cap12-alternative" not in body


# ==========================================================================
# 5. Owner free text cannot alter technical selection
# ==========================================================================
def test_the_resolver_takes_only_the_domain_and_the_role():
    params = list(inspect.signature(resolve_advisory).parameters)
    assert params == ["root_domain", "role_category", "artifact"]
    assert list(inspect.signature(cap12.supports).parameters) == [
        "root_domain", "role_category"]


def test_component_text_never_reaches_the_resolver(mech, monkeypatch):
    c, _aid, sid = mech
    calls = []
    real = webapp._cap12.resolve_advisory

    def spy(*args, **kwargs):
        calls.append((args, kwargs))
        return real(*args, **kwargs)

    monkeypatch.setattr(webapp._cap12, "resolve_advisory", spy)
    _post(c, sid, component_name="Aluminium bracket carrying a 40 kg load",
          component_function="structural wood panel in ABS, 3 mm thick")
    assert calls == [(("mechanical", "form_mockup"), {})]


def test_keyword_bait_in_component_text_changes_nothing(mech):
    c, _aid, sid = mech

    def families(body):
        return (re.findall(r'data-cap12-material>([^<]+)<', body),
                re.findall(r'data-cap12-process>([^<]+)<', body))

    base = _post(c, sid).get_data(as_text=True)
    for name, function in (
            ("Steel gear, 12 mm thick", "carries 500 N, ABS and PLA and nylon"),
            ("Wood and MDF panel", "plywood enclosure for mains electronics"),
            ("Heat sink", "food-contact medical implant in titanium")):
        other = _post(c, sid, component_name=name,
                      component_function=function).get_data(as_text=True)
        assert families(other) == families(base)
        assert families(base)[0] == ["Foam core", "Thermoplastic"]


# ==========================================================================
# 6-8. No persistence, no Manufacturing Evidence row, no state mutation
# ==========================================================================
def test_nothing_is_persisted_by_get_or_post(mech):
    c, _aid, sid = mech
    before = _snapshot(c)
    assert c.get(ADV % sid).status_code == 200
    assert _post(c, sid).status_code == 200
    assert _post(c, sid, role_category="").status_code == 200
    assert _post(c, sid, component_name="").status_code == 400
    assert _snapshot(c) == before


def test_no_manufacturing_evidence_row_is_written(mech):
    c, _aid, sid = mech
    store = webapp._get_store()
    assert tuple(store.load_readiness_evidence(sid)) == ()
    _post(c, sid, component_name="Ramp handle shell")
    assert tuple(store.load_readiness_evidence(sid)) == ()


def test_no_readiness_progression_or_session_state_changes(mech):
    c, _aid, sid = mech
    state = SESSION_STORE[sid]["state"]
    marker = (state.iteration, pickle.dumps(state.__dict__), state.domain)
    _post(c, sid)
    _post(c, sid, role_category="")
    after = SESSION_STORE[sid]["state"]
    assert (after.iteration, pickle.dumps(after.__dict__), after.domain) == marker


def test_the_module_and_route_write_nothing():
    module = open(cap12.__file__.replace(".pyc", ".py"), encoding="utf-8").read()
    for writer in ("open(target, \"w\"", "write(", "sqlite", "_get_store", "requests",
                   "urllib", "socket", "random", "datetime", "os.environ"):
        assert writer not in module, writer
    app_source = open(os.path.join(os.path.dirname(__file__), "..", "web", "app.py"),
                      encoding="utf-8").read()
    start = app_source.index("def cap12_form_mockup_advisory_post")
    route = app_source[start:app_source.index("# ====", start)]
    for banned in ("append", "save_", "write", "set_", "SESSION_STORE", "redirect"):
        assert banned not in route, banned


# ==========================================================================
# 9. No rank / best / preferred wording
# ==========================================================================
BANNED_RANKING = ("best", "preferred", "optimal", "safest", "strongest",
                  "cheapest", "cheaper", "rank", "recommended", "top choice",
                  "first choice", "most suitable", "ideal choice")
BANNED_RANKING_AR = ("الأفضل", "الأمثل", "الأقوى", "الأرخص", "الأكثر أمانًا",
                     "مُوصى", "موصى به")


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_no_ranking_or_best_wording_in_any_cap12_copy(lang):
    banned = BANNED_RANKING if lang == "en" else BANNED_RANKING_AR
    offenders = []
    for key, entry in ui_text.UI_STRINGS.items():
        if key.startswith("UI_CAP12_"):
            for token in banned:
                if token in entry[lang].lower():
                    offenders.append((key, token))
    assert not offenders, offenders


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_no_ranking_wording_on_the_rendered_advisory(mech, lang):
    c, _aid, sid = mech
    c.post("/ui-language", data={"lang": lang})
    text = _text_of(_post(c, sid).get_data(as_text=True)).lower()
    for token in (BANNED_RANKING if lang == "en" else BANNED_RANKING_AR):
        assert token not in text, token
    assert ui_text.text("UI_CAP12_ALTERNATIVES_NOTE", lang).lower() in text


# ==========================================================================
# 10. CAP-13 prohibited fields are absent
# ==========================================================================
CAP13_FIELDS = ("grade", "alloy", "subtype", "thickness", "tolerance",
                "dimension", "load", "stress", "safety_factor", "conductor",
                "temperature", "rating", "strength", "specification",
                "suitability", "verdict", "brand", "sku", "vendor", "price",
                "polymer")


def test_no_cap13_field_exists_in_the_artifact_or_the_result():
    data = load_artifact()
    keys = set()
    for claim in data["claims"]:
        keys |= set(claim)
    for source in data["sources"]:
        keys |= set(source)
    result = resolve_advisory("mechanical", "form_mockup")
    keys |= set(result)
    for alt in result["alternatives"]:
        keys |= set(alt) | set(alt["material"])
    for key in keys:
        for banned in CAP13_FIELDS:
            assert banned not in key.lower(), (key, banned)


def test_an_added_cap13_style_field_is_refused_by_the_validator():
    for field in ("grade", "thickness_mm", "load_rating", "material_grade"):
        data = _artifact()
        data["claims"][1][field] = "x"
        with pytest.raises(Cap12KnowledgeError):
            validate_artifact(data)


def test_the_advisory_names_no_grade_number_or_specific_polymer(mech):
    c, _aid, sid = mech
    body = _post(c, sid).get_data(as_text=True)
    advisory = body[body.index('<div class="fam" data-cap12-role-boundary'):
                    body.index('<ul class="sources"')]
    text = _text_of(advisory)
    # "3D printing" is the only digit the governed wording may carry
    assert not re.search(r"\d", re.sub(r"\b3D\b", "", text)), "a number reached the advisory"
    for token in (r"\bABS\b", r"\bPLA\b", r"\bPETG\b", r"\bPEI\b", r"\bPEEK\b",
                  r"polycarbonate", r"\bnylon\b", r"\bUltem\b", r"\bwood\b",
                  r"\bMDF\b", r"\baluminum\b", r"\baluminium\b", r"\bsteel\b"):
        assert not re.search(token, text, re.I), token


def test_the_boundary_statement_is_always_rendered(mech, elec):
    for client, _aid, sid in (mech, elec):
        for body in (client.get(ADV % sid).get_data(as_text=True),
                     _post(client, sid).get_data(as_text=True)):
            assert ui_text.text("UI_CAP12_BOUNDARY", "en") in _text_of(body)
    mc, _a, msid = mech
    available = _post(mc, msid).get_data(as_text=True)
    assert ui_text.text("UI_CAP12_PROTOTYPE_WARNING", "en") in _text_of(available)


# ==========================================================================
# 11. EN / AR render correctly
# ==========================================================================
def test_every_cap12_string_has_both_languages():
    keys = [k for k in ui_text.UI_STRINGS if k.startswith("UI_CAP12_")]
    assert len(keys) > 30
    for key in keys:
        for lang in ("en", "ar"):
            assert ui_text.UI_STRINGS[key].get(lang, "").strip(), (key, lang)
    for key in keys:
        if key.startswith("UI_CAP12_CLAIM_"):
            assert re.search(r"[؀-ۿ]", ui_text.UI_STRINGS[key]["ar"]), key


def test_english_copy_is_pinned_to_the_governed_claims():
    for claim in load_artifact()["claims"]:
        suffix = claim["claim_id"].rsplit(":", 1)[-1]
        assert ui_text.UI_STRINGS["UI_CAP12_CLAIM_%s_FACT" % suffix]["en"] == claim["fact"]
        assert (ui_text.UI_STRINGS["UI_CAP12_CLAIM_%s_LIMITATION" % suffix]["en"]
                == claim["limitation"])


def test_english_rendering(mech):
    c, _aid, sid = mech
    text = _content_text(_post(c, sid).get_data(as_text=True))
    for key in ("UI_CAP12_TITLE", "UI_CAP12_RESULT_HEADING", "UI_CAP12_BOUNDARY",
                "UI_CAP12_PROTOTYPE_WARNING", "UI_CAP12_SOURCES_NOTE",
                "UI_CAP12_ACK", "UI_CAP12_FAMILY_FOAM_CORE",
                "UI_CAP12_PROCESS_ADDITIVE_FFF_FDM", "UI_CAP12_CLAIM_C002_FACT"):
        assert ui_text.text(key, "en") in text, key
    assert not re.search(r"[؀-ۿ]", text)


def test_arabic_rendering_and_direction(mech):
    c, _aid, sid = mech
    c.post("/ui-language", data={"lang": "ar"})
    body = _post(c, sid, component_name="مقبض المنحدر",
                 component_function="يُظهر شكل المقبض للمراجعة.").get_data(as_text=True)
    text = _text_of(body)
    for key in ("UI_CAP12_TITLE", "UI_CAP12_RESULT_HEADING", "UI_CAP12_BOUNDARY",
                "UI_CAP12_PROTOTYPE_WARNING", "UI_CAP12_ACK",
                "UI_CAP12_FAMILY_FOAM_CORE", "UI_CAP12_CLAIM_C004_FACT",
                "UI_CAP12_CLAIM_C005_LIMITATION"):
        assert ui_text.text(key, "ar") in text, key
    for key in ("UI_CAP12_RESULT_HEADING", "UI_CAP12_BOUNDARY",
                "UI_CAP12_PROTOTYPE_WARNING", "UI_CAP12_CLAIM_C002_FACT"):
        assert ui_text.text(key, "en") not in text, key
    assert "مقبض المنحدر" in text
    assert re.search(r'<bdi dir="auto" data-cap12-shown-name>', body)
    assert 'dir="rtl"' in body


def test_no_raw_internal_token_is_shown_where_a_label_exists(mech):
    c, _aid, sid = mech
    for lang in ("en", "ar"):
        c.post("/ui-language", data={"lang": lang})
        text = _text_of(_post(c, sid).get_data(as_text=True))
        for token in ("foam_core", "manual_cut_and_join", "additive_fff_fdm",
                      "form_mockup", "cap12:", "cap12_", "UI_CAP12",
                      "material_family", "process_family", "AVAILABLE",
                      "UNABLE_TO_RECOMMEND", "KNOWLEDGE_UNAVAILABLE"):
            assert token not in text, (lang, token)


def test_user_text_is_html_escaped(mech):
    c, _aid, sid = mech
    body = _post(c, sid, component_name="<script>alert(1)</script>",
                 component_function="<img src=x onerror=1>").get_data(as_text=True)
    assert "<script>alert(1)</script>" not in body
    assert "&lt;script&gt;" in body
    assert "<img src=x" not in body


# ==========================================================================
# 12. Source / provenance references resolve; tampering fails closed
# ==========================================================================
def test_every_reference_resolves_and_every_source_is_exactly_identified():
    data = load_artifact()
    sources = {s["record_id"]: s for s in data["sources"]}
    claims = {c["claim_id"]: c for c in data["claims"]}
    reports = {s["report_number"]: s["ntrs_document_id"] for s in data["sources"]
               if s["record_type"] == "source"}
    assert reports == {"NASA-CR-196533": "19950012552",
                       "NASA/SP-2015-624": "20160000818",
                       "NASA/TM-2016-219344": "20170000214"}
    for claim in claims.values():
        assert claim["source_ref"] in sources
        assert claim["source_use_policy_ref"] in sources
        assert claim["claim_id"] in sources[claim["source_ref"]]["supports_claim_ids"]
    for source in sources.values():
        assert source["inspection_basis"] == "LEAD_SUPPLIED"
        assert source["paraphrase_only_limitation"]
        assert source["third_party_material_exclusion"]
        assert source["no_endorsement_limitation"]
        for cid in source["supports_claim_ids"]:
            assert claims[cid]["source_ref"] == source["record_id"]
    policy = next(s for s in data["sources"] if s["record_type"] == "source_use_policy")
    assert policy["acknowledgement"] == "Reference source material: NASA"


def test_the_artifact_is_not_a_domain_pack_or_in_the_pack_provenance():
    assert not os.path.exists(os.path.join(
        os.path.dirname(__file__), "..", "domains", "cap12"))
    prov = open(os.path.join(os.path.dirname(__file__), "..", "domains",
                             "domain_provenance.json"), encoding="utf-8").read()
    assert "cap12" not in prov.lower()
    from engine.domain_registry import load_registry
    assert not any("cap12" in pack_id for pack_id in load_registry("domains/"))
    for pack in ("mechanical", "electronics_electrical"):
        text = open(os.path.join(os.path.dirname(__file__), "..", "domains", pack,
                                 "domain.json"), encoding="utf-8").read()
        assert "form_mockup" not in text and "foam" not in text.lower()


def _mut_unknown_source(d): d["claims"][1]["source_ref"] = "cap12:SR999"
def _mut_unknown_policy(d): d["claims"][1]["source_use_policy_ref"] = "cap12:SU999"
def _mut_policy_is_a_source(d): d["claims"][1]["source_use_policy_ref"] = "cap12:SR001"
def _mut_source_forgets_claim(d): d["sources"][1]["supports_claim_ids"].remove("cap12:FM:C002")
def _mut_source_lists_foreign_claim(d): d["sources"][0]["supports_claim_ids"].append("cap12:FM:C004")
def _mut_pair_across_sources(d): d["claims"][1]["process_family_refs"] = ["additive_fff_fdm"]
def _mut_missing_report(d): del d["sources"][1]["report_number"]
def _mut_blank_ntrs(d): d["sources"][2]["ntrs_document_id"] = " "
def _mut_basis(d): d["sources"][0]["inspection_basis"] = "MODEL_GENERATED"
def _mut_blank_exclusion(d): d["sources"][0]["third_party_material_exclusion"] = ""
def _mut_family_token(d): d["claims"][1]["family_token"] = "wood_mdf"
def _mut_domain(d): d["claims"][2]["applicable_domain"] = "electronics_electrical"
def _mut_role(d): d["claims"][2]["role_category"] = "enclosure"
def _mut_dup_claim(d): d["claims"][2]["claim_id"] = d["claims"][1]["claim_id"]
def _mut_advisory_type(d): d["claims"][1]["advisory_type"] = "recommendation"
def _mut_limitation_family(d): d["claims"][0]["family_token"] = "foam_core"
def _mut_scope(d): d["scope"]["applicable_domain"] = "electronics_electrical"
def _mut_artifact_id(d): d["artifact_id"] = "something_else"
def _mut_version(d): d["schema_version"] = "9.9"
def _mut_extra_top(d): d["recommendation_rank"] = ["foam_core"]
def _mut_blank_fact(d): d["claims"][1]["fact"] = ""
def _mut_blank_limitation(d): d["claims"][3]["limitation"] = "  "
def _mut_ref_to_limitation_family(d): d["claims"][2]["process_family_refs"] = ["manual_cut_and_join"]


TAMPERS = [v for k, v in sorted(globals().items()) if k.startswith("_mut_")]


@pytest.mark.parametrize("mutate", TAMPERS, ids=lambda f: f.__name__[5:])
def test_tampering_fails_closed(mutate):
    data = _artifact()
    mutate(data)
    with pytest.raises(Cap12KnowledgeError):
        validate_artifact(data)
    assert resolve_advisory("mechanical", "form_mockup", artifact=data) == {
        "state": STATE_UNABLE, "reason": "KNOWLEDGE_UNAVAILABLE"}


def test_a_missing_or_corrupt_artifact_file_fails_closed(tmp_path, monkeypatch):
    bad = tmp_path / "bad.json"
    bad.write_text("{not json", encoding="utf-8")
    for path in (tmp_path / "missing.json", bad):
        monkeypatch.setattr(cap12, "ARTIFACT_PATH", path)
        assert resolve_advisory("mechanical", "form_mockup") == {
            "state": STATE_UNABLE, "reason": "KNOWLEDGE_UNAVAILABLE"}


def test_the_resolver_returns_copies_not_governed_truth():
    first = resolve_advisory("mechanical", "form_mockup")
    first["alternatives"][0]["material"]["fact"] = "altered"
    first["sources"][0]["source_title"] = "altered"
    again = resolve_advisory("mechanical", "form_mockup")
    assert again["alternatives"][0]["material"]["fact"] != "altered"
    assert again["sources"][0]["source_title"] != "altered"


# ==========================================================================
# 13. Incomplete knowledge fails closed rather than offering a pseudo-choice
# ==========================================================================
def _drop(data, claim_ids, source_ids=()):
    data["claims"] = [c for c in data["claims"] if c["claim_id"] not in claim_ids]
    data["sources"] = [s for s in data["sources"] if s["record_id"] not in source_ids]


def test_one_material_direction_is_never_offered_as_a_choice():
    data = _artifact()
    _drop(data, {"cap12:FM:C004", "cap12:FM:C005"}, {"cap12:SR003"})
    validate_artifact(data)          # structurally consistent, but incomplete
    assert resolve_advisory("mechanical", "form_mockup", artifact=data) == {
        "state": STATE_UNABLE, "reason": "INSUFFICIENT_ALTERNATIVES"}


def test_a_material_without_a_process_does_not_count_as_an_alternative():
    data = _artifact()
    data["claims"][1]["process_family_refs"] = []
    assert resolve_advisory("mechanical", "form_mockup", artifact=data) == {
        "state": STATE_UNABLE, "reason": "INSUFFICIENT_ALTERNATIVES"}


def test_a_missing_role_boundary_fails_closed():
    data = _artifact()
    _drop(data, {"cap12:FM:C001"}, {"cap12:SR001"})
    assert resolve_advisory("mechanical", "form_mockup", artifact=data) == {
        "state": STATE_UNABLE, "reason": "INSUFFICIENT_ALTERNATIVES"}


def test_a_dangling_process_reference_fails_closed():
    data = _artifact()
    _drop(data, {"cap12:FM:C005"})
    data["sources"][2]["supports_claim_ids"].remove("cap12:FM:C005")
    assert resolve_advisory("mechanical", "form_mockup", artifact=data) == {
        "state": STATE_UNABLE, "reason": "KNOWLEDGE_UNAVAILABLE"}


def test_the_route_shows_the_unable_page_when_knowledge_is_broken(mech, tmp_path,
                                                                  monkeypatch):
    c, _aid, sid = mech
    monkeypatch.setattr(cap12, "ARTIFACT_PATH", tmp_path / "missing.json")
    r = _post(c, sid)
    assert r.status_code == 200
    body = r.get_data(as_text=True)
    assert 'data-cap12-result="unable"' in body
    assert "data-cap12-alternative" not in body
    assert ui_text.text("UI_CAP12_REASON_KNOWLEDGE_UNAVAILABLE", "en") in _text_of(body)


# ==========================================================================
# 14. The core journey stays usable when CAP-12 is ignored (or broken)
# ==========================================================================
def test_the_link_is_optional_and_only_offered_for_a_mechanical_root(mech, elec):
    mc, _a, msid = mech
    ec, _b, esid = elec
    mbody = _page(mc, msid)
    assert "data-cap12-link" in mbody and (ADV % msid) in mbody
    assert "data-cap12-link" not in _page(ec, esid)
    # the link is plain navigation: no CAP-12 advice on the session page itself
    assert "data-cap12-result" not in mbody and "data-cap12-alternative" not in mbody


def test_the_journey_progresses_and_the_report_is_unchanged_without_cap12(
        mech, tmp_path, monkeypatch):
    c, _aid, sid = mech
    monkeypatch.setattr(cap12, "ARTIFACT_PATH", tmp_path / "missing.json")
    page = _page(c, sid)                        # a broken CAP-12 never breaks this
    token = re.search(r'name="answer_token" value="([^"]+)"', page).group(1)
    r = c.post(SESSION % sid, data={"response": PROBLEM, "action": "answered",
                                    "answer_token": token})
    assert r.status_code in (200, 302, 303)
    assert _page(c, sid)
    before = c.get("/session/%s/deliverable" % sid)
    _post(c, sid)
    after = c.get("/session/%s/deliverable" % sid)
    assert before.status_code == after.status_code
    for response in (before, after):
        text = _text_of(response.get_data(as_text=True)).lower()
        for banned in ("form mock-up", "foam core", "thermoplastic", "fff", "cap-12"):
            assert banned not in text, banned


def test_no_cap12_content_in_the_session_report_or_export_surfaces():
    source = open(os.path.join(os.path.dirname(__file__), "..", "web", "app.py"),
                  encoding="utf-8").read()
    for fn in ("def show_deliverable(", "def download_deliverable_pdf(",
               "def _readiness_snapshot_context"):
        assert fn in source, fn
        start = source.index(fn)
        end = min(source.index(marker, start + 10)
                  for marker in ("\ndef ", "\n# ===", "\n@app.route"))
        assert "_cap12" not in source[start:end], fn
    for module in ("engine/deliverable_assembler.py", "engine/read_export_service.py",
                   "engine/readiness_snapshot.py", "engine/commercial_evidence.py",
                   "engine/requirement_quantity.py", "web/cap01_guidance.py",
                   "engine/subsystem_model.py"):
        text = open(os.path.join(os.path.dirname(__file__), "..", module),
                    encoding="utf-8").read()
        assert "cap12_form_mockup" not in text, module


# ==========================================================================
# Request integrity, authorization and bounded input
# ==========================================================================
def test_the_route_is_in_the_r05_inventory():
    from tests.test_r05_request_integrity import MUTATIONS
    assert "/session/<sid>/form-mockup-advisory" in MUTATIONS


def test_csrf_is_enforced():
    c = app.test_client()
    sid = "not-a-project"
    assert c.post(ADV % sid, data=OK_FORM).status_code == 403


def test_another_account_and_anonymous_callers_are_denied(mech):
    _c, _aid, sid = mech
    other, _ = _client_for("cap12-other@example.com")
    anon = _new_client()
    for client in (other, anon):
        for response in (client.get(ADV % sid), _post(client, sid)):
            assert response.status_code == 302
            body = response.get_data(as_text=True)
            assert "data-cap12" not in body and "Foam core" not in body


@pytest.mark.parametrize("over", [
    {"component_name": ""}, {"component_name": "   "},
    {"component_function": ""},
    {"component_name": "x" * 121}, {"component_function": "y" * 501},
    {"component_name": "bad\x00name"}, {"component_name": "bad\x07name"},
    {"component_function": "bad\x00function"}, {"component_name": "line\nbreak"},
])
def test_bounded_descriptor_text_is_enforced_and_nothing_is_produced(mech, over):
    c, _aid, sid = mech
    r = _post(c, sid, **over)
    assert r.status_code == 400
    body = r.get_data(as_text=True)
    assert "data-cap12-error" in body and "data-cap12-result" not in body
    assert "\x00" not in body


def test_the_bounds_accept_the_limits_and_multiline_function(mech):
    c, _aid, sid = mech
    r = _post(c, sid, component_name="n" * 120,
              component_function="line one\nline two\t" + "f" * 470)
    assert r.status_code == 200
    assert 'data-cap12-result="available"' in r.get_data(as_text=True)


def test_unknown_and_repeated_fields_are_refused_whole(mech):
    c, _aid, sid = mech
    for extra in ({"material": "aluminium"}, {"domain": "mechanical"},
                  {"root_domain": "mechanical"}, {"dimension": "10"},
                  {"claim_id": "cap12:FM:C002"}):
        r = _post(c, sid, **extra)
        assert r.status_code == 400
        assert "data-cap12-result" not in r.get_data(as_text=True)
    from werkzeug.datastructures import MultiDict
    repeated = MultiDict(list(OK_FORM.items()) + [("role_category", "form_mockup")])
    r = c.post(ADV % sid, data=repeated)
    assert r.status_code == 400


def test_a_request_supplied_root_domain_is_ignored(elec):
    c, _aid, sid = elec
    r = _post(c, sid, root_domain="mechanical")
    assert r.status_code == 400
    r = _post(c, sid)
    assert 'data-cap12-result="unable"' in r.get_data(as_text=True)


def test_get_renders_the_form_with_the_explicit_empty_choice(mech):
    c, _aid, sid = mech
    body = c.get(ADV % sid).get_data(as_text=True)
    assert 'name="role_category"' in body
    assert re.search(r'<option value="" selected>', body)
    assert 'value="form_mockup"' in body
    assert not re.search(r'<option value="form_mockup"\s+selected', body)
    assert "data-cap12-result" not in body
    assert ui_text.text("UI_CAP12_ROLE_DEFINITION", "en") in _text_of(body)
