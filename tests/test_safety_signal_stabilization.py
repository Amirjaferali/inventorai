"""Safety Signal Stabilization — Workstream 2 fixture matrix (contract §6).

File: tests/test_safety_signal_stabilization.py
Governed by docs/governance/SAFETY_SIGNAL_STABILIZATION_INCREMENT_CONTRACT.md
(APPROVED AND CANONICAL — recorded by merged PR #170, canonicalized by PR #171;
blob 3db597c77d14aa8f39f7a624c7c32d4984e4f3a3).

Purpose: pin the stabilized inventor-stated safety-signal extraction —
positive / negative / metamorphic / deduplication / pairing fixtures — per the
canonical contract. All NEW Workstream 2 fixtures live here;
tests/test_safety_signal.py is preserved unchanged (contract §6 preamble).
The `_WARNING` text is intentionally re-declared here ONLY for the §6.3
side-by-side distinction test the contract itself requires in this file.

Prohibited behaviors verified: unchanged public output shape (SafetySignal
field set), unchanged provenance/validation constants, unchanged excerpt
behavior (raw statement; documented whitespace handling only), deterministic
matching and ordering, no schema `sources` field.
"""
import copy
import os
import sys
import uuid

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from engine.idea_state import IdeaState, Evidence, ASSERTED  # noqa: E402
from engine.safety_signal import (  # noqa: E402
    derive_inventor_stated_safety_signals,
    PROVENANCE_INVENTOR_STATED,
    VALIDATION_REQUIRES_INDEPENDENT,
)

# Pinned public field set (contract §3.5: schema frozen; no `sources` field).
_PUBLIC_FIELDS = {
    "signal_id", "source", "provenance", "safety_subject", "failure_condition",
    "possible_consequence", "domain_context", "validation_status",
    "display_label", "caution_text", "statement",
}


def _state(text=None, domain="electronics_electrical"):
    s = IdeaState(idea_id=str(uuid.uuid4()))
    s.domain = domain
    s.domain_signal = domain
    if text is not None:
        s.idea_summary = text
    return s


def _signals(text):
    return derive_inventor_stated_safety_signals(_state(text))


def _norm(text):
    return " ".join(text.split())


# ---------------------------------------------------------------------------
# §6.1 Positive fixtures — complete standalone statements (must signal alone)
# ---------------------------------------------------------------------------

# Owner-approved complete-context design: every standalone positive is a full
# realistic inventor statement containing an explicit failure / invalid-use
# condition. (The isolated phrase "dangerous appliance could remain powered"
# is NOT required to signal by itself; "could remain powered" is NOT a
# failure-state cue in Workstream 2 — owner decision §0.3.)
_POSITIVE_STANDALONE = (
    ("wrong-load-remain-powered",
     "If the sensing identifies the wrong load, the dangerous appliance could remain powered."),
    ("fails-to-disconnect-power",
     "If the breaker fails to disconnect power, the wiring could overheat and cause a fire."),
    ("wrong-branch-fail-to-isolate",
     "If it trips the wrong branch, the wrong appliance could be disconnected and it would fail to isolate the actual source of danger."),
    ("leaving-powered-could-allow-overheating",
     "If the relay contacts weld shut, leaving the appliance powered could allow overheating."),
    ("relay-sticks-fire-risk-could-continue",
     "If the relay sticks, damage or overheating could continue and the fire risk could continue until someone notices."),
    ("ws1-sensing-is-wrong",
     "If the sensing is wrong, the dangerous appliance could remain powered."),
)

# §6.1 permitted adjacent-sentence pairs (condition → consequence, same source).
_POSITIVE_PAIRS = (
    ("pair-wrong-load",
     "If the sensing identifies the wrong load. The dangerous appliance could remain powered."),
    ("pair-fragment-fire-risk",
     "If the relay sticks. The fire risk could continue until someone notices."),
)


def test_positive_standalone_statements_signal():
    for label, text in _POSITIVE_STANDALONE:
        sigs = _signals(text)
        assert len(sigs) >= 1, label
        sig = sigs[0]
        assert sig.provenance == PROVENANCE_INVENTOR_STATED, label
        assert sig.validation_status == VALIDATION_REQUIRES_INDEPENDENT, label
        assert sig.failure_condition and sig.safety_subject and sig.possible_consequence, label


def test_positive_adjacent_pairs_signal():
    for label, text in _POSITIVE_PAIRS:
        sigs = _signals(text)
        assert len(sigs) >= 1, label
        assert sigs[0].provenance == PROVENANCE_INVENTOR_STATED, label


def test_isolated_fragment_without_failure_condition_does_not_signal():
    # Contract §6.1: "fire risk could continue" is an incomplete fragment — no
    # failure/invalid-use condition — so it must NOT signal in isolation.
    assert _signals("The fire risk could continue.") == ()


# ---------------------------------------------------------------------------
# §6.2 Negative fixtures — each must produce ZERO signals
# ---------------------------------------------------------------------------

_NEGATIVES = (
    ("no-claim-attribution",
     "No claim is made that the appliance is dangerous."),
    ("specialist-deferred-determination",
     "A specialist will determine whether the condition is dangerous."),
    ("discussion-only-fire-risk",
     "The design discusses fire risk and lists mitigation options for the enclosure."),
    ("no-evidence-relay-failed",
     "There is no evidence that the relay failed."),
    ("warns-but-does-not-control-power",
     "The device warns about fire risk but does not control power."),
    ("negated-worst-case",
     "Even in a worst case there is no risk of overheating because the fuse cuts power."),
    ("hypothetical-unrelated",
     "If some hypothetical gadget elsewhere malfunctioned, this design would be unaffected."),
    ("adjacent-unrelated-hazard-mentions",
     "Overheating is a common topic in electronics forums. Fire safety is also popular."),
    # Owner-ordered benign-failover correction (PR #172 review finding):
    # benign OPERATIONAL continuation is not a safety consequence. "could
    # continue" must bind to an explicitly harmful continuation, not to an
    # electrical subject alone.
    ("benign-failover-mains",
     "If the battery fails to charge, operation could continue on mains power."),
    ("benign-failover-backup",
     "If the charger fails, service could continue using the backup supply."),
    ("benign-failover-redundant",
     "If one feed is unavailable, normal operation could continue on the redundant circuit."),
)

# Harmful-continuation counterpart positives (owner-ordered paired checks):
# the SAME "could continue" surface form must still be detected when the
# continuing thing is itself harmful (fire risk / overheating / damage).
_HARMFUL_CONTINUATION_POSITIVES = (
    ("relay-sticks-fire-risk", "If the relay sticks, the fire risk could continue."),
    ("isolation-fails-overheating", "If isolation fails, overheating could continue."),
    ("protection-fails-damage", "If protection fails, damage could continue."),
)


def test_harmful_continuation_remains_positive_and_benign_failover_negative():
    for label, text in _HARMFUL_CONTINUATION_POSITIVES:
        assert len(_signals(text)) == 1, label
    for label, text in _NEGATIVES[-3:]:
        assert _signals(text) == (), label


def test_negative_fixtures_produce_no_signal():
    for label, text in _NEGATIVES:
        assert _signals(text) == (), label


def test_cross_record_condition_consequence_never_pairs():
    # Contract §5.1: pairing never crosses assertion records or state fields.
    # The condition sentence and the consequence sentence live in two SEPARATE
    # recorded answers; they must never combine into one signal.
    state = _state()
    state.record_interaction("answered", "If the relay sticks.", iteration=1,
                             gap_context="PHYSICAL_FEASIBILITY")
    state.record_interaction("answered",
                             "The fire risk could continue until someone notices.",
                             iteration=2, gap_context="PHYSICAL_FEASIBILITY")
    assert derive_inventor_stated_safety_signals(state) == ()


# ---------------------------------------------------------------------------
# §6.3 The _WARNING distinction (owner decision §0.4)
# ---------------------------------------------------------------------------

def test_warning_reliability_positive_but_capability_description_negative():
    """Contract §6.3: `_WARNING` states a FAILURE CONDITION ("wrong results")
    with a stated consequence ("miss a real risk" / "too late") and remains
    POSITIVE. The capability/control description "the device warns about fire
    risk but does not control power" states NO failure condition and must be
    NEGATIVE. (The `_WARNING` text is re-declared here only for this
    contract-required side-by-side test.)"""
    warning = ("Wrong results could make the device miss a real risk or warn "
               "the user too late.")
    assert len(_signals(warning)) == 1
    assert _signals("The device warns about fire risk but does not control power.") == ()


# ---------------------------------------------------------------------------
# §6.4 Metamorphic fixtures — per-group invariants
# ---------------------------------------------------------------------------

_METAMORPHIC_GROUPS = {
    "fail-to-forms": (
        "The breaker fails to disconnect power, so the wiring could overheat and cause a fire.",
        "The breakers fail to disconnect power, so the wiring could overheat and cause a fire.",
        "The breaker failed to disconnect power, so the wiring could overheat and cause a fire.",
    ),
    "disconnect-isolate-remove-energized": (
        "If the relay fails to disconnect power, the heater could remain energized and cause a fire.",
        "If the relay fails to isolate the circuit, the heater could remain energized and cause a fire.",
        "If the relay fails to remove power, the heater could remain energized and cause a fire.",
        "If the relay fails to disconnect power, the heater could stay energized and cause a fire.",
    ),
    "active-passive": (
        "If the relay fails to disconnect power, the fire risk could continue.",
        "If power fails to be disconnected by the relay, the fire risk could continue.",
    ),
    "singular-plural": (
        "If the sensing identifies the wrong load, the dangerous appliance could remain powered.",
        "If the sensing identifies the wrong loads, the dangerous appliances could remain powered.",
    ),
    "reordered-cause-consequence": (
        "If the sensing identifies the wrong load, the dangerous appliance could remain powered.",
        "The dangerous appliance could remain powered if the sensing identifies the wrong load.",
    ),
    "adjacent-sentence-split": (
        "If the sensing identifies the wrong load, the dangerous appliance could remain powered.",
        "If the sensing identifies the wrong load. The dangerous appliance could remain powered.",
    ),
    "intent-preserving-paraphrase": (
        "If the sensing identifies the wrong load, the dangerous appliance could remain powered.",
        "Should the sensing pick the wrong load, the dangerous appliance could remain powered.",
    ),
}


def test_metamorphic_groups_stable_classification_and_invariants():
    for group, members in _METAMORPHIC_GROUPS.items():
        for text in members:
            sigs = _signals(text)
            # equal detection classification: every member is positive
            assert len(sigs) == 1, (group, text)  # and no duplicate-count inflation
            sig = sigs[0]
            assert sig.provenance == PROVENANCE_INVENTOR_STATED, group
            assert sig.validation_status == VALIDATION_REQUIRES_INDEPENDENT, group
            # excerpt faithful to its OWN original text (whitespace handling only)
            assert sig.statement == _norm(text), (group, text)
            # unchanged public output shape
            assert set(sig.__dict__.keys()) == _PUBLIC_FIELDS, group


def test_metamorphic_deterministic_ordering_and_repeatability():
    for group, members in _METAMORPHIC_GROUPS.items():
        for text in members:
            state = _state(text)
            assert (derive_inventor_stated_safety_signals(state)
                    == derive_inventor_stated_safety_signals(state)), (group, text)


# ---------------------------------------------------------------------------
# §6.5 Deduplication fixtures (owner decisions §0.2 / contract §4)
# ---------------------------------------------------------------------------

_DUP = "If the sensing identifies the wrong load, the dangerous appliance could remain powered."


def _multi_source_state(a, b, c):
    state = _state()
    state.record_interaction("answered", a, iteration=1,
                             gap_context="MECHANISM_COMPLETENESS")
    state.known_problem = Evidence(content=b, quality=ASSERTED, iteration=1)
    state.known_mechanism = Evidence(content=c, quality=ASSERTED, iteration=1)
    return state


def test_exact_duplicates_across_sources_collapse_to_one_signal():
    state = _multi_source_state(_DUP, _DUP, _DUP)
    sigs = derive_inventor_stated_safety_signals(state)
    assert len(sigs) == 1
    # deterministic source precedence: assertions precede known_problem/known_mechanism
    assert sigs[0].source.startswith("assertion:")
    assert sigs[0].statement == _norm(_DUP)


def test_materially_different_statements_are_not_deduplicated():
    variants = (
        _DUP.replace("appliance", "device"),          # one word differs
        _DUP.replace("If", "IF"),                     # case differs (no case folding)
        _DUP.replace("powered.", "powered!"),         # punctuation differs
    )
    for variant in variants:
        state = _multi_source_state(_DUP, variant, _DUP)
        sigs = derive_inventor_stated_safety_signals(state)
        assert len(sigs) == 2, variant


def test_whitespace_only_variants_are_deduplicated():
    spaced = _DUP.replace(", ", ",   ").replace(" could", "\n could")
    state = _multi_source_state(_DUP, spaced, _DUP)
    assert len(derive_inventor_stated_safety_signals(state)) == 1


def test_unicode_nfc_variants_are_deduplicated_with_excerpt_integrity():
    # Dedicated NFC fixture (owner decision §0.2): the same statement written
    # with a precomposed vs a combining-mark character is ONE statement.
    composed = _DUP.replace("powered.", "powered — sécurité note.")
    decomposed = _DUP.replace("powered.", "powered — sécurité note.")
    assert composed != decomposed  # byte-different, identical after NFC
    state = _multi_source_state(composed, decomposed, composed)
    sigs = derive_inventor_stated_safety_signals(state)
    assert len(sigs) == 1
    # emitted raw excerpt unchanged beyond documented whitespace handling
    assert sigs[0].statement == _norm(composed)


# ---------------------------------------------------------------------------
# Public shape, purity, determinism (contract §3.5 / §3.6)
# ---------------------------------------------------------------------------

def test_public_shape_and_constants_unchanged():
    sigs = _signals(_DUP)
    assert len(sigs) == 1
    sig = sigs[0]
    assert set(sig.__dict__.keys()) == _PUBLIC_FIELDS
    assert not hasattr(sig, "sources")
    assert sig.display_label == "Potential safety-critical assumption (inventor-stated)"
    assert sig.domain_context == "electronics_electrical"


def test_derivation_read_only_and_deterministic_ordering_across_sources():
    a = "If the breaker fails to disconnect power, the wiring could overheat and cause a fire."
    b = "If the relay sticks, damage or overheating could continue and the fire risk could continue."
    state = _state()
    state.record_interaction("answered", a, iteration=1, gap_context="MECHANISM_COMPLETENESS")
    state.record_interaction("answered", b, iteration=2, gap_context="PHYSICAL_FEASIBILITY")
    before = copy.deepcopy(state.__dict__)
    sigs = derive_inventor_stated_safety_signals(state)
    assert state.__dict__ == before                     # read-only
    assert [s.signal_id for s in sigs] == ["SIG-%03d" % i for i in range(1, len(sigs) + 1)]
    assert len(sigs) == 2
    assert sigs[0].statement == _norm(a) and sigs[1].statement == _norm(b)  # ledger order
