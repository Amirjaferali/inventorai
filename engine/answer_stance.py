"""T2-G (partial) — bounded recognition of an EXPLICIT mechanism unknown.

Authority: Owner decision `T2G-VERSIONED-IMPLEMENT-01` v1.0, adopting the
`T2G-BOUNDED-DESIGN-01` v1.1 direction. This module owns ONE narrow question:

    did this answer positively declare that the requested mechanism
    information is NOT known, and supply no explanation of it anyway?

What it is NOT
--------------
It is not language understanding, translation, sentiment, a negation parser
or a claim about whether anything the inventor wrote is TRUE. It reads the
ALREADY-REGISTERED explicit-ignorance vocabularies and the ALREADY-COMMITTED
per-question intent markers; it introduces no new vocabulary of its own and
broadens no existing consumer. Every judgement is a pure, deterministic
function of the text plus committed content — no clock, no randomness, no
persistence, no network.

Bounds, stated rather than hidden
---------------------------------
  * ONLY the registered explicit-unknown phrasings are recognised. An
    unregistered way of saying "I don't know", and any statement shorter than
    the existing detector's minimum length, are NOT recognised: the answer is
    then treated exactly as it is today. Under-recognition is the deliberate
    direction of error.
  * A qualifying carrier must relate to the SPECIFIC question's requested
    information (its committed intent markers). A bare component name, an
    uncertainty-only phrase, or an unrelated sentence never covers a question
    and never, on its own, defeats the eligibility veto.
  * Physical negation is not ignorance. "The latch does NOT carry the load;
    the load path runs around it" stays a supported explanation.
  * A mixed answer keeps its supported clause only when that clause is a
    SEPARATE sentence by this module's own bounded sentence handling. A single
    sentence that both declares an unknown and explains something is treated as
    cued throughout, and a genuine explanation shorter than the surplus floor
    is missed. Both are under-progress, and both are disclosed rather than
    presented as solved.
  * Under T2-G-2 a contrast boundary does NOT clear governing scope. A clause
    is refused as NEW support when its segment was a question, when a later
    recognised unknown in the same sentence refers back at it, when a
    supposition opened earlier still governs it, or when it is reported speech
    or quoted in its entirety. Each is decided by where the cue sits relative
    to the mechanism material, so a bare pronoun, reporting word or quotation
    mark is never on its own a veto. These refusals reach the T2-G-2 path only
    and can never withdraw a level-1 or pre-T2-G result.

Version gating
--------------
Every public predicate is inert unless the caller's canonical state carries
the T2-G engine-contract version. An unversioned or legacy state NEVER
enables the new rule (`engine/session_reconstruction.py` owns the version
vocabulary; this module only compares).

Import discipline: nothing from `engine.progression_loop` or
`engine.intent_serving` is imported at module scope. The committed-marker
matcher is INJECTED by the caller and the ignorance vocabularies are read
through a lazy, function-scope import, so both module-import orders are safe.
"""
import re

from engine.idea_state import MECHANISM_COMPLETENESS
from engine.semantic_registry import detect_registered_unknown

# The exact named scope of this partial slice.
T2G_SCOPED_GAPS = frozenset({MECHANISM_COMPLETENESS})
T2G_SCOPED_DOMAINS = frozenset({"electronics_electrical", "mechanical"})

# The two committed variants whose OWN request is for uncertainty / missing
# detail. Naming a missing detail genuinely answers THESE questions, so their
# coverage is unchanged. Identifying uncertainty is never mechanism knowledge:
# the eligibility veto below ignores this exemption entirely.
UNCERTAINTY_QUESTION_IDS = frozenset({
    "N-MC-4",
    "mechanical:MECHANISM_COMPLETENESS:Q4",
})

# Bounded sentence handling for THIS module only — the existing
# `progression_loop._SENTENCE_SPLIT_RE` and `_GATE_SENTENCE_BOUNDARY_RE` keep
# their own meanings and consumers. Both the English and the Arabic question
# mark and semicolon are terminators here; the Arabic comma deliberately is
# NOT, so "«لا أعرف مسار الحمل، و…»" stays ONE cued clause.
_SENTENCE_BOUNDARY_RE = re.compile(r"[.!?;؛؟]+|[\r\n]+")

# Whole-word tokens, both scripts. Used only to size a candidate carrier.
_WORD_RE = re.compile(r"[^\W\d_]+", re.UNICODE)

# A qualifying carrier must say something ABOUT the requested information, not
# merely echo committed nouns from it: the carrying sentence needs at least this
# many words that are NOT part of any occurrence of that variant's own markers.
# Precisely: three surplus words FAIL and four PASS.
# Language-neutral by construction (a token count, not a character count or an
# English pattern). It follows the existing floors in this codebase
# (`_MIN_ACKNOWLEDGED_UNKNOWN_LENGTH`, `MIN_REASONED_RESPONSE_LENGTH`,
# `_MIN_STRUCTURED_WORDS`) rather than introducing a new kind of threshold.
#
# Two things it does NOT do, stated rather than implied: a genuine but very
# terse explanation of four words or fewer beyond the markers is missed, and an
# irrelevant sentence that merely happens to contain a marker plus ordinary
# prose still counts. Neither is solved here — general paraphrase and clause
# interpretation are out of this slice's scope.
_MIN_CARRIER_CONTEXT_WORDS = 4


# ==========================================================================
# T2-G-2 (`T2G-CONCISE-MIXED-IMPLEMENT-02`) — the FINITE vocabularies for the
# concise/mixed rule. Declared centrally here and scoped to the T2-G-2 engine
# contract version ONLY: under every earlier version none of them is consulted
# and sentence handling is exactly what it was. No new registry file, no broad
# domain lexicon, no global normalisation, and no competing ignorance list —
# registered ignorance detection stays the single owner of that question.
# ==========================================================================

# Standalone CONTRAST boundaries, and only these four. `and` / `و` are
# deliberately NOT boundaries: a prototype that split them scored worse than
# the accepted rule, because `و` is a word-initial letter in Arabic. The
# prefixed Arabic form `ولكن` is not recognised in this slice — a disclosed
# limit, not an oversight.
_T2G2_CONTRAST_EN = ("but", "however")
_T2G2_CONTRAST_AR = ("لكن", "لكنّ")

# HYPOTHETICAL / non-assertive constructions. A clause carrying one of these is
# never admitted as an independent explanation by the new path, so splitting can
# not turn a supposition into support.
_T2G2_HYPOTHETICAL_EN = ("if ", "suppose", "imagine", "hypothetic", "would ",
                         "might ", "maybe", "perhaps", "probably")
_T2G2_HYPOTHETICAL_AR = ("لو ", "إذا ", "اذا ", "لنفترض", "ربما", "لعل")

# CLOSED function-word list. Used only to size a NEWLY admitted concise
# fragment; it never changes matching, relevance or quality.
_T2G2_STOPWORDS_EN = frozenset({
    "the", "a", "an", "of", "to", "into", "in", "on", "at", "by", "for",
    "from", "with", "and", "or", "is", "are", "was", "were", "be", "been",
    "it", "its", "this", "that", "these", "those", "there", "here", "then",
    "so", "as", "up", "down", "out", "over", "my", "your", "his", "her",
    "their", "our", "i", "you", "he", "she", "they", "we", "do", "does",
    "did", "not", "no", "can", "could", "will", "just", "also", "but",
    "however", "very", "only", "all", "any", "some", "each", "which", "how",
})
_T2G2_STOPWORDS_AR = frozenset({
    "ال", "من", "إلى", "الى", "في", "على", "عن", "ثم", "و", "أو", "او",
    "هو", "هي", "هذا", "هذه", "ذلك", "التي", "الذي", "مع", "عند", "لكن",
    "قد", "كان", "كانت", "لا", "ما", "كل", "أي", "اي", "بين", "حتى",
})

# RELATION tokens: the component/flow/function verbs a mechanism explanation
# uses to connect roles. A relation may sit INSIDE a committed marker (for
# example `transfers force`); repeated markers alone still carry no relation
# pattern, because a pattern needs role material on BOTH sides of the relation.
_T2G2_RELATIONS_EN = frozenset({
    "transfers", "transfer", "carries", "carry", "moves", "move", "presses",
    "press", "pushes", "push", "pulls", "pull", "rotates", "rotate", "drives",
    "drive", "connects", "connect", "holds", "hold", "locks", "lock", "sends",
    "send", "reads", "read", "triggers", "trigger", "converts", "convert",
    "runs", "run", "flows", "flow", "supports", "support", "guides", "guide",
    "switches", "switch", "measures", "measure", "detects", "detect",
})
_T2G2_RELATIONS_AR = frozenset({
    "ينقل", "تنقل", "ينتقل", "تنتقل", "يحمل", "تحمل", "يحرك", "تحرك",
    "يدفع", "تدفع", "يسحب", "تسحب", "يدور", "تدور", "يثبت", "تثبت",
    "يقفل", "تقفل", "يرسل", "ترسل", "يحول", "تحول", "يقرأ", "تقرأ",
    "يقيس", "تقيس", "يكشف", "تكشف", "يوصل", "توصل", "يسند", "تسند",
})

# ==========================================================================
# `PR643-T2G2-SCOPE-REPAIR-01` — GOVERNING SCOPE.
#
# Splitting a sentence at a contrast boundary does not, on its own, make what
# sits on the other side an independent assertion by the inventor. Four kinds
# of scope survive an allowed boundary, and each is decided by where the cue
# actually sits relative to the mechanism material — never by the bare presence
# of a pronoun, a reporting word or a quotation mark. All four are consulted by
# the T2-G-2 path ONLY: no earlier version, and no level-1 result, can be
# withdrawn by any of them.
# ==========================================================================

# ANAPHORA — surfaces that point BACK at something already said instead of
# naming a subject of their own. Presence alone decides nothing: it matters
# only inside a recognised ignorance clause that names none of THIS question's
# committed markers (see `_t2g2_back_reference_index`).
_T2G2_ANAPHORA_EN = frozenset({"that", "this", "it", "these", "those", "so"})
_T2G2_ANAPHORA_AR = frozenset({
    "ذلك", "هذا", "هذه", "تلك", "ذاك", "بذلك", "به", "بها", "كذلك",
})

# REPORTED-SPEECH frames. A clause is reported only when the frame stands
# BEFORE this question's committed material in that clause, so it actually
# governs it — "the sensor reads the pressure" is not hearsay, and a frame in a
# neighbouring clause never reaches across.
_T2G2_REPORTED_EN = ("they say", "they said", "he says", "he said", "she says",
                     "she said", "someone said", "it is said", "i read",
                     "i heard", "supposedly", "allegedly", "reportedly")
_T2G2_REPORTED_AR = ("يقولون", "يقول", "قيل", "يقال", "سمعت", "قرأت")

# QUOTATION pairs. Only material quoted IN ITS ENTIRETY is someone else's
# words; a quoted component name inside a clause the inventor is asserting
# (the deck NAMED IN QUOTES, transferring force into the rail) is untouched.
# The ASCII apostrophe and the typographic single quote are deliberately NOT
# quotation marks here: in English they are apostrophes ("don't", "the latch's
# pin"), and pairing them would invent quotations that are not there.
_T2G2_QUOTE_PAIRS = (('"', '"'), ("“", "”"), ("«", "»"))
_T2G2_CLAUSE_EDGE = " \t\r\n,،.؛;:—-"

# SUBORDINATING hypothetical openers — the subset of the registered
# hypothetical cues that opens a protasis and therefore still governs what
# follows it in the same sentence. The modal cues ("would", "might", "maybe",
# "perhaps", "probably", "ربما", "لعل") stay clause-local, exactly as
# accepted, because they qualify only their own clause.
_T2G2_SUBORDINATING_HYPOTHETICAL = ("if", "suppose", "imagine",
                                    "لو", "إذا", "اذا", "لنفترض")

# INTERROGATIVE terminators. A question is not an assertion; the terminator is
# read from the ORIGINAL text (see `_sentence_records`) rather than guessed
# from a fragment whose delimiter was already discarded.
_T2G2_INTERROGATIVE = ("?", "؟")


def _english_unknown_markers():
    """The EXISTING registered English explicit-unknown markers, read from
    their owner. Lazy so the import graph stays acyclic in both orders."""
    from engine.progression_loop import _ACKNOWLEDGED_UNKNOWN_MARKERS
    return _ACKNOWLEDGED_UNKNOWN_MARKERS


def _sentence_records(text):
    """The bounded split, WITH each segment's own original terminator.

    `PR643-T2G2-SCOPE-REPAIR-01`: the T2-G-2 path must be able to tell an
    assertion from a question, and the terminator that decides it was being
    thrown away by the split. Each record is ``(segment, terminator)`` where
    the terminator is the exact boundary text that ended that segment (``""``
    at the end of the input). The segments are IDENTICAL to what the previous
    split produced — `sentences` below is defined from these records, so every
    existing consumer, and the whole level-1 rule, are byte-unchanged."""
    if not isinstance(text, str) or not text:
        return ()
    records = []
    position = 0
    for match in _SENTENCE_BOUNDARY_RE.finditer(text):
        segment = text[position:match.start()]
        if segment.strip():
            records.append((segment, match.group(0), position))
        position = match.end()
    tail = text[position:]
    if tail.strip():
        records.append((tail, "", position))
    return tuple(records)


def sentences(text):
    """The bounded sentence split used by this module only. Public behaviour
    is unchanged: exactly the segments `_sentence_records` yields."""
    return tuple(segment for segment, _terminator, _offset in _sentence_records(text))


def _t2g2_quote_spans(text):
    """Character spans of ``text`` enclosed in a MATCHED quotation pair.

    One left-to-right pass; an unmatched opener ends the scan rather than
    guessing an extent. Used to tell whether a whole segment is someone else's
    quoted sentence, which a segment boundary inside the quotation would
    otherwise hide."""
    if not isinstance(text, str) or not text:
        return ()
    closers = dict(_T2G2_QUOTE_PAIRS)
    spans = []
    index = 0
    while index < len(text):
        closing = closers.get(text[index])
        if closing is None:
            index += 1
            continue
        end = text.find(closing, index + 1)
        if end == -1:
            break
        spans.append((index, end + 1))
        index = end + 1
    return tuple(spans)


def _t2g2_segment_is_quoted(segment, offset, quote_spans):
    """True when this segment's whole non-space extent lies inside one quoted
    span of the original answer."""
    if not quote_spans:
        return False
    lead = len(segment) - len(segment.lstrip())
    trail = len(segment) - len(segment.rstrip())
    start = offset + lead
    end = offset + len(segment) - trail
    return any(span_start <= start and end <= span_end
               for span_start, span_end in quote_spans)


def declares_ignorance(sentence):
    """True when THIS sentence carries a REGISTERED explicit-unknown surface
    on either language. Uses the existing English marker tuple and the
    existing Arabic normalising detector — no new vocabulary, and neither
    consumer's own behaviour is touched."""
    if not isinstance(sentence, str) or not sentence:
        return False
    lowered = sentence.lower()
    for marker in _english_unknown_markers():
        if marker in lowered:
            return True
    return detect_registered_unknown(sentence) is not None


def _committed_markers(question_id):
    """This variant's OWN committed marker surfaces, read from the canonical
    W2-C table. Lazy so the import graph stays acyclic in both orders; the
    table is never copied, extended or reinterpreted here, and matching
    semantics stay exactly the caller's."""
    from engine.intent_serving import _INTENT_MARKERS
    return _INTENT_MARKERS.get(question_id)


def _lowered_to_original(sentence, lowered):
    """Index map from positions in ``lowered`` back to positions in
    ``sentence``, or ``None`` when it cannot be built exactly.

    ``str.lower()`` is not always length-preserving: lowercasing U+0130 (LATIN
    CAPITAL LETTER I WITH DOT ABOVE) yields TWO code points, so every English
    match found after one sits at a larger index in the lowered text than in the
    original. Word spans are measured on the ORIGINAL sentence, so the two
    coordinate systems must be reconciled before anything is merged or counted.

    The map is built per character, which is exact here: the lowercase of a
    single character is never shorter than one character, so when the two
    strings are the same length every position corresponds one-to-one (the fast
    path below), and otherwise each character's own expansion gives its origin.
    A returned index is the ORIGINAL character that produced that lowered
    position, so a match landing inside an expansion is attributed to the whole
    original character — the conservative reading.

    The input is never modified, normalised, filtered or re-cased for matching:
    ``lowered`` stays exactly ``sentence.lower()`` and remains the only haystack
    the English surfaces are searched in."""
    origin = []
    for index, character in enumerate(sentence):
        origin.extend([index] * len(character.lower()))
    if len(origin) != len(lowered):
        # Defensive: some future context-dependent casing whose whole-string
        # result is not the per-character concatenation in LENGTH. Refuse to
        # guess coordinates rather than report wrong ones.
        return None
    return origin


def _marker_spans(sentence, question_id):
    """Every character span of the ORIGINAL ``sentence`` occupied by an
    occurrence of this variant's committed markers, merged so overlapping and
    adjacent occurrences are counted ONCE.

    English surfaces are matched against the whole-string ``sentence.lower()``,
    exactly as ``_matches_intent`` does — the match DECISION is unchanged — and
    each match is then mapped back to its original character span. Arabic
    surfaces are matched verbatim against the original text and need no
    mapping. Each marker is scanned with ``str.find`` and the marker set per
    question is fixed and small; the index map is one bounded local pass and is
    built only when lowercasing actually changed the length. Measured cost is
    reported in the candidate evidence; no window enumeration, no repeated
    joins, no truncation and no cache."""
    entry = _committed_markers(question_id)
    if entry is None:
        return ()
    english, arabic = entry
    lowered = sentence.lower()
    if len(lowered) == len(sentence):
        origin = None                     # indices already align one-to-one
    else:
        origin = _lowered_to_original(sentence, lowered)
        if origin is None:
            return ()                     # coordinates unknown: not a carrier
    found = []
    for surfaces, haystack, remap in ((english, lowered, True),
                                      (arabic, sentence, False)):
        for surface in surfaces:
            if not surface:
                continue
            start = haystack.find(surface)
            while start != -1:
                stop = start + len(surface)
                if remap and origin is not None:
                    found.append((origin[start], origin[stop - 1] + 1))
                else:
                    found.append((start, stop))
                start = haystack.find(surface, start + 1)
    if not found:
        return ()
    found.sort()
    merged = [found[0]]
    for start, end in found[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:                       # overlapping or touching
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))
    return tuple(merged)


def _carries_context(sentence, question_id, matches_intent):
    """True when the sentence says something BEYOND this variant's markers.

    EVERY occurrence of every one of that variant's markers is discounted —
    repetitions and combinations included, and overlapping occurrences counted
    once — so a bare component name never becomes explanatory context merely by
    being repeated. A word counts as surplus only when it lies wholly outside
    the merged marker spans.

    Sizing is a small number of bounded passes over the sentence for the fixed
    committed marker set — measured, not asserted as a complexity class. The
    caller has already decided that the sentence matches; this only sizes what
    else the sentence says, and never widens or narrows the match itself."""
    spans = _marker_spans(sentence, question_id)
    if not spans:
        # The caller matched but this variant's canonical markers are not
        # readable here (an unknown id, or a table that cannot be loaded). Not
        # a carrier: the safe direction is to leave the question owed an
        # answer, never to grant progress on evidence we cannot size.
        return False
    surplus = 0
    for word in _WORD_RE.finditer(sentence):
        start, end = word.span()
        if not any(span_start <= start and end <= span_end
                   for span_start, span_end in spans):
            surplus += 1
            if surplus >= _MIN_CARRIER_CONTEXT_WORDS:
                return True
    return False


_T2G2_CONTRAST_RE = re.compile(
    r"\b(?:%s)\b" % "|".join(
        re.escape(cue) for cue in _T2G2_CONTRAST_EN + _T2G2_CONTRAST_AR))


def _t2g2_clauses(sentence):
    """Split ONE sentence at standalone contrast boundaries only.

    Exactly the four registered contrast tokens, each matched as a WHOLE token,
    so no substring inside a word is ever a boundary and no other conjunction
    is split. A sentence without a contrast boundary comes back unchanged, so
    this can only ever add clauses to look at.

    Boundaries are located in ``sentence.lower()`` — the same whole-string
    lowercase haystack the committed matcher uses, so no case-insensitive
    matching mode and no re-casing of the input is introduced — and then mapped
    back to ORIGINAL character offsets through the accepted coordinate map
    before the original text is cut. The returned clauses are therefore exact
    substrings of the inventor's own words."""
    lowered = sentence.lower()
    if len(lowered) == len(sentence):
        origin = None                     # indices already align one-to-one
    else:
        origin = _lowered_to_original(sentence, lowered)
        if origin is None:
            return (sentence,)            # coordinates unknown: do not cut
    cuts = []
    for match in _T2G2_CONTRAST_RE.finditer(lowered):
        start, stop = match.span()
        if origin is None:
            cuts.append((start, stop))
        else:
            cuts.append((origin[start], origin[stop - 1] + 1))
    if not cuts:
        return (sentence,)
    parts = []
    previous = 0
    for start, stop in cuts:
        parts.append(sentence[previous:start])
        previous = stop
    parts.append(sentence[previous:])
    return tuple(part for part in parts if part.strip())


def _t2g2_is_hypothetical(clause):
    """True when the clause is a supposition rather than an assertion. A
    hypothetical clause is never admitted as an independent explanation, so a
    split can not turn `I do not know, but it would probably transfer force`
    into support."""
    lowered = clause.lower()
    if any(cue in lowered for cue in _T2G2_HYPOTHETICAL_EN):
        return True
    return any(cue in clause for cue in _T2G2_HYPOTHETICAL_AR)


def _t2g2_has_anaphor(clause):
    """True when the clause contains a whole-token surface that points BACK at
    something already said. On its own this decides NOTHING — it is one of two
    conditions in `_t2g2_back_reference_index`."""
    for word in _WORD_RE.finditer(clause):
        token = word.group(0)
        if token.lower() in _T2G2_ANAPHORA_EN or token in _T2G2_ANAPHORA_AR:
            return True
    return False


def _t2g2_back_reference_index(clauses, question_id):
    """Index of the first clause whose recognised ignorance refers BACK at what
    was already said, or ``None``.

    Both conditions must hold, so a pronoun alone is never a veto:

      1. the clause carries a REGISTERED explicit unknown (the existing
         detector, unchanged); and
      2. it names NONE of this question's committed markers — it supplies no
         subject matter of its own — while carrying an anaphor.

    "…but I do not know if that is right" satisfies both: the doubt is about
    the sibling clause, so that clause is not an independent assertion. "I do
    not know the bolt size but…" satisfies neither — the uncertainty names its
    own, separate detail — and "…but I do not know if that load path is right"
    names committed material, so it is left alone too. Only clauses BEFORE the
    back-reference lose their new-support eligibility; a clause after it is a
    fresh statement and is judged normally."""
    for index, clause in enumerate(clauses):
        if not declares_ignorance(clause):
            continue
        if _marker_spans(clause, question_id):
            continue
        if _t2g2_has_anaphor(clause):
            return index
    return None


def _t2g2_is_reported(clause, spans):
    """True when a reported-speech frame actually GOVERNS this clause's
    mechanism material — the frame stands before this question's first
    committed marker in the same clause. A reporting word elsewhere, or in a
    neighbouring clause, does not reach it."""
    if not spans:
        return False
    limit = spans[0][0]
    lowered = clause.lower()
    for cue in _T2G2_REPORTED_EN:
        position = lowered.find(cue)
        if 0 <= position < limit:
            return True
    for cue in _T2G2_REPORTED_AR:
        position = clause.find(cue)
        if 0 <= position < limit:
            return True
    return False


def _t2g2_is_wholly_quoted(clause):
    """True only when the WHOLE clause is enclosed in one quotation pair —
    someone else's sentence. A quoted component name inside an otherwise
    unquoted clause is untouched, so quotation is never a blanket veto."""
    stripped = clause.strip(_T2G2_CLAUSE_EDGE)
    if len(stripped) < 2:
        return False
    return any(stripped.startswith(opening) and stripped.endswith(closing)
               for opening, closing in _T2G2_QUOTE_PAIRS)


def _t2g2_opens_hypothetical(clause):
    """True when the clause OPENS a supposition, which therefore still governs
    the clauses after it in the same sentence. Clause-internal modal cues are
    not included here: they qualify only their own clause, which
    `_t2g2_is_hypothetical` already handles."""
    stripped = clause.strip(_T2G2_CLAUSE_EDGE)
    lowered = stripped.lower()
    for cue in _T2G2_SUBORDINATING_HYPOTHETICAL:
        for candidate in (lowered, stripped):
            if candidate.startswith(cue) and candidate[len(cue):len(cue) + 1].isspace():
                return True
    return False


def _t2g2_is_questioned(terminator):
    """True when the segment the clause came from ended in a question mark, in
    either script. Read from the ORIGINAL terminator carried by
    `_sentence_records`, never reconstructed from the fragment."""
    if not terminator:
        return False
    return any(mark in terminator for mark in _T2G2_INTERROGATIVE)


def _t2g2_role_items(clause, spans):
    """The role material of a clause as ``(start, end, kind)`` triples: each
    committed-marker occurrence, and each non-stopword word lying wholly
    outside every marker span. Stopwords and digits carry no role."""
    items = [(start, end, "marker") for start, end in spans]
    for word in _WORD_RE.finditer(clause):
        start, end = word.span()
        if any(s <= start and end <= e for s, e in spans):
            continue
        token = word.group(0)
        if token.lower() in _T2G2_STOPWORDS_EN or token in _T2G2_STOPWORDS_AR:
            continue
        items.append((start, end, "word"))
    return items


def _t2g2_concise_pattern(clause, question_id):
    """True when a SHORT clause states a relation between roles.

    The clause must contain a registered relation token — which may sit inside
    a committed marker — with role material on BOTH sides of it, and at least
    one non-marker content word somewhere in the clause. That is what
    separates a short real explanation from a committed noun echoed three
    times: repeated markers supply no relation and no non-marker content, so
    they can never satisfy this. Two arbitrary content words do not satisfy
    it either, and neither does a relation with nothing on one side of it."""
    spans = _marker_spans(clause, question_id)
    if not spans:
        return False
    items = _t2g2_role_items(clause, spans)
    if not any(kind == "word" for _s, _e, kind in items):
        return False                       # markers alone: no explanation
    for word in _WORD_RE.finditer(clause):
        token = word.group(0)
        if token.lower() not in _T2G2_RELATIONS_EN and token not in _T2G2_RELATIONS_AR:
            continue
        start, end = word.span()
        left = [i for i in items if i[1] <= start]
        right = [i for i in items if i[0] >= end]
        if not left or not right:
            continue                       # a relation with an empty side
        if len(left) == 1 and len(right) == 1 and left[0] == right[0]:
            continue                       # the same single role on both sides
        return True
    return False


def _t2g2_clause_carrier(sentence, question_id, matches_intent, terminator="",
                         quoted=False):
    """The T2-G-2 addition: judge each contrast clause of the sentence on its
    own, so an explanation that shares a sentence with a recognised unknown is
    not discarded with it, and a concise clause can qualify through the
    relation pattern.

    A clause becomes NEW support only when nothing still governs it. Crossing a
    contrast boundary does not clear scope, so `PR643-T2G2-SCOPE-REPAIR-01`
    establishes the governing scope first, at four points:

      * the whole segment was a QUESTION (its own original terminator) — a
        question asks for the mechanism, it does not state one;
      * a recognised ignorance clause later in the sentence refers BACK at this
        clause, so this clause is what is being doubted;
      * a subordinating supposition opened EARLIER in the sentence and still
        governs here;
      * this clause, or the whole segment it came from, is quoted in its
        entirety, or the clause is reported speech.

    Ignorance-cued and clause-local hypothetical clauses are skipped as before.
    Every refusal here removes only NEW T2-G-2 support: the level-1 rule has
    already run on the whole sentence in `qualifying_carrier` and is never
    revisited, so no older or default result can be withdrawn."""
    if quoted or _t2g2_is_questioned(terminator):
        return False
    clauses = _t2g2_clauses(sentence)
    if len(clauses) == 1 and not _t2g2_concise_pattern(clauses[0], question_id):
        # No contrast boundary and no concise pattern: nothing new to add.
        return False
    back_reference = _t2g2_back_reference_index(clauses, question_id)
    supposed = False
    for index, clause in enumerate(clauses):
        governed = supposed
        if _t2g2_opens_hypothetical(clause):
            supposed = True
        if declares_ignorance(clause) or _t2g2_is_hypothetical(clause):
            continue
        if governed:
            continue                      # inside a supposition opened earlier
        if back_reference is not None and index < back_reference:
            continue                      # this is what the doubt is about
        if _t2g2_is_wholly_quoted(clause):
            continue
        if not matches_intent(clause, question_id):
            continue
        spans = _marker_spans(clause, question_id)
        if _t2g2_is_reported(clause, spans):
            continue
        if _carries_context(clause, question_id, matches_intent):
            return True
        if _t2g2_concise_pattern(clause, question_id):
            return True
    return False


def qualifying_carrier(text, question_id, matches_intent, rule_level=1):
    """True when ``text`` carries THIS question's committed intent markers,
    WITHOUT declaring ignorance alongside them, and says something beyond the
    marker itself.

    ``matches_intent`` is the caller's own committed-marker predicate — this
    module never imports or reimplements it, and never changes its meaning.
    Question-specific by construction: a carrier for one variant says nothing
    about any other variant.

    ``rule_level`` defaults to 1, which is exactly the accepted T2-G-1 rule:
    whole-sentence scope, four surplus words. Every existing direct caller
    therefore keeps its behaviour unchanged. Level 2 (the T2-G-2 engine
    contract) adds the contrast-clause and concise-relation paths as a UNION on
    top — it can only admit explanations level 1 already misses, never withdraw
    one it already accepts. Any failure inside the new path falls back to the
    level-1 answer, so a failed T2-G-2 interpretation never grants support of
    its own."""
    quote_spans = ()
    if rule_level >= 2:
        try:
            quote_spans = _t2g2_quote_spans(text)
        except Exception:
            # The governing scope of this answer cannot be read. Fall back to
            # the level-1 rule for the whole text rather than grant new support
            # on evidence we could not size.
            rule_level = 1
    for sentence, terminator, offset in _sentence_records(text):
        if not declares_ignorance(sentence) and matches_intent(sentence, question_id) \
                and _carries_context(sentence, question_id, matches_intent):
            return True
        if rule_level >= 2:
            try:
                if _t2g2_clause_carrier(
                        sentence, question_id, matches_intent,
                        terminator=terminator,
                        quoted=_t2g2_segment_is_quoted(sentence, offset,
                                                       quote_spans)):
                    return True
            except Exception:
                continue          # conservative: no new support from a failure
    return False


def t2g_rule_level(state, gap_type=None, domain=None):
    """The T-2-G rule level this project runs under: 0, 1 or 2.

    Read from the project's OWN persisted engine-contract version — never from
    a request field, the UI language, a timestamp or a default. An absent,
    unknown or pre-T2-G stamp gives 0, so an unversioned runtime or test state
    can never silently enable any of this. Level 1 is the accepted T2-G-1 rule
    exactly; level 2 adds the bounded concise/mixed paths for T2-G-2 projects
    only. Outside the named gap and domains the level is 0 at every version."""
    from engine.session_reconstruction import (
        ENGINE_CONTRACT_VERSION_T2G1, ENGINE_CONTRACT_VERSION_T2G2)
    levels = {ENGINE_CONTRACT_VERSION_T2G1: 1, ENGINE_CONTRACT_VERSION_T2G2: 2}
    level = levels.get(getattr(state, "engine_contract_version", None), 0)
    if not level:
        return 0
    if gap_type is not None and gap_type not in T2G_SCOPED_GAPS:
        return 0
    resolved = domain if domain is not None else getattr(state, "domain", None)
    return level if resolved in T2G_SCOPED_DOMAINS else 0


def is_t2g_active(state, gap_type=None, domain=None):
    """True when ANY T-2-G rule level applies. Signature and meaning preserved
    for existing callers; the level itself is read through
    ``t2g_rule_level``."""
    return t2g_rule_level(state, gap_type=gap_type, domain=domain) > 0


def covers_variant(state, text, question_id, matches_intent, domain=None,
                   gap_type=MECHANISM_COMPLETENESS):
    """PURPOSE-AWARE coverage for ONE committed variant.

    Legacy/out-of-scope: exactly today's committed-marker result.
    In scope: a knowledge-seeking variant is covered only by a qualifying
    carrier; an uncertainty-seeking variant keeps its existing coverage when
    otherwise matched, because naming the uncertainty IS its answer."""
    if not matches_intent(text, question_id):
        return False
    level = t2g_rule_level(state, gap_type=gap_type, domain=domain)
    if not level:
        return True
    if question_id in UNCERTAINTY_QUESTION_IDS:
        return True
    return qualifying_carrier(text, question_id, matches_intent, rule_level=level)


def explicit_unknown_without_mechanism(state, gap_type, response,
                                       detect_unknown, variant_ids,
                                       matches_intent):
    """The SATISFACTION-ELIGIBILITY veto — never a relevance or quality result.

    True only when ALL of these hold, each on positive evidence:
      1. a T2-G rule level applies (the project's own version, and the named
         gap/domain scope) — and the SAME level governs the carrier test, so
         eligibility and coverage can never read an answer differently;
      2. the EXISTING acknowledged-unknown detector recognises an explicit
         unknown in this answer, under ITS OWN declared bounds (registered
         phrasings, minimum length) — an unrecognised phrasing is simply not
         a recognised unknown here either;
      3. no KNOWLEDGE-SEEKING committed variant of this gap has a qualifying
         carrier anywhere in the answer.

    The uncertainty-seeking variants are excluded from (3) deliberately:
    identifying a missing detail answers those questions but supplies no
    mechanism, so it must not defeat the veto."""
    level = t2g_rule_level(state, gap_type=gap_type)
    if not level:
        return False
    if detect_unknown(response) is None:
        return False
    for question_id in variant_ids:
        if question_id in UNCERTAINTY_QUESTION_IDS:
            continue
        if qualifying_carrier(response, question_id, matches_intent,
                              rule_level=level):
            return False
    return True
