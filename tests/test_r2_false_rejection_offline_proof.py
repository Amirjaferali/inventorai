# -*- coding: utf-8 -*-
"""R2 FALSE-REJECTION OFFLINE PROOF: three independent axes, measured on the real
engine. Verdict: FALSE CREDIT reduced; FALSE REJECTION BLOCKED / METHOD NOT
QUALIFIED.

This is an Owner-authorized offline proof under PR #967. It has no production
caller, provider call, writer, engine contract, route or persisted decision.

THE THREE AXES ARE INDEPENDENT. None implies another:
  1. project relation: RELATED (#966 source binding and transitive invalidation);
  2. new contribution: CONTENT_BEARING;
  3. served-gap relevance: the content addresses the governed Mechanism
     Completeness question.

COMPOSITION (`_compose`)
  * WITHHOLD: no credit, and the answer stays recorded verbatim. This applies
    when any of the following holds:
      - the relation is not a valid RELATED (UNRELATED, UNCERTAIN, UNAVAILABLE,
        absent or stale);
      - the contribution is not CONTENT_BEARING;
      - served-gap relevance is NOT_ADDRESSED.
  * INCUMBENT: served-gap relevance is UNCERTAIN, meaning no qualified method
    exists. The EXISTING governed relevance owner (`addresses_gap` and its W2-C
    supplement), the quality rules and the T2-G-3 / T2-G-4 stance guards decide,
    unchanged. The injected axes can only withhold here, never grant.
  * WIDEN: served-gap relevance is ADDRESSED. This is the ONLY path that could
    recover a false rejection. Here an injected judgement replaces the governed
    relevance owner's verdict for this one answer.
    - No qualified component produces that judgement. It is an ORACLE in these
      tests, and every WIDEN test is a boundary contract, never evidence.

WHAT IS MEASURED, WITH NO ORACLE
The recorded Run 03 decisions (#965) are composed with the real engine on the
frozen #951 holdout and compared with the #963 incumbent baseline:
  * false credit:    38 / 60  ->  0 / 60
  * false rejection: 31 / 60  -> 31 / 60
The figures are identical from an OPEN and from a PARTIAL prior. The relation
and novelty axes add no new false rejection. Every remaining false rejection is
a lexical miss of the governed relevance owner, so recovering it needs a
served-gap method. Run 03 has no served-gap axis, and the hazard test below
shows why widening without one is unsafe: on a content-free reference, the
incumbent quality rule does not stop a widened answer from being credited.
These are observations on one synthetic holdout and one recorded run. They are
not a real-user rate and not a qualification.

A SECOND, SEPARATE FALSE-REJECTION MODE is found and NOT repaired: the unchanged
T2-G explicit-unknown rule rejects a mixed answer, meaning a real mechanism
followed by a pending choice, although the mechanism alone is credited. Neither
the composition nor widening touches that rule, which does not read relevance.
"""
import json
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

METHOD = "r2-false-rejection-three-axis/offline-proof"
CONTENT = "CONTENT_BEARING"
NO_CONTENT = "NO_NEW_CONTENT"
GAP_ADDRESSED = "ADDRESSED"
GAP_NOT_ADDRESSED = "NOT_ADDRESSED"
GAP_UNCERTAIN = "UNCERTAIN"
GAP_VALUES = (GAP_ADDRESSED, GAP_NOT_ADDRESSED, GAP_UNCERTAIN)
CONTRIBUTION_VALUES = (CONTENT, NO_CONTENT, "UNCERTAIN")
PRIORS = ("OPEN", "PARTIAL")
WITHHOLD, INCUMBENT, WIDEN = "WITHHOLD", "INCUMBENT", "WIDEN"
Q1 = "mechanical:MECHANISM_COMPLETENESS:Q1"


@dataclass(frozen=True)
class InjectedJudgement:
    record_id: str
    project_relation: str
    new_contribution: str
    served_gap_relevance: str
    method_id: str
    source_digest: str


def _record(text, question_id=Q1, record_id="rec_0"):
    return SimpleNamespace(
        record_id=record_id, gap_context=MC,
        question_target="PATHN:" + question_id, disposition="answered",
        content=text, superseded_by=None, supersedes=[],
    )


def _inject(seed, record, project_relation=sr.CX_RELATED, new_contribution=CONTENT,
            served_gap_relevance=GAP_UNCERTAIN, method=METHOD):
    return InjectedJudgement(
        record_id=record.record_id, project_relation=project_relation,
        new_contribution=new_contribution, served_gap_relevance=served_gap_relevance,
        method_id=method,
        source_digest=sr.contextual_source_digest(method, seed, record, None))


def _compose(seed, ledger, injected):
    """(path, reason). The relation axis goes through the merged #966 owner
    (identity, source binding, staleness, corruption). The other two axes are
    test-only injected values. No axis implies another, and only WIDEN can
    replace the governed relevance verdict."""
    active = {r.record_id for r in ledger
              if r.disposition == "answered" and r.superseded_by is None}
    if injected is None:
        return WITHHOLD, sr.CX_REASON_ABSENT
    if (not isinstance(injected, InjectedJudgement)
            or injected.record_id not in active
            or injected.new_contribution not in CONTRIBUTION_VALUES
            or injected.served_gap_relevance not in GAP_VALUES):
        raise sr.ContextualDecisionError("invalid injected assessment")
    plan = sr.contextual_admission_plan(
        seed, ledger, {injected.record_id: sr.ContextualDecision(
            injected.record_id, injected.project_relation, injected.method_id,
            injected.source_digest)}, METHOD)
    relation = plan[injected.record_id]
    if relation.outcome != sr.CX_ADMITTED:
        return WITHHOLD, relation.reason or relation.outcome
    if injected.new_contribution != CONTENT:
        return WITHHOLD, "NO_CONFIRMED_NEW_CONTENT"
    if injected.served_gap_relevance == GAP_NOT_ADDRESSED:
        return WITHHOLD, "SERVED_GAP_NOT_ADDRESSED"
    if injected.served_gap_relevance == GAP_UNCERTAIN:
        return INCUMBENT, "SERVED_GAP_NOT_ESTABLISHED"
    return WIDEN, "SERVED_GAP_ADDRESSED_ORACLE_ONLY"


def _state(domain, served_index, prior):
    state = IdeaState(idea_id="synthetic-r2-proof")
    state.domain, state.path = domain, "N"
    state.engine_contract_version = sr.ENGINE_CONTRACT_VERSION_T2G4
    state.maturity_level = 1
    state.gaps.append(Gap(gap_type=MC, status=prior, opened_at=0,
                          iterations_open=served_index))
    if prior == "PARTIAL":
        state.known_mechanism = Evidence(
            content="[previous synthetic statement]", quality=ASSERTED,
            iteration=0, provenance=OWNER_STATED)
    return state


def _run(seed, text, injected, prior="OPEN", domain="mechanical", served_index=0,
         question_id=Q1, monkeypatch=None):
    """The real canonical `run_iteration` / `integrate_response` under T2-G-4.
    WITHHOLD runs nothing (the #966 unapplied path). INCUMBENT runs the engine
    unchanged. WIDEN replaces the governed relevance verdict for THIS answer's
    exact text only; every other sentence-level check, including the T2-G-3 /
    T2-G-4 stance vetoes, still uses the governed owner."""
    record = _record(text, question_id)
    state = _state(domain, served_index, prior)
    state.assertions = [record]
    path, reason = _compose(seed, [record], injected)
    if path == INCUMBENT:
        pl.run_iteration(state, text)
    elif path == WIDEN:
        original = pl.addresses_gap

        def widened(response, gap):
            return True if (response == text and gap == MC) else original(response, gap)
        with monkeypatch.context() as scoped:
            scoped.setattr(pl, "addresses_gap", widened)
            pl.run_iteration(state, text)
    return state, path, reason


def _credited(state, text, prior):
    status = state.get_gap(MC).status
    advanced = (status in ("PARTIAL", "CLOSED")) if prior == "OPEN" else status == "CLOSED"
    return advanced or (state.known_mechanism is not None
                        and state.known_mechanism.content == text)


# ==========================================================================
# 1. the measurement, with NO oracle: recorded Run 03 decisions on the engine
# ==========================================================================
def _evidence():
    base = h.CONTEXT_HISTORY_EVIDENCE_DIR
    with open(h.CONTEXT_HISTORY_INCUMBENT_BASELINE_PATH, encoding="utf-8") as fh:
        incumbent = {r["case_id"]: r for r in json.load(fh)["rows"]}
    with open(h.CONTEXT_HISTORY_RUN_03_REPORT_PATH, encoding="utf-8") as fh:
        run03 = {r["case_id"]: r["decision"] for r in json.load(fh)["rows"]}
    assert base and set(incumbent) == set(run03) and len(run03) == 120
    return incumbent, run03


@pytest.fixture(scope="module")
def measured():
    """Every frozen case through the real engine. The relation and novelty axes
    are Run 03's RECORDED decisions. No served-gap decision exists, so it is
    UNCERTAIN everywhere: the only state the evidence supports."""
    manifest = h.context_history_manifest()
    incumbent, run03 = _evidence()
    rows = {}
    for case in manifest["cases"]:
        decision = run03[case["case_id"]]
        for prior in PRIORS:
            record = _record(case["current_answer"], case["question_id"])
            judgement = _inject(case["original_idea"], record,
                                project_relation=decision["project_relation"],
                                new_contribution=decision["new_contribution"])
            state, path, _ = _run(case["original_idea"], case["current_answer"], judgement,
                                  prior, case["domain"], case["served_index"],
                                  case["question_id"])
            assert path in (WITHHOLD, INCUMBENT)                # never WIDEN here
            rows[(case["case_id"], prior)] = {
                "composed": _credited(state, case["current_answer"], prior),
                "incumbent": incumbent[case["case_id"]]["granted"][prior],
                "positive": incumbent[case["case_id"]]["frozen_progress_positive"],
                "lexical": incumbent[case["case_id"]]["addresses_gap"],
                "category": case["category"], "path": path}
    return rows


@pytest.mark.parametrize("prior", PRIORS)
def test_false_credit_and_false_rejection_are_measured_separately(measured, prior):
    rows = [r for (cid, p), r in measured.items() if p == prior]
    negatives = [r for r in rows if not r["positive"]]
    positives = [r for r in rows if r["positive"]]
    assert len(negatives) == len(positives) == 60
    assert sum(r["incumbent"] for r in negatives) == 38       # #963 baseline
    assert sum(not r["incumbent"] for r in positives) == 31   # #963 baseline
    assert sum(r["composed"] for r in negatives) == 0         # false credit 38 -> 0
    assert sum(not r["composed"] for r in positives) == 31    # false rejection unchanged
    # no new false rejection: every positive the incumbent credits stays credited
    assert all(r["composed"] for r in positives if r["incumbent"])
    # the composition never credits what the incumbent rejects (axes cannot grant)
    assert not any(r["composed"] and not r["incumbent"] for r in rows)


def test_every_remaining_false_rejection_is_a_lexical_served_gap_miss(measured):
    unresolved = {cid for (cid, p), r in measured.items()
                  if p == "OPEN" and r["positive"] and not r["composed"]}
    assert len(unresolved) == 31
    assert all(not measured[(cid, "OPEN")]["lexical"] for cid in unresolved)
    assert all(measured[(cid, "OPEN")]["path"] == INCUMBENT for cid in unresolved)
    by_category = {}
    for cid in unresolved:
        cat = measured[(cid, "OPEN")]["category"]
        by_category[cat] = by_category.get(cat, 0) + 1
    assert by_category == {"PLAIN_LANGUAGE_DETAIL": 8, "HISTORY_COUNTERFACTUAL_NEW": 8,
                           "RESTATE_THEN_NEW": 6, "AMENDMENT": 5, "NEW_DETAIL": 4}


def test_the_measurement_is_deterministic_and_matches_the_committed_evidence(measured):
    incumbent, _ = _evidence()
    for (cid, prior), r in measured.items():
        if r["path"] == INCUMBENT:                       # the engine ran unchanged
            assert r["composed"] == incumbent[cid]["granted"][prior], (cid, prior)


# ==========================================================================
# 2. WIDEN: boundary contract only (ORACLE, never evidence)
# ==========================================================================
SEED = ("A folding mechanical wheelchair ramp with a spring latch that must stay "
        "locked flat and fold away without tools.")


def test_oracle_widening_can_recover_a_lexical_miss_only_through_the_engine(monkeypatch):
    """The recovery path exists, and it depends entirely on the oracle."""
    incumbent, _ = _evidence()
    case = [c for c in h.context_history_manifest()["cases"]
            if c["category"] == "PLAIN_LANGUAGE_DETAIL" and c["domain"] == "mechanical"
            and not incumbent[c["case_id"]]["granted"]["OPEN"]][0]   # a real lexical miss
    rec = _record(case["current_answer"], case["question_id"])
    held, path, _ = _run(case["original_idea"], case["current_answer"],
                         _inject(case["original_idea"], rec), "OPEN", case["domain"],
                         case["served_index"], case["question_id"])
    assert path == INCUMBENT and not _credited(held, case["current_answer"], "OPEN")
    widened, path, _ = _run(case["original_idea"], case["current_answer"],
                            _inject(case["original_idea"], rec,
                                    served_gap_relevance=GAP_ADDRESSED),
                            "OPEN", case["domain"], case["served_index"],
                            case["question_id"], monkeypatch)
    assert path == WIDEN and _credited(widened, case["current_answer"], "OPEN")
    assert widened.known_mechanism.provenance == OWNER_STATED
    assert widened.maturity_level == 1


@pytest.mark.parametrize("text", [
    "I haven't decided whether the latch should be a spring catch or a magnet. "
    "I haven't chosen how the ramp will fold either.",                       # T2-G-4
    "Should the latch be a spring catch? Would a magnet hold it better?",    # T2-G-3
    "I do not know how it locks. I have no idea what holds it flat.",        # unknown
])
def test_widening_never_overrides_the_existing_stance_guards(monkeypatch, text):
    rec = _record(text)
    state, path, _ = _run(SEED, text, _inject(SEED, rec, served_gap_relevance=GAP_ADDRESSED),
                          monkeypatch=monkeypatch)
    assert path == WIDEN
    assert state.get_gap(MC).status == "OPEN" and state.known_mechanism is None


def test_widening_hazard_the_quality_rule_does_not_stop_content_free_text(monkeypatch):
    """WHY THE METHOD IS NOT QUALIFIED. If the injected axes wrongly mark a
    content-free reference as CONTENT_BEARING and ADDRESSED, the incumbent
    quality rule credits it. Once relevance is widened, the injected judgement
    is effectively sufficient. A served-gap method must therefore be qualified
    on its own before any widening; the engine is no safety net here."""
    text = "As I said before, it works the way I described earlier."
    rec = _record(text)
    held, path, _ = _run(SEED, text, _inject(SEED, rec))
    assert path == INCUMBENT and not _credited(held, text, "OPEN")
    wrong, path, _ = _run(SEED, text, _inject(SEED, rec, served_gap_relevance=GAP_ADDRESSED),
                          monkeypatch=monkeypatch)
    assert path == WIDEN and _credited(wrong, text, "OPEN")              # the hazard


# ==========================================================================
# 3. independence, failure policy, mixed answers, source chain, isolation
# ==========================================================================
@pytest.mark.parametrize("relation,contribution,gap,expected", [
    (sr.CX_UNRELATED, CONTENT, GAP_ADDRESSED, WITHHOLD),
    (sr.CX_UNCERTAIN, CONTENT, GAP_ADDRESSED, WITHHOLD),
    (sr.CX_UNAVAILABLE, CONTENT, GAP_ADDRESSED, WITHHOLD),
    (sr.CX_RELATED, NO_CONTENT, GAP_ADDRESSED, WITHHOLD),
    (sr.CX_RELATED, "UNCERTAIN", GAP_ADDRESSED, WITHHOLD),
    (sr.CX_RELATED, CONTENT, GAP_NOT_ADDRESSED, WITHHOLD),
    (sr.CX_RELATED, CONTENT, GAP_UNCERTAIN, INCUMBENT),
    (sr.CX_RELATED, CONTENT, GAP_ADDRESSED, WIDEN),
])
def test_no_axis_implies_another(relation, contribution, gap, expected):
    rec = _record("A newly stated part rotates and moves the board.")
    path, _ = _compose("Synthetic invention", [rec],
                       _inject("Synthetic invention", rec, relation, contribution, gap))
    assert path == expected


def test_new_project_content_outside_the_served_gap_cannot_advance():
    seed = ("My automatic pill divider moves tablets into a row and cuts each tablet "
            "into halves when I press a handle.")
    answer = ("I changed its shipping package to a reusable folded cardboard tray with "
              "nesting ribs so retailers can stack many boxes.")
    rec = _record(answer)
    state, path, reason = _run(seed, answer, _inject(
        seed, rec, served_gap_relevance=GAP_NOT_ADDRESSED))
    assert (path, reason) == (WITHHOLD, "SERVED_GAP_NOT_ADDRESSED")
    assert state.get_gap(MC).status == "OPEN" and state.known_mechanism is None
    assert state.assertions[0].content == answer                       # kept verbatim


def test_absent_stale_and_invalid_decisions_fail_closed():
    seed = "Original invented tool"
    rec = _record("The gate moves up with a small hinge.")
    assert _compose(seed, [rec], None) == (WITHHOLD, sr.CX_REASON_ABSENT)
    good = _inject(seed, rec)
    assert _compose(seed, [rec], good)[0] == INCUMBENT
    for other_seed, other in [("Another invented tool", rec),
                              (seed, _record(rec.content, "mechanical:MECHANISM_COMPLETENESS:Q3")),
                              (seed, _record("The gate does not move at all."))]:
        assert _compose(other_seed, [other], good) == (WITHHOLD, sr.CX_REASON_STALE)
    with pytest.raises(sr.ContextualDecisionError):
        _compose(seed, [rec], InjectedJudgement(rec.record_id, sr.CX_RELATED, "NOT_AN_AXIS",
                                                GAP_UNCERTAIN, METHOD, good.source_digest))


def test_a_mixed_answer_is_an_unresolved_incumbent_false_rejection(monkeypatch):
    """FINDING, not repaired here. A real mechanism followed by a pending choice
    is REJECTED by the unchanged T2-G explicit-unknown rule
    (`explicit_unknown_without_mechanism`), although the same mechanism alone
    is credited. This is a false rejection "merely because uncertainty is
    present". It is not a lexical miss, and it is not on the frozen holdout.

    The three-axis composition neither causes nor repairs it, and neither does
    oracle widening, because that rule does not read relevance. The answer
    stays recorded verbatim. Repairing it means separating clauses in the
    T2-G owner, which needs its own Owner decision and engine contract."""
    from tests.test_r2_contextual_admission_offline_proof import LEGIT, UNDECIDED
    alone, path, _ = _run(SEED, LEGIT, _inject(SEED, _record(LEGIT)))
    assert path == INCUMBENT and _credited(alone, LEGIT, "OPEN")
    text = LEGIT + " " + UNDECIDED
    rec = _record(text)
    for relevance in (GAP_UNCERTAIN, GAP_ADDRESSED):
        state, path, _ = _run(SEED, text, _inject(SEED, rec, served_gap_relevance=relevance),
                              monkeypatch=monkeypatch)
        assert path in (INCUMBENT, WIDEN)
        assert state.known_mechanism is None and state.get_gap(MC).status == "OPEN"
        assert state.assertions[0].content == text                     # kept verbatim


def test_the_source_chain_stays_with_the_966_owner_and_contracts_are_unchanged():
    seed = "Synthetic mechanical invention"
    chain = [_record(t, record_id="rec_%d" % i)
             for i, t in enumerate(("The hinge moves", "The hook holds", "The spring releases"))]
    decisions, parent, parent_digest = {}, None, None
    for rec in chain:
        digest = sr.contextual_source_digest(METHOD, seed, rec, parent, parent_digest)
        decisions[rec.record_id] = sr.ContextualDecision(rec.record_id, sr.CX_RELATED,
                                                         METHOD, digest)
        parent, parent_digest = rec, digest
    assert {x.outcome for x in sr.contextual_admission_plan(
        seed, chain, decisions, METHOD).values()} == {sr.CX_ADMITTED}
    chain[0].content = "The hinge is replaced with a flexible strip"
    stale = sr.contextual_admission_plan(seed, chain, decisions, METHOD)
    assert {(x.outcome, x.reason) for x in stale.values()} == {(sr.CX_PENDING,
                                                                  sr.CX_REASON_STALE)}
    # The only version added since is T2-G-5 (the separately authorized
    # exact-repeat repair), not this candidate.
    assert sr.CURRENT_ENGINE_CONTRACT_VERSION == sr.ENGINE_CONTRACT_VERSION_T2G5
    assert sr.GAP_BOUND_REPLAY_VERSIONS == (sr.ENGINE_CONTRACT_VERSION_XG1,
                                           sr.ENGINE_CONTRACT_VERSION_T2G4,
                                           sr.ENGINE_CONTRACT_VERSION_T2G5)
    assert all("false-rejection" not in v for v in sr.SUPPORTED_ENGINE_CONTRACT_VERSIONS)
