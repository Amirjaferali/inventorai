"""Stage 25 / CAP-13 - planar single-force moment: the method-authority adapter.

Method authority: docs/governance/STAGE25_CAP13_PLANAR_SINGLE_FORCE_MOMENT_METHOD_CONTRACT.md
(§3 method definition, §6 numeric domain and numerical acceptance). Identity
``cap13:planar_single_force_moment``, version ``1.0`` (§2).

This module holds ONE pure deterministic function and nothing else: no request
handling, no unit handling, no I/O. It is handed to the shared calculation owner
once, by application wiring, as an immutable binding; the owner never imports it.

Role identifiers (§4): ``F`` is the force magnitude in N, ``d_perp`` is the ASCII
role identifier of ``d⊥`` (the perpendicular distance in mm from the inventor's
chosen point to the force's line of action) and ``M`` is the moment magnitude in
N·mm. The identifiers are implementation details, never aliases of the roles.

Numeric representation (documented, deterministic): inputs are IEEE-754 binary64
floats, already admitted by the owner as finite and strictly positive. The ONE
executed operation is ``M = F * d_perp``: no tolerance widening, no rounding, no
clamping and no magnitude ceiling (§3, §6).

Numerical acceptance (§6): the computed product is accepted ONLY when it is
finite, strictly positive and within a relative error of ``2**-52`` of the EXACT
mathematical product of the two actual binary input values, checked with exact
rational arithmetic. A correctly rounded binary64 product meets that bound for
every normal result; a subnormal result is accepted when it meets the same bound
(an exact subnormal product always does) and is never refused merely for being
subnormal. Overflow to infinity, underflow to zero and a subnormal result whose
rounding error exceeds the bound raise ``ArithmeticError``; the owner turns that
into ``FAILURE / EXECUTION_INTEGRITY_FAILURE`` with no numerical payload. A zero
input never reaches this function: it is refused before execution.
"""
import math
from fractions import Fraction

METHOD_ID = "cap13:planar_single_force_moment"
METHOD_VERSION = "1.0"

# The accepted relative-error bound against the exact product (§6).
RELATIVE_ERROR_BOUND = Fraction(1, 2 ** 52)


def evaluate(F, d_perp):
    """Return ``{"M": float}`` for admitted finite floats with ``F > 0`` and
    ``d_perp > 0``. Raises ``ArithmeticError`` on any integrity failure."""
    if not (isinstance(F, float) and isinstance(d_perp, float)
            and math.isfinite(F) and math.isfinite(d_perp)
            and F > 0.0 and d_perp > 0.0):
        raise ArithmeticError("input outside the admitted domain")
    moment = F * d_perp
    if not math.isfinite(moment):
        raise ArithmeticError("non-finite moment")
    if moment <= 0.0:
        raise ArithmeticError("moment underflowed to zero")
    exact = Fraction(F) * Fraction(d_perp)
    if abs(Fraction(moment) - exact) > exact * RELATIVE_ERROR_BOUND:
        raise ArithmeticError("moment outside the accepted relative error")
    return {"M": moment}
