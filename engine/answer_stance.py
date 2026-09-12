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


def _english_unknown_markers():
    """The EXISTING registered English explicit-unknown markers, read from
    their owner. Lazy so the import graph stays acyclic in both orders."""
    from engine.progression_loop import _ACKNOWLEDGED_UNKNOWN_MARKERS
    return _ACKNOWLEDGED_UNKNOWN_MARKERS


def sentences(text):
    """The bounded sentence split used by this module only."""
    if not isinstance(text, str) or not text:
        return ()
    return tuple(part for part in _SENTENCE_BOUNDARY_RE.split(text) if part.strip())


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


def _marker_spans(sentence, question_id):
    """Every character span of ``sentence`` occupied by an occurrence of this
    variant's committed markers, merged so overlapping and adjacent occurrences
    are counted ONCE.

    Cost is linear in the sentence length for the fixed committed marker set:
    each marker is scanned once with ``str.find``, and the marker set per
    question is fixed and small. No window enumeration and no repeated joins."""
    entry = _committed_markers(question_id)
    if entry is None:
        return ()
    english, arabic = entry
    lowered = sentence.lower()
    found = []
    for surfaces, haystack in ((english, lowered), (arabic, sentence)):
        for surface in surfaces:
            if not surface:
                continue
            start = haystack.find(surface)
            while start != -1:
                found.append((start, start + len(surface)))
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

    Linear in the sentence length for the fixed committed marker set. The
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


def qualifying_carrier(text, question_id, matches_intent):
    """True when some sentence of ``text`` carries THIS question's committed
    intent markers, WITHOUT declaring ignorance in the same sentence, and says
    something beyond the marker itself.

    ``matches_intent`` is the caller's own committed-marker predicate — this
    module never imports or reimplements it, and never changes its meaning.
    Question-specific by construction: a carrier for one variant says nothing
    about any other variant."""
    for sentence in sentences(text):
        if declares_ignorance(sentence):
            continue
        if not matches_intent(sentence, question_id):
            continue
        if _carries_context(sentence, question_id, matches_intent):
            return True
    return False


def is_t2g_active(state, gap_type=None, domain=None):
    """True only for a state whose PERSISTED engine-contract version is the
    T2-G one, inside the named gap/domain scope. Absent, unknown or legacy
    version -> False, so an unversioned runtime or test state can never
    silently enable the new rule."""
    from engine.session_reconstruction import ENGINE_CONTRACT_VERSION_T2G1
    if getattr(state, "engine_contract_version", None) != ENGINE_CONTRACT_VERSION_T2G1:
        return False
    if gap_type is not None and gap_type not in T2G_SCOPED_GAPS:
        return False
    resolved = domain if domain is not None else getattr(state, "domain", None)
    return resolved in T2G_SCOPED_DOMAINS


def covers_variant(state, text, question_id, matches_intent, domain=None,
                   gap_type=MECHANISM_COMPLETENESS):
    """PURPOSE-AWARE coverage for ONE committed variant.

    Legacy/out-of-scope: exactly today's committed-marker result.
    In scope: a knowledge-seeking variant is covered only by a qualifying
    carrier; an uncertainty-seeking variant keeps its existing coverage when
    otherwise matched, because naming the uncertainty IS its answer."""
    if not matches_intent(text, question_id):
        return False
    if not is_t2g_active(state, gap_type=gap_type, domain=domain):
        return True
    if question_id in UNCERTAINTY_QUESTION_IDS:
        return True
    return qualifying_carrier(text, question_id, matches_intent)


def explicit_unknown_without_mechanism(state, gap_type, response,
                                       detect_unknown, variant_ids,
                                       matches_intent):
    """The SATISFACTION-ELIGIBILITY veto — never a relevance or quality result.

    True only when ALL of these hold, each on positive evidence:
      1. the T2-G version and the named gap/domain scope are active;
      2. the EXISTING acknowledged-unknown detector recognises an explicit
         unknown in this answer, under ITS OWN declared bounds (registered
         phrasings, minimum length) — an unrecognised phrasing is simply not
         a recognised unknown here either;
      3. no KNOWLEDGE-SEEKING committed variant of this gap has a qualifying
         carrier anywhere in the answer.

    The uncertainty-seeking variants are excluded from (3) deliberately:
    identifying a missing detail answers those questions but supplies no
    mechanism, so it must not defeat the veto."""
    if not is_t2g_active(state, gap_type=gap_type):
        return False
    if detect_unknown(response) is None:
        return False
    for question_id in variant_ids:
        if question_id in UNCERTAINTY_QUESTION_IDS:
            continue
        if qualifying_carrier(response, question_id, matches_intent):
            return False
    return True
