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
and changes nothing here. A further narrow, Owner-authorized exception
(CAP13-PLANAR-MOMENT-INTEGRATED-PART-01): the admitted request-local calculation
``cap13:planar_single_force_moment`` v1.0 may likewise be OFFERED for the declared
Mechanical part whatever the initial analysis focus, decided in the web layer
from the same validated durable composition; it establishes no applicability,
suitability, validation or safety and changes nothing here. A further narrow,
Owner-authorized exception (ROTATIONAL-LOAD-SLICE-01): the admitted request-local
calculation ``cap13:linear_speed_dependent_rotational_load`` v1.0 may likewise be
OFFERED for the declared Mechanical part whatever the initial analysis focus,
decided in the web layer from the same validated durable composition; it
establishes no applicability, suitability, validation or safety and changes nothing
here. A further narrow, Owner-authorized exception
(TMP36-NOMINAL-VOLTAGE-TEMPERATURE-01): the admitted request-local calculation
``tmp36:nominal_voltage_to_temperature`` v1.0 may likewise be OFFERED for the
declared Electrical / Electronics part whatever the initial analysis focus,
decided in the web layer from the same validated durable composition; it
establishes no sensor choice, applicability, suitability, validation or safety
and changes nothing here. A further narrow, Owner-authorized exception
(CAP13-PLANAR-REQUIRED-FORCE-01): the admitted request-local calculation
``cap13:planar_required_force`` v1.0 may likewise be OFFERED for the declared
Mechanical part whatever the initial analysis focus, decided in the web layer
from the same validated durable composition; it establishes no actuation,
applicability, suitability, validation or safety and changes nothing here. A further narrow,
Owner-authorized exception (DC-RESISTIVE-LOAD-INTEGRATED-PART-01): the three admitted
request-local calculations ``electrical:dc_resistive_load_current``,
``electrical:dc_resistive_load_power`` and ``electrical:dc_resistive_load_energy``, each
v1.0, may likewise be OFFERED for the declared Electrical / Electronics part whatever the
initial analysis focus, decided in the web layer from the same validated durable
composition; it establishes no load type, applicability, suitability, validation or
safety and changes nothing here. A further narrow, Owner-authorized exception
(DC-CONSTANT-CURRENT-CHARGE-01): the admitted request-local calculation
``electrical:dc_constant_current_charge`` v1.0 may likewise be OFFERED for the declared
Electrical / Electronics part whatever the initial analysis focus, decided in the web
layer from the same validated durable composition; it establishes no load, current
constancy, battery, applicability, suitability, validation or safety and changes
nothing here. A further narrow, Owner-authorized exception
(PWM-AVERAGE-VOLTAGE-01): the admitted request-local calculation
``electrical:pwm_average_voltage`` v1.0 may likewise be OFFERED for the declared
Electrical / Electronics part whatever the initial analysis focus, decided in the web
layer from the same validated durable composition; it establishes no waveform, load
response, applicability, suitability, validation or safety and changes nothing here. A
further narrow, Owner-authorized exception (CONTROL-CYCLE-INTEGRATED-PART-01): the
existing request-local 28-T4 evaluation ``control_cycle:ready_running_single_transition``
v1.0 and the existing composition
``temperature_control_condition:tmp36_threshold_ready_running`` v1.0 may likewise be
OFFERED for the declared Electrical / Electronics part whatever the initial analysis
focus, decided in the web layer from the same validated durable composition — the
composition only where both of its existing gates resolve to that SAME current part; it
establishes no control requirement, actuation, timing, compatibility, suitability,
validation or safety and changes nothing here. A
further narrow, Owner-authorized exception
(MEASUREMENT-PLANNING-INTEGRATED-PART-01): the three existing, read-only Electronics
measurement-planning guidance elements of the CAP-09 planning page (the measured-quantity
versus observed-condition guidance, the measurement-conditions awareness note and the
sensing / accuracy-resolution reference panel) may likewise be SHOWN for the declared
Electrical / Electronics part whatever the initial analysis focus, decided in the web layer
from the same validated durable composition; they say nothing about any experiment,
sensing need or technical assessment and change nothing here. A further narrow,
Owner-authorized exception (MECHANICAL-NATURAL-FREQUENCY-01): the admitted
request-local calculation ``mechanical:spring_mass_natural_frequency`` v1.0 may
likewise be OFFERED for the declared Mechanical part whatever the initial analysis
focus, decided in the web layer from the same validated durable composition; it
establishes no spring-mass system, model applicability, stiffness or mass value,
resonance, suitability, validation or safety and changes nothing here. A further narrow,
Owner-authorized exception (MECHANICAL-FREE-LINEAR-THERMAL-EXPANSION-01): the admitted
request-local calculation ``mechanical:free_linear_thermal_expansion`` v1.0 may likewise
be OFFERED for the declared Mechanical part whatever the initial analysis focus, decided
in the web layer from the same validated durable composition; it establishes no material,
coefficient, length, temperature change, model applicability, fit, clearance, stress,
suitability, validation or safety and changes nothing here. No other specialist
behaviour is granted by these exceptions. Subsystem identity is
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
from engine import mechanical_planar_clearance as _pcc
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


# --- PART-BOUND-TEMPERATURE-CHANGE-DECLARATION-01 (Increment A): the inventor's
# statement that ONE Mechanical part experiences a temperature change ----------
# ONE closed, positive, part-bound statement: the inventor states that the ONE
# identified Mechanical part of a valid durable Stage-15 composition experiences
# a temperature change during use. It is bound ONLY to that part's existing
# ``subsystem_id`` (never a ``component_id``, a name, a function text, a domain
# alone or a list position) and is OWNER_STATED / UNVALIDATED by construction:
# InventorAI records that the inventor made the statement, never that the
# physical condition was checked. It has no payload: its identity is the part,
# its kind is fixed, and its only state is whether it is CURRENTLY declared. So
# there is no correction operation (nothing could truthfully be corrected) —
# only DECLARE and WITHDRAW. NOT DECLARED (no current statement) means only that
# InventorAI holds no such statement, never that the part does not change
# temperature; a withdrawal removes the statement and is never a negative
# physical statement. The Stage-15 part itself is never edited, replaced,
# withdrawn or rebound by it. Nothing here is inferred from text, answers,
# constraints, interface preparation, components, keywords, a classifier, an
# LLM or a calculation, and nothing reads it to decide eligibility, routing,
# questions, readiness, progression, gaps or SafetySignal.
PART_TEMPERATURE_CHANGE_DOMAINS = ("mechanical",)


class PartTemperatureChangeError(ValueError):
    """A proposed or stored temperature-change statement names no Mechanical
    part of the project's own valid composition, or is malformed. Structural
    message only."""


@dataclass(frozen=True)
class PartTemperatureChangeDeclaration:
    """The inventor's CURRENT statement that the part ``subsystem_id``
    experiences a temperature change during use. OWNER_STATED / UNVALIDATED by
    construction; never a measurement, a validated condition or an input to
    any calculation, eligibility or routing."""
    subsystem_id: str
    provenance: str = OWNER_STATED
    validation_state: str = UNVALIDATED


def part_temperature_change_target(composition, subsystem_id):
    """The ``Subsystem`` a temperature-change statement may name: a part of
    THIS validated ``composition`` whose domain is in
    ``PART_TEMPERATURE_CHANGE_DOMAINS``, matched by its exact ``subsystem_id``;
    else ``PartTemperatureChangeError``. An empty composition (an ordinary
    project with no Stage-15 parts) admits nothing."""
    if not isinstance(subsystem_id, str) or not is_valid_subsystem_id(subsystem_id):
        raise PartTemperatureChangeError("malformed part identity")
    for sub in tuple(composition or ()):
        if sub.subsystem_id == subsystem_id:
            if sub.domain not in PART_TEMPERATURE_CHANGE_DOMAINS:
                raise PartTemperatureChangeError("the part is not a Mechanical part")
            return sub
    raise PartTemperatureChangeError("the part is not a part of this project")


def validate_part_temperature_changes(declarations, composition):
    """Validate a project's stored statements against its OWN validated
    ``composition`` and return them as a tuple in composition order, or raise
    ``PartTemperatureChangeError``. Empty is valid. Every entry must name a
    DISTINCT Mechanical part of this composition by its exact id and carry the
    fixed OWNER_STATED / UNVALIDATED values; anything else (an orphan, another
    part's domain, a duplicate) invalidates the WHOLE collection — never
    remapped, dropped or rebound."""
    items = tuple(declarations or ())
    if not items:
        return ()
    order = [sub.subsystem_id for sub in tuple(composition or ())]
    seen = set()
    for item in items:
        if not isinstance(item, PartTemperatureChangeDeclaration):
            raise PartTemperatureChangeError("entry is not a temperature-change statement")
        part_temperature_change_target(composition, item.subsystem_id)
        if item.subsystem_id in seen:
            raise PartTemperatureChangeError("duplicated statement")
        seen.add(item.subsystem_id)
        if item.provenance != OWNER_STATED or item.validation_state != UNVALIDATED:
            raise PartTemperatureChangeError(
                "statement provenance / validation state is invalid")
    return tuple(sorted(items, key=lambda d: order.index(d.subsystem_id)))


def part_temperature_change_declared(declarations, subsystem_id):
    """True iff ``subsystem_id`` has a CURRENT statement among ``declarations``
    (already validated). False means NOT DECLARED only."""
    return any(item.subsystem_id == subsystem_id for item in declarations or ())


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


# --- COMPONENT-PARTICIPATION-VERIFICATION-PREPARATION-01 ---------------------
# For ONE existing participation (ONE component taking part in ONE declared
# interaction) the inventor may record, in their own words, what they expect
# that component to contribute that could be observed, and the evidence or
# review they would need to check it. Verification PREPARATION only: both are
# OWNER_STATED / UNVALIDATED, never a mechanism, a compatibility, a
# feasibility, a requirement, evidence or a check that anything was verified.
# The pair is identified ONLY by the existing ``(interface_id, component_id)``;
# the interaction as a whole keeps its own ``InterfacePreparation``.
#
# Owner decision "keep, hide while absent": the notes are NOT part of the
# participation row. When the inventor removes the component from the
# interaction's participants the notes stay stored, are not shown, and are
# marked ``carried_over``; when the same participation is added again they are
# shown again, explicitly as earlier, unvalidated statements recorded before
# the removal - never as freshly reconfirmed - until the inventor saves them
# again. A withdrawn component's notes stay as history, are never current and
# take no new write; a later, separate declaration is a new identity and
# inherits nothing. Text follows the interface-preparation rule
# (``valid_preparation_text``, 1,000 characters each).
PARTICIPATION_EXPECTED_CONTRIBUTION = "expected_contribution"
PARTICIPATION_EVIDENCE_NEEDED = "evidence_needed"
PARTICIPATION_PREPARATION_FIELDS = (PARTICIPATION_EXPECTED_CONTRIBUTION,
                                    PARTICIPATION_EVIDENCE_NEEDED)
MAX_PARTICIPATION_PREPARATION_LENGTH = MAX_INTERFACE_PREPARATION_LENGTH


class ParticipationPreparationError(ValueError):
    """A submitted or stored participation preparation violates the bounded
    contract. Structural message only — never user text."""


@dataclass(frozen=True)
class ParticipationPreparation:
    """The inventor's notes for ONE participation, identified ONLY by
    ``(interface_id, component_id)``. Each field is the inventor's own trimmed
    text or ``None`` (not recorded); a value with both fields ``None`` is never
    stored. ``carried_over`` is True when the participation was removed after
    these notes were last saved: they are earlier statements, not current
    reconfirmed ones. OWNER_STATED / UNVALIDATED by construction."""
    interface_id: str
    component_id: str
    expected_contribution: Optional[str] = None
    evidence_needed: Optional[str] = None
    carried_over: bool = False
    provenance: str = OWNER_STATED
    validation_state: str = UNVALIDATED

    def value(self, field_name):
        if field_name not in PARTICIPATION_PREPARATION_FIELDS:
            raise ParticipationPreparationError("unknown participation preparation field")
        return getattr(self, field_name)

    def recorded_fields(self):
        return tuple(f for f in PARTICIPATION_PREPARATION_FIELDS
                     if getattr(self, f) is not None)


def validate_participation_preparations(preparations, interfaces, inventory):
    """Validate a project's stored participation preparations against its OWN
    durable ``interfaces`` and validated ``ComponentInventory`` and return them
    in canonical order (interface order, then component declaration order), or
    raise ``ParticipationPreparationError``. Empty is valid. Every entry must
    name an interaction of this project and a DECLARED component of this
    project (active or withdrawn — a withdrawn component's notes are valid
    stored history) by exact id, at most once, hold at least one note of valid
    stored text, a boolean ``carried_over`` and the fixed OWNER_STATED /
    UNVALIDATED values. An orphan is invalid — never remapped or dropped. A
    stored note need not have a stored participation: removal keeps it."""
    items = tuple(preparations or ())
    if not items:
        return ()
    if not isinstance(inventory, ComponentInventory):
        raise ParticipationPreparationError("no validated inventory")
    interface_order = [item.interface_id for item in interfaces or ()]
    component_order = [record.component_id for record in inventory.records]
    seen = set()
    for item in items:
        if not isinstance(item, ParticipationPreparation):
            raise ParticipationPreparationError("entry is not a participation preparation")
        if item.interface_id not in interface_order:
            raise ParticipationPreparationError(
                "preparation names no interaction of this project")
        if item.component_id not in component_order:
            raise ParticipationPreparationError(
                "preparation names no declared component of this project")
        pair = (item.interface_id, item.component_id)
        if pair in seen:
            raise ParticipationPreparationError("preparation is duplicated")
        seen.add(pair)
        if not item.recorded_fields():
            raise ParticipationPreparationError("a stored preparation records nothing")
        for field_name in item.recorded_fields():
            if not valid_preparation_text(getattr(item, field_name)):
                raise ParticipationPreparationError("preparation text is invalid")
        if not isinstance(item.carried_over, bool):
            raise ParticipationPreparationError("carried-over marker is invalid")
        if item.provenance != OWNER_STATED or item.validation_state != UNVALIDATED:
            raise ParticipationPreparationError(
                "preparation provenance / validation state is invalid")
    return tuple(sorted(items, key=lambda p: (interface_order.index(p.interface_id),
                                              component_order.index(p.component_id))))


def current_participation_preparations(preparations, participations, active_components):
    """``{(interface_id, component_id): ParticipationPreparation}`` for the
    CURRENT participations only (stored participation rows whose component is
    in ``active_components``). Notes of a removed participation or of a
    withdrawn component are never part of it. Inputs must already be
    validated."""
    current = {(interface_id, component_id)
               for interface_id, ids in current_interface_participants(
                   participations, active_components).items()
               for component_id in ids}
    return {(item.interface_id, item.component_id): item
            for item in preparations or ()
            if (item.interface_id, item.component_id) in current}


def participation_preparation_target(inventory, interfaces, participations,
                                     interface_id, component_id, values):
    """The canonical requested notes for ONE CURRENT participation, as a
    ``ParticipationPreparation`` (``carried_over`` False — saving makes them
    current) or ``None`` when both are cleared, or raise:
    ``ParticipationPreparationError`` (an interaction or component that is not
    this project's, a malformed id, a pair that is not a current participation,
    an unknown field or invalid text) or ``ComponentAlreadyWithdrawn`` (a
    withdrawn component takes no new note). ``values`` maps each of
    ``PARTICIPATION_PREPARATION_FIELDS`` to trimmed text or ``None``."""
    if not isinstance(inventory, ComponentInventory):
        raise ParticipationPreparationError("no validated inventory")
    if not is_valid_interface_id(interface_id) or not is_valid_component_id(component_id):
        raise ParticipationPreparationError("malformed identity")
    if interface_id not in {item.interface_id for item in interfaces or ()}:
        raise ParticipationPreparationError("the id names no interaction of this project")
    record = inventory.record_for(component_id)
    if record is None:
        raise ParticipationPreparationError("the component is not a component of this project")
    if record.withdrawn:
        raise ComponentAlreadyWithdrawn("the component is withdrawn")
    current = current_interface_participants(participations, inventory.active)
    if component_id not in current.get(interface_id, ()):
        raise ParticipationPreparationError("the component does not take part in this interaction")
    if not isinstance(values, dict) or set(values) != set(PARTICIPATION_PREPARATION_FIELDS):
        raise ParticipationPreparationError("unknown or missing participation preparation field")
    for text in values.values():
        if text is not None and not valid_preparation_text(text):
            raise ParticipationPreparationError("preparation text is empty, invalid or too long")
    if all(text is None for text in values.values()):
        return None
    return ParticipationPreparation(interface_id=interface_id, component_id=component_id,
                                    **values)


# --- BOARD-ENCLOSURE-PLANAR-CLEARANCE-01: the board-enclosure planar clearance
# declaration ------------------------------------------------------------------
# For ONE existing declared interaction of a valid integrated composition the
# inventor may declare which of TWO DISTINCT current participants is the board
# and which the enclosure, describe the board plane / selected usable region,
# and enter the nominal dimensions, the required clearance per side, optional
# basis notes and the eight applicability answers of the method contract
# (MECHANICAL_PLANAR_CENTERED_RECTANGULAR_CLEARANCE_METHOD_CONTRACT.md §5).
# These are INPUTS only - OWNER_STATED / UNVALIDATED by construction; no result
# is stored (calc/units §12): the comparison is derived on every read.
#
# Lifecycle: revision 0 declares an identity (``pcd-``); corrections append the
# COMPLETE new material (at most 20); ONE terminal withdrawal is reserved and
# available whatever the corrections used. History is never rewritten and a
# withdrawal is not erasure. At most ONE active declaration per interaction and
# at most 50 lifetime identities per project (resource limits only).
#
# Binding: every material revision records the board and enclosure component
# revision positions and each one's participation removal generation (the
# counter the participation writer increments when it removes that
# participation). A component correction or withdrawal, a lost participation,
# or a removal followed by re-addition therefore leaves the declaration
# NEEDS RECONFIRMATION - never silently revived - until the inventor rebinds
# it explicitly with a new correction. Rendering never writes.
PLANAR_CLEARANCE_DECLARED = "DECLARED"
PLANAR_CLEARANCE_CORRECTED = "CORRECTED"
PLANAR_CLEARANCE_WITHDRAWN = "WITHDRAWN"
PLANAR_CLEARANCE_KINDS = (PLANAR_CLEARANCE_DECLARED, PLANAR_CLEARANCE_CORRECTED,
                          PLANAR_CLEARANCE_WITHDRAWN)
MAX_PLANAR_CLEARANCE_IDENTITIES_PER_PROJECT = 50
MAX_PLANAR_CLEARANCE_CORRECTIONS = 20
# revision 0 + 20 corrections + one reserved terminal withdrawal
MAX_PLANAR_CLEARANCE_REVISION_NO = MAX_PLANAR_CLEARANCE_CORRECTIONS + 1
MAX_PLANAR_CLEARANCE_TEXT_LENGTH = 300
MAX_PLANAR_CLEARANCE_VERSION_TEXT = 80
PLANAR_CLEARANCE_BASIS_FIELDS = ("basis_board", "basis_region", "basis_clearance")

# BOARD-OUTLINE-SOURCE-BINDING-01 - the file-linked declaration shape. A v1
# declaration is source-free; a v2 declaration carries exactly ONE source binding:
# the identity, size and measured outline of ONE inspected KiCad board file and
# how its axes map onto the declared board. The binding is NOT the inventor's
# value and verifies nothing: the comparison always uses the DECLARED values, and
# whether the file outline equals them (EXACT / DIFFERS) is derived on read. The
# Mechanical method and its declaration constant are unchanged.
PLANAR_CLEARANCE_DECLARATION_V2 = "planar-clearance-declaration/2"
PLANAR_CLEARANCE_DECLARATION_VERSIONS = (_pcc.DECLARATION_VERSION,
                                         PLANAR_CLEARANCE_DECLARATION_V2)
PCC_SOURCE_KIND_KICAD = "kicad_pcb"
PCC_AXIS_FILE_X_IS_BOARD_X = "file_x_is_board_x"
PCC_AXIS_FILE_X_IS_BOARD_Y = "file_x_is_board_y"
PCC_SOURCE_AXIS_ASSIGNMENTS = (PCC_AXIS_FILE_X_IS_BOARD_X, PCC_AXIS_FILE_X_IS_BOARD_Y)
PCC_SOURCE_MAX_BYTES = 128 * 1024
_HEX64_RE = re.compile(r"^[0-9a-f]{64}$")
# Agreement of the file outline with the declared board (derived, never stored).
PCC_SOURCE_EXACT = "EXACT"
PCC_SOURCE_DIFFERS = "DIFFERS"
_PLANAR_CLEARANCE_ID_RE = re.compile(r"^pcd-[0-9a-f]{32}$")
_PLANAR_CLEARANCE_REVISION_ID_RE = re.compile(r"^pcr-[0-9a-f]{32}$")

# Binding issues (why a declaration needs reconfirmation), with the role.
PCC_ISSUE_COMPONENT_WITHDRAWN = "COMPONENT_WITHDRAWN"
PCC_ISSUE_COMPONENT_CHANGED = "COMPONENT_CHANGED"
PCC_ISSUE_NOT_PARTICIPATING = "NOT_PARTICIPATING"
PCC_ISSUE_PARTICIPATION_CHANGED = "PARTICIPATION_CHANGED"
PCC_ISSUE_METHOD_CHANGED = "METHOD_CHANGED"
PCC_ROLE_BOARD = "board"
PCC_ROLE_ENCLOSURE = "enclosure"


class PlanarClearanceError(ValueError):
    """A submitted or stored planar clearance declaration violates the bounded
    contract. Structural message only - never user text."""


class PlanarClearanceUnknown(PlanarClearanceError):
    """The revision names no declaration of this project."""


class PlanarClearanceStale(PlanarClearanceError):
    """The declaration, a component or a participation changed since the
    form was shown."""


class PlanarClearanceAlreadyWithdrawn(PlanarClearanceError):
    """The declaration is withdrawn: withdrawal is terminal."""


class PlanarClearanceCorrectionLimit(PlanarClearanceError):
    """The declaration holds the maximum number of corrections."""


class PlanarClearanceIdentityLimit(PlanarClearanceError):
    """The project holds the maximum number of declaration identities."""


class PlanarClearanceActiveExists(PlanarClearanceError):
    """The interaction already has an active declaration (correct it)."""


class PlanarClearanceUnchanged(PlanarClearanceError):
    """A correction that restates the current material and bindings exactly."""


class PlanarClearanceNotEligible(PlanarClearanceError):
    """The named components are not two distinct current participants of the
    interaction (or are not active components of this project)."""


class PlanarClearanceUnlinkNotAcknowledged(PlanarClearanceError):
    """With file-linked writes off, a correction of a file-linked declaration
    would save it without its file link, and the inventor has not explicitly
    acknowledged that for the CURRENT revision (missing or stale)."""


class PlanarClearanceSourceMismatch(PlanarClearanceError):
    """A file-linked declaration no longer matches what was inspected (the
    board, its revision or participation, or the declaration history changed),
    or a source binding is malformed or reused."""


@dataclass(frozen=True)
class PlanarClearanceSource:
    """ONE source binding of a v2 revision. ``file_x`` / ``file_y`` are the
    outline dimensions along the FILE's own axes (exact decimal text);
    ``axis_assignment`` says which declared board axis the file's x maps onto
    (bound by the save). A fresh inspection carries ``nonce_hash`` (the hash of
    its single-use inspection nonce, never the token); a carried-forward binding
    carries ``carry_forward_from`` (the revision whose binding it repeats) and
    no nonce hash."""
    kind: str
    source_sha256: str
    source_size: int
    format_id: str
    reader_id: str
    rule_id: str
    file_x: str
    file_y: str
    axis_assignment: str
    inspected_at: str
    nonce_hash: Optional[str]
    carry_forward_from: Optional[str]

    def board_dims(self):
        """The file outline as ``(board_x, board_y)`` under the axis assignment."""
        if self.axis_assignment == PCC_AXIS_FILE_X_IS_BOARD_Y:
            return self.file_y, self.file_x
        return self.file_x, self.file_y

    def same_inspection(self, other):
        """True when both bindings describe the same inspected outline and axis
        assignment (the nonce hash / carry-forward link aside)."""
        keys = ("kind", "source_sha256", "source_size", "format_id", "reader_id",
                "rule_id", "file_x", "file_y", "axis_assignment", "inspected_at")
        return all(getattr(self, k) == getattr(other, k) for k in keys)


def check_planar_clearance_source(source):
    """Shape-validate ONE stored or proposed source binding."""
    if not isinstance(source, PlanarClearanceSource):
        raise PlanarClearanceError("not a source binding")
    if source.kind != PCC_SOURCE_KIND_KICAD:
        raise PlanarClearanceError("unknown source kind")
    if not isinstance(source.source_sha256, str) or not _HEX64_RE.match(source.source_sha256):
        raise PlanarClearanceError("source digest malformed")
    if not _is_count(source.source_size, PCC_SOURCE_MAX_BYTES) or source.source_size < 1:
        raise PlanarClearanceError("source size malformed")
    for text in (source.format_id, source.reader_id, source.rule_id, source.inspected_at):
        if not valid_subsystem_text(text, MAX_PLANAR_CLEARANCE_VERSION_TEXT):
            raise PlanarClearanceError("source identity malformed")
    for value in (source.file_x, source.file_y):
        if not isinstance(value, str) or not _pcc.is_admitted_value("board_x", value):
            raise PlanarClearanceError("source dimension malformed")
    if source.axis_assignment not in PCC_SOURCE_AXIS_ASSIGNMENTS:
        raise PlanarClearanceError("unknown axis assignment")
    fresh = source.nonce_hash is not None
    if fresh == (source.carry_forward_from is not None):
        raise PlanarClearanceError("a binding is either fresh or carried forward")
    if fresh and (not isinstance(source.nonce_hash, str)
                  or not _HEX64_RE.match(source.nonce_hash)):
        raise PlanarClearanceError("nonce hash malformed")
    if not fresh and not is_valid_planar_clearance_revision_id(source.carry_forward_from):
        raise PlanarClearanceError("carry-forward link malformed")
    return source


def planar_clearance_source_agreement(material):
    """``None`` for a source-free material; otherwise ``(state, changed_axes,
    file_dims, declared_dims)``: EXACT when both declared board dimensions are
    entered and equal the file outline under the axis assignment by exact
    decimal comparison (84 == 84.0); DIFFERS otherwise. A value not entered or
    marked unknown never counts as EXACT (it is listed as changed)."""
    source = getattr(material, "source", None)
    if source is None:
        return None
    declared = material.values_map()
    file_dims = source.board_dims()
    changed = []
    for axis, role, file_value in (("x", "board_x", file_dims[0]),
                                   ("y", "board_y", file_dims[1])):
        value = declared.get(role)
        parsed = _pcc.parse_value(value) if isinstance(value, str) else None
        if parsed is None or parsed != _pcc.parse_value(file_value):
            changed.append(axis)
    state = PCC_SOURCE_EXACT if not changed else PCC_SOURCE_DIFFERS
    return (state, tuple(changed), file_dims,
            (declared.get("board_x"), declared.get("board_y")))


# What a region- or clearance-only correction may change (everything else must
# stay exactly as it was for a binding to be carried forward).
_PCC_CARRY_VALUE_ROLES = ("region_x", "region_y", _pcc.CLEARANCE_ROLE)
_PCC_CARRY_BASIS = ("basis_region", "basis_clearance")


def carry_forward_allowed(previous, material):
    """True when a correction to ``material`` may carry ``previous``'s source
    binding forward: ``previous`` is file-linked and the correction changes only
    the region (its values, description and note) and / or the clearance (its
    value and note) - the board and enclosure identities, revisions and
    participation generations, both declared board dimensions, the board note
    and every applicability answer stay exactly as they were."""
    if previous is None or getattr(previous, "source", None) is None:
        return False
    keys = ("interface_id", "board_component_id", "enclosure_component_id",
            "board_component_revision", "enclosure_component_revision",
            "board_participation_epoch", "enclosure_participation_epoch",
            "axis_pairing", "applicability", "method_id", "method_version")
    if any(getattr(previous, k) != getattr(material, k) for k in keys):
        return False
    old, new = previous.values_map(), material.values_map()
    if any(old.get(r) != new.get(r) for r in _pcc.VALUE_ROLES
           if r not in _PCC_CARRY_VALUE_ROLES):
        return False
    ob, nb = previous.basis_map(), material.basis_map()
    return all(ob.get(f) == nb.get(f) for f in PLANAR_CLEARANCE_BASIS_FIELDS
               if f not in _PCC_CARRY_BASIS)


@dataclass(frozen=True)
class PlanarClearanceMaterial:
    """The COMPLETE inventor material of one revision. ``values`` follows
    ``_pcc.VALUE_ROLES`` (exact decimal text, ``"unknown"`` or ``None``);
    ``basis`` follows ``PLANAR_CLEARANCE_BASIS_FIELDS``; ``applicability``
    follows ``_pcc.DECLARATION_IDS`` (answer or ``None``)."""
    interface_id: str
    board_component_id: str
    enclosure_component_id: str
    board_component_revision: int
    enclosure_component_revision: int
    board_participation_epoch: int
    enclosure_participation_epoch: int
    axis_pairing: str
    region_description: Optional[str]
    values: tuple
    basis: tuple
    applicability: tuple
    method_id: str
    method_version: str
    declaration_version: str
    source: Optional["PlanarClearanceSource"] = None

    def values_map(self):
        return dict(zip(_pcc.VALUE_ROLES, self.values))

    def basis_map(self):
        return dict(zip(PLANAR_CLEARANCE_BASIS_FIELDS, self.basis))

    def applicability_map(self):
        return dict(zip(_pcc.DECLARATION_IDS, self.applicability))

    def evaluation_input(self):
        """The material the method consumer evaluates (§7)."""
        return {"values": self.values_map(),
                "region_description": self.region_description,
                "applicability": self.applicability_map()}


@dataclass(frozen=True)
class PlanarClearanceRevision:
    """ONE append-only revision. A WITHDRAWN revision carries no material."""
    revision_id: str
    declaration_id: str
    revision_no: int
    kind: str
    interface_id: str
    material: Optional[PlanarClearanceMaterial]
    provenance: str = OWNER_STATED
    validation_state: str = UNVALIDATED


@dataclass(frozen=True)
class PlanarClearanceRecord:
    """ONE declaration identity with its validated history, oldest first.
    ``current`` is the latest material revision (``None`` never: revision 0
    always carries material); ``head_revision_no`` the latest position."""
    declaration_id: str
    interface_id: str
    revisions: tuple
    withdrawn: bool

    @property
    def head(self):
        return self.revisions[-1]

    @property
    def head_revision_no(self):
        return self.revisions[-1].revision_no

    @property
    def current_revision(self):
        return [r for r in self.revisions if r.material is not None][-1]

    @property
    def current(self):
        return self.current_revision.material

    @property
    def corrections(self):
        return len([r for r in self.revisions if r.kind == PLANAR_CLEARANCE_CORRECTED])


@dataclass(frozen=True)
class PlanarClearanceLedger:
    """The ONE authoritative projection of a project's declarations, in order
    of first declaration."""
    records: tuple

    def record_for(self, declaration_id):
        for record in self.records:
            if record.declaration_id == declaration_id:
                return record
        return None

    def active_for(self, interface_id):
        for record in self.records:
            if record.interface_id == interface_id and not record.withdrawn:
                return record
        return None

    def history_for(self, interface_id):
        return tuple(r for r in self.records if r.interface_id == interface_id)


def new_planar_clearance_id():
    return "pcd-" + uuid.uuid4().hex


def new_planar_clearance_revision_id():
    return "pcr-" + uuid.uuid4().hex


def is_valid_planar_clearance_id(value):
    return isinstance(value, str) and bool(_PLANAR_CLEARANCE_ID_RE.match(value))


def is_valid_planar_clearance_revision_id(value):
    return isinstance(value, str) and bool(_PLANAR_CLEARANCE_REVISION_ID_RE.match(value))


def valid_planar_clearance_text(value):
    """A stored description or basis note: non-empty, already trimmed, at most
    300 characters, free of NUL."""
    return valid_subsystem_text(value, MAX_PLANAR_CLEARANCE_TEXT_LENGTH)


def valid_planar_clearance_value(role, value):
    """``None`` (not entered), ``"unknown"`` or an admitted exact decimal."""
    return value is None or value == _pcc.VALUE_UNKNOWN \
        or _pcc.is_admitted_value(role, value)


def _is_count(value, upper=None):
    return (isinstance(value, int) and not isinstance(value, bool) and value >= 0
            and (upper is None or value <= upper))


def check_planar_clearance_material(material, interfaces, inventory):
    """Shape-validate ONE stored or proposed material against the project's
    interactions and DECLARED components (active or withdrawn: a stored
    binding to a later-withdrawn component is valid history). Raises
    ``PlanarClearanceError``."""
    if not isinstance(material, PlanarClearanceMaterial):
        raise PlanarClearanceError("not a planar clearance material")
    if not isinstance(inventory, ComponentInventory):
        raise PlanarClearanceError("no validated inventory")
    if material.interface_id not in {i.interface_id for i in interfaces or ()}:
        raise PlanarClearanceError("the material names no interaction of this project")
    for component_id in (material.board_component_id, material.enclosure_component_id):
        if not is_valid_component_id(component_id) \
                or inventory.record_for(component_id) is None:
            raise PlanarClearanceError("the material names no component of this project")
    if material.board_component_id == material.enclosure_component_id:
        raise PlanarClearanceError("board and enclosure are the same component")
    for count in (material.board_component_revision, material.enclosure_component_revision):
        if not _is_count(count, MAX_REVISIONS_PER_COMPONENT):
            raise PlanarClearanceError("component revision position out of range")
    for count in (material.board_participation_epoch, material.enclosure_participation_epoch):
        if not _is_count(count):
            raise PlanarClearanceError("participation generation malformed")
    if material.axis_pairing != _pcc.AXIS_PAIRING:
        raise PlanarClearanceError("unknown axis pairing")
    if material.region_description is not None \
            and not valid_planar_clearance_text(material.region_description):
        raise PlanarClearanceError("region description invalid")
    if not isinstance(material.values, tuple) \
            or len(material.values) != len(_pcc.VALUE_ROLES) \
            or not all(valid_planar_clearance_value(role, value)
                       for role, value in zip(_pcc.VALUE_ROLES, material.values)):
        raise PlanarClearanceError("values malformed")
    if not isinstance(material.basis, tuple) \
            or len(material.basis) != len(PLANAR_CLEARANCE_BASIS_FIELDS) \
            or not all(v is None or valid_planar_clearance_text(v) for v in material.basis):
        raise PlanarClearanceError("basis notes malformed")
    if not isinstance(material.applicability, tuple) \
            or len(material.applicability) != len(_pcc.DECLARATION_IDS) \
            or not all(v is None or v in _pcc.ANSWERS for v in material.applicability):
        raise PlanarClearanceError("applicability answers malformed")
    for text in (material.method_id, material.method_version, material.declaration_version):
        if not valid_subsystem_text(text, MAX_PLANAR_CLEARANCE_VERSION_TEXT):
            raise PlanarClearanceError("version identity malformed")
    # BOARD-OUTLINE-SOURCE-BINDING-01: v2 carries exactly one binding; every
    # other declaration shape carries none.
    if material.declaration_version == PLANAR_CLEARANCE_DECLARATION_V2:
        check_planar_clearance_source(material.source)
    elif material.source is not None:
        raise PlanarClearanceError("a source-free declaration carries a binding")
    return material


def project_planar_clearance(revisions, interfaces, inventory):
    """Validate a project's COMPLETE declaration history WHOLE and return the
    ``PlanarClearanceLedger``, or raise ``PlanarClearanceError`` (nothing
    partial). Each identity: positions exactly 0..k; revision 0 DECLARED,
    then CORRECTED (at most 20), then at most one terminal WITHDRAWN; one
    interaction for life; distinct revision ids; at most one active identity
    per interaction and at most 50 identities per project."""
    by_id, order, seen = {}, [], set()
    for rev in tuple(revisions or ()):
        if not isinstance(rev, PlanarClearanceRevision):
            raise PlanarClearanceError("history entry is not a revision")
        if not is_valid_planar_clearance_id(rev.declaration_id) \
                or not is_valid_planar_clearance_revision_id(rev.revision_id):
            raise PlanarClearanceError("identity malformed")
        if rev.revision_id in seen:
            raise PlanarClearanceError("revision identity duplicated")
        seen.add(rev.revision_id)
        if rev.provenance != OWNER_STATED or rev.validation_state != UNVALIDATED:
            raise PlanarClearanceError("provenance / validation state invalid")
        if not _is_count(rev.revision_no, MAX_PLANAR_CLEARANCE_REVISION_NO) \
                or rev.kind not in PLANAR_CLEARANCE_KINDS:
            raise PlanarClearanceError("revision position or kind invalid")
        if rev.kind == PLANAR_CLEARANCE_WITHDRAWN:
            if rev.material is not None:
                raise PlanarClearanceError("a withdrawal carries material")
            if rev.interface_id not in {i.interface_id for i in interfaces or ()}:
                raise PlanarClearanceError("withdrawal names no interaction")
        else:
            check_planar_clearance_material(rev.material, interfaces, inventory)
            if rev.material.interface_id != rev.interface_id:
                raise PlanarClearanceError("material interaction mismatch")
        if rev.declaration_id not in by_id:
            by_id[rev.declaration_id] = []
            order.append(rev.declaration_id)
        by_id[rev.declaration_id].append(rev)
    if len(order) > MAX_PLANAR_CLEARANCE_IDENTITIES_PER_PROJECT:
        raise PlanarClearanceError("too many declaration identities")
    records, active, nonces = [], set(), set()
    for declaration_id in order:
        history = sorted(by_id[declaration_id], key=lambda r: r.revision_no)
        if [r.revision_no for r in history] != list(range(len(history))):
            raise PlanarClearanceError("history is not one contiguous chain")
        kinds = [r.kind for r in history]
        if kinds[0] != PLANAR_CLEARANCE_DECLARED \
                or any(k != PLANAR_CLEARANCE_CORRECTED for k in kinds[1:-1]) \
                or (len(kinds) > 1 and kinds[-1] == PLANAR_CLEARANCE_DECLARED):
            raise PlanarClearanceError("history kinds out of order")
        corrections = kinds.count(PLANAR_CLEARANCE_CORRECTED)
        if corrections > MAX_PLANAR_CLEARANCE_CORRECTIONS:
            raise PlanarClearanceError("too many corrections")
        if len({r.interface_id for r in history}) != 1:
            raise PlanarClearanceError("declaration changed interaction")
        previous = None
        for rev in history:
            source = rev.material.source if rev.material is not None else None
            if source is not None:
                if source.nonce_hash is not None:
                    if source.nonce_hash in nonces:
                        raise PlanarClearanceError("an inspection was used twice")
                    nonces.add(source.nonce_hash)
                elif (previous is None or previous.revision_id != source.carry_forward_from
                      or rev.kind != PLANAR_CLEARANCE_CORRECTED
                      or not carry_forward_allowed(previous.material, rev.material)
                      or not previous.material.source.same_inspection(source)):
                    raise PlanarClearanceError("a carried-forward binding is not admissible")
            previous = rev
        withdrawn = kinds[-1] == PLANAR_CLEARANCE_WITHDRAWN
        interface_id = history[0].interface_id
        if not withdrawn:
            if interface_id in active:
                raise PlanarClearanceError("two active declarations for one interaction")
            active.add(interface_id)
        records.append(PlanarClearanceRecord(
            declaration_id=declaration_id, interface_id=interface_id,
            revisions=tuple(history), withdrawn=withdrawn))
    return PlanarClearanceLedger(records=tuple(records))


def planar_clearance_binding_issues(material, inventory, participations, epochs):
    """Why a CURRENT material needs reconfirmation, as a tuple of
    ``(issue, role)`` in a fixed order; empty when every binding still holds.
    ``participations`` must already be validated; ``epochs`` maps
    ``(interface_id, component_id)`` to the removal generation (absent = 0)."""
    issues = []
    current = current_interface_participants(participations, inventory.active)
    participants = current.get(material.interface_id, ())
    for role, component_id, revision, epoch in (
            (PCC_ROLE_BOARD, material.board_component_id,
             material.board_component_revision, material.board_participation_epoch),
            (PCC_ROLE_ENCLOSURE, material.enclosure_component_id,
             material.enclosure_component_revision,
             material.enclosure_participation_epoch)):
        record = inventory.record_for(component_id)
        if record is None or record.withdrawn:
            issues.append((PCC_ISSUE_COMPONENT_WITHDRAWN, role))
            continue
        if record.head_revision_no != revision:
            issues.append((PCC_ISSUE_COMPONENT_CHANGED, role))
        if component_id not in participants:
            issues.append((PCC_ISSUE_NOT_PARTICIPATING, role))
        elif epochs.get((material.interface_id, component_id), 0) != epoch:
            issues.append((PCC_ISSUE_PARTICIPATION_CHANGED, role))
    if (material.method_id, material.method_version) != (_pcc.METHOD_ID, _pcc.METHOD_VERSION) \
            or material.declaration_version not in PLANAR_CLEARANCE_DECLARATION_VERSIONS:
        issues.append((PCC_ISSUE_METHOD_CHANGED, None))
    return tuple(issues)


def planar_clearance_material(inventory, interfaces, participations, epochs,
                              interface_id, board_component_id,
                              enclosure_component_id, expected_board_revision,
                              expected_enclosure_revision, expected_board_epoch,
                              expected_enclosure_epoch, region_description,
                              values, basis, applicability, source=None):
    """Build the COMPLETE material of a new revision against CURRENT durable
    truth: the interaction is this project's; the board and enclosure are two
    distinct ACTIVE components that currently take part in it
    (``PlanarClearanceNotEligible``); their revision positions and removal
    generations equal what the form showed (``PlanarClearanceStale``); every
    value, note and answer is admissible (``PlanarClearanceError``). The
    bindings are stamped from durable truth, never from the client."""
    if not isinstance(inventory, ComponentInventory):
        raise PlanarClearanceError("no validated inventory")
    if interface_id not in {i.interface_id for i in interfaces or ()}:
        raise PlanarClearanceError("the id names no interaction of this project")
    if board_component_id == enclosure_component_id:
        raise PlanarClearanceNotEligible("board and enclosure must be different")
    participants = current_interface_participants(
        participations, inventory.active).get(interface_id, ())
    stamped = []
    for component_id, expected_revision, expected_epoch in (
            (board_component_id, expected_board_revision, expected_board_epoch),
            (enclosure_component_id, expected_enclosure_revision,
             expected_enclosure_epoch)):
        record = inventory.record_for(component_id) \
            if is_valid_component_id(component_id) else None
        if record is None or record.withdrawn or component_id not in participants:
            raise PlanarClearanceNotEligible(
                "the component is not a current participant of this interaction")
        epoch = epochs.get((interface_id, component_id), 0)
        if expected_revision != record.head_revision_no or expected_epoch != epoch:
            raise PlanarClearanceStale("the component or participation changed")
        stamped.append((record.head_revision_no, epoch))
    material = PlanarClearanceMaterial(
        interface_id=interface_id, board_component_id=board_component_id,
        enclosure_component_id=enclosure_component_id,
        board_component_revision=stamped[0][0],
        enclosure_component_revision=stamped[1][0],
        board_participation_epoch=stamped[0][1],
        enclosure_participation_epoch=stamped[1][1],
        axis_pairing=_pcc.AXIS_PAIRING, region_description=region_description,
        values=tuple(values), basis=tuple(basis), applicability=tuple(applicability),
        method_id=_pcc.METHOD_ID, method_version=_pcc.METHOD_VERSION,
        declaration_version=(_pcc.DECLARATION_VERSION if source is None
                             else PLANAR_CLEARANCE_DECLARATION_V2),
        source=source)
    return check_planar_clearance_material(material, interfaces, inventory)


def declared_planar_clearance(ledger, material):
    """Revision 0 of a NEW identity: no active declaration exists for the
    interaction and an identity is left."""
    if not isinstance(ledger, PlanarClearanceLedger):
        raise PlanarClearanceError("no validated ledger")
    if ledger.active_for(material.interface_id) is not None:
        raise PlanarClearanceActiveExists("an active declaration exists")
    if len(ledger.records) >= MAX_PLANAR_CLEARANCE_IDENTITIES_PER_PROJECT:
        raise PlanarClearanceIdentityLimit("the identity limit is reached")
    return PlanarClearanceRevision(
        revision_id=new_planar_clearance_revision_id(),
        declaration_id=new_planar_clearance_id(), revision_no=0,
        kind=PLANAR_CLEARANCE_DECLARED, interface_id=material.interface_id,
        material=material)


def _revisable(ledger, declaration_id, expected_head):
    if not isinstance(ledger, PlanarClearanceLedger):
        raise PlanarClearanceError("no validated ledger")
    record = ledger.record_for(declaration_id) \
        if is_valid_planar_clearance_id(declaration_id) else None
    if record is None:
        raise PlanarClearanceUnknown("no such declaration")
    if record.withdrawn:
        raise PlanarClearanceAlreadyWithdrawn("the declaration is withdrawn")
    if expected_head != record.head_revision_no:
        raise PlanarClearanceStale("the declaration changed")
    return record


def corrected_planar_clearance(ledger, declaration_id, expected_head, material):
    """The next CORRECTED revision with the COMPLETE new material (which may
    rebind the board / enclosure); refuses an exact restatement."""
    record = _revisable(ledger, declaration_id, expected_head)
    if material.interface_id != record.interface_id:
        raise PlanarClearanceError("a correction cannot change the interaction")
    if record.corrections >= MAX_PLANAR_CLEARANCE_CORRECTIONS:
        raise PlanarClearanceCorrectionLimit("the correction limit is reached")
    if material == record.current:
        raise PlanarClearanceUnchanged("the correction changes nothing")
    return PlanarClearanceRevision(
        revision_id=new_planar_clearance_revision_id(),
        declaration_id=declaration_id, revision_no=record.head_revision_no + 1,
        kind=PLANAR_CLEARANCE_CORRECTED, interface_id=record.interface_id,
        material=material)


def withdrawn_planar_clearance(ledger, declaration_id, expected_head):
    """The ONE reserved terminal withdrawal (available whatever corrections
    were used)."""
    record = _revisable(ledger, declaration_id, expected_head)
    return PlanarClearanceRevision(
        revision_id=new_planar_clearance_revision_id(),
        declaration_id=declaration_id, revision_no=record.head_revision_no + 1,
        kind=PLANAR_CLEARANCE_WITHDRAWN, interface_id=record.interface_id,
        material=None)


def same_planar_clearance_action(stored, revision):
    """True when ``revision`` restates the action ``stored`` committed: the
    same kind, interaction and material, and - except for a first declaration,
    whose identity is generated afresh on each attempt - the same identity and
    position (the revision id, provenance and validation state are not
    material)."""
    if (stored.kind, stored.interface_id, stored.material) != (
            revision.kind, revision.interface_id, revision.material):
        return False
    if stored.kind == PLANAR_CLEARANCE_DECLARED:
        return revision.revision_no == 0
    return (stored.declaration_id, stored.revision_no) == (
        revision.declaration_id, revision.revision_no)


# =============================================================================
# G1-PLANAR-MOMENT-SAVED-DECLARATION-01 - the inventor's saved planar-moment
# configurations (Owner-authorized; the moment contract §§12-13 as amended).
# =============================================================================
# ONE revisioned, append-only declaration of the INPUTS of the existing CAP-13
# planar single-force moment (``cap13:planar_single_force_moment``) for ONE
# inventor-declared component: the exact entered force and perpendicular
# distance, the five declarations, the nine screen answers, and the inventor's
# own description of the chosen point and of the force context. The calculated
# moment is NEVER stored: it is re-derived on every read through the unchanged
# consumer (calc / units §12 unchanged; the shared owner stays stateless).
#
# Lifecycle (the planar-clearance pattern): revision 0 DECLARED, at most 20
# CORRECTED revisions (each with the COMPLETE material), then ONE reserved
# terminal WITHDRAWN revision available whatever the corrections used.
# Withdrawal is not erasure. A declaration is bound to its component for life.
# At most ONE active declaration per component and at most 50 lifetime
# identities per project: bounded first-slice resource limits, never a claim
# that a component has only one force or one point.
#
# Binding: every material revision records the component's revision position,
# the ONE declared Mechanical part it was saved for (integrated projects; None
# on a Mechanical-focus project without a composition) and the method identity
# (method id / version and the governed artifact's version and digest). A
# component correction or withdrawal, a lost part link, or a changed method or
# governed artifact leaves the declaration NEEDS RECONFIRMATION - no number is
# shown - until the inventor explicitly re-saves it as a correction. Every
# saved configuration was ADMITTED by the existing method at its serialized
# save (all declarations apply, no screen item is yes, both values are
# admitted and the consumer returned SUCCESS). The component association, the
# point and the force context are OWNER_STATED / UNVALIDATED: the declared
# component is not established to carry that force, and a saved configuration
# is not a complete force or component assessment, an evidence item, a
# verified design, a compatibility or a safety statement.
from engine import cap13_planar_moment as _cap13m  # noqa: E402

PLANAR_MOMENT_DECLARED = "DECLARED"
PLANAR_MOMENT_CORRECTED = "CORRECTED"
PLANAR_MOMENT_WITHDRAWN = "WITHDRAWN"
PLANAR_MOMENT_KINDS = (PLANAR_MOMENT_DECLARED, PLANAR_MOMENT_CORRECTED,
                       PLANAR_MOMENT_WITHDRAWN)
MAX_PLANAR_MOMENT_IDENTITIES_PER_PROJECT = 50
MAX_PLANAR_MOMENT_CORRECTIONS = 20
# revision 0 + 20 corrections + one reserved terminal withdrawal
MAX_PLANAR_MOMENT_REVISION_NO = MAX_PLANAR_MOMENT_CORRECTIONS + 1
MAX_PLANAR_MOMENT_TEXT_LENGTH = 300
MAX_PLANAR_MOMENT_VERSION_TEXT = 80
PLANAR_MOMENT_DECLARATION_VERSION = "planar-moment-declaration/1"
PLANAR_MOMENT_DECLARATION_VERSIONS = (PLANAR_MOMENT_DECLARATION_VERSION,)
PLANAR_MOMENT_VALUE_ROLES = tuple(role for role, _unit in _cap13m.VALUE_ROLES)
PLANAR_MOMENT_PART_DOMAIN = _cap13m.ELIGIBLE_ROOT_DOMAIN
_PLANAR_MOMENT_ID_RE = re.compile(r"^pmd-[0-9a-f]{32}$")
_PLANAR_MOMENT_REVISION_ID_RE = re.compile(r"^pmr-[0-9a-f]{32}$")
_PM_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")

# Why a CURRENT material needs reconfirmation (fixed order).
PM_ISSUE_COMPONENT_WITHDRAWN = "COMPONENT_WITHDRAWN"
PM_ISSUE_COMPONENT_CHANGED = "COMPONENT_CHANGED"
PM_ISSUE_PART_LINK_LOST = "PART_LINK_LOST"
PM_ISSUE_METHOD_CHANGED = "METHOD_CHANGED"
PM_ISSUES = (PM_ISSUE_COMPONENT_WITHDRAWN, PM_ISSUE_COMPONENT_CHANGED,
             PM_ISSUE_PART_LINK_LOST, PM_ISSUE_METHOD_CHANGED)


class PlanarMomentError(ValueError):
    """A submitted or stored planar-moment declaration violates the bounded
    contract. Structural message only - never user text."""


class PlanarMomentUnknown(PlanarMomentError):
    """The revision names no declaration of this project."""


class PlanarMomentStale(PlanarMomentError):
    """The declaration or its component changed since the form was shown."""


class PlanarMomentAlreadyWithdrawn(PlanarMomentError):
    """The declaration is withdrawn: withdrawal is terminal."""


class PlanarMomentCorrectionLimit(PlanarMomentError):
    """The declaration holds the maximum number of corrections."""


class PlanarMomentIdentityLimit(PlanarMomentError):
    """The project holds the maximum number of declaration identities."""


class PlanarMomentActiveExists(PlanarMomentError):
    """The component already has an active saved configuration (correct it)."""


class PlanarMomentUnchanged(PlanarMomentError):
    """A correction that restates the current material and bindings exactly."""


class PlanarMomentNotEligible(PlanarMomentError):
    """The component is not an active component this calculation may be saved
    for (on an integrated project: one linked to the declared Mechanical part;
    otherwise: a Mechanical-focus project), or the project is not eligible."""


class PlanarMomentNotAdmitted(PlanarMomentError):
    """The configuration is not admitted by the existing method (a declaration
    does not apply, a screen item is yes, a value is not admitted, or the
    consumer did not return SUCCESS): nothing is saved."""


@dataclass(frozen=True)
class PlanarMomentMaterial:
    """The COMPLETE inventor material of one revision. ``values`` follows
    ``PLANAR_MOMENT_VALUE_ROLES`` (the exact entered text); ``declarations``
    follows ``_cap13m.DECLARATION_IDS``; ``screen`` follows
    ``_cap13m.SCREEN_ITEMS``. ``part_id`` is the declared Mechanical part the
    configuration was saved for, or None (no integrated composition)."""
    component_id: str
    component_revision: int
    part_id: Optional[str]
    point_description: str
    force_context: str
    values: tuple
    declarations: tuple
    screen: tuple
    method_id: str
    method_version: str
    artifact_version: str
    artifact_sha256: str
    declaration_version: str

    def values_map(self):
        return dict(zip(PLANAR_MOMENT_VALUE_ROLES, self.values))

    def captured(self):
        """The consumer's captured-submission shape (``capture_form``'s
        output) for this material: re-evaluation runs the SAME consumer."""
        return {"declarations": dict(zip(_cap13m.DECLARATION_IDS, self.declarations)),
                "screen": dict(zip(_cap13m.SCREEN_ITEMS, self.screen)),
                "values": self.values_map()}


@dataclass(frozen=True)
class PlanarMomentRevision:
    """ONE append-only revision. A WITHDRAWN revision carries no material."""
    revision_id: str
    declaration_id: str
    revision_no: int
    kind: str
    component_id: str
    material: Optional[PlanarMomentMaterial]
    provenance: str = OWNER_STATED
    validation_state: str = UNVALIDATED


@dataclass(frozen=True)
class PlanarMomentRecord:
    """ONE declaration identity with its validated history, oldest first."""
    declaration_id: str
    component_id: str
    revisions: tuple
    withdrawn: bool

    @property
    def head(self):
        return self.revisions[-1]

    @property
    def head_revision_no(self):
        return self.revisions[-1].revision_no

    @property
    def current_revision(self):
        return [r for r in self.revisions if r.material is not None][-1]

    @property
    def current(self):
        return self.current_revision.material

    @property
    def corrections(self):
        return len([r for r in self.revisions if r.kind == PLANAR_MOMENT_CORRECTED])


@dataclass(frozen=True)
class PlanarMomentLedger:
    """The ONE authoritative projection of a project's saved configurations,
    in order of first declaration."""
    records: tuple

    def record_for(self, declaration_id):
        for record in self.records:
            if record.declaration_id == declaration_id:
                return record
        return None

    def active_for(self, component_id):
        for record in self.records:
            if record.component_id == component_id and not record.withdrawn:
                return record
        return None


def new_planar_moment_id():
    return "pmd-" + uuid.uuid4().hex


def new_planar_moment_revision_id():
    return "pmr-" + uuid.uuid4().hex


def is_valid_planar_moment_id(value):
    return isinstance(value, str) and bool(_PLANAR_MOMENT_ID_RE.match(value))


def is_valid_planar_moment_revision_id(value):
    return isinstance(value, str) and bool(_PLANAR_MOMENT_REVISION_ID_RE.match(value))


def valid_planar_moment_text(value):
    """A stored point description or force context: non-empty, already
    trimmed, at most 300 characters, free of NUL and control characters."""
    return valid_subsystem_text(value, MAX_PLANAR_MOMENT_TEXT_LENGTH)


def planar_moment_admitted_shape(declarations, screen, values):
    """True only for a COMPLETE configuration the method admits before its
    owner runs: every declaration applies, every screen item is no, and both
    values are admitted unsigned decimals greater than zero (the consumer's
    own grammar). The consumer's SUCCESS is required on top of this."""
    if tuple(declarations) != (_cap13m.ANSWER_APPLIES,) * len(_cap13m.DECLARATION_IDS):
        return False
    if tuple(screen) != (_cap13m.SCREEN_NO,) * len(_cap13m.SCREEN_ITEMS):
        return False
    if len(tuple(values)) != len(PLANAR_MOMENT_VALUE_ROLES):
        return False
    for text in values:
        number = _cap13m.parse_number(text)
        if number is None or number <= 0.0:
            return False
    return True


def _pm_mechanical_part(composition):
    matches = [s for s in tuple(composition or ())
               if getattr(s, "domain", None) == PLANAR_MOMENT_PART_DOMAIN]
    return matches[0] if len(matches) == 1 else None


def planar_moment_target_part(composition, root_domain, component):
    """The part an ACTIVE ``component`` may be saved for, as ``(eligible,
    part_id)``: on an integrated project (a declared Mechanical part exists)
    only a component the inventor linked to that part, saved for it; otherwise
    any component of a Mechanical-focus project, saved for no part. Nothing is
    inferred from a name, a function text or a list position."""
    part = _pm_mechanical_part(composition)
    if part is not None:
        if component is not None and part.subsystem_id in component.subsystem_ids:
            return True, part.subsystem_id
        return False, None
    if not tuple(composition or ()) and root_domain == PLANAR_MOMENT_PART_DOMAIN:
        return component is not None, None
    return False, None


def check_planar_moment_material(material, inventory, composition):
    """Shape-validate ONE stored or proposed material against the project's
    DECLARED components (active or withdrawn: a stored binding to a later
    withdrawn component is valid history) and its composition. Raises
    ``PlanarMomentError``."""
    if not isinstance(material, PlanarMomentMaterial):
        raise PlanarMomentError("not a planar moment material")
    if not isinstance(inventory, ComponentInventory):
        raise PlanarMomentError("no validated inventory")
    if not is_valid_component_id(material.component_id) \
            or inventory.record_for(material.component_id) is None:
        raise PlanarMomentError("the material names no component of this project")
    if not _is_count(material.component_revision, MAX_REVISIONS_PER_COMPONENT):
        raise PlanarMomentError("component revision position out of range")
    if material.part_id is not None and material.part_id not in {
            s.subsystem_id for s in tuple(composition or ())}:
        raise PlanarMomentError("the material names no part of this project")
    for text in (material.point_description, material.force_context):
        if not valid_planar_moment_text(text):
            raise PlanarMomentError("description invalid")
    if not isinstance(material.values, tuple) or not isinstance(material.declarations, tuple) \
            or not isinstance(material.screen, tuple) \
            or len(material.declarations) != len(_cap13m.DECLARATION_IDS) \
            or len(material.screen) != len(_cap13m.SCREEN_ITEMS) \
            or not all(isinstance(v, str) and 0 < len(v) <= _cap13m.MAX_VALUE_CHARS
                       for v in material.values) \
            or not planar_moment_admitted_shape(material.declarations, material.screen,
                                                material.values):
        raise PlanarMomentNotAdmitted("the configuration is not admitted")
    for text in (material.method_id, material.method_version, material.artifact_version,
                 material.declaration_version):
        if not valid_subsystem_text(text, MAX_PLANAR_MOMENT_VERSION_TEXT):
            raise PlanarMomentError("version identity malformed")
    if not isinstance(material.artifact_sha256, str) \
            or not _PM_SHA256_RE.match(material.artifact_sha256):
        raise PlanarMomentError("artifact digest malformed")
    return material


def project_planar_moments(revisions, inventory, composition):
    """Validate a project's COMPLETE declaration history WHOLE and return the
    ``PlanarMomentLedger``, or raise ``PlanarMomentError`` (nothing partial).
    Each identity: positions exactly 0..k; revision 0 DECLARED, then CORRECTED
    (at most 20), then at most one terminal WITHDRAWN; one component for life;
    distinct revision ids; at most one active identity per component and at
    most 50 identities per project."""
    by_id, order, seen = {}, [], set()
    for rev in tuple(revisions or ()):
        if not isinstance(rev, PlanarMomentRevision):
            raise PlanarMomentError("history entry is not a revision")
        if not is_valid_planar_moment_id(rev.declaration_id) \
                or not is_valid_planar_moment_revision_id(rev.revision_id):
            raise PlanarMomentError("identity malformed")
        if rev.revision_id in seen:
            raise PlanarMomentError("revision identity duplicated")
        seen.add(rev.revision_id)
        if rev.provenance != OWNER_STATED or rev.validation_state != UNVALIDATED:
            raise PlanarMomentError("provenance / validation state invalid")
        if not _is_count(rev.revision_no, MAX_PLANAR_MOMENT_REVISION_NO) \
                or rev.kind not in PLANAR_MOMENT_KINDS:
            raise PlanarMomentError("revision position or kind invalid")
        if not is_valid_component_id(rev.component_id) \
                or inventory.record_for(rev.component_id) is None:
            raise PlanarMomentError("the revision names no component of this project")
        if rev.kind == PLANAR_MOMENT_WITHDRAWN:
            if rev.material is not None:
                raise PlanarMomentError("a withdrawal carries material")
        else:
            check_planar_moment_material(rev.material, inventory, composition)
            if rev.material.component_id != rev.component_id:
                raise PlanarMomentError("material component mismatch")
        if rev.declaration_id not in by_id:
            by_id[rev.declaration_id] = []
            order.append(rev.declaration_id)
        by_id[rev.declaration_id].append(rev)
    if len(order) > MAX_PLANAR_MOMENT_IDENTITIES_PER_PROJECT:
        raise PlanarMomentError("too many declaration identities")
    records, active = [], set()
    for declaration_id in order:
        history = sorted(by_id[declaration_id], key=lambda r: r.revision_no)
        if [r.revision_no for r in history] != list(range(len(history))):
            raise PlanarMomentError("history is not one contiguous chain")
        kinds = [r.kind for r in history]
        if kinds[0] != PLANAR_MOMENT_DECLARED \
                or any(k != PLANAR_MOMENT_CORRECTED for k in kinds[1:-1]) \
                or (len(kinds) > 1 and kinds[-1] == PLANAR_MOMENT_DECLARED):
            raise PlanarMomentError("history kinds out of order")
        if kinds.count(PLANAR_MOMENT_CORRECTED) > MAX_PLANAR_MOMENT_CORRECTIONS:
            raise PlanarMomentError("too many corrections")
        if len({r.component_id for r in history}) != 1:
            raise PlanarMomentError("declaration changed component")
        withdrawn = kinds[-1] == PLANAR_MOMENT_WITHDRAWN
        component_id = history[0].component_id
        if not withdrawn:
            if component_id in active:
                raise PlanarMomentError("two active declarations for one component")
            active.add(component_id)
        records.append(PlanarMomentRecord(
            declaration_id=declaration_id, component_id=component_id,
            revisions=tuple(history), withdrawn=withdrawn))
    return PlanarMomentLedger(records=tuple(records))


def planar_moment_binding_issues(material, inventory, composition, root_domain,
                                 current_identity):
    """Why a CURRENT material needs reconfirmation, as a tuple from
    ``PM_ISSUES`` in fixed order; empty when every binding still holds.
    ``current_identity`` is ``(method_id, method_version, artifact_version,
    artifact_sha256)`` of the CURRENT consumer and governed artifact, read by
    the store (``engine.record_store.planar_moment_method_identity``; None when
    the artifact cannot be read: METHOD_CHANGED, fail closed). This module does
    no IO."""
    issues = []
    record = inventory.record_for(material.component_id)
    if record is None or record.withdrawn:
        issues.append(PM_ISSUE_COMPONENT_WITHDRAWN)
    else:
        if record.head_revision_no != material.component_revision:
            issues.append(PM_ISSUE_COMPONENT_CHANGED)
        eligible, part_id = planar_moment_target_part(composition, root_domain,
                                                      record.current)
        if not eligible or part_id != material.part_id:
            issues.append(PM_ISSUE_PART_LINK_LOST)
    stored = (material.method_id, material.method_version, material.artifact_version,
              material.artifact_sha256)
    if current_identity is None or stored != tuple(current_identity) \
            or material.declaration_version not in PLANAR_MOMENT_DECLARATION_VERSIONS:
        issues.append(PM_ISSUE_METHOD_CHANGED)
    return tuple(issues)


def planar_moment_material(inventory, composition, root_domain, component_id,
                           expected_revision, point_description, force_context,
                           values, declarations, screen, current_identity):
    """Build the COMPLETE material of a new revision against CURRENT durable
    truth: the component is an ACTIVE component this calculation may be saved
    for (``PlanarMomentNotEligible``); its revision position equals what the
    form showed (``PlanarMomentStale``); the configuration is admitted in
    shape (``PlanarMomentNotAdmitted``) and every text is admissible. The
    bindings and the method identity are stamped from durable / current truth,
    never from the client."""
    if not isinstance(inventory, ComponentInventory):
        raise PlanarMomentError("no validated inventory")
    if current_identity is None:
        raise PlanarMomentNotAdmitted("the method's governed content is unavailable")
    record = inventory.record_for(component_id) \
        if is_valid_component_id(component_id) else None
    if record is None or record.withdrawn:
        raise PlanarMomentNotEligible("the component is not an active component")
    eligible, part_id = planar_moment_target_part(composition, root_domain, record.current)
    if not eligible:
        raise PlanarMomentNotEligible("the component cannot carry this calculation here")
    if expected_revision != record.head_revision_no:
        raise PlanarMomentStale("the component changed")
    method_id, method_version, artifact_version, artifact_sha256 = current_identity
    material = PlanarMomentMaterial(
        component_id=component_id, component_revision=record.head_revision_no,
        part_id=part_id, point_description=point_description,
        force_context=force_context, values=tuple(values),
        declarations=tuple(declarations), screen=tuple(screen),
        method_id=method_id, method_version=method_version,
        artifact_version=artifact_version, artifact_sha256=artifact_sha256,
        declaration_version=PLANAR_MOMENT_DECLARATION_VERSION)
    return check_planar_moment_material(material, inventory, composition)


def declared_planar_moment(ledger, material):
    """Revision 0 of a NEW identity: no active declaration exists for the
    component and an identity is left."""
    if not isinstance(ledger, PlanarMomentLedger):
        raise PlanarMomentError("no validated ledger")
    if ledger.active_for(material.component_id) is not None:
        raise PlanarMomentActiveExists("an active saved configuration exists")
    if len(ledger.records) >= MAX_PLANAR_MOMENT_IDENTITIES_PER_PROJECT:
        raise PlanarMomentIdentityLimit("the identity limit is reached")
    return PlanarMomentRevision(
        revision_id=new_planar_moment_revision_id(),
        declaration_id=new_planar_moment_id(), revision_no=0,
        kind=PLANAR_MOMENT_DECLARED, component_id=material.component_id,
        material=material)


def _pm_revisable(ledger, declaration_id, expected_head):
    if not isinstance(ledger, PlanarMomentLedger):
        raise PlanarMomentError("no validated ledger")
    record = ledger.record_for(declaration_id) \
        if is_valid_planar_moment_id(declaration_id) else None
    if record is None:
        raise PlanarMomentUnknown("no such declaration")
    if record.withdrawn:
        raise PlanarMomentAlreadyWithdrawn("the declaration is withdrawn")
    if expected_head != record.head_revision_no:
        raise PlanarMomentStale("the declaration changed")
    return record


def corrected_planar_moment(ledger, declaration_id, expected_head, material):
    """The next CORRECTED revision with the COMPLETE new material (which
    re-stamps the component revision, the part and the method identity, so a
    correction is also the explicit reconfirmation); refuses an exact
    restatement."""
    record = _pm_revisable(ledger, declaration_id, expected_head)
    if material.component_id != record.component_id:
        raise PlanarMomentError("a correction cannot change the component")
    if record.corrections >= MAX_PLANAR_MOMENT_CORRECTIONS:
        raise PlanarMomentCorrectionLimit("the correction limit is reached")
    if material == record.current:
        raise PlanarMomentUnchanged("the correction changes nothing")
    return PlanarMomentRevision(
        revision_id=new_planar_moment_revision_id(),
        declaration_id=declaration_id, revision_no=record.head_revision_no + 1,
        kind=PLANAR_MOMENT_CORRECTED, component_id=record.component_id,
        material=material)


def withdrawn_planar_moment(ledger, declaration_id, expected_head):
    """The ONE reserved terminal withdrawal (available whatever corrections
    were used)."""
    record = _pm_revisable(ledger, declaration_id, expected_head)
    return PlanarMomentRevision(
        revision_id=new_planar_moment_revision_id(),
        declaration_id=declaration_id, revision_no=record.head_revision_no + 1,
        kind=PLANAR_MOMENT_WITHDRAWN, component_id=record.component_id,
        material=None)


def same_planar_moment_action(stored, revision):
    """True when ``revision`` restates the action ``stored`` committed: the
    same kind, component and material, and - except for a first declaration,
    whose identity is generated afresh on each attempt - the same identity and
    position."""
    if (stored.kind, stored.component_id, stored.material) != (
            revision.kind, revision.component_id, revision.material):
        return False
    if stored.kind == PLANAR_MOMENT_DECLARED:
        return revision.revision_no == 0
    return (stored.declaration_id, stored.revision_no) == (
        revision.declaration_id, revision.revision_no)
