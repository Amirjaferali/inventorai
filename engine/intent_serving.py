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


# --------------------------------------------------------------------------
# T2-G (`T2G-VERSIONED-IMPLEMENT-01`) read-only seams.
#
# `_matches_intent` is UNCHANGED and stays the one committed-marker predicate;
# `matches_committed_intent` is a public alias so `engine/answer_stance.py`
# can be handed the matcher instead of importing a private name or
# reimplementing it. `supplemental_relevance` below keeps calling
# `_matches_intent` directly and keeps its exact replay-parity scope.
# --------------------------------------------------------------------------
def matches_committed_intent(text, question_id):
    """The unchanged committed-marker predicate, exposed for injection."""
    return _matches_intent(text, question_id)


def declared_variant_ids(state, gap_type):
    """This domain/gap's committed variant ids in committed order, or ``()``
    fail-closed when W2-C is inert here (no registry, no artifact, unknown
    id). Read-only; changes no serving decision."""
    try:
        domain = getattr(state, "domain", None)
        if _load_registry(domain) is None:
            return ()
        variants = _gap_variants(domain, gap_type)
        if not variants:
            return ()
        return tuple(variant.question_id for variant in variants)
    except Exception:
        return ()


def _t2g_covered(state, text, question_id, gap_type):
    """The ONE purpose-aware coverage helper used at BOTH coverage sites.

    Outside the T2-G version/gap/domain scope it returns exactly today's
    committed-marker result, so legacy projects, other gaps and other domains
    are untouched. Fail-closed to today's result on any error."""
    try:
        from engine import answer_stance
        return answer_stance.covers_variant(
            state, text, question_id, _matches_intent, gap_type=gap_type)
    except Exception:
        return _matches_intent(text, question_id)


# ---------------------------------------------------------------------------
# Derived intent-coverage + the bounded serving law.
# ---------------------------------------------------------------------------

#: Why an adjusted variant is served. ``coverage`` is the original W2-C law
#: (the canonical variant's intent is already covered); ``stated_unknown`` is
#: IDEA-GROUNDED-FUNCTIONAL-DEVELOPMENT-02 (the inventor said, in their own
#: words, that the part THIS variant asks about is not yet known).
BASIS_COVERAGE = "coverage"
BASIS_STATED_UNKNOWN = "stated_unknown"
#: After the stated-unknown variant was asked out of committed order, the
#: index law can point back at it; the journey then resumes at the earliest
#: committed variant not yet asked (never shown as chosen-for-the-unknown).
BASIS_RESUMED = "stated_unknown_resumed"


@dataclass(frozen=True)
class IntentServing:
    """Immutable W2-C serving result: the committed variant to display
    (identity + text read atomically from the committed artifact), whether it
    differs from the canonical index-law variant, and why (``basis``)."""
    question_id: str
    text: str
    design_gap_id: str
    adjusted: bool
    basis: str = BASIS_COVERAGE


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
        if any(_t2g_covered(state, record.content, variant.question_id,
                            gap_type)
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
      * IDEA-GROUNDED-FUNCTIONAL-DEVELOPMENT-02, evaluated before the two
        rules above: when the inventor's own explicit unknown (idea
        statement or an active answer of this gap) carries the committed
        intent markers of a knowledge-seeking variant that is uncovered,
        not routed and not yet asked, that variant is served (the first in
        committed order) — see ``_stated_unknown_focus``. When it is c
        itself, c is served unadjusted.
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
        if any(_t2g_covered(state, record.content, variant.question_id,
                            gap_type)
               for record in records)}
    # Safe Question Reduction Slice 1: a question whose need is routed to a
    # specialist / evidence is not eligible for Owner questioning, so W2-C
    # never adjusts the display to it (empty set without routing).
    from engine.need_routing import outstanding_routed_question_ids
    routed = outstanding_routed_question_ids(state, gap_type)
    # IDEA-GROUNDED-FUNCTIONAL-DEVELOPMENT-02: the inventor's own explicit
    # unknown points at ONE committed variant of this gap — serve it (once)
    # so the journey develops the part they said is not yet known. Fails
    # closed to the unchanged law below.
    try:
        matched = _stated_unknown_matches(state, gap_type, variants)
        asked = _asked_question_ids(state, gap_type) if matched else set()
        focus = _stated_unknown_focus(variants, matched, covered, routed, asked)
    except Exception:
        matched, asked, focus = frozenset(), set(), None
    # The stated-unknown variant was already asked out of committed order
    # and the index law now points back at it: do not ask it twice — resume
    # at the earliest committed variant not covered, routed or asked.
    if focus is None and canonical.question_id in matched \
            and canonical.question_id in asked \
            and canonical.question_id not in covered:
        for variant in variants:
            vid = variant.question_id
            if vid not in covered and vid not in routed and vid not in asked:
                return IntentServing(vid, variant.text, variant.design_gap_id,
                                     adjusted=True, basis=BASIS_RESUMED)
    if focus is not None:
        if focus.question_id == canonical.question_id:
            return IntentServing(canonical.question_id, canonical.text,
                                 canonical.design_gap_id, adjusted=False)
        return IntentServing(focus.question_id, focus.text,
                             focus.design_gap_id, adjusted=True,
                             basis=BASIS_STATED_UNKNOWN)
    if canonical.question_id not in covered:
        return IntentServing(canonical.question_id, canonical.text,
                             canonical.design_gap_id, adjusted=False)
    for variant in variants[canonical_index + 1:]:
        if variant.question_id not in covered \
                and variant.question_id not in routed:
            return IntentServing(variant.question_id, variant.text,
                                 variant.design_gap_id, adjusted=True)
    for variant in variants[:canonical_index]:
        if variant.question_id not in covered \
                and variant.question_id not in routed:
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


def committed_question_exists(domain, question_id):
    """True iff ``question_id`` is a record of THIS domain's committed, fully
    validated WS10 question-intent registry.

    Read-only presentation support (T2-B'): it lets the render edge confirm
    that an identity it already resolved from canonical state is backed by a
    committed registry record before any explanation is displayed, without
    duplicating the registry, exposing a record, or loading it a second time.
    It changes no serving decision and returns False on ANY failure — an
    unknown domain, a registry that does not validate, or an unknown id — so
    the caller fails closed to no explanation."""
    try:
        registry = _load_registry(domain)
        if registry is None:
            return False
        registry.get(question_id)
        return True
    except Exception:
        return False


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


# ---------------------------------------------------------------------------
# IDEA-GROUNDED-FUNCTIONAL-NEED-01 — the inventor's own explicit unknown,
# grounded in their idea statement or their answers, shown with the question
# that develops it (read-only, derived, never persisted).
#
# What this is: for the CURRENT canonical gap and the committed question the
# page serves, the inventor's own sentences that positively declare that a
# part of the idea is not yet known — recognised ONLY by the existing
# acknowledged-unknown detector (its registered English markers, its
# registered Arabic surfaces and its minimum length, unchanged) — read from
#   * the idea statement captured by the existing Level-0 seam
#     (``state.idea_summary``; the seed is never a ledger record), and
#   * the ACTIVE answered ledger records of the SAME gap (a superseded or
#     withdrawn answer is never read; a non-answer disposition is not an
#     answer);
# each tied to the gap it is shown with and to how far an EXISTING admitted
# mapping connects it to the served question:
#   QUESTION — the statement carries the served committed variant's own
#              EN/AR-paired intent markers (``_matches_intent``), the same
#              test the T2-G owner applies to decide that an explicit unknown
#              concerns THIS question's requested information;
#   GAP      — the inventor said it while this gap was being questioned
#              (provenance), or the statement carries the committed markers
#              of another variant of this gap, or the canonical relevance
#              owner (``gap_relevance.addresses_gap``) finds the gap's
#              governed intent vocabulary in it;
#   NONE     — no admitted mapping connects it: nothing is claimed.
# A NONE-bound idea-statement need is returned only before the inventor's
# first active answered record, so the idea's own unknown greets the first
# question(s) and then lives on only in the recorded-unknowns panel.
#
# What this is NOT: no component, sensor, control method, architecture or
# discipline is inferred; no new vocabulary, heuristic, normalisation or
# proposal carrier; no gap, maturity, progression, routing, evidence,
# readiness or serving decision changes; ``select_next_gap`` and the W2-C
# serving law above are untouched. Every result is a pure function of the
# canonical state plus committed content, so a reconstructed or resumed
# session recomputes it identically. Fail-closed: any failure yields the
# inert result (``None`` / ``()``) and the page renders exactly as before.
# ---------------------------------------------------------------------------

GROUNDED_SOURCE_IDEA = "idea"
GROUNDED_SOURCE_ANSWER = "answer"
GROUNDED_BINDING_QUESTION = "question"
GROUNDED_BINDING_GAP = "gap"
GROUNDED_BINDING_NONE = "none"


@dataclass(frozen=True)
class GroundedFunctionalNeed:
    """ONE inventor-stated unresolved part of the idea, as shown with the
    current question. ``statement`` is the inventor's own sentence verbatim
    (the existing detector's bounded fragment); ``basis`` is the registered
    marker or surface that recognised it (provenance, never shown as a
    claim); ``question_id`` is set only under a QUESTION binding."""
    source: str
    statement: str
    basis: str
    gap_type: str
    binding: str
    question_id: "str | None"


def idea_stated_unknown(state):
    """The inventor's explicit unknown inside their idea statement, as the
    ``(statement, basis)`` pair the existing detector recognises, or ``None``.

    Reads ``state.idea_summary`` — the statement the Level-0 seam captured
    verbatim, display-trimmed at a word boundary with a visible marker when
    very long: a sentence the trim cuts is shown cut, with that marker, and
    a sentence lying entirely past the cut is not read at all (the same
    trimmed statement on every replay, so live and reconstructed states
    agree; under-recognition is the direction of error). The detector's own
    bounds apply unchanged: an unregistered way of saying "I don't know", a
    statement shorter than its minimum length and the bare technical word
    "unknown" are not recognised. Fail-closed ``None``."""
    try:
        summary = getattr(state, "idea_summary", None)
        if not isinstance(summary, str) or not summary.strip():
            return None
        from engine.progression_loop import _detect_acknowledged_unknown
        unknown = _detect_acknowledged_unknown(summary, None, 0)
        if unknown is None:
            return None
        statement = unknown.verbatim.strip()
        if not statement or not isinstance(unknown.category_basis, str):
            return None
        return statement, unknown.category_basis
    except Exception:
        return None


def _binding_for(statement, gap_type, question_id, variant_ids, provenance):
    """The strongest EXISTING admitted connection between ``statement`` and
    the served question / gap. Positive evidence only."""
    if question_id is not None and _matches_intent(statement, question_id):
        return GROUNDED_BINDING_QUESTION
    if provenance:
        return GROUNDED_BINDING_GAP
    if any(_matches_intent(statement, vid) for vid in variant_ids
           if vid != question_id):
        return GROUNDED_BINDING_GAP
    from engine.gap_relevance import addresses_gap
    if addresses_gap(statement, gap_type):
        return GROUNDED_BINDING_GAP
    return GROUNDED_BINDING_NONE


def grounded_functional_needs(state, gap_type, question_id=None):
    """The inventor-stated unresolved parts of the idea to show with the
    question of ``gap_type`` that the page serves (``question_id`` is that
    served committed variant's id, or ``None`` when the ask is not a
    committed record). Idea-statement need first, then answer-time needs in
    canonical ledger order; identical statements appear once. ``()`` when
    there is nothing to show or on ANY failure (never an exception)."""
    try:
        if not isinstance(gap_type, str) or not gap_type:
            return ()
        if getattr(state, "domain", None) is None:
            return ()
        variant_ids = declared_variant_ids(state, gap_type)
        from engine.idea_state import DISPOSITION_ANSWERED
        # ANY gap (not `_gap_answer_records`, which is gap-scoped): the first
        # active answered record anywhere ends the idea's greeting phase.
        answered_any = any(
            getattr(r, "superseded_by", None) is None
            and getattr(r, "disposition", None) == DISPOSITION_ANSWERED
            for r in getattr(state, "assertions", []))
        needs = []
        for source, statement, basis in _stated_unknowns(state, gap_type):
            binding = _binding_for(statement, gap_type, question_id,
                                   variant_ids,
                                   provenance=source == GROUNDED_SOURCE_ANSWER)
            if source == GROUNDED_SOURCE_IDEA \
                    and binding == GROUNDED_BINDING_NONE and answered_any:
                continue
            needs.append(GroundedFunctionalNeed(
                source, statement, basis, gap_type, binding,
                question_id if binding == GROUNDED_BINDING_QUESTION else None))
        return tuple(needs)
    except Exception:
        return ()


def _stated_unknowns(state, gap_type):
    """``(source, statement, basis)`` for every inventor-stated explicit
    unknown relevant to ``gap_type``: the idea statement's (if any) first,
    then those inside ACTIVE answered records of this gap in canonical
    ledger order; an identical statement once. Recognition is the existing
    detector's alone. Raises on an unreadable ledger (callers fail closed)."""
    from engine.progression_loop import _detect_acknowledged_unknown
    found = []
    seen = set()
    idea = idea_stated_unknown(state)
    if idea is not None:
        found.append((GROUNDED_SOURCE_IDEA, idea[0], idea[1]))
        seen.add(idea[0])
    for record in _gap_answer_records(state, gap_type):
        content = getattr(record, "content", None)
        if not isinstance(content, str):
            continue
        unknown = _detect_acknowledged_unknown(content, gap_type, 0)
        if unknown is None:
            continue
        statement = unknown.verbatim.strip()
        if not statement or statement in seen:
            continue
        found.append((GROUNDED_SOURCE_ANSWER, statement, unknown.category_basis))
        seen.add(statement)
    return found


def _asked_question_ids(state, gap_type):
    """Committed question ids of this gap the inventor has already responded
    to — any ACTIVE record of the gap whose durable ``question_target`` names
    it (an answer, a non-answer, or a correction, which inherits its
    target). Replay-faithful: ``question_target`` is durable record truth."""
    asked = set()
    for record in getattr(state, "assertions", []):
        if getattr(record, "superseded_by", None) is not None \
                or getattr(record, "gap_context", None) != gap_type:
            continue
        target = getattr(record, "question_target", None)
        if isinstance(target, str) and target.startswith("PATHN:"):
            asked.add(target[len("PATHN:"):])
    return asked


def _stated_unknown_matches(state, gap_type, variants):
    """The knowledge-seeking committed variants of this gap whose EN/AR-paired
    intent markers an inventor-stated explicit unknown carries
    (``_matches_intent`` — the same admitted mapping the T2-G owner uses to
    decide that an unknown concerns THIS question's requested information).
    ``answer_stance.UNCERTAINTY_QUESTION_IDS`` are excluded: they ask the
    inventor to name an uncertainty, which the statement already does."""
    statements = [statement for _source, statement, _basis
                  in _stated_unknowns(state, gap_type)]
    if not statements:
        return frozenset()
    from engine.answer_stance import UNCERTAINTY_QUESTION_IDS
    return frozenset(
        variant.question_id for variant in variants
        if variant.question_id not in UNCERTAINTY_QUESTION_IDS
        and any(_matches_intent(statement, variant.question_id)
                for statement in statements))


def _stated_unknown_focus(variants, matched, covered, routed, asked):
    """IDEA-GROUNDED-FUNCTIONAL-DEVELOPMENT-02 — the committed variant of
    this gap that develops what the inventor said is not yet known, or None:
    the FIRST variant, in committed order, that a stated unknown matches
    (``_stated_unknown_matches``) and that is not covered by an answer of
    this gap, not an outstanding routed need and not yet asked
    (``_asked_question_ids``) — so it is served once, never repeated.
    Positive evidence only: no match, no focus. The statement is never an
    answer: it marks nothing covered and moves no state."""
    for variant in variants:
        vid = variant.question_id
        if vid in matched and vid not in covered and vid not in routed \
                and vid not in asked:
            return variant
    return None


def stated_unknown_serving(state, gap_type):
    """True when the variant the page serves for ``gap_type`` was chosen
    because of the inventor's stated unknown (read-only; False on any
    failure). The web layer uses the returned IntentServing's ``basis``
    directly; this is the same answer for callers without it."""
    serving = w2c_served_question(state, gap_type)
    return serving is not None and serving.basis == BASIS_STATED_UNKNOWN
