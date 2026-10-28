"""Electrical / Electronics - PWM average voltage: the method-authority adapter.

Method authority: docs/governance/ELECTRICAL_PWM_AVERAGE_VOLTAGE_METHOD_CONTRACT.md
(§3 method definition, §6 numeric domain and numerical acceptance). Identity
``electrical:pwm_average_voltage``, version ``1.0`` (§2).

This module holds ONE pure deterministic function and nothing else: no request
handling, no unit handling, no I/O. It is handed to the shared calculation owner
once, by application wiring, as an immutable binding; the owner never imports it.

The relation is the arithmetic time-average, over one period, of an ideal
periodic two-level voltage waveform that equals the declared supply level
``v_supply`` during the on-interval ``t_on`` and zero for the remainder of the
period ``t_period``: a periodic voltage equal to E for an interval and zero
otherwise has an average proportional to the on-time fraction (NASA TN
D-5643, recorded as the method's NASA-PWM-S1), which InventorAI restates as
``v_avg = v_supply * t_on / t_period``. It is restated independently; no NASA
text is copied. The adapter infers nothing about any load: the result is the
waveform average only, never an equivalent DC voltage, a load response, an
average power, an RMS value, a current, a ripple or a filtered output.

Role identifiers (§4): ``v_supply`` (V, not negative: the waveform switches
between zero and the declared supply level, never a bipolar waveform),
``t_on`` (s, within zero and the period inclusive), ``t_period`` (s, strictly
positive) and ``v_avg`` (V, never negative, never above ``v_supply``).

Numeric arrangement (documented, deterministic): the exact rational value of
``v_supply * t_on / t_period`` is formed from the three binary64 inputs and
rounded ONCE to binary64 (round half to even). A zero supply level or a zero
on-time (``0.0`` or ``-0.0``) gives the exact rational zero and returns ``0.0``
exactly - never confused with an underflow and never a negative zero. An
on-time equal to the period gives exactly ``v_supply``. A nonzero exact result
is accepted only when the rounded value is finite, positive and within a
relative error of ``2**-52`` of it. Overflow, underflow to zero of a nonzero
result, an out-of-bound result and any input outside the admitted domain (a
negative supply level, a period that is not positive, a negative on-time or an
on-time above the period) raise ``ArithmeticError``; the owner turns that into
``FAILURE / EXECUTION_INTEGRITY_FAILURE`` with no numerical payload. This
acceptance rule belongs to this method only.
"""
import math
from fractions import Fraction

METHOD_ID = "electrical:pwm_average_voltage"
METHOD_VERSION = "1.0"

# The accepted relative-error bound against the exact nonzero result (§6).
RELATIVE_ERROR_BOUND = Fraction(1, 2 ** 52)


def evaluate(v_supply, t_on, t_period):
    """Return ``{"v_avg": float}`` for admitted finite floats with
    ``v_supply >= 0``, ``t_period > 0`` and ``0 <= t_on <= t_period``. Raises
    ``ArithmeticError`` on any integrity failure."""
    if not all(isinstance(v, float) and math.isfinite(v)
               for v in (v_supply, t_on, t_period)):
        raise ArithmeticError("input not a finite float")
    if not v_supply >= 0.0 or not t_period > 0.0 \
            or not t_on >= 0.0 or not t_on <= t_period:
        raise ArithmeticError("input outside the admitted domain")
    exact = Fraction(v_supply) * Fraction(t_on) / Fraction(t_period)
    if exact == 0:
        return {"v_avg": 0.0}
    try:
        average = float(exact)
    except OverflowError:
        raise ArithmeticError("average overflows binary64") from None
    if not math.isfinite(average):
        raise ArithmeticError("non-finite average")
    if not average > 0.0:
        raise ArithmeticError("nonzero average underflowed or lost its sign")
    if abs(Fraction(average) - exact) > exact * RELATIVE_ERROR_BOUND:
        raise ArithmeticError("average outside the accepted relative error")
    return {"v_avg": average}
