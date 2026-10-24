"""Sensors / Instrumentation C3 - TMP36 nominal voltage-to-temperature: the method-authority adapter.

Method authority: docs/governance/SENSORS_C3_TMP36_NOMINAL_VOLTAGE_TO_TEMPERATURE_METHOD_CONTRACT.md
(§3 method definition, §6 numeric domain and numerical acceptance). Identity
``tmp36:nominal_voltage_to_temperature``, version ``1.0`` (§2).

This module holds ONE pure deterministic function and nothing else: no request
handling, no unit handling, no I/O. It is handed to the shared calculation owner
once, by application wiring, as an immutable binding; the owner never imports it.

The relation is restated independently from the nominal TMP36 output
characteristic of the Analog Devices TMP35/TMP36/TMP37 data sheet, Rev. H
(offset 500 mV, scale 10 mV/°C): ``T = (V_OUT - 500) / 10``. No data-sheet text,
table, figure or code is copied.

Role identifiers (§4): ``v_out`` (mV, the inventor-declared TMP36 output voltage,
within the nominal-model interval 100 to 1750 mV inclusive) and ``t_celsius``
(°C, signed, the NOMINAL temperature of the relation; never a measured, accurate
or guaranteed device temperature).

Numeric arrangement (documented, deterministic): the exact rational value of
``(v_out - 500) / 10`` is formed from the binary64 input and rounded ONCE to
binary64 (round half to even). An input of exactly 500 mV gives the exact
rational zero and returns ``0.0`` exactly. A nonzero exact result is accepted
only when the rounded value is finite, nonzero, of the exact result's sign,
within a relative error of ``2**-52`` of it and inside the nominal temperature
interval. An input outside the nominal-model interval never reaches this
function from the page (the consumer refuses it from the exact decimal first);
here it raises ``ArithmeticError``, as does any other integrity failure, and the
owner turns that into ``FAILURE / EXECUTION_INTEGRITY_FAILURE`` with no
numerical payload. This acceptance rule belongs to this method only.
"""
import math
from fractions import Fraction

METHOD_ID = "tmp36:nominal_voltage_to_temperature"
METHOD_VERSION = "1.0"

# The nominal TMP36 output characteristic (§3): offset in mV and scale in mV/°C.
OFFSET_MV = 500
SCALE_MV_PER_C = 10

# The nominal-model input interval in mV and the temperature interval it maps
# to in °C (§6). Both ends are exactly representable in binary64.
V_MIN_MV = 100
V_MAX_MV = 1750
T_MIN_C = -40
T_MAX_C = 125

# The accepted relative-error bound against the exact nonzero result (§6).
RELATIVE_ERROR_BOUND = Fraction(1, 2 ** 52)


def evaluate(v_out):
    """Return ``{"t_celsius": float}`` for an admitted finite float ``v_out``
    with ``100 <= v_out <= 1750``. Raises ``ArithmeticError`` on any integrity
    failure."""
    if not (isinstance(v_out, float) and math.isfinite(v_out)):
        raise ArithmeticError("input not a finite float")
    if not (V_MIN_MV <= v_out <= V_MAX_MV):
        raise ArithmeticError("input outside the nominal-model interval")
    exact = (Fraction(v_out) - OFFSET_MV) / SCALE_MV_PER_C
    if exact == 0:
        return {"t_celsius": 0.0}
    t_celsius = float(exact)
    if not math.isfinite(t_celsius) or t_celsius == 0.0:
        raise ArithmeticError("temperature not finite and nonzero")
    if (t_celsius < 0.0) != (exact < 0):
        raise ArithmeticError("temperature sign changed")
    if abs(Fraction(t_celsius) - exact) > abs(exact) * RELATIVE_ERROR_BOUND:
        raise ArithmeticError("temperature outside the accepted relative error")
    if not (T_MIN_C <= t_celsius <= T_MAX_C):
        raise ArithmeticError("temperature outside the nominal interval")
    return {"t_celsius": t_celsius}
