"""Workstream 6 — Requirement Landscape Synthesis: BASE RED gate.

File: tests/test_requirement_landscape_synthesis.py
Purpose: the single new focused test file authorized by the canonical
Workstream 6 Increment Contract (docs/governance/
REQUIREMENT_LANDSCAPE_SYNTHESIS_INCREMENT_CONTRACT.md; recording PR #189,
merge 90f1c34877743510535c397798fcd7da88693606; status canonicalized via
PR #190, merge fbe645a761b278b18f57b27a9d691880d989597f). On the authorized
base it proves (contract §9 R1-R5) that the required synthesis behavior is
ABSENT: byte-identical Requirement Landscape statements render repeatedly
with no truthful repetition sentence; `unknown`, `deferred`, and
`provisional_assumption` ledger records carry the legacy "Recorded answer"
vocabulary; the additive `_session_meta.requirement_landscape_synthesis`
object does not exist; and the empty-content placeholder carries the legacy
wording. At a future GREEN head these tests must prove the §7 owner-approved
public wordings byte-exact.
Input contract: exercises ONLY committed real paths — the web journey
(web.app test client with the byte-identical Workstream 1 baseline inputs),
minimal deterministic disposition fixtures on the in-memory IdeaState in
web.app.SESSION_STORE, engine.deliverable_assembler.assemble_deliverable,
engine.requirement_landscape.derive_requirement_landscape, and the rendered
/session/<sid>/deliverable HTML. Deterministic committed inputs only; no
mocks, no network, no dependency on PR #167 or PR #162.
Output contract: "PROTECTED INVARIANT" tests (P1-P6) must pass on base AND
at head — they pin the contract §3 frozen guarantees (row count, requirement
IDs, ordering, byte-verbatim statements, the Section 13-to-Section 14
arithmetic and statement pass-through ties, the pinned top-level package key
set, and the Workstream 4/5 protections). "RED" tests (R1-R5) must FAIL on
the authorized base for the intended semantic reasons only, with every
required wording pinned byte-exactly to contract §7. Zero skipped and zero
xfailed tests at every stage.
Prohibited behaviors: must not modify production source, templates, any
other test file, fixtures, or evidence; must not use prefix, normalized,
semantic, fuzzy, or AI-based statement comparison (byte-identical only);
must not group or require grouping of non-byte-identical statements; must
not require any Workstream 7 logic, responsibility, confidence, grouping,
count, referral, tool-guidance, validation-planning, or structural change;
must not assert implementation-chosen mechanics beyond the names and
wordings the contract itself pins.
"""
import html as html_module
import json

import pytest

from web.app import app, SESSION_STORE, DOMAIN_CONFIRM_VALUE
from engine.deliverable_assembler import assemble_deliverable
from engine.requirement_landscape import derive_requirement_landscape
from engine.idea_state import (
    IdeaState,
    DISPOSITION_UNKNOWN,
    DISPOSITION_DEFERRED,
    DISPOSITION_PROVISIONAL_ASSUMPTION,
    DISPOSITION_ANSWERED,
)

# --- Byte-identical committed journey inputs (WS1 baseline) — copied verbatim
# from the committed evidence harnesses and the Workstream 5 gate ------------
IDEA_WS1 = (
    "A smart plug-in safety device that senses appliance current and voltage "
    "with a microcontroller and disconnects a relay to warn about dangerous "
    "appliances"
)
CORE = ("The current sensor detects an abnormal rise because the shunt "
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

# The six distinct WS1-journey statements (byte-identical vocabulary only).
VARIANTS = [CORE + suffix for suffix in DANGER_BY_ITERATION.values()]
DISTINCT_STATEMENTS = [CORE] + VARIANTS + [UNKNOWN_TEXT]
EXPECTED_CORE_REPEATS = 8          # owner-pinned count for the WS1 journey
EXPECTED_ROW_TOTAL = 13

# --- Contract §7 owner-approved exact public wordings (byte-exact) -----------
REPETITION_SENTENCE = "This statement was recorded {n} times during the session."

UNKNOWN_LABEL = "Recorded unknown"
UNKNOWN_STATUS = "You indicated that this is not known yet."
UNKNOWN_ACTION = ("This item remains unresolved. It may later be addressed "
                  "through additional information, evidence, or specialist input.")

DEFERRED_LABEL = "Deferred decision"
DEFERRED_STATUS = "You chose to defer this item."
DEFERRED_ACTION = ("This item remains unresolved and can be revisited when "
                   "you are ready to decide.")

PROVISIONAL_LABEL = "Provisional assumption"
PROVISIONAL_STATUS = ("This assumption was recorded as a temporary direction "
                      "and has not been validated.")
PROVISIONAL_ACTION = "Validate, revise, or replace it before relying on it."

PLACEHOLDER_WORDING = (
    "Insufficient information was recorded to organize this item reliably.\n"
    "This does not indicate that the idea is invalid; the item remains unresolved.")

# --- Legacy vocabulary the corrected output must not use for these records ---
LEGACY_LABEL = "Recorded answer"
LEGACY_STATUS = "Recorded from your answers (not yet verified)"
LEGACY_ACTION = "Validate the recorded answer against the available evidence."
LEGACY_PLACEHOLDER = "Recorded answer awaiting restatement."

# --- Protected constants (contract §3/§8 frozen guarantees) ------------------
FROZEN_S13_DISCLAIMER = (
    "No structurally grounded risks are recorded for the current requirements. "
    "This is not a statement that the idea is risk-free, safe, or verified; it "
    "means no structural adverse-consequence signal exists in the recorded state."
)
EXPECTED_TOP_LEVEL_KEYS = {
    "package_version", "schema_id", "session_id", "generated_at",
    "section_1_disclaimer", "section_2_invention_summary",
    "section_3_assessment_overview", "section_4_requirements",
    "section_5_assumptions", "section_6_risks", "section_7_recommendations",
    "section_8_unresolved_items", "section_9_stage3_reasoning",
    "section_10_recommended_next_steps", "section_11_prototype_test_plan",
    "section_12_next_development_step", "section_13_requirement_landscape",
    "section_14_validation_plan", "_session_meta",
}


# --- Helpers (test-only, deterministic) --------------------------------------
def _section13(body):
    """The rendered Section 13 region (unescaped), from the 'Requirement
    Landscape' heading to the following 'What is assumed' block."""
    i = body.find("<h3>Requirement Landscape</h3>")
    assert i >= 0, "fixture defect: Section 13 heading not found"
    j = body.find("What is assumed", i)
    return html_module.unescape(body[i:(j if j > i else len(body))])


def _standalone_counts(section_text, statements):
    """Exact standalone occurrence count per statement, byte-identical only.

    Longer statements are counted and removed first so a statement that is a
    byte-exact prefix of another (the WS1 core sentence inside its appended
    variants) is never miscounted. No prefix, normalized, semantic, fuzzy, or
    AI-based matching — plain byte-identical substring counting.
    """
    working = section_text
    counts = {}
    for idx, stmt in enumerate(
            sorted(statements, key=len, reverse=True)):
        counts[stmt] = working.count(stmt)
        working = working.replace(stmt, f"<removed:{idx}>")
    return counts


def _start(idea):
    client = app.test_client()
    r = client.post("/start", data={"idea": idea,
                                    "domain_confirm": DOMAIN_CONFIRM_VALUE})
    assert r.status_code == 302, "fixture defect: /start did not redirect"
    return client, r.headers["Location"].rsplit("/", 1)[-1]


@pytest.fixture()
def ws1_journey():
    """Completed WS1 baseline journey (byte-identical committed inputs).
    Fails loudly (fixture defect, not a RED signal) if the deterministic
    journey shape drifts from the recorded baseline."""
    client, sid = _start(IDEA_WS1)
    for i in range(2, MAX_ITERATIONS + 2):
        page = client.get(f"/session/{sid}").get_data(as_text=True)
        if '<p class="complete">' in page:
            break
        if i == UNKNOWN_ITERATION:
            action, text = "unknown", UNKNOWN_TEXT
        else:
            action, text = "answered", CORE + DANGER_BY_ITERATION.get(i, "")
        client.post(f"/session/{sid}", data={"response": text, "action": action})
    else:
        pytest.fail("fixture defect: WS1 journey did not complete")
    state = SESSION_STORE[sid]["state"]
    package = assemble_deliverable(state)
    rows = package["section_13_requirement_landscape"]["requirements"]
    statements = [r["statement"] for r in rows]
    if len(rows) != EXPECTED_ROW_TOTAL:
        pytest.fail("fixture defect: WS1 journey produced %d Section 13 rows, "
                    "expected %d" % (len(rows), EXPECTED_ROW_TOTAL))
    if statements.count(CORE) != EXPECTED_CORE_REPEATS:
        pytest.fail("fixture defect: WS1 journey produced %d byte-identical "
                    "core rows, expected %d"
                    % (statements.count(CORE), EXPECTED_CORE_REPEATS))
    if set(statements) != set(DISTINCT_STATEMENTS):
        pytest.fail("fixture defect: WS1 journey statement set drifted from "
                    "the recorded baseline")
    html = client.get(f"/session/{sid}/deliverable").get_data(as_text=True)
    yield state, package, html
    SESSION_STORE.pop(sid, None)


def _single_record_fixture(disposition, content):
    """Minimal deterministic single-record fixture rendered through the real
    deliverable route. Disposition selection uses ONLY the exact existing
    AssertionRecord.disposition value — no lexical or quality inference."""
    import uuid
    state = IdeaState(idea_id="ws6-" + uuid.uuid4().hex[:8])
    state.record_interaction(disposition, content=content, iteration=0)
    sid = "ws6-render-" + uuid.uuid4().hex[:8]
    SESSION_STORE[sid] = {"state": state, "last_result": None, "transcript": []}
    try:
        package = assemble_deliverable(state)
        html = app.test_client().get(
            f"/session/{sid}/deliverable").get_data(as_text=True)
    finally:
        SESSION_STORE.pop(sid, None)
    rows = package["section_13_requirement_landscape"]["requirements"]
    assert len(rows) == 1, "fixture defect: expected exactly one Section 13 row"
    return state, package, rows[0], html


def _assert_truthful_vocabulary(row, sec, label, status, action, content):
    """Contract §7 byte-exact wording assertions for one disposition row
    (JSON and HTML), plus the frozen byte-verbatim statement guarantee."""
    # Frozen guarantee first: the inventor statement itself is untouched.
    assert row["statement"] == content            # byte-verbatim, untruncated
    # RED at base: the legacy vocabulary is still in place.
    assert row["provenance"] == label, (
        "Section 13 provenance must use the owner-approved wording %r; "
        "found %r" % (label, row["provenance"]))
    assert row["status"] == status
    assert row["resolving_action"] == action
    # Rendered HTML carries the same owner-approved wordings.
    assert label in sec
    assert status in sec
    assert action in sec


# =============================================================================
# GROUP P — PROTECTED INVARIANTS (must PASS on base AND at head).
# =============================================================================

def test_p1_ws1_rows_ids_ordering_and_section14_tie(ws1_journey):
    """Contract §3: row count, requirement IDs, ordering, and the Section
    13-to-Section 14 arithmetic tie are frozen. No new anchor kind or
    requirement-ID prefix may ever appear for these records."""
    state, package, _ = ws1_journey
    landscape = derive_requirement_landscape(state)
    ids = [r.requirement_id for r in landscape.requirements]
    assert ids == ["req:assertion:rec_%d" % i
                   for i in range(1, EXPECTED_ROW_TOTAL + 1)]
    s13 = package["section_13_requirement_landscape"]
    s14 = package["section_14_validation_plan"]
    assert s13["total"] == len(s13["requirements"]) == EXPECTED_ROW_TOTAL
    assert (s14["validation_step_total"] + s14["blocked_item_total"]
            == s13["total"])


def test_p2_distinct_statements_each_fully_visible_exactly_once_or_more(ws1_journey):
    """Contract §9 R1 invariant (base-holding side): every non-byte-identical
    statement in the approved RED fixture is fully visible in the rendered
    Section 13 — at base each appears exactly once standalone; at head each
    must REMAIN fully visible exactly once. Byte-identical counting only."""
    _, _, html = ws1_journey
    sec = _section13(html)
    counts = _standalone_counts(sec, DISTINCT_STATEMENTS)
    for stmt in VARIANTS + [UNKNOWN_TEXT]:
        assert counts[stmt] == 1, (
            "non-byte-identical statement must remain fully visible exactly "
            "once: %r (count %d)" % (stmt[:60], counts[stmt]))


def test_p3_statements_byte_verbatim_and_untruncated(ws1_journey):
    """Contract §3: inventor statements stay byte-verbatim in the Section 13
    JSON rows — never paraphrased, truncated, or reworded."""
    _, package, _ = ws1_journey
    statements = [r["statement"]
                  for r in package["section_13_requirement_landscape"]["requirements"]]
    assert statements.count(CORE) == EXPECTED_CORE_REPEATS
    for stmt in DISTINCT_STATEMENTS:
        assert stmt in statements


def test_p4_no_new_top_level_package_key(ws1_journey):
    """Contract §3/D5: additive nesting only — the top-level deliverable key
    set is unchanged; new metadata may live only under _session_meta."""
    _, package, _ = ws1_journey
    assert set(package) == EXPECTED_TOP_LEVEL_KEYS


def test_p5_section13_to_section14_statement_passthrough_tie():
    """Contract §4.1: Section 14 consumes the landscape's resolving action and
    anchor label unchanged (pass-through tie). Holds at base (legacy wording
    on both sides) and must hold at head (approved wording on both sides) —
    with NO Workstream 7 logic, count, or structure change."""
    for disposition, content in (
            (DISPOSITION_UNKNOWN, "I don't know the safe cutoff current yet."),
            (DISPOSITION_DEFERRED, "I will decide the enclosure later."),
            (DISPOSITION_PROVISIONAL_ASSUMPTION, "Assume a 5V relay coil for now.")):
        _, package, row, _ = _single_record_fixture(disposition, content)
        s14 = package["section_14_validation_plan"]
        assert s14["validation_step_total"] + s14["blocked_item_total"] == 1
        entries = s14["steps"] + s14["blocked_items"]
        entry = entries[0]
        assert entry["provenance"] == row["provenance"]
        if s14["steps"]:
            assert entry["statement"] == row["resolving_action"]


def test_p6_ws4_criticality_and_ws5_linkage_protected(ws1_journey):
    """Contract §3: Workstream 4 criticality fields and the Workstream 5
    linkage object remain untouched; the frozen Section 13 zero-risk
    disclaimer is byte-identical."""
    _, package, _ = ws1_journey
    s13 = package["section_13_requirement_landscape"]
    assert s13["risk_disclaimer"] == FROZEN_S13_DISCLAIMER
    for row in s13["requirements"]:
        assert row["criticality"] == "Not yet determined"
        assert row["criticality_authority"] == (
            "assigned automatically by the system; not yet reviewed")
    assert "risk_safety_linkage" in package["_session_meta"]


# =============================================================================
# GROUP R — BASE RED (must FAIL on the authorized base for the intended
# semantic reasons only; at a future GREEN head they must pass).
# =============================================================================

def test_r1_exact_repeat_rendered_once_with_owner_count_wording(ws1_journey):
    """Contract §9 R1: the byte-identical WS1 core statement renders once with
    exactly the owner-approved repetition sentence. BASE renders it 8 times
    with no count sentence, so this fails at base. Byte-identical grouping
    only — the appended-clause variants are asserted separately visible by
    the P2 invariant and must never be grouped into the core statement."""
    _, _, html = ws1_journey
    sec = _section13(html)
    counts = _standalone_counts(sec, DISTINCT_STATEMENTS)
    expected_sentence = REPETITION_SENTENCE.format(n=EXPECTED_CORE_REPEATS)
    assert counts[CORE] == 1, (
        "the byte-identical statement must be presented once (found %d "
        "standalone renderings)" % counts[CORE])
    assert expected_sentence in sec, (
        "missing owner-approved repetition wording: %r" % expected_sentence)


def test_r2_recorded_unknown_truthful_vocabulary():
    """Contract §9 R2: an `unknown`-disposition record must carry the exact
    §7.1 wordings in JSON and HTML instead of the legacy 'Recorded answer'
    vocabulary. Fails at base on the legacy vocabulary."""
    content = "I don't know the safe cutoff current yet."
    _, package, row, html = _single_record_fixture(DISPOSITION_UNKNOWN, content)
    sec = _section13(html)
    _assert_truthful_vocabulary(
        row, sec, UNKNOWN_LABEL, UNKNOWN_STATUS, UNKNOWN_ACTION, content)
    assert LEGACY_LABEL != row["provenance"]
    assert LEGACY_ACTION != row["resolving_action"]


def test_r3_deferred_decision_truthful_vocabulary():
    """Contract §9 R3 (deferred): exact §7.2 wordings replace the legacy
    generic vocabulary. Fails at base."""
    content = "I will decide the enclosure later."
    _, package, row, html = _single_record_fixture(DISPOSITION_DEFERRED, content)
    sec = _section13(html)
    _assert_truthful_vocabulary(
        row, sec, DEFERRED_LABEL, DEFERRED_STATUS, DEFERRED_ACTION, content)


def test_r3_provisional_assumption_truthful_vocabulary():
    """Contract §9 R3 (provisional_assumption): exact §7.3 wordings replace
    the legacy generic vocabulary. Fails at base."""
    content = "Assume a 5V relay coil for now."
    _, package, row, html = _single_record_fixture(
        DISPOSITION_PROVISIONAL_ASSUMPTION, content)
    sec = _section13(html)
    _assert_truthful_vocabulary(
        row, sec, PROVISIONAL_LABEL, PROVISIONAL_STATUS, PROVISIONAL_ACTION,
        content)


def test_r4_requirement_landscape_synthesis_metadata_with_parity(ws1_journey):
    """Contract §9 R4: the additive _session_meta.requirement_landscape_synthesis
    object exists (additive nesting only; no new top-level key; Section 13
    rows, count, IDs, and ordering unchanged — pinned by P1/P4), is JSON-safe,
    and its repetition facts are machine-consistent with BOTH the Section 13
    JSON rows and the rendered HTML (parity by machine-built values, not
    independent substrings). Fails at base because the object does not exist."""
    state, package, html = ws1_journey
    meta = package["_session_meta"]
    assert "requirement_landscape_synthesis" in meta, (
        "_session_meta.requirement_landscape_synthesis does not exist")
    rls = meta["requirement_landscape_synthesis"]
    json.dumps(rls)                       # JSON-safe additive metadata only
    rows = package["section_13_requirement_landscape"]["requirements"]
    sec = _section13(html)

    # --- Direct machine-comparable METADATA <-> JSON parity (GREEN
    # strengthening carried forward from the PR #191 merge record): every
    # metadata statement group's occurrence_count must equal the number of
    # FULLY byte-identical Section 13 rows (statement AND metadata), and its
    # repetition_note must be exactly the owner sentence built from that
    # derived count (None for a single occurrence). The groups must cover
    # every inventor-record row exactly once.
    def _row_key(r):
        return (r["statement"], r["provenance"], r["status"],
                r["criticality"], r["criticality_authority"],
                r["criticality_rationale"], r["resolving_action"])
    groupable = [r for r in rows
                 if r["provenance"] in ("Recorded answer", "Recorded unknown",
                                        "Deferred decision",
                                        "Provisional assumption")]
    groups = rls["statement_groups"]
    assert sum(g["occurrence_count"] for g in groups) == len(groupable)
    assert rls["group_total"] == len(groups)
    for g in groups:
        expected_count = sum(1 for r in groupable if _row_key(r) == (
            g["statement"], g["provenance"], g["status"], g["criticality"],
            g["criticality_authority"], g["criticality_rationale"],
            g["resolving_action"]))
        assert g["occurrence_count"] == expected_count, (
            "metadata count %d disagrees with the %d byte-identical JSON "
            "rows for %r" % (g["occurrence_count"], expected_count,
                             g["statement"][:60]))
        if g["occurrence_count"] > 1:
            assert g["repetition_note"] == REPETITION_SENTENCE.format(
                n=g["occurrence_count"])
        else:
            assert g["repetition_note"] is None
    assert rls["repeated_group_total"] == sum(
        1 for g in groups if g["occurrence_count"] > 1)

    # --- Direct machine-comparable METADATA <-> HTML parity: the rendered
    # HTML must present exactly the metadata's statements and repetition
    # sentences — the note string asserted below is taken FROM the metadata
    # (never rebuilt independently), the statement must render standalone
    # exactly once, and the total number of rendered repetition sentences
    # must equal the metadata's repeated-group total, so the test fails if
    # metadata says one count or statement while HTML presents another.
    rendered = _standalone_counts(
        sec, sorted({g["statement"] for g in groups}, key=len))
    for g in groups:
        assert rendered[g["statement"]] == 1, (
            "metadata statement not rendered standalone exactly once: %r"
            % g["statement"][:60])
        if g["repetition_note"] is not None:
            assert g["repetition_note"] in sec, (
                "metadata repetition sentence missing from HTML: %r"
                % g["repetition_note"])
    assert sec.count("This statement was recorded ") == (
        rls["repeated_group_total"]), (
        "HTML presents a different number of repetition sentences than the "
        "metadata records")


def test_r5_empty_content_placeholder_owner_wording():
    """Contract §9 R5: the existing empty-content placeholder path (and ONLY
    that path — no insufficiency inference from answer quality, technical
    complexity, domain, wording, or vocabulary) must emit the exact owner
    two-line wording. Fails at base on the legacy placeholder."""
    _, package, row, html = _single_record_fixture(DISPOSITION_ANSWERED, "")
    assert row["statement"] == PLACEHOLDER_WORDING, (
        "empty-content placeholder must use the owner-approved wording; "
        "found %r" % row["statement"])
    assert row["statement"] != LEGACY_PLACEHOLDER
    sec = _section13(html)
    assert PLACEHOLDER_WORDING.split("\n")[0] in sec
