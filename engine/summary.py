"""
Summary Builder — deterministic output only.
Reads existing IdeaState — no engine behavior changes.
No API calls. No new domains. No scoring changes.
Governed by: MVP_SCOPE_FREEZE.md
"""

from datetime import datetime
from engine.idea_state import IdeaState, OPEN, PARTIAL, CLOSED, ACCEPTED_RISK


def _extract_boundaries(state: IdeaState) -> list:
    """
    Extract boundary statements from iteration_log.
    Looks for responses given after boundary questions.
    No new fields added to IdeaState.
    """
    boundary_keywords = [
        "not do", "not cover", "does not", "only works",
        "cannot", "limited to", "excludes", "boundary",
        "does not work", "not store", "not replace"
    ]
    boundaries = []
    for log in state.iteration_log:
        q = (log.question_asked or "").lower()
        r = (log.response_summary or "").lower()
        if "not do" in q or "not cover" in q or "boundary" in q:
            if log.response_summary and len(log.response_summary) > 10:
                boundaries.append(log.response_summary[:200])
        elif any(kw in r for kw in boundary_keywords):
            if log.response_summary and len(log.response_summary) > 10:
                boundaries.append(log.response_summary[:200])
    return boundaries


def _next_step(state: IdeaState) -> str:
    """
    Deterministic next step recommendation.
    No AI. No API. Pure state logic.
    """
    if state.maturity_level == 0:
        return "Describe the problem your invention solves and who experiences it."

    if state.maturity_level == 1:
        mech = state.known_mechanism
        if mech is None:
            return "Describe HOW your invention works at a functional level."
        if mech.quality == "ASSERTED":
            return "Provide more detail on the mechanism — explain the reasoning, not just the outcome."
        return "Name the physical operating principle your mechanism relies on."

    if state.maturity_level == 2:
        open_gaps = [g for g in state.gaps if g.status in (OPEN, PARTIAL)]
        if open_gaps:
            gap_names = [g.gap_type for g in open_gaps]
            return f"Address remaining gaps before external review: {', '.join(gap_names)}"
        return "Ready for domain expert or patent advisor review."

    return "Continue progression to next maturity level."


def build_summary(state: IdeaState) -> dict:
    """
    Build deterministic JSON summary from existing IdeaState.
    Same input → same output shape always.
    """
    # Evidence quality
    qualities = []
    if state.known_problem:
        qualities.append(state.known_problem.quality)
    if state.known_mechanism:
        qualities.append(state.known_mechanism.quality)

    evidence_quality = max(
        qualities,
        key=lambda q: ["ASSERTED", "REASONED", "DEMONSTRATED"].index(q)
    ) if qualities else "NONE"

    # Gaps
    all_gaps = [
        {
            "type": g.gap_type,
            "status": g.status,
            "iterations_open": g.iterations_open,
        }
        for g in state.gaps
    ]

    open_gaps = [g for g in all_gaps if g["status"] in (OPEN, PARTIAL)]

    # Boundaries from log
    boundaries = _extract_boundaries(state)

    summary = {
        "idea_id"             : state.idea_id,
        "domain_signal"       : state.domain_signal or "unknown",
        "maturity_level"      : state.maturity_level,
        "direction"           : state.direction,
        "total_iterations"    : state.iteration,

        "known_problem"       : {
            "content" : state.known_problem.content[:200] if state.known_problem else None,
            "quality" : state.known_problem.quality if state.known_problem else None,
        },

        "known_mechanism"     : {
            "content" : state.known_mechanism.content[:200] if state.known_mechanism else None,
            "quality" : state.known_mechanism.quality if state.known_mechanism else None,
        },

        "known_boundaries"    : boundaries,

        "gaps"                : all_gaps,
        "open_gaps"           : open_gaps,
        "open_gap_count"      : len(open_gaps),

        "evidence_quality"    : evidence_quality,
        "next_recommended_step": _next_step(state),

        "generated_at"        : datetime.utcnow().isoformat() + "Z",
    }

    return summary
