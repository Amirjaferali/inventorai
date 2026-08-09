"""P8-I1 — Entitlement Service (Flask-free, fail-closed governed-capability seam).

The single canonical seam for governed capability access:

    evaluate_entitlement(account_store, account_id, capability) -> Decision

Callers ask a CAPABILITY question and never branch on plan identity themselves
(no scattered ``if plan == ...``). Effective entitlements are DERIVED at
evaluation time from the durable commercial assignment (``account_store``) plus
the versioned code catalog (:mod:`engine.plan_catalog`); nothing is persisted
per account, so a reviewed catalog change is reflected immediately without any
per-account rewrite (derived-not-snapshot).

Fail-closed semantics (raises :class:`EntitlementError`):
  * missing / None caller identity;
  * missing / nonexistent account (MUST NOT receive the technical default);
  * non-active account (``disabled`` / ``deleted``) — existing Phase-5 semantics;
  * unknown plan reference, malformed assignment, catalog/descriptor failure.
A valid ACTIVE account with NO commercial assignment resolves to the internal
technical default identity (legitimate legacy/default state) — NOT an error.

OD-N: this module is the ONLY engine module permitted to import the commercial
catalog; the deterministic core (scoring / progression / safety / evidence)
imports nothing here, so commercial state can never influence technical truth.
This module reads account-store DATA only and never mutates account/auth/
credential state — credential revocation stays plan-independent.
"""

from engine import plan_catalog


class EntitlementError(Exception):
    """Fail-closed entitlement-evaluation error (kept generic; discloses no
    account/plan detail to callers)."""


class Decision:
    """Result of a governed capability evaluation. ``allow`` is the only
    authorization signal; ``reason`` and ``plan_identity`` are diagnostic."""

    __slots__ = ("allow", "reason", "plan_identity")

    def __init__(self, allow, reason, plan_identity):
        self.allow = allow
        self.reason = reason
        self.plan_identity = plan_identity

    def __repr__(self):
        return "Decision(allow=%r, reason=%r, plan_identity=%r)" % (
            self.allow, self.reason, self.plan_identity)


def _resolve_plan_identity(account_store, account_id):
    """Resolve the effective commercial plan identity for ``account_id`` or raise
    :class:`EntitlementError` (fail closed). Enforces account existence + active
    status via the existing Phase-5 account semantics; a missing account MUST NOT
    be defaulted. Absence of an assignment for a valid active account is the
    legitimate legacy/default state and resolves to the technical default."""
    if not account_id:
        raise EntitlementError("no account identity")
    try:
        account = account_store.get_account_by_id(account_id)
    except Exception:
        raise EntitlementError("account lookup failed")       # fail closed
    if account is None:
        raise EntitlementError("account does not exist")      # F: never defaulted
    if account.get("status") != "active":
        raise EntitlementError("account not active")          # disabled / deleted
    try:
        assignment = account_store.get_commercial_assignment(account_id)
    except Exception:
        raise EntitlementError("assignment lookup failed")    # fail closed
    if assignment is None:
        return plan_catalog.default_plan_identity()           # A: legacy/default
    plan_id = assignment.get("plan_id")
    plan_version = assignment.get("plan_version")
    if not plan_id or not plan_version:
        raise EntitlementError("malformed commercial assignment")   # D
    return (plan_id, plan_version)


def evaluate_entitlement(account_store, account_id, capability):
    """Return a :class:`Decision` for ``capability``. Raises
    :class:`EntitlementError` (fail closed) for every non-authoritative state
    (missing/non-active account, unknown/malformed assignment, catalog failure).
    For a resolved plan whose descriptor simply does not grant ``capability``,
    returns ``Decision(allow=False, ...)``."""
    plan_identity = _resolve_plan_identity(account_store, account_id)
    try:
        descriptor = plan_catalog.entitlement_descriptor(*plan_identity)
    except plan_catalog.CatalogError:
        raise EntitlementError("catalog/descriptor failure")  # C (unknown) / E (malformed)
    allowed = bool(descriptor.get(capability, False))
    return Decision(allow=allowed,
                    reason=("granted" if allowed else "not_entitled"),
                    plan_identity=plan_identity)
