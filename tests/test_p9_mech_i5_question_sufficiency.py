"""P9-MECH-I5 — §12(a) Mechanical Question-Content Sufficiency Evidence.

Governed by the AUTHORITATIVE increment contract
``docs/governance/P9_MECH_I5_QUESTION_SUFFICIENCY_EVIDENCE_CONTRACT.md``.

EVIDENCE ONLY — zero runtime change; every pin asserts the UNCHANGED runtime
through the CANONICAL generic question path (``engine.domain_rules.
get_domain_question``, runtime-consumed by ``engine/progression_loop.py``).
No second question service, no Path-N wrapper, no seam repair.

§12(b) STATUS (reconciled under D-GMPR-D3-PN — DGMPR_D3_PATH_N_DOMAIN_NEUTRAL_
SERVICE_CONTRACT.md §5, reconciliation #1): the original blocker pin here
asserted that ``engine/path_n_questions.py`` returned ``None`` for a mechanical
domain identity and was WRITTEN to flip at the D-GMPR gate. That gate's
implementation made the canonical seam domain-neutral, so the pin below now
asserts the REMEDIATED behavior (mechanical served its own verbatim committed
artifact; electronics/None unchanged). §12(b)'s activation-grade completion
remains recordable only at the D-GMPR lane's own closure.

WORDING-SUFFICIENCY CRITERIA (defined BEFORE evaluation; each is asserted
mechanically where checkable and recorded as reviewed evidence where semantic):
  W1 understandable to a non-specialist (lay vocabulary; no jargon beyond the
     pack's own declared concept-level terms);
  W2 one primary question per prompt (exactly one question mark; a
     parenthetical example list does not add a second question);
  W3 no hidden electronics-only terminology (no electronics-vocabulary tokens);
  W4 aligned with its governed gap type (mechanism/feasibility/boundary focus);
  W5 no capability claim beyond the Mechanical I1 declarations (no demand for
     FEA/stress/tolerance/materials-certification/manufacturing-validation/
     regulatory/thermal/physical-testing evidence — asking the INVENTOR to
     STATE principles or constraints is within declared concept-level scope);
  W6 no specialist assumption not represented in the pack.
VERDICT (recorded): all ten committed questions PASS W1–W6 — §12(a) wording
sufficiency is supported by evidence; nothing was rewritten or patched.

At the time of this gate's recorded evidence run, Mechanical was NOT QUALIFIED
and NOT ACTIVATED (§15/§16 then open). Mechanical was subsequently qualified and
activated by later governed Phase-9 gates (see
docs/governance/PHASE_9_FORMAL_CLOSURE_RECORD.md); the recorded verdict above is
historical evidence, unchanged by that activation.
"""

import hashlib
import json
import os
import warnings

from engine.domain_activation import activated_domains, is_activated, support_state
from engine.domain_rules import get_domain_question
from engine.path_n_questions import get_served_question

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DOMAINS = os.path.join(_REPO, "domains")
_MECH_PATH = os.path.join(_DOMAINS, "mechanical", "domain.json")
_PROV_PATH = os.path.join(_DOMAINS, "domain_provenance.json")

# ---------------------------------------------------------------- invariance anchors

# L2SC-01 reconciliation (disclosed; see test_p9_mech_i3_signal_quality.py's
# own reconciliation comment for the full domain_rules/progression_loop
# disclosure). engine/path_n_questions.py is untouched by L2SC-01 — hash
# unchanged.
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
# engine/path_n_questions.py is untouched by PVCG-R2-I — hash unchanged.
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
    "engine/progression_loop.py": "b6cf9819ca54677d76bdf9facf47710a9d96f2e8f9a5c3a3120126b971cfcf72",
    # D-GMPR-D3-PN reconciliation #2 (disclosed; DGMPR_D3_PATH_N_DOMAIN_NEUTRAL_
    # SERVICE_CONTRACT.md §5): the seam hash is re-frozen at the remediated
    # domain-neutral seam. domain_rules/progression_loop hashes are UNCHANGED.
    "engine/path_n_questions.py": "a1a682d38293defd4b351e6238aeb870b4f765eaf3fc0f105c4932f75286ce7f",
}
# L2SC-01 reconciliation (disclosed; docs/governance/L2SC01_SUBSTANCE_SIGNAL_
# PLURAL_ALIAS_INCREMENT_CONTRACT.md §10): mechanical and electronics_electrical
# re-frozen after adding the authorized, additive-only
# `substance_signal_plural_aliases` field to each — signal inventory, question-
# inventory pins, and this file's own test inventory are untouched (same
# signal-inventory-unchanged proof cited below).
_FROZEN_PACK_SHA256 = {
    # mechanical: the I4 terminal-corpus validity anchor. P9-MECH-SF
    # reconciliation (contract §4 item 11 — the corrected contract's added
    # certain flip, disclosed): re-frozen after the mandatory declaration
    # truthfulness cascade under the SAME signal-inventory-unchanged proof as
    # the I4 anchor (canonical classification/substance hashes 860ce084…/
    # c14ae2d5… pinned in tests/test_p9_mech_safety_cue_family.py); no corpus
    # rebuild — declaration bytes are the only pack change. Engine hashes,
    # other-pack hashes, question-inventory pins, and this file's test
    # inventory are untouched.
    "mechanical": "901dd7188ddefda9cbe69a835cc64959c1d55debfe61b262d720abd904069e79",
    "electronics_electrical": "53f431e38a70c2b621e19afb7323ad9bc4732c6c4151ea6b8c46a3214f098dfb",
    "medical_device": "6070cf9281a7a376780175e7e1d3879be598384bcaf4dc370e56f7bf613e3ade",
    "software": "1c9cefa14641c079ddb5c21c59f398866adf43561101743b67e611936a67e3a7",
    "iot_electronics": "f04c825ad25dea0c6db2ee310649fe377329f30c5461f2756019104013e53406",
}

# The exact committed Mechanical question inventory (equality-pinned; the
# calibration/anti-drift primary protection — any rewording flips RED).
_EXPECTED_QUESTIONS = {
    "MECHANISM_COMPLETENESS": [
        "Describe the physical steps your mechanism takes to achieve its function.",
        "What moves, connects, or transfers force?",
        "What are the individual mechanical components and how does each one contribute to the overall motion or function?",
        "If someone tried to build your mechanism tomorrow with no further explanation, what physical detail would be missing?",
    ],
    "PHYSICAL_FEASIBILITY": [
        "What physical principle does your mechanism rely on? (e.g. leverage, spring tension, gear ratio, friction)",
        "What are the material or force constraints your mechanism must operate within?",
    ],
    "BOUNDARY_AMBIGUITY": [
        "What does your mechanism specifically NOT do or NOT cover?",
        "State at least one clear mechanical boundary.",
        "Name one existing mechanical approach similar to yours.",
        "What makes yours different in a concrete, physical way?",
    ],
}

# W5 calibration yardstick — the I1 NOT-COVERED expertise classes: no question may
# DEMAND evidence from these classes (word-boundary guard; the equality pin above
# remains the primary protection against paraphrased drift).
_W5_FORBIDDEN_DEMANDS = (
    "fea", "finite element", "fatigue", "gd&t", "tolerance stack", "certif",
    "regulatory", "manufacturing process", "thermal", "simulation",
    "physical testing", "supply chain", "stress analysis",
)

# W3 guard — electronics-only vocabulary that must not appear in Mechanical prompts.
_W3_ELECTRONICS_TOKENS = (
    "circuit", "voltage", "current", "resistor", "capacitor", "pcb", "firmware",
    "microcontroller", "electrical", "electronic",
)


def _mech():
    with open(_MECH_PATH, encoding="utf-8") as fh:
        return json.load(fh)


# ---------------------------------------------------------------- evidence-class completeness


def test_evidence_class_inventory_complete():
    # m5 guard: introspect the module's REAL test inventory — disabling,
    # renaming, or deleting any evidence test flips this pin RED.
    expected_tests = [
        "test_content_keyed_cross_domain_leakage_protection",
        "test_deterministic_repeated_service",
        "test_dgmpr_seam_remediated_mechanical_served",
        "test_engine_files_byte_frozen",
        "test_evidence_class_inventory_complete",
        "test_exact_ordered_progression_and_clamping",
        "test_fail_safe_none_cases",
        "test_full_gap_type_coverage",
        "test_pack_bytes_frozen_incl_i4_validity_anchor",
        "test_progression_matches_pack_arrays_not_retyped_constants",
        "test_provenance_lineage_resolves",
        "test_recognition_activation_separation",
        "test_w2_one_primary_question_per_prompt",
        "test_w3_no_electronics_only_terminology",
        "test_w4_gap_type_alignment_markers",
        "test_w5_no_capability_demand_beyond_declarations",
    ]
    actual = sorted(name for name in globals() if name.startswith("test_"))
    assert actual == expected_tests, "evidence-class inventory changed (m5 guard)"
    # m6 guard: the critical calibration assertions are self-pinned verbatim in
    # this file's source — weakening a threshold or guard constant flips RED.
    # Needles are CONSTRUCTED at runtime so this pin list cannot satisfy itself.
    with open(os.path.abspath(__file__), encoding="utf-8") as fh:
        source = fh.read()
    needles = (
        'assert text.count("?") <= ' + "1,".rstrip(","),
        'assert not re.search(r"\\b" + re.escape(term) + r"\\b", joined)',
        "assert len(set(served.values())) == " + "4,".rstrip(","),
    )
    for critical in needles:
        assert source.count(critical) == 1, (
            f"critical calibration pin weakened/removed: {critical!r}"
        )
    assert sum(len(v) for v in _EXPECTED_QUESTIONS.values()) == 10


# ---------------------------------------------------------------- coverage / progression / clamping


def test_full_gap_type_coverage():
    data = _mech()
    declared = [g["gap_type_id"] for g in data["gap_type_mappings"]]
    assert declared == ["MECHANISM_COMPLETENESS", "PHYSICAL_FEASIBILITY", "BOUNDARY_AMBIGUITY"]
    for gap in declared:
        first = get_domain_question("mechanical", gap, 0)
        assert isinstance(first, str) and first.strip(), f"no question served for {gap}"


def test_exact_ordered_progression_and_clamping():
    for gap, expected in _EXPECTED_QUESTIONS.items():
        for i, text in enumerate(expected):
            assert get_domain_question("mechanical", gap, i) == text, f"{gap}[{i}]"
        # index clamping: beyond the last index the LAST question keeps serving
        for beyond in (len(expected), len(expected) + 5, 99):
            assert get_domain_question("mechanical", gap, beyond) == expected[-1], f"{gap} clamp"


def test_progression_matches_pack_arrays_not_retyped_constants():
    data = _mech()
    for g in data["gap_type_mappings"]:
        pack_texts = [q["text"] for q in g["questions"]]
        assert pack_texts == _EXPECTED_QUESTIONS[g["gap_type_id"]]
        assert [q["order"] for q in g["questions"]] == list(range(1, len(pack_texts) + 1))


# ---------------------------------------------------------------- wording sufficiency + calibration


def test_w2_one_primary_question_per_prompt():
    for gap, texts in _EXPECTED_QUESTIONS.items():
        for text in texts:
            assert text.count("?") <= 1, f"multiple questions in one prompt: {text!r}"


def test_w3_no_electronics_only_terminology():
    joined = " ".join(t for ts in _EXPECTED_QUESTIONS.values() for t in ts).lower()
    for token in _W3_ELECTRONICS_TOKENS:
        assert token not in joined, f"electronics-only term in Mechanical prompt: {token!r}"


def test_w5_no_capability_demand_beyond_declarations():
    import re

    joined = " ".join(t for ts in _EXPECTED_QUESTIONS.values() for t in ts).lower()
    for term in _W5_FORBIDDEN_DEMANDS:
        assert not re.search(r"\b" + re.escape(term) + r"\b", joined), (
            f"question demands undeclared expertise: {term!r}"
        )


def test_w4_gap_type_alignment_markers():
    # Each gap type's prompts speak to their governed focus (mechanical proof of
    # alignment: the pack's own domain_label focus terms appear in the set).
    mc = " ".join(_EXPECTED_QUESTIONS["MECHANISM_COMPLETENESS"]).lower()
    pf = " ".join(_EXPECTED_QUESTIONS["PHYSICAL_FEASIBILITY"]).lower()
    ba = " ".join(_EXPECTED_QUESTIONS["BOUNDARY_AMBIGUITY"]).lower()
    assert "mechanism" in mc and ("moves" in mc or "force" in mc)
    assert "physical principle" in pf and "constraints" in pf
    assert "not" in ba and ("boundary" in ba or "different" in ba)


# ---------------------------------------------------------------- provenance


def test_provenance_lineage_resolves():
    data = _mech()
    with open(_PROV_PATH, encoding="utf-8") as fh:
        records = {r["record_id"] for r in json.load(fh)["records"]}
    for g in data["gap_type_mappings"]:
        assert g["provenance_ref"] in records, g["gap_type_id"]
        for q in g["questions"]:
            assert q["provenance_ref"] in records, q["question_id"]
            assert q["question_id"].startswith("mechanical:")


# ---------------------------------------------------------------- fail-safe + content-keyed leakage


def test_fail_safe_none_cases():
    assert get_domain_question("mechanical", "NO_SUCH_GAP", 0) is None
    assert get_domain_question("no_such_domain", "MECHANISM_COMPLETENESS", 0) is None


def test_content_keyed_cross_domain_leakage_protection():
    # Gap-type IDs are SHARED across packs, so leakage evidence must be
    # CONTENT-keyed (per independent review): the same shared gap id serves
    # each domain its OWN committed text, and mechanical text appears verbatim
    # in the mechanical pack only.
    shared_gap = "MECHANISM_COMPLETENESS"
    served = {
        dom: get_domain_question(dom, shared_gap, 0)
        for dom in ("mechanical", "software", "medical_device", "electronics_electrical")
    }
    assert served["mechanical"] == _EXPECTED_QUESTIONS[shared_gap][0]
    assert len(set(served.values())) == 4, f"shared gap id served duplicated text: {served}"
    mech_texts = {t for ts in _EXPECTED_QUESTIONS.values() for t in ts}
    for dom in ("software", "medical_device", "electronics_electrical"):
        with open(os.path.join(_DOMAINS, dom, "domain.json"), encoding="utf-8") as fh:
            sibling = json.load(fh)
        sibling_texts = {
            q["text"] for g in sibling["gap_type_mappings"] for q in g["questions"]
        }
        assert not (mech_texts & sibling_texts), f"mechanical text duplicated in {dom}"


# ---------------------------------------------------------------- §12(b) D-GMPR blocker pin


def test_dgmpr_seam_remediated_mechanical_served():
    # D-GMPR-D3-PN reconciliation #1 (disclosed; DGMPR_D3_PATH_N_DOMAIN_NEUTRAL_
    # SERVICE_CONTRACT.md §5): the former blocker pin (mechanical → None) was
    # WRITTEN to flip at the D-GMPR gate and is replaced by the remediated-
    # behavior pin — mechanical is now served its OWN verbatim committed artifact
    # through the canonical seam, while electronics and the None default remain
    # served unchanged. §12(b)'s activation-grade completion is recordable only
    # at that lane's closure, not here.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        served = get_served_question("MECHANISM_COMPLETENESS", 0, domain="mechanical")
        assert served is not None
        assert served.question_id == "mechanical:MECHANISM_COMPLETENESS:Q1"
        assert served.text == _EXPECTED_QUESTIONS["MECHANISM_COMPLETENESS"][0]
        assert get_served_question("MECHANISM_COMPLETENESS", 0, domain=None) is not None
        assert (
            get_served_question("MECHANISM_COMPLETENESS", 0, domain="electronics_electrical")
            is not None
        )


# ---------------------------------------------------------------- recognition / activation / invariance


def test_recognition_activation_separation():
    # Mechanical Activation Execution Gate: mechanical is now really
    # activated. `medical_device` preserves the "recognition alone does not
    # confer activation" principle this test guards.
    assert support_state("medical_device") == "recognized_not_activated"
    assert is_activated("medical_device") is False
    assert is_activated("mechanical") is True
    assert activated_domains() == ["electronics_electrical", "mechanical"]


def test_engine_files_byte_frozen():
    for path, expected in _FROZEN_ENGINE_SHA256.items():
        with open(os.path.join(_REPO, path), "rb") as fh:
            digest = hashlib.sha256(fh.read()).hexdigest()
        assert digest == expected, f"engine file changed outside a governed gate: {path}"


def test_pack_bytes_frozen_incl_i4_validity_anchor():
    for pack, expected in _FROZEN_PACK_SHA256.items():
        with open(os.path.join(_DOMAINS, pack, "domain.json"), "rb") as fh:
            digest = hashlib.sha256(fh.read()).hexdigest()
        assert digest == expected, f"{pack} pack changed (I5 is evidence-only)"


def test_deterministic_repeated_service():
    for gap in _EXPECTED_QUESTIONS:
        for i in (0, 1, 7):
            assert get_domain_question("mechanical", gap, i) == get_domain_question(
                "mechanical", gap, i
            )
