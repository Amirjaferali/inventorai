"""Electrical / Electronics - PWM Average Voltage - Slice 1: the consumer.

Authority: docs/governance/ELECTRICAL_PWM_AVERAGE_VOLTAGE_METHOD_CONTRACT.md
(§5 declarations, §6 numeric domain, numerical acceptance and display, §7
refusal layering and pre-owner order, §8 screen, §9 disclosure). ONE optional,
advisory, request-local evaluation of the arithmetic time-average, over one
period, of ONE inventor-declared ideal two-level voltage waveform (the declared
supply level during the on-interval, zero for the rest of the period),
V_avg = V_supply x t_on / T in volts, on an Electrical / Electronics-root
project or for the declared Electrical / Electronics part of a valid durable
integrated composition (eligibility is decided in the web layer).

What this module owns
  * the method's governed artifact (method authority, declarations, screen,
    numeric domain, limitations, disclosure meaning, source and source-use
    records) and its fail-closed validation;
  * strict capture of the submitted form values (the ONLY place a string is
    turned into a number; the shared owner never parses), keeping the exact
    decimal values for the decimal reference;
  * the deterministic pre-owner order of §7 - completeness -> screen ->
    declarations -> numeric grammar -> supply level not negative -> period
    positive -> on-time not negative -> on-time not above the period -> owner
    -> decimal reference; the FIRST failing stage alone decides the outcome;
  * the exact result's finite display (12 significant digits, round half to
    even, labelled exact or rounded);
  * the mapping of the shared owner's local state onto display reasons (§7):
    the owner state and token are preserved, never rewritten.

What it does not own: execution, unit validation and result packaging (the
shared owner, ``engine/deterministic_calculation.py``), the relation and its
binary64 acceptance (the method adapter, ``engine/pwm_average_voltage_method.py``),
authorization, eligibility and rendering (the web layer). It never imports or
loads another calculation consumer or artifact, persists nothing, reads no
project, session, store, answer, component or SafetySignal, and has no
network, provider, model, clock or randomness dependency. Nothing here is an
equivalent steady DC voltage, a load response, a motor speed, a torque, a
current, an average power, an RMS value, a ripple, a filtered output, a
switching-frequency or time-constant statement, a measurement or evidence; no
unit is converted (V and s only) and no duty-cycle quantity exists outside the
product. It imports no other calculation consumer: its display rule is its own
(calc/units §13J).
"""
import copy
import hashlib
import json
import math
import re
from fractions import Fraction
from pathlib import Path

from engine import deterministic_calculation as _dc

METHOD_ID = "electrical:pwm_average_voltage"
METHOD_VERSION = "1.0"

ARTIFACT_ID = "electrical_pwm_average_voltage"
ARTIFACT_SCHEMA_VERSION = "1.0"
ARTIFACT_PATH = (Path(__file__).resolve().parent.parent / "docs" / "governance"
                 / "electrical_content_config" / "pwm_average_voltage_v1.json")

# The trusted durable root domain that makes a project eligible (§1), and the
# domain of the declared Stage 15 part the web-layer gate may offer it for.
ELIGIBLE_ROOT_DOMAIN = "electronics_electrical"

# §5 declarations D-1 to D-4, in contract order. Each one stays its own
# statement; any answer other than "applies" refuses MODEL_NOT_SUPPORTED.
DECLARATIONS = (
    ("ideal_two_level_waveform", "D-1"),
    ("fixed_period_and_on_time", "D-2"),
    ("declared_values", "D-3"),
    ("waveform_average_wanted", "D-4"),
)
DECLARATION_IDS = tuple(d for d, _ in DECLARATIONS)
_CONTRACT_REF = dict(DECLARATIONS)

# §8 six-item high-risk screen, in contract order (the DC load screen).
SCREEN_ITEMS = ("mains_or_high_voltage", "battery_or_storage_cell",
                "fire_or_overheating", "medical_or_life_supporting",
                "vehicle_or_aerospace", "safety_function")

# Numeric roles the inventor enters, with their fixed units (§4). The units are
# shown, never chosen; nothing is converted.
VALUE_ROLES = (("v_supply", "V"), ("t_on", "s"), ("t_period", "s"))
_UNIT = dict(VALUE_ROLES)
OUTPUT_ROLE = "v_avg"
OUTPUT_UNIT = "V"

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
# minus is accepted on every field so that a negative value is read and then
# refused with its own reason; an exact zero, "-0" included, is a zero value.
MAX_VALUE_CHARS = 64
INTEGER_DIGITS = 9
FRACTION_DIGITS = 9
_NUMBER = re.compile(r"-?[0-9]{1,%d}(?:\.[0-9]{1,%d})?"
                     % (INTEGER_DIGITS, FRACTION_DIGITS), re.ASCII)

# The decimal-reference acceptance of a successful owner result (§6): the
# binary64 average must agree with the exact decimal value within this
# relative bound (the proven worst case is below 4.0000001 x 2**-53).
DECIMAL_REFERENCE_BOUND = Fraction(1, 2 ** 50)
# The finite display (§6): significant digits, round half to even.
DISPLAY_SIGNIFICANT_DIGITS = 12
# Plain decimal notation for 10**-6 <= V < 10**12; scientific otherwise.
_PLAIN_MIN_EXPONENT = -6
_PLAIN_MAX_EXPONENT = 11

# Outcomes (display reasons, §7). Not owner states.
OUTCOME_SUCCESS = "SUCCESS"
NOT_DECLARED = "NOT_DECLARED"
ENGINEERING_REVIEW_REQUIRED = "ENGINEERING_REVIEW_REQUIRED"
MODEL_NOT_SUPPORTED = "MODEL_NOT_SUPPORTED"
INVALID_NUMERIC_INPUT = "INVALID_NUMERIC_INPUT"
VOLTAGE_NEGATIVE = "VOLTAGE_NEGATIVE"
PERIOD_NOT_POSITIVE = "PERIOD_NOT_POSITIVE"
ON_TIME_NEGATIVE = "ON_TIME_NEGATIVE"
ON_TIME_EXCEEDS_PERIOD = "ON_TIME_EXCEEDS_PERIOD"
UNIT_NOT_SUPPORTED = "UNIT_NOT_SUPPORTED"
KNOWLEDGE_UNAVAILABLE = "KNOWLEDGE_UNAVAILABLE"
UNMAPPED_OWNER_OUTCOME = "UNMAPPED_OWNER_OUTCOME"
OUTCOMES = (OUTCOME_SUCCESS, NOT_DECLARED, ENGINEERING_REVIEW_REQUIRED,
            MODEL_NOT_SUPPORTED, INVALID_NUMERIC_INPUT, VOLTAGE_NEGATIVE,
            PERIOD_NOT_POSITIVE, ON_TIME_NEGATIVE, ON_TIME_EXCEEDS_PERIOD,
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
_EXPECTED_ROLES = (("v_supply", "voltage", "V"),
                   ("t_on", "time", "s"),
                   ("t_period", "time", "s"),
                   ("v_avg", "voltage", "V"))
_DISCLOSURE_ITEMS = 7
_SOURCE_POLICY = {"NASA-PWM-S1": "pwm:SU001", "NASA-PWM-S2": "pwm:SU001"}

# The accepted governed meaning of artifact version "1", pinned per section.
_SEMANTIC_DIGESTS = {
    "method": "8db54ef95057053666fe3127bcad58c14139df98c8feaecbd3b9aaa90d6fcdd7",
    "numeric_domain": "0e3e048a4196dd46001d15ef2ad99ad44be278737f245a6e08984d4fda21e3f7",
    "declarations": "2c8ca6e9ecd2854b66b2011d0ccd498b0a887337af074b77ac07405969a6de76",
    "screen_items": "7c71d7602291468b7c4442a892fdf64dfeff433d57109a68fa1abb72070dcde4",
    "limitations": "10edbf9822016db79e8ded075dd6a414cb07d0b322c72a272d485455af546f4c",
    "disclosure": "f1d99f4e50b0c6e12133964d14de72e16ca968ed0050422fcfeed2f0dea9e862",
    "sources": "d0a675566bd1a4e2831f974580915a297d3ca27859594104c4ac3f297d1268ea",
}
_PINNED_ARTIFACT_VERSION = "1"


def _section_digest(value):
    canonical = json.dumps(value, sort_keys=True, separators=(",", ":"),
                           ensure_ascii=True)
    return hashlib.sha256(canonical.encode("ascii")).hexdigest()


class PwmKnowledgeError(ValueError):
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
        raise PwmKnowledgeError("%s: not a bounded non-empty string" % field)


def validate_artifact(data):
    """Validate the WHOLE governed artifact or raise ``PwmKnowledgeError``.
    Returns ``data``."""
    if not isinstance(data, dict) or set(data) != _TOP_KEYS:
        raise PwmKnowledgeError("artifact: unexpected or missing field")
    if data["artifact_id"] != ARTIFACT_ID \
            or data["schema_version"] != ARTIFACT_SCHEMA_VERSION:
        raise PwmKnowledgeError("artifact: unknown identity or version")
    for field in ("artifact_version", "owner", "slice", "governance_note"):
        _text(data[field], field)
    method = data["method"]
    if not isinstance(method, dict) or set(method) != _METHOD_KEYS:
        raise PwmKnowledgeError("method: unexpected or missing field")
    for field in _METHOD_KEYS:
        _text(method[field], field)
    if method["method_id"] != METHOD_ID or method["method_version"] != METHOD_VERSION:
        raise PwmKnowledgeError("method: unknown identity or version")
    domain = data["numeric_domain"]
    if not isinstance(domain, dict) or set(domain) != _DOMAIN_KEYS:
        raise PwmKnowledgeError("numeric_domain: unexpected or missing field")
    roles = domain["roles"]
    if not isinstance(roles, list) or len(roles) != len(_EXPECTED_ROLES):
        raise PwmKnowledgeError("numeric_domain: roles malformed")
    for entry, expected in zip(roles, _EXPECTED_ROLES):
        if not isinstance(entry, dict) or set(entry) != _ROLE_KEYS:
            raise PwmKnowledgeError("numeric_domain: role malformed")
        for field in _ROLE_KEYS:
            _text(entry[field], field)
        if (entry["role"], entry["quantity_kind"], entry["unit_token"]) != expected:
            raise PwmKnowledgeError("numeric_domain: role binding changed")
    if not isinstance(domain["rules"], list) or not domain["rules"]:
        raise PwmKnowledgeError("numeric_domain: rules missing")
    for rule in domain["rules"]:
        _text(rule, "rule")
    decls = data["declarations"]
    if not isinstance(decls, list) \
            or [d.get("declaration_id") if isinstance(d, dict) else None
                for d in decls] != list(DECLARATION_IDS):
        raise PwmKnowledgeError("declarations: not the §5 set")
    for entry in decls:
        if set(entry) != _DECL_KEYS:
            raise PwmKnowledgeError("declarations: unexpected or missing field")
        _text(entry["accepted_value"], "accepted_value")
        if entry["contract_ref"] != _CONTRACT_REF[entry["declaration_id"]] \
                or entry["refusal"] != MODEL_NOT_SUPPORTED:
            raise PwmKnowledgeError("declarations: refusal mapping changed")
    items = data["screen_items"]
    if not isinstance(items, list) \
            or [i.get("item_id") if isinstance(i, dict) else None
                for i in items] != list(SCREEN_ITEMS):
        raise PwmKnowledgeError("screen_items: not the §8 set")
    for entry in items:
        if set(entry) != _SCREEN_KEYS:
            raise PwmKnowledgeError("screen_items: unexpected or missing field")
        _text(entry["item"], "item")
    if not isinstance(data["limitations"], list) or not data["limitations"]:
        raise PwmKnowledgeError("limitations: missing")
    for entry in data["limitations"]:
        _text(entry, "limitation")
    disclosure = data["disclosure"]
    if not isinstance(disclosure, list) or len(disclosure) != _DISCLOSURE_ITEMS:
        raise PwmKnowledgeError("disclosure: not the seven §9 requirements")
    for entry in disclosure:
        _text(entry, "disclosure")
    sources = data["sources"]
    if not isinstance(sources, list) or not sources:
        raise PwmKnowledgeError("sources: missing")
    by_id = {}
    for record in sources:
        if not isinstance(record, dict):
            raise PwmKnowledgeError("sources: not an object")
        record_type = record.get("record_type")
        allowed = _SOURCE_KEYS | (_POLICY_EXTRA_KEYS
                                  if record_type == "source_use_policy"
                                  else frozenset())
        if set(record) != allowed:
            raise PwmKnowledgeError("sources: unexpected or missing field")
        if record_type not in ("source", "source_use_policy"):
            raise PwmKnowledgeError("sources: unknown record type")
        for field in allowed - {"record_type"}:
            _text(record[field], field)
        if not _ISO_DATE.fullmatch(record["inspection_date"]):
            raise PwmKnowledgeError("sources: inspection date malformed")
        if record["inspection_basis"] != "LEAD_SUPPLIED":
            raise PwmKnowledgeError("sources: unknown inspection basis")
        if record["record_id"] in by_id:
            raise PwmKnowledgeError("sources: duplicate record id")
        by_id[record["record_id"]] = record
    for source_id, policy_id in _SOURCE_POLICY.items():
        policy = by_id.get(policy_id)
        if policy is None or policy["record_type"] != "source_use_policy":
            raise PwmKnowledgeError("sources: source-use record missing")
        record = by_id.get(source_id)
        if record is None or record["record_type"] != "source" \
                or record["source_use_policy_ref"] != policy_id:
            raise PwmKnowledgeError("sources: source unresolved")
    if data["artifact_version"] != _PINNED_ARTIFACT_VERSION:
        raise PwmKnowledgeError("artifact: unpinned version")
    for section, expected in _SEMANTIC_DIGESTS.items():
        if _section_digest(data[section]) != expected:
            raise PwmKnowledgeError("%s: governed content changed" % section)
    return data


def load_artifact(path=None):
    """Read and validate the committed artifact. Any failure raises
    ``PwmKnowledgeError``. Reads one local file only."""
    target = Path(path) if path is not None else ARTIFACT_PATH
    try:
        with open(target, encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, ValueError):
        raise PwmKnowledgeError("artifact: unreadable") from None
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
    if role not in _UNIT:
        raise KeyError(role)
    if not isinstance(text, str) or len(text) > MAX_VALUE_CHARS \
            or not _NUMBER.fullmatch(text):
        return None
    return Fraction(text)


def exact_average(v_supply, t_on, t_period):
    """The exact rational value V_supply x t_on / T of the decimal reference
    (§6). Never shown unless a successful owner result agrees with it."""
    return v_supply * t_on / t_period


def agrees_with_reference(value, reference, supply):
    """The decimal-reference acceptance of §6: exactly zero when, and only
    when, the reference is zero; otherwise positive, not above the binary64
    ``supply`` and within a relative error of at most
    ``DECIMAL_REFERENCE_BOUND``. A negative value, even a negative zero, never
    agrees."""
    if not isinstance(value, float) or not math.isfinite(value):
        return False
    if math.copysign(1.0, value) < 0:
        return False
    if reference == 0:
        return value == 0.0
    if not value > 0.0 or reference < 0:
        return False
    if isinstance(supply, float) and value > supply:
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


def format_average(value):
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
        "average": None if display is None else display["average"],
    }


def evaluate(captured, binding, artifact=None, owner_artifact_path=None):
    """Run the §7 order for ONE captured submission. Never raises.

    Request integrity, authorization, eligibility and malformed requests belong
    to the web layer and have already passed. Then, first failing stage alone
    wins: completeness -> high-risk screen -> declarations D-1 to D-4 -> numeric
    grammar -> supply level not negative -> period positive -> on-time not
    negative -> on-time not above the period -> the shared owner -> the
    decimal-reference acceptance. No numerical payload accompanies any
    non-success outcome."""
    try:
        if artifact is None:
            load_artifact()
        else:
            validate_artifact(artifact)
    except PwmKnowledgeError:
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
    if values["v_supply"] < 0:
        return _outcome(VOLTAGE_NEGATIVE)
    if not values["t_period"] > 0:
        return _outcome(PERIOD_NOT_POSITIVE)
    if values["t_on"] < 0:
        return _outcome(ON_TIME_NEGATIVE)
    if values["t_on"] > values["t_period"]:
        return _outcome(ON_TIME_EXCEEDS_PERIOD)
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
    reference = exact_average(values["v_supply"], values["t_on"], values["t_period"])
    try:
        output = owner["outputs"][OUTPUT_ROLE]
        # The owner's echoed output token must be the method's own V (§4); a
        # same-kind token such as mV is admitted by the owner but not here.
        accepted = output["unit"] == OUTPUT_UNIT and agrees_with_reference(
            output["value"], reference, float(values["v_supply"]))
    except (KeyError, TypeError):
        accepted = False
    if not accepted:
        return _outcome(KNOWLEDGE_UNAVAILABLE, owner)
    text, exact = format_average(reference)
    return _outcome(OUTCOME_SUCCESS, owner, copy.deepcopy(owner),
                    {"value": text, "exact": exact, "average": reference})
