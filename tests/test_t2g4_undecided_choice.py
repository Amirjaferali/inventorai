"""T2-G-4 — an answer that only says how the mechanism is still undecided earns
no Mechanism Completeness credit (engine-contract version T2G4 only).

The defect (synthetic Q10 trace): "Flash in daylight too. I haven't chosen how
to sense slowing." was credited, because the only mechanism word ("sense") sits
in the sentence saying the mechanism is NOT decided, and "haven't chosen" is no
registered explicit-unknown phrasing. These tests prove, on synthetic inputs
only: the exact Q10 answer is saved verbatim and earns nothing; genuine
explanations beside a pending choice keep their credit; repeated pending-choice
answers manufacture no progress; live, correction, cold reconstruction and
resume agree; every earlier version keeps its own reading; English and Arabic
positive and negative controls behave as the bounded rule states.
"""
import html as _html

import pytest

from engine import answer_stance as st
from engine import need_routing as nr
from engine.idea_state import (MECHANISM_COMPLETENESS as MC,
                               PHYSICAL_FEASIBILITY as PF)
from engine.intent_serving import matches_committed_intent as MATCH
from engine.session_reconstruction import (
    CURRENT_ENGINE_CONTRACT_VERSION, ENGINE_CONTRACT_VERSION_NR1,
    ENGINE_CONTRACT_VERSION_T2G1, ENGINE_CONTRACT_VERSION_T2G2,
    ENGINE_CONTRACT_VERSION_T2G3, ENGINE_CONTRACT_VERSION_T2G4,
    ENGINE_CONTRACT_VERSION_T2G5,
    ENGINE_CONTRACT_VERSION_XG1, GAP_BOUND_REPLAY_VERSIONS,
    RECONSTRUCTION_VERSION, ROUTING_AWARE_ENGINE_CONTRACT_VERSIONS,
    SUPPORTED_ENGINE_CONTRACT_VERSIONS, reconstruct_readonly_state)
from web import ui_text
from tests.test_t2g_versioned_journey import (  # noqa: F401 — fixture reuse
    client, _login, _start, _answer, _page, _snapshot, _stamp,
    _correct, _active_answers)

T2G4 = ENGINE_CONTRACT_VERSION_T2G4
T2G5 = ENGINE_CONTRACT_VERSION_T2G5
PRIOR_VERSIONS = (RECONSTRUCTION_VERSION, ENGINE_CONTRACT_VERSION_T2G1,
                  ENGINE_CONTRACT_VERSION_T2G2, ENGINE_CONTRACT_VERSION_NR1,
                  ENGINE_CONTRACT_VERSION_T2G3, ENGINE_CONTRACT_VERSION_XG1)
EE = "electronics_electrical"
MECH = "mechanical"
DOMAINS = (EE, MECH)

BIKE = ("A small gadget for my bike that switches its light on by itself when "
        "it gets dark, and makes it flash when I slow down.")
Q10 = "Flash in daylight too. I haven't chosen how to sense slowing."
PENDING_ONLY = "I haven't chosen how to sense slowing."

NEW_REASON = "recorded as an undecided choice"
NOTICE_EN = ("The parts of it about how this works were read as saying that "
             "has not been decided or chosen yet")
NOTICE_AR = "وقد قُرئت أجزاؤها المتعلقة بطريقة العمل على أنها تذكر أن ذلك لم يُحسم"

# Pending-choice answers: every mechanism-relevant clause is a pending choice.
WITHHELD_EN = [
    Q10,
    "Flash in daylight too. I have not worked out how it will detect the bike "
    "slowing down.",
    "I haven't figured out how the sensor would notice braking.",
    "We haven't picked which sensor detects the slowing yet.",
    "I still need to decide how the gadget senses that I am slowing down.",
    "I have yet to choose how the light senses that I slow down.",
]
WITHHELD_AR = [
    "لم أختر بعد الحساس الذي يكشف التباطؤ.",
    "يومض في النهار أيضا. لم أخترها بعد، الحساس الذي يكشف التباطؤ.",
    "ما حددت للحين الحساس الذي يكشف التباطؤ.",
]
# Genuine explanations, some beside a pending choice: credit is kept.
CREDITED = [
    # a separate asserted sentence beside the pending choice
    "A light sensor notices when it gets dark and the circuit switches the "
    "lamp on. I haven't chosen how to sense slowing.",
    # the asserted clause after a contrast boundary in the same sentence
    "I haven't chosen how to sense slowing, but a light sensor notices when it "
    "gets dark and the circuit switches the lamp on.",
    # physical negation is not a pending choice
    "The light sensor does not need a battery of its own; it sends its reading "
    "to the controller which switches the LED on.",
    # an affirmative decision is not a pending choice
    "I chose a light sensor that sends its reading to the controller, which "
    "switches the LED on.",
    "حساس صغير على العجلة يقيس سرعة دورانها، وعندما تبطئ الدورات تجعل الدائرة "
    "الضوء يومض.",
    # review F1: a present-tense "I don't choose / pick X" describes automatic
    # operation, not an open choice
    "I don't choose the flash rate by hand because the controller sets it from "
    "the pulse interval measured by the reed switch on the wheel.",
    "I don't pick the threshold, the controller determines it from the light "
    "sensor reading and switches the LED on when it drops.",
    # "pick up" means sensing
    "We haven't picked up any vibration because the rubber damper absorbs it "
    "and the sensor sends a clean reading to the controller.",
    # review F5: a pending clause beside an unknown and an asserted clause
    "I don't know the exact sensor yet. I haven't chosen the battery, but the "
    "sensor would notice the problem and respond by switching the relay off "
    "which cuts the current.",
]


def _bike(c, appmod, domain=EE, version=None):
    """The ordinary bike idea matches no discipline on its own, so the inventor
    chooses one, exactly as on the real start page. ``version`` creates the
    project under that contract (only the creation constant is changed)."""
    extra = {"domain_choice": domain}
    if version is None:
        return _start(c, BIKE, domain, extra)
    original = appmod.CURRENT_ENGINE_CONTRACT_VERSION
    appmod.CURRENT_ENGINE_CONTRACT_VERSION = version
    try:
        return _start(c, BIKE, domain, extra)
    finally:
        appmod.CURRENT_ENGINE_CONTRACT_VERSION = original


def _reason(appmod, sid):
    return (appmod.SESSION_STORE[sid].get("last_result") or {}).get("reason") or ""


def _mc(appmod, sid):
    state = appmod.SESSION_STORE[sid]["state"]
    return state.get_gap(MC).status, state.known_mechanism


class _State:
    def __init__(self, version=T2G4, domain=MECH):
        self.engine_contract_version = version
        self.domain = domain
        self.iteration = 0


# ==========================================================================
# 1. Version policy
# ==========================================================================
def test_exactly_one_seventh_version_is_added_and_stamped():
    assert T2G4 == "p4-2-level1-recon-v1-t2g2-nr1-t2g3-xg1-t2g4"
    # T2-G-5 follows T2-G-4, carries every level-4 rule and is now stamped.
    assert SUPPORTED_ENGINE_CONTRACT_VERSIONS == PRIOR_VERSIONS + (T2G4, T2G5)
    assert CURRENT_ENGINE_CONTRACT_VERSION == T2G5
    # it carries XG1's gap-bound replay and the NR1 routing unchanged
    assert GAP_BOUND_REPLAY_VERSIONS == (ENGINE_CONTRACT_VERSION_XG1, T2G4,
                                         T2G5)
    assert ROUTING_AWARE_ENGINE_CONTRACT_VERSIONS[-2:] == (T2G4, T2G5)
    assert nr.is_routing_aware(T2G4)


def test_rule_level_four_only_for_the_new_version_and_scope():
    levels = {RECONSTRUCTION_VERSION: 0, ENGINE_CONTRACT_VERSION_T2G1: 1,
              ENGINE_CONTRACT_VERSION_T2G2: 2, ENGINE_CONTRACT_VERSION_NR1: 2,
              ENGINE_CONTRACT_VERSION_T2G3: 3, ENGINE_CONTRACT_VERSION_XG1: 3,
              T2G4: 4, T2G5: 5}
    for version, level in levels.items():
        assert st.t2g_rule_level(_State(version), MC) == level
    assert st.t2g_rule_level(_State(T2G4), PF) == 0
    assert st.t2g_rule_level(_State(T2G4, domain="software"), MC) == 0
    # below level 4 the new veto never fires, whatever the text
    for version in PRIOR_VERSIONS:
        assert st.undecided_without_mechanism(
            _State(version), MC, PENDING_ONLY, lambda s: True) is False


def test_the_disclosure_follows_the_projects_own_version(client):
    c, appmod, _db = client
    _login(c, appmod)
    # T2-G-5 projects carry their own description; the T2-G-4 one stays
    # exactly the description of a project recorded under T2-G-4.
    new = _bike(c, appmod, version=T2G4)
    prior = _bike(c, appmod, version=ENGINE_CONTRACT_VERSION_XG1)
    t4_en = ui_text.text("UI_T2G4_QUESTION_SET", "en")
    t4_ar = ui_text.text("UI_T2G4_QUESTION_SET", "ar")
    t3_en = ui_text.text("UI_T2G3_QUESTION_SET", "en")
    assert t4_en in _page(c, new) and t3_en not in _page(c, new)
    assert t4_ar in _page(c, new, "ar")
    assert t3_en in _page(c, prior) and t4_en not in _page(c, prior)
    assert "have not decided or chosen" in t4_en
    assert "covers only certain phrasings" in t4_en
    assert "engineering-correct is not checked" in t4_en
    assert "لم تقرر أو لم تختر" in t4_ar


# ==========================================================================
# 2. The bounded recogniser
# ==========================================================================
@pytest.mark.parametrize("clause", [
    "I haven't chosen how to sense slowing",
    "I have not yet decided which sensor",
    "I’ve not picked the sensor",
    "We still haven't selected a sensor",
    "I didn't yet decide how it notices braking",
    "I still don't decide how it notices braking",
    "I still need to work out how it senses slowing",
    "We have yet to figure out how the light flashes",
    "I'm still undecided about the sensor",
    "and I haven't settled on a sensor",
    "لم أختر بعد الحساس",
    "لم أقرّر بعد كيف",
    "أنا لم أحدد بعد",
    "ما قررت للحين",
    "وللحين ما اخترت شلون",
    "لم أخترها",
])
def test_a_pending_choice_opening_is_recognised(clause):
    assert st._t2g4_opens_undecided(clause) is True


@pytest.mark.parametrize("clause", [
    "I chose a wheel magnet",
    "I decided to use a light sensor",
    "We picked a hall sensor for the wheel",
    "The sensor I haven't chosen yet reads the wheel",   # not at the opening
    "I do not know how it senses slowing",               # an unknown, not a choice
    "Supposedly I haven't chosen",
    "ما اخترته هو حساس مغناطيسي",                         # "what I chose is …"
    "ما قررت هو أن الحساس يقرأ العجلة",
    "ما اخترت كان مفتاح ريد",                             # "what I chose was …"
    "I don't choose the flash rate by hand",             # automatic operation
    "We don't pick up vibration",
    "We haven't picked up any vibration",
    "لم أكن أعرف",
    "",
])
def test_affirmative_and_other_clauses_are_not_recognised(clause):
    assert st._t2g4_opens_undecided(clause) is False


def test_the_recogniser_fails_closed_and_never_rewrites_the_answer():
    assert st._t2g4_opens_undecided(None) is False
    text = "  I haven't chosen how to sense slowing  "
    st._t2g4_opens_undecided(text)
    assert text == "  I haven't chosen how to sense slowing  "

    def boom(_sentence):
        raise RuntimeError("relevance unavailable")
    assert st.undecided_without_mechanism(_State(), MC, PENDING_ONLY, boom) is False


def test_coverage_and_eligibility_read_the_pending_choice_alike():
    """A pending choice is never a qualifying carrier at level 4, so variant
    coverage cannot count what eligibility withholds; an asserted clause after a
    contrast boundary still carries."""
    q2 = "mechanical:MECHANISM_COMPLETENESS:Q2"
    pending = ("I haven't chosen how the load path runs from the deck panel "
               "into the hinge line and the frame rail.")
    assert st.qualifying_carrier(pending, q2, MATCH, rule_level=3) is True
    assert st.qualifying_carrier(pending, q2, MATCH, rule_level=4) is False
    mixed = ("I haven't chosen the colour, but the load path runs from the deck "
             "panel into the hinge line and the frame rail carries it.")
    assert st.qualifying_carrier(mixed, q2, MATCH, rule_level=4) is True
    # review F1: automatic operation keeps its coverage
    automatic = ("I don't choose the force path by hand, the lever transfers "
                 "force from the handle to the hinge pin.")
    assert st.qualifying_carrier(automatic, q2, MATCH, rule_level=3) is True
    assert st.qualifying_carrier(automatic, q2, MATCH, rule_level=4) is True
    # review F5: the level-1 reading of the clause beside a pending choice is
    # kept, so a served question is not re-opened by the new rule
    beside = ("I haven't chosen the battery, but the sensor would notice the "
              "problem and respond by switching the relay off which cuts the "
              "current.")
    assert st.qualifying_carrier(beside, "N-MC-1", MATCH, rule_level=3) is True
    assert st.qualifying_carrier(beside, "N-MC-1", MATCH, rule_level=4) is True


# ==========================================================================
# 3. The live journey
# ==========================================================================
@pytest.mark.parametrize("domain", DOMAINS)
def test_the_exact_q10_answer_is_saved_verbatim_and_earns_nothing(client, domain):
    c, appmod, db = client
    _login(c, appmod)
    sid = _bike(c, appmod, domain)
    assert _stamp(db, sid) == CURRENT_ENGINE_CONTRACT_VERSION   # level >= 4
    assert _answer(c, sid, Q10).status_code == 302
    status, mechanism = _mc(appmod, sid)
    assert status == "OPEN" and mechanism is None
    assert NEW_REASON in _reason(appmod, sid)
    records = _active_answers(appmod, sid)
    assert [r.content for r in records] == [Q10]
    assert records[0].provenance == "OWNER_STATED"
    assert records[0].validation_status == "UNVALIDATED"
    page = _page(c, sid)
    assert NOTICE_EN in page
    assert Q10 in page                     # still shown, verbatim
    assert NOTICE_AR in _page(c, sid, "ar")
    # the acknowledged-unknown track and its vocabularies are untouched
    assert appmod.SESSION_STORE[sid]["state"].acknowledged_unknowns == []


@pytest.mark.parametrize("answer", WITHHELD_EN + WITHHELD_AR)
def test_pending_choice_controls_earn_nothing(client, answer):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _bike(c, appmod)
    _answer(c, sid, answer)
    status, mechanism = _mc(appmod, sid)
    assert status == "OPEN" and mechanism is None
    assert NEW_REASON in _reason(appmod, sid)


@pytest.mark.parametrize("answer", CREDITED)
def test_genuine_explanations_keep_their_credit(client, answer):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _bike(c, appmod)
    _answer(c, sid, answer)
    status, mechanism = _mc(appmod, sid)
    assert status == "PARTIAL" and mechanism is not None
    assert mechanism.content == answer
    assert NEW_REASON not in _reason(appmod, sid)


def test_repeated_pending_choices_manufacture_no_progress(client):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _bike(c, appmod)
    for answer in (Q10, PENDING_ONLY, Q10, WITHHELD_EN[3], PENDING_ONLY):
        assert _answer(c, sid, answer).status_code == 302
        state = appmod.SESSION_STORE[sid]["state"]
        mc = state.get_gap(MC)
        assert mc is None or mc.status == "OPEN"
        assert state.known_mechanism is None
    assert len(_active_answers(appmod, sid)) == 5      # every answer is kept


# ==========================================================================
# 4. Live, correction, cold reconstruction and resume agree
# ==========================================================================
@pytest.mark.parametrize("answer", [Q10, CREDITED[0]])
def test_live_cold_and_resumed_agree(client, answer):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _bike(c, appmod)
    _answer(c, sid, answer)
    live = _snapshot(appmod, sid)
    appmod.SESSION_STORE.clear()
    session = reconstruct_readonly_state(appmod._get_store(), sid)
    assert session.review.level == 1
    assert session.state.engine_contract_version == \
        CURRENT_ENGINE_CONTRACT_VERSION
    assert (session.state.known_mechanism is None) == \
        (live["known_mechanism"] is None)
    assert appmod._resolve_question_context(session.state, None).identity == \
        live["identity"]
    assert c.post(f"/session/{sid}/resume", data={}).status_code == 302
    assert _snapshot(appmod, sid) == live


def test_a_correction_recomputes_under_the_new_version(client):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _bike(c, appmod)
    _answer(c, sid, CREDITED[0])
    assert _mc(appmod, sid)[0] == "PARTIAL"
    # correcting the explanation into a pending choice withdraws the credit
    target = _active_answers(appmod, sid)[0]
    assert _correct(c, sid, target.record_id, Q10).status_code == 302
    status, mechanism = _mc(appmod, sid)
    assert status == "OPEN" and mechanism is None
    # and correcting it back restores it
    target = _active_answers(appmod, sid)[0]
    assert target.content == Q10
    assert _correct(c, sid, target.record_id, CREDITED[0]).status_code == 302
    status, mechanism = _mc(appmod, sid)
    assert status == "PARTIAL" and mechanism.content == CREDITED[0]


# ==========================================================================
# 5. Every earlier version keeps its own reading, live and replayed
# ==========================================================================
@pytest.mark.parametrize("version", PRIOR_VERSIONS)
def test_every_earlier_version_keeps_its_own_reading(client, version):
    c, appmod, db = client
    _login(c, appmod)
    sid = _bike(c, appmod, version=version)
    _answer(c, sid, Q10)
    status, mechanism = _mc(appmod, sid)
    assert status == "PARTIAL" and mechanism is not None   # unchanged reading
    assert NEW_REASON not in _reason(appmod, sid)
    live = _snapshot(appmod, sid)
    appmod.SESSION_STORE.clear()
    session = reconstruct_readonly_state(appmod._get_store(), sid)
    assert session.state.engine_contract_version == version
    assert session.state.known_mechanism is not None
    assert c.post(f"/session/{sid}/resume", data={}).status_code == 302
    assert _snapshot(appmod, sid) == live
    assert _stamp(db, sid) == version


@pytest.mark.parametrize("answer", WITHHELD_EN + WITHHELD_AR)
def test_each_pending_choice_control_was_credited_before_this_version(client, answer):
    """The negative controls exercise the defect: under XG1 (the previous
    stamp) each of them earned Mechanism Completeness credit."""
    c, appmod, _db = client
    _login(c, appmod)
    sid = _bike(c, appmod, version=ENGINE_CONTRACT_VERSION_XG1)
    _answer(c, sid, answer)
    status, mechanism = _mc(appmod, sid)
    assert status == "PARTIAL" and mechanism is not None
