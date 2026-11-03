"""G1-LLM-SEMANTIC-BRIDGE-QUALIFICATION-01 — offline preparation guards.

The replies below are HANDCRAFTED test material for the validator and the
scorer. None is a model result and none is evidence that a model understood
anything. No test opens a network connection.
"""
import json
import re
from pathlib import Path

import pytest

from engine import domain_activation
from scripts import run_g1_precreation_semantic_eval as ev

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "run_g1_precreation_semantic_eval.py"
PREREGISTRATION_SHA256 = "fb5c96dcf981b91fde517fc4404c4e3d3f7bb90a23124b0793960d73b54a2a82"


@pytest.fixture(scope="module")
def pack():
    return ev.load_pack()


def _span(text, term):
    """A grounded quote: the term plus its neighbouring word (two word runs)."""
    low = text.lower()
    i = low.index(term)
    words = list(re.finditer(r"\S+", text))
    idx = next(k for k, w in enumerate(words) if w.end() > i)
    end_idx = next(k for k, w in enumerate(words) if w.end() >= i + len(term))
    lo, hi = idx, end_idx
    if hi == lo:
        hi = min(hi + 1, len(words) - 1) if hi + 1 < len(words) else hi
        if hi == lo:
            lo -= 1
    return text[words[lo].start():words[hi].end()].strip(".,;:")


def _reply(**kw):
    base = {"outcome": "RESPONDED", "stated_function": [], "stated_parts": [],
            "negated_or_excluded": [], "unknowns": [], "clarification_questions": [],
            "ai_suggestions": [], "composition_suggestion": ev.NO_INTEGRATED_SUGGESTION}
    base.update(kw)
    return base


def _oracle(case, ref):
    """A reply built FROM the reference: what a perfect reader would return."""
    t = case["idea_text"]
    negs = [{"text": n["any_of"][0], "source_quote": _span(t, n["any_of"][0])}
            for n in ref["required_negations"]]
    parts = [{"text": p["any_of"][0], "source_quote": _span(t, p["any_of"][0]),
              "candidate_concept": p["concept"]} for p in ref["required_parts"]]
    return _reply(stated_parts=parts, negated_or_excluded=negs,
                  unknowns=list(ref["expected_unknowns"]),
                  composition_suggestion=ref["allowed_composition"][0])


# ── Pack, pre-registration and request ───────────────────────────────────────
def test_pack_is_frozen_synthetic_english_and_pinned(pack):
    cases, refs = pack
    assert len(cases) == 20 and set(refs) == {c["case_id"] for c in cases}
    assert {c["language"] for c in cases} == {"en"}
    assert sum(r["allowed_composition"] == [ev.SUGGEST_INTEGRATED] for r in refs.values()) == 6
    assert sum(len(r["required_parts"]) for r in refs.values()) == 25
    assert sum(len(r["required_negations"]) for r in refs.values()) == 3
    assert sum(bool(r["expected_unknowns"]) for r in refs.values()) == 5


def test_preregistration_is_pinned():
    assert ev.preregistration_digest() == PREREGISTRATION_SHA256


def test_request_carries_only_the_idea_text(pack):
    cases, refs = pack
    for case in cases:
        view = ev.request_view(case)
        assert json.loads(view["input"]) == {"idea_text": case["idea_text"]}
        flat = json.dumps(view)
        assert case["case_id"] not in flat
        assert refs[case["case_id"]]["category"] not in flat


# ── INVENTORAI owns the vocabulary ───────────────────────────────────────────
def test_governed_concepts_come_from_the_canonical_owners():
    assert ev.governed_concepts() == ("mechanical", "electronics_electrical",
                                      ev.NO_GOVERNED_MAPPING)
    schema = ev._schema(ev.governed_concepts())
    enum = schema["properties"]["stated_parts"]["items"]["properties"][
        "candidate_concept"]["enum"]
    assert enum == list(ev.governed_concepts())
    assert all(re.fullmatch(r"[a-z_A-Z]+", c) for c in enum)   # ids, never labels


def test_deactivating_a_domain_removes_it_and_blocks_admission(monkeypatch, pack):
    cases, _refs = pack
    monkeypatch.setattr(domain_activation, "is_activated", lambda d, *a, **k: d != "mechanical")
    concepts = ev.governed_concepts()
    assert "mechanical" not in concepts
    t = cases[0]["idea_text"]
    reply = _reply(stated_parts=[
        {"text": "board", "source_quote": "circuit board", "candidate_concept":
         "electronics_electrical"}], composition_suggestion=ev.SUGGEST_INTEGRATED)
    assert ev.validate(reply, t, concepts)["effective"] == ev.NOT_ADMITTED


def test_invented_concept_is_rejected_and_falls_back(pack):
    t = pack[0][0]["idea_text"]
    reply = _reply(stated_parts=[{"text": "x", "source_quote": "circuit board",
                                  "candidate_concept": "robotics"}])
    v = ev.validate(reply, t)
    assert (v["status"], v["effective"]) == (ev.V_REJECTED, ev.FALLBACK)


def test_ungrounded_quote_is_rejected(pack):
    t = pack[0][0]["idea_text"]
    reply = _reply(stated_function=[{"text": "x", "source_quote": "a waterproof motor"}])
    assert ev.validate(reply, t)["effective"] == ev.FALLBACK


def test_suggestion_attribution_is_enforced(pack):
    t = pack[0][0]["idea_text"]
    reply = _reply(ai_suggestions=[{"text": "x", "attribution": "OWNER_STATED",
                                    "status": "UNVERIFIED"}])
    assert ev.validate(reply, t)["status"] == ev.V_REJECTED


def test_integrated_admitted_only_with_both_grounded_non_negated_parts(pack):
    cases, refs = pack
    by_id = {c["case_id"]: c for c in cases}
    good = _oracle(by_id["P01"], refs["P01"])
    assert ev.validate(good, by_id["P01"]["idea_text"])["effective"] == ev.SUGGEST_INTEGRATED
    one = dict(good, stated_parts=good["stated_parts"][:1])
    assert ev.validate(one, by_id["P01"]["idea_text"])["effective"] == ev.NOT_ADMITTED
    t7 = by_id["P07"]["idea_text"]
    negated_case = _reply(
        stated_parts=[{"text": "board", "source_quote": "circuit board",
                       "candidate_concept": "electronics_electrical"},
                      {"text": "case", "source_quote": "any case, housing",
                       "candidate_concept": "mechanical"}],
        negated_or_excluded=[{"text": "no case", "source_quote":
                              "I do not want any case, housing or cover"}],
        composition_suggestion=ev.SUGGEST_INTEGRATED)
    assert ev.validate(negated_case, t7)["effective"] == ev.NOT_ADMITTED


# ── Fallback: failures never become understanding ───────────────────────────
@pytest.mark.parametrize("reply,status", [
    (None, "ERROR"), ({"outcome": "RESPONDED"}, "STRUCTURE_VIOLATION"),
    ("ABSTAIN", "STRUCTURE_VIOLATION"),
])
def test_missing_or_malformed_reply_falls_back(reply, status, pack):
    v = ev.validate(reply, pack[0][0]["idea_text"])
    assert (v["status"], v["effective"]) == (status, ev.FALLBACK)


def test_abstain_must_be_empty_and_reads_as_clarify(pack):
    t = pack[0][0]["idea_text"]
    assert ev.validate(_reply(outcome="ABSTAIN"), t)["effective"] == ev.CLARIFY_FIRST
    dirty = _reply(outcome="ABSTAIN", unknowns=["x"])
    assert ev.validate(dirty, t)["effective"] == ev.FALLBACK


# ── Scorer and decision rule ─────────────────────────────────────────────────
def test_forbidden_part_and_negation_are_critical(pack):
    cases, refs = pack
    by_id = {c["case_id"]: c for c in cases}
    t5 = by_id["P05"]["idea_text"]
    tablet = _reply(stated_parts=[{"text": "tablet", "source_quote": "a tablet",
                                   "candidate_concept": "electronics_electrical"}])
    assert "K4" in ev.score_case(tablet, t5, refs["P05"])["critical"]
    t16 = by_id["P16"]["idea_text"]
    neg = _reply(stated_function=[{"text": "electric", "source_quote": "nothing electric"}])
    assert "K5" in ev.score_case(neg, t16, refs["P16"])["critical"]


def test_handcrafted_oracle_passes_and_one_false_suggestion_fails(pack):
    cases, refs = pack
    scored = [ev.score_case(_oracle(c, refs[c["case_id"]]), c["idea_text"], refs[c["case_id"]])
              for c in cases]
    assert all(not s["critical"] for s in scored)
    base = ev.baseline()["integrated_recall"]
    assert ev.decide(scored, refs, base)["verdict"] == "PRELIMINARY_GO"
    by_id = {c["case_id"]: c for c in cases}
    t7 = by_id["P07"]["idea_text"]
    false_int = _reply(
        stated_parts=[{"text": "board", "source_quote": "circuit board",
                       "candidate_concept": "electronics_electrical"},
                      {"text": "cover", "source_quote": "or cover around",
                       "candidate_concept": "mechanical"}],
        composition_suggestion=ev.SUGGEST_INTEGRATED)
    s7 = ev.score_case(false_int, t7, refs["P07"])
    assert {"K3", "K4", "K5"} <= set(s7["critical"])
    worse = [s7 if s["case_id"] == "P07" else s for s in scored]
    assert ev.decide(worse, refs, base)["verdict"] == "NO_GO"
    assert ev.decide(scored[:-1], refs, base)["verdict"] == "INCOMPLETE"


def test_deterministic_baseline_is_measured_and_matches_start(pack):
    from web import app as web_app
    from engine.domain_rules import classify_domain
    b = ev.baseline()
    assert (b["composition_ok"], b["integrated"]) == (11, 6)
    assert b["integrated_recall"] == pytest.approx(1 / 6)
    for case in pack[0]:
        outcome, _c = ev.deterministic_composition(case["idea_text"])
        tie = web_app._is_exact_composition_tie(classify_domain(case["idea_text"]))
        assert (outcome == ev.SUGGEST_INTEGRATED) == tie


# ── Language independence (no Arabic qualification is claimed) ──────────────
def test_same_contract_validates_an_arabic_reply():
    text = "أريد لوحة دوائر داخل علبة بلاستيكية، ولم أحدد الأبعاد."
    reply = _reply(
        stated_parts=[{"text": "لوحة", "source_quote": "لوحة دوائر",
                       "candidate_concept": "electronics_electrical"},
                      {"text": "علبة", "source_quote": "داخل علبة",
                       "candidate_concept": "mechanical"}],
        unknowns=["الأبعاد"], composition_suggestion=ev.SUGGEST_INTEGRATED)
    assert ev.validate(reply, text)["effective"] == ev.SUGGEST_INTEGRATED
    hamza = dict(reply, stated_parts=[dict(reply["stated_parts"][0],
                                           source_quote="أريد لوحة")] + reply["stated_parts"][1:])
    assert ev.validate(hamza, text.replace("أريد", "اريد"))["status"] == ev.V_VALID


# ── Boundaries: offline only, no product coupling ────────────────────────────
def test_no_provider_path_and_no_product_import():
    src = SCRIPT.read_text(encoding="utf-8")
    for banned in ("urllib", "requests", "allow_network", "OpenAIMsnlAdapter",
                   "technical_orchestration_openai", "--provider", "managed_credential"):
        assert banned not in src, banned
    for folder in ("engine", "web"):
        for path in (ROOT / folder).rglob("*.py"):
            assert "run_g1_precreation_semantic_eval" not in path.read_text(encoding="utf-8")
