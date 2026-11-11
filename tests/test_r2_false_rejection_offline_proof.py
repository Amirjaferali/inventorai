# -*- coding: utf-8 -*-
"""R2 FALSE-REJECTION OFFLINE PROOF — injectable boundary, NOT a semantic method.

This test-only proof composes the existing #966 source-bound contextual decision
with TWO additional, independent INJECTED judgements: new contribution and
served-Mechanism-Completeness relevance. The third judgement is an explicit
UNQUALIFIED ORACLE INPUT, not inferred from RELATED, CONTENT_BEARING, matching
words, or the frozen holdout labels. No production caller, provider, writer,
new engine contract, or application route is introduced.

A positive result here proves only that a correctly supplied three-axis
decision can be composed with the incumbent's quality and progression rules.
It does NOT prove an available method can supply the served-gap judgement.
The 120 frozen cases are reused for a structural/oracle-bound comparison only,
never as an independently measured model-qualification score.
"""
from dataclasses import dataclass
from types import SimpleNamespace

import pytest

from engine import progression_loop as pl
from engine import session_reconstruction as sr
from engine.idea_state import (
    ASSERTED, Evidence, Gap, IdeaState, MECHANISM_COMPLETENESS as MC,
    OWNER_STATED,
)
from tests.test_msnl_llm_eval_harness import h

METHOD = "r2-false-rejection-three-axis/offline-oracle-only"
CONTENT = "CONTENT_BEARING"
NO_CONTENT = "NO_NEW_CONTENT"
GAP_ADDRESSED = "ADDRESSED"
GAP_NOT_ADDRESSED = "NOT_ADDRESSED"
GAP_UNCERTAIN = "UNCERTAIN"
GAP_VALUES = (GAP_ADDRESSED, GAP_NOT_ADDRESSED, GAP_UNCERTAIN)
CONTRIBUTION_VALUES = (CONTENT, NO_CONTENT, "UNCERTAIN")
OLD_PRIORS = ("OPEN", "PARTIAL")


@dataclass(frozen=True)
class InjectedJudgement:
    record_id: str
    project_relation: str
    new_contribution: str
    served_gap_relevance: str
    method_id: str
    source_digest: str


def _record(text, question_id="mechanical:MECHANISM_COMPLETENESS:Q1", record_id="rec_0"):
    return SimpleNamespace(
        record_id=record_id, gap_context=MC,
        question_target="PATHN:" + question_id, disposition="answered",
        content=text, superseded_by=None, supersedes=[],
    )


def _inject(seed, record, project_relation=sr.CX_RELATED,
            new_contribution=CONTENT, served_gap_relevance=GAP_ADDRESSED,
            method=METHOD):
    return InjectedJudgement(
        record_id=record.record_id, project_relation=project_relation,
        new_contribution=new_contribution,
        served_gap_relevance=served_gap_relevance, method_id=method,
        source_digest=sr.contextual_source_digest(method, seed, record, None),
    )


def _admission(seed, ledger, injected):
    """Only an EXACT, source-bound, three-axis affirmative can recover credit.

    #966 owns identity, previous-context binding, decision corruption and stale
    refusal. The two new axes are test-only injected metadata. Missing axes,
    UNCERTAIN, source drift and UNRELATED never generate a positive override.
    """
    active = {r.record_id: r for r in ledger if r.disposition == "answered"
              and r.superseded_by is None}
    if injected is None:
        return False, "ABSENT"
    if (not isinstance(injected, InjectedJudgement)
            or injected.record_id not in active
            or injected.new_contribution not in CONTRIBUTION_VALUES
            or injected.served_gap_relevance not in GAP_VALUES):
        raise sr.ContextualDecisionError("invalid injected assessment")
    decision = sr.ContextualDecision(
        injected.record_id, injected.project_relation,
        injected.method_id, injected.source_digest)
    plan = sr.contextual_admission_plan(
        seed, ledger, {injected.record_id: decision}, METHOD)
    existing = plan[injected.record_id]
    if existing.outcome != sr.CX_ADMITTED:
        return False, existing.reason or existing.outcome
    if injected.new_contribution != CONTENT:
        return False, "NO_CONFIRMED_NEW_CONTENT"
    if injected.served_gap_relevance != GAP_ADDRESSED:
        return False, "SERVED_GAP_NOT_ESTABLISHED"
    return True, "THREE_AXES_POSITIVE_INJECTED_ONLY"


def _starting_state(case, prior):
    state = IdeaState(idea_id="synthetic-r2-proof")
    state.domain, state.path = case["domain"], "N"
    state.engine_contract_version = sr.ENGINE_CONTRACT_VERSION_T2G4
    state.maturity_level = 1
    state.gaps.append(Gap(gap_type=MC, status=prior,
                          opened_at=0, iterations_open=case["served_index"]))
    if prior == "PARTIAL":
        state.known_mechanism = Evidence(
            content="[previous synthetic statement]", quality=ASSERTED,
            iteration=0, provenance=OWNER_STATED)
    return state


def _run_injected(case, prior, injected, monkeypatch):
    """Test-only composition: withheld = #966's skip; recovery = R2 eligibility.

    In production there is NO route invoking this function. The test patches
    ONLY this exact answer/gap while calling the real run_iteration and
    integrate_response, so quality, T2-G-3/4 vetoes, maturity and attribution
    are evaluated by their unchanged owners. An injected judgement itself
    cannot set any part of the state.
    """
    record = _record(case["current_answer"], case["question_id"])
    state = _starting_state(case, prior)
    state.assertions = [record]  # documentary source, exact and verbatim
    admitted, reason = _admission(case["original_idea"], [record], injected)
    if admitted:
        original = pl.addresses_gap

        def recovered_only_for_this_record(text, gap):
            if text == record.content and gap == record.gap_context:
                return True
            return original(text, gap)

        with monkeypatch.context() as scoped:
            scoped.setattr(pl, "addresses_gap", recovered_only_for_this_record)
            pl.run_iteration(state, record.content)
    return state, admitted, reason


def _credited(state, answer, prior):
    gap = state.get_gap(MC)
    advanced = (prior == "OPEN" and gap.status in ("PARTIAL", "CLOSED")) or (
        prior == "PARTIAL" and gap.status == "CLOSED")
    mechanism_set = (state.known_mechanism is not None
                     and state.known_mechanism.content == answer)
    return advanced or mechanism_set


@pytest.fixture(scope="module")
def frozen():
    # The already-pinned #951/#963/#965 material: NO fixture, hash, label or
    # result is edited, and NO provider is asked to classify these cases.
    manifest = h.context_history_manifest()
    assert len(manifest["cases"]) == 120
    return manifest["cases"]


@pytest.mark.parametrize("prior", OLD_PRIORS)
def test_both_error_directions_on_the_frozen_cases_are_independent(
        frozen, prior, monkeypatch):
    """An ORACLE-BOUND compositional ceiling, not accuracy of a classifier.

    A case's FROZEN label supplies each injected judgement for this diagnostic
    only. This cannot test whether a real method would produce that judgement.
    The original incumbent's 31/60 false rejections and 38/60 false credits
    remain the independently recorded baseline and are not overwritten.
    """
    recovered, wrong_credit = [], []
    candidates = [c for c in frozen if c["slot_label"]["project_relation"] == "RELATED"
                  and c["slot_label"]["new_contribution"] == CONTENT]
    assert len(candidates) == 60
    for case in frozen:
        record = _record(case["current_answer"], case["question_id"])
        slot = case["slot_label"]
        injection = _inject(
            case["original_idea"], record,
            project_relation=slot["project_relation"],
            new_contribution=slot["new_contribution"],
            served_gap_relevance=(GAP_ADDRESSED if case in candidates
                                  else GAP_UNCERTAIN),
        )
        state, admitted, _ = _run_injected(case, prior, injection, monkeypatch)
        credit = _credited(state, case["current_answer"], prior)
        if case in candidates:
            if credit:
                recovered.append(case["case_id"])
            assert not admitted or state.known_mechanism is None or (
                state.known_mechanism.provenance == OWNER_STATED
                and state.known_mechanism.content == case["current_answer"])
            assert state.maturity_level == 1  # no direct grant of maturity
        else:
            if credit:
                wrong_credit.append(case["case_id"])
            assert not admitted
            assert state.get_gap(MC).status == prior
            assert state.maturity_level == 1
            assert state.assertions[0].content == case["current_answer"]
            assert state.get_gap(MC).evidence == []
    assert wrong_credit == [], wrong_credit
    # Representative false-rejections in EACH promised family are recoverable
    # in both languages where the real existing stance/quality guards allow.
    by_id = {c["case_id"]: c for c in frozen}
    families = {"NEW_DETAIL", "PLAIN_LANGUAGE_DETAIL", "AMENDMENT",
                "RESTATE_THEN_NEW", "HISTORY_COUNTERFACTUAL_NEW"}
    assert families <= {by_id[i]["category"] for i in recovered}
    # Do not assert 60/60: a retained T2-G guard may conservatively withhold.


@pytest.mark.parametrize("gap_decision", [GAP_NOT_ADDRESSED, GAP_UNCERTAIN])
def test_genuinely_new_project_content_outside_served_gap_cannot_advance(
        gap_decision, monkeypatch):
    # New physical product information with plausible technical detail, but
    # shipping-packaging changes do not explain the mechanism of this device.
    # The independent served-gap verdict is INJECTED, not guessed from words.
    seed = ("My automatic pill divider moves tablets into a row and cuts each "
            "tablet into halves when I press a handle.")
    answer = ("I changed its shipping package to a reusable folded cardboard "
              "tray with nesting ribs so retailers can stack many boxes.")
    case = {"domain": "mechanical", "served_index": 0,
            "question_id": "mechanical:MECHANISM_COMPLETENESS:Q1",
            "original_idea": seed, "current_answer": answer}
    rec = _record(answer, case["question_id"])
    injection = _inject(seed, rec, new_contribution=CONTENT,
                        served_gap_relevance=gap_decision)
    state, admitted, reason = _run_injected(case, "OPEN", injection, monkeypatch)
    assert not admitted and reason == "SERVED_GAP_NOT_ESTABLISHED"
    assert state.get_gap(MC).status == "OPEN"
    assert state.known_mechanism is None and state.maturity_level == 1
    assert state.assertions[0].content == answer  # no loss of owner statement


@pytest.mark.parametrize("relation,contribution,gap_decision", [
    (sr.CX_UNRELATED, CONTENT, GAP_ADDRESSED),
    (sr.CX_RELATED, NO_CONTENT, GAP_ADDRESSED),
    (sr.CX_RELATED, CONTENT, GAP_UNCERTAIN),
    (sr.CX_RELATED, CONTENT, GAP_NOT_ADDRESSED),
    (sr.CX_UNCERTAIN, CONTENT, GAP_ADDRESSED),
    (sr.CX_UNAVAILABLE, CONTENT, GAP_ADDRESSED),
])
def test_every_required_axis_is_independent_and_withholds_on_uncertainty(
        relation, contribution, gap_decision):
    record = _record("A newly stated part rotates and moves the board.")
    decision = _inject("Synthetic original invention", record,
                       project_relation=relation, new_contribution=contribution,
                       served_gap_relevance=gap_decision)
    allowed, _ = _admission("Synthetic original invention", [record], decision)
    assert not allowed


def test_absence_stale_question_seed_and_invalid_decision_fail_closed():
    seed = "Original invented tool"
    r = _record("The gate moves up with a small hinge.")
    assert _admission(seed, [r], None) == (False, "ABSENT")
    good = _inject(seed, r)
    assert _admission(seed, [r], good)[0]
    for altered_seed, altered_record in [
        ("Another invented tool", r),
        (seed, _record(r.content, "mechanical:MECHANISM_COMPLETENESS:Q3")),
        (seed, _record("The gate does not move at all.")),
    ]:
        admitted, reason = _admission(altered_seed, [altered_record], good)
        assert not admitted and reason == sr.CX_REASON_STALE
    malformed = InjectedJudgement(
        r.record_id, sr.CX_RELATED, "NOT_AN_AXIS", GAP_ADDRESSED,
        METHOD, good.source_digest)
    with pytest.raises(sr.ContextualDecisionError):
        _admission(seed, [r], malformed)


def test_mixed_assertion_and_pending_choice_keeps_distinct_facts(monkeypatch):
    # The first sentence is a real asserted mechanism, the second a separate
    # undecided choice; there must not be an indiscriminate "contains unknown"
    # veto. The existing stance owner still decides the progression result.
    from tests.test_r2_contextual_admission_offline_proof import LEGIT, UNDECIDED
    text = LEGIT + " " + UNDECIDED
    case = {"domain": "mechanical", "served_index": 0,
            "question_id": "mechanical:MECHANISM_COMPLETENESS:Q1",
            "original_idea": "A folding wheelchair ramp rests on a doorstep.",
            "current_answer": text}
    rec = _record(text, case["question_id"])
    yes = _inject(case["original_idea"], rec)
    state, admitted, _ = _run_injected(case, "OPEN", yes, monkeypatch)
    assert admitted
    assert state.assertions[0].content == text
    assert state.known_mechanism is not None
    assert state.known_mechanism.content == text
    assert state.known_mechanism.provenance == OWNER_STATED
    assert state.maturity_level == 1

    # Without a defensible served-gap judgement the identical mixed answer
    # stays recorded but *none* of its possible credit is inferred.
    unassessed = _inject(case["original_idea"], rec,
                         served_gap_relevance=GAP_UNCERTAIN)
    held, admitted, _ = _run_injected(case, "OPEN", unassessed, monkeypatch)
    assert not admitted and held.known_mechanism is None
    assert held.assertions[0].content == text


def test_source_chain_and_historical_contracts_are_not_replaced():
    # The source-binding and transitive invalidation owner is STILL #966.
    a = _record("The hinge moves", record_id="rec_0")
    b = _record("The hook holds", record_id="rec_1")
    c = _record("The spring releases", record_id="rec_2")
    seed = "Synthetic mechanical invention"
    plan_inputs = {}
    parent, parent_digest = None, None
    for rec in (a, b, c):
        digest = sr.contextual_source_digest(
            METHOD, seed, rec, parent, parent_digest)
        plan_inputs[rec.record_id] = sr.ContextualDecision(
            rec.record_id, sr.CX_RELATED, METHOD, digest)
        parent, parent_digest = rec, digest
    original = sr.contextual_admission_plan(seed, [a, b, c], plan_inputs, METHOD)
    assert all(x.outcome == sr.CX_ADMITTED for x in original.values())
    a.content = "The hinge is replaced with a flexible strip"
    stale = sr.contextual_admission_plan(seed, [a, b, c], plan_inputs, METHOD)
    assert all(x.outcome == sr.CX_PENDING for x in stale.values())
    assert all(x.reason == sr.CX_REASON_STALE for x in stale.values())
    assert sr.CURRENT_ENGINE_CONTRACT_VERSION == sr.ENGINE_CONTRACT_VERSION_T2G4
    assert sr.GAP_BOUND_REPLAY_VERSIONS == (
        sr.ENGINE_CONTRACT_VERSION_XG1, sr.ENGINE_CONTRACT_VERSION_T2G4)
    assert all("false-rejection" not in version
               for version in sr.SUPPORTED_ENGINE_CONTRACT_VERSIONS)
