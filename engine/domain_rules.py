"""
Domain Rules — lightweight electronics/electrical only.
MVP: 3 rules maximum per MVP_SCOPE_FREEZE.md
"""

from engine.domain_registry import load_registry
from engine import domain_activation
_REGISTRY = load_registry("domains/")

from dataclasses import dataclass
from enum import Enum


class DomainResultKind(Enum):
    """The four canonical domain-classification result kinds (P9-E2-R)."""
    SINGLE = "single"
    NONE = "none"
    AMBIGUOUS_TIE = "ambiguous_tie"
    MULTI_DOMAIN_NEEDS_D4 = "multi_domain_needs_d4"


class DomainAmbiguityReason(Enum):
    """Deterministic, non-LLM reason codes for the richer kinds (P9-E2-R 12).
    Rendered to human-readable text at the caller; NEVER model-generated."""
    EQUAL_SCORE = "equal_score"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    OVERLAPPING_SCOPE = "overlapping_scope"
    MULTI_DOMAIN = "multi_domain"


class AmbiguousDomainResultError(RuntimeError):
    """Raised by the legacy ``infer_domain`` wrapper when the canonical classifier
    yields a richer kind the ``str | None`` surface cannot represent. Fail-loud by
    design (P9-E2-R 4/8): never silently collapse ambiguity to ``None`` / a domain.
    A ``RuntimeError`` subclass (NOT ``AssertionError``, which is elided under
    ``python -O``)."""


@dataclass(frozen=True)
class DomainClassification:
    """Immutable canonical domain-classification result (P9-E2-R).

    Invariants are enforced mechanically at construction (P9-E2-R 6/11):
    - ``kind`` is exactly one ``DomainResultKind``.
    - SINGLE: exactly one registry-recognized ``selected_domain``; empty
      ``candidates``; no ``reason``.
    - NONE: no ``selected_domain``; empty ``candidates``; no ``reason``.
    - AMBIGUOUS_TIE / MULTI_DOMAIN_NEEDS_D4: no ``selected_domain``; >= 2
      registry-recognized ``candidates`` with UNIQUE ids in canonical (sorted)
      order (duplicates rejected); a deterministic ``reason`` code. AMBIGUOUS_TIE
      additionally requires EVERY candidate to be ACTIVATED (D3-D).
    - Mutual exclusion: a selected domain and a non-empty candidate set never
      co-occur. Canonical ordering is for deterministic equality ONLY --
      ``canonical order != precedence`` (an AMBIGUOUS_TIE has no winner).
    The result is frozen; it never carries fabricated confidence and never mutates
    activation state."""
    kind: "DomainResultKind"
    selected_domain: "str | None" = None
    candidates: tuple = ()
    reason: "DomainAmbiguityReason | None" = None

    def __post_init__(self):
        if not isinstance(self.kind, DomainResultKind):
            raise ValueError("DomainClassification.kind must be a DomainResultKind")
        cands = self.candidates
        if not isinstance(cands, tuple):
            raise ValueError("candidates must be a tuple")
        if any((not isinstance(c, str)) or (not c.strip()) for c in cands):
            raise ValueError("candidate ids must be non-empty strings")
        if len(set(cands)) != len(cands):
            raise ValueError("candidate ids must be unique (duplicates rejected)")
        if tuple(sorted(cands)) != cands:
            raise ValueError(
                "candidates must be in canonical (sorted) order; "
                "canonical order is NOT precedence")
        if self.kind is DomainResultKind.SINGLE:
            if not isinstance(self.selected_domain, str) or not self.selected_domain.strip():
                raise ValueError("SINGLE requires exactly one selected_domain")
            if self.selected_domain not in _REGISTRY:
                raise ValueError("SINGLE selected_domain must be registry-recognized")
            if cands:
                raise ValueError("SINGLE must have an empty candidate set")
            if self.reason is not None:
                raise ValueError("SINGLE must not carry an ambiguity reason")
        elif self.kind is DomainResultKind.NONE:
            if self.selected_domain is not None:
                raise ValueError("NONE must not carry a selected_domain")
            if cands:
                raise ValueError("NONE must have no candidate set")
            if self.reason is not None:
                raise ValueError("NONE must not carry an ambiguity reason")
        else:  # AMBIGUOUS_TIE or MULTI_DOMAIN_NEEDS_D4
            if self.selected_domain is not None:
                raise ValueError("a tie/multi result must not carry a selected winner")
            if len(cands) < 2:
                raise ValueError("a tie/multi result requires >= 2 candidates")
            if not all(c in _REGISTRY for c in cands):
                raise ValueError("all candidates must be registry-recognized")
            if not isinstance(self.reason, DomainAmbiguityReason):
                raise ValueError("a tie/multi result requires a deterministic reason code")
            if self.kind is DomainResultKind.AMBIGUOUS_TIE:
                if not all(domain_activation.is_activated(c, _REGISTRY) for c in cands):
                    raise ValueError("all AMBIGUOUS_TIE candidates must be activated (D3-D)")



# DEPRECATED: authority moved to registry — Step 5 (AB-005). Remove in Step 7.


def classify_domain(idea_text: str) -> "DomainClassification":
    """Canonical domain classifier (P9-E2-R). The single source of classification
    truth (one classifier owner). TODAY it yields only ``SINGLE`` / ``NONE`` --
    behavior-equivalent to the historical ``infer_domain`` string result -- and it
    introduces NO tie detection (that is the later, separate P9-E2 tie-precedence
    runtime). The richer kinds (AMBIGUOUS_TIE / MULTI_DOMAIN_NEEDS_D4) are
    representable by ``DomainClassification`` but are NOT produced here, so no
    currently-unreachable behavior is made reachable by P9-E2-R."""
    text = idea_text.lower()
    scores = {
        pack_id: sum(1 for item in pack["classification_signals"] if item["signal"] in text)
        for pack_id, pack in _REGISTRY.items()
    }
    if not scores or max(scores.values()) == 0:
        return DomainClassification(kind=DomainResultKind.NONE)
    best_score = max(scores.values())
    tied = [d for d in scores if scores[d] == best_score]
    # D3-D (core domain-neutrality): on a classification tie, an ACTIVATED domain
    # outranks a RECOGNIZED_NOT_ACTIVATED one -- a recognized-but-not-activated
    # pack can NEVER become effective activated routing/admission authority through
    # this shared inference seam via an ungoverned literal. Consumes the canonical
    # 5-I2 activation policy; deterministic (sorted). With exactly one activated
    # specialist domain this yields a single domain -- P9-E2-R does NOT change this
    # tie behavior (representation seam only); governed multi-activated precedence
    # is the separate P9-E2 gate.
    activated_tied = sorted(d for d in tied if domain_activation.is_activated(d, _REGISTRY))
    if activated_tied:
        return DomainClassification(
            kind=DomainResultKind.SINGLE, selected_domain=activated_tied[0])
    # No activated tied domain: preserve the prior deterministic priority order for
    # backward compatibility (line-34 fallback, unchanged; see P9-E2-R 21 for the
    # registered future Nth-domain obligation).
    priority = ["medical_device", "electronics_electrical", "mechanical", "software"]
    for domain in priority:
        if scores.get(domain, 0) == best_score:
            return DomainClassification(
                kind=DomainResultKind.SINGLE, selected_domain=domain)
    return DomainClassification(kind=DomainResultKind.NONE)


def infer_domain(idea_text: str) -> str | None:
    """LEGACY compatibility wrapper over ``classify_domain`` (P9-E2-R 4/8).

    Total over ``SINGLE`` (-> selected domain string) and ``NONE`` (-> ``None``);
    it FAILS LOUD -- raising ``AmbiguousDomainResultError`` -- for the richer kinds
    ``AMBIGUOUS_TIE`` / ``MULTI_DOMAIN_NEEDS_D4`` that the ``str | None`` surface
    cannot represent. It NEVER returns ``None`` or an arbitrary domain for a richer
    kind (that would reintroduce the silent electronics-admission hazard). New
    production admission callers MUST use ``classify_domain`` and dispatch by
    ``kind``; this wrapper survives only for the frozen architecture-guardrail
    signature and legacy/test consumers that only ever encounter SINGLE/NONE."""
    result = classify_domain(idea_text)
    if result.kind is DomainResultKind.SINGLE:
        return result.selected_domain
    if result.kind is DomainResultKind.NONE:
        return None
    raise AmbiguousDomainResultError(
        f"infer_domain() cannot represent a {result.kind.value!r} result; callers "
        "must consume classify_domain() and dispatch by kind (P9-E2-R)."
    )
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
