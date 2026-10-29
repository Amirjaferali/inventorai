"""Mechanical - Spring-Mass Natural Frequency - Slice 1: the consumer.

Authority: docs/governance/MECHANICAL_SPRING_MASS_NATURAL_FREQUENCY_METHOD_CONTRACT.md
(§5 declarations, §6 numeric domain, numerical acceptance and display, §7
refusal layering and pre-owner order, §8 screen, §9 disclosure). ONE optional,
advisory, request-local calculation of the undamped natural frequency of ONE
inventor-declared single-degree-of-freedom spring-mass model, on a
Mechanical-root project or for the ONE declared Mechanical part of a valid
durable integrated project (§1; eligibility is decided in the web layer).

What this module owns
  * the method's governed artifact (method authority, declarations, screen,
    numeric domain, limitations, disclosure meaning, NBS / NIST source and
    source-use records) and its fail-closed validation;
  * strict capture of the submitted form values (the ONLY place a string is
    turned into a number; the shared owner never parses), keeping the exact
    decimal values for the decimal reference;
  * the deterministic pre-owner order of §7 - completeness -> screen ->
    declarations -> numeric grammar and strictly positive exact decimals ->
    owner -> decimal reference -> display; the FIRST failing stage alone
    decides the outcome;
  * the decimal reference (the ``decimal`` module at 60 significant digits
    from the EXACT decimal inputs; an algorithm independent of the adapter's
    integer square-root bracket and of the binary64 execution) and the finite
    display (12 significant digits, round half to even, always labelled
    rounded: the result of a rational k / m is never a terminating decimal);
  * the mapping of the shared owner's local state onto display reasons (§7):
    the owner state and token are preserved, never rewritten.

What it does not own: execution, unit validation and result packaging (the
shared owner, ``engine/deterministic_calculation.py``), the relation, the
mathematical-constant policy and the binary acceptance (the method adapter,
``engine/mechanical_natural_frequency_method.py``), authorization, eligibility
and rendering (the web layer). It never imports or loads another calculation
consumer, adapter or artifact, persists nothing, reads no project, session,
store, answer, component or SafetySignal, and has no network, provider, model,
clock or randomness dependency. Nothing here is a resonance verdict, a damping,
amplitude, transmissibility or isolation result, a margin, a component choice,
a suitability or safety statement, a measurement or evidence. Its display rule
is its own (calc/units §13K).
"""
import copy
import hashlib
import json
import math
import re
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

from engine import deterministic_calculation as _dc

METHOD_ID = "mechanical:spring_mass_natural_frequency"
METHOD_VERSION = "1.0"

ARTIFACT_ID = "mechanical_spring_mass_natural_frequency"
ARTIFACT_SCHEMA_VERSION = "1.0"
ARTIFACT_PATH = (Path(__file__).resolve().parent.parent / "docs" / "governance"
                 / "mechanical_content_config"
                 / "spring_mass_natural_frequency_v1.json")

# The trusted durable root domain that makes a project eligible (§1); the
# declared Mechanical part of a valid integrated composition is decided in the
# web layer through the shared ``_calc_gate``.
ELIGIBLE_ROOT_DOMAIN = "mechanical"

# §5 declarations D-1 to D-7, in contract order. Each one stays its own
# statement; any answer other than "applies" refuses MODEL_NOT_SUPPORTED.
DECLARATIONS = (
    ("single_mass", "D-1"),
    ("single_linear_spring", "D-2"),
    ("rigid_support", "D-3"),
    ("single_degree_of_freedom", "D-4"),
    ("own_values", "D-5"),
    ("damping_not_modelled", "D-6"),
    ("outside_scope_excluded", "D-7"),
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
VALUE_ROLES = (("k", "N/m"), ("m", "kg"))
_UNIT = dict(VALUE_ROLES)
OUTPUT_ROLE = "f0"
OUTPUT_UNIT = "Hz"

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
# range of valid stiffnesses or masses) and the representation limits of the
# strict unsigned decimal grammar.
MAX_VALUE_CHARS = 64
INTEGER_DIGITS = 12
FRACTION_DIGITS = 9
_UNSIGNED = re.compile(r"[0-9]{1,%d}(?:\.[0-9]{1,%d})?"
                       % (INTEGER_DIGITS, FRACTION_DIGITS), re.ASCII)

# The decimal reference (§6): the ``decimal`` module at this precision, with
# the 60-decimal TRUNCATION of π (the next digits are 5923...). The reference
# carries a relative error far below 10^-57; the accepted owner result must
# agree with it within DECIMAL_REFERENCE_BOUND (the proven worst case of the
# binary path, including the two input conversions, is below 4 x 2^-53).
REFERENCE_PRECISION = 60
PI_60_DECIMALS = "3.141592653589793238462643383279502884197169399375105820974944"
DECIMAL_REFERENCE_BOUND = Fraction(1, 2 ** 50)
# The finite display (§6): significant digits, round half to even; the display
# is accepted only when the reference widened by DISPLAY_GUARD on either side
# rounds to the same digits.
DISPLAY_SIGNIFICANT_DIGITS = 12
DISPLAY_GUARD = Fraction(1, 10 ** 55)
# Plain decimal notation for 10**-6 <= f0 < 10**12; scientific otherwise.
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
_EXPECTED_ROLES = (("k", "stiffness", "N/m"), ("m", "mass", "kg"),
                   ("f0", "frequency", "Hz"))
_DISCLOSURE_ITEMS = 7
# Each source record and the source-use record it must resolve to.
_SOURCE_POLICY = {"NBS-NF-S1": "mnf:SU001", "NIST-NF-U": "mnf:SU002"}

# The accepted governed meaning of artifact version "1", pinned per section: the
# SHA-256 of each section's canonical JSON (sorted keys, compact, ASCII). Any
# semantic edit - a declaration or screen meaning, a numeric-domain rule, the
# executed form or derivation, a limitation, a disclosure item or a source
# record - fails closed even when every key and id survives. Changing them needs
# a new artifact version under its own authorization, not an edit here alone.
_SEMANTIC_DIGESTS = {
    "method": "ce39e7da03d5df1072db2d08f778edf0867a91b64070d23d12d5d0d616d657d8",
    "numeric_domain": "047fb140840b7c255f15d396f74da22cc05a8cc12cda52eff2bbdd23b63abd52",
    "declarations": "a7cae5b2c885cb5a7ee4ecb1efaa4bc0702d9d0a946052144f7a15c6e5a7ab6a",
    "screen_items": "9afd531ae5d2b462bf82545c32394d22dc3c584abbfb8a7da0626cf2b1a00504",
    "limitations": "d5a61f796b880d6c2a9543d48dc31263cdd89ea63f350d9cd7e611b5d4408dc0",
    "disclosure": "28447ca88f1982b06412646de129ce3278932f11f7094a5d2f4dab601662af4d",
    "sources": "197146ff797974e20533e805ea4371fed301e08a3800297561caa90db9a41fe9",
}
_PINNED_ARTIFACT_VERSION = "1"


def _section_digest(value):
    canonical = json.dumps(value, sort_keys=True, separators=(",", ":"),
                           ensure_ascii=True)
    return hashlib.sha256(canonical.encode("ascii")).hexdigest()


class NaturalFrequencyKnowledgeError(ValueError):
    """The natural-frequency governed artifact is missing, unreadable or not
    valid. The consumer turns this into ``KNOWLEDGE_UNAVAILABLE`` with no
    calculation. The message names structure only, never content."""


def is_eligible(root_domain):
    """True iff the trusted durable root domain makes a project eligible (§1).
    Pure; anything but the exact token is ineligible."""
    return isinstance(root_domain, str) and root_domain == ELIGIBLE_ROOT_DOMAIN


def _text(value, field):
    limit = _MAX_LONG_TEXT if field in _LONG_FIELDS else _MAX_TEXT
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise NaturalFrequencyKnowledgeError("%s: not a bounded non-empty string" % field)


def validate_artifact(data):
    """Validate the WHOLE artifact or raise ``NaturalFrequencyKnowledgeError``.
    Exact keys, closed vocabularies, the method identity, the §5 / §8 sets and
    the seven §9 disclosure items exactly as the contract states them, and every
    source bound to its own source-use record. Returns ``data``."""
    if not isinstance(data, dict) or set(data) != _TOP_KEYS:
        raise NaturalFrequencyKnowledgeError("artifact: unexpected or missing field")
    if data["artifact_id"] != ARTIFACT_ID \
            or data["schema_version"] != ARTIFACT_SCHEMA_VERSION:
        raise NaturalFrequencyKnowledgeError("artifact: unknown identity or version")
    for field in ("artifact_version", "owner", "slice", "governance_note"):
        _text(data[field], field)
    method = data["method"]
    if not isinstance(method, dict) or set(method) != _METHOD_KEYS:
        raise NaturalFrequencyKnowledgeError("method: unexpected or missing field")
    for field in _METHOD_KEYS:
        _text(method[field], field)
    if method["method_id"] != METHOD_ID or method["method_version"] != METHOD_VERSION:
        raise NaturalFrequencyKnowledgeError("method: unknown identity or version")
    domain = data["numeric_domain"]
    if not isinstance(domain, dict) or set(domain) != _DOMAIN_KEYS:
        raise NaturalFrequencyKnowledgeError("numeric_domain: unexpected or missing field")
    roles = domain["roles"]
    if not isinstance(roles, list) or len(roles) != len(_EXPECTED_ROLES):
        raise NaturalFrequencyKnowledgeError("numeric_domain: roles malformed")
    for entry, expected in zip(roles, _EXPECTED_ROLES):
        if not isinstance(entry, dict) or set(entry) != _ROLE_KEYS:
            raise NaturalFrequencyKnowledgeError("numeric_domain: role malformed")
        for field in _ROLE_KEYS:
            _text(entry[field], field)
        if (entry["role"], entry["quantity_kind"], entry["unit_token"]) != expected:
            raise NaturalFrequencyKnowledgeError("numeric_domain: role binding changed")
    if not isinstance(domain["rules"], list) or not domain["rules"]:
        raise NaturalFrequencyKnowledgeError("numeric_domain: rules missing")
    for rule in domain["rules"]:
        _text(rule, "rule")
    decls = data["declarations"]
    if not isinstance(decls, list) \
            or [d.get("declaration_id") if isinstance(d, dict) else None
                for d in decls] != list(DECLARATION_IDS):
        raise NaturalFrequencyKnowledgeError("declarations: not the §5 set")
    for entry in decls:
        if set(entry) != _DECL_KEYS:
            raise NaturalFrequencyKnowledgeError("declarations: unexpected or missing field")
        _text(entry["accepted_value"], "accepted_value")
        if entry["contract_ref"] != _CONTRACT_REF[entry["declaration_id"]] \
                or entry["refusal"] != MODEL_NOT_SUPPORTED:
            raise NaturalFrequencyKnowledgeError("declarations: refusal mapping changed")
    items = data["screen_items"]
    if not isinstance(items, list) \
            or [i.get("item_id") if isinstance(i, dict) else None
                for i in items] != list(SCREEN_ITEMS):
        raise NaturalFrequencyKnowledgeError("screen_items: not the §8 set")
    for entry in items:
        if set(entry) != _SCREEN_KEYS:
            raise NaturalFrequencyKnowledgeError("screen_items: unexpected or missing field")
        _text(entry["item"], "item")
    if not isinstance(data["limitations"], list) or not data["limitations"]:
        raise NaturalFrequencyKnowledgeError("limitations: missing")
    for entry in data["limitations"]:
        _text(entry, "limitation")
    disclosure = data["disclosure"]
    if not isinstance(disclosure, list) or len(disclosure) != _DISCLOSURE_ITEMS:
        raise NaturalFrequencyKnowledgeError("disclosure: not the seven §9 requirements")
    for entry in disclosure:
        _text(entry, "disclosure")
    sources = data["sources"]
    if not isinstance(sources, list) or not sources:
        raise NaturalFrequencyKnowledgeError("sources: missing")
    by_id = {}
    for record in sources:
        if not isinstance(record, dict):
            raise NaturalFrequencyKnowledgeError("sources: not an object")
        record_type = record.get("record_type")
        allowed = _SOURCE_KEYS | (_POLICY_EXTRA_KEYS
                                  if record_type == "source_use_policy"
                                  else frozenset())
        if set(record) != allowed:
            raise NaturalFrequencyKnowledgeError("sources: unexpected or missing field")
        if record_type not in ("source", "source_use_policy"):
            raise NaturalFrequencyKnowledgeError("sources: unknown record type")
        for field in allowed - {"record_type"}:
            _text(record[field], field)
        if not _ISO_DATE.fullmatch(record["inspection_date"]):
            raise NaturalFrequencyKnowledgeError("sources: inspection date malformed")
        if record["inspection_basis"] != "LEAD_SUPPLIED":
            raise NaturalFrequencyKnowledgeError("sources: unknown inspection basis")
        if record["record_id"] in by_id:
            raise NaturalFrequencyKnowledgeError("sources: duplicate record id")
        by_id[record["record_id"]] = record
    for source_id, policy_id in _SOURCE_POLICY.items():
        policy = by_id.get(policy_id)
        if policy is None or policy["record_type"] != "source_use_policy":
            raise NaturalFrequencyKnowledgeError("sources: source-use record missing")
        record = by_id.get(source_id)
        if record is None or record["record_type"] != "source" \
                or record["source_use_policy_ref"] != policy_id:
            raise NaturalFrequencyKnowledgeError("sources: source unresolved")
    if data["artifact_version"] != _PINNED_ARTIFACT_VERSION:
        raise NaturalFrequencyKnowledgeError("artifact: unpinned version")
    for section, expected in _SEMANTIC_DIGESTS.items():
        if _section_digest(data[section]) != expected:
            raise NaturalFrequencyKnowledgeError("%s: governed content changed" % section)
    return data


def load_artifact(path=None):
    """Read and validate the committed artifact. Any failure raises
    ``NaturalFrequencyKnowledgeError``. Reads one local file only."""
    target = Path(path) if path is not None else ARTIFACT_PATH
    try:
        with open(target, encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, ValueError):
        raise NaturalFrequencyKnowledgeError("artifact: unreadable") from None
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


def parse_value(text):
    """The ONE string-to-number step: the EXACT decimal value (a ``Fraction``)
    of a strict unsigned ASCII decimal within the representation limits (§6),
    or ``None``. Nothing is rounded; zero is returned as zero and refused by
    the caller."""
    if not isinstance(text, str) or len(text) > MAX_VALUE_CHARS \
            or not _UNSIGNED.fullmatch(text):
        return None
    return Fraction(text)


def reference_frequency(k, m):
    """The decimal reference of §6 as an exact ``Fraction``: with the
    ``decimal`` module at ``REFERENCE_PRECISION`` significant digits, the
    correctly rounded quotient ``k / m`` of the exact decimal inputs, its
    correctly rounded square root and the correctly rounded division by
    ``2 π`` with the 60-decimal truncation of π. Independent of the adapter's
    integer square-root bracket and of the binary64 execution."""
    if not (isinstance(k, Fraction) and isinstance(m, Fraction) and k > 0 and m > 0):
        raise ValueError("strictly positive exact decimals required")
    with localcontext() as context:
        context.prec = REFERENCE_PRECISION
        k_dec = Decimal(k.numerator) / Decimal(k.denominator)
        m_dec = Decimal(m.numerator) / Decimal(m.denominator)
        ratio = k_dec / m_dec
        frequency = ratio.sqrt() / (2 * Decimal(PI_60_DECIMALS))
    return Fraction(frequency)


def agrees_with_reference(value, reference):
    """The decimal-reference acceptance of §6: a finite, strictly positive
    binary64 value within a relative error of at most
    ``DECIMAL_REFERENCE_BOUND`` of the (positive) reference."""
    if not isinstance(value, float) or not math.isfinite(value) or not value > 0.0:
        return False
    if not isinstance(reference, Fraction) or reference <= 0:
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


def _round_significant(magnitude):
    """``(digits, exponent)`` of a positive ``Fraction`` rounded once to
    ``DISPLAY_SIGNIFICANT_DIGITS`` significant digits, half to even."""
    exponent = _exponent10(magnitude)
    shift = DISPLAY_SIGNIFICANT_DIGITS - 1 - exponent
    digits = round(magnitude * Fraction(10) ** shift)   # half to even on a Fraction
    if digits == 10 ** DISPLAY_SIGNIFICANT_DIGITS:
        exponent += 1
        shift -= 1
        digits = round(magnitude * Fraction(10) ** shift)
    return digits, exponent


def format_frequency(reference):
    """The finite display of the positive exact ``Fraction`` reference (§6):
    its 12-significant-digit rounding (half to even, trailing zeros dropped;
    plain decimal for 10**-6 <= value < 10**12, ``m × 10^e`` otherwise), or
    ``None`` when the reference widened by ``DISPLAY_GUARD`` on either side
    would not round to the same digits. The value is always a rounding: no
    exact label exists for this method."""
    if not isinstance(reference, Fraction) or reference <= 0:
        raise TypeError("positive exact Fraction required")
    digits, exponent = _round_significant(reference)
    for guarded in (reference * (1 - DISPLAY_GUARD), reference * (1 + DISPLAY_GUARD)):
        if _round_significant(guarded) != (digits, exponent):
            return None
    text = str(digits)                          # DISPLAY_SIGNIFICANT_DIGITS digits
    if _PLAIN_MIN_EXPONENT <= exponent <= _PLAIN_MAX_EXPONENT:
        if exponent >= 0:
            whole, fraction = text[:exponent + 1], text[exponent + 1:]
        else:
            whole, fraction = "0", "0" * (-exponent - 1) + text
        fraction = fraction.rstrip("0")
        return whole + ("." + fraction if fraction else "")
    mantissa = text[0] + ("." + text[1:].rstrip("0") if text[1:].rstrip("0") else "")
    return "%s × 10^%d" % (mantissa, exponent)


def _outcome(outcome, owner=None, result=None, display=None):
    return {
        "outcome": outcome,
        "owner_state": None if owner is None else owner.get("state"),
        "owner_reason": None if owner is None else owner.get("reason"),
        "result": result,
        "display_value": None if display is None else display["value"],
        "frequency": None if display is None else display["frequency"],
    }


def evaluate(captured, binding, artifact=None, owner_artifact_path=None):
    """Run the §7 order for ONE captured submission. Never raises.

    Request integrity, authorization, eligibility and malformed requests belong
    to the web layer and have already passed. Then, first failing stage alone
    wins: completeness -> high-risk screen -> declarations D-1 to D-7 -> numeric
    grammar and strictly positive exact decimals -> the shared owner -> the
    decimal-reference acceptance -> the guarded display. No numerical payload
    accompanies any non-success outcome."""
    try:
        if artifact is None:
            load_artifact()
        else:
            validate_artifact(artifact)
    except NaturalFrequencyKnowledgeError:
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
    # 3. declarations D-1 to D-7: any answer other than "applies" refuses.
    if any(declarations[d] != ANSWER_APPLIES for d in DECLARATION_IDS):
        return _outcome(MODEL_NOT_SUPPORTED)
    # 4. numeric: grammar, representation limits and strictly positive exact
    # decimals, all before any binary rounding. A zero is refused, never computed.
    values = {role: parse_value(raw[role]) for role, _ in VALUE_ROLES}
    if any(v is None or not v > 0 for v in values.values()):
        return _outcome(INVALID_NUMERIC_INPUT)
    # 5. the shared owner, with typed values (one correctly rounded conversion
    # each) and the fixed §4 unit tokens only.
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
    # 6. the decimal reference from the exact decimal inputs, then the display.
    reference = reference_frequency(values["k"], values["m"])
    try:
        output = owner["outputs"][OUTPUT_ROLE]
        accepted = output["unit"] == OUTPUT_UNIT \
            and agrees_with_reference(output["value"], reference)
    except (KeyError, TypeError):
        accepted = False
    if not accepted:
        return _outcome(KNOWLEDGE_UNAVAILABLE, owner)
    text = format_frequency(reference)
    if text is None:
        return _outcome(KNOWLEDGE_UNAVAILABLE, owner)
    return _outcome(OUTCOME_SUCCESS, owner, copy.deepcopy(owner),
                    {"value": text, "frequency": reference})
