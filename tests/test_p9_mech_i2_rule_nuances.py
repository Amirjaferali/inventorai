"""P9-MECH-I2 — Mechanical Qualification-Grade Rule Nuances pins.

Governed by the AUTHORITATIVE increment contract
``docs/governance/P9_MECH_I2_QUALIFICATION_GRADE_RULE_NUANCES_CONTRACT.md``.

Repository truth (mechanically verified at the contract gate): ``rule_nuances``
are ACCESSOR-ONLY — ``engine.domain_rules.get_active_rules`` is the sole reader,
projects only ``modifier_value``, and has NO downstream runtime caller. The I2
enrichment is therefore metadata-only with an EXPECTED RUNTIME DIFFERENTIAL OF
ZERO; these pins prove both the qualification-grade shape/content AND the
invariance of every runtime-visible surface. Anti-overclaim protection is the
EXACT-CONTENT equality pin on descriptions and modifier_type (any added or
paraphrased expertise claim, however worded, flips RED); no simple word-list is
relied on.
"""

import hashlib
import json
import os
import warnings

from engine.domain_activation import activated_domains
from engine.domain_registry import load_registry
from engine.domain_rules import classify_domain, get_active_rules
from engine.safety_signal import has_governed_safety_cue_family

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DOMAINS = os.path.join(_REPO, "domains")
_MECH_PATH = os.path.join(_DOMAINS, "mechanical", "domain.json")
_PROV_PATH = os.path.join(_DOMAINS, "domain_provenance.json")

# --- Accessor baselines (frozen at the contract gate; MUST never change in I2). ---
_ACCESSOR_BASELINES = {
    "mechanical": ["MECHANISM_COMPLETENESS", "PHYSICAL_FEASIBILITY", "BOUNDARY_AMBIGUITY"],
    "electronics_electrical": [
        "PHYSICAL_PRINCIPLE_REQUIRED",
        "POWER_ACKNOWLEDGMENT_IF_ENERGY",
        "NO_PLATFORM_SPECIFIC_NAMING",
    ],
    "software": ["MECHANISM_COMPLETENESS", "BOUNDARY_AMBIGUITY"],
    "medical_device": ["MECHANISM_COMPLETENESS", "PHYSICAL_FEASIBILITY", "BOUNDARY_AMBIGUITY"],
}

# --- Truthful modifier_type: the entries ARE governed active-gap-rule markers
# (each modifier_value is one of the pack's own gap_type_ids, migrated verbatim
# from the historical hardcoded get_active_rules branch). Explicitly NOT
# electronics' requirement-marker semantic. ---
_TRUTHFUL_MODIFIER_TYPE = "active_gap_rule_marker"

# --- Exact approved qualification-grade entries (equality-pinned in full). ---
_APPROVED_NUANCES = [
    {
        "rule_id": "mechanical:RN001",
        "description": (
            "Active gap rule marking the Mechanical Mechanism Completeness gap type: "
            "the inventor's description is examined, at concept level only, for what "
            "moves, connects, or transfers force, using the pack's governed questions "
            "for this gap type."
        ),
        "layer": 1,
        "modifier_type": _TRUTHFUL_MODIFIER_TYPE,
        "modifier_value": "MECHANISM_COMPLETENESS",
        "provenance_ref": "mechanical:PR003",
    },
    {
        "rule_id": "mechanical:RN002",
        "description": (
            "Active gap rule marking the Mechanical Physical Feasibility gap type: the "
            "inventor's stated physical principle (e.g. leverage, spring tension, gear "
            "ratio, friction) and stated operating constraints are examined at concept "
            "level only, using the pack's governed questions for this gap type."
        ),
        "layer": 1,
        "modifier_type": _TRUTHFUL_MODIFIER_TYPE,
        "modifier_value": "PHYSICAL_FEASIBILITY",
        "provenance_ref": "mechanical:PR003",
    },
    {
        "rule_id": "mechanical:RN003",
        "description": (
            "Active gap rule marking the Mechanical Boundary Ambiguity gap type: what "
            "the mechanism does not do or cover, and its concrete physical "
            "differentiation from existing mechanical approaches, are examined at "
            "concept level only, using the pack's governed questions for this gap type."
        ),
        "layer": 2,
        "modifier_type": _TRUTHFUL_MODIFIER_TYPE,
        "modifier_value": "BOUNDARY_AMBIGUITY",
        "provenance_ref": "mechanical:PR003",
    },
]

# --- Frozen canonical hashes of every OTHER mechanical field (byte-frozen in I2). ---
# P9-MECH-I3 mechanically-forced adjustment (disclosed): the classification_signals
# and substance_signals hashes below were re-frozen at the I3-authorized values —
# the AUTHORITATIVE P9-MECH-I3 contract owns exactly those two lists (evidence-based
# AB-006 dispositions), so the I2-era freeze of them was an increment-scoped
# protection that I3 legitimately supersedes. The load-bearing purpose is preserved:
# every other field stays frozen at its I2 value, and the two adjusted fields are
# now pinned MORE strongly by tests/test_p9_mech_i3_signal_quality.py's
# exact-content inventory equality pins.
_FROZEN_MECH_FIELDS = {
    "classification_signals": "860ce084389c842e3dc2b5771651bb145579cc19a6c53f303f198ea8419c498e",
    "substance_signals": "c14ae2d504479d191f91a16c960d065400479b4ce6238757fb5ab4cb1b094ac5",
    "gap_type_mappings": "857820ed6be7a25fa9200756b4453487b87144b45fc2fafb9fcd53158ef2e7f2",
    "aliases": "bc7f35e42f32845fad8c2d2e0c5c3ed39a84e54673f351eb581e9d8b38368bd2",
    # P9-MECH-SF reconciliation (contract §4 item 8, disclosed): the mandatory
    # declaration truthfulness cascade changed EXACTLY these two fields (the
    # detection-scoped safety statements); re-frozen at the cascade values.
    # Every other frozen field above/below is byte-identical to its prior value.
    "capability_declaration": "b5452a9903b37c382bd59abef9e145cebcdb954185b8645f769376c441e9e491",
    "coverage_declaration": "9dd7a4cc8587b31ca91b2dbccb964c7e8ddcf010aa6df9685d099d7fdc33bb5c",
    "journey_extension": "85473dc88684f165cc080218237b0e76573bc1b80ea7cfa77cb76b78c0f28bcc",
}

# --- Other-pack byte pins (unchanged since P9-MECH-I1; re-frozen for I2). ---
_FROZEN_PACK_SHA256 = {
    "electronics_electrical": "3539cfc62710da92f12ac529c07ddaea85011536e5c9f88efb2e2303bb1b964c",
    "medical_device": "6070cf9281a7a376780175e7e1d3879be598384bcaf4dc370e56f7bf613e3ade",
    "software": "1c9cefa14641c079ddb5c21c59f398866adf43561101743b67e611936a67e3a7",
    "iot_electronics": "f04c825ad25dea0c6db2ee310649fe377329f30c5461f2756019104013e53406",
}

# --- Classifier corpus pins (parent-frozen; declarations/nuances are not classifier inputs). ---
_CLASSIFIER_PINS = [
    ("A gear and pulley hoist with a crankshaft drive", "single", "mechanical"),
    ("ESP32 sensor circuit with WiFi", "single", "electronics_electrical"),
    ("a catheter for veins", "single", "medical_device"),
    ("an app to organize daily schedules", "single", "software"),
    ("gear and catheter", "single", "medical_device"),
    ("circuit and hinge", "single", "electronics_electrical"),
    ("nothing recognizable at all", "none", None),
    ("a system of gears and levers", "single", "mechanical"),
]


def _mech():
    with open(_MECH_PATH, encoding="utf-8") as fh:
        return json.load(fh)


def _canon_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


# ---------------------------------------------------------------- shape / content


def test_exact_entry_count():
    assert len(_mech()["rule_nuances"]) == 3


def test_exact_modifier_value_sequence():
    assert [rn["modifier_value"] for rn in _mech()["rule_nuances"]] == _ACCESSOR_BASELINES[
        "mechanical"
    ]


def test_full_shape_per_entry():
    for i, rn in enumerate(_mech()["rule_nuances"]):
        assert sorted(rn.keys()) == [
            "description",
            "layer",
            "modifier_type",
            "modifier_value",
            "provenance_ref",
            "rule_id",
        ], f"rule_nuances[{i}] lacks the qualification-grade full shape (parent deficiency)"


def test_truthful_modifier_type_exact():
    for rn in _mech()["rule_nuances"]:
        assert rn["modifier_type"] == _TRUTHFUL_MODIFIER_TYPE
        # m10 guard: the electronics requirement-marker semantic is a DIFFERENT
        # meaning and must never be copied onto the mechanical gap-rule markers.
        assert rn["modifier_type"] != "additional_signal_required"


def test_exact_approved_entries():
    assert _mech()["rule_nuances"] == _APPROVED_NUANCES


def test_layers_grounded_in_gap_types():
    data = _mech()
    gap_layers = {g["gap_type_id"]: g["layer"] for g in data["gap_type_mappings"]}
    for rn in data["rule_nuances"]:
        assert rn["layer"] == gap_layers[rn["modifier_value"]]


def test_modifier_values_are_pack_gap_types():
    data = _mech()
    gap_ids = {g["gap_type_id"] for g in data["gap_type_mappings"]}
    for rn in data["rule_nuances"]:
        assert rn["modifier_value"] in gap_ids


# ---------------------------------------------------------------- provenance


def test_provenance_resolution():
    with open(_PROV_PATH, encoding="utf-8") as fh:
        records = {r["record_id"]: r for r in json.load(fh)["records"]}
    for rn in _mech()["rule_nuances"]:
        assert rn["provenance_ref"] == "mechanical:PR003"
    assert "mechanical:PR003" in records, "additive provenance record mechanical:PR003 missing"
    pr3 = records["mechanical:PR003"]
    assert pr3["pack_id"] == "mechanical"
    assert pr3["source_type"] == "governance_record"
    assert "P9_MECH_I2" in pr3["notes"] or "P9-MECH-I2" in pr3["notes"]
    # Existing records untouched alongside it.
    assert "mechanical:PR001" in records and "mechanical:PR002" in records


# ---------------------------------------------------------------- runtime-inertness disclosure


def test_runtime_inertness_disclosure():
    notes = _mech()["_governance_notes"]
    assert "p9_mech_i2_rule_nuances" in notes, "runtime-inertness disclosure absent (parent deficiency)"
    note = notes["p9_mech_i2_rule_nuances"]
    for frag in (
        "get_active_rules",
        "modifier_value",
        "no downstream runtime consumer",
        "metadata",
    ):
        assert frag in note, f"disclosure missing required fragment: {frag!r}"
    # The historical governance note about the original migration is preserved.
    assert "rule_nuances_absent" in notes


# ---------------------------------------------------------------- frozen-field invariance


def test_all_other_mechanical_fields_byte_stable():
    data = _mech()
    for field, expected in _FROZEN_MECH_FIELDS.items():
        assert _canon_hash(data[field]) == expected, f"frozen mechanical field changed: {field}"


def test_other_packs_byte_identical():
    for pack, expected in _FROZEN_PACK_SHA256.items():
        path = os.path.join(_DOMAINS, pack, "domain.json")
        with open(path, "rb") as fh:
            digest = hashlib.sha256(fh.read()).hexdigest()
        assert digest == expected, f"{pack} pack changed (forbidden in P9-MECH-I2)"


# ---------------------------------------------------------------- runtime invariance


def test_accessor_four_pack_identity_and_unknown_empty():
    for domain, expected in _ACCESSOR_BASELINES.items():
        assert get_active_rules(domain) == expected, f"accessor output changed for {domain}"
    assert get_active_rules("no_such_domain") == []


def test_classifier_corpus_zero_differential():
    for text, kind, selected in _CLASSIFIER_PINS:
        c = classify_domain(text)
        assert (c.kind.value, c.selected_domain) == (kind, selected), text


def test_recognized_set_stable_and_iot_still_skipped():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        registry = load_registry(_DOMAINS)
    assert sorted(registry) == [
        "electronics_electrical",
        "mechanical",
        "medical_device",
        "software",
    ]
    assert "iot_electronics" not in registry


def test_activation_state_unchanged():
    assert activated_domains() == ["electronics_electrical"]


def test_safety_family_now_governed_for_mechanical():
    """P9-MECH-SF reconciliation (contract §4 item 2, disclosed): the I2-era
    absence pin flipped — the governed Mechanical safety-cue family exists
    (evidence: tests/test_p9_mech_safety_cue_family.py)."""
    assert has_governed_safety_cue_family("mechanical") is True


def test_deterministic_repeated_loads():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        first = load_registry(_DOMAINS)
        second = load_registry(_DOMAINS)
    assert first["mechanical"]["rule_nuances"] == second["mechanical"]["rule_nuances"]
    assert get_active_rules("mechanical") == get_active_rules("mechanical")
