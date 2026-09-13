"""T2-G-2 — concise and mixed mechanism explanations, version-gated.

`T2G-CONCISE-MIXED-IMPLEMENT-02`. Synthetic fixtures only; no real-user record.
Route assertions always read the FULL served identity, canonical knowledge, gap
state, coverage and unknown tracking together — a carrier Boolean on its own
proves none of them.
"""
import html as _html
import re
import sqlite3

import pytest

import web.app as appmod
from engine import account_credentials as acct
from engine import answer_stance as st
from engine.idea_state import MECHANISM_COMPLETENESS as MC
from engine.intent_serving import compute_intent_coverage
from engine.intent_serving import matches_committed_intent as MATCH
from engine.session_reconstruction import (
    ENGINE_CONTRACT_VERSION_T2G1, ENGINE_CONTRACT_VERSION_T2G2,
    RECONSTRUCTION_VERSION, SUPPORTED_ENGINE_CONTRACT_VERSIONS,
    reconstruct_readonly_state)
from tests.csrf_client import csrf_client

PW = "correct horse battery staple"
MECH_SEED = ("A folding mechanical wheelchair ramp with a spring latch. The "
             "inventor wants the ramp to stay reliably locked in the flat, "
             "load-bearing position and to fold away without tools")
EE_SEED = ("An electronic circuit uses a sensor and a switch to cut the power "
           "when the current gets too high.")

Q2 = "PATHN:mechanical:MECHANISM_COMPLETENESS:Q2"
Q3 = "PATHN:mechanical:MECHANISM_COMPLETENESS:Q3"
Q2_ID = "mechanical:MECHANISM_COMPLETENESS:Q2"
Q4_ID = "mechanical:MECHANISM_COMPLETENESS:Q4"
EE3 = "PATHN:N-MC-3"
COV_Q2 = ["mechanical:MECHANISM_COMPLETENESS:Q2"]
UNKNOWN_NOTICE = "not known yet has been saved"

# ---- fixtures, in full -----------------------------------------------------
CONCISE_EN = "Deck transfers force into rail."
CONCISE_EN2 = "The hinge line carries the load path."
CONCISE_AR = "السطح ينقل القوة إلى الإطار."
CONCISE_EE = "The sensor and buzzer are the main parts."
MIXED_EN = ("I do not know the bolt size but the load path runs from the deck "
            "into the hinge line.")
MIXED_AR = ("لا أعرف مقاس البرغي لكن مسار الحمل ينتقل من لوح السطح إلى خط "
            "المفصلة.")
UNKNOWN_EN = ("I do not know the load path, and I have not worked out how the "
              "hinge line transfers force at all.")
UNKNOWN_EN_YET = ("I do not know yet how the load path transfers force into "
                  "the frame rail.")
UNKNOWN_AR = ("لا أعرف مسار الحمل ولم أحدد بعد كيف ينقل خط المفصلة القوة على "
              "الإطلاق.")
UNKNOWN_LEAD = "I do not know the load path at all here. "
NEGATION_EN = ("The spring latch does not carry the load; the load path runs "
               "around it into the hinge line.")
AFFIRMATIVE_EN = ("The load path runs from the deck panel into the hinge line "
                  "and the spring latch transfers force into the frame rail.")
HYPOTHETICAL_EN = ("I do not know the load path but it would probably transfer "
                   "force into the rail.")
DOTTED_I = "İ"


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("INVENTORAI_DB_PATH", str(tmp_path / "t2g2.sqlite"))
    monkeypatch.setattr(appmod, "_STORE", None)
    appmod.SESSION_STORE.clear()
    appmod.app.config["TESTING"] = True
    with csrf_client(appmod.app) as c:
        yield c, appmod, str(tmp_path / "t2g2.sqlite")


def _login(c, appmod, email="owner@example.com"):
    store = appmod._get_account_store()
    aid = acct.new_account_id()
    store.create_account(aid, acct.normalize_email(email), acct.hash_password(PW),
                         "2026-01-01T00:00:00.000000Z", status="active")
    store.mark_email_verified(aid, "2026-01-01T00:00:00.000000Z")
    assert c.post("/login", data={"email": email, "password": PW}).status_code == 302


def _start(c, seed=MECH_SEED, domain="mechanical", extra=None):
    data = {"idea": seed, "domain_confirm": domain}
    if extra:
        data.update(extra)
    r = c.post("/start", data=data)
    assert r.status_code == 302
    return r.headers["Location"].rsplit("/", 1)[-1]


def _stamped_start(c, appmod, version, seed=MECH_SEED, domain="mechanical"):
    """Genuinely CREATED under `version` — no history is ever rewritten."""
    original = appmod.CURRENT_ENGINE_CONTRACT_VERSION
    appmod.CURRENT_ENGINE_CONTRACT_VERSION = version
    try:
        return _start(c, seed, domain)
    finally:
        appmod.CURRENT_ENGINE_CONTRACT_VERSION = original


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
        "coverage": sorted(compute_intent_coverage(state, qctx.gap_type) or []),
        "unknowns": len(getattr(state, "acknowledged_unknowns", [])),
        "records": len(state.assertions),
    }


def _stamp(db, sid):
    con = sqlite3.connect(db)
    try:
        row = con.execute("SELECT engine_contract_version FROM projects "
                          "WHERE project_id=?", (sid,)).fetchone()
    finally:
        con.close()
    return None if row is None else row[0]


class _State:
    def __init__(self, version=ENGINE_CONTRACT_VERSION_T2G2, domain="mechanical"):
        if version is not None:
            self.engine_contract_version = version
        self.domain = domain
        self.iteration = 0


# ==========================================================================
# 1. The declared vocabularies, enumerated
# ==========================================================================
def test_the_contrast_boundaries_are_exactly_the_four_registered_tokens():
    assert st._T2G2_CONTRAST_EN == ("but", "however")
    assert st._T2G2_CONTRAST_AR == ("لكن", "لكنّ")
    for withheld in ("yet", "though", "although", "أما", "غير أن", "إلا أن"):
        assert withheld not in st._T2G2_CONTRAST_EN
        assert withheld not in st._T2G2_CONTRAST_AR


def test_the_declared_vocabularies_are_finite_and_scoped():
    assert len(st._T2G2_STOPWORDS_EN) == 68
    assert len(st._T2G2_STOPWORDS_AR) == 31
    assert len(st._T2G2_RELATIONS_EN) == 44
    assert len(st._T2G2_RELATIONS_AR) == 32
    assert len(st._T2G2_HYPOTHETICAL_EN) == 9
    assert len(st._T2G2_HYPOTHETICAL_AR) == 6
    for token in ("transfers", "carries", "runs", "measures"):
        assert token in st._T2G2_RELATIONS_EN
    for token in ("ينقل", "ينتقل", "يحمل"):
        assert token in st._T2G2_RELATIONS_AR
    # no competing ignorance list: registered detection stays the only owner
    from engine.progression_loop import _ACKNOWLEDGED_UNKNOWN_MARKERS
    for marker in _ACKNOWLEDGED_UNKNOWN_MARKERS:
        assert marker not in st._T2G2_HYPOTHETICAL_EN


# ==========================================================================
# 2. Version gating — three versions, each read as itself
# ==========================================================================
def test_the_rule_level_is_read_from_the_projects_own_version():
    assert st.t2g_rule_level(_State(version=None), gap_type=MC) == 0
    assert st.t2g_rule_level(_State(version=RECONSTRUCTION_VERSION), gap_type=MC) == 0
    assert st.t2g_rule_level(_State(version=ENGINE_CONTRACT_VERSION_T2G1), gap_type=MC) == 1
    assert st.t2g_rule_level(_State(), gap_type=MC) == 2
    # scope still bounds every version
    assert st.t2g_rule_level(_State(), gap_type="PHYSICAL_FEASIBILITY") == 0
    assert st.t2g_rule_level(_State(domain="software"), gap_type=MC) == 0
    assert st.is_t2g_active(_State(), gap_type=MC) is True
    assert st.is_t2g_active(_State(version=RECONSTRUCTION_VERSION), gap_type=MC) is False


@pytest.mark.parametrize("version", [None, "", "anything",
                                     "p4-2-level1-recon-v1-t2g9",
                                     "p4-2-level1-recon-v3"])
def test_an_unsupported_stamp_enables_nothing(version):
    assert st.t2g_rule_level(_State(version=version), gap_type=MC) == 0
    assert version not in SUPPORTED_ENGINE_CONTRACT_VERSIONS


def test_older_direct_callers_keep_their_default_behaviour():
    """`qualifying_carrier` defaults to the accepted level-1 rule."""
    import inspect
    signature = inspect.signature(st.qualifying_carrier)
    assert signature.parameters["rule_level"].default == 1
    assert st.qualifying_carrier(CONCISE_EN, Q2_ID, MATCH) is False
    assert st.qualifying_carrier(CONCISE_EN, Q2_ID, MATCH, rule_level=1) is False
    assert st.qualifying_carrier(CONCISE_EN, Q2_ID, MATCH, rule_level=2) is True


def test_level_two_is_a_union_and_never_withdraws_a_level_one_carrier():
    for text in (AFFIRMATIVE_EN, NEGATION_EN, CONCISE_AR, CONCISE_EE,
                 "The load path runs but the deck is red."):
        qid = "N-MC-2" if text is CONCISE_EE else Q2_ID
        if st.qualifying_carrier(text, qid, MATCH, rule_level=1):
            assert st.qualifying_carrier(text, qid, MATCH, rule_level=2) is True


# ==========================================================================
# 3. Clause scope
# ==========================================================================
@pytest.mark.parametrize("sentence,count", [
    ("I do not know the size but the load path runs", 2),
    ("no contrast boundary at all here", 1),
    ("لا أعرف المقاس لكن مسار الحمل ينتقل", 2),
    ("rebuttal buttress buttons", 1),          # never a substring boundary
    ("a and b and c", 1),                      # `and` is not a boundary
    ("أ و ب و ج", 1),                          # `و` is not a boundary
])
def test_only_registered_standalone_contrast_tokens_split(sentence, count):
    assert len(st._t2g2_clauses(sentence)) == count


def test_clauses_are_exact_substrings_of_the_original_text():
    sentence = DOTTED_I + " I do not know but the load path runs into the rail."
    for clause in st._t2g2_clauses(sentence):
        assert clause in sentence


@pytest.mark.parametrize("text", [
    HYPOTHETICAL_EN,
    "I do not know the load path but if the latch moved it would carry force.",
    "لا أعرف مسار الحمل لكن ربما ينقل المزلاج القوة إلى الإطار.",
])
def test_a_split_never_promotes_a_hypothetical_clause(text):
    assert st.qualifying_carrier(text, Q2_ID, MATCH, rule_level=2) is False


def test_a_split_never_detaches_text_still_inside_the_unknown():
    assert st.qualifying_carrier(UNKNOWN_EN, Q2_ID, MATCH, rule_level=2) is False
    assert st.qualifying_carrier(UNKNOWN_EN_YET, Q2_ID, MATCH, rule_level=2) is False
    assert st.qualifying_carrier(UNKNOWN_AR, Q2_ID, MATCH, rule_level=2) is False


# ==========================================================================
# 4. Concise carriers, and what must never become one
# ==========================================================================
@pytest.mark.parametrize("text", [CONCISE_EN, CONCISE_EN2, CONCISE_AR])
def test_a_concise_relation_between_roles_qualifies(text):
    assert st.qualifying_carrier(text, Q2_ID, MATCH, rule_level=2) is True


@pytest.mark.parametrize("text", [
    "Force path force path force path.",       # repetition only
    "مسار القوة مسار القوة مسار القوة.",
    DOTTED_I + " Force path force path force path.",
    "Hinge line.",                             # bare noun
    "Hinge line yesterday.",                   # two arbitrary content words
    "Force path thing.",
    "Load path Bob.",
    "Force path runs.",                        # relation with an empty side
    "Runs load path.",                         # relation with an empty side
])
def test_neither_repetition_nor_padding_nor_a_lone_relation_qualifies(text):
    assert st.qualifying_carrier(text, Q2_ID, MATCH, rule_level=2) is False
    assert st.qualifying_carrier(text, Q2_ID, MATCH, rule_level=1) is False


def test_a_relation_inside_a_committed_marker_still_counts_as_the_relation():
    """`transfers force` is itself a committed marker; the relation inside it
    may connect roles, but the marker alone never can."""
    assert MATCH("transfers force", Q2_ID) is True
    assert st.qualifying_carrier("transfers force", Q2_ID, MATCH, rule_level=2) is False
    assert st.qualifying_carrier("transfers force transfers force", Q2_ID,
                                 MATCH, rule_level=2) is False
    assert st.qualifying_carrier(CONCISE_EN, Q2_ID, MATCH, rule_level=2) is True


def test_the_uncertainty_purpose_distinction_is_unchanged():
    naming = "I do not know the latch tolerance; that detail would be missing."
    assert Q4_ID in st.UNCERTAINTY_QUESTION_IDS
    assert st.covers_variant(_State(), naming, Q4_ID, MATCH, gap_type=MC) is True
    assert st.covers_variant(_State(), naming, Q2_ID, MATCH, gap_type=MC) is False


def test_the_level_one_content_boundary_is_unchanged_at_level_two():
    assert st._MIN_CARRIER_CONTEXT_WORDS == 4
    assert st._carries_context("the load path aa bb", Q2_ID, MATCH) is False    # 3
    assert st._carries_context("the load path aa bb cc", Q2_ID, MATCH) is True  # 4


# ==========================================================================
# 5. Integrated routes — both domains, both languages
# ==========================================================================
def _t2g2(c, appmod, answer, seed=MECH_SEED, domain="mechanical"):
    sid = _start(c, seed, domain)
    _answer(c, sid, answer)
    return sid, _snapshot(appmod, sid)


@pytest.mark.parametrize("answer", [CONCISE_EN, CONCISE_EN2, MIXED_EN, MIXED_AR])
def test_concise_and_mixed_answers_now_progress(client, answer):
    c, appmod, db = client
    _login(c, appmod)
    sid, got = _t2g2(c, appmod, answer)
    assert _stamp(db, sid) == ENGINE_CONTRACT_VERSION_T2G2
    assert got["identity"] == Q3
    assert got["status"] == "PARTIAL"
    assert got["known_mechanism"] == "ASSERTED"
    assert got["coverage"] == COV_Q2
    assert got["records"] == 1
    assert UNKNOWN_NOTICE not in _page(c, sid)


def test_the_same_answers_are_unchanged_on_a_t2g1_project(client):
    c, appmod, db = client
    _login(c, appmod)
    for answer, identity, status, known in (
            (CONCISE_EN, Q2, "PARTIAL", "ASSERTED"),
            (MIXED_EN, Q2, "OPEN", None)):
        sid = _stamped_start(c, appmod, ENGINE_CONTRACT_VERSION_T2G1)
        _answer(c, sid, answer)
        got = _snapshot(appmod, sid)
        assert _stamp(db, sid) == ENGINE_CONTRACT_VERSION_T2G1
        assert got["identity"] == identity and got["status"] == status
        assert got["known_mechanism"] == known
        appmod.SESSION_STORE.clear()


def test_a_concise_electronics_answer_is_unchanged(client):
    c, appmod, _db = client
    _login(c, appmod)
    sid, got = _t2g2(c, appmod, CONCISE_EE, EE_SEED, "electronics_electrical")
    assert got["identity"] == EE3
    assert got["coverage"] == ["N-MC-2"]


@pytest.mark.parametrize("answer", [
    UNKNOWN_EN, UNKNOWN_EN_YET, UNKNOWN_AR, HYPOTHETICAL_EN,
    UNKNOWN_LEAD + "Force path force path force path.",
    UNKNOWN_LEAD + DOTTED_I + " Force path force path force path.",
    UNKNOWN_LEAD + "Hinge line.",
    UNKNOWN_LEAD + "Hinge line yesterday.",
    UNKNOWN_LEAD + "Force path runs.",
])
def test_unknowns_repetition_padding_and_decoys_still_supply_nothing(client, answer):
    c, appmod, _db = client
    _login(c, appmod)
    sid, got = _t2g2(c, appmod, answer)
    assert got["identity"] == Q2
    assert got["status"] == "OPEN"
    assert got["known_mechanism"] is None
    assert got["coverage"] == []
    assert got["unknowns"] == 1
    assert got["records"] == 1
    assert UNKNOWN_NOTICE in _page(c, sid)


@pytest.mark.parametrize("answer,known", [(NEGATION_EN, "ASSERTED"),
                                          (AFFIRMATIVE_EN, "REASONED")])
def test_negation_and_full_explanations_are_unchanged(client, answer, known):
    c, appmod, _db = client
    _login(c, appmod)
    _sid, got = _t2g2(c, appmod, answer)
    assert got["identity"] == Q3 and got["status"] == "PARTIAL"
    assert got["known_mechanism"] == known and got["coverage"] == COV_Q2


def test_a_described_relationship_is_not_verified_truth(client):
    """Quality stays with the untouched assessor: a concise description is
    ASSERTED, never promoted."""
    c, appmod, _db = client
    _login(c, appmod)
    _sid, got = _t2g2(c, appmod, CONCISE_EN)
    assert got["known_mechanism"] == "ASSERTED"


# ==========================================================================
# 6. Continuity: correction, replay, resume, raw answers, T2-D, cost
# ==========================================================================
@pytest.mark.parametrize("version", [RECONSTRUCTION_VERSION,
                                     ENGINE_CONTRACT_VERSION_T2G1,
                                     ENGINE_CONTRACT_VERSION_T2G2])
def test_live_replay_restart_and_resume_agree_on_every_version(client, version):
    c, appmod, db = client
    _login(c, appmod)
    sid = _stamped_start(c, appmod, version)
    _answer(c, sid, MIXED_EN)
    live = _snapshot(appmod, sid)
    appmod.SESSION_STORE.clear()
    session = reconstruct_readonly_state(appmod._get_store(), sid)
    assert session.review.level == 1
    assert getattr(session.state, "engine_contract_version", None) == version
    assert appmod._resolve_question_context(session.state, None).identity == \
        live["identity"]
    _raw(c, sid)
    assert c.post(f"/session/{sid}/resume", data={}).status_code == 302
    assert _snapshot(appmod, sid) == live
    assert _stamp(db, sid) == version


def test_corrections_recompute_in_both_directions(client):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _start(c)
    _answer(c, sid, UNKNOWN_EN)
    assert _snapshot(appmod, sid)["known_mechanism"] is None
    record = _active_answers(appmod, sid)[0]
    assert _correct(c, sid, record.record_id, CONCISE_EN).status_code in (302, 303)
    assert _snapshot(appmod, sid)["known_mechanism"] == "ASSERTED"
    record = _active_answers(appmod, sid)[0]
    assert _correct(c, sid, record.record_id, UNKNOWN_EN).status_code in (302, 303)
    got = _snapshot(appmod, sid)
    assert got["known_mechanism"] is None and got["status"] == "OPEN"
    assert got["identity"] == Q2


def test_the_raw_answer_is_preserved_and_the_unknown_part_is_not_promoted(client):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _start(c)
    _answer(c, sid, MIXED_EN)
    stored = _active_answers(appmod, sid)
    assert len(stored) == 1 and stored[0].content == MIXED_EN
    got = _snapshot(appmod, sid)
    assert got["unknowns"] == 1              # the unknown is still recorded once
    assert got["coverage"] == COV_Q2         # only the explained variant


def test_the_version_cannot_be_switched_through_request_fields(client):
    c, appmod, db = client
    _login(c, appmod)
    sid = _stamped_start(c, appmod, ENGINE_CONTRACT_VERSION_T2G1)
    _answer(c, sid, MIXED_EN,
            extra={"engine_contract_version": ENGINE_CONTRACT_VERSION_T2G2})
    assert _stamp(db, sid) == ENGINE_CONTRACT_VERSION_T2G1
    assert _snapshot(appmod, sid)["known_mechanism"] is None
    appmod.SESSION_STORE.clear()
    _raw(c, sid)
    c.post(f"/session/{sid}/resume",
           data={"engine_contract_version": ENGINE_CONTRACT_VERSION_T2G2})
    assert _stamp(db, sid) == ENGINE_CONTRACT_VERSION_T2G1
    assert _snapshot(appmod, sid)["version"] == ENGINE_CONTRACT_VERSION_T2G1


def test_t2d_binds_to_the_question_actually_displayed(client):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _start(c)
    _answer(c, sid, CONCISE_EN)
    entry = appmod.SESSION_STORE[sid]
    qctx = appmod._resolve_question_context(entry["state"], entry.get("last_result"))
    context = appmod._feedback_context(sid, entry["state"], qctx)
    assert qctx.identity == Q3
    assert context is not None and context["identity"] == Q3


def test_the_accepted_cold_suppression_boundary_is_intact(client):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _start(c)
    _answer(c, sid, CONCISE_EN)
    appmod.SESSION_STORE.clear()
    cold = _page(c, sid)
    assert 'id="reconstructed-review"' in cold
    assert re.search(r'class="t2d-cold-selected"', cold) is None
    assert getattr(appmod.SESSION_STORE[sid]["state"], "domain", None) is None


def test_the_disclosure_follows_the_projects_own_version_including_after_resume(client):
    c, appmod, _db = client
    _login(c, appmod)
    newest = _start(c)
    t2g1 = _stamped_start(c, appmod, ENGINE_CONTRACT_VERSION_T2G1)
    legacy = _stamped_start(c, appmod, RECONSTRUCTION_VERSION)
    text = appmod.ui_text.text
    assert text("UI_T2G2_QUESTION_SET", "en") in _page(c, newest)
    assert text("UI_T2G_QUESTION_SET", "en") in _page(c, t2g1)
    assert text("UI_T1D_QUESTION_SET", "en") in _page(c, legacy)
    assert text("UI_T2G2_QUESTION_SET", "ar") in _page(c, newest, "ar")
    # and the project's own wording survives an explicit resume
    _answer(c, t2g1, CONCISE_EN)
    appmod.SESSION_STORE.clear()
    _raw(c, t2g1)
    assert c.post(f"/session/{t2g1}/resume", data={}).status_code == 302
    page = _page(c, t2g1)
    assert text("UI_T2G_QUESTION_SET", "en") in page
    assert text("UI_T2G2_QUESTION_SET", "en") not in page


def test_bounded_cost_at_the_accepted_input_limit(client):
    """The new path adds bounded local work only; the limit is not reduced."""
    import time
    from web.app import MAX_FREE_TEXT_CHARS
    for body in ((("alpha " * 3330) + "load path")[:MAX_FREE_TEXT_CHARS - 1],
                 (("but the load path runs into the rail. ") * 400)[:MAX_FREE_TEXT_CHARS - 1],
                 ((DOTTED_I + " but load path transfers force. ") * 400)[:MAX_FREE_TEXT_CHARS - 1]):
        start = time.perf_counter()
        st.qualifying_carrier(body, Q2_ID, MATCH, rule_level=2)
        assert time.perf_counter() - start < 5.0
