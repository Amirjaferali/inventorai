"""G1-PRECREATION-LLM-RUNNER-01 — network-free guards for the guarded runner.

Every transport here is a local fake; nothing reaches a network. The replies
are HANDCRAFTED test material, never evidence that a model understood anything.
"""
import io
import json
from pathlib import Path

import pytest

from engine import technical_orchestration_openai as toa
from scripts import run_g1_precreation_campaign as rc
from scripts import run_g1_precreation_semantic_eval as ev
from tests.test_g1_precreation_semantic_eval import _all_recognized, _oracle, CLEAR

ROOT = Path(__file__).resolve().parent.parent
REVISION = "0" * 40
VERIFIED = {"verified_on": "2026-11-03", "source": "test fixture",
            "input_usd_per_1m": rc.PRICING["input_usd_per_1m"],
            "output_usd_per_1m": rc.PRICING["output_usd_per_1m"]}


@pytest.fixture(scope="module")
def pack():
    return ev.load_pack()


@pytest.fixture
def evidence(tmp_path, monkeypatch):
    """Point the fixed evidence paths at a temporary directory."""
    d = tmp_path / "evidence"
    monkeypatch.setattr(rc, "EVIDENCE_DIR", str(d))
    monkeypatch.setattr(rc, "JOURNAL_PATH", str(d / "campaign_01_journal.jsonl"))
    monkeypatch.setattr(rc, "REPORT_PATH", str(d / "campaign_01_report.json"))
    monkeypatch.setattr(rc, "_evidence_in_history", lambda: False)
    return d


def _body(reply, *, model=toa.MODEL, usage=True, refusal=False, out_tokens=300):
    part = ({"type": "refusal", "refusal": "no"} if refusal
            else {"type": "output_text", "text": json.dumps(reply)})
    data = {"id": "resp_x", "status": "completed", "model": model,
            "output": [{"type": "message", "content": [part]}]}
    if usage:
        data["usage"] = {"input_tokens": 1500, "output_tokens": out_tokens}
    return 200, json.dumps(data).encode()


class _Fake:
    OFFLINE_FAKE = True

    def __init__(self, responses):
        self.responses, self.calls = list(responses), []

    def __call__(self, url, headers, body, timeout):
        self.calls.append(json.loads(body.decode("utf-8")))
        item = self.responses.pop(0)
        if isinstance(item, BaseException):
            raise item
        return item


class _NotFake(_Fake):
    """A local transport that does NOT declare itself an offline fake, so the
    runner treats it as real and must apply every boundary first."""
    OFFLINE_FAKE = False


def _adapter(transport):
    return rc.OpenAIMsnlAdapter(allow_network=True, transport=rc.RecordingTransport(transport))


def _oracle_responses(pack):
    cases, refs = pack
    return [_body(_oracle(c, refs[c["case_id"]])) for c in cases]


def _run(pack, responses, cases=None):
    """A fake run with an in-memory journal; returns (report, fake, journal lines)."""
    fake, journal = _Fake(responses), io.StringIO()
    adapter = _adapter(fake)
    report = rc.campaign(adapter, pack[0] if cases is None else cases,
                         rc.run_manifest(REVISION, adapter._model), journal)
    return report, fake, journal.getvalue().splitlines()


def _bound(report, **judged):
    return dict(judged, report_sha256=rc._digest(report))


def _open(monkeypatch, revision=REVISION):
    """Simulate a separately authorized activation (gate open, price verified,
    clean checkout at ``revision``) without changing the module on disk."""
    monkeypatch.setattr(rc, "G1_PRECREATION_CAMPAIGN_AUTHORIZED", True)
    monkeypatch.setattr(rc, "PRICE_VERIFICATION", dict(VERIFIED))
    monkeypatch.setattr(rc, "current_revision", lambda: revision)


# ── The gate is closed in this revision ─────────────────────────────────────
def test_committed_gate_is_closed_and_price_unverified():
    assert rc.G1_PRECREATION_CAMPAIGN_AUTHORIZED is False
    assert rc.AUTHORIZED_RUN_MANIFEST_SHA256 is None
    assert rc.PRICE_VERIFICATION is None and rc.price_verified() is False


def test_cli_campaign_refuses_before_any_adapter_or_transport(monkeypatch, evidence, capsys):
    def boom(*a, **k):
        raise AssertionError("an adapter or transport was built")
    monkeypatch.setattr(rc, "OpenAIMsnlAdapter", boom)
    monkeypatch.setattr(toa, "_urllib_transport", boom)
    monkeypatch.setattr(rc, "current_revision", lambda: REVISION)
    digest = rc._digest(rc.run_manifest(REVISION, rc.MODEL))
    code = rc.main(["--provider", "openai", "--allow-network", "--managed-credential",
                    "--authorized-manifest", digest])
    assert code == 2 and "campaign gate is closed" in capsys.readouterr().out
    assert not evidence.exists()


def test_campaign_with_a_real_transport_refuses_while_the_gate_is_closed(pack, evidence):
    transport = _NotFake(_oracle_responses(pack))
    adapter = _adapter(transport)
    manifest = rc.run_manifest(REVISION, adapter._model)
    with pytest.raises(rc.PackError, match="gate is closed"):
        rc.campaign(adapter, pack[0], manifest, None, rc._digest(manifest))
    assert transport.calls == [] and not evidence.exists()


# ── Every boundary fails closed, in an otherwise open activation ────────────
@pytest.mark.parametrize("breach", [
    "no_digest", "wrong_digest", "price_unverified", "price_mismatch", "dirty_or_other_revision",
    "evidence_in_tree", "evidence_in_history", "caller_journal", "wrong_model", "extra_case",
])
def test_boundary_refuses_each_breach(breach, pack, evidence, monkeypatch):
    _open(monkeypatch)
    cases = list(pack[0])
    manifest = rc.run_manifest(REVISION, rc.MODEL)
    digest, journal = rc._digest(manifest), None
    if breach == "no_digest":
        digest = None
    elif breach == "wrong_digest":
        digest = "f" * 64
    elif breach == "price_unverified":
        monkeypatch.setattr(rc, "PRICE_VERIFICATION", None)
    elif breach == "price_mismatch":
        monkeypatch.setattr(rc, "PRICE_VERIFICATION", dict(VERIFIED, output_usd_per_1m=9.0))
    elif breach == "dirty_or_other_revision":
        monkeypatch.setattr(rc, "current_revision", lambda: "1" * 40)
    elif breach == "evidence_in_tree":
        evidence.mkdir()
        Path(rc.JOURNAL_PATH).write_text("")
    elif breach == "evidence_in_history":
        monkeypatch.setattr(rc, "_evidence_in_history", lambda: True)
    elif breach == "caller_journal":
        journal = object()
    elif breach == "wrong_model":
        manifest = rc.run_manifest(REVISION, "gpt-other")
        digest = rc._digest(manifest)
    elif breach == "extra_case":
        cases = cases + [cases[0]]
    with pytest.raises(rc.PackError):
        rc.check_campaign_boundary(cases, manifest, digest, journal)


def test_changed_fixture_or_preregistration_cannot_be_used(monkeypatch):
    monkeypatch.setattr(ev, "INPUT_SHA256", "0" * 64)
    with pytest.raises(rc.PackError):
        rc.run_manifest(REVISION, rc.MODEL)


def test_open_activation_passes_every_boundary(pack, evidence, monkeypatch):
    _open(monkeypatch)
    manifest = rc.run_manifest(REVISION, rc.MODEL)
    rc.check_campaign_boundary(list(pack[0]), manifest, rc._digest(manifest))


# ── Manifest identity and budget ────────────────────────────────────────────
def test_manifest_binds_the_whole_run_configuration(pack):
    m = rc.run_manifest(REVISION, rc.MODEL)
    assert m["input_sha256"] == ev.INPUT_SHA256 and m["reference_sha256"] == ev.REFERENCE_SHA256
    assert (m["preregistration_revision"], m["preregistration_sha256"]) == (
        4, ev.preregistration_digest())
    assert m["payloads_sha256"] == rc._digest([rc.payload(c) for c in pack[0]])
    assert (m["model"], m["endpoint"], m["max_output_tokens"], m["max_provider_requests"],
            m["retries"], m["store"], m["tools"]) == (
        "gpt-6-sol", toa.ENDPOINT, 1200, 20, 0, False, "none")
    assert m["budget"]["ceiling_usd"] == 5.0 and m["budget"]["price_verification"] is None
    assert m["evidence"] == {
        "journal": "docs/benchmarks/evidence/g1_precreation_semantic_v1/campaign_01_journal.jsonl",
        "report": "docs/benchmarks/evidence/g1_precreation_semantic_v1/campaign_01_report.json"}
    assert "never rerun" in m["one_run_policy"]


def test_any_configuration_change_changes_the_digest(monkeypatch):
    base = rc._digest(rc.run_manifest(REVISION, rc.MODEL))
    monkeypatch.setattr(rc, "MAX_OUTPUT_TOKENS", 1201)
    assert rc._digest(rc.run_manifest(REVISION, rc.MODEL)) != base
    monkeypatch.undo()
    assert rc._digest(rc.run_manifest("1" * 40, rc.MODEL)) != base
    monkeypatch.setattr(rc, "PRICE_VERIFICATION", dict(VERIFIED))
    assert rc._digest(rc.run_manifest(REVISION, rc.MODEL)) != base


def test_budget_plan_reserves_every_exact_payload_within_the_ceiling(pack):
    plan = rc.budget_plan(pack[0])
    assert plan["requests"] == 20 and plan["within_ceiling"] is True
    assert plan["all_reservations_usd"] <= 5.0


def test_cost_ceiling_stops_before_send_and_the_rest_is_not_attempted(pack, monkeypatch):
    monkeypatch.setattr(rc, "CAMPAIGN_CEILING_USD", 0.2)
    report, fake, _j = _run(pack, _oracle_responses(pack))
    sent = [r for r in report["rows"] if r["provider_status"] != rc.P_NOT_ATTEMPTED]
    rest = report["rows"][len(sent):]
    assert 1 <= len(fake.calls) == len(sent) < 20 and report["stopped_on"] == rc.ERR_COST_CEILING
    assert rest[0]["error_kind"] == rc.ERR_COST_CEILING
    assert all(r["provider_status"] == rc.P_NOT_ATTEMPTED for r in rest)
    bound = report["spend"]["conservative_bound_usd"]
    next_reservation = rc.reservation_usd(len(rc._body(pack[0][len(sent)], rc.MODEL)))
    assert bound <= 0.2 < bound + next_reservation        # stopped exactly by the rule


def test_missing_usage_is_charged_the_whole_reservation(pack):
    responses = _oracle_responses(pack)
    cases, refs = pack
    responses[0] = _body(_oracle(cases[0], refs[cases[0]["case_id"]]), usage=False)
    report, _fake, _j = _run(pack, responses)
    first = report["rows"][0]["attempt"]
    assert first["bound_usd"] == first["reserved_usd"] and first["measured_cost_usd"] is None
    assert report["spend"]["measured_cost_complete"] is False


# ── Requests: one per case, nothing but the idea text ───────────────────────
def test_one_request_per_case_and_no_reference_material_is_sent(pack):
    cases, refs = pack
    report, fake, _j = _run(pack, _oracle_responses(pack))
    assert len(fake.calls) == 20 and report["requests"] == 20
    for case, sent in zip(cases, fake.calls):
        assert set(sent) == {"model", "instructions", "input", "store", "max_output_tokens", "text"}
        assert sent["store"] is False and "tools" not in sent
        assert json.loads(sent["input"]) == {"idea_text": case["idea_text"]}
        flat = json.dumps(sent)
        assert case["case_id"] not in flat
        for r in refs.values():
            assert r["category"] not in flat
            for u in r["expected_unknowns"]:
                assert u["meaning"] not in flat
        assert "EXTERNAL_CONTEXT" not in flat and "allowed_composition" not in flat


def test_duplicate_case_is_refused(pack):
    cases = list(pack[0])
    fake = _Fake(_oracle_responses(pack) * 2)
    adapter = _adapter(fake)
    with pytest.raises(rc.PackError, match="duplicate"):
        rc.campaign(adapter, [cases[0], cases[0]], rc.run_manifest(REVISION, adapter._model))
    assert len(fake.calls) == 1


# ── Provider failures stop the run; a refusal is scored, never credited ─────
@pytest.mark.parametrize("bad,kind", [
    ((200, b"not json"), toa.ERR_MALFORMED),
    ((500, b"{}"), toa.ERR_HTTP_STATUS),
    ("over_cap", rc.ERR_COST_UNBOUNDED),
    ("other_model", rc.ERR_MODEL_UNCONFIRMED),
])
def test_provider_error_stops_and_the_run_is_incomplete(bad, kind, pack):
    responses = _oracle_responses(pack)
    cases, refs = pack
    good = _oracle(cases[2], refs[cases[2]["case_id"]])
    responses[2] = {"over_cap": _body(good, out_tokens=1201),
                    "other_model": _body(good, model="gpt-other")}.get(bad, bad)
    report, fake, lines = _run(pack, responses)
    assert len(fake.calls) == 3 and report["stopped_on"] == rc.P_ERROR
    assert report["rows"][2]["error_kind"] == kind
    assert all(r["provider_status"] == rc.P_NOT_ATTEMPTED for r in report["rows"][3:])
    agg = rc.aggregate(report, _bound(report, k6=CLEAR, g5=_all_recognized(refs)),
                       report["manifest_sha256"], lines)
    assert agg["verdict"] == "INCOMPLETE"


@pytest.mark.parametrize("last", [(500, b"{}"), "other_model", "bare_abstain"])
def test_provider_stop_on_the_last_case_is_incomplete_not_a_verdict(last, pack):
    cases, refs = pack
    responses = _oracle_responses(pack)
    good = _oracle(cases[-1], refs[cases[-1]["case_id"]])
    responses[-1] = {"other_model": _body(good, model="gpt-other"),
                     "bare_abstain": (200, json.dumps({
                         "id": "r", "status": "completed", "model": toa.MODEL,
                         "usage": {"input_tokens": 9, "output_tokens": 9},
                         "output": [{"type": "message", "content": [
                             {"type": "output_text", "text": toa.ABSTAIN}]}]}).encode())
                     }.get(last, last)
    report, _fake, lines = _run(pack, responses)
    assert not any(r["provider_status"] == rc.P_NOT_ATTEMPTED for r in report["rows"])
    full = _bound(report, k6=CLEAR, g5=_all_recognized(refs),
                  k4_context={"P12-part-1": ev.K6_CLEAR, "P12-part-2": ev.K6_CLEAR})
    assert rc.aggregate(report, full, report["manifest_sha256"], lines)["verdict"] \
        == "INCOMPLETE"


def test_refusal_does_not_stop_and_earns_nothing(pack):
    responses = _oracle_responses(pack)
    responses[0] = _body(None, refusal=True)
    report, fake, _j = _run(pack, responses)
    assert len(fake.calls) == 20 and report["rows"][0]["provider_status"] == rc.P_REFUSAL
    scored, _ = rc.score_report(report)
    assert scored[0]["status"] == ev.V_ERROR and scored[0]["effective"] == ev.FALLBACK


def test_interruption_leaves_the_journal_and_a_rerun_is_refused(pack, evidence, monkeypatch):
    _open(monkeypatch)
    responses = _oracle_responses(pack)
    responses[3] = KeyboardInterrupt()
    transport = _NotFake(responses)
    adapter = _adapter(transport)
    manifest = rc.run_manifest(REVISION, adapter._model)
    with pytest.raises(KeyboardInterrupt):
        rc.campaign(adapter, pack[0], manifest, None, rc._digest(manifest))
    lines = [json.loads(x) for x in Path(rc.JOURNAL_PATH).read_text().splitlines()]
    assert [x["event"] for x in lines].count("reserved") == 4
    again = _adapter(_NotFake(_oracle_responses(pack)))
    with pytest.raises(rc.PackError, match="one run only"):
        rc.campaign(again, pack[0], manifest, None, rc._digest(manifest))


# ── After the run: no verdict without the human reviews ─────────────────────
def _full_assessment(report, refs, items):
    return _bound(report, k6=CLEAR, g5=_all_recognized(refs),
                  k4_context={i["item_id"]: ev.K6_CLEAR for i in items["k4_context"]})


def test_no_go_without_every_human_assessment(pack):
    _cases, refs = pack
    report, _fake, lines = _run(pack, _oracle_responses(pack))
    digest = report["manifest_sha256"]
    assert rc.aggregate(report, None, digest, lines)["verdict"] == "INCOMPLETE_REVIEW"
    partial = _bound(report, k6=CLEAR, g5=_all_recognized(refs))   # K4 context pending
    assert rc.aggregate(report, partial, digest, lines)["verdict"] == "INCOMPLETE_REVIEW"
    items = rc.review_items(report, digest, lines)
    assert items["report_sha256"] == rc._digest(report)
    assert [i["item_id"] for i in items["k4_context"]] == ["P12-part-1", "P12-part-2"]
    assert rc.aggregate(report, _full_assessment(report, refs, items), digest, lines)[
        "verdict"] == "PRELIMINARY_GO"


def test_assessment_must_be_bound_to_this_exact_report(pack):
    _cases, refs = pack
    report, _fake, lines = _run(pack, _oracle_responses(pack))
    digest = report["manifest_sha256"]
    full = _full_assessment(report, refs, rc.review_items(report, digest, lines))
    for bad in (dict(full, report_sha256="f" * 64),
                {k: v for k, v in full.items() if k != "report_sha256"}, []):
        with pytest.raises(rc.PackError, match="not bound"):
            rc.aggregate(report, bad, digest, lines)


def test_fabricated_or_edited_rows_do_not_match_the_journal(pack):
    """Reviewer probe: a run stopped by HTTP 500 at case 6, with rows 6-20 then
    rewritten as fabricated replies, must be refused, never a GO."""
    cases, refs = pack
    responses = _oracle_responses(pack)
    responses[5] = (500, b"{}")
    report, _fake, lines = _run(pack, responses)
    digest = report["manifest_sha256"]
    forged = json.loads(json.dumps(report))
    for case, row in zip(cases[5:], forged["rows"][5:]):
        row.update(provider_status=rc.P_RESPONDED, error_kind=None,
                   reply=_oracle(case, refs[case["case_id"]]),
                   attempt=dict(forged["rows"][0]["attempt"]))
    forged["stopped_on"], forged["requests"] = None, 20
    with pytest.raises(rc.PackError, match="journal"):
        rc.aggregate(forged, None, digest, lines)
    good, _f, good_lines = _run(pack, _oracle_responses(pack))
    edited = json.loads(json.dumps(good))
    edited["rows"][0]["reply"]["composition_suggestion"] = ev.CLARIFY_FIRST
    with pytest.raises(rc.PackError, match="journal"):
        rc.aggregate(edited, None, good["manifest_sha256"], good_lines)
    with pytest.raises(rc.PackError):
        rc.aggregate(good, None, good["manifest_sha256"], good_lines[:-1])
    for journal in ([1, 2], None, ["{"]):
        with pytest.raises(rc.PackError):
            rc.aggregate(good, None, good["manifest_sha256"], journal)


@pytest.mark.parametrize("mutate", [
    lambda r: r.update(rows=[1] * 20),
    lambda r: r["rows"][0].pop("reply"),
    lambda r: r["rows"][0].update(provider_status="DONE"),
    lambda r: r["rows"][0].update(reply=None),
    lambda r: r.update(rows="x"),
])
def test_malformed_report_is_refused_not_crashed(mutate, pack):
    report, _fake, lines = _run(pack, _oracle_responses(pack))
    bad = json.loads(json.dumps(report))
    mutate(bad)
    with pytest.raises(rc.PackError):
        rc.aggregate(bad, None, report["manifest_sha256"], lines)


def test_report_must_be_the_authorized_untampered_run(pack):
    report, _fake, lines = _run(pack, _oracle_responses(pack))
    with pytest.raises(rc.PackError):
        rc.aggregate(report, None, "f" * 64, lines)
    tampered = dict(report, manifest=dict(report["manifest"], max_output_tokens=4000))
    with pytest.raises(rc.PackError):
        rc.aggregate(tampered, None, report["manifest_sha256"], lines)
    shuffled = dict(report, rows=list(reversed(report["rows"])))
    with pytest.raises(rc.PackError):
        rc.aggregate(shuffled, None, report["manifest_sha256"], lines)


# ── Offline surfaces and boundaries ─────────────────────────────────────────
def test_offline_plan_sends_nothing(monkeypatch, capsys):
    monkeypatch.setattr(toa, "_urllib_transport",
                        lambda *a, **k: (_ for _ in ()).throw(AssertionError("network")))
    assert rc.main([]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["campaign_authorized"] is False and out["price_verified"] is False
    assert out["cases"] == 20 and out["budget"]["within_ceiling"] is True


def test_runner_is_not_imported_by_any_product_module_and_the_pack_is_untouched():
    for folder in ("engine", "web"):
        for path in (ROOT / folder).rglob("*.py"):
            assert "run_g1_precreation_campaign" not in path.read_text(encoding="utf-8")
    assert ev.PREREGISTRATION_REVISION == 4
    assert ev.preregistration_digest() == (
        "aae4a9af41d84616409badfcc77b9a313bae40dcc0919b69851de6b231285e1f")
