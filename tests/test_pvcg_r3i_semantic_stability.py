"""PVCG-R3-I — Semantic Stability: EN/AR governed equivalence.

Authority: docs/governance/PVCG_R3_C_SEMANTIC_STABILITY_CONTRACT.md
(AUTHORITATIVE, PR #551, merge 7b7aa2f1…).

WHAT THIS SUITE PROVES, AND WHAT IT DOES NOT
--------------------------------------------
It proves that inputs activating the SAME registered concept set for the served
gap produce the SAME §7.1 material progression outcome, in English or Arabic,
from the same authoritative starting state (§7.3). It proves NOTHING about
unregistered wording in either language — that residual is a declared KNOWN
BOUND (§7.4) and is asserted here explicitly rather than implied away.

COVERAGE ADEQUACY (§10.3 — the binding T-1 / T-1b lesson)
---------------------------------------------------------
Probes are generated from the DECLARED inventory
(``engine.semantic_registry.DECLARED_INVENTORY``), never from the live matcher
tables: a probe generated from the live table would vanish together with the
entry it is supposed to protect. Probe isolation is machine-validated and the
suite REFUSES AT COLLECTION if any probe is not isolated.
"""

import warnings

import pytest

from engine.idea_state import (
    IdeaState, Gap, OPEN,
    MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY,
    PROBLEM_MECHANISM_FIT, ASSUMPTION_INVENTORY, EXPERTISE_GAP_AWARENESS,
)
from engine.progression_loop import (
    integrate_response, assess_response, QUESTIONS,
    _detect_acknowledged_unknown, ASSERTED, REASONED,
)
from engine.gap_relevance import addresses_gap, _INTENT_WORDS, _INTENT_PHRASES
from engine.semantic_registry import (
    CONCEPTS, DECLARED_INVENTORY, CAUSAL_SURFACES,
    ACKNOWLEDGED_UNKNOWN_SURFACES, SUBSTANCE_SURFACES,
    activated_concepts, normalize_ar, WORD, PHRASE,
)
from web.result_feedback import get_result_feedback
from web.ui_text import localize_deep

DOMAIN = "mechanical"
GAPS = (MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY,
        PROBLEM_MECHANISM_FIT, ASSUMPTION_INVENTORY, EXPERTISE_GAP_AWARENESS)


# ---------------------------------------------------------------------------
# Helpers — no Flask, no I/O, no persistence, no network.
# ---------------------------------------------------------------------------
def _state():
    state = IdeaState(idea_id="pvcg-r3i", iteration=1, domain_signal=DOMAIN,
                      path="N")
    state.domain = DOMAIN
    return state


def _with_gap(gap_type, status=OPEN):
    state = _state()
    state.gaps.append(Gap(gap_type=gap_type, status=status, opened_at=1))
    return state


def _serve(state, gap_type, answer):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return integrate_response(state, gap_type, QUESTIONS[gap_type][0], answer)


def _quality(answer):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return assess_response(answer, DOMAIN)


def outcome(gap_type, answer):
    """The §7.1 ten-field material progression outcome, from a fresh state."""
    state = _with_gap(gap_type)
    gap0 = state.get_gap(gap_type)
    before_ev, before_unk = len(gap0.evidence), len(state.acknowledged_unknowns)
    transition, reason = _serve(state, gap_type, answer)
    gap = state.get_gap(gap_type)
    return (
        addresses_gap(answer, gap_type),                       # 1 eligibility
        _quality(answer),                                      # 2 quality tier
        transition,                                            # 3 transition
        get_result_feedback({"transition": transition,
                             "reason": reason}),               # 4 reason class
        gap.status,                                            # 5 gap status
        gap.closed_at is not None,                             # 6 closed_at
        len(gap.evidence) - before_ev,                         # 7 evidence delta
        state.known_mechanism is not None,                     # 8 known_mechanism
        state.known_problem is not None,                       # 9 known_problem
        len(state.acknowledged_unknowns) - before_unk,         # 10 unknown delta
    )


# Materially equivalent EN/AR pairs — one per governed gap. These are the D-1
# reproduction corpus and the §7.3 equivalence corpus.
PAIRS = {
 MECHANISM_COMPLETENESS: (
   "When the user presses the handle, the lever rotates and drives a spring-loaded "
   "latch, which opens the valve in three steps.",
   "عندما يضغط المستخدم على المقبض، تدور الذراع وتدفع مزلاجًا مزودًا بنابض، "
   "فيفتح الصمام على ثلاث خطوات."),
 PHYSICAL_FEASIBILITY: (
   "The mechanism relies on the physical principle of spring compression, and the "
   "power requirement is low because the lever converts hand force directly.",
   "تعتمد الآلية على مبدأ فيزيائي هو انضغاط النابض، ومتطلبات الطاقة منخفضة لأن "
   "الذراع تحول قوة اليد مباشرة."),
 BOUNDARY_AMBIGUITY: (
   "This invention does not cover powered actuation, and unlike existing designs "
   "the core lever cannot be replaced without losing the mechanism.",
   "هذا الاختراع لا يغطي التشغيل الكهربائي، وعلى خلاف التصاميم الموجودة فإن "
   "الذراع الأساسية لا يمكن استبدالها."),
 PROBLEM_MECHANISM_FIT: (
   "The problem is that users struggle to open the valve quickly, and this "
   "mechanism solves it rather than a powered pump because it needs no energy.",
   "المشكلة أن المستخدمين يعانون من صعوبة فتح الصمام بسرعة، وهذه الآلية تحل "
   "المشكلة بدلًا من مضخة كهربائية."),
 ASSUMPTION_INVENTORY: (
   "I am assuming the spring tension stays constant over time, and that "
   "assumption is untested, so the mechanism might fail if it is wrong.",
   "أفترض أن شدّ النابض يبقى ثابتًا مع الوقت، وهذا الافتراض غير مختبر، وقد "
   "تفشل الآلية إذا كان خاطئًا."),
 EXPERTISE_GAP_AWARENESS: (
   "Building this needs mechanical engineering expertise in spring design, and I "
   "would need to bring in a specialist because I lack that knowledge.",
   "يحتاج بناء هذا إلى خبرة في الهندسة الميكانيكية وتصميم النوابض، وسأحتاج إلى "
   "الاستعانة بأخصائي لأنني أفتقر لتلك المعرفة."),
}


# ---------------------------------------------------------------------------
# §15.1 — the reproduced defect, now closed. D-1 / D-2 / D-3 / D-4.
# ---------------------------------------------------------------------------
class TestD1EligibilityAndMaterialEquivalence:
    """D-1: eligibility diverged on 6/6 governed gaps at the base."""

    @pytest.mark.parametrize("gap", GAPS)
    def test_material_outcome_is_equal_for_the_governed_pair(self, gap):
        en, ar = PAIRS[gap]
        assert outcome(gap, en) == outcome(gap, ar), (
            "§7.3 violated for %s: the ten-field material progression outcome "
            "must be identical for governed-equivalent EN/AR inputs" % gap)

    @pytest.mark.parametrize("gap", GAPS)
    def test_both_languages_are_eligible(self, gap):
        en, ar = PAIRS[gap]
        assert addresses_gap(en, gap) is True
        assert addresses_gap(ar, gap) is True

    @pytest.mark.parametrize("concept", CONCEPTS, ids=[c.concept_id for c in CONCEPTS])
    def test_7_3_success_condition_over_registered_surface_pairs(self, concept):
        """§7.3 — the executable success condition, stated exactly as the
        contract defines it: for EVERY pair (x, y) of registered surfaces of a
        class, from the same starting state and the same served gap, all ten
        §7.1 fields are equal. This is a property of REGISTERED surfaces, not of
        hand-written sentence pairs.
        """
        probes = ["%s %s %s" % (_CARRIER[0], surface, _CARRIER[1])
                  for surface, _mode in concept.ar_surfaces + concept.en_surfaces]
        first = outcome(concept.owner, probes[0])
        for probe in probes[1:]:
            assert outcome(concept.owner, probe) == first, (
                "§7.3 violated inside %s: two registered surfaces of the same "
                "concept produce different material outcomes" % concept.concept_id)


class TestD2QualityCeiling:
    """D-2: an Arabic-only inventor could never close a gap. The decisive one."""

    MECH_EN = [
      "When the user presses the handle, the lever rotates and drives a spring-loaded latch, which opens the valve in three steps.",
      "The second component is a cam that converts rotation into linear travel, which then releases the latch.",
      "Once the latch releases, the spring pushes the piston and the valve opens fully in sequence.",
    ]
    MECH_AR = [
      "عندما يضغط المستخدم على المقبض، تدور الذراع وتدفع مزلاجًا مزودًا بنابض، فيفتح الصمام على ثلاث خطوات.",
      "المكوّن الثاني كامة تحول الدوران إلى حركة خطية، ثم تحرر المزلاج بعد ذلك مباشرة.",
      "بمجرد أن يتحرر المزلاج، يدفع النابض المكبس فينفتح الصمام بالكامل على التوالي.",
    ]

    def _trajectory(self, corpus):
        state = _with_gap(MECHANISM_COMPLETENESS)
        seen = []
        for i in range(8):
            state.iteration = i + 1
            _serve(state, MECHANISM_COMPLETENESS, corpus[i % len(corpus)])
            seen.append(state.get_gap(MECHANISM_COMPLETENESS).status)
        return seen

    def test_arabic_can_now_close_a_gap(self):
        assert "CLOSED" in self._trajectory(self.MECH_AR), (
            "D-2 regression: an Arabic-only inventor cannot advance a gap")

    def test_arabic_and_english_trajectories_match(self):
        assert self._trajectory(self.MECH_AR) == self._trajectory(self.MECH_EN)

    @pytest.mark.parametrize("answer", MECH_AR)
    def test_registered_arabic_mechanism_answers_reach_reasoned(self, answer):
        assert _quality(answer) == REASONED


class TestD3AcknowledgedUnknown:
    """D-3: the hidden side-effect track. unknown != satisfied/reasoned."""

    EN = "I do not know the exact spring tension that the latch will need in practice."
    AR = "لا أعرف قيمة شدّ النابض الدقيقة التي سيحتاجها المزلاج في الاستخدام الفعلي إطلاقًا."

    def test_arabic_unknown_is_now_recorded(self):
        got = _detect_acknowledged_unknown(self.AR, MECHANISM_COMPLETENESS, 1)
        assert got is not None
        assert got.category_basis, "a truthful category_basis is required"

    def test_english_unknown_still_recorded_unchanged(self):
        got = _detect_acknowledged_unknown(self.EN, MECHANISM_COMPLETENESS, 1)
        assert got is not None and got.category_basis == "i do not know"

    def test_unknown_is_never_satisfaction(self):
        """The epistemic invariant: unknown != reasoned != demonstrated."""
        for text in (self.EN, self.AR):
            assert _quality(text) == ASSERTED
        state = _with_gap(MECHANISM_COMPLETENESS)
        _serve(state, MECHANISM_COMPLETENESS, self.AR)
        assert state.get_gap(MECHANISM_COMPLETENESS).status != "CLOSED"
        assert state.known_mechanism is None or \
            state.known_mechanism.quality != REASONED

    def test_unknown_track_delta_is_equal_across_languages(self):
        def unknown_delta(text):
            state = _with_gap(MECHANISM_COMPLETENESS)
            _serve(state, MECHANISM_COMPLETENESS, text)
            return len(state.acknowledged_unknowns)
        assert unknown_delta(self.EN) == unknown_delta(self.AR) == 1


class TestD4DisclosureIsTruthful:
    """D-4: the not-addressed reason reached only the unknown-reason fallback."""

    FALLBACK = ("This point cannot move forward yet. Review the result details "
                "for the specific reason.")

    def test_not_addressed_reason_has_a_specific_classification(self):
        got = get_result_feedback({
            "transition": "WARN",
            "reason": "MECHANISM_COMPLETENESS not addressed — this answer does "
                      "not respond to the question that was asked"})
        assert got is not None and got != self.FALLBACK

    def test_the_disclosure_exists_in_both_supported_languages(self):
        """§8.1 — any wording R3 introduces must reach both UI languages."""
        english = get_result_feedback({
            "transition": "WARN",
            "reason": "MECHANISM_COMPLETENESS not addressed — this answer does "
                      "not respond to the question that was asked"})
        arabic = localize_deep(english, "ar")
        assert arabic != english, "the R3 disclosure is not localized to Arabic"
        assert localize_deep(english, "en") == english

    def test_disclosure_promises_no_understanding(self):
        english = get_result_feedback({
            "transition": "WARN", "reason": "X not addressed — y"}).lower()
        for overclaim in ("understand", "meaning", "translate", "any language"):
            assert overclaim not in english


# ---------------------------------------------------------------------------
# §10.2 — the ELEVEN mandatory adversarial categories.
# ---------------------------------------------------------------------------
class TestAdversarialCategories:

    def test_1_translation_collision_one_surface_two_families(self):
        """No Arabic surface may be reachable from two gap families."""
        owner_of = {}
        for cid, owner, surface, _mode in DECLARED_INVENTORY:
            prev = owner_of.get(surface)
            assert prev in (None, owner), (
                "translation collision: %r is registered to %s and %s"
                % (surface, prev, owner))
            owner_of[surface] = owner

    def test_2_synonym_collision_within_a_family_is_declared(self):
        """Two concepts in one family must not share an Arabic surface."""
        seen = {}
        for cid, owner, surface, _mode in DECLARED_INVENTORY:
            key = (owner, surface)
            assert key not in seen or seen[key] == cid, (
                "synonym collision: %r maps to both %s and %s"
                % (surface, seen[key], cid))
            seen[key] = cid

    def test_3_one_concept_has_exactly_one_owning_gap(self):
        for concept in CONCEPTS:
            assert concept.owner in GAPS
            assert sum(1 for c in CONCEPTS
                       if c.concept_id == concept.concept_id) == 1

    def test_4_technical_noun_off_topic_does_not_satisfy(self):
        """The Arabic analogue of the R2 `battery` surface question."""
        answer = "البطارية حمراء اللون."
        state = _with_gap(MECHANISM_COMPLETENESS)
        _serve(state, MECHANISM_COMPLETENESS, answer)
        assert state.get_gap(MECHANISM_COMPLETENESS).status != "CLOSED"
        assert state.known_mechanism is None

    def test_5_negation_is_characterised_not_worsened(self):
        """The English negated form is already eligible at the base; Arabic must
        not be made WORSE, and the truthful state is asserted, not hidden."""
        en = "It does not work by any steps."
        ar = "لا يعمل بأي خطوات."
        # Both carry a registered intent surface (EN 'steps' / AR 'خطوات'), so
        # both are eligible. R3 does not add negation semantics — that is R4.
        assert addresses_gap(en, MECHANISM_COMPLETENESS) is True
        assert addresses_gap(ar, MECHANISM_COMPLETENESS) is True

    def test_6_uncertainty_does_not_manufacture_closure(self):
        for text in ("I don't know how it works yet, honestly.",
                     "لا أعرف كيف يعمل هذا حتى الآن، بصراحة تامة."):
            state = _with_gap(MECHANISM_COMPLETENESS)
            _serve(state, MECHANISM_COMPLETENESS, text)
            assert state.get_gap(MECHANISM_COMPLETENESS).status != "CLOSED"

    def test_7_contradicted_statement_does_not_close(self):
        answer = ("الصمام يفتح دائمًا ولا يفتح أبدًا في نفس الوقت تمامًا.")
        state = _with_gap(MECHANISM_COMPLETENESS)
        _serve(state, MECHANISM_COMPLETENESS, answer)
        # R3 adds no contradiction engine (that is R4); it must simply not
        # manufacture closure from a self-contradicting single answer.
        assert state.get_gap(MECHANISM_COMPLETENESS).status != "CLOSED"

    @pytest.mark.parametrize("served", GAPS)
    def test_8_cross_gap_reuse_creates_no_off_diagonal_closure(self, served):
        """§16.1 — the property the repository ACTUALLY has: no off-diagonal
        CLOSURE and no off-diagonal SATISFACTION. Deliberately NOT a
        zero-eligibility requirement."""
        for owner, (_en, ar) in PAIRS.items():
            if owner == served:
                continue
            en = PAIRS[owner][0]

            def _off_diagonal(text):
                state = _with_gap(served)
                for _ in range(2):
                    _serve(state, served, text)
                gap = state.get_gap(served)
                return (gap.status == "CLOSED",
                        state.known_mechanism is not None,
                        state.known_problem is not None,
                        len(gap.evidence))

            ar_leak, en_leak = _off_diagonal(ar), _off_diagonal(en)
            assert ar_leak == en_leak, (
                "NEW off-diagonal leakage introduced by R3: serving the %s "
                "answer against %s behaves differently in Arabic (%r) than in "
                "English (%r). R3's obligation is NO NEW LEAKAGE measured "
                "differentially against the base; pre-existing English "
                "cross-talk is out of scope (R3-C §14 residual 1, §16.1)."
                % (owner, served, ar_leak, en_leak))

    def test_9_mixed_language_one_token_flip_is_characterised(self):
        """N-4 — mandatory because a single embedded English token flips an
        otherwise unregistered Arabic answer. Asserted, not discovered later."""
        unregistered_ar = "هذه الفكرة جميلة جدا وسوف تنال إعجاب الناس تقريبا."
        assert addresses_gap(unregistered_ar, MECHANISM_COMPLETENESS) is False
        assert addresses_gap(unregistered_ar + " steps",
                             MECHANISM_COMPLETENESS) is True

    def test_10_token_boundary_no_substring_bleed(self):
        """§9.3 — word surfaces match by TOKEN. A surface glued inside a longer
        Arabic token must NOT match, or Arabic clitics would over-match."""
        # 'خطوات' (steps) glued into a longer token must not activate MC-STEP.
        assert addresses_gap("زخطواتز", MECHANISM_COMPLETENESS) is False
        # The declared proclitic forms DO match — that is the intended bound.
        assert addresses_gap("بخطوات واضحة", MECHANISM_COMPLETENESS) is True
        assert addresses_gap("والخطوات واضحة", MECHANISM_COMPLETENESS) is True

    def test_11_empty_and_whitespace_are_not_eligible(self):
        for text in ("", "   ", "\t\n", " "):
            for gap in GAPS:
                assert addresses_gap(text, gap) is False


# ---------------------------------------------------------------------------
# §16 — the SEVEN binding negative controls.
# ---------------------------------------------------------------------------
class TestNegativeControls:

    def test_1_diagonal_behaviour_is_identical_across_languages(self):
        """The authoritative 6x6 CLOSURE control is
        ``tests/test_pvcg_r2i_gap_relevance.py::
        test_each_genuine_answer_closes_only_its_own_gap`` over its own curated
        GENUINE corpus, and it is reported GREEN on this candidate. Re-asserting
        that closure property here over a DIFFERENT corpus would assert
        something the authoritative base does not satisfy (§16.1). What R3 owes
        on the diagonal is that the two languages behave the SAME."""
        for served in GAPS:
            en, ar = PAIRS[served]

            def _diagonal(text):
                state = _with_gap(served)
                return [(_serve(state, served, text),
                         state.get_gap(served).status) for _ in range(3)]

            assert _diagonal(en) == _diagonal(ar), (
                "diagonal divergence on %s" % served)

    def test_2_unregistered_arabic_is_not_eligible(self):
        """'It is Arabic and technical, therefore accept' is a rejection
        condition."""
        for text in ("هذه الفكرة جميلة جدا وسوف تنال إعجاب الناس في كل مكان.",
                     "أعتقد أن الطقس اليوم جميل ومناسب للخروج مع العائلة."):
            for gap in GAPS:
                if activated_concepts(text, gap):
                    continue
                assert addresses_gap(text, gap) is False

    def test_3_unregistered_english_paraphrase_still_not_eligible(self):
        """N-3 — R3 must not accidentally widen English while adding Arabic."""
        paraphrase = ("Pushing the grip makes the arm swing round, which lets go "
                      "of the catch held by a coiled wire, so the flap swings wide.")
        assert addresses_gap(paraphrase, MECHANISM_COMPLETENESS) is False

    def test_4_empty_and_whitespace_not_eligible(self):
        for gap in GAPS:
            assert addresses_gap("", gap) is False
            assert addresses_gap("     ", gap) is False

    def test_5_off_topic_answer_to_served_gap_in_both_languages(self):
        en, ar = PAIRS[EXPERTISE_GAP_AWARENESS]
        assert addresses_gap(en, MECHANISM_COMPLETENESS) is False
        assert addresses_gap(ar, MECHANISM_COMPLETENESS) is False

    def test_6_near_miss_under_an_unauthorized_normalization(self):
        """A string differing from a registered surface by a fold §9.2 did NOT
        authorize (teh marbuta, yeh/alef-maqsura) must remain not eligible."""
        # Probes use the inert carrier so the ONLY candidate surface is the
        # near-miss itself. MC-STAGE registers مرحلة; the teh-marbuta variant
        # is NOT authorized to fold, so it must NOT match.
        assert addresses_gap(_probe_for("مرحله"), MECHANISM_COMPLETENESS) is False
        # PM-SOLVE registers يحل; the alef-maqsura near-miss must not match.
        assert addresses_gap(_probe_for("يحلى"), PROBLEM_MECHANISM_FIT) is False

    def test_7_registered_intent_without_causal_structure_stays_asserted(self):
        """An Arabic answer with an intent concept but NO registered causal
        structure must stay ASSERTED, exactly as its English counterpart."""
        ar = "الخطوات موجودة في هذا الجهاز الميكانيكي البسيط جدا بلا تفصيل."
        en = "The steps exist in this simple mechanical device without detail."
        assert _quality(ar) == ASSERTED
        assert _quality(en) == ASSERTED


# ---------------------------------------------------------------------------
# §10.3 — COVERAGE ADEQUACY. Probes generated from the DECLARED inventory.
# ---------------------------------------------------------------------------
# A neutral Arabic carrier containing NO registered surface of any family. If
# this ever stops being true the isolation validator below fails at collection.
_CARRIER = ("هذا", "فقط", "هنا")


#: An affix that appears in NO registered surface and is not a declared
#: proclitic, used to DISSOLVE a companion token while preserving a phrase
#: substring — the technique PVCG_R2_FORMAL_CLOSURE_RECORD.md §6 established
#: for the T-1b phrase→word containments ("zstep by stepz").
#: A DIGRAPH, not a single letter: no single Arabic letter is absent from every
#: registered surface (ز, for instance, occurs inside جزء), so a one-letter
#: affix could not carry the "appears in no surface" invariant below.
_DISSOLVE = "ظظ"


def _plain_probe(surface):
    return "%s %s %s" % (_CARRIER[0], surface, _CARRIER[1])


def _dissolved_probe(surface):
    """Keep the phrase as a SUBSTRING while dissolving its boundary tokens."""
    return "%s %s%s%s %s" % (_CARRIER[0], _DISSOLVE, surface, _DISSOLVE,
                             _CARRIER[1])


def _probe_for(surface):
    """The isolated probe for ``surface``.

    A registered PHRASE may properly contain a shorter registered WORD of the
    SAME family (e.g. متطلبات الطاقة contains طاقة). That is genuine same-family
    co-activation, not a defect — but it makes the plain probe non-isolated, so
    the coverage claim would be meaningless. The dissolved form preserves the
    phrase substring and breaks the companion token, exactly as the R2 marker
    suite does. A phrase→word containment is NEVER used to argue that the
    contained entry is non-operative — that argument is unsound (T-1b).
    """
    plain = _plain_probe(surface)
    return plain if _is_isolated(surface, plain) else _dissolved_probe(surface)


def _is_isolated(surface, probe):
    """True when ``probe`` activates at most the one concept owning ``surface``."""
    owners = {cid: owner for cid, owner, s, _m in DECLARED_INVENTORY if s == surface}
    if len(owners) != 1:
        return False
    concept_id, owner = next(iter(owners.items()))
    if activated_concepts(probe, owner) != frozenset({concept_id}):
        return False
    return all(not activated_concepts(probe, other)
               for other in GAPS if other != owner)


def _isolation_report(concept_id, owner, surface):
    """Return None when the probe is isolated, else the reason it is not."""
    probe = _probe_for(surface)
    own = activated_concepts(probe, owner)
    if own != frozenset({concept_id}):
        return ("probe for %s activates %s in its own family, expected exactly "
                "{%s}" % (surface, sorted(own), concept_id))
    for other in GAPS:
        if other == owner:
            continue
        foreign = activated_concepts(probe, other)
        if foreign:
            return ("probe for %s leaks into %s via %s"
                    % (surface, other, sorted(foreign)))
    return None


def _collection_guard():
    """§10.3 — REFUSE AT COLLECTION if any generated probe is not isolated."""
    problems = [r for r in
                (_isolation_report(cid, owner, surface)
                 for cid, owner, surface, _mode in DECLARED_INVENTORY)
                if r is not None]
    return problems


_ISOLATION_PROBLEMS = _collection_guard()


def test_carrier_is_itself_inert():
    """Validator self-test: the carrier alone must activate nothing anywhere."""
    for gap in GAPS:
        assert activated_concepts(" ".join(_CARRIER), gap) == frozenset()
        assert addresses_gap(" ".join(_CARRIER), gap) is False


def test_dissolving_affix_is_itself_inert():
    """Validator self-test: the dissolving affix must not create or suppress a
    match on its own, and must not be a declared proclitic."""
    from engine.semantic_registry import _AR_PROCLITICS
    assert _DISSOLVE not in _AR_PROCLITICS
    for gap in GAPS:
        assert addresses_gap("%s %s %s" % (_CARRIER[0], _DISSOLVE, _CARRIER[1]),
                             gap) is False
    for _cid, _owner, surface, _mode in DECLARED_INVENTORY:
        assert _DISSOLVE not in surface, (
            "the dissolving affix appears in registered surface %r" % surface)


def test_probes_requiring_dissolution_are_declared():
    """Auditable: exactly which surfaces needed the dissolved form, and why."""
    needed = sorted(surface for _c, _o, surface, _m in DECLARED_INVENTORY
                    if not _is_isolated(surface, _plain_probe(surface)))
    for surface in needed:
        assert " " in surface, (
            "only multi-word PHRASE surfaces may require dissolution; %r is not "
            "a phrase, so its non-isolation is a real collision" % surface)
        assert _is_isolated(surface, _dissolved_probe(surface)), (
            "%r is not isolable even when dissolved" % surface)


def test_every_generated_probe_is_isolated():
    """Collection-time adequacy guard (§10.3). A non-isolated probe would make
    the coverage claim below meaningless, so it fails loudly instead."""
    assert _ISOLATION_PROBLEMS == [], _ISOLATION_PROBLEMS


@pytest.mark.parametrize(
    "concept_id,owner,surface,mode",
    DECLARED_INVENTORY,
    ids=["%s:%s" % (c, s) for c, _o, s, _m in DECLARED_INVENTORY])
def test_declared_surface_is_operative(concept_id, owner, surface, mode):
    """One machine-isolated POSITIVE probe per declared Arabic surface.

    Generated from the DECLARED inventory, so deleting the surface from the
    live table leaves this probe in place to FAIL — the T-1 lesson.
    """
    probe = _probe_for(surface)
    assert addresses_gap(probe, owner) is True, (
        "declared surface %r of %s is NOT operative" % (surface, concept_id))
    assert concept_id in activated_concepts(probe, owner)


@pytest.mark.parametrize(
    "concept_id,owner,surface,mode",
    DECLARED_INVENTORY,
    ids=["%s:%s" % (c, s) for c, _o, s, _m in DECLARED_INVENTORY])
def test_declared_surface_has_cross_family_exclusivity(concept_id, owner,
                                                       surface, mode):
    """The same probe must activate NOTHING in the other five families."""
    probe = _probe_for(surface)
    for other in GAPS:
        if other == owner:
            continue
        assert addresses_gap(probe, other) is False, (
            "%r (owned by %s) also satisfies %s" % (surface, owner, other))


# ---------------------------------------------------------------------------
# §6 — deterministic mechanism constraints, and the prohibitions.
# ---------------------------------------------------------------------------
class TestDeterminismAndProhibitions:

    @pytest.mark.parametrize("gap", GAPS)
    def test_decision_is_deterministic_over_repetitions(self, gap):
        _en, ar = PAIRS[gap]
        first = outcome(gap, ar)
        for _ in range(11):
            assert outcome(gap, ar) == first

    def test_no_prohibited_subsystem_is_imported(self):
        """§6.2 — stated as a fact of the delivered code, not as a promise."""
        import inspect
        import engine.semantic_registry as module
        source = inspect.getsource(module).lower()
        for banned in ("import requests", "import urllib", "import socket",
                       "openai", "anthropic", "transformers", "torch",
                       "numpy", "sklearn", "embedding", "vector store",
                       "http://", "https://", "random.", "datetime.now",
                       "time.time", "open("):
            assert banned not in source, (
                "prohibited construct %r present in the R3 registry" % banned)

    def test_registry_depends_only_on_stdlib_re_and_unicodedata(self):
        import engine.semantic_registry as module
        imported = [n for n in ("re", "unicodedata") if hasattr(module, n)]
        assert imported == ["re", "unicodedata"]

    def test_every_concept_carries_all_five_contract_fields(self):
        """§5.1 — a concept with no governed-question provenance must not exist."""
        for c in CONCEPTS:
            assert c.concept_id and c.owner in GAPS and c.provenance
            assert c.en_surfaces and c.ar_surfaces
            for _surface, mode in c.ar_surfaces + c.en_surfaces:
                assert mode in (WORD, PHRASE)


class TestEnglishIsNotWidened:
    """§16.3 — R3 must not widen English by even one token."""

    def test_every_registered_english_surface_already_existed(self):
        for c in CONCEPTS:
            for surface, mode in c.en_surfaces:
                if mode == WORD:
                    assert surface in _INTENT_WORDS[c.owner], (
                        "%s registers NEW English word %r — R3 may not widen "
                        "English" % (c.concept_id, surface))
                else:
                    assert surface in _INTENT_PHRASES.get(c.owner, ()), (
                        "%s registers NEW English phrase %r" % (c.concept_id, surface))


class TestNormalizationBoundary:
    """§9.2 — authorized transformations only; the rest must NOT happen."""

    def test_nfc_is_applied(self):
        import unicodedata
        decomposed = unicodedata.normalize("NFD", "خطوات")
        assert normalize_ar(decomposed) == normalize_ar("خطوات")

    def test_tatweel_removal_is_necessary_and_applied(self):
        assert addresses_gap("هذا خطــوات فقط", MECHANISM_COMPLETENESS) is True

    def test_harakat_removal_is_necessary_and_applied(self):
        assert addresses_gap("هذا خَطَوَاتٌ فقط", MECHANISM_COMPLETENESS) is True

    def test_alef_folding_is_necessary_and_applied(self):
        assert addresses_gap("هذا أفترض فقط", ASSUMPTION_INVENTORY) is True

    def test_teh_marbuta_is_NOT_folded(self):
        """NOT authorized by §9.2 — folding it would be a lossy collapse."""
        assert normalize_ar("مرحلة") != normalize_ar("مرحله")

    def test_yeh_and_alef_maqsura_are_NOT_folded(self):
        assert normalize_ar("يحل") != normalize_ar("يحلى")

    def test_arabic_indic_digits_are_NOT_folded(self):
        assert normalize_ar("٣") != "3"

    def test_hamza_carriers_keep_their_letter_identity(self):
        """A blanket combining-mark strip would rewrite ئ→ي and ؤ→و, which is a
        letter fold §9.2 does not authorize."""
        assert normalize_ar("مبادئ") == "مبادئ"
        assert normalize_ar("مسؤول") == "مسؤول"

    def test_latin_normalization_is_not_added(self):
        """§9.1 — N-1 measured English already stable; R3 adds nothing."""
        assert normalize_ar("Step BY step") == "Step BY step"
