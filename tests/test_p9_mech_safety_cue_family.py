"""P9-MECH-SF — Governed Mechanical Safety-Cue Family evidence (OD-M2 clause 3).

Governed by the AUTHORITATIVE corrected contract
``docs/governance/P9_MECH_SAFETY_CUE_FAMILY_CONTRACT.md`` (merge ``d1b79ef4``;
D-P9-MECH-02 / OD-M2 clause 3: the family MUST be complete, merged, and
post-merge verified BEFORE any Owner activation authorization for
``mechanical``).

This file is the focused evidence for the ONE bounded implementation increment:

* the additive ``mechanical`` entry in the F001 ``_DOMAIN_CUE_FAMILIES`` seam
  (exact electronics-precedent shape; NEW provenance-tagged hazard vocabulary
  authored under contract §3's objective criteria; provenance mechanical:PR005);
* the SAME-increment declaration truthfulness cascade in
  ``domains/mechanical/domain.json`` (detection-scoped covered statement;
  "safety determination" stays NOT COVERED);
* the signal-inventory-unchanged proof that re-froze the I4/I5 pack-hash
  validity anchors WITHOUT any corpus rebuild (declarations are not signals).

Detection semantics are the unchanged F001 semantics: cues mark
inventor-STATED safety-relevant statements for required-independent-validation
labeling — NEVER a safety determination, certification, or compliance
conclusion. At the time of this gate, Mechanical was NOT ACTIVATED and admission
was untouched; Mechanical was subsequently activated by a later governed Phase-9
gate (see docs/governance/PHASE_9_FORMAL_CLOSURE_RECORD.md). The detection
semantics recorded here are unchanged by that activation.
"""

import hashlib
import json
import os

from engine.domain_activation import activated_domains, is_activated, support_state
from engine.idea_state import IdeaState
from engine.deliverable_assembler import assemble_deliverable
from engine import safety_signal as ss
from engine.safety_signal import (
    derive_inventor_stated_safety_signals,
    has_governed_safety_cue_family,
)

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DOMAINS = os.path.join(_REPO, "domains")
_MECH_PATH = os.path.join(_DOMAINS, "mechanical", "domain.json")
_PROV_PATH = os.path.join(_DOMAINS, "domain_provenance.json")

ELEC = "electronics_electrical"
MECH = "mechanical"

# --- Exact authored vocabulary (contract §3(5): equality pins are the primary
# anti-drift / anti-stuffing protection — any addition, removal, or rewording
# of the governed family is RED here first).
_PINNED_FAILURE = (
    "should not be used", "must not be used", "do not use",
    "cannot be safely", "can not be safely", "not be safely",
    "if it fails", "if this fails", "fails to", "fail to", "failed to",
    "failure to", "malfunction", "does not work",
    "jams", "jammed", "seizes", "seized", "binds up",
    "comes loose", "come loose", "came loose",
    "breaks", "breaks off", "broke", "snaps", "snapped",
    "shatters", "shattered", "cracks", "cracked",
    "wears out", "worn out", "gives way", "gave way",
    "slips", "slipped", "detaches", "detached",
    "tips over", "tipped over", "collapses", "collapsed",
    "flies off", "fly off", "flew off",
    "guard fails", "brake fails", "latch fails", "lock fails", "catch fails",
    "guard is removed", "guard is missing", "without the guard",
)
_PINNED_SUBJECT = (
    "pinch point", "pinch points", "nip point", "nip points",
    "crush point", "crush points", "crush zone",
    "moving part", "moving parts", "rotating part", "rotating parts",
    "spinning parts", "spinning blade", "rotating blade",
    "blade", "blades", "cutter", "cutting edge", "sharp edge", "sharp edges",
    "shear point", "shear points",
    "entanglement", "entanglement point",
    "stored energy", "spring under tension", "compressed spring",
    "loaded spring", "spring tension",
    "high pressure", "pressurized", "pressurised",
    "heavy load", "suspended load", "falling object", "falling objects",
    "flying debris", "ejected part", "ejected parts", "projectile",
    "counterweight",
    "guard", "safety guard", "machine guard",
)
_PINNED_CONSEQUENCE = (
    "injury", "injuries", "injure", "injured",
    "harm", "amputation", "amputate", "amputated",
    "laceration", "lacerations",
    "crush a finger", "crush fingers", "crush a hand", "crush someone",
    "crushed", "crushing injury",
    "lose a finger", "losing a finger", "lose fingers",
    "broken bone", "broken bones", "fractured",
    "caught in", "get caught", "trapped", "trap a hand", "trap fingers",
    "entangled", "struck by", "strike someone", "hit someone",
    "fall on someone", "falls on someone", "land on someone",
    "unsafe", "safety risk", "create a risk", "creates a risk",
    "danger", "dangerous",
    "puncture", "impale", "impaled", "severed", "sever a",
)
_PINNED_CONTEXT = (
    "gear", "gears", "gearbox", "lever", "pulley", "spring", "shaft",
    "bearing", "linkage", "mechanism", "hinge", "clamp", "crank",
    "flywheel", "conveyor", "roller", "piston", "clutch",
    "chain drive", "belt drive", "cam", "ratchet", "winch",
)

# --- Electronics IDENTITY vocabulary (collision guard basis, contract §3(6)):
# the electronics context terms plus the distinctly-electrical subject /
# consequence cues. Generic safety English ("harm", "injury", "danger",
# "fails to", …) is NOT electronics identity and MAY appear in both families;
# the terms below may appear in NEITHER mechanical cue class.
_ELEC_IDENTITY = (
    # electronics context terms (byte-pinned electronics family content)
    "insulation", "voltage", "current", "plug", "circuit", "wire", "battery",
    "mains", "electric", "electrical", "electronic", "overcurrent",
    "overvoltage", "relay", "sensor", "microcontroller", "capacitor",
    "resistor", "power", "fuse", "breaker",
    # distinctly electrical subjects/consequences
    "electric shock", "electrical shock", "shock", "short circuit",
    "short-circuit", "high voltage", "live wire", "electrocute",
    "electrocuted", "electrocution", "spark", "thermal runaway",
    "overheat", "overheating", "excessive heat", "catch fire", "cause a fire",
    "shock the user", "burn",
)

# --- Frozen electronics family (m3 guard): canonical sha256 over the family
# dict with tuples listed — captured at this increment's parent and required
# identical forever after (the electronics vocabulary is byte-preserved).
_ELEC_FAMILY_SHA256 = (
    "1cc29b7924f92212ed5ebe3081fd1d1c60c4eac288807b941f7c66df5fa0fdde")

# --- Signal-inventory-unchanged proof (contract §4 items 10-11): the canonical
# hashes of the ONLY two signal inventories, identical to their I2/I3-era pins.
# This is the ONE explicit proof on which BOTH the I4 and the I5 mechanical
# full-pack hash anchors were re-frozen without any corpus rebuild
# (declaration bytes changed; signal bytes did not).
_FROZEN_SIGNAL_INVENTORY = {
    "classification_signals": (
        "860ce084389c842e3dc2b5771651bb145579cc19a6c53f303f198ea8419c498e"),
    "substance_signals": (
        "c14ae2d504479d191f91a16c960d065400479b4ce6238757fb5ab4cb1b094ac5"),
}
_FROZEN_NON_DECLARATION_FIELDS = {
    "gap_type_mappings": (
        "857820ed6be7a25fa9200756b4453487b87144b45fc2fafb9fcd53158ef2e7f2"),
    "aliases": (
        "bc7f35e42f32845fad8c2d2e0c5c3ed39a84e54673f351eb581e9d8b38368bd2"),
    "journey_extension": (
        "85473dc88684f165cc080218237b0e76573bc1b80ea7cfa77cb76b78c0f28bcc"),
}

# --- The exact truthful declaration cascade content (equality pins).
_SAFETY_BOUNDARY_STATEMENT = (
    "Safety determination of any kind is NOT COVERED: the governed Mechanical "
    "safety-cue family (mechanical:PR005) provides inventor-stated "
    "safety-signal DETECTION only; every detected signal requires independent "
    "validation and is never a determination that the idea is safe or unsafe"
)
_COVERED_DETECTION_ENTRY = (
    "Detection of inventor-stated mechanical safety signals via the governed "
    "Mechanical safety-cue family: flags safety-relevant failure statements "
    "the inventor has already made (e.g. crush, pinch, entanglement, "
    "stored-energy release, part ejection) for required independent "
    "validation — detection only, never a safety determination"
)
_SUPPORTED_DETECTION_CATEGORY = "inventor_stated_safety_signal_detection"

# Texts that must NOT fire for a mechanical session (the contract's
# vocabulary-conditional pins, asserted here affirmatively as standing
# collision guards: electronics hazard texts, the D3-A trigger, and the F001
# cold-load / r1 example texts).
_MUST_NOT_FIRE = (
    "If the alarm fails to warn people, the fire hazard could cause harm to "
    "anyone nearby.",
    "If the sensor fails to detect overcurrent, it could cause a fire.",
    "The battery insulation may malfunction and cause harm.",
    "a hinge idea",
    "A folding ladder hinge idea",
    "",
    "plain words",
    "The gearbox uses a planetary gear set.",
)


def _state(domain, text):
    st = IdeaState(idea_id="p9-mech-sf-test")
    if domain is not None:
        st.domain = domain
        st.domain_signal = domain
    st.idea_summary = text
    return st


def _signals_block(state):
    return assemble_deliverable(state)["_session_meta"][
        "inventor_stated_safety_signals"]


def _mech_pack():
    with open(_MECH_PATH, encoding="utf-8") as fh:
        return json.load(fh)


def _canon_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def _family():
    return ss._DOMAIN_CUE_FAMILIES[MECH]


def _all_mech_cues():
    fam = _family()
    return tuple(fam["failure"]) + tuple(fam["subject"]) + \
        tuple(fam["consequence"]) + tuple(fam["context_terms"])


# ---------------------------------------------------------------- family presence


def test_family_now_governed_for_mechanical():
    assert has_governed_safety_cue_family(MECH) is True
    assert has_governed_safety_cue_family(ELEC) is True
    assert has_governed_safety_cue_family(None) is True   # governed legacy default


def test_fail_safe_domains_still_family_less():
    for d in ("software", "medical_device", "unknown_future_domain"):
        assert has_governed_safety_cue_family(d) is False
        st = _state(d, "If the guard comes loose, fingers could be caught in "
                       "the rotating parts and crushed.")
        assert derive_inventor_stated_safety_signals(st) == ()
        assert _signals_block(st).get("capability_scope") == \
            "no_governed_safety_cue_family"


# ---------------------------------------------------------------- family shape / vocabulary


def test_family_shape_mirrors_electronics_precedent():
    fam = _family()
    assert sorted(fam.keys()) == sorted(
        ss._DOMAIN_CUE_FAMILIES[ELEC].keys())
    assert sorted(fam.keys()) == [
        "consequence", "context_terms", "failure", "owner", "subject"]
    assert fam["owner"] == MECH
    for key in ("failure", "subject", "consequence", "context_terms"):
        cues = fam[key]
        assert isinstance(cues, tuple) and cues, key
        for cue in cues:
            assert isinstance(cue, str) and cue.strip(), (key, cue)
            assert cue == cue.lower(), (key, cue)   # token-anchored lowercase


def test_vocabulary_equality_pinned():
    fam = _family()
    assert fam["failure"] == _PINNED_FAILURE
    assert fam["subject"] == _PINNED_SUBJECT
    assert fam["consequence"] == _PINNED_CONSEQUENCE
    assert fam["context_terms"] == _PINNED_CONTEXT


def test_no_electronics_identity_collision():
    """Contract §3(6): no electronics identity term appears — as a whole word —
    inside ANY mechanical cue, and the subject/context classes are fully
    disjoint from the electronics family's."""
    import re
    for cue in _all_mech_cues():
        for term in _ELEC_IDENTITY:
            assert not re.search(r"(?<![a-z0-9])" + re.escape(term) +
                                 r"(?![a-z0-9])", cue), (cue, term)
    elec = ss._DOMAIN_CUE_FAMILIES[ELEC]
    fam = _family()
    assert not set(fam["subject"]) & set(elec["subject"])
    assert not set(fam["context_terms"]) & set(elec["context_terms"])


def test_no_thermal_claim_in_family_or_declarations():
    """THERM-01 boundary: no thermal vocabulary anywhere in the family, and no
    thermal/certification/simulation claim enters the covered declarations
    (the I1 forbidden-covered lexicon guard is re-asserted there)."""
    for cue in _all_mech_cues():
        assert "thermal" not in cue and "overheat" not in cue, cue
    covered = " ".join(
        _mech_pack()["coverage_declaration"]["covered_areas"]).lower()
    for banned in ("thermal", "certif", "simulation", "tolerance stack"):
        assert banned not in covered, banned


# ---------------------------------------------------------------- derivation GREEN


def test_green_same_sentence_derivation():
    st = _state(MECH, "If the guard comes loose, fingers could be caught in "
                      "the rotating parts and crushed.")
    signals = derive_inventor_stated_safety_signals(st)
    assert len(signals) == 1
    sig = signals[0]
    assert sig.provenance == ss.PROVENANCE_INVENTOR_STATED
    assert sig.validation_status == ss.VALIDATION_REQUIRES_INDEPENDENT
    assert sig.domain_context == MECH
    assert sig.safety_subject == "rotating parts"
    assert sig.failure_condition == "comes loose"
    assert sig.possible_consequence == "crushed"
    assert "not a determination" in sig.caution_text
    assert "requires independent validation" in sig.caution_text


def test_green_adjacent_pair_derivation():
    st = _state(MECH, "If the latch gives way, the spring under tension is "
                      "released. Someone nearby could suffer a serious injury.")
    signals = derive_inventor_stated_safety_signals(st)
    assert len(signals) == 1
    assert signals[0].safety_subject == "spring under tension"
    assert signals[0].failure_condition == "gives way"
    assert signals[0].possible_consequence == "injury"
    assert signals[0].domain_context == MECH


def test_green_never_electronics_labeled():
    texts = (
        "If the guard comes loose, fingers could be caught in the rotating "
        "parts and crushed.",
        "the gear housing could crush a finger if the guard fails",
        "If the latch gives way, the spring under tension is released. "
        "Someone nearby could suffer a serious injury.",
    )
    for text in texts:
        for sig in derive_inventor_stated_safety_signals(_state(MECH, text)):
            assert sig.domain_context == MECH
            assert sig.domain_context != ELEC


def test_non_cue_mechanical_text_derives_nothing():
    for text in ("The gearbox uses a planetary gear set.",
                 "A lever arm rotates the output shaft smoothly.",
                 "a hinge idea"):
        assert derive_inventor_stated_safety_signals(_state(MECH, text)) == ()


def test_negation_and_attribution_guards_apply():
    for text in ("There is no safety risk if the blade comes loose.",
                 "A specialist will determine whether the guard fails and "
                 "fingers could be caught in the rotating parts and crushed."):
        assert derive_inventor_stated_safety_signals(_state(MECH, text)) == ()


def test_electronics_hazard_texts_do_not_fire_for_mechanical_session():
    """Standing collision guards: the contract's vocabulary-conditional pins
    (F001 r2 / family-less loop / cold-load seed; the D3-A trigger) remain
    truthfully un-flipped — asserted affirmatively here."""
    for text in _MUST_NOT_FIRE:
        assert derive_inventor_stated_safety_signals(_state(MECH, text)) == (), text


# ---------------------------------------------------------------- S15 deliverable surface


def test_s15_capability_scope_statement_dropped_automatically():
    """The mechanical deliverable block now mirrors the electronics shape (no
    capability_scope key) with NO assembler change — the statement keys on
    has_governed_safety_cue_family alone."""
    block = _signals_block(_state(MECH, "a plain mechanism idea"))
    assert "capability_scope" not in block
    assert block["signals"] == []
    firing = _signals_block(_state(
        MECH, "If the guard comes loose, fingers could be caught in the "
              "rotating parts and crushed."))
    assert "capability_scope" not in firing
    assert firing["total"] == 1
    assert firing["signals"][0]["domain_context"] == MECH


# ---------------------------------------------------------------- electronics protection


def test_electronics_family_constants_byte_identical():
    fam = ss._DOMAIN_CUE_FAMILIES[ELEC]
    canon = json.dumps(
        {k: (v if isinstance(v, str) else list(v)) for k, v in fam.items()},
        sort_keys=True)
    assert hashlib.sha256(canon.encode()).hexdigest() == _ELEC_FAMILY_SHA256
    assert fam["failure"] is ss._FAILURE_CUES
    assert fam["subject"] is ss._SUBJECT_CUES
    assert fam["consequence"] is ss._CONSEQUENCE_CUES
    assert fam["context_terms"] is ss._ELECTRICAL_TERMS


def test_electronics_derivation_behavior_preserved():
    st = _state(ELEC, "If the alarm fails to warn people, the fire hazard "
                      "could cause harm to anyone nearby.")
    signals = derive_inventor_stated_safety_signals(st)
    assert len(signals) == 1
    assert signals[0].domain_context == ELEC
    none_st = _state(None, "If the sensor fails to detect overcurrent, it "
                           "could cause a fire.")
    fallback = derive_inventor_stated_safety_signals(none_st)
    assert len(fallback) == 1
    assert fallback[0].domain_context == ELEC   # legacy MVP default unchanged
    block = _signals_block(_state(ELEC, "a plain electronics idea"))
    assert "capability_scope" not in block


# ---------------------------------------------------------------- declaration cascade


def test_declaration_cascade_exact_content():
    pack = _mech_pack()
    cap = pack["capability_declaration"]
    cov = pack["coverage_declaration"]
    assert cap["unsupported_categories"][0] == _SAFETY_BOUNDARY_STATEMENT
    assert cov["not_covered_areas"][0] == _SAFETY_BOUNDARY_STATEMENT
    assert cov["covered_areas"][-1] == _COVERED_DETECTION_ENTRY
    assert cap["supported_analysis_categories"][-1] == \
        _SUPPORTED_DETECTION_CATEGORY
    # safety determination stays NOT COVERED, in both declarations
    assert "Safety determination of any kind is NOT COVERED" in \
        cap["unsupported_categories"][0]
    assert "never a determination" in cov["not_covered_areas"][0]


def test_declaration_cascade_complete_no_stale_pending_statement():
    """Truthfulness-cascade completeness: the former OD-M2 clause-1
    'NOT COVERED pending a governed Mechanical safety-cue family' wording
    survives NOWHERE in the pack."""
    raw = json.dumps(_mech_pack()).lower()
    assert "pending a governed" not in raw
    assert "safety-signal derivation is not covered" not in raw


def test_declaration_and_family_consistent():
    """No false capability advertisement in either direction: the declaration
    claims detection ⇔ the governed family exists and detects."""
    covered = " ".join(_mech_pack()["coverage_declaration"]["covered_areas"])
    assert "safety-cue family" in covered
    assert has_governed_safety_cue_family(MECH) is True
    st = _state(MECH, "If the guard comes loose, fingers could be caught in "
                      "the rotating parts and crushed.")
    assert len(derive_inventor_stated_safety_signals(st)) == 1


# ---------------------------------------------------------------- inventory-unchanged proof


def test_signal_inventory_unchanged_proof():
    """The ONE explicit proof (contract §4 items 10-11) behind the I4 AND I5
    mechanical pack-hash re-freezes: both signal inventories are canonically
    identical to their I2/I3-era pins — no corpus rebuild was required or
    performed."""
    pack = _mech_pack()
    for field, expected in _FROZEN_SIGNAL_INVENTORY.items():
        assert _canon_hash(pack[field]) == expected, field
    for field, expected in _FROZEN_NON_DECLARATION_FIELDS.items():
        assert _canon_hash(pack[field]) == expected, field


# ---------------------------------------------------------------- provenance


def test_provenance_record_pr005():
    with open(_PROV_PATH, encoding="utf-8") as fh:
        records = {r["record_id"]: r for r in json.load(fh)["records"]}
    assert "mechanical:PR005" in records
    rec = records["mechanical:PR005"]
    assert rec["pack_id"] == MECH
    assert rec["source_type"] == "governance_record"
    assert "P9_MECH_SAFETY_CUE_FAMILY_CONTRACT" in rec["notes"]
    assert "never a safety determination" in rec["notes"]
    assert "hazard classes" in rec["notes"]
    # prior records untouched alongside it
    for rid in ("mechanical:PR001", "mechanical:PR002",
                "mechanical:PR003", "mechanical:PR004"):
        assert rid in records
    # the declarations and the pack note reference PR005
    assert "mechanical:PR005" in json.dumps(_mech_pack())


# ---------------------------------------------------------------- activation honesty


def test_activation_state_now_includes_mechanical():
    # Mechanical Activation Execution Gate: mechanical is now really
    # activated in production — the governed safety-cue family this file
    # covers is no longer gated behind a recognized-but-inactive domain.
    assert activated_domains() == [ELEC, MECH]
    assert support_state(MECH) == "activated"
    assert is_activated(MECH) is True
    assert is_activated(ELEC) is True


# ---------------------------------------------------------------- determinism


def test_deterministic_repeated_derivation():
    text = ("If the guard comes loose, fingers could be caught in the "
            "rotating parts and crushed.")
    first = derive_inventor_stated_safety_signals(_state(MECH, text))
    second = derive_inventor_stated_safety_signals(_state(MECH, text))
    assert [(s.signal_id, s.safety_subject, s.failure_condition,
             s.possible_consequence, s.domain_context, s.statement)
            for s in first] == \
           [(s.signal_id, s.safety_subject, s.failure_condition,
             s.possible_consequence, s.domain_context, s.statement)
            for s in second]
    assert has_governed_safety_cue_family(MECH) is \
        has_governed_safety_cue_family(MECH) is True


# ---------------------------------------------------------------- self-integrity


_EXPECTED_TESTS = [
    "test_activation_state_now_includes_mechanical",
    "test_declaration_and_family_consistent",
    "test_declaration_cascade_complete_no_stale_pending_statement",
    "test_declaration_cascade_exact_content",
    "test_deterministic_repeated_derivation",
    "test_electronics_derivation_behavior_preserved",
    "test_electronics_family_constants_byte_identical",
    "test_electronics_hazard_texts_do_not_fire_for_mechanical_session",
    "test_fail_safe_domains_still_family_less",
    "test_family_now_governed_for_mechanical",
    "test_family_shape_mirrors_electronics_precedent",
    "test_green_adjacent_pair_derivation",
    "test_green_never_electronics_labeled",
    "test_green_same_sentence_derivation",
    "test_negation_and_attribution_guards_apply",
    "test_no_electronics_identity_collision",
    "test_no_thermal_claim_in_family_or_declarations",
    "test_non_cue_mechanical_text_derives_nothing",
    "test_provenance_record_pr005",
    "test_s15_capability_scope_statement_dropped_automatically",
    "test_self_integrity",
    "test_signal_inventory_unchanged_proof",
    "test_vocabulary_equality_pinned",
]


def test_self_integrity():
    """Anti-tamper (the established I5/D-GMPR pattern): the file's test
    inventory is introspected and pinned, and load-bearing engine constructs
    are needle-checked with runtime-CONSTRUCTED needles (the needle list
    cannot satisfy itself)."""
    actual = sorted(name for name in globals() if name.startswith("test_"))
    assert actual == _EXPECTED_TESTS
    source = open(ss.__file__.rstrip("c"), encoding="utf-8").read()
    needles = (
        "_MECHANICAL" + "_DOMAIN = \"mechanical\"",
        "_MECH_" + "FAILURE_CUES = (",
        "_MECH_" + "SUBJECT_CUES = (",
        "_MECH_" + "CONSEQUENCE_CUES = (",
        "_MECH_" + "CONTEXT_TERMS = (",
        "mechanical" + ":PR005",
    )
    for needle in needles:
        assert needle in source, needle
