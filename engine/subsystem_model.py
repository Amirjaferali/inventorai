"""
engine/subsystem_model.py

§5-I3 — Subsystem + cross-domain project model foundation.

Foundation only (governed by the accepted §5-C1 contract-of-record, decisions
**D-S5-04** and **D-S5-05**). Additive, in-memory, persistence-independent.

Model semantics:

    ONE PROJECT (engine.idea_state.IdeaState)
        → ZERO OR MORE Subsystem descriptors
            → EACH subsystem MAY reference a canonical domain

Binding rules:

  * The project stays generic. The scalar root domain
    (``state.domain`` / persisted ``confirmed_domain``) is preserved and is NEVER
    changed by anything here; there is NO peer-root ``domains = [...]`` list
    (D-S5-04). Multiple subsystem domain references never become multiple project
    root domains.
  * A subsystem domain reference is **metadata only**. Referencing a domain NEVER
    activates it and NEVER grants specialist behavior. Support state is resolved
    through the §5-I2 activation policy (``engine.domain_activation``), so a
    reference is ACTIVATED only when that domain is already activated
    (electronics), otherwise RECOGNIZED_NOT_ACTIVATED or UNKNOWN_OR_UNSUPPORTED —
    an unknown reference is never silently defaulted to electronics.
  * No persistence, no web/UI, no domain-pack, no new registry/taxonomy: the
    canonical Domain Registry (via the activation policy) remains the domain
    authority (D-FPC-MAP-06).
"""

from dataclasses import dataclass
from typing import Optional

from engine import domain_activation


@dataclass
class Subsystem:
    """Minimum subsystem descriptor (D-S5-05): a stable id and an OPTIONAL canonical
    domain reference (canonical pack id or alias), or ``None`` for no reference."""
    subsystem_id: str
    domain: Optional[str] = None


def project_subsystems(state):
    """Return the project's subsystem descriptors (empty when absent)."""
    return list(getattr(state, "subsystems", None) or [])


def add_subsystem(state, subsystem_id, domain=None):
    """Append a subsystem descriptor to the project (in-memory only).

    Never touches ``state.domain`` / the root confirmed domain, and never activates
    a domain. Returns the created ``Subsystem``.
    """
    subs = getattr(state, "subsystems", None)
    if subs is None:
        subs = []
        state.subsystems = subs
    sub = Subsystem(subsystem_id=subsystem_id, domain=domain)
    subs.append(sub)
    return sub


def subsystem_support_state(subsystem, registry=None):
    """The §5-I2 support state of the subsystem's domain reference. A subsystem
    with no domain reference is ``UNKNOWN_OR_UNSUPPORTED``."""
    return domain_activation.support_state(getattr(subsystem, "domain", None), registry)


def is_subsystem_domain_activated(subsystem, registry=None):
    """True only when the referenced domain is itself activated by the canonical
    policy. A subsystem reference never grants activation of its own accord."""
    return domain_activation.is_activated(getattr(subsystem, "domain", None), registry)


def subsystem_domains(state):
    """Ordered list of the non-``None`` domain references across the project's
    subsystems (metadata; not root domains)."""
    return [s.domain for s in project_subsystems(state) if getattr(s, "domain", None) is not None]
