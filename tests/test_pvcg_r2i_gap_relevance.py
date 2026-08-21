"""PVCG-R2-I — gap-relevance / manufactured-satisfaction hardening.

File path        : tests/test_pvcg_r2i_gap_relevance.py
Purpose          : prove the PVCG-R2-C §4 product truth at the live answer→gap
                   seam — a response may influence gap satisfaction only when it
                   is sufficiently relevant to the specific served gap/question
                   context, deterministically and fail-closed.
Governing        : docs/governance/PVCG_R2_C_GAP_RELEVANCE_HARDENING_CONTRACT.md
                   (AUTHORITATIVE, PR #548, merge 4d746d15…) §4, §6, §8, §9.
Input contract   : the public engine surface only —
                   engine.progression_loop.integrate_response / assess_response
                   and engine.gap_relevance.addresses_gap. No Flask app, no
                   database, no network, no filesystem.
Output contract  : deterministic pass/fail assertions over gap.status,
                   transition result, known_mechanism / known_problem, Stage-3
                   evidence capture and the pure eligibility predicate.
Prohibited       : asserting on wall-clock, randomness, model output or any
                   external call; special-casing one hard-coded sentence;
                   asserting semantic understanding or multilingual equivalence
                   (that is PVCG-R3, explicitly out of scope — see
                   test_lexical_bound_is_documented_not_concealed).

Truthful description of the mechanism under test: it is LEXICAL and
deterministic. It matches governed per-gap intent vocabulary. It does not
understand meaning, does not stabilise paraphrase, and does not work across
languages. Those bounds are asserted here on purpose, not concealed.
"""

import warnings

import pytest

from engine.idea_state import (
    IdeaState, Gap,
    OPEN, PARTIAL, CLOSED,
    ASSERTED, REASONED,
    MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY,
    PROBLEM_MECHANISM_FIT, ASSUMPTION_INVENTORY, EXPERTISE_GAP_AWARENESS,
    STAGE_3_GAP_TYPES,
)
from engine.progression_loop import assess_response, integrate_response

DOMAIN = "electronics_electrical"

ALL_GAPS = (
    MECHANISM_COMPLETENESS,
    PHYSICAL_FEASIBILITY,
    BOUNDARY_AMBIGUITY,
    PROBLEM_MECHANISM_FIT,
    ASSUMPTION_INVENTORY,
    EXPERTISE_GAP_AWARENESS,
)

# ---------------------------------------------------------------------------
# Corpora.
#
# OFF_TOPIC: three DIFFERENT signal-rich, causally-structured answers that
# answer none of the six governed questions. Three variants (not one sentence)
# so no implementation can pass by special-casing a literal string.
# ---------------------------------------------------------------------------
OFF_TOPIC = {
    "components-list": (
        "The circuit uses a sensor and a relay and a capacitor and a resistor, "
        "and the voltage increases because the current flows through the "
        "microcontroller."
    ),
    "board-inventory": (
        "The board carries a transistor, a capacitor and an led, and the "
        "analog signal rises because the voltage across the resistor grows."
    ),
    "enclosure-inventory": (
        "Inside the enclosure there is a microcontroller, a display and a "
        "motor, and the digital data changes because the threshold voltage "
        "rises."
    ),
}

# One genuinely gap-appropriate answer per governed gap type. Each is REASONED
# under the EXISTING quality rules (R2 changes no quality rule) and each carries
# the intent vocabulary of its own governed question and of no other.
GENUINE = {
    MECHANISM_COMPLETENESS: (
        "The current sensor detects an abnormal rise because the shunt "
        "resistor voltage increases, therefore the microcontroller opens the "
        "relay to disconnect the appliance."
    ),
    PHYSICAL_FEASIBILITY: (
        "The design relies on resistive sensing and consumes about 20 "
        "milliamps from a 5 volt supply, because the resistor and the "
        "microcontroller draw continuous current, therefore the temperature "
        "range must stay modest."
    ),
    BOUNDARY_AMBIGUITY: (
        "It does not cover gas leaks or overheating ovens, which means those "
        "hazards stay outside its scope; the current threshold is restricted "
        "to electrical faults and the core cannot be replaced."
    ),
    PROBLEM_MECHANISM_FIT: (
        "The problem is that people leave faulty appliances plugged in and the "
        "risk matters to them, therefore this relay based approach solves it "
        "rather than a fuse because the current sensor acts earlier."
    ),
    ASSUMPTION_INVENTORY: (
        "I am assuming the resistor stays accurate over time, because the "
        "current sensor calibration was never re-checked, therefore that "
        "assumption is unverified and untested."
    ),
    EXPERTISE_GAP_AWARENESS: (
        "Building this needs power electronics expertise, because the relay "
        "and the microcontroller firmware must be certified, therefore I would "
        "need to consult a specialist engineer."
    ),
}

# A SHORT but genuinely relevant mechanism answer (adversarial case 6).
SHORT_RELEVANT_MECHANISM = (
    "The sensor detects the fault, therefore the relay opens the contact."
)

# Materially different gap pairs that must not be interchangeable. These span
# two Stage-2 pairs and one Stage-3 pair, so the proof is not one gap family.
MATERIALLY_DIFFERENT_PAIRS = (
    (MECHANISM_COMPLETENESS, BOUNDARY_AMBIGUITY),
    (BOUNDARY_AMBIGUITY, MECHANISM_COMPLETENESS),
    (ASSUMPTION_INVENTORY, EXPERTISE_GAP_AWARENESS),
    (MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY),
    (PROBLEM_MECHANISM_FIT, ASSUMPTION_INVENTORY),
)


# ---------------------------------------------------------------------------
# Helpers — no Flask, no I/O, no persistence.
# ---------------------------------------------------------------------------
def _state():
    state = IdeaState(idea_id="pvcg-r2i", domain_signal=DOMAIN)
    state.domain = DOMAIN
    return state


def _with_gap(gap_type, status=OPEN):
    state = _state()
    state.gaps.append(Gap(gap_type=gap_type, status=status, opened_at=0))
    return state


def _serve(state, gap_type, answer):
    """Drive exactly one answer through the single live answer→gap seam."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return integrate_response(state, gap_type, "served question", answer)


def _deliver_until_closed_attempt(gap_type, answer, times):
    """Serve the same answer `times` times against a freshly opened gap."""
    state = _with_gap(gap_type)
    results = [_serve(state, gap_type, answer) for _ in range(times)]
    return state, results


# ---------------------------------------------------------------------------
# Corpus self-checks — keep the RED/GREEN evidence honest.
# ---------------------------------------------------------------------------
class TestCorpusPreconditions:
    """The corpus must actually be signal-rich, or the RED proof is vacuous."""

    @pytest.mark.parametrize("label", sorted(OFF_TOPIC))
    def test_off_topic_answers_are_reasoned_quality(self, label):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            assert assess_response(OFF_TOPIC[label], DOMAIN) == REASONED, (
                "the off-topic corpus must be REASONED under the EXISTING "
                "quality rules, otherwise it could not manufacture "
                "satisfaction and the defect proof would be vacuous"
            )

    @pytest.mark.parametrize("gap_type", ALL_GAPS)
    def test_genuine_answers_are_reasoned_quality(self, gap_type):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            assert assess_response(GENUINE[gap_type], DOMAIN) == REASONED

    def test_short_relevant_answer_is_reasoned_quality(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            assert assess_response(SHORT_RELEVANT_MECHANISM, DOMAIN) == REASONED

    def test_off_topic_corpus_has_three_distinct_answers(self):
        assert len(set(OFF_TOPIC.values())) == 3


# ---------------------------------------------------------------------------
# RED-1 — manufactured satisfaction.
# ---------------------------------------------------------------------------
class TestRed1ManufacturedSatisfaction:
    """A signal-rich but off-topic answer must not satisfy or close a gap."""

    @pytest.mark.parametrize("gap_type", ALL_GAPS)
    @pytest.mark.parametrize("label", sorted(OFF_TOPIC))
    def test_off_topic_answer_never_closes_the_served_gap(self, gap_type, label):
        state, results = _deliver_until_closed_attempt(
            gap_type, OFF_TOPIC[label], times=2)
        gap = state.get_gap(gap_type)
        assert gap.status != CLOSED, (
            f"{label} closed {gap_type} without addressing it"
        )
        assert gap.closed_at is None
        assert all(r[0] != "PASS" for r in results)

    @pytest.mark.parametrize("gap_type", ALL_GAPS)
    @pytest.mark.parametrize("label", sorted(OFF_TOPIC))
    def test_off_topic_answer_does_not_advance_gap_status(self, gap_type, label):
        state = _with_gap(gap_type)
        _serve(state, gap_type, OFF_TOPIC[label])
        assert state.get_gap(gap_type).status == OPEN, (
            "an answer that does not address the served gap must not move the "
            "gap toward closure (PARTIAL is a step toward CLOSED)"
        )

    @pytest.mark.parametrize("label", sorted(OFF_TOPIC))
    def test_off_topic_answer_does_not_establish_known_mechanism(self, label):
        state = _with_gap(MECHANISM_COMPLETENESS)
        _serve(state, MECHANISM_COMPLETENESS, OFF_TOPIC[label])
        assert state.known_mechanism is None

    @pytest.mark.parametrize("gap_type", ALL_GAPS)
    @pytest.mark.parametrize("label", sorted(OFF_TOPIC))
    def test_off_topic_answer_does_not_establish_known_problem(
            self, gap_type, label):
        state = _with_gap(gap_type)
        _serve(state, gap_type, OFF_TOPIC[label])
        assert state.known_problem is None

    @pytest.mark.parametrize("gap_type", sorted(STAGE_3_GAP_TYPES))
    @pytest.mark.parametrize("label", sorted(OFF_TOPIC))
    def test_off_topic_answer_is_not_captured_as_stage3_evidence(
            self, gap_type, label):
        state = _with_gap(gap_type)
        _serve(state, gap_type, OFF_TOPIC[label])
        assert state.get_gap(gap_type).evidence == []

    @pytest.mark.parametrize("label", sorted(OFF_TOPIC))
    def test_off_topic_answer_cannot_close_a_partial_gap(self, label):
        """The PARTIAL→CLOSED shortcut must not be reachable off-topic."""
        state = _with_gap(MECHANISM_COMPLETENESS, status=PARTIAL)
        transition, _ = _serve(state, MECHANISM_COMPLETENESS, OFF_TOPIC[label])
        assert transition != "PASS"
        assert state.get_gap(MECHANISM_COMPLETENESS).status == PARTIAL


# ---------------------------------------------------------------------------
# RED-2 — cross-gap answer reuse.
# ---------------------------------------------------------------------------
class TestRed2CrossGapAnswerReuse:
    """An answer written for Gap A must not automatically satisfy Gap B."""

    @pytest.mark.parametrize("source_gap,target_gap", MATERIALLY_DIFFERENT_PAIRS)
    def test_answer_for_one_gap_does_not_close_a_different_gap(
            self, source_gap, target_gap):
        state, results = _deliver_until_closed_attempt(
            target_gap, GENUINE[source_gap], times=2)
        assert state.get_gap(target_gap).status != CLOSED, (
            f"the {source_gap} answer closed {target_gap}"
        )
        assert all(r[0] != "PASS" for r in results)

    @pytest.mark.parametrize("source_gap,target_gap", MATERIALLY_DIFFERENT_PAIRS)
    def test_answer_for_one_gap_does_not_advance_a_different_gap(
            self, source_gap, target_gap):
        state = _with_gap(target_gap)
        _serve(state, target_gap, GENUINE[source_gap])
        assert state.get_gap(target_gap).status == OPEN

    def test_each_genuine_answer_closes_only_its_own_gap(self):
        """Full 6x6 matrix — the diagonal progresses, the rest must not close."""
        closed = {}
        for answer_gap in ALL_GAPS:
            for served_gap in ALL_GAPS:
                state, _ = _deliver_until_closed_attempt(
                    served_gap, GENUINE[answer_gap], times=2)
                closed[(answer_gap, served_gap)] = (
                    state.get_gap(served_gap).status == CLOSED)
        for answer_gap in ALL_GAPS:
            assert closed[(answer_gap, answer_gap)] is True, (
                f"the genuine {answer_gap} answer must still progress"
            )
        off_diagonal = [k for k, v in closed.items() if k[0] != k[1] and v]
        assert off_diagonal == [], (
            f"answers closed gaps they do not address: {off_diagonal}"
        )


# ---------------------------------------------------------------------------
# RED-3 — repetition must not manufacture satisfaction.
# ---------------------------------------------------------------------------
class TestRed3RepetitionCannotManufactureSatisfaction:

    @pytest.mark.parametrize("gap_type", ALL_GAPS)
    @pytest.mark.parametrize("label", sorted(OFF_TOPIC))
    def test_five_repetitions_of_an_irrelevant_answer_never_close(
            self, gap_type, label):
        state, results = _deliver_until_closed_attempt(
            gap_type, OFF_TOPIC[label], times=5)
        assert state.get_gap(gap_type).status != CLOSED
        assert all(r[0] != "PASS" for r in results)

    @pytest.mark.parametrize("gap_type", ALL_GAPS)
    def test_repetition_outcome_is_stable_not_cumulative(self, gap_type):
        state, results = _deliver_until_closed_attempt(
            gap_type, OFF_TOPIC["components-list"], times=4)
        assert len({r for r in results}) == 1, (
            "repeating an irrelevant answer must not accumulate credit"
        )


# ---------------------------------------------------------------------------
# RED-4 / §10 — legitimate answers are preserved.
# ---------------------------------------------------------------------------
class TestRed4LegitimateAnswerControl:

    @pytest.mark.parametrize("gap_type", ALL_GAPS)
    def test_relevant_reasoned_answer_progresses_then_closes(self, gap_type):
        state = _with_gap(gap_type)
        first, _ = _serve(state, gap_type, GENUINE[gap_type])
        assert first == "WARN"
        assert state.get_gap(gap_type).status == PARTIAL
        second, _ = _serve(state, gap_type, GENUINE[gap_type])
        assert second == "PASS"
        assert state.get_gap(gap_type).status == CLOSED

    def test_relevant_mechanism_answer_still_establishes_known_mechanism(self):
        state = _with_gap(MECHANISM_COMPLETENESS)
        _serve(state, MECHANISM_COMPLETENESS, GENUINE[MECHANISM_COMPLETENESS])
        assert state.known_mechanism is not None
        assert state.known_mechanism.content == GENUINE[MECHANISM_COMPLETENESS]

    @pytest.mark.parametrize("gap_type", sorted(STAGE_3_GAP_TYPES))
    def test_relevant_stage3_answer_is_still_captured_as_evidence(self, gap_type):
        state = _with_gap(gap_type)
        _serve(state, gap_type, GENUINE[gap_type])
        assert len(state.get_gap(gap_type).evidence) == 1

    def test_short_but_relevant_answer_is_not_rejected_by_relevance(self):
        """Relevance is not a length test (adversarial case 6)."""
        state = _with_gap(MECHANISM_COMPLETENESS)
        transition, _ = _serve(
            state, MECHANISM_COMPLETENESS, SHORT_RELEVANT_MECHANISM)
        assert transition == "WARN"
        assert state.get_gap(MECHANISM_COMPLETENESS).status == PARTIAL

    def test_weak_but_relevant_answer_keeps_its_existing_truthful_outcome(self):
        """Relevance is eligibility, NOT quality. A relevant ASSERTED answer
        must still receive exactly the pre-R2 ASSERTED outcome — R2 must not
        upgrade it to PASS merely because it is on topic."""
        weak_relevant = "It has some components and a few steps."
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            assert assess_response(weak_relevant, DOMAIN) == ASSERTED
        state = _with_gap(MECHANISM_COMPLETENESS)
        transition, reason = _serve(
            state, MECHANISM_COMPLETENESS, weak_relevant)
        assert transition == "WARN"
        assert "asserted only" in reason
        assert state.get_gap(MECHANISM_COMPLETENESS).status == PARTIAL


# ---------------------------------------------------------------------------
# Fail-closed semantics — §4: not eligible, never punitive.
# ---------------------------------------------------------------------------
class TestFailClosedIsNotPunitive:

    @pytest.mark.parametrize("gap_type", ALL_GAPS)
    @pytest.mark.parametrize("label", sorted(OFF_TOPIC))
    def test_irrelevant_answer_never_returns_block(self, gap_type, label):
        transition, _ = _serve(_with_gap(gap_type), gap_type, OFF_TOPIC[label])
        assert transition == "WARN"

    @pytest.mark.parametrize("gap_type", ALL_GAPS)
    def test_irrelevant_answer_never_raises(self, gap_type):
        _serve(_with_gap(gap_type), gap_type, OFF_TOPIC["board-inventory"])

    def test_irrelevant_answer_reason_is_about_the_question_not_the_inventor(self):
        _, reason = _serve(
            _with_gap(BOUNDARY_AMBIGUITY), BOUNDARY_AMBIGUITY,
            OFF_TOPIC["components-list"])
        lowered = reason.lower()
        assert "not addressed" in lowered
        for punitive in ("invalid", "wrong", "error", "contradiction",
                         "rejected", "failure"):
            assert punitive not in lowered

    def test_relevance_does_not_downgrade_recorded_quality(self):
        """The quality tier recorded for an off-topic answer is unchanged; only
        its eligibility to satisfy the served gap is withheld."""
        state = _with_gap(PHYSICAL_FEASIBILITY)
        answer = OFF_TOPIC["components-list"]
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            assert assess_response(answer, DOMAIN) == REASONED
        _serve(state, PHYSICAL_FEASIBILITY, answer)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            assert assess_response(answer, DOMAIN) == REASONED

    def test_empty_and_whitespace_answers_are_handled_without_error(self):
        for answer in ("", "   ", "\n\t"):
            transition, _ = _serve(
                _with_gap(MECHANISM_COMPLETENESS), MECHANISM_COMPLETENESS,
                answer)
            assert transition in ("WARN", "PASS", "BLOCK")


# ---------------------------------------------------------------------------
# Determinism.
# ---------------------------------------------------------------------------
class TestDeterminism:

    @pytest.mark.parametrize("gap_type", ALL_GAPS)
    def test_same_state_same_gap_same_answer_gives_same_result(self, gap_type):
        outcomes = set()
        for _ in range(12):
            state = _with_gap(gap_type)
            transition, reason = _serve(
                state, gap_type, OFF_TOPIC["enclosure-inventory"])
            outcomes.add((transition, reason, state.get_gap(gap_type).status))
        assert len(outcomes) == 1

    @pytest.mark.parametrize("gap_type", ALL_GAPS)
    def test_relevant_answer_result_is_also_deterministic(self, gap_type):
        outcomes = set()
        for _ in range(12):
            state = _with_gap(gap_type)
            transition, reason = _serve(state, gap_type, GENUINE[gap_type])
            outcomes.add((transition, reason, state.get_gap(gap_type).status))
        assert len(outcomes) == 1

    def test_eligibility_predicate_is_pure_and_repeatable(self):
        from engine.gap_relevance import addresses_gap
        for gap_type in ALL_GAPS:
            for answer in list(OFF_TOPIC.values()) + list(GENUINE.values()):
                first = addresses_gap(answer, gap_type)
                assert all(
                    addresses_gap(answer, gap_type) is first for _ in range(8))

    def test_module_imports_no_clock_random_or_network(self):
        import inspect
        import engine.gap_relevance as module
        source = inspect.getsource(module)
        for forbidden in ("import random", "import time", "datetime",
                          "requests", "urllib", "socket", "openai",
                          "anthropic", "subprocess", "os.environ"):
            assert forbidden not in source, (
                f"non-deterministic or external dependency found: {forbidden}"
            )


# ---------------------------------------------------------------------------
# Adversarial battery — directive §11 cases 1-10.
# ---------------------------------------------------------------------------
class TestAdversarialSignalStuffing:

    def test_1_long_answer_many_technical_nouns_wrong_topic(self):
        answer = (
            "The assembly contains a microcontroller, a relay, a capacitor, a "
            "resistor, a transistor, an led, a display, a motor and an "
            "ultrasonic sensor, and the analog voltage rises because the "
            "current in the circuit grows while the digital signal changes."
        )
        state, results = _deliver_until_closed_attempt(
            BOUNDARY_AMBIGUITY, answer, times=3)
        assert state.get_gap(BOUNDARY_AMBIGUITY).status != CLOSED
        assert all(r[0] != "PASS" for r in results)

    def test_2_causal_connectors_but_wrong_gap(self):
        answer = (
            "Because the capacitor charges and therefore the voltage rises, "
            "the resistor warms and thus the current through the "
            "microcontroller changes."
        )
        state, results = _deliver_until_closed_attempt(
            EXPERTISE_GAP_AWARENESS, answer, times=3)
        assert state.get_gap(EXPERTISE_GAP_AWARENESS).status != CLOSED
        assert all(r[0] != "PASS" for r in results)

    def test_3_answer_copied_from_another_gap(self):
        state, results = _deliver_until_closed_attempt(
            ASSUMPTION_INVENTORY, GENUINE[MECHANISM_COMPLETENESS], times=3)
        assert state.get_gap(ASSUMPTION_INVENTORY).status != CLOSED
        assert all(r[0] != "PASS" for r in results)

    def test_4_repeated_copied_answer(self):
        state, results = _deliver_until_closed_attempt(
            PHYSICAL_FEASIBILITY, GENUINE[BOUNDARY_AMBIGUITY], times=6)
        assert state.get_gap(PHYSICAL_FEASIBILITY).status != CLOSED
        assert all(r[0] != "PASS" for r in results)

    def test_5_relevant_answer_with_irrelevant_extra_text(self):
        answer = (
            GENUINE[MECHANISM_COMPLETENESS]
            + " Separately, the enclosure colour is blue and the packaging "
              "arrives in a cardboard box."
        )
        state = _with_gap(MECHANISM_COMPLETENESS)
        transition, _ = _serve(state, MECHANISM_COMPLETENESS, answer)
        assert transition == "WARN"
        assert state.get_gap(MECHANISM_COMPLETENESS).status == PARTIAL

    def test_6_short_genuinely_relevant_answer(self):
        state = _with_gap(MECHANISM_COMPLETENESS)
        _serve(state, MECHANISM_COMPLETENESS, SHORT_RELEVANT_MECHANISM)
        assert state.get_gap(MECHANISM_COMPLETENESS).status == PARTIAL

    def test_7_generic_mechanism_answer_presented_to_boundary_gap(self):
        state, results = _deliver_until_closed_attempt(
            BOUNDARY_AMBIGUITY, GENUINE[MECHANISM_COMPLETENESS], times=3)
        assert state.get_gap(BOUNDARY_AMBIGUITY).status != CLOSED
        assert all(r[0] != "PASS" for r in results)

    def test_8_boundary_answer_presented_to_mechanism_gap(self):
        state, results = _deliver_until_closed_attempt(
            MECHANISM_COMPLETENESS, GENUINE[BOUNDARY_AMBIGUITY], times=3)
        assert state.get_gap(MECHANISM_COMPLETENESS).status != CLOSED
        assert all(r[0] != "PASS" for r in results)

    def test_9_assumption_answer_presented_to_expertise_gap(self):
        state, results = _deliver_until_closed_attempt(
            EXPERTISE_GAP_AWARENESS, GENUINE[ASSUMPTION_INVENTORY], times=3)
        assert state.get_gap(EXPERTISE_GAP_AWARENESS).status != CLOSED
        assert all(r[0] != "PASS" for r in results)

    def test_10_same_answer_same_state_is_deterministic(self):
        seen = set()
        for _ in range(10):
            state = _with_gap(PROBLEM_MECHANISM_FIT)
            result = _serve(
                state, PROBLEM_MECHANISM_FIT, GENUINE[EXPERTISE_GAP_AWARENESS])
            seen.add((result, state.get_gap(PROBLEM_MECHANISM_FIT).status))
        assert len(seen) == 1


# ---------------------------------------------------------------------------
# Gap-awareness — the guard must read the ACTUAL served gap type.
# ---------------------------------------------------------------------------
class TestGapAwareness:

    def test_same_answer_is_eligible_for_one_gap_and_not_another(self):
        from engine.gap_relevance import addresses_gap
        answer = GENUINE[MECHANISM_COMPLETENESS]
        assert addresses_gap(answer, MECHANISM_COMPLETENESS) is True
        assert addresses_gap(answer, BOUNDARY_AMBIGUITY) is False

    def test_eligibility_differs_across_at_least_two_gap_families(self):
        from engine.gap_relevance import addresses_gap
        stage2 = addresses_gap(
            GENUINE[PHYSICAL_FEASIBILITY], PHYSICAL_FEASIBILITY)
        stage3 = addresses_gap(
            GENUINE[PHYSICAL_FEASIBILITY], EXPERTISE_GAP_AWARENESS)
        assert stage2 is True and stage3 is False

    def test_every_governed_gap_type_has_its_own_intent_family(self):
        from engine.gap_relevance import GOVERNED_GAP_TYPES
        assert set(GOVERNED_GAP_TYPES) == set(ALL_GAPS)

    def test_unknown_gap_type_is_fail_closed(self):
        from engine.gap_relevance import addresses_gap
        assert addresses_gap(GENUINE[MECHANISM_COMPLETENESS], "NOT_A_GAP") is False
        assert addresses_gap(GENUINE[MECHANISM_COMPLETENESS], None) is False

    def test_non_string_response_is_fail_closed(self):
        from engine.gap_relevance import addresses_gap
        for bad in (None, 42, [], {}, object()):
            assert addresses_gap(bad, MECHANISM_COMPLETENESS) is False

    def test_no_single_sentence_is_special_cased(self):
        """No literal corpus sentence may appear in the implementation."""
        import inspect
        import engine.gap_relevance as module
        source = inspect.getsource(module)
        for sentence in list(OFF_TOPIC.values()) + list(GENUINE.values()):
            assert sentence not in source
            assert sentence[:40] not in source


# ---------------------------------------------------------------------------
# Declared bounds — R2 is not R3. Stated, not concealed.
# ---------------------------------------------------------------------------
class TestDeclaredLexicalBounds:

    def test_lexical_bound_is_documented_not_concealed(self):
        import engine.gap_relevance as module
        doc = (module.__doc__ or "").lower()
        assert "lexical" in doc
        assert "not" in doc and "semantic" in doc

    def test_non_english_paraphrase_is_not_recognised_r3_bound(self):
        """PVCG-R3 territory. An Arabic mechanism answer is NOT recognised by
        this lexical guard. This is a KNOWN BOUND of R2, asserted here so the
        limitation is visible in the test record rather than implied away."""
        from engine.gap_relevance import addresses_gap
        arabic_mechanism_answer = (
            "المستشعر يكشف الارتفاع غير الطبيعي في التيار، لذلك يفتح المتحكم "
            "الدقيق المرحل لفصل الجهاز."
        )
        assert addresses_gap(
            arabic_mechanism_answer, MECHANISM_COMPLETENESS) is False

    def test_guard_makes_no_multilingual_or_understanding_claim(self):
        import inspect
        import engine.gap_relevance as module
        source = inspect.getsource(module).lower()
        for overclaim in ("semantic understanding", "understands meaning",
                          "multilingual", "meaning-level"):
            assert overclaim not in source


# ---------------------------------------------------------------------------
# PVCG-R1 parallel tracks must be untouched by R2.
# ---------------------------------------------------------------------------
class TestR1ParallelTrackUnaffected:

    def test_acknowledged_unknown_still_recorded_for_irrelevant_answer(self):
        """The acknowledged-unknown track is explicitly unconditional and must
        stay unconditional — R2 governs satisfaction eligibility only."""
        state = _with_gap(BOUNDARY_AMBIGUITY)
        answer = (
            "I don't know how the capacitor and the resistor behave over a "
            "long period, and I have not measured it yet at all."
        )
        _serve(state, BOUNDARY_AMBIGUITY, answer)
        assert len(state.acknowledged_unknowns) == 1

    def test_gap_is_created_when_absent_even_for_irrelevant_answer(self):
        """The pre-R2 gap-creation behaviour is unchanged."""
        state = _state()
        _serve(state, MECHANISM_COMPLETENESS, OFF_TOPIC["board-inventory"])
        assert state.get_gap(MECHANISM_COMPLETENESS) is not None
