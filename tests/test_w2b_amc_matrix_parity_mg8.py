"""W2-B / RVR-6a (amended contract) — serving-decision state-transition
matrix, reconstruction/reload parity, and the COMPLETE MG-8 diagnosis.

Authority: Contract Amendment 1 §9 (serving-decision matrix + parity
retained as mandatory evidence) and §13 (MG-8 diagnosis/measurement only —
real /start, durable seed, known_problem, idea_summary, both guards,
cause-vs-symptom, cold reconstruction, no semantic change).
"""
import copy
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import html as _html

import pytest

from engine.idea_state import (
    IdeaState, Gap, OPEN,
    MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY,
    DISPOSITION_ANSWERED,
)
from engine.progression_loop import (
    run_iteration, select_next_gap, accept_gap_risk,
    advance_after_disposition, compute_serving_decision,
    TRIGGER_COMPLETED_INTENT_SKIP, TRIGGER_MULTIPLE_ALTERNATIVES,
    _EXHAUSTED_EXIT_PROMPT,
)
from engine.adaptive_register import (
    compute_register, REGISTER_NEUTRAL, REGISTER_ELEVATED,
)
from engine.decision_composition import (
    declare_decision_context, declare_alternative,
)

SEED = ("a manually foldable wheelchair ramp for a home doorway — the "
        "inventor wants the ramp to stay reliably locked in the flat, "
        "load-bearing position and to fold away without tools")
REASONED_SEED = (SEED + " When the latch closes over the center rib, it "
                 "locks the panel so that the ramp stays rigid under load.")
MC_STRONG = ("(1) unfolding: the operator lifts the handle and the panel "
             "rotates on the hinge until flat. (2) locking: the toggle latch "
             "snaps over the center rib and holds the panel rigid. "
             "(3) folding: pressing the release lever frees the latch and the "
             "panel folds upward.")
PF_PLAIN = ("I have not tested whether the toggle latch stays reliable "
            "under repeated loading and outdoor use.")
WEAK = "i don't know"

# representative problem-prose seed corpus ([EXEC]-probed): most real
# problem statements carry no causal/structural/substance form
MG8_CORPUS_BELOW = (
    "People with wheelchairs cannot get over the doorway step at our home "
    "without another person helping them.",
    "My mother struggles every day to enter the house because of the raised "
    "threshold at the front door.",
    "Delivery workers keep tripping on the metal strip at the entrance and "
    "drop packages.",
    "The gap between the porch and the door frame makes wheelchair access "
    "impossible in winter.",
    "Children riding small bikes cannot cross the doorway sill and fall "
    "over frequently.",
)


def _fresh():
    s = IdeaState(idea_id="w2b-mat")
    s.domain = "software"
    s.domain_signal = "software"
    s.path = "N"
    s.gaps.append(Gap(MECHANISM_COMPLETENESS, OPEN, 0))
    return s


def _answer(state, content):
    targeted = select_next_gap(state)
    result = run_iteration(state, content)
    state.record_interaction(action=DISPOSITION_ANSWERED, content=content,
                             gap_context=targeted, iteration=state.iteration)
    return result


def _view(state):
    reg = compute_register(state)
    dec = compute_serving_decision(
        state, register_elevated=(reg.level == REGISTER_ELEVATED))
    return reg, dec


# --- serving-decision state-transition matrix ---------------------------------

def test_state_transition_matrix():
    """PRESTATE + latest event -> (canonical gap, register, override source,
    served override, primary action). Persistence column: derived only —
    verified by the purity/reload tests below."""
    s = _fresh()
    rows = []

    def snap(event):
        reg, dec = _view(s)
        rows.append((event, dec.served_gap, reg.level,
                     dec.question_override_source, dec.primary_action))

    snap("fresh")
    _answer(s, MC_STRONG); snap("strong#1")
    _answer(s, MC_STRONG); snap("strong#2")          # MC closes, PF opens
    _answer(s, PF_PLAIN);  snap("attempt#1")
    _answer(s, PF_PLAIN);  snap("attempt#2")
    _answer(s, PF_PLAIN);  snap("attempt#3")         # clamp -> skip override
    _answer(s, WEAK);      snap("weak#1")            # M=2 holds (hysteresis)
    _answer(s, WEAK);      snap("weak#2")            # register lowers
    ctx = declare_decision_context(s, "Which latch should hold?",
                                   iteration=s.iteration)
    declare_alternative(s, "toggle latch", ctx.record_id,
                        iteration=s.iteration)
    declare_alternative(s, "spring pin", ctx.record_id,
                        iteration=s.iteration)
    snap("alternatives-cross")                       # action slot fires
    _answer(s, PF_PLAIN);  snap("post-decision-answer")   # transition expires

    MC, PF = MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY
    SKIP = TRIGGER_COMPLETED_INTENT_SKIP
    from engine.progression_loop import TRIGGER_CRITICAL_UNRESOLVED as CRIT
    assert rows == [
        ("fresh",             MC, REGISTER_NEUTRAL,  None, None),
        ("strong#1",          MC, REGISTER_NEUTRAL,  None, None),
        ("strong#2",          PF, REGISTER_ELEVATED, None, None),
        ("attempt#1",         PF, REGISTER_ELEVATED, None, None),
        ("attempt#2",         PF, REGISTER_ELEVATED, None, None),
        # from the stall threshold on, PF is a stalled level-1 blocker: the
        # skip owns the slot while the register is ELEVATED (precedence),
        # and the critical reframe/exit serving truthfully remains once the
        # register lowers — the stalled blocker never regresses to verbatim
        # repeats
        ("attempt#3",         PF, REGISTER_ELEVATED, SKIP, None),
        ("weak#1",            PF, REGISTER_ELEVATED, SKIP, None),
        ("weak#2",            PF, REGISTER_NEUTRAL,  CRIT, None),
        ("alternatives-cross", PF, REGISTER_NEUTRAL, CRIT, "decision_refine"),
        ("post-decision-answer", PF, REGISTER_NEUTRAL, CRIT, None),
    ]
    # disposition transition: accept-risk reroutes, no override on fresh gap
    _answer(s, PF_PLAIN)                       # restore an active attempt
    accept_gap_risk(s, PHYSICAL_FEASIBILITY)
    advance_after_disposition(s)
    reg, dec = _view(s)
    assert dec.served_gap == BOUNDARY_AMBIGUITY
    assert dec.accepted_risk_gaps == (PHYSICAL_FEASIBILITY,)
    assert dec.question_override is None


def test_no_hidden_persisted_adaptive_state():
    s = _fresh()
    for content in (MC_STRONG, MC_STRONG, PF_PLAIN, PF_PLAIN, PF_PLAIN):
        _answer(s, content)
    before = set(s.__dict__.keys())
    _view(s); _view(s)
    assert set(s.__dict__.keys()) == before
    # reload equivalence: a deep copy (cold object) derives the same view
    assert _view(copy.deepcopy(s)) == _view(s)


# --- reconstruction parity (real durable journey) -----------------------------

@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("INVENTORAI_DB_PATH", str(tmp_path / "w2b-par.sqlite"))
    import web.app as appmod
    monkeypatch.setattr(appmod, "_STORE", None)
    appmod.SESSION_STORE.clear()
    appmod.app.config["TESTING"] = True
    with appmod.app.test_client() as c:
        yield c, appmod


def _wtoken(c, sid):
    page = c.get(f"/session/{sid}").get_data(as_text=True)
    m = re.search(r'name="answer_token" value="([^"]+)"', page)
    return _html.unescape(m.group(1))


def test_reconstruction_reproduces_serving_decision(client):
    c, appmod = client
    r = c.post("/start", data={"idea": SEED, "domain_confirm": "mechanical"})
    sid = r.headers["Location"].rsplit("/", 1)[-1]
    for content in (MC_STRONG, MC_STRONG, PF_PLAIN):
        c.post(f"/session/{sid}", data={
            "response": content, "answer_token": _wtoken(c, sid),
            "action": "answered"})
    c.post(f"/session/{sid}/decision/declare-context", data={
        "content": "Which latch should hold?",
        "answer_token": _wtoken(c, sid)})
    state = appmod.SESSION_STORE[sid]["state"]
    ctx_root = state.assertions[-1].record_id
    for alt in ("toggle latch", "spring pin"):
        c.post(f"/session/{sid}/decision/declare-alternative", data={
            "content": alt, "context_root": ctx_root,
            "answer_token": _wtoken(c, sid)})
    live = appmod.SESSION_STORE[sid]["state"]
    live_view = _view(live)
    assert live_view[1].primary_action == "decision_refine"

    from engine.session_reconstruction import reconstruct_readonly_state
    recon = reconstruct_readonly_state(appmod._get_store(), sid)
    assert recon.review.level == 1 and recon.state is not None
    assert _view(recon.state) == live_view


# --- MG-8 COMPLETE diagnosis (measurement only) -------------------------------

def test_mg8_pair_below_reasoned_seed(client):
    """The authoritative phenomenon PAIR through the REAL route: the seed is
    durably recorded at /start while known_problem (and idea_summary, same
    level-0 guard) stay unpopulated for a below-REASONED seed; the seed is
    never a ledger record. Measurement only — no semantics change."""
    c, appmod = client
    r = c.post("/start", data={"idea": SEED, "domain_confirm": "mechanical"})
    sid = r.headers["Location"].rsplit("/", 1)[-1]
    inputs = appmod._get_store().load_reconstruction_inputs(sid)
    assert inputs["seed_idea_text"] == SEED            # durable half
    state = appmod.SESSION_STORE[sid]["state"]
    assert state.known_problem is None                 # unpopulated half
    assert state.idea_summary is None                  # same-guard symptom
    assert state.assertions == []                      # never a ledger record
    # cold reconstruction reproduces the pair deterministically
    from engine.session_reconstruction import reconstruct_readonly_state
    recon = reconstruct_readonly_state(appmod._get_store(), sid)
    assert recon.review.level == 1
    assert recon.state.known_problem is None


def test_mg8_reasoned_control(client):
    c, appmod = client
    r = c.post("/start", data={"idea": REASONED_SEED,
                               "domain_confirm": "mechanical"})
    sid = r.headers["Location"].rsplit("/", 1)[-1]
    inputs = appmod._get_store().load_reconstruction_inputs(sid)
    assert inputs["seed_idea_text"] == REASONED_SEED
    state = appmod.SESSION_STORE[sid]["state"]
    assert state.known_problem is not None             # capture-gated,
    assert state.idea_summary is not None              # not storage-gated


def test_mg8_conjunct_isolation():
    """Cause isolation: the SEED path is the level-0 branch whose guard is
    `quality >= REASONED` ALONE (no relevance conjunct); the sibling in-gap
    guard additionally requires relevance. Both measured through the real
    engine paths."""
    # level-0 branch (gapless state): quality gate only
    s = IdeaState(idea_id="mg8-a")
    s.domain = "mechanical"; s.domain_signal = "mechanical"; s.path = "N"
    run_iteration(s, SEED)                    # ASSERTED -> not captured
    assert s.known_problem is None
    s2 = IdeaState(idea_id="mg8-b")
    s2.domain = "mechanical"; s2.domain_signal = "mechanical"; s2.path = "N"
    run_iteration(s2, REASONED_SEED)          # REASONED -> captured
    assert s2.known_problem is not None
    # sibling in-gap guard: REASONED but NOT addressing the served gap ->
    # not captured (relevance conjunct)
    s3 = IdeaState(idea_id="mg8-c")
    s3.domain = "mechanical"; s3.domain_signal = "mechanical"; s3.path = "N"
    s3.gaps.append(Gap(MECHANISM_COMPLETENESS, OPEN, 0))
    off_gap = ("(1) pricing: the subscription tier structure follows the "
               "regional purchasing-power distribution. (2) marketing: the "
               "campaign sequencing follows the seasonal demand cycle. "
               "(3) partnerships: the distribution agreements follow the "
               "retailer certification timeline.")
    run_iteration(s3, off_gap)
    assert s3.known_problem is None


def test_mg8_cause_vs_symptom_corpus_probe():
    """Proximate cause: representative problem prose rarely carries the
    causal/structural/substance form the quality gate requires — the pair
    is the RULE for problem-shaped seeds, not an edge case."""
    from engine.progression_loop import assess_response
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        tiers = [assess_response(t, "mechanical") for t in MG8_CORPUS_BELOW]
    assert tiers.count("ASSERTED") == len(MG8_CORPUS_BELOW)
