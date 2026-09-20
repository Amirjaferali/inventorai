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
Coverage probes come from ``tests/fixtures/pvcg_r3i_frozen_expectations.py``,
a FROZEN corpus of literal committed data that imports nothing from the object
under test. It does not shrink when a runtime entry is deleted, so a deletion
leaves the expectation standing and the assertion goes RED.

The previous candidate (1ce9ef34, REJECTED) parametrized these probes over
``DECLARED_INVENTORY``, which is derived from ``CONCEPTS`` at import — so
deleting a surface deleted its own test case and the suite stayed GREEN while
real behaviour was lost (measured: focused 453 -> 451 and full 4229 -> 4227,
both with ZERO failures). That was defect B-2 and this file no longer relies on
that pattern for adequacy. ``DECLARED_INVENTORY`` is still used for the §7.3
equivalence sweep and the isolation helpers, which are not adequacy oracles.
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
    has_registered_causal_structure, substance_surface_present,
    detect_registered_unknown,
)
from engine.domain_rules import get_substance_signals
from tests.fixtures.pvcg_r3i_frozen_expectations import (
    EXPECTED_SURFACES, CONCEPT, CAUSAL, UNKNOWN, SUBSTANCE,
    PATH_N_PF_PAIRING,
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
        probes = [_probe_for(surface)
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

    def test_the_t2g_explicit_unknown_reason_has_its_own_classification(self):
        """T2-G (`T2G-VERSIONED-IMPLEMENT-01`): saying you do not know something
        IS a response, so the recognized-unknown reason must never fall into
        the "not addressed" category, and must not reach the vague fallback."""
        reason = ("MECHANISM_COMPLETENESS recorded as an explicit unknown — "
                  "this answer states the information is not known yet and "
                  "supplies no mechanism explanation")
        got = get_result_feedback({"transition": "WARN", "reason": reason})
        assert got is not None and got != self.FALLBACK
        not_addressed = get_result_feedback({
            "transition": "WARN",
            "reason": "MECHANISM_COMPLETENESS not addressed — this answer does "
                      "not respond to the question that was asked"})
        assert got != not_addressed
        lowered = got.lower()
        assert "has been saved" in lowered
        # it never implies the statement was lost, irrelevant or validated
        for overclaim in ("lost", "irrelevant", "verified", "validated",
                          "incorrect", "wrong"):
            assert overclaim not in lowered
        arabic = localize_deep(got, "ar")
        assert arabic != got, "the T2-G reason is not localized to Arabic"
        assert localize_deep(got, "en") == got

    def test_the_t2g_reason_disclosure_promises_no_understanding(self):
        english = get_result_feedback({
            "transition": "WARN",
            "reason": "X recorded as an explicit unknown — y"}).lower()
        for overclaim in ("understand", "meaning", "translate", "any language"):
            assert overclaim not in english

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
        # N-3 repair: this control previously did `if activated_concepts(...):
        # continue`, so it skipped exactly the cases it named and could never
        # fail. The أعتقد sentence is now asserted explicitly against the
        # accepted mirrored-breadth truth instead of being silently skipped.
        for text in ("هذه الفكرة جميلة جدا وسوف تنال إعجاب الناس في كل مكان.",
                     "سوف اعمل على هذا المشروع في وقت لاحق عندما تتوفر الفرصة."):
            for gap in GAPS:
                assert addresses_gap(text, gap) is False, (
                    "unregistered Arabic prose became eligible for %s" % gap)
        # Carries اعتقد, a registered surface mirroring the PRE-EXISTING English
        # marker `believe`. Eligible in BOTH languages by design (§14 residual
        # 1) — asserted, not skipped.
        mirrored = "أعتقد أن الطقس اليوم جميل ومناسب للخروج مع العائلة."
        assert addresses_gap(mirrored, ASSUMPTION_INVENTORY) is True
        for gap in GAPS:
            if gap != ASSUMPTION_INVENTORY:
                assert addresses_gap(mirrored, gap) is False

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

    def test_8_pre_existing_english_breadth_is_MIRRORED_not_narrowed(self):
        """Creator-Grill finding, disclosed rather than concealed.

        `believe` and `expect` are PRE-EXISTING English ASSUMPTION_INVENTORY
        intent markers, so ordinary English prose containing them is already
        eligible at the authoritative base — §14 residual 1 (English lexical
        breadth), which R3 must NOT reopen. Their registered Arabic surfaces
        (اعتقد / اتوقع) therefore mirror that breadth EXACTLY.

        Making the Arabic side stricter than the English side would CREATE a
        new EN/AR divergence — precisely the defect R3 exists to remove — so
        the mirrored breadth is the correct behaviour, not a leak. It is pinned
        here so the limitation is visible in the test record.
        """
        prose = [
            ("I believe the weather today is nice and suitable for going out.",
             "أعتقد أن الطقس اليوم جميل ومناسب للخروج مع العائلة والأصدقاء."),
            ("I expect the weather to be fine tomorrow for the family trip.",
             "أتوقع أن يكون الطقس جميلا غدا من أجل رحلة العائلة."),
        ]
        for en, ar in prose:
            assert addresses_gap(en, ASSUMPTION_INVENTORY) is True
            assert addresses_gap(ar, ASSUMPTION_INVENTORY) == \
                addresses_gap(en, ASSUMPTION_INVENTORY), (
                    "Arabic must mirror the pre-existing English breadth, "
                    "neither widening nor narrowing it")

    def test_7_registered_intent_without_causal_structure_stays_asserted(self):
        """An Arabic answer with an intent concept but NO registered causal
        structure must stay ASSERTED, exactly as its English counterpart."""
        ar = "الخطوات موجودة في هذا الجهاز الميكانيكي البسيط جدا بلا تفصيل."
        en = "The steps exist in this simple mechanical device without detail."
        assert _quality(ar) == ASSERTED
        assert _quality(en) == ASSERTED


# ---------------------------------------------------------------------------
# §10.3 — COVERAGE ADEQUACY, driven by the FROZEN INDEPENDENT CORPUS.
# ---------------------------------------------------------------------------
# Independent External Review REJECTED candidate 1ce9ef34 on defect B-2: the
# probes were parametrized over DECLARED_INVENTORY, which is derived from
# CONCEPTS at import. Deleting a registered surface deleted its own test case,
# so the suite stayed GREEN while real behaviour was lost (measured: focused
# 453 -> 451 and full 4229 -> 4227, both with ZERO failures).
#
# The oracle now comes from tests/fixtures/pvcg_r3i_frozen_expectations.py,
# which imports NOTHING from the object under test. A deleted runtime entry
# leaves its expectation standing, so the assertion goes RED. The parity test
# below keeps the two in sync in BOTH directions, so a silently ADDED runtime
# surface with no frozen expectation fails just as loudly.

# A neutral Arabic carrier containing NO registered surface of any family, and
# a dissolving affix absent from every registered surface. Used by the §7.3
# equivalence sweep and the near-miss controls. NOT the coverage-adequacy
# oracle — that is the frozen corpus below.
_CARRIER = ("هذا", "فقط", "هنا")
_DISSOLVE = "ظظ"


def _plain_probe(surface):
    return "%s %s %s" % (_CARRIER[0], surface, _CARRIER[1])


def _dissolved_probe(surface):
    return "%s %s%s%s %s" % (_CARRIER[0], _DISSOLVE, surface, _DISSOLVE,
                             _CARRIER[1])


def _is_isolated(surface, probe):
    owners = {cid: owner for cid, owner, sfc, _m in DECLARED_INVENTORY
              if sfc == surface}
    if len(owners) != 1:
        return False
    concept_id, owner = next(iter(owners.items()))
    if activated_concepts(probe, owner) != frozenset({concept_id}):
        return False
    return all(not activated_concepts(probe, other)
               for other in GAPS if other != owner)


def _probe_for(surface):
    plain = _plain_probe(surface)
    return plain if _is_isolated(surface, plain) else _dissolved_probe(surface)


def test_carrier_and_dissolving_affix_are_inert():
    """Validator self-test for the helpers above."""
    for gap in GAPS:
        assert addresses_gap(" ".join(_CARRIER), gap) is False
        assert addresses_gap("%s %s %s" % (_CARRIER[0], _DISSOLVE,
                                           _CARRIER[1]), gap) is False
    for _c, _o, surface, _m in DECLARED_INVENTORY:
        assert _DISSOLVE not in surface


_BY_CLASS = {}
for _row in EXPECTED_SURFACES:
    _BY_CLASS.setdefault(_row[0], []).append(_row)

_CONCEPT_ROWS = tuple(_BY_CLASS[CONCEPT])
_CAUSAL_ROWS = tuple(_BY_CLASS[CAUSAL])
_UNKNOWN_ROWS = tuple(_BY_CLASS[UNKNOWN])
_SUBSTANCE_ROWS = tuple(_BY_CLASS[SUBSTANCE])


def test_frozen_corpus_is_independent_of_the_object_under_test():
    """The oracle must not import the matcher it is supposed to police."""
    import ast
    import inspect
    import tests.fixtures.pvcg_r3i_frozen_expectations as frozen
    tree = ast.parse(inspect.getsource(frozen))
    imports = [node for node in ast.walk(tree)
               if isinstance(node, (ast.Import, ast.ImportFrom))]
    assert imports == [], (
        "the frozen corpus must contain no import statement; found %d"
        % len(imports))


def test_frozen_corpus_and_live_registry_agree_in_both_directions():
    """Deletion AND silent addition both fail here."""
    frozen_concept = {(r[1], r[2], r[3], r[4]) for r in _CONCEPT_ROWS}
    live_concept = {(c.concept_id, c.owner, surface, mode)
                    for c in CONCEPTS for surface, mode in c.ar_surfaces}
    assert frozen_concept == live_concept, (
        "concept surfaces drifted; missing from live=%s, unexpected in live=%s"
        % (sorted(frozen_concept - live_concept),
           sorted(live_concept - frozen_concept)))

    frozen_causal = {(r[3], r[4]) for r in _CAUSAL_ROWS}
    live_causal = {(surface, mode) for surface, mode, _m in CAUSAL_SURFACES}
    assert frozen_causal == live_causal, (
        "causal surfaces drifted; missing=%s, unexpected=%s"
        % (sorted(frozen_causal - live_causal),
           sorted(live_causal - frozen_causal)))

    frozen_unknown = {r[3] for r in _UNKNOWN_ROWS}
    live_unknown = {surface for surface, _m in ACKNOWLEDGED_UNKNOWN_SURFACES}
    assert frozen_unknown == live_unknown

    frozen_substance = {(r[2], r[1], r[3]) for r in _SUBSTANCE_ROWS}
    live_substance = {(domain, signal, surface)
                      for domain, sigmap in SUBSTANCE_SURFACES.items()
                      for signal, surfaces in sigmap.items()
                      for surface in surfaces}
    assert frozen_substance == live_substance


@pytest.mark.parametrize("row", _CONCEPT_ROWS,
                         ids=["%s:%s" % (r[1], r[3]) for r in _CONCEPT_ROWS])
def test_frozen_concept_surface_is_operative(row):
    _cls, concept_id, owner, surface, _mode, probe = row
    assert addresses_gap(probe, owner) is True, (
        "frozen concept surface %r of %s is NOT operative" % (surface, concept_id))
    assert concept_id in activated_concepts(probe, owner)


@pytest.mark.parametrize("row", _CONCEPT_ROWS,
                         ids=["%s:%s" % (r[1], r[3]) for r in _CONCEPT_ROWS])
def test_frozen_concept_surface_is_cross_family_exclusive(row):
    _cls, _cid, owner, surface, _mode, probe = row
    for other in GAPS:
        if other == owner:
            continue
        assert addresses_gap(probe, other) is False, (
            "%r (owned by %s) also satisfies %s" % (surface, owner, other))


@pytest.mark.parametrize("row", _CAUSAL_ROWS,
                         ids=[r[3] for r in _CAUSAL_ROWS])
def test_frozen_causal_surface_is_operative(row):
    _cls, mirror, _scope, surface, _mode, probe = row
    assert has_registered_causal_structure(probe) is True, (
        "frozen causal surface %r (mirrors %r) is NOT operative"
        % (surface, mirror))


@pytest.mark.parametrize("row", _UNKNOWN_ROWS,
                         ids=[r[3] for r in _UNKNOWN_ROWS])
def test_frozen_unknown_surface_is_operative(row):
    _cls, mirror, _scope, surface, _mode, probe = row
    assert detect_registered_unknown(probe) is not None, (
        "frozen unknown surface %r (mirrors %r) is NOT operative"
        % (surface, mirror))


@pytest.mark.parametrize("row", _SUBSTANCE_ROWS,
                         ids=["%s:%s" % (r[1], r[3]) for r in _SUBSTANCE_ROWS])
def test_frozen_substance_surface_is_operative(row):
    _cls, signal, domain, surface, _mode, probe = row
    assert substance_surface_present(probe, domain) is True, (
        "frozen substance surface %r for signal %r is NOT operative"
        % (surface, signal))


def test_every_substance_surface_maps_to_a_committed_pack_signal():
    """R3 adds NO new substance concept — one-to-one with the packs (§5.4)."""
    for _cls, signal, domain, _surface, _mode, _probe in _SUBSTANCE_ROWS:
        assert signal in set(get_substance_signals(domain)), (
            "%r is not a committed pack signal of %s" % (signal, domain))


# ---------------------------------------------------------------------------
# B-1 — Arabic causal surfaces must not fire from inside an unrelated word.
# ---------------------------------------------------------------------------
class TestCausalTokenBoundary:
    """Independent External Review defect B-1, repaired and pinned.

    A raw substring rule let the 2-character surface `ثم` fire from inside
    ordinary words (`ثمن` price, `عثمان` a name, `ثمانية` eight, `استثمار`
    investment). Measured consequence at the rejected candidate: an Arabic
    answer whose only qualifying token was the noun `ثمن` reached REASONED and
    CLOSED the gap, while the same sentence with the synonym `سعر` and the
    faithful English counterpart both stayed ASSERTED / PARTIAL.
    """

    BLEED = ["ثمن", "الثمن", "عثمان", "مثمر", "الثمار", "ثمانية", "ثمين",
             "استثمار", "المستثمر", "ثمة", "الحين", "حينها", "يستحين",
             "اذاعي", "الاذاعة", "شاذا", "لكيلا", "بلكيت", "فتحتى"]

    LEGITIMATE = [
        "ثم تحرر المزلاج بعد ذلك مباشرة.",
        # NOTE: this line qualifies through تدور, NOT through وثم — see
        # test_definite_article_does_not_reach_a_causal_surface for the exact
        # proclitic boundary.
        "وثم تدور الذراع بعد ذلك.",
        "عندما يضغط المستخدم على المقبض تدور الذراع.",
        "حين يرتفع الضغط يفتح الصمام.",
        "بمجرد أن يتحرر المزلاج يدفع النابض المكبس.",
        "اذا ارتفع الضغط يفتح الصمام تلقائيا.",
        "الذراع تحول قوة اليد الى حركة خطية.",
        "هذا يؤدي الى فتح الصمام بالكامل.",
        "فتدور الذراع وتدفع المزلاج.",
        "النظام يقيس الضغط ثم يقارن القيمة بالعتبة.",
    ]

    @pytest.mark.parametrize("word", BLEED)
    def test_causal_surface_does_not_fire_from_inside_a_word(self, word):
        assert has_registered_causal_structure(
            "هذا %s فقط في الجهاز" % word) is False, (
            "causal structure recognised from lexical containment in %r" % word)

    @pytest.mark.parametrize("text", LEGITIMATE)
    def test_legitimate_causal_usage_still_recognised(self, text):
        assert has_registered_causal_structure(text) is True

    def test_ordinary_noun_cannot_manufacture_quality_or_closure(self):
        """The exact material consequence the reviewer proved, pinned."""
        with_bleed = ("المكونات الرئيسية للجهاز هي المزلاج والصمام وقد ارتفع "
                      "ثمن هذه القطع كثيرا هذا العام.")
        with_synonym = ("المكونات الرئيسية للجهاز هي المزلاج والصمام وقد ارتفع "
                        "سعر هذه القطع كثيرا هذا العام.")
        english = ("The main components of the device are the latch and the "
                   "valve and the price of these parts rose a lot this year.")

        def material(answer):
            state = _with_gap(MECHANISM_COMPLETENESS)
            for i in range(2):
                state.iteration = i + 1
                _serve(state, MECHANISM_COMPLETENESS, answer)
            gap = state.get_gap(MECHANISM_COMPLETENESS)
            return _quality(answer), gap.status, gap.closed_at is not None

        assert material(with_bleed) == material(with_synonym), (
            "an ordinary noun sharing letters with a causal surface changed "
            "the material outcome")
        assert material(with_bleed) == material(english), (
            "Arabic is materially easier than its faithful English counterpart")
        assert material(with_bleed)[2] is False

    def test_every_single_token_causal_surface_is_word_mode(self):
        """Structural guarantee: no bare token may be matched by substring."""
        for surface, mode, _mirror in CAUSAL_SURFACES:
            if " " not in surface:
                assert mode == WORD, (
                    "single-token causal surface %r declared %s — that is the "
                    "B-1 defect" % (surface, mode))

    def test_definite_article_does_not_reach_a_causal_surface(self):
        """`ال` turns a connective into a noun phrase, so the article family is
        excluded from causal proclitic stripping while verbs keep و/ف/ب/ك/ل."""
        from engine.semantic_registry import (
            _AR_CAUSAL_PROCLITICS, _AR_ARTICLE_PROCLITICS,
            _MIN_PROCLITIC_SURFACE_LEN)
        assert not (set(_AR_CAUSAL_PROCLITICS) & _AR_ARTICLE_PROCLITICS)
        # Every probe below uses the inert carrier, so the ONLY candidate
        # surface is the one under test. An earlier version of this assertion
        # used "وثم تدور الذراع", which passed through تدور rather than through
        # the proclitic on ثم — a test passing for the wrong reason.
        assert has_registered_causal_structure("هذا الحين فقط") is False
        assert has_registered_causal_structure("هذا وحين فقط") is True
        assert has_registered_causal_structure("هذا فتدور فقط") is True
        assert has_registered_causal_structure("هذا وتدور فقط") is True
        # ثم is 2 characters, below the guard, so NO proclitic reaches it. The
        # behaviour is more conservative than a naive reading would suggest and
        # is asserted here so the comment can never drift from the code again.
        assert len("ثم") < _MIN_PROCLITIC_SURFACE_LEN
        assert has_registered_causal_structure("هذا ثم فقط") is True
        assert has_registered_causal_structure("هذا وثم فقط") is False
        assert has_registered_causal_structure("هذا فثم فقط") is False


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


# ---------------------------------------------------------------------------
# PATH-N PARITY — the PF-SAFETY / PF-DURABILITY families, EN↔AR.
#
# RVR-2 widened the ENGLISH PHYSICAL_FEASIBILITY family by re-deriving surfaces
# from the committed Path-N bank (gap_relevance.py: "'work safely in the real
# world', 'running reliably over time', 'heat, water, time, or wear'"). That
# landed one day after this registry and touched gap_relevance.py alone, so the
# paired Arabic concepts were never added and an Arabic answer expressing the
# SAME owned family was not recognised while its English counterpart was.
#
# These tests pin the CLASS, not a sentence: for each family, several distinct
# Arabic wordings and morphology variants must activate PHYSICAL_FEASIBILITY,
# and none of them may reach any other gap.
# ---------------------------------------------------------------------------
_PATH_N_FAMILIES = {
    "PF-SAFETY": (
        "لا أعرف هامش الأمان المطلوب تحت الحمل.",
        "بأمان تام هو ما أريده من هذا التصميم.",
        "الأمان هو ما يقلقني أكثر في هذا التصميم.",
    ),
    "PF-RELIABILITY": (
        "لن يعمل بشكل موثوق مع الوقت في الخارج.",
        "موثوقية الآلية غير معروفة بعد.",
    ),
    "PF-WEAR": (
        "التآكل قد يوقف الآلية بعد سنة.",
        "أخشى تآكل السطح المعدني مع الاستعمال.",
    ),
    "PF-WATER": (
        "الماء قد يدخل إلى العلبة ويعطلها.",
        "لم أختبرها بالماء ولا أعرف ماذا سيحدث.",
    ),
    "PF-PHYSICAL-WORKABILITY": (
        "لا أعرف إن كان هذا ممكنا من الناحية الفيزيائية.",
        "أريد التحقق من الناحية الفيزيائية قبل البناء.",
        "بالفيزيائية لم أتحقق بعد.",
    ),
}


@pytest.mark.parametrize("concept_id,probe", [
    (cid, probe) for cid, probes in _PATH_N_FAMILIES.items() for probe in probes
], ids=["%s:%d" % (cid, i)
        for cid, probes in _PATH_N_FAMILIES.items()
        for i in range(len(probes))])
def test_path_n_family_activates_physical_feasibility_in_arabic(concept_id, probe):
    """The owned family is recognised through the concept, not a fixed string."""
    assert addresses_gap(probe, PHYSICAL_FEASIBILITY) is True, probe
    assert concept_id in activated_concepts(probe, PHYSICAL_FEASIBILITY)


@pytest.mark.parametrize("probe", [p for ps in _PATH_N_FAMILIES.values() for p in ps])
def test_path_n_family_reaches_no_other_gap(probe):
    """Widening PHYSICAL_FEASIBILITY must not contaminate another family."""
    for other in GAPS:
        if other == PHYSICAL_FEASIBILITY:
            continue
        assert addresses_gap(probe, other) is False, (other, probe)


# Negative controls, one per non-feasibility content class. Each is ordinary
# Arabic an inventor might really write; none expresses a governed PF concept.
_NOT_FEASIBILITY = {
    "mechanism": "المزلاج ينقل القوة إلى الإطار عبر خط المفصلة.",
    "boundary": "فكرتي لا تغطي الأبواب الكهربائية إطلاقا.",
    "commercial": "السعر المستهدف مئة دينار والسوق كبير جدا.",
    "affective": "أشعر بالراحة والفخر عند استخدام المنتج.",
    "step_sequence": "الخطوات: أفرد المنحدر، ثم يقفل المثبت، ثم يعبر الكرسي.",
}


@pytest.mark.parametrize("label,probe", sorted(_NOT_FEASIBILITY.items()))
def test_non_feasibility_arabic_content_stays_irrelevant(label, probe):
    assert addresses_gap(probe, PHYSICAL_FEASIBILITY) is False, (label, probe)


def test_bare_force_is_not_a_registered_feasibility_surface():
    """`قوة` is carried inside the committed MC marker نقل القوة, so
    registering it would make a mechanism-only answer satisfy feasibility.
    The English side excludes bare `force` for the same reason."""
    registered = {surface for c in CONCEPTS
                  if c.owner == PHYSICAL_FEASIBILITY
                  for surface, _mode in c.ar_surfaces}
    assert "قوة" not in registered
    assert "force" not in _INTENT_WORDS[PHYSICAL_FEASIBILITY]


def test_answer_derived_vocabulary_is_not_registered():
    """The R7 residual stays open rather than being closed from an answer.

    `رطوبة` (damp) and `تلف` (damage) appear in a measured RUN-002 answer and
    in no governed PHYSICAL_FEASIBILITY question, in either language. §5.6
    prohibits registering a concept no governed question expresses, so the
    unregistered-wording residual is preserved as a declared known bound.
    """
    registered = {surface for c in CONCEPTS
                  for surface, _mode in c.ar_surfaces}
    for answer_only in ("رطوبة", "تلف", "يتلف", "تتلف"):
        assert answer_only not in registered, answer_only


def test_every_path_n_concept_cites_a_committed_governed_question():
    """§5.1/3 — provenance, or the concept must not exist."""
    by_id = {c.concept_id: c for c in CONCEPTS}
    for cid in _PATH_N_FAMILIES:
        concept = by_id[cid]
        assert concept.owner == PHYSICAL_FEASIBILITY
        assert "N-PF-" in concept.provenance, concept.provenance
        assert concept.en_surfaces and concept.ar_surfaces


@pytest.mark.parametrize("english,concept_id,provenance_token", PATH_N_PF_PAIRING,
                         ids=[r[0] for r in PATH_N_PF_PAIRING])
def test_each_path_n_english_surface_is_paired_on_its_own_concept(
        english, concept_id, provenance_token):
    """The invariant this repair exists to restore, checked per concept.

    A union check over all PHYSICAL_FEASIBILITY concepts would pass if an
    English surface were paired onto the WRONG concept, so each row is checked
    against the concept and the governed question it actually belongs to.

    The expectation rows live in the frozen fixture and are LITERAL: they do
    not derive from the registry, so deleting or moving a pairing leaves the
    expectation standing and this goes RED. They also do not discover a NEW
    English widening on their own — that still has to be added by hand, and the
    fixture says so rather than implying otherwise.
    """
    assert english in _INTENT_WORDS[PHYSICAL_FEASIBILITY], (
        "%r is not (or no longer) an admitted English PF surface" % english)
    by_id = {c.concept_id: c for c in CONCEPTS}
    assert concept_id in by_id, "concept %s is missing" % concept_id
    concept = by_id[concept_id]
    assert concept.owner == PHYSICAL_FEASIBILITY
    assert provenance_token in concept.provenance, concept.provenance
    assert (english, WORD) in concept.en_surfaces, (
        "%r is not carried by %s" % (english, concept_id))
    assert concept.ar_surfaces, (
        "%s carries %r in English with no Arabic pair" % (concept_id, english))


@pytest.mark.parametrize("english,concept_id,_prov", PATH_N_PF_PAIRING,
                         ids=[r[0] for r in PATH_N_PF_PAIRING])
def test_no_other_concept_claims_a_path_n_english_surface(
        english, concept_id, _prov):
    """One surface, one concept — a second claimant would make the per-concept
    check above satisfiable by the wrong owner."""
    claimants = {c.concept_id for c in CONCEPTS
                 if (english, WORD) in c.en_surfaces}
    assert claimants == {concept_id}, sorted(claimants)


def test_the_frozen_pairing_table_covers_the_four_path_n_questions():
    """All four governed PF questions of the bank are represented.

    N-PF-4 was the live unpaired instance the previous candidate missed while
    its guard asserted a narrower set than its wording claimed.
    """
    tokens = {row[2] for row in PATH_N_PF_PAIRING}
    assert tokens == {"N-PF-1", "N-PF-2", "N-PF-3", "N-PF-4"}, sorted(tokens)


# ---------------------------------------------------------------------------
# N-PF-4 — "can this physically work" is its own governed concept.
#
# PF-PRINCIPLE (Q1) asks WHICH physical principle the mechanism relies on.
# N-PF-4 asks WHETHER it can physically work. They share vocabulary and are
# not the same question, so the registry keeps them apart and these tests hold
# that boundary rather than assuming it.
# ---------------------------------------------------------------------------
def test_the_english_physically_surface_is_relevant_and_reaches_no_other_gap():
    probe = "I am not sure whether this can physically work at all."
    assert addresses_gap(probe, PHYSICAL_FEASIBILITY) is True
    assert activated_concepts(probe, PHYSICAL_FEASIBILITY) == frozenset(
        {"PF-PHYSICAL-WORKABILITY"})
    for other in GAPS:
        if other != PHYSICAL_FEASIBILITY:
            assert addresses_gap(probe, other) is False, other


def test_n_pf_4_and_pf_principle_stay_distinct_concepts():
    """Truthful provenance: neither question absorbs the other."""
    workability = "لا أعرف إن كان هذا ممكنا من الناحية الفيزيائية."
    principle = "تعتمد الآلية على مبدأ فيزيائي هو انضغاط النابض."
    assert activated_concepts(workability, PHYSICAL_FEASIBILITY) == frozenset(
        {"PF-PHYSICAL-WORKABILITY"})
    assert "PF-PRINCIPLE" in activated_concepts(principle, PHYSICAL_FEASIBILITY)
    assert "PF-PHYSICAL-WORKABILITY" not in activated_concepts(
        principle, PHYSICAL_FEASIBILITY)


def test_the_q1_masculine_principle_form_is_not_an_n_pf_4_surface():
    """`فيزيائي` belongs to the Q1 principle question; registering it here
    would claim N-PF-4 provenance for wording N-PF-4 does not use."""
    by_id = {c.concept_id: c for c in CONCEPTS}
    ar = {surface for surface, _mode
          in by_id["PF-PHYSICAL-WORKABILITY"].ar_surfaces}
    assert ar == {"فيزيائية"}, sorted(ar)
    assert "فيزيائي" not in ar
    assert "فيزيائيا" not in ar     # in no governed question, in either language
