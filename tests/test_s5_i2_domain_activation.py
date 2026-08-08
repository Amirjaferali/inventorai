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
