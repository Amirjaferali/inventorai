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
    ENGINE_CONTRACT_VERSION_T2G1, RECONSTRUCTION_VERSION,
    SUPPORTED_ENGINE_CONTRACT_VERSIONS)

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
def test_the_two_supported_versions_are_exactly_these():
    assert RECONSTRUCTION_VERSION == "p4-2-level1-recon-v1"
    assert ENGINE_CONTRACT_VERSION_T2G1 == "p4-2-level1-recon-v1-t2g1"
    assert SUPPORTED_ENGINE_CONTRACT_VERSIONS == (
        RECONSTRUCTION_VERSION, ENGINE_CONTRACT_VERSION_T2G1)


@pytest.mark.parametrize("version", [None, RECONSTRUCTION_VERSION, "", "anything",
                                     "p4-2-level1-recon-v1-t2g2"])
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
