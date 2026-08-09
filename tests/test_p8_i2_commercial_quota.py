"""P8-I2 — Commercial Usage Quotas / Limits (RED → GREEN).

Behavioral tests for the accepted bounded P8-I2 contract
(`docs/governance/PHASE_8_I2_COMMERCIAL_USAGE_QUOTAS_INCREMENT_CONTRACT.md`,
PR #419). Provider-neutral commercial usage-limit foundation over the P8-I1
entitlement layer:

    Account / Commercial Principal → Plan Identity → Entitlement Evaluation
        → Commercial Quota Evaluation → Governed Capability Access
    (WITHOUT payment processing or public commercial packaging)

Fail-closed, plan-neutral (OD-N), atomic hard-cap consumption, idempotent,
anti-lock-in. Neutral INTERNAL proof meter only — no real user-facing paywall,
no marketed values, no lifecycle/provider/UI. SQLite files live only in tmp_path.

On the pre-implementation base these tests are RED because
``engine.quota_service`` and the account-store ``commercial_usage`` tables do
not exist.
"""
import ast
import os
import sqlite3
import threading

import pytest

from engine.account_store import SqliteAccountStore
from engine import domain_activation
from engine import plan_catalog

# Modules under test — absent on the base → genuine RED (import error).
from engine import quota_service as q


_NOW = "2026-01-01T00:00:00Z"
_EPOCH = 1_800_000_000            # deterministic injectable clock (epoch seconds)

DEFAULT = plan_catalog.default_plan_identity()          # entitled; proof quota limit 2 (lifetime)
ZERO = ("__zero_quota_technical__", "1")                # entitled; proof quota limit 0
UNLIMITED_PLAN = ("__unlimited_technical__", "1")       # entitled; proof quota UNLIMITED
FIXED = ("__fixed_window_technical__", "1")             # entitled; proof quota limit 1 fixed window
MALFORMED = ("__malformed_quota_technical__", "1")      # entitled; malformed quota policy
RESTRICTED = plan_catalog.RESTRICTED_TECHNICAL_PLAN     # NOT entitled to the proof capability
METER = plan_catalog.QUOTA_PROOF_METER


def _store(tmp_path, name="p8i2.sqlite3"):
    return SqliteAccountStore(str(tmp_path / name))


def _account(store, account_id="acct_1", status="active", plan=None):
    store.create_account(account_id, account_id + "@ex.test", "scrypt$dummyhash",
                         _NOW, status=status)
    if plan is not None:
        store.set_commercial_assignment(account_id, plan[0], plan[1], _NOW)
    return account_id


# 1 — entitled + quota available → allowed, consumes exactly once.
def test_entitled_available_allows_and_consumes_once(tmp_path):
    s = _store(tmp_path)
    a = _account(s, plan=DEFAULT)                        # limit 2
    d = q.consume_quota(s, a, METER, now=_EPOCH)
    assert d.outcome == q.OUTCOME_ALLOWED and d.allowed is True
    assert q.evaluate_quota(s, a, METER, now=_EPOCH).used == 1


# 2 — entitled + quota exhausted → deny, no increment beyond limit.
def test_entitled_exhausted_denies_without_increment(tmp_path):
    s = _store(tmp_path)
    a = _account(s, plan=ZERO)                           # limit 0 → immediately exhausted
    d = q.consume_quota(s, a, METER, now=_EPOCH)
    assert d.outcome == q.OUTCOME_DENIED_EXHAUSTED and d.allowed is False
    assert q.evaluate_quota(s, a, METER, now=_EPOCH).used == 0     # never incremented


# 2b — hard cap: consume up to the limit then deny; counter never exceeds limit.
def test_hard_cap_denies_beyond_limit(tmp_path):
    s = _store(tmp_path)
    a = _account(s, plan=DEFAULT)                        # limit 2
    assert q.consume_quota(s, a, METER, now=_EPOCH).allowed is True
    assert q.consume_quota(s, a, METER, now=_EPOCH).allowed is True
    third = q.consume_quota(s, a, METER, now=_EPOCH)
    assert third.outcome == q.OUTCOME_DENIED_EXHAUSTED
    assert q.evaluate_quota(s, a, METER, now=_EPOCH).used == 2     # capped


# 3 — not entitled → deny, no quota consumption.
def test_not_entitled_denies_without_consumption(tmp_path):
    s = _store(tmp_path)
    a = _account(s, plan=RESTRICTED)                     # entitlement proof = False
    d = q.consume_quota(s, a, METER, now=_EPOCH)
    assert d.outcome == q.OUTCOME_DENIED_NOT_ENTITLED and d.allowed is False
    assert s.get_commercial_usage(a, METER, "lifetime") == 0     # durable counter untouched


# 4 — missing account → fail closed, no consumption.
def test_missing_account_fails_closed(tmp_path):
    s = _store(tmp_path)
    d = q.consume_quota(s, "ghost", METER, now=_EPOCH)
    assert d.allowed is False
    assert d.outcome in (q.OUTCOME_DENIED_INVALID, q.OUTCOME_INTERNAL_FAIL_CLOSED)


# 5 — disabled/deleted account → fail closed, no consumption.
@pytest.mark.parametrize("status", ["disabled", "deleted"])
def test_non_active_account_fails_closed(tmp_path, status):
    s = _store(tmp_path)
    a = _account(s, plan=DEFAULT)
    s.set_status(a, status, _NOW)
    d = q.consume_quota(s, a, METER, now=_EPOCH)
    assert d.allowed is False
    assert s.get_commercial_usage(a, METER, "lifetime") == 0     # durable counter untouched


# 6 — malformed quota policy → fail closed, no consumption.
def test_malformed_quota_policy_fails_closed(tmp_path):
    s = _store(tmp_path)
    a = _account(s, plan=MALFORMED)
    d = q.consume_quota(s, a, METER, now=_EPOCH)
    assert d.allowed is False
    assert d.outcome in (q.OUTCOME_DENIED_INVALID, q.OUTCOME_INTERNAL_FAIL_CLOSED)


# 7 — security rate-limit independence: quota consumption never touches the
#     security rate-limit state (auth_rate_limits), and vice versa.
def test_security_rate_limit_independent_from_quota(tmp_path):
    s = _store(tmp_path)
    a = _account(s, plan=DEFAULT)
    # A commercial consumption must not create/alter any security rate-limit row.
    q.consume_quota(s, a, METER, now=_EPOCH)
    with s._read() as c:
        assert c.execute("SELECT COUNT(*) FROM auth_rate_limits").fetchone()[0] == 0
    # A security rate-limit attempt must not consume commercial quota.
    assert s.record_rate_attempt("subj", "login", _NOW,
                                 "2026-01-01T00:01:00Z", 5) is True
    assert q.evaluate_quota(s, a, METER, now=_EPOCH).used == 1   # only the commercial consume


# 8 / 9 — API scope + credential revocation remain plan/quota-independent.
def test_api_scope_and_revocation_independent_of_quota(tmp_path):
    s = _store(tmp_path)
    a = _account(s, plan=DEFAULT)
    cred = s.create_api_credential("cred1", "sechash", a, "project:read", _NOW)
    q.consume_quota(s, a, METER, now=_EPOCH)             # consume commercial quota
    row = s.get_api_credential("cred1")
    assert row["scopes"] == "project:read" and row["status"] == "active"
    s.revoke_api_credential("cred1", _NOW)               # revocation is plan/quota-independent
    assert s.get_api_credential("cred1")["status"] == "revoked"
    # exhausting quota does not un-revoke or change the credential
    a2 = _account(s, "acct_2", plan=ZERO)
    q.consume_quota(s, a2, METER, now=_EPOCH)
    assert s.get_api_credential("cred1")["status"] == "revoked"


# 10 — idempotent retry: repeated identical logical consumption does not double-count.
def test_idempotent_retry_does_not_double_count(tmp_path):
    s = _store(tmp_path)
    a = _account(s, plan=DEFAULT)                        # limit 2
    d1 = q.consume_quota(s, a, METER, now=_EPOCH, idempotency_key="k1")
    d2 = q.consume_quota(s, a, METER, now=_EPOCH, idempotency_key="k1")
    assert d1.allowed is True and d2.allowed is True
    assert q.evaluate_quota(s, a, METER, now=_EPOCH).used == 1     # counted once


# 10b — same idempotency key + different amount → conflict, no second consumption.
def test_same_key_different_amount_is_conflict(tmp_path):
    s = _store(tmp_path)
    a = _account(s, plan=DEFAULT)
    q.consume_quota(s, a, METER, amount=1, now=_EPOCH, idempotency_key="k1")
    d = q.consume_quota(s, a, METER, amount=2, now=_EPOCH, idempotency_key="k1")
    assert d.allowed is False and d.outcome == q.OUTCOME_DENIED_INVALID
    assert q.evaluate_quota(s, a, METER, now=_EPOCH).used == 1     # unchanged


# 11 — concurrent final-slot consumption cannot oversubscribe a hard cap.
def test_concurrent_final_slot_no_oversubscription(tmp_path):
    s = _store(tmp_path)
    a = _account(s, plan=DEFAULT)                        # limit 2
    results = []
    barrier = threading.Barrier(6)

    def worker(i):
        barrier.wait()
        try:
            results.append(q.consume_quota(s, a, METER, now=_EPOCH,
                                           idempotency_key="w%d" % i).allowed)
        except Exception:
            results.append(False)

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(6)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert sum(1 for r in results if r) == 2            # exactly the cap, never 3+
    assert q.evaluate_quota(s, a, METER, now=_EPOCH).used == 2


# 12 — consumption amount / integer safety.
@pytest.mark.parametrize("amount", [0, -1, 1.5, "1"])
def test_invalid_amount_rejected(tmp_path, amount):
    s = _store(tmp_path)
    a = _account(s, plan=UNLIMITED_PLAN)
    with pytest.raises(q.QuotaError):
        q.consume_quota(s, a, METER, amount=amount, now=_EPOCH)
    assert q.evaluate_quota(s, a, METER, now=_EPOCH).used == 0


def test_unlimited_plan_allows_and_records(tmp_path):
    s = _store(tmp_path)
    a = _account(s, plan=UNLIMITED_PLAN)
    for _ in range(3):
        assert q.consume_quota(s, a, METER, now=_EPOCH).allowed is True
    assert q.evaluate_quota(s, a, METER, now=_EPOCH).used == 3


# 13 — quota policy is derived at evaluation (no per-account snapshot).
def test_quota_policy_is_derived_not_snapshot(tmp_path, monkeypatch):
    s = _store(tmp_path)
    a = _account(s, plan=DEFAULT)                        # limit 2
    assert q.consume_quota(s, a, METER, now=_EPOCH).allowed is True   # used 1
    before_assignment = s.get_commercial_assignment(a)
    # Tighten the reviewed catalog limit to 1 — no per-account write.
    patched = dict(plan_catalog._QUOTA_CATALOG)
    patched[DEFAULT] = {METER: {"limit": 1, "window": {"kind": "lifetime"}}}
    monkeypatch.setattr(plan_catalog, "_QUOTA_CATALOG", patched)
    d = q.consume_quota(s, a, METER, now=_EPOCH)         # now already at new limit → deny
    assert d.outcome == q.OUTCOME_DENIED_EXHAUSTED
    assert s.get_commercial_assignment(a) == before_assignment       # no per-account rewrite


# 14 — quota decrease below already-consumed usage remains safe (no negative, no delete).
def test_quota_decrease_below_usage_is_safe(tmp_path, monkeypatch):
    s = _store(tmp_path)
    a = _account(s, plan=DEFAULT)                        # limit 2
    q.consume_quota(s, a, METER, now=_EPOCH)
    q.consume_quota(s, a, METER, now=_EPOCH)             # used 2
    patched = dict(plan_catalog._QUOTA_CATALOG)
    patched[DEFAULT] = {METER: {"limit": 1, "window": {"kind": "lifetime"}}}   # now below usage
    monkeypatch.setattr(plan_catalog, "_QUOTA_CATALOG", patched)
    dec = q.evaluate_quota(s, a, METER, now=_EPOCH)
    assert dec.used == 2 and dec.remaining == 0          # floored, not negative; data intact
    assert q.consume_quota(s, a, METER, now=_EPOCH).outcome == q.OUTCOME_DENIED_EXHAUSTED


# 15 — existing Owner data remains readable/exportable, and the Owner's own
#      account data-rights operation (deletion) still works, when the commercial
#      creation quota is exhausted. Uses the REAL existing engine seams; quota
#      does not gate them. (record_store is append/read-only — there is no
#      record delete seam to invent; the Owner data-rights delete seam that
#      exists is the account-level `set_status('deleted')`.)
def test_owner_data_access_not_blocked_by_quota(tmp_path):
    from engine.record_store import SqliteRecordStore
    from engine.record_contract import ProjectRecordContract
    from engine.idea_state import AssertionRecord, OWNER_STATED, UNVALIDATED
    from engine import read_export_service
    s = _store(tmp_path)
    a = _account(s, plan=ZERO)                           # commercial creation quota exhausted
    assert q.consume_quota(s, a, METER, now=_EPOCH).outcome == q.OUTCOME_DENIED_EXHAUSTED
    rs = SqliteRecordStore(str(tmp_path / "rec.sqlite3"))
    contract = ProjectRecordContract(idea_id="idea-1", assertions=[
        AssertionRecord(record_id="r1", disposition="answered", content="c",
                        gap_context="g", iteration=1, provenance=OWNER_STATED,
                        validation_status=UNVALIDATED)])
    rs.create_project(contract, project_id="p1", owner_account_id=a)
    # READ of already-owned data — unaffected by commercial quota exhaustion.
    assert rs.load_contract("p1").idea_id == "idea-1"
    # EXPORT of already-owned data via the real P7-I1 seam — unaffected.
    assert read_export_service.produce_project_export(rs, "p1", a)["idea_id"] == "idea-1"
    # Owner account data-rights DELETE — unaffected by commercial quota.
    assert s.set_status(a, "deleted", _NOW) == 1
    assert s.get_account_by_id(a)["status"] == "deleted"


# 16 — OD-N behavioral: technical evaluation invariant to quota state.
def test_od_n_technical_truth_invariant_to_quota(tmp_path):
    s = _store(tmp_path)
    a = _account(s, plan=DEFAULT)
    baseline = domain_activation.support_state("electronics_electrical")
    q.consume_quota(s, a, METER, now=_EPOCH)             # consume commercial quota
    q.consume_quota(s, a, METER, now=_EPOCH)             # exhaust
    q.consume_quota(s, a, METER, now=_EPOCH)             # denied
    assert domain_activation.support_state("electronics_electrical") == baseline


# 17 — engine-wide commercial isolation incl. quota_service + no commercial
#      dynamic imports under engine/.
def test_engine_wide_commercial_isolation_includes_quota():
    allowlist = {"entitlement_service", "quota_service"}       # the only commercial seams
    commercial = {"plan_catalog", "entitlement_service", "quota_service"}
    engine_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "engine")
    static_offenders, dynamic_offenders = [], []
    for fn in os.listdir(engine_dir):
        if not fn.endswith(".py"):
            continue
        modname = fn[:-3]
        src = open(os.path.join(engine_dir, fn), encoding="utf-8").read()
        tree = ast.parse(src)
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
        if modname not in allowlist and (imported & commercial):
            static_offenders.append((fn, sorted(imported & commercial)))
        # No string-based dynamic import of a commercial module from a non-seam.
        if modname not in allowlist:
            for c in commercial:
                if ("import_module(" in src and c in src) or ("__import__(" in src and c in src):
                    dynamic_offenders.append((fn, c))
    assert static_offenders == [], "static commercial leak: %r" % static_offenders
    assert dynamic_offenders == [], "dynamic commercial import: %r" % dynamic_offenders


# 18 — TRUE prior-schema → P8-I2 additive migration (genuine pre-P8-I2 DB).
def test_true_prior_schema_additive_migration(tmp_path):
    path = str(tmp_path / "prior.sqlite3")
    # Build a faithful pre-P8-I2 DB: accounts + commercial_assignments ONLY,
    # WITHOUT the P8-I2 usage tables, via raw SQL.
    conn = sqlite3.connect(path)
    conn.executescript(
        "CREATE TABLE accounts (account_id TEXT PRIMARY KEY, email_normalized TEXT "
        "NOT NULL UNIQUE, email_verified INTEGER NOT NULL DEFAULT 0, status TEXT NOT "
        "NULL DEFAULT 'active', password_hash TEXT NOT NULL, session_epoch INTEGER "
        "NOT NULL DEFAULT 0, created_at TEXT NOT NULL, updated_at TEXT NOT NULL, "
        "deleted_at TEXT);"
        "CREATE TABLE commercial_assignments (account_id TEXT PRIMARY KEY, plan_id "
        "TEXT NOT NULL, plan_version TEXT NOT NULL, assigned_at TEXT NOT NULL, "
        "updated_at TEXT NOT NULL);"
        "INSERT INTO accounts VALUES ('old','old@ex.test',1,'active','h',0,'t','t',NULL);"
        "INSERT INTO commercial_assignments VALUES ('old','__default_technical__','1','t','t');")
    conn.commit()
    conn.close()
    # No P8-I2 usage table yet.
    conn = sqlite3.connect(path)
    tables_before = {r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'")}
    conn.close()
    assert "commercial_usage" not in tables_before
    # Open with candidate store → additive creation, old data intact, no backfill.
    s = SqliteAccountStore(path)
    assert s.get_account_by_id("old")["email_verified"] is True
    assert s.get_commercial_assignment("old")["plan_id"] == "__default_technical__"
    assert s.get_commercial_usage("old", METER, "lifetime") == 0     # new table present, empty


# 19 — fresh DB initializes the commercial usage tables.
def test_fresh_db_has_usage_tables(tmp_path):
    s = _store(tmp_path, "fresh.sqlite3")
    assert s.get_commercial_usage("nobody", METER, "lifetime") == 0


# 20 — rollback / atomicity: a forced failure rolls back BOTH counter and
#      idempotency (no partial/unaudited consumption).
def test_consumption_is_atomic(tmp_path, monkeypatch):
    s = _store(tmp_path)
    a = _account(s, plan=DEFAULT)

    def boom(*args, **kwargs):
        raise RuntimeError("forced idempotency-write failure")

    monkeypatch.setattr(s, "_insert_quota_idempotency", boom)
    with pytest.raises(RuntimeError):
        q.consume_quota(s, a, METER, now=_EPOCH, idempotency_key="kX")
    assert q.evaluate_quota(s, a, METER, now=_EPOCH).used == 0        # counter rolled back too


# 21 — a fixed-window quota resets across windows deterministically (injectable clock).
def test_fixed_window_resets_across_windows(tmp_path):
    s = _store(tmp_path)
    a = _account(s, plan=FIXED)                          # limit 1, fixed 3600s window
    assert q.consume_quota(s, a, METER, now=_EPOCH).allowed is True
    assert q.consume_quota(s, a, METER, now=_EPOCH).outcome == q.OUTCOME_DENIED_EXHAUSTED
    # Next window (advance beyond 3600s) → allowed again.
    assert q.consume_quota(s, a, METER, now=_EPOCH + 3600).allowed is True


# R1-A — evaluate_quota (read-only) for a finite quota with used == limit must
#        DENY (not fail open); no mutation.
def test_evaluate_quota_denies_when_finite_limit_reached(tmp_path):
    s = _store(tmp_path)
    a = _account(s, plan=DEFAULT)                        # limit 2
    q.consume_quota(s, a, METER, now=_EPOCH)
    q.consume_quota(s, a, METER, now=_EPOCH)             # used == limit == 2
    before = s.get_commercial_usage(a, METER, "lifetime")
    d = q.evaluate_quota(s, a, METER, now=_EPOCH)
    assert d.outcome == q.OUTCOME_DENIED_EXHAUSTED
    assert d.allowed is False
    assert d.remaining == 0
    assert d.used == 2
    assert s.get_commercial_usage(a, METER, "lifetime") == before   # read-only, no mutation


# R1-B — evaluate_quota for an explicit zero-limit policy (used == 0) must DENY.
def test_evaluate_quota_denies_zero_limit_from_start(tmp_path):
    s = _store(tmp_path)
    a = _account(s, plan=ZERO)                           # limit 0
    d = q.evaluate_quota(s, a, METER, now=_EPOCH)
    assert d.outcome == q.OUTCOME_DENIED_EXHAUSTED
    assert d.allowed is False
    assert d.remaining == 0
    assert s.get_commercial_usage(a, METER, "lifetime") == 0        # no mutation


# R1-C — evaluate_quota for an UNLIMITED policy stays allowed (unchanged).
def test_evaluate_quota_unlimited_stays_allowed(tmp_path):
    s = _store(tmp_path)
    a = _account(s, plan=UNLIMITED_PLAN)
    d = q.evaluate_quota(s, a, METER, now=_EPOCH)
    assert d.outcome == q.OUTCOME_ALLOWED and d.allowed is True and d.remaining is None


# Cleanup — lifetime consumption with now=None must not persist the literal
# string "None" as the usage timestamp (data-quality fix; no semantic change).
def test_lifetime_consumption_timestamp_not_none_literal(tmp_path):
    s = _store(tmp_path)
    a = _account(s, plan=DEFAULT)                        # lifetime window
    assert q.consume_quota(s, a, METER).allowed is True  # now defaults to None
    with s._read() as c:
        ts = c.execute("SELECT updated_at FROM commercial_usage "
                       "WHERE account_id = ? AND meter = ?", (a, METER)).fetchone()[0]
    assert ts != "None"


# Cleanup — an idempotency key identifies ONE logical consumption; replaying the
# same key in a LATER quota window does not re-consume in that window.
def test_idempotency_key_replay_in_later_window_does_not_reconsume(tmp_path):
    s = _store(tmp_path)
    a = _account(s, plan=FIXED)                          # limit 1, fixed 3600s window
    assert q.consume_quota(s, a, METER, now=_EPOCH, idempotency_key="kw").allowed is True
    d = q.consume_quota(s, a, METER, now=_EPOCH + 3600, idempotency_key="kw")
    assert d.allowed is True                             # prior-outcome replay, not a new consume
    # The later window's own counter was not incremented by the replay.
    from engine.quota_service import _window_key
    later_key = _window_key({"kind": "fixed", "seconds": 3600}, _EPOCH + 3600)
    assert s.get_commercial_usage(a, METER, later_key) == 0
