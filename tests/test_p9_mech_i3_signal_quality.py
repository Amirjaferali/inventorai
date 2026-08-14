"""P9-MECH-I3 — Mechanical Signal-Quality / AB-006 Evidence & Disposition pins.

Governed by the AUTHORITATIVE increment contract
``docs/governance/P9_MECH_I3_SIGNAL_QUALITY_AB006_DISPOSITION_CONTRACT.md``.

Evidence-derived dispositions implemented (each grounded by parent-RED cases in
this file — see the corpus sections; the disposition record lives in the pack's
``_governance_notes.p9_mech_i3_signal_quality``):

  * ``mechanism``  (classification) — REMOVE (reclassify to substance-only, where
    it already exists): proven false attraction of software prose via the OD2
    legacy 1-1 tie ("a voting mechanism for the app" → mechanical on the parent).
  * ``locking``    (classification) — REPLACE with the multi-word signal
    ``locking mechanism`` (narrowing): kills software-prose false attraction
    ("optimistic locking strategy for the api") while keeping the genuine
    mechanical phrase; bidirectional evidence pinned below.
  * ``bracket``, ``fastener``, ``valve``, ``actuator`` — RETAIN WITH EVIDENCE
    (medical/electronics precedence structurally protects the cross-domain valve/
    actuator cases; bracket carries one documented residual collision).
  * ``force``, ``bar`` (substance) — REMOVE: proven SUBSTRING false-substance
    defect (identical vague "somehow" answers flip ASSERTED→REASONED solely
    because "bar" hides in "barrier" / "force" in "reinforced").
  * ``mechanism``, ``pressure``, ``compression`` (substance) — RETAIN WITH
    EVIDENCE (their substring class is clean or domain-scoped; residuals noted).

Runtime differential is BOUNDED and fully categorized (Cat-A mechanism removal;
Cat-B locking replacement; Cat-C substance removals); every other surface is
pinned invariant, including the engine files by byte hash. The OD2 legacy
precedence RULE is untouched — the Cat-A/Cat-B deltas are tie-COMPOSITION
changes from corrected vocabulary, individually disclosed in the corpus pins.
The established legacy classifier-pin corpus is EIGHT texts (corrected count
per independent review) and is pinned unchanged.
"""

import hashlib
import json
import os
import warnings

from engine.domain_activation import activated_domains
from engine.domain_registry import load_registry
from engine.domain_rules import classify_domain, get_active_rules
from engine.progression_loop import assess_response
from engine.safety_signal import has_governed_safety_cue_family

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DOMAINS = os.path.join(_REPO, "domains")
_MECH_PATH = os.path.join(_DOMAINS, "mechanical", "domain.json")
_PROV_PATH = os.path.join(_DOMAINS, "domain_provenance.json")

# ---------------------------------------------------------------- approved final inventories

_APPROVED_CLASSIFICATION_SIGNALS = [
    "gear", "hinge", "spring", "clamp", "lever", "pulley", "bearing", "shaft",
    "linkage", "torque", "friction", "joint", "actuator", "piston", "valve",
    "bracket", "fastener", "locking mechanism",
]
_APPROVED_SUBSTANCE_SIGNALS = [
    "piston", "spring", "valve", "gear", "lever", "hydraulic", "pneumatic",
    "pressure", "torque", "compression", "seal", "bearing", "actuator",
    "mechanism", "friction",
]

# Engine byte freeze (no classifier/tie/substance-semantics change may ride along).
_FROZEN_ENGINE_SHA256 = {
    "engine/domain_rules.py": "5df2ae26b0a6e78f37bb467d1d8b3d377596f9fcbbc7f869d1ed1ac5b5ab204b",
    "engine/progression_loop.py": "bbb49b49f388dba2f0b906a79bdd656de23b33ec7101bd9d9da9c290ae45c4c5",
}
# Other-pack byte freeze (unchanged lineage from I1/I2).
_FROZEN_PACK_SHA256 = {
    "electronics_electrical": "3539cfc62710da92f12ac529c07ddaea85011536e5c9f88efb2e2303bb1b964c",
    "medical_device": "6070cf9281a7a376780175e7e1d3879be598384bcaf4dc370e56f7bf613e3ade",
    "software": "1c9cefa14641c079ddb5c21c59f398866adf43561101743b67e611936a67e3a7",
    "iot_electronics": "f04c825ad25dea0c6db2ee310649fe377329f30c5461f2756019104013e53406",
}
# Mechanical fields OUTSIDE the two authorized signal lists stay canonically frozen.
_FROZEN_MECH_FIELDS = {
    "gap_type_mappings": "857820ed6be7a25fa9200756b4453487b87144b45fc2fafb9fcd53158ef2e7f2",
    "aliases": "bc7f35e42f32845fad8c2d2e0c5c3ed39a84e54673f351eb581e9d8b38368bd2",
    # P9-MECH-SF reconciliation (contract §4 item 9, disclosed): the mandatory
    # declaration truthfulness cascade changed EXACTLY these two fields (the
    # detection-scoped safety statements); re-frozen at the cascade values.
    # gap_type_mappings/aliases/journey_extension are byte-identical.
    "capability_declaration": "b5452a9903b37c382bd59abef9e145cebcdb954185b8645f769376c441e9e491",
    "coverage_declaration": "9dd7a4cc8587b31ca91b2dbccb964c7e8ddcf010aa6df9685d099d7fdc33bb5c",
    "journey_extension": "85473dc88684f165cc080218237b0e76573bc1b80ea7cfa77cb76b78c0f28bcc",
}

# The established EIGHT-text legacy classifier-pin corpus (corrected count) — invariant.
_LEGACY_PINS = [
    ("A gear and pulley hoist with a crankshaft drive", "single", "mechanical"),
    ("ESP32 sensor circuit with WiFi", "single", "electronics_electrical"),
    ("a catheter for veins", "single", "medical_device"),
    ("an app to organize daily schedules", "single", "software"),
    ("gear and catheter", "single", "medical_device"),
    ("circuit and hinge", "single", "electronics_electrical"),
    ("nothing recognizable at all", "none", None),
    ("a system of gears and levers", "single", "mechanical"),
]

# Defect corpus — CORRECTED outcomes (Cat-A/Cat-B deltas vs parent; disclosed tie-composition changes).
_CORRECTED_OUTCOMES = [
    # Cat-A: 'mechanism' removed from classification (parent: mechanical via legacy tie / solo match).
    ("a voting mechanism for the app", "single", "software"),
    ("a delivery mechanism for software updates", "single", "software"),
    ("a mechanism that folds chairs flat", "none", None),  # documented recall trade-off (Cat-A)
    # Cat-B: 'locking' replaced by multi-word 'locking mechanism' (parent: mechanical via legacy tie).
    ("optimistic locking strategy for the api", "single", "software"),
    ("row locking in the database engine", "single", "software"),
]

# Protected outcomes — must classify the SAME as on the parent (retention/precedence evidence).
_PROTECTED_OUTCOMES = [
    # genuine mechanical phrases still captured (multi-word replacement working):
    ("a door locking mechanism with a spring latch", "single", "mechanical"),
    ("a locking mechanism for the cabinet", "single", "mechanical"),
    ("a locking mechanisms catalog for cabinets", "single", "mechanical"),  # bounded plural on final token
    # retained-signal evidence:
    ("a hinge mounted bracket with a lever and a small switch", "single", "mechanical"),
    ("a wall bracket for hanging shelves", "single", "mechanical"),
    ("a quick release fastener for bicycle wheels", "single", "mechanical"),
    ("a valve that regulates water flow in pipes", "single", "mechanical"),
    # cross-domain ownership structurally protected by precedence (medical > mech; elec > mech):
    ("an artificial heart valve implant", "single", "medical_device"),
    ("a replacement heart valve", "single", "medical_device"),
    ("a linear actuator with a servo circuit", "single", "electronics_electrical"),
    # EXPLICIT tie cases preserved (OD2 legacy precedence rule untouched):
    ("a pulley and a database", "single", "mechanical"),
    ("a lever and an app", "single", "mechanical"),
    ("gear and catheter", "single", "medical_device"),
    # NONE / unknown boundary:
    ("a better way to organize my day", "none", None),
    ("nothing recognizable at all", "none", None),
]

# Sibling single-domain corpus — byte-identical outcomes required.
_SIBLING_PINS = [
    ("ESP32 sensor circuit with WiFi", "single", "electronics_electrical"),
    ("a resistor and a capacitor on a circuit board", "single", "electronics_electrical"),
    ("an app to organize daily schedules", "single", "software"),
    ("a sql database backend with an api", "single", "software"),
    ("a catheter for veins", "single", "medical_device"),
    ("an implantable stent for cardiac patients", "single", "medical_device"),
]

_FLAGGED = [
    "mechanism", "force", "bar", "bracket", "fastener", "locking",
    "valve", "pressure", "compression", "actuator",
]


def _mech():
    with open(_MECH_PATH, encoding="utf-8") as fh:
        return json.load(fh)


def _canon_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


# ---------------------------------------------------------------- inventories (anti-stuffing)


def test_exact_final_classification_signal_inventory():
    signals = [s["signal"] for s in _mech()["classification_signals"]]
    assert signals == _APPROVED_CLASSIFICATION_SIGNALS, (
        "classification inventory must equal the approved evidence-derived set "
        "(parent deficiency: contains 'mechanism' and single-word 'locking')"
    )


def test_exact_final_substance_signal_inventory():
    signals = [s["signal"] for s in _mech()["substance_signals"]]
    assert signals == _APPROVED_SUBSTANCE_SIGNALS, (
        "substance inventory must equal the approved evidence-derived set "
        "(parent deficiency: contains substring-defective 'force' and 'bar')"
    )


def test_retained_signal_dormant_metadata_unchanged():
    # Retained classification signals keep their exact dormant weight/layer values;
    # the replacement 'locking mechanism' carries the replaced entry's dormant pattern.
    expected = {
        "gear": (0.9, 2), "hinge": (0.8, 2), "spring": (0.8, 1), "clamp": (0.7, 2),
        "lever": (0.9, 1), "pulley": (0.9, 1), "bearing": (0.8, 2), "shaft": (0.8, 2),
        "linkage": (0.9, 2), "locking mechanism": (0.4, 2), "torque": (0.9, 1),
        "friction": (0.8, 1), "joint": (0.7, 2), "actuator": (0.6, 2),
        "piston": (0.9, 2), "valve": (0.8, 2), "bracket": (0.5, 2), "fastener": (0.4, 2),
    }
    actual = {s["signal"]: (s["weight"], s["layer"]) for s in _mech()["classification_signals"]}
    assert actual == expected


# ---------------------------------------------------------------- disposition record


def test_disposition_record_complete():
    notes = _mech()["_governance_notes"]
    assert "p9_mech_i3_signal_quality" in notes, "disposition record absent (parent deficiency)"
    record = notes["p9_mech_i3_signal_quality"]
    for signal in _FLAGGED:
        assert f"{signal}:" in record, f"flagged signal not dispositioned: {signal!r}"
    for required in (
        "REMOVE", "REPLACE", "RETAIN WITH EVIDENCE", "no downstream",
        "OD2", "residual", "mechanical:PR004",
    ):
        assert required in record, f"disposition record missing element: {required!r}"
    # Exact-content pin (sha256) of the FULL disposition record: any reworded,
    # gutted, or capability-inflating paraphrase (e.g. accuracy "guarantees")
    # flips RED — the m10 guard; fragments above give right-reason granularity.
    assert (
        hashlib.sha256(record.encode()).hexdigest()
        == "f9f0241fbdbef13691373993d2a3d85bf365783cb2aeb93ee830701f6544ccab"
    ), "disposition record content changed from the approved reviewed text"
    # Historical AB-006 flag note preserved untouched.
    assert "ab006_candidates" in notes
    assert "Flagged for AB-006 Domain Signal Quality Review" in notes["ab006_candidates"]


def test_replacement_signal_provenance_and_context():
    entries = {s["signal"]: s for s in _mech()["classification_signals"]}
    lm = entries["locking mechanism"]
    assert lm["provenance_ref"] == "mechanical:PR004"
    with open(_PROV_PATH, encoding="utf-8") as fh:
        records = {r["record_id"]: r for r in json.load(fh)["records"]}
    assert "mechanical:PR004" in records
    pr4 = records["mechanical:PR004"]
    assert pr4["pack_id"] == "mechanical"
    assert pr4["source_type"] == "governance_record"
    assert "P9_MECH_I3" in pr4["notes"] or "P9-MECH-I3" in pr4["notes"]
    for rid in ("mechanical:PR001", "mechanical:PR002", "mechanical:PR003"):
        assert rid in records


# ---------------------------------------------------------------- corrected & protected outcomes


def test_corrected_defect_outcomes():
    for text, kind, selected in _CORRECTED_OUTCOMES:
        c = classify_domain(text)
        assert (c.kind.value, c.selected_domain) == (kind, selected), text


def test_protected_outcomes_unchanged():
    for text, kind, selected in _PROTECTED_OUTCOMES:
        c = classify_domain(text)
        assert (c.kind.value, c.selected_domain) == (kind, selected), text


def test_legacy_eight_pin_corpus_unchanged():
    assert len(_LEGACY_PINS) == 8  # corrected count per independent review
    for text, kind, selected in _LEGACY_PINS:
        c = classify_domain(text)
        assert (c.kind.value, c.selected_domain) == (kind, selected), text


def test_sibling_single_domain_corpus_unchanged():
    for text, kind, selected in _SIBLING_PINS:
        c = classify_domain(text)
        assert (c.kind.value, c.selected_domain) == (kind, selected), text


# ---------------------------------------------------------------- substance-path correction (Cat-C)


def test_substring_substance_defect_corrected():
    # Parent defect: identical vague answers flipped ASSERTED→REASONED solely via
    # 'bar' in 'barrier' / 'force' in 'reinforced'. Corrected: both now ASSERTED.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        vague_bar = assess_response(
            "It somehow works because the barrier blocks the door from sliding out of its track",
            "mechanical",
        )
        vague_force = assess_response(
            "It somehow holds together because the reinforced edge takes the load when pushed",
            "mechanical",
        )
    assert vague_bar == "ASSERTED"
    assert vague_force == "ASSERTED"


def test_genuine_substance_still_recognized():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        genuine = assess_response(
            "The spring pushes the lever back because the coil stores energy when compressed",
            "mechanical",
        )
    assert genuine == "REASONED"


# ---------------------------------------------------------------- invariance pins


def test_engine_files_byte_frozen():
    for path, expected in _FROZEN_ENGINE_SHA256.items():
        with open(os.path.join(_REPO, path), "rb") as fh:
            digest = hashlib.sha256(fh.read()).hexdigest()
        assert digest == expected, f"engine file changed (forbidden in P9-MECH-I3): {path}"


def test_other_packs_byte_identical():
    for pack, expected in _FROZEN_PACK_SHA256.items():
        with open(os.path.join(_DOMAINS, pack, "domain.json"), "rb") as fh:
            digest = hashlib.sha256(fh.read()).hexdigest()
        assert digest == expected, f"{pack} pack changed (forbidden in P9-MECH-I3)"


def test_frozen_mechanical_fields_byte_stable():
    data = _mech()
    for field, expected in _FROZEN_MECH_FIELDS.items():
        assert _canon_hash(data[field]) == expected, f"frozen mechanical field changed: {field}"
    # I2 nuances stay exactly as merged (accessor projection pinned below).
    assert [rn["modifier_value"] for rn in data["rule_nuances"]] == [
        "MECHANISM_COMPLETENESS", "PHYSICAL_FEASIBILITY", "BOUNDARY_AMBIGUITY",
    ]


def test_accessor_outputs_unchanged():
    assert get_active_rules("mechanical") == [
        "MECHANISM_COMPLETENESS", "PHYSICAL_FEASIBILITY", "BOUNDARY_AMBIGUITY",
    ]
    assert get_active_rules("electronics_electrical") == [
        "PHYSICAL_PRINCIPLE_REQUIRED", "POWER_ACKNOWLEDGMENT_IF_ENERGY",
        "NO_PLATFORM_SPECIFIC_NAMING",
    ]
    assert get_active_rules("no_such_domain") == []


def test_recognized_set_and_activation_unchanged():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        registry = load_registry(_DOMAINS)
    assert sorted(registry) == [
        "electronics_electrical", "mechanical", "medical_device", "software",
    ]
    assert "iot_electronics" not in registry
    assert activated_domains() == ["electronics_electrical"]


def test_safety_family_now_governed_for_mechanical():
    """P9-MECH-SF reconciliation (contract §4 item 3, disclosed): the I3-era
    absence pin flipped — the governed Mechanical safety-cue family exists
    (evidence: tests/test_p9_mech_safety_cue_family.py)."""
    assert has_governed_safety_cue_family("mechanical") is True


def test_deterministic_repeated_classification():
    for text in ("a voting mechanism for the app", "a locking mechanism for the cabinet"):
        first = classify_domain(text)
        second = classify_domain(text)
        assert (first.kind, first.selected_domain) == (second.kind, second.selected_domain)
