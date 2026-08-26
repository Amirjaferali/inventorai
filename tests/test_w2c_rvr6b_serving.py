"""W2-C / RVR-6b — the intent-coverage serving law (suppression + within-gap
ordering + decision-aware deference), determinism, and reconstruction parity.

The law under test (contract §F.2-§F.5): canonical uncovered → inert;
canonical covered → next later uncovered, else earliest uncovered (recovery),
else inert (all covered — the governed clamp/reframe/exit machinery is never
overridden). Deference: while the W2-B alternatives transition is active the
question slot stays canonical. select_next_gap is never consulted, promoted,
or bypassed — everything happens inside the one served gap."""
import pytest

import engine.intent_serving as intent_serving
from engine.intent_serving import (
    compute_intent_coverage, w2c_served_question, supplemental_relevance,
)
from engine.idea_state import IdeaState, Gap, OPEN, DISPOSITION_ANSWERED
from engine.decision_composition import declare_decision_context, declare_alternative

MECH = "mechanical"
MC = "MECHANISM_COMPLETENESS"
Q1 = "mechanical:MECHANISM_COMPLETENESS:Q1"
Q2 = "mechanical:MECHANISM_COMPLETENESS:Q2"
Q3 = "mechanical:MECHANISM_COMPLETENESS:Q3"
Q4 = "mechanical:MECHANISM_COMPLETENESS:Q4"

# answers carrying each variant's committed intent vocabulary
COVERS_Q1 = "The physical steps are: unfold, lock, roll."
COVERS_Q2 = "The force path runs through the hinge line into the latch."
COVERS_Q3 = "Each component contributes to the overall motion of the ramp."
NEUTRAL = "I will have to think about that for a while."


@pytest.fixture(autouse=True)
def _fresh_cache(monkeypatch):
    monkeypatch.setattr(intent_serving, "_REGISTRY_CACHE", {})


def _state(iters=0):
    s = IdeaState(idea_id="w2c-serve")
    s.domain = MECH
    s.path = "N"
    s.gaps.append(Gap(gap_type=MC, status=OPEN, opened_at=0,
                      iterations_open=iters))
    return s


def _answered(state, content, gap=MC):
    return state.record_interaction(action=DISPOSITION_ANSWERED,
                                    content=content, gap_context=gap)


def test_uncovered_canonical_variant_is_inert():
    s = _state(iters=0)
    _answered(s, NEUTRAL)
    assert w2c_served_question(s, MC) is None


def test_covered_canonical_variant_is_suppressed_forward():
    # canonical index 1 = Q2; a recorded answer already carries Q2's intent
    s = _state(iters=1)
    _answered(s, COVERS_Q2)
    served = w2c_served_question(s, MC)
    assert served is not None and served.question_id == Q3


def test_recovery_serves_earliest_uncovered_when_forward_exhausted():
    # canonical index 3 = Q4 covered; Q3 covered; Q1 uncovered -> recover Q1
    s = _state(iters=3)
    _answered(s, COVERS_Q3)
    _answered(s, "If someone built it tomorrow the missing detail would be the latch preload.")
    served = w2c_served_question(s, MC)
    # canonical Q4 covered ("would be missing"/"missing detail"); forward none;
    # earliest uncovered is Q1 (Q2 uncovered too but Q1 earlier... unless Q1
    # matched). COVERS_Q3 does not carry Q1/Q2 vocabulary.
    assert served is not None and served.question_id in (Q1, Q2)
    assert served.question_id == Q1


def test_all_covered_is_inert_canonical_clamp_governs():
    s = _state(iters=2)
    _answered(s, COVERS_Q1)
    _answered(s, COVERS_Q2)
    _answered(s, COVERS_Q3)
    _answered(s, "The missing detail would be the exact spring preload value.")
    assert w2c_served_question(s, MC) is None


def test_coverage_state_is_derived_and_reversible():
    s = _state(iters=1)
    rec = _answered(s, COVERS_Q2)
    assert Q2 in compute_intent_coverage(s, MC)
    # superseding the contributing record recomputes coverage — nothing latched
    rec.superseded_by = "rec_999"
    assert Q2 not in compute_intent_coverage(s, MC)


def test_determinism_same_state_same_result():
    s = _state(iters=1)
    _answered(s, COVERS_Q2)
    first = w2c_served_question(s, MC)
    second = w2c_served_question(s, MC)
    assert first == second


def test_ledger_insertion_order_is_irrelevant():
    s = _state(iters=1)
    _answered(s, NEUTRAL)
    _answered(s, COVERS_Q2)
    s.assertions.reverse()  # canonical rec_N order must be reconstructed
    served = w2c_served_question(s, MC)
    assert served is not None and served.question_id == Q3


def test_reconstruction_parity_rebuilt_state_identical():
    def build():
        s = _state(iters=1)
        _answered(s, COVERS_Q2)
        return s
    a, b = build(), build()
    assert w2c_served_question(a, MC) == w2c_served_question(b, MC)
    assert compute_intent_coverage(a, MC) == compute_intent_coverage(b, MC)


def test_decision_alternatives_transition_defers_to_canonical():
    # same covered-canonical state as the suppression test, but the LATEST
    # ledger record is a second active alternative declaration (the W2-B
    # trigger-3 true transition) -> the question slot stays canonical
    s = _state(iters=1)
    _answered(s, COVERS_Q2)
    ctx = declare_decision_context(s, "Which latch design should hold?")
    declare_alternative(s, "toggle latch", ctx.record_id)
    declare_alternative(s, "spring pin", ctx.record_id)
    assert w2c_served_question(s, MC) is None
    # and the deference ends with the next record (transition expires)
    _answered(s, NEUTRAL)
    served = w2c_served_question(s, MC)
    assert served is not None and served.question_id == Q3


def test_artifactless_domain_is_inert():
    s = _state(iters=1)
    s.domain = "software"
    _answered(s, COVERS_Q2)
    assert w2c_served_question(s, MC) is None
    assert compute_intent_coverage(s, MC) is None


def test_registry_failure_is_inert(monkeypatch):
    monkeypatch.setitem(
        intent_serving._DOMAIN_REGISTRY_FILES, MECH,
        ("docs/governance/path_n_content_config/does_not_exist.json",
         intent_serving._DOMAIN_REGISTRY_FILES[MECH][1]))
    s = _state(iters=1)
    _answered(s, COVERS_Q2)
    assert w2c_served_question(s, MC) is None
    assert supplemental_relevance(s, MC, COVERS_Q2) is False


def test_no_gap_and_malformed_gap_fail_closed():
    s = IdeaState(idea_id="w2c-nogap")
    s.domain = MECH
    s.path = "N"
    assert w2c_served_question(s, MC) is None            # gap absent -> iters 0, inert
    assert w2c_served_question(s, "NOT_A_GAP") is None   # unmapped gap type
    assert supplemental_relevance(s, "NOT_A_GAP", COVERS_Q2) is False


def test_select_next_gap_is_never_consulted(monkeypatch):
    # ownership fence: the W2-C law must not read or influence canonical gap
    # selection — poisoning select_next_gap must not change the result
    import engine.progression_loop as pl
    def _boom(*a, **k):
        raise AssertionError("W2-C consulted select_next_gap")
    monkeypatch.setattr(pl, "select_next_gap", _boom)
    s = _state(iters=1)
    _answered(s, COVERS_Q2)
    served = w2c_served_question(s, MC)
    assert served is not None and served.question_id == Q3


def test_serving_result_is_a_committed_variant_never_generated_text():
    from engine.path_n_questions import get_served_question
    s = _state(iters=1)
    _answered(s, COVERS_Q2)
    served = w2c_served_question(s, MC)
    committed = {get_served_question(MC, i, domain=MECH).text for i in range(4)}
    assert served.text in committed
