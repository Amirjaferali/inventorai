"""P9-MECH-I1 — Mechanical Truthful Capability & Coverage Declaration pins.

Governed by the AUTHORITATIVE increment contract
``docs/governance/P9_MECH_I1_TRUTHFUL_CAPABILITY_COVERAGE_DECLARATION_CONTRACT.md``
(P9-MECH-QC lineage; OD-M2 = D-P9-MECH-02, Option B-hardened, Mechanical-specific).

These tests pin the DECLARATION-ONLY increment: additive, truthful, provenance-
tagged capability/coverage metadata in ``domains/mechanical/domain.json`` with
ZERO runtime-behavior change. Anti-overclaim protection is an EXACT-CONTENT pin
(any added or paraphrased covered claim — FEA, "thermal simulation", or any
other unsupported expertise, however worded — flips the equality pins RED); the
lexicon guard is defense-in-depth only, not the primary protection.

P9-MECH-SF RECONCILIATION (contract §4 items 6-7, disclosed): the governed
Mechanical safety-cue family now EXISTS (merge lineage of the corrected
P9-MECH-SF contract, base ``d1b79ef4``), so this file's I1-era safety pins
were reconciled: the family-absence pin flipped to the governed-present state;
the OD-M2 clause-1 "NOT COVERED pending…" statement pins were re-pinned to the
truthful detection-scoped cascade statements; the covered/supported equality
pins gained EXACTLY the detection entry; and "safety-signal derivation" left
the mandatory NOT-COVERED concepts (detection is now covered — "safety
determination" remains NOT COVERED, unchanged). Every non-safety pin is
byte-identical to its I1 value. Evidence for the family itself lives in
``tests/test_p9_mech_safety_cue_family.py``.
"""

import hashlib
import json
import os
import warnings

import pytest

from engine.domain_activation import activated_domains
from engine.domain_registry import load_registry
from engine.domain_rules import classify_domain
from engine.safety_signal import (
    derive_inventor_stated_safety_signals,
    has_governed_safety_cue_family,
)

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DOMAINS = os.path.join(_REPO, "domains")
_MECH_PATH = os.path.join(_DOMAINS, "mechanical", "domain.json")
_PROV_PATH = os.path.join(_DOMAINS, "domain_provenance.json")

# --- Frozen byte-identity pins for every OTHER pack (P9-MECH-I1 forbids touching them). ---
# L2SC-01 reconciliation (disclosed; docs/governance/L2SC01_SUBSTANCE_SIGNAL_
# PLURAL_ALIAS_INCREMENT_CONTRACT.md §10): electronics_electrical re-frozen
# after adding the authorized, additive-only `substance_signal_plural_aliases`
# field (the 8 historical pairs migrated from the retired engine-hardcoded
# map). classification_signals/substance_signals content is byte-unchanged
# (see tests/test_p9_mech_safety_cue_family.py::test_signal_inventory_
# unchanged_proof, unaffected by this reconciliation). medical_device/
# software/iot_electronics hashes are untouched.
_FROZEN_PACK_SHA256 = {
    "electronics_electrical": "53f431e38a70c2b621e19afb7323ad9bc4732c6c4151ea6b8c46a3214f098dfb",
    "medical_device": "6070cf9281a7a376780175e7e1d3879be598384bcaf4dc370e56f7bf613e3ade",
    "software": "1c9cefa14641c079ddb5c21c59f398866adf43561101743b67e611936a67e3a7",
    "iot_electronics": "f04c825ad25dea0c6db2ee310649fe377329f30c5461f2756019104013e53406",
}

# --- The exact approved truthful covered content (P9-MECH-QC §5 concept-level scope ONLY).
# EXACT equality is the anti-smuggling protection: any addition, removal, or rewording is RED.
_APPROVED_COVERED_AREAS = [
    "Concept-level explanation of the mechanical mechanism: what moves, connects, or transfers force",
    "Concept-level physical-feasibility reasoning against the inventor's stated principles (e.g. leverage, spring tension, gear ratio, friction)",
    "Concept-level boundary and differentiation reasoning versus existing mechanical approaches",
    "Mechanical mechanism completeness as a reasoning quality assessment",
    "Gap detection for the pack's governed gap types (MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY)",
    # P9-MECH-SF cascade (the ONLY covered addition; detection-scoped, never a
    # safety determination):
    "Detection of inventor-stated mechanical safety signals via the governed "
    "Mechanical safety-cue family: flags safety-relevant failure statements "
    "the inventor has already made (e.g. crush, pinch, entanglement, "
    "stored-energy release, part ejection) for required independent "
    "validation — detection only, never a safety determination",
]
_APPROVED_SUPPORTED_ANALYSIS = [
    "concept_level_mechanism_completeness",
    "concept_level_physical_feasibility_reasoning",
    "concept_level_boundary_differentiation",
    "governed_gap_type_question_service",
    "inventor_stated_safety_signal_detection",   # P9-MECH-SF cascade
]

# P9-MECH-SF reconciliation: the OD-M2 clause-1 statement was REPLACED by the
# truthful detection-scoped safety-boundary statement; these fragments pin the
# replacement in BOTH declarations (safety determination stays NOT COVERED).
_ODM2_SUBSTRINGS = (
    "Safety determination of any kind is NOT COVERED",
    "governed Mechanical safety-cue family (mechanical:PR005)",
    "safety-signal DETECTION only",
    "requires independent validation",
    "never a determination that the idea is safe or unsafe",
)

# Mandatory NOT-COVERED concepts (contract §4 deliverable (a); checked as case-insensitive
# substrings over the joined not_covered_areas text). P9-MECH-SF reconciliation:
# "safety-signal derivation" left this list — detection is now truthfully
# covered by the governed family; "safety determination" remains, unchanged.
_MANDATORY_NOT_COVERED_CONCEPTS = (
    "fea",
    "fatigue",
    "tolerance",
    "gd&t",
    "material",
    "manufacturing process",
    "cad",
    "physical-fit",
    "regulatory",
    "certification",
    "cost",
    "supply chain",
    "physical testing",
    "thermal",
    "safety determination",
)

# Defense-in-depth lexicon guard over COVERED/SUPPORTED content only.
_FORBIDDEN_IN_COVERED = (
    "fea",
    "finite element",
    "fatigue",
    "gd&t",
    "tolerance stack",
    "certif",
    "regulatory",
    "manufactur",
    "thermal",
    "stress analysis",
    "physical testing",
    "supply chain",
    "cost",
    "simulation",
)

# Frozen classifier pins captured on the clean parent (must stay identical after I1 —
# declarations are NOT classifier inputs).
_CLASSIFIER_PINS = [
    ("A gear and pulley hoist with a crankshaft drive", "single", "mechanical"),
    ("ESP32 sensor circuit with WiFi", "single", "electronics_electrical"),
    ("a catheter for veins", "single", "medical_device"),
    ("an app to organize daily schedules", "single", "software"),
    # Mechanical Activation Execution Gate: `mechanical` is now activated —
    # D3-D resolves this tie against the still-not-activated medical_device.
    ("gear and catheter", "single", "mechanical"),
    # Both electronics_electrical and mechanical are now activated -> a real
    # activated-tie (P9-E2 AMBIGUOUS_TIE), no longer a SINGLE electronics win.
    ("circuit and hinge", "ambiguous_tie", None),
    ("nothing recognizable at all", "none", None),
    ("a system of gears and levers", "single", "mechanical"),
]


def _mech():
    with open(_MECH_PATH, encoding="utf-8") as fh:
        return json.load(fh)


def _prov_records():
    with open(_PROV_PATH, encoding="utf-8") as fh:
        return json.load(fh)["records"]


# ---------------------------------------------------------------- declaration presence/shape


def test_coverage_declaration_present_with_electronics_parity_shape():
    cd = _mech().get("coverage_declaration")
    assert isinstance(cd, dict), "mechanical pack lacks coverage_declaration (parent deficiency)"
    assert sorted(cd.keys()) == ["covered_areas", "known_limitations", "not_covered_areas"]
    for key in ("covered_areas", "not_covered_areas", "known_limitations"):
        assert isinstance(cd[key], list) and cd[key]
        assert all(isinstance(x, str) and x.strip() for x in cd[key])


def test_capability_declaration_present_with_shape():
    cap = _mech().get("capability_declaration")
    assert isinstance(cap, dict), "mechanical pack lacks capability_declaration (parent deficiency)"
    for key in (
        "supported_analysis_categories",
        "unsupported_categories",
        "supported_gap_types",
        "evidence_expectations",
        "known_unknowns",
        "provenance_ref",
    ):
        assert key in cap, f"capability_declaration missing {key!r}"


def test_covered_areas_exact_approved_content():
    assert _mech()["coverage_declaration"]["covered_areas"] == _APPROVED_COVERED_AREAS


def test_supported_analysis_categories_exact():
    cap = _mech()["capability_declaration"]
    assert cap["supported_analysis_categories"] == _APPROVED_SUPPORTED_ANALYSIS


def test_supported_gap_types_match_pack_reality():
    data = _mech()
    actual = sorted(g["gap_type_id"] for g in data["gap_type_mappings"])
    assert sorted(data["capability_declaration"]["supported_gap_types"]) == actual


# ---------------------------------------------------------------- OD-M2 clause 1 (both declarations)


def test_od_m2_statement_in_coverage_not_covered():
    joined = " ".join(_mech()["coverage_declaration"]["not_covered_areas"])
    for frag in _ODM2_SUBSTRINGS:
        assert frag in joined, f"OD-M2 clause-1 fragment missing from coverage: {frag!r}"


def test_od_m2_statement_in_capability_unsupported():
    joined = " ".join(_mech()["capability_declaration"]["unsupported_categories"])
    for frag in _ODM2_SUBSTRINGS:
        assert frag in joined, f"OD-M2 clause-1 fragment missing from capability: {frag!r}"


# ---------------------------------------------------------------- mandatory truthfulness content


def test_mandatory_not_covered_concepts_present():
    joined = " ".join(_mech()["coverage_declaration"]["not_covered_areas"]).lower()
    for concept in _MANDATORY_NOT_COVERED_CONCEPTS:
        assert concept in joined, f"mandatory NOT-COVERED concept missing: {concept!r}"


def test_known_limitations_meaningful():
    joined = " ".join(_mech()["coverage_declaration"]["known_limitations"]).lower()
    for frag in (
        "early-concept",
        "parent-level",
        "concept validation",
        "unknown",
        "physical",
        "specialist",
    ):
        assert frag in joined, f"required known-limitation fragment missing: {frag!r}"
    ku = _mech()["capability_declaration"]["known_unknowns"]
    assert isinstance(ku, list) and ku
    assert any("software" in x.lower() or "physical" in x.lower() for x in ku)


def test_no_forbidden_expertise_in_covered_content():
    import re

    cap = _mech()["capability_declaration"]
    covered_text = " ".join(
        _mech()["coverage_declaration"]["covered_areas"]
        + cap["supported_analysis_categories"]
        + cap["evidence_expectations"]
    ).lower()
    for term in _FORBIDDEN_IN_COVERED:
        # Word-boundary match so short terms (e.g. "fea") do not false-positive
        # inside truthful words like "feasibility". The exact-content equality
        # pins above remain the primary anti-paraphrase protection.
        pattern = r"\b" + re.escape(term) + r"\b"
        assert not re.search(pattern, covered_text), (
            f"unsupported expertise claimed in covered content: {term!r}"
        )


# ---------------------------------------------------------------- provenance


def test_declaration_provenance_grounded():
    data = _mech()
    assert data["capability_declaration"]["provenance_ref"] == "mechanical:PR002"
    notes = data["_governance_notes"]
    assert "p9_mech_i1_declarations" in notes
    assert "mechanical:PR002" in notes["p9_mech_i1_declarations"]
    assert "coverage_declaration" in notes["p9_mech_i1_declarations"]
    recs = {r["record_id"]: r for r in _prov_records()}
    assert "mechanical:PR002" in recs, "additive provenance record mechanical:PR002 missing"
    pr2 = recs["mechanical:PR002"]
    assert pr2["pack_id"] == "mechanical"
    assert pr2["source_type"] == "governance_record"
    assert "P9_MECH_I1" in pr2["notes"] or "P9-MECH-I1" in pr2["notes"]
    # The original external-source record is untouched alongside it.
    assert "mechanical:PR001" in recs


# ---------------------------------------------------------------- non-degradation / stability


def test_other_packs_byte_identical():
    for pack, expected in _FROZEN_PACK_SHA256.items():
        path = os.path.join(_DOMAINS, pack, "domain.json")
        with open(path, "rb") as fh:
            digest = hashlib.sha256(fh.read()).hexdigest()
        assert digest == expected, f"{pack} pack changed (forbidden in P9-MECH-I1)"


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


def test_deterministic_repeated_load():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        first = load_registry(_DOMAINS)
        second = load_registry(_DOMAINS)
    assert sorted(first) == sorted(second)
    assert first["mechanical"] == second["mechanical"]
    assert first["mechanical"].get("coverage_declaration") == second["mechanical"].get(
        "coverage_declaration"
    )


def test_mechanical_recognition_identity_unchanged():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        mech = load_registry(_DOMAINS)["mechanical"]
    assert mech["pack_id"] == "mechanical"
    assert mech["aliases"] == ["mechanical"]
    assert mech["display_name"] == "Mechanical"
    assert mech["schema_version"] == "1.0"


class _StubState:
    """Minimal read-only state for the derive seam: mechanical session domain
    with inventor text present. Pre-P9-MECH-SF this file pinned the truthful
    ABSENCE of a governed family (derive == () regardless of the text); the
    family now exists, so the same stub proves governed-present detection."""

    domain = "mechanical"
    domain_signal = "mechanical"
    idea_summary = "the gear housing could crush a finger if the guard fails"
    assertions = ()
    acknowledged_unknowns = ()


def test_safety_family_now_governed_for_mechanical():
    """P9-MECH-SF reconciliation (contract §4 item 1, disclosed): the I1-era
    ``test_safety_family_remains_absent_for_mechanical`` absence pin flipped —
    the governed family exists; the stub's inventor-stated hazard text now
    derives exactly one mechanical-labeled, validation-required signal."""
    assert has_governed_safety_cue_family("mechanical") is True
    signals = derive_inventor_stated_safety_signals(_StubState())
    assert len(signals) == 1
    assert signals[0].domain_context == "mechanical"
    assert signals[0].validation_status == "requires_independent_validation"


def test_activation_state_unchanged():
    assert activated_domains() == ["electronics_electrical", "mechanical"]


def test_classifier_behavior_unchanged_over_pinned_corpus():
    for text, kind, selected in _CLASSIFIER_PINS:
        c = classify_domain(text)
        assert (c.kind.value, c.selected_domain) == (kind, selected), text
