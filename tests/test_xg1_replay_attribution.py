"""Cross-gap replay attribution repair (engine-contract version XG1).

Under XG1 ONLY, a replayed active gap-bound answer enters ``run_iteration``
only when its own durable ``gap_context`` is the gap ``select_next_gap`` chooses
at that answer's replay position (after ``prepare_answer`` and routing).
Otherwise it stays saved, verbatim and in the ledger, is reported in
``unapplied_answer_record_ids`` and earns no iteration, gap, transition or
maturity credit. Every earlier version replays exactly as before.

Every fixture is synthetic; no real-user record is used.
"""
import html as _html

import pytest

import engine.session_reconstruction as sr
from engine import progression_loop as pl
from engine.idea_state import (
    ACCEPTED_RISK, CLOSED, OPEN, PARTIAL, Gap, IdeaState,
    MECHANISM_COMPLETENESS as MC, PHYSICAL_FEASIBILITY as PF,
    BOUNDARY_AMBIGUITY as BA)
from engine.session_reconstruction import (
    ENGINE_CONTRACT_VERSION_NR1, ENGINE_CONTRACT_VERSION_T2G1,
    ENGINE_CONTRACT_VERSION_T2G2, ENGINE_CONTRACT_VERSION_T2G3,
    ENGINE_CONTRACT_VERSION_XG1, ENGINE_CONTRACT_VERSION_DV1,
    GAP_BOUND_REPLAY_VERSIONS,
    RECONSTRUCTION_VERSION, ROUTING_AWARE_ENGINE_CONTRACT_VERSIONS,
    SUPPORTED_ENGINE_CONTRACT_VERSIONS, UNAPPLIED_ANSWERS_ATTR,
    _replays_into_own_gap, reconstruct_readonly_state)
from engine import need_routing as nr
from engine.record_store import StoreError
from web import ui_text
from tests.test_t2g_versioned_journey import (  # noqa: F401 — fixture reuse
    client, _login, _stamped_start, _answer, _raw, _correct, _active_answers)

PRIOR_VERSIONS = (RECONSTRUCTION_VERSION, ENGINE_CONTRACT_VERSION_T2G1,
                  ENGINE_CONTRACT_VERSION_T2G2, ENGINE_CONTRACT_VERSION_NR1,
                  ENGINE_CONTRACT_VERSION_T2G3)
XG1 = ENGINE_CONTRACT_VERSION_XG1
EE = "electronics_electrical"

SEED = ("An automatic plant-watering device that waters my houseplants while I "
        "am travelling, using a soil-moisture sensor and a small pump.")
MC1 = ("The soil-moisture sensor reads the soil, and when the soil is dry the "
       "controller switches on the small pump, which sends water from the tank "
       "to the pot until the sensor reads wet again. It must keep doing this on "
       "its own for the whole two weeks I am away.")
MC1_CORRECTED = MC1.replace("two weeks", "one weekend")
MC2 = ("The main parts are the moisture sensor, a controller, the pump and a "
       "water tank; I do not know what pump flow rate or tank size is needed.")
MC3 = ("First the sensor measures the soil, then the controller compares it "
       "with a dry level, then the pump runs for a short time, and then the "
       "controller waits and checks again.")
PF1 = ("It needs a steady water supply and power, and the sensor must not give "
       "false dry readings because the pump would then run too often and flood "
       "the pot.")
PF2 = ("Because the pump only runs when the sensor reads dry, the main risk is "
       "a stuck sensor, so it should be checked against a known wet and dry pot "
       "before the trip and the tank must hold enough water for the whole "
       "period.")
BA1 = ("It should handle watering one indoor pot while nobody is home, and it "
       "is not responsible for outdoor gardens or fertilising.")
BA_AS_MC_CORRECTION = (
    "Because it is only responsible for one indoor pot while nobody is home, "
    "it deliberately does not handle outdoor gardens, fertilising or several "
    "pots, and someone else must refill the tank before a trip.")
WEAK_MC = "It waters the plant."

NOTICE_EN = ui_text.text("UI_XG1_UNAPPLIED_HEADING", "en")
NOTICE_AR = ui_text.text("UI_XG1_UNAPPLIED_HEADING", "ar")


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def _project(c, appmod, version, answers):
    sid = _stamped_start(c, appmod, version, SEED, EE)
    for text in answers:
        _answer(c, sid, text)
    return sid


def _live(appmod, sid):
    return appmod.SESSION_STORE[sid]["state"]


def _gaps(state):
    return ([(g.gap_type, g.status, g.iterations_open) for g in state.gaps],
            state.maturity_level)


def _record(appmod, sid, prefix):
    return [r for r in _active_answers(appmod, sid) if r.content.startswith(prefix)][0]


def _ledger(appmod, sid):
    return [(r.record_id, r.disposition, r.gap_context, r.question_target,
             tuple(r.supersedes), r.superseded_by, r.content)
            for r in appmod._get_store().load_contract(sid).assertions]


def _view(appmod, state):
    return (_gaps(state),
            appmod._resolve_question_context(state, None).identity,
            tuple(getattr(state, UNAPPLIED_ANSWERS_ATTR, ())))


def _cold(appmod, sid):
    appmod.SESSION_STORE.clear()
    return reconstruct_readonly_state(appmod._get_store(), sid)


def _page(c, sid, lang=None):
    return _html.unescape(_raw(c, sid, lang))


def _corrected(c, appmod, version, answers, prefix, replacement):
    sid = _project(c, appmod, version, answers)
    before = _gaps(_live(appmod, sid))
    target = _record(appmod, sid, prefix)
    assert _correct(c, sid, target.record_id, replacement).status_code == 302
    return sid, before, target


# ==========================================================================
# 1. Versioning and inheritance
# ==========================================================================
def test_exactly_one_sixth_version_is_added_for_new_projects():
    assert XG1 == "p4-2-level1-recon-v1-t2g2-nr1-t2g3-xg1"
    # The displayed-variant relevance repair (DV1) is the seventh version; it
    # is now what new projects record and it carries the gap-bound replay.
    assert SUPPORTED_ENGINE_CONTRACT_VERSIONS == PRIOR_VERSIONS + (
        XG1, ENGINE_CONTRACT_VERSION_DV1)
    assert sr.CURRENT_ENGINE_CONTRACT_VERSION == ENGINE_CONTRACT_VERSION_DV1
    assert GAP_BOUND_REPLAY_VERSIONS == (XG1, ENGINE_CONTRACT_VERSION_DV1)


def test_the_new_version_inherits_t2g3_and_nr1_unchanged():
    from engine.answer_stance import t2g_rule_level
    state = IdeaState(idea_id="i")
    state.domain = "mechanical"
    for version, level in ((ENGINE_CONTRACT_VERSION_T2G3, 3), (XG1, 3)):
        state.engine_contract_version = version
        assert t2g_rule_level(state, MC) == level
    assert ROUTING_AWARE_ENGINE_CONTRACT_VERSIONS == (
        ENGINE_CONTRACT_VERSION_NR1, ENGINE_CONTRACT_VERSION_T2G3, XG1,
        ENGINE_CONTRACT_VERSION_DV1)
    assert nr.is_routing_aware(XG1)
    import web.app as appmod
    for version in (ENGINE_CONTRACT_VERSION_T2G3, XG1):
        state.engine_contract_version = version
        assert appmod._questioning_disclosure_key(state) == "UI_T2G3_QUESTION_SET"


def test_a_real_start_records_the_new_version(client):
    # The newest version (DV1) carries this gap-bound replay unchanged.
    c, appmod, db = client
    _login(c, appmod)
    r = c.post("/start", data={"idea": SEED, "domain_confirm": EE})
    sid = r.headers["Location"].rsplit("/", 1)[-1]
    assert appmod._get_store().load_reconstruction_inputs(sid)[
        "engine_contract_version"] == ENGINE_CONTRACT_VERSION_DV1
    assert _live(appmod, sid).engine_contract_version == ENGINE_CONTRACT_VERSION_DV1
    assert ENGINE_CONTRACT_VERSION_DV1 in GAP_BOUND_REPLAY_VERSIONS


# ==========================================================================
# 2. The predicate — every own-gap state
# ==========================================================================
def _state(*gaps, paused=()):
    state = IdeaState(idea_id="i")
    state.domain = EE
    state.engine_contract_version = XG1
    state.gaps = [Gap(gap_type=g, status=s, opened_at=0) for g, s in gaps]
    if paused:
        setattr(state, pl._PAUSED_ATTR, frozenset(paused))
    return state


@pytest.mark.parametrize("gaps,own,expected", [
    (((MC, CLOSED), (PF, OPEN)), MC, False),                    # own gap CLOSED
    (((MC, CLOSED), (PF, ACCEPTED_RISK), (BA, OPEN)), PF, False),  # ACCEPTED_RISK
    (((MC, CLOSED), (PF, OPEN)), BA, False),                     # own gap absent
    (((MC, PARTIAL), (PF, OPEN)), PF, False),                    # another gap selected
    (((MC, CLOSED), (PF, CLOSED), (BA, CLOSED)), BA, False),     # nothing selected
    (((MC, CLOSED), (PF, PARTIAL)), PF, True),                   # own gap selected
])
def test_an_answer_replays_only_into_its_own_selected_gap(gaps, own, expected):
    assert _replays_into_own_gap(_state(*gaps), own) is expected


def test_a_legacy_record_without_a_gap_keeps_its_reading():
    assert _replays_into_own_gap(_state((MC, CLOSED)), None) is True


def test_a_paused_own_gap_is_eligible_only_once_the_answer_resumes_it():
    state = _state((MC, PARTIAL), (PF, OPEN), paused=(MC,))
    assert _replays_into_own_gap(state, MC) is False
    pl.prepare_answer(state, MC)                 # the replay order: resume first
    assert _replays_into_own_gap(state, MC) is True


def test_a_routed_exhausted_own_gap_is_not_selected():
    from tests.test_safe_question_routing_pf_q2 import (
        _state as routed_state, _to_pf, PF_STRONG)
    state = _to_pf(routed_state(version=XG1))
    pl.run_iteration(state, PF_STRONG)           # PF:Q1 answered; PF:Q2 is routed
    gap = state.get_gap(PF)
    assert gap.status in (OPEN, PARTIAL) and nr.owner_questioning_exhausted(state, gap)
    assert _replays_into_own_gap(state, PF) is False


def test_the_live_correction_owners_are_unchanged():
    """answer_applicable / correction_admissible are not tightened: a CLOSED
    gap can still be corrected and legitimately reopen during replay."""
    state = _state((MC, CLOSED), (PF, OPEN))
    assert pl.answer_applicable(state, MC) is True
    assert pl.correction_admissible(state, MC) is True


# ==========================================================================
# 3. The defect under the previous behaviour, and its repair
# ==========================================================================
@pytest.mark.parametrize("version", PRIOR_VERSIONS)
def test_every_earlier_version_keeps_its_exact_cross_gap_replay(client, version):
    c, appmod, _db = client
    _login(c, appmod)
    sid, before, _ = _corrected(c, appmod, version, [MC1, MC2, MC3],
                                "The soil-moisture", MC1_CORRECTED)
    assert before == ([(MC, CLOSED, 3), (PF, OPEN, 0)], 1)
    live = _view(appmod, _live(appmod, sid))
    assert live == (([(MC, CLOSED, 2), (PF, PARTIAL, 1)], 1), "PATHN:N-PF-2", ())
    cold = _cold(appmod, sid)
    assert cold.review.unapplied_answer_record_ids == ()
    assert _view(appmod, cold.state) == live


def test_an_mc_correction_no_longer_credits_physical_feasibility(client):
    c, appmod, _db = client
    _login(c, appmod)
    sid, before, target = _corrected(c, appmod, XG1, [MC1, MC2, MC3],
                                     "The soil-moisture", MC1_CORRECTED)
    assert before == ([(MC, CLOSED, 3), (PF, OPEN, 0)], 1)
    live = _view(appmod, _live(appmod, sid))
    assert live == (([(MC, CLOSED, 2), (PF, OPEN, 0)], 1), "PATHN:N-PF-1", ("rec_4",))
    cold = _cold(appmod, sid)
    assert cold.review.unapplied_answer_record_ids == ("rec_4",)
    assert _view(appmod, cold.state) == live


def test_an_mc_correction_no_longer_closes_feasibility_or_opens_boundary(client):
    c, appmod, _db = client
    _login(c, appmod)
    for version, after in (
            (ENGINE_CONTRACT_VERSION_T2G3,
             ([(MC, CLOSED, 2), (PF, CLOSED, 2), (BA, OPEN, 0)], 1)),
            (XG1, ([(MC, CLOSED, 2), (PF, PARTIAL, 1)], 1))):
        sid, _before, _ = _corrected(c, appmod, version, [MC1, MC2, MC3, PF1],
                                     "The soil-moisture", MC1_CORRECTED)
        assert _gaps(_live(appmod, sid)) == after


def test_false_level_two_maturity_is_prevented(client):
    c, appmod, _db = client
    _login(c, appmod)
    answers = [MC1, MC2, MC3, PF1, PF2, BA1]
    results = {}
    for version in (ENGINE_CONTRACT_VERSION_T2G3, XG1):
        sid, before, _ = _corrected(c, appmod, version, answers,
                                    "The soil-moisture", BA_AS_MC_CORRECTION)
        assert before == ([(MC, CLOSED, 3), (PF, CLOSED, 2), (BA, PARTIAL, 1)], 1)
        results[version] = (_gaps(_live(appmod, sid)), _gaps(_cold(appmod, sid).state))
    # the previous behaviour: a Mechanism correction closed Boundary -> Level 2
    assert results[ENGINE_CONTRACT_VERSION_T2G3][0][1] == 2
    # repaired: Boundary keeps its own state and maturity stays at Level 1
    live, cold = results[XG1]
    assert live == cold == ([(MC, CLOSED, 2), (PF, CLOSED, 2), (BA, PARTIAL, 1)], 1)


def test_a_later_unchanged_answer_displaced_by_an_earlier_correction(client):
    c, appmod, _db = client
    _login(c, appmod)
    sid, _b, _ = _corrected(c, appmod, ENGINE_CONTRACT_VERSION_T2G3,
                            [MC1, MC2, MC3, PF1], "First the sensor", WEAK_MC)
    # previous behaviour: the Feasibility answer was credited to Mechanism
    assert _gaps(_live(appmod, sid)) == ([(MC, PARTIAL, 4)], 1)
    sid, _b, _ = _corrected(c, appmod, XG1, [MC1, MC2, MC3, PF1],
                            "First the sensor", WEAK_MC)
    pf_answer = _record(appmod, sid, "It needs a steady")
    live = _view(appmod, _live(appmod, sid))
    assert live[0] == ([(MC, PARTIAL, 3)], 1)
    assert live[2] == (pf_answer.record_id,)
    assert pf_answer.gap_context == PF                  # durable truth unchanged
    cold = _cold(appmod, sid)
    assert cold.review.unapplied_answer_record_ids == (pf_answer.record_id,)
    assert _view(appmod, cold.state) == live


# ==========================================================================
# 4. Legitimate same-gap corrections are unchanged
# ==========================================================================
@pytest.mark.parametrize("answers,prefix,replacement", [
    ([MC1, MC2], "The soil-moisture", MC1_CORRECTED),          # gap still open
    ([MC1, MC2, MC3], "First the sensor",                      # CLOSED live, reopens
     MC3.replace("short time", "few seconds")),
    ([MC1, MC2, MC3, PF1], "It needs a steady",                # the current gap
     PF1.replace("steady", "reliable")),
])
def test_same_gap_corrections_replay_identically_on_both_versions(
        client, answers, prefix, replacement):
    c, appmod, _db = client
    _login(c, appmod)
    views = []
    for version in (ENGINE_CONTRACT_VERSION_T2G3, XG1):
        sid, _b, _ = _corrected(c, appmod, version, answers, prefix, replacement)
        live = _view(appmod, _live(appmod, sid))
        assert live[2] == ()
        assert _view(appmod, _cold(appmod, sid).state) == live
        views.append(live)
    assert views[0] == views[1]


def test_an_ordinary_history_has_no_unapplied_answer(client):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _project(c, appmod, XG1, [MC1, MC2, MC3, PF1])
    assert not hasattr(_live(appmod, sid), UNAPPLIED_ANSWERS_ATTR)
    cold = _cold(appmod, sid)
    assert cold.review.unapplied_answer_record_ids == ()
    assert not hasattr(cold.state, UNAPPLIED_ANSWERS_ATTR)


# ==========================================================================
# 5. Durable truth, parity and the correction route
# ==========================================================================
def test_the_correction_chain_and_text_are_preserved_verbatim(client):
    c, appmod, _db = client
    _login(c, appmod)
    sid, _b, target = _corrected(c, appmod, XG1, [MC1, MC2, MC3],
                                 "The soil-moisture", MC1_CORRECTED)
    ledger = _ledger(appmod, sid)
    assert ledger[0] == ("rec_1", "answered", MC, "PATHN:N-MC-1", (), "rec_4", MC1)
    assert ledger[3] == ("rec_4", "answered", MC, "PATHN:N-MC-1", ("rec_1",), None,
                         MC1_CORRECTED)
    assert [r[0] for r in ledger] == ["rec_1", "rec_2", "rec_3", "rec_4"]


def test_live_cold_and_resumed_agree_on_counters_question_and_records(client):
    c, appmod, _db = client
    _login(c, appmod)
    sid, _b, _ = _corrected(c, appmod, XG1, [MC1, MC2, MC3, PF1],
                            "First the sensor", WEAK_MC)
    live = _view(appmod, _live(appmod, sid))
    live_ledger = _ledger(appmod, sid)
    cold = _cold(appmod, sid)
    assert _view(appmod, cold.state) == live
    _raw(c, sid)
    assert c.post(f"/session/{sid}/resume", data={}).status_code == 302
    assert _view(appmod, _live(appmod, sid)) == live
    assert _ledger(appmod, sid) == live_ledger


def test_a_retried_correction_writes_nothing_more(client):
    c, appmod, _db = client
    _login(c, appmod)
    sid, _b, target = _corrected(c, appmod, XG1, [MC1, MC2, MC3],
                                 "The soil-moisture", MC1_CORRECTED)
    n = len(_ledger(appmod, sid))
    _correct(c, sid, target.record_id, MC1_CORRECTED)     # the target is now stale
    assert len(_ledger(appmod, sid)) == n
    assert "could not be applied" in _page(c, sid)
    assert _view(appmod, _live(appmod, sid))[2] == ("rec_4",)


def test_a_failed_correction_write_changes_nothing(client, monkeypatch):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _project(c, appmod, XG1, [MC1, MC2, MC3])
    before = (_view(appmod, _live(appmod, sid)), _ledger(appmod, sid))
    target = _record(appmod, sid, "The soil-moisture")

    def _fail(*_a, **_k):
        raise StoreError("unavailable")
    with monkeypatch.context() as m:
        m.setattr(appmod._get_store(), "append_record", _fail)
        _correct(c, sid, target.record_id, MC1_CORRECTED)
    assert (_view(appmod, _live(appmod, sid)), _ledger(appmod, sid)) == before


# ==========================================================================
# 6. Saved-but-not-counted disclosure
# ==========================================================================
def test_the_notice_names_only_the_affected_answer_and_survives_reload_and_resume(
        client):
    c, appmod, _db = client
    _login(c, appmod)
    sid, _b, _ = _corrected(c, appmod, XG1, [MC1, MC2, MC3, PF1],
                            "First the sensor", WEAK_MC)
    for page in (_page(c, sid), _page(c, sid)):          # after the PRG, a reload
        assert NOTICE_EN in page
        notice = page.split(NOTICE_EN, 1)[1][:2500]
        assert "It needs a steady water supply" in notice
        assert "First the sensor" not in notice and "The soil-moisture" not in notice
    arabic_raw = _raw(c, sid, "ar")
    arabic = _html.unescape(arabic_raw)
    assert NOTICE_AR in arabic and NOTICE_EN not in arabic
    assert 'dir="rtl"' in arabic_raw and 'lang="ar"' in arabic_raw
    appmod.SESSION_STORE.clear()
    assert NOTICE_EN in _page(c, sid)                     # cold read-only page
    assert c.post(f"/session/{sid}/resume", data={}).status_code == 302
    assert NOTICE_EN in _page(c, sid)                     # writable resume


def test_the_notice_is_truthful_in_both_languages():
    en = ui_text.text("UI_XG1_UNAPPLIED_EXPLAIN", "en")
    assert "saved in your project exactly as you wrote" in en
    assert "not counted toward progress right now" in en
    assert "not counted toward any other part either" in en
    assert "other progress shown on this page may also have changed" in en
    ar = ui_text.text("UI_XG1_UNAPPLIED_EXPLAIN", "ar")
    assert "محفوظة في مشروعك كما كتبتها" in ar
    assert "لا تُحتسب الآن في التقدّم" in ar
    assert "قد يكون تقدّم آخر" in ar


def test_no_notice_without_an_unapplied_answer_or_on_an_earlier_version(client):
    c, appmod, _db = client
    _login(c, appmod)
    ordinary = _project(c, appmod, XG1, [MC1, MC2, MC3, PF1])
    assert NOTICE_EN not in _page(c, ordinary)
    earlier, _b, _ = _corrected(c, appmod, ENGINE_CONTRACT_VERSION_T2G3,
                                [MC1, MC2, MC3, PF1], "First the sensor", WEAK_MC)
    assert NOTICE_EN not in _page(c, earlier)


def test_one_projects_notice_never_shows_another_projects_answer(client):
    c, appmod, _db = client
    _login(c, appmod)
    affected, _b, _ = _corrected(c, appmod, XG1, [MC1, MC2, MC3, PF1],
                                 "First the sensor", WEAK_MC)
    other = _project(c, appmod, XG1, [MC1, MC2, MC3])
    assert NOTICE_EN in _page(c, affected)
    assert NOTICE_EN not in _page(c, other)
