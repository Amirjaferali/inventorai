"""Guided Answer Co-Authoring Increment 1 — Advisory Prompt Support.

DETERMINISTIC, DISPLAY-ONLY, CONTENT-FREE ADVISORY PROMPTS — WEB/DISPLAY LAYER.

Governed by
`docs/governance/GUIDED_ANSWER_COAUTHORING_INCREMENT_CONTRACT.md`
(true-merged via PR #127) and its scope decision
`docs/governance/GUIDED_ANSWER_COAUTHORING_SCOPE_DECISION.md` (PR #125).

This module maps a committed `gap_type` to a short, bounded, CATEGORY-LEVEL set
of "what kind of information would strengthen your own answer" prompts, so a
non-specialist inventor can decide what specifics to add when writing their OWN
answer to the current question. It helps the inventor DEVELOP THEIR IDEA; it does
not author, rewrite, complete, grade, or replace the answer.

Strict boundaries (contract §6/§7/§10; scope decision §6/§7/§12):
  * Pure, deterministic, display-only. Computed at render time from the current
    `gap_type` alone. No engine call, no AI/generative/LLM call, no network, no
    I/O, no persistence, no stored state, no hidden state.
  * It NEVER reads, stores, rewrites, improves, corrects, completes, or mutates
    the inventor's answer; never closes a gap; never advances maturity or
    readiness; never satisfies a transition gate; never creates an Evidence
    record; never changes scoring; and never alters any PASS/WARN/BLOCK outcome.
  * It emits only bounded, neutral, CATEGORY-LEVEL prompts about what KIND of
    detail to consider. It NEVER supplies answer content, a component, a number,
    or final answer wording, and never claims the answer is correct, complete,
    validated, safe, compliant, patent-ready, or engineering-ready.
  * This is NOT the Inventor Answer Clarification / Improve Wording Assistant: it
    introduces no `suggested_clarified_answer` / `user_approved_answer` /
    `original_user_answer` / `clarification_status` field or flow, and no
    equivalent; it adds no save/approve/apply action and no new session action.
  * The inventor remains the sole author and source of any saved answer.

Distinct from the two existing display-only surfaces:
  * `web/clarification_labels.py` (Increment 1B) EXPLAINS what the current
    question is asking.
  * `web/scaffolding_guidance.py` (More Detail Needed) names the KIND of missing
    detail AFTER the engine has already returned a WARN insufficiency.
  * This module offers OPTIONAL, forward-looking "what to include" categories to
    help the inventor build their own answer, available for the current question.
"""

# Advisory heading and the mandatory optional/authorship reminder shown with
# every set of prompts. The note reaffirms that prompts are optional, that the
# inventor writes their own answer, and that guidance is not validation or
# safety/compliance/patent/engineering approval (contract §10).
_HEADING = "Optional: what you could include in your answer"

_NOTE = (
    "These prompts are optional. You write your own answer in your own words — "
    "they are not a required format. This guidance is not validation, and it is "
    "not safety, compliance, patent, or engineering approval; it only helps you "
    "think through what details you might add."
)

# Per-gap-type, category-level prompts. Each names a KIND of information the
# inventor could add; none proposes or supplies answer content, a value, a
# component, or a validation/readiness claim. Mirrors the gap-type keys used by
# the existing display-only surfaces (web/clarification_labels.py).
_PROMPTS = {
    "MECHANISM_COMPLETENESS": (
        "The main parts or steps involved, in the order they happen.",
        "What starts the process, and what it produces at the end.",
        "What the idea senses, detects, or responds to, if anything.",
        "Anything you have observed that suggests it behaves this way.",
    ),
    "BOUNDARY_AMBIGUITY": (
        "What the idea is meant to cover, and what it deliberately does not do.",
        "Who or what it is for, and the situations where it applies.",
        "Conditions or limits where it would stop applying.",
        "Any point where you are still deciding the boundary.",
    ),
    "ASSUMPTION_INVENTORY": (
        "Things you are currently taking for granted but have not checked.",
        "Which of those assumptions would matter most if they were wrong.",
        "Conditions, materials, or behaviors you expect to hold true.",
        "Anything you already know still needs checking.",
    ),
    "PROBLEM_MECHANISM_FIT": (
        "The problem on its own — who has it and why it matters.",
        "How you intend the idea to address that problem.",
        "Where the match between problem and idea might be weaker.",
        "Anything you have seen that suggests the idea helps.",
    ),
    "PHYSICAL_FEASIBILITY": (
        "The basic working principle you expect makes it work.",
        "The conditions or operating range it would need to work within.",
        "What could physically get in the way of it working.",
        "Any observation or test that speaks to whether it can work.",
    ),
    "EXPERTISE_GAP_AWARENESS": (
        "The kinds of technical skills or fields the build would involve.",
        "Which parts you could describe yourself, in plain words.",
        "Which parts clearly need a specialist's input.",
        "Anything you are unsure how to describe yet.",
    ),
}

# Safe, neutral fallback for unknown / missing gap types. Content-free and
# truthful; never invents a question and never claims certainty.
_FALLBACK = (
    "What you currently know about this part of the idea, in your own words.",
    "The parts you are confident about, and the parts still uncertain.",
    "Anything you have observed that is relevant.",
    "What you would still need to find out.",
)


def get_answer_coauthoring_prompts(gap_type):
    """Return optional, display-only, category-level co-authoring prompts.

    Pure and deterministic. `gap_type` is the current gap id (or None), used only
    to select which category-level prompt set to display. Returns a fresh dict
    ``{heading, prompts, note}`` where ``prompts`` is a list of content-free
    strings naming KINDS of detail the inventor could add to their own answer.
    Unknown or None gap types resolve to a safe generic fallback. Never raises;
    never performs I/O; never reads, stores, or mutates any answer or state; and
    never affects scoring, maturity, readiness, gaps, the transcript, or the
    IdeaState.
    """
    prompts = _PROMPTS.get(gap_type, _FALLBACK)
    return {
        "heading": _HEADING,
        "prompts": list(prompts),
        "note": _NOTE,
    }
