"""
engine/readiness_snapshot.py
READINESS-SNAPSHOT-RUNTIME-01 — the first runtime presentation of Readiness.

It answers ONE question: *what evidence is currently available for each
readiness dimension?* It does not answer "should I proceed?" — that belongs to
the product verdict and to FDC-001, both untouched here.

WHY THIS IS NOT AN ENGINE
-------------------------
It decides nothing. In this product version exactly ONE disposition is
reachable, `INSUFFICIENT_EVIDENCE`, and that is a property of the code rather
than of the data: `PASS`, `PASS_WITH_CONDITIONS` and `HOLD` are not merely
unreached here, they are not constructible — no branch, threshold, comparison or
count can produce them, so no future input makes one appear. There is no score,
no percentage, no composite, no ranking and no threshold anywhere below.

It also persists nothing. Every function is pure: same inputs, same output, no
I/O, no durable record, no cache. Calling it twice changes nothing.

WHY EACH DIMENSION SAYS WHAT IT SAYS
------------------------------------
* TECHNICAL — insufficient because the evidence ladder's upper tiers have no
  authorized writer in this version. Owner statements are recorded at ASSERTED
  or REASONED and stay UNVALIDATED, so a positive verified disposition cannot be
  awarded to anyone. That is a limit of THIS VERSION, not a finding about the
  invention: it says nothing about whether the idea works.
* COMMERCIAL — insufficient because every recorded item is the inventor's own
  statement, which nothing has checked. Recording is never validating. The
  counts below report WHAT WAS RECORDED and never interpret it: no demand, no
  market size, no attractiveness, no willingness to pay, no profitability and no
  investment judgement is inferred from them, ever.
* MANUFACTURING — not assessed at all, so it receives NO disposition, not even
  `INSUFFICIENT_EVIDENCE`. Saying "insufficient evidence" would imply somebody
  looked; nobody has.

ABSENCE IS NOT NEGATIVE EVIDENCE. A project with no Commercial evidence has a
blank page, not a poor market. An unassessed Manufacturing dimension is not a
manufacturing problem. Unverified technical evidence is not a technical
impossibility. The wording each row carries is chosen so a reader cannot take
the opposite meaning.
"""
from engine.commercial_evidence import (
    ACTIVE_DIMENSIONS,
    CLAIM_STATUS_UNVALIDATED,
    commercial_evidence_view,
    manufacturing_evidence_view,
)
from engine.derived_readiness import READINESS_GAP_CONTEXTS, derive_readiness
from engine.idea_state import UNVALIDATED, VALIDATED_STATUSES

# The Owner-adopted Readiness vocabulary. Only the first is emittable in this
# version; the others are named here ONLY so a test can assert their absence,
# and no code path below can return one.
DISPOSITION_INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"

#: The dispositions this module is permitted to emit. One value, deliberately.
EMITTABLE_DISPOSITIONS = (DISPOSITION_INSUFFICIENT_EVIDENCE,)

# Dimension keys of the snapshot rows, in presentation order.
ROW_TECHNICAL = "technical"
ROW_COMMERCIAL = "commercial"
ROW_MANUFACTURING = "manufacturing"

# Why a dimension is insufficient — a closed set of REASON CODES the caller
# renders into its own bilingual wording. A reason explains the state of the
# EVIDENCE; none of them is a judgement about the idea.
REASON_NO_UPPER_TIER_WRITER = "no_upper_tier_writer"     # technical
REASON_NOTHING_RECORDED = "nothing_recorded"             # commercial, zero rows
REASON_RECORDED_BUT_UNCHECKED = "recorded_but_unchecked"  # evidence, >0 rows
# `STATE_NOT_ASSESSED` retired at `MANUFACTURING-READINESS-SNAPSHOT-01`.
# Manufacturing had no evidence owner then, so "nobody has looked" was the only
# truthful thing to say. It has one now, so its evidence sufficiency can be
# reported exactly as Commercial's is — and a constant asserting nobody has
# looked would be the stale half of a true statement.


def technical_row(state):
    """Compose the Technical row from the EXISTING derived-readiness owner and
    the ledger it already reads. Pure; reads no store and writes nothing.

    ``verified_contexts`` is always 0 in this version and is reported rather
    than hidden, so the row stays truthful if an upper-tier writer is ever
    authorized: the counts would change, and only then would this module need to
    learn a second disposition."""
    readiness = derive_readiness(state)
    records = [r for r in getattr(state, "assertions", None) or ()
               if r.gap_context in READINESS_GAP_CONTEXTS]
    contexts = sorted({r.gap_context for r in records})
    qualities = {getattr(r, "quality", None) for r in records}
    qualities.discard(None)
    validated = [r for r in records
                 if getattr(r, "validation_status", UNVALIDATED)
                 in VALIDATED_STATUSES]
    return {
        "dimension": ROW_TECHNICAL,
        "disposition": DISPOSITION_INSUFFICIENT_EVIDENCE,
        "reason": REASON_NO_UPPER_TIER_WRITER,
        "recorded_items": len(records),
        "areas_covered": len(contexts),
        "qualities": tuple(sorted(qualities)),
        "all_unvalidated": not validated,
        "verified_contexts": len(
            [c for c in contexts if readiness.is_verified(c)]),
    }


def _evidence_row(dimension, view):
    """Compose ONE evidence-sufficiency row from a dimension's OWN canonical
    view. Pure, and identical for every dimension by construction.

    The disposition is a constant, not a computation: no count, no ratio and no
    comparison below can produce anything but `INSUFFICIENT_EVIDENCE`, because
    every item any owner can currently hold is the inventor's own UNVALIDATED
    statement and no authorized path promotes one. The counts report WHAT WAS
    RECORDED; none is a threshold, and none is interpreted. Two dimensions
    reporting the same disposition does not make them comparable — it means
    neither has validated evidence, which is a statement about this version
    rather than about either subject."""
    statuses = {r["claim_status"] for r in view["active"]}
    return {
        "dimension": dimension,
        "disposition": DISPOSITION_INSUFFICIENT_EVIDENCE,
        "reason": (REASON_NOTHING_RECORDED if not view["total"]
                   else REASON_RECORDED_BUT_UNCHECKED),
        "recorded_items": view["total"],
        "topics_covered": len(view["topics"]),
        "topics": tuple(view["topics"]),
        # True iff every recorded item is still the inventor's unchecked
        # statement. Reported, never used as a threshold.
        "all_unvalidated": statuses <= {CLAIM_STATUS_UNVALIDATED},
    }


def commercial_row(rows):
    """Compose the Commercial row from the AUTHORITATIVE Commercial Evidence
    Owner's own view and nothing else. Pure.

    ``rows`` is the project's durable evidence history as the store returns it.
    The counts are of what the inventor recorded; the row never reads a verdict,
    a decision workspace, a requirement landscape or free text elsewhere, and it
    interprets none of what it counts."""
    return _evidence_row(ROW_COMMERCIAL, commercial_evidence_view(rows))


def manufacturing_row(rows):
    """Compose the Manufacturing row from the AUTHORITATIVE Manufacturing
    Evidence Owner's own view and nothing else. Pure.

    This row previously carried NO disposition, because Manufacturing had no
    evidence owner and saying "insufficient evidence" would have implied an
    assessment nobody had made. It has an owner now, so the honest thing to
    report is the same thing Commercial reports: what was recorded, and that
    none of it has been checked.

    What has NOT changed is what the row means. It is evidence sufficiency, not
    manufacturability: it says nothing about whether the thing can be made, made
    affordably, or made at all, and no count of materials, processes or tooling
    moves it toward saying so. The dimension reads NOTHING from the Technical
    ledger, Commercial evidence, requirements, the verdict, the decision
    workspace, or cost text recorded anywhere else."""
    return _evidence_row(ROW_MANUFACTURING, manufacturing_evidence_view(rows))


def readiness_snapshot(state, evidence_rows):
    """The whole snapshot: three rows in presentation order. Pure.

    Composes the existing authoritative owners and nothing else. Creates no
    record, writes nothing, and can emit no disposition other than
    `INSUFFICIENT_EVIDENCE`.

    ``evidence_rows`` is the project's WHOLE durable evidence history; each row
    scopes it to its own dimension through that dimension's canonical view, so
    a Commercial item can never reach the Manufacturing count or the reverse.

    There is deliberately NO aggregate. No overall disposition, no weakest link,
    no percentage, no traffic light, no weighted anything: three independent
    statements about three independent bodies of evidence. Combining them would
    invent a judgement none of the owners made, and the fact that all three
    currently read the same is a fact about this version's validation paths
    rather than a finding that the three are equally far along."""
    return {
        "rows": (technical_row(state),
                 commercial_row(evidence_rows),
                 manufacturing_row(evidence_rows)),
        "dimensions": (ROW_TECHNICAL, ROW_COMMERCIAL, ROW_MANUFACTURING),
        # Which dimensions accept EVIDENCE, composed from the canonical owner
        # rather than restated, so this can never drift from the truth again.
        # Named `evidence_*` deliberately: Manufacturing accepting evidence says
        # NOTHING about Manufacturing readiness, which remains unassessed and
        # undispositioned. Reading this as a readiness state would be exactly
        # the confusion the Manufacturing row is worded to prevent.
        "evidence_dimensions_active": tuple(ACTIVE_DIMENSIONS),
    }
