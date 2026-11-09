"""R2 cross-idea facet — the frozen project-context veto falsification: harness tests.

Network-free: every reply comes from a fake transport, nothing is sent and
nothing here is a model result. Pins the committed manifest (digest, selection,
swaps, instructions, budget, stop rules), the exact request body, the
fail-closed cost reservation, the veto-only composition, the three decisive
falsifications, every INVALID path, the separate reporting of classification
and progression consequences, and the closed run gate.
"""
import collections
import copy
import hashlib
import json
import os

import pytest

from engine import technical_orchestration_openai as toa
from tests.test_msnl_llm_eval_harness import h, _reply

MANIFEST_SHA256 = "a43232da68a1bf3067a7027b280f7fe3a0f5811487d085424bee38b63b2928f0"
PACK_SHA256 = "aec7ad88c677e8a5fc1bdb7fbb7eb283c5ade738a8769d92a0480bbf86c4449a"


@pytest.fixture(scope="module")
def frozen():
    return h.project_context_manifest()


def _usage(inp=900, out=120):
    return {"input_tokens": inp, "output_tokens": out,
            "output_tokens_details": {"reasoning_tokens": 40}, "total_tokens": inp + out}


def _wrap(obj, model="gpt-6-sol", usage=None, status=200, tier="default"):
    status, raw = _reply(obj, status=status)
    body = json.loads(raw.decode("utf-8"))
    body.update(model=model, usage=_usage() if usage is None else usage, service_tier=tier)
    return status, json.dumps(body).encode("utf-8")


class Fake:
    """Answers each request from its item; ``decide(item, answer)`` returns the
    reply object (or a full (status, raw) pair)."""

    def __init__(self, manifest, pack, decide):
        self.by_input = {}
        for it in manifest["items"]:
            idea, q, a = h.pc_item_text(manifest, pack, it)
            self.by_input[json.dumps({"project_idea": idea, "question": q, "answer": a},
                                     ensure_ascii=False, sort_keys=True)] = (it, a)
        self.decide, self.bodies = decide, []

    def __call__(self, url, headers, body, timeout):
        assert url == toa.ENDPOINT and "Authorization" not in headers
        payload = json.loads(body.decode("utf-8"))
        self.bodies.append(payload)
        item, answer = self.by_input[payload["input"]]
        out = self.decide(item, answer)
        return out if isinstance(out, tuple) else _wrap(out)


def _refusal():
    status, raw = _reply({}, refusal=True)
    body = json.loads(raw.decode("utf-8"))
    body.update(model="gpt-6-sol", usage=_usage(), service_tier="default")
    return status, json.dumps(body).encode("utf-8")


def _expected(item, answer):
    """A reply that is always right: the expected verdict, a grounded quote."""
    v = item["expected_verdict"]
    return {"verdict": v, "quote": "" if v == "UNCERTAIN" else " ".join(answer.split()[:4])}


def _run(frozen, decide, manifest=None):
    manifest = manifest or frozen[0]
    fake = Fake(manifest, frozen[1], decide)
    adapter = h.OpenAIMsnlAdapter(allow_network=True, transport=fake)
    outcome, stop, rows, spend = h.project_context_run(adapter, manifest, frozen[1])
    return outcome, stop, rows, spend, fake


def _ordered(manifest):
    return sorted(manifest["items"], key=lambda it: it["request_index"])


# ─── the frozen manifest ───────────────────────────────────────────────────────

def test_the_manifest_pack_and_instructions_are_pinned(frozen):
    manifest, pack = frozen
    assert h.PROJECT_CONTEXT_MANIFEST_SHA256 == MANIFEST_SHA256
    assert hashlib.sha256(open(h.PROJECT_CONTEXT_MANIFEST_PATH, "rb").read()).hexdigest() == MANIFEST_SHA256
    assert manifest["source_pack"]["sha256"] == PACK_SHA256
    assert hashlib.sha256(manifest["arm"]["instructions"].encode()).hexdigest() == \
        manifest["arm"]["instructions_sha256"]
    assert manifest["provider"]["model"] == "gpt-6-sol" and "NONE" in manifest["provider"]["substitution"]
    # The gate may be open ONLY for the one authorized run, i.e. while no evidence of it
    # exists; once the evidence exists it must be closed again.
    assert isinstance(h.PROJECT_CONTEXT_RUN_AUTHORIZED, bool)
    if os.path.exists(h.PROJECT_CONTEXT_REPORT_PATH) or os.path.exists(h.PROJECT_CONTEXT_JOURNAL_PATH):
        assert h.PROJECT_CONTEXT_RUN_AUTHORIZED is False
    assert h.PC_ALLOWED_SERVICE_TIERS == ("default",)
    assert "NOT AUTHORIZED TO RUN" in manifest["status"]


def test_selection_is_sixty_items_covering_every_project_category_and_language(frozen):
    manifest, pack = frozen
    items = manifest["items"]
    assert len(items) == 60 <= manifest["budget"]["max_provider_requests"] == 60
    assert sorted(it["request_index"] for it in items) == list(range(1, 61))
    kinds = collections.Counter(it["kind"] for it in items)
    assert kinds == {"PACK_CASE": 48, "IDEA_SWAP": 12}
    cases = [it for it in items if it["kind"] == "PACK_CASE"]
    assert {it["category"] for it in cases} == set(pack["categories"])
    assert collections.Counter(it["project_id"] for it in items) == {p: 10 for p in
                                                                     ("P1", "P2", "P3", "P4", "P5", "P6")}
    assert collections.Counter(it["variety"] for it in items) == {"en": 30, "ar-msa": 30}
    by = {c["case_id"]: c for c in pack["cases"]}
    for it in items:                                  # the #948 pack is used, never changed
        src = by[it["source_case_id"]]
        assert it["engine_baseline"] == src["engine_baseline"]
        if it["kind"] == "PACK_CASE":
            assert it["expected_outcome"] == src["expected_outcome"]


def test_swaps_keep_answer_question_and_language_and_were_rechecked(frozen):
    manifest, pack = frozen
    domain = {p["project_id"]: p["domain"] for p in pack["projects"]}
    for it in (i for i in manifest["items"] if i["kind"] == "IDEA_SWAP"):
        assert it["category"] in ("NEW_DETAIL", "FAITHFUL_PARAPHRASE")
        assert it["idea_project_id"] != it["project_id"]
        assert domain[it["idea_project_id"]] == domain[it["project_id"]]
        assert (it["expected_verdict"], it["expected_outcome"]) == ("UNRELATED", "NO_CREDIT")
        idea, q, a = h.pc_item_text(manifest, pack, it)
        src = next(c for c in pack["cases"] if c["case_id"] == it["source_case_id"])
        assert (q, a) == (src["served_question"], src["text"]) and idea != src["project_idea"]
        got = {p: h.mc_engine_outcome(pack, dict(src, project_idea=idea), p) for p in h.PRIORS}
        assert {p: {"status_after": o["status_after"], "granted": o["granted"]}
                for p, o in got.items()} == it["engine_baseline"]
    assert "12/12 swaps UNRELATED" in manifest["swap_recheck"]["result"]


# ─── the request and the cost bound ────────────────────────────────────────────

def test_the_request_carries_only_idea_question_and_answer(frozen):
    manifest, pack = frozen
    it = _ordered(manifest)[0]
    payload = h.pc_payload(manifest, pack, it)
    assert set(payload) == {"model", "instructions", "input", "store", "max_output_tokens", "text"}
    assert payload["store"] is False and payload["max_output_tokens"] == 4000
    assert set(json.loads(payload["input"])) == {"project_idea", "question", "answer"}
    for leak in (it["item_id"], it["category"], it["expected_outcome"], "engine_baseline",
                 it["source_case_id"]):
        assert leak not in payload["input"] and leak not in payload["instructions"]
    schema = payload["text"]["format"]
    assert schema["strict"] is True and schema["schema"]["properties"]["verdict"]["enum"] == \
        list(h.PC_VERDICTS)


def test_reservations_are_bounded_recomputed_and_under_the_ceiling(frozen):
    manifest, pack = frozen
    b = manifest["budget"]
    res = [round(h.pc_reservation_usd(manifest, h.pc_payload(manifest, pack, it)), 6)
           for it in _ordered(manifest)]
    assert res == b["reservations_usd_by_request_index"]
    assert round(sum(res), 6) == b["worst_case_reserved_usd_total"] < b["cost_ceiling_usd"] == 5.0
    for it in _ordered(manifest):
        payload = h.pc_payload(manifest, pack, it)
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        assert h.pc_input_token_bound(manifest, payload) == len(body) + 1000
    assert b["pricing"]["input_usd_per_1m"] == 2.0 and b["pricing"]["output_usd_per_1m"] == 10.0


# ─── decisions and composition ────────────────────────────────────────────────

def test_grounding_and_veto_only_composition():
    answer = "The lever lifts the gate and the spring pulls it back."
    assert h.pc_decision(answer, {"verdict": "RELATED", "quote": "lever lifts the gate"}) == "RELATED"
    assert h.pc_decision(answer, {"verdict": "RELATED", "quote": "a sentence not in it"}) == "UNGROUNDED"
    assert h.pc_decision(answer, {"verdict": "UNRELATED", "quote": ""}) == "UNGROUNDED"
    assert h.pc_decision(answer, {"verdict": "UNCERTAIN", "quote": ""}) == "UNCERTAIN"
    assert h.pc_decision(answer, {"verdict": "UNCERTAIN", "quote": "the lever"}) == "UNGROUNDED"
    granted = {"engine_baseline": {p: {"granted": True, "status_after": "PARTIAL"} for p in h.PRIORS}}
    refused = {"engine_baseline": {p: {"granted": False, "status_after": "OPEN"} for p in h.PRIORS}}
    for decision in ("RELATED", "UNRELATED", "UNCERTAIN", "CONFLICT", "UNGROUNDED"):
        for item in (granted, refused):
            for v in h.pc_compose(item, decision).values():
                assert v["composed_granted"] <= v["engine_granted"]      # never new credit
                assert v["composed_granted"] == (v["engine_granted"] and decision == "RELATED")


# ─── the run: outcomes and stops ──────────────────────────────────────────────

def test_a_perfect_classifier_is_not_falsified_and_removes_incumbent_false_grants(frozen):
    outcome, stop, rows, spend, fake = _run(frozen, _expected)
    assert (outcome, stop) == (h.PC_NOT_FALSIFIED, None)
    assert len(rows) == 60 and spend["requests_sent"] == 60 and len(fake.bodies) == 60
    assert [json.loads(b["input"])["answer"] for b in fake.bodies] == \
        [h.pc_item_text(frozen[0], frozen[1], it)[2] for it in _ordered(frozen[0])]
    report = h.project_context_report(frozen[0], outcome, stop, rows, spend)
    assert report["untested_items"] == [] and report["overall"]["tested"] == 60
    assert report["overall"].get("correct_no", 0) == 0
    assert report["overall"].get("surviving_false_grant_veto_OPEN", 0) == 0
    assert report["overall"]["incumbent_false_grant_removed_OPEN"] > 0
    assert "newly_withheld_eligible_OPEN" not in report["overall"]


def _first(manifest, pred):
    return next(it for it in _ordered(manifest) if pred(it))


def _granted(it):
    return any(it["engine_baseline"][p]["granted"] for p in h.PRIORS)


@pytest.mark.parametrize("name, pred, wrong, outcome", [
    ("unrelated", lambda it: it["expected_verdict"] == "UNRELATED" and _granted(it), "RELATED",
     "FALSIFIED_UNRELATED_CREDIT_SURVIVED"),
    ("eligible", lambda it: it["expected_outcome"] == "GRANT_ELIGIBLE" and _granted(it), "UNRELATED",
     "FALSIFIED_ELIGIBLE_CREDIT_WITHHELD"),
    ("conflict", lambda it: it["expected_verdict"] == "CONFLICT" and _granted(it), "RELATED",
     "FALSIFIED_CONFLICT_SILENTLY_GRANTED"),
])
def test_each_decisive_failure_stops_at_once_and_lists_the_untested(frozen, name, pred, wrong, outcome):
    target = _first(frozen[0], pred)

    def decide(item, answer):
        if item["item_id"] == target["item_id"]:
            return {"verdict": wrong, "quote": " ".join(answer.split()[:4])}
        return _expected(item, answer)
    got, stop, rows, spend, fake = _run(frozen, decide)
    assert got == outcome and (stop["reason"], stop["item_id"]) == (outcome, target["item_id"])
    assert (stop["verdict"], stop["decision"]) == (wrong, wrong)         # the cause is recorded
    assert len(fake.bodies) == target["request_index"] == len(rows)
    report = h.project_context_report(frozen[0], got, stop, rows, spend)
    assert len(report["untested_items"]) == 60 - target["request_index"]


def test_abstaining_on_an_eligible_item_the_engine_did_not_credit_never_falsifies(frozen):
    target = _first(frozen[0], lambda it: it["expected_outcome"] == "GRANT_ELIGIBLE" and not _granted(it))

    def decide(item, answer):
        if item["item_id"] == target["item_id"]:
            return {"verdict": "UNCERTAIN", "quote": ""}
        return _expected(item, answer)
    outcome, stop, rows, spend, _ = _run(frozen, decide)
    assert outcome == h.PC_NOT_FALSIFIED
    report = h.project_context_report(frozen[0], outcome, stop, rows, spend)
    assert "abstention_on_eligible" not in report["overall"]          # F3 sits inside F2
    assert report["overall"]["decision_UNCERTAIN"] == 1 + sum(
        1 for it in frozen[0]["items"] if it["expected_verdict"] == "UNCERTAIN")


def test_an_ungrounded_related_withholds_eligible_credit_but_cannot_falsify_unrelated(frozen):
    eligible = _first(frozen[0], lambda it: it["expected_outcome"] == "GRANT_ELIGIBLE" and _granted(it))
    unrelated = _first(frozen[0], lambda it: it["expected_verdict"] == "UNRELATED" and _granted(it))

    def ungrounded_on(target):
        def decide(item, answer):
            if item["item_id"] == target["item_id"]:
                return {"verdict": "RELATED", "quote": "words that are not in the answer"}
            return _expected(item, answer)
        return decide
    outcome, stop, rows, spend, _ = _run(frozen, ungrounded_on(eligible))
    assert (outcome, stop["decision"]) == (h.PC_FALSIFIED_ELIGIBLE, "UNGROUNDED")
    outcome, stop, rows, spend, _ = _run(frozen, ungrounded_on(unrelated))
    assert outcome == h.PC_NOT_FALSIFIED
    row = next(r for r in rows if r["item_id"] == unrelated["item_id"])
    assert row["decision"] == "UNGROUNDED" and not any(v["composed_granted"] for v in row["composed"].values())


@pytest.mark.parametrize("reply, reason", [
    (lambda item, answer: (500, b"{}"), "http_status"),
    (lambda item, answer: _wrap(_expected(item, answer), model="gpt-6.1-sol"), "model_unconfirmed"),
    (lambda item, answer: _wrap({"verdict": "MAYBE", "quote": ""}), "malformed"),
    (lambda item, answer: _wrap({"verdict": "RELATED"}), "malformed"),
    (lambda item, answer: _wrap(_expected(item, answer), usage={"output_tokens": 10}), "usage_unknown"),
    (lambda item, answer: _wrap(_expected(item, answer), usage=_usage(out=4001)), "cost_unbounded"),
    (lambda item, answer: _wrap(_expected(item, answer), usage=_usage(inp=999999)),
     "input_tokens_over_reserved_bound"),
    (lambda item, answer: _refusal(), "refusal"),
    (lambda item, answer: (200, json.dumps({"status": "incomplete", "output": [], "model": "gpt-6-sol",
                                            "usage": _usage(), "service_tier": "default"}).encode()),
     "incomplete"),
    (lambda item, answer: _wrap(_expected(item, answer), tier="priority"), "service_tier_not_standard"),
    (lambda item, answer: _wrap(_expected(item, answer), tier=None), "service_tier_not_standard"),
])
def test_every_invalid_path_stops_at_the_first_request_without_retry(frozen, reply, reason):
    outcome, stop, rows, spend, fake = _run(frozen, reply)
    assert outcome == h.PC_INVALID and len(fake.bodies) == 1 and len(rows) == 1
    assert stop["reason"] == reason


def test_a_transport_exception_is_invalid_without_retry(frozen):
    def boom(item, answer):
        raise OSError("network down")
    outcome, stop, rows, spend, fake = _run(frozen, boom)
    assert outcome == h.PC_INVALID and stop["reason"] == "transport" and len(fake.bodies) == 1


def test_an_exhausted_allocation_is_invalid(frozen):
    manifest = copy.deepcopy(frozen[0])
    manifest["budget"]["max_provider_requests"] = 3
    outcome, stop, rows, spend, fake = _run(frozen, _expected, manifest)
    assert outcome == h.PC_INVALID and stop["reason"] == "budget_exhausted"
    assert len(fake.bodies) == 3 and spend["requests_sent"] == 3


def test_the_pinned_maximum_input_bound_recomputes(frozen):
    manifest, pack = frozen
    assert manifest["budget"]["max_input_token_bound"] == max(
        h.pc_input_token_bound(manifest, h.pc_payload(manifest, pack, it)) for it in manifest["items"])


def test_the_cost_ceiling_refuses_before_sending(frozen):
    manifest = copy.deepcopy(frozen[0])
    manifest["budget"]["cost_ceiling_usd"] = 0.01
    outcome, stop, rows, spend, fake = _run(frozen, _expected, manifest)
    assert outcome == h.PC_INVALID and stop["reason"] == "cost_ceiling" and fake.bodies == []


def test_journal_keeps_no_prompt_or_reply_text(frozen, tmp_path):
    path = tmp_path / "journal.jsonl"
    fake = Fake(frozen[0], frozen[1], _expected)
    adapter = h.OpenAIMsnlAdapter(allow_network=True, transport=fake)
    with open(path, "w", encoding="utf-8") as journal:
        h.project_context_run(adapter, frozen[0], frozen[1], journal)
    outcome, stop, rows, spend, _ = _run(frozen, _expected)
    report = json.dumps(h.project_context_report(frozen[0], outcome, stop, rows, spend), ensure_ascii=False)
    for text in (path.read_text(encoding="utf-8"), report):
        assert frozen[0]["arm"]["instructions"][:60] not in text
        for it in _ordered(frozen[0]):
            idea, q, a = h.pc_item_text(frozen[0], frozen[1], it)
            assert a not in text and idea not in text and q not in text


# ─── the closed gate ──────────────────────────────────────────────────────────

def test_the_run_is_refused_while_not_authorized_and_sends_nothing(monkeypatch):
    monkeypatch.setattr(h, "PROJECT_CONTEXT_RUN_AUTHORIZED", False)

    def boom(*a, **k):
        raise AssertionError("no adapter may be built")
    monkeypatch.setattr(h, "OpenAIMsnlAdapter", boom)
    out = h.project_context_falsification("openai", True, True)
    assert out["provider_requests"] == 0 and "not authorized" in out["refused"]
    plan = h.project_context_falsification("lexical", False, False)
    assert plan["items"] == 60 and plan["baseline_drift"] == []
    assert plan["worst_case_reserved_usd"] < plan["ceiling_usd"]
    assert h.main(["--project-context-falsification", "--provider", "openai"]) == 2


def test_the_authorized_path_writes_exclusive_evidence_once(frozen, monkeypatch, tmp_path):
    """With the gate opened ONLY inside this test, a fake transport and a temporary
    evidence directory: one run writes journal and report; a second is refused."""
    real = h.OpenAIMsnlAdapter
    monkeypatch.setattr(h, "PROJECT_CONTEXT_RUN_AUTHORIZED", True)
    monkeypatch.setattr(h, "PROJECT_CONTEXT_EVIDENCE_DIR", str(tmp_path))
    monkeypatch.setattr(h, "PROJECT_CONTEXT_JOURNAL_PATH", str(tmp_path / "journal.jsonl"))
    monkeypatch.setattr(h, "PROJECT_CONTEXT_REPORT_PATH", str(tmp_path / "report.json"))
    fake = Fake(frozen[0], frozen[1], _expected)
    monkeypatch.setattr(h, "OpenAIMsnlAdapter",
                        lambda allow_network=False: real(allow_network=allow_network, transport=fake))
    with pytest.raises(SystemExit):
        h.project_context_falsification("openai", True, False)        # both network flags needed
    out = h.project_context_falsification("openai", True, True)
    assert out["outcome"] == h.PC_NOT_FALSIFIED and out["provider_requests"] == 60
    report = json.loads((tmp_path / "report.json").read_text(encoding="utf-8"))
    assert report["outcome"] == h.PC_NOT_FALSIFIED and report["untested_items"] == []
    again = h.project_context_falsification("openai", True, True)
    assert "already exists" in again["refused"] and again["provider_requests"] == 0
    assert len(fake.bodies) == 60


# ─── the ONE authorized run's evidence (2026-11-09) ───────────────────────────

def test_the_recorded_run_is_internally_consistent_and_the_gate_is_closed(frozen):
    """The committed report recomputes from its own rows, agrees with the fsynced
    journal and stayed inside the authorization: gpt-6-sol, Standard tier, at most
    60 requests, under US$5, no error, no retry."""
    assert h.PROJECT_CONTEXT_RUN_AUTHORIZED is False
    report = json.load(open(h.PROJECT_CONTEXT_REPORT_PATH, encoding="utf-8"))
    journal = [json.loads(line) for line in open(h.PROJECT_CONTEXT_JOURNAL_PATH, encoding="utf-8")]
    assert report == json.loads(json.dumps(h.project_context_report(
        frozen[0], report["outcome"], report["stop"], report["rows"], report["spend"]), sort_keys=True))
    attempts = [e for e in journal if e["event"] == "attempt"]
    reserved = [e for e in journal if e["event"] == "reserved"]
    assert journal[0]["event"] == "start" and journal[-1]["event"] == "end"
    assert journal[0]["manifest_sha256"] == MANIFEST_SHA256 and journal[0]["model"] == "gpt-6-sol"
    assert len(attempts) == len(reserved) == report["spend"]["requests_sent"] == len(report["rows"]) <= 60
    assert [a["item_id"] for a in attempts] == [it["item_id"] for it in _ordered(frozen[0])][:len(attempts)]
    assert {a["model"] for a in attempts} == {"gpt-6-sol"} and {a["service_tier"] for a in attempts} == {"default"}
    assert all(a["error"] is None and a["http_status"] == 200 for a in attempts)
    total = sum(a["measured_cost_usd"] for a in attempts)
    assert abs(total - report["spend"]["measured_cost_usd"]) < 1e-6 and total < 5.0
    assert report["outcome"] == h.PC_FALSIFIED_ELIGIBLE == report["stop"]["reason"]
    assert report["stop"]["item_id"] == attempts[-1]["item_id"] == "P4-C02-ar-msa"
    assert len(report["untested_items"]) == 60 - len(attempts)
