"""P8-AF-I1 — Canonical Access-Grant (source-neutral, provider-neutral value object).

The smallest source-neutral representation of a *grant of access*: WHY a subject
currently holds (or held) access, traceable to its source and bounded in time. It
is pure declarative DATA — an immutable value object with strict fail-closed
validation — and carries NO quota counters, NO payment-provider identifiers, NO
raw provider payload, NO data-ownership semantics, NO authentication credentials,
and NO business pricing (the fixed ``__slots__`` structurally forbid such fields).

This module is a LEAF: it imports no other engine module (no plan_catalog, no
quota, no lifecycle, no account, no payment). Identity/entitlement REFERENCE
validation against the P8-I1 catalog is performed by the resolver
(:mod:`engine.access_resolver`), not here — so an access grant never redefines
entitlement and never couples to a provider (OD-N preserved).

Input contract: ``make_access_grant(...)`` with an explicit, well-typed field set.
Output contract: an immutable :class:`AccessGrant`, or :class:`AccessGrantError`
(fail closed) for any missing/malformed/ill-typed field.
Prohibited: mutable state; wall-clock reads; quota/provider/credential/pricing/
data-ownership fields; imperative access decisions (that is the resolver's job).
"""

# The ONLY status under which a grant may contribute effective access. Any other
# recognised status is a recorded, non-contributing state; an UNKNOWN status is
# malformed (fail closed).
STATUS_ACTIVE = "active"
STATUS_REVOKED = "revoked"
STATUS_INACTIVE = "inactive"
_ALLOWED_STATUSES = (STATUS_ACTIVE, STATUS_REVOKED, STATUS_INACTIVE)


class AccessGrantError(Exception):
    """Fail-closed access-grant validation error (kept generic; discloses no
    subject/source detail)."""


def _require_nonempty_str(value, field):
    if not isinstance(value, str) or not value.strip():
        raise AccessGrantError("%s must be a non-empty string" % field)


def _require_epoch_int(value, field):
    # bool is a subclass of int — reject it explicitly so a boolean can never be
    # mistaken for an epoch timestamp.
    if not isinstance(value, int) or isinstance(value, bool):
        raise AccessGrantError("%s must be an integer epoch time" % field)


class AccessGrant:
    """An immutable, source-neutral grant of access. Constructed only via
    :func:`make_access_grant` (which validates every field). The fixed slots are
    the structural guarantee that no quota/provider/credential/pricing/
    data-ownership field can ever be attached."""

    __slots__ = ("grant_id", "subject", "source", "entitlement_reference",
                 "effective_from", "effective_until", "status", "provenance")

    def __init__(self, grant_id, subject, source, entitlement_reference,
                 effective_from, effective_until, status, provenance):
        object.__setattr__(self, "grant_id", grant_id)
        object.__setattr__(self, "subject", subject)
        object.__setattr__(self, "source", source)
        object.__setattr__(self, "entitlement_reference", entitlement_reference)
        object.__setattr__(self, "effective_from", effective_from)
        object.__setattr__(self, "effective_until", effective_until)
        object.__setattr__(self, "status", status)
        object.__setattr__(self, "provenance", provenance)

    def __setattr__(self, name, value):                       # immutable
        raise AttributeError("AccessGrant is immutable")

    def __delattr__(self, name):
        raise AttributeError("AccessGrant is immutable")

    def __repr__(self):
        return ("AccessGrant(grant_id=%r, subject=%r, source=%r, "
                "entitlement_reference=%r, effective_from=%r, effective_until=%r, "
                "status=%r, provenance=%r)" % (
                    self.grant_id, self.subject, self.source,
                    self.entitlement_reference, self.effective_from,
                    self.effective_until, self.status, self.provenance))


def make_access_grant(*, grant_id, subject, source, entitlement_reference,
                      effective_from, effective_until, status, provenance):
    """Validate and construct an :class:`AccessGrant` (fail closed).

    ``entitlement_reference`` MUST be a ``(plan_id, plan_version)`` pair of
    non-empty strings — a REFERENCE to a P8-I1 catalog identity (never a
    capability descriptor; existence in the catalog is verified by the resolver).
    ``effective_from`` is an epoch-second int; ``effective_until`` is an
    epoch-second int STRICTLY greater than ``effective_from``, or ``None`` for an
    open-ended grant. ``status`` must be one of the recognised statuses.
    """
    _require_nonempty_str(grant_id, "grant_id")
    _require_nonempty_str(subject, "subject")
    _require_nonempty_str(source, "source")
    _require_nonempty_str(provenance, "provenance")

    if (not isinstance(entitlement_reference, tuple)
            or len(entitlement_reference) != 2):
        raise AccessGrantError("entitlement_reference must be a (plan_id, plan_version) pair")
    plan_id, plan_version = entitlement_reference
    _require_nonempty_str(plan_id, "entitlement_reference.plan_id")
    _require_nonempty_str(plan_version, "entitlement_reference.plan_version")

    _require_epoch_int(effective_from, "effective_from")
    if effective_until is not None:
        _require_epoch_int(effective_until, "effective_until")
        if effective_until <= effective_from:
            raise AccessGrantError("effective_until must be strictly after effective_from")

    if status not in _ALLOWED_STATUSES:
        raise AccessGrantError("unknown status: %r" % (status, ))

    return AccessGrant(grant_id, subject, source, entitlement_reference,
                       effective_from, effective_until, status, provenance)


def is_effective_at(grant, now):
    """Pure predicate: is ``grant`` an ACTIVE grant whose ``[effective_from,
    effective_until)`` window contains ``now``? ``now`` is an injected epoch-second
    int (wall-clock is never read here). Returns ``False`` for a non-active status
    or an out-of-window instant; raises :class:`AccessGrantError` for a
    non-:class:`AccessGrant` or a non-int ``now`` (fail closed)."""
    if not isinstance(grant, AccessGrant):
        raise AccessGrantError("not an AccessGrant")
    _require_epoch_int(now, "now")
    if grant.status != STATUS_ACTIVE:
        return False
    if now < grant.effective_from:
        return False
    if grant.effective_until is not None and now >= grant.effective_until:
        return False
    return True


def exclusion_reason(grant, now):
    """Return a deterministic reason string explaining why ``grant`` does NOT
    contribute at ``now`` (``None`` if it IS effective). Used for provenance."""
    if grant.status != STATUS_ACTIVE:
        return "status_%s" % grant.status
    if now < grant.effective_from:
        return "not_yet_effective"
    if grant.effective_until is not None and now >= grant.effective_until:
        return "expired"
    return None
