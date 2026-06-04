"""
stage3_evaluator.py — Stage 3 Response Quality Evaluation

Governance authority: STAGE3_EVALUATION_MODEL, STAGE3_GAP_EVIDENCE_MODEL,
                      STAGE3_CAPABILITY_MODEL, STAGE3_EXIT_CRITERIA

Scope: Evaluates Stage 3 response quality only.
       Does NOT decide progression.
       Does NOT authorize transitions.
       Does NOT advance maturity.
       Does NOT modify IdeaState directly.

The four evaluation acts per STAGE3_EVALUATION_MODEL:
  Act 1 — Detection: identify candidate evidence signals in response
  Act 2 — Evidence Confirmation: confirm signals constitute genuine evidence items
  Act 3 — Capability Assessment: assess whether evidence demonstrates capability
  Act 4 — Resolution Judgment: judge whether capability is sufficient for gap resolution

Acts 1-4 produce observations only. Authorization is a separate layer
per TRANSITION_AUTHORIZATION_GOVERNANCE OA-1 (Hybrid Model).
"""

from dataclasses import dataclass, field
from typing import Optional

from engine.idea_state import (
    PROBLEM_MECHANISM_FIT,
    ASSUMPTION_INVENTORY,
    EXPERTISE_GAP_AWARENESS,
    REASONED, ASSERTED,
)


# ─────────────────────────────────────────────────────────────
# Evidence item identifiers per STAGE3_GAP_EVIDENCE_MODEL
# ─────────────────────────────────────────────────────────────

# PROBLEM_MECHANISM_FIT evidence items
PMF_E1 = "PMF_E1"  # Independent problem articulation
PMF_E2 = "PMF_E2"  # Causal fit justification
PMF_E3 = "PMF_E3"  # Fit boundary awareness

# ASSUMPTION_INVENTORY evidence items
AI_E1 = "AI_E1"   # Assumption identification
AI_E2 = "AI_E2"   # Assumption classification
AI_E3 = "AI_E3"   # Assumption consequence reasoning

# EXPERTISE_GAP_AWARENESS evidence items
EGA_E1 = "EGA_E1"  # Domain expertise identification
EGA_E2 = "EGA_E2"  # Self-assessment against requirement
EGA_E3 = "EGA_E3"  # Consequence reasoning for expertise gap


# ─────────────────────────────────────────────────────────────
# Result dataclasses
# ─────────────────────────────────────────────────────────────

@dataclass
class EvidenceObservation:
    """Act 2 output — confirmed evidence items for one gap response."""
    gap_type: str
    confirmed_items: list = field(default_factory=list)   # e.g. [PMF_E1, PMF_E2]
    missing_items: list = field(default_factory=list)
    notes: str = ""


@dataclass
class CapabilityObservation:
    """Act 3 output — capability assessment for one gap."""
    gap_type: str
    capability_present: bool = False
    integration_observed: bool = False  # evidence items cohere, not isolated
    notes: str = ""


@dataclass
class ResolutionObservation:
    """Act 4 output — resolution judgment for one gap.
    This is an OBSERVATION, not an authorization decision.
    Authorization requires human review per OA-1 Hybrid Model."""
    gap_type: str
    sufficient_for_resolution: bool = False
    notes: str = ""


@dataclass
class Stage3EvaluationResult:
    """Full evaluation result for one Stage 3 gap response.
    Produced by evaluate_stage3_response().
    Does NOT trigger progression. Does NOT authorize transition."""
    gap_type: str
    base_quality: str           # REASONED or ASSERTED from assess_response
    act1_signals: list = field(default_factory=list)
    act2_evidence: Optional[EvidenceObservation] = None
    act3_capability: Optional[CapabilityObservation] = None
    act4_resolution: Optional[ResolutionObservation] = None
    is_stage3_gap: bool = False


# ─────────────────────────────────────────────────────────────
# Detection signals per gap type (Act 1)
# ─────────────────────────────────────────────────────────────

# Signals indicating Problem-Mechanism Fit reasoning
_PMF_SIGNALS = [
    "addresses", "solves", "because", "therefore", "the problem is",
    "my invention", "this mechanism", "specifically", "designed to",
    "intended to", "in order to", "so that", "which means",
    "fit", "mismatch", "does not address", "fails to",
]

# Signals indicating Assumption Inventory reasoning
_AI_SIGNALS = [
    "assume", "assuming", "assumption", "depends on", "relies on",
    "requires", "presupposes", "if", "provided that", "given that",
    "unvalidated", "not yet proven", "need to verify", "uncertain",
    "I believe", "I expect", "should work", "might",
]

# Signals indicating Expertise Gap Awareness reasoning
_EGA_SIGNALS = [
    "don't know", "do not know", "lack", "need expertise",
    "need help", "unfamiliar", "limited knowledge", "need to learn",
    "consult", "specialist", "expert", "beyond my knowledge",
    "gap in my knowledge", "would need", "cannot determine",
    "not sure how", "need to research",
]

_GAP_SIGNALS = {
    PROBLEM_MECHANISM_FIT: _PMF_SIGNALS,
    ASSUMPTION_INVENTORY: _AI_SIGNALS,
    EXPERTISE_GAP_AWARENESS: _EGA_SIGNALS,
}


# ─────────────────────────────────────────────────────────────
# Core evaluation function
# ─────────────────────────────────────────────────────────────

def evaluate_stage3_response(
    gap_type: str,
    response: str,
    base_quality: str,
    invention_reference: Optional[str] = None,
) -> Stage3EvaluationResult:
    """
    Evaluate a Stage 3 gap response through four acts.

    Parameters:
        gap_type: one of PROBLEM_MECHANISM_FIT, ASSUMPTION_INVENTORY,
                  EXPERTISE_GAP_AWARENESS
        response: inventor's text response
        base_quality: REASONED or ASSERTED from assess_response()
        invention_reference: idea_summary for PGC-2 grounding check

    Returns Stage3EvaluationResult — observations only, no progression decisions.
    """
    from engine.idea_state import STAGE_3_GAP_TYPES

    result = Stage3EvaluationResult(
        gap_type=gap_type,
        base_quality=base_quality,
        is_stage3_gap=(gap_type in STAGE_3_GAP_TYPES),
    )

    if gap_type not in STAGE_3_GAP_TYPES:
        return result  # Not a Stage 3 gap — return empty observation

    r_lower = response.lower()

    # ── Act 1: Detection ──────────────────────────────────────
    signals = _GAP_SIGNALS.get(gap_type, [])
    detected = [sig for sig in signals if sig in r_lower]
    result.act1_signals = detected

    # ── Act 2: Evidence Confirmation ─────────────────────────
    evidence = _confirm_evidence(gap_type, r_lower, detected, invention_reference)
    result.act2_evidence = evidence

    # ── Act 3: Capability Assessment ──────────────────────────
    capability = _assess_capability(gap_type, evidence, base_quality)
    result.act3_capability = capability

    # ── Act 4: Resolution Judgment ────────────────────────────
    resolution = _judge_resolution(gap_type, capability, base_quality)
    result.act4_resolution = resolution

    return result


def _confirm_evidence(
    gap_type: str,
    r_lower: str,
    detected_signals: list,
    invention_reference: Optional[str],
) -> EvidenceObservation:
    """Act 2: Confirm which evidence items are present."""
    obs = EvidenceObservation(gap_type=gap_type)

    has_signals = len(detected_signals) >= 1
    has_invention_ref = (
        invention_reference is not None
        and any(
            word in r_lower
            for word in (invention_reference or "").lower().split()
            if len(word) > 4
        )
    ) if invention_reference else False

    if gap_type == PROBLEM_MECHANISM_FIT:
        # PMF-E1: independent problem articulation (mentions problem without just restating question)
        if has_signals and len(r_lower) >= 60:
            obs.confirmed_items.append(PMF_E1)
        else:
            obs.missing_items.append(PMF_E1)
        # PMF-E2: causal fit justification (mechanism addresses problem with reasoning)
        causal_words = ["because", "therefore", "which means", "so that", "in order to"]
        if any(w in r_lower for w in causal_words) and has_signals:
            obs.confirmed_items.append(PMF_E2)
        else:
            obs.missing_items.append(PMF_E2)
        # PMF-E3: fit boundary awareness (acknowledges limits or mismatches)
        boundary_words = ["does not", "cannot", "limitation", "only", "but not",
                         "mismatch", "fails to", "does not address"]
        if any(w in r_lower for w in boundary_words):
            obs.confirmed_items.append(PMF_E3)
        else:
            obs.missing_items.append(PMF_E3)

    elif gap_type == ASSUMPTION_INVENTORY:
        # AI-E1: assumption identification (names at least one assumption)
        if has_signals and len(r_lower) >= 40:
            obs.confirmed_items.append(AI_E1)
        else:
            obs.missing_items.append(AI_E1)
        # AI-E2: assumption classification (labels assumptions by type or status)
        classification_words = ["unvalidated", "proven", "not yet", "need to verify",
                                "certain", "uncertain", "validated", "tested"]
        if any(w in r_lower for w in classification_words):
            obs.confirmed_items.append(AI_E2)
        else:
            obs.missing_items.append(AI_E2)
        # AI-E3: consequence reasoning (what happens if assumption is wrong)
        consequence_words = ["if not", "if wrong", "would fail", "would not work",
                            "risk", "could mean", "affects", "impact"]
        if any(w in r_lower for w in consequence_words):
            obs.confirmed_items.append(AI_E3)
        else:
            obs.missing_items.append(AI_E3)

    elif gap_type == EXPERTISE_GAP_AWARENESS:
        # EGA-E1: domain expertise identification (names required expertise)
        if has_signals and len(r_lower) >= 40:
            obs.confirmed_items.append(EGA_E1)
        else:
            obs.missing_items.append(EGA_E1)
        # EGA-E2: self-assessment (inventor evaluates own knowledge against requirement)
        self_assessment_words = ["i lack", "i don't know", "i do not know",
                                 "limited", "i need", "beyond my"]
        if any(w in r_lower for w in self_assessment_words):
            obs.confirmed_items.append(EGA_E2)
        else:
            obs.missing_items.append(EGA_E2)
        # EGA-E3: consequence reasoning (what gap means for implementation path)
        consequence_words = ["need to", "would need", "must consult", "before i can",
                            "can't proceed", "blocks", "required to"]
        if any(w in r_lower for w in consequence_words):
            obs.confirmed_items.append(EGA_E3)
        else:
            obs.missing_items.append(EGA_E3)

    return obs


def _assess_capability(
    gap_type: str,
    evidence: EvidenceObservation,
    base_quality: str,
) -> CapabilityObservation:
    """Act 3: Assess whether evidence demonstrates capability.
    Capability requires evidence items to cohere — not just be present."""
    obs = CapabilityObservation(gap_type=gap_type)

    confirmed_count = len(evidence.confirmed_items)

    # Minimum: at least 2 evidence items AND base quality is REASONED
    # Per STAGE3_CAPABILITY_MODEL: capability requires integration, not isolated items
    if confirmed_count >= 2 and base_quality == REASONED:
        obs.capability_present = True
        # Integration observed if all 3 evidence items confirmed
        # (coherent reasoning act, not 3 separate responses)
        if confirmed_count == 3:
            obs.integration_observed = True
            obs.notes = "All three evidence items confirmed — integration observed"
        else:
            obs.notes = f"{confirmed_count}/3 evidence items confirmed — partial capability"
    else:
        obs.capability_present = False
        obs.notes = (
            f"Capability not demonstrated: {confirmed_count}/3 items, "
            f"quality={base_quality}"
        )

    return obs


def _judge_resolution(
    gap_type: str,
    capability: CapabilityObservation,
    base_quality: str,
) -> ResolutionObservation:
    """Act 4: Judge whether demonstrated capability is sufficient for resolution.
    This is an OBSERVATION only — not an authorization decision.
    Per TRANSITION_AUTHORIZATION_GOVERNANCE: authorization requires human Layer 2 review."""
    obs = ResolutionObservation(gap_type=gap_type)

    if capability.capability_present:
        obs.sufficient_for_resolution = True
        obs.notes = (
            "Capability observed — gap may be sufficient for resolution. "
            "Requires human reviewer Layer 2 assessment per "
            "TRANSITION_AUTHORIZATION_GOVERNANCE OA-1."
        )
    else:
        obs.sufficient_for_resolution = False
        obs.notes = "Capability not yet demonstrated — gap resolution not indicated."

    return obs


# ─────────────────────────────────────────────────────────────
# Stage-level integration check (SL-R3 proxy)
# ─────────────────────────────────────────────────────────────

def check_cross_gap_integration(
    evaluations: list,
) -> dict:
    """
    Check for cross-gap integration signals across multiple Stage 3 evaluations.
    Proxy for SL-R3 — reasoning integration demonstrated.

    This is an OBSERVATION only. Does not authorize stage transition.
    Per STAGE3_EXIT_CRITERIA SL-R3 and TRANSITION_AUTHORIZATION_GOVERNANCE.

    Parameters:
        evaluations: list of Stage3EvaluationResult across PMF, AI, EGA gaps

    Returns dict with integration assessment.
    """
    if len(evaluations) < 2:
        return {
            "integration_checkable": False,
            "reason": "Fewer than 2 gap evaluations — cross-gap integration not assessable",
        }

    capable_gaps = [
        e.gap_type for e in evaluations
        if e.act3_capability and e.act3_capability.capability_present
    ]

    return {
        "integration_checkable": True,
        "capable_gap_count": len(capable_gaps),
        "capable_gaps": capable_gaps,
        "sl_r3_proxy_met": len(capable_gaps) >= 2,
        "note": (
            "SL-R3 proxy: cross-gap integration observable. "
            "Full SL-R3 assessment requires human reviewer Layer 2 "
            "per TRANSITION_AUTHORIZATION_GOVERNANCE OA-1."
        ),
    }
