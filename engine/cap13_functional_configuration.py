"""IDEA-TO-ENGINEERING-CONFIG-01 — request-local functional fit projection.

CAP-13 owns ONE *provisional dimensional envelope*, not a design method.
Only explicit, bounded EN/AR wording in the inventor's original idea is read.
No Path-N/ledger/T2-A quantity content, LLM, persistence, shared calculator,
method admission, material assumption or engineering safety inference is used.
An unsupported/ambiguous statement has NO positive engineering output.
"""
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
import hashlib
import re

GRAMMAR_VERSION = "desktop_raise_explicit_v1"
CANDIDATE = "PROVISIONAL_DIMENSIONAL_ENVELOPE"
_MAX_IDEA_CHARS = 2000
_MAX_VALUE = Decimal("100000")  # Capture bound only, NEVER a family validity limit.
_UNITS = r"(?:cm|mm|سم|ملم)"
_NUMBER = r"[0-9]+(?:\.[0-9]+)?"
_DIMENSION = re.compile(
    rf"(?P<a>{_NUMBER})\s*[×xX*]\s*(?P<b>{_NUMBER})\s*(?P<unit>{_UNITS})(?![\w/])"
)
_RISE = re.compile(
    rf"(?P<verb>\braise\b|\blift\b|\belevate\b|رفع|أرفع|ارفع|يرفع)"
    rf"[^\n.؛!?؟]{{0,80}}?(?P<n>{_NUMBER})\s*(?P<unit>{_UNITS})(?![\w/])",
    re.IGNORECASE,
)
_DESKTOP = re.compile(r"\b(?:desk|desktop|table)\b|مكتب|طاول", re.IGNORECASE)
_EXCLUSION = re.compile(
    r"\b(?:step\s+on|stand\s+on\s+it|people\s+stand|people\s+sit|person|people|child|children|wall)\b|"
    r"(?:يقف|يصعد|يجلس)\s+(?:عليه|فوقه)|درج\s+للوقوف|شخص|طفل|أطفال|جدار|حائط",
    re.IGNORECASE,
)
_NEGATED = re.compile(
    r"\b(?:do\s+not|don't|not|never)\s+(?:want\s+to\s+)?(?:raise|lift|elevate)\b|"
    r"لا\s+(?:أريد|اريد)?\s*(?:رفع|ارفع|أرفع)", re.IGNORECASE,
)
_ARABIC_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹", "01234567890123456789")


@dataclass(frozen=True)
class ProvisionalFit:
    """Not a feasible or safe design: fit-only information from one idea."""
    status: str
    grammar_version: str
    source_digest: str
    source_type: str
    source_excerpt: str
    size_span: str
    rise_span: str
    top_length: str
    top_depth: str
    size_unit: str
    surface_lift: str
    lift_unit: str
    fit_rule: str
    engineering_status: str


def _positive_number(token):
    try:
        number = Decimal(token)
    except (InvalidOperation, ValueError):
        return None
    if not number.is_finite() or not 0 < number <= _MAX_VALUE:
        return None
    return number


def _display_number(number):
    return format(number.normalize(), "f")


def derive_provisional_fit(original_idea):
    """Return a strictly bounded candidate or None; never change inventor data.

    This is intentionally NOT open-ended natural-language understanding.
    Only the original statement may be passed by the caller, not T2-A text or
    a display-trimmed excerpt. Recognition does not admit CAP-13 calculations.
    """
    if not isinstance(original_idea, str) or not 0 < len(original_idea) <= _MAX_IDEA_CHARS:
        return None
    if _EXCLUSION.search(original_idea) or _NEGATED.search(original_idea):
        return None
    if not _DESKTOP.search(original_idea):
        return None
    # One-to-one digit translation only. No general transliteration, guessing,
    # range interpolation or spelling correction is performed.
    searchable = original_idea.translate(_ARABIC_DIGITS)
    sizes = list(_DIMENSION.finditer(searchable))
    if len(sizes) != 1:
        return None
    size = sizes[0]
    # Without an explicit dimensions label, the pair might refer to something
    # unrelated. This recognizes only a narrow declarative form, not any two
    # numbers separated by an 'x'.
    preceding = searchable[max(0, size.start() - 40):size.start()]
    if not re.search(r"(?:dimensions|size|أبعاد|ابعاد|أبعاده|ابعاده|مقاس|مقاسات)\s*:?\s*$", preceding, re.IGNORECASE):
        return None
    # Do not treat the second dimension as the lift measurement. Keep source
    # indexes identical by blanking, not deleting, the dimension substring.
    unmasked = (searchable[:size.start()]
                + " " * (size.end() - size.start())
                + searchable[size.end():])
    rises = list(_RISE.finditer(unmasked))
    if len(rises) != 1:
        return None
    rise = rises[0]
    # Only a single explicit rise and dimension pair can become a candidate.
    # This rule cannot silently choose between conflicting requirements.
    length, depth, lift = (_positive_number(size.group("a")),
                           _positive_number(size.group("b")),
                           _positive_number(rise.group("n")))
    if None in (length, depth, lift):
        return None
    return ProvisionalFit(
        status=CANDIDATE,
        grammar_version=GRAMMAR_VERSION,
        source_digest=hashlib.sha256(original_idea.encode("utf-8")).hexdigest(),
        source_type="ORIGINAL_IDEA_STATEMENT",
        source_excerpt=original_idea,
        size_span=original_idea[size.start():size.end()],
        rise_span=original_idea[rise.start():rise.end()],
        top_length=_display_number(length),
        top_depth=_display_number(depth),
        size_unit=size.group("unit"),
        surface_lift=_display_number(lift),
        lift_unit=rise.group("unit"),
        fit_rule="TOP_PLAN_AT_LEAST_OBJECT_DIMENSIONS_NO_OVERHANG_CANDIDATE",
        engineering_status="NOT_ASSESSED",
    )
