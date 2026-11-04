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
# F1 correction: the v1 exclusion sentence is kept verbatim as the first
# sentence, so every v1 protection (including "someone else's device" and
# unqualified "packaging") survives; the inclusion clause is narrowed (F2).
CANDIDATE_COMPONENT_RULE = ORIGINAL_COMPONENT_RULE + (
    "A component counts as a stated part only when the text states that it is "
    "built into, or incorporated as part of, the person's finished invention, "
    "even if the person bought or reused it. Being included does NOT mean the "
    "person designed or manufactured that part, owns its rights, or has "
    "verified its suitability. Holding, carrying, mounting on, fastening onto, "
    "plugging into, connecting to or being used with a separate device does "
    "NOT make that device a part. "
)
ORIGINAL_COMPOSITION_RULE = (
    "CLARIFY_FIRST if that is genuinely open and a question to the person should "
    "come first; otherwise NO_INTEGRATED_SUGGESTION."
)
CANDIDATE_COMPOSITION_RULE = (
    "CLARIFY_FIRST if it is genuinely open whether a mechanical or an "
    "electrical or electronic part is part of the invention at all, or what the "
    "invention is or does, and a question to the person should come first; ask "
    "about that uncertainty instead of assigning inclusion or exclusion. An open "
    "engineering detail (size, which component, material, power, or how a "
    "stated part is attached) does not by itself require CLARIFY_FIRST. "
    "Otherwise NO_INTEGRATED_SUGGESTION. Never infer an unstated part to "
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
