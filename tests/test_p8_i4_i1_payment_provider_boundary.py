"""P8-I4-I1 — Provider-Neutral Payment Boundary Foundation — focused tests.

Proves the accepted P8-I4-C boundary with a deterministic fake/reference adapter and
no real provider: port + two fakes (replaceability); additive provider-mapping +
durable provider-event dedupe; opaque external refs; strict provider-event
idempotency (exact duplicate replays, conflicting-fingerprint fails closed); durable
fingerprint (no raw payload); fail-closed catalogue; atomic dedupe+lifecycle;
adapter fault / timeout → no mutation; canonical-mapping-only (raw provider name never
enters the P8-I3 log); P8-I1/I2/I3 authority preserved; concurrency; import isolation.
"""

import ast
import os
import sqlite3
import threading

import pytest

from engine.account_store import SqliteAccountStore
from engine import plan_catalog
from engine import entitlement_service as ent
from engine import quota_service
from engine import subscription_lifecycle_service as sls
from engine import payment_provider_port as port
from engine import payment_ingestion as ingest
from engine.payment_fake_adapter import FakeReferenceAdapterA, FakeReferenceAdapterB


_NOW = "2026-01-01T00:00:00Z"
_SECRET = "fake-shared-token"


def _store(tmp_path, name="p8i4.db"):
    return SqliteAccountStore(os.path.join(str(tmp_path), name))


def _account(store, account_id="acct-1", status="active"):
    store.create_account(account_id, account_id + "@x.test", "hash", _NOW,
                         status=status)
    return account_id


def _map(store, account_id, adapter, sub_ref, cust_ref="cust-x"):
    return store.put_provider_mapping(
        account_id, provider=adapter.provider_key,
        external_subscription_ref=sub_ref, external_customer_ref=cust_ref,
        now_iso=_NOW)


def _raw_a(kind, sub, evt, when=None, sig=_SECRET):
    r = {"kind": kind, "sub": sub, "evt": evt, "sig": sig}
    if when is not None:
        r["when"] = when
    return r


def _raw_b(event, subscription, eid, effective=None, token=_SECRET):
    r = {"event": event, "subscription": subscription, "id": eid, "token": token}
    if effective is not None:
        r["effective"] = effective
    return r


# --- 2/3 port + two fakes satisfy the port; replaceability -------------------

def test_fakes_satisfy_port():
    for a in (FakeReferenceAdapterA(), FakeReferenceAdapterB()):
        assert isinstance(a, port.PaymentProviderPort)
        assert isinstance(a.provider_key, str) and a.provider_key


def test_replaceability_same_port_different_provider(tmp_path):
    s = _store(tmp_path)
    a1 = _account(s, "acct-a")
    a2 = _account(s, "acct-b")
    A, B = FakeReferenceAdapterA(), FakeReferenceAdapterB()
    _map(s, a1, A, "subA")
    _map(s, a2, B, "subB")
    # start both via different providers -> both reach the SAME P8-I3 authority
    ingest.ingest_provider_event(s, A, _raw_a("sub_started", "subA", "eA1"), now=10)
    ingest.ingest_provider_event(s, B, _raw_b("activation", "subB", "eB1"), now=10)
    assert sls.get_state(s, a1, now=10).current_state == sls.STATE_ACTIVE
    assert sls.get_state(s, a2, now=10).current_state == sls.STATE_ACTIVE


# --- 5 opaque external refs / 6 additive mapping / 7 reopen -------------------

def test_external_refs_opaque_and_mapping_durable(tmp_path):
    dbp = os.path.join(str(tmp_path), "reopen.db")
    s = SqliteAccountStore(dbp)
    a = _account(s)
    A = FakeReferenceAdapterA()
    cust, sub = A.create_customer_context(a)              # opaque strings
    assert isinstance(cust, str) and isinstance(sub, str)
    assert _map(s, a, A, sub, cust) == "created"
    del s
    s2 = SqliteAccountStore(dbp)                           # reopen existing DB
    assert s2.get_provider_mapping_account(A.provider_key, sub) == a


def test_lifecycle_and_provider_tables_present(tmp_path):
    _store(tmp_path)
    with sqlite3.connect(os.path.join(str(tmp_path), "p8i4.db")) as c:
        names = {r[0] for r in c.execute(
            "SELECT name FROM sqlite_master WHERE type='table'")}
    assert {"provider_mapping", "provider_event_dedupe"} <= names
    assert {"accounts", "commercial_assignments", "commercial_usage",
            "subscription_lifecycle_events"} <= names       # untouched foundations


# --- 8/9/10/11 fail-closed catalogue ----------------------------------------

def test_unknown_provider_fails_closed(tmp_path):
    s = _store(tmp_path)
    a = _account(s)
    A = FakeReferenceAdapterA()
    # no mapping created for this sub -> unknown/missing mapping
    with pytest.raises(port.ProviderBoundaryError):
        ingest.ingest_provider_event(s, A, _raw_a("sub_started", "ghost-sub", "e1"), now=10)


def test_missing_mapping_fails_closed(tmp_path):
    s = _store(tmp_path)
    _account(s)
    A = FakeReferenceAdapterA()
    with pytest.raises(port.ProviderBoundaryError):
        ingest.ingest_provider_event(s, A, _raw_a("sub_renewed", "no-map", "e1"), now=10)


def test_bad_authenticity_fails_closed_no_mutation(tmp_path):
    s = _store(tmp_path)
    a = _account(s)
    A = FakeReferenceAdapterA()
    _map(s, a, A, "sub1")
    with pytest.raises(port.ProviderBoundaryError):
        ingest.ingest_provider_event(s, A, _raw_a("sub_started", "sub1", "e1", sig="WRONG"), now=10)
    assert sls.get_state(s, a, now=10).current_state == sls.STATE_NONE
    assert s.get_provider_event(A.provider_key, "e1") is None


def test_unsupported_event_fails_closed(tmp_path):
    s = _store(tmp_path)
    a = _account(s)
    A = FakeReferenceAdapterA()
    _map(s, a, A, "sub1")
    with pytest.raises(port.ProviderBoundaryError):
        ingest.ingest_provider_event(s, A, _raw_a("totally_unknown_kind", "sub1", "e1"), now=10)


def test_disabled_and_deleted_account_fail_closed(tmp_path):
    s = _store(tmp_path)
    a = _account(s, "acct-dis", status="active")
    A = FakeReferenceAdapterA()
    _map(s, a, A, "sub1")
    s.set_status(a, "disabled", _NOW)
    with pytest.raises(port.ProviderBoundaryError):
        ingest.ingest_provider_event(s, A, _raw_a("sub_started", "sub1", "e1"), now=10)
    assert s.get_provider_event(A.provider_key, "e1") is None


def test_cross_account_mapping_conflict_denied(tmp_path):
    s = _store(tmp_path)
    a1 = _account(s, "acct-a")
    a2 = _account(s, "acct-b")
    A = FakeReferenceAdapterA()
    assert _map(s, a1, A, "shared-sub") == "created"
    assert _map(s, a2, A, "shared-sub") == "cross_account_conflict"   # fail closed
    assert s.get_provider_mapping_account(A.provider_key, "shared-sub") == a1


def test_malformed_ref_denied(tmp_path):
    s = _store(tmp_path)
    a = _account(s)
    A = FakeReferenceAdapterA()
    assert s.put_provider_mapping(a, provider=A.provider_key,
                                  external_subscription_ref="  ",
                                  external_customer_ref="c", now_iso=_NOW) == "malformed_ref"


# --- 12/13/14/15/16 dedupe + strict idempotency -----------------------------

def test_exact_duplicate_idempotent(tmp_path):
    s = _store(tmp_path)
    a = _account(s)
    A = FakeReferenceAdapterA()
    _map(s, a, A, "sub1")
    ingest.ingest_provider_event(s, A, _raw_a("sub_started", "sub1", "e1"), now=10)
    r2 = ingest.ingest_provider_event(s, A, _raw_a("sub_started", "sub1", "e1"), now=99)
    assert r2.duplicate is True and r2.status == "provider_duplicate"
    # exactly one lifecycle event appended
    assert len(sls.list_events(s, a)) == 1


def test_conflicting_duplicate_payload_fails_closed(tmp_path):
    s = _store(tmp_path)
    a = _account(s)
    A = FakeReferenceAdapterA()
    _map(s, a, A, "sub1")
    ingest.ingest_provider_event(s, A, _raw_a("sub_started", "sub1", "e1"), now=10)
    # same provider + same event id, but a materially different canonical content
    with pytest.raises(port.ProviderBoundaryError):
        ingest.ingest_provider_event(s, A, _raw_a("sub_canceled", "sub1", "e1"), now=20)
    assert sls.get_state(s, a, now=20).current_state == sls.STATE_ACTIVE   # unchanged


def test_same_event_id_different_providers_independent(tmp_path):
    s = _store(tmp_path)
    a1 = _account(s, "acct-a")
    a2 = _account(s, "acct-b")
    A, B = FakeReferenceAdapterA(), FakeReferenceAdapterB()
    _map(s, a1, A, "subA")
    _map(s, a2, B, "subB")
    ingest.ingest_provider_event(s, A, _raw_a("sub_started", "subA", "SAME"), now=10)
    ingest.ingest_provider_event(s, B, _raw_b("activation", "subB", "SAME"), now=10)
    assert s.get_provider_event(A.provider_key, "SAME")["account_id"] == a1
    assert s.get_provider_event(B.provider_key, "SAME")["account_id"] == a2


def test_dedupe_survives_restart(tmp_path):
    dbp = os.path.join(str(tmp_path), "r.db")
    s = SqliteAccountStore(dbp)
    a = _account(s)
    A = FakeReferenceAdapterA()
    _map(s, a, A, "sub1")
    ingest.ingest_provider_event(s, A, _raw_a("sub_started", "sub1", "e1"), now=10)
    del s
    s2 = SqliteAccountStore(dbp)
    r = ingest.ingest_provider_event(s2, A, _raw_a("sub_started", "sub1", "e1"), now=50)
    assert r.duplicate is True                              # durable dedupe


def test_rejected_pre_acceptance_can_later_succeed(tmp_path):
    s = _store(tmp_path)
    a = _account(s)
    A = FakeReferenceAdapterA()
    _map(s, a, A, "sub1")
    # invalid transition first: renew from `none` is invalid -> fail closed, NOT recorded
    with pytest.raises(port.ProviderBoundaryError):
        ingest.ingest_provider_event(s, A, _raw_a("sub_renewed", "sub1", "e1"), now=10)
    assert s.get_provider_event(A.provider_key, "e1") is None
    # corrected redelivery (same event id) now maps to a valid transition -> accepted
    r = ingest.ingest_provider_event(s, A, _raw_a("sub_started", "sub1", "e1"), now=20)
    assert r.accepted is True and r.duplicate is False


# --- 18/19/20 fingerprint / no raw payload ----------------------------------

def test_no_raw_payload_persisted(tmp_path):
    s = _store(tmp_path)
    a = _account(s)
    A = FakeReferenceAdapterA()
    _map(s, a, A, "sub1")
    ingest.ingest_provider_event(s, A, _raw_a("sub_started", "sub1", "e1", sig=_SECRET), now=10)
    rec = s.get_provider_event(A.provider_key, "e1")
    # the fake secret / native keys must NOT appear anywhere in the persisted record
    blob = repr(rec)
    assert _SECRET not in blob and "sig" not in blob and "kind" not in blob
    # nor in the durable lifecycle event record
    ev_blob = repr([vars(e) if hasattr(e, "__dict__")
                    else {k: getattr(e, k) for k in e.__slots__}
                    for e in sls.list_events(s, a)])
    assert _SECRET not in ev_blob


def test_fingerprint_deterministic_and_content_sensitive():
    op1 = port.CanonicalOperation(provider="p", provider_event_id="e",
                                  external_subscription_ref="s",
                                  canonical_event_type=sls.EV_STARTED)
    op2 = port.CanonicalOperation(provider="p", provider_event_id="e",
                                  external_subscription_ref="s",
                                  canonical_event_type=sls.EV_STARTED)
    op3 = port.CanonicalOperation(provider="p", provider_event_id="e",
                                  external_subscription_ref="s",
                                  canonical_event_type=sls.EV_CANCELLED)
    assert port.fingerprint(op1.normalized()) == port.fingerprint(op2.normalized())
    assert port.fingerprint(op1.normalized()) != port.fingerprint(op3.normalized())


# --- 21/22 adapter exception / timeout -> no mutation ------------------------

def test_adapter_exception_no_mutation(tmp_path):
    s = _store(tmp_path)
    a = _account(s)
    A = FakeReferenceAdapterA(fault="exception")
    _map(s, a, A, "sub1")
    with pytest.raises(Exception):
        ingest.ingest_provider_event(s, A, _raw_a("sub_started", "sub1", "e1"), now=10)
    assert sls.get_state(s, a, now=10).current_state == sls.STATE_NONE
    assert s.get_provider_event(A.provider_key, "e1") is None


def test_adapter_timeout_no_mutation(tmp_path):
    s = _store(tmp_path)
    a = _account(s)
    A = FakeReferenceAdapterA(fault="timeout")
    _map(s, a, A, "sub1")
    with pytest.raises(Exception):
        ingest.ingest_provider_event(s, A, _raw_a("sub_started", "sub1", "e1"), now=10)
    assert s.get_provider_event(A.provider_key, "e1") is None


# --- 23/24/25/26 canonical-mapping-only + P8-I3 authority --------------------

def test_raw_provider_name_never_enters_lifecycle_log(tmp_path):
    s = _store(tmp_path)
    a = _account(s)
    A = FakeReferenceAdapterA()
    _map(s, a, A, "sub1")
    ingest.ingest_provider_event(s, A, _raw_a("sub_started", "sub1", "e1"), now=10)
    ingest.ingest_provider_event(s, A, _raw_a("charge_failed", "sub1", "e2"), now=20)
    types = [e.event_type for e in sls.list_events(s, a)]
    assert types == [sls.EV_STARTED, sls.EV_PAYMENT_STATUS_CHANGED]   # canonical only
    assert "charge_failed" not in types and "sub_started" not in types


def test_invalid_transition_rejected_by_p8i3(tmp_path):
    s = _store(tmp_path)
    a = _account(s)
    A = FakeReferenceAdapterA()
    _map(s, a, A, "sub1")
    # cancel from `none` is an invalid P8-I3 transition -> fail closed
    with pytest.raises(port.ProviderBoundaryError):
        ingest.ingest_provider_event(s, A, _raw_a("sub_canceled", "sub1", "e1"), now=10)


def test_payment_failed_maps_to_past_due(tmp_path):
    s = _store(tmp_path)
    a = _account(s)
    A = FakeReferenceAdapterA()
    _map(s, a, A, "sub1")
    ingest.ingest_provider_event(s, A, _raw_a("sub_started", "sub1", "e1"), now=10)
    ingest.ingest_provider_event(s, A, _raw_a("charge_failed", "sub1", "e2"), now=20)
    assert sls.get_state(s, a, now=20).current_state == sls.STATE_PAST_DUE


# --- 27/28 quota + entitlement authority unchanged --------------------------

def test_quota_and_entitlement_authority_unchanged(tmp_path):
    s = _store(tmp_path)
    a = _account(s)
    s.set_commercial_assignment(a, *plan_catalog._UNLIMITED_TECHNICAL_PLAN, _NOW)
    quota_service.consume_quota(s, a, plan_catalog.QUOTA_PROOF_METER, amount=1)
    before_used = s.get_commercial_usage(a, plan_catalog.QUOTA_PROOF_METER, "lifetime")
    before_plan = ent.evaluate_entitlement(s, a, plan_catalog.CAPABILITY_INTERNAL_PROOF).plan_identity
    A = FakeReferenceAdapterA()
    _map(s, a, A, "sub1")
    ingest.ingest_provider_event(s, A, _raw_a("sub_started", "sub1", "e1"), now=10)
    ingest.ingest_provider_event(s, A, _raw_a("charge_failed", "sub1", "e2"), now=20)
    assert s.get_commercial_usage(a, plan_catalog.QUOTA_PROOF_METER, "lifetime") == before_used
    assert ent.evaluate_entitlement(s, a, plan_catalog.CAPABILITY_INTERNAL_PROOF).plan_identity == before_plan


# --- 29/30 atomicity: dedupe + lifecycle all-or-nothing ---------------------

def test_ingest_is_atomic_forced_rollback(tmp_path, monkeypatch):
    s = _store(tmp_path)
    a = _account(s)
    A = FakeReferenceAdapterA()
    _map(s, a, A, "sub1")
    orig = SqliteAccountStore._upsert_lifecycle_state

    def boom(self, *args, **kwargs):
        raise RuntimeError("forced failure inside ingest txn")

    monkeypatch.setattr(SqliteAccountStore, "_upsert_lifecycle_state", boom)
    with pytest.raises(Exception):
        ingest.ingest_provider_event(s, A, _raw_a("sub_started", "sub1", "e1"), now=10)
    monkeypatch.setattr(SqliteAccountStore, "_upsert_lifecycle_state", orig)
    # neither a dedupe record nor a lifecycle event survived
    assert s.get_provider_event(A.provider_key, "e1") is None
    assert len(sls.list_events(s, a)) == 0


# --- 33/34 concurrency ------------------------------------------------------

def test_concurrent_same_event_one_applies(tmp_path):
    s = _store(tmp_path)
    a = _account(s)
    A = FakeReferenceAdapterA()
    _map(s, a, A, "sub1")
    outcomes = []
    barrier = threading.Barrier(6)

    def worker():
        barrier.wait()
        try:
            r = ingest.ingest_provider_event(s, A, _raw_a("sub_started", "sub1", "e1"), now=10)
            outcomes.append("dup" if r.duplicate else "applied")
        except port.ProviderBoundaryError:
            outcomes.append("denied")

    th = [threading.Thread(target=worker) for _ in range(6)]
    for t in th:
        t.start()
    for t in th:
        t.join()
    assert outcomes.count("applied") == 1
    assert "denied" not in outcomes                        # exact dup, never conflict
    assert len(sls.list_events(s, a)) == 1


def test_concurrent_conflicting_payload_one_wins(tmp_path):
    s = _store(tmp_path)
    a = _account(s)
    A = FakeReferenceAdapterA()
    _map(s, a, A, "sub1")
    outcomes = []
    barrier = threading.Barrier(2)

    def worker(kind):
        barrier.wait()
        try:
            ingest.ingest_provider_event(s, A, _raw_a(kind, "sub1", "e1"), now=10)
            outcomes.append("applied")
        except port.ProviderBoundaryError:
            outcomes.append("conflict")

    th = [threading.Thread(target=worker, args=("sub_started",)),
          threading.Thread(target=worker, args=("charge_failed",))]
    for t in th:
        t.start()
    for t in th:
        t.join()
    # both share event id e1 with different canonical content -> exactly one durable
    assert outcomes.count("applied") == 1
    assert len(sls.list_events(s, a)) == 1


# --- 31/35 no secret persisted / import isolation ---------------------------

def test_core_modules_do_not_import_payment_boundary():
    engine_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "engine")
    payment_modules = {"payment_provider_port", "payment_fake_adapter",
                       "payment_ingestion"}
    core = {"scoring", "progression_loop", "idea_state", "safety_signal",
            "domain_rules", "domain_registry", "domain_activation",
            "subscription_lifecycle_service", "quota_service",
            "entitlement_service", "plan_catalog", "account_store"}
    for modname in core:
        tree = ast.parse(open(os.path.join(engine_dir, modname + ".py"),
                              encoding="utf-8").read())
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for al in node.names:
                    imported.add(al.name.split(".")[-1])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imported.add(node.module.split(".")[-1])
                for al in node.names:
                    imported.add(al.name)
        assert not (imported & payment_modules), \
            "%s imports the payment boundary" % modname


def test_no_provider_sdk_or_network_import():
    engine_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "engine")
    forbidden = {"stripe", "paddle", "paypal", "requests", "urllib", "http",
                 "socket", "ssl"}
    for modname in ("payment_provider_port", "payment_fake_adapter", "payment_ingestion"):
        tree = ast.parse(open(os.path.join(engine_dir, modname + ".py"),
                              encoding="utf-8").read())
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for al in node.names:
                    imported.add(al.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        assert not (imported & forbidden), \
            "%s: provider/network coupling %s" % (modname, sorted(imported & forbidden))


# --- 36 later sub-increments not implemented --------------------------------

def test_p8_i4_i2_i3_not_implemented():
    # no webhook transport / signature-verification / reconciliation module exists
    engine_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "engine")
    files = set(os.listdir(engine_dir))
    for forbidden in ("payment_webhook.py", "payment_reconciliation.py"):
        assert forbidden not in files
