"""P5-1 — Account & Credential Foundation: pure credential helpers.

Deterministic, side-effect-free helpers for the Phase 5 account foundation
(gate G-P5-1-ACCOUNT-CREDENTIAL-FOUNDATION-IMPLEMENTATION-01, formal contract
G-P5-FORMAL-CONTRACT-AND-CONTINUING-AUTHORIZATION-01, Option A). No persistence,
no Flask, no network, no login/session. Uses only Werkzeug (already a dependency)
and the Python standard library — NO new runtime dependency.

Boundaries: email is NEVER the durable identifier (the store uses an immutable
UUID); passwords are hashed with Werkzeug scrypt and never returned in reversible
form; raw tokens are generated here but only their hash is ever persisted.
"""
import re
import secrets
import hashlib
import uuid

from werkzeug.security import generate_password_hash, check_password_hash

# Bounded password policy (contract §6): a usability-first minimum length with a
# hard maximum so a pathological input cannot be hashed unbounded. No forced
# composition rules; the password is never silently trimmed or altered.
MIN_PASSWORD_LENGTH = 12
MAX_PASSWORD_LENGTH = 1024
MAX_EMAIL_LENGTH = 254   # RFC-practical bound; not a full RFC validator

_PASSWORD_METHOD = "scrypt"
# A deliberately narrow, bounded email shape check (NOT full RFC 5322): exactly one
# "@", non-empty local and domain parts, at least one dot in the domain, no spaces.
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def normalize_email(email):
    """One deterministic normalization rule (contract §5): trim surrounding
    whitespace and lowercase the address. The local-part content is otherwise
    preserved — NO dot removal, NO plus-addressing stripping, NO provider-specific
    transforms, and no equivalence inference beyond this."""
    if email is None:
        return ""
    return email.strip().lower()


def is_valid_email(email_normalized):
    """Bounded structural validity of an ALREADY-normalized email. Fail closed on
    empty, over-length, spaces, or a shape outside the narrow bounded pattern."""
    if not email_normalized or len(email_normalized) > MAX_EMAIL_LENGTH:
        return False
    return bool(_EMAIL_RE.match(email_normalized))


def validate_password(password):
    """Return (ok, reason). Enforce the bounded minimum policy WITHOUT altering the
    value: reject empty/None, too short, or too long. No composition requirements."""
    if not isinstance(password, str) or password == "":
        return False, "empty"
    if len(password) < MIN_PASSWORD_LENGTH:
        return False, "too_short"
    if len(password) > MAX_PASSWORD_LENGTH:
        return False, "too_long"
    return True, "ok"


def hash_password(password):
    """Werkzeug scrypt hash. The plaintext is never stored, logged, or returned;
    only this one-way hash is persisted."""
    return generate_password_hash(password, method=_PASSWORD_METHOD)


def verify_password(password_hash, password):
    """Constant-time-ish verification via Werkzeug. Internal primitive only —
    P5-1 exposes NO login flow."""
    if not password_hash or password is None:
        return False
    try:
        return check_password_hash(password_hash, password)
    except Exception:
        return False


def new_account_id():
    """Immutable, durable internal account identifier — a UUID, NOT the email."""
    return "acct_" + uuid.uuid4().hex


def new_token_id():
    return "etok_" + uuid.uuid4().hex


def new_raw_token():
    """A cryptographically secure raw token. It is placed ONLY in the outbound
    (dev-sink) email; it is never stored, never logged, and never returned in an
    ordinary HTTP response. Only ``hash_token`` output is persisted."""
    return secrets.token_urlsafe(32)


def hash_token(raw_token):
    """Bounded one-way hash of a raw token for at-rest storage (SHA-256 hex)."""
    return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()


def email_digest(email_normalized):
    """A privacy-preserving, non-reversible digest of a normalized email, for
    rate-limit subject keys and correlation — so raw email need not be used as a
    key. Truncated SHA-256 hex."""
    return hashlib.sha256(("p5-email:" + (email_normalized or "")).encode("utf-8")).hexdigest()[:32]
