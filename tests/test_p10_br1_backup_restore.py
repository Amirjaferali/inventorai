"""P10-BR1 — Durable-Database Backup & Restore Drill (RED/GREEN).

Behaviour-based tests for the Owner-authorized bounded Phase-10 implementation
gate `P10-BR1 — Durable-Database Backup & Restore Drill Increment`:
provider-neutral, filesystem-local, SQLite-consistent backup + restore +
validation + parity for the authoritative InventorAI durable datastore
(`engine/account_store.py` + `engine/record_store.py`, one shared
`INVENTORAI_DB_PATH` file).

Load-bearing safety properties proven here:
  * backup uses the SQLite online-backup mechanism (never a raw copy of a live
    file) and NEVER modifies the source database;
  * the source is opened read-only and a missing source is a fail-closed error
    (no silent empty-DB creation);
  * restore goes to a SEPARATE explicit target and never silently overwrites
    an existing database (overwrite is explicit and guarded);
  * corrupt / non-SQLite input fails closed at both backup and restore, leaving
    no partial output behind;
  * parity is verified against the CURRENT dynamically-derived schema inventory
    (no hard-coded historical table count);
  * restored databases open through the normal repository stores.

Real on-disk SQLite only (autouse conftest isolation); real account/record
stores; real web routes for representative population; synthetic data only.
No test ever touches the shared local-development database, and no generated
`.db`/backup artifact is committed.
"""
import hashlib
import os
import sqlite3

import pytest

import web.app as webapp
from web.app import app
from engine import account_credentials as _acct
from engine.account_store import SqliteAccountStore
from engine.record_store import SqliteRecordStore

from engine.backup_service import (
    BackupError,
    backup_database,
    restore_database,
    validate_sqlite_database,
    database_parity_report,
)

PW = "correct horse battery staple"
IDEA = ("An electronic circuit uses a sensor and a switch to cut the power "
        "when the current gets too high.")
FORM = {"idea": IDEA, "domain_confirm": "electronics_electrical"}
NOW = "2026-01-01T00:00:00.000000Z"
LATER = "2026-01-01T01:00:00.000000Z"


# --------------------------------------------------------------------------
# helpers (synthetic data; real seams only)
# --------------------------------------------------------------------------
@pytest.fixture
def db_path():
    return os.environ["INVENTORAI_DB_PATH"]


def _new_client():
    app.config["TESTING"] = True
    return app.test_client()


def _mk_account(email, verified=True):
    store = webapp._get_account_store()
    aid = "acct-" + hashlib.sha256(email.encode()).hexdigest()[:12]
    store.create_account(aid, _acct.normalize_email(email),
                         _acct.hash_password(PW), NOW)
    if verified:
        store.mark_email_verified(aid, NOW)
    return aid


def _login(email):
    c = _new_client()
    r = c.post("/login", data={"email": email, "password": PW})
    assert r.status_code == 302, r.status_code
    return c


def _start_project(client):
    r = client.post("/start", data=FORM)
    assert r.status_code == 302, r.status_code
    return r.headers["Location"].rsplit("/session/", 1)[-1]


def _populate_source():
    """Representative durable data through REAL repository seams only:
    accounts, email_tokens, auth_rate_limits, commercial_assignments,
    commercial_audit, projects, records. Remaining scaffold tables stay empty
    and participate through schema + zero-row parity. Returns evidence keys."""
    aid_a = _mk_account("br1-alpha@example.com")
    aid_b = _mk_account("br1-beta@example.com", verified=False)
    store = webapp._get_account_store()
    store.create_email_token("tok-br1-1", aid_b, "verification",
                             _acct.hash_token("raw-br1-token"), LATER, NOW)
    store.record_rate_attempt("subject-br1", "login", NOW, LATER, 10)
    store.set_commercial_assignment(aid_a, "free", "v1", NOW)
    client = _login("br1-alpha@example.com")
    sid = _start_project(client)
    return {"aid_a": aid_a, "aid_b": aid_b, "sid": sid}


def _file_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _sqlite_master(path):
    conn = sqlite3.connect("file:%s?mode=ro" % path, uri=True)
    try:
        return sorted(conn.execute(
            "SELECT type, name, tbl_name, sql FROM sqlite_master "
            "WHERE name NOT LIKE 'sqlite_%'").fetchall())
    finally:
        conn.close()


def _table_names(path):
    return sorted(r[1] for r in _sqlite_master(path) if r[0] == "table")


def _row_counts(path):
    conn = sqlite3.connect("file:%s?mode=ro" % path, uri=True)
    try:
        return {t: conn.execute('SELECT COUNT(*) FROM "%s"' % t).fetchone()[0]
                for t in _table_names(path)}
    finally:
        conn.close()


def _reference_schema_tables(tmp_path):
    """Dynamically derive the CURRENT full durable-table inventory by
    initializing both real stores on a fresh file. Deliberately NOT a
    hard-coded historical count."""
    ref = str(tmp_path / "reference-schema.sqlite")
    SqliteAccountStore(ref).close()
    SqliteRecordStore(ref).close()
    return _table_names(ref)


# ==========================================================================
# Backup creation + validation
# ==========================================================================
def test_backup_creates_validated_consistent_backup(db_path, tmp_path):
    _populate_source()
    dest = str(tmp_path / "backup.sqlite")
    result = backup_database(db_path, dest)
    assert os.path.isfile(dest)
    assert result["backup_path"] == dest
    assert result["quick_check"] == "ok"
    report = validate_sqlite_database(dest)
    assert report["quick_check"] == "ok"
    assert "accounts" in report["tables"] and "records" in report["tables"]


def test_backup_source_completely_unmodified(db_path, tmp_path):
    keys = _populate_source()
    before_hash = _file_sha256(db_path)
    before_counts = _row_counts(db_path)
    backup_database(db_path, str(tmp_path / "b.sqlite"))
    assert _file_sha256(db_path) == before_hash
    assert _row_counts(db_path) == before_counts
    row = webapp._get_account_store().get_account_by_id(keys["aid_a"])
    assert row is not None and row["status"] == "active"


def test_backup_with_live_store_connections_open(db_path, tmp_path):
    """The application stores hold open connections while the backup runs —
    the online-backup mechanism must produce a valid consistent snapshot."""
    _populate_source()
    assert webapp._ACCOUNT_STORE is not None      # live connection open
    dest = str(tmp_path / "live.sqlite")
    backup_database(db_path, dest)
    assert validate_sqlite_database(dest)["quick_check"] == "ok"


def test_backup_missing_source_fails_closed(tmp_path):
    missing = str(tmp_path / "does-not-exist.sqlite")
    dest = str(tmp_path / "never.sqlite")
    with pytest.raises(BackupError):
        backup_database(missing, dest)
    assert not os.path.exists(missing)   # no silent empty source DB created
    assert not os.path.exists(dest)      # no output artifact


def test_backup_rejects_non_sqlite_source(tmp_path):
    garbage = tmp_path / "garbage.sqlite"
    garbage.write_bytes(b"this is not a sqlite database at all" * 30)
    dest = str(tmp_path / "never.sqlite")
    with pytest.raises(BackupError):
        backup_database(str(garbage), dest)
    assert not os.path.exists(dest)      # no partial output left behind


def test_backup_same_path_rejected(db_path, tmp_path):
    _populate_source()
    with pytest.raises(BackupError):
        backup_database(db_path, db_path)
    # different spelling of the same file must also be rejected
    alias = os.path.join(os.path.dirname(db_path), ".",
                         os.path.basename(db_path))
    with pytest.raises(BackupError):
        backup_database(db_path, alias)
    assert validate_sqlite_database(db_path)["quick_check"] == "ok"


def test_backup_destination_collision_requires_explicit_overwrite(db_path, tmp_path):
    _populate_source()
    dest = tmp_path / "existing.sqlite"
    dest.write_bytes(b"pre-existing destination content")
    with pytest.raises(BackupError):
        backup_database(db_path, str(dest))
    assert dest.read_bytes() == b"pre-existing destination content"
    backup_database(db_path, str(dest), overwrite=True)
    assert validate_sqlite_database(str(dest))["quick_check"] == "ok"


def test_backup_destination_parent_missing_fails_closed(db_path, tmp_path):
    _populate_source()
    dest = str(tmp_path / "no-such-dir" / "backup.sqlite")
    with pytest.raises(BackupError):
        backup_database(db_path, dest)
    assert not os.path.exists(dest)


# ==========================================================================
# Restore + parity
# ==========================================================================
def _backup_then_restore(db_path, tmp_path):
    backup = str(tmp_path / "drill-backup.sqlite")
    target = str(tmp_path / "drill-restored.sqlite")
    backup_database(db_path, backup)
    restore_database(backup, target)
    return backup, target


def test_restore_schema_and_table_inventory_parity(db_path, tmp_path):
    _populate_source()
    _, target = _backup_then_restore(db_path, tmp_path)
    assert _sqlite_master(target) == _sqlite_master(db_path)
    # every durable table of the CURRENT authoritative schema is present —
    # inventory derived live from both real stores, never hard-coded
    expected = _reference_schema_tables(tmp_path)
    assert expected  # sanity: dynamic derivation produced a real inventory
    assert set(expected).issubset(set(_table_names(target)))


def test_restore_row_count_parity_every_table(db_path, tmp_path):
    _populate_source()
    _, target = _backup_then_restore(db_path, tmp_path)
    assert _row_counts(target) == _row_counts(db_path)
    report = database_parity_report(db_path, target)
    assert report["schema_equal"] is True
    assert report["row_counts_equal"] is True
    assert report["mismatches"] == []


def test_restore_semantic_record_parity_via_real_stores(db_path, tmp_path):
    keys = _populate_source()
    src_store = webapp._get_account_store()
    src_row = src_store.get_account_by_id(keys["aid_a"])
    src_owner = webapp._get_store().load_owner(keys["sid"])
    src_evidence = webapp._get_store().load_accepted_answer_evidence(keys["sid"])
    _, target = _backup_then_restore(db_path, tmp_path)
    acct = SqliteAccountStore(target)
    rec = SqliteRecordStore(target)
    try:
        row = acct.get_account_by_id(keys["aid_a"])
        assert row == src_row                     # identity/hash/status/epoch
        unverified = acct.get_account_by_id(keys["aid_b"])
        assert unverified["email_verified"] == 0
        assert rec.load_owner(keys["sid"]) == src_owner
        assert src_owner[-1] == keys["aid_a"]      # owner id inside the tuple
        assert rec.load_accepted_answer_evidence(keys["sid"]) == src_evidence
        assert keys["sid"] in rec.project_ids_for_owner(keys["aid_a"])
    finally:
        acct.close()
        rec.close()


def test_restore_target_is_separate_and_source_untouched(db_path, tmp_path):
    _populate_source()
    before_hash = _file_sha256(db_path)
    backup, target = _backup_then_restore(db_path, tmp_path)
    assert len({os.path.realpath(p) for p in (db_path, backup, target)}) == 3
    assert _file_sha256(db_path) == before_hash


def test_restore_refuses_existing_target_without_overwrite(db_path, tmp_path):
    _populate_source()
    backup = str(tmp_path / "b.sqlite")
    backup_database(db_path, backup)
    target = tmp_path / "occupied.sqlite"
    target.write_bytes(b"live-looking database bytes")
    with pytest.raises(BackupError):
        restore_database(backup, str(target))
    assert target.read_bytes() == b"live-looking database bytes"
    restore_database(backup, str(target), overwrite=True)
    assert validate_sqlite_database(str(target))["quick_check"] == "ok"


def test_restore_rejects_corrupt_backup(db_path, tmp_path):
    _populate_source()
    corrupt = tmp_path / "corrupt.sqlite"
    corrupt.write_bytes(b"\x00\x01broken" * 100)
    target = str(tmp_path / "never.sqlite")
    with pytest.raises(BackupError):
        restore_database(str(corrupt), target)
    assert not os.path.exists(target)


def test_restore_rejects_truncated_real_backup(db_path, tmp_path):
    """A truncated copy of a REAL backup (valid header, broken body) must
    fail validation, not restore silently."""
    _populate_source()
    backup = str(tmp_path / "b.sqlite")
    backup_database(db_path, backup)
    truncated = tmp_path / "truncated.sqlite"
    truncated.write_bytes(open(backup, "rb").read()[:600])
    with pytest.raises(BackupError):
        restore_database(str(truncated), str(tmp_path / "never.sqlite"))
    assert not os.path.exists(str(tmp_path / "never.sqlite"))


def test_restore_same_path_rejected(db_path, tmp_path):
    _populate_source()
    backup = str(tmp_path / "b.sqlite")
    backup_database(db_path, backup)
    with pytest.raises(BackupError):
        restore_database(backup, backup)
    assert validate_sqlite_database(backup)["quick_check"] == "ok"


# ==========================================================================
# Validation seam, repeatability, empty DB, no data exposure
# ==========================================================================
def test_validate_fails_closed_on_missing_and_invalid(tmp_path):
    with pytest.raises(BackupError):
        validate_sqlite_database(str(tmp_path / "missing.sqlite"))
    bad = tmp_path / "bad.sqlite"
    bad.write_bytes(b"not a database")
    with pytest.raises(BackupError):
        validate_sqlite_database(str(bad))


def test_validate_required_tables_enforced(db_path, tmp_path):
    _populate_source()
    report = validate_sqlite_database(db_path,
                                      required_tables=("accounts", "records"))
    assert report["quick_check"] == "ok"
    with pytest.raises(BackupError):
        validate_sqlite_database(db_path,
                                 required_tables=("accounts", "no_such_table"))


def test_repeated_backup_deterministic_and_resources_released(db_path, tmp_path):
    _populate_source()
    for i in range(3):
        dest = str(tmp_path / ("repeat-%d.sqlite" % i))
        backup_database(db_path, dest)
        report = database_parity_report(db_path, dest)
        assert report["schema_equal"] and report["row_counts_equal"]
        # resources released: the backup file is immediately removable
        os.remove(dest)
    assert validate_sqlite_database(db_path)["quick_check"] == "ok"


def test_empty_but_valid_database_roundtrip(tmp_path):
    source = str(tmp_path / "empty-valid.sqlite")
    SqliteAccountStore(source).close()
    SqliteRecordStore(source).close()
    backup = str(tmp_path / "empty-backup.sqlite")
    target = str(tmp_path / "empty-restored.sqlite")
    backup_database(source, backup)
    restore_database(backup, target)
    report = database_parity_report(source, target)
    assert report["schema_equal"] and report["row_counts_equal"]
    assert all(count == 0 for count in _row_counts(target).values())


def test_results_expose_no_data_contents(db_path, tmp_path):
    _populate_source()
    dest = str(tmp_path / "b.sqlite")
    result = backup_database(db_path, dest)
    validation = validate_sqlite_database(dest)
    parity = database_parity_report(db_path, dest)
    blob = repr((result, validation, parity))
    assert "br1-alpha@example.com" not in blob
    assert "raw-br1-token" not in blob
    assert PW not in blob and IDEA[:20] not in blob
