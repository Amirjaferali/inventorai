"""Mechanical - planar centered rectangular clearance: the method-authority adapter.

Method authority: docs/governance/MECHANICAL_PLANAR_CENTERED_RECTANGULAR_CLEARANCE_METHOD_CONTRACT.md
(§3 method definition and derivation, §6 numeric domain and numerical
acceptance). Identity ``mechanical:planar_centered_rectangular_clearance``,
version ``1.0`` (§2).

This module holds ONE pure deterministic function and nothing else: no request
handling, no unit handling, no I/O, no geometric verdict. It is handed to the
shared calculation owner once, by application wiring, as an immutable binding;
the owner never imports it.

The relation is InventorAI's own derivation (no external text, table or code):
ONE rectangular board outline placed centered and axis-aligned in ONE rectangular
usable region at the board plane leaves, on each axis, half of the difference
between the region and the board on each side; subtracting the required
clearance per side gives the margin on that axis:

    margin_x = (region_x - board_x) / 2 - c
    margin_y = (region_y - board_y) / 2 - c

Role identifiers (§4): ``board_x``, ``board_y``, ``region_x``, ``region_y`` (mm,
strictly positive), ``c`` (mm, zero or positive) and the outputs ``margin_x``,
``margin_y`` (mm, signed: negative means the declared clearance is not
available on that axis).

Numeric arrangement (documented, deterministic; §6): each margin is the exact
rational value of the expression over the binary64 inputs, rounded ONCE to
binary64 (round half to even). An exact zero returns ``0.0`` exactly (never a
negative zero). A nonzero exact margin is accepted only when the rounded value
is finite, nonzero, of the same sign as the exact value and within a relative
error of ``2**-53`` of it (one correct rounding). Anything else, and any input
outside the admitted domain, raises ``ArithmeticError``; the owner turns that
into ``FAILURE / EXECUTION_INTEGRITY_FAILURE`` with no numerical payload. The
geometric decision is NOT made here: it is made by the method consumer on the
exact ENTERED decimals (contract §6), and this binary result is only checked
against that exact reference.
"""
import math
from fractions import Fraction

METHOD_ID = "mechanical:planar_centered_rectangular_clearance"
METHOD_VERSION = "1.0"

# One correctly rounded binary64 result is within half an ulp: a relative
# error of at most 2**-53 for every normal result (§6).
RELATIVE_ROUNDING_BOUND = Fraction(1, 2 ** 53)


def _margin(region, board, c):
    exact = (Fraction(region) - Fraction(board)) / 2 - Fraction(c)
    if exact == 0:
        return 0.0
    try:
        value = float(exact)
    except OverflowError:
        raise ArithmeticError("margin overflows binary64") from None
    if not math.isfinite(value):
        raise ArithmeticError("non-finite margin")
    if value == 0.0 or (value > 0.0) != (exact > 0):
        raise ArithmeticError("nonzero margin underflowed or lost its sign")
    if abs(Fraction(value) - exact) > abs(exact) * RELATIVE_ROUNDING_BOUND:
        raise ArithmeticError("margin outside one correct rounding")
    return value


def evaluate(board_x, board_y, region_x, region_y, c):
    """Return ``{"margin_x": float, "margin_y": float}`` for admitted finite
    floats with every dimension ``> 0`` and ``c >= 0``. Raises
    ``ArithmeticError`` on any integrity failure."""
    values = (board_x, board_y, region_x, region_y, c)
    if not all(isinstance(v, float) and math.isfinite(v) for v in values):
        raise ArithmeticError("input not a finite float")
    if not all(v > 0.0 for v in values[:4]) or not c >= 0.0:
        raise ArithmeticError("input outside the admitted domain")
    return {"margin_x": _margin(region_x, board_x, c),
            "margin_y": _margin(region_y, board_y, c)}
