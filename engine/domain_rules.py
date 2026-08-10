"""
Domain Rules — lightweight electronics/electrical only.
MVP: 3 rules maximum per MVP_SCOPE_FREEZE.md
"""

from engine.domain_registry import load_registry
from engine import domain_activation
_REGISTRY = load_registry("domains/")

# DEPRECATED: authority moved to registry — Step 5 (AB-005). Remove in Step 7.


def infer_domain(idea_text: str) -> str | None:
	text = idea_text.lower()
	scores = {
		pack_id: sum(1 for item in pack["classification_signals"] if item["signal"] in text)
		for pack_id, pack in _REGISTRY.items()
	}
	if not scores or max(scores.values()) == 0:
		return None
	best_score = max(scores.values())
	tied = [d for d in scores if scores[d] == best_score]
	# D3-D (core domain-neutrality): on a classification tie, an ACTIVATED domain
	# outranks a RECOGNIZED_NOT_ACTIVATED one — a recognized-but-not-activated pack
	# can NEVER become effective activated routing/admission authority through this
	# shared inference seam via an ungoverned literal. Consumes the canonical §5-I2
	# activation policy (engine/domain_activation.py); deterministic (sorted). When
	# no tied domain is activated (an edge case that yields no admissible domain
	# regardless of ordering), the prior deterministic priority order is preserved
	# for backward compatibility.
	activated_tied = sorted(d for d in tied if domain_activation.is_activated(d, _REGISTRY))
	if activated_tied:
		return activated_tied[0]
	priority = ["medical_device", "electronics_electrical", "mechanical", "software"]
	for domain in priority:
		if scores.get(domain, 0) == best_score:
			return domain
	return None
def get_active_rules(domain: str) -> list:
    # AB-006-A Step 1e: all domains read from registry rule_nuances
    pack = _REGISTRY.get(domain)
    if pack and pack.get("rule_nuances"):
        return [rn["modifier_value"] for rn in pack["rule_nuances"]]
    return []

# ------------------------------------
# Domain-specific question registry
# ------------------------------------







# ------------------------------------
# Software domain
# MVP interpretation:
# MECHANISM_COMPLETENESS = software logic/workflow/algorithm
# PHYSICAL_FEASIBILITY excluded — assumes physical constraints
# BOUNDARY_AMBIGUITY = scope and what the system does NOT do
# This is MVP-only. Future richer taxonomy requires framework review.
# ------------------------------------




def is_known_domain(domain: str) -> bool:
    # AB-006-D: check domain existence without exposing _REGISTRY
    return domain in _REGISTRY


def get_substance_signals(domain: str) -> list:
    # AB-006-C: registry accessor — replaces direct _REGISTRY access in progression_loop.py
    pack = _REGISTRY.get(domain)
    if pack:
        return [s["signal"] for s in pack.get("substance_signals", [])]
    return []

def get_domain_question(domain: str, gap_type: str, iterations_open: int) -> str | None:
    """
    Return a domain-specific question for gap_type, or None to trigger generic fallback.
    Domain layer owns questions. Engine must not contain domain-specific question logic.
    """
    # Gap Discovery Authority: read from registry gap_type_mappings (AB-005 Step 6b)
    pack = _REGISTRY.get(domain)
    if not pack:
        return None
    for mapping in pack.get("gap_type_mappings", []):
        if mapping.get("gap_type_id") == gap_type:
            questions = mapping.get("questions", [])
            if not questions:
                return None
            index = min(iterations_open, len(questions) - 1)
            return questions[index].get("text")
    return None
