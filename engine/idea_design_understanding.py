# -*- coding: utf-8 -*-
"""IDEA-DESIGN-UNDERSTANDING-PROJECTION-01 — one read-only composition of the
project's existing canonical truth into a structured design-understanding view.

What this module owns, and only this:
  * the deterministic COMPOSITION of outputs that existing owners already
    produce, into fixed presentation sections in a fixed order;
  * the presentation GROUPING of those outputs (section keys, item order);
  * REFERENCES back to the canonical owner records (ids the owners minted).

What it does not own (and never derives, infers, renames or re-labels):
  * provenance, validation, disposition, interpretation status, resolution
    state, requirement authority, criticality, responsibility — every such
    attribute is copied from its owner under the owner's OWN field name
    (``Item.attributes``); a field the owner does not carry is not invented;
  * any cross-owner relationship: a ``Link`` is emitted only where the owner
    record itself holds the identity it points to (an interface's endpoint
    ids, a component's part ids, a record's question target, a requirement's
    canonical anchor, a routed need's question, a reading's quoted grounding).
    Items shown together in one section or one picture are not thereby
    related — not a component to a function, not a reading to a part, not a
    capability to an unresolved item;
  * engineering applicability, compatibility, progression, readiness,
    eligibility, design choice, component or mechanism generation.

Placement under a section is presentation metadata only. "System organized"
is never a token on an item. The reserved term for future system proposals is
NOT used here: the picture carries a fixed boundary disclosure instead.

Sources arrive already read (``Sources``): the web adapter reads the durable
inputs through the EXISTING readers (the project envelope's seed statement,
the #849 functional-handoff view with its Step-6 actions, the #836 idea-stated
unknown, the Stage-15 composite reader ``load_parts_components_interactions``
and the prototype-need reader). This module performs no I/O. The pure engine
derivations it reads from the state are the existing owners' own functions.

Statuses: a section is PRESENT when it holds at least one item; ABSENT when
the owner read succeeded and holds nothing; UNAVAILABLE when the owner could
not be read or validated (never rendered as "none"). Only a missing or
malformed ledger refuses the whole picture; the Stage-15 cluster (parts,
components, interactions) inherits its composite reader's own all-or-nothing
boundary; every other section is independent.
"""
from dataclasses import dataclass
from typing import Optional

from engine import idea_state as _ledger
from engine import need_routing as _routing
from engine import subsystem_model as _composition
from engine.functional_need_handoff import INTERPRETATION_STATUS as _READING_STATUS
from engine.idea_development_outputs import derive_next_development_step
from engine.requirement_landscape import derive_requirement_landscape

# --- section keys (presentation structure only, fixed order) -------------------
SECTION_ORIGINAL_IDEA = "original_idea"
SECTION_RECORDED_UNDERSTANDING = "recorded_understanding"
SECTION_FUNCTIONAL_READINGS = "functional_readings"
SECTION_STATED_UNKNOWNS = "stated_unknowns"
SECTION_CONSTRAINTS = "constraints"
SECTION_PARTS = "parts"
SECTION_COMPONENTS = "components"
SECTION_INTERACTIONS = "interactions"
SECTION_UNRESOLVED_WORK = "unresolved_work"
SECTION_ENGINEERING_CONTINUATIONS = "engineering_continuations"

SECTION_KEYS = (
    SECTION_ORIGINAL_IDEA, SECTION_RECORDED_UNDERSTANDING,
    SECTION_FUNCTIONAL_READINGS, SECTION_STATED_UNKNOWNS, SECTION_CONSTRAINTS,
    SECTION_PARTS, SECTION_COMPONENTS, SECTION_INTERACTIONS,
    SECTION_UNRESOLVED_WORK, SECTION_ENGINEERING_CONTINUATIONS,
)

# --- section statuses -------------------------------------------------------------
PRESENT = "PRESENT"
ABSENT = "ABSENT"
UNAVAILABLE = "UNAVAILABLE"

# --- the closed link vocabulary: each kind names the owner field it is read from --
LINK_PART = "part"                      # subsystem id held by the owner record
LINK_COMPONENT = "component"            # component id held by a participation row
LINK_RECORD = "record"                  # ledger record id held by the owner record
LINK_GAP = "gap"                        # gap_context / gap_type held by the record
LINK_QUESTION = "question"              # question_target / question_id held by it
LINK_DEPENDENT_PART = "dependent_part"  # InterfaceDependency.dependent_subsystem_id
LINK_DEPENDS_ON_PART = "depends_on_part"  # InterfaceDependency.depends_on_subsystem_id
LINK_REQUIREMENT_ANCHOR = "requirement_anchor"  # DerivedRequirement.primary_anchor
LINK_GROUNDING_QUOTE = "grounding_quote"  # ProposedRole.groundings (exact span)
LINK_KINDS = frozenset({
    LINK_PART, LINK_COMPONENT, LINK_RECORD, LINK_GAP, LINK_QUESTION,
    LINK_DEPENDENT_PART, LINK_DEPENDS_ON_PART, LINK_REQUIREMENT_ANCHOR,
    LINK_GROUNDING_QUOTE,
})

# --- content kinds: the owner record kind each item is a projection of -----------
KIND_IDEA_STATEMENT = "idea_statement"
KIND_ANSWER = "answer"
KIND_PROVISIONAL_ASSUMPTION = "provisional_assumption"
KIND_NON_ANSWER = "non_answer"
KIND_IDEA_STATED_UNKNOWN = "idea_stated_unknown"
KIND_ACKNOWLEDGED_UNKNOWN = "acknowledged_unknown"
KIND_FUNCTIONAL_ROLE = "functional_role"
KIND_CONSTRAINT = "constraint"
KIND_PART = "part"
KIND_COMPONENT = "component"
KIND_INTERACTION = "interaction"
KIND_GAP = "gap"
KIND_ROUTED_NEED = "routed_need"
KIND_DECLARED_CONTRADICTION = "declared_contradiction"
KIND_REQUIREMENT = "requirement"
KIND_NEXT_DEVELOPMENT_STEP = "next_development_step"
KIND_ENGINEERING_CONTINUATION = "engineering_continuation"

# --- owner names, as references to the canonical owner (documentation values) ---
OWNER_SEED_STATEMENT = "project_envelope.seed_idea_text"
OWNER_LEDGER_RECORD = "engine.idea_state.AssertionRecord"
OWNER_ACKNOWLEDGED_UNKNOWN = "engine.idea_state.AcknowledgedUnknown"
OWNER_IDEA_STATED_UNKNOWN = "engine.intent_serving.idea_stated_unknown"
OWNER_FUNCTIONAL_READING = "engine.functional_need_handoff.project_functional_roles"
OWNER_CONSTRAINT = "engine.idea_state.constraint_history"
OWNER_PART = "engine.subsystem_model.Subsystem"
OWNER_COMPONENT = "engine.subsystem_model.ProjectComponent"
OWNER_INTERACTION = "engine.subsystem_model.SubsystemInterface"
OWNER_GAP = "engine.idea_state.Gap"
OWNER_ROUTED_NEED = "engine.need_routing.outstanding_needs"
OWNER_CONTRADICTION = "engine.idea_state.active_declared_contradiction_pairs"
OWNER_REQUIREMENT = "engine.requirement_landscape.DerivedRequirement"
OWNER_NEXT_STEP = "engine.idea_development_outputs.derive_next_development_step"
OWNER_CONTINUATION = "web.app._handoff_actions"   # Step 6 presentation / action output

# The inventor's own provenance values, exactly as the #843 / #849 views read them.
_INVENTOR_PROVENANCE = ("OWNER_STATED", "LEGACY_UNSPECIFIED")
_RECORDED_DISPOSITIONS = (_ledger.DISPOSITION_ANSWERED,
                          _ledger.DISPOSITION_PROVISIONAL_ASSUMPTION)
_UNKNOWN_DISPOSITIONS = (_ledger.DISPOSITION_UNKNOWN, _ledger.DISPOSITION_DEFERRED)


class _Unreadable:
    """Sentinel: the owner should have been readable but could not be read or
    validated. Distinct from ``None`` (read fine, nothing there)."""
    __slots__ = ()

    def __repr__(self):
        return "UNREADABLE"


UNREADABLE = _Unreadable()


@dataclass(frozen=True)
class Link:
    kind: str
    reference: str


@dataclass(frozen=True)
class Item:
    """One projected owner record. ``attributes`` is a tuple of ``(name,
    value)`` pairs under the OWNER's field names; only fields the owner holds
    are present. ``links`` holds only identity-bound references the owner
    record itself carries."""
    content_kind: str
    owner: str
    reference: str
    text: Optional[str]
    attributes: tuple = ()
    links: tuple = ()

    def attribute(self, name, default=None):
        for key, value in self.attributes:
            if key == name:
                return value
        return default


@dataclass(frozen=True)
class Section:
    """``details``: owner-native section-level facts (e.g. the handoff's
    abstained count). ``unavailable``: names of OPTIONAL inputs of this section
    that could not be read while the section itself still renders."""
    key: str
    status: str
    items: tuple = ()
    details: tuple = ()
    unavailable: tuple = ()


@dataclass(frozen=True)
class DesignUnderstanding:
    """``available`` is False only when no usable ledger exists (whole-view
    refusal). ``names`` maps part / component ids to the inventor's own display
    names so a link can be shown by name instead of by internal id."""
    available: bool
    sections: tuple = ()
    names: tuple = ()

    def section(self, key):
        for section in self.sections:
            if section.key == key:
                return section
        return None

    def name_of(self, reference):
        for key, value in self.names:
            if key == reference:
                return value
        return None


@dataclass(frozen=True)
class Sources:
    """Everything the composer reads. Each optional input is the owner's value,
    ``None`` (read fine, nothing there) or ``UNREADABLE``.

    ``state``: the page's ``IdeaState`` (live, or the cold-load state).
    ``derived_available``: False when the state is a cold, unreconstructed
    one (``state.domain is None``), where the progression-derived truth
    (gaps, routes, requirement rows, next step) is not present — the existing
    Compass applies the same rule.
    ``original_idea``: the verbatim seed statement.
    ``functional_handoff``: the EXISTING #849 session view dict (with the
    Step-6 ``action`` on each capability), ``None`` when that view shows
    nothing, ``{"available": False}`` or ``UNREADABLE`` on failure.
    ``idea_stated_unknown``: the #836 sentence, verbatim.
    ``composition``: the EXISTING ``load_parts_components_interactions``
    mapping, read in that reader's own snapshot.
    ``prototype_needs``: ``{component_id: need_text}`` for the SAME current
    components, or ``UNREADABLE`` when the notes could not be read or belong
    to a different component state."""
    state: object
    derived_available: bool = True
    original_idea: object = None
    functional_handoff: object = None
    idea_stated_unknown: object = None
    composition: object = UNREADABLE
    prototype_needs: object = UNREADABLE


def unavailable():
    """The whole-view refusal value."""
    return DesignUnderstanding(available=False)


def compose(sources):
    """Compose the picture. Pure, deterministic, read-only; mutates nothing."""
    state = sources.state
    records = _ledger_records(state)
    if records is None:
        return unavailable()
    names = []
    sections = (
        _original_idea(sources.original_idea),
        _recorded_understanding(records),
        _functional_readings(sources.functional_handoff),
        _stated_unknowns(state, records, sources.idea_stated_unknown),
        _constraints(records),
    )
    sections += _stage15_cluster(sources.composition, sources.prototype_needs, names)
    sections += (
        _unresolved_work(state, records, sources.derived_available),
        _engineering_continuations(sources.functional_handoff),
    )
    return DesignUnderstanding(available=True, sections=tuple(sections),
                               names=tuple(names))


# --- helpers ------------------------------------------------------------------------
def _ledger_records(state):
    """The ledger as a list, or None when there is no usable ledger: no state,
    a non-iterable ledger, an entry without an id, or a duplicated id."""
    if state is None:
        return None
    try:
        records = list(getattr(state, "assertions", None) or ())
    except TypeError:
        return None
    seen = set()
    for record in records:
        record_id = getattr(record, "record_id", None)
        if not isinstance(record_id, str) or not record_id or record_id in seen:
            return None
        seen.add(record_id)
    return records


def _own(record, *names):
    """``(name, value)`` for every named owner field the record carries with a
    non-None value — the owner's names, never translated."""
    out = []
    for name in names:
        value = getattr(record, name, None)
        if value is not None:
            out.append((name, value))
    return tuple(out)


def _section_for(key, items, details=(), unavailable_inputs=()):
    status = PRESENT if items else ABSENT
    return Section(key=key, status=status, items=tuple(items),
                   details=tuple(details), unavailable=tuple(unavailable_inputs))


def _unavailable_section(key):
    return Section(key=key, status=UNAVAILABLE)


def _is_active_inventor_record(record):
    return (getattr(record, "superseded_by", None) is None
            and getattr(record, "provenance", None) in _INVENTOR_PROVENANCE)


def _record_links(record):
    links = []
    gap = getattr(record, "gap_context", None)
    if isinstance(gap, str) and gap:
        links.append(Link(LINK_GAP, gap))
    target = getattr(record, "question_target", None)
    if isinstance(target, str) and target:
        links.append(Link(LINK_QUESTION, target))
    return tuple(links)


def _record_item(record, kind):
    return Item(
        content_kind=kind, owner=OWNER_LEDGER_RECORD,
        reference=record.record_id,
        text=(getattr(record, "content", None) or "").strip() or None,
        attributes=_own(record, "provenance", "validation_status", "disposition",
                        "gap_context", "question_target", "iteration"),
        links=_record_links(record))


# --- sections -----------------------------------------------------------------------
def _original_idea(seed):
    if seed is UNREADABLE:
        return _unavailable_section(SECTION_ORIGINAL_IDEA)
    if not isinstance(seed, str) or not seed.strip():
        return _section_for(SECTION_ORIGINAL_IDEA, ())
    return _section_for(SECTION_ORIGINAL_IDEA, (Item(
        content_kind=KIND_IDEA_STATEMENT, owner=OWNER_SEED_STATEMENT,
        reference="seed_idea_text", text=seed),))


def _recorded_understanding(records):
    """The inventor's ACTIVE recorded answers and declared assumptions, in
    ledger order — the same active / inventor-provenance / disposition filter
    the #843 view applies; every record keeps its own fields."""
    items = []
    for record in records:
        if not _is_active_inventor_record(record):
            continue
        disposition = getattr(record, "disposition", None)
        if disposition not in _RECORDED_DISPOSITIONS:
            continue
        kind = (KIND_PROVISIONAL_ASSUMPTION
                if disposition == _ledger.DISPOSITION_PROVISIONAL_ASSUMPTION
                else KIND_ANSWER)
        item = _record_item(record, kind)
        if item.text:
            items.append(item)
    return _section_for(SECTION_RECORDED_UNDERSTANDING, items)


def _handoff_roles(view):
    """``(roles, abstained, idea_available)`` from the #849 view, or None when
    that view is unavailable."""
    if view is UNREADABLE or view is None:
        return ((), 0, None) if view is None else None
    if not isinstance(view, dict) or not view.get("available"):
        return None
    return (tuple(view.get("roles") or ()), int(view.get("abstained") or 0),
            view.get("idea_available"))


def _quote_links(quotes):
    links = []
    for quote in quotes or ():
        kind = getattr(quote, "source_kind", None)
        ref = getattr(quote, "source_ref", None)
        start = getattr(quote, "start", None)
        end = getattr(quote, "end", None)
        if kind is None or ref is None or start is None or end is None:
            continue
        links.append(Link(LINK_GROUNDING_QUOTE, "%s:%s:%s-%s" % (kind, ref, start, end)))
    return tuple(links)


def _quote_texts(quotes):
    return tuple(getattr(q, "quote", None) for q in quotes or ()
                 if isinstance(getattr(q, "quote", None), str))


def _functional_readings(view):
    resolved = _handoff_roles(view)
    if resolved is None:
        return _unavailable_section(SECTION_FUNCTIONAL_READINGS)
    roles, abstained, idea_available = resolved
    items = []
    for role in roles:
        groundings = role.get("groundings") or ()
        items.append(Item(
            content_kind=KIND_FUNCTIONAL_ROLE, owner=OWNER_FUNCTIONAL_READING,
            reference="%s:%s" % (role.get("role"), role.get("object")),
            text=None,
            attributes=(
                ("role", role.get("role")),
                ("object_key", role.get("object")),
                ("status", role.get("status")),
                ("interpretation_status", _READING_STATUS),
                ("groundings", _quote_texts(groundings)),
                ("negations", _quote_texts(role.get("negations"))),
                ("method_uncertainties", _quote_texts(role.get("uncertain"))),
            ),
            links=_quote_links(groundings)))
    details = []
    if abstained:
        details.append(("abstained", abstained))
    if idea_available is False:
        details.append(("idea_available", False))
    return _section_for(SECTION_FUNCTIONAL_READINGS, items, details)


def _stated_unknowns(state, records, idea_unknown):
    items = []
    unreadable = []
    if idea_unknown is UNREADABLE:
        unreadable.append("idea_stated_unknown")
    elif isinstance(idea_unknown, str) and idea_unknown.strip():
        items.append(Item(
            content_kind=KIND_IDEA_STATED_UNKNOWN, owner=OWNER_IDEA_STATED_UNKNOWN,
            reference="seed_idea_text", text=idea_unknown))
    for index, unknown in enumerate(getattr(state, "acknowledged_unknowns", None) or (), 1):
        verbatim = getattr(unknown, "verbatim", None)
        if not isinstance(verbatim, str) or not verbatim.strip():
            continue
        gap = getattr(unknown, "gap_context", None)
        items.append(Item(
            content_kind=KIND_ACKNOWLEDGED_UNKNOWN, owner=OWNER_ACKNOWLEDGED_UNKNOWN,
            reference="acknowledged_unknown:%d" % index, text=verbatim,
            attributes=_own(unknown, "iteration", "gap_context", "category_basis"),
            links=(Link(LINK_GAP, gap),) if isinstance(gap, str) and gap else ()))
    for record in records:
        if not _is_active_inventor_record(record):
            continue
        if getattr(record, "disposition", None) not in _UNKNOWN_DISPOSITIONS:
            continue
        items.append(_record_item(record, KIND_NON_ANSWER))
    return _section_for(SECTION_STATED_UNKNOWNS, items, (), unreadable)


def _constraints(records):
    try:
        history = _ledger.constraint_history(records)
    except Exception:
        return _unavailable_section(SECTION_CONSTRAINTS)
    by_id = {r.record_id: r for r in records}
    items = []
    for constraint in sorted(history.constraints, key=lambda c: c.position):
        if constraint.withdrawn:
            continue
        head = by_id.get(constraint.record_id)
        attributes = (("strength", constraint.strength),
                      ("corrections", constraint.corrections))
        if head is not None:
            attributes += _own(head, "provenance", "validation_status")
        items.append(Item(
            content_kind=KIND_CONSTRAINT, owner=OWNER_CONSTRAINT,
            reference=constraint.constraint_id, text=constraint.text,
            attributes=attributes,
            links=(Link(LINK_RECORD, constraint.record_id),)))
    return _section_for(SECTION_CONSTRAINTS, items)


def _stage15_cluster(composition, prototype_needs, names):
    """Parts, components and interactions from the EXISTING composite reader.
    That reader validates every collection against the composition of the same
    snapshot and refuses whole; the three sections inherit that boundary."""
    if composition is UNREADABLE or not isinstance(composition, dict):
        return (_unavailable_section(SECTION_PARTS),
                _unavailable_section(SECTION_COMPONENTS),
                _unavailable_section(SECTION_INTERACTIONS))
    try:
        subsystems = tuple(composition.get("subsystems") or ())
        focus = composition.get("focus")
        interfaces = tuple(composition.get("interfaces") or ())
        preparations = tuple(composition.get("preparations") or ())
        dependencies = tuple(composition.get("dependencies") or ())
        components = tuple(composition.get("components") or ())
        participations = tuple(composition.get("participations") or ())
        for sub in subsystems:
            names.append((sub.subsystem_id, sub.display_name))
        for component in components:
            names.append((component.component_id, component.display_name))
        parts = _parts(subsystems, focus)
        comps = _components(components, prototype_needs)
        interactions = _interactions(interfaces, preparations, dependencies,
                                     participations, components)
    except Exception:
        del names[:]
        return (_unavailable_section(SECTION_PARTS),
                _unavailable_section(SECTION_COMPONENTS),
                _unavailable_section(SECTION_INTERACTIONS))
    return (parts, comps, interactions)


def _parts(subsystems, focus):
    items = []
    for sub in subsystems:
        attributes = _own(sub, "function_text", "domain", "provenance",
                          "validation_state")
        attributes += (("initial_analysis_focus", bool(focus) and sub.domain == focus),)
        items.append(Item(
            content_kind=KIND_PART, owner=OWNER_PART, reference=sub.subsystem_id,
            text=sub.display_name, attributes=attributes))
    return _section_for(SECTION_PARTS, items)


def _components(components, prototype_needs):
    needs_unreadable = prototype_needs is UNREADABLE or not isinstance(prototype_needs, dict)
    items = []
    for component in components:
        attributes = _own(component, "function_text", "provenance", "validation_state")
        if not needs_unreadable:
            need = prototype_needs.get(component.component_id)
            if isinstance(need, str) and need:
                attributes += (("prototype_need", need),)
        items.append(Item(
            content_kind=KIND_COMPONENT, owner=OWNER_COMPONENT,
            reference=component.component_id, text=component.display_name,
            attributes=attributes,
            links=tuple(Link(LINK_PART, ref) for ref in component.subsystem_ids)))
    unavailable_inputs = ("prototype_needs",) if (needs_unreadable and items) else ()
    return _section_for(SECTION_COMPONENTS, items, (), unavailable_inputs)


def _interactions(interfaces, preparations, dependencies, participations, components):
    participants = _composition.current_interface_participants(participations, components)
    items = []
    for interface in interfaces:
        preparation = _composition.preparation_for(preparations, interface.interface_id)
        attributes = _own(interface, "provenance", "validation_state")
        attributes += (("preparation_presence",
                        _composition.preparation_presence(preparation)),)
        links = [Link(LINK_PART, interface.subsystem_a_id),
                 Link(LINK_PART, interface.subsystem_b_id)]
        dependency = _composition.dependency_for(dependencies, interface.interface_id)
        if dependency is not None:
            attributes += (("dependency_kind", dependency.kind),)
            if dependency.dependent_subsystem_id:
                links.append(Link(LINK_DEPENDENT_PART, dependency.dependent_subsystem_id))
            if dependency.depends_on_subsystem_id:
                links.append(Link(LINK_DEPENDS_ON_PART, dependency.depends_on_subsystem_id))
        for component_id in participants.get(interface.interface_id, ()):
            links.append(Link(LINK_COMPONENT, component_id))
        items.append(Item(
            content_kind=KIND_INTERACTION, owner=OWNER_INTERACTION,
            reference=interface.interface_id, text=interface.description,
            attributes=attributes, links=tuple(links)))
    return _section_for(SECTION_INTERACTIONS, items)


def _unresolved_work(state, records, derived_available):
    """The progression-derived unresolved truth, each item from its own owner.
    A requirement row is a distinct derived object (its own identity) and links
    to its canonical anchor; the anchored record itself is not repeated here."""
    if not derived_available:
        return _unavailable_section(SECTION_UNRESOLVED_WORK)
    try:
        items = []
        for gap in getattr(state, "gaps", None) or ():
            if getattr(gap, "status", None) not in (_ledger.OPEN, _ledger.PARTIAL):
                continue
            items.append(Item(
                content_kind=KIND_GAP, owner=OWNER_GAP, reference=gap.gap_type,
                text=None, attributes=_own(gap, "status", "iterations_open")))
        for gap_type, question_id, required_input, _policy in _routing.outstanding_needs(state):
            items.append(Item(
                content_kind=KIND_ROUTED_NEED, owner=OWNER_ROUTED_NEED,
                reference="%s:%s" % (gap_type, question_id), text=None,
                attributes=(("gap_type", gap_type), ("question_id", question_id),
                            ("required_input", required_input)),
                links=(Link(LINK_GAP, gap_type), Link(LINK_QUESTION, question_id))))
        for lo, hi in _ledger.active_declared_contradiction_pairs(records):
            items.append(Item(
                content_kind=KIND_DECLARED_CONTRADICTION, owner=OWNER_CONTRADICTION,
                reference="%s|%s" % (lo, hi), text=None,
                links=(Link(LINK_RECORD, lo), Link(LINK_RECORD, hi))))
        for req in derive_requirement_landscape(state).requirements:
            anchor = req.primary_anchor
            items.append(Item(
                content_kind=KIND_REQUIREMENT, owner=OWNER_REQUIREMENT,
                reference=req.requirement_id, text=req.statement,
                attributes=_own(req, "source_status", "criticality",
                                "criticality_authority"),
                links=(Link(LINK_REQUIREMENT_ANCHOR,
                            "%s:%s" % (anchor.anchor_kind, anchor.anchor_reference)),)))
        step = derive_next_development_step(state)
        if step is not None:
            # The step is a distinct derived object; its reference is the
            # owner's own (issue_type, reference_id) pair, so no two items of
            # the picture share one reference string.
            items.append(Item(
                content_kind=KIND_NEXT_DEVELOPMENT_STEP, owner=OWNER_NEXT_STEP,
                reference="%s:%s" % (step.issue_type, step.reference_id),
                text=step.title,
                attributes=_own(step, "issue_type", "reference_id")))
    except Exception:
        return _unavailable_section(SECTION_UNRESOLVED_WORK)
    return _section_for(SECTION_UNRESOLVED_WORK, items)


def _engineering_continuations(view):
    """The Step-6 actions exactly as the existing handoff view produced them:
    an existing page that its own owner's gate already permits. A continuation
    is attributed to the role it was offered for (the owner's own placement);
    it is not a statement that the capability fulfils the functional need."""
    resolved = _handoff_roles(view)
    if resolved is None:
        return _unavailable_section(SECTION_ENGINEERING_CONTINUATIONS)
    roles, _abstained, _idea_available = resolved
    items = []
    for role in roles:
        for capability in role.get("capabilities") or ():
            action = capability.get("action")
            if not action:
                continue
            items.append(Item(
                content_kind=KIND_ENGINEERING_CONTINUATION, owner=OWNER_CONTINUATION,
                reference="%s:%s" % (role.get("role"), capability.get("ref")),
                text=None,
                attributes=(("role", role.get("role")),
                            ("ref", capability.get("ref")),
                            ("state", capability.get("state")),
                            ("action", action))))
    return _section_for(SECTION_ENGINEERING_CONTINUATIONS, items)
