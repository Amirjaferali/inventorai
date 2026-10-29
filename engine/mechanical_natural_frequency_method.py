"""Mechanical - spring-mass natural frequency: the method-authority adapter.

Method authority: docs/governance/MECHANICAL_SPRING_MASS_NATURAL_FREQUENCY_METHOD_CONTRACT.md
(§3 method definition and derivation, §6 numeric domain and numerical
acceptance). Identity ``mechanical:spring_mass_natural_frequency``, version
``1.0`` (§2).

This module holds ONE pure deterministic function and nothing else: no request
handling, no unit handling, no I/O. It is handed to the shared calculation owner
once, by application wiring, as an immutable binding; the owner never imports it.

The relation is the undamped natural frequency of ONE single-degree-of-freedom
spring-mass system - one mass ``m`` driven by one linear spring of stiffness
``k`` whose other end is attached to a support of relatively very large mass -
restated independently from NBS Technical Note 487 (Newman, 1969; recorded as
NBS-NF-S1): the undamped natural angular frequency is ``sqrt(k / m)``. With NIST
SP 330 (recorded as NIST-NF-U) stating that angular frequency in rad/s and
frequency in Hz differ by the factor 2π, the ordinary natural frequency is
``f0 = sqrt(k / m) / (2π)``. No NBS or NIST text is copied.

Role identifiers (§4): ``k`` (N/m, strictly positive), ``m`` (kg, strictly
positive) and ``f0`` (Hz, strictly positive).

Numeric arrangement (documented, deterministic; §6):

* Execution is in binary64 with three IEEE-754 correctly rounded operations in
  this fixed order: ``ratio = k / m``, ``omega = math.sqrt(ratio)``,
  ``f0 = omega / TWO_PI``.
* Mathematical-constant policy (method-local; no constants registry):
  ``TWO_PI = 2.0 * math.pi`` - the exact doubling of the binary64 value nearest
  π (the Python / C library constant, round-to-nearest). For the acceptance and
  for every reference computation this module uses the 50-decimal TRUNCATION of
  π recorded in ``PI_50_DECIMALS`` as the rational interval
  ``PI_LOW < π < PI_HIGH`` (``PI_HIGH = PI_LOW + 10**-50``). Both facts are
  verifiable independently of this module (a Machin-formula computation of π
  and ``float(PI_LOW) == math.pi``) and are pinned by test.
* Acceptance (an independent reference, never the executed path): from the two
  actual binary input values the EXACT rational ratio is formed; its square root
  is bracketed with integer arithmetic (``math.isqrt`` at scale ``10**40``) as a
  rational interval ``[s_low, s_high]`` with ``s_high - s_low`` below ``10**-40``
  relative; the natural frequency is then bracketed as
  ``[s_low / (2 PI_HIGH), s_high / (2 PI_LOW)]``, an interval that contains the
  true value of ``sqrt(k/m) / (2π)`` for those binary inputs. The computed ``f0``
  is accepted ONLY when it is finite, strictly positive and within a relative
  error of ``2**-50`` of that interval. For a ratio that is a normal binary64
  number the three executed operations carry at most about ``2.9 x 2**-53``
  relative error (the ratio's rounding ``2**-53``, halved by the square root to
  ``0.5 x 2**-53``; the square root's own rounding ``2**-53``; the π constant
  below ``0.4 x 2**-53``; the final division ``2**-53``), so a correctly
  rounded execution always meets the bound; a subnormal ratio is
  accepted only when its larger rounding error still meets the bound, and a
  zero ratio or an overflow of ``k / m`` is reported as an integrity failure,
  never as a number.
* Overflow to infinity, underflow to zero, an out-of-bound result and any input
  outside the admitted domain raise ``ArithmeticError``; the owner turns that
  into ``FAILURE / EXECUTION_INTEGRITY_FAILURE`` with no numerical payload. This
  acceptance rule belongs to this method only.
"""
import math
from fractions import Fraction

METHOD_ID = "mechanical:spring_mass_natural_frequency"
METHOD_VERSION = "1.0"

# The 50-decimal TRUNCATION of π (the next digits are 58209...). PI_LOW < π < PI_HIGH.
PI_50_DECIMALS = "3.14159265358979323846264338327950288419716939937510"
PI_LOW = Fraction(PI_50_DECIMALS)
PI_HIGH = PI_LOW + Fraction(1, 10 ** 50)

# The executed constant: the exact doubling of the binary64 value nearest π.
TWO_PI = 2.0 * math.pi

# The integer-arithmetic square-root bracket: scale 10**40 (relative width of
# the bracket below 10**-40 for every positive rational ratio).
SQRT_SCALE = 10 ** 40

# The accepted relative-error bound of the executed f0 against the reference
# interval (§6).
RELATIVE_ERROR_BOUND = Fraction(1, 2 ** 50)


def sqrt_bounds(value):
    """Rational bounds ``(low, high)`` with ``low <= sqrt(value) <= high`` for a
    strictly positive ``Fraction``, from integer arithmetic only:
    ``sqrt(p / q) = sqrt(p q) / q`` and ``n = isqrt(p q S**2)`` gives
    ``n <= sqrt(p q) S < n + 1``."""
    if not isinstance(value, Fraction) or value <= 0:
        raise ArithmeticError("square root of a non-positive value")
    p, q = value.numerator, value.denominator
    n = math.isqrt(p * q * SQRT_SCALE * SQRT_SCALE)
    return Fraction(n, q * SQRT_SCALE), Fraction(n + 1, q * SQRT_SCALE)


def frequency_bounds(k, m):
    """Rational bounds ``(low, high)`` of ``sqrt(k / m) / (2π)`` for two
    strictly positive ``Fraction`` values: the square-root bracket divided by
    the π bracket, so the true value lies inside."""
    if not (isinstance(k, Fraction) and isinstance(m, Fraction) and k > 0 and m > 0):
        raise ArithmeticError("input outside the admitted domain")
    s_low, s_high = sqrt_bounds(k / m)
    return s_low / (2 * PI_HIGH), s_high / (2 * PI_LOW)


def evaluate(k, m):
    """Return ``{"f0": float}`` for admitted finite floats with ``k > 0`` and
    ``m > 0``. Raises ``ArithmeticError`` on any integrity failure."""
    if not all(isinstance(v, float) and math.isfinite(v) for v in (k, m)):
        raise ArithmeticError("input not a finite float")
    if not (k > 0.0 and m > 0.0):
        raise ArithmeticError("input outside the admitted domain")
    ratio = k / m
    if not math.isfinite(ratio) or ratio <= 0.0:
        raise ArithmeticError("stiffness-to-mass ratio overflowed or underflowed")
    omega = math.sqrt(ratio)
    f0 = omega / TWO_PI
    if not math.isfinite(f0) or f0 <= 0.0:
        raise ArithmeticError("non-finite or non-positive natural frequency")
    low, high = frequency_bounds(Fraction(k), Fraction(m))
    produced = Fraction(f0)
    if produced < low * (1 - RELATIVE_ERROR_BOUND) \
            or produced > high * (1 + RELATIVE_ERROR_BOUND):
        raise ArithmeticError("natural frequency outside the accepted relative error")
    return {"f0": f0}
