"""
Progression Loop — MVP core logic.
Scope: electronics/electrical, LEVEL 0-2 only.
Governed by: MVP_SCOPE_FREEZE.md

Responsibilities:
  - Identify highest-priority open gap
  - Generate one question per iteration
  - Integrate response into IdeaState
  - Evaluate PASS / WARN / BLOCK
  - Detect stall and reframe

NOT responsible for:
  - Domain rule enforcement (domain_rules.py)
  - Scoring (engine/scoring.py)
  - Replay (scripts/)
"""

from engine.idea_state import (
    IdeaState, Evidence, Gap, IterationLog,
    PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY, MECHANISM_COMPLETENESS,
    OPEN, PARTIAL, CLOSED, ACCEPTED_RISK,
    ASSERTED, REASONED, DEMONSTRATED,
    PROGRESSING, STALLED, REGRESSING
)


# --- Gap priority order (per MVP_SCOPE_FREEZE) ---
GAP_PRIORITY = [
    MECHANISM_COMPLETENESS,
    PHYSICAL_FEASIBILITY,
    BOUNDARY_AMBIGUITY,
]

STALL_THRESHOLD = 3  # iterations before reframe


# ─────────────────────────────────────────────
# 1. Select next gap to address
# ─────────────────────────────────────────────

def select_next_gap(state: IdeaState) -> str | None:
    """
    Return the highest-priority OPEN gap_type.
    Returns None if no open gaps exist.
    """
    open_gaps = {g.gap_type: g for g in state.gaps if g.status == OPEN}
    for gap_type in GAP_PRIORITY:
        if gap_type in open_gaps:
            return gap_type
    return None


# ─────────────────────────────────────────────
# 2. Generate one question for a gap
# ─────────────────────────────────────────────

QUESTIONS = {
    MECHANISM_COMPLETENESS: [
        "Describe specifically HOW your invention works — "
        "not what it achieves, but the physical or functional steps it takes.",

        "What are the individual components or actions inside your mechanism? "
        "Name each one and what it does.",

        "If someone tried to build your invention tomorrow with no further explanation, "
        "what would be missing from your current description?",
    ],
    PHYSICAL_FEASIBILITY: [
        "What physical principle does your mechanism rely on? "
        "(e.g. resistive sensing, inductive coupling, optical detection)",

        "Does your invention consume or manage energy? "
        "If yes, what is the approximate power requirement and source?",

        "What are the physical limits or constraints your mechanism must operate within? "
        "(e.g. temperature range, signal frequency, material properties)",
    ],
    BOUNDARY_AMBIGUITY: [
        "What does your invention specifically NOT do or NOT cover? "
        "State at least one clear boundary.",

        "Name one existing approach that is similar to yours. "
        "What makes yours different in a specific, concrete way?",

        "If someone tried to copy your invention by changing only one component, "
        "would it still be your invention? What is the core that cannot be replaced?",
    ],
}


def get_question(domain: str, gap_type: str, iterations_open: int) -> str:
    """
    Select question for gap_type.
    Asks domain layer first; falls back to generic questions.
    Framework-level delegation — no domain-specific logic here.
    """
    from engine.domain_rules import get_domain_question
    domain_q = get_domain_question(domain, gap_type, iterations_open)
    if domain_q:
        return domain_q
    variants = QUESTIONS[gap_type]
    index = min(iterations_open, len(variants) - 1)
    return variants[index]


# ─────────────────────────────────────────────
# 3. Integrate response → update gap status
# ─────────────────────────────────────────────

# Weak-answer patterns that must not advance maturity
_WEAK_PATTERNS = {
    "i don't know", "i do not know", "not sure", "no idea",
    "i don't know", "unknown", "maybe", "n/a", "na",
    "i have no idea", "i'm not sure", "i am not sure",
    "something", "somehow", "i don't", "don't know",
}

# Substance signals: at least one required for REASONED
_SUBSTANCE_SIGNALS = [
    # components/devices
    "sensor", "microcontroller", "arduino", "esp", "raspberry",
    "motor", "pump", "relay", "led", "display", "battery",
    "chip", "ic", "resistor", "capacitor", "transistor",
    "bluetooth", "wifi", "ble", "mqtt", "uart", "i2c", "spi",
    # actions/signals
    "reads", "sends", "detects", "measures", "activates",
    "triggers", "converts", "transmits", "receives", "processes",
    "samples", "outputs", "controls", "monitors", "calculates",
    # principles
    "voltage", "current", "frequency", "analog", "digital",
    "signal", "threshold", "filter", "protocol", "data",
    "piezoelectric", "hall", "infrared", "ultrasonic", "capacitive",
]


def assess_response(response: str) -> str:
    """
    Quality assessment: weak-answer guard + substance check.
    MVP: pattern rejection + substance heuristic.
    Future: replace substance check with AI-advisory assessment.
    """
    r = response.strip()
    r_lower = r.lower()

    # 1. Reject explicit weak answers regardless of length
    if r_lower in _WEAK_PATTERNS:
        return ASSERTED  # stays ASSERTED — will not pass evaluate_transition

    # 2. Reject vague filler phrases (contains weak tokens, no substance)
    weak_tokens = {"somehow", "something", "technology", "stuff", "things"}
    substance_tokens = set(_SUBSTANCE_SIGNALS)
    words = set(r_lower.split())
    has_weak = bool(words & weak_tokens)
    has_substance = any(sig in r_lower for sig in _SUBSTANCE_SIGNALS)

    if has_weak and not has_substance:
        return ASSERTED  # vague filler — no technical substance

    # 3. Short but technically specific answers are valid (e.g. "Hall sensor")
    if has_substance:
        return REASONED

    # 4. Length fallback for borderline answers without clear substance signals
    if len(r) < 20:
        return ASSERTED
    # No substance signals detected — treat as ASSERTED regardless of length
    return ASSERTED  # DEMONSTRATED requires external evidence — not in MVP


def integrate_response(
    state: IdeaState,
    gap_type: str,
    question: str,
    response: str,
) -> tuple[str, str]:
    """
    Update IdeaState based on response.
    Returns (transition_result, reason).
    transition_result: PASS | WARN | BLOCK
    """
    quality = assess_response(response)
    evidence = Evidence(
        content=response,
        quality=quality,
        iteration=state.iteration,
    )

    # Update known elements
    if gap_type == MECHANISM_COMPLETENESS:
        if state.known_mechanism is None or quality >= state.known_mechanism.quality:
            state.known_mechanism = evidence

    # أي evidence في المراحل المبكرة تُثبت المشكلة ضمنياً
    if state.known_problem is None:
        state.known_problem = evidence

    # Update gap status
    gap = state.get_gap(gap_type)
    if gap is None:
        gap = Gap(gap_type=gap_type, status=OPEN, opened_at=state.iteration)
        state.gaps.append(gap)

    if quality == DEMONSTRATED:
        gap.status = CLOSED
        gap.closed_at = state.iteration
        return "PASS", f"{gap_type} closed with DEMONSTRATED evidence"

    elif quality == REASONED:
        if gap.status == PARTIAL:
            gap.status = CLOSED
            gap.closed_at = state.iteration
            return "PASS", f"{gap_type} closed after REASONED follow-up"
        else:
            gap.status = PARTIAL
            return "WARN", f"{gap_type} partially addressed — needs more depth"

    else:  # ASSERTED
        gap.status = PARTIAL
        return "WARN", f"{gap_type} asserted only — reasoning required"


# ─────────────────────────────────────────────
# 4. Evaluate maturity transition
# ─────────────────────────────────────────────

def evaluate_transition(state: IdeaState) -> tuple[bool, str]:
    """
    Check if state qualifies for maturity_level increment.
    Returns (can_transition, reason).
    Deterministic — no AI involvement.
    """
    level = state.maturity_level

    if level == 0:
        # 0 → 1: problem established with beneficiary signal
        if state.known_problem and state.known_problem.quality >= ASSERTED:
            mech_gap = state.get_gap(MECHANISM_COMPLETENESS)
            if mech_gap and mech_gap.status == OPEN and mech_gap.iterations_open == 0:
                return False, "MECHANISM_COMPLETENESS must be attempted first"
            return True, "Problem established — ready for LEVEL 1"
        return False, "Problem not yet established"

    if level == 1:
        # 1 → 2: mechanism established + no blocking gaps
        if state.known_mechanism is None:
            return False, "Mechanism not established"
        if state.known_mechanism.quality == ASSERTED:
            return False, "Mechanism quality must be REASONED minimum"
        mech_gap = state.get_gap(MECHANISM_COMPLETENESS)
        if mech_gap and mech_gap.status == OPEN:
            return False, "BLOCK: MECHANISM_COMPLETENESS still open"
        return True, "Mechanism established — ready for LEVEL 2"

    return False, f"LEVEL {level} is max for MVP"


# ─────────────────────────────────────────────
# 5. Detect stall
# ─────────────────────────────────────────────

def update_direction(state: IdeaState, prev_level: int) -> None:
    if state.maturity_level > prev_level:
        state.direction = PROGRESSING
    else:
        open_count = len(state.get_open_gaps())
        stalled_gaps = [
            g for g in state.gaps
            if g.status == OPEN and g.iterations_open >= STALL_THRESHOLD
        ]
        if stalled_gaps:
            state.direction = STALLED
        else:
            state.direction = PROGRESSING


# ─────────────────────────────────────────────
# 6. Main loop step
# ─────────────────────────────────────────────

def run_iteration(state: IdeaState, response: str) -> dict:
    """
    Execute one full iteration of the progression loop.
    Returns result dict with question, transition, direction.
    """
    state.iteration += 1
    prev_level = state.maturity_level

    # Update gap iteration counters
    for g in state.gaps:
        if g.status == OPEN:
            g.iterations_open += 1

    # Select gap
    gap_type = select_next_gap(state)

    if gap_type is None:
        can, reason = evaluate_transition(state)
        if can and state.maturity_level < 2:
            state.maturity_level += 1
        update_direction(state, prev_level)
        # إذا وصلنا LEVEL 2 — نطلب تعمق في boundary
        closing_q = None
        if state.maturity_level == 2:
            closing_q = "Your mechanism is taking shape. Now state clearly: what does your invention NOT do or NOT cover? Name at least one boundary."
        return {
            "iteration": state.iteration,
            "gap_targeted": None,
            "question": closing_q,
            "transition": "PASS" if can else "WARN",
            "reason": reason,
            "maturity_level": state.maturity_level,
            "direction": state.direction,
        }

    # Get question — AI advisory (G-A) or fallback to domain/generic
    gap = state.get_gap(gap_type)
    iterations_open = gap.iterations_open if gap else 0
    from engine.ai_advisor import get_ai_question
    _ai_context = {
        "domain": state.domain,
        "gap_type": gap_type,
        "idea_summary": getattr(state, 'idea_summary', None),
        "last_response": response[:200] if response else None,
        "iteration": state.iteration,
    }
    question = get_ai_question(state.domain, gap_type, _ai_context) \
        or get_question(state.domain, gap_type, iterations_open)

    # Integrate response
    transition, reason = integrate_response(state, gap_type, question, response)

    # Check transition
    can, t_reason = evaluate_transition(state)
    if can and state.maturity_level < 2:
        state.maturity_level += 1
        transition = "PASS"
        reason = t_reason

    update_direction(state, prev_level)

    # Log
    log = IterationLog(
        iteration=state.iteration,
        gap_targeted=gap_type,
        question_asked=question,
        response_summary=response[:100],
        gaps_changed=[gap_type],
        maturity_before=prev_level,
        maturity_after=state.maturity_level,
    )
    state.iteration_log.append(log)

    return {
        "iteration"     : state.iteration,
        "gap_targeted"  : gap_type,
        "question"      : question,
        "transition"    : transition,
        "reason"        : reason,
        "maturity_level": state.maturity_level,
        "direction"     : state.direction,
    }
