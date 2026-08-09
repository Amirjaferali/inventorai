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
# Internal technical test plans (P8-I2) — used ONLY to prove the quota
# architecture (entitled + differing quota policies). Not marketed plans.
_ZERO_QUOTA_TECHNICAL_PLAN = ("__zero_quota_technical__", "1")
_UNLIMITED_TECHNICAL_PLAN = ("__unlimited_technical__", "1")
_FIXED_WINDOW_TECHNICAL_PLAN = ("__fixed_window_technical__", "1")
_MALFORMED_QUOTA_TECHNICAL_PLAN = ("__malformed_quota_technical__", "1")

_CATALOG = {
    (TECHNICAL_DEFAULT_PLAN_ID, TECHNICAL_DEFAULT_PLAN_VERSION): {
        CAPABILITY_INTERNAL_PROOF: True,
    },
    RESTRICTED_TECHNICAL_PLAN: {
        CAPABILITY_INTERNAL_PROOF: False,
    },
    _ZERO_QUOTA_TECHNICAL_PLAN: {CAPABILITY_INTERNAL_PROOF: True},
    _UNLIMITED_TECHNICAL_PLAN: {CAPABILITY_INTERNAL_PROOF: True},
    _FIXED_WINDOW_TECHNICAL_PLAN: {CAPABILITY_INTERNAL_PROOF: True},
    _MALFORMED_QUOTA_TECHNICAL_PLAN: {CAPABILITY_INTERNAL_PROOF: True},
}

# --- P8-I2: commercial usage-quota policy (declarative, versioned) ----------
# UNLIMITED is a NAMED sentinel (never a magic huge integer). A meter maps to
# the governing entitlement capability; quota is evaluated only after entitlement
# grants the capability. Neutral internal proof meter only — no marketed meter.
UNLIMITED = "__unlimited__"
QUOTA_PROOF_METER = "__quota_proof_meter__"

# meter → governing entitlement capability (entitlement is checked first).
_METER_CAPABILITY = {
    QUOTA_PROOF_METER: CAPABILITY_INTERNAL_PROOF,
}

# {(plan_id, plan_version): {meter: {"limit": int|UNLIMITED, "window": {...}}}}.
# Technical PROOF fixtures — NOT Owner-approved commercial limits; never public.
_QUOTA_CATALOG = {
    (TECHNICAL_DEFAULT_PLAN_ID, TECHNICAL_DEFAULT_PLAN_VERSION): {
        QUOTA_PROOF_METER: {"limit": 2, "window": {"kind": "lifetime"}},
    },
    _ZERO_QUOTA_TECHNICAL_PLAN: {
        QUOTA_PROOF_METER: {"limit": 0, "window": {"kind": "lifetime"}},
    },
    _UNLIMITED_TECHNICAL_PLAN: {
        QUOTA_PROOF_METER: {"limit": UNLIMITED, "window": {"kind": "lifetime"}},
    },
    _FIXED_WINDOW_TECHNICAL_PLAN: {
        QUOTA_PROOF_METER: {"limit": 1, "window": {"kind": "fixed", "seconds": 3600}},
    },
    _MALFORMED_QUOTA_TECHNICAL_PLAN: {
        QUOTA_PROOF_METER: "not-a-valid-policy",          # malformed → fail closed
    },
}


def meter_capability(meter):
    """Return the entitlement capability that governs ``meter``, or raise
    :class:`CatalogError` for an unknown meter (fail closed)."""
    try:
        return _METER_CAPABILITY[meter]
    except (KeyError, TypeError):
        raise CatalogError("unknown meter: %r" % (meter,))


def quota_policy(plan_id, plan_version, meter):
    """Return an immutable copy of the validated declarative quota policy
    ``{"limit": int|UNLIMITED, "window": {...}}`` for a plan identity + meter, or
    raise :class:`CatalogError` (fail closed) for unknown identity, missing meter
    policy, or a malformed policy/limit/window. Never returns a partial policy."""
    try:
        policies = _QUOTA_CATALOG[(plan_id, plan_version)]
    except (KeyError, TypeError):
        raise CatalogError("no quota policy for plan %r@%r" % (plan_id, plan_version))
    if not isinstance(policies, dict):
        raise CatalogError("malformed quota policy set for %r@%r" % (plan_id, plan_version))
    try:
        policy = policies[meter]
    except (KeyError, TypeError):
        raise CatalogError("no quota policy for meter %r" % (meter,))
    if (not isinstance(policy, dict) or "limit" not in policy
            or "window" not in policy):
        raise CatalogError("malformed quota policy for meter %r" % (meter,))
    limit = policy["limit"]
    if limit is not UNLIMITED and (
            not isinstance(limit, int) or isinstance(limit, bool) or limit < 0):
        raise CatalogError("malformed quota limit for meter %r" % (meter,))
    window = policy["window"]
    if not isinstance(window, dict) or window.get("kind") not in ("lifetime", "fixed"):
        raise CatalogError("malformed quota window for meter %r" % (meter,))
    if window["kind"] == "fixed":
        secs = window.get("seconds")
        if not isinstance(secs, int) or isinstance(secs, bool) or secs <= 0:
            raise CatalogError("malformed fixed window for meter %r" % (meter,))
    return {"limit": limit, "window": dict(window)}


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
