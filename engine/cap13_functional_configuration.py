"""IDEA-TO-ENGINEERING-CONFIG-01 — request-local functional fit projection.

CAP-13 owns ONE *provisional dimensional envelope*, not a design method.
Only explicit, bounded EN/AR wording in the inventor's own statements is read:
the original idea and, since CAP13-PROVISIONAL-FIT-CURRENT-ANSWERS-01, the
verbatim text of each CURRENT answered inventor record the caller supplies
(the PR #956 source rule). Each statement is read ON ITS OWN by the same
grammar; quantities are never combined across statements, and statements that
disagree give no candidate. No Path-N/T2-A quantity content, LLM, persistence,
shared calculator, method admission, material assumption or engineering safety
inference is used. An unsupported/ambiguous statement has NO positive
engineering output.
"""
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
import hashlib
import re

GRAMMAR_VERSION = "desktop_raise_explicit_v1"
CANDIDATE = "PROVISIONAL_DIMENSIONAL_ENVELOPE"
SOURCE_IDEA = "ORIGINAL_IDEA_STATEMENT"
SOURCE_ANSWER = "CURRENT_ANSWER"
_MAX_IDEA_CHARS = 2000
_MAX_VALUE = Decimal("100000")  # Capture bound only, NEVER a family validity limit.
_UNITS = r"(?:cm|mm|سم|ملم)"
# A number never starts inside a run of digits: a later start in the same run
# reaches the same next character as the run's first digit, so it can match
# nothing the first start does not, but without the guard every digit of a long
# run restarts a scan to the run's end (quadratic in the run's length). The
# guard keeps each statement's scan linear; the results are unchanged.
_NUMBER = r"(?<![0-9])[0-9]+(?:\.[0-9]+)?"
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
# Any negation word in the rise statement's sentence, before or inside the rise
# span, refuses the candidate (fail closed). This is a stop list, not a parser:
# it never decides what a negated sentence means. A listed word used without
# negating (e.g. a relative "ما") also refuses, which is the safe direction; a
# negation form it does not list is not caught.
_NEGATION_WORD = re.compile(
    r"(?<!\w)(?:not|never|no|cannot)(?!\w)|n't(?!\w)|"
    r"(?<!\w)[وف]?(?:لا|لن|لم|ليس|ليست|لست|ما|مش|مو)(?!\w)",
    re.IGNORECASE,
)
_SENTENCE_BREAK = re.compile(r"[\n.;؛!?؟]")
# An ambiguous lift must not become a single-valued offer. Masked object
# dimensions are excluded from this check, and decimal dots are not boundaries.
_RISE_AMOUNT = re.compile(r"(?<![0-9.])[0-9]+(?:\.[0-9]+)?(?![0-9])")
_RISE_END = re.compile(r"[\n!?؟]|\.(?![0-9])")
_RISE_LIMIT = re.compile(
    r"\b(?:between|either|up\s+to|at\s+(?:least|most)|no\s+(?:more|less)\s+than)\b|"
    r"(?:بين|إما|اما|حتى|لغاية|على\s+الأقل|بحد\s+أقصى)", re.IGNORECASE)
_AMBIGUOUS_RISE = object()
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


@dataclass(frozen=True)
class FitConflict:
    """The inventor's current statements each hold a candidate, but not the
    same one: no candidate is offered and none is chosen."""
    status: str = "CONFLICTING_STATEMENTS"


CONFLICT = FitConflict()


def derive_provisional_fit(original_idea):
    """Return a strictly bounded candidate or None; never change inventor data.

    This is intentionally NOT open-ended natural-language understanding.
    Only the original statement may be passed by the caller, not T2-A text or
    a display-trimmed excerpt. Recognition does not admit CAP-13 calculations.
    """
    located = _locate(original_idea, SOURCE_IDEA)
    return located[0] if located is not None and located is not _AMBIGUOUS_RISE else None


def derive_current_fit(original_idea, answer_texts):
    """The ONE candidate the inventor's current statements give, ``CONFLICT``,
    or None (CAP13-PROVISIONAL-FIT-CURRENT-ANSWERS-01).

    ``answer_texts`` are the verbatim texts of the CURRENT answered inventor
    records, already selected by the caller's PR #956 filter. The original idea
    and then each answer are read on their own by the unchanged grammar. No
    candidate -> None. Candidates whose dimension pair (in either written
    order), lift and unit tokens are written identically -> ONE candidate: from
    the original idea when it holds one, otherwise from the most recent answer,
    labelled by ``source_type``. Anything else -> ``CONFLICT``; numbers and
    units are compared as written and never converted or coerced. Raises
    ``ValueError`` when ``answer_texts`` is not a sequence of strings, so an
    unreadable history is never read as an empty one."""
    if not isinstance(answer_texts, (list, tuple)) \
            or not all(isinstance(text, str) for text in answer_texts):
        raise ValueError("unreadable answer texts")
    located = []
    from_idea = _locate(original_idea, SOURCE_IDEA)
    if from_idea is _AMBIGUOUS_RISE:
        return None
    if from_idea is not None:
        located.append(from_idea)
    for text in answer_texts:
        found = _locate(text, SOURCE_ANSWER)
        if found is _AMBIGUOUS_RISE:
            return None  # Never fall back to a possibly superseded exact lift.
        if found is not None:
            located.append(found)
    if not located:
        return None
    if len({key for _fit, key in located}) != 1:
        return CONFLICT
    return located[0][0] if from_idea is not None else located[-1][0]


def _locate(original_idea, source_type):
    """One exact candidate and key, None, or the internal ambiguous-lift marker.
    Never turn an explicitly ranged/alternative lift into one selected height."""
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
    # A negated or limiting rise ("لا أريد أن أرفع ...", "I won't raise ...",
    # "... لا يزيد عن 3 سم") is never read as the inventor's requirement.
    breaks = [m.end() for m in _SENTENCE_BREAK.finditer(unmasked, 0, rise.start())]
    sentence_start = breaks[-1] if breaks else 0
    if _NEGATION_WORD.search(unmasked, sentence_start, rise.end()):
        return None
    # Keep semicolons in the statement: "raise 10 cm; or 15 cm" remains
    # ambiguous. The object dimensions have already been masked out.
    statement_end = _RISE_END.search(unmasked, rise.start())
    lift_statement = unmasked[rise.start():statement_end.start() if statement_end else len(unmasked)]
    if len(_RISE_AMOUNT.findall(lift_statement)) != 1 or _RISE_LIMIT.search(lift_statement):
        return _AMBIGUOUS_RISE
    # Only a single explicit rise and dimension pair can become a candidate.
    # This rule cannot silently choose between conflicting requirements.
    length, depth, lift = (_positive_number(size.group("a")),
                           _positive_number(size.group("b")),
                           _positive_number(rise.group("n")))
    if None in (length, depth, lift):
        return None
    key = (tuple(sorted((size.group("a"), size.group("b")))), size.group("unit"),
           rise.group("n"), rise.group("unit"))
    return ProvisionalFit(
        status=CANDIDATE,
        grammar_version=GRAMMAR_VERSION,
        source_digest=hashlib.sha256(original_idea.encode("utf-8")).hexdigest(),
        source_type=source_type,
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
    ), key
