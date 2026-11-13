"""Mechanical - Planar Centered Rectangular Clearance: the method consumer.

Authority: docs/governance/MECHANICAL_PLANAR_CENTERED_RECTANGULAR_CLEARANCE_METHOD_CONTRACT.md
(§3 method, §5 declarations, §6 numeric domain and numerical acceptance, §7
outcome order, §9 disclosure). BOARD-ENCLOSURE-PLANAR-CLEARANCE-01.

What this module owns (method authority, Mechanical)
  * the method's governed artifact (identity, model, derivation, numeric domain,
    declarations, limitations, disclosure meaning, source records) and its
    fail-closed validation with per-section semantic pins;
  * the representation policy of an entered value (the ONE place a string
    becomes a number): a strict unsigned ASCII decimal, kept EXACT as a
    ``Fraction``; the shared owner never parses;
  * the geometric decision on the exact ENTERED decimals (met exactly when both
    margins are nonnegative; equality meets), the bridge acceptance of the shared
    owner's binary result against that exact reference, and the exact display;
  * the §7 outcome order, preserving the shared owner's state and reason token;
  * the §3A derived consequence (BOARD-ENCLOSURE-CONDITIONAL-REGION-BOUND-01):
    for a MET or NOT MET evaluation only, the per-axis minimum usable-region
    dimension ``board + 2c`` and the additional region dimension
    ``max(0, minimum - region)``, exact on the entered decimals and
    cross-checked against the margin (``minimum - region == -2 x margin``).

What it does not own: execution, unit validation and packaging (the shared
owner, ``engine/deterministic_calculation.py``); the relation's binary
arithmetic (the adapter, ``engine/mechanical_planar_clearance_method.py``); the
inventor's declaration, its lifecycle and its staleness (the Stage-15 owner,
``engine/subsystem_model.py``, persisted by ``engine/record_store.py``);
authorization, rendering and the shared presentation model (the web layer). It
persists nothing, reads no store, project, session or answer, imports no other
calculation consumer, and has no network, provider, model, clock or randomness
dependency. Nothing here states that parts fit, are compatible, safe, verified,
manufacturable or ready.
"""
import copy
import hashlib
import json
import math
import re
from fractions import Fraction
from pathlib import Path

from engine import deterministic_calculation as _dc

METHOD_ID = "mechanical:planar_centered_rectangular_clearance"
METHOD_VERSION = "1.0"
# The inventor-input shape of contract §5 / §8; stored with every revision.
DECLARATION_VERSION = "planar-clearance-declaration/1"

ARTIFACT_ID = "mechanical_planar_centered_rectangular_clearance"
ARTIFACT_SCHEMA_VERSION = "1.0"
# §3A: the governed derived consequence and its own version. Adding it changes
# neither METHOD_VERSION nor DECLARATION_VERSION, so no stored declaration is
# relabelled or reads NEEDS RECONFIRMATION because of it.
REGION_BOUND_ID = "mechanical:planar_centered_rectangular_clearance/region_bound"
REGION_BOUND_VERSION = "1"
ARTIFACT_PATH = (Path(__file__).resolve().parent.parent / "docs" / "governance"
                 / "mechanical_content_config"
                 / "planar_centered_rectangular_clearance_v1.json")

# §5 applicability declarations D-1 to D-8, in contract order.
DECLARATIONS = (
    ("rectangular_board", "D-1"),
    ("rectangular_region", "D-2"),
    ("region_unobstructed", "D-3"),
    ("centered_axis_aligned", "D-4"),
    ("same_plane", "D-5"),
    ("not_guide_mounted", "D-6"),
    ("uniform_clearance", "D-7"),
    ("nominal_values", "D-8"),
)
DECLARATION_IDS = tuple(d for d, _ in DECLARATIONS)
_CONTRACT_REF = dict(DECLARATIONS)
ANSWER_APPLIES = "applies"
ANSWER_DOES_NOT_APPLY = "does_not_apply"
ANSWERS = (ANSWER_APPLIES, ANSWER_DOES_NOT_APPLY)

# §4 roles, all in the exact token mm. ``c`` may be zero.
DIMENSION_ROLES = ("board_x", "board_y", "region_x", "region_y")
CLEARANCE_ROLE = "c"
VALUE_ROLES = DIMENSION_ROLES + (CLEARANCE_ROLE,)
UNIT = "mm"
OUTPUT_ROLES = ("margin_x", "margin_y")
AXES = (("x", "board_x", "region_x", "margin_x"),
        ("y", "board_y", "region_y", "margin_y"))
# The explicit, only admitted axis pairing (no rotation, no placement search).
AXIS_PAIRING = "board_x_along_region_x"
# An explicit "I do not know this value yet" (never zero, never a number).
VALUE_UNKNOWN = "unknown"

# §6 representation policy - NOT a physical rating or range.
VALUE_INTEGER_DIGITS = 6
VALUE_FRACTION_DIGITS = 4
MAX_VALUE_CHARS = VALUE_INTEGER_DIGITS + 1 + VALUE_FRACTION_DIGITS
_DECIMAL = re.compile(r"[0-9]{1,%d}(?:\.[0-9]{1,%d})?"
                      % (VALUE_INTEGER_DIGITS, VALUE_FRACTION_DIGITS), re.ASCII)
# One correctly rounded binary64 conversion / result: relative error <= 2**-53.
UNIT_ROUNDOFF = Fraction(1, 2 ** 53)

# Outcomes (scoped presentation meanings, §7; never owner states).
OUTCOME_MET = "MET"
OUTCOME_NOT_MET = "NOT_MET"
OUTCOME_MISSING = "MISSING_INFORMATION"
OUTCOME_INAPPLICABLE = "INAPPLICABLE"
OUTCOME_NOT_COMPUTED = "COULD_NOT_BE_COMPUTED"
OUTCOMES = (OUTCOME_MET, OUTCOME_NOT_MET, OUTCOME_MISSING, OUTCOME_INAPPLICABLE,
            OUTCOME_NOT_COMPUTED)
# What a MISSING_INFORMATION outcome names (besides the value roles).
MISSING_REGION_DESCRIPTION = "region_description"

_MAX_TEXT = 1500
_MAX_LONG_TEXT = 2000
_LONG_FIELDS = frozenset({"governance_note", "inspected_content", "derivation"})
_ISO_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
_TOP_KEYS = frozenset({
    "artifact_id", "schema_version", "artifact_version", "owner", "slice",
    "governance_note", "method", "numeric_domain", "declarations",
    "limitations", "disclosure", "sources", "region_bound"})
_REGION_BOUND_KEYS = frozenset({"consequence_id", "consequence_version", "contract",
                                "executed_form", "eligibility", "statements"})
_REGION_BOUND_STATEMENTS = 6
_METHOD_KEYS = frozenset({"method_id", "method_version", "declaration_version",
                          "contract", "model", "executed_form", "derivation"})
_DOMAIN_KEYS = frozenset({"roles", "rules"})
_ROLE_KEYS = frozenset({"role", "meaning", "quantity_kind", "unit_token"})
_DECL_KEYS = frozenset({"declaration_id", "contract_ref", "statement"})
_SOURCE_KEYS = frozenset({
    "record_id", "record_type", "source_type", "publisher", "source_title",
    "url", "source_use_policy_ref", "inspection_basis", "inspection_date",
    "inspected_content", "third_party_material_exclusion",
    "no_endorsement_limitation"})
_EXPECTED_ROLES = tuple((r, "length", UNIT) for r in VALUE_ROLES + OUTPUT_ROLES)
_DISCLOSURE_ITEMS = 7
_SOURCE_POLICY = {"PCC-DERIVATION": "pcc:SU001", "NIST-PCC-U": "pcc:SU002"}

# The accepted governed meaning of artifact version "1", pinned per section
# (SHA-256 of each section's canonical JSON). Any semantic edit fails closed.
_SEMANTIC_DIGESTS = {
    "method": "769fb1c53f639d8b8e40dd8add8bd41915b12c51e3b9fb21b77f1de222149721",
    "numeric_domain": "c2d7eabd4bb7719b98e3d0cb31917ec96deb0ac841fa53236f6069cf2b2cb308",
    "declarations": "a5007fd8ebdb9768a920b3e0fa858f311c5c4a23a6e4334cd8bca02b8f604aff",
    "limitations": "01b2c7163c2a4c28fd7a761a2528b775b2e7f31a310ef746c3780daf5e321ecb",
    "disclosure": "054eb2f44421d06aff16835a310f0402fcac621dd1d585103b9973a888540857",
    "sources": "64d83b2ef55909ea1d2db2dc275190f00c486d5c0f532e4d5de03d50f2801b8a",
    # artifact version 2 (§3A); every version-1 digest above is unchanged
    "region_bound": "52ee265bde74501db806983bb0150caaad26d3c0a652287f08ab56cb48b0d396",
}
_PINNED_ARTIFACT_VERSION = "2"


def _section_digest(value):
    canonical = json.dumps(value, sort_keys=True, separators=(",", ":"),
                           ensure_ascii=True)
    return hashlib.sha256(canonical.encode("ascii")).hexdigest()


class PlanarClearanceKnowledgeError(ValueError):
    """The governed artifact is missing, unreadable or not valid. Turned into
    ``COULD_NOT_BE_COMPUTED`` with no verdict. Structural message only."""


def _text(value, field):
    limit = _MAX_LONG_TEXT if field in _LONG_FIELDS else _MAX_TEXT
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise PlanarClearanceKnowledgeError("%s: not a bounded non-empty string" % field)


def validate_artifact(data):
    """Validate the WHOLE artifact or raise ``PlanarClearanceKnowledgeError``.
    Returns ``data``."""
    if not isinstance(data, dict) or set(data) != _TOP_KEYS:
        raise PlanarClearanceKnowledgeError("artifact: unexpected or missing field")
    if data["artifact_id"] != ARTIFACT_ID \
            or data["schema_version"] != ARTIFACT_SCHEMA_VERSION:
        raise PlanarClearanceKnowledgeError("artifact: unknown identity or version")
    for field in ("artifact_version", "owner", "slice", "governance_note"):
        _text(data[field], field)
    method = data["method"]
    if not isinstance(method, dict) or set(method) != _METHOD_KEYS:
        raise PlanarClearanceKnowledgeError("method: unexpected or missing field")
    for field in _METHOD_KEYS:
        _text(method[field], field)
    if (method["method_id"], method["method_version"],
            method["declaration_version"]) != (METHOD_ID, METHOD_VERSION,
                                               DECLARATION_VERSION):
        raise PlanarClearanceKnowledgeError("method: unknown identity or version")
    domain = data["numeric_domain"]
    if not isinstance(domain, dict) or set(domain) != _DOMAIN_KEYS:
        raise PlanarClearanceKnowledgeError("numeric_domain: unexpected or missing field")
    roles = domain["roles"]
    if not isinstance(roles, list) or len(roles) != len(_EXPECTED_ROLES):
        raise PlanarClearanceKnowledgeError("numeric_domain: roles malformed")
    for entry, expected in zip(roles, _EXPECTED_ROLES):
        if not isinstance(entry, dict) or set(entry) != _ROLE_KEYS:
            raise PlanarClearanceKnowledgeError("numeric_domain: role malformed")
        for field in _ROLE_KEYS:
            _text(entry[field], field)
        if (entry["role"], entry["quantity_kind"], entry["unit_token"]) != expected:
            raise PlanarClearanceKnowledgeError("numeric_domain: role binding changed")
    if not isinstance(domain["rules"], list) or not domain["rules"]:
        raise PlanarClearanceKnowledgeError("numeric_domain: rules missing")
    for rule in domain["rules"]:
        _text(rule, "rule")
    decls = data["declarations"]
    if not isinstance(decls, list) \
            or [d.get("declaration_id") if isinstance(d, dict) else None
                for d in decls] != list(DECLARATION_IDS):
        raise PlanarClearanceKnowledgeError("declarations: not the §5 set")
    for entry in decls:
        if set(entry) != _DECL_KEYS \
                or entry["contract_ref"] != _CONTRACT_REF[entry["declaration_id"]]:
            raise PlanarClearanceKnowledgeError("declarations: malformed")
        _text(entry["statement"], "statement")
    for section, count in (("limitations", None), ("disclosure", _DISCLOSURE_ITEMS)):
        items = data[section]
        if not isinstance(items, list) or not items \
                or (count is not None and len(items) != count):
            raise PlanarClearanceKnowledgeError("%s: malformed" % section)
        for entry in items:
            _text(entry, section)
    bound = data["region_bound"]
    if not isinstance(bound, dict) or set(bound) != _REGION_BOUND_KEYS:
        raise PlanarClearanceKnowledgeError("region_bound: unexpected or missing field")
    for field in _REGION_BOUND_KEYS - {"statements"}:
        _text(bound[field], field)
    if (bound["consequence_id"], bound["consequence_version"]) != (
            REGION_BOUND_ID, REGION_BOUND_VERSION):
        raise PlanarClearanceKnowledgeError("region_bound: unknown identity or version")
    statements = bound["statements"]
    if not isinstance(statements, list) or len(statements) != _REGION_BOUND_STATEMENTS:
        raise PlanarClearanceKnowledgeError("region_bound: statements malformed")
    for entry in statements:
        _text(entry, "statement")
    sources = data["sources"]
    if not isinstance(sources, list) or not sources:
        raise PlanarClearanceKnowledgeError("sources: missing")
    by_id = {}
    for record in sources:
        if not isinstance(record, dict) or set(record) != _SOURCE_KEYS:
            raise PlanarClearanceKnowledgeError("sources: unexpected or missing field")
        if record["record_type"] not in ("source", "source_use_policy"):
            raise PlanarClearanceKnowledgeError("sources: unknown record type")
        for field in _SOURCE_KEYS - {"record_type"}:
            _text(record[field], field)
        if not _ISO_DATE.fullmatch(record["inspection_date"]) \
                or record["inspection_basis"] != "LEAD_SUPPLIED":
            raise PlanarClearanceKnowledgeError("sources: inspection record malformed")
        if record["record_id"] in by_id:
            raise PlanarClearanceKnowledgeError("sources: duplicate record id")
        by_id[record["record_id"]] = record
    for source_id, policy_id in _SOURCE_POLICY.items():
        policy, record = by_id.get(policy_id), by_id.get(source_id)
        if policy is None or policy["record_type"] != "source_use_policy" \
                or record is None or record["record_type"] != "source" \
                or record["source_use_policy_ref"] != policy_id:
            raise PlanarClearanceKnowledgeError("sources: source unresolved")
    if data["artifact_version"] != _PINNED_ARTIFACT_VERSION:
        raise PlanarClearanceKnowledgeError("artifact: unpinned version")
    for section, expected in _SEMANTIC_DIGESTS.items():
        if _section_digest(data[section]) != expected:
            raise PlanarClearanceKnowledgeError("%s: governed content changed" % section)
    return data


def load_artifact(path=None):
    """Read and validate the committed artifact (one local file)."""
    target = Path(path) if path is not None else ARTIFACT_PATH
    try:
        with open(target, encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, ValueError):
        raise PlanarClearanceKnowledgeError("artifact: unreadable") from None
    return validate_artifact(data)


# --- representation policy (§6) ---------------------------------------------
def parse_value(text):
    """The ONE string-to-number step: the EXACT decimal value (``Fraction``) of
    a strict unsigned ASCII decimal within the representation limits, or
    ``None``. Nothing is rounded, truncated or normalised."""
    if not isinstance(text, str) or len(text) > MAX_VALUE_CHARS \
            or not _DECIMAL.fullmatch(text):
        return None
    return Fraction(text)


def is_admitted_value(role, text):
    """True when ``text`` is an admissible entered value for ``role``: the
    strict grammar, and strictly positive for a dimension or zero / positive
    for the clearance. Used by the declaration owner at capture and on load."""
    value = parse_value(text)
    if value is None or role not in VALUE_ROLES:
        return False
    return value >= 0 if role == CLEARANCE_ROLE else value > 0


def exact_margins(values):
    """The exact rational margins of contract §3 from exact ``Fraction``
    inputs: ``{"margin_x": Fraction, "margin_y": Fraction}``."""
    c = values[CLEARANCE_ROLE]
    return {margin: (values[region] - values[board]) / 2 - c
            for _axis, board, region, margin in AXES}


def region_bound(values, exact):
    """§3A: per axis, the exact minimum usable-region dimension that satisfies
    the declared condition with the declared board dimension, clearance,
    centered placement and applicability held fixed, and the additional region
    dimension needed for it (zero when the axis already satisfies it). Exact
    ``Fraction`` arithmetic on the entered decimals; each pair is cross-checked
    against the §3 margin (``minimum - region == -2 x margin``) and a mismatch
    raises ``ArithmeticError`` (never reachable for consistent inputs)."""
    c = values[CLEARANCE_ROLE]
    bounds = {}
    for axis, board, region, margin in AXES:
        minimum = values[board] + 2 * c
        if minimum - values[region] != -2 * exact[margin]:
            raise ArithmeticError("region bound disagrees with the margin")
        additional = max(Fraction(0), minimum - values[region])
        bounds[axis] = {"minimum": minimum, "additional": additional}
    return bounds


def bridge_bound(region, board, c, exact):
    """The §6 absolute / mixed bound on |binary - exact decimal| for one axis:
    ``e + (|m| + e)·u`` with ``e = ((R + B)/2 + c)·u``."""
    conversion = ((region + board) / 2 + c) * UNIT_ROUNDOFF
    return conversion + (abs(exact) + conversion) * UNIT_ROUNDOFF


def agrees_with_reference(value, exact, region, board, c):
    """The bridge acceptance: a finite binary64 ``value`` within the §6 bound
    of the exact decimal margin. No sign agreement is demanded near zero and
    no relative test against zero is made; the bound adds nothing to the
    geometric decision, which is taken from ``exact`` alone."""
    if not isinstance(value, float) or not math.isfinite(value):
        return False
    return abs(Fraction(value) - exact) <= bridge_bound(region, board, c, exact)


def format_exact(value):
    """The exact decimal text of a ``Fraction`` whose denominator has only the
    prime factors 2 and 5 (every margin of §6 does): no rounding. A leading
    minus marks a negative value; zero is ``"0"``."""
    if not isinstance(value, Fraction):
        raise TypeError("exact Fraction required")
    den, twos, fives = value.denominator, 0, 0
    while den % 2 == 0:
        den //= 2
        twos += 1
    while den % 5 == 0:
        den //= 5
        fives += 1
    if den != 1:
        raise ValueError("not a terminating decimal")
    places = max(twos, fives)
    scaled = abs(value) * 10 ** places
    digits = str(scaled.numerator).rjust(places + 1, "0")
    whole, frac = digits[:len(digits) - places], digits[len(digits) - places:]
    frac = frac.rstrip("0")
    body = whole + ("." + frac if frac else "")
    return ("-" if value < 0 else "") + body


def _outcome(outcome, **extra):
    result = {"outcome": outcome, "missing": [], "inapplicable": [],
              "owner_state": None, "owner_reason": None, "result_identity": None,
              "margins": None, "axes": None, "region_bound": None,
              "clearance_text": None}
    result.update(extra)
    return result


def evaluate(material, binding, artifact=None, owner_artifact_path=None):
    """Run the §7 order for ONE validated declaration material. Never raises.

    ``material`` is a mapping with ``values`` ({role: decimal text, ``"unknown"``
    or ``None``}), ``region_description`` (text or ``None``) and
    ``applicability`` ({declaration id: answer or ``None``}). Order: artifact ->
    applicability (any "does not apply" -> INAPPLICABLE) -> completeness ->
    grammar -> shared owner -> bridge -> MET / NOT MET decided on the exact
    entered decimals. No verdict accompanies any other outcome."""
    try:
        if artifact is None:
            load_artifact()
        else:
            validate_artifact(artifact)
    except PlanarClearanceKnowledgeError:
        return _outcome(OUTCOME_NOT_COMPUTED)
    try:
        answers = {d: material["applicability"].get(d) for d in DECLARATION_IDS}
        raw = {role: material["values"].get(role) for role in VALUE_ROLES}
        description = material.get("region_description")
    except (KeyError, AttributeError, TypeError):
        return _outcome(OUTCOME_NOT_COMPUTED)
    inapplicable = [d for d in DECLARATION_IDS if answers[d] == ANSWER_DOES_NOT_APPLY]
    missing = [role for role in VALUE_ROLES if raw[role] in (None, "", VALUE_UNKNOWN)]
    if not (isinstance(description, str) and description.strip()):
        missing.append(MISSING_REGION_DESCRIPTION)
    missing += [d for d in DECLARATION_IDS if answers[d] not in ANSWERS]
    if inapplicable:
        return _outcome(OUTCOME_INAPPLICABLE, inapplicable=inapplicable, missing=missing)
    if missing:
        return _outcome(OUTCOME_MISSING, missing=missing)
    if any(not is_admitted_value(role, raw[role]) for role in VALUE_ROLES):
        return _outcome(OUTCOME_NOT_COMPUTED)
    values = {role: parse_value(raw[role]) for role in VALUE_ROLES}
    request = {
        "method_id": METHOD_ID,
        "method_version": METHOD_VERSION,
        "inputs": {role: {"value": float(values[role]) + 0.0, "unit": UNIT}
                   for role in VALUE_ROLES},
        "subject_ref": None,
    }
    owner = _dc.execute(binding, request, artifact_path=owner_artifact_path)
    state, reason = owner.get("state"), owner.get("reason")
    if state != _dc.STATE_SUCCESS:
        return _outcome(OUTCOME_NOT_COMPUTED, owner_state=state, owner_reason=reason)
    exact = exact_margins(values)
    axes = []
    try:
        for axis, board, region, margin in AXES:
            output = owner["outputs"][margin]
            if output["unit"] != UNIT or not agrees_with_reference(
                    output["value"], exact[margin], values[region], values[board],
                    values[CLEARANCE_ROLE]):
                return _outcome(OUTCOME_NOT_COMPUTED, owner_state=state,
                                owner_reason=_dc.EXECUTION_INTEGRITY_FAILURE)
            # G1-2-LINKED-CHECK-TESTED-CLEARANCE-01: the nominal clearance on
            # EACH side of this axis, (region - board) / 2, exact on the entered
            # decimals and cross-checked against the margin (side - c ==
            # margin). Negative when the board is wider than the region; the
            # overlap is then shown as its own positive amount.
            side = (values[region] - values[board]) / 2
            if side - values[CLEARANCE_ROLE] != exact[margin]:
                raise TypeError("per-side clearance disagrees with the margin")
            axes.append({"axis": axis, "margin": exact[margin],
                         "margin_text": format_exact(exact[margin]),
                         "met": exact[margin] >= 0,
                         "shortfall_text": (format_exact(-exact[margin])
                                            if exact[margin] < 0 else None),
                         "side_gap": side,
                         "side_gap_text": format_exact(side) if side >= 0 else None,
                         "overlap_text": format_exact(-side) if side < 0 else None})
    except (KeyError, TypeError):
        return _outcome(OUTCOME_NOT_COMPUTED, owner_state=state,
                        owner_reason=_dc.EXECUTION_INTEGRITY_FAILURE)
    try:
        bounds = region_bound(values, exact)
    except ArithmeticError:
        return _outcome(OUTCOME_NOT_COMPUTED, owner_state=state,
                        owner_reason=_dc.EXECUTION_INTEGRITY_FAILURE)
    for item, (_axis, _board, region, _margin) in zip(axes, AXES):
        bound = bounds[item["axis"]]
        minimum_text = format_exact(bound["minimum"])
        item.update({
            "region_text": format_exact(values[region]),
            "region_min": bound["minimum"],
            "region_min_text": minimum_text,
            # within the §6 entry grammar, so it could be entered as a region
            # value here; a larger exact bound is shown untruncated and flagged
            "region_min_enterable": parse_value(minimum_text) is not None,
            "additional": bound["additional"],
            "additional_text": format_exact(bound["additional"]),
            "increase_needed": bound["additional"] > 0,
        })
    met = all(item["met"] for item in axes)
    return _outcome(OUTCOME_MET if met else OUTCOME_NOT_MET, owner_state=state,
                    owner_reason=reason,
                    result_identity=owner.get("result_identity"),
                    margins=copy.deepcopy(exact), axes=axes,
                    clearance_text=format_exact(values[CLEARANCE_ROLE]),
                    region_bound={"consequence_id": REGION_BOUND_ID,
                                  "consequence_version": REGION_BOUND_VERSION})
