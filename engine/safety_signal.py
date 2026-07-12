"""Inventor-Stated Safety Signals — pure, read-only additive advisory derivation.

Governance (merged, binding):
`docs/governance/SAFETY_AWARE_INVENTOR_STATED_SAFETY_SIGNALS_INCREMENT_CONTRACT.md`
(true-merged via PR #120) and the PR #118 scope decision. This is the FIRST
additive Safety-Aware increment: it elevates safety-relevant assumptions,
failure conditions, and consequences that the inventor has ALREADY stated in the
recorded ``IdeaState``, into a clearly-labelled advisory signal. It is additive
and advisory only.

Strict boundaries (contract §3–§7):
- Pure, deterministic, read-only; NEVER mutates the input ``IdeaState`` or any
  record; no engine call, no scoring, no persistence, no network, no hidden state.
- Derives ONLY from inventor-stated / clearly inventor-grounded content already
  recorded (assertion-ledger content, acknowledged unknowns, the established
  problem/mechanism evidence text, and the idea summary).
- Does NOT change scoring, maturity, readiness, gap closure, evidence
  classification, thresholds, the generic-verb trap, causal tokens,
  ``derive_requirement_landscape``, the Increment-4 ``criticality`` field,
  ``RequirementLandscape.risks``, or the Section 6 risk generator.
- Conservative detection: a bare keyword (e.g. "safety") is NEVER sufficient. A
  signal requires the co-occurrence, in ONE inventor-stated text, of an explicit
  failure / invalid-use condition, a safety-relevant subject, a consequence cue,
  AND electronics/electrical context — with negation suppression.
- Never claims the invention is safe or unsafe, and never implies certification,
  compliance, approval, legal, patent, or engineering validation. Every signal is
  labelled inventor-stated and requiring independent validation.

Workstream 2 stabilization (owner-gated; governed by
`docs/governance/SAFETY_SIGNAL_STABILIZATION_INCREMENT_CONTRACT.md`, APPROVED
AND CANONICAL, blob 3db597c77d14aa8f39f7a624c7c32d4984e4f3a3): the detection
internals are sentence-bounded (PR #166 boundary definition), use explicit
finite cue-variant families (token-anchored; no stemming, no suffix folding),
apply sentence-scoped negation plus attribution / deferred-determination
guards, permit only same-source condition→consequence pairing across
IMMEDIATELY adjacent sentences, and deduplicate exact duplicate statements
(whitespace collapse + Unicode NFC only) before signal construction with
deterministic source precedence. The public API, SafetySignal fields, output
shape, provenance/validation constants, and excerpt behavior are unchanged.
"""
import re
import unicodedata
from dataclasses import dataclass
from typing import Optional, Tuple

# --- Frozen advisory vocabulary (contract §5 / §7) --------------------------------
PROVENANCE_INVENTOR_STATED = "inventor_stated"
VALIDATION_REQUIRES_INDEPENDENT = "requires_independent_validation"
_DISPLAY_LABEL = "Potential safety-critical assumption (inventor-stated)"
_CAUTION_TEXT = (
    "Inventor-stated safety signal — requires independent validation. This is "
    "not a determination that the idea is safe or unsafe, and it is not "
    "certification, compliance, or engineering approval."
)
_MVP_DOMAIN = "electronics_electrical"

# --- Conservative detection cue sets (contract §6) --------------------------------
# A signal fires ONLY when a text matches at least one cue from EACH of the three
# categories below AND has electronics/electrical context AND is not negated.
_FAILURE_CUES = (
    "should not be used", "must not be used", "do not use", "cannot be safely",
    "can not be safely", "cannot be achieved", "cannot achieve", "not be safely",
    "if it fails", "if this fails", "fails to", "wrong result", "wrong results",
    "inaccurate", "malfunction", "does not work",
    # Workstream 2 explicit variant family (contract §3.2.b): finite,
    # token-anchored additions only — no stemming, no suffix folding.
    "fail to", "failed to", "failure to",
    "identifies the wrong", "trips the wrong", "sensing is wrong",
    "wrong load", "wrong branch",
    "sticks", "stuck",
    "leaving the appliance powered", "left powered",
)
_SUBJECT_CUES = (
    "insulation", "electric shock", "electrical shock", "shock", "overcurrent",
    "over-current", "over current", "overvoltage", "over-voltage",
    "short circuit", "short-circuit", "fire", "overheat", "overheating",
    "excessive heat", "high voltage", "mains", "live wire", "electrocut",
    "spark", "thermal runaway", "burn", "hazard", "warn", "warning", "alert",
    "detect",
    # Workstream 2 explicit variant family: token-anchored matching means the
    # historical stem "electrocut" no longer reaches its inflections, so they
    # are enumerated explicitly; "danger"/"dangerous" are safety-relevant
    # subject qualifiers evidenced by the WS1 false-negative baseline.
    "electrocute", "electrocuted", "electrocutes", "electrocuting", "electrocution",
    "danger", "dangerous",
)
_CONSEQUENCE_CUES = (
    "safety risk", "unsafe", "create a risk", "creates a risk", "could create a",
    "danger", "hazardous", "harm", "injury", "injure", "electrocut",
    "catch fire", "cause a fire", "shock the user", "miss a real risk",
    "missed warning", "too late", "late warning", "damage",
    # Workstream 2 explicit variant family (finite; token-anchored).
    "electrocute", "electrocuted", "electrocutes", "electrocuting", "electrocution",
    "could remain powered", "remain powered", "stay powered",
    "could remain energized", "remain energized", "stay energized",
    "could be disconnected", "could allow overheating", "could continue",
)
# Electronics/electrical context: satisfied by the session domain OR by an
# electrical-domain term appearing in the inventor's own text.
_ELECTRICAL_TERMS = (
    "insulation", "voltage", "current", "plug", "circuit", "wire", "battery",
    "mains", "electric", "electrical", "electronic", "overcurrent",
    "overvoltage", "relay", "sensor", "microcontroller", "capacitor",
    "resistor", "power", "fuse", "breaker",
)
# Negation guards: if present, the SENTENCE is NOT treated as a safety signal
# (Workstream 2: applied sentence-scoped, and to either sentence of a pair).
_NEGATION_CUES = (
    "no safety concern", "no safety concerns", "not a safety", "safety is not",
    "no safety risk", "without safety risk", "poses no risk", "no risk of",
    "not create a risk", "without any risk", "no risk to",
)
# Attribution / deferred-determination guards (Workstream 2, contract §3.2.c):
# the inventor is describing what is NOT claimed, what someone else will
# determine, or what there is no evidence for — never a stated safety signal.
_ATTRIBUTION_CUES = (
    "no claim is made that",
    "a specialist will determine whether",
    "there is no evidence that",
)

_MAX_EXCERPT = 400  # bounded verbatim excerpt length for display

# --- Workstream 2 sentence-bounded matching machinery -----------------------------
# Sentence boundaries use the committed PR #166 definition: sentences end at
# '.', '?', '!' runs and at line breaks (so adjacent list items inside ONE
# recorded statement are adjacent sentences).
_SENTENCE_BOUNDARY_RE = re.compile(r"[.!?]+|[\r\n]+")

# Token-anchored cue matching: a cue matches only at word boundaries (no
# stemming, no suffix folding — the PR #166 explicit-alias precedent). The
# per-cue patterns are literal-escaped, so no unbounded or backtracking-prone
# regex constructions exist (contract §3.6).
_CUE_PATTERNS = {}


def _cue_in(sentence, cue):
    pattern = _CUE_PATTERNS.get(cue)
    if pattern is None:
        pattern = re.compile(r"(?<![a-z0-9])" + re.escape(cue) + r"(?![a-z0-9])")
        _CUE_PATTERNS[cue] = pattern
    return pattern.search(sentence) is not None


def _first_cue_in_sentence(sentence, cues):
    for cue in cues:
        if _cue_in(sentence, cue):
            return cue
    return None


def _sentences(lowered_text):
    return [s for s in _SENTENCE_BOUNDARY_RE.split(lowered_text) if s and s.strip()]


def _vetoed(sentence):
    return (_first_cue_in_sentence(sentence, _NEGATION_CUES) is not None
            or _first_cue_in_sentence(sentence, _ATTRIBUTION_CUES) is not None)


def _dedup_key(text):
    """Exact-duplicate detection key (contract §4.4): whitespace collapse
    (identical to the documented excerpt handling) plus Unicode NFC — and
    NOTHING else (no case folding, punctuation removal, stemming, or any
    semantic/paraphrase/probabilistic similarity)."""
    return unicodedata.normalize("NFC", " ".join(text.split()))


@dataclass(frozen=True)
class SafetySignal:
    """One inventor-stated safety signal (advisory-only). All fields are display
    context derived from already-recorded content; nothing is persisted."""
    signal_id: str
    source: str
    provenance: str
    safety_subject: str
    failure_condition: str
    possible_consequence: str
    domain_context: str
    validation_status: str
    display_label: str
    caution_text: str
    statement: str


def _domain_of(state):
    domain = getattr(state, "domain", None) or getattr(state, "domain_signal", None)
    return domain


def _has_electrical_context(lowered, domain):
    if domain == _MVP_DOMAIN:
        return True
    return any(_cue_in(lowered, term) for term in _ELECTRICAL_TERMS)


def _same_sentence_hit(sentence, domain):
    """Conservative same-sentence conjunction: failure + subject + consequence
    all within ONE sentence, sentence not vetoed, electrical context satisfied
    by the session domain or by an electrical term in the sentence."""
    if _vetoed(sentence):
        return None
    failure = _first_cue_in_sentence(sentence, _FAILURE_CUES)
    subject = _first_cue_in_sentence(sentence, _SUBJECT_CUES)
    consequence = _first_cue_in_sentence(sentence, _CONSEQUENCE_CUES)
    if failure is None or subject is None or consequence is None:
        return None
    if not _has_electrical_context(sentence, domain):
        return None
    return subject, failure, consequence


def _pair_hit(first, second, domain):
    """Bounded adjacent-sentence pairing (contract §5): condition→consequence
    ONLY, immediately adjacent sentences of the SAME source text — sentence N
    carries the failure/invalid-use cue, sentence N+1 the consequence cue, the
    safety-relevant subject in either; a guard hit in EITHER sentence vetoes
    the pair; electrical context is satisfied over the pair. Two unrelated
    hazard mentions never pair (failure and consequence are both required)."""
    if _vetoed(first) or _vetoed(second):
        return None
    failure = _first_cue_in_sentence(first, _FAILURE_CUES)
    if failure is None:
        return None
    consequence = _first_cue_in_sentence(second, _CONSEQUENCE_CUES)
    if consequence is None:
        return None
    subject = (_first_cue_in_sentence(first, _SUBJECT_CUES)
               or _first_cue_in_sentence(second, _SUBJECT_CUES))
    if subject is None:
        return None
    if not _has_electrical_context(first + " " + second, domain):
        return None
    return subject, failure, consequence


def _detect(text, domain):
    """Return (subject, failure, consequence, domain_context) if ``text`` is a
    conservative inventor-stated safety signal, else None. Read-only, pure,
    deterministic: sentences are evaluated in order; the first qualifying
    sentence, or the first qualifying immediately-adjacent
    condition→consequence pair, wins. Pairing never crosses source texts —
    this function only ever sees ONE source record's text."""
    if not text or not isinstance(text, str):
        return None
    lowered = text.lower()
    sentences = _sentences(lowered)
    domain_context = domain if domain == _MVP_DOMAIN else _MVP_DOMAIN
    for i, sentence in enumerate(sentences):
        hit = _same_sentence_hit(sentence, domain)
        if hit is not None:
            return hit[0], hit[1], hit[2], domain_context
        if i + 1 < len(sentences):
            hit = _pair_hit(sentence, sentences[i + 1], domain)
            if hit is not None:
                return hit[0], hit[1], hit[2], domain_context
    return None


def _inventor_texts(state):
    """Ordered (source_label, text) pairs of inventor-stated / inventor-grounded
    content already recorded on ``state``. Read-only; never mutates."""
    pairs = []
    summary = getattr(state, "idea_summary", None)
    if summary:
        pairs.append(("idea_summary", summary))
    for record in getattr(state, "assertions", []) or []:
        if getattr(record, "superseded_by", None) is not None:
            continue
        content = getattr(record, "content", None)
        if content:
            pairs.append(("assertion:" + str(getattr(record, "record_id", "?")), content))
    for i, unknown in enumerate(getattr(state, "acknowledged_unknowns", []) or []):
        verbatim = getattr(unknown, "verbatim", None)
        if verbatim:
            pairs.append(("acknowledged_unknown:" + str(i), verbatim))
    for attr in ("known_problem", "known_mechanism"):
        ev = getattr(state, attr, None)
        content = getattr(ev, "content", None) if ev is not None else None
        if content:
            pairs.append((attr, content))
    return pairs


def _excerpt(text):
    text = " ".join(text.split())
    if len(text) <= _MAX_EXCERPT:
        return text
    return text[:_MAX_EXCERPT].rstrip() + "…"


def derive_inventor_stated_safety_signals(state) -> Tuple[SafetySignal, ...]:
    """Return the immutable tuple of inventor-stated safety signals for ``state``.

    Pure, deterministic, read-only. Never mutates ``state``. Every signal is
    inventor-stated and labelled as requiring independent validation. Returns an
    empty tuple when no conservative safety signal is present — which is NOT a
    statement that the idea is safe, unsafe, risk-free, or verified.
    """
    domain = _domain_of(state)
    signals = []
    n = 1
    seen = set()  # exact-duplicate statements (contract §4): first source wins
    for source, text in _inventor_texts(state):
        key = _dedup_key(text) if isinstance(text, str) else text
        if key in seen:
            continue
        seen.add(key)
        hit = _detect(text, domain)
        if hit is None:
            continue
        subject, failure, consequence, domain_context = hit
        signals.append(SafetySignal(
            signal_id="SIG-%03d" % n,
            source=source,
            provenance=PROVENANCE_INVENTOR_STATED,
            safety_subject=subject,
            failure_condition=failure,
            possible_consequence=consequence,
            domain_context=domain_context,
            validation_status=VALIDATION_REQUIRES_INDEPENDENT,
            display_label=_DISPLAY_LABEL,
            caution_text=_CAUTION_TEXT,
            statement=_excerpt(text),
        ))
        n += 1
    return tuple(signals)
