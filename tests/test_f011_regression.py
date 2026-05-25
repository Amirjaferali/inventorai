"""
F-011 Regression Test
Defect: Weak/empty responses advanced Level 0->1 maturity transition.
Fix: evaluate_transition() now requires known_problem.quality >= REASONED for Level 0->1.
Commit: eba4213
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from engine.idea_state import IdeaState, Evidence
from engine.progression_loop import assess_response, evaluate_transition


def make_state_with_problem(response: str) -> IdeaState:
    state = IdeaState(idea_id='f011-test')
    state.domain = 'electronics'
    quality = assess_response(response)
    evidence = Evidence(content=response, quality=quality, iteration=1)
    state.known_problem = evidence
    return state


def test_empty_string_does_not_advance():
    state = make_state_with_problem("")
    can, reason = evaluate_transition(state)
    assert can is False, f"F-011 REGRESSION: '' must not advance Level 0->1, got transition=True, reason={reason}"


def test_i_dont_know_does_not_advance():
    state = make_state_with_problem("I don't know")
    can, reason = evaluate_transition(state)
    assert can is False, f"F-011 REGRESSION: 'I don't know' must not advance Level 0->1, got transition=True, reason={reason}"


def test_maybe_does_not_advance():
    state = make_state_with_problem("maybe")
    can, reason = evaluate_transition(state)
    assert can is False, f"F-011 REGRESSION: 'maybe' must not advance Level 0->1, got transition=True, reason={reason}"


def test_not_sure_does_not_advance():
    state = make_state_with_problem("not sure")
    can, reason = evaluate_transition(state)
    assert can is False, f"F-011 REGRESSION: 'not sure' must not advance Level 0->1, got transition=True, reason={reason}"


def test_hall_sensor_advances():
    state = make_state_with_problem("Hall sensor")
    can, reason = evaluate_transition(state)
    assert can is True, f"F-011 REGRESSION: 'Hall sensor' must advance Level 0->1, got transition=False, reason={reason}"


def test_piezoelectric_advances():
    state = make_state_with_problem("uses piezoelectric sensor to detect pressure")
    can, reason = evaluate_transition(state)
    assert can is True, f"F-011 REGRESSION: piezoelectric answer must advance Level 0->1, got transition=False, reason={reason}"


if __name__ == '__main__':
    tests = [
        test_empty_string_does_not_advance,
        test_i_dont_know_does_not_advance,
        test_maybe_does_not_advance,
        test_not_sure_does_not_advance,
        test_hall_sensor_advances,
        test_piezoelectric_advances,
    ]
    passed = 0
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS  {t.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"FAIL  {t.__name__}: {e}")
            failed += 1
    print(f"\n{passed} passed, {failed} failed")
    sys.exit(0 if failed == 0 else 1)
