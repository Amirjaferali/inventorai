"""Campaign 02 guarded runner — network-free guards.

Every transport is a local fake. Replies are HANDCRAFTED from the reference
to exercise the runner and decision rule; they are not model results.
"""
import io
import json
from pathlib import Path

import pytest

from engine import technical_orchestration_openai as toa
from scripts import g1_precreation_heldout_v2_preregistration as ho
from scripts import g1_precreation_semantic_v2_candidate as v2c
from scripts import run_g1_precreation_campaign as c01
from scripts import run_g1_precreation_campaign_02 as c02
from scripts import run_g1_precreation_semantic_eval as ev
from tests.test_g1_precreation_campaign import _Fake, _NotFake, _adapter, _body
from tests.test_g1_precreation_heldout_v2_preregistration import _full
from tests.test_g1_precreation_semantic_eval import _oracle

ROOT = Path(__file__).resolve().parent.parent
REVISION = "0" * 40


@pytest.fixture(scope="module")
def pack():
    return ho.load_heldout()


@pytest.fixture
def evidence(tmp_path, monkeypatch):
    d = tmp_path / "evidence02"
    monkeypatch.setattr(c02, "EVIDENCE_DIR", str(d))
    monkeypatch.setattr(c02, "JOURNAL_PATH", str(d / "campaign_02_journal.jsonl"))
    monkeypatch.setattr(c02, "REPORT_PATH", str(d / "campaign_02_report.json"))
    monkeypatch.setattr(c02, "_evidence_in_history", lambda: False)
    return d


def _responses(pack):
    cases, refs = pack
    return [_body(_oracle(c, refs[c["case_id"]])) for c in cases]


def _run(pack, responses):
    fake, journal = _Fake(responses), io.StringIO()
    adapter = _adapter(fake)
    report = c02.campaign(adapter, pack[0], c02.run_manifest(REVISION, adapter._model), journal)
    return report, fake, journal.getvalue().splitlines()


def _bound(report, scored, refs, **k4):
    return dict(_full(scored, refs, **k4), report_sha256=c02._digest(report))


# ── Identity and limits ─────────────────────────────────────────────────────
def test_campaign_02_limits_and_distinct_identity():
    assert (c02.MAX_PROVIDER_REQUESTS, c02.RETRIES, c02.MAX_OUTPUT_TOKENS,
            c02.CAMPAIGN_CEILING_USD) == (24, 0, 1200, 5.0)
    assert c02.AUTHORIZED_RUN_MANIFEST_SHA256 is None
    assert c02.EVIDENCE_DIR != c01.EVIDENCE_DIR
    assert c02.JOURNAL_PATH.endswith("g1_precreation_semantic_heldout_v2/campaign_02_journal.jsonl")
    assert c02.REPORT_PATH.endswith("g1_precreation_semantic_heldout_v2/campaign_02_report.json")


def test_campaign_01_runner_and_evidence_are_untouched():
    assert c01.MAX_PROVIDER_REQUESTS == 20 and c01.EVIDENCE_DIR.endswith("g1_precreation_semantic_v1")
    for name in ("campaign_01_journal.jsonl", "campaign_01_report.json"):
        assert (Path(c01.EVIDENCE_DIR) / name).exists()
    assert ev.preregistration_digest() == (
        "aae4a9af41d84616409badfcc77b9a313bae40dcc0919b69851de6b231285e1f")


def test_frozen_prompt_pack_and_preregistration_identities():
    assert ho.INPUT_SHA256 == "db4b88f007d26bc02e0da49bfa06e3ae481c41ab749de0d13db4ae594dda059d"
    assert ho.REFERENCE_SHA256 == "9803322931c2dc4f6e990c4b368b73a521a1b5dae3e628babf07d5500a99fa08"
    assert ho.preregistration_digest() == (
        "b1a7c2c35f38f074c3343b97fd4be9f0d2dd5d98c741de86d27e02e3309e06d1")
    m = c02.run_manifest(REVISION, c02.MODEL)
    assert m["candidate_instructions_sha256"] == c02._sha(v2c.candidate_instructions())


# ── Requests: the v2 prompt, the idea text, nothing else ────────────────────
def test_payload_is_the_v2_candidate_with_only_the_idea_text(pack):
    cases, refs = pack
    for case in cases:
        body = c02.payload(case)
        assert set(body) == {"model", "instructions", "input", "store", "max_output_tokens", "text"}
        assert body["instructions"] == v2c.candidate_instructions()
        assert body["instructions"] != ev._instructions(ev.governed_concepts())
        assert body["text"]["format"]["schema"] == ev._schema(ev.governed_concepts())
        assert body["store"] is False and "tools" not in body and body["max_output_tokens"] == 1200
        assert json.loads(body["input"]) == {"idea_text": case["idea_text"]}
        # Everything except the idea text itself: no id, label or annotation of ANY case.
        flat = json.dumps({k: v for k, v in body.items() if k != "input"})
        assert case["case_id"] not in json.dumps(body)
        for r in refs.values():
            assert r["category"] not in flat
            for u in r["expected_unknowns"]:
                assert u["meaning"] not in flat


def test_manifest_binds_the_whole_campaign(pack):
    m = c02.run_manifest(REVISION, c02.MODEL)
    assert (m["campaign_id"], m["pack_id"], m["input_sha256"], m["reference_sha256"],
            m["preregistration_sha256"]) == (
        "g1-precreation-campaign-02", ho.PACK_ID, ho.INPUT_SHA256, ho.REFERENCE_SHA256,
        ho.preregistration_digest())
    assert m["payloads_sha256"] == c02._digest([c02.payload(c) for c in pack[0]])
    assert (m["model"], m["endpoint"], m["max_provider_requests"], m["retries"],
            m["max_output_tokens"], m["store"], m["tools"]) == (
        "gpt-6-sol", toa.ENDPOINT, 24, 0, 1200, False, "none")
    assert m["budget"]["price_verification"] == c01.PRICE_VERIFICATION
    assert m["not_campaign_01"]["campaign_01_evidence"].endswith("g1_precreation_semantic_v1")


def test_a_changed_prompt_or_pack_changes_or_refuses_the_manifest(monkeypatch):
    base = c02._digest(c02.run_manifest(REVISION, c02.MODEL))
    monkeypatch.setattr(v2c, "CANDIDATE_COMPOSITION_RULE", v2c.CANDIDATE_COMPOSITION_RULE + " x")
    assert c02._digest(c02.run_manifest(REVISION, c02.MODEL)) != base
    monkeypatch.undo()
    monkeypatch.setattr(ho, "REFERENCE_SHA256", "0" * 64)
    with pytest.raises(c02.PackError):
        c02.run_manifest(REVISION, c02.MODEL)


def test_budget_reserves_every_request_within_the_ceiling(pack):
    plan = c02.budget_plan(pack[0])
    assert plan["requests"] == 24 and plan["within_ceiling"] is True
    assert plan["all_reservations_usd"] <= 5.0


# ── Authorization: fails closed before any provider interaction ─────────────
@pytest.mark.parametrize("digest", [None, "f" * 64, "not-a-digest"])
def test_cli_refuses_before_any_adapter_or_transport(digest, monkeypatch, evidence, capsys):
    def boom(*a, **k):
        raise AssertionError("an adapter or transport was built")
    monkeypatch.setattr(c02, "OpenAIMsnlAdapter", boom)
    monkeypatch.setattr(toa, "_urllib_transport", boom)
    monkeypatch.setattr(c02, "current_revision", lambda: REVISION)
    argv = ["--provider", "openai", "--allow-network", "--managed-credential"]
    if digest is not None:
        argv += ["--authorized-manifest", digest]
    assert c02.main(argv) == 2 and "not authorized" in capsys.readouterr().out
    assert not evidence.exists()


def test_real_transport_without_the_digest_sends_nothing(pack, evidence):
    transport = _NotFake(_responses(pack))
    adapter = _adapter(transport)
    with pytest.raises(c02.PackError, match="not authorized"):
        c02.campaign(adapter, pack[0], c02.run_manifest(REVISION, adapter._model), None, None)
    assert transport.calls == [] and not evidence.exists()


@pytest.mark.parametrize("breach", [
    "wrong_digest", "price_unverified", "other_revision", "evidence_in_tree",
    "evidence_in_history", "caller_journal", "wrong_model", "extra_case",
])
def test_boundary_refuses_each_breach(breach, pack, evidence, monkeypatch):
    monkeypatch.setattr(c02, "current_revision", lambda: REVISION)
    cases = list(pack[0])
    manifest = c02.run_manifest(REVISION, c02.MODEL)
    digest, journal = c02._digest(manifest), None
    if breach == "wrong_digest":
        digest = "e" * 64
    elif breach == "price_unverified":
        monkeypatch.setattr(c01, "PRICE_VERIFICATION", None)
    elif breach == "other_revision":
        monkeypatch.setattr(c02, "current_revision", lambda: "1" * 40)
    elif breach == "evidence_in_tree":
        evidence.mkdir()
        Path(c02.JOURNAL_PATH).write_text("")
    elif breach == "evidence_in_history":
        monkeypatch.setattr(c02, "_evidence_in_history", lambda: True)
    elif breach == "caller_journal":
        journal = object()
    elif breach == "wrong_model":
        manifest = c02.run_manifest(REVISION, "gpt-other")
        digest = c02._digest(manifest)
    elif breach == "extra_case":
        cases = cases + [cases[0]]
    with pytest.raises(c02.PackError):
        c02.check_campaign_boundary(cases, manifest, digest, journal)


def test_the_exact_digest_passes_every_boundary(pack, evidence, monkeypatch):
    monkeypatch.setattr(c02, "current_revision", lambda: REVISION)
    manifest = c02.run_manifest(REVISION, c02.MODEL)
    c02.check_campaign_boundary(list(pack[0]), manifest, c02._digest(manifest))


# ── One run, interruption, provider failures ───────────────────────────────
def test_interrupted_run_keeps_its_journal_and_cannot_restart(pack, evidence, monkeypatch):
    monkeypatch.setattr(c02, "current_revision", lambda: REVISION)
    responses = _responses(pack)
    responses[5] = KeyboardInterrupt()
    adapter = _adapter(_NotFake(responses))
    manifest = c02.run_manifest(REVISION, adapter._model)
    with pytest.raises(KeyboardInterrupt):
        c02.campaign(adapter, pack[0], manifest, None, c02._digest(manifest))
    lines = [json.loads(x) for x in Path(c02.JOURNAL_PATH).read_text().splitlines()]
    assert [x["event"] for x in lines].count("reserved") == 6
    again = _adapter(_NotFake(_responses(pack)))
    with pytest.raises(c02.PackError, match="one run only"):
        c02.campaign(again, pack[0], manifest, None, c02._digest(manifest))


@pytest.mark.parametrize("index", [3, 23])
def test_provider_error_anywhere_is_incomplete_never_a_verdict(index, pack):
    _cases, refs = pack
    responses = _responses(pack)
    responses[index] = (500, b"{}")
    report, _fake, lines = _run(pack, responses)
    scored, _ = c02.score_report(report)
    agg = c02.aggregate(report, _bound(report, scored, refs), report["manifest_sha256"], lines)
    assert agg["verdict"] == "INCOMPLETE"


def test_refusal_without_a_reply_is_incomplete_not_credited(pack):
    _cases, refs = pack
    responses = _responses(pack)
    responses[0] = _body(None, refusal=True)
    report, fake, lines = _run(pack, responses)
    assert len(fake.calls) == 24 and report["rows"][0]["provider_status"] == c02.P_REFUSAL
    scored, _ = c02.score_report(report)
    agg = c02.aggregate(report, _bound(report, scored, refs), report["manifest_sha256"], lines)
    assert agg["verdict"] == "INCOMPLETE"


def test_cost_ceiling_stops_before_send(pack, monkeypatch):
    monkeypatch.setattr(c02, "CAMPAIGN_CEILING_USD", 0.2)
    report, fake, _lines = _run(pack, _responses(pack))
    assert 1 <= len(fake.calls) < 24 and report["stopped_on"] == c02.ERR_COST_CEILING
    assert report["spend"]["conservative_bound_usd"] <= 0.2


# ── After the run: no GO without every human review ─────────────────────────
def test_reference_reader_run_needs_every_bound_review(pack):
    _cases, refs = pack
    report, fake, lines = _run(pack, _responses(pack))
    assert len(fake.calls) == 24 and report["requests"] == 24
    digest = report["manifest_sha256"]
    assert c02.aggregate(report, None, digest, lines)["verdict"] == "INCOMPLETE_REVIEW"
    items = c02.review_items(report, digest, lines)
    assert items["report_sha256"] == c02._digest(report) and items["k4_context"]
    scored, _ = c02.score_report(report)
    full = _bound(report, scored, refs)
    assert c02.aggregate(report, full, digest, lines)["verdict"] == "PRELIMINARY_GO"
    unbound = {k: v for k, v in full.items() if k != "report_sha256"}
    with pytest.raises(c02.PackError, match="not bound"):
        c02.aggregate(report, unbound, digest, lines)


def test_forged_rows_or_a_foreign_report_are_refused(pack):
    cases, refs = pack
    responses = _responses(pack)
    responses[4] = (500, b"{}")
    report, _fake, lines = _run(pack, responses)
    forged = json.loads(json.dumps(report))
    for case, row in zip(cases[4:], forged["rows"][4:]):
        row.update(provider_status=c02.P_RESPONDED, error_kind=None,
                   reply=_oracle(case, refs[case["case_id"]]),
                   attempt=dict(forged["rows"][0]["attempt"]))
    forged["stopped_on"], forged["requests"] = None, 24
    with pytest.raises(c02.PackError, match="journal"):
        c02.aggregate(forged, None, report["manifest_sha256"], lines)
    with pytest.raises(c02.PackError):
        c02.aggregate(report, None, "f" * 64, lines)


# ── Boundaries ──────────────────────────────────────────────────────────────
def test_offline_plan_sends_nothing_and_no_product_import(monkeypatch, capsys):
    monkeypatch.setattr(toa, "_urllib_transport",
                        lambda *a, **k: (_ for _ in ()).throw(AssertionError("network")))
    assert c02.main([]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["cases"] == 24 and out["budget"]["within_ceiling"] is True
    for folder in ("engine", "web"):
        for path in (ROOT / folder).rglob("*.py"):
            assert "run_g1_precreation_campaign_02" not in path.read_text(encoding="utf-8")
