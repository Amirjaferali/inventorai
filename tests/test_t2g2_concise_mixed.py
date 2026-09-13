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


# ==========================================================================
# 7. `PR643-T2G2-SCOPE-REPAIR-01` — a boundary does not clear governing scope.
#
# PROVENANCE, stated plainly: every fixture below is a regression NEWLY
# CONSTRUCTED by the implementing session for this bounded repair. The two
# route answers restate the Lead's adopted `C` findings, which came from
# applying the original requirement — not from the independent review, whose
# verdict on the reviewed head was `B` and stands unaltered.
#
# Each guard is proved by a MATCHED PAIR that differs only in the cue, so a
# refusal is attributable to the scope and not to some other property of the
# sentence. Every refusal reaches the T2-G-2 path only.
# ==========================================================================
BACKREF_EN = ("The deck transfers force into the rail, but I do not know if "
              "that is right.")
BACKREF_AR = "السطح ينقل القوة إلى الإطار لكن لا أعرف إن كان ذلك صحيحًا."
BACKREF_DETAIL_EN = ("The deck transfers force into the rail, but I do not "
                     "know the bolt torque.")
BACKREF_NAMED_EN = ("The deck transfers force into the rail, but I do not "
                    "know if that load path is right.")
BACKREF_FIRST_EN = ("I do not know if that is right, but deck transfers force "
                    "into rail.")
CONCISE_QUESTION_EN = "Deck transfers force into rail?"
CONCISE_QUESTION_AR = "السطح ينقل القوة إلى الإطار؟"
QUESTION_THEN_ANSWER = "What is the load path? Deck transfers force into rail."
ANSWER_THEN_QUESTION = "Deck transfers force into rail. Is that right?"
MIXED_QUESTION_EN = ("I do not know the bolt size, but does the load path run "
                     "from the deck into the hinge line?")
MIXED_QUESTION_AR = ("لا أعرف مقاس البرغي لكن هل مسار الحمل ينتقل من لوح "
                     "السطح إلى خط المفصلة؟")
REPORTED_MIXED_EN = ("I do not know the bolt size but they say the load path "
                     "runs from the deck into the hinge line.")
REPORTED_MIXED_AR = ("لا أعرف مقاس البرغي لكن يقولون إن مسار الحمل ينتقل من "
                     "لوح السطح إلى خط المفصلة.")
READS_EN = ("I do not know the housing, but the sensor reads the load path "
            "from the deck panel.")
QUOTED_SEGMENT_EN = '"Deck transfers force into rail."'
QUOTED_CLAUSE_EN = ('I do not know the bolt size but "the load path runs from '
                    'the deck into the hinge line".')
QUOTED_COMPONENT_EN = ('The "deck" transfers force into rail, but I do not '
                       'know the bolt size.')
_SUPPOSE_TAIL = "the load path runs from the deck into the hinge line"
SUPPOSED_EN = ("Suppose the latch fails, but I do not know the bolt size, "
               "however " + _SUPPOSE_TAIL + ".")
SUPPOSED_CONTROL_EN = ("The latch fails, but I do not know the bolt size, "
                       "however " + _SUPPOSE_TAIL + ".")
SUPPOSED_AFTER_EN = ("I do not know the bolt size, but " + _SUPPOSE_TAIL +
                     ", however suppose the latch fails.")
SUPPOSED_AR = ("لو تعطل المزلاج لكن لا أعرف مقاس البرغي لكن مسار الحمل ينتقل "
               "من لوح السطح إلى خط المفصلة.")
SUPPOSED_CONTROL_AR = ("المزلاج يتعطل لكن لا أعرف مقاس البرغي لكن مسار الحمل "
                       "ينتقل من لوح السطح إلى خط المفصلة.")

# (label, refused-under-t2g2, admitted-under-t2g2) — identical but for the cue.
SCOPE_PAIRS = (
    ("back-reference EN", BACKREF_EN, BACKREF_DETAIL_EN),
    ("back-reference AR", BACKREF_AR,
     "السطح ينقل القوة إلى الإطار لكن لا أعرف مقاس البرغي."),
    # `PR643-T2G2-SCOPE-REPAIR-02` CORRECTS this row. It shipped with
    # BACKREF_NAMED_EN on the ADMITTED side, which encoded the defect: an
    # uncertainty that repeats the very mechanism it doubts is not made
    # independent by naming it. It is now the refused side.
    ("back-reference naming committed material", BACKREF_NAMED_EN,
     BACKREF_DETAIL_EN),
    ("back-reference direction", BACKREF_EN, BACKREF_FIRST_EN),
    ("question EN", CONCISE_QUESTION_EN, CONCISE_EN),
    ("question per segment", MIXED_QUESTION_EN, MIXED_EN),
    ("question is not sentence-wide", MIXED_QUESTION_EN, ANSWER_THEN_QUESTION),
    ("question AR across a boundary", MIXED_QUESTION_AR, MIXED_AR),
    ("reported speech EN", REPORTED_MIXED_EN, MIXED_EN),
    ("reported speech AR", REPORTED_MIXED_AR, MIXED_AR),
    ("a relation verb is not a reporting frame", REPORTED_MIXED_EN, READS_EN),
    ("wholly quoted segment", QUOTED_SEGMENT_EN, CONCISE_EN),
    ("wholly quoted clause", QUOTED_CLAUSE_EN, MIXED_EN),
    ("quotation labelling a component", QUOTED_SEGMENT_EN, QUOTED_COMPONENT_EN),
    ("supposition governs rightward EN", SUPPOSED_EN, SUPPOSED_CONTROL_EN),
    ("supposition after the carrier EN", SUPPOSED_EN, SUPPOSED_AFTER_EN),
    ("supposition governs rightward AR", SUPPOSED_AR, SUPPOSED_CONTROL_AR),
)


@pytest.mark.parametrize("label,refused,admitted", SCOPE_PAIRS,
                         ids=[p[0] for p in SCOPE_PAIRS])
def test_each_governing_scope_is_decided_against_a_matched_control(
        label, refused, admitted):
    """The pair differs only in the cue, so the refusal is the cue's doing."""
    assert st.qualifying_carrier(refused, Q2_ID, MATCH, rule_level=2) is False
    assert st.qualifying_carrier(admitted, Q2_ID, MATCH, rule_level=2) is True


@pytest.mark.parametrize("label,refused,admitted", SCOPE_PAIRS,
                         ids=[p[0] for p in SCOPE_PAIRS])
def test_no_governing_scope_refusal_withdraws_a_level_one_carrier(
        label, refused, admitted):
    """Level 2 stays a strict UNION over level 1: every one of these fixtures
    that level 1 accepts is still accepted at level 2. The refusals reach only
    what T2-G-2 would NEWLY admit."""
    for text in (refused, admitted):
        if st.qualifying_carrier(text, Q2_ID, MATCH, rule_level=1):
            assert st.qualifying_carrier(text, Q2_ID, MATCH, rule_level=2)


def test_the_refused_fixtures_are_decided_by_scope_not_by_level_one():
    """Guard on the guards: each refused fixture must be one level 1 already
    declined, otherwise the pair above would prove nothing about T2-G-2."""
    for _label, refused, _admitted in SCOPE_PAIRS:
        assert st.qualifying_carrier(refused, Q2_ID, MATCH, rule_level=1) is False


def test_the_governing_scope_cues_are_finite_and_enumerated():
    assert len(st._T2G2_ANAPHORA_EN) == 6
    assert len(st._T2G2_ANAPHORA_AR) == 9
    assert len(st._T2G2_REPORTED_EN) == 13
    assert len(st._T2G2_REPORTED_AR) == 6
    assert st._T2G2_QUOTE_PAIRS == (('"', '"'), ("“", "”"), ("«", "»"))
    assert len(st._T2G2_UNCERTAINTY_PARTICLES_EN) == 10
    assert len(st._T2G2_UNCERTAINTY_PARTICLES_AR) == 6
    assert st._T2G2_EXTENT_MAX_WORDS == 6
    assert st._T2G2_INTERROGATIVE == ("?", "؟")
    # the subordinating openers are a SUBSET of the accepted hypothetical cues
    for cue in st._T2G2_SUBORDINATING_HYPOTHETICAL:
        assert any(registered.strip() == cue for registered in
                   st._T2G2_HYPOTHETICAL_EN + st._T2G2_HYPOTHETICAL_AR)
    # no apostrophe is treated as a quotation mark
    for pair in st._T2G2_QUOTE_PAIRS:
        assert "'" not in pair and "’" not in pair


@pytest.mark.parametrize("text", [
    "a. b! c? d; e", "أ؟ ب؛ ج", "لا أعرف مسار الحمل، ولم أحدد شيئا",
    BACKREF_EN, CONCISE_QUESTION_EN, MIXED_AR, QUESTION_THEN_ANSWER,
    "", "   ", "one\ntwo\r\nthree", "trailing.", ".leading",
])
def test_public_sentences_behaviour_is_unchanged_by_the_record_form(text):
    """`sentences()` is now derived from `_sentence_records`; its output must
    stay exactly the previous split, so no existing consumer moves."""
    import re as _re
    previous = tuple(part for part in st._SENTENCE_BOUNDARY_RE.split(text)
                     if part.strip()) if isinstance(text, str) and text else ()
    assert st.sentences(text) == previous
    assert isinstance(previous, tuple)
    del _re


def test_the_records_carry_the_original_terminator_and_offset():
    records = st._sentence_records("Deck transfers force into rail? Yes.")
    assert [(segment.strip(), terminator) for segment, terminator, _o in records] \
        == [("Deck transfers force into rail", "?"), ("Yes", ".")]
    for segment, _terminator, offset in records:
        assert "Deck transfers force into rail? Yes."[offset:offset + len(segment)] \
            == segment
    assert st._sentence_records("no terminator")[0][1] == ""


def test_an_unreadable_quotation_scan_falls_back_to_level_one(monkeypatch):
    """A failure while establishing scope must never grant new support."""
    def boom(_text):
        raise RuntimeError("scope unreadable")
    monkeypatch.setattr(st, "_t2g2_quote_spans", boom)
    assert st.qualifying_carrier(CONCISE_EN, Q2_ID, MATCH, rule_level=2) is False
    assert st.qualifying_carrier(AFFIRMATIVE_EN, Q2_ID, MATCH,
                                 rule_level=2) is True   # level 1 still stands


def test_bounded_cost_with_the_new_scope_cues(client):
    """The four scope decisions add bounded local work only."""
    import time
    from web.app import MAX_FREE_TEXT_CHARS
    for body in ((BACKREF_EN + " ") * 400, (QUOTED_CLAUSE_EN + " ") * 300,
                 ('"' * 4000) + (CONCISE_EN + " ") * 300,
                 (SUPPOSED_EN + " ") * 200):
        body = body[:MAX_FREE_TEXT_CHARS - 1]
        start = time.perf_counter()
        st.qualifying_carrier(body, Q2_ID, MATCH, rule_level=2)
        assert time.perf_counter() - start < 5.0


# ---- the two findings, as fully specified supported journeys ---------------
_SCOPE_ROUTE_UNCHANGED = {
    "identity": Q2, "gap": MC, "status": "OPEN", "known_mechanism": None,
    "coverage": [], "unknowns": 1, "records": 1,
}


def test_finding_one_backward_referencing_uncertainty_supplies_no_mechanism(client):
    """`The deck transfers force into the rail, but I do not know if that is
    right.` The doubt is about the explanation itself, so T2-G-2 must read it
    exactly as T2-G-1 does — and still record the unknown once."""
    c, appmod, db = client
    _login(c, appmod)
    seen = {}
    for version in (ENGINE_CONTRACT_VERSION_T2G1, ENGINE_CONTRACT_VERSION_T2G2):
        sid = _stamped_start(c, appmod, version)
        _answer(c, sid, BACKREF_EN)
        snapshot = _snapshot(appmod, sid)
        assert snapshot == dict(_SCOPE_ROUTE_UNCHANGED, version=version), version
        assert _stamp(db, sid) == version
        assert UNKNOWN_NOTICE in _page(c, sid)
        seen[version] = snapshot
    assert seen[ENGINE_CONTRACT_VERSION_T2G1]["identity"] == \
        seen[ENGINE_CONTRACT_VERSION_T2G2]["identity"] == Q2


def test_finding_three_a_concise_question_supplies_no_mechanism(client):
    """`Deck transfers force into rail?` asks for the mechanism. T2-G-2 must
    neither cover Q2 nor advance the served question beyond it; the older
    quality reading of the same answer is untouched."""
    c, appmod, db = client
    _login(c, appmod)
    for version in (ENGINE_CONTRACT_VERSION_T2G1, ENGINE_CONTRACT_VERSION_T2G2):
        sid = _stamped_start(c, appmod, version)
        _answer(c, sid, CONCISE_QUESTION_EN)
        assert _snapshot(appmod, sid) == {
            "version": version, "identity": Q2, "gap": MC, "status": "PARTIAL",
            "known_mechanism": "ASSERTED", "coverage": [], "unknowns": 0,
            "records": 1}, version
        assert _stamp(db, sid) == version


@pytest.mark.parametrize("answer,identity,coverage", [
    (BACKREF_DETAIL_EN, Q3, COV_Q2),
    (QUOTED_COMPONENT_EN, Q3, COV_Q2),
    (ANSWER_THEN_QUESTION, Q3, COV_Q2),
])
def test_genuine_explanations_beside_these_cues_still_progress(
        client, answer, identity, coverage):
    """Positive route controls: uncertainty about an INDEPENDENT detail, a
    quotation that merely labels a component, and a question that follows a
    real assertion all keep their T2-G-2 progress."""
    c, appmod, _db = client
    _login(c, appmod)
    sid = _stamped_start(c, appmod, ENGINE_CONTRACT_VERSION_T2G2)
    _answer(c, sid, answer)
    snapshot = _snapshot(appmod, sid)
    assert snapshot["identity"] == identity
    assert snapshot["coverage"] == coverage
    assert snapshot["status"] == "PARTIAL"


@pytest.mark.parametrize("answer", [BACKREF_EN, CONCISE_QUESTION_EN])
def test_the_repaired_readings_survive_replay_restart_and_resume(client, answer):
    c, appmod, db = client
    _login(c, appmod)
    sid = _stamped_start(c, appmod, ENGINE_CONTRACT_VERSION_T2G2)
    _answer(c, sid, answer)
    live = _snapshot(appmod, sid)
    appmod.SESSION_STORE.clear()
    session = reconstruct_readonly_state(appmod._get_store(), sid)
    assert getattr(session.state, "engine_contract_version", None) == \
        ENGINE_CONTRACT_VERSION_T2G2
    assert appmod._resolve_question_context(session.state, None).identity == \
        live["identity"]
    _raw(c, sid)
    assert c.post(f"/session/{sid}/resume", data={}).status_code == 302
    assert _snapshot(appmod, sid) == live
    assert _stamp(db, sid) == ENGINE_CONTRACT_VERSION_T2G2


def test_a_correction_can_still_turn_a_doubted_explanation_into_a_real_one(client):
    """The refusal is a reading of THIS answer, never a lock: correcting the
    doubted sentence into a plain explanation recomputes to mechanism support."""
    c, appmod, _db = client
    _login(c, appmod)
    sid = _stamped_start(c, appmod, ENGINE_CONTRACT_VERSION_T2G2)
    _answer(c, sid, BACKREF_EN)
    assert _snapshot(appmod, sid)["identity"] == Q2
    record_id = _active_answers(appmod, sid)[0].record_id
    assert _correct(c, sid, record_id, AFFIRMATIVE_EN).status_code == 302
    after = _snapshot(appmod, sid)
    assert after["identity"] == Q3
    assert after["coverage"] == COV_Q2
    assert after["known_mechanism"] == "REASONED"


# ==========================================================================
# 8. `PR643-T2G2-SCOPE-REPAIR-02` — the back-reference exemption is gone, and
#    object-less uncertainty is recognised.
#
# PROVENANCE. The two English route answers and the Arabic fragment
# `مسار الحمل هذا` are what the independent differential review reported on
# `406d893b`; the surrounding Arabic sentences, every control and every unit
# case below were CONSTRUCTED by the implementing session. No fixture here is
# presented as reviewer-authored beyond that fragment.
# ==========================================================================
NAMED_REF_AR = ("السطح ينقل القوة إلى الإطار لكن لا أعرف إن كان مسار الحمل "
                "هذا صحيحًا.")
OBJECTLESS_EN = "The deck transfers force into the rail, but I'm not sure."
OBJECTLESS_EN2 = "The deck transfers force into the rail, but I do not know."
OBJECTLESS_EN_YET = ("The deck transfers force into the rail, but I am not "
                     "sure yet.")
OBJECTLESS_AR = "السطح ينقل القوة إلى الإطار لكن لست متأكدًا."
OBJECTLESS_AR2 = "السطح ينقل القوة إلى الإطار لكن لم أحدد بعد."
DETAIL_AR = "السطح ينقل القوة إلى الإطار لكن لا أعرف مقاس البرغي."

SCOPE_PAIRS_02 = (
    ("named reference EN", BACKREF_NAMED_EN, BACKREF_DETAIL_EN),
    ("named reference AR", NAMED_REF_AR, DETAIL_AR),
    ("object-less EN", OBJECTLESS_EN, BACKREF_DETAIL_EN),
    ("object-less EN bare", OBJECTLESS_EN2, BACKREF_DETAIL_EN),
    ("object-less EN particle", OBJECTLESS_EN_YET, BACKREF_DETAIL_EN),
    ("object-less AR", OBJECTLESS_AR, DETAIL_AR),
    ("object-less AR particle", OBJECTLESS_AR2, DETAIL_AR),
)


@pytest.mark.parametrize("label,refused,admitted", SCOPE_PAIRS_02,
                         ids=[p[0] for p in SCOPE_PAIRS_02])
def test_backward_reference_no_longer_exempts_a_named_or_object_less_unknown(
        label, refused, admitted):
    """Each pair differs only in what the uncertainty is ABOUT."""
    assert st.qualifying_carrier(refused, Q2_ID, MATCH, rule_level=2) is False
    assert st.qualifying_carrier(admitted, Q2_ID, MATCH, rule_level=2) is True


@pytest.mark.parametrize("label,refused,admitted", SCOPE_PAIRS_02,
                         ids=[p[0] for p in SCOPE_PAIRS_02])
def test_the_new_refusals_are_decided_by_scope_not_by_level_one(
        label, refused, admitted):
    """Level 1 already declines every refused fixture, so the pair says
    something about T2-G-2 — and level 2 stays a union over level 1."""
    assert st.qualifying_carrier(refused, Q2_ID, MATCH, rule_level=1) is False
    for text in (refused, admitted):
        if st.qualifying_carrier(text, Q2_ID, MATCH, rule_level=1):
            assert st.qualifying_carrier(text, Q2_ID, MATCH, rule_level=2)


def test_naming_the_committed_mechanism_no_longer_exempts_the_uncertainty():
    """The removed exemption, stated directly: the doubted clause repeats this
    question's own committed marker and is still a back-reference."""
    clauses = st._t2g2_clauses(BACKREF_NAMED_EN.rstrip("."))
    doubting = clauses[-1]
    assert st._marker_spans(doubting, Q2_ID)          # it DOES name the marker
    assert st._t2g2_back_reference_index(clauses) == len(clauses) - 1


# ---- the residual-content approach, validated against registered forms ----
@pytest.mark.parametrize("clause,names_subject", [
    (" I do not know the bolt torque.", True),
    (" I am not sure about the bolt size.", True),
    (" I do not know if that load path is right.", True),   # anaphor rule's job
    (" I'm not sure.", False),
    (" I do not know.", False),
    (" I have not decided.", False),
    (" I do not know yet.", False),                          # particle residue
    (" I am not sure yet.", False),
    (" لا أعرف مقاس البرغي.", True),
    (" لست متأكدًا.", False),                                 # one-letter residue
    (" لم أحدد بعد.", False),                                 # particle residue
    (" لا أعلم.", False),
])
def test_the_residue_test_reads_actual_registered_forms(clause, names_subject):
    """Validated against the REGISTERED surfaces rather than assumed. Two
    Arabic forms make the naive residue reading wrong and are handled: the
    registry surface `لست متاكد` leaves the one-character inflection `ا`, and
    `لم احدد` leaves the particle `بعد`. Neither is a named subject."""
    assert st.declares_ignorance(clause)
    assert st._t2g2_names_own_subject(clause) is names_subject


def test_the_arabic_extent_comes_from_the_canonical_detector():
    """No surface list is copied and no normaliser is introduced here: the
    extent is the leftmost shortest window the registry detector recognises."""
    from engine.semantic_registry import detect_registered_unknown
    clause = " لا أعرف مقاس البرغي."
    start, stop = st._t2g2_registered_extent(clause)
    assert clause[start:stop] == "لا أعرف"
    assert detect_registered_unknown(clause[start:stop]) is not None
    assert st._t2g2_registered_extent(" the deck transfers force") is None
    # bounded: windows are capped, never an unbounded search
    assert st._T2G2_EXTENT_MAX_WORDS == 6


def test_a_pronoun_outside_a_registered_unknown_is_never_a_veto():
    """The anaphor test is consulted only inside a clause the registered
    detector already recognised."""
    plain = "The deck holds it, but the load path runs from the deck into the hinge line."
    assert st._t2g2_back_reference_index(st._t2g2_clauses(plain)) is None
    assert st.qualifying_carrier(plain, Q2_ID, MATCH, rule_level=2) is True


# ---- reported-frame coordinate correction ---------------------------------
_REPORTED_TAIL = " they say the load path runs from the deck into the hinge line"


@pytest.mark.parametrize("expansions", [0, 1, 3, 20])
def test_a_reported_frame_is_located_in_one_coordinate_system(expansions):
    """The cue is found in `clause.lower()` while the marker span is measured
    on the ORIGINAL clause, and `str.lower()` is not length-preserving. Twenty
    U+0130 before the frame pushed the lowered offset past the original marker
    start, so the frame stopped governing. The controls with no or short
    expansion are unchanged."""
    clause = (DOTTED_I * expansions) + _REPORTED_TAIL
    assert st._t2g2_is_reported(clause, st._marker_spans(clause, Q2_ID)) is True
    sentence = "I do not know the bolt size but " + clause + "."
    assert st.qualifying_carrier(sentence, Q2_ID, MATCH, rule_level=2) is False


def test_the_expansion_is_real_and_the_raw_clause_is_untouched():
    clause = (DOTTED_I * 20) + _REPORTED_TAIL
    before = clause
    st._t2g2_is_reported(clause, st._marker_spans(clause, Q2_ID))
    assert clause == before
    assert len(clause.lower()) == len(clause) + 20
    assert clause.lower().find("they say") > st._marker_spans(clause, Q2_ID)[0][0]


def test_an_unmappable_reported_clause_refuses_rather_than_guesses(monkeypatch):
    """Conservative failure handling: when the two coordinate systems cannot be
    reconciled, the clause is treated as governed rather than guessed at. The
    spans are taken BEFORE the map is broken, so this exercises the reported
    check itself and not `_marker_spans`' own refusal."""
    clause = (DOTTED_I * 20) + _REPORTED_TAIL
    spans = st._marker_spans(clause, Q2_ID)
    assert spans
    monkeypatch.setattr(st, "_lowered_to_original", lambda *_a: None)
    assert st._t2g2_is_reported(clause, spans) is True


# ---- integrated journeys, full state asserted together --------------------
_SCOPE02_UNCHANGED = {
    "identity": Q2, "gap": MC, "status": "OPEN", "known_mechanism": None,
    "coverage": [], "unknowns": 1, "records": 1,
}
REPORTED_DOTTED = ("I do not know the bolt size but " + (DOTTED_I * 20) +
                   _REPORTED_TAIL + ".")


@pytest.mark.parametrize("answer", [
    BACKREF_NAMED_EN, OBJECTLESS_EN, NAMED_REF_AR, OBJECTLESS_AR,
    REPORTED_DOTTED])
def test_the_remaining_scope_journeys_read_the_same_on_both_versions(
        client, answer):
    """Full served identity, gap state, canonical knowledge, coverage and
    unknown tracking together — a carrier Boolean proves none of them."""
    c, appmod, db = client
    _login(c, appmod)
    for version in (ENGINE_CONTRACT_VERSION_T2G1, ENGINE_CONTRACT_VERSION_T2G2):
        sid = _stamped_start(c, appmod, version)
        _answer(c, sid, answer)
        assert _snapshot(appmod, sid) == dict(_SCOPE02_UNCHANGED,
                                              version=version), version
        assert _stamp(db, sid) == version


@pytest.mark.parametrize("answer", [BACKREF_DETAIL_EN, DETAIL_AR])
def test_independent_detail_uncertainty_still_progresses_on_both_scripts(
        client, answer):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _stamped_start(c, appmod, ENGINE_CONTRACT_VERSION_T2G2)
    _answer(c, sid, answer)
    assert _snapshot(appmod, sid) == {
        "version": ENGINE_CONTRACT_VERSION_T2G2, "identity": Q3, "gap": MC,
        "status": "PARTIAL", "known_mechanism": "REASONED",
        "coverage": COV_Q2, "unknowns": 1, "records": 1}


@pytest.mark.parametrize("answer", [BACKREF_NAMED_EN, OBJECTLESS_AR])
def test_the_new_readings_survive_replay_restart_and_resume(client, answer):
    c, appmod, db = client
    _login(c, appmod)
    sid = _stamped_start(c, appmod, ENGINE_CONTRACT_VERSION_T2G2)
    _answer(c, sid, answer)
    live = _snapshot(appmod, sid)
    appmod.SESSION_STORE.clear()
    session = reconstruct_readonly_state(appmod._get_store(), sid)
    assert appmod._resolve_question_context(session.state, None).identity == \
        live["identity"]
    _raw(c, sid)
    assert c.post(f"/session/{sid}/resume", data={}).status_code == 302
    assert _snapshot(appmod, sid) == live
    assert _stamp(db, sid) == ENGINE_CONTRACT_VERSION_T2G2


def test_the_raw_answer_is_stored_verbatim_and_the_unknown_recorded_once(client):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _stamped_start(c, appmod, ENGINE_CONTRACT_VERSION_T2G2)
    _answer(c, sid, OBJECTLESS_EN)
    records = _active_answers(appmod, sid)
    assert len(records) == 1
    assert records[0].content == OBJECTLESS_EN
    assert _snapshot(appmod, sid)["unknowns"] == 1


def test_corrections_recompute_in_both_directions_across_the_new_rule(client):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _stamped_start(c, appmod, ENGINE_CONTRACT_VERSION_T2G2)
    _answer(c, sid, OBJECTLESS_EN)
    assert _snapshot(appmod, sid)["identity"] == Q2
    first = _active_answers(appmod, sid)[0].record_id
    assert _correct(c, sid, first, AFFIRMATIVE_EN).status_code == 302
    after = _snapshot(appmod, sid)
    assert (after["identity"], after["coverage"]) == (Q3, COV_Q2)
    second = _active_answers(appmod, sid)[0].record_id
    assert _correct(c, sid, second, NAMED_REF_AR).status_code == 302
    back = _snapshot(appmod, sid)
    assert (back["identity"], back["coverage"], back["known_mechanism"]) == \
        (Q2, [], None)


def test_a_scope_failure_still_falls_back_to_the_level_one_answer(monkeypatch):
    def boom(_clauses):
        raise RuntimeError("scope unreadable")
    monkeypatch.setattr(st, "_t2g2_back_reference_index", boom)
    assert st.qualifying_carrier(BACKREF_NAMED_EN, Q2_ID, MATCH,
                                 rule_level=2) is False
    assert st.qualifying_carrier(AFFIRMATIVE_EN, Q2_ID, MATCH,
                                 rule_level=2) is True


def test_bounded_cost_of_the_registered_extent_probe(monkeypatch):
    """`PR643-T2G2-SCOPE-REPAIR-03` CORRECTS this test's premise.

    As shipped on `2de82db8` it measured nothing of the kind it claimed. Two
    faults, both established by the independent review and reproduced here:
    the two long bodies carried no contrast boundary, so `_t2g2_clause_carrier`
    returned before the back-reference check and the extent probe was never
    called; and truncating `"load path " * 2000` to the input limit removed the
    trailing registered cue outright, leaving a body with no unknown in it at
    all.

    The corrected bodies keep the registered unknown after truncation, cross the
    contrast-clause path, and put the surface at the END of the long ignorance
    clause — the worst case for a left-to-right probe. The premise is ASSERTED,
    not assumed: the cue must still be present, the sentence must split, and the
    probe must actually be entered.

    The ceiling stays the existing 5-second safety bound. The measurements are
    evidence that this path is currently practical on this machine, not a
    performance guarantee."""
    import time
    from web.app import MAX_FREE_TEXT_CHARS

    seen = {"calls": 0}
    real_extent = st._t2g2_registered_extent

    def counting_extent(clause):
        seen["calls"] += 1
        return real_extent(clause)
    monkeypatch.setattr(st, "_t2g2_registered_extent", counting_extent)

    cases = (("القوة تنتقل هنا لكن ", "مسار الحمل ", " لست متأكدا"),
             ("Force runs here but ", "load path ", " I am not sure"))
    for prefix, filler, suffix in cases:
        repeats = ((MAX_FREE_TEXT_CHARS - 1 - len(prefix) - len(suffix))
                   // len(filler))
        body = prefix + (filler * repeats) + suffix
        assert len(body) < MAX_FREE_TEXT_CHARS
        # premise 1 — the registered unknown survived sizing
        assert suffix.strip() in body
        assert st.declares_ignorance(body)
        # premise 2 — the contrast-clause path is crossed
        assert len(st._t2g2_clauses(st.sentences(body)[0])) > 1
        seen["calls"] = 0
        start = time.perf_counter()
        st.qualifying_carrier(body, Q2_ID, MATCH, rule_level=2)
        elapsed = time.perf_counter() - start
        # premise 3 — the probe was actually entered
        assert seen["calls"] >= 1
        assert elapsed < 5.0


# ==========================================================================
# 9. `PR643-T2G2-SCOPE-REPAIR-03` — a vowelled Arabic demonstrative is still
#    a demonstrative.
#
# PROVENANCE. The plain and diacritized Arabic answers below are the pair the
# independent differential review reproduced on `2de82db8`. Every control in
# this section is an implementation-session fixture and is not attributed to
# the reviewer.
# ==========================================================================
BACKREF_AR_PLAIN = "السطح ينقل القوة إلى الإطار لكن لا أعرف إن كان ذلك صحيحًا."
BACKREF_AR_DIACRITIZED = ("السطح ينقل القوة إلى الإطار لكن لا أعرف إن كان "
                          "ذَلِكَ صحيحًا.")
DETAIL_AR_DIACRITIZED = "السطح ينقل القوة إلى الإطار لكن لا أعرف مَقاسَ البُرغي."


def test_the_declared_arabic_marks_are_exactly_the_reviewed_range():
    assert st._T2G2_ARABIC_MARKS == frozenset(
        [chr(point) for point in range(0x064B, 0x0653)] + [chr(0x0670)])
    assert len(st._T2G2_ARABIC_MARKS) == 9
    for mark in ("\u064b", "\u064e", "\u0650", "\u0651", "\u0652", "\u0670"):
        assert mark in st._T2G2_ARABIC_MARKS
    # marks only: no letter, no digit and no punctuation is ever dropped
    for keep in ("ذ", "ل", "ك", "أ", "ا", "و", ".", "،", "9", "a"):
        assert keep not in st._T2G2_ARABIC_MARKS


def test_mark_free_text_is_returned_unchanged_and_the_input_is_never_rewritten():
    plain = "لا أعرف إن كان ذلك صحيحا"
    assert st._t2g2_without_arabic_marks(plain) is plain
    vowelled = "ذَلِكَ"
    before = vowelled
    assert st._t2g2_without_arabic_marks(vowelled) == "ذلك"
    assert vowelled == before


def test_dropping_marks_does_not_invent_an_anaphor_in_unrelated_arabic():
    """The positive control: removing the marks must not turn ordinary vowelled
    Arabic into a backward reference."""
    for clause in (" لا أعرف مَقاسَ البُرغي", " مسار الحمل يَنتقل إلى الإطار",
                   " لا أعرف عَزمَ الشد"):
        assert st._t2g2_has_anaphor(clause) is False
    # and the vowelled demonstrative IS recognised
    assert st._t2g2_has_anaphor(" لا أعرف إن كان ذَلِكَ صحيحًا") is True


@pytest.mark.parametrize("answer,label", [
    (BACKREF_AR_PLAIN, "plain backward reference"),
    (BACKREF_AR_DIACRITIZED, "diacritized backward reference"),
])
def test_a_vowelled_arabic_back_reference_supplies_no_mechanism(
        client, answer, label):
    """Full route result on BOTH versions, so the no-new-support boundary is
    explicit rather than inferred from a private helper."""
    c, appmod, db = client
    _login(c, appmod)
    for version in (ENGINE_CONTRACT_VERSION_T2G1, ENGINE_CONTRACT_VERSION_T2G2):
        sid = _stamped_start(c, appmod, version)
        _answer(c, sid, answer)
        assert _snapshot(appmod, sid) == {
            "version": version, "identity": Q2, "gap": MC, "status": "OPEN",
            "known_mechanism": None, "coverage": [], "unknowns": 1,
            "records": 1}, (label, version)
        assert _stamp(db, sid) == version


@pytest.mark.parametrize("answer", [DETAIL_AR, DETAIL_AR_DIACRITIZED])
def test_a_genuine_independent_detail_still_progresses_vowelled_or_not(
        client, answer):
    """The route-level positive control: an Arabic uncertainty about a separate
    detail keeps its T2-G-2 progress whether or not it carries marks, and is
    unchanged on T2-G-1."""
    c, appmod, _db = client
    _login(c, appmod)
    plain_side = _stamped_start(c, appmod, ENGINE_CONTRACT_VERSION_T2G1)
    _answer(c, plain_side, answer)
    assert _snapshot(appmod, plain_side)["identity"] == Q2
    sid = _stamped_start(c, appmod, ENGINE_CONTRACT_VERSION_T2G2)
    _answer(c, sid, answer)
    assert _snapshot(appmod, sid) == {
        "version": ENGINE_CONTRACT_VERSION_T2G2, "identity": Q3, "gap": MC,
        "status": "PARTIAL", "known_mechanism": "REASONED",
        "coverage": COV_Q2, "unknowns": 1, "records": 1}


def test_the_vowelled_reading_survives_replay_restart_and_resume(client):
    c, appmod, db = client
    _login(c, appmod)
    sid = _stamped_start(c, appmod, ENGINE_CONTRACT_VERSION_T2G2)
    _answer(c, sid, BACKREF_AR_DIACRITIZED)
    live = _snapshot(appmod, sid)
    assert _active_answers(appmod, sid)[0].content == BACKREF_AR_DIACRITIZED
    appmod.SESSION_STORE.clear()
    session = reconstruct_readonly_state(appmod._get_store(), sid)
    assert appmod._resolve_question_context(session.state, None).identity == \
        live["identity"]
    _raw(c, sid)
    assert c.post(f"/session/{sid}/resume", data={}).status_code == 302
    assert _snapshot(appmod, sid) == live
    assert _stamp(db, sid) == ENGINE_CONTRACT_VERSION_T2G2
