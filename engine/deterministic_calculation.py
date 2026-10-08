"""Shared deterministic calculation and units owner - first increment (A2 method-first).

Gate: Stage 25 / CAP-13 A-5 first bounded implementation, under the accepted
docs/governance/SHARED_DETERMINISTIC_CALCULATION_AND_UNITS_OWNER_BOUNDARY_CONTRACT.md
(with its accepted Correction 01, shape A2) and the accepted
docs/governance/STAGE25_CAP13_TWO_SUPPORT_STATIC_REACTIONS_METHOD_CONTRACT.md.
The owner is descriptive and unnumbered: it carries no CAP identifier.

What this owner owns (calc/units contract §3) - the execution ENVELOPE only:
  * admission of a request against its own governed artifact (§9);
  * exact role -> quantity kind -> unit token validation (no alias, no
    conversion, no dimensional equivalence);
  * typed numeric validation (no strings, no parsing, booleans refused, NaN and
    infinities refused);
  * deterministic execution control of ONE trusted, pre-bound method adapter;
  * finiteness / integrity / admitted-result-range checks;
  * result packaging with versions, request digest and result identity.

What it does NOT own: the method's equations, applicability, numeric domain,
declarations, screen, limitations or source authority. Those belong to the
method authority (CAP-13) and reach this module only as one immutable binding
created by application wiring (``bind_method``). This module imports no consumer
or method-authority module, reads no project, session, ledger, store, answer or
requirement quantity, writes nothing and has no clock, randomness, network,
provider or model dependency.

Result states (owner-local, calc/units contract §7) and closed reason tokens (§8)
are defined below. A non-success result never carries a numerical payload.
"""
import hashlib
import json
import math
import re
import types
from pathlib import Path

# --- owner-local result states (calc/units contract §7) --------------------
STATE_SUCCESS = "SUCCESS"
STATE_UNABLE = "UNABLE_TO_DETERMINE"
STATE_FAILURE = "FAILURE"
STATE_REFUSAL = "REFUSAL"
STATES = (STATE_SUCCESS, STATE_UNABLE, STATE_FAILURE, STATE_REFUSAL)

# --- closed reason tokens (calc/units contract §8) -------------------------
OPERATION_NOT_ADMITTED = "OPERATION_NOT_ADMITTED"
UNIT_NOT_ADMITTED = "UNIT_NOT_ADMITTED"
UNKNOWN_UNIT = "UNKNOWN_UNIT"
INCOMPATIBLE_DIMENSION = "INCOMPATIBLE_DIMENSION"
SEMANTIC_KIND_MISMATCH = "SEMANTIC_KIND_MISMATCH"
MISSING_PROVENANCE = "MISSING_PROVENANCE"
METHOD_NOT_REGISTERED = "METHOD_NOT_REGISTERED"
VERSION_MISMATCH = "VERSION_MISMATCH"
INVALID_NUMERIC_INPUT = "INVALID_NUMERIC_INPUT"
INPUT_MISSING = "INPUT_MISSING"
INPUT_OUTSIDE_ADMITTED_RANGE = "INPUT_OUTSIDE_ADMITTED_RANGE"
APPLICABILITY_REFUSED_BY_METHOD_AUTHORITY = "APPLICABILITY_REFUSED_BY_METHOD_AUTHORITY"
SOURCE_UNAVAILABLE = "SOURCE_UNAVAILABLE"
EXECUTION_INTEGRITY_FAILURE = "EXECUTION_INTEGRITY_FAILURE"

REASON_STATE = {
    OPERATION_NOT_ADMITTED: STATE_REFUSAL,
    UNIT_NOT_ADMITTED: STATE_REFUSAL,
    UNKNOWN_UNIT: STATE_REFUSAL,
    INCOMPATIBLE_DIMENSION: STATE_REFUSAL,
    SEMANTIC_KIND_MISMATCH: STATE_REFUSAL,
    MISSING_PROVENANCE: STATE_REFUSAL,
    METHOD_NOT_REGISTERED: STATE_REFUSAL,
    VERSION_MISMATCH: STATE_REFUSAL,
    INVALID_NUMERIC_INPUT: STATE_REFUSAL,
    INPUT_MISSING: STATE_UNABLE,
    INPUT_OUTSIDE_ADMITTED_RANGE: STATE_UNABLE,
    APPLICABILITY_REFUSED_BY_METHOD_AUTHORITY: STATE_UNABLE,
    SOURCE_UNAVAILABLE: STATE_UNABLE,
    EXECUTION_INTEGRITY_FAILURE: STATE_FAILURE,
}

VALIDATION_STATUS = "UNVALIDATED"
PROVENANCE_OWNER_STATED = "OWNER_STATED"
PROVENANCE_CALCULATED = "CALCULATED"

IMPLEMENTATION_VERSION = "1.0.0"
ARTIFACT_ID = "deterministic_calculation_owner"
ARTIFACT_SCHEMA_VERSION = "1.0"
ARTIFACT_PATH = (Path(__file__).resolve().parent.parent / "docs" / "governance"
                 / "deterministic_calculation_config"
                 / "deterministic_calculation_owner_v1.json")

# The closed applicability / result-range condition vocabulary this owner can
# check mechanically. The conditions themselves are declared by the method
# authority in the governed method record; the owner only evaluates them.
CONDITION_GREATER_THAN_ZERO = "greater_than_zero"
CONDITION_WITHIN_ZERO_AND_ROLE = "within_zero_and_role"
_CONDITIONS = (CONDITION_GREATER_THAN_ZERO, CONDITION_WITHIN_ZERO_AND_ROLE)

_ISO_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
_MAX_TEXT = 700
_MAX_LONG_TEXT = 2000
_LONG_FIELDS = frozenset({"governance_note", "inspected_content"})

_TOP_KEYS = frozenset({
    "artifact_id", "schema_version", "artifact_version", "owner",
    "governance_note", "quantity_kinds", "unit_records", "source_use_policies",
    "methods"})
_KIND_KEYS = frozenset({"quantity_kind", "dimension"})
_UNIT_KEYS = frozenset({
    "record_id", "unit_token", "unit_name", "quantity_kind", "source_title",
    "publisher", "edition", "doi", "url", "inspected_location",
    "inspected_content", "source_use_policy_ref", "inspection_basis",
    "inspection_date", "inspection_reference"})
_POLICY_KEYS = frozenset({
    "record_id", "source_title", "publisher", "url", "inspected_content",
    "inspection_basis", "inspection_date", "inspection_reference",
    "acknowledgement", "third_party_material_exclusion",
    "no_endorsement_limitation"})
_METHOD_KEYS = frozenset({
    "method_id", "method_version", "adapter_identity", "technical_authority",
    "method_authority_artifact", "source_qualification", "input_roles",
    "output_roles", "applicability", "result_range"})
_AUTHORITY_ARTIFACT_KEYS = frozenset({"artifact_id", "artifact_version"})
_QUALIFICATION_KEYS = frozenset({
    "source_ref", "source_title", "publisher", "url", "source_use_policy_ref",
    "inspection_basis", "inspection_date"})
_ROLE_KEYS = frozenset({"role", "quantity_kind", "unit_token"})
_CONDITION_KEYS = frozenset({"role", "condition", "bound_role"})
_REQUEST_KEYS = frozenset({"method_id", "method_version", "inputs", "subject_ref"})
_INPUT_KEYS = frozenset({"value", "unit"})


class CalculationArtifactError(ValueError):
    """The owner's governed artifact is present but not valid. Execution turns it
    into ``FAILURE / EXECUTION_INTEGRITY_FAILURE``. The message names structure
    only, never content."""


class CalculationArtifactUnavailable(OSError):
    """The owner's governed artifact cannot be read. Execution turns it into
    ``UNABLE_TO_DETERMINE / SOURCE_UNAVAILABLE``."""


# ---------------------------------------------------------------------------
# governed artifact (calc/units contract §9)
# ---------------------------------------------------------------------------
def _text(value, field):
    limit = _MAX_LONG_TEXT if field in _LONG_FIELDS else _MAX_TEXT
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise CalculationArtifactError("%s: not a bounded non-empty string" % field)


def _date(value):
    if not isinstance(value, str) or not _ISO_DATE.fullmatch(value):
        raise CalculationArtifactError("inspection date malformed")


def _roles(entries, kinds, units_by_token, field):
    if not isinstance(entries, list) or not entries:
        raise CalculationArtifactError("%s: missing" % field)
    roles = {}
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != _ROLE_KEYS:
            raise CalculationArtifactError("%s: unexpected or missing field" % field)
        for key in _ROLE_KEYS:
            _text(entry[key], key)
        if entry["role"] in roles:
            raise CalculationArtifactError("%s: duplicate role" % field)
        if entry["quantity_kind"] not in kinds:
            raise CalculationArtifactError("%s: unknown quantity kind" % field)
        unit = units_by_token.get(entry["unit_token"])
        if unit is None or unit["quantity_kind"] != entry["quantity_kind"]:
            raise CalculationArtifactError("%s: unit not bound to the kind" % field)
        roles[entry["role"]] = entry
    return roles


def _conditions(entries, roles, field):
    if not isinstance(entries, list):
        raise CalculationArtifactError("%s: malformed" % field)
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != _CONDITION_KEYS:
            raise CalculationArtifactError("%s: unexpected or missing field" % field)
        if entry["condition"] not in _CONDITIONS:
            raise CalculationArtifactError("%s: unknown condition" % field)
        if entry["role"] not in roles:
            raise CalculationArtifactError("%s: unknown role" % field)
        if entry["condition"] == CONDITION_WITHIN_ZERO_AND_ROLE:
            if entry["bound_role"] is None:
                raise CalculationArtifactError("%s: bound role missing" % field)
        elif entry["bound_role"] is not None:
            raise CalculationArtifactError("%s: unexpected bound role" % field)


def validate_artifact(data):
    """Validate the WHOLE owner artifact or raise ``CalculationArtifactError``.
    Closed records, exact keys, unknown keys refused (calc/units contract §9).
    Returns ``data``."""
    if not isinstance(data, dict) or set(data) != _TOP_KEYS:
        raise CalculationArtifactError("artifact: unexpected or missing field")
    if data["artifact_id"] != ARTIFACT_ID \
            or data["schema_version"] != ARTIFACT_SCHEMA_VERSION:
        raise CalculationArtifactError("artifact: unknown identity or version")
    for field in ("artifact_version", "owner", "governance_note"):
        _text(data[field], field)

    kinds = {}
    if not isinstance(data["quantity_kinds"], list) or not data["quantity_kinds"]:
        raise CalculationArtifactError("quantity_kinds: missing")
    for kind in data["quantity_kinds"]:
        if not isinstance(kind, dict) or set(kind) != _KIND_KEYS:
            raise CalculationArtifactError("quantity_kinds: unexpected or missing field")
        _text(kind["quantity_kind"], "quantity_kind")
        _text(kind["dimension"], "dimension")
        if kind["quantity_kind"] in kinds:
            raise CalculationArtifactError("quantity_kinds: duplicate")
        kinds[kind["quantity_kind"]] = kind

    policies = {}
    if not isinstance(data["source_use_policies"], list) \
            or not data["source_use_policies"]:
        raise CalculationArtifactError("source_use_policies: missing")
    for policy in data["source_use_policies"]:
        if not isinstance(policy, dict) or set(policy) != _POLICY_KEYS:
            raise CalculationArtifactError(
                "source_use_policies: unexpected or missing field")
        for field in _POLICY_KEYS - {"inspection_date"}:
            _text(policy[field], field)
        _date(policy["inspection_date"])
        if policy["inspection_basis"] != "LEAD_SUPPLIED":
            raise CalculationArtifactError("source_use_policies: unknown basis")
        if policy["record_id"] in policies:
            raise CalculationArtifactError("source_use_policies: duplicate")
        policies[policy["record_id"]] = policy

    units = {}
    if not isinstance(data["unit_records"], list) or not data["unit_records"]:
        raise CalculationArtifactError("unit_records: missing")
    seen_ids = set()
    for unit in data["unit_records"]:
        if not isinstance(unit, dict) or set(unit) != _UNIT_KEYS:
            raise CalculationArtifactError("unit_records: unexpected or missing field")
        for field in _UNIT_KEYS - {"inspection_date"}:
            _text(unit[field], field)
        _date(unit["inspection_date"])
        if unit["inspection_basis"] != "LEAD_SUPPLIED":
            raise CalculationArtifactError("unit_records: unknown basis")
        if unit["quantity_kind"] not in kinds:
            raise CalculationArtifactError("unit_records: unknown quantity kind")
        if unit["source_use_policy_ref"] not in policies:
            raise CalculationArtifactError("unit_records: source-use unresolved")
        if unit["unit_token"] in units or unit["record_id"] in seen_ids:
            raise CalculationArtifactError("unit_records: duplicate")
        # No conversion and no alias in this increment: ONE unit token per
        # quantity kind, so a second spelling of a kind's unit cannot be admitted.
        if any(u["quantity_kind"] == unit["quantity_kind"] for u in units.values()):
            raise CalculationArtifactError("unit_records: alias or second unit for a kind")
        seen_ids.add(unit["record_id"])
        units[unit["unit_token"]] = unit

    methods = data["methods"]
    if not isinstance(methods, list) or not methods:
        raise CalculationArtifactError("methods: missing")
    seen_methods = set()
    for method in methods:
        if not isinstance(method, dict) or set(method) != _METHOD_KEYS:
            raise CalculationArtifactError("methods: unexpected or missing field")
        for field in ("method_id", "method_version", "adapter_identity",
                      "technical_authority"):
            _text(method[field], field)
        if method["method_id"] in seen_methods:
            raise CalculationArtifactError("methods: duplicate")
        seen_methods.add(method["method_id"])
        authority = method["method_authority_artifact"]
        if not isinstance(authority, dict) \
                or set(authority) != _AUTHORITY_ARTIFACT_KEYS:
            raise CalculationArtifactError("methods: authority reference malformed")
        _text(authority["artifact_id"], "artifact_id")
        _text(authority["artifact_version"], "artifact_version")
        qualification = method["source_qualification"]
        if not isinstance(qualification, list) or not qualification:
            raise CalculationArtifactError("methods: source qualification missing")
        for entry in qualification:
            if not isinstance(entry, dict) or set(entry) != _QUALIFICATION_KEYS:
                raise CalculationArtifactError(
                    "methods: source qualification malformed")
            for field in _QUALIFICATION_KEYS - {"inspection_date"}:
                _text(entry[field], field)
            _date(entry["inspection_date"])
            if entry["inspection_basis"] != "LEAD_SUPPLIED":
                raise CalculationArtifactError("methods: unknown inspection basis")
        inputs = _roles(method["input_roles"], kinds, units, "input_roles")
        outputs = _roles(method["output_roles"], kinds, units, "output_roles")
        if set(inputs) & set(outputs):
            raise CalculationArtifactError("methods: a role is both input and output")
        _conditions(method["applicability"], inputs, "applicability")
        for entry in method["applicability"]:
            if entry["bound_role"] is not None and entry["bound_role"] not in inputs:
                raise CalculationArtifactError("applicability: unknown bound role")
        _conditions(method["result_range"], outputs, "result_range")
        for entry in method["result_range"]:
            if entry["bound_role"] is not None and entry["bound_role"] not in inputs:
                raise CalculationArtifactError("result_range: unknown bound role")
    return data


def load_artifact(path=None):
    """Read and validate the committed owner artifact. A missing or unreadable
    file raises ``CalculationArtifactUnavailable``; an invalid one raises
    ``CalculationArtifactError``. Reads one local file only."""
    target = Path(path) if path is not None else ARTIFACT_PATH
    try:
        with open(target, encoding="utf-8") as handle:
            raw = handle.read()
    except OSError:
        raise CalculationArtifactUnavailable("artifact: unreadable") from None
    try:
        data = json.loads(raw)
    except ValueError:
        raise CalculationArtifactError("artifact: not valid JSON") from None
    return validate_artifact(data)


# ---------------------------------------------------------------------------
# the ONE immutable trusted binding (created by application wiring)
# ---------------------------------------------------------------------------
class MethodBinding:
    """One immutable binding of ONE method identity and version to ONE trusted
    adapter function, created once by application wiring. Not a registry: there
    is no lookup by name, no discovery, no module path and no mutation."""
    __slots__ = ("_method_id", "_method_version", "_adapter")

    def __init__(self, method_id, method_version, adapter):
        object.__setattr__(self, "_method_id", method_id)
        object.__setattr__(self, "_method_version", method_version)
        object.__setattr__(self, "_adapter", adapter)

    def __setattr__(self, name, value):
        raise AttributeError("MethodBinding is immutable")

    def __delattr__(self, name):
        raise AttributeError("MethodBinding is immutable")

    @property
    def method_id(self):
        return self._method_id

    @property
    def method_version(self):
        return self._method_version

    @property
    def adapter_identity(self):
        return _adapter_identity(self._adapter)


def _adapter_identity(adapter):
    if not isinstance(adapter, types.FunctionType):
        return None
    return "%s.%s" % (adapter.__module__, adapter.__qualname__)


def bind_method(method_id, method_version, adapter):
    """Create the ONE immutable binding. Pure: it reads no artifact and never
    raises for a wrong adapter - a binding whose adapter does not match the
    governed method record fails closed at execution (``EXECUTION_INTEGRITY_FAILURE``)."""
    return MethodBinding(method_id, method_version, adapter)


# ---------------------------------------------------------------------------
# execution
# ---------------------------------------------------------------------------
def _canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False)


def _digest(value):
    return hashlib.sha256(_canonical(value).encode("ascii")).hexdigest()


def _non_success(reason, identity=None):
    result = {"state": REASON_STATE[reason], "reason": reason, "outputs": None}
    if identity:
        result.update(identity)
    return result


def _is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _check(condition, value, bound):
    if condition == CONDITION_GREATER_THAN_ZERO:
        return value > 0.0
    return 0.0 <= value <= bound


def execute(binding, request, artifact_path=None):
    """Execute ONE admitted request through ONE trusted binding. Never raises.

    ``request`` is a plain dict: ``method_id``, ``method_version``, ``inputs``
    ({role: {"value": <typed number>, "unit": <exact token>}}) and ``subject_ref``
    (an opaque consumer reference echoed unchanged, or None). Strings are never
    parsed here. Returns a plain dict whose ``state`` is one of ``STATES`` and,
    for a non-success state, exactly one closed ``reason`` and ``outputs=None``.
    """
    if not isinstance(binding, MethodBinding):
        return _non_success(OPERATION_NOT_ADMITTED)
    if not isinstance(request, dict) or set(request) != _REQUEST_KEYS \
            or not isinstance(request["inputs"], dict) \
            or not (request["subject_ref"] is None
                    or isinstance(request["subject_ref"], str)):
        return _non_success(OPERATION_NOT_ADMITTED)
    if request["method_id"] != binding.method_id:
        return _non_success(OPERATION_NOT_ADMITTED)
    try:
        data = load_artifact(artifact_path)
    except CalculationArtifactUnavailable:
        return _non_success(SOURCE_UNAVAILABLE)
    except CalculationArtifactError:
        return _non_success(EXECUTION_INTEGRITY_FAILURE)
    record = next((m for m in data["methods"]
                   if m["method_id"] == binding.method_id), None)
    if record is None:
        return _non_success(METHOD_NOT_REGISTERED)
    if request["method_version"] != record["method_version"] \
            or binding.method_version != record["method_version"]:
        return _non_success(VERSION_MISMATCH)
    if binding.adapter_identity != record["adapter_identity"]:
        return _non_success(EXECUTION_INTEGRITY_FAILURE)
    identity = {
        "method_id": record["method_id"],
        "method_version": record["method_version"],
        "artifact_id": data["artifact_id"],
        "artifact_version": data["artifact_version"],
        "implementation_version": IMPLEMENTATION_VERSION,
    }

    units = {u["unit_token"]: u for u in data["unit_records"]}
    roles = {r["role"]: r for r in record["input_roles"]}
    inputs = request["inputs"]
    for role in inputs:
        if role not in roles:
            return _non_success(OPERATION_NOT_ADMITTED, identity)
    values = {}
    for role, spec in roles.items():
        given = inputs.get(role)
        if given is None:
            return _non_success(INPUT_MISSING, identity)
        if not isinstance(given, dict) or set(given) != _INPUT_KEYS:
            return _non_success(OPERATION_NOT_ADMITTED, identity)
        unit = given["unit"]
        if not isinstance(unit, str) or unit not in units:
            return _non_success(UNKNOWN_UNIT, identity)
        if unit != spec["unit_token"]:
            return _non_success(UNIT_NOT_ADMITTED, identity)
        value = given["value"]
        if not _is_number(value):
            return _non_success(INVALID_NUMERIC_INPUT, identity)
        try:
            number = float(value)
        except (OverflowError, ValueError, TypeError):
            return _non_success(INVALID_NUMERIC_INPUT, identity)
        if not math.isfinite(number):
            return _non_success(INVALID_NUMERIC_INPUT, identity)
        values[role] = number

    for condition in record["applicability"]:
        bound = values.get(condition["bound_role"]) \
            if condition["bound_role"] is not None else None
        if not _check(condition["condition"], values[condition["role"]], bound):
            return _non_success(INPUT_OUTSIDE_ADMITTED_RANGE, identity)

    try:
        produced = binding._adapter(**values)
    except Exception:  # noqa: BLE001 - any adapter fault fails closed
        return _non_success(EXECUTION_INTEGRITY_FAILURE, identity)
    output_roles = {r["role"]: r for r in record["output_roles"]}
    if not isinstance(produced, dict) or set(produced) != set(output_roles):
        return _non_success(EXECUTION_INTEGRITY_FAILURE, identity)
    outputs = {}
    for role, value in produced.items():
        if not isinstance(value, float) or not math.isfinite(value):
            return _non_success(EXECUTION_INTEGRITY_FAILURE, identity)
        outputs[role] = value
    for condition in record["result_range"]:
        bound = values.get(condition["bound_role"]) \
            if condition["bound_role"] is not None else None
        if not _check(condition["condition"], outputs[condition["role"]], bound):
            return _non_success(EXECUTION_INTEGRITY_FAILURE, identity)

    echoed = {role: {"value": values[role], "unit": roles[role]["unit_token"],
                     "provenance": PROVENANCE_OWNER_STATED}
              for role in roles}
    packaged = {role: {"value": outputs[role],
                       "unit": output_roles[role]["unit_token"],
                       "provenance": PROVENANCE_CALCULATED}
                for role in output_roles}
    request_digest = _digest({
        "method_id": request["method_id"],
        "method_version": request["method_version"],
        "inputs": {role: {"value": values[role], "unit": inputs[role]["unit"]}
                   for role in roles},
        "subject_ref": request["subject_ref"],
    })
    used_tokens = {r["unit_token"] for r in list(record["input_roles"])
                   + list(record["output_roles"])}
    unit_records = sorted(
        ({"record_id": units[t]["record_id"], "unit_token": t,
          "source_title": units[t]["source_title"],
          "edition": units[t]["edition"], "url": units[t]["url"]}
         for t in used_tokens), key=lambda u: u["record_id"])
    result = {
        "state": STATE_SUCCESS,
        "reason": None,
        "outputs": packaged,
        "inputs": echoed,
        "subject_ref": request["subject_ref"],
        "validation_status": VALIDATION_STATUS,
        "unit_records": unit_records,
        "source_qualification": [dict(q) for q in record["source_qualification"]],
        "request_digest": request_digest,
    }
    result.update(identity)
    result["result_identity"] = _digest({
        "request_digest": request_digest,
        "outputs": {role: packaged[role]["value"] for role in packaged},
        "identity": identity,
    })
    return result
