"""Gap-relevance eligibility — PVCG-R2-I.

File path      : engine/gap_relevance.py
Purpose        : decide, deterministically, whether a response addresses the
                 SPECIFIC gap that was served, so that an answer which does not
                 address the served gap cannot influence that gap's
                 satisfaction. Implements the product truth frozen by
                 docs/governance/PVCG_R2_C_GAP_RELEVANCE_HARDENING_CONTRACT.md
                 §4 (AUTHORITATIVE, PR #548, merge 4d746d15…).
Input contract : ``addresses_gap(response, gap_type)`` — ``response`` is the raw
                 inventor answer, ``gap_type`` is one of the six governed gap
                 type strings in ``GOVERNED_GAP_TYPES``.
Output contract: ``True`` when the response carries at least one intent marker
                 of the served gap's governed question family; ``False``
                 otherwise. ``False`` is also returned, fail-closed, for an
                 unrecognised gap type or a non-string response.
Prohibited     : any state mutation, I/O, clock read, randomness, network call,
                 model call, per-sentence special-casing, or dependency on any
                 module other than the standard-library ``re``.

WHAT THIS IS, STATED TRUTHFULLY
-------------------------------
This is a LEXICAL, deterministic marker test over the vocabulary of the six
governed questions in ``engine.progression_loop.QUESTIONS``. It is NOT a
semantic component. It does not interpret an answer, it does not stabilise
paraphrase, and it does not carry across languages — an answer written in
another language, or one that expresses the same intent using none of the
governed vocabulary, is treated as NOT eligible. That is the fail-closed
direction the contract requires (`uncertain relevance != satisfied`), and it is
a KNOWN BOUND of R2, not a defect to be hidden. Stabilising equivalent wording
is PVCG-R3 and is explicitly NOT authorised here.

Eligibility is NOT quality. A response that is eligible still has to satisfy the
existing quality rules in ``assess_response`` before it can advance a gap; a
response that is not eligible keeps its assessed quality, is still recorded, and
is never converted into BLOCK, a contradiction, or an input-validation failure.
"""

import re

from engine.idea_state import (
    MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY,
    PROBLEM_MECHANISM_FIT, ASSUMPTION_INVENTORY, EXPERTISE_GAP_AWARENESS,
)

# Whole-word intent markers per governed gap type.
#
# Each family is derived from the vocabulary of that gap's own governed
# questions (engine.progression_loop.QUESTIONS). Deliberately EXCLUDED from
# every family: bare domain vocabulary (sensor, relay, capacitor, resistor,
# voltage, current, microcontroller …) and bare causal connectives (because,
# therefore, since, thus). Those are exactly the signals PVCG-R2-C §4 declares
# insufficient on their own, so admitting them would re-create the defect.
_INTENT_WORDS = {
    # "Describe specifically HOW your invention works … the physical or
    # functional steps it takes"; "the individual components or actions inside
    # your mechanism".
    MECHANISM_COMPLETENESS: frozenset({
        "step", "steps", "stage", "stages", "sequence", "process", "procedure",
        "component", "components", "module", "modules", "subsystem",
        "subsystems", "part", "parts",
        "actuates", "actuate", "triggers", "trigger", "activates", "activate",
        "switches", "switch", "opens", "open", "closes", "close",
        "converts", "convert", "drives", "drive", "transmits", "transmit",
        "receives", "receive", "sends", "send", "measures", "measure",
        "detects", "detect", "senses", "sense", "compares", "compare",
        "computes", "compute", "disconnects", "disconnect",
        "connects", "connect", "rotates", "rotate", "moves", "move",
        "amplifies", "amplify", "filters", "latches", "latch",
    }),
    # "What physical principle does your mechanism rely on?"; "power
    # requirement and source"; "physical limits or constraints (temperature
    # range, signal frequency, material properties)".
    PHYSICAL_FEASIBILITY: frozenset({
        "principle", "principles", "physics",
        "energy", "consumes", "consume", "consumption", "draws", "draw",
        "battery", "batteries", "supply",
        "watt", "watts", "milliwatt", "milliwatts", "milliamp", "milliamps",
        "amp", "amps", "ampere", "amperes", "joule", "joules",
        "temperature", "thermal", "heat", "frequency", "hz", "khz", "mhz",
        "material", "materials", "tolerance", "tolerances",
        "constraint", "constraints", "efficiency", "withstand",
        "rated", "rating", "capacity", "feasible", "feasibility",
        "resistive", "inductive", "capacitive", "optical", "magnetic",
    }),
    # "What does your invention specifically NOT do or NOT cover?"; "one
    # existing approach that is similar … what makes yours different"; "the
    # core that cannot be replaced".
    BOUNDARY_AMBIGUITY: frozenset({
        "boundary", "boundaries", "scope",
        "exclude", "excludes", "excluded", "excluding",
        "unlike", "differs", "differ", "different", "difference", "differences",
        "distinct", "distinguishes",
        "alternative", "alternatives", "existing", "competitor", "competitors",
        "prior", "replace", "replaced", "replacing", "replaceable",
        "irreplaceable", "core", "essential",
        "versus", "vs", "compared", "comparison", "whereas",
        "outside", "beyond", "limitation", "limitations",
        "restricted", "restricts", "uncovered",
    }),
    # "describe the problem you are trying to solve … why does it matter to
    # them"; "why does your mechanism solve this problem rather than a
    # different approach"; "situations or conditions where it would not solve".
    PROBLEM_MECHANISM_FIT: frozenset({
        "problem", "problems", "issue", "issues",
        "user", "users", "person", "people", "customer", "customers",
        "matters", "pain", "suffer", "suffers", "struggle", "struggles",
        "solves", "solve", "solved", "solving", "addresses",
        "suited", "suitable",
        "situation", "situations", "condition", "conditions",
        "scenario", "scenarios", "unsuitable",
    }),
    # "What are you taking for granted … that you have not yet tested or
    # verified"; "things you expect to be true"; "which assumptions are
    # essential".
    ASSUMPTION_INVENTORY: frozenset({
        "assume", "assumes", "assumed", "assuming",
        "assumption", "assumptions",
        "presume", "presumes", "presumed",
        "unverified", "untested", "unproven", "unconfirmed",
        "hypothesis", "hypotheses",
        "expect", "expects", "expected", "granted",
        "believe", "believed",
    }),
    # "What areas of technical knowledge would someone need"; "domains of
    # expertise required"; "genuine gaps where you would need to learn more or
    # bring in someone else".
    EXPERTISE_GAP_AWARENESS: frozenset({
        "expertise", "expert", "experts", "knowledge",
        "skill", "skills", "discipline", "disciplines",
        "specialist", "specialists", "engineer", "engineers", "engineering",
        "training", "trained", "learn", "learning",
        "familiar", "unfamiliar", "experience", "experienced", "background",
        "consult", "consultant", "hire", "mentor",
        "professional", "qualified", "competence", "competency",
    }),
}

# Multi-word intent markers. Matched as plain substrings on the lowered
# response because they are phrases, not tokens.
_INTENT_PHRASES = {
    MECHANISM_COMPLETENESS: (
        "how it works", "works by", "in order to", "step by step",
    ),
    PHYSICAL_FEASIBILITY: (
        "power requirement", "power requirements", "power consumption",
        "power source", "temperature range", "operating range",
        "physical limit", "physical limits", "operating limit",
    ),
    BOUNDARY_AMBIGUITY: (
        "does not", "doesn't", "not cover", "not intended",
        "as opposed to", "cannot be replaced",
    ),
    PROBLEM_MECHANISM_FIT: (
        "rather than", "instead of", "right fit", "less well",
        "would not solve",
    ),
    ASSUMPTION_INVENTORY: (
        "take for granted", "taking for granted", "taken for granted",
        "turned out to be wrong",
    ),
    EXPERTISE_GAP_AWARENESS: (
        "bring in", "need help", "would need to learn",
        "do not know how", "don't know how", "someone else",
    ),
}

#: The six governed gap types this module can adjudicate. Anything else is
#: fail-closed — a gap type with no governed intent family is never eligible.
GOVERNED_GAP_TYPES = tuple(sorted(_INTENT_WORDS))

_WORD_RE = re.compile(r"[a-z0-9]+")


def addresses_gap(response, gap_type):
    """Return True when ``response`` carries the served gap's intent vocabulary.

    Pure and deterministic: the result depends only on the two arguments. No
    state is read or written, nothing is logged, and nothing external is
    consulted. Fail-closed on every uncertain input.
    """
    if not isinstance(response, str):
        return False
    if gap_type not in _INTENT_WORDS:
        return False
    lowered = response.lower()
    for phrase in _INTENT_PHRASES.get(gap_type, ()):
        if phrase in lowered:
            return True
    return not _INTENT_WORDS[gap_type].isdisjoint(_WORD_RE.findall(lowered))
