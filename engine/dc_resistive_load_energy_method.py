"""Electrical / Electronics - DC resistive load energy: the method-authority adapter.

Method authority: docs/governance/ELECTRICAL_DC_RESISTIVE_LOAD_ENERGY_METHOD_CONTRACT.md
(§3 method definition, §6 numeric domain and numerical acceptance). Identity
``electrical:dc_resistive_load_energy``, version ``1.0`` (§2).

This module holds ONE pure deterministic function and nothing else: no request
handling, no unit handling, no I/O. It is handed to the shared calculation owner
once, by application wiring, as an immutable binding; the owner never imports it.

The relation is the electrical energy absorbed by a resistive element held at a
constant power for a declared duration: with the power relation P = V x I and
Ohm's law I = V / R (DOE-HDBK-1011/1-92, recorded as
electronics_electrical:PR004) the absorbed power is V ** 2 / R, and with power
the rate at which energy is transferred (DOE-HDBK-1010-92, recorded as
electronics_electrical:PR008) a power that stays constant throughout the
duration t gives the energy E = P x t, so
``e_load = v_load ** 2 * t_duration / r_load``. It is restated independently;
no DOE text is copied.

Role identifiers (§4): ``v_load`` (V, signed, the voltage across the load from
its declared + terminal to its declared - terminal), ``r_load`` (Ω, strictly
positive), ``t_duration`` (s, not negative) and ``e_load`` (J, the energy the
load absorbs under the passive sign convention; never negative for a positive
resistance and a duration that is not negative).

Numeric arrangement (documented, deterministic): the exact rational value of
``v_load ** 2 * t_duration / r_load`` is formed from the three binary64 inputs
and rounded ONCE to binary64 (round half to even). A zero voltage or a zero
duration (``0.0`` or ``-0.0``) gives the exact rational zero and returns ``0.0``
exactly - never confused with an underflow and never a negative zero. A nonzero
exact result is accepted only when the rounded value is finite, positive and
within a relative error of ``2**-52`` of it. Overflow, underflow to zero of a
nonzero result, an out-of-bound result and any input outside the admitted
domain (a resistance that is not positive or a negative duration) raise
``ArithmeticError``; the owner turns that into
``FAILURE / EXECUTION_INTEGRITY_FAILURE`` with no numerical payload. This
acceptance rule belongs to this method only.
"""
import math
from fractions import Fraction

METHOD_ID = "electrical:dc_resistive_load_energy"
METHOD_VERSION = "1.0"

# The accepted relative-error bound against the exact nonzero result (§6).
RELATIVE_ERROR_BOUND = Fraction(1, 2 ** 52)


def evaluate(v_load, r_load, t_duration):
    """Return ``{"e_load": float}`` for admitted finite floats with
    ``r_load > 0`` and ``t_duration >= 0``. Raises ``ArithmeticError`` on any
    integrity failure."""
    if not all(isinstance(v, float) and math.isfinite(v)
               for v in (v_load, r_load, t_duration)):
        raise ArithmeticError("input not a finite float")
    if not r_load > 0.0 or not t_duration >= 0.0:
        raise ArithmeticError("input outside the admitted domain")
    voltage = Fraction(v_load)
    exact = voltage * voltage * Fraction(t_duration) / Fraction(r_load)
    if exact == 0:
        return {"e_load": 0.0}
    try:
        energy = float(exact)
    except OverflowError:
        raise ArithmeticError("energy overflows binary64") from None
    if not math.isfinite(energy):
        raise ArithmeticError("non-finite energy")
    if not energy > 0.0:
        raise ArithmeticError("nonzero energy underflowed or lost its sign")
    if abs(Fraction(energy) - exact) > exact * RELATIVE_ERROR_BOUND:
        raise ArithmeticError("energy outside the accepted relative error")
    return {"e_load": energy}
