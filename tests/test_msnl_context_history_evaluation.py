"""R2 context-and-history evaluation — the frozen candidate, holdout and harness.

Network-free: every reply comes from a fake transport, nothing is sent and
nothing here is a model result. Pins the preregistration and its ordering
before the cases, the frozen instructions, the 120 blind-labelled synthetic
cases and their constructed counterfactuals, the exact request body, the
fail-closed cost reservation, the two-axis decision and grounding, every
falsification criterion (symmetric: unjustified progress AND rejection of
legitimate new information), every INVALID path and the closed run gate.
"""
import collections
import hashlib
import json
import os

import pytest

from engine import technical_orchestration_openai as toa
from tests.test_msnl_llm_eval_harness import h, _reply

PREREG_SHA256 = "d8896785bb84713fa54c8b59fcfdb30c8f71af9251e5ef4d45f9f20c6267a8c2"
MANIFEST_SHA256 = "bcdf6e3ea610bdac0acbb9d099bc35d5ea5473fbdbda56465365fcdaaabda847"
INSTRUCTIONS_SHA256 = "440fd58ed38a221e17524abf8396637d7ca23df2ba921e4a07a46ee2b9873c51"
POSITIVE = ("NEW_DETAIL", "PLAIN_LANGUAGE_DETAIL", "RESTATE_THEN_NEW", "AMENDMENT",
            "HISTORY_COUNTERFACTUAL_NEW")
NEGATIVE = ("PARAPHRASE_OF_PREVIOUS", "CONTENT_FREE_REFERENCE", "UNKNOWN_OR_UNDECIDED",
            "OTHER_INVENTION_SHARED_VOCAB", "PROJECT_COUNTERFACTUAL")


@pytest.fixture(scope="module")
def manifest():
    return h.context_history_manifest()


def _usage(inp=900, out=120):
    return {"input_tokens": inp, "output_tokens": out,
            "output_tokens_details": {"reasoning_tokens": 40}, "total_tokens": inp + out}


def _wrap(obj, model="gpt-6-sol", usage=None, status=200, tier="default"):
    status, raw = _reply(obj, status=status)
    body = json.loads(raw.decode("utf-8"))
    body.update(model=model, usage=_usage() if usage is None else usage, service_tier=tier)
    return status, json.dumps(body).encode("utf-8")


def _refusal():
    status, raw = _reply({}, refusal=True)
    body = json.loads(raw.decode("utf-8"))
    body.update(model="gpt-6-sol", usage=_usage(), service_tier="default")
    return status, json.dumps(body).encode("utf-8")


class Fake:
    """Answers each request from its case; ``decide(case)`` returns the reply
    object (or a full (status, raw) pair)."""

    def __init__(self, manifest, decide):
        self.by_input = {json.dumps({f: c[f] for f in h.CH_INPUT_FIELDS}, ensure_ascii=False,
                                    sort_keys=True): c for c in manifest["cases"]}
        assert len(self.by_input) == len(manifest["cases"])
        self.decide, self.bodies = decide, []

    def __call__(self, url, headers, body, timeout):
        assert url == toa.ENDPOINT and "Authorization" not in headers
        payload = json.loads(body.decode("utf-8"))
        self.bodies.append(payload)
        out = self.decide(self.by_input[payload["input"]])
        return out if isinstance(out, tuple) else _wrap(out)


def _quote(case):
    return " ".join(case["current_answer"].split()[:4])


def _expected(case):
    """A reply that is always right on both axes, with a grounded quote."""
    s = case["slot_label"]
    contribution = s["new_contribution"] or "CONTENT_BEARING"
    return {"project_relation": s["project_relation"], "new_contribution": contribution,
            "possible_amendment": s["possible_amendment"],
            "evidence_quote": _quote(case) if contribution == "CONTENT_BEARING" else ""}


def _run(manifest, decide):
    fake = Fake(manifest, decide)
    adapter = h.OpenAIMsnlAdapter(allow_network=True, transport=fake)
    stop, rows, spend = h.context_history_run(adapter, manifest)
    return h.context_history_report(manifest, stop, rows, spend), fake


def _first(manifest, category):
    return next(c for c in h.ch_ordered(manifest)
                if c["category"] == category and not c["label_disputed"])


def _overriding(target, reply):
    return lambda c: reply if c["case_id"] == target["case_id"] else _expected(c)


# ─── preregistration and freezing order ───────────────────────────────────────

def test_the_preregistration_manifest_and_instructions_are_pinned(manifest):
    assert h.CONTEXT_HISTORY_PREREG_SHA256 == PREREG_SHA256
    assert h.CONTEXT_HISTORY_MANIFEST_SHA256 == MANIFEST_SHA256
    for path, digest in ((h.CONTEXT_HISTORY_PREREG_PATH, PREREG_SHA256),
                         (h.CONTEXT_HISTORY_MANIFEST_PATH, MANIFEST_SHA256)):
        assert hashlib.sha256(open(path, "rb").read()).hexdigest() == digest
    prereg = json.load(open(h.CONTEXT_HISTORY_PREREG_PATH, encoding="utf-8"))
    assert manifest["candidate"] == prereg["candidate"]
    assert manifest["candidate"]["instructions_sha256"] == INSTRUCTIONS_SHA256 == \
        hashlib.sha256(manifest["candidate"]["instructions"].encode("utf-8")).hexdigest()
    # The gate may be open ONLY for the one authorized run, i.e. while no evidence of it
    # exists; once the evidence exists it must be closed again.
    assert isinstance(h.CONTEXT_HISTORY_RUN_AUTHORIZED, bool)
    if os.path.exists(h.CONTEXT_HISTORY_REPORT_PATH) or os.path.exists(h.CONTEXT_HISTORY_JOURNAL_PATH):
        assert h.CONTEXT_HISTORY_RUN_AUTHORIZED is False
    assert "NOT AUTHORIZED TO RUN" in manifest["status"]
    assert manifest["budget"]["max_provider_requests"] == prereg["run_plan"]["max_provider_requests"] == 120
    assert manifest["budget"]["cost_ceiling_usd"] == prereg["run_plan"]["cost_ceiling_usd"] == 6.0
    assert manifest["budget"]["max_output_tokens"] == prereg["run_plan"]["max_output_tokens"] == 2000


def test_the_instructions_name_both_axes_and_the_amendment_rule_and_no_case(manifest):
    text = manifest["candidate"]["instructions"]
    for phrase in ("project_relation", "new_contribution", "possible_amendment", "evidence_quote",
                   "never, on its own, a reason for UNRELATED", "It never changes project_relation",
                   "proves nothing", "Do not judge whether the design is good"):
        assert phrase in text, phrase
    for c in manifest["cases"]:                      # written before any case existed
        assert c["current_answer"] not in text and c["original_idea"] not in text
    schema = manifest["candidate"]["output_schema"]
    assert schema["required"] == list(h.CH_FIELDS) and schema["additionalProperties"] is False
    assert schema["properties"]["project_relation"]["enum"] == list(h.CH_RELATIONS)
    assert schema["properties"]["new_contribution"]["enum"] == list(h.CH_CONTRIBUTIONS)


def test_the_annotation_records_the_order_independence_and_limits(manifest):
    a = manifest["annotation"]
    assert PREREG_SHA256 in a["preregistration_order"]
    assert a["authored_sha256"] in a["preregistration_order"]
    for key in ("method", "label_agreement", "disagreement_resolution", "independence_limits",
                "human_native_speaker_review", "edited_after_authoring"):
        assert a.get(key), key
    assert "NOT PERFORMED" in a["human_native_speaker_review"]
    assert "same model family" in a["independence_limits"]
    assert a["edited_after_authoring"].startswith("none")


# ─── the holdout ──────────────────────────────────────────────────────────────

def test_the_holdout_is_balanced_bilingual_and_covers_every_category(manifest):
    cases = manifest["cases"]
    assert len(cases) == 120 and sorted(c["request_index"] for c in cases) == list(range(1, 121))
    assert collections.Counter(c["category"] for c in cases) == {k: 12 for k in POSITIVE + NEGATIVE}
    assert collections.Counter(c["side"] for c in cases) == {"positive": 60, "negative": 60}
    assert collections.Counter(c["variety"] for c in cases) == {"en": 60, "ar-msa": 60}
    assert collections.Counter(c["domain"] for c in cases) == {"mechanical": 60,
                                                               "electronics_electrical": 60}
    for c in cases:
        assert (c["side"] == "positive") == (c["category"] in POSITIVE)
        expected = manifest["categories"][c["category"]]
        assert c["slot_label"] == {k: expected[k] for k in ("project_relation", "new_contribution",
                                                            "possible_amendment")}
    assert len({(c["original_idea"], c["preceding_answer"], c["current_answer"]) for c in cases}) == 120
    text = " ".join(c["current_answer"] + " " + c["original_idea"] for c in cases).lower()
    for word in ("wheelchair", "bicycle", "watering", "enclosure", "fridge", "refrigerator",
                 "wringer", "overshoe"):
        assert word not in text, word


def test_the_counterfactuals_reuse_exact_authored_text(manifest):
    by = {c["case_id"]: c for c in manifest["cases"]}
    projects = {p["project_id"]: p for p in manifest["projects"]}
    partners = manifest["partners"]
    for c in manifest["cases"]:
        p = projects[c["project_id"]]
        v = c["variety"]
        assert c["original_idea"] == p["idea"][v]
        if c["category"] == "HISTORY_COUNTERFACTUAL_NEW":
            twin = by[c["case_id"].replace("-C05-", "-C06-")]
            assert twin["category"] == "PARAPHRASE_OF_PREVIOUS"
            assert c["current_answer"] == twin["current_answer"]
            assert c["preceding_answer"] == p["preceding_answer_B"][v] != twin["preceding_answer"]
        elif c["category"] == "PROJECT_COUNTERFACTUAL":
            partner = partners[c["project_id"]]
            src = by["%s-C01-%s" % (partner, v)]
            assert src["category"] == "NEW_DETAIL" and c["current_answer"] == src["current_answer"]
            assert projects[partner]["domain"] == p["domain"] and partner != c["project_id"]
            assert c["preceding_answer"] == p["preceding_answer_A"][v]
        else:
            assert c["preceding_answer"] == p["preceding_answer_A"][v]


def test_disputed_labels_are_flagged_excluded_and_within_the_preregistered_limit(manifest):
    disputed = []
    for c in manifest["cases"]:
        b, s = c["blind_label"], c["slot_label"]
        rel = b["project_relation"] != s["project_relation"]
        con = s["project_relation"] == "RELATED" and b["new_contribution"] != s["new_contribution"]
        assert c["label_disputed"] == (rel or con), c["case_id"]
        if c["label_disputed"]:
            disputed.append(c["case_id"])
    assert len(disputed) <= 12                                  # PREPARATION_INVALID otherwise
    per = collections.Counter(c["category"] for c in manifest["cases"] if not c["label_disputed"])
    assert min(per[k] for k in POSITIVE + NEGATIVE) >= 8
    assert ("Disputed: " + (", ".join(disputed) if disputed else "none")) in \
        manifest["annotation"]["disagreement_resolution"]


def test_served_questions_are_the_committed_questions(manifest):
    from engine.idea_state import MECHANISM_COMPLETENESS as MC
    from engine.path_n_questions import get_served_question
    arabic = {c["question_id"]: c["served_question"]
              for c in h._load(h.MECHANISM_PACK_PATH, h.MECHANISM_PACK_SHA256)["cases"]
              if c["variety"] == "ar-msa"}
    for c in manifest["cases"]:
        q = get_served_question(MC, c["served_index"], domain=c["domain"])
        assert q.question_id == c["question_id"]
        assert c["served_question"] == (" ".join(q.text.split()) if c["variety"] == "en"
                                        else arabic[c["question_id"]])


# ─── the request and the cost bound ───────────────────────────────────────────

def test_the_request_carries_only_the_four_texts(manifest):
    c = h.ch_ordered(manifest)[0]
    payload = h.ch_payload(manifest, c)
    assert set(payload) == {"model", "instructions", "input", "store", "max_output_tokens", "text"}
    assert payload["store"] is False and payload["max_output_tokens"] == 2000
    assert set(json.loads(payload["input"])) == set(h.CH_INPUT_FIELDS)
    for c in manifest["cases"]:
        body = json.dumps(h.ch_payload(manifest, c), ensure_ascii=False)
        for leak in (c["case_id"], c["category"], "slot_label", "blind_label", "label_disputed"):
            assert leak not in body
    assert payload["text"]["format"]["strict"] is True


def test_reservations_are_bounded_recomputed_and_under_the_ceiling(manifest):
    b = manifest["budget"]
    res = [round(h.ch_reservation_usd(manifest, h.ch_payload(manifest, c)), 6)
           for c in h.ch_ordered(manifest)]
    assert res == b["reservations_usd_by_request_index"]
    assert round(sum(res), 6) == b["worst_case_reserved_usd_total"] < b["cost_ceiling_usd"]
    for c in h.ch_ordered(manifest):
        payload = h.ch_payload(manifest, c)
        assert h.pc_input_token_bound(manifest, payload) == \
            len(json.dumps(payload, ensure_ascii=False).encode("utf-8")) + 1000
    assert b["pricing"]["input_usd_per_1m"] == 2.0 and b["pricing"]["output_usd_per_1m"] == 10.0


# ─── the decision ─────────────────────────────────────────────────────────────

def test_the_two_axes_are_decided_independently_and_grounded():
    a = "The clip slides along the rail and a small spring pushes it back."
    rep = lambda r, n, q, amend=False: {"project_relation": r, "new_contribution": n,  # noqa: E731
                                        "possible_amendment": amend, "evidence_quote": q}
    d = h.ch_decision(a, rep("RELATED", "CONTENT_BEARING", "a small spring pushes it back"))
    assert d["progress_eligible"] and d["new_contribution"] == "CONTENT_BEARING"
    assert h.ch_decision(a, rep("RELATED", "CONTENT_BEARING", "not in it"))["new_contribution"] == \
        h.CH_UNGROUNDED
    assert not h.ch_decision(a, rep("RELATED", "CONTENT_BEARING", ""))["progress_eligible"]
    assert not h.ch_decision(a, rep("UNRELATED", "CONTENT_BEARING", "the clip"))["progress_eligible"]
    assert not h.ch_decision(a, rep("UNCERTAIN", "CONTENT_BEARING", "the clip"))["progress_eligible"]
    assert h.ch_decision(a, rep("RELATED", "NO_NEW_CONTENT", "the clip"))["new_contribution"] == \
        h.CH_UNGROUNDED
    d = h.ch_decision(a, rep("RELATED", "CONTENT_BEARING", "The clip slides", amend=True))
    assert d["progress_eligible"] and d["possible_amendment"] is True     # disclosure, not a veto


# ─── outcomes ─────────────────────────────────────────────────────────────────

def test_a_perfect_candidate_is_not_falsified(manifest):
    report, fake = _run(manifest, _expected)
    assert report["outcome"] == [h.CH_NOT_FALSIFIED] and report["stop"] is None
    assert len(fake.bodies) == 120 and report["untested_cases"] == []
    o = report["measures"]["overall"]
    assert o["M-UP"][0] == o["M-LR"][0] == o["M-ABST"][0] == o["M-FLIP"][0] == 0
    undisputed = [c for c in manifest["cases"] if not c["label_disputed"]]
    assert o["M-UP"][1] == sum(c["side"] == "negative" for c in undisputed)
    assert o["M-LR"][1] == sum(c["side"] == "positive" for c in undisputed)


@pytest.mark.parametrize("category, wrong, criterion", [
    ("PARAPHRASE_OF_PREVIOUS", ("RELATED", "CONTENT_BEARING"), h.CH_F1),
    ("CONTENT_FREE_REFERENCE", ("RELATED", "CONTENT_BEARING"), h.CH_F1),
    ("UNKNOWN_OR_UNDECIDED", ("RELATED", "CONTENT_BEARING"), h.CH_F1),
    ("OTHER_INVENTION_SHARED_VOCAB", ("RELATED", "CONTENT_BEARING"), h.CH_F1),
    ("PROJECT_COUNTERFACTUAL", ("RELATED", "CONTENT_BEARING"), h.CH_F1),
    ("NEW_DETAIL", ("RELATED", "NO_NEW_CONTENT"), h.CH_F2),
    ("PLAIN_LANGUAGE_DETAIL", ("RELATED", "NO_NEW_CONTENT"), h.CH_F2),
    ("HISTORY_COUNTERFACTUAL_NEW", ("RELATED", "NO_NEW_CONTENT"), h.CH_F2),
    ("RESTATE_THEN_NEW", ("RELATED", "NO_NEW_CONTENT"), h.CH_F2),
    ("UNKNOWN_OR_UNDECIDED", ("UNRELATED", "NO_NEW_CONTENT"), h.CH_F4),
])
def test_one_wrong_case_falsifies_and_the_run_still_measures_every_case(manifest, category, wrong,
                                                                        criterion):
    target = _first(manifest, category)
    quote = _quote(target) if wrong[1] == "CONTENT_BEARING" else ""
    reply = {"project_relation": wrong[0], "new_contribution": wrong[1],
             "possible_amendment": False, "evidence_quote": quote}
    report, fake = _run(manifest, _overriding(target, reply))
    assert criterion in report["outcome"] and report["stop"] is None
    assert len(fake.bodies) == 120 and report["untested_cases"] == []      # no early stop


def test_an_amendment_judged_unrelated_falsifies_twice(manifest):
    """The #950 failure shape: a design change must never make an answer unrelated."""
    target = _first(manifest, "AMENDMENT")
    reply = {"project_relation": "UNRELATED", "new_contribution": "CONTENT_BEARING",
             "possible_amendment": True, "evidence_quote": _quote(target)}
    report, _ = _run(manifest, _overriding(target, reply))
    assert report["outcome"] == [h.CH_F2, h.CH_F4]


def test_an_ungrounded_positive_is_a_rejection_and_a_missed_amendment_flag_is_only_reported(manifest):
    target = _first(manifest, "NEW_DETAIL")
    reply = {"project_relation": "RELATED", "new_contribution": "CONTENT_BEARING",
             "possible_amendment": False, "evidence_quote": "words that are not in the answer"}
    report, _ = _run(manifest, _overriding(target, reply))
    assert report["outcome"] == [h.CH_F2]
    target = _first(manifest, "AMENDMENT")
    reply = dict(_expected(target), possible_amendment=False)
    report, _ = _run(manifest, _overriding(target, reply))
    assert report["outcome"] == [h.CH_NOT_FALSIFIED]
    recall = report["measures"]["overall"]["M-AMEND-recall"]
    assert recall[0] == recall[1] - 1


def test_abstention_on_positives_is_tolerated_up_to_three(manifest):
    positives = [c for c in h.ch_ordered(manifest) if c["side"] == "positive" and not c["label_disputed"]]

    def abstain(n):
        ids = {c["case_id"] for c in positives[:n]}
        return lambda c: ({"project_relation": "RELATED", "new_contribution": "UNCERTAIN",
                           "possible_amendment": False, "evidence_quote": ""}
                          if c["case_id"] in ids else _expected(c))
    report, _ = _run(manifest, abstain(3))
    assert h.CH_F3 not in report["outcome"] and h.CH_F2 not in report["outcome"]
    report, _ = _run(manifest, abstain(4))
    assert report["outcome"] == [h.CH_F3]


def test_a_disputed_case_is_never_scored(manifest):
    """This holdout has no disputed case; a copy with one marked disputed shows
    that such a case is excluded from every measure, whatever the reply."""
    copy_ = json.loads(json.dumps(manifest))
    target = _first(copy_, "CONTENT_FREE_REFERENCE")
    target["label_disputed"] = True
    wrong = {"project_relation": "RELATED", "new_contribution": "CONTENT_BEARING",
             "possible_amendment": False, "evidence_quote": _quote(target)}
    report, _ = _run(copy_, _overriding(target, wrong))
    assert report["outcome"] == [h.CH_NOT_FALSIFIED]
    assert report["excluded_disputed"] == [target["case_id"]]
    assert report["measures"]["overall"]["M-UP"][1] == 59


# ─── INVALID paths ────────────────────────────────────────────────────────────

@pytest.mark.parametrize("reply, reason", [
    (lambda c: _refusal(), "refusal"),
    (lambda c: {"project_relation": "RELATED"}, toa.ERR_MALFORMED),
    (lambda c: dict(_expected(c), new_contribution="MAYBE"), toa.ERR_MALFORMED),
    (lambda c: dict(_expected(c), possible_amendment="no"), toa.ERR_MALFORMED),
    (lambda c: _wrap(_expected(c), model="gpt-4o"), h.ERR_MODEL_UNCONFIRMED),
    (lambda c: _wrap(_expected(c), tier="flex"), h.ERR_SERVICE_TIER),
    (lambda c: _wrap(_expected(c), usage={"input_tokens": 10}), h.ERR_USAGE_UNKNOWN),
    (lambda c: _wrap(_expected(c), usage=_usage(out=2001)), h.ERR_COST_UNBOUNDED),
    (lambda c: _wrap(_expected(c), usage=_usage(inp=10 ** 6)), h.ERR_INPUT_BOUND),
])
def test_every_invalid_path_stops_at_the_first_request_without_retry(manifest, reply, reason):
    report, fake = _run(manifest, reply)
    assert report["outcome"] == h.CH_INVALID and report["stop"]["reason"] == reason
    assert len(fake.bodies) == 1 and len(report["untested_cases"]) == 120


def test_the_ceiling_and_allocation_refuse_before_sending(manifest):
    tight = json.loads(json.dumps(manifest))
    tight["budget"]["cost_ceiling_usd"] = 0.01
    report, fake = _run(tight, _expected)
    assert report["stop"]["reason"] == h.ERR_COST_CEILING and fake.bodies == []
    short = json.loads(json.dumps(manifest))
    short["budget"]["max_provider_requests"] = 5
    report, fake = _run(short, _expected)
    assert report["stop"]["reason"] == h.ERR_BUDGET and len(fake.bodies) == 5
    assert report["outcome"] == h.CH_INVALID


def test_journal_and_report_keep_no_case_text_or_quote(manifest, tmp_path):
    path = tmp_path / "journal.jsonl"
    fake = Fake(manifest, _expected)
    adapter = h.OpenAIMsnlAdapter(allow_network=True, transport=fake)
    with open(path, "w", encoding="utf-8") as journal:
        stop, rows, spend = h.context_history_run(adapter, manifest, journal)
    report = json.dumps(h.context_history_report(manifest, stop, rows, spend), ensure_ascii=False)
    for text in (path.read_text(encoding="utf-8"), report):
        assert manifest["candidate"]["instructions"][:60] not in text
        assert "evidence_quote" not in text
        for c in manifest["cases"]:
            for field in h.CH_INPUT_FIELDS:
                assert c[field] not in text


# ─── the closed gate ──────────────────────────────────────────────────────────

def test_the_run_is_refused_while_not_authorized_and_sends_nothing(monkeypatch):
    monkeypatch.setattr(h, "CONTEXT_HISTORY_RUN_AUTHORIZED", False)

    def boom(*a, **k):
        raise AssertionError("no adapter may be built")
    monkeypatch.setattr(h, "OpenAIMsnlAdapter", boom)
    out = h.context_history_evaluation("openai", True, True)
    assert out["provider_requests"] == 0 and "not authorized" in out["refused"]
    plan = h.context_history_evaluation("lexical", False, False)
    assert plan["cases"] == 120 and plan["worst_case_reserved_usd"] < plan["ceiling_usd"]
    assert h.main(["--context-history-evaluation", "--provider", "openai"]) == 2
    assert h.main(["--context-history-evaluation", "--project-context-falsification"]) == 2


def test_the_authorized_path_writes_exclusive_evidence_once(manifest, monkeypatch, tmp_path):
    """With the gate opened ONLY inside this test, a fake transport and a temporary
    evidence directory: one run writes journal and report; a second is refused."""
    real = h.OpenAIMsnlAdapter
    monkeypatch.setattr(h, "CONTEXT_HISTORY_RUN_AUTHORIZED", True)
    monkeypatch.setattr(h, "CONTEXT_HISTORY_EVIDENCE_DIR", str(tmp_path))
    monkeypatch.setattr(h, "CONTEXT_HISTORY_JOURNAL_PATH", str(tmp_path / "journal.jsonl"))
    monkeypatch.setattr(h, "CONTEXT_HISTORY_REPORT_PATH", str(tmp_path / "report.json"))
    fake = Fake(manifest, _expected)
    monkeypatch.setattr(h, "OpenAIMsnlAdapter",
                        lambda allow_network=False: real(allow_network=allow_network, transport=fake))
    with pytest.raises(SystemExit):
        h.context_history_evaluation("openai", True, False)
    out = h.context_history_evaluation("openai", True, True)
    assert out["outcome"] == [h.CH_NOT_FALSIFIED] and out["provider_requests"] == 120
    journal = [json.loads(line) for line in (tmp_path / "journal.jsonl").read_text().splitlines()]
    assert [e["event"] for e in journal] == ["start"] + ["reserved", "attempt"] * 120 + ["end"]
    again = h.context_history_evaluation("openai", True, True)
    assert "already exists" in again["refused"] and again["provider_requests"] == 0
    assert len(fake.bodies) == 120


def test_a_null_reply_is_invalid_never_skipped(manifest):
    """Review M1: a JSON null reply (schema-valid JSON, no object) stops the run
    INVALID at once; no case is ever silently left unscored."""
    report, fake = _run(manifest, lambda c: _wrap(None))
    assert report["outcome"] == h.CH_INVALID and report["stop"]["reason"] == toa.ERR_MALFORMED
    assert len(fake.bodies) == 1 and len(report["untested_cases"]) == 120


def test_an_incomplete_measurement_is_never_a_verdict(manifest):
    report = h.context_history_report(manifest, None, [], {"requests_sent": 0})
    assert report["outcome"] == h.CH_INVALID and len(report["untested_cases"]) == 120


def test_uncertain_with_a_quote_is_an_abstention_not_a_rejection(manifest):
    """Review N1: the preregistration counts UNCERTAIN on either axis as an
    abstention, whatever its quote; it is never progress."""
    target = _first(manifest, "NEW_DETAIL")
    reply = {"project_relation": "RELATED", "new_contribution": "UNCERTAIN",
             "possible_amendment": False, "evidence_quote": _quote(target)}
    report, _ = _run(manifest, _overriding(target, reply))
    o = report["measures"]["overall"]
    assert report["outcome"] == [h.CH_NOT_FALSIFIED]
    assert (o["M-ABST"][0], o["M-LR"][0], o["M-UP"][0]) == (1, 0, 0)
    target = _first(manifest, "PLAIN_LANGUAGE_DETAIL")
    reply = dict(reply, new_contribution="NO_NEW_CONTENT")
    report, _ = _run(manifest, _overriding(target, reply))
    assert report["outcome"] == [h.CH_F2]


# ─── the ONE authorized run's evidence (2026-11-10) ───────────────────────────

def _recorded():
    with open(h.CONTEXT_HISTORY_REPORT_PATH, encoding="utf-8") as fh:
        report = json.load(fh)
    with open(h.CONTEXT_HISTORY_JOURNAL_PATH, encoding="utf-8") as fh:
        journal = [json.loads(line) for line in fh]
    return report, journal


def test_the_recorded_run_is_internally_consistent_and_the_gate_is_closed(manifest):
    """The committed report recomputes from its own rows, agrees with the fsynced
    journal and stayed inside the authorization: gpt-6-sol, Standard tier, at most
    120 requests, under US$6, no retry, no restart, frozen order."""
    assert h.CONTEXT_HISTORY_RUN_AUTHORIZED is False
    report, journal = _recorded()
    assert report == json.loads(json.dumps(h.context_history_report(
        manifest, report["stop"], report["rows"], report["spend"]), sort_keys=True))
    attempts = [e for e in journal if e["event"] == "attempt"]
    n = len(attempts)
    assert journal[0] == {"event": "start", "manifest_sha256": MANIFEST_SHA256,
                          "model": "gpt-6-sol", "ceiling_usd": 6.0}
    assert [e["event"] for e in journal] == ["start"] + ["reserved", "attempt"] * n + ["end"]
    assert [a["attempt"] for a in attempts] == list(range(1, n + 1))
    order = [c["case_id"] for c in h.ch_ordered(manifest)]
    assert [a["case_id"] for a in attempts] == order[:n] and n == report["spend"]["requests_sent"] <= 120
    for row, att in zip(report["rows"], attempts):
        assert row["case_id"] == att["case_id"] and row["attempt"]["attempt"] == att["attempt"]
        assert (row["error"], row["decision"]) == (att["error"], att["decision"])
        for key in ("usage", "measured_cost_usd", "response_id", "model", "service_tier",
                    "input_token_bound", "reserved_usd", "http_status", "sent"):
            assert row["attempt"][key] == att[key], key
    ok = attempts[:-1]
    assert all(a["error"] is None and a["http_status"] == 200 for a in ok)
    assert {a["model"] for a in ok} == {"gpt-6-sol"} and {a["service_tier"] for a in ok} == {"default"}
    assert all(a["usage"]["output_tokens"] <= 2000 and a["usage"]["input_tokens"] <= a["input_token_bound"]
               for a in ok)
    total = sum(a["measured_cost_usd"] for a in ok)
    assert abs(total - report["spend"]["measured_cost_usd"]) < 1e-6 and total < 6.0
    assert journal[-1]["outcome"] == report["outcome"]


def test_the_recorded_outcome_is_invalid_by_one_transport_failure_without_retry(manifest):
    report, journal = _recorded()
    attempts = [e for e in journal if e["event"] == "attempt"]
    assert report["outcome"] == h.CH_INVALID
    assert report["stop"] == {"reason": toa.ERR_TRANSPORT, "case_id": "CH2-C05-ar-msa"}
    last = attempts[-1]
    assert (last["attempt"], last["case_id"], last["error"], last["sent"]) == \
        (118, "CH2-C05-ar-msa", toa.ERR_TRANSPORT, True)
    assert last["decision"] is None and last["measured_cost_usd"] is None
    # never retried, never filled: the failed case and the two never sent stay untested
    order = [c["case_id"] for c in h.ch_ordered(manifest)]
    assert report["untested_cases"] == order[117:] == ["CH2-C05-ar-msa", "CH6-C04-ar-msa",
                                                      "CH3-C07-ar-msa"]
    assert sum(1 for a in attempts if a["case_id"] == "CH2-C05-ar-msa") == 1
    # the committed bound charges the failed request its full reservation
    assert abs(report["spend"]["committed_bound_usd"]
               - (report["spend"]["measured_cost_usd"] + last["reserved_usd"])) < 1e-6
    # INVALID: no criterion is evaluated, whatever the scored rows show
    assert h.CH_F1 not in report["outcome"] and h.CH_NOT_FALSIFIED not in report["outcome"]


def test_a_second_invocation_is_refused_and_sends_nothing(monkeypatch):
    def boom(*a, **k):
        raise AssertionError("no adapter may be built")
    monkeypatch.setattr(h, "OpenAIMsnlAdapter", boom)
    out = h.context_history_evaluation("openai", True, True)          # the gate is closed
    assert out["provider_requests"] == 0 and "not authorized" in out["refused"]
    monkeypatch.setattr(h, "CONTEXT_HISTORY_RUN_AUTHORIZED", True)    # even if reopened
    out = h.context_history_evaluation("openai", True, True)
    assert out["provider_requests"] == 0 and "already exists" in out["refused"]


def test_the_evidence_keeps_no_case_text_quote_instructions_or_raw_reply(manifest):
    texts = [open(p, encoding="utf-8").read() for p in (h.CONTEXT_HISTORY_REPORT_PATH,
                                                        h.CONTEXT_HISTORY_JOURNAL_PATH)]
    for text in texts:
        assert manifest["candidate"]["instructions"][:60] not in text
        assert "evidence_quote" not in text and "Authorization" not in text
        for c in manifest["cases"]:
            for field in h.CH_INPUT_FIELDS:
                assert c[field] not in text
