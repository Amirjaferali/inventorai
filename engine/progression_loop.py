"""
Progression Loop — MVP core logic.
Scope: electronics/electrical, LEVEL 0-2 only.
Governed by: MVP_SCOPE_FREEZE.md

Responsibilities:
  - Identify highest-priority open gap
  - Generate one question per iteration
  - Integrate response into IdeaState
  - Evaluate PASS / WARN / BLOCK
  - Detect stall and reframe

NOT responsible for:
  - Domain rule enforcement (domain_rules.py)
  - Scoring (engine/scoring.py)
  - Replay (scripts/)
"""

import re
import warnings
from engine.domain_rules import (
    get_substance_signals, get_substance_signal_plural_aliases, is_known_domain,
)
from engine.gap_relevance import addresses_gap
from engine.semantic_registry import (
    has_registered_causal_structure, substance_surface_present,
    detect_registered_unknown, normalize_ar,
)
from engine.idea_state import (
    IdeaState, Evidence, Gap, IterationLog, AcknowledgedUnknown,
    PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY, MECHANISM_COMPLETENESS,
    PROBLEM_MECHANISM_FIT, ASSUMPTION_INVENTORY, EXPERTISE_GAP_AWARENESS,
    STAGE_2_GAP_TYPES, STAGE_3_GAP_TYPES,
    OPEN, PARTIAL, CLOSED, ACCEPTED_RISK,
    ASSERTED, REASONED, DEMONSTRATED, OWNER_STATED,
    PROGRESSING, STALLED, REGRESSING
)


# --- Gap priority order (per MVP_SCOPE_FREEZE) ---
GAP_PRIORITY = [
    MECHANISM_COMPLETENESS,
    PHYSICAL_FEASIBILITY,
    BOUNDARY_AMBIGUITY,
]

# Stage 3 gap priority (per STAGE3_GAP_TAXONOMY_PROPOSAL)
# PMF must be attempted before AI; AI before EGA
STAGE3_GAP_PRIORITY = [
    PROBLEM_MECHANISM_FIT,
    ASSUMPTION_INVENTORY,
    EXPERTISE_GAP_AWARENESS,
]

STALL_THRESHOLD = 3  # iterations before reframe

_IDEA_SUMMARY_MAX = 500

def _trim_idea_summary(text: str) -> str:
    """Inventor statement safely trimmed — display safeguard, not summarization.

    When the statement exceeds the limit it is cut at a word boundary and an
    explicit ellipsis marker is appended, so the truncation is visible and never
    reads as a broken mid-phrase sentence. The full original statement remains
    available in ``state.known_problem.content``; this is a display safeguard
    only and adds no meaning.
    """
    text = text.strip()
    if len(text) <= _IDEA_SUMMARY_MAX:
        return text
    trimmed = text[:_IDEA_SUMMARY_MAX]
    boundary = trimmed.rfind(" ")
    cut = trimmed[:boundary] if boundary > 0 else trimmed
    return cut.rstrip() + "…"



# ─────────────────────────────────────────────
# 1. Select next gap to address
# ─────────────────────────────────────────────

def _active_gap_priority(state: IdeaState) -> list[str]:
    """
    Return the gap-priority order for the state's current stage.

    Stage 3 (state.current_stage == 3) uses STAGE3_GAP_PRIORITY; every other
    stage uses the Stage 2 GAP_PRIORITY. This mirrors the stage-aware
    selection already performed by the no-active-gap cascade in
    run_iteration(); it introduces no new priority data and no new gap
    types. Behaviour-preserving for Stage 2 (current_stage defaults to 2).
    """
    return (
        STAGE3_GAP_PRIORITY
        if getattr(state, "current_stage", 2) == 3
        else GAP_PRIORITY
    )


def select_next_gap(state: IdeaState) -> str | None:
    """
    Return the highest-priority OPEN/PARTIAL gap_type for the active stage.
    Returns None if no open gaps exist.
    """
    open_gaps = {g.gap_type: g for g in state.gaps if g.status in (OPEN, PARTIAL)}
    for gap_type in _active_gap_priority(state):
        if gap_type in open_gaps:
            return gap_type
    return None


def _open_next_gap_if_needed(state):
    """Open the next active-stage priority gap if no OPEN/PARTIAL gap exists. Returns gap_type or None."""
    if any(g.status in (OPEN, PARTIAL) for g in state.gaps):
        return None
    for next_gap_type in _active_gap_priority(state):
        if state.get_gap(next_gap_type) is None:
            from engine.idea_state import Gap
            gap = Gap(gap_type=next_gap_type, status=OPEN, opened_at=state.iteration)
            state.gaps.append(gap)
            return next_gap_type
    return None



# ─────────────────────────────────────────────
# 2. Generate one question for a gap
# ─────────────────────────────────────────────

QUESTIONS = {
    MECHANISM_COMPLETENESS: [
        "Describe specifically HOW your invention works — "
        "not what it achieves, but the physical or functional steps it takes.",

        "What are the individual components or actions inside your mechanism? "
        "Name each one and what it does.",

        "If someone tried to build your invention tomorrow with no further explanation, "
        "what would be missing from your current description?",
    ],
    PHYSICAL_FEASIBILITY: [
        "What physical principle does your mechanism rely on? "
        "(e.g. resistive sensing, inductive coupling, optical detection)",

        "Does your invention consume or manage energy? "
        "If yes, what is the approximate power requirement and source?",

        "What are the physical limits or constraints your mechanism must operate within? "
        "(e.g. temperature range, signal frequency, material properties)",
    ],
    BOUNDARY_AMBIGUITY: [
        "What does your invention specifically NOT do or NOT cover? "
        "State at least one clear boundary.",

        "Name one existing approach that is similar to yours. "
        "What makes yours different in a specific, concrete way?",

        "If someone tried to copy your invention by changing only one component, "
        "would it still be your invention? What is the core that cannot be replaced?",
    ],
    # ── Stage 3 questions — sourced verbatim from STAGE3_QUESTION_SET.md (admitted 5926b63) ──
    PROBLEM_MECHANISM_FIT: [
        # PMF-Q1 — Primary Evidence Target: PMF-E1
        "Without describing how your mechanism works, describe the problem you are trying to solve. "
        "What is happening for the person or system that has this problem, and why does it matter to them?",
        # PMF-Q2 — Primary Evidence Target: PMF-E2
        "Why does your mechanism solve this problem rather than a different approach? "
        "What is it about how your mechanism works that makes it the right fit for this problem?",
        # PMF-Q3 — Primary Evidence Target: PMF-E3
        "Are there situations or conditions where your mechanism would not solve this problem, "
        "or would solve it less well? What are those conditions?",
    ],
    ASSUMPTION_INVENTORY: [
        # AI-Q1 — Primary Evidence Target: AI-E1
        "What are you taking for granted about your mechanism that you have not yet tested or verified? "
        "These might be things you expect to be true, materials you assume are available, "
        "or conditions you assume will hold.",
        # AI-Q2 — Primary Evidence Target: AI-E2
        "For each assumption you named, would your mechanism still work if that assumption turned out to be wrong? "
        "Which assumptions are essential — the mechanism fails without them — "
        "and which ones would just require you to adjust your approach?",
        # AI-Q3 — Primary Evidence Target: AI-E3
        "Now that you have thought through your assumptions — is there anything you realize you were assuming "
        "that you had not recognized as an assumption before this conversation? "
        "Something that seemed obvious but is actually unverified?",
    ],
    EXPERTISE_GAP_AWARENESS: [
        # EGA-Q1 — Primary Evidence Target: EGA-E1
        "What areas of technical knowledge would someone need to actually build or implement your mechanism? "
        "List the domains of expertise required — not what you know, but what the implementation itself demands.",
        # EGA-Q2 — Primary Evidence Target: EGA-E2
        "Of the expertise areas you just identified — which ones do you have sufficient working knowledge of "
        "to proceed, and which ones represent genuine gaps where you would need to learn more or bring in someone else?",
        # EGA-Q3 — Primary Evidence Target: EGA-E3
        "For the expertise gaps you identified — what would happen to your implementation if those gaps were not "
        "addressed before you started building? What specific problems would you run into?",
    ],
}


# Deterministic, question-layer stall reframe (Increment 1 — Owner-Expert
# Question Boundary). Shown on the non-specialist Path N flow once a gap's
# approved Path N variants are exhausted, instead of repeating the final variant
# verbatim (NON_SPECIALIST_QUESTIONING_POLICY §7; MVP_SCOPE_FREEZE "reframed after
# 3 stalls"). Plain language; asks what the owner already knows and what
# information would be needed; contains no engineering-gated terminology. It is
# pure display content: it does not change gap status, evidence, maturity,
# iteration semantics, or the six owner actions, adds no new action, performs no
# I/O or LLM call, and starts no conversational / multi-question loop. A single
# deterministic reframe is sufficient for this bounded increment; the owner's
# existing six actions remain the truthful exits.
# RVR-2 (Wave-1 remediation contract): served AFTER the single reframe render,
# instead of repeating the identical reframe indefinitely (the S2 run recorded
# the same reframe re-served 18-20x). A different, stable, governed message
# that names the honest exits. Display selection only - canonical state, gap
# status, get_question(), and the six owner actions are untouched.
_EXHAUSTED_EXIT_PROMPT = (
    "The prepared questions for this area are exhausted, and repeating them "
    "will not move it forward. Your honest options now: add genuinely new "
    "information in the answer box; mark this unknown or deferred; note a "
    "provisional assumption; ask for a specialist or evidence; or - if it "
    "cannot be resolved now - accept it explicitly as a known risk so the "
    "journey can move on while the risk stays visibly recorded."
)

_STALL_REFRAME = (
    "Let's take this part in plainer terms. In your own words, what do you "
    "already know about this aspect of your idea — and what information do you "
    "think you would need, or who could help you find it, to work out the rest? "
    "If you are not sure, you can also use the options below to mark it unknown, "
    "defer it, note a provisional assumption, or ask for a specialist or evidence."
)


def get_question(domain: str, gap_type: str, iterations_open: int,
                 path: str | None = None) -> str:
    """
    Select question for gap_type.
    path == "N": resolves from the approved Path N artifact
    (engine/path_n_questions.py). Gap types not covered by the artifact
    fall through to generic QUESTIONS — the explicit Stage 3 fallthrough
    (b3a5fba §8), not a hidden fallback to Path T content.
    Default / any other path value: existing behavior unchanged —
    domain layer first, generic QUESTIONS fallback.
    Framework-level delegation — no domain-specific logic here.

    Pure selector: this returns the approved/clamped variant for the position and
    deliberately performs NO stall reframe, so the Path N artifact-selection
    invariant is preserved. The owner-facing stall reframe is applied separately
    by get_display_question() (used by the web session view).
    """
    if path == "N":
        from engine.path_n_questions import get_path_n_question
        # P9-E1: propagate the canonical session domain the caller already holds
        # into the domain-aware Path-N seam. A recognized non-electronics domain
        # then receives None here (seam-owned) and falls through to the generic
        # variant; Electronics and the None default are unchanged.
        path_n_q = get_path_n_question(gap_type, iterations_open, domain=domain)
        if path_n_q is not None:
            return path_n_q
        variants = QUESTIONS[gap_type]
        index = min(iterations_open, len(variants) - 1)
        return variants[index]
    from engine.domain_rules import get_domain_question
    domain_q = get_domain_question(domain, gap_type, iterations_open)
    if domain_q:
        return domain_q
    variants = QUESTIONS[gap_type]
    index = min(iterations_open, len(variants) - 1)
    return variants[index]


def get_display_question(domain: str, gap_type: str, iterations_open: int,
                         path: str | None = None) -> str:
    """Owner-facing question for the current gap, with the Increment 1 stall
    reframe applied (Owner-Expert Question Boundary).

    Identical to get_question(), except that on the non-specialist Path N flow
    (path == "N"), once a Stage 2 gap's approved Path N variants are exhausted —
    i.e. get_question() would otherwise repeat the final variant verbatim — the
    deterministic plain-language reframe (_STALL_REFRAME) is returned instead
    (NON_SPECIALIST_QUESTIONING_POLICY §7; MVP_SCOPE_FREEZE "reframed after 3
    stalls"). This is the function the web session view uses to render the
    displayed question; get_question() itself stays a pure selector so the
    approved Path N artifact-selection invariant is unchanged.

    Pure display selection: no engine state, gap status, evidence, maturity,
    iteration semantics, or owner action is changed; no persistence, I/O, or LLM
    call is performed; the approved artifact is not modified. A single
    deterministic reframe is sufficient — the existing six owner actions remain
    the truthful exits.
    """
    if path == "N" and iterations_open > 0:
        from engine.path_n_questions import get_path_n_question
        # P9-E1: propagate the canonical session domain into the domain-aware
        # Path-N seam for the exhaustion comparison too. For a recognized
        # non-electronics domain both reads are None, so the Electronics-specific
        # stall reframe is correctly NOT fired and control falls through to the
        # generic variant; Electronics and the None default are unchanged.
        current = get_path_n_question(gap_type, iterations_open, domain=domain)
        # Path N serves Stage 2 gaps; a clamp (current == the previous
        # iteration's question) marks variant exhaustion → reframe instead of a
        # verbatim repeat. Stage 3 gaps return None here and are unaffected.
        if current is not None and current == get_path_n_question(
            gap_type, iterations_open - 1, domain=domain
        ):
            # RVR-2: the reframe is served exactly ONCE (the first exhausted
            # render). Every later exhausted render serves the deterministic
            # exit prompt instead of re-serving the identical reframe - the
            # governed reason the question changes is that the variants are
            # exhausted and the honest exits are now the productive path.
            if iterations_open >= 2 and current == get_path_n_question(
                gap_type, iterations_open - 2, domain=domain
            ):
                return _EXHAUSTED_EXIT_PROMPT
            return _STALL_REFRAME
    return get_question(domain, gap_type, iterations_open, path=path)


# ─────────────────────────────────────────────
# 2b. Acknowledged unknown detection (parallel track)
# Conservative: false negatives ok, false positives not.
# Governance: TRANSITION_AUTHORIZATION_GOVERNANCE s4 Layer 1 PGC-3
# Authorization: Owner-authorized 2026-06-06
# ─────────────────────────────────────────────

_ACKNOWLEDGED_UNKNOWN_MARKERS = (
    "i do not know",
    "i don't know the",
    "i am not sure about",
    "i'm not sure about",
    "i have not yet determined",
    "i do not yet know",
    "i haven't determined",
    "i have not decided",
    "i haven't decided",
    "i am not yet sure",
    "i'm not yet sure",
    "i have not yet researched",
    "i haven't researched",
    # Fragment-capture correction (owner-authorized 2026-07-10): remaining
    # minimum supported explicit-unknown phrases. Appended AFTER the original
    # markers so category_basis resolution for previously detected responses
    # is unchanged. Explicit inventor-marked uncertainty only — the bare
    # technical word "unknown" must never match.
    "i don't know",
    "i am not sure",
    "i'm not sure",
    "it is still unknown",
    "this is not yet known",
)

_MIN_ACKNOWLEDGED_UNKNOWN_LENGTH = 40

# Deterministic sentence boundary: a terminator (. ! ?) followed by
# whitespace. Markers contain no terminators, so a matched marker can never
# span a split point.
_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")


def _extract_unknown_fragment(r, marker):
    """
    Bounded acknowledged-unknown fragment: the inventor-written sentence
    containing the explicit unknown marker, verbatim except surrounding
    whitespace. A whole response is returned only when it is a single
    sentence. Never paraphrases, never captures neighboring sentences.
    """
    sentences = [s.strip() for s in _SENTENCE_SPLIT_RE.split(r) if s.strip()]
    if len(sentences) <= 1:
        return r
    for sentence in sentences:
        if marker in sentence.lower():
            return sentence
    # Defensive fallback (unreachable for the current marker set, which
    # cannot span a split point): capture from the marker to the end of its
    # sentence rather than mislabeling the whole multi-sentence answer.
    start = r.lower().find(marker)
    tail = _SENTENCE_SPLIT_RE.split(r[start:], 1)[0].strip()
    return tail or r


def _extract_unknown_fragment_normalized(r, surface):
    """Bounded acknowledged-unknown fragment for a NORMALIZED Arabic surface.

    Identical bounding rule to ``_extract_unknown_fragment``: the inventor's own
    sentence, verbatim except surrounding whitespace, never a paraphrase and
    never a neighbouring sentence. The surface is matched against the NORMALIZED
    form of each sentence, but the VERBATIM sentence is what is returned.
    """
    sentences = [x.strip() for x in _SENTENCE_SPLIT_RE.split(r) if x.strip()]
    if len(sentences) <= 1:
        return r
    for sentence in sentences:
        if surface in normalize_ar(sentence.lower()):
            return sentence
    return r


def _detect_acknowledged_unknown(response, gap_type, iteration):
    """
    Conservative detection of explicit acknowledged unknowns.
    Requires ignorance marker AND minimum response length.
    Returns AcknowledgedUnknown or None.
    NO effect on gap closure or quality classification.
    verbatim holds only the bounded unknown fragment (owner-authorized
    2026-07-10 correction); the full answer stays in the transcript,
    interaction ledger, and evidence records unchanged.
    """
    r = response.strip()
    if len(r) < _MIN_ACKNOWLEDGED_UNKNOWN_LENGTH:
        return None
    r_lower = r.lower()
    for marker in _ACKNOWLEDGED_UNKNOWN_MARKERS:
        if marker in r_lower:
            return AcknowledgedUnknown(
                iteration=iteration,
                gap_context=gap_type,
                verbatim=_extract_unknown_fragment(r, marker),
                category_basis=marker,
            )
    # PVCG-R3-I (D-3): the registered ARABIC unknown surfaces mirror the
    # English markers above one-for-one. An Arabic inventor's explicitly stated
    # unknown is recorded on the SAME parallel track, with a truthful
    # category_basis. This changes no gap status, no quality tier and no return
    # value — unknown is still never satisfied, never REASONED, never
    # DEMONSTRATED. R4 correction/invalidation is NOT activated here.
    surface = detect_registered_unknown(r)
    if surface is not None:
        return AcknowledgedUnknown(
            iteration=iteration,
            gap_context=gap_type,
            verbatim=_extract_unknown_fragment_normalized(r, surface),
            category_basis=surface,
        )
    return None


# ─────────────────────────────────────────────
# 3. Integrate response → update gap status
# ─────────────────────────────────────────────

# Weak-answer patterns that must not advance maturity
_WEAK_PATTERNS = {
    "i don't know", "i do not know", "not sure", "no idea",
    "i don't know", "unknown", "maybe", "n/a", "na",
    "i have no idea", "i'm not sure", "i am not sure",
    "something", "somehow", "i don't", "don't know",
}

# Substance signals: at least one required for REASONED
_GENERIC_CAUSAL_VERBS = {
    "detects","detect","sends","send","uses","use",
    "connects","connect","receives","receive","triggers",
    "trigger","activates","activate","processes","process",
}
_CAUSAL_STRUCTURE_PATTERNS = [
    "when ","if ","after ","before ","until ","once ","as soon as ",
    "causes","produces","results in","leads to",
    "converts","transforms","transfers",
    "measures","calculates","compares","exceeds",
    "locks","releases","pushes","pulls","blocks","rotates",
    "in order to","so that","which means","which causes",
    "by measuring","by detecting","by converting","then ",
    
]
def _has_causal_structure(r_lower):
    # PVCG-R3-I: the English table is evaluated first and is byte-unchanged.
    # The registered Arabic causal-structure surfaces mirror the SAME role for
    # Arabic (R3-C §5.4) and add no new causal construction; without them an
    # Arabic answer can never reach REASONED, which is D-2 — the decisive
    # launch-material finding.
    if any(p in r_lower for p in _CAUSAL_STRUCTURE_PATTERNS):
        return True
    return has_registered_causal_structure(r_lower)
def _is_generic_verb_trap(r_lower):
    if not (set(r_lower.split()) & _GENERIC_CAUSAL_VERBS): return False
    return not _has_causal_structure(r_lower)


# ─── Layer-2 bounded scoring correction (owner-authorized 2026-07-11) ───
# Previously missing explicit causal connectives. DISTINCT gated path —
# deliberately NOT added to _CAUSAL_STRUCTURE_PATTERNS: existing entries keep
# their raw substring semantics unchanged, while this path additionally
# requires an electronics/electrical domain substance signal matched as a
# WHOLE WORD (with an explicit safe plural alias map) in the SAME SENTENCE as the
# connective, on the directional side the connective supports. Case-
# insensitive. Bare "so", "and so", "for", "as", "while", punctuation-only
# inference, quoted-speech parsing, negation parsing, and probabilistic
# classification are intentionally excluded.
#
# TRUE SENTENCE BOUNDING (owner-authorized correction 2026-07-11): sentences
# are bounded deterministically by ".", "?", "!", and line breaks; semicolons,
# commas, and colons stay inside a sentence for this increment. The qualifying
# substance must occur in the same sentence as the qualifying connective —
# substance found only in another sentence never qualifies, and sides from
# different sentences or from different connective occurrences are never
# combined. Each connective occurrence is evaluated independently.
#
# Direction of the supporting side WITHIN the selected sentence:
#   - cause connectives (because / since / due to): the rationale FOLLOWS
#     the connective, so substance is required AFTER it, before the sentence
#     ends;
#   - consequence connectives (therefore / thus / hence / as a result): the
#     supporting cause PRECEDES the connective, so substance is required
#     BEFORE it, after the sentence starts. A result-first connective whose
#     result side (the sentence part after it) is empty is nonsensical and
#     never qualifies.
#
# Narrowly documented conservative disqualifiers (NOT parsers — fixed
# character/token checks only; each can only produce false negatives, never
# false positives; the same lexical technology as the existing weak-pattern
# and acknowledged-unknown marker lists):
#   * QUOTE GUARD — a double-quote character anywhere in the connective's
#     sentence disqualifies that occurrence: quoted material in the sentence
#     cannot be attributed to the owner's own reasoning without quote
#     parsing, which is not authorized.
#   * REPORTED-SPEECH GUARD — a fixed whole-token marker (said / says /
#     told / heard / claims / claimed / reported / according) BEFORE the
#     connective in the same sentence disqualifies that occurrence: the
#     causal claim is attributed to a third party, not stated as the
#     owner's own reasoning.
#   * NEGATION GUARD — the whole token "not" or "never" BEFORE the
#     connective in the same sentence disqualifies that occurrence ("does
#     not fail because ..." is a negated explanation). Contracted negations
#     (e.g. "doesn't") are NOT recognized — a documented conservative
#     limitation, not a negation parser.
#   * TEMPORAL-SINCE GUARD — "since" ONLY additionally requires a non-empty
#     claim side before it in the same sentence: sentence-initial "since"
#     is frequently temporal ("Since Tuesday ...") and this narrow lexical
#     detector cannot distinguish the temporal from the causal reading
#     there, so it conservatively never qualifies. Sentence-initial
#     "because" remains eligible (unambiguously causal).
_NEW_CAUSAL_CONNECTIVES_CAUSE_FIRST = ("because", "since", "due to")
_NEW_CAUSAL_CONNECTIVES_RESULT_FIRST = ("therefore", "thus", "hence", "as a result")

_SUBSTANCE_WORD_RE = re.compile(r"[a-z0-9]+")

# Deterministic sentence boundaries for this narrow detector: terminator
# punctuation runs or line-break runs. NOT a general NLP sentence tokenizer;
# no external dependency.
_GATE_SENTENCE_BOUNDARY_RE = re.compile(r"[.!?]+|[\r\n]+")

# Fixed guard sets — see the narrowly documented disqualifiers above.
_GATE_QUOTE_CHARS = "\"“”«»"
_GATE_REPORTED_SPEECH_TOKENS = frozenset({
    "said", "says", "told", "heard", "claims", "claimed", "reported",
    "according",
})
_GATE_PRE_NEGATION_TOKENS = frozenset({"not", "never"})


def _connective_regex(connective):
    # Whole-word connective match; multi-word connectives tolerate any
    # whitespace run between their words ("due to", "as a result").
    return re.compile(
        r"\b" + r"\s+".join(re.escape(part) for part in connective.split()) + r"\b"
    )


_NEW_CONNECTIVE_RES_CAUSE_FIRST = tuple(
    _connective_regex(c) for c in _NEW_CAUSAL_CONNECTIVES_CAUSE_FIRST)
_NEW_CONNECTIVE_RES_RESULT_FIRST = tuple(
    _connective_regex(c) for c in _NEW_CAUSAL_CONNECTIVES_RESULT_FIRST)


# L2SC-01 (owner-authorized; docs/governance/L2SC01_SUBSTANCE_SIGNAL_PLURAL_
# ALIAS_INCREMENT_CONTRACT.md): plural-alias ownership lives in each domain
# pack's own registry-owned `substance_signal_plural_aliases` field (read via
# `engine.domain_rules.get_substance_signal_plural_aliases(domain)`), NOT in
# this shared engine module. There is exactly ONE live source of plural-alias
# data — the domain pack — for every domain, including electronics (whose
# historical 8-pair map was migrated into `domains/electronics_electrical/
# domain.json` unchanged). Generic suffix stripping (-s / -es / -ies) remains
# NOT ratified: independent probing previously demonstrated false-positive
# folds such as "ices"→"ic", "halls"→"hall", non-electronics "chips", and
# verbal "displays" — plural recognition stays limited to each pack's
# explicit, conservative, Owner-reviewed alias map. These are MATCHING
# ALIASES ONLY: they modify no classifier/activation data, add no
# classification vocabulary, and are never derived dynamically from suffix
# rules.


def _has_whole_word_substance(text_lower, substance_tokens, plural_aliases):
    """
    Whole-word substance-signal detection with an explicit safe plural map.
    Tokenizes on alphanumeric runs, so substring fragments inside larger
    words never match ("ic" in "nice"/"device"/"which", "led" in
    "called"/"enabled", "esp" in "especially", "hall" in "shall").
    A plural form matches ONLY via the caller-supplied `plural_aliases`
    (the CURRENT domain's own registry-owned map — see L2SC-01) and only
    when its singular is an authorized registry signal — no suffix
    stripping, no stemming, no vocabulary addition, no cross-domain
    borrowing. Deterministic; no side effects.
    """
    for w in _SUBSTANCE_WORD_RE.findall(text_lower):
        if w in substance_tokens:
            return True
        singular = plural_aliases.get(w)
        if singular is not None and singular in substance_tokens:
            return True
    return False


def _gate_sentence_spans(r_lower):
    """
    Deterministic (start, end) character spans of the sentences of r_lower,
    bounded by terminator punctuation (. ! ?) and line breaks. Semicolons,
    commas, and colons remain inside a sentence. Empty segments between
    consecutive boundaries are skipped. Pure; no side effects.
    """
    spans = []
    start = 0
    for m in _GATE_SENTENCE_BOUNDARY_RE.finditer(r_lower):
        if m.start() > start:
            spans.append((start, m.start()))
        start = m.end()
    if start < len(r_lower):
        spans.append((start, len(r_lower)))
    return spans


def _gate_directional_segment(r_lower, spans, match, cause_first, connective):
    """
    Return the same-sentence directional segment for one connective
    occurrence, or None when the occurrence cannot qualify:

      * the occurrence does not sit fully inside one sentence (a multi-word
        connective spanning a line break spans a sentence boundary);
      * the quote guard, reported-speech guard, or negation guard fires;
      * "since" opens its sentence (temporal-since guard);
      * a result-first connective has an empty result side.

    cause_first=True selects the sentence part AFTER the connective (the
    rationale); cause_first=False selects the part BEFORE it (the supporting
    cause). Sides from other sentences are never used. Deterministic.
    """
    for start, end in spans:
        if start <= match.start() and match.end() <= end:
            sentence = r_lower[start:end]
            if any(q in sentence for q in _GATE_QUOTE_CHARS):
                return None
            before = r_lower[start:match.start()]
            after = r_lower[match.end():end]
            before_tokens = set(_SUBSTANCE_WORD_RE.findall(before))
            if before_tokens & _GATE_REPORTED_SPEECH_TOKENS:
                return None
            if before_tokens & _GATE_PRE_NEGATION_TOKENS:
                return None
            if connective == "since" and not before_tokens:
                return None            # temporal-since guard
            if not cause_first and not _SUBSTANCE_WORD_RE.search(after):
                return None            # empty result side is nonsensical
            return after if cause_first else before
    return None                        # spans a sentence boundary


def _connective_whole_word_substance_gate(r_lower, substance_tokens, plural_aliases):
    """
    New-connective gate (TRUE SENTENCE-BOUNDED): an authorized new
    connective present as a whole word AND a whole-word (explicit safe
    plural aliases only)
    substance signal in the SAME SENTENCE, on the directional side that
    connective supports. Every occurrence is evaluated independently;
    substance from a different sentence never qualifies, and opposing sides
    of different occurrences are never combined. Returns False whenever the
    substance check is disabled (empty/unknown domain or empty signal list)
    — this path never fires without domain substance authority, so
    domain="" and unknown-domain behavior is unchanged. `plural_aliases` is
    the CURRENT domain's own registry-owned plural-alias map (L2SC-01) —
    never a different domain's, never merged across domains. Deterministic;
    no side effects.
    """
    if not substance_tokens:
        return False
    spans = _gate_sentence_spans(r_lower)
    for connectives, regexes, cause_first in (
        (_NEW_CAUSAL_CONNECTIVES_CAUSE_FIRST, _NEW_CONNECTIVE_RES_CAUSE_FIRST, True),
        (_NEW_CAUSAL_CONNECTIVES_RESULT_FIRST, _NEW_CONNECTIVE_RES_RESULT_FIRST, False),
    ):
        for connective, conn_re in zip(connectives, regexes):
            for m in conn_re.finditer(r_lower):
                segment = _gate_directional_segment(
                    r_lower, spans, m, cause_first, connective)
                if segment is not None and _has_whole_word_substance(
                        segment, substance_tokens, plural_aliases):
                    return True
    return False



# ─── Layer-3 bounded structured-substance gate (Wave-1 RVR-3, OD-R2) ───
# The frozen S2 run proved a perspective inversion: practitioner-form answers
# carrying MORE engineering substance assessed BELOW everyday prose, solely
# because they lack the preferred conversational causal substrings. This gate
# recognizes committed STRUCTURAL-TECHNICAL form - enumeration markers,
# labeled technical clauses, hyphenated technical compounds - as a distinct
# deterministic REASONED path. Pure text predicate: no model inference, no
# semantic interpretation, no probabilistic scoring. It never bypasses the
# weak-pattern / weak-token rejections above it, and the generic-verb trap
# yields to it exactly as the trap already yields to the Layer-2 connective
# gate. Unicode-letter classes, so the same structural forms count in Arabic.
import re as _re
_ENUM_MARKER_RE = _re.compile(r"\(\d{1,2}\)|(?:^|[\s:;])\d{1,2}\.\s")
_LABEL_CLAUSE_RE = _re.compile(
    r"(?:^|[.!?;]\s+)[^\W\d_][\w /\-]{2,40}:\s", _re.UNICODE)
_HYPHEN_COMPOUND_RE = _re.compile(
    r"\b[^\W\d_]{3,}-[^\W\d_]{3,}\b", _re.UNICODE)
_MIN_STRUCTURED_WORDS = 12
_LONG_TOKEN_RE = _re.compile(r"[^\W\d_]{6,}", _re.UNICODE)
_ARABIC_CHAR_RE = _re.compile(r"[\u0600-\u06ff]")
_MIN_DISTINCT_LONG_TOKENS = 2

def _distinct_long_tokens(r_lower):
    """Distinct 'long' content tokens: >= 8 letters, or >= 6 letters for
    Arabic-script tokens (Arabic morphology packs the same content into
    shorter surface forms - measured on the frozen corpus)."""
    out = set()
    for tok in _LONG_TOKEN_RE.findall(r_lower):
        if len(tok) >= 8 or _ARABIC_CHAR_RE.search(tok):
            out.add(tok)
    return out

def _structured_technical_form(r_lower):
    """Deterministic structural-technical form test (thresholds fixed):
    (at least two enumeration markers, OR at least two distinct hyphenated
    compounds, OR one labeled clause plus one enumeration/hyphen marker),
    AND at least two distinct long tokens (>= 8 unicode letters) - the
    measured discriminator that separates technical enumeration from
    enumerated small-talk ("(1) cool (2) nice"), in English and Arabic
    alike. Pure text predicate; no model inference."""
    enum = len(_ENUM_MARKER_RE.findall(r_lower))
    hyph = len(set(_HYPHEN_COMPOUND_RE.findall(r_lower)))
    label = len(_LABEL_CLAUSE_RE.findall(r_lower))
    # semicolon-separated technical clause chains count in both scripts
    # (";" and the Arabic "؛").
    semis = r_lower.count(";") + r_lower.count("؛")
    structured = ((enum >= 2) or (hyph >= 2)
                  or (label >= 1 and (enum + hyph) >= 1)
                  or (label >= 1 and semis >= 2))
    if not structured:
        return False
    return len(_distinct_long_tokens(r_lower)) >= _MIN_DISTINCT_LONG_TOKENS


MIN_REASONED_RESPONSE_LENGTH = 40  # anti-triviality guard only — see ADR-003 Step 6 note

def assess_response(response: str, domain: str = "") -> str:
    """
    Quality assessment: weak-answer guard + substance check.
    Rules 1-2: weak pattern rejection. Rule 2.5: generic verb trap.
    Rule 3: substance + causal structure + length. See ADR-004.
    """
    r = response.strip()
    r_lower = r.lower()

    # 1. Reject explicit weak answers regardless of length
    if r_lower in _WEAK_PATTERNS:
        return ASSERTED  # stays ASSERTED — will not pass evaluate_transition

    # 2. Reject vague filler phrases (contains weak tokens, no substance)
    weak_tokens = {"somehow", "something", "technology", "stuff", "things"}
    # Substance Signal Authority: read from registry per domain (AB-005 Step 7)
    substance_tokens = set(
        get_substance_signals(domain)
    )
    # L2SC-01: the CURRENT domain's own registry-owned plural-alias map —
    # never a different domain's, never merged, never derived automatically.
    plural_aliases = get_substance_signal_plural_aliases(domain)
    # AB-006-D: fail-explicit observability for empty/unknown domain
    if not domain:
        warnings.warn(
            "assess_response called with empty domain — "
            "substance check disabled (AB-006-D)",
            stacklevel=2
        )
    elif not is_known_domain(domain):
        warnings.warn(
            "assess_response: domain=" + repr(domain) + " not found in registry — "
            "substance check disabled (AB-006-D)",
            stacklevel=2
        )
    elif not substance_tokens:
        warnings.warn(
            "assess_response: domain=" + repr(domain) + " has no substance signals in registry — "
            "substance check disabled (AB-006-D)",
            stacklevel=2
        )
    words = set(r_lower.split())
    has_weak = bool(words & weak_tokens)
    # PVCG-R3-I: the pack's own signals are consulted first and unchanged; the
    # registered Arabic surfaces are one-to-one with those ALREADY-COMMITTED
    # signals (R3-C §5.4). No pack is edited, no signal is added, and no domain
    # capability changes — the surfaces live in the unpinned R3 registry.
    has_substance = (any(sig in r_lower for sig in substance_tokens)
                     or substance_surface_present(r_lower, domain))

    if has_weak and not has_substance:
        return ASSERTED  # vague filler — no technical substance

    # 3. Substance token present AND response meets minimum length (anti-triviality guard)
    #    NOTE: length threshold does NOT validate reasoning quality — see ADR-003 Step 6 note
    # Layer-2 gated path input (owner-authorized 2026-07-11): evaluated here
    # only so the generic-verb trap recognizes the new connective+substance
    # form as causal structure — exactly as the trap already yields to the
    # existing _CAUSAL_STRUCTURE_PATTERNS. The trap is unchanged for every
    # input that does not qualify for the new gate. REASONED is still granted
    # only at path C below, after the existing causal path.
    new_connective_gate = _connective_whole_word_substance_gate(
        r_lower, substance_tokens, plural_aliases)
    # Wave-1 RVR-3: the structured-technical gate (Layer-3) - evaluated here
    # only so the generic-verb trap yields to it the same way it yields to the
    # Layer-2 connective gate. REASONED via this gate is granted only at path D
    # below, after the existing paths, and only past the length/word floors.
    structured_gate = (_structured_technical_form(r_lower)
                       and len(r_lower.split()) >= _MIN_STRUCTURED_WORDS)
    if _is_generic_verb_trap(r_lower) and not new_connective_gate \
            and not structured_gate:
        return ASSERTED
    has_causal = _has_causal_structure(r_lower)
    # REASONED path A: substance domain token + causal structure + length
    # REASONED path B: causal structure + no trap + length (for non-electronics domains)
    if has_causal and not _is_generic_verb_trap(r_lower) and len(r) >= MIN_REASONED_RESPONSE_LENGTH:
        return REASONED
    # REASONED path C (Layer-2, owner-authorized): authorized new causal
    # connective + whole-word (explicit-plural-alias) substance signal in the
    # supporting clause + existing minimum length. Distinct gated path —
    # never bypasses the weak-pattern / weak-token rejections above.
    if new_connective_gate and len(r) >= MIN_REASONED_RESPONSE_LENGTH:
        return REASONED
    # REASONED path D (Layer-3, Wave-1 RVR-3): committed structural-technical
    # form + the existing minimum length. Distinct gated path - never bypasses
    # the weak-pattern / weak-token rejections above.
    if structured_gate and len(r) >= MIN_REASONED_RESPONSE_LENGTH:
        return REASONED

    # 4. Length fallback for borderline answers without clear substance signals
    if len(r) < 20:
        return ASSERTED
    # No substance signals detected — treat as ASSERTED regardless of length
    return ASSERTED  # DEMONSTRATED requires external evidence — not in MVP


def integrate_response(
    state: IdeaState,
    gap_type: str,
    question: str,
    response: str,
) -> tuple[str, str]:
    """
    Update IdeaState based on response.
    Returns (transition_result, reason).
    transition_result: PASS | WARN | BLOCK
    """
    quality = assess_response(response, state.domain)
    # PVCG-R2-I (authoritative contract PVCG_R2_C_GAP_RELEVANCE_HARDENING_
    # CONTRACT.md §4/§6): satisfaction eligibility for the SERVED gap. A
    # response that does not address the gap that was actually asked about may
    # not influence that gap's satisfaction, no matter how much generic
    # technical substance, domain vocabulary or causal language it carries.
    # Deterministic, fail-closed, lexical (see engine/gap_relevance.py for the
    # stated bound); it is eligibility only and never a quality judgement, a
    # BLOCK, a contradiction, or an input-validation failure.
    relevant = addresses_gap(response, gap_type)
    evidence = Evidence(
        content=response,
        quality=quality,
        iteration=state.iteration,
        # Wave-1 RVR-3 / MG-5: an owner answer's evidence is OWNER_STATED -
        # the durable ledger already records exactly this provenance for the
        # same answers; the rendered registry now matches it.
        provenance=OWNER_STATED,
    )

    # Update known elements
    if relevant and gap_type == MECHANISM_COMPLETENESS:
        if state.known_mechanism is None or quality >= state.known_mechanism.quality:
            state.known_mechanism = evidence

    # أي evidence في المراحل المبكرة تُثبت المشكلة ضمنياً
    if relevant and state.known_problem is None and quality >= REASONED:  # RISK-002
        state.known_problem = evidence

    # Update gap status
    gap = state.get_gap(gap_type)
    if gap is None:
        gap = Gap(gap_type=gap_type, status=OPEN, opened_at=state.iteration)
        state.gaps.append(gap)

    # Parallel track: record acknowledged unknown if present.
    # Unconditional -- runs for DEMONSTRATED, REASONED, and ASSERTED.
    # Does NOT affect gap.status, quality, or any return value.
    _unknown = _detect_acknowledged_unknown(response, gap_type, state.iteration)
    if _unknown is not None:
        state.acknowledged_unknowns.append(_unknown)

    # Capture accepted (substantiated) evidence for Stage 3 reasoning gaps only.
    # Restricted to PROBLEM_MECHANISM_FIT / ASSUMPTION_INVENTORY /
    # EXPERTISE_GAP_AWARENESS — Stage 2 gaps do not use this capture path.
    # "Accepted" = REASONED or better (the quality tier that advances a gap);
    # ASSERTED and empty/whitespace responses are NOT recorded. Append-only:
    # no effect on gap.status, quality, transition, or return value.
    if (relevant
            and gap_type in STAGE_3_GAP_TYPES
            and response.strip()
            and quality in (REASONED, DEMONSTRATED)):
        gap.evidence.append(evidence)

    # PVCG-R2-I fail-closed exit. The answer is recorded and its assessed
    # quality is unchanged; it is simply not eligible to satisfy or close THIS
    # gap, so the gap status is left exactly as it was. Deliberately placed
    # after gap creation and after the unconditional acknowledged-unknown
    # track, both of which R2 does not govern.
    if not relevant:
        return "WARN", (f"{gap_type} not addressed — this answer does not "
                        f"respond to the question that was asked")

    # PVCG-R4-C §10.4 G-1/G-2/G-4 — CLOSED-gap safety guard.
    #
    # Before R4 this function had no CLOSED branch, so a REASONED answer against
    # an already-CLOSED gap fell through to the `else` below and overwrote CLOSED
    # with PARTIAL **while leaving closed_at set** — an impossible mixed state.
    # It was never reachable at runtime, because `select_next_gap` returns only
    # OPEN/PARTIAL gaps and this function's single runtime caller
    # (`run_iteration`) takes its gap_type from there. The runtime was protected
    # by the CALLER's filter, not by this function.
    #
    # R4 exposes an explicit correction path, so the hazard is now closed HERE,
    # by construction rather than by caller discipline (G-1): an already-CLOSED
    # gap is never weakened in place and `closed_at` can never be orphaned (G-4).
    #
    # This is NOT a reopen path (G-2): the ordinary forward journey is unchanged,
    # OPEN->PARTIAL->CLOSED still only moves forward, and WPS-001 INV-004 is
    # preserved exactly. A correction reaches a WEAKER outcome only through full
    # deterministic replay onto a FRESH IdeaState (G-3) — a property of the new
    # run, never a backward transition in the old one.
    if gap.status == CLOSED:
        return "PASS", f"{gap_type} already closed — no change"

    if quality == DEMONSTRATED:
        gap.status = CLOSED
        gap.closed_at = state.iteration
        return "PASS", f"{gap_type} closed with DEMONSTRATED evidence"

    elif quality == REASONED:
        if gap.status == PARTIAL:
            gap.status = CLOSED
            gap.closed_at = state.iteration
            return "PASS", f"{gap_type} closed after REASONED follow-up"
        else:
            gap.status = PARTIAL
            return "WARN", f"{gap_type} partially addressed — needs more depth"

    else:  # ASSERTED
        gap.status = PARTIAL
        return "WARN", f"{gap_type} asserted only — reasoning required"


def accept_gap_risk(state: IdeaState, gap_type: str) -> None:
    """RVR-1 (Wave-1 remediation contract, OD-R1) — the ONLY writer of
    ``Gap.status = ACCEPTED_RISK``.

    Explicit-owner-action lifecycle transition: the named gap moves from
    OPEN/PARTIAL to ACCEPTED_RISK. Never automatic — the sole live caller is
    the governed /session/<sid>/accept-risk route after an explicit user
    confirmation, and the sole replay caller applies the durably recorded
    ``risk_accepted`` disposition (deterministic replay).

    Refused loudly (ValueError, nothing mutated) when:
      * the gap does not exist on this state;
      * the gap is not OPEN/PARTIAL (CLOSED and ACCEPTED_RISK never move);
      * the gap is MECHANISM_COMPLETENESS — the core mechanism can never be
        risk-accepted: an idea whose mechanism is unknown is truthfully
        BLOCKED, not riskily acceptable.

    ACCEPTED_RISK is acceptance, not resolution: nothing here touches
    evidence, quality, maturity, known_mechanism/known_problem, or closed_at.
    """
    if gap_type == MECHANISM_COMPLETENESS:
        raise ValueError(
            "MECHANISM_COMPLETENESS cannot be risk-accepted - the core "
            "mechanism must be established, not accepted as unknown")
    gap = state.get_gap(gap_type)
    if gap is None:
        raise ValueError(f"no such gap on this state: {gap_type!r}")
    if gap.status not in (OPEN, PARTIAL):
        raise ValueError(
            f"{gap_type} is {gap.status} - only an OPEN/PARTIAL gap can be "
            "accepted as a known risk")
    gap.status = ACCEPTED_RISK


def advance_after_disposition(state: IdeaState):
    """RVR-1 (Wave-1) — canonical progression continuation after an explicit
    gap disposition (accept_gap_risk).

    Opens the next priority gap through the existing cascade; when no gap
    remains to open or serve, the canonical iteration step runs with EMPTY
    input (nothing is assessed, no evidence is created) so the SAME
    evaluate_transition/stage logic every answered iteration uses decides
    whether maturity advances and the next stage's gaps open. Deterministic;
    used identically by the live accept-risk route and the reconstruction
    replay, so live and replayed states stay byte-equivalent.
    """
    opened = _open_next_gap_if_needed(state)
    if opened is None and select_next_gap(state) is None:
        return run_iteration(state, "")
    return None


# ─────────────────────────────────────────────
# 4. Evaluate maturity transition
# ─────────────────────────────────────────────

def evaluate_transition(state: IdeaState) -> tuple[bool, str]:
    """
    Check if state qualifies for maturity_level increment.
    Returns (can_transition, reason).
    Deterministic — no AI involvement.
    """
    level = state.maturity_level

    if level == 0:
        # 0 → 1: problem established with beneficiary signal
        if state.known_problem and state.known_problem.quality >= REASONED:
            mech_gap = state.get_gap(MECHANISM_COMPLETENESS)
            if mech_gap and mech_gap.status == OPEN and mech_gap.iterations_open == 0:
                return False, "MECHANISM_COMPLETENESS must be attempted first"
            return True, "Problem established — ready for LEVEL 1"
        return False, "Problem not yet established"

    if level == 1:
        # 1 → 2: mechanism established + no blocking gaps
        if state.known_mechanism is None:
            return False, "Mechanism not established"
        if state.known_mechanism.quality == ASSERTED:
            return False, "Mechanism quality must be REASONED minimum"
        mech_gap = state.get_gap(MECHANISM_COMPLETENESS)
        if mech_gap and mech_gap.status != CLOSED:
            return False, "BLOCK: MECHANISM_COMPLETENESS not yet closed"
        # GD-001 / ILT-F-001: all Stage Two gaps must exist and be CLOSED
        REQUIRED_STAGE_TWO_GAPS = [
            MECHANISM_COMPLETENESS,
            PHYSICAL_FEASIBILITY,
            BOUNDARY_AMBIGUITY,
        ]
        for required_gap in REQUIRED_STAGE_TWO_GAPS:
            gap = state.get_gap(required_gap)
            if gap is None:
                return False, f"BLOCK: {required_gap} not yet opened"
            # RVR-1 (OD-R1): PHYSICAL_FEASIBILITY and BOUNDARY_AMBIGUITY are
            # satisfied by CLOSED **or** by the explicit owner disposition
            # ACCEPTED_RISK — acceptance counts toward completion while staying
            # visibly unresolved everywhere it renders. MECHANISM_COMPLETENESS
            # is exempt by construction: accept_gap_risk refuses it, and the
            # dedicated mech_gap CLOSED check above still governs it.
            if required_gap != MECHANISM_COMPLETENESS \
                    and gap.status == ACCEPTED_RISK:
                continue
            if gap.status != CLOSED:
                return False, f"BLOCK: {required_gap} not yet closed (status: {gap.status})"
        return True, "Mechanism established — ready for LEVEL 2"

    return False, f"LEVEL {level} is max for MVP"


# ─────────────────────────────────────────────
# 5. Detect stall
# ─────────────────────────────────────────────

def update_direction(state: IdeaState, prev_level: int) -> None:
    if state.maturity_level > prev_level:
        state.direction = PROGRESSING
    else:
        open_count = len(state.get_open_gaps())
        stalled_gaps = [
            g for g in state.gaps
            if g.status in (OPEN, PARTIAL) and g.iterations_open >= STALL_THRESHOLD
        ]
        if stalled_gaps:
            state.direction = STALLED
        else:
            state.direction = PROGRESSING


# ─────────────────────────────────────────────
# 6. Main loop step
# ─────────────────────────────────────────────

def run_iteration(state: IdeaState, response: str) -> dict:
    """
    Execute one full iteration of the progression loop.
    Returns result dict with question, transition, direction.
    """
    state.iteration += 1
    prev_level = state.maturity_level

    # Update gap iteration counters
    for g in state.gaps:
        if g.status in (OPEN, PARTIAL):
            g.iterations_open += 1

    # Select gap
    gap_type = select_next_gap(state)

    # Level-0 problem establishment path
    # Handles initial response when no gaps exist yet (maturity=0)
    if gap_type is None and state.maturity_level == 0 and response:
        quality = assess_response(response, state.domain)
        evidence = Evidence(
            content=response,
            quality=quality,
            iteration=state.iteration,
            provenance=OWNER_STATED,   # Wave-1 RVR-3 / MG-5
        )
        if quality >= REASONED and (state.known_problem is None or quality > state.known_problem.quality):  # RISK-002
            state.known_problem = evidence
            if state.idea_summary is None:  # R-007: capture once
                state.idea_summary = _trim_idea_summary(response)

    if gap_type is None:
        can, reason = evaluate_transition(state)
        if can and state.maturity_level < 2:
            state.maturity_level += 1
            if state.maturity_level == 2:
                state.current_stage = 3
        # Level-1 gap initialization: open MECHANISM_COMPLETENESS if maturity just reached 1
        if state.maturity_level == 1 and len(state.gaps) == 0 and state.get_gap(MECHANISM_COMPLETENESS) is None:
            from engine.idea_state import Gap
            gap = Gap(gap_type=MECHANISM_COMPLETENESS, status=OPEN, opened_at=state.iteration)
            state.gaps.append(gap)
        # GAP_PRIORITY cascade: open next gap when no OPEN/PARTIAL gap exists
        next_gap_opened = None
        if len([g for g in state.gaps if g.status in (OPEN, PARTIAL)]) == 0:
            # Select gap priority based on current stage
            active_priority = (
                STAGE3_GAP_PRIORITY
                if getattr(state, "current_stage", 2) == 3
                else GAP_PRIORITY
            )
            for next_gap_type in active_priority:
                if state.get_gap(next_gap_type) is None:
                    from engine.idea_state import Gap
                    gap = Gap(gap_type=next_gap_type, status=OPEN, opened_at=state.iteration)
                    state.gaps.append(gap)
                    next_gap_opened = next_gap_type
                    break
        update_direction(state, prev_level)
        # إذا وصلنا LEVEL 2 — نطلب تعمق في boundary
        # If cascade opened a new gap, generate its question and return
        if next_gap_opened:
            new_gap = state.get_gap(next_gap_opened)
            iterations_open = new_gap.iterations_open if new_gap else 0
            from engine.ai_advisor import get_ai_question
            _ai_ctx = {
                "domain": state.domain,
                "gap_type": next_gap_opened,
                "idea_summary": getattr(state, "idea_summary", None),
                "last_response": None,
                "iteration": state.iteration,
            }
            _ai_q = None if state.path == "N" \
                else get_ai_question(state.domain, next_gap_opened, _ai_ctx)
            next_q = _ai_q \
                or get_question(state.domain, next_gap_opened, iterations_open,
                                path=state.path)
            result = {
                "iteration"     : state.iteration,
                "gap_targeted"  : next_gap_opened,
                "question"      : next_q,
                "transition"    : "PASS" if can else "WARN",
                "reason"        : reason,
                "maturity_level": state.maturity_level,
                "direction"     : state.direction,
            }
        else:
            closing_q = None
            if state.maturity_level == 2:
                closing_q = "Your mechanism is taking shape. Now state clearly: what does your invention NOT do or NOT cover? Name at least one boundary."
            result = {
                "iteration": state.iteration,
                "gap_targeted": None,
                "question": closing_q,
                "transition": "PASS" if can else "WARN",
                "reason": reason,
                "maturity_level": state.maturity_level,
                "direction": state.direction,
            }

    else:
        # Get question — AI advisory (G-A) or fallback to domain/generic
        gap = state.get_gap(gap_type)
        iterations_open = gap.iterations_open if gap else 0
        from engine.ai_advisor import get_ai_question
        _ai_context = {
            "domain": state.domain,
            "gap_type": gap_type,
            "idea_summary": getattr(state, 'idea_summary', None),
            "last_response": response[:200] if response else None,
            "iteration": state.iteration,
        }
        _ai_q = None if state.path == "N" \
            else get_ai_question(state.domain, gap_type, _ai_context)
        question = _ai_q \
            or get_question(state.domain, gap_type, iterations_open,
                            path=state.path)

        # Integrate response
        transition, reason = integrate_response(state, gap_type, question, response)

        # Check transition
        can, t_reason = evaluate_transition(state)
        if can and state.maturity_level < 2:
            state.maturity_level += 1
            if state.maturity_level == 2:
                state.current_stage = 3
            transition = "PASS"
            reason = t_reason

        update_direction(state, prev_level)

        # GAP_PRIORITY cascade — open next gap if none remain
        next_gap_opened = _open_next_gap_if_needed(state)
        next_q = None
        if next_gap_opened:
            new_gap = state.get_gap(next_gap_opened)
            iterations_open = new_gap.iterations_open if new_gap else 0
            from engine.ai_advisor import get_ai_question
            ai_ctx = {
                "domain": state.domain,
                "gap_type": next_gap_opened,
                "idea_summary": getattr(state, "idea_summary", None),
                "last_response": None,
                "iteration": state.iteration,
            }
            _ai_q = (
                None if state.path == "N"
                else get_ai_question(state.domain, next_gap_opened, ai_ctx)
            )
            next_q = (
                _ai_q
                or get_question(state.domain, next_gap_opened, iterations_open,
                                path=state.path)
            )
        result = {
            "iteration": state.iteration,
            "gap_targeted": next_gap_opened,
            "question": next_q,
            "transition": transition,
            "reason": reason,
            "maturity_level": state.maturity_level,
            "direction": state.direction,
        }

    # Log — single exit guaranteed by structure
    log = IterationLog(
        iteration=state.iteration,
        gap_targeted=result.get('gap_targeted'),
        question_asked=result.get('question'),
        response_summary=response[:100],
        gaps_changed=[result.get('gap_targeted')],
        maturity_before=prev_level,
        maturity_after=state.maturity_level,
    )
    state.iteration_log.append(log)
    return result
