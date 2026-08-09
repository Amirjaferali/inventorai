"""P8-I1 — Plan & Entitlement Foundation (RED → GREEN).

Behavioral tests for the accepted bounded P8-I1 contract
(`docs/governance/PHASE_8_I1_PLAN_ENTITLEMENT_FOUNDATION_INCREMENT_CONTRACT.md`,
PR #417). Provider-neutral commercial identity + entitlement foundation:

    Account → Commercial Plan Identity → Entitlement Evaluation
            → Governed Capability Access   (WITHOUT payment processing)

The proof is fail-closed, plan-neutral (OD-N), derived-not-snapshot, and uses a
neutral INTERNAL capability seam only — no real user-facing paywall, no marketed
plan names, no lifecycle/quota/provider/UI. SQLite files live only in tmp_path.

On the pre-implementation base these tests are RED because
``engine.plan_catalog``, ``engine.entitlement_service`` and the account-store
``commercial_assignments`` methods do not exist.
"""
import ast
import os

import pytest

from engine.account_store import SqliteAccountStore
from engine import domain_activation

# Modules under test — absent on the base → genuine RED (import error).
from engine import plan_catalog
from engine import entitlement_service as ent


_NOW = "2026-01-01T00:00:00Z"


def _store(tmp_path, name="p8i1.sqlite3"):
    return SqliteAccountStore(str(tmp_path / name))


def _account(store, account_id="acct_1", status="active"):
    store.create_account(account_id, account_id + "@ex.test", "scrypt$dummyhash",
                         _NOW, status=status)
    return account_id


def _proof_cap():
    return plan_catalog.CAPABILITY_INTERNAL_PROOF


# 1 — Legacy/default absence: active account, no assignment → technical default.
def test_legacy_active_account_no_assignment_resolves_to_technical_default(tmp_path):
    s = _store(tmp_path)
    acct = _account(s)
    assert s.get_commercial_assignment(acct) is None          # legitimate absence
    d = ent.evaluate_entitlement(s, acct, _proof_cap())
    assert d.allow is True                                     # NOT an error
    assert d.plan_identity == plan_catalog.default_plan_identity()


# 2 — Valid explicit assignment → deterministic derived entitlement (both ways).
def test_valid_assignment_derives_deterministic_entitlement(tmp_path):
    s = _store(tmp_path)
    acct = _account(s)
    s.set_commercial_assignment(acct, *plan_catalog.default_plan_identity(), _NOW)
    assert ent.evaluate_entitlement(s, acct, _proof_cap()).allow is True
    s.set_commercial_assignment(acct, *plan_catalog.RESTRICTED_TECHNICAL_PLAN, _NOW)
    d = ent.evaluate_entitlement(s, acct, _proof_cap())
    assert d.allow is False                                    # differentiated, deterministic
    assert d.plan_identity == plan_catalog.RESTRICTED_TECHNICAL_PLAN


# 3 — Unknown explicit plan reference → fail closed.
def test_unknown_plan_reference_fails_closed(tmp_path):
    s = _store(tmp_path)
    acct = _account(s)
    s.set_commercial_assignment(acct, "no_such_plan", "9", _NOW)
    with pytest.raises(ent.EntitlementError):
        ent.evaluate_entitlement(s, acct, _proof_cap())


# 4 — Malformed commercial assignment → fail closed.
def test_malformed_assignment_fails_closed(tmp_path):
    s = _store(tmp_path)
    acct = _account(s)
    s.set_commercial_assignment(acct, "", "", _NOW)            # empty identity = malformed
    with pytest.raises(ent.EntitlementError):
        ent.evaluate_entitlement(s, acct, _proof_cap())


# 5 — Catalog/descriptor failure → fail closed.
def test_catalog_descriptor_failure_fails_closed(tmp_path, monkeypatch):
    s = _store(tmp_path)
    acct = _account(s)
    s.set_commercial_assignment(acct, *plan_catalog.default_plan_identity(), _NOW)
    # Corrupt the catalog descriptor for the assigned plan (non-dict).
    bad = dict(plan_catalog._CATALOG)
    bad[plan_catalog.default_plan_identity()] = "not-a-descriptor"
    monkeypatch.setattr(plan_catalog, "_CATALOG", bad)
    with pytest.raises(ent.EntitlementError):
        ent.evaluate_entitlement(s, acct, _proof_cap())


# 6 — Missing/nonexistent account → fail closed AND NOT defaulted.
def test_missing_account_fails_closed_and_not_defaulted(tmp_path):
    s = _store(tmp_path)
    with pytest.raises(ent.EntitlementError):
        ent.evaluate_entitlement(s, "ghost_account", _proof_cap())


# 7 — Disabled/deleted account → fail closed (existing Phase-5 semantics).
@pytest.mark.parametrize("status", ["disabled", "deleted"])
def test_non_active_account_fails_closed(tmp_path, status):
    s = _store(tmp_path)
    acct = _account(s)
    s.set_commercial_assignment(acct, *plan_catalog.default_plan_identity(), _NOW)
    s.set_status(acct, status, _NOW)
    with pytest.raises(ent.EntitlementError):
        ent.evaluate_entitlement(s, acct, _proof_cap())


# 8 — Derived-not-snapshot: catalog change alters effective entitlement with NO
#     per-account rewrite.
def test_effective_entitlement_is_derived_not_snapshot(tmp_path, monkeypatch):
    s = _store(tmp_path)
    acct = _account(s)
    s.set_commercial_assignment(acct, *plan_catalog.default_plan_identity(), _NOW)
    before_row = s.get_commercial_assignment(acct)
    assert ent.evaluate_entitlement(s, acct, _proof_cap()).allow is True
    # Change the reviewed catalog definition (deny the capability) — no DB write.
    patched = dict(plan_catalog._CATALOG)
    patched[plan_catalog.default_plan_identity()] = {_proof_cap(): False}
    monkeypatch.setattr(plan_catalog, "_CATALOG", patched)
    assert ent.evaluate_entitlement(s, acct, _proof_cap()).allow is False
    after_row = s.get_commercial_assignment(acct)
    assert after_row == before_row                            # no per-account entitlement rewrite


# 9 — Governed capability answered via the canonical seam; the neutral internal
#     capability/plan identifiers do not leak into non-commercial engine modules.
def test_capability_via_canonical_seam_no_leak_of_internal_identifiers():
    d = ent.evaluate_entitlement.__module__
    assert d == "engine.entitlement_service"                  # single canonical seam
    commercial_files = {"engine/plan_catalog.py", "engine/entitlement_service.py"}
    literals = (plan_catalog.TECHNICAL_DEFAULT_PLAN_ID,
                plan_catalog.CAPABILITY_INTERNAL_PROOF)
    engine_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "engine")
    for fn in os.listdir(engine_dir):
        if not fn.endswith(".py"):
            continue
        rel = "engine/" + fn
        if rel in commercial_files:
            continue
        text = open(os.path.join(engine_dir, fn), encoding="utf-8").read()
        for lit in literals:
            assert lit not in text, "%s leaks internal commercial identifier" % rel


# 10 — OD-N behavioral neutrality: identical technical inputs under differing
#      commercial identities → identical technical evaluation.
def test_od_n_behavioral_technical_truth_is_plan_neutral(tmp_path):
    s = _store(tmp_path)
    acct = _account(s)
    baseline = domain_activation.support_state("electronics_electrical")
    s.set_commercial_assignment(acct, *plan_catalog.default_plan_identity(), _NOW)
    under_default = domain_activation.support_state("electronics_electrical")
    s.set_commercial_assignment(acct, *plan_catalog.RESTRICTED_TECHNICAL_PLAN, _NOW)
    under_restricted = domain_activation.support_state("electronics_electrical")
    assert baseline == under_default == under_restricted


# 11 — OD-N engine-wide inverted-allowlist static import guard.
def test_od_n_engine_wide_no_commercial_imports_outside_allowlist():
    # Commercial seams permitted to import the commercial layer. Extended by
    # P8-I2 to include the quota_service seam (which consumes entitlement_service
    # + plan_catalog); the deterministic core still imports none of them.
    allowlist = {"entitlement_service", "quota_service"}
    commercial = {"plan_catalog", "entitlement_service", "quota_service"}
    engine_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "engine")
    offenders = []
    for fn in os.listdir(engine_dir):
        if not fn.endswith(".py"):
            continue
        modname = fn[:-3]
        if modname in allowlist:
            continue
        tree = ast.parse(open(os.path.join(engine_dir, fn), encoding="utf-8").read())
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for a in node.names:
                    imported.add(a.name.split(".")[-1])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imported.add(node.module.split(".")[-1])
                for a in node.names:
                    imported.add(a.name)
        leaked = imported & commercial
        if leaked:
            offenders.append((fn, sorted(leaked)))
    assert offenders == [], "commercial imports leaked into engine core: %r" % offenders


# 12 — Atomic assignment + commercial audit: a failure rolls back BOTH (no
#      partial/unaudited mutation).
def test_assignment_and_audit_are_atomic(tmp_path, monkeypatch):
    s = _store(tmp_path)
    acct = _account(s)

    def boom(*a, **k):
        raise RuntimeError("forced audit failure")

    monkeypatch.setattr(s, "_append_commercial_audit", boom)
    with pytest.raises(RuntimeError):
        s.set_commercial_assignment(acct, *plan_catalog.default_plan_identity(), _NOW)
    assert s.get_commercial_assignment(acct) is None          # assignment rolled back
    assert s.list_commercial_audit(acct) == []                # no unaudited/partial mutation


# 12b — Successful assignment writes exactly one atomic audit event.
def test_successful_assignment_writes_audit(tmp_path):
    s = _store(tmp_path)
    acct = _account(s)
    s.set_commercial_assignment(acct, *plan_catalog.default_plan_identity(), _NOW)
    audit = s.list_commercial_audit(acct)
    assert len(audit) == 1 and audit[0]["event_type"] == "assigned"


# 13 — Additive migration on an existing DB: reopening leaves data intact and the
#      commercial tables present.
def test_existing_db_additive_migration_preserves_data(tmp_path):
    path = str(tmp_path / "existing.sqlite3")
    s1 = SqliteAccountStore(path)
    s1.create_account("acct_x", "acct_x@ex.test", "scrypt$h", _NOW)
    s1.set_commercial_assignment("acct_x", *plan_catalog.default_plan_identity(), _NOW)
    # Reopen (idempotent schema) — existing account + assignment untouched.
    s2 = SqliteAccountStore(path)
    assert s2.get_account_by_id("acct_x")["status"] == "active"
    assert s2.get_commercial_assignment("acct_x")["plan_id"] == \
        plan_catalog.TECHNICAL_DEFAULT_PLAN_ID


# 14 — Fresh DB initializes the commercial tables.
def test_fresh_db_has_commercial_tables(tmp_path):
    s = _store(tmp_path, "fresh.sqlite3")
    # Absent-assignment lookup succeeds (table exists) and returns None.
    assert s.get_commercial_assignment("nobody") is None
    assert s.list_commercial_audit("nobody") == []


# 15 — Ownership/auth semantics unchanged; commercial identity is orthogonal to
#      account/credential state (credential revocation stays plan-independent).
def test_commercial_assignment_does_not_touch_account_or_auth_state(tmp_path):
    s = _store(tmp_path)
    acct = _account(s)
    before = s.get_account_by_id(acct)
    s.set_commercial_assignment(acct, *plan_catalog.RESTRICTED_TECHNICAL_PLAN, _NOW)
    after = s.get_account_by_id(acct)
    assert after == before                                    # status/epoch/verification unchanged
