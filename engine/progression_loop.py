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

import warnings
from engine.domain_rules import get_substance_signals, is_known_domain
from engine.idea_state import (
    IdeaState, Evidence, Gap, IterationLog, AcknowledgedUnknown,
    PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY, MECHANISM_COMPLETENESS,
    PROBLEM_MECHANISM_FIT, ASSUMPTION_INVENTORY, EXPERTISE_GAP_AWARENESS,
    STAGE_2_GAP_TYPES, STAGE_3_GAP_TYPES,
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

# Stage 3 gap priority (per STAGE3_GAP_TAXONOMY_PROPOSAL)
# PMF must be attempted before AI; AI before EGA
STAGE3_GAP_PRIORITY = [
    PROBLEM_MECHANISM_FIT,
    ASSUMPTION_INVENTORY,
    EXPERTISE_GAP_AWARENESS,
]

STALL_THRESHOLD = 3  # iterations before reframe

_IDEA_SUMMARY_MAX = 500

def _trim_idea_summary(text: str) -> str:
    """Inventor statement safely trimmed — display safeguard, not summarization.

    When the statement exceeds the limit it is cut at a word boundary and an
    explicit ellipsis marker is appended, so the truncation is visible and never
    reads as a broken mid-phrase sentence. The full original statement remains
    available in ``state.known_problem.content``; this is a display safeguard
    only and adds no meaning.
    """
    text = text.strip()
    if len(text) <= _IDEA_SUMMARY_MAX:
        return text
    trimmed = text[:_IDEA_SUMMARY_MAX]
    boundary = trimmed.rfind(" ")
    cut = trimmed[:boundary] if boundary > 0 else trimmed
    return cut.rstrip() + "…"



# ─────────────────────────────────────────────
# 1. Select next gap to address
# ─────────────────────────────────────────────

def _active_gap_priority(state: IdeaState) -> list[str]:
    """
    Return the gap-priority order for the state's current stage.

    Stage 3 (state.current_stage == 3) uses STAGE3_GAP_PRIORITY; every other
    stage uses the Stage 2 GAP_PRIORITY. This mirrors the stage-aware
    selection already performed by the no-active-gap cascade in
    run_iteration(); it introduces no new priority data and no new gap
    types. Behaviour-preserving for Stage 2 (current_stage defaults to 2).
    """
    return (
        STAGE3_GAP_PRIORITY
        if getattr(state, "current_stage", 2) == 3
        else GAP_PRIORITY
    )


def select_next_gap(state: IdeaState) -> str | None:
    """
    Return the highest-priority OPEN/PARTIAL gap_type for the active stage.
    Returns None if no open gaps exist.
    """
    open_gaps = {g.gap_type: g for g in state.gaps if g.status in (OPEN, PARTIAL)}
    for gap_type in _active_gap_priority(state):
        if gap_type in open_gaps:
            return gap_type
    return None


def _open_next_gap_if_needed(state):
    """Open the next active-stage priority gap if no OPEN/PARTIAL gap exists. Returns gap_type or None."""
    if any(g.status in (OPEN, PARTIAL) for g in state.gaps):
        return None
    for next_gap_type in _active_gap_priority(state):
        if state.get_gap(next_gap_type) is None:
            from engine.idea_state import Gap
            gap = Gap(gap_type=next_gap_type, status=OPEN, opened_at=state.iteration)
            state.gaps.append(gap)
            return next_gap_type
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
    # ── Stage 3 questions — sourced verbatim from STAGE3_QUESTION_SET.md (admitted 5926b63) ──
    PROBLEM_MECHANISM_FIT: [
        # PMF-Q1 — Primary Evidence Target: PMF-E1
        "Without describing how your mechanism works, describe the problem you are trying to solve. "
        "What is happening for the person or system that has this problem, and why does it matter to them?",
        # PMF-Q2 — Primary Evidence Target: PMF-E2
        "Why does your mechanism solve this problem rather than a different approach? "
        "What is it about how your mechanism works that makes it the right fit for this problem?",
        # PMF-Q3 — Primary Evidence Target: PMF-E3
        "Are there situations or conditions where your mechanism would not solve this problem, "
        "or would solve it less well? What are those conditions?",
    ],
    ASSUMPTION_INVENTORY: [
        # AI-Q1 — Primary Evidence Target: AI-E1
        "What are you taking for granted about your mechanism that you have not yet tested or verified? "
        "These might be things you expect to be true, materials you assume are available, "
        "or conditions you assume will hold.",
        # AI-Q2 — Primary Evidence Target: AI-E2
        "For each assumption you named, would your mechanism still work if that assumption turned out to be wrong? "
        "Which assumptions are essential — the mechanism fails without them — "
        "and which ones would just require you to adjust your approach?",
        # AI-Q3 — Primary Evidence Target: AI-E3
        "Now that you have thought through your assumptions — is there anything you realize you were assuming "
        "that you had not recognized as an assumption before this conversation? "
        "Something that seemed obvious but is actually unverified?",
    ],
    EXPERTISE_GAP_AWARENESS: [
        # EGA-Q1 — Primary Evidence Target: EGA-E1
        "What areas of technical knowledge would someone need to actually build or implement your mechanism? "
        "List the domains of expertise required — not what you know, but what the implementation itself demands.",
        # EGA-Q2 — Primary Evidence Target: EGA-E2
        "Of the expertise areas you just identified — which ones do you have sufficient working knowledge of "
        "to proceed, and which ones represent genuine gaps where you would need to learn more or bring in someone else?",
        # EGA-Q3 — Primary Evidence Target: EGA-E3
        "For the expertise gaps you identified — what would happen to your implementation if those gaps were not "
        "addressed before you started building? What specific problems would you run into?",
    ],
}


# Deterministic, question-layer stall reframe (Increment 1 — Owner-Expert
# Question Boundary). Shown on the non-specialist Path N flow once a gap's
# approved Path N variants are exhausted, instead of repeating the final variant
# verbatim (NON_SPECIALIST_QUESTIONING_POLICY §7; MVP_SCOPE_FREEZE "reframed after
# 3 stalls"). Plain language; asks what the owner already knows and what
# information would be needed; contains no engineering-gated terminology. It is
# pure display content: it does not change gap status, evidence, maturity,
# iteration semantics, or the six owner actions, adds no new action, performs no
# I/O or LLM call, and starts no conversational / multi-question loop. A single
# deterministic reframe is sufficient for this bounded increment; the owner's
# existing six actions remain the truthful exits.
_STALL_REFRAME = (
    "Let's take this part in plainer terms. In your own words, what do you "
    "already know about this aspect of your idea — and what information do you "
    "think you would need, or who could help you find it, to work out the rest? "
    "If you are not sure, you can also use the options below to mark it unknown, "
    "defer it, note a provisional assumption, or ask for a specialist or evidence."
)


def get_question(domain: str, gap_type: str, iterations_open: int,
                 path: str | None = None) -> str:
    """
    Select question for gap_type.
    path == "N": resolves from the approved Path N artifact
    (engine/path_n_questions.py). Gap types not covered by the artifact
    fall through to generic QUESTIONS — the explicit Stage 3 fallthrough
    (b3a5fba §8), not a hidden fallback to Path T content.
    Default / any other path value: existing behavior unchanged —
    domain layer first, generic QUESTIONS fallback.
    Framework-level delegation — no domain-specific logic here.

    Pure selector: this returns the approved/clamped variant for the position and
    deliberately performs NO stall reframe, so the Path N artifact-selection
    invariant is preserved. The owner-facing stall reframe is applied separately
    by get_display_question() (used by the web session view).
    """
    if path == "N":
        from engine.path_n_questions import get_path_n_question
        path_n_q = get_path_n_question(gap_type, iterations_open)
        if path_n_q is not None:
            return path_n_q
        variants = QUESTIONS[gap_type]
        index = min(iterations_open, len(variants) - 1)
        return variants[index]
    from engine.domain_rules import get_domain_question
    domain_q = get_domain_question(domain, gap_type, iterations_open)
    if domain_q:
        return domain_q
    variants = QUESTIONS[gap_type]
    index = min(iterations_open, len(variants) - 1)
    return variants[index]


def get_display_question(domain: str, gap_type: str, iterations_open: int,
                         path: str | None = None) -> str:
    """Owner-facing question for the current gap, with the Increment 1 stall
    reframe applied (Owner-Expert Question Boundary).

    Identical to get_question(), except that on the non-specialist Path N flow
    (path == "N"), once a Stage 2 gap's approved Path N variants are exhausted —
    i.e. get_question() would otherwise repeat the final variant verbatim — the
    deterministic plain-language reframe (_STALL_REFRAME) is returned instead
    (NON_SPECIALIST_QUESTIONING_POLICY §7; MVP_SCOPE_FREEZE "reframed after 3
    stalls"). This is the function the web session view uses to render the
    displayed question; get_question() itself stays a pure selector so the
    approved Path N artifact-selection invariant is unchanged.

    Pure display selection: no engine state, gap status, evidence, maturity,
    iteration semantics, or owner action is changed; no persistence, I/O, or LLM
    call is performed; the approved artifact is not modified. A single
    deterministic reframe is sufficient — the existing six owner actions remain
    the truthful exits.
    """
    if path == "N" and iterations_open > 0:
        from engine.path_n_questions import get_path_n_question
        current = get_path_n_question(gap_type, iterations_open)
        # Path N serves Stage 2 gaps; a clamp (current == the previous
        # iteration's question) marks variant exhaustion → reframe instead of a
        # verbatim repeat. Stage 3 gaps return None here and are unaffected.
        if current is not None and current == get_path_n_question(
            gap_type, iterations_open - 1
        ):
            return _STALL_REFRAME
    return get_question(domain, gap_type, iterations_open, path=path)


# ─────────────────────────────────────────────
# 2b. Acknowledged unknown detection (parallel track)
# Conservative: false negatives ok, false positives not.
# Governance: TRANSITION_AUTHORIZATION_GOVERNANCE s4 Layer 1 PGC-3
# Authorization: Owner-authorized 2026-06-06
# ─────────────────────────────────────────────

_ACKNOWLEDGED_UNKNOWN_MARKERS = (
    "i do not know",
    "i don't know the",
    "i am not sure about",
    "i'm not sure about",
    "i have not yet determined",
    "i do not yet know",
    "i haven't determined",
    "i have not decided",
    "i haven't decided",
    "i am not yet sure",
    "i'm not yet sure",
    "i have not yet researched",
    "i haven't researched",
)

_MIN_ACKNOWLEDGED_UNKNOWN_LENGTH = 40


def _detect_acknowledged_unknown(response, gap_type, iteration):
    """
    Conservative detection of explicit acknowledged unknowns.
    Requires ignorance marker AND minimum response length.
    Returns AcknowledgedUnknown or None.
    NO effect on gap closure or quality classification.
    """
    r = response.strip()
    if len(r) < _MIN_ACKNOWLEDGED_UNKNOWN_LENGTH:
        return None
    r_lower = r.lower()
    for marker in _ACKNOWLEDGED_UNKNOWN_MARKERS:
        if marker in r_lower:
            return AcknowledgedUnknown(
                iteration=iteration,
                gap_context=gap_type,
                verbatim=r,
                category_basis=marker,
            )
    return None


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
_GENERIC_CAUSAL_VERBS = {
    "detects","detect","sends","send","uses","use",
    "connects","connect","receives","receive","triggers",
    "trigger","activates","activate","processes","process",
}
_CAUSAL_STRUCTURE_PATTERNS = [
    "when ","if ","after ","before ","until ","once ","as soon as ",
    "causes","produces","results in","leads to",
    "converts","transforms","transfers",
    "measures","calculates","compares","exceeds",
    "locks","releases","pushes","pulls","blocks","rotates",
    "in order to","so that","which means","which causes",
    "by measuring","by detecting","by converting","then ",
    
]
def _has_causal_structure(r_lower):
    return any(p in r_lower for p in _CAUSAL_STRUCTURE_PATTERNS)
def _is_generic_verb_trap(r_lower):
    if not (set(r_lower.split()) & _GENERIC_CAUSAL_VERBS): return False
    return not _has_causal_structure(r_lower)



MIN_REASONED_RESPONSE_LENGTH = 40  # anti-triviality guard only — see ADR-003 Step 6 note

def assess_response(response: str, domain: str = "") -> str:
    """
    Quality assessment: weak-answer guard + substance check.
    Rules 1-2: weak pattern rejection. Rule 2.5: generic verb trap.
    Rule 3: substance + causal structure + length. See ADR-004.
    """
    r = response.strip()
    r_lower = r.lower()

    # 1. Reject explicit weak answers regardless of length
    if r_lower in _WEAK_PATTERNS:
        return ASSERTED  # stays ASSERTED — will not pass evaluate_transition

    # 2. Reject vague filler phrases (contains weak tokens, no substance)
    weak_tokens = {"somehow", "something", "technology", "stuff", "things"}
    # Substance Signal Authority: read from registry per domain (AB-005 Step 7)
    substance_tokens = set(
        get_substance_signals(domain)
    )
    # AB-006-D: fail-explicit observability for empty/unknown domain
    if not domain:
        warnings.warn(
            "assess_response called with empty domain — "
            "substance check disabled (AB-006-D)",
            stacklevel=2
        )
    elif not is_known_domain(domain):
        warnings.warn(
            "assess_response: domain=" + repr(domain) + " not found in registry — "
            "substance check disabled (AB-006-D)",
            stacklevel=2
        )
    elif not substance_tokens:
        warnings.warn(
            "assess_response: domain=" + repr(domain) + " has no substance signals in registry — "
            "substance check disabled (AB-006-D)",
            stacklevel=2
        )
    words = set(r_lower.split())
    has_weak = bool(words & weak_tokens)
    has_substance = any(sig in r_lower for sig in substance_tokens)

    if has_weak and not has_substance:
        return ASSERTED  # vague filler — no technical substance

    # 3. Substance token present AND response meets minimum length (anti-triviality guard)
    #    NOTE: length threshold does NOT validate reasoning quality — see ADR-003 Step 6 note
    if _is_generic_verb_trap(r_lower):
        return ASSERTED
    has_causal = _has_causal_structure(r_lower)
    # REASONED path A: substance domain token + causal structure + length
    # REASONED path B: causal structure + no trap + length (for non-electronics domains)
    if has_causal and not _is_generic_verb_trap(r_lower) and len(r) >= MIN_REASONED_RESPONSE_LENGTH:
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
    quality = assess_response(response, state.domain)
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
    if state.known_problem is None and quality >= REASONED:  # RISK-002
        state.known_problem = evidence

    # Update gap status
    gap = state.get_gap(gap_type)
    if gap is None:
        gap = Gap(gap_type=gap_type, status=OPEN, opened_at=state.iteration)
        state.gaps.append(gap)

    # Parallel track: record acknowledged unknown if present.
    # Unconditional -- runs for DEMONSTRATED, REASONED, and ASSERTED.
    # Does NOT affect gap.status, quality, or any return value.
    _unknown = _detect_acknowledged_unknown(response, gap_type, state.iteration)
    if _unknown is not None:
        state.acknowledged_unknowns.append(_unknown)

    # Capture accepted (substantiated) evidence for Stage 3 reasoning gaps only.
    # Restricted to PROBLEM_MECHANISM_FIT / ASSUMPTION_INVENTORY /
    # EXPERTISE_GAP_AWARENESS — Stage 2 gaps do not use this capture path.
    # "Accepted" = REASONED or better (the quality tier that advances a gap);
    # ASSERTED and empty/whitespace responses are NOT recorded. Append-only:
    # no effect on gap.status, quality, transition, or return value.
    if (gap_type in STAGE_3_GAP_TYPES
            and response.strip()
            and quality in (REASONED, DEMONSTRATED)):
        gap.evidence.append(evidence)

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
        if state.known_problem and state.known_problem.quality >= REASONED:
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
        if mech_gap and mech_gap.status != CLOSED:
            return False, "BLOCK: MECHANISM_COMPLETENESS not yet closed"
        # GD-001 / ILT-F-001: all Stage Two gaps must exist and be CLOSED
        REQUIRED_STAGE_TWO_GAPS = [
            MECHANISM_COMPLETENESS,
            PHYSICAL_FEASIBILITY,
            BOUNDARY_AMBIGUITY,
        ]
        for required_gap in REQUIRED_STAGE_TWO_GAPS:
            gap = state.get_gap(required_gap)
            if gap is None:
                return False, f"BLOCK: {required_gap} not yet opened"
            if gap.status != CLOSED:
                return False, f"BLOCK: {required_gap} not yet closed (status: {gap.status})"
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
            if g.status in (OPEN, PARTIAL) and g.iterations_open >= STALL_THRESHOLD
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
        if g.status in (OPEN, PARTIAL):
            g.iterations_open += 1

    # Select gap
    gap_type = select_next_gap(state)

    # Level-0 problem establishment path
    # Handles initial response when no gaps exist yet (maturity=0)
    if gap_type is None and state.maturity_level == 0 and response:
        quality = assess_response(response, state.domain)
        evidence = Evidence(
            content=response,
            quality=quality,
            iteration=state.iteration,
        )
        if quality >= REASONED and (state.known_problem is None or quality > state.known_problem.quality):  # RISK-002
            state.known_problem = evidence
            if state.idea_summary is None:  # R-007: capture once
                state.idea_summary = _trim_idea_summary(response)

    if gap_type is None:
        can, reason = evaluate_transition(state)
        if can and state.maturity_level < 2:
            state.maturity_level += 1
            if state.maturity_level == 2:
                state.current_stage = 3
        # Level-1 gap initialization: open MECHANISM_COMPLETENESS if maturity just reached 1
        if state.maturity_level == 1 and len(state.gaps) == 0 and state.get_gap(MECHANISM_COMPLETENESS) is None:
            from engine.idea_state import Gap
            gap = Gap(gap_type=MECHANISM_COMPLETENESS, status=OPEN, opened_at=state.iteration)
            state.gaps.append(gap)
        # GAP_PRIORITY cascade: open next gap when no OPEN/PARTIAL gap exists
        next_gap_opened = None
        if len([g for g in state.gaps if g.status in (OPEN, PARTIAL)]) == 0:
            # Select gap priority based on current stage
            active_priority = (
                STAGE3_GAP_PRIORITY
                if getattr(state, "current_stage", 2) == 3
                else GAP_PRIORITY
            )
            for next_gap_type in active_priority:
                if state.get_gap(next_gap_type) is None:
                    from engine.idea_state import Gap
                    gap = Gap(gap_type=next_gap_type, status=OPEN, opened_at=state.iteration)
                    state.gaps.append(gap)
                    next_gap_opened = next_gap_type
                    break
        update_direction(state, prev_level)
        # إذا وصلنا LEVEL 2 — نطلب تعمق في boundary
        # If cascade opened a new gap, generate its question and return
        if next_gap_opened:
            new_gap = state.get_gap(next_gap_opened)
            iterations_open = new_gap.iterations_open if new_gap else 0
            from engine.ai_advisor import get_ai_question
            _ai_ctx = {
                "domain": state.domain,
                "gap_type": next_gap_opened,
                "idea_summary": getattr(state, "idea_summary", None),
                "last_response": None,
                "iteration": state.iteration,
            }
            _ai_q = None if state.path == "N" \
                else get_ai_question(state.domain, next_gap_opened, _ai_ctx)
            next_q = _ai_q \
                or get_question(state.domain, next_gap_opened, iterations_open,
                                path=state.path)
            result = {
                "iteration"     : state.iteration,
                "gap_targeted"  : next_gap_opened,
                "question"      : next_q,
                "transition"    : "PASS" if can else "WARN",
                "reason"        : reason,
                "maturity_level": state.maturity_level,
                "direction"     : state.direction,
            }
        else:
            closing_q = None
            if state.maturity_level == 2:
                closing_q = "Your mechanism is taking shape. Now state clearly: what does your invention NOT do or NOT cover? Name at least one boundary."
            result = {
                "iteration": state.iteration,
                "gap_targeted": None,
                "question": closing_q,
                "transition": "PASS" if can else "WARN",
                "reason": reason,
                "maturity_level": state.maturity_level,
                "direction": state.direction,
            }

    else:
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
        _ai_q = None if state.path == "N" \
            else get_ai_question(state.domain, gap_type, _ai_context)
        question = _ai_q \
            or get_question(state.domain, gap_type, iterations_open,
                            path=state.path)

        # Integrate response
        transition, reason = integrate_response(state, gap_type, question, response)

        # Check transition
        can, t_reason = evaluate_transition(state)
        if can and state.maturity_level < 2:
            state.maturity_level += 1
            if state.maturity_level == 2:
                state.current_stage = 3
            transition = "PASS"
            reason = t_reason

        update_direction(state, prev_level)

        # GAP_PRIORITY cascade — open next gap if none remain
        next_gap_opened = _open_next_gap_if_needed(state)
        next_q = None
        if next_gap_opened:
            new_gap = state.get_gap(next_gap_opened)
            iterations_open = new_gap.iterations_open if new_gap else 0
            from engine.ai_advisor import get_ai_question
            ai_ctx = {
                "domain": state.domain,
                "gap_type": next_gap_opened,
                "idea_summary": getattr(state, "idea_summary", None),
                "last_response": None,
                "iteration": state.iteration,
            }
            _ai_q = (
                None if state.path == "N"
                else get_ai_question(state.domain, next_gap_opened, ai_ctx)
            )
            next_q = (
                _ai_q
                or get_question(state.domain, next_gap_opened, iterations_open,
                                path=state.path)
            )
        result = {
            "iteration": state.iteration,
            "gap_targeted": next_gap_opened,
            "question": next_q,
            "transition": transition,
            "reason": reason,
            "maturity_level": state.maturity_level,
            "direction": state.direction,
        }

    # Log — single exit guaranteed by structure
    log = IterationLog(
        iteration=state.iteration,
        gap_targeted=result.get('gap_targeted'),
        question_asked=result.get('question'),
        response_summary=response[:100],
        gaps_changed=[result.get('gap_targeted')],
        maturity_before=prev_level,
        maturity_after=state.maturity_level,
    )
    state.iteration_log.append(log)
    return result
