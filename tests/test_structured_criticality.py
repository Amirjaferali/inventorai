"""Workstream 4 — Structured Criticality Capture: BASE RED / HEAD GREEN gate.

File: tests/test_structured_criticality.py
Purpose: the single test file authorized by the recorded Workstream 4
Increment Contract (docs/governance/
STRUCTURED_CRITICALITY_CAPTURE_INCREMENT_CONTRACT.md; recording PR #181,
merge cb1f4fd8fb4854864ef89c3f3df2275d818785c9, contract blob
44b2a1f254e80c98ff80cbced89db3332af7ce57). On the authorized base it proves
(contract §11) that the required structured-criticality behavior is ABSENT;
at head it must prove the §12 GREEN behaviors byte-exact.
Input contract: exercises ONLY committed real paths — the web journey
(web.app test client with the byte-identical Workstream 1 baseline inputs),
the in-memory IdeaState in web.app.SESSION_STORE, the pure derivation
engine.requirement_landscape.derive_requirement_landscape, and the
deliverable boundary engine.deliverable_assembler.assemble_deliverable plus
the rendered /session/<sid>/deliverable HTML. No mocks, no monkeypatching,
no fixture files.
Output contract: two disjoint groups. "PROTECTED INVARIANT" tests (P1-P5)
must pass on base AND at head (they pin behavior the increment must not
change). "RED" tests (R1-R8) fail on base because the §6 recorded-state
model, the §6.3 guarded recorder, and the §4 owner-confirmed/undetermined
representations do not exist yet; each RED failure carries an
obligation-specific message naming the distinct missing contract behavior,
never a fixture defect. GREEN JOURNEY TESTS (G1-G5, TestGreenJourney):
real executable journey tests over the implemented completion-stage
confirmation surface, covering every entry recorded in
GREEN_ONLY_JOURNEY_OBLIGATIONS (the former owner-recorded GREEN-only
placeholder, now replaced as mandated — this suite must show zero
skipped and zero xfailed).
Prohibited behaviors: must not modify any source file or any other test
file; must not assert an implementation-chosen mechanism (route paths,
endpoint names, placement, template structure, storage layout, or the
recorder's Python call shape beyond the contractually required record
content); must not touch persistence, scoring, Safety Signals, or the
frozen evidence trees.

Contract-pinned surface used here (and nothing beyond it):
  * IdeaState.criticality_confirmations  (contract §6.1)
  * IdeaState.record_criticality_confirmation(...)  (contract §6.3; the
    RECORDED RESULT and rejection semantics are asserted, not a fixed
    Python signature — optional data for a deferral is simply not passed)
  * record fields: requirement_id, action, category, rationale_verbatim,
    rationale_source, provenance="owner_confirmed"  (contract §6.1)
  * categories FEASIBILITY-THREATENING / VALUE-ENHANCING / REFINEMENT /
    UNDETERMINED and authorities system-derived / undetermined /
    owner-confirmed  (contract §4)
  * public wordings: "Essential to feasibility", "Important to value",
    "Refinement or improvement", "Not yet determined",
    "Confirmed by the inventor", "Confirmation not yet available"  (§4)
  * the five lightweight actions "Yes, that is correct", "Change this
    part", "Something is missing", "I am not sure yet", "Decide later"
    (contract §7.2, owner-approved wording) — NOT used as any BASE RED
    failure condition; they are GREEN-stage assertions on the ultimately
    chosen authorized interaction surface (see
    GREEN_ONLY_JOURNEY_OBLIGATIONS).
"""
import json
from test_p4_1b2a_durable_answer_append import answered_post  # P4-1b-2a

import pytest

from web.app import app, SESSION_STORE, DOMAIN_CONFIRM_VALUE
from engine.deliverable_assembler import assemble_deliverable
from engine.requirement_landscape import derive_requirement_landscape

# --- Byte-identical Workstream 1 baseline journey inputs (contract §11: the
# reused WS1 journey; copied verbatim from the committed Workstream 3
# evidence harness docs/governance/evidence/workstream3_deliverable_hygiene/
# generate_ws3_artifacts.py — do not edit) -----------------------------------
IDEA_WS1 = (
    "A smart plug-in safety device that senses appliance current and voltage "
    "with a microcontroller and disconnects a relay to warn about dangerous "
    "appliances"
)
BASE = ("The current sensor detects an abnormal rise because the shunt "
        "resistor voltage increases, therefore the microcontroller opens the "
        "relay to disconnect the appliance.")
DANGER_BY_ITERATION = {
    3: " If the sensing is wrong, the dangerous appliance could remain powered.",
    4: (" If it trips the wrong branch, the wrong appliance could be "
        "disconnected and it would fail to isolate the actual source of danger."),
    6: (" If the relay sticks, damage or overheating could continue and the "
        "fire risk could continue until someone notices."),
    7: (" The current sensing accuracy is essential; the buzzer volume and "
        "alert timing are adjustable."),
}
UNKNOWN_ITERATION = 5
UNKNOWN_TEXT = "I don't know yet."
MAX_ITERATIONS = 30

# The inventor's iteration-7 essential/adjustable statement (the recorded
# input at the heart of plan §3.B defect 7), byte-verbatim.
ITERATION_7_STATEMENT = BASE + DANGER_BY_ITERATION[7]

# Contract §4 canonical categories (internal-only strings).
CATEGORY_FEASIBILITY = "FEASIBILITY-THREATENING"
CATEGORY_VALUE = "VALUE-ENHANCING"
CATEGORY_REFINEMENT = "REFINEMENT"
CATEGORY_UNDETERMINED = "UNDETERMINED"

# Contract §4 public wordings (byte-exact).
PUBLIC_ESSENTIAL = "Essential to feasibility"
PUBLIC_VALUE = "Important to value"
PUBLIC_REFINEMENT = "Refinement or improvement"
PUBLIC_NOT_YET_DETERMINED = "Not yet determined"
PUBLIC_OWNER_CONFIRMED = "Confirmed by the inventor"
PUBLIC_DEFERRED = "Confirmation not yet available"
# Existing committed system-derived wording (contract §4: unchanged).
PUBLIC_SYSTEM_DERIVED = "assigned automatically by the system; not yet reviewed"

# Contract §7.2 five lightweight actions (owner-approved wording, byte-exact).
# GREEN-stage assertion material only — never a BASE RED failure condition.
LIGHTWEIGHT_ACTIONS = [
    "Yes, that is correct",
    "Change this part",
    "Something is missing",
    "I am not sure yet",
    "Decide later",
]

# --- Mandatory GREEN journey obligations (owner final RED-suite review). On
# base these could not be functionally probed without assuming the
# implementation-chosen surface; they are now implemented as the real journey
# tests in TestGreenJourney below (G1-G5). ----------------------------------
GREEN_ONLY_JOURNEY_OBLIGATIONS = [
    ("summary_first_journey_capability",
     "After completing the real WS1 journey, a reachable functional action "
     "lets the inventor review a contextual criticality summary, explicitly "
     "accept or correct it, or explicitly defer (contract §7.2, §11(6)); "
     "the five LIGHTWEIGHT_ACTIONS wordings are asserted byte-exact on the "
     "ultimately chosen authorized interaction surface."),
    ("deferral_without_penalty_zero_delta",
     "State compared before and after an ACTUAL deferral proves zero "
     "maturity, scoring, gap, transition, and unrelated-state deltas "
     "(contract §7.8; GREEN usability criterion #10)."),
]


# --- Real-path journey helpers ----------------------------------------------
def _start(idea):
    client = app.test_client()
    r = client.post("/start", data={"idea": idea,
                                    "domain_confirm": DOMAIN_CONFIRM_VALUE})
    assert r.status_code == 302, (
        "fixture defect: /start did not redirect (%s)" % r.status_code)
    sid = r.headers["Location"].rsplit("/", 1)[-1]
    return client, sid


def _drive_ws1_journey_to_completion(client, sid):
    """Drive the byte-identical WS1 journey; collect every rendered flow page
    (including the completion page). Fails loudly if the journey does not
    complete (fixture defect, not a RED result)."""
    pages = []
    for i in range(2, MAX_ITERATIONS + 2):
        page = client.get(f"/session/{sid}").get_data(as_text=True)
        pages.append(page)
        if '<p class="complete">' in page:
            return pages
        if i == UNKNOWN_ITERATION:
            action, text = "unknown", UNKNOWN_TEXT
        else:
            action, text = "answered", BASE + DANGER_BY_ITERATION.get(i, "")
        answered_post(client, sid, {"response": text, "action": action})
    pytest.fail("fixture defect: WS1 journey did not reach the completion "
                "branch within %d iterations" % MAX_ITERATIONS)


@pytest.fixture()
def ws1_completed():
    """Completed WS1 baseline journey: (client, sid, state, flow_pages)."""
    client, sid = _start(IDEA_WS1)
    pages = _drive_ws1_journey_to_completion(client, sid)
    state = SESSION_STORE[sid]["state"]
    yield client, sid, state, pages
    SESSION_STORE.pop(sid, None)


def _section13(state):
    return assemble_deliverable(state)["section_13_requirement_landscape"]


def _first_requirement(state):
    landscape = derive_requirement_landscape(state)
    assert landscape.requirements, "fixture defect: empty landscape"
    return landscape.requirements[0]


def _confirm(state, target, category, obligation):
    """Record an explicit confirmation via the §6.3 guarded recorder, reusing
    the inventor's verbatim iteration-7 statement as rationale. On base the
    recorder does not exist: fail with the OBLIGATION-SPECIFIC message so the
    RED failure names the distinct unmet contract behavior (shared root
    cause: contract §11(3) — no recorder API, no route)."""
    if not hasattr(state, "record_criticality_confirmation"):
        pytest.fail("missing behavior: %s — unmet on base because no "
                    "structured confirmation path exists (contract §11(3): "
                    "no recorder API, no route)" % obligation)
    rec_id = target.primary_anchor.anchor_reference
    state.record_criticality_confirmation(
        requirement_id=target.requirement_id,
        action="confirmed",
        category=category,
        rationale_verbatim=ITERATION_7_STATEMENT,
        rationale_source="reused_statement:" + rec_id,
    )
    return target


def _defer(state, target, obligation):
    """Record an explicit deferral. Per the owner revision, no optional data
    is passed as explicit None — a deferral carries no category and no
    rationale, so only the action itself is supplied; the RECORDED RESULT is
    what the contract fixes (§6.1), not the call shape."""
    if not hasattr(state, "record_criticality_confirmation"):
        pytest.fail("missing behavior: %s — unmet on base because no "
                    "structured confirmation path exists (contract §11(3): "
                    "no recorder API, no route)" % obligation)
    state.record_criticality_confirmation(
        requirement_id=target.requirement_id,
        action="deferred",
    )
    return target


# =============================================================================
# GROUP P — PROTECTED INVARIANTS (must PASS on base AND at head).
# =============================================================================
class TestProtectedInvariants:
    def test_p1_ai_q2_free_text_never_classifies_criticality(self, ws1_completed):
        """Coverage A / contract §11(1)-(2): the inventor's explicit
        iteration-7 essential/adjustable statement, although recorded, must
        NOT silently produce any criticality classification. This invariant
        holds on base and MUST still hold at head (only explicit confirmation
        may classify; free text alone never does)."""
        _, _, state, _ = ws1_completed
        landscape = derive_requirement_landscape(state)
        assert landscape.requirements, "fixture defect: empty landscape"
        for r in landscape.requirements:
            assert r.criticality == CATEGORY_UNDETERMINED
            assert r.criticality_authority == "system-derived"
            assert r.criticality_rationale is None

    def test_p2_iteration7_statement_recorded_verbatim(self, ws1_completed):
        """The essential/adjustable input WAS received and is preserved
        byte-verbatim in the session ledger (proves defect §3.B.7 is about a
        missing confirmation path, not missing input)."""
        _, _, state, _ = ws1_completed
        contents = [getattr(rec, "content", "") or ""
                    for rec in getattr(state, "assertions", [])]
        assert any(ITERATION_7_STATEMENT == c for c in contents), (
            "fixture defect: iteration-7 statement not recorded verbatim")

    def test_p3_section13_never_interacted_public_wording(self, ws1_completed):
        """Contract §12 (correctness, never-interacted leg): on base and at
        head, requirements without any explicit inventor action render the
        existing committed public wordings, byte-exact, in Section 13 JSON."""
        _, _, state, _ = ws1_completed
        s13 = _section13(state)
        assert s13["requirements"], "fixture defect: no §13 requirements"
        for row in s13["requirements"]:
            assert row["criticality"] == PUBLIC_NOT_YET_DETERMINED
            assert row["criticality_authority"] == PUBLIC_SYSTEM_DERIVED
            assert row["criticality_rationale"] is None

    def test_p4_rendering_changes_nothing(self, ws1_completed):
        """GREEN #5/#17 invariant leg (render-without-accepting probe):
        merely rendering the session page and the deliverable never alters
        the derived landscape or Section 13."""
        client, sid, state, _ = ws1_completed
        before_landscape = derive_requirement_landscape(state)
        before_s13 = json.dumps(_section13(state), sort_keys=True, default=str)
        client.get(f"/session/{sid}")
        client.get(f"/session/{sid}/deliverable")
        client.get(f"/session/{sid}")
        after_landscape = derive_requirement_landscape(state)
        after_s13 = json.dumps(_section13(state), sort_keys=True, default=str)
        assert before_landscape == after_landscape
        assert before_s13 == after_s13

    def test_p5_no_raw_category_or_authority_tokens_inventor_facing(
            self, ws1_completed):
        """Contract §12 Protection: the raw internal category/authority
        tokens never appear in inventor-facing Section 13 JSON or the
        rendered deliverable HTML (true on base; must remain true at head)."""
        client, sid, state, _ = ws1_completed
        s13_text = json.dumps(_section13(state), default=str)
        html = client.get(f"/session/{sid}/deliverable").get_data(as_text=True)
        for token in (CATEGORY_FEASIBILITY, CATEGORY_VALUE, CATEGORY_REFINEMENT,
                      "owner-confirmed", "system-derived"):
            assert token not in s13_text, token
            assert token not in html, token


# =============================================================================
# GROUP R — GENUINE RED (must FAIL on base: the behavior does not exist).
# Each test names its own distinct contract obligation in its failure message.
# =============================================================================
class TestRecordedStateModelRed:
    def test_r1_confirmation_history_exists(self, ws1_completed):
        """Contract §6.1 (coverage B): IdeaState carries the session-bounded
        append-only confirmation history, seeded empty. MISSING ON BASE."""
        _, _, state, _ = ws1_completed
        assert hasattr(state, "criticality_confirmations"), (
            "missing behavior: the §6.1 append-only confirmation history "
            "(IdeaState.criticality_confirmations) does not exist on base")
        assert state.criticality_confirmations == []

    def test_r2_guarded_recorder_records_owner_confirmation(self, ws1_completed):
        """Contract §6.3 + §6.1 (coverage B/C): the guarded recorder exists
        and stores one frozen record with the §6.1 fields — the reused
        verbatim rationale, its attribution, and owner_confirmed provenance.
        MISSING ON BASE."""
        _, _, state, _ = ws1_completed
        target = _first_requirement(state)
        rec_id = target.primary_anchor.anchor_reference
        _confirm(state, target, CATEGORY_FEASIBILITY,
                 "the §6.3 guarded recorder storing a §6.1 confirmation record")
        history = state.criticality_confirmations
        assert len(history) == 1
        record = history[0]
        assert record.requirement_id == target.requirement_id
        assert record.action == "confirmed"
        assert record.category == CATEGORY_FEASIBILITY
        assert record.rationale_verbatim == ITERATION_7_STATEMENT
        assert record.rationale_source == "reused_statement:" + rec_id
        assert record.provenance == "owner_confirmed"

    def test_r3_recorder_rejects_confirmed_undetermined(self, ws1_completed):
        """Contract §4 clarification / §6.3 (coverage C): confirmed +
        UNDETERMINED is invalid — rejected at the recorder, nothing stored.
        MISSING ON BASE (no guard exists)."""
        _, _, state, _ = ws1_completed
        target = _first_requirement(state)
        if not hasattr(state, "record_criticality_confirmation"):
            pytest.fail("missing behavior: rejection of the invalid "
                        "confirmed + UNDETERMINED combination — unmet on "
                        "base because the §6.3 guarded recorder is absent")
        with pytest.raises(Exception):
            state.record_criticality_confirmation(
                requirement_id=target.requirement_id,
                action="confirmed",
                category=CATEGORY_UNDETERMINED,
                rationale_verbatim=ITERATION_7_STATEMENT,
                rationale_source="reused_statement:x",
            )
        assert state.criticality_confirmations == []

    def test_r4_recorder_rejects_missing_rationale(self, ws1_completed):
        """Contract §6.3 (coverage C): a non-UNDETERMINED confirmation
        without a non-empty rationale is rejected — nothing stored.
        MISSING ON BASE (no guard exists)."""
        _, _, state, _ = ws1_completed
        target = _first_requirement(state)
        if not hasattr(state, "record_criticality_confirmation"):
            pytest.fail("missing behavior: rejection of a non-UNDETERMINED "
                        "confirmation without a rationale — unmet on base "
                        "because the §6.3 guarded recorder is absent")
        with pytest.raises(Exception):
            state.record_criticality_confirmation(
                requirement_id=target.requirement_id,
                action="confirmed",
                category=CATEGORY_VALUE,
                rationale_verbatim="",
                rationale_source="inventor_typed",
            )
        assert state.criticality_confirmations == []


class TestEndToEndRepresentationRed:
    def test_r5_confirmed_category_reaches_section13_json(self, ws1_completed):
        """Contract §11(4) / §12 (coverage C): an explicitly confirmed
        category is representable end-to-end — Section 13 JSON shows the §4
        public wordings byte-exact and the verbatim rationale.
        MISSING ON BASE."""
        _, _, state, _ = ws1_completed
        target = _confirm(
            state, _first_requirement(state), CATEGORY_FEASIBILITY,
            "end-to-end representation of a confirmed category in "
            "Section 13 JSON (\"Essential to feasibility\" / "
            "\"Confirmed by the inventor\" / verbatim rationale)")
        rows = [r for r in _section13(state)["requirements"]
                if r["statement"] == target.statement]
        assert rows, "confirmed requirement absent from §13"
        row = rows[0]
        assert row["criticality"] == PUBLIC_ESSENTIAL
        assert row["criticality_authority"] == PUBLIC_OWNER_CONFIRMED
        assert row["criticality_rationale"] == ITERATION_7_STATEMENT

    def test_r6_confirmed_category_reaches_rendered_html(self, ws1_completed):
        """Contract §11(4) / §12 (coverage C): the confirmed public wording,
        authority, and verbatim rationale render in the deliverable HTML.
        MISSING ON BASE."""
        client, sid, state, _ = ws1_completed
        _confirm(state, _first_requirement(state), CATEGORY_FEASIBILITY,
                 "end-to-end rendering of a confirmed category in the "
                 "deliverable HTML")
        html = client.get(f"/session/{sid}/deliverable").get_data(as_text=True)
        assert PUBLIC_ESSENTIAL in html
        assert PUBLIC_OWNER_CONFIRMED in html
        assert ITERATION_7_STATEMENT in html

    def test_r7_explicit_deferral_representable(self, ws1_completed):
        """Contract §11(5) / §4 (coverage C): explicit deferral yields
        UNDETERMINED / undetermined and the public wording "Confirmation not
        yet available" — the `undetermined` authority is reachable.
        MISSING ON BASE."""
        _, _, state, _ = ws1_completed
        target = _defer(state, _first_requirement(state),
                        "representation of an explicit deferral as "
                        "UNDETERMINED / undetermined (\"Confirmation not "
                        "yet available\")")
        derived = [r for r in derive_requirement_landscape(state).requirements
                   if r.requirement_id == target.requirement_id]
        assert derived, "deferred requirement vanished from derivation"
        assert derived[0].criticality == CATEGORY_UNDETERMINED
        assert derived[0].criticality_authority == "undetermined"
        rows = [r for r in _section13(state)["requirements"]
                if r["statement"] == target.statement]
        assert rows and rows[0]["criticality_authority"] == PUBLIC_DEFERRED
        assert rows[0]["criticality"] == PUBLIC_NOT_YET_DETERMINED

    def test_r8_history_append_only_latest_governs(self, ws1_completed):
        """Contract §6.1-§6.2 / §12 (coverage C): earlier records survive
        later corrections; the latest explicit action governs the derived
        result. MISSING ON BASE."""
        _, _, state, _ = ws1_completed
        target = _defer(state, _first_requirement(state),
                        "append-only confirmation history where the latest "
                        "explicit action governs the derived result")
        _confirm(state, target, CATEGORY_REFINEMENT,
                 "append-only confirmation history where the latest "
                 "explicit action governs the derived result")
        history = state.criticality_confirmations
        assert len(history) == 2, "history must be append-only (both survive)"
        assert history[0].action == "deferred"
        assert history[1].action == "confirmed"
        derived = [r for r in derive_requirement_landscape(state).requirements
                   if r.requirement_id == target.requirement_id]
        assert derived[0].criticality == CATEGORY_REFINEMENT
        assert derived[0].criticality_authority == "owner-confirmed"


# =============================================================================
# GROUP G — GREEN JOURNEY TESTS (real journeys over the implemented
# completion-stage surface; replaces the owner-recorded GREEN-only
# placeholder; every GREEN_ONLY_JOURNEY_OBLIGATIONS entry is covered).
# =============================================================================
import re as _re

SUMMARY_LEAD = "This is what I understood from your explanation:"
CLARIFICATION_QUESTION = (
    "Would the idea still achieve its purpose if this part changed?")
CATEGORY_CHOICE_LABELS = [
    "The idea may not work without this",
    "The idea would still work, but this adds important value",
    "This mainly improves or refines the idea",
    "I am not sure yet",
]
# §7.9 banned inventor-facing governance vocabulary (exact phrases).
BANNED_UI_TERMS = [
    "criticality authority", "owner-confirmed", "system-derived",
    "undetermined authority", "rationale requirement", "evidence gate",
    "classification compliance",
]

_FOCUS_TOKEN_RE = _re.compile(r'name="focus_token" value="([0-9a-f]{16})"')
_RATIONALE_RE = _re.compile(
    r'<textarea name="rationale"[^>]*>(.*?)</textarea>', _re.S)


def _page(client, sid):
    return client.get(f"/session/{sid}").get_data(as_text=True)


def _focus_token(page):
    m = _FOCUS_TOKEN_RE.search(page)
    assert m, "no focus token rendered on the confirmation surface"
    return m.group(1)


def _fresh_completed_journey():
    """A second completed WS1 journey for tests needing an untouched state."""
    client, sid = _start(IDEA_WS1)
    _drive_ws1_journey_to_completion(client, sid)
    return client, sid, SESSION_STORE[sid]["state"]


class TestGreenJourney:
    def test_g1_summary_first_surface_five_actions_clean_vocabulary(
            self, ws1_completed):
        """G1 (§7.2 / GREEN #1-#4, #12; obligations A, B, F): the completed
        real journey presents the summary-first block with the exact lead-in,
        the inventor's own recorded words, and ALL FIVE lightweight actions
        byte-exact — while exposing no raw category/authority/requirement-id
        token and no §7.9 banned governance phrase."""
        client, sid, _, _ = ws1_completed
        page = _page(client, sid)
        assert SUMMARY_LEAD in page
        assert "You said:" in page
        for action in LIGHTWEIGHT_ACTIONS:
            assert action in page, "missing lightweight action: %r" % action
        for token in (CATEGORY_FEASIBILITY, CATEGORY_VALUE, CATEGORY_REFINEMENT,
                      "req:assertion:", "req:gap:", "req:contradiction:"):
            assert token not in page, token
        for phrase in BANNED_UI_TERMS:
            assert phrase not in page, phrase

    def test_g2_accept_flow_end_to_end_no_adoption_before_acceptance(
            self, ws1_completed):
        """G2 (§7.2/§7.4/§7.7/§7.10; §12 correctness; obligations A, C-accept,
        D): 'Yes, that is correct' leads to exactly one supportive
        clarification; nothing is adopted before the explicit final
        acceptance; accepting 'The idea may not work without this' with the
        prefilled verbatim rationale (zero retyping) records the confirmation
        and renders the §4 public wordings end-to-end."""
        client, sid, state, _ = ws1_completed
        page = _page(client, sid)
        token = _focus_token(page)
        # Step 1: confirm the understanding summary.
        r = client.post(f"/session/{sid}", data={
            "criticality_action": "summary_correct", "focus_token": token})
        assert r.status_code == 302
        assert state.criticality_confirmations == []   # no silent adoption
        # Step 2: the single clarification, with the prefilled rationale.
        page = _page(client, sid)
        assert CLARIFICATION_QUESTION in page
        for label in CATEGORY_CHOICE_LABELS:
            assert label in page, label
        # Rendering the unaccepted proposal changes nothing (GREEN #5/#17).
        for req in derive_requirement_landscape(state).requirements:
            assert req.criticality == CATEGORY_UNDETERMINED
            assert req.criticality_authority == "system-derived"
        rationale_m = _RATIONALE_RE.search(page)
        assert rationale_m, "no prefilled rationale textarea"
        rationale = rationale_m.group(1)
        assert rationale.strip(), "proposed rationale is empty"
        token = _focus_token(page)
        # Step 3: explicit acceptance — zero typed input (accept as displayed).
        r = client.post(f"/session/{sid}", data={
            "criticality_action": "clarify_choice", "focus_token": token,
            "category_choice": "essential", "rationale": rationale})
        assert r.status_code == 302
        history = state.criticality_confirmations
        assert len(history) == 1
        record = history[0]
        assert record.action == "confirmed"
        assert record.category == CATEGORY_FEASIBILITY
        assert record.rationale_verbatim == rationale
        assert record.rationale_source.startswith("reused_statement:")
        assert record.provenance == "owner_confirmed"
        # End-to-end public representation (byte-exact §4 wordings).
        confirmed = [r_ for r_ in derive_requirement_landscape(state).requirements
                     if r_.requirement_id == record.requirement_id]
        assert confirmed and confirmed[0].criticality == CATEGORY_FEASIBILITY
        assert confirmed[0].criticality_authority == "owner-confirmed"
        rows = [row for row in _section13(state)["requirements"]
                if row["criticality"] == PUBLIC_ESSENTIAL]
        assert rows and rows[0]["criticality_authority"] == PUBLIC_OWNER_CONFIRMED
        assert rows[0]["criticality_rationale"] == rationale
        html = client.get(f"/session/{sid}/deliverable").get_data(as_text=True)
        assert PUBLIC_ESSENTIAL in html and PUBLIC_OWNER_CONFIRMED in html
        assert rationale in html

    def test_g3_correction_and_missing_paths_store_nothing(self, ws1_completed):
        """G3 (§7.2 / owner rule 6; obligation C-correct/missing): 'Change
        this part' and 'Something is missing' store no confirmation and
        return the inventor to an existing free-text answer path on the same
        journey."""
        client, sid, state, _ = ws1_completed
        for action in ("summary_change", "summary_missing"):
            token = _focus_token(_page(client, sid))
            r = client.post(f"/session/{sid}", data={
                "criticality_action": action, "focus_token": token})
            assert r.status_code == 302
            assert state.criticality_confirmations == []
            page = _page(client, sid)
            assert 'name="response"' in page, (
                "no free-text path offered after %s" % action)
            # The next input flows through the EXISTING answer handling.
            r = answered_post(client, sid, {
                "response": "The relay module is the part that changed.",
                "action": "answered"})
            assert r.status_code == 302
            assert state.criticality_confirmations == []

    def test_g4_uncertainty_and_deferral_zero_delta(self):
        """G4 (§7.8 / GREEN #10; obligations C-uncertainty/defer, E): both
        'I am not sure yet' and 'Decide later' record an explicit deferral
        with ZERO change to maturity, scoring, gaps, transitions, iteration,
        direction, the ledger, the last result, and every unrelated
        deliverable section."""
        for action in ("summary_unsure", "summary_later"):
            client, sid, state = _fresh_completed_journey()
            entry = SESSION_STORE[sid]
            token = _focus_token(_page(client, sid))
            before = assemble_deliverable(state)
            snapshot = (
                state.maturity_level, state.iteration, state.direction,
                [(g.gap_type, g.status, g.iterations_open) for g in state.gaps],
                len(state.assertions), len(state.acknowledged_unknowns),
                entry.get("last_result"),
            )
            r = client.post(f"/session/{sid}", data={
                "criticality_action": action, "focus_token": token})
            assert r.status_code == 302
            after = assemble_deliverable(state)
            assert snapshot == (
                state.maturity_level, state.iteration, state.direction,
                [(g.gap_type, g.status, g.iterations_open) for g in state.gaps],
                len(state.assertions), len(state.acknowledged_unknowns),
                entry.get("last_result"),
            )
            for key in before:
                if key in ("section_13_requirement_landscape", "generated_at"):
                    continue
                before_val, after_val = before[key], after[key]
                if key == "_session_meta":
                    # Workstream 6 owner ruling (GREEN continuation): the
                    # additive _session_meta.requirement_landscape_synthesis
                    # object is canonically DERIVED from Section 13 values, so
                    # it legitimately changes when the deferred row's Section
                    # 13 criticality metadata changes — exactly parallel to
                    # the existing section_13 exclusion above. Every other
                    # _session_meta key remains strictly asserted.
                    before_val = {k: v for k, v in before_val.items()
                                  if k != "requirement_landscape_synthesis"}
                    after_val = {k: v for k, v in after_val.items()
                                 if k != "requirement_landscape_synthesis"}
                assert json.dumps(before_val, sort_keys=True, default=str) == \
                    json.dumps(after_val, sort_keys=True, default=str), (
                        "deferral altered unrelated deliverable section %r "
                        "after %s" % (key, action))
            history = state.criticality_confirmations
            assert len(history) == 1 and history[0].action == "deferred"
            assert history[0].category is None
            deferred = [r_ for r_ in derive_requirement_landscape(state).requirements
                        if r_.requirement_id == history[0].requirement_id]
            assert deferred[0].criticality == CATEGORY_UNDETERMINED
            assert deferred[0].criticality_authority == "undetermined"
            rows = [row for row in _section13(state)["requirements"]
                    if row["criticality_authority"] == PUBLIC_DEFERRED]
            assert rows and rows[0]["criticality"] == PUBLIC_NOT_YET_DETERMINED
            SESSION_STORE.pop(sid, None)

    def test_g5_manipulated_or_stale_posts_rejected(self, ws1_completed):
        """G5 (§6.3 route rejection / owner rule 5; obligation G): stale,
        mismatched, or manipulated submissions — a wrong focus token, an
        unknown action, a clarify submission without the summary step, a
        manipulated category value (the route-level confirmed+UNDETERMINED
        analogue), and an emptied rationale — are all rejected with HTTP 400
        and NOTHING stored."""
        client, sid, state, _ = ws1_completed
        token = _focus_token(_page(client, sid))
        bad = [
            {"criticality_action": "summary_correct", "focus_token": "0" * 16},
            {"criticality_action": "bogus_action", "focus_token": token},
            {"criticality_action": "clarify_choice", "focus_token": token,
             "category_choice": "essential", "rationale": "text"},  # no summary step
        ]
        for form in bad:
            r = client.post(f"/session/{sid}", data=form)
            assert r.status_code == 400, form
            assert state.criticality_confirmations == []
        # Enter the clarify stage legitimately, then attempt manipulation.
        r = client.post(f"/session/{sid}", data={
            "criticality_action": "summary_correct", "focus_token": token})
        assert r.status_code == 302
        page = _page(client, sid)
        token = _focus_token(page)
        rationale = _RATIONALE_RE.search(page).group(1)
        for form in (
            {"criticality_action": "clarify_choice", "focus_token": token,
             "category_choice": "UNDETERMINED", "rationale": rationale},
            {"criticality_action": "clarify_choice", "focus_token": token,
             "category_choice": "essential", "rationale": "   "},
        ):
            r = client.post(f"/session/{sid}", data=form)
            assert r.status_code == 400, form
            assert state.criticality_confirmations == []


# --- P4-1b-2a BF2: the REAL criticality-correction free-text form -------------
def test_p4_1b2a_criticality_correction_form_carries_and_enforces_token():
    """BF2 (REV1): drive the real journey to the criticality-correction stage,
    inspect the actual rendered correction form, and submit the extracted token
    through the real route. Proves the correction free-text form (A) carries the
    server-issued token, (B) posts its true production shape (response + token,
    NO action), (C) resolves to `answered` via the legacy default rule, (D)
    durably appends before acknowledgement with record_id = rec_N, (E) is an
    idempotent no-op on same-token/same-content retry, and (F) fails closed on
    same-token/different-content."""
    import os
    import re as _re
    from engine.record_store import SqliteRecordStore

    client, sid = _start(IDEA_WS1)
    _drive_ws1_journey_to_completion(client, sid)
    # Enter the correction stage via the real summary action (NOT answered_post:
    # this criticality branch ignores the answer token).
    ftok = _focus_token(_page(client, sid))
    assert client.post(f"/session/{sid}", data={
        "criticality_action": "summary_change", "focus_token": ftok}
    ).status_code == 302

    page = _page(client, sid)
    # Isolate the correction free-text form (the one carrying the response field).
    forms = _re.findall(r"<form\b[^>]*>(.*?)</form>", page, _re.DOTALL)
    corr = [f for f in forms if 'name="response"' in f]
    assert corr, "the correction free-text form must render at the correction stage"
    corr_html = corr[0]
    # (A) token present; (B) production shape: response + answer_token, no action.
    assert 'name="answer_token"' in corr_html, "(A) correction form must carry the token"
    assert 'name="action"' not in corr_html, "(B) correction form posts NO action field"
    mtok = _re.search(r'name="answer_token"[^>]*value="([^"]+)"', corr_html)
    assert mtok and mtok.group(1), "(A) a server-issued token value must render"
    atok = mtok.group(1)

    def _durable_answers():
        st = SqliteRecordStore(os.environ["INVENTORAI_DB_PATH"])
        try:
            contract = st.load_contract(sid)
        finally:
            st.close()
        return [r for r in contract.assertions if r.disposition == "answered"]

    before = len(_durable_answers())
    correction = "The enclosure also overheats during long fan runs and needs a vent."
    # (C)+(D): submit the correction with response + token, NO action field.
    assert client.post(f"/session/{sid}",
                       data={"response": correction, "answer_token": atok}
                       ).status_code in (301, 302)
    after = _durable_answers()
    assert len(after) == before + 1, "(C/D) correction resolves to answered and durably appends once"
    assert after[-1].content == correction, "(D) the accepted correction is stored verbatim"
    assert _re.fullmatch(r"rec_\d+", after[-1].record_id), "(D) record_id stays rec_N (Option A)"

    # (E) same token + same content retry: no second durable event.
    client.post(f"/session/{sid}", data={"response": correction, "answer_token": atok})
    assert len(_durable_answers()) == before + 1, "(E) same-token same-content retry does not double-append"

    # (F) same token + different content: fail closed, no second event.
    client.post(f"/session/{sid}",
                data={"response": "A completely different correction body.", "answer_token": atok})
    assert len(_durable_answers()) == before + 1, "(F) same-token different-content fails closed"
    SESSION_STORE.pop(sid, None)
