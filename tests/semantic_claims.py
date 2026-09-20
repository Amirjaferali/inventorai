"""Claim-scoped semantic classifier for governance truth-guards.

File: tests/semantic_claims.py
Purpose: for a bounded concept vocabulary — selection, provisioning,
deployment, activation, completion — find each individual CLAIM OCCURRENCE in
a piece of document prose and give that occurrence its own polarity, then
aggregate.

Why the claim-occurrence model. The previous version classified a concept by
scanning the surrounding text. That let one claim's modifier change another
claim's polarity: in "the scheduler is deployed but not activated" the `not`
governing *activated* reached backwards and negated *deployed*, and in
"provider work is completed but verification is pending" the word `pending`
defeated a completion claim it had nothing to do with. Polarity is a property
of a claim, not of a paragraph.

The model:

  normalize → split into clauses → find occurrences per clause →
  give each occurrence a polarity from ITS OWN clause → aggregate

A clause is the scope. A negator negates only claims that follow it inside the
same clause (or, for an existence noun, an explicit denial that follows it:
"provisioning does not exist"). A temporal or hypothetical modifier —
"planned", "pending", "failed" — only reaches claims in its own clause.
Aggregation preserves CONFLICT when the SAME predicate is both affirmed and
denied; it never silently prefers one side. It does not raise CONFLICT when
two different predicates disagree, because they usually have different
subjects and this classifier cannot read subjects.

This is deliberately NOT an English parser, and must not grow into one. It is
a bounded grammar over this release-readiness vocabulary, and it fails toward
NON_AFFIRMING — which never satisfies a positive requirement — so unclear
prose cannot be mistaken for an assertion of present fact.

Runtime is linear in the length of the text: fixed clause splitting plus one
`finditer` per term per clause. No nested quantifiers, no backtracking traps.

This module is a helper, not a test module: it defines no test.
"""
import collections
import re
import unicodedata

AFFIRMED = "AFFIRMED"
NEGATED = "NEGATED"
NON_AFFIRMING = "NON_AFFIRMING"
CONFLICT = "CONFLICT"
ABSENT = "ABSENT"

ClaimOccurrence = collections.namedtuple(
    "ClaimOccurrence", "concept predicate polarity span clause")

# --------------------------------------------------------------------------
# Concept vocabulary.
#
#   "state"   — participles/adjectives asserting a present state when plain
#               ("is provisioned"); AFFIRMED unless negated or qualified.
#   "noun"    — names the activity and asserts nothing alone ("provisioning");
#               affirms only with an explicit existence predicate beside it.
#   "pattern" — multi-word claim forms with their own regex, used where a bare
#               word would be ambiguous (see activation, below).
# --------------------------------------------------------------------------
_LIVE_SUBJECT = r"(?:is|are|was|were|remains?|stays?|becomes?|went|goes|got)"

CONCEPTS = {
    "selection": {
        "state": ("selected", "chosen", "adopted"),
        "noun": ("selection",),
        "pattern": (),
    },
    "provisioning": {
        "state": ("provisioned",),
        "noun": ("provisioning",),
        "pattern": (),
    },
    "deployment": {
        "state": ("deployed",),
        "noun": ("deployment",),
        "pattern": (),
    },
    "activation": {
        # Bare "live" is NOT listed: "one live backup object" describes the
        # object, not the system. Service-level liveness is matched by the
        # patterns below, which require a subject predicate or a status form.
        "state": ("activated", "live-activated"),
        "noun": ("activation",),
        "pattern": (
            r"\b" + _LIVE_SUBJECT + r"\s+(?:currently\s+|now\s+|already\s+)?live\b",
            r"\bstatus\s*[:=]\s*live\b",
            r"\brunning\s+in\s+production\b",
            r"\bin\s+production\b",
            # "not live" is a claim form of its own, so that a negated
            # liveness statement registers rather than going unseen.
            r"\bnot\s+(?:yet\s+|currently\s+)?live\b",
        ),
    },
    "completion": {
        "state": ("complete", "completed", "done", "finished"),
        "noun": ("completion",),
        "pattern": (),
    },
}

# --------------------------------------------------------------------------
# Normalization. Hyphenated negation compounds become their spaced forms so
# that "not-yet-deployed" and "not yet deployed" mean the same thing, while
# genuine compounds like "live-activated" are left intact.
# --------------------------------------------------------------------------
_HYPHEN_NEGATION = re.compile(
    r"\b(not|never|non)-(yet-|currently-|longer-)?")


def normalize(text):
    text = unicodedata.normalize("NFKC", text).casefold()
    text = text.replace("‑", "-")                 # non-breaking hyphen
    text = re.sub(r"[*_`]+", " ", text)                # emphasis is not meaning
    text = _HYPHEN_NEGATION.sub(lambda m: m.group(1) + " " +
                                (m.group(2) or "").replace("-", " "), text)
    return re.sub(r"\s+", " ", text)


# --------------------------------------------------------------------------
# Clause segmentation: the scope within which a modifier may act.
# --------------------------------------------------------------------------
_NEGATOR = re.compile(
    r"\b(?:not|never|no|nor|cannot|can't|couldn't|without|lacks?|lacking)\b")

_CONJUNCTIONS = ("and", "but", "or", "nor", "while", "whereas", "though",
                 "although", "however", "because", "so")
_CLAUSE_SPLIT = re.compile(
    r"[.;,—–()\[\]]|\b(?:" + "|".join(_CONJUNCTIONS) + r")\b")

# Negation distributes across "or"/"nor" onto a bare trailing predicate —
# "no provider has been chosen or adopted" denies both. It deliberately does
# NOT distribute across "and"/"but", and not onto a clause with its own
# subject, because "not deployed but the service is live" affirms liveness.
# Refusing to distribute leaves a claim AFFIRMED, which is the safe direction
# for a truth guard: it never reads an assertion as a denial.
_DISTRIBUTING = ("or", "nor")
_CARRY_MAX_TOKENS = 4


def clauses(norm_text):
    """Split into (clause_text, offset, carried_negation) triples."""
    pieces, cursor = [], 0
    for match in _CLAUSE_SPLIT.finditer(norm_text):
        if match.start() > cursor:
            pieces.append((norm_text[cursor:match.start()], cursor,
                           match.group(0).strip()))
        elif pieces:
            pieces[-1] = pieces[-1][:2] + (match.group(0).strip(),)
        cursor = match.end()
    if cursor < len(norm_text):
        pieces.append((norm_text[cursor:], cursor, ""))

    out, carry = [], False
    for text, offset, separator in pieces:
        if not text.strip():
            continue
        out.append((text, offset, carry))
        carry = (separator in _DISTRIBUTING
                 and bool(_NEGATOR.search(text))
                 and len(text.split()) <= 24)
    # a carried negation applies only to a short trailing predicate — never
    # onto a clause that introduces its own subject
    return [(t, o, c and len(t.split()) <= _CARRY_MAX_TOKENS)
            for t, o, c in out]


# --------------------------------------------------------------------------
# Clause-local polarity signals.
# --------------------------------------------------------------------------
# An explicit denial of existence that FOLLOWS a noun claim:
# "provisioning does not exist", "provisioning no longer exists",
# "provisioning cannot exist", "provisioning never took place".
_EXISTENCE_DENIAL = re.compile(
    r"^\s*(?:[a-z0-9-]+\s+){0,2}"
    r"(?:does not|do not|did not|is not|are not|was not|were not|has not|"
    r"have not|cannot|can not|could not|will not|no longer|never)\s+"
    r"(?:[a-z0-9-]+\s+){0,2}"
    r"(?:exists?|existed|occur(?:red)?|took place|take place|happen(?:ed)?"
    r"|established|proven|demonstrated|achieved|reached|in place)\b")

# A present-tense existence predicate that lets a NOUN affirm.
_EXISTENCE = re.compile(
    r"^\s*(?:[a-z0-9-]+\s+){0,2}"
    r"(?:exists?|existed|is in place|are in place|is present|are present"
    r"|is active|has occurred|have occurred|took place"
    r"|completed successfully|succeeded)\b")

# Modifiers that place a claim outside present fact.
_MODIFIER = re.compile(
    r"\b(?:planned|proposed|pending|attempted|intended|scheduled|expected"
    r"|future|upcoming|failed|failing|aborted|deferred|considered"
    r"|under consideration|will|would|shall|may|might|should|to be)\b")


def _polarity(clause, start, end, is_noun, carried_negation=False):
    """Polarity of ONE occurrence, from ITS OWN clause only."""
    before, after = clause[:start], clause[end:]

    # Denial first: a denied existence can never become an affirmation.
    if carried_negation or _NEGATOR.search(before):
        return NEGATED
    if is_noun and _EXISTENCE_DENIAL.match(after):
        return NEGATED

    if _MODIFIER.search(clause):
        return NON_AFFIRMING

    if is_noun:
        return AFFIRMED if _EXISTENCE.match(after) else NON_AFFIRMING

    return AFFIRMED


def occurrences(text, concept):
    """Every claim occurrence for `concept`, each with its own polarity.

    Longer terms are matched first and their spans consumed, so a compound
    such as "live-activated" cannot also yield an inner "activated" claim and
    manufacture affirmative evidence inside a single negated compound.
    """
    spec = CONCEPTS[concept]
    found = []

    for clause, offset, carried in clauses(normalize(text)):
        taken = []

        def overlaps(start, end):
            return any(start < t_end and end > t_start
                       for t_start, t_end in taken)

        terms = ([(t, False) for t in
                  sorted(spec["state"], key=len, reverse=True)] +
                 [(t, True) for t in spec["noun"]])

        for pattern in spec["pattern"]:
            for match in re.finditer(pattern, clause):
                if overlaps(*match.span()):
                    continue
                taken.append(match.span())
                polarity = NEGATED if _NEGATOR.search(match.group(0)) \
                    else _polarity(clause, match.start(), match.end(), False,
                                   carried)
                found.append(ClaimOccurrence(
                    concept, match.group(0).strip(), polarity,
                    (offset + match.start(), offset + match.end()), clause))

        for term, is_noun in terms:
            for match in re.finditer(
                    r"(?<![a-z0-9])" + re.escape(term) + r"(?![a-z0-9])",
                    clause):
                if overlaps(*match.span()):
                    continue
                taken.append(match.span())
                found.append(ClaimOccurrence(
                    concept, term,
                    _polarity(clause, match.start(), match.end(), is_noun,
                              carried),
                    (offset + match.start(), offset + match.end()), clause))

    return found


def aggregate(claim_occurrences):
    """Combine occurrence polarities without discarding disagreement.

    CONFLICT is raised when the SAME predicate is both affirmed and denied —
    "the provider is provisioned … the provider is not provisioned". It is
    deliberately not raised when two different predicates of one concept
    disagree, because they usually have different subjects and this classifier
    cannot tell subjects apart: "the platform stack is the selected approach"
    and "no third-party provider was adopted" are both true at once. Treating
    that as a contradiction would reject truthful prose, and a bounded
    classifier must not adjudicate what it cannot read.
    """
    if not claim_occurrences:
        return ABSENT

    by_predicate = collections.defaultdict(set)
    for occurrence in claim_occurrences:
        by_predicate[occurrence.predicate].add(occurrence.polarity)
    for polarities in by_predicate.values():
        if AFFIRMED in polarities and NEGATED in polarities:
            return CONFLICT

    polarities = {o.polarity for o in claim_occurrences}
    if AFFIRMED in polarities:
        return AFFIRMED
    if NEGATED in polarities:
        return NEGATED
    return NON_AFFIRMING


def classify(text, concept):
    """AFFIRMED / NEGATED / NON_AFFIRMING / CONFLICT / ABSENT."""
    return aggregate(occurrences(text, concept))


def explain(text, concept):
    """Human-readable occurrence list — for failure messages and debugging."""
    return [(o.predicate, o.polarity, o.clause.strip())
            for o in occurrences(text, concept)]
