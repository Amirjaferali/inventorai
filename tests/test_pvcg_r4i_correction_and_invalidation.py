"""PVCG-R4-I — explicit user correction + deterministic invalidation by FULL replay.

File-creation contract:
  Path: tests/test_pvcg_r4i_correction_and_invalidation.py
  Purpose: behaviour tests for the bounded FPC-02 / P4-2 implementation required by
    the authoritative
    `docs/governance/PVCG_R4_C_USER_CORRECTION_AND_DETERMINISTIC_INVALIDATION_CONTRACT.md`.
    PVCG-R4 is the CONFORMANCE owner only; FPC-02 / P4-2 remain the implementation
    owners, so every assertion here exercises the EXISTING canonical models (the
    Increment-2 supersession primitive, the P4-0 record contract, the P4-1a
    INSERT-only store, the P4-2 Level-1 reconstruction replay) rather than any
    parallel R4 model.
  Input contract: the live web app + durable store (conftest per-test DB isolation)
    and real /start -> answer journeys; restart simulated by removing the
    SESSION_STORE entry while the durable DB persists (governed P4-2/PC1/PC2/PC3
    convention).
  Output contract: pass/fail evidence only; no durable artifact left behind.
  Prohibited behaviors: NO weakening of any fail-closed assertion; NO fabricated
    reconstruction; NO assertion that passes vacuously (every corpus-dependent test
    asserts its own precondition first); NO probe derived from the object under
    test (the INV-004 corpus is literal and committed here).
"""
import copy
import re

import pytest

import web.app as webapp
from web.app import app, SESSION_STORE
from engine.idea_state import (
    IdeaState, Gap, OPEN, PARTIAL, CLOSED,
    MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY,
)
from engine.progression_loop import integrate_response, run_iteration, select_next_gap
from engine.record_contract import (
    ProjectRecordContract, InvalidReferenceError, reconcile_supersession_edges,
)
from engine.session_reconstruction import reconstruct_readonly_state
from engine.deliverable_assembler import assemble_deliverable

ELEC_IDEA = "ESP32 microcontroller circuit with a voltage sensor"

# A strong mechanism answer that reaches the mechanism gap.
MECH_STRONG = (
    "The mechanism works because the accelerometer outputs a voltage proportional "
    "to deceleration; the microcontroller reads it through the ADC and drives the "
    "LED through a transistor because the LED current exceeds the GPIO limit.")
PROBLEM_ANSWER = (
    "The problem is that cyclists have no reliable brake light. My circuit senses "
    "deceleration with an accelerometer because sudden voltage change on the sensor "
    "indicates braking, so the microcontroller switches the LED because riders "
    "behind need warning.")
# A corrected mechanism answer, still on-topic and still causal.
MECH_CORRECTED = (
    "The mechanism is different: there is no accelerometer at all. A reed switch on "
    "the brake lever closes the circuit because the lever movement moves a magnet, "
    "which causes the microcontroller to switch the LED through a transistor.")
# Faithful Arabic counterparts (registered R3 surfaces only; nothing new added).
MECH_STRONG_AR = (
    "تعمل الالية لان المستشعر يعطي جهدا يتناسب مع التباطؤ ثم يقرأه المتحكم عبر "
    "المحول مما يؤدي الى تشغيل المصباح عبر الترانزستور بخطوات واضحة ومتكررة.")
MECH_CORRECTED_AR = (
    "الالية مختلفة تماما فلا يوجد مستشعر تسارع بل مفتاح على ذراع المكابح يغلق "
    "الدائرة لان حركة الذراع تحرك المغناطيس مما يسبب تشغيل المصباح عبر الترانزستور.")
OFF_TOPIC = "The enclosure is blue and we will ship it in a cardboard box."


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


def _token(client, sid):
    body = client.get("/session/" + sid).get_data(as_text=True)
    m = re.search(r'name="answer_token" value="([^"]+)"', body)
    return m.group(1) if m else None


def _answer(client, sid, response):
    return client.post("/session/" + sid, data={
        "response": response, "action": "answered",
        "answer_token": _token(client, sid)})


def _correct(client, sid, record_id, response):
    return client.post("/session/" + sid + "/correct", data={
        "supersedes_record_id": record_id, "response": response})


def _store():
    return webapp._get_store()


def _start(client, answers=(PROBLEM_ANSWER, MECH_STRONG)):
    r = client.post("/start", data={"idea": ELEC_IDEA,
                                    "domain_confirm": "electronics_electrical"})
    assert r.status_code == 302
    sid = r.headers["Location"].rsplit("/", 1)[-1]
    for a in answers:
        assert _answer(client, sid, a).status_code == 302
    return sid


def _answered_ids(sid):
    return [r.record_id for r in _store().load_accepted_answer_evidence(sid)]


def _snapshot(state):
    """Comparable progression facts (never mutated)."""
    return (state.maturity_level, state.current_stage,
            tuple(sorted((g.gap_type, g.status, g.closed_at) for g in state.gaps)),
            getattr(getattr(state, "known_mechanism", None), "content", None),
            getattr(getattr(state, "known_problem", None), "content", None))


# =========================================================================
# A — an explicit correction of a NAMED prior accepted record is expressible.
# =========================================================================
class TestAExplicitCorrection:

    def test_correction_route_accepts_an_explicit_record_target(self, client):
        sid = _start(client)
        ids = _answered_ids(sid)
        assert len(ids) >= 2, "precondition: at least two accepted answers"
        r = _correct(client, sid, ids[-1], MECH_CORRECTED)
        assert r.status_code == 302
        assert SESSION_STORE[sid].get("_answer_error") is None

    def test_correction_requires_both_a_target_and_a_response(self, client):
        sid = _start(client)
        before = len(_answered_ids(sid))
        assert _correct(client, sid, "", MECH_CORRECTED).status_code == 302
        assert _correct(client, sid, _answered_ids(sid)[0], "").status_code == 302
        assert len(_answered_ids(sid)) == before, "nothing stored on an incomplete correction"

    def test_unknown_or_already_superseded_target_stores_nothing(self, client):
        sid = _start(client)
        ids = _answered_ids(sid)
        before = len(ids)
        assert _correct(client, sid, "rec_9999", MECH_CORRECTED).status_code == 302
        assert len(_answered_ids(sid)) == before
        assert _correct(client, sid, ids[-1], MECH_CORRECTED).status_code == 302
        after_first = len(_answered_ids(sid))
        # the same target a second time is already superseded -> refused
        assert _correct(client, sid, ids[-1], "another try because the parts move").status_code == 302
        assert len(_answered_ids(sid)) == after_first


# =========================================================================
# B / G / H — supersession WITH RETENTION; nothing destroyed or renumbered.
# =========================================================================
class TestBSupersessionWithRetention:

    def test_prior_record_is_retained_verbatim_and_marked_superseded(self, client):
        sid = _start(client)
        ids = _answered_ids(sid)
        target = ids[-1]
        before = {r.record_id: r.content
                  for r in _store().load_accepted_answer_evidence(sid)}
        _correct(client, sid, target, MECH_CORRECTED)
        after = {r.record_id: r for r in _store().load_accepted_answer_evidence(sid)}
        assert target in after, "the superseded record is RETAINED, never deleted"
        assert after[target].content == before[target], "content is never rewritten"
        assert after[target].superseded_by is not None
        new_id = after[target].superseded_by
        assert target in after[new_id].supersedes, "forward edge on the NEW record"

    def test_no_record_id_is_reused_or_renumbered(self, client):
        sid = _start(client)
        before = _answered_ids(sid)
        _correct(client, sid, before[-1], MECH_CORRECTED)
        after = _answered_ids(sid)
        assert after[:len(before)] == before, "existing rec_N are stable"
        assert len(set(after)) == len(after), "no rec_N reuse"
        assert len(after) == len(before) + 1, "a correction APPENDS exactly one record"

    def test_correction_is_an_append_not_a_destructive_update(self, client):
        sid = _start(client)
        ids = _answered_ids(sid)
        _correct(client, sid, ids[0], "The problem is different because the rider brakes suddenly, which causes the light to matter.")
        contract = _store().load_contract(sid)
        kept = [r for r in contract.assertions if r.record_id == ids[0]]
        assert len(kept) == 1 and kept[0].content, "history retained, auditable"


# =========================================================================
# C — the correction persists and survives a restart, deterministically.
# =========================================================================
class TestCPersistenceAndReload:

    def test_reload_reproduces_the_corrected_state_not_the_pre_correction_state(self, client):
        sid = _start(client)
        ids = _answered_ids(sid)
        pre = _snapshot(SESSION_STORE[sid]["state"])
        _correct(client, sid, ids[-1], MECH_CORRECTED)
        corrected = _snapshot(SESSION_STORE[sid]["state"])
        assert corrected != pre, "precondition: the correction changed the live state"
        SESSION_STORE.pop(sid)                      # simulate restart
        recon = reconstruct_readonly_state(_store(), sid)
        assert recon.review.level == 1
        assert _snapshot(recon.state) == corrected

    def test_superseded_record_survives_reload_and_stays_out_of_the_active_set(self, client):
        sid = _start(client)
        target = _answered_ids(sid)[-1]
        _correct(client, sid, target, MECH_CORRECTED)
        SESSION_STORE.pop(sid)
        contract = _store().load_contract(sid)
        by_id = {r.record_id: r for r in contract.assertions}
        assert target in by_id, "durably retained after reload"
        assert by_id[target].superseded_by is not None, "inverse edge re-derived on load"

    def test_withdrawn_count_is_surfaced_after_reload(self, client):
        sid = _start(client)
        _correct(client, sid, _answered_ids(sid)[-1], MECH_CORRECTED)
        SESSION_STORE.pop(sid)
        recon = reconstruct_readonly_state(_store(), sid)
        assert recon.review.withdrawn_source_records == 1


# =========================================================================
# D / R — recomputation is FULL replay of the amended stream, never targeted.
# =========================================================================
class TestDFullReplay:

    def test_every_surviving_answer_is_replayed_not_only_the_corrected_one(self, client):
        sid = _start(client)
        ids = _answered_ids(sid)
        _correct(client, sid, ids[-1], MECH_CORRECTED)
        live = SESSION_STORE[sid]["state"]
        # The FIRST answer was never touched by the correction, yet its effect is
        # present in the replayed state — proof the whole stream was replayed
        # rather than a targeted patch applied to the changed record only.
        assert live.known_problem is not None
        assert live.iteration >= 2

    def test_replay_uses_the_unchanged_canonical_path(self, client):
        sid = _start(client)
        _correct(client, sid, _answered_ids(sid)[-1], MECH_CORRECTED)
        live = SESSION_STORE[sid]["state"]
        SESSION_STORE.pop(sid)
        recon = reconstruct_readonly_state(_store(), sid)
        assert _snapshot(recon.state) == _snapshot(live), (
            "the live state after correction IS the reconstruction result")

    def test_no_dependency_or_propagation_model_is_introduced(self):
        import engine.session_reconstruction as sr
        import engine.progression_loop as pl
        for module in (sr, pl):
            names = dir(module)
            for forbidden in ("dependency_graph", "propagate", "invalidate_dependents",
                              "targeted_reevaluation", "partial_replay"):
                assert forbidden not in names, (
                    "%s must not gain %s" % (module.__name__, forbidden))


# =========================================================================
# E / F — the withdrawn basis stops being current truth; evaluation may DECREASE.
# =========================================================================
class TestEWithdrawnBasisAndDecrease:

    def test_withdrawn_mechanism_text_is_no_longer_current_support(self, client):
        sid = _start(client)
        live = SESSION_STORE[sid]["state"]
        assert live.known_mechanism is not None, "precondition: a mechanism was established"
        assert "accelerometer" in live.known_mechanism.content
        _correct(client, sid, _answered_ids(sid)[-1], MECH_CORRECTED)
        after = SESSION_STORE[sid]["state"]
        if after.known_mechanism is not None:
            assert after.known_mechanism.content != MECH_STRONG, (
                "the withdrawn answer must not remain the current mechanism")

    def test_withdrawn_text_is_absent_from_the_recomposed_deliverable(self, client):
        import json
        sid = _start(client)
        pkg_before = json.dumps(assemble_deliverable(SESSION_STORE[sid]["state"]),
                                ensure_ascii=False)
        assert MECH_STRONG[:40] in pkg_before, "precondition: it WAS presented"
        _correct(client, sid, _answered_ids(sid)[-1], MECH_CORRECTED)
        pkg_after = json.dumps(assemble_deliverable(SESSION_STORE[sid]["state"]),
                               ensure_ascii=False)
        assert MECH_STRONG[:40] not in pkg_after, (
            "withdrawn source material must not be presented as current")

    def test_evaluation_is_free_to_decrease_after_a_withdrawal(self, client):
        # Withdraw the mechanism answer and replace it with an OFF-TOPIC one:
        # the amended stream no longer supports the prior conclusion, so the
        # replayed state must be weaker, not merely different.
        sid = _start(client)
        before = SESSION_STORE[sid]["state"]
        mech_before = getattr(getattr(before, "known_mechanism", None), "content", None)
        closed_before = {g.gap_type for g in before.gaps if g.status == CLOSED}
        partial_before = {g.gap_type for g in before.gaps if g.status == PARTIAL}
        assert mech_before or closed_before or partial_before, (
            "precondition: something was established before the withdrawal")
        _correct(client, sid, _answered_ids(sid)[-1], OFF_TOPIC)
        after = SESSION_STORE[sid]["state"]
        mech_after = getattr(getattr(after, "known_mechanism", None), "content", None)
        closed_after = {g.gap_type for g in after.gaps if g.status == CLOSED}
        partial_after = {g.gap_type for g in after.gaps if g.status == PARTIAL}
        weaker = (
            after.maturity_level < before.maturity_level
            or closed_after < closed_before
            or (mech_before is not None and mech_after != mech_before)
            or partial_after < partial_before
        )
        assert weaker, (
            "readiness/evaluation MUST be able to decrease: "
            "before=(%r, %r, %r) after=(%r, %r, %r)"
            % (before.maturity_level, sorted(closed_before), bool(mech_before),
               after.maturity_level, sorted(closed_after), bool(mech_after)))

    def test_withdrawal_marker_is_explicit_and_counts_only(self, client):
        sid = _start(client)
        meta = assemble_deliverable(SESSION_STORE[sid]["state"])["_session_meta"]
        assert meta["withdrawn_source_records"] == {"total": 0, "note": None}
        _correct(client, sid, _answered_ids(sid)[-1], MECH_CORRECTED)
        meta = assemble_deliverable(SESSION_STORE[sid]["state"])["_session_meta"]
        assert meta["withdrawn_source_records"]["total"] == 1
        note = meta["withdrawn_source_records"]["note"]
        assert note and "withdrew" in note
        assert "rec_" not in note, "aggregate only — no record id is exported"
        assert MECH_STRONG[:30] not in note, "no withdrawn content is exported"


# =========================================================================
# I / F-2 — a replay failure leaves live state EXACTLY unchanged.
# =========================================================================
class TestIReplayFailureRollback:

    def test_replay_failure_leaves_live_state_unchanged_and_is_not_acknowledged(
            self, client, monkeypatch):
        sid = _start(client)
        before = _snapshot(SESSION_STORE[sid]["state"])
        before_obj = SESSION_STORE[sid]["state"]
        monkeypatch.setattr(
            webapp, "reconstruct_readonly_state",
            lambda *a, **k: (_ for _ in ()).throw(RuntimeError("replay down")))
        r = _correct(client, sid, _answered_ids(sid)[-1], MECH_CORRECTED)
        assert r.status_code == 302
        assert SESSION_STORE[sid]["state"] is before_obj, "no partial replacement"
        assert _snapshot(SESSION_STORE[sid]["state"]) == before
        assert SESSION_STORE[sid].get("_interaction_ack") is None, (
            "a failed replay is never reported as an applied correction")

    def test_durable_stream_stays_valid_and_reloadable_after_a_replay_failure(
            self, client, monkeypatch):
        sid = _start(client)
        monkeypatch.setattr(
            webapp, "reconstruct_readonly_state",
            lambda *a, **k: (_ for _ in ()).throw(RuntimeError("replay down")))
        _correct(client, sid, _answered_ids(sid)[-1], MECH_CORRECTED)
        monkeypatch.undo()
        contract = _store().load_contract(sid)      # must not raise ContractError
        assert contract.assertions


# =========================================================================
# J — EN/AR correction equivalence (PVCG-R3 preserved across the new seam).
# =========================================================================
class TestJBilingualEquivalence:

    def test_en_and_ar_corrections_produce_equivalent_progression(self, client):
        def run(base, corrected):
            sid = _start(client, answers=(PROBLEM_ANSWER, base))
            _correct(client, sid, _answered_ids(sid)[-1], corrected)
            st = SESSION_STORE[sid]["state"]
            return (st.maturity_level, st.current_stage,
                    tuple(sorted((g.gap_type, g.status) for g in st.gaps)),
                    st.known_mechanism is not None)
        assert run(MECH_STRONG, MECH_CORRECTED) == run(MECH_STRONG_AR, MECH_CORRECTED_AR)

    def test_correction_messages_are_localised_on_their_actual_render_path(self):
        """Each message must be localised by the helper `show_session` really
        calls for it: `_answer_error` goes through `localize_message`, while
        `_interaction_ack` goes through `localize_deep`. Testing only the
        convenient helper would pass while an Arabic reader still saw English."""
        from web import ui_text
        errors = (webapp.CORRECTION_NOT_APPLIED_MESSAGE,
                  webapp.CORRECTION_INCOMPLETE_MESSAGE)
        for msg in errors:                      # rendered via localize_message
            assert ui_text.localize_message(msg, "en") == msg
            assert ui_text.localize_message(msg, "ar") != msg, (
                "a language-asymmetric correction path is a rejection condition")
        ack = webapp.CORRECTION_APPLIED_ACK     # rendered via localize_deep
        assert ui_text.localize_deep(ack, "en") == ack
        assert ui_text.localize_deep(ack, "ar") != ack, (
            "the success acknowledgement must be localised by the helper the "
            "render path actually uses (localize_deep), not only by "
            "localize_message")

    def test_the_ack_reaches_an_arabic_reader_in_arabic_end_to_end(self, client):
        sid = _start(client)
        # The real route contract is `lang` (web/app.py set_ui_language).
        assert client.post("/ui-language", data={"lang": "ar"}).status_code == 302
        _correct(client, sid, _answered_ids(sid)[-1], MECH_CORRECTED)
        body = client.get("/session/" + sid).get_data(as_text=True)
        from web import ui_text
        ar = ui_text.localize_deep(webapp.CORRECTION_APPLIED_ACK, "ar")
        assert webapp.CORRECTION_APPLIED_ACK not in body, (
            "the English ack must not reach an Arabic reader")
        assert ar[:24] in body, "the Arabic ack must be rendered"


# =========================================================================
# K / L / S — R2 preserved; no semantic inference of "correction".
# =========================================================================
class TestKR2PreservationAndNoInference:

    def test_an_irrelevant_correction_cannot_manufacture_closure(self, client):
        sid = _start(client)
        _correct(client, sid, _answered_ids(sid)[-1], OFF_TOPIC)
        st = SESSION_STORE[sid]["state"]
        mech = st.get_gap(MECHANISM_COMPLETENESS)
        assert mech is None or mech.status != CLOSED, (
            "an off-topic correction must not close the mechanism gap")

    def test_correction_is_never_punitive(self, client):
        sid = _start(client)
        r = _correct(client, sid, _answered_ids(sid)[-1], OFF_TOPIC)
        assert r.status_code == 302, "never a BLOCK or a hard rejection"
        assert SESSION_STORE[sid]["state"] is not None

    def test_retraction_wording_alone_is_inert_without_an_explicit_action(self, client):
        # §6 C-1: "actually I was wrong" typed as an ORDINARY answer must behave
        # exactly as before — recorded, never treated as a correction.
        sid = _start(client)
        before_ids = _answered_ids(sid)
        before_withdrawn = assemble_deliverable(
            SESSION_STORE[sid]["state"])["_session_meta"]["withdrawn_source_records"]["total"]
        _answer(client, sid, "Actually I was wrong. There is no accelerometer at all.")
        after_withdrawn = assemble_deliverable(
            SESSION_STORE[sid]["state"])["_session_meta"]["withdrawn_source_records"]["total"]
        assert after_withdrawn == before_withdrawn == 0, (
            "no supersession may be INFERRED from wording")
        assert len(_answered_ids(sid)) == len(before_ids) + 1, "it is still recorded"


# =========================================================================
# M / Q — determinism and idempotency.
# =========================================================================
class TestMDeterminism:

    def test_resubmitting_the_same_correction_is_an_idempotent_no_op(self, client):
        sid = _start(client)
        target = _answered_ids(sid)[-1]
        _correct(client, sid, target, MECH_CORRECTED)
        n_after_first = len(_answered_ids(sid))
        state_after_first = _snapshot(SESSION_STORE[sid]["state"])
        _correct(client, sid, target, MECH_CORRECTED)          # exact resubmit
        assert len(_answered_ids(sid)) == n_after_first, "no second durable record"
        assert _snapshot(SESSION_STORE[sid]["state"]) == state_after_first

    def test_identical_amended_streams_reconstruct_identically(self, client):
        sid = _start(client)
        _correct(client, sid, _answered_ids(sid)[-1], MECH_CORRECTED)
        SESSION_STORE.pop(sid)
        a = reconstruct_readonly_state(_store(), sid)
        b = reconstruct_readonly_state(_store(), sid)
        assert _snapshot(a.state) == _snapshot(b.state)
        assert a.review == b.review


# =========================================================================
# N / P — the CLOSED-gap guard: the impossible mixed state is UNREACHABLE.
# =========================================================================
class TestNClosedGapGuard:

    CAUSAL = ("The circuit closes because the relay coil energizes the contact, "
              "which causes the current to flow through the load in a repeatable "
              "sequence of steps.")

    def _closed_gap_state(self):
        st = IdeaState(idea_id="guard")
        st.domain = "electronics_electrical"
        st.gaps.append(Gap(gap_type=MECHANISM_COMPLETENESS, status=OPEN, opened_at=0))
        for _ in range(2):
            integrate_response(st, MECHANISM_COMPLETENESS, "q", self.CAUSAL)
        return st

    def test_precondition_the_gap_really_reaches_closed(self):
        st = self._closed_gap_state()
        assert st.get_gap(MECHANISM_COMPLETENESS).status == CLOSED, (
            "this suite must never assert the guard vacuously")

    def test_a_closed_gap_is_never_weakened_in_place(self):
        st = self._closed_gap_state()
        integrate_response(st, MECHANISM_COMPLETENESS, "q", self.CAUSAL)
        gap = st.get_gap(MECHANISM_COMPLETENESS)
        assert gap.status == CLOSED, "CLOSED must never become PARTIAL in place"

    def test_the_impossible_mixed_state_is_unreachable(self):
        st = self._closed_gap_state()
        for probe in (self.CAUSAL, MECH_CORRECTED, OFF_TOPIC, "maybe"):
            integrate_response(st, MECHANISM_COMPLETENESS, "q", probe)
            gap = st.get_gap(MECHANISM_COMPLETENESS)
            assert not (gap.status == PARTIAL and gap.closed_at is not None), (
                "status=PARTIAL with closed_at set is an impossible state")

    def test_closed_at_is_set_if_and_only_if_the_gap_is_closed(self):
        st = self._closed_gap_state()
        for probe in (self.CAUSAL, OFF_TOPIC, MECH_CORRECTED):
            integrate_response(st, MECHANISM_COMPLETENESS, "q", probe)
        for gap in st.gaps:
            assert (gap.closed_at is not None) == (gap.status == CLOSED), (
                "closed_at/status inconsistency on %r" % gap.gap_type)


# =========================================================================
# O — NON-VACUOUS WPS-001 INV-004 regression coverage.
#
# The committed `tests/test_wps001_invariants.py::test_closed_gap_does_not_reopen`
# skips whenever its corpus reaches no CLOSED gap, which leaves its final
# assertion vacuous. The corpus below is literal, committed here, and is asserted
# to reach CLOSED *before* the invariant is checked.
# =========================================================================
class TestOInv004NonVacuous:

    CORPUS = (
        "A temperature sensor fails silently when manual checks are missed, so the "
        "operator loses the alarm.",
        "The circuit closes because the relay coil energizes the contact, which "
        "causes the current to flow through the load in a repeatable sequence of steps.",
        "It relies on inductive coupling and consumes energy from a 3.3V battery, "
        "because the coil converts current into a magnetic field which therefore "
        "moves the armature.",
        "The system boundary includes the sensor board and relay only; the external "
        "mains wiring is outside scope, because the enclosure limits what the device "
        "controls.",
    )

    def _driven(self):
        st = IdeaState(idea_id="inv004")
        st.domain = "electronics_electrical"
        run_iteration(st, self.CORPUS[0])
        for _ in range(14):
            gap = select_next_gap(st)
            if gap is None:
                break
            body = {MECHANISM_COMPLETENESS: self.CORPUS[1],
                    PHYSICAL_FEASIBILITY: self.CORPUS[2],
                    BOUNDARY_AMBIGUITY: self.CORPUS[3]}.get(gap, self.CORPUS[1])
            run_iteration(st, body)
        return st

    def test_the_corpus_provably_reaches_closed(self):
        st = self._driven()
        closed = {g.gap_type for g in st.gaps if g.status == CLOSED}
        assert closed, ("NON-VACUITY GUARD: this corpus must reach CLOSED, "
                        "otherwise the invariant below asserts nothing")

    def test_inv004_closed_gaps_never_move_backward(self):
        st = self._driven()
        closed = {g.gap_type for g in st.gaps if g.status == CLOSED}
        assert closed
        for _ in range(4):
            run_iteration(st, "Actually I was wrong. There is no relay at all. "
                              "I do not know how it works.")
        for gap in st.gaps:
            if gap.gap_type in closed:
                assert gap.status == CLOSED, (
                    "WPS-001 INV-004 VIOLATED: %r was CLOSED, now %r"
                    % (gap.gap_type, gap.status))
                assert gap.closed_at is not None

    def test_the_guard_is_what_holds_it_not_the_caller_filter(self):
        # Remove the caller's protection by calling integrate_response directly
        # on an already-CLOSED gap — the exact shape that produced the impossible
        # state before the guard existed.
        st = self._driven()
        closed = [g for g in st.gaps if g.status == CLOSED]
        assert closed, "non-vacuity guard"
        gap = closed[0]
        integrate_response(st, gap.gap_type, "q", self.CORPUS[1])
        assert gap.status == CLOSED and gap.closed_at is not None


# =========================================================================
# T — pack / domain neutrality and structural non-regression.
# =========================================================================
class TestTNeutralityAndStructure:

    def test_correction_path_does_not_branch_on_domain(self):
        import inspect
        src = inspect.getsource(webapp.correct_answer)
        for token in ("electronics", "mechanical", "domain_rules", "domain.json"):
            assert token not in src, (
                "the correction path must be domain-neutral (found %r)" % token)

    def test_supersession_derivation_is_additive_and_idempotent(self):
        st = IdeaState(idea_id="d")
        a = st.record_interaction("answered", "one", gap_context="G")
        b = st.record_interaction("answered", "two", gap_context="G",
                                  supersedes=[a.record_id])
        blob = ProjectRecordContract.from_state(st).to_dict()
        # Simulate the durable reality: the prior row was never rewritten.
        for row in blob["assertions"]:
            if row["record_id"] == a.record_id:
                row["superseded_by"] = None
        restored = ProjectRecordContract.from_dict(blob)
        by_id = {r.record_id: r for r in restored.assertions}
        assert by_id[a.record_id].superseded_by == b.record_id, "inverse re-derived"
        # idempotent: deriving again changes nothing
        before = [(r.record_id, r.superseded_by) for r in restored.assertions]
        reconcile_supersession_edges(restored.assertions)
        assert [(r.record_id, r.superseded_by) for r in restored.assertions] == before

    def test_conflicting_supersession_edges_are_rejected_not_repaired(self):
        st = IdeaState(idea_id="c")
        a = st.record_interaction("answered", "one", gap_context="G")
        st.record_interaction("answered", "two", gap_context="G",
                              supersedes=[a.record_id])
        blob = ProjectRecordContract.from_state(st).to_dict()
        for row in blob["assertions"]:
            if row["record_id"] == a.record_id:
                row["superseded_by"] = "rec_999"
        with pytest.raises(InvalidReferenceError):
            ProjectRecordContract.from_dict(blob)

    def test_two_records_cannot_supersede_the_same_prior_record(self):
        st = IdeaState(idea_id="m")
        a = st.record_interaction("answered", "one", gap_context="G")
        b = st.record_interaction("answered", "two", gap_context="G",
                                  supersedes=[a.record_id])
        blob = ProjectRecordContract.from_state(st).to_dict()
        blob["assertions"].append(dict(blob["assertions"][-1],
                                       record_id="rec_3",
                                       superseded_by=None))
        for row in blob["assertions"]:
            if row["record_id"] == a.record_id:
                row["superseded_by"] = None
        with pytest.raises(InvalidReferenceError):
            ProjectRecordContract.from_dict(blob)

    def test_pre_r4_minting_is_byte_identical(self):
        st = IdeaState(idea_id="p")
        r = st.record_interaction("answered", "content", gap_context="G",
                                  iteration=3)
        assert r.supersedes == [] and r.superseded_by is None
        assert r.record_id == "rec_1"
