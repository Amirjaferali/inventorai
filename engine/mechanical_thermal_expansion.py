"""Mechanical - Free Linear Thermal Expansion - Slice 1: the consumer.

Authority: docs/governance/MECHANICAL_FREE_LINEAR_THERMAL_EXPANSION_METHOD_CONTRACT.md
(§5 declarations, §6 numeric domain, numerical acceptance and display, §7
refusal layering and pre-owner order, §8 screen, §9 disclosure). ONE optional,
advisory, request-local calculation of the FREE change in length of ONE
inventor-declared unrestrained length of ONE material, on a Mechanical-root
project or for the ONE declared Mechanical part of a valid durable integrated
project (§1; eligibility is decided in the web layer).

What this module owns
  * the method's governed artifact (method authority, declarations, screen,
    numeric domain, limitations, disclosure meaning, NBS / NASA / NIST source
    and source-use records) and its fail-closed validation;
  * strict capture of the submitted form values (the ONLY place a string is
    turned into a number; the shared owner never parses), keeping the exact
    decimal values for the decimal reference;
  * the deterministic pre-owner order of §7 - completeness -> screen ->
    declarations -> numeric grammar and strictly positive exact coefficient
    and length -> owner -> decimal reference -> display; the FIRST failing
    stage alone decides the outcome;
  * the decimal reference (the exact rational product of the ENTERED decimals,
    computed without binary arithmetic) and the finite display (12 significant
    digits, round half to even, signed, labelled exact or rounded);
  * the mapping of the shared owner's local state onto display reasons (§7):
    the owner state and token are preserved, never rewritten.

What it does not own: execution, unit validation and result packaging (the
shared owner, ``engine/deterministic_calculation.py``), the relation and the
binary acceptance (the method adapter,
``engine/mechanical_thermal_expansion_method.py``), authorization, eligibility
and rendering (the web layer). It never imports or loads another calculation
consumer, adapter or artifact, persists nothing, reads no project, session,
store, answer, component or SafetySignal, holds no material-property value and
has no network, provider, model, clock or randomness dependency. Nothing here
is a stress, joint-force, fit, tolerance, clearance, gap, failure, suitability
or safety statement, a measurement or evidence, and no result is carried into
or out of any other calculation (THERM-01 included). Its display rule is its
own (calc/units §13L).
"""
import copy
import hashlib
import json
import math
import re
from fractions import Fraction
from pathlib import Path

from engine import deterministic_calculation as _dc

METHOD_ID = "mechanical:free_linear_thermal_expansion"
METHOD_VERSION = "1.0"

ARTIFACT_ID = "mechanical_free_linear_thermal_expansion"
ARTIFACT_SCHEMA_VERSION = "1.0"
ARTIFACT_PATH = (Path(__file__).resolve().parent.parent / "docs" / "governance"
                 / "mechanical_content_config"
                 / "free_linear_thermal_expansion_v1.json")

# The trusted durable root domain that makes a project eligible (§1); the
# declared Mechanical part of a valid integrated composition is decided in the
# web layer through the shared ``_calc_gate``.
ELIGIBLE_ROOT_DOMAIN = "mechanical"

# §5 declarations D-1 to D-8, in contract order. Each one stays its own
# statement; any answer other than "applies" refuses MODEL_NOT_SUPPORTED.
DECLARATIONS = (
    ("free_unrestrained", "D-1"),
    ("one_material_uniform_temperature", "D-2"),
    ("own_coefficient", "D-3"),
    ("coefficient_direction", "D-4"),
    ("average_over_interval", "D-5"),
    ("reference_length", "D-6"),
    ("signed_change", "D-7"),
    ("reversible_thermal_change_only", "D-8"),
)
DECLARATION_IDS = tuple(d for d, _ in DECLARATIONS)
_CONTRACT_REF = dict(DECLARATIONS)

# §8 nine-item high-risk screen, in contract order: the same items as the
# other Mechanical calculation screens, so the inventor answers one familiar
# screen (its EN / AR copy is the existing UI_CAP13_SCREEN_* copy).
SCREEN_ITEMS = ("supports_people", "overhead_or_falling_hazard", "children",
                "safety_critical_load_path", "pressure", "high_temperature",
                "battery_containment", "medical_use", "food_contact")

# Numeric roles the inventor enters, with their fixed units (§4). The units are
# shown, never chosen.
VALUE_ROLES = (("alpha_avg", "1/K"), ("L_ref", "mm"), ("delta_T", "K"))
_UNIT = dict(VALUE_ROLES)
OUTPUT_ROLE = "delta_L"
OUTPUT_UNIT = "mm"

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
# range of valid coefficients, lengths or temperature changes) and the
# representation limits of the strict decimal grammars. They are NOT physical
# limits or material ranges.
MAX_VALUE_CHARS = 64
ALPHA_INTEGER_DIGITS = 12
ALPHA_FRACTION_DIGITS = 12
LENGTH_INTEGER_DIGITS = 12
LENGTH_FRACTION_DIGITS = 9
DELTA_T_INTEGER_DIGITS = 9
DELTA_T_FRACTION_DIGITS = 9
_ALPHA = re.compile(r"[0-9]{1,%d}(?:\.[0-9]{1,%d})?"
                    % (ALPHA_INTEGER_DIGITS, ALPHA_FRACTION_DIGITS), re.ASCII)
_LENGTH = re.compile(r"[0-9]{1,%d}(?:\.[0-9]{1,%d})?"
                     % (LENGTH_INTEGER_DIGITS, LENGTH_FRACTION_DIGITS), re.ASCII)
_DELTA_T = re.compile(r"-?[0-9]{1,%d}(?:\.[0-9]{1,%d})?"
                      % (DELTA_T_INTEGER_DIGITS, DELTA_T_FRACTION_DIGITS), re.ASCII)
_GRAMMAR = {"alpha_avg": _ALPHA, "L_ref": _LENGTH, "delta_T": _DELTA_T}

# The decimal-reference acceptance of a successful owner result (§6): the
# binary64 change in length must agree with the exact decimal product within
# this relative bound (the proven worst case is below 4.0000001 x 2**-53).
DECIMAL_REFERENCE_BOUND = Fraction(1, 2 ** 50)
# The finite display (§6): significant digits, round half to even.
DISPLAY_SIGNIFICANT_DIGITS = 12
# Plain decimal notation for 10**-6 <= |delta_L| < 10**12; scientific otherwise.
_PLAIN_MIN_EXPONENT = -6
_PLAIN_MAX_EXPONENT = 11

# Outcomes (display reasons, §7). Not owner states.
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
_EXPECTED_ROLES = (("alpha_avg", "linear_thermal_expansion_coefficient", "1/K"),
                   ("L_ref", "length", "mm"),
                   ("delta_T", "temperature_difference", "K"),
                   ("delta_L", "length", "mm"))
_DISCLOSURE_ITEMS = 7
# Each source record and the source-use record it must resolve to.
_SOURCE_POLICY = {"NBS-TE-S1": "mte:SU001", "NASA-TE-S2": "mte:SU002",
                  "NIST-TE-U": "mte:SU003"}

# The accepted governed meaning of artifact version "1", pinned per section: the
# SHA-256 of each section's canonical JSON (sorted keys, compact, ASCII). Any
# semantic edit - a declaration or screen meaning, a numeric-domain rule, the
# executed form or derivation, a limitation, a disclosure item or a source
# record - fails closed even when every key and id survives. Changing them needs
# a new artifact version under its own authorization, not an edit here alone.
_SEMANTIC_DIGESTS = {
    "method": "10168f72b6661ba041c621e60642a9713786a2b2bcba73f0a500c925f0edaf34",
    "numeric_domain": "f11ed478062f9e91e68b5d22d8b7dc6fec1c43958c25f4bc322b1a951e5aa26d",
    "declarations": "11cd3bf7ef52f175e05884d7511bf4490fa4009f7ba916db3518a87d563e1e91",
    "screen_items": "9afd531ae5d2b462bf82545c32394d22dc3c584abbfb8a7da0626cf2b1a00504",
    "limitations": "5e58d3386ac7face44f52ae5c61dff0f59dff05cb1a3847731cebadd1753747c",
    "disclosure": "aa53a01b4008a61783eae60a8084549e1becebb97101918afe6a3d59063805a6",
    "sources": "98e718740f6b1cbb57000b40f0eac0ba77353381e6849df369e6d6ad75a7e56a",
}
_PINNED_ARTIFACT_VERSION = "1"


def _section_digest(value):
    canonical = json.dumps(value, sort_keys=True, separators=(",", ":"),
                           ensure_ascii=True)
    return hashlib.sha256(canonical.encode("ascii")).hexdigest()


class ThermalExpansionKnowledgeError(ValueError):
    """The free linear thermal-expansion governed artifact is missing, unreadable or not
    valid. The consumer turns this into ``KNOWLEDGE_UNAVAILABLE`` with no
    calculation. The message names structure only, never content."""


def is_eligible(root_domain):
    """True iff the trusted durable root domain makes a project eligible (§1).
    Pure; anything but the exact token is ineligible."""
    return isinstance(root_domain, str) and root_domain == ELIGIBLE_ROOT_DOMAIN


def _text(value, field):
    limit = _MAX_LONG_TEXT if field in _LONG_FIELDS else _MAX_TEXT
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise ThermalExpansionKnowledgeError("%s: not a bounded non-empty string" % field)


def validate_artifact(data):
    """Validate the WHOLE artifact or raise ``ThermalExpansionKnowledgeError``.
    Exact keys, closed vocabularies, the method identity, the §5 / §8 sets and
    the seven §9 disclosure items exactly as the contract states them, and every
    source bound to its own source-use record. Returns ``data``."""
    if not isinstance(data, dict) or set(data) != _TOP_KEYS:
        raise ThermalExpansionKnowledgeError("artifact: unexpected or missing field")
    if data["artifact_id"] != ARTIFACT_ID \
            or data["schema_version"] != ARTIFACT_SCHEMA_VERSION:
        raise ThermalExpansionKnowledgeError("artifact: unknown identity or version")
    for field in ("artifact_version", "owner", "slice", "governance_note"):
        _text(data[field], field)
    method = data["method"]
    if not isinstance(method, dict) or set(method) != _METHOD_KEYS:
        raise ThermalExpansionKnowledgeError("method: unexpected or missing field")
    for field in _METHOD_KEYS:
        _text(method[field], field)
    if method["method_id"] != METHOD_ID or method["method_version"] != METHOD_VERSION:
        raise ThermalExpansionKnowledgeError("method: unknown identity or version")
    domain = data["numeric_domain"]
    if not isinstance(domain, dict) or set(domain) != _DOMAIN_KEYS:
        raise ThermalExpansionKnowledgeError("numeric_domain: unexpected or missing field")
    roles = domain["roles"]
    if not isinstance(roles, list) or len(roles) != len(_EXPECTED_ROLES):
        raise ThermalExpansionKnowledgeError("numeric_domain: roles malformed")
    for entry, expected in zip(roles, _EXPECTED_ROLES):
        if not isinstance(entry, dict) or set(entry) != _ROLE_KEYS:
            raise ThermalExpansionKnowledgeError("numeric_domain: role malformed")
        for field in _ROLE_KEYS:
            _text(entry[field], field)
        if (entry["role"], entry["quantity_kind"], entry["unit_token"]) != expected:
            raise ThermalExpansionKnowledgeError("numeric_domain: role binding changed")
    if not isinstance(domain["rules"], list) or not domain["rules"]:
        raise ThermalExpansionKnowledgeError("numeric_domain: rules missing")
    for rule in domain["rules"]:
        _text(rule, "rule")
    decls = data["declarations"]
    if not isinstance(decls, list) \
            or [d.get("declaration_id") if isinstance(d, dict) else None
                for d in decls] != list(DECLARATION_IDS):
        raise ThermalExpansionKnowledgeError("declarations: not the §5 set")
    for entry in decls:
        if set(entry) != _DECL_KEYS:
            raise ThermalExpansionKnowledgeError("declarations: unexpected or missing field")
        _text(entry["accepted_value"], "accepted_value")
        if entry["contract_ref"] != _CONTRACT_REF[entry["declaration_id"]] \
                or entry["refusal"] != MODEL_NOT_SUPPORTED:
            raise ThermalExpansionKnowledgeError("declarations: refusal mapping changed")
    items = data["screen_items"]
    if not isinstance(items, list) \
            or [i.get("item_id") if isinstance(i, dict) else None
                for i in items] != list(SCREEN_ITEMS):
        raise ThermalExpansionKnowledgeError("screen_items: not the §8 set")
    for entry in items:
        if set(entry) != _SCREEN_KEYS:
            raise ThermalExpansionKnowledgeError("screen_items: unexpected or missing field")
        _text(entry["item"], "item")
    if not isinstance(data["limitations"], list) or not data["limitations"]:
        raise ThermalExpansionKnowledgeError("limitations: missing")
    for entry in data["limitations"]:
        _text(entry, "limitation")
    disclosure = data["disclosure"]
    if not isinstance(disclosure, list) or len(disclosure) != _DISCLOSURE_ITEMS:
        raise ThermalExpansionKnowledgeError("disclosure: not the seven §9 requirements")
    for entry in disclosure:
        _text(entry, "disclosure")
    sources = data["sources"]
    if not isinstance(sources, list) or not sources:
        raise ThermalExpansionKnowledgeError("sources: missing")
    by_id = {}
    for record in sources:
        if not isinstance(record, dict):
            raise ThermalExpansionKnowledgeError("sources: not an object")
        record_type = record.get("record_type")
        allowed = _SOURCE_KEYS | (_POLICY_EXTRA_KEYS
                                  if record_type == "source_use_policy"
                                  else frozenset())
        if set(record) != allowed:
            raise ThermalExpansionKnowledgeError("sources: unexpected or missing field")
        if record_type not in ("source", "source_use_policy"):
            raise ThermalExpansionKnowledgeError("sources: unknown record type")
        for field in allowed - {"record_type"}:
            _text(record[field], field)
        if not _ISO_DATE.fullmatch(record["inspection_date"]):
            raise ThermalExpansionKnowledgeError("sources: inspection date malformed")
        if record["inspection_basis"] != "LEAD_SUPPLIED":
            raise ThermalExpansionKnowledgeError("sources: unknown inspection basis")
        if record["record_id"] in by_id:
            raise ThermalExpansionKnowledgeError("sources: duplicate record id")
        by_id[record["record_id"]] = record
    for source_id, policy_id in _SOURCE_POLICY.items():
        policy = by_id.get(policy_id)
        if policy is None or policy["record_type"] != "source_use_policy":
            raise ThermalExpansionKnowledgeError("sources: source-use record missing")
        record = by_id.get(source_id)
        if record is None or record["record_type"] != "source" \
                or record["source_use_policy_ref"] != policy_id:
            raise ThermalExpansionKnowledgeError("sources: source unresolved")
    if data["artifact_version"] != _PINNED_ARTIFACT_VERSION:
        raise ThermalExpansionKnowledgeError("artifact: unpinned version")
    for section, expected in _SEMANTIC_DIGESTS.items():
        if _section_digest(data[section]) != expected:
            raise ThermalExpansionKnowledgeError("%s: governed content changed" % section)
    return data


def load_artifact(path=None):
    """Read and validate the committed artifact. Any failure raises
    ``ThermalExpansionKnowledgeError``. Reads one local file only."""
    target = Path(path) if path is not None else ARTIFACT_PATH
    try:
        with open(target, encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, ValueError):
        raise ThermalExpansionKnowledgeError("artifact: unreadable") from None
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


def parse_value(text, role):
    """The ONE string-to-number step: the EXACT decimal value (a ``Fraction``)
    of a strict ASCII decimal within the role's representation limits (§6), or
    ``None``. Nothing is rounded; a zero coefficient or length is returned as
    zero and refused by the caller."""
    pattern = _GRAMMAR[role]
    if not isinstance(text, str) or len(text) > MAX_VALUE_CHARS \
            or not pattern.fullmatch(text):
        return None
    return Fraction(text)


def exact_change(alpha_avg, L_ref, delta_T):
    """The exact rational product alpha_avg x L_ref x delta_T of the decimal
    reference (§6). Never shown unless a successful owner result agrees with
    it."""
    return alpha_avg * L_ref * delta_T


def agrees_with_reference(value, reference):
    """The decimal-reference acceptance of §6: exactly ``+0.0`` when, and only
    when, the reference is zero; otherwise of the same sign and within a
    relative error of at most ``DECIMAL_REFERENCE_BOUND``. A negative zero
    never agrees."""
    if not isinstance(value, float) or not math.isfinite(value):
        return False
    if not isinstance(reference, Fraction):
        return False
    if reference == 0:
        return value == 0.0 and math.copysign(1.0, value) > 0
    if value == 0.0 or (value > 0.0) != (reference > 0):
        return False
    return abs(Fraction(value) - reference) <= abs(reference) * DECIMAL_REFERENCE_BOUND


def _exponent10(magnitude):
    """floor(log10(magnitude)) for a positive ``Fraction``, exactly."""
    exponent = len(str(magnitude.numerator)) - len(str(magnitude.denominator))
    while Fraction(10) ** exponent > magnitude:
        exponent -= 1
    while Fraction(10) ** (exponent + 1) <= magnitude:
        exponent += 1
    return exponent


def format_change(value):
    """The finite display of an exact ``Fraction`` (§6): ``(text, exact)``.

    Zero is ``("0", True)``. Otherwise the magnitude is rounded once to
    ``DISPLAY_SIGNIFICANT_DIGITS`` significant digits, half to even, and the
    sign kept; ``exact`` is True only when that rounding changed nothing.
    Trailing zeros are dropped. Plain decimal notation is used for
    10**-6 <= |value| < 10**12 and ``m × 10^e`` otherwise. A nonzero value
    never displays as zero."""
    if not isinstance(value, Fraction):
        raise TypeError("exact Fraction required")
    if value == 0:
        return "0", True
    sign = "-" if value < 0 else ""
    magnitude = abs(value)
    exponent = _exponent10(magnitude)
    shift = DISPLAY_SIGNIFICANT_DIGITS - 1 - exponent
    digits = round(magnitude * Fraction(10) ** shift)   # half to even on a Fraction
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
        "change": None if display is None else display["change"],
    }


def evaluate(captured, binding, artifact=None, owner_artifact_path=None):
    """Run the §7 order for ONE captured submission. Never raises.

    Request integrity, authorization, eligibility and malformed requests belong
    to the web layer and have already passed. Then, first failing stage alone
    wins: completeness -> high-risk screen -> declarations D-1 to D-8 -> numeric
    grammar and strictly positive exact coefficient and length -> the shared
    owner -> the decimal-reference acceptance -> the display. No numerical
    payload accompanies any non-success outcome."""
    try:
        if artifact is None:
            load_artifact()
        else:
            validate_artifact(artifact)
    except ThermalExpansionKnowledgeError:
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
    # 3. declarations D-1 to D-8: any answer other than "applies" refuses.
    if any(declarations[d] != ANSWER_APPLIES for d in DECLARATION_IDS):
        return _outcome(MODEL_NOT_SUPPORTED)
    # 4. numeric: grammar, representation limits and a strictly positive exact
    # coefficient and length, all before any binary rounding. A zero is refused.
    values = {role: parse_value(raw[role], role) for role, _ in VALUE_ROLES}
    if any(v is None for v in values.values()) \
            or not values["alpha_avg"] > 0 or not values["L_ref"] > 0:
        return _outcome(INVALID_NUMERIC_INPUT)
    # 5. the shared owner, with typed values (one correctly rounded conversion
    # each; a negative zero temperature change is passed as +0.0) and the fixed
    # §4 unit tokens only.
    request = {
        "method_id": METHOD_ID,
        "method_version": METHOD_VERSION,
        "inputs": {role: {"value": float(values[role]) + 0.0, "unit": _UNIT[role]}
                   for role, _ in VALUE_ROLES},
        "subject_ref": None,
    }
    owner = _dc.execute(binding, request, artifact_path=owner_artifact_path)
    if owner.get("state") != _dc.STATE_SUCCESS:
        mapped = OWNER_CORRESPONDENCE.get((owner.get("state"), owner.get("reason")))
        return _outcome(mapped or UNMAPPED_OWNER_OUTCOME, owner)
    # 6. the exact decimal reference from the entered decimals, then the display.
    reference = exact_change(values["alpha_avg"], values["L_ref"], values["delta_T"])
    try:
        output = owner["outputs"][OUTPUT_ROLE]
        accepted = output["unit"] == OUTPUT_UNIT \
            and agrees_with_reference(output["value"], reference)
    except (KeyError, TypeError):
        accepted = False
    if not accepted:
        return _outcome(KNOWLEDGE_UNAVAILABLE, owner)
    text, exact = format_change(reference)
    return _outcome(OUTCOME_SUCCESS, owner, copy.deepcopy(owner),
                    {"value": text, "exact": exact, "change": reference})
