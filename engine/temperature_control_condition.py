"""TEMPERATURE-TO-CONTROL-CONDITION-01 - Slice 1: TMP36 nominal temperature -> threshold -> one READY / RUNNING cycle.

Authority: docs/governance/TEMPERATURE_TO_CONTROL_CONDITION_COMPOSITION_CONTRACT.md,
with the named consumer exceptions it records in the TMP36 method contract (§1A)
and the 28-T4 control-cycle contract (§6A). Identity
``temperature_control_condition:tmp36_threshold_ready_running``, version ``1.0``.

ONE optional, advisory, request-local composition of two existing evaluations,
in this fixed order and within one request:

  1. the EXISTING TMP36 consumer (``engine/tmp36_nominal_temperature.py``)
     evaluates the inventor-declared output voltage with its own declarations,
     screen, interval, binary and decimal-reference acceptance and refusals;
  2. the inventor-declared Celsius threshold is read as an exact decimal inside
     -40 °C to +125 °C;
  3. the ONE fixed condition ``nominal_temperature_C >= threshold_C`` is
     evaluated on the EXACT decimal values (the accepted nominal temperature the
     TMP36 consumer returns, never a float and never display text);
  4. only the resulting Boolean is passed as ``start_input`` to the EXISTING
     28-T4 evaluator (``engine/control_cycle.py``), which runs its own
     confirmations, screen and five-step cycle unchanged.

What this module owns: strict capture of the combined form (each part's fields
carry a fixed prefix and are handed to that part's own capture unchanged; a
client can never submit ``start_input``), the threshold grammar and range, the
one comparison, the composition's own confirmation and the order of the stages.
It owns no equation, state table, output map or refusal rule of either part:
any refusal of either part ends the composition with no temperature, condition,
state or output - never a partial success. It persists nothing, keeps no state
between calls, reads no project, session, store or SafetySignal, and has no
network, provider, model, clock or randomness dependency. Nothing here is a
measurement, a thermostat, a controller, a device command, a safety function or
evidence.
"""
import re
from fractions import Fraction

from engine import control_cycle as _cc
from engine import tmp36_nominal_temperature as _tmp36

COMPOSITION_ID = "temperature_control_condition:tmp36_threshold_ready_running"
COMPOSITION_VERSION = "1.0"

# Eligibility is the INTERSECTION of the two existing gates (decided in the web
# layer); both name this root domain, and the 28-T4 gate admits the root only.
ELIGIBLE_ROOT_DOMAIN = _cc.ELIGIBLE_ROOT_DOMAIN

# The fixed threshold interval in °C, inclusive (the TMP36 nominal-model
# temperature range), and the threshold grammar: an optional single leading
# minus, digits and at most four fractional digits (the resolution of an
# admitted nominal temperature). A representation rule only.
THRESHOLD_MIN_C = Fraction(-40)
THRESHOLD_MAX_C = Fraction(125)
THRESHOLD_FRACTION_DIGITS = 4
MAX_THRESHOLD_CHARS = 64
_THRESHOLD = re.compile(r"-?[0-9]+(?:\.[0-9]{1,%d})?" % THRESHOLD_FRACTION_DIGITS,
                        re.ASCII)

# The composition's own confirmation (contract §5).
CONDITION_DECLARATION = "condition_meaning"
DECLARATION_FIELD = "decl_%s" % CONDITION_DECLARATION
THRESHOLD_FIELD = "threshold_c"
TMP36_PREFIX = "t_"
CYCLE_PREFIX = "c_"
_TMP36_FIELDS = frozenset(_tmp36.FORM_FIELDS) - {"csrf_token"}
# start_input is NEVER a client field here: it is derived from the condition.
_CYCLE_FIELDS = frozenset(_cc.FORM_FIELDS) - {"csrf_token", _cc.INPUT_FIELD}
FORM_FIELDS = frozenset(
    ["csrf_token", DECLARATION_FIELD, THRESHOLD_FIELD]
    + [TMP36_PREFIX + f for f in _TMP36_FIELDS]
    + [CYCLE_PREFIX + f for f in _CYCLE_FIELDS])

ANSWER_APPLIES = _cc.ANSWER_APPLIES
ANSWER_DOES_NOT_APPLY = _cc.ANSWER_DOES_NOT_APPLY

# Composition outcomes (contract §7). A part's refusal is carried with the
# part's own outcome token, preserved, never rewritten.
OUTCOME_SUCCESS = "SUCCESS"
NOT_DECLARED = "NOT_DECLARED"
MODEL_NOT_SUPPORTED = "MODEL_NOT_SUPPORTED"
INVALID_THRESHOLD = "INVALID_THRESHOLD"
THRESHOLD_OUTSIDE_RANGE = "THRESHOLD_OUTSIDE_RANGE"
TMP36_REFUSED = "TMP36_REFUSED"
CONTROL_CYCLE_REFUSED = "CONTROL_CYCLE_REFUSED"
OUTCOMES = (OUTCOME_SUCCESS, NOT_DECLARED, MODEL_NOT_SUPPORTED, INVALID_THRESHOLD,
            THRESHOLD_OUTSIDE_RANGE, TMP36_REFUSED, CONTROL_CYCLE_REFUSED)

VALIDATION_STATUS = "UNVALIDATED"


def is_eligible(root_domain):
    """True iff BOTH parts' root rules admit the trusted durable root domain.
    Pure. The web layer additionally requires the TMP36 gate itself, so the
    composition is the intersection of the two existing gates."""
    return _tmp36.is_eligible(root_domain) and _cc.is_eligible(root_domain)


def capture_form(form):
    """Strict capture of one combined submission, or ``None`` when MALFORMED:
    an unknown field (including ``start_input`` under any spelling, or any field
    without its part's prefix), a field sent more than once, or a value the
    owning part's own capture refuses. Each part's fields are stripped of their
    prefix and handed to that part's ``capture_form`` unchanged. Returns
    ``{"tmp36", "cycle", "condition_meaning", "threshold"}``."""
    if not isinstance(form, dict) or set(form) - FORM_FIELDS:
        return None
    for values in form.values():
        if not isinstance(values, list) or len(values) != 1 \
                or not isinstance(values[0], str):
            return None
    tmp36_form = {k[len(TMP36_PREFIX):]: v for k, v in form.items()
                  if k.startswith(TMP36_PREFIX)}
    cycle_form = {k[len(CYCLE_PREFIX):]: v for k, v in form.items()
                  if k.startswith(CYCLE_PREFIX)}
    tmp36_captured = _tmp36.capture_form(tmp36_form)
    cycle_captured = _cc.capture_form(cycle_form)
    if tmp36_captured is None or cycle_captured is None:
        return None
    meaning = form.get(DECLARATION_FIELD, [""])[0]
    if meaning not in ("", ANSWER_APPLIES, ANSWER_DOES_NOT_APPLY):
        return None
    return {"tmp36": tmp36_captured, "cycle": cycle_captured,
            "condition_meaning": meaning,
            "threshold": form.get(THRESHOLD_FIELD, [""])[0]}


def parse_threshold(text):
    """The EXACT decimal value (a ``Fraction``) of a strict ASCII decimal with an
    optional single leading minus and at most four fractional digits, or
    ``None``. Nothing is rounded."""
    if not isinstance(text, str) or len(text) > MAX_THRESHOLD_CHARS \
            or not _THRESHOLD.fullmatch(text):
        return None
    return Fraction(text)


def condition_holds(nominal_temperature, threshold):
    """The ONE fixed condition ``nominal_temperature_C >= threshold_C`` on exact
    ``Fraction`` values only; anything else is refused by raising."""
    if not isinstance(nominal_temperature, Fraction) \
            or not isinstance(threshold, Fraction):
        raise TypeError("exact Fraction values required")
    return nominal_temperature >= threshold


def _refused(outcome, part_outcome=None):
    return {"outcome": outcome, "part_outcome": part_outcome}


def evaluate(captured, tmp36_binding):
    """Run the composition for ONE captured submission. Never raises.

    Request integrity, authorization, eligibility and malformed requests belong
    to the web layer and have already passed. First failing stage alone wins:
    composition completeness -> composition confirmation -> threshold grammar ->
    threshold range -> the TMP36 consumer (its own full order) -> the fixed
    condition -> the 28-T4 evaluator (its own full order, with the derived
    start_input). A refusal carries no temperature, condition, state or output."""
    if captured["condition_meaning"] == "" or captured["threshold"] == "":
        return _refused(NOT_DECLARED)
    if captured["condition_meaning"] != ANSWER_APPLIES:
        return _refused(MODEL_NOT_SUPPORTED)
    threshold = parse_threshold(captured["threshold"])
    if threshold is None:
        return _refused(INVALID_THRESHOLD)
    if not THRESHOLD_MIN_C <= threshold <= THRESHOLD_MAX_C:
        return _refused(THRESHOLD_OUTSIDE_RANGE)
    temperature = _tmp36.evaluate(captured["tmp36"], tmp36_binding)
    nominal = temperature.get("nominal_temperature")
    if temperature.get("outcome") != _tmp36.OUTCOME_SUCCESS \
            or not isinstance(nominal, Fraction):
        part = temperature.get("outcome")
        return _refused(TMP36_REFUSED,
                        part if part != _tmp36.OUTCOME_SUCCESS
                        else _tmp36.KNOWLEDGE_UNAVAILABLE)
    condition = condition_holds(nominal, threshold)
    cycle_captured = dict(captured["cycle"])
    cycle_captured["start_input"] = _cc.INPUT_TRUE if condition else _cc.INPUT_FALSE
    cycle = _cc.evaluate(cycle_captured)
    if cycle.get("outcome") != _cc.OUTCOME_SUCCESS \
            or cycle.get("frozen_input") is not condition:
        part = cycle.get("outcome")
        return _refused(CONTROL_CYCLE_REFUSED,
                        part if part != _cc.OUTCOME_SUCCESS
                        else _cc.DEFINITION_UNAVAILABLE)
    owner = temperature["result"]
    return {
        "outcome": OUTCOME_SUCCESS,
        "part_outcome": None,
        "declared_voltage_text": captured["tmp36"]["values"]["v_out"],
        "nominal_temperature": nominal,
        "nominal_temperature_display": temperature["display_value"],
        "nominal_temperature_unit": owner["outputs"]["t_celsius"]["unit"],
        "threshold": threshold,
        "threshold_text": captured["threshold"],
        "condition": condition,
        "start_input": cycle["frozen_input"],
        "previous_state": cycle["previous_state"],
        "transition_status": cycle["transition_status"],
        "transition_applied": cycle["transition_applied"],
        "next_state": cycle["next_state"],
        "output": cycle["output"],
        "temperature_method": (owner["method_id"], owner["method_version"]),
        "cycle_method": (cycle["method_id"], cycle["method_version"]),
        "composition": (COMPOSITION_ID, COMPOSITION_VERSION),
        "validation_status": VALIDATION_STATUS,
    }
