"""G1 pre-creation candidate v2 instructions — OFFLINE EVALUATION DESIGN ONLY.

Not used by the frozen campaign-01 runner or by any product path. No provider
client, network, storage, scoring, schema or product authority is added here.
The v1 scorer and authoritative concept vocabulary remain the only owners.
"""
from scripts import run_g1_precreation_semantic_eval as v1

ORIGINAL_COMPONENT_RULE = (
    "A device the invention only holds or works with, someone else's device, "
    "packaging, a technology mentioned only as inspiration, and anything "
    "hypothetical, undecided or negated is NOT a stated part. "
)
CANDIDATE_COMPONENT_RULE = (
    "Count as a stated included part a pre-existing board or module that the "
    "person explicitly intends to install, connect, fasten or use as a functional "
    "constituent of the finished invention, even if the person bought or reused it. "
    "Being included does NOT mean the person designed or manufactured that part, "
    "owns its rights, or has verified its suitability. Exclude a standalone "
    "device that the invention merely holds, carries, supports or works with "
    "while that device remains separate; exclude shipping packaging, external "
    "installation targets, inspiration, hypothetical, undecided or negated parts. "
    "Do not include an external device just because it appears nearby. "
)
ORIGINAL_COMPOSITION_RULE = (
    "CLARIFY_FIRST if that is genuinely open and a question to the person should "
    "come first; otherwise NO_INTEGRATED_SUGGESTION."
)
CANDIDATE_COMPOSITION_RULE = (
    "CLARIFY_FIRST when the kind or function of the proposed invention is too "
    "unclear to choose a composition route, or when whether a mentioned part "
    "belongs to the final assembly is genuinely undecided; ask about that "
    "uncertainty before assigning inclusion or exclusion. Otherwise return "
    "NO_INTEGRATED_SUGGESTION if an integrated composition is not grounded. "
    "Do NOT choose CLARIFY_FIRST merely because dimensions, mounting details "
    "or another engineering question remains: a clearly stated integrated "
    "assembly can still need questions. Never infer an unstated part to "
    "justify SUGGEST_INTEGRATED."
)


def candidate_instructions(concepts=None):
    """A distinct, unqualified prompt candidate from v1's already-owned schema."""
    concepts = v1.governed_concepts() if concepts is None else concepts
    original = v1._instructions(concepts)
    if original.count(ORIGINAL_COMPONENT_RULE) != 1:
        raise ValueError("frozen component rule unavailable/ambiguous")
    if original.count(ORIGINAL_COMPOSITION_RULE) != 1:
        raise ValueError("frozen composition rule unavailable/ambiguous")
    return (original.replace(ORIGINAL_COMPONENT_RULE, CANDIDATE_COMPONENT_RULE, 1)
                    .replace(ORIGINAL_COMPOSITION_RULE, CANDIDATE_COMPOSITION_RULE, 1))


def candidate_request_view(idea_text, concepts=None):
    """Offline preparation only; no provider call, storage or score."""
    import json

    if not isinstance(idea_text, str) or not idea_text.strip():
        raise ValueError("idea text required")
    concepts = v1.governed_concepts() if concepts is None else concepts
    return {
        "instructions": candidate_instructions(concepts),
        "input": json.dumps({"idea_text": idea_text}, ensure_ascii=False),
        "schema": v1._schema(concepts),
    }
