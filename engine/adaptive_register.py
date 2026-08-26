"""W2-B / RVR-6a — derived evidence-weighted reversible register calibration.

Authority: W2-B implementation contract (PR #573) §B.5/§C/§D as amended by
Contract Amendment 1 §8 (authoritative via PR #575), enacting OD-R5 and
Wave-2 contract §G (architecture A: deterministic recomputation from stored
answer content via the EXISTING pure assessors — no new persistent field).

Purpose (and only this):
  * classify each ACTIVE ``answered`` ledger record into one deterministic
    evidence signal (STRONG / WEAK / NONE) using ONLY the existing pure
    assessors — ``engine.gap_relevance.addresses_gap`` (the one governed
    relevance owner) and ``engine.progression_loop._structured_technical_form``
    (the Layer-3 structural-technical predicate) plus the existing
    ``_WEAK_PATTERNS`` exact-form refusal guard;
  * fold those signals, in canonical ``rec_N`` order, into ONE bounded
    two-level register (NEUTRAL / ELEVATED) with deterministic hysteresis:
    W consecutive STRONG signals raise, M contrary WEAK signals lower.

Input contract: a canonical ``IdeaState`` (only ``state.assertions`` is
read). Output contract: an immutable ``RegisterState``.

Prohibited behaviours (contract §D/§H — boundaries):
  * NEVER persisted — recomputed on demand from the amended active ledger;
    reconstruction/replay reproduces it byte-identically because its inputs
    are exactly the restored ledger truth;
  * the stored per-answer ``quality`` field is a STATE-LEVEL AGGREGATE and
    is NEVER consumed here as an answer-local signal (§D disclosure);
  * no persona, no profile, no model inference, no permanent flag, no
    timestamps, no randomness; NEUTRAL on insufficient or conflicting
    evidence (empty ledger, missing gap identity, alternating signals);
  * REVERSIBLE by construction: superseding a contributing record changes
    the recomputation; WEAK signals lower an ELEVATED register after M
    occurrences; nothing is ever latched.

REGISTER LEVEL COUNT (Amendment §8.2 proposal-row duty): exactly TWO levels
(NEUTRAL / ELEVATED) — the bounded minimum. No repository authority
enumerates register levels; a third level would have NO consumer (the only
register-gated behavior is the completed-intent skip, a binary gate), so a
wider scale would be unconsumed scope. Proposal, ratified only at Owner
exact-SHA acceptance.

W/M values (contract §C as amended by §8.1-§8.2): ``W_PROPOSED = 2`` /
``M_PROPOSED = 2`` is the CURRENT OWNER-PERMITTED PROPOSAL — NOT
Owner-accepted, NOT frozen. The earlier M=1 proposal was OVERTURNED by
oscillation/churn evidence (repeated strong-strong-weak cycles flip the
register 8 times in 12 answers at M=1 versus once at M=2 — re-derived in
tests/test_w2b_amc_register_calibration.py, which also exercises W in
{1,2,3} and M in {1,2,3} per the §8.2 anti-hard-coding rule). Values freeze
ONLY at Owner exact-SHA acceptance of this implementation candidate.
"""
from dataclasses import dataclass

from engine.gap_relevance import addresses_gap
from engine.idea_state import DISPOSITION_ANSWERED
from engine.progression_loop import _structured_technical_form, _WEAK_PATTERNS

# Register levels — deliberately exactly two (see the level-count proposal
# in the module docstring).
REGISTER_NEUTRAL = "NEUTRAL"
REGISTER_ELEVATED = "ELEVATED"

# Per-record evidence signals.
SIGNAL_STRONG = "STRONG"   # addresses its served gap AND structural-technical
SIGNAL_WEAK = "WEAK"       # exact weak/refusal form, or does not address it
SIGNAL_NONE = "NONE"       # substantive-but-unstructured, or insufficient
                           # identity (no gap_context / empty content)

# CURRENT OWNER-PERMITTED PROPOSAL (Amendment §8.1) — not accepted, not
# frozen; the calibration suite attempts to falsify these values.
W_PROPOSED = 2   # raise: consecutive STRONG signals required for ELEVATED
M_PROPOSED = 2   # lower: contrary WEAK signals that revert to NEUTRAL


@dataclass(frozen=True)
class RegisterState:
    """Immutable derived register snapshot. ``contributions`` cites every
    record that fed the fold — (record_id, signal) in canonical order — the
    §H provenance requirement (evaluator-facing evidence, not a UI claim)."""
    level: str
    strong_run: int
    weak_run: int
    contributions: tuple


def _record_seq(record_id):
    """Canonical ``rec_N`` ordering key. A non-canonical id fails loudly
    (never silently mis-orders) — canonical mints always produce rec_N."""
    prefix, _, num = str(record_id).partition("_")
    if prefix != "rec" or not num.isdigit():
        raise ValueError(f"non-canonical ledger record id: {record_id!r}")
    return int(num)


def classify_answer_signal(record):
    """Deterministic per-record evidence signal for one ACTIVE answered
    record. Pure; consumes ONLY the stored verbatim content and the recorded
    served-gap identity — never the stored ``quality`` aggregate."""
    content = (record.content or "").strip()
    if not content:
        return SIGNAL_NONE
    lowered = content.lower()
    if lowered in _WEAK_PATTERNS:
        return SIGNAL_WEAK
    gap_context = getattr(record, "gap_context", None)
    if not gap_context:
        # No served-gap identity: insufficient evidence — neither strength
        # nor contrariness is fabricated from an unattributed answer.
        return SIGNAL_NONE
    if not addresses_gap(content, gap_context):
        # A non-responsive answer is contrary evidence for calibration
        # purposes only — nothing here re-scores or re-classifies the answer.
        return SIGNAL_WEAK
    if _structured_technical_form(lowered):
        return SIGNAL_STRONG
    return SIGNAL_NONE


def compute_register(state, w=W_PROPOSED, m=M_PROPOSED):
    """Fold the ACTIVE answered ledger into the derived register.

    Deterministic and insertion-order independent (records fold in canonical
    ``rec_N`` order regardless of list order); pure (no mutation, no
    persistence, no I/O). Hysteresis: ``w`` consecutive STRONG signals raise
    NEUTRAL -> ELEVATED; while ELEVATED, ``m`` WEAK signals lower back to
    NEUTRAL (the strong run then restarts from zero). A STRONG signal while
    ELEVATED resets the contrary count (hysteresis, not a latch: any
    ``m``-run of WEAK signals still lowers, and supersession recomputation
    always applies). A NONE signal breaks a consecutive-strong run but is
    NOT contrary evidence — it never lowers an ELEVATED register.

    The ``w``/``m`` parameters exist so the calibration suite can actually
    exercise bounded alternatives (Amendment §8.2 anti-hard-coding rule);
    runtime callers use the module proposal defaults.
    """
    records = sorted(
        (r for r in getattr(state, "assertions", [])
         if getattr(r, "superseded_by", None) is None
         and r.disposition == DISPOSITION_ANSWERED),
        key=lambda r: _record_seq(r.record_id))
    level = REGISTER_NEUTRAL
    strong_run = 0
    weak_run = 0
    contributions = []
    for record in records:
        signal = classify_answer_signal(record)
        contributions.append((record.record_id, signal))
        if signal == SIGNAL_STRONG:
            weak_run = 0
            strong_run += 1
            if level == REGISTER_NEUTRAL and strong_run >= w:
                level = REGISTER_ELEVATED
        elif signal == SIGNAL_WEAK:
            strong_run = 0
            if level == REGISTER_ELEVATED:
                weak_run += 1
                if weak_run >= m:
                    level = REGISTER_NEUTRAL
                    weak_run = 0
        else:  # SIGNAL_NONE
            strong_run = 0
    return RegisterState(level=level, strong_run=strong_run,
                         weak_run=weak_run,
                         contributions=tuple(contributions))
