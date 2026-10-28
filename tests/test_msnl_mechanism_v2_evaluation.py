"""T2-G / R2 — the ONE v2 evaluation: network-free tests for the frozen fresh
holdout (`tests/fixtures/msnl_mechanism_content_v2_holdout.json`) and the v2
execution controls of `scripts/run_msnl_eval.py` (fresh qualification x3 then
v1 regression x1 on ONE shared 640-attempt / US$25 ledger, fixed evidence
paths, no restart, offline rescore). Every provider path uses a fake
transport; nothing is sent and nothing here is a model result.
"""
import collections
import copy
import hashlib
import json
import pathlib
import re

import pytest

from engine import technical_orchestration_openai as toa
from engine.path_n_questions import get_served_question
from tests.test_msnl_llm_eval_harness import h
from tests.test_msnl_mechanism_content_harness import _mc_reply

ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"


@pytest.fixture(scope="module")
def packs():
    return h._mechanism_v2_holdout()


# ─── the frozen fresh holdout ───────────────────────────────────────────────

def test_the_holdout_is_pinned_and_runs_the_frozen_candidate_instructions(packs):
    fresh, regression = packs
    assert fresh["pack_id"] == "msnl-mechanism-content-v2-holdout"
    assert hashlib.sha256(fresh["arm"]["instructions"].encode()).hexdigest() == \
        h.MECHANISM_V2_INSTRUCTIONS_SHA256 == \
        "8b3027b5daaf1498d3a48fbe23cccda4024cf63abcbfdaea09963eecb7790a4c"
    assert fresh["arm"]["instructions"] == regression["arm"]["instructions"]
    v1 = h._mechanism_pack()
    for key in ("decision", "grounding", "labelling_rules", "categories",
                "acceptance_criteria", "thresholds", "scope", "varieties", "replay"):
        assert fresh[key] == v1[key], key
    assert fresh["arm"]["output_schema"] == v1["arm"]["output_schema"]
    assert regression["cases"] == v1["cases"]
    b = fresh["budget"]
    assert (b["max_attempts_total"], b["qualification_attempts"],
            b["regression_attempts"], b["cost_ceiling_usd"]) == (640, 480, 160, 25.0)
    assert b["pricing"] == v1["budget"]["pricing"]
    assert fresh["evaluation"]["regression_pack_sha256"] == h.MECHANISM_PACK_SHA256


def test_the_design_counts_balance_pairs_and_tentative_groups_hold(packs):
    fresh, _ = packs
    d, cases = fresh["design"], fresh["cases"]
    assert len(cases) == 160 and len({c["case_id"] for c in cases}) == 160
    assert len({c["text"] for c in cases}) == 160
    groups = collections.defaultdict(list)
    for c in cases:
        groups[c["group_id"]].append(c)
        assert c["label"] == fresh["categories"][c["category"]][0]
    assert len(groups) == 40
    for members in groups.values():
        assert sorted(m["variety"] for m in members) == sorted(h.VARIETIES)
        assert len({(m["category"], m["label"], m["domain"], m["question_id"], m["pair_id"])
                    for m in members}) == 1
    first = [m[0] for m in groups.values()]
    assert dict(collections.Counter(c["category"] for c in first)) == \
        {**d["positive_groups"], **d["negative_groups"]}
    assert collections.Counter((c["domain"], c["label"]) for c in first) == {
        ("mechanical", "PRESENT"): 10, ("mechanical", "ABSENT"): 10,
        ("electronics_electrical", "PRESENT"): 10, ("electronics_electrical", "ABSENT"): 10}
    pairs = collections.defaultdict(set)
    for c in first:
        pairs[c["pair_id"]].add((c["label"], c["domain"], c["question_id"]))
    assert len(pairs) == 20
    for members in pairs.values():
        assert {m[0] for m in members} == {"PRESENT", "ABSENT"}
        assert len({m[1:] for m in members}) == 1
    tentative = d["tentative_positive_groups"]
    assert len(tentative) >= 2
    assert all(groups[g][0]["label"] == "PRESENT" for g in tentative)


def test_served_contexts_and_the_frozen_engine_baseline_hold(packs):
    fresh, regression = packs
    for c in fresh["cases"]:
        served = get_served_question("MECHANISM_COMPLETENESS", c["served_index"],
                                     domain=c["domain"])
        assert served.question_id == c["question_id"]
        assert c["served_question"] == (served.text if c["variety"] == "en"
                                        else served.text_ar)
        assert set(c["engine_baseline"]) == set(h.PRIORS)
    assert h.mc_precondition(fresh) == [] and h.mc_precondition(regression) == []


def _shingles(text, n=8):
    words = re.findall(r"\w+", text.lower())
    return {" ".join(words[i:i + n]) for i in range(len(words) - n + 1)}


def test_the_holdout_is_independent_of_v1_the_development_examples_and_older_packs(packs):
    fresh, regression = packs
    older = [c["text"] for c in regression["cases"]]
    cand = json.loads((FIXTURES / "msnl_mechanism_content_v2_candidate.json")
                      .read_text(encoding="utf-8"))
    older += [e["text"] for e in cand["development_examples"]["examples"]]
    older += [i["text"] for i in json.loads((FIXTURES / "msnl_mechanism_preflight_v1.json")
                                            .read_text(encoding="utf-8"))["inputs"]]
    for name in ("msnl_evaluation_pack_v1.json", "msnl_unknown_probe_v1.json",
                 "msnl_holdout_v1.json", "msnl_responsiveness_v1.json"):
        data = json.loads((FIXTURES / name).read_text(encoding="utf-8"))
        older += [c["text"] for c in data["cases"] if isinstance(c.get("text"), str)]
    runs = set().union(*(_shingles(t) for t in older))
    question_runs = set().union(*(_shingles(c["served_question"]) for c in fresh["cases"]))
    for c in fresh["cases"]:
        assert c["text"] not in set(older), c["case_id"]
        assert not ((_shingles(c["text"]) - question_runs) & runs), c["case_id"]
    a = fresh["annotation"]
    for key in ("method", "label_agreement", "disagreement_resolution",
                "reworded_for_eligibility", "independence_check", "human_native_speaker_review"):
        assert a.get(key), key
    assert "NOT PERFORMED" in a["human_native_speaker_review"]


# ─── the v2 execution controls (fake transport) ─────────────────────────────

def _mini(packs, n_fresh=8, n_reg=8):
    fresh, regression = copy.deepcopy(packs[0]), copy.deepcopy(packs[1])
    fresh["cases"] = fresh["cases"][:n_fresh]
    regression["cases"] = regression["cases"][:n_reg]
    return fresh, regression


class Fake:
    def __init__(self, packs, reply=None):
        self.by_text = {c["text"]: c for p in packs for c in p["cases"]}
        self.reply, self.bodies = reply, []

    def __call__(self, url, headers, body, timeout):
        assert url == toa.ENDPOINT and "Authorization" not in headers
        payload = json.loads(body.decode("utf-8"))
        self.bodies.append(payload)
        case = self.by_text[json.loads(payload["input"])["answer"]]
        if self.reply is not None:
            return self.reply(len(self.bodies), case)
        if case["label"] == "PRESENT":
            from engine import answer_stance as st
            seg, term, _ = st._sentence_records(case["text"])[-1]
            return _mc_reply({"responsive": "RESPONSIVE", "stance": "ASSERTS",
                              "mechanism_content": "PRESENT", "quote": seg.strip() + term})
        return _mc_reply({"responsive": "RESPONSIVE", "stance": "ASSERTS",
                          "mechanism_content": "ABSENT", "quote": ""})


def _evaluate(fresh, regression, fake, journal=None):
    adapter = h.OpenAIMsnlAdapter(allow_network=True, transport=fake)
    return h.mechanism_v2_evaluation(adapter, fresh, regression, journal)


def test_qualification_runs_three_passes_then_one_regression_pass_in_order(packs):
    fresh, regression = _mini(packs)
    fake = Fake([fresh, regression])
    q_runs, r_runs, spend = _evaluate(fresh, regression, fake)
    assert [len(r) for r in q_runs] == [8, 8, 8] and [len(r) for r in r_runs] == [8]
    sent = [json.loads(b["input"])["answer"] for b in fake.bodies]
    order = [c["text"] for c in fresh["cases"]] * 3 + [c["text"] for c in regression["cases"]]
    assert sent == order and spend["requests_sent"] == 32
    for body in fake.bodies:
        assert hashlib.sha256(body["instructions"].encode()).hexdigest() == \
            h.MECHANISM_V2_INSTRUCTIONS_SHA256
        assert body["max_output_tokens"] == 4096 and body["store"] is False
    result = h.mechanism_v2_result(fresh, regression, q_runs, r_runs,
                                   {"qualification": [], "regression": []})
    assert result["regression"]["qualifies"] is False
    assert set(result["regression"]["known_failures"]) == set(h.MECHANISM_V1_KNOWN_FAILURES)


def test_one_ledger_caps_attempts_and_cost_across_both_sets(packs):
    fresh, regression = _mini(packs)
    fresh["budget"] = dict(fresh["budget"], max_attempts_total=28)
    fake = Fake([fresh, regression])
    q_runs, r_runs, spend = _evaluate(fresh, regression, fake)
    assert spend["requests_sent"] == 28 == len(fake.bodies)
    assert r_runs and r_runs[0][-1]["error"] == h.ERR_BUDGET
    fresh, regression = _mini(packs)
    one = h._pf_usd(4500 + 1000, 4096, 12.0, 60.0)
    fresh["budget"] = dict(fresh["budget"], cost_ceiling_usd=one * 2)
    fake = Fake([fresh, regression])
    q_runs, r_runs, spend = _evaluate(fresh, regression, fake)
    assert spend["conservative_bound_usd"] <= one * 2 and r_runs == []
    assert any(r["error"] == h.ERR_COST_CEILING for run in q_runs for r in run)
    assert h.mechanism_verdict(fresh, q_runs, [])["campaign_status"] == "INVALID"


def test_an_error_in_qualification_halts_everything_after_it(packs):
    fresh, regression = _mini(packs)
    fake = Fake([fresh, regression], reply=lambda n, case: (500, b"") if n == 3
                else Fake([fresh, regression])(toa.ENDPOINT, {}, json.dumps(
                    {"input": json.dumps({"answer": case["text"]})}).encode(), 1))
    q_runs, r_runs, spend = _evaluate(fresh, regression, fake)
    assert len(fake.bodies) == 3 and r_runs == []
    assert q_runs[0][-1]["error"] == toa.ERR_HTTP_STATUS
    assert h.mechanism_verdict(fresh, q_runs, [])["campaign_status"] == "INVALID"


def test_an_unconfirmed_model_or_incomplete_reply_is_an_error_stop(packs):
    for model, status in (("gpt-6.1-sol", "completed"), ("gpt-6-sol", "incomplete")):
        fresh, regression = _mini(packs)

        def reply(n, case, model=model, status=status):
            s, raw = _mc_reply({"responsive": "RESPONSIVE", "stance": "ASSERTS",
                                "mechanism_content": "ABSENT", "quote": ""}, model)
            body = json.loads(raw)
            body["status"] = status
            return s, json.dumps(body).encode()
        fake = Fake([fresh, regression], reply=reply)
        q_runs, r_runs, _ = _evaluate(fresh, regression, fake)
        assert len(fake.bodies) == 1 and r_runs == []
        assert q_runs[0][0]["error"] in (h.ERR_MODEL_UNCONFIRMED, toa.ERR_INCOMPLETE)


def test_the_journal_tags_every_attempt_with_its_set(packs, tmp_path):
    fresh, regression = _mini(packs, 4, 4)
    path = tmp_path / "journal.jsonl"
    with open(path, "x", encoding="utf-8") as journal:
        _evaluate(fresh, regression, Fake([fresh, regression]), journal)
    lines = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines()]
    sets = [l["set"] for l in lines if l["event"] == "attempt"]
    assert sets == ["qualification"] * 12 + ["regression"] * 4


def test_the_run_is_refused_unless_authorized_new_and_flagged(packs, monkeypatch, tmp_path):
    monkeypatch.setattr(h, "OpenAIMsnlAdapter", None)    # building one would fail
    monkeypatch.setattr(h, "MECHANISM_V2_EVIDENCE_DIR", str(tmp_path))
    monkeypatch.setattr(h, "MECHANISM_V2_REPORT_PATH", str(tmp_path / "report.json"))
    monkeypatch.setattr(h, "MECHANISM_V2_JOURNAL_PATH", str(tmp_path / "journal.jsonl"))
    monkeypatch.setattr(h, "MECHANISM_V2_EVALUATION_AUTHORIZED", False)
    out = h.mechanism_v2_run("openai", True, True)
    assert out["provider_requests"] == 0 and "not authorized" in out["refused"]
    monkeypatch.setattr(h, "MECHANISM_V2_EVALUATION_AUTHORIZED", True)
    (tmp_path / "journal.jsonl").write_text("{}\n", encoding="utf-8")
    out = h.mechanism_v2_run("openai", True, True)
    assert out["provider_requests"] == 0 and "already started" in out["refused"]
    (tmp_path / "report.json").write_text("{}", encoding="utf-8")
    out = h.mechanism_v2_run("openai", True, True)
    assert out["provider_requests"] == 0 and "already exists" in out["refused"]
    assert h.mechanism_v2_run("lexical", False, False)["provider_requests"] == 0
    assert h.main(["--mechanism-v2-evaluation", "--provider", "openai"]) == 2
    assert h.main(["--mechanism-v2-evaluation", "--mechanism-content"]) == 2
    assert h.main(["--mechanism-v2-rescore", "x.json", "--allow-network"]) == 2


def test_the_other_execution_paths_stay_closed():
    assert h.MECHANISM_CONTENT_CAMPAIGN_AUTHORIZED is False
    assert h.MECHANISM_PREFLIGHT_AUTHORIZED is False


def test_the_offline_rescore_replays_a_saved_report(packs, monkeypatch, tmp_path):
    fresh, regression = _mini(packs)
    q_runs, r_runs, _ = _evaluate(fresh, regression, Fake([fresh, regression]))
    saved = {"holdout_sha256": h.MECHANISM_V2_HOLDOUT_SHA256,
             "instructions_sha256": h.MECHANISM_V2_INSTRUCTIONS_SHA256,
             "case_level": {"qualification": [[{"case_id": r["case_id"], "reply": r["reply"],
                                                "error": r["error"]} for r in run]
                                              for run in q_runs],
                            "regression": [[{"case_id": r["case_id"], "reply": r["reply"],
                                             "error": r["error"]} for r in run]
                                           for run in r_runs]}}
    path = tmp_path / "saved.json"
    path.write_text(json.dumps(saved, ensure_ascii=False), encoding="utf-8")
    monkeypatch.setattr(h, "_mechanism_v2_holdout", lambda: (fresh, regression))
    monkeypatch.setattr(h, "OpenAIMsnlAdapter", None)
    out = h.mechanism_v2_rescore(str(path))
    assert [[r["decision"] for r in run] for run in out["case_level"]["qualification"]] == \
        [[r["decision"] for r in run] for run in q_runs]
    assert out["result"]["regression"]["qualifies"] is False


def test_the_v2_lexical_check_has_no_product_or_store_side_effect(tmp_path):
    import os
    import subprocess
    import sys
    db = tmp_path / "must-not-exist.sqlite"
    code = (
        "import importlib.util, sqlite3, sys\n"
        "def boom(*a, **k): raise SystemExit('side effect')\n"
        "sqlite3.connect = boom\n"
        "spec = importlib.util.spec_from_file_location('h', %r)\n"
        "h = importlib.util.module_from_spec(spec); spec.loader.exec_module(h)\n"
        "h.OpenAIMsnlAdapter = boom\n"
        "out = h.mechanism_v2_run('lexical', False, False)\n"
        "assert out['provider_requests'] == 0 and not any(out['precondition_violations'].values())\n"
        "print(sorted(m for m in ('web', 'web.app') if m in sys.modules))\n"
    ) % str(ROOT / "scripts" / "run_msnl_eval.py")
    env = dict(os.environ, INVENTORAI_DB_PATH=str(db))
    out = subprocess.run([sys.executable, "-c", code], cwd=ROOT, env=env,
                         capture_output=True, text=True, timeout=600)
    assert out.returncode == 0, out.stderr
    assert out.stdout.strip() == "[]"
    assert not db.exists()
