"""
Focused tests for the Layer-2 bounded scoring correction (owner-authorized
2026-07-11): explicit causal connectives (because / since / therefore / thus /
hence / due to / as a result) qualify for REASONED only through a distinct
gated path that additionally requires an electronics/electrical domain
substance signal matched as a WHOLE WORD (explicit safe plural alias map) in the
SAME SENTENCE as the connective, on the directional side it supports
(TRUE SENTENCE-BOUNDED correction, owner-authorized 2026-07-11):

  - sentences are bounded deterministically by . ? ! and line breaks;
    semicolons, commas, and colons stay inside a sentence;
  - cause connectives (because / since / due to): substance AFTER the
    connective, before its sentence ends;
  - consequence connectives (therefore / thus / hence / as a result):
    substance BEFORE the connective, after its sentence starts; an empty
    result side never qualifies;
  - substance found only in ANOTHER sentence never qualifies; occurrences
    are evaluated independently and sides are never combined across
    occurrences or sentences;
  - narrowly documented conservative disqualifiers (fixed token/character
    checks, not parsers): a double-quote character in the sentence; a
    reported-speech marker (said/says/told/heard/claims/claimed/reported/
    according) before the connective; the token "not"/"never" before the
    connective; and sentence-initial "since" (temporal ambiguity).

Existing _CAUSAL_STRUCTURE_PATTERNS entries, weak-pattern rejection,
weak-token rejection, and the generic-verb trap keep their current behavior
for every input that does not qualify for the new gate. The gate never uses
raw substring substance semantics, never fires for empty/unknown domains, and
grants REASONED only at the existing minimum response length.
"""

import warnings
from test_p4_1b2a_durable_answer_append import answered_post, seed_direct_session_envelope  # P4-1b-2a

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
    from engine.domain_rules import get_substance_signals, get_substance_signal_plural_aliases
    toks = set(get_substance_signals(D))
    aliases = get_substance_signal_plural_aliases(D)
    # Direct signals match as words.
    assert _has_whole_word_substance("the sensor and the relay", toks, aliases)
    # Substring fragments inside larger words never match.
    for trap in ("nice", "device", "which", "called", "enabled",
                 "especially", "shall", "relayed", "hallway", "iceberg",
                 "sliced", "displayed", "espresso"):
        assert not _has_whole_word_substance(trap, toks, aliases), trap


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
# (5) Explicit safe plural alias map — L2SC-01: pack-scoped registry-owned
# source (docs/governance/L2SC01_SUBSTANCE_SIGNAL_PLURAL_ALIAS_INCREMENT_
# CONTRACT.md), NOT a shared-engine hardcoded map. Generic suffix folding
# remains NOT ratified.
# ---------------------------------------------------------------------------

def test_explicit_plural_map_is_exactly_the_authorized_pairs():
    from engine.domain_rules import get_substance_signal_plural_aliases
    aliases = get_substance_signal_plural_aliases(D)
    assert aliases == {
        "sensors": "sensor", "relays": "relay", "resistors": "resistor",
        "batteries": "battery", "capacitors": "capacitor", "motors": "motor",
        "leds": "led", "ics": "ic",
    }
    # "hall", "chip", "display", and "esp" deliberately have no plural alias.
    for excluded in ("halls", "chips", "displays", "esps"):
        assert excluded not in aliases, excluded


def test_explicit_plural_map_recognizes_only_the_authorized_pairs():
    from engine.domain_rules import get_substance_signals, get_substance_signal_plural_aliases
    toks = set(get_substance_signals(D))
    aliases = get_substance_signal_plural_aliases(D)
    # The eight authorized plural forms match (and their singulars still do).
    for plural in ("sensors", "relays", "resistors", "batteries",
                   "capacitors", "motors", "leds", "ics"):
        assert _has_whole_word_substance(plural, toks, aliases), plural
    for singular in ("sensor", "relay", "resistor", "battery",
                     "capacitor", "motor", "led", "ic"):
        assert _has_whole_word_substance(singular, toks, aliases), singular
    # No generic suffix stripping: non-whitelisted plurals and inflections
    # never match, including the independently demonstrated false folds.
    for rejected in ("ices", "halls", "chips", "displays", "buses",
                     "classes", "glasses", "statuses", "series", "analyses",
                     "relaying", "displaying"):
        assert not _has_whole_word_substance(rejected, toks, aliases), rejected
    # The map never invents vocabulary: non-signal plurals stay unmatched.
    for nonsignal in ("parts", "areas", "things", "wires", "cases"):
        assert not _has_whole_word_substance(nonsignal, toks, aliases), nonsignal


def test_plural_alias_map_is_pack_scoped_not_shared_engine_hardcode():
    """L2SC-01: confirms there is exactly ONE live source of plural-alias
    data (the domain pack registry) — the historical shared-engine constant
    no longer exists at all."""
    import engine.progression_loop as pl
    assert not hasattr(pl, "_SUBSTANCE_PLURAL_ALIASES")


_UNSAFE_PLURAL_REJECTION_SENTENCES = [
    ("ices", "The dessert stays cold because the ices melt slowly in the "
             "insulated serving tray."),
    ("halls", "The venue works well because the halls stay quiet during the "
              "evening events."),
    ("chips", "The snack bowl empties fast because the chips taste salty and "
              "fresh every single day."),
    ("displays", "The kiosk attracts attention because it displays bright "
                 "messages all day long."),
    ("buses", "The commute is easy because the buses arrive every ten "
              "minutes at this corner."),
    ("classes", "The course fills early because the classes cover very "
                "popular topics each term."),
    ("glasses", "The tray looks elegant because the glasses sparkle under "
                "the warm dining lights."),
    ("statuses", "The board stays useful because the statuses update every "
                 "hour without any effort."),
    ("series", "The show stays popular because the series builds suspense "
               "across every single season."),
    ("analyses", "The report reads clearly because the analyses were written "
                 "in plain simple language."),
    ("relaying", "The signal keeps moving because the relaying happens at "
                 "every node along the path."),
    ("displaying", "The stand works nicely because the displaying continues "
                   "even in direct sunlight."),
]


@pytest.mark.parametrize("label,text", _UNSAFE_PLURAL_REJECTION_SENTENCES)
def test_non_whitelisted_plural_forms_never_qualify(label, text):
    # Each sentence has an authorized connective, exceeds the minimum length,
    # and carries the probe word in the rationale side — it must stay
    # ASSERTED because no explicit plural alias exists for the probe word.
    assert len(text) >= MIN_REASONED_RESPONSE_LENGTH
    assert assess_response(text, D) == ASSERTED, label


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
        "fan must continue because sensor reads high", set(), {}) is False


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
    seed_direct_session_envelope(sid, state)  # explicit P4-1b-2a durable envelope
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
        r = answered_post(app.test_client(), sid, {"action": "answered", "response": answer})
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


# ===========================================================================
# TRUE SENTENCE BOUNDING (owner-authorized correction 2026-07-11).
# The reviewed head searched the remaining start/end of the WHOLE response,
# across sentence boundaries. The corrected gate requires the qualifying
# substance in the SAME SENTENCE as the qualifying connective, on the
# directional side it supports.
# ===========================================================================

def test_cross_sentence_substance_leakage_never_qualifies():
    # Owner-required rejection cases: substance in a DIFFERENT sentence must
    # not let a substance-free causal clause qualify.
    assert assess_response(
        "It fails because the spring is weak. The sensor is a separate part "
        "entirely.", D) == ASSERTED
    assert assess_response(
        "The sensor is a separate part entirely. Therefore the design is "
        "good.", D) == ASSERTED
    assert assess_response(
        "It works because the design is popular. A relay is used elsewhere "
        "in the product.", D) == ASSERTED


def test_line_breaks_are_sentence_boundaries():
    # A line break bounds the sentence exactly like . ? ! — substance on the
    # other side of a line break never qualifies.
    assert assess_response(
        "It fails because the spring is weak\nThe sensor is a separate part "
        "entirely", D) == ASSERTED
    assert assess_response(
        "The sensor is a separate part entirely\nTherefore the design is "
        "good and useful", D) == ASSERTED


def test_multiword_connective_spanning_a_line_break_never_qualifies():
    # "due\nto" spans a sentence boundary, so the occurrence is skipped
    # (documented conservative false negative).
    assert assess_response(
        "The relay contacts may weld due\nto motor inrush current exceeding "
        "their rated capacity", D) == ASSERTED


def test_wrong_side_substance_never_qualifies():
    # Cause-first: substance only BEFORE the connective (claim side).
    assert assess_response(
        "The sensor fails constantly because the spring is far too weak "
        "for this design.", D) == ASSERTED
    # Result-first: substance only AFTER the connective (result side).
    assert assess_response(
        "The design is elegant and simple; therefore the sensor will work "
        "reliably every time.", D) == ASSERTED


def test_multiple_connective_occurrences_evaluated_independently():
    # No occurrence has same-sentence directional substance -> ASSERTED,
    # even though substance exists elsewhere in the response.
    assert assess_response(
        "The sensor is reliable because it is nice. The design is slow "
        "therefore it is safe.", D) == ASSERTED
    # One valid occurrence among invalid ones is sufficient.
    assert assess_response(
        "It is nice because people like it. The alarm stays on because the "
        "sensor still reads heat.", D) == REASONED
    assert assess_response(
        "Therefore it is good. The relay coil saturates under load; "
        "therefore the driver needs a diode.", D) == REASONED


def test_result_first_with_empty_result_side_never_qualifies():
    assert assess_response(
        "The sensor voltage drifts constantly upward; therefore.",
        D) == ASSERTED


def test_sentence_initial_because_remains_eligible():
    # Sentence-initial "because" is unambiguously causal and stays eligible
    # (pinned by the existing punctuation test as well).
    assert assess_response(
        "Because the sensor overheats quickly in the sealed box, the fan "
        "must run longer than one minute.", D) == REASONED


def test_sentence_initial_since_never_qualifies():
    # Temporal-since guard: sentence-initial "since" is frequently temporal
    # and never qualifies — including the owner-required temporal case with
    # substance after it, and the causal sentence-initial form (a documented
    # conservative false negative).
    assert assess_response(
        "Since Tuesday the sensor prototype has been on my desk and I have "
        "been thinking about it.", D) == ASSERTED
    assert assess_response(
        "Since the sensor must stay powered at night, the relay latches the "
        "supply on.", D) == ASSERTED


# ---------------------------------------------------------------------------
# Owner-required quoted / attributed / negated rejection cases (narrowly
# documented conservative guards — fixed token/character checks, not parsers).
# ---------------------------------------------------------------------------

def test_owner_required_quoted_statement_stays_asserted():
    assert assess_response(
        'Someone said "the sensor fails because the relay overheats," but I '
        "have not verified that explanation.", D) == ASSERTED


def test_owner_required_third_party_statement_stays_asserted():
    assert assess_response(
        "An engineer told me the sensor fails because the relay overheats, "
        "but I have not confirmed it.", D) == ASSERTED


def test_owner_required_negated_explanation_stays_asserted():
    assert assess_response(
        "The sensor does not fail because the relay overheats; I do not "
        "know the actual cause.", D) == ASSERTED


def test_additional_guard_variants_stay_asserted():
    # says-attribution, "never" negation, curly quotes, "according to".
    assert assess_response(
        "My colleague says it fails because the relay overheats, but I "
        "cannot explain the mechanism.", D) == ASSERTED
    assert assess_response(
        "The alarm never fires because the sensor threshold is high, and I "
        "have not investigated further.", D) == ASSERTED
    assert assess_response(
        "Someone wrote “it fails because the relay overheats” but "
        "I have not verified anything myself.", D) == ASSERTED
    assert assess_response(
        "According to the manual it fails because the relay overheats, but "
        "I have not checked the manual claim.", D) == ASSERTED


# ---------------------------------------------------------------------------
# Owner-required accepted cases (same-sentence directional substance).
# ---------------------------------------------------------------------------

_OWNER_REQUIRED_REASONED_CASES = [
    ("because", "The enclosure should use a sealed sensor chamber because "
                "dust buildup can distort the sensor reading and cause "
                "false alarms."),
    ("since", "The relay should retain the local threshold since the sensor "
              "must continue operating when connectivity is unavailable."),
    ("therefore", "The sensor voltage continues drifting as the enclosure "
                  "heats; therefore the fan relay should remain active "
                  "until the reading recovers."),
    ("due to", "The relay contacts may weld due to motor inrush current "
               "exceeding their rated capacity."),
    ("as a result", "The sensor voltage drifts as the enclosure heats; as a "
                    "result the controller may activate the fan too late."),
    ("thus", "The relay coil heats rapidly under continuous load; thus the "
             "enclosure needs a vent path."),
    ("hence", "The sensor output saturates near strong magnetic fields; "
              "hence the mounting location matters."),
]


@pytest.mark.parametrize("label,text", _OWNER_REQUIRED_REASONED_CASES)
def test_owner_required_accepted_cases_are_reasoned(label, text):
    assert assess_response(text, D) == REASONED, label


def test_owner_required_token_stuffing_is_the_known_residual_false_positive():
    # HONEST DISCLOSURE (owner-required): this stuffing case satisfies the
    # formally authorized lexical gate (whole-word substance "sensor" in the
    # same-sentence rationale side of "because" + length >= 40) and is the
    # single known residual false positive of the sentence-bounded gate. It
    # is pinned here so any future change to this behavior is visible; it is
    # NOT hidden or tuned around.
    assert assess_response(
        "It works because sensor relay resistor battery controller.",
        D) == REASONED


# ---------------------------------------------------------------------------
# Fixed review matrix (owner-required, >= 85 cases). Committed as test data
# so the final independent review can reproduce the FP/FN claim exactly.
# Each entry: (case_id, text, expected_classification, semantically_reasoned)
# where semantically_reasoned is the honest judgment of whether the response
# states the owner's own substantive reasoning (used only for FP/FN
# accounting; the test asserts expected_classification exactly).
# ---------------------------------------------------------------------------

_R, _A = REASONED, ASSERTED
_REVIEW_MATRIX = (
    # --- owner-required accepted (same-sentence directional substance) ---
    ("own-acc-because", "The enclosure should use a sealed sensor chamber because dust buildup can distort the sensor reading and cause false alarms.", _R, True),
    ("own-acc-since", "The relay should retain the local threshold since the sensor must continue operating when connectivity is unavailable.", _R, True),
    ("own-acc-therefore", "The sensor voltage continues drifting as the enclosure heats; therefore the fan relay should remain active until the reading recovers.", _R, True),
    ("own-acc-dueto", "The relay contacts may weld due to motor inrush current exceeding their rated capacity.", _R, True),
    ("own-acc-asresult", "The sensor voltage drifts as the enclosure heats; as a result the controller may activate the fan too late.", _R, True),
    ("own-acc-thus", "The relay coil heats rapidly under continuous load; thus the enclosure needs a vent path.", _R, True),
    ("own-acc-hence", "The sensor output saturates near strong magnetic fields; hence the mounting location matters.", _R, True),
    # --- original PR accepted set (unchanged under sentence bounding) ---
    ("pr-acc-because", "Fan must continue because sensor still reads high temperature and enclosure has not cooled.", _R, True),
    ("pr-acc-since", "The threshold stays stored locally since the sensor and relay must keep operating offline.", _R, True),
    ("pr-acc-therefore", "The relay coil overheats during long operation; therefore the enclosure needs a cooling vent.", _R, True),
    ("pr-acc-thus", "The capacitor keeps discharging through the coil; thus the alarm stays powered in a brownout.", _R, True),
    ("pr-acc-hence", "The battery voltage sags under motor load; hence the alarm needs a separate supply rail.", _R, True),
    ("pr-acc-dueto", "The relay contacts may weld due to the motor inrush current exceeding their rated capacity.", _R, True),
    ("pr-acc-asresult", "The sensor voltage drifts as the enclosure heats; as a result the controller may trigger the fan too late.", _R, True),
    # --- cross-sentence leakage (owner-required rejections) ---
    ("leak-cause", "It fails because the spring is weak. The sensor is a separate part entirely.", _A, True),
    ("leak-result", "The sensor is a separate part entirely. Therefore the design is good.", _A, False),
    ("leak-unrelated", "It works because the design is popular. A relay is used elsewhere in the product.", _A, False),
    ("leak-newline-cause", "It fails because the spring is weak\nThe sensor is a separate part entirely", _A, True),
    ("leak-newline-result", "The sensor is a separate part entirely\nTherefore the design is good and useful", _A, False),
    # --- wrong directional side ---
    ("side-cause-before", "The sensor fails constantly because the spring is far too weak for this design.", _A, True),
    ("side-result-after", "The design is elegant and simple; therefore the sensor will work reliably every time.", _A, False),
    ("side-cause-before2", "The relay clicks loudly because the case has no padding inside it at all.", _A, True),
    ("side-result-after2", "It looks finished now; hence the battery compartment should be fine as designed.", _A, False),
    # --- multiple connective occurrences ---
    ("multi-none-valid", "The sensor is reliable because it is nice. The design is slow therefore it is safe.", _A, False),
    ("multi-one-valid", "It is nice because people like it. The alarm stays on because the sensor still reads heat.", _R, True),
    ("multi-result-second", "Therefore it is good. The relay coil saturates under load; therefore the driver needs a diode.", _R, True),
    ("multi-same-sentence", "The fan runs because the sensor overheats when dust blocks the vent slots.", _R, True),
    # --- quotes / attribution / negation (owner-required rejections) ---
    ("quote-owner", 'Someone said "the sensor fails because the relay overheats," but I have not verified that explanation.', _A, False),
    ("attrib-owner", "An engineer told me the sensor fails because the relay overheats, but I have not confirmed it.", _A, False),
    ("negation-owner", "The sensor does not fail because the relay overheats; I do not know the actual cause.", _A, False),
    ("quote-curly", "Someone wrote “it fails because the relay overheats” but I have not verified anything myself.", _A, False),
    ("attrib-says", "My colleague says it fails because the relay overheats, but I cannot explain the mechanism.", _A, False),
    ("attrib-according", "According to the manual it fails because the relay overheats, but I have not checked the manual claim.", _A, False),
    ("negation-never", "The alarm never fires because the sensor threshold is high, and I have not investigated further.", _A, False),
    ("quote-substancefree", "Someone said the sensor fails because heat is bad, but I have not checked anything.", _A, False),
    ("attrib-video", "A video claims it breaks because of bad wiring, but I did not verify the claim at all.", _A, False),
    ("negation-metalcase", "It does not overheat because of the metal case, and I have not found the real cause.", _A, False),
    # --- temporal since ---
    ("temporal-owner", "Since Tuesday the sensor prototype has been on my desk and I have been thinking about it.", _A, False),
    ("temporal-thinking", "Since Tuesday I have been thinking about this invention and it seems very interesting.", _A, False),
    ("temporal-sketch", "Since yesterday I have been sketching the case shape and thinking about the colors.", _A, False),
    ("since-initial-causal", "Since the sensor must stay powered at night, the relay latches the supply on.", _A, True),
    # --- stuffing ---
    ("stuff-owner-residual-fp", "It works because sensor relay resistor battery controller.", _R, False),
    ("stuff-preconnective", "Sensor relay battery voltage current chip resistor. It is great because it is nice.", _A, False),
    ("stuff-post-result", "It is nice and everyone likes it very much; therefore sensor relay battery voltage.", _A, False),
    ("stuff-numeric", "It scores 12345 because 99999 88888 77777 66666 55555 44444 33333 22222 11111 00000.", _A, False),
    ("stuff-connectives", "Because because because therefore hence thus due to as a result it is wonderful today.", _A, False),
    ("stuff-repeat-because", "Because it is good because it is useful because it is innovative.", _A, False),
    # --- substring traps (whole-word matching) ---
    ("trap-nice-device", "It is a good device because everyone thinks it is very nice and useful.", _A, False),
    ("trap-which", "This matters because everyone can tell which parts feel nice and which do not.", _A, False),
    ("trap-called-enabled", "The feature works because it is called smart mode and stays enabled all day long.", _A, False),
    ("trap-especially-hallway", "People like it because it is especially handy in the kitchen and hallway areas.", _A, False),
    ("trap-shall", "We shall win because we shall try harder and we shall never give up on this plan.", _A, False),
    # --- explicit safe plural aliases ---
    ("plural-resistors", "The cabinet needs venting because the resistors and batteries overheat during long idle periods.", _R, True),
    ("plural-relays", "Contacts wear out quickly because the relays switch at full motor load every few seconds.", _R, True),
    ("plural-capacitors", "The supply sags briefly because the capacitors leak charge during cold storage months.", _R, True),
    ("plural-motors", "The chassis vibrates loudly because the motors stall under heavy load without extra cooling.", _R, True),
    ("plural-leds", "The panel stays visible because the leds shine through the diffuser at night.", _R, True),
    ("plural-ics", "The board runs hot because the ics draw current constantly at full clock speed.", _R, True),
    ("plural-nonsignal", "The box needs padding because the parts and wires and cases rattle during transport.", _A, True),
    ("plural-things", "It helps because the things inside it are arranged nicely and packed very well.", _A, False),
    # --- unsafe generic-fold artifacts (owner-required ASSERTED; no alias) ---
    ("plural-unsafe-ices", "The dessert stays cold because the ices melt slowly in the insulated serving tray.", _A, False),
    ("plural-unsafe-halls", "The venue works well because the halls stay quiet during the evening events.", _A, False),
    ("plural-unsafe-chips", "The snack bowl empties fast because the chips taste salty and fresh every single day.", _A, False),
    ("plural-unsafe-displays", "The kiosk attracts attention because it displays bright messages all day long.", _A, False),
    # --- praise / weak placeholders / weak patterns ---
    ("praise", "It is nice because everyone loves how it looks on the kitchen counter every day.", _A, False),
    ("weak-technology", "It works because technology makes everything better somehow.", _A, False),
    ("weak-stuff", "It helps because something in the box does stuff somehow every day.", _A, False),
    ("weak-exact", "i don't know", _A, False),
    # --- punctuation adjacency / case forms / whitespace ---
    ("punct-initial-because", "Because the sensor overheats quickly in the sealed box, the fan must run longer than one minute.", _R, True),
    ("punct-paren", "The vent stays open longer (because the sensor cools slowly) and the alarm still sounds.", _R, True),
    ("punct-commas", "It matters, because the sensor drifts, in many operating cases indoors.", _R, True),
    ("case-upper", "FAN MUST CONTINUE BECAUSE SENSOR STILL READS HIGH TEMPERATURE AND ENCLOSURE HAS NOT COOLED.", _R, True),
    ("case-mixed", "Fan Must Continue Because Sensor Still Reads High Temperature And Enclosure Has Not Cooled.", _R, True),
    ("ws-multiword", "The relay contacts may weld due  to the motor inrush current exceeding their rated capacity.", _R, True),
    ("ws-newline-connective", "The relay contacts may weld due\nto motor inrush current exceeding their rated capacity", _A, True),
    # --- empty / short / boundary lengths ---
    ("short-under20", "because sensor bad", _A, False),
    ("short-under40", "It fails because relay dies.", _A, True),
    ("result-empty-side", "The sensor voltage drifts constantly upward; therefore.", _A, False),
    # --- existing-path controls (must remain byte-identical behavior) ---
    ("ctl-hall-sensor", "A Hall sensor detects magnetic field changes by measuring voltage perpendicular to current flow, enabling contactless position detection.", _R, True),
    ("ctl-when", "When the load current exceeds the limit, the relay opens so that the wiring stays safe.", _R, True),
    ("ctl-brake", "A bicycle brake light that turns on when the rider decelerates, using a sensor to detect slowing down.", _R, True),
    ("ctl-generic-verb", "it uses a sensor and connects to wifi and sends alerts to the phone app every day", _A, True),
    ("ctl-alerts-short", "It alerts people.", _A, False),
    ("ctl-plain-claim", "This is the best invention for kitchens and it will help many families every single day.", _A, False),
    # --- generic-verb trap interplay ---
    ("trap-yield-because", "It uses a relay because the sensor current spikes past the safe threshold quickly.", _R, True),
    ("trap-hold-substancefree", "It uses batteries because everyone says it is very nice and quite useful overall.", _A, False),
    ("trap-hold-noconnective", "It uses a small box and it sends alerts and everyone can use it easily.", _A, False),
    ("trap-yield-asresult", "The sensor voltage drifts as the enclosure heats; as a result the controller may activate the fan too late again.", _R, True),
    # --- known false negatives (documented; substance-free rationale) ---
    ("fn-dust-thermal", "The device should use a sealed sensor chamber because dust buildup can distort the thermal readings and cause false alarms.", _A, True),
    ("fn-connectivity", "The controller should retain the previous threshold locally since internet connectivity may be unavailable during a fault.", _A, True),
    ("fn-noconnective-chain", "The thermistor resistance drops with heat. The comparator output flips at 2.5 volts. The relay coil energizes and disconnects the load.", _A, True),
    ("fn-scope-boundary", "The device covers only single-phase circuits because three-phase fault currents exceed the sensor's saturation limit.", _R, True),
    # --- additional same-sentence acceptance/rejection variants ---
    ("acc-semicolon-kept", "The battery drains overnight; the alarm still fires because the sensor stays powered from the backup rail.", _R, True),
    ("rej-question-boundary", "Does it matter because of noise? The sensor sits in a separate shielded box.", _A, False),
    ("rej-exclaim-boundary", "It fails because the hinge sticks! The sensor is mounted somewhere else entirely.", _A, True),
    ("acc-question-sentence", "Should the fan keep running because the sensor still reports heat above the limit?", _R, True),
    ("rej-substance-only-claimside-result", "The enclosure looks strong; therefore it will survive the drop test easily.", _A, False),
    ("acc-result-both-sides", "The relay coil saturates under sustained load; therefore the driver transistor needs a flyback diode.", _R, True),
    ("rej-two-sentences-no-substance", "It fails because the spring is weak. It also rattles during hard shaking.", _A, True),
    ("rej-guard-not-before-dueto", "The failure is not due to the sensor wiring, and I have not found the true cause.", _A, False),
)


def test_review_matrix_has_at_least_85_cases_with_unique_ids():
    assert len(_REVIEW_MATRIX) >= 85
    ids = [case_id for case_id, _, _, _ in _REVIEW_MATRIX]
    assert len(ids) == len(set(ids))


@pytest.mark.parametrize(
    "case_id,text,expected,_sem",
    _REVIEW_MATRIX,
    ids=[c[0] for c in _REVIEW_MATRIX])
def test_review_matrix_case(case_id, text, expected, _sem):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        assert assess_response(text, D) == expected, case_id


def test_review_matrix_fp_fn_totals_are_pinned_and_honest():
    # FP = classified REASONED without genuine owner reasoning;
    # FN = genuine owner reasoning classified ASSERTED.
    fps = [c for c, _, exp, sem in _REVIEW_MATRIX if exp == REASONED and not sem]
    fns = [c for c, _, exp, sem in _REVIEW_MATRIX if exp == ASSERTED and sem]
    # The single known residual false positive is the owner-disclosed token
    # stuffing case; no other false positive exists in the matrix.
    assert fps == ["stuff-owner-residual-fp"]
    # Known false negatives are the documented conservative cost of the
    # sentence-bounded gate and its guards (substance-free rationale clauses,
    # vocabulary gaps, temporal-since guard, line-break-split connective,
    # cross-sentence claim splits, short answers).
    assert len(fns) == len([
        c for c, _, exp, sem in _REVIEW_MATRIX if exp == ASSERTED and sem])
    assert 8 <= len(fns) <= 16, fns
