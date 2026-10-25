"""Electrical / Electronics - DC resistive load current: the method-authority adapter.

Method authority: docs/governance/ELECTRICAL_DC_RESISTIVE_LOAD_CURRENT_METHOD_CONTRACT.md
(§3 method definition, §6 numeric domain and numerical acceptance). Identity
``electrical:dc_resistive_load_current``, version ``1.0`` (§2).

This module holds ONE pure deterministic function and nothing else: no request
handling, no unit handling, no I/O. It is handed to the shared calculation owner
once, by application wiring, as an immutable binding; the owner never imports it.

The relation is Ohm's law for a resistive element (DOE-HDBK-1011/1-92, recorded
as electronics_electrical:PR004), solved for the current:
``i_load = v_load / r_load``. It is restated independently; no DOE text is copied.

Role identifiers (§4): ``v_load`` (V, signed, the voltage across the load from
its declared + terminal to its declared - terminal), ``r_load`` (Ω, strictly
positive) and ``i_load`` (A, signed: positive for current through the load from
the + terminal to the - terminal, the same reference direction as the voltage).

Numeric arrangement (documented, deterministic): the exact rational value of
``v_load / r_load`` is formed from the two binary64 inputs and rounded ONCE to
binary64 (round half to even). A zero voltage gives the exact rational zero and
returns ``0.0`` exactly - never confused with an underflow. A nonzero exact
result is accepted only when the rounded value is finite, nonzero, of the exact
result's sign and within a relative error of ``2**-52`` of it. Overflow,
underflow to zero of a nonzero result, an out-of-bound result and any input
outside the admitted domain raise ``ArithmeticError``; the owner turns that into
``FAILURE / EXECUTION_INTEGRITY_FAILURE`` with no numerical payload. This
acceptance rule belongs to this method only.
"""
import math
from fractions import Fraction

METHOD_ID = "electrical:dc_resistive_load_current"
METHOD_VERSION = "1.0"

# The accepted relative-error bound against the exact nonzero result (§6).
RELATIVE_ERROR_BOUND = Fraction(1, 2 ** 52)


def evaluate(v_load, r_load):
    """Return ``{"i_load": float}`` for admitted finite floats with
    ``r_load > 0``. Raises ``ArithmeticError`` on any integrity failure."""
    if not all(isinstance(v, float) and math.isfinite(v) for v in (v_load, r_load)):
        raise ArithmeticError("input not a finite float")
    if not r_load > 0.0:
        raise ArithmeticError("input outside the admitted domain")
    exact = Fraction(v_load) / Fraction(r_load)
    if exact == 0:
        return {"i_load": 0.0}
    try:
        current = float(exact)
    except OverflowError:
        raise ArithmeticError("current overflows binary64") from None
    if not math.isfinite(current):
        raise ArithmeticError("non-finite current")
    if current == 0.0:
        raise ArithmeticError("nonzero current underflowed to zero")
    if (current < 0.0) != (exact < 0):
        raise ArithmeticError("current sign changed")
    if abs(Fraction(current) - exact) > abs(exact) * RELATIVE_ERROR_BOUND:
        raise ArithmeticError("current outside the accepted relative error")
    return {"i_load": current}
