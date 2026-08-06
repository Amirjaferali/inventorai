"""
tests/test_acknowledged_unknown_fragment_capture.py

Owner-authorized 2026-07-10: acknowledged-unknown FRAGMENT capture only.

Defect fixed: _detect_acknowledged_unknown stored the WHOLE submitted
response as the acknowledged unknown (verbatim = full response), so a
substantive answer containing one bounded unknown sentence was displayed in
full under "What You Have Marked as Not Yet Known".

Correction under test: only the inventor-written sentence containing the
explicit unknown marker is stored as the acknowledged unknown. The full
answer remains verbatim in every authoritative answer store (Evidence,
transcript, interaction ledger). Scoring, gap lifecycle, maturity,
iteration behavior, and the explicit "unknown" non-answer action are
unchanged.
"""
import os
from test_p4_1b2a_durable_answer_append import answered_post  # P4-1b-2a
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.idea_state import (  # noqa: E402
    IdeaState, Gap, AcknowledgedUnknown,
    MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY,
    OPEN, PARTIAL,
)
from engine.progression_loop import (  # noqa: E402
    _detect_acknowledged_unknown, _extract_unknown_fragment,
    assess_response, integrate_response,
)
from web.app import app, SESSION_STORE, DOMAIN_CONFIRM_VALUE  # noqa: E402


DEMO_UNKNOWN_SENTENCE = ("What I do not know yet is how much dust "
                         "accumulation will affect the thermal sensor.")

DEMO_ANSWER = (
    "The thermal sensor measures the heatsink temperature because the "
    "resistance of the thermistor changes with heat, which produces a "
    "measurable voltage change at the ADC input. The microcontroller "
    "compares the sampled value against a configured threshold and "
    "triggers the fan relay when the limit is exceeded. "
    + DEMO_UNKNOWN_SENTENCE
)


def _state(domain="electronics_electrical"):
    s = IdeaState(idea_id="frag", domain_signal=domain)
    s.domain = domain  # normally set by run_iteration()
    return s


# ─────────────────────────────────────────────
# Required test 1 — response that IS the unknown statement
# ─────────────────────────────────────────────

class TestWholeStatementResponses:
    def test_short_canonical_statement_keeps_conservative_length_gate(self):
        # Pre-existing conservative behavior, unchanged by this fix: responses
        # below the minimum length create no acknowledged-unknown record (the
        # explicit "I do not know this yet" ACTION is the honest path for
        # this). The fragment correction does not broaden detection.
        assert _detect_acknowledged_unknown(
            "I do not know this yet.", MECHANISM_COMPLETENESS, 1) is None

    def test_single_sentence_unknown_captured_whole(self):
        r = ("I do not know this yet and have no basis to estimate the "
             "sensor drift at all.")
        result = _detect_acknowledged_unknown(r, MECHANISM_COMPLETENESS, 1)
        assert result is not None
        # The whole response IS the unknown statement (single sentence), so
        # storing it whole is correct.
        assert result.verbatim == r


# ─────────────────────────────────────────────
# Required tests 2-5 — bounded fragment extraction
# ─────────────────────────────────────────────

class TestBoundedFragment:
    def test_demo_class_unknown_sentence_last(self):
        result = _detect_acknowledged_unknown(
            DEMO_ANSWER, MECHANISM_COMPLETENESS, 3)
        assert result is not None
        assert result.verbatim == DEMO_UNKNOWN_SENTENCE
        # Nothing the inventor did not write; exact substring of the answer.
        assert result.verbatim in DEMO_ANSWER

    def test_full_answer_preserved_in_evidence_store(self):
        state = _state()
        integrate_response(state, MECHANISM_COMPLETENESS, "Q?", DEMO_ANSWER)
        # Authoritative in-engine answer storage keeps the FULL response.
        assert state.known_mechanism is not None
        assert state.known_mechanism.content == DEMO_ANSWER
        # Only the bounded unknown sentence is the acknowledged unknown.
        assert [u.verbatim for u in state.acknowledged_unknowns] == \
            [DEMO_UNKNOWN_SENTENCE]

    def test_unknown_sentence_first_then_reasoning(self):
        r = ("What I do not know yet is the safe operating temperature of "
             "the enclosure. The regulator steps the input down to 5V and "
             "feeds the logic rail through a polyfuse.")
        result = _detect_acknowledged_unknown(r, PHYSICAL_FEASIBILITY, 2)
        assert result is not None
        assert result.verbatim == ("What I do not know yet is the safe "
                                   "operating temperature of the enclosure.")

    def test_uncertainty_sentence_in_middle_excludes_neighbors(self):
        before1 = "The relay isolates the mains side from the logic side."
        before2 = ("The optocoupler transfers the switching signal, which "
                   "keeps the grounds separated.")
        unknown = "I am not sure whether the creepage distance is sufficient."
        after = ("The firmware debounces the input before it toggles the "
                 "output, so that transients do not cause chatter.")
        r = " ".join([before1, before2, unknown, after])
        result = _detect_acknowledged_unknown(r, PHYSICAL_FEASIBILITY, 4)
        assert result is not None
        assert result.verbatim == unknown
        for excluded in (before1, before2, after):
            assert excluded not in result.verbatim

    def test_contraction_im_not_sure_bounded_verbatim(self):
        unknown = "I'm not sure whether battery ageing changes the threshold."
        r = ("The comparator trips when the cell voltage drops below the "
             "reference, which causes the load switch to open. " + unknown)
        result = _detect_acknowledged_unknown(r, MECHANISM_COMPLETENESS, 2)
        assert result is not None
        assert result.verbatim == unknown

    def test_remaining_minimum_patterns_supported(self):
        pad = ("The driver stage switches the MOSFET, which causes the coil "
               "to energize. ")
        for unknown in (
            "It is still unknown how fast the capacitor discharges here.",
            "This is not yet known for the final enclosure material choice.",
            "I am not sure how the shielding behaves near the antenna.",
        ):
            result = _detect_acknowledged_unknown(
                pad + unknown, MECHANISM_COMPLETENESS, 1)
            assert result is not None, unknown
            assert result.verbatim == unknown

    def test_fragment_never_rewritten(self):
        # Verbatim except surrounding whitespace trimming: the fragment must
        # be an exact substring of the submitted text.
        result = _detect_acknowledged_unknown(
            "  " + DEMO_ANSWER + "  ", MECHANISM_COMPLETENESS, 1)
        assert result is not None
        assert result.verbatim in DEMO_ANSWER

    def test_extract_helper_single_sentence_returns_whole(self):
        r = "I do not know the drift characteristics of this thermistor yet"
        assert _extract_unknown_fragment(r, "i do not know") == r


# ─────────────────────────────────────────────
# Required tests 6-7 — no false positives
# ─────────────────────────────────────────────

class TestNoFalsePositives:
    def test_no_marker_no_record(self):
        r = ("The sensor measures pressure differential across the pipe "
             "because a leak causes a drop in flow resistance, which "
             "produces a measurable voltage change.")
        assert _detect_acknowledged_unknown(r, MECHANISM_COMPLETENESS, 1) is None
        state = _state()
        integrate_response(state, MECHANISM_COMPLETENESS, "Q?", r)
        assert state.acknowledged_unknowns == []

    def test_technical_word_unknown_is_not_an_acknowledgment(self):
        r = ("The unknown variable in the control loop is resolved by the "
             "calibration step, which measures the sensor offset at startup "
             "and stores it in memory.")
        assert _detect_acknowledged_unknown(r, MECHANISM_COMPLETENESS, 1) is None


# ─────────────────────────────────────────────
# Required test 8 — explicit unknown non-answer action unchanged
# ─────────────────────────────────────────────

class TestExplicitUnknownActionUnchanged:
    def _start_session(self):
        resp = app.test_client().post(
            "/start",
            data={"idea": "ESP32 microcontroller circuit with a voltage sensor",
                  "domain_confirm": DOMAIN_CONFIRM_VALUE},
            follow_redirects=False)
        assert resp.status_code == 302
        return resp.headers["Location"].rsplit("/", 1)[-1]

    def test_unknown_action_path_unchanged(self):
        sid = self._start_session()
        try:
            state = SESSION_STORE[sid]["state"]
            text = "I do not know this yet."
            before = (state.iteration, state.maturity_level,
                      [(g.gap_type, g.status) for g in state.gaps],
                      len(state.acknowledged_unknowns))
            app.test_client().post(f"/session/{sid}",
                                   data={"action": "unknown", "response": text})
            after = (state.iteration, state.maturity_level,
                     [(g.gap_type, g.status) for g in state.gaps],
                     len(state.acknowledged_unknowns))
            # No iteration, maturity, gap, or acknowledged-unknown change —
            # the explicit action stays on its own storage path.
            assert before == after
            actions = SESSION_STORE[sid].get("interaction_actions", [])
            assert actions and actions[-1]["action"] == "unknown"
            # The user's chosen unknown text is preserved verbatim.
            assert actions[-1]["text"] == text
            ledger = getattr(state, "assertions", [])
            assert ledger and ledger[-1].disposition == "unknown"
            assert ledger[-1].content == text
        finally:
            SESSION_STORE.pop(sid, None)


# ─────────────────────────────────────────────
# Required tests 9-11 — scoring / progression / verbatim independence
# ─────────────────────────────────────────────

class TestExtractionIndependence:
    def test_assess_response_identical_for_same_response(self):
        # Scoring never consults acknowledged unknowns; the assessed quality
        # of the demo answer is a pure function of the response text.
        q1 = assess_response(DEMO_ANSWER, "electronics_electrical")
        q2 = assess_response(DEMO_ANSWER, "electronics_electrical")
        assert q1 == q2

    def test_progression_identical_with_and_without_extraction(self, monkeypatch):
        # Same response, two identical states: one with detection active,
        # one with detection disabled. Everything except the parallel-track
        # acknowledged_unknowns list must be identical.
        r = DEMO_ANSWER

        state_with = _state()
        result_with = integrate_response(state_with, MECHANISM_COMPLETENESS, "Q?", r)

        import engine.progression_loop as pl
        monkeypatch.setattr(
            pl, "_detect_acknowledged_unknown", lambda *a, **k: None)
        state_without = _state()
        result_without = integrate_response(
            state_without, MECHANISM_COMPLETENESS, "Q?", r)

        assert result_with == result_without
        assert state_with.iteration == state_without.iteration
        assert state_with.maturity_level == state_without.maturity_level
        assert ([(g.gap_type, g.status, g.closed_at) for g in state_with.gaps]
                == [(g.gap_type, g.status, g.closed_at)
                    for g in state_without.gaps])
        assert (getattr(state_with.known_mechanism, "content", None)
                == getattr(state_without.known_mechanism, "content", None))
        # Only the parallel track differs.
        assert len(state_with.acknowledged_unknowns) == 1
        assert state_without.acknowledged_unknowns == []

    def test_web_answered_flow_full_answer_verbatim_fragment_stored(self):
        sid = None
        resp = app.test_client().post(
            "/start",
            data={"idea": "ESP32 microcontroller circuit with a voltage sensor",
                  "domain_confirm": DOMAIN_CONFIRM_VALUE},
            follow_redirects=False)
        assert resp.status_code == 302
        sid = resp.headers["Location"].rsplit("/", 1)[-1]
        try:
            state = SESSION_STORE[sid]["state"]
            # Deterministically target the answered->integrate_response path.
            state.gaps.append(Gap(gap_type=MECHANISM_COMPLETENESS,
                                  status=OPEN, opened_at=state.iteration))
            answered_post(app.test_client(), sid, {"action": "answered", "response": DEMO_ANSWER})
            # Transcript: full answer, byte-for-byte.
            transcript = SESSION_STORE[sid]["transcript"]
            assert transcript and transcript[-1]["response"] == DEMO_ANSWER
            # Interaction ledger: full answer, byte-for-byte.
            ledger = getattr(state, "assertions", [])
            assert ledger and ledger[-1].content == DEMO_ANSWER
            # Acknowledged unknown: ONLY the bounded unknown sentence.
            assert [u.verbatim for u in state.acknowledged_unknowns] == \
                [DEMO_UNKNOWN_SENTENCE]
            # Session panel renders only the bounded fragment, not the
            # substantive reasoning.
            body = app.test_client().get(f"/session/{sid}").get_data(as_text=True)
            assert DEMO_UNKNOWN_SENTENCE in body
            assert "What You Have Marked as Not Yet Known" in body
        finally:
            SESSION_STORE.pop(sid, None)

    def test_deliverable_registry_holds_only_bounded_fragment(self):
        from engine.deliverable_assembler import assemble_deliverable
        state = _state()
        integrate_response(state, MECHANISM_COMPLETENESS, "Q?", DEMO_ANSWER)
        pkg = assemble_deliverable(state)
        unknowns = pkg["section_5_assumptions"]["inventor_unknowns"]
        assert len(unknowns) == 1
        blob = str(unknowns[0])
        assert DEMO_UNKNOWN_SENTENCE in blob
        assert "The thermal sensor measures the heatsink temperature" not in blob


# ─────────────────────────────────────────────
# Required test 12 — duplicate behavior documented, not expanded
# ─────────────────────────────────────────────

class TestDuplicateBehaviorUnchanged:
    def test_repeat_submission_appends_again_as_before(self):
        # Current committed behavior has NO duplicate suppression in
        # integrate_response (append-only parallel track); this fix does not
        # silently add one. Documented, not expanded.
        state = _state()
        integrate_response(state, MECHANISM_COMPLETENESS, "Q?", DEMO_ANSWER)
        integrate_response(state, MECHANISM_COMPLETENESS, "Q?", DEMO_ANSWER)
        assert [u.verbatim for u in state.acknowledged_unknowns] == \
            [DEMO_UNKNOWN_SENTENCE, DEMO_UNKNOWN_SENTENCE]
