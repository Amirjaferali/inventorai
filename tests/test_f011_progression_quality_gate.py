import pytest
from engine.idea_state import Evidence, IdeaState
from engine.progression_loop import assess_response, evaluate_transition


@pytest.mark.parametrize("response", [
    "",
    "I don't know",
    "maybe",
    "not sure",
    "i do not know",
    "unknown",
    "no idea",
    " ",
])
def test_f011_weak_or_empty_problem_responses_do_not_advance_level_0(response):
    state = IdeaState(idea_id="f011-test")
    quality = assess_response(response)
    state.known_problem = Evidence(content=response, quality=quality, iteration=1)
    can_transition, reason = evaluate_transition(state)
    assert can_transition is False
    assert reason == "Problem not yet established"


@pytest.mark.parametrize("response", [
    "Hall sensor",
    "uses piezoelectric sensor to detect pressure",
])
def test_f011_specific_technical_problem_responses_can_advance_level_0(response):
    state = IdeaState(idea_id="f011-test")
    quality = assess_response(response)
    state.known_problem = Evidence(content=response, quality=quality, iteration=1)
    can_transition, reason = evaluate_transition(state)
    assert can_transition is True
    assert reason == "Problem established — ready for LEVEL 1"
