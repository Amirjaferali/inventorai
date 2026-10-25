"""Electrical / Electronics - DC Resistive Load Power - Slice 1: the consumer.

Authority: docs/governance/ELECTRICAL_DC_RESISTIVE_LOAD_POWER_METHOD_CONTRACT.md
(§5 declarations, §6 numeric domain, numerical acceptance and display, §7
refusal layering and pre-owner order, §8 screen, §9 disclosure). ONE optional,
advisory, request-local evaluation of the theoretical electrical power that ONE
inventor-declared, steady-state DC resistive load absorbs at ONE declared
voltage, on an Electrical / Electronics-root project (eligibility is decided in
the web layer).

What this module owns
  * the method's governed artifact (method authority, declarations, screen,
    numeric domain, limitations, disclosure meaning, source and source-use
    records) and its fail-closed validation;
  * strict capture of the submitted form values (the ONLY place a string is
    turned into a number; the shared owner never parses), keeping the exact
    decimal values for the decimal reference;
  * the deterministic pre-owner order of §7 - completeness -> screen ->
    declarations -> numeric grammar -> positive resistance -> owner -> decimal
    reference; the FIRST failing stage alone decides the outcome;
  * the exact result's finite display (12 significant digits, round half to
    even, labelled exact or rounded);
  * the mapping of the shared owner's local state onto display reasons (§7):
    the owner state and token are preserved, never rewritten.

What it does not own: execution, unit validation and result packaging (the
shared owner, ``engine/deterministic_calculation.py``), the relation and its
binary64 acceptance (the method adapter,
``engine/dc_resistive_load_power_method.py``), authorization, eligibility and
rendering (the web layer). It never imports or loads another calculation
consumer or artifact, persists nothing, reads no project, session, store,
answer, component or SafetySignal, and has no network, provider, model, clock
or randomness dependency. Nothing here is a source, driver, wire, fuse or
component rating, a temperature or thermal result, a compatibility or
suitability result, a measurement or evidence. It imports no other
calculation consumer: its display rule is its own (calc/units §13F).
"""
import copy
import hashlib
import json
import math
import re
from fractions import Fraction
from pathlib import Path

from engine import deterministic_calculation as _dc

METHOD_ID = "electrical:dc_resistive_load_power"
METHOD_VERSION = "1.0"

ARTIFACT_ID = "electrical_dc_resistive_load_power"
ARTIFACT_SCHEMA_VERSION = "1.0"
ARTIFACT_PATH = (Path(__file__).resolve().parent.parent / "docs" / "governance"
                 / "electrical_content_config"
                 / "dc_resistive_load_power_v1.json")

# The trusted durable root domain that makes a project eligible (§1). Root
# only: no declared Stage 15 part grants this method.
ELIGIBLE_ROOT_DOMAIN = "electronics_electrical"

# §5 declarations D-1 to D-4, in contract order. Each one stays its own
# statement; any answer other than "applies" refuses MODEL_NOT_SUPPORTED.
DECLARATIONS = (
    ("steady_state_dc", "D-1"),
    ("resistive_load", "D-2"),
    ("declared_values", "D-3"),
    ("absorbed_power_convention", "D-4"),
)
DECLARATION_IDS = tuple(d for d, _ in DECLARATIONS)
_CONTRACT_REF = dict(DECLARATIONS)

# §8 six-item high-risk screen, in contract order.
SCREEN_ITEMS = ("mains_or_high_voltage", "battery_or_storage_cell",
                "fire_or_overheating", "medical_or_life_supporting",
                "vehicle_or_aerospace", "safety_function")

# Numeric roles the inventor enters, with their fixed units (§4). The units are
# shown, never chosen.
VALUE_ROLES = (("v_load", "V"), ("r_load", "Ω"))
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

# Representation limits of the strict decimal grammar (§6). They bound what can
# be typed; they are NOT physical limits or equipment ratings. A single leading
# minus is accepted on both fields: on v_load it is a signed voltage, on r_load
# it is read and then refused as a resistance that is not positive.
MAX_VALUE_CHARS = 64
V_INTEGER_DIGITS = 9
R_INTEGER_DIGITS = 12
FRACTION_DIGITS = 9
_VOLTAGE = re.compile(r"-?[0-9]{1,%d}(?:\.[0-9]{1,%d})?"
                      % (V_INTEGER_DIGITS, FRACTION_DIGITS), re.ASCII)
_RESISTANCE = re.compile(r"-?[0-9]{1,%d}(?:\.[0-9]{1,%d})?"
                         % (R_INTEGER_DIGITS, FRACTION_DIGITS), re.ASCII)

# The decimal-reference acceptance of a successful owner result (§6): the
# binary64 power must agree with the exact decimal result within this relative
# bound (the proven worst case is below 4.0000001 x 2**-53).
DECIMAL_REFERENCE_BOUND = Fraction(1, 2 ** 50)
# The finite display (§6): significant digits, round half to even.
DISPLAY_SIGNIFICANT_DIGITS = 12
# Plain decimal notation for 10**-6 <= P < 10**12; scientific otherwise.
_PLAIN_MIN_EXPONENT = -6
_PLAIN_MAX_EXPONENT = 11

# Outcomes (display reasons, §7). Not owner states.
OUTCOME_SUCCESS = "SUCCESS"
NOT_DECLARED = "NOT_DECLARED"
ENGINEERING_REVIEW_REQUIRED = "ENGINEERING_REVIEW_REQUIRED"
MODEL_NOT_SUPPORTED = "MODEL_NOT_SUPPORTED"
INVALID_NUMERIC_INPUT = "INVALID_NUMERIC_INPUT"
RESISTANCE_NOT_POSITIVE = "RESISTANCE_NOT_POSITIVE"
UNIT_NOT_SUPPORTED = "UNIT_NOT_SUPPORTED"
KNOWLEDGE_UNAVAILABLE = "KNOWLEDGE_UNAVAILABLE"
UNMAPPED_OWNER_OUTCOME = "UNMAPPED_OWNER_OUTCOME"
OUTCOMES = (OUTCOME_SUCCESS, NOT_DECLARED, ENGINEERING_REVIEW_REQUIRED,
            MODEL_NOT_SUPPORTED, INVALID_NUMERIC_INPUT, RESISTANCE_NOT_POSITIVE,
            UNIT_NOT_SUPPORTED, KNOWLEDGE_UNAVAILABLE, UNMAPPED_OWNER_OUTCOME)

# §7 correspondence: the shared-owner local state / token -> display reason.
OWNER_CORRESPONDENCE = {
    (_dc.STATE_REFUSAL, _dc.INVALID_NUMERIC_INPUT): INVALID_NUMERIC_INPUT,
    (_dc.STATE_REFUSAL, _dc.UNIT_NOT_ADMITTED): UNIT_NOT_SUPPORTED,
    (_dc.STATE_REFUSAL, _dc.UNKNOWN_UNIT): UNIT_NOT_SUPPORTED,
    (_dc.STATE_REFUSAL, _dc.METHOD_NOT_REGISTERED): KNOWLEDGE_UNAVAILABLE,
    (_dc.STATE_REFUSAL, _dc.VERSION_MISMATCH): KNOWLEDGE_UNAVAILABLE,
    (_dc.STATE_UNABLE, _dc.SOURCE_UNAVAILABLE): KNOWLEDGE_UNAVAILABLE,
    (_dc.STATE_FAILURE, _dc.EXECUTION_INTEGRITY_FAILURE): KNOWLEDGE_UNAVAILABLE,
}

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
_EXPECTED_ROLES = (("v_load", "voltage", "V"),
                   ("r_load", "electric_resistance", "Ω"),
                   ("p_load", "power", "W"))
_DISCLOSURE_ITEMS = 7
_SOURCE_POLICY = {"DOE-PWR-S1": "dcpower:SU001", "NIST-W-S1": "dcpower:SU002"}

# The accepted governed meaning of artifact version "1", pinned per section.
_SEMANTIC_DIGESTS = {
    "method": "f5f00e22cc8c700f5f3a4733b5b26d394f1e12b886af5d076d98d90ff5202b58",
    "numeric_domain": "24390853f93413ec24b8a01bb083c378e11758d5387150c948c3136a52efc917",
    "declarations": "292f84bd7bc4f133b981af4d3ba12310828f63d507cc4310499d73262a8f5d47",
    "screen_items": "7c71d7602291468b7c4442a892fdf64dfeff433d57109a68fa1abb72070dcde4",
    "limitations": "6b322b7058356c3ee172c7133137c32d0767f5db37ffcfa00e91b8397d6b2e2c",
    "disclosure": "b2d304eccaebf66aca5750df3ea86bf9d0794db6d3cfaf728d5a5ac2a79608cb",
    "sources": "08095a7380a86cfe20af9101bdc87daba8756a8380480a568704999cdd981f0e",
}
_PINNED_ARTIFACT_VERSION = "1"


def _section_digest(value):
    canonical = json.dumps(value, sort_keys=True, separators=(",", ":"),
                           ensure_ascii=True)
    return hashlib.sha256(canonical.encode("ascii")).hexdigest()


class DcPowerKnowledgeError(ValueError):
    """The governed artifact is missing, unreadable or not valid. The consumer
    turns this into ``KNOWLEDGE_UNAVAILABLE`` with no calculation. The message
    names structure only, never content."""


def is_eligible(root_domain):
    """True iff the trusted durable root domain makes a project eligible (§1).
    Pure; anything but the exact token is ineligible."""
    return isinstance(root_domain, str) and root_domain == ELIGIBLE_ROOT_DOMAIN


def _text(value, field):
    limit = _MAX_LONG_TEXT if field in _LONG_FIELDS else _MAX_TEXT
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise DcPowerKnowledgeError("%s: not a bounded non-empty string" % field)


def validate_artifact(data):
    """Validate the WHOLE governed artifact or raise ``DcPowerKnowledgeError``.
    Returns ``data``."""
    if not isinstance(data, dict) or set(data) != _TOP_KEYS:
        raise DcPowerKnowledgeError("artifact: unexpected or missing field")
    if data["artifact_id"] != ARTIFACT_ID \
            or data["schema_version"] != ARTIFACT_SCHEMA_VERSION:
        raise DcPowerKnowledgeError("artifact: unknown identity or version")
    for field in ("artifact_version", "owner", "slice", "governance_note"):
        _text(data[field], field)
    method = data["method"]
    if not isinstance(method, dict) or set(method) != _METHOD_KEYS:
        raise DcPowerKnowledgeError("method: unexpected or missing field")
    for field in _METHOD_KEYS:
        _text(method[field], field)
    if method["method_id"] != METHOD_ID or method["method_version"] != METHOD_VERSION:
        raise DcPowerKnowledgeError("method: unknown identity or version")
    domain = data["numeric_domain"]
    if not isinstance(domain, dict) or set(domain) != _DOMAIN_KEYS:
        raise DcPowerKnowledgeError("numeric_domain: unexpected or missing field")
    roles = domain["roles"]
    if not isinstance(roles, list) or len(roles) != len(_EXPECTED_ROLES):
        raise DcPowerKnowledgeError("numeric_domain: roles malformed")
    for entry, expected in zip(roles, _EXPECTED_ROLES):
        if not isinstance(entry, dict) or set(entry) != _ROLE_KEYS:
            raise DcPowerKnowledgeError("numeric_domain: role malformed")
        for field in _ROLE_KEYS:
            _text(entry[field], field)
        if (entry["role"], entry["quantity_kind"], entry["unit_token"]) != expected:
            raise DcPowerKnowledgeError("numeric_domain: role binding changed")
    if not isinstance(domain["rules"], list) or not domain["rules"]:
        raise DcPowerKnowledgeError("numeric_domain: rules missing")
    for rule in domain["rules"]:
        _text(rule, "rule")
    decls = data["declarations"]
    if not isinstance(decls, list) \
            or [d.get("declaration_id") if isinstance(d, dict) else None
                for d in decls] != list(DECLARATION_IDS):
        raise DcPowerKnowledgeError("declarations: not the §5 set")
    for entry in decls:
        if set(entry) != _DECL_KEYS:
            raise DcPowerKnowledgeError("declarations: unexpected or missing field")
        _text(entry["accepted_value"], "accepted_value")
        if entry["contract_ref"] != _CONTRACT_REF[entry["declaration_id"]] \
                or entry["refusal"] != MODEL_NOT_SUPPORTED:
            raise DcPowerKnowledgeError("declarations: refusal mapping changed")
    items = data["screen_items"]
    if not isinstance(items, list) \
            or [i.get("item_id") if isinstance(i, dict) else None
                for i in items] != list(SCREEN_ITEMS):
        raise DcPowerKnowledgeError("screen_items: not the §8 set")
    for entry in items:
        if set(entry) != _SCREEN_KEYS:
            raise DcPowerKnowledgeError("screen_items: unexpected or missing field")
        _text(entry["item"], "item")
    if not isinstance(data["limitations"], list) or not data["limitations"]:
        raise DcPowerKnowledgeError("limitations: missing")
    for entry in data["limitations"]:
        _text(entry, "limitation")
    disclosure = data["disclosure"]
    if not isinstance(disclosure, list) or len(disclosure) != _DISCLOSURE_ITEMS:
        raise DcPowerKnowledgeError("disclosure: not the seven §9 requirements")
    for entry in disclosure:
        _text(entry, "disclosure")
    sources = data["sources"]
    if not isinstance(sources, list) or not sources:
        raise DcPowerKnowledgeError("sources: missing")
    by_id = {}
    for record in sources:
        if not isinstance(record, dict):
            raise DcPowerKnowledgeError("sources: not an object")
        record_type = record.get("record_type")
        allowed = _SOURCE_KEYS | (_POLICY_EXTRA_KEYS
                                  if record_type == "source_use_policy"
                                  else frozenset())
        if set(record) != allowed:
            raise DcPowerKnowledgeError("sources: unexpected or missing field")
        if record_type not in ("source", "source_use_policy"):
            raise DcPowerKnowledgeError("sources: unknown record type")
        for field in allowed - {"record_type"}:
            _text(record[field], field)
        if not _ISO_DATE.fullmatch(record["inspection_date"]):
            raise DcPowerKnowledgeError("sources: inspection date malformed")
        if record["inspection_basis"] != "LEAD_SUPPLIED":
            raise DcPowerKnowledgeError("sources: unknown inspection basis")
        if record["record_id"] in by_id:
            raise DcPowerKnowledgeError("sources: duplicate record id")
        by_id[record["record_id"]] = record
    for source_id, policy_id in _SOURCE_POLICY.items():
        policy = by_id.get(policy_id)
        if policy is None or policy["record_type"] != "source_use_policy":
            raise DcPowerKnowledgeError("sources: source-use record missing")
        record = by_id.get(source_id)
        if record is None or record["record_type"] != "source" \
                or record["source_use_policy_ref"] != policy_id:
            raise DcPowerKnowledgeError("sources: source unresolved")
    if data["artifact_version"] != _PINNED_ARTIFACT_VERSION:
        raise DcPowerKnowledgeError("artifact: unpinned version")
    for section, expected in _SEMANTIC_DIGESTS.items():
        if _section_digest(data[section]) != expected:
            raise DcPowerKnowledgeError("%s: governed content changed" % section)
    return data


def load_artifact(path=None):
    """Read and validate the committed artifact. Any failure raises
    ``DcPowerKnowledgeError``. Reads one local file only."""
    target = Path(path) if path is not None else ARTIFACT_PATH
    try:
        with open(target, encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, ValueError):
        raise DcPowerKnowledgeError("artifact: unreadable") from None
    return validate_artifact(data)


def capture_form(form):
    """Strict capture of one submission, or ``None`` when MALFORMED: an unknown
    field, a field sent more than once, or a declaration / screen answer outside
    its closed choices. An absent or empty answer is unanswered (NOT_DECLARED).
    Returns ``{"declarations", "screen", "values"}`` of raw strings."""
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


def parse_value(text, role):
    """The ONE string-to-number step: the EXACT decimal value (a ``Fraction``)
    of a strict ASCII decimal within the role's representation limits (§6), or
    ``None``. Nothing is rounded."""
    pattern = {"v_load": _VOLTAGE, "r_load": _RESISTANCE}[role]
    if not isinstance(text, str) or len(text) > MAX_VALUE_CHARS \
            or not pattern.fullmatch(text):
        return None
    return Fraction(text)


def exact_power(v_load, r_load):
    """The exact rational value V**2 / R of the decimal reference (§6). Never
    shown unless a successful owner result agrees with it."""
    return v_load * v_load / r_load


def agrees_with_reference(value, reference):
    """The decimal-reference acceptance of §6: exactly zero when, and only
    when, the reference is zero; otherwise positive and within a relative
    error of at most ``DECIMAL_REFERENCE_BOUND``. A negative value, even a
    negative zero, never agrees."""
    if not isinstance(value, float) or not math.isfinite(value):
        return False
    if math.copysign(1.0, value) < 0:
        return False
    if reference == 0:
        return value == 0.0
    if not value > 0.0 or reference < 0:
        return False
    return abs(Fraction(value) - reference) <= reference * DECIMAL_REFERENCE_BOUND


def _exponent10(magnitude):
    """floor(log10(magnitude)) for a positive ``Fraction``, exactly."""
    exponent = len(str(magnitude.numerator)) - len(str(magnitude.denominator))
    while Fraction(10) ** exponent > magnitude:
        exponent -= 1
    while Fraction(10) ** (exponent + 1) <= magnitude:
        exponent += 1
    return exponent


def format_power(value):
    """The finite display of an exact ``Fraction`` (§6): ``(text, exact)``.

    Zero is ``("0", True)``. Otherwise the value is rounded once to
    ``DISPLAY_SIGNIFICANT_DIGITS`` significant digits, half to even; ``exact``
    is True only when that rounding changed nothing. Trailing zeros are
    dropped. Plain decimal notation is used for 10**-6 <= |value| < 10**12 and
    ``m × 10^e`` otherwise. A nonzero value never displays as zero."""
    if not isinstance(value, Fraction):
        raise TypeError("exact Fraction required")
    if value == 0:
        return "0", True
    sign = "-" if value < 0 else ""
    magnitude = abs(value)
    exponent = _exponent10(magnitude)
    shift = DISPLAY_SIGNIFICANT_DIGITS - 1 - exponent
    scaled = magnitude * Fraction(10) ** shift
    digits = round(scaled)                      # half to even on a Fraction
    if digits == 10 ** DISPLAY_SIGNIFICANT_DIGITS:
        exponent += 1
        shift -= 1
        digits = round(magnitude * Fraction(10) ** shift)
    exact = Fraction(digits, 1) / Fraction(10) ** shift == magnitude
    text = str(digits)                          # DISPLAY_SIGNIFICANT_DIGITS digits
    if _PLAIN_MIN_EXPONENT <= exponent <= _PLAIN_MAX_EXPONENT:
        if exponent >= 0:
            whole, fraction = text[:exponent + 1], text[exponent + 1:]
        else:
            whole, fraction = "0", "0" * (-exponent - 1) + text
        fraction = fraction.rstrip("0")
        body = whole + ("." + fraction if fraction else "")
    else:
        mantissa = text[0] + ("." + text[1:].rstrip("0") if text[1:].rstrip("0") else "")
        body = "%s × 10^%d" % (mantissa, exponent)
    return sign + body, exact


def _outcome(outcome, owner=None, result=None, display=None):
    return {
        "outcome": outcome,
        "owner_state": None if owner is None else owner.get("state"),
        "owner_reason": None if owner is None else owner.get("reason"),
        "result": result,
        "display_value": None if display is None else display["value"],
        "display_exact": None if display is None else display["exact"],
        "power": None if display is None else display["power"],
    }


def evaluate(captured, binding, artifact=None, owner_artifact_path=None):
    """Run the §7 order for ONE captured submission. Never raises.

    Request integrity, authorization, eligibility and malformed requests belong
    to the web layer and have already passed. Then, first failing stage alone
    wins: completeness -> high-risk screen -> declarations D-1 to D-4 -> numeric
    grammar -> positive resistance -> the shared owner -> the decimal-reference
    acceptance. No numerical payload accompanies any non-success outcome."""
    try:
        if artifact is None:
            load_artifact()
        else:
            validate_artifact(artifact)
    except DcPowerKnowledgeError:
        return _outcome(KNOWLEDGE_UNAVAILABLE)
    declarations = captured["declarations"]
    screen = captured["screen"]
    raw = captured["values"]
    if any(declarations[d] == "" for d in DECLARATION_IDS) \
            or any(screen[s] == "" for s in SCREEN_ITEMS):
        return _outcome(NOT_DECLARED)
    if any(screen[s] == SCREEN_YES for s in SCREEN_ITEMS):
        return _outcome(ENGINEERING_REVIEW_REQUIRED)
    if any(declarations[d] != ANSWER_APPLIES for d in DECLARATION_IDS):
        return _outcome(MODEL_NOT_SUPPORTED)
    values = {role: parse_value(raw[role], role) for role, _ in VALUE_ROLES}
    if any(v is None for v in values.values()):
        return _outcome(INVALID_NUMERIC_INPUT)
    if not values["r_load"] > 0:
        return _outcome(RESISTANCE_NOT_POSITIVE)
    request = {
        "method_id": METHOD_ID,
        "method_version": METHOD_VERSION,
        "inputs": {role: {"value": float(values[role]), "unit": _UNIT[role]}
                   for role, _ in VALUE_ROLES},
        "subject_ref": None,
    }
    owner = _dc.execute(binding, request, artifact_path=owner_artifact_path)
    if owner.get("state") != _dc.STATE_SUCCESS:
        mapped = OWNER_CORRESPONDENCE.get((owner.get("state"), owner.get("reason")))
        return _outcome(mapped or UNMAPPED_OWNER_OUTCOME, owner)
    reference = exact_power(values["v_load"], values["r_load"])
    try:
        accepted = agrees_with_reference(owner["outputs"]["p_load"]["value"], reference)
    except (KeyError, TypeError):
        accepted = False
    if not accepted:
        return _outcome(KNOWLEDGE_UNAVAILABLE, owner)
    text, exact = format_power(reference)
    return _outcome(OUTCOME_SUCCESS, owner, copy.deepcopy(owner),
                    {"value": text, "exact": exact, "power": reference})
