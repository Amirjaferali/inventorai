"""OD-INFRA-5 — off-provider object upload (Cloudflare R2, S3-compatible HTTPS).

File path: ``engine/r2_object_upload.py``
Purpose:   put ONE already-created local file into ONE off-provider object
           store over HTTPS, and report whether the provider accepted it.

WHAT THIS IS NOT — the boundary that makes the architecture safe:
  * NOT a backup engine. It has no SQLite call, no `sqlite3` import, no schema
    or table awareness, no consistency logic and no validation logic. The ONE
    backup owner remains ``engine/backup_service.py``; this module receives a
    file that service already produced and validated, and moves bytes.
  * NOT a datastore, cache or runtime persistence layer. Nothing in `web/` or
    the request path imports it. The canonical database remains the single
    SQLite file at ``INVENTORAI_DB_PATH``.
  * NOT a retention or lifecycle manager. It can PUT. It cannot list, overwrite
    deliberately, expire or DELETE — there is no delete code path in this file,
    because retention policy is unresolved in the privacy/legal lane and an
    invented expiry would be a policy decision this module has no right to make.
  * NOT a general S3 client. One operation (single-shot PUT), one signature
    shape, no multipart, no presigning, no bucket administration.

Dependency posture: the standard library only — ``hashlib``, ``hmac``,
``urllib.request``. ``requirements.txt`` is unchanged, so the existing
dependency-family guard (which forbids `boto3`) keeps holding. That guard is
also WHY this is stdlib: an SDK would have to be a *runtime* dependency to be
present in the production image, because the upload must run inside the
container where the persistent disk is actually mounted — an operator-only SDK
installed outside the image could never reach ``/var/data``.

Signing: AWS Signature Version 4, service ``s3``, region ``auto`` (what R2
expects). The signing primitives are exposed as separate pure functions so they
can be exercised against the published AWS SigV4 example vector rather than only
against themselves.

Secrecy: no logging of any kind happens in this module. No access key, secret
key, signature, authorization header, signing key or object content is returned,
stored on an exception, or placed in a message. ``R2UploadError`` carries a
short stable reason code and nothing else.
"""
import datetime
import hashlib
import hmac
import os
import urllib.error
import urllib.parse
import urllib.request

# R2's S3-compatible endpoint expects this region token and service name.
R2_REGION = "auto"
S3_SERVICE = "s3"
_ALGORITHM = "AWS4-HMAC-SHA256"

# One bounded request timeout; a hung provider must not hold an operator job
# open forever.
DEFAULT_TIMEOUT_SECONDS = 120.0

# Single-shot PUT only. Above this the correct answer is multipart upload, which
# this module deliberately does not implement — so it fails closed and says so
# rather than silently truncating or half-uploading.
MAX_OBJECT_BYTES = 4 * 1024 * 1024 * 1024

_HASH_CHUNK_BYTES = 1024 * 1024


class R2UploadError(Exception):
    """An off-provider upload did not demonstrably succeed.

    Every failure mode reaches the caller through this ONE class: bad input, a
    non-HTTPS endpoint, an unreadable source, an oversize object, a provider
    rejection, a transport failure. It carries a short stable reason code and
    never a credential, signature, endpoint secret or file content.
    """

    def __init__(self, reason_code, detail=""):
        message = reason_code if not detail else "%s: %s" % (reason_code, detail)
        super().__init__(message)
        self.reason_code = reason_code


# --- SigV4 primitives (pure; independently testable) -------------------------

def _hmac_sha256(key, message):
    return hmac.new(key, message.encode("utf-8"), hashlib.sha256).digest()


def signing_key(secret_access_key, datestamp, region, service):
    """The SigV4 derived signing key: HMAC chain over date, region, service."""
    initial = ("AWS4" + secret_access_key).encode("utf-8")
    return _hmac_sha256(
        _hmac_sha256(_hmac_sha256(_hmac_sha256(initial, datestamp), region),
                     service),
        "aws4_request")


def canonical_headers(headers):
    """Return ``(canonical_headers_block, signed_headers_list)``.

    Header names are lowercased, values whitespace-trimmed, and both the block
    and the list are ordered by name — the exact canonicalization SigV4 requires.
    """
    normalized = {}
    for name, value in headers.items():
        normalized[str(name).strip().lower()] = " ".join(str(value).split())
    names = sorted(normalized)
    block = "".join("%s:%s\n" % (name, normalized[name]) for name in names)
    return block, ";".join(names)


def canonical_request(method, canonical_uri, canonical_query, headers,
                      payload_hash):
    block, signed = canonical_headers(headers)
    return ("\n".join([method.upper(), canonical_uri, canonical_query, block,
                       signed, payload_hash]),
            signed)


def string_to_sign(amz_date, credential_scope, canonical_request_text):
    digest = hashlib.sha256(canonical_request_text.encode("utf-8")).hexdigest()
    return "\n".join([_ALGORITHM, amz_date, credential_scope, digest])


def authorization_header(access_key_id, secret_access_key, region, service,
                         amz_date, method, canonical_uri, canonical_query,
                         headers, payload_hash):
    """Build the full SigV4 ``Authorization`` value.

    Returns ``(authorization, signed_headers, signature)``. Kept as one pure
    function of its inputs so it can be checked against a published vector.
    """
    datestamp = amz_date[:8]
    request_text, signed = canonical_request(
        method, canonical_uri, canonical_query, headers, payload_hash)
    scope = "/".join([datestamp, region, service, "aws4_request"])
    signature = hmac.new(
        signing_key(secret_access_key, datestamp, region, service),
        string_to_sign(amz_date, scope, request_text).encode("utf-8"),
        hashlib.sha256).hexdigest()
    authorization = (
        "%s Credential=%s/%s, SignedHeaders=%s, Signature=%s"
        % (_ALGORITHM, access_key_id, scope, signed, signature))
    return authorization, signed, signature


# --- object key / path canonicalization --------------------------------------

def canonical_object_uri(bucket, object_key):
    """The canonical URI for a path-style S3 request: ``/bucket/key``.

    Each segment is URI-encoded; ``/`` inside the key is preserved (it is the
    object-name separator, not a character to escape).
    """
    if not bucket or "/" in bucket:
        raise R2UploadError("invalid_bucket")
    key = object_key.lstrip("/")
    if not key or key != object_key.strip() or ".." in key.split("/"):
        raise R2UploadError("invalid_object_key")
    return "/%s/%s" % (urllib.parse.quote(bucket, safe=""),
                       urllib.parse.quote(key, safe="/"))


def account_endpoint(account_id):
    """The R2 S3-compatible origin for one account. Always HTTPS."""
    identifier = (account_id or "").strip()
    if not identifier or any(ch in identifier for ch in "/:? "):
        raise R2UploadError("invalid_account_id")
    return "https://%s.r2.cloudflarestorage.com" % identifier


# --- the one operation -------------------------------------------------------

def _file_digest(path):
    """SHA-256 of the file, read in bounded chunks (never fully in memory)."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(_HASH_CHUNK_BYTES), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _https_put(url, headers, path, size, timeout_seconds):
    """PUT the file at `path` and return ``(status, response-body-bytes)``.

    The default transport. Tests substitute a deterministic local callable, so
    no test performs a network request. `Content-Length` is set explicitly so
    the body is NOT chunk-encoded (a chunked body would not match the payload
    signature).
    """
    if not url.startswith("https://"):
        raise R2UploadError("insecure_endpoint")
    with open(path, "rb") as body:
        request = urllib.request.Request(url, data=body, headers=headers,
                                         method="PUT")
        request.add_unredirected_header("Content-Length", str(size))
        try:
            with urllib.request.urlopen(request,
                                        timeout=timeout_seconds) as response:
                return response.getcode(), response.read(8192)
        except urllib.error.HTTPError as error:
            return error.code, error.read(8192) or b""


def put_object(source_path, bucket, object_key, account_id, access_key_id,
               secret_access_key, endpoint=None,
               timeout_seconds=DEFAULT_TIMEOUT_SECONDS, transport=None,
               now=None):
    """Upload ONE local file to ONE R2 object. Fail closed; no retry.

    Returns a small evidence report (object URI, byte count, SHA-256, provider
    status) on CONFIRMED provider acceptance — a 2xx response and nothing
    weaker. Every other outcome raises ``R2UploadError``.

    The report deliberately contains no credential, no signature and no file
    content; the SHA-256 is of the backup artifact, which the operator can
    recompute locally to prove the stored object matches what was sent.
    """
    for name, value in (("access_key_id", access_key_id),
                        ("secret_access_key", secret_access_key)):
        if not isinstance(value, str) or not value.strip():
            raise R2UploadError("missing_credentials", name)
    if not os.path.isfile(source_path):
        raise R2UploadError("source_not_found")
    size = os.path.getsize(source_path)
    if size <= 0:
        raise R2UploadError("source_empty")
    if size > MAX_OBJECT_BYTES:
        raise R2UploadError("source_too_large_for_single_put")

    origin = (endpoint or account_endpoint(account_id)).rstrip("/")
    if not origin.startswith("https://"):
        raise R2UploadError("insecure_endpoint")
    host = urllib.parse.urlsplit(origin).netloc
    if not host:
        raise R2UploadError("insecure_endpoint")

    uri = canonical_object_uri(bucket, object_key)
    payload_hash = _file_digest(source_path)
    moment = now or datetime.datetime.now(datetime.timezone.utc)
    amz_date = moment.strftime("%Y%m%dT%H%M%SZ")

    signed_headers = {"host": host,
                      "x-amz-content-sha256": payload_hash,
                      "x-amz-date": amz_date}
    authorization, _signed, _signature = authorization_header(
        access_key_id.strip(), secret_access_key.strip(), R2_REGION, S3_SERVICE,
        amz_date, "PUT", uri, "", signed_headers, payload_hash)

    request_headers = dict(signed_headers)
    request_headers["Authorization"] = authorization
    request_headers["Content-Type"] = "application/octet-stream"

    send = transport or _https_put
    try:
        status, _body = send(origin + uri, request_headers, source_path, size,
                             float(timeout_seconds))
    except R2UploadError:
        raise
    except Exception:
        # The cause chain is severed deliberately: a propagating transport error
        # can carry the signed URL (and therefore the object path) into any
        # traceback that gets logged.
        raise R2UploadError("provider_unreachable") from None

    try:
        code = int(status)
    except (TypeError, ValueError):
        raise R2UploadError("provider_response_invalid") from None
    if not 200 <= code < 300:
        raise R2UploadError("provider_rejected", "status %d" % code)

    return {"object": uri, "bytes": size, "sha256": payload_hash,
            "provider_status": code, "accepted": True}
