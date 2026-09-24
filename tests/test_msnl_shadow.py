"""MSNL local-only shadow — Candidate 01.

File-creation contract:
  Path: tests/test_msnl_shadow.py
  Purpose: prove the local-only shadow seam of `engine/msnl_shadow.py`: the
    immutable, source-bound contracts; the closed registry vocabulary; the two
    local adapters and the local policy; and that the web CAPTURE seam fires
    exactly once per newly committed accepted answer / correction, never on a
    refused, failed or duplicate event, never from replay, and never changes an
    engine, gap, maturity, ledger or acknowledgement outcome.
  Input contract: the live web app + durable store (conftest per-test DB
    isolation) and synthetic answers copied from the existing R4 correction
    suite. No real user data; no network; no provider.
  Output contract: pass/fail evidence only.
  Prohibited behaviors: no claim of semantic precision, paraphrase coverage or
    extension rate — the lexical baseline is an UNCALIBRATED registered-surface
    detector, exercised here only to prove the harness mechanics.
"""
import ast
import dataclasses
import pathlib
import re

import pytest

import web.app as webapp
from web.app import app, SESSION_STORE
from engine import msnl_shadow as ms
from engine import semantic_registry
from engine.idea_state import MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY
from engine.record_store import StoreError
from engine.session_reconstruction import reconstruct_readonly_state
from tests.csrf_client import csrf_client

ROOT = pathlib.Path(__file__).resolve().parents[1]

ELEC_IDEA = "ESP32 microcontroller circuit with a voltage sensor"
PROBLEM_ANSWER = (
    "The problem is that cyclists have no reliable brake light. My circuit senses "
    "deceleration with an accelerometer because sudden voltage change on the sensor "
    "indicates braking, so the microcontroller switches the LED because riders "
    "behind need warning.")
MECH_STRONG = (
    "The mechanism works because the accelerometer outputs a voltage proportional "
    "to deceleration; the microcontroller reads it through the ADC and drives the "
    "LED through a transistor because the LED current exceeds the GPIO limit.")
MECH_CORRECTED = (
    "The mechanism is different: there is no accelerometer at all. A reed switch on "
    "the brake lever closes the circuit because the lever movement moves a magnet, "
    "which causes the microcontroller to switch the LED through a transistor.")


# ─────────────────────────────────────────────────────────────────────────────
# helpers
# ─────────────────────────────────────────────────────────────────────────────

@pytest.fixture
def client():
    app.config["TESTING"] = True
    return csrf_client(app)


@pytest.fixture
def captured(monkeypatch):
    """Enable the switch and inject an in-memory collector as the sink."""
    events = []
    monkeypatch.setattr(ms, "MSNL_CAPTURE_ENABLED", True)
    monkeypatch.setattr(ms, "_capture_sink", events.append)
    return events


def _token(client, sid):
    body = client.get("/session/" + sid).get_data(as_text=True)
    m = re.search(r'name="answer_token" value="([^"]+)"', body)
    return m.group(1) if m else None


def _answer(client, sid, response, token=None, action="answered"):
    return client.post("/session/" + sid, data={
        "response": response, "action": action,
        "answer_token": token or _token(client, sid)})


def _correct(client, sid, record_id, response, token=None):
    return client.post("/session/" + sid + "/correct", data={
        "supersedes_record_id": record_id, "response": response,
        "answer_token": token or _token(client, sid)})


def _new_project(client):
    r = client.post("/start", data={"idea": ELEC_IDEA,
                                    "domain_confirm": "electronics_electrical"})
    assert r.status_code == 302
    return r.headers["Location"].rsplit("/", 1)[-1]


def _start(client, answers=(PROBLEM_ANSWER, MECH_STRONG)):
    sid = _new_project(client)
    for a in answers:
        assert _answer(client, sid, a).status_code == 302
    return sid


def _ledger(sid):
    return tuple(webapp._get_store().load_contract(sid).assertions)


def _ledger_facts(sid):
    """Durable ledger content comparable across two projects (ids excluded)."""
    return tuple((r.disposition, r.content, r.gap_context, r.question_target,
                  r.provenance, r.validation_status, r.quality)
                 for r in _ledger(sid))


def _progress(state):
    return (state.maturity_level, state.current_stage,
            tuple(sorted((g.gap_type, g.status, g.closed_at) for g in state.gaps)),
            getattr(getattr(state, "known_mechanism", None), "content", None),
            getattr(getattr(state, "known_problem", None), "content", None),
            len(state.acknowledged_unknowns))


def _event(**over):
    fields = dict(ref=ms.LocalRef("project-1", "rec-1"),
                  accepted_text="The process has three steps.",
                  gap_type=MECHANISM_COMPLETENESS, question_target="Q",
                  domain="electronics_electrical", kind=ms.EVENT_ANSWERED)
    fields.update(over)
    return ms.AcceptedEvent(**fields)


class _Stub:
    name = "stub"

    def __init__(self, reply):
        self.reply = reply

    def propose(self, request):
        if isinstance(self.reply, Exception):
            raise self.reply
        return self.reply


# ─────────────────────────────────────────────────────────────────────────────
# 1–7 — contracts, closed vocabulary, adapters, local policy
# ─────────────────────────────────────────────────────────────────────────────

class TestContracts:

    def test_observation_request_response_and_result_are_immutable(self):
        event = _event()
        request = ms.build_request(event)
        response = ms.ShadowResponse(ms.ABSTAIN)
        result = ms.evaluate(event, ms.NullAdapter())
        for obj, field in ((event.ref, "record_id"), (event, "accepted_text"),
                           (request, "accepted_text"), (request.candidates[0], "concept_id"),
                           (response, "outcome"), (result, "disposition")):
            with pytest.raises(dataclasses.FrozenInstanceError):
                setattr(obj, field, "changed")
        assert isinstance(request.candidates, tuple)

    @pytest.mark.parametrize("over", [
        {"accepted_text": ""}, {"accepted_text": None}, {"gap_type": "NOT_A_GAP"},
        {"question_target": 7}, {"domain": ""}, {"domain": None}, {"kind": "OTHER"},
        {"kind": ms.EVENT_ANSWERED, "correction_status": ms.CORRECTION_APPLIED},
        {"kind": ms.EVENT_CORRECTION},
        {"kind": ms.EVENT_CORRECTION, "correction_status": "MAYBE"},
        {"ref": ("project-1", "rec-1")},
    ])
    def test_invalid_observation_is_refused(self, over):
        with pytest.raises(ValueError):
            _event(**over)

    def test_local_ref_is_project_scoped(self):
        with pytest.raises(ValueError):
            ms.LocalRef("", "rec-1")
        with pytest.raises(ValueError):
            ms.LocalRef("project-1", "")
        assert ms.LocalRef("a", "rec-1") != ms.LocalRef("b", "rec-1")

    @pytest.mark.parametrize("target", ["", 0, b"Q", ("Q",)])
    def test_question_target_must_be_none_or_non_empty_text(self, target):
        # R1: the durable record contract — None or a non-empty string.
        with pytest.raises(ValueError):
            _event(question_target=target)

    @pytest.mark.parametrize("target", [None, "PATHN:N-MC-2", " padded "])
    def test_valid_question_target_is_kept_verbatim(self, target):
        assert _event(question_target=target).question_target == target

    def test_genuinely_absent_gap_and_target_are_allowed(self):
        event = _event(gap_type=None, question_target=None)
        assert ms.build_request(event).candidates == ()

    def test_request_carries_no_identifier_or_project_context(self):
        event = _event(ref=ms.LocalRef("sid-SECRET-123", "rec-SECRET-456"))
        request = ms.build_request(event)
        assert {f.name for f in dataclasses.fields(request)} == {
            "accepted_text", "gap_type", "question_target", "domain",
            "candidates", "schema_version"}
        assert "SECRET" not in repr(request)
        assert request.schema_version == ms.SHADOW_SCHEMA_VERSION
        assert "lang" not in repr(dataclasses.fields(request))

    def test_response_carries_no_correlation_rationale_or_timestamp(self):
        assert {f.name for f in dataclasses.fields(ms.ShadowResponse)} == {
            "outcome", "concept_ids", "confidence"}


class TestClosedVocabulary:

    @pytest.mark.parametrize("gap", semantic_registry.GOVERNED_OWNERS)
    def test_candidates_are_the_registry_concepts_of_the_served_gap_only(self, gap):
        cands = ms.candidate_concepts(gap)
        expected = [(c.concept_id, c.provenance) for c in semantic_registry.CONCEPTS
                    if c.owner == gap]
        assert [(c.concept_id, c.provenance) for c in cands] == expected
        assert cands, "precondition: every governed gap owns concepts"
        others = {c.concept_id for c in semantic_registry.CONCEPTS if c.owner != gap}
        assert not ({c.concept_id for c in cands} & others)

    @pytest.mark.parametrize("gap", [None, "", "NOT_A_GAP", 3])
    def test_unknown_or_absent_gap_has_no_candidates(self, gap):
        assert ms.candidate_concepts(gap) == ()

    def test_caller_supplied_inventory_is_refused(self):
        forged = (ms.CandidateConcept("MC-INVENTED", "made up"),)
        cross = ms.candidate_concepts(PHYSICAL_FEASIBILITY)
        for candidates in (forged, cross, ()):
            with pytest.raises(ValueError):
                ms.ShadowRequest("text", MECHANISM_COMPLETENESS, None,
                                 "electronics_electrical", candidates)

    def test_registry_is_not_changed_by_the_shadow(self):
        before = tuple(semantic_registry.CONCEPTS)
        ms.evaluate(_event(), ms.LexicalBaselineAdapter())
        assert tuple(semantic_registry.CONCEPTS) == before


class TestResponseRules:

    def test_proposed_requires_non_empty_ids(self):
        with pytest.raises(ValueError):
            ms.ShadowResponse(ms.PROPOSED, ())
        assert ms.ShadowResponse(ms.PROPOSED, ("MC-STEP",)).concept_ids == ("MC-STEP",)

    @pytest.mark.parametrize("outcome", [ms.ABSTAIN, ms.NO_MAPPING, ms.ERROR])
    def test_non_proposals_require_empty_ids(self, outcome):
        assert ms.ShadowResponse(outcome).concept_ids == ()
        with pytest.raises(ValueError):
            ms.ShadowResponse(outcome, ("MC-STEP",))

    @pytest.mark.parametrize("bad", [
        {"outcome": "MAYBE"}, {"outcome": ms.PROPOSED, "concept_ids": ["MC-STEP"]},
        {"outcome": ms.PROPOSED, "concept_ids": ("MC-STEP", "MC-STEP")},
        {"outcome": ms.PROPOSED, "concept_ids": (1,)},
        # R2: an empty-string id is refused by the response contract itself
        {"outcome": ms.PROPOSED, "concept_ids": ("",)},
        {"outcome": ms.PROPOSED, "concept_ids": ("MC-STEP", "")},
    ])
    def test_malformed_response_is_refused(self, bad):
        with pytest.raises(ValueError):
            ms.ShadowResponse(**bad)

    @pytest.mark.parametrize("ids", [
        ("MC-INVENTED",),                       # not in the registry at all
        ("PF-PRINCIPLE",),                      # a real id owned by ANOTHER gap
        ("MC-STEP", "MC-INVENTED"),             # one bad id poisons the proposal
    ])
    def test_unsupported_or_out_of_gap_ids_are_discarded(self, ids):
        result = ms.evaluate(_event(), _Stub(ms.ShadowResponse(ms.PROPOSED, ids)))
        assert result.disposition == ms.DISPOSITION_DISCARDED_UNSUPPORTED
        assert result.concept_ids == ()

    def test_confidence_has_no_authority(self):
        high = ms.evaluate(_event(), _Stub(ms.ShadowResponse(
            ms.PROPOSED, ("PF-PRINCIPLE",), confidence=0.99)))
        assert high.disposition == ms.DISPOSITION_DISCARDED_UNSUPPORTED
        low = ms.evaluate(_event(), _Stub(ms.ShadowResponse(
            ms.PROPOSED, ("MC-STEP",), confidence=0.01)))
        assert low.disposition == ms.DISPOSITION_PROPOSAL
        assert not hasattr(low, "confidence")

    @pytest.mark.parametrize("reply", [
        RuntimeError("adapter blew up"), None, {"outcome": "PROPOSED"},
        ms.ShadowResponse(ms.ERROR)])
    def test_adapter_failure_is_isolated_as_error(self, reply):
        result = ms.evaluate(_event(), _Stub(reply))
        assert (result.outcome, result.disposition, result.concept_ids) == (
            ms.ERROR, ms.DISPOSITION_ADAPTER_ERROR, ())

    def test_result_is_correlated_locally_not_by_the_adapter(self):
        ref = ms.LocalRef("project-9", "rec-9")
        assert ms.evaluate(_event(ref=ref), ms.NullAdapter()).ref == ref


class TestAdapters:

    def test_null_adapter_abstains(self):
        response = ms.NullAdapter().propose(ms.build_request(_event()))
        assert (response.outcome, response.concept_ids) == (ms.ABSTAIN, ())
        result = ms.evaluate(_event(), ms.NullAdapter())
        assert result.disposition == ms.DISPOSITION_ABSTAINED

    def test_lexical_baseline_returns_registered_hits_without_confidence(self):
        text = "The process has three steps."
        response = ms.LexicalBaselineAdapter().propose(ms.build_request(
            _event(accepted_text=text)))
        assert response.outcome == ms.PROPOSED
        assert response.confidence is None
        assert set(response.concept_ids) == semantic_registry.activated_concepts(
            text, MECHANISM_COMPLETENESS)
        result = ms.evaluate(_event(accepted_text=text), ms.LexicalBaselineAdapter())
        assert result.disposition == ms.DISPOSITION_PROPOSAL
        assert result.adapter_name == "lexical-baseline-uncalibrated"

    def test_lexical_baseline_no_hit_and_no_gap_are_no_mapping(self):
        for event in (_event(accepted_text="The enclosure is blue."),
                      _event(gap_type=None)):
            result = ms.evaluate(event, ms.LexicalBaselineAdapter())
            assert result.disposition == ms.DISPOSITION_NO_MAPPING

    def test_a_registered_hit_is_not_an_owner_assertion(self):
        # Negation still carries the registered surface: the baseline detects
        # lexical occurrence, not an affirmatively asserted fact.
        result = ms.evaluate(_event(accepted_text="There are no steps at all."),
                             ms.LexicalBaselineAdapter())
        assert "MC-STEP" in result.concept_ids


class TestCaptureSeamUnit:

    def test_switch_is_off_by_default_and_the_default_sink_discards(self):
        assert ms.MSNL_CAPTURE_ENABLED is False
        assert ms._capture_sink is ms._discard
        assert ms._discard(_event()) is None

    def test_disabled_capture_reaches_no_sink(self, monkeypatch):
        seen = []
        monkeypatch.setattr(ms, "_capture_sink", seen.append)
        ms.capture_accepted_event(project_ref="p", record_id="r", accepted_text="x",
                                  gap_type=None, question_target=None,
                                  domain="electronics_electrical",
                                  kind=ms.EVENT_ANSWERED)
        assert seen == []

    def test_invalid_event_or_failing_sink_never_raises(self, monkeypatch, captured):
        assert ms.capture_accepted_event(
            project_ref="p", record_id="r", accepted_text="", gap_type=None,
            question_target=None, domain="d", kind=ms.EVENT_ANSWERED) is None
        assert captured == []

        def boom(event):
            raise RuntimeError("sink failed")
        monkeypatch.setattr(ms, "_capture_sink", boom)
        assert ms.capture_accepted_event(
            project_ref="p", record_id="r", accepted_text="x", gap_type=None,
            question_target=None, domain="d", kind=ms.EVENT_ANSWERED) is None


# ─────────────────────────────────────────────────────────────────────────────
# 8–11 — the ordinary-answer capture point
# ─────────────────────────────────────────────────────────────────────────────

class TestAnswerCapture:

    def test_start_seed_is_not_captured(self, client, captured):
        _new_project(client)
        assert captured == []

    def test_one_new_durable_answer_is_captured_exactly_once(self, client, captured):
        sid = _start(client, answers=(PROBLEM_ANSWER,))
        captured.clear()
        before = len(_ledger(sid))
        targeted = webapp.select_next_gap(SESSION_STORE[sid]["state"])
        assert _answer(client, sid, "   " + MECH_STRONG + "  \n").status_code == 302
        ledger = _ledger(sid)
        assert len(ledger) == before + 1
        assert len(captured) == 1
        event, record = captured[0], ledger[-1]
        assert event.ref == ms.LocalRef(sid, record.record_id)
        assert event.accepted_text == MECH_STRONG == record.content   # post-strip text
        assert event.kind == ms.EVENT_ANSWERED and event.correction_status is None
        assert event.gap_type == record.gap_context == targeted
        assert event.question_target == record.question_target
        assert event.domain == "electronics_electrical"

    def test_confirmed_duplicate_is_not_captured_again(self, client, captured):
        sid = _start(client, answers=(PROBLEM_ANSWER,))
        captured.clear()
        token = _token(client, sid)
        assert _answer(client, sid, MECH_STRONG, token=token).status_code == 302
        before = len(_ledger(sid))
        assert _answer(client, sid, MECH_STRONG, token=token).status_code == 302
        assert len(_ledger(sid)) == before, "precondition: the retry was a no-op"
        assert len(captured) == 1

    def test_rejected_and_non_answer_posts_are_not_captured(self, client, captured):
        sid = _start(client, answers=(PROBLEM_ANSWER,))
        captured.clear()
        before = len(_ledger(sid))
        _answer(client, sid, "")                                         # empty
        assert _answer(client, sid, "x" * (webapp.MAX_FREE_TEXT_CHARS + 1)
                       ).status_code == 400                              # over-length
        _answer(client, sid, MECH_STRONG, token="forged-token")          # refused
        _answer(client, sid, "I do not know yet.", action="unknown")     # metadata only
        assert len(_ledger(sid)) == before + 1, "precondition: only the unknown note saved"
        assert captured == []

    def test_durable_failure_is_not_captured(self, client, captured, monkeypatch):
        sid = _start(client, answers=(PROBLEM_ANSWER,))
        captured.clear()
        before = len(_ledger(sid))

        def unavailable(*a, **k):
            raise StoreError("unavailable")
        monkeypatch.setattr(webapp._get_store(), "append_record", unavailable)
        _answer(client, sid, MECH_STRONG)
        monkeypatch.undo()
        assert SESSION_STORE[sid].get("_answer_error") == webapp.ANSWER_NOT_SAVED_MESSAGE
        assert len(_ledger(sid)) == before
        assert captured == []

    @pytest.mark.parametrize("where", ["seam", "sink"])
    def test_capture_failure_leaves_the_answer_outcome_unchanged(
            self, client, monkeypatch, where):
        baseline_client = csrf_client(app)
        base_sid = _start(baseline_client)

        def boom(*a, **k):
            raise RuntimeError("capture failed")
        if where == "seam":
            monkeypatch.setattr(ms, "capture_accepted_event", boom)
        else:
            monkeypatch.setattr(ms, "MSNL_CAPTURE_ENABLED", True)
            monkeypatch.setattr(ms, "_capture_sink", boom)
        sid = _new_project(client)
        assert _answer(client, sid, PROBLEM_ANSWER).status_code == 302
        r = _answer(client, sid, MECH_STRONG)
        assert r.status_code == 302 and r.headers["Location"].endswith("/session/" + sid)
        entry = SESSION_STORE[sid]
        assert entry.get("_answer_error") is None
        assert entry.get("_answer_accepted") is True
        assert _progress(entry["state"]) == _progress(SESSION_STORE[base_sid]["state"])
        assert _ledger_facts(sid) == _ledger_facts(base_sid)


# ─────────────────────────────────────────────────────────────────────────────
# 12–15 — the correction capture points
# ─────────────────────────────────────────────────────────────────────────────

class TestCorrectionCapture:

    def test_applied_correction_is_captured_once_with_inherited_context(
            self, client, captured):
        sid = _start(client)
        target = _ledger(sid)[-1]
        assert target.question_target is not None, "precondition: a real target"
        captured.clear()
        assert _correct(client, sid, target.record_id, MECH_CORRECTED).status_code == 302
        assert SESSION_STORE[sid]["_interaction_ack"] == webapp.CORRECTION_APPLIED_ACK
        new = _ledger(sid)[-1]
        assert len(captured) == 1
        event = captured[0]
        assert event.ref == ms.LocalRef(sid, new.record_id)
        assert (event.kind, event.correction_status) == (
            ms.EVENT_CORRECTION, ms.CORRECTION_APPLIED)
        assert event.accepted_text == MECH_CORRECTED == new.content
        assert event.gap_type == target.gap_context == new.gap_context
        # inherited verbatim — never re-resolved from the current question
        assert event.question_target == target.question_target == new.question_target
        assert event.domain == "electronics_electrical"

    @pytest.mark.parametrize("failure", ["reconstruction", "reattachment"])
    def test_saved_not_applied_correction_is_captured_once(
            self, client, captured, monkeypatch, failure):
        sid = _start(client)
        target = _ledger(sid)[-1]
        live_before = _progress(SESSION_STORE[sid]["state"])
        captured.clear()
        token = _token(client, sid)     # rendered before the failure is injected
        if failure == "reconstruction":
            def boom(*a, **k):
                raise RuntimeError("replay unavailable")
            monkeypatch.setattr(webapp, "reconstruct_readonly_state", boom)
        else:
            monkeypatch.setattr(webapp, "_attach_quantity_history", lambda *a: False)
        assert _correct(client, sid, target.record_id, MECH_CORRECTED,
                        token=token).status_code == 302
        assert (SESSION_STORE[sid]["_answer_error"]
                == webapp.CORRECTION_SAVED_NOT_YET_APPLIED_MESSAGE)
        assert _progress(SESSION_STORE[sid]["state"]) == live_before
        assert len(captured) == 1
        event = captured[0]
        assert (event.kind, event.correction_status) == (
            ms.EVENT_CORRECTION, ms.CORRECTION_SAVED_NOT_APPLIED)
        assert event.ref == ms.LocalRef(sid, _ledger(sid)[-1].record_id)
        assert event.question_target == target.question_target
        # the same correction resubmitted is an idempotent duplicate: no capture
        SESSION_STORE[sid].pop("_answer_error", None)
        before = len(_ledger(sid))
        assert _correct(client, sid, target.record_id, MECH_CORRECTED,
                        token=token).status_code == 302
        assert len(_ledger(sid)) == before, "precondition: duplicate was a no-op"
        assert len(captured) == 1

    def test_rejected_and_failed_corrections_are_not_captured(
            self, client, captured, monkeypatch):
        sid = _start(client)
        target = _ledger(sid)[-1]
        captured.clear()
        _correct(client, sid, "no-such-record", MECH_CORRECTED)          # unknown target
        _correct(client, sid, target.record_id, "")                       # incomplete
        client.post("/session/" + sid + "/correct", data={                # bad token
            "supersedes_record_id": target.record_id, "response": MECH_CORRECTED,
            "answer_token": "forged"})

        def unavailable(*a, **k):
            raise StoreError("unavailable")
        monkeypatch.setattr(webapp._get_store(), "append_record", unavailable)
        _correct(client, sid, target.record_id, MECH_CORRECTED)          # durable failure
        monkeypatch.undo()
        assert _ledger(sid)[-1].record_id == target.record_id
        assert captured == []

    def test_superseded_target_is_rejected_without_capture(self, client, captured):
        sid = _start(client)
        target = _ledger(sid)[-1]
        captured.clear()
        assert _correct(client, sid, target.record_id, MECH_CORRECTED).status_code == 302
        assert len(captured) == 1
        _correct(client, sid, target.record_id, MECH_CORRECTED + " Again.")
        assert len(captured) == 1


# ─────────────────────────────────────────────────────────────────────────────
# 16–18 — replay isolation, no-effect, import/call isolation
# ─────────────────────────────────────────────────────────────────────────────

_AUTHORITATIVE = ("engine/progression_loop.py", "engine/gap_relevance.py",
                  "engine/semantic_registry.py", "engine/intent_serving.py",
                  "engine/answer_stance.py", "engine/session_reconstruction.py")


def _imported_modules(path):
    tree = ast.parse((ROOT / path).read_text(encoding="utf-8"))
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            base = node.module or ""
            names.add(base)
            names.update(base + "." + a.name for a in node.names)
    return names


class TestIsolation:

    def test_replay_never_invokes_msnl(self, client, captured, monkeypatch):
        sid = _start(client)
        target = _ledger(sid)[-1]
        assert _correct(client, sid, target.record_id, MECH_CORRECTED).status_code == 302
        captured.clear()

        def forbidden(*a, **k):
            raise AssertionError("MSNL reached from replay")
        for name in ("capture_accepted_event", "evaluate", "build_request"):
            monkeypatch.setattr(ms, name, forbidden)
        monkeypatch.setattr(ms, "_capture_sink", forbidden)
        recon = reconstruct_readonly_state(webapp._get_store(), sid)
        assert recon.review.level == 1 and recon.state is not None
        assert captured == []

    @pytest.mark.parametrize("path", _AUTHORITATIVE)
    def test_authoritative_engine_modules_have_no_msnl_edge(self, path):
        assert not any("msnl" in n for n in _imported_modules(path)), path
        assert "msnl" not in (ROOT / path).read_text(encoding="utf-8").lower(), path

    def test_shadow_module_imports_only_the_registry(self):
        imported = _imported_modules("engine/msnl_shadow.py")
        assert "engine.ai_advisor" not in imported
        allowed = {"dataclasses", "dataclasses.dataclass", "engine.semantic_registry",
                   "engine.semantic_registry.CONCEPTS",
                   "engine.semantic_registry.GOVERNED_OWNERS",
                   "engine.semantic_registry.activated_concepts"}
        assert imported <= allowed, imported - allowed

    def test_web_reaches_only_the_capture_seam(self):
        source = (ROOT / "web/app.py").read_text(encoding="utf-8")
        uses = set(re.findall(r"_msnl_shadow\.(\w+)", source))
        assert uses == {"capture_accepted_event", "EVENT_ANSWERED", "EVENT_CORRECTION",
                        "CORRECTION_APPLIED", "CORRECTION_SAVED_NOT_APPLIED"}, uses
        assert "from engine.msnl_shadow" not in source

    def test_ai_advisor_stays_pinned_off(self):
        from engine.ai_advisor import AI_ADVISORY_ENABLED
        assert AI_ADVISORY_ENABLED is False

    def test_capture_on_and_off_give_identical_product_outcomes(self, monkeypatch):
        def journey():
            c = csrf_client(app)
            sid = _start(c)
            target = _ledger(sid)[-1]
            assert _correct(c, sid, target.record_id, MECH_CORRECTED).status_code == 302
            entry = SESSION_STORE[sid]
            return (_progress(entry["state"]), _ledger_facts(sid),
                    entry.get("_interaction_ack"), entry.get("_answer_error"))

        off = journey()
        events = []
        monkeypatch.setattr(ms, "MSNL_CAPTURE_ENABLED", True)
        monkeypatch.setattr(ms, "_capture_sink", events.append)
        on = journey()
        assert len(events) == 3, "precondition: two answers + one correction captured"
        assert on == off
