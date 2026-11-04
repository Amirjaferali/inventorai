"""Offline checks for a distinct G1 semantic v2 evaluation candidate.

Passing means construction and isolation, not model competence or qualification.
"""
import json
from pathlib import Path

import pytest

from engine import domain_activation
from scripts import g1_precreation_semantic_v2_candidate as candidate
from scripts import run_g1_precreation_semantic_eval as v1

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts/run_g1_precreation_campaign.py"
V1_REPORT = ROOT / "docs/benchmarks/evidence/g1_precreation_semantic_v1/campaign_01_report.json"

def test_candidate_changes_only_two_known_instruction_spans():
    concepts = v1.governed_concepts()
    original = v1._instructions(concepts)
    proposed = candidate.candidate_instructions(concepts)
    assert proposed != original
    assert candidate.ORIGINAL_COMPONENT_RULE in original
    assert candidate.ORIGINAL_COMPOSITION_RULE in original
    assert candidate.ORIGINAL_COMPONENT_RULE not in proposed
    assert candidate.ORIGINAL_COMPOSITION_RULE not in proposed
    assert proposed == (original.replace(
        candidate.ORIGINAL_COMPONENT_RULE,
        candidate.CANDIDATE_COMPONENT_RULE, 1).replace(
        candidate.ORIGINAL_COMPOSITION_RULE,
        candidate.CANDIDATE_COMPOSITION_RULE, 1))
    assert "source_quote" in proposed
    assert "UNVERIFIED" in proposed
    assert "Output only the JSON object." in proposed
    assert "explicitly intends to install" in proposed
    assert "while that device remains separate" in proposed
    assert "Do NOT choose CLARIFY_FIRST merely because dimensions" in proposed

def test_candidate_request_reuses_existing_schema_and_accepts_idea_only():
    idea = "I am fitting my old circuit board into a new wooden case."
    view = candidate.candidate_request_view(idea)
    assert set(view) == {"instructions", "input", "schema"}
    assert json.loads(view["input"]) == {"idea_text": idea}
    assert view["schema"] == v1._schema(v1.governed_concepts())
    assert view["instructions"] == candidate.candidate_instructions()
    for bad in (None, "", "   ", [], {}):
        with pytest.raises(ValueError):
            candidate.candidate_request_view(bad)

def test_canonical_domain_activation_still_controls_candidate_concepts(monkeypatch):
    monkeypatch.setattr(domain_activation, "is_activated", lambda d, *a, **k: d != "mechanical")
    active = v1.governed_concepts()
    assert "mechanical" not in active
    schema = candidate.candidate_request_view("I want a circuit board.")["schema"]
    enum = schema["properties"]["stated_parts"]["items"]["properties"]["candidate_concept"]["enum"]
    assert enum == list(active)
    assert candidate.candidate_instructions(active).count("NO_GOVERNED_MAPPING") > 0

def test_original_campaign_is_consumed_and_not_an_implicit_v2_run():
    report = json.loads(V1_REPORT.read_text(encoding="utf-8"))
    assert report["manifest_sha256"] == (
        "8e149e563ddf21857370beb6767b5975e29fcfb7fa205845e0406aaafcbf094d")
    assert report["requests"] == 20
    assert v1.PREREGISTRATION_REVISION == 4
    assert v1.preregistration_digest() == (
        "aae4a9af41d84616409badfcc77b9a313bae40dcc0919b69851de6b231285e1f")
    runner = RUNNER.read_text(encoding="utf-8")
    assert "ev.load_pack()" in runner
    assert "g1_precreation_semantic_v2_candidate" not in runner
    assert "AUTHORIZED_RUN_MANIFEST_SHA256 = None" in runner

def test_changes_are_prompt_only_and_never_duplicate_validator():
    source = (ROOT / "scripts/g1_precreation_semantic_v2_candidate.py").read_text(
        encoding="utf-8")
    assert "def candidate_instructions(" in source
    assert "def candidate_request_view(" in source
    assert "def validate(" not in source
    assert "def score_case(" not in source
    assert "OpenAIMsnlAdapter" not in source
    assert "requests.post" not in source
