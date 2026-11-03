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
PREREGISTRATION_SHA256 = "aae4a9af41d84616409badfcc77b9a313bae40dcc0919b69851de6b231285e1f"


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
                  unknowns=[u["meaning"] for u in ref["expected_unknowns"]],
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
    assert sum(len(r["expected_unknowns"]) for r in refs.values()) == 7


def test_preregistration_revision_4_supersedes_three_unevaluated_revisions():
    pre = ev.preregistration()
    assert pre["revision"] == 4
    assert [(x["revision"], x["sha256"], x["evaluated"]) for x in pre["supersedes"]] == [
        (1, "fb5c96dcf981b91fde517fc4404c4e3d3f7bb90a23124b0793960d73b54a2a82", False),
        (2, "22389804aa27ea5f81c3704d28f17b44b8cd58a0161993e5daa672a3ba83563b", False),
        (3, "cfefe654fcf37d895db42047f68eb68d3a1eb9702b9dbfbe1f136e901db101b7", False)]
    assert ev.preregistration_digest() not in {x["sha256"] for x in pre["supersedes"]}


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


def _all_recognized(refs):
    return {u["unknown_id"]: ev.G5_RECOGNIZED
            for r in refs.values() for u in r["expected_unknowns"]}


CLEAR = {"status": ev.K6_CLEAR, "failed_cases": []}


def _full(scored, refs, **k4):
    """Every human review complete: K6 clear, every G5 unknown recognized and
    every K4 context item clear unless overridden."""
    items = {k: ev.K6_CLEAR for x in scored for k in x["context_review"]}
    items.update(k4)
    return {"k6": CLEAR, "g5": _all_recognized(refs), "k4_context": items}


def _oracle_scores(pack):
    cases, refs = pack
    return [ev.score_case(_oracle(c, refs[c["case_id"]]), c["idea_text"], refs[c["case_id"]])
            for c in cases]


def test_handcrafted_oracle_passes_and_one_false_suggestion_fails(pack):
    cases, refs = pack
    scored = _oracle_scores(pack)
    assert all(not s["critical"] for s in scored)
    base = ev.baseline()["integrated_recall"]
    full = _full(scored, refs)
    assert ev.decide(scored, refs, base, full)["verdict"] == "PRELIMINARY_GO"
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
    assert ev.decide(worse, refs, base, full)["verdict"] == "NO_GO"
    assert ev.decide(scored[:-1], refs, base, full)["verdict"] == "INCOMPLETE"


# ── K6: no record is NOT_ASSESSED, never clear ──────────────────────────────
def test_omitted_k6_review_can_never_give_a_go(pack):
    _cases, refs = pack
    scored, base = _oracle_scores(pack), ev.baseline()["integrated_recall"]
    g5 = _all_recognized(refs)
    for assessment in (None, {"g5": g5}, {"k6": None, "g5": g5}):
        d = ev.decide(scored, refs, base, assessment)
        assert (d["verdict"], d["k6"]) == ("INCOMPLETE_REVIEW", ev.K6_NOT_ASSESSED)
    failed = {"k6": {"status": ev.K6_FAILURE, "failed_cases": ["P04"]}, "g5": g5}
    d = ev.decide(scored, refs, base, failed)
    assert d["verdict"] == "NO_GO" and "K6" in d["critical"]


@pytest.mark.parametrize("k6", [
    {"status": ev.K6_CLEAR, "failed_cases": ["P04"]},
    {"status": ev.K6_FAILURE, "failed_cases": []},
    {"status": ev.K6_FAILURE, "failed_cases": ["P99"]},
    {"status": "PASS", "failed_cases": []},
    {"status": ev.K6_CLEAR},
    {"status": ev.K6_CLEAR, "failed_cases": None},
    {"status": ev.K6_FAILURE, "failed_cases": [["P04"]]},
    "ASSESSED_CLEAR",
])
def test_inconsistent_k6_record_is_refused(k6, pack):
    _cases, refs = pack
    with pytest.raises(ev.PackError):
        ev.decide(_oracle_scores(pack), refs, 0.0, {"k6": k6, "g5": _all_recognized(refs)})


@pytest.mark.parametrize("assessment", [[], "clear", {"k6": CLEAR, "g5": []},
                                        {"k6": CLEAR, "g5": {"P01-U1": True}}])
def test_malformed_assessment_is_refused_not_crashed(assessment, pack):
    _cases, refs = pack
    with pytest.raises(ev.PackError):
        ev.decide(_oracle_scores(pack), refs, 0.0, assessment)


def test_k6_failure_may_name_only_a_reviewed_reply(pack):
    cases, refs = pack
    by_id = {c["case_id"]: c for c in cases}
    scored = [ev.score_case(None, by_id["P05"]["idea_text"], refs["P05"])
              if x["case_id"] == "P05" else x for x in _oracle_scores(pack)]
    with pytest.raises(ev.PackError):
        ev.decide(scored, refs, 0.0, {"k6": {"status": ev.K6_FAILURE, "failed_cases": ["P05"]}})


def test_k6_flags_are_advisory_and_every_answered_reply_is_reviewed(pack):
    cases, refs = pack
    scored = _oracle_scores(pack)
    items = ev.review_items(scored, pack, {c["case_id"]: _oracle(c, refs[c["case_id"]])
                                           for c in cases})
    assert len(items["k6"]) == 20 and all(i["advisory_flags"] == [] for i in items["k6"])
    assert all(i["reply"] is not None for i in items["k6"])


# ── G5: only the frozen unknown, judged by a human, earns credit ─────────────
def test_irrelevant_unknown_earns_no_g5_credit(pack):
    cases, refs = pack
    by_id = {c["case_id"]: c for c in cases}
    irrelevant = dict(_oracle(by_id["P01"], refs["P01"]),
                      unknowns=["what colour the logo should be"], clarification_questions=[])
    s = ev.score_case(irrelevant, by_id["P01"]["idea_text"], refs["P01"])
    assert set(s["unknowns"].values()) == {ev.G5_NOT_ASSESSED}
    assert s["unknown_screen_hits"] == {"P01-U1": False, "P01-U2": False}
    scored = [s if x["case_id"] == "P01" else x for x in _oracle_scores(pack)]
    base = ev.baseline()["integrated_recall"]
    assert ev.decide(scored, refs, base, {"k6": CLEAR})["verdict"] == "INCOMPLETE_REVIEW"
    judged = dict(_all_recognized(refs), **{"P01-U1": ev.G5_NOT_RECOGNIZED,
                                           "P01-U2": ev.G5_NOT_RECOGNIZED})
    d = ev.decide(scored, refs, base, {"k6": CLEAR, "g5": judged})
    assert d["verdict"] == "NO_GO" and d["graded"]["G5"] is False


def test_abstention_is_safe_but_earns_no_g5_credit(pack):
    cases, refs = pack
    by_id = {c["case_id"]: c for c in cases}
    for reply in (_reply(outcome="ABSTAIN"), None, {"outcome": "RESPONDED"}):
        s = ev.score_case(reply, by_id["P10"]["idea_text"], refs["P10"])
        assert set(s["unknowns"].values()) == {ev.G5_NOT_RECOGNIZED}
    s = ev.score_case(_reply(outcome="ABSTAIN"), by_id["P10"]["idea_text"], refs["P10"])
    assert s["critical"] == [] and s["effective"] == ev.CLARIFY_FIRST
    scored = [s if x["case_id"] == "P10" else x for x in _oracle_scores(pack)]
    g5 = {k: v for k, v in _all_recognized(refs).items() if not k.startswith("P10-")}
    d = ev.decide(scored, refs, ev.baseline()["integrated_recall"], {"k6": CLEAR, "g5": g5})
    assert d["verdict"] == "NO_GO" and d["g5"]["recognized"] == 5
    with pytest.raises(ev.PackError):         # an automatic NOT_RECOGNIZED cannot be overruled
        ev.decide(scored, refs, 0.0, {"k6": CLEAR, "g5": _all_recognized(refs)})


def test_g5_review_items_carry_the_frozen_meaning(pack):
    cases, refs = pack
    replies = {c["case_id"]: _oracle(c, refs[c["case_id"]]) for c in cases}
    items = ev.review_items(_oracle_scores(pack), pack, replies)["g5"]
    assert sorted(i["unknown_id"] for i in items) == sorted(_all_recognized(refs))
    assert all(i["meaning"] for i in items)


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


# ── K4 external context (Owner P12 ruling): the handlebar is not a designed part
P12_PCB = {"text": "a PCB", "source_quote": "Picture a PCB",
           "candidate_concept": "electronics_electrical"}


def _p12(*mech):
    return _reply(stated_parts=[P12_PCB, *mech], composition_suggestion=ev.SUGGEST_INTEGRATED)


def _p12_scores(pack, reply):
    cases, refs = pack
    text = next(c["idea_text"] for c in cases if c["case_id"] == "P12")
    s12 = ev.score_case(reply, text, refs["P12"])
    return s12, [s12 if x["case_id"] == "P12" else x for x in _oracle_scores(pack)]


def test_p12_every_stated_part_is_reviewed_whatever_its_wording(pack):
    casing = {"text": "casing", "source_quote": "3D-printed casing", "candidate_concept":
              "mechanical"}
    s12, _scored = _p12_scores(pack, _p12(casing))
    assert s12["critical"] == [] and s12["context_review"] == {
        "P12-part-1": ev.K6_NOT_ASSESSED, "P12-part-2": ev.K6_NOT_ASSESSED}
    other, _ = _p12_scores(pack, _reply(stated_parts=[P12_PCB]))
    assert other["context_review"] == {"P12-part-1": ev.K6_NOT_ASSESSED}
    nothing, _ = _p12_scores(pack, _reply())
    assert nothing["context_review"] == {}


def test_p12_faithful_pcb_and_casing_are_judged_clear_and_stay_valid(pack):
    _cases, refs = pack
    casing = {"text": "a 3D-printed casing", "candidate_concept": "mechanical",
              "source_quote": "casing that clips onto a bike handlebar"}
    s12, scored = _p12_scores(pack, _p12(casing))
    assert s12["critical"] == [] and s12["effective"] == ev.SUGGEST_INTEGRATED
    assert s12["parts_found"] == 2
    base = ev.baseline()["integrated_recall"]
    assert ev.decide(scored, refs, base, _full(scored, refs))["verdict"] == "PRELIMINARY_GO"


@pytest.mark.parametrize("external", [
    {"text": "bicycle handle", "source_quote": "3D-printed casing"},   # no context word at all
    {"text": "the bike handlebar", "source_quote": "a bike handlebar"},
    {"text": "the bar the casing clips onto",
     "source_quote": "casing that clips onto a bike handlebar"},
])
def test_p12_external_part_is_never_clean_unjudged_and_a_failure_is_k4(external, pack):
    _cases, refs = pack
    casing = {"text": "casing", "source_quote": "3D-printed casing", "candidate_concept":
              "mechanical"}
    s12, scored = _p12_scores(pack, _p12(casing, dict(external, candidate_concept="mechanical")))
    assert s12["critical"] == [] and s12["context_review"]["P12-part-3"] == ev.K6_NOT_ASSESSED
    base = ev.baseline()["integrated_recall"]
    pending = _full(scored, refs)
    del pending["k4_context"]["P12-part-3"]
    d = ev.decide(scored, refs, base, pending)
    assert d["verdict"] == "INCOMPLETE_REVIEW" and d["k4_context_not_assessed"] == ["P12-part-3"]
    d = ev.decide(scored, refs, base, _full(scored, refs, **{"P12-part-3": ev.K6_FAILURE}))
    assert d["verdict"] == "NO_GO" and "K4" in d["critical"]


def test_p12_review_items_name_each_part_and_the_context(pack):
    cases, refs = pack
    bicycle = {"text": "bicycle handle", "source_quote": "3D-printed casing",
               "candidate_concept": "mechanical"}
    reply = _p12(bicycle)
    s12, scored = _p12_scores(pack, reply)
    replies = {c["case_id"]: _oracle(c, refs[c["case_id"]]) for c in cases}
    replies["P12"] = reply
    items = ev.review_items(scored, pack, replies)["k4_context"]
    assert [(i["item_id"], i["part"], i["context_terms"]) for i in items] == [
        ("P12-part-1", P12_PCB, ["handlebar", "bike"]),
        ("P12-part-2", bicycle, ["handlebar", "bike"])]
    base = ev.baseline()["integrated_recall"]
    for bad in ({"P12-part-9": ev.K6_CLEAR}, {"P12-part-2": "PASS"}, ["P12-part-2"]):
        record = _full(scored, refs)
        record["k4_context"] = bad
        with pytest.raises(ev.PackError):
            ev.decide(scored, refs, base, record)


def test_no_other_case_gets_a_context_review(pack):
    assert {k for x in _oracle_scores(pack) for k in x["context_review"]} == {
        "P12-part-1", "P12-part-2"}


def test_external_context_role_is_only_on_p12(pack):
    _cases, refs = pack
    roles = {(cid, f["term"]) for cid, r in refs.items() for f in r["forbidden_stated_parts"]
             if "role" in f}
    assert roles == {("P12", "handlebar"), ("P12", "bike")}
