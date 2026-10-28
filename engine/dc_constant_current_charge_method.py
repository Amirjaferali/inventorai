"""Electrical / Electronics - DC constant-current charge: the method-authority adapter.

Method authority: docs/governance/ELECTRICAL_DC_CONSTANT_CURRENT_CHARGE_METHOD_CONTRACT.md
(§3 method definition, §6 numeric domain and numerical acceptance). Identity
``electrical:dc_constant_current_charge``, version ``1.0`` (§2).

This module holds ONE pure deterministic function and nothing else: no request
handling, no unit handling, no I/O. It is handed to the shared calculation owner
once, by application wiring, as an immutable binding; the owner never imports it.

The relation is the electric charge that flows through one load while one DC
current stays constant for one declared duration: electric current is the flow
of electric charge, one ampere being one coulomb passing a point per second
(DOE-HDBK-1011/1-92, recorded as electronics_electrical:PR018), so for a current
``i_load`` that stays constant throughout the duration ``t_duration`` the charge
that flows is ``q_load = i_load * t_duration``. The product is InventorAI's own
algebraic restatement under that explicit constant-current restriction; it is
not claimed that DOE prints the integrated form, and no varying-current,
average-current or integration treatment is derived. With the current in
amperes and the duration in hours the product is in ampere hours (A·h), the
unit the request declares; this adapter performs no conversion (no coulomb, no
milliampere hour, no second).

Role identifiers (§4): ``i_load`` (A, not negative, the constant current
through the load), ``t_duration`` (h, not negative) and ``q_load`` (A·h, the
charge that flows through the load during the declared duration; never
negative).

Numeric arrangement (documented, deterministic): the exact rational value of
``i_load * t_duration`` is formed from the two binary64 inputs and rounded ONCE
to binary64 (round half to even). A zero current or a zero duration (``0.0`` or
``-0.0``) gives the exact rational zero and returns ``0.0`` exactly - never
confused with an underflow and never a negative zero. A nonzero exact result is
accepted only when the rounded value is finite, positive and within a relative
error of ``2**-52`` of it. Overflow, underflow to zero of a nonzero result, an
out-of-bound result and any input outside the admitted domain (a negative
current or a negative duration) raise ``ArithmeticError``; the owner turns that
into ``FAILURE / EXECUTION_INTEGRITY_FAILURE`` with no numerical payload. This
acceptance rule belongs to this method only.
"""
import math
from fractions import Fraction

METHOD_ID = "electrical:dc_constant_current_charge"
METHOD_VERSION = "1.0"

# The accepted relative-error bound against the exact nonzero result (§6).
RELATIVE_ERROR_BOUND = Fraction(1, 2 ** 52)


def evaluate(i_load, t_duration):
    """Return ``{"q_load": float}`` for admitted finite floats with
    ``i_load >= 0`` and ``t_duration >= 0``. Raises ``ArithmeticError`` on any
    integrity failure."""
    if not all(isinstance(v, float) and math.isfinite(v)
               for v in (i_load, t_duration)):
        raise ArithmeticError("input not a finite float")
    if not i_load >= 0.0 or not t_duration >= 0.0:
        raise ArithmeticError("input outside the admitted domain")
    exact = Fraction(i_load) * Fraction(t_duration)
    if exact == 0:
        return {"q_load": 0.0}
    try:
        charge = float(exact)
    except OverflowError:
        raise ArithmeticError("charge overflows binary64") from None
    if not math.isfinite(charge):
        raise ArithmeticError("non-finite charge")
    if not charge > 0.0:
        raise ArithmeticError("nonzero charge underflowed or lost its sign")
    if abs(Fraction(charge) - exact) > exact * RELATIVE_ERROR_BOUND:
        raise ArithmeticError("charge outside the accepted relative error")
    return {"q_load": charge}
