"""T2-G / R2 — the ONE Owner-authorized mechanism-content campaign: network-free
tests for its pre-execution amendment 02 and the campaign-path controls of
`scripts/run_msnl_eval.py` (currency ceiling and reservation, model identity,
error stops, progressive journal, duplicate-run refusal, frozen-pack
integrity). Every provider path uses a fake transport; nothing is sent.
"""
import copy
import hashlib
import json

import pytest

from engine import technical_orchestration_openai as toa
from tests.test_msnl_llm_eval_harness import h
from tests.test_msnl_mechanism_content_harness import _mc_reply, _mini_pack, _perfect

CASES_SHA256 = "4bf1399bc507a11e3c1da1e45a2213539f0e96da494b5861996b4b2bb3a762fc"


@pytest.fixture(scope="module")
def pack():
    return h._mechanism_pack()


@pytest.fixture(scope="module")
def spec():
    with open(h.MECHANISM_PACK_PATH, encoding="utf-8") as fh:
        return json.load(fh)


class Fake:
    """Answers each request from its case through ``decide``; records bodies."""

    def __init__(self, pack, decide=_perfect, reply=None):
        self.by_text = {c["text"]: c for c in pack["cases"]}
        self.decide, self.reply, self.bodies = decide, reply, []

    def __call__(self, url, headers, body, timeout):
        assert url == toa.ENDPOINT and "Authorization" not in headers
        payload = json.loads(body.decode("utf-8"))
        self.bodies.append(payload)
        if self.reply is not None:
            return self.reply(len(self.bodies))
        case = self.by_text[json.loads(payload["input"])["answer"]]
        return _mc_reply(self.decide(case))


def _campaign(pack, fake, journal=None):
    adapter = h.OpenAIMsnlAdapter(allow_network=True, transport=fake)
    return h.mechanism_campaign(adapter, pack, journal)


# ─── amendment 02: resource limits only ─────────────────────────────────────

def test_amendment_02_changes_resource_limits_only(pack):
    t, b = pack["thresholds"], pack["budget"]
    assert t["max_output_tokens"] == 4096 and t["max_input_characters"] == 6000
    assert t["max_provider_requests"] == 480 == t["VS1_runs"] * len(pack["cases"])
    assert (t["VP1_overall_min"], t["VP1_variety_min"], t["VP2_max_parity_gap"],
            t["VA1_max_positive_abstention"], t["VS1_min_outcome_agreement"],
            t["VC1_max_false_grants"]) == (0.95, 0.9, 0.1, 0.05, 0.95, 0)
    assert b["cost_ceiling_usd"] == 25.0
    assert (b["pricing"]["input_usd_per_1m"], b["pricing"]["output_usd_per_1m"]) == (2.0, 10.0)
    assert (b["reservation_input_usd_per_1m"], b["reservation_output_usd_per_1m"]) == \
        (12.0, 60.0)
    amendment = pack["annotation"]["pre_execution_amendment_02"]
    assert amendment["pack_sha256_before"] == \
        "c4c1d7e484de5abac1022d59d12b47816f2093f5191809e47bd75b89fb8d82ea"
    assert "pre_execution_amendment_02" in pack["annotation"]["preregistration_order"]
    cases = hashlib.sha256(json.dumps(pack["cases"], ensure_ascii=False,
                                      sort_keys=True).encode()).hexdigest()
    assert cases == CASES_SHA256
    assert hashlib.sha256(pack["arm"]["instructions"].encode()).hexdigest() == \
        h.MECHANISM_PREFLIGHT_INSTRUCTIONS_SHA256          # the tested instructions
    assert h._preflight_pack()["pack_id"] == "msnl-mechanism-preflight-v1"


def test_every_campaign_request_is_the_tested_configuration_at_cap_4096(pack):
    fake = Fake(pack)
    one = copy.deepcopy(pack)
    one["cases"] = pack["cases"][:3]
    one["thresholds"] = dict(pack["thresholds"], VS1_runs=1, max_provider_requests=3)
    runs, requests, _ = _campaign(one, fake)
    assert requests == 3 == len(fake.bodies)
    for body, case in zip(fake.bodies, one["cases"]):
        assert body["max_output_tokens"] == 4096
        expected = h.mechanism_payload(pack, case)
        assert body == expected and body["store"] is False and "reasoning" not in body
        assert body["instructions"] == pack["arm"]["instructions"]


# ─── the currency ceiling and the reservation ───────────────────────────────

def test_the_whole_campaign_fits_the_ceiling_at_measured_like_usage(spec):
    pack = _mini_pack(spec)
    runs, requests, spend = _campaign(pack, Fake(pack))
    assert requests == 3 * len(pack["cases"]) and spend["requests_sent"] == requests
    one = (700 * 12.0 + 90 * 60.0) / 1e6
    assert spend["conservative_bound_usd"] == pytest.approx(requests * one, abs=1e-5)
    assert spend["measured_cost_usd"] == pytest.approx(
        requests * (700 * 2.0 + 90 * 10.0) / 1e6, abs=1e-5)
    assert spend["measured_cost_complete"] is True and spend["ceiling_usd"] == 25.0
    row = runs[0][0]["attempt"]
    assert row["model"] == "gpt-6-sol" and row["http_status"] == 200
    assert row["usage"]["reasoning_tokens"] == 20 and row["bound_usd"] < row["reserved_usd"]


def test_no_request_is_sent_when_its_reservation_would_exceed_the_ceiling(spec):
    pack = _mini_pack(spec)
    first = h._pf_usd(len(json.dumps(h.mechanism_payload(pack, pack["cases"][0]),
                                     ensure_ascii=False).encode()) + 1000, 4096, 12.0, 60.0)
    pack["budget"] = dict(pack["budget"], cost_ceiling_usd=first + 0.03)
    fake = Fake(pack)
    runs, requests, spend = _campaign(pack, fake)
    assert requests == len(fake.bodies) >= 1
    assert runs[-1][-1]["error"] == h.ERR_COST_CEILING
    assert spend["conservative_bound_usd"] <= pack["budget"]["cost_ceiling_usd"]
    assert h.mechanism_verdict(pack, runs, [])["campaign_status"] == "INVALID"


def test_uncertain_cost_is_charged_its_whole_reservation_and_stops(spec):
    pack = _mini_pack(spec)
    fake = Fake(pack, reply=lambda n: (500, b""))
    runs, requests, spend = _campaign(pack, fake)
    assert requests == 1 and runs[0][0]["error"] == toa.ERR_HTTP_STATUS
    attempt = runs[0][0]["attempt"]
    assert attempt["bound_usd"] == attempt["reserved_usd"]
    assert spend["conservative_bound_usd"] == attempt["reserved_usd"]
    assert spend["measured_cost_complete"] is False


# ─── model identity and every other error stop ──────────────────────────────

def _body(model="gpt-6-sol", status="completed", reason=None, output_tokens=90,
          reply=None):
    s, raw = _mc_reply(reply or {"responsive": "RESPONSIVE", "stance": "ASSERTS",
                                 "mechanism_content": "ABSENT", "quote": ""}, model)
    body = json.loads(raw)
    body["status"] = status
    body["usage"]["output_tokens"] = output_tokens
    if reason:
        body["incomplete_details"] = {"reason": reason}
    return lambda n: (s, json.dumps(body).encode())


@pytest.mark.parametrize("reply,kind", [
    (_body(model="gpt-6.1-sol"), h.ERR_MODEL_UNCONFIRMED),
    (_body(model=None), h.ERR_MODEL_UNCONFIRMED),
    (_body(status="incomplete", reason="max_output_tokens"), toa.ERR_INCOMPLETE),
    (_body(status="incomplete", reason="content_filter"), toa.ERR_INCOMPLETE),
    (_body(output_tokens=4097), h.ERR_COST_UNBOUNDED),
    (_body(reply={"responsive": "RESPONSIVE"}), toa.ERR_MALFORMED),
    (lambda n: (401, b""), toa.ERR_HTTP_STATUS),
])
def test_every_error_stops_the_campaign_after_one_request(spec, reply, kind):
    pack = _mini_pack(spec)
    fake = Fake(pack, reply=reply)
    runs, requests, _ = _campaign(pack, fake)
    assert requests == 1 == len(fake.bodies)
    assert runs[0][0]["error"] == kind and runs[0][0]["decision"] == h.MC_ERROR
    result = h.mechanism_verdict(pack, runs, [])
    assert result["campaign_status"] == "INVALID" and result["verdict"] == "FAIL"


def test_a_transport_failure_stops_without_retry(spec):
    pack = _mini_pack(spec)

    def boom(n):
        raise OSError("down")
    runs, requests, spend = _campaign(pack, Fake(pack, reply=boom))
    assert requests == 1 and runs[0][0]["error"] == toa.ERR_TRANSPORT
    assert spend["conservative_bound_usd"] == runs[0][0]["attempt"]["reserved_usd"]


# ─── progressive journal and duplicate-run refusal ──────────────────────────

def test_the_journal_records_every_reservation_and_attempt_as_it_happens(spec, tmp_path):
    pack = _mini_pack(spec)
    path = tmp_path / "journal.jsonl"
    with open(path, "x", encoding="utf-8") as journal:
        runs, requests, _ = _campaign(pack, Fake(pack), journal)
    lines = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines()]
    assert [l["event"] for l in lines] == ["reserved", "attempt"] * requests
    assert all(l["model"] == "gpt-6-sol" for l in lines if l["event"] == "attempt")
    assert "instructions" not in path.read_text(encoding="utf-8")


def _authorized_pack(monkeypatch, pack, evidence):
    monkeypatch.setattr(h, "_mechanism_pack", lambda: pack)
    monkeypatch.setattr(h, "mc_precondition", lambda p: [])
    monkeypatch.setattr(h, "MECHANISM_CONTENT_CAMPAIGN_AUTHORIZED", True)
    monkeypatch.setattr(h, "MECHANISM_CAMPAIGN_EVIDENCE_PATH", str(evidence))


def test_a_campaign_needs_a_new_journal_and_never_restarts(spec, monkeypatch, tmp_path):
    pack = _mini_pack(spec)
    _authorized_pack(monkeypatch, pack, tmp_path / "evidence.json")
    monkeypatch.setattr(h, "OpenAIMsnlAdapter", None)    # building one would fail
    out = h.mechanism_content("openai", True, True, None)
    assert out["provider_requests"] == 0 and "journal path is required" in out["refused"]
    existing = tmp_path / "journal.jsonl"
    existing.write_text("{}\n", encoding="utf-8")
    out = h.mechanism_content("openai", True, True, str(existing))
    assert out["provider_requests"] == 0 and "already started" in out["refused"]
    (tmp_path / "evidence.json").write_text("{}", encoding="utf-8")
    out = h.mechanism_content("openai", True, True, str(tmp_path / "new.jsonl"))
    assert out["provider_requests"] == 0 and "evidence already exists" in out["refused"]
    assert not (tmp_path / "new.jsonl").exists()


def test_one_authorized_campaign_runs_end_to_end_through_the_cli_path(spec, monkeypatch,
                                                                     tmp_path):
    pack = _mini_pack(spec)
    _authorized_pack(monkeypatch, pack, tmp_path / "evidence.json")
    fake = Fake(pack)
    real = h.OpenAIMsnlAdapter
    monkeypatch.setattr(h, "OpenAIMsnlAdapter",
                        lambda allow_network: real(allow_network=allow_network,
                                                   transport=fake))
    journal = tmp_path / "journal.jsonl"
    out = h.mechanism_content("openai", True, True, str(journal))
    assert out["provider_requests"] == len(fake.bodies) == 3 * len(pack["cases"])
    assert out["result"]["verdict"] == "PASS"
    assert out["spend"]["requests_sent"] == 3 * len(pack["cases"])
    events = [json.loads(l)["event"] for l in journal.read_text().splitlines()]
    assert events[0] == "start" and events[-1] == "end"
    # a second invocation with the same journal sends nothing
    again = h.mechanism_content("openai", True, True, str(journal))
    assert again["provider_requests"] == 0 and len(fake.bodies) == 3 * len(pack["cases"])
    assert h.main(["--mechanism-content", "--provider", "openai"]) == 2
