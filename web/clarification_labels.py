"""
Increment 1B — clarification display (deterministic, owner-invoked, display-only).

DETERMINISTIC EPHEMERAL SYSTEM GUIDANCE — WEB/DISPLAY-LAYER ONLY.

This module maps a committed `gap_type` to a short, plain-language explanation of
the CURRENT question so a non-specialist owner can choose to understand it before
answering, deferring, or marking it unknown. It is purely a display aid:

  * it is computed at render time from the current gap_type (no IdeaState field,
    no transcript field, no interaction metadata, no durable persistence);
  * it explains ONLY the existing single question — it never asks another
    question, splits the question, generates a follow-up, or creates a new
    iteration;
  * it does NOT answer the invention question, invent project-specific facts,
    convert uncertainty into certainty, imply a specialist was consulted or that
    evidence already exists, force escalation, close a gap, change scoring,
    maturity, gates, the transcript, or the deliverable, or auto-select/replace
    any Increment 1A owner action;
  * it imports no engine state, performs no I/O, touches no session or
    persistence, and calls no LLM or external service.

The clarification content is system guidance — NOT user evidence, NOT an owner
answer, NOT system analysis of the idea. Unknown or missing gap types resolve
safely to a generic clarification; this never raises and never mutates anything.
"""

# Per-gap-type clarification content (owner-approved, deterministic). Visible text
# uses plain language only and contains no internal gap-type identifiers. Each
# entry explains the existing question; none introduces a new question.
_CLARIFICATION = {
    "MECHANISM_COMPLETENESS": {
        "label": "What this question is asking",
        "plain_language": (
            "This is asking you to walk through how your idea works from start "
            "to finish — what happens first, what happens next, and how those "
            "steps lead to the result you want."
        ),
        "information_needed": (
            "A step-by-step description, in your own words, of how the idea turns "
            "its starting point into the outcome."
        ),
        "answer_shape": (
            "A few plain sentences describing the sequence of steps. Everyday "
            "language is fine; exact technical figures are not required."
        ),
        "support_hint": (
            "If part of the chain is still unclear, you can describe the parts "
            "you know and mark the rest as not yet known."
        ),
    },
    "BOUNDARY_AMBIGUITY": {
        "label": "What this question is asking",
        "plain_language": (
            "This is asking you to describe the edges of your idea — what it is "
            "meant to cover, and what it deliberately leaves out."
        ),
        "information_needed": (
            "What problem it handles, who it is for, and where it stops or does "
            "not apply."
        ),
        "answer_shape": (
            "A short description of what is inside and outside the idea's scope. "
            "No legal or patent wording is needed."
        ),
        "support_hint": (
            "If a boundary is still undecided, you can say so rather than "
            "guessing."
        ),
    },
    "ASSUMPTION_INVENTORY": {
        "label": "What this question is asking",
        "plain_language": (
            "This is asking which things you are currently taking for granted "
            "about your idea that you have not yet checked."
        ),
        "information_needed": (
            "Conditions, materials, or behaviors you expect to hold true but "
            "have not confirmed."
        ),
        "answer_shape": (
            "A short list of things you are assuming, in plain words, and which "
            "ones would matter most if they turned out to be wrong."
        ),
        "support_hint": (
            "Listing an assumption does not commit you to it; it just records "
            "what still needs checking."
        ),
    },
    "PROBLEM_MECHANISM_FIT": {
        "label": "What this question is asking",
        "plain_language": (
            "This is asking you to describe the problem on its own, and then how "
            "your idea is meant to address it."
        ),
        "information_needed": (
            "Who has the problem and why it matters, described separately from "
            "how your idea works, plus where the match might be weaker."
        ),
        "answer_shape": (
            "First describe the problem in plain language, then describe how you "
            "intend the idea to help. It is fine to leave the strength of that "
            "relationship as uncertain."
        ),
        "support_hint": (
            "You only need to describe the problem and your intent; you do not "
            "need to prove the fit yourself."
        ),
    },
    "PHYSICAL_FEASIBILITY": {
        "label": "What this question is asking",
        "plain_language": (
            "This is asking what makes your idea actually work — the basic "
            "principle, components, or process behind it."
        ),
        "information_needed": (
            "The working principle in plain terms. Whether it truly holds may "
            "later need a measurement, test, or outside evidence."
        ),
        "answer_shape": (
            "A plain description of the principle you expect to make it work. "
            "Exact measurements are not required here."
        ),
        "support_hint": (
            "If confirming it would need a test or evidence you do not have, you "
            "can note that and continue."
        ),
    },
    "EXPERTISE_GAP_AWARENESS": {
        "label": "What this question is asking",
        "plain_language": (
            "This is asking which areas of know-how someone would need to "
            "actually build your idea — not what you personally know."
        ),
        "information_needed": (
            "The kinds of technical fields or skills the build would demand."
        ),
        "answer_shape": (
            "A short list of the areas of expertise involved. You do not need to "
            "have that expertise yourself."
        ),
        "support_hint": (
            "If a particular area clearly needs a specialist, you can note that "
            "and request specialist input rather than answering it."
        ),
    },
}

# Safe generic fallback for unknown / missing gap types. Truthful and neutral;
# never claims certainty and never invents a question.
_FALLBACK = {
    "label": "What this question is asking",
    "plain_language": (
        "This is asking you to describe this part of your idea in your own "
        "words."
    ),
    "information_needed": (
        "Whatever you currently know about this part of the idea."
    ),
    "answer_shape": (
        "A few plain sentences. It is fine to describe only what you know and "
        "mark the rest as not yet known."
    ),
    "support_hint": (
        "You can answer with what you know or choose any of the available "
        "actions that truthfully reflects what you need next."
    ),
}


def get_clarification(gap_type):
    """Return deterministic clarification display content for a gap_type.

    Returns a FRESH dict {label, plain_language, information_needed,
    answer_shape, support_hint}. Unknown or None gap types resolve to a safe
    generic fallback. Never raises; never mutates anything; performs no I/O.
    """
    content = _CLARIFICATION.get(gap_type, _FALLBACK)
    return {
        "label": content["label"],
        "plain_language": content["plain_language"],
        "information_needed": content["information_needed"],
        "answer_shape": content["answer_shape"],
        "support_hint": content["support_hint"],
    }
