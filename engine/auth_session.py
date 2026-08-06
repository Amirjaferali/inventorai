"""P5-2 — Authenticated-session pure helpers (no Flask, no persistence, no network).

Deterministic, side-effect-free helpers for the authenticated-session model
(gate G-P5-2-AUTH-SESSIONS-VERIFIED-EMAIL-RECOVERY-IMPLEMENTATION-01). The web
layer stores the session dict returned here inside Flask's SIGNED cookie session
(distinct from the project ``sid``) and calls ``validate_session`` on every
authenticated request. Only bounded identity/session metadata is carried:
``account_id``, ``session_epoch``, ``issued_at``, ``last_seen_at``,
``absolute_expires_at`` and a CSRF token. NEVER the email, password hash, any
verification/reset token, or project data.

All time arithmetic is done on timezone-naive UTC ``datetime`` objects supplied
by the caller (testable); timestamps are serialised as canonical fixed-width
ISO-8601 UTC strings so lexicographic comparison stays monotonic.
"""
import hmac
import secrets
from datetime import datetime, timedelta

# Session lifetime bounds (contract §6): idle 2 hours, absolute 14 days.
IDLE_TIMEOUT_SECONDS = 2 * 60 * 60
ABSOLUTE_TIMEOUT_SECONDS = 14 * 24 * 60 * 60

# Bounded set of keys allowed in the authenticated session cookie. Anything else
# is neither written nor trusted.
SESSION_KEYS = ("account_id", "session_epoch", "issued_at", "last_seen_at",
                "absolute_expires_at", "csrf")


def iso(dt):
    """Canonical fixed-width UTC ISO-8601 (always 6-digit microseconds) so string
    comparison of timestamps is monotonic."""
    return dt.strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"


def parse(value):
    """Parse a canonical ISO string back to a naive UTC datetime. Returns None on
    any malformed input (fail closed)."""
    if not value or not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value.rstrip("Z"))
    except (ValueError, TypeError):
        return None


def new_csrf_token():
    """An unpredictable, URL-safe CSRF token bound to the session it is stored in."""
    return secrets.token_urlsafe(32)


def csrf_matches(expected, provided):
    """Constant-time CSRF comparison. False on any missing/empty/non-str side."""
    if not expected or not provided:
        return False
    if not isinstance(expected, str) or not isinstance(provided, str):
        return False
    return hmac.compare_digest(expected, provided)


def build_session(account_id, session_epoch, now_dt):
    """Build a FRESH authenticated session dict (used on login and on rotation).
    A new CSRF token is minted, so any pre-login cookie state is fully replaced
    (session-fixation defence). ``absolute_expires_at`` is fixed at issuance."""
    return {
        "account_id": account_id,
        "session_epoch": int(session_epoch),
        "issued_at": iso(now_dt),
        "last_seen_at": iso(now_dt),
        "absolute_expires_at": iso(now_dt + timedelta(seconds=ABSOLUTE_TIMEOUT_SECONDS)),
        "csrf": new_csrf_token(),
    }


def validate_session(session, account, now_dt):
    """Validate an authenticated session against the live account and the current
    time. Returns ``(ok, reason)``. Fails closed on anything missing or stale:

    - ``no_session``     — no/blank authenticated session
    - ``malformed``      — missing/undecodable required fields
    - ``no_account``     — account no longer exists
    - ``inactive``       — account status is not ``active`` (disabled/deleted/other)
    - ``epoch_mismatch`` — ``session_epoch`` revoked (logout-all / password reset)
    - ``absolute_expired``/``idle_expired`` — lifetime bounds exceeded
    """
    if not session or not session.get("account_id"):
        return False, "no_session"
    for key in ("session_epoch", "issued_at", "last_seen_at", "absolute_expires_at"):
        if key not in session:
            return False, "malformed"
    if account is None:
        return False, "no_account"
    if account.get("status") != "active":
        return False, "inactive"
    if account.get("account_id") != session.get("account_id"):
        return False, "no_account"
    try:
        if int(session["session_epoch"]) != int(account["session_epoch"]):
            return False, "epoch_mismatch"
    except (TypeError, ValueError):
        return False, "malformed"
    absolute = parse(session.get("absolute_expires_at"))
    last_seen = parse(session.get("last_seen_at"))
    if absolute is None or last_seen is None:
        return False, "malformed"
    if now_dt >= absolute:
        return False, "absolute_expired"
    if (now_dt - last_seen).total_seconds() > IDLE_TIMEOUT_SECONDS:
        return False, "idle_expired"
    return True, "ok"


def touch_session(session, now_dt):
    """Return a copy of the session with ``last_seen_at`` advanced to now (idle
    window slides). ``absolute_expires_at`` is never extended."""
    updated = dict(session)
    updated["last_seen_at"] = iso(now_dt)
    return updated
