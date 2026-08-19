"""P10-BR1 — provider-neutral SQLite backup / restore / validation service.

File path: ``engine/backup_service.py``
Purpose:   the smallest reusable seam for creating a CONSISTENT backup of the
           InventorAI durable SQLite datastore, validating a backup, restoring
           it to a SEPARATE explicit target, and producing a schema/row-count
           parity report. Local-filesystem, standard-library only.

Input contract:
  * every operation takes EXPLICIT source/backup/target paths — nothing is
    inferred from the environment, and the live application database path is
    never assumed or defaulted;
  * ``overwrite`` is explicit and defaults to ``False`` everywhere.

Output contract:
  * operations return small deterministic dicts (paths, ``quick_check``
    result, sorted table-name inventory, mismatch labels). They NEVER include
    row contents, emails, hashes, tokens, or any stored user data;
  * every failure raises ``BackupError`` (fail closed) and leaves NO partial
    final output file behind.

Prohibited behaviors (binding, per the P10-BR1 authorization):
  * NO raw file copy of a live database as the backup mechanism — backups and
    restores use the SQLite online-backup API (``sqlite3.Connection.backup``);
  * NO modification of the source database (sources are opened read-only);
  * NO silent creation of a missing source database;
  * NO silent overwrite of an existing destination/target;
  * NO retention policy, scheduling, rotation, or deletion of prior backups;
  * NO cloud/provider/offsite dependency of any kind;
  * NO schema change, migration, or data mutation of any database.
"""
import os
import sqlite3
from urllib.request import pathname2url

_BUSY_TIMEOUT_SECONDS = 5.0
# Namespaced temporary suffix so an interrupted operation can never be
# mistaken for (or leave behind) a final backup/restore artifact.
_INPROGRESS_SUFFIX = ".p10br1-inprogress"


class BackupError(Exception):
    """Single fail-closed error type for every backup/restore/validation
    failure. Messages carry paths and reasons only — never database contents."""


def _open_readonly(path):
    """Open an EXISTING SQLite file strictly read-only (URI ``mode=ro``).
    Cannot create a missing file and cannot write to the source."""
    uri = "file:%s?mode=ro" % pathname2url(os.path.abspath(path))
    return sqlite3.connect(uri, uri=True, timeout=_BUSY_TIMEOUT_SECONDS)


def _quick_check_and_tables(conn):
    """Run ``PRAGMA quick_check`` and collect the user-table inventory on an
    open connection. Raises ``BackupError`` on any corruption signal."""
    rows = conn.execute("PRAGMA quick_check").fetchall()
    if rows != [("ok",)]:
        raise BackupError("SQLite quick_check failed: %d finding(s)" % len(rows))
    tables = sorted(
        r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type = 'table' AND name NOT LIKE 'sqlite_%'").fetchall())
    return tables


def validate_sqlite_database(path, required_tables=None):
    """Fail-closed validation of one SQLite database file.

    Verifies: the file exists; SQLite opens it read-only; ``PRAGMA
    quick_check`` reports ``ok``; and (when given) every name in
    ``required_tables`` exists. Returns ``{"path", "quick_check", "tables"}``
    — table NAMES only, never contents."""
    if not os.path.isfile(path):
        raise BackupError("database file does not exist: %s" % path)
    try:
        conn = _open_readonly(path)
    except sqlite3.Error as exc:
        raise BackupError("cannot open %s as SQLite: %s" % (path, exc)) from exc
    try:
        try:
            tables = _quick_check_and_tables(conn)
        except sqlite3.Error as exc:
            raise BackupError(
                "%s is not a readable SQLite database: %s" % (path, exc)) from exc
    finally:
        conn.close()
    if required_tables:
        missing = sorted(set(required_tables) - set(tables))
        if missing:
            raise BackupError(
                "%s is missing required table(s): %s" % (path, ", ".join(missing)))
    return {"path": path, "quick_check": "ok", "tables": tuple(tables)}


def _check_destination(source_path, destination_path, overwrite):
    """Shared destination guards: never the source file itself, parent
    directory must already exist (no silent directory creation), and an
    existing destination requires an explicit ``overwrite=True``."""
    if os.path.realpath(source_path) == os.path.realpath(destination_path):
        raise BackupError(
            "destination must be a different file than the source: %s"
            % destination_path)
    parent = os.path.dirname(os.path.abspath(destination_path))
    if not os.path.isdir(parent):
        raise BackupError(
            "destination directory does not exist: %s" % parent)
    if os.path.exists(destination_path) and not overwrite:
        raise BackupError(
            "destination already exists (pass overwrite=True to replace): %s"
            % destination_path)


def _consistent_copy(source_path, destination_path):
    """Copy ``source_path`` into ``destination_path`` using the SQLite
    online-backup API via an in-progress temporary file, then atomically move
    it into place. The source is opened read-only; a failure removes the
    in-progress file so no partial output survives. Returns the validated
    destination table inventory."""
    inprogress = destination_path + _INPROGRESS_SUFFIX
    if os.path.exists(inprogress):
        # Leftover from a previously interrupted run of THIS operation only
        # (namespaced suffix); never a user file.
        os.remove(inprogress)
    src = _open_readonly(source_path)
    try:
        dst = sqlite3.connect(inprogress, timeout=_BUSY_TIMEOUT_SECONDS)
        try:
            src.backup(dst)
        finally:
            dst.close()
    except sqlite3.Error as exc:
        if os.path.exists(inprogress):
            os.remove(inprogress)
        raise BackupError(
            "SQLite online backup from %s failed: %s" % (source_path, exc)) from exc
    finally:
        src.close()
    try:
        result = validate_sqlite_database(inprogress)
    except BackupError:
        os.remove(inprogress)
        raise
    os.replace(inprogress, destination_path)
    return result["tables"]


def backup_database(source_path, backup_path, overwrite=False):
    """Create a SQLite-consistent backup of ``source_path`` at ``backup_path``.

    Fail-closed guards: the source must already exist and validate as a real
    SQLite database (a missing source is an error — it is never silently
    created); the destination must differ from the source, its parent
    directory must exist, and an existing destination is only replaced with
    ``overwrite=True``. The source is opened read-only and is never modified.
    The backup is validated (``quick_check`` + table-inventory equality with
    the source) before it is moved into its final path."""
    source_report = validate_sqlite_database(source_path)
    _check_destination(source_path, backup_path, overwrite)
    tables = _consistent_copy(source_path, backup_path)
    if tables != source_report["tables"]:
        os.remove(backup_path)
        raise BackupError(
            "backup table inventory does not match source: %s" % backup_path)
    return {"source_path": source_path, "backup_path": backup_path,
            "quick_check": "ok", "tables": tables}


def restore_database(backup_path, target_path, overwrite=False):
    """Restore a VALIDATED backup into a SEPARATE explicit ``target_path``.

    The backup is fully validated first (fail closed on corrupt/invalid
    input). The target must differ from the backup, its parent directory must
    exist, and an existing target is only replaced with the explicit, guarded
    ``overwrite=True`` — there is no silent overwrite path. The restored
    database is validated and its table inventory compared with the backup
    before it is moved into place."""
    backup_report = validate_sqlite_database(backup_path)
    _check_destination(backup_path, target_path, overwrite)
    tables = _consistent_copy(backup_path, target_path)
    if tables != backup_report["tables"]:
        os.remove(target_path)
        raise BackupError(
            "restored table inventory does not match backup: %s" % target_path)
    return {"backup_path": backup_path, "target_path": target_path,
            "quick_check": "ok", "tables": tables}


def database_parity_report(path_a, path_b):
    """Compare two SQLite databases: full ``sqlite_master`` schema-object
    parity (type/name/parent/SQL of every user table, index, trigger, view)
    and per-table row-count parity across the union of user tables. Both
    files must validate first (fail closed). The report carries object NAMES
    and counts only — never row contents."""
    validate_sqlite_database(path_a)
    validate_sqlite_database(path_b)

    def _schema(path):
        conn = _open_readonly(path)
        try:
            return sorted(conn.execute(
                "SELECT type, name, tbl_name, sql FROM sqlite_master "
                "WHERE name NOT LIKE 'sqlite_%'").fetchall())
        finally:
            conn.close()

    def _counts(path):
        conn = _open_readonly(path)
        try:
            tables = _quick_check_and_tables(conn)
            return {t: conn.execute('SELECT COUNT(*) FROM "%s"' % t).fetchone()[0]
                    for t in tables}
        finally:
            conn.close()

    schema_a, schema_b = _schema(path_a), _schema(path_b)
    counts_a, counts_b = _counts(path_a), _counts(path_b)
    mismatches = []
    if schema_a != schema_b:
        named_a = {(r[0], r[1]) for r in schema_a}
        named_b = {(r[0], r[1]) for r in schema_b}
        for kind, name in sorted(named_a ^ named_b):
            mismatches.append("schema object only on one side: %s %s"
                              % (kind, name))
        for kind, name in sorted(named_a & named_b):
            if ([r for r in schema_a if (r[0], r[1]) == (kind, name)]
                    != [r for r in schema_b if (r[0], r[1]) == (kind, name)]):
                mismatches.append("schema definition differs: %s %s"
                                  % (kind, name))
    for table in sorted(set(counts_a) | set(counts_b)):
        if counts_a.get(table) != counts_b.get(table):
            mismatches.append(
                "row count differs for table %s: %s vs %s"
                % (table, counts_a.get(table), counts_b.get(table)))
    return {"schema_equal": schema_a == schema_b,
            "row_counts_equal":
                all(counts_a.get(t) == counts_b.get(t)
                    for t in set(counts_a) | set(counts_b)),
            "tables_compared": len(set(counts_a) | set(counts_b)),
            "mismatches": mismatches}
