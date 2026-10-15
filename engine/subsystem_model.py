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
grants no specialist behaviour to the non-focused part — with ONE narrow,
Owner-authorized exception (CAP13-THERM01-INTEGRATED-PART-01, 2026-10-10): the
two admitted request-local calculations, ``cap13:static_reactions_two_support``
v1.0 and ``therm01:conduction_temperature_difference_single_path`` v1.0, may be
OFFERED for the declared Mechanical and Electrical / Electronics part
respectively whatever the initial analysis focus (eligibility is decided in the
web layer from this validated durable composition). Offering a calculation for a
declared part establishes no applicability, validation or safety and changes
nothing here. A further narrow, Owner-authorized exception
(CAP12-INTEGRATED-MECHANICAL-PART-01): the existing CAP-12 form mock-up advisory
may likewise be OFFERED for the declared Mechanical part whatever the initial
analysis focus, decided in the web layer from the same validated durable
composition; it establishes no suitability, compatibility, validation or safety
and changes nothing here. No other specialist behaviour is granted by these
exceptions. Subsystem identity is
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

Stage 28 — Control-Loop Optional Part — Slice 1 (additive, dormant): the
composition may additionally hold ONE optional part (``OPTIONAL_COMPOSITION_
DOMAINS``) after the required pair, reusing the same descriptor, identity,
provenance and persistence. It is never the initial analysis focus, and it is
admitted at entry only while the canonical policy lists it as part-eligible;
interfaces may then join any two DISTINCT parts of the composition.

Stage 28 — Control-Loop Optional Part — Slice 2 (additive, dormant): this
module is ALSO the semantic owner of the inventor's CURRENT answers to the
governed questions of an OPTIONAL part (``PartAnswer``), keyed by the part's
existing ``subsystem_id`` and the governed question id. They are attributes of
that ONE part — never a gap, a gap state, evidence, a readiness, maturity,
progression or Integration input — and the only derived statement is recording
completeness (``part_family_presence``).

COMPONENT-INVENTORY-DECLARE-LIST-01 (additive): this module is ALSO the
semantic owner of the inventor's manually DECLARED components
(``ProjectComponent``) — ONE record per physical component, belonging to its
project, optionally referencing zero or more of that project's OWN durable
parts. The references are inventor-declared associations only, never proof of
containment, compatibility, contribution or suitability; nothing is inferred,
edited or deleted, and no component text enters ``IdeaState``.
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
# Stage 28 — Control-Loop Optional Part — Slice 1: the ONE optional part slot a
# composition may additionally hold, AFTER the required pair and in this fixed
# order. A part here is never the initial analysis focus (the scalar root stays
# a ``COMPOSITION_DOMAINS`` domain) and is admitted at entry only while the
# canonical policy lists it as part-eligible
# (``engine.domain_activation.is_part_eligible``); its presence here grants no
# activation, evaluation or specialist behaviour. Not an N-domain model:
# extending this tuple is a separately-authorized slice.
OPTIONAL_COMPOSITION_DOMAINS = ("control_loop",)
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
    Electronics part (``COMPOSITION_DOMAINS`` order), optionally followed by
    exactly ONE part of the optional slot (``OPTIONAL_COMPOSITION_DOMAINS``),
    each with a system-shaped, distinct id, canonical domain id, valid bounded
    texts, OWNER_STATED provenance and UNVALIDATED validation state — and the
    project's scalar root (the initial analysis focus) must be one of the two
    REQUIRED parts' domains, never the optional part's. Structural only: part
    eligibility is decided at entry by the canonical policy, never here. Used
    identically before the durable write and on every load."""
    subs = tuple(subsystems or ())
    if not subs:
        return ()
    expected = COMPOSITION_DOMAINS + OPTIONAL_COMPOSITION_DOMAINS
    if len(subs) not in (len(COMPOSITION_DOMAINS), len(expected)):
        raise CompositionError(
            "composition must hold the two required parts and at most the optional part")
    if confirmed_domain not in COMPOSITION_DOMAINS:
        raise CompositionError("initial analysis focus is not a composed part domain")
    seen = set()
    for sub, expected_domain in zip(subs, expected):
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


# --- Stage 15 closure: the Owner-declared interface dependency (current value) --
# For ONE existing durable interface the inventor may declare, in their own
# terms, which part relies on the other through that interaction. It is a
# SEPARATE current-value attribute keyed ONLY by the existing ``interface_id``:
# the append-only ``SubsystemInterface`` stays exactly as declared — its
# endpoint pair is still UNORDERED and its stored order still carries no
# direction, flow or dependency meaning. A dependency is OWNER_STATED and
# UNVALIDATED by construction; absence means "not declared", never
# "independent". A ONE-WAY dependency names the exact dependent part and the
# exact part it relies on, both distinct endpoints of that interface; MUTUAL is
# its own explicit declaration and is never inferred from endpoint order.
# Nothing here evaluates consistency, carries effects onward, derives a
# requirement, a plan step, a gap, readiness or compatibility, or creates a
# relationship graph: that evaluation stays with the future D4 gate.
DEPENDENCY_ONE_WAY = "one_way"
DEPENDENCY_MUTUAL = "mutual"
DEPENDENCY_KINDS = (DEPENDENCY_ONE_WAY, DEPENDENCY_MUTUAL)
# Explicit bound (characters), the bound the Owner's interface description
# already uses. Over-limit input is rejected, never truncated.
MAX_INTERFACE_DEPENDENCY_NOTE_LENGTH = 300


@dataclass(frozen=True)
class InterfaceDependency:
    """The inventor's CURRENT dependency declaration for ONE existing
    interface, identified ONLY by its ``interface_id``. ``kind`` is one-way or
    mutual; a one-way declaration carries the exact dependent subsystem id and
    the exact subsystem id it relies on; ``note`` is the Owner's optional own
    explanation. Never evidence, a requirement, a verification or a
    compatibility fact."""
    interface_id: str
    kind: str
    dependent_subsystem_id: Optional[str] = None
    depends_on_subsystem_id: Optional[str] = None
    note: Optional[str] = None


def valid_dependency_note(value):
    """A stored note is exactly what the route stores: ``None`` (no note) or a
    non-empty, already-trimmed string within the bound and free of NUL."""
    return value is None or valid_subsystem_text(
        value, MAX_INTERFACE_DEPENDENCY_NOTE_LENGTH)


def check_interface_dependency(dependency, interface):
    """Return ``dependency`` iff it is a valid declaration for exactly
    ``interface`` (the project's durable ``SubsystemInterface``), or raise
    ``InterfaceError``. A one-way declaration must name the interface's two
    DISTINCT endpoints, one as the dependent part and the other as the part it
    relies on — by exact identity, never by position; a mutual declaration
    names no direction."""
    if not isinstance(dependency, InterfaceDependency):
        raise InterfaceError("dependency entry is not a dependency declaration")
    if not isinstance(interface, SubsystemInterface) \
            or dependency.interface_id != interface.interface_id:
        raise InterfaceError("dependency names another interface")
    if dependency.kind == DEPENDENCY_ONE_WAY:
        pair = (dependency.dependent_subsystem_id,
                dependency.depends_on_subsystem_id)
        if pair[0] == pair[1] or set(pair) != {interface.subsystem_a_id,
                                               interface.subsystem_b_id}:
            raise InterfaceError(
                "a one-way dependency joins the two parts of this interface")
    elif dependency.kind == DEPENDENCY_MUTUAL:
        if dependency.dependent_subsystem_id is not None \
                or dependency.depends_on_subsystem_id is not None:
            raise InterfaceError("a mutual dependency names no direction")
    else:
        raise InterfaceError("unknown dependency kind")
    if not valid_dependency_note(dependency.note):
        raise InterfaceError("dependency note is invalid")
    return dependency


def validate_interface_dependencies(dependencies, interfaces):
    """Validate a project's stored dependency declarations against its OWN
    durable interfaces and return them in the interfaces' order, or raise
    ``InterfaceError``. Empty is valid. Every entry must name a DISTINCT
    interface of ``interfaces`` by exact id and be a valid declaration for it;
    an orphan is invalid — never remapped or dropped."""
    items = tuple(dependencies or ())
    if not items:
        return ()
    by_id = {item.interface_id: item for item in (interfaces or ())}
    order = list(by_id)
    seen = set()
    for item in items:
        interface_id = getattr(item, "interface_id", None)
        if interface_id not in by_id or interface_id in seen:
            raise InterfaceError("dependency names no distinct interface of this project")
        seen.add(interface_id)
        check_interface_dependency(item, by_id[interface_id])
    return tuple(sorted(items, key=lambda d: order.index(d.interface_id)))


def dependency_for(dependencies, interface_id):
    """The dependency declaration of exactly ``interface_id`` or ``None`` (not
    declared) — resolution by identity only."""
    for item in dependencies or ():
        if item.interface_id == interface_id:
            return item
    return None


# --- Stage 28 — Control-Loop Optional Part — Slice 2: part answers (dormant) ---
# The inventor's own CURRENT answers to the governed questions an OPTIONAL
# composed part is asked. The question set is the part's own pack questions for
# exactly these gap families, in this order (resolved by the caller through
# ``engine.domain_rules.get_domain_questions``); PHYSICAL_FEASIBILITY is
# deliberately absent. A family name here is a grouping of that part's
# questions only: it shares NO state with the project's root gap of the same
# name, and nothing here is a gap, a gap state, evidence, a readiness,
# maturity or progression input, an Integration fact, a validation or a
# feasibility determination. An answer is keyed by (project, subsystem id,
# governed question id) and is OWNER_STATED / UNVALIDATED by construction.
# 28-T5-NONFOCUSED-REQUIRED-PART-QUESTIONS-SAFETY-01: the SAME current-value
# answers are also kept for exactly ONE more part of a durable composition —
# the REQUIRED part that is NOT the project's initial analysis focus (the
# Mechanical part of an Electrical / Electronics-focused project, or the
# reverse), asked its OWN pack's questions for the same two families. The
# focused required part is never a question part (its questions are the root
# analysis), and nothing about the part answers changes: they stay outside the
# root gaps, progression, readiness, evidence and the focus.
PART_QUESTION_GAP_TYPES = ("MECHANISM_COMPLETENESS", "BOUNDARY_AMBIGUITY")
# Explicit bound (characters), the bound the other Owner-authored current-value
# texts of a composed project already use. Over-limit input is rejected.
MAX_PART_ANSWER_LENGTH = 1000
# A governed question id: ``<pack id>:<gap type>:Q<n>`` (structure only; a
# stored id is never checked against, or remapped to, the current pack).
MAX_PART_QUESTION_ID_LENGTH = 128
_PART_QUESTION_ID_RE = re.compile(r"^[a-z][a-z0-9_]*:[A-Z][A-Z_]*:Q[1-9][0-9]*$")

# Derived presence — recording completeness only, never a gap state, a
# resolution, a validation or technical completeness.
PART_ANSWER_RECORDED = "recorded"
PART_ANSWER_NOT_RECORDED = "not_recorded"
PART_FAMILY_NONE_RECORDED = "none_recorded"
PART_FAMILY_SOME_RECORDED = "some_recorded"
PART_FAMILY_ALL_RECORDED = "all_recorded"


class PartAnswerError(ValueError):
    """A proposed or durable part answer violates the bounded Slice-2
    contract. Structural message only — it never carries user text."""


@dataclass(frozen=True)
class PartAnswer:
    """The inventor's CURRENT answer to ONE governed question for ONE question
    part (the optional part, or the non-focused required part — see
    ``part_question_owner``): the part's ``subsystem_id``, the governed ``question_id``
    and the Owner's own trimmed ``answer_text``. Never a gap, evidence, a
    validation or a readiness, progression or Integration input."""
    subsystem_id: str
    question_id: str
    answer_text: str


def is_valid_part_question_id(value):
    """True only for a structurally valid governed question id."""
    return (isinstance(value, str) and len(value) <= MAX_PART_QUESTION_ID_LENGTH
            and bool(_PART_QUESTION_ID_RE.match(value)))


def valid_part_answer_text(value):
    """A stored answer is exactly what the route stores: a non-empty,
    already-trimmed string (internal line breaks kept) within the bound and
    free of NUL."""
    return valid_subsystem_text(value, MAX_PART_ANSWER_LENGTH)


def nonfocused_required_part(composition, focus):
    """The REQUIRED part of ``composition`` that is NOT the initial analysis
    focus ``focus``, or ``None`` (no composition, or a focus that is not one
    of the required pair's domains). Resolution by the durable domain of each
    part against the durable scalar root only — never by name, text or list
    position."""
    if focus not in COMPOSITION_DOMAINS:
        return None
    for sub in composition or ():
        if sub.domain in COMPOSITION_DOMAINS and sub.domain != focus:
            return sub
    return None


def part_question_owner(composition, subsystem_id, focus=None):
    """The question part of ``composition`` whose identity is exactly
    ``subsystem_id``, or raise ``PartAnswerError``. A question part is the
    OPTIONAL part and — only when the durable initial analysis focus
    ``focus`` is given — the NON-FOCUSED REQUIRED part
    (``nonfocused_required_part``). The focused required part, another
    project's part or an unknown id never carries part answers; without
    ``focus`` only the optional part does (the original contract)."""
    nonfocused = nonfocused_required_part(composition, focus)
    for sub in composition or ():
        if sub.subsystem_id != subsystem_id:
            continue
        if sub.domain in OPTIONAL_COMPOSITION_DOMAINS or sub is nonfocused:
            return sub
    raise PartAnswerError("the answer names no question part of this project")


def question_parts(composition, focus):
    """The question parts of a durable composition in a fixed order: the
    non-focused required part first, then the optional part when present.
    ``()`` for an ordinary project."""
    parts = []
    nonfocused = nonfocused_required_part(composition, focus)
    if nonfocused is not None:
        parts.append(nonfocused)
    parts.extend(sub for sub in composition or ()
                 if sub.domain in OPTIONAL_COMPOSITION_DOMAINS)
    return tuple(parts)


def check_part_answer_target(part, question_id):
    """Raise ``PartAnswerError`` unless ``question_id`` is a structurally
    valid governed id of ``part``'s OWN pack (its ``<pack id>`` prefix is the
    part's domain) in one of the part question families, so an answer can
    never be filed under another domain's question even when the gap-family
    name is the same, nor under a PHYSICAL_FEASIBILITY question."""
    if not is_valid_part_question_id(question_id) \
            or question_id.split(":", 1)[0] != part.domain:
        raise PartAnswerError("the question id is not one of this part's pack")
    # 28-T5: the question families a part is asked are exactly
    # ``PART_QUESTION_GAP_TYPES`` — never PHYSICAL_FEASIBILITY — and the store
    # refuses any other family too, not only the route.
    if question_id.split(":")[1] not in PART_QUESTION_GAP_TYPES:
        raise PartAnswerError("the question id is not of a part question family")


def validate_part_answers(answers, composition, focus=None):
    """Validate a project's stored part answers against its OWN durable
    composition and return them as a tuple, or raise ``PartAnswerError``.
    Empty is valid. Every entry must name a question part of ``composition``
    (``part_question_owner``, with the durable ``focus``) by exact id, a structurally valid question id of that part's own pack
    (never checked against or remapped to the CURRENT pack: a stored answer
    to a question that is no longer asked stays as history), be distinct per
    (part, question) and hold valid stored text."""
    items = tuple(answers or ())
    seen = set()
    for item in items:
        if not isinstance(item, PartAnswer):
            raise PartAnswerError("part answer entry is not a part answer")
        part = part_question_owner(composition, item.subsystem_id, focus)
        check_part_answer_target(part, item.question_id)
        key = (item.subsystem_id, item.question_id)
        if key in seen:
            raise PartAnswerError("a part question is answered twice")
        seen.add(key)
        if not valid_part_answer_text(item.answer_text):
            raise PartAnswerError("part answer text is invalid")
    return items


def part_answer_for(answers, subsystem_id, question_id):
    """The answer of exactly (``subsystem_id``, ``question_id``) or ``None``
    (not recorded) — resolution by identity only."""
    for item in answers or ():
        if item.subsystem_id == subsystem_id and item.question_id == question_id:
            return item
    return None


def part_family_presence(question_ids, answers, subsystem_id):
    """The derived recording completeness of ONE family of governed
    questions for ONE part: none / some / all of ``question_ids`` hold a
    recorded answer. Presence only — never open, partial, closed, resolved,
    validated or technically complete."""
    count = sum(1 for qid in question_ids
                if part_answer_for(answers, subsystem_id, qid) is not None)
    if count == 0:
        return PART_FAMILY_NONE_RECORDED
    if count == len(question_ids):
        return PART_FAMILY_ALL_RECORDED
    return PART_FAMILY_SOME_RECORDED


# --- COMPONENT-INVENTORY-DECLARE-LIST-01: inventor-declared components --------
# ONE record per PHYSICAL COMPONENT the inventor says the invention includes —
# never one per part or discipline. It belongs directly to its project; on an
# integrated project it MAY reference zero or more of that project's OWN durable
# parts (``subsystem_ids``), stored in the composition's own part order for
# determinism only. An empty reference collection means project-level /
# unassigned: nothing is fabricated or defaulted to the root domain. A reference
# is the inventor's declared association only — never proof of physical
# containment, compatibility, technical contribution or suitability — and one
# component referenced by several parts stays ONE component. Equal names never
# merge two declarations. No delete, quantity, specification, rating, material,
# price, supplier, taxonomy or validation. COMPONENT-INVENTORY-CORRECT-WITHDRAW-01
# adds correction and terminal withdrawal as an append-only revision history
# over these immutable declarations (the revision section below).
MAX_COMPONENT_NAME_LENGTH = MAX_SUBSYSTEM_NAME_LENGTH
MAX_COMPONENT_FUNCTION_LENGTH = MAX_SUBSYSTEM_FUNCTION_LENGTH
# Bounded growth. The ACTIVE cap: at most this many components are current
# (not withdrawn) at once; a withdrawal frees an active slot.
MAX_PROJECT_COMPONENTS_PER_PROJECT = 50
# The LIFETIME cap: at most this many component identities are ever declared in
# one project. Identities and declaration sequence numbers are never recycled.
MAX_DECLARED_COMPONENTS_PER_PROJECT = 500
_COMPONENT_ID_RE = re.compile(r"^cmp-[0-9a-f]{32}$")


class ComponentError(ValueError):
    """A proposed or durable component declaration violates the bounded
    declare-and-list contract. Structural message only — never user text."""


@dataclass(frozen=True)
class ProjectComponent:
    """ONE inventor-declared physical component of a project. ``component_id``
    is system-generated, opaque and immutable; ``display_name`` and
    ``function_text`` are the inventor's own trimmed text; ``subsystem_ids`` is
    the duplicate-free tuple of the project's OWN durable parts the inventor
    associated it with, in the composition's part order (``()`` =
    project-level / unassigned). OWNER_STATED and UNVALIDATED by construction;
    never evidence, a gap, a readiness input or a technical fact."""
    component_id: str
    display_name: str
    function_text: str
    subsystem_ids: tuple
    provenance: str
    validation_state: str


def new_component_id():
    """A system-generated, opaque, collision-safe component identity, derived
    from nothing the inventor typed, no part and no list position."""
    return "cmp-" + uuid.uuid4().hex


def is_valid_component_id(value):
    """True only for an id of the exact system-generated shape."""
    return isinstance(value, str) and bool(_COMPONENT_ID_RE.match(value))


def canonical_component_parts(composition, subsystem_ids):
    """The inventor-selected part references as a duplicate-free tuple in the
    composition's own part order. Every reference must name a part of
    ``composition`` (the project's OWN durable composition) exactly once;
    anything else raises ``ComponentError``. ``()`` stays ``()`` — it is never
    defaulted to a part or to the root domain."""
    refs = tuple(subsystem_ids or ())
    order = [sub.subsystem_id for sub in (composition or ())]
    if len(set(refs)) != len(refs):
        raise ComponentError("a part is referenced twice")
    if any(ref not in order for ref in refs):
        raise ComponentError("a referenced part is not a part of this project")
    return tuple(sorted(refs, key=order.index))


def declared_component(composition, display_name, function_text, subsystem_ids):
    """Build ONE inventor-declared component with a fresh system-generated id,
    OWNER_STATED provenance and UNVALIDATED state. Texts must already be the
    stored (trimmed) form; invalid or over-limit text raises ``ComponentError``
    (never truncated or reinterpreted). A client never supplies the id."""
    if not valid_subsystem_text(display_name, MAX_COMPONENT_NAME_LENGTH):
        raise ComponentError("component name is empty, invalid or too long")
    if not valid_subsystem_text(function_text, MAX_COMPONENT_FUNCTION_LENGTH):
        raise ComponentError("component function is empty, invalid or too long")
    return ProjectComponent(
        component_id=new_component_id(), display_name=display_name,
        function_text=function_text,
        subsystem_ids=canonical_component_parts(composition, subsystem_ids),
        provenance=OWNER_STATED, validation_state=UNVALIDATED)


def same_component_material(stored, component):
    """True when two declarations carry the SAME inventor material: the same
    name, function text and set of referenced parts. The id, provenance and
    validation state are not material."""
    return (stored.display_name == component.display_name
            and stored.function_text == component.function_text
            and set(stored.subsystem_ids) == set(component.subsystem_ids))


def validate_components(components, composition):
    """Validate a project's COMPLETE component inventory against its OWN
    durable composition and return it as a tuple, or raise ``ComponentError``.

    Empty is valid (every ordinary, pre-slice or undeclared project). Every
    entry must carry a system-shaped, distinct id; valid bounded texts; a
    duplicate-free tuple of parts of ``composition`` in its part order (``()``
    is valid — an ordinary project can only hold ``()``); OWNER_STATED
    provenance and UNVALIDATED state; and the declarations are within the
    per-project LIFETIME cap (the active cap is a property of the current
    projection, ``project_component_inventory``). Used identically before the
    durable write and on every load."""
    items = tuple(components or ())
    if len(items) > MAX_DECLARED_COMPONENTS_PER_PROJECT:
        raise ComponentError("too many component declarations")
    seen = set()
    for item in items:
        if not isinstance(item, ProjectComponent):
            raise ComponentError("inventory entry is not a component declaration")
        if not is_valid_component_id(item.component_id) or item.component_id in seen:
            raise ComponentError("component identity is malformed or duplicated")
        seen.add(item.component_id)
        if not valid_subsystem_text(item.display_name, MAX_COMPONENT_NAME_LENGTH):
            raise ComponentError("component name is invalid")
        if not valid_subsystem_text(item.function_text, MAX_COMPONENT_FUNCTION_LENGTH):
            raise ComponentError("component function is invalid")
        if not isinstance(item.subsystem_ids, tuple) or not all(
                isinstance(ref, str) for ref in item.subsystem_ids):
            raise ComponentError("component part references are malformed")
        if canonical_component_parts(composition, item.subsystem_ids) \
                != item.subsystem_ids:
            raise ComponentError("component part references are not in canonical order")
        if item.provenance != OWNER_STATED or item.validation_state != UNVALIDATED:
            raise ComponentError("component provenance / validation state is invalid")
    return items


# --- COMPONENT-INVENTORY-CORRECT-WITHDRAW-01: correction and withdrawal -------
# The inventor may CORRECT a current component's name, function and part links,
# or WITHDRAW it from the active inventory. Both are append-only REVISIONS over
# the immutable original declaration: the declaration row, its system-generated
# ``component_id`` and its declaration order never change, and no revision is
# ever rewritten or removed. Each component carries ONE contiguous linear
# history (revision 1, 2, ... k); a WITHDRAWN revision is terminal. The CURRENT
# component is the original declaration with its latest correction applied; a
# withdrawn component is historical only and never active. Every revision is
# OWNER_STATED / UNVALIDATED: a correction is the inventor's restatement, never
# engineering verification, and a withdrawal removes nothing from the durable
# record (it is not erasure).
COMPONENT_REVISION_CORRECTED = "CORRECTED"
COMPONENT_REVISION_WITHDRAWN = "WITHDRAWN"
COMPONENT_REVISION_KINDS = (COMPONENT_REVISION_CORRECTED,
                            COMPONENT_REVISION_WITHDRAWN)
# Per-component bound: at most this many corrections, plus ONE separately
# reserved terminal withdrawal (so a component with every correction used can
# still be withdrawn).
MAX_CORRECTIONS_PER_COMPONENT = 20
MAX_REVISIONS_PER_COMPONENT = MAX_CORRECTIONS_PER_COMPONENT + 1
_COMPONENT_REVISION_ID_RE = re.compile(r"^crv-[0-9a-f]{32}$")


class ComponentRevisionError(ComponentError):
    """A proposed component revision is not admissible against the CURRENT
    inventory. Structural message only — never user text."""


class ComponentUnknown(ComponentRevisionError):
    """The revision names no component of this project."""


class ComponentStale(ComponentRevisionError):
    """The revision was prepared against an older version of the component."""


class ComponentAlreadyWithdrawn(ComponentRevisionError):
    """The component is withdrawn: withdrawal is terminal."""


class ComponentCorrectionLimit(ComponentRevisionError):
    """The component already holds the maximum number of corrections."""


class ComponentUnchanged(ComponentRevisionError):
    """A correction that restates the current material exactly."""


@dataclass(frozen=True)
class ComponentRevision:
    """ONE append-only revision of ONE declared component. ``revision_id`` is
    system-generated and immutable; ``revision_no`` is the component-local
    position (1 = first revision after the declaration). A CORRECTED revision
    carries the complete corrected material (``display_name``,
    ``function_text``, ``subsystem_ids``); a WITHDRAWN revision carries none."""
    revision_id: str
    component_id: str
    revision_no: int
    kind: str
    display_name: Optional[str]
    function_text: Optional[str]
    subsystem_ids: Optional[tuple]
    provenance: str
    validation_state: str


@dataclass(frozen=True)
class ComponentVersion:
    """One historical version of a component's material: ``revision_no`` 0 is
    the original declaration, ``n`` the n-th correction."""
    revision_no: int
    display_name: str
    function_text: str
    subsystem_ids: tuple


@dataclass(frozen=True)
class ComponentRecord:
    """ONE declared component with its validated history. ``current`` is the
    latest material as a ``ProjectComponent`` (the stable ``component_id``,
    OWNER_STATED / UNVALIDATED); ``versions`` is every material version,
    oldest first; ``head_revision_no`` is 0 when there is no revision."""
    current: ProjectComponent
    versions: tuple
    head_revision_no: int
    corrections: int
    withdrawn: bool

    @property
    def component_id(self):
        return self.current.component_id


@dataclass(frozen=True)
class ComponentInventory:
    """The ONE authoritative projection of a project's component inventory:
    every declared component in declaration order with its history. ``active``
    is the current inventory every consumer presents; ``withdrawn`` is the
    historical remainder, never active."""
    records: tuple

    @property
    def active(self):
        return tuple(r.current for r in self.records if not r.withdrawn)

    @property
    def withdrawn(self):
        return tuple(r for r in self.records if r.withdrawn)

    @property
    def declared_count(self):
        return len(self.records)

    def record_for(self, component_id):
        for record in self.records:
            if record.component_id == component_id:
                return record
        return None


def new_component_revision_id():
    """A system-generated, opaque, collision-safe revision identity."""
    return "crv-" + uuid.uuid4().hex


def is_valid_component_revision_id(value):
    """True only for a revision id of the exact system-generated shape."""
    return isinstance(value, str) and bool(_COMPONENT_REVISION_ID_RE.match(value))


def same_revision_material(stored, revision):
    """True when two revisions carry the SAME material: the same component,
    kind and position and, for a correction, the same name, function and set
    of referenced parts. The revision id, provenance and validation state are
    not material."""
    if (stored.component_id != revision.component_id
            or stored.kind != revision.kind
            or stored.revision_no != revision.revision_no):
        return False
    if stored.kind == COMPONENT_REVISION_WITHDRAWN:
        return True
    return (stored.display_name == revision.display_name
            and stored.function_text == revision.function_text
            and set(stored.subsystem_ids) == set(revision.subsystem_ids))


def _validate_revision_shape(rev, composition):
    if not isinstance(rev, ComponentRevision):
        raise ComponentError("history entry is not a component revision")
    if not is_valid_component_revision_id(rev.revision_id):
        raise ComponentError("revision identity is malformed")
    if not is_valid_component_id(rev.component_id):
        raise ComponentError("revision component identity is malformed")
    if not isinstance(rev.revision_no, int) or isinstance(rev.revision_no, bool) \
            or not 1 <= rev.revision_no <= MAX_REVISIONS_PER_COMPONENT:
        raise ComponentError("revision position is out of range")
    if rev.provenance != OWNER_STATED or rev.validation_state != UNVALIDATED:
        raise ComponentError("revision provenance / validation state is invalid")
    if rev.kind == COMPONENT_REVISION_WITHDRAWN:
        if (rev.display_name is not None or rev.function_text is not None
                or rev.subsystem_ids is not None):
            raise ComponentError("a withdrawal carries material")
        return
    if rev.kind != COMPONENT_REVISION_CORRECTED:
        raise ComponentError("revision kind is unknown")
    if rev.revision_no > MAX_CORRECTIONS_PER_COMPONENT:
        raise ComponentError("too many corrections")
    if not valid_subsystem_text(rev.display_name, MAX_COMPONENT_NAME_LENGTH):
        raise ComponentError("corrected component name is invalid")
    if not valid_subsystem_text(rev.function_text, MAX_COMPONENT_FUNCTION_LENGTH):
        raise ComponentError("corrected component function is invalid")
    if not isinstance(rev.subsystem_ids, tuple) or not all(
            isinstance(ref, str) for ref in rev.subsystem_ids):
        raise ComponentError("corrected part references are malformed")
    if canonical_component_parts(composition, rev.subsystem_ids) != rev.subsystem_ids:
        raise ComponentError("corrected part references are not in canonical order")


def project_component_inventory(declarations, revisions, composition):
    """Validate a project's COMPLETE declarations and revision history WHOLE
    against its OWN durable ``composition`` and return the one authoritative
    ``ComponentInventory``, or raise ``ComponentError`` (nothing partial; a
    defect anywhere never falls back to the original declarations).

    Declarations: as ``validate_components`` (lifetime cap). Revisions: each
    well formed, with a distinct revision id; each names a declared component;
    each component's revisions are exactly 1..k with no gap, fork or
    duplicate; nothing follows a withdrawal; at most the per-component number
    of corrections. The projection holds at most the ACTIVE cap of current
    components."""
    decls = validate_components(declarations, composition)
    by_component = {item.component_id: [] for item in decls}
    seen = set()
    for rev in tuple(revisions or ()):
        _validate_revision_shape(rev, composition)
        if rev.revision_id in seen:
            raise ComponentError("revision identity is duplicated")
        seen.add(rev.revision_id)
        if rev.component_id not in by_component:
            raise ComponentError("a revision names no declared component")
        by_component[rev.component_id].append(rev)
    records = []
    for item in decls:
        history = sorted(by_component[item.component_id], key=lambda r: r.revision_no)
        if [r.revision_no for r in history] != list(range(1, len(history) + 1)):
            raise ComponentError("revision history is not one contiguous chain")
        if any(r.kind == COMPONENT_REVISION_WITHDRAWN for r in history[:-1]):
            raise ComponentError("a revision follows a withdrawal")
        versions = [ComponentVersion(0, item.display_name, item.function_text,
                                     item.subsystem_ids)]
        for rev in history:
            if rev.kind == COMPONENT_REVISION_CORRECTED:
                versions.append(ComponentVersion(
                    rev.revision_no, rev.display_name, rev.function_text,
                    rev.subsystem_ids))
        latest = versions[-1]
        current = ProjectComponent(
            component_id=item.component_id, display_name=latest.display_name,
            function_text=latest.function_text, subsystem_ids=latest.subsystem_ids,
            provenance=OWNER_STATED, validation_state=UNVALIDATED)
        records.append(ComponentRecord(
            current=current, versions=tuple(versions),
            head_revision_no=len(history), corrections=len(versions) - 1,
            withdrawn=bool(history) and history[-1].kind == COMPONENT_REVISION_WITHDRAWN))
    inventory = ComponentInventory(records=tuple(records))
    if len(inventory.active) > MAX_PROJECT_COMPONENTS_PER_PROJECT:
        raise ComponentError("too many active components")
    return inventory


def _revisable_record(inventory, component_id, expected_revision_no):
    if not isinstance(inventory, ComponentInventory):
        raise ComponentError("no validated inventory")
    record = inventory.record_for(component_id) if isinstance(component_id, str) else None
    if record is None:
        raise ComponentUnknown("the component is not a component of this project")
    if record.withdrawn:
        raise ComponentAlreadyWithdrawn("the component is withdrawn")
    if expected_revision_no != record.head_revision_no:
        raise ComponentStale("the component changed since this version was read")
    return record


def corrected_component_revision(inventory, composition, component_id,
                                 expected_revision_no, display_name,
                                 function_text, subsystem_ids):
    """Build ONE correction of a CURRENT component against the validated
    ``inventory``: the component exists, is not withdrawn, has not changed
    since ``expected_revision_no`` and has a correction left; the complete
    new material is valid and differs from the current material. Raises a
    ``ComponentRevisionError`` subclass or ``ComponentError`` otherwise."""
    record = _revisable_record(inventory, component_id, expected_revision_no)
    if record.corrections >= MAX_CORRECTIONS_PER_COMPONENT:
        raise ComponentCorrectionLimit("the correction limit is reached")
    if not valid_subsystem_text(display_name, MAX_COMPONENT_NAME_LENGTH):
        raise ComponentError("component name is empty, invalid or too long")
    if not valid_subsystem_text(function_text, MAX_COMPONENT_FUNCTION_LENGTH):
        raise ComponentError("component function is empty, invalid or too long")
    parts = canonical_component_parts(composition, subsystem_ids)
    if same_component_material(record.current, ProjectComponent(
            component_id=component_id, display_name=display_name,
            function_text=function_text, subsystem_ids=parts,
            provenance=OWNER_STATED, validation_state=UNVALIDATED)):
        raise ComponentUnchanged("the correction changes nothing")
    return ComponentRevision(
        revision_id=new_component_revision_id(), component_id=component_id,
        revision_no=record.head_revision_no + 1,
        kind=COMPONENT_REVISION_CORRECTED, display_name=display_name,
        function_text=function_text, subsystem_ids=parts,
        provenance=OWNER_STATED, validation_state=UNVALIDATED)


def withdrawn_component_revision(inventory, component_id, expected_revision_no):
    """Build the ONE terminal withdrawal of a CURRENT component against the
    validated ``inventory`` (it exists, is not already withdrawn and has not
    changed since ``expected_revision_no``). The withdrawal slot is reserved:
    it is available even when every correction is used."""
    record = _revisable_record(inventory, component_id, expected_revision_no)
    return ComponentRevision(
        revision_id=new_component_revision_id(), component_id=component_id,
        revision_no=record.head_revision_no + 1,
        kind=COMPONENT_REVISION_WITHDRAWN, display_name=None,
        function_text=None, subsystem_ids=None,
        provenance=OWNER_STATED, validation_state=UNVALIDATED)


# --- COMPONENT-PROTOTYPE-NEED-NOTE-01: the inventor's prototype-need note -----
# For ONE existing ACTIVE declared component the inventor may record, replace
# or clear ONE optional, free-text planning statement of what they expect to
# need of that component for ONE prototype (e.g. "four similar wheel units").
# A CURRENT-VALUE attribute keyed ONLY by the component's stable
# ``component_id`` — never by its name, position or text. It is the inventor's
# own planning statement, OWNER_STATED / UNVALIDATED by construction: never a
# physical inventory count, a quantity, a component-equivalence assertion, a
# BOM line, a specification or a verified engineering requirement. Nothing is
# parsed, counted, converted, totalled, multiplied, grouped or matched; absence
# means NOT STATED, never a default of one. The component's identity, its
# revision material, its correction quota and the active / lifetime bounds are
# untouched: a correction keeps the component's id and so its note; a
# withdrawn component's note stays stored but is never presented as a current
# need; a later, separate declaration is a new identity and inherits nothing.
# The text policy follows the existing quantity-text discipline of
# ``engine.requirement_quantity`` (text only; outer whitespace stripped only;
# empty rejected; C0 / C1 control characters rejected; at most 120 Unicode code
# points; never truncated or reinterpreted) without extending that owner.
MAX_COMPONENT_PROTOTYPE_NEED_LENGTH = 120
# C0 controls (U+0000–U+001F: tab and line breaks included) and C1 controls
# (U+007F–U+009F), exactly the ``engine.requirement_quantity`` policy set.
_PROTOTYPE_NEED_CONTROL_RE = re.compile("[\\x00-\\x1f\\x7f-\\x9f]")


class ComponentPrototypeNeedError(ValueError):
    """A submitted or stored prototype-need note violates the bounded text
    policy or names no admissible component. Structural message only — never
    the inventor's text."""


@dataclass(frozen=True)
class ComponentPrototypeNeed:
    """The inventor's CURRENT prototype-need note for ONE declared component,
    identified ONLY by that component's ``component_id``. ``need_text`` is the
    stored (policy-normalised) text. OWNER_STATED and UNVALIDATED by
    construction; never evidence, a requirement, a count or a technical fact."""
    component_id: str
    need_text: str
    provenance: str = OWNER_STATED
    validation_state: str = UNVALIDATED


def normalize_prototype_need_text(text):
    """Apply the bounded text policy and return the stored form, or raise
    ``ComponentPrototypeNeedError``: text only; outer whitespace stripped only;
    empty rejected; C0 / C1 control characters rejected; more than
    ``MAX_COMPONENT_PROTOTYPE_NEED_LENGTH`` code points rejected. Deterministic
    and idempotent; nothing is parsed, converted or normalised otherwise."""
    if not isinstance(text, str):
        raise ComponentPrototypeNeedError("prototype need must be text")
    stripped = text.strip()
    if not stripped:
        raise ComponentPrototypeNeedError("prototype need is empty")
    if _PROTOTYPE_NEED_CONTROL_RE.search(stripped):
        raise ComponentPrototypeNeedError("prototype need contains control characters")
    if len(stripped) > MAX_COMPONENT_PROTOTYPE_NEED_LENGTH:
        raise ComponentPrototypeNeedError("prototype need is too long")
    return stripped


def is_stored_prototype_need_text(text):
    """True iff ``text`` is EXACTLY a stored (post-policy) prototype need."""
    try:
        return normalize_prototype_need_text(text) == text
    except ComponentPrototypeNeedError:
        return False


def validate_component_prototype_needs(needs, inventory):
    """Validate a project's stored prototype-need notes against its OWN
    validated ``ComponentInventory`` and return them as a tuple in declaration
    order, or raise ``ComponentPrototypeNeedError``. Empty is valid. Every
    entry must name a DISTINCT declared component of this project by its exact
    id (a note on a withdrawn component is valid stored history, never a
    current need), carry exactly the stored text form and the fixed
    OWNER_STATED / UNVALIDATED values. A note naming no declared component is
    an orphan and invalid — never remapped or dropped."""
    items = tuple(needs or ())
    if not items:
        return ()
    if not isinstance(inventory, ComponentInventory):
        raise ComponentPrototypeNeedError("no validated inventory")
    order = [record.component_id for record in inventory.records]
    seen = set()
    for item in items:
        if not isinstance(item, ComponentPrototypeNeed):
            raise ComponentPrototypeNeedError("entry is not a prototype need")
        if item.component_id not in order or item.component_id in seen:
            raise ComponentPrototypeNeedError(
                "prototype need names no distinct declared component")
        seen.add(item.component_id)
        if not is_stored_prototype_need_text(item.need_text):
            raise ComponentPrototypeNeedError("stored prototype need is invalid")
        if item.provenance != OWNER_STATED or item.validation_state != UNVALIDATED:
            raise ComponentPrototypeNeedError(
                "prototype need provenance / validation state is invalid")
    return tuple(sorted(items, key=lambda n: order.index(n.component_id)))


def current_prototype_needs(needs, inventory):
    """The prototype-need text of every CURRENT (not withdrawn) component that
    has one, as ``{component_id: need_text}``. A withdrawn component's note is
    never part of it. ``needs`` must already be validated against
    ``inventory``."""
    active = {component.component_id for component in inventory.active}
    return {item.component_id: item.need_text for item in needs or ()
            if item.component_id in active}


def prototype_need_target(inventory, component_id):
    """The ACTIVE ``ComponentRecord`` a prototype-need write may name, or
    raise: ``ComponentUnknown`` (not a declared component of this project) or
    ``ComponentAlreadyWithdrawn`` (withdrawn — a withdrawn component takes no
    new need)."""
    if not isinstance(inventory, ComponentInventory):
        raise ComponentError("no validated inventory")
    record = inventory.record_for(component_id) if isinstance(component_id, str) else None
    if record is None:
        raise ComponentUnknown("the component is not a component of this project")
    if record.withdrawn:
        raise ComponentAlreadyWithdrawn("the component is withdrawn")
    return record


# --- COMPONENT-INTERFACE-PARTICIPATION-01: components taking part in an
# interaction -----------------------------------------------------------------
# For ONE existing Owner-declared interaction the inventor may state which of
# the project's existing declared physical components take part in it. ONE row
# per (interaction, component) pair, keyed ONLY by the interaction's
# ``interface_id`` and the component's stable ``component_id`` — never by a
# name, a position or text. It is the inventor's own statement, OWNER_STATED /
# UNVALIDATED by construction: never a physical connection, an assembly step,
# a compatibility, completeness, suitability or safety fact, a BOM line or
# evidence. Nothing is inferred: participation is never derived from the
# component's part links, and no overlap with the interaction's two parts is
# required (a part link is itself only the inventor's association).
#
# CURRENT participation of an interaction = its stored rows whose component is
# ACTIVE in the validated inventory, in the inventory's declaration order.
# Stored rows of a component that was later withdrawn stay as history: they are
# never shown as current, never compared, reasserted or deleted by an ordinary
# replacement, and a withdrawn component can never be newly named. A
# correction keeps the component's id and so its participation; a later,
# separate declaration is a new identity and inherits nothing. Absence of any
# row reads NOT RECORDED; an unreadable collection reads UNAVAILABLE. The
# analytical-relationship NEXT TRIGGER was evaluated for this attribute: it is
# a current-value attribute of ONE existing interaction naming existing
# components (as a component's part links are an attribute of the component),
# not a new relation owner — no shared generic relationship primitive or graph
# is justified.


class InterfaceParticipationError(ValueError):
    """A submitted or stored participation violates the bounded contract.
    Structural message only — never user text."""


@dataclass(frozen=True)
class InterfaceParticipation:
    """ONE stored statement that the component ``component_id`` takes part in
    the interaction ``interface_id``. OWNER_STATED and UNVALIDATED by
    construction; never evidence, a requirement, a connection or a fact."""
    interface_id: str
    component_id: str
    provenance: str = OWNER_STATED
    validation_state: str = UNVALIDATED


def validate_interface_participations(participations, interfaces, inventory):
    """Validate a project's stored participation rows against its OWN durable
    ``interfaces`` and validated ``ComponentInventory`` and return them as a
    tuple in canonical order (interface order, then component declaration
    order), or raise ``InterfaceParticipationError``. Empty is valid. Every
    row must name an interaction of this project and a DECLARED component of
    this project (active or withdrawn — a withdrawn component's row is valid
    stored history) by exact id, at most once, with the fixed OWNER_STATED /
    UNVALIDATED values. An orphan is invalid — never remapped or dropped."""
    items = tuple(participations or ())
    if not items:
        return ()
    if not isinstance(inventory, ComponentInventory):
        raise InterfaceParticipationError("no validated inventory")
    interface_order = [item.interface_id for item in interfaces or ()]
    component_order = [record.component_id for record in inventory.records]
    seen = set()
    for item in items:
        if not isinstance(item, InterfaceParticipation):
            raise InterfaceParticipationError("entry is not a participation")
        if item.interface_id not in interface_order:
            raise InterfaceParticipationError(
                "participation names no interaction of this project")
        if item.component_id not in component_order:
            raise InterfaceParticipationError(
                "participation names no declared component of this project")
        pair = (item.interface_id, item.component_id)
        if pair in seen:
            raise InterfaceParticipationError("participation is duplicated")
        seen.add(pair)
        if item.provenance != OWNER_STATED or item.validation_state != UNVALIDATED:
            raise InterfaceParticipationError(
                "participation provenance / validation state is invalid")
    return tuple(sorted(items, key=lambda p: (interface_order.index(p.interface_id),
                                              component_order.index(p.component_id))))


def current_interface_participants(participations, active_components):
    """``{interface_id: (component_id, ...)}`` of every interaction with at
    least one CURRENT participant: stored rows whose component is in
    ``active_components`` (the inventory's active projection), in that
    projection's order. A withdrawn component is never part of it.
    ``participations`` must already be validated."""
    order = [component.component_id for component in active_components or ()]
    current = {}
    for item in participations or ():
        if item.component_id in order:
            current.setdefault(item.interface_id, []).append(item.component_id)
    return {interface_id: tuple(sorted(ids, key=order.index))
            for interface_id, ids in current.items()}


def participation_target(inventory, interfaces, interface_id, component_ids):
    """The canonical requested participant set for ONE interaction, as a
    tuple in declaration order, or raise: ``InterfaceParticipationError``
    (an interaction that is not one of ``interfaces``, a malformed or
    duplicated id, or a component that is not declared in this project) or
    ``ComponentAlreadyWithdrawn`` (a withdrawn component takes no new
    participation). Empty is valid (nothing recorded)."""
    if not isinstance(inventory, ComponentInventory):
        raise InterfaceParticipationError("no validated inventory")
    if interface_id not in {item.interface_id for item in interfaces or ()}:
        raise InterfaceParticipationError("the id names no interaction of this project")
    ids = tuple(component_ids or ())
    if len(set(ids)) != len(ids):
        raise InterfaceParticipationError("a component is named twice")
    for component_id in ids:
        if not is_valid_component_id(component_id):
            raise InterfaceParticipationError("malformed component identity")
        record = inventory.record_for(component_id)
        if record is None:
            raise InterfaceParticipationError(
                "the component is not a component of this project")
        if record.withdrawn:
            raise ComponentAlreadyWithdrawn("the component is withdrawn")
    order = [record.component_id for record in inventory.records]
    return tuple(sorted(ids, key=order.index))
