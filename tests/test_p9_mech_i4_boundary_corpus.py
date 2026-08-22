"""P9-MECH-I4 — Terminal Cross-Domain Boundary-Evidence Corpus (P9-MECH-QC §9).

Governed by the AUTHORITATIVE increment contract
``docs/governance/P9_MECH_I4_TERMINAL_BOUNDARY_CORPUS_CONTRACT.md``.

EVIDENCE ONLY — this file changes no runtime behavior; every pin asserts the
UNCHANGED authoritative runtime. Expected labels are never chosen to match the
runtime: each carries a truthfulness rationale grounded in the packs' declared
context ownership and the governed precedence rules, and tie cases are proven
ties-by-construction using the classifier's OWN canonical scoring function
(``_present_signal_count``) — no matching logic is re-implemented here.

TERMINALITY / VALIDITY SCOPE (binding statements):
  * This corpus's validity is tied to the CURRENT frozen Mechanical signal
    inventory (the authoritative P9-MECH-I3 state, anchored below by the
    mechanical pack's byte hash: 18 classification signals incl. the multi-word
    ``locking mechanism``; 15 substance signals).
  * Any FUTURE authorized signal-inventory change invalidates this terminal
    corpus and requires its re-validation at that future gate.
  * Unchanged runtime + unchanged inventory does NOT require rebuilding it.
  * Future authorized engine changes may update the byte pins below under
    their own governed gate — this corpus does NOT permanently freeze the
    classifier architecture; the pins exist so no such change rides along
    UNGOVERNED.
  * Mixed-domain cases are CLASSIFICATION-boundary evidence only: no D4 /
    composition semantics are invoked, simulated, or implied. Mechanical
    remains NOT QUALIFIED.

Reconciliation note (Mechanical Activation Execution Gate): mechanical is now
REALLY activated in production (`activated_domains() ==
['electronics_electrical', 'mechanical']`). Per this file's own terminality
rule ("any future authorized ... change invalidates this terminal corpus"),
the corpus entries whose expected outcome depended on mechanical being
recognized-but-not-activated (D3-D precedence, or an activated-vs-activated
tie against electronics) are updated below to their real current outcome,
each annotated at the point of change; entries independent of activation
state are unchanged. The signal-inventory byte pins and non-activation-
dependent boundary evidence remain otherwise unchanged and still authoritative.
"""

import hashlib
import os
import warnings

from engine.domain_activation import activated_domains, is_activated, support_state
from engine.domain_registry import load_registry
from engine.domain_rules import (
    _REGISTRY,
    _TOKEN_RE,
    _present_signal_count,
    classify_domain,
)
from engine.safety_signal import has_governed_safety_cue_family

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DOMAINS = os.path.join(_REPO, "domains")

# ---------------------------------------------------------------- invariance anchors

# L2SC-01 reconciliation (disclosed; see test_p9_mech_i3_signal_quality.py's
# own reconciliation comment for the full engine-file disclosure).
# P10-DBT1 reconciliation (disclosed; PHASE_9_FORMAL_CLOSURE_RECORD.md §5
# item 1): domain_rules.py re-frozen after a DOCSTRING-ONLY truth repair of
# classify_domain (stale "production-unreachable today" claim; AST proven
# identical modulo docstrings — zero behavior change).
# PVCG-R2-I reconciliation (disclosed; see test_p9_mech_i3_signal_quality.py's
# own reconciliation comment for the full progression_loop disclosure, and
# docs/governance/PVCG_R2_C_GAP_RELEVANCE_HARDENING_CONTRACT.md §2.4/§2.5 for
# the authorization). progression_loop.py re-frozen after the ONE BOUNDED R2
# gap-relevance reconciliation; prior digest preserved as historical evidence:
#   a8e1ffdf9accf3ed57fc6c32d51c7e77ce9e260c0d39a8ec3030e2635ff03dc3
# The boundary corpus and its inventory anchor are unaffected.
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
_FROZEN_ENGINE_SHA256 = {
    "engine/domain_rules.py": "0e47326ad92a6e5b0a63eb06db9e3ad96ae72c9aaf64471dd21621265b1db1ab",
    "engine/progression_loop.py": "c268cd6380129170da19f3ba03158eebd9a5480711b43e39280e8ce9e74f63f8",
}
# The mechanical pack hash IS this corpus's inventory validity anchor.
# P9-MECH-SF reconciliation (contract §4 item 10, disclosed): re-frozen after
# the mandatory declaration truthfulness cascade under the corpus's OWN
# validity terms — the classification/substance SIGNAL INVENTORY is proven
# byte-unchanged (canonical hashes 860ce084…/c14ae2d5… pinned in
# tests/test_p9_mech_safety_cue_family.py::test_signal_inventory_unchanged_proof
# and re-checked by the I2 frozen-field pins), so the corpus stays valid and
# NO corpus rebuild was required or performed. Declaration bytes are the only
# pack change.
# L2SC-01 reconciliation (disclosed; docs/governance/L2SC01_SUBSTANCE_SIGNAL_
# PLURAL_ALIAS_INCREMENT_CONTRACT.md §10): mechanical re-frozen after adding
# the authorized, additive-only `substance_signal_plural_aliases` field (3
# pairs: piston/valve/actuator). classification_signals/substance_signals
# content is byte-unchanged (same signal-inventory proof cited above, which
# this reconciliation does not disturb); electronics_electrical re-frozen for
# the same reason as I1.
_FROZEN_PACK_SHA256 = {
    "mechanical": "901dd7188ddefda9cbe69a835cc64959c1d55debfe61b262d720abd904069e79",
    "electronics_electrical": "53f431e38a70c2b621e19afb7323ad9bc4732c6c4151ea6b8c46a3214f098dfb",
    "medical_device": "6070cf9281a7a376780175e7e1d3879be598384bcaf4dc370e56f7bf613e3ade",
    "software": "1c9cefa14641c079ddb5c21c59f398866adf43561101743b67e611936a67e3a7",
    "iot_electronics": "f04c825ad25dea0c6db2ee310649fe377329f30c5461f2756019104013e53406",
}


def _scores(text):
    """Per-pack present-signal counts via the classifier's OWN scoring function."""
    tokens = _TOKEN_RE.findall(text.lower())
    token_set = set(tokens)
    return {
        pack_id: count
        for pack_id, pack in _REGISTRY.items()
        if (count := _present_signal_count(pack, tokens, token_set))
    }


def _outcome(text):
    c = classify_domain(text)
    return (c.kind.value, c.selected_domain)


# ================================================================ corpus classes
# Every case: (text, expected_kind, expected_selected). Rationales are grounded in
# the packs' declared context ownership + the governed precedence rules; cases
# marked RESIDUAL/LIMITATION pin documented I3 residuals honestly — they are
# recorded limitations, NOT endorsements.

# Class 1 — positive representative Mechanical journeys (declared concept-level scope).
_CLASS_POSITIVE = [
    ("A gear and pulley hoist with a crankshaft drive", "single", "mechanical"),
    ("a spring loaded clamp with a torque limiter", "single", "mechanical"),
    ("a gearbox with a shaft and bearing assembly", "single", "mechanical"),
    ("A hinge mounted bracket with a lever and a small switch", "single", "mechanical"),
]

# Class 2 — multi-word `locking mechanism` + bounded final-token plural (I3 replacement signal).
_CLASS_LOCKING_MECHANISM = [
    ("a locking mechanism for gates", "single", "mechanical"),
    ("locking mechanisms for sliding gates", "single", "mechanical"),
    ("a door locking mechanism with a spring latch", "single", "mechanical"),
    # narrowing holds: software locking prose no longer attracts mechanical
    ("optimistic locking strategy for the api", "single", "software"),
]

# Class 3 — Mechanical vs Electronics hard cases.
_CLASS_VS_ELECTRONICS = [
    ("ESP32 sensor circuit with WiFi", "single", "electronics_electrical"),
    ("a resistor and a capacitor on a circuit board", "single", "electronics_electrical"),
    # Mechanical Activation Execution Gate: both electronics_electrical and
    # mechanical are now activated -> a real activated-tie (AMBIGUOUS_TIE),
    # not a SINGLE electronics precedence win.
    ("a linear actuator with a servo circuit", "ambiguous_tie", None),
    ("a purely mechanical hand crank winch with a pulley", "single", "mechanical"),
]

# Class 4 — Mechanical vs Software hard cases (I3-corrected classes at corrected outcomes).
_CLASS_VS_SOFTWARE = [
    ("a voting mechanism for the app", "single", "software"),
    ("a delivery mechanism for software updates", "single", "software"),
    ("row locking in the database engine", "single", "software"),
    ("a software workflow for gear inventory management", "single", "software"),  # software 2 > mech 1
]

# Class 5 — Mechanical vs Medical hard cases (medical context ownership + precedence).
_CLASS_VS_MEDICAL = [
    ("an artificial heart valve implant", "single", "medical_device"),  # not a tie; unaffected by activation
    # Mechanical Activation Execution Gate: mechanical is now activated;
    # D3-D resolves this real (non-tie) score difference to mechanical.
    ("a replacement heart valve", "single", "mechanical"),
    ("a valve that regulates water flow in pipes", "single", "mechanical"),
]

# Class 6 — EXPLICIT tie cases, proven ties-by-construction (score parity asserted).
#   (text, expected outcome, exact expected score map)
_CLASS_TIES = [
    # legacy zero-activated precedence: mechanical > software
    ("a pulley and a database", ("single", "mechanical"), {"mechanical": 1, "software": 1}),
    ("a lever and an app", ("single", "mechanical"), {"mechanical": 1, "software": 1}),
    # Mechanical Activation Execution Gate: mechanical is now activated -> D3-D
    # (the ACTIVATED domain wins the tie), not legacy medical_device precedence.
    ("gear and catheter", ("single", "mechanical"), {"mechanical": 1, "medical_device": 1}),
    # BOTH domains are now activated -> a real activated-tie (AMBIGUOUS_TIE),
    # not a D3-D single-activated-domain win.
    ("circuit and hinge", ("ambiguous_tie", None),
     {"electronics_electrical": 1, "mechanical": 1}),
    # THREE-WAY: mechanical is the sole ACTIVATED candidate among the tie -> D3-D.
    ("gear and catheter and app", ("single", "mechanical"),
     {"mechanical": 1, "medical_device": 1, "software": 1}),
]

# Class 7 — mixed-domain cases (CLASSIFICATION boundaries only; no D4 semantics).
_CLASS_MIXED = [
    # medical outscores the mechanical+electronics components (sole top, not a tie)
    ("an implantable pump with a piston and a control circuit", "single", "medical_device"),
    ("a system of gears and levers", "single", "mechanical"),  # mech 2 > software 1 ('system')
]

# Class 8 — NONE / unknown / generic ambiguity / empty input.
_CLASS_NONE = [
    ("", "none", None),
    ("   ", "none", None),
    ("nothing recognizable at all", "none", None),
    ("a better way to organize my day", "none", None),
    ("an improvement to everyday life", "none", None),
    ("engineering excellence in general", "none", None),
]

# Class 9 — documented I3 residuals, pinned honestly AS residuals (recorded limitations).
_CLASS_RESIDUALS = [
    # RESIDUAL (I3 disposition record): retained 'bracket' still attracts software
    # tournament prose via the legacy 1-1 tie — documented limitation, not endorsement.
    ("tournament bracket seeding for the app", "single", "mechanical"),
    # RESIDUAL (I3 recall trade-off): bare-'mechanism' ideas classify NONE after the
    # generic signal's removal — documented limitation.
    ("a mechanism that folds chairs flat", "none", None),
]

# Class 10 — adversarial synonyms / recall boundaries (limitations labeled as such).
_CLASS_RECALL_BOUNDARY = [
    # LIMITATION: genuine mechanical concepts phrased outside the frozen inventory
    # truthfully classify NONE today (honest recall boundary of the vocabulary).
    ("a contraption of cogs and sprockets", "none", None),
    ("a rotating cam follower assembly", "none", None),
    ("a widget that spins and folds", "none", None),
]

# Class 11 — the corrected EIGHT-text legacy classifier corpus, verbatim.
_CLASS_LEGACY_8 = [
    ("A gear and pulley hoist with a crankshaft drive", "single", "mechanical"),
    ("ESP32 sensor circuit with WiFi", "single", "electronics_electrical"),
    ("a catheter for veins", "single", "medical_device"),
    ("an app to organize daily schedules", "single", "software"),
    # Mechanical Activation Execution Gate: `mechanical` is now activated —
    # D3-D resolves this tie against the still-not-activated medical_device.
    ("gear and catheter", "single", "mechanical"),
    # Both electronics_electrical and mechanical are now activated -> a real
    # activated-tie (AMBIGUOUS_TIE), no longer a SINGLE electronics win.
    ("circuit and hinge", "ambiguous_tie", None),
    ("nothing recognizable at all", "none", None),
    ("a system of gears and levers", "single", "mechanical"),
]

# Class 12 — sibling-domain non-degradation corpus.
_CLASS_SIBLINGS = [
    ("ESP32 sensor circuit with WiFi", "single", "electronics_electrical"),
    ("a resistor and a capacitor on a circuit board", "single", "electronics_electrical"),
    ("an app to organize daily schedules", "single", "software"),
    ("a sql database backend with an api", "single", "software"),
    ("a catheter for veins", "single", "medical_device"),
    ("an implantable stent for cardiac patients", "single", "medical_device"),
]

_ALL_SIMPLE_CLASSES = {
    "positive": _CLASS_POSITIVE,
    "locking_mechanism": _CLASS_LOCKING_MECHANISM,
    "vs_electronics": _CLASS_VS_ELECTRONICS,
    "vs_software": _CLASS_VS_SOFTWARE,
    "vs_medical": _CLASS_VS_MEDICAL,
    "mixed": _CLASS_MIXED,
    "none_unknown": _CLASS_NONE,
    "residuals": _CLASS_RESIDUALS,
    "recall_boundary": _CLASS_RECALL_BOUNDARY,
    "legacy_8": _CLASS_LEGACY_8,
    "siblings": _CLASS_SIBLINGS,
}


# ---------------------------------------------------------------- class-coverage completeness


def test_corpus_class_inventory_complete():
    # m5 guard: deleting any corpus class flips this pin.
    assert sorted(_ALL_SIMPLE_CLASSES) == [
        "legacy_8", "locking_mechanism", "mixed", "none_unknown", "positive",
        "recall_boundary", "residuals", "siblings", "vs_electronics",
        "vs_medical", "vs_software",
    ]
    assert all(cases for cases in _ALL_SIMPLE_CLASSES.values())
    assert len(_CLASS_LEGACY_8) == 8  # corrected count — exactly eight, verbatim
    assert len(_CLASS_TIES) == 5 and any(len(s) == 3 for _, _, s in _CLASS_TIES)


# ---------------------------------------------------------------- corpus outcome pins


def test_positive_mechanical_journeys():
    for text, kind, selected in _CLASS_POSITIVE:
        assert _outcome(text) == (kind, selected), text


def test_locking_mechanism_and_bounded_plural():
    for text, kind, selected in _CLASS_LOCKING_MECHANISM:
        assert _outcome(text) == (kind, selected), text


def test_mechanical_vs_electronics():
    for text, kind, selected in _CLASS_VS_ELECTRONICS:
        assert _outcome(text) == (kind, selected), text


def test_mechanical_vs_software():
    for text, kind, selected in _CLASS_VS_SOFTWARE:
        assert _outcome(text) == (kind, selected), text
    # honest-precondition: the gear-inventory case is NOT a tie — software outscores.
    assert _scores("a software workflow for gear inventory management") == {
        "software": 2, "mechanical": 1,
    }


def test_mechanical_vs_medical():
    for text, kind, selected in _CLASS_VS_MEDICAL:
        assert _outcome(text) == (kind, selected), text


def test_explicit_ties_proven_by_score_parity():
    # m6 guard: each tie case asserts the EXACT engine-computed score map, so a
    # weakened (non-parity) text fails its precondition rather than passing
    # for the wrong reason.
    for text, expected_outcome, expected_scores in _CLASS_TIES:
        assert _scores(text) == expected_scores, f"tie precondition broken: {text!r}"
        assert _outcome(text) == expected_outcome, text


def test_three_way_tie_resolved_by_activation_now_not_legacy_precedence():
    # Mechanical Activation Execution Gate: mechanical is now the sole
    # ACTIVATED candidate among this three-way score tie, so D3-D resolves it
    # directly — the legacy zero-activated precedence path (medical_device >
    # electronics > mechanical > software) is no longer exercised by this
    # input at all.
    text = "gear and catheter and app"
    assert _scores(text) == {"mechanical": 1, "medical_device": 1, "software": 1}
    assert _outcome(text) == ("single", "mechanical")


def test_mixed_domain_classification_only():
    for text, kind, selected in _CLASS_MIXED:
        assert _outcome(text) == (kind, selected), text
    # honest-precondition: the implantable-pump case is a sole-top medical win, not a tie.
    assert _scores("an implantable pump with a piston and a control circuit") == {
        "medical_device": 2, "mechanical": 1, "electronics_electrical": 1,
    }


def test_none_unknown_generic_and_empty():
    for text, kind, selected in _CLASS_NONE:
        assert _outcome(text) == (kind, selected), repr(text)


def test_documented_residuals_pinned_as_residuals():
    for text, kind, selected in _CLASS_RESIDUALS:
        assert _outcome(text) == (kind, selected), text
    # residual precondition: the tournament case IS the documented 1-1 legacy tie.
    assert _scores("tournament bracket seeding for the app") == {
        "mechanical": 1, "software": 1,
    }


def test_recall_boundaries_labeled_as_limitations():
    for text, kind, selected in _CLASS_RECALL_BOUNDARY:
        assert _outcome(text) == (kind, selected), text
        assert _scores(text) == {}, f"recall-boundary case unexpectedly matched: {text!r}"


def test_legacy_eight_text_corpus_verbatim():
    for text, kind, selected in _CLASS_LEGACY_8:
        assert _outcome(text) == (kind, selected), text


def test_sibling_domain_non_degradation():
    for text, kind, selected in _CLASS_SIBLINGS:
        assert _outcome(text) == (kind, selected), text


# ---------------------------------------------------------------- invariance pins


def test_engine_files_byte_frozen():
    for path, expected in _FROZEN_ENGINE_SHA256.items():
        with open(os.path.join(_REPO, path), "rb") as fh:
            digest = hashlib.sha256(fh.read()).hexdigest()
        assert digest == expected, f"engine file changed outside a governed gate: {path}"


def test_pack_bytes_frozen_inventory_validity_anchor():
    # The mechanical hash is the corpus's inventory validity anchor (I3 state);
    # sibling hashes protect non-degradation; iot stays D8-reserved.
    for pack, expected in _FROZEN_PACK_SHA256.items():
        with open(os.path.join(_DOMAINS, pack, "domain.json"), "rb") as fh:
            digest = hashlib.sha256(fh.read()).hexdigest()
        assert digest == expected, f"{pack} pack changed — corpus validity requires re-validation"


def test_recognized_set_and_activation_state():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        registry = load_registry(_DOMAINS)
    assert sorted(registry) == [
        "electronics_electrical", "mechanical", "medical_device", "software",
    ]
    assert activated_domains() == ["electronics_electrical", "mechanical"]


def test_recognition_is_not_activation():
    # Classification identity confers NO activation by itself: medical_device
    # classifies (class 5) yet remains recognized-not-activated. Mechanical is
    # now really activated via the separate, explicit Mechanical Activation
    # Execution Gate — not because it classifies — so mechanical classifying
    # (class 1) is shown alongside its (now true) activation, not as a
    # counter-example.
    assert _outcome("A gear and pulley hoist with a crankshaft drive") == ("single", "mechanical")
    assert is_activated("mechanical") is True
    assert _outcome("a catheter for veins") == ("single", "medical_device")
    assert support_state("medical_device") == "recognized_not_activated"
    assert is_activated("medical_device") is False
    assert is_activated("electronics_electrical") is True


def test_mechanical_safety_family_now_governed():
    """P9-MECH-SF reconciliation (contract §4 item 4, disclosed): the I4-era
    absence pin flipped — the governed Mechanical safety-cue family exists
    (evidence: tests/test_p9_mech_safety_cue_family.py)."""
    assert has_governed_safety_cue_family("mechanical") is True


def test_deterministic_repeated_classification():
    for text in ("a pulley and a database", "gear and catheter and app", ""):
        assert _outcome(text) == _outcome(text)
