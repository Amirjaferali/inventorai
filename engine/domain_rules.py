"""
Domain Rules — lightweight electronics/electrical only.
MVP: 3 rules maximum per MVP_SCOPE_FREEZE.md
"""

import re

from engine.domain_registry import load_registry
from engine import domain_activation
_REGISTRY = load_registry("domains/")

from dataclasses import dataclass
from enum import Enum


# CF5-F003 corrective matching semantics (base corrective contract §4 + Amendment 01 §A3).
# Deterministic, domain-neutral, N-domain capable; consulted ONLY by classify_domain().
# Tokenizer: maximal ASCII-alphanumeric runs; punctuation/whitespace are delimiters
# (so "ESP32." / "(LED)" / "drug-delivery" -> "esp32" / "led" / "drug","delivery").
_TOKEN_RE = re.compile(r"[a-z0-9]+")


def _single_word_matches(sig_token, token_set):
    """§4.2/§4.3: a single-word signal matches an input token equal to it, or its
    bounded plural ``+"s"`` / ``+"es"`` -- and NOTHING else (no stemming / fuzzy /
    edit-distance / substring / ``+ies`` / irregular morphology)."""
    return (sig_token in token_set
            or (sig_token + "s") in token_set
            or (sig_token + "es") in token_set)


def _phrase_matches(sig_tokens, tokens):
    """§4.5: a multi-word signal matches only as a contiguous whole-token sequence;
    the bounded ``+"s"``/``+"es"`` plural is permitted on the FINAL token only. No
    token skipping, no reordering; intermediate tokens match exactly."""
    n = len(sig_tokens)
    last = sig_tokens[-1]
    for i in range(len(tokens) - n + 1):
        if all(tokens[i + j] == sig_tokens[j] for j in range(n - 1)):
            t = tokens[i + n - 1]
            if t == last or t == (last + "s") or t == (last + "es"):
                return True
    return False


def _present_signal_count(pack, tokens, token_set):
    """Number of DISTINCT registered signals of ``pack`` present in the tokenized
    text -- the domain's classification score. Computed as the cardinality of the
    UNION (Amendment 01 §A3, AT-MOST-ONCE / set membership) of:

      (i)  base matches -- signals matched by the whole-token + bounded-plural rule
           (single-word via exact/``+s``/``+es``; multi-word via contiguous token
           sequence with bounded plural on the final token); and
      (ii) same-domain registered containment -- every single-word registered signal
           ``X`` such that a registered container signal ``Y`` of the SAME pack is a
           BASE match (present via ANY authorized base form, incl. its bounded plural
           -- plural-container aware), with ``X != Y`` and ``X`` a substring of the
           registered signal string ``Y``.

    Each registered signal is counted at most once (a signal already base-matched is
    not re-credited via containment -- no double count). Containment is same-domain
    only (the loop is within one pack): no cross-domain leakage (e.g. electronics
    ``sensor`` is never credited from medical ``biosensor``); the container ``Y`` must
    be a registered signal (no credit inside a non-registered word, so
    ``controlled``/``knowledge``/``ecosystem`` never match); the contained ``X`` must
    be a registered same-domain single-word signal that is a substring of ``Y``. The
    containment credit never exceeds the single boolean contribution the same signal
    could have supplied through parent substring matching (Amendment 01 §A3a)."""
    base_present = set()
    single_word = {}  # registered single-word signal string -> its lone token
    for item in pack["classification_signals"]:
        sig = item["signal"].lower()
        sig_tokens = _TOKEN_RE.findall(sig)
        if not sig_tokens:
            continue
        if len(sig_tokens) == 1:
            single_word[sig] = sig_tokens[0]
            if _single_word_matches(sig_tokens[0], token_set):
                base_present.add(sig)
        else:
            if _phrase_matches(sig_tokens, tokens):
                base_present.add(sig)
    present = set(base_present)
    # (ii) same-domain registered containment, plural-container aware, at-most-once.
    # Container Y ranges over BASE matches only (containment is not itself chained);
    # X is a same-domain registered single-word signal that is a substring of Y.
    for y in base_present:
        for x_sig, _x_tok in single_word.items():
            if x_sig != y and x_sig in y:
                present.add(x_sig)
    return len(present)


class DomainResultKind(Enum):
    """The canonical domain-classification result kinds (P9-E2-R, extended by
    the CF5-F004 corrective contract §3.4).

    ``UNRESOLVED_NON_ACTIVATED_TIE`` (CF5-F004, merged contract PR #462): a
    ZERO-ACTIVATED top-score tie that the bounded legacy compatibility layer
    cannot resolve (it involves a non-legacy registered domain, or only
    non-legacy domains). Fail-closed: complete canonical candidate set, no
    winner, deterministic reason, NO activation requirement — deliberately
    DISTINCT from the P9-E2 ``AMBIGUOUS_TIE`` (whose activated-only invariant
    is untouched). ``MULTI_DOMAIN_NEEDS_D4`` is NOT reused for this case:
    equal-score evidence does not establish multi-domain composition, reuse
    would manufacture false D4 semantics, and the closed P9-E2 policy already
    rejects manufacturing that kind from equal-score evidence."""
    SINGLE = "single"
    NONE = "none"
    AMBIGUOUS_TIE = "ambiguous_tie"
    MULTI_DOMAIN_NEEDS_D4 = "multi_domain_needs_d4"
    UNRESOLVED_NON_ACTIVATED_TIE = "unresolved_non_activated_tie"


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
        else:  # AMBIGUOUS_TIE, MULTI_DOMAIN_NEEDS_D4 or UNRESOLVED_NON_ACTIVATED_TIE
            if self.selected_domain is not None:
                raise ValueError("a tie/multi result must not carry a selected winner")
            if len(cands) < 2:
                raise ValueError("a tie/multi result requires >= 2 candidates")
            if not all(c in _REGISTRY for c in cands):
                raise ValueError("all candidates must be registry-recognized")
            if not isinstance(self.reason, DomainAmbiguityReason):
                raise ValueError("a tie/multi result requires a deterministic reason code")
            if self.kind is DomainResultKind.AMBIGUOUS_TIE:
                # P9-E2-R invariant UNTOUCHED by CF5-F004: AMBIGUOUS_TIE stays
                # activated-only (D3-D); the zero-activated unresolved tie uses
                # its own kind above, which carries NO activation requirement.
                if not all(domain_activation.is_activated(c, _REGISTRY) for c in cands):
                    raise ValueError("all AMBIGUOUS_TIE candidates must be activated (D3-D)")



# DEPRECATED: authority moved to registry — Step 5 (AB-005). Remove in Step 7.

# CF5-F004 (merged contract §3.2; Owner OD2): the historical zero-activated
# precedence, preserved EXACTLY and ONLY as a bounded compatibility layer among
# these four legacy ids. It is a precedence order, NOT a membership gate: it is
# consulted solely when every top-tied domain is a legacy member, so it can
# never exclude, erase, or displace a newly registered domain.
_LEGACY_ZERO_ACTIVATED_PRECEDENCE = (
    "medical_device", "electronics_electrical", "mechanical", "software")
_LEGACY_ZERO_ACTIVATED_PRECEDENCE_SET = frozenset(_LEGACY_ZERO_ACTIVATED_PRECEDENCE)


def classify_domain(idea_text: str) -> "DomainClassification":
    """Canonical domain classifier (P9-E2-R representation seam; P9-E2 tie policy).
    The single source of classification truth (one classifier owner). It yields
    ``SINGLE`` / ``NONE`` and -- since P9-E2 -- ``AMBIGUOUS_TIE`` when TWO OR MORE
    ACTIVATED domains are equally top-scored (governed tie precedence: no winner,
    fail closed downstream). ``MULTI_DOMAIN_NEEDS_D4`` remains representable but is
    NOT produced here (D4 multi-domain composition is a separate, unexecuted gate).
    With the current real activation state (``electronics_electrical`` only) at most
    one domain is ever activated-tied, so the AMBIGUOUS_TIE branch is
    production-unreachable today; it becomes reachable only under a future governed
    second-domain activation (or a bounded self-restoring activation test double)."""
    tokens = _TOKEN_RE.findall(idea_text.lower())
    token_set = set(tokens)
    scores = {
        pack_id: _present_signal_count(pack, tokens, token_set)
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
    # 5-I2 activation policy; deterministic (sorted). Exactly one activated tied
    # domain yields SINGLE (unchanged); two or more is the governed P9-E2 tie.
    activated_tied = sorted(d for d in tied if domain_activation.is_activated(d, _REGISTRY))
    if len(activated_tied) == 1:
        # Case 1 (D3-D): a single activated domain among the tied set -> SINGLE.
        return DomainClassification(
            kind=DomainResultKind.SINGLE, selected_domain=activated_tied[0])
    if len(activated_tied) >= 2:
        # Case 3 (P9-E2 governed tie precedence): two or more ACTIVATED domains are
        # equally top-scored -> a genuine ambiguous tie with NO winner. There is no
        # arbitrary / alphabetical / registration / dict-order winner, no Electronics
        # preference, and no LLM tie-break. MULTI_DOMAIN_NEEDS_D4 is NOT manufactured
        # (deterministic equal-score evidence cannot distinguish a genuine
        # multi-domain need from ordinary equal-score ambiguity; D4 stays separate).
        # ``activated_tied`` is already sorted -> canonical order, NOT precedence.
        return DomainClassification(
            kind=DomainResultKind.AMBIGUOUS_TIE,
            candidates=tuple(activated_tied),
            reason=DomainAmbiguityReason.EQUAL_SCORE)
    # Case 0 (CF5-F004 corrective, merged contract §3; Owner D-CF5-F004-01):
    # zero-activated resolution derives candidate membership from the canonical
    # registry — the scored top-tied set itself — so NO hardcoded membership
    # list decides whether a registered domain can win (the prior 4-id literal
    # silently dropped an unlisted sole top scorer to NONE and silently awarded
    # a legacy member on a mixed tie: the validated F004 failure arms).
    if len(tied) == 1:
        # Arm A: a SOLE top-scoring registered domain is the truthful,
        # deterministic SINGLE result regardless of legacy-list membership
        # (a unique top score is the classifier's existing winner semantics,
        # not an invented precedence).
        return DomainClassification(
            kind=DomainResultKind.SINGLE, selected_domain=tied[0])
    # Legacy compatibility layer (OD2): the historical zero-activated
    # precedence medical_device > electronics_electrical > mechanical >
    # software survives ONLY as an explicit bounded order AMONG the legacy
    # four — reproducing today's outputs exactly for every current-registry
    # input — and can never exclude, erase, or displace a non-legacy
    # registered domain (it is consulted only when EVERY tied domain is a
    # legacy member).
    tied_set = set(tied)
    if tied_set <= _LEGACY_ZERO_ACTIVATED_PRECEDENCE_SET:
        for domain in _LEGACY_ZERO_ACTIVATED_PRECEDENCE:
            if domain in tied_set:
                return DomainClassification(
                    kind=DomainResultKind.SINGLE, selected_domain=domain)
    # Arm B: a zero-activated tie involving a non-legacy registered domain (or
    # only non-legacy domains) has no governed precedence — no winner may be
    # invented and no candidate silently erased (OD2). Fail closed with the
    # COMPLETE canonical candidate set; downstream consumers dispatch this
    # kind to their existing refusal/bounded-stop surfaces, and the legacy
    # infer_domain wrapper fails loud on it (its frozen contract).
    return DomainClassification(
        kind=DomainResultKind.UNRESOLVED_NON_ACTIVATED_TIE,
        candidates=tuple(sorted(tied)),
        reason=DomainAmbiguityReason.EQUAL_SCORE)


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


def get_substance_signal_plural_aliases(domain: str) -> dict:
    """L2SC-01 (docs/governance/L2SC01_SUBSTANCE_SIGNAL_PLURAL_ALIAS_INCREMENT_
    CONTRACT.md §5/§7): registry accessor mirroring `get_substance_signals`'s
    ownership pattern. Returns the requested domain's OWN explicit plural-alias
    map (``{alias: canonical_signal}``) — never merged, derived, or borrowed
    from another pack. An unknown domain or a pack with no
    `substance_signal_plural_aliases` field returns an empty dict (absence is
    valid and backward compatible)."""
    pack = _REGISTRY.get(domain)
    if pack:
        return dict(pack.get("substance_signal_plural_aliases", {}))
    return {}

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
