"""Plain-Language Result Feedback — deterministic, display-only feedback text.

DETERMINISTIC, DISPLAY-ONLY, CONTENT-FREE RESULT FEEDBACK — WEB/DISPLAY LAYER.

Governed by
`docs/governance/PLAIN_LANGUAGE_RESULT_FEEDBACK_INCREMENT_CONTRACT.md`
(true-merged via PR #155) and its scope decision
`docs/governance/PLAIN_LANGUAGE_RESULT_FEEDBACK_SCOPE_DECISION.md` (PR #153).

Maps the already-computed session result (its transition + raw reason) to a
short, supportive, plain-language explanation for the PRIMARY visible feedback
line, so the inventor does not see raw engine-internal tokens such as
"MECHANISM_COMPLETENESS asserted only — reasoning required" as the main feedback.
The raw authoritative reason is preserved unchanged by the caller and rendered
only as non-primary provenance.

Strict boundaries (contract sections 5, 7, 8, 13):
  * Pure, deterministic, display-only. Computed at render time from the given
    result alone. No engine call, no AI/LLM call, no network, no I/O, no
    persistence, no stored state, no hidden state, and no imports of engine /
    scoring / persistence / Safety-Signals / domain-gate modules.
  * It NEVER alters `last_result`; NEVER rewrites `last_result.reason`; NEVER
    recomputes scoring, transition, maturity, gaps, or failed criteria; and never
    changes any PASS/WARN/BLOCK outcome. The truthful transition badge and the
    raw reason (as provenance) are rendered by the template independently.
  * It returns only user-facing display text, or ``None`` when no feedback line
    should render. It NEVER supplies answer content, a component, a number, a
    material, a mechanism, a safety fact, or a domain detail, and never claims
    the answer/idea is production-ready, engineering-validated, safe, compliant,
    patent-ready, feasibility-validated, or complete beyond the current demo flow.
  * The inventor remains the sole author of any saved answer; this module reads
    and writes no answer text.

Distinct from `web/scaffolding_guidance.py`: that helper offers "what KIND of
detail to add" prompts in the WARN state; this helper explains the RESULT itself
(WARN/PASS/BLOCK) in plain language. Both read the same already-computed
`last_result` read-only; neither mutates it.
"""

# --- Pinned friendly copy (increment contract section 10) ------------------
# Supportive, plain-language, truthful, concise, neutral, non-authoring, and
# free of raw internal tokens. The PASS strings are scoped to "the current demo
# flow" so they make no engineering / readiness / validation claim.
# Detector-honest (owner-gated feedback-truthfulness correction): the system
# knows only that its recognizer did not detect enough explicit structure; it
# must never claim the answer lacks reasoning (answers using "because"/"since"
# or step-by-step causal chains can remain in this state).
_WARN_ASSERTED_ONLY = (
    "The current demo did not recognize enough explicit reasoning structure in "
    "your answer to move this area forward yet. Making the cause-and-effect "
    "relationship more explicit may help."
)
# Accepted-partial (Increment 1 — accepted-vs-rejected result-state clarity):
# a first REASONED answer that moved the gap to PARTIAL was ACCEPTED and counts
# toward closure. The wording must communicate accepted / counted / progressed /
# not yet complete, and must never imply rejection.
_WARN_PARTIALLY_ADDRESSED = (
    "Your answer was accepted and moved this area forward. One focused "
    "follow-up is still needed to complete it."
)
_PASS_DEMONSTRATED_EVIDENCE = (
    "This point is supported well enough to move forward in the current demo flow."
)
_PASS_REASONED_FOLLOW_UP = (
    "Your follow-up added enough reasoning to continue in the current demo flow."
)
_NOT_ESTABLISHED = (
    "This point is not established yet, so the idea cannot move forward on this item."
)
# Semantic WARN corrections (independent-review defect): distinct live WARN
# reasons whose meaning is NOT "unestablished". Each is plain-language, truthful,
# concise, non-authoring, and free of readiness/validation/safety/compliance/
# feasibility/patent claims.
_MVP_CAP = (
    "This point has reached the highest maturity level supported by the current MVP demo."
)
_SEQUENCING = (
    "An earlier required step needs to be addressed first before this can move forward."
)
_REASONED_MINIMUM = (
    "This needs more reasoning or supporting detail before it can move forward."
)
# Conservative fallback for an unknown / future WARN reason: it does NOT invent
# the cause, does NOT claim the point is unestablished, and points the inventor
# to the raw reason preserved in the non-primary result details.
_GENERIC_WARN = (
    "This point cannot move forward yet. Review the result details for the specific reason."
)


def get_result_feedback(last_result):
    """Return a plain-language feedback string for the current result, or None.

    Pure and deterministic. ``last_result`` is the already-computed result dict
    (or None). Reads only its ``transition`` and raw ``reason``; never mutates
    them, never re-scores. Keyed on the transition, with WARN/PASS
    sub-classification by stable substrings of the raw reason (the same read-only
    substrings `scaffolding_guidance` relies on). Unknown / unexpected
    reason/gap combinations degrade SAFELY to a truthful, non-success message
    rather than inventing a misleading success (contract test 28). Returns
    ``None`` when there is no result or no recognized transition, so no feedback
    line renders. Never raises; performs no I/O.
    """
    if not isinstance(last_result, dict):
        return None
    transition = last_result.get("transition")
    reason = last_result.get("reason") or ""

    if transition == "PASS":
        if "REASONED follow-up" in reason:
            return _PASS_REASONED_FOLLOW_UP
        # "DEMONSTRATED evidence", or a maturity-advance PASS
        # ("... established — ready for LEVEL ...") — both are truthful
        # "supported well enough to move forward in the current demo flow".
        return _PASS_DEMONSTRATED_EVIDENCE

    if transition == "WARN":
        # Semantically faithful mapping of every live WARN reason. Specific
        # categories are matched before the generic fallback; the raw reason is
        # never mutated. See the source-review live-reason inventory:
        #   "{gap_type} asserted only — reasoning required"      -> asserted-only
        #   "{gap_type} partially addressed — needs more depth"  -> partially
        #   "LEVEL N is max for MVP"                             -> MVP maturity cap
        #   "... must be attempted first"                        -> sequencing
        #   "... must be REASONED minimum"                       -> reasoning needed
        #   "... not (yet) established / not yet closed / opened"-> not established
        #   anything else                                        -> conservative fallback
        if "asserted only" in reason:
            return _WARN_ASSERTED_ONLY
        if "partially addressed" in reason:
            return _WARN_PARTIALLY_ADDRESSED
        if "is max for MVP" in reason:
            return _MVP_CAP
        if "must be attempted first" in reason:
            return _SEQUENCING
        if "REASONED minimum" in reason:
            return _REASONED_MINIMUM
        if ("not established" in reason or "not yet established" in reason
                or "not yet closed" in reason or "not yet opened" in reason):
            return _NOT_ESTABLISHED
        # Unknown / future WARN reason: do not invent the cause, do not claim the
        # point is unestablished, and direct the inventor to the result details.
        return _GENERIC_WARN

    if transition == "BLOCK":
        # A genuine BLOCK means there is not enough to continue on this item.
        return _NOT_ESTABLISHED

    # No result / unrecognized transition: render no feedback message.
    return None


# --- Result-state badge (Increment 1: accepted-vs-rejected clarity) ---------
# The badge is the strongest visible result signal. Before this increment the
# template mapped ALL WARN outcomes to one badge ("More detail needed"),
# collapsing two materially different states: an ACCEPTED first REASONED answer
# that moved its gap to PARTIAL, and an ASSERTED answer that was not accepted
# as sufficient. The mapping below distinguishes them using only the
# already-computed transition and the same stable, replay-locked reason
# substrings this module (and web/scaffolding_guidance.py) already pin. It is
# pure, display-only presentation selection: no engine value, transition,
# reason, gap status, maturity, direction, or transcript entry is read back,
# recomputed, or mutated.
_BADGE_PASS = {"css_class": "badge-pass", "label": "Good progress"}
_BADGE_ACCEPTED_PARTIAL = {"css_class": "badge-accepted", "label": "Accepted — one more step"}
_BADGE_WARN_ASSERTED = {"css_class": "badge-warn", "label": "More explanation needed"}
_BADGE_WARN_OTHER = {"css_class": "badge-warn", "label": "More detail needed"}
_BADGE_BLOCK = {"css_class": "badge-block", "label": "Not enough to continue"}


def get_result_badge(last_result):
    """Return the badge presentation ``{css_class, label}`` for a result, or None.

    Pure and deterministic. Reads only ``transition`` and the raw ``reason`` of
    the already-computed result dict; never mutates them, never re-scores.
    Returns a fresh dict per call so callers cannot alter the pinned constants.
    ``None`` (no result / unrecognized transition) lets the template fall back
    to the neutral "Response recorded" badge, preserving prior behavior.

    WARN sub-classification (same stable substrings as get_result_feedback):
      * "asserted only"        -> not accepted as sufficient ("More explanation needed")
      * "partially addressed"  -> accepted first REASONED answer, gap now PARTIAL
                                  ("Accepted — one more step")
      * anything else          -> the prior generic WARN badge ("More detail needed")
    """
    if not isinstance(last_result, dict):
        return None
    transition = last_result.get("transition")
    reason = last_result.get("reason") or ""

    if transition == "PASS":
        return dict(_BADGE_PASS)
    if transition == "WARN":
        if "asserted only" in reason:
            return dict(_BADGE_WARN_ASSERTED)
        if "partially addressed" in reason:
            return dict(_BADGE_ACCEPTED_PARTIAL)
        return dict(_BADGE_WARN_OTHER)
    if transition == "BLOCK":
        return dict(_BADGE_BLOCK)
    return None
