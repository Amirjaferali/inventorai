"""D-GMPR-D3-PN — Path-N Domain-Neutral Question Service (RED→GREEN evidence).

Governed by the AUTHORITATIVE corrected contract
``docs/governance/DGMPR_D3_PATH_N_DOMAIN_NEUTRAL_SERVICE_CONTRACT.md``.

Proves the remediation of the LAST D-GMPR-01-D-D3 coupling: ONE canonical Path-N
seam (same public functions/signatures) with EXPLICIT BOUNDED domain→artifact
resolution; Electronics + the None default byte-identical; mechanical served its
OWN committed artifact — a VERBATIM projection of the I5-proven pack questions;
artifact-less recognized domains, unknown domains, and traversal-shaped strings
fail-safe to None; per-domain caches isolated; no wrapper, no second service.

Reconciliation note (Mechanical Activation Execution Gate): mechanical is now
REALLY activated in production (`engine.domain_activation.activated_domains()
== ['electronics_electrical', 'mechanical']`) and remains NOT QUALIFIED
(P9-QS qualification is a separate, still-unauthorized gate). The single test
below that specifically pins the pre-activation "recognized_not_activated"
state is reconstructed via a local activation double so this file's Path-N
service-neutrality claims (which do not themselves depend on activation
state) remain otherwise unchanged.
"""

import hashlib
import json
import os
import warnings

from engine import path_n_questions, progression_loop
from engine.domain_activation import activated_domains, is_activated, support_state
from engine.path_n_questions import ServedQuestion, get_path_n_question, get_served_question

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CONFIG = os.path.join(_REPO, "docs", "governance", "path_n_content_config")
_MECH_ARTIFACT = os.path.join(_CONFIG, "mechanical_path_n_questions.json")
_ELEC_ARTIFACT = os.path.join(_CONFIG, "electronics_electrical_path_n_questions.json")
_MECH_PACK = os.path.join(_REPO, "domains", "mechanical", "domain.json")

# Electronics artifact byte-freeze (contract: MUST NOT change).
# RVR-7 re-freeze (authorized; implementation path manifest freeze PR #588):
# the electronics artifact gains the governed `text_ar` sibling on every entry.
# English `text`, `question_id`, order and metadata are byte-unchanged — proven
# by `test_electronics_english_surface_unchanged_under_rvr7` below, which is what
# actually protects the English content; this hash pins the file as a whole.
#   pre-RVR-7 electronics artifact =
#       399ce8b9a7f65f33b77d4f8a11d8e544f49133b27e2689c04c24fb7ef92efbfd
# RVR-7 semantic-repair re-freeze (authorized; Owner-adopted second bilingual
# semantic review, 32/34 accepted, repair required on N-PF-3 MATERIAL NARROWING
# and N-PF-4 TECHNICAL-MEANING SHIFT). ONLY those two `text_ar` values changed;
# every English `text`, every `question_id`, the order, the metadata and the
# other nine Arabic variants are byte-unchanged — proven independently by
# `test_electronics_english_surface_unchanged_under_rvr7`, which pins the English
# surface verbatim and passed unmodified across this re-freeze. This hash pins
# the file as a whole and is the mechanically consequent update.
#   pre-repair (RVR-7 implementation) electronics artifact =
#       a9ccd4296f0853400b8a0a7d089f4b8dec4606f801d9222d04b3ea27abb69ac1
_ELEC_ARTIFACT_SHA256 = "7b3e06c0492c91486b429ce14479c43a1c8ff3ebe268137c148b07cc7cb8590c"


def _mech_artifact():
    with open(_MECH_ARTIFACT, encoding="utf-8") as fh:
        return json.load(fh)


# ---------------------------------------------------------------- artifact shape & verbatim projection


def test_mechanical_artifact_exists_with_contract_shape():
    data = _mech_artifact()
    assert sorted(data.keys()) == ["gaps", "metadata"]
    md = data["metadata"]
    for key in ("domain", "source", "provenance_ref", "contract", "generated_by_gate"):
        assert key in md, f"metadata missing required key: {key}"
    assert md["domain"] == "mechanical"
    assert md["provenance_ref"] == "mechanical:PR001"
    assert "DGMPR_D3_PATH_N_DOMAIN_NEUTRAL_SERVICE_CONTRACT" in md["contract"]
    assert "verbatim" in md["source"]
    # RVR-7 (PR #588): the CLOSED allowed-key set. `text_ar` is the single governed
    # Arabic sibling admitted by the authoritative freeze (§5.E); every other key is
    # still rejected, so unknown-field protection is preserved — and tightened,
    # because the allowlist admits exactly one disclosed extension and nothing else.
    for gap, variants in data["gaps"].items():
        for entry in variants:
            assert set(entry).issubset({"question_id", "text", "text_ar"}), gap
            assert {"question_id", "text"}.issubset(entry), gap


def test_mechanical_artifact_is_verbatim_pack_projection():
    # 1:1 with the I5-proven pack content: same gap types, order, question_id, text.
    with open(_MECH_PACK, encoding="utf-8") as fh:
        pack = json.load(fh)
    expected = {
        g["gap_type_id"]: [
            {"question_id": q["question_id"], "text": q["text"]} for q in g["questions"]
        ]
        for g in pack["gap_type_mappings"]
    }
    # RVR-7 (PR #588 §5.E): the projection is now taken over the ENGLISH fields
    # only. English provenance is UNCHANGED in strength — the artifact's
    # {question_id, text} projection must still equal the pack 1:1, so any drift of
    # the mechanical English wording at the artifact still flips this RED. The pack
    # itself is untouched and carries no Arabic content.
    english_projection = {
        gap: [{"question_id": e["question_id"], "text": e["text"]} for e in variants]
        for gap, variants in _mech_artifact()["gaps"].items()
    }
    assert english_projection == expected
    assert sum(len(v) for v in expected.values()) == 10


# ---------------------------------------------------------------- GREEN: mechanical served canonically


def test_mechanical_served_all_gap_types_all_indices_with_clamping():
    gaps = _mech_artifact()["gaps"]
    for gap, variants in gaps.items():
        for i, entry in enumerate(variants):
            served = get_served_question(gap, i, domain="mechanical")
            assert isinstance(served, ServedQuestion)
            assert served.question_id == entry["question_id"]
            assert served.text == entry["text"]
            assert served.design_gap_id == gap
        for beyond in (len(variants), len(variants) + 7):
            clamped = get_served_question(gap, beyond, domain="mechanical")
            assert clamped.question_id == variants[-1]["question_id"], f"{gap} clamp"


def test_runtime_callers_serve_mechanical_content_on_path_n():
    gap = "MECHANISM_COMPLETENESS"
    first = _mech_artifact()["gaps"][gap][0]["text"]
    assert progression_loop.get_question("mechanical", gap, 0, path="N") == first
    assert progression_loop.get_display_question("mechanical", gap, 0, path="N") == first


def test_neutral_stall_reframe_at_mechanical_exhaustion():
    gap = "MECHANISM_COMPLETENESS"
    exhausted = len(_mech_artifact()["gaps"][gap])  # beyond last index → clamp
    shown = progression_loop.get_display_question("mechanical", gap, exhausted, path="N")
    assert shown == progression_loop._STALL_REFRAME
    for electronics_only in ("circuit", "electrical", "electronic", "voltage"):
        assert electronics_only not in shown.lower()


# ---------------------------------------------------------------- Electronics exact non-regression


def test_electronics_artifact_byte_frozen():
    with open(_ELEC_ARTIFACT, "rb") as fh:
        assert hashlib.sha256(fh.read()).hexdigest() == _ELEC_ARTIFACT_SHA256


def test_electronics_and_none_default_serve_identical_electronics_content():
    with open(_ELEC_ARTIFACT, encoding="utf-8") as fh:
        gaps = json.load(fh)["gaps"]
    for gap, variants in gaps.items():
        for i in range(len(variants) + 2):
            explicit = get_served_question(gap, i, domain="electronics_electrical")
            default = get_served_question(gap, i, domain=None)
            expected = variants[min(i, len(variants) - 1)]
            for served in (explicit, default):
                assert served.question_id == expected["question_id"], f"{gap}[{i}]"
                assert served.text == expected["text"], f"{gap}[{i}]"
            assert explicit == default


def test_no_cross_domain_leakage_between_artifacts():
    gap = "MECHANISM_COMPLETENESS"  # shared gap-type id across both artifacts
    mech = get_served_question(gap, 0, domain="mechanical")
    elec = get_served_question(gap, 0, domain="electronics_electrical")
    default = get_served_question(gap, 0, domain=None)
    assert mech.question_id.startswith("mechanical:")
    assert not elec.question_id.startswith("mechanical:")
    assert mech.question_id != elec.question_id and mech.text != elec.text
    assert default == elec  # the None default is Electronics, never mechanical


# ---------------------------------------------------------------- fail-safe / bounded resolution


def test_artifactless_and_unknown_domains_fail_safe_none():
    for domain in (
        "software", "medical_device", "iot_electronics", "no_such_domain",
        "../mechanical", "../../etc/passwd", "mechanical/../electronics_electrical",
        "", "MECHANICAL",
    ):
        assert get_served_question("MECHANISM_COMPLETENESS", 0, domain=domain) is None, domain
        assert get_path_n_question("MECHANISM_COMPLETENESS", 0, domain=domain) is None, domain


def test_bounded_mapping_is_the_only_resolution_path():
    # The explicit bounded mapping contains exactly the two committed artifacts;
    # raw domain strings never reach the filesystem (m-probe target).
    mapping = path_n_questions._DOMAIN_ARTIFACTS
    assert sorted(mapping.keys()) == ["electronics_electrical", "mechanical"]
    for key, artifact_path in mapping.items():
        assert artifact_path.parent == path_n_questions._ARTIFACT_DIR
        assert artifact_path.name == f"{key}_path_n_questions.json"
        assert artifact_path.exists()


def test_runtime_fallthrough_unchanged_for_artifactless_domains():
    gap = "MECHANISM_COMPLETENESS"
    generic = progression_loop.QUESTIONS[gap][0]
    assert progression_loop.get_question("software", gap, 0, path="N") == generic
    assert progression_loop.get_question("medical_device", gap, 0, path="N") == generic


def test_malformed_artifact_fails_loud_without_poisoning_other_caches(tmp_path, monkeypatch):
    # A broken artifact for one domain fails loudly and does NOT contaminate the
    # other domains' caches (per-domain load-once; success-only population).
    broken = tmp_path / "broken_path_n_questions.json"
    broken.write_text('{"metadata": {}, "gaps": {}}', encoding="utf-8")
    mapping = dict(path_n_questions._DOMAIN_ARTIFACTS)
    mapping["broken"] = broken
    monkeypatch.setattr(path_n_questions, "_DOMAIN_ARTIFACTS", mapping)
    try:
        import pytest

        with pytest.raises(ValueError):
            get_served_question("MECHANISM_COMPLETENESS", 0, domain="broken")
        assert "broken" not in path_n_questions._PATH_N_GAPS
        # Other domains keep serving normally after the failure.
        assert get_served_question("MECHANISM_COMPLETENESS", 0, domain="mechanical") is not None
        assert get_served_question("MECHANISM_COMPLETENESS", 0, domain=None) is not None
    finally:
        path_n_questions._PATH_N_GAPS.pop("broken", None)


def test_deterministic_repeats_and_cache_isolation():
    for _ in range(2):
        m = get_served_question("PHYSICAL_FEASIBILITY", 1, domain="mechanical")
        e = get_served_question("PHYSICAL_FEASIBILITY", 1, domain="electronics_electrical")
        assert m == get_served_question("PHYSICAL_FEASIBILITY", 1, domain="mechanical")
        assert e == get_served_question("PHYSICAL_FEASIBILITY", 1, domain="electronics_electrical")
        assert m != e
    assert set(path_n_questions._PATH_N_GAPS.keys()) <= {"electronics_electrical", "mechanical"}


# ---------------------------------------------------------------- self-integrity (anti-weakening)


def test_evidence_inventory_and_critical_pins_intact():
    # Introspect the module's REAL test inventory (deleting/renaming any evidence
    # test flips RED) and source-pin the critical assertions via RUNTIME-
    # CONSTRUCTED needles (weakening a guard constant flips RED; the needle list
    # cannot satisfy itself). The proven I5 self-integrity pattern.
    expected_tests = [
        "test_artifactless_and_unknown_domains_fail_safe_none",
        "test_bounded_mapping_is_the_only_resolution_path",
        "test_deterministic_repeats_and_cache_isolation",
        "test_electronics_and_none_default_serve_identical_electronics_content",
        "test_electronics_artifact_byte_frozen",
        "test_electronics_english_surface_unchanged_under_rvr7",
        "test_evidence_inventory_and_critical_pins_intact",
        "test_malformed_artifact_fails_loud_without_poisoning_other_caches",
        "test_mechanical_artifact_exists_with_contract_shape",
        "test_mechanical_artifact_is_verbatim_pack_projection",
        "test_mechanical_pack_carries_no_arabic_content",
        "test_mechanical_served_all_gap_types_all_indices_with_clamping",
        "test_mechanical_service_does_not_activate_mechanical",
        "test_neutral_stall_reframe_at_mechanical_exhaustion",
        "test_no_cross_domain_leakage_between_artifacts",
        "test_runtime_callers_serve_mechanical_content_on_path_n",
        "test_runtime_fallthrough_unchanged_for_artifactless_domains",
    ]
    actual = sorted(name for name in globals() if name.startswith("test_"))
    assert actual == expected_tests, "evidence inventory changed"
    with open(os.path.abspath(__file__), encoding="utf-8") as fh:
        source = fh.read()
    needles = (
        'assert is_activated("mechanical") is ' + "False,".rstrip(","),
        'assert get_served_question("MECHANISM_COMPLETENESS", 0, domain=domain) is ' + "None,".rstrip(","),
        "assert activated_domains() == " + '["electronics_electrical"],'.rstrip(","),
    )
    for critical in needles:
        assert source.count(critical) == 1, f"critical pin weakened/removed: {critical!r}"


# ---------------------------------------------------------------- recognition / activation


def test_mechanical_service_does_not_activate_mechanical(monkeypatch):
    # Pinned to the pre-activation state this specific claim is about; see the
    # module docstring's reconciliation note. Real production activation now
    # includes mechanical.
    from engine import domain_activation
    monkeypatch.setattr(domain_activation, "_ACTIVATED_DOMAINS",
                         frozenset({"electronics_electrical"}))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        assert get_served_question("MECHANISM_COMPLETENESS", 0, domain="mechanical") is not None
        assert support_state("mechanical") == "recognized_not_activated"
        assert is_activated("mechanical") is False
        assert activated_domains() == ["electronics_electrical"]


# ---------------------------------------------------------------- RVR-7 English-provenance evidence

# The pre-RVR-7 English surface of the electronics artifact, pinned verbatim so a
# re-freeze of the whole-file hash can never quietly carry an English change with it.
_ELEC_EN_PRE_RVR7 = {
    "N-MC-1": "Explain in everyday words how you imagine the system would notice the problem and respond.",
    "N-MC-2": "What are the main parts of your idea, in your own words, and what does each part do?",
    "N-MC-3": "Walk through what happens step by step, from the moment the problem starts to the moment someone knows about it.",
    "N-MC-4": "Is there any part of how it works that you're unsure about or imagining loosely? Describe it as best you can.",
    "N-PF-1": "What would need to be true for this system to work safely in the real world?",
    "N-PF-2": "What do you think would keep the system running reliably over time?",
    "N-PF-3": "Are there real-world conditions, such as heat, water, time, or wear, that might stop it from working? Which ones worry you most?",
    "N-PF-4": "If an engineer offered to check one thing about whether this can physically work, what would you ask them to check first?",
    "N-BA-1": "Which situations should the system be responsible for handling?",
    "N-BA-2": "What is your idea responsible for, and what is someone or something else's job?",
    "N-BA-3": "Describe a situation where the system should definitely react, and one where it should definitely stay quiet.",
}


def test_electronics_english_surface_unchanged_under_rvr7():
    """The RVR-7 hash re-freeze is additive ONLY: every English question text and
    the committed id order are byte-identical to the pre-RVR-7 artifact."""
    with open(_ELEC_ARTIFACT, encoding="utf-8") as fh:
        gaps = json.load(fh)["gaps"]
    english = {e["question_id"]: e["text"] for v in gaps.values() for e in v}
    assert english == _ELEC_EN_PRE_RVR7
    for variants in gaps.values():
        for entry in variants:
            assert set(entry).issubset({"question_id", "text", "text_ar"})


def test_mechanical_pack_carries_no_arabic_content():
    """RVR-7 §5.E: Arabic lives in the Path-N artifact ONLY. The mechanical domain
    pack stays byte-identical and acquires no second Arabic content location."""
    with open(_MECH_PACK, encoding="utf-8") as fh:
        raw = fh.read()
    assert not [c for c in raw if "\u0600" <= c <= "\u06ff"], (
        "mechanical domain pack must carry no Arabic content")
