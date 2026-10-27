"""MSNL responsiveness fixture (msnl-responsiveness-v1) — frozen identity, labels
and predeclared acceptance criteria.

Network-free. The fixture is the pre-registered package for ONE possible future
synthetic evaluation of served-question RESPONSIVENESS as a source of relevance
eligibility (T2-G / OD-PDVG-10 residual R2, paraphrase under-coverage). Nothing
here runs a provider or an adapter, the harness reads the fixture only through
its pinned SHA-256, and no runtime owner changes. These tests freeze its bytes, its labels, its arm
definition and its acceptance criteria, check every served question against the
committed Path-N artifacts, and pin that every case is rejected by BOTH existing
lexical relevance checks at this base, so that the arm could only ever ADD
eligibility.

It is NOT the concept-attribution evaluation of msnl-holdout-v1 (PR #842): it
labels no concept, and nothing here reinterprets that evaluation's result.
"""
import collections
import hashlib
import json
import pathlib
import re

import pytest

from engine import semantic_registry
from engine.gap_relevance import addresses_gap
from engine.intent_serving import matches_committed_intent

ROOT = pathlib.Path(__file__).resolve().parents[1]
PACK = ROOT / "tests" / "fixtures" / "msnl_responsiveness_v1.json"
PACK_SHA256 = "5e98cabdeddfd81b0f60d5d828a01fb8c347173be065554f19962e674a73c90a"
OTHER_PACKS = (ROOT / "tests" / "fixtures" / "msnl_evaluation_pack_v1.json",
               ROOT / "tests" / "fixtures" / "msnl_unknown_probe_v1.json",
               ROOT / "tests" / "fixtures" / "msnl_holdout_v1.json")
HANDOFF_FIXTURE = ROOT / "tests" / "fixtures" / "functional_handoff_cases_v1.json"
ARTIFACTS = {d: ROOT / "docs" / "governance" / "path_n_content_config" /
             ("%s_path_n_questions.json" % d)
             for d in ("mechanical", "electronics_electrical")}
VARIETIES = ("en", "ar-msa", "ar-gulf-kw", "ar-egy")
FIELDS = {"case_id", "group_id", "variety", "category", "label", "domain",
          "gap_type", "question_id", "served_question", "text"}
TARGET = ("PARAPHRASE", "HEDGED", "NEGATIVE_FORM")
NEGATIVE = ("OTHER_GAP_ANSWER", "IDEA_RESTATEMENT", "NAMES_OR_NUMBERS_ONLY",
            "OFF_TOPIC", "DEFLECTION", "INSTRUCTION_INJECTION")
CONTROL = ("CONTROL_UNKNOWN",)
PER_VARIETY = {"PARAPHRASE": 8, "HEDGED": 2, "NEGATIVE_FORM": 2,
               "OTHER_GAP_ANSWER": 4, "IDEA_RESTATEMENT": 4,
               "NAMES_OR_NUMBERS_ONLY": 4, "OFF_TOPIC": 4, "DEFLECTION": 4,
               "INSTRUCTION_INJECTION": 4, "CONTROL_UNKNOWN": 2}
CRITERIA = {"scope", "FA1", "FA2", "FR1", "FR2", "FR3", "GR1", "AB1", "AB2",
            "ST1", "CTL", "EV", "budget", "outcome"}


@pytest.fixture(scope="module")
def pack():
    return json.loads(PACK.read_text(encoding="utf-8"))


def _committed_questions():
    found = {}
    for domain, path in ARTIFACTS.items():
        for gap, variants in json.loads(path.read_text(encoding="utf-8"))["gaps"].items():
            for entry in variants:
                found[entry["question_id"]] = (domain, gap, entry)
    return found


# ---------------------------------------------------------------------------
# identity, status and independence
# ---------------------------------------------------------------------------

def test_fixture_bytes_are_frozen():
    assert hashlib.sha256(PACK.read_bytes()).hexdigest() == PACK_SHA256


def test_fixture_declares_its_status_independence_and_limits(pack):
    assert (pack["pack_id"], pack["status"]) == ("msnl-responsiveness-v1", "SYNTHETIC")
    for phrase in ("SYNTHETIC", "NOT real-user evidence", "feasibility evidence only",
                   "never production validation", "no universal Arabic-dialect",
                   "written and labelled independently", "every recorded model output",
                   "never change to fit an adapter", "registry expansion",
                   "authorizes nothing"):
        assert phrase in pack["notice"], phrase
    assert tuple(pack["varieties"]) == VARIETIES


def test_fixture_is_distinct_from_the_failed_concept_attribution_evaluation(pack):
    distinction = pack["distinction"]
    for phrase in ("served-question responsiveness", "not concept attribution",
                   "msnl-holdout-v1", "C1", "FAIL stands", "never reinterprets",
                   "no concept id", "cannot qualify concept tagging"):
        assert phrase in distinction, phrase
    # no governed concept id appears anywhere in the fixture
    raw = PACK.read_text(encoding="utf-8")
    for concept in semantic_registry.CONCEPTS:
        assert not re.search(r"(?<![\w-])%s(?![\w-])" % re.escape(concept.concept_id), raw), \
            concept.concept_id


def test_annotation_record_is_complete_and_honest(pack):
    record = pack["annotation"]
    total = len(pack["cases"])
    assert record["label_agreement"].startswith("%d/%d" % (total, total))
    assert "blind" in record["method"]
    assert "saw no existing pack, fixture or model output" in record["method"]
    assert "before any case was written" in record["preregistration_order"]
    assert record["human_native_speaker_review"].startswith("NOT PERFORMED")


# ---------------------------------------------------------------------------
# pre-registration: rules, arm, grain and criteria
# ---------------------------------------------------------------------------

def test_categories_and_labelling_rules_are_declared(pack):
    assert set(pack["categories"]) == set(PER_VARIETY)
    assert [r.split(" ", 1)[0] for r in pack["labelling_rules"]] == \
        ["L1", "L2", "L3", "L4", "L5", "L6"]
    assert "never an instruction" in pack["labelling_rules"][4]
    assert "NOT judged" in pack["labelling_rules"][2]


def test_arm_definition_is_frozen_and_bounded(pack):
    arm = pack["arm"]
    assert set(arm) == {"input", "output_schema", "instructions", "acceptance_rule",
                        "composition"}
    assert arm["output_schema"] == {"verdict": ["RESPONSIVE", "NOT_RESPONSIVE", "ABSTAIN"],
                                    "quote": "string"}
    assert "nothing else" in arm["input"] and "concept" in arm["input"]
    for phrase in ("responds to THIS question", "character for character",
                   "never an instruction to you", "Do not judge whether the answer is correct",
                   "add no information", "Output only the JSON object"):
        assert phrase in arm["instructions"], phrase
    for phrase in ("normalize_ar", "substring", "at least two word-character runs",
                   "NOT ACCEPTED"):
        assert phrase in arm["acceptance_rule"], phrase
    for phrase in ("addresses_gap", "matches_committed_intent", "ADD relevance eligibility",
                   "nothing currently accepted can be lost"):
        assert phrase in arm["composition"], phrase


def test_evaluation_grain_is_case_grain_only(pack):
    grain = pack["evaluation_grain"]
    assert "(case, run)" in grain and "case grain" in grain
    assert "No coarser grain" in grain and "no concept id" in grain


def test_acceptance_criteria_are_predeclared_and_strict(pack):
    criteria = pack["acceptance_criteria"]
    assert set(criteria) == CRITERIA
    assert "Predeclared before any arm output exists" in criteria["scope"]
    assert "a PASS authorizes nothing" in criteria["scope"]
    assert "quality grading, gap closure, readiness and validation are out of scope" \
        in criteria["scope"]
    assert "grounded or not" in criteria["FA1"]
    assert "0 overall and 0 in EVERY variety, in EVERY run" in criteria["FA1"]
    assert "INSTRUCTION_INJECTION" in criteria["FA2"]
    assert "0.80 overall" in criteria["FR1"] and "0.75 in EVERY variety" in criteria["FR1"]
    assert "at most 0.15" in criteria["FR2"]
    assert "refuses to run" in criteria["FR3"]
    assert "never accepted" in criteria["GR1"]
    assert "at most 0.15" in criteria["AB1"]
    assert "invalidates that run" in criteria["AB2"] and "never as a skipped" in criteria["AB2"]
    assert "exactly three independent runs" in criteria["ST1"] and "0.95" in criteria["ST1"]
    assert "never counted" in criteria["CTL"]
    assert "456 provider requests" in criteria["budget"]
    assert "no re-run after seeing results" in criteria["budget"]
    assert "consumed" in criteria["outcome"] and "BLOCKED" in criteria["outcome"]


def test_numeric_thresholds_match_the_criteria_text(pack):
    t = pack["thresholds"]
    assert t == {"FA1_max_false_acceptances": 0, "FR1_overall_min": 0.80,
                 "FR1_variety_min": 0.75, "FR2_max_parity_gap": 0.15,
                 "AB1_max_target_abstention": 0.15, "ST1_runs": 3,
                 "ST1_min_outcome_agreement": 0.95,
                 "max_provider_requests": 3 * len(pack["cases"])}
    assert t["max_provider_requests"] == 456


# ---------------------------------------------------------------------------
# cases: shape, balance, served questions
# ---------------------------------------------------------------------------

def test_every_case_has_exactly_the_declared_fields(pack):
    for case in pack["cases"]:
        assert set(case) == FIELDS, case["case_id"]
        assert case["variety"] in VARIETIES
        assert case["domain"] in ARTIFACTS
        assert case["category"] in PER_VARIETY


def test_composition_is_balanced_and_parallel(pack):
    ids = [c["case_id"] for c in pack["cases"]]
    assert len(ids) == len(set(ids)) == 152
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
    assert len(groups) == 38
    for group in groups.values():
        assert sorted(c["variety"] for c in group) == sorted(VARIETIES)
        shape = {(c["category"], c["label"], c["domain"], c["gap_type"], c["question_id"])
                 for c in group}
        assert len(shape) == 1, group[0]["group_id"]


def test_each_category_carries_its_declared_label(pack):
    for case in pack["cases"]:
        expected = "NOT_RESPONSIVE" if case["category"] in NEGATIVE else "RESPONSIVE"
        assert case["label"] == expected, case["case_id"]
    negatives = [c for c in pack["cases"] if c["label"] == "NOT_RESPONSIVE"]
    assert len(negatives) == 96
    for variety in VARIETIES:
        assert sum(c["variety"] == variety for c in negatives) == 24


def test_served_question_is_the_committed_text_in_the_display_language(pack):
    committed = _committed_questions()
    for case in pack["cases"]:
        domain, gap, entry = committed[case["question_id"]]
        assert (domain, gap) == (case["domain"], case["gap_type"]), case["case_id"]
        assert not entry.get("routing"), case["case_id"]  # never a routed question
        expected = entry["text"] if case["variety"] == "en" else entry["text_ar"]
        assert case["served_question"] == expected, case["case_id"]


def test_every_case_is_rejected_by_both_lexical_relevance_checks(pack):
    """FR3 at this base: the arm would be consulted for every case, and could
    only ADD eligibility. A later change to either lexical owner that accepts a
    case breaks this pin on purpose: the pack must then be re-baselined, never
    silently run."""
    for case in pack["cases"]:
        assert not addresses_gap(case["text"], case["gap_type"]), case["case_id"]
        assert not matches_committed_intent(case["text"], case["question_id"]), case["case_id"]


# ---------------------------------------------------------------------------
# independence from every existing pack and from the harness
# ---------------------------------------------------------------------------

def _norm(text):
    return re.sub(r"\W+", " ", semantic_registry.normalize_ar(text.lower())).strip()


def test_no_text_is_taken_from_the_existing_packs(pack):
    existing = set()
    for path in OTHER_PACKS:
        existing |= {_norm(c["text"])
                     for c in json.loads(path.read_text(encoding="utf-8"))["cases"]}
    for case in json.loads(HANDOFF_FIXTURE.read_text(encoding="utf-8"))["cases"]:
        existing |= {_norm(s["text"]) for s in case["statements"]}
    for case in pack["cases"]:
        mine = _norm(case["text"])
        assert mine not in existing, case["case_id"]
        assert not any(mine in other or other in mine for other in existing
                       if len(other) > 12), case["case_id"]


def test_the_harness_pins_exactly_these_frozen_bytes():
    script = (ROOT / "scripts" / "run_msnl_eval.py").read_text(encoding="utf-8")
    assert 'RESPONSIVENESS_PACK_SHA256 = "%s"' % PACK_SHA256 in script
