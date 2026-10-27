"""T2-G / R2 — the ONE bounded synthetic provider preflight: network-free tests
for the `--mechanism-preflight` path of `scripts/run_msnl_eval.py` and the
pinned `tests/fixtures/msnl_mechanism_preflight_v1.json`.

Every provider path here uses an injected fake transport; hosted CI never
reaches the network. The tests pin isolation from the holdout, budget
reservation, sanitized metadata, the stop rules and the refusal paths. They
measure nothing about any model and authorize nothing.
"""
import copy
import json
import re

import pytest

from engine import technical_orchestration_openai as toa
from tests.test_msnl_llm_eval_harness import h

GOOD = {"responsive": "RESPONSIVE", "stance": "ASSERTS",
        "mechanism_content": "PRESENT", "quote": "a sentence"}
SECRET = "sk-THIS-MUST-NEVER-APPEAR"


def _body(status="completed", reply=GOOD, usage=None, reason=None, rid="resp_test1",
          refusal=False, extra_text="hidden reasoning words"):
    content = ([{"type": "refusal", "refusal": "no"}] if refusal
               else [{"type": "output_text", "text": json.dumps(reply)}])
    body = {"id": rid, "status": status,
            "output": [{"type": "reasoning", "summary": [{"text": extra_text}]},
                       {"type": "message", "content": content}],
            "usage": usage if usage is not None else {
                "input_tokens": 900, "input_tokens_details": {"cached_tokens": 0},
                "output_tokens": 120, "output_tokens_details": {"reasoning_tokens": 64},
                "total_tokens": 1020}}
    if reason:
        body["incomplete_details"] = {"reason": reason}
    return 200, json.dumps(body).encode("utf-8")


class Fake:
    """Returns the queued replies in order; records each request body."""

    def __init__(self, *replies):
        self.replies, self.bodies = list(replies), []

    def __call__(self, url, headers, body, timeout):
        assert url == toa.ENDPOINT and "Authorization" not in headers
        self.bodies.append(json.loads(body.decode("utf-8")))
        reply = self.replies.pop(0)
        if isinstance(reply, Exception):
            raise reply
        return reply


@pytest.fixture(scope="module")
def arm():
    return h._mechanism_pack()


@pytest.fixture(scope="module")
def pre():
    return h._preflight_pack()


def _run(arm, pre, *replies, budget=None):
    pack = copy.deepcopy(pre)
    if budget is not None:
        pack["limits"]["budget_usd"] = budget
    fake = Fake(*replies)
    adapter = h.OpenAIMsnlAdapter(allow_network=True, transport=fake)
    rows, summary = h.mechanism_preflight(adapter, arm, pack)
    return rows, summary, fake


# ─── the pinned preflight fixture ────────────────────────────────────────────

def _shingles(text, n=8):
    words = re.findall(r"\w+", text.lower())
    return {" ".join(words[i:i + n]) for i in range(len(words) - n + 1)}


def test_the_fixture_is_pinned_separate_from_the_holdout_and_predeclared(arm, pre):
    assert pre["pack_id"] == "msnl-mechanism-preflight-v1" and pre["status"] == "SYNTHETIC"
    assert pre["arm_source"]["pack_sha256"] == h.MECHANISM_PACK_SHA256
    assert [i["variety"] for i in pre["inputs"]] == ["en", "en", "ar-msa", "ar-gulf-kw"]
    assert pre["configurations"] == [300, 4096]
    ids = [i["input_id"] for i in pre["inputs"]]
    assert pre["order"] == [[i, cap] for cap in (300, 4096) for i in ids]
    assert pre["limits"] == {"max_generation_requests": 8, "budget_usd": 5.0}
    holdout = arm["cases"]
    runs = set().union(*(_shingles(c["text"]) for c in holdout))
    for item in pre["inputs"]:
        assert item["text"] not in {c["text"] for c in holdout}
        assert not (_shingles(item["text"]) & runs), item["input_id"]


def test_a_preflight_input_equal_to_a_holdout_case_is_refused(arm, monkeypatch, pre):
    bad = copy.deepcopy(pre)
    bad["inputs"][0]["text"] = arm["cases"][0]["text"]
    monkeypatch.setattr(h, "_load", lambda path, sha: bad if "preflight" in path
                        else arm)
    with pytest.raises(h.PackError):
        h._preflight_pack()


# ─── requests: fixed settings, only the cap varies, no holdout text ──────────

def test_requests_follow_the_order_and_vary_only_the_output_cap(arm, pre):
    rows, summary, fake = _run(arm, pre, *[_body() for _ in range(8)])
    assert summary["requests_attempted"] == summary["requests_sent"] == 8 == len(fake.bodies)
    assert summary["requests_completed_valid"] == 8 and summary["stopped"] is None
    by_id = {i["input_id"]: i for i in pre["inputs"]}
    holdout_texts = {c["text"] for c in arm["cases"]}
    for body, (input_id, cap) in zip(fake.bodies, pre["order"]):
        expected = h.mechanism_payload(arm, by_id[input_id])
        assert body["max_output_tokens"] == cap
        assert {k: v for k, v in body.items() if k != "max_output_tokens"} == \
            {k: v for k, v in expected.items() if k != "max_output_tokens"}
        assert body["instructions"] == arm["arm"]["instructions"]
        assert json.loads(body["input"])["answer"] == by_id[input_id]["text"]
        assert body["store"] is False and "reasoning" not in body
        assert not any(text in body["input"] for text in holdout_texts)


def test_the_report_keeps_metadata_only_never_reply_or_reasoning_text(arm, pre):
    reply = dict(GOOD, quote="UNIQUE-REPLY-QUOTE")
    rows, summary, _ = _run(arm, pre, *[_body(reply=reply) for _ in range(8)])
    dumped = json.dumps([rows, summary])
    assert "UNIQUE-REPLY-QUOTE" not in dumped and "hidden reasoning words" not in dumped
    assert "instructions" not in dumped
    row = rows[0]
    assert row["response_id"] == "resp_test1" and row["http_status"] == 200
    assert row["usage"] == {"input_tokens": 900, "cached_input_tokens": 0,
                            "output_tokens": 120, "reasoning_tokens": 64,
                            "total_tokens": 1020}
    assert isinstance(row["latency_ms"], int)


def test_cost_counts_reasoning_inside_output_once(arm, pre):
    rows, summary, _ = _run(arm, pre, *[_body() for _ in range(8)])
    price = pre["pricing"]
    one = (900 * price["input_usd_per_1m"] + 120 * price["output_usd_per_1m"]) / 1e6
    assert rows[0]["measured_cost_usd"] == round(one, 6)
    assert summary["measured_cost_usd"] == round(8 * one, 6)
    bound = (900 * 12.0 + 120 * 60.0) / 1e6
    assert rows[0]["bound_usd"] == round(bound, 6)
    assert summary["measured_cost_complete"] is True


# ─── the stop rules ──────────────────────────────────────────────────────────

def test_an_output_cap_incomplete_is_measured_and_the_run_continues(arm, pre):
    capped = _body(status="incomplete", reason="max_output_tokens",
                   usage={"input_tokens": 900, "output_tokens": 300,
                          "output_tokens_details": {"reasoning_tokens": 300}})
    rows, summary, fake = _run(arm, pre, *([capped] * 4 + [_body()] * 4))
    assert len(fake.bodies) == 8 and summary["stopped"] is None
    assert summary["by_max_output_tokens"] == {
        "300": {"attempted": 4, "completed_valid": 0, "incomplete_output_cap": 4},
        "4096": {"attempted": 4, "completed_valid": 4, "incomplete_output_cap": 0}}
    assert rows[0]["outcome"] == h.PF_CAPPED and rows[0]["schema_valid"] is False


@pytest.mark.parametrize("reply,outcome", [
    (OSError("boom"), "TRANSPORT"),
    ((401, json.dumps({"error": {"type": "invalid_request_error",
                                 "code": "invalid_api_key",
                                 "message": "bad key " + SECRET}}).encode()), "HTTP_STATUS"),
    ((404, b"not json " + SECRET.encode()), "HTTP_STATUS"),
    (_body(refusal=True), "REFUSAL"),
    (_body(status="incomplete", reason="content_filter"), "INCOMPLETE_OTHER"),
    (_body(reply={"responsive": "RESPONSIVE"}), "SCHEMA_INVALID"),
    (_body(reply=dict(GOOD, stance="HEDGES")), "SCHEMA_INVALID"),
    (_body(usage={"input_tokens": 900, "output_tokens": 301}), "COST_UNBOUNDED"),
])
def test_every_other_failure_stops_at_once_without_retry(arm, pre, reply, outcome):
    rows, summary, fake = _run(arm, pre, reply, *[_body() for _ in range(7)])
    assert len(fake.bodies) == 1 and len(rows) == 1
    assert summary["stopped"] == outcome == rows[0]["outcome"]
    assert SECRET not in json.dumps([rows, summary])


def test_a_non_200_keeps_only_its_status_and_sanitized_error_identifiers(arm, pre):
    reply = (401, json.dumps({"error": {"type": "invalid_request_error",
                                        "code": "invalid_api_key",
                                        "message": "bad key " + SECRET}}).encode())
    rows, _, _ = _run(arm, pre, reply)
    assert (rows[0]["http_status"], rows[0]["error_type"], rows[0]["error_code"]) == \
        (401, "invalid_request_error", "invalid_api_key")
    assert rows[0]["bound_usd"] == rows[0]["reserved_usd"]      # treated conservatively
    assert rows[0]["measured_cost_usd"] == "UNAVAILABLE"


def test_metadata_is_never_free_text():
    raw = json.dumps({"id": "resp with spaces", "status": "x" * 200,
                      "incomplete_details": {"reason": "a b"},
                      "usage": {"input_tokens": True, "output_tokens": -1,
                                "total_tokens": "10"}}).encode()
    meta = h.preflight_response_meta(raw)
    assert meta["response_id"] == meta["response_status"] == \
        meta["incomplete_reason"] == "UNAVAILABLE"
    assert set(meta["usage"].values()) == {"UNAVAILABLE"}
    assert h.preflight_response_meta(b"\xff")["usage"]["input_tokens"] == "UNAVAILABLE"


# ─── budget enforcement ──────────────────────────────────────────────────────

def test_a_request_is_never_sent_when_its_reservation_would_exceed_the_budget(arm, pre):
    plan = h.mechanism_preflight_run("lexical", False, False)["plan"]
    first_four = sum(p["reserved_usd"] for p in plan[:4])
    rows, summary, fake = _run(arm, pre, *[_body() for _ in range(8)],
                               budget=first_four + 0.01)
    # usage-based bounds are below the reservations, so more fits, but never
    # a request whose own reservation does not fit
    assert summary["stopped"] == "BUDGET_RESERVATION"
    assert len(fake.bodies) == len(rows) < 8
    assert summary["conservative_bound_usd"] <= first_four + 0.01


def test_unknown_usage_is_charged_its_whole_reservation(arm, pre):
    rows, summary, _ = _run(arm, pre, *[_body(usage={}) for _ in range(8)])
    assert all(r["bound_usd"] == r["reserved_usd"] for r in rows)
    assert summary["measured_cost_complete"] is False
    assert summary["conservative_bound_usd"] == pytest.approx(
        sum(r["reserved_usd"] for r in rows), abs=1e-5)
    assert summary["conservative_bound_usd"] <= pre["limits"]["budget_usd"]


def test_the_whole_plan_fits_the_budget_at_its_conservative_reservation():
    out = h.mechanism_preflight_run("lexical", False, False)
    assert out["provider_requests"] == 0 and len(out["plan"]) == 8
    assert sum(p["reserved_usd"] for p in out["plan"]) < out["limits"]["budget_usd"]
    assert out["campaign_authorized"] is False


# ─── refusal and isolation ───────────────────────────────────────────────────

def test_the_preflight_never_sends_without_authorization_or_flags(monkeypatch):
    monkeypatch.setattr(h, "OpenAIMsnlAdapter", None)    # building one would fail
    monkeypatch.setattr(h, "MECHANISM_PREFLIGHT_AUTHORIZED", False)
    out = h.mechanism_preflight_run("openai", True, True)
    assert out["provider_requests"] == 0 and "refused" in out
    assert h.main(["--mechanism-preflight", "--provider", "openai"]) == 2
    assert h.main(["--mechanism-preflight", "--mechanism-content"]) == 2


def test_the_campaign_stays_refused():
    assert h.MECHANISM_CONTENT_CAMPAIGN_AUTHORIZED is False
    out = h.mechanism_content("openai", True, True)
    assert out["provider_requests"] == 0 and "refused" in out


def test_the_default_adapter_reaches_no_network(arm, pre):
    fake = Fake()
    adapter = h.OpenAIMsnlAdapter(transport=fake)        # allow_network defaults off
    rows, summary = h.mechanism_preflight(adapter, arm, copy.deepcopy(pre))
    assert fake.bodies == [] and summary["stopped"] == "NOT_SENT"
    assert summary["requests_sent"] == 0 and rows[0]["bound_usd"] == 0.0
    assert rows[0]["http_status"] == "UNAVAILABLE"


def test_the_preflight_has_no_product_or_store_side_effect(tmp_path):
    """In a fresh interpreter, a whole fake-transport preflight imports no web
    layer, opens no SQLite connection and creates no database file."""
    import os
    import pathlib
    import subprocess
    import sys
    root = pathlib.Path(__file__).resolve().parents[1]
    db = tmp_path / "must-not-exist.sqlite"
    code = (
        "import importlib.util, json, sqlite3, sys\n"
        "def boom(*a, **k): raise SystemExit('side effect')\n"
        "sqlite3.connect = boom\n"
        "spec = importlib.util.spec_from_file_location('h', %r)\n"
        "h = importlib.util.module_from_spec(spec); spec.loader.exec_module(h)\n"
        "body = json.dumps({'id': 'resp_x', 'status': 'completed', 'output': [{'type': "
        "'message', 'content': [{'type': 'output_text', 'text': json.dumps({'responsive': "
        "'RESPONSIVE', 'stance': 'ASSERTS', 'mechanism_content': 'ABSENT', 'quote': ''})}]}],"
        " 'usage': {'input_tokens': 10, 'output_tokens': 5}}).encode()\n"
        "fake = lambda url, headers, data, timeout: (200, body)\n"
        "a = h.OpenAIMsnlAdapter(allow_network=True, transport=fake)\n"
        "rows, summary = h.mechanism_preflight(a, h._mechanism_pack(), h._preflight_pack())\n"
        "assert summary['requests_completed_valid'] == 8, summary\n"
        "print(sorted(m for m in ('web', 'web.app') if m in sys.modules))\n"
    ) % str(root / "scripts" / "run_msnl_eval.py")
    env = dict(os.environ, INVENTORAI_DB_PATH=str(db))
    out = subprocess.run([sys.executable, "-c", code], cwd=root, env=env,
                         capture_output=True, text=True, timeout=300)
    assert out.returncode == 0, out.stderr
    assert out.stdout.strip() == "[]"
    assert not db.exists()
