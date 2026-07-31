"""
tests/test_domain_registry.py
Domain Registry Tests — reconciled to the governed Domain Registry v1.0 contract.

These tests are aligned with the currently implemented and closed Domain
Registry v1.0 architecture (as shipped in ``engine/domain_registry.py`` and
wired through ``engine/domain_rules.py``):
  * registry entries are keyed by ``pack_id``;
  * only packs with ``schema_version == "1.0"`` are loaded;
  * validation is performed through ``_validate_domain_v1``;
  * runtime authority is the ``engine/domain_rules.py`` -> ``load_registry("domains/")`` wiring;
  * the legacy ``capability_id``-keyed contract and legacy ``governance{}`` validation
    model are retired and are NOT authoritative.

``iot_electronics`` remains a latent legacy pack (``schema_version == None``): it is
skipped by the loader, not activated, and is not asserted as loadable here.

V1.0 VALIDATION GAPS — PRESERVED, NOT FIXED
-------------------------------------------
This reconciliation is test-only and asserts exactly the behavior that
``_validate_domain_v1`` currently enforces. It does NOT claim that the following
safeguards are implemented, and does NOT invent tests asserting them:
  * format validation for ``version``;
  * validation of ``activated_date``, ``deprecated_date``, and ``schema_date``;
  * allowed-value validation for ``status``;
  * rejection of empty ``classification_signals``;
  * rejection of empty ``substance_signals``;
  * type and completeness validation for ``gap_type_mappings``;
  * type and completeness validation for ``rule_nuances``;
  * provenance or governance-metadata validation.

These are genuine v1.0 hardening gaps. They are NOT silently considered resolved;
they are outside this test-only reconciliation; and they require a separately
authorized production-validation increment (which would modify
``_validate_domain_v1``). This file must not assert behavior not currently
enforced by the loader.
"""

import json
import os
import sys
import pytest
from types import MappingProxyType

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from engine.domain_registry import (
    load_registry, get_domain, list_domains,
    RegistryLoadError, DomainNotFoundError,
)

# A real, active v1.0 pack shipped in domains/ (keyed by pack_id).
KNOWN_ACTIVE_PACK_ID = "electronics_electrical"

# v1.0 required top-level fields, per engine.domain_registry._validate_domain_v1.
V1_REQUIRED_FIELDS = (
    "schema_version", "pack_id", "version", "status",
    "display_name", "classification_signals", "substance_signals",
    "gap_type_mappings", "rule_nuances",
)


def _make_domain_dir(tmp_path, subdir_name, data):
    domain_dir = tmp_path / subdir_name
    domain_dir.mkdir()
    (domain_dir / "domain.json").write_text(json.dumps(data), encoding="utf-8")
    return tmp_path


def _valid_v1_domain(pack_id="test_pack"):
    """A minimal domain pack that satisfies the governed v1.0 contract."""
    return {
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


def _legacy_domain(capability_id="legacy_pack"):
    """A legacy (pre-v1.0) pack shaped like domains/iot_electronics/domain.json.

    It has no ``schema_version`` and is therefore skipped by the v1.0 loader.
    """
    return {
        "taxonomy_group": "test_group",
        "capability_id": capability_id,
        "display_name": "Legacy Pack",
        "description": "A legacy-schema domain used for testing.",
        "domain_signals": ["signal_a", "signal_b"],
        "gaps": ["GAP_ONE", "GAP_TWO"],
        "notes": "Legacy notes.",
        "governance": {
            "source": "test source",
            "license": "proprietary",
            "owner": "test-owner",
            "review_date": "2025-01-01",
            "version": "1.0.0",
            "deprecation_status": "active",
        },
    }


def _repo_root():
    return os.path.join(os.path.dirname(__file__), "..")


def _domains_dir():
    return os.path.join(_repo_root(), "domains")


class TestLoadValidV1Domain:
    def test_load_real_active_pack(self):
        registry = load_registry(_domains_dir())
        assert KNOWN_ACTIVE_PACK_ID in registry

    def test_registry_is_mapping_proxy(self):
        registry = load_registry(_domains_dir())
        assert isinstance(registry, MappingProxyType)

    def test_registry_is_immutable(self):
        registry = load_registry(_domains_dir())
        with pytest.raises(TypeError):
            registry["new_key"] = {}

    def test_registry_keyed_by_pack_id(self, tmp_path):
        _make_domain_dir(tmp_path, "some_dir", _valid_v1_domain("my_pack"))
        registry = load_registry(str(tmp_path))
        assert "my_pack" in registry

    def test_domain_contains_expected_v1_keys(self):
        registry = load_registry(_domains_dir())
        domain = registry[KNOWN_ACTIVE_PACK_ID]
        for key in V1_REQUIRED_FIELDS:
            assert key in domain, f"Missing key: {key}"

    def test_loaded_pack_has_governed_status_and_version(self):
        registry = load_registry(_domains_dir())
        pack = registry[KNOWN_ACTIVE_PACK_ID]
        assert pack["status"] == "active"
        assert pack["version"]


class TestRealRegistryLatencyGuard:
    # Read-only regression against the real domains/ directory. Its purpose is to
    # make accidental fifth-domain activation visible as a failing test that
    # requires an explicit owner decision. No domain JSON is modified.
    EXPECTED_ACTIVE_PACKS = [
        "electronics_electrical",
        "mechanical",
        "medical_device",
        "software",
    ]

    def test_iot_electronics_not_loaded(self):
        registry = load_registry(_domains_dir())
        assert "iot_electronics" not in registry

    def test_real_registry_has_exactly_four_active_packs(self):
        registry = load_registry(_domains_dir())
        assert list_domains(registry) == sorted(self.EXPECTED_ACTIVE_PACKS)


class TestListDomains:
    def test_list_domains_returns_list(self, tmp_path):
        _make_domain_dir(tmp_path, "alpha", _valid_v1_domain("alpha"))
        registry = load_registry(str(tmp_path))
        assert isinstance(list_domains(registry), list)

    def test_list_domains_sorted(self, tmp_path):
        _make_domain_dir(tmp_path, "zebra", _valid_v1_domain("zebra"))
        _make_domain_dir(tmp_path, "alpha", _valid_v1_domain("alpha"))
        _make_domain_dir(tmp_path, "middle", _valid_v1_domain("middle"))
        registry = load_registry(str(tmp_path))
        result = list_domains(registry)
        assert result == sorted(result)

    def test_list_domains_contains_known_domain(self):
        registry = load_registry(_domains_dir())
        assert KNOWN_ACTIVE_PACK_ID in list_domains(registry)


class TestGetDomain:
    def test_get_domain_returns_dict(self, tmp_path):
        _make_domain_dir(tmp_path, "test_domain", _valid_v1_domain("test_pack"))
        registry = load_registry(str(tmp_path))
        assert isinstance(get_domain(registry, "test_pack"), dict)

    def test_get_domain_correct_content(self, tmp_path):
        _make_domain_dir(tmp_path, "my_domain", _valid_v1_domain("my_pack"))
        registry = load_registry(str(tmp_path))
        result = get_domain(registry, "my_pack")
        assert result["pack_id"] == "my_pack"

    def test_get_domain_missing_raises(self, tmp_path):
        _make_domain_dir(tmp_path, "test_domain", _valid_v1_domain("test_pack"))
        registry = load_registry(str(tmp_path))
        with pytest.raises(DomainNotFoundError):
            get_domain(registry, "nonexistent_pack")


class TestDeterministicLoading:
    def test_load_registry_is_repeatable(self, tmp_path):
        _make_domain_dir(tmp_path, "test_domain", _valid_v1_domain("test_pack"))
        r1 = load_registry(str(tmp_path))
        r2 = load_registry(str(tmp_path))
        assert dict(r1) == dict(r2)

    def test_load_order_is_sorted(self, tmp_path):
        _make_domain_dir(tmp_path, "zzz_dir", _valid_v1_domain("zzz_pack"))
        _make_domain_dir(tmp_path, "aaa_dir", _valid_v1_domain("aaa_pack"))
        registry = load_registry(str(tmp_path))
        assert list_domains(registry) == ["aaa_pack", "zzz_pack"]

    def test_subdir_without_domain_json_is_skipped(self, tmp_path):
        (tmp_path / "empty_subdir").mkdir()
        _make_domain_dir(tmp_path, "valid_dir", _valid_v1_domain("valid_pack"))
        registry = load_registry(str(tmp_path))
        assert "valid_pack" in registry
        assert len(registry) == 1


class TestSchemaVersionGate:
    def test_non_v1_schema_pack_is_skipped(self, tmp_path):
        data = _valid_v1_domain("old_pack")
        data["schema_version"] = "0.9"
        _make_domain_dir(tmp_path, "old_dir", data)
        registry = load_registry(str(tmp_path))
        assert "old_pack" not in registry
        assert len(registry) == 0

    def test_missing_schema_version_pack_is_skipped(self, tmp_path):
        data = _valid_v1_domain("no_schema_pack")
        del data["schema_version"]
        _make_domain_dir(tmp_path, "no_schema_dir", data)
        registry = load_registry(str(tmp_path))
        assert len(registry) == 0

    def test_legacy_capability_id_pack_is_skipped(self, tmp_path):
        # Mirrors domains/iot_electronics/domain.json: a legacy pack (no
        # schema_version) is skipped by the v1.0 loader — latent, not activated.
        _make_domain_dir(tmp_path, "iot_like_dir", _legacy_domain("iot_electronics"))
        registry = load_registry(str(tmp_path))
        assert "iot_electronics" not in registry
        assert len(registry) == 0


class TestV1RequiredFieldValidation:
    @pytest.mark.parametrize("missing_field", [
        "pack_id", "version", "status", "display_name",
        "classification_signals", "substance_signals",
        "gap_type_mappings", "rule_nuances",
    ])
    def test_missing_v1_required_field_raises(self, tmp_path, missing_field):
        data = _valid_v1_domain()
        del data[missing_field]
        _make_domain_dir(tmp_path, "bad_dir", data)
        with pytest.raises(RegistryLoadError, match=missing_field):
            load_registry(str(tmp_path))


class TestV1ValueValidation:
    def test_empty_pack_id_raises(self, tmp_path):
        data = _valid_v1_domain()
        data["pack_id"] = "   "
        _make_domain_dir(tmp_path, "bad_dir", data)
        with pytest.raises(RegistryLoadError, match="pack_id"):
            load_registry(str(tmp_path))

    def test_non_list_classification_signals_raises(self, tmp_path):
        data = _valid_v1_domain()
        data["classification_signals"] = "not_a_list"
        _make_domain_dir(tmp_path, "bad_dir", data)
        with pytest.raises(RegistryLoadError, match="classification_signals"):
            load_registry(str(tmp_path))

    def test_non_list_substance_signals_raises(self, tmp_path):
        data = _valid_v1_domain()
        data["substance_signals"] = "not_a_list"
        _make_domain_dir(tmp_path, "bad_dir", data)
        with pytest.raises(RegistryLoadError, match="substance_signals"):
            load_registry(str(tmp_path))

    # --- v1.0 validation hardening (owner-approved: A1, A1, B1-LIMITED, B1-LIMITED) ---

    def test_empty_classification_signals_raises(self, tmp_path):
        # A1: classification_signals must be a NON-EMPTY list.
        data = _valid_v1_domain()
        data["classification_signals"] = []
        _make_domain_dir(tmp_path, "bad_dir", data)
        with pytest.raises(RegistryLoadError, match="classification_signals"):
            load_registry(str(tmp_path))

    def test_empty_substance_signals_raises(self, tmp_path):
        # A1: substance_signals must be a NON-EMPTY list.
        data = _valid_v1_domain()
        data["substance_signals"] = []
        _make_domain_dir(tmp_path, "bad_dir", data)
        with pytest.raises(RegistryLoadError, match="substance_signals"):
            load_registry(str(tmp_path))

    def test_non_list_gap_type_mappings_raises(self, tmp_path):
        # B1-LIMITED: gap_type_mappings must be a list (non-emptiness deferred).
        data = _valid_v1_domain()
        data["gap_type_mappings"] = {"not": "a list"}
        _make_domain_dir(tmp_path, "bad_dir", data)
        with pytest.raises(RegistryLoadError, match="gap_type_mappings"):
            load_registry(str(tmp_path))

    def test_non_list_rule_nuances_raises(self, tmp_path):
        # B1-LIMITED: rule_nuances must be a list (non-emptiness deferred).
        data = _valid_v1_domain()
        data["rule_nuances"] = {"not": "a list"}
        _make_domain_dir(tmp_path, "bad_dir", data)
        with pytest.raises(RegistryLoadError, match="rule_nuances"):
            load_registry(str(tmp_path))

    def test_empty_gap_type_mappings_and_rule_nuances_are_accepted(self, tmp_path):
        # B1-LIMITED boundary: non-emptiness is DEFERRED, so empty lists load.
        data = _valid_v1_domain("boundary_pack")
        data["gap_type_mappings"] = []
        data["rule_nuances"] = []
        _make_domain_dir(tmp_path, "boundary_dir", data)
        registry = load_registry(str(tmp_path))
        assert "boundary_pack" in registry

    def test_invalid_json_raises(self, tmp_path):
        domain_dir = tmp_path / "bad_dir"
        domain_dir.mkdir()
        (domain_dir / "domain.json").write_text("{not valid json", encoding="utf-8")
        with pytest.raises(RegistryLoadError, match="Invalid JSON"):
            load_registry(str(tmp_path))

    def test_missing_domains_dir_raises(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            load_registry(str(tmp_path / "nonexistent_dir"))


class TestRuntimeIntegration:
    def test_domain_rules_loads_registry(self):
        # v1.0: domain_rules.py is the intentional integration point — it loads
        # the registry (AB-005 closed; registry is the runtime authority).
        path = os.path.join(_repo_root(), "engine", "domain_rules.py")
        with open(path, encoding="utf-8") as fh:
            content = fh.read()
        assert "domain_registry" in content
        assert "load_registry" in content

    def test_progression_loop_does_not_import_registry_directly(self):
        # Domain-registry integration is centralized in domain_rules.py;
        # progression_loop.py reaches domain behavior through that layer only.
        path = os.path.join(_repo_root(), "engine", "progression_loop.py")
        with open(path, encoding="utf-8") as fh:
            content = fh.read()
        assert "domain_registry" not in content

    def test_web_app_does_not_import_registry_directly(self):
        path = os.path.join(_repo_root(), "web", "app.py")
        with open(path, encoding="utf-8") as fh:
            content = fh.read()
        assert "domain_registry" not in content
