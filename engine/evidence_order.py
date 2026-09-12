"""
engine/evidence_order.py
T2-F — the ONE canonical semantic ordering of the evidence-quality axis.

Purpose
-------
`ASSERTED < REASONED < DEMONSTRATED` is a SEMANTIC ladder. Python's string
comparison is not: it orders the committed constants
`ASSERTED < DEMONSTRATED < REASONED`, so `'DEMONSTRATED' >= 'REASONED'` is
False. Every raw `>=` / `>` on the quality axis therefore encodes the WRONG
ladder, and the defect is masked today only because no writer produces
`DEMONSTRATED`. This module is the single place the ladder is defined, so the
masking invariant becomes enforced rather than emergent.

Input contract
--------------
`quality_rank(q)`          -> int rank for a recognised constant.
`quality_at_least(q, floor)` -> bool: is `q` at least as strong as `floor`?
`quality_stronger(a, b)`   -> bool: is `a` strictly stronger than `b`?

Output contract
---------------
Ranks are ordinal ONLY. They are an ordering device, never a score, weight,
confidence, percentage or threshold, and they are never serialized, persisted,
exported or displayed.

Prohibited behaviours
---------------------
* changing the serialized constants (they stay "ASSERTED"/"REASONED"/
  "DEMONSTRATED" everywhere they are stored, exported or rendered);
* silently coercing an unrecognised value to a tier;
* introducing a second ordering map anywhere in the tree;
* any promotion rule — this module orders values, it never writes one.

Unknown-value behaviour (explicit, and deliberately NOT uniform)
---------------------------------------------------------------
* `None` is the legacy "no quality recorded" value carried by pre-Increment-2
  `Evidence`/`AssertionRecord` rows. It ranks BELOW every tier and never
  raises, which is exactly the behaviour the existing raw comparisons already
  produced for it. Legacy rows keep their current meaning.
* Any OTHER unrecognised value raises `UnknownQualityError`. Callers at the
  PROGRESSION authority must let it propagate: that boundary decides promotion
  and must never promote on a value it cannot interpret. The presentation
  boundary (`engine.deliverable_assembler`) is documented "never raises" and
  keeps its own fail-closed map instead of calling this module.
"""
from engine.idea_state import ASSERTED, REASONED, DEMONSTRATED


class UnknownQualityError(ValueError):
    """Raised when a quality value is not a recognised tier and is not the
    legacy ``None``. Carries only the repr of the offending value — never user
    content, an identifier, or any surrounding state."""


#: The canonical semantic ladder. Ordinal positions only; see the module
#: contract above. `engine.deliverable_assembler` keeps a separate fail-closed
#: presentation map by design (it must never raise); a test pins the two to be
#: value-equivalent so they can never drift apart.
QUALITY_ORDER = {
    ASSERTED: 0,
    REASONED: 1,
    DEMONSTRATED: 2,
}

#: Strictly below every tier: the rank of a legacy record with no recorded
#: quality. Never a tier, never written, never displayed.
_NO_QUALITY_RANK = -1


def quality_rank(quality):
    """Ordinal rank of ``quality`` on the canonical ladder.

    ``None`` (legacy, no quality recorded) ranks below every tier. Any other
    unrecognised value raises ``UnknownQualityError`` — a corruption tripwire
    for the progression authority, not a user-visible path (``assess_response``
    returns only ``ASSERTED`` or ``REASONED``)."""
    if quality is None:
        return _NO_QUALITY_RANK
    try:
        return QUALITY_ORDER[quality]
    except (KeyError, TypeError):
        raise UnknownQualityError(
            "unrecognised evidence quality: %r" % (quality,)) from None


def quality_at_least(quality, floor):
    """True when ``quality`` is at least as strong as ``floor`` on the
    canonical ladder (the semantic replacement for a raw ``>=``)."""
    return quality_rank(quality) >= quality_rank(floor)


def quality_stronger(quality, other):
    """True when ``quality`` is strictly stronger than ``other`` on the
    canonical ladder (the semantic replacement for a raw ``>``)."""
    return quality_rank(quality) > quality_rank(other)
