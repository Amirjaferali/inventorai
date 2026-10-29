"""FIRST-G1-PROOF-B — offline guards for the free-form idea-clarification pilot harness.

Synthetic data only; no network. A fake transport exercises the evaluation
mechanics. Nothing here is evidence of model quality or of real
prompt-injection resistance.
"""
import copy
import hashlib
import importlib.util
import io
import json
import pathlib

import pytest

from engine import technical_orchestration_openai as toa

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "run_proof_b_eval.py"
# Pinned: changing the instructions, schema, limits or decision rule changes the
# pre-registration and must be a deliberate, reviewed edit.
PREREGISTRATION_SHA256 = "490c730115c31a77e5025eef8acb52f027f6bfb964b4a9469ba20fee661389d5"


@pytest.fixture(scope="module")
def pb():
    spec = importlib.util.spec_from_file_location("run_proof_b_eval", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def pilot(pb):
    return pb.load_pilot()


def _reply(**over):
    reply = {"outcome": "RESPONDED",
             "inventor_stated": [{"text": "Keep potted plants from drying while away.",
                                  "source_quote": "keeps my potted plants from drying out"}],
             "ai_suggestions": [{"text": "A wicking reservoir could be explored.",
                                 "attribution": "AI_PROPOSED", "status": "UNVERIFIED"}],
             "clarification_questions": ["How long are you usually away?"],
             "unresolved_or_abstain": ["How it should work is not yet decided."]}
    reply.update(over)
    return reply


def _body(text, refusal=False, status="completed"):
    part = {"type": "refusal", "refusal": "no"} if refusal else {"type": "output_text", "text": text}
    return json.dumps({"status": status, "output": [{"type": "message", "content": [part]}]}).encode()


class _Transport:
    def __init__(self, responses):
        self.responses, self.calls = list(responses), []

    def __call__(self, url, headers, body, timeout):
        self.calls.append(json.loads(body.decode("utf-8")))
        item = self.responses.pop(0)
        if isinstance(item, Exception):
            raise item
        return item


def _adapter(pb, responses):
    transport = _Transport(responses)
    return pb.OpenAIMsnlAdapter(allow_network=True, transport=transport), transport


# ── fixture ─────────────────────────────────────────────────────────────────
def test_fixture_is_pinned_and_forms_the_4x8_matrix(pb, pilot):
    cases, refs = pilot
    assert hashlib.sha256(pathlib.Path(pb.INPUT_PATH).read_bytes()).hexdigest() == pb.INPUT_SHA256
    assert hashlib.sha256(pathlib.Path(pb.REFERENCE_PATH).read_bytes()).hexdigest() == pb.REFERENCE_SHA256
    assert len(cases) == 32 and len({c["case_id"] for c in cases}) == 32
    for lang in pb.LANGUAGES:
        assert sum(c["language"] == lang for c in cases) == 8
    assert set(refs) == {c["case_id"] for c in cases}
    assert json.loads(pathlib.Path(pb.INPUT_PATH).read_text(encoding="utf-8"))["status"] \
        == "DRAFT_NOT_INDEPENDENTLY_VALIDATED"


def test_a_tampered_fixture_is_refused(pb, tmp_path, monkeypatch):
    data = json.loads(pathlib.Path(pb.INPUT_PATH).read_text(encoding="utf-8"))
    data["cases"][0]["idea_text"] += " "
    bad = tmp_path / "inputs.json"
    bad.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    monkeypatch.setattr(pb, "INPUT_PATH", str(bad))
    with pytest.raises(pb.PackError):
        pb.load_pilot()


def test_pilot_texts_are_disjoint_from_every_earlier_fixture(pilot):
    cases, _refs = pilot
    own = {"proof_b_pilot_inputs_draft_v1.json", "proof_b_pilot_reference_draft_v1.json"}
    for path in (ROOT / "tests" / "fixtures").glob("*.json"):
        if path.name in own:
            continue
        text = path.read_text(encoding="utf-8")
        assert not any(c["idea_text"] in text for c in cases), path.name


# ── payload: input only, labels never sent ─────────────────────────────────
def test_payload_sends_only_the_idea_text(pb, pilot):
    cases, refs = pilot
    for case in cases:
        body = pb.payload(case)
        assert set(body) == {"model", "instructions", "input", "store", "max_output_tokens", "text"}
        assert body["store"] is False and body["text"]["format"]["strict"] is True
        assert json.loads(body["input"]) == {"idea_text": case["idea_text"]}
    assert pb.label_leaks(cases, refs) == []


def test_leak_check_catches_a_payload_that_carries_labels(pb, pilot):
    cases, refs = pilot

    def leaky(case):
        body = pb.payload(case)
        body["input"] = json.dumps({"idea_text": case["idea_text"],
                                    "hint": refs[case["case_id"]]["stated_intent"]})
        return body

    def tagged(case):
        body = pb.payload(case)
        body["instructions"] += " " + case["case_id"]
        return body
    assert pb.label_leaks(cases, refs, build=leaky)
    assert {k for _c, k in pb.label_leaks(cases, refs, build=tagged)} == {"case_id"}


def test_preregistration_is_pinned(pb):
    assert pb.preregistration_digest() == PREREGISTRATION_SHA256
    schema = pb.PREREGISTRATION["schema"]
    assert set(schema["required"]) == {"outcome", "inventor_stated", "ai_suggestions",
                                       "clarification_questions", "unresolved_or_abstain"}
    assert pb.PREREGISTRATION["limits"]["retries"] == 0
    assert pb.PREREGISTRATION["limits"]["max_provider_requests"] == 32


# ── parsing keeps the four outputs apart and refuses bad structure ─────────
def test_a_valid_reply_is_kept_in_four_separate_parts(pb):
    status, parts = pb.parse_reply(_reply())
    assert status == pb.ST_OK
    assert parts["inventor_stated"][0]["source_quote"] == "keeps my potted plants from drying out"
    assert parts["ai_suggestions"][0]["attribution"] == "AI_PROPOSED"
    assert parts["ai_suggestions"][0]["status"] == "UNVERIFIED"
    assert parts["clarification_questions"] == ["How long are you usually away?"]


@pytest.mark.parametrize("bad", [
    {"extra": 1},
    {"ai_suggestions": [{"text": "x y", "attribution": "INVENTOR", "status": "UNVERIFIED"}]},
    {"ai_suggestions": [{"text": "x y", "attribution": "AI_PROPOSED", "status": "VERIFIED"}]},
    {"ai_suggestions": [{"text": "a b", "attribution": "AI_PROPOSED", "status": "UNVERIFIED"}] * 3},
    {"clarification_questions": ["q?", "q?", "q?"]},
    {"inventor_stated": [{"text": "", "source_quote": "plants"}]},
    {"inventor_stated": [{"text": "x", "source_quote": "y" * 401}]},
    {"outcome": "ABSTAIN"},
    {"outcome": "MAYBE"},
    {"unresolved_or_abstain": "not a list"},
])
def test_bad_structure_is_a_structure_violation(pb, bad):
    reply = _reply()
    if "extra" in bad:
        reply["extra"] = 1
    else:
        reply.update(bad)
    assert pb.parse_reply(reply) == (pb.ST_STRUCTURE, None)


def test_an_empty_abstain_is_a_model_abstain(pb):
    reply = {"outcome": "ABSTAIN", "inventor_stated": [], "ai_suggestions": [],
             "clarification_questions": [], "unresolved_or_abstain": []}
    assert pb.parse_reply(reply)[0] == pb.ST_MODEL_ABSTAIN


def test_flags_prompt_the_rater_but_decide_nothing(pb, pilot):
    cases, _refs = pilot
    case = next(c for c in cases if c["case_id"] == "G01-en")
    _s, parts = pb.parse_reply(_reply(
        inventor_stated=[{"text": "Wants an automatic pump.", "source_quote": "an automatic pump"}],
        unresolved_or_abstain=["This cannot be certified safe here."]))
    flags = pb.review_flags(case, parts)
    assert flags["ungrounded_stated_items"] == [0]
    assert ["unresolved_or_abstain", "certified"] in flags["authority_terms"]
    ar = next(c for c in cases if c["case_id"] == "G06-ar-msa")
    _s, parts = pb.parse_reply(_reply(inventor_stated=[
        {"text": "صندوق لفرز البراغي", "source_quote": "يساعد في فرز البراغي الصغيرة"}],
        unresolved_or_abstain=["لا يمكن القول إن التصميم معتمد."]))
    flags = pb.review_flags(ar, parts)
    assert flags["ungrounded_stated_items"] == []
    assert ["unresolved_or_abstain", "معتمد"] in flags["authority_terms"]


# ── the provider path: errors, refusals and the gate ───────────────────────
def test_network_is_off_by_default_and_sends_nothing(pb, pilot):
    cases, _refs = pilot
    transport = _Transport([])
    adapter = pb.OpenAIMsnlAdapter(transport=transport)
    row = pb.classify(adapter, cases[0])
    assert row["status"] == pb.ST_ERROR and row["error_kind"] == toa.ERR_NETWORK_NOT_ALLOWED
    assert transport.calls == []


@pytest.mark.parametrize("response,status,kind", [
    ((200, _body(json.dumps(_reply()))), "RESPONDED", None),
    ((200, _body("", refusal=True)), "PROVIDER_REFUSAL", None),
    ((500, b""), "ERROR", toa.ERR_HTTP_STATUS),
    ((302, b""), "ERROR", toa.ERR_HTTP_STATUS),
    ((200, _body("not json")), "ERROR", toa.ERR_MALFORMED),
    ((200, _body(json.dumps(_reply()), status="incomplete")), "ERROR", toa.ERR_INCOMPLETE),
    (OSError("down"), "ERROR", toa.ERR_TRANSPORT),
    ((200, _body(json.dumps({"outcome": "RESPONDED"}))), "STRUCTURE_VIOLATION", None),
])
def test_each_outcome_is_classified_separately(pb, pilot, response, status, kind):
    cases, _refs = pilot
    adapter, transport = _adapter(pb, [response])
    row = pb.classify(adapter, cases[0])
    assert (row["status"], row["error_kind"]) == (status, kind)
    assert len(transport.calls) == 1
    assert json.loads(transport.calls[0]["input"]) == {"idea_text": cases[0]["idea_text"]}


def test_campaign_makes_one_call_per_case_and_stops_on_the_first_error(pb, pilot):
    cases, _refs = pilot
    ok = (200, _body(json.dumps(_reply())))
    adapter, transport = _adapter(pb, [ok, ok, (500, b"")] + [ok] * 40)
    journal = io.StringIO()
    report = pb.campaign(adapter, cases, journal)
    assert report["requests"] == 3 and len(transport.calls) == 3
    assert report["stopped_on"] == pb.ST_ERROR
    statuses = [r["status"] for r in report["rows"]]
    assert statuses[:3] == ["RESPONDED", "RESPONDED", "ERROR"]
    assert set(statuses[3:]) == {"NOT_ATTEMPTED"} and len(statuses) == 32
    lines = [json.loads(x) for x in journal.getvalue().splitlines()]
    assert lines[0] == {"reserve": cases[0]["case_id"], "request": 1}
    assert lines[1]["attempt"] == cases[0]["case_id"]


def test_campaign_never_exceeds_the_cap_and_never_retries(pb, pilot):
    cases, _refs = pilot
    ok = (200, _body(json.dumps(_reply())))
    adapter, transport = _adapter(pb, [ok] * 64)
    report = pb.campaign(adapter, cases + cases)
    assert report["requests"] == pb.MAX_PROVIDER_REQUESTS == len(transport.calls) == 32


def test_the_campaign_gate_is_closed(pb, monkeypatch, capsys):
    assert pb.PROOF_B_CAMPAIGN_AUTHORIZED is False

    def refuse(*_a, **_k):
        raise AssertionError("no adapter may be built while the gate is closed")
    monkeypatch.setattr(pb, "OpenAIMsnlAdapter", refuse)
    monkeypatch.setattr(toa, "_urllib_transport", refuse)
    code = pb.main(["--provider", "openai", "--allow-network", "--managed-credential",
                    "--journal", "unused.jsonl"])
    assert code == 2 and "not authorized" in capsys.readouterr().out
    assert pb.main([]) == 0


# ── human review and the pre-registered decision ───────────────────────────
def _sheet(pb, pilot, verdict="PASS"):
    cases, refs = pilot
    ok = (200, _body(json.dumps(_reply())))
    adapter, _t = _adapter(pb, [ok] * 32)
    sheet = pb.review_sheet(pb.campaign(adapter, cases), cases, refs)
    for entry in sheet["cases"]:
        entry["verdicts"] = {c: verdict for c in entry["verdicts"]}
    return sheet


def test_review_sheet_shows_reference_to_the_rater_and_eligible_criteria(pb, pilot):
    cases, refs = pilot
    sheet = _sheet(pb, pilot, verdict=None)
    by = {e["case_id"]: e for e in sheet["cases"]}
    assert by["G06-en"]["reference"]["category"] == "prompt_injection"
    assert "I7" in by["G06-en"]["verdicts"] and "I5" not in by["G06-en"]["verdicts"]
    assert "I5" in by["G02-en"]["verdicts"] and "I3" in by["G02-en"]["verdicts"]
    assert "I4" in by["G08-ar-egy"]["verdicts"]
    assert all({"I1", "I6", "I8", "I9", "I2"} <= set(e["verdicts"]) for e in sheet["cases"])


def test_aggregate_follows_the_preregistered_rule(pb, pilot):
    assert pb.aggregate(_sheet(pb, pilot))["decision"] == "PILOT_GO_FOR_LARGER_STUDY"
    incomplete = _sheet(pb, pilot)
    incomplete["cases"][0]["verdicts"]["I1"] = None
    assert pb.aggregate(incomplete)["decision"] == "INCOMPLETE_REVIEW"
    one_critical = _sheet(pb, pilot)
    one_critical["cases"][5]["verdicts"]["I6"] = "FAIL"
    result = pb.aggregate(one_critical)
    assert result["decision"] == "NO_GO_UNCHANGED_APPROACH"
    assert result["critical_failures"] == [[one_critical["cases"][5]["case_id"], "I6"]]
    graded = _sheet(pb, pilot)
    i4 = [e for e in graded["cases"] if "I4" in e["verdicts"]]
    for e in i4[: len(i4) // 4]:
        e["verdicts"]["I4"] = "FAIL"          # exactly 3/4 still passes
    assert pb.aggregate(graded)["decision"] == "PILOT_GO_FOR_LARGER_STUDY"
    i4[len(i4) // 4]["verdicts"]["I4"] = "FAIL"
    assert pb.aggregate(graded)["decision"] == "NO_GO_UNCHANGED_APPROACH"
    per = pb.aggregate(_sheet(pb, pilot))["per_language"]
    assert {k: v["cases"] for k, v in per.items()} == {lang: 8 for lang in pb.LANGUAGES}


def test_aggregate_refuses_unknown_verdicts(pb, pilot):
    sheet = _sheet(pb, pilot)
    sheet["cases"][0]["verdicts"]["I1"] = "MOSTLY"
    with pytest.raises(pb.PackError):
        pb.aggregate(sheet)


# ── isolation ──────────────────────────────────────────────────────────────
def test_no_product_module_imports_the_harness_and_it_imports_no_owner(pb):
    for path in list((ROOT / "engine").glob("*.py")) + list((ROOT / "web").glob("*.py")):
        assert "run_proof_b_eval" not in path.read_text(encoding="utf-8"), path.name
    src = SCRIPT.read_text(encoding="utf-8")
    imported = {line.split()[1] for line in src.splitlines()
                if line.startswith(("from engine", "import engine", "from web", "from scripts"))}
    assert imported == {"engine", "scripts.run_msnl_eval"}
    for owner in ("idea_state", "intent_serving", "progression_loop", "record_store",
                  "technical_orchestration_shadow", "gap_relevance", "web.app"):
        assert owner not in src.replace("technical_orchestration_openai", "")
