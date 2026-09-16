"""SERIOUS-RELEASE-PRE-RELEASE-TRANCHE-01, Slice E — backup/restore operator CLI.

File path: ``scripts/inventorai_backup.py``
Purpose:   the operator-accessible entry point for the ALREADY EXISTING,
           already governed backup capability in ``engine/backup_service.py``
           (P10-BR1). Before this wrapper the capability was reachable only
           from Python or from the test suite, so a production operator had
           no runnable command; the DR plan's Scenario 7 procedure described
           steps nobody could execute directly.

What this is NOT: a second backup engine. Every operation below delegates to
the existing service functions unchanged — this module contains no SQLite
call, no copy logic, no validation logic and no retention logic of its own.

Input contract:
  * one subcommand plus EXPLICIT paths — nothing is inferred from the
    environment, and the live application database path is never defaulted or
    guessed (mirrors the service's own input contract);
  * ``--overwrite`` is opt-in and defaults to False on both ``backup`` and
    ``restore``.

Output contract:
  * a deterministic evidence header (UTC timestamp, operation, resolved
    absolute paths) followed by the service's own returned report, printed as
    sorted JSON so two runs are comparable;
  * reports carry paths, ``quick_check`` results, table NAMES and row COUNTS
    only — never row contents, emails, hashes or tokens, because that is what
    the underlying service returns and nothing here adds to it.

Exit codes:
  * ``0`` success;
  * ``2`` usage error (argparse);
  * ``3`` ``BackupError`` — every fail-closed condition the service enforces
    (missing or invalid source, same source and destination, missing parent
    directory, existing destination without ``--overwrite``, inventory
    mismatch). The message is printed to stderr; no partial output file is
    left behind, because the service removes it.

Prohibited (binding, inherited from P10-BR1 and this tranche's authorization):
  * NO retention policy, scheduling, rotation or deletion of prior backups;
  * NO cloud/provider API of any kind — this runs the same way on a laptop and
    inside the production container, which is what makes the resulting backup
    PORTABLE and independent of the hosting provider;
  * NO restore onto the live database by default. ``restore`` writes to a
    SEPARATE explicit target; overwriting an existing file at that target
    requires ``--overwrite`` typed by the operator. Repointing
    ``INVENTORAI_DB_PATH`` at a verified restore is a deliberate, separate
    human step (DR plan Scenario 7), never something this CLI performs.
"""
import argparse
import datetime
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.backup_service import (  # noqa: E402  (path set above)
    BackupError,
    backup_database,
    database_parity_report,
    restore_database,
    validate_sqlite_database,
)

_EXIT_BACKUP_ERROR = 3


def _utc_now():
    return datetime.datetime.now(datetime.timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ")


def _header(operation, **paths):
    """Deterministic evidence header, in the style of the existing
    ``scripts/run_dependency_audit.py`` wrapper."""
    lines = ["InventorAI backup operator CLI (P10-BR1 service; no second engine)",
             "timestamp: " + _utc_now(),
             "operation: " + operation]
    for name in sorted(paths):
        lines.append("%s: %s" % (name, paths[name]))
    return "\n".join(lines)


def _emit(operation, report, **paths):
    print(_header(operation, **paths))
    print(json.dumps(report, sort_keys=True, indent=2, default=list))


def _abs(path):
    return os.path.abspath(os.path.expanduser(path))


def _cmd_validate(args):
    path = _abs(args.database)
    _emit("validate", validate_sqlite_database(path), database=path)
    return 0


def _cmd_backup(args):
    source, backup = _abs(args.source), _abs(args.backup)
    report = backup_database(source, backup, overwrite=args.overwrite)
    _emit("backup", report, source=source, backup=backup)
    return 0


def _cmd_restore(args):
    backup, target = _abs(args.backup), _abs(args.target)
    report = restore_database(backup, target, overwrite=args.overwrite)
    _emit("restore", report, backup=backup, target=target)
    return 0


def _cmd_parity(args):
    a, b = _abs(args.first), _abs(args.second)
    _emit("parity", database_parity_report(a, b), first=a, second=b)
    return 0


def build_parser():
    parser = argparse.ArgumentParser(
        prog="inventorai_backup",
        description=("Operator entry point for the existing P10-BR1 backup "
                     "service. Every path is explicit; nothing is inferred "
                     "from the environment."))
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser(
        "validate", help="fail-closed validation of one SQLite database")
    validate.add_argument("database", help="path to the database to validate")
    validate.set_defaults(func=_cmd_validate)

    backup = subparsers.add_parser(
        "backup", help="create a consistent backup of a database")
    backup.add_argument("source", help="path to the live database (read-only)")
    backup.add_argument("backup", help="path to write the backup to")
    backup.add_argument("--overwrite", action="store_true",
                        help="replace an existing backup file (off by default)")
    backup.set_defaults(func=_cmd_backup)

    restore = subparsers.add_parser(
        "restore",
        help=("restore a validated backup to a SEPARATE target path; never "
              "writes onto the live database implicitly"))
    restore.add_argument("backup", help="path to the backup to restore from")
    restore.add_argument("target", help="NEW path to restore into")
    restore.add_argument("--overwrite", action="store_true",
                         help="replace an existing target file (off by default)")
    restore.set_defaults(func=_cmd_restore)

    parity = subparsers.add_parser(
        "parity", help="schema-object and row-count parity between two databases")
    parity.add_argument("first", help="first database")
    parity.add_argument("second", help="second database")
    parity.set_defaults(func=_cmd_parity)

    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except BackupError as exc:
        print("BACKUP ERROR: %s" % exc, file=sys.stderr)
        return _EXIT_BACKUP_ERROR


if __name__ == "__main__":
    raise SystemExit(main())
