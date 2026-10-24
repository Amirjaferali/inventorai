"""Stage 25 / CAP-13 - linear speed-dependent rotational load: the method-authority adapter.

Method authority: docs/governance/STAGE25_CAP13_LINEAR_SPEED_DEPENDENT_ROTATIONAL_LOAD_METHOD_CONTRACT.md
(§3 method definition, §6 numeric domain and numerical acceptance). Identity
``cap13:linear_speed_dependent_rotational_load``, version ``1.0`` (§2).

This module holds ONE pure deterministic function and nothing else: no request
handling, no unit handling, no I/O. It is handed to the shared calculation owner
once, by application wiring, as an immutable binding; the owner never imports it.

The mathematical relation is a fact independently restated from the scientific
reference (Modelica Standard Library v4.1.0,
``Modelica.Mechanics.Rotational.Sources.LinearSpeedDependentTorque`` with
``TorqueDirection=false``): ``tau = tau_nominal * (w / w_nominal)``. No Modelica
code is copied or executed.

Role identifiers (§4): ``tau_nominal`` (N·m, strictly negative: a resisting
load), ``w_nominal`` (rad/s, strictly positive), ``w`` (rad/s, signed, zero
valid) and ``tau`` (N·m, signed): the accelerating torque the load applies at the
shaft, positive in the positive direction of rotation (Modelica ``-flange.tau``).

Numeric arrangement (documented, deterministic): the exact rational value of
``tau_nominal * w / w_nominal`` is formed from the three binary64 inputs and
rounded ONCE to binary64 (round half to even), so no intermediate product or
quotient can overflow, underflow or round. A zero operating speed gives the
exact rational zero and returns ``0.0`` exactly - never confused with an
underflow. A nonzero exact result is accepted only when the rounded value is
finite, nonzero, of the exact result's sign and within a relative error of
``2**-52`` of it; a subnormal result is accepted only when it meets that bound.
Overflow, underflow to zero of a nonzero result, an out-of-bound result and any
input outside the admitted domain raise ``ArithmeticError``; the owner turns
that into ``FAILURE / EXECUTION_INTEGRITY_FAILURE`` with no numerical payload.
This acceptance rule belongs to this method only.
"""
import math
from fractions import Fraction

METHOD_ID = "cap13:linear_speed_dependent_rotational_load"
METHOD_VERSION = "1.0"

# The accepted relative-error bound against the exact nonzero result (§6).
RELATIVE_ERROR_BOUND = Fraction(1, 2 ** 52)


def evaluate(tau_nominal, w_nominal, w):
    """Return ``{"tau": float}`` for admitted finite floats with
    ``tau_nominal < 0``, ``w_nominal > 0`` and finite ``w``. Raises
    ``ArithmeticError`` on any integrity failure."""
    if not all(isinstance(v, float) and math.isfinite(v)
               for v in (tau_nominal, w_nominal, w)):
        raise ArithmeticError("input not a finite float")
    if not (tau_nominal < 0.0 and w_nominal > 0.0):
        raise ArithmeticError("input outside the admitted domain")
    exact = Fraction(tau_nominal) * Fraction(w) / Fraction(w_nominal)
    if exact == 0:
        return {"tau": 0.0}
    try:
        tau = float(exact)
    except OverflowError:
        raise ArithmeticError("torque overflows binary64") from None
    if not math.isfinite(tau):
        raise ArithmeticError("non-finite torque")
    if tau == 0.0:
        raise ArithmeticError("nonzero torque underflowed to zero")
    if (tau < 0.0) != (exact < 0):
        raise ArithmeticError("torque sign changed")
    if abs(Fraction(tau) - exact) > abs(exact) * RELATIVE_ERROR_BOUND:
        raise ArithmeticError("torque outside the accepted relative error")
    return {"tau": tau}
