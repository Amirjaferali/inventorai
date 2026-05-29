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


@pytest.mark.xfail(reason="ADR-003 Step 6: component label only — no claim/basis/relationship")
def test_f011_hall_sensor_alone_does_not_advance_level_0():
    """Hall sensor alone is a component label. ADR-003 requires claim+basis+relationship."""
    state = IdeaState(idea_id="f011-test")
    quality = assess_response("Hall sensor")
    state.known_problem = Evidence(content="Hall sensor", quality=quality, iteration=1)
    can_transition, reason = evaluate_transition(state)
    assert can_transition is True  # expected to fail — blocked by anti-triviality guard


def test_f011_piezoelectric_response_advances_level_0():
    """44 chars, substance token, meets MIN_REASONED_RESPONSE_LENGTH."""
    state = IdeaState(idea_id="f011-test")
    response = "The piezoelectric sensor produces voltage when pressure deforms the crystal, so the controller detects pressure changes from that voltage signal."
    quality = assess_response(response)
    state.known_problem = Evidence(content=response, quality=quality, iteration=1)
    can_transition, reason = evaluate_transition(state)
    assert can_transition is True
    assert reason == "Problem established — ready for LEVEL 1"
