"""STAGE38-DATABASE-STARTUP-SAFETY-01 — production opens an EXISTING database only.

Production never silently replaces the established SQLite database with a new
empty one: every store-opening path (project store, account store, email
dispatcher, backup scheduler) opens with ``create=False`` — URI ``mode=rw``, no
created directory, and a missing, unopenable or unrecognised file refused before
any schema DDL. Background operations start only after production admission,
production ``/health`` is 503 on a missing / unrecognised / replaced file even
with cached connections, the backup pipeline never uploads an unrecognised
database, and creating (``provision``) or restoring the database is an explicit
operator operation. Development and tests keep the original behaviour.
"""
import importlib.util
import json
import os
import sqlite3
import subprocess
import sys

import pytest

import web.app as webapp
from engine import backup_service
from engine.account_store import SqliteAccountStore
from engine.backup_service import (
    INVENTORAI_ANCHOR_TABLES, BackupError, DatabaseNotAdmitted,
    check_existing_database, open_existing_database,
)
from engine.offsite_backup_scheduler import OffsiteBackupScheduler, perform_offsite_backup
from engine.record_store import SqliteRecordStore

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLI_PATH = os.path.join(ROOT, "scripts", "inventorai_backup.py")
SETTINGS = {"INVENTORAI_R2_ACCOUNT_ID": "testaccount",
            "INVENTORAI_R2_BUCKET": "inventorai-backups-test",
            "INVENTORAI_R2_ACCESS_KEY_ID": "TESTONLYACCESSKEYID",
            "INVENTORAI_R2_SECRET_ACCESS_KEY": "test-only-secret-not-a-real-key",
            "INVENTORAI_R2_PREFIX": "daily"}
OK_BODY = {"database": "ok", "status": "ok"}
ERROR_BODY = {"database": "error", "status": "unavailable"}


def _cli():
    spec = importlib.util.spec_from_file_location("_s38_backup_cli", CLI_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _provision(path):
    assert _cli().main(["provision", str(path)]) == 0
    return str(path)


def _tables(path):
    con = sqlite3.connect("file:%s?mode=ro" % path, uri=True)
    try:
        return {r[0] for r in con.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'")}
    finally:
        con.close()


def _digest(path):
    with open(path, "rb") as handle:
        return handle.read()


def _health(client=None):
    response = (client or webapp.app.test_client()).get("/health")
    return response.status_code, json.loads(response.get_data(as_text=True))


@pytest.fixture
def production(monkeypatch):
    monkeypatch.setenv("INVENTORAI_ENV", "production")
    monkeypatch.setenv("INVENTORAI_SECRET_KEY", "s38-test-not-a-secret")


class _Transport:
    def __init__(self):
        self.calls = []

    def __call__(self, url, headers, path, size, timeout_seconds):
        self.calls.append(path)
        return 200, b"<ok/>"


# ===========================================================================
# the one admission rule (engine/backup_service.py)
# ===========================================================================
def test_missing_file_and_directory_are_refused_and_never_created(tmp_path):
    target = tmp_path / "no-such-dir" / "inventorai.sqlite"
    for opener in (lambda: SqliteRecordStore(str(target), create=False),
                   lambda: SqliteAccountStore(str(target), create=False),
                   lambda: open_existing_database(str(target)),
                   lambda: check_existing_database(str(target))):
        with pytest.raises(DatabaseNotAdmitted):
            opener()
    assert not (tmp_path / "no-such-dir").exists()
    flat = tmp_path / "absent.sqlite"
    with pytest.raises(DatabaseNotAdmitted):
        SqliteRecordStore(str(flat), create=False)
    assert not flat.exists()


@pytest.mark.parametrize("kind", ["zero_bytes", "empty_sqlite", "foreign_sqlite"])
def test_unrecognised_files_are_refused_before_any_ddl(tmp_path, kind):
    path = tmp_path / "db.sqlite"
    if kind == "zero_bytes":
        path.write_bytes(b"")
    else:
        con = sqlite3.connect(str(path))
        if kind == "foreign_sqlite":
            con.execute("CREATE TABLE other (x)")
        else:
            con.execute("CREATE TABLE t (x)")
            con.execute("DROP TABLE t")
        con.commit()
        con.close()
    before = _digest(path)
    for opener in (lambda: SqliteRecordStore(str(path), create=False),
                   lambda: SqliteAccountStore(str(path), create=False),
                   lambda: check_existing_database(str(path))):
        with pytest.raises(DatabaseNotAdmitted):
            opener()
    assert _digest(path) == before                       # no schema written


def test_not_a_database_file_is_refused(tmp_path):
    path = tmp_path / "db.sqlite"
    path.write_bytes(b"this is not a sqlite database" * 64)
    with pytest.raises(DatabaseNotAdmitted):
        SqliteRecordStore(str(path), create=False)
    with pytest.raises(DatabaseNotAdmitted):
        check_existing_database(str(path))


def test_memory_and_uri_names_cannot_be_opened_as_existing():
    for name in (":memory:", "", "file:x.sqlite?mode=rwc"):
        with pytest.raises(DatabaseNotAdmitted):
            open_existing_database(name)
    SqliteRecordStore(":memory:").close()                 # default unchanged


def test_recognised_database_opens_and_keeps_its_data(tmp_path):
    path = _provision(tmp_path / "db.sqlite")
    con = sqlite3.connect(path)
    con.execute("CREATE TABLE sentinel (v TEXT)")
    con.execute("INSERT INTO sentinel VALUES ('kept')")
    con.commit()
    con.close()
    SqliteRecordStore(path, create=False).close()
    SqliteAccountStore(path, create=False).close()
    assert set(INVENTORAI_ANCHOR_TABLES) <= _tables(path)
    con = sqlite3.connect(path)
    assert con.execute("SELECT v FROM sentinel").fetchall() == [("kept",)]
    con.close()


def test_partially_initialised_and_legacy_databases_still_migrate(tmp_path):
    """A recognised database is brought up to date by the stores' own additive
    migrations: an account-only database gains the project tables, a
    project-only (pre-account) database gains the account tables, and a missing
    later table is re-added — legitimate empty tables stay legitimate."""
    account_only = str(tmp_path / "accounts.sqlite")
    SqliteAccountStore(account_only).close()
    assert "projects" not in _tables(account_only)
    SqliteRecordStore(account_only, create=False).close()
    assert {"projects", "records"} <= _tables(account_only)

    project_only = str(tmp_path / "projects.sqlite")
    SqliteRecordStore(project_only).close()
    assert "accounts" not in _tables(project_only)
    SqliteAccountStore(project_only, create=False).close()
    assert "accounts" in _tables(project_only)

    full = _provision(tmp_path / "full.sqlite")
    con = sqlite3.connect(full)
    con.execute("DROP TABLE decision_cell_value_events")
    con.commit()
    con.close()
    SqliteRecordStore(full, create=False).close()
    assert "decision_cell_value_events" in _tables(full)


@pytest.mark.parametrize("name", ["with space.sqlite", "q?mark.sqlite",
                                  "hash#mark.sqlite", "pct%41.sqlite"])
def test_uri_encoding_targets_exactly_the_named_file(tmp_path, name):
    absent = tmp_path / name
    with pytest.raises(DatabaseNotAdmitted):
        SqliteAccountStore(str(absent), create=False)
    assert sorted(os.listdir(tmp_path)) == []             # no stray file
    path = _provision(absent)
    SqliteRecordStore(path, create=False).close()
    assert sorted(os.listdir(tmp_path)) == [name]


# ===========================================================================
# the four application opening paths (web/app.py) in production
# ===========================================================================
def test_production_paths_refuse_and_create_nothing(production, tmp_path, monkeypatch):
    target = tmp_path / "mount-missing" / "inventorai.sqlite"
    monkeypatch.setenv("INVENTORAI_DB_PATH", str(target))
    for opener in (webapp._get_store, webapp._get_account_store,
                   webapp._open_dispatcher_store, webapp._open_offsite_backup_store):
        with pytest.raises(DatabaseNotAdmitted):
            opener()
    assert not (tmp_path / "mount-missing").exists()
    assert webapp._STORE is None and webapp._ACCOUNT_STORE is None


def test_production_paths_open_a_provisioned_database(production, tmp_path, monkeypatch):
    path = _provision(tmp_path / "inventorai.sqlite")
    monkeypatch.setenv("INVENTORAI_DB_PATH", path)
    assert webapp._get_store() is webapp._get_store()
    assert webapp._get_account_store() is webapp._get_account_store()
    webapp._open_dispatcher_store().close()
    webapp._open_offsite_backup_store().close()
    assert sorted(os.listdir(tmp_path)) == ["inventorai.sqlite"]


def test_development_keeps_lazy_creation(tmp_path, monkeypatch):
    monkeypatch.delenv("INVENTORAI_ENV", raising=False)
    target = tmp_path / "new-dir" / "dev.sqlite"
    monkeypatch.setenv("INVENTORAI_DB_PATH", str(target))
    webapp._get_store()
    assert target.exists()
    assert _health() == (200, OK_BODY)


def test_restored_database_is_admitted(production, tmp_path, monkeypatch):
    live = _provision(tmp_path / "live.sqlite")
    store = SqliteAccountStore(live)
    store.close()
    backup = str(tmp_path / "backup.sqlite")
    target = str(tmp_path / "restored.sqlite")
    backup_service.backup_database(live, backup)
    backup_service.restore_database(backup, target)
    monkeypatch.setenv("INVENTORAI_DB_PATH", target)
    assert webapp._production_database_admitted() is True
    webapp._get_account_store()
    assert _health() == (200, OK_BODY)


# ===========================================================================
# production admission and /health
# ===========================================================================
def test_admission_refuses_missing_and_reports_class_only(production, tmp_path,
                                                          monkeypatch):
    events = []
    monkeypatch.setattr(webapp._obs, "emit",
                        lambda event, **fields: events.append((event, fields)))
    monkeypatch.setenv("INVENTORAI_DB_PATH", str(tmp_path / "absent.sqlite"))
    assert webapp._production_database_admitted() is False
    assert events == [("database.admission_refused",
                       {"level": "error", "component": "database",
                        "error_class": "DatabaseNotAdmitted"})]
    assert not (tmp_path / "absent.sqlite").exists()
    monkeypatch.setenv("INVENTORAI_DB_PATH", _provision(tmp_path / "db.sqlite"))
    assert webapp._production_database_admitted() is True


def test_development_admission_is_always_true(monkeypatch, tmp_path):
    monkeypatch.delenv("INVENTORAI_ENV", raising=False)
    monkeypatch.setenv("INVENTORAI_DB_PATH", str(tmp_path / "absent.sqlite"))
    assert webapp._production_database_admitted() is True


def test_production_health_is_503_on_missing_or_unrecognised(production, tmp_path,
                                                             monkeypatch):
    absent = tmp_path / "absent.sqlite"
    monkeypatch.setenv("INVENTORAI_DB_PATH", str(absent))
    assert _health() == (503, ERROR_BODY)
    assert not absent.exists()
    empty = tmp_path / "empty.sqlite"
    empty.write_bytes(b"")
    monkeypatch.setenv("INVENTORAI_DB_PATH", str(empty))
    assert _health() == (503, ERROR_BODY)
    assert empty.read_bytes() == b""
    monkeypatch.setenv("INVENTORAI_DB_PATH", _provision(tmp_path / "db.sqlite"))
    assert _health() == (200, OK_BODY)


def test_production_health_detects_deletion_under_cached_connections(
        production, tmp_path, monkeypatch):
    path = _provision(tmp_path / "db.sqlite")
    monkeypatch.setenv("INVENTORAI_DB_PATH", path)
    webapp._get_store()
    webapp._get_account_store()
    assert _health() == (200, OK_BODY)
    os.remove(path)                                       # cached connections stay open
    assert _health() == (503, ERROR_BODY)
    assert not os.path.exists(path)                       # health recreated nothing


def test_production_health_detects_replacement_under_cached_connections(
        production, tmp_path, monkeypatch):
    path = _provision(tmp_path / "db.sqlite")
    monkeypatch.setenv("INVENTORAI_DB_PATH", path)
    webapp._get_account_store()
    assert _health() == (200, OK_BODY)
    os.remove(path)
    _provision(path)                                      # a different file, same name
    assert _health() == (503, ERROR_BODY)


def test_development_health_contract_unchanged(monkeypatch, tmp_path):
    monkeypatch.delenv("INVENTORAI_ENV", raising=False)
    monkeypatch.setenv("INVENTORAI_DB_PATH", str(tmp_path / "absent.sqlite"))
    assert _health() == (200, {"database": "uninitialized", "status": "ok"})


# ===========================================================================
# background operations: dispatcher and backup scheduler
# ===========================================================================
def test_scheduler_reopen_after_loss_uploads_nothing(production, tmp_path, monkeypatch):
    path = tmp_path / "lost.sqlite"
    monkeypatch.setenv("INVENTORAI_DB_PATH", str(path))
    transport = _Transport()
    scheduler = OffsiteBackupScheduler(
        open_store=webapp._open_offsite_backup_store,
        source_path=webapp._resolve_db_path,
        resolve_settings=lambda: dict(SETTINGS), transport=transport)
    with pytest.raises(DatabaseNotAdmitted):
        scheduler.run_if_due()
    assert transport.calls == []
    assert not path.exists()


def test_dispatcher_reopen_after_loss_creates_nothing(production, tmp_path, monkeypatch):
    path = tmp_path / "lost.sqlite"
    monkeypatch.setenv("INVENTORAI_DB_PATH", str(path))
    with pytest.raises(DatabaseNotAdmitted):
        webapp._EMAIL_DISPATCHER.dispatch_pending()
    assert not path.exists()


@pytest.mark.parametrize("kind", ["empty_sqlite", "foreign_sqlite"])
def test_pipeline_never_uploads_an_unrecognised_database(tmp_path, kind):
    source = str(tmp_path / "source.sqlite")
    con = sqlite3.connect(source)
    con.execute("CREATE TABLE other (x)")
    if kind == "empty_sqlite":
        con.execute("DROP TABLE other")
    con.commit()
    con.close()
    transport = _Transport()
    with pytest.raises(BackupError):
        perform_offsite_backup(source, SETTINGS, transport=transport)
    assert transport.calls == []


def _cold_boot(env_extra, program):
    env = dict(os.environ)
    for name in list(env):
        if name.startswith("INVENTORAI_R2_") or name.startswith("INVENTORAI_EMAIL"):
            env.pop(name)
    env.update({"INVENTORAI_ENV": "production",
                "INVENTORAI_SECRET_KEY": "boot-probe-not-a-real-secret",
                "PYTHONWARNINGS": "ignore"})
    env.update(env_extra)
    return subprocess.run([sys.executable, "-c", program], cwd=ROOT, env=env,
                          capture_output=True, text=True, timeout=180)


def test_production_boot_without_database_starts_no_background_operation(tmp_path):
    path = tmp_path / "mount" / "inventorai.sqlite"
    env = dict(SETTINGS, INVENTORAI_DB_PATH=str(path),
               INVENTORAI_EMAIL_PROVIDER="resend",
               INVENTORAI_RESEND_API_KEY="probe-key-not-real",
               INVENTORAI_EMAIL_FROM="InventorAI <no-reply@example.test>",
               INVENTORAI_PUBLIC_BASE_URL="https://app.example.test")
    result = _cold_boot(
        env,
        "import threading, web.app as w;"
        "assert w._PRODUCTION_DATABASE_ADMITTED is False;"
        "assert w._EMAIL_DISPATCHER_STARTED is False;"
        "assert w._OFFSITE_BACKUP_SCHEDULER_STARTED is False;"
        "assert not [t for t in threading.enumerate() if t.name.startswith('inventorai-')];"
        "print(w.app.test_client().get('/health').status_code)")
    assert result.returncode == 0, result.stderr[-2000:]
    assert result.stdout.strip() == "503"
    assert not (tmp_path / "mount").exists()


def test_production_boot_with_provisioned_database_is_admitted(tmp_path):
    path = _provision(tmp_path / "inventorai.sqlite")
    result = _cold_boot(
        {"INVENTORAI_DB_PATH": path},
        "import web.app as w;"
        "assert w._PRODUCTION_DATABASE_ADMITTED is True;"
        "print(w.app.test_client().get('/health').status_code)")
    assert result.returncode == 0, result.stderr[-2000:]
    assert result.stdout.strip() == "200"


# ===========================================================================
# explicit provisioning (scripts/inventorai_backup.py provision)
# ===========================================================================
def test_provision_creates_a_recognised_database_and_nothing_else(tmp_path):
    path = _provision(tmp_path / "inventorai.sqlite")
    assert set(INVENTORAI_ANCHOR_TABLES) <= _tables(path)
    assert sorted(os.listdir(tmp_path)) == ["inventorai.sqlite"]
    check_existing_database(path)


def test_provision_never_replaces_an_existing_file(tmp_path, capsys):
    path = _provision(tmp_path / "inventorai.sqlite")
    store = SqliteAccountStore(path)
    store.close()
    before = _digest(path)
    assert _cli().main(["provision", path]) == 3
    assert "BACKUP ERROR" in capsys.readouterr().err
    assert _digest(path) == before
    other = tmp_path / "other.sqlite"
    other.write_bytes(b"")
    assert _cli().main(["provision", str(other)]) == 3
    assert other.read_bytes() == b""


def test_provision_creates_no_directory(tmp_path):
    target = tmp_path / "missing-mount" / "inventorai.sqlite"
    assert _cli().main(["provision", str(target)]) == 3
    assert not (tmp_path / "missing-mount").exists()


def test_interrupted_provisioning_leaves_no_database(tmp_path, monkeypatch):
    cli = _cli()
    target = tmp_path / "inventorai.sqlite"
    import engine.account_store as account_store

    class _Interrupted(Exception):
        pass

    def _fail(*_args, **_kwargs):
        raise _Interrupted()
    monkeypatch.setattr(account_store, "SqliteAccountStore", _fail)
    with pytest.raises(BackupError):
        cli.provision_database(str(target))
    assert sorted(os.listdir(tmp_path)) == []             # no target, no leftover
    monkeypatch.undo()
    # a leftover from a hard interruption is discarded by the next run
    leftover = str(target) + cli._PROVISION_INPROGRESS_SUFFIX
    open(leftover, "wb").write(b"partial")
    cli.provision_database(str(target))
    assert sorted(os.listdir(tmp_path)) == ["inventorai.sqlite"]
    check_existing_database(str(target))


def test_provision_never_overwrites_a_concurrently_created_target(tmp_path, monkeypatch):
    cli = _cli()
    target = str(tmp_path / "inventorai.sqlite")
    real_validate = cli.validate_sqlite_database

    def _validate_then_race(path, **kwargs):
        report = real_validate(path, **kwargs)
        with open(target, "wb") as handle:                # another actor wins
            handle.write(b"theirs")
        return report
    monkeypatch.setattr(cli, "validate_sqlite_database", _validate_then_race)
    with pytest.raises(BackupError):
        cli.provision_database(target)
    assert open(target, "rb").read() == b"theirs"
    assert sorted(os.listdir(tmp_path)) == ["inventorai.sqlite"]
