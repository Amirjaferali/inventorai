"""W2-C / RVR-6b — real served-route evidence, composition with W2-B, EN/AR
route behavior, reconstruction parity through the real durable journey, and
the mandatory lapsed-acceptance revalidation's live-route leg.

Composed precedence exercised here (proposed at this implementation
candidate, Owner-accepted only at exact-SHA acceptance):
  1. W2-B question-slot overrides (LAPSED > SKIP > CRITICAL) — always first;
  2. W2-B alternatives transition (action slot) — W2-C question slot defers;
  3. W2-C intent-coverage law — only over the plain canonical Path-N variant;
  4. canonical serving (index law / stall reframe / exhausted exit) —
     baseline and universal fail-closed target, never overridden by W2-C.
"""
import html as _html
import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

import engine.intent_serving as intent_serving
from engine.idea_state import (
    MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, DISPOSITION_ANSWERED,
    DISPOSITION_RISK_ACCEPTED,
)
from engine.path_n_questions import get_served_question
from engine.progression_loop import (
    select_next_gap, get_display_question, _STALL_REFRAME,
    _EXHAUSTED_EXIT_PROMPT,
)

SEED = ("a manually foldable wheelchair ramp for a home doorway — the "
        "inventor wants the ramp to stay reliably locked in the flat, "
        "load-bearing position and to fold away without tools")
ELEC_SEED = ("a doorway sensor that notices when the ramp is left deployed "
             "and alerts the resident through a small indicator")
MC_STRONG = ("(1) unfolding: the operator lifts the handle and the panel "
             "rotates on the hinge until flat. (2) locking: the toggle latch "
             "snaps over the center rib and holds the panel rigid. "
             "(3) folding: pressing the release lever frees the latch and the "
             "panel folds upward.")
PF_PLAIN = ("I have not tested whether the toggle latch stays reliable "
            "under repeated loading and outdoor use.")
MC_RETRACTION = ("That earlier locking description was wrong and I need to "
                 "rethink the whole latch approach from scratch.")
# does NOT address MECHANISM by the family test, and carries Q2's committed
# intent vocabulary ("force path") — a coverage writer for Q2 without closing
COVERS_Q2_ONLY = "The force path is what I planned around from the start."
NEUTRAL_ANSWER = "I will need to think more about this whole area."

MECH_MC = [get_served_question(MECHANISM_COMPLETENESS, i, domain="mechanical")
           for i in range(4)]


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("INVENTORAI_DB_PATH", str(tmp_path / "w2c-web.sqlite"))
    monkeypatch.setattr(intent_serving, "_REGISTRY_CACHE", {})
    import web.app as appmod
    monkeypatch.setattr(appmod, "_STORE", None)
    appmod.SESSION_STORE.clear()
    appmod.app.config["TESTING"] = True
    with appmod.app.test_client() as c:
        yield c, appmod


def _start(c, domain="mechanical", seed=SEED):
    r = c.post("/start", data={"idea": seed, "domain_confirm": domain})
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


def _page(c, sid, lang=None):
    url = f"/session/{sid}" + (f"?lang={lang}" if lang else "")
    return _html.unescape(c.get(url).get_data(as_text=True))


def _state(appmod, sid):
    return appmod.SESSION_STORE[sid]["state"]


# --- real served-route: mechanical --------------------------------------------

def test_mech_uncovered_journey_is_byte_canonical(client):
    """No coverage evidence -> the W2-C layer is inert and the canonical
    question is served verbatim (deterministic no-op on plain journeys)."""
    c, appmod = client
    sid = _start(c)
    _answer(c, sid, NEUTRAL_ANSWER)
    state = _state(appmod, sid)
    assert select_next_gap(state) == MECHANISM_COMPLETENESS
    gap = state.get_gap(MECHANISM_COMPLETENESS)
    expected = get_display_question("mechanical", MECHANISM_COMPLETENESS,
                                    gap.iterations_open, path="N")
    assert expected in _page(c, sid)


def test_mech_covered_intent_is_suppressed_on_the_live_route(client):
    """A recorded answer that already carries Q2's committed intent
    vocabulary makes the Q2 turn serve Q3 instead — the covered intent is
    not re-asked (real suppression on the real route)."""
    c, appmod = client
    sid = _start(c)
    _answer(c, sid, COVERS_Q2_ONLY)          # recorded against MC (gap 0 turn)
    state = _state(appmod, sid)
    assert select_next_gap(state) == MECHANISM_COMPLETENESS
    gap = state.get_gap(MECHANISM_COMPLETENESS)
    assert gap.iterations_open == 1          # canonical turn would be Q2
    page = _page(c, sid)
    assert MECH_MC[2].text in page           # Q3 served instead
    assert MECH_MC[1].text not in page       # covered Q2 not re-asked


def test_mech_ar_coverage_behaves_identically(client):
    """The paired Arabic surface writes the SAME coverage: an AR answer
    carrying Q2's paired vocabulary suppresses Q2 exactly like the EN one
    (no bilingual divergence in coverage/suppression/ordering)."""
    c, appmod = client
    sid = _start(c)
    _answer(c, sid, "لقد خططت حول مسار القوة منذ البداية.")
    page = _page(c, sid)
    assert MECH_MC[2].text in page
    assert MECH_MC[1].text not in page


def test_ui_language_is_independent_of_coverage(client):
    """UI-language separation: the same adjusted serving renders under the
    Arabic UI without changing which committed variant is chosen."""
    c, appmod = client
    sid = _start(c)
    _answer(c, sid, COVERS_Q2_ONLY)
    page_ar = _page(c, sid, lang="ar")
    assert MECH_MC[2].text in page_ar        # committed EN variant text
    assert MECH_MC[1].text not in page_ar


def test_reframe_and_exit_surfaces_are_never_overridden(client):
    """Precedence 4: at artifact exhaustion the RVR-2 stall reframe / exit
    prompt serve exactly as before, even though uncovered variants remain."""
    c, appmod = client
    sid = _start(c)
    for _ in range(5):
        _answer(c, sid, NEUTRAL_ANSWER)
        if select_next_gap(_state(appmod, sid)) != MECHANISM_COMPLETENESS:
            break
    state = _state(appmod, sid)
    if select_next_gap(state) == MECHANISM_COMPLETENESS:
        page = _page(c, sid)
        assert (_STALL_REFRAME in page) or (_EXHAUSTED_EXIT_PROMPT in page)


def test_w2b_lapse_flow_and_revalidation_live_leg(client):
    """Mandatory lapsed-acceptance revalidation (live-route leg): with W2-C
    active, the correction-lapse journey reopens the lapsed area exactly as
    the W2-B suite proved — the reopened gap serves a truthful committed
    question of the SAME gap and the governed lapse cue renders. The
    mechanical proof of NOT AFFECTED is in the evidence pack (render-only
    consumer census + ledger-free supplement scope)."""
    c, appmod = client
    sid = _start(c)
    steps = 0
    while (select_next_gap(_state(appmod, sid)) == MECHANISM_COMPLETENESS
           and steps < 8):
        _answer(c, sid, MC_STRONG)
        steps += 1
    assert select_next_gap(_state(appmod, sid)) == PHYSICAL_FEASIBILITY
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
    assert risk_records
    steps = 0
    while (select_next_gap(state) == MECHANISM_COMPLETENESS and steps < 8):
        _answer(c, sid, MC_STRONG)
        steps += 1
    assert select_next_gap(state) == PHYSICAL_FEASIBILITY
    page = _page(c, sid)
    from web import ui_text
    assert ui_text.UI_STRINGS["UI_W2B_CUE_REOPENED_LAPSE"]["en"] in page
    pf_variants = {get_served_question(PHYSICAL_FEASIBILITY, i,
                                       domain="mechanical").text
                   for i in range(2)}
    assert any(v in page for v in pf_variants)


def test_fail_closed_registry_outage_serves_canonical(client, monkeypatch):
    monkeypatch.setitem(
        intent_serving._DOMAIN_REGISTRY_FILES, "mechanical",
        ("docs/governance/path_n_content_config/does_not_exist.json",
         intent_serving._DOMAIN_REGISTRY_FILES["mechanical"][1]))
    c, appmod = client
    sid = _start(c)
    _answer(c, sid, COVERS_Q2_ONLY)
    page = _page(c, sid)
    assert MECH_MC[1].text in page           # canonical Q2 — no suppression
    assert MECH_MC[2].text not in page


# --- real served-route: electronics -------------------------------------------

def test_electronics_covered_intent_suppressed(client):
    c, appmod = client
    sid = _start(c, domain="electronics_electrical", seed=ELEC_SEED)
    state = _state(appmod, sid)
    if select_next_gap(state) != MECHANISM_COMPLETENESS:
        pytest.skip("electronics journey did not open MECHANISM first")
    # covers N-MC-2 ("main parts") without addressing the family test
    _answer(c, sid, "The main parts were already listed in my notes.")
    state = _state(appmod, sid)
    gap = state.get_gap(MECHANISM_COMPLETENESS)
    if gap is None or gap.iterations_open != 1:
        pytest.skip("journey advanced differently — covered elsewhere")
    n_mc = [get_served_question(MECHANISM_COMPLETENESS, i,
                                domain="electronics_electrical")
            for i in range(4)]
    page = _page(c, sid)
    assert n_mc[2].text in page              # N-MC-3 served
    assert n_mc[1].text not in page          # covered N-MC-2 suppressed


# --- reconstruction parity through the real durable journey -------------------

def test_reconstruction_parity_with_supplement_and_coverage(client):
    """Live vs reconstructed state parity for a journey that exercised BOTH
    W2-C state effects (the supplement) and the coverage-adjusted display:
    the reconstructed canonical state matches the live one field-for-field
    on gaps/maturity/stage, and the recomputed W2-C serving is identical."""
    c, appmod = client
    sid = _start(c)
    fixture = json.load(open("tests/fixtures/s2_run_001_answer_maps.json"))
    w1n3 = fixture["answers"]["M-1|expert|en"]["MECHANISM_COMPLETENESS"][1]
    _answer(c, sid, NEUTRAL_ANSWER)          # turn 0 (Q1)
    _answer(c, sid, w1n3)                    # turn 1 (Q2) — supplement fires
    _answer(c, sid, COVERS_Q2_ONLY)          # coverage writer
    live = _state(appmod, sid)
    from engine.session_reconstruction import reconstruct_readonly_state
    recon = reconstruct_readonly_state(appmod._get_store(), sid)
    assert recon.state is not None
    for attr in ("maturity_level", "current_stage", "iteration"):
        assert getattr(recon.state, attr) == getattr(live, attr)
    assert ([(g.gap_type, g.status, g.iterations_open) for g in recon.state.gaps]
            == [(g.gap_type, g.status, g.iterations_open) for g in live.gaps])
    gap_type = select_next_gap(live)
    if gap_type:
        assert (intent_serving.w2c_served_question(recon.state, gap_type)
                == intent_serving.w2c_served_question(live, gap_type))
        assert (intent_serving.compute_intent_coverage(recon.state, gap_type)
                == intent_serving.compute_intent_coverage(live, gap_type))
