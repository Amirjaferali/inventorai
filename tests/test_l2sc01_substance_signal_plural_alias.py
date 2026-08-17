"""L2SC-01 — Substance-Signal Plural-Alias Domain-Completeness (implementation).

Authoritative contract:
`docs/governance/L2SC01_SUBSTANCE_SIGNAL_PLURAL_ALIAS_INCREMENT_CONTRACT.md`
(material correction of rejected candidate `219f7c1`, defect MD-1).

Implements Option B: an optional, pack-scoped `substance_signal_plural_aliases`
registry field (mirroring the existing pack-level `aliases` precedent), read via
`engine.domain_rules.get_substance_signal_plural_aliases(domain)` and consumed by
the Layer-2 causal-connective gate (`engine/progression_loop.py`). The historical
shared-engine hardcoded map (`_SUBSTANCE_PLURAL_ALIASES`) no longer exists — there
is exactly ONE live source of plural-alias data: the domain pack itself.

Authorized Mechanical aliases (contract §4, only 3 of 15 signals — the rejected
candidate's 9-pair set was rejected by independent review for insufficient
verb-form/idiom screening): `piston`/`pistons`, `valve`/`valves`,
`actuator`/`actuators`. The remaining 12 Mechanical signals are explicitly NOT
aliased and must never gain Layer-2 substance recognition via their plural
surface form alone (§12.D — rejected-alias guards).

MD-A CORRECTION (this revision, independent-review rejection of candidate
`714d538`, preserved immutable at `refs/rejected/l2sc01-runtime-impl-714d538`):
runtime/data are BYTE-IDENTICAL to `714d538` — the reviewer found the runtime
implementation itself materially correct. The defect was in section D below:
in 10 of the 12 original adversarial sentences, the rejected alias word sat on
the WRONG side of its "because" connective (before it, in the effect clause,
never inspected by the cause-first directional gate) — so the guard passed
regardless of whether the alias was authorized, unauthorized, or absent
entirely. Only 2 of 12 (`torque`, `mechanism`) were genuinely load-bearing.
Section D below replaces all 10 vacuous sentences with direction-correct
constructions (the rejected word placed in the supporting clause the gate
actually inspects) and adds an explicit three-way differential proof — clean
map (ASSERTED) / poisoned map (REASONED) / neutral-control map (ASSERTED) —
for every one of the 12 excluded signals, so the guard's outcome is
demonstrated to depend on the alias under test, not assumed from sentence
construction alone.
"""

import json
import os
import sys
import warnings
from unittest import mock

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from engine.domain_registry import load_registry, RegistryLoadError
from engine.domain_rules import get_substance_signal_plural_aliases, get_substance_signals
from engine.idea_state import IdeaState, Gap, MECHANISM_COMPLETENESS, OPEN
from engine.progression_loop import assess_response, integrate_response, REASONED, ASSERTED

MECH = "mechanical"
ELEC = "electronics_electrical"


def _assess(resp, domain):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return assess_response(resp, domain)


# ============================================================= A. electronics
def test_green_electronics_plural_alias_registry_derived_byte_identical():
    """The 8 historical electronics pairs now live in the pack, not the
    engine, and still produce REASONED for both singular and plural via the
    real assess_response path (byte/behavior-identical to the pre-migration
    hardcoded-map behavior, re-pinned end-to-end)."""
    pairs = [
        ("sensor", "sensors"), ("relay", "relays"), ("resistor", "resistors"),
        ("battery", "batteries"), ("capacitor", "capacitors"),
        ("motor", "motors"), ("led", "leds"), ("ic", "ics"),
    ]
    for singular, plural in pairs:
        s = _assess(f"The circuit activates because the {singular} reports a "
                     f"stable reading every single cycle.", ELEC)
        p = _assess(f"The circuit activates because the {plural} report a "
                     f"stable reading every single cycle.", ELEC)
        assert s == REASONED, singular
        assert p == REASONED, plural


def test_green_electronics_plural_alias_map_lives_in_registry_not_engine():
    aliases = get_substance_signal_plural_aliases(ELEC)
    assert aliases == {
        "sensors": "sensor", "relays": "relay", "resistors": "resistor",
        "batteries": "battery", "capacitors": "capacitor", "motors": "motor",
        "leds": "led", "ics": "ic",
    }


# ============================================== B. Mechanical approved parity
@pytest.mark.parametrize("singular,plural,sentence_template", [
    ("piston", "pistons",
     "The engine runs smoothly because the {} compress the air efficiently "
     "and reliably."),
    ("valve", "valves",
     "The system regulates flow because the {} close tightly to stop the "
     "liquid from leaking."),
    ("actuator", "actuators",
     "The {} extend fully therefore the arm reaches the target position "
     "reliably every cycle."),
])
def test_green_mechanical_approved_alias_parity(singular, plural, sentence_template):
    s = _assess(sentence_template.format(singular), MECH)
    p = _assess(sentence_template.format(plural), MECH)
    assert s == REASONED, singular
    assert p == REASONED, plural


def test_green_mechanical_approved_alias_set_is_exactly_three():
    aliases = get_substance_signal_plural_aliases(MECH)
    assert aliases == {
        "pistons": "piston", "valves": "valve", "actuators": "actuator",
    }


# === C. authorized-alias sentence-boundary / directional-discipline guards ===
# NAMED HONESTLY (independent-review §12.C observation): these are NOT
# singular-vs-plural-specific false-positive guards — the sentence-boundary
# and directional-segment logic they exercise is the PRE-EXISTING Layer-2
# gate mechanism (`_gate_sentence_spans` / `_gate_directional_segment`),
# unrelated to plural aliasing and identical whether the word under test is
# singular or plural. They confirm only that an authorized alias does not
# bypass that pre-existing discipline — re-exercised here because L2SC-01
# added new alias vocabulary that could in principle have been wired past it.
@pytest.mark.parametrize("label,sentence", [
    ("pistons wrong sentence",
     "The garage mentioned the pistons yesterday. The mechanic left early "
     "because traffic was heavy this evening."),
    ("valves wrong sentence",
     "The supplier discussed the valves earlier. The customer complained "
     "because the delivery arrived very late today."),
    ("actuators wrong side",
     "The actuators appeared in the report. The meeting ended early "
     "therefore everyone left the building quickly today."),
])
def test_green_mechanical_authorized_alias_respects_sentence_boundary_and_direction(label, sentence):
    """The mere PRESENCE of an approved alias word anywhere in the response
    is not sufficient — it must appear in the qualifying connective's own
    sentence, on the directional side that connective requires. This is a
    sentence-boundary/directional-discipline guard (pre-existing mechanism,
    not a plural-specific false-positive guard — see section comment above).
    Each case here places the alias word in a different sentence (or the
    wrong side of a result-first connective) than the qualifying connective,
    whose own sentence carries no substance."""
    assert _assess(sentence, MECH) == ASSERTED, label


# ============================================ D. rejected-alias false-positive guards
# MD-A CORRECTION (module docstring; independent-review rejection of
# candidate `714d538`). Every sentence below places the rejected alias word
# in the SAME clause the Layer-2 gate's directional-segment logic actually
# inspects for its connective (`_gate_directional_segment`: for cause-first
# "because", that is the clause AFTER the connective) — direction-correct,
# analogous to the reviewer's own demonstrated example ("The joint stays
# tight because the gasket seals the mating surface completely."). Each
# sentence is additionally verified to contain no `_CAUSAL_STRUCTURE_
# PATTERNS` substring and no OTHER canonical substance word in the
# supporting clause, so the only path that could grant REASONED is the
# Layer-2 alias-gated path exercised by the alias word itself — never an
# independent, unrelated confound. `torque` and `mechanism` were already
# direction-correct in the rejected candidate and are carried forward
# unchanged; the other 10 are corrected constructions.
#
# Each tuple is (label, sentence, alias_word, canonical_target) — the last
# two feed the load-bearing differential tests below, which POISON a copy
# of the real Mechanical alias map with exactly {alias_word: canonical_
# target} and assert the classification flips from ASSERTED to REASONED —
# proving each guard's outcome actually depends on alias-map content, not
# merely on sentence structure (§4/§5 of the independent-review correction).
_REJECTED_ALIAS_CASES = [
    ("seal/verb",
     "The joint stays tight because the gasket seals the mating surface "
     "completely.",
     "seals", "seal"),
    ("spring/verb",
     "The door stays shut because the latch springs against the frame "
     "every single time.",
     "springs", "spring"),
    ("bearing/idiom",
     "The team struggles to plan because the new hire loses their "
     "bearings during every stressful meeting.",
     "bearings", "bearing"),
    ("gear/idiom",
     "The festival attracts huge crowds because the whole town gears up "
     "for the celebration every single year.",
     "gears", "gear"),
    ("lever/idiom",
     "The proposal succeeds because the committee invokes the levers of "
     "influence very effectively this time.",
     "levers", "lever"),
    ("hydraulic/field-noun",
     "The graduate finds better job offers because the university "
     "teaches hydraulics as a required course every semester.",
     "hydraulics", "hydraulic"),
    ("pneumatic/field-noun",
     "The graduate finds better job offers because the university "
     "teaches pneumatics as a required course every semester.",
     "pneumatics", "pneumatic"),
    ("pressure/idiom",
     "The staff turnover rises sharply because the employees constantly "
     "work under pressures from senior management every quarter.",
     "pressures", "pressure"),
    ("compression/idiom",
     "The patient survives the emergency because the paramedic "
     "immediately performs compressions with practiced precision and "
     "skill.",
     "compressions", "compression"),
    ("friction/idiom",
     "The merger negotiations stall for weeks because the two companies "
     "report frictions over pricing and control.",
     "frictions", "friction"),
    ("torque/rejected",
     "The car performs well because the torques feel strong throughout "
     "the entire test drive today.",
     "torques", "torque"),
    ("mechanism/generic",
     "The patient copes well because the mechanisms helped during a "
     "difficult and stressful year.",
     "mechanisms", "mechanism"),
]
_REJECTED_ALIAS_SENTENCES = [
    (label, sentence) for label, sentence, _, _ in _REJECTED_ALIAS_CASES
]


@pytest.mark.parametrize("label,sentence", _REJECTED_ALIAS_SENTENCES)
def test_red_mechanical_rejected_alias_never_grants_reasoned(label, sentence):
    """Baseline (A): against the REAL, correct Mechanical alias map (only
    piston/valve/actuator), none of the 12 excluded signals may gain Layer-2
    substance evidence merely from their surface word — each sentence above
    is a genuine verb/idiom/meaning-shift use, not a mechanism explanation.
    This alone does NOT prove the guard is load-bearing — see the poisoned-
    map differential test below, which is the actual MD-1/MD-A protection."""
    assert _assess(sentence, MECH) == ASSERTED, label


@pytest.mark.parametrize(
    "label,sentence,alias_word,canonical_target", _REJECTED_ALIAS_CASES)
def test_red_rejected_alias_flips_to_reasoned_when_alias_map_is_poisoned(
        label, sentence, alias_word, canonical_target):
    """Load-bearing differential proof (B), independent-review MD-A
    correction: the SAME sentence that is ASSERTED above against the real
    map becomes REASONED here ONLY because the alias map is poisoned with
    exactly the rejected pair under test ({alias_word: canonical_target}).
    This is the genuine MD-1 recurrence guard — it demonstrates the
    classification actually depends on alias-map content for this specific
    sentence, rather than assuming it from sentence construction alone."""
    poisoned = dict(get_substance_signal_plural_aliases(MECH))
    poisoned[alias_word] = canonical_target
    with mock.patch("engine.progression_loop.get_substance_signal_plural_aliases",
                     return_value=poisoned):
        assert _assess(sentence, MECH) == REASONED, label


@pytest.mark.parametrize(
    "label,sentence,alias_word,canonical_target", _REJECTED_ALIAS_CASES)
def test_green_rejected_alias_neutral_control_unaffected_by_unrelated_poison(
        label, sentence, alias_word, canonical_target):
    """Neutral control (C) for the differential proof above: poisoning the
    map with an UNRELATED alias (never appearing in the sentence under test)
    must NOT flip the result to REASONED — proving the REASONED flip in the
    test above is specifically caused by the alias word under test being
    present and mapped, not by any alias-map mutation whatsoever (e.g. a
    gate implementation that ignored alias content and just checked "is the
    map non-default" would fail this control while passing the one above)."""
    del alias_word, canonical_target  # unused: the poison here is deliberately unrelated
    unrelated = dict(get_substance_signal_plural_aliases(MECH))
    unrelated["zzz_unrelated_neutral_control_alias"] = "piston"
    with mock.patch("engine.progression_loop.get_substance_signal_plural_aliases",
                     return_value=unrelated):
        assert _assess(sentence, MECH) == ASSERTED, label


def test_green_mechanical_excluded_set_is_exactly_twelve_and_disjoint_from_authorized():
    """Configuration/inventory pin — valid and useful, but NOT by itself
    sufficient MD-1/MD-A protection (§6 of the independent-review
    correction); the genuinely load-bearing behavioral proof is the
    poisoned-map differential test above."""
    aliases = get_substance_signal_plural_aliases(MECH)
    excluded = {"springs", "seals", "bearings", "gears", "levers",
                "hydraulics", "pneumatics", "pressures", "torques",
                "compressions", "frictions", "mechanisms"}
    assert len(excluded) == 12
    assert not (excluded & set(aliases.keys()))


# ========================================================= E. no morphology
def test_green_mechanical_no_generic_suffix_stripping():
    """A non-authorized Mechanical plural must not become recognized even
    when naive suffix removal would land on a real, currently-unaliased
    signal (e.g. stripping -s from "seals" would yield "seal", a real
    signal — but seal has NO authorized alias)."""
    for word in ("seals", "springs", "gears", "bearings", "levers"):
        assert word not in get_substance_signal_plural_aliases(MECH), word


# ================================================= F. registry validation
def _minimal_v1_pack(**overrides):
    data = {
        "schema_version": "1.0",
        "pack_id": "test_pack",
        "version": "1.0",
        "status": "registered",
        "display_name": "Test Pack",
        "classification_signals": [{"signal": "test_signal"}],
        "substance_signals": [{"signal": "widget"}, {"signal": "gadget"}],
        "gap_type_mappings": [{"gap_type_id": "TEST_GAP"}],
        "rule_nuances": [{"rule_id": "TEST_RULE"}],
    }
    data.update(overrides)
    return data


def _write_pack(tmp_path, subdir, data):
    d = tmp_path / subdir
    d.mkdir()
    (d / "domain.json").write_text(json.dumps(data), encoding="utf-8")


def test_green_registry_absent_alias_field_backward_compatible(tmp_path):
    _write_pack(tmp_path, "d", _minimal_v1_pack())
    reg = load_registry(str(tmp_path))
    assert "test_pack" in reg
    assert "substance_signal_plural_aliases" not in reg["test_pack"]


def test_green_registry_valid_alias_map_accepted(tmp_path):
    _write_pack(tmp_path, "d", _minimal_v1_pack(
        substance_signal_plural_aliases={"widgets": "widget"}))
    reg = load_registry(str(tmp_path))
    assert reg["test_pack"]["substance_signal_plural_aliases"] == {"widgets": "widget"}


def test_green_registry_empty_alias_map_accepted(tmp_path):
    _write_pack(tmp_path, "d", _minimal_v1_pack(substance_signal_plural_aliases={}))
    reg = load_registry(str(tmp_path))
    assert reg["test_pack"]["substance_signal_plural_aliases"] == {}


def test_red_registry_non_object_alias_field_rejected(tmp_path):
    _write_pack(tmp_path, "d", _minimal_v1_pack(
        substance_signal_plural_aliases=["widgets", "widget"]))
    with pytest.raises(RegistryLoadError):
        load_registry(str(tmp_path))


def test_red_registry_empty_alias_key_rejected(tmp_path):
    _write_pack(tmp_path, "d", _minimal_v1_pack(
        substance_signal_plural_aliases={"": "widget"}))
    with pytest.raises(RegistryLoadError):
        load_registry(str(tmp_path))


def test_red_registry_empty_alias_value_rejected(tmp_path):
    _write_pack(tmp_path, "d", _minimal_v1_pack(
        substance_signal_plural_aliases={"widgets": ""}))
    with pytest.raises(RegistryLoadError):
        load_registry(str(tmp_path))


def test_red_registry_non_string_alias_value_rejected(tmp_path):
    _write_pack(tmp_path, "d", _minimal_v1_pack(
        substance_signal_plural_aliases={"widgets": 123}))
    with pytest.raises(RegistryLoadError):
        load_registry(str(tmp_path))


def test_red_registry_dangling_alias_target_rejected(tmp_path):
    """The required, mandatory validation rule (contract §7/§11): an alias
    target absent from the SAME pack's substance_signals fails registry
    load, fail-closed."""
    _write_pack(tmp_path, "d", _minimal_v1_pack(
        substance_signal_plural_aliases={"widgets": "nonexistent_signal"}))
    with pytest.raises(RegistryLoadError):
        load_registry(str(tmp_path))


def test_green_registry_target_must_exist_in_same_pack_not_any_pack(tmp_path):
    """An alias target valid in one pack does not validate a different
    pack's alias — each pack is validated independently against its OWN
    substance_signals."""
    _write_pack(tmp_path, "pack_a", _minimal_v1_pack(
        pack_id="pack_a", substance_signals=[{"signal": "alpha"}]))
    _write_pack(tmp_path, "pack_b", _minimal_v1_pack(
        pack_id="pack_b", substance_signals=[{"signal": "beta"}],
        substance_signal_plural_aliases={"alphas": "alpha"}))
    with pytest.raises(RegistryLoadError):
        load_registry(str(tmp_path))


# ============================================== G. cross-domain isolation
def test_green_mechanical_alias_does_not_leak_into_electronics():
    mech_only = {"pistons", "valves", "actuators"}
    elec_aliases = get_substance_signal_plural_aliases(ELEC)
    assert not (mech_only & set(elec_aliases.keys()))


def test_green_electronics_alias_does_not_leak_into_mechanical():
    elec_only = {"sensors", "relays", "resistors", "batteries",
                 "capacitors", "motors", "leds", "ics"}
    mech_aliases = get_substance_signal_plural_aliases(MECH)
    assert not (elec_only & set(mech_aliases.keys()))


def test_green_mechanical_plural_does_not_match_as_electronics_substance():
    """A genuinely Mechanical plural-aliased word must not be recognized as
    Electronics substance evidence merely by existing in the Mechanical
    pack — cross-domain isolation exercised through the real gate."""
    resp = "The circuit activates because the pistons compress the air " \
           "efficiently and reliably."
    assert _assess(resp, ELEC) == ASSERTED


# ===================================================== H. outcome sensitivity
def _run_two_turn_gap(domain, first, second):
    state = IdeaState(idea_id="l2sc01-outcome-probe")
    state.domain = domain
    state.gaps.append(Gap(MECHANISM_COMPLETENESS, OPEN, 0))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        integrate_response(state, MECHANISM_COMPLETENESS, "Q1", first)
        return integrate_response(state, MECHANISM_COMPLETENESS, "Q2", second)


def test_green_outcome_sensitivity_plural_now_closes_gap_like_singular():
    """End-to-end, through the real gap-closure state machine: the
    originally-demonstrated WARN-vs-PASS divergence for a plural-only
    Mechanical substance word is now fixed for an authorized pair."""
    weak = "It has a mechanism."
    plural_only = ("The mechanism engages because the pistons mesh with the "
                   "drive shaft smoothly and reliably.")
    singular_only = ("The mechanism engages because the piston meshes with "
                     "the drive shaft smoothly and reliably.")
    transition_plural, reason_plural = _run_two_turn_gap(MECH, weak, plural_only)
    transition_singular, reason_singular = _run_two_turn_gap(MECH, weak, singular_only)
    assert transition_plural == "PASS", reason_plural
    assert transition_singular == "PASS", reason_singular
    assert transition_plural == transition_singular
