"""P8-I3 — Subscription Lifecycle — focused behavioral tests (RED-first).

Covers the accepted CORRECTED P8-I3-C contract: bounded 5-state machine + implicit
`none`; additive append-only event log (source of truth) + derived current-state
cache; one-transaction atomicity; durable idempotency/replay; deterministic ordering
+ equal-effective_at tie-break; injected clock; read/projection vs authorized
materialization; RC-1 `none` entitlement-neutral (no silent legacy downgrade); RC-2
canonical past_due exits; RC-3 unique cancellation mapping; P8-I2 quota authority /
no reset; anti-lockout; account fail-closed; provider neutrality; regression.
"""

import os
import sqlite3
import threading

import pytest

from engine.account_store import SqliteAccountStore
from engine import plan_catalog
from engine import entitlement_service as ent
from engine import quota_service
from engine import subscription_lifecycle_service as sls


_NOW = "2026-01-01T00:00:00Z"


def _store(tmp_path):
    return SqliteAccountStore(os.path.join(str(tmp_path), "p8i3.db"))


def _account(store, account_id="acct-1", status="active"):
    store.create_account(account_id, account_id + "@x.test", "hash", _NOW,
                         status=status)
    return account_id


def _proof_cap():
    return plan_catalog.CAPABILITY_INTERNAL_PROOF


# --- 5 create / valid transition / states -----------------------------------

def test_initial_state_is_none_no_row(tmp_path):
    s = _store(tmp_path)
    a = _account(s)
    proj = sls.get_state(s, a, now=0)
    assert proj.current_state == sls.STATE_NONE


def test_subscription_started_creates_active(tmp_path):
    s = _store(tmp_path)
    a = _account(s)
    r = sls.apply_event(s, a, sls.EV_STARTED, now=10)
    assert r.status == "applied"
    assert sls.get_state(s, a, now=10).current_state == sls.STATE_ACTIVE


def test_trial_started_then_converted(tmp_path):
    s = _store(tmp_path)
    a = _account(s)
    sls.apply_event(s, a, sls.EV_TRIAL_STARTED, now=10)
    assert sls.get_state(s, a, now=10).current_state == sls.STATE_TRIALING
    sls.apply_event(s, a, sls.EV_TRIAL_CONVERTED, now=20)
    assert sls.get_state(s, a, now=20).current_state == sls.STATE_ACTIVE


def test_renewal_keeps_active(tmp_path):
    s = _store(tmp_path)
    a = _account(s)
    sls.apply_event(s, a, sls.EV_STARTED, now=10)
    sls.apply_event(s, a, sls.EV_RENEWED, now=20)
    assert sls.get_state(s, a, now=20).current_state == sls.STATE_ACTIVE


# --- 7 invalid transition fails closed --------------------------------------

def test_invalid_transition_denied_no_mutation(tmp_path):
    s = _store(tmp_path)
    a = _account(s)
    sls.apply_event(s, a, sls.EV_STARTED, now=10)      # active
    # renew is only valid from active; trial_converted from active is invalid
    with pytest.raises(sls.LifecycleError):
        sls.apply_event(s, a, sls.EV_TRIAL_CONVERTED, now=20)
    assert sls.get_state(s, a, now=20).current_state == sls.STATE_ACTIVE  # unchanged


def test_none_to_canceled_direct_is_invalid(tmp_path):
    s = _store(tmp_path)
    a = _account(s)
    with pytest.raises(sls.LifecycleError):
        sls.apply_event(s, a, sls.EV_CANCELLED, now=10)


def test_malformed_event_type_fails_closed(tmp_path):
    s = _store(tmp_path)
    a = _account(s)
    with pytest.raises(sls.LifecycleError):
        sls.apply_event(s, a, "provider_magic_event", now=10)


# --- 8/9 idempotency + replay -----------------------------------------------

def test_duplicate_event_idempotent(tmp_path):
    s = _store(tmp_path)
    a = _account(s)
    r1 = sls.apply_event(s, a, sls.EV_STARTED, now=10, idempotency_key="k1")
    r2 = sls.apply_event(s, a, sls.EV_STARTED, now=10, idempotency_key="k1")
    assert r1.status == "applied"
    assert r2.status == "idempotent_replay"
    assert len(sls.list_events(s, a)) == 1                       # no duplicate history


def test_replay_deterministic_same_result(tmp_path):
    s = _store(tmp_path)
    a = _account(s)
    sls.apply_event(s, a, sls.EV_STARTED, now=10, idempotency_key="k1")
    r = sls.apply_event(s, a, sls.EV_STARTED, now=999, idempotency_key="k1")
    assert r.status == "idempotent_replay"
    assert r.current_state == sls.STATE_ACTIVE


# --- 10 out-of-order stale event rejected -----------------------------------

def test_stale_effective_at_rejected(tmp_path):
    s = _store(tmp_path)
    a = _account(s)
    sls.apply_event(s, a, sls.EV_STARTED, now=100)              # current_since = 100
    with pytest.raises(sls.LifecycleError):
        sls.apply_event(s, a, sls.EV_RENEWED, now=100, effective_at=50)  # stale


# --- 12/13/14/15 account fail-closed ----------------------------------------

def test_missing_account_denied(tmp_path):
    s = _store(tmp_path)
    with pytest.raises(sls.LifecycleError):
        sls.apply_event(s, "ghost", sls.EV_STARTED, now=10)


def test_disabled_account_denied(tmp_path):
    s = _store(tmp_path)
    a = _account(s, "acct-dis", status="disabled")
    with pytest.raises(sls.LifecycleError):
        sls.apply_event(s, a, sls.EV_STARTED, now=10)


def test_deleted_account_denied(tmp_path):
    s = _store(tmp_path)
    a = _account(s, "acct-del", status="deleted")
    with pytest.raises(sls.LifecycleError):
        sls.apply_event(s, a, sls.EV_STARTED, now=10)


def test_cross_account_isolation(tmp_path):
    s = _store(tmp_path)
    a = _account(s, "acct-a")
    b = _account(s, "acct-b")
    sls.apply_event(s, a, sls.EV_STARTED, now=10)
    assert sls.get_state(s, b, now=10).current_state == sls.STATE_NONE  # b untouched


# --- 16/17 concurrency ------------------------------------------------------

def test_concurrent_same_event_one_applies(tmp_path):
    s = _store(tmp_path)
    a = _account(s)
    results = []
    barrier = threading.Barrier(6)

    def worker():
        barrier.wait()
        try:
            results.append(sls.apply_event(s, a, sls.EV_STARTED, now=10,
                                           idempotency_key="same").status)
        except Exception as e:  # noqa: BLE001
            results.append(type(e).__name__)

    threads = [threading.Thread(target=worker) for _ in range(6)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert results.count("applied") == 1
    assert len(sls.list_events(s, a)) == 1


# --- 18/19/36-39 scheduled cancellation, materialization, projection --------

def test_cancellation_requested_then_effective_materialization(tmp_path):
    s = _store(tmp_path)
    a = _account(s)
    sls.apply_event(s, a, sls.EV_STARTED, now=10)
    sls.apply_event(s, a, sls.EV_CANCELLATION_REQUESTED, now=20, effective_at=100)
    # requested but not yet effective: stored state stays active, pending true
    proj = sls.get_state(s, a, now=50)
    assert proj.current_state == sls.STATE_ACTIVE
    assert proj.cancellation_pending is True
    # read/projection at/after effective_at projects canceled but MUST NOT write
    proj_due = sls.get_state(s, a, now=150)
    assert proj_due.projected_state == sls.STATE_CANCELED
    assert sls.list_events(s, a) and sls.list_events(s, a)[-1].event_type != sls.EV_CANCELLED
    # authorized materialization writes durably
    r = sls.materialize_due(s, a, now=150)
    assert r is not None and r.current_state == sls.STATE_CANCELED
    assert sls.list_events(s, a)[-1].event_type == sls.EV_CANCELLED
    # idempotent second materialization
    assert sls.materialize_due(s, a, now=160) is None


def test_projection_does_not_write(tmp_path):
    s = _store(tmp_path)
    a = _account(s)
    sls.apply_event(s, a, sls.EV_STARTED, now=10)
    sls.apply_event(s, a, sls.EV_CANCELLATION_REQUESTED, now=20, effective_at=100)
    n_before = len(sls.list_events(s, a))
    sls.get_state(s, a, now=500)                                # due, projected
    sls.project_effective_entitlement(s, a, _proof_cap(), now=500)
    assert len(sls.list_events(s, a)) == n_before               # NO silent write


def test_event_log_equals_derived_after_materialization(tmp_path):
    s = _store(tmp_path)
    a = _account(s)
    sls.apply_event(s, a, sls.EV_STARTED, now=10)
    sls.apply_event(s, a, sls.EV_CANCELLATION_REQUESTED, now=20, effective_at=100)
    sls.materialize_due(s, a, now=150)
    replay = sls.rebuild_state_from_events(s, a)
    assert replay == sls.get_state(s, a, now=150).current_state


# --- 21 plan-change interaction (coordinated, atomic) -----------------------

def test_plan_change_coordinated_with_assignment(tmp_path):
    s = _store(tmp_path)
    a = _account(s)
    sls.apply_event(s, a, sls.EV_STARTED, now=10)
    target = plan_catalog.RESTRICTED_TECHNICAL_PLAN
    sls.apply_event(s, a, sls.EV_CHANGED, now=20, target_plan=target)
    assert s.get_commercial_assignment(a)["plan_id"] == target[0]
    assert sls.get_state(s, a, now=20).current_state == sls.STATE_ACTIVE  # state unchanged


# --- 22/23 RC-1: `none` entitlement-neutral (NO silent legacy downgrade) ----

def test_none_with_nondefault_assignment_preserves_entitlement(tmp_path):
    s = _store(tmp_path)
    a = _account(s)
    # legacy account: an explicit assignment, NO lifecycle row (state none)
    s.set_commercial_assignment(a, *plan_catalog._UNLIMITED_TECHNICAL_PLAN, _NOW)
    assert sls.get_state(s, a, now=0).current_state == sls.STATE_NONE
    proj = sls.project_effective_entitlement(s, a, plan_catalog.QUOTA_PROOF_CAP
                                             if hasattr(plan_catalog, "QUOTA_PROOF_CAP")
                                             else _proof_cap(), now=0)
    baseline = ent.evaluate_entitlement(s, a, _proof_cap())
    # `none` must delegate to P8-I1 unchanged: same plan identity, same allow.
    assert proj.plan_identity == baseline.plan_identity == plan_catalog._UNLIMITED_TECHNICAL_PLAN
    assert proj.allow == baseline.allow


def test_none_without_assignment_uses_default(tmp_path):
    s = _store(tmp_path)
    a = _account(s)
    proj = sls.project_effective_entitlement(s, a, _proof_cap(), now=0)
    assert proj.plan_identity == plan_catalog.default_plan_identity()
    assert proj.allow == ent.evaluate_entitlement(s, a, _proof_cap()).allow


def test_terminal_canceled_projects_default(tmp_path):
    s = _store(tmp_path)
    a = _account(s)
    s.set_commercial_assignment(a, *plan_catalog._UNLIMITED_TECHNICAL_PLAN, _NOW)
    sls.apply_event(s, a, sls.EV_STARTED, now=10)
    sls.apply_event(s, a, sls.EV_CANCELLED, now=20)            # immediate effective cancel
    proj = sls.project_effective_entitlement(s, a, _proof_cap(), now=20)
    assert proj.plan_identity == plan_catalog.default_plan_identity()  # terminal -> default


# --- 24 quota not reset on lifecycle transition -----------------------------

def test_quota_not_reset_on_transition(tmp_path):
    s = _store(tmp_path)
    a = _account(s)
    s.set_commercial_assignment(a, *plan_catalog._UNLIMITED_TECHNICAL_PLAN, _NOW)
    sls.apply_event(s, a, sls.EV_STARTED, now=10)
    quota_service.consume_quota(s, a, plan_catalog.QUOTA_PROOF_METER, amount=1)
    used_before = s.get_commercial_usage(a, plan_catalog.QUOTA_PROOF_METER, "lifetime")
    sls.apply_event(s, a, sls.EV_RENEWED, now=20)
    sls.apply_event(s, a, sls.EV_CHANGED, now=30,
                    target_plan=plan_catalog._UNLIMITED_TECHNICAL_PLAN)
    used_after = s.get_commercial_usage(a, plan_catalog.QUOTA_PROOF_METER, "lifetime")
    assert used_after == used_before == 1                      # no silent reset


# --- 34/35 RC-2 canonical past_due exits ------------------------------------

def test_past_due_expired_uses_subscription_expired(tmp_path):
    s = _store(tmp_path)
    a = _account(s)
    sls.apply_event(s, a, sls.EV_STARTED, now=10)
    sls.apply_event(s, a, sls.EV_PAYMENT_STATUS_CHANGED, now=20, payment_status="failed")
    assert sls.get_state(s, a, now=20).current_state == sls.STATE_PAST_DUE
    sls.apply_event(s, a, sls.EV_EXPIRED, now=30, reason="grace_exhausted")
    assert sls.get_state(s, a, now=30).current_state == sls.STATE_EXPIRED


def test_past_due_canceled_uses_subscription_cancelled(tmp_path):
    s = _store(tmp_path)
    a = _account(s)
    sls.apply_event(s, a, sls.EV_STARTED, now=10)
    sls.apply_event(s, a, sls.EV_PAYMENT_STATUS_CHANGED, now=20, payment_status="failed")
    sls.apply_event(s, a, sls.EV_CANCELLED, now=30)
    assert sls.get_state(s, a, now=30).current_state == sls.STATE_CANCELED


def test_past_due_recovers_to_active(tmp_path):
    s = _store(tmp_path)
    a = _account(s)
    sls.apply_event(s, a, sls.EV_STARTED, now=10)
    sls.apply_event(s, a, sls.EV_PAYMENT_STATUS_CHANGED, now=20, payment_status="failed")
    sls.apply_event(s, a, sls.EV_PAYMENT_STATUS_CHANGED, now=30, payment_status="recovered")
    assert sls.get_state(s, a, now=30).current_state == sls.STATE_ACTIVE


# --- 40 RC-3: change_scheduled does NOT alias cancellation ------------------

def test_change_scheduled_is_not_cancellation(tmp_path):
    s = _store(tmp_path)
    a = _account(s)
    sls.apply_event(s, a, sls.EV_STARTED, now=10)
    sls.apply_event(s, a, sls.EV_CHANGE_SCHEDULED, now=20, effective_at=100,
                    target_plan=plan_catalog.RESTRICTED_TECHNICAL_PLAN)
    proj = sls.get_state(s, a, now=50)
    assert proj.cancellation_pending is False                  # a PLAN change, not a cancel
    sls.materialize_due(s, a, now=150)
    # plan changed, but lifecycle stays active (not canceled)
    assert sls.get_state(s, a, now=150).current_state == sls.STATE_ACTIVE
    assert s.get_commercial_assignment(a)["plan_id"] == plan_catalog.RESTRICTED_TECHNICAL_PLAN[0]


# --- 36 equal-effective_at tie-break by event sequence ----------------------

def test_equal_effective_at_tiebreak_by_sequence(tmp_path):
    s = _store(tmp_path)
    a = _account(s)
    sls.apply_event(s, a, sls.EV_STARTED, now=10, effective_at=10)
    sls.apply_event(s, a, sls.EV_PAYMENT_STATUS_CHANGED, now=10, effective_at=10,
                    payment_status="failed")
    events = sls.list_events(s, a)
    # strictly increasing durable sequence even with identical effective_at
    seqs = [e.event_id for e in events]
    assert seqs == sorted(seqs) and len(set(seqs)) == len(seqs)
    assert sls.get_state(s, a, now=10).current_state == sls.STATE_PAST_DUE  # last wins deterministically


# --- 25 anti-lockout: existing-data access never blocked --------------------

def test_anti_lockout_read_export_available_when_canceled(tmp_path):
    s = _store(tmp_path)
    a = _account(s)
    sls.apply_event(s, a, sls.EV_STARTED, now=10)
    sls.apply_event(s, a, sls.EV_CANCELLED, now=20)
    # account remains active & owned; lifecycle terminal does not disable the account
    assert s.get_account_by_id(a)["status"] == "active"
    # lifecycle exposes no capability that blocks data read/export/delete
    assert not hasattr(sls, "block_data_access")


# --- 26 provider neutrality --------------------------------------------------

def test_provider_neutral_external_reference_opaque(tmp_path):
    s = _store(tmp_path)
    a = _account(s)
    sls.apply_event(s, a, sls.EV_STARTED, now=10,
                    source="internal", external_reference="opaque-xyz")
    e = sls.list_events(s, a)[-1]
    assert e.source == "internal" and e.external_reference == "opaque-xyz"


def test_no_provider_module_imported():
    import ast
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                        "engine", "subscription_lifecycle_service.py")
    tree = ast.parse(open(path, encoding="utf-8").read())
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                imported.add(a.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
    forbidden = {"stripe", "paddle", "paypal", "requests", "urllib", "http",
                 "socket", "ssl"}
    assert not (imported & forbidden), \
        "provider/network coupling leaked: %s" % sorted(imported & forbidden)


# --- 27/2/3/4 durability + additive schema + existing records preserved -----

def test_additive_schema_reopen_preserves_records(tmp_path):
    dbp = os.path.join(str(tmp_path), "reopen.db")
    s = SqliteAccountStore(dbp)
    a = _account(s)
    s.set_commercial_assignment(a, *plan_catalog._UNLIMITED_TECHNICAL_PLAN, _NOW)
    sls.apply_event(s, a, sls.EV_STARTED, now=10)
    del s
    s2 = SqliteAccountStore(dbp)                                # reopen existing DB
    assert s2.get_account_by_id(a)["status"] == "active"       # preserved
    assert s2.get_commercial_assignment(a)["plan_id"] == plan_catalog._UNLIMITED_TECHNICAL_PLAN[0]
    assert sls.get_state(s2, a, now=10).current_state == sls.STATE_ACTIVE  # durable across reopen


def test_lifecycle_tables_are_additive_create_if_not_exists(tmp_path):
    s = _store(tmp_path)
    with sqlite3.connect(os.path.join(str(tmp_path), "p8i3.db")) as c:
        names = {r[0] for r in c.execute(
            "SELECT name FROM sqlite_master WHERE type='table'")}
    assert {"subscription_lifecycle_events", "subscription_lifecycle_state"} <= names
    assert {"accounts", "commercial_assignments", "commercial_usage"} <= names  # untouched


# --- 28 atomic rollback: event+state write is all-or-nothing ----------------

def test_interrupted_write_rolls_back_event_and_state(tmp_path, monkeypatch):
    s = _store(tmp_path)
    a = _account(s)
    sls.apply_event(s, a, sls.EV_STARTED, now=10)
    n_before = len(sls.list_events(s, a))

    # Force the derived-state upsert to fail; the appended event MUST roll back too.
    orig = SqliteAccountStore._upsert_lifecycle_state

    def boom(self, c, *args, **kwargs):
        raise RuntimeError("forced state-upsert failure")

    monkeypatch.setattr(SqliteAccountStore, "_upsert_lifecycle_state", boom)
    with pytest.raises(Exception):
        sls.apply_event(s, a, sls.EV_RENEWED, now=20)
    monkeypatch.setattr(SqliteAccountStore, "_upsert_lifecycle_state", orig)
    assert len(sls.list_events(s, a)) == n_before              # event rolled back with state


# --- 33 injected-clock determinism ------------------------------------------

def test_injected_clock_determinism(tmp_path):
    s = _store(tmp_path)
    a = _account(s)
    sls.apply_event(s, a, sls.EV_STARTED, now=10)
    sls.apply_event(s, a, sls.EV_CANCELLATION_REQUESTED, now=20, effective_at=100)
    assert sls.get_state(s, a, now=99).projected_state == sls.STATE_ACTIVE   # not yet due
    assert sls.get_state(s, a, now=100).projected_state == sls.STATE_CANCELED  # due at boundary


# ============================================================================
# Verdict-B corrections (RC-I1..RC-I6) — behavioral RED-first regression tests.
# ============================================================================

def test_rc_i1_two_thread_scheduling_exclusivity(tmp_path):
    """D1: two concurrent scheduling events (cancellation_requested vs
    subscription_change_scheduled) from the same state must not BOTH become
    durable — exactly one pending schedule is permitted."""
    s = _store(tmp_path)
    a = _account(s)
    sls.apply_event(s, a, sls.EV_STARTED, now=10)
    outcomes = []
    barrier = threading.Barrier(2)

    def t_cancel():
        barrier.wait()
        try:
            sls.apply_event(s, a, sls.EV_CANCELLATION_REQUESTED, now=20,
                            effective_at=100, idempotency_key="cancel")
            outcomes.append("cancel_ok")
        except sls.LifecycleError:
            outcomes.append("cancel_denied")

    def t_change():
        barrier.wait()
        try:
            sls.apply_event(s, a, sls.EV_CHANGE_SCHEDULED, now=20, effective_at=100,
                            target_plan=plan_catalog.RESTRICTED_TECHNICAL_PLAN,
                            idempotency_key="change")
            outcomes.append("change_ok")
        except sls.LifecycleError:
            outcomes.append("change_denied")

    th = [threading.Thread(target=t_cancel), threading.Thread(target=t_change)]
    for t in th:
        t.start()
    for t in th:
        t.join()
    ok = [o for o in outcomes if o.endswith("_ok")]
    assert len(ok) == 1, outcomes                              # exactly one pending schedule
    sched_events = [e for e in sls.list_events(s, a)
                    if e.event_type in (sls.EV_CANCELLATION_REQUESTED,
                                        sls.EV_CHANGE_SCHEDULED)]
    assert len(sched_events) == 1                              # no silent second schedule


def test_rc_i2_store_rejects_stale_effective_at_in_transaction(tmp_path):
    """D2: the durable append must fail closed for an effective_at earlier than the
    latest committed state (in-transaction check), not only in the service
    pre-read."""
    s = _store(tmp_path)
    a = _account(s)
    sls.apply_event(s, a, sls.EV_STARTED, now=100)             # current_since = 100
    # A writer that validated earlier (from active) submits a stale effective_at.
    status, state, eid = s.apply_lifecycle_event(
        a, event_type=sls.EV_RENEWED, expected_from_state=sls.STATE_ACTIVE,
        new_current_state=sls.STATE_ACTIVE, event_to_state=sls.STATE_ACTIVE,
        effective_at="50", recorded_at="50")
    assert status == "conflict_stale"                          # rejected in-txn
    assert len(sls.list_events(s, a)) == 1                     # no stale event appended


def test_rc_i3_two_thread_different_transition_race(tmp_path):
    """D3: two threads attempt genuinely-conflicting transitions from the same
    state (cancel vs expire — both leave `active` for different states). The
    in-transaction from-state guard permits exactly one; the other fails closed;
    the log stays valid and equals the derived state. (Deterministic: whichever
    commits first changes `active`, so the second always conflicts.)"""
    s = _store(tmp_path)
    a = _account(s)
    sls.apply_event(s, a, sls.EV_STARTED, now=10)
    outcomes = []
    barrier = threading.Barrier(2)

    def t_cancel():
        barrier.wait()
        try:
            sls.apply_event(s, a, sls.EV_CANCELLED, now=20, idempotency_key="cancel")
            outcomes.append("cancel_ok")
        except sls.LifecycleError:
            outcomes.append("cancel_denied")

    def t_expire():
        barrier.wait()
        try:
            sls.apply_event(s, a, sls.EV_EXPIRED, now=20, idempotency_key="expire")
            outcomes.append("expire_ok")
        except sls.LifecycleError:
            outcomes.append("expire_denied")

    th = [threading.Thread(target=t_cancel), threading.Thread(target=t_expire)]
    for t in th:
        t.start()
    for t in th:
        t.join()
    assert len([o for o in outcomes if o.endswith("_ok")]) == 1, outcomes
    assert sls.rebuild_state_from_events(s, a) == sls.get_state(s, a, now=99).current_state


def test_rc_i4_scheduled_target_plan_persisted_in_event_log(tmp_path):
    """D4 source-of-truth: a scheduled plan change persists its target plan in the
    append-only event row (not only the derived cache)."""
    s = _store(tmp_path)
    a = _account(s)
    sls.apply_event(s, a, sls.EV_STARTED, now=10)
    sls.apply_event(s, a, sls.EV_CHANGE_SCHEDULED, now=20, effective_at=100,
                    target_plan=plan_catalog.RESTRICTED_TECHNICAL_PLAN)
    ev = s.list_lifecycle_events(a)[-1]
    assert ev.get("target_plan_id") == plan_catalog.RESTRICTED_TECHNICAL_PLAN[0]
    assert ev.get("target_plan_version") == plan_catalog.RESTRICTED_TECHNICAL_PLAN[1]


def test_rc_i4_rebuild_pending_plan_from_event_log_only(tmp_path):
    """D4: reconstruct the pending scheduled plan change from the event log ALONE
    (ignoring the derived cache); the rebuilt schedule matches the durable cache."""
    s = _store(tmp_path)
    a = _account(s)
    sls.apply_event(s, a, sls.EV_STARTED, now=10)
    sls.apply_event(s, a, sls.EV_CHANGE_SCHEDULED, now=20, effective_at=100,
                    target_plan=plan_catalog.RESTRICTED_TECHNICAL_PLAN)
    rebuilt = sls.rebuild_from_events(s, a)
    row = s.get_lifecycle_state_row(a)
    assert rebuilt["current_state"] == row["current_state"]
    assert rebuilt["scheduled_effective_at"] == row["scheduled_effective_at"]
    assert rebuilt["scheduled_plan_id"] == row["scheduled_plan_id"] \
        == plan_catalog.RESTRICTED_TECHNICAL_PLAN[0]
    assert rebuilt["scheduled_plan_version"] == row["scheduled_plan_version"] \
        == plan_catalog.RESTRICTED_TECHNICAL_PLAN[1]


def test_rc_i5_same_effective_at_across_epochs_materializes_separately(tmp_path):
    """D5: a scheduled cancellation reusing the SAME effective_at in a later epoch
    materializes as a distinct new event — the old event must not replay and wedge
    the new schedule."""
    s = _store(tmp_path)
    a = _account(s)
    sls.apply_event(s, a, sls.EV_STARTED, now=10)
    sls.apply_event(s, a, sls.EV_CANCELLATION_REQUESTED, now=20, effective_at=100)
    sls.materialize_due(s, a, now=150)
    assert sls.get_state(s, a, now=150).current_state == sls.STATE_CANCELED
    # new epoch
    sls.apply_event(s, a, sls.EV_STARTED, now=200)
    sls.apply_event(s, a, sls.EV_CANCELLATION_REQUESTED, now=210, effective_at=100)
    r = sls.materialize_due(s, a, now=250)
    assert r is not None and r.current_state == sls.STATE_CANCELED    # NOT wedged
    cancels = [e for e in sls.list_events(s, a) if e.event_type == sls.EV_CANCELLED]
    assert len(cancels) == 2                                   # two distinct effective cancels
    # repeated materialization of the same scheduled event is idempotent
    assert sls.materialize_due(s, a, now=260) is None


def test_rc_i6_missing_account_lifecycle_read_denied(tmp_path):
    s = _store(tmp_path)
    with pytest.raises(sls.LifecycleError):
        sls.get_state(s, "ghost", now=0)
    with pytest.raises(sls.LifecycleError):
        sls.list_events(s, "ghost")


def test_rc_i6_disabled_account_lifecycle_read_denied(tmp_path):
    s = _store(tmp_path)
    a = _account(s, "acct-dis", status="disabled")
    with pytest.raises(sls.LifecycleError):
        sls.get_state(s, a, now=0)
    with pytest.raises(sls.LifecycleError):
        sls.list_events(s, a)


def test_rc_i6_deleted_account_lifecycle_read_denied(tmp_path):
    s = _store(tmp_path)
    a = _account(s, "acct-del", status="deleted")
    with pytest.raises(sls.LifecycleError):
        sls.get_state(s, a, now=0)


def test_rc_i6_active_account_lifecycle_read_allowed(tmp_path):
    s = _store(tmp_path)
    a = _account(s)
    sls.apply_event(s, a, sls.EV_STARTED, now=10)
    assert sls.get_state(s, a, now=10).current_state == sls.STATE_ACTIVE  # active OK
