"""Autonomous Technical Orchestration — Synthetic Evaluation Pack V1 and harness.

File-creation contract:
  Path: tests/test_technical_orchestration_eval.py
  Purpose: prove the committed synthetic pack
    (`tests/fixtures/technical_orchestration_eval_v1.json`) is well-formed,
    pinned, complete in its declared coverage and distinct from the MSNL pack
    and the T1-C′ study corpus; that the simulated adapter outputs adjudicate as
    labelled; that the deterministic metrics compute as defined; and that the
    developer harness (`scripts/run_technical_orchestration_eval.py`) is
    network-free by default and structurally unable to take real input.
  Input contract: the committed pack; fake transports; scripted test adapters.
  Output contract: pass/fail evidence only.
  Prohibited behaviors: no network, no credential, no real data, no claim of
    model quality, no acceptance threshold.
"""
import collections
import hashlib
import importlib.util
import io
import json
import pathlib
import shutil

import pytest

from engine import technical_orchestration_openai as toa
from engine import technical_orchestration_shadow as tos

ROOT = pathlib.Path(__file__).resolve().parents[1]
PACK = ROOT / "tests" / "fixtures" / "technical_orchestration_eval_v1.json"
FAKE_KEY = "sk-test-FAKE-harness-never-real"


def _harness():
    spec = importlib.util.spec_from_file_location(
        "run_technical_orchestration_eval",
        ROOT / "scripts" / "run_technical_orchestration_eval.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = _harness()


@pytest.fixture(scope="module")
def pack():
    return H.load_pack()


class Replay:
    """Test-only adapter: replays a fixed provider-neutral reply dict. It is
    never a product adapter and generates nothing."""

    name = "replay"

    def __init__(self, reply):
        self.reply = reply

    def propose(self, request):
        r = self.reply
        return tos.OrchestrationResponse(r["outcome"], tuple(
            tos.Proposal(p["kind"], p["text"], tuple(p["source_handles"]), p["gap_type"])
            for p in r["proposals"]))


class Scripted:
    """Test-only adapter: per case, one grounded proposal of the first expected
    kind (or an abstention). Used only to check the metric arithmetic."""

    name = "scripted"

    def __init__(self, by_gap_text):
        self.by_gap_text = by_gap_text

    def propose(self, request):
        item = self.by_gap_text.get(request.sources[0].text)
        if item is None:
            return tos.OrchestrationResponse(tos.ABSTAIN)
        return tos.OrchestrationResponse(tos.PROPOSED, tuple(
            tos.Proposal(k, t, ("s1",), request.gap_type) for k, t in item))


# ─────────────────────────────────────────────────────────────────────────────
# 1. The pack
# ─────────────────────────────────────────────────────────────────────────────

def test_pack_is_pinned_and_declared_synthetic(pack):
    assert hashlib.sha256(PACK.read_bytes()).hexdigest() == H.PACK_SHA256
    assert pack["synthetic"] is True and pack["pack_id"] == "technical-orchestration-eval-v1"
    for needle in ("SYNTHETIC", "no real inventor", "not a tuning corpus",
                   "native-speaker review"):
        assert needle in pack["statement"]


def test_pack_size_and_kind_coverage(pack):
    cases = pack["cases"]
    assert len(cases) == 55
    by_cat = collections.Counter(c["category"] for c in cases)
    for kind in tos.PROPOSAL_KINDS:
        assert by_cat[kind] == 4, kind
    assert sum(by_cat[k] for k in tos.PROPOSAL_KINDS) == 32


def test_every_negative_and_safety_category_is_present(pack):
    by_cat = collections.Counter(c["category"] for c in pack["cases"])
    assert {k: by_cat[k] for k in H.NEGATIVE_CATEGORIES} == {
        "ABSTAIN": 2, "UNSUPPORTED_REQUEST": 2, "FINAL_DESIGN_REQUEST": 2,
        "SAFETY_CERTIFICATION_REQUEST": 2, "CONTRADICTION": 2, "NEGATION": 2,
        "PROMPT_INJECTION": 4, "PLANTED_PERSONAL_DATA": 2, "OUT_OF_DOMAIN": 2,
        "VERY_SHORT": 2, "UNKNOWN_CONTEXT": 1}
    sims = collections.Counter(s["category"] for s in pack["simulated_responses"])
    for needed in ("UNKNOWN_HANDLE_OUTPUT", "UNSUPPORTED_KIND_OUTPUT", "MALFORMED_OUTPUT",
                   "INVALID_TEXT_OUTPUT", "GAP_OUT_OF_SCOPE_OUTPUT", "OVER_CAP_OUTPUT"):
        assert sims[needed] >= 1, needed


def test_language_breakdown_and_complete_pairs(pack):
    langs = collections.Counter(c["language"] for c in pack["cases"])
    assert langs == {"en": 19, "msa": 12, "kw": 13, "eg": 11}
    groups = collections.defaultdict(list)
    for c in pack["cases"]:
        if c["pair_group"]:
            groups[c["pair_group"]].append(c)
    assert len(groups) == 8
    for g, members in groups.items():
        assert sorted(m["language"] for m in members) == sorted(H.LANGUAGES)
        assert len({(m["category"], m["domain"], m["gap_type"]) for m in members}) == 1
        assert len({len(m["sources"]) for m in members}) == 1


def test_every_case_is_a_valid_request_with_no_identifier(pack):
    for c in pack["cases"]:
        req, handle_map = H.case_request(c)
        assert set(handle_map) == {s.handle for s in req.sources}
        assert c["case_id"] not in json.dumps(req.as_payload(), ensure_ascii=False)


def test_expectations_are_bounded_not_exact_prose(pack):
    for c in pack["cases"]:
        e = c["expect"]
        assert set(e) == {"expected_kinds", "abstain", "min_proposals", "max_proposals",
                          "forbidden_phrases", "injection", "review_focus"}
        assert 0 <= e["min_proposals"] <= e["max_proposals"] <= tos.MAX_PROPOSALS
    injected = [c for c in pack["cases"] if c["expect"]["injection"]]
    assert {c["language"] for c in injected} == set(H.LANGUAGES)
    assert all("s9" in c["sources"][0] for c in injected)


def test_pack_is_not_the_msnl_pack_or_the_t1c_corpus(pack):
    ours = {t for c in pack["cases"] for t in c["sources"] if len(t) > 12}
    msnl = (ROOT / "tests" / "fixtures" / "msnl_evaluation_pack_v1.json").read_text(encoding="utf-8")
    t1c_path = ROOT / "docs" / "validation" / "T1C_STANDARDIZED_STUDY_CORPUS_V1.md"
    t1c = t1c_path.read_text(encoding="utf-8") if t1c_path.exists() else ""
    assert not [t for t in ours if t in msnl or t in t1c]


def test_planted_personal_data_is_visibly_synthetic(pack):
    pii = [c for c in pack["cases"] if c["category"] == "PLANTED_PERSONAL_DATA"]
    for c in pii:
        assert "synthetic@example.com" in c["sources"][0]
        assert c["expect"]["forbidden_phrases"]


def test_tampered_pack_is_refused(tmp_path, monkeypatch):
    copy = tmp_path / "pack.json"
    shutil.copy(PACK, copy)
    copy.write_bytes(copy.read_bytes().replace(b"A water-tank", b"A water-tonk"))
    monkeypatch.setattr(H, "PACK_PATH", str(copy))
    with pytest.raises(H.PackError):
        H.load_pack()
    assert H.main([]) == 2


# ─────────────────────────────────────────────────────────────────────────────
# 2. Simulated adapter outputs adjudicate as labelled
# ─────────────────────────────────────────────────────────────────────────────

def test_simulated_outputs_adjudicate_as_labelled(pack):
    cases = {c["case_id"]: c for c in pack["cases"]}
    for sim in pack["simulated_responses"]:
        req, _ = H.case_request(cases[sim["case_id"]])
        res = tos.evaluate(req, Replay(sim["response"]))
        e = sim["expect"]
        assert (res.outcome, res.disposition) == (e["outcome"], e["disposition"]), sim["response_id"]
        assert list(res.discarded) == e["discarded"], sim["response_id"]
        if "accepted" in e:
            assert len(res.proposals) == e["accepted"]


# ─────────────────────────────────────────────────────────────────────────────
# 3. Metrics
# ─────────────────────────────────────────────────────────────────────────────

def test_null_baseline_metrics(pack):
    m = H.metrics(pack, H.run(tos.NullAdapter(), pack))
    assert m["cases_run"] == 55 and m["outcomes"] == {"ABSTAIN": 55}
    for rate in ("source_grounded_proposal_rate", "valid_handle_rate",
                 "unsupported_attribution_rate", "forbidden_authority_claim_rate",
                 "proposal_kind_compliance_rate", "gap_scope_compliance_rate"):
        assert m[rate] is None
    assert m["required_abstention_correct"] == [4, 4]
    assert m["unexpected_abstentions"] == [32, 32]
    assert m["expected_kind_agreement"] == [0, 35]
    assert m["cross_language_kind_consistency"] == [8, 8]
    assert not [k for k in m if "score" in k or "threshold" in k or "pass" in k]


def test_metric_arithmetic_on_a_scripted_adapter(pack):
    script = {}
    for c in pack["cases"]:
        if c["category"] in tos.PROPOSAL_KINDS:
            items = [(c["category"], "Grounded %s idea." % c["category"].lower())]
            if c["category"] == tos.ALTERNATIVE:
                items.append((tos.ALTERNATIVE, "A second distinct approach."))
            if c["language"] == "eg" and c["category"] == tos.DIRECTION:
                items = [(tos.EVIDENCE_NEED, "Measure the buckle force.")]
            script[c["sources"][0]] = items
        elif c["category"] == "PROMPT_INJECTION" and c["language"] == "en":
            script[c["sources"][0]] = [(tos.DIRECTION, "This design is verified.")]
    runs = H.run(Scripted(script), pack)
    m = H.metrics(pack, runs)
    assert m["raw_proposals"] == m["accepted_proposals"] == 37
    assert m["source_grounded_proposal_rate"] == 1.0
    assert m["valid_handle_rate"] == 1.0
    assert m["forbidden_authority_claim_rate"] == round(1 / 37, 4)
    assert m["expected_kind_agreement"] == [31, 35]
    assert m["alternative_diversity_cases"] == [4, 8]
    assert m["prompt_injection_resisted"] == [3, 4]
    assert m["cross_language_kind_consistency"] == [7, 8]
    assert m["unexpected_abstentions"] == [0, 32]


def test_metrics_count_hallucinated_handles(pack):
    case = next(c for c in pack["cases"] if c["case_id"] == "direction-en")
    sim = next(s for s in pack["simulated_responses"] if s["response_id"] == "sim-unknown-handle")
    req, _ = H.case_request(case)
    m = H.metrics(pack, [(case, tos.evaluate(req, Replay(sim["response"])), None)])
    assert m["valid_handle_rate"] == 0.0 and m["unsupported_attribution_rate"] == 1.0


# ─────────────────────────────────────────────────────────────────────────────
# 4. The harness: offline by default, no real-data input
# ─────────────────────────────────────────────────────────────────────────────

@pytest.fixture
def no_network(monkeypatch):
    import socket
    import urllib.request

    def refuse(*a, **k):
        raise AssertionError("network must not be touched")
    monkeypatch.setattr(urllib.request, "urlopen", refuse)
    monkeypatch.setattr(socket, "create_connection", refuse)


def test_default_invocation_is_null_and_offline(no_network, capsys):
    assert H.main([]) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["adapter"] == "null" and report["metrics"]["cases_run"] == 55
    assert all("proposals" not in c for c in report["cases"])


def test_openai_needs_explicit_network_permission_and_a_credential(no_network, monkeypatch, capsys):
    monkeypatch.setenv(toa.CREDENTIAL_ENV, FAKE_KEY)
    assert H.main(["--provider", "openai"]) == 2
    monkeypatch.delenv(toa.CREDENTIAL_ENV)
    assert H.main(["--provider", "openai", "--allow-network"]) == 2
    out = capsys.readouterr()
    assert FAKE_KEY not in out.out + out.err


def test_openai_run_uses_only_the_committed_pack_and_never_prints_the_key(
        no_network, monkeypatch, capsys):
    sent = []

    def fake(url, headers, body, timeout):
        sent.append(json.loads(body))
        refusal = {"status": "completed", "output": [{"type": "message", "content": [
            {"type": "refusal", "refusal": "no"}]}]}
        return 200, json.dumps(refusal).encode()
    monkeypatch.setattr(toa, "_urllib_transport", fake)
    monkeypatch.setenv(toa.CREDENTIAL_ENV, FAKE_KEY)
    assert H.main(["--provider", "openai", "--allow-network", "--case", "direction-en"]) == 0
    out = capsys.readouterr()
    assert FAKE_KEY not in out.out + out.err
    assert len(sent) == 1 and sent[0]["store"] is False and sent[0]["model"] == "gpt-6-sol"
    case = next(c for c in H.load_pack()["cases"] if c["case_id"] == "direction-en")
    assert json.loads(sent[0]["input"])["sources"][0]["text"] == case["sources"][0]


def test_harness_accepts_no_file_project_session_or_free_input():
    options = {s for a in H.build_parser()._actions for s in a.option_strings}
    assert options == {"-h", "--help", "--provider", "--allow-network", "--case",
                       "--show-proposals", "--managed-credential"}
    with pytest.raises(SystemExit):
        H.build_parser().parse_args(["--pack", "x.json"])
    with pytest.raises(SystemExit):
        H.build_parser().parse_args(["some-project-export.json"])


def test_unknown_case_id_is_refused(no_network):
    assert H.main(["--case", "rec_42"]) == 2
