"""OD-INFRA-5 — off-provider (Cloudflare R2) backup operator CLI.

File path: ``scripts/inventorai_offsite_backup.py``
Purpose:   make the Owner-decided DAILY off-provider backup a single runnable,
           schedulable command, composed from the two existing owners:

               engine/backup_service.py   (the ONE backup engine)
                 -> temporary validated SQLite backup
                     -> engine/r2_object_upload.py  (transport only)
                         -> Cloudflare R2

Why this is a SEPARATE script from ``scripts/inventorai_backup.py``: that CLI
states, as a binding boundary, that it uses "NO cloud/provider API of any kind",
which is what makes the backup it produces portable and provider-independent.
That boundary is worth keeping intact rather than eroding, so the provider step
lives here instead. ``scripts/inventorai_backup.py`` is unchanged by this
tranche and remains usable on its own.

What this is NOT:
  * NOT a second backup engine — every byte of the backup is produced by
    ``backup_database`` and validated by ``validate_sqlite_database``. There is
    no SQLite call and no copy logic in this file or in the uploader.
  * NOT a retention manager. There is no delete, expire, rotate or list path
    anywhere in this tranche: retention duration is unresolved in the
    privacy/legal lane, and inventing one here would be a policy decision this
    script has no authority to make. Old objects accumulate until a governed
    retention decision exists.
  * NOT a scheduler. It is schedulable — one command, explicit exit codes, no
    interactive input — but no cron job, Render Cron Job or timer is created by
    this repository. Activating the daily schedule is a separate Owner-side
    provider action.
  * NOT a raw-file uploader. BOTH commands run the backup engine first, so no
    operator-supplied file is ever PUT as-is. A live WAL database's main file
    can pass validation while its committed rows sit in the `-wal` sidecar, and
    shipping that file would store an incomplete artifact as a "backup".
  * NOT a restore path. Restore remains ``scripts/inventorai_backup.py restore``
    against a locally held backup, and repointing ``INVENTORAI_DB_PATH`` stays a
    deliberate human step (DR plan Scenario 7).

Configuration — environment ONLY, never a file, never an argument (so a
credential cannot reach a shell history, a process list, or this repository):
    INVENTORAI_R2_ACCOUNT_ID          Cloudflare account id (forms the endpoint)
    INVENTORAI_R2_BUCKET              destination bucket
    INVENTORAI_R2_ACCESS_KEY_ID       R2 access key id
    INVENTORAI_R2_SECRET_ACCESS_KEY   R2 secret access key
    INVENTORAI_R2_PREFIX              optional object-key prefix (default none)
Absent or blank configuration FAILS CLOSED with a named, value-free message.

Output: a deterministic evidence header plus the uploader's report as sorted
JSON — object key, byte count, SHA-256 of the artifact, provider status. No
credential, signature, authorization header, table name, row or user content is
printed, because none of it is returned to this layer.

Exit codes:
    0  the provider ACCEPTED the object (2xx). Nothing weaker is success.
    2  usage error (argparse)
    3  BackupError    — any fail-closed condition of the backup service
    4  R2UploadError  — missing configuration, rejection, or transport failure
"""
import argparse
import datetime
import json
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.backup_service import (  # noqa: E402  (path set above)
    BackupError,
    backup_database,
    validate_sqlite_database,
)
from engine.r2_object_upload import (  # noqa: E402
    R2UploadError,
    put_object,
)

_EXIT_BACKUP_ERROR = 3
_EXIT_UPLOAD_ERROR = 4

_REQUIRED_SETTINGS = ("INVENTORAI_R2_ACCOUNT_ID", "INVENTORAI_R2_BUCKET",
                      "INVENTORAI_R2_ACCESS_KEY_ID",
                      "INVENTORAI_R2_SECRET_ACCESS_KEY")


def _utc_now():
    return datetime.datetime.now(datetime.timezone.utc)


def _stamp(moment):
    return moment.strftime("%Y%m%dT%H%M%SZ")


def resolve_settings(environ=None):
    """Read the provider configuration from the environment. Fail closed.

    Raises ``R2UploadError('missing_configuration', <NAME>)`` naming only the
    VARIABLE that is absent — never a value, and never a partial value.
    """
    source = environ if environ is not None else os.environ
    resolved = {}
    for name in _REQUIRED_SETTINGS:
        value = (source.get(name) or "").strip()
        if not value:
            raise R2UploadError("missing_configuration", name)
        resolved[name] = value
    resolved["INVENTORAI_R2_PREFIX"] = (
        source.get("INVENTORAI_R2_PREFIX") or "").strip().strip("/")
    return resolved


def object_key(prefix, filename):
    """Compose the destination object key. No timestamp parsing, no collision
    handling that could overwrite silently — the caller supplies a unique name."""
    return "%s/%s" % (prefix, filename) if prefix else filename


def _emit(operation, report, **facts):
    lines = ["InventorAI off-provider backup (existing backup engine + R2 "
             "transport; no second engine, no retention)",
             "timestamp: " + _stamp(_utc_now()),
             "operation: " + operation]
    for name in sorted(facts):
        lines.append("%s: %s" % (name, facts[name]))
    print("\n".join(lines))
    print(json.dumps(report, sort_keys=True, indent=2, default=list))


def _upload(settings, path, key, timeout_seconds, transport=None):
    return put_object(
        source_path=path, bucket=settings["INVENTORAI_R2_BUCKET"],
        object_key=key, account_id=settings["INVENTORAI_R2_ACCOUNT_ID"],
        access_key_id=settings["INVENTORAI_R2_ACCESS_KEY_ID"],
        secret_access_key=settings["INVENTORAI_R2_SECRET_ACCESS_KEY"],
        timeout_seconds=timeout_seconds, transport=transport)


def _cmd_upload(args, environ=None, transport=None):
    """Upload a named database or backup file - ALWAYS via the backup engine.

    B-3 REPAIR. This command previously validated the given file and uploaded
    THAT FILE AS-IS. Against a live database in WAL mode that is unsafe in a way
    validation cannot catch: the main file alone can pass ``PRAGMA quick_check``
    while the committed rows still live in the ``-wal`` sidecar, so the object
    stored off-provider is an incomplete artifact reported as a successful
    backup. Reproduced in
    `tests/test_infra_offsite_backup_r2.py::test_wal_committed_rows_are_never_
    shipped_as_a_raw_main_file`, where the copied main file validates clean and
    then cannot even see the table.

    There is therefore NO raw-file upload path left in this tool: the input is
    treated as a SOURCE, and the existing service produces a consistent artifact
    from it through the SQLite online-backup API (which reads the WAL). That is
    correct for a live database and harmless for an existing backup file, which
    is itself just a valid SQLite database. No second backup engine is
    introduced, and the source is only ever opened read-only.
    """
    settings = resolve_settings(environ)
    source = os.path.abspath(os.path.expanduser(args.source))
    validate_sqlite_database(source)
    moment = _utc_now()
    filename = args.name or ("inventorai-%s.sqlite" % _stamp(moment))
    workspace = tempfile.mkdtemp(prefix="inventorai-offsite-")
    try:
        staged = os.path.join(workspace, filename)
        backup_report = backup_database(source, staged)
        key = args.key or object_key(settings["INVENTORAI_R2_PREFIX"], filename)
        upload_report = _upload(settings, staged, key, args.timeout, transport)
        _emit("upload", {"backup": backup_report, "upload": upload_report},
              source=source, key=key)
        return 0
    finally:
        shutil.rmtree(workspace, ignore_errors=True)


def _cmd_daily(args, environ=None, transport=None):
    """The schedulable daily job: consistent backup -> validate -> upload ->
    remove the temporary local artifact.

    The live database is only ever read (the service opens the source read-only
    and uses the SQLite online-backup API), so this is safe to run against the
    serving database. The temporary backup is removed in every outcome,
    including failure, so a daily schedule cannot fill the persistent disk.
    """
    settings = resolve_settings(environ)
    source = os.path.abspath(os.path.expanduser(args.database))
    moment = _utc_now()
    filename = "inventorai-%s.sqlite" % _stamp(moment)
    workspace = tempfile.mkdtemp(prefix="inventorai-offsite-")
    try:
        staged = os.path.join(workspace, filename)
        backup_report = backup_database(source, staged)
        key = object_key(settings["INVENTORAI_R2_PREFIX"], filename)
        upload_report = _upload(settings, staged, key, args.timeout, transport)
        _emit("daily", {"backup": backup_report, "upload": upload_report},
              database=source, key=key)
        return 0
    finally:
        shutil.rmtree(workspace, ignore_errors=True)


def build_parser():
    parser = argparse.ArgumentParser(
        prog="inventorai_offsite_backup",
        description=("Off-provider backup to Cloudflare R2, composed from the "
                     "existing backup service and a stdlib HTTPS uploader. "
                     "Credentials come from the environment only."))
    subparsers = parser.add_subparsers(dest="command", required=True)

    daily = subparsers.add_parser(
        "daily",
        help=("consistent backup of the live database, then upload, then "
              "remove the temporary local copy (the schedulable command)"))
    daily.add_argument("database", help="path to the live database (read-only)")
    daily.add_argument("--timeout", type=float, default=120.0,
                       help="bounded upload timeout in seconds")
    daily.set_defaults(func=_cmd_daily)

    upload = subparsers.add_parser(
        "upload",
        help=("upload a named database/backup file, always through the backup "
              "engine first (no raw file is ever uploaded)"))
    upload.add_argument("source", help="path to the database or backup to copy")
    upload.add_argument("--name", default=None,
                        help="artifact filename (default: a UTC-stamped name)")
    upload.add_argument("--key", default=None,
                        help="destination object key (default: prefix + filename)")
    upload.add_argument("--timeout", type=float, default=120.0,
                        help="bounded upload timeout in seconds")
    upload.set_defaults(func=_cmd_upload)

    return parser


def main(argv=None, environ=None, transport=None):
    args = build_parser().parse_args(argv)
    try:
        return args.func(args, environ=environ, transport=transport)
    except BackupError as exc:
        print("BACKUP ERROR: %s" % exc, file=sys.stderr)
        return _EXIT_BACKUP_ERROR
    except R2UploadError as exc:
        print("OFF-PROVIDER UPLOAD ERROR: %s" % exc, file=sys.stderr)
        return _EXIT_UPLOAD_ERROR


if __name__ == "__main__":
    raise SystemExit(main())
