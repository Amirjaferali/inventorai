"""
engine/disclosure_export.py

Stage 35 — Structured Invention Disclosure Export — first bounded slice: the ONE
owner of the disclosure projection (implementation contract
``docs/governance/STAGE35_DISCLOSURE_EXPORT_FIRST_SLICE_IMPLEMENTATION_CONTRACT.md``).

For ONE project owned by the requesting account it composes ONE deterministic
projection from ONE store-owned SQLite read snapshot. It composes references and
values that existing owners produce; it derives no engineering truth, infers,
summarizes and re-words nothing, renders no legal conclusion, patent claim,
assessment or HTML, persists nothing, writes no log line and makes no network,
provider or AI call. It holds only the export's own fixed text (the disclaimers,
the scope label, the problem-capture limitation) and the closed v1 token sets.

Two outcomes besides success, never mixed: ``ProjectAccessDenied`` (raised by the
unchanged authorization owner, a DENIAL) and ``DisclosureExportRefused`` (every
other failure, a REFUSAL: no file, no partial output). No first-slice source
failure is section-local, so no composition from the store produces
``UNAVAILABLE`` (§3.4).
"""
import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone

from engine.deliverable_assembler import assemble_deliverable, resolved_problem
from engine.experiment_result import execution_states
from engine.idea_state import (
    ANCESTRY_ASSUMPTION_ORIGIN, DECISION_ACTION_DISPOSITIONS, DISPOSITION_ANSWERED,
    DISPOSITION_CONTRADICTION_DECLARED, DISPOSITION_PROVISIONAL_ASSUMPTION,
    DISPOSITION_UNKNOWN, INTERACTION_DISPOSITIONS, OPEN, PARTIAL, PROVENANCE_VALUES,
    VALIDATION_STATUSES, active_declared_contradiction_pairs,
    classify_assumption_ancestry,
)
from engine.need_routing import REQUIRED_INPUT_SPECIALIST, active_routes
from engine.read_export_service import ProjectAccessDenied, get_authorized_project_read
from engine.requirement_landscape import derive_requirement_landscape
from engine.requirement_quantity import QUANTITY_KINDS, requirement_quantities_meta
from engine.session_reconstruction import (
    apply_planning_metadata, load_planning_metadata, reconstruct_readonly_state,
)
from engine.subsystem_model import DEPENDENCY_MUTUAL, DEPENDENCY_ONE_WAY

# --- versions and file names (§9.1) -------------------------------------------
DISCLOSURE_SCHEMA_VERSION = "inventorai-disclosure/1"
JSON_FORMAT_VERSION = "inventorai-disclosure-json/1"
HTML_FORMAT_VERSION = "inventorai-disclosure-html/1"
JSON_FILE_NAME = "inventorai-disclosure-export-v1.json"
HTML_FILE_NAME = "inventorai-disclosure-export-v1.html"

# --- the export's own fixed text (§10, §12.1, §12.2, §12.6) -------------------
DISCLAIMERS = (
    ("D01", "This document is not legal advice. InventorAI does not provide legal services.",
     "هذه الوثيقة ليست استشارة قانونية، ولا يقدّم InventorAI خدمات قانونية."),
    ("D02", "This document is not a patentability opinion. InventorAI has not assessed "
            "whether this invention is new, inventive or patentable.",
     "هذه الوثيقة ليست رأيًا بشأن قابلية الاختراع للحصول على براءة. لم يقيّم InventorAI "
     "ما إذا كان هذا الاختراع جديدًا أو ينطوي على خطوة ابتكارية أو قابلًا للحصول على براءة."),
    ("D03", "This document is not a prior-art search. InventorAI has not searched for or "
            "cleared prior art.",
     "هذه الوثيقة ليست بحثًا في التقنية السابقة (prior art). لم يبحث InventorAI عن "
     "التقنية السابقة ولم يؤكد خلوّ الطريق منها."),
    ("D04", "This document is not a freedom-to-operate opinion.",
     "هذه الوثيقة ليست رأيًا بشأن حرية الاستغلال (freedom to operate)."),
    ("D05", "This document is not a filing-ready patent application.",
     "هذه الوثيقة ليست طلب براءة اختراع جاهزًا للإيداع."),
    ("D06", "InventorAI has not drafted or generated any patent claim in this document. Any "
            "claim-like wording appears only inside text quoted from the inventor, "
            "reproduced as written and not assessed. Nothing in this document is a legally "
            "valid claim.",
     "لم يصِغ InventorAI أي مطالبة براءة (patent claim) في هذه الوثيقة ولم يولّدها. أي صياغة "
     "تشبه المطالبات لا ترد إلا داخل نص منقول عن المخترع، مُستنسَخ كما كُتب ودون تقييم. لا "
     "شيء في هذه الوثيقة مطالبة صالحة قانونيًا."),
    ("D07", "Evidence recorded here is not a validated conclusion. Items marked unvalidated "
            "have not been checked by InventorAI.",
     "الأدلة المسجّلة هنا ليست استنتاجًا متحقَّقًا منه. العناصر الموسومة بأنها غير متحقَّق "
     "منها لم يتحقق منها InventorAI."),
    ("D08", "This document does not establish a conception date, an invention date, "
            "priority, inventorship or ownership.",
     "لا تُثبت هذه الوثيقة تاريخ تصوّر الاختراع ولا تاريخ الاختراع ولا الأسبقية ولا صفة "
     "المخترع ولا الملكية."),
    ("D09", "Any digest or date in this document is an integrity aid only. It is not a legal "
            "timestamp, a notarization or proof of priority.",
     "أي بصمة رقمية (digest) أو تاريخ في هذه الوثيقة أداة للتحقق من سلامة المحتوى فقط، "
     "وليس ختمًا زمنيًا قانونيًا ولا توثيقًا رسميًا ولا دليلًا على الأسبقية."),
    ("D10", "Sharing this document may count as a disclosure of the invention in some "
            "jurisdictions. Consult a qualified patent professional before sharing it.",
     "قد تُعدّ مشاركة هذه الوثيقة إفصاحًا عن الاختراع في بعض الولايات القضائية. استشر "
     "مختصًا مؤهلًا في البراءات قبل مشاركتها."),
    ("D11", "For legal advice, consult a qualified patent professional.",
     "للحصول على استشارة قانونية، استشر مختصًا مؤهلًا في البراءات."),
)
SCOPE_LABEL = {
    "en": "Invention disclosure export — this project only — not legal advice",
    "ar": "تصدير الإفصاح عن الاختراع — هذا المشروع فقط — ليس استشارة قانونية",
}
CAPTURE_LIMITATION = (
    "InventorAI captures the problem statement at the step where the inventor describes "
    "the problem and may shorten it at a 500-character limit. The text shown here may "
    "therefore have been shortened; an ellipsis (…) at its end may indicate that "
    "shortening.")

# --- closed v1 token sets (§9.3) ----------------------------------------------
RECORDED = "RECORDED"
NOTHING_RECORDED = "NOTHING_RECORDED"
NOT_CAPTURED = "NOT_CAPTURED"
RAW_TEXT_ONLY = "RAW_TEXT_ONLY"
EXCLUDED = "EXCLUDED_FROM_FIRST_SLICE"
NOT_APPLICABLE = "NOT_APPLICABLE"
UNAVAILABLE = "UNAVAILABLE"
MARKERS = frozenset({RECORDED, NOTHING_RECORDED, NOT_CAPTURED, RAW_TEXT_ONLY, EXCLUDED,
                     NOT_APPLICABLE, UNAVAILABLE})

SYSTEM = "SYSTEM_ASSERTION"
QUOTED = "QUOTED_INVENTOR_CONTENT"
CONTENT_CLASSES = frozenset({SYSTEM, QUOTED})

REASONS = frozenset({
    "NON_INTEGRATED_PROJECT", "PLANNING_INPUTS", "CONFIDENTIAL_EVIDENCE_CATEGORIES",
    "RESULT_TEXT_NOT_CARRIED", "CARRIED_ON_EVERY_ITEM", "NO_APPROVAL_RECORD",
    "FORM_ROW_QUALITY_DERIVED", "OBJECTIVE_NAMES_EVIDENCE_LEVEL"})

SOURCE_OWNERS = frozenset({
    "SECTION2_RESOLUTION", "LEDGER", "SUBSYSTEM_COMPOSITION", "INTERFACE_DEPENDENCY",
    "ACKNOWLEDGED_UNKNOWNS", "NEED_ROUTING", "GAP_LIFECYCLE", "REQUIREMENT_LANDSCAPE",
    "REQUIREMENT_QUANTITY", "PROTOTYPE_TEST_PLAN", "PLANNING_METADATA",
    "EXPERIMENT_RESULTS", "DISCLOSURE_EXPORT"})

CURRENT = "CURRENT"
SUPERSEDED = "SUPERSEDED"
_PLANNING_PROVENANCE = frozenset({"user_defined", "source_stated"})

FIELD_TOKENS = (
    "invention_title", "problem_addressed", "background_and_existing_limitations",
    "invention_objective", "technical_concept", "parts",
    "component_descriptions_beyond_parts", "relationships",
    "operating_sequence_or_workflow", "alternative_embodiments",
    "typed_materials_dimensions_parameters_conditions",
    "raw_materials_dimensions_parameters_conditions",
    "interface_verification_preparation_inputs", "novelty_and_differentiation",
    "unresolved_technical_issues", "assumptions", "missing_information",
    "technical_evidence", "commercial_manufacturing_integration_evidence",
    "diagrams_and_files", "experiments", "experiment_result_text", "validation_results",
    "risks", "uncertainty_and_abstentions", "corrections", "approvals",
    "source_and_provenance_references", "requirement_landscape",
)

# Allowed (marker, reason, pointer) per field (§8.2); UNAVAILABLE is admitted only
# through the section-outcome seam (§3.4) and is never produced from the store.
_REC = (RECORDED, None, None)
_NOTHING = (NOTHING_RECORDED, None, None)
_NC = (NOT_CAPTURED, None, None)
_NON_INTEGRATED = (NOT_CAPTURED, "NON_INTEGRATED_PROJECT", None)
_FIELD_DISPOSITIONS = {
    "invention_title": {_NC},
    "problem_addressed": {_REC, _NOTHING},
    "background_and_existing_limitations": {_NC},
    "invention_objective": {_NC},
    "technical_concept": {_REC, _NOTHING},
    "parts": {_REC, _NON_INTEGRATED},
    "component_descriptions_beyond_parts": {_NC, _NON_INTEGRATED},
    "relationships": {_REC, _NOTHING, _NON_INTEGRATED},
    "operating_sequence_or_workflow": {_NC},
    "alternative_embodiments": {_NC},
    "typed_materials_dimensions_parameters_conditions": {_NC},
    "raw_materials_dimensions_parameters_conditions": {
        _REC, _NOTHING, (RAW_TEXT_ONLY, None, "requirement_landscape")},
    "interface_verification_preparation_inputs": {(EXCLUDED, "PLANNING_INPUTS", None)},
    "novelty_and_differentiation": {_NC},
    "unresolved_technical_issues": {_REC, _NOTHING},
    "assumptions": {_REC, _NOTHING},
    "missing_information": {_REC, _NOTHING},
    "technical_evidence": {_REC, _NOTHING},
    "commercial_manufacturing_integration_evidence": {
        (EXCLUDED, "CONFIDENTIAL_EVIDENCE_CATEGORIES", None)},
    "diagrams_and_files": {_NC},
    "experiments": {_REC, _NOTHING},
    "experiment_result_text": {(EXCLUDED, "RESULT_TEXT_NOT_CARRIED", None)},
    "validation_results": {_NC},
    "risks": {_REC, _NOTHING},
    "uncertainty_and_abstentions": {(NOT_APPLICABLE, "CARRIED_ON_EVERY_ITEM", None)},
    "corrections": {_REC, _NOTHING},
    "approvals": {(NOT_CAPTURED, "NO_APPROVAL_RECORD", None)},
    "source_and_provenance_references": {(NOT_APPLICABLE, "CARRIED_ON_EVERY_ITEM", None)},
    "requirement_landscape": {_REC, _NOTHING},
}

# Item kinds per field (§8.2, §8.3).
_FIELD_KINDS = {
    "problem_addressed": {"resolved_problem"},
    "technical_concept": {"known_mechanism"},
    "parts": {"part"},
    "relationships": {"interface"},
    "raw_materials_dimensions_parameters_conditions": {"requirement_quantity"},
    "unresolved_technical_issues": {"unresolved_gap", "declared_contradiction",
                                    "declared_contradiction_history"},
    "assumptions": {"assumption"},
    "missing_information": {"gap_reference", "acknowledged_unknown", "recorded_unknown",
                            "routed_specialist_need"},
    "technical_evidence": {"evidence_reference"},
    "experiments": {"experiment"},
    "risks": {"gap_reference"},
    "corrections": {"correction_version"},
    "requirement_landscape": {"requirement"},
}
ITEM_KINDS = frozenset(k for kinds in _FIELD_KINDS.values() for k in kinds)
REFERENCE_ONLY_KINDS = frozenset({"gap_reference", "evidence_reference"})

# Slots per kind: (slot token, expected content class or None for either).
_KIND_SLOTS = {
    "resolved_problem": {"text": QUOTED, "capture_limitation": SYSTEM},
    "known_mechanism": {"text": QUOTED},
    "part": {"name": QUOTED, "function": QUOTED},
    "interface": {"description": QUOTED, "dependency": SYSTEM, "dependency_note": QUOTED},
    "unresolved_gap": {"gap_state": SYSTEM},
    "declared_contradiction": {"declaration": SYSTEM, "answer_a": QUOTED, "answer_b": QUOTED},
    "declared_contradiction_history": {"declaration": SYSTEM, "answer_a": QUOTED,
                                       "answer_b": QUOTED},
    "assumption": {"text": QUOTED},
    "acknowledged_unknown": {"text": QUOTED},
    "recorded_unknown": {"unknown_disposition": SYSTEM},
    "routed_specialist_need": {"routed_need": SYSTEM},
    "gap_reference": {},
    "evidence_reference": {"cap11_form": None},
    "experiment": {"title": SYSTEM, "objective": SYSTEM, "what_to_observe": SYSTEM,
                   "success_criterion": QUOTED, "measurement_method": QUOTED,
                   "test_hypothesis": QUOTED, "test_variable": QUOTED,
                   "execution_state": SYSTEM},
    "correction_version": {"text": QUOTED},
    "requirement": {"label": SYSTEM, "status": SYSTEM, "resolving_action": SYSTEM,
                    "statement": None, "answer_a": QUOTED, "answer_b": QUOTED,
                    "part_a": QUOTED, "part_b": QUOTED, "description": QUOTED},
    "requirement_quantity": {"value_text": QUOTED},
}
SLOT_TOKENS = frozenset(s for slots in _KIND_SLOTS.values() for s in slots)

# The exact slot set of a requirement row per anchor kind (§7).
_ROW_BASE = frozenset({"label", "status", "resolving_action"})
_REQUIREMENT_SLOTS = {
    "assertion": _ROW_BASE | {"statement"},
    "pending_evidence": _ROW_BASE | {"statement"},
    "pending_specialist": _ROW_BASE | {"statement"},
    "gap": _ROW_BASE | {"statement"},
    "active_contradiction": (_ROW_BASE | {"answer_a", "answer_b"},
                             _ROW_BASE | {"statement", "answer_a", "answer_b"}),
    "subsystem_interface": _ROW_BASE | {"part_a", "part_b", "description"},
}

# Envelope fields a RECORDED slot of each (kind, slot) may carry as RECORDED;
# every other envelope field is NOT_APPLICABLE (§8.1, §8.3). An owner value can
# only appear where the owner holds one, so a substituted default is refused.
_PV = frozenset({"provenance", "validation_state"})
_PVC = frozenset({"provenance", "validation_state", "currency"})
_P = frozenset({"provenance"})
_NONE = frozenset()
_ENVELOPE_FIELDS = {
    ("resolved_problem", "text"): _PV, ("resolved_problem", "capture_limitation"): _NONE,
    ("known_mechanism", "text"): _PV,
    ("part", "name"): _PV, ("part", "function"): _PV,
    ("interface", "description"): _PV, ("interface", "dependency"): _NONE,
    ("interface", "dependency_note"): _NONE,
    ("unresolved_gap", "gap_state"): _NONE,
    ("declared_contradiction", "declaration"): _PVC,
    ("declared_contradiction", "answer_a"): _PVC, ("declared_contradiction", "answer_b"): _PVC,
    ("declared_contradiction_history", "declaration"): _PVC,
    ("declared_contradiction_history", "answer_a"): _PVC,
    ("declared_contradiction_history", "answer_b"): _PVC,
    ("assumption", "text"): _PVC,
    ("acknowledged_unknown", "text"): _NONE,
    ("recorded_unknown", "unknown_disposition"): _PVC,
    ("routed_specialist_need", "routed_need"): _P,
    ("experiment", "title"): _NONE, ("experiment", "objective"): _NONE,
    ("experiment", "what_to_observe"): _NONE, ("experiment", "execution_state"): _NONE,
    ("experiment", "success_criterion"): _P, ("experiment", "measurement_method"): _P,
    ("experiment", "test_hypothesis"): _P, ("experiment", "test_variable"): _P,
    ("correction_version", "text"): _PVC,
    ("requirement", "label"): _NONE, ("requirement", "status"): _NONE,
    ("requirement", "resolving_action"): _NONE, ("requirement", "statement"): _PVC,
    ("requirement", "answer_a"): _PVC, ("requirement", "answer_b"): _PVC,
    ("requirement", "part_a"): _PV, ("requirement", "part_b"): _PV,
    ("requirement", "description"): _PV,
    ("requirement_quantity", "value_text"): _PV,
}

# Item-level token keys per kind and slot-level token keys per (kind, slot) (§8.1).
_ITEM_TOKENS = {
    "part": frozenset({"part_domain"}),
    "assumption": frozenset({"gap_type"}),
    "acknowledged_unknown": frozenset({"gap_type"}),
    "correction_version": frozenset({"chain", "position", "gap_type", "disposition"}),
    "requirement": frozenset({"anchor_kind"}),
    "requirement_quantity": frozenset({"quantity_kind", "active", "anchor_active"}),
}
_SLOT_TOKENS = {
    ("interface", "dependency"): frozenset({"dependency_kind", "dependent_part",
                                            "depends_on_part"}),
    ("unresolved_gap", "gap_state"): frozenset({"gap_type", "gap_status"}),
    ("declared_contradiction", "declaration"): frozenset({"active"}),
    ("declared_contradiction_history", "declaration"): frozenset({"active"}),
    ("recorded_unknown", "unknown_disposition"): frozenset({"disposition", "gap_type"}),
    ("routed_specialist_need", "routed_need"): frozenset({"gap_type", "required_input"}),
    ("experiment", "execution_state"): frozenset({"state", "count"}),
}
TOKEN_KEYS = frozenset(k for keys in list(_ITEM_TOKENS.values())
                       + list(_SLOT_TOKENS.values()) for k in keys)

# Kinds a ref of each kind may name (§7, §8.3).
_REF_TARGETS = {
    "interface": frozenset({"part"}),
    "declared_contradiction": frozenset({"requirement"}),
    "assumption": frozenset({"assumption", "requirement", "correction_version"}),
    "recorded_unknown": frozenset({"requirement"}),
    "routed_specialist_need": frozenset({"requirement"}),
    "gap_reference": frozenset({"unresolved_gap"}),
    "evidence_reference": frozenset({"resolved_problem", "known_mechanism"}),
    "correction_version": frozenset({"assumption"}),
    "requirement": frozenset({"declared_contradiction", "interface"}),
    "requirement_quantity": frozenset({"requirement"}),
}

_PLANNING_CONCEPTS = ("success_criteria", "measurement_methods", "test_hypotheses",
                      "test_variables")
_RECORD_ROW_KINDS = frozenset({"assertion", "pending_evidence", "pending_specialist"})
_CORRECTION_DISPOSITIONS = INTERACTION_DISPOSITIONS - DECISION_ACTION_DISPOSITIONS
_EXECUTION_STATE_TOKENS = frozenset({"none", "recorded"})


class DisclosureExportRefused(Exception):
    """A bounded refusal: no JSON, no HTML, no file and no partial output. The
    message is structural only and never carries project content."""


@dataclass(frozen=True)
class MaterializedSources:
    """Every source value one export needs, read inside ONE snapshot (§3.1).
    ``section_outcomes`` is the section-outcome seam (§3.4, #24): empty for every
    store composition, because no first-slice source failure is section-local."""
    state: object
    requirement_quantities: tuple
    planning_metadata: dict
    interface_dependencies: tuple
    result_events: tuple
    section_outcomes: dict = field(default_factory=dict)


# --- snapshot materialization (§3.1 steps 2–6) ----------------------------------
def materialize_sources(store, project_id, account_id):
    """Read every source inside ONE store-owned snapshot. ``ProjectAccessDenied``
    from the authorization owner propagates; every other failure raises."""
    if not store.committed_state_readable():
        raise DisclosureExportRefused("the read snapshot cannot be acquired")
    with store.read_snapshot():
        get_authorized_project_read(store, project_id, account_id)            # S1
        reconstructed = reconstruct_readonly_state(store, project_id)        # S2
        if reconstructed.review.level != 1 or reconstructed.state is None:
            raise DisclosureExportRefused("the project cannot be reconstructed")
        quantities = tuple(store.load_requirement_quantities(project_id))    # S22
        planning = load_planning_metadata(store, project_id)                 # E2
        dependencies = tuple(store.load_interface_dependencies(project_id))  # S8
        events = tuple(store.load_result_events(project_id))                 # S7
        if store.committed_state_readable():
            raise DisclosureExportRefused("the read snapshot was lost")
    if not store.committed_state_readable():
        raise DisclosureExportRefused("the read snapshot did not end cleanly")
    return MaterializedSources(
        state=reconstructed.state, requirement_quantities=quantities,
        planning_metadata=planning, interface_dependencies=dependencies,
        result_events=events)


def compose_disclosure_projection(store, project_id, account_id):
    """The projection ``content`` of ONE owned project, or ``ProjectAccessDenied``
    (DENIAL) / ``DisclosureExportRefused`` (REFUSAL)."""
    try:
        sources = materialize_sources(store, project_id, account_id)
    except (ProjectAccessDenied, DisclosureExportRefused):
        raise
    except Exception:
        raise DisclosureExportRefused("a source could not be read") from None
    return compose_projection(sources)


# --- pure composition (§3.1 step 7, §5–§8) ---------------------------------------
def compose_projection(sources):
    """Compose and schema-check the projection from already-materialized sources,
    with no store access. Any failure is a REFUSAL."""
    try:
        content = _Composer(sources).content()
        check_projection(content)
    except DisclosureExportRefused:
        raise
    except Exception:
        raise DisclosureExportRefused("the projection could not be composed") from None
    return content


def _refuse(message):
    raise DisclosureExportRefused(message)


def _held(value):
    return ({"marker": RECORDED, "value": value} if value is not None
            else {"marker": NOT_APPLICABLE, "value": None})


def _envelope(provenance=None, validation_state=None, currency=None):
    return {"provenance": _held(provenance), "validation_state": _held(validation_state),
            "limitation": {"marker": NOT_APPLICABLE, "value": None},
            "currency": _held(currency)}


def _record_envelope(record):
    return _envelope(record.provenance, record.validation_status,
                     CURRENT if record.superseded_by is None else SUPERSEDED)


def _recorded(content_class, value, source_owner, envelope, tokens=None):
    return {"marker": RECORDED, "reason": None, "content_class": content_class,
            "value": value, "tokens": dict(tokens or {}), "source_owner": source_owner,
            "envelope": envelope}


def _marked(marker, reason=None):
    return {"marker": marker, "reason": reason, "content_class": None, "value": None,
            "tokens": {}, "source_owner": None, "envelope": None}


def _quoted_or_nothing(value, source_owner, envelope):
    return (_marked(NOTHING_RECORDED) if value is None
            else _recorded(QUOTED, value, source_owner, envelope))


def _key(token, n):
    return "%s.%d" % (token, n)


def _item(key, kind, slots, tokens=None, refs=None):
    return {"item_key": key, "kind": kind, "tokens": dict(tokens or {}),
            "refs": list(refs or []), "slots": slots}


def _field(token, marker, items=None, reason=None, pointer=None):
    return {"field": token, "marker": marker, "reason": reason, "pointer": pointer,
            "items": list(items or [])}


def _listed(token, items):
    return _field(token, RECORDED if items else NOTHING_RECORDED, items)


class _Composer:
    """One pass over one materialized snapshot. Keys are fixed by owner order
    before any item is built, so every cross-reference names a stable key."""

    def __init__(self, sources):
        planning = sources.planning_metadata
        if any(planning.get(concept) is None for concept in _PLANNING_CONCEPTS):
            _refuse("planning metadata is not bound to this project")
        state = sources.state
        apply_planning_metadata(state, planning)
        state.requirement_quantities = list(sources.requirement_quantities)
        self.state = state
        self.dependencies = tuple(sources.interface_dependencies)
        self.events = tuple(sources.result_events)
        self.outcomes = dict(sources.section_outcomes or {})
        self.records = list(state.assertions)
        self.by_id = {r.record_id: r for r in self.records}
        if len(self.by_id) != len(self.records):
            _refuse("duplicate ledger identity")
        self.package = assemble_deliverable(state)
        self.landscape = derive_requirement_landscape(state).requirements
        self.quantity_meta = requirement_quantities_meta(state)
        self.routes = active_routes(state)
        self.declared_pairs = active_declared_contradiction_pairs(self.records)
        self.integrated = bool(state.subsystems)
        self.gaps = [g for g in state.gaps if g.status in (OPEN, PARTIAL)]
        self.declarations = [r for r in self.records
                             if r.disposition == DISPOSITION_CONTRADICTION_DECLARED]
        self._assign_keys()
        self.chains = self._correction_chains()

    # -- keys ---------------------------------------------------------------
    def _assign_keys(self):
        state = self.state
        self.part_keys = ({s.subsystem_id: _key("parts", n)
                           for n, s in enumerate(state.subsystems, 1)}
                          if self.integrated else {})
        self.interface_keys = ({i.interface_id: _key("relationships", n)
                                for n, i in enumerate(state.subsystem_interfaces, 1)}
                               if self.integrated else {})
        self.gap_keys = [_key("unresolved_technical_issues", n)
                         for n in range(1, len(self.gaps) + 1)]
        self.declaration_keys = {
            d.record_id: _key("unresolved_technical_issues", len(self.gaps) + n)
            for n, d in enumerate(self.declarations, 1)}
        self.assumption_keys = {
            r.record_id: _key("assumptions", n) for n, r in enumerate(
                [r for r in self.records
                 if r.disposition == DISPOSITION_PROVISIONAL_ASSUMPTION], 1)}
        self.row_keys, self.own_rows, self.routing_rows = {}, {}, {}
        self.contradiction_rows = []
        for n, req in enumerate(self.landscape, 1):
            key = _key("requirement_landscape", n)
            if req.requirement_id in self.row_keys:
                _refuse("duplicate requirement identity")
            self.row_keys[req.requirement_id] = key
            kind = req.primary_anchor.anchor_kind
            reference = req.primary_anchor.anchor_reference
            if kind in _RECORD_ROW_KINDS:
                if reference in self.by_id:
                    self.own_rows[reference] = key
                else:
                    self.routing_rows[reference] = key
            elif kind == "active_contradiction":
                lo, hi = reference.split("|", 1)
                self.contradiction_rows.append((lo, hi, key))

    def canonical_rows(self, record_id):
        """The field-29 row(s) canonically representing ``record_id`` (§7)."""
        if record_id in self.own_rows:
            return [self.own_rows[record_id]]
        rows = [key for lo, hi, key in self.contradiction_rows if record_id in (lo, hi)]
        if not rows:
            _refuse("a record has no canonical requirement row")
        return rows

    # -- correction chains (§8.3) -------------------------------------------
    def _correction_chains(self):
        members = [r for r in self.records if r.disposition in _CORRECTION_DISPOSITIONS]
        ids = {r.record_id for r in members}
        order = {r.record_id: n for n, r in enumerate(self.records)}
        visited, chains = set(), []
        for root in members:
            if any(prior in ids for prior in (root.supersedes or ())):
                continue
            chain, node = [root], root
            visited.add(root.record_id)
            while node.superseded_by is not None and node.superseded_by in ids:
                node = self.by_id[node.superseded_by]
                if node.record_id in visited:
                    _refuse("cyclic supersession history")
                visited.add(node.record_id)
                chain.append(node)
            chains.append(chain)
        if visited != ids:
            _refuse("inconsistent supersession history")
        carried = []
        for chain in chains:
            assumption_at = [n for n, r in enumerate(chain)
                             if r.disposition == DISPOSITION_PROVISIONAL_ASSUMPTION]
            if not assumption_at:
                if len(chain) >= 2:
                    carried.append((chain, None))
                continue
            if classify_assumption_ancestry(chain[-1], self.by_id) != \
                    ANCESTRY_ASSUMPTION_ORIGIN:
                _refuse("malformed assumption ancestry")
            segment = chain[assumption_at[-1] + 1:]
            if len(segment) >= 2:
                carried.append((segment, chain[assumption_at[-1]].record_id))
        carried.sort(key=lambda entry: order[entry[0][0].record_id])
        self.correction_keys, n = {}, 0
        for chain, _origin in carried:
            for record in chain:
                n += 1
                self.correction_keys[record.record_id] = _key("corrections", n)
        return carried

    # -- fields -------------------------------------------------------------
    def content(self):
        fields = {
            "invention_title": _field("invention_title", NOT_CAPTURED),
            "problem_addressed": self._problem(),
            "background_and_existing_limitations": _field(
                "background_and_existing_limitations", NOT_CAPTURED),
            "invention_objective": _field("invention_objective", NOT_CAPTURED),
            "technical_concept": self._mechanism(),
            "parts": self._parts(),
            "component_descriptions_beyond_parts": _field(
                "component_descriptions_beyond_parts", NOT_CAPTURED,
                reason=None if self.integrated else "NON_INTEGRATED_PROJECT"),
            "relationships": self._relationships(),
            "operating_sequence_or_workflow": _field("operating_sequence_or_workflow",
                                                     NOT_CAPTURED),
            "alternative_embodiments": _field("alternative_embodiments", NOT_CAPTURED),
            "typed_materials_dimensions_parameters_conditions": _field(
                "typed_materials_dimensions_parameters_conditions", NOT_CAPTURED),
            "interface_verification_preparation_inputs": _field(
                "interface_verification_preparation_inputs", EXCLUDED,
                reason="PLANNING_INPUTS"),
            "novelty_and_differentiation": _field("novelty_and_differentiation",
                                                  NOT_CAPTURED),
            "unresolved_technical_issues": self._unresolved(),
            "assumptions": self._assumptions(),
            "missing_information": self._missing(),
            "technical_evidence": self._evidence(),
            "commercial_manufacturing_integration_evidence": _field(
                "commercial_manufacturing_integration_evidence", EXCLUDED,
                reason="CONFIDENTIAL_EVIDENCE_CATEGORIES"),
            "diagrams_and_files": _field("diagrams_and_files", NOT_CAPTURED),
            "experiments": self._experiments(),
            "experiment_result_text": _field("experiment_result_text", EXCLUDED,
                                             reason="RESULT_TEXT_NOT_CARRIED"),
            "validation_results": _field("validation_results", NOT_CAPTURED),
            "risks": _listed("risks", self._gap_references("risks")),
            "uncertainty_and_abstentions": _field(
                "uncertainty_and_abstentions", NOT_APPLICABLE,
                reason="CARRIED_ON_EVERY_ITEM"),
            "corrections": self._corrections(),
            "approvals": _field("approvals", NOT_CAPTURED, reason="NO_APPROVAL_RECORD"),
            "source_and_provenance_references": _field(
                "source_and_provenance_references", NOT_APPLICABLE,
                reason="CARRIED_ON_EVERY_ITEM"),
        }
        landscape = self._landscape()
        fields["requirement_landscape"] = landscape
        fields["raw_materials_dimensions_parameters_conditions"] = self._quantities(landscape)
        for token, outcome in self.outcomes.items():
            if token not in fields or outcome != UNAVAILABLE:
                _refuse("unknown section outcome")
            fields[token] = _field(token, UNAVAILABLE)
        ordered = [fields[token] for token in FIELD_TOKENS]
        return {
            "disclaimers": [{"id": i, "en": en, "ar": ar} for i, en, ar in DISCLAIMERS],
            "scope_label": dict(SCOPE_LABEL),
            "unavailable_notice": _any_unavailable(ordered),
            "fields": ordered,
        }

    def _problem(self):
        problem = resolved_problem(self.state)
        if problem is None:
            return _field("problem_addressed", NOTHING_RECORDED)
        slots = {
            "text": _recorded(QUOTED, problem.content, "SECTION2_RESOLUTION",
                              _envelope(problem.provenance, problem.validation_status)),
            "capture_limitation": _recorded(SYSTEM, CAPTURE_LIMITATION,
                                            "DISCLOSURE_EXPORT", _envelope()),
        }
        return _listed("problem_addressed",
                       [_item(_key("problem_addressed", 1), "resolved_problem", slots)])

    def _mechanism(self):
        mechanism = self.state.known_mechanism
        if mechanism is None:
            return _field("technical_concept", NOTHING_RECORDED)
        slots = {"text": _recorded(QUOTED, mechanism.content, "SECTION2_RESOLUTION",
                                   _envelope(mechanism.provenance,
                                             mechanism.validation_status))}
        return _listed("technical_concept",
                       [_item(_key("technical_concept", 1), "known_mechanism", slots)])

    def _parts(self):
        if not self.integrated:
            return _field("parts", NOT_CAPTURED, reason="NON_INTEGRATED_PROJECT")
        items = []
        for sub in self.state.subsystems:
            env = _envelope(sub.provenance, sub.validation_state)
            items.append(_item(
                self.part_keys[sub.subsystem_id], "part",
                {"name": _quoted_or_nothing(sub.display_name, "SUBSYSTEM_COMPOSITION", env),
                 "function": _quoted_or_nothing(sub.function_text, "SUBSYSTEM_COMPOSITION",
                                                _envelope(sub.provenance,
                                                          sub.validation_state))},
                tokens={"part_domain": sub.domain}))
        return _listed("parts", items)

    def _relationships(self):
        if not self.integrated:
            return _field("relationships", NOT_CAPTURED, reason="NON_INTEGRATED_PROJECT")
        dependencies = {}
        for dependency in self.dependencies:
            if dependency.interface_id not in self.interface_keys \
                    or dependency.interface_id in dependencies:
                _refuse("a dependency names no interface of this project")
            dependencies[dependency.interface_id] = dependency
        items = []
        for interface in self.state.subsystem_interfaces:
            ends = [self.part_keys.get(interface.subsystem_a_id),
                    self.part_keys.get(interface.subsystem_b_id)]
            if None in ends:
                _refuse("an interface endpoint does not resolve")
            slots = {"description": _recorded(
                QUOTED, interface.description, "SUBSYSTEM_COMPOSITION",
                _envelope(interface.provenance, interface.validation_state))}
            dependency = dependencies.get(interface.interface_id)
            if dependency is None:
                slots["dependency"] = _marked(NOTHING_RECORDED)
                slots["dependency_note"] = _marked(NOTHING_RECORDED)
            else:
                tokens = {"dependency_kind": dependency.kind}
                if dependency.kind == DEPENDENCY_ONE_WAY:
                    tokens["dependent_part"] = self.part_keys.get(
                        dependency.dependent_subsystem_id)
                    tokens["depends_on_part"] = self.part_keys.get(
                        dependency.depends_on_subsystem_id)
                    if None in (tokens["dependent_part"], tokens["depends_on_part"]):
                        _refuse("a dependency part does not resolve")
                elif dependency.kind != DEPENDENCY_MUTUAL:
                    _refuse("unknown dependency kind")
                slots["dependency"] = _recorded(SYSTEM, None, "INTERFACE_DEPENDENCY",
                                                _envelope(), tokens)
                slots["dependency_note"] = _quoted_or_nothing(
                    dependency.note, "INTERFACE_DEPENDENCY", _envelope())
            items.append(_item(self.interface_keys[interface.interface_id], "interface",
                               slots, refs=ends))
        return _listed("relationships", items)

    def _unresolved(self):
        items = []
        for key, gap in zip(self.gap_keys, self.gaps):
            items.append(_item(key, "unresolved_gap", {"gap_state": _recorded(
                SYSTEM, None, "GAP_LIFECYCLE", _envelope(),
                {"gap_type": gap.gap_type, "gap_status": gap.status})}))
        for declaration in self.declarations:
            pair = tuple(declaration.contradiction_endpoints or ())
            if len(pair) != 2 or pair[0] not in self.by_id or pair[1] not in self.by_id:
                _refuse("a declared contradiction endpoint does not resolve")
            active = pair in self.declared_pairs
            a, b = self.by_id[pair[0]], self.by_id[pair[1]]
            refs = []
            if active:
                refs = [key for lo, hi, key in self.contradiction_rows if (lo, hi) == pair]
                if len(refs) != 1:
                    _refuse("a declared contradiction has no requirement row")
            items.append(_item(
                self.declaration_keys[declaration.record_id],
                "declared_contradiction" if active else "declared_contradiction_history",
                {"declaration": _recorded(SYSTEM, None, "LEDGER",
                                          _record_envelope(declaration), {"active": active}),
                 "answer_a": _recorded(QUOTED, a.content, "LEDGER", _record_envelope(a)),
                 "answer_b": _recorded(QUOTED, b.content, "LEDGER", _record_envelope(b))},
                refs=refs))
        return _listed("unresolved_technical_issues", items)

    def _assumptions(self):
        items = []
        for record in self.records:
            if record.disposition != DISPOSITION_PROVISIONAL_ASSUMPTION:
                continue
            refs = []
            if record.superseded_by is not None:
                successor = self.by_id.get(record.superseded_by)
                if successor is None:
                    _refuse("an assumption successor does not resolve")
                if successor.disposition == DISPOSITION_PROVISIONAL_ASSUMPTION:
                    refs = [self.assumption_keys[successor.record_id]]
                elif successor.disposition == DISPOSITION_ANSWERED:
                    if successor.superseded_by is None:
                        refs = self.canonical_rows(successor.record_id)
                    elif successor.record_id in self.correction_keys:
                        refs = [self.correction_keys[successor.record_id]]
                    else:
                        _refuse("an assumption successor has no correction item")
                else:
                    _refuse("an assumption successor has another disposition")
            items.append(_item(
                self.assumption_keys[record.record_id], "assumption",
                {"text": _recorded(QUOTED, record.content, "LEDGER",
                                   _record_envelope(record))},
                tokens={"gap_type": record.gap_context}, refs=refs))
        return _listed("assumptions", items)

    def _gap_references(self, token):
        return [_item(_key(token, n), "gap_reference", {}, refs=[gap_key])
                for n, gap_key in enumerate(self.gap_keys, 1)]

    def _missing(self):
        items = self._gap_references("missing_information")
        n = len(items)
        for unknown in self.state.acknowledged_unknowns:
            n += 1
            items.append(_item(
                _key("missing_information", n), "acknowledged_unknown",
                {"text": _recorded(QUOTED, unknown.verbatim, "ACKNOWLEDGED_UNKNOWNS",
                                   _envelope())},
                tokens={"gap_type": unknown.gap_context}))
        for record in self.records:
            if record.disposition != DISPOSITION_UNKNOWN or record.superseded_by is not None:
                continue
            n += 1
            items.append(_item(
                _key("missing_information", n), "recorded_unknown",
                {"unknown_disposition": _recorded(
                    SYSTEM, None, "LEDGER", _record_envelope(record),
                    {"disposition": record.disposition, "gap_type": record.gap_context})},
                refs=self.canonical_rows(record.record_id)))
        for revision in self.routes.values():
            if revision.required_input != REQUIRED_INPUT_SPECIALIST:
                continue
            row = self.routing_rows.get(
                "routing:" + revision.gap_type + ":" + revision.question_id)
            if row is None:
                _refuse("a routed need has no requirement row")
            n += 1
            items.append(_item(
                _key("missing_information", n), "routed_specialist_need",
                {"routed_need": _recorded(
                    SYSTEM, None, "NEED_ROUTING", _envelope(revision.provenance),
                    {"gap_type": revision.gap_type,
                     "required_input": revision.required_input})},
                refs=[row]))
        return _listed("missing_information", items)

    def _evidence(self):
        targets = []
        if resolved_problem(self.state) is not None:
            targets.append(_key("problem_addressed", 1))
        if self.state.known_mechanism is not None:
            targets.append(_key("technical_concept", 1))
        items = [_item(_key("technical_evidence", n), "evidence_reference",
                       {"cap11_form": _marked(EXCLUDED, "FORM_ROW_QUALITY_DERIVED")},
                       refs=[target])
                 for n, target in enumerate(targets, 1)]
        return _listed("technical_evidence", items)

    def _experiments(self):
        plan = self.package["section_11_prototype_test_plan"]["items"]
        states = execution_states(self.events, [it["experiment_id"] for it in plan])
        items = []
        for n, it in enumerate(plan, 1):
            slots = {
                "title": _recorded(SYSTEM, it["experiment_title"], "PROTOTYPE_TEST_PLAN",
                                   _envelope()),
                "objective": (
                    _marked(EXCLUDED, "OBJECTIVE_NAMES_EVIDENCE_LEVEL")
                    if it["traceability"]["source_type"] == "reasoned_leading_claim"
                    else _recorded(SYSTEM, it["objective"], "PROTOTYPE_TEST_PLAN",
                                   _envelope())),
                "what_to_observe": _recorded(SYSTEM, it["what_to_observe"],
                                             "PROTOTYPE_TEST_PLAN", _envelope()),
            }
            if it["success_criterion_status"] == "required":
                slots["success_criterion"] = _marked(NOTHING_RECORDED)
            else:
                provenance = it["success_criterion_provenance"]
                slots["success_criterion"] = _recorded(
                    QUOTED, it["success_criterion"],
                    "PLANNING_METADATA" if provenance == "user_defined"
                    else "PROTOTYPE_TEST_PLAN", _envelope(provenance))
            for slot in ("measurement_method", "test_hypothesis", "test_variable"):
                slots[slot] = (_recorded(QUOTED, it[slot], "PLANNING_METADATA",
                                         _envelope(it[slot + "_provenance"]))
                               if slot in it else _marked(NOTHING_RECORDED))
            execution = states[it["experiment_id"]]
            slots["execution_state"] = _recorded(
                SYSTEM, None, "EXPERIMENT_RESULTS", _envelope(),
                {"state": execution["state"], "count": execution["count"]})
            items.append(_item(_key("experiments", n), "experiment", slots))
        return _listed("experiments", items)

    def _corrections(self):
        items = []
        for chain_no, (chain, origin) in enumerate(self.chains, 1):
            for position, record in enumerate(chain, 1):
                refs = ([self.assumption_keys[origin]]
                        if origin is not None and position == 1 else [])
                items.append(_item(
                    self.correction_keys[record.record_id], "correction_version",
                    {"text": _recorded(QUOTED, record.content, "LEDGER",
                                       _record_envelope(record))},
                    tokens={"chain": chain_no, "position": position,
                            "gap_type": record.gap_context,
                            "disposition": record.disposition},
                    refs=refs))
        return _listed("corrections", items)

    def _landscape(self):
        interfaces = {i.interface_id: i for i in self.state.subsystem_interfaces}
        parts = {s.subsystem_id: s for s in self.state.subsystems}
        routing = {"routing:%s:%s" % need for need in self.routes}
        items = []
        for req in self.landscape:
            kind = req.primary_anchor.anchor_kind
            reference = req.primary_anchor.anchor_reference

            def system(value):
                return _recorded(SYSTEM, value, "REQUIREMENT_LANDSCAPE", _envelope())
            slots = {
                "label": system(req.primary_anchor.display_label),
                "status": system(req.source_status),
                "resolving_action": (system(req.resolving_action.statement)
                                     if req.resolving_action is not None
                                     else _marked(NOTHING_RECORDED)),
            }
            refs = []
            if kind in _RECORD_ROW_KINDS:
                record = self.by_id.get(reference)
                if record is not None:
                    slots["statement"] = (
                        _recorded(QUOTED, record.content, "LEDGER", _record_envelope(record))
                        if (record.content or "").strip() else _marked(NOTHING_RECORDED))
                elif reference in routing:
                    slots["statement"] = system(req.statement)
                else:
                    _refuse("a requirement anchor does not resolve")
            elif kind == "gap":
                slots["statement"] = system(req.statement)
            elif kind == "active_contradiction":
                lo, hi = reference.split("|", 1)
                if lo not in self.by_id or hi not in self.by_id:
                    _refuse("a contradiction endpoint does not resolve")
                a, b = self.by_id[lo], self.by_id[hi]
                if (lo, hi) in self.declared_pairs:
                    refs = [self.declaration_keys[d.record_id] for d in self.declarations
                            if tuple(d.contradiction_endpoints or ()) == (lo, hi)]
                else:
                    slots["statement"] = system(req.statement)
                slots["answer_a"] = _recorded(QUOTED, a.content, "LEDGER", _record_envelope(a))
                slots["answer_b"] = _recorded(QUOTED, b.content, "LEDGER", _record_envelope(b))
            elif kind == "subsystem_interface":
                interface = interfaces.get(reference)
                if interface is None or reference not in self.interface_keys:
                    _refuse("an interface row does not resolve")
                a = parts.get(interface.subsystem_a_id)
                b = parts.get(interface.subsystem_b_id)
                if a is None or b is None:
                    _refuse("an interface part does not resolve")
                env = _envelope(interface.provenance, interface.validation_state)
                slots["part_a"] = _recorded(QUOTED, a.display_name, "SUBSYSTEM_COMPOSITION",
                                            env)
                slots["part_b"] = _recorded(QUOTED, b.display_name, "SUBSYSTEM_COMPOSITION",
                                            _envelope(interface.provenance,
                                                      interface.validation_state))
                slots["description"] = _recorded(
                    QUOTED, interface.description, "SUBSYSTEM_COMPOSITION",
                    _envelope(interface.provenance, interface.validation_state))
                refs = [self.interface_keys[reference]]
            else:
                _refuse("unknown requirement anchor kind")
            items.append(_item(self.row_keys[req.requirement_id], "requirement", slots,
                               tokens={"anchor_kind": kind}, refs=refs))
        return _listed("requirement_landscape", items)

    def _quantities(self, landscape):
        rows = (self.quantity_meta or {}).get("rows") or []
        if not rows:
            quoted = any(v["marker"] == RECORDED and v["content_class"] == QUOTED
                         for item in landscape["items"] for v in item["slots"].values())
            if quoted:
                return _field("raw_materials_dimensions_parameters_conditions",
                              RAW_TEXT_ONLY, pointer="requirement_landscape")
            return _field("raw_materials_dimensions_parameters_conditions",
                          NOTHING_RECORDED)
        items = []
        for n, row in enumerate(rows, 1):
            refs = []
            if row["anchor_active"]:
                key = self.row_keys.get(row["requirement_id"])
                if key is None or self.own_rows.get(row["anchor_record_id"]) != key:
                    _refuse("a quantity anchor has no requirement row")
                refs = [key]
            items.append(_item(
                _key("raw_materials_dimensions_parameters_conditions", n),
                "requirement_quantity",
                {"value_text": _recorded(QUOTED, row["value_text"], "REQUIREMENT_QUANTITY",
                                         _envelope(row["provenance"],
                                                   row["validation_status"]))},
                tokens={"quantity_kind": row["quantity_kind"], "active": row["active"],
                        "anchor_active": row["anchor_active"]},
                refs=refs))
        return _listed("raw_materials_dimensions_parameters_conditions", items)


def _any_unavailable(fields):
    for f in fields:
        if f["marker"] == UNAVAILABLE:
            return True
        for item in f["items"]:
            for value in item["slots"].values():
                if value["marker"] == UNAVAILABLE:
                    return True
                for env in (value["envelope"] or {}).values():
                    if env["marker"] == UNAVAILABLE:
                        return True
    return False


# --- schema check (§9.6) ---------------------------------------------------------
_CONTENT_KEYS = frozenset({"disclaimers", "scope_label", "unavailable_notice", "fields"})
_FIELD_KEYS = frozenset({"field", "marker", "reason", "pointer", "items"})
_ITEM_KEYS = frozenset({"item_key", "kind", "tokens", "refs", "slots"})
_VALUE_KEYS = frozenset({"marker", "reason", "content_class", "value", "tokens",
                         "source_owner", "envelope"})
_ENVELOPE_KEYS = ("provenance", "validation_state", "limitation", "currency")
_ENVELOPE_VALUES = {
    "provenance": frozenset(PROVENANCE_VALUES) | _PLANNING_PROVENANCE,
    "validation_state": frozenset(VALIDATION_STATUSES),
    "currency": frozenset({CURRENT, SUPERSEDED}),
}


def _check(condition, message):
    if not condition:
        raise DisclosureExportRefused("schema: " + message)


def _check_text(value):
    _check(value is None or isinstance(value, str), "value type")
    if isinstance(value, str):
        try:
            value.encode("utf-8")
        except UnicodeError:
            _check(False, "value encoding")


def _check_scalar(value):
    _check(value is None or isinstance(value, (str, int, bool)), "token type")
    if isinstance(value, str):
        _check_text(value)


def check_projection(content):
    """Validate the finished projection against the closed v1 schema; any
    unknown key, token, marker, reason or kind, any attribution defect and any
    dangling ref refuses (global schema failure)."""
    _check(isinstance(content, dict) and set(content) == _CONTENT_KEYS, "content keys")
    _check(content["disclaimers"] == [{"id": i, "en": en, "ar": ar}
                                      for i, en, ar in DISCLAIMERS], "disclaimers")
    _check(content["scope_label"] == SCOPE_LABEL, "scope label")
    fields = content["fields"]
    _check(isinstance(fields, list)
           and [f.get("field") if isinstance(f, dict) else None for f in fields]
           == list(FIELD_TOKENS), "field order")
    index = {}
    for f in fields:
        _check(set(f) == _FIELD_KEYS, "field keys")
        combo = (f["marker"], f["reason"], f["pointer"])
        _check(combo in _FIELD_DISPOSITIONS[f["field"]] or combo == (UNAVAILABLE, None, None),
               "field disposition")
        items = f["items"]
        _check(isinstance(items, list), "items")
        _check(bool(items) == (f["marker"] == RECORDED), "items versus marker")
        for n, item in enumerate(items, 1):
            _check(isinstance(item, dict) and set(item) == _ITEM_KEYS, "item keys")
            _check(item["item_key"] == _key(f["field"], n), "item key")
            _check(item["kind"] in _FIELD_KINDS.get(f["field"], ()), "item kind")
            index[item["item_key"]] = item
    for item in index.values():
        _check_item(item, index)
    _check(content["unavailable_notice"] is _any_unavailable(fields), "unavailable notice")


def _check_item(item, index):
    kind = item["kind"]
    tokens, refs, slots = item["tokens"], item["refs"], item["slots"]
    _check(isinstance(tokens, dict) and set(tokens) <= _ITEM_TOKENS.get(kind, frozenset()),
           "item tokens")
    for value in tokens.values():
        _check_scalar(value)
    _check(isinstance(refs, list) and all(isinstance(r, str) for r in refs), "refs")
    for ref in refs:
        _check(ref in index, "dangling ref")
        _check(index[ref]["kind"] in _REF_TARGETS.get(kind, ()), "ref target kind")
    allowed = _KIND_SLOTS[kind]
    _check(isinstance(slots, dict) and set(slots) <= set(allowed), "slot tokens")
    recorded = []
    for slot, value in slots.items():
        _check_value(kind, slot, value, allowed[slot], index)
        if value["marker"] == RECORDED:
            recorded.append(slot)
    if kind in REFERENCE_ONLY_KINDS:
        _check(not recorded and len(refs) == 1, "reference-only item")
    else:
        _check(bool(recorded), "truth-bearing item without attribution")
    _check_kind(kind, tokens, refs, slots, index)


def _check_value(kind, slot, value, expected_class, index):
    _check(isinstance(value, dict) and set(value) == _VALUE_KEYS, "value keys")
    marker = value["marker"]
    _check(marker in MARKERS, "value marker")
    if marker != RECORDED:
        _check(value["content_class"] is None and value["value"] is None
               and value["source_owner"] is None and value["envelope"] is None
               and value["tokens"] == {}, "non-recorded value")
        _check(value["reason"] is None or value["reason"] in REASONS, "value reason")
        return
    _check(value["reason"] is None, "recorded value reason")
    _check(value["content_class"] in CONTENT_CLASSES, "content class")
    _check(expected_class is None or value["content_class"] == expected_class,
           "content class for slot")
    _check(value["source_owner"] in SOURCE_OWNERS, "source owner")
    _check_text(value["value"])
    tokens = value["tokens"]
    _check(isinstance(tokens, dict)
           and set(tokens) <= _SLOT_TOKENS.get((kind, slot), frozenset()), "slot tokens")
    for token in tokens.values():
        _check_scalar(token)
    envelope = value["envelope"]
    _check(isinstance(envelope, dict) and tuple(sorted(envelope)) == tuple(
        sorted(_ENVELOPE_KEYS)), "envelope keys")
    may_record = _ENVELOPE_FIELDS.get((kind, slot), frozenset())
    for name in _ENVELOPE_KEYS:
        entry = envelope[name]
        _check(isinstance(entry, dict) and set(entry) == {"marker", "value"}, "envelope entry")
        _check(entry["marker"] in (RECORDED, NOT_APPLICABLE, UNAVAILABLE), "envelope marker")
        if entry["marker"] == RECORDED:
            _check(name in may_record, "envelope value the owner does not hold")
            _check(entry["value"] in _ENVELOPE_VALUES[name], "envelope token")
        else:
            _check(entry["value"] is None, "envelope value")


def _check_kind(kind, tokens, refs, slots, index):
    """The per-kind structural rules of §7, §8.1 and §8.3."""
    if kind == "resolved_problem":
        _check(set(slots) == {"text", "capture_limitation"}, "problem slots")
        lim = slots["capture_limitation"]
        _check(lim["marker"] == RECORDED and lim["value"] == CAPTURE_LIMITATION
               and lim["source_owner"] == "DISCLOSURE_EXPORT", "capture limitation")
    elif kind == "experiment":
        _check(set(slots) == set(_KIND_SLOTS["experiment"]), "experiment slots")
        state = slots["execution_state"]
        _check(state["marker"] == RECORDED and set(state["tokens"]) == {"state", "count"}
               and state["tokens"]["state"] in _EXECUTION_STATE_TOKENS
               and isinstance(state["tokens"]["count"], int)
               and (state["tokens"]["count"] > 0) == (state["tokens"]["state"] == "recorded"),
               "execution state")
    elif kind == "requirement_quantity":
        _check(set(slots) == {"value_text"}, "quantity slots")
        _check(set(tokens) == {"quantity_kind", "active", "anchor_active"}
               and tokens["quantity_kind"] in QUANTITY_KINDS
               and isinstance(tokens["active"], bool)
               and isinstance(tokens["anchor_active"], bool), "quantity tokens")
        _check(len(refs) == (1 if tokens["anchor_active"] else 0), "quantity ref")
        for ref in refs:
            _check(index[ref]["tokens"].get("anchor_kind") == "assertion", "quantity row")
    elif kind == "requirement":
        anchor = tokens.get("anchor_kind")
        _check(anchor in _REQUIREMENT_SLOTS, "anchor kind")
        allowed = _REQUIREMENT_SLOTS[anchor]
        allowed = allowed if isinstance(allowed, tuple) else (allowed,)
        _check(frozenset(slots) in allowed, "requirement slots")
        if anchor == "subsystem_interface":
            _check(len(refs) == 1 and index[refs[0]]["kind"] == "interface", "interface row")
        elif anchor == "active_contradiction" and "statement" not in slots:
            _check(len(refs) >= 1 and all(index[r]["kind"] == "declared_contradiction"
                                          for r in refs), "declared row")
        else:
            _check(refs == [], "requirement refs")
        statement = slots.get("statement")
        if statement is not None and statement["marker"] == RECORDED \
                and statement["content_class"] == SYSTEM:
            _check(all(v["marker"] == NOT_APPLICABLE
                       for v in statement["envelope"].values()), "system statement")
    elif kind == "interface":
        _check(set(slots) == {"description", "dependency", "dependency_note"}
               and len(refs) == 2, "interface item")
        dependency = slots["dependency"]
        if dependency["marker"] == RECORDED:
            dep = dependency["tokens"]
            if dep.get("dependency_kind") == DEPENDENCY_ONE_WAY:
                _check(set(dep) == {"dependency_kind", "dependent_part", "depends_on_part"}
                       and dep["dependent_part"] in refs and dep["depends_on_part"] in refs
                       and dep["dependent_part"] != dep["depends_on_part"], "one-way dependency")
            else:
                _check(dep == {"dependency_kind": DEPENDENCY_MUTUAL}, "mutual dependency")
        else:
            _check(slots["dependency_note"]["marker"] != RECORDED, "note without dependency")
    elif kind in ("declared_contradiction", "declared_contradiction_history"):
        active = slots["declaration"]["tokens"].get("active")
        _check(active is (kind == "declared_contradiction"), "declaration state")
        _check(len(refs) == (1 if active else 0), "declaration ref")
    elif kind == "unresolved_gap":
        _check(slots["gap_state"]["tokens"].get("gap_status") in (OPEN, PARTIAL)
               and set(slots["gap_state"]["tokens"]) == {"gap_type", "gap_status"},
               "gap state")
    elif kind == "recorded_unknown":
        state = slots["unknown_disposition"]["tokens"]
        _check(set(state) == {"disposition", "gap_type"}
               and state["disposition"] == DISPOSITION_UNKNOWN and refs, "recorded unknown")
    elif kind == "routed_specialist_need":
        need = slots["routed_need"]["tokens"]
        _check(set(need) == {"gap_type", "required_input"}
               and need["required_input"] == REQUIRED_INPUT_SPECIALIST
               and len(refs) == 1, "routed need")
    elif kind == "evidence_reference":
        form = slots.get("cap11_form")
        _check(set(slots) == {"cap11_form"} and form["marker"] == EXCLUDED
               and form["reason"] == "FORM_ROW_QUALITY_DERIVED", "evidence reference")
    elif kind == "gap_reference":
        _check(slots == {}, "gap reference")
    elif kind == "correction_version":
        _check(set(tokens) == {"chain", "position", "gap_type", "disposition"}
               and isinstance(tokens["chain"], int) and tokens["chain"] >= 1
               and isinstance(tokens["position"], int) and tokens["position"] >= 1
               and len(refs) <= (1 if tokens["position"] == 1 else 0), "correction item")
    elif kind == "part":
        _check(set(tokens) == {"part_domain"}, "part tokens")


# --- serialization (§9.2, §9.4) --------------------------------------------------
def canonical_bytes(content):
    return json.dumps(content, sort_keys=True, ensure_ascii=False, separators=(",", ":"),
                      allow_nan=False).encode("utf-8")


def content_digest(content):
    return "sha256:" + hashlib.sha256(canonical_bytes(content)).hexdigest()


def generated_at_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def export_document(content, generated_at, export_format_version):
    """The five-key top level around a finished, checked projection."""
    if export_format_version not in (JSON_FORMAT_VERSION, HTML_FORMAT_VERSION):
        raise ValueError("unknown export format version")
    return {"content": content, "content_digest": content_digest(content),
            "disclosure_schema_version": DISCLOSURE_SCHEMA_VERSION,
            "export_format_version": export_format_version,
            "generated_at": generated_at}


def serialize_json(document):
    return json.dumps(document, sort_keys=True, ensure_ascii=False, indent=2,
                      separators=(",", ": "), allow_nan=False) + "\n"
