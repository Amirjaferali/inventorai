"""Stage 25 / CAP-13 - planar required force: the method-authority adapter.

Method authority: docs/governance/STAGE25_CAP13_PLANAR_REQUIRED_FORCE_METHOD_CONTRACT.md
(§3 method definition, §6 numeric domain and numerical acceptance). Identity
``cap13:planar_required_force``, version ``1.0`` (§2).

This module holds ONE pure deterministic function and nothing else: no request
handling, no unit handling, no I/O. It is handed to the shared calculation owner
once, by application wiring, as an immutable binding; the owner never imports it.

The relation is the moment of a force about a point - the force multiplied by
the perpendicular distance from the point to its line of action (NASA-S1,
NASA-T1) - solved for the force: ``F = M_target / d_perp``. The rearrangement is
InventorAI's own restatement; no NASA text is copied.

Role identifiers (§4): ``M_target`` (N·mm, the inventor's own target moment
magnitude, zero or more), ``d_perp`` (mm, the ASCII role identifier of ``d⊥``,
strictly positive) and ``F`` (N, the magnitude of the one force that would
produce that moment at that distance).

Numeric arrangement (documented, deterministic): the exact rational value of
``M_target / d_perp`` is formed from the two binary64 inputs and rounded ONCE to
binary64 (round half to even). A zero target moment gives the exact rational
zero and returns ``0.0`` exactly - never confused with an underflow. A nonzero
exact result is accepted only when the rounded value is finite, strictly
positive and within a relative error of ``2**-52`` of it. Overflow, underflow to
zero of a nonzero result, an out-of-bound result and any input outside the
admitted domain raise ``ArithmeticError``; the owner turns that into
``FAILURE / EXECUTION_INTEGRITY_FAILURE`` with no numerical payload. This
acceptance rule belongs to this method only.
"""
import math
from fractions import Fraction

METHOD_ID = "cap13:planar_required_force"
METHOD_VERSION = "1.0"

# The accepted relative-error bound against the exact nonzero result (§6).
RELATIVE_ERROR_BOUND = Fraction(1, 2 ** 52)


def evaluate(M_target, d_perp):
    """Return ``{"F": float}`` for admitted finite floats with
    ``M_target >= 0`` and ``d_perp > 0``. Raises ``ArithmeticError`` on any
    integrity failure."""
    if not all(isinstance(v, float) and math.isfinite(v) for v in (M_target, d_perp)):
        raise ArithmeticError("input not a finite float")
    if not (M_target >= 0.0 and d_perp > 0.0):
        raise ArithmeticError("input outside the admitted domain")
    exact = Fraction(M_target) / Fraction(d_perp)
    if exact == 0:
        return {"F": 0.0}
    try:
        force = float(exact)
    except OverflowError:
        raise ArithmeticError("force overflows binary64") from None
    if not math.isfinite(force):
        raise ArithmeticError("non-finite force")
    if force <= 0.0:
        raise ArithmeticError("nonzero force underflowed to zero")
    if abs(Fraction(force) - exact) > exact * RELATIVE_ERROR_BOUND:
        raise ArithmeticError("force outside the accepted relative error")
    return {"F": force}
