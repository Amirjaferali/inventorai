"""Sensors / Instrumentation C3 - TMP36 Nominal Voltage-to-Temperature - Slice 1: the consumer.

Authority: docs/governance/SENSORS_C3_TMP36_NOMINAL_VOLTAGE_TO_TEMPERATURE_METHOD_CONTRACT.md
(§5 declarations, §6 numeric domain and numerical acceptance, §7 refusal layering
and pre-owner order, §8 screen, §9 disclosure). ONE optional, advisory,
request-local nominal reading of ONE inventor-declared output voltage of ONE
Analog Devices TMP36 as a temperature on the Celsius scale, on an Electrical /
Electronics-root project or for the ONE declared Electrical / Electronics part
of a valid durable integrated project (§1; eligibility is decided in the web
layer).

What this module owns
  * the method's governed artifact (method authority, declarations, screen,
    numeric domain, limitations, disclosure meaning, data-sheet source and
    source-use records) and its fail-closed validation;
  * strict capture of the submitted form values (the ONLY place a string is
    turned into a number; the shared owner never parses), with the exact
    decimal value of the declared voltage kept for the nominal-interval check
    and the decimal reference;
  * the deterministic pre-owner order of §7 - completeness -> screen ->
    declarations -> numeric grammar -> nominal-model interval; the FIRST failing
    stage alone decides the outcome;
  * the decimal-reference acceptance of a successful owner result and its
    exact decimal display (§6);
  * the mapping of the shared owner's local state onto display reasons (§7):
    the owner state and token are preserved, never rewritten.

What it does not own: execution, unit validation and result packaging (the
shared owner, ``engine/deterministic_calculation.py``), the relation and its
binary64 acceptance (the method adapter,
``engine/tmp36_nominal_temperature_method.py``), authorization, eligibility and
rendering (the web layer). It never imports or loads another calculation
consumer or artifact, persists nothing, reads no project, session, store,
answer, requirement quantity or SafetySignal, and has no network, provider,
model, clock or randomness dependency. Nothing here is a measurement, evidence,
a sensor selection, an ADC, calibration, accuracy, compatibility or safety
statement.
"""
import copy
import hashlib
import json
import re
from fractions import Fraction
from pathlib import Path

from engine import deterministic_calculation as _dc

METHOD_ID = "tmp36:nominal_voltage_to_temperature"
METHOD_VERSION = "1.0"

ARTIFACT_ID = "tmp36_nominal_voltage_to_temperature"
ARTIFACT_SCHEMA_VERSION = "1.0"
ARTIFACT_PATH = (Path(__file__).resolve().parent.parent / "docs" / "governance"
                 / "tmp36_content_config"
                 / "nominal_voltage_to_temperature_v1.json")

# The trusted durable root domain that makes a project eligible (§1).
ELIGIBLE_ROOT_DOMAIN = "electronics_electrical"

# §5 declarations D-1 to D-4, in contract order. Each one stays its own
# statement; any answer other than "applies" refuses MODEL_NOT_SUPPORTED.
DECLARATIONS = (
    ("device_tmp36", "D-1"),
    ("declared_voltage", "D-2"),
    ("datasheet_conditions", "D-3"),
    ("nominal_only", "D-4"),
)
DECLARATION_IDS = tuple(d for d, _ in DECLARATIONS)
_CONTRACT_REF = dict(DECLARATIONS)

# §8 seven-item high-risk screen, in contract order: uses of a temperature
# reading where relying on a nominal value could put people or property at risk.
SCREEN_ITEMS = ("battery_or_storage_cell", "mains_or_high_voltage",
                "fire_or_ignition", "touch_skin_or_medical",
                "safety_critical_or_life_supporting", "aerospace_or_vehicle",
                "food_safety")

# The ONE numeric role the inventor enters, with its fixed unit (§4). The unit is
# shown, never chosen. ``v_out`` is the ASCII identifier of the role V_OUT.
VALUE_ROLES = (("v_out", "mV"),)
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
# range of valid voltages).
MAX_VALUE_CHARS = 64
# At most three digits after the decimal point (§6): a representation rule, so
# that every admitted value is a whole number of thousandths of a millivolt. It
# implies no measurement resolution or precision.
MAX_FRACTION_DIGITS = 3

# The nominal-model interval of the declared voltage, in mV, inclusive (§6):
# the nominal relation applied to the stated specified temperature range
# -40 °C to +125 °C. It is NOT the data sheet's electrical output-voltage
# specification and NOT a claim of device accuracy.
V_MIN_MV = Fraction(100)
V_MAX_MV = Fraction(1750)
_OFFSET_MV = Fraction(500)
_SCALE_MV_PER_C = Fraction(10)

# The decimal-reference acceptance of a successful owner result (§6): the
# binary64 temperature must agree with the exact decimal relation within this
# absolute bound in °C. The proven worst case for every admitted input is below
# 2**-46 * 1.3, so the bound is met with margin; it is far below the 0.0001 °C
# spacing of admitted results, so the exact decimal display is unambiguous.
DECIMAL_REFERENCE_BOUND = Fraction(1, 2 ** 45)
# Digits after the decimal point of the exact decimal display (§6).
DISPLAY_FRACTION_DIGITS = 4

# TMP36 outcomes (display reasons, §7). Not owner states.
OUTCOME_SUCCESS = "SUCCESS"
NOT_DECLARED = "NOT_DECLARED"
ENGINEERING_REVIEW_REQUIRED = "ENGINEERING_REVIEW_REQUIRED"
MODEL_NOT_SUPPORTED = "MODEL_NOT_SUPPORTED"
INVALID_NUMERIC_INPUT = "INVALID_NUMERIC_INPUT"
OUTSIDE_NOMINAL_MODEL_RANGE = "OUTSIDE_NOMINAL_MODEL_RANGE"
UNIT_NOT_SUPPORTED = "UNIT_NOT_SUPPORTED"
KNOWLEDGE_UNAVAILABLE = "KNOWLEDGE_UNAVAILABLE"
# Neutral fail-closed outcome for an owner state / token §7 does not map. It is
# NOT a reason token: no reason is invented and the owner state is preserved.
UNMAPPED_OWNER_OUTCOME = "UNMAPPED_OWNER_OUTCOME"
OUTCOMES = (OUTCOME_SUCCESS, NOT_DECLARED, ENGINEERING_REVIEW_REQUIRED,
            MODEL_NOT_SUPPORTED, INVALID_NUMERIC_INPUT,
            OUTSIDE_NOMINAL_MODEL_RANGE, UNIT_NOT_SUPPORTED,
            KNOWLEDGE_UNAVAILABLE, UNMAPPED_OWNER_OUTCOME)

# §7 correspondence: the shared-owner local state / token -> TMP36 display.
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
# fractional part of one to three digits; no sign, exponent, comma, underscore,
# space, hex, unit suffix, inf or nan. Nothing is normalized or case-folded first.
_MILLIVOLTS = re.compile(r"[0-9]+(?:\.[0-9]{1,%d})?" % MAX_FRACTION_DIGITS, re.ASCII)

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
_EXPECTED_ROLES = (("v_out", "voltage", "mV"),
                   ("t_celsius", "celsius_temperature", "°C"))
_DISCLOSURE_ITEMS = 7
# Each source record and the source-use record it must resolve to.
_SOURCE_POLICY = {"ADI-S1": "tmp36:SU001"}

# The accepted governed meaning of artifact version "1", pinned per section: the
# SHA-256 of each section's canonical JSON (sorted keys, compact, ASCII). Any
# semantic edit - a declaration or screen meaning, a numeric-domain rule, the
# executed form or derivation, a limitation, a disclosure item or a source
# record - fails closed even when every key and id survives. Changing them needs
# a new artifact version under its own authorization, not an edit here alone.
_SEMANTIC_DIGESTS = {
    "method": "be2bd1bfe9b6b62509226908c2f16213d9e3a6ffe3eaa2f360157d49e5710af0",
    "numeric_domain": "f63bad7a094ec423f7f5a02a9eea4d7f723596eb88da8a60fd456f550f3f29aa",
    "declarations": "498bf345e32d6af6d05f360fa488386b2115797fd1ddda09adbbceb932a7648b",
    "screen_items": "89ae6dd38f19834ce0935bd870ef3bd5afab5273d77f663e4ae8bf9bae6a7ad1",
    "limitations": "40eb336112fb57ddb13846b61846960873d4496f8d0b9a6f1a007796ff4903c0",
    "disclosure": "25260be75474f34bf8ebec02db633f9e8fdb110623a01ddb045d823d2a070193",
    "sources": "7ef1caf81ca882cdede2c6bc6d7ad970b1ddeb3490a7b9af61edc10988a4f7f4",
}
_PINNED_ARTIFACT_VERSION = "1"


def _section_digest(value):
    canonical = json.dumps(value, sort_keys=True, separators=(",", ":"),
                           ensure_ascii=True)
    return hashlib.sha256(canonical.encode("ascii")).hexdigest()


class Tmp36KnowledgeError(ValueError):
    """The TMP36 governed artifact is missing, unreadable or not valid. The
    consumer turns this into ``KNOWLEDGE_UNAVAILABLE`` with no calculation. The
    message names structure only, never content."""


def is_eligible(root_domain):
    """True iff the trusted durable root domain makes a project eligible (§1).
    Pure; anything but the exact token is ineligible."""
    return isinstance(root_domain, str) and root_domain == ELIGIBLE_ROOT_DOMAIN


def _text(value, field):
    limit = _MAX_LONG_TEXT if field in _LONG_FIELDS else _MAX_TEXT
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise Tmp36KnowledgeError("%s: not a bounded non-empty string" % field)


def validate_artifact(data):
    """Validate the WHOLE TMP36 artifact or raise ``Tmp36KnowledgeError``.
    Exact keys, closed vocabularies, the method identity, the §5 / §8 sets and
    the seven §9 disclosure items exactly as the contract states them, and every
    source bound to its own source-use record. Returns ``data``."""
    if not isinstance(data, dict) or set(data) != _TOP_KEYS:
        raise Tmp36KnowledgeError("artifact: unexpected or missing field")
    if data["artifact_id"] != ARTIFACT_ID \
            or data["schema_version"] != ARTIFACT_SCHEMA_VERSION:
        raise Tmp36KnowledgeError("artifact: unknown identity or version")
    for field in ("artifact_version", "owner", "slice", "governance_note"):
        _text(data[field], field)
    method = data["method"]
    if not isinstance(method, dict) or set(method) != _METHOD_KEYS:
        raise Tmp36KnowledgeError("method: unexpected or missing field")
    for field in _METHOD_KEYS:
        _text(method[field], field)
    if method["method_id"] != METHOD_ID or method["method_version"] != METHOD_VERSION:
        raise Tmp36KnowledgeError("method: unknown identity or version")
    domain = data["numeric_domain"]
    if not isinstance(domain, dict) or set(domain) != _DOMAIN_KEYS:
        raise Tmp36KnowledgeError("numeric_domain: unexpected or missing field")
    roles = domain["roles"]
    if not isinstance(roles, list) or len(roles) != len(_EXPECTED_ROLES):
        raise Tmp36KnowledgeError("numeric_domain: roles malformed")
    for entry, expected in zip(roles, _EXPECTED_ROLES):
        if not isinstance(entry, dict) or set(entry) != _ROLE_KEYS:
            raise Tmp36KnowledgeError("numeric_domain: role malformed")
        for field in _ROLE_KEYS:
            _text(entry[field], field)
        if (entry["role"], entry["quantity_kind"], entry["unit_token"]) != expected:
            raise Tmp36KnowledgeError("numeric_domain: role binding changed")
    if not isinstance(domain["rules"], list) or not domain["rules"]:
        raise Tmp36KnowledgeError("numeric_domain: rules missing")
    for rule in domain["rules"]:
        _text(rule, "rule")
    decls = data["declarations"]
    if not isinstance(decls, list) \
            or [d.get("declaration_id") if isinstance(d, dict) else None
                for d in decls] != list(DECLARATION_IDS):
        raise Tmp36KnowledgeError("declarations: not the §5 set")
    for entry in decls:
        if set(entry) != _DECL_KEYS:
            raise Tmp36KnowledgeError("declarations: unexpected or missing field")
        _text(entry["accepted_value"], "accepted_value")
        if entry["contract_ref"] != _CONTRACT_REF[entry["declaration_id"]] \
                or entry["refusal"] != MODEL_NOT_SUPPORTED:
            raise Tmp36KnowledgeError("declarations: refusal mapping changed")
    items = data["screen_items"]
    if not isinstance(items, list) \
            or [i.get("item_id") if isinstance(i, dict) else None
                for i in items] != list(SCREEN_ITEMS):
        raise Tmp36KnowledgeError("screen_items: not the §8 set")
    for entry in items:
        if set(entry) != _SCREEN_KEYS:
            raise Tmp36KnowledgeError("screen_items: unexpected or missing field")
        _text(entry["item"], "item")
    if not isinstance(data["limitations"], list) or not data["limitations"]:
        raise Tmp36KnowledgeError("limitations: missing")
    for entry in data["limitations"]:
        _text(entry, "limitation")
    disclosure = data["disclosure"]
    if not isinstance(disclosure, list) or len(disclosure) != _DISCLOSURE_ITEMS:
        raise Tmp36KnowledgeError("disclosure: not the seven §9 requirements")
    for entry in disclosure:
        _text(entry, "disclosure")
    sources = data["sources"]
    if not isinstance(sources, list) or not sources:
        raise Tmp36KnowledgeError("sources: missing")
    by_id = {}
    for record in sources:
        if not isinstance(record, dict):
            raise Tmp36KnowledgeError("sources: not an object")
        record_type = record.get("record_type")
        allowed = _SOURCE_KEYS | (_POLICY_EXTRA_KEYS
                                  if record_type == "source_use_policy"
                                  else frozenset())
        if set(record) != allowed:
            raise Tmp36KnowledgeError("sources: unexpected or missing field")
        if record_type not in ("source", "source_use_policy"):
            raise Tmp36KnowledgeError("sources: unknown record type")
        for field in allowed - {"record_type"}:
            _text(record[field], field)
        if not _ISO_DATE.fullmatch(record["inspection_date"]):
            raise Tmp36KnowledgeError("sources: inspection date malformed")
        if record["inspection_basis"] != "LEAD_SUPPLIED":
            raise Tmp36KnowledgeError("sources: unknown inspection basis")
        if record["record_id"] in by_id:
            raise Tmp36KnowledgeError("sources: duplicate record id")
        by_id[record["record_id"]] = record
    for source_id, policy_id in _SOURCE_POLICY.items():
        policy = by_id.get(policy_id)
        if policy is None or policy["record_type"] != "source_use_policy":
            raise Tmp36KnowledgeError("sources: source-use record missing")
        record = by_id.get(source_id)
        if record is None or record["record_type"] != "source" \
                or record["source_use_policy_ref"] != policy_id:
            raise Tmp36KnowledgeError("sources: source unresolved")
    if data["artifact_version"] != _PINNED_ARTIFACT_VERSION:
        raise Tmp36KnowledgeError("artifact: unpinned version")
    for section, expected in _SEMANTIC_DIGESTS.items():
        if _section_digest(data[section]) != expected:
            raise Tmp36KnowledgeError("%s: governed content changed" % section)
    return data


def load_artifact(path=None):
    """Read and validate the committed TMP36 artifact. Any failure raises
    ``Tmp36KnowledgeError``. Reads one local file only."""
    target = Path(path) if path is not None else ARTIFACT_PATH
    try:
        with open(target, encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, ValueError):
        raise Tmp36KnowledgeError("artifact: unreadable") from None
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


def parse_millivolts(text):
    """The ONE string-to-number step: the EXACT decimal value, as a
    ``Fraction``, of a strict unsigned ASCII decimal with at most three digits
    after the decimal point and at most ``MAX_VALUE_CHARS`` characters, or
    ``None`` when the spelling is not admitted or over-length. Nothing is
    rounded here; the nominal-model interval is checked by the caller (§6)."""
    if not isinstance(text, str) or len(text) > MAX_VALUE_CHARS:
        return None
    if not _MILLIVOLTS.fullmatch(text):
        return None
    return Fraction(text)


def within_nominal_interval(millivolts):
    """True iff the exact decimal voltage lies inside the nominal-model
    interval 100 mV to 1750 mV inclusive (§6), decided before any binary
    rounding."""
    return V_MIN_MV <= millivolts <= V_MAX_MV


def nominal_temperature(millivolts):
    """The exact decimal reference of the nominal relation (§3, §6):
    ``(V_OUT - 500) / 10`` as a ``Fraction``. Never shown unless a successful
    owner result agrees with it."""
    return (millivolts - _OFFSET_MV) / _SCALE_MV_PER_C


def agrees_with_reference(value, reference):
    """The decimal-reference acceptance of §6: the binary64 ``value`` is exactly
    zero when, and only when, the reference is zero; otherwise it has the
    reference's sign and lies within ``DECIMAL_REFERENCE_BOUND`` of it."""
    if not isinstance(value, float):
        return False
    if reference == 0:
        return value == 0.0
    if value == 0.0 or (value < 0.0) != (reference < 0):
        return False
    return abs(Fraction(value) - reference) <= DECIMAL_REFERENCE_BOUND


def format_reference(reference):
    """The exact decimal display of an accepted nominal temperature: every
    admitted input gives a whole number of ten-thousandths of a degree, shown
    with at least one and at most four digits after the decimal point and no
    rounding. It implies no measurement resolution, precision or accuracy."""
    scaled = reference * 10 ** DISPLAY_FRACTION_DIGITS
    if scaled.denominator != 1:
        raise ValueError("reference not a whole number of display units")
    magnitude = abs(scaled.numerator)
    whole, fraction = divmod(magnitude, 10 ** DISPLAY_FRACTION_DIGITS)
    digits = ("%0*d" % (DISPLAY_FRACTION_DIGITS, fraction)).rstrip("0") or "0"
    return "%s%d.%s" % ("-" if scaled.numerator < 0 else "", whole, digits)


def _outcome(outcome, owner=None, result=None, display_value=None,
             nominal_temperature=None):
    return {
        "outcome": outcome,
        "owner_state": None if owner is None else owner.get("state"),
        "owner_reason": None if owner is None else owner.get("reason"),
        "result": result,
        "display_value": display_value,
        # TEMPERATURE-TO-CONTROL-CONDITION-01: the EXACT decimal nominal
        # temperature (a ``Fraction``) this evaluation accepted, set on SUCCESS
        # only, so its one named composition consumer compares the accepted
        # value itself and never re-derives it or parses the display text.
        "nominal_temperature": nominal_temperature,
    }


def evaluate(captured, binding, artifact=None, owner_artifact_path=None):
    """Run the §7 pre-owner order for ONE captured submission. Never raises.

    Request integrity, authorization, eligibility and malformed requests belong
    to the web layer and have already passed. Then, first failing stage alone
    wins: completeness (every declaration and screen item answered) -> high-risk
    screen -> declarations D-1 to D-4 -> numeric grammar -> nominal-model
    interval (from the exact decimal value) -> the shared owner -> the
    decimal-reference acceptance. No stage after a failing one is evaluated,
    and no numerical payload accompanies any non-success outcome.
    """
    try:
        if artifact is None:
            load_artifact()
        else:
            validate_artifact(artifact)
    except Tmp36KnowledgeError:
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
    # 3. declarations D-1 to D-4: any answer other than "applies" refuses.
    if any(declarations[d] != ANSWER_APPLIES for d in DECLARATION_IDS):
        return _outcome(MODEL_NOT_SUPPORTED)
    # 4. numeric grammar: omitted, malformed or over-length text.
    millivolts = parse_millivolts(raw["v_out"])
    if millivolts is None:
        return _outcome(INVALID_NUMERIC_INPUT)
    # 5. nominal-model interval, from the exact decimal value before any binary
    # rounding: 100.001 is inside and 1750.001 outside, whatever binary64 does.
    if not within_nominal_interval(millivolts):
        return _outcome(OUTSIDE_NOMINAL_MODEL_RANGE)
    # 6. the shared owner, with the correctly rounded binary64 value and the
    # fixed §4 unit token only. The interval ends are exact in binary64, so an
    # admitted decimal stays inside the interval after rounding.
    request = {
        "method_id": METHOD_ID,
        "method_version": METHOD_VERSION,
        "inputs": {"v_out": {"value": float(millivolts), "unit": _UNIT["v_out"]}},
        "subject_ref": None,
    }
    owner = _dc.execute(binding, request, artifact_path=owner_artifact_path)
    if owner.get("state") != _dc.STATE_SUCCESS:
        mapped = OWNER_CORRESPONDENCE.get((owner.get("state"), owner.get("reason")))
        return _outcome(mapped or UNMAPPED_OWNER_OUTCOME, owner)
    # 7. decimal-reference acceptance: the owner's binary64 result must agree
    # with the exact decimal relation; otherwise fail closed with no number.
    reference = nominal_temperature(millivolts)
    try:
        produced = owner["outputs"]["t_celsius"]["value"]
        accepted = agrees_with_reference(produced, reference)
        display_value = format_reference(reference) if accepted else None
    except (KeyError, TypeError, ValueError):
        accepted, display_value = False, None
    if not accepted:
        return _outcome(KNOWLEDGE_UNAVAILABLE, owner)
    return _outcome(OUTCOME_SUCCESS, owner, copy.deepcopy(owner), display_value,
                    reference)
