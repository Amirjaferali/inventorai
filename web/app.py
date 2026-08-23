"""
InventorAI Web Interface (Phase H-A)
Thin web shell only. Engine called as library.
SESSION_STORE: in-memory, non-production, temporary.
"""
import json
import os
import re
import secrets
import tempfile
import uuid
from urllib.parse import urlparse as _urlparse
from flask import (
    Flask, request, redirect, url_for, render_template, make_response,
    has_request_context, session as flask_session,
)
from engine.domain_rules import classify_domain, DomainResultKind, is_known_domain
from engine import domain_activation
from engine.idea_state import (
    IdeaState, SuccessCriterion,
    CRITICALITY_FEASIBILITY_THREATENING, CRITICALITY_VALUE_ENHANCING,
    CRITICALITY_REFINEMENT, CRITICALITY_ACTION_CONFIRMED,
    CRITICALITY_ACTION_DEFERRED,
)
# Workstream 4 (structured criticality): the same pure landscape derivation
# that feeds Section 13, used read-only to select the confirmation focus.
from engine.requirement_landscape import derive_requirement_landscape
from engine.progression_loop import (
    run_iteration, select_next_gap, get_question, get_display_question,
    # RVR-1 (Wave-1): the canonical accepted-risk lifecycle writer and the
    # existing next-gap cascade, invoked ONLY by the explicit accept-risk route.
    accept_gap_risk, _open_next_gap_if_needed,
)
from engine.idea_state import (
    DISPOSITION_RISK_ACCEPTED, MECHANISM_COMPLETENESS as _MECH_GAP,
)
from web.gap_labels import (
    GAP_LABELS, get_gap_label, get_maturity_label, SESSION_DISCLOSURE,
    get_session_disclosure, friendly_gap_name,
)
from web import ui_text
from web import observability as _obs
from urllib.request import pathname2url as _pathname2url
from engine.deliverable_assembler import assemble_deliverable
# P4-1b-1 (G-P4-1B-1-DOC-01 / PR #358): the merged P4-1a durable store and the
# P4-0 record contract, used ONLY to durably create and cold-load a NEW project
# envelope keyed by the unified sid==project_id capability. No accepted-input
# append, Keep/Refine durability, transcript/last_result persistence, or replay
# is introduced here (those are P4-1b-2 / P4-2).
import sqlite3
from engine.record_store import SqliteRecordStore, StoreError
from engine.record_contract import ProjectRecordContract
# P10-D3a (established contract, PR #510): the canonical internal read/export
# seam (P7-I1), consumed UNMODIFIED by the browser self-service export route.
from engine import read_export_service as _read_export
# P5-1 — Account & Credential Foundation (Phase 5, Option A). Additive account
# persistence + pure credential helpers + a development email sink. NO login /
# authenticated session / project ownership here (those are P5-2 / P5-3).
from engine.account_store import (
    SqliteAccountStore, EmailExistsError, VERIFICATION, RESET,
)
from engine import account_credentials as _acct
from engine import auth_session as _auth
from engine.email_sender import DevMemoryEmailSender
# P4-2 Level-1: the exact supported reconstruction/engine-contract version stamp
# persisted at project creation (read-only reconstruction lives entirely in the
# engine; web only persists these additive envelope inputs).
from engine.session_reconstruction import (
    RECONSTRUCTION_VERSION,
    reconstruct_readonly_state,
    reconstruct_review_state,
)
# Increment 3 (R-5): the SAME shared public derivation that feeds the deliverable
# section, imported as a module-level name so one selection feeds both surfaces.
from engine.idea_development_outputs import derive_next_development_step
from web.responsibility_labels import get_responsibility  # Increment 1B: advisory only
from web.clarification_labels import get_clarification  # Increment 1B: display-only clarification
from web.scaffolding_guidance import get_scaffolding_guidance  # MDN: display-only WARN guidance
from web.answer_coauthoring_prompts import get_answer_coauthoring_prompts  # GACA Increment 1: display-only advisory prompts
from web.uncertainty_guidance import get_uncertainty_guidance  # GUS: display-only supportive uncertainty guidance
from web.result_feedback import get_result_feedback  # PLRF: display-only plain-language result feedback
from web.domain_label import public_domain_label as _public_domain_label  # P6-1: central public label resolver (display-only)

# --- G-SC0 Bounded Security Containment: runtime security configuration -------
# Runtime debug, host, and the Flask secret are environment-controlled with safe
# defaults. No secret value is hard-coded in source. See README "Runtime security
# configuration". No accounts/authentication/authorization are introduced here.
_TRUTHY = frozenset({"1", "true", "yes", "on"})


def _debug_enabled():
    """Debug is OFF unless INVENTORAI_DEBUG is an explicit recognized truthy value.
    Ambiguous or unknown values never enable debug."""
    return os.environ.get("INVENTORAI_DEBUG", "").strip().lower() in _TRUTHY


def _resolve_host():
    """Host defaults to loopback (127.0.0.1); override only via INVENTORAI_HOST."""
    return os.environ.get("INVENTORAI_HOST", "").strip() or "127.0.0.1"


def _is_production():
    return os.environ.get("INVENTORAI_ENV", "").strip().lower() == "production"


def _resolve_secret_key():
    """Return the Flask secret. Sourced from INVENTORAI_SECRET_KEY. When explicit
    production mode is enabled and the secret is missing, fail clearly. For local
    development only, an ephemeral random secret is generated (never persisted or
    logged). No fixed secret value is stored in source."""
    secret = os.environ.get("INVENTORAI_SECRET_KEY", "")
    if secret:
        return secret
    if _is_production():
        raise RuntimeError(
            "INVENTORAI_SECRET_KEY must be set to a non-empty value when "
            "INVENTORAI_ENV=production."
        )
    return secrets.token_hex(32)


app = Flask(__name__)
app.secret_key = _resolve_secret_key()
# P5-2: authenticated-session cookie hardening (contract §6). The signed-cookie
# session (name "session") is DISTINCT from the project `sid`. HttpOnly + SameSite
# =Lax always; Secure only in explicit production (so http:// dev/tests still
# work); a bounded absolute cookie lifetime matching the 14-day absolute session
# expiry. Server-side idle/absolute/epoch checks remain authoritative.
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=_is_production(),
    PERMANENT_SESSION_LIFETIME=__import__("datetime").timedelta(
        seconds=_auth.ABSOLUTE_TIMEOUT_SECONDS),
    # P10-SEC2: one transport-level request-body bound. 128 KiB comfortably
    # covers the largest legitimate payload (a MAX_FREE_TEXT_CHARS free-text
    # field at worst-case 4-byte UTF-8 ≈ 80 KiB, plus small form fields) while
    # rejecting pathological bodies with Werkzeug's standard 413. This bounds
    # transport size only — it is NOT a WAF, NOT DoS prevention, and NOT a
    # production proxy limit.
    MAX_CONTENT_LENGTH=128 * 1024,
)
# P10-SEC1: ONE centralized provider-neutral response-hardening seam. Every
# response (HTML, JSON, redirects, 4xx/5xx, static files, /health) receives the
# same bounded security-header set. The CSP is the smallest policy supported by
# the verified compatibility inventory of this application:
#   * default-src 'none'      — deny-by-default; the app loads no images, fonts,
#                               media, or remote assets and makes no fetch/XHR;
#   * script-src 'self'       — the ONLY script is the same-origin static
#                               web/static/js/local_draft.js; ZERO inline script
#                               bodies and ZERO inline event handlers exist, so
#                               'unsafe-inline' is NOT granted for scripts;
#   * style-src 'unsafe-inline' — narrowly justified: every template styles
#                               itself via inline <style> blocks/attributes and
#                               no external stylesheet exists; removing this
#                               would be a UI redesign outside this gate;
#   * frame-ancestors 'none'  — no legitimate framing exists (clickjacking
#                               denial, consistent with X-Frame-Options: DENY);
#   * base-uri 'none'; form-action 'self' — no <base> tag; all forms post to
#                               same-origin relative paths.
# No 'unsafe-eval'. No wildcard/host/scheme sources. No reporting endpoint.
# HSTS is deliberately ABSENT: no TLS termination or trusted-proxy semantics
# exist in this repository, so emitting Strict-Transport-Security anywhere
# would assert an HTTPS posture that does not exist (DEFERRED to the future
# production/infrastructure gate). `setdefault` keeps the seam additive: a
# route that explicitly sets one of these headers is never overwritten. These
# headers harden responses; they do NOT constitute a security review, PSRR
# execution, TLS posture, or any compliance claim.
_SECURITY_HEADERS = (
    ("Content-Security-Policy",
     "default-src 'none'; script-src 'self'; style-src 'unsafe-inline'; "
     "frame-ancestors 'none'; base-uri 'none'; form-action 'self'"),
    ("X-Content-Type-Options", "nosniff"),
    ("X-Frame-Options", "DENY"),
    ("Referrer-Policy", "strict-origin-when-cross-origin"),
)


@app.after_request
def _apply_security_headers(response):
    for name, value in _SECURITY_HEADERS:
        response.headers.setdefault(name, value)
    return response


# EMAIL-H1 (OBS-P5-2-01, application-controlled portion): the emailed
# verification and reset links carry the RAW token in the URL path. The URL-token
# architecture, token hashing, TTLs, single-use consumption and generic failure
# behaviour are all UNCHANGED here; this seam hardens only what the application
# itself governs about those two responses:
#   * Referrer-Policy: no-referrer — a token-bearing page must never hand its own
#     URL (and therefore the token) to any outbound navigation. This tightens the
#     global `strict-origin-when-cross-origin` default for THESE responses only;
#     the global baseline is unchanged for every other route, and the `setdefault`
#     seam above deliberately never overwrites a route-set header.
#   * Cache-Control: no-store — the token-bearing response must not be written to
#     a browser or intermediary cache. `no-store` is the complete directive for
#     this purpose; no legacy `Pragma` companion is added because nothing in this
#     repository targets an HTTP/1.0 cache and an untested directive would be an
#     unsupported claim.
# PROVIDER/PROXY ACCESS-LOG TOKEN EXPOSURE IS NOT ADDRESSED HERE and remains OPEN:
# what a hosting provider or reverse proxy records in its access logs is outside
# application control and must be verified before a production email-provider or
# reverse-proxy deployment.
_TOKEN_BEARING_RESPONSE_HEADERS = (
    ("Referrer-Policy", "no-referrer"),
    ("Cache-Control", "no-store"),
)

# The endpoints whose URL path contains a raw single-use token.
_TOKEN_BEARING_ENDPOINTS = frozenset(
    ("verify_email", "reset_form", "reset_submit"))


def _token_bearing(body, status=200):
    """Return ``body`` as a response carrying the token-bearing hardening headers.

    Set explicitly (not `setdefault`) so the tightened values win over the global
    baseline for these responses only."""
    response = make_response(body, status)
    for name, value in _TOKEN_BEARING_RESPONSE_HEADERS:
        response.headers[name] = value
    return response


@app.context_processor
def _inject_safe_language_switch_target():
    """EMAIL-H1: the shared shell's language links carry ``next=<current path>``.

    On a token-bearing page that would reflect the RAW token into a rendered
    anchor href. For those endpoints only, the language switch returns to the
    landing page instead; everywhere else the behaviour is unchanged. Switching
    language on a reset/verify page therefore leaves that page — the emailed link
    remains valid and can simply be reopened (nothing is consumed by rendering)."""
    target = "/"
    if has_request_context():
        target = request.path
        if request.endpoint in _TOKEN_BEARING_ENDPOINTS:
            target = "/"
    return {"lang_switch_next": target}


# P10-SEC2: one semantic free-text bound for the two primary free-text
# surfaces (the /start idea text and the /session/<sid> answer/action text).
# 20,000 characters is justified from PRESENT product behavior — an order of
# magnitude above every legitimate description observed in repository evidence
# (governed ILT-002 transcripts and tests use well under 2,000 characters) —
# and deliberately NOT the stale 10,000 figure from historical documentation.
# Policy: EXPLICIT rejection only — never silent truncation, never stripping,
# never normalization. NUL (\x00) is rejected as invalid product content
# (silent stripping could change user intent). Newlines, tabs, punctuation,
# Arabic, and all other legitimate Unicode pass untouched; there is NO general
# control-character sanitizer and NO ASCII-only rule.
MAX_FREE_TEXT_CHARS = 20000


def _free_text_error(value, lang):
    """Return None when `value` is acceptable free text, else a bounded
    bilingual rejection message (fixed catalogue copy, `_unsupported_domain_
    message` precedent). Rejects ONLY: length > MAX_FREE_TEXT_CHARS, or an
    embedded NUL byte. Never mutates the value; never echoes it back."""
    if len(value) > MAX_FREE_TEXT_CHARS:
        if lang == "ar":
            return ("النص المُدخل أطول من الحد المسموح (%d حرفًا). "
                    "لم يتم حفظ أي شيء — يُرجى تقصير النص وإعادة الإرسال."
                    % MAX_FREE_TEXT_CHARS)
        return ("The submitted text is longer than the allowed limit "
                "(%d characters). Nothing was saved - please shorten the "
                "text and submit again." % MAX_FREE_TEXT_CHARS)
    if "\x00" in value:
        if lang == "ar":
            return ("النص المُدخل يحتوي على رمز غير صالح. "
                    "لم يتم حفظ أي شيء — يُرجى إزالة الرمز وإعادة الإرسال.")
        return ("The submitted text contains an invalid character. Nothing "
                "was saved - please remove it and submit again.")
    return None


# Presentation-only Jinja filter: translate an internal gap-type ID to a short
# inventor-friendly label for the few session-page surfaces that render raw
# reference/context IDs. Non-gap values pass through unchanged. Display only.
app.jinja_env.filters["gap_display"] = friendly_gap_name
# P6-1 (Truthful Domain Labeling Foundation): the SINGLE central, server-side,
# bilingual public-domain-label resolver. Templates consume this one filter so no
# surface reproduces domain-id conditionals or a hard-coded label; it maps the
# trusted runtime domain to a Tier-1 public label and falls back to a neutral
# "General idea review" for unknown/missing/unsupported state (never electronics).
# Presentation only — activates no domain and changes no deterministic behavior.
app.jinja_env.filters["public_domain_label"] = _public_domain_label
# D-P6-18: expose the UI-string resolver and language/direction to EVERY template
# render path. For normal requests the context processor below overrides these with
# the per-request values; registering them as Jinja globals additionally keeps a
# direct ``jinja_env.get_template(...).render(...)`` (used by some tests) working —
# ``t`` stays request-safe and defaults to English outside a request context.
app.jinja_env.globals["t"] = lambda key: ui_text.text(key, _current_ui_lang())
app.jinja_env.globals["ui_lang"] = "en"
app.jinja_env.globals["ui_dir"] = "ltr"
SESSION_STORE = {}

# --- P4-1b-1: durable project store (construction, configuration, cold-load) --
# The in-memory SESSION_STORE remains the active working state within a live
# process; SQLite is the durable project-envelope mirror and cold-reload source,
# keyed by the unified `sid`==`project_id` pre-account capability. There is NO
# sid->project_id mapping table, no project_ids() scan, and no reversible mapping
# layer. project_ids() is never exposed through any route/API/UI surface. This
# capability is an unguessable lookup only — not authentication, ownership,
# account authorization, or verified identity (Phase 5). No cache framework or
# invalidation platform is introduced.
_STORE = None
# Generic, non-disclosing message for a durable-store failure at /start. It never
# reveals project existence, capability validity, contract state, or DB detail.
SERVICE_UNAVAILABLE_MESSAGE = (
    "This service is temporarily unavailable. Please try again in a moment.")


def _resolve_db_path():
    """Resolve the SQLite database path from INVENTORAI_DB_PATH.

    Explicit env value wins. In explicit production mode a missing value is a
    hard fail (no silent fallback). For local development only, an explicit,
    app-namespaced temp path is used (never a repository-tracked file; the
    envelope carries no verbatim user content — R6 is preserved)."""
    path = os.environ.get("INVENTORAI_DB_PATH", "").strip()
    if path:
        return path
    if _is_production():
        raise RuntimeError(
            "INVENTORAI_DB_PATH must be set to a writable path when "
            "INVENTORAI_ENV=production.")
    return os.path.join(tempfile.gettempdir(), "inventorai_dev",
                        "inventorai_p4_1b1.sqlite")


def _get_store():
    """Return the one application-scoped SqliteRecordStore (single-process MVP),
    building it on first use from the resolved path. Multi-worker topology,
    pooling, per-request connections, WAL tuning, and production datastore
    selection are deferred. Raises on an unusable path (caller fails closed)."""
    global _STORE
    if _STORE is None:
        path = _resolve_db_path()
        directory = os.path.dirname(path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        _STORE = SqliteRecordStore(path)
    return _STORE


# --- P5-1: account store, development email sink, and bounded policy ----------
# The account store is SEPARATE from the project record store (its own connection
# + tables) and shares the same INVENTORAI_DB_PATH file. It is additive: opening
# it on a pre-P5 database only creates the new tables. No accounts/auth/ownership
# behaviour is wired beyond registration + verification-token issuance here.
_ACCOUNT_STORE = None
# Development-only email sink (in-memory). A production provider adapter is a
# separate, later concern; the raw verification token appears ONLY in a sink
# message body and never in the application logs.
_EMAIL_SENDER = DevMemoryEmailSender()

_VERIFICATION_TTL_SECONDS = 24 * 60 * 60          # contract §8: 24 hours
# Foundational bounded rate limit for registration (contract §10): a small
# store-backed counter, NOT an abuse-prevention platform. Same generic response
# whether accepted, duplicate, or limited.
_REGISTER_RATE_LIMIT = 10
_REGISTER_RATE_WINDOW_SECONDS = 60 * 60
# One generic, non-enumerating registration response (contract §7): it never
# reveals whether the email was newly registered, already in use, or belongs to a
# disabled/deleted account, nor whether an email was actually sent.
REGISTER_GENERIC_MESSAGE_EN = (
    "If the address can be used, verification instructions have been sent.")
REGISTER_GENERIC_MESSAGE_AR = (
    "إذا كان بالإمكان استخدام هذا العنوان، فسيتم إرسال تعليمات التحقق.")


def _get_account_store():
    """Return the one application-scoped SqliteAccountStore, built on first use
    from the resolved DB path (same file as the project store; separate tables)."""
    global _ACCOUNT_STORE
    if _ACCOUNT_STORE is None:
        path = _resolve_db_path()
        directory = os.path.dirname(path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        _ACCOUNT_STORE = SqliteAccountStore(path)
    return _ACCOUNT_STORE


# --- P10-OB1: minimal provider-neutral health/readiness surface ----------------
def _database_health():
    """Non-mutating local-dependency probe (P10-OB1). Answers only: are the
    required LOCAL runtime dependencies usable right now?

    Never creates a file, schema, or row: already-initialized application
    stores are probed with existing PUBLIC read-only reads; an existing but
    not-yet-opened database file is opened strictly read-only for a trivial
    read; a missing file reports ``"uninitialized"`` (the lazy runtime creates
    it on first real use, so absence is a normal pre-first-use state, not a
    failure). Returns ``"ok"`` | ``"uninitialized"`` | ``"error"``. It proves
    nothing about external providers, payment, hosting, security, PSRR, legal
    readiness, or deployment readiness."""
    try:
        probed = False
        if _ACCOUNT_STORE is not None:
            _ACCOUNT_STORE.count_accounts()
            probed = True
        if _STORE is not None:
            _STORE.project_ids()
            probed = True
        if probed:
            return "ok"
        path = _resolve_db_path()
        if not os.path.isfile(path):
            return "uninitialized"
        conn = sqlite3.connect(
            "file:%s?mode=ro" % _pathname2url(os.path.abspath(path)),
            uri=True)
        try:
            # A trivial catalog read: forces a real page-1 read (a corrupt or
            # non-SQLite file fails here) while remaining strictly read-only.
            conn.execute("SELECT count(*) FROM sqlite_master").fetchone()
        finally:
            conn.close()
        return "ok"
    except Exception as exc:
        # Bounded operational diagnostics only: the exception CLASS name —
        # never message text, a path, or user data (P10-OB1 data-minimization).
        _obs.emit("health.db_probe_failed", level="warning",
                  component="health", error_class=type(exc).__name__)
        return "error"


def _utc_now():
    from datetime import datetime
    return datetime.utcnow()


def _iso(dt):
    # Canonical fixed-width UTC ISO-8601 (always 6-digit microseconds) so the
    # bounded rate-limit window check — which compares these timestamp STRINGS
    # lexicographically (engine.account_store.record_rate_attempt) — stays
    # monotonic even at the exact-whole-second boundary, where a bare
    # ``isoformat()`` would omit the microseconds and break ordering.
    return dt.strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"


# --- P5-2: authenticated sessions / verification / recovery -------------------
# Token lifetimes (contract §10/§13): verification 24h (reused from P5-1),
# reset 1h. Bounded rate limits keyed on privacy-safe digests. All auth responses
# are generic and non-enumerating.
_RESET_TTL_SECONDS = 60 * 60                      # reset token: 1 hour
_LOGIN_RATE_LIMIT = 10
_LOGIN_RATE_WINDOW_SECONDS = 15 * 60
_RESEND_RATE_LIMIT = 5
_RESEND_RATE_WINDOW_SECONDS = 60 * 60
_RECOVER_RATE_LIMIT = 5
_RECOVER_RATE_WINDOW_SECONDS = 60 * 60
_AUTH_SESSION_KEY = "auth"                        # namespaced slot inside flask.session

# One generic, non-enumerating message per auth surface (never reveals whether an
# email exists, a password was wrong, or an account is disabled/deleted/unverified).
LOGIN_FAILED_MESSAGE_EN = "Those sign-in details did not match. Please try again."
LOGIN_FAILED_MESSAGE_AR = "بيانات تسجيل الدخول غير متطابقة. يرجى المحاولة مرة أخرى."
RECOVER_GENERIC_MESSAGE_EN = (
    "If that address matches an account, password-reset instructions have been sent.")
RECOVER_GENERIC_MESSAGE_AR = (
    "إذا كان هذا العنوان مطابقًا لحساب، فقد أُرسلت تعليمات إعادة تعيين كلمة المرور.")
RESEND_GENERIC_MESSAGE_EN = (
    "If verification is still needed, a new verification message has been sent.")
RESEND_GENERIC_MESSAGE_AR = (
    "إذا كان التحقق لا يزال مطلوبًا، فقد أُرسلت رسالة تحقق جديدة.")


def _cleanup_rate_limits(now):
    """Opportunistic bounded cleanup of expired rate-limit rows (contract §3).
    Never raises into the request path."""
    try:
        _get_account_store().cleanup_expired_rate_limits(_iso(now))
    except Exception:
        pass


def _rate_ok(subject_key, action, now, limit, window_seconds):
    """Concurrency-safe rate check via the hardened store primitive. Fails closed
    (returns False) on any store error so a failure can never bypass the limit."""
    try:
        return _get_account_store().record_rate_attempt(
            subject_key=subject_key, action=action, now_iso=_iso(now),
            window_reset_iso=_iso(now + _timedelta_seconds(window_seconds)),
            limit=limit)
    except Exception:
        return False


def _current_account():
    """Return the live, valid signed-in account (dict) or None. Validates the
    authenticated session against the live account and the clock (status / epoch /
    idle / absolute); on ANY failure it clears the session and returns None (fail
    closed). Slides the idle window on success."""
    auth = flask_session.get(_AUTH_SESSION_KEY)
    if not auth:
        return None
    try:
        account = _get_account_store().get_account_by_id(auth.get("account_id"))
    except Exception:
        account = None
    now = _utc_now()
    ok, _reason = _auth.validate_session(auth, account, now)
    if not ok:
        flask_session.pop(_AUTH_SESSION_KEY, None)
        return None
    flask_session[_AUTH_SESSION_KEY] = _auth.touch_session(auth, now)
    return account


@app.context_processor
def _inject_account_context():
    """Expose a lightweight ``account_context`` to every template for the bounded
    Draft-L2 account-switch isolation (contract §15). It is the signed-in
    ``account_id`` (from the cookie claim) or ``"anon"`` when signed out — used
    ONLY to namespace same-device local drafts so one account's draft is never
    shown under another account (or anonymously). It performs NO database read and
    NO session mutation, and it is NOT an authorization or ownership signal."""
    auth = flask_session.get(_AUTH_SESSION_KEY)
    ctx = auth.get("account_id") if isinstance(auth, dict) else None
    return {"account_context": ctx or "anon"}


# --- D-P6-18 Global UI Language ----------------------------------------------
# The explicit UI-language selection (English | العربية) lives in the signed Flask
# session under a single ``ui_lang`` slot, DISTINCT from the auth slot and from any
# project state. It is a presentation preference only: it is never inferred from
# user input, carries no authorization/ownership meaning, and controls no
# deterministic behaviour, engine, schema, or account persistence. Default English.
def _current_ui_lang():
    """The selected UI language (``"en"`` default / ``"ar"``). Request-context
    safe: returns English outside a request (e.g. a direct template render), so
    the ``t`` Jinja global below never raises."""
    if not has_request_context():
        return "en"
    return ui_text.normalize(flask_session.get("ui_lang"))


@app.context_processor
def _inject_ui_language():
    """Expose the selected UI language, its writing direction, and the central
    ``t(key)`` UI-string resolver to every template (single-language rendering)."""
    lang = _current_ui_lang()
    return {
        "ui_lang": lang,
        "ui_dir": ui_text.direction(lang),
        "t": (lambda key: ui_text.text(key, lang)),
    }


def _is_safe_local_path(target):
    """True only for a same-origin relative path (leading single ``/``); blocks
    protocol-relative and absolute-URL open-redirect targets."""
    if not isinstance(target, str) or not target.startswith("/") or target.startswith("//"):
        return False
    parsed = _urlparse(target)
    return not parsed.scheme and not parsed.netloc


@app.route("/ui-language", methods=["GET", "POST"])
def set_ui_language():
    """Set the explicit global UI language and return to the originating page.

    Presentation only: it writes the ``ui_lang`` preference into the signed session
    and redirects to a SAFE local ``next`` path. It creates/changes no project,
    account, schema, or durable preference, and translates no question or output.
    Accepts the shared shell's GET language links and a POST form alike."""
    flask_session["ui_lang"] = ui_text.normalize(request.values.get("lang"))
    nxt = request.values.get("next") or ""
    if not _is_safe_local_path(nxt):
        nxt = url_for("index")
    return redirect(nxt)


def _session_csrf():
    auth = flask_session.get(_AUTH_SESSION_KEY)
    return auth.get("csrf") if auth else None


def _csrf_valid():
    """Constant-time CSRF check for authenticated state-changing POSTs."""
    return _auth.csrf_matches(_session_csrf(), request.form.get("csrf_token", ""))


def _sign_in(account, now):
    """Establish a FRESH authenticated session (session rotation / fixation
    defence): clear any prior session state and mint a new one with a new CSRF
    token. Never carries pre-login cookie state forward."""
    ui_lang = flask_session.get("ui_lang")   # D-P6-18: preserve UI-language choice
    flask_session.clear()
    flask_session[_AUTH_SESSION_KEY] = _auth.build_session(
        account["account_id"], account["session_epoch"], now)
    if ui_lang == "ar":
        flask_session["ui_lang"] = "ar"
    flask_session.permanent = True


# --- P5-3: project ownership & central route authorization --------------------
# The SINGLE server-side authorization decision for every project-scoped route.
# It resolves ownership from DURABLE state (never from the `sid` capability, the
# signed cookie, a template, JavaScript, or any client-provided field) and the
# validated authenticated session, and it FAILS CLOSED.
#
# Model (contract §8/§9): a project that does not exist, or is owned by another
# account, or is owned but accessed anonymously / by a disabled-deleted account,
# is denied GENERICALLY — indistinguishably — so existence and ownership never
# leak. A legacy/anonymous NULL-owner project keeps exactly its prior
# capability-access behaviour (the anonymous journey is preserved).
def _project_authorized(sid):
    """Return True iff the current caller may access project ``sid``. Owned
    projects require the authenticated, active OWNER (server-side account_id ==
    durable owner_account_id); NULL-owner (legacy/anonymous) projects preserve the
    existing sid-capability access; a missing project is denied. Fails closed on
    any error. `sid` possession alone is NEVER treated as ownership."""
    try:
        exists, owner = _get_store().load_owner(sid)
    except Exception:
        return False                       # fail closed
    if not exists:
        # No durable project row. In the real flow every project is durably
        # created at /start BEFORE any live session, so a missing durable row
        # means the sid is unknown → generic denial. The ONLY exception is a live
        # in-memory session with no durable backing (an unowned anonymous/legacy
        # runtime session): it can never be owned (no durable owner exists), so
        # preserving its existing capability access opens no cross-account path.
        return sid in SESSION_STORE
    if owner is None:
        return True                        # legacy/anonymous NULL-owner: preserved
    account = _current_account()           # validates status / epoch / expiry
    if account is None:
        return False                       # owned project, anonymous/invalid session
    return account["account_id"] == owner  # only the durable owner


def _deny_project():
    """One generic, non-enumerating denial for every failed project access
    (missing, non-owner, anonymous-to-owned, disabled/deleted). It is byte-for-byte
    the pre-P5-3 'not available' behaviour (redirect to the home page), so a denial
    never discloses whether the project exists, who owns it, or why access failed.
    It never redirects to /login (which would reveal an owned project exists)."""
    return redirect(url_for("index"))


def _owned_by_current(sid):
    """True only when the current authenticated account is the durable owner of
    ``sid`` — used for the truthful 'saved to your account' surface. Never a
    security decision on its own."""
    try:
        exists, owner = _get_store().load_owner(sid)
    except Exception:
        return False
    if not exists or owner is None:
        return False
    account = _current_account()
    return account is not None and account["account_id"] == owner


def _new_project_owner():
    """The owner_account_id to stamp on a NEW project at /start, or None. Only an
    authenticated, ACTIVE, EMAIL-VERIFIED account owns a new durable project
    (contract §6). Anonymous and unverified users create NULL-owner projects (the
    anonymous journey), with no ownership claimed. Derived ONLY from the validated
    server session — never from client input."""
    account = _current_account()
    if account is None:
        return None
    if account.get("status") == "active" and account.get("email_verified"):
        return account["account_id"]
    return None


def _cold_load_entry(sid):
    """P4-1b-1 durable cold-load: rebuild the MINIMUM runtime entry for `sid`
    from the durable project envelope (the `sid` IS the durable `project_id`).

    Returns the minimal entry, or None on any missing/malformed/unsupported/
    unavailable durable state — the caller then falls through to the existing
    generic unavailable behaviour, disclosing nothing. Readiness is re-derived
    by the render path from the reconstructed ledger; transcript and cached
    last_result are NOT restored as authoritative. No mapping lookup or
    project_ids() scan is used."""
    try:
        contract = _get_store().load_contract(sid)   # scoped by sid==project_id
        state = contract.to_state()
        # CF5-F001 NB-R1 (bounded cold-load identity restoration; corrective
        # contract §4): restore the SAFETY-RELEVANT session-domain identity
        # from the ALREADY-PERSISTED, creation-validated reconstruction inputs
        # (`confirmed_domain`) — and ONLY that. Without it a cold-loaded
        # session diverges from live safety-signal detection (the validated
        # NB-R1 live-vs-cold-load inconsistency). MECHANICALLY-FORCED
        # NARROWING of the contract §4 letter (disclosed for review): the
        # identity is restored onto `domain_signal` ONLY — the safety
        # derivation's `_domain_of` fallback consumes it — while `state.domain`
        # deliberately stays absent, because the committed P4-1b-2a
        # non-resume guard (`submit_answer`: "state.domain is None" = the
        # cold-load marker) anchors the governed fail-closed guarantee that a
        # cold-loaded session cannot be answered (complete resume = P4-2, out
        # of scope). Restoring `state.domain` would silently re-enable
        # resume-answering across restarts — a governed-boundary violation —
        # and would also alter non-safety surfaces (question display). This
        # narrowing is a strict subset of the mandated restoration and the
        # smallest change that fixes NB-R1 while preserving every committed
        # boundary. Legacy/partial envelopes (NULL reconstruction columns)
        # restore nothing and keep the prior behavior (fail-safe; no
        # migration; no schema change; identity restoration is not admission
        # and implies no activation). `path` and broader cold-load fidelity
        # remain governed by the P4 lanes.
        try:
            inputs = _get_store().load_reconstruction_inputs(sid)
        except Exception:
            inputs = None
        restored_domain = (inputs or {}).get("confirmed_domain")
        if restored_domain:
            state.domain_signal = restored_domain
    except Exception:
        # Fail closed. Storage/contract errors are translated to the generic
        # unavailable behaviour at this web boundary; no user content is logged.
        return None
    return {"state": state, "last_result": None, "transcript": []}


# Production fail-fast (mirrors the R16 secret-key policy): in explicit
# production mode the durable store must be constructable at startup — a missing
# or unusable INVENTORAI_DB_PATH makes the app refuse to start rather than
# silently degrade per request. Local/development stays lazy so tests and dev
# runs are unaffected (no eager database file is created outside production).
if _is_production():
    _get_store()

# --- Increment 1A: structured owner actions (conformance correction) ---------
# Non-specialist owners respond through explicit, structured actions instead of
# being forced to invent technical prose. ONLY `answered` enters the existing
# assessment path (run_iteration -> assess/integrate/transition); its behavior
# and the ILT-002 transcript record are unchanged. The five non-answer actions
# still never assess, score, close or alter a gap, advance maturity, satisfy a
# transition gate, or create an evidence record, and the SESSION_STORE entry
# keeps its additive in-memory display metadata.
#
# --- Increment 2: durable, truthful disposition records -----------------------
# In addition (Increment 2 truthful-state correction), every owner action now
# also appends a durable in-memory record to the IdeaState interaction ledger
# (state.record_interaction). This ledger is NOT progression state: it does not
# assess, score, advance maturity, alter the gap lifecycle, satisfy a gate, or
# create Evidence; it carries the truthful provenance/validation/disposition of
# what the owner did. It remains persistence-independent — no durable persistence
# is used, the transcript schema is untouched, and the frozen engine.session_store
# is never imported.
ACTION_ANSWERED = "answered"
INTERACTION_ACTIONS = {
    ACTION_ANSWERED,
    "unknown",
    "deferred",
    "provisional_assumption",
    "specialist_requested",
    "evidence_requested",
}
# Honest, non-progress acknowledgements for the five non-answer actions. None of
# these implies the question is resolved, verified, or answered.
_NON_ANSWER_ACK = {
    "unknown": "Recorded that you do not know this yet. It is kept as an open unknown and does not resolve the question.",
    "deferred": "Recorded as deferred. The question remains open and unresolved.",
    "provisional_assumption": "Recorded as a provisional assumption (not verified). It does not resolve the question or count as evidence.",
    "specialist_requested": "Recorded that specialist input is needed. No technical answer has been assumed.",
    "evidence_requested": "Recorded that evidence is needed. No evidence or result has been recorded.",
}
# G-UX-ANSWER-VALIDATION: shown only when the owner chooses to answer but submits
# a whitespace-normalized empty response. Position-neutral; echoes no user content.
ANSWER_REQUIRED_MESSAGE = "Enter an answer, or choose one of the response options below."
# P4-1b-2a: generic, non-disclosing transient shown when an answered submission
# cannot be durably accepted (missing/invalid token, a same-token/different-content
# reuse, or an unavailable durable append). It reveals nothing about the token
# mechanism, the durable store, or any user content — fail closed, then retry.
ANSWER_NOT_SAVED_MESSAGE = "That answer could not be saved just now. Please try again."
# PVCG-R1: the durable-failure message for the five NON-ANSWER actions. It is a
# separate string because calling "I don't know" / "defer" an *answer* would
# misdescribe what the owner actually did; the answered message above is
# unchanged. Registered in `ui_text._MESSAGE_KEYS` so it localises like its
# answered counterpart.
INTERACTION_NOT_SAVED_MESSAGE = (
    "That response could not be saved just now. Please try again.")
# G-UX-SNAPSHOT-DECISION: truthful, temporary-session acknowledgement for the
# "Keep current snapshot" post-output decision. It selects the CURRENT deterministic
# working snapshot for this temporary session only — it does not serialize, duplicate,
# version, persist, approve, or create ownership. Echoes no idea/snapshot content.
# --- PVCG-R4 explicit correction / withdrawal (PVCG_R4_C ... CONTRACT.md) -----
# Storage stays English; display localises through `ui_text.localize_message`
# (registered as UI_B_CORRECT_001/002/003), so the path is EN/AR equivalent.
CORRECTION_NOT_APPLIED_MESSAGE = (
    "That correction could not be applied just now. Nothing was changed."
)
CORRECTION_INCOMPLETE_MESSAGE = (
    "Select which of your earlier answers to withdraw, and enter the "
    "corrected answer."
)
# NB-1 (Independent External Review). The durable append happens BEFORE the
# replay (the contract's persist-before-acknowledge ordering, §6 C-6), so once
# the append has committed, "Nothing was changed" is FALSE: accepted-source
# history DID change. This message is used ONLY on that post-durable path. It
# claims no rollback of the durable append — the append stands, and the next
# successful load applies it through reconstruction (§9 F-4).
CORRECTION_SAVED_NOT_YET_APPLIED_MESSAGE = (
    "Your correction was saved, but the page could not be updated just now. "
    "What you see below has not changed yet. The saved correction will be "
    "reflected whenever this project can be rebuilt successfully."
)

CORRECTION_APPLIED_ACK = (
    "Your earlier answer was withdrawn and kept in the project history. "
    "Everything shown has been recomputed from your remaining answers."
)

# RVR-1 (Wave-1): explicit accepted-risk acknowledgement / failure messages.
# Same catalogue conventions as the other acks (canonical English constant,
# Arabic via the ui_text presentation map); truthful: accepted != resolved.
RISK_ACCEPTED_ACK = (
    "Recorded as an accepted risk. This gap is explicitly accepted by you as "
    "a known, unresolved risk - it is NOT resolved and NOT validated, and it "
    "stays visible in your assessment.")
RISK_NOT_ACCEPTED_MESSAGE = (
    "The risk acceptance was not recorded. Nothing was changed - please "
    "review the question and try again.")

KEEP_SNAPSHOT_ACK = (
    "Current working snapshot selected for this temporary session. "
    "It has not been permanently saved or approved."
)

# --- Workstream 4: structured criticality confirmation flow -------------------
# (docs/governance/STRUCTURED_CRITICALITY_CAPTURE_INCREMENT_CONTRACT.md §7;
# owner GREEN authorization.) A lightweight, summary-first step on the existing
# completion-stage session surface — no new route. One contextually supported
# requirement at a time (grouped confirmation is NOT implemented, per the
# owner's deliberate minimum-risk restriction). The server re-derives the
# current focus from authoritative session state on every request and never
# trusts a browser-supplied target: stale, mismatched, or manipulated
# submissions are rejected with NOTHING stored. All inventor-facing wording is
# plain language — no raw category, authority, provenance, or requirement-id
# token ever renders.
import hashlib as _crit_hashlib

CRITICALITY_SUMMARY_LEAD = "This is what I understood from your explanation:"
CRITICALITY_CLARIFICATION = (
    "Would the idea still achieve its purpose if this part changed?")
# Exact owner-mandated plain-language choices and their internal mapping. The
# mapping happens server-side only; the raw category never reaches the page.
CRITICALITY_CHOICES = (
    ("essential",  "The idea may not work without this"),
    ("value",      "The idea would still work, but this adds important value"),
    ("refinement", "This mainly improves or refines the idea"),
    ("unsure",     "I am not sure yet"),
)
_CRITICALITY_CHOICE_CATEGORY = {
    "essential":  CRITICALITY_FEASIBILITY_THREATENING,
    "value":      CRITICALITY_VALUE_ENHANCING,
    "refinement": CRITICALITY_REFINEMENT,
}
# Exact owner-mandated five lightweight actions (contract §7.2).
CRITICALITY_SUMMARY_ACTIONS = (
    ("summary_correct", "Yes, that is correct"),
    ("summary_change",  "Change this part"),
    ("summary_missing", "Something is missing"),
    ("summary_unsure",  "I am not sure yet"),
    ("summary_later",   "Decide later"),
)
_CRITICALITY_SUMMARY_VALUES = {v for v, _ in CRITICALITY_SUMMARY_ACTIONS}


def _criticality_focus(state):
    """The single current focus: the first landscape requirement, in the
    stable derivation order, that (a) has understanding context — its primary
    anchor is an inventor ledger record with verbatim content — and (b) has
    no recorded confirmation/deferral yet. Requirements without understanding
    context are never offered for classification (contract §7.1): they keep
    the untouched never-interacted default."""
    landscape = derive_requirement_landscape(state)
    for req in landscape.requirements:
        if state.current_criticality_confirmation(req.requirement_id):
            continue
        if req.primary_anchor.anchor_kind != "assertion":
            continue
        record = next(
            (a for a in state.assertions
             if a.record_id == req.primary_anchor.anchor_reference), None)
        if record is not None and (record.content or "").strip():
            return req, record
    return None, None


def _criticality_focus_token(sid, requirement_id):
    """Opaque per-focus token: lets the server detect a submission rendered
    against a different (stale) focus without ever exposing the raw
    requirement id in the page."""
    digest = _crit_hashlib.sha256(
        ("ws4:" + sid + ":" + requirement_id).encode("utf-8")).hexdigest()
    return digest[:16]


# --- P4-1b-2a: answered-submission token + SEPARATE durable idempotency identity
# (G-P4-1B-2A-B3-CONTRACT-AMENDMENT-01, OPTION A). The token is a server-issued,
# sid-signed, unpredictable value carried by a hidden field on every
# answered-producing form. The durable idempotency identity is a SEPARATE
# HMAC-SHA-256(secret, sid || token) truncated to >= 128 bits — it is stored in
# engine.record_store and is NEVER the engine record_id (which stays rec_N).
import hmac as _p2a_hmac
import hashlib as _p2a_hashlib

_ANSWER_TOKEN_SEP = "."
_ANSWER_TOKEN_NONCE_BYTES = 24
# 32 hex chars of SHA-256 output == 128 bits (owner constraint: truncation >= 128b).
_ANSWER_HMAC_HEX_LEN = 32


def _canonical_message(*fields):
    """Unambiguous, length-prefixed canonical encoding of ordered fields: each
    field is emitted as its UTF-8 byte-length (decimal ASCII) + ':' + its UTF-8
    bytes. Because every field carries its own explicit length, no field content
    (including a separator byte, empty string, or a value equal to another
    field's boundary) can ever be mistaken for a field boundary. Field VALUES are
    passed through verbatim — this encoding wraps them, it does not normalise
    them (accepted-response case/punctuation/whitespace/line-breaks preserved)."""
    out = b""
    for f in fields:
        fb = ("" if f is None else str(f)).encode("utf-8")
        out += str(len(fb)).encode("ascii") + b":" + fb
    return out


def _answer_secret():
    """The existing approved environment secret (INVENTORAI_SECRET_KEY, resolved
    into app.secret_key). No new secret is minted here."""
    key = app.secret_key
    return key.encode("utf-8") if isinstance(key, str) else key


def _answer_token_sig(sid, nonce):
    msg = _canonical_message("p4-1b2a-answer-token", sid, nonce)
    return _p2a_hmac.new(_answer_secret(), msg,
                         _p2a_hashlib.sha256).hexdigest()[:_ANSWER_HMAC_HEX_LEN]


def _issue_answer_token(sid):
    """A fresh, unpredictable, sid-signed answered-submission token."""
    nonce = secrets.token_urlsafe(_ANSWER_TOKEN_NONCE_BYTES)
    return nonce + _ANSWER_TOKEN_SEP + _answer_token_sig(sid, nonce)


def _answer_token_for(sid, entry):
    """Return the entry's current answered-submission token, issuing and storing
    one when absent. The token is RETAINED across renders (and across a
    validation-error re-render) until an accepted answer consumes it, then it is
    rotated; this realises the owner's single-use-for-acceptance lifecycle."""
    tok = entry.get("answer_token")
    if not tok:
        tok = _issue_answer_token(sid)
        entry["answer_token"] = tok
    return tok


def _valid_answer_token(sid, token):
    """Verify a submitted token is server-issued FOR THIS sid (stateless). Fails
    closed on missing, malformed, forged, cross-session, or cross-project
    tokens — the signature binds sid, so a token minted for another session does
    not verify here."""
    if not token or _ANSWER_TOKEN_SEP not in token:
        return False
    nonce, _, sig = token.partition(_ANSWER_TOKEN_SEP)
    if not nonce or not sig:
        return False
    return _p2a_hmac.compare_digest(sig, _answer_token_sig(sid, nonce))


def _answer_idempotency_key(sid, token):
    """The SEPARATE durable idempotency identity: HMAC-SHA-256(secret, sid ||
    token) truncated to >= 128 bits. Project-bound; token-derived; one-way (the
    raw token is not stored). This is NOT the engine record_id."""
    msg = _canonical_message(sid, token)
    return _p2a_hmac.new(_answer_secret(), msg,
                         _p2a_hashlib.sha256).hexdigest()[:_ANSWER_HMAC_HEX_LEN]


def _interaction_idempotency_key(sid, action, gap_context, iteration, content):
    """PVCG-R1: the durable idempotency identity of ONE accepted NON-ANSWER
    interaction — HMAC-SHA-256(secret, canonical(sid, action, gap_context,
    iteration, content)) truncated to the same >= 128 bits as the answered key.

    It reuses the answered path's construction (`_canonical_message` +
    `_answer_secret`) with its own domain-separator label, and is stored in the
    SAME additive `idempotency_key` column under the SAME partial UNIQUE index.
    It is NOT the engine `record_id` (which stays `rec_N`).

    Why the event fields rather than the answered token: the answered token is
    RETAINED across renders until an accepted answer consumes it, so two
    genuinely DIFFERENT non-answer actions would share one token and collide.
    A non-answer action never advances `state.iteration`, so a refresh, retry,
    or double-submit reproduces all five fields exactly and is recognised as the
    same event, while a different action / gap / text yields a different key."""
    msg = _canonical_message("pvcg-r1-interaction", sid, action,
                             gap_context or "", str(iteration), content or "")
    return _p2a_hmac.new(_answer_secret(), msg,
                         _p2a_hashlib.sha256).hexdigest()[:_ANSWER_HMAC_HEX_LEN]


def _answer_fingerprint(sid, target_step, action, accepted_response):
    """SHA-256 over the length-prefixed canonical encoding of
    (sid, target_step, resolved_action, exact_accepted_response). The response
    component is the EXACT value accepted and passed to record_interaction
    (post-validation); the canonical encoding wraps it without any whitespace
    collapsing or meaning-changing normalisation, and its length-prefixing makes
    the four field boundaries unambiguous for any field contents."""
    msg = _canonical_message(sid, target_step or "", action, accepted_response)
    return _p2a_hashlib.sha256(msg).hexdigest()


def _payload_answer_fingerprint(sid, payload):
    """Recompute the fingerprint from a STORED record payload (confirm-by-reload,
    C3): binds the same fields from the durable record so a same-token retry with
    identical accepted content is recognised without ever auto-classifying an
    IntegrityError as a duplicate."""
    return _answer_fingerprint(sid, payload.get("gap_context"),
                               payload.get("disposition") or "",
                               payload.get("content") or "")


def _criticality_step_context(entry, state, sid):
    """Read-only render context for the completion-stage block, or None when
    the step does not apply (journey not complete, or no contextually
    supported unconfirmed requirement remains). Mutates nothing."""
    if state.maturity_level < 2 or state.get_open_gaps():
        return None
    if entry.get("criticality_correction"):
        return {"stage": "correction"}
    req, record = _criticality_focus(state)
    if req is None:
        return None
    stage_state = entry.get("criticality_stage") or {}
    stage = ("clarify"
             if stage_state.get("requirement_id") == req.requirement_id
             else "summary")
    return {
        "stage": stage,
        "summary_lead": CRITICALITY_SUMMARY_LEAD,
        "statement": req.statement,
        "you_said": record.content,
        "clarification": CRITICALITY_CLARIFICATION,
        "choices": CRITICALITY_CHOICES,
        "summary_actions": CRITICALITY_SUMMARY_ACTIONS,
        "proposed_rationale": record.content,
        "focus_token": _criticality_focus_token(sid, req.requirement_id),
    }


def _handle_criticality_action(entry, state, sid):
    """POST branch for the structured criticality actions. Never calls
    run_iteration; never touches gaps, maturity, the ledger, the transcript,
    scoring, or any unrelated state. Every rejection returns HTTP 400 with
    NOTHING stored."""
    def _reject():
        return ("This confirmation step is no longer current. "
                "No change was made.", 400)

    crit_action = (request.form.get("criticality_action") or "").strip()
    # Server-side focus protection (owner rule 5): re-derive the authoritative
    # focus and require the rendered token to match it.
    req, record = _criticality_focus(state)
    if req is None:
        return _reject()
    if request.form.get("focus_token", "") != \
            _criticality_focus_token(sid, req.requirement_id):
        return _reject()

    if crit_action in _CRITICALITY_SUMMARY_VALUES:
        entry.pop("criticality_stage", None)
        if crit_action == "summary_correct":
            # Understanding confirmed — advance to the single clarification.
            # No criticality is stored by this action (no silent adoption).
            entry["criticality_stage"] = {"requirement_id": req.requirement_id}
        elif crit_action in ("summary_unsure", "summary_later"):
            state.record_criticality_confirmation(
                requirement_id=req.requirement_id,
                action=CRITICALITY_ACTION_DEFERRED,
                iteration=state.iteration)
        else:
            # Change this part / Something is missing: store nothing; return
            # the inventor to the existing free-text answer path (owner rule 6).
            entry["criticality_correction"] = True
        return redirect(url_for("show_session", sid=sid))

    if crit_action == "clarify_choice":
        if (entry.get("criticality_stage") or {}).get("requirement_id") \
                != req.requirement_id:
            return _reject()
        choice = (request.form.get("category_choice") or "").strip()
        if choice == "unsure":
            entry.pop("criticality_stage", None)
            state.record_criticality_confirmation(
                requirement_id=req.requirement_id,
                action=CRITICALITY_ACTION_DEFERRED,
                iteration=state.iteration)
            return redirect(url_for("show_session", sid=sid))
        category = _CRITICALITY_CHOICE_CATEGORY.get(choice)
        rationale = request.form.get("rationale", "")
        if category is None or not rationale.strip():
            return _reject()
        source = ("reused_statement:" + record.record_id
                  if rationale == record.content else "inventor_edited")
        try:
            state.record_criticality_confirmation(
                requirement_id=req.requirement_id,
                action=CRITICALITY_ACTION_CONFIRMED, category=category,
                rationale_verbatim=rationale, rationale_source=source,
                iteration=state.iteration)
        except ValueError:
            return _reject()
        entry.pop("criticality_stage", None)
        return redirect(url_for("show_session", sid=sid))

    return _reject()

# Option B product-boundary enforcement (DOMAIN_SCOPE_OWNER_RESOLUTION_OPTION_B).
# Historical electronics-only refusal copy — served EXACTLY (byte-identical) while
# `['electronics_electrical']` is the whole activation set; under any broadened
# activation set the truthful activation-derived copy is composed instead
# (CF5-F002 §4.E — bounded CF-2 facet only; CF-2 is NOT closed here).
UNSUPPORTED_DOMAIN_MESSAGE = (
    "InventorAI currently supports electronics and electrical ideas only. "
    "Please describe an electronics or electrical invention."
)

# Explicit domain confirmation at the generic product boundary (ADR-001: "Domain
# assignment is explicit or it does not occur"; Owner decision D-CF5-F002-01 D1).
# The user must affirmatively confirm the domain; consent is never inferred from
# the idea text. Since CF5-F002 the confirm control's value is DERIVED from the
# canonical activation set / classifier (no hardcoded constant on the /start
# path); whether the confirmed domain is admitted to specialist RUNTIME remains
# decided solely by the canonical engine activation policy
# (see `_admit_specialist_domain`). DOMAIN_CONFIRM_VALUE survives ONLY as the
# historical electronics consent value for legacy consumers (ILT-002 fixed-domain
# routes / existing tests); POST /start no longer reads it.
DOMAIN_CONFIRM_VALUE = "electronics_electrical"
CONFIRMATION_REQUIRED_MESSAGE = (
    "Please confirm that your idea is an electronics or electrical idea "
    "before starting."
)
# Historical bounded conflict set (electronics-only activation state). Kept for
# legacy consumers; the /start path now derives the equivalent membership test
# from the canonical recognition + activation seams
# (`_is_recognized_not_activated`), which equals this constant's membership
# under `['electronics_electrical']`.
CONFLICTING_SUPPORTED_DOMAINS = {"mechanical", "medical_device", "software"}


def _activated_specialist_domains():
    """CF5-F002 (D3): the canonical activated specialist-domain set for the
    /start admission surface — read at request time from the §5-I2 activation
    policy (`engine.domain_activation.activated_domains()`), never cached and
    never hardcoded, so admission behavior always derives from the activation
    set with no Electronics special case."""
    return domain_activation.activated_domains()


def _domain_label(domain):
    """Human-readable presentation label for a specialist domain, derived
    deterministically from the domain id (domain-neutral; no fixed list; no
    direct registry access from the web layer — the frozen architecture
    boundary). Presentation only: labels never affect classification,
    activation, admission, or the persisted session-domain."""
    return domain.replace("_", " ").title()


def _is_recognized_not_activated(domain, activated):
    """True when ``domain`` is registry-recognized (via the canonical
    `engine.domain_rules.is_known_domain` seam) but NOT currently activated —
    the activation-derived generalization of the historical electronics-only
    CONFLICTING_SUPPORTED_DOMAINS membership test (equivalent to it under
    `['electronics_electrical']`). Recognition never grants admission (§5-I2)."""
    return is_known_domain(domain) and domain not in set(activated)


def _supported_domains_phrase(activated):
    """Truthful natural-language enumeration of the activated domains."""
    labels = [_domain_label(d) for d in activated]
    if len(labels) == 1:
        return labels[0]
    return ", ".join(labels[:-1]) + " or " + labels[-1]


def _unsupported_domain_message(activated, lang="en"):
    """Activation-derived refusal copy (§4.E). Byte-identical to the historical
    electronics-only message under `['electronics_electrical']`; truthful
    (never "electronics only") under any broadened activation set.

    CF-2 Arabic-localization remainder: `lang="en"` (the default) preserves
    this function's EXACT prior behavior byte-for-byte — no caller that
    omits `lang` observes any change. Arabic uses fixed catalogue copy: the
    electronics-only and empty-activation branches translate the real EN
    state; the broadened (2+) branch is deliberately domain-neutral (no
    Tier-1 label translation invented here — out of scope; see
    `docs/governance/CF2_CLI_REMAINDER_TRUTHFULNESS_CONTRACT.md` §4 boundary,
    reused for this facet)."""
    if ui_text.normalize(lang) == "ar":
        if activated == ["electronics_electrical"]:
            return ui_text.text("UI_B_START_010", lang)
        if not activated:
            return ui_text.text("UI_B_START_020", lang)
        return ui_text.text("UI_B_START_021", lang)
    if activated == ["electronics_electrical"]:
        return UNSUPPORTED_DOMAIN_MESSAGE
    if not activated:
        return ("InventorAI has no specialist domain available right now. "
                "Please try again later.")
    return (
        "InventorAI currently supports " + _supported_domains_phrase(activated)
        + " ideas only. Please describe an invention in a supported domain."
    )


def _confirmation_required_message(domain, lang="en"):
    """Consent-required copy for the sole-activated-domain one-step form.
    Byte-identical to the historical message for electronics.

    CF-2 Arabic-localization remainder: see `_unsupported_domain_message`
    docstring for the `lang` contract (default-`en` byte-identity; Arabic
    domain-neutral for any non-electronics sole domain)."""
    if ui_text.normalize(lang) == "ar":
        if domain == "electronics_electrical":
            return ui_text.text("UI_B_START_011", lang)
        return ui_text.text("UI_B_START_022", lang)
    if domain == "electronics_electrical":
        return CONFIRMATION_REQUIRED_MESSAGE
    return ("Please confirm that your idea is a " + _domain_label(domain)
            + " idea before starting.")


def _present_confirm_message(domain, lang="en"):
    """D1/U1: prompt shown when the classifier-selected (or explicitly chosen)
    ACTIVATED domain is presented for explicit confirm/decline.

    CF-2 Arabic-localization remainder: see `_unsupported_domain_message`
    docstring for the `lang` contract (default-`en` byte-identity; Arabic
    domain-neutral for any non-electronics domain)."""
    if ui_text.normalize(lang) == "ar":
        if domain == "electronics_electrical":
            return ui_text.text("UI_B_START_023", lang)
        return ui_text.text("UI_B_START_024", lang)
    return ("Your idea appears to belong to the " + _domain_label(domain)
            + " domain. Please confirm this domain to start, or revise your "
            "description.")


# D2/U2: prompt shown with the explicit activated-domain choice set when the
# classifier resolves NONE and two or more specialist domains are activated.
DOMAIN_CHOICE_MESSAGE = (
    "Your description did not clearly match one supported domain. Please choose "
    "the domain that best fits your idea, then confirm it."
)


class DomainNotActivatedError(RuntimeError):
    """Raised when specialist-runtime admission is attempted for a domain the
    canonical engine activation policy does not currently activate."""


def _admit_specialist_domain(domain):
    """§5-I2 — single source of specialist-activation truth for the web layer.

    Return ``domain`` iff the canonical engine activation policy
    (``engine.domain_activation``) currently activates it; otherwise raise
    ``DomainNotActivatedError``. This binds every specialist-session admission to
    the engine policy so the web layer holds no competing activation decision: a
    recognized-but-not-activated or unknown domain can never gain specialist
    runtime here. Behavior-preserving today — ``electronics_electrical`` is
    activated, so current electronics admission is unchanged.
    """
    if not domain_activation.is_activated(domain):
        raise DomainNotActivatedError(
            f"domain {domain!r} is not activated for specialist runtime"
        )
    return domain

# --- Domain Gate / Entry UX Increment (post-PR #100 Increment Contract) --------
# Bounded ambiguity resolution for the /start domain gate. The problem being
# fixed (see the merged evidence record + Increment Contract §3, §7.C, §10):
# ordinary lay wording can produce spurious WEAK *conflicting-supported-domain*
# classifications (e.g. the generic word "monitoring" -> medical_device) that
# the gate then hard-rejects even though the idea is a genuine electronics/
# electrical one and the owner explicitly confirmed that domain. (Historically
# the classifier also matched signals as raw SUBSTRINGS — e.g. "app" inside
# "appliance" -> software — but since the CF5-F003 corrective the canonical
# classifier matches whole tokens only; that spurious-substring source is gone.)
# This increment lets the explicit confirmation resolve such WEAK/ambiguous
# conflicts, while STRONG unsupported-domain evidence is never overridden. It
# adds NO domain, activates no technology family, changes no classifier/
# registry/domain pack, and makes no safety/feasibility/compliance claim.
# Matching here is word/token based (not substring) precisely so that markers
# like "app" cannot fire inside "appliance" and "medical" cannot fire inside
# "medicine".
_TOKEN_RE = re.compile(r"[a-z0-9]+")

# Strong, unambiguous evidence of a specific NON-ACTIVATED technology family.
# When present, the idea clearly belongs to a domain outside the activation set;
# explicit confirmation must NOT override it (Increment Contract §7.C, §10, §15).
# CF5-F002 / CF-6 facet: each word group is keyed by the registry domain it
# evidences (or None for never-registered families), and a group counts as
# STRONG-UNSUPPORTED only while its domain is NOT in the canonical activation
# set — stale vocabulary can never suppress an ACTIVATED domain. Under the
# current activation state `['electronics_electrical']` every group below is
# active, i.e. behavior is unchanged. Matched against word tokens. Words that
# ALSO carry ordinary electronics meanings are deliberately EXCLUDED so valid
# electronics ideas are not rejected (independent-review boundary fix): NOT
# "pulse" (pulse circuits/signals), NOT "algorithm" (embedded/electronics
# control wording), NOT "diagnostic"/"diagnostics" (electronics
# self-diagnostics) — only the medical noun/verb forms
# diagnosis/diagnose/diagnoses/diagnosing are strong.
_STRONG_UNSUPPORTED_WORD_FAMILIES = {
    # medical_device / health (note: NOT "monitoring" — that is a weak/ambiguous
    # term per §10 — and NOT "medicine")
    "medical_device": frozenset({
        "medical", "cardiac", "heart", "blood", "insulin", "glucose",
        "clinical", "surgical", "surgery", "implant", "implantable",
        "prosthetic", "catheter", "stent", "biosensor", "patient", "dementia",
        "therapeutic", "respiratory", "neural", "retinal", "orthopedic",
        "diagnosis", "diagnose", "diagnoses", "diagnosing",
        "hearing", "wearable", "fever", "rehabilitation",
    }),
    "mechanical": frozenset({
        "mechanical", "gear", "gearbox", "gearing", "shaft", "bearing",
        "torque", "piston", "pulley", "hydraulic", "crankshaft", "camshaft",
    }),
    "software": frozenset({
        "software", "api", "backend", "frontend", "database", "sql",
    }),
    # drone / solar / robotics / agriculture (never-registered families, §6/§15):
    # not resolvable to any registry domain, so they can never become activated
    # and always remain strong-unsupported.
    None: frozenset({
        "drone", "solar", "crop", "crops", "agriculture", "agricultural",
        "pesticide", "herbicide", "irrigation", "farm", "farms",
        "robot", "robots", "robotic", "robotics",
    }),
}
# Strong multi-word markers; matched as substrings of the full text, keyed by
# the registry domain they evidence (same activation-awareness as above).
_STRONG_UNSUPPORTED_SUBSTRING_FAMILIES = (
    ("machine learning", "software"),
    ("neural network", "software"),
    ("body temperature", "medical_device"),
)
# Legacy flat views (exact same members as before the CF5-F002 partition) for
# existing consumers/tests that inspect the vocabulary as a whole.
_STRONG_UNSUPPORTED_WORDS = frozenset().union(
    *_STRONG_UNSUPPORTED_WORD_FAMILIES.values())
_STRONG_UNSUPPORTED_SUBSTRINGS = tuple(
    s for s, _family in _STRONG_UNSUPPORTED_SUBSTRING_FAMILIES)

# Lay household-electrical MECHANISM evidence. Presence indicates a genuine
# electrical mechanism written in non-specialist words, so the idea is admitted
# under the explicit confirmation even if the deterministic classifier missed it
# or returned a weak conflicting supported domain (Increment Contract §7.B).
# Deliberately EXCLUDES bare "appliance"/"alert"/"device" (which carry no
# electrical mechanism on their own — see §9.B, which must NOT be admitted).
# "power"/"powers" are matched ONLY as whole word tokens (independent-review
# boundary fix): the previous "power" SUBSTRING marker fired inside unrelated
# words such as "powerful", "empowers", and "hand-powered", falsely admitting
# software-only and mechanical-only ideas. "powered" is deliberately NOT a
# marker because it frequently names a non-electrical energy source
# ("hand-powered", "spring-powered") and carries no electrical mechanism alone.
_LAY_ELECTRICAL_WORDS = frozenset({
    "plug", "socket", "outlet", "switch", "circuit", "wire", "wiring",
    "voltage", "sensor", "sensors", "charger", "chargers", "battery",
    "batteries", "relay", "electric", "electrical", "electronic",
    "electronics", "electricity", "current", "currents", "transistor",
    "microcontroller", "arduino", "esp32", "led", "wifi", "bluetooth",
    "power", "powers",
})

# Bounded medical-conflict corroboration bar (independent-review boundary fix):
# when the unchanged deterministic classifier returns `medical_device`, ONE lay
# electrical token must not flip the conflict toward electronics/electrical
# (Increment Contract §7.C: confirmation helps resolve ambiguity but is not an
# unconditional override). At least TWO distinct lay electrical mechanism words
# are required; otherwise the owner is guided to name the mechanism instead.
_MEDICAL_CONFLICT_LAY_MINIMUM = 2

# User-facing guidance shown when an idea does not yet clearly show an electrical
# mechanism (Increment Contract §7.E). Advisory only: it makes NO validation,
# safety, feasibility, compliance, or build-readiness claim, and does NOT admit
# the idea (no session is created).
MECHANISM_GUIDANCE_MESSAGE = (
    "InventorAI currently supports electronics and electrical ideas only. Your "
    "description does not yet clearly show the electrical mechanism. Try adding a "
    "simple phrase describing how it works electrically — for example that it uses "
    "a sensor, current, switch, circuit, power, plug, or microcontroller."
)


def _has_strong_unsupported_evidence(lowered_text: str, activated=None) -> bool:
    """True when the text carries clear, unambiguous evidence of a technology
    family whose domain is NOT currently activated (CF5-F002 / CF-6 facet: a
    vocabulary group is skipped once its domain is in the canonical activation
    set, so stale vocabulary never suppresses an ACTIVATED domain). With the
    current activation state `['electronics_electrical']` every group counts,
    i.e. behavior is exactly the historical one.

    Word/token based so short markers never fire inside unrelated words (e.g.
    "app" inside "appliance", "medical" inside "medicine"). Read-only; no state.
    ``activated`` may be the already-derived activated-domain collection; when
    omitted it is read from the canonical activation policy.
    """
    if activated is None:
        activated = _activated_specialist_domains()
    activated_set = set(activated)
    tokens = set(_TOKEN_RE.findall(lowered_text))
    for family, words in _STRONG_UNSUPPORTED_WORD_FAMILIES.items():
        if family is not None and family in activated_set:
            continue
        if tokens & words:
            return True
    for substring, family in _STRONG_UNSUPPORTED_SUBSTRING_FAMILIES:
        if family is not None and family in activated_set:
            continue
        if substring in lowered_text:
            return True
    return False


def _lay_electrical_evidence_count(lowered_text: str) -> int:
    """Number of DISTINCT lay household-electrical MECHANISM words in the text.

    Word/token based only (no substrings) so markers never fire inside
    unrelated words ("power" inside "powerful"/"empowers"). Read-only.
    """
    tokens = set(_TOKEN_RE.findall(lowered_text))
    return len(tokens & _LAY_ELECTRICAL_WORDS)

def _render_start_page(error=None, status=None, present_domain=None,
                       choice_domains=None, carry_idea=None, carried_choice=None):
    """CF5-F002 (Amendment 01 §14.1): single renderer for the /start admission
    surface (`index.html`). Supplies the activation-derived consent context so
    the rendered consent control always presents/carries a domain from the
    canonical activation set — never a hardcoded constant. Rendering modes:

      * default             — the start form; with exactly ONE activated domain
                              it carries that sole domain's explicit-consent
                              checkbox (behaviorally identical to the historical
                              electronics page under `['electronics_electrical']`,
                              U4); with >= 2 activated domains consent is
                              collected after classification (two-step seam).
      * present_domain      — D1/U1: present the classifier-selected (or D2
                              chosen) ACTIVATED domain for explicit
                              confirm/decline; `carried_choice` re-carries a D2
                              choice through the confirm submission.
      * choice_domains      — D2/U2: present ONLY the currently activated
                              specialist domains as an explicit choice set.

    Presentation only: no session, no admission, no persistence.
    """
    activated = _activated_specialist_domains()
    sole = activated[0] if len(activated) == 1 else None
    is_elec_only = (activated == ["electronics_electrical"])
    labels = {d: _domain_label(d) for d in activated}
    if present_domain is not None and present_domain not in labels:
        labels[present_domain] = _domain_label(present_domain)
    # CF-2 Arabic-localization remainder: computed once, reused for every
    # generalized-context string below (`start_scope_sentence`,
    # `start_placeholder`, `start_supported_note`, `start_confirm_label`,
    # `start_present_confirm_label`, `start_choice_prompt`) — these six
    # previously bypassed localization entirely (always raw English). English
    # output below is UNCHANGED (byte-identical); Arabic uses fixed catalogue
    # copy, domain-neutral wherever the underlying content would otherwise
    # require translating a non-electronics domain name (out of scope — see
    # `_unsupported_domain_message`).
    lang = _current_ui_lang()
    is_ar = ui_text.normalize(lang) == "ar"
    generalized = None
    if not is_elec_only:
        phrase = _supported_domains_phrase(activated) if activated else None
        if is_ar:
            generalized = {
                "start_scope_sentence": (
                    ui_text.text("UI_B_START_026", lang) if phrase else
                    ui_text.text("UI_B_START_025", lang)),
                "start_placeholder": ui_text.text("UI_B_START_027", lang),
                "start_supported_note": (
                    ui_text.text("UI_B_START_029", lang) if phrase else
                    ui_text.text("UI_B_START_028", lang)),
                "start_confirm_label": (
                    ui_text.text("UI_B_START_030", lang)
                    if sole is not None else None),
            }
        else:
            generalized = {
                "start_scope_sentence": (
                    (phrase + " ideas are currently supported. Before starting, "
                     "please confirm the domain your idea belongs to.")
                    if phrase else
                    "No specialist domain is currently available."),
                "start_placeholder": "Describe your invention...",
                "start_supported_note": (
                    ("Currently supported: " + phrase + " ideas.")
                    if phrase else "Currently supported: none."),
                "start_confirm_label": (
                    ("I confirm that this idea is primarily a "
                     + labels[sole] + " idea.") if sole is not None else None),
            }
    if present_domain is None:
        present_confirm_label = None
    elif is_ar:
        present_confirm_label = ui_text.text(
            "UI_B_START_023" if present_domain == "electronics_electrical"
            else "UI_B_START_024", lang)
    else:
        present_confirm_label = ("I confirm that my idea belongs to the "
                                  + labels[present_domain] + " domain.")
    choice_prompt = (
        (ui_text.text("UI_B_START_031", lang) if is_ar
         else "Choose your idea's domain:")
        if choice_domains else None)
    rendered = render_template(
        "index.html", error=error,
        start_sole_domain=sole,
        start_is_electronics_only=is_elec_only,
        start_domain_labels=labels,
        start_present_domain=present_domain,
        start_present_confirm_label=present_confirm_label,
        start_choice_domains=choice_domains,
        start_choice_prompt=choice_prompt,
        start_carry_idea=carry_idea,
        start_carried_choice=carried_choice,
        **(generalized or {}))
    return rendered if status is None else (rendered, status)


@app.route("/health", methods=["GET"])
def health():
    """P10-OB1 — the single minimal health/readiness surface. Deterministic,
    machine-readable, unauthenticated, session-free, side-effect-free, and
    data-minimized: exactly two bounded enum fields, no user data, no secrets,
    no filesystem/database details, no versions, no stack traces. 200 while
    the local runtime dependencies are usable (or simply not yet lazily
    initialized); 503 only on a real local dependency failure. Local health
    is NOT production/deployment readiness and is no authorization signal."""
    db_state = _database_health()
    body = {"status": "ok" if db_state != "error" else "unavailable",
            "database": db_state}
    return app.response_class(
        response=json.dumps(body, sort_keys=True),
        status=200 if db_state != "error" else 503,
        mimetype="application/json")


@app.route("/", methods=["GET"])
def index():
    return _render_start_page()


# --- P5-1: account registration (foundation only; NO login/session/ownership) --
def _register_generic_response(form_error=None, status=200):
    """Render the registration page with the single generic, non-enumerating
    acknowledgement (or a format-validation error, which is safe to show because
    it concerns the submitted input, not whether an account exists)."""
    return render_template(
        "register.html",
        generic_message_en=REGISTER_GENERIC_MESSAGE_EN,
        generic_message_ar=REGISTER_GENERIC_MESSAGE_AR,
        submitted=(form_error is None and status == 200),
        form_error=form_error,
    ), status


@app.route("/register", methods=["GET"])
def register_form():
    return render_template(
        "register.html",
        generic_message_en=REGISTER_GENERIC_MESSAGE_EN,
        generic_message_ar=REGISTER_GENERIC_MESSAGE_AR,
        submitted=False, form_error=None)


@app.route("/register", methods=["POST"])
def register_submit():
    """Minimum P5-1 registration. Validates + normalizes + hashes, creates the
    account atomically, issues a verification token (hash stored; raw token only
    in the dev email sink), and returns ONE generic non-enumerating response.
    Never signs the user in, never creates a project. Format/length/mismatch
    errors ARE shown (they concern the input, not account existence); account
    existence / disabled / deleted states are never revealed."""
    email_raw = request.form.get("email", "")
    password = request.form.get("password", "")
    password_confirm = request.form.get("password_confirm", "")

    email_normalized = _acct.normalize_email(email_raw)

    # Input-format validation (safe to surface — not account-state-sensitive).
    if not _acct.is_valid_email(email_normalized):
        return _register_generic_response(form_error="email_invalid", status=400)
    ok, _reason = _acct.validate_password(password)
    if not ok:
        return _register_generic_response(form_error="password_invalid", status=400)
    if password != password_confirm:
        return _register_generic_response(form_error="password_mismatch", status=400)

    now = _utc_now()
    # Bounded rate limit keyed on a privacy-preserving email digest (no raw email
    # as a key). Whether limited or not, the PUBLIC response is identical.
    try:
        allowed = _get_account_store().record_rate_attempt(
            subject_key=_acct.email_digest(email_normalized), action="register",
            now_iso=_iso(now),
            window_reset_iso=_iso(now + _timedelta_seconds(_REGISTER_RATE_WINDOW_SECONDS)),
            limit=_REGISTER_RATE_LIMIT)
    except Exception:
        allowed = False  # fail closed; still returns the generic response
    if not allowed:
        return _register_generic_response()

    # Create the account atomically; a duplicate email fails closed to the SAME
    # generic response (no enumeration). Any other store failure is also generic.
    try:
        store = _get_account_store()
        account_id = _acct.new_account_id()
        store.create_account(
            account_id=account_id, email_normalized=email_normalized,
            password_hash=_acct.hash_password(password), created_at=_iso(now))
    except EmailExistsError:
        return _register_generic_response()          # existing account: identical response
    except Exception:
        return _register_generic_response()          # generic; no internal detail leaked

    # Issue a verification token: store only its hash; the RAW token goes solely
    # into the dev email sink message body (never logged, never in the response).
    try:
        raw_token = _acct.new_raw_token()
        store.create_email_token(
            token_id=_acct.new_token_id(), account_id=account_id,
            token_type=VERIFICATION, token_hash=_acct.hash_token(raw_token),
            expires_at=_iso(now + _timedelta_seconds(_VERIFICATION_TTL_SECONDS)),
            created_at=_iso(now))
        _EMAIL_SENDER.send(
            to=email_normalized,
            subject="Verify your InventorAI email",
            body=("Use this code to verify your email (valid 24 hours): "
                  + raw_token))
    except Exception:
        # A token/email-sink failure does not change the generic response and does
        # not sign anyone in; the account row already committed atomically above.
        pass
    return _register_generic_response()


def _timedelta_seconds(seconds):
    from datetime import timedelta
    return timedelta(seconds=seconds)


# --- P5-2: authenticated sessions, email verification & account recovery ------
# A constant dummy scrypt hash so a login for an unknown email still runs one
# scrypt verification (constant-ish timing; no account-existence timing oracle).
_DUMMY_PASSWORD_HASH = _acct.hash_password(secrets.token_urlsafe(24))


def _csrf_reject():
    """Generic, non-enumerating rejection for a missing/invalid CSRF token."""
    return ("Your session security token was missing or invalid. Please reload "
            "the page and try again.", 403)


def _issue_verification(account, now):
    """Issue (and dev-sink send) a fresh verification token; only its hash is
    stored, the raw token goes solely into the sink body."""
    raw = _acct.new_raw_token()
    _get_account_store().create_email_token(
        token_id=_acct.new_token_id(), account_id=account["account_id"],
        token_type=VERIFICATION, token_hash=_acct.hash_token(raw),
        expires_at=_iso(now + _timedelta_seconds(_VERIFICATION_TTL_SECONDS)),
        created_at=_iso(now))
    _EMAIL_SENDER.send(
        to=account["email_normalized"], subject="Verify your InventorAI email",
        body=("Use this link to verify your email (valid 24 hours): "
              "/verify/" + raw))


def _issue_reset(account, now):
    """Issue (and dev-sink send) a fresh 1-hour password-reset token; hash-only
    at rest; the raw token appears solely in the sink body, never in logs."""
    raw = _acct.new_raw_token()
    _get_account_store().create_email_token(
        token_id=_acct.new_token_id(), account_id=account["account_id"],
        token_type=RESET, token_hash=_acct.hash_token(raw),
        expires_at=_iso(now + _timedelta_seconds(_RESET_TTL_SECONDS)),
        created_at=_iso(now))
    _EMAIL_SENDER.send(
        to=account["email_normalized"], subject="Reset your InventorAI password",
        body=("Use this link to reset your password (valid 1 hour): "
              "/reset/" + raw))


def _render_login(error=False, status=200, deactivated=False):
    return render_template(
        "login.html", login_error=error, deactivated=deactivated,
        login_failed_en=LOGIN_FAILED_MESSAGE_EN,
        login_failed_ar=LOGIN_FAILED_MESSAGE_AR), status


@app.route("/login", methods=["GET"])
def login_form():
    if _current_account():
        return redirect(url_for("account_home"))
    # P10-D3b: truthful post-deactivation notice (display-only; no mutation and
    # no account detail — the flag comes solely from the redirect query string).
    return _render_login(
        deactivated=(request.args.get("notice") == "deactivated"))


@app.route("/login", methods=["POST"])
def login_submit():
    """Authenticate email + password. Generic non-enumerating failure; hardened
    rate limit; scrypt verify; only an ACTIVE account may sign in; session is
    ROTATED on success. No project creation, no ownership assignment. Unverified
    accounts MAY sign in (limited per contract) — verification is not a login
    gate here."""
    email_normalized = _acct.normalize_email(request.form.get("email", ""))
    password = request.form.get("password", "")
    now = _utc_now()
    _cleanup_rate_limits(now)
    if not _rate_ok(_acct.email_digest(email_normalized), "login", now,
                    _LOGIN_RATE_LIMIT, _LOGIN_RATE_WINDOW_SECONDS):
        return _render_login(error=True, status=429)
    account = None
    try:
        if _acct.is_valid_email(email_normalized):
            account = _get_account_store().get_account_by_normalized_email(email_normalized)
    except Exception:
        account = None
    # Always run exactly one scrypt verification (real or dummy) — no existence
    # timing oracle. Accept only an active account with a correct password.
    stored_hash = account["password_hash"] if account else _DUMMY_PASSWORD_HASH
    password_ok = _acct.verify_password(stored_hash, password)
    if account is None or account["status"] != "active" or not password_ok:
        return _render_login(error=True, status=401)   # identical generic failure
    _sign_in(account, now)
    return redirect(url_for("account_home"))


@app.route("/account", methods=["GET"])
def account_home():
    account = _current_account()
    if not account:
        return redirect(url_for("login_form"))
    return render_template("account.html", account=account,
                           csrf_token=_session_csrf(), notice=None,
                           owned_projects=_owned_projects(account))


def _owned_projects(account):
    """The minimum truthful 'Your projects' list: the project_ids durably owned by
    THIS account (contract §13). Never includes NULL-owner legacy projects and
    never another account's projects. No dashboard/analytics/sharing."""
    try:
        return _get_store().project_ids_for_owner(account["account_id"])
    except Exception:
        return []


@app.route("/account/projects/<project_id>/export", methods=["GET"])
def account_project_export(project_id):
    """P10-D3a — Self-Service Project Export (established contract
    ``docs/governance/P10_D3A_SELF_SERVICE_PROJECT_EXPORT_INCREMENT_CONTRACT.md``,
    merged PR #510).

    ONE browser/session-authenticated, PROJECT-SCOPED export: the signed-in
    durable OWNER downloads the canonical Structured Export of one owned project.
    The route is pure glue — identity comes from the existing validated
    ``_current_account()`` seam and the decision + payload come from the existing
    canonical P7-I1 seam ``produce_project_export``, consumed UNMODIFIED (§S-3).
    The seam's STRICTER durable-owner rule is binding here (§6.2): a NULL-owner
    legacy/anonymous project is denied — this route never falls back to the more
    permissive ``_project_authorized`` capability helper.

    Denial is ONE generic, non-enumerating response (§S-4): anonymous callers,
    non-owners, missing projects, and NULL-owner projects all receive the exact
    same ``_deny_project()`` redirect, so a denial never reveals whether a
    project exists or who owns it. Any unexpected failure FAILS CLOSED (§S-4b):
    a bare generic 503 with no traceback, exception text, or partial payload.

    The success response is the seam dict serialized directly as
    ``application/json`` with a deterministic project-scoped attachment filename
    (§S-4a): no wrapper key, no API-v1 envelope, no HTML, no transformation. No
    API credential is required or consulted; no ``access_audit`` event is
    written (§6.4 — the deferred Phase-7 §25 disposition is preserved, not
    extended); nothing durable is created or mutated."""
    account = _current_account()
    if account is None:
        return _deny_project()
    try:
        export = _read_export.produce_project_export(
            _get_store(), project_id, account["account_id"])
        body = json.dumps(export)
    except _read_export.ProjectAccessDenied:
        return _deny_project()
    except Exception:
        # Fail closed (§S-4b): generic, empty-bodied 503 — never a traceback,
        # internal detail, or partial export served as success.
        return app.response_class(status=503)
    response = app.response_class(
        response=body,
        status=200,
        mimetype="application/json",
    )
    response.headers["Content-Disposition"] = (
        'attachment; filename="inventorai-project-%s-export.json"' % project_id)
    return response


@app.route("/account/deactivate", methods=["POST"])
def account_deactivate():
    """P10-D3b — Account Deactivation (established contract
    ``docs/governance/P10_D3B_ACCOUNT_DEACTIVATION_INCREMENT_CONTRACT.md``,
    merged PR #512).

    ONE self-service account state transition: the authenticated account holder
    DEACTIVATES their own account. This is deactivation, NOT deletion: exactly
    one ``accounts`` row changes (``status`` -> ``"deleted"``, ``deleted_at``
    stamped, ``updated_at``/``session_epoch`` updated) via the EXISTING bounded
    store primitives ``set_status`` + ``increment_session_epoch``; no row in any
    table is removed and no retention behaviour changes.

    Guard order (fail closed, ``logout_all`` precedent): authenticated
    ``_current_account()`` -> ``_csrf_valid()`` -> password re-entry verified
    with the EXISTING ``verify_password`` helper. A failed guard mutates
    NOTHING. POST only — no GET/query-param mutation.

    Enforcement after success is the EXISTING status-gated machinery, consumed
    not duplicated: ``validate_session`` fails closed (``inactive``) for every
    session of a non-active account (primary mechanism — the epoch bump is
    defense-in-depth only, contract §3 S-3); login requires an active account;
    ``web/api_v1.py`` refuses credentials whose bound account is non-active, so
    API credentials become unusable WITHOUT being individually revoked or
    deleted (contract §6.5). Partial-failure semantics (contract §3 S-5): if
    the epoch bump fails after ``set_status`` succeeded, the account IS
    deactivated and every session still dies on its next request — no false
    rollback claim. Unexpected failure before mutation returns a bare generic
    503 (no traceback/internal detail). No ``access_audit`` write (§6.6 —
    Phase-7 §25 disposition preserved, not extended). No reactivation path."""
    account = _current_account()
    if not account:
        return redirect(url_for("login_form"))
    if not _csrf_valid():
        return _csrf_reject()
    if not _acct.verify_password(account["password_hash"],
                                 request.form.get("password", "")):
        # Safe generic failure; nothing mutated (contract §5).
        return render_template("account.html", account=account,
                               csrf_token=_session_csrf(),
                               notice="deactivate_failed",
                               owned_projects=_owned_projects(account)), 403
    now_iso = _iso(_utc_now())
    try:
        if _get_account_store().set_status(
                account["account_id"], "deleted", now_iso) != 1:
            raise RuntimeError("account row not updated")
    except Exception:
        # Fail closed (contract §3 S-5): bare generic 503 — never a traceback,
        # internal detail, or false success.
        return app.response_class(status=503)
    try:
        _get_account_store().increment_session_epoch(account["account_id"], now_iso)
    except Exception:
        pass    # defense-in-depth only: status alone already ends every session
    ui_lang = flask_session.get("ui_lang")   # D-P6-18: preserve UI-language choice
    flask_session.clear()
    if ui_lang == "ar":
        flask_session["ui_lang"] = "ar"
    return redirect(url_for("login_form", notice="deactivated"))


@app.route("/logout", methods=["POST"])
def logout():
    """Log out the CURRENT browser session only. CSRF-protected when signed in.
    Never deletes accepted-answer data, never changes ownership, never uploads or
    exposes a local draft."""
    if _current_account() and not _csrf_valid():
        return _csrf_reject()
    _ui_lang = flask_session.get("ui_lang")   # D-P6-18: preserve UI-language choice
    flask_session.clear()
    if _ui_lang == "ar":
        flask_session["ui_lang"] = "ar"
    return redirect(url_for("login_form"))


@app.route("/logout-all", methods=["POST"])
def logout_all():
    """Revoke EVERY authenticated session for the account by incrementing
    ``session_epoch`` (this cookie's epoch becomes stale too). CSRF-protected."""
    account = _current_account()
    if not account:
        return redirect(url_for("login_form"))
    if not _csrf_valid():
        return _csrf_reject()
    try:
        _get_account_store().increment_session_epoch(account["account_id"], _iso(_utc_now()))
    except Exception:
        pass
    _ui_lang = flask_session.get("ui_lang")   # D-P6-18: preserve UI-language choice
    flask_session.clear()
    if _ui_lang == "ar":
        flask_session["ui_lang"] = "ar"
    return redirect(url_for("login_form"))


@app.route("/account/resend-verification", methods=["POST"])
def resend_verification():
    """Authenticated, CSRF-protected verification resend. Generic outcome;
    hardened rate limit; supersede-then-issue only for an active, still-unverified
    account. A deleted account cannot reach here (its session is invalid); a
    disabled account fails closed the same way."""
    account = _current_account()
    if not account:
        return redirect(url_for("login_form"))
    if not _csrf_valid():
        return _csrf_reject()
    now = _utc_now()
    _cleanup_rate_limits(now)
    allowed = _rate_ok(_acct.email_digest(account["email_normalized"]), "resend",
                       now, _RESEND_RATE_LIMIT, _RESEND_RATE_WINDOW_SECONDS)
    if allowed and account["status"] == "active" and not account["email_verified"]:
        try:
            _issue_verification(account, now)
        except Exception:
            pass
    return render_template("account.html", account=account,
                           csrf_token=_session_csrf(), notice="resend")


@app.route("/verify/<token>", methods=["GET"])
def verify_email(token):
    """Complete email verification from the emailed link. Atomically consume the
    raw token (hash before lookup; type must be verification; unused; unexpired;
    active account) and set ``email_verified``. Replay/expired/invalid all render
    the SAME generic failure. No ownership is created."""
    now = _utc_now()
    verified = False
    try:
        account_id = _get_account_store().consume_token(
            _acct.hash_token(token), VERIFICATION, _iso(now))
        if account_id:
            _get_account_store().mark_email_verified(account_id, _iso(now))
            verified = True
    except Exception:
        verified = False
    return _token_bearing(render_template("verify_result.html", verified=verified))


@app.route("/recover", methods=["GET"])
def recover_form():
    return render_template("recover.html", submitted=False,
                           generic_en=RECOVER_GENERIC_MESSAGE_EN,
                           generic_ar=RECOVER_GENERIC_MESSAGE_AR)


@app.route("/recover", methods=["POST"])
def recover_submit():
    """Request a password reset. ALWAYS returns the same generic response (no
    enumeration of existence / status / verification). Hardened rate limit; a
    1-hour hash-only reset token is issued only for an active account."""
    email_normalized = _acct.normalize_email(request.form.get("email", ""))
    now = _utc_now()
    _cleanup_rate_limits(now)
    allowed = _rate_ok(_acct.email_digest(email_normalized), "recover", now,
                       _RECOVER_RATE_LIMIT, _RECOVER_RATE_WINDOW_SECONDS)
    if allowed and _acct.is_valid_email(email_normalized):
        try:
            account = _get_account_store().get_account_by_normalized_email(email_normalized)
            if account and account["status"] == "active":
                _issue_reset(account, now)
        except Exception:
            pass
    return render_template("recover.html", submitted=True,
                           generic_en=RECOVER_GENERIC_MESSAGE_EN,
                           generic_ar=RECOVER_GENERIC_MESSAGE_AR)


@app.route("/reset/<token>", methods=["GET"])
def reset_form(token):
    return _token_bearing(
        render_template("reset.html", form_error=None, done=False))


@app.route("/reset/<token>", methods=["POST"])
def reset_submit(token):
    """Complete a password reset. Validate the new password (P5-1 policy), then
    atomically consume the reset token (type reset; unused; unexpired; active
    account), scrypt-hash and store the new password, INCREMENT ``session_epoch``
    (revoking every existing authenticated session), and supersede any other
    reset tokens. Does NOT auto-sign-in. Invalid/expired/used → generic failure."""
    password = request.form.get("password", "")
    confirm = request.form.get("password_confirm", "")
    ok, _reason = _acct.validate_password(password)
    if not ok:
        return _token_bearing(render_template(
            "reset.html", form_error="password_invalid", done=False), 400)
    if password != confirm:
        return _token_bearing(render_template(
            "reset.html", form_error="password_mismatch", done=False), 400)
    now = _utc_now()
    account_id = None
    try:
        store = _get_account_store()
        account_id = store.consume_token(_acct.hash_token(token), RESET, _iso(now))
        if account_id:
            store.set_password_hash(account_id, _acct.hash_password(password), _iso(now))
            store.increment_session_epoch(account_id, _iso(now))
            store.supersede_tokens(account_id, RESET, _iso(now))
    except Exception:
        account_id = None
    if not account_id:
        return _token_bearing(render_template(
            "reset.html", form_error="token_invalid", done=False), 400)
    _ui_lang = flask_session.get("ui_lang")   # D-P6-18: preserve UI-language choice
    flask_session.clear()   # never auto-sign-in on reset
    if _ui_lang == "ar":
        flask_session["ui_lang"] = "ar"
    return _token_bearing(
        render_template("reset.html", form_error=None, done=True))


@app.route("/data-and-session", methods=["GET"])
def data_and_session():
    # G-UX-TRUST (S15): static informational Data & Session trust surface.
    # GET-only; takes no session id; reads no session data; mutates nothing;
    # calls no engine function; performs no logging, persistence, or redirect;
    # renders only the static template.
    return render_template("data_session.html")

@app.route("/start", methods=["POST"])
def start():
    idea_text = request.form.get("idea", "").strip()
    if not idea_text:
        return redirect(url_for("index"))
    # P10-SEC2: bounded free-text hardening — explicit rejection (400, this
    # surface's existing form-error convention), never truncation; runs before
    # ANY classification, session creation, or durable write. The legacy
    # fixed-domain ILT-002 start routes are historical evidence surfaces and
    # remain transport-bounded only (MAX_CONTENT_LENGTH).
    _input_error = _free_text_error(idea_text, _current_ui_lang())
    if _input_error is not None:
        return _render_start_page(error=_input_error, status=400)
    # CF5-F002 (Owner decision D-CF5-F002-01, D1/D2/D3): the /start admission
    # surface derives ALL domain behavior from the canonical activation set
    # (engine.domain_activation, §5-I2) and the canonical classifier
    # (engine.domain_rules.classify_domain) — no hardcoded electronics
    # constant, branch, or special case. `_admit_specialist_domain` remains the
    # single activation gate at the admission point.
    activated = _activated_specialist_domains()
    confirm = request.form.get("domain_confirm")
    choice = request.form.get("domain_choice")
    # CF-2 Arabic-localization remainder: computed once, reused at every
    # message-producing call site below (same reuse discipline already
    # established for `activated`).
    lang = _current_ui_lang()
    if not activated:
        # Defensive fail-closed boundary: with no activated specialist domain
        # nothing is admissible. Unreachable under any governed activation state.
        return _render_start_page(error=_unsupported_domain_message(activated, lang))
    sole = activated[0] if len(activated) == 1 else None
    if sole is not None and confirm != sole:
        # Exactly ONE activated domain: the one-step form carries that sole
        # domain's explicit confirmation (ADR-001 explicit assignment; D1/U3).
        # Consent is never inferred from the idea text; without it no session
        # is created. Behaviorally identical to the historical electronics-only
        # flow under `['electronics_electrical']`.
        return _render_start_page(error=_confirmation_required_message(sole, lang))
    # Canonical deterministic classification (P9-E2-R): dispatch by result KIND,
    # never by truthiness / string identity of the structured result.
    # classify_domain() yields SINGLE / NONE and — since P9-E2 — AMBIGUOUS_TIE
    # when two or more ACTIVATED domains are equally top-scored (reachable only
    # under a broadened activation set, exercised today via bounded activation
    # doubles); MULTI_DOMAIN_NEEDS_D4 remains representable but is never
    # produced (D4 is a separate, unexecuted gate) — its branch stays dormant
    # and fail-closed.
    classification = classify_domain(idea_text)
    if classification.kind is DomainResultKind.AMBIGUOUS_TIE:
        # Fail closed: an ambiguous activated tie is NOT a single supported
        # domain. It must never enter the None classifier-miss fallback, never
        # admit a winner, never create a session (P9-E2-R 7/14; §4.B/D).
        return _render_start_page(error=_unsupported_domain_message(activated, lang))
    if classification.kind is DomainResultKind.MULTI_DOMAIN_NEEDS_D4:
        # Fail closed: a genuine multi-domain idea is NOT admissible as one
        # domain, and D4 is NOT executed here. No implication that multi-domain
        # analysis occurred (P9-E2-R 7/14/16).
        return _render_start_page(error=_unsupported_domain_message(activated, lang))
    if classification.kind is DomainResultKind.UNRESOLVED_NON_ACTIVATED_TIE:
        # CF5-F004 (merged contract §3.5): a zero-activated tie the legacy
        # compatibility layer cannot resolve is NOT admissible as one domain
        # and must NEVER fall through to the NONE consent path (the validated
        # dangerous chain: silent NONE -> sole-electronics consent -> a
        # mislabeled electronics session). Same existing fail-closed refusal
        # surface; no admission/UX change.
        return _render_start_page(error=_unsupported_domain_message(activated, lang))
    # SINGLE -> the resolved registry domain string; NONE -> None.
    domain = (classification.selected_domain
              if classification.kind is DomainResultKind.SINGLE else None)
    lowered = idea_text.lower()
    # Domain Gate / Entry UX Increment (post-PR #100 Increment Contract),
    # activation-aware since CF5-F002 (CF-6 facet): vocabulary evidencing a
    # domain that is NOW ACTIVATED no longer fires, so stale vocabulary can
    # never suppress an activated domain; families outside the activation set
    # still refuse, and explicit confirmation cannot override them
    # (§7.C, §10, §15).
    if _has_strong_unsupported_evidence(lowered, activated):
        return _render_start_page(error=_unsupported_domain_message(activated, lang))
    if domain is not None and domain in activated:
        # D1 — the classifier resolved exactly one ACTIVATED specialist domain:
        # that classified domain (and only it) is the admissible target.
        target = domain
    elif domain is not None:
        # Recognized-but-not-activated (or unexpected) classification.
        if (sole == "electronics_electrical"
                and _is_recognized_not_activated(domain, activated)):
            # Domain Gate / Entry UX Increment weak-conflict resolution,
            # preserved unchanged for the governed electronics-only one-step
            # flow (§4.A backward compatibility): a weak/ambiguous conflicting
            # supported-domain classification (e.g. the generic word
            # "monitoring") with no strong unsupported evidence resolves toward
            # the explicitly confirmed electronics domain ONLY with
            # corroborating lay electrical mechanism evidence; a medical_device
            # conflict requires MORE corroboration than one lay token (§7.C,
            # §10 — confirmation is never an unconditional override). Otherwise
            # guide the owner toward naming the electrical mechanism instead of
            # a bare hard rejection (§7.B, §7.E). No session on guidance.
            required = (_MEDICAL_CONFLICT_LAY_MINIMUM
                        if domain == "medical_device" else 1)
            if _lay_electrical_evidence_count(lowered) < required:
                return _render_start_page(
                    error=ui_text.localize_message(MECHANISM_GUIDANCE_MESSAGE, lang))
            target = sole
        else:
            # §4.B/C/F: a recognized-but-not-activated domain is never offered
            # and never admitted (no cross-domain relabeling); unexpected
            # classifier values are refused defensively.
            return _render_start_page(error=_unsupported_domain_message(activated, lang))
    else:
        # NONE — classifier miss.
        if sole is not None:
            # Derived corner (D2 backward-compat + D3): with exactly one
            # activated domain, offer that sole domain under the explicit
            # consent already validated above. Under `['electronics_electrical']`
            # this is the unchanged governed NONE->Electronics
            # explicit-consent admission (covers functional ideas the signal
            # classifier misses).
            target = sole
        elif choice in activated:
            # D2 — the user explicitly chose one of the currently activated
            # specialist domains; it still requires explicit confirmation below.
            target = choice
        else:
            # D2 — no (valid) choice yet: present ONLY the currently activated
            # specialist domains as the explicit choice set. No silent
            # Electronics/default fallback; no session. A forged choice outside
            # the activation set lands here (never admitted).
            return _render_start_page(
                error=ui_text.localize_message(DOMAIN_CHOICE_MESSAGE, lang),
                choice_domains=activated, carry_idea=idea_text)
    if confirm != target:
        # Explicit consent for the resolved target domain (D1/D2/U1: no
        # auto-admit). Present exactly the target for confirm/decline; a
        # missing or mismatched confirmation (including one for a DIFFERENT
        # activated domain) never admits and never relabels (§4.F).
        return _render_start_page(
            error=_present_confirm_message(target, lang), present_domain=target,
            carried_choice=(choice if choice == target else None),
            carry_idea=idea_text)
    # Admit: the persisted session-domain is exactly the classified-or-chosen
    # AND explicitly confirmed ACTIVATED domain (§4.F — no cross-domain
    # mislabeling).
    state = IdeaState(idea_id=str(uuid.uuid4()))
    # Specialist-runtime admission remains bound to the canonical engine
    # activation policy (§5-I2) at this single gate; the target is admitted
    # only because the policy currently activates it.
    state.domain = _admit_specialist_domain(target)
    state.domain_signal = state.domain
    # Increment 1 (Owner-Expert Question Boundary): the general /start flow is the
    # non-specialist owner flow and must use the committed Path N non-specialist-safe
    # question provider (NON_SPECIALIST_QUESTIONING_POLICY). This is the same
    # provider already used by the governed _path_n route; no new question bank,
    # mode selector, role, or engine-state field is introduced. The named ILT
    # routes below are deliberately left on their existing default behavior.
    state.path = "N"
    # P4-1b-1 unified capability: ONE uuid4 is used as both the route `sid` and
    # the durable `project_id` (`idea_id` stays a separate uuid4, set above).
    sid = str(uuid.uuid4())
    initial_result = run_iteration(state, idea_text)
    # P4-1b-1 creation order: durably create the project envelope BEFORE any live
    # session is advertised. Durable creation is the commit point for /start; on
    # failure we fail closed — no SESSION_STORE entry, generic unavailable, no
    # user content logged. The envelope carries only the accepted-input ledger
    # (empty at creation) + idea_id; readiness/gaps/last_result are NOT persisted.
    # P5-3: a NEW project is owned ONLY when an authenticated, active, verified
    # account creates it (ownership derived solely from the validated server
    # session, never from client input). Anonymous and unverified users create a
    # NULL-owner project — the anonymous journey is preserved and no ownership is
    # claimed. Ownership is written ATOMICALLY inside create_project's INSERT.
    owner_account_id = _new_project_owner()
    try:
        contract = ProjectRecordContract.from_state(state)
        _get_store().create_project(
            contract, project_id=sid,
            reconstruction_inputs=_reconstruction_inputs(idea_text, state),
            owner_account_id=owner_account_id)
    except Exception:
        return _render_start_page(
            error=ui_text.localize_message(SERVICE_UNAVAILABLE_MESSAGE, _current_ui_lang()),
            status=503)
    SESSION_STORE[sid] = {"state": state, "last_result": initial_result, "transcript": [],
                          # Draft Level 2: a truthful ONE-SHOT seed-accepted signal.
                          # Set only here at successful /start; the first session
                          # render pops it so the client clears ONLY the matching
                          # seed draft (never on an unrelated session render).
                          "_seed_accepted": True}
    return redirect(url_for("show_session", sid=sid))

def _reconstruction_inputs(seed_idea, state):
    """P4-2 Level-1 (G-P4-2-LEVEL1-IMPLEMENTATION-01): the additive, persisted-once
    project-envelope reconstruction inputs for a newly created project. Written
    ONLY at creation; never mutated afterwards. ``seed_idea`` is verbatim user
    content — it is stored only in the durable project envelope, never logged,
    never placed in an exception string, and never duplicated into an
    ``AssertionRecord``. The confirmed domain and path are read from the state the
    start route already established; the version is the exact supported stamp."""
    return {
        "seed_idea_text": seed_idea,
        "confirmed_domain": getattr(state, "domain", None),
        "path": getattr(state, "path", None),
        "engine_contract_version": RECONSTRUCTION_VERSION,
    }

def _finalize_started_session(sid, state, initial_result, seed_idea=None):
    """Shared start finalisation. Durably create the project envelope (the SAME
    minimum P4-1b-1 envelope /start uses) BEFORE advertising a live session, then
    store the runtime entry. Fail closed (generic 503) if durable creation fails,
    so no live session is advertised without durable backing. Added for P4-1b-2a
    so the legacy start_ilt002_* routes remain usable: their accepted answers
    require a durable envelope. No second persistence model; no UX/scope change.
    P4-2 Level-1: the additive reconstruction inputs (seed/domain/path/version) are
    persisted at this creation point when the caller supplies the seed idea."""
    try:
        _get_store().create_project(
            ProjectRecordContract.from_state(state), project_id=sid,
            reconstruction_inputs=_reconstruction_inputs(seed_idea, state))
    except Exception:
        return _render_start_page(
            error=ui_text.localize_message(SERVICE_UNAVAILABLE_MESSAGE, _current_ui_lang()),
            status=503)
    SESSION_STORE[sid] = {"state": state, "last_result": initial_result, "transcript": [],
                          # Draft Level 2: a truthful ONE-SHOT seed-accepted signal.
                          # Set only here at successful /start; the first session
                          # render pops it so the client clears ONLY the matching
                          # seed draft (never on an unrelated session render).
                          "_seed_accepted": True}
    return redirect(url_for("show_session", sid=sid))


@app.route("/start_ilt002_water_leak", methods=["POST"])
def start_ilt002_water_leak():
    idea_text = request.form.get("idea", "").strip()
    if not idea_text:
        return redirect(url_for("index"))
    state = IdeaState(idea_id=str(uuid.uuid4()))
    # Specialist-runtime admission bound to the canonical engine activation policy (§5-I2).
    state.domain = _admit_specialist_domain("electronics_electrical")
    state.domain_signal = state.domain
    sid = str(uuid.uuid4())
    initial_result = run_iteration(state, idea_text)
    return _finalize_started_session(sid, state, initial_result, seed_idea=idea_text)

@app.route("/start_ilt002_combination_lock", methods=["POST"])
def start_ilt002_combination_lock():
    idea_text = request.form.get("idea", "").strip()
    if not idea_text:
        return redirect(url_for("index"))
    state = IdeaState(idea_id=str(uuid.uuid4()))
    # Specialist-runtime admission bound to the canonical engine activation policy (§5-I2).
    state.domain = _admit_specialist_domain("electronics_electrical")
    state.domain_signal = state.domain
    sid = str(uuid.uuid4())
    initial_result = run_iteration(state, idea_text)
    return _finalize_started_session(sid, state, initial_result, seed_idea=idea_text)

@app.route("/start_ilt002_combination_lock_path_n", methods=["POST"])
def start_ilt002_combination_lock_path_n():
    idea_text = request.form.get("idea", "").strip()
    if not idea_text:
        return redirect(url_for("index"))
    state = IdeaState(idea_id=str(uuid.uuid4()))
    # Specialist-runtime admission bound to the canonical engine activation policy (§5-I2).
    state.domain = _admit_specialist_domain("electronics_electrical")
    state.domain_signal = state.domain
    state.path = "N"
    sid = str(uuid.uuid4())
    initial_result = run_iteration(state, idea_text)
    return _finalize_started_session(sid, state, initial_result, seed_idea=idea_text)

def _draft_context_id(question):
    """Draft Level 2: a stable, non-sensitive per-question context identifier for
    the client-side local-draft key. A short SHA-256 digest of the CURRENT question
    text (or a fixed token when there is no gap/question), so a draft saved for one
    question is not offered for a different/changed question. It carries no raw
    invention text, persists nothing server-side, and affects no engine behaviour."""
    import hashlib
    basis = (question or "").strip()
    if not basis:
        return "intake"
    return hashlib.sha256(basis.encode("utf-8")).hexdigest()[:16]

@app.route("/session/<sid>/resume", methods=["POST"])
def resume_project(sid):
    """P10-PC3 — TRUE WRITABLE RESUME: explicit establishment of a NEW
    transient writable context for the SAME durable project (implements
    docs/governance/P10_PC3_TRUE_WRITABLE_RESUME_INCREMENT_CONTRACT.md).

    Canonical sequence: ownership check -> deterministic reconstruction
    (single canonical replay) -> validation/eligibility -> establishment.
    Establishment performs ZERO durable writes (reconstruction is read-only);
    the first durable write after resume can only be a valid new user action
    through the UNCHANGED accepted-answer pipeline. GET never establishes.
    The original in-memory session is NOT restored (transcript, last_result,
    the transient non-answer action/display metadata in `interaction_actions`,
    criticality stage stay absent — never fabricated); this is a reconstructed
    continuation. PVCG-R1 precision: the DURABLE non-answer ledger records
    (`unknown` / `deferred` / `provisional_assumption` / `specialist_requested`
    / `evidence_requested`) ARE reconstructed, verbatim, by the canonical
    reconstruction above — it is only their transient/display metadata that is
    absent. Every failure path fails closed to the truthful read-only view
    (never a 500, never a fabricated writable state); denials stay generic and
    non-enumerating."""
    if not _project_authorized(sid):
        return _deny_project()
    entry = SESSION_STORE.get(sid)
    if entry is not None and getattr(entry["state"], "domain", None) is not None:
        # Already live or already established: idempotent no-op.
        return redirect(url_for("show_session", sid=sid))
    try:
        _recon = reconstruct_readonly_state(_get_store(), sid)
    except Exception:
        _recon = None
    if _recon is None or _recon.review.level != 1 or _recon.state is None:
        # Legacy/version-mismatch/corrupt/unavailable: read-only view remains.
        return redirect(url_for("show_session", sid=sid))
    rstate = _recon.state
    if not domain_activation.is_activated(getattr(rstate, "domain", None)):
        return redirect(url_for("show_session", sid=sid))
    if rstate.maturity_level >= 2 and not rstate.get_open_gaps():
        # Completed project: truthful completion/deliverable surfaces remain;
        # a completed journey never reopens into a writable question flow.
        return redirect(url_for("show_session", sid=sid))
    # Establishment: the replayed canonical IdeaState (domain/path set by the
    # canonical replay from the persisted inputs; ledger restored verbatim)
    # becomes the state of a FRESH transient entry. A fresh answer token is
    # minted lazily on next render; nothing historical-transient is fabricated.
    SESSION_STORE[sid] = {
        "state": rstate,
        "last_result": None,
        "transcript": [],
        "resumed_project": True,
    }
    return redirect(url_for("show_session", sid=sid))


@app.route("/session/<sid>", methods=["GET"])
def show_session(sid):
    if not _project_authorized(sid):
        return _deny_project()
    entry = SESSION_STORE.get(sid)
    if not entry:
        # P4-1b-1 durable cold-load: after memory loss, rebuild the minimum
        # runtime entry from the durable project envelope keyed by sid. On any
        # missing/malformed/unavailable durable state this returns None and we
        # fall through to the existing generic unavailable behaviour (no
        # disclosure of whether the project ever existed).
        entry = _cold_load_entry(sid)
        if not entry:
            return redirect(url_for("index"))
        SESSION_STORE[sid] = entry
    state = entry["state"]
    last_result = entry.get("last_result")
    # P10-PC1: surface the merged P4-2 Level-1 deterministic READ-ONLY
    # reconstruction on cold-loaded sessions (the committed cold-load marker is
    # `state.domain is None`; live /start sessions always carry a domain).
    # Display-only: `state.domain` is NOT restored, the P4-1b-2a non-resume
    # guard is untouched, and any reconstruction failure (Level-0 fallback,
    # ContractError, replay-limit, store unavailability) fails closed to the
    # prior cold-load page — never a 500, never a false reconstruction claim.
    reconstructed_review = None
    if getattr(state, "domain", None) is None:
        try:
            _recon = reconstruct_review_state(_get_store(), sid)
            if _recon.level == 1 and _recon.reconstructed:
                reconstructed_review = {
                    "domain": getattr(state, "domain_signal", None),
                    "maturity_level": _recon.maturity_level,
                    "current_stage": _recon.current_stage,
                    "open_gaps": list(_recon.open_gaps),
                    "next_question": _recon.next_question,
                    "answers_count": len(_recon.accepted_answer_evidence),
                    # P10-PC3: writable-resume eligibility for the explicit
                    # establishment button (display precheck only; the POST
                    # route re-validates from scratch). Completed projects
                    # (maturity >= 2, no open gaps) never reopen. Fields come
                    # from the Level-1 review snapshot; the display domain is
                    # the persisted confirmed identity on domain_signal.
                    "resume_eligible": bool(
                        (_recon.maturity_level < 2 or _recon.open_gaps)
                        and domain_activation.is_activated(
                            getattr(state, "domain_signal", None))),
                }
        except Exception:
            reconstructed_review = None
    INTAKE_QUESTION = "Describe your invention in more detail — what specific problem does it solve, and how does it solve it?"

    gap_type = select_next_gap(state)
    question = None
    if gap_type:
        gap = state.get_gap(gap_type)
        iterations_open = gap.iterations_open if gap else 0
        # Increment 1 (Owner-Expert Question Boundary): render via the display
        # selector so an exhausted non-specialist Path N gap shows the
        # deterministic plain-language reframe instead of repeating the final
        # question verbatim. Pure selection — no engine/state/maturity effect.
        # `domain` is attached by the /start routes for live sessions; guard the
        # read so render-context construction never raises if it is absent (the
        # value is unchanged for every real session). No routing/method/state
        # change; the displayed question is identical when `domain` is present.
        question = get_display_question(getattr(state, "domain", None), gap_type,
                                        iterations_open, path=state.path)
    elif (
        state.maturity_level == 0
        and len(state.gaps) == 0
        and last_result is not None
        and last_result.get("transition") == "WARN"
        and "not yet established" in (last_result.get("reason") or "")
    ):
        question = INTAKE_QUESTION
    open_gaps = state.get_open_gaps()
    closed_gaps = [g for g in state.gaps if g.status == "CLOSED"]
    gap_labels = {g.gap_type: GAP_LABELS.get(g.gap_type, GAP_LABELS["__default__"]) for g in state.gaps}
    current_gap_label = GAP_LABELS.get(gap_type, GAP_LABELS["__default__"]) if gap_type else None
    # Transcript capture: store question before render so POST can record it.
    # No engine effect. Evidence preservation only.
    if entry is not None and question is not None:
        entry["last_question"] = question
    # Increment 3 (R-5): compute the one prioritized next development step from the
    # ALREADY-LOADED in-memory IdeaState via the shared pure derivation, and pass
    # it to the presentation-only session callout. Read-only: no route/method
    # change, no state mutation, no persistence, no scoring/progression.
    next_development_step = derive_next_development_step(state)
    # Guided Uncertainty Support (Increment Contract PR #134): derive, READ-ONLY,
    # the user's most recent submitted text from already-existing session state —
    # the last transcript response (an `answered` submission) or the last
    # non-answer interaction text (e.g. the "I do not know this yet" action) —
    # choosing the more recent by iteration. This reads existing structures only;
    # it mutates nothing, adds no field, and never re-scores. The text feeds the
    # pure display-only helper below; the saved answer is unaffected.
    _uncertainty_candidates = []
    _tx = entry.get("transcript") or []
    if _tx:
        _uncertainty_candidates.append(
            (_tx[-1].get("iteration", 0), _tx[-1].get("response", "") or ""))
    _actions = entry.get("interaction_actions") or []
    if _actions:
        _uncertainty_candidates.append(
            (_actions[-1].get("iteration", 0), _actions[-1].get("text", "") or ""))
    _uncertainty_text = (
        max(_uncertainty_candidates, key=lambda c: c[0])[1]
        if _uncertainty_candidates else "")
    return render_template("session.html",
        sid=sid,
        # P5-3: a TRUTHFUL owned-state signal — True only when the current
        # authenticated account is the durable owner of this project. Never claims
        # ownership for a NULL-owner (legacy/anonymous) project. Display only.
        project_owned_by_you=_owned_by_current(sid),
        # Draft Level 2 (local-draft recovery, client-side only): a truthful,
        # one-shot ACCEPTED signal (set only after a durable accepted answer,
        # popped here so it renders once) plus a stable per-question context id and
        # a draft-schema version. These let the client-side local-draft script key
        # drafts to the current question and clear them after a confirmed accept.
        # They add NO durable/engine/accepted-answer behaviour and store nothing.
        answer_accepted=(entry.pop("_answer_accepted", False) if entry else False),
        seed_accepted=(entry.pop("_seed_accepted", False) if entry else False),
        draft_context=_draft_context_id(question),
        draft_context_version="v1",
        state=state,
        # P4-1b-2a: the server-issued token every answered-producing form must
        # carry (retained across renders until an accepted answer consumes it).
        answer_token=_answer_token_for(sid, entry),
        # Workstream 4: read-only render context for the completion-stage
        # structured criticality step (None while the journey is in progress
        # or when no contextually supported unconfirmed requirement remains).
        # D-P6-18 final UI-chrome boundary: the criticality step's chrome (summary
        # lead, choice/action labels) follows ui_lang; the clarification ASK, the
        # echoed user statement/rationale, and tokens are NOT in the map and stay
        # verbatim (localize_deep passes unknown strings through unchanged).
        criticality_step=ui_text.localize_deep(
            _criticality_step_context(entry, state, sid), _current_ui_lang()),
        next_development_step=next_development_step,
        question=question,
        open_gaps=open_gaps,
        gap_type=gap_type,
        last_result=last_result,
        # D-P6-18: gap-label heading/guidance/stage_note are UI chrome/framing (not
        # the actual question), so they follow ui_lang via the presentation map.
        gap_labels=ui_text.localize_deep(gap_labels, _current_ui_lang()),
        current_gap_label=ui_text.localize_deep(current_gap_label, _current_ui_lang()),
        # P10-PC1: on a Level-1 reconstructed cold view, the stage/progress
        # displays show the TRUE reconstructed maturity instead of the reset
        # minimal-state value (display only; state is unchanged).
        maturity_label=get_maturity_label(
            reconstructed_review["maturity_level"] if reconstructed_review
            else state.maturity_level, _current_ui_lang()),
        display_maturity_level=(
            reconstructed_review["maturity_level"] if reconstructed_review
            else state.maturity_level),
        reconstructed_review=reconstructed_review,
        # P10-PC3: truthful mode banner for an explicitly resumed project
        # ("reconstructed continuation" — NEVER "restored original session").
        # Transient presentation flag only; set solely by the establishment
        # route below.
        resumed_project=bool(entry.get("resumed_project")),
        session_disclosure=get_session_disclosure(_current_ui_lang()),
        closed_gaps=closed_gaps,
        interaction_ack=ui_text.localize_deep(
            entry.pop("_interaction_ack", None) if entry else None, _current_ui_lang()),
        # G-UX-ANSWER-VALIDATION: single-use empty-answer validation error, popped
        # here so it renders exactly once after the Post/Redirect/Get and never
        # repeats on a later plain GET. None on every normal load.
        answer_error=ui_text.localize_message(
            entry.pop("_answer_error", None) if entry else None, _current_ui_lang()),
        # Increment 1B: advisory, derived, read-only responsibility guidance for
        # the current gap. Computed at render time; never stored, never affects
        # gates/scoring/maturity/closure/transcript/IdeaState. None when no gap.
        current_responsibility=ui_text.localize_deep(
            get_responsibility(gap_type) if gap_type else None, _current_ui_lang()),
        # Increment 1B clarification display: deterministic, owner-invoked,
        # display-only guidance explaining the current question. Derived from the
        # same gap_type at render time; never stored, never affects
        # gates/scoring/maturity/closure/transcript/IdeaState/persistence; adds no
        # owner action and no POST handling. None when no gap (intake path).
        current_clarification=ui_text.localize_deep(
            get_clarification(gap_type) if gap_type else None, _current_ui_lang()),
        # More Detail Needed / Guided Answer Scaffolding (Increment Contract PR
        # #106): deterministic, display-only guidance naming the KIND of missing
        # detail to add when the ALREADY-computed engine outcome for the current
        # answer is WARN. Derived at render time from the existing `last_result`
        # (unchanged) and the current gap; never stored, never rewrites/mutates
        # the answer, never closes a gap, never advances maturity, never creates
        # evidence, and never alters the PASS/WARN/BLOCK outcome. None unless WARN.
        current_scaffolding_guidance=ui_text.localize_deep(
            get_scaffolding_guidance(last_result, gap_type), _current_ui_lang()),
        # Plain-Language Result Feedback (Increment Contract PR #155): deterministic,
        # display-only, content-free plain-language explanation of the ALREADY-computed
        # result for the PRIMARY visible feedback line, derived at render time from the
        # existing `last_result` (transition + raw reason) alone. It never mutates
        # `last_result`, never rewrites `last_result.reason`, never re-scores, and never
        # alters the PASS/WARN/BLOCK outcome; the truthful badge and the raw reason (as
        # non-primary provenance) are rendered by the template independently. None when
        # there is no result / no recognized transition.
        current_result_feedback=ui_text.localize_deep(
            get_result_feedback(last_result), _current_ui_lang()),
        # Guided Answer Co-Authoring Increment 1 — Advisory Prompt Support
        # (Increment Contract PR #127): deterministic, display-only, content-free
        # OPTIONAL prompts naming the KIND of information the inventor could add to
        # their OWN answer for the current question. Derived at render time from
        # the current gap_type alone; never stored, never reads/rewrites/mutates
        # the answer, never closes a gap, never advances maturity/readiness, never
        # changes scoring/criticality, never touches the transcript/IdeaState/
        # persistence, and adds no owner action, save/approve flow, or form field.
        # None when there is no gap (intake path). The inventor remains the sole
        # author of any saved answer.
        current_answer_coauthoring=ui_text.localize_deep(
            get_answer_coauthoring_prompts(gap_type) if gap_type else None, _current_ui_lang()),
        # Guided Uncertainty Support (Increment Contract PR #134): deterministic,
        # display-only, content-free SUPPORTIVE prompts shown when the user's most
        # recent submitted text expresses uncertainty ("I don't know" / "لا أعرف").
        # Derived at render time from the read-only `_uncertainty_text` signal
        # above; never stored, never reads/rewrites/mutates the answer, never
        # closes a gap, never marks uncertainty as sufficient, never advances
        # maturity/readiness, never changes scoring/criticality, never touches the
        # transcript/IdeaState/persistence, and adds no owner action, save/approve
        # flow, or form field. None when the text is not uncertainty. The inventor
        # remains the sole author of any saved answer.
        current_uncertainty_guidance=get_uncertainty_guidance(_uncertainty_text),
    )
@app.route("/session/<sid>/deliverable", methods=["GET"])
def show_deliverable(sid):
    if not _project_authorized(sid):
        return _deny_project()
    entry = SESSION_STORE.get(sid)
    if not entry:
        # P10-PC2: a direct deliverable link to a saved project must survive a
        # restart exactly like the session page does (P4-1b-1 cold-load; same
        # generic fail-closed redirect when no durable state exists).
        entry = _cold_load_entry(sid)
        if not entry:
            return redirect(url_for("index"))
        SESSION_STORE[sid] = entry
    state = entry["state"]
    # P10-PC2: on a cold-loaded session (committed marker: state.domain is
    # None) assemble the deliverable from the Level-1 deterministic READ-ONLY
    # reconstruction, so the report states the project's TRUE progress instead
    # of the reset minimal state. Display-only: the reconstructed IdeaState is
    # never rehydrated into SESSION_STORE, never mutated, never answerable
    # (the non-resume guard is untouched). Any failure (Level-0 fallback,
    # ContractError, replay limit, store unavailability) keeps the prior
    # behavior — never a 500, never a false reconstruction claim.
    reconstructed_deliverable = False
    if getattr(state, "domain", None) is None:
        try:
            _recon = reconstruct_readonly_state(_get_store(), sid)
            if _recon.review.level == 1 and _recon.state is not None:
                state = _recon.state
                reconstructed_deliverable = True
        except Exception:
            reconstructed_deliverable = False
    package = assemble_deliverable(state)
    eligible = package["_session_meta"]["deliverable_eligible"]
    return render_template(
        "deliverable.html",
        sid=sid,
        package=package,
        eligible=eligible,
        reconstructed_deliverable=reconstructed_deliverable,
        # G-UX-SNAPSHOT-DECISION: single-use, per-sid "Keep current snapshot"
        # acknowledgement, popped here so it renders once after the Post/Redirect/Get
        # and never repeats on a later plain GET. None on every normal load.
        snapshot_kept_ack=ui_text.localize_message(
            entry.pop("_snapshot_kept_ack", None) if entry else None, _current_ui_lang()),
    )


@app.route("/session/<sid>/correct", methods=["POST"])
def correct_answer(sid):
    """PVCG-R4 — EXPLICIT USER CORRECTION / WITHDRAWAL of one prior accepted
    source record, then FULL deterministic replay.

    Implements the authoritative
    `docs/governance/PVCG_R4_C_USER_CORRECTION_AND_DETERMINISTIC_INVALIDATION_CONTRACT.md`.
    PVCG-R4 is the CONFORMANCE owner only: the implementation here consumes the
    EXISTING canonical models (the Increment-2 supersession primitive, the P4-0
    record contract, the P4-1a INSERT-only store, and the P4-2 Level-1
    reconstruction replay). It introduces no parallel state model, no second
    replay engine, no dependency model and no persistence schema change.

    Canonical sequence (§6 C-1/C-5/C-6, §8 RP-1/RP-4, §9 F-1/F-2/F-3):
      ownership -> EXPLICIT record-targeted validation -> staged mint ->
      durable append -> FULL replay of the amended stream -> ATOMIC live-state
      replacement.

    §6 C-1: the correction is explicit and names the prior `record_id`. Nothing
    is ever inferred from retraction wording, sentiment, or any classifier.
    §6 C-2/§7 S-1: the prior record is retained verbatim and never deleted,
    renumbered or rewritten; the new record carries the edge FORWARD (C-3).
    §8 RP-1: recomputation is FULL replay of the whole amended stream — naming
    one record narrows WHICH INPUT was withdrawn, never how much is recomputed.
    §8 RP-4: progression state changes ONLY by replacement with the replayed
    state; this route never assigns `gap.status`, `known_mechanism`,
    `known_problem`, `maturity_level` or `current_stage`.
    §9 F-2/F-3: if replay does not produce a Level-1 state, live memory is left
    exactly as it was and nothing is acknowledged as applied.
    """
    if not _project_authorized(sid):
        return _deny_project()
    entry = SESSION_STORE.get(sid)
    if not entry:
        return redirect(url_for("index"))
    state = entry["state"]

    # NB-2 (Independent External Review) — TOKEN PARITY with the closest
    # functional peer, `submit_answer`. This route mutates accepted durable
    # state, so it takes the SAME mandatory server-issued token, validated by
    # the SAME canonical `_valid_answer_token` (stateless HMAC binding the sid,
    # so a missing / malformed / forged / cross-session token all fail closed).
    # No second CSRF or token model is introduced and `_project_authorized`
    # above is unchanged.
    #
    # Placed FIRST, before parsing, staging, minting or any durable call, so a
    # token failure can never reach the store: no durable correction record, no
    # supersession edge, no replay, and no live-state change. The rejection is
    # generic and discloses nothing about the token mechanism.
    if not _valid_answer_token(sid, request.form.get("answer_token", "")):
        entry["_answer_error"] = CORRECTION_NOT_APPLIED_MESSAGE
        return redirect(url_for("show_session", sid=sid))

    target_id = (request.form.get("supersedes_record_id") or "").strip()
    response = (request.form.get("response") or "").strip()

    # §6 C-8: the same bounded free-text hardening as the answered and
    # non-answer paths, before any state or durable change.
    _input_error = _free_text_error(response, _current_ui_lang())
    if _input_error is not None:
        return (_input_error, 400)
    if not target_id or not response:
        entry["_answer_error"] = CORRECTION_INCOMPLETE_MESSAGE
        return redirect(url_for("show_session", sid=sid))

    # §6 C-5 — fail closed BEFORE anything is staged or stored. The target must
    # be a real, still-active, accepted ANSWER record of THIS project: the
    # amended stream is the answered stream (§14 P-1), so only an answered
    # record can be withdrawn from it.
    target = None
    for record in getattr(state, "assertions", []):
        if record.record_id == target_id:
            target = record
            break
    if (target is None
            or target.disposition != ACTION_ANSWERED
            or getattr(target, "superseded_by", None) is not None):
        entry["_answer_error"] = CORRECTION_NOT_APPLIED_MESSAGE
        return redirect(url_for("show_session", sid=sid))

    # §6 C-6 — staged mint against a THROWAWAY ledger view, so live state is
    # untouched until the durable append commits. The minting seam re-validates
    # (unknown id / self / already-superseded / cycle) and raises with NOTHING
    # appended on any violation.
    import copy
    # Deep-ish copies: `mark_supersession` writes the inverse edge, so the LIVE
    # records must not be reachable from the throwaway view before the durable
    # append commits.
    _minter = IdeaState(idea_id=state.idea_id)
    _minter.assertions = [copy.deepcopy(r) for r in state.assertions]
    try:
        new_record = _minter.record_interaction(
            action=ACTION_ANSWERED, content=response,
            gap_context=target.gap_context, iteration=state.iteration,
            supersedes=[target_id],
        )
    except ValueError:
        entry["_answer_error"] = CORRECTION_NOT_APPLIED_MESSAGE
        return redirect(url_for("show_session", sid=sid))

    # §6 C-7 — a SEPARATE durable idempotency identity, derived from the exact
    # correction event, so a refresh/retry/double-submit produces no second
    # durable record, no second supersession edge and no second replay.
    idem_key = _interaction_idempotency_key(
        sid, "correct:" + target_id, target.gap_context, state.iteration,
        response)
    try:
        _get_store().append_record(sid, new_record, idempotency_key=idem_key)
    except sqlite3.IntegrityError:
        # Never auto-classify an IntegrityError as a duplicate: the same event
        # resubmitted is an idempotent no-op; anything else fails closed.
        try:
            prior = _get_store().record_payload_for_idempotency_key(sid, idem_key)
        except StoreError:
            prior = None
        if prior is None or prior.get("content") != response:
            entry["_answer_error"] = CORRECTION_NOT_APPLIED_MESSAGE
        return redirect(url_for("show_session", sid=sid))
    except StoreError:
        # §9 F-1: durable append unavailable — nothing changed, nothing claimed.
        entry["_answer_error"] = CORRECTION_NOT_APPLIED_MESSAGE
        return redirect(url_for("show_session", sid=sid))

    # §8 RP-1 — FULL deterministic replay of the AMENDED accepted-source stream
    # through the UNCHANGED canonical reconstruction (which itself replays
    # through the UNCHANGED `progression_loop.run_iteration`). No targeted
    # recomputation, no selective patching, no dependency propagation.
    try:
        _recon = reconstruct_readonly_state(_get_store(), sid)
    except Exception:
        _recon = None
    if _recon is None or _recon.review.level != 1 or _recon.state is None:
        # §9 F-2/F-3: replay did not produce a state, so live memory is left
        # EXACTLY as it was — never partially replaced — and the correction is
        # not reported as APPLIED. The durable stream stays valid and
        # re-loadable, so the next load applies it (§9 F-4).
        #
        # NB-1: the durable append ALREADY committed above, so this path must
        # NOT say "Nothing was changed" — that would be factually false about
        # accepted-source history.
        #
        # The promise is deliberately CONDITIONAL, not "on the next load". A
        # project already sitting at MAX_ACCEPTED_ANSWER_REPLAY crosses the
        # bound when the correction append takes the durable stream to
        # limit + 1, and EVERY subsequent reconstruction then raises
        # ReconstructionReplayLimitError — so an unconditional next-load
        # promise would be false there. The bound is checked against the FULL
        # persisted stream on purpose (§8 RP-9: a correction must not become a
        # way to get UNDER the limit), so this is contract-correct behaviour
        # and it is the MESSAGE that must tell the truth, not the bound that
        # must move. Repairing the replay bound is NOT authorized here and is
        # deliberately not done.
        #
        # So the message states only what is true in BOTH cases: the correction
        # was saved, the live view was not updated, and the saved correction is
        # reflected whenever the project can be rebuilt successfully. No
        # durable rollback is claimed, and the contract's persistence ordering
        # is unchanged.
        entry["_answer_error"] = CORRECTION_SAVED_NOT_YET_APPLIED_MESSAGE
        return redirect(url_for("show_session", sid=sid))

    # §8 RP-4 — ATOMIC live-state replacement. The replayed state REPLACES the
    # prior one wholesale; no field of the old state is edited, so no stored gap
    # status is ever moved backward (WPS-001 INV-004 preserved, §8.1/G-3). A
    # weaker outcome is a property of this NEW forward run.
    entry["state"] = _recon.state
    entry["last_result"] = None
    entry.pop("answer_token", None)
    entry["_interaction_ack"] = CORRECTION_APPLIED_ACK
    return redirect(url_for("show_session", sid=sid))


@app.route("/session/<sid>/accept-risk", methods=["POST"])
def accept_risk(sid):
    """RVR-1 (Wave-1 remediation contract, OD-R1) — EXPLICIT owner acceptance of
    the currently served gap as a known risk.

    Governed, never automatic: requires the explicit confirmation field, the
    same server-issued answer token as every state-changing session POST, and
    project authorization. Persist-before-acknowledge (the proven non-answer
    shape): the durable ledger record commits BEFORE the live gap status moves,
    and on any durable failure nothing changes and nothing is acknowledged.
    The gap-status write goes through the ONE canonical lifecycle writer
    (`engine.progression_loop.accept_gap_risk`), which refuses
    MECHANISM_COMPLETENESS and any non-OPEN/PARTIAL gap. WS12 stays
    observation-only — its classification is consumed at deliverable render,
    never here. Truthful UX: the acknowledgement says accepted, not resolved.
    """
    if not _project_authorized(sid):
        return _deny_project()
    entry = SESSION_STORE.get(sid)
    if not entry:
        return redirect(url_for("index"))
    state = entry["state"]
    if not _valid_answer_token(sid, request.form.get("answer_token", "")):
        entry["_answer_error"] = RISK_NOT_ACCEPTED_MESSAGE
        return redirect(url_for("show_session", sid=sid))
    if getattr(state, "domain", None) is None:
        # Cold-loaded non-resumable session: same refusal shape as answers.
        entry["_answer_error"] = RISK_NOT_ACCEPTED_MESSAGE
        return redirect(url_for("show_session", sid=sid))
    gap_type = (request.form.get("gap_type") or "").strip()
    reason = (request.form.get("reason") or "").strip()
    _input_error = _free_text_error(reason, _current_ui_lang())
    if _input_error is not None:
        return (_input_error, 400)
    # Explicit confirmation is mandatory; the accepted gap must be exactly the
    # currently served one (the question the user is looking at), so consent
    # can never silently target a different gap.
    if (request.form.get("risk_confirm") != "yes"
            or not gap_type
            or gap_type != select_next_gap(state)
            or gap_type == _MECH_GAP):
        entry["_answer_error"] = RISK_NOT_ACCEPTED_MESSAGE
        return redirect(url_for("show_session", sid=sid))
    gap = state.get_gap(gap_type)
    if gap is None or gap.status not in ("OPEN", "PARTIAL"):
        entry["_answer_error"] = RISK_NOT_ACCEPTED_MESSAGE
        return redirect(url_for("show_session", sid=sid))
    # Staged mint on a throwaway ledger view (the proven persist-before-
    # acknowledge shape): live state untouched until the durable append commits.
    _minter = IdeaState(idea_id=state.idea_id)
    _minter.assertions = list(state.assertions)
    new_record = _minter.record_interaction(
        action=DISPOSITION_RISK_ACCEPTED, content=reason or "",
        gap_context=gap_type, iteration=state.iteration,
    )
    idem_key = _interaction_idempotency_key(
        sid, DISPOSITION_RISK_ACCEPTED, gap_type, state.iteration, reason or "")
    fingerprint = _answer_fingerprint(
        sid, gap_type, DISPOSITION_RISK_ACCEPTED, reason or "")
    try:
        _get_store().append_record(sid, new_record, idempotency_key=idem_key)
    except sqlite3.IntegrityError:
        try:
            prior = _get_store().record_payload_for_idempotency_key(sid, idem_key)
        except StoreError:
            prior = None
        if prior is not None and _payload_answer_fingerprint(sid, prior) == fingerprint:
            # Same event resubmitted: idempotent no-op, no second acceptance.
            entry["_interaction_ack"] = RISK_ACCEPTED_ACK
            return redirect(url_for("show_session", sid=sid))
        entry["_answer_error"] = RISK_NOT_ACCEPTED_MESSAGE
        return redirect(url_for("show_session", sid=sid))
    except StoreError:
        entry["_answer_error"] = RISK_NOT_ACCEPTED_MESSAGE
        return redirect(url_for("show_session", sid=sid))
    # Durable success — publish: ledger record, then the canonical lifecycle
    # write, then the existing next-gap cascade so the journey advances.
    state.assertions.append(new_record)
    try:
        accept_gap_risk(state, gap_type)
    except ValueError:
        # Unreachable after the validations above; truthful fail-closed anyway:
        # the durable record stands as recorded owner intent, the live status
        # is unchanged, and no acceptance is acknowledged.
        entry["_answer_error"] = RISK_NOT_ACCEPTED_MESSAGE
        return redirect(url_for("show_session", sid=sid))
    _open_next_gap_if_needed(state)
    entry.pop("answer_token", None)
    entry["_interaction_ack"] = RISK_ACCEPTED_ACK
    return redirect(url_for("show_session", sid=sid))


@app.route("/session/<sid>/keep-snapshot", methods=["POST"])
def keep_snapshot(sid):
    if not _project_authorized(sid):
        return _deny_project()
    # G-UX-SNAPSHOT-DECISION: "Keep current snapshot" — a meaningful but bounded
    # post-output decision within the CURRENT temporary session. It records a
    # single-use, per-sid presentation acknowledgement only and preserves
    # Post/Redirect/Get. It NEVER serializes/duplicates/versions the snapshot,
    # writes any durable store, mutates deterministic IdeaState/results/gaps/
    # maturity/transcript/evidence/interaction-ledger, or leaks across session ids.
    # The current deterministic state itself remains the working snapshot.
    entry = SESSION_STORE.get(sid)
    if not entry:
        # Generic behavior: does not disclose whether the session previously existed.
        return redirect(url_for("index"))
    entry["_snapshot_kept_ack"] = KEEP_SNAPSHOT_ACK
    return redirect(url_for("show_deliverable", sid=sid))

# Per-experiment owner-defined success criteria (planning metadata only).
# Field name on the form is "criterion__<experiment_id>". A criterion is a
# user-defined target, never a test result; this route never runs progression,
# never calls submit_answer, and never writes the ILT-002 transcript.
MAX_CRITERION_LENGTH = 1000
_CRITERION_FIELD_PREFIX = "criterion__"


@app.route("/session/<sid>/success-criteria", methods=["GET"])
def success_criteria(sid):
    if not _project_authorized(sid):
        return _deny_project()
    entry = SESSION_STORE.get(sid)
    if not entry:
        return redirect(url_for("index"))
    package = assemble_deliverable(entry["state"])
    plan = package["section_11_prototype_test_plan"]
    return render_template(
        "success_criteria.html",
        sid=sid,
        experiments=plan["items"],
        stale_notice=plan.get("stale_criteria_notice"),
        field_prefix=_CRITERION_FIELD_PREFIX,
        max_length=MAX_CRITERION_LENGTH,
    )


@app.route("/session/<sid>/success-criteria", methods=["POST"])
def save_success_criteria(sid):
    if not _project_authorized(sid):
        return _deny_project()
    entry = SESSION_STORE.get(sid)
    if not entry:
        return redirect(url_for("index"))
    state = entry["state"]
    package = assemble_deliverable(state)
    plan = package["section_11_prototype_test_plan"]
    current_ids = {it["experiment_id"] for it in plan["items"]}

    # Collect submitted criteria, namespaced by experiment_id.
    submitted = {name[len(_CRITERION_FIELD_PREFIX):]: val
                 for name, val in request.form.items()
                 if name.startswith(_CRITERION_FIELD_PREFIX)}

    def _reject(message):
        return render_template(
            "success_criteria.html", sid=sid, experiments=plan["items"],
            stale_notice=plan.get("stale_criteria_notice"),
            field_prefix=_CRITERION_FIELD_PREFIX, max_length=MAX_CRITERION_LENGTH,
            # CF-2 Arabic-localization remainder: `message` is always one of
            # this function's two known English literals below, registered in
            # `ui_text._MESSAGE_KEYS`; localize_message() fails open (passes
            # through unchanged) for anything unregistered.
            error=ui_text.localize_message(message, _current_ui_lang()),
        ), 400

    # Validate before any write: reject unknown/stale ids and over-limit input.
    for eid in submitted:
        if eid not in current_ids:
            return _reject("A submitted experiment is not part of the current plan. "
                           "No changes were saved.")
    for eid, raw in submitted.items():
        if len(raw.strip()) > MAX_CRITERION_LENGTH:
            return _reject(f"A criterion exceeds the {MAX_CRITERION_LENGTH}-character "
                           "limit. No changes were saved.")

    # Apply: trim only; whitespace-only removes; idempotent upsert.
    if not isinstance(getattr(state, "success_criteria", None), dict):
        state.success_criteria = {}
    for eid, raw in submitted.items():
        text = raw.strip()
        if text:
            state.success_criteria[eid] = SuccessCriterion(criterion=text)
        else:
            state.success_criteria.pop(eid, None)
    return redirect(url_for("show_deliverable", sid=sid))


@app.route("/session/<sid>", methods=["POST"])
def submit_answer(sid):
    if not _project_authorized(sid):
        return _deny_project()
    entry = SESSION_STORE.get(sid)
    if not entry:
        return redirect(url_for("index"))
    state = entry["state"]
    # Workstream 4: the structured criticality actions are handled by their
    # own guarded branch (additive; the six frozen dispositions below are
    # untouched). Any OTHER post leaves the criticality step, so its transient
    # UI stage is cleared — recorded confirmations are unaffected.
    if request.form.get("criticality_action") is not None:
        return _handle_criticality_action(entry, state, sid)
    entry.pop("criticality_stage", None)
    entry.pop("criticality_correction", None)
    # Increment 1A: resolve the explicit structured action. Legacy-compatibility
    # rule (chosen, explicit): a submission with NO `action` field is treated as
    # `answered` — exactly the pre-1A behavior, where a non-empty `response` is
    # assessed and an empty one is a no-op. An explicit but UNRECOGNIZED action is
    # rejected with HTTP 400 (never silently assessed), so a malformed client can
    # not smuggle an unknown action into the assessment path.
    action = request.form.get("action", ACTION_ANSWERED).strip().lower()
    if action not in INTERACTION_ACTIONS:
        return ("Unrecognized session action. No change was made.", 400)
    response = request.form.get("response", "").strip()
    # P10-SEC2: bounded free-text hardening for BOTH the answered path and the
    # non-answer action-metadata path — explicit rejection using this route's
    # existing plain-text 400 convention; before any state or durable change.
    _input_error = _free_text_error(response, _current_ui_lang())
    if _input_error is not None:
        return (_input_error, 400)

    if action != ACTION_ANSWERED:
        # Non-answer action: record as additive in-memory metadata only. This
        # path NEVER calls run_iteration, never assesses/scores, never closes or
        # alters a gap, never advances maturity, never satisfies a gate, and never
        # creates an evidence record. select_next_gap() is a read-only selector
        # used only to label which question the action was taken against. Optional
        # owner text is retained verbatim as metadata, not as an assessed response
        # or evidence. The journey truthfully redisplays the same (still-open)
        # question with an honest acknowledgement rather than feigning progress.
        gap_ctx = select_next_gap(state)
        # Increment 2 + PVCG-R1: the disposition record on the IdeaState ledger,
        # now written through the CANONICAL durable seam. It adds NO epistemic
        # movement (no assess/score/gap/maturity/transcript change) — it records,
        # truthfully, that the owner took this non-answer action against the
        # still-open question, and that record now survives a process restart.
        #
        # PERSIST BEFORE ACKNOWLEDGE (the answered path's proven shape): the
        # record is minted against a throwaway ledger view so LIVE state is
        # untouched until the durable append commits. A metadata-only action
        # changes nothing else on the state, so publication is exactly the one
        # ledger append — no whole-state swap and no object identity is
        # disturbed. On any durable failure live memory is left unchanged and
        # nothing is acknowledged.
        _minter = IdeaState(idea_id=state.idea_id)
        _minter.assertions = list(state.assertions)
        new_record = _minter.record_interaction(
            action=action, content=response or "",
            gap_context=gap_ctx, iteration=state.iteration,
        )
        idem_key = _interaction_idempotency_key(
            sid, action, gap_ctx, state.iteration, response or "")
        fingerprint = _answer_fingerprint(sid, gap_ctx, action, response or "")
        try:
            _get_store().append_record(sid, new_record, idempotency_key=idem_key)
        except sqlite3.IntegrityError:
            # Never auto-classify an IntegrityError as a duplicate: reload and
            # confirm the SAME accepted content under the SAME idempotency
            # identity before treating a retry as an idempotent no-op.
            try:
                prior = _get_store().record_payload_for_idempotency_key(
                    sid, idem_key)
            except StoreError:
                prior = None
            if prior is not None and _payload_answer_fingerprint(sid, prior) == fingerprint:
                # Same event resubmitted (refresh / retry / double-submit): no
                # second durable truth and no second in-memory record.
                entry["_interaction_ack"] = _NON_ANSWER_ACK[action]
                return redirect(url_for("show_session", sid=sid))
            entry["_answer_error"] = INTERACTION_NOT_SAVED_MESSAGE
            return redirect(url_for("show_session", sid=sid))
        except StoreError:
            # Durable append unavailable (including an absent project envelope):
            # fail closed; live memory unchanged; nothing is acknowledged.
            entry["_answer_error"] = INTERACTION_NOT_SAVED_MESSAGE
            return redirect(url_for("show_session", sid=sid))
        # Durable success — publish the single ledger delta into LIVE memory.
        state.assertions.append(new_record)
        entry.setdefault("interaction_actions", []).append({
            "action": action,
            "iteration": state.iteration,
            "gap_type": gap_ctx,
            "text": response or None,
        })
        entry["_interaction_ack"] = _NON_ANSWER_ACK[action]
        return redirect(url_for("show_session", sid=sid))

    # ANSWERED — P4-1b-2a (G-P4-1B-2A-B3-CONTRACT-AMENDMENT-01, OPTION A):
    # a mandatory server-issued token, then a STAGED evaluation whose result is
    # published to live memory only after a durable append succeeds
    # (persist-before-acknowledge). record_id stays rec_N; a SEPARATE durable
    # idempotency identity is the durable duplicate backstop.
    token = request.form.get("answer_token", "")
    if not _valid_answer_token(sid, token):
        # No tokenless fallback: a missing/malformed/forged/cross-session token
        # fails closed generically — no assessment, no durable append, no
        # acceptance, and no disclosure of the token mechanism.
        entry["_answer_error"] = ANSWER_NOT_SAVED_MESSAGE
        return redirect(url_for("show_session", sid=sid))
    if getattr(state, "domain", None) is None:
        # A cold-loaded session (P4-1b-1) restores the durable ledger + fresh
        # readiness ONLY — it deliberately does not restore the runtime domain or
        # progression, and continuing to answer it is complete session resume
        # (P4-2), which is out of scope here. Refuse a NEW answer generically and
        # fail closed (no assessment, no durable append, no 500/traceback) rather
        # than operating on a non-resumable state. The durable evidence remains
        # viewable; it is simply not extendable in this bounded increment.
        entry["_answer_error"] = ANSWER_NOT_SAVED_MESSAGE
        return redirect(url_for("show_session", sid=sid))
    if response:
        import copy
        from datetime import datetime
        # C1 staging: evaluate on a CLONE and publish only after a durable append
        # succeeds. On any durable failure the clone is discarded and live memory
        # is left unchanged (no partial publication).
        staged = copy.deepcopy(state)
        targeted_gap = select_next_gap(staged)   # gap this answer addresses (pre-iteration)
        result = run_iteration(staged, response)
        # Increment 2 provenance preserved (OWNER_STATED, UNVALIDATED, current
        # leading evidence quality) — now created on the staged copy.
        new_record = staged.record_interaction(
            action=ACTION_ANSWERED, content=response,
            gap_context=targeted_gap, iteration=staged.iteration,
            quality=getattr(getattr(staged, "known_mechanism", None), "quality", None)
                    or getattr(getattr(staged, "known_problem", None), "quality", None),
        )
        idem_key = _answer_idempotency_key(sid, token)
        fingerprint = _answer_fingerprint(sid, targeted_gap, ACTION_ANSWERED, response)
        try:
            _get_store().append_record(sid, new_record, idempotency_key=idem_key)
        except sqlite3.IntegrityError:
            # C3: never auto-classify an IntegrityError as a duplicate. Reload and
            # confirm the SAME accepted content under the SAME idempotency identity
            # before treating a retry as an idempotent no-op; a same-token /
            # different-content submission fails closed.
            try:
                prior = _get_store().record_payload_for_idempotency_key(sid, idem_key)
            except StoreError:
                prior = None
            if prior is not None and _payload_answer_fingerprint(sid, prior) == fingerprint:
                # Idempotent no-op: no second event, no second progression, no
                # reconstructed result, no replay claim. Redirect to the session.
                return redirect(url_for("show_session", sid=sid))
            entry["_answer_error"] = ANSWER_NOT_SAVED_MESSAGE
            return redirect(url_for("show_session", sid=sid))
        except StoreError:
            # Durable append unavailable: fail closed; live memory unchanged.
            entry["_answer_error"] = ANSWER_NOT_SAVED_MESSAGE
            return redirect(url_for("show_session", sid=sid))
        # Durable success — publish the staged evaluation into the LIVE session
        # object IN PLACE (preserving its identity) only now that the durable
        # append has committed (persist-before-acknowledge). On any durable
        # failure above we returned early without ever mutating live memory.
        # G-SC0 (R6): no verbatim disk write; the transcript stays in memory.
        state.__dict__.update(staged.__dict__)
        entry["last_result"] = result
        entry["transcript"].append({
            "session_id": sid,
            "iteration": staged.iteration,
            "question":  entry.get("last_question", ""),
            "response":  response,
            "domain":    getattr(staged, "domain", None),
            "timestamp": datetime.utcnow().isoformat() + "Z",
        })
        # Consume the token (single-use for acceptance); the next render issues a
        # fresh one, so distinct submissions get distinct idempotency identities.
        entry.pop("answer_token", None)
        # Draft Level 2 (G-DRAFT-L2-...-IMPLEMENTATION-01): a truthful, one-shot
        # ACCEPTED signal, set ONLY here after a durable append committed and the
        # staged evaluation was published. The next session render exposes it once
        # (then pops it) so the client-side local-draft script can clear the
        # matching local draft. It is set on NO failure/ambiguous path; it never
        # persists, and it changes no engine/durable/accepted-answer semantics.
        entry["_answer_accepted"] = True
    else:
        # G-UX-ANSWER-VALIDATION: answered chosen but the response is empty. Set a
        # SINGLE-USE transient and preserve Post/Redirect/Get. The empty string is
        # never assessed/scored/appended. The token is NOT consumed — it is
        # retained across this validation-error re-render (owner decision).
        entry["_answer_error"] = ANSWER_REQUIRED_MESSAGE
    return redirect(url_for("show_session", sid=sid))


# ---------------------------------------------------------------------------
# FDC-001 first increment — Technical Decision Workspace.
# In-memory only. Distinct from SESSION_STORE; imports no session_store; writes
# no durable state; performs no benchmark run. Activation-only lane surface.
# ---------------------------------------------------------------------------
from engine import decision_workspace as fdc001_dw

# Dedicated in-memory store for FDC-001 decision records (non-durable).
FDC001_DECISIONS = {}

# P10-D2: app-layer ownership metadata ONLY (no change to
# engine/decision_workspace.py, no durable persistence, no new identity
# system). did -> authenticated owner_account_id, or None for an anonymously
# created decision (whose access is instead bound to the creating browser's
# own signed Flask session, tracked under "fdc001_created" below).
FDC001_DECISION_OWNERS = {}


def _fdc001_authorized(did):
    """True iff the current caller may access decision ``did``. An owned
    decision requires the authenticated, active account that created it
    (server-side account_id == stored owner); an anonymous (owner is None)
    decision requires ``did`` to be present in the CREATING browser's own
    signed session ("fdc001_created") — a different anonymous session with
    only the same ``did`` is never authorized. Fails closed on any missing/
    malformed/unexpected state. Bare ``did`` possession is NEVER sufficient."""
    if did not in FDC001_DECISION_OWNERS:
        return False
    owner = FDC001_DECISION_OWNERS[did]
    if owner is not None:
        account = _current_account()
        return account is not None and account["account_id"] == owner
    return did in flask_session.get("fdc001_created", [])


def _fdc001_get_authorized(did):
    """Return the FDC001_DECISIONS record for ``did`` iff it exists AND the
    current caller is authorized for it; otherwise None (fails closed)."""
    record = FDC001_DECISIONS.get(did)
    if record is None or not _fdc001_authorized(did):
        return None
    return record


def _deny_fdc001():
    """One generic, non-enumerating denial for every failed Decision Workspace
    access (missing, non-owner, foreign-anonymous-session) — byte-identical to
    the pre-existing "start a new decision" redirect, so a denial never
    discloses whether the decision exists."""
    return redirect(url_for("decision_workspace_start"))


# P10-SEC4: the engine's deterministic DecisionError diagnostics legitimately
# %r-echo the offending enum/id value. Those fields are user-controlled and are
# NOT free-text-guarded (deliberately — they are ids/enums, not content), so a
# pathological value can be as large as the transport bound allows and would be
# reflected verbatim (autoescaped, but still kilobytes of junk) into the 400
# page. The bound below applies to the RENDERED copy ONLY: the engine seam and
# its exception messages remain byte-complete, short legitimate diagnostics
# render verbatim, and truncation is always explicit — never silent.
_DW_ERROR_ECHO_BOUND = 300


def _dw_bounded_error(prefix, exc):
    """Return the route family's conventional '<Prefix>: <engine message>'
    error string with the user-reflected copy bounded at
    ``_DW_ERROR_ECHO_BOUND`` characters (explicit truncation marker)."""
    message = "%s: %s" % (prefix, exc)
    if len(message) > _DW_ERROR_ECHO_BOUND:
        message = message[:_DW_ERROR_ECHO_BOUND] + " … [diagnostic truncated]"
    return message


def _dw_free_text_reject(record, *field_names):
    """P10-SEC3: bounded free-text guard for Decision Workspace form fields —
    reuses the canonical P10-SEC2 helper `_free_text_error` (explicit
    rejection only: MAX_FREE_TEXT_CHARS cap + NUL rejection; never truncation,
    stripping, or normalization; Arabic/Unicode/multiline untouched) and this
    route family's EXISTING error convention. Runs AFTER the non-enumerating
    ownership denial and BEFORE any engine call, so a rejection mutates
    nothing and discloses nothing. Returns a 400 response or None."""
    for name in field_names:
        err = _free_text_error(request.form.get(name, ""), _current_ui_lang())
        if err is not None:
            return _render_decision_workspace(record, error=err, status=400)
    return None


@app.route("/decision-workspace", methods=["GET"])
def decision_workspace_start():
    record = fdc001_dw.DecisionRecord()
    did = record.decision_id
    FDC001_DECISIONS[did] = record
    account = _current_account()
    if account is not None:
        FDC001_DECISION_OWNERS[did] = account["account_id"]
    else:
        FDC001_DECISION_OWNERS[did] = None
        created = flask_session.get("fdc001_created", [])
        created.append(did)
        flask_session["fdc001_created"] = created
    return redirect(url_for("decision_workspace_view", did=did))


def _render_decision_workspace(record, error=None, status=200):
    """Render the workspace, optionally with a bounded user-visible validation
    error. The error is a concise message only — never a traceback."""
    html = render_template(
        "decision_workspace.html",
        view=record.to_record_dict(),
        candidate_names=list(fdc001_dw.CANDIDATE_NAMES),
        limitations=list(fdc001_dw.EXPORT_LIMITATIONS),
        error=error,
    )
    return (html, status)


@app.route("/decision-workspace/<did>", methods=["GET"])
def decision_workspace_view(did):
    record = _fdc001_get_authorized(did)
    if record is None:
        return _deny_fdc001()
    return _render_decision_workspace(record)


@app.route("/decision-workspace/<did>/input", methods=["POST"])
def decision_workspace_add_input(did):
    record = _fdc001_get_authorized(did)
    if record is None:
        return _deny_fdc001()
    _rej = _dw_free_text_reject(record, "text", "provenance")
    if _rej is not None:
        return _rej
    candidate_id = request.form.get("candidate_id", "").strip()
    candidate_ids = [candidate_id] if candidate_id else []
    try:
        record.add_input(
            request.form.get("text", "").strip(),
            request.form.get("claim_class", "").strip(),
            request.form.get("provenance", "").strip(),
            decision_relevant=request.form.get("decision_relevant") == "on",
            candidate_ids=candidate_ids,
        )
    except fdc001_dw.DecisionError as exc:
        # The record is left unmodified; show a concise bounded error.
        return _render_decision_workspace(
            record, error=_dw_bounded_error("Input rejected", exc), status=400)
    return redirect(url_for("decision_workspace_view", did=did))


@app.route("/decision-workspace/<did>/constraint", methods=["POST"])
def decision_workspace_add_constraint(did):
    record = _fdc001_get_authorized(did)
    if record is None:
        return _deny_fdc001()
    _rej = _dw_free_text_reject(record, "text", "provenance")
    if _rej is not None:
        return _rej
    candidate_id = request.form.get("candidate_id", "").strip()
    candidate_ids = [candidate_id] if candidate_id else []
    try:
        record.add_constraint(
            request.form.get("text", "").strip(),
            request.form.get("constraint_strength", "").strip(),
            request.form.get("provenance", "").strip(),
            confirmed=request.form.get("confirmed") == "on",
            candidate_ids=candidate_ids,
        )
    except fdc001_dw.DecisionError as exc:
        return _render_decision_workspace(
            record, error=_dw_bounded_error("Constraint rejected", exc), status=400)
    return redirect(url_for("decision_workspace_view", did=did))


@app.route("/decision-workspace/<did>/gap", methods=["POST"])
def decision_workspace_gap_action(did):
    record = _fdc001_get_authorized(did)
    if record is None:
        return _deny_fdc001()
    _rej = _dw_free_text_reject(record, "rationale")
    if _rej is not None:
        return _rej
    action = request.form.get("action", "").strip()
    gap_id = request.form.get("gap_id", "").strip()
    try:
        if action in ("resolve", "reclassify"):
            # FDC-002 user-facing route guard (reconciled contract, spec §12.1 /
            # guarantee #31): the legacy bare-text resolve/reclassify route must
            # NOT clear or reclassify a physical/calibration blocker. Reject
            # BEFORE invoking the legacy domain mutation, so the rejection is
            # bounded (HTTP 400) and atomic — no gap, revision, history,
            # readiness, blocker, or change-impact mutation. The FDC-002
            # evidence-assessment workflow is the sole user-facing path for that
            # blocker. (gap_blocker_code is read-only and raises for unknown ids.)
            if (record.gap_blocker_code(gap_id)
                    == fdc001_dw.MISSING_PHYSICAL_OR_CALIBRATION_INFORMATION):
                return _render_decision_workspace(
                    record,
                    error=("Gap action rejected: the "
                           "missing_physical_or_calibration_information blocker "
                           "can be cleared only through the evidence-assessment "
                           "workflow (record evidence, then assess and decide), "
                           "not this route."),
                    status=400)
            if action == "resolve":
                record.resolve_gap(gap_id)
            else:
                record.reclassify_gap(
                    gap_id, request.form.get("rationale", "").strip())
        else:
            raise fdc001_dw.DecisionError("unknown gap action: %r" % action)
    except fdc001_dw.DecisionError as exc:
        return _render_decision_workspace(
            record, error=_dw_bounded_error("Gap action rejected", exc), status=400)
    return redirect(url_for("decision_workspace_view", did=did))


@app.route("/decision-workspace/<did>/evidence", methods=["POST"])
def decision_workspace_add_evidence(did):
    record = _fdc001_get_authorized(did)
    if record is None:
        return _deny_fdc001()
    _rej = _dw_free_text_reject(record, "text", "provenance", "method",
                                "source_label", "evidence_version",
                                "limitations")
    if _rej is not None:
        return _rej
    candidate_id = request.form.get("candidate_id", "").strip()
    candidate_ids = [candidate_id] if candidate_id else []
    try:
        # verification_status is NEVER read from the form: it is system-set to
        # `unverified` inside add_evidence (§7.4). Any posted value is ignored.
        record.add_evidence(
            request.form.get("gap_id", "").strip(),
            request.form.get("text", "").strip(),
            request.form.get("claim_class", "").strip(),
            request.form.get("provenance", "").strip(),
            method=request.form.get("method", "").strip() or None,
            source_label=request.form.get("source_label", "").strip() or None,
            evidence_version=request.form.get("evidence_version", "").strip() or None,
            limitations=request.form.get("limitations", "").strip() or None,
            candidate_ids=candidate_ids,
            decision_relevant=request.form.get("decision_relevant") == "on",
        )
    except fdc001_dw.DecisionError as exc:
        return _render_decision_workspace(
            record, error=_dw_bounded_error("Evidence rejected", exc), status=400)
    return redirect(url_for("decision_workspace_view", did=did))


@app.route("/decision-workspace/<did>/gap-assessment", methods=["POST"])
def decision_workspace_gap_assessment(did):
    record = _fdc001_get_authorized(did)
    if record is None:
        return _deny_fdc001()
    _rej = _dw_free_text_reject(record, "rationale", "resolution_rationale")
    if _rej is not None:
        return _rej
    evidence_ids = [e.strip() for e in request.form.getlist("evidence_ids")
                    if e.strip()]
    try:
        record.assess_gap(
            request.form.get("gap_id", "").strip(),
            evidence_ids,
            request.form.get("assessment", "").strip(),
            request.form.get("rationale", "").strip(),
            request.form.get("resolution_decision", "").strip(),
            resolution_rationale=(
                request.form.get("resolution_rationale", "").strip() or None),
        )
    except fdc001_dw.DecisionError as exc:
        return _render_decision_workspace(
            record, error=_dw_bounded_error("Gap assessment rejected", exc), status=400)
    return redirect(url_for("decision_workspace_view", did=did))


@app.route("/decision-workspace/<did>/preference", methods=["POST"])
def decision_workspace_preference(did):
    record = _fdc001_get_authorized(did)
    if record is None:
        return _deny_fdc001()
    _rej = _dw_free_text_reject(record, "rationale")
    if _rej is not None:
        return _rej
    action = request.form.get("action", "").strip()
    try:
        if action == "set":
            record.set_owner_preference(
                request.form.get("candidate_id", "").strip(),
                request.form.get("rationale", "").strip() or None)
        elif action == "clear":
            record.clear_owner_preference()
        else:
            raise fdc001_dw.DecisionError("unknown preference action: %r" % action)
    except fdc001_dw.DecisionError as exc:
        return _render_decision_workspace(
            record, error=_dw_bounded_error("Preference action rejected", exc), status=400)
    return redirect(url_for("decision_workspace_view", did=did))


@app.route("/decision-workspace/<did>/candidate", methods=["POST"])
def decision_workspace_dispose_candidate(did):
    record = _fdc001_get_authorized(did)
    if record is not None:
        _rej = _dw_free_text_reject(record, "disposition_reason",
                                    "disposition_basis")
        if _rej is not None:
            return _rej
    if record is None:
        return _deny_fdc001()
    try:
        record.dispose_candidate(
            request.form.get("candidate_id", "").strip(),
            request.form.get("option_status", "").strip(),
            request.form.get("disposition_reason", "").strip(),
            request.form.get("disposition_basis", "").strip(),
        )
    except fdc001_dw.DecisionError as exc:
        return _render_decision_workspace(
            record, error=_dw_bounded_error("Candidate disposition rejected", exc), status=400)
    return redirect(url_for("decision_workspace_view", did=did))


@app.route("/decision-workspace/<did>/export", methods=["GET"])
def decision_workspace_export(did):
    record = _fdc001_get_authorized(did)
    if record is None:
        return _deny_fdc001()
    # Deterministic, safe attachment filename derived from the decision id.
    filename = "fdc001-decision-%s.json" % record.decision_id
    response = app.response_class(
        response=record.to_json(),
        status=200,
        mimetype="application/json",
    )
    response.headers["Content-Disposition"] = (
        'attachment; filename="%s"' % filename)
    return response


def _run_config():
    """Explicit run configuration for the bounded single-threaded P4-1b-1 MVP
    (G-P4-1B-1-AMEND-01 / D-P4-1B-1-AMEND-01). `threaded` is pinned **False** so
    requests are served one at a time, matching the single application-scoped
    `SqliteRecordStore` connection (which is thread-bound); the runtime must NOT
    rely on Flask's default threaded serving. This is a bounded MVP decision, NOT
    a claim that Flask's built-in server is a production deployment architecture;
    multi-worker/threaded topology is deferred. No `engine/record_store.py`
    change and no `check_same_thread` override is used. Exposed as a small helper
    so the selected serving boundary is inspectable and testable."""
    return {
        "debug": _debug_enabled(),
        "host": _resolve_host(),
        "port": 5000,
        "threaded": False,
    }


# P7-I2 (established contract, PR #405): mount the versioned read-only public
# API blueprint. Registration only — all API behaviour lives in web/api_v1.py.
from web.api_v1 import api_v1_bp as _api_v1_bp  # noqa: E402  (mount-time import)
app.register_blueprint(_api_v1_bp)


if __name__ == "__main__":
    app.run(**_run_config())
