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
"""
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
)
_SUBJECT_CUES = (
    "insulation", "electric shock", "electrical shock", "shock", "overcurrent",
    "over-current", "over current", "overvoltage", "over-voltage",
    "short circuit", "short-circuit", "fire", "overheat", "overheating",
    "excessive heat", "high voltage", "mains", "live wire", "electrocut",
    "spark", "thermal runaway", "burn", "hazard", "warn", "warning", "alert",
    "detect",
)
_CONSEQUENCE_CUES = (
    "safety risk", "unsafe", "create a risk", "creates a risk", "could create a",
    "danger", "hazardous", "harm", "injury", "injure", "electrocut",
    "catch fire", "cause a fire", "shock the user", "miss a real risk",
    "missed warning", "too late", "late warning", "damage",
)
# Electronics/electrical context: satisfied by the session domain OR by an
# electrical-domain term appearing in the inventor's own text.
_ELECTRICAL_TERMS = (
    "insulation", "voltage", "current", "plug", "circuit", "wire", "battery",
    "mains", "electric", "electrical", "electronic", "overcurrent",
    "overvoltage", "relay", "sensor", "microcontroller", "capacitor",
    "resistor", "power", "fuse", "breaker",
)
# Negation guards: if present, the text is NOT treated as a safety signal.
_NEGATION_CUES = (
    "no safety concern", "no safety concerns", "not a safety", "safety is not",
    "no safety risk", "without safety risk", "poses no risk", "no risk of",
    "not create a risk", "without any risk", "no risk to",
)

_MAX_EXCERPT = 400  # bounded verbatim excerpt length for display


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


def _first_cue(lowered, cues):
    for cue in cues:
        if cue in lowered:
            return cue
    return None


def _domain_of(state):
    domain = getattr(state, "domain", None) or getattr(state, "domain_signal", None)
    return domain


def _has_electrical_context(lowered, domain):
    if domain == _MVP_DOMAIN:
        return True
    return any(term in lowered for term in _ELECTRICAL_TERMS)


def _detect(text, domain):
    """Return (subject, failure, consequence, domain_context) if ``text`` is a
    conservative inventor-stated safety signal, else None. Read-only, pure."""
    if not text or not isinstance(text, str):
        return None
    lowered = text.lower()
    if _first_cue(lowered, _NEGATION_CUES) is not None:
        return None
    subject = _first_cue(lowered, _SUBJECT_CUES)
    failure = _first_cue(lowered, _FAILURE_CUES)
    consequence = _first_cue(lowered, _CONSEQUENCE_CUES)
    if subject is None or failure is None or consequence is None:
        return None
    if not _has_electrical_context(lowered, domain):
        return None
    domain_context = domain if domain == _MVP_DOMAIN else _MVP_DOMAIN
    return subject, failure, consequence, domain_context


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
    for source, text in _inventor_texts(state):
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
