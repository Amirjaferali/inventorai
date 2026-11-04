"""Held-out v2 pack and pre-registration: identity, independence evidence and decision rule.

Network-free. The replies built here are HANDCRAFTED from the reference to
exercise the decision rule; they are not model results.
"""
import difflib
import json
from pathlib import Path

import pytest

from scripts import g1_precreation_heldout_v2_preregistration as ho
from scripts import run_g1_precreation_semantic_eval as ev
from tests.test_g1_precreation_semantic_eval import CLEAR, _oracle, _reply

ROOT = Path(__file__).resolve().parent.parent
PREREGISTRATION_SHA256 = "b1a7c2c35f38f074c3343b97fd4be9f0d2dd5d98c741de86d27e02e3309e06d1"


@pytest.fixture(scope="module")
def pack():
    return ho.load_heldout()


def _scores(pack, replies=None):
    cases, refs = pack
    replies = replies or {}
    return [ev.score_case(replies.get(c["case_id"], _oracle(c, refs[c["case_id"]])),
                          c["idea_text"], refs[c["case_id"]]) for c in cases]


def _full(scored, refs, **k4):
    items = {k: ev.K6_CLEAR for s in scored for k in s["context_review"]}
    items.update(k4)
    return {"k6": CLEAR, "k4_context": items,
            "g5": {u["unknown_id"]: ev.G5_RECOGNIZED
                   for r in refs.values() for u in r["expected_unknowns"]}}


# ── Frozen identity ─────────────────────────────────────────────────────────
def test_pack_is_pinned_frozen_and_balanced(pack):
    cases, refs = pack
    assert len(cases) == 24 and [c["case_id"] for c in cases] == list(ho.CASE_IDS)
    assert {c["language"] for c in cases} == {"en"}
    assert sorted(r["group"] for r in refs.values()) == sorted("ABCD" * 6)
    assert sum(r["allowed_composition"] == [ev.SUGGEST_INTEGRATED] for r in refs.values()) == 10
    assert sum(len(r["required_parts"]) for r in refs.values()) == 33
    assert sum(len(r["required_negations"]) for r in refs.values()) == 3
    assert sum(len(r["expected_unknowns"]) for r in refs.values()) == 17
    assert sum(bool(r["expected_unknowns"]) for r in refs.values()) == 12
    assert refs["H12"]["expected_unknowns"] == []


def test_preregistration_is_pinned():
    assert ho.preregistration_digest() == PREREGISTRATION_SHA256


def test_a_changed_byte_is_refused(monkeypatch):
    monkeypatch.setattr(ho, "REFERENCE_SHA256", "0" * 64)
    with pytest.raises(ho.PackError):
        ho.load_heldout()


# ── Independence evidence and disposition ───────────────────────────────────
def test_authorship_and_adjudication_records_are_present():
    inputs = json.loads(Path(ho.INPUT_PATH).read_text(encoding="utf-8"))
    reference = json.loads(Path(ho.REFERENCE_PATH).read_text(encoding="utf-8"))
    authorship = json.dumps(inputs["authorship"]).lower()
    assert "28f5d4f" in authorship and "blind" in authorship
    adjudication = reference["adjudication"]
    assert set(adjudication["changes"]) == {"H13", "H16"}
    assert set(adjudication["cases_reviewed"]) == {"H13", "H09", "H12", "H16", "H18", "H05"}
    assert "prompt-blind" in adjudication["adjudicator_statement"]


def test_pack_does_not_reuse_the_v1_campaign_or_the_development_cases(pack):
    v1 = json.loads((ROOT / "tests/fixtures/g1_precreation_semantic_inputs_v1.json").read_text())
    dev = json.loads((ROOT / "tests/fixtures/g1_precreation_semantic_boundary_challenge_v1.json")
                     .read_text())
    earlier = [c["idea_text"].lower() for c in v1["cases"] + dev["cases"]]
    for case in pack[0]:
        text = case["idea_text"].lower()
        assert max(difflib.SequenceMatcher(None, text, e).ratio() for e in earlier) < 0.75


def test_external_context_cases_review_every_stated_part(pack):
    cases, refs = pack
    scored = _scores(pack)
    external = {c for c, r in refs.items()
                if any(f.get("role") == ev.EXTERNAL_CONTEXT for f in r["forbidden_stated_parts"])}
    assert len(external) == 9
    for s in scored:
        parts = len(_oracle(next(c for c in cases if c["case_id"] == s["case_id"]),
                            refs[s["case_id"]])["stated_parts"])
        assert len(s["context_review"]) == (parts if s["case_id"] in external else 0)


# ── Decision rule ───────────────────────────────────────────────────────────
def test_handcrafted_reference_reader_needs_every_review(pack):
    _cases, refs = pack
    scored = _scores(pack)
    assert all(not s["critical"] for s in scored)
    base = ho.baseline()["integrated_recall"]
    assert ho.decide(scored, refs, base, None)["verdict"] == "INCOMPLETE_REVIEW"
    d = ho.decide(scored, refs, base, _full(scored, refs))
    assert d["verdict"] == "PRELIMINARY_GO" and d["by_group"] == {g: 6 for g in "ABCD"}


def test_one_false_integration_on_an_external_device_is_no_go(pack):
    cases, refs = pack
    b = next(c for c in cases if refs[c["case_id"]]["group"] == "B"
             and ev.SUGGEST_INTEGRATED not in refs[c["case_id"]]["allowed_composition"]
             and refs[c["case_id"]]["required_parts"])
    good = _oracle(b, refs[b["case_id"]])
    concepts = {p["candidate_concept"] for p in good["stated_parts"]}
    other = next(d for d in ev.subsystem_model.COMPOSITION_DOMAINS if d not in concepts)
    forged = dict(good, composition_suggestion=ev.SUGGEST_INTEGRATED,
                  stated_parts=good["stated_parts"] + [
                      {"text": "device", "source_quote": good["stated_parts"][0]["source_quote"],
                       "candidate_concept": other}])
    scored = _scores(pack, {b["case_id"]: forged})
    d = ho.decide(scored, refs, ho.baseline()["integrated_recall"], _full(scored, refs))
    assert d["verdict"] == "NO_GO" and "K3" in d["critical"]


def test_group_floor_is_enforced(pack):
    cases, refs = pack
    group_c = [c for c in cases if refs[c["case_id"]]["group"] == "C"
               and ev.NO_INTEGRATED_SUGGESTION not in refs[c["case_id"]]["allowed_composition"]][:2]
    wrong = {c["case_id"]: _reply(composition_suggestion=ev.NO_INTEGRATED_SUGGESTION)
             for c in group_c}
    assert len(wrong) == 2
    scored = _scores(pack, wrong)
    d = ho.decide(scored, refs, ho.baseline()["integrated_recall"], _full(scored, refs))
    assert d["by_group"]["C"] == 4 and d["graded"]["GA"] is False and d["verdict"] == "NO_GO"


def test_missing_case_is_incomplete(pack):
    _cases, refs = pack
    assert ho.decide(_scores(pack)[:-1], refs, 0.0, None)["verdict"] == "INCOMPLETE"


def test_provider_error_on_any_case_is_incomplete_even_with_every_review_clear(pack):
    """Review finding 1: one errored case (no reply) must not reach a verdict."""
    _cases, refs = pack
    scored = _scores(pack, {"H08": None})
    d = ho.decide(scored, refs, ho.baseline()["integrated_recall"], _full(scored, refs))
    assert d == {"verdict": "INCOMPLETE", "provider_errors": ["H08"]}


def test_superseded_identity_is_recorded_and_never_evaluated():
    pre = ho.preregistration()
    assert pre["supersedes"] == [{
        "preregistration_sha256": "d4df1e33c9eefbecec4b7a381fbe2ff1f0de9a3f65f9ae25452ac0a82b7243d5",
        "reference_sha256": "6748366706acde0c36d1a9e89a0b01fb33da7257f19c6ee3e44afa5ddad7d31b",
        "evaluated": False}]
    reference = json.loads(Path(ho.REFERENCE_PATH).read_text(encoding="utf-8"))
    assert set(reference["post_review_correction"]["changes"]) == {"H12"}


# ── Boundaries ──────────────────────────────────────────────────────────────
def test_offline_only_and_v1_untouched():
    src = (ROOT / "scripts/g1_precreation_heldout_v2_preregistration.py").read_text()
    for banned in ("urllib", "allow_network", "OpenAIMsnlAdapter", "technical_orchestration_openai",
                   "--provider", "managed_credential"):
        assert banned not in src
    for folder in ("engine", "web"):
        for path in (ROOT / folder).rglob("*.py"):
            assert "g1_precreation_heldout_v2" not in path.read_text(encoding="utf-8")
    assert ev.preregistration_digest() == (
        "aae4a9af41d84616409badfcc77b9a313bae40dcc0919b69851de6b231285e1f")
