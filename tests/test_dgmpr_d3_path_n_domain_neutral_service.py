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
_ELEC_ARTIFACT_SHA256 = "399ce8b9a7f65f33b77d4f8a11d8e544f49133b27e2689c04c24fb7ef92efbfd"


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
    for gap, variants in data["gaps"].items():
        for entry in variants:
            assert sorted(entry.keys()) == ["question_id", "text"], gap


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
    assert _mech_artifact()["gaps"] == expected
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
        "test_evidence_inventory_and_critical_pins_intact",
        "test_malformed_artifact_fails_loud_without_poisoning_other_caches",
        "test_mechanical_artifact_exists_with_contract_shape",
        "test_mechanical_artifact_is_verbatim_pack_projection",
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
