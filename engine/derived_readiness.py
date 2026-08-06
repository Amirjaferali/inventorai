"""
engine/derived_readiness.py
Increment 2 — pure, non-mutating derivation of current verified readiness.

`derive_readiness(state)` returns a read-only `DerivedReadiness` view computed
ENTIRELY from already-stored state (gap lifecycle, the append-only interaction
ledger, provenance, validation status, dispositions, pending state, and
contradiction/supersession relationships).

It is purely derived and MUST NOT:
  * modify maturity, reverse lifecycle, or close/reopen gaps;
  * rewrite or mutate evidence or any record;
  * resolve contradictions automatically;
  * rank sources or select a winning claim;
  * introduce any numeric scoring framework;
  * call or modify score_case().

Derived verified readiness can DECREASE and can present BELOW stored CLOSED /
high maturity: a stored CLOSED gap or high maturity does NOT force derived
verified readiness. A gap context is "verified" only when its ACTIVE recorded
interactions carry no owner-unvalidated, provisional, pending, or
unresolved-conflict state.

Owner ruling on supersession (F-3): an explicitly superseded record is retained
IMMUTABLY in history (content, provenance, validation, identity unchanged) but is
DEACTIVATED for current readiness evaluation only. The superseding record is
evaluated normally — so an unvalidated record superseded by an independently
verified record may permit verified readiness when no other ACTIVE blocker
remains, while a verified record superseded by an unvalidated record does not.
This performs no ranking, source selection, winner selection, or automated
conflict resolution; it merely excludes the deactivated record from the CURRENT
active set. Contradiction edges still block only while BOTH endpoints are active.
"""
from engine.idea_state import (
    UNVALIDATED,
    DISPOSITION_PROVISIONAL_ASSUMPTION,
)


class DerivedReadiness:
    """Read-only derived view. Holds no mutable authority over the state; every
    method recomputes from the snapshot captured at construction."""

    def __init__(self, state):
        self._state = state
        by_context = {}
        for r in getattr(state, "assertions", []):
            by_context.setdefault(r.gap_context, []).append(r)
        self._by_context = by_context

    @staticmethod
    def _is_active(record):
        """A record is ACTIVE for current readiness unless it has been explicitly
        superseded (owner ruling F-3). Superseded records remain in history but
        are deactivated for current evaluation only."""
        return getattr(record, "superseded_by", None) is None

    def _active(self, gap_type):
        return [r for r in self._by_context.get(gap_type, []) if self._is_active(r)]

    def _has_active_unresolved_contradiction(self, gap_type):
        """A contradiction blocks readiness only while BOTH endpoints are active.
        Superseding one endpoint deactivates that side, so a contradiction with a
        superseded record no longer blocks the active set. No conflict is resolved
        automatically; the deactivated record is simply not in the active set."""
        active = self._active(gap_type)
        active_ids = {r.record_id for r in active}
        for r in active:
            if any(other in active_ids for other in getattr(r, "contradicts", [])):
                return True
        return False

    def is_verified(self, gap_type):
        """True only if every ACTIVE interaction for this context is validated and
        none is provisional, pending, or in an active unresolved contradiction.
        With no active records, readiness is not verified (nothing to stand on).
        Stored CLOSED / maturity are intentionally NOT inputs here."""
        recs = self._active(gap_type)
        if not recs:
            return False
        if any(r.disposition == DISPOSITION_PROVISIONAL_ASSUMPTION for r in recs):
            return False
        if any(getattr(r, "pending", None) for r in recs):
            return False
        if self._has_active_unresolved_contradiction(gap_type):
            return False
        if any(r.validation_status == UNVALIDATED for r in recs):
            return False
        return True

    def unverified_contexts(self):
        """Gap contexts that have records but are not verified."""
        return [c for c in self._by_context if not self.is_verified(c)]

    def overall_verified(self):
        """True only if at least one gap context has records and every gap
        context with records is verified. Absent any records, there is no basis
        to claim verified readiness, so this is False."""
        contexts = list(self._by_context)
        if not contexts:
            return False
        return all(self.is_verified(c) for c in contexts)


def derive_readiness(state):
    """Pure factory: build a read-only DerivedReadiness view of `state`."""
    return DerivedReadiness(state)
