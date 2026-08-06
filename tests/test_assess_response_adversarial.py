"""
Adversarial tests for assess_response()
Step 3 of implementation order — NO fixes, tests only.
"""

from engine.progression_loop import assess_response, ASSERTED, REASONED


# GROUP 1: Single-token attacks
def test_single_token_sensor():
    assert assess_response("sensor") == ASSERTED

def test_single_token_microcontroller():
    assert assess_response("microcontroller") == ASSERTED

def test_single_token_algorithm():
    assert assess_response("algorithm") == ASSERTED

def test_single_token_voltage():
    assert assess_response("voltage") == ASSERTED

def test_single_token_signal():
    assert assess_response("signal") == ASSERTED


# GROUP 2: Short phrase attacks
def test_short_phrase_it_processes_data():
    assert assess_response("it processes data") == ASSERTED

def test_short_phrase_uses_sensor():
    assert assess_response("uses sensor") == ASSERTED

def test_short_phrase_voltage_and_current():
    assert assess_response("voltage and current") == ASSERTED

def test_short_phrase_has_algorithm():
    assert assess_response("has algorithm") == ASSERTED

def test_short_phrase_microcontroller_controls_motor():
    assert assess_response("microcontroller controls motor") == ASSERTED


# GROUP 3: Vague + substance token
def test_vague_with_token_uses_technology_sensor():
    assert assess_response("it uses technology and sensor") == ASSERTED

def test_vague_it_detects_things():
    assert assess_response("it detects things somehow") == ASSERTED

def test_vague_the_signal_is_good():
    assert assess_response("the signal is good") == ASSERTED


# GROUP 4: Substring attacks
def test_substring_data_in_database_update():
    assert assess_response("database update needed") == ASSERTED

def test_substring_signal_in_signaling():
    assert assess_response("signaling pathway") == ASSERTED

def test_substring_bar_in_barrier():
    assert assess_response("barrier protection") == ASSERTED

def test_substring_seal_in_sealed():
    assert assess_response("it is sealed") == ASSERTED

def test_substring_filter_in_filtering():
    assert assess_response("by filtering noise") == ASSERTED


# GROUP 5: Correct ASSERTED — regression protection
def test_empty_string_is_asserted():
    assert assess_response("") == ASSERTED

def test_pure_vague_filler_is_asserted():
    assert assess_response("somehow something technology") == ASSERTED

def test_short_no_substance_is_asserted():
    assert assess_response("it works well") == ASSERTED

def test_length_under_20_no_substance_is_asserted():
    assert assess_response("good idea") == ASSERTED

def test_whitespace_only_is_asserted():
    assert assess_response("   ") == ASSERTED


# GROUP 6: Legitimate REASONED — regression protection
def test_reasoned_hall_sensor_explanation():
    result = assess_response(
        "A Hall sensor detects magnetic field changes by measuring voltage "
        "perpendicular to current flow, enabling contactless position detection."
    )
    assert result == REASONED

def test_reasoned_algorithm_with_explanation():
    result = assess_response(
        "The algorithm parses the input stream and tokenizes it into AST nodes, "
        "then applies static analysis rules to detect type mismatches."
    )
    assert result == REASONED


# GROUP 7: Boundary
def test_exactly_20_chars_no_substance():
    assert assess_response("a" * 20) == ASSERTED

def test_19_chars_no_substance():
    assert assess_response("a" * 19) == ASSERTED
