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
  * Only ``electronics_electrical`` is currently activated. Activating any further
    domain is a future, separately-authorized gate (Phase 9) — NOT done here.

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

# The ONLY currently activated specialist domain. Explicit and deliberately
# separate from pack lifecycle status. Adding an entry here is a future,
# separately-authorized domain-activation gate — it is NOT changed by §5-I2.
_ACTIVATED_DOMAINS = frozenset({"electronics_electrical"})

_DEFAULT_DOMAINS_DIR = "domains/"


def _resolve_pack_id(domain, registry):
    """Return the canonical ``pack_id`` for a domain identifier (canonical id or
    alias), or ``None`` if it is not recognized by the registry.

    Recognition-only: this never grants activation. An empty/blank/non-string value
    is unrecognized.
    """
    if not isinstance(domain, str) or not domain.strip():
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


def activated_domains():
    """The sorted list of currently activated domains (electronics only)."""
    return sorted(_ACTIVATED_DOMAINS)
