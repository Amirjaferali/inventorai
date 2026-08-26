"""W2-B / RVR-6a (amended contract) — real web serving behavior.

Authority: Contract Amendment 1 §4/§5/§10/§16 (authoritative via PR #575).
Real-journey proof that the served interaction actually changes with state
(never a cue alone), that trigger-free journeys render byte-identically,
that reachability limitations are honored truthfully (no false firing on
the governed artifact surface), and that every W2-B string is a governed
EN/AR pair that never overstates what happened.
"""
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import html as _html

import pytest

from engine.idea_state import (
    MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY,
    PROBLEM_MECHANISM_FIT,
    DISPOSITION_ANSWERED, DISPOSITION_RISK_ACCEPTED,
)
from engine.progression_loop import (
    QUESTIONS, select_next_gap, _EXHAUSTED_EXIT_PROMPT,
)
from web import ui_text

SEED = ("a manually foldable wheelchair ramp for a home doorway — the "
        "inventor wants the ramp to stay reliably locked in the flat, "
        "load-bearing position and to fold away without tools")
MC_STRONG = ("(1) unfolding: the operator lifts the handle and the panel "
             "rotates on the hinge until flat. (2) locking: the toggle latch "
             "snaps over the center rib and holds the panel rigid. "
             "(3) folding: pressing the release lever frees the latch and the "
             "panel folds upward.")
PF_STRONG = ("(1) load path: the toggle latch carries the vertical load "
             "through a steel pin rated well above the wheelchair weight. "
             "(2) energy: the ramp is unpowered - no power source or current "
             "is required. (3) operating limits: outdoor temperature range "
             "and repeated-folding fatigue stay within the material limits.")
BA_STRONG = ("(1) boundary: the ramp does not cover stair flights - single "
             "doorway thresholds only. (2) difference: unlike wedge ramps, "
             "the folding hinge-line keeps a continuous load-bearing surface. "
             "(3) core: the center toggle latch is the irreplaceable locking "
             "mechanism.")
PF_PLAIN = ("I have not tested whether the toggle latch stays reliable "
            "under repeated loading and outdoor use.")
PMF_PLAIN = ("People with wheelchairs cannot cross the raised doorway "
             "threshold at home without help from another person.")
WEAK = "i don't know"
MC_RETRACTION = ("That earlier locking description was wrong and I need to "
                 "rethink the whole latch approach from scratch.")

W2B_KEYS = (
    "UI_W2B_CUE_RISK_NOT_REASKED",
    "UI_W2B_CUE_REOPENED_LAPSE",
    "UI_W2B_CUE_CRITICAL_REPHRASED",
    "UI_W2B_CUE_INTENT_SKIP",
    "UI_W2B_ACTION_DECISION_EVIDENCE",
    "UI_W2B_ACTION_DECISION_LINK",
)


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("INVENTORAI_DB_PATH", str(tmp_path / "w2b-web.sqlite"))
    import web.app as appmod
    monkeypatch.setattr(appmod, "_STORE", None)
    appmod.SESSION_STORE.clear()
    appmod.app.config["TESTING"] = True
    with appmod.app.test_client() as c:
        yield c, appmod


def _start(c):
    r = c.post("/start", data={"idea": SEED, "domain_confirm": "mechanical"})
    assert r.status_code == 302
    return r.headers["Location"].rsplit("/", 1)[-1]


def _token(c, sid):
    page = c.get(f"/session/{sid}").get_data(as_text=True)
    m = re.search(r'name="answer_token" value="([^"]+)"', page)
    return _html.unescape(m.group(1))


def _answer(c, sid, text):
    return c.post(f"/session/{sid}", data={
        "response": text, "answer_token": _token(c, sid),
        "action": "answered"})


def _page(c, sid):
    return _html.unescape(c.get(f"/session/{sid}").get_data(as_text=True))


def _state(appmod, sid):
    return appmod.SESSION_STORE[sid]["state"]


def _close_mech(c, appmod, sid, max_steps=8):
    steps = 0
    while (select_next_gap(_state(appmod, sid)) == MECHANISM_COMPLETENESS
           and steps < max_steps):
        _answer(c, sid, MC_STRONG)
        steps += 1
    assert select_next_gap(_state(appmod, sid)) == PHYSICAL_FEASIBILITY


def _to_stage3(c, appmod, sid):
    _close_mech(c, appmod, sid)
    for content in (PF_STRONG, PF_STRONG, BA_STRONG, BA_STRONG):
        _answer(c, sid, content)
    state = _state(appmod, sid)
    assert state.current_stage == 3
    assert select_next_gap(state) == PROBLEM_MECHANISM_FIT


def _en(key):
    return ui_text.UI_STRINGS[key]["en"]


# --- catalogue discipline / truthfulness --------------------------------------

def test_every_w2b_string_is_a_governed_en_ar_pair():
    for key in W2B_KEYS:
        entry = ui_text.UI_STRINGS.get(key)
        assert isinstance(entry, dict), key
        assert entry.get("en") and entry.get("ar"), key
        assert entry["en"] != entry["ar"], key


def test_no_string_overstates_engine_behavior():
    for key in W2B_KEYS:
        en = _en(key).lower()
        for forbidden in ("served first", "is resolved", "has been resolved",
                          "is complete", "completed this area",
                          "no longer a risk", "are comparable"):
            assert forbidden not in en, (key, forbidden)


# --- trigger-free preservation ------------------------------------------------

def test_trigger_free_page_has_no_w2b_markup(client):
    c, appmod = client
    sid = _start(c)
    page = _page(c, sid)
    for marker in ("w2b-routing-cues", "w2b-risk-note", "w2b-primary-action"):
        assert marker not in page
    for key in W2B_KEYS:
        assert _en(key) not in page


# --- trigger 4: real served-question change through the journey ---------------

def test_stage3_skip_serves_exit_prompt_instead_of_verbatim_repeat(client):
    c, appmod = client
    sid = _start(c)
    _to_stage3(c, appmod, sid)
    baseline_repeat = QUESTIONS[PROBLEM_MECHANISM_FIT][-1]
    suppressed_seen = False
    for _ in range(6):
        page = _page(c, sid)
        if _en("UI_W2B_CUE_INTENT_SKIP") in page:
            suppressed_seen = True
            break
        _answer(c, sid, PMF_PLAIN)
    assert suppressed_seen, "clamped stage-3 repeat never adapted"
    # the SERVED QUESTION is materially different, not merely annotated
    assert _EXHAUSTED_EXIT_PROMPT in page
    assert baseline_repeat not in page
    # contrary evidence lowers the register (M=2: two weak signals) and the
    # serving truthfully reverses to the canonical question
    _answer(c, sid, WEAK)
    _answer(c, sid, WEAK)
    page2 = _page(c, sid)
    assert _en("UI_W2B_CUE_INTENT_SKIP") not in page2
    assert baseline_repeat in page2


# --- accepted risk: rerouting + transparency ---------------------------------

def test_accepted_risk_not_reasked_with_note(client):
    c, appmod = client
    sid = _start(c)
    _close_mech(c, appmod, sid)
    _answer(c, sid, PF_PLAIN)
    r = c.post(f"/session/{sid}/accept-risk", data={
        "gap_type": PHYSICAL_FEASIBILITY, "risk_confirm": "yes",
        "reason": "cannot verify yet", "answer_token": _token(c, sid)})
    assert r.status_code == 302
    state = _state(appmod, sid)
    assert select_next_gap(state) == BOUNDARY_AMBIGUITY
    assert _en("UI_W2B_CUE_RISK_NOT_REASKED") in _page(c, sid)


# --- lapse: reachable transparency + truthful canonical re-ask ---------------

def test_lapse_reopens_with_cue_and_canonical_primary_question(client):
    """Real correction flow: the lapsed area re-opens and the canonical
    serving re-asks its primary question (the truthful re-resolution); the
    governed cue explains the reopening. The stale-index override class is
    engine-proven (serving-policy suite) and declared route-limited in the
    evidence pack — this test pins that NO false override or false cue
    appears where the canonical behavior is already correct."""
    c, appmod = client
    sid = _start(c)
    _close_mech(c, appmod, sid)
    _answer(c, sid, PF_PLAIN)
    c.post(f"/session/{sid}/accept-risk", data={
        "gap_type": PHYSICAL_FEASIBILITY, "risk_confirm": "yes",
        "reason": "cannot verify yet", "answer_token": _token(c, sid)})
    state = _state(appmod, sid)
    mc_answers = [r for r in state.assertions
                  if r.disposition == DISPOSITION_ANSWERED
                  and r.gap_context == MECHANISM_COMPLETENESS
                  and r.superseded_by is None]
    r = c.post(f"/session/{sid}/correct", data={
        "supersedes_record_id": mc_answers[-1].record_id,
        "response": MC_RETRACTION,
        "answer_token": _token(c, sid)})
    assert r.status_code == 302
    state = _state(appmod, sid)
    risk_records = [r2 for r2 in state.assertions
                    if r2.disposition == DISPOSITION_RISK_ACCEPTED
                    and r2.superseded_by is None]
    assert risk_records                      # the acceptance record stands
    pf = state.get_gap(PHYSICAL_FEASIBILITY)
    assert pf is None or pf.status in ("OPEN", "PARTIAL")   # lapsed
    steps = 0
    while (select_next_gap(state) == MECHANISM_COMPLETENESS and steps < 8):
        _answer(c, sid, MC_STRONG)
        steps += 1
    assert select_next_gap(state) == PHYSICAL_FEASIBILITY
    page = _page(c, sid)
    assert _en("UI_W2B_CUE_REOPENED_LAPSE") in page
    # canonical serving already asks the area's primary question at the
    # reopened index — truthful re-resolution with no fabricated override
    pf = state.get_gap(PHYSICAL_FEASIBILITY)
    from engine.progression_loop import get_display_question
    expected = get_display_question("mechanical", PHYSICAL_FEASIBILITY,
                                    pf.iterations_open, path="N")
    assert expected in page


# --- no false firing on the governed artifact surface ------------------------

def test_no_critical_or_skip_firing_on_artifact_exhaustion(client):
    """Stalling a stage-2 gap of an artifact domain lands on RVR-2's
    governed reframe/exit surface; the W2-B policy must not double-govern
    it — no critical/skip cue, no override marker."""
    c, appmod = client
    sid = _start(c)
    _close_mech(c, appmod, sid)
    for _ in range(4):
        _answer(c, sid, WEAK)
    page = _page(c, sid)
    assert _en("UI_W2B_CUE_CRITICAL_REPHRASED") not in page
    assert _en("UI_W2B_CUE_INTENT_SKIP") not in page


# --- Arabic rendering ---------------------------------------------------------

def test_cues_render_single_language_arabic(client):
    c, appmod = client
    sid = _start(c)
    _close_mech(c, appmod, sid)
    _answer(c, sid, PF_PLAIN)
    c.post(f"/session/{sid}/accept-risk", data={
        "gap_type": PHYSICAL_FEASIBILITY, "risk_confirm": "yes",
        "reason": "cannot verify yet", "answer_token": _token(c, sid)})
    with c.session_transaction() as fs:
        fs["ui_lang"] = "ar"
    page = _page(c, sid)
    assert ui_text.UI_STRINGS["UI_W2B_CUE_RISK_NOT_REASKED"]["ar"] in page
    assert _en("UI_W2B_CUE_RISK_NOT_REASKED") not in page
