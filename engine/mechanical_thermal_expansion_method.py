"""Mechanical - free linear thermal expansion: the method-authority adapter.

Method authority: docs/governance/MECHANICAL_FREE_LINEAR_THERMAL_EXPANSION_METHOD_CONTRACT.md
(§3 method definition and derivation, §6 numeric domain and numerical
acceptance). Identity ``mechanical:free_linear_thermal_expansion``, version
``1.0`` (§2).

This module holds ONE pure deterministic function and nothing else: no request
handling, no unit handling, no I/O. It is handed to the shared calculation owner
once, by application wiring, as an immutable binding; the owner never imports it.

The relation is the FREE change in length of ONE unrestrained length of ONE
material over a declared temperature change. NBS Circular 486 (Hidnert and
Souder, 1950; recorded as NBS-TE-S1) defines the average coefficient of linear
expansion over a temperature range, and records that the change in length
depends on the original length and on the temperature range; restated by
InventorAI for exactly the declared interval and the length the coefficient
refers to, ``delta_L = alpha_avg * L_ref * delta_T``. No NBS text or data is
copied, and no coefficient value exists here.

Role identifiers (§4): ``alpha_avg`` (1/K, strictly positive), ``L_ref`` (mm,
strictly positive), ``delta_T`` (K, signed: final minus initial temperature)
and ``delta_L`` (mm, signed: positive lengthens, negative shortens).

Numeric arrangement (documented, deterministic; §6): the exact rational value
of ``alpha_avg * L_ref * delta_T`` is formed from the three binary64 inputs and
rounded ONCE to binary64 (round half to even). A zero temperature change
(``0.0`` or ``-0.0``) gives the exact rational zero and returns ``0.0`` exactly -
never a negative zero and never confused with an underflow. A nonzero exact
result is accepted only when the rounded value is finite, nonzero, of the same
sign as the exact value and within a relative error of ``2**-52`` of it.
Overflow, underflow to zero of a nonzero result, a sign change, an out-of-bound
result and any input outside the admitted domain (a coefficient or a length
that is not positive) raise ``ArithmeticError``; the owner turns that into
``FAILURE / EXECUTION_INTEGRITY_FAILURE`` with no numerical payload. This
acceptance rule belongs to this method only.
"""
import math
from fractions import Fraction

METHOD_ID = "mechanical:free_linear_thermal_expansion"
METHOD_VERSION = "1.0"

# The accepted relative-error bound against the exact nonzero result (§6).
RELATIVE_ERROR_BOUND = Fraction(1, 2 ** 52)


def evaluate(alpha_avg, L_ref, delta_T):
    """Return ``{"delta_L": float}`` for admitted finite floats with
    ``alpha_avg > 0`` and ``L_ref > 0``. Raises ``ArithmeticError`` on any
    integrity failure."""
    if not all(isinstance(v, float) and math.isfinite(v)
               for v in (alpha_avg, L_ref, delta_T)):
        raise ArithmeticError("input not a finite float")
    if not alpha_avg > 0.0 or not L_ref > 0.0:
        raise ArithmeticError("input outside the admitted domain")
    exact = Fraction(alpha_avg) * Fraction(L_ref) * Fraction(delta_T)
    if exact == 0:
        return {"delta_L": 0.0}
    try:
        change = float(exact)
    except OverflowError:
        raise ArithmeticError("change in length overflows binary64") from None
    if not math.isfinite(change):
        raise ArithmeticError("non-finite change in length")
    if change == 0.0 or (change > 0.0) != (exact > 0):
        raise ArithmeticError("nonzero change in length underflowed or lost its sign")
    if abs(Fraction(change) - exact) > abs(exact) * RELATIVE_ERROR_BOUND:
        raise ArithmeticError("change in length outside the accepted relative error")
    return {"delta_L": change}
