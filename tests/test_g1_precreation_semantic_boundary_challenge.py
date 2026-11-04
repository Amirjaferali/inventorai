"""G1 boundary challenge integrity; offline only, no model evaluation or product import."""
import json
from collections import Counter
from pathlib import Path

from engine import subsystem_model, domain_activation
from scripts import run_g1_precreation_semantic_eval as frozen

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "tests/fixtures/g1_precreation_semantic_boundary_challenge_v1.json"
OLD = ROOT / "tests/fixtures/g1_precreation_semantic_inputs_v1.json"
REPORT = ROOT / "docs/benchmarks/evidence/g1_precreation_semantic_v1/campaign_01_report.json"


def _read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_challenge_is_new_synthetic_diagnostic_not_authorized_campaign():
    pack = _read(PATH)
    assert pack["state"] == "DIAGNOSTIC_ONLY_NOT_HOLDOUT"
    assert pack["synthetic_only"] is True
    assert pack["provider_runs_authorized"] is False
    cases = pack["cases"]
    assert len(cases) == 16
    assert len({case["case_id"] for case in cases}) == 16
    assert all(case["synthetic"] is True and case["language"] == "en" for case in cases)
    counts = Counter(case["allowed_composition"][0] for case in cases)
    assert counts == {frozen.SUGGEST_INTEGRATED: 7,
                      frozen.NO_INTEGRATED_SUGGESTION: 7,
                      frozen.CLARIFY_FIRST: 2}
    pairs = Counter(case["case_id"].split("-")[1][0] for case in cases)
    assert len(pairs) == 8 and set(pairs.values()) == {2}


def test_concepts_source_terms_and_admission_cases_are_grounded():
    canonical = set(subsystem_model.COMPOSITION_DOMAINS)
    assert all(domain_activation.is_activated(d) for d in canonical)
    for case in _read(PATH)["cases"]:
        text = case["idea_text"].casefold()
        parts = case["required_parts"]
        assert case["allowed_composition"][0] in frozen.COMPOSITION_OUTCOMES
        assert {p["concept"] for p in parts} <= canonical
        assert all(p["phrase"].casefold() in text for p in parts)
        assert all(term.casefold() in text for term in case["external_context"])
        if case["allowed_composition"] == [frozen.SUGGEST_INTEGRATED]:
            assert {p["concept"] for p in parts} == canonical
            assert case["scenario"] == "included"
        if case["allowed_composition"] == [frozen.CLARIFY_FIRST]:
            assert case["scenario"] in ("vague", "undecided")
        if case["scenario"] == "external":
            assert case["external_context"]
            assert case["allowed_composition"] == [frozen.NO_INTEGRATED_SUGGESTION]
        if case["scenario"] in ("packaging", "single"):
            assert case["allowed_composition"] == [frozen.NO_INTEGRATED_SUGGESTION]
        if case["scenario"] == "packaging":
            assert case["external_context"]


def test_consumed_v1_campaign_remains_separate_and_no_new_run_is_claimed():
    v1 = _read(OLD)
    new = _read(PATH)
    prior = {case["idea_text"].casefold() for case in v1["cases"]}
    assert not prior.intersection(c["idea_text"].casefold() for c in new["cases"])
    assert all(not case["case_id"].startswith("P") for case in new["cases"])
    report = _read(REPORT)
    assert report["requests"] == 20
    assert report["manifest_sha256"] == (
        "8e149e563ddf21857370beb6767b5975e29fcfb7fa205845e0406aaafcbf094d")
    assert frozen.PREREGISTRATION_REVISION == 4
    assert frozen.preregistration_digest() == (
        "aae4a9af41d84616409badfcc77b9a313bae40dcc0919b69851de6b231285e1f")
