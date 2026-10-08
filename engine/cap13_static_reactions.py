"""Stage 25 / CAP-13 - Two-Support Static Reactions - Slice 1: the CAP-13 consumer.

Authority: docs/governance/STAGE25_CAP13_TWO_SUPPORT_STATIC_REACTIONS_METHOD_CONTRACT.md
(§6 declarations, §7 numeric domain, §8 refusal layering, §9 screen, §12A journey
gate and evaluation order, §12B wording). ONE optional, advisory, request-local
calculation for ONE declared configuration on a Mechanical-root project.

What this module owns
  * the CAP-13-owned governed artifact (method authority, declarations, screen,
    numeric domain, limitations, disclosure meaning, NASA source and source-use
    records) and its fail-closed validation;
  * strict capture of the submitted form values (the ONLY place a string is
    turned into a number; the shared owner never parses);
  * the deterministic pre-owner evaluation order of §12A - the FIRST failing
    stage alone decides the outcome;
  * the mapping of the shared owner's local state onto CAP-13 display reasons
    (§8 Layer A / Layer B): the owner state and token are preserved, never
    rewritten.

What it does not own: execution, unit validation and result packaging (the
shared owner, ``engine/deterministic_calculation.py``), the equations (the
method adapter, ``engine/cap13_static_reactions_method.py``), authorization,
eligibility and rendering (the web layer). It persists nothing, reads no
project, session, store, answer, requirement quantity or SafetySignal, and has
no network, provider, model, clock or randomness dependency. Nothing here is
evidence, a specification or a capacity, adequacy or safety statement.
"""
import copy
import json
import math
import re
from pathlib import Path

from engine import deterministic_calculation as _dc

METHOD_ID = "cap13:static_reactions_two_support"
METHOD_VERSION = "1.0"

ARTIFACT_ID = "cap13_static_reactions_two_support"
ARTIFACT_SCHEMA_VERSION = "1.0"
ARTIFACT_PATH = (Path(__file__).resolve().parent.parent / "docs" / "governance"
                 / "cap13_content_config" / "static_reactions_two_support_v1.json")

# The trusted durable root domain that makes a project eligible (§12A).
ELIGIBLE_ROOT_DOMAIN = "mechanical"

# §6 declarations, in contract order, with their refusal group.
GROUP_LOAD = "load"
GROUP_SUPPORT = "support"
GROUP_CENTRE_OF_GRAVITY = "centre_of_gravity"
DECLARATIONS = (
    ("condition", GROUP_LOAD),
    ("applied_load", GROUP_LOAD),
    ("weight", GROUP_LOAD),
    ("support_count", GROUP_SUPPORT),
    ("support_geometry", GROUP_SUPPORT),
    ("support_action", GROUP_SUPPORT),
    ("support_direction", GROUP_SUPPORT),
    ("support_moment", GROUP_SUPPORT),
    ("load_paths", GROUP_SUPPORT),
    ("centre_of_gravity", GROUP_CENTRE_OF_GRAVITY),
)
DECLARATION_IDS = tuple(d for d, _ in DECLARATIONS)
_GROUP = dict(DECLARATIONS)

# §9 nine-item high-risk screen, in contract order.
SCREEN_ITEMS = ("supports_people", "overhead_or_falling_hazard", "children",
                "safety_critical_load_path", "pressure", "high_temperature",
                "battery_containment", "medical_use", "food_contact")

# Numeric roles the inventor enters, with their fixed units (§5). The units are
# shown, never chosen.
VALUE_ROLES = (("P", "N"), ("L", "mm"), ("x", "mm"))
_UNIT = dict(VALUE_ROLES)

ANSWER_MATCHES = "matches"
ANSWER_DIFFERS = "differs"
SCREEN_YES = "yes"
SCREEN_NO = "no"

DECLARATION_FIELD = "decl_%s"
SCREEN_FIELD = "screen_%s"
VALUE_FIELD = "value_%s"
FORM_FIELDS = frozenset(
    ["csrf_token"]
    + [DECLARATION_FIELD % d for d in DECLARATION_IDS]
    + [SCREEN_FIELD % s for s in SCREEN_ITEMS]
    + [VALUE_FIELD % r for r, _ in VALUE_ROLES])

# CAP-13 outcomes (Layer A display reasons, §8 / §12B B-4). Not owner states.
OUTCOME_SUCCESS = "SUCCESS"
NOT_DECLARED = "NOT_DECLARED"
ENGINEERING_REVIEW_REQUIRED = "ENGINEERING_REVIEW_REQUIRED"
LOAD_NOT_SUPPORTED = "LOAD_NOT_SUPPORTED"
SUPPORT_NOT_SUPPORTED = "SUPPORT_NOT_SUPPORTED"
INVALID_NUMERIC_INPUT = "INVALID_NUMERIC_INPUT"
CG_OUTSIDE_SUPPORT_SPAN = "CG_OUTSIDE_SUPPORT_SPAN"
UNIT_NOT_SUPPORTED = "UNIT_NOT_SUPPORTED"
KNOWLEDGE_UNAVAILABLE = "KNOWLEDGE_UNAVAILABLE"
# Neutral fail-closed outcome for an owner state / token §8 does not map. It is
# NOT a reason token: no reason is invented and the owner state is preserved.
UNMAPPED_OWNER_OUTCOME = "UNMAPPED_OWNER_OUTCOME"
OUTCOMES = (OUTCOME_SUCCESS, NOT_DECLARED, ENGINEERING_REVIEW_REQUIRED,
            LOAD_NOT_SUPPORTED, SUPPORT_NOT_SUPPORTED, INVALID_NUMERIC_INPUT,
            CG_OUTSIDE_SUPPORT_SPAN, UNIT_NOT_SUPPORTED, KNOWLEDGE_UNAVAILABLE,
            UNMAPPED_OWNER_OUTCOME)

# §8 correspondence: the shared-owner local state / token -> CAP-13 display.
OWNER_CORRESPONDENCE = {
    (_dc.STATE_REFUSAL, _dc.INVALID_NUMERIC_INPUT): INVALID_NUMERIC_INPUT,
    (_dc.STATE_REFUSAL, _dc.UNIT_NOT_ADMITTED): UNIT_NOT_SUPPORTED,
    (_dc.STATE_REFUSAL, _dc.UNKNOWN_UNIT): UNIT_NOT_SUPPORTED,
    (_dc.STATE_REFUSAL, _dc.METHOD_NOT_REGISTERED): KNOWLEDGE_UNAVAILABLE,
    (_dc.STATE_REFUSAL, _dc.VERSION_MISMATCH): KNOWLEDGE_UNAVAILABLE,
    (_dc.STATE_UNABLE, _dc.SOURCE_UNAVAILABLE): KNOWLEDGE_UNAVAILABLE,
    (_dc.STATE_FAILURE, _dc.EXECUTION_INTEGRITY_FAILURE): KNOWLEDGE_UNAVAILABLE,
}

# Strict v1 numeric grammar (explicit ASCII digits only; no Unicode digits, no
# sign except a leading "-" on x, no exponent, comma, underscore, space, hex,
# unit suffix, inf or nan). Nothing is normalized or case-folded first.
_UNSIGNED = re.compile(r"[0-9]+(?:\.[0-9]+)?", re.ASCII)
_SIGNED = re.compile(r"-?[0-9]+(?:\.[0-9]+)?", re.ASCII)

_MAX_TEXT = 1500
_MAX_LONG_TEXT = 2000
_LONG_FIELDS = frozenset({"governance_note", "disclosure", "inspected_content"})
_ISO_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
_TOP_KEYS = frozenset({
    "artifact_id", "schema_version", "artifact_version", "owner", "slice",
    "governance_note", "method", "numeric_domain", "declarations",
    "screen_items", "limitations", "disclosure", "sources"})
_METHOD_KEYS = frozenset({"method_id", "method_version", "contract", "model",
                          "executed_form", "derivation"})
_DOMAIN_KEYS = frozenset({"roles", "rules"})
_ROLE_KEYS = frozenset({"role", "meaning", "quantity_kind", "unit_token"})
_DECL_KEYS = frozenset({"declaration_id", "group", "accepted_value", "refusal"})
_SCREEN_KEYS = frozenset({"item_id", "item"})
_SOURCE_KEYS = frozenset({
    "record_id", "record_type", "source_type", "publisher", "source_title",
    "url", "source_use_policy_ref", "inspection_basis", "inspection_date",
    "inspected_content", "paraphrase_only_limitation",
    "third_party_material_exclusion", "no_endorsement_limitation"})
_POLICY_EXTRA_KEYS = frozenset({"acknowledgement"})
_EXPECTED_ROLES = (("P", "force", "N"), ("L", "length", "mm"),
                   ("x", "length", "mm"), ("R_L", "force", "N"),
                   ("R_R", "force", "N"))
_EXPECTED_REFUSAL = {GROUP_LOAD: LOAD_NOT_SUPPORTED,
                     GROUP_SUPPORT: SUPPORT_NOT_SUPPORTED,
                     GROUP_CENTRE_OF_GRAVITY: NOT_DECLARED}
_METHOD_SOURCES = ("NASA-S1", "NASA-S2")
_POLICY_ID = "cap13:SU001"


class Cap13KnowledgeError(ValueError):
    """The CAP-13 governed artifact is missing, unreadable or not valid. The
    consumer turns this into ``KNOWLEDGE_UNAVAILABLE`` with no calculation. The
    message names structure only, never content."""


def is_eligible(root_domain):
    """True iff the trusted durable root domain makes a project eligible (§12A).
    Pure; anything but the exact token is ineligible."""
    return isinstance(root_domain, str) and root_domain == ELIGIBLE_ROOT_DOMAIN


def _text(value, field):
    limit = _MAX_LONG_TEXT if field in _LONG_FIELDS else _MAX_TEXT
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise Cap13KnowledgeError("%s: not a bounded non-empty string" % field)


def validate_artifact(data):
    """Validate the WHOLE CAP-13 artifact or raise ``Cap13KnowledgeError``.
    Exact keys, closed vocabularies, the method identity and the §6 / §9 sets
    exactly as the contract states them, and every method source bound to the
    CAP-13 source-use record. Returns ``data``."""
    if not isinstance(data, dict) or set(data) != _TOP_KEYS:
        raise Cap13KnowledgeError("artifact: unexpected or missing field")
    if data["artifact_id"] != ARTIFACT_ID \
            or data["schema_version"] != ARTIFACT_SCHEMA_VERSION:
        raise Cap13KnowledgeError("artifact: unknown identity or version")
    for field in ("artifact_version", "owner", "slice", "governance_note",
                  "disclosure"):
        _text(data[field], field)
    method = data["method"]
    if not isinstance(method, dict) or set(method) != _METHOD_KEYS:
        raise Cap13KnowledgeError("method: unexpected or missing field")
    for field in _METHOD_KEYS:
        _text(method[field], field)
    if method["method_id"] != METHOD_ID or method["method_version"] != METHOD_VERSION:
        raise Cap13KnowledgeError("method: unknown identity or version")
    domain = data["numeric_domain"]
    if not isinstance(domain, dict) or set(domain) != _DOMAIN_KEYS:
        raise Cap13KnowledgeError("numeric_domain: unexpected or missing field")
    roles = domain["roles"]
    if not isinstance(roles, list) or len(roles) != len(_EXPECTED_ROLES):
        raise Cap13KnowledgeError("numeric_domain: roles malformed")
    for entry, expected in zip(roles, _EXPECTED_ROLES):
        if not isinstance(entry, dict) or set(entry) != _ROLE_KEYS:
            raise Cap13KnowledgeError("numeric_domain: role malformed")
        for field in _ROLE_KEYS:
            _text(entry[field], field)
        if (entry["role"], entry["quantity_kind"], entry["unit_token"]) != expected:
            raise Cap13KnowledgeError("numeric_domain: role binding changed")
    if not isinstance(domain["rules"], list) or not domain["rules"]:
        raise Cap13KnowledgeError("numeric_domain: rules missing")
    for rule in domain["rules"]:
        _text(rule, "rule")
    decls = data["declarations"]
    if not isinstance(decls, list) \
            or [d.get("declaration_id") if isinstance(d, dict) else None
                for d in decls] != list(DECLARATION_IDS):
        raise Cap13KnowledgeError("declarations: not the §6 set")
    for entry in decls:
        if set(entry) != _DECL_KEYS:
            raise Cap13KnowledgeError("declarations: unexpected or missing field")
        _text(entry["accepted_value"], "accepted_value")
        if entry["group"] != _GROUP[entry["declaration_id"]] \
                or entry["refusal"] != _EXPECTED_REFUSAL[entry["group"]]:
            raise Cap13KnowledgeError("declarations: refusal mapping changed")
    items = data["screen_items"]
    if not isinstance(items, list) \
            or [i.get("item_id") if isinstance(i, dict) else None
                for i in items] != list(SCREEN_ITEMS):
        raise Cap13KnowledgeError("screen_items: not the §9 set")
    for entry in items:
        if set(entry) != _SCREEN_KEYS:
            raise Cap13KnowledgeError("screen_items: unexpected or missing field")
        _text(entry["item"], "item")
    if not isinstance(data["limitations"], list) or not data["limitations"]:
        raise Cap13KnowledgeError("limitations: missing")
    for entry in data["limitations"]:
        _text(entry, "limitation")
    sources = data["sources"]
    if not isinstance(sources, list) or not sources:
        raise Cap13KnowledgeError("sources: missing")
    by_id = {}
    for record in sources:
        if not isinstance(record, dict):
            raise Cap13KnowledgeError("sources: not an object")
        record_type = record.get("record_type")
        allowed = _SOURCE_KEYS | (_POLICY_EXTRA_KEYS
                                  if record_type == "source_use_policy"
                                  else frozenset())
        if set(record) != allowed:
            raise Cap13KnowledgeError("sources: unexpected or missing field")
        if record_type not in ("source", "source_use_policy"):
            raise Cap13KnowledgeError("sources: unknown record type")
        for field in allowed - {"record_type"}:
            _text(record[field], field)
        if not _ISO_DATE.fullmatch(record["inspection_date"]):
            raise Cap13KnowledgeError("sources: inspection date malformed")
        if record["inspection_basis"] != "LEAD_SUPPLIED":
            raise Cap13KnowledgeError("sources: unknown inspection basis")
        if record["record_id"] in by_id:
            raise Cap13KnowledgeError("sources: duplicate record id")
        by_id[record["record_id"]] = record
    policy = by_id.get(_POLICY_ID)
    if policy is None or policy["record_type"] != "source_use_policy":
        raise Cap13KnowledgeError("sources: CAP-13 source-use record missing")
    for source_id in _METHOD_SOURCES:
        record = by_id.get(source_id)
        if record is None or record["record_type"] != "source" \
                or record["source_use_policy_ref"] != _POLICY_ID:
            raise Cap13KnowledgeError("sources: method source unresolved")
    return data


def load_artifact(path=None):
    """Read and validate the committed CAP-13 artifact. Any failure raises
    ``Cap13KnowledgeError``. Reads one local file only."""
    target = Path(path) if path is not None else ARTIFACT_PATH
    try:
        with open(target, encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, ValueError):
        raise Cap13KnowledgeError("artifact: unreadable") from None
    return validate_artifact(data)


def capture_form(form):
    """Strict capture of one submission.

    ``form`` is a mapping whose values are lists of strings (a request multi-dict
    flattened with ``getlist``). Returns ``None`` for a MALFORMED request: an
    unknown field, a field sent more than once, or a declaration / screen answer
    outside its closed choices. An absent or empty field is NOT malformed; it is
    unanswered, which the evaluation reports as ``NOT_DECLARED``.
    Returns ``{"declarations", "screen", "values"}`` of raw strings otherwise.
    """
    if not isinstance(form, dict):
        return None
    if set(form) - FORM_FIELDS:
        return None
    flat = {}
    for key, values in form.items():
        if not isinstance(values, list) or len(values) != 1 \
                or not isinstance(values[0], str):
            return None
        flat[key] = values[0]
    declarations = {}
    for decl in DECLARATION_IDS:
        answer = flat.get(DECLARATION_FIELD % decl, "")
        if answer not in ("", ANSWER_MATCHES, ANSWER_DIFFERS):
            return None
        declarations[decl] = answer
    screen = {}
    for item in SCREEN_ITEMS:
        answer = flat.get(SCREEN_FIELD % item, "")
        if answer not in ("", SCREEN_YES, SCREEN_NO):
            return None
        screen[item] = answer
    values = {role: flat.get(VALUE_FIELD % role, "") for role, _ in VALUE_ROLES}
    return {"declarations": declarations, "screen": screen, "values": values}


def parse_number(text, signed):
    """The ONE string-to-number step: ``float`` of a strict ASCII decimal, or
    ``None`` when the spelling is not admitted or the value is not finite."""
    if not isinstance(text, str):
        return None
    grammar = _SIGNED if signed else _UNSIGNED
    if not grammar.fullmatch(text):
        return None
    try:
        number = float(text)
    except (ValueError, OverflowError):
        return None
    return number if math.isfinite(number) else None


def _outcome(outcome, owner=None, result=None):
    return {
        "outcome": outcome,
        "owner_state": None if owner is None else owner.get("state"),
        "owner_reason": None if owner is None else owner.get("reason"),
        "result": result,
    }


def evaluate(captured, binding, artifact=None, owner_artifact_path=None):
    """Run the §12A evaluation order for ONE captured submission. Never raises.

    Stage 1 (request integrity, authorization, eligibility, malformed request)
    belongs to the web layer and has already passed. Then, first failing stage
    alone wins: completeness -> high-risk screen -> load declarations -> support
    declarations -> numeric type and positivity -> centre-of-gravity span ->
    the shared owner. No stage after a failing one is evaluated, and no
    numerical payload accompanies any non-success outcome.
    """
    try:
        if artifact is None:
            load_artifact()
        else:
            validate_artifact(artifact)
    except Cap13KnowledgeError:
        return _outcome(KNOWLEDGE_UNAVAILABLE)
    declarations = captured["declarations"]
    screen = captured["screen"]
    raw = captured["values"]

    # 2. completeness (and the centre-of-gravity declaration, whose §6 refusal is
    #    NOT_DECLARED).
    if any(declarations[d] == "" for d in DECLARATION_IDS) \
            or any(screen[s] == "" for s in SCREEN_ITEMS) \
            or any(raw[role] == "" for role, _ in VALUE_ROLES) \
            or declarations["centre_of_gravity"] != ANSWER_MATCHES:
        return _outcome(NOT_DECLARED)
    # 3. high-risk screen: any YES abstains; the owner is not invoked.
    if any(screen[s] == SCREEN_YES for s in SCREEN_ITEMS):
        return _outcome(ENGINEERING_REVIEW_REQUIRED)
    # 4. load declarations.
    if any(declarations[d] != ANSWER_MATCHES
           for d in DECLARATION_IDS if _GROUP[d] == GROUP_LOAD):
        return _outcome(LOAD_NOT_SUPPORTED)
    # 5. support declarations.
    if any(declarations[d] != ANSWER_MATCHES
           for d in DECLARATION_IDS if _GROUP[d] == GROUP_SUPPORT):
        return _outcome(SUPPORT_NOT_SUPPORTED)
    # 6. numeric type and positivity.
    p = parse_number(raw["P"], signed=False)
    length = parse_number(raw["L"], signed=False)
    x = parse_number(raw["x"], signed=True)
    if p is None or length is None or x is None or p <= 0.0 or length <= 0.0:
        return _outcome(INVALID_NUMERIC_INPUT)
    # 7. centre-of-gravity span.
    if x < 0.0 or x > length:
        return _outcome(CG_OUTSIDE_SUPPORT_SPAN)
    # "-0" spells the left support position; carry it as +0.0 so no displayed
    # reaction ever reads as a signed zero. Arithmetic identity only.
    if x == 0.0:
        x = 0.0
    # 8. the shared owner, with typed values and the fixed §5 unit tokens only.
    request = {
        "method_id": METHOD_ID,
        "method_version": METHOD_VERSION,
        "inputs": {"P": {"value": p, "unit": _UNIT["P"]},
                   "L": {"value": length, "unit": _UNIT["L"]},
                   "x": {"value": x, "unit": _UNIT["x"]}},
        "subject_ref": None,
    }
    owner = _dc.execute(binding, request, artifact_path=owner_artifact_path)
    if owner.get("state") == _dc.STATE_SUCCESS:
        return _outcome(OUTCOME_SUCCESS, owner, copy.deepcopy(owner))
    mapped = OWNER_CORRESPONDENCE.get((owner.get("state"), owner.get("reason")))
    return _outcome(mapped or UNMAPPED_OWNER_OUTCOME, owner)


def format_value(value):
    """The deterministic display of a produced value: Python's shortest
    round-trip ``repr`` of the binary64 result. No rounding, precision or
    significant-figure policy is applied or implied."""
    return repr(float(value))
