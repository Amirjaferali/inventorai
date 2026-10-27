"""Electrical / Electronics - DC resistive load power: the method-authority adapter.

Method authority: docs/governance/ELECTRICAL_DC_RESISTIVE_LOAD_POWER_METHOD_CONTRACT.md
(§3 method definition, §6 numeric domain and numerical acceptance). Identity
``electrical:dc_resistive_load_power``, version ``1.0`` (§2).

This module holds ONE pure deterministic function and nothing else: no request
handling, no unit handling, no I/O. It is handed to the shared calculation owner
once, by application wiring, as an immutable binding; the owner never imports it.

The relation is the electric power absorbed by a resistive element: with the
power relation P = V x I and Ohm's law I = V / R (DOE-HDBK-1011/1-92, recorded
as electronics_electrical:PR004), ``p_load = v_load ** 2 / r_load``. It is
restated independently; no DOE text is copied.

Role identifiers (§4): ``v_load`` (V, signed, the voltage across the load from
its declared + terminal to its declared - terminal), ``r_load`` (Ω, strictly
positive) and ``p_load`` (W, the power the load absorbs under the passive sign
convention; never negative for a positive resistance).

Numeric arrangement (documented, deterministic): the exact rational value of
``v_load ** 2 / r_load`` is formed from the two binary64 inputs and rounded ONCE
to binary64 (round half to even). A zero voltage (``0.0`` or ``-0.0``) gives the
exact rational zero and returns ``0.0`` exactly - never confused with an
underflow and never a negative zero. A nonzero exact result is accepted only
when the rounded value is finite, positive and within a relative error of
``2**-52`` of it. Overflow, underflow to zero of a nonzero result, an
out-of-bound result and any input outside the admitted domain raise
``ArithmeticError``; the owner turns that into
``FAILURE / EXECUTION_INTEGRITY_FAILURE`` with no numerical payload. This
acceptance rule belongs to this method only.
"""
import math
from fractions import Fraction

METHOD_ID = "electrical:dc_resistive_load_power"
METHOD_VERSION = "1.0"

# The accepted relative-error bound against the exact nonzero result (§6).
RELATIVE_ERROR_BOUND = Fraction(1, 2 ** 52)


def evaluate(v_load, r_load):
    """Return ``{"p_load": float}`` for admitted finite floats with
    ``r_load > 0``. Raises ``ArithmeticError`` on any integrity failure."""
    if not all(isinstance(v, float) and math.isfinite(v) for v in (v_load, r_load)):
        raise ArithmeticError("input not a finite float")
    if not r_load > 0.0:
        raise ArithmeticError("input outside the admitted domain")
    voltage = Fraction(v_load)
    exact = voltage * voltage / Fraction(r_load)
    if exact == 0:
        return {"p_load": 0.0}
    try:
        power = float(exact)
    except OverflowError:
        raise ArithmeticError("power overflows binary64") from None
    if not math.isfinite(power):
        raise ArithmeticError("non-finite power")
    if not power > 0.0:
        raise ArithmeticError("nonzero power underflowed or lost its sign")
    if abs(Fraction(power) - exact) > exact * RELATIVE_ERROR_BOUND:
        raise ArithmeticError("power outside the accepted relative error")
    return {"p_load": power}
