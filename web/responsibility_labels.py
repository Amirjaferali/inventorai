"""
Increment 1B — responsibility guidance (Option E: label + one guidance sentence).

ADVISORY, DERIVED, PER-GAP-TYPE, WEB-DISPLAY-LAYER ONLY.

This module maps a committed `gap_type` to a short, plain-language responsibility
LABEL and ONE guidance sentence, so a non-specialist owner can see — near the
current question — whether they are reasonably expected to answer it, or whether
a specialist or a test/evidence is the likely source. It is purely advisory:

  * it is computed at render time from the current gap_type (no IdeaState field,
    no transcript field, no durable persistence, no schema_version);
  * it does NOT rewrite the question, add a user action, auto-select or constrain
    any Increment 1A action, cause assessment, or affect scoring, maturity, gap
    closure, gates, transcript, or the deliverable;
  * it never claims that a specialist has already answered or that evidence
    already exists — it only states who would typically answer and that the owner
    may request specialist input / evidence and continue.

Responsibility vocabulary (owner-approved, exactly five values; distinct from the
Increment 1A interaction dispositions, which are the user's *chosen* actions):
OWNER_INPUT, SYSTEM_ANALYSIS, SPECIALIST_INPUT, EMPIRICAL_EVIDENCE, UNDETERMINED.

Unknown or missing gap types resolve safely to UNDETERMINED; this never raises.
"""

# Approved responsibility values (advisory classification, not user actions).
OWNER_INPUT = "OWNER_INPUT"
SYSTEM_ANALYSIS = "SYSTEM_ANALYSIS"
SPECIALIST_INPUT = "SPECIALIST_INPUT"
EMPIRICAL_EVIDENCE = "EMPIRICAL_EVIDENCE"
UNDETERMINED = "UNDETERMINED"

# Per-responsibility short label + one concise guidance sentence (owner-approved
# intent). No sentence implies a specialist or evidence already exists.
_GUIDANCE = {
    OWNER_INPUT: {
        "label": "You can answer this",
        "guidance": ("You can answer this from your intended design or current "
                     "understanding. Exact engineering values are not required."),
    },
    SYSTEM_ANALYSIS: {
        "label": "The system can help with this",
        "guidance": ("The system can help examine this relationship. You may "
                     "still mark what is uncertain."),
    },
    SPECIALIST_INPUT: {
        "label": "Specialist input may help",
        "guidance": ("This usually needs input from a relevant technical "
                     "specialist. You can request specialist input and continue."),
    },
    EMPIRICAL_EVIDENCE: {
        "label": "Evidence or a test may be needed",
        "guidance": ("This usually needs a measurement, test, or external "
                     "evidence. You can request evidence and continue."),
    },
    UNDETERMINED: {
        "label": "Who answers this is not yet clear",
        "guidance": ("It is not yet clear who should answer this. You can "
                     "answer, defer, or mark it as unknown."),
    },
}

# Static per-gap-type advisory classification (owner-approved initial mapping).
# Gap-type identifiers are the committed constants in engine.idea_state.
_GAP_RESPONSIBILITY = {
    "MECHANISM_COMPLETENESS": OWNER_INPUT,
    "BOUNDARY_AMBIGUITY": OWNER_INPUT,
    "PROBLEM_MECHANISM_FIT": SYSTEM_ANALYSIS,
    "ASSUMPTION_INVENTORY": OWNER_INPUT,
    "PHYSICAL_FEASIBILITY": EMPIRICAL_EVIDENCE,
    "EXPERTISE_GAP_AWARENESS": SPECIALIST_INPUT,
}


def get_responsibility(gap_type):
    """Return advisory responsibility guidance for a gap_type.

    Returns a dict {responsibility, label, guidance}. Unknown or None gap types
    resolve to UNDETERMINED. Never raises; never mutates anything.
    """
    responsibility = _GAP_RESPONSIBILITY.get(gap_type, UNDETERMINED)
    text = _GUIDANCE[responsibility]
    return {
        "responsibility": responsibility,
        "label": text["label"],
        "guidance": text["guidance"],
    }
