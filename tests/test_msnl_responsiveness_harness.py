"""T2-G / R2 responsiveness campaign — network-free harness contract tests.

Covers the `--responsiveness` path of `scripts/run_msnl_eval.py` over the
frozen `tests/fixtures/msnl_responsiveness_v1.json`. Every provider path uses
an injected fake transport: hosted CI never reaches the network. These tests
pin that the harness executes the FROZEN arm (instructions, input fields,
verdict enum, grounding rule, thresholds, budget) exactly, stops at the first
error, and scores every criterion at case grain; they do not evaluate a model.
"""
import json

import pytest

from engine import technical_orchestration_openai as toa
from tests.test_msnl_llm_eval_harness import FakeTransport, _reply, h


@pytest.fixture(scope="module")
def pack():
    return h._load(h.RESPONSIVENESS_PACK_PATH, h.RESPONSIVENESS_PACK_SHA256)


def _rows(pack, decide):
    """Per-case rows exactly as the campaign builds them, from decide(case)."""
    rows = []
    for case in pack["cases"]:
        verdict, quote = decide(case)
        rows.append({"case_id": case["case_id"], "verdict": verdict, "quote": quote,
                     "grounded": h.quote_grounded(quote, case["text"]),
                     "accepted": h.responsiveness_accepted(verdict, quote, case["text"]),
                     "error": None})
    return rows


def _two_words(text):
    return " ".join(text.split()[:3])


def _perfect(case):
    if case["label"] == "RESPONSIVE":
        return "RESPONSIVE", _two_words(case["text"])
    return "NOT_RESPONSIVE", ""


class OracleTransport:
    """Answers every request from the case it carries, via ``decide``; can
    fail at request number ``fail_at`` (1-based) with ``failure``."""

    def __init__(self, pack, decide=_perfect, fail_at=None, failure=None):
        self.by_text = {c["text"]: c for c in pack["cases"]}
        self.decide, self.fail_at, self.failure = decide, fail_at, failure
        self.calls = []

    def __call__(self, url, headers, body, timeout):
        payload = json.loads(body.decode("utf-8"))
        self.calls.append((url, headers, payload))
        if self.fail_at is not None and len(self.calls) == self.fail_at:
            return self.failure
        case = self.by_text[json.loads(payload["input"])["answer"]]
        verdict, quote = self.decide(case)
        return _reply({"verdict": verdict, "quote": quote})


def _adapter(transport):
    return h.OpenAIMsnlAdapter(allow_network=True, transport=transport)


# ─── the frozen arm, executed exactly ───────────────────────────────────────

def test_the_payload_carries_the_frozen_arm_and_nothing_else(pack):
    case = pack["cases"][0]
    payload = h.responsiveness_payload(pack, case)
    assert payload["instructions"] == pack["arm"]["instructions"]
    assert json.loads(payload["input"]) == {"question": case["served_question"],
                                            "answer": case["text"]}
    schema = payload["text"]["format"]["schema"]
    assert schema["properties"]["verdict"]["enum"] == \
        pack["arm"]["output_schema"]["verdict"]
    assert set(schema["required"]) == {"verdict", "quote"}
    assert schema["additionalProperties"] is False
    assert payload["store"] is False and payload["model"] == toa.MODEL
    for forbidden in ("case_id", "category", "label", "domain", "gap_type", "question_id"):
        assert forbidden not in payload["input"], forbidden


def test_requests_go_only_to_the_approved_endpoint_without_a_credential(pack):
    transport = FakeTransport(_reply({"verdict": "NOT_RESPONSIVE", "quote": ""}))
    verdict, quote, err = h.classify_responsiveness(_adapter(transport), pack,
                                                    pack["cases"][0])
    assert (verdict, quote, err) == ("NOT_RESPONSIVE", "", None)
    url, headers, _ = transport.calls[0]
    assert url == toa.ENDPOINT and set(headers) == {"Content-Type"}


def test_the_adapter_stays_off_without_network_permission(pack):
    adapter = h.OpenAIMsnlAdapter(allow_network=False, transport=FakeTransport())
    assert h.classify_responsiveness(adapter, pack, pack["cases"][0])[2] == \
        toa.ERR_NETWORK_NOT_ALLOWED


# ─── acceptance rule: grounding ─────────────────────────────────────────────

def test_grounding_follows_the_frozen_acceptance_rule():
    text = "أبي   الغطاء يسكر لحاله لما أشيل رجلي"
    assert h.quote_grounded("الغطاء يسكر", text)
    assert h.quote_grounded("ابي الغطاء", text)            # normalize_ar on both sides
    assert h.quote_grounded("أبي الغطاء  يسكر", text)       # whitespace collapsed
    assert not h.quote_grounded("الغطاء", text)             # one word-character run
    assert not h.quote_grounded("الغطاء يفتح", text)        # not a substring
    assert not h.quote_grounded(None, text)
    assert not h.quote_grounded("", text)
    assert h.quote_grounded("lid closes", "The lid closes by itself.")
    assert not h.quote_grounded("Lid Closes", "The lid closes by itself.")  # verbatim case


def test_only_a_grounded_responsive_verdict_is_accepted():
    text = "The lid closes by itself when I lift my foot."
    assert h.responsiveness_accepted("RESPONSIVE", "lid closes", text)
    assert not h.responsiveness_accepted("RESPONSIVE", "lid opens", text)
    assert not h.responsiveness_accepted("NOT_RESPONSIVE", "lid closes", text)
    assert not h.responsiveness_accepted("ABSTAIN", "lid closes", text)
    assert not h.responsiveness_accepted(None, None, text)


# ─── FR3 precondition and refusals before any request ───────────────────────

def test_every_case_meets_the_lexical_precondition(pack):
    assert h.responsiveness_precondition(pack) == []


def test_a_broken_precondition_sends_nothing(monkeypatch):
    import engine.gap_relevance as gr
    monkeypatch.setattr(gr, "addresses_gap", lambda text, gap: True)

    def no_network(*_a, **_k):
        raise AssertionError("nothing may be sent when FR3 fails")
    monkeypatch.setattr(toa, "_urllib_transport", no_network)
    out = h.responsiveness("openai", True, True)
    assert out["provider_requests"] == 0 and "refused" in out
    assert len(out["precondition_violations"]) == 152


def test_a_budget_inconsistent_with_the_pack_is_refused(monkeypatch, pack):
    broken = json.loads(json.dumps(pack))
    broken["thresholds"]["max_provider_requests"] = 457
    monkeypatch.setattr(h, "_load", lambda path, sha: broken)
    with pytest.raises(h.PackError):
        h.responsiveness("lexical", False, False)


def test_the_lexical_mode_only_checks_and_sends_nothing(monkeypatch, capsys):
    def no_network(*_a, **_k):
        raise AssertionError("the lexical mode sends nothing")
    monkeypatch.setattr(toa, "_urllib_transport", no_network)
    assert h.main(["--responsiveness"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["provider_requests"] == 0 and out["precondition_violations"] == []
    assert out["pack_sha256"] == h.RESPONSIVENESS_PACK_SHA256


@pytest.mark.parametrize("argv", [
    ["--responsiveness", "--provider", "openai"],
    ["--responsiveness", "--provider", "openai", "--allow-network"],
    ["--responsiveness", "--show-cases"],
    ["--responsiveness", "--rescore", "x.json"],
])
def test_the_campaign_is_refused_without_its_exact_options(argv, capsys):
    assert h.main(argv) == 2
    assert "refused" in json.loads(capsys.readouterr().out)


# ─── the campaign: three passes, budget, stop at first error ────────────────

def test_a_perfect_campaign_uses_exactly_the_budget_and_passes(pack):
    transport = OracleTransport(pack)
    runs, requests = h.responsiveness_campaign(_adapter(transport), pack)
    assert requests == len(transport.calls) == 456 == pack["thresholds"]["max_provider_requests"]
    assert [len(r) for r in runs] == [152, 152, 152]
    result = h.responsiveness_verdict(pack, runs, [])
    assert result["verdict"] == "PASS" and result["campaign_status"] == "COMPLETE"
    assert result["agreement"] == {"identical": 144, "cases": 144, "rate": 1.0}
    assert all(result["criteria_held_in_every_run"].values())


@pytest.mark.parametrize("failure,kind", [
    (_reply(None, refusal=True), h.ERR_REFUSAL),
    ((500, b""), toa.ERR_HTTP_STATUS),
    ((200, b"not json"), toa.ERR_MALFORMED),
    (_reply({"verdict": "RESPONSIVE", "quote": "x", "extra": 1}), toa.ERR_MALFORMED),
    (_reply({"verdict": "MAYBE", "quote": "x"}), toa.ERR_MALFORMED),
    ((200, json.dumps({"status": "incomplete"}).encode()), toa.ERR_INCOMPLETE),
])
def test_the_first_error_stops_the_campaign_and_invalidates_it(pack, failure, kind):
    transport = OracleTransport(pack, fail_at=170, failure=failure)
    runs, requests = h.responsiveness_campaign(_adapter(transport), pack)
    assert requests == len(transport.calls) == 170          # nothing after the error
    assert [len(r) for r in runs] == [152, 18]
    assert runs[1][-1]["error"] == kind
    result = h.responsiveness_verdict(pack, runs, [])
    assert result["campaign_status"] == "INVALID" and result["verdict"] == "FAIL"
    assert result["criteria_held_in_every_run"]["AB2"] is False
    assert result["runs"][1]["errors"] == [{"case_id": runs[1][-1]["case_id"], "kind": kind}]


def test_a_transport_exception_is_an_error_not_a_verdict(pack):
    def boom(*_a):
        raise OSError("down")
    runs, requests = h.responsiveness_campaign(_adapter(boom), pack)
    assert requests == 1 and runs[0][0]["error"] == toa.ERR_TRANSPORT


# ─── scoring: every frozen criterion at case grain ──────────────────────────

def _report(pack, decide):
    return h.responsiveness_run_report(pack, _rows(pack, decide))


def test_any_responsive_verdict_on_a_negative_is_a_false_acceptance(pack):
    target = next(c for c in pack["cases"] if c["category"] == "OFF_TOPIC"
                  and c["variety"] == "ar-egy")

    def decide(case):
        if case is target:
            return "RESPONSIVE", "not a quote from the text"   # ungrounded still counts
        return _perfect(case)
    rep = _report(pack, decide)
    assert rep["by_variety"]["ar-egy"]["false_acceptances"] == 1
    assert rep["by_variety"]["en"]["false_acceptances"] == 0
    assert rep["criteria"]["FA1"] is False


def test_injection_responsive_verdicts_fail_fa2(pack):
    def decide(case):
        if case["category"] == "INSTRUCTION_INJECTION" and case["variety"] == "en":
            return "RESPONSIVE", _two_words(case["text"])
        return _perfect(case)
    rep = _report(pack, decide)
    assert rep["by_variety"]["overall"]["injection_responsive"] == 4
    assert rep["criteria"]["FA2"] is False and rep["criteria"]["FA1"] is False


def test_ungrounded_responsive_targets_are_counted_and_never_accepted(pack):
    def decide(case):
        if case["label"] == "RESPONSIVE":
            return "RESPONSIVE", "words that are absent"
        return "NOT_RESPONSIVE", ""
    rep = _report(pack, decide)
    o = rep["by_variety"]["overall"]
    assert o["target_accepted"] == 0 and o["target_responsive_ungrounded"] == 48
    assert o["responsive_ungrounded"] == 56            # 48 targets + 8 controls
    assert rep["criteria"]["FR1"] is False


def _reject_first(pack, n_by_variety, verdict="NOT_RESPONSIVE"):
    """Reject the first n target cases of each variety; everything else perfect."""
    seen = {}
    chosen = set()
    for case in pack["cases"]:
        if case["category"] in h.TARGET_CATEGORIES:
            k = seen.get(case["variety"], 0)
            if k < n_by_variety.get(case["variety"], 0):
                chosen.add(case["case_id"])
            seen[case["variety"]] = k + 1

    def decide(case):
        if case["case_id"] in chosen:
            return verdict, ""
        return _perfect(case)
    return decide


def test_recovery_thresholds_are_the_frozen_ones(pack):
    # per variety: 9/12 = 0.75 holds, 8/12 does not
    assert _report(pack, _reject_first(pack, {"ar-egy": 3}))["criteria"]["FR1"] is True
    assert _report(pack, _reject_first(pack, {"ar-egy": 4}))["criteria"]["FR1"] is False
    # overall: 39/48 holds (>= 0.80), 38/48 does not
    ok = {"en": 1, "ar-msa": 3, "ar-gulf-kw": 3, "ar-egy": 2}          # 9 rejected
    bad = {"en": 2, "ar-msa": 3, "ar-gulf-kw": 3, "ar-egy": 2}         # 10 rejected
    assert _report(pack, _reject_first(pack, ok))["criteria"]["FR1"] is True
    assert _report(pack, _reject_first(pack, bad))["criteria"]["FR1"] is False


def test_language_parity_is_english_minus_each_arabic_variety(pack):
    one = _report(pack, _reject_first(pack, {"ar-msa": 1}))           # gap 1/12
    two = _report(pack, _reject_first(pack, {"ar-msa": 2}))           # gap 2/12
    assert one["criteria"]["FR2"] is True and two["criteria"]["FR2"] is False
    behind = _report(pack, _reject_first(pack, {"en": 2}))            # Arabic ahead
    assert behind["criteria"]["FR2"] is True


def test_abstention_threshold_counts_target_abstentions_only(pack):
    seven = {"en": 2, "ar-msa": 2, "ar-gulf-kw": 2, "ar-egy": 1}
    eight = {"en": 2, "ar-msa": 2, "ar-gulf-kw": 2, "ar-egy": 2}
    assert _report(pack, _reject_first(pack, seven, "ABSTAIN"))["criteria"]["AB1"] is True
    assert _report(pack, _reject_first(pack, eight, "ABSTAIN"))["criteria"]["AB1"] is False


def test_controls_are_reported_separately_and_never_counted(pack):
    def decide(case):
        if case["category"] in h.CONTROL_CATEGORIES:
            return "NOT_RESPONSIVE", ""
        return _perfect(case)
    rep = _report(pack, decide)
    assert rep["by_variety"]["overall"]["controls"]["rejected"] == 8
    assert all(rep["criteria"].values())


def test_agreement_is_over_non_control_cases_and_uses_the_frozen_minimum(pack):
    def flip(n):
        ids = [c["case_id"] for c in pack["cases"]
               if c["category"] in h.TARGET_CATEGORIES][:n]

        def decide(case):
            if case["case_id"] in ids:
                return "NOT_RESPONSIVE", ""
            return _perfect(case)
        return decide
    perfect = _rows(pack, _perfect)
    seven, eight = _rows(pack, flip(7)), _rows(pack, flip(8))
    a7 = h.responsiveness_agreement(pack, [perfect, perfect, seven])
    a8 = h.responsiveness_agreement(pack, [perfect, perfect, eight])
    assert (a7["identical"], a8["identical"]) == (137, 136)
    assert h.responsiveness_verdict(pack, [perfect, perfect, seven], [])[
        "criteria_held_in_every_run"]["ST1"] is True                    # 137/144 >= 0.95
    assert h.responsiveness_verdict(pack, [perfect, perfect, eight], [])[
        "criteria_held_in_every_run"]["ST1"] is False                   # 136/144 < 0.95


def test_fewer_than_three_runs_can_never_pass(pack):
    perfect = _rows(pack, _perfect)
    result = h.responsiveness_verdict(pack, [perfect, perfect], [])
    assert result["verdict"] == "FAIL" and result["campaign_status"] == "INVALID"
