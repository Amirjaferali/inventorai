"""Stage 25 / CAP-13 - two-support static reactions: the method-authority adapter.

Method authority: docs/governance/STAGE25_CAP13_TWO_SUPPORT_STATIC_REACTIONS_METHOD_CONTRACT.md
(§4 method definition, §7 numeric domain). Identity ``cap13:static_reactions_two_support``,
version ``1.0`` (§2).

This module holds ONE pure deterministic function and nothing else: no request
handling, no unit handling, no I/O. It is handed to the shared calculation owner
once, by application wiring, as an immutable binding; the owner never imports it.

Numeric representation and evaluation order (documented, deterministic):
  inputs are IEEE-754 binary64 floats, already admitted by the owner;
  ``ratio_right = x / L`` and ``ratio_left = (L - x) / L`` are evaluated first,
  then ``R_R = P * ratio_right`` and ``R_L = P * ratio_left``.
This grouping is the accepted executed form ``R_R = P × x / L``,
``R_L = P × (L − x) / L`` (§4) evaluated with the ratio first: each ratio lies in
[0, 1] inside the admitted domain, so neither product can exceed ``P`` and no
intermediate can overflow. Each reaction comes from its own expression; neither
is derived by subtracting the other, and no force-balance tolerance check is
made (§4). The endpoints stay exact: at ``x = 0`` the left ratio is ``L / L = 1``
and the right ratio ``0``; at ``x = L`` the right ratio is ``1`` and the left
``0``. No rounding is applied.

A non-finite intermediate or output, or an interior configuration
(``0 < x < L``) whose reactions collapse to zero through representation limits,
raises ``ArithmeticError``; the owner turns that into
``FAILURE / EXECUTION_INTEGRITY_FAILURE`` with no numerical payload.
"""
import math

METHOD_ID = "cap13:static_reactions_two_support"
METHOD_VERSION = "1.0"


def evaluate(P, L, x):
    """Return ``{"R_L": float, "R_R": float}`` for admitted finite floats with
    ``P > 0``, ``L > 0`` and ``0 <= x <= L``. Raises ``ArithmeticError`` on any
    integrity failure."""
    ratio_right = x / L
    ratio_left = (L - x) / L
    if not (math.isfinite(ratio_right) and math.isfinite(ratio_left)):
        raise ArithmeticError("non-finite intermediate")
    reaction_right = P * ratio_right
    reaction_left = P * ratio_left
    if not (math.isfinite(reaction_right) and math.isfinite(reaction_left)):
        raise ArithmeticError("non-finite reaction")
    if 0.0 < x < L and (reaction_right <= 0.0 or reaction_left <= 0.0):
        raise ArithmeticError("interior reaction collapsed")
    return {"R_L": reaction_left, "R_R": reaction_right}
