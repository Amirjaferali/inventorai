"""G1-1/2 component-concept qualification — network-free preparation guards.

Every transport is a local fake. The replies built here are HANDCRAFTED from the
reference to exercise the validator, the review items and the decision rule; they are
not model results and say nothing about any model's competence.
"""
import copy
import io
import json
import socket
from pathlib import Path

import pytest

from scripts import g1_precreation_heldout_v2_preregistration as ho
from scripts import run_g1_precreation_campaign as c01
from scripts import run_g1_precreation_campaign_02 as c02
from scripts import run_g1_component_concept_eval as cc
from tests.test_g1_precreation_campaign import _Fake, _NotFake, _adapter, _body

ROOT = Path(__file__).resolve().parent.parent
REVISION = "0" * 40
INSTRUCTIONS_SHA256 = "e5047edb1815fd70c02889f589d80142fc509bb44d427957dbf1a7aa0c84de9a"
SCHEMA_SHA256 = "59c5c056838c76039b1a4a58b0c5ef79d1ce354d2bb4ec7967ea3047bd057a22"
PREREGISTRATION_SHA256 = "fa55b6f613788c60d3c72a17b1c02358f3d37db4063e434a32f90db1c0b331b4"


@pytest.fixture(autouse=True)
def _no_network(monkeypatch):
    def refuse(*a, **k):
        raise AssertionError("network attempted")
    monkeypatch.setattr(socket.socket, "connect", refuse)
    monkeypatch.setattr(socket, "create_connection", refuse)


@pytest.fixture(scope="module")
def pack():
    return cc.load_pack()


@pytest.fixture
def evidence(tmp_path, monkeypatch):
    d = tmp_path / "evidence"
    monkeypatch.setattr(cc, "EVIDENCE_DIR", str(d))
    monkeypatch.setattr(cc, "JOURNAL_PATH", str(d / "run_journal.jsonl"))
    monkeypatch.setattr(cc, "REPORT_PATH", str(d / "run_report.json"))
    monkeypatch.setattr(cc, "_evidence_in_history", lambda: False)
    return d


# ── handcrafted replies and assessments ─────────────────────────────────────
def _oracle(case, ref):
    """A reply that follows the reference: an exercise of the rules, not a model."""
    empty = {k: [] for k in cc.schema()["properties"] if k != "outcome"}
    g = ref["group"]
    if g == "NON_DEVICE":
        return dict(empty, outcome=cc.ABSTAIN, missing_information=["what is to be built"])
    if g == "AMBIGUOUS":
        return dict(empty, outcome=cc.RESPONDED,
                    clarification_questions=["What should it do for you?"],
                    missing_information=[u["meaning"] for u in ref["expected_unknowns"]][:6])
    fns = [{"id": "F%d" % (i + 1), "text": f["meaning"][:200], "origin": cc.AI_PROPOSED,
            "source_quote": "", "resolution": "UNRESOLVED" if f["may_be_unresolved"] else "PROPOSED"}
           for i, f in enumerate(ref["essential_functions"])]
    comps = [{"id": "C%d" % (i + 1), "type": "component type %d" % (i + 1), "serves": [f["id"]],
              "attribution": cc.AI_PROPOSED, "status": cc.UNVERIFIED} for i, f in enumerate(fns)]
    rels = [{"from": comps[i]["id"], "to": comps[i + 1]["id"], "kind": "SIGNAL"}
            for i in range(len(comps) - 1)]
    return dict(empty, outcome=cc.RESPONDED, functions=fns, component_types=comps,
                relationships=rels,
                alternatives=[{"for_function": "F1", "options": ["another approach"]}],
                missing_information=[u["meaning"][:200] for u in ref["expected_unknowns"]][:6])


def _scored(pack, replies=None):
    cases, refs = pack
    replies = replies or {}
    return [cc.score_case(replies.get(c["case_id"], _oracle(c, refs[c["case_id"]])), c,
                          refs[c["case_id"]]) for c in cases]


def _good_answer(kind):
    return {"K1": cc.CLEAR, "K2": cc.CLEAR, "K3": cc.CLEAR, "G1": "ADDRESSED", "G2": "COHERENT",
            "G3": "RECOGNIZED", "G4": "RELEVANT", "G5": "CLARIFIED"}[kind]


def _judged(scored, **override):
    out = {i: _good_answer(k) for s in scored for i, k in s["items"].items()}
    out.update(override)
    return out


def _record(scored, report_sha="r" * 64, **kw):
    base = {"evaluation_id": cc.EVALUATION_ID, "report_sha256": report_sha,
            "reviewer": {"name": "Reviewer Name", "kind": "HUMAN",
                         "languages": ["en", "ar-msa", "ar-gulf", "ar-egyptian"]},
            "attestation": cc.ATTESTATION, "attested_on": "2026-11-06",
            "judgments": _judged(scored)}
    base.update(kw)
    return base


def _varieties(pack):
    return [c["variety"] for c in pack[0]]


# ── 1. frozen identity, independence and balance ────────────────────────────
def test_instructions_schema_and_preregistration_are_pinned():
    assert cc._sha(cc.INSTRUCTIONS) == INSTRUCTIONS_SHA256
    assert cc._sha(cc.schema()) == SCHEMA_SHA256
    assert cc.preregistration_digest() == PREREGISTRATION_SHA256


def test_pack_is_pinned_balanced_and_contains_the_plant_case(pack):
    cases, refs = pack
    assert [c["case_id"] for c in cases] == list(cc.CASE_IDS)
    groups = [refs[c["case_id"]]["group"] for c in cases]
    assert {g: groups.count(g) for g in cc.GROUPS} == cc.GROUPS
    varieties = [c["variety"] for c in cases]
    assert {v: varieties.count(v) for v in cc.VARIETIES} == cc.VARIETIES
    plant = next(c for c in cases if c["idea_text"] == cc.PLANT_IDEA)
    assert refs[plant["case_id"]]["group"] == "POSITIVE" and plant["variety"] == "en"
    assert all(c["synthetic"] is True for c in cases)


def test_a_changed_byte_is_refused(monkeypatch):
    monkeypatch.setattr(cc, "REFERENCE_SHA256", "0" * 64)
    with pytest.raises(cc.PackError):
        cc.load_pack()
    monkeypatch.setattr(cc, "INPUT_SHA256", None)
    with pytest.raises(cc.PackError):
        cc.load_pack()


def test_heldout_authorship_and_adjudication_are_recorded():
    inputs = json.loads(Path(cc.INPUT_PATH).read_text(encoding="utf-8"))
    reference = json.loads(Path(cc.REFERENCE_PATH).read_text(encoding="utf-8"))
    assert inputs["authorship"]["role"] == "blind author"
    assert inputs["authorship"]["base_commit"] == "9ad18ef0b2e68301efb0fae912a7c1b790aa1823"
    adjudication = reference["adjudication"]
    assert adjudication["role"] == "prompt-blind adjudicator"
    assert adjudication["base_commit"] == cc.AUTHOR_COMMIT
    assert set(adjudication) >= {"role", "statement", "changes", "cases_reviewed"}
    assert set(adjudication["cases_reviewed"]) == set(cc.CASE_IDS)
    assert cc.FROZEN_BEFORE_PACK_COMMIT and cc.AUTHOR_COMMIT and cc.ADJUDICATION_COMMIT


def test_heldout_cases_are_new_against_every_earlier_pack_including_development(pack):
    sims = cc.similarity_to_earlier_packs(pack[0])
    assert max(sims.values()) < cc.MAX_SIMILARITY, sims
    # only the Owner-specified plant example is shared with the development pack
    dev_ideas = {c["idea_text"] for c in cc.load_pack(development=True)[0]}
    assert {c["idea_text"] for c in pack[0]} & dev_ideas == {cc.PLANT_IDEA}


def test_the_development_pack_is_evidence_only_with_both_adjudications_reconciled():
    cases, refs = cc.load_pack(development=True)
    assert [c["case_id"] for c in cases] == list(cc.DEV_CASE_IDS)
    reference = json.loads(Path(cc.DEV_REFERENCE_PATH).read_text(encoding="utf-8"))
    assert reference["adjudication"]["role"] == "prompt-blind adjudicator"
    assert reference["second_adjudication"]["commit"] == cc.DEV_COMMITS["adjudication_2"]
    assert set(reference["reconciliation"]["cases"]) == {"C05", "C10", "C15", "C16"}
    assert "never a held-out qualification" in reference["reconciliation"]["status"]
    assert "dry" not in refs["C05"]["essential_functions"][0]["meaning"].lower()
    assert [f["function_id"] for f in refs["C15"]["essential_functions"]] == [
        "C15-F1", "C15-F2", "C15-F3"]
    assert refs["C16"]["meaningful_choice"] == {"meaning": "Heating only versus heating plus cooling"}
    assert [u["unknown_id"] for u in refs["C10"]["expected_unknowns"]] == ["C10-U1", "C10-U2"]
    assert cc.preregistration()["development_pack"]["status"].startswith("development evidence")
    assert cc.PACK_ID != cc.DEV_PACK_ID and set(cc.CASE_IDS).isdisjoint(cc.DEV_CASE_IDS)


def test_m1_every_enforced_format_rule_is_stated_in_the_instructions():
    text = cc.INSTRUCTIONS
    for key, cap in cc.LIMITS.items():
        assert str(cap) in text, key
    assert "S1, S2" in text and "F1, F2" in text and "C1, C2" in text and "1 to 99" in text
    assert "at least two words" in text and "character for" in text
    assert "never RESPONDED with empty lists" in text


def test_the_priming_example_is_gone_and_no_reference_answer_is_in_the_instructions(pack):
    assert "moisture" not in cc.INSTRUCTIONS.lower() and "for example" not in cc.INSTRUCTIONS.lower()
    for ref in pack[1].values():
        for f in ref["essential_functions"]:
            assert f["meaning"].lower() not in cc.INSTRUCTIONS.lower()


def test_campaign_01_and_02_are_untouched():
    assert c02.MAX_OUTPUT_TOKENS == 1200 and c02.MAX_PROVIDER_REQUESTS == 24
    assert ho.preregistration_digest() == (
        "b1a7c2c35f38f074c3343b97fd4be9f0d2dd5d98c741de86d27e02e3309e06d1")
    report = ROOT / "docs/benchmarks/evidence/g1_precreation_semantic_heldout_v2/campaign_02_report.json"
    assert c02._sha(json.loads(report.read_text(encoding="utf-8"))) == (
        "bbf60d01604d9521dfde21e09cf7bd04ecd881e15ab096890a6790cb61fa104d")
    assert cc.EVIDENCE_DIR not in (c01.EVIDENCE_DIR, c02.EVIDENCE_DIR)


# ── 2. deterministic structural and grounding checks ────────────────────────
IDEA = "A 12 V garden pump timer that waters my plants every morning, without any app."


def _reply(**kw):
    r = {"outcome": cc.RESPONDED,
         "stated": [{"id": "S1", "kind": "VALUE", "text": "12 V", "source_quote": "A 12 V garden pump"}],
         "functions": [{"id": "F1", "text": "water the plants", "origin": cc.STATED,
                        "source_quote": "waters my plants every morning", "resolution": "PROPOSED"},
                       {"id": "F2", "text": "keep time", "origin": cc.AI_PROPOSED,
                        "source_quote": "", "resolution": "PROPOSED"}],
         "component_types": [{"id": "C1", "type": "timer", "serves": ["F2"],
                              "attribution": cc.AI_PROPOSED, "status": cc.UNVERIFIED},
                             {"id": "C2", "type": "12 V water pump", "serves": ["F1"],
                              "attribution": cc.AI_PROPOSED, "status": cc.UNVERIFIED}],
         "relationships": [{"from": "C1", "to": "C2", "kind": "SIGNAL"}],
         "alternatives": [{"for_function": "F1", "options": ["gravity-fed valve"]}],
         "missing_information": ["where the water comes from"],
         "clarification_questions": ["Is there a tap nearby?"],
         "excluded_by_inventor": [{"text": "no app", "source_quote": "without any app"}]}
    r.update(kw)
    return r


def test_a_well_formed_grounded_reply_is_valid_and_keeps_an_inventor_value():
    assert cc.validate(_reply(), IDEA) == {"status": cc.V_VALID, "critical": []}


@pytest.mark.parametrize("mutate", [
    lambda r: r.pop("alternatives"),
    lambda r: r.update(outcome="MAYBE"),
    lambda r: r["relationships"].append({"from": "C1", "to": "C9", "kind": "SIGNAL"}),
    lambda r: r["relationships"].append({"from": "C1", "to": "C1", "kind": "POWER"}),
    lambda r: r["relationships"].append({"from": "C1", "to": "C2", "kind": "COMPATIBLE"}),
    lambda r: r["component_types"].append(dict(r["component_types"][0])),          # duplicate id
    lambda r: r["component_types"][0].update(serves=[]),
    lambda r: r["component_types"][0].update(serves=["F7"]),
    lambda r: r["component_types"][0].update(status="VERIFIED"),
    lambda r: r["alternatives"][0].update(for_function="F9"),
    lambda r: r["alternatives"][0].update(options=[]),
    lambda r: r.update(clarification_questions=["a?", "b?", "c?"]),
    lambda r: r["functions"][0].update(text="x" * 241),
    lambda r: r.update(outcome=cc.ABSTAIN),                                         # abstain with a concept
])
def test_structure_violations_are_k5(mutate):
    r = _reply()
    mutate(r)
    assert cc.validate(r, IDEA) == {"status": cc.V_STRUCTURE, "critical": ["K5"]}


@pytest.mark.parametrize("mutate,critical", [
    (lambda r: r["stated"][0].update(source_quote="a solar panel"), ["K1"]),
    (lambda r: r["functions"][1].update(source_quote="keeps time"), ["K1"]),
    (lambda r: r["excluded_by_inventor"][0].update(source_quote="no wires"), ["K1"]),
    (lambda r: r["component_types"][1].update(type="24 V water pump"), ["K3"]),
    (lambda r: r["alternatives"][0].update(options=["a 2 L reservoir"]), ["K3"]),
])
def test_grounding_and_invented_specifications_are_automatic_failures(mutate, critical):
    r = _reply()
    mutate(r)
    assert cc.validate(r, IDEA) == {"status": cc.V_REJECTED, "critical": critical}


def test_an_abstention_with_only_questions_is_valid_and_a_missing_reply_is_an_error():
    empty = {k: [] for k in cc.schema()["properties"] if k != "outcome"}
    ab = dict(empty, outcome=cc.ABSTAIN, clarification_questions=["What would you build?"])
    assert cc.validate(ab, IDEA)["status"] == cc.V_ABSTAIN
    assert cc.validate(None, IDEA)["status"] == cc.V_ERROR


def test_the_request_carries_only_instructions_schema_and_idea(pack):
    body = cc.payload(pack[0][0])
    assert set(body) == {"model", "instructions", "input", "store", "max_output_tokens", "text"}
    assert body["input"] == pack[0][0]["idea_text"] and body["store"] is False
    raw = json.dumps(body, ensure_ascii=False)
    for ref in pack[1].values():
        for f in ref["essential_functions"]:
            assert f["meaning"] not in raw                       # no reference label leaks


# ── 3. decision rule ────────────────────────────────────────────────────────
def test_reference_following_replies_need_every_human_review(pack):
    _cases, refs = pack
    scored = _scored(pack)
    assert all(not s["critical"] for s in scored)
    assert cc.decide(scored, refs, {})["verdict"] == "INCOMPLETE_REVIEW"
    d = cc.decide(scored, refs, _judged(scored))
    assert d["verdict"] == "PRELIMINARY_GO" and all(d["graded"].values())


def test_one_unassessed_item_keeps_the_review_incomplete(pack):
    _cases, refs = pack
    scored = _scored(pack)
    judged = _judged(scored)
    judged.pop(next(iter(judged)))
    assert cc.decide(scored, refs, judged)["verdict"] == "INCOMPLETE_REVIEW"


@pytest.mark.parametrize("kind", ["K1", "K2", "K3"])
def test_one_human_critical_failure_is_no_go(pack, kind):
    _cases, refs = pack
    scored = _scored(pack)
    item = next(i for s in scored for i, k in s["items"].items() if k == kind)
    d = cc.decide(scored, refs, _judged(scored, **{item: cc.FAILURE}))
    assert d["verdict"] == "NO_GO" and kind in d["critical"]


def test_a_graded_threshold_that_can_no_longer_pass_is_no_go_before_review_ends(pack):
    _cases, refs = pack
    scored = _scored(pack)
    g2 = [i for s in scored for i, k in s["items"].items() if k == "G2"][:2]
    d = cc.decide(scored, refs, {i: "NOT_COHERENT" for i in g2})       # rest unassessed
    assert d["verdict"] == "NO_GO" and d["graded_reachable"]["G2"] is False


def test_invented_detail_and_committed_designs_earn_nothing(pack):
    _cases, refs = pack
    scored = _scored(pack)
    amb = [i for s in scored for i, k in s["items"].items() if k == "G5"]
    d = cc.decide(scored, refs, _judged(scored, **{amb[0]: "COMMITTED_DESIGN"}))
    assert d["verdict"] == "NO_GO" and d["graded"]["G5"] is False
    fns = [i for s in scored for i, k in s["items"].items() if k == "G1"]
    d = cc.decide(scored, refs, _judged(scored, **{i: "INVENTED_DETAIL" for i in fns[:5]}))
    assert d["verdict"] == "NO_GO" and d["graded"]["G1"] is False


def test_a_non_device_case_given_a_concept_is_k4(pack):
    cases, refs = pack
    nd = next(c for c in cases if refs[c["case_id"]]["group"] == "NON_DEVICE")
    pos = next(c for c in cases if refs[c["case_id"]]["group"] == "POSITIVE")
    forged = _oracle(pos, refs[pos["case_id"]])
    scored = _scored(pack, {nd["case_id"]: forged})
    d = cc.decide(scored, refs, _judged(scored))
    assert d["verdict"] == "NO_GO" and "K4" in d["critical"]


def test_a_provider_error_is_incomplete_and_a_malformed_reply_is_no_go(pack):
    _cases, refs = pack
    scored = _scored(pack, {"C03": None})
    assert cc.decide(scored, refs, _judged(scored))["verdict"] == "INCOMPLETE"
    scored = _scored(pack, {"C03": {"outcome": "RESPONDED"}})
    d = cc.decide(scored, refs, _judged(scored))
    assert d["verdict"] == "NO_GO" and "K5" in d["critical"]


def test_review_items_give_each_judgment_its_question_and_evidence(pack):
    scored = _scored(pack)
    out = cc.review_items(scored, pack, {})
    kinds = {i["criterion"] for i in out["items"]}
    assert kinds == {"K1", "K2", "K3", "G1", "G2", "G3", "G4", "G5"}
    for item in out["items"]:
        assert item["question"] == cc.REVIEW_QUESTIONS[item["criterion"]][0]
        assert item["idea_text"] and item["language"] in ("en", "ar-msa", "ar-gulf", "ar-egyptian")
    assert out["attestation_required"] == cc.ATTESTATION


# ── 4. reviewer-record safeguards ───────────────────────────────────────────
def test_a_valid_human_record_is_accepted_and_not_assessed_stays_open(pack):
    scored = _scored(pack)
    rec = _record(scored)
    assert cc.check_assessment(rec, scored, "r" * 64, _varieties(pack)) == rec["judgments"]
    first = next(iter(rec["judgments"]))
    rec["judgments"][first] = cc.NOT_ASSESSED
    assert first not in cc.check_assessment(rec, scored, "r" * 64, _varieties(pack))


@pytest.mark.parametrize("mutate", [
    lambda r: r["reviewer"].update(kind="AI"),
    lambda r: r["reviewer"].update(name="  "),
    lambda r: r["reviewer"].update(languages=["en"]),                      # no Arabic competence
    lambda r: r["reviewer"].update(languages=["en", "ar-msa", "ar-gulf", "ar-egyptian", "fr"]),
    lambda r: r.update(attestation=cc.ATTESTATION.replace("myself", "with help")),
    lambda r: r.update(attested_on="yesterday"),
    lambda r: r.update(report_sha256="x" * 64),
    lambda r: r.update(evaluation_id="g1-precreation-campaign-02"),
    lambda r: r["judgments"].update({"C99-F1": "ADDRESSED"}),
    lambda r: r["judgments"].update({next(iter(r["judgments"])): "MAYBE"}),
    lambda r: r.update(ai_generated=False),
    lambda r: r.pop("attestation"),
])
def test_records_that_are_not_attested_human_reviews_are_refused(pack, mutate):
    scored = _scored(pack)
    rec = _record(scored)
    mutate(rec)
    with pytest.raises(cc.PackError):
        cc.check_assessment(rec, scored, "r" * 64, _varieties(pack))


def test_the_verdict_always_discloses_the_human_review_basis(pack):
    _cases, refs = pack
    scored = _scored(pack)
    assert "does not by itself authenticate" in cc.decide(scored, refs, _judged(scored))[
        "human_review_basis"]


# ── 5. provider boundary, budget and one run ────────────────────────────────
def test_limits_and_distinct_identity():
    assert (cc.MAX_PROVIDER_REQUESTS, cc.RETRIES, cc.MAX_OUTPUT_TOKENS, cc.CEILING_USD) == (
        16, 0, 2000, 5.0)
    assert cc.AUTHORIZED_RUN_MANIFEST_SHA256 is None
    assert cc.RESERVATION["max_output_tokens"] == 2000 and cc.RESERVATION["multiplier"] == 6


def test_the_conservative_budget_fits_the_ceiling(pack):
    plan = cc.budget_plan(pack[0])
    assert plan["requests"] == 16 and plan["within_ceiling"] and plan["price_verified"]
    expected = sum(cc._pf_usd(len(cc._body(c, cc.MODEL)) + 1000, 2000, 12.0, 60.0) for c in pack[0])
    assert plan["all_reservations_usd"] == round(expected, 6) <= cc.CEILING_USD


@pytest.mark.parametrize("authorized", [None, "", "0" * 64, "not-a-digest"])
def test_no_request_without_the_owner_named_manifest(pack, evidence, authorized):
    manifest = cc.run_manifest(REVISION, cc.MODEL)
    fake = _NotFake([])
    with pytest.raises(cc.PackError):
        cc.run(_adapter(fake), pack[0], manifest, None, authorized)
    assert fake.calls == [] and not evidence.exists()


def test_the_cli_plan_sends_nothing(capsys):
    assert cc.main([]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["provider_path"].startswith("closed") and out["budget"]["within_ceiling"]
    assert cc.main(["--provider", "openai"]) == 2                     # no network flags


def test_an_offline_fake_run_binds_report_journal_review_and_verdict(pack, evidence):
    cases, refs = pack
    fake, journal = _Fake([_body(_oracle(c, refs[c["case_id"]])) for c in cases]), io.StringIO()
    adapter = _adapter(fake)
    manifest = cc.run_manifest(REVISION, adapter._model)
    report = cc.run(adapter, cases, manifest, journal)
    assert len(fake.calls) == 16 and report["requests"] == 16 and report["stopped_on"] is None
    assert all(call["max_output_tokens"] == 2000 and call["store"] is False for call in fake.calls)
    lines = journal.getvalue().splitlines()
    sha = cc._digest(manifest)
    items = cc.report_review_items(report, sha, lines)
    assert items["report_sha256"] == cc._digest(report)
    scored, _r = cc.score_report(report)
    assert cc.aggregate(report, None, sha, lines)["verdict"] == "INCOMPLETE_REVIEW"
    rec = _record(scored, report_sha=cc._digest(report))
    assert cc.aggregate(report, rec, sha, lines)["verdict"] == "PRELIMINARY_GO"
    tampered = copy.deepcopy(report)
    tampered["rows"][0]["reply"]["outcome"] = cc.ABSTAIN
    with pytest.raises(cc.PackError):
        cc.aggregate(tampered, rec, sha, lines)


def test_nothing_in_the_product_imports_this_evaluation():
    for folder in ("engine", "web"):
        for path in (ROOT / folder).rglob("*.py"):
            assert "run_g1_component_concept_eval" not in path.read_text(encoding="utf-8")


# ── 6. independent-review corrections (pack-neutral; frozen texts unchanged) ─
def test_an_ambiguous_abstention_that_asks_first_is_judged_by_a_human(pack):
    """G5 counts "requests clarification first": an ABSTAIN with questions is a human item."""
    cases, refs = pack
    empty = {k: [] for k in cc.schema()["properties"] if k != "outcome"}
    amb = [c for c in cases if refs[c["case_id"]]["group"] == "AMBIGUOUS"]
    asks = dict(empty, outcome=cc.ABSTAIN, clarification_questions=["What should it do?"],
                missing_information=["what the thing is"])
    scored = _scored(pack, {c["case_id"]: asks for c in amb})
    for s in scored:
        if s["group"] == "AMBIGUOUS":
            assert s["items"]["%s:G5" % s["case_id"]] == "G5"
            assert "%s:K3" % s["case_id"] in s["items"]
    assert cc.decide(scored, refs, _judged(scored))["verdict"] == "PRELIMINARY_GO"
    silent = dict(empty, outcome=cc.ABSTAIN)
    scored = _scored(pack, {c["case_id"]: silent for c in amb})
    s = next(s for s in scored if s["group"] == "AMBIGUOUS")
    assert s["auto"]["%s:G5" % s["case_id"]] == "SAFE_ABSTAIN" and not s["items"]
    assert cc.decide(scored, refs, _judged(scored))["verdict"] == "NO_GO"   # none CLARIFIED


@pytest.mark.parametrize("idea,proposed,critical", [
    ("A feeder for my cat.", "dispense food 3 a day", []),                 # an article, not amperes
    ("A feeder for my cat.", "a 2 A charger", ["K3"]),                     # amperes
    ("مضخة ١٢ V لري النباتات في حديقتي", "12 V pump", []),                 # Arabic-Indic digits
    ("A 1,5 L water tank on a stand.", "1.5 L tank", []),                  # decimal comma
    ("A 1,5 L water tank on a stand.", "2,5 L tank", ["K3"]),
])
def test_number_matching_is_whole_number_and_digit_system_neutral(idea, proposed, critical):
    r = {"outcome": cc.RESPONDED, "stated": [],
         "functions": [{"id": "F1", "text": "do the job", "origin": cc.AI_PROPOSED,
                        "source_quote": "", "resolution": "PROPOSED"}],
         "component_types": [{"id": "C1", "type": proposed, "serves": ["F1"],
                              "attribution": cc.AI_PROPOSED, "status": cc.UNVERIFIED}],
         "relationships": [], "alternatives": [], "missing_information": [],
         "clarification_questions": [], "excluded_by_inventor": []}
    assert cc.validate(r, idea)["critical"] == critical


@pytest.mark.parametrize("mutate", [
    lambda r: r["component_types"][0].update(serves=[["F2"]]),
    lambda r: r["relationships"][0].update({"from": ["C1"]}),
    lambda r: r["alternatives"][0].update(for_function={"F1": 1}),
])
def test_unhashable_values_are_refused_not_crashed(mutate):
    r = _reply()
    mutate(r)
    assert cc.validate(r, IDEA) == {"status": cc.V_STRUCTURE, "critical": ["K5"]}


# ── 7. M3: the expected outcome is enforced ─────────────────────────────────
def _empty(outcome):
    return dict({k: [] for k in cc.schema()["properties"] if k != "outcome"}, outcome=outcome)


def test_a_non_device_case_must_actually_abstain(pack):
    cases, refs = pack
    nd = [c["case_id"] for c in cases if refs[c["case_id"]]["group"] == "NON_DEVICE"]
    scored = _scored(pack, {nd[0]: _empty(cc.RESPONDED)})               # empty RESPONDED
    d = cc.decide(scored, refs, _judged(scored))
    assert d["verdict"] == "NO_GO" and "K4" in d["critical"]
    scored = _scored(pack, {i: _empty(cc.ABSTAIN) for i in nd})
    assert cc.decide(scored, refs, _judged(scored))["verdict"] == "PRELIMINARY_GO"


@pytest.mark.parametrize("group", ["POSITIVE", "EXCLUSION", "UNSUPPORTED"])
def test_abstaining_where_a_concept_is_required_never_qualifies(pack, group):
    cases, refs = pack
    target = next(c["case_id"] for c in cases if refs[c["case_id"]]["group"] == group)
    scored = _scored(pack, {target: _empty(cc.ABSTAIN)})
    d = cc.decide(scored, refs, _judged(scored))
    assert d["verdict"] == "NO_GO" and d["graded"]["G6"] is False


def test_a_concept_without_component_types_is_not_delivered(pack):
    cases, refs = pack
    case = next(c for c in cases if refs[c["case_id"]]["group"] == "EXCLUSION")
    reply = _oracle(case, refs[case["case_id"]])
    reply = dict(reply, component_types=[], relationships=[])
    scored = _scored(pack, {case["case_id"]: reply})
    d = cc.decide(scored, refs, _judged(scored))
    assert d["verdict"] == "NO_GO" and d["graded"]["G6"] is False


def test_an_ambiguous_case_may_still_safely_abstain_or_ask(pack):
    cases, refs = pack
    amb = [c["case_id"] for c in cases if refs[c["case_id"]]["group"] == "AMBIGUOUS"]
    asks = dict(_empty(cc.ABSTAIN), clarification_questions=["What should it do?"])
    scored = _scored(pack, {amb[0]: _empty(cc.ABSTAIN), amb[1]: asks})
    d = cc.decide(scored, refs, _judged(scored))
    assert d["verdict"] == "PRELIMINARY_GO" and d["graded"]["G6"] is True
