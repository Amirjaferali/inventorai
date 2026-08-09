"""P8-I2 — Commercial Usage Quota Service (Flask-free, fail-closed seam).

The single canonical governed-usage seam over the P8-I1 entitlement layer:

    consume_quota(account_store, account_id, meter, amount=1, now=None,
                  idempotency_key=None) -> QuotaDecision
    evaluate_quota(account_store, account_id, meter, now=None) -> QuotaDecision

Canonical flow: Account/Principal → Plan Identity → Entitlement Evaluation
(P8-I1 seam, FIRST) → Commercial Quota Evaluation → Governed Capability Access.
Quota is distinct from entitlement: entitlement asks *may this identity use the
capability at all?*; quota asks *if entitled, how much governed usage remains?*

Fail-closed for every non-authoritative state (missing/disabled/deleted account,
not entitled, unknown/malformed assignment, malformed quota policy, unknown
meter). Denied/failed states NEVER consume. Consumption is atomic (evaluate +
increment + idempotency write in one account-store ``BEGIN IMMEDIATE`` critical
section) so concurrent final-slot requests cannot oversubscribe a hard cap; the
optional idempotency key prevents retry double-counting; a same-key replay with a
different amount is a conflict (never a second count).

Quota subject = (account_id, meter) — the commercial account principal, never a
browser session or API credential. Effective policy is DERIVED at evaluation from
the versioned code catalog (no per-account snapshot). OD-N: this module imports
only the commercial layer (plan_catalog + entitlement_service); the deterministic
core imports nothing here, so quota state can never influence technical truth.
This module and account_store never change security rate-limit, API scope, or
credential-revocation semantics (credential revocation stays plan/quota-independent).
Commercial usage evidence is NOT a financial/invoice/provider ledger.
"""

from engine import plan_catalog
from engine import entitlement_service


class QuotaError(Exception):
    """Fail-closed quota error (invalid amount, malformed policy, same-key/
    different-amount conflict propagated by the caller path). Kept generic."""


OUTCOME_ALLOWED = "allowed"
OUTCOME_DENIED_NOT_ENTITLED = "denied_not_entitled"
OUTCOME_DENIED_EXHAUSTED = "denied_quota_exhausted"
OUTCOME_DENIED_INVALID = "denied_invalid_account_or_commercial_state"
OUTCOME_INTERNAL_FAIL_CLOSED = "internal_fail_closed"


class QuotaDecision:
    """Machine-level quota decision. ``allowed`` is the only authorization
    signal; ``used``/``remaining`` are diagnostic (``remaining`` is ``None`` for
    an UNLIMITED policy)."""

    __slots__ = ("outcome", "allowed", "used", "remaining", "meter", "plan_identity")

    def __init__(self, outcome, allowed, used, remaining, meter, plan_identity):
        self.outcome = outcome
        self.allowed = allowed
        self.used = used
        self.remaining = remaining
        self.meter = meter
        self.plan_identity = plan_identity

    def __repr__(self):
        return ("QuotaDecision(outcome=%r, allowed=%r, used=%r, remaining=%r, "
                "meter=%r, plan_identity=%r)" % (self.outcome, self.allowed,
                self.used, self.remaining, self.meter, self.plan_identity))


def _validate_amount(amount):
    if not isinstance(amount, int) or isinstance(amount, bool) or amount <= 0:
        raise QuotaError("invalid consumption amount: %r" % (amount,))


def _window_key(window, now):
    """Deterministic durable window key from the injectable time source. Lifetime
    → a constant; fixed → a bucket of ``now`` (epoch seconds) by window length."""
    if window["kind"] == "lifetime":
        return "lifetime"
    if not isinstance(now, int) or isinstance(now, bool):
        raise QuotaError("fixed window requires an integer epoch time source")
    seconds = window["seconds"]
    return "fixed:%d:%d" % (seconds, now // seconds)


def _resolve(account_store, account_id, meter):
    """Resolve (plan_identity, policy, window) for an entitled active account, or
    raise a fail-closed signal. Returns a tuple; the caller maps exceptions to a
    fail-closed decision. Entitlement is evaluated FIRST (P8-I1 seam)."""
    capability = plan_catalog.meter_capability(meter)          # unknown meter → CatalogError
    ent = entitlement_service.evaluate_entitlement(account_store, account_id, capability)
    if not ent.allow:
        return ("not_entitled", ent.plan_identity, None, None)
    policy = plan_catalog.quota_policy(*ent.plan_identity, meter=meter)   # malformed → CatalogError
    window_key_unused = None
    return ("entitled", ent.plan_identity, policy, window_key_unused)


def _decide(account_store, account_id, meter, amount, now, idempotency_key, mutate):
    try:
        _validate_amount(amount)
    except QuotaError:
        raise                                                  # amount errors surface (tests pin)
    try:
        state, plan_identity, policy, _ = _resolve(account_store, account_id, meter)
    except entitlement_service.EntitlementError:
        return QuotaDecision(OUTCOME_DENIED_INVALID, False, None, None, meter, None)
    except plan_catalog.CatalogError:
        return QuotaDecision(OUTCOME_DENIED_INVALID, False, None, None, meter, None)
    if state == "not_entitled":
        return QuotaDecision(OUTCOME_DENIED_NOT_ENTITLED, False, None, None,
                             meter, plan_identity)
    limit = policy["limit"]
    unlimited = limit is plan_catalog.UNLIMITED
    try:
        window_key = _window_key(policy["window"], now)
    except QuotaError:
        raise
    if not mutate:
        used = account_store.get_commercial_usage(account_id, meter, window_key)
        if not unlimited and used >= limit:
            # Read-only path must NOT fail open: an already-exhausted (or explicit
            # zero-limit) finite quota answers "another use is NOT allowed".
            return QuotaDecision(OUTCOME_DENIED_EXHAUSTED, False, used, 0,
                                 meter, plan_identity)
        remaining = None if unlimited else max(0, limit - used)
        return QuotaDecision(OUTCOME_ALLOWED, True, used, remaining, meter, plan_identity)
    # Atomic evaluate-and-consume inside the account-store BEGIN IMMEDIATE.
    # Timestamp text reflects the injectable clock (epoch seconds); it is empty
    # when no clock is supplied (a lifetime-window consumption needs none) — never
    # the literal string "None".
    now_ts = "" if now is None else str(now)
    status, used = account_store.consume_commercial_quota(
        account_id, meter, window_key, unlimited,
        (0 if unlimited else limit), amount, now_ts, idempotency_key)
    if status == "conflict":                                   # same key, different amount
        return QuotaDecision(OUTCOME_DENIED_INVALID, False, used,
                             (None if unlimited else max(0, limit - used)),
                             meter, plan_identity)
    if status == "exhausted":
        return QuotaDecision(OUTCOME_DENIED_EXHAUSTED, False, used,
                             (None if unlimited else max(0, limit - used)),
                             meter, plan_identity)
    # allowed / allowed_idempotent_replay
    remaining = None if unlimited else max(0, limit - used)
    return QuotaDecision(OUTCOME_ALLOWED, True, used, remaining, meter, plan_identity)


def evaluate_quota(account_store, account_id, meter, now=None):
    """Read-only quota evaluation (no consumption). Fail-closed decision for
    non-authoritative states."""
    return _decide(account_store, account_id, meter, 1, now, None, mutate=False)


def consume_quota(account_store, account_id, meter, amount=1, now=None,
                  idempotency_key=None):
    """Atomically evaluate entitlement + quota and consume ``amount`` units on
    success (no consumption on any denial/failure). Returns a QuotaDecision whose
    ``allowed`` flag is the only authorization signal; every non-authoritative
    state (missing/non-active account, not entitled, unknown/malformed
    assignment, malformed quota policy, exhausted, same-key/different-amount
    conflict) yields ``allowed=False`` and no consumption.

    Raises :class:`QuotaError` for a caller-side fault: an invalid ``amount``
    (non-positive / non-int), or missing/invalid ``now`` when the resolved
    policy uses a fixed technical window and therefore requires an integer epoch
    time source.

    Idempotency-key semantics: an ``idempotency_key`` identifies ONE logical
    consumption. It is keyed by (account, meter, key) — not by window — so a
    replay reusing the same key (even in a later quota window) returns the prior
    outcome and does NOT consume again; a same-key replay with a different
    ``amount`` is a conflict (denied, no second consumption)."""
    return _decide(account_store, account_id, meter, amount, now, idempotency_key,
                   mutate=True)
