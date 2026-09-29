"""
engine/subsystem_model.py

§5-I3 — Subsystem + cross-domain project model foundation.

Foundation only (governed by the accepted §5-C1 contract-of-record, decisions
**D-S5-04** and **D-S5-05**). Additive and in-memory; since Stage 15 Slice 1
an Owner-declared composition is ALSO durably persisted by the existing record
store (see the Stage 15 note below) — this module itself performs no I/O.

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
  * No web/UI, no domain-pack, no new registry/taxonomy: the canonical Domain
    Registry (via the activation policy) remains the domain authority
    (D-FPC-MAP-06).

Stage 15 Slice 1 — Integrated Invention Entry & Durable Subsystem Composition
(additive): the SAME descriptor now optionally carries the Owner-declared part
facts (display name, function / role, OWNER_STATED provenance, UNVALIDATED
validation state) and is durably persisted by the existing record store
(``project_subsystems`` sidecar, written only inside ``create_project``). The
bounded composition this slice admits is exactly ONE Mechanical part plus ONE
Electrical / Electronics part (``COMPOSITION_DOMAINS``); the scalar root domain
stays the Owner-selected INITIAL ANALYSIS FOCUS and is still never changed
here. A declared composition is an OWNER-STATED, UNVALIDATED fact: it is not a
classification, it evaluates nothing, validates nothing, activates nothing and
grants no specialist behaviour to the non-focused part. Subsystem identity is
system-generated (``new_subsystem_id``), opaque, immutable and never derived
from a name, a function text, a domain id or a list position; a client never
supplies one. Declared part text is PRIVATE inventor / project information —
never shared technical knowledge, never logged, never sent to any provider.
"""

import re
import uuid
from dataclasses import dataclass
from typing import Optional

from engine import domain_activation
from engine.idea_state import OWNER_STATED, UNVALIDATED


@dataclass
class Subsystem:
    """Minimum subsystem descriptor (D-S5-05): a stable id and an OPTIONAL canonical
    domain reference (canonical pack id or alias), or ``None`` for no reference.

    Stage 15 Slice 1 additive fields (all default ``None`` so every existing
    two-field caller is unchanged): the Owner-declared ``display_name`` and
    ``function_text`` of a composed part, its ``provenance`` (OWNER_STATED) and
    its ``validation_state`` (UNVALIDATED). They describe what the Owner said the
    part is; they are never evidence, a gap, a validation or a readiness input."""
    subsystem_id: str
    domain: Optional[str] = None
    display_name: Optional[str] = None
    function_text: Optional[str] = None
    provenance: Optional[str] = None
    validation_state: Optional[str] = None


# --- Stage 15 Slice 1: the bounded Owner-declared composition ------------------
# The ONLY composition this slice admits: exactly one Mechanical part and exactly
# one Electrical / Electronics part, stored and shown in THIS fixed order (never
# reordered by classifier output). Canonical pack ids only — an alias is never
# stored. Extending the set is a separately-authorized slice.
COMPOSITION_DOMAINS = ("mechanical", "electronics_electrical")
# Explicit bounds (characters). Over-limit input is rejected, never truncated.
MAX_SUBSYSTEM_NAME_LENGTH = 80
MAX_SUBSYSTEM_FUNCTION_LENGTH = 300
_SUBSYSTEM_ID_RE = re.compile(r"^sub-[0-9a-f]{32}$")


class CompositionError(ValueError):
    """A proposed or durable subsystem composition violates the bounded Stage-15
    contract. Structural message only — it never carries user text."""


def new_subsystem_id():
    """A system-generated, opaque, collision-safe subsystem identity. Derived
    from nothing the Owner typed and from no domain id or list position."""
    return "sub-" + uuid.uuid4().hex


def is_valid_subsystem_id(value):
    """True only for an id of the exact system-generated shape."""
    return isinstance(value, str) and bool(_SUBSYSTEM_ID_RE.match(value))


def valid_subsystem_text(value, limit):
    """A stored part text is exactly what the route stores: a non-empty,
    already-trimmed string within ``limit`` characters and free of NUL."""
    return (isinstance(value, str) and value == value.strip()
            and 0 < len(value) <= limit and "\x00" not in value)


def declared_subsystem(domain, display_name, function_text):
    """Build ONE Owner-declared composed part with a fresh system-generated id,
    OWNER_STATED provenance and UNVALIDATED validation state. Validation of the
    whole composition happens in ``validate_composition``."""
    return Subsystem(subsystem_id=new_subsystem_id(), domain=domain,
                     display_name=display_name, function_text=function_text,
                     provenance=OWNER_STATED, validation_state=UNVALIDATED)


def validate_composition(subsystems, confirmed_domain):
    """Validate a project's subsystem composition against the bounded Stage-15
    contract and return it as a tuple, or raise ``CompositionError``.

    An empty collection is valid (every ordinary / pre-slice project). Otherwise
    it must be EXACTLY one Mechanical part followed by one Electrical /
    Electronics part (``COMPOSITION_DOMAINS`` order), each with a
    system-shaped, distinct id, canonical domain id, valid bounded texts,
    OWNER_STATED provenance and UNVALIDATED validation state — and the project's
    scalar root (the initial analysis focus) must be one of the two parts'
    domains. Used identically before the durable write and on every load."""
    subs = tuple(subsystems or ())
    if not subs:
        return ()
    if len(subs) != len(COMPOSITION_DOMAINS):
        raise CompositionError("composition must hold exactly the two declared parts")
    if confirmed_domain not in COMPOSITION_DOMAINS:
        raise CompositionError("initial analysis focus is not a composed part domain")
    seen = set()
    for sub, expected_domain in zip(subs, COMPOSITION_DOMAINS):
        if not isinstance(sub, Subsystem):
            raise CompositionError("composition entry is not a subsystem descriptor")
        if not is_valid_subsystem_id(sub.subsystem_id) or sub.subsystem_id in seen:
            raise CompositionError("subsystem identity is malformed or duplicated")
        seen.add(sub.subsystem_id)
        if sub.domain != expected_domain:
            raise CompositionError("subsystem domain is not the expected canonical part domain")
        if not valid_subsystem_text(sub.display_name, MAX_SUBSYSTEM_NAME_LENGTH):
            raise CompositionError("subsystem display name is invalid")
        if not valid_subsystem_text(sub.function_text, MAX_SUBSYSTEM_FUNCTION_LENGTH):
            raise CompositionError("subsystem function text is invalid")
        if sub.provenance != OWNER_STATED or sub.validation_state != UNVALIDATED:
            raise CompositionError("subsystem provenance / validation state is invalid")
    return subs


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
