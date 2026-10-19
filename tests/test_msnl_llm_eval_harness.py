"""MSNL synthetic LLM feasibility harness — network-free contract tests.

Covers `scripts/run_msnl_eval.py` and the synthetic explicit-unknown probe
`tests/fixtures/msnl_unknown_probe_v1.json`. Every provider path here uses an
injected fake transport: hosted CI never reaches the network. Scores are
evidence, never CI thresholds; these tests pin only the harness mechanics,
the payload boundary and the probe's schema.
"""
import importlib.util
import json
import pathlib

import pytest

from engine import msnl_shadow as ms
from engine import technical_orchestration_openai as toa

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "run_msnl_eval.py"
PROBE = ROOT / "tests" / "fixtures" / "msnl_unknown_probe_v1.json"


def _load_script():
    spec = importlib.util.spec_from_file_location("run_msnl_eval", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


h = _load_script()


def _request(text="The drum rotates whenever the handle is turned.",
             gap="MECHANISM_COMPLETENESS"):
    return ms.ShadowRequest(text, gap, None, "mechanical", ms.candidate_concepts(gap))


def _reply(obj, status=200, refusal=False):
    content = ([{"type": "refusal", "refusal": "no"}] if refusal
               else [{"type": "output_text", "text": json.dumps(obj)}])
    body = {"status": "completed",
            "output": [{"type": "message", "content": content}]}
    return status, json.dumps(body).encode("utf-8")


class FakeTransport:
    def __init__(self, *replies):
        self.replies = list(replies)
        self.calls = []

    def __call__(self, url, headers, body, timeout):
        self.calls.append((url, headers, json.loads(body.decode("utf-8"))))
        return self.replies.pop(0)


# ─── pinned synthetic packs ─────────────────────────────────────────────────

def test_both_packs_are_pinned_and_load():
    assert h._load(h.CONCEPT_PACK_PATH, h.CONCEPT_PACK_SHA256)["pack_id"] == \
        "msnl-evaluation-pack-v1"
    assert h._load(h.UNKNOWN_PACK_PATH, h.UNKNOWN_PACK_SHA256)["pack_id"] == \
        "msnl-unknown-probe-v1"
    with pytest.raises(h.PackError):
        h._load(h.UNKNOWN_PACK_PATH, "0" * 64)


def test_unknown_probe_is_synthetic_balanced_and_long_enough():
    pack = json.loads(PROBE.read_text(encoding="utf-8"))
    assert pack["status"] == "SYNTHETIC"
    for phrase in ("SYNTHETIC", "NOT real-user evidence", "no universal Arabic-dialect",
                   "never change to fit an adapter", "registry expansion"):
        assert phrase in pack["notice"], phrase
    assert tuple(pack["varieties"]) == h.VARIETIES
    ids = [c["case_id"] for c in pack["cases"]]
    assert len(ids) == len(set(ids)) == 20
    for variety in h.VARIETIES:
        rows = [c for c in pack["cases"] if c["variety"] == variety]
        assert sorted(c["expectation"] for c in rows) == \
            [h.EXPLICIT_UNKNOWN] * 2 + [h.NOT_UNKNOWN] * 3
    for case in pack["cases"]:
        assert set(case) == {"case_id", "variety", "expectation", "text"}
        # above the existing detector's minimum length, so a miss is about wording
        assert len(case["text"]) >= 40, case["case_id"]


# ─── the payload boundary ───────────────────────────────────────────────────

def test_concept_payload_sends_only_the_answer_gap_and_registry_candidates():
    req = _request()
    payload = h.concept_payload(req)
    assert set(payload) == {"model", "instructions", "input", "store",
                            "max_output_tokens", "text"}
    assert payload["store"] is False and payload["model"] == toa.MODEL
    body = json.loads(payload["input"])
    assert set(body) == {"answer", "question_area", "candidates"}
    assert body["answer"] == req.accepted_text
    ids = [c["concept_id"] for c in body["candidates"]]
    assert ids == [c.concept_id for c in ms.candidate_concepts(req.gap_type)]
    schema = payload["text"]["format"]["schema"]
    assert schema["properties"]["concept_ids"]["items"]["enum"] == ids
    assert payload["text"]["format"]["strict"] is True
    for forbidden in ("project", "record", "session", "account", "domain"):
        assert forbidden not in body


def test_unknown_payload_sends_only_the_statement():
    payload = h.unknown_payload("I don't know how it works yet, honestly.")
    assert json.loads(payload["input"]) == {"statement": "I don't know how it works yet, honestly."}
    assert payload["store"] is False


# ─── adapter behaviour (fake transport only) ────────────────────────────────

def test_adapter_is_off_without_network_permission():
    transport = FakeTransport()
    adapter = h.OpenAIMsnlAdapter(transport=transport)
    assert adapter.propose(_request()).outcome == ms.ERROR
    assert adapter.classify_unknown("I don't know how it works yet, honestly.") == ms.ERROR
    assert transport.calls == []
    assert adapter.errors == {toa.ERR_NETWORK_NOT_ALLOWED: 2}


def test_adapter_sends_no_credential_and_posts_only_to_the_approved_endpoint():
    transport = FakeTransport(_reply({"outcome": "PROPOSED", "concept_ids": ["MC-ROTATE"]}))
    h.OpenAIMsnlAdapter(allow_network=True, transport=transport).propose(_request())
    url, headers, _body = transport.calls[0]
    assert url == toa.ENDPOINT
    assert headers == {"Content-Type": "application/json"}


def test_adapter_maps_outcomes_through_the_unchanged_local_policy():
    def event(text="The drum rotates whenever the handle is turned."):
        return ms.AcceptedEvent(ref=ms.LocalRef("t", "c"), accepted_text=text,
                                gap_type="MECHANISM_COMPLETENESS", question_target=None,
                                domain="mechanical", kind=ms.EVENT_ANSWERED)
    cases = [
        (_reply({"outcome": "PROPOSED", "concept_ids": ["MC-ROTATE"]}),
         ms.DISPOSITION_PROPOSAL, ("MC-ROTATE",)),
        (_reply({"outcome": "ABSTAIN", "concept_ids": []}), ms.DISPOSITION_ABSTAINED, ()),
        (_reply({"outcome": "NO_MAPPING", "concept_ids": []}), ms.DISPOSITION_NO_MAPPING, ()),
        (_reply({"outcome": "PROPOSED", "concept_ids": ["PF-ENERGY"]}),
         ms.DISPOSITION_DISCARDED_UNSUPPORTED, ()),       # outside the served gap
        (_reply({}, refusal=True), ms.DISPOSITION_ABSTAINED, ()),
        ((401, b""), ms.DISPOSITION_ADAPTER_ERROR, ()),
        ((200, b"not json"), ms.DISPOSITION_ADAPTER_ERROR, ()),
        (_reply({"outcome": "PROPOSED"}), ms.DISPOSITION_ADAPTER_ERROR, ()),
    ]
    for reply, disposition, ids in cases:
        adapter = h.OpenAIMsnlAdapter(allow_network=True, transport=FakeTransport(reply))
        result = ms.evaluate(event(), adapter)
        assert (result.disposition, tuple(result.concept_ids)) == (disposition, ids), reply


def test_unknown_classification_mapping():
    for obj, expected in (({"outcome": "EXPLICIT_UNKNOWN"}, h.EXPLICIT_UNKNOWN),
                          ({"outcome": "NOT_UNKNOWN"}, h.NOT_UNKNOWN),
                          ({"outcome": "ABSTAIN"}, ms.ABSTAIN),
                          ({"outcome": "MAYBE"}, ms.ERROR)):
        adapter = h.OpenAIMsnlAdapter(allow_network=True, transport=FakeTransport(_reply(obj)))
        assert adapter.classify_unknown("I don't know how it works yet, honestly.") == expected
    adapter = h.OpenAIMsnlAdapter(allow_network=True, transport=FakeTransport((401, b"")))
    assert adapter.classify_unknown("I don't know how it works yet, honestly.") == ms.ERROR
    assert adapter.errors == {toa.ERR_HTTP_STATUS: 1}


# ─── harness mechanics ──────────────────────────────────────────────────────

def test_lexical_run_reports_both_packs_without_network(capsys):
    assert h.main([]) == 0
    out = json.loads(capsys.readouterr().out)
    assert set(out["concepts"]) == {"lexical-baseline-uncalibrated"}
    assert set(out["unknowns"]) == {"existing-acknowledged-unknown-detector"}
    for variety in h.VARIETIES:
        assert variety in out["concepts"]["lexical-baseline-uncalibrated"]
        assert variety in out["unknowns"]["existing-acknowledged-unknown-detector"]["by_variety"]
    assert "llm_error_kinds" not in out


@pytest.mark.parametrize("argv", [["--provider", "openai"],
                                  ["--provider", "openai", "--allow-network"],
                                  ["--provider", "openai", "--managed-credential"]])
def test_openai_is_refused_without_both_permissions(argv, capsys):
    assert h.main(argv) == 2
    assert "refused" in json.loads(capsys.readouterr().out)


def test_errors_are_reported_as_errors_never_as_safe_results():
    class Failing(h.OpenAIMsnlAdapter):
        def __init__(self):
            super().__init__(allow_network=True, transport=lambda *a: (401, b""))
    pack = h._load(h.UNKNOWN_PACK_PATH, h.UNKNOWN_PACK_SHA256)
    rep = h.unknown_report(Failing(), pack)
    assert rep["overall"]["errors"] == 20 and rep["overall"]["correct"] == 0


# ─── isolation ──────────────────────────────────────────────────────────────

def test_no_product_module_reaches_the_harness():
    for folder in ("engine", "web", "api"):
        for path in (ROOT / folder).glob("*.py") if (ROOT / folder).is_dir() else ():
            assert "run_msnl_eval" not in path.read_text(encoding="utf-8"), path
    import ast
    tree = ast.parse(SCRIPT.read_text(encoding="utf-8"))
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)
            imported.update(node.module + "." + a.name for a in node.names)
    for forbidden in ("web", "web.app", "engine.record_store", "engine.ai_advisor",
                      "sqlite3", "logging", "requests", "openai"):
        assert forbidden not in imported, forbidden
    assert "OPENAI_API_KEY" not in SCRIPT.read_text(encoding="utf-8")


# ─── MSNL-EVAL-02: three grains, nothing hidden ─────────────────────────────

def _row(expected, predicted, disposition=ms.DISPOSITION_PROPOSAL, variety="en"):
    return {"variety": variety, "expected": list(expected), "predicted": list(predicted),
            "disposition": disposition}


def _overall(rows, grain):
    return h.grain_report(rows)[grain]["overall"]


def test_sibling_extra_is_false_at_concept_grain_and_counted_beneath_coarser_ones():
    rows = [_row(["MC-DETECT"], ["MC-COMPONENT", "MC-DETECT"])]   # both MC/Q2
    concept = _overall(rows, "concept")
    assert (concept["false_attributions"], concept["hits"], concept["exact"]) == (1, 1, 0)
    for grain in ("governed_question", "gap"):
        out = _overall(rows, grain)
        assert (out["false_attributions"], out["concept_errors_beneath"], out["exact"]) == \
            (0, 1, 1), grain


def test_cross_question_extra_stays_false_at_the_governed_question_grain():
    rows = [_row(["MC-OPEN"], ["MC-HOW-IT-WORKS", "MC-OPEN"])]    # Q2 + Q1
    assert _overall(rows, "governed_question")["false_attributions"] == 1
    gap = _overall(rows, "gap")
    assert (gap["false_attributions"], gap["concept_errors_beneath"]) == (0, 1)


def test_a_proposal_on_a_safe_case_is_false_at_every_grain():
    rows = [_row([], ["MC-COMPONENT"])]
    for grain in h.GRAINS:
        out = _overall(rows, grain)
        assert (out["false_attributions"], out["match_cases"]) == (1, 0), grain


def test_errors_abstentions_and_no_mapping_stay_separate():
    rows = [_row(["MC-DETECT"], [], ms.DISPOSITION_ADAPTER_ERROR),
            _row(["MC-DETECT"], [], ms.DISPOSITION_ABSTAINED),
            _row([], [], ms.DISPOSITION_NO_MAPPING),
            _row([], [], ms.DISPOSITION_DISCARDED_UNSUPPORTED)]
    for grain in h.GRAINS:
        out = _overall(rows, grain)
        assert (out["errors"], out["abstained"], out["no_mapping"],
                out["discarded_unsupported"], out["hits"], out["false_attributions"]) == \
            (1, 1, 1, 1, 0, 0), grain


def test_grains_are_reported_per_variety_and_disclaim_relevance():
    rows = [_row(["PF-BATTERY"], ["PF-BATTERY"], variety=v) for v in h.VARIETIES]
    rep = h.grain_report(rows)
    assert set(rep) == {"measures", *h.GRAINS}
    for phrase in ("AFFIRMED", "no grain here measures gap relevance",
                   "engine.gap_relevance.addresses_gap", "concept_errors_beneath"):
        assert phrase in rep["measures"], phrase
    for grain in h.GRAINS:
        assert set(rep[grain]) == {"overall", *h.VARIETIES}
        assert all(rep[grain][v]["hits"] == 1 for v in h.VARIETIES)


def test_unregistered_concept_ids_are_refused():
    with pytest.raises(h.PackError):
        h.grain_report([_row([], ["NOT-A-CONCEPT"])])


def test_concept_grain_reproduces_the_existing_pack_scorer():
    from tests.test_msnl_evaluation_pack import aggregate, run_pack
    pack = h._load(h.CONCEPT_PACK_PATH, h.CONCEPT_PACK_SHA256)
    results = run_pack(ms.LexicalBaselineAdapter(), pack)
    base = aggregate(results)
    concept = h.grain_report([
        {"variety": r.variety, "expected": sorted(r.expected),
         "predicted": sorted(r.predicted), "disposition": r.disposition}
        for r in results])["concept"]["overall"]
    assert concept["false_attributions"] == base["false_attributions"]
    assert concept["exact"] == round(base["exact_agreement"] * base["cases"])


# ─── MSNL-EVAL-02: offline re-scoring of a saved report ─────────────────────

def _saved_lexical_report(capsys, tmp_path):
    assert h.main(["--show-cases"]) == 0
    out = json.loads(capsys.readouterr().out)
    path = tmp_path / "saved.json"
    path.write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    return out, path


def test_rescore_reproduces_the_live_grains_without_any_network(capsys, tmp_path, monkeypatch):
    live, path = _saved_lexical_report(capsys, tmp_path)

    def no_network(*_a, **_k):
        raise AssertionError("re-scoring must never reach the network")
    monkeypatch.setattr(toa, "_urllib_transport", no_network)
    assert h.main(["--rescore", str(path)]) == 0
    rescored = json.loads(capsys.readouterr().out)
    name = "lexical-baseline-uncalibrated"
    assert rescored["concepts"][name]["grains"] == live["concepts"][name]["grains"]
    assert len(rescored["rescored_sha256"]) == 64


def test_rescore_refuses_a_tampered_label_a_missing_case_or_no_cases(capsys, tmp_path):
    live, path = _saved_lexical_report(capsys, tmp_path)
    name = "lexical-baseline-uncalibrated"
    def relabel(o):
        case = o["concepts"][name]["cases"][0]
        case["expected"] = sorted(set(case["expected"]) ^ {"BA-SCOPE"})
    for mutate in (relabel,
                   lambda o: o["concepts"][name]["cases"].pop(),
                   lambda o: o["concepts"][name].pop("cases"),
                   lambda o: o.update(concept_pack="other-pack")):
        broken = json.loads(json.dumps(live))
        mutate(broken)
        path.write_text(json.dumps(broken), encoding="utf-8")
        assert h.main(["--rescore", str(path)]) == 2
        assert "refused" in json.loads(capsys.readouterr().out)


@pytest.mark.parametrize("extra", [["--provider", "openai"], ["--allow-network"],
                                   ["--managed-credential"]])
def test_rescore_takes_no_provider_or_network_option(extra, capsys, tmp_path):
    _live, path = _saved_lexical_report(capsys, tmp_path)
    assert h.main(["--rescore", str(path), *extra]) == 2
    assert "refused" in json.loads(capsys.readouterr().out)


# ─── MSNL-EVAL-03: grounded stated-only arm, breaker, held-out criteria ─────

def _grounded(*items, outcome="PROPOSED"):
    return _reply({"outcome": outcome, "proposals": [
        {"concept_id": c, "quote": q, "basis": b} for c, q, b in items]})


def test_grounded_payload_keeps_the_input_boundary_and_adds_only_evidence_fields():
    req = _request()
    payload = h.grounded_payload(req)
    plain = h.concept_payload(req)
    assert set(payload) == set(plain) and payload["input"] == plain["input"]
    assert payload["store"] is False
    schema = payload["text"]["format"]["schema"]
    item = schema["properties"]["proposals"]["items"]
    assert item["properties"]["concept_id"]["enum"] == \
        [c.concept_id for c in ms.candidate_concepts(req.gap_type)]
    assert item["properties"]["basis"]["enum"] == [h.STATED, h.IMPLIED]
    assert payload["text"]["format"]["strict"] is True
    # the grounded prompt keeps every original rule and only replaces the reply clause
    assert payload["instructions"].startswith(h.CONCEPT_INSTRUCTIONS.split(
        "Return PROPOSED with the ids otherwise.")[0])


def test_grounded_admission_keeps_only_stated_verbatim_quotes_and_records_the_rest():
    text = "The drum rotates whenever the handle is turned."
    adapter = h.GroundedOpenAIMsnlAdapter(allow_network=True, transport=FakeTransport(
        _grounded(("MC-ROTATE", " drum rotates ", "STATED"),
                  ("MC-COMPONENT", "handle", "IMPLIED"),
                  ("MC-DRIVE", "it moves", "STATED"))))
    response = adapter.propose(_request(text))
    assert (response.outcome, response.concept_ids) == (ms.PROPOSED, ("MC-ROTATE",))
    assert adapter.withheld[text] == [{"concept_id": "MC-COMPONENT", "reason": "implied"},
                                      {"concept_id": "MC-DRIVE", "reason": "ungrounded"}]


def test_grounded_outcomes_errors_and_all_withheld_map_through_the_local_policy():
    text = "The drum rotates whenever the handle is turned."
    event = ms.AcceptedEvent(ref=ms.LocalRef("t", "c"), accepted_text=text,
                             gap_type="MECHANISM_COMPLETENESS", question_target=None,
                             domain="mechanical", kind=ms.EVENT_ANSWERED)
    cases = [
        (_grounded(("MC-COMPONENT", "handle", "IMPLIED")), ms.DISPOSITION_ABSTAINED),
        (_grounded(outcome="NO_MAPPING"), ms.DISPOSITION_NO_MAPPING),
        (_grounded(outcome="ABSTAIN"), ms.DISPOSITION_ABSTAINED),
        (_reply({}, refusal=True), ms.DISPOSITION_ABSTAINED),
        (_reply({"outcome": "PROPOSED", "concept_ids": ["MC-ROTATE"]}),
         ms.DISPOSITION_ADAPTER_ERROR),
        (_reply({"outcome": "PROPOSED", "proposals": [{"concept_id": "MC-ROTATE"}]}),
         ms.DISPOSITION_ADAPTER_ERROR),
        ((500, b""), ms.DISPOSITION_ADAPTER_ERROR),
        (_grounded(("PF-ENERGY", "drum rotates", "STATED")),
         ms.DISPOSITION_DISCARDED_UNSUPPORTED),
    ]
    for reply, disposition in cases:
        adapter = h.GroundedOpenAIMsnlAdapter(allow_network=True,
                                              transport=FakeTransport(reply))
        assert ms.evaluate(event, adapter).disposition == disposition, reply


def test_circuit_breaker_stops_after_two_auth_failures_or_three_consecutive_failures():
    for replies, sent in (([(401, b"")] * 5, 2), ([(500, b"")] * 5, 3),
                          ([(500, b""), (500, b""), _reply({"outcome": "NOT_UNKNOWN"}),
                            (500, b""), (500, b""), (500, b"")], 6)):
        transport = FakeTransport(*replies)
        adapter = h.OpenAIMsnlAdapter(allow_network=True, transport=transport)
        for _ in range(len(replies)):
            adapter.classify_unknown("I don't know how it works yet, honestly.")
        assert len(transport.calls) == sent, replies
        assert adapter.errors.get(h.ERR_CIRCUIT_OPEN, 0) == len(replies) - sent


def _m(false=(0, 0, 0, 0), hits=(8, 8, 8, 8), abst=0, multi="12/12", neg="4/4",
       neg_meaning="4/4", errors=0, unsupported=0):
    out = {v: {"false_attributions": f, "hits": hh, "match_cases": 8,
               "abstained_on_match": 0, "errors": 0, "discarded_unsupported": 0}
           for v, f, hh in zip(h.VARIETIES, false, hits)}
    out["overall"] = {"false_attributions": sum(false), "hits": sum(hits), "match_cases": 32,
                      "abstained_on_match": abst, "errors": errors,
                      "discarded_unsupported": unsupported}
    out.update(multi_concept_exact=multi, negation_clean=neg, negation_as_meaning_exact=neg_meaning)
    return out


LEXICAL = _m(false=(1, 1, 1, 0), hits=(8, 4, 2, 2), multi="6/12", neg="1/4", neg_meaning="2/4")
UNKNOWN_OK = {"overall": {"explicit_unknown_recognized": "8/8", "false_unknown": 0, "errors": 0}}


def test_frozen_criteria_need_three_runs_for_a_pass_and_fail_on_any_breach():
    good = h.holdout_criteria(LEXICAL, _m(), _m(), UNKNOWN_OK)
    assert [good[k]["status"] for k in ("C1", "C2", "C3", "C4", "C5", "C6")] == [h.PASS] * 6
    assert good["C7"]["status"] == h.NOT_VERIFIED and good["verdict"] == h.NOT_VERIFIED
    breaches = {"C1": _m(false=(0, 0, 0, 1)),            # any variety above lexical fails
                "C2": _m(hits=(8, 8, 5, 8)),
                "C3": _m(multi="7/12"),
                "C4": _m(neg="3/4"),
                "C6": _m(abst=4),
                "C7": _m(unsupported=1)}
    for key, grounded in breaches.items():
        out = h.holdout_criteria(LEXICAL, _m(), grounded, UNKNOWN_OK)
        assert out[key]["status"] == h.FAIL and out["verdict"] == h.FAIL, key
    bad_unknown = {"overall": {"explicit_unknown_recognized": "7/8", "false_unknown": 0,
                               "errors": 0}}
    assert h.holdout_criteria(LEXICAL, _m(), _m(), bad_unknown)["C5"]["status"] == h.FAIL


def test_any_provider_error_invalidates_the_run():
    out = h.holdout_criteria(LEXICAL, _m(), _m(errors=1), UNKNOWN_OK)
    assert out["verdict"] == h.NOT_VERIFIED and "RUN INVALID" in out["reason"]


def test_criteria_thresholds_mirror_the_frozen_fixture_text():
    pack = h._load(h.HOLDOUT_PACK_PATH, h.HOLDOUT_PACK_SHA256)
    criteria = pack["acceptance_criteria"]
    for key, phrase in (("C1", "EVERY variety and overall"), ("C2", "at least 0.75"),
                        ("C2", "ar-gulf-kw and in ar-egy"), ("C3", "At least 8 of the 12"),
                        ("C4", "NEGATION cases propose no concept"),
                        ("C4", "at least 3 of 4 varieties"), ("C5", "8/8"),
                        ("C5", "0 false unknowns"), ("C6", "no more than 0.10"),
                        ("C7", "any provider error invalidates"), ("C7", "3 independent runs")):
        assert phrase in criteria[key], (key, phrase)


def test_holdout_lexical_run_is_offline_and_reproduces_the_frozen_baseline(capsys, monkeypatch):
    def no_network(*_a, **_k):
        raise AssertionError("no network in a lexical held-out run")
    monkeypatch.setattr(toa, "_urllib_transport", no_network)
    assert h.main(["--holdout"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert set(out["arms"]) == {"lexical-baseline-uncalibrated"}
    m = out["arms"]["lexical-baseline-uncalibrated"]["metrics"]
    assert [m[v]["false_attributions"] for v in h.VARIETIES] == [1, 1, 1, 0]
    assert [m[v]["hits"] for v in h.VARIETIES] == [8, 4, 2, 2]
    assert out["criteria"]["verdict"] == h.NOT_VERIFIED


@pytest.mark.parametrize("argv", [["--holdout", "--provider", "openai"],
                                  ["--holdout", "--provider", "openai", "--allow-network"]])
def test_holdout_llm_arms_need_both_permissions(argv, capsys):
    assert h.main(argv) == 2
    assert "refused" in json.loads(capsys.readouterr().out)


def test_rescore_refuses_the_holdout_flag(capsys, tmp_path):
    path = tmp_path / "x.json"
    path.write_text("{}", encoding="utf-8")
    assert h.main(["--rescore", str(path), "--holdout"]) == 2
