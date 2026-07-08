"""More Detail Needed / Guided Answer Scaffolding — deterministic display-only guidance.

Originally governed by
`docs/governance/MORE_DETAIL_NEEDED_GUIDED_SCAFFOLDING_INCREMENT_CONTRACT.md`
(true-merged via PR #106); the Layer-1 feedback-wording / gap-type-aware
refinement below is governed by
`docs/governance/LAYER1_FEEDBACK_WORDING_GAP_TYPE_GUIDANCE_INCREMENT_CONTRACT.md`
(true-merged via PR #115). This module derives, at render time, bounded neutral
guidance that names the KIND of missing detail an inventor should add when the
deterministic engine has ALREADY returned a WARN-class insufficiency for the
current answer.

Strict boundaries (unchanged from the original contract; reaffirmed by the
Layer-1 contract §4/§5/§6):
- Pure, deterministic, display-only. No engine call, no AI/generative call, no
  network, no persistence, no stored state, no hidden state.
- Reads only the already-computed `last_result` (the WARN outcome) and the
  current `gap_type`. It never reads back, stores, rewrites, improves, corrects,
  completes, or mutates the inventor's answer; never closes a gap; never advances
  maturity; never satisfies a transition gate; never creates an Evidence record;
  and never alters the PASS/WARN/BLOCK outcome it accompanies.
- Names missing detail CATEGORIES and asks bounded, neutral, content-free
  questions only. It never suggests answer content and never claims validation,
  safety, feasibility, compliance, buildability, patentability, or readiness.
- This is NOT the Inventor Answer Clarification / Improve Wording Assistant: it
  introduces no `suggested_clarified_answer` / `user_approved_answer` /
  `original_user_answer` / `clarification_status` field or flow, and no
  equivalent.

Layer-1 refinement (PR #115 contract §4): the displayed wording now distinguishes
three honest cases using ONLY the already-computed outcome — (a) a first
accepted / REASONED answer whose gap is `PARTIAL` (accepted; one more specific
answer is needed before the gap can close — never a quality judgment), (b) an
asserted-only answer (reasoning is needed), and (c) a boundary / feasibility /
limitation answer (limits, conditions, assumptions, constraints, or evidence are
needed) — and the category prompts are gap-type-aware. Engine reason strings
(`engine.progression_loop.integrate_response`) are unchanged; this module only
selects display wording from the already-computed WARN outcome and the available
`gap_type`.
"""

# --- Gap-type families (Layer-1 contract §4) -------------------------------
# The engine's three Stage-2 gap types (engine/idea_state.py) map to guidance
# families. Unknown / absent gap types fall back to the MECHANISM prompt set,
# preserving the original PR #108 display behavior.
_MECHANISM = "mechanism"
_BOUNDARY = "boundary"
_FEASIBILITY = "feasibility"

# Bounded, neutral, category-level prompts per family. Each asks WHAT KIND of
# detail is missing; none proposes or supplies the answer text, a component, a
# number, a validation/readiness claim, or final answer wording.
_MECHANISM_PROMPTS = (
    "What physical part or mechanism does this use?",
    "What condition triggers the action?",
    "What does the device sense or detect?",
    "What output or response happens?",
    "What evidence or observation supports this?",
)
_BOUNDARY_PROMPTS = (
    "What is in scope, and what does this deliberately NOT do?",
    "Where are the limits or boundaries of where it applies?",
    "What operating conditions or assumptions does it depend on?",
    "What edge cases or exceptions are handled?",
    "What evidence or observation supports these limits?",
)
_FEASIBILITY_PROMPTS = (
    "What physical limits or operating range does this work within?",
    "What conditions or constraints must hold for it to work?",
    "What assumptions about the environment does it rely on?",
    "What could physically prevent it from working?",
    "What evidence or observation supports that it can work?",
)
_PROMPTS_BY_FAMILY = {
    _MECHANISM: _MECHANISM_PROMPTS,
    _BOUNDARY: _BOUNDARY_PROMPTS,
    _FEASIBILITY: _FEASIBILITY_PROMPTS,
}
# Default prompt set for a generic / unknown gap (preserves PR #108 behavior).
_DEFAULT_PROMPTS = _MECHANISM_PROMPTS

# --- Deterministic lead lines ----------------------------------------------
# Keyed on (case, family). `case` is the KIND of WARN insufficiency the engine
# already reported, matched on stable substrings of the WARN `reason` string.
# No scoring is recomputed here; classification only selects display wording.

# Case (b): asserted-only — the answer states what happens but not how/why.
_ASSERTED_BY_FAMILY = {
    _MECHANISM: (
        "Your answer says what happens, but not how or why it works. Add the "
        "missing mechanism or reasoning — describe what makes it work."
    ),
    _BOUNDARY: (
        "Your answer names a limit or scope, but not the reasoning behind it. "
        "Explain why that boundary holds — the conditions or assumptions that "
        "set it."
    ),
    _FEASIBILITY: (
        "Your answer states that it works, but not the reasoning. Explain the "
        "conditions, limits, or constraints that make it work."
    ),
}
_ASSERTED_GENERIC = (
    "Your answer says what happens, but not how or why it works. Add the missing "
    "mechanism or reasoning — describe what makes it work."
)

# Case (a): first accepted / REASONED answer whose gap is PARTIAL. Honest
# wording — the answer was accepted and is NOT treated as weak; the deterministic
# gate simply needs one more specific answer on the same point before the gap can
# close. The wording keeps the truthful WARN state visible (the gap is not yet
# closed) without implying poor quality.
_PARTIAL_BY_FAMILY = {
    _MECHANISM: (
        "Good — this answer was accepted and counts toward this point. The system "
        "needs one more specific answer about how it works before it can close, "
        "so add one more concrete detail — a part, a trigger condition, or what "
        "it senses."
    ),
    _BOUNDARY: (
        "Good — this answer was accepted and counts toward this point. The system "
        "needs one more specific answer about scope or limits before it can "
        "close, so add one more concrete detail — what it does not do, or a "
        "condition where it stops applying."
    ),
    _FEASIBILITY: (
        "Good — this answer was accepted and counts toward this point. The system "
        "needs one more specific answer about the physical limits or conditions "
        "before it can close, so add one more concrete detail — a constraint or "
        "operating range."
    ),
}
_PARTIAL_GENERIC = (
    "Good — this answer was accepted and counts toward this point. The system "
    "needs one more specific answer on the same point before it can close, so add "
    "one more concrete detail."
)

# Case: intake — the idea itself is not yet described.
_LEAD_INTAKE = (
    "The idea is not fully described yet. Say what problem it solves and, in "
    "plain words, how it solves it."
)
# Fallback for any other WARN reason.
_LEAD_GENERIC = (
    "This answer needs more detail. Add a specific point about the mechanism, the "
    "trigger condition, the operating boundary, or a supporting observation."
)

_HEADING = "What kind of detail to add"

# Neutral, display-only reminder that the guidance is not answer content and does
# not grade or change the answer.
_NOTE = (
    "These are prompts to help you add detail. They do not change or grade your "
    "answer — you write it in your own words."
)


def _gap_family(gap_type, reason_blob):
    """Classify the guidance family from the gap id (or the reason token).

    Display-context only. The engine reason string is prefixed with the gap-type
    token, so the family is recoverable even when `gap_type` is not passed. An
    unknown / absent gap type yields ``None`` (generic → default prompts).
    """
    blob = ((gap_type or "") + " " + (reason_blob or "")).upper()
    if "MECHANISM_COMPLETENESS" in blob:
        return _MECHANISM
    if "BOUNDARY_AMBIGUITY" in blob:
        return _BOUNDARY
    if "PHYSICAL_FEASIBILITY" in blob:
        return _FEASIBILITY
    return None


def get_scaffolding_guidance(last_result, gap_type=None):
    """Return bounded display-only guidance for a WARN-class insufficiency, else None.

    Pure and deterministic. `last_result` is the already-computed engine result
    dict (or None); `gap_type` is the current gap id (or None), accepted as display
    context only and never used to recompute any outcome. Returns a small dict
    ``{heading, lead, prompts, note}`` for WARN outcomes, or ``None`` for every
    other outcome (PASS / BLOCK / no result). Never mutates its inputs; never
    touches the answer, the gap lifecycle, maturity, or the PASS/WARN/BLOCK
    outcome.
    """
    if not isinstance(last_result, dict):
        return None
    if last_result.get("transition") != "WARN":
        return None
    reason = last_result.get("reason") or ""
    lowered = reason.lower()
    family = _gap_family(gap_type, reason)

    if "not yet established" in lowered:
        lead = _LEAD_INTAKE
    elif "reasoning required" in lowered:
        # Case (b): asserted-only — reasoning needed.
        lead = _ASSERTED_BY_FAMILY.get(family, _ASSERTED_GENERIC)
    elif "needs more depth" in lowered:
        # Case (a): first accepted/REASONED answer — honest "one more answer" wording.
        lead = _PARTIAL_BY_FAMILY.get(family, _PARTIAL_GENERIC)
    else:
        lead = _LEAD_GENERIC

    prompts = _PROMPTS_BY_FAMILY.get(family, _DEFAULT_PROMPTS)
    return {
        "heading": _HEADING,
        "lead": lead,
        "prompts": list(prompts),
        "note": _NOTE,
    }
