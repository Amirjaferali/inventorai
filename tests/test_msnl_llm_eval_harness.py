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
