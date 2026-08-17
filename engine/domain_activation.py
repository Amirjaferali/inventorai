"""
engine/domain_activation.py

§5-I2 — Activation-status policy + explicit unsupported-domain model.

Foundation only (governed by the accepted §5-C1 contract-of-record). It makes the
truth of *whether a domain is currently activated for specialist/domain-specific
user experience* explicit, deterministic, and testable — reusable by future runtime
surfaces and safe for a future (separately authorized) domain-activation gate.

Binding boundaries (D-S5-03 / §5-C1):

  * The canonical Domain Registry (``engine/domain_registry.py``) remains the single
    source of domain recognition. This module creates NO second registry and NO new
    taxonomy — it consumes the registry.
  * Pack lifecycle ``status`` (``registered`` / ``deprecated`` / legacy ``active``)
    is NOT runtime activation. REGISTERED != USER-ACTIVE. Activation is decided ONLY
    by the explicit allowlist below, never by pack status, pack existence, pack
    loading, registry membership, alias resolution, or metadata.
  * ``electronics_electrical`` and ``mechanical`` are activated per explicit Owner
    authorization (Mechanical Activation Execution Gate; P9_MECHANICAL_DOMAIN_
    QUALIFICATION_CONTRACT.md §16, Requirement 12). Activating any further domain
    remains a future, separately-authorized gate.

Alias handling is recognition-only: an alias resolves to its canonical ``pack_id``
for the RECOGNIZED determination; activation is then decided by the canonical
``pack_id`` against the allowlist, so an alias can never grant activation a pack_id
would not already have.
"""

from engine.domain_registry import load_registry

# Bounded, testable support states.
ACTIVATED = "activated"
RECOGNIZED_NOT_ACTIVATED = "recognized_not_activated"
UNKNOWN_OR_UNSUPPORTED = "unknown_or_unsupported"

# The currently activated specialist domains. Explicit and deliberately separate
# from pack lifecycle status. Adding an entry here is a separately-authorized
# domain-activation gate — it is NOT changed by §5-I2 itself.
_ACTIVATED_DOMAINS = frozenset({"electronics_electrical", "mechanical"})

_DEFAULT_DOMAINS_DIR = "domains/"


def _resolve_pack_id(domain, registry):
    """Return the canonical ``pack_id`` for a domain identifier (canonical id or
    alias), or ``None`` if it is not recognized by the registry.

    Recognition-only: this never grants activation. An empty/blank/non-string value
    is unrecognized.
    """
    if domain is None:
        return None
    if not isinstance(domain, str):
        # P9-E2-R defensive boundary (19): a DomainClassification / result object
        # (or any non-string) must NEVER be silently coerced to an "unknown domain".
        # Fail loud so a programming mistake that leaks a structured result into the
        # activation/registry layer aborts instead of losing truth silently.
        raise TypeError(
            f"domain identifier must be a string, got {type(domain).__name__} "
            "(P9-E2-R defensive boundary)")
    if not domain.strip():
        return None
    if domain in registry:
        return domain
    for pack_id, data in registry.items():
        if domain in (data.get("aliases") or ()):
            return pack_id
    return None


def support_state(domain, registry=None):
    """Classify ``domain`` into exactly one of ``ACTIVATED`` /
    ``RECOGNIZED_NOT_ACTIVATED`` / ``UNKNOWN_OR_UNSUPPORTED``.

    ``registry`` may be an already-loaded registry (a ``MappingProxyType`` from
    ``load_registry``); if omitted the canonical ``domains/`` registry is loaded.
    """
    if registry is None:
        registry = load_registry(_DEFAULT_DOMAINS_DIR)
    pack_id = _resolve_pack_id(domain, registry)
    if pack_id is None:
        return UNKNOWN_OR_UNSUPPORTED
    if pack_id in _ACTIVATED_DOMAINS:
        return ACTIVATED
    return RECOGNIZED_NOT_ACTIVATED


def is_activated(domain, registry=None):
    """True only when ``domain`` resolves to an explicitly activated domain."""
    return support_state(domain, registry) == ACTIVATED


def activated_domains(registry=None):
    """The sorted list of currently activated domains that are ALSO canonically
    recognized by the Domain Registry.

    Enforces the invariant **ACTIVATED ⊆ RECOGNIZED**: an allowlisted id that is not
    present in the registry (canonical id or alias) is never reported, so the
    activation policy can never drift ahead of the canonical registry. ``registry``
    defaults to the canonical ``domains/`` registry.
    """
    if registry is None:
        registry = load_registry(_DEFAULT_DOMAINS_DIR)
    return sorted(d for d in _ACTIVATED_DOMAINS if _resolve_pack_id(d, registry) is not None)
