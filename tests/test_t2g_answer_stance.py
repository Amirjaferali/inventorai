"""T2-G unit surface — bounded recognition of an EXPLICIT mechanism unknown.

`T2G-VERSIONED-IMPLEMENT-01`. Synthetic fixtures only; no real-user record.
These tests pin the module's OWN bounds — including the ones it fails to
recognise — so the limits stay disclosed rather than implied.
"""
import subprocess
import sys

import pytest

from engine import answer_stance as st
from engine.idea_state import MECHANISM_COMPLETENESS as MC
from engine.intent_serving import matches_committed_intent as MATCH
from engine.progression_loop import (
    _ACKNOWLEDGED_UNKNOWN_MARKERS, _detect_acknowledged_unknown)
from engine.session_reconstruction import (
    ENGINE_CONTRACT_VERSION_T2G1, ENGINE_CONTRACT_VERSION_T2G2,
    RECONSTRUCTION_VERSION, SUPPORTED_ENGINE_CONTRACT_VERSIONS)

def _code_only(source):
    """Source with comments and the module docstring removed: a guard must read
    the CODE, never the prose that deliberately names what it avoids."""
    body = source.split('"""', 2)[2] if source.count('"""') >= 2 else source
    return "\n".join(line for line in body.splitlines()
                      if not line.strip().startswith("#"))


Q1 = "mechanical:MECHANISM_COMPLETENESS:Q1"
Q2 = "mechanical:MECHANISM_COMPLETENESS:Q2"
Q4 = "mechanical:MECHANISM_COMPLETENESS:Q4"
MECH_IDS = (Q1, Q2, "mechanical:MECHANISM_COMPLETENESS:Q3", Q4)
EE_IDS = ("N-MC-1", "N-MC-2", "N-MC-3", "N-MC-4")

AFFIRM = ("The load path runs from the deck panel into the hinge line and the "
          "spring latch transfers force into the frame rail.")
UNKNOWN = ("I do not know the load path, and I have not worked out how the "
           "hinge line transfers force into the frame rail at all.")
AR_AFFIRM = ("مسار الحمل ينتقل من لوح السطح إلى خط المفصلة ثم ينقل المزلاج "
             "النابضي القوة إلى قضيب الإطار.")
AR_UNKNOWN = ("لا أعرف مسار الحمل ولم أحدد بعد كيف ينقل خط المفصلة القوة إلى "
              "قضيب الإطار على الإطلاق.")


class _State:
    """The minimum canonical carrier the predicates read."""

    def __init__(self, version=ENGINE_CONTRACT_VERSION_T2G1, domain="mechanical"):
        if version is not None:
            self.engine_contract_version = version
        self.domain = domain
        self.iteration = 0


def _detect(state):
    return lambda text: _detect_acknowledged_unknown(text, MC, 0)


def _veto(state, response, ids=MECH_IDS):
    return st.explicit_unknown_without_mechanism(
        state, MC, response, detect_unknown=_detect(state),
        variant_ids=ids, matches_intent=MATCH)


# ==========================================================================
# 1. Version gating — the rule can never switch itself on
# ==========================================================================
def test_the_supported_versions_are_exactly_these():
    # Safe Question Reduction Slice 1 adds the FOURTH, routing-aware version.
    from engine.session_reconstruction import ENGINE_CONTRACT_VERSION_NR1
    assert RECONSTRUCTION_VERSION == "p4-2-level1-recon-v1"
    assert ENGINE_CONTRACT_VERSION_T2G1 == "p4-2-level1-recon-v1-t2g1"
    assert ENGINE_CONTRACT_VERSION_T2G2 == "p4-2-level1-recon-v1-t2g2"
    assert ENGINE_CONTRACT_VERSION_NR1 == "p4-2-level1-recon-v1-t2g2-nr1"
    assert SUPPORTED_ENGINE_CONTRACT_VERSIONS == (
        RECONSTRUCTION_VERSION, ENGINE_CONTRACT_VERSION_T2G1,
        ENGINE_CONTRACT_VERSION_T2G2, ENGINE_CONTRACT_VERSION_NR1)


@pytest.mark.parametrize("version", [None, RECONSTRUCTION_VERSION, "", "anything",
                                     "p4-2-level1-recon-v1-t2g9",
                                     "p4-2-level1-recon-v2"])
def test_an_unversioned_or_legacy_state_never_enables_the_rule(version):
    state = _State(version=version)
    assert st.is_t2g_active(state, gap_type=MC) is False
    assert _veto(state, UNKNOWN) is False
    # coverage is exactly today's committed-marker result
    assert st.covers_variant(state, UNKNOWN, Q2, MATCH, gap_type=MC) is True


def test_the_rule_is_confined_to_the_named_gap_and_domains():
    assert st.is_t2g_active(_State(), gap_type=MC) is True
    assert st.is_t2g_active(_State(), gap_type="PHYSICAL_FEASIBILITY") is False
    assert st.is_t2g_active(_State(domain="software"), gap_type=MC) is False
    assert st.is_t2g_active(_State(domain=None), gap_type=MC) is False
    assert st.T2G_SCOPED_GAPS == frozenset({MC})
    assert st.T2G_SCOPED_DOMAINS == frozenset({"electronics_electrical", "mechanical"})


# ==========================================================================
# 2. What the veto does and does not fire on
# ==========================================================================
@pytest.mark.parametrize("text", [UNKNOWN, AR_UNKNOWN])
def test_a_recognised_explicit_unknown_with_no_explanation_is_vetoed(text):
    assert _veto(_State(), text) is True


@pytest.mark.parametrize("text", [AFFIRM, AR_AFFIRM])
def test_an_affirmative_explanation_is_never_vetoed(text):
    assert _veto(_State(), text) is False


def test_physical_negation_is_not_ignorance():
    """A useful NEGATIVE mechanism description must survive untouched."""
    negative = ("The spring latch does not carry the load; the load path runs "
                "around it, from the deck straight into the hinge line and "
                "then the frame rail.")
    assert _veto(_State(), negative) is False
    assert st.covers_variant(_State(), negative, Q2, MATCH, gap_type=MC) is True


def test_a_mixed_answer_keeps_its_supported_clause():
    mixed = ("I do not know the exact bolt size yet. The load path runs from "
             "the deck into the hinge line and then into the frame rail.")
    assert _veto(_State(), mixed) is False
    assert st.covers_variant(_State(), mixed, Q2, MATCH, gap_type=MC) is True
    ar_mixed = ("لا أعرف مقاس البرغي بعد. مسار الحمل ينتقل من لوح السطح إلى "
                "خط المفصلة ثم إلى قضيب الإطار.")
    assert _veto(_State(), ar_mixed) is False


@pytest.mark.parametrize("tail", [
    "Spring latch.",                                   # a bare component name
    "Hinge line",                                      # a bare committed noun
    "My brother runs a workshop in the next town.",    # unrelated
    "I am unsure.",                                    # uncertainty only
])
def test_a_bare_noun_or_unrelated_sentence_never_defeats_the_veto(tail):
    assert _veto(_State(), UNKNOWN + " " + tail) is True


def test_the_veto_reads_only_the_named_gaps_knowledge_seeking_variants():
    """A carrier for the UNCERTAINTY variant alone does not defeat the veto."""
    text = UNKNOWN + " That detail would be missing if I said no more."
    assert MATCH(text, Q4) is True                     # it does answer Q4
    assert _veto(_State(), text) is True               # still no mechanism


# ==========================================================================
# 3. Purpose-aware coverage
# ==========================================================================
def test_a_knowledge_seeking_variant_needs_a_qualifying_carrier():
    assert st.covers_variant(_State(), AFFIRM, Q2, MATCH, gap_type=MC) is True
    assert st.covers_variant(_State(), UNKNOWN, Q2, MATCH, gap_type=MC) is False
    assert st.covers_variant(_State(), AR_AFFIRM, Q2, MATCH, gap_type=MC) is True
    assert st.covers_variant(_State(), AR_UNKNOWN, Q2, MATCH, gap_type=MC) is False


@pytest.mark.parametrize("qid,text", [
    ("N-MC-4", "There is a part I am unsure about: I do not know how the board "
               "decides the threshold, I am imagining loosely."),
    ("N-MC-4", "هناك جزء لست متأكدا منه، فأنا أتخيله بشكل فضفاض."),
    (Q4, "I do not know the latch tolerance; that detail would be missing."),
])
def test_the_uncertainty_variants_keep_their_coverage(qid, text):
    """Naming a missing detail ANSWERS these two questions."""
    assert qid in st.UNCERTAINTY_QUESTION_IDS
    domain = "electronics_electrical" if qid.startswith("N-") else "mechanical"
    state = _State(domain=domain)
    assert st.covers_variant(state, text, qid, MATCH, gap_type=MC) is True


def test_the_uncertainty_exemption_is_not_mechanism_knowledge():
    text = "I do not know the latch tolerance; that detail would be missing."
    assert st.covers_variant(_State(), text, Q4, MATCH, gap_type=MC) is True
    assert _veto(_State(), text) is True               # coverage != knowledge


def test_coverage_never_invents_a_match():
    assert st.covers_variant(_State(), "totally unrelated prose", Q2, MATCH,
                             gap_type=MC) is False


# ==========================================================================
# 4. Declared bounds — stated, not hidden
# ==========================================================================
def test_only_registered_ignorance_phrasings_are_recognised():
    for marker in _ACKNOWLEDGED_UNKNOWN_MARKERS:
        assert st.declares_ignorance("well, " + marker + " about that part")
    # an UNREGISTERED phrasing is not recognised — a disclosed limitation
    assert st.declares_ignorance("no clue about the load path") is False
    assert _veto(_State(), "No clue about the load path or the hinge line, "
                           "honestly, none whatsoever at this point.") is False


def test_the_bare_technical_word_unknown_is_not_an_ignorance_marker():
    assert st.declares_ignorance("the unknown load path") is False


def test_the_existing_detectors_minimum_length_bound_still_applies():
    """Below the existing detector's floor nothing is recognised — the bound is
    inherited, not re-invented."""
    short = "I do not know."
    assert _detect_acknowledged_unknown(short, MC, 0) is None
    assert _veto(_State(), short) is False


def test_arabic_ignorance_surfaces_are_recognised_through_the_existing_detector():
    assert st.declares_ignorance("لا أعرف مسار الحمل") is True
    assert st.declares_ignorance("مسار الحمل واضح تماما") is False


# ==========================================================================
# 5. Bounded sentence handling
# ==========================================================================
def test_english_and_arabic_terminators_both_split():
    assert len(st.sentences("a. b! c? d; e")) == 5
    assert len(st.sentences("أ؟ ب؛ ج")) == 3
    # the Arabic comma is deliberately NOT a boundary
    assert len(st.sentences("لا أعرف مسار الحمل، ولم أحدد شيئا")) == 1


def test_sentence_handling_is_local_to_this_module():
    """The existing splitters keep their own meanings and consumers."""
    import inspect
    from engine import progression_loop as pl
    assert pl._SENTENCE_SPLIT_RE.pattern == r"(?<=[.!?])\s+"
    assert pl._GATE_SENTENCE_BOUNDARY_RE.pattern == r"[.!?]+|[\r\n]+"
    src = _code_only(inspect.getsource(st))
    assert "_SENTENCE_SPLIT_RE" not in src
    assert "_GATE_SENTENCE_BOUNDARY_RE" not in src


# ==========================================================================
# 6. Import hygiene — no cycle in either order, no global patching
# ==========================================================================
@pytest.mark.parametrize("first,second", [
    ("engine.progression_loop", "engine.intent_serving"),
    ("engine.intent_serving", "engine.progression_loop"),
    ("engine.answer_stance", "engine.progression_loop"),
    ("engine.intent_serving", "engine.answer_stance"),
])
def test_both_module_import_orders_are_clean(first, second):
    code = ("import importlib, sys;"
            "importlib.import_module(%r);"
            "importlib.import_module(%r);"
            "print('ok')" % (first, second))
    out = subprocess.run([sys.executable, "-c", code], capture_output=True,
                         text=True)
    assert out.returncode == 0, out.stderr[-800:]
    assert "ok" in out.stdout


def test_answer_stance_imports_no_consumer_at_module_scope():
    import inspect
    body = _code_only(inspect.getsource(st))
    head = body.split("import re", 1)[1].split("def ", 1)[0]
    assert "progression_loop" not in head
    assert "intent_serving" not in head


def test_matches_committed_intent_is_the_unchanged_predicate():
    from engine import intent_serving as isv
    for text, qid in ((AFFIRM, Q2), (UNKNOWN, Q2), ("nothing", Q2)):
        assert isv.matches_committed_intent(text, qid) == isv._matches_intent(text, qid)


# ==========================================================================
# 7. F-1 / F-2 carrier repair — PR642-T2G-CARRIER-REPAIR-01
# ==========================================================================
AR_UNKNOWN = ("لا أعرف مسار الحمل ولم أحدد بعد كيف ينقل خط المفصلة القوة إلى "
              "قضيب الإطار على الإطلاق.")
EE_UNKNOWN = ("I do not know what the main parts are yet, and I cannot say what "
              "each part does because I have not chosen any of the hardware.")


def _ee_state():
    return _State(domain="electronics_electrical")


# --------------------------------------------------------------------------
# F-2 — every marker occurrence is discounted, repetitions included
# --------------------------------------------------------------------------
@pytest.mark.parametrize("tail", [
    "Force path force path force path.",
    "Hinge line hinge line hinge line.",
    "Force path hinge line force path hinge line.",
    "Load path force path load path force path.",     # different markers
    "load path, load path, load path, load path",     # separated by commas
    "LOAD PATH LOAD PATH LOAD PATH",                  # case-insensitive EN
])
def test_repeated_markers_never_become_explanatory_context(tail):
    """F-2: a marker echoed three times is still only the marker."""
    assert _veto(_State(), UNKNOWN + " " + tail) is True


@pytest.mark.parametrize("tail", [
    "مسار القوة مسار القوة مسار القوة.",
    "خط المفصلة خط المفصلة خط المفصلة.",
    "مسار الحمل خط المفصلة مسار الحمل خط المفصلة.",
])
def test_repeated_arabic_markers_never_become_context(tail):
    assert _veto(_State(), AR_UNKNOWN + " " + tail) is True


def test_repeated_electronics_markers_never_become_context():
    assert st.covers_variant(_ee_state(), "Main parts main parts main parts.",
                             "N-MC-2", MATCH, gap_type=MC) is False
    assert _veto(_ee_state(), EE_UNKNOWN + " Main parts main parts main parts.",
                 ids=EE_IDS) is True


def test_overlapping_marker_occurrences_are_counted_once():
    """`would notice` and `notice the problem` overlap on `notice`; the union
    is discounted once, and the leftover words are what decide."""
    state = _ee_state()
    overlapping = "Would notice the problem."
    assert MATCH(overlapping, "N-MC-1") is True
    assert st._marker_spans(overlapping, "N-MC-1") == ((0, len(overlapping) - 1),)
    assert st.covers_variant(state, overlapping, "N-MC-1", MATCH, gap_type=MC) is False


@pytest.mark.parametrize("tail,expected_veto", [
    # POSITIVE CONTROLS: markers plus a genuine explanation still carry
    ("Force path force path: the deck panel presses down into the hinge line "
     "and the frame rail carries it into the chassis.", False),
    ("The load path runs from the deck into the hinge line and then the rail.", False),
    # and the marker-only forms do not
    ("Force path.", True),
    ("Load path load path.", True),
])
def test_genuine_explanation_still_carries_after_repeated_markers(tail, expected_veto):
    assert _veto(_State(), UNKNOWN + " " + tail) is expected_veto


def test_the_arabic_positive_control_still_carries():
    real = ("مسار القوة ينتقل من لوح السطح إلى خط المفصلة ثم إلى قضيب الإطار "
            "ويحمله الهيكل.")
    assert _veto(_State(), AR_UNKNOWN + " " + real) is False
    assert st.covers_variant(_State(), real, Q2, MATCH, gap_type=MC) is True


def test_surplus_counts_only_words_outside_every_marker_span():
    spans = st._marker_spans("the load path runs into the hinge line", Q2)
    assert len(spans) == 2                       # two distinct occurrences
    # four surplus words ("the", "runs", "into", "the") reach the floor
    assert st._carries_context("the load path runs into the hinge line", Q2,
                               MATCH) is True
    assert st._carries_context("the load path the hinge line", Q2, MATCH) is False


def test_an_unreadable_marker_table_is_not_a_carrier():
    """Fail toward leaving the question owed an answer, never toward progress."""
    assert st._marker_spans("anything at all", "NOT-A-COMMITTED-ID") == ()
    assert st._carries_context("anything at all", "NOT-A-COMMITTED-ID",
                               lambda *a: True) is False


# --------------------------------------------------------------------------
# F-1 — bounded work, not a timing hope
# --------------------------------------------------------------------------
def test_the_carrier_check_calls_the_matcher_a_bounded_number_of_times():
    """F-1, stable work bound: sizing a sentence must not re-invoke the matcher
    per token window. The matcher is consulted ONCE per sentence, whatever the
    sentence length — this fails deterministically if window enumeration
    returns, with no reliance on wall-clock time."""
    calls = []

    def counting(text, question_id):
        calls.append(len(text))
        return MATCH(text, question_id)

    for words in (10, 100, 1000):
        calls.clear()
        sentence = ("alpha " * words) + "load path"
        assert st.qualifying_carrier(sentence, Q2, counting) is True
        assert len(calls) == 1, (words, len(calls))
        assert calls[0] == len(sentence)          # the whole sentence, once


def test_the_marker_scan_is_linear_in_sentence_length():
    """Doubling the sentence at most roughly doubles the span scan; the old
    window enumeration grew by about 8x per doubling."""
    import time
    def elapsed(words):
        sentence = ("alpha " * words) + "load path"
        best = None
        for _ in range(3):
            start = time.perf_counter()
            st._marker_spans(sentence, Q2)
            span = time.perf_counter() - start
            best = span if best is None else min(best, span)
        return best
    small, large = elapsed(500), elapsed(4000)     # 8x the length
    assert large < max(small * 40, 0.05)           # generous, still excludes n^3


@pytest.mark.parametrize("body", [
    ("alpha " * 3330) + "load path",               # marker at the very END
    "load path " + ("alpha " * 3330),              # marker at the very start
    "load path " * 1999,                           # maximum marker density
])
def test_an_answer_at_the_accepted_character_limit_is_handled_quickly(body):
    """The accepted 20,000-character limit is NOT reduced to hide cost; the
    helper simply handles it. Loose bound: this asserts the collapse of a
    minutes-long path, not a performance target."""
    import time
    from web.app import MAX_FREE_TEXT_CHARS
    assert len(body) <= MAX_FREE_TEXT_CHARS
    start = time.perf_counter()
    st.qualifying_carrier(body, Q2, MATCH)
    assert time.perf_counter() - start < 5.0


def test_the_repair_did_not_widen_or_narrow_the_match_itself():
    """`_matches_intent` decides WHETHER the sentence matches; the repair only
    sizes what else it says."""
    import inspect
    source = _code_only(inspect.getsource(st._carries_context))
    assert "matches_intent" not in source          # sizing consults it no more
    for text in (AFFIRM, UNKNOWN, "hinge line", "nothing here",
                 "I do not know. The load path runs into the hinge line here."):
        expected = any(
            (not st.declares_ignorance(part)) and MATCH(part, Q2)
            and st._carries_context(part, Q2, MATCH)
            for part in st.sentences(text))
        assert st.qualifying_carrier(text, Q2, MATCH) is expected


def test_the_canonical_marker_table_is_read_not_duplicated():
    import inspect
    from engine import intent_serving as isv
    assert st._committed_markers(Q2) is isv._INTENT_MARKERS[Q2]
    body = _code_only(inspect.getsource(st))
    for marker in ("force path", "hinge line", "main parts", "مسار القوة"):
        assert marker not in body                  # no second vocabulary


# ==========================================================================
# 8. F-3 Unicode span coordinates — PR642-T2G-UNICODE-SPAN-REPAIR-02
#
# English surfaces are matched in `sentence.lower()`; word spans are measured
# on the ORIGINAL sentence. U+0130 lowercases to TWO code points, so without a
# coordinate map every English match after one sits at the wrong index and the
# marker-only bypass returns through a Unicode side door.
# ==========================================================================
DOTTED_I = "İ"                       # LATIN CAPITAL LETTER I WITH DOT ABOVE


def test_the_expansion_this_repair_exists_for_is_real():
    assert len(DOTTED_I.lower()) == 2
    assert len((DOTTED_I + "x").lower()) == 3


@pytest.mark.parametrize("sentence", [
    DOTTED_I + " Force path force path force path.",
    (DOTTED_I * 3) + " Force path force path force path.",
    "Force path " + DOTTED_I + " force path " + DOTTED_I + " force path.",
    "مسار القوة " + DOTTED_I + " force path force path.",
    DOTTED_I + "stanbul: load path load path.",
])
def test_marker_only_stays_marker_only_across_the_expansion(sentence):
    """F-3: each of these is still nothing but repeated markers."""
    assert MATCH(sentence, Q2) is True
    assert st.qualifying_carrier(sentence, Q2, MATCH) is False
    assert st.covers_variant(_State(), sentence, Q2, MATCH, gap_type=MC) is False
    assert _veto(_State(), UNKNOWN + " " + sentence) is True


@pytest.mark.parametrize("sentence", [
    "Force path force path force path.",                       # no expansion
    DOTTED_I + " Force path force path.",                      # leading
    "Force path " + DOTTED_I + " force path.",                 # between
    (DOTTED_I * 5) + "load path" + (DOTTED_I * 5),             # both sides
    "مسار القوة " + DOTTED_I + " force path.",                 # mixed AR/EN
    "The load path runs into the hinge line and the rail.",    # ordinary
])
def test_every_span_is_an_original_text_coordinate(sentence):
    """A returned span must slice a real marker OUT OF THE ORIGINAL TEXT."""
    spans = st._marker_spans(sentence, Q2)
    assert spans, sentence
    for start, end in spans:
        assert 0 <= start < end <= len(sentence)
        assert MATCH(sentence[start:end], Q2), (sentence, (start, end))


def test_the_repair_changes_no_match_decision():
    """Spans exist exactly when the unchanged matcher matches — across every
    committed id, in both scripts, with and without the expansion."""
    from engine.intent_serving import _INTENT_MARKERS
    checked = 0
    for question_id, (english, arabic) in _INTENT_MARKERS.items():
        candidates = ["no marker here at all", DOTTED_I, DOTTED_I * 4]
        for surface in list(english)[:3]:
            candidates += [surface, surface.upper(), DOTTED_I + " " + surface,
                           (DOTTED_I * 2) + surface, "x " + surface + " y"]
        for surface in list(arabic)[:2]:
            candidates += [surface, DOTTED_I + " " + surface]
        for text in candidates:
            assert bool(st._marker_spans(text, question_id)) is MATCH(text, question_id)
            checked += 1
    assert checked > 300


def test_arabic_matching_is_unaffected_by_the_mapping():
    arabic_only = "مسار القوة مسار القوة مسار القوة."
    assert st.qualifying_carrier(arabic_only, Q2, MATCH) is False
    spans = st._marker_spans(arabic_only, Q2)
    assert len(spans) == 3
    for start, end in spans:
        assert arabic_only[start:end] == "مسار القوة"


def test_overlap_merging_still_holds_under_the_expansion():
    state = _ee_state()
    overlapping = DOTTED_I + " Would notice the problem."
    assert MATCH(overlapping, "N-MC-1") is True
    spans = st._marker_spans(overlapping, "N-MC-1")
    assert len(spans) == 1                              # merged, counted once
    start, end = spans[0]
    assert overlapping[start:end] == "Would notice the problem"
    assert st.covers_variant(state, overlapping, "N-MC-1", MATCH,
                             gap_type=MC) is False


def test_a_genuine_explanation_still_carries_under_the_expansion():
    """The positive control must not be suppressed by the repair."""
    real = (DOTTED_I + " Force path force path: the deck panel presses down "
            "into the hinge line and the frame rail carries it.")
    assert st.qualifying_carrier(real, Q2, MATCH) is True
    assert _veto(_State(), UNKNOWN + " " + real) is False


def test_the_surplus_threshold_is_exactly_three_fails_four_passes():
    """Same-touch precision, wording only: the rule is unchanged."""
    assert st._MIN_CARRIER_CONTEXT_WORDS == 4
    assert st._carries_context("the load path aa bb", Q2, MATCH) is False   # 3
    assert st._carries_context("the load path aa bb cc", Q2, MATCH) is True  # 4
    # and the same either side of the expansion
    assert st._carries_context(DOTTED_I + " load path aa bb", Q2, MATCH) is False
    assert st._carries_context(DOTTED_I + " load path aa bb cc", Q2, MATCH) is True


def test_the_input_is_never_rewritten_by_the_mapping():
    """U+0130 is not deleted, rejected, normalised or re-cased; the answer text
    itself is untouched and the lowered haystack stays `sentence.lower()`."""
    import inspect
    sentence = DOTTED_I + " load path"
    before = sentence
    st._marker_spans(sentence, Q2)
    assert sentence == before
    source = _code_only(inspect.getsource(st))
    for forbidden in ("casefold", "unicodedata", "normalize", "encode(",
                      "IGNORECASE", "ascii"):
        assert forbidden not in source, forbidden
    assert "sentence.lower()" in source


def test_the_index_map_is_exact_or_refuses():
    sentence = DOTTED_I + "abc"
    lowered = sentence.lower()
    origin = st._lowered_to_original(sentence, lowered)
    assert origin == [0, 0, 1, 2, 3]                 # the expansion is attributed
    assert st._lowered_to_original(sentence, "too short") is None


def test_the_expansion_path_does_not_undo_the_work_bound():
    """One small time-limited check that coordinate mapping stays cheap at the
    accepted input limit. Loose bound, not a performance target."""
    import time
    from web.app import MAX_FREE_TEXT_CHARS
    for body in (((DOTTED_I + "lpha ") * 3330 + "load path")[:MAX_FREE_TEXT_CHARS - 1],
                 ((DOTTED_I + " load path ") * 999)[:MAX_FREE_TEXT_CHARS - 1]):
        start = time.perf_counter()
        st.qualifying_carrier(body, Q2, MATCH)
        assert time.perf_counter() - start < 5.0
