"""W2-C / RVR-6b — intent-aware serving over the committed WS10 registries.

Authority: the authoritative W2-C/RVR-6b contract
(docs/governance/W2_C_RVR6B_IMPLEMENTATION_CONTRACT_CANDIDATE.md, PR #579)
under the exercised OD-W2-WS10-SCOPE decision (two per-domain registry
instances over the existing 21 committed ids through the unmodified
D11/D19 loader) and the separate Owner implementation-start authorization.

What this module owns (and only this):
  * per-domain access to the TWO committed WS10 question-intent registries
    (load-once, read-only, fail-closed — never a fabricated or partial
    registry; the loader itself is byte-unchanged);
  * the W2-C-authored, question-id-scoped, EN/AR-PAIRED intent marker sets
    for exactly the 21 committed ids (provenance: each committed question's
    own text + its registry intent record — every entry carries BOTH an
    English and an Arabic surface set, so intent coverage can never diverge
    by language);
  * the derived, deterministic, never-persisted INTENT-COVERAGE state of the
    current gap's committed variants;
  * the bounded intent-aware serving law (suppression + within-gap ordering)
    for the CURRENT canonical gap only;
  * the W1-N3 question-id-scoped supplemental relevance check consulted,
    fail-closed, by ``integrate_response`` when the governed family test
    (``gap_relevance.addresses_gap`` — the canonical relevance owner) says
    "not addressing".

Ownership boundaries (contract §F/§I — preserved, never duplicated):
  * ``select_next_gap`` remains the sole canonical gap-selection owner: this
    module NEVER chooses, promotes, reorders, opens, or skips a gap — it
    orders/suppresses committed question variants INSIDE the already-selected
    current gap only;
  * ``gap_relevance`` remains the canonical relevance owner: the supplement
    widens eligibility only for the variant actually displayed, never
    replaces or forks the family test;
  * FDC-001 / DecisionRecord remains the sole comparison/readiness owner:
    decision awareness here is READ-ONLY deference — while the W2-B
    alternatives transition is active the question slot is left canonical so
    the decision-evidence action block stays the one primary CTA;
  * the W2-B Option-C serving policy (register, four triggers, frozen
    W=2/M=2) is untouched; its question-slot overrides always win over this
    module (the composition precedence proposed in the implementation
    evidence pack);
  * WS11 (question-aware evaluation) stays dormant: intent coverage is a
    suppression/ordering input only — never an evaluation verdict, never
    SATISFIED, never gap completion (``evaluate_transition`` owns that), and
    never a user-facing progress claim.

Determinism / reconstruction: every public result is a pure function of the
canonical ``IdeaState`` (ledger + gaps) and committed content. Nothing is
persisted, no clock, no randomness, no process memory beyond the read-only
committed-registry cache. A reconstructed session recomputes identical
results because its inputs are exactly the restored canonical truth.

Fail-closed rule (contract §F.3): on ANY absence, malformation, unknown id,
load failure, or internal error, the public functions return the inert
result (``None`` / ``False``) and canonical serving proceeds unchanged.
Suppression can only ever occur on positive committed-marker evidence.

Registry path note (declared limitation): the ratified D8/D6 loader checks
compare the registry's committed ``source_artifact`` string against the
EXACT path string passed to ``load_question_intent_registry``. The committed
registries record repository-relative paths, so runtime loading succeeds
when the process working directory is the repository root (as in the test
suite and the governed web entrypoint); anywhere else the accessor fails
closed to canonical serving — a truthful degradation, never an error page.
"""
from dataclasses import dataclass
from pathlib import Path

# ---------------------------------------------------------------------------
# Committed per-domain registry instances (OD-W2-WS10-SCOPE — exercised).
# ---------------------------------------------------------------------------

_CONFIG_DIR = "docs/governance/path_n_content_config"

_DOMAIN_REGISTRY_FILES = {
    "electronics_electrical": (
        f"{_CONFIG_DIR}/electronics_electrical_question_intent_registry.json",
        f"{_CONFIG_DIR}/electronics_electrical_path_n_questions.json",
    ),
    "mechanical": (
        f"{_CONFIG_DIR}/mechanical_question_intent_registry.json",
        f"{_CONFIG_DIR}/mechanical_path_n_questions.json",
    ),
}

# Per-process read-only cache of successfully validated registries (mirrors
# the path_n_questions load-once pattern). A load FAILURE is deliberately NOT
# cached: a transient read problem must not disable W2-C for the process
# lifetime, and a permanent one keeps failing closed identically.
_REGISTRY_CACHE: dict = {}


def _load_registry(domain):
    """Return the domain's validated QuestionIntentRegistry, or None
    (fail-closed) when the domain has no committed registry or the committed
    registry/source pair does not validate through the unmodified loader."""
    if domain not in _DOMAIN_REGISTRY_FILES:
        return None
    if domain in _REGISTRY_CACHE:
        return _REGISTRY_CACHE[domain]
    try:
        from engine.question_intent_registry import load_question_intent_registry
        registry_rel, source_rel = _DOMAIN_REGISTRY_FILES[domain]
        registry = load_question_intent_registry(Path(registry_rel), Path(source_rel))
    except Exception:
        return None
    _REGISTRY_CACHE[domain] = registry
    return registry


# ---------------------------------------------------------------------------
# W2-C-authored, question-id-scoped, EN/AR-paired intent marker sets.
#
# Derivation (contract §F.1/§F.6 + Wave-2 §J): every entry derives from the
# committed question's OWN vocabulary (and, for mechanical:...:Q1's principle
# examples, the committed question's own example list). Family-wide additions
# remain PROHIBITED (the measured EN/AR differential-leak record inside
# engine/gap_relevance.py stands untouched); these sets are consulted ONLY
# (a) to mark a specific committed variant's intent as covered by recorded
# answers of the SAME gap, and (b) as the W1-N3 supplemental relevance test
# for the variant actually displayed. Every entry is EN/AR-paired by
# construction — a marker set with either surface empty would be a
# language-divergence defect (asserted by the W2-C tests).
# ---------------------------------------------------------------------------

_INTENT_MARKERS = {
    # electronics_electrical
    "N-MC-1": (("notice the problem", "would notice", "respond by", "responds by",
                "notices and", "and respond"),
               ("يلاحظ المشكلة", "يستجيب", "سيلاحظ")),
    "N-MC-2": (("main parts", "each part does", "part does"),
               ("الأجزاء الرئيسية", "كل جزء يقوم")),
    "N-MC-3": (("step by step", "sequence of events", "one step at a time"),
               ("خطوة بخطوة", "تسلسل الأحداث")),
    "N-MC-4": (("imagining loosely", "loosely imagined", "unclear how"),
               ("بشكل فضفاض", "غير واضح كيف")),
    "N-PF-1": (("work safely", "safe operation", "safely in the real world",
                "safety requirement"),
               ("يعمل بأمان", "متطلبات السلامة", "بأمان")),
    "N-PF-2": (("running reliably", "reliably over time"),
               ("بشكل موثوق مع الوقت", "يعمل بشكل موثوق")),
    "N-PF-3": (("environmental condition", "environmental conditions"),
               ("الظروف البيئية", "ظروف بيئية")),
    "N-PF-4": (("check first", "ask them to check", "verify first",
                "first thing to check"),
               ("يتحقق أولا", "التحقق أولا", "أول شيء يتم فحصه")),
    "N-BA-1": (("responsible for handling", "should handle", "in scope",
                "situations it handles"),
               ("مسؤول عن التعامل", "ضمن النطاق", "يتعامل معها")),
    "N-BA-2": (("someone else's job", "something else's job", "else's job",
                "not my system's job"),
               ("مهمة شخص آخر", "مهمة جهة أخرى", "ليست مهمته")),
    "N-BA-3": (("definitely react", "stay quiet", "should not react",
                "definitely respond"),
               ("يتفاعل بالتأكيد", "يبقى صامتا", "لا يتفاعل")),
    # mechanical
    "mechanical:MECHANISM_COMPLETENESS:Q1": (
        ("physical steps", "step is", "steps the mechanism", "in order the"),
        ("الخطوات المادية", "خطوات الآلية", "الخطوة الأولى")),
    "mechanical:MECHANISM_COMPLETENESS:Q2": (
        ("force path", "load path", "transfers force", "transfer force",
         "hinge line"),
        ("مسار القوة", "مسار الحمل", "نقل القوة", "خط المفصلة")),
    "mechanical:MECHANISM_COMPLETENESS:Q3": (
        ("each component", "overall motion", "component contributes"),
        ("كل مكون", "الحركة الكلية")),
    "mechanical:MECHANISM_COMPLETENESS:Q4": (
        ("missing detail", "would be missing", "no further explanation",
         "detail would be missing"),
        ("التفاصيل المفقودة", "سيكون مفقودا", "تفصيل مفقود")),
    "mechanical:PHYSICAL_FEASIBILITY:Q1": (
        ("physical principle", "principle it relies on",
         "relies on the principle"),
        ("مبدأ فيزيائي", "المبدأ الفيزيائي", "يعتمد على مبدأ")),
    "mechanical:PHYSICAL_FEASIBILITY:Q2": (
        ("force constraint", "material constraint", "must operate within",
         "load rating"),
        ("قيود القوة", "قيود المواد", "حد التحميل")),
    "mechanical:BOUNDARY_AMBIGUITY:Q1": (
        ("does not do", "not cover", "specifically not", "out of scope"),
        ("لا يقوم", "لا يغطي", "خارج النطاق")),
    "mechanical:BOUNDARY_AMBIGUITY:Q2": (
        ("mechanical boundary", "boundary is"),
        ("حد ميكانيكي", "الحد هو")),
    "mechanical:BOUNDARY_AMBIGUITY:Q3": (
        ("similar existing", "existing mechanical approach",
         "similar approach", "existing approach"),
        ("نهج مشابه", "أسلوب مشابه", "نهج قائم")),
    "mechanical:BOUNDARY_AMBIGUITY:Q4": (
        ("makes yours different", "different because", "concrete difference",
         "differs by", "physically different"),
        ("مختلف لأن", "الفرق المادي", "مختلف ماديا")),
}


def _matches_intent(text, question_id):
    """True when ``text`` carries the committed variant's intent vocabulary
    on EITHER paired surface (EN substring on the lowered text, or the Arabic
    surface verbatim). Pure, deterministic, fail-closed on unknown ids."""
    if not isinstance(text, str) or not text:
        return False
    entry = _INTENT_MARKERS.get(question_id)
    if entry is None:
        return False
    en_set, ar_set = entry
    lowered = text.lower()
    for marker in en_set:
        if marker in lowered:
            return True
    for marker in ar_set:
        if marker in text:
            return True
    return False


# ---------------------------------------------------------------------------
# Derived intent-coverage + the bounded serving law.
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class IntentServing:
    """Immutable W2-C serving result: the committed variant to display
    (identity + text read atomically from the committed artifact) and
    whether it differs from the canonical index-law variant."""
    question_id: str
    text: str
    design_gap_id: str
    adjusted: bool


def _gap_variants(domain, gap_type):
    """The current gap's committed variants, in committed artifact order.
    None when the domain/gap has no Path-N artifact mapping (Stage-3 or
    artifact-less domains — W2-C is inert there by construction)."""
    from engine.path_n_questions import get_served_question
    variants = []
    index = 0
    while True:
        served = get_served_question(gap_type, index, domain=domain)
        if served is None:
            return None if index == 0 else tuple(variants)
        if variants and served.question_id == variants[-1].question_id:
            return tuple(variants)  # clamp reached — list complete
        variants.append(served)
        index += 1


def _gap_answer_records(state, gap_type):
    """ACTIVE answered ledger records for this gap, in canonical rec_N order
    (exactly the W2-B canonical read pattern — composition, not a fork)."""
    from engine.adaptive_register import _record_seq
    from engine.idea_state import DISPOSITION_ANSWERED
    return sorted(
        (r for r in getattr(state, "assertions", [])
         if getattr(r, "superseded_by", None) is None
         and getattr(r, "disposition", None) == DISPOSITION_ANSWERED
         and getattr(r, "gap_context", None) == gap_type),
        key=lambda r: _record_seq(r.record_id))


def compute_intent_coverage(state, gap_type):
    """Derived per-variant intent-coverage for the current gap: the set of
    committed question_ids whose intent vocabulary is carried by at least
    one ACTIVE answered record of the SAME gap. Deterministic, never
    persisted, reversible (supersession recomputes). Returns None fail-closed
    when W2-C is inactive for this domain/gap (no registry, unknown ids, no
    artifact)."""
    domain = getattr(state, "domain", None)
    registry = _load_registry(domain)
    if registry is None:
        return None
    variants = _gap_variants(domain, gap_type)
    if not variants:
        return None
    try:
        for variant in variants:
            registry.get(variant.question_id)  # unknown id -> fail closed
    except Exception:
        return None
    records = _gap_answer_records(state, gap_type)
    covered = frozenset(
        variant.question_id for variant in variants
        if any(_matches_intent(record.content, variant.question_id)
               for record in records))
    return covered


def _effective(state, gap_type):
    """The W2-C serving law. Returns an IntentServing (always the variant the
    user should see, adjusted or not), or None when W2-C is inert for this
    render and canonical serving governs unchanged.

    Law (contract §F.3/§F.4, stateless and deterministic):
      * decision-aware deference (§F.5): while the W2-B alternatives
        transition is active, the question slot stays canonical — the
        decision-evidence action block is the primary CTA;
      * let c = the canonical index-law variant. If c's intent is NOT
        covered, serve c (inert — the asked question is still owed an
        answer);
      * if c IS covered, serve the next later uncovered variant (committed
        order); if none, the earliest uncovered variant (recovery of a
        missed intent); if every variant is covered, stay canonical — the
        governed clamp/reframe/exit machinery is the truthful path and is
        never overridden here.
    """
    domain = getattr(state, "domain", None)
    registry = _load_registry(domain)
    if registry is None:
        return None
    variants = _gap_variants(domain, gap_type)
    if not variants:
        return None
    try:
        for variant in variants:
            registry.get(variant.question_id)
    except Exception:
        return None
    try:
        from engine.progression_loop import _alternatives_crossing_context
        alternatives_active = _alternatives_crossing_context(state) is not None
    except Exception:
        alternatives_active = False
    gap = state.get_gap(gap_type) if hasattr(state, "get_gap") else None
    iterations_open = gap.iterations_open if gap is not None else 0
    canonical_index = min(iterations_open, len(variants) - 1)
    canonical = variants[canonical_index]
    if alternatives_active:
        return IntentServing(canonical.question_id, canonical.text,
                             canonical.design_gap_id, adjusted=False)
    records = _gap_answer_records(state, gap_type)
    covered = {
        variant.question_id for variant in variants
        if any(_matches_intent(record.content, variant.question_id)
               for record in records)}
    if canonical.question_id not in covered:
        return IntentServing(canonical.question_id, canonical.text,
                             canonical.design_gap_id, adjusted=False)
    for variant in variants[canonical_index + 1:]:
        if variant.question_id not in covered:
            return IntentServing(variant.question_id, variant.text,
                                 variant.design_gap_id, adjusted=True)
    for variant in variants[:canonical_index]:
        if variant.question_id not in covered:
            return IntentServing(variant.question_id, variant.text,
                                 variant.design_gap_id, adjusted=True)
    return IntentServing(canonical.question_id, canonical.text,
                         canonical.design_gap_id, adjusted=False)


def w2c_served_question(state, gap_type):
    """Public serving hook for the web session view: the ADJUSTED committed
    variant to display instead of the canonical one, or None when canonical
    serving stands (inert, deference, coverage-complete, or ANY failure —
    fail-closed, never an exception)."""
    try:
        serving = _effective(state, gap_type)
    except Exception:
        return None
    if serving is None or not serving.adjusted:
        return None
    return serving


def supplemental_relevance(state, gap_type, response):
    """W1-N3 bounded attempt (contract §E/§F.6): question-id-scoped
    supplemental relevance for the CANONICAL index-law variant of the served
    gap. Consulted by ``integrate_response`` only after the canonical family
    test said "not addressing"; True only on a positive committed-marker
    match (EN or the paired AR surface — identical outcome by construction).

    REPLAY-PARITY SCOPE RULE (deliberate, fail-closed): the scope is the
    canonical ``min(iterations_open, n-1)`` variant — NOT the W2-C-adjusted
    display — because reconstruction replays ``run_iteration`` over an
    initially EMPTY ledger (the durable ledger is restored verbatim AFTER
    the replay loop), so any ledger-dependent scope here would make live and
    replayed progression diverge (the W2-B ledger-less-replay lesson). The
    canonical scope depends only on committed content + the replay-faithful
    ``iterations_open``, so live and replay recompute identically. Whenever
    the display is unadjusted (including every historical journey and the
    measured W1-N3 case) the canonical variant IS the displayed variant;
    under an adjusted display the supplement deliberately stays with the
    canonical scope — a safe false-negative, never a false positive.

    Fail-closed False on any failure; NEVER weakens the canonical family
    test and never consults any other variant's markers."""
    try:
        domain = getattr(state, "domain", None)
        registry = _load_registry(domain)
        if registry is None:
            return False
        variants = _gap_variants(domain, gap_type)
        if not variants:
            return False
        for variant in variants:
            registry.get(variant.question_id)  # unknown id -> fail closed
        gap = state.get_gap(gap_type) if hasattr(state, "get_gap") else None
        iterations_open = gap.iterations_open if gap is not None else 0
        canonical = variants[min(iterations_open, len(variants) - 1)]
        return _matches_intent(response, canonical.question_id)
    except Exception:
        return False
