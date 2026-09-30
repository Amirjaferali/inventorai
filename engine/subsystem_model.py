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

Stage 15 Slice 2 — Subsystem Interface Declaration (additive): this module is
ALSO the semantic owner of an Owner-declared INTERFACE between two parts of the
SAME project's durable composition — a bounded relation between existing
subsystem identities, never an answer, assumption, contradiction, decision,
gap, evidence, readiness or compatibility fact, and never a ledger record.
An interface carries a system-generated, opaque, immutable ``interface_id``;
exactly two DISTINCT endpoints naming parts of that composition; the Owner's
own free-text description; OWNER_STATED provenance and UNVALIDATED state.
The two endpoints are an UNORDERED pair: they are stored in the composition's
own fixed part order purely for determinism, which carries NO direction, flow,
dependency, source / target or compatibility meaning. Several distinct
interfaces may join the same two parts. A part's name, function and domain are
never copied into an interface — they stay owned by the part itself. There is
no interface category or taxonomy, no inference of an interface from part
names or domains, no generic graph and no relation engine.

Stage 15 Slice 3 — Interface Verification Preparation (additive): this module
is ALSO the semantic owner of the inventor's own CURRENT verification-
preparation inputs for ONE existing durable interface — the intended operating
conditions, an observable acceptance criterion and the evidence or review
needed, each independently optional while the inventor is still preparing.
They are attributes of that ONE interface, keyed ONLY by its existing
``interface_id`` (no second identity), OWNER_STATED and UNVALIDATED by
construction; the append-only ``SubsystemInterface`` declaration itself is NOT
changed. They are planning inputs, never evidence, a verification result, a
compatibility, feasibility or readiness fact, a gap closure or an IRL input,
and nothing here parses, grades, infers or generates any of them. The only
derived statement is factual presence (none / some / all three recorded).
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


# --- Stage 15 Slice 2: Owner-declared interfaces between composed parts ---------
# Explicit bound (characters), the same bound the Owner's part function text
# already uses. Over-limit input is rejected, never truncated.
MAX_INTERFACE_DESCRIPTION_LENGTH = 300
# Bounded growth: a project cannot accumulate an unbounded interface list.
MAX_SUBSYSTEM_INTERFACES_PER_PROJECT = 20
_INTERFACE_ID_RE = re.compile(r"^ifc-[0-9a-f]{32}$")


@dataclass(frozen=True)
class SubsystemInterface:
    """ONE Owner-declared interface between two DISTINCT parts of the same
    project's composition. ``subsystem_a_id`` / ``subsystem_b_id`` are the
    UNORDERED endpoint pair written in the composition's part order (for
    determinism only — no direction, flow, dependency or source / target
    meaning). ``description`` is the Owner's own trimmed text. It is never
    evidence, a gap, a validation, a readiness input or a compatibility fact."""
    interface_id: str
    subsystem_a_id: str
    subsystem_b_id: str
    description: str
    provenance: str
    validation_state: str


class InterfaceError(ValueError):
    """A proposed or durable interface declaration violates the bounded
    Stage-15 Slice-2 contract. Structural message only — never user text."""


def new_interface_id():
    """A system-generated, opaque, collision-safe interface identity, derived
    from nothing the Owner typed, no part and no list position."""
    return "ifc-" + uuid.uuid4().hex


def is_valid_interface_id(value):
    """True only for an id of the exact system-generated shape."""
    return isinstance(value, str) and bool(_INTERFACE_ID_RE.match(value))


def interface_description(raw):
    """The storable form of an Owner-typed interface description: trimmed,
    and otherwise verbatim. Raises ``InterfaceError`` for an empty, NUL-bearing
    or over-limit description (never truncated, never stripped of a NUL)."""
    if not isinstance(raw, str):
        raise InterfaceError("interface description is not text")
    text = raw.strip()
    if not valid_subsystem_text(text, MAX_INTERFACE_DESCRIPTION_LENGTH):
        raise InterfaceError("interface description is empty, invalid or too long")
    return text


def canonical_interface_endpoints(composition, endpoint_x, endpoint_y):
    """The UNORDERED endpoint pair ``{endpoint_x, endpoint_y}`` as the
    ``(subsystem_a_id, subsystem_b_id)`` tuple in the composition's own part
    order. Both must be DISTINCT parts of ``composition`` (the project's own
    durable composition); anything else raises ``InterfaceError``. The
    ordering exists for determinism only and carries no direction."""
    order = [sub.subsystem_id for sub in (composition or ())]
    if endpoint_x == endpoint_y:
        raise InterfaceError("an interface joins two different parts")
    if endpoint_x not in order or endpoint_y not in order:
        raise InterfaceError("an interface endpoint is not a part of this project")
    first, second = sorted((endpoint_x, endpoint_y), key=order.index)
    return first, second


def declared_interface(composition, endpoint_x, endpoint_y, raw_description):
    """Build ONE Owner-declared interface with a fresh system-generated id,
    OWNER_STATED provenance and UNVALIDATED state, joining two distinct parts
    of ``composition``. A client never supplies the id."""
    first, second = canonical_interface_endpoints(composition, endpoint_x, endpoint_y)
    return SubsystemInterface(
        interface_id=new_interface_id(), subsystem_a_id=first,
        subsystem_b_id=second, description=interface_description(raw_description),
        provenance=OWNER_STATED, validation_state=UNVALIDATED)


def same_interface_material(stored, interface):
    """True when two declarations carry the SAME Owner material: the same
    unordered endpoint pair and the same stored description. The id, the
    provenance and the validation state are not material."""
    return ({stored.subsystem_a_id, stored.subsystem_b_id}
            == {interface.subsystem_a_id, interface.subsystem_b_id}
            and stored.description == interface.description)


def validate_interfaces(interfaces, composition):
    """Validate a project's interface declarations against its OWN durable
    composition and return them as a tuple, or raise ``InterfaceError``.

    Empty is valid (every ordinary, pre-slice or undeclared project). Every
    entry must carry a system-shaped, distinct id; two distinct endpoints that
    are parts of ``composition`` written in its part order; a valid bounded
    description; OWNER_STATED provenance and UNVALIDATED state. Interfaces
    without a composition are invalid. Used identically before the durable
    write and on every load."""
    items = tuple(interfaces or ())
    if not items:
        return ()
    if len(items) > MAX_SUBSYSTEM_INTERFACES_PER_PROJECT:
        raise InterfaceError("too many interface declarations")
    if not composition:
        raise InterfaceError("interfaces exist without a composition")
    seen = set()
    for item in items:
        if not isinstance(item, SubsystemInterface):
            raise InterfaceError("interface entry is not an interface declaration")
        if not is_valid_interface_id(item.interface_id) or item.interface_id in seen:
            raise InterfaceError("interface identity is malformed or duplicated")
        seen.add(item.interface_id)
        if canonical_interface_endpoints(
                composition, item.subsystem_a_id, item.subsystem_b_id) != (
                item.subsystem_a_id, item.subsystem_b_id):
            raise InterfaceError("interface endpoints are not in canonical order")
        if not valid_subsystem_text(item.description, MAX_INTERFACE_DESCRIPTION_LENGTH):
            raise InterfaceError("interface description is invalid")
        if item.provenance != OWNER_STATED or item.validation_state != UNVALIDATED:
            raise InterfaceError("interface provenance / validation state is invalid")
    return items


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


# --- Stage 15 Slice 3: the inventor's verification-preparation inputs --------
# The three preparation inputs the Slice-2 Validation Plan step already asks
# for, in that step's own order. Canonical field names are internal only.
PREPARATION_OPERATING_CONDITIONS = "operating_conditions"
PREPARATION_ACCEPTANCE_CRITERION = "acceptance_criterion"
PREPARATION_EVIDENCE_NEEDED = "evidence_needed"
PREPARATION_FIELDS = (PREPARATION_OPERATING_CONDITIONS,
                      PREPARATION_ACCEPTANCE_CRITERION,
                      PREPARATION_EVIDENCE_NEEDED)
# Explicit per-field bound (characters), the bound the other Owner-authored
# planning fields already use. Over-limit input is rejected, never truncated.
MAX_INTERFACE_PREPARATION_LENGTH = 1000

# Derived presence of the three inputs — a factual statement about which
# fields hold text, never a status, a PASS, a completion award or a verdict.
PREPARATION_NONE_RECORDED = "none_recorded"
PREPARATION_PARTLY_RECORDED = "partly_recorded"
PREPARATION_ALL_RECORDED = "all_recorded"


@dataclass(frozen=True)
class InterfacePreparation:
    """The inventor's CURRENT verification-preparation inputs for ONE existing
    interface, identified ONLY by that interface's ``interface_id``. Each
    field is the Owner's own trimmed text or ``None`` (not recorded). A value
    with every field ``None`` is never stored — it means nothing is recorded."""
    interface_id: str
    operating_conditions: Optional[str] = None
    acceptance_criterion: Optional[str] = None
    evidence_needed: Optional[str] = None

    def value(self, field_name):
        if field_name not in PREPARATION_FIELDS:
            raise InterfaceError("unknown preparation field")
        return getattr(self, field_name)

    def recorded_fields(self):
        """The fields that hold text, in the canonical field order."""
        return tuple(f for f in PREPARATION_FIELDS if getattr(self, f) is not None)

    def missing_fields(self):
        """The fields not recorded yet, in the canonical field order."""
        return tuple(f for f in PREPARATION_FIELDS if getattr(self, f) is None)


def valid_preparation_text(value):
    """A stored preparation input is exactly what the route stores: a
    non-empty, already-trimmed string (internal line breaks kept) within the
    bound and free of NUL."""
    return valid_subsystem_text(value, MAX_INTERFACE_PREPARATION_LENGTH)


def preparation_presence(preparation):
    """The derived presence of the three inputs for ONE interface
    (``preparation`` may be ``None``: nothing recorded). Factual only: all
    three present never means verified, sufficient, correct or compatible."""
    count = 0 if preparation is None else len(preparation.recorded_fields())
    if count == 0:
        return PREPARATION_NONE_RECORDED
    if count == len(PREPARATION_FIELDS):
        return PREPARATION_ALL_RECORDED
    return PREPARATION_PARTLY_RECORDED


def merged_preparation(interface_id, current, changes):
    """The preparation that results from applying ``changes`` (a mapping of
    field name -> trimmed text, or ``None`` to clear that field) to
    ``current`` (the stored ``InterfacePreparation`` or ``None``). Fields
    absent from ``changes`` keep their current value. Returns ``None`` when
    every field ends up cleared (nothing recorded -> no stored value). Raises
    ``InterfaceError`` for an unknown field or invalid text."""
    values = {f: (None if current is None else getattr(current, f))
              for f in PREPARATION_FIELDS}
    try:
        items = list(changes.items())
    except AttributeError:
        raise InterfaceError("preparation changes must be a mapping") from None
    for field_name, text in items:
        if field_name not in PREPARATION_FIELDS:
            raise InterfaceError("unknown preparation field")
        if text is not None and not valid_preparation_text(text):
            raise InterfaceError("preparation text is empty, invalid or too long")
        values[field_name] = text
    if all(v is None for v in values.values()):
        return None
    return InterfacePreparation(interface_id=interface_id, **values)


def validate_interface_preparations(preparations, interfaces):
    """Validate a project's stored preparation inputs against its OWN durable
    interfaces and return them as a tuple in the interfaces' order, or raise
    ``InterfaceError``. Empty is valid. Every entry must name a DISTINCT
    interface of ``interfaces`` by its exact id (never by position, endpoint
    or text), hold at least one input, and every present input must be valid
    stored text. A preparation for an interface that is not in the collection
    is an orphan and invalid — it is never remapped or dropped."""
    items = tuple(preparations or ())
    if not items:
        return ()
    order = [item.interface_id for item in (interfaces or ())]
    seen = set()
    for item in items:
        if not isinstance(item, InterfacePreparation):
            raise InterfaceError("preparation entry is not a preparation")
        if item.interface_id not in order or item.interface_id in seen:
            raise InterfaceError("preparation names no distinct interface of this project")
        seen.add(item.interface_id)
        if not item.recorded_fields():
            raise InterfaceError("a stored preparation records nothing")
        for field_name in item.recorded_fields():
            if not valid_preparation_text(getattr(item, field_name)):
                raise InterfaceError("preparation text is invalid")
    return tuple(sorted(items, key=lambda p: order.index(p.interface_id)))


def preparation_for(preparations, interface_id):
    """The preparation of exactly ``interface_id`` in ``preparations`` or
    ``None`` — resolution by identity only."""
    for item in preparations or ():
        if item.interface_id == interface_id:
            return item
    return None
