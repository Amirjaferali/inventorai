# -*- coding: utf-8 -*-
"""G1-AI-INTENT-READBACK-CONSUMER-PROOF-01: baseline /start versus an
optional, source-bound pre-creation readback, on synthetic data and preserved
provider replies only (tests/g1_intent_readback_proof.py).

Every journey runs through the UNCHANGED /start route. The readback seam is
test-only; these tests show where it changes what the inventor sees and what
they then do, that its errors are caught only by the inventor's correction,
and that it adds no engineering, provenance, progression or persistence
effect. Development evidence only: no model, prompt or product is qualified.
"""
import json
import os
import re
import sqlite3

import pytest

import tests.g1_intent_readback_proof as rp
import web.app as appmod
from engine.session_reconstruction import reconstruct_readonly_state
from tests.test_t2g_versioned_journey import client, _login  # noqa: F401 — fixture reuse

MECH, EE = "mechanical", "electronics_electrical"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _tables(db):
    con = sqlite3.connect(db)
    try:
        names = [r[0] for r in con.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
        return {n: con.execute('SELECT * FROM "%s"' % n).fetchall() for n in names}
    finally:
        con.close()


def _visible(body):
    body = re.sub(r"<script.*?</script>|<style.*?</style>", "", body, flags=re.S)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", body))


def _post(c, data):
    return c.post("/start", data=data)


def _created(r):
    assert r.status_code == 302, r.status_code
    return r.headers["Location"].rsplit("/", 1)[-1]


def _integrated(c, idea, parts, focus=MECH):
    data = {"idea": idea, "integrated_invention": "yes", "composition_step": "1",
            "composition_answer": "yes", "initial_focus": focus}
    data.update({k: v for k, v in parts.items() if k != "note"})
    return _post(c, data)


def _subsystems(db, sid):
    con = sqlite3.connect(db)
    try:
        cols = [r[1] for r in con.execute("PRAGMA table_info(project_subsystems)")]
        rows = con.execute("SELECT * FROM project_subsystems WHERE project_id=?", (sid,)).fetchall()
        return [dict(zip(cols, r)) for r in rows]
    finally:
        con.close()


def _db_text(db):
    return json.dumps(_tables(db), ensure_ascii=False, default=str)


# ==========================================================================
# 0. the evidence this proof stands on
# ==========================================================================
def test_preserved_readings_are_hash_checked_and_constructed_ones_are_labelled():
    fx = rp.fixture()
    assert "not a fresh or independent holdout" in fx["status"]
    for case in fx["preserved_source"]["cases_used"]:
        idea, reply, source = rp.preserved(case)
        assert source["evidence_ref"].endswith("campaign_02_report.json")
        assert rp.build(idea, reply, source) is not None
    assert fx["constructed"]["H08_incorrect"]["origin"].startswith("CONSTRUCTED_INCORRECT")
    assert "NOT a provider output" in fx["constructed"]["AR01"]["origin"]


def test_the_seam_has_no_provider_route_or_production_caller():
    src = open(os.path.join(ROOT, "tests", "g1_intent_readback_proof.py"), encoding="utf-8").read()
    for forbidden in ("requests", "urllib", "http.client", "openai", "socket", "@app.route",
                      "_create_project_session", "integrate_response", "SESSION_STORE"):
        assert forbidden not in src.split('"""', 2)[2], forbidden
    for folder in ("web", "engine", "scripts"):
        for base, _dirs, files in os.walk(os.path.join(ROOT, folder)):
            for f in files:
                if f.endswith((".py", ".html")):
                    assert "g1_intent_readback_proof" not in open(os.path.join(base, f),
                                                                  encoding="utf-8").read()


# ==========================================================================
# 1. a clear invention keeps the ordinary direct path
# ==========================================================================
def test_a_clear_invention_starts_directly_with_no_extra_confirmation(client):
    c, _app, db = client
    _login(c, _app)
    idea, reply, source = rp.preserved("H23")
    sid = _created(_post(c, {"idea": idea, "domain_confirm": MECH}))
    assert reconstruct_readonly_state(appmod._get_store(), sid).state.domain == MECH
    rb = rp.build(idea, reply, source)
    assert rb is not None and not rb.points_to_integrated
    page = rp.render(rb)
    assert 'data-pointer="none"' in page and "you can also start directly" in page
    assert "data-obstacle" not in page    # nothing about the integrated option is open here


# ==========================================================================
# 2. the ambiguous integrated invention: a genuine part versus what it serves
# ==========================================================================
def test_baseline_lets_an_external_device_become_the_declared_electrical_part(client):
    c, _app, db = client
    _login(c, _app)
    idea, _reply, _src = rp.preserved("H01")
    chooser = _visible(_post(c, {"idea": idea}).get_data(as_text=True))
    assert "did not clearly match one supported domain" in chooser
    for word in ("power tools", "battery fan", "not part"):
        assert word not in chooser.split("Describe your idea", 1)[1].split(idea, 1)[1]
    slip = rp.fixture()["inventor_inputs"]["H01_parts_baseline_mistake"]
    sid = _created(_integrated(c, idea, slip))
    names = {row["domain"]: row["display_name"] for row in _subsystems(db, sid)}
    assert names[EE] == "Power tools"     # accepted as the invention's own part


def test_the_readback_names_the_real_parts_and_points_to_the_existing_option(client):
    c, _app, db = client
    _login(c, _app)
    idea, reply, source = rp.preserved("H01")
    rb = rp.build(idea, reply, source)
    assert rb.points_to_integrated
    kinds = {p.kind: p.quote for p in rb.parts}
    assert "battery fan" in kinds[EE] and "toolbox" in kinds[MECH]
    assert all("power tools" not in p.quote for p in rb.parts)
    page = rp.render(rb)
    assert 'data-pointer="integrated"' in page and "you name each part in your own words" in page
    before = _tables(db)
    assert rp.resolve(rp.issue(rb), rb, idea, "confirm")["scope"] == rp.CONFIRMATION_SCOPE
    assert _tables(db) == before
    own = rp.fixture()["inventor_inputs"]["H01_parts_after_readback"]
    sid = _created(_integrated(c, idea, own))
    names = {row["domain"]: row["display_name"] for row in _subsystems(db, sid)}
    assert names == {MECH: own["mech_part_name"], EE: own["elec_part_name"]}
    stored = _db_text(db)
    for part in rb.parts:
        assert part.text not in stored            # the AI wording is never stored


# ==========================================================================
# 3-4. a wrong AI reading and the inventor's correction
# ==========================================================================
def test_the_validator_alone_accepts_the_wrong_reading():
    idea, _reply, _src = rp.preserved("H08")
    wrong, source = rp.constructed("H08_incorrect")
    rb = rp.build(idea, wrong["reply"], source)
    assert rb is not None and rb.points_to_integrated     # nothing deterministic catches it


def test_the_inventor_correction_changes_the_meaning_and_the_next_action(client):
    c, _app, db = client
    _login(c, _app)
    idea, _reply, _src = rp.preserved("H08")
    wrong, source = rp.constructed("H08_incorrect")
    rb = rp.build(idea, wrong["reply"], source)
    page = rp.render(rb)
    assert 'data-pointer="integrated"' in page and "my phone" in page
    fix = rp.fixture()["inventor_inputs"]["H08_correction"]
    result = rp.resolve(rp.issue(rb), rb, idea, "correct",
                        exclude_index=fix["excluded_part_index"], remark=fix["remark"])
    fixed = result["readback"]
    assert result["remark_origin"] == rp.INVENTOR_ORIGIN and fixed.remark == fix["remark"]
    assert not fixed.points_to_integrated and fixed.effective != "SUGGEST_INTEGRATED"
    page = rp.render(fixed)
    assert 'data-excluded="1"' in page and 'data-pointer="none"' in page
    assert '<li data-part="1"' not in page and "The phone is mine" in page
    # the recommended action returns to the ordinary, unchanged mechanical start;
    # the integrated option stays offered on that page exactly as before
    confirm = _visible(_post(c, {"idea": idea}).get_data(as_text=True))
    assert "appears to belong to the Mechanical domain" in confirm
    sid = _created(_post(c, {"idea": idea, "domain_confirm": MECH}))
    assert _subsystems(db, sid) == []
    assert rp.resolve(result["token"], fixed, idea, "confirm")["action"] == "confirm"


# ==========================================================================
# 5. an unknown mechanism stays unknown
# ==========================================================================
def test_an_unknown_drive_source_stays_open_and_the_ai_question_is_not_asked(client):
    c, _app, db = client
    _login(c, _app)
    idea, reply, source = rp.preserved("H14")
    assert reply["clarification_questions"]      # the provider did ask spring-or-electric
    rb = rp.build(idea, reply, source)
    page = rp.render(rb)
    assert reply["clarification_questions"][0] not in page
    assert "data-open" in page and "You do not need to decide it to start" in page
    assert "data-obstacle" in page and 'data-pointer="none"' in page
    direct = _created(_post(c, {"idea": idea, "domain_confirm": MECH}))
    rp.resolve(rp.issue(rb), rb, idea, "confirm")
    assisted = _created(_post(c, {"idea": idea, "domain_confirm": MECH}))
    a = reconstruct_readonly_state(appmod._get_store(), direct).state
    b = reconstruct_readonly_state(appmod._get_store(), assisted).state
    assert [g.status for g in a.gaps] == [g.status for g in b.gaps]
    assert len(a.assertions) == len(b.assertions) and a.known_mechanism == b.known_mechanism
    for u in rb.unknowns:
        assert u not in _db_text(db)


def test_a_maybe_feature_stays_undecided():
    idea, reply, source = rp.preserved("H13")
    rb = rp.build(idea, reply, source)
    assert rb.unknowns and not rb.points_to_integrated
    assert all(p.kind == MECH for p in rb.parts)
    assert reply["clarification_questions"][0] not in rp.render(rb)


# ==========================================================================
# 6. repeated, stale, rejected, tampered and unavailable readbacks
# ==========================================================================
def test_a_token_works_once():
    idea, reply, source = rp.preserved("H01")
    rb = rp.build(idea, reply, source)
    token = rp.issue(rb)
    assert rp.resolve(token, rb, idea, "confirm") is not None
    assert rp.resolve(token, rb, idea, "confirm") is None


def test_a_changed_idea_makes_the_readback_stale():
    idea, reply, source = rp.preserved("H01")
    rb = rp.build(idea, reply, source)
    assert rp.resolve(rp.issue(rb), rb, idea + " It also has a handle.", "confirm") is None


def test_a_rejected_readback_is_gone_and_changes_nothing(client):
    c, _app, db = client
    idea, reply, source = rp.preserved("H01")
    rb = rp.build(idea, reply, source)
    token = rp.issue(rb)
    before = _tables(db)
    assert rp.resolve(token, rb, idea, "reject") == {"action": "reject", "shown": False,
                                                    "recorded": False}
    assert rp.resolve(token, rb, idea, "confirm") is None and _tables(db) == before


def test_a_tampered_or_swapped_reading_is_refused():
    idea, reply, source = rp.preserved("H01")
    rb = rp.build(idea, reply, source)
    token = rp.issue(rb)
    other_idea, other_reply, other_source = rp.preserved("H08")
    swapped = rp.build(other_idea, other_reply, other_source)
    assert rp.resolve(token, swapped, other_idea, "confirm") is None
    import dataclasses
    forged = dataclasses.replace(rb, points_to_integrated=False)
    assert rp.resolve(token, forged, idea, "confirm") is None
    assert rp.resolve(token, rb, idea, "confirm") is not None


@pytest.mark.parametrize("mutate", [
    lambda r: None,
    lambda r: {**r, "outcome": "ABSTAIN"},
    lambda r: {**r, "stated_parts": [{**r["stated_parts"][0], "source_quote": "a solar panel"}]},
    lambda r: {**r, "stated_parts": [{**r["stated_parts"][0], "candidate_concept": "robotics"}]},
])
def test_an_unavailable_reading_leaves_the_baseline_page_unchanged(client, mutate):
    c, _app, _db = client
    idea, reply, source = rp.preserved("H01")
    assert rp.build(idea, mutate(json.loads(json.dumps(reply))), source) is None
    page = _post(c, {"idea": idea}).get_data(as_text=True)
    assert "g1-readback" not in page and "did not clearly match one supported domain" in page


def test_an_invalid_correction_is_refused():
    idea, reply, source = rp.preserved("H01")
    rb = rp.build(idea, reply, source)
    assert rp.resolve(rp.issue(rb), rb, idea, "correct", exclude_index=7) is None
    assert rp.resolve(rp.issue(rb), rb, idea, "correct", exclude_index=None) is None


# ==========================================================================
# attribution and the absence of any engineering or progression effect
# ==========================================================================
def test_readback_operations_touch_no_store_or_session(client):
    """No AI wording can reach integrate_response: the seam has no write path
    and never imports it (test_the_seam_has_no_provider_route_or_production_caller).
    Here: building, rendering and resolving every readback writes nothing."""
    c, _app, db = client
    _login(c, _app)
    before, store = _tables(db), dict(appmod.SESSION_STORE)
    for case in ("H01", "H08", "H13", "H14", "H23"):
        idea, reply, source = rp.preserved(case)
        rb = rp.build(idea, reply, source)
        rp.render(rb), rp.render(rb, "ar")
        res = rp.resolve(rp.issue(rb), rb, idea, "confirm")
        assert res["recorded"] is False and res["creates_project"] is False
        assert res["reading_origin"] == (rp.READING_ORIGIN, rp.READING_STATUS)
        assert res["idea_origin"] == rp.INVENTOR_ORIGIN and res["idea_text"] == idea
    assert _tables(db) == before and dict(appmod.SESSION_STORE) == store


def test_inventor_and_ai_words_are_always_labelled_apart():
    idea, reply, source = rp.preserved("H01")
    page = rp.render(rp.build(idea, reply, source))
    assert 'data-ai-label' in page and "AI-proposed reading, not checked" in page
    assert '<blockquote data-inventor-words><bdi>%s</bdi>' % idea in page
    assert page.count("data-ai-text") == len(reply["stated_function"]) + len(reply["stated_parts"])
    assert "not an engineering check" in page and "not saved" in page
    assert page.count("<button") >= 3 and "disabled" in page


# ==========================================================================
# 7. Arabic presentation (no Arabic model qualification)
# ==========================================================================
def test_the_arabic_presentation():
    item, source = rp.constructed("AR01")
    rb = rp.build(item["idea_text"], item["reply"], source)
    page = rp.render(rb, "ar")
    assert 'lang="ar" dir="rtl"' in page and "كيف قرأ InventorAI فكرتك" in page
    assert item["idea_text"] in page and 'data-pointer="integrated"' in page
    assert "لا تحتاج إلى أن تقرّره لتبدأ" in page
    en = rp.render(rp.build(*rp.preserved("H01")[:2], rp.preserved("H01")[2]), "en")
    assert 'lang="en" dir="ltr"' in en
    for key in rp.TEXT["en"]:
        assert key in rp.TEXT["ar"] and rp.TEXT["ar"][key] != rp.TEXT["en"][key]


# ==========================================================================
# review corrections
# ==========================================================================
def test_an_invalid_correction_keeps_the_token():
    idea, reply, source = rp.preserved("H01")
    rb = rp.build(idea, reply, source)
    token = rp.issue(rb)
    assert rp.resolve(token, rb, idea, "correct", exclude_index=7) is None
    assert rp.resolve(token, rb, idea, "correct", exclude_index=0, remark="x" * 301) is None
    assert rp.resolve(token, rb, idea, "confirm") is not None


def test_a_later_correction_keeps_the_earlier_remark():
    idea, _reply, _src = rp.preserved("H08")
    wrong, source = rp.constructed("H08_incorrect")
    rb = rp.build(idea, wrong["reply"], source)
    first = rp.resolve(rp.issue(rb), rb, idea, "correct", exclude_index=1, remark="The phone is mine.")
    second = rp.resolve(first["token"], first["readback"], idea, "correct", exclude_index=0)
    assert second["readback"].remark == "The phone is mine."
    assert second["readback"].excluded == (0, 1)


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_the_pointer_quotes_the_real_start_page_option(lang):
    from web import ui_text
    idea, reply, source = rp.preserved("H01")
    page = rp.render(rp.build(idea, reply, source), lang)
    label = ui_text.text("UI_S15_OFFER_LABEL", lang).rstrip(".")
    assert __import__("html").escape(label) in page


def test_only_a_literal_quote_is_called_your_words():
    idea, reply, source = rp.preserved("H01")
    changed = json.loads(json.dumps(reply))
    changed["stated_parts"][0]["source_quote"] = changed["stated_parts"][0]["source_quote"].replace(" ", "  ", 1)
    rb = rp.build(idea, changed, source)
    assert rb is not None                         # the validator accepts it after normalisation
    page = rp.render(rb)
    assert "the AI&#x27;s quote of your words" in page and "(your words:" in page
