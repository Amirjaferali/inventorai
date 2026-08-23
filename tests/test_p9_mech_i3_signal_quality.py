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
# L2SC-01 reconciliation (disclosed; docs/governance/L2SC01_SUBSTANCE_SIGNAL_
# PLURAL_ALIAS_INCREMENT_CONTRACT.md §10): domain_rules.py gained
# `get_substance_signal_plural_aliases`; progression_loop.py's Layer-2 gate now
# consumes the domain-owned plural-alias map instead of a hardcoded dict — no
# classifier/tie/admission semantics changed; the substance-signal lookup and
# causal-connective dispatch logic are otherwise byte-for-byte unchanged.
# P10-DBT1 reconciliation (disclosed; PHASE_9_FORMAL_CLOSURE_RECORD.md §5
# item 1): domain_rules.py re-frozen after a DOCSTRING-ONLY truth repair of
# classify_domain (stale "production-unreachable today" claim; AST proven
# identical modulo docstrings — zero behavior change).
# PVCG-R2-I reconciliation (disclosed; docs/governance/PVCG_R2_C_GAP_RELEVANCE_
# HARDENING_CONTRACT.md §2.4/§2.5, AUTHORITATIVE via PR #548 merge 4d746d15):
# progression_loop.py re-frozen after the ONE BOUNDED R2 reconciliation the
# contract authorizes. The only change is the gap-relevance eligibility seam
# inside integrate_response — the engine.gap_relevance import, one
# `addresses_gap(response, gap_type)` call, three side effects (known_mechanism,
# known_problem, Stage-3 evidence capture) now conditioned on it, and one
# fail-closed WARN return. No classifier, tie, substance-semantics, quality,
# gap-priority, question, maturity or stall behaviour changed, and nothing else
# in the file was touched. Historical digests preserved as evidence:
#   pre-L2SC-01  progression_loop.py = bbb49b49… (see the L2SC-01 note above)
#   pre-R2-I     progression_loop.py =
#       a8e1ffdf9accf3ed57fc6c32d51c7e77ce9e260c0d39a8ec3030e2635ff03dc3
# This authorization is ONE bounded reconciliation, NOT a general permission to
# edit engine/progression_loop.py; the guard below is unchanged and still
# enforced against the new expected value.
# PVCG-R3-I RECONCILIATION (owner-authorized, bounded — the SECOND and only
# other reconciliation of this pin). Authority: PVCG_R3_C_SEMANTIC_STABILITY_
# CONTRACT.md §13.1/§13.2/§13.2a (AUTHORITATIVE, PR #551, merge 7b7aa2f1…),
# which permits EXACTLY ONE engine pin to move and names this file as one of
# the three ENFORCING locations that must be updated together in the same
# candidate. Why the pin had to move: closing D-2 — an Arabic-only inventor can
# never close a gap because assess_response returns ASSERTED unconditionally
# for Arabic — is impossible from engine/gap_relevance.py, because the ASSERTED
# ceiling is produced by _has_causal_structure / the substance check INSIDE this
# pinned file. RED was established at the authoritative base BEFORE the pin was
# touched, and demonstrated the §7.1 material divergence, not merely a digest
# mismatch. Scope of the edit: one import, the Arabic branch of
# _has_causal_structure, the Arabic branch of the substance check, the Arabic
# branch of _detect_acknowledged_unknown, and one bounded fragment helper.
# Question selection, gap priority, scoring thresholds, maturity, stall
# behaviour and the six governed gap types are untouched.
#   pre-R3-I     progression_loop.py =
#       07c9bff500662de54ac0f7388c1f2e13a721549c6f4943cde865b98a22c525d6
# PVCG-R4-I pin reconciliation (PVCG_R4_C_USER_CORRECTION_AND_DETERMINISTIC_
# INVALIDATION_CONTRACT.md §16.2, performed exactly under the R3-C §13.2a
# mechanism the R4 contract adopts by reference). The R4 contract DISCLOSED this
# movement in advance rather than leaving it to be discovered at review: the
# §10.4 G-1 CLOSED-gap safety guard lands in this pinned file.
# Scope of the edit: ONE guard in `integrate_response` — an already-CLOSED gap
# returns unchanged instead of falling through to the PARTIAL branch, which
# previously left `status=PARTIAL` with `closed_at` still set (an impossible
# mixed state). RED was established at the authoritative base BEFORE the pin was
# touched and demonstrated that impossible state reachable, not merely a digest
# mismatch. Question selection, gap priority, scoring thresholds, maturity,
# stall behaviour, the six governed gap types, and the ordinary forward-only
# journey (WPS-001 INV-004) are untouched; no CLOSED gap can reopen through the
# normal answer path.
#   pre-R4-I     progression_loop.py =
#       3cbd76849c0f572191a552db1a41a8cd418d02fac1d59d9b8804c72883239a55
# Wave-1 remediation pin reconciliation (WAVE_1_REMEDIATION_IMPLEMENTATION_
# CONTRACTS.md, Owner-authorized RVR-1/RVR-2/RVR-3; same §13.2a mechanism as
# the R3-I and R4-I reconciliations above). The Wave-1 contract moves this
# pinned file in three disclosed, bounded steps: RVR-1 adds the canonical
# `accept_gap_risk` lifecycle writer and the ACCEPTED_RISK completion
# semantics; RVR-2 bounds the exhausted-question reframe; RVR-3 adds the
# deterministic Layer-3 structured-substance REASONED path. Question identity,
# gap priority, the six governed gap types, Arabic branches, and the ordinary
# forward-only journey are untouched; the pin below records the digest at the
# latest completed Wave-1 step.
#   pre-Wave-1   progression_loop.py =
#       c268cd6380129170da19f3ba03158eebd9a5480711b43e39280e8ce9e74f63f8
_FROZEN_ENGINE_SHA256 = {
    "engine/domain_rules.py": "0e47326ad92a6e5b0a63eb06db9e3ad96ae72c9aaf64471dd21621265b1db1ab",
    "engine/progression_loop.py": "4ba9ceec80b7924d2d153e2274cccab41b2630d70b321b9608fff0bd1281b026",
}
# Other-pack byte freeze (unchanged lineage from I1/I2). L2SC-01 reconciliation
# (disclosed; electronics_electrical re-frozen, see I1's own comment).
_FROZEN_PACK_SHA256 = {
    "electronics_electrical": "53f431e38a70c2b621e19afb7323ad9bc4732c6c4151ea6b8c46a3214f098dfb",
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
    # Mechanical Activation Execution Gate: `mechanical` is now activated —
    # D3-D resolves this tie against the still-not-activated medical_device.
    ("gear and catheter", "single", "mechanical"),
    # Both electronics_electrical and mechanical are now activated -> a real
    # activated-tie (P9-E2 AMBIGUOUS_TIE), no longer a SINGLE electronics win.
    ("circuit and hinge", "ambiguous_tie", None),
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
    # Mechanical Activation Execution Gate: `mechanical` is now activated, so
    # entries that previously won by precedence-over-a-non-activated-mechanical
    # now reflect real D3-D/tie outcomes with mechanical genuinely in the mix.
    ("an artificial heart valve implant", "single", "medical_device"),  # not a tie; unaffected
    ("a replacement heart valve", "single", "mechanical"),
    ("a linear actuator with a servo circuit", "ambiguous_tie", None),
    # EXPLICIT tie cases preserved (OD2 legacy precedence rule untouched):
    ("a pulley and a database", "single", "mechanical"),
    ("a lever and an app", "single", "mechanical"),
    ("gear and catheter", "single", "mechanical"),
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
    assert activated_domains() == ["electronics_electrical", "mechanical"]


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
