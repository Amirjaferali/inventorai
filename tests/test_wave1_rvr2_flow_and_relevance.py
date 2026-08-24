"""Wave-1 RVR-2 — Question-flow dead-end removal + relevance re-derivation.

Contract: docs/governance/WAVE_1_REMEDIATION_IMPLEMENTATION_CONTRACTS.md (RVR-2).
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from engine.progression_loop import (
    get_display_question, get_question, _STALL_REFRAME, _EXHAUSTED_EXIT_PROMPT,
)
from engine.path_n_questions import get_path_n_question
from engine.gap_relevance import addresses_gap
from engine.idea_state import (
    MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY,
)

_STAGE2 = (MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY)

def _variant_count(gap, domain):
    n = 0
    while True:
        q = get_path_n_question(gap, n, domain=domain)
        if q is None:
            return n
        if n and q == get_path_n_question(gap, n - 1, domain=domain):
            return n
        n += 1

def test_reframe_served_exactly_once_then_exit_prompt_both_domains():
    for domain in ("electronics_electrical", "mechanical"):
        for gap in _STAGE2:
            n = _variant_count(gap, domain)
            assert get_display_question(domain, gap, n, path="N") == _STALL_REFRAME
            for i in (n + 1, n + 2, n + 10):
                q = get_display_question(domain, gap, i, path="N")
                assert q == _EXHAUSTED_EXIT_PROMPT, (domain, gap, i)

def test_no_identical_question_served_more_than_twice_over_long_horizon():
    for domain in ("electronics_electrical", "mechanical"):
        for gap in _STAGE2:
            served = [get_display_question(domain, gap, i, path="N")
                      for i in range(25)]
            # the exit prompt is the deliberate steady state; excluding it,
            # nothing repeats beyond its single reframe render
            from collections import Counter
            counts = Counter(q for q in served if q != _EXHAUSTED_EXIT_PROMPT)
            assert max(counts.values()) <= 1, (domain, gap, counts.most_common(2))

def test_exit_prompt_names_the_honest_exits_and_is_distinct():
    t = _EXHAUSTED_EXIT_PROMPT.lower()
    for needle in ("unknown", "deferred", "provisional", "specialist",
                   "evidence", "known risk"):
        assert needle in t
    assert _EXHAUSTED_EXIT_PROMPT != _STALL_REFRAME
    # truthful: never claims something IS resolved or the journey complete
    assert "is resolved" not in t and "has been resolved" not in t
    assert "journey is complete" not in t and "all done" not in t

def test_display_selection_is_pure_and_get_question_unchanged():
    # get_question (the pure selector) still clamps to the final variant —
    # display-layer behavior did not leak into the canonical selector.
    n = _variant_count(MECHANISM_COMPLETENESS, "electronics_electrical")
    last = get_path_n_question(MECHANISM_COMPLETENESS, n - 1,
                               domain="electronics_electrical")
    assert get_path_n_question(MECHANISM_COMPLETENESS, n + 5,
                               domain="electronics_electrical") == last

# --- relevance re-derivation (frozen S2 corpus facts as fixtures) ------------

E1_FEAS_RELIABLE = ("I have not tested anything or measured anything yet, so I "
                    "cannot say how reliable it will be over time.")
M1_FEAS_SAFETY = ("It relies on the holder keeping the ramp flat under the "
                  "weight of a wheelchair. I do not know how much weight or "
                  "what safety margin is needed - that has not been worked "
                  "out or tested.")
M1_MECH_TRANSFER = ("The hinge transfers the force into the frame and the "
                    "latch keeps the motion locked in the flat position.")

def test_honest_feasibility_answers_now_address_the_gap():
    assert addresses_gap(E1_FEAS_RELIABLE, PHYSICAL_FEASIBILITY)
    assert addresses_gap(M1_FEAS_SAFETY, PHYSICAL_FEASIBILITY)

def test_mechanical_bank_vocabulary_addresses_mechanism():
    assert addresses_gap(M1_MECH_TRANSFER, MECHANISM_COMPLETENESS)

def test_off_topic_answers_still_refused():
    off = ("My marketing strategy targets early adopters through social "
           "media campaigns and influencer partnerships in the first year.")
    for gap in _STAGE2:
        assert not addresses_gap(off, gap), gap
    # bare causal connective + generic praise still refused (R2 exclusions)
    assert not addresses_gap(
        "Because it is amazing it will succeed since everyone wants it.",
        PHYSICAL_FEASIBILITY)
