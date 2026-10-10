"""Stage 18 / CAP-01 — the bounded CAP-01 presentation-profile resolver.

Gate: the Owner-authorized bounded Stage-18 / CAP-01 guidance increments — the
first (checklist, PR #678) and the second (research-direction addendum) — recorded
in ACTIVE_INCREMENT_CONTRACT.md.

Purpose
  The ONE place that answers "does an AUTHORIZED CAP-01 guidance profile exist
  for this canonical domain, and which copy keys does it render?". It owns
  capability AVAILABILITY and profile STRUCTURE. It owns no text: every string
  stays in ``web/ui_text.py``, and this module only names the stable keys that
  catalogue resolves. Availability is not translation, which is why the two do
  not share a module.

Input contract
  * ``profile_for_domain(domain_id)`` / ``profile_copy(domain_id)`` — ``domain_id``
    is a TRUSTED, server-resolved canonical domain identifier (``state.domain`` /
    ``state.domain_signal`` / a package ``capability_id`` derived from them),
    never request, query, form or free-text input.
  * ``profiles_for_package(package)`` — an already-assembled deliverable package.
    It is read, never mutated, and nothing is derived that the assembler did not
    already decide.

Output contract
  Copy KEYS only, never resolved text, so the caller renders through the existing
  ``ui_text.text`` / ``t()`` / ``ui_lang`` seam and exactly ONE language can reach
  a reader. Every function is pure and never raises, so it is safe on any
  template path.

Boundaries
  * Presentation only. It activates no domain, classifies no text, infers no
    concept-class membership, changes no deterministic evaluation, and owns no
    evidence, risk, assumption, contradiction, readiness or gap truth.
  * DOMAIN ACTIVATION IS NOT CAP-01 PROFILE AVAILABILITY. A domain can be fully
    activated and still have no CAP-01 profile — ``mechanical`` is exactly that
    case today. "No profile" means ONLY *no domain-specific CAP-01 guidance
    profile is authorized yet*. It NEVER means unsupported, invalid,
    not-activated, failed or incomplete, and nothing here may drive an
    unsupported-domain message.
  * CAP-01 is a GUIDANCE owner, not a technical-production owner. It absorbs no
    responsibility from CAP-04, CAP-06, CAP-07, CAP-08, CAP-09, CAP-10, CAP-11,
    CAP-12, CAP-13, CAP-14, THERM-01, WS-PFV-001 or the shared Technical
    Realization layer (roadmap §8C, invariants A–C and I).
  * Both bounded increments are presentation-only and class-general. They are
    early increments, not CAP-01's ceiling, and not its permanent architecture
    (invariants D and H).
  * No plugin framework, no generic capability registry, no unused future row.
"""
from web import ui_text

# The domain -> AUTHORIZED CAP-01 guidance-profile table: the ONLY place a CAP-01
# domain literal lives. The deterministic core (progression_loop / idea_state /
# domain_rules / domain_activation / semantic_registry / requirement_landscape /
# validation_plan) carries no CAP-01 vocabulary and needs NO change to gain a
# future profile — a separately-authorized profile is ONE row here plus its own
# ``UI_<profile id>_*`` copy keys in the catalogue. There is deliberately no
# permanent ``if electronics / elif mechanical`` chain anywhere.
CAP01_PROFILE_BY_DOMAIN = {
    "electronics_electrical": "CAP01_ELECTRONICS_INTERFACE_V1",
}

# The copy parts every CAP-01 profile supplies, mapped to the view key the caller
# reads. Item keys are discovered by the ``_ITEM_<n>`` convention instead of being
# listed, so a future profile picks its own item count with no code change here.
_COPY_PARTS = {
    "title_key":    "TITLE",
    "intro_key":    "INTRO",
    "boundary_key": "BOUNDARY",
    "limit_key":    "LIMIT",
    "evidence_key": "EVIDENCE",
}

# An OPTIONAL research-direction group a profile may carry: a heading, an intro
# and its own ``RESEARCH_ITEM_<n>`` lines, discovered by the same convention as the
# checklist items. It is optional so a future profile is never forced to ship one,
# and all-or-nothing so it can never render as half a group; its absence leaves the
# rest of the profile exactly as it was.
_RESEARCH_PARTS = {
    "title_key": "RESEARCH_TITLE",
    "intro_key": "RESEARCH_INTRO",
}

# Where the canonical, already-assembled domain rows live. Read as a COLLECTION,
# deliberately: today the assembler emits exactly one capability, but that is a
# CURRENT RUNTIME LIMITATION, not the CAP-01 domain model (invariant F). Reading
# ``[0]`` would harden today's shape into the architecture and force a rewrite
# the day a package legitimately carries more than one canonical domain.
_SECTION = "section_3_assessment_overview"
_ROWS = "capabilities_assessed"


def profile_for_domain(domain_id):
    """The AUTHORIZED CAP-01 guidance-profile id for a trusted canonical domain
    id, or ``None`` when no CAP-01 profile is authorized for it.

    Pure and data-driven: it reads the table above and nothing else. ``None``
    means "no CAP-01 profile authorized yet", never "unsupported domain"."""
    if isinstance(domain_id, str):
        return CAP01_PROFILE_BY_DOMAIN.get(domain_id.strip())
    return None


def profile_copy(domain_id):
    """The CAP-01 copy KEYS to render for a trusted canonical domain id, or
    ``None`` when no authorized profile exists for it (or its copy is incomplete).

    Returns a fresh dict of catalogue keys — ``profile_id``, the five part keys,
    an ordered ``item_keys`` tuple and ``research`` (the optional research-direction
    group, or ``None``). Never text. An incomplete profile fails closed rather than
    rendering half a block, and ``None`` is a silent no-render, not an
    unsupported-domain signal."""
    profile_id = profile_for_domain(domain_id)
    if profile_id is None:
        return None
    prefix = "UI_" + profile_id + "_"
    view = {name: prefix + part for name, part in _COPY_PARTS.items()}
    if not all(ui_text.has_string(key) for key in view.values()):
        return None
    item_keys = _numbered(prefix + "ITEM_")
    if not item_keys:
        return None
    view["profile_id"] = profile_id
    view["item_keys"] = item_keys
    view["research"] = _research(prefix)
    return view


def _numbered(stem):
    """The consecutive ``<stem>1``, ``<stem>2``, ... keys the catalogue carries."""
    keys = []
    while ui_text.has_string(stem + "%d" % (len(keys) + 1)):
        keys.append(stem + "%d" % (len(keys) + 1))
    return tuple(keys)


def _research(prefix):
    """The profile's research-direction group as catalogue keys, or ``None``.

    All-or-nothing: a heading, an intro and at least one line, or nothing at all.
    Where to look and which generic terms to search for are navigation aids only;
    this retrieves nothing, creates no evidence and claims nothing about the
    reader's project."""
    group = {name: prefix + part for name, part in _RESEARCH_PARTS.items()}
    if not all(ui_text.has_string(key) for key in group.values()):
        return None
    group["item_keys"] = _numbered(prefix + "RESEARCH_ITEM_")
    return group if group["item_keys"] else None


def _rows(package):
    """The canonical capability rows of an assembled package, as a tuple.

    Defensive by design: a package shape this does not recognise yields no rows
    and therefore no CAP-01 block, which is the safe outcome on a template path."""
    try:
        rows = package[_SECTION][_ROWS]
    except (TypeError, KeyError, IndexError):
        return ()
    if not isinstance(rows, (list, tuple)):
        return ()
    return tuple(row for row in rows if isinstance(row, dict))


def profiles_for_package(package):
    """Zero or more authorized CAP-01 presentation profiles for an assembled
    package, in source order, deduplicated by profile.

    Three separate facts decide, all of them already canonical in the package and
    none of them derived here: the capability row's trusted ``capability_id``,
    whether an AUTHORIZED CAP-01 profile exists for it, and whether that row
    still reports at least one unresolved/open gap. A row failing any of the
    three contributes nothing, and a package whose domains have no authorized
    profile yields an empty tuple — which renders nothing and says nothing about
    those domains' support.

    Consuming the rows as a COLLECTION is the forward-compatible part. It is not
    a claim that the runtime supports multiple domains today: it does not, the
    assembler emits one row, and nothing here creates multi-domain truth,
    infers subsystem membership or activates anything. It only means that the day
    a package legitimately carries more than one canonical domain, this resolver
    extends rather than needing replacement."""
    seen, profiles = set(), []
    for row in _rows(package):
        if not row.get("gaps_open"):
            continue
        view = profile_copy(row.get("capability_id"))
        if view is None or view["profile_id"] in seen:
            continue
        seen.add(view["profile_id"])
        profiles.append(view)
    return tuple(profiles)


# ---------------------------------------------------------------------------
# MECHANICAL CAP-01 — OPEN-GAP TECHNICAL CONTEXT (Owner-authorized bounded slice)
#
# A SECOND, gap-scoped presentation shape beside the domain-level checklist
# profile above. It answers ONE question: "for this trusted canonical domain,
# which CURRENT (OPEN / PARTIAL) canonical gaps have an authorized explanatory
# context, and which copy keys does each render?". The copy explains, at concept
# level, what the exact gap concerns within the governed Mechanical package
# (``domains/mechanical/domain.json``: gap_type_mappings, rule_nuances,
# capability_declaration, coverage_declaration) and what InventorAI does NOT
# conclude from it. It is explanatory context only — no question, action,
# responsibility, required input, closure rule or next action: Path-N stays the
# only served-question owner and CAP-04 the only action owner.
#
# Binding is by EXACT canonical identity and EXACT canonical lifecycle state:
# the gap's ``gap_type`` constant and ``status`` constant as carried on the
# already-loaded ``IdeaState``. Never by display label, translated label,
# question text, rendered title, keyword, fuzzy match or list position. The
# publicized ``gaps_detail[].gap_type`` of the assembled package is presentation
# wording ("Physical Feasibility") and is deliberately NOT read here.
#
# The existing Electronics profile path above is untouched: a domain with no row
# in this table contributes nothing, and "nothing" means only that no gap-scoped
# CAP-01 context is authorized for it.
# ---------------------------------------------------------------------------

# Trusted canonical domain id -> (context group id, canonical gap ids in the
# deterministic SOURCE order the governed package declares them). ONE row per
# authorized domain; ONE context per supported canonical gap; nothing else.
# The ``electronics_electrical`` row began (Electrical / Electronics Technical
# Deepening Slice 1) with PHYSICAL_FEASIBILITY only; the Stage-18 closure adds
# MECHANISM_COMPLETENESS and BOUNDARY_AMBIGUITY, so both active domains now carry
# all three governed technical gaps, each grounded only in its own governed
# package (``domains/<pack>/domain.json``). It stays separate from, and changes
# nothing in, the domain-level CAP01_ELECTRONICS_INTERFACE_V1 checklist /
# research profile above.
CAP01_GAP_CONTEXT_BY_DOMAIN = {
    "mechanical": (
        "CAP01_MECHANICAL_GAP_CONTEXT_V1",
        ("MECHANISM_COMPLETENESS", "PHYSICAL_FEASIBILITY", "BOUNDARY_AMBIGUITY"),
    ),
    "electronics_electrical": (
        "CAP01_ELECTRONICS_GAP_CONTEXT_V1",
        ("MECHANISM_COMPLETENESS", "PHYSICAL_FEASIBILITY", "BOUNDARY_AMBIGUITY"),
    ),
}

# The ONLY lifecycle states that make a gap CURRENT for this context. CLOSED,
# ACCEPTED_RISK, an unknown state or an absent gap render nothing.
_CURRENT_GAP_STATES = frozenset({"OPEN", "PARTIAL"})

# Group-level copy parts (one heading + one intro for the whole block).
_GAP_GROUP_PARTS = {
    "title_key": "TITLE",
    "intro_key": "INTRO",
}

# Per-gap copy parts: the gap heading, what the gap CONCERNS at concept level,
# and what InventorAI does NOT conclude from it.
_GAP_CONTEXT_PARTS = {
    "title_key":   "TITLE",
    "meaning_key": "MEANING",
    "limit_key":   "LIMIT",
}

# MECHANICAL TECHNICAL DEEPENING SLICE 1 — FORCE, MOMENT & PRESSURE FUNDAMENTALS.
# An OPTIONAL reference-fundamentals sub-view attached to ONE already-resolved
# gap context. (trusted canonical domain id, EXACT canonical gap id) -> (the
# governed pack's reference_fundamentals group id, its claim ids in the pack's
# source order). The gap context's own binding (exact gap id + exact OPEN /
# PARTIAL lifecycle state, decided in ``gap_contexts_for_gaps``) is the ONLY
# authority for whether anything renders; this table adds no second binding,
# reads no inventor text, no classification / substance signal and no package
# wording, and selects no relationship for a project — the SAME bounded
# reference set is shown whenever the exact authorized condition exists. The
# technical claim / source / limitation truth lives in
# ``domains/mechanical/domain.json`` (reference_fundamentals) and
# ``domains/domain_provenance.json``; the copy lives in ``web/ui_text.py``; this
# table owns availability and structure only. No calculation, no formula
# selection, no generic knowledge or calculation registry.
# ELECTRICAL / ELECTRONICS TECHNICAL DEEPENING SLICE 1 — BASIC ELECTRICAL REFERENCE
# FUNDAMENTALS adds ONE row on the same seam: the exact Electronics
# PHYSICAL_FEASIBILITY context carries three bounded reference claims (Ohm's-law
# reference, basic power reference, SI unit discipline) declared in
# ``domains/electronics_electrical/domain.json`` (basic_electrical_reference_v1)
# with provenance electronics_electrical:PR004–PR007. Same rules: no second
# binding, no inventor text, no signals, no calculation, no formula selection.
CAP01_GAP_FUNDAMENTALS = {
    ("mechanical", "PHYSICAL_FEASIBILITY"): (
        "force_moment_pressure_v1",
        ("torque_moment_perpendicular", "ideal_static_moment_balance",
         "pressure_force_area_uniform", "si_quantity_unit_discipline"),
    ),
    ("electronics_electrical", "PHYSICAL_FEASIBILITY"): (
        "basic_electrical_reference_v1",
        ("ohms_law_reference", "electrical_power_vi_reference",
         "si_electrical_unit_discipline"),
    ),
}

# ELECTRICAL-ENERGY-TIME-REFERENCE-01 — the ONE further bounded group a context
# may carry AFTER its group above, in this fixed order: (trusted canonical domain
# id, EXACT canonical gap id) -> ordered ((group id, claim ids in the pack's
# source order, the group's own copy-key namespace under the context prefix),).
# The group above keeps its own binding, copy namespace ("FUNDAMENTALS_") and
# content; together they form the fixed ordered collection ``fundamentals_groups``
# of ``gap_context_copy``. Same rules: the context's own binding (exact gap id +
# exact OPEN / PARTIAL state) is the only authority; no inventor text, signal,
# alias or keyword, no runtime discovery, no pack-driven formula selection, no
# user-controlled group selection and no calculation. The claim / source /
# limitation truth lives in ``domains/electronics_electrical/domain.json``
# (electrical_energy_time_reference_v1) with provenance
# electronics_electrical:PR008–PR011.
# 28-T1-SENSING-VALUE-THRESHOLD-01 adds ONE row on the same seam: the exact
# Electronics MECHANISM_COMPLETENESS context (which has no group of its own above)
# carries ONE prose-only conceptual group, sensing_value_threshold_reference_v1
# (``domains/electronics_electrical/domain.json``; provenance
# electronics_electrical:PR012–PR013) — reporting a sensed quantity's value
# versus indicating whether it is above a threshold. Same rules as above.
CAP01_GAP_FUNDAMENTALS_EXTENSIONS = {
    ("electronics_electrical", "PHYSICAL_FEASIBILITY"): (
        ("electrical_energy_time_reference_v1",
         ("constant_power_energy_reference", "energy_time_unit_discipline"),
         "ENERGY_TIME_FUNDAMENTALS_"),
    ),
    ("electronics_electrical", "MECHANISM_COMPLETENESS"): (
        ("sensing_value_threshold_reference_v1",
         ("sensed_value_versus_threshold_indication",),
         "SENSING_FUNDAMENTALS_"),
    ),
}

# Group-level parts of the fundamentals sub-view, then the four parts every item
# carries. ``EQUATION`` is deliberately its own part so the template can isolate
# the language-neutral relationship / unit symbols in a left-to-right span.
_FUNDAMENTALS_PARTS = {
    "title_key":    "TITLE",
    "intro_key":    "INTRO",
    "source_key":   "SOURCE",
    "boundary_key": "BOUNDARY",
}
_FUNDAMENTALS_ITEM_PARTS = {
    "title_key":    "TITLE",
    "lead_key":     "LEAD",
    "equation_key": "EQUATION",
    "note_key":     "NOTE",
}

# The ONLY groups whose items carry no relationship / equation: a conceptual
# explanation, never a placeholder equation. Named by exact group id; every
# other group keeps requiring all four parts above and still fails closed when
# any of them is missing. A prose-only item carries a title and ONE text part,
# both required (all-or-nothing on the group, exactly as above).
_FUNDAMENTALS_PROSE_ONLY_GROUPS = frozenset({"sensing_value_threshold_reference_v1"})
_FUNDAMENTALS_PROSE_ITEM_PARTS = {
    "title_key": "TITLE",
    "text_key":  "TEXT",
}


# STAGE 18 — GAP-SCOPED TECHNICAL NEXT-STEP GUIDANCE — CLOSURE. An OPTIONAL
# next-steps sub-view attached to ONE already-resolved gap context: the
# information still missing (a bounded summary of the gap's OWN canonical
# questions), what to look into (bounded topics plus generic search terms),
# what could be measured, checked or documented (class-level categories only)
# and the specialist boundary (an explicit abstention). Same rules as the
# fundamentals sub-view above: the gap context's own binding (trusted domain id
# + exact canonical gap id + exact OPEN / PARTIAL state) is the ONLY authority
# for whether anything renders; this table adds no second binding, reads no
# inventor text, answer, keyword, label, classification signal or list
# position, and selects nothing for a project. No value, range, threshold,
# formula selection, calculation, test protocol, pass / fail criterion,
# material / thickness / specification / safety statement, named standard,
# laboratory, vendor or specialist category exists here or in its copy.
#
# Each row: (trusted canonical domain id, EXACT canonical gap id) ->
# (next-steps group id, source anchors). The anchors are traceability only —
# never rendered and never used to choose anything — and every one names
# EXISTING governed truth that the tests resolve:
#   ("question", <question id>)   a governed question of that exact gap in the
#                                 pack's gap_type_mappings (the missing-
#                                 information owner stays Path-N);
#   ("rule", <rule id>)           a governed rule_nuances entry of the pack;
#   ("coverage", <path>)          "<declaration>.<field>.<index>" of the pack's
#                                 capability / coverage declaration (the last
#                                 segment is the list position);
#   ("fundamental", <claim id>)   a reference_fundamentals claim whose
#                                 applicable_gap_type is that exact gap;
#   ("routing", <policy ref>)     the committed Path-N RoutingPolicy of a
#                                 question of that exact gap (fact only; no
#                                 routing is read, written or changed here).
CAP01_GAP_NEXT_STEPS = {
    ("mechanical", "MECHANISM_COMPLETENESS"): ("CAP01_MECHANICAL_NEXT_STEPS_V1", (
        ("question", "mechanical:MECHANISM_COMPLETENESS:Q1"),
        ("question", "mechanical:MECHANISM_COMPLETENESS:Q2"),
        ("question", "mechanical:MECHANISM_COMPLETENESS:Q3"),
        ("question", "mechanical:MECHANISM_COMPLETENESS:Q4"),
        ("rule", "mechanical:RN001"),
        ("coverage", "coverage_declaration.covered_areas.0"),
    )),
    ("mechanical", "PHYSICAL_FEASIBILITY"): ("CAP01_MECHANICAL_NEXT_STEPS_V1", (
        ("question", "mechanical:PHYSICAL_FEASIBILITY:Q1"),
        ("question", "mechanical:PHYSICAL_FEASIBILITY:Q2"),
        ("rule", "mechanical:RN002"),
        ("coverage", "coverage_declaration.covered_areas.1"),
        ("coverage", "capability_declaration.known_unknowns.1"),
        ("fundamental", "torque_moment_perpendicular"),
        ("fundamental", "ideal_static_moment_balance"),
        ("fundamental", "pressure_force_area_uniform"),
        ("fundamental", "si_quantity_unit_discipline"),
        ("routing", "mechanical-path-n-routing-v1:PHYSICAL_FEASIBILITY:Q2"),
    )),
    ("mechanical", "BOUNDARY_AMBIGUITY"): ("CAP01_MECHANICAL_NEXT_STEPS_V1", (
        ("question", "mechanical:BOUNDARY_AMBIGUITY:Q1"),
        ("question", "mechanical:BOUNDARY_AMBIGUITY:Q2"),
        ("question", "mechanical:BOUNDARY_AMBIGUITY:Q3"),
        ("question", "mechanical:BOUNDARY_AMBIGUITY:Q4"),
        ("rule", "mechanical:RN003"),
        ("coverage", "coverage_declaration.covered_areas.2"),
    )),
    ("electronics_electrical", "MECHANISM_COMPLETENESS"): ("CAP01_ELECTRONICS_NEXT_STEPS_V1", (
        ("question", "electronics_electrical:MECHANISM_COMPLETENESS:Q1"),
        ("question", "electronics_electrical:MECHANISM_COMPLETENESS:Q2"),
        ("question", "electronics_electrical:MECHANISM_COMPLETENESS:Q3"),
        ("question", "electronics_electrical:MECHANISM_COMPLETENESS:Q4"),
        ("rule", "electronics_electrical:RN001"),
        ("rule", "electronics_electrical:RN003"),
        ("coverage", "coverage_declaration.covered_areas.0"),
        ("coverage", "coverage_declaration.covered_areas.2"),
    )),
    ("electronics_electrical", "PHYSICAL_FEASIBILITY"): ("CAP01_ELECTRONICS_NEXT_STEPS_V1", (
        ("question", "electronics_electrical:PHYSICAL_FEASIBILITY:Q1"),
        ("question", "electronics_electrical:PHYSICAL_FEASIBILITY:Q2"),
        ("question", "electronics_electrical:PHYSICAL_FEASIBILITY:Q3"),
        ("rule", "electronics_electrical:RN002"),
        ("coverage", "coverage_declaration.covered_areas.1"),
        ("fundamental", "ohms_law_reference"),
        ("fundamental", "electrical_power_vi_reference"),
        ("fundamental", "si_electrical_unit_discipline"),
    )),
    ("electronics_electrical", "BOUNDARY_AMBIGUITY"): ("CAP01_ELECTRONICS_NEXT_STEPS_V1", (
        ("question", "electronics_electrical:BOUNDARY_AMBIGUITY:Q1"),
        ("question", "electronics_electrical:BOUNDARY_AMBIGUITY:Q2"),
        ("question", "electronics_electrical:BOUNDARY_AMBIGUITY:Q3"),
    )),
}

# The shared, domain-neutral sub-view labels (one set for every row), then the
# per-gap parts: one MISSING summary, numbered TOPIC / SEARCH / MEASURE lines
# (discovered by the ``_<n>`` convention) and one SPECIALIST boundary line.
_NEXT_STEPS_LABEL_PREFIX = "UI_CAP01_NEXT_STEPS_V1_"
_NEXT_STEPS_LABEL_PARTS = {
    "title_key":            "TITLE",
    "missing_label_key":    "MISSING_LABEL",
    "look_label_key":       "LOOK_LABEL",
    "search_label_key":     "SEARCH_LABEL",
    "measure_label_key":    "MEASURE_LABEL",
    "specialist_label_key": "SPECIALIST_LABEL",
    "boundary_key":         "BOUNDARY",
}
_NEXT_STEPS_PARTS = {
    "missing_key":    "MISSING",
    "specialist_key": "SPECIALIST",
}
_NEXT_STEPS_LISTS = {
    "topic_keys":   "TOPIC_",
    "search_keys":  "SEARCH_",
    "measure_keys": "MEASURE_",
}


def _gap_identity(gap):
    """``(gap_type, status)`` of one canonical gap record, or ``None``.

    Accepts the ``IdeaState.gaps`` record shape (``.gap_type`` / ``.status``
    attributes) or an explicit ``(gap_type, status)`` pair. Both values must be
    strings and are compared EXACTLY — no normalisation, no stripping, no case
    folding — so a display label, a translated label or a near string can never
    satisfy the binding."""
    if isinstance(gap, (tuple, list)) and len(gap) == 2:
        gap_type, status = gap
    else:
        gap_type = getattr(gap, "gap_type", None)
        status = getattr(gap, "status", None)
    if isinstance(gap_type, str) and isinstance(status, str):
        return gap_type, status
    return None


def _current_gap_states(gaps):
    """Canonical gap id -> its EXACT lifecycle state, first record per id.

    Mirrors the canonical ``IdeaState.get_gap`` accessor (first match wins), so
    a duplicated record never yields a second context and never changes the
    state the canonical accessor would report."""
    states = {}
    try:
        records = tuple(gaps)
    except TypeError:
        return states
    for gap in records:
        identity = _gap_identity(gap)
        if identity is None:
            continue
        gap_type, status = identity
        if gap_type not in states:
            states[gap_type] = status
    return states


def gap_context_copy(domain_id, gap_type):
    """The CAP-01 gap-context copy KEYS for one trusted canonical domain id and
    one EXACT canonical gap id, or ``None`` when no context is authorized for
    that pair (or its copy is incomplete).

    Pure and data-driven. The result carries ``group_id``, ``gap_type`` (the
    canonical id, for traceability attributes only — never as visible text) and
    the three part keys. Never text. Availability is not lifecycle: this does
    not know whether the gap is current; ``gap_contexts_for_gaps`` decides that."""
    if not isinstance(domain_id, str) or not isinstance(gap_type, str):
        return None
    row = CAP01_GAP_CONTEXT_BY_DOMAIN.get(domain_id.strip())
    if row is None:
        return None
    group_id, gap_ids = row
    if gap_type not in gap_ids:
        return None
    prefix = "UI_" + group_id + "_" + gap_type + "_"
    view = {name: prefix + part for name, part in _GAP_CONTEXT_PARTS.items()}
    if not all(ui_text.has_string(key) for key in view.values()):
        return None
    view["group_id"] = group_id
    view["gap_type"] = gap_type
    view["fundamentals"] = _fundamentals(domain_id.strip(), gap_type, prefix)
    view["fundamentals_groups"] = _fundamentals_groups(
        domain_id.strip(), gap_type, prefix, view["fundamentals"])
    view["next_steps"] = _next_steps(domain_id.strip(), gap_type)
    return view


def _fundamentals(domain_id, gap_type, prefix):
    """The OPTIONAL reference-fundamentals sub-view of one gap context, as copy
    KEYS plus the pack's group / claim identifiers, or ``None``.

    All-or-nothing: the group parts and every item's four parts must exist in
    the catalogue, or nothing renders — a half set of relationships would be a
    different (and untruthful) statement. ``None`` here never removes the gap
    context itself; the context's title / meaning / limit render unchanged."""
    row = CAP01_GAP_FUNDAMENTALS.get((domain_id, gap_type))
    if row is None:
        return None
    group_id, claim_ids = row
    return _fundamentals_group(group_id, claim_ids, prefix + "FUNDAMENTALS_")


def _fundamentals_groups(domain_id, gap_type, prefix, first):
    """The fixed ORDERED collection of reference-fundamentals groups of one gap
    context: the context's own group (``first``, from ``_fundamentals``) and then
    each ``CAP01_GAP_FUNDAMENTALS_EXTENSIONS`` group in its fixed order. Each
    group is all-or-nothing on its OWN copy: an incomplete group is left out
    whole and never removes the other group or the gap context. Empty tuple when
    no group is available."""
    groups = [first] if first is not None else []
    for group_id, claim_ids, namespace in CAP01_GAP_FUNDAMENTALS_EXTENSIONS.get(
            (domain_id, gap_type), ()):
        group = _fundamentals_group(group_id, claim_ids, prefix + namespace)
        if group is not None:
            groups.append(group)
    return tuple(groups)


def _fundamentals_group(group_id, claim_ids, stem):
    """ONE reference-fundamentals group as copy KEYS under ``stem`` plus its
    group / claim identifiers, or ``None`` when any of its copy is missing."""
    view = {name: stem + part for name, part in _FUNDAMENTALS_PARTS.items()}
    if not all(ui_text.has_string(key) for key in view.values()):
        return None
    prose_only = group_id in _FUNDAMENTALS_PROSE_ONLY_GROUPS
    item_parts = _FUNDAMENTALS_PROSE_ITEM_PARTS if prose_only else _FUNDAMENTALS_ITEM_PARTS
    claims = []
    for number, claim_id in enumerate(claim_ids, 1):
        item = {name: stem + "ITEM_%d_" % number + part
                for name, part in item_parts.items()}
        if not all(ui_text.has_string(key) for key in item.values()):
            return None
        item["claim_id"] = claim_id
        claims.append(item)
    if not claims:
        return None
    view["group_id"] = group_id
    view["prose_only"] = prose_only
    # Named ``claims`` (never ``items``): a template attribute lookup on a dict
    # would otherwise resolve to the dict method and iterate nothing.
    view["claims"] = tuple(claims)
    return view


def _next_steps(domain_id, gap_type):
    """The OPTIONAL technical next-steps sub-view of one gap context, as copy
    KEYS plus its group id and source anchors, or ``None``.

    All-or-nothing: every shared label, the gap's MISSING and SPECIALIST lines
    and at least one TOPIC, SEARCH and MEASURE line must exist in the catalogue,
    or nothing renders — half a set of next steps would be a different (and
    untruthful) statement. ``None`` never removes the gap context itself."""
    row = CAP01_GAP_NEXT_STEPS.get((domain_id, gap_type))
    if row is None:
        return None
    group_id, anchors = row
    view = {name: _NEXT_STEPS_LABEL_PREFIX + part
            for name, part in _NEXT_STEPS_LABEL_PARTS.items()}
    prefix = "UI_" + group_id + "_" + gap_type + "_"
    view.update({name: prefix + part for name, part in _NEXT_STEPS_PARTS.items()})
    if not all(ui_text.has_string(key) for key in view.values()):
        return None
    for name, stem in _NEXT_STEPS_LISTS.items():
        view[name] = _numbered(prefix + stem)
        if not view[name]:
            return None
    view["group_id"] = group_id
    view["anchors"] = anchors
    return view


def _gap_group_copy(group_id):
    """The group heading / intro copy KEYS for a context group, or ``None`` when
    the group copy is incomplete (fail closed: no half block)."""
    prefix = "UI_" + group_id + "_"
    view = {name: prefix + part for name, part in _GAP_GROUP_PARTS.items()}
    if not all(ui_text.has_string(key) for key in view.values()):
        return None
    view["group_id"] = group_id
    return view


def gap_contexts_for_gaps(domain_id, gaps):
    """The resolved gap-scoped CAP-01 view for ONE trusted canonical domain id
    and the canonical gap records of the already-loaded state, or ``None``.

    Exactly three facts decide each context and none is derived here: the
    trusted domain id has an authorized context row; the canonical gap id is
    one of that row's supported gaps; and the gap's EXACT canonical lifecycle
    state is OPEN or PARTIAL on the state. Contexts come back in the table's
    deterministic source order (never state order), at most once per canonical
    gap, each carrying its copy keys, its canonical ``gap_type`` and its exact
    ``gap_state``. A domain without a row, a domain with no current supported
    gap, or incomplete copy yields ``None`` — a silent no-render that says
    nothing about the domain's support. Never raises."""
    if not isinstance(domain_id, str):
        return None
    row = CAP01_GAP_CONTEXT_BY_DOMAIN.get(domain_id.strip())
    if row is None:
        return None
    group_id, gap_ids = row
    group = _gap_group_copy(group_id)
    if group is None:
        return None
    states = _current_gap_states(gaps)
    contexts = []
    for gap_type in gap_ids:
        state = states.get(gap_type)
        if state not in _CURRENT_GAP_STATES:
            continue
        view = gap_context_copy(domain_id, gap_type)
        if view is None:
            continue
        view["gap_state"] = state
        contexts.append(view)
    if not contexts:
        return None
    group["contexts"] = tuple(contexts)
    return group


def gap_contexts_for_package(package, gaps):
    """The gap-scoped CAP-01 view for an assembled package plus the canonical
    gap records of the state it was assembled from, or ``None``.

    The package supplies ONLY the trusted canonical domain context (the
    capability rows' ``capability_id``, read as a COLLECTION exactly like
    ``profiles_for_package``); the gap identities and lifecycle states come from
    the canonical ``gaps`` records, never from the package's publicized
    presentation wording. The first row whose domain has an authorized context
    and at least one current supported gap wins; today's single-domain runtime
    is a current limitation, not the model. Never raises."""
    for row in _rows(package):
        view = gap_contexts_for_gaps(row.get("capability_id"), gaps)
        if view is not None:
            return view
    return None
