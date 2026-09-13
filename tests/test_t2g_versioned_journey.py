"""T2-G route-level journeys — the real integrated code, both versions.

`T2G-VERSIONED-IMPLEMENT-01`. Every fixture below is synthetic; no real-user
record is used. Assertions read FULL served-question identities and canonical
state, never a selected phrase.
"""
import html as _html
import os
import re
import sqlite3

import pytest

import web.app as appmod
from engine import account_credentials as acct
from engine.intent_serving import compute_intent_coverage
from engine.progression_loop import accept_gap_risk
from engine.idea_state import MECHANISM_COMPLETENESS as MC
from engine.session_reconstruction import (
    ENGINE_CONTRACT_VERSION_T2G1, RECONSTRUCTION_VERSION,
    reconstruct_readonly_state)
from tests.csrf_client import csrf_client

PW = "correct horse battery staple"
MECH_SEED = ("A folding mechanical wheelchair ramp with a spring latch. The "
             "inventor wants the ramp to stay reliably locked in the flat, "
             "load-bearing position and to fold away without tools")
EE_SEED = ("An electronic circuit uses a sensor and a switch to cut the power "
           "when the current gets too high.")

# ---- the exact fixtures the design return used, in full --------------------
F1_AFFIRM = ("The load path runs from the deck panel into the hinge line and "
             "the spring latch transfers force into the frame rail, so the "
             "ramp stays locked flat.")
F2_UNKNOWN = ("I do not know the load path, and I have not worked out how the "
              "hinge line transfers force into the frame rail at all.")
F3_NEGATIVE = ("The spring latch does not carry the load; the load path runs "
               "around it, from the deck straight into the hinge line and "
               "then the frame rail.")
F4_MIXED = ("I do not know the exact bolt size yet. The load path runs from "
            "the deck into the hinge line and then into the frame rail.")
G1_AFFIRM = ("مسار الحمل ينتقل من لوح السطح إلى خط المفصلة ثم ينقل المزلاج "
             "النابضي القوة إلى قضيب الإطار، لذلك يبقى المنحدر مقفلا في الوضع "
             "المسطح.")
G2_UNKNOWN = ("لا أعرف مسار الحمل ولم أحدد بعد كيف ينقل خط المفصلة القوة إلى "
              "قضيب الإطار على الإطلاق.")
G4_MIXED = ("لا أعرف مقاس البرغي بعد. مسار الحمل ينتقل من لوح السطح إلى خط "
            "المفصلة ثم إلى قضيب الإطار.")
H1_AFFIRM = ("The main parts are a vibration sensor on the pump housing, a "
             "small controller board, and a buzzer; each part does one job: "
             "the sensor reads the shaking, the board compares it to a "
             "threshold, and the buzzer alerts the operator.")
H2_UNKNOWN = ("I do not know what the main parts are yet, and I cannot say "
              "what each part does because I have not chosen any of the "
              "hardware.")
X1_BARE_NOUN = F2_UNKNOWN + " Spring latch."
X2_UNRELATED = F2_UNKNOWN + " My brother runs a workshop in the next town over."
K_FOLLOW_UP = ("The load path runs from the deck panel into the hinge line and "
               "the spring latch transfers force into the frame rail.")

Q2 = "PATHN:mechanical:MECHANISM_COMPLETENESS:Q2"
Q3 = "PATHN:mechanical:MECHANISM_COMPLETENESS:Q3"
EE2 = "PATHN:N-MC-2"
EE3 = "PATHN:N-MC-3"

UNKNOWN_NOTICE = "not known yet has been saved"
NOT_ADDRESSED_NOTICE = "not recognized as responding"
T2G_DISCLOSURE = "recognising some ways of saying you do not know"
LEGACY_DISCLOSURE = "does not read the meaning of your answers"


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("INVENTORAI_DB_PATH", str(tmp_path / "t2g.sqlite"))
    monkeypatch.setattr(appmod, "_STORE", None)
    appmod.SESSION_STORE.clear()
    appmod.app.config["TESTING"] = True
    with csrf_client(appmod.app) as c:
        yield c, appmod, str(tmp_path / "t2g.sqlite")


def _login(c, appmod, email="owner@example.com"):
    store = appmod._get_account_store()
    aid = acct.new_account_id()
    store.create_account(aid, acct.normalize_email(email), acct.hash_password(PW),
                         "2026-01-01T00:00:00.000000Z", status="active")
    store.mark_email_verified(aid, "2026-01-01T00:00:00.000000Z")
    assert c.post("/login", data={"email": email, "password": PW}).status_code == 302
    return aid


def _start(c, seed=MECH_SEED, domain="mechanical", extra=None):
    data = {"idea": seed, "domain_confirm": domain}
    if extra:
        data.update(extra)
    r = c.post("/start", data=data)
    assert r.status_code == 302
    return r.headers["Location"].rsplit("/", 1)[-1]


def _raw(c, sid, lang=None):
    if lang:
        assert c.post("/ui-language", data={"lang": lang}).status_code in (302, 303)
    body = c.get(f"/session/{sid}").get_data(as_text=True)
    if lang:
        c.post("/ui-language", data={"lang": "en"})
    return body


def _page(c, sid, lang=None):
    return _html.unescape(_raw(c, sid, lang))


def _answer(c, sid, text, extra=None):
    token = _html.unescape(re.search(
        r'name="answer_token" value="([^"]+)"', _raw(c, sid)).group(1))
    data = {"response": text, "answer_token": token, "action": "answered"}
    if extra:
        data.update(extra)
    return c.post(f"/session/{sid}", data=data)


def _state(appmod, sid):
    return appmod.SESSION_STORE[sid]["state"]


def _snapshot(appmod, sid):
    entry = appmod.SESSION_STORE[sid]
    state = entry["state"]
    qctx = appmod._resolve_question_context(state, entry.get("last_result"))
    gap = state.get_gap(qctx.gap_type) if qctx.gap_type else None
    return {
        "version": getattr(state, "engine_contract_version", None),
        "identity": qctx.identity,
        "gap": qctx.gap_type,
        "status": None if gap is None else gap.status,
        "known_mechanism": (None if state.known_mechanism is None
                            else state.known_mechanism.quality),
        "known_problem": (None if state.known_problem is None
                          else state.known_problem.quality),
        "coverage": sorted(compute_intent_coverage(state, qctx.gap_type) or []),
        "unknowns": len(getattr(state, "acknowledged_unknowns", [])),
        "records": len(state.assertions),
    }


def _stamp(db, sid):
    con = sqlite3.connect(db)
    try:
        row = con.execute(
            "SELECT engine_contract_version FROM projects WHERE project_id=?",
            (sid,)).fetchone()
    finally:
        con.close()
    return None if row is None else row[0]


def _set_stamp(db, sid, value):
    con = sqlite3.connect(db)
    try:
        con.execute("UPDATE projects SET engine_contract_version=? "
                    "WHERE project_id=?", (value, sid))
        con.commit()
    finally:
        con.close()


def _legacy_start(c, appmod, seed=MECH_SEED, domain="mechanical"):
    """A project created BEFORE T2-G: it records the earlier stamp, exactly as
    every existing project already does."""
    original = appmod.CURRENT_ENGINE_CONTRACT_VERSION
    appmod.CURRENT_ENGINE_CONTRACT_VERSION = RECONSTRUCTION_VERSION
    try:
        return _start(c, seed, domain)
    finally:
        appmod.CURRENT_ENGINE_CONTRACT_VERSION = original


# ==========================================================================
# 1. Version policy
# ==========================================================================
def test_a_new_project_records_and_runs_under_the_new_version(client):
    c, appmod, db = client
    _login(c, appmod)
    sid = _start(c)
    assert _stamp(db, sid) == ENGINE_CONTRACT_VERSION_T2G1
    assert _snapshot(appmod, sid)["version"] == ENGINE_CONTRACT_VERSION_T2G1


def test_the_version_is_selected_before_the_seed_is_interpreted(client):
    """The carrier the seed was read under IS the stamp that was persisted."""
    import inspect
    c, appmod, db = client
    source = inspect.getsource(appmod.start)
    assign = source.index("state.engine_contract_version = ")
    seed_run = source.index("initial_result = run_iteration(state, idea_text)")
    persist = source.index("_reconstruction_inputs(idea_text, state)")
    assert assign < seed_run < persist
    _login(c, appmod)
    sid = _start(c)
    assert _stamp(db, sid) == _snapshot(appmod, sid)["version"]


def test_a_legacy_project_keeps_its_own_recorded_version(client):
    c, appmod, db = client
    _login(c, appmod)
    sid = _legacy_start(c, appmod)
    assert _stamp(db, sid) == RECONSTRUCTION_VERSION
    _answer(c, sid, F2_UNKNOWN)
    assert _snapshot(appmod, sid)["version"] == RECONSTRUCTION_VERSION
    assert _stamp(db, sid) == RECONSTRUCTION_VERSION      # never rewritten


@pytest.mark.parametrize("forged", [RECONSTRUCTION_VERSION, "anything", ""])
def test_the_version_cannot_be_switched_by_browser_input(client, forged):
    c, appmod, db = client
    _login(c, appmod)
    sid = _start(c, extra={"engine_contract_version": forged})
    assert _stamp(db, sid) == ENGINE_CONTRACT_VERSION_T2G1
    _answer(c, sid, F2_UNKNOWN, extra={"engine_contract_version": forged})
    assert _stamp(db, sid) == ENGINE_CONTRACT_VERSION_T2G1
    assert _snapshot(appmod, sid)["version"] == ENGINE_CONTRACT_VERSION_T2G1


def test_ordinary_resume_does_not_switch_the_version(client):
    c, appmod, db = client
    _login(c, appmod)
    sid = _legacy_start(c, appmod)
    _answer(c, sid, F1_AFFIRM)
    appmod.SESSION_STORE.clear()
    _raw(c, sid)
    assert c.post(f"/session/{sid}/resume",
                  data={"engine_contract_version": ENGINE_CONTRACT_VERSION_T2G1}
                  ).status_code == 302
    assert _snapshot(appmod, sid)["version"] == RECONSTRUCTION_VERSION
    assert _stamp(db, sid) == RECONSTRUCTION_VERSION


@pytest.mark.parametrize("value,status", [
    (None, "LEVEL_0_NO_RECONSTRUCTION_METADATA"),
    ("p4-2-level1-recon-v9-bogus", "LEVEL_0_VERSION_MISMATCH"),
])
def test_missing_or_unsupported_metadata_stays_fail_closed(client, value, status):
    c, appmod, db = client
    _login(c, appmod)
    sid = _start(c)
    _answer(c, sid, F1_AFFIRM)
    _set_stamp(db, sid, value)
    appmod._STORE = None
    appmod.SESSION_STORE.clear()
    review = reconstruct_readonly_state(appmod._get_store(), sid)
    assert review.review.level == 0
    assert review.review.status == status
    assert review.state is None


# ==========================================================================
# 2. The new rule — canonical state AND served identity
# ==========================================================================
@pytest.mark.parametrize("answer,identity", [
    (F1_AFFIRM, Q3), (F3_NEGATIVE, Q3), (F4_MIXED, Q3), (G1_AFFIRM, Q3),
    (G4_MIXED, Q3),
])
def test_a_supported_explanation_is_unaffected(client, answer, identity):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _start(c)
    _answer(c, sid, answer)
    got = _snapshot(appmod, sid)
    assert got["identity"] == identity
    assert got["status"] == "PARTIAL"
    assert got["known_mechanism"] == "REASONED"
    assert got["coverage"] == ["mechanical:MECHANISM_COMPLETENESS:Q2"]
    assert NOT_ADDRESSED_NOTICE not in _page(c, sid)


@pytest.mark.parametrize("answer", [F2_UNKNOWN, G2_UNKNOWN, X1_BARE_NOUN,
                                    X2_UNRELATED])
def test_a_recognised_unknown_supplies_no_mechanism_and_re_asks(client, answer):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _start(c)
    _answer(c, sid, answer)
    got = _snapshot(appmod, sid)
    assert got["identity"] == Q2                       # the question stands
    assert got["status"] == "OPEN"                     # no progress
    assert got["known_mechanism"] is None
    assert got["known_problem"] is None
    assert got["coverage"] == []
    assert got["unknowns"] == 1                        # captured exactly once
    assert got["records"] == 1                         # the answer is saved


def test_the_electronics_journey_behaves_identically(client):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _start(c, EE_SEED, "electronics_electrical")
    _answer(c, sid, H2_UNKNOWN)
    got = _snapshot(appmod, sid)
    assert got["identity"] == EE2 and got["status"] == "OPEN"
    assert got["known_mechanism"] is None and got["coverage"] == []
    appmod.SESSION_STORE.clear()
    sid2 = _start(c, EE_SEED, "electronics_electrical")
    _answer(c, sid2, H1_AFFIRM)
    got2 = _snapshot(appmod, sid2)
    assert got2["identity"] == EE3 and got2["known_mechanism"] == "REASONED"


def test_a_legacy_project_reproduces_the_pre_t2g_reading(client):
    """The SAME unknown answer, on a legacy project: baseline behaviour."""
    c, appmod, _db = client
    _login(c, appmod)
    sid = _legacy_start(c, appmod)
    _answer(c, sid, F2_UNKNOWN)
    got = _snapshot(appmod, sid)
    assert got["identity"] == Q3                       # pre-T2-G serving
    assert got["status"] == "PARTIAL"
    assert got["known_mechanism"] == "REASONED"
    assert got["coverage"] == ["mechanical:MECHANISM_COMPLETENESS:Q2"]


def test_the_veto_does_not_reach_other_gaps(client):
    """An explicit unknown against a LATER gap keeps its existing behaviour."""
    c, appmod, _db = client
    _login(c, appmod)
    sid = _start(c)
    for text in (F1_AFFIRM, K_FOLLOW_UP):
        _answer(c, sid, text)
    assert _snapshot(appmod, sid)["gap"] != MC          # moved past mechanism
    before = _snapshot(appmod, sid)
    _answer(c, sid, "I do not know the physical principle it relies on, and I "
                    "have not worked out the force constraint at all yet.")
    after = _snapshot(appmod, sid)
    assert after["gap"] == before["gap"]
    assert after["status"] == "PARTIAL"                # unchanged pre-T2-G path


# ==========================================================================
# 3. Progress, correction, replay, resume
# ==========================================================================
def test_an_unknown_then_an_explanation_does_not_close_the_gap_early(client):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _start(c)
    _answer(c, sid, F2_UNKNOWN)
    _answer(c, sid, K_FOLLOW_UP)
    got = _snapshot(appmod, sid)
    assert got["gap"] == MC and got["status"] == "PARTIAL"   # not CLOSED
    assert got["identity"] == Q3
    assert got["known_mechanism"] == "REASONED"              # knowledge arrived
    assert got["unknowns"] == 1                              # still exactly once
    assert got["records"] == 2                               # both saved


def test_prior_knowledge_is_never_erased_by_a_later_unknown(client):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _start(c)
    _answer(c, sid, F1_AFFIRM)
    before = _snapshot(appmod, sid)
    _answer(c, sid, F2_UNKNOWN)
    after = _snapshot(appmod, sid)
    assert after["known_mechanism"] == before["known_mechanism"] == "REASONED"
    assert after["status"] == before["status"] == "PARTIAL"
    assert after["coverage"] == before["coverage"]


def test_live_replay_and_resume_agree_on_the_new_version(client):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _start(c)
    _answer(c, sid, F2_UNKNOWN)
    live = _snapshot(appmod, sid)
    appmod.SESSION_STORE.clear()
    session = reconstruct_readonly_state(appmod._get_store(), sid)
    assert session.review.level == 1
    assert getattr(session.state, "engine_contract_version", None) == \
        ENGINE_CONTRACT_VERSION_T2G1
    replayed = appmod._resolve_question_context(session.state, None)
    assert replayed.identity == live["identity"]
    assert session.state.known_mechanism is None
    _raw(c, sid)
    assert c.post(f"/session/{sid}/resume", data={}).status_code == 302
    assert _snapshot(appmod, sid) == live


def test_a_legacy_history_that_already_advanced_replays_and_resumes_unchanged(client):
    c, appmod, db = client
    _login(c, appmod)
    sid = _legacy_start(c, appmod)
    for text in (F2_UNKNOWN, K_FOLLOW_UP,
                 "Each component contributes: the deck carries the person, the "
                 "hinge line takes the moment, and the frame rail carries it "
                 "into the chassis."):
        _answer(c, sid, text)
    live = _snapshot(appmod, sid)
    assert live["gap"] != MC                       # it advanced past mechanism
    appmod.SESSION_STORE.clear()
    session = reconstruct_readonly_state(appmod._get_store(), sid)
    assert getattr(session.state, "engine_contract_version", None) == \
        RECONSTRUCTION_VERSION
    assert appmod._resolve_question_context(session.state, None).identity == \
        live["identity"]
    _raw(c, sid)
    assert c.post(f"/session/{sid}/resume", data={}).status_code == 302
    assert _snapshot(appmod, sid) == live
    assert _stamp(db, sid) == RECONSTRUCTION_VERSION


def _correct(c, sid, record_id, response):
    token = _html.unescape(re.search(
        r'name="answer_token" value="([^"]+)"', _raw(c, sid)).group(1))
    return c.post(f"/session/{sid}/correct", data={
        "supersedes_record_id": record_id, "response": response,
        "answer_token": token})


def _active_answers(appmod, sid):
    contract = appmod._get_store().load_contract(sid)
    return [r for r in contract.assertions
            if getattr(r, "superseded_by", None) is None
            and r.disposition == "answered"]


def test_a_real_correction_of_an_unknown_recomputes_under_the_new_version(client):
    """The GENUINE R4 supersession path, not a follow-up answer: correcting the
    unknown into an explanation must recompute eligibility from scratch."""
    c, appmod, _db = client
    _login(c, appmod)
    sid = _start(c)
    _answer(c, sid, F2_UNKNOWN)
    assert _snapshot(appmod, sid)["known_mechanism"] is None
    record = _active_answers(appmod, sid)[0]
    assert _correct(c, sid, record.record_id, K_FOLLOW_UP).status_code in (302, 303)
    got = _snapshot(appmod, sid)
    assert got["known_mechanism"] == "REASONED"      # the correction supplies it
    assert got["identity"] == Q3
    appmod.SESSION_STORE.clear()
    session = reconstruct_readonly_state(appmod._get_store(), sid)
    assert session.review.withdrawn_source_records == 1
    assert session.state.known_mechanism is not None
    assert appmod._resolve_question_context(session.state, None).identity == Q3


def test_a_real_correction_into_an_unknown_withdraws_the_knowledge(client):
    """The converse: correcting an explanation INTO an explicit unknown must
    recompute to no mechanism knowledge, through full replay — never by
    patching the old state in place."""
    c, appmod, _db = client
    _login(c, appmod)
    sid = _start(c)
    _answer(c, sid, F1_AFFIRM)
    assert _snapshot(appmod, sid)["known_mechanism"] == "REASONED"
    record = _active_answers(appmod, sid)[0]
    assert _correct(c, sid, record.record_id, F2_UNKNOWN).status_code in (302, 303)
    got = _snapshot(appmod, sid)
    assert got["known_mechanism"] is None
    assert got["status"] == "OPEN"
    assert got["identity"] == Q2
    assert got["coverage"] == []
    appmod.SESSION_STORE.clear()
    session = reconstruct_readonly_state(appmod._get_store(), sid)
    assert session.state.known_mechanism is None
    assert session.review.withdrawn_source_records == 1


def test_the_same_correction_on_a_legacy_project_keeps_the_baseline(client):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _legacy_start(c, appmod)
    _answer(c, sid, F1_AFFIRM)
    record = _active_answers(appmod, sid)[0]
    assert _correct(c, sid, record.record_id, F2_UNKNOWN).status_code in (302, 303)
    got = _snapshot(appmod, sid)
    assert got["known_mechanism"] == "REASONED"      # pre-T2-G reading
    assert got["status"] == "PARTIAL"
    assert got["identity"] == Q3


# ==========================================================================
# 4. Truthful, version-scoped copy
# ==========================================================================
def test_the_new_disclosure_shows_only_where_the_rule_applies(client):
    c, appmod, _db = client
    _login(c, appmod)
    new = _start(c)
    legacy = _legacy_start(c, appmod)
    new_page, legacy_page = _page(c, new), _page(c, legacy)
    assert T2G_DISCLOSURE in new_page and LEGACY_DISCLOSURE not in new_page
    assert LEGACY_DISCLOSURE in legacy_page and T2G_DISCLOSURE not in legacy_page
    assert appmod.ui_text.text("UI_T2G_QUESTION_SET", "ar") in _page(c, new, "ar")
    assert appmod.ui_text.text("UI_T1D_QUESTION_SET", "ar") in _page(c, legacy, "ar")


def test_the_new_disclosure_is_truthful_in_both_languages(client):
    _c, appmod, _db = client
    copy = {"en": appmod.ui_text.text("UI_T2G_QUESTION_SET", "en"),
            "ar": appmod.ui_text.text("UI_T2G_QUESTION_SET", "ar")}
    lowered = copy["en"].lower()
    assert "fixed" in lowered and "set" in lowered
    assert "no new questions are generated" in lowered
    assert "engineering-correct is not checked" in lowered
    assert "covers only certain phrasings" in lowered
    for overclaim in ("understands", "understanding", "any language",
                      "always", "verified", "validated", "never adapts"):
        assert overclaim not in lowered
    assert copy["ar"] and copy["ar"] != copy["en"]


def test_the_saved_unknown_gets_its_own_bilingual_notice(client):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _start(c)
    _answer(c, sid, F2_UNKNOWN)
    english = _page(c, sid)
    assert UNKNOWN_NOTICE in english
    assert NOT_ADDRESSED_NOTICE not in english
    for overclaim in ("lost", "irrelevant", "verified", "validated", "incorrect"):
        assert overclaim not in english.lower().split("saved with your project")[0][-400:]
    # the Arabic counterpart, on its own project so the notice is the fresh one
    sid_ar = _start(c)
    _answer(c, sid_ar, G2_UNKNOWN)
    arabic = _page(c, sid_ar, "ar")
    assert "تم حفظ قولك إن هذا غير معروف بعد مع مشروعك" in arabic
    assert UNKNOWN_NOTICE not in arabic


def test_a_legacy_project_still_gets_the_legacy_reason(client):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _legacy_start(c, appmod)
    _answer(c, sid, F2_UNKNOWN)
    assert UNKNOWN_NOTICE not in _page(c, sid)


# ==========================================================================
# 5. Non-interference
# ==========================================================================
def test_mechanism_completeness_still_cannot_be_risk_accepted(client):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _start(c)
    _answer(c, sid, F2_UNKNOWN)
    with pytest.raises(ValueError):
        accept_gap_risk(_state(appmod, sid), MC)
    assert _snapshot(appmod, sid)["status"] == "OPEN"
    assert f"/session/{sid}/accept-risk" not in _raw(c, sid)


def test_t2d_feedback_binds_to_the_question_actually_displayed(client):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _start(c)
    _answer(c, sid, F2_UNKNOWN)
    entry = appmod.SESSION_STORE[sid]
    qctx = appmod._resolve_question_context(entry["state"], entry.get("last_result"))
    context = appmod._feedback_context(sid, entry["state"], qctx)
    assert qctx.identity == Q2
    assert context is not None and context["identity"] == Q2
    forms = [f for f in re.findall(r'action="([^"]+)"', _raw(c, sid))
             if "question-feedback" in f]
    assert len(forms) == 1


def test_the_accepted_cold_suppression_boundary_is_intact(client):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _start(c)
    _answer(c, sid, F2_UNKNOWN)
    appmod.SESSION_STORE.clear()
    cold = _page(c, sid)
    assert 'id="reconstructed-review"' in cold
    assert re.search(r'class="t2d-cold-selected"', cold) is None
    assert "question-feedback" not in cold
    assert getattr(appmod.SESSION_STORE[sid]["state"], "domain", None) is None


def test_the_shared_selector_and_relevance_owners_are_unchanged(client):
    import inspect
    _c, appmod, _db = client
    from engine import intent_serving as isv
    from engine import progression_loop as pl
    module = inspect.getsource(appmod)
    assert module.count("_canonical_q = get_question(") == 1
    integrate = inspect.getsource(pl.integrate_response)
    assert "relevant = addresses_gap(response, gap_type)" in integrate
    assert "eligible = relevant and not unknown_only" in integrate
    # `relevant` itself is never reassigned by the veto
    assert "relevant = " not in integrate.split("unknown_only = False")[1]
    supplement = inspect.getsource(isv.supplemental_relevance)
    assert "_matches_intent(response, canonical.question_id)" in supplement
    assert "answer_stance" not in supplement
    # the public alias delegates; it does not reimplement the predicate
    alias = inspect.getsource(isv.matches_committed_intent)
    assert "return _matches_intent(text, question_id)" in alias
    assert "_INTENT_MARKERS" not in alias


def test_a_feedback_or_stance_failure_never_breaks_the_journey(client, monkeypatch):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _start(c)
    from engine import answer_stance
    monkeypatch.setattr(answer_stance, "explicit_unknown_without_mechanism",
                        lambda *a, **k: (_ for _ in ()).throw(RuntimeError("boom")))
    _answer(c, sid, F2_UNKNOWN)
    got = _snapshot(appmod, sid)
    assert got["records"] == 1
    assert got["status"] == "PARTIAL"          # fail-closed to today's reading


# ==========================================================================
# 6. F-1 / F-2 carrier repair through the real routes
#    PR642-T2G-CARRIER-REPAIR-01
# ==========================================================================
MARKER_ONLY_EN = "Force path force path force path."
MARKER_ONLY_EN2 = "Hinge line hinge line hinge line."
MARKER_ONLY_AR = "مسار القوة مسار القوة مسار القوة."
MARKER_ONLY_EE = "Main parts main parts main parts."
REAL_AFTER_MARKERS_EN = ("Force path force path: the deck panel presses down "
                         "into the hinge line and the frame rail carries it "
                         "into the chassis.")
REAL_AFTER_MARKERS_AR = ("مسار القوة ينتقل من لوح السطح إلى خط المفصلة ثم إلى "
                         "قضيب الإطار ويحمله الهيكل.")


@pytest.mark.parametrize("tail", [MARKER_ONLY_EN, MARKER_ONLY_EN2])
def test_repeated_markers_do_not_buy_progress_through_the_route(client, tail):
    """F-2 at route level: the unknown is recognised, the tail is only markers,
    so nothing may advance. Full identity, state and notice asserted together."""
    c, appmod, _db = client
    _login(c, appmod)
    sid = _start(c)
    _answer(c, sid, F2_UNKNOWN + " " + tail)
    got = _snapshot(appmod, sid)
    assert got["identity"] == Q2
    assert got["status"] == "OPEN"
    assert got["known_mechanism"] is None
    assert got["known_problem"] is None
    assert got["coverage"] == []
    assert got["unknowns"] == 1
    assert got["records"] == 1
    assert UNKNOWN_NOTICE in _page(c, sid)


def test_repeated_arabic_markers_do_not_buy_progress(client):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _start(c)
    _answer(c, sid, G2_UNKNOWN + " " + MARKER_ONLY_AR)
    got = _snapshot(appmod, sid)
    assert got["identity"] == Q2 and got["status"] == "OPEN"
    assert got["known_mechanism"] is None and got["coverage"] == []
    assert "تم حفظ قولك إن هذا غير معروف بعد مع مشروعك" in _page(c, sid, "ar")


def test_repeated_markers_do_not_buy_progress_in_electronics(client):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _start(c, EE_SEED, "electronics_electrical")
    _answer(c, sid, H2_UNKNOWN + " " + MARKER_ONLY_EE)
    got = _snapshot(appmod, sid)
    assert got["identity"] == EE2 and got["status"] == "OPEN"
    assert got["known_mechanism"] is None and got["coverage"] == []
    assert UNKNOWN_NOTICE in _page(c, sid)


@pytest.mark.parametrize("tail,lang", [(REAL_AFTER_MARKERS_EN, "en"),
                                       (REAL_AFTER_MARKERS_AR, "ar")])
def test_a_genuine_explanation_after_markers_still_progresses(client, tail, lang):
    """The positive control: repeated markers followed by a real explanation
    must still be recognised, in both languages."""
    c, appmod, _db = client
    _login(c, appmod)
    sid = _start(c)
    unknown = F2_UNKNOWN if lang == "en" else G2_UNKNOWN
    _answer(c, sid, unknown + " " + tail)
    got = _snapshot(appmod, sid)
    assert got["identity"] == Q3
    assert got["status"] == "PARTIAL"
    assert got["known_mechanism"] == "REASONED"
    assert got["coverage"] == ["mechanical:MECHANISM_COMPLETENESS:Q2"]
    assert UNKNOWN_NOTICE not in _page(c, sid)


def test_both_coverage_consumers_agree_after_the_repair(client):
    """`compute_intent_coverage` and the serving law read the SAME helper."""
    from engine.intent_serving import compute_intent_coverage, w2c_served_question
    c, appmod, _db = client
    _login(c, appmod)
    sid = _start(c)
    _answer(c, sid, F2_UNKNOWN + " " + MARKER_ONLY_EN)
    state = _state(appmod, sid)
    assert compute_intent_coverage(state, MC) == frozenset()
    assert w2c_served_question(state, MC) is None      # canonical serving stands
    assert _snapshot(appmod, sid)["identity"] == Q2
    # and the positive control moves BOTH consumers together
    sid2 = _start(c)
    _answer(c, sid2, F2_UNKNOWN + " " + REAL_AFTER_MARKERS_EN)
    state2 = _state(appmod, sid2)
    assert compute_intent_coverage(state2, MC) == frozenset(
        {"mechanical:MECHANISM_COMPLETENESS:Q2"})
    assert _snapshot(appmod, sid2)["identity"] == Q3


def test_the_marker_only_record_replays_and_resumes_identically(client):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _start(c)
    _answer(c, sid, F2_UNKNOWN + " " + MARKER_ONLY_EN)
    live = _snapshot(appmod, sid)
    appmod.SESSION_STORE.clear()
    session = reconstruct_readonly_state(appmod._get_store(), sid)
    assert session.review.level == 1
    assert session.state.known_mechanism is None
    assert appmod._resolve_question_context(session.state, None).identity == Q2
    _raw(c, sid)
    assert c.post(f"/session/{sid}/resume", data={}).status_code == 302
    assert _snapshot(appmod, sid) == live


def test_a_legacy_project_is_unchanged_by_the_carrier_repair(client):
    """The same marker-only answer on a legacy project keeps the pre-T2-G
    reading — the repair is inside the versioned rule, not outside it."""
    c, appmod, _db = client
    _login(c, appmod)
    sid = _legacy_start(c, appmod)
    _answer(c, sid, F2_UNKNOWN + " " + MARKER_ONLY_EN)
    got = _snapshot(appmod, sid)
    assert got["version"] == RECONSTRUCTION_VERSION
    assert got["identity"] == Q3
    assert got["status"] == "PARTIAL"
    assert got["known_mechanism"] == "REASONED"
    assert UNKNOWN_NOTICE not in _page(c, sid)


def test_an_answer_at_the_accepted_limit_renders_without_a_cost_collapse(client):
    """F-1 at route level. The accepted MAX_FREE_TEXT_CHARS limit is NOT
    reduced; repeated live and resumed renders simply stay fast. The bound is
    deliberately loose — it excludes the minutes-long path, it is not a
    performance target."""
    import time
    from web.app import MAX_FREE_TEXT_CHARS
    c, appmod, _db = client
    _login(c, appmod)
    sid = _start(c)
    body = (("alpha " * 3300) + "load path runs into the hinge line.")[:MAX_FREE_TEXT_CHARS - 1]
    assert len(body) < MAX_FREE_TEXT_CHARS
    _answer(c, sid, body)
    for _ in range(3):
        start = time.perf_counter()
        _raw(c, sid)
        assert time.perf_counter() - start < 5.0
    appmod.SESSION_STORE.clear()
    _raw(c, sid)
    assert c.post(f"/session/{sid}/resume", data={}).status_code == 302
    for _ in range(2):
        start = time.perf_counter()
        _raw(c, sid)
        assert time.perf_counter() - start < 5.0


# ==========================================================================
# 7. F-3 Unicode span coordinates through the real routes
#    PR642-T2G-UNICODE-SPAN-REPAIR-02
# ==========================================================================
DOTTED_I = "İ"
UNICODE_MARKER_ONLY_EN = DOTTED_I + " Force path force path force path."
UNICODE_MARKER_ONLY_EN3 = (DOTTED_I * 3) + " Hinge line hinge line hinge line."
UNICODE_BETWEEN_EN = ("Force path " + DOTTED_I + " force path " + DOTTED_I
                      + " force path.")
UNICODE_MARKER_ONLY_AR = DOTTED_I + " مسار القوة مسار القوة مسار القوة."
UNICODE_MIXED_CONTROL = "مسار القوة " + DOTTED_I + " force path force path."
UNICODE_MARKER_ONLY_EE = (DOTTED_I * 2) + " Main parts main parts main parts."
UNICODE_REAL_EXPLANATION = (
    DOTTED_I + " Force path force path: the deck panel presses down into the "
    "hinge line and the frame rail carries it into the chassis.")


@pytest.mark.parametrize("tail", [UNICODE_MARKER_ONLY_EN, UNICODE_MARKER_ONLY_EN3,
                                  UNICODE_BETWEEN_EN, UNICODE_MIXED_CONTROL])
def test_a_unicode_expansion_does_not_buy_progress(client, tail):
    """F-3 at route level: U+0130 before or between English markers must not
    reopen the marker-only bypass. Knowledge, gap status, notice and the full
    served identity asserted together."""
    c, appmod, _db = client
    _login(c, appmod)
    sid = _start(c)
    _answer(c, sid, F2_UNKNOWN + " " + tail)
    got = _snapshot(appmod, sid)
    assert got["identity"] == Q2
    assert got["status"] == "OPEN"
    assert got["known_mechanism"] is None
    assert got["known_problem"] is None
    assert got["coverage"] == []
    assert got["unknowns"] == 1
    assert got["records"] == 1
    assert UNKNOWN_NOTICE in _page(c, sid)


def test_a_unicode_expansion_does_not_buy_progress_in_arabic(client):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _start(c)
    _answer(c, sid, G2_UNKNOWN + " " + UNICODE_MARKER_ONLY_AR)
    got = _snapshot(appmod, sid)
    assert got["identity"] == Q2 and got["status"] == "OPEN"
    assert got["known_mechanism"] is None and got["coverage"] == []
    assert "تم حفظ قولك إن هذا غير معروف بعد مع مشروعك" in _page(c, sid, "ar")


def test_a_unicode_expansion_does_not_buy_progress_in_electronics(client):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _start(c, EE_SEED, "electronics_electrical")
    _answer(c, sid, H2_UNKNOWN + " " + UNICODE_MARKER_ONLY_EE)
    got = _snapshot(appmod, sid)
    assert got["identity"] == EE2 and got["status"] == "OPEN"
    assert got["known_mechanism"] is None and got["coverage"] == []
    assert UNKNOWN_NOTICE in _page(c, sid)


def test_a_genuine_explanation_after_a_unicode_expansion_still_progresses(client):
    """The positive control survives the repair."""
    c, appmod, _db = client
    _login(c, appmod)
    sid = _start(c)
    _answer(c, sid, F2_UNKNOWN + " " + UNICODE_REAL_EXPLANATION)
    got = _snapshot(appmod, sid)
    assert got["identity"] == Q3
    assert got["status"] == "PARTIAL"
    assert got["known_mechanism"] == "REASONED"
    assert got["coverage"] == ["mechanical:MECHANISM_COMPLETENESS:Q2"]
    assert UNKNOWN_NOTICE not in _page(c, sid)


def test_the_unicode_record_replays_and_resumes_identically(client):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _start(c)
    _answer(c, sid, F2_UNKNOWN + " " + UNICODE_MARKER_ONLY_EN)
    live = _snapshot(appmod, sid)
    appmod.SESSION_STORE.clear()
    session = reconstruct_readonly_state(appmod._get_store(), sid)
    assert session.review.level == 1
    assert session.state.known_mechanism is None
    assert appmod._resolve_question_context(session.state, None).identity == Q2
    _raw(c, sid)
    assert c.post(f"/session/{sid}/resume", data={}).status_code == 302
    assert _snapshot(appmod, sid) == live


def test_the_stored_answer_keeps_its_unicode_verbatim(client):
    """The repair maps coordinates; it never rewrites, filters or re-cases the
    inventor's own text."""
    c, appmod, _db = client
    _login(c, appmod)
    sid = _start(c)
    submitted = F2_UNKNOWN + " " + UNICODE_MARKER_ONLY_EN
    _answer(c, sid, submitted)
    contract = appmod._get_store().load_contract(sid)
    stored = [r for r in contract.assertions if r.disposition == "answered"]
    assert len(stored) == 1
    assert stored[0].content == submitted
    assert DOTTED_I in stored[0].content


def test_a_legacy_project_is_unchanged_by_the_unicode_repair(client):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _legacy_start(c, appmod)
    _answer(c, sid, F2_UNKNOWN + " " + UNICODE_MARKER_ONLY_EN)
    got = _snapshot(appmod, sid)
    assert got["version"] == RECONSTRUCTION_VERSION
    assert got["identity"] == Q3
    assert got["status"] == "PARTIAL"
    assert got["known_mechanism"] == "REASONED"
    assert UNKNOWN_NOTICE not in _page(c, sid)
