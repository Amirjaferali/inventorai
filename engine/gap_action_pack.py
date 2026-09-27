"""CAP-04 Slice 1 — the Actionable Gap Pack.

ONE read-only package per CURRENT unresolved gap, joining facts that already
exist in separate canonical owners so the inventor can see, in one place, what
the project truth currently calls for on that gap:

  * the gap requirement itself       — ``derive_requirement_landscape`` (the
    only unresolved-gap owner; OPEN / PARTIAL already collapse to one gap
    requirement per gap type there);
  * its required input / closure     — the SAME gap's ``derive_validation_plan``
    step (responsibility, evidence category, closure condition, verbatim);
  * routed needs for that exact gap  — ``need_routing.active_routes`` joined to
    its committed ``RoutingPolicy`` and its own Validation Plan step, ONLY by
    the exact ``(gap_type, question_id)`` identity.

Pure, deterministic, read-only, local: no Flask, session, persistence,
network, provider or language decision. It asks nothing, writes nothing,
closes nothing, ranks nothing and chooses nothing; the landscape order it keeps
is a stable identity order, not a priority. A structural inconsistency raises
``GapActionPackError`` (the surface then reads "unavailable", never "no gaps");
a routed need whose committed policy cannot be reconciled exactly is kept as
an unavailable detail rather than guessed.
"""
from dataclasses import dataclass
from typing import Optional, Tuple

from engine.idea_state import ACCEPTED_RISK
from engine.need_routing import OPERATION_ROUTE, active_routes
from engine.requirement_landscape import derive_requirement_landscape
from engine.validation_plan import derive_validation_plan

GAP_STATE_OPEN = "OPEN"
GAP_STATE_PARTIAL = "PARTIAL"
# The landscape's own source-status wording for a gap requirement; anything
# else is structurally inconsistent and fails closed.
_GAP_STATE_BY_SOURCE_STATUS = {
    "open": GAP_STATE_OPEN,
    "partially addressed": GAP_STATE_PARTIAL,
}
_ROUTED_ANCHOR_KINDS = {"SPECIALIST": "pending_specialist",
                        "EVIDENCE": "pending_evidence"}


class GapActionPackError(ValueError):
    """The canonical owners disagree; no pack set can be derived truthfully."""


@dataclass(frozen=True)
class RoutedNeed:
    """One CURRENT routed need of the pack's own gap. ``available`` is False
    when the exact route cannot be reconciled with its committed policy or its
    own Validation Plan step; every descriptive field is then None."""
    gap_type: str                  # traceability only — never shown
    question_id: str               # traceability only — never shown
    required_input: str            # SPECIALIST | EVIDENCE (route's own token)
    available: bool
    responsibility: Optional[str]
    evidence_category: Optional[str]
    closure_condition: Optional[str]
    need_text: Optional[str]
    need_text_ar: Optional[str]


@dataclass(frozen=True)
class GapActionPack:
    gap_type: str                  # canonical identity (traceability)
    requirement_id: str            # canonical identity (traceability)
    display_label: str             # the landscape's canonical label
    gap_state: str                 # OPEN | PARTIAL
    source_status: str             # the landscape's own status wording
    action_statement: str          # resolving_action.statement, verbatim
    responsibility: str            # the Validation Plan step, verbatim
    evidence_category: str
    closure_condition: str
    routed_needs: Tuple[RoutedNeed, ...]


@dataclass(frozen=True)
class GapActionPackSet:
    packs: Tuple[GapActionPack, ...]
    # Gaps whose lifecycle status is ACCEPTED_RISK: not unresolved-open, so no
    # pack, but never presented as resolved either.
    accepted_risk_gap_types: Tuple[str, ...]


def _policies_for(state):
    domain = getattr(state, "domain", None)
    if domain is None:
        return None
    try:
        from engine.path_n_questions import routing_policies
        return {(gap, qid): policy for gap, qid, policy in routing_policies(domain)}
    except Exception:
        return None


def _routed_need(gap_type, question_id, rev, policies, steps_by_ref):
    unavailable = RoutedNeed(gap_type, question_id, rev.required_input, False,
                             None, None, None, None, None)
    if rev.operation != OPERATION_ROUTE or policies is None:
        return unavailable
    policy = policies.get((gap_type, question_id))
    if policy is None or policy.policy_ref != rev.policy_ref \
            or policy.required_input != rev.required_input:
        return unavailable
    kind = _ROUTED_ANCHOR_KINDS.get(rev.required_input)
    step = steps_by_ref.get((kind, "routing:%s:%s" % (gap_type, question_id)))
    if kind is None or step is None:
        return unavailable
    return RoutedNeed(gap_type, question_id, rev.required_input, True,
                      step.responsibility, step.evidence_category,
                      step.closure_condition, policy.need_text, policy.need_text_ar)


def derive_gap_action_packs(state):
    """The ``GapActionPackSet`` for ``state``: one pack per unresolved gap
    requirement of the canonical landscape, in landscape order. Pure; raises
    ``GapActionPackError`` when the owners are inconsistent."""
    landscape = derive_requirement_landscape(state)
    plan = derive_validation_plan(state)
    steps_by_ref = {(s.provenance.anchor_kind, s.provenance.reference): s
                    for s in plan.steps}
    routes = active_routes(state)
    policies = _policies_for(state) if routes else {}

    packs = []
    seen = set()
    for req in landscape.requirements:
        anchor = req.primary_anchor
        if anchor.anchor_kind != "gap":
            continue
        gap_type = anchor.anchor_reference
        if gap_type in seen:
            raise GapActionPackError("duplicate gap requirement")
        seen.add(gap_type)
        gap_state = _GAP_STATE_BY_SOURCE_STATUS.get(req.source_status)
        step = steps_by_ref.get(("gap", gap_type))
        if gap_state is None or step is None or req.resolving_action is None \
                or not isinstance(anchor.display_label, str) \
                or not anchor.display_label.strip():
            raise GapActionPackError("gap requirement cannot be joined")
        routed = tuple(
            _routed_need(g, qid, rev, policies, steps_by_ref)
            for (g, qid), rev in routes.items() if g == gap_type)
        packs.append(GapActionPack(
            gap_type=gap_type,
            requirement_id=req.requirement_id,
            display_label=anchor.display_label,
            gap_state=gap_state,
            source_status=req.source_status,
            action_statement=req.resolving_action.statement,
            responsibility=step.responsibility,
            evidence_category=step.evidence_category,
            closure_condition=step.closure_condition,
            routed_needs=routed,
        ))
    accepted = tuple(sorted(
        g.gap_type for g in getattr(state, "gaps", []) or []
        if getattr(g, "status", None) == ACCEPTED_RISK))
    return GapActionPackSet(packs=tuple(packs), accepted_risk_gap_types=accepted)
