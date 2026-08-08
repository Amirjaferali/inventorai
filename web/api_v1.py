"""P7-I2 — Versioned Read/Export Public API + first-public-exposure security
baseline (established contract
``docs/governance/P7_I2_VERSIONED_READ_EXPORT_PUBLIC_API_INCREMENT_CONTRACT.md``,
merged PR #405, under Standing Phase-7 Authorization D-P7-STANDING-01).

Purpose: the one small public API transport blueprint exposing EXACTLY the two
read-only V1 product surfaces through the established P7-I1 internal seam:

    GET /api/v1/projects/<project_id>          — versioned Project Read
    GET /api/v1/projects/<project_id>/export   — versioned Structured Export

Input contract: an HTTP GET with a machine credential in the ``Authorization``
header (``Bearer <credential_id>.<secret>``; never in URL/query) and an optional
``X-Request-Id``. Output contract: a versioned JSON envelope carrying
``api_version`` (plus ``export_contract_version`` on export) and the request
correlation id, or the single stable non-enumerating error envelope
``{"error": {"code", "message", "request_id"}}``.

Security baseline honoured here (contract §6–§12):

* Machine/API principal is DISTINCT from the human browser session — this module
  never reads ``_current_account``, the Flask signed-cookie session, or any
  login cookie. A browser-authenticated user without a machine credential does
  not authenticate.
* Two-tier protective rate limiting via the EXISTING hardened atomic
  ``record_rate_attempt`` (P5-2-PRE-01): a PRE-AUTH limiter keyed on a bounded
  fixed-size digest of the *presented* credential identifier, checked BEFORE
  any secret verification, plus a distinct POST-AUTH ``api_read`` limiter keyed
  on the authenticated ``credential_id``. Both fail closed on store failure.
  This is a per-presented-credential protection floor ONLY: each distinct
  presented identifier maps to its own bucket, so it does NOT prevent
  rotating-identifier or distributed abuse — those remain deferred to the
  broader Abuse Controls obligation (P7-C §18); IP/network-origin limiting is
  NOT part of P7-I2.
* Secret verification uses the existing high-entropy token fast-hash precedent
  (``account_credentials.hash_token``) with a constant-time comparison; the raw
  secret is returned only at issuance and never stored or logged.
* Owner-bound authorization is CONSUMED from the P7-I1 seam (cross-owner and
  missing projects collapse into one identical generic denial).
* Every served or denied decision writes one durable ``access_audit`` event;
  audit-write failure and rate-limit-store failure FAIL CLOSED (deny).
* No DDL/migration runs here (contract §12): the additive tables live in the
  existing ``SqliteAccountStore`` constructor-owned schema lifecycle.

Prohibited here (contract §4/§17, D-FPC-MAP-06): any non-GET method, mutation,
import/write path, additional public surface, browser-session reuse, duplicate
authorization/rate-limit/audit framework, quotas/billing, monitoring platform,
or P7-I3 integration code.
"""
import hashlib
import hmac
import re
import uuid

from flask import Blueprint, jsonify, request

from engine import account_credentials as _acct
from engine import read_export_service as _seam

api_v1_bp = Blueprint("api_v1", __name__, url_prefix="/api/v1")

API_VERSION = "v1"
EXPORT_CONTRACT_VERSION = "1"
SCOPE_PROJECT_READ = "project:read"

# Bounded protective floors (named constants; deterministic and test-overridable;
# NOT quotas/billing tiers). Pre-auth mirrors the login-limiter posture; the
# authenticated tier is a distinct, more permissive read floor.
_PREAUTH_RATE_LIMIT = 30
_PREAUTH_RATE_WINDOW_SECONDS = 15 * 60
_API_READ_RATE_LIMIT = 120
_API_READ_RATE_WINDOW_SECONDS = 60 * 60

# Input bounds: the presented credential material is length-bounded BEFORE any
# digest/lookup work; the audit target id is stored bounded.
_MAX_PRESENTED_CREDENTIAL_LENGTH = 512
_MAX_AUDIT_PROJECT_ID_LENGTH = 128
_REQUEST_ID_RE = re.compile(r"[A-Za-z0-9-]{1,64}")

# The stable public error vocabulary (contract §9): one shape, generic wording,
# no internal detail, no existence disclosure.
_ERROR_HTTP_STATUS = {
    "unauthenticated": 401,
    "forbidden": 403,
    "not_available": 404,
    "invalid_request": 400,
    "rate_limited": 429,
    "internal_error": 500,
}
_ERROR_MESSAGES = {
    "unauthenticated": "Authentication was not accepted.",
    "forbidden": "The credential does not permit this operation.",
    "not_available": "The requested resource is not available.",
    "invalid_request": "The request could not be processed.",
    "rate_limited": "Too many attempts. Please try again later.",
    "internal_error": "The service could not complete the request.",
}


def _webapp():
    """The web composition root (lazy import: this module is imported by
    ``web.app`` at mount time). Stores are ALWAYS obtained through the existing
    application-scoped accessors — this module never constructs a datastore."""
    import web.app as webapp
    return webapp


def _now_iso():
    webapp = _webapp()
    return webapp._iso(webapp._utc_now())


# --- programmatic credential issuance (contract §13) ---------------------------
def issue_api_credential(store, owner_account_id, scopes=None, expires_at=None):
    """Programmatic/internal issuance path (no owner-facing UI): generate a
    high-entropy secret, persist ONLY its one-way hash bound to exactly one
    ``owner_account_id`` with the ``project:read`` scope by default, and return
    ``(credential_id, raw_secret)``. The raw secret exists only in this return
    value — it is never stored, logged, or shown again. Revocation is the
    existing store path ``store.revoke_api_credential`` (rotation = issue new +
    revoke old)."""
    scope_string = " ".join(scopes) if scopes else SCOPE_PROJECT_READ
    credential_id = "apic_" + uuid.uuid4().hex
    raw_secret = _acct.new_raw_token()
    store.create_api_credential(
        credential_id=credential_id,
        secret_hash=_acct.hash_token(raw_secret),
        owner_account_id=owner_account_id,
        scopes=scope_string,
        created_at=_now_iso(),
        expires_at=expires_at)
    return credential_id, raw_secret


# --- correlation identity (contract §9/§11/§16.E) ------------------------------
def _resolve_request_id():
    """Server-generated request id by default. A caller-supplied ``X-Request-Id``
    is accepted only when it matches the bounded charset/length rule; anything
    malformed is REPLACED (never echoed unchanged) so a caller cannot inject
    into logs/audit."""
    supplied = request.headers.get("X-Request-Id", "")
    if supplied and _REQUEST_ID_RE.fullmatch(supplied):
        return supplied
    return "req-" + uuid.uuid4().hex


# --- rate limiting (contract §10) ----------------------------------------------
def _presented_subject(presented):
    """Bounded fixed-size limiter subject for the *presented* credential
    identifier: the input is length-bounded, then reduced to a truncated SHA-256
    digest (the existing ``email_digest`` precedent), so a raw unbounded
    identifier is never stored as a limiter subject. This bounds the subject
    REPRESENTATION only — each distinct presented identifier still derives its
    own bucket, so rotating/distributed abuse is NOT prevented here (deferred
    broader Abuse Controls; P7-C §18)."""
    bounded = (presented or "")[:_MAX_PRESENTED_CREDENTIAL_LENGTH]
    return hashlib.sha256(
        ("p7i2-api-cred:" + bounded).encode("utf-8")).hexdigest()[:32]


def _rate_check(subject_key, action, limit, window_seconds):
    """One atomic bounded-window attempt via the EXISTING hardened store counter.
    Returns "ok", "limited", or "error"; a store failure can never fail open."""
    webapp = _webapp()
    now = webapp._utc_now()
    try:
        allowed = webapp._get_account_store().record_rate_attempt(
            subject_key=subject_key, action=action, now_iso=webapp._iso(now),
            window_reset_iso=webapp._iso(
                now + webapp._timedelta_seconds(window_seconds)),
            limit=limit)
    except Exception:
        return "error"
    return "ok" if allowed else "limited"


# --- response + audit plumbing (contract §9/§11) -------------------------------
def _error_body(code, rid):
    return {"error": {"code": code, "message": _ERROR_MESSAGES[code],
                      "request_id": rid}}


def _finish(rid, surface, project_id, credential_id, outcome, body, status):
    """Write the mandatory durable audit event, then return the response. If the
    audit event cannot be recorded the decision is NOT served: the response is
    replaced by the generic internal error (fail closed, contract §11)."""
    try:
        _webapp()._get_account_store().record_access_audit(
            request_id=rid, surface=surface, outcome=outcome,
            created_at=_now_iso(), credential_id=credential_id,
            project_id=(project_id or "")[:_MAX_AUDIT_PROJECT_ID_LENGTH])
    except Exception:
        return jsonify(_error_body("internal_error", rid)), 500
    return jsonify(body), status


def _deny(rid, surface, project_id, credential_id, code, outcome):
    return _finish(rid, surface, project_id, credential_id, outcome,
                   _error_body(code, rid), _ERROR_HTTP_STATUS[code])


# --- authentication / authorization pipeline (contract §6/§7/§10/§11) ----------
def _authenticate(rid, surface, project_id):
    """Resolve the machine principal for this request. Returns
    ``(credential_row, None)`` on success or ``(None, error_response)`` on any
    denial. Order is frozen by the contract: presented credential identifier →
    bound input → fixed-size subject digest → atomic PRE-AUTH limiter →
    credential lookup → constant-time secret verification → lifecycle checks
    (revoked / expired / bound-account status) → scope → POST-AUTH limiter.
    Every failure is a generic non-enumerating denial."""
    header = request.headers.get("Authorization", "")
    if header.startswith("Bearer "):
        presented = header[len("Bearer "):].strip()
    else:
        presented = header.strip()
    if not presented:
        return None, _deny(rid, surface, project_id, None,
                           "unauthenticated", "denied_unauthenticated")

    # The pre-auth limiter subject is the presented credential IDENTIFIER (the
    # part before the secret separator; the whole presented value when it has no
    # separator), so unknown-credential attempts and invalid-secret attempts for
    # the same presented id consume the SAME bucket (contract §10.A).
    credential_id, sep, secret = presented.partition(".")

    # PRE-AUTH tier: consumed by unknown credentials, malformed credentials, and
    # invalid secrets alike — always BEFORE any secret verification work.
    outcome = _rate_check(_presented_subject(credential_id or presented),
                          "api_preauth",
                          _PREAUTH_RATE_LIMIT, _PREAUTH_RATE_WINDOW_SECONDS)
    if outcome == "limited":
        return None, _deny(rid, surface, project_id, None,
                           "rate_limited", "denied_rate_limited")
    if outcome == "error":
        return None, _deny(rid, surface, project_id, None,
                           "internal_error", "error_internal")

    if not sep or not credential_id or not secret:
        return None, _deny(rid, surface, project_id, None,
                           "unauthenticated", "denied_unauthenticated")

    store = _webapp()._get_account_store()
    # the presented secret is hashed BEFORE the unknown/known branch so an
    # unknown credential id costs the same hash work as a wrong secret (no
    # credential-id existence signal through response timing)
    presented_hash = _acct.hash_token(secret)
    row = store.get_api_credential(credential_id)
    if row is None:
        return None, _deny(rid, surface, project_id, None,
                           "unauthenticated", "denied_unauthenticated")
    if not hmac.compare_digest(row["secret_hash"], presented_hash):
        return None, _deny(rid, surface, project_id, None,
                           "unauthenticated", "denied_unauthenticated")
    if row["status"] != "active":
        return None, _deny(rid, surface, project_id, None,
                           "unauthenticated", "denied_unauthenticated")
    if row["expires_at"] is not None and _now_iso() >= row["expires_at"]:
        return None, _deny(rid, surface, project_id, None,
                           "unauthenticated", "denied_unauthenticated")
    account = store.get_account_by_id(row["owner_account_id"])
    if account is None or account["status"] != "active":
        # canonical account semantics: only an ACTIVE bound account authenticates
        return None, _deny(rid, surface, project_id, None,
                           "unauthenticated", "denied_unauthenticated")
    if SCOPE_PROJECT_READ not in row["scopes"].split():
        return None, _deny(rid, surface, project_id, row["credential_id"],
                           "forbidden", "denied_forbidden")

    # POST-AUTH tier: the distinct authenticated ``api_read`` protective floor.
    outcome = _rate_check(row["credential_id"], "api_read",
                          _API_READ_RATE_LIMIT, _API_READ_RATE_WINDOW_SECONDS)
    if outcome == "limited":
        return None, _deny(rid, surface, project_id, row["credential_id"],
                           "rate_limited", "denied_rate_limited")
    if outcome == "error":
        return None, _deny(rid, surface, project_id, row["credential_id"],
                           "internal_error", "error_internal")
    return row, None


# --- the two public V1 surfaces (contract §2/§4/§8) ----------------------------
def _handle(project_id, surface):
    rid = _resolve_request_id()
    credential = None
    try:
        credential, error = _authenticate(rid, surface, project_id)
        if error is not None:
            return error
        account_id = credential["owner_account_id"]
        record_store = _webapp()._get_store()
        try:
            if surface == "project_read":
                contract = _seam.get_authorized_project_read(
                    record_store, project_id, account_id)
                body = {
                    "api_version": API_VERSION,
                    "request_id": rid,
                    # data-minimized projection — deliberately NOT the record
                    # contract's lossless to_dict() (contract §8)
                    "project": {
                        "idea_id": contract.idea_id,
                        "assertion_count": len(list(
                            getattr(contract, "assertions", []))),
                    },
                }
            else:
                export = _seam.produce_project_export(
                    record_store, project_id, account_id)
                body = {
                    "api_version": API_VERSION,
                    "export_contract_version": EXPORT_CONTRACT_VERSION,
                    "request_id": rid,
                    "export": export,
                }
        except _seam.ProjectAccessDenied:
            # cross-owner and missing collapse into ONE identical generic denial
            return _deny(rid, surface, project_id, credential["credential_id"],
                         "not_available", "denied_not_available")
        return _finish(rid, surface, project_id, credential["credential_id"],
                       "served", body, 200)
    except Exception:
        # no exception detail ever reaches the public envelope (fail closed)
        return _deny(rid, surface, project_id,
                     credential["credential_id"] if credential else None,
                     "internal_error", "error_internal")


@api_v1_bp.get("/projects/<project_id>")
def project_read(project_id):
    return _handle(project_id, "project_read")


@api_v1_bp.get("/projects/<project_id>/export")
def project_export(project_id):
    return _handle(project_id, "project_export")
