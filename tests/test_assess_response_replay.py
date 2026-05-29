import pytest
from engine.idea_state import ASSERTED, REASONED
from engine.progression_loop import assess_response

REPLAY_MATRIX = [
    ("The sensor detects water and sends a signal to the phone.", ASSERTED, "regression: generic verbs, no causal structure"),
    ("The clamp locks when pressure pushes the pin into the groove.", REASONED, "beginner-mechanical: when + pushes + into"),
    ("The door opens after the key rotates the cylinder.", REASONED, "beginner-mechanical: after + rotates"),
    ("When water bridges the two probes, resistance drops below the threshold and the circuit produces an alert that triggers the notification.", REASONED, "strong-electronics: full causal chain"),
    ("The catalyst causes the reaction by lowering activation energy, which means molecules convert faster into the final product.", REASONED, "strong-chemistry: causes + which means"),
    ("The spring releases stored force when the lever exceeds the pivot angle, pushing the gate open.", REASONED, "mechanical: releases + when + exceeds"),
    ("The rear latch rotates after the lever retracts the locking pin.", REASONED, "valid mechanism — rotates + after"),
    ("When a customer submits the form, the system compares the input against stored records and produces a match result.", REASONED, "workflow: when + compares + produces"),
    ("The technology works through pressure and flow to produce results.", ASSERTED, "buzzword mimicry"),
    ("It functions via advanced processes that convert inputs into outputs.", ASSERTED, "vague conversion claim"),
    ("The system uses sensors and processors and connects to the cloud and monitors things and reports data and handles various situations and manages workflows and stores information and displays results.", ASSERTED, "length gaming"),
    ("The sensor signal processor network module data interface unit handles the circuit board algorithm protocol operation system.", ASSERTED, "rule-3 loophole guard: jargon, no structure"),
    ("The pin it goes into hole when bar is pushing down on spring.", REASONED, "non-native: when + into + pushing"),
    ("Water makes sensor wet, then signal goes to phone after wet detected.", REASONED, "non-native: after — sequential causation"),
    ("I don't know.", ASSERTED, "explicit weak pattern"),
    ("It uses technology to somehow connect the things together.", ASSERTED, "weak tokens + no substance"),
    ("Sensor detects it.", ASSERTED, "too short + generic verb"),
]

@pytest.mark.parametrize("response,expected,description", REPLAY_MATRIX)
def test_replay_matrix(response, expected, description):
    result = assess_response(response)
    assert result == expected, f"\nFAIL [{description}]\n  Input: {response!r}\n  Expected: {expected}\n  Got: {result}"
