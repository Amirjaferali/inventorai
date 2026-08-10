"""P8-AF-I1 — Access-Resolution seam (deterministic, pure, read-only, explainable).

The SINGLE canonical place that composes a set of :class:`engine.access_grant.
AccessGrant` records into an effective access decision. Access decisions must not
be scattered across templates / payment adapters / lifecycle / organization /
quota / ad-hoc role checks; those surfaces CONSUME this resolver's result.

Guarantees (P8-AF-C §5–§6):
  * deterministic and ORDER-INDEPENDENT;
  * pure / side-effect-free / read-only — it mutates no input, consumes/mutates
    NO quota, creates NO lifecycle transition, touches NO account/auth/payment,
    and persists nothing;
  * source-neutral and provider-neutral;
  * REFERENCES the P8-I1 entitlement authority (``plan_catalog``) to VALIDATE that
    a grant's ``entitlement_reference`` is a real catalog identity — it never
    redefines entitlements and never reads capability booleans to decide access;
  * explainable — the result names the selected source and why others were excluded.

Minimal safe precedence (the smallest rule consistent with the contract; the full
business ordering of not-yet-activated sources is DEFERRED — P8-AF-C §6):
  * zero effective grants                         → DENY (``no_effective_grant``);
  * effective grants, all one distinct entitlement → GRANT that single entitlement
    (one quota-policy path — never additive / double-counted);
  * effective grants spanning >1 distinct entitlement → DENY, fail closed
    (``ambiguous_competing_entitlements_precedence_deferred``) — NO invented
    business priority such as "bigger plan wins".

This module imports ONLY the leaf value object and the P8-I1 catalog (reference
validation); it is registered in the OD-N commercial allowlist.
"""

from engine import access_grant as _ag
from engine import plan_catalog as _catalog


class AccessResolverError(Exception):
    """Fail-closed resolution error for malformed/ill-typed input (bad ``now``, a
    non-:class:`AccessGrant` element, or a grant whose entitlement identity is not
    in the P8-I1 catalog). A DENIED decision is NOT an error — it is a valid
    :class:`AccessResolution`."""


class AccessResolution:
    """Immutable, explainable result of :func:`resolve_access`. Exposes ONLY
    access/entitlement provenance — never any data-ownership or cross-account
    permission (access ≠ ownership; P8-AF-C §4/§18)."""

    __slots__ = ("granted", "entitlement_reference", "selected_grant_id",
                 "reason", "contributing_grant_ids", "excluded")

    def __init__(self, granted, entitlement_reference, selected_grant_id, reason,
                 contributing_grant_ids, excluded):
        object.__setattr__(self, "granted", granted)
        object.__setattr__(self, "entitlement_reference", entitlement_reference)
        object.__setattr__(self, "selected_grant_id", selected_grant_id)
        object.__setattr__(self, "reason", reason)
        object.__setattr__(self, "contributing_grant_ids", contributing_grant_ids)
        object.__setattr__(self, "excluded", excluded)

    def __setattr__(self, name, value):
        raise AttributeError("AccessResolution is immutable")

    def __delattr__(self, name):
        raise AttributeError("AccessResolution is immutable")

    def __repr__(self):
        return ("AccessResolution(granted=%r, entitlement_reference=%r, "
                "selected_grant_id=%r, reason=%r, contributing_grant_ids=%r, "
                "excluded=%r)" % (
                    self.granted, self.entitlement_reference, self.selected_grant_id,
                    self.reason, self.contributing_grant_ids, self.excluded))


def _validate_entitlement_identity(reference):
    """REFERENCE the P8-I1 authority: confirm ``reference`` resolves to a real
    catalog identity (fail closed if unknown/malformed). Reads NO capability
    booleans and makes NO access decision from the descriptor — identity only."""
    try:
        _catalog.entitlement_descriptor(reference[0], reference[1])
    except _catalog.CatalogError as exc:
        raise AccessResolverError("unknown entitlement identity: %r" % (reference, )) from exc


def resolve_access(grants, *, now):
    """Resolve the effective access decision for ``grants`` at the injected epoch
    instant ``now``. Returns an :class:`AccessResolution`. Raises
    :class:`AccessResolverError` (fail closed) for a non-int ``now``, a
    non-:class:`AccessGrant` element, or a grant whose entitlement identity is not
    in the P8-I1 catalog. Never mutates input, quota, lifecycle, account, or
    provider state."""
    if not isinstance(now, int) or isinstance(now, bool):
        raise AccessResolverError("now must be an integer epoch time")

    materialized = list(grants)                              # read-only snapshot
    for g in materialized:
        if not isinstance(g, _ag.AccessGrant):
            raise AccessResolverError("every element must be an AccessGrant")

    effective, excluded = [], []
    for g in materialized:
        if _ag.is_effective_at(g, now):
            _validate_entitlement_identity(g.entitlement_reference)   # reference, fail closed
            effective.append(g)
        else:
            excluded.append((g.grant_id, _ag.exclusion_reason(g, now)))
    excluded = tuple(sorted(excluded))                       # order-independent

    if not effective:
        return AccessResolution(
            granted=False, entitlement_reference=None, selected_grant_id=None,
            reason="no_effective_grant", contributing_grant_ids=(), excluded=excluded)

    distinct = {g.entitlement_reference for g in effective}
    contributing = tuple(sorted(g.grant_id for g in effective))

    if len(distinct) > 1:
        # Genuine competing entitlements with NO governed precedence yet → fail
        # closed, deterministically, inventing no business priority (§6).
        return AccessResolution(
            granted=False, entitlement_reference=None, selected_grant_id=None,
            reason="ambiguous_competing_entitlements_precedence_deferred",
            contributing_grant_ids=contributing, excluded=excluded)

    # Exactly one distinct entitlement across all effective grants → a single,
    # unambiguous quota-policy path (never additive). The named representative is
    # the deterministic minimum grant_id (order-independent); the entitlement is
    # identical regardless of which effective grant is named.
    (entitlement, ) = tuple(distinct)
    selected_grant_id = min(g.grant_id for g in effective)
    return AccessResolution(
        granted=True, entitlement_reference=entitlement,
        selected_grant_id=selected_grant_id, reason="single_effective_entitlement",
        contributing_grant_ids=contributing, excluded=excluded)
