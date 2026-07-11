"""
Focused tests for the Layer-2 bounded scoring correction (owner-authorized
2026-07-11): explicit causal connectives (because / since / therefore / thus /
hence / due to / as a result) qualify for REASONED only through a distinct
gated path that additionally requires an electronics/electrical domain
substance signal matched as a WHOLE WORD (conservative plural folding) inside
the clause that supports the connective:

  - cause connectives (because / since / due to): substance AFTER the
    connective (the rationale clause);
  - consequence connectives (therefore / thus / hence / as a result):
    substance BEFORE the connective (the supporting cause).

Existing _CAUSAL_STRUCTURE_PATTERNS entries, weak-pattern rejection,
weak-token rejection, and the generic-verb trap keep their current behavior
for every input that does not qualify for the new gate. The gate never uses
raw substring substance semantics, never fires for empty/unknown domains, and
grants REASONED only at the existing minimum response length.
"""

import warnings

import pytest

from engine.progression_loop import (
    ASSERTED,
    REASONED,
    MIN_REASONED_RESPONSE_LENGTH,
    _CAUSAL_STRUCTURE_PATTERNS,
    _NEW_CAUSAL_CONNECTIVES_CAUSE_FIRST,
    _NEW_CAUSAL_CONNECTIVES_RESULT_FIRST,
    _connective_whole_word_substance_gate,
    _has_whole_word_substance,
    assess_response,
    integrate_response,
    MECHANISM_COMPLETENESS,
)
from engine.idea_state import IdeaState, OPEN, PARTIAL, CLOSED

D = "electronics_electrical"


# ---------------------------------------------------------------------------
# (0) The authorized connective constant is exactly the owner-approved set.
# ---------------------------------------------------------------------------

def test_connective_constant_is_exactly_the_authorized_set():
    assert set(_NEW_CAUSAL_CONNECTIVES_CAUSE_FIRST) == {"because", "since", "due to"}
    assert set(_NEW_CAUSAL_CONNECTIVES_RESULT_FIRST) == {
        "therefore", "thus", "hence", "as a result"}
    # Explicitly excluded connectives are not present anywhere in the set.
    excluded = {"so", "and so", "for", "as", "while"}
    assert not excluded & (set(_NEW_CAUSAL_CONNECTIVES_CAUSE_FIRST)
                           | set(_NEW_CAUSAL_CONNECTIVES_RESULT_FIRST))


def test_existing_causal_structure_patterns_frozen():
    # The existing pattern list must remain exactly as before this change
    # (raw substring semantics unchanged; the new connectives live in a
    # distinct gated path and were NOT added here).
    assert _CAUSAL_STRUCTURE_PATTERNS == [
        "when ", "if ", "after ", "before ", "until ", "once ", "as soon as ",
        "causes", "produces", "results in", "leads to",
        "converts", "transforms", "transfers",
        "measures", "calculates", "compares", "exceeds",
        "locks", "releases", "pushes", "pulls", "blocks", "rotates",
        "in order to", "so that", "which means", "which causes",
        "by measuring", "by detecting", "by converting", "then ",
    ]


# ---------------------------------------------------------------------------
# (1) Every authorized connective qualifies with whole-word clause substance.
# ---------------------------------------------------------------------------

_CONNECTIVE_REASONED_CASES = [
    ("because", "Fan must continue because sensor still reads high temperature "
                "and enclosure has not cooled."),
    ("since", "The threshold stays stored locally since the sensor and relay "
              "must keep operating offline."),
    ("therefore", "The relay coil overheats during long operation; therefore "
                  "the enclosure needs a cooling vent."),
    ("thus", "The capacitor keeps discharging through the coil; thus the alarm "
             "stays powered in a brownout."),
    ("hence", "The battery voltage sags under motor load; hence the alarm "
              "needs a separate supply rail."),
    ("due to", "The relay contacts may weld due to the motor inrush current "
               "exceeding their rated capacity."),
    ("as a result", "The sensor voltage drifts as the enclosure heats; as a "
                    "result the controller may trigger the fan too late."),
]


@pytest.mark.parametrize("label,text", _CONNECTIVE_REASONED_CASES)
def test_each_authorized_connective_with_substance_is_reasoned(label, text):
    assert assess_response(text, D) == REASONED, label


# ---------------------------------------------------------------------------
# (2) Uppercase and mixed-case forms.
# ---------------------------------------------------------------------------

def test_connective_matching_is_case_insensitive():
    upper = ("FAN MUST CONTINUE BECAUSE SENSOR STILL READS HIGH TEMPERATURE "
             "AND ENCLOSURE HAS NOT COOLED.")
    mixed = ("Fan Must Continue Because Sensor Still Reads High Temperature "
             "And Enclosure Has Not Cooled.")
    assert assess_response(upper, D) == REASONED
    assert assess_response(mixed, D) == REASONED


# ---------------------------------------------------------------------------
# (3) Whitespace and punctuation around connectives.
# ---------------------------------------------------------------------------

def test_multiword_connective_tolerates_extra_internal_whitespace():
    text = ("The relay contacts may weld due  to the motor inrush current "
            "exceeding their rated capacity.")
    assert assess_response(text, D) == REASONED


def test_connective_with_surrounding_punctuation_still_matches():
    comma = ("Because the sensor overheats quickly in the sealed box, the fan "
             "must run longer than one minute.")
    paren = ("The vent stays open longer (because the sensor cools slowly) "
             "and the alarm still sounds.")
    assert assess_response(comma, D) == REASONED
    assert assess_response(paren, D) == REASONED


# ---------------------------------------------------------------------------
# (4) Whole-word substance matching; (6) substring rejection.
# ---------------------------------------------------------------------------

def test_substance_signals_match_only_as_whole_words():
    from engine.domain_rules import get_substance_signals
    toks = set(get_substance_signals(D))
    # Direct signals match as words.
    assert _has_whole_word_substance("the sensor and the relay", toks)
    # Substring fragments inside larger words never match.
    for trap in ("nice", "device", "which", "called", "enabled",
                 "especially", "shall", "relayed", "hallway", "iceberg",
                 "sliced", "displayed", "espresso"):
        assert not _has_whole_word_substance(trap, toks), trap


_SUBSTRING_TRAP_SENTENCES = [
    ("nice/device", "It is a good device because everyone thinks it is very "
                    "nice and useful."),
    ("which", "This matters because everyone can tell which parts feel nice "
              "and which do not."),
    ("called/enabled", "The feature works because it is called smart mode and "
                       "stays enabled all day long."),
    ("especially/hallway", "People like it because it is especially handy in "
                           "the kitchen and hallway areas."),
    ("shall", "We shall win because we shall try harder and we shall never "
              "give up on this plan."),
]


@pytest.mark.parametrize("label,text", _SUBSTRING_TRAP_SENTENCES)
def test_substring_only_fake_substance_never_qualifies(label, text):
    assert assess_response(text, D) == ASSERTED, label


# ---------------------------------------------------------------------------
# (5) Conservative plural folding.
# ---------------------------------------------------------------------------

def test_plural_folding_recognizes_normal_plurals_of_authorized_signals():
    from engine.domain_rules import get_substance_signals
    toks = set(get_substance_signals(D))
    for plural in ("sensors", "relays", "resistors", "batteries",
                   "capacitors", "motors", "leds", "chips"):
        assert _has_whole_word_substance(plural, toks), plural
    # Folding never invents vocabulary: non-signal plurals stay unmatched.
    for nonsignal in ("parts", "areas", "things", "wires", "cases"):
        assert not _has_whole_word_substance(nonsignal, toks), nonsignal


def test_plural_substance_in_rationale_clause_is_reasoned():
    text = ("The cabinet needs venting because the resistors and batteries "
            "overheat during long idle periods.")
    assert assess_response(text, D) == REASONED
    text2 = ("Contacts wear out quickly because the relays switch at full "
             "motor load every few seconds.")
    assert assess_response(text2, D) == REASONED


# ---------------------------------------------------------------------------
# (7) Superficial praise; (8) weak placeholders.
# ---------------------------------------------------------------------------

def test_superficial_praise_remains_asserted():
    assert assess_response(
        "It is a good device because everyone thinks it is very nice and "
        "useful.", D) == ASSERTED


def test_weak_placeholder_answers_remain_asserted():
    assert assess_response(
        "It works because technology makes everything better somehow.",
        D) == ASSERTED
    assert assess_response(
        "It helps because something in the box does stuff somehow every day.",
        D) == ASSERTED


# ---------------------------------------------------------------------------
# (9) Quoted causal language; (10) third-party causal claims.
# ---------------------------------------------------------------------------

def test_quoted_causal_language_with_substance_free_rationale_stays_asserted():
    assert assess_response(
        "Someone said the sensor fails because heat is bad, but I have not "
        "checked anything.", D) == ASSERTED
    assert assess_response(
        'My friend told me "it fails because the heat is bad" but I cannot '
        "explain it myself.", D) == ASSERTED


def test_third_party_causal_claim_stays_asserted():
    assert assess_response(
        "A video claims it breaks because of bad wiring, but I did not "
        "verify the claim at all.", D) == ASSERTED


# ---------------------------------------------------------------------------
# (11) Negated causal language; (12) temporal "since".
# ---------------------------------------------------------------------------

def test_negated_causal_language_without_clause_substance_stays_asserted():
    assert assess_response(
        "It does not overheat because of the metal case, and I have not "
        "found the real cause.", D) == ASSERTED


def test_temporal_since_stays_asserted():
    assert assess_response(
        "Since Tuesday I have been thinking about this invention and it "
        "seems very interesting.", D) == ASSERTED
    assert assess_response(
        "Since yesterday I have been sketching the case shape and thinking "
        "about the colors.", D) == ASSERTED


# ---------------------------------------------------------------------------
# (13) Repeated connective stuffing; (14) domain-token stuffing;
# (15) numeric stuffing.
# ---------------------------------------------------------------------------

def test_repeated_connective_stuffing_stays_asserted():
    assert assess_response(
        "Because it is good because it is useful because it is innovative.",
        D) == ASSERTED
    assert assess_response(
        "Because because because therefore hence thus due to as a result it "
        "is wonderful today.", D) == ASSERTED


def test_domain_token_stuffing_outside_supporting_clause_stays_asserted():
    # Tokens stuffed BEFORE a cause connective do not satisfy the gate — the
    # rationale clause after "because" is substance-free.
    assert assess_response(
        "Sensor relay battery voltage current chip resistor. It is great "
        "because it is nice.", D) == ASSERTED
    # Tokens stuffed AFTER a consequence connective do not satisfy the gate —
    # the supporting cause before "therefore" is substance-free.
    assert assess_response(
        "It is nice and everyone likes it very much; therefore sensor relay "
        "battery voltage.", D) == ASSERTED


def test_numeric_stuffing_stays_asserted():
    assert assess_response(
        "It scores 12345 because 99999 88888 77777 66666 55555 44444 33333 "
        "22222 11111 00000.", D) == ASSERTED


# ---------------------------------------------------------------------------
# (16) No-domain behavior; (17) unknown-domain behavior.
# ---------------------------------------------------------------------------

def test_gate_never_fires_without_domain():
    text = ("Fan must continue because sensor still reads high temperature "
            "and enclosure has not cooled.")
    with pytest.warns(UserWarning):
        assert assess_response(text, "") == ASSERTED


def test_gate_never_fires_for_unknown_domain():
    text = ("Fan must continue because sensor still reads high temperature "
            "and enclosure has not cooled.")
    with pytest.warns(UserWarning):
        assert assess_response(text, "underwater_basketweaving") == ASSERTED


def test_existing_no_domain_reasoned_path_unchanged():
    # The existing causal path (no substance requirement) still works with an
    # empty domain — unchanged behavior.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        assert assess_response(
            "A Hall sensor detects magnetic field changes by measuring "
            "voltage perpendicular to current flow, enabling contactless "
            "position detection.", "") == REASONED


def test_gate_helper_returns_false_for_empty_signal_set():
    assert _connective_whole_word_substance_gate(
        "fan must continue because sensor reads high", set()) is False


# ---------------------------------------------------------------------------
# (18) Response below minimum length.
# ---------------------------------------------------------------------------

def test_new_path_respects_existing_minimum_length():
    base = "It fails because the relay melts"
    at_min = base + " " + "x" * (MIN_REASONED_RESPONSE_LENGTH - len(base) - 1)
    below_min = base + " " + "x" * (MIN_REASONED_RESPONSE_LENGTH - len(base) - 2)
    assert len(at_min) == MIN_REASONED_RESPONSE_LENGTH
    assert len(below_min) == MIN_REASONED_RESPONSE_LENGTH - 1
    assert assess_response(at_min, D) == REASONED
    assert assess_response(below_min, D) == ASSERTED


# ---------------------------------------------------------------------------
# (19) Existing causal patterns / trap / weak-input behavior unchanged.
# ---------------------------------------------------------------------------

def test_existing_causal_pattern_classifications_unchanged():
    # when / if / so that / measurement-verb behavior — pre-change REASONED
    # controls stay REASONED.
    assert assess_response(
        "The controller should retain the threshold locally since the sensor "
        "and relay must still operate when internet connectivity is "
        "unavailable.", D) == REASONED
    assert assess_response(
        "A Hall sensor detects magnetic field changes by measuring voltage "
        "perpendicular to current flow, enabling contactless position "
        "detection.", D) == REASONED


def test_generic_verb_trap_preserved_when_gate_does_not_qualify():
    # Generic verb + connective whose supporting clause is substance-free:
    # the trap still rejects exactly as before.
    assert assess_response(
        "It uses batteries because everyone says it is very nice and quite "
        "useful overall.", D) == ASSERTED
    # Generic-verb answers without any new connective are untouched.
    assert assess_response(
        "it uses a sensor and connects to wifi and sends alerts to the phone "
        "app every day", D) == ASSERTED


def test_weak_pattern_and_weak_token_rejections_precede_new_gate():
    # Exact weak answers stay rejected regardless of connectives.
    assert assess_response("i don't know", D) == ASSERTED
    # Weak-token + no substance stays rejected even with a connective.
    assert assess_response(
        "It works because technology makes everything better somehow.",
        D) == ASSERTED


# ---------------------------------------------------------------------------
# (20) Determinism.
# ---------------------------------------------------------------------------

def test_assessment_is_deterministic():
    samples = [t for _, t in _CONNECTIVE_REASONED_CASES] + \
              [t for _, t in _SUBSTRING_TRAP_SENTENCES]
    for text in samples:
        first = assess_response(text, D)
        for _ in range(25):
            assert assess_response(text, D) == first


# ---------------------------------------------------------------------------
# (21) First REASONED answer: OPEN → PARTIAL only; (22) follow-up closure.
# ---------------------------------------------------------------------------

def test_first_new_gate_reasoned_answer_moves_open_gap_to_partial_only():
    state = IdeaState(idea_id="gate-t1")
    state.domain = D
    state.iteration = 1
    answer = ("Fan must continue because sensor still reads high temperature "
              "and enclosure has not cooled.")
    transition, reason = integrate_response(
        state, MECHANISM_COMPLETENESS, "How does it work?", answer)
    gap = state.get_gap(MECHANISM_COMPLETENESS)
    assert transition == "WARN"
    assert "partially addressed" in reason
    assert gap.status == PARTIAL          # never OPEN → CLOSED in one step
    assert gap.closed_at is None


def test_reasoned_follow_up_closes_partial_gap():
    state = IdeaState(idea_id="gate-t2")
    state.domain = D
    state.iteration = 1
    first = ("Fan must continue because sensor still reads high temperature "
             "and enclosure has not cooled.")
    followup = ("The relay contacts may weld due to the motor inrush current "
                "exceeding their rated capacity.")
    integrate_response(state, MECHANISM_COMPLETENESS, "q", first)
    state.iteration = 2
    transition, reason = integrate_response(
        state, MECHANISM_COMPLETENESS, "q", followup)
    gap = state.get_gap(MECHANISM_COMPLETENESS)
    assert transition == "PASS"
    assert "closed after REASONED follow-up" in reason
    assert gap.status == CLOSED


# ---------------------------------------------------------------------------
# (23) No scoring bypass for the explicit unknown action;
# (24) no transcript/ledger mutation beyond existing behavior.
# ---------------------------------------------------------------------------

def _seed_session():
    import uuid
    from web.app import SESSION_STORE
    from engine.progression_loop import run_iteration
    state = IdeaState(idea_id="gate-web-" + uuid.uuid4().hex[:8])
    state.domain = D
    run_iteration(state, "A bicycle brake light that turns on when the rider "
                         "decelerates, using a sensor to detect slowing down.")
    sid = "gate-web-" + uuid.uuid4().hex
    SESSION_STORE[sid] = {
        "state": state,
        "last_result": None,
        "transcript": [],
        "last_question": "What is the core mechanism?",
    }
    return sid


def test_explicit_unknown_action_is_never_assessed_even_with_gate_text():
    from web.app import app, SESSION_STORE
    sid = _seed_session()
    try:
        entry = SESSION_STORE[sid]
        state = entry["state"]
        before = (state.iteration, state.maturity_level,
                  [(g.gap_type, g.status) for g in state.gaps])
        r = app.test_client().post(
            f"/session/{sid}",
            data={"action": "unknown",
                  "response": "Fan must continue because sensor still reads "
                              "high temperature and enclosure has not cooled."})
        assert r.status_code in (301, 302)
        after = (state.iteration, state.maturity_level,
                 [(g.gap_type, g.status) for g in state.gaps])
        assert after == before                    # no scoring, no gap movement
        assert entry["last_result"] is None       # never assessed
        assert entry["transcript"] == []          # no transcript record
    finally:
        SESSION_STORE.pop(sid, None)


def test_answered_flow_keeps_transcript_and_ledger_verbatim():
    from web.app import app, SESSION_STORE
    sid = _seed_session()
    try:
        entry = SESSION_STORE[sid]
        state = entry["state"]
        answer = ("Fan must continue because sensor still reads high "
                  "temperature and enclosure has not cooled.")
        r = app.test_client().post(
            f"/session/{sid}", data={"action": "answered", "response": answer})
        assert r.status_code in (301, 302)
        # Exactly one new transcript record, byte-for-byte verbatim.
        assert len(entry["transcript"]) == 1
        assert entry["transcript"][0]["response"] == answer
        # Exactly one new ledger record, verbatim content.
        assert len(state.assertions) == 1
        assert state.assertions[0].content == answer
        # No acknowledged unknown was invented.
        assert state.acknowledged_unknowns == []
        # First REASONED answer moved the open gap to PARTIAL only.
        gap = state.get_gap(MECHANISM_COMPLETENESS)
        assert gap.status == PARTIAL
        assert entry["last_result"]["transition"] == "WARN"
    finally:
        SESSION_STORE.pop(sid, None)
