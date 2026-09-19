"""One bounded semantic claim classifier for governance truth-guards.

File: tests/semantic_claims.py
Purpose: decide, for a bounded vocabulary of concepts, whether a piece of
document prose AFFIRMS that concept as present fact, NEGATES it, or merely
mentions it without asserting anything (NON_AFFIRMING) — or never mentions it
at all (ABSENT).

Why this exists. The release-readiness guard grew two separate mechanisms: one
that looked for positive keywords and one that looked for required negations.
They could disagree. That produced two failure classes at once — a bare noun
like "provisioning" counted as evidence that provisioning existed, and a
negation one helper accepted ("not yet deployed") the other rejected. Adding
more literal strings to each side would have kept them out of step. There is
now ONE classifier, and both the contradiction rules and the required-evidence
rules read their answer from it.

This is deliberately NOT an English parser. It is a bounded grammar over a
fixed concept vocabulary, and it is designed so that the failure mode is a
refusal to affirm rather than a false affirmation: when the prose is unclear,
the answer is NON_AFFIRMING, which never satisfies a positive requirement.

This module is a helper, not a test module: it defines no test.
"""
import re
import unicodedata

AFFIRMED = "AFFIRMED"
NEGATED = "NEGATED"
NON_AFFIRMING = "NON_AFFIRMING"
ABSENT = "ABSENT"

# --------------------------------------------------------------------------
# Concept vocabulary.
#
# "state" terms are participles/adjectives that assert a present state when
# used plainly ("is provisioned"). "noun" terms name the activity and assert
# nothing on their own ("provisioning") — they affirm only when an explicit
# existence predicate follows. "phrase" terms are multi-word assertions.
# --------------------------------------------------------------------------
CONCEPTS = {
    "selection": {
        "state": ("selected",),
        "noun": ("selection",),
        "phrase": (),
    },
    "provisioning": {
        "state": ("provisioned",),
        "noun": ("provisioning",),
        "phrase": (),
    },
    "deployment": {
        "state": ("deployed",),
        "noun": ("deployment",),
        "phrase": (),
    },
    "activation": {
        # bare "live" is NOT an affirmation term: "one live backup object"
        # says nothing about the system being live. "not live" is still
        # recognised as a negation, below.
        "state": ("activated", "live-activated"),
        "noun": ("activation",),
        "phrase": ("is live", "now live", "goes live", "went live",
                   "running in production", "in production"),
    },
    "completion": {
        "state": ("complete", "completed", "done", "finished"),
        "noun": ("completion",),
        "phrase": ("fully complete", "fully completed"),
    },
}

# Negators. "non" is included because it only ever appears hyphen-attached
# ("non-provisioned"), which the gap below permits.
_NEGATOR_WORDS = frozenset(("not", "never", "no", "nor", "non"))

# A clause boundary or a coordinating conjunction ENDS a negator's reach, so
# "no scheduled run evidence exists, so it is deployed" does not read as a
# negation of "deployed", while "no separate third-party provider is selected"
# does. This walks tokens backwards rather than matching a regex with a nested
# quantifier, which backtracks catastrophically on real prose.
_CONJUNCTION_WORDS = frozenset((
    "and", "but", "or", "so", "while", "though", "however", "whereas",
    "because", "although"))
_CLAUSE_TOKENS = frozenset((".", ";", ":", ",", "—", "–"))
_TOKEN = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*|[.;:,—–]")
_NEGATOR_REACH = 12          # tokens


def _negator_governs(left):
    """True when a negator still reaches the position at the end of `left`."""
    tokens = _TOKEN.findall(left)
    for token in reversed(tokens[-_NEGATOR_REACH:]):
        if token in _CLAUSE_TOKENS or token in _CONJUNCTION_WORDS:
            return False
        if token in _NEGATOR_WORDS:
            return True
    return False

# An explicit denial that FOLLOWS the term: "provisioning does not exist",
# "completion is not established", "deployment has not occurred".
_NEG_AFTER = re.compile(
    r"^[\s*_`)\]\"'-]*(?:[a-z0-9-]+\s+){0,3}"
    r"(?:does|do|is|are|has|have|was|were|will|can|could)?\s*"
    r"\bnot\b")

# Modifiers that place the concept outside present fact. Any of these in the
# immediate neighbourhood defeats affirmation.
_NON_AFFIRMING = (
    "planned", "proposed", "pending", "attempted", "intended", "scheduled",
    "expected", "future", "failed", "failing", "aborted", "deferred",
    "will", "would", "shall", "may", "might", "should", "to be", "upcoming",
)
_NON_AFFIRMING_RE = re.compile(
    r"\b(?:" + "|".join(re.escape(w) for w in _NON_AFFIRMING) + r")\b")

# Existence predicates that let a NOUN affirm present fact.
_EXISTENCE_RE = re.compile(
    r"^[\s*_`)\]\"'-]*(?:[a-z0-9-]+\s+){0,2}"
    r"(?:exists?|is in place|are in place|is present|are present"
    r"|is active|is live|has occurred|have occurred|took place"
    r"|completed successfully|succeeded)\b")

# Negation phrases that need no term of their own to count.
_EXTRA_NEGATIONS = {
    "activation": (r"\bnot[\s-]+(?:yet[\s-]+|currently[\s-]+)?live\b",),
}

_CLAUSE_BREAK = re.compile(r"[.;:,—–]")


def normalize(text):
    """Casefold, strip Markdown emphasis, normalise dashes, keep hyphens."""
    text = unicodedata.normalize("NFKC", text).casefold()
    text = text.replace("‑", "-")          # non-breaking hyphen
    text = re.sub(r"[*_`]+", " ", text)         # emphasis is not meaning
    text = re.sub(r"\s+", " ", text)
    return text


def _left_window(text, start, limit=140):
    return text[max(0, start - limit):start]


def _right_window(text, end, limit=80):
    return text[end:end + limit]


def _clause_before(window):
    """The part of the left window since the last clause boundary."""
    breaks = list(_CLAUSE_BREAK.finditer(window))
    return window[breaks[-1].end():] if breaks else window


def _clause_after(window):
    match = _CLAUSE_BREAK.search(window)
    return window[:match.start()] if match else window


def _classify_occurrence(text, start, end, is_noun):
    left = _left_window(text, start)
    right = _right_window(text, end)

    if _negator_governs(left) or _NEG_AFTER.match(right):
        return NEGATED

    # "planned", "will be", "failed" and friends, within the same clause
    if _NON_AFFIRMING_RE.search(_clause_before(left)) or \
            _NON_AFFIRMING_RE.search(_clause_after(right)):
        return NON_AFFIRMING

    if is_noun:
        # a noun asserts nothing by itself; it needs an existence predicate
        return AFFIRMED if _EXISTENCE_RE.match(right) else NON_AFFIRMING

    return AFFIRMED


def classify(text, concept, allow_owner_selected=True):
    """Classify `concept` in `text`.

    Returns AFFIRMED, NEGATED, NON_AFFIRMING or ABSENT. When occurrences
    disagree, the strongest present assertion wins: AFFIRMED over NEGATED over
    NON_AFFIRMING. A document that both affirms and negates a concept is
    reporting an affirmation somewhere, and that is what a guard must see.
    """
    spec = CONCEPTS[concept]
    norm = normalize(text)
    verdicts = []

    for terms, is_noun in ((spec["state"], False), (spec["noun"], True),
                           (spec["phrase"], False)):
        for term in terms:
            pattern = r"(?<![a-z0-9])" + re.escape(term) + r"(?![a-z0-9])"
            for match in re.finditer(pattern, norm):
                left = _left_window(norm, match.start())
                if (allow_owner_selected and concept == "selection"
                        and left.endswith("owner-")):
                    continue                    # a recorded Owner selection
                verdicts.append(
                    _classify_occurrence(norm, match.start(), match.end(),
                                         is_noun))

    for pattern in _EXTRA_NEGATIONS.get(concept, ()):
        if re.search(pattern, norm):
            verdicts.append(NEGATED)

    if not verdicts:
        return ABSENT
    if AFFIRMED in verdicts:
        return AFFIRMED
    if NEGATED in verdicts:
        return NEGATED
    return NON_AFFIRMING


def affirmed(text, concept, **kw):
    return classify(text, concept, **kw) == AFFIRMED


def negated(text, concept, **kw):
    return classify(text, concept, **kw) == NEGATED
