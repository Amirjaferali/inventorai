"""T2-G-5 — a word-for-word repeat of a Mechanism Completeness answer that
already moved the gap earns no further credit (engine-contract version T2G5
only).

The defect (synthetic trace, both active domains): an answer moved Mechanism
Completeness OPEN -> PARTIAL; the byte-identical answer, submitted to the next
question, moved it PARTIAL -> CLOSED ("closed after REASONED follow-up") and
replaced the recorded mechanism with itself. These tests prove, on synthetic
inputs only:

* the repeat is saved verbatim but moves no gap, mechanism, problem or maturity,
  while the question counter moves exactly as for every other WARN;
* identity is NFC + whitespace only: case ("5 mW" vs "5 MW"), digits,
  diacritics and symbols are kept, so a changed unit or diacritic is new text;
* only an answer that actually changed the gap's status is remembered: a
  rejected answer, an answer left unapplied by gap-bound replay and a
  superseded answer never produce a repeat match, and the same wording under
  another gap is assessed normally;
* live, cold reconstruction, resume and corrections (both ways) agree;
* all seven earlier versions keep their exact behaviour (the repeat still
  closes there) and never gain the derived record.

It does NOT solve R2 (plain-language under-crediting) or any paraphrase case.
"""
import unicodedata

import pytest

from engine import need_routing as nr
from engine import progression_loop as pl
from engine import answer_stance as st
from engine.idea_state import (IdeaState, MECHANISM_COMPLETENESS as MC,
                               PHYSICAL_FEASIBILITY as PF)
from engine.session_reconstruction import (
    CURRENT_ENGINE_CONTRACT_VERSION, ENGINE_CONTRACT_VERSION_T2G4,
    ENGINE_CONTRACT_VERSION_T2G5, GAP_BOUND_REPLAY_VERSIONS,
    ROUTING_AWARE_ENGINE_CONTRACT_VERSIONS, SUPPORTED_ENGINE_CONTRACT_VERSIONS,
    reconstruct_readonly_state)
from web import result_feedback, ui_text
from tests.test_t2g_versioned_journey import (  # noqa: F401 — fixture reuse
    client, _login, _start, _answer, _page, _snapshot, _stamp,
    _correct, _active_answers)

T2G5 = ENGINE_CONTRACT_VERSION_T2G5
EARLIER_VERSIONS = SUPPORTED_ENGINE_CONTRACT_VERSIONS[:-1]
EE = "electronics_electrical"
MECH = "mechanical"
ATTR = pl.STATUS_MOVING_ANSWERS_ATTR
REPEAT_REASON = "recorded as a repeat"

PLANT = ("I want a pot that waters my plants by itself when the soil gets dry, "
         "because I always forget to water them.")
PLANT_A = ("The sensor tells a small controller board when the soil is dry, the "
           "board switches the pump on for a few seconds, then switches it off.")
PLANT_B = PLANT_A + (" A float switch in the tank stops the pump when the tank "
                     "is empty.")
PLANT_UNIT = ("The sensor tells the controller when the soil is dry, and the "
              "controller switches the 5 mW pump on for a few seconds, then "
              "switches it off.")
PLANT_REJECTED = ("A small sensor in the soil checks how wet it is, and when it "
                  "is dry a little pump pushes water from a tank through a tube "
                  "into the pot.")

RAMP = ("A folding mechanical wheelchair ramp with a spring latch. The "
        "inventor wants the ramp to stay reliably locked in the flat, "
        "load-bearing position and to fold away without tools")
RAMP_A = ("The load path runs from the deck panel into the hinge line and the "
          "spring latch transfers force into the frame rail, so the ramp stays "
          "locked flat.")
RAMP_B = ("When the ramp is laid flat the spring pushes the latch pin into a "
          "hole in the frame rail, and the pin then carries the deck load "
          "across the hinge line until the handle pulls it back.")

BIKE = ("A small gadget for my bike that switches its light on by itself when "
        "it gets dark, and makes it flash when I slow down.")
BIKE_AR = ("حساس صغير على العجلة يقيس سرعة دورانها، وعندما تبطئ الدورات تجعل "
           "الدائرة الضوء يومض.")

JOURNEYS = {EE: (PLANT, PLANT_A, PLANT_B), MECH: (RAMP, RAMP_A, RAMP_B)}

NOTICE_EN = ("It is word for word the same as an earlier answer that was "
             "already counted for this point")
NOTICE_AR = "وهي مطابقة حرفيًا لإجابة سابقة احتُسبت بالفعل لهذه النقطة"


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def _engine(domain, seed, version=T2G5):
    """An in-memory project exactly as /start builds it (routing included)."""
    state = IdeaState(idea_id="t2g5")
    state.domain = domain
    state.domain_signal = domain
    state.path = "N"
    state.engine_contract_version = version
    if version in ROUTING_AWARE_ENGINE_CONTRACT_VERSIONS:
        for revision in nr.creation_revisions("p-t2g5", domain, "N", version):
            nr.apply_revision(state, revision)
    pl.run_iteration(state, seed)
    return state


def _mc(state):
    gap = state.get_gap(MC)
    return None if gap is None else gap.status


def _keys(state):
    return (getattr(state, ATTR, None) or {}).get(MC, ())


def _created(c, appmod, version, seed, domain):
    """A project genuinely CREATED under ``version`` (only the creation
    constant changes); an ordinary idea names its discipline as the inventor
    chooses it on the real start page."""
    original = appmod.CURRENT_ENGINE_CONTRACT_VERSION
    appmod.CURRENT_ENGINE_CONTRACT_VERSION = version
    try:
        return _start(c, seed, domain, {"domain_choice": domain})
    finally:
        appmod.CURRENT_ENGINE_CONTRACT_VERSION = original


def _project(c, appmod, domain, answers, version=T2G5):
    sid = _created(c, appmod, version, JOURNEYS[domain][0], domain)
    for text in answers:
        assert _answer(c, sid, text).status_code == 302
    return sid


def _live(appmod, sid):
    return appmod.SESSION_STORE[sid]["state"]


def _reason(appmod, sid):
    return (appmod.SESSION_STORE[sid].get("last_result") or {}).get("reason") or ""


def _view(state):
    km = state.known_mechanism
    return ([(g.gap_type, g.status, g.iterations_open) for g in state.gaps],
            state.maturity_level,
            None if km is None else (km.content, km.quality, km.iteration),
            _keys(state))


def _cold(appmod, sid):
    appmod.SESSION_STORE.clear()
    session = reconstruct_readonly_state(appmod._get_store(), sid)
    assert session.review.level == 1
    return session.state


# ==========================================================================
# 1. Version policy
# ==========================================================================
def test_exactly_one_eighth_version_is_added_and_stamped():
    assert T2G5 == "p4-2-level1-recon-v1-t2g2-nr1-t2g3-xg1-t2g4-t2g5"
    assert SUPPORTED_ENGINE_CONTRACT_VERSIONS[-2:] == (
        ENGINE_CONTRACT_VERSION_T2G4, T2G5)
    assert len(SUPPORTED_ENGINE_CONTRACT_VERSIONS) == 8
    assert CURRENT_ENGINE_CONTRACT_VERSION == T2G5
    assert GAP_BOUND_REPLAY_VERSIONS[-1] == T2G5
    assert ROUTING_AWARE_ENGINE_CONTRACT_VERSIONS[-1] == T2G5
    assert nr.is_routing_aware(T2G5)


class _State:
    def __init__(self, version, domain=MECH):
        self.engine_contract_version = version
        self.domain = domain


def test_rule_level_five_only_for_the_new_version_and_scope():
    assert st.t2g_rule_level(_State(T2G5), MC) == 5
    for version in EARLIER_VERSIONS:
        assert st.t2g_rule_level(_State(version), MC) < 5
    assert st.t2g_rule_level(_State(T2G5), PF) == 0
    assert st.t2g_rule_level(_State(T2G5, domain="software"), MC) == 0
    # outside the scope nothing is remembered or matched
    state = _State(T2G5)
    pl.record_status_moving_answer(state, PF, RAMP_A)
    assert not hasattr(state, ATTR)
    assert pl.repeats_status_moving_answer(state, PF, RAMP_A) is False


# ==========================================================================
# 2. Conservative identity
# ==========================================================================
def test_identity_is_nfc_and_whitespace_only():
    key = pl.answer_identity_key
    assert key("  a  b\tc\n d e ") == "a b c d e"
    assert key(unicodedata.normalize("NFD", "café ئ")) == key("café ئ")
    assert key("5 mW pump") != key("5 MW pump")                 # case kept
    assert key("Rθ = 2 K/W") != key("Rθ = 3 K/W")              # digits kept
    assert key("حساس") != key("حَسّاس")                         # diacritics kept
    assert key("حساس") != key("حســاس")                         # tatweel kept
    assert key("It does not lock.") != key("It does lock.")     # negation kept
    assert key("pin A-12") != key("pin A12")                    # symbols kept
    assert key(None) == ""


# ==========================================================================
# 3. The engine rule, both active domains
# ==========================================================================
@pytest.mark.parametrize("domain", (EE, MECH))
def test_an_exact_repeat_moves_nothing_but_the_question_counter(domain):
    seed, first, _second = JOURNEYS[domain]
    state = _engine(domain, seed)
    pl.run_iteration(state, first)
    assert _mc(state) == "PARTIAL"
    mechanism = state.known_mechanism
    problem = state.known_problem
    maturity = state.maturity_level
    counter = state.get_gap(MC).iterations_open
    result = pl.run_iteration(state, first)
    assert REPEAT_REASON in result["reason"]
    assert _mc(state) == "PARTIAL"
    assert state.known_mechanism is mechanism        # not replaced by the repeat
    assert state.known_problem is problem
    assert state.maturity_level == maturity
    assert state.get_gap(MC).iterations_open == counter + 1   # unchanged semantics
    assert _keys(state) == (pl.answer_identity_key(first),)


@pytest.mark.parametrize("domain", (EE, MECH))
def test_a_new_follow_up_still_closes(domain):
    seed, first, second = JOURNEYS[domain]
    state = _engine(domain, seed)
    for text in (first, first, second):
        pl.run_iteration(state, text)
    assert _mc(state) == "CLOSED"
    assert state.known_mechanism.content == second


def test_an_earlier_answer_plus_new_material_is_new():
    state = _engine(EE, PLANT)
    pl.run_iteration(state, PLANT_A)
    result = pl.run_iteration(state, PLANT_B)
    assert REPEAT_REASON not in result["reason"]
    assert _mc(state) == "CLOSED"


def test_whitespace_only_differences_are_still_a_repeat():
    state = _engine(EE, PLANT)
    pl.run_iteration(state, PLANT_UNIT)
    spaced = "  " + PLANT_UNIT.replace(" ", " \n ", 3) + "\t"
    assert REPEAT_REASON in pl.run_iteration(state, spaced)["reason"]
    assert _mc(state) == "PARTIAL"


def test_case_sensitive_units_are_different_answers():
    state = _engine(EE, PLANT)
    pl.run_iteration(state, PLANT_UNIT)
    result = pl.run_iteration(state, PLANT_UNIT.replace("5 mW", "5 MW"))
    assert REPEAT_REASON not in result["reason"]
    assert _mc(state) == "CLOSED"


def test_an_arabic_exact_repeat_and_its_nfd_form_earn_nothing():
    for repeat in (BIKE_AR, unicodedata.normalize("NFD", BIKE_AR)):
        state = _engine(EE, BIKE)
        pl.run_iteration(state, BIKE_AR)
        assert _mc(state) == "PARTIAL"
        assert REPEAT_REASON in pl.run_iteration(state, repeat)["reason"]
        assert _mc(state) == "PARTIAL"


def test_an_arabic_diacritic_change_is_new_text():
    state = _engine(EE, BIKE)
    pl.run_iteration(state, BIKE_AR)
    result = pl.run_iteration(state, BIKE_AR.replace("حساس", "حَسّاس"))
    assert REPEAT_REASON not in result["reason"]


def test_a_rejected_answer_is_never_remembered():
    state = _engine(EE, PLANT)
    for _ in range(2):
        result = pl.run_iteration(state, PLANT_REJECTED)
        assert "not addressed" in result["reason"]
        assert REPEAT_REASON not in result["reason"]
    assert _mc(state) == "OPEN" and not hasattr(state, ATTR)


def test_the_same_wording_under_another_gap_is_assessed_normally():
    state = _engine(MECH, RAMP)
    for text in (RAMP_A, RAMP_B):
        pl.run_iteration(state, text)
    assert _mc(state) == "CLOSED"
    assert pl.select_next_gap(state) == PF
    result = pl.run_iteration(state, RAMP_A)
    assert REPEAT_REASON not in result["reason"]
    assert set((getattr(state, ATTR, None) or {})) == {MC}


@pytest.mark.parametrize("domain", (EE, MECH))
@pytest.mark.parametrize("version", EARLIER_VERSIONS)
def test_every_earlier_version_keeps_its_exact_behaviour(version, domain):
    seed, first, _second = JOURNEYS[domain]
    state = _engine(domain, seed, version)
    pl.run_iteration(state, first)
    result = pl.run_iteration(state, first)
    assert REPEAT_REASON not in result["reason"]
    assert _mc(state) == "CLOSED"                      # the historical reading
    assert not hasattr(state, ATTR)


# ==========================================================================
# 4. Live, cold reconstruction and resume agree
# ==========================================================================
@pytest.mark.parametrize("domain", (EE, MECH))
def test_live_cold_and_resumed_agree(client, domain):
    c, appmod, db = client
    _login(c, appmod)
    _seed, first, second = JOURNEYS[domain]
    sid = _project(c, appmod, domain, [first, first])
    assert _stamp(db, sid) == T2G5
    assert REPEAT_REASON in _reason(appmod, sid)
    live = _view(_live(appmod, sid))
    assert live[0][0][:2] == (MC, "PARTIAL")
    snap = _snapshot(appmod, sid)
    assert [r.content for r in _active_answers(appmod, sid)] == [first, first]
    assert _view(_cold(appmod, sid)) == live          # the ledger is not read
    assert c.post(f"/session/{sid}/resume", data={}).status_code == 302
    assert _view(_live(appmod, sid)) == live
    assert _snapshot(appmod, sid)["identity"] == snap["identity"]
    # and the resumed project continues normally
    assert _answer(c, sid, second).status_code == 302
    assert _live(appmod, sid).get_gap(MC).status == "CLOSED"
    assert _view(_cold(appmod, sid))[0][0][:2] == (MC, "CLOSED")


@pytest.mark.parametrize("version", EARLIER_VERSIONS)
def test_earlier_versions_keep_their_reading_live_and_replayed(client, version):
    c, appmod, db = client
    _login(c, appmod)
    sid = _project(c, appmod, EE, [PLANT_A, PLANT_A], version=version)
    assert _stamp(db, sid) == version
    live = _view(_live(appmod, sid))
    assert live[0][0][:2] == (MC, "CLOSED") and live[3] == ()
    assert _view(_cold(appmod, sid)) == live
    assert c.post(f"/session/{sid}/resume", data={}).status_code == 302
    assert _view(_live(appmod, sid)) == live


# ==========================================================================
# 5. Corrections, both ways, and gap-bound unapplied answers
# ==========================================================================
@pytest.mark.parametrize("domain", (EE, MECH))
def test_a_superseded_answer_never_produces_a_repeat_match(client, domain):
    c, appmod, _db = client
    _login(c, appmod)
    _seed, first, second = JOURNEYS[domain]
    sid = _project(c, appmod, domain, [first, first])
    assert _live(appmod, sid).get_gap(MC).status == "PARTIAL"
    # correct the FIRST answer into something else: the second one is no
    # longer a repeat of anything that moved the gap, so it now closes it
    target = _active_answers(appmod, sid)[0]
    assert _correct(c, sid, target.record_id, second).status_code == 302
    live = _view(_live(appmod, sid))
    assert live[0][0][:2] == (MC, "CLOSED")
    assert pl.answer_identity_key(first) in live[3]
    assert _view(_cold(appmod, sid)) == live


@pytest.mark.parametrize("domain", (EE, MECH))
def test_correcting_into_and_out_of_a_repeat(client, domain):
    c, appmod, _db = client
    _login(c, appmod)
    _seed, first, second = JOURNEYS[domain]
    sid = _project(c, appmod, domain, [first, second])
    assert _live(appmod, sid).get_gap(MC).status == "CLOSED"
    # correct the follow-up INTO a repeat: the rebuilt history earns nothing
    target = _active_answers(appmod, sid)[1]
    assert _correct(c, sid, target.record_id, first).status_code == 302
    live = _view(_live(appmod, sid))
    assert live[0][0][:2] == (MC, "PARTIAL")
    assert live[2][0] == first
    assert _view(_cold(appmod, sid)) == live
    assert c.post(f"/session/{sid}/resume", data={}).status_code == 302
    assert _view(_live(appmod, sid)) == live
    # and correcting it back restores the closure
    target = _active_answers(appmod, sid)[1]
    assert target.content == first
    assert _correct(c, sid, target.record_id, second).status_code == 302
    live = _view(_live(appmod, sid))
    assert live[0][0][:2] == (MC, "CLOSED")
    assert _view(_cold(appmod, sid)) == live


def test_an_unapplied_gap_bound_answer_is_never_remembered(client):
    from tests.test_xg1_replay_attribution import (
        SEED as XSEED, MC1, MC1_CORRECTED, MC2, MC3)
    c, appmod, _db = client
    _login(c, appmod)
    sid = _created(c, appmod, T2G5, XSEED, EE)
    for text in (MC1, MC2, MC3):
        _answer(c, sid, text)
    target = [r for r in _active_answers(appmod, sid)
              if r.content == MC1][0]
    assert _correct(c, sid, target.record_id, MC1_CORRECTED).status_code == 302
    state = _live(appmod, sid)
    unapplied = getattr(state, "unapplied_answer_record_ids", ())
    assert unapplied, "the scenario must leave one answer unapplied"
    texts = {r.record_id: r.content for r in _active_answers(appmod, sid)}
    keys = _keys(state)
    for record_id in unapplied:
        assert pl.answer_identity_key(texts[record_id]) not in keys
    assert _view(_cold(appmod, sid)) == _view(state)


# ==========================================================================
# 6. Feedback and disclosure, EN / AR
# ==========================================================================
def test_the_feedback_is_truthful_in_both_languages(client):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _project(c, appmod, EE, [PLANT_A, PLANT_A])
    page_en = _page(c, sid)
    assert NOTICE_EN in page_en
    assert NOTICE_AR in _page(c, sid, "ar")
    message = result_feedback.get_result_feedback(
        {"transition": "WARN", "reason": _reason(appmod, sid)})
    assert message.startswith("Your answer has been saved with your project.")
    assert "same question" not in message           # the counter has moved
    assert "adds no new information" in message
    # both answers stay saved, verbatim
    assert [r.content for r in _active_answers(appmod, sid)] == [PLANT_A, PLANT_A]


def test_the_disclosure_follows_the_projects_own_version(client):
    c, appmod, _db = client
    _login(c, appmod)
    new = _project(c, appmod, EE, [])
    prior = _project(c, appmod, EE, [], version=ENGINE_CONTRACT_VERSION_T2G4)
    t5_en = ui_text.text("UI_T2G5_QUESTION_SET", "en")
    t5_ar = ui_text.text("UI_T2G5_QUESTION_SET", "ar")
    t4_en = ui_text.text("UI_T2G4_QUESTION_SET", "en")
    assert t5_en in _page(c, new) and t4_en not in _page(c, new)
    assert t5_ar in _page(c, new, "ar")
    assert t4_en in _page(c, prior) and t5_en not in _page(c, prior)
    assert "word for word the same as an earlier answer" in t5_en
    assert "engineering-correct is not checked" in t5_en
    assert "مطابقة حرفيًا" in t5_ar
