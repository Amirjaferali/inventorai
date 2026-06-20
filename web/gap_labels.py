# gap_labels.py
# Translation layer: internal gap type constants -> inventor-facing guidance.
# Drop into web/ directory. No engine changes required.

GAP_LABELS = {
    "PHYSICAL_FEASIBILITY": {
        "heading": "Does your idea have a clear working principle?",
        "guidance": (
            "Describe what makes your idea work — the components, materials, "
            "forces, or processes involved. Be as specific as you can about "
            "the mechanism, not just the goal."
        ),
        "stage_note": "Exploring feasibility",
    },
    "BOUNDARY_AMBIGUITY": {
        "heading": "What does your idea do — and what doesn't it do?",
        "guidance": (
            "Define the scope clearly: what problem it solves, who it's for, "
            "and where it stops. Clear boundaries help identify what is truly "
            "novel and what still needs development."
        ),
        "stage_note": "Defining scope",
    },
    "MECHANISM_COMPLETENESS": {
        "heading": "How does it work, step by step?",
        "guidance": (
            "Walk through the operating mechanism — the causal chain from "
            "input to output. What happens at each stage? What converts, "
            "controls, or transforms the inputs into the desired result?"
        ),
        "stage_note": "Developing mechanism",
    },
    "PROBLEM_MECHANISM_FIT": {
        "heading": "How does your idea address the problem?",
        "guidance": (
            "Describe the problem on its own terms first — who experiences it "
            "and why it matters — without describing your idea. Then explain how "
            "your idea is intended to address that problem, and identify situations "
            "where the match may be weaker."
        ),
        "stage_note": "Checking problem fit",
    },
    "ASSUMPTION_INVENTORY": {
        "heading": "What are you assuming that hasn't been tested yet?",
        "guidance": (
            "List anything you are taking for granted about your idea that you "
            "have not yet verified — materials, conditions, or behaviors you "
            "expect to hold true. Then note which of these would be most "
            "serious if they turned out to be wrong."
        ),
        "stage_note": "Surfacing assumptions",
    },
    "EXPERTISE_GAP_AWARENESS": {
        "heading": "What expertise would building this require?",
        "guidance": (
            "List the areas of technical knowledge someone would need to build "
            "your idea — not what you personally know, but what the implementation "
            "itself demands. Then identify which areas require specialist input."
        ),
        "stage_note": "Identifying expertise needs",
    },
    "__default__": {
        "heading": "Tell us more about this aspect of your idea",
        "guidance": (
            "Provide as much specific detail as you can. "
            "Concrete descriptions help more than general ones."
        ),
        "stage_note": "Exploring",
    },
}

MATURITY_LABELS = {
    0: {
        "label": "Getting started",
        "meaning": "Share your idea — what it does and the problem it addresses.",
    },
    1: {
        "label": "Problem established",
        "meaning": (
            "You have described the core problem and your idea's direction. "
            "Now let's develop the mechanism."
        ),
    },
    2: {
        "label": "Ready for structured review",
        "meaning": (
            "You have worked through the key questions. This is a good point "
            "to seek technical feedback from domain experts."
        ),
    },
}

SESSION_DISCLOSURE = (
    "This platform helps you structure your thinking through guided questions. "
    "It tracks how you have addressed key areas — external technical validation "
    "remains a separate step."
)


def get_gap_label(gap_type: str) -> dict:
    return GAP_LABELS.get(gap_type, GAP_LABELS["__default__"])


def get_maturity_label(level: int) -> dict:
    return MATURITY_LABELS.get(level, MATURITY_LABELS[0])
