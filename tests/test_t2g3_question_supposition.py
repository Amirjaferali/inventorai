"""T2-G-3 — a mechanism written only as a question or a supposition is not
credited (false-progression correction).

Two rules, under the T2-G-3 engine-contract version ONLY:
  1. a whole sentence that ends in "?" / "؟" or opens with "suppose",
     "imagine" or "لنفترض" is never a mechanism carrier;
  2. with or without an explicit "I don't know", an answer whose every
     mechanism-relevant sentence is such a sentence supplies no mechanism and
     gets its own WARN reason and EN / AR feedback.

Every fixture is synthetic; no real-user record is used. Assertions read the
canonical state and the full served-question identity, never a phrase alone.
"""
import pytest

from engine import answer_stance as st
from engine.idea_state import MECHANISM_COMPLETENESS as MC
from engine.intent_serving import matches_committed_intent as MATCH
from engine.session_reconstruction import (
    ENGINE_CONTRACT_VERSION_NR1, ENGINE_CONTRACT_VERSION_T2G1,
    ENGINE_CONTRACT_VERSION_T2G2, ENGINE_CONTRACT_VERSION_T2G3,
    RECONSTRUCTION_VERSION, ROUTING_AWARE_ENGINE_CONTRACT_VERSIONS,
    SUPPORTED_ENGINE_CONTRACT_VERSIONS, reconstruct_readonly_state)
from engine import need_routing as nr
from web import ui_text
from tests.test_t2g_versioned_journey import (  # noqa: F401 — fixture reuse
    client, _login, _start, _stamped_start, _answer, _snapshot, _stamp, _page,
    _raw, _correct, _active_answers, EE_SEED, F1_AFFIRM, F3_NEGATIVE,
    F4_MIXED, G1_AFFIRM, G4_MIXED, Q2, Q3, UNKNOWN_NOTICE,
    NOT_ADDRESSED_NOTICE)

PRIOR_VERSIONS = (RECONSTRUCTION_VERSION, ENGINE_CONTRACT_VERSION_T2G1,
                  ENGINE_CONTRACT_VERSION_T2G2, ENGINE_CONTRACT_VERSION_NR1)

BODY = ("the load path run from the deck panel into the hinge line, and does "
        "the spring latch transfer force into the frame rail")
SUPPOSED = ("the load path runs from the deck panel into the hinge line and "
            "the spring latch transfers force into the frame rail.")
AR_BODY = ("مسار الحمل ينتقل من لوح السطح إلى خط المفصلة ثم ينقل المزلاج "
           "النابضي القوة إلى قضيب الإطار")
UNK_EN = "I do not know how it works yet. "
UNK_AR = "لا أعرف كيف يعمل بعد. "

# C8 — interrogative; C9 — explicitly hypothetical.
C8_EN = "Does " + BODY + "?"
C8_AR = "هل " + AR_BODY + "؟"
C9_EN = "Suppose " + SUPPOSED
C9_EN_IMAGINE = "Imagine " + SUPPOSED
C9_AR = "لنفترض أن " + AR_BODY + "."

WITHHELD_NO_UNKNOWN = [C8_EN, C8_AR, C9_EN, C9_EN_IMAGINE, C9_AR,
                       "Suppose, for now, " + SUPPOSED,
                       C8_EN + " " + C9_EN]
WITHHELD_WITH_UNKNOWN = [UNK_EN + C8_EN, UNK_EN + C9_EN, UNK_AR + C8_AR,
                         UNK_AR + C9_AR]

IF_EN = ("If the ramp is loaded, the load path runs from the deck panel into "
         "the hinge line and the spring latch transfers force into the frame "
         "rail.")
IF_AR = "إذا حُمّل المنحدر، " + AR_BODY + "."
LAW_AR = "لو حُمّل المنحدر، " + AR_BODY + "."
WHEN_EN = ("When the ramp is wet, the load path still runs from the deck panel "
           "into the hinge line and the spring latch transfers force into the "
           "frame rail.")
SUPPOSEDLY_EN = "Supposedly " + SUPPOSED
PRESERVED = [F1_AFFIRM, G1_AFFIRM, F3_NEGATIVE, F4_MIXED, G4_MIXED, IF_EN,
             IF_AR, LAW_AR, WHEN_EN, SUPPOSEDLY_EN,
             C8_EN + " " + F1_AFFIRM, F1_AFFIRM + " Is that enough?",
             C9_EN + " " + F1_AFFIRM, C8_AR + " " + G1_AFFIRM]

NEW_REASON = "recorded as a question or supposition"
NEW_NOTICE_EN = ("It asks about or supposes how the mechanism might work but "
                 "does not state how it works")
NEW_NOTICE_AR = "وهي تسأل عن كيفية عمل الآلية أو تفترضها"

MECH_IDS = tuple("mechanical:MECHANISM_COMPLETENESS:Q%d" % n for n in (1, 2, 3, 4))


class _State:
    def __init__(self, version=ENGINE_CONTRACT_VERSION_T2G3, domain="mechanical"):
        self.engine_contract_version = version
        self.domain = domain
        self.iteration = 0


def _reason(appmod, sid):
    return (appmod.SESSION_STORE[sid].get("last_result") or {}).get("reason") or ""


# ==========================================================================
# 1. Versioning and the qualified vocabulary
# ==========================================================================
def test_one_new_version_is_added_and_every_earlier_one_is_kept():
    assert ENGINE_CONTRACT_VERSION_T2G3 == "p4-2-level1-recon-v1-t2g2-nr1-t2g3"
    assert SUPPORTED_ENGINE_CONTRACT_VERSIONS == PRIOR_VERSIONS + (
        ENGINE_CONTRACT_VERSION_T2G3,)
    # routing materialization is carried, not replaced
    assert ROUTING_AWARE_ENGINE_CONTRACT_VERSIONS == (
        ENGINE_CONTRACT_VERSION_NR1, ENGINE_CONTRACT_VERSION_T2G3)


def test_the_rule_level_is_three_only_for_the_new_version():
    assert st.t2g_rule_level(_State(), MC) == 3
    expected = {RECONSTRUCTION_VERSION: 0, ENGINE_CONTRACT_VERSION_T2G1: 1,
                ENGINE_CONTRACT_VERSION_T2G2: 2, ENGINE_CONTRACT_VERSION_NR1: 2}
    for version, level in expected.items():
        assert st.t2g_rule_level(_State(version), MC) == level
    assert st.t2g_rule_level(_State(domain="software"), MC) == 0
    assert st.t2g_rule_level(_State(), "PHYSICAL_FEASIBILITY") == 0


def test_the_supposition_openers_are_exactly_the_qualified_three():
    assert st._T2G3_SUPPOSITION_OPENERS == ("suppose", "imagine", "لنفترض")
    for cue in ("if", "إذا", "اذا", "لو"):
        assert cue not in st._T2G3_SUPPOSITION_OPENERS


@pytest.mark.parametrize("segment,expected", [
    ("Suppose the latch holds", True), ("IMAGINE the latch holds", True),
    ("Suppose, the latch holds", True), ("  imagine: the latch holds", True),
    ("لنفترض أن المزلاج يثبت", True), ("لنفترضْ أن المزلاج يثبت", True),
    ("Supposedly the latch holds", False), ("Imagined loads act", False),
    ("The latch, suppose, holds", False), ("If the latch holds", False),
    ("إذا ثبت المزلاج", False), ("لو ثبت المزلاج", False),
    ("Let us suppose the latch holds", False),
])
def test_a_cue_counts_only_as_a_whole_word_opening_the_sentence(segment, expected):
    assert st._t2g3_opens_supposition(segment) is expected


def test_an_unpunctuated_question_is_not_recognised():
    """Disclosed bound: only the ? / ؟ terminator marks a question."""
    assert not st._t2g3_is_non_assertive("Does the latch transfer force", "")
    assert not st._t2g3_is_non_assertive("Does the latch transfer force", ".")
    assert st._t2g3_is_non_assertive("Does the latch transfer force", "?")
    assert st._t2g3_is_non_assertive("هل ينقل المزلاج القوة", "؟")


# ==========================================================================
# 2. Rule 1 — the whole-sentence carrier refusal, at level 3 only
# ==========================================================================
@pytest.mark.parametrize("text", [C8_EN, C9_EN, C9_EN_IMAGINE, C8_AR, C9_AR])
def test_a_question_or_supposition_is_no_carrier_at_level_three_only(text):
    carried = {level: any(st.qualifying_carrier(text, q, MATCH, rule_level=level)
                          for q in MECH_IDS) for level in (1, 2, 3)}
    assert carried[1] and carried[2]            # the accepted earlier reading
    assert not carried[3]


@pytest.mark.parametrize("text", PRESERVED)
def test_a_stated_explanation_keeps_its_carrier_at_level_three(text):
    for q in MECH_IDS:
        assert st.qualifying_carrier(text, q, MATCH, rule_level=3) == \
            st.qualifying_carrier(text, q, MATCH, rule_level=2)


def test_level_three_never_admits_what_level_two_refuses(monkeypatch):
    monkeypatch.setattr(st, "_t2g2_quote_spans",
                        lambda _text: (_ for _ in ()).throw(RuntimeError()))
    # unreadable quotation scan: the clause path stays off, the refusal holds
    assert not any(st.qualifying_carrier(C8_EN, q, MATCH, rule_level=3)
                   for q in MECH_IDS)


# ==========================================================================
# 3. Rule 2 — the non-assertive veto
# ==========================================================================
def _relevant(sentence):
    from engine.gap_relevance import addresses_gap
    return addresses_gap(sentence, MC) or any(MATCH(sentence, q) for q in MECH_IDS)


@pytest.mark.parametrize("text", WITHHELD_NO_UNKNOWN)
def test_every_relevant_sentence_non_assertive_vetoes_at_level_three(text):
    assert st.non_assertive_without_mechanism(_State(), MC, text, _relevant)
    for version in PRIOR_VERSIONS:
        assert not st.non_assertive_without_mechanism(
            _State(version), MC, text, _relevant)


@pytest.mark.parametrize("text", PRESERVED)
def test_one_stated_relevant_sentence_keeps_the_answer(text):
    assert not st.non_assertive_without_mechanism(_State(), MC, text, _relevant)


def test_the_veto_needs_a_relevant_sentence_and_stays_in_scope():
    assert not st.non_assertive_without_mechanism(
        _State(), MC, "Is it raining today?", _relevant)
    assert not st.non_assertive_without_mechanism(
        _State(), "PHYSICAL_FEASIBILITY", C8_EN, _relevant)
    assert not st.non_assertive_without_mechanism(
        _State(domain="software"), MC, C8_EN, _relevant)


# ==========================================================================
# 4. Route level — the real /start stamps the new version
# ==========================================================================
def test_a_real_start_records_the_new_version_and_its_routing(client):
    c, appmod, db = client
    _login(c, appmod)
    sid = _start(c)
    assert _stamp(db, sid) == ENGINE_CONTRACT_VERSION_T2G3
    assert _snapshot(appmod, sid)["version"] == ENGINE_CONTRACT_VERSION_T2G3
    assert nr.is_routing_aware(ENGINE_CONTRACT_VERSION_T2G3)
    rows = appmod._get_store().load_need_routing(sid)
    assert [(r.gap_type, r.operation, r.required_input) for r in rows] == [
        ("PHYSICAL_FEASIBILITY", "ROUTE", "SPECIALIST")]


@pytest.mark.parametrize("answer", WITHHELD_NO_UNKNOWN)
def test_c8_c9_without_an_unknown_supply_no_mechanism(client, answer):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _start(c)
    _answer(c, sid, answer)
    got = _snapshot(appmod, sid)
    assert got["identity"] == Q2                     # the question stands
    assert got["status"] == "OPEN"
    assert got["known_mechanism"] is None
    assert got["known_problem"] is None
    assert got["coverage"] == []                     # W2-C agrees
    assert got["unknowns"] == 0
    assert got["records"] == 1                       # the answer is saved
    assert _active_answers(appmod, sid)[0].content == answer
    assert NEW_REASON in _reason(appmod, sid)


@pytest.mark.parametrize("answer", WITHHELD_WITH_UNKNOWN)
def test_c8_c9_with_an_unknown_keep_the_unknown_and_supply_no_mechanism(
        client, answer):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _start(c)
    _answer(c, sid, answer)
    got = _snapshot(appmod, sid)
    assert got["identity"] == Q2
    assert got["status"] == "OPEN"
    assert got["known_mechanism"] is None
    assert got["coverage"] == []
    assert got["unknowns"] == 1                      # captured exactly once
    assert _active_answers(appmod, sid)[0].content == answer
    # the existing explicit-unknown reason stays the truthful one here
    assert "recorded as an explicit unknown" in _reason(appmod, sid)
    assert UNKNOWN_NOTICE in _page(c, sid)


@pytest.mark.parametrize("answer", PRESERVED)
def test_stated_explanations_conditions_negation_and_mixed_answers_still_progress(
        client, answer):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _start(c)
    _answer(c, sid, answer)
    got = _snapshot(appmod, sid)
    assert got["status"] == "PARTIAL"
    assert got["known_mechanism"] == "REASONED"
    assert got["identity"] == Q3
    assert got["coverage"] == ["mechanical:MECHANISM_COMPLETENESS:Q2"]
    assert NEW_REASON not in _reason(appmod, sid)
    assert NEW_NOTICE_EN not in _page(c, sid)


@pytest.mark.parametrize("version", PRIOR_VERSIONS)
@pytest.mark.parametrize("answer", WITHHELD_NO_UNKNOWN + WITHHELD_WITH_UNKNOWN)
def test_every_earlier_version_keeps_its_own_reading(client, version, answer):
    """The accepted earlier reading is unchanged: no earlier project is
    reinterpreted by the new rule."""
    c, appmod, db = client
    _login(c, appmod)
    sid = _stamped_start(c, appmod, version)
    _answer(c, sid, answer)
    got = _snapshot(appmod, sid)
    assert got["status"] == "PARTIAL"
    assert got["known_mechanism"] in ("REASONED", "ASSERTED")
    assert NEW_REASON not in _reason(appmod, sid)
    assert _stamp(db, sid) == version


def test_the_electronics_journey_applies_the_same_rule(client):
    c, appmod, _db = client
    _login(c, appmod)
    question = ("Does the sensor read the current, and does the main part, the "
                "switch, then cut the power when the current gets too high?")
    sid = _start(c, EE_SEED, "electronics_electrical")
    _answer(c, sid, question)
    got = _snapshot(appmod, sid)
    assert got["known_mechanism"] is None and got["status"] == "OPEN"
    legacy = _stamped_start(c, appmod, ENGINE_CONTRACT_VERSION_NR1, EE_SEED,
                            "electronics_electrical")
    _answer(c, legacy, question)
    assert _snapshot(appmod, legacy)["known_mechanism"] is not None


# ==========================================================================
# 5. Feedback, disclosure and RTL
# ==========================================================================
def test_the_new_feedback_is_shown_only_when_the_rule_withholds(client):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _start(c)
    _answer(c, sid, C8_EN)
    english = _page(c, sid)
    assert NEW_NOTICE_EN in english
    assert NOT_ADDRESSED_NOTICE not in english
    assert UNKNOWN_NOTICE not in english
    lowered = english.lower()
    for overclaim in ("verified", "validated", "incorrect", "wrong"):
        assert overclaim not in lowered.split("saved with your project")[1][:300]
    arabic_raw = _raw(c, sid, "ar")
    assert NEW_NOTICE_AR in _page(c, sid, "ar")
    assert NEW_NOTICE_EN not in _page(c, sid, "ar")
    assert 'dir="rtl"' in arabic_raw and 'lang="ar"' in arabic_raw


def test_the_feedback_mapping_is_exact_in_both_languages():
    from web.result_feedback import get_result_feedback
    reason = ("MECHANISM_COMPLETENESS recorded as a question or supposition — "
              "this answer asks about or supposes the mechanism and does not "
              "state how it works")
    english = get_result_feedback({"transition": "WARN", "reason": reason})
    assert english == (
        "Your answer has been saved with your project. It asks about or "
        "supposes how the mechanism might work but does not state how it "
        "works, so this point has not moved forward. If you know how it works, "
        "describe it as a statement; if you do not know yet, you can say so.")
    assert ui_text.localize_deep(english, "ar") == (
        "تم حفظ إجابتك مع مشروعك. وهي تسأل عن كيفية عمل الآلية أو تفترضها، "
        "لكنها لا تذكر كيف تعمل، لذلك لم تتقدّم هذه النقطة. إذا كنت تعرف كيف "
        "تعمل، فصِفها كعبارة تقريرية؛ وإن كنت لا تعرف بعد، يمكنك قول ذلك.")


def test_the_new_disclosure_follows_the_projects_own_version(client):
    c, appmod, _db = client
    _login(c, appmod)
    new = _start(c)
    prior = _stamped_start(c, appmod, ENGINE_CONTRACT_VERSION_NR1)
    t3_en = ui_text.text("UI_T2G3_QUESTION_SET", "en")
    t3_ar = ui_text.text("UI_T2G3_QUESTION_SET", "ar")
    t2_en = ui_text.text("UI_T2G2_QUESTION_SET", "en")
    assert t3_en in _page(c, new) and t2_en not in _page(c, new)
    assert t3_ar in _page(c, new, "ar")
    assert t2_en in _page(c, prior) and t3_en not in _page(c, prior)
    lowered = t3_en.lower()
    assert "written only as a question" in lowered
    assert "covers only certain phrasings" in lowered
    assert "does not understand your writing in general" in lowered
    assert "engineering-correct is not checked" in lowered


# ==========================================================================
# 6. Corrections and live / cold / resumed parity
# ==========================================================================
def test_a_correction_recomputes_in_both_directions(client):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _start(c)
    _answer(c, sid, C9_EN)
    assert _snapshot(appmod, sid)["known_mechanism"] is None
    record = _active_answers(appmod, sid)[0]
    assert _correct(c, sid, record.record_id, F1_AFFIRM).status_code in (302, 303)
    got = _snapshot(appmod, sid)
    assert got["known_mechanism"] == "REASONED" and got["identity"] == Q3

    other = _start(c)
    _answer(c, other, F1_AFFIRM)
    record = _active_answers(appmod, other)[0]
    assert _correct(c, other, record.record_id, C8_AR).status_code in (302, 303)
    got = _snapshot(appmod, other)
    assert got["known_mechanism"] is None
    assert got["status"] == "OPEN" and got["identity"] == Q2
    assert got["coverage"] == []
    appmod.SESSION_STORE.clear()
    session = reconstruct_readonly_state(appmod._get_store(), other)
    assert session.state.known_mechanism is None
    assert session.review.withdrawn_source_records == 1


@pytest.mark.parametrize("answer", [C8_EN, C9_AR, UNK_EN + C8_EN, F1_AFFIRM])
def test_live_cold_and_resumed_agree(client, answer):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _start(c)
    _answer(c, sid, answer)
    live = _snapshot(appmod, sid)
    appmod.SESSION_STORE.clear()
    session = reconstruct_readonly_state(appmod._get_store(), sid)
    assert session.review.level == 1
    assert session.state.engine_contract_version == ENGINE_CONTRACT_VERSION_T2G3
    assert appmod._resolve_question_context(session.state, None).identity == \
        live["identity"]
    assert (session.state.known_mechanism is None) == \
        (live["known_mechanism"] is None)
    _raw(c, sid)
    assert c.post(f"/session/{sid}/resume", data={}).status_code == 302
    assert _snapshot(appmod, sid) == live


@pytest.mark.parametrize("version", PRIOR_VERSIONS)
def test_an_earlier_project_replays_its_question_answer_unchanged(client, version):
    c, appmod, db = client
    _login(c, appmod)
    sid = _stamped_start(c, appmod, version)
    _answer(c, sid, C8_EN)
    live = _snapshot(appmod, sid)
    appmod.SESSION_STORE.clear()
    session = reconstruct_readonly_state(appmod._get_store(), sid)
    assert session.state.engine_contract_version == version
    assert session.state.known_mechanism is not None
    _raw(c, sid)
    assert c.post(f"/session/{sid}/resume", data={}).status_code == 302
    assert _snapshot(appmod, sid) == live
    assert _stamp(db, sid) == version
