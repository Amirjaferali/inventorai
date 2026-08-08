"""
tests/test_s5_i2_domain_activation.py

§5-I2 — Activation-status policy + explicit unsupported-domain model, governed by
the accepted §5-C1 contract-of-record (D-S5-03: pack lifecycle status is separate
from runtime/user activation; REGISTERED != USER-ACTIVE) and building on the §5-I1
hardened Domain Registry.

Foundation only. These tests encode the missing §5-I2 semantics — an explicit,
deterministic, registry-compatible support-state classification with three states:

  * ACTIVATED
  * RECOGNIZED_NOT_ACTIVATED
  * UNKNOWN_OR_UNSUPPORTED

RED (base 4770244): `engine.domain_activation` does not exist, so the missing
activation-truth API cannot classify these cases. GREEN: the policy classifies them
deterministically using the canonical registry and an explicit activation allowlist
that is SEPARATE from pack status. No new domain is activated (electronics only).
"""

import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from engine.domain_registry import load_registry
from engine import domain_activation as da


def _repo_registry():
    return load_registry(os.path.join(os.path.dirname(__file__), "..", "domains"))


# --- Support-state classification against the real registry -----------------

class TestRealRegistrySupportState:
    def test_electronics_is_activated(self):
        assert da.support_state("electronics_electrical", _repo_registry()) == da.ACTIVATED
        assert da.is_activated("electronics_electrical", _repo_registry()) is True

    @pytest.mark.parametrize("pack_id", ["mechanical", "medical_device", "software"])
    def test_recognized_non_electronics_not_activated(self, pack_id):
        st = da.support_state(pack_id, _repo_registry())
        assert st == da.RECOGNIZED_NOT_ACTIVATED
        assert da.is_activated(pack_id, _repo_registry()) is False

    def test_recognized_not_activated_is_distinct_from_unknown(self):
        reg = _repo_registry()
        assert da.support_state("mechanical", reg) != da.support_state("banana", reg)

    @pytest.mark.parametrize("unknown", ["banana", "drone", "", "   ", None])
    def test_unknown_or_missing_is_unsupported(self, unknown):
        assert da.support_state(unknown, _repo_registry()) == da.UNKNOWN_OR_UNSUPPORTED
        assert da.is_activated(unknown, _repo_registry()) is False

    def test_unknown_never_becomes_electronics(self):
        assert da.support_state("banana", _repo_registry()) != da.ACTIVATED


class TestAliasesRespectActivationPolicy:
    @pytest.mark.parametrize("alias", ["electronics", "electrical"])
    def test_activated_domain_aliases_are_activated(self, alias):
        # Aliases of an ACTIVATED domain resolve to ACTIVATED (recognition-only
        # resolution; the alias still maps to the activated canonical pack).
        assert da.support_state(alias, _repo_registry()) == da.ACTIVATED

    @pytest.mark.parametrize("alias", ["medical"])
    def test_non_activated_domain_alias_cannot_bypass_activation(self, alias):
        # An alias of a RECOGNIZED-but-NOT-ACTIVATED domain must NOT become activated.
        assert da.support_state(alias, _repo_registry()) == da.RECOGNIZED_NOT_ACTIVATED
        assert da.is_activated(alias, _repo_registry()) is False


# --- Pack status must NOT imply runtime activation (D-S5-03) -----------------

def _pack(pack_id, status="active", aliases=None):
    return {
        "schema_version": "1.0",
        "pack_id": pack_id,
        "version": "1.0",
        "status": status,
        "display_name": pack_id,
        "classification_signals": [{"signal": "s"}],
        "substance_signals": [{"signal": "s"}],
        "gap_type_mappings": [{"gap_type_id": "G"}],
        "rule_nuances": [{"rule_id": "R"}],
        **({"aliases": aliases} if aliases is not None else {}),
    }


def _synthetic_registry(tmp_path, packs):
    for i, p in enumerate(packs):
        d = tmp_path / f"dir_{i}"
        d.mkdir()
        (d / "domain.json").write_text(json.dumps(p), encoding="utf-8")
    # provenance manifest covering all packs (soft-gate satisfied)
    (tmp_path / "domain_provenance.json").write_text(
        json.dumps({"schema_version": "1.0",
                    "records": [{"record_id": f"{p['pack_id']}:PR001",
                                 "pack_id": p["pack_id"]} for p in packs]}),
        encoding="utf-8",
    )
    return load_registry(str(tmp_path))


class TestPackStatusIsNotActivation:
    def test_status_active_non_electronics_pack_not_activated(self, tmp_path):
        reg = _synthetic_registry(tmp_path, [_pack("widgets", status="active")])
        assert da.support_state("widgets", reg) == da.RECOGNIZED_NOT_ACTIVATED
        assert da.is_activated("widgets", reg) is False

    def test_registered_status_non_electronics_pack_not_activated(self, tmp_path):
        reg = _synthetic_registry(tmp_path, [_pack("gizmos", status="registered")])
        assert da.support_state("gizmos", reg) == da.RECOGNIZED_NOT_ACTIVATED

    def test_pack_loading_does_not_grant_activation(self, tmp_path):
        # A freshly-loaded valid pack is RECOGNIZED, never ACTIVATED, unless it is
        # on the explicit activation allowlist.
        reg = _synthetic_registry(tmp_path, [_pack("newthing")])
        assert da.support_state("newthing", reg) != da.ACTIVATED


class TestActivationAllowlist:
    def test_only_electronics_is_activated(self):
        assert da.activated_domains() == ["electronics_electrical"]

    def test_activated_domains_is_a_bounded_set(self):
        # Guard against accidental fifth activation.
        assert len(da.activated_domains()) == 1


# --- §5-I2 completion: activated_domains registry cross-check (ACTIVATED ⊆ RECOGNIZED) ---

class TestActivatedSubsetOfRecognized:
    def test_activated_domains_excludes_unrecognized_allowlist_id(self, monkeypatch):
        # An allowlisted id that is NOT canonically recognized must never be
        # reported by activated_domains() (drift wrinkle: ACTIVATED must ⊆ RECOGNIZED).
        monkeypatch.setattr(da, "_ACTIVATED_DOMAINS",
                            frozenset({"electronics_electrical", "ghost_domain"}))
        result = da.activated_domains()
        assert "ghost_domain" not in result
        assert "electronics_electrical" in result

    def test_activated_subset_of_recognized_real_registry(self):
        reg = _repo_registry()
        for d in da.activated_domains(reg):
            assert da._resolve_pack_id(d, reg) is not None

    def test_activated_domains_empty_when_registry_lacks_activated(self, tmp_path):
        # If the canonical activated domain is absent from a registry, it is not
        # reported as activated for that registry.
        reg = _synthetic_registry(tmp_path, [_pack("unrelated")])
        assert da.activated_domains(reg) == []


# --- §5-I2 completion: default-load (registry=None) production path ----------

class TestDefaultLoadPath:
    def test_default_path_electronics_activated(self):
        assert da.support_state("electronics_electrical") == da.ACTIVATED
        assert da.is_activated("electronics_electrical") is True

    def test_default_path_known_non_electronics_not_activated(self):
        assert da.support_state("mechanical") == da.RECOGNIZED_NOT_ACTIVATED

    def test_default_path_activated_domains(self):
        assert da.activated_domains() == ["electronics_electrical"]


# --- §5-I2 completion: web specialist admission bound to the engine policy ----

class TestWebActivationBinding:
    def test_web_admission_helper_accepts_activated_domain(self):
        import web.app as appmod
        assert appmod._admit_specialist_domain("electronics_electrical") == "electronics_electrical"

    def test_web_admission_helper_refuses_recognized_not_activated(self):
        # Specific error type so a missing helper (AttributeError) cannot false-pass.
        import web.app as appmod
        with pytest.raises(appmod.DomainNotActivatedError):
            appmod._admit_specialist_domain("mechanical")

    def test_web_admission_helper_refuses_unknown(self):
        import web.app as appmod
        with pytest.raises(appmod.DomainNotActivatedError):
            appmod._admit_specialist_domain("banana")

    def test_web_admission_bound_to_policy_under_deactivation(self, monkeypatch):
        # Drift guard: if the engine policy no longer activates electronics, the web
        # specialist-admission helper must NOT independently admit it.
        import web.app as appmod
        monkeypatch.setattr(da, "_ACTIVATED_DOMAINS", frozenset())
        with pytest.raises(appmod.DomainNotActivatedError):
            appmod._admit_specialist_domain("electronics_electrical")

    def test_web_confirm_value_is_policy_activated(self):
        # The domain the /start consent gate admits must be ACTIVATED by the policy.
        import web.app as appmod
        assert da.is_activated(appmod.DOMAIN_CONFIRM_VALUE) is True

    def test_web_conflicting_domains_are_recognized_not_activated(self):
        # The web classifier's conflicting-supported set must resolve as recognized
        # but NOT activated under the engine policy.
        import web.app as appmod
        reg = _repo_registry()
        for d in appmod.CONFLICTING_SUPPORTED_DOMAINS:
            assert da.support_state(d, reg) == da.RECOGNIZED_NOT_ACTIVATED
