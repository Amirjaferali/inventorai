"""Stage 27 / THERM-01 - single-path conduction temperature difference: the method-authority adapter.

Method authority: docs/governance/STAGE27_THERM01_CONDUCTION_TEMPERATURE_DIFFERENCE_METHOD_CONTRACT.md
(§3 method definition and derivation, §6 numeric domain). Identity
``therm01:conduction_temperature_difference_single_path``, version ``1.0`` (§2).

This module holds ONE pure deterministic function and nothing else: no request
handling, no unit handling, no I/O. It is handed to the shared calculation owner
once, by application wiring, as an immutable binding; the owner never imports it.

Role identifiers (§4): ``P`` is the heat flow in W, ``R_theta`` is the ASCII role
identifier of ``Rθ`` (the inventor-supplied total thermal resistance in K/W) and
``delta_T`` is the ASCII role identifier of ``ΔT`` (a temperature difference in
K). The identifiers are implementation details, never aliases of the roles.

Numeric representation (documented, deterministic): inputs are IEEE-754 binary64
floats, already admitted by the owner as finite and strictly positive. The ONE
executed operation is ``delta_T = P * R_theta``: no subtraction, no tolerance, no
rounding, no clamping and no magnitude ceiling (§3, §6). A product that overflows
to infinity is not finite and raises ``ArithmeticError``; the owner turns that into
``FAILURE / EXECUTION_INTEGRITY_FAILURE`` with no numerical payload (§6). A
product that underflows to zero is returned as computed and fails the owner's
governed result-range check (``delta_T > 0``), which is likewise
``FAILURE / EXECUTION_INTEGRITY_FAILURE``: a positive heat flow through a positive
resistance never yields a zero temperature difference.
"""
import math

METHOD_ID = "therm01:conduction_temperature_difference_single_path"
METHOD_VERSION = "1.0"


def evaluate(P, R_theta):
    """Return ``{"delta_T": float}`` for admitted finite floats with ``P > 0`` and
    ``R_theta > 0``. Raises ``ArithmeticError`` on any integrity failure."""
    delta_t = P * R_theta
    if not math.isfinite(delta_t):
        raise ArithmeticError("non-finite temperature difference")
    return {"delta_T": delta_t}
