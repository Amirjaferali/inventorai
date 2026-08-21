"""Workstream 7 — Actionable Validation Plan — BASE RED (contract §9).

File: tests/test_actionable_validation_plan.py
Purpose: deterministic BASE RED gate for the canonical Workstream 7 contract
(docs/governance/ACTIONABLE_VALIDATION_PLAN_INCREMENT_CONTRACT.md). Encodes
exactly six semantic RED cases (R1-R6, contract §9) that FAIL on the
pre-implementation BASE because the required owner-approved Section 14
presentation does not exist yet, plus exactly twelve protected-invariant
assertions (P1-P12, contract §9.1) that PASS on BASE and must keep passing
at HEAD.
Input contract: run under pytest from the repository root. Exercises ONLY the
real production path: the committed Flask routes (web.app), the real
engine.validation_plan.derive_validation_plan, the real
engine.deliverable_assembler.assemble_deliverable, and the committed
deliverable template. Deterministic fixtures; no network; no randomness in
any assertion; no monkeypatching of any production seam; no mocks.
Output contract: on BASE exactly 18 collected, 6 failed (R1-R6, one-to-one),
12 passed (P1-P12), 0 errors / 0 skipped / 0 xfailed.
Prohibited behaviors: MUST NOT modify production source, templates, any other
test, evidence, or governance state; MUST NOT use skip/xfail/conditional
pass/placeholder or artificial failures; MUST NOT name any specialist type,
tool, laboratory, simulation, standard, threshold, test method, product, or
service; MUST NOT imply that D13 (Technical Capability Gap Detection and
Actionable Research Guidance) is implemented or satisfied.
"""
import os
from test_p4_1b2a_durable_answer_append import answered_post  # P4-1b-2a
import re
import sys
import uuid

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.deliverable_assembler import assemble_deliverable
from engine.idea_state import (
    IdeaState,
    LEGACY_UNSPECIFIED,
    DISPOSITION_ANSWERED,
    DISPOSITION_UNKNOWN,
    DISPOSITION_DEFERRED,
    DISPOSITION_PROVISIONAL_ASSUMPTION,
    DISPOSITION_EVIDENCE_REQUESTED,
    DISPOSITION_SPECIALIST_REQUESTED,
)
from engine.requirement_landscape import derive_requirement_landscape
from engine.validation_plan import derive_validation_plan
from engine.progression_loop import select_next_gap
# PVCG-R2-I defect-dependent input correction (contract §3.2/§3.4):
# the shared WS1 gap-appropriate extension helper, defined once in
# test_structured_criticality.py and reused here rather than duplicated.
from test_structured_criticality import gap_appropriate
from web.app import app, SESSION_STORE, DOMAIN_CONFIRM_VALUE

# ---------------------------------------------------------------------------
# Contract §5 exact public wordings (byte-exact; owner-approved).
# ---------------------------------------------------------------------------
ANSWERED_ACTION_PREFIX = (
    "Validate this recorded answer against the available evidence: "
)


def expected_answered_action(requirement_statement):
    """The §5.1 requirement-linked answered action with the byte-verbatim
    embedded requirement statement (D3/C1)."""
    return ANSWERED_ACTION_PREFIX + "“" + requirement_statement + "”"


RESPONSIBILITY_UNDETERMINED_LINE_1 = "Responsibility has not yet been assigned."
RESPONSIBILITY_UNDETERMINED_LINE_2 = (
    "Choose who will own this validation step before relying on the result."
)
PENDING_EVIDENCE_ADVISORY = (
    "Additional evidence is still required for this item.\n"
    "Prepare or obtain the evidence identified in the recorded request "
    "before treating the item as validated."
)
PENDING_SPECIALIST_ADVISORY = (
    "Specialist input is still required for this item.\n"
    "The appropriate specialist has not yet been identified by the system."
)

# Current BASE vocabulary (for precondition proof only; the RED expectations
# above supersede it).
LEGACY_GENERIC_ANSWERED_ACTION = (
    "Validate the recorded answer against the available evidence."
)

# Workstream 6 disposition pass-through wordings (§5.6 unchanged vocabulary;
# protected, never amended — mirrors, without modifying, the Workstream 6 P5
# assertion in tests/test_requirement_landscape_synthesis.py).
WS6_DISPOSITION_ACTIONS = {
    DISPOSITION_UNKNOWN: (
        "This item remains unresolved. It may later be addressed through "
        "additional information, evidence, or specialist input."),
    DISPOSITION_DEFERRED: (
        "This item remains unresolved and can be revisited when you are "
        "ready to decide."),
    DISPOSITION_PROVISIONAL_ASSUMPTION: (
        "Validate, revise, or replace it before relying on it."),
}
WS6_DISPOSITION_LABELS = {
    DISPOSITION_UNKNOWN: "Recorded unknown",
    DISPOSITION_DEFERRED: "Deferred decision",
    DISPOSITION_PROVISIONAL_ASSUMPTION: "Provisional assumption",
}

ANSWERED_ANCHOR_LABEL = "Recorded answer"
FROZEN_RESPONSIBILITY_TOKENS = frozenset({
    "OWNER_EXECUTABLE", "SYSTEM_DERIVABLE", "SPECIALIST_REQUIRED",
    "EMPIRICAL_EVIDENCE_REQUIRED", "UNDETERMINED",
})

# ---------------------------------------------------------------------------
# Canonical Workstream 1 journey — byte-identical inputs to the committed
# baseline (docs/governance/evidence/workstream1_deliverable_baseline/
# inputs_false_negative_journey.json), driven through the REAL Flask flow.
# ---------------------------------------------------------------------------
IDEA_WS1 = (
    "A smart plug-in safety device that senses appliance current and voltage "
    "with a microcontroller and disconnects a relay to warn about dangerous "
    "appliances"
)
BASE_ANSWER = (
    "The current sensor detects an abnormal rise because the shunt "
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


def _run_ws1_journey():
    """Drive the committed Flask session flow with the canonical Workstream 1
    inputs and return (state, package, deliverable_html). Real routes and the
    real assembler only — nothing is mocked."""
    client = app.test_client()
    resp = client.post("/start", data={"idea": IDEA_WS1,
                                       "domain_confirm": DOMAIN_CONFIRM_VALUE})
    assert resp.status_code == 302, resp.status_code
    sid = resp.headers["Location"].rsplit("/", 1)[-1]
    for i in range(2, MAX_ITERATIONS + 2):
        page = client.get(f"/session/{sid}").get_data(as_text=True)
        if '<p class="complete">' in page:
            break
        if i == UNKNOWN_ITERATION:
            action, text = "unknown", UNKNOWN_TEXT
        else:
            action, text = "answered", gap_appropriate(
                BASE_ANSWER + DANGER_BY_ITERATION.get(i, ""),
                select_next_gap(SESSION_STORE[sid]["state"]))
        answered_post(client, sid, {"response": text, "action": action})
    state = SESSION_STORE[sid]["state"]
    package = assemble_deliverable(state)
    html = client.get(f"/session/{sid}/deliverable").get_data(as_text=True)
    SESSION_STORE.pop(sid, None)
    return state, package, html


@pytest.fixture(scope="module")
def ws1():
    state, package, html = _run_ws1_journey()
    return {"state": state, "package": package, "html": html}


# ---------------------------------------------------------------------------
# Minimal deterministic disposition fixtures (real ledger + real derivations).
# ---------------------------------------------------------------------------
ANSWERED_STATEMENT = (
    "The relay contacts are rated above the maximum expected appliance "
    "current, so switching does not weld the contacts.")
UNDETERMINED_STATEMENT = (
    "A previously imported note about enclosure venting whose origin was "
    "not recorded.")
EVIDENCE_REQUEST_STATEMENT = (
    "Measure the actual trip time of the relay under a representative "
    "overload condition.")
SPECIALIST_REQUEST_STATEMENT = (
    "Review whether the sensing approach is adequate for the intended "
    "protective function.")


def _answered_state():
    """One answered, owner-stated record (responsibility OWNER_EXECUTABLE)."""
    s = IdeaState(idea_id="ws7-answered")
    s.record_interaction(DISPOSITION_ANSWERED, iteration=0,
                         content=ANSWERED_STATEMENT)
    return s


def _undetermined_state():
    """One answered record whose provenance is LEGACY_UNSPECIFIED and whose
    responsibility is unrecorded, so the committed §7 precedence resolves the
    step responsibility to the internal token UNDETERMINED."""
    s = IdeaState(idea_id="ws7-undetermined")
    s.record_interaction(DISPOSITION_ANSWERED, iteration=0,
                         content=UNDETERMINED_STATEMENT,
                         provenance=LEGACY_UNSPECIFIED)
    return s


def _pending_evidence_state():
    s = IdeaState(idea_id="ws7-pending-evidence")
    s.record_interaction(DISPOSITION_EVIDENCE_REQUESTED, iteration=0,
                         content=EVIDENCE_REQUEST_STATEMENT)
    return s


def _pending_specialist_state():
    s = IdeaState(idea_id="ws7-pending-specialist")
    s.record_interaction(DISPOSITION_SPECIALIST_REQUESTED, iteration=0,
                         content=SPECIALIST_REQUEST_STATEMENT)
    return s


def _disposition_state():
    """One record for each of the three Workstream 6 dispositions."""
    s = IdeaState(idea_id="ws7-dispositions")
    s.record_interaction(DISPOSITION_UNKNOWN, iteration=0,
                         content="Unknown item content.")
    s.record_interaction(DISPOSITION_DEFERRED, iteration=0,
                         content="Deferred item content.")
    s.record_interaction(DISPOSITION_PROVISIONAL_ASSUMPTION, iteration=0,
                         content="Provisional item content.")
    return s


def _collapse_state():
    """Three byte-identical answered records (Phase 7B collapse fixture)."""
    s = IdeaState(idea_id="ws7-collapse")
    for _ in range(3):
        s.record_interaction(DISPOSITION_ANSWERED, iteration=0,
                             content=ANSWERED_STATEMENT)
    return s


def _render(state):
    """Render the committed deliverable route for a prepared state."""
    sid = "ws7-red-" + uuid.uuid4().hex[:8]
    SESSION_STORE[sid] = {"state": state, "last_result": None, "transcript": []}
    try:
        resp = app.test_client().get(f"/session/{sid}/deliverable")
        assert resp.status_code == 200, resp.status_code
        return resp.get_data(as_text=True)
    finally:
        SESSION_STORE.pop(sid, None)


def _section14_html(body):
    i = body.find("<h3>Validation Plan</h3>")
    assert i >= 0, "Section 14 heading not found in deliverable HTML"
    j = body.find("back-link", i)
    return body[i:(j if j > i else len(body))]


def _s14(package):
    return package["section_14_validation_plan"]


def _s13(package):
    return package["section_13_requirement_landscape"]


def _record_content(state, record_id):
    for r in state.assertions:
        if r.record_id == record_id:
            return r.content
    raise AssertionError(f"record not found: {record_id!r}")


def _answered_engine_steps(state):
    """Engine-level plan steps anchored on answered (legacy-label) records."""
    plan = derive_validation_plan(state)
    return [st for st in plan.steps
            if st.provenance.display_label == ANSWERED_ANCHOR_LABEL]


# ===========================================================================
# R1-R6 — intentional deterministic semantic RED failures (contract §9).
# ===========================================================================
def test_r1_answered_actions_must_be_requirement_linked_not_generic(ws1):
    """R1 — the canonical Workstream 1 journey's 12 answered steps currently
    share one generic statement; the owner-approved presentation requires each
    answered action to embed its own requirement statement (D3/C1)."""
    state = ws1["state"]
    answered = _answered_engine_steps(state)
    # Stable precondition (BASE and HEAD): exactly twelve answered steps.
    assert len(answered) == 12, [st.step_id for st in answered]
    # Proof of the current BASE defect, recorded in the failure output.
    generic = [st for st in answered
               if st.statement == LEGACY_GENERIC_ANSWERED_ACTION]
    # RED expectation: every answered action must be requirement-linked.
    mismatches = []
    for st in answered:
        content = _record_content(state, st.provenance.reference)
        expected = expected_answered_action(content.strip())
        if st.statement != expected:
            mismatches.append((st.step_id, st.statement))
    assert not mismatches, (
        f"{len(generic)} of {len(answered)} answered steps still share the "
        f"generic statement {LEGACY_GENERIC_ANSWERED_ACTION!r}; "
        f"requirement-linked differentiation is required: {mismatches!r}")


def test_r2_requirement_linked_wording_with_byte_verbatim_embed():
    """R2 — a minimal answered fixture must receive the exact §5.1 wording
    embedding the requirement statement byte-verbatim."""
    state = _answered_state()
    expected = expected_answered_action(ANSWERED_STATEMENT)
    plan = derive_validation_plan(state)
    assert len(plan.steps) == 1
    assert plan.steps[0].statement == expected
    package = assemble_deliverable(state)
    steps = _s14(package)["steps"]
    assert len(steps) == 1
    assert steps[0]["statement"] == expected


def test_r3_undetermined_responsibility_uses_honest_two_line_wording():
    """R3 — an UNDETERMINED-responsibility step must present the exact §5.2
    two-line wording while the internal token remains UNDETERMINED."""
    state = _undetermined_state()
    plan = derive_validation_plan(state)
    assert len(plan.steps) == 1
    # Internal token unchanged (passes on BASE and HEAD).
    assert plan.steps[0].responsibility == "UNDETERMINED"
    # RED expectation: the rendered Section 14 presents the two owner-approved
    # lines instead of the placeholder label "Responsibility undetermined".
    sec14 = _section14_html(_render(state))
    assert RESPONSIBILITY_UNDETERMINED_LINE_1 in sec14, sec14
    assert RESPONSIBILITY_UNDETERMINED_LINE_2 in sec14, sec14


def test_r4_meaningless_confidence_line_suppressed_in_html_json_unchanged():
    """R4 — HTML must not render a confidence line for UNDETERMINED while the
    JSON confidence fields and the internal token remain byte-unchanged."""
    state = _answered_state()
    plan = derive_validation_plan(state)
    assert plan.steps[0].confidence == "UNDETERMINED"
    step = _s14(assemble_deliverable(state))["steps"][0]
    # JSON byte-unchanged (passes on BASE and HEAD).
    assert step["confidence"] == "Confidence undetermined"
    assert step["confidence_label"] == "Confidence undetermined"
    # RED expectation: no rendered confidence fragment in Section 14.
    sec14 = _section14_html(_render(state))
    assert "Confidence:" not in sec14, sec14


def test_r5_pending_evidence_advisory_present_in_json_and_html():
    """R5 — the pending_evidence step must carry the exact §5.4 advisory in
    the additive per-step `advisory` field and in the rendered HTML."""
    state = _pending_evidence_state()
    steps = _s14(assemble_deliverable(state))["steps"]
    assert len(steps) == 1
    assert steps[0].get("advisory") == PENDING_EVIDENCE_ADVISORY, steps[0]
    sec14 = _section14_html(_render(state))
    for line in PENDING_EVIDENCE_ADVISORY.split("\n"):
        assert line in sec14, (line, sec14)


def test_r6_pending_specialist_advisory_present_in_json_and_html():
    """R6 — the pending_specialist step must carry the exact §5.5 advisory
    (including the explicit capability limitation) in the additive per-step
    `advisory` field and in the rendered HTML."""
    state = _pending_specialist_state()
    steps = _s14(assemble_deliverable(state))["steps"]
    assert len(steps) == 1
    assert steps[0].get("advisory") == PENDING_SPECIALIST_ADVISORY, steps[0]
    sec14 = _section14_html(_render(state))
    for line in PENDING_SPECIALIST_ADVISORY.split("\n"):
        assert line in sec14, (line, sec14)


# ===========================================================================
# P1-P12 — protected invariants (contract §9.1; PASS on BASE and HEAD).
# ===========================================================================
def test_p1_exactly_one_step_or_blocked_item_per_eligible_requirement(ws1):
    """P1 — one Section 14 step OR one blocked item per well-formed Section 13
    requirement, never both and never more."""
    state = ws1["state"]
    landscape = derive_requirement_landscape(state)
    plan = derive_validation_plan(state)
    covered = ([st.step_id[len("vstep:"):] for st in plan.steps]
               + [b.item_id[len("vblock:"):] for b in plan.blocked_items])
    expected = [r.requirement_id for r in landscape.requirements]
    assert sorted(covered) == sorted(expected)
    assert len(covered) == len(set(covered))


def test_p2_section13_section14_arithmetic_tie_unchanged(ws1):
    """P2 — the committed Section 13 <-> Section 14 arithmetic tie."""
    package = ws1["package"]
    s13, s14 = _s13(package), _s14(package)
    assert s14["validation_plan_source"] == "requirement_landscape"
    assert s14["validation_step_total"] == len(s14["steps"])
    assert s14["blocked_item_total"] == len(s14["blocked_items"])
    assert (s14["validation_step_total"] + s14["blocked_item_total"]
            == s13["total"] == len(s13["requirements"]))


def test_p3_vstep_and_vblock_id_schemes_unchanged(ws1):
    """P3 — every step id is `vstep:` + requirement id and every blocked id is
    `vblock:` + requirement id; no other scheme appears."""
    for state in (ws1["state"], _pending_evidence_state(),
                  _pending_specialist_state()):
        landscape = derive_requirement_landscape(state)
        rids = {r.requirement_id for r in landscape.requirements}
        plan = derive_validation_plan(state)
        for st in plan.steps:
            assert st.step_id.startswith("vstep:")
            assert st.step_id[len("vstep:"):] in rids
        for b in plan.blocked_items:
            assert b.item_id.startswith("vblock:")
            assert b.item_id[len("vblock:"):] in rids


def test_p4_source_requirement_ids_unchanged():
    """P4 — the Increment 4 requirement identifier scheme is unchanged for
    the three record-anchored kinds."""
    cases = (
        (_answered_state(), "req:assertion:rec_1"),
        (_pending_evidence_state(), "req:evidence:rec_1"),
        (_pending_specialist_state(), "req:specialist:rec_1"),
    )
    for state, expected_id in cases:
        landscape = derive_requirement_landscape(state)
        assert [r.requirement_id for r in landscape.requirements] == [expected_id]


def test_p5_landscape_inherited_order_unchanged(ws1):
    """P5 — Section 14 steps preserve the Increment 4 landscape order of the
    eligible requirements (organizational order only)."""
    state = ws1["state"]
    landscape = derive_requirement_landscape(state)
    plan = derive_validation_plan(state)
    eligible_order = ["vstep:" + r.requirement_id
                      for r in landscape.requirements
                      if "vstep:" + r.requirement_id
                      in {st.step_id for st in plan.steps}]
    assert [st.step_id for st in plan.steps] == eligible_order


def test_p6_section13_rows_statements_ids_order_byte_unchanged(ws1):
    """P6 — the Section 13 JSON rows mirror the landscape derivation
    byte-for-byte (statement, provenance label, resolving action, order) and
    carry no additive Workstream 7 field."""
    state, package = ws1["state"], ws1["package"]
    landscape = derive_requirement_landscape(state)
    rows = _s13(package)["requirements"]
    assert len(rows) == len(landscape.requirements)
    for row, req in zip(rows, landscape.requirements):
        assert row["statement"] == req.statement
        assert row["provenance"] == req.primary_anchor.display_label
        assert row["resolving_action"] == req.resolving_action.statement
        assert "advisory" not in row


def test_p7_disposition_passthrough_byte_unchanged():
    """P7 — the unknown / deferred / provisional_assumption Section 13 -> 14
    pass-through stays byte-unchanged (the Workstream 6 vocabulary; the
    Workstream 6 P5 assertion itself is never amended)."""
    state = _disposition_state()
    package = assemble_deliverable(state)
    rows = _s13(package)["requirements"]
    steps = _s14(package)["steps"]
    assert len(rows) == len(steps) == 3
    by_label = {row["provenance"]: row for row in rows}
    step_by_label = {st["provenance"]: st for st in steps}
    for disposition, label in WS6_DISPOSITION_LABELS.items():
        row, step = by_label[label], step_by_label[label]
        assert row["resolving_action"] == WS6_DISPOSITION_ACTIONS[disposition]
        assert step["statement"] == row["resolving_action"]


def test_p8_grouping_collapse_headers_and_count_wording_unchanged():
    """P8 — Phase 7A group headers and the Phase 7B collapse count wording
    are unchanged for identical answered rows."""
    state = _collapse_state()
    sec14 = _section14_html(_render(state))
    assert "Checks you can do yourself" in sec14
    assert sec14.count("(applies to 3 recorded answers)") == 1


def test_p9_inventor_statements_preserved_byte_verbatim(ws1):
    """P9 — recorded inventor statements appear byte-verbatim as Section 13
    requirement statements (minimal fixture and canonical journey)."""
    package = assemble_deliverable(_answered_state())
    assert [r["statement"] for r in _s13(package)["requirements"]] \
        == [ANSWERED_STATEMENT]
    ws1_statements = [r["statement"]
                      for r in _s13(ws1["package"])["requirements"]]
    assert BASE_ANSWER in ws1_statements
    assert UNKNOWN_TEXT in ws1_statements


def test_p10_internal_responsibility_and_confidence_tokens_unchanged(ws1):
    """P10 — the frozen internal responsibility vocabulary and the bounded
    UNDETERMINED confidence token are unchanged at the engine level."""
    for state in (ws1["state"], _answered_state(), _undetermined_state(),
                  _pending_evidence_state(), _pending_specialist_state()):
        plan = derive_validation_plan(state)
        for st in plan.steps:
            assert st.responsibility in FROZEN_RESPONSIBILITY_TOKENS
            assert st.confidence == "UNDETERMINED"
    undetermined_plan = derive_validation_plan(_undetermined_state())
    assert undetermined_plan.steps[0].responsibility == "UNDETERMINED"


def test_p11_advisory_absent_or_null_for_all_non_pending_rows(ws1):
    """P11 — the additive `advisory` field is absent or null on every
    non-pending Section 14 row (all canonical-journey rows are non-pending)."""
    s14 = _s14(ws1["package"])
    for st in s14["steps"]:
        assert st.get("advisory") is None, st
    for b in s14["blocked_items"]:
        assert b.get("advisory") is None, b


def test_p12_no_specialist_tool_threshold_or_d13_claim_in_section14(ws1):
    """P12 — no specialist type, tool, simulation, laboratory, standard,
    threshold, test method, product, confidence score, or D13-completion
    claim appears in the system-generated Section 14 vocabulary."""
    forbidden_system_vocabulary = re.compile(
        r"(oscilloscope|multimeter|laborator|simulation|test method"
        r"|electrical engineer|mechanical engineer"
        r"|\b(?:IEC|ISO|ASTM|EN)\s?\d"
        r"|\d+\s?(?:volts?|amps?|amperes?|ohms?|hertz|%))", re.IGNORECASE)
    d13_claim = re.compile(
        r"(technical capability gap|capability gap detect|research guidance"
        r"|specialist (?:was|has been) identified)", re.IGNORECASE)
    states = (ws1["state"], _pending_evidence_state(),
              _pending_specialist_state(), _undetermined_state())
    for state in states:
        package = assemble_deliverable(state)
        s14 = _s14(package)
        for st in s14["steps"]:
            system_fields = [
                st["responsibility"], st["responsibility_label"],
                st["evidence_category"], st["closure_condition"],
                st["provenance"], st["confidence"], st["confidence_label"],
                st.get("advisory") or "",
            ]
            for value in system_fields:
                assert not forbidden_system_vocabulary.search(value), value
            assert not any(ch.isdigit() for ch in st["confidence"])
            assert not any(ch.isdigit() for ch in st["confidence_label"])
        for b in s14["blocked_items"]:
            for value in (b["reason"], b["missing"], b["responsibility"],
                          b["responsibility_label"], b["provenance"]):
                assert not forbidden_system_vocabulary.search(value), value
        sec14 = _section14_html(_render(state))
        assert not d13_claim.search(sec14), sec14
