"""Wave-2 W2-D — W1-S2 substantive-attempt gate (live Accept Risk availability).

Contract: docs/governance/WAVE_2_BOUNDED_IMPLEMENTATION_CONTRACT_CANDIDATE.md §F
(authoritative via PR #563 merge 58e92e09). The live Accept Risk affordance and
route become available for the currently served eligible gap ONLY when at least
one ACTIVE ledger record satisfies the canonical active-set rule:
  superseded_by is None  AND  disposition == answered  AND
  gap_context == served gap  AND  content not weak/refusal  AND
  addresses_gap(content, gap_type) is True.
A superseded/withdrawn attempt does NOT satisfy the gate. The gate is a LIVE
availability policy only: the canonical writer `accept_gap_risk` is unchanged
and historical accepted-risk ledgers still reconstruct identically.
"""
import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

from engine.idea_state import (
    IdeaState, Gap, OPEN, PARTIAL, ACCEPTED_RISK,
    MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY,
    DISPOSITION_RISK_ACCEPTED,
)
from engine.progression_loop import (
    select_next_gap, substantive_attempt_recorded,
)
from engine.gap_relevance import addresses_gap


# --- shared journey material (same frozen-corpus material as the RVR-1 suite) --

SEED = ("a manually foldable wheelchair ramp for a home doorway — the inventor "
        "wants the ramp to stay reliably locked in the flat, load-bearing "
        "position and to fold away without tools")
MECH = ("The ramp folds up and down by hand. When it is down flat, it must "
        "stay firmly held so a wheelchair can roll over it. I am considering "
        "three ways to hold it: a toggle latch that snaps over its center, a "
        "spring pin that clicks into place, or a small gate piece that drops "
        "into place by its own weight.")
# Substantive-but-unresolved attempt: relevant to PHYSICAL_FEASIBILITY (proven
# [EXEC]), assessed ASSERTED, leaves the gap OPEN/PARTIAL and still served.
FEAS_ATTEMPT = ("I have not tested whether the toggle latch stays reliable "
                "under repeated loading and outdoor use.")
# Known-adversarial stuffing fixture (W1-N1 class): hyphenated buzzwords with
# no feasibility-family content — must never unlock Accept Risk.
STUFFING = ("state-of-the-art sensor-fusion next-generation "
            "performance-optimized architecture-driven market-leading "
            "solution platform")
# Generic filler — dodges the exact weak-pattern match but has no relevance.
FILLER = "maybe there is something we could try somehow with the general approach"
# W1-N3-class legitimate false-negative fixture: genuine technical content the
# lexical relevance family does not recognize; the gate must FAIL SAFE.
FALSE_NEGATIVE = ("The latch bracket was machined from 6061-T6 and torque "
                  "specs were confirmed on the bench.")
# Correction replacement that must NOT itself qualify (no family words).
RETRACTION = "That earlier statement was a mistake on my part and I am taking it back."


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("INVENTORAI_DB_PATH", str(tmp_path / "w2d.sqlite"))
    import web.app as appmod
    monkeypatch.setattr(appmod, "_STORE", None)
    appmod.SESSION_STORE.clear()
    appmod.app.config["TESTING"] = True
    with appmod.app.test_client() as c:
        yield c, appmod


def _start(c):
    r = c.post("/start", data={"idea": SEED, "domain_confirm": "mechanical"})
    assert r.status_code == 302 and "/session/" in r.headers["Location"]
    return r.headers["Location"].rsplit("/", 1)[-1]


def _token(c, sid):
    import re, html
    page = c.get(f"/session/{sid}").get_data(as_text=True)
    m = re.search(r'name="answer_token" value="([^"]+)"', page)
    return html.unescape(m.group(1))


def _answer(c, sid, text):
    return c.post(f"/session/{sid}", data={
        "response": text, "answer_token": _token(c, sid), "action": "answered"})


def _close_mech(c, appmod, sid, max_steps=8):
    state = appmod.SESSION_STORE[sid]["state"]
    steps = 0
    while select_next_gap(state) == MECHANISM_COMPLETENESS and steps < max_steps:
        _answer(c, sid, MECH)
        steps += 1
    assert select_next_gap(state) == PHYSICAL_FEASIBILITY


def _accept(c, sid, gap):
    return c.post(f"/session/{sid}/accept-risk", data={
        "gap_type": gap, "risk_confirm": "yes", "reason": "cannot verify yet",
        "answer_token": _token(c, sid)})


def _page(c, sid):
    return c.get(f"/session/{sid}").get_data(as_text=True)


# --- fixture sanity guards (protect the test vectors themselves) --------------

def test_fixture_vectors_hold():
    assert addresses_gap(FEAS_ATTEMPT, PHYSICAL_FEASIBILITY) is True
    assert addresses_gap(STUFFING, PHYSICAL_FEASIBILITY) is False
    assert addresses_gap(FILLER, PHYSICAL_FEASIBILITY) is False
    assert addresses_gap(MECH, PHYSICAL_FEASIBILITY) is False
    assert addresses_gap(FALSE_NEGATIVE, PHYSICAL_FEASIBILITY) is False
    assert addresses_gap(RETRACTION, PHYSICAL_FEASIBILITY) is False


# --- helper semantics (pure, deterministic, active-set rule) ------------------

def _rec(state, content, gap, superseded=None):
    r = state.record_interaction(action="answered", content=content,
                                 gap_context=gap, iteration=1)
    if superseded:
        r.superseded_by = superseded
    return r

def test_helper_active_set_rule():
    s = IdeaState(idea_id="x")
    s.gaps.append(Gap(gap_type=PHYSICAL_FEASIBILITY, status=OPEN, opened_at=1))
    assert substantive_attempt_recorded(s, PHYSICAL_FEASIBILITY) is False
    # weak/refusal exact forms never qualify
    _rec(s, "I don't know", PHYSICAL_FEASIBILITY)
    _rec(s, "n/a", PHYSICAL_FEASIBILITY)
    assert substantive_attempt_recorded(s, PHYSICAL_FEASIBILITY) is False
    # irrelevant content never qualifies
    _rec(s, FILLER, PHYSICAL_FEASIBILITY)
    _rec(s, STUFFING, PHYSICAL_FEASIBILITY)
    assert substantive_attempt_recorded(s, PHYSICAL_FEASIBILITY) is False
    # a qualifying attempt for ANOTHER gap does not leak
    _rec(s, FEAS_ATTEMPT, BOUNDARY_AMBIGUITY)
    assert substantive_attempt_recorded(s, PHYSICAL_FEASIBILITY) is False
    # an active substantive relevant attempt qualifies
    q = _rec(s, FEAS_ATTEMPT, PHYSICAL_FEASIBILITY)
    assert substantive_attempt_recorded(s, PHYSICAL_FEASIBILITY) is True
    # a superseded attempt does NOT satisfy the gate
    q.superseded_by = "rec_99"
    assert substantive_attempt_recorded(s, PHYSICAL_FEASIBILITY) is False

def test_helper_is_deterministic_and_readonly():
    s = IdeaState(idea_id="x")
    s.gaps.append(Gap(gap_type=PHYSICAL_FEASIBILITY, status=OPEN, opened_at=1))
    _rec(s, FEAS_ATTEMPT, PHYSICAL_FEASIBILITY)
    before = [(r.record_id, r.superseded_by, r.content) for r in s.assertions]
    assert all(substantive_attempt_recorded(s, PHYSICAL_FEASIBILITY)
               for _ in range(3))
    assert [(r.record_id, r.superseded_by, r.content) for r in s.assertions] == before


# --- S2-1: no attempt → affordance hidden AND direct route rejected -----------

def test_s2_1_no_attempt_unavailable(client):
    c, appmod = client
    sid = _start(c)
    _close_mech(c, appmod, sid)
    state = appmod.SESSION_STORE[sid]["state"]
    # UI affordance hidden
    assert "/accept-risk" not in _page(c, sid)
    # direct route invocation rejected safely, nothing durable, nothing moved
    _accept(c, sid, PHYSICAL_FEASIBILITY)
    assert state.get_gap(PHYSICAL_FEASIBILITY).status in (OPEN, PARTIAL)
    assert [r for r in state.assertions
            if r.disposition == DISPOSITION_RISK_ACCEPTED] == []


# --- S2-2/S2-3/S2-4/S2-5: junk never unlocks ----------------------------------

@pytest.mark.parametrize("junk", ["I don't know", "n/a", FILLER, MECH, STUFFING])
def test_s2_2345_junk_never_unlocks(client, junk):
    c, appmod = client
    sid = _start(c)
    _close_mech(c, appmod, sid)
    state = appmod.SESSION_STORE[sid]["state"]
    _answer(c, sid, junk)
    assert select_next_gap(state) == PHYSICAL_FEASIBILITY
    assert "/accept-risk" not in _page(c, sid)
    _accept(c, sid, PHYSICAL_FEASIBILITY)
    assert state.get_gap(PHYSICAL_FEASIBILITY).status in (OPEN, PARTIAL)
    assert [r for r in state.assertions
            if r.disposition == DISPOSITION_RISK_ACCEPTED] == []


# --- S2-6: a legitimate concise relevant attempt unlocks ----------------------

def test_s2_6_legitimate_attempt_unlocks(client):
    c, appmod = client
    sid = _start(c)
    _close_mech(c, appmod, sid)
    state = appmod.SESSION_STORE[sid]["state"]
    _answer(c, sid, FEAS_ATTEMPT)
    assert select_next_gap(state) == PHYSICAL_FEASIBILITY
    # UI and route agree: affordance shown, acceptance succeeds
    assert "/accept-risk" in _page(c, sid)
    _accept(c, sid, PHYSICAL_FEASIBILITY)
    assert state.get_gap(PHYSICAL_FEASIBILITY).status == ACCEPTED_RISK


# --- S2-7/S2-8: correction removes eligibility; a new attempt restores it -----

def test_s2_78_supersession_removes_then_new_attempt_restores(client):
    c, appmod = client
    sid = _start(c)
    _close_mech(c, appmod, sid)
    state = appmod.SESSION_STORE[sid]["state"]
    _answer(c, sid, FEAS_ATTEMPT)
    assert substantive_attempt_recorded(state, PHYSICAL_FEASIBILITY) is True
    assert "/accept-risk" in _page(c, sid)
    target = next(r for r in state.assertions if r.content == FEAS_ATTEMPT)
    r = c.post(f"/session/{sid}/correct", data={
        "supersedes_record_id": target.record_id, "response": RETRACTION,
        "answer_token": _token(c, sid)})
    assert r.status_code == 302
    state = appmod.SESSION_STORE[sid]["state"]   # atomic replacement
    # the prior attempt is superseded and the retraction does not qualify
    assert select_next_gap(state) == PHYSICAL_FEASIBILITY
    assert substantive_attempt_recorded(state, PHYSICAL_FEASIBILITY) is False
    assert "/accept-risk" not in _page(c, sid)
    _accept(c, sid, PHYSICAL_FEASIBILITY)
    assert state.get_gap(PHYSICAL_FEASIBILITY).status in (OPEN, PARTIAL)
    # a NEW qualifying active attempt restores availability
    _answer(c, sid, FEAS_ATTEMPT)
    state = appmod.SESSION_STORE[sid]["state"]
    assert substantive_attempt_recorded(state, PHYSICAL_FEASIBILITY) is True
    assert "/accept-risk" in _page(c, sid)
    _accept(c, sid, PHYSICAL_FEASIBILITY)
    assert state.get_gap(PHYSICAL_FEASIBILITY).status == ACCEPTED_RISK


# --- S2-9: historical replay unchanged (gate is live-only) --------------------

def test_s2_9_historical_accepted_risk_ledger_reconstructs(client):
    """A durable history whose acceptance was recorded is reconstructed with
    the acceptance applied — the availability gate governs NEW live actions
    only and lives outside the canonical writer/replay."""
    c, appmod = client
    sid = _start(c)
    _close_mech(c, appmod, sid)
    _answer(c, sid, FEAS_ATTEMPT)
    _accept(c, sid, PHYSICAL_FEASIBILITY)
    state = appmod.SESSION_STORE[sid]["state"]
    assert state.get_gap(PHYSICAL_FEASIBILITY).status == ACCEPTED_RISK
    from web.app import _get_store
    from engine.session_reconstruction import reconstruct_readonly_state
    recon = reconstruct_readonly_state(_get_store(), sid)
    assert recon.review.level == 1
    assert recon.state.get_gap(PHYSICAL_FEASIBILITY).status == ACCEPTED_RISK
    # and the replay applied (did not lapse) the recorded acceptance
    outcomes = recon.review.risk_acceptance_outcomes
    assert [o for o in outcomes if not o.applied] == []
    assert len([o for o in outcomes if o.applied]) == 1


# --- S2-10: W1-N3-class false negative fails SAFE -----------------------------

def test_s2_10_false_negative_fails_safe(client):
    c, appmod = client
    sid = _start(c)
    _close_mech(c, appmod, sid)
    state = appmod.SESSION_STORE[sid]["state"]
    _answer(c, sid, FALSE_NEGATIVE)
    # fail-safe: the legitimate-but-unrecognized attempt does not unlock;
    # the truthful exits remain (the non-answer actions are still rendered)
    assert "/accept-risk" not in _page(c, sid)
    _accept(c, sid, PHYSICAL_FEASIBILITY)
    assert state.get_gap(PHYSICAL_FEASIBILITY).status in (OPEN, PARTIAL)
    page = _page(c, sid)
    assert 'name="action"' in page  # the governed non-answer exits still render


# --- single live availability policy ------------------------------------------

def test_single_availability_policy_source():
    """Exactly one live availability policy: the route and the template both
    consume `substantive_attempt_recorded` (no second predicate)."""
    import inspect, web.app as appmod
    src = inspect.getsource(appmod.accept_risk)
    assert "substantive_attempt_recorded" in src
    show = inspect.getsource(appmod.show_session)
    assert "substantive_attempt_recorded" in show
    with open(os.path.join(os.path.dirname(__file__), "..",
                           "web", "templates", "session.html"),
              encoding="utf-8") as f:
        tpl = f.read()
    assert "risk_available" in tpl
