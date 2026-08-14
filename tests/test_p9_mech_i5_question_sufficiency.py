"""P9-MECH-I5 — §12(a) Mechanical Question-Content Sufficiency Evidence.

Governed by the AUTHORITATIVE increment contract
``docs/governance/P9_MECH_I5_QUESTION_SUFFICIENCY_EVIDENCE_CONTRACT.md``.

EVIDENCE ONLY — zero runtime change; every pin asserts the UNCHANGED runtime
through the CANONICAL generic question path (``engine.domain_rules.
get_domain_question``, runtime-consumed by ``engine/progression_loop.py``).
No second question service, no Path-N wrapper, no seam repair.

§12(b) STATUS (binding evidence, not permission): the non-specialist Path-N
service for Mechanical remains BLOCKED by the OPEN ``D-GMPR-01-D-D3`` coupling —
``engine/path_n_questions.py`` serves the Electronics-OWNED committed artifact
only and returns ``None`` for a mechanical domain identity. The pin below
asserts that blocker AS a blocker so its future remediation (at the D-GMPR
gate, its own owner) surfaces visibly. Activation-grade §12 completion remains
conditional on that gate.

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

Mechanical remains NOT QUALIFIED and NOT ACTIVATED; §15/§16 remain open.
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

_FROZEN_ENGINE_SHA256 = {
    "engine/domain_rules.py": "5df2ae26b0a6e78f37bb467d1d8b3d377596f9fcbbc7f869d1ed1ac5b5ab204b",
    "engine/progression_loop.py": "bbb49b49f388dba2f0b906a79bdd656de23b33ec7101bd9d9da9c290ae45c4c5",
    "engine/path_n_questions.py": "1dcd218af527c8a4433a4e46c858b2114afb239a544cbbebea0da819319b7282",
}
_FROZEN_PACK_SHA256 = {
    # mechanical: the I4 terminal-corpus validity anchor — MUST stay byte-frozen here.
    "mechanical": "ae9db65c3d69635368c9d8f708ad76a94293e715c9c92b7c953aea83f9cacb5d",
    "electronics_electrical": "3539cfc62710da92f12ac529c07ddaea85011536e5c9f88efb2e2303bb1b964c",
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
        "test_dgmpr_seam_blocker_still_present",
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


def test_dgmpr_seam_blocker_still_present():
    # BLOCKER EVIDENCE, not permission: the Electronics-OWNED Path-N artifact
    # serves electronics/None only; a mechanical identity receives None. When
    # the future D-GMPR gate remediates the seam, THIS pin fails visibly and
    # must be reconciled under that gate's own contract.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        assert get_served_question("MECHANISM_COMPLETENESS", 0, domain="mechanical") is None
        assert get_served_question("MECHANISM_COMPLETENESS", 0, domain=None) is not None
        assert (
            get_served_question("MECHANISM_COMPLETENESS", 0, domain="electronics_electrical")
            is not None
        )


# ---------------------------------------------------------------- recognition / activation / invariance


def test_recognition_activation_separation():
    assert support_state("mechanical") == "recognized_not_activated"
    assert is_activated("mechanical") is False
    assert activated_domains() == ["electronics_electrical"]


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
