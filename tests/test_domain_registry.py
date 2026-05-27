"""
tests/test_domain_registry.py
Phase 5 Step 3 - Domain Registry Tests
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


def _make_domain_dir(tmp_path, subdir_name, data):
    domain_dir = tmp_path / subdir_name
    domain_dir.mkdir()
    (domain_dir / "domain.json").write_text(json.dumps(data), encoding="utf-8")
    return tmp_path


def _valid_domain(capability_id="test_domain"):
    return {
        "taxonomy_group": "test_group",
        "capability_id": capability_id,
        "display_name": "Test Domain",
        "description": "A domain used for testing.",
        "domain_signals": ["signal_a", "signal_b"],
        "gaps": ["GAP_ONE", "GAP_TWO"],
        "notes": "Test notes.",
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


class TestLoadValidDomain:
    def test_load_iot_electronics_domain(self):
        registry = load_registry(_domains_dir())
        assert "iot_electronics" in registry

    def test_registry_is_mapping_proxy(self):
        registry = load_registry(_domains_dir())
        assert isinstance(registry, MappingProxyType)

    def test_registry_is_immutable(self):
        registry = load_registry(_domains_dir())
        with pytest.raises(TypeError):
            registry["new_key"] = {}

    def test_registry_keyed_by_capability_id(self, tmp_path):
        _make_domain_dir(tmp_path, "some_dir", _valid_domain("my_capability"))
        registry = load_registry(str(tmp_path))
        assert "my_capability" in registry

    def test_domain_contains_expected_keys(self):
        registry = load_registry(_domains_dir())
        domain = registry["iot_electronics"]
        for key in ("taxonomy_group", "capability_id", "display_name",
                    "description", "domain_signals", "gaps", "notes", "governance"):
            assert key in domain, f"Missing key: {key}"

    def test_governance_contains_expected_keys(self):
        registry = load_registry(_domains_dir())
        gov = registry["iot_electronics"]["governance"]
        for key in ("source", "license", "owner",
                    "review_date", "version", "deprecation_status"):
            assert key in gov, f"Missing governance key: {key}"


class TestListDomains:
    def test_list_domains_returns_list(self, tmp_path):
        _make_domain_dir(tmp_path, "alpha", _valid_domain("alpha"))
        registry = load_registry(str(tmp_path))
        assert isinstance(list_domains(registry), list)

    def test_list_domains_sorted(self, tmp_path):
        _make_domain_dir(tmp_path, "zebra", _valid_domain("zebra"))
        _make_domain_dir(tmp_path, "alpha", _valid_domain("alpha"))
        _make_domain_dir(tmp_path, "middle", _valid_domain("middle"))
        registry = load_registry(str(tmp_path))
        result = list_domains(registry)
        assert result == sorted(result)

    def test_list_domains_contains_known_domain(self):
        registry = load_registry(_domains_dir())
        assert "iot_electronics" in list_domains(registry)


class TestGetDomain:
    def test_get_domain_returns_dict(self, tmp_path):
        _make_domain_dir(tmp_path, "test_domain", _valid_domain("test_domain"))
        registry = load_registry(str(tmp_path))
        assert isinstance(get_domain(registry, "test_domain"), dict)

    def test_get_domain_correct_content(self, tmp_path):
        _make_domain_dir(tmp_path, "my_domain", _valid_domain("my_domain"))
        registry = load_registry(str(tmp_path))
        result = get_domain(registry, "my_domain")
        assert result["capability_id"] == "my_domain"

    def test_get_domain_missing_raises(self, tmp_path):
        _make_domain_dir(tmp_path, "test_domain", _valid_domain("test_domain"))
        registry = load_registry(str(tmp_path))
        with pytest.raises(DomainNotFoundError):
            get_domain(registry, "nonexistent_domain")


class TestDeterministicLoading:
    def test_load_registry_is_repeatable(self, tmp_path):
        _make_domain_dir(tmp_path, "test_domain", _valid_domain("test_domain"))
        r1 = load_registry(str(tmp_path))
        r2 = load_registry(str(tmp_path))
        assert dict(r1) == dict(r2)

    def test_load_order_is_sorted(self, tmp_path):
        _make_domain_dir(tmp_path, "zzz_domain", _valid_domain("zzz_domain"))
        _make_domain_dir(tmp_path, "aaa_domain", _valid_domain("aaa_domain"))
        registry = load_registry(str(tmp_path))
        assert list_domains(registry) == ["aaa_domain", "zzz_domain"]

    def test_subdir_without_domain_json_is_skipped(self, tmp_path):
        (tmp_path / "empty_subdir").mkdir()
        _make_domain_dir(tmp_path, "valid_domain", _valid_domain("valid_domain"))
        registry = load_registry(str(tmp_path))
        assert "valid_domain" in registry
        assert len(registry) == 1


class TestMissingFieldValidation:
    @pytest.mark.parametrize("missing_field", [
        "taxonomy_group", "capability_id", "display_name",
        "description", "domain_signals", "gaps", "notes", "governance",
    ])
    def test_missing_top_level_field_raises(self, tmp_path, missing_field):
        data = _valid_domain()
        del data[missing_field]
        _make_domain_dir(tmp_path, "bad_domain", data)
        with pytest.raises(RegistryLoadError, match=missing_field):
            load_registry(str(tmp_path))

    @pytest.mark.parametrize("missing_field", [
        "source", "license", "owner",
        "review_date", "version", "deprecation_status",
    ])
    def test_missing_governance_field_raises(self, tmp_path, missing_field):
        data = _valid_domain()
        del data["governance"][missing_field]
        _make_domain_dir(tmp_path, "bad_domain", data)
        with pytest.raises(RegistryLoadError, match=missing_field):
            load_registry(str(tmp_path))


class TestInvalidValueValidation:
    def test_invalid_version_format_raises(self, tmp_path):
        data = _valid_domain()
        data["governance"]["version"] = "v1.0"
        _make_domain_dir(tmp_path, "bad_domain", data)
        with pytest.raises(RegistryLoadError, match="semver"):
            load_registry(str(tmp_path))

    def test_invalid_review_date_raises(self, tmp_path):
        data = _valid_domain()
        data["governance"]["review_date"] = "01-01-2025"
        _make_domain_dir(tmp_path, "bad_domain", data)
        with pytest.raises(RegistryLoadError, match="ISO-8601"):
            load_registry(str(tmp_path))

    def test_invalid_deprecation_status_raises(self, tmp_path):
        data = _valid_domain()
        data["governance"]["deprecation_status"] = "unknown_status"
        _make_domain_dir(tmp_path, "bad_domain", data)
        with pytest.raises(RegistryLoadError, match="deprecation_status"):
            load_registry(str(tmp_path))

    def test_empty_capability_id_raises(self, tmp_path):
        data = _valid_domain()
        data["capability_id"] = "   "
        _make_domain_dir(tmp_path, "bad_domain", data)
        with pytest.raises(RegistryLoadError, match="capability_id"):
            load_registry(str(tmp_path))

    def test_empty_domain_signals_raises(self, tmp_path):
        data = _valid_domain()
        data["domain_signals"] = []
        _make_domain_dir(tmp_path, "bad_domain", data)
        with pytest.raises(RegistryLoadError, match="domain_signals"):
            load_registry(str(tmp_path))

    def test_empty_gaps_raises(self, tmp_path):
        data = _valid_domain()
        data["gaps"] = []
        _make_domain_dir(tmp_path, "bad_domain", data)
        with pytest.raises(RegistryLoadError, match="gaps"):
            load_registry(str(tmp_path))

    def test_invalid_json_raises(self, tmp_path):
        domain_dir = tmp_path / "bad_domain"
        domain_dir.mkdir()
        (domain_dir / "domain.json").write_text("{not valid json", encoding="utf-8")
        with pytest.raises(RegistryLoadError, match="Invalid JSON"):
            load_registry(str(tmp_path))

    def test_missing_domains_dir_raises(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            load_registry(str(tmp_path / "nonexistent_dir"))

    def test_empty_governance_source_raises(self, tmp_path):
        data = _valid_domain()
        data["governance"]["source"] = ""
        _make_domain_dir(tmp_path, "bad_domain", data)
        with pytest.raises(RegistryLoadError, match="governance.source"):
            load_registry(str(tmp_path))


class TestRuntimeIsolation:
    def test_domain_rules_not_modified(self):
        path = os.path.join(_repo_root(), "engine", "domain_rules.py")
        with open(path, encoding="utf-8") as fh:
            content = fh.read()
        assert "domain_registry" not in content

    def test_progression_loop_not_modified(self):
        path = os.path.join(_repo_root(), "engine", "progression_loop.py")
        with open(path, encoding="utf-8") as fh:
            content = fh.read()
        assert "domain_registry" not in content

    def test_web_app_not_modified(self):
        path = os.path.join(_repo_root(), "web", "app.py")
        with open(path, encoding="utf-8") as fh:
            content = fh.read()
        assert "domain_registry" not in content
