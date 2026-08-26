"""W2-B / RVR-6a (amended contract) — trigger 3:
`multiple_decision_alternatives_declared` as a TRUE ledger transition, and
the FDC-001 hard fence.

Authority: Contract Amendment 1 §5 row 3 / §7 (authoritative via PR #575).
The trigger is the crossing (active alternatives < 2 → >= 2) attributable to
the latest ledger event — never a standing `count >= 2` predicate, never a
comparability claim, no persisted fired-state, idempotent on idle re-render.
FDC-001 (`engine/decision_workspace.py`) remains the sole owner of decision
comparability/readiness; `len(active_alternatives) >= 2` is never a
comparability proxy; no rendered page may contradict FDC-001 truth.
"""
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import html as _html

import pytest

from engine.idea_state import (
    IdeaState, Gap, OPEN, MECHANISM_COMPLETENESS, DISPOSITION_ANSWERED,
)
from engine.progression_loop import (
    compute_serving_decision, TRIGGER_MULTIPLE_ALTERNATIVES,
    _alternatives_crossing_context,
)
from engine.decision_composition import (
    declare_decision_context, declare_alternative, refine_alternative,
    withdraw_alternative, compose_decision_records,
)
from engine.decision_workspace import INSUFFICIENT_INFORMATION
from web import ui_text

SEED = ("a manually foldable wheelchair ramp for a home doorway — the "
        "inventor wants the ramp to stay reliably locked in the flat, "
        "load-bearing position and to fold away without tools")


def _state():
    s = IdeaState(idea_id="w2b-dec")
    s.domain = "software"
    s.domain_signal = "software"
    s.path = "N"
    s.gaps.append(Gap(MECHANISM_COMPLETENESS, OPEN, 0))
    return s


# --- the TRUE transition ------------------------------------------------------

def test_crossing_fires_exactly_at_second_alternative():
    s = _state()
    ctx = declare_decision_context(s, "Which latch design should hold?")
    assert _alternatives_crossing_context(s) is None
    declare_alternative(s, "toggle latch", ctx.record_id)
    assert _alternatives_crossing_context(s) is None       # count 1: no fire
    declare_alternative(s, "spring pin", ctx.record_id)
    assert _alternatives_crossing_context(s) is not None   # 1 -> 2: FIRES
    d = compute_serving_decision(s, register_elevated=False)
    assert TRIGGER_MULTIPLE_ALTERNATIVES in d.triggers
    assert d.primary_action == "decision_refine"
    # the question slot is untouched by the action-slot trigger
    assert d.question_override is None


def test_third_alternative_is_not_newly():
    s = _state()
    ctx = declare_decision_context(s, "Which latch design should hold?")
    declare_alternative(s, "toggle latch", ctx.record_id)
    declare_alternative(s, "spring pin", ctx.record_id)
    declare_alternative(s, "gravity gate", ctx.record_id)  # 2 -> 3
    assert _alternatives_crossing_context(s) is None
    d = compute_serving_decision(s, register_elevated=False)
    assert TRIGGER_MULTIPLE_ALTERNATIVES not in d.triggers
    assert d.primary_action is None


def test_refine_does_not_re_fire():
    s = _state()
    ctx = declare_decision_context(s, "Which latch design should hold?")
    declare_alternative(s, "toggle latch", ctx.record_id)
    alt2 = declare_alternative(s, "spring pin", ctx.record_id)
    refine_alternative(s, "spring pin with detent", alt2.record_id)
    assert _alternatives_crossing_context(s) is None       # 2 -> 2


def test_withdrawal_reverses_and_redeclare_fires_again():
    s = _state()
    ctx = declare_decision_context(s, "Which latch design should hold?")
    declare_alternative(s, "toggle latch", ctx.record_id)
    alt2 = declare_alternative(s, "spring pin", ctx.record_id)
    withdraw_alternative(s, alt2.record_id, "not viable")
    assert _alternatives_crossing_context(s) is None       # withdrawal event
    declare_alternative(s, "gravity gate", ctx.record_id)  # 1 -> 2 again
    assert _alternatives_crossing_context(s) is not None


def test_transition_expires_after_the_next_ledger_event():
    """No persisted fired-state: the transition is 'the latest ledger event
    crossed <2 -> >=2'. Any subsequent record ends it deterministically."""
    s = _state()
    ctx = declare_decision_context(s, "Which latch design should hold?")
    declare_alternative(s, "toggle latch", ctx.record_id)
    declare_alternative(s, "spring pin", ctx.record_id)
    assert _alternatives_crossing_context(s) is not None
    s.record_interaction(action=DISPOSITION_ANSWERED, content="more detail",
                         gap_context=MECHANISM_COMPLETENESS)
    assert _alternatives_crossing_context(s) is None
    d = compute_serving_decision(s, register_elevated=False)
    assert d.primary_action is None


def test_idle_re_render_is_idempotent():
    s = _state()
    ctx = declare_decision_context(s, "Which latch design should hold?")
    declare_alternative(s, "toggle latch", ctx.record_id)
    declare_alternative(s, "spring pin", ctx.record_id)
    first = compute_serving_decision(s, register_elevated=False)
    for _ in range(4):                     # unchanged ledger snapshot
        assert compute_serving_decision(s, register_elevated=False) == first
    assert first.primary_action == "decision_refine"


# --- FDC-001 hard fence -------------------------------------------------------

def test_two_alternatives_remain_insufficient_information():
    """The canonical owner's truth: two active alternatives WITHOUT covered
    comparison context stay `insufficient_information` — and every W2-B
    computation leaves that readiness byte-unchanged."""
    s = _state()
    ctx = declare_decision_context(s, "Which latch design should hold?")
    declare_alternative(s, "toggle latch", ctx.record_id)
    declare_alternative(s, "spring pin", ctx.record_id)
    records = compose_decision_records(s)
    assert len(records) == 1
    assert records[0].readiness_status == INSUFFICIENT_INFORMATION
    compute_serving_decision(s, register_elevated=False)
    compute_serving_decision(s, register_elevated=True)
    assert compose_decision_records(s)[0].readiness_status \
        == INSUFFICIENT_INFORMATION


def test_no_comparability_claim_in_any_w2b_string():
    """No W2-B catalogue string may claim comparability/readiness — that
    truth belongs to FDC-001 alone. The action text explicitly states no
    comparison has started."""
    w2b_keys = [k for k in ui_text.UI_STRINGS if k.startswith("UI_W2B")]
    assert w2b_keys, "W2-B catalogue entries missing"
    for key in w2b_keys:
        en = ui_text.UI_STRINGS[key]["en"].lower()
        # the ban is on POSITIVE claims; the explicit negation
        # "no comparison has started" is the required disclosure
        en_wo_negation = en.replace("no comparison has started", "")
        for forbidden in ("are comparable", "now comparable",
                          "ready to compare", "comparison has started",
                          "comparison started"):
            assert forbidden not in en_wo_negation, (key, forbidden)
    action = ui_text.UI_STRINGS["UI_W2B_ACTION_DECISION_EVIDENCE"]["en"]
    assert "No comparison has started" in action


def test_engine_has_no_len2_comparability_proxy():
    """The transition helper is a crossing detector over declared
    alternatives; nothing in the W2-B engine surface DEFINES a
    comparability identifier, function, or verdict — the stem may appear
    only in prose stating FDC-001's exclusive ownership."""
    root = os.path.join(os.path.dirname(__file__), "..")
    ident = re.compile(r"(def\s+\w*comparab|\bcomparab\w*\s*=|"
                       r"['\"]comparab)", re.IGNORECASE)
    for rel in ("engine/adaptive_register.py", "engine/progression_loop.py"):
        src = open(os.path.join(root, rel), encoding="utf-8").read()
        assert not ident.search(src), rel


# --- web journey: real action-slot consequence with truthful page ------------

@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("INVENTORAI_DB_PATH", str(tmp_path / "w2b-dec.sqlite"))
    import web.app as appmod
    monkeypatch.setattr(appmod, "_STORE", None)
    appmod.SESSION_STORE.clear()
    appmod.app.config["TESTING"] = True
    with appmod.app.test_client() as c:
        yield c, appmod


def _token(c, sid):
    page = c.get(f"/session/{sid}").get_data(as_text=True)
    m = re.search(r'name="answer_token" value="([^"]+)"', page)
    return _html.unescape(m.group(1))


def _page(c, sid):
    return _html.unescape(c.get(f"/session/{sid}").get_data(as_text=True))


def test_web_transition_serves_action_block_once_then_expires(client):
    c, appmod = client
    r = c.post("/start", data={"idea": SEED, "domain_confirm": "mechanical"})
    sid = r.headers["Location"].rsplit("/", 1)[-1]
    r = c.post(f"/session/{sid}/decision/declare-context", data={
        "content": "Which latch design should hold the ramp?",
        "answer_token": _token(c, sid)})
    assert r.status_code == 302
    state = appmod.SESSION_STORE[sid]["state"]
    ctx_root = state.assertions[-1].record_id
    action_text = ui_text.UI_STRINGS["UI_W2B_ACTION_DECISION_EVIDENCE"]["en"]
    assert action_text not in _page(c, sid)
    c.post(f"/session/{sid}/decision/declare-alternative", data={
        "content": "toggle latch", "context_root": ctx_root,
        "answer_token": _token(c, sid)})
    assert action_text not in _page(c, sid)          # one alternative: no fire
    c.post(f"/session/{sid}/decision/declare-alternative", data={
        "content": "spring pin", "context_root": ctx_root,
        "answer_token": _token(c, sid)})
    page = _page(c, sid)
    assert action_text in page                        # the crossing fires
    assert 'href="#w2b-decision-capture"' in page     # real governed action
    assert "w2b-primary-action" in page
    # the W2-A readiness note still renders its FDC-001 truth on the SAME
    # page with no contradiction
    assert ui_text.UI_STRINGS["UI_W2A_READINESS_NOTE"]["en"] in page
    assert "now comparable" not in page.lower()
    # idle re-render: still deterministic (same ledger -> same page state)
    assert action_text in _page(c, sid)
    # the next governed interaction ends the transition
    c.post(f"/session/{sid}", data={
        "response": "The latch bar rides over the center rib when closed.",
        "answer_token": _token(c, sid), "action": "answered"})
    assert action_text not in _page(c, sid)
