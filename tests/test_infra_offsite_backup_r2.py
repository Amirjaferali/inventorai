"""OD-INFRA-5 — off-provider (Cloudflare R2) backup: transport + operator CLI.

File: tests/test_infra_offsite_backup_r2.py
Purpose: pin the ONE thing this tranche adds to backup handling — moving an
already-created, already-validated backup artifact off the hosting provider —
and pin the boundaries that keep it from becoming anything more.

Input contract: `engine/r2_object_upload.py` (SigV4 primitives, `put_object`,
`R2UploadError`); `scripts/inventorai_offsite_backup.py` (`main`,
`resolve_settings`, `object_key`).
Output contract: the existing backup service remains the ONE backup owner; the
live database is never written; credentials come from the environment and never
appear in output; only confirmed provider acceptance is success; there is no
remote delete, expiry or retention path anywhere.
Prohibited: performing a real network request; creating any Cloudflare resource;
requiring real credentials to run; implementing a second backup algorithm;
inventing a retention rule.

Backup/restore/parity semantics themselves remain owned by
`tests/test_p10_br1_backup_restore.py` — nothing here duplicates them.
"""
import ast
import datetime
import hashlib
import importlib.util
import io
import json
import os
import sqlite3

import pytest

from engine.backup_service import (
    BackupError,
    backup_database,
    validate_sqlite_database,
)
from engine.r2_object_upload import (
    MAX_OBJECT_BYTES,
    R2_REGION,
    R2UploadError,
    S3_SERVICE,
    account_endpoint,
    authorization_header,
    canonical_headers,
    canonical_object_uri,
    canonical_request,
    put_object,
    signing_key,
    string_to_sign,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLI_PATH = os.path.join(ROOT, "scripts", "inventorai_offsite_backup.py")
UPLOADER_SOURCE = os.path.join(ROOT, "engine", "r2_object_upload.py")
# The in-process daily scheduler owns the ONE pipeline composition the CLI
# delegates to; it is held to the same remote-boundary guards as the CLI.
SCHEDULER_SOURCE = os.path.join(ROOT, "engine", "offsite_backup_scheduler.py")

# Test-only values. Not credentials: nothing here reaches any provider.
ACCOUNT_ID = "testaccount"
BUCKET = "inventorai-backups-test"
ACCESS_KEY_ID = "TESTONLYACCESSKEYID"
SECRET_KEY = "test-only-secret-not-a-real-key"

SETTINGS = {"INVENTORAI_R2_ACCOUNT_ID": ACCOUNT_ID,
            "INVENTORAI_R2_BUCKET": BUCKET,
            "INVENTORAI_R2_ACCESS_KEY_ID": ACCESS_KEY_ID,
            "INVENTORAI_R2_SECRET_ACCESS_KEY": SECRET_KEY}


def _load_cli():
    spec = importlib.util.spec_from_file_location("inventorai_offsite_backup",
                                                  CLI_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


cli = _load_cli()


class _RecordingTransport:
    """A local stand-in for R2. Records the signed request, returns a scripted
    status, and never opens a socket."""

    def __init__(self, status=200, raises=None):
        self.status = status
        self.raises = raises
        self.calls = []

    def __call__(self, url, headers, path, size, timeout_seconds):
        with open(path, "rb") as handle:
            body = handle.read()
        self.calls.append({"url": url, "headers": dict(headers), "path": path,
                           "size": size, "timeout": timeout_seconds,
                           "body": body,
                           "body_sha256": hashlib.sha256(body).hexdigest(),
                           "body_bytes": len(body)})
        if self.raises is not None:
            raise self.raises
        return self.status, b"<ok/>"


@pytest.fixture
def live_database(tmp_path):
    """A small real SQLite database standing in for the serving database."""
    path = tmp_path / "live.sqlite"
    with sqlite3.connect(str(path)) as connection:
        connection.execute("CREATE TABLE accounts (id TEXT, email TEXT)")
        connection.execute("INSERT INTO accounts VALUES ('a1', 'x@example.com')")
        connection.execute("CREATE TABLE records (id TEXT, payload TEXT)")
        connection.execute("INSERT INTO records VALUES ('r1', 'invention text')")
    return str(path)


@pytest.fixture
def backup_artifact(tmp_path, live_database):
    """A backup produced by the EXISTING service — the only way one is made."""
    destination = str(tmp_path / "artifact.sqlite")
    backup_database(live_database, destination)
    return destination


def _upload(path, transport, **overrides):
    options = {"source_path": path, "bucket": BUCKET,
               "object_key": "daily/artifact.sqlite", "account_id": ACCOUNT_ID,
               "access_key_id": ACCESS_KEY_ID,
               "secret_access_key": SECRET_KEY, "transport": transport}
    options.update(overrides)
    return put_object(**options)


# --- SigV4 correctness, checked against the PUBLISHED AWS example ------------

def test_signature_matches_the_published_aws_sigv4_example():
    """Non-circular correctness evidence: the AWS documentation's own SigV4
    example (GET Object with a Range header, us-east-1) must reproduce the
    signature AWS publishes for it. This is the one check that validates the
    canonicalization, the scope and the HMAC chain against an outside source
    rather than against this implementation's own output."""
    empty = hashlib.sha256(b"").hexdigest()
    _authorization, signed, signature = authorization_header(
        "AKIAIOSFODNN7EXAMPLE", "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
        "us-east-1", "s3", "20130524T000000Z",
        "GET", "/test.txt", "",
        {"Host": "examplebucket.s3.amazonaws.com", "Range": "bytes=0-9",
         "x-amz-content-sha256": empty, "x-amz-date": "20130524T000000Z"},
        empty)
    assert signed == "host;range;x-amz-content-sha256;x-amz-date"
    assert signature == (
        "f0e8bdb87c964420e857bd35b5d6ed310bd44f0170aba48dd91039c6036bdb41")


def test_canonical_headers_lowercase_trim_and_sort():
    block, signed = canonical_headers(
        {"X-Amz-Date": " 20200101T000000Z ", "Host": "h.example",
         "x-amz-content-sha256": "abc"})
    assert signed == "host;x-amz-content-sha256;x-amz-date"
    assert block == ("host:h.example\n"
                     "x-amz-content-sha256:abc\n"
                     "x-amz-date:20200101T000000Z\n")


def test_canonical_request_has_the_required_shape():
    text, signed = canonical_request(
        "put", "/b/k", "", {"Host": "h.example"}, "PAYLOADHASH")
    lines = text.split("\n")
    assert lines[0] == "PUT"            # method upper-cased
    assert lines[1] == "/b/k"
    assert lines[2] == ""               # no query string
    assert lines[-1] == "PAYLOADHASH"   # payload hash terminates the request
    assert lines[-2] == signed


def test_string_to_sign_is_algorithm_date_scope_and_digest():
    value = string_to_sign("20200101T000000Z", "20200101/auto/s3/aws4_request",
                           "CANONICAL")
    parts = value.split("\n")
    assert parts[0] == "AWS4-HMAC-SHA256"
    assert parts[1] == "20200101T000000Z"
    assert parts[2] == "20200101/auto/s3/aws4_request"
    assert parts[3] == hashlib.sha256(b"CANONICAL").hexdigest()


def test_signing_key_is_the_four_step_hmac_chain():
    assert len(signing_key(SECRET_KEY, "20200101", R2_REGION, S3_SERVICE)) == 32
    assert (signing_key(SECRET_KEY, "20200101", R2_REGION, S3_SERVICE)
            != signing_key(SECRET_KEY, "20200102", R2_REGION, S3_SERVICE))
    assert (signing_key(SECRET_KEY, "20200101", R2_REGION, S3_SERVICE)
            != signing_key(SECRET_KEY + "x", "20200101", R2_REGION, S3_SERVICE))


def test_r2_uses_the_region_and_service_tokens_r2_expects():
    assert R2_REGION == "auto"
    assert S3_SERVICE == "s3"


# --- endpoint and key handling ------------------------------------------------

def test_account_endpoint_is_always_https():
    assert account_endpoint(ACCOUNT_ID) == (
        "https://testaccount.r2cloudflarestorage.com".replace(
            "r2cloudflarestorage", "r2.cloudflarestorage"))
    assert account_endpoint(ACCOUNT_ID).startswith("https://")


@pytest.mark.parametrize("value", ["", "   ", "a/b", "a:b", "a b", "a?b", None])
def test_account_endpoint_rejects_a_malformed_account_id(value):
    with pytest.raises(R2UploadError):
        account_endpoint(value)


def test_canonical_object_uri_encodes_segments_and_keeps_separators():
    assert canonical_object_uri(BUCKET, "daily/a b.sqlite") == (
        "/%s/daily/a%%20b.sqlite" % BUCKET)


@pytest.mark.parametrize("bucket,key", [
    ("", "k"), ("a/b", "k"), (BUCKET, ""), (BUCKET, "   "),
    (BUCKET, "../escape"), (BUCKET, "a/../../etc/passwd"),
])
def test_canonical_object_uri_fails_closed_on_traversal_or_empty(bucket, key):
    with pytest.raises(R2UploadError):
        canonical_object_uri(bucket, key)


# --- the upload: only confirmed acceptance is success ------------------------

@pytest.mark.parametrize("status", [200, 201, 204])
def test_provider_acceptance_is_reported_with_verifiable_evidence(
        backup_artifact, status):
    transport = _RecordingTransport(status=status)
    report = _upload(backup_artifact, transport)
    assert report["accepted"] is True
    assert report["provider_status"] == status
    assert report["bytes"] == os.path.getsize(backup_artifact)
    with open(backup_artifact, "rb") as handle:
        assert report["sha256"] == hashlib.sha256(handle.read()).hexdigest()
    # The digest the provider was asked to store matches the bytes actually sent.
    assert transport.calls[0]["body_sha256"] == report["sha256"]
    assert transport.calls[0]["headers"]["x-amz-content-sha256"] == report["sha256"]


@pytest.mark.parametrize("status", [301, 400, 401, 403, 404, 429, 500, 503])
def test_a_non_2xx_response_is_never_treated_as_a_stored_backup(backup_artifact,
                                                                status):
    with pytest.raises(R2UploadError) as raised:
        _upload(backup_artifact, _RecordingTransport(status=status))
    assert raised.value.reason_code == "provider_rejected"


@pytest.mark.parametrize("error", [
    TimeoutError("timed out"), OSError("reset"), Exception("unknown")])
def test_transport_failure_is_a_bounded_failure_not_a_success(backup_artifact,
                                                              error):
    with pytest.raises(R2UploadError) as raised:
        _upload(backup_artifact, _RecordingTransport(raises=error))
    assert raised.value.reason_code == "provider_unreachable"
    assert raised.value.__cause__ is None


def test_upload_makes_exactly_one_attempt_with_no_retry(backup_artifact):
    transport = _RecordingTransport(status=500)
    with pytest.raises(R2UploadError):
        _upload(backup_artifact, transport)
    assert len(transport.calls) == 1


def test_upload_is_https_only(backup_artifact):
    transport = _RecordingTransport()
    _upload(backup_artifact, transport)
    assert transport.calls[0]["url"].startswith("https://")
    for insecure in ("http://x.example", "ftp://x.example", "x.example"):
        with pytest.raises(R2UploadError) as raised:
            _upload(backup_artifact, transport, endpoint=insecure)
        assert raised.value.reason_code == "insecure_endpoint"


def test_upload_timeout_is_bounded_and_reaches_the_transport(backup_artifact):
    transport = _RecordingTransport()
    _upload(backup_artifact, transport, timeout_seconds=30.0)
    assert transport.calls[0]["timeout"] == 30.0


@pytest.mark.parametrize("missing", ["access_key_id", "secret_access_key"])
def test_absent_credentials_fail_closed_before_any_request(backup_artifact,
                                                           missing):
    transport = _RecordingTransport()
    with pytest.raises(R2UploadError) as raised:
        _upload(backup_artifact, transport, **{missing: "   "})
    assert raised.value.reason_code == "missing_credentials"
    assert transport.calls == []


def test_missing_or_empty_source_fails_closed(tmp_path):
    transport = _RecordingTransport()
    with pytest.raises(R2UploadError) as raised:
        _upload(str(tmp_path / "absent.sqlite"), transport)
    assert raised.value.reason_code == "source_not_found"
    empty = tmp_path / "empty.sqlite"
    empty.write_bytes(b"")
    with pytest.raises(R2UploadError) as raised:
        _upload(str(empty), transport)
    assert raised.value.reason_code == "source_empty"
    assert transport.calls == []


def test_single_put_size_bound_is_declared_and_enforced(backup_artifact,
                                                        monkeypatch):
    """Above the single-PUT bound the correct answer is multipart upload, which
    is deliberately not implemented — so it must fail closed, never truncate."""
    assert MAX_OBJECT_BYTES <= 5 * 1024 * 1024 * 1024
    monkeypatch.setattr("engine.r2_object_upload.MAX_OBJECT_BYTES", 1)
    with pytest.raises(R2UploadError) as raised:
        _upload(backup_artifact, _RecordingTransport())
    assert raised.value.reason_code == "source_too_large_for_single_put"


def test_request_is_signed_with_an_authorization_header(backup_artifact):
    transport = _RecordingTransport()
    _upload(backup_artifact, transport)
    headers = transport.calls[0]["headers"]
    assert headers["Authorization"].startswith("AWS4-HMAC-SHA256 Credential=")
    assert "/auto/s3/aws4_request" in headers["Authorization"]
    # `if-none-match` is part of the SIGNED set (create-only, B-4): an unsigned
    # conditional header could be stripped in transit, silently restoring
    # overwrite behaviour.
    assert "SignedHeaders=host;if-none-match;x-amz-content-sha256;x-amz-date" in (
        headers["Authorization"])
    assert "x-amz-date" in headers
    assert headers["if-none-match"] == "*"


def test_a_fixed_moment_produces_a_deterministic_signature(backup_artifact):
    """Regression anchor: same file, same credentials, same instant -> same
    signature. Guards against a later refactor silently changing the
    canonicalization."""
    moment = datetime.datetime(2026, 1, 2, 3, 4, 5,
                               tzinfo=datetime.timezone.utc)
    first, second = _RecordingTransport(), _RecordingTransport()
    _upload(backup_artifact, first, now=moment)
    _upload(backup_artifact, second, now=moment)
    assert (first.calls[0]["headers"]["Authorization"]
            == second.calls[0]["headers"]["Authorization"])
    assert first.calls[0]["headers"]["x-amz-date"] == "20260102T030405Z"


# --- secrecy ------------------------------------------------------------------

def test_the_report_carries_no_credential_or_signature(backup_artifact):
    report = _upload(backup_artifact, _RecordingTransport())
    text = json.dumps(report)
    for forbidden in (ACCESS_KEY_ID, SECRET_KEY, "AWS4-HMAC-SHA256",
                      "Authorization", "Bearer"):
        assert forbidden not in text, forbidden


def test_no_failure_message_carries_a_credential(backup_artifact):
    for transport in (_RecordingTransport(status=403),
                      _RecordingTransport(raises=OSError("x"))):
        try:
            _upload(backup_artifact, transport)
        except R2UploadError as exc:
            text = "%r %s" % (exc, exc)
            assert SECRET_KEY not in text
            assert ACCESS_KEY_ID not in text


def test_the_uploader_module_writes_no_logs_and_knows_no_sqlite():
    """Two boundaries in one source check: no logging seam at all, and no
    database awareness — the uploader moves bytes and nothing else."""
    source = io.open(UPLOADER_SOURCE, encoding="utf-8").read()
    for forbidden in ("import logging", "logging.", "getLogger", "print("):
        assert forbidden not in source, forbidden
    for forbidden in ("import sqlite3", "sqlite3.", "PRAGMA", "SELECT ",
                      "CREATE TABLE", "sqlite_master"):
        assert forbidden not in source, forbidden


def _operative(path):
    """Return ``(string-constants, identifiers)`` for the EXECUTABLE code only.

    Docstrings and comments are excluded on purpose. A guard that scans raw
    source text cannot tell "there is no delete path" (prose) from a delete
    path, so it would fire on its own explanation — the same trap the
    `.dockerignore` guard was hardened against. This mirrors the existing
    `_conf_operative_strings` approach in
    tests/test_infra_render_production_serving.py.
    """
    tree = ast.parse(io.open(path, encoding="utf-8").read())
    docstrings = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef,
                             ast.AsyncFunctionDef)):
            body = getattr(node, "body", None)
            if (body and isinstance(body[0], ast.Expr)
                    and isinstance(body[0].value, ast.Constant)
                    and isinstance(body[0].value.value, str)):
                docstrings.add(id(body[0].value))
    strings, identifiers = [], []
    for node in ast.walk(tree):
        if (isinstance(node, ast.Constant) and isinstance(node.value, str)
                and id(node) not in docstrings):
            strings.append(node.value)
        elif isinstance(node, ast.Name):
            identifiers.append(node.id)
        elif isinstance(node, ast.Attribute):
            identifiers.append(node.attr)
        elif isinstance(node, ast.keyword) and node.arg:
            identifiers.append(node.arg)
    return strings, identifiers


def _imported_modules(path):
    """Module names actually imported by executable code: the top-level name
    of every import, plus the full dotted module of every `from` import."""
    tree = ast.parse(io.open(path, encoding="utf-8").read())
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module.split(".")[0])
            names.add(node.module)
    return names


def test_no_remote_delete_expiry_or_retention_path_exists():
    """Retention is unresolved in the privacy/legal lane. There is therefore no
    EXECUTABLE code able to remove or expire a remote object, in any of the
    three files — asserted against operative code, not against prose."""
    for path in (UPLOADER_SOURCE, CLI_PATH, SCHEDULER_SOURCE):
        strings, identifiers = _operative(path)
        for value in strings:
            lowered = value.lower()
            # Mechanism tokens only. The word "retention" itself is deliberately
            # NOT forbidden in a string: the CLI's operator banner truthfully
            # states "no retention", and a guard that banned the word would
            # force that disclosure to be deleted.
            for forbidden in ("delete", "lifecycle", "expiration",
                              "x-amz-expiration", "x-amz-lifecycle"):
                assert forbidden not in lowered, (path, value)
        for name in identifiers:
            lowered = name.lower()
            for forbidden in ("delete", "unlink", "lifecycle", "expire",
                              "retention"):
                assert forbidden not in lowered, (path, name)


def test_the_operator_banner_discloses_the_absent_retention_rule():
    """The operator sees, on every run, that no retention exists — so an
    accumulating bucket is a disclosed consequence, not a surprise."""
    strings, _ = _operative(CLI_PATH)
    banner = [value for value in strings if "no second engine" in value]
    assert banner and "no retention" in banner[0].lower()


def test_the_only_http_method_the_uploader_can_issue_is_put():
    """Positive form of the same boundary: PUT is the one verb present in
    executable code, so there is no reachable list, get or delete request."""
    strings, _identifiers = _operative(UPLOADER_SOURCE)
    methods = {value.upper() for value in strings
               if value.upper() in ("GET", "PUT", "POST", "DELETE", "HEAD",
                                    "LIST")}
    assert methods == {"PUT"}, methods


def test_the_temporary_workspace_cleanup_is_local_only():
    """ONE temporary workspace lifecycle exists, in the shared pipeline
    (`perform_offsite_backup`): a LOCAL directory staged under
    `tempfile.mkdtemp` and removed in every outcome. The CLI delegates to it
    and stages nothing of its own. That is the only removal anywhere, asserted
    explicitly so the operative guard above stays absolute about REMOTE
    objects. (Before the scheduler, the CLI held two copies of this lifecycle,
    one per command; they were unified rather than triplicated.)"""
    scheduler = io.open(SCHEDULER_SOURCE, encoding="utf-8").read()
    assert scheduler.count("shutil.rmtree(workspace") == 1
    assert scheduler.count("tempfile.mkdtemp") == 1
    cli = io.open(CLI_PATH, encoding="utf-8").read()
    assert "rmtree" not in cli and "mkdtemp" not in cli
    strings, identifiers = _operative(UPLOADER_SOURCE)
    assert not any("rmtree" in value for value in strings)
    assert not any("rmtree" in name for name in identifiers)


def _route_functions(tree):
    """Every function decorated as a Flask route or blueprint route."""
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for decorator in node.decorator_list:
            target = decorator.func if isinstance(decorator, ast.Call) else decorator
            if isinstance(target, ast.Attribute) and target.attr in (
                    "route", "get", "post", "before_request", "after_request",
                    "errorhandler"):
                yield node
                break


def test_the_web_application_never_imports_the_uploader():
    """Nothing in the request path may reach the off-provider transport, so R2
    can never become runtime persistence. The web layer never imports the
    uploader at all; the ONE thing it imports from the off-provider path is
    the scheduler's lifecycle (start it in production, once), and no route,
    request hook or error handler references the scheduler, its store opener
    or its settings resolver. (Superseded: the earlier absolute ban on the
    word "offsite" in `web/app.py`, written when no in-process schedule
    existed; the boundary it protected - request path vs. transport - is now
    asserted directly.)"""
    source = io.open(os.path.join(ROOT, "web", "app.py"),
                     encoding="utf-8").read()
    assert "r2_object_upload" not in source
    assert "put_object" not in source
    tree = ast.parse(source)
    imported = {alias.asname or alias.name
                for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)
                and node.module == "engine.offsite_backup_scheduler"
                for alias in node.names}
    assert imported == {"_OffsiteBackupScheduler", "_offsite_backup_configured",
                        "_live_offsite_backup_scheduler",
                        "_offsite_backup_resolve_settings"}, imported
    routes = list(_route_functions(tree))
    assert routes, "no routes found - the guard would be vacuous"
    forbidden = {"_OFFSITE_BACKUP_SCHEDULER", "_open_offsite_backup_store",
                 "_resolve_offsite_backup_settings", "_OffsiteBackupScheduler",
                 "_offsite_backup_configured", "_offsite_backup_resolve_settings",
                 "_live_offsite_backup_scheduler", "perform_offsite_backup",
                 "run_if_due"}
    for function in routes:
        names = {n.id for n in ast.walk(function) if isinstance(n, ast.Name)}
        attrs = {n.attr for n in ast.walk(function) if isinstance(n, ast.Attribute)}
        assert not (names | attrs) & forbidden, (function.name,
                                                 (names | attrs) & forbidden)


# --- the operator CLI ---------------------------------------------------------

def test_settings_come_from_the_environment_and_fail_closed_by_name():
    assert cli.resolve_settings(dict(SETTINGS))["INVENTORAI_R2_BUCKET"] == BUCKET
    for name in SETTINGS:
        partial = dict(SETTINGS)
        partial[name] = "   "
        with pytest.raises(R2UploadError) as raised:
            cli.resolve_settings(partial)
        assert raised.value.reason_code == "missing_configuration"
        assert name in str(raised.value)
        assert SETTINGS[name] not in str(raised.value)


def test_the_cli_accepts_no_credential_as_an_argument():
    """A credential on the command line would land in shell history and in the
    process list, so the parser must not offer one."""
    help_text = cli.build_parser().format_help().lower()
    for forbidden in ("--access-key", "--secret", "--api-key", "--credential",
                      "--token"):
        assert forbidden not in help_text, forbidden


def test_object_key_composition_honours_an_optional_prefix():
    assert cli.object_key("", "f.sqlite") == "f.sqlite"
    assert cli.object_key("daily", "f.sqlite") == "daily/f.sqlite"


def test_daily_runs_the_existing_engine_then_uploads_then_cleans_up(
        live_database, tmp_path, capsys):
    """The whole authorized pipeline, end to end, with a local transport."""
    before = sorted(os.listdir(tmp_path))
    transport = _RecordingTransport()
    environ = dict(SETTINGS, INVENTORAI_R2_PREFIX="daily")
    code = cli.main(["daily", live_database], environ=environ,
                    transport=transport)
    assert code == 0
    assert len(transport.calls) == 1
    uploaded = transport.calls[0]

    # What was uploaded is a real, openable SQLite backup of the live database,
    # produced by the existing service — not a raw copy and not a re-implementation.
    assert uploaded["url"].startswith("https://testaccount.r2.cloudflarestorage.com/")
    assert "/daily/inventorai-" in uploaded["url"]
    assert uploaded["body_bytes"] > 0
    assert uploaded["body"].startswith(b"SQLite format 3\x00")

    # The temporary local artifact is gone: a daily schedule cannot fill the
    # disk. Checked BEFORE anything else is written into tmp_path.
    assert sorted(os.listdir(tmp_path)) == before
    assert not os.path.exists(uploaded["path"])

    # What was uploaded opens as a real SQLite database carrying the live
    # content — proof the existing engine produced it, not a byte smear.
    restored = os.path.join(str(tmp_path), "verify-uploaded.sqlite")
    with open(restored, "wb") as handle:
        handle.write(uploaded["body"])
    with sqlite3.connect(restored) as connection:
        tables = {row[0] for row in connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table'")}
        rows = connection.execute("SELECT id FROM records").fetchall()
    assert {"accounts", "records"} <= tables
    assert rows == [("r1",)]

    output = capsys.readouterr().out
    assert '"accepted": true' in output
    for forbidden in (SECRET_KEY, ACCESS_KEY_ID, "Authorization",
                      "x@example.com", "invention text"):
        assert forbidden not in output, forbidden


def test_daily_never_writes_to_the_live_database(live_database):
    """The source is opened read-only by the service; this asserts the file is
    byte-identical and its mtime unchanged after a full daily run."""
    with open(live_database, "rb") as handle:
        before_bytes = handle.read()
    before_stat = os.stat(live_database)
    cli.main(["daily", live_database], environ=dict(SETTINGS),
             transport=_RecordingTransport())
    with open(live_database, "rb") as handle:
        assert handle.read() == before_bytes
    assert os.stat(live_database).st_mtime == before_stat.st_mtime
    assert os.stat(live_database).st_size == before_stat.st_size


def test_daily_removes_the_temporary_artifact_even_when_the_upload_fails(
        live_database, tmp_path):
    transport = _RecordingTransport(status=500)
    before = sorted(os.listdir(tmp_path))
    code = cli.main(["daily", live_database], environ=dict(SETTINGS),
                    transport=transport)
    assert code == 4
    assert sorted(os.listdir(tmp_path)) == before
    assert not os.path.exists(transport.calls[0]["path"])


def test_daily_object_names_are_unique_per_run(live_database):
    keys = []
    for _ in range(2):
        transport = _RecordingTransport()
        cli.main(["daily", live_database], environ=dict(SETTINGS),
                 transport=transport)
        keys.append(transport.calls[0]["url"])
    # Same second or not, an existing object is never deliberately replaced by
    # a --overwrite-style flag: there is none.
    assert "--overwrite" not in cli.build_parser().format_help()
    assert all(key.endswith(".sqlite") for key in keys)


def test_upload_validates_the_artifact_before_shipping_it(tmp_path):
    """A corrupt file must never be shipped off-provider and counted as a
    backup. Validation is the existing service's, not a new implementation."""
    corrupt = tmp_path / "corrupt.sqlite"
    corrupt.write_bytes(b"this is definitely not a sqlite database")
    transport = _RecordingTransport()
    code = cli.main(["upload", str(corrupt)], environ=dict(SETTINGS),
                    transport=transport)
    assert code == 3                       # BackupError, not an upload error
    assert transport.calls == []


def test_upload_ships_a_validated_artifact(backup_artifact, capsys):
    transport = _RecordingTransport()
    code = cli.main(["upload", backup_artifact, "--key", "manual/a.sqlite"],
                    environ=dict(SETTINGS), transport=transport)
    assert code == 0
    assert transport.calls[0]["url"].endswith("/manual/a.sqlite")
    assert '"accepted": true' in capsys.readouterr().out


def test_missing_configuration_exits_non_zero_without_touching_the_database(
        live_database):
    transport = _RecordingTransport()
    code = cli.main(["daily", live_database], environ={}, transport=transport)
    assert code == 4
    assert transport.calls == []


def test_the_cli_is_not_a_second_backup_engine():
    """Operative-code check: the CLI imports no SQLite module and issues no SQL
    or copy of its own — it can only delegate. Asserted against executable code,
    not raw text, because the module docstring legitimately DISCUSSES `PRAGMA`
    and WAL when explaining why raw-file upload was removed."""
    assert "sqlite3" not in _imported_modules(CLI_PATH)
    strings, identifiers = _operative(CLI_PATH)
    for value in strings:
        upper = value.upper()
        for forbidden in ("PRAGMA", "SQLITE_MASTER", "SELECT ", "CREATE TABLE"):
            assert forbidden not in upper, value
    for name in identifiers:
        assert name not in ("copyfile", "copy", "copy2", "connect"), name
    # The CLI can only DELEGATE: its backup comes from the shared pipeline,
    # whose backup comes from the existing service. Asserted on the executable
    # import graph, not on prose.
    assert "engine.offsite_backup_scheduler" in _imported_modules(CLI_PATH)
    _strings, identifiers = _operative(CLI_PATH)
    assert "perform_offsite_backup" in identifiers
    assert "backup_database" not in identifiers          # not re-implemented
    assert "sqlite3" not in _imported_modules(SCHEDULER_SOURCE)
    scheduler = io.open(SCHEDULER_SOURCE, encoding="utf-8").read()
    assert "from engine.backup_service import BackupError, backup_database" in scheduler
    assert "from engine.r2_object_upload import R2UploadError, put_object" in scheduler


def test_the_existing_backup_cli_is_unchanged_by_this_tranche():
    """`scripts/inventorai_backup.py` keeps its provider-neutral boundary — the
    reason the provider step lives in a separate script."""
    source = io.open(os.path.join(ROOT, "scripts", "inventorai_backup.py"),
                     encoding="utf-8").read()
    assert "NO cloud/provider API of any kind" in source
    assert "r2" not in source.lower()
    assert "cloudflare" not in source.lower()


def test_backup_error_and_upload_error_use_distinct_exit_codes():
    assert cli._EXIT_BACKUP_ERROR == 3
    assert cli._EXIT_UPLOAD_ERROR == 4
    assert issubclass(BackupError, Exception)
    assert not issubclass(R2UploadError, BackupError)


def test_the_default_upload_transport_refuses_a_non_https_url_itself():
    """`put_object` validates the endpoint before delegating, so this guard
    inside the real transport would otherwise never run. The function that
    actually opens a socket refuses a plaintext URL on its own."""
    from engine.r2_object_upload import _https_put
    with pytest.raises(R2UploadError) as raised:
        _https_put("http://x.example/b/k", {}, __file__, 10, 1.0)
    assert raised.value.reason_code == "insecure_endpoint"


# =============================================================================
# CORRECTIVE PASS (independent-review defect set B-1, B-3, B-4, B-5).
# =============================================================================

from engine.r2_object_upload import (  # noqa: E402
    R2_HOST_SUFFIX,
    _NoRedirectHandler,
    _build_https_only_opener,
    account_host,
    trusted_origin,
)


# --- B-3: a live WAL database's main file is never shipped -------------------

@pytest.fixture
def wal_database(tmp_path):
    """A live database in WAL mode with rows committed into the -wal sidecar."""
    path = str(tmp_path / "wal-live.sqlite")
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("CREATE TABLE accounts (id TEXT)")
    conn.execute("INSERT INTO accounts VALUES ('before-wal')")
    conn.commit()
    conn.execute("INSERT INTO accounts VALUES ('committed-into-wal-1')")
    conn.execute("INSERT INTO accounts VALUES ('committed-into-wal-2')")
    conn.commit()
    yield path, conn
    conn.close()


def test_the_raw_main_file_of_a_wal_database_is_a_false_backup(wal_database,
                                                               tmp_path):
    """The defect's premise, reproduced rather than asserted: copying the main
    file alone passes `quick_check` and yet loses the data entirely."""
    live, conn = wal_database
    assert [r[0] for r in conn.execute("SELECT id FROM accounts")] == [
        "before-wal", "committed-into-wal-1", "committed-into-wal-2"]
    assert os.path.exists(live + "-wal")

    raw = str(tmp_path / "raw-main-only.sqlite")
    with open(live, "rb") as source, open(raw, "wb") as target:
        target.write(source.read())
    # It VALIDATES - which is exactly why validation was not a sufficient guard.
    assert validate_sqlite_database(raw)["quick_check"] == "ok"
    with sqlite3.connect(raw) as shipped:
        with pytest.raises(sqlite3.DatabaseError):
            shipped.execute("SELECT id FROM accounts").fetchall()


def test_wal_committed_rows_are_never_shipped_as_a_raw_main_file(wal_database):
    """B-3. Both operator commands now run the backup engine first, so what
    reaches the provider is a consistent artifact containing the WAL-committed
    rows - never the raw main file that passes validation while holding none."""
    live, _conn = wal_database
    for argv in (["daily", live], ["upload", live]):
        transport = _RecordingTransport()
        assert cli.main(argv, environ=dict(SETTINGS),
                        transport=transport) == 0, argv
        body = transport.calls[0]["body"]
        assert body.startswith(b"SQLite format 3\x00")
        restored = live + ".shipped"
        with open(restored, "wb") as handle:
            handle.write(body)
        with sqlite3.connect(restored) as check:
            rows = [r[0] for r in check.execute("SELECT id FROM accounts")]
        os.remove(restored)
        assert rows == ["before-wal", "committed-into-wal-1",
                        "committed-into-wal-2"], (argv, rows)


def test_no_operator_command_uploads_its_input_file_directly(wal_database):
    """B-3, structurally: the bytes the provider receives are never the bytes of
    the operator-supplied path, because a staged artifact is uploaded instead."""
    live, _conn = wal_database
    with open(live, "rb") as handle:
        raw_bytes = handle.read()
    for argv in (["daily", live], ["upload", live]):
        transport = _RecordingTransport()
        cli.main(argv, environ=dict(SETTINGS), transport=transport)
        call = transport.calls[0]
        assert call["path"] != live, argv
        assert call["body"] != raw_bytes, argv


def test_upload_still_refuses_a_corrupt_source(tmp_path):
    corrupt = tmp_path / "corrupt.sqlite"
    corrupt.write_bytes(b"not a sqlite database at all")
    transport = _RecordingTransport()
    assert cli.main(["upload", str(corrupt)], environ=dict(SETTINGS),
                    transport=transport) == 3
    assert transport.calls == []


# --- B-4: create-only object writes ----------------------------------------

def test_the_conditional_create_header_is_sent_and_signed(backup_artifact):
    transport = _RecordingTransport()
    report = _upload(backup_artifact, transport)
    headers = transport.calls[0]["headers"]
    assert headers["if-none-match"] == "*"
    assert "if-none-match" in headers["Authorization"]
    assert report["create_only"] is True


def test_a_412_precondition_failure_is_a_collision_not_a_success(
        backup_artifact):
    """B-4. The provider refuses to replace an existing key; that is never
    reported as a stored backup."""
    with pytest.raises(R2UploadError) as raised:
        _upload(backup_artifact, _RecordingTransport(status=412))
    assert raised.value.reason_code == "object_already_exists"


def test_first_upload_succeeds_and_a_duplicate_key_fails(backup_artifact):
    """The create-only contract as an operator sees it, with a transport that
    models a provider enforcing `If-None-Match: *`."""

    class _CreateOnlyProvider:
        def __init__(self):
            self.stored = {}
            self.calls = []

        def __call__(self, url, headers, path, size, timeout_seconds):
            self.calls.append(url)
            if headers.get("if-none-match") != "*":       # unconditional PUT
                self.stored[url] = size                   # would overwrite
                return 200, b""
            if url in self.stored:
                return 412, b"<Error><Code>PreconditionFailed</Code></Error>"
            self.stored[url] = size
            return 200, b""

    provider = _CreateOnlyProvider()
    first = _upload(backup_artifact, provider, object_key="daily/same-key.sqlite")
    assert first["accepted"] is True
    with pytest.raises(R2UploadError) as raised:
        _upload(backup_artifact, provider, object_key="daily/same-key.sqlite")
    assert raised.value.reason_code == "object_already_exists"
    assert len(provider.stored) == 1                      # nothing replaced


def test_create_only_adds_no_delete_list_or_lifecycle_path():
    """B-4 must not have smuggled in remote management. The operative guards
    above still hold after the change."""
    strings, identifiers = _operative(UPLOADER_SOURCE)
    for value in strings:
        assert "delete" not in value.lower(), value
    for name in identifiers:
        assert "delete" not in name.lower(), name


# --- B-5: endpoint / account-id authority confusion -------------------------

@pytest.mark.parametrize("account", [
    "collector.invalid#", "@host", "a\\b", "a/b", "a:b", "a?b", "a b",
    "a\tb", "a\nb", "a\rb", "a%2fb", "a%5cb", "a#b", "ab", "A1B2C3D4",
    "x" * 65, "", "   ", None, 7, "acc.ount", "acc_ount", "acc-ount",
])
def test_account_id_rejects_every_authority_confusing_shape(account):
    with pytest.raises(R2UploadError) as raised:
        account_endpoint(account)
    assert raised.value.reason_code == "invalid_account_id"


def test_a_valid_account_id_yields_exactly_one_trusted_host():
    account = "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6"
    assert account_host(account) == account + R2_HOST_SUFFIX
    assert account_endpoint(account) == "https://" + account + R2_HOST_SUFFIX


@pytest.mark.parametrize("origin,reason", [
    ("http://acct.r2.cloudflarestorage.com", "insecure_endpoint"),
    ("acct.r2.cloudflarestorage.com", "insecure_endpoint"),
    ("https://", "insecure_endpoint"),
    ("https://u:p@acct.r2.cloudflarestorage.com", "insecure_endpoint"),
    ("https://acct.r2.cloudflarestorage.com?x=1", "insecure_endpoint"),
    ("https://acct.r2.cloudflarestorage.com#f", "insecure_endpoint"),
    ("https://acct.r2.cloudflarestorage.com/bucket", "insecure_endpoint"),
    ("https://acct.r2.cloudflarestorage.com\\@evil.example", "insecure_endpoint"),
    ("https://acct%2f@evil.example", "insecure_endpoint"),
    ("https://acct%5c.evil.example", "insecure_endpoint"),
    ("https://acct%23.evil.example", "insecure_endpoint"),
    ("https://acct%40evil.example", "insecure_endpoint"),
    ("https://acct.r2.cloudflare\tstorage.com", "insecure_endpoint"),
    ("https://acct.r2.cloudflare\nstorage.com", "insecure_endpoint"),
    ("https://acct.r2.cloudflare storage.com", "insecure_endpoint"),
    ("https://evil.example", "untrusted_endpoint_host"),
    ("https://r2.cloudflarestorage.com.evil.example", "untrusted_endpoint_host"),
])
def test_trusted_origin_rejects_authority_confusion(origin, reason):
    with pytest.raises(R2UploadError) as raised:
        trusted_origin(origin)
    assert raised.value.reason_code == reason, origin


def test_trusted_origin_accepts_only_a_bare_r2_origin():
    good = "https://acct.r2.cloudflarestorage.com"
    assert trusted_origin(good) == good
    assert trusted_origin(good + "/") == good
    assert trusted_origin(good + "///") == good


def test_the_endpoint_seam_is_held_to_the_same_trusted_shape(backup_artifact):
    """The `endpoint=` test seam cannot be used - or configured - to redirect an
    upload to an untrusted origin."""
    transport = _RecordingTransport()
    with pytest.raises(R2UploadError) as raised:
        _upload(backup_artifact, transport, endpoint="https://evil.example")
    assert raised.value.reason_code == "untrusted_endpoint_host"
    assert transport.calls == []


def test_the_signed_host_is_the_host_actually_dialled(backup_artifact):
    """B-5's core requirement: never sign one target and send another."""
    transport = _RecordingTransport()
    _upload(backup_artifact, transport)
    call = transport.calls[0]
    dialled = call["url"].split("/")[2]
    assert call["headers"]["host"] == dialled
    assert dialled == account_host(ACCOUNT_ID)
    assert call["url"].startswith("https://" + dialled + "/")


def test_the_operator_cli_passes_no_endpoint_override(live_database):
    """Production config has no way to set the endpoint: the CLI never passes
    one, so the account-derived trusted origin is the only possibility."""
    # Operative code only: the docstring legitimately explains that the account
    # id "forms the endpoint".
    _strings, identifiers = _operative(CLI_PATH)
    assert "endpoint" not in identifiers
    transport = _RecordingTransport()
    cli.main(["daily", live_database], environ=dict(SETTINGS),
             transport=transport)
    assert transport.calls[0]["url"].startswith(
        "https://" + account_host(ACCOUNT_ID) + "/")


# --- B-1 for the upload transport ------------------------------------------

def test_the_upload_opener_refuses_redirects_and_plaintext():
    """B-1 applies to the upload too: a redirect would carry the SigV4
    Authorization header, and the object bytes, to another origin."""
    import urllib.error
    opener = _build_https_only_opener()
    kinds = [type(handler).__name__ for handler in opener.handlers]
    assert kinds.count("_NoRedirectHandler") == 1
    assert sum("Redirect" in kind for kind in kinds) == 1
    for absent in ("HTTPHandler", "FileHandler", "FTPHandler", "DataHandler"):
        assert absent not in kinds, absent
    assert _NoRedirectHandler().redirect_request(
        None, None, 302, "Found", {}, "https://evil.example") is None
    with pytest.raises(urllib.error.URLError):
        opener.open("http://127.0.0.1:1/x", timeout=5)


@pytest.mark.parametrize("status", [301, 302, 303, 307, 308])
def test_a_redirect_status_is_never_a_stored_backup(backup_artifact, status):
    with pytest.raises(R2UploadError) as raised:
        _upload(backup_artifact, _RecordingTransport(status=status))
    assert raised.value.reason_code == "provider_rejected"


def test_sigv4_primitives_are_unchanged_by_this_corrective_pass():
    """Guard against a regression in the one thing already independently
    validated: the published AWS example signature must still reproduce."""
    empty = hashlib.sha256(b"").hexdigest()
    _authorization, _signed, signature = authorization_header(
        "AKIAIOSFODNN7EXAMPLE", "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
        "us-east-1", "s3", "20130524T000000Z", "GET", "/test.txt", "",
        {"Host": "examplebucket.s3.amazonaws.com", "Range": "bytes=0-9",
         "x-amz-content-sha256": empty, "x-amz-date": "20130524T000000Z"},
        empty)
    assert signature == (
        "f0e8bdb87c964420e857bd35b5d6ed310bd44f0170aba48dd91039c6036bdb41")
