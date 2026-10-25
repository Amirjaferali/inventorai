"""Stage 25 / CAP-13 - Planar Required Force - Slice 1: the required-force consumer.

Authority: docs/governance/STAGE25_CAP13_PLANAR_REQUIRED_FORCE_METHOD_CONTRACT.md
(§5 declarations, §6 numeric domain, numerical acceptance and display, §7
refusal layering and pre-owner order, §8 screen, §9 disclosure). ONE optional,
advisory, request-local calculation of the magnitude of the ONE force that,
acting at the inventor's own perpendicular distance from ONE inventor-chosen
point in ONE plane, would produce the inventor's own target moment about that
point, on a Mechanical-root project or for the ONE declared Mechanical part of a
valid durable integrated project (§1; eligibility is decided in the web layer).

What this module owns
  * the method's governed artifact (method authority, declarations, screen,
    numeric domain, limitations, disclosure meaning, NASA / NIST source and
    source-use records) and its fail-closed validation;
  * strict capture of the submitted form values (the ONLY place a string is
    turned into a number; the shared owner never parses), keeping the exact
    decimal values for the decimal reference;
  * the deterministic pre-owner order of §7 - completeness -> screen ->
    declarations -> numeric grammar -> positive distance -> owner -> decimal
    reference; the FIRST failing stage alone decides the outcome;
  * the exact quotient's finite display (12 significant digits, round half to
    even, labelled exact or rounded);
  * the mapping of the shared owner's local state onto display reasons (§7):
    the owner state and token are preserved, never rewritten.

What it does not own: execution, unit validation and result packaging (the
shared owner, ``engine/deterministic_calculation.py``), the relation and its
binary64 acceptance (the method adapter,
``engine/cap13_planar_required_force_method.py``), authorization, eligibility
and rendering (the web layer). It never imports or loads another calculation
consumer or artifact - the planar-moment method's evidence is restated in this
method's own source records, not read from that artifact - persists nothing,
transfers no result to or from any other calculation, reads no project,
session, store, answer, requirement quantity or SafetySignal, and has no
network, provider, model, clock or randomness dependency. Nothing here infers a
target moment, geometry or friction, or is an actuation, capacity, strength,
suitability or safety statement, a measurement or evidence.
"""
import copy
import hashlib
import json
import math
import re
from fractions import Fraction
from pathlib import Path

from engine import deterministic_calculation as _dc

METHOD_ID = "cap13:planar_required_force"
METHOD_VERSION = "1.0"

ARTIFACT_ID = "cap13_planar_required_force"
ARTIFACT_SCHEMA_VERSION = "1.0"
ARTIFACT_PATH = (Path(__file__).resolve().parent.parent / "docs" / "governance"
                 / "cap13_content_config"
                 / "planar_required_force_v1.json")

# The trusted durable root domain that makes a project eligible (§1); a declared
# Mechanical part of a valid durable integrated composition is offered through
# the web layer's shared ``_calc_gate`` rule.
ELIGIBLE_ROOT_DOMAIN = "mechanical"

# §5 declarations D-1 to D-6, in contract order. Each one stays its own
# statement; any answer other than "applies" refuses MODEL_NOT_SUPPORTED.
DECLARATIONS = (
    ("planar", "D-1"),
    ("single_force", "D-2"),
    ("perpendicular_distance", "D-3"),
    ("chosen_point", "D-4"),
    ("target_moment", "D-5"),
    ("static_magnitude", "D-6"),
)
DECLARATION_IDS = tuple(d for d, _ in DECLARATIONS)
_CONTRACT_REF = dict(DECLARATIONS)

# §8 nine-item high-risk screen, in contract order: the same items as the
# other CAP-13 screens, so a CAP-13 inventor answers one familiar screen.
SCREEN_ITEMS = ("supports_people", "overhead_or_falling_hazard", "children",
                "safety_critical_load_path", "pressure", "high_temperature",
                "battery_containment", "medical_use", "food_contact")

# Numeric roles the inventor enters, with their fixed units (§4). The units are
# shown, never chosen. ``d_perp`` is the ASCII identifier of the role d⊥.
VALUE_ROLES = (("M_target", "N·mm"), ("d_perp", "mm"))
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

# Representation limits of the strict unsigned decimal grammar (§6). They bound
# what can be typed; they are NOT physical limits, ratings or a claim that such
# values are realistic. Inside them every nonzero exact quotient lies between
# 10**-18 and 10**21 N, well inside the normal binary64 range.
MAX_VALUE_CHARS = 64
M_INTEGER_DIGITS = 12
D_INTEGER_DIGITS = 9
FRACTION_DIGITS = 9
_MOMENT = re.compile(r"[0-9]{1,%d}(?:\.[0-9]{1,%d})?"
                     % (M_INTEGER_DIGITS, FRACTION_DIGITS), re.ASCII)
_DISTANCE = re.compile(r"[0-9]{1,%d}(?:\.[0-9]{1,%d})?"
                       % (D_INTEGER_DIGITS, FRACTION_DIGITS), re.ASCII)

# The decimal-reference acceptance of a successful owner result (§6): the
# binary64 force must agree with the exact decimal quotient within this
# relative bound (the proven worst case is below 3.0000001 x 2**-53).
DECIMAL_REFERENCE_BOUND = Fraction(1, 2 ** 51)
# The finite display (§6): significant digits, round half to even.
DISPLAY_SIGNIFICANT_DIGITS = 12
# Plain decimal notation for 10**-6 <= F < 10**12; scientific otherwise.
_PLAIN_MIN_EXPONENT = -6
_PLAIN_MAX_EXPONENT = 11

# Outcomes (display reasons, §7). Not owner states.
OUTCOME_SUCCESS = "SUCCESS"
NOT_DECLARED = "NOT_DECLARED"
ENGINEERING_REVIEW_REQUIRED = "ENGINEERING_REVIEW_REQUIRED"
MODEL_NOT_SUPPORTED = "MODEL_NOT_SUPPORTED"
INVALID_NUMERIC_INPUT = "INVALID_NUMERIC_INPUT"
DISTANCE_NOT_POSITIVE = "DISTANCE_NOT_POSITIVE"
UNIT_NOT_SUPPORTED = "UNIT_NOT_SUPPORTED"
KNOWLEDGE_UNAVAILABLE = "KNOWLEDGE_UNAVAILABLE"
# Neutral fail-closed outcome for an owner state / token §7 does not map. It is
# NOT a reason token: no reason is invented and the owner state is preserved.
UNMAPPED_OWNER_OUTCOME = "UNMAPPED_OWNER_OUTCOME"
OUTCOMES = (OUTCOME_SUCCESS, NOT_DECLARED, ENGINEERING_REVIEW_REQUIRED,
            MODEL_NOT_SUPPORTED, INVALID_NUMERIC_INPUT, DISTANCE_NOT_POSITIVE,
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
_EXPECTED_ROLES = (("M_target", "moment", "N·mm"), ("d_perp", "length", "mm"),
                   ("F", "force", "N"))
_DISCLOSURE_ITEMS = 7
# Each source record and the source-use record it must resolve to.
_SOURCE_POLICY = {"NASA-S1": "cap13f:SU001", "NASA-T1": "cap13f:SU001",
                  "NIST-U": "cap13f:SU002"}

# The accepted governed meaning of artifact version "1", pinned per section: the
# SHA-256 of each section's canonical JSON (sorted keys, compact, ASCII). Any
# semantic edit fails closed even when every key and id survives. Changing them
# needs a new artifact version under its own authorization, not an edit here
# alone.
_SEMANTIC_DIGESTS = {
    "method": "ed4aca3bede04df03be0a3afff636778ab131d92824f8a8cc0e5e85fb42c1cc9",
    "numeric_domain": "2dec09bdcd880845114d34849f469f23fc2f65f54567eb05fe6c1e069375fca8",
    "declarations": "463e6a61a60c3609088bd45cec23be62953389a89810d71bfb354cf16e804488",
    "screen_items": "9afd531ae5d2b462bf82545c32394d22dc3c584abbfb8a7da0626cf2b1a00504",
    "limitations": "aa74959c5021164d8dbb4beac222f522834c37a3c9ab3bc9681bcf0bc60c67b3",
    "disclosure": "71b159b0806173921db4808d91937c0aee7eb60eaee6908e0cbec8e9131ea94e",
    "sources": "86fe5ccebb524388b4bfc49cb438c444e98d7045f0be5f7d3d8731305f72c513",
}
_PINNED_ARTIFACT_VERSION = "1"


def _section_digest(value):
    canonical = json.dumps(value, sort_keys=True, separators=(",", ":"),
                           ensure_ascii=True)
    return hashlib.sha256(canonical.encode("ascii")).hexdigest()


class RequiredForceKnowledgeError(ValueError):
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
        raise RequiredForceKnowledgeError("%s: not a bounded non-empty string" % field)


def validate_artifact(data):
    """Validate the WHOLE artifact or raise ``RequiredForceKnowledgeError``.
    Exact keys, closed vocabularies, the method identity, the §5 / §8 sets and
    the seven §9 disclosure items exactly as the contract states them, and every
    source bound to its own source-use record. Returns ``data``."""
    if not isinstance(data, dict) or set(data) != _TOP_KEYS:
        raise RequiredForceKnowledgeError("artifact: unexpected or missing field")
    if data["artifact_id"] != ARTIFACT_ID \
            or data["schema_version"] != ARTIFACT_SCHEMA_VERSION:
        raise RequiredForceKnowledgeError("artifact: unknown identity or version")
    for field in ("artifact_version", "owner", "slice", "governance_note"):
        _text(data[field], field)
    method = data["method"]
    if not isinstance(method, dict) or set(method) != _METHOD_KEYS:
        raise RequiredForceKnowledgeError("method: unexpected or missing field")
    for field in _METHOD_KEYS:
        _text(method[field], field)
    if method["method_id"] != METHOD_ID or method["method_version"] != METHOD_VERSION:
        raise RequiredForceKnowledgeError("method: unknown identity or version")
    domain = data["numeric_domain"]
    if not isinstance(domain, dict) or set(domain) != _DOMAIN_KEYS:
        raise RequiredForceKnowledgeError("numeric_domain: unexpected or missing field")
    roles = domain["roles"]
    if not isinstance(roles, list) or len(roles) != len(_EXPECTED_ROLES):
        raise RequiredForceKnowledgeError("numeric_domain: roles malformed")
    for entry, expected in zip(roles, _EXPECTED_ROLES):
        if not isinstance(entry, dict) or set(entry) != _ROLE_KEYS:
            raise RequiredForceKnowledgeError("numeric_domain: role malformed")
        for field in _ROLE_KEYS:
            _text(entry[field], field)
        if (entry["role"], entry["quantity_kind"], entry["unit_token"]) != expected:
            raise RequiredForceKnowledgeError("numeric_domain: role binding changed")
    if not isinstance(domain["rules"], list) or not domain["rules"]:
        raise RequiredForceKnowledgeError("numeric_domain: rules missing")
    for rule in domain["rules"]:
        _text(rule, "rule")
    decls = data["declarations"]
    if not isinstance(decls, list) \
            or [d.get("declaration_id") if isinstance(d, dict) else None
                for d in decls] != list(DECLARATION_IDS):
        raise RequiredForceKnowledgeError("declarations: not the §5 set")
    for entry in decls:
        if set(entry) != _DECL_KEYS:
            raise RequiredForceKnowledgeError("declarations: unexpected or missing field")
        _text(entry["accepted_value"], "accepted_value")
        if entry["contract_ref"] != _CONTRACT_REF[entry["declaration_id"]] \
                or entry["refusal"] != MODEL_NOT_SUPPORTED:
            raise RequiredForceKnowledgeError("declarations: refusal mapping changed")
    items = data["screen_items"]
    if not isinstance(items, list) \
            or [i.get("item_id") if isinstance(i, dict) else None
                for i in items] != list(SCREEN_ITEMS):
        raise RequiredForceKnowledgeError("screen_items: not the §8 set")
    for entry in items:
        if set(entry) != _SCREEN_KEYS:
            raise RequiredForceKnowledgeError("screen_items: unexpected or missing field")
        _text(entry["item"], "item")
    if not isinstance(data["limitations"], list) or not data["limitations"]:
        raise RequiredForceKnowledgeError("limitations: missing")
    for entry in data["limitations"]:
        _text(entry, "limitation")
    disclosure = data["disclosure"]
    if not isinstance(disclosure, list) or len(disclosure) != _DISCLOSURE_ITEMS:
        raise RequiredForceKnowledgeError("disclosure: not the seven §9 requirements")
    for entry in disclosure:
        _text(entry, "disclosure")
    sources = data["sources"]
    if not isinstance(sources, list) or not sources:
        raise RequiredForceKnowledgeError("sources: missing")
    by_id = {}
    for record in sources:
        if not isinstance(record, dict):
            raise RequiredForceKnowledgeError("sources: not an object")
        record_type = record.get("record_type")
        allowed = _SOURCE_KEYS | (_POLICY_EXTRA_KEYS
                                  if record_type == "source_use_policy"
                                  else frozenset())
        if set(record) != allowed:
            raise RequiredForceKnowledgeError("sources: unexpected or missing field")
        if record_type not in ("source", "source_use_policy"):
            raise RequiredForceKnowledgeError("sources: unknown record type")
        for field in allowed - {"record_type"}:
            _text(record[field], field)
        if not _ISO_DATE.fullmatch(record["inspection_date"]):
            raise RequiredForceKnowledgeError("sources: inspection date malformed")
        if record["inspection_basis"] != "LEAD_SUPPLIED":
            raise RequiredForceKnowledgeError("sources: unknown inspection basis")
        if record["record_id"] in by_id:
            raise RequiredForceKnowledgeError("sources: duplicate record id")
        by_id[record["record_id"]] = record
    for source_id, policy_id in _SOURCE_POLICY.items():
        policy = by_id.get(policy_id)
        if policy is None or policy["record_type"] != "source_use_policy":
            raise RequiredForceKnowledgeError("sources: source-use record missing")
        record = by_id.get(source_id)
        if record is None or record["record_type"] != "source" \
                or record["source_use_policy_ref"] != policy_id:
            raise RequiredForceKnowledgeError("sources: source unresolved")
    if data["artifact_version"] != _PINNED_ARTIFACT_VERSION:
        raise RequiredForceKnowledgeError("artifact: unpinned version")
    for section, expected in _SEMANTIC_DIGESTS.items():
        if _section_digest(data[section]) != expected:
            raise RequiredForceKnowledgeError("%s: governed content changed" % section)
    return data


def load_artifact(path=None):
    """Read and validate the committed artifact. Any failure raises
    ``RequiredForceKnowledgeError``. Reads one local file only."""
    target = Path(path) if path is not None else ARTIFACT_PATH
    try:
        with open(target, encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, ValueError):
        raise RequiredForceKnowledgeError("artifact: unreadable") from None
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
    of a strict unsigned ASCII decimal within the role's representation limits
    (§6), or ``None``. Nothing is rounded."""
    pattern = {"M_target": _MOMENT, "d_perp": _DISTANCE}[role]
    if not isinstance(text, str) or len(text) > MAX_VALUE_CHARS \
            or not pattern.fullmatch(text):
        return None
    return Fraction(text)


def exact_force(m_target, d_perp):
    """The exact rational quotient of the decimal reference (§6). Never shown
    unless a successful owner result agrees with it."""
    return m_target / d_perp


def agrees_with_reference(value, reference):
    """The decimal-reference acceptance of §6: exactly zero when, and only
    when, the reference is zero; otherwise strictly positive and within a
    relative error of ``DECIMAL_REFERENCE_BOUND``."""
    if not isinstance(value, float) or not math.isfinite(value):
        return False
    if reference == 0:
        return value == 0.0
    if not value > 0.0 or not reference > 0:
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


def format_force(value):
    """The finite display of an exact non-negative ``Fraction`` (§6):
    ``(text, exact)``.

    Zero is ``("0", True)``. Otherwise the value is rounded once to
    ``DISPLAY_SIGNIFICANT_DIGITS`` significant digits, half to even; ``exact``
    is True only when that rounding changed nothing. Trailing zeros are
    dropped. Plain decimal notation is used for 10**-6 <= value < 10**12 and
    ``m × 10^e`` otherwise. A nonzero value never displays as zero."""
    if not isinstance(value, Fraction):
        raise TypeError("exact Fraction required")
    if value < 0:
        raise ValueError("a force magnitude is never negative")
    if value == 0:
        return "0", True
    exponent = _exponent10(value)
    shift = DISPLAY_SIGNIFICANT_DIGITS - 1 - exponent
    digits = round(value * Fraction(10) ** shift)  # half to even on a Fraction
    if digits == 10 ** DISPLAY_SIGNIFICANT_DIGITS:
        exponent += 1
        shift -= 1
        digits = round(value * Fraction(10) ** shift)
    exact = Fraction(digits, 1) / Fraction(10) ** shift == value
    text = str(digits)                             # DISPLAY_SIGNIFICANT_DIGITS digits
    if _PLAIN_MIN_EXPONENT <= exponent <= _PLAIN_MAX_EXPONENT:
        if exponent >= 0:
            whole, fraction = text[:exponent + 1], text[exponent + 1:]
        else:
            whole, fraction = "0", "0" * (-exponent - 1) + text
        fraction = fraction.rstrip("0")
        body = whole + ("." + fraction if fraction else "")
    else:
        tail = text[1:].rstrip("0")
        body = "%s × 10^%d" % (text[0] + ("." + tail if tail else ""), exponent)
    return body, exact


def _outcome(outcome, owner=None, result=None, display=None):
    return {
        "outcome": outcome,
        "owner_state": None if owner is None else owner.get("state"),
        "owner_reason": None if owner is None else owner.get("reason"),
        "result": result,
        "display_value": None if display is None else display["value"],
        "display_exact": None if display is None else display["exact"],
        "zero_moment": None if display is None else display["zero"],
        "force": None if display is None else display["force"],
    }


def evaluate(captured, binding, artifact=None, owner_artifact_path=None):
    """Run the §7 order for ONE captured submission. Never raises.

    Request integrity, authorization, eligibility and malformed requests belong
    to the web layer and have already passed. Then, first failing stage alone
    wins: completeness -> high-risk screen -> declarations D-1 to D-6 -> numeric
    grammar -> positive distance -> the shared owner -> the decimal-reference
    acceptance. No numerical payload accompanies any non-success outcome."""
    try:
        if artifact is None:
            load_artifact()
        else:
            validate_artifact(artifact)
    except RequiredForceKnowledgeError:
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
    # 3. declarations D-1 to D-6: any answer other than "applies" refuses.
    if any(declarations[d] != ANSWER_APPLIES for d in DECLARATION_IDS):
        return _outcome(MODEL_NOT_SUPPORTED)
    # 4. numeric grammar, on the exact decimals.
    values = {role: parse_value(raw[role], role) for role, _ in VALUE_ROLES}
    if any(v is None for v in values.values()):
        return _outcome(INVALID_NUMERIC_INPUT)
    # 5. positive distance, decided on the exact decimal before any rounding.
    if not values["d_perp"] > 0:
        return _outcome(DISTANCE_NOT_POSITIVE)
    # 6. the shared owner, with one correctly rounded binary64 value per input
    # and the fixed §4 unit tokens only.
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
    # 7. the decimal-reference acceptance.
    reference = exact_force(values["M_target"], values["d_perp"])
    try:
        accepted = agrees_with_reference(owner["outputs"]["F"]["value"], reference)
    except (KeyError, TypeError):
        accepted = False
    if not accepted:
        return _outcome(KNOWLEDGE_UNAVAILABLE, owner)
    text, exact = format_force(reference)
    return _outcome(OUTCOME_SUCCESS, owner, copy.deepcopy(owner),
                    {"value": text, "exact": exact, "zero": reference == 0,
                     "force": reference})
