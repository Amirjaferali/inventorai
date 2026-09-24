"""MSNL Evaluation Pack V1 — provider-neutral, local, synthetic.

File-creation contract:
  Path: tests/test_msnl_evaluation_pack.py
  Purpose: validate the fixed-label SYNTHETIC evaluation pack
    `tests/fixtures/msnl_evaluation_pack_v1.json` and provide the reusable,
    pure evaluation harness (`run_pack`, `aggregate`, `pairwise_agreement`,
    `report`) that scores ANY MSNL adapter against the same labels — the
    NullAdapter and the uncalibrated LexicalBaselineAdapter today, a future
    local or external adapter later, with no label change.
  Input contract: the committed pack + `engine.msnl_shadow` + the committed
    `engine.semantic_registry` inventory. No provider, no model, no network,
    no web app, no store, no real user data.
  Output contract: pass/fail on pack schema, label legality and harness
    mechanics ONLY. An adapter's semantic score is REPORTED, never a CI
    threshold: the lexical baseline is expected to miss valid paraphrase and
    dialect wording, and those misses are measurements, not defects.
  Prohibited behaviors: no registry expansion, no label change to fit an
    adapter, no tuning, no claim of dialect support or semantic precision.
"""
import copy
import json
import pathlib
from collections import namedtuple

import pytest

from engine import msnl_shadow as ms
from engine import semantic_registry

ROOT = pathlib.Path(__file__).resolve().parents[1]
PACK_PATH = ROOT / "tests" / "fixtures" / "msnl_evaluation_pack_v1.json"
PACK_REF = "msnl-evaluation-pack-v1"

VARIETIES = ("en", "ar-msa", "ar-gulf-kw", "ar-egy")
EXPECTATIONS = ("MATCH", "ABSTAIN", "NO_MAPPING")
CATEGORIES = ("PARAPHRASE_EQUIVALENCE", "NEGATION", "AMBIGUOUS", "EXCLUDED_COLLISION",
              "UNRELATED_TECHNICAL", "CROSS_GAP_WORD", "UNSUPPORTED_WORDING",
              "MULTIPLE_PLAUSIBLE")
DOMAINS = ("electronics_electrical", "mechanical")
CASE_KEYS = {"case_id", "group_id", "variety", "category", "gap_type", "domain",
             "question_target", "expectation", "expected_concepts", "text"}
#: The named pairs the Owner asked to see, in report order.
NAMED_PAIRS = (("en", "ar-msa"), ("ar-msa", "ar-gulf-kw"), ("ar-msa", "ar-egy"),
               ("ar-gulf-kw", "ar-egy"), ("en", "ar-gulf-kw"), ("en", "ar-egy"))


# ─────────────────────────────────────────────────────────────────────────────
# The reusable harness (pure; importable by a future adapter evaluation)
# ─────────────────────────────────────────────────────────────────────────────

CaseResult = namedtuple("CaseResult", (
    "case_id", "group_id", "variety", "category", "expectation", "expected",
    "outcome", "disposition", "predicted", "exact", "false_attribution",
    "abstained", "unsupported", "outcome_kind_agrees"))


def load_pack(path=PACK_PATH):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _event(case):
    return ms.AcceptedEvent(
        ref=ms.LocalRef(PACK_REF, case["case_id"]),
        accepted_text=case["text"], gap_type=case["gap_type"],
        question_target=case["question_target"], domain=case["domain"],
        kind=ms.EVENT_ANSWERED)


def score_case(case, result):
    """Score one adapter result against the case's FIXED label."""
    expected = frozenset(case["expected_concepts"])
    predicted = frozenset(result.concept_ids)
    if case["expectation"] == "MATCH":
        exact = predicted == expected
        false_attribution = bool(predicted - expected)
        kind = exact
    else:
        exact = not predicted
        false_attribution = bool(predicted)
        kind = result.outcome == case["expectation"]
    return CaseResult(
        case["case_id"], case["group_id"], case["variety"], case["category"],
        case["expectation"], expected, result.outcome, result.disposition,
        predicted, exact, false_attribution, not predicted,
        result.disposition == ms.DISPOSITION_DISCARDED_UNSUPPORTED, kind)


def run_pack(adapter, pack=None):
    """Evaluate every case through the unchanged local policy
    (`msnl_shadow.evaluate`). Labels are read, never written."""
    pack = load_pack() if pack is None else pack
    return tuple(score_case(case, ms.evaluate(_event(case), adapter))
                 for case in pack["cases"])


def _ratio(num, den):
    return None if den == 0 else round(num / den, 4)


def aggregate(results):
    """Coverage and precision are reported separately: an adapter that
    abstains often can be precise while covering little."""
    n = len(results)
    match = [r for r in results if r.expectation == "MATCH"]
    safe = [r for r in results if r.expectation != "MATCH"]
    proposals = [r for r in results if r.predicted]
    covered = sum(r.exact for r in match)
    return {
        "cases": n,
        "exact_agreement": _ratio(sum(r.exact for r in results), n),
        "false_attribution_rate": _ratio(sum(r.false_attribution for r in results), n),
        "false_attributions": sum(r.false_attribution for r in results),
        "abstention_rate": _ratio(sum(r.abstained for r in results), n),
        "unsupported_concept_rate": _ratio(sum(r.unsupported for r in results), n),
        "outcome_kind_agreement": _ratio(sum(r.outcome_kind_agrees for r in results), n),
        "match_cases": len(match),
        "coverage": _ratio(covered, len(match)),
        "coverage_gap": None if not match else round(1 - covered / len(match), 4),
        "proposals": len(proposals),
        "precision": _ratio(sum(not r.false_attribution for r in proposals),
                            len(proposals)),
        "safe_cases": len(safe),
        "safe_case_correct_rate": _ratio(sum(r.exact for r in safe), len(safe)),
    }


def pairwise_agreement(results, a, b):
    """Over paired groups holding both varieties: `agreement` = the same
    predicted set; `correct_agreement` = both exactly right."""
    by_group = {}
    for r in results:
        if r.group_id is not None:
            by_group.setdefault(r.group_id, {})[r.variety] = r
    pairs = [(g[a], g[b]) for g in by_group.values() if a in g and b in g]
    return {"pairs": len(pairs),
            "agreement": _ratio(sum(x.predicted == y.predicted for x, y in pairs), len(pairs)),
            "correct_agreement": _ratio(sum(x.exact and y.exact for x, y in pairs), len(pairs))}


def report(adapter, pack=None):
    results = run_pack(adapter, pack)
    return {
        "adapter": getattr(adapter, "name", "unnamed"),
        "overall": aggregate(results),
        "by_variety": {v: aggregate([r for r in results if r.variety == v])
                       for v in VARIETIES},
        "pairs": {a + "~" + b: pairwise_agreement(results, a, b) for a, b in NAMED_PAIRS},
        "by_category": {c: aggregate([r for r in results if r.category == c])
                        for c in CATEGORIES},
    }


# ─────────────────────────────────────────────────────────────────────────────
# Pack schema and label legality (CI gates)
# ─────────────────────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def pack():
    return load_pack()


def _committed_question_gaps():
    gaps = {}
    for domain in DOMAINS:
        path = (ROOT / "docs" / "governance" / "path_n_content_config"
                / (domain + "_question_intent_registry.json"))
        for record in json.loads(path.read_text(encoding="utf-8"))["records"]:
            gaps[(domain, "PATHN:" + record["question_id"])] = record["design_gap_id"]
    return gaps


class TestPackSchema:

    def test_pack_is_declared_synthetic_with_bounded_vocabularies(self, pack):
        assert pack["pack_id"] == PACK_REF
        assert pack["status"] == "SYNTHETIC"
        for phrase in ("SYNTHETIC", "NOT real-user evidence", "no universal Arabic-dialect",
                       "never change to fit an adapter", "registry expansion"):
            assert phrase in pack["notice"], phrase
        assert tuple(pack["varieties"]) == VARIETIES
        assert tuple(pack["expectation_types"]) == EXPECTATIONS
        assert tuple(pack["categories"]) == CATEGORIES

    def test_every_case_has_exactly_the_declared_fields(self, pack):
        assert pack["cases"]
        for case in pack["cases"]:
            assert set(case) == CASE_KEYS, case["case_id"]
            assert isinstance(case["text"], str) and case["text"].strip()
            assert isinstance(case["expected_concepts"], list)

    def test_case_ids_are_unique(self, pack):
        ids = [c["case_id"] for c in pack["cases"]]
        assert len(ids) == len(set(ids))

    def test_labels_come_from_the_declared_vocabularies(self, pack):
        for case in pack["cases"]:
            assert case["variety"] in VARIETIES, case["case_id"]
            assert case["expectation"] in EXPECTATIONS, case["case_id"]
            assert case["category"] in CATEGORIES, case["case_id"]
            assert case["domain"] in DOMAINS, case["case_id"]
            assert case["gap_type"] in semantic_registry.GOVERNED_OWNERS, case["case_id"]

    def test_every_variety_and_category_is_represented(self, pack):
        assert {c["variety"] for c in pack["cases"]} == set(VARIETIES)
        assert {c["category"] for c in pack["cases"]} == set(CATEGORIES)

    def test_expectation_semantics(self, pack):
        for case in pack["cases"]:
            ids = case["expected_concepts"]
            assert len(ids) == len(set(ids)), case["case_id"]
            if case["expectation"] == "MATCH":
                assert ids, case["case_id"]
            else:
                assert ids == [], case["case_id"]
            if case["category"] == "PARAPHRASE_EQUIVALENCE":
                assert case["expectation"] == "MATCH", case["case_id"]
            else:
                assert case["expectation"] != "MATCH", case["case_id"]

    def test_every_expected_concept_exists_and_belongs_to_the_declared_gap(self, pack):
        owner = {c.concept_id: c.owner for c in semantic_registry.CONCEPTS}
        for case in pack["cases"]:
            for concept_id in case["expected_concepts"]:
                assert concept_id in owner, (case["case_id"], concept_id)
                assert owner[concept_id] == case["gap_type"], (case["case_id"], concept_id)

    def test_question_targets_are_committed_and_match_the_gap(self, pack):
        committed = _committed_question_gaps()
        for case in pack["cases"]:
            target = case["question_target"]
            if target is None:
                continue
            key = (case["domain"], target)
            assert key in committed, case["case_id"]
            assert committed[key] == case["gap_type"], case["case_id"]
            # a valid observation for the shadow contract
            ms.AcceptedEvent(ref=ms.LocalRef(PACK_REF, case["case_id"]),
                             accepted_text=case["text"], gap_type=case["gap_type"],
                             question_target=target, domain=case["domain"],
                             kind=ms.EVENT_ANSWERED)

    def test_paired_groups_share_one_label_across_distinct_varieties(self, pack):
        groups = {}
        for case in pack["cases"]:
            if case["group_id"] is not None:
                groups.setdefault(case["group_id"], []).append(case)
        assert len(groups) >= 12
        for gid, cases in groups.items():
            assert len(cases) >= 2, gid
            varieties = [c["variety"] for c in cases]
            assert len(varieties) == len(set(varieties)), gid
            for field in ("gap_type", "expectation", "category"):
                assert len({c[field] for c in cases}) == 1, (gid, field)
            assert len({tuple(sorted(c["expected_concepts"])) for c in cases}) == 1, gid
        full = [g for g, cs in groups.items() if {c["variety"] for c in cs} == set(VARIETIES)]
        assert len(full) >= 12, "every paraphrase group covers all four varieties"

    def test_pack_does_not_reuse_the_t1c_study_corpus(self, pack):
        corpus = ROOT / "docs" / "validation" / "T1C_STANDARDIZED_STUDY_CORPUS_V1.md"
        if corpus.exists():
            text = corpus.read_text(encoding="utf-8")
            for case in pack["cases"]:
                assert case["text"] not in text, case["case_id"]


# ─────────────────────────────────────────────────────────────────────────────
# Harness mechanics (CI gates) — never a semantic threshold
# ─────────────────────────────────────────────────────────────────────────────

class _Oracle:
    """A perfect adapter built from the labels, used only to prove the metric
    arithmetic. It is not an MSNL adapter and never ships."""

    name = "test-oracle"

    def __init__(self, pack):
        self.labels = {c["text"]: c for c in pack["cases"]}

    def propose(self, request):
        case = self.labels[request.accepted_text]
        if case["expectation"] == "MATCH":
            order = [c.concept_id for c in request.candidates]
            ids = tuple(sorted(case["expected_concepts"], key=order.index))
            return ms.ShadowResponse(ms.PROPOSED, ids)
        return ms.ShadowResponse(case["expectation"])


class _AlwaysOutOfGap:
    name = "test-out-of-gap"

    def propose(self, request):
        return ms.ShadowResponse(ms.PROPOSED, ("NOT-A-REGISTERED-CONCEPT",))


class TestHarness:

    def test_null_adapter_abstains_everywhere(self, pack):
        results = run_pack(ms.NullAdapter(), pack)
        assert all(r.outcome == ms.ABSTAIN and not r.predicted for r in results)
        overall = aggregate(results)
        assert overall["false_attribution_rate"] == 0
        assert overall["abstention_rate"] == 1
        assert overall["coverage"] == 0 and overall["coverage_gap"] == 1
        assert overall["precision"] is None and overall["proposals"] == 0
        assert overall["safe_case_correct_rate"] == 1

    def test_perfect_oracle_scores_perfectly(self, pack):
        overall = aggregate(run_pack(_Oracle(pack), pack))
        assert overall["exact_agreement"] == 1
        assert overall["outcome_kind_agreement"] == 1
        assert overall["false_attribution_rate"] == 0
        assert overall["coverage"] == 1 and overall["precision"] == 1
        pairs = pairwise_agreement(run_pack(_Oracle(pack), pack), "en", "ar-msa")
        assert pairs["pairs"] >= 12 and pairs["correct_agreement"] == 1

    def test_unsupported_concepts_are_counted_and_never_credited(self, pack):
        overall = aggregate(run_pack(_AlwaysOutOfGap(), pack))
        assert overall["unsupported_concept_rate"] == 1
        assert overall["exact_agreement"] == _ratio(overall["safe_cases"], overall["cases"])
        assert overall["coverage"] == 0 and overall["false_attribution_rate"] == 0

    def test_lexical_baseline_is_evaluated_without_changing_any_label(self, pack):
        before_bytes = PACK_PATH.read_bytes()
        frozen = copy.deepcopy(pack)
        results = run_pack(ms.LexicalBaselineAdapter(), pack)
        assert pack == frozen
        assert PACK_PATH.read_bytes() == before_bytes
        assert len(results) == len(pack["cases"])
        assert all(r.outcome in (ms.PROPOSED, ms.NO_MAPPING) for r in results)
        # every baseline proposal stays inside the served gap's registry
        for r in results:
            assert not r.unsupported

    def test_metrics_are_deterministic(self, pack):
        first = report(ms.LexicalBaselineAdapter(), pack)
        second = report(ms.LexicalBaselineAdapter(), pack)
        assert first == second
        shuffled = dict(pack, cases=list(reversed(pack["cases"])))
        assert report(ms.LexicalBaselineAdapter(), shuffled)["overall"] == first["overall"]

    def test_baseline_report_is_well_formed_and_threshold_free(self, pack):
        rep = report(ms.LexicalBaselineAdapter(), pack)
        assert rep["adapter"] == "lexical-baseline-uncalibrated"
        for section in [rep["overall"], *rep["by_variety"].values(),
                        *rep["by_category"].values()]:
            for key, value in section.items():
                if value is not None and key not in (
                        "cases", "match_cases", "proposals", "safe_cases",
                        "false_attributions"):
                    assert 0 <= value <= 1, key
        assert sum(v["cases"] for v in rep["by_variety"].values()) == len(pack["cases"])

    def test_evaluation_touches_no_product_state(self, pack, monkeypatch):
        def forbidden(*a, **k):
            raise AssertionError("capture seam reached from the evaluation harness")
        monkeypatch.setattr(ms, "capture_accepted_event", forbidden)
        monkeypatch.setattr(ms, "_capture_sink", forbidden)
        registry_before = tuple(semantic_registry.CONCEPTS)
        report(ms.LexicalBaselineAdapter(), pack)
        report(ms.NullAdapter(), pack)
        assert tuple(semantic_registry.CONCEPTS) == registry_before
        assert ms.MSNL_CAPTURE_ENABLED is False
        source = pathlib.Path(__file__).read_text(encoding="utf-8")
        for forbidden_import in ("import web", "from web", "record_store",
                                 "progression_loop", "session_reconstruction"):
            assert forbidden_import not in source.replace(
                '"' + forbidden_import + '"', ""), forbidden_import
