"""
tests/test_s5_i1_domain_registry_hardening.py

§5-I1 — Domain Registry validation hardening (D-P6-14), governed by the accepted
§5-C1 contract-of-record (docs/governance/PRODUCT_FOUNDATION_S5_MULTI_DOMAIN_FOUNDATION_CONTRACT.md).

These tests encode the D-P6-14 validation gaps that the CURRENT loader does NOT
enforce (genuine RED on base 3da1e03), plus backward-compatibility guarantees that
must remain green:

  * allowed lifecycle status values (D-S5-03: lifecycle only, NOT activation);
  * validated version format (MAJOR.MINOR[.PATCH], compatible with existing "1.0");
  * gap_type_mappings element structure (matching the current consumer);
  * rule_nuances element structure (minimum: object; modifier_value NOT frozen);
  * deterministic pack_id collision detection (no silent last-wins);
  * cross-pack alias collision detection (structural uniqueness; no runtime alias
    resolution is introduced);
  * provenance coverage validated against the canonical domains/domain_provenance.json
    (D-FPC-MAP-06: reuse the canonical artifact, do not duplicate a per-pack block),
    soft-gated on the manifest's presence so isolated unit dirs still load.

Scope guards asserted here: legacy iot_electronics stays skipped/inactive; the real
registry still loads exactly the four packs; electronics status is unchanged ("active").
No web/persistence/activation code is exercised or required.
"""

import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from engine.domain_registry import load_registry, list_domains, RegistryLoadError


# --- helpers ---------------------------------------------------------------

def _valid_v1_domain(pack_id="test_pack", **overrides):
    data = {
        "schema_version": "1.0",
        "pack_id": pack_id,
        "version": "1.0",
        "status": "active",
        "display_name": "Test Pack",
        "classification_signals": [{"signal": "test_signal"}],
        "substance_signals": [{"signal": "test_substance"}],
        "gap_type_mappings": [{"gap_type_id": "TEST_GAP"}],
        "rule_nuances": [{"rule_id": "TEST_RULE"}],
    }
    data.update(overrides)
    return data


def _make_pack(tmp_path, subdir, data):
    d = tmp_path / subdir
    d.mkdir()
    (d / "domain.json").write_text(json.dumps(data), encoding="utf-8")


def _write_provenance(tmp_path, pack_ids):
    records = [{"record_id": f"{p}:PR001", "pack_id": p} for p in pack_ids]
    (tmp_path / "domain_provenance.json").write_text(
        json.dumps({"schema_version": "1.0", "records": records}), encoding="utf-8"
    )


def _repo_domains_dir():
    return os.path.join(os.path.dirname(__file__), "..", "domains")


# --- RED: validation gaps that must now be enforced ------------------------

class TestStatusValueHardening:
    def test_unknown_status_rejected(self, tmp_path):
        _make_pack(tmp_path, "d", _valid_v1_domain("p", status="enabled"))
        with pytest.raises(RegistryLoadError):
            load_registry(str(tmp_path))

    def test_registered_status_accepted(self, tmp_path):
        _make_pack(tmp_path, "d", _valid_v1_domain("p", status="registered"))
        assert "p" in load_registry(str(tmp_path))

    def test_deprecated_status_accepted(self, tmp_path):
        _make_pack(tmp_path, "d", _valid_v1_domain("p", status="deprecated"))
        assert "p" in load_registry(str(tmp_path))

    def test_legacy_active_status_still_accepted(self, tmp_path):
        # D-S5-03 back-compat: existing packs use "active"; accepted as a legacy
        # lifecycle value (never reinterpreted as user-facing activation).
        _make_pack(tmp_path, "d", _valid_v1_domain("p", status="active"))
        assert "p" in load_registry(str(tmp_path))


class TestVersionFormatHardening:
    @pytest.mark.parametrize("bad", ["1", "v1.0", "1.x", "1.0.0.0", "", "abc"])
    def test_malformed_version_rejected(self, tmp_path, bad):
        _make_pack(tmp_path, "d", _valid_v1_domain("p", version=bad))
        with pytest.raises(RegistryLoadError):
            load_registry(str(tmp_path))

    @pytest.mark.parametrize("good", ["1.0", "1.0.0", "2.13", "0.1.4"])
    def test_valid_version_accepted(self, tmp_path, good):
        _make_pack(tmp_path, "d", _valid_v1_domain("p", version=good))
        assert "p" in load_registry(str(tmp_path))


class TestGapTypeMappingsHardening:
    def test_non_object_element_rejected(self, tmp_path):
        _make_pack(tmp_path, "d", _valid_v1_domain("p", gap_type_mappings=["not-an-object"]))
        with pytest.raises(RegistryLoadError):
            load_registry(str(tmp_path))

    def test_missing_gap_type_id_rejected(self, tmp_path):
        _make_pack(tmp_path, "d", _valid_v1_domain("p", gap_type_mappings=[{"domain_label": "x"}]))
        with pytest.raises(RegistryLoadError):
            load_registry(str(tmp_path))

    def test_malformed_question_rejected(self, tmp_path):
        bad = [{"gap_type_id": "G", "questions": [{"question_id": "q"}]}]  # missing text
        _make_pack(tmp_path, "d", _valid_v1_domain("p", gap_type_mappings=bad))
        with pytest.raises(RegistryLoadError):
            load_registry(str(tmp_path))

    def test_wellformed_mapping_with_questions_accepted(self, tmp_path):
        ok = [{"gap_type_id": "G", "questions": [{"question_id": "q", "text": "Ask?"}]}]
        _make_pack(tmp_path, "d", _valid_v1_domain("p", gap_type_mappings=ok))
        assert "p" in load_registry(str(tmp_path))


class TestRuleNuancesHardening:
    def test_non_object_element_rejected(self, tmp_path):
        _make_pack(tmp_path, "d", _valid_v1_domain("p", rule_nuances=["not-an-object"]))
        with pytest.raises(RegistryLoadError):
            load_registry(str(tmp_path))

    def test_minimal_object_element_still_accepted(self, tmp_path):
        # modifier_value is NOT frozen (the governed minimal pack omits it).
        _make_pack(tmp_path, "d", _valid_v1_domain("p", rule_nuances=[{"rule_id": "R"}]))
        assert "p" in load_registry(str(tmp_path))


class TestPackIdCollision:
    def test_duplicate_pack_id_rejected(self, tmp_path):
        _make_pack(tmp_path, "dir_a", _valid_v1_domain("same_id"))
        _make_pack(tmp_path, "dir_b", _valid_v1_domain("same_id"))
        with pytest.raises(RegistryLoadError):
            load_registry(str(tmp_path))


class TestAliasCollision:
    def test_same_alias_two_packs_rejected(self, tmp_path):
        _make_pack(tmp_path, "dir_a", _valid_v1_domain("pack_a", aliases=["shared_alias"]))
        _make_pack(tmp_path, "dir_b", _valid_v1_domain("pack_b", aliases=["shared_alias"]))
        with pytest.raises(RegistryLoadError):
            load_registry(str(tmp_path))

    def test_alias_colliding_with_other_pack_id_rejected(self, tmp_path):
        _make_pack(tmp_path, "dir_a", _valid_v1_domain("pack_a"))
        _make_pack(tmp_path, "dir_b", _valid_v1_domain("pack_b", aliases=["pack_a"]))
        with pytest.raises(RegistryLoadError):
            load_registry(str(tmp_path))

    def test_self_alias_allowed(self, tmp_path):
        _make_pack(tmp_path, "dir_a", _valid_v1_domain("pack_a", aliases=["pack_a", "pa"]))
        assert "pack_a" in load_registry(str(tmp_path))

    def test_unique_aliases_accepted(self, tmp_path):
        _make_pack(tmp_path, "dir_a", _valid_v1_domain("pack_a", aliases=["a1"]))
        _make_pack(tmp_path, "dir_b", _valid_v1_domain("pack_b", aliases=["b1"]))
        reg = load_registry(str(tmp_path))
        assert "pack_a" in reg and "pack_b" in reg


class TestProvenanceCoverage:
    def test_pack_without_provenance_rejected_when_manifest_present(self, tmp_path):
        _make_pack(tmp_path, "d", _valid_v1_domain("covered"))
        _make_pack(tmp_path, "e", _valid_v1_domain("uncovered"))
        _write_provenance(tmp_path, ["covered"])  # uncovered has no record
        with pytest.raises(RegistryLoadError):
            load_registry(str(tmp_path))

    def test_all_covered_accepted(self, tmp_path):
        _make_pack(tmp_path, "d", _valid_v1_domain("covered"))
        _write_provenance(tmp_path, ["covered"])
        assert "covered" in load_registry(str(tmp_path))

    def test_no_manifest_soft_gates_coverage(self, tmp_path):
        # Isolated unit dirs (no provenance manifest) still load — back-compat.
        _make_pack(tmp_path, "d", _valid_v1_domain("p"))
        assert "p" in load_registry(str(tmp_path))


# --- GREEN scope guards: real registry + legacy IoT unchanged --------------

class TestRealRegistryUnchanged:
    def test_real_registry_still_four_packs(self):
        reg = load_registry(_repo_domains_dir())
        assert list_domains(reg) == sorted(
            ["electronics_electrical", "mechanical", "medical_device", "software"]
        )

    def test_legacy_iot_still_skipped(self):
        reg = load_registry(_repo_domains_dir())
        assert "iot_electronics" not in reg

    def test_electronics_status_unchanged(self):
        reg = load_registry(_repo_domains_dir())
        assert reg["electronics_electrical"]["status"] == "active"
