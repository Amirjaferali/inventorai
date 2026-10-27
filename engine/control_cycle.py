"""Stage 28 / 28-T4 - Single Vendor-Neutral Control-Cycle Evaluation - Slice 1.

Authority: docs/governance/STAGE28_T4_CONTROL_CYCLE_READY_RUNNING_CONTRACT.md
(§3 fixed definition and cycle order, §5 confirmations, §6 inputs, §7 outcomes
and refusal layering, §8 screen, §9 disclosure). Identity
``control_cycle:ready_running_single_transition``, version ``1.0``.

ONE optional, advisory, request-local evaluation of ONE fixed, fully declared,
non-safety control-state transition, on an Electrical / Electronics-root
project (eligibility is decided in the web layer):

  1. freeze the one Boolean input ``start_input``;
  2. read the one previous state;
  3. evaluate the one transition (READY -> RUNNING when start_input is true)
     against the previous state and the frozen input;
  4. select the next state - the target when the transition applies and its
     condition holds, otherwise the previous state;
  5. calculate the one Boolean output as ``output_map[next_state]``.

The definition is FIXED by its governed artifact and pinned here: there is no
client-supplied state, transition, condition, expression, callback or output
map, and no generic state-machine framework, scheduler or rule engine. Reading
the output from the next state is InventorAI's own design decision, not a
claimed OpenPLC, PLC or IEC 61131-3 execution semantic. A transition that does
not fire is a routine result, never a refusal.

What this module owns: the governed artifact and its fail-closed validation
(duplicate keys, unknown keys, a changed vocabulary, a missing or contradictory
output map, a transition whose source or target is unknown, and any semantic
edit all fail closed); strict capture of the submitted form; the pre-evaluation
order; and the evaluation itself. It is not a method of the shared deterministic
calculation owner, persists nothing, keeps no state between calls, reads no
project, session, store, answer, component or SafetySignal, and has no network,
provider, model, clock or randomness dependency. Nothing here is a device
command, a safety function, an interlock or evidence.
"""
import hashlib
import json
import re
from pathlib import Path

METHOD_ID = "control_cycle:ready_running_single_transition"
METHOD_VERSION = "1.0"

ARTIFACT_ID = "control_cycle_ready_running_single_transition"
ARTIFACT_SCHEMA_VERSION = "1.0"
ARTIFACT_PATH = (Path(__file__).resolve().parent.parent / "docs" / "governance"
                 / "control_cycle_content_config"
                 / "ready_running_single_transition_v1.json")

# The trusted durable root domain that makes a project eligible (§1).
ELIGIBLE_ROOT_DOMAIN = "electronics_electrical"

# The fixed definition (§3), pinned here AND in the governed artifact; the two
# must agree exactly, or the evaluation fails closed.
STATE_READY = "READY"
STATE_RUNNING = "RUNNING"
STATES = (STATE_READY, STATE_RUNNING)
INPUT_NAME = "start_input"
OUTPUT_NAME = "output"
DEFINITION = {
    "states": [STATE_READY, STATE_RUNNING],
    "input": {"name": INPUT_NAME, "type": "boolean"},
    "transitions": [
        {"source": STATE_READY, "condition": {"input": INPUT_NAME, "equals": True},
         "target": STATE_RUNNING}],
    "output": {"name": OUTPUT_NAME, "type": "boolean"},
    "output_map": {STATE_READY: False, STATE_RUNNING: True},
}

# Transition status of a successful evaluation (§7). All three are routine.
TRANSITION_APPLIED = "APPLIED"
TRANSITION_CONDITION_FALSE = "NOT_APPLIED_CONDITION_FALSE"
TRANSITION_NOT_APPLICABLE = "NOT_APPLICABLE_FROM_STATE"
TRANSITION_STATUSES = (TRANSITION_APPLIED, TRANSITION_CONDITION_FALSE,
                       TRANSITION_NOT_APPLICABLE)

# §5 confirmations D-1 to D-5, in contract order. Any answer other than
# "applies" refuses MODEL_NOT_SUPPORTED.
DECLARATIONS = (
    ("two_states", "D-1"),
    ("one_transition", "D-2"),
    ("output_meaning", "D-3"),
    ("one_frozen_input", "D-4"),
    ("logical_only", "D-5"),
)
DECLARATION_IDS = tuple(d for d, _ in DECLARATIONS)
_CONTRACT_REF = dict(DECLARATIONS)

# §8 six-item high-risk screen, in contract order.
SCREEN_ITEMS = ("safety_function", "machinery_motion", "mains_or_high_voltage",
                "heating_or_fire", "medical_or_life_supporting",
                "vehicle_or_aerospace")

ANSWER_APPLIES = "applies"
ANSWER_DOES_NOT_APPLY = "does_not_apply"
SCREEN_YES = "yes"
SCREEN_NO = "no"
INPUT_TRUE = "true"
INPUT_FALSE = "false"

DECLARATION_FIELD = "decl_%s"
SCREEN_FIELD = "screen_%s"
PREVIOUS_STATE_FIELD = "previous_state"
INPUT_FIELD = "start_input"
FORM_FIELDS = frozenset(
    ["csrf_token", PREVIOUS_STATE_FIELD, INPUT_FIELD]
    + [DECLARATION_FIELD % d for d in DECLARATION_IDS]
    + [SCREEN_FIELD % s for s in SCREEN_ITEMS])

# Outcomes (§7).
OUTCOME_SUCCESS = "SUCCESS"
NOT_DECLARED = "NOT_DECLARED"
ENGINEERING_REVIEW_REQUIRED = "ENGINEERING_REVIEW_REQUIRED"
MODEL_NOT_SUPPORTED = "MODEL_NOT_SUPPORTED"
UNKNOWN_STATE = "UNKNOWN_STATE"
INVALID_INPUT_SNAPSHOT = "INVALID_INPUT_SNAPSHOT"
DEFINITION_UNAVAILABLE = "DEFINITION_UNAVAILABLE"
OUTCOMES = (OUTCOME_SUCCESS, NOT_DECLARED, ENGINEERING_REVIEW_REQUIRED,
            MODEL_NOT_SUPPORTED, UNKNOWN_STATE, INVALID_INPUT_SNAPSHOT,
            DEFINITION_UNAVAILABLE)

VALIDATION_STATUS = "UNVALIDATED"

_MAX_TEXT = 1500
_LONG_FIELDS = frozenset({"governance_note", "inspected_content"})
_MAX_LONG_TEXT = 2000
_ISO_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
_TOP_KEYS = frozenset({
    "artifact_id", "schema_version", "artifact_version", "owner", "slice",
    "governance_note", "method", "definition", "declarations", "screen_items",
    "limitations", "disclosure", "sources"})
_METHOD_KEYS = frozenset({"method_id", "method_version", "contract", "cycle_order",
                          "output_rule", "no_transition_rule"})
_DEFINITION_KEYS = frozenset({"states", "input", "transitions", "output",
                              "output_map"})
_SIGNAL_KEYS = frozenset({"name", "type"})
_TRANSITION_KEYS = frozenset({"source", "condition", "target"})
_CONDITION_KEYS = frozenset({"input", "equals"})
_DECL_KEYS = frozenset({"declaration_id", "contract_ref", "accepted_value",
                        "refusal"})
_SCREEN_KEYS = frozenset({"item_id", "item"})
_SOURCE_KEYS = frozenset({
    "record_id", "record_type", "source_type", "publisher", "source_title",
    "url", "source_use_policy_ref", "inspection_basis", "inspection_date",
    "inspected_content", "paraphrase_only_limitation",
    "third_party_material_exclusion", "no_endorsement_limitation"})
_POLICY_EXTRA_KEYS = frozenset({"acknowledgement"})
_DISCLOSURE_ITEMS = 7
_SOURCE_POLICY = {"OPENPLC-S1": "oplc:SU001"}

# The accepted governed meaning of artifact version "1", pinned per section: the
# SHA-256 of each section's canonical JSON (sorted keys, compact, ASCII). Any
# semantic edit fails closed even when every key and id survives; changing the
# definition needs a new version under its own authorization.
_SEMANTIC_DIGESTS = {
    "method": "6c1e947724606490c6d543e3b02982f5dfa55a7f0505a9875f2405836a340b57",
    "definition": "a82ff7218811d45d2e0217f7e033efab4960595ea28ebad763faac728452dd47",
    "declarations": "bfa505124346fdd478802f6c0c42104bf40ed02a6799be2941497ac6ef4f11c6",
    "screen_items": "0a279eb393307c02b33ed654b6134728b1378889a356f71bc15a3ae9f2d39e5e",
    "limitations": "0f3791e7e1e5e8226199e90a6ce21b0472745f7e23e1b87f83a2ff40f0d46e89",
    "disclosure": "a4b8ae2bcc423e83ef69a0fbdc773fefa25538064d4df491daee5e12f37e1db6",
    "sources": "1554f57a78239826e7a9eb0f1cea5aa2a325838d29181b6df85ba900321c8d69",
}
_PINNED_ARTIFACT_VERSION = "1"


class ControlCycleDefinitionError(ValueError):
    """The governed definition is missing, unreadable, ambiguous or not valid.
    The evaluation turns this into ``DEFINITION_UNAVAILABLE`` and evaluates
    nothing. The message names structure only, never content."""


def _section_digest(value):
    canonical = json.dumps(value, sort_keys=True, separators=(",", ":"),
                           ensure_ascii=True)
    return hashlib.sha256(canonical.encode("ascii")).hexdigest()


def is_eligible(root_domain):
    """True iff the trusted durable root domain makes a project eligible (§1).
    Pure; anything but the exact token is ineligible."""
    return isinstance(root_domain, str) and root_domain == ELIGIBLE_ROOT_DOMAIN


def _text(value, field):
    limit = _MAX_LONG_TEXT if field in _LONG_FIELDS else _MAX_TEXT
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise ControlCycleDefinitionError("%s: not a bounded non-empty string" % field)


def _no_duplicate_keys(pairs):
    """``json`` object hook: a key given twice in one object (for example two
    output-map entries for one state) is an ambiguous rule representation."""
    result = {}
    for key, value in pairs:
        if key in result:
            raise ControlCycleDefinitionError("definition: duplicate key")
        result[key] = value
    return result


def validate_definition(definition):
    """Validate the fixed definition or raise ``ControlCycleDefinitionError``:
    exact keys; exactly the two-state vocabulary, without duplicates; one
    Boolean input; exactly one transition whose source and target are known,
    distinct states and whose condition reads that input against a Boolean;
    one Boolean output; and an output map with exactly one Boolean entry per
    state. Then it must equal the pinned ``DEFINITION``, so a contradictory
    definition cannot be evaluated. Returns ``definition``."""
    if not isinstance(definition, dict) or set(definition) != _DEFINITION_KEYS:
        raise ControlCycleDefinitionError("definition: unexpected or missing field")
    states = definition["states"]
    if not isinstance(states, list) or len(set(states)) != len(states) \
            or any(not isinstance(s, str) for s in states):
        raise ControlCycleDefinitionError("definition: states malformed or duplicated")
    if tuple(states) != STATES:
        raise ControlCycleDefinitionError("definition: unsupported state vocabulary")
    for signal in (definition["input"], definition["output"]):
        if not isinstance(signal, dict) or set(signal) != _SIGNAL_KEYS \
                or signal["type"] != "boolean":
            raise ControlCycleDefinitionError("definition: signal malformed")
    transitions = definition["transitions"]
    if not isinstance(transitions, list) or len(transitions) != 1:
        raise ControlCycleDefinitionError("definition: not exactly one transition")
    transition = transitions[0]
    if not isinstance(transition, dict) or set(transition) != _TRANSITION_KEYS:
        raise ControlCycleDefinitionError("definition: transition malformed")
    if transition["source"] not in states or transition["target"] not in states \
            or transition["source"] == transition["target"]:
        raise ControlCycleDefinitionError("definition: transition states unknown")
    condition = transition["condition"]
    if not isinstance(condition, dict) or set(condition) != _CONDITION_KEYS \
            or condition["input"] != definition["input"]["name"] \
            or not isinstance(condition["equals"], bool):
        raise ControlCycleDefinitionError("definition: condition malformed")
    output_map = definition["output_map"]
    if not isinstance(output_map, dict) or set(output_map) != set(states) \
            or any(not isinstance(v, bool) for v in output_map.values()):
        raise ControlCycleDefinitionError("definition: output map incomplete")
    if definition != DEFINITION:
        raise ControlCycleDefinitionError("definition: contradicts the pinned definition")
    return definition


def validate_artifact(data):
    """Validate the WHOLE governed artifact or raise
    ``ControlCycleDefinitionError``. Returns ``data``."""
    if not isinstance(data, dict) or set(data) != _TOP_KEYS:
        raise ControlCycleDefinitionError("artifact: unexpected or missing field")
    if data["artifact_id"] != ARTIFACT_ID \
            or data["schema_version"] != ARTIFACT_SCHEMA_VERSION:
        raise ControlCycleDefinitionError("artifact: unknown identity or version")
    for field in ("artifact_version", "owner", "slice", "governance_note"):
        _text(data[field], field)
    method = data["method"]
    if not isinstance(method, dict) or set(method) != _METHOD_KEYS:
        raise ControlCycleDefinitionError("method: unexpected or missing field")
    for field in _METHOD_KEYS:
        _text(method[field], field)
    if method["method_id"] != METHOD_ID or method["method_version"] != METHOD_VERSION:
        raise ControlCycleDefinitionError("method: unknown identity or version")
    validate_definition(data["definition"])
    decls = data["declarations"]
    if not isinstance(decls, list) \
            or [d.get("declaration_id") if isinstance(d, dict) else None
                for d in decls] != list(DECLARATION_IDS):
        raise ControlCycleDefinitionError("declarations: not the §5 set")
    for entry in decls:
        if set(entry) != _DECL_KEYS:
            raise ControlCycleDefinitionError("declarations: unexpected or missing field")
        _text(entry["accepted_value"], "accepted_value")
        if entry["contract_ref"] != _CONTRACT_REF[entry["declaration_id"]] \
                or entry["refusal"] != MODEL_NOT_SUPPORTED:
            raise ControlCycleDefinitionError("declarations: refusal mapping changed")
    items = data["screen_items"]
    if not isinstance(items, list) \
            or [i.get("item_id") if isinstance(i, dict) else None
                for i in items] != list(SCREEN_ITEMS):
        raise ControlCycleDefinitionError("screen_items: not the §8 set")
    for entry in items:
        if set(entry) != _SCREEN_KEYS:
            raise ControlCycleDefinitionError("screen_items: unexpected or missing field")
        _text(entry["item"], "item")
    if not isinstance(data["limitations"], list) or not data["limitations"]:
        raise ControlCycleDefinitionError("limitations: missing")
    for entry in data["limitations"]:
        _text(entry, "limitation")
    disclosure = data["disclosure"]
    if not isinstance(disclosure, list) or len(disclosure) != _DISCLOSURE_ITEMS:
        raise ControlCycleDefinitionError("disclosure: not the seven §9 requirements")
    for entry in disclosure:
        _text(entry, "disclosure")
    sources = data["sources"]
    if not isinstance(sources, list) or not sources:
        raise ControlCycleDefinitionError("sources: missing")
    by_id = {}
    for record in sources:
        if not isinstance(record, dict):
            raise ControlCycleDefinitionError("sources: not an object")
        record_type = record.get("record_type")
        allowed = _SOURCE_KEYS | (_POLICY_EXTRA_KEYS
                                  if record_type == "source_use_policy"
                                  else frozenset())
        if set(record) != allowed:
            raise ControlCycleDefinitionError("sources: unexpected or missing field")
        if record_type not in ("source", "source_use_policy"):
            raise ControlCycleDefinitionError("sources: unknown record type")
        for field in allowed - {"record_type"}:
            _text(record[field], field)
        if not _ISO_DATE.fullmatch(record["inspection_date"]):
            raise ControlCycleDefinitionError("sources: inspection date malformed")
        if record["inspection_basis"] != "LEAD_SUPPLIED":
            raise ControlCycleDefinitionError("sources: unknown inspection basis")
        if record["record_id"] in by_id:
            raise ControlCycleDefinitionError("sources: duplicate record id")
        by_id[record["record_id"]] = record
    for source_id, policy_id in _SOURCE_POLICY.items():
        policy = by_id.get(policy_id)
        if policy is None or policy["record_type"] != "source_use_policy":
            raise ControlCycleDefinitionError("sources: source-use record missing")
        record = by_id.get(source_id)
        if record is None or record["record_type"] != "source" \
                or record["source_use_policy_ref"] != policy_id:
            raise ControlCycleDefinitionError("sources: source unresolved")
    if data["artifact_version"] != _PINNED_ARTIFACT_VERSION:
        raise ControlCycleDefinitionError("artifact: unpinned version")
    for section, expected in _SEMANTIC_DIGESTS.items():
        if _section_digest(data[section]) != expected:
            raise ControlCycleDefinitionError("%s: governed content changed" % section)
    return data


def load_artifact(path=None):
    """Read and validate the committed artifact, refusing a key given twice in
    any object. Any failure raises ``ControlCycleDefinitionError``. Reads one
    local file only."""
    target = Path(path) if path is not None else ARTIFACT_PATH
    try:
        with open(target, encoding="utf-8") as handle:
            data = json.load(handle, object_pairs_hook=_no_duplicate_keys)
    except (OSError, ValueError):
        raise ControlCycleDefinitionError("artifact: unreadable") from None
    return validate_artifact(data)


def capture_form(form):
    """Strict capture of one submission.

    ``form`` is a mapping whose values are lists of strings (a request multi-dict
    flattened with ``getlist``). Returns ``None`` for a MALFORMED request: an
    unknown field (including any attempt to supply a state, transition,
    condition, target or output), a field sent more than once, or an answer
    outside its closed choices (a previous state outside READY / RUNNING, an
    input other than true / false). An absent or empty answer is NOT malformed;
    it is unanswered, which the evaluation reports as ``NOT_DECLARED``.
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
    previous = flat.get(PREVIOUS_STATE_FIELD, "")
    if previous not in ("",) + STATES:
        return None
    snapshot = flat.get(INPUT_FIELD, "")
    if snapshot not in ("", INPUT_TRUE, INPUT_FALSE):
        return None
    return {"declarations": declarations, "screen": screen,
            "previous_state": previous, "start_input": snapshot}


def evaluate_cycle(previous_state, start_input, definition=None):
    """The five-step cycle of §3 for ONE previous state and ONE Boolean input,
    against the pinned definition. Pure; never raises; keeps nothing.

    Returns ``{"outcome": SUCCESS, ...}`` with the previous state, the frozen
    input, the transition status, whether it was applied, the next state and
    the Boolean output; or ``{"outcome": <refusal>}`` with no state or output
    for an invalid definition, an unknown previous state or an input that is
    not exactly ``True`` or ``False``."""
    try:
        validate_definition(DEFINITION if definition is None else definition)
    except ControlCycleDefinitionError:
        return {"outcome": DEFINITION_UNAVAILABLE}
    # 1. freeze the input: exactly a bool, read once and held for the cycle.
    if type(start_input) is not bool:
        return {"outcome": INVALID_INPUT_SNAPSHOT}
    frozen = bool(start_input)
    # 2. read the previous state.
    if not isinstance(previous_state, str) or previous_state not in STATES:
        return {"outcome": UNKNOWN_STATE}
    # 3. evaluate the one transition against the previous state and frozen input.
    (transition,) = DEFINITION["transitions"]
    if previous_state != transition["source"]:
        status, next_state = TRANSITION_NOT_APPLICABLE, previous_state
    elif frozen == transition["condition"]["equals"]:
        status, next_state = TRANSITION_APPLIED, transition["target"]
    else:
        status, next_state = TRANSITION_CONDITION_FALSE, previous_state
    # 4. / 5. the next state is selected; the output is read from it.
    return {
        "outcome": OUTCOME_SUCCESS,
        "previous_state": previous_state,
        "frozen_input": frozen,
        "transition_status": status,
        "transition_applied": status == TRANSITION_APPLIED,
        "next_state": next_state,
        "output": DEFINITION["output_map"][next_state],
        "method_id": METHOD_ID,
        "method_version": METHOD_VERSION,
        "validation_status": VALIDATION_STATUS,
    }


def evaluate(captured, artifact=None):
    """Run the §7 order for ONE captured submission. Never raises.

    Request integrity, authorization, eligibility and malformed requests belong
    to the web layer and have already passed. Then, first failing stage alone
    wins: governed definition -> completeness (every confirmation, screen item,
    the previous state and the input answered) -> high-risk screen ->
    confirmations D-1 to D-5 -> the cycle. No stage after a failing one is
    evaluated, and no state or output accompanies a non-success outcome."""
    try:
        if artifact is None:
            load_artifact()
        else:
            validate_artifact(artifact)
    except ControlCycleDefinitionError:
        return {"outcome": DEFINITION_UNAVAILABLE}
    declarations = captured["declarations"]
    screen = captured["screen"]
    if any(declarations[d] == "" for d in DECLARATION_IDS) \
            or any(screen[s] == "" for s in SCREEN_ITEMS) \
            or captured["previous_state"] == "" or captured["start_input"] == "":
        return {"outcome": NOT_DECLARED}
    if any(screen[s] == SCREEN_YES for s in SCREEN_ITEMS):
        return {"outcome": ENGINEERING_REVIEW_REQUIRED}
    if any(declarations[d] != ANSWER_APPLIES for d in DECLARATION_IDS):
        return {"outcome": MODEL_NOT_SUPPORTED}
    snapshot = {INPUT_TRUE: True, INPUT_FALSE: False}.get(captured["start_input"])
    if snapshot is None:
        return {"outcome": INVALID_INPUT_SNAPSHOT}
    return evaluate_cycle(captured["previous_state"], snapshot)
