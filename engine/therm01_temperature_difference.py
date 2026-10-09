"""Stage 27 / THERM-01 - Single-Path Temperature-Difference - Slice 1: the THERM-01 consumer.

Authority: docs/governance/STAGE27_THERM01_CONDUCTION_TEMPERATURE_DIFFERENCE_METHOD_CONTRACT.md
(§5 declarations, §6 numeric domain, §7 refusal layering and pre-owner order, §8
screen, §9 / §9A disclosure and wording). ONE optional, advisory, request-local
calculation for ONE declared heat path on an Electrical / Electronics-root project.

What this module owns
  * the THERM-01-owned governed artifact (method authority, declarations, screen,
    numeric domain, limitations, disclosure meaning, DOE / NIST source and
    source-use records) and its fail-closed validation;
  * strict capture of the submitted form values (the ONLY place a string is
    turned into a number; the shared owner never parses);
  * the deterministic pre-owner order of §7 - completeness -> screen ->
    declarations -> numeric; the FIRST failing stage alone decides the outcome;
  * the mapping of the shared owner's local state onto THERM-01 display reasons
    (§7 Layer A / Layer B): the owner state and token are preserved, never
    rewritten.

What it does not own: execution, unit validation and result packaging (the
shared owner, ``engine/deterministic_calculation.py``), the equation (the method
adapter, ``engine/therm01_conduction_method.py``), authorization, eligibility and
rendering (the web layer). It never imports or loads anything of CAP-13, persists
nothing, reads no project, session, store, answer, requirement quantity or
SafetySignal, and has no network, provider, model, clock or randomness
dependency. Nothing here is evidence, a temperature, a rating, a margin or a
safety or suitability statement.
"""
import copy
import hashlib
import json
import math
import re
from pathlib import Path

from engine import deterministic_calculation as _dc

METHOD_ID = "therm01:conduction_temperature_difference_single_path"
METHOD_VERSION = "1.0"

ARTIFACT_ID = "therm01_conduction_temperature_difference_single_path"
ARTIFACT_SCHEMA_VERSION = "1.0"
ARTIFACT_PATH = (Path(__file__).resolve().parent.parent / "docs" / "governance"
                 / "therm01_content_config"
                 / "conduction_temperature_difference_single_path_v1.json")

# The trusted durable root domain that makes a project eligible (§1).
ELIGIBLE_ROOT_DOMAIN = "electronics_electrical"

# §5 declarations D-1 to D-6, in contract order. Each one stays its own
# statement; any answer other than "applies" refuses PATH_NOT_SUPPORTED.
DECLARATIONS = (
    ("steady_state", "D-1"),
    ("single_path", "D-2"),
    ("uniform_one_dimensional_flow", "D-3"),
    ("constant_area", "D-4"),
    ("total_resistance", "D-5"),
    ("constant_resistance", "D-6"),
)
DECLARATION_IDS = tuple(d for d, _ in DECLARATIONS)
_CONTRACT_REF = dict(DECLARATIONS)

# §8 ten-item high-risk screen, in contract order.
SCREEN_ITEMS = ("battery_or_storage_cell", "mains_or_high_voltage",
                "fire_or_ignition", "touch_skin_or_medical",
                "pressurized_or_sealed", "safety_critical_or_life_supporting",
                "aerospace_or_vehicle", "non_electrical_heat_source",
                "cryogenic", "transient_or_pulsed")

# Numeric roles the inventor enters, with their fixed units (§4). The units are
# shown, never chosen. ``R_theta`` is the ASCII identifier of the role Rθ.
VALUE_ROLES = (("P", "W"), ("R_theta", "K/W"))
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
# range of valid heat flows or resistances).
MAX_VALUE_CHARS = 64

# THERM-01 outcomes (Layer A display reasons, §7 / §9A A-4). Not owner states.
OUTCOME_SUCCESS = "SUCCESS"
NOT_DECLARED = "NOT_DECLARED"
THERMAL_SPECIALIST_REVIEW_REQUIRED = "THERMAL_SPECIALIST_REVIEW_REQUIRED"
PATH_NOT_SUPPORTED = "PATH_NOT_SUPPORTED"
INVALID_NUMERIC_INPUT = "INVALID_NUMERIC_INPUT"
UNIT_NOT_SUPPORTED = "UNIT_NOT_SUPPORTED"
KNOWLEDGE_UNAVAILABLE = "KNOWLEDGE_UNAVAILABLE"
# Neutral fail-closed outcome for an owner state / token §7 does not map. It is
# NOT a reason token: no reason is invented and the owner state is preserved.
UNMAPPED_OWNER_OUTCOME = "UNMAPPED_OWNER_OUTCOME"
OUTCOMES = (OUTCOME_SUCCESS, NOT_DECLARED, THERMAL_SPECIALIST_REVIEW_REQUIRED,
            PATH_NOT_SUPPORTED, INVALID_NUMERIC_INPUT, UNIT_NOT_SUPPORTED,
            KNOWLEDGE_UNAVAILABLE, UNMAPPED_OWNER_OUTCOME)

# §7 correspondence: the shared-owner local state / token -> THERM-01 display.
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
# fractional part; no sign, exponent, comma, underscore, space, hex, unit suffix,
# inf or nan. Nothing is normalized or case-folded first.
_UNSIGNED = re.compile(r"[0-9]+(?:\.[0-9]+)?", re.ASCII)

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
_EXPECTED_ROLES = (("P", "power", "W"), ("R_theta", "thermal_resistance", "K/W"),
                   ("delta_T", "temperature_difference", "K"))
_DISCLOSURE_ITEMS = 7
# Each source record and the source-use record it must resolve to.
_SOURCE_POLICY = {"THERM-S1": "THERM-SU-DOE", "THERM-U": "THERM-SU-NIST"}

# The accepted governed meaning of artifact version "1", pinned per section: the
# SHA-256 of each section's canonical JSON (sorted keys, compact, ASCII). Any
# semantic edit - a declaration or screen meaning, a numeric-domain rule, the
# executed form or derivation, a limitation, a disclosure item or a source
# record - fails closed even when every key and id survives. Changing them needs
# a new artifact version under its own authorization, not an edit here alone.
_SEMANTIC_DIGESTS = {
    "method": "4bc8d72edc842e86270e43b1c8a25c87474c15acfc2e74cf4c5e463312c2acfc",
    "numeric_domain": "69037afd1cf0186e0840e0989f7529ec7b20278e16749eb8770eaa7e6858633a",
    "declarations": "f47c7f63d66bfb4dd8ab73ee66082f5fd5a2d46f7bb783a49eb9629f098746a2",
    "screen_items": "0605df1b670781ade45d030a0c36ca328d3bbfd072cd47a93a25ddced0ecbdc3",
    "limitations": "aae66b6bce268eea8a8bf6540277895029617f549ad1e2c73d9e443e3242ba50",
    "disclosure": "f14d1083177939721a28534a969b2f79cef0195ec7584eb73eb773e0e10f31bb",
    "sources": "443f6943969bec7c85b842265be4443818d5dce529d7e449e2e4e589e94f97f2",
}
_PINNED_ARTIFACT_VERSION = "1"


def _section_digest(value):
    canonical = json.dumps(value, sort_keys=True, separators=(",", ":"),
                           ensure_ascii=True)
    return hashlib.sha256(canonical.encode("ascii")).hexdigest()


class Therm01KnowledgeError(ValueError):
    """The THERM-01 governed artifact is missing, unreadable or not valid. The
    consumer turns this into ``KNOWLEDGE_UNAVAILABLE`` with no calculation. The
    message names structure only, never content."""


def is_eligible(root_domain):
    """True iff the trusted durable root domain makes a project eligible (§1).
    Pure; anything but the exact token is ineligible."""
    return isinstance(root_domain, str) and root_domain == ELIGIBLE_ROOT_DOMAIN


def _text(value, field):
    limit = _MAX_LONG_TEXT if field in _LONG_FIELDS else _MAX_TEXT
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise Therm01KnowledgeError("%s: not a bounded non-empty string" % field)


def validate_artifact(data):
    """Validate the WHOLE THERM-01 artifact or raise ``Therm01KnowledgeError``.
    Exact keys, closed vocabularies, the method identity, the §5 / §8 sets and
    the seven §9 disclosure items exactly as the contract states them, and every
    source bound to its own THERM-01 source-use record. Returns ``data``."""
    if not isinstance(data, dict) or set(data) != _TOP_KEYS:
        raise Therm01KnowledgeError("artifact: unexpected or missing field")
    if data["artifact_id"] != ARTIFACT_ID \
            or data["schema_version"] != ARTIFACT_SCHEMA_VERSION:
        raise Therm01KnowledgeError("artifact: unknown identity or version")
    for field in ("artifact_version", "owner", "slice", "governance_note"):
        _text(data[field], field)
    method = data["method"]
    if not isinstance(method, dict) or set(method) != _METHOD_KEYS:
        raise Therm01KnowledgeError("method: unexpected or missing field")
    for field in _METHOD_KEYS:
        _text(method[field], field)
    if method["method_id"] != METHOD_ID or method["method_version"] != METHOD_VERSION:
        raise Therm01KnowledgeError("method: unknown identity or version")
    domain = data["numeric_domain"]
    if not isinstance(domain, dict) or set(domain) != _DOMAIN_KEYS:
        raise Therm01KnowledgeError("numeric_domain: unexpected or missing field")
    roles = domain["roles"]
    if not isinstance(roles, list) or len(roles) != len(_EXPECTED_ROLES):
        raise Therm01KnowledgeError("numeric_domain: roles malformed")
    for entry, expected in zip(roles, _EXPECTED_ROLES):
        if not isinstance(entry, dict) or set(entry) != _ROLE_KEYS:
            raise Therm01KnowledgeError("numeric_domain: role malformed")
        for field in _ROLE_KEYS:
            _text(entry[field], field)
        if (entry["role"], entry["quantity_kind"], entry["unit_token"]) != expected:
            raise Therm01KnowledgeError("numeric_domain: role binding changed")
    if not isinstance(domain["rules"], list) or not domain["rules"]:
        raise Therm01KnowledgeError("numeric_domain: rules missing")
    for rule in domain["rules"]:
        _text(rule, "rule")
    decls = data["declarations"]
    if not isinstance(decls, list) \
            or [d.get("declaration_id") if isinstance(d, dict) else None
                for d in decls] != list(DECLARATION_IDS):
        raise Therm01KnowledgeError("declarations: not the §5 set")
    for entry in decls:
        if set(entry) != _DECL_KEYS:
            raise Therm01KnowledgeError("declarations: unexpected or missing field")
        _text(entry["accepted_value"], "accepted_value")
        if entry["contract_ref"] != _CONTRACT_REF[entry["declaration_id"]] \
                or entry["refusal"] != PATH_NOT_SUPPORTED:
            raise Therm01KnowledgeError("declarations: refusal mapping changed")
    items = data["screen_items"]
    if not isinstance(items, list) \
            or [i.get("item_id") if isinstance(i, dict) else None
                for i in items] != list(SCREEN_ITEMS):
        raise Therm01KnowledgeError("screen_items: not the §8 set")
    for entry in items:
        if set(entry) != _SCREEN_KEYS:
            raise Therm01KnowledgeError("screen_items: unexpected or missing field")
        _text(entry["item"], "item")
    if not isinstance(data["limitations"], list) or not data["limitations"]:
        raise Therm01KnowledgeError("limitations: missing")
    for entry in data["limitations"]:
        _text(entry, "limitation")
    disclosure = data["disclosure"]
    if not isinstance(disclosure, list) or len(disclosure) != _DISCLOSURE_ITEMS:
        raise Therm01KnowledgeError("disclosure: not the seven §9 requirements")
    for entry in disclosure:
        _text(entry, "disclosure")
    sources = data["sources"]
    if not isinstance(sources, list) or not sources:
        raise Therm01KnowledgeError("sources: missing")
    by_id = {}
    for record in sources:
        if not isinstance(record, dict):
            raise Therm01KnowledgeError("sources: not an object")
        record_type = record.get("record_type")
        allowed = _SOURCE_KEYS | (_POLICY_EXTRA_KEYS
                                  if record_type == "source_use_policy"
                                  else frozenset())
        if set(record) != allowed:
            raise Therm01KnowledgeError("sources: unexpected or missing field")
        if record_type not in ("source", "source_use_policy"):
            raise Therm01KnowledgeError("sources: unknown record type")
        for field in allowed - {"record_type"}:
            _text(record[field], field)
        if not _ISO_DATE.fullmatch(record["inspection_date"]):
            raise Therm01KnowledgeError("sources: inspection date malformed")
        if record["inspection_basis"] != "LEAD_SUPPLIED":
            raise Therm01KnowledgeError("sources: unknown inspection basis")
        if record["record_id"] in by_id:
            raise Therm01KnowledgeError("sources: duplicate record id")
        by_id[record["record_id"]] = record
    for source_id, policy_id in _SOURCE_POLICY.items():
        policy = by_id.get(policy_id)
        if policy is None or policy["record_type"] != "source_use_policy":
            raise Therm01KnowledgeError("sources: THERM-01 source-use record missing")
        record = by_id.get(source_id)
        if record is None or record["record_type"] != "source" \
                or record["source_use_policy_ref"] != policy_id:
            raise Therm01KnowledgeError("sources: source unresolved")
    if data["artifact_version"] != _PINNED_ARTIFACT_VERSION:
        raise Therm01KnowledgeError("artifact: unpinned version")
    for section, expected in _SEMANTIC_DIGESTS.items():
        if _section_digest(data[section]) != expected:
            raise Therm01KnowledgeError("%s: governed content changed" % section)
    return data


def load_artifact(path=None):
    """Read and validate the committed THERM-01 artifact. Any failure raises
    ``Therm01KnowledgeError``. Reads one local file only."""
    target = Path(path) if path is not None else ARTIFACT_PATH
    try:
        with open(target, encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, ValueError):
        raise Therm01KnowledgeError("artifact: unreadable") from None
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


def parse_number(text):
    """The ONE string-to-number step: ``float`` of a strict unsigned ASCII
    decimal of at most ``MAX_VALUE_CHARS`` characters, or ``None`` when the
    spelling is not admitted, over-length or not finite."""
    if not isinstance(text, str) or len(text) > MAX_VALUE_CHARS:
        return None
    if not _UNSIGNED.fullmatch(text):
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
    screen -> declarations D-1 to D-6 -> numeric (finite, strictly positive,
    within the non-physical text bound) -> the shared owner. No stage after a
    failing one is evaluated, and no numerical payload accompanies any
    non-success outcome.
    """
    try:
        if artifact is None:
            load_artifact()
        else:
            validate_artifact(artifact)
    except Therm01KnowledgeError:
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
        return _outcome(THERMAL_SPECIALIST_REVIEW_REQUIRED)
    # 3. declarations D-1 to D-6: any answer other than "applies" refuses.
    if any(declarations[d] != ANSWER_APPLIES for d in DECLARATION_IDS):
        return _outcome(PATH_NOT_SUPPORTED)
    # 4. numeric: malformed, over-length, non-finite, zero or negative.
    power = parse_number(raw["P"])
    resistance = parse_number(raw["R_theta"])
    if power is None or resistance is None or power <= 0.0 or resistance <= 0.0:
        return _outcome(INVALID_NUMERIC_INPUT)
    # 5. the shared owner, with typed values and the fixed §4 unit tokens only.
    request = {
        "method_id": METHOD_ID,
        "method_version": METHOD_VERSION,
        "inputs": {"P": {"value": power, "unit": _UNIT["P"]},
                   "R_theta": {"value": resistance, "unit": _UNIT["R_theta"]}},
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
