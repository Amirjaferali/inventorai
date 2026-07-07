"""More Detail Needed / Guided Answer Scaffolding — deterministic display-only guidance.

Governed by
`docs/governance/MORE_DETAIL_NEEDED_GUIDED_SCAFFOLDING_INCREMENT_CONTRACT.md`
(true-merged via PR #106). This module derives, at render time, bounded neutral
guidance that names the KIND of missing detail an inventor should add when the
deterministic engine has ALREADY returned a WARN-class insufficiency for the
current answer.

Strict boundaries (contract §7 / §8 / §10):
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

Factual attribution (confirmed from code; corrects the two non-blocking PR #104
§11 items, per the Increment Contract §3.1): the WARN `reason` strings this
module classifies on are produced by `engine.progression_loop.integrate_response`
(NOT `evaluate_transition`), and the session-view "Direction:" text is
`state.direction` surfaced via `engine.progression_loop` on the web layer's
`last_result` (NOT `engine/summary.py`). This module recomputes none of them; it
only selects display wording from the already-computed WARN outcome.
"""

# Bounded, neutral, category-level prompts (contract §9). Each asks WHAT KIND of
# detail is missing; none proposes or supplies the answer text.
_CATEGORY_PROMPTS = (
    "What physical part or mechanism does this use?",
    "What condition triggers the action?",
    "What does the device sense or detect?",
    "What output or response happens?",
    "What evidence or observation supports this?",
)

# Deterministic lead lines keyed on the KIND of WARN insufficiency the engine
# already reported, matched on stable substrings of the WARN `reason` string. No
# scoring is recomputed here; classification only selects display wording.
_LEAD_ASSERTED = (
    "Your answer says what happens, but not how or why it works. Add the missing "
    "mechanism or reasoning — describe what makes it work."
)
_LEAD_PARTIAL = (
    "You have started explaining this. Add more specific detail about the "
    "mechanism, the trigger condition, or the operating boundary."
)
_LEAD_INTAKE = (
    "The idea is not fully described yet. Say what problem it solves and, in "
    "plain words, how it solves it."
)
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
    lowered = (last_result.get("reason") or "").lower()
    if "not yet established" in lowered:
        lead = _LEAD_INTAKE
    elif "reasoning required" in lowered:
        lead = _LEAD_ASSERTED
    elif "needs more depth" in lowered:
        lead = _LEAD_PARTIAL
    else:
        lead = _LEAD_GENERIC
    return {
        "heading": _HEADING,
        "lead": lead,
        "prompts": list(_CATEGORY_PROMPTS),
        "note": _NOTE,
    }
