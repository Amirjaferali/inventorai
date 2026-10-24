"""Stage 25 / CAP-13 - Planar Single-Force Moment - Slice 1: the CAP-13 moment consumer.

Authority: docs/governance/STAGE25_CAP13_PLANAR_SINGLE_FORCE_MOMENT_METHOD_CONTRACT.md
(§5 declarations, §6 numeric domain and numerical acceptance, §7 refusal layering
and pre-owner order, §8 screen, §9 disclosure). ONE optional, advisory,
request-local calculation of the magnitude of the moment of ONE force about ONE
inventor-chosen point in ONE plane, on a Mechanical-root project ONLY (§1: the
Stage 15 integrated-part exception is not extended to this method).

What this module owns
  * the moment method's governed artifact (method authority, declarations,
    screen, numeric domain, limitations, disclosure meaning, NASA / NIST source
    and source-use records) and its fail-closed validation;
  * strict capture of the submitted form values (the ONLY place a string is
    turned into a number; the shared owner never parses);
  * the deterministic pre-owner order of §7 - completeness -> screen ->
    declarations -> numeric; the FIRST failing stage alone decides the outcome;
  * the mapping of the shared owner's local state onto display reasons (§7):
    the owner state and token are preserved, never rewritten.

What it does not own: execution, unit validation and result packaging (the
shared owner, ``engine/deterministic_calculation.py``), the equation and its
numerical acceptance (the method adapter, ``engine/cap13_planar_moment_method.py``),
authorization, eligibility and rendering (the web layer). It never imports or
loads the two-support reactions consumer or its artifact, nor anything of
THERM-01, persists nothing, reads no project, session, store, answer,
requirement quantity or SafetySignal, and has no network, provider, model, clock
or randomness dependency. Nothing here is evidence, an equilibrium, capacity,
strength, suitability or safety statement.
"""
import copy
import hashlib
import json
import math
import re
from pathlib import Path

from engine import deterministic_calculation as _dc

METHOD_ID = "cap13:planar_single_force_moment"
METHOD_VERSION = "1.0"

ARTIFACT_ID = "cap13_planar_single_force_moment"
ARTIFACT_SCHEMA_VERSION = "1.0"
ARTIFACT_PATH = (Path(__file__).resolve().parent.parent / "docs" / "governance"
                 / "cap13_content_config"
                 / "planar_single_force_moment_v1.json")

# The trusted durable root domain that makes a project eligible (§1).
ELIGIBLE_ROOT_DOMAIN = "mechanical"

# §5 declarations D-1 to D-5, in contract order. Each one stays its own
# statement; any answer other than "applies" refuses MODEL_NOT_SUPPORTED.
DECLARATIONS = (
    ("planar", "D-1"),
    ("single_force", "D-2"),
    ("perpendicular_distance", "D-3"),
    ("chosen_point", "D-4"),
    ("static_magnitude", "D-5"),
)
DECLARATION_IDS = tuple(d for d, _ in DECLARATIONS)
_CONTRACT_REF = dict(DECLARATIONS)

# §8 nine-item high-risk screen, in contract order: the same items as the
# two-support reactions screen, so a CAP-13 inventor answers one familiar screen.
SCREEN_ITEMS = ("supports_people", "overhead_or_falling_hazard", "children",
                "safety_critical_load_path", "pressure", "high_temperature",
                "battery_containment", "medical_use", "food_contact")

# Numeric roles the inventor enters, with their fixed units (§4). The units are
# shown, never chosen. ``d_perp`` is the ASCII identifier of the role d⊥.
VALUE_ROLES = (("F", "N"), ("d_perp", "mm"))
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
# range of valid forces or distances).
MAX_VALUE_CHARS = 64

# Moment outcomes (display reasons, §7). Not owner states.
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

# §7 correspondence: the shared-owner local state / token -> moment display.
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
_EXPECTED_ROLES = (("F", "force", "N"), ("d_perp", "length", "mm"),
                   ("M", "moment", "N·mm"))
_DISCLOSURE_ITEMS = 7
# Each source record and the source-use record it must resolve to.
_SOURCE_POLICY = {"NASA-S1": "cap13m:SU001", "NASA-T1": "cap13m:SU001",
                  "NIST-U": "cap13m:SU002"}

# The accepted governed meaning of artifact version "1", pinned per section: the
# SHA-256 of each section's canonical JSON (sorted keys, compact, ASCII). Any
# semantic edit - a declaration or screen meaning, a numeric-domain rule, the
# executed form or derivation, a limitation, a disclosure item or a source
# record - fails closed even when every key and id survives. Changing them needs
# a new artifact version under its own authorization, not an edit here alone.
_SEMANTIC_DIGESTS = {
    "method": "f09f4b3c55e1b28547387cff61a48240ae6fbe7697f9b93c201c764c00f93904",
    "numeric_domain": "ecaff928480d5810afd5beaf80029551cd4fc6b807e672243658c3c83e177a45",
    "declarations": "5bd780787472337bfcca13472f087314fc4fc1edacf930152383f3944e36ec97",
    "screen_items": "9afd531ae5d2b462bf82545c32394d22dc3c584abbfb8a7da0626cf2b1a00504",
    "limitations": "7fd59f5fa1e2dca674f45d802163423f14077965c3e0df7e39f6bf1890af1db5",
    "disclosure": "1bf554b71e480738d33f65f32ba77ea50952fd3753fae6f0601aeb0926fdada7",
    "sources": "bcbee5bccf970e65d2601d1fa860436c3b99c4f60c709cfcf08609acac4b6af4",
}
_PINNED_ARTIFACT_VERSION = "1"


def _section_digest(value):
    canonical = json.dumps(value, sort_keys=True, separators=(",", ":"),
                           ensure_ascii=True)
    return hashlib.sha256(canonical.encode("ascii")).hexdigest()


class MomentKnowledgeError(ValueError):
    """The moment governed artifact is missing, unreadable or not valid. The
    consumer turns this into ``KNOWLEDGE_UNAVAILABLE`` with no calculation. The
    message names structure only, never content."""


def is_eligible(root_domain):
    """True iff the trusted durable root domain makes a project eligible (§1).
    Pure; anything but the exact token is ineligible."""
    return isinstance(root_domain, str) and root_domain == ELIGIBLE_ROOT_DOMAIN


def _text(value, field):
    limit = _MAX_LONG_TEXT if field in _LONG_FIELDS else _MAX_TEXT
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise MomentKnowledgeError("%s: not a bounded non-empty string" % field)


def validate_artifact(data):
    """Validate the WHOLE moment artifact or raise ``MomentKnowledgeError``.
    Exact keys, closed vocabularies, the method identity, the §5 / §8 sets and
    the seven §9 disclosure items exactly as the contract states them, and every
    source bound to its own source-use record. Returns ``data``."""
    if not isinstance(data, dict) or set(data) != _TOP_KEYS:
        raise MomentKnowledgeError("artifact: unexpected or missing field")
    if data["artifact_id"] != ARTIFACT_ID \
            or data["schema_version"] != ARTIFACT_SCHEMA_VERSION:
        raise MomentKnowledgeError("artifact: unknown identity or version")
    for field in ("artifact_version", "owner", "slice", "governance_note"):
        _text(data[field], field)
    method = data["method"]
    if not isinstance(method, dict) or set(method) != _METHOD_KEYS:
        raise MomentKnowledgeError("method: unexpected or missing field")
    for field in _METHOD_KEYS:
        _text(method[field], field)
    if method["method_id"] != METHOD_ID or method["method_version"] != METHOD_VERSION:
        raise MomentKnowledgeError("method: unknown identity or version")
    domain = data["numeric_domain"]
    if not isinstance(domain, dict) or set(domain) != _DOMAIN_KEYS:
        raise MomentKnowledgeError("numeric_domain: unexpected or missing field")
    roles = domain["roles"]
    if not isinstance(roles, list) or len(roles) != len(_EXPECTED_ROLES):
        raise MomentKnowledgeError("numeric_domain: roles malformed")
    for entry, expected in zip(roles, _EXPECTED_ROLES):
        if not isinstance(entry, dict) or set(entry) != _ROLE_KEYS:
            raise MomentKnowledgeError("numeric_domain: role malformed")
        for field in _ROLE_KEYS:
            _text(entry[field], field)
        if (entry["role"], entry["quantity_kind"], entry["unit_token"]) != expected:
            raise MomentKnowledgeError("numeric_domain: role binding changed")
    if not isinstance(domain["rules"], list) or not domain["rules"]:
        raise MomentKnowledgeError("numeric_domain: rules missing")
    for rule in domain["rules"]:
        _text(rule, "rule")
    decls = data["declarations"]
    if not isinstance(decls, list) \
            or [d.get("declaration_id") if isinstance(d, dict) else None
                for d in decls] != list(DECLARATION_IDS):
        raise MomentKnowledgeError("declarations: not the §5 set")
    for entry in decls:
        if set(entry) != _DECL_KEYS:
            raise MomentKnowledgeError("declarations: unexpected or missing field")
        _text(entry["accepted_value"], "accepted_value")
        if entry["contract_ref"] != _CONTRACT_REF[entry["declaration_id"]] \
                or entry["refusal"] != MODEL_NOT_SUPPORTED:
            raise MomentKnowledgeError("declarations: refusal mapping changed")
    items = data["screen_items"]
    if not isinstance(items, list) \
            or [i.get("item_id") if isinstance(i, dict) else None
                for i in items] != list(SCREEN_ITEMS):
        raise MomentKnowledgeError("screen_items: not the §8 set")
    for entry in items:
        if set(entry) != _SCREEN_KEYS:
            raise MomentKnowledgeError("screen_items: unexpected or missing field")
        _text(entry["item"], "item")
    if not isinstance(data["limitations"], list) or not data["limitations"]:
        raise MomentKnowledgeError("limitations: missing")
    for entry in data["limitations"]:
        _text(entry, "limitation")
    disclosure = data["disclosure"]
    if not isinstance(disclosure, list) or len(disclosure) != _DISCLOSURE_ITEMS:
        raise MomentKnowledgeError("disclosure: not the seven §9 requirements")
    for entry in disclosure:
        _text(entry, "disclosure")
    sources = data["sources"]
    if not isinstance(sources, list) or not sources:
        raise MomentKnowledgeError("sources: missing")
    by_id = {}
    for record in sources:
        if not isinstance(record, dict):
            raise MomentKnowledgeError("sources: not an object")
        record_type = record.get("record_type")
        allowed = _SOURCE_KEYS | (_POLICY_EXTRA_KEYS
                                  if record_type == "source_use_policy"
                                  else frozenset())
        if set(record) != allowed:
            raise MomentKnowledgeError("sources: unexpected or missing field")
        if record_type not in ("source", "source_use_policy"):
            raise MomentKnowledgeError("sources: unknown record type")
        for field in allowed - {"record_type"}:
            _text(record[field], field)
        if not _ISO_DATE.fullmatch(record["inspection_date"]):
            raise MomentKnowledgeError("sources: inspection date malformed")
        if record["inspection_basis"] != "LEAD_SUPPLIED":
            raise MomentKnowledgeError("sources: unknown inspection basis")
        if record["record_id"] in by_id:
            raise MomentKnowledgeError("sources: duplicate record id")
        by_id[record["record_id"]] = record
    for source_id, policy_id in _SOURCE_POLICY.items():
        policy = by_id.get(policy_id)
        if policy is None or policy["record_type"] != "source_use_policy":
            raise MomentKnowledgeError("sources: source-use record missing")
        record = by_id.get(source_id)
        if record is None or record["record_type"] != "source" \
                or record["source_use_policy_ref"] != policy_id:
            raise MomentKnowledgeError("sources: source unresolved")
    if data["artifact_version"] != _PINNED_ARTIFACT_VERSION:
        raise MomentKnowledgeError("artifact: unpinned version")
    for section, expected in _SEMANTIC_DIGESTS.items():
        if _section_digest(data[section]) != expected:
            raise MomentKnowledgeError("%s: governed content changed" % section)
    return data


def load_artifact(path=None):
    """Read and validate the committed moment artifact. Any failure raises
    ``MomentKnowledgeError``. Reads one local file only."""
    target = Path(path) if path is not None else ARTIFACT_PATH
    try:
        with open(target, encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, ValueError):
        raise MomentKnowledgeError("artifact: unreadable") from None
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
    screen -> declarations D-1 to D-5 -> numeric (finite, strictly positive,
    within the non-physical text bound) -> the shared owner. No stage after a
    failing one is evaluated, and no numerical payload accompanies any
    non-success outcome.
    """
    try:
        if artifact is None:
            load_artifact()
        else:
            validate_artifact(artifact)
    except MomentKnowledgeError:
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
    # 4. numeric: malformed, over-length, non-finite, zero or negative. A zero
    # input is refused here, never computed (§6).
    force = parse_number(raw["F"])
    distance = parse_number(raw["d_perp"])
    if force is None or distance is None or force <= 0.0 or distance <= 0.0:
        return _outcome(INVALID_NUMERIC_INPUT)
    # 5. the shared owner, with typed values and the fixed §4 unit tokens only.
    request = {
        "method_id": METHOD_ID,
        "method_version": METHOD_VERSION,
        "inputs": {"F": {"value": force, "unit": _UNIT["F"]},
                   "d_perp": {"value": distance, "unit": _UNIT["d_perp"]}},
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
