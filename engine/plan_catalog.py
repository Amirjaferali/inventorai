"""P8-I1 — Plan Catalog (code-resident, versioned, declarative).

Commercial plan definitions as declarative DATA only — capability-flag values,
never imperative commercial logic, never marketed plan names, provider- and
packaging-neutral. Effective entitlements are DERIVED from this catalog at
evaluation time by :mod:`engine.entitlement_service`; nothing here is persisted
per account, so a reviewed catalog change never requires rewriting account rows
(P8-I1 contract: derived-not-snapshot; bounded P8-C refinement — catalog is
code-resident versioned declarative data).

This module is a leaf: it imports no other engine module, so the deterministic
core can never be coupled to commercial state through it (OD-N).

Input contract: read-only lookups keyed by ``(plan_id, plan_version)``.
Output contract: an immutable copy of a declarative ``{capability: bool}``
descriptor, or :class:`CatalogError` for any unknown / unresolvable / malformed
plan identity (fail closed).
Prohibited: marketed plan names; prices; imperative ``if plan == ...`` logic;
public exposure of the internal identifiers below; lifecycle/quota/provider data.
"""

# Internal TECHNICAL default identity — unmistakably internal, NOT a marketed
# plan name, NOT final free-plan packaging, and NOT exposed through any public
# API/UI. A valid active account with no commercial assignment resolves here.
TECHNICAL_DEFAULT_PLAN_ID = "__default_technical__"
TECHNICAL_DEFAULT_PLAN_VERSION = "1"

# A second internal, non-default technical plan used ONLY to prove entitlement
# derivation and capability differentiation. Not a marketed plan.
RESTRICTED_TECHNICAL_PLAN = ("__restricted_technical__", "1")

# Neutral INTERNAL capability key used only to prove the entitlement seam
# end-to-end. Not a user-facing feature; not exposed publicly; introduces no
# real paywall on any existing capability.
CAPABILITY_INTERNAL_PROOF = "__entitlement_proof_capability__"


class CatalogError(Exception):
    """Raised when a plan identity cannot be resolved to a valid declarative
    descriptor (unknown identity or malformed descriptor). Kept generic."""


# Declarative catalog: {(plan_id, plan_version): {capability_key: bool}}. A new
# packaging is a NEW (plan_id, plan_version) or version entry — never an in-place
# mutation that would strand already-assigned accounts.
_CATALOG = {
    (TECHNICAL_DEFAULT_PLAN_ID, TECHNICAL_DEFAULT_PLAN_VERSION): {
        CAPABILITY_INTERNAL_PROOF: True,
    },
    RESTRICTED_TECHNICAL_PLAN: {
        CAPABILITY_INTERNAL_PROOF: False,
    },
}


def default_plan_identity():
    """The internal technical default ``(plan_id, plan_version)``."""
    return (TECHNICAL_DEFAULT_PLAN_ID, TECHNICAL_DEFAULT_PLAN_VERSION)


def entitlement_descriptor(plan_id, plan_version):
    """Return an immutable copy of the declarative capability descriptor for a
    plan identity, or raise :class:`CatalogError` (fail closed) if the identity
    is unknown/unresolvable or the descriptor is malformed. Never returns a
    partial or fabricated descriptor."""
    try:
        descriptor = _CATALOG[(plan_id, plan_version)]
    except (KeyError, TypeError):
        raise CatalogError("unknown plan identity: %r@%r" % (plan_id, plan_version))
    if not isinstance(descriptor, dict):
        raise CatalogError("malformed descriptor for %r@%r" % (plan_id, plan_version))
    return dict(descriptor)
