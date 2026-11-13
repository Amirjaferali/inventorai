"""G1 faithful rephrasing — guarded single-run runner (network-free).

Every transport is a local fake. Replies are HANDCRAFTED from the adjudicated
reference to exercise the runner and the frozen decision rule; they are not
model results, and nothing here measures any model.
"""
import io
import json
from pathlib import Path

import pytest

from engine import technical_orchestration_openai as toa
from scripts import g1_faithful_rephrasing_eval as ev
from scripts import g1_faithful_rephrasing_prompt as fp
from scripts import run_g1_faithful_rephrasing_campaign as rc
from scripts import run_g1_precreation_campaign as c01
from scripts import run_g1_precreation_campaign_02 as c02
from scripts.run_msnl_eval import quote_grounded
from tests.test_g1_precreation_campaign import _Fake, _NotFake, _adapter, _body

REVISION = "0" * 40


@pytest.fixture(scope="module")
def pack():
    return ev.load_pack()


@pytest.fixture
def evidence(tmp_path, monkeypatch):
    d = tmp_path / "evidence"
    monkeypatch.setattr(rc, "EVIDENCE_DIR", str(d))
    monkeypatch.setattr(rc, "JOURNAL_PATH", str(d / "campaign_journal.jsonl"))
    monkeypatch.setattr(rc, "REPORT_PATH", str(d / "campaign_report.json"))
    monkeypatch.setattr(rc, "_evidence_in_history", lambda: False)
    return d


def _oracle(case, ref):
    """A handcrafted reply that restates the reference: the idea text as the
    rephrasing (right script) and one statement per traceable reference point."""
    lang = ev.language_of(case["variety"])
    if ref["expected_abstain"]:
        return {"outcome": "ABSTAINED", "language": lang, "rephrasing": "", "statements": [],
                "abstain_reason": "NOT_AN_INVENTION"}
    statements = [{"kind": p["kind"], "text": p["statement"] if lang == "en" else p["source_span"],
                   "source_quote": p["source_span"]}
                  for p in ref["points"] if quote_grounded(p["source_span"], case["idea_text"])]
    return {"outcome": "REPHRASED", "language": lang, "rephrasing": case["idea_text"][:1500],
            "statements": statements or [{"kind": "FUNCTION", "text": case["idea_text"][:300],
                                          "source_quote": case["idea_text"][:300]}],
            "abstain_reason": "NONE"}


def _responses(pack):
    cases, ref = pack
    return [_body(_oracle(c, ref[c["case_id"]])) for c in cases]


def _run(pack, responses):
    fake, journal = _Fake(responses), io.StringIO()
    adapter = _adapter(fake)
    report = rc.campaign(adapter, pack[0], rc.run_manifest(REVISION, adapter._model), journal)
    return report, fake, journal.getvalue().splitlines()


def _assessment(report, lines, digest, mutate=None):
    msg = rc.assessment_message(report, digest, lines)
    _cases, ref = ev.load_pack()
    records = {}
    for key, cid in msg["keymap"].items():
        records[key] = {"points": {p["id"]: "PRESERVED" for p in ref[cid]["points"]},
                        "material_additions": [], "unknown_resolved": False,
                        "instruction_followed": False,
                        "abstention": "CORRECT" if ref[cid]["expected_abstain"] else
                        "NOT_APPLICABLE",                     # derived (A2) for the oracle
                        "unsupported_statements": [], "style_issues": [], "notes": ""}
        if mutate:
            mutate(cid, records[key])
    return msg, {"report_sha256": msg["report_sha256"], "records": records}


# ── Identity and limits ─────────────────────────────────────────────────────
def test_limits_and_distinct_identity():
    assert (rc.MAX_PROVIDER_REQUESTS, rc.RETRIES, rc.MAX_OUTPUT_TOKENS,
            rc.CAMPAIGN_CEILING_USD) == (40, 0, 2000, 10.0)
    assert rc.AUTHORIZED_RUN_MANIFEST_SHA256 is None
    assert rc.EVIDENCE_DIR not in (c01.EVIDENCE_DIR, c02.EVIDENCE_DIR)
    assert rc.MODEL == toa.MODEL == c01.PRICING["model"]
    assert not Path(rc.EVIDENCE_DIR).exists()


def test_manifest_binds_prompt_pack_and_preregistration(pack):
    m = rc.run_manifest(REVISION, rc.MODEL)
    assert (m["cases_sha256"], m["reference_sha256"], m["preregistration_sha256"],
            m["instructions_sha256"], m["schema_sha256"]) == (
        ev.CASES_SHA256, ev.REFERENCE_SHA256, ev.PREREG_SHA256,
        ev.INSTRUCTIONS_SHA256, ev.SCHEMA_SHA256)
    assert m["payloads_sha256"] == rc._digest([rc.payload(c) for c in pack[0]])
    assert (m["max_provider_requests"], m["retries"], m["store"], m["tools"]) == (
        40, 0, False, "none")


def test_payload_is_the_frozen_prompt_with_only_the_idea_text(pack):
    cases, ref = pack
    for case in cases:
        body = rc.payload(case)
        assert set(body) == {"model", "instructions", "input", "store", "max_output_tokens",
                             "text"}
        assert body["instructions"] == fp.INSTRUCTIONS and body["store"] is False
        assert body["text"]["format"]["schema"] == fp.schema()
        assert json.loads(body["input"]) == {"idea_text": case["idea_text"]}
        whole = json.dumps(body, ensure_ascii=False)
        assert case["case_id"] not in whole
        assert case["variety"] == "en" or case["variety"] not in whole
        flat = json.dumps({k: v for k, v in body.items() if k != "input"})
        assert case["category"] not in flat or case["category"] in fp.INSTRUCTIONS
        for other in ref.values():          # no reference statement outside the idea text
            for p in other["points"]:
                assert p["statement"] not in flat


def test_budget_reserves_every_request_within_the_ceiling(pack):
    plan = rc.budget_plan(pack[0])
    assert plan["requests"] == 40 and plan["within_ceiling"] is True


# ── Authorization: fails closed before any provider interaction ─────────────
@pytest.mark.parametrize("digest", [None, "f" * 64, "not-a-digest"])
def test_cli_refuses_before_any_adapter_or_transport(digest, monkeypatch, evidence, capsys):
    def boom(*a, **k):
        raise AssertionError("an adapter or transport was built")
    monkeypatch.setattr(rc, "OpenAIMsnlAdapter", boom)
    monkeypatch.setattr(toa, "_urllib_transport", boom)
    monkeypatch.setattr(rc, "current_revision", lambda: REVISION)
    argv = ["--provider", "openai", "--allow-network", "--managed-credential"]
    if digest is not None:
        argv += ["--authorized-manifest", digest]
    assert rc.main(argv) == 2 and "not authorized" in capsys.readouterr().out
    assert not evidence.exists()


def test_real_transport_without_the_digest_sends_nothing(pack, evidence):
    transport = _NotFake(_responses(pack))
    adapter = _adapter(transport)
    with pytest.raises(rc.PackError, match="not authorized"):
        rc.campaign(adapter, pack[0], rc.run_manifest(REVISION, adapter._model), None, None)
    assert transport.calls == [] and not evidence.exists()


@pytest.mark.parametrize("breach", [
    "wrong_digest", "price_unverified", "other_revision", "evidence_in_tree",
    "evidence_in_history", "caller_journal", "wrong_model", "extra_case", "prep_invalid",
])
def test_boundary_refuses_each_breach(breach, pack, evidence, monkeypatch):
    monkeypatch.setattr(rc, "current_revision", lambda: REVISION)
    cases = list(pack[0])
    manifest = rc.run_manifest(REVISION, rc.MODEL)
    digest, journal = rc._digest(manifest), None
    if breach == "wrong_digest":
        digest = "e" * 64
    elif breach == "price_unverified":
        monkeypatch.setattr(c01, "PRICE_VERIFICATION", None)
    elif breach == "other_revision":
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
    elif breach == "prep_invalid":
        monkeypatch.setattr(ev, "preparation_checks",
                            lambda *a, **k: {"verdict": ev.PREPARATION_INVALID})
    expected = {"wrong_digest": "not authorized", "price_unverified": "price basis",
                "other_revision": "this checkout", "evidence_in_tree": "already exists",
                "evidence_in_history": "already exists", "caller_journal": "created by the run",
                "wrong_model": "price basis for this model", "extra_case": "pinned pack",
                "prep_invalid": "PREPARATION_INVALID"}[breach]
    with pytest.raises(rc.PackError, match=expected):
        rc.check_campaign_boundary(cases, manifest, digest, journal)


def test_the_exact_digest_passes_every_boundary(pack, evidence, monkeypatch):
    monkeypatch.setattr(rc, "current_revision", lambda: REVISION)
    manifest = rc.run_manifest(REVISION, rc.MODEL)
    rc.check_campaign_boundary(list(pack[0]), manifest, rc._digest(manifest))


def test_interrupted_run_keeps_its_journal_and_cannot_restart(pack, evidence, monkeypatch):
    monkeypatch.setattr(rc, "current_revision", lambda: REVISION)
    responses = _responses(pack)
    responses[5] = KeyboardInterrupt()
    adapter = _adapter(_NotFake(responses))
    manifest = rc.run_manifest(REVISION, adapter._model)
    with pytest.raises(KeyboardInterrupt):
        rc.campaign(adapter, pack[0], manifest, None, rc._digest(manifest))
    lines = [json.loads(x) for x in Path(rc.JOURNAL_PATH).read_text().splitlines()]
    assert [x["event"] for x in lines].count("reserved") == 6
    again = _adapter(_NotFake(_responses(pack)))
    with pytest.raises(rc.PackError, match="one run only"):
        rc.campaign(again, pack[0], manifest, None, rc._digest(manifest))


# ── After the run ───────────────────────────────────────────────────────────
def test_every_handcrafted_reply_is_deterministically_valid(pack):
    cases, ref = pack
    for c in cases:
        assert ev.validate_reply(_oracle(c, ref[c["case_id"]]), c) == (ev.VALID, []), c["case_id"]


def test_a_fully_preserved_assessment_qualifies_every_subset_separately(pack):
    report, fake, lines = _run(pack, _responses(pack))
    assert len(fake.calls) == 40 and report["stopped_on"] is None
    digest = report["manifest_sha256"]
    msg, assessment = _assessment(report, lines, digest)
    for cid in msg["keymap"].values():
        assert all(cid not in m for m in msg["messages"])
    out = rc.aggregate(report, assessment, digest, lines)
    assert set(out["subsets"]) == set(ev.SUBSETS)
    assert all(s["verdict"] == ev.QUALIFIED for s in out["subsets"].values())
    assert "untested language variety" in out["scope"]


def test_one_hard_failure_fails_only_its_own_subset(pack):
    report, _fake, lines = _run(pack, _responses(pack))
    cases, ref = pack
    target = next(c["case_id"] for c in cases
                  if c["variety"] == "ar_egyptian" and ref[c["case_id"]]["points"])

    def mutate(cid, rec):
        if cid == target:
            rec["material_additions"] = [{"type": "COMPONENT", "text": "a motor"}]
    _msg, assessment = _assessment(report, lines, report["manifest_sha256"], mutate)
    out = rc.aggregate(report, assessment, report["manifest_sha256"], lines)
    assert out["subsets"]["ar_egyptian"]["verdict"] == ev.NOT_QUALIFIED
    assert out["subsets"]["ar_egyptian"]["hard_failure_cases"] == [target]
    assert all(out["subsets"][s]["verdict"] == ev.QUALIFIED
               for s in ("en", "ar_msa", "ar_gulf_kuwaiti"))


def test_provider_error_or_refusal(pack):
    responses = _responses(pack)
    responses[3] = (500, b"{}")
    report, _fake, lines = _run(pack, responses)
    out = rc.aggregate(report, None, report["manifest_sha256"], lines)
    assert out["verdict"] == ev.INCOMPLETE
    responses = _responses(pack)
    responses[0] = _body(None, refusal=True)
    report, _fake, lines = _run(pack, responses)
    assert report["rows"][0]["provider_status"] == rc.P_REFUSAL and report["stopped_on"] is None
    _msg, assessment = _assessment(report, lines, report["manifest_sha256"])
    out = rc.aggregate(report, assessment, report["manifest_sha256"], lines)
    first = pack[0][0]
    row = next(r for r in out["subsets"][first["variety"]]["rows"]
               if r["case_id"] == first["case_id"])
    assert row["verdict"] == ev.NOT_FAITHFUL and row["validation"] == ev.NO_REPLY


def test_assessment_must_be_bound_and_complete(pack):
    report, _fake, lines = _run(pack, _responses(pack))
    digest = report["manifest_sha256"]
    _msg, assessment = _assessment(report, lines, digest)
    with pytest.raises(rc.PackError):
        rc.aggregate(report, dict(assessment, report_sha256="0" * 64), digest, lines)
    partial = dict(assessment, records=dict(list(assessment["records"].items())[1:]))
    with pytest.raises(rc.PackError):
        rc.aggregate(report, partial, digest, lines)
    with pytest.raises(rc.PackError):
        rc.aggregate(report, assessment, "f" * 64, lines)
    tampered = json.loads(json.dumps(report))
    tampered["rows"][0]["reply"] = {"outcome": "ABSTAINED"}
    with pytest.raises(rc.PackError):
        rc.aggregate(tampered, assessment, digest, lines)


def test_a_restated_non_idea_or_invalid_reply_fails_its_subset(pack):
    """Amendment A2 at run level: a restated non-invention (MISSED_ABSTAIN) and a
    deterministically invalid reply each fail their own subset, whatever the
    assessor writes."""
    cases, ref = pack
    responses = _responses(pack)
    non_idea = next(i for i, c in enumerate(cases)
                    if c["variety"] == "ar_msa" and ref[c["case_id"]]["expected_abstain"])
    invalid = next(i for i, c in enumerate(cases) if c["variety"] == "en")
    restated = {"outcome": "REPHRASED", "language": "ar",
                "rephrasing": cases[non_idea]["idea_text"],
                "statements": [{"kind": "FUNCTION", "text": cases[non_idea]["idea_text"][:60],
                                "source_quote": cases[non_idea]["idea_text"][:60]}],
                "abstain_reason": "NONE"}
    fabricated = dict(_oracle(cases[invalid], ref[cases[invalid]["case_id"]]),
                      statements=[{"kind": "FUNCTION", "text": "An electric motor.",
                                   "source_quote": "an electric motor inside"}])
    responses[non_idea], responses[invalid] = _body(restated), _body(fabricated)
    report, _fake, lines = _run(pack, responses)

    def mutate(cid, rec):
        if cid == cases[non_idea]["case_id"]:
            rec["abstention"] = "MISSED_ABSTAIN"
    _msg, assessment = _assessment(report, lines, report["manifest_sha256"], mutate)
    out = rc.aggregate(report, assessment, report["manifest_sha256"], lines)
    assert out["subsets"]["ar_msa"]["verdict"] == ev.NOT_QUALIFIED
    assert out["subsets"]["ar_msa"]["hard_failure_cases"] == [cases[non_idea]["case_id"]]
    assert out["subsets"]["en"]["verdict"] == ev.NOT_QUALIFIED
    assert out["subsets"]["en"]["hard_failure_cases"] == [cases[invalid]["case_id"]]
    assert set(out["reported_not_gating"]) == set(ev.SUBSETS)
    # An assessor value that disagrees with the derived abstention is refused.
    _msg, wrong = _assessment(report, lines, report["manifest_sha256"])
    with pytest.raises(rc.PackError, match="abstention"):
        rc.aggregate(report, wrong, report["manifest_sha256"], lines)
