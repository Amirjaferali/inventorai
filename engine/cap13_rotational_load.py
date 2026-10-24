"""Stage 25 / CAP-13 - Linear Speed-Dependent Rotational Load - Slice 1: the CAP-13 rotational-load consumer.

Authority: docs/governance/STAGE25_CAP13_LINEAR_SPEED_DEPENDENT_ROTATIONAL_LOAD_METHOD_CONTRACT.md
(§5 declarations, §6 numeric domain and numerical acceptance, §7 refusal layering
and pre-owner order, §8 screen, §9 disclosure). ONE optional, advisory,
request-local evaluation of the signed torque that ONE inventor-declared
resisting load, proportional to shaft speed, applies at ONE shaft at ONE
operating speed, on a Mechanical-root project or for the ONE declared Mechanical
part of a valid durable integrated project (§1; eligibility is decided in the
web layer).

What this module owns
  * the method's governed artifact (method authority, declarations, screen,
    numeric domain, limitations, disclosure meaning, Modelica source and
    source-use records) and its fail-closed validation;
  * strict capture of the submitted form values (the ONLY place a string is
    turned into a number; the shared owner never parses);
  * the deterministic pre-owner order of §7 - completeness -> screen ->
    declarations -> numeric; the FIRST failing stage alone decides the outcome;
  * the mapping of the shared owner's local state onto display reasons (§7):
    the owner state and token are preserved, never rewritten.

What it does not own: execution, unit validation and result packaging (the
shared owner, ``engine/deterministic_calculation.py``), the equation and its
numerical acceptance (the method adapter,
``engine/cap13_rotational_load_method.py``), authorization, eligibility and
rendering (the web layer). It never imports or loads another CAP-13 or THERM-01
consumer or artifact, persists nothing, reads no project, session, store,
answer, requirement quantity or SafetySignal, and has no network, provider,
model, clock or randomness dependency. Nothing here is evidence, a dynamics,
motor-selection, suitability or safety statement.
"""
import copy
import hashlib
import json
import math
import re
from pathlib import Path

from engine import deterministic_calculation as _dc

METHOD_ID = "cap13:linear_speed_dependent_rotational_load"
METHOD_VERSION = "1.0"

ARTIFACT_ID = "cap13_linear_speed_dependent_rotational_load"
ARTIFACT_SCHEMA_VERSION = "1.0"
ARTIFACT_PATH = (Path(__file__).resolve().parent.parent / "docs" / "governance"
                 / "cap13_content_config"
                 / "linear_speed_dependent_rotational_load_v1.json")

# The trusted durable root domain that makes a project eligible (§1).
ELIGIBLE_ROOT_DOMAIN = "mechanical"

# §5 declarations D-1 to D-5, in contract order. Each one stays its own
# statement; any answer other than "applies" refuses MODEL_NOT_SUPPORTED.
DECLARATIONS = (
    ("linear_through_zero", "D-1"),
    ("nominal_point", "D-2"),
    ("single_axis", "D-3"),
    ("load_only", "D-4"),
    ("sign_convention", "D-5"),
)
DECLARATION_IDS = tuple(d for d, _ in DECLARATIONS)
_CONTRACT_REF = dict(DECLARATIONS)

# §8 nine-item high-risk screen, in contract order: the same items as the
# two-support reactions screen, so a CAP-13 inventor answers one familiar screen.
SCREEN_ITEMS = ("supports_people", "overhead_or_falling_hazard", "children",
                "safety_critical_load_path", "pressure", "high_temperature",
                "battery_containment", "medical_use", "food_contact")

# Numeric roles the inventor enters, with their fixed units (§4). The units are
# shown, never chosen. ``tau_nominal``, ``w_nominal`` and ``w`` are the ASCII
# identifiers of the roles τ_nominal, ω_nominal and ω.
VALUE_ROLES = (("tau_nominal", "N·m"), ("w_nominal", "rad/s"), ("w", "rad/s"))
# The roles typed with an optional single leading minus sign (§6).
SIGNED_ROLES = frozenset({"tau_nominal", "w"})
_UNIT = dict(VALUE_ROLES)

ANSWER_APPLIES = "applies"
ANSWER_DOES_NOT_APPLY = "does_not_apply"
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

# The NON-PHYSICAL text bound of §6 (abuse / resource protection only; never a
# range of valid torques or speeds).
MAX_VALUE_CHARS = 64

# Rotational-load outcomes (display reasons, §7). Not owner states.
OUTCOME_SUCCESS = "SUCCESS"
NOT_DECLARED = "NOT_DECLARED"
ENGINEERING_REVIEW_REQUIRED = "ENGINEERING_REVIEW_REQUIRED"
MODEL_NOT_SUPPORTED = "MODEL_NOT_SUPPORTED"
INVALID_NUMERIC_INPUT = "INVALID_NUMERIC_INPUT"
UNIT_NOT_SUPPORTED = "UNIT_NOT_SUPPORTED"
KNOWLEDGE_UNAVAILABLE = "KNOWLEDGE_UNAVAILABLE"
# Neutral fail-closed outcome for an owner state / token §7 does not map. It is
# NOT a reason token: no reason is invented and the owner state is preserved.
UNMAPPED_OWNER_OUTCOME = "UNMAPPED_OWNER_OUTCOME"
OUTCOMES = (OUTCOME_SUCCESS, NOT_DECLARED, ENGINEERING_REVIEW_REQUIRED,
            MODEL_NOT_SUPPORTED, INVALID_NUMERIC_INPUT, UNIT_NOT_SUPPORTED,
            KNOWLEDGE_UNAVAILABLE, UNMAPPED_OWNER_OUTCOME)

# §7 correspondence: the shared-owner local state / token -> rotational-load display.
OWNER_CORRESPONDENCE = {
    (_dc.STATE_REFUSAL, _dc.INVALID_NUMERIC_INPUT): INVALID_NUMERIC_INPUT,
    (_dc.STATE_REFUSAL, _dc.UNIT_NOT_ADMITTED): UNIT_NOT_SUPPORTED,
    (_dc.STATE_REFUSAL, _dc.UNKNOWN_UNIT): UNIT_NOT_SUPPORTED,
    (_dc.STATE_REFUSAL, _dc.METHOD_NOT_REGISTERED): KNOWLEDGE_UNAVAILABLE,
    (_dc.STATE_REFUSAL, _dc.VERSION_MISMATCH): KNOWLEDGE_UNAVAILABLE,
    (_dc.STATE_UNABLE, _dc.SOURCE_UNAVAILABLE): KNOWLEDGE_UNAVAILABLE,
    (_dc.STATE_FAILURE, _dc.EXECUTION_INTEGRITY_FAILURE): KNOWLEDGE_UNAVAILABLE,
}

# Strict v1 numeric grammar (§6): explicit ASCII digits with an optional single
# fractional part and, for the signed roles only, one leading minus sign; no plus
# sign, exponent, comma, underscore, space, hex, unit suffix, inf or nan. Nothing
# is normalized or case-folded first.
_UNSIGNED = re.compile(r"[0-9]+(?:\.[0-9]+)?", re.ASCII)
_SIGNED = re.compile(r"-?[0-9]+(?:\.[0-9]+)?", re.ASCII)

_MAX_TEXT = 1500
_MAX_LONG_TEXT = 2000
_LONG_FIELDS = frozenset({"governance_note", "inspected_content"})
_ISO_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
_TOP_KEYS = frozenset({
    "artifact_id", "schema_version", "artifact_version", "owner", "slice",
    "governance_note", "method", "numeric_domain", "declarations",
    "screen_items", "limitations", "disclosure", "sources"})
_METHOD_KEYS = frozenset({"method_id", "method_version", "contract", "model",
                          "executed_form", "derivation"})
_DOMAIN_KEYS = frozenset({"roles", "rules"})
_ROLE_KEYS = frozenset({"role", "meaning", "quantity_kind", "unit_token"})
_DECL_KEYS = frozenset({"declaration_id", "contract_ref", "accepted_value",
                        "refusal"})
_SCREEN_KEYS = frozenset({"item_id", "item"})
_SOURCE_KEYS = frozenset({
    "record_id", "record_type", "source_type", "publisher", "source_title",
    "url", "source_use_policy_ref", "inspection_basis", "inspection_date",
    "inspected_content", "paraphrase_only_limitation",
    "third_party_material_exclusion", "no_endorsement_limitation"})
_POLICY_EXTRA_KEYS = frozenset({"acknowledgement"})
_EXPECTED_ROLES = (("tau_nominal", "torque", "N·m"),
                   ("w_nominal", "angular_velocity", "rad/s"),
                   ("w", "angular_velocity", "rad/s"),
                   ("tau", "torque", "N·m"))
_DISCLOSURE_ITEMS = 7
# Each source record and the source-use record it must resolve to.
_SOURCE_POLICY = {"MODELICA-S1": "cap13r:SU001"}

# The accepted governed meaning of artifact version "1", pinned per section: the
# SHA-256 of each section's canonical JSON (sorted keys, compact, ASCII). Any
# semantic edit - a declaration or screen meaning, a numeric-domain rule, the
# executed form or derivation, a limitation, a disclosure item or a source
# record - fails closed even when every key and id survives. Changing them needs
# a new artifact version under its own authorization, not an edit here alone.
_SEMANTIC_DIGESTS = {
    "method": "68a4475d9a818875607d1bc01dd1825539c7a80eec74d7842d0ca7b6a2849eb0",
    "numeric_domain": "2ce4eb5af0c433d6ee683f8aa7cade28403911eb0feda97f4239fb2e28c9880c",
    "declarations": "0d44ecfb2f734c3e11aa80434674a486e367dbd8f15b5b82cfb32e875400ddb3",
    "screen_items": "9afd531ae5d2b462bf82545c32394d22dc3c584abbfb8a7da0626cf2b1a00504",
    "limitations": "691a1230ec3a813d00debd54b064a64078cc4c651a232e8334213da6855ab6c4",
    "disclosure": "ed666528cd28737fe9d8d337bc1cab2f1c901a197431d57800f4ff034a4be4f8",
    "sources": "382d2e83c5a6957c8748ee877f74e24b3deb4000684dedef01bda10ae3aafbd7",
}
_PINNED_ARTIFACT_VERSION = "1"


def _section_digest(value):
    canonical = json.dumps(value, sort_keys=True, separators=(",", ":"),
                           ensure_ascii=True)
    return hashlib.sha256(canonical.encode("ascii")).hexdigest()


class RotationalLoadKnowledgeError(ValueError):
    """The rotational-load governed artifact is missing, unreadable or not valid. The
    consumer turns this into ``KNOWLEDGE_UNAVAILABLE`` with no calculation. The
    message names structure only, never content."""


def is_eligible(root_domain):
    """True iff the trusted durable root domain makes a project eligible (§1).
    Pure; anything but the exact token is ineligible."""
    return isinstance(root_domain, str) and root_domain == ELIGIBLE_ROOT_DOMAIN


def _text(value, field):
    limit = _MAX_LONG_TEXT if field in _LONG_FIELDS else _MAX_TEXT
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise RotationalLoadKnowledgeError("%s: not a bounded non-empty string" % field)


def validate_artifact(data):
    """Validate the WHOLE rotational-load artifact or raise ``RotationalLoadKnowledgeError``.
    Exact keys, closed vocabularies, the method identity, the §5 / §8 sets and
    the seven §9 disclosure items exactly as the contract states them, and every
    source bound to its own source-use record. Returns ``data``."""
    if not isinstance(data, dict) or set(data) != _TOP_KEYS:
        raise RotationalLoadKnowledgeError("artifact: unexpected or missing field")
    if data["artifact_id"] != ARTIFACT_ID \
            or data["schema_version"] != ARTIFACT_SCHEMA_VERSION:
        raise RotationalLoadKnowledgeError("artifact: unknown identity or version")
    for field in ("artifact_version", "owner", "slice", "governance_note"):
        _text(data[field], field)
    method = data["method"]
    if not isinstance(method, dict) or set(method) != _METHOD_KEYS:
        raise RotationalLoadKnowledgeError("method: unexpected or missing field")
    for field in _METHOD_KEYS:
        _text(method[field], field)
    if method["method_id"] != METHOD_ID or method["method_version"] != METHOD_VERSION:
        raise RotationalLoadKnowledgeError("method: unknown identity or version")
    domain = data["numeric_domain"]
    if not isinstance(domain, dict) or set(domain) != _DOMAIN_KEYS:
        raise RotationalLoadKnowledgeError("numeric_domain: unexpected or missing field")
    roles = domain["roles"]
    if not isinstance(roles, list) or len(roles) != len(_EXPECTED_ROLES):
        raise RotationalLoadKnowledgeError("numeric_domain: roles malformed")
    for entry, expected in zip(roles, _EXPECTED_ROLES):
        if not isinstance(entry, dict) or set(entry) != _ROLE_KEYS:
            raise RotationalLoadKnowledgeError("numeric_domain: role malformed")
        for field in _ROLE_KEYS:
            _text(entry[field], field)
        if (entry["role"], entry["quantity_kind"], entry["unit_token"]) != expected:
            raise RotationalLoadKnowledgeError("numeric_domain: role binding changed")
    if not isinstance(domain["rules"], list) or not domain["rules"]:
        raise RotationalLoadKnowledgeError("numeric_domain: rules missing")
    for rule in domain["rules"]:
        _text(rule, "rule")
    decls = data["declarations"]
    if not isinstance(decls, list) \
            or [d.get("declaration_id") if isinstance(d, dict) else None
                for d in decls] != list(DECLARATION_IDS):
        raise RotationalLoadKnowledgeError("declarations: not the §5 set")
    for entry in decls:
        if set(entry) != _DECL_KEYS:
            raise RotationalLoadKnowledgeError("declarations: unexpected or missing field")
        _text(entry["accepted_value"], "accepted_value")
        if entry["contract_ref"] != _CONTRACT_REF[entry["declaration_id"]] \
                or entry["refusal"] != MODEL_NOT_SUPPORTED:
            raise RotationalLoadKnowledgeError("declarations: refusal mapping changed")
    items = data["screen_items"]
    if not isinstance(items, list) \
            or [i.get("item_id") if isinstance(i, dict) else None
                for i in items] != list(SCREEN_ITEMS):
        raise RotationalLoadKnowledgeError("screen_items: not the §8 set")
    for entry in items:
        if set(entry) != _SCREEN_KEYS:
            raise RotationalLoadKnowledgeError("screen_items: unexpected or missing field")
        _text(entry["item"], "item")
    if not isinstance(data["limitations"], list) or not data["limitations"]:
        raise RotationalLoadKnowledgeError("limitations: missing")
    for entry in data["limitations"]:
        _text(entry, "limitation")
    disclosure = data["disclosure"]
    if not isinstance(disclosure, list) or len(disclosure) != _DISCLOSURE_ITEMS:
        raise RotationalLoadKnowledgeError("disclosure: not the seven §9 requirements")
    for entry in disclosure:
        _text(entry, "disclosure")
    sources = data["sources"]
    if not isinstance(sources, list) or not sources:
        raise RotationalLoadKnowledgeError("sources: missing")
    by_id = {}
    for record in sources:
        if not isinstance(record, dict):
            raise RotationalLoadKnowledgeError("sources: not an object")
        record_type = record.get("record_type")
        allowed = _SOURCE_KEYS | (_POLICY_EXTRA_KEYS
                                  if record_type == "source_use_policy"
                                  else frozenset())
        if set(record) != allowed:
            raise RotationalLoadKnowledgeError("sources: unexpected or missing field")
        if record_type not in ("source", "source_use_policy"):
            raise RotationalLoadKnowledgeError("sources: unknown record type")
        for field in allowed - {"record_type"}:
            _text(record[field], field)
        if not _ISO_DATE.fullmatch(record["inspection_date"]):
            raise RotationalLoadKnowledgeError("sources: inspection date malformed")
        if record["inspection_basis"] != "LEAD_SUPPLIED":
            raise RotationalLoadKnowledgeError("sources: unknown inspection basis")
        if record["record_id"] in by_id:
            raise RotationalLoadKnowledgeError("sources: duplicate record id")
        by_id[record["record_id"]] = record
    for source_id, policy_id in _SOURCE_POLICY.items():
        policy = by_id.get(policy_id)
        if policy is None or policy["record_type"] != "source_use_policy":
            raise RotationalLoadKnowledgeError("sources: source-use record missing")
        record = by_id.get(source_id)
        if record is None or record["record_type"] != "source" \
                or record["source_use_policy_ref"] != policy_id:
            raise RotationalLoadKnowledgeError("sources: source unresolved")
    if data["artifact_version"] != _PINNED_ARTIFACT_VERSION:
        raise RotationalLoadKnowledgeError("artifact: unpinned version")
    for section, expected in _SEMANTIC_DIGESTS.items():
        if _section_digest(data[section]) != expected:
            raise RotationalLoadKnowledgeError("%s: governed content changed" % section)
    return data


def load_artifact(path=None):
    """Read and validate the committed rotational-load artifact. Any failure raises
    ``RotationalLoadKnowledgeError``. Reads one local file only."""
    target = Path(path) if path is not None else ARTIFACT_PATH
    try:
        with open(target, encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, ValueError):
        raise RotationalLoadKnowledgeError("artifact: unreadable") from None
    return validate_artifact(data)


def capture_form(form):
    """Strict capture of one submission.

    ``form`` is a mapping whose values are lists of strings (a request multi-dict
    flattened with ``getlist``). Returns ``None`` for a MALFORMED request: an
    unknown field, a field sent more than once, or a declaration / screen answer
    outside its closed choices. An absent or empty declaration or screen answer
    is NOT malformed; it is unanswered, which the evaluation reports as
    ``NOT_DECLARED``. Returns ``{"declarations", "screen", "values"}`` of raw
    strings otherwise.
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
        if answer not in ("", ANSWER_APPLIES, ANSWER_DOES_NOT_APPLY):
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


def parse_number(text, signed=False):
    """The ONE string-to-number step: ``float`` of a strict ASCII decimal of at
    most ``MAX_VALUE_CHARS`` characters - with one optional leading minus sign
    only when ``signed`` - or ``None`` when the spelling is not admitted,
    over-length or not finite. Signs are checked by the caller (§6)."""
    if not isinstance(text, str) or len(text) > MAX_VALUE_CHARS:
        return None
    if not (_SIGNED if signed else _UNSIGNED).fullmatch(text):
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
    """Run the §7 pre-owner order for ONE captured submission. Never raises.

    Request integrity, authorization, eligibility and malformed requests belong
    to the web layer and have already passed. Then, first failing stage alone
    wins: completeness (every declaration and screen item answered) -> high-risk
    screen -> declarations D-1 to D-5 -> numeric (finite, admitted grammar,
    tau_nominal < 0, w_nominal > 0, w signed, within the non-physical text
    bound) -> the shared owner. No stage after a
    failing one is evaluated, and no numerical payload accompanies any
    non-success outcome.
    """
    try:
        if artifact is None:
            load_artifact()
        else:
            validate_artifact(artifact)
    except RotationalLoadKnowledgeError:
        return _outcome(KNOWLEDGE_UNAVAILABLE)
    declarations = captured["declarations"]
    screen = captured["screen"]
    raw = captured["values"]

    # 1. completeness: every §5 declaration and §8 screen item answered.
    if any(declarations[d] == "" for d in DECLARATION_IDS) \
            or any(screen[s] == "" for s in SCREEN_ITEMS):
        return _outcome(NOT_DECLARED)
    # 2. high-risk screen: any YES abstains; the owner is not invoked.
    if any(screen[s] == SCREEN_YES for s in SCREEN_ITEMS):
        return _outcome(ENGINEERING_REVIEW_REQUIRED)
    # 3. declarations D-1 to D-5: any answer other than "applies" refuses.
    if any(declarations[d] != ANSWER_APPLIES for d in DECLARATION_IDS):
        return _outcome(MODEL_NOT_SUPPORTED)
    # 4. numeric: malformed, over-length, non-finite or wrong-signed. A zero
    # operating speed is valid; a zero or positive nominal torque and a zero or
    # negative nominal speed are refused here, never computed (§6).
    values = {role: parse_number(raw[role], signed=role in SIGNED_ROLES)
              for role, _ in VALUE_ROLES}
    if any(v is None for v in values.values()) \
            or not values["tau_nominal"] < 0.0 or not values["w_nominal"] > 0.0:
        return _outcome(INVALID_NUMERIC_INPUT)
    # 5. the shared owner, with typed values and the fixed §4 unit tokens only.
    request = {
        "method_id": METHOD_ID,
        "method_version": METHOD_VERSION,
        "inputs": {role: {"value": values[role], "unit": _UNIT[role]}
                   for role, _ in VALUE_ROLES},
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
