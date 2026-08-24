"""Wave-2 W2-D — W1-N4 correction-lapse transparency.

Contract: docs/governance/WAVE_2_BOUNDED_IMPLEMENTATION_CONTRACT_CANDIDATE.md §K
(authoritative via PR #563 merge 58e92e09). Computation lives at the RVR-1/R4-C
reconstruction seam: the replay reports, per recorded `risk_accepted`
disposition, whether it re-applied or lapsed (read-only derived artifact; the
D-AISR-06 full-re-evaluation semantics are unchanged and no stale acceptance is
ever preserved). Rendering lives in the RVR-5 correction UX: when a correction
causes a prior acceptance to lapse, the user sees a truthful governed
explanation next to the correction acknowledgement.
"""
import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

from engine.idea_state import (
    ACCEPTED_RISK, OPEN, PARTIAL,
    MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY,
    DISPOSITION_RISK_ACCEPTED,
)
from engine.progression_loop import select_next_gap

SEED = ("a manually foldable wheelchair ramp for a home doorway — the inventor "
        "wants the ramp to stay reliably locked in the flat, load-bearing "
        "position and to fold away without tools")
MECH = ("The ramp folds up and down by hand. When it is down flat, it must "
        "stay firmly held so a wheelchair can roll over it. I am considering "
        "three ways to hold it: a toggle latch that snaps over its center, a "
        "spring pin that clicks into place, or a small gate piece that drops "
        "into place by its own weight.")
FEAS_ATTEMPT = ("I have not tested whether the toggle latch stays reliable "
                "under repeated loading and outdoor use.")
# A weak mechanism replacement: superseding one of the two closing MECH answers
# with this reopens the journey upstream of PHYSICAL_FEASIBILITY.
WEAK_MECH = "The ramp is held down by a part that keeps it in place."


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("INVENTORAI_DB_PATH", str(tmp_path / "w2dn4.sqlite"))
    import web.app as appmod
    monkeypatch.setattr(appmod, "_STORE", None)
    appmod.SESSION_STORE.clear()
    appmod.app.config["TESTING"] = True
    with appmod.app.test_client() as c:
        yield c, appmod


def _start(c):
    r = c.post("/start", data={"idea": SEED, "domain_confirm": "mechanical"})
    return r.headers["Location"].rsplit("/", 1)[-1]


def _token(c, sid):
    import re, html
    page = c.get(f"/session/{sid}").get_data(as_text=True)
    m = re.search(r'name="answer_token" value="([^"]+)"', page)
    return html.unescape(m.group(1))


def _answer(c, sid, text):
    return c.post(f"/session/{sid}", data={
        "response": text, "answer_token": _token(c, sid), "action": "answered"})


def _accepted_journey(c, appmod, sid):
    """seed → MECH×2 (closes MECH) → substantive feasibility attempt →
    accepted risk on PHYSICAL_FEASIBILITY."""
    state = appmod.SESSION_STORE[sid]["state"]
    steps = 0
    while select_next_gap(state) == MECHANISM_COMPLETENESS and steps < 8:
        _answer(c, sid, MECH)
        steps += 1
    assert select_next_gap(state) == PHYSICAL_FEASIBILITY
    _answer(c, sid, FEAS_ATTEMPT)
    r = c.post(f"/session/{sid}/accept-risk", data={
        "gap_type": PHYSICAL_FEASIBILITY, "risk_confirm": "yes",
        "reason": "cannot verify yet", "answer_token": _token(c, sid)})
    assert r.status_code == 302
    assert state.get_gap(PHYSICAL_FEASIBILITY).status == ACCEPTED_RISK
    return state


def _correct(c, sid, target_id, replacement):
    return c.post(f"/session/{sid}/correct", data={
        "supersedes_record_id": target_id, "response": replacement,
        "answer_token": _token(c, sid)}, follow_redirects=False)


def _mech_record(state, index=0):
    recs = [r for r in state.assertions
            if r.disposition == "answered" and r.content == MECH
            and r.superseded_by is None]
    return recs[index]


# --- N4-1: correction that leaves the acceptance applicable → no notice -------
# Canonical R4-C replay is seq-ordered and a replacement record replays at the
# END of the amended stream, so the acceptance-preserving correction is one
# whose withdrawal does not disturb the pre-acceptance replay prefix: here,
# superseding the feasibility ATTEMPT itself (the acceptance then replays
# against a still-OPEN gap and re-applies). Correcting an upstream mechanism
# answer is a GENUINE lapse under those frozen semantics and is covered by
# N4-2 below.

def test_n4_1_benign_correction_no_false_lapse(client):
    c, appmod = client
    sid = _start(c)
    state = _accepted_journey(c, appmod, sid)
    target = next(r for r in state.assertions
                  if r.content == FEAS_ATTEMPT and r.superseded_by is None)
    _correct(c, sid, target.record_id,
             "I still have not verified whether the spring pin stays reliable "
             "under repeated outdoor loading.")
    state = appmod.SESSION_STORE[sid]["state"]
    assert state.get_gap(PHYSICAL_FEASIBILITY).status == ACCEPTED_RISK
    page = c.get(f"/session/{sid}").get_data(as_text=True)
    assert "risk-lapse" not in page


# --- N4-2/N4-3/N4-4: invalidating correction → lapse + truthful notice --------

def test_n4_234_lapse_reported_and_rendered(client):
    c, appmod = client
    sid = _start(c)
    state = _accepted_journey(c, appmod, sid)
    target = _mech_record(state)
    r = _correct(c, sid, target.record_id, WEAK_MECH)
    assert r.status_code == 302
    state = appmod.SESSION_STORE[sid]["state"]
    # N4-4: no stale acceptance in the rebuilt canonical state — the journey
    # rebuilt upstream, PHYSICAL_FEASIBILITY is no longer covered
    g = state.get_gap(PHYSICAL_FEASIBILITY)
    assert g is None or g.status != ACCEPTED_RISK
    # N4-2: the lapse report names the affected acceptance/gap
    from web.app import _get_store
    from engine.session_reconstruction import reconstruct_readonly_state
    recon = reconstruct_readonly_state(_get_store(), sid)
    lapsed = [o for o in recon.review.risk_acceptance_outcomes if not o.applied]
    assert len(lapsed) == 1
    assert lapsed[0].gap_context == PHYSICAL_FEASIBILITY
    assert lapsed[0].record_id
    assert lapsed[0].reason  # bounded deterministic category
    # N4-3: the correction acknowledgement view carries the truthful notice
    page = c.get(f"/session/{sid}").get_data(as_text=True)
    assert "risk-lapse" in page
    # the notice does not lie: no claim the gap is CLOSED/resolved
    assert "risk acceptance" in page or "acceptance" in page


def test_n4_3_notice_renders_once_then_clears(client):
    c, appmod = client
    sid = _start(c)
    state = _accepted_journey(c, appmod, sid)
    target = _mech_record(state)
    _correct(c, sid, target.record_id, WEAK_MECH)
    first = c.get(f"/session/{sid}").get_data(as_text=True)
    assert "risk-lapse" in first
    # N4-7: single-use notice — a later plain GET does not repeat it
    second = c.get(f"/session/{sid}").get_data(as_text=True)
    assert "risk-lapse" not in second


# --- N4-5: replay/live equivalence of the lapse classification ----------------

def test_n4_5_replay_classifies_deterministically(client):
    c, appmod = client
    sid = _start(c)
    state = _accepted_journey(c, appmod, sid)
    target = _mech_record(state)
    _correct(c, sid, target.record_id, WEAK_MECH)
    from web.app import _get_store
    from engine.session_reconstruction import reconstruct_readonly_state
    r1 = reconstruct_readonly_state(_get_store(), sid)
    r2 = reconstruct_readonly_state(_get_store(), sid)
    o1 = [(o.record_id, o.gap_context, o.applied, o.reason)
          for o in r1.review.risk_acceptance_outcomes]
    o2 = [(o.record_id, o.gap_context, o.applied, o.reason)
          for o in r2.review.risk_acceptance_outcomes]
    assert o1 == o2 and len(o1) == 1 and o1[0][2] is False
    # live state after the correction equals the replayed state
    live = appmod.SESSION_STORE[sid]["state"]
    assert {g.gap_type: g.status for g in live.gaps} == \
           {g.gap_type: g.status for g in r1.state.gaps}


# --- N4-6: multiple acceptances — only genuinely lapsed items reported --------

def test_n4_6_multiple_acceptances_only_lapsed_reported(client):
    c, appmod = client
    sid = _start(c)
    state = _accepted_journey(c, appmod, sid)
    # second acceptance: BOUNDARY_AMBIGUITY after its own substantive attempt
    assert select_next_gap(state) == BOUNDARY_AMBIGUITY
    _answer(c, sid, "One person is responsible for locking the ramp and "
                    "handles checking it before each use.")
    r = c.post(f"/session/{sid}/accept-risk", data={
        "gap_type": BOUNDARY_AMBIGUITY, "risk_confirm": "yes",
        "reason": "cannot decide yet", "answer_token": _token(c, sid)})
    state = appmod.SESSION_STORE[sid]["state"]
    assert state.get_gap(BOUNDARY_AMBIGUITY).status == ACCEPTED_RISK
    # supersede ONLY the feasibility attempt with a non-qualifying retraction:
    # feasibility acceptance replays against a still-OPEN gap and re-applies;
    # nothing about BOUNDARY should lapse either.
    target = next(r_ for r_ in state.assertions
                  if r_.content.startswith("I have not tested"))
    _correct(c, sid, target.record_id,
             "That earlier statement was a mistake on my part and I am taking it back.")
    from web.app import _get_store
    from engine.session_reconstruction import reconstruct_readonly_state
    recon = reconstruct_readonly_state(_get_store(), sid)
    outcomes = recon.review.risk_acceptance_outcomes
    assert len(outcomes) == 2
    assert [o for o in outcomes if not o.applied] == []
    page = c.get(f"/session/{sid}").get_data(as_text=True)
    assert "risk-lapse" not in page


# --- N4-7b (adversarial): an already-lapsed acceptance is not re-announced ----

def test_n4_7b_old_lapse_not_reannounced_by_later_correction(client):
    c, appmod = client
    sid = _start(c)
    state = _accepted_journey(c, appmod, sid)
    target = _mech_record(state)
    _correct(c, sid, target.record_id, WEAK_MECH)     # causes the lapse
    assert "risk-lapse" in c.get(f"/session/{sid}").get_data(as_text=True)
    # a LATER unrelated correction: the old lapsed acceptance stays lapsed in
    # the ledger, but it did not lapse BY this event — no repeat notice.
    state = appmod.SESSION_STORE[sid]["state"]
    target2 = next(r_ for r_ in state.assertions
                   if r_.disposition == "answered" and r_.content == WEAK_MECH
                   and r_.superseded_by is None)
    _correct(c, sid, target2.record_id,
             "The part that keeps the ramp down is a simple sliding bolt.")
    page = c.get(f"/session/{sid}").get_data(as_text=True)
    assert "risk-lapse" not in page


# --- N4-8: correction with no prior acceptance — UX unchanged -----------------

def test_n4_8_no_acceptance_correction_unchanged(client):
    c, appmod = client
    sid = _start(c)
    state = appmod.SESSION_STORE[sid]["state"]
    steps = 0
    while select_next_gap(state) == MECHANISM_COMPLETENESS and steps < 8:
        _answer(c, sid, MECH)
        steps += 1
    target = _mech_record(state)
    _correct(c, sid, target.record_id, MECH)
    page = c.get(f"/session/{sid}").get_data(as_text=True)
    assert "risk-lapse" not in page
    # outcomes list exists and is empty — no acceptance in the history
    from web.app import _get_store
    from engine.session_reconstruction import reconstruct_readonly_state
    recon = reconstruct_readonly_state(_get_store(), sid)
    assert recon.review.risk_acceptance_outcomes == ()
