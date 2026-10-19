"""MSNL held-out fixture (msnl-holdout-v1) — frozen identity and label integrity.

Network-free. The fixture is feasibility evidence for a FUTURE mitigation
experiment; nothing here runs a provider, and the harness's pinned packs are
unchanged. These tests freeze its bytes, its labels and its predeclared
acceptance criteria, check every label against the governed registry, and show
that the existing evaluation infrastructure can score it.
"""
import collections
import hashlib
import json
import pathlib
import re

import pytest

from engine import msnl_shadow as ms
from engine import semantic_registry

ROOT = pathlib.Path(__file__).resolve().parents[1]
HOLDOUT = ROOT / "tests" / "fixtures" / "msnl_holdout_v1.json"
HOLDOUT_SHA256 = "54397e3d053a0b2ffa0da23344b7804bf27f3951929c9e475139a6a223ec8e97"
OTHER_PACKS = (ROOT / "tests" / "fixtures" / "msnl_evaluation_pack_v1.json",
               ROOT / "tests" / "fixtures" / "msnl_unknown_probe_v1.json")
VARIETIES = ("en", "ar-msa", "ar-gulf-kw", "ar-egy")
FIELDS = {"case_id", "group_id", "variety", "category", "gap_type", "domain",
          "question_target", "expectation", "expected_concepts", "gap_relevant", "text"}
PER_VARIETY = {"SINGLE_STATED": 4, "MULTI_CROSS_QUESTION": 2, "MULTI_SAME_QUESTION": 1,
               "NEGATION": 1, "NEGATION_AS_MEANING": 1, "HEDGE": 1, "SPEC_ONLY": 1}
_QUESTION = {c.concept_id: c.provenance.split(" ", 1)[0] for c in semantic_registry.CONCEPTS}


@pytest.fixture(scope="module")
def pack():
    return json.loads(HOLDOUT.read_text(encoding="utf-8"))


def test_fixture_bytes_are_frozen():
    assert hashlib.sha256(HOLDOUT.read_bytes()).hexdigest() == HOLDOUT_SHA256


def test_fixture_declares_its_status_independence_and_limits(pack):
    assert (pack["pack_id"], pack["status"]) == ("msnl-holdout-v1", "SYNTHETIC")
    for phrase in ("SYNTHETIC", "NOT real-user evidence", "feasibility evidence only",
                   "never production validation", "no universal Arabic-dialect",
                   "independently of msnl-evaluation-pack-v1", "every recorded model output",
                   "never change to fit an adapter", "registry expansion"):
        assert phrase in pack["notice"], phrase
    assert tuple(pack["varieties"]) == VARIETIES
    assert set(pack["categories"]) == set(PER_VARIETY)
    assert [r.split(" ", 1)[0] for r in pack["labelling_rules"]] == \
        ["R1", "R2", "R3", "R4", "R5", "R6", "R7"]


def test_annotation_record_is_complete_and_honest(pack):
    record = pack["annotation"]
    assert record["label_agreement"].startswith("%d/%d" % (len(pack["cases"]), len(pack["cases"])))
    assert "blind" in record["method"]
    assert record["human_native_speaker_review"].startswith("NOT PERFORMED")


def test_acceptance_criteria_are_predeclared_and_strict(pack):
    criteria = pack["acceptance_criteria"]
    assert set(criteria) == {"scope", "C1", "C2", "C3", "C4", "C5", "C6", "C7"}
    assert "EVERY variety" in criteria["C1"] and "no increase in any variety" in criteria["C1"]
    assert "Concept grain decides" in criteria["scope"]
    assert "Feasibility evidence only" in criteria["scope"]
    assert "follows each case's label" in criteria["C4"]
    assert "reported separately" in criteria["C6"]
    assert "invalidates" in criteria["C7"]


def test_every_case_has_exactly_the_declared_fields(pack):
    for case in pack["cases"]:
        assert set(case) == FIELDS, case["case_id"]
        assert case["question_target"] is None
        assert case["domain"] in ("mechanical", "electronics_electrical")


def test_composition_is_balanced_and_parallel(pack):
    ids = [c["case_id"] for c in pack["cases"]]
    assert len(ids) == len(set(ids)) == 44
    texts = [c["text"] for c in pack["cases"]]
    assert len(texts) == len(set(texts))
    for variety in VARIETIES:
        counts = collections.Counter(c["category"] for c in pack["cases"]
                                     if c["variety"] == variety)
        assert counts == PER_VARIETY, variety
    groups = collections.defaultdict(list)
    for case in pack["cases"]:
        assert case["case_id"] == case["group_id"] + "-" + case["variety"]
        groups[case["group_id"]].append(case)
    for group in groups.values():
        assert sorted(c["variety"] for c in group) == sorted(VARIETIES)
        labels = {(c["category"], c["gap_type"], tuple(sorted(c["expected_concepts"])),
                   c["expectation"], c["gap_relevant"]) for c in group}
        assert len(labels) == 1, group[0]["group_id"]


def test_labels_are_registry_concepts_of_the_served_gap(pack):
    for case in pack["cases"]:
        allowed = {c.concept_id for c in ms.candidate_concepts(case["gap_type"])}
        assert allowed, case["case_id"]
        assert set(case["expected_concepts"]) <= allowed, case["case_id"]
        assert (case["expectation"] == "MATCH") == bool(case["expected_concepts"]), case["case_id"]


def test_each_category_carries_its_declared_label_shape(pack):
    for case in pack["cases"]:
        concepts, category = case["expected_concepts"], case["category"]
        questions = {_QUESTION[i] for i in concepts}
        if category == "SINGLE_STATED":
            assert len(concepts) == 1 and case["gap_relevant"]
        elif category == "MULTI_CROSS_QUESTION":
            assert len(concepts) == 2 and len(questions) == 2
        elif category == "MULTI_SAME_QUESTION":
            assert len(concepts) == 2 and len(questions) == 1
        elif category == "NEGATION":
            assert (case["expectation"], case["gap_relevant"]) == ("ABSTAIN", True)
        elif category == "NEGATION_AS_MEANING":
            assert concepts == ["BA-NOT-COVER"] and case["gap_relevant"]
        elif category == "HEDGE":
            assert (case["expectation"], case["gap_relevant"]) == ("ABSTAIN", True)
        elif category == "SPEC_ONLY":
            assert (case["expectation"], case["gap_relevant"]) == ("NO_MAPPING", False)


def _norm(text):
    return re.sub(r"\W+", " ", semantic_registry.normalize_ar(text.lower())).strip()


def test_no_text_is_taken_from_the_existing_packs(pack):
    existing = set()
    for path in OTHER_PACKS:
        existing |= {_norm(c["text"]) for c in json.loads(path.read_text(encoding="utf-8"))["cases"]}
    for case in pack["cases"]:
        mine = _norm(case["text"])
        assert mine not in existing, case["case_id"]
        assert not any(mine in other or other in mine for other in existing if len(other) > 12), \
            case["case_id"]


def test_existing_infrastructure_scores_it_without_any_network(pack, monkeypatch):
    from engine import technical_orchestration_openai as toa
    from tests.test_msnl_evaluation_pack import aggregate, run_pack
    import importlib.util

    def no_network(*_a, **_k):
        raise AssertionError("the held-out fixture must be scored offline here")
    monkeypatch.setattr(toa, "_urllib_transport", no_network)
    results = run_pack(ms.LexicalBaselineAdapter(), pack)
    assert len(results) == 44 and aggregate(results)["cases"] == 44
    spec = importlib.util.spec_from_file_location(
        "run_msnl_eval", ROOT / "scripts" / "run_msnl_eval.py")
    harness = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(harness)
    grains = harness.grain_report([
        {"variety": r.variety, "expected": sorted(r.expected),
         "predicted": sorted(r.predicted), "disposition": r.disposition} for r in results])
    assert grains["concept"]["overall"]["cases"] == 44


def test_the_harness_pins_exactly_these_frozen_bytes():
    script = (ROOT / "scripts" / "run_msnl_eval.py").read_text(encoding="utf-8")
    assert 'HOLDOUT_PACK_SHA256 = "%s"' % HOLDOUT_SHA256 in script
