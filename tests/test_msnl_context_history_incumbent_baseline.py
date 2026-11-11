# -*- coding: utf-8 -*-
"""R2-OFFLINE-BASELINE-01 — the incumbent deterministic assessment on the frozen context-history
holdout, preserved as reproducible evidence.

Offline, network-free, synthetic. What is pinned:
  * the committed record recomputes exactly from the frozen #951 manifest, through the unchanged
    `mc_engine_outcome` composition and the existing `addresses_gap` / `assess_response` owners;
  * the observed counts: false credit 38 of 60 and false rejection 31 of 60 (30 / 48 and 23 / 48 on
    the authored cases), identical from an OPEN and a PARTIAL prior, by category, project and
    language;
  * the 24 identical-text pairs (each a positive and a negative frozen label) get ONE incumbent
    outcome each, so the incumbent necessarily errs on exactly one side of every pair;
  * the record states how the incumbent's single output differs from the candidate's two-axis
    evaluation, its limits, and carries ids and labels only, never case text;
  * the frozen manifest, preregistration, candidate and both INVALID run records are unchanged and
    the run gate stays closed. Nothing here is an F1-F4 verdict or a qualification.
"""
import json
import socket

import pytest

from tests.test_msnl_context_history_evaluation import MANIFEST_SHA256, PREREG_SHA256
from tests.test_msnl_context_history_evaluation import (
    test_every_recorded_run_is_pinned_distinct_and_the_gate_is_closed as _runs_pinned_and_gate_closed)
from tests.test_msnl_llm_eval_harness import h

POSITIVE = ("AMENDMENT", "HISTORY_COUNTERFACTUAL_NEW", "NEW_DETAIL", "PLAIN_LANGUAGE_DETAIL",
            "RESTATE_THEN_NEW")
EXPECTED_BY_CATEGORY = {   # false credit on negatives, false rejection on positives, of 12 each
    "AMENDMENT": 5, "HISTORY_COUNTERFACTUAL_NEW": 8, "NEW_DETAIL": 4, "PLAIN_LANGUAGE_DETAIL": 8,
    "RESTATE_THEN_NEW": 6, "CONTENT_FREE_REFERENCE": 11, "OTHER_INVENTION_SHARED_VOCAB": 12,
    "PARAPHRASE_OF_PREVIOUS": 4, "PROJECT_COUNTERFACTUAL": 8, "UNKNOWN_OR_UNDECIDED": 3}


@pytest.fixture(scope="module")
def recorded():
    with open(h.CONTEXT_HISTORY_INCUMBENT_BASELINE_PATH, encoding="utf-8") as fh:
        return json.load(fh)


@pytest.fixture(scope="module")
def recomputed():
    def refuse(*_a, **_k):
        raise AssertionError("the incumbent baseline must not open a network connection")
    connect, create = socket.socket.connect, socket.create_connection
    socket.socket.connect, socket.create_connection = refuse, refuse
    try:
        return json.loads(json.dumps(h.context_history_incumbent_baseline(), sort_keys=True))
    finally:
        socket.socket.connect, socket.create_connection = connect, create


def test_the_record_recomputes_exactly_from_the_frozen_manifest(recorded, recomputed):
    assert recorded == recomputed
    assert recorded["manifest_sha256"] == MANIFEST_SHA256
    assert recorded["preregistration_sha256"] == PREREG_SHA256
    assert recorded["engine_contract_version"] == h.CONTEXT_HISTORY_INCUMBENT_ENGINE_VERSION
    assert len(recorded["rows"]) == 120 and all(r["unadjusted"] for r in recorded["rows"])


@pytest.mark.parametrize("prior", ["OPEN", "PARTIAL"])
def test_the_observed_false_credit_and_false_rejection(recorded, prior):
    measures = recorded["measures"][prior]
    assert measures["overall"] == {"false_credit": [38, 60], "false_rejection": [31, 60]}
    assert measures["authored_only"] == {"false_credit": [30, 48], "false_rejection": [23, 48]}
    for category, wrong in EXPECTED_BY_CATEGORY.items():
        axis = "false_rejection" if category in POSITIVE else "false_credit"
        assert measures["by_category"][category][axis] == [wrong, 12], category
    assert measures["by_variety"] == {
        "en": {"false_credit": [19, 30], "false_rejection": [16, 30]},
        "ar-msa": {"false_credit": [19, 30], "false_rejection": [15, 30]}}
    assert measures["by_domain"] == {
        "mechanical": {"false_credit": [18, 30], "false_rejection": [18, 30]},
        "electronics_electrical": {"false_credit": [20, 30], "false_rejection": [13, 30]}}
    assert sorted(measures["by_project_id"]) == ["CH1", "CH2", "CH3", "CH4", "CH5", "CH6"]
    assert sum(g["false_credit"][0] for g in measures["by_project_id"].values()) == 38
    assert sum(g["false_rejection"][0] for g in measures["by_project_id"].values()) == 31
    assert recorded["priors_identical"] is True


def test_every_unrelated_invention_answer_is_credited(recorded):
    """The R2 cross-idea facet (acceptance obligation A2) on every project and language."""
    rows = [r for r in recorded["rows"] if r["category"] == "OTHER_INVENTION_SHARED_VOCAB"]
    assert len(rows) == 12 and all(r["granted"] == {"OPEN": True, "PARTIAL": True} for r in rows)
    assert {r["project_id"] for r in rows} == {"CH1", "CH2", "CH3", "CH4", "CH5", "CH6"}
    assert {r["variety"] for r in rows} == {"en", "ar-msa"}


def test_identical_texts_needing_different_judgements_get_one_incumbent_outcome(recorded):
    pairs = recorded["identical_text_pairs"]
    assert len(pairs) == 24
    combos = sorted(tuple(p["categories"]) for p in pairs)
    assert combos == sorted([("HISTORY_COUNTERFACTUAL_NEW", "PARAPHRASE_OF_PREVIOUS")] * 12
                            + [("NEW_DETAIL", "PROJECT_COUNTERFACTUAL")] * 12)
    index = {r["case_id"]: r for r in recorded["rows"]}
    for pair in pairs:
        assert len(pair["incumbent_granted"]) == 1                  # one outcome for both texts
        labels = {index[c]["frozen_progress_positive"] for c in pair["case_ids"]}
        assert labels == {True, False}                              # so exactly one side is wrong


def test_the_interface_differences_and_limits_are_stated(recorded):
    joined = " ".join(recorded["interface_differences"])
    for phrase in ("never reads the original idea or the preceding answer", "two independent axes",
                   "F3 (over-abstention) and F4 (relation flip) have no incumbent counterpart",
                   "not method equivalence and not an F1-F4 verdict"):
        assert phrase in joined, phrase
    limits = " ".join(recorded["limits"])
    for phrase in ("not a real-user failure rate", "no dialect", "says nothing about the candidate"):
        assert phrase in limits, phrase


def test_the_record_carries_ids_and_labels_only_never_case_text(recorded, manifest_cases):
    raw = json.dumps(recorded, ensure_ascii=False)
    for case in manifest_cases:
        for field in ("original_idea", "preceding_answer", "current_answer"):
            assert case[field] not in raw, (case["case_id"], field)


@pytest.fixture(scope="module")
def manifest_cases():
    return h.context_history_manifest()["cases"]


def test_frozen_inputs_and_both_invalid_runs_are_unchanged():
    manifest = h.context_history_manifest()                         # hash-verified on load
    assert len(manifest["cases"]) == 120
    _runs_pinned_and_gate_closed()
    assert h.CONTEXT_HISTORY_INCUMBENT_BASELINE_PATH not in {
        h.CONTEXT_HISTORY_RUN_01_REPORT_PATH, h.CONTEXT_HISTORY_RUN_01_JOURNAL_PATH,
        h.CONTEXT_HISTORY_RUN_02_REPORT_PATH, h.CONTEXT_HISTORY_RUN_02_JOURNAL_PATH,
        h.CONTEXT_HISTORY_REPORT_PATH, h.CONTEXT_HISTORY_JOURNAL_PATH}
