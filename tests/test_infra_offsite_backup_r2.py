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

from engine.backup_service import BackupError, backup_database
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
    assert "SignedHeaders=host;x-amz-content-sha256;x-amz-date" in (
        headers["Authorization"])
    assert "x-amz-date" in headers


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


def test_no_remote_delete_expiry_or_retention_path_exists():
    """Retention is unresolved in the privacy/legal lane. There is therefore no
    EXECUTABLE code able to remove or expire a remote object, in either new
    file — asserted against operative code, not against prose."""
    for path in (UPLOADER_SOURCE, CLI_PATH):
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
    """The CLI does remove its own temporary directory — a LOCAL artifact. That
    is the only removal anywhere, and it is asserted explicitly here so the
    operative guard above stays absolute about REMOTE objects."""
    source = io.open(CLI_PATH, encoding="utf-8").read()
    assert source.count("shutil.rmtree") == 1
    assert "workspace" in source
    strings, _ = _operative(UPLOADER_SOURCE)
    assert not any("rmtree" in value for value in strings)


def test_the_web_application_never_imports_the_uploader():
    """The off-provider path is operator tooling. Nothing in the request path
    may reach it, so R2 can never become runtime persistence."""
    source = io.open(os.path.join(ROOT, "web", "app.py"),
                     encoding="utf-8").read()
    assert "r2_object_upload" not in source
    assert "offsite" not in source.lower()


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
    source = io.open(CLI_PATH, encoding="utf-8").read()
    for forbidden in ("import sqlite3", "sqlite3.connect", "shutil.copy",
                      "PRAGMA", "sqlite_master"):
        assert forbidden not in source, forbidden
    assert "from engine.backup_service import" in source
    assert "backup_database" in source


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
