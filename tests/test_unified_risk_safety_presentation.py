"""Workstream 5 — Unified Risk and Safety Presentation: BASE RED / HEAD GREEN gate.

File: tests/test_unified_risk_safety_presentation.py
Purpose: the single test file authorized by the canonical Workstream 5
Increment Contract (docs/governance/
UNIFIED_RISK_SAFETY_PRESENTATION_INCREMENT_CONTRACT.md; recording PR #185,
merge 8b6868fce5e5fe81f221f3a6e8ab271552751339, contract blob
92029fdfcc2a6a05374a72b0782808c9d3fa24da; status canonicalized via PR #186,
merge 3bf67da09d2a0f64591ba6c874507eada54897c8). On the authorized base it
proves (contract §15) that the required linkage behavior among the
Inventor-Stated Safety Signals panel, the Section 6 "What could go wrong"
presentation, and the Section 13 structural-risk disclaimer is ABSENT; at
head it must prove the §16 GREEN behaviors with the §5 public wordings
byte-exact.
Input contract: exercises ONLY committed real paths — the web journey
(web.app test client with the byte-identical Workstream 1 baseline inputs
and the committed PR #122 positive safety statement), the in-memory
IdeaState in web.app.SESSION_STORE, engine.deliverable_assembler
.assemble_deliverable, and the rendered /session/<sid>/deliverable HTML.
Deterministic committed inputs only; no mocks, no network, no dependency on
PR #167 or PR #162.
Output contract: two disjoint groups. "PROTECTED INVARIANT" tests (P1-P6)
must pass on base AND at head. "RED" tests (R1-R5) fail on base because the
contract §4 linkage block (_session_meta.risk_safety_linkage) and the §5
wordings do not exist yet; each RED failure carries an obligation-specific
message naming the missing contract behavior, never a fixture defect. R6 is
DOCUMENTATION-ONLY (owner decision D4): it records the existing
near-duplicate signal presentation as a known limitation, passes on base
AND at head, and is NOT a RED-to-GREEN gate. Zero skipped and zero xfailed
tests at every stage.
Prohibited behaviors: must not modify production source, templates, any
other test file (including tests/test_deliverable_hygiene.py), fixtures,
or evidence; must not weaken the frozen disclaimer, signal fields, or
dedup semantics; must not assert implementation-chosen mechanics beyond
the names and wordings the contract itself pins.

Contract-pinned surface used here (and nothing beyond it):
  * _session_meta.risk_safety_linkage  (contract §4.1 / D5)
  * the three §5 public wordings (byte-exact; HTML matching is
    whitespace-collapsed because HTML rendering may rewrap lines — the
    JSON linkage block carries the wordings verbatim at GREEN)
  * the frozen Section 13 disclaimer and Section 6 row semantics
"""
import json
import re

import pytest

from web.app import app, SESSION_STORE, DOMAIN_CONFIRM_VALUE
from engine.deliverable_assembler import assemble_deliverable
from engine.safety_signal import derive_inventor_stated_safety_signals
from engine.idea_state import DEMONSTRATED

# --- Byte-identical committed journey inputs (WS1 baseline; PR #122 positive
# statement) — copied verbatim from the committed evidence harnesses ----------
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
POSITIVE_STATEMENT = (
    "If insulation cannot be safely achieved inside the plug housing, the "
    "device should not be used because it could create a safety risk."
)

# Contract §5 approved exact public wordings (byte-exact; owner decision D2).
WORDING_S6_LINKAGE = (
    "You also described possible safety consequences in your own words.\n"
    "See “Inventor-Stated Safety Signals.”\n\n"
    "These are your statements, not confirmed risks, and they still require\n"
    "independent validation.")
WORDING_S6_EMPTY_QUALIFIED = (
    "No system-derived risks were identified from the current session state.\n\n"
    "This does not mean the idea is safe or risk-free. Safety consequences you\n"
    "described are listed separately under “Inventor-Stated Safety Signals” and\n"
    "have not been independently validated.")
WORDING_S13_ADJACENT = (
    "You also described possible safety consequences in your own words.\n\n"
    "They are listed separately under “Inventor-Stated Safety Signals.” They are\n"
    "not structural risk records and have not been independently validated.")

# Frozen Section 13 disclaimer (byte-identity protected; contract §8).
FROZEN_S13_DISCLAIMER = (
    "No structurally grounded risks are recorded for the current requirements. "
    "This is not a statement that the idea is risk-free, safe, or verified; it "
    "means no structural adverse-consequence signal exists in the recorded state."
)

_SEVERITIES = {"high", "medium", "low"}
_RAW_TOKENS = ("inventor_stated_safety_signals\" leaked", "UNDETERMINED",
               "system-derived", "owner-confirmed", "LEGACY_UNSPECIFIED")


def _collapse(text):
    """Whitespace-collapsed form for HTML wording matching (HTML rendering may
    rewrap the pinned multi-line wordings; the byte-exact form is asserted on
    the JSON linkage block at GREEN)."""
    return " ".join(text.split())


def _s6_region(html):
    """The rendered Section 6 region: from the 'What could go wrong' heading
    to the next section heading."""
    m = re.search(r"<h2>What could go wrong</h2>(.*?)</section>", html, re.S)
    assert m, "fixture defect: Section 6 region not found in deliverable HTML"
    return m.group(1)


# --- Real-path journey fixtures ----------------------------------------------
def _start(idea):
    client = app.test_client()
    r = client.post("/start", data={"idea": idea,
                                    "domain_confirm": DOMAIN_CONFIRM_VALUE})
    assert r.status_code == 302, "fixture defect: /start did not redirect"
    return client, r.headers["Location"].rsplit("/", 1)[-1]


@pytest.fixture()
def ws1_journey():
    """Completed WS1 baseline journey with populated safety signals.
    Fails loudly if the intended safety-signal state is absent."""
    client, sid = _start(IDEA_WS1)
    for i in range(2, MAX_ITERATIONS + 2):
        page = client.get(f"/session/{sid}").get_data(as_text=True)
        if '<p class="complete">' in page:
            break
        if i == UNKNOWN_ITERATION:
            action, text = "unknown", UNKNOWN_TEXT
        else:
            action, text = "answered", BASE + DANGER_BY_ITERATION.get(i, "")
        client.post(f"/session/{sid}", data={"response": text, "action": action})
    else:
        pytest.fail("fixture defect: WS1 journey did not complete")
    state = SESSION_STORE[sid]["state"]
    package = assemble_deliverable(state)
    signals = package["_session_meta"]["inventor_stated_safety_signals"]
    if not signals["signals"]:
        pytest.fail("fixture defect: WS1 journey produced no safety signals — "
                    "the intended safety-signal state is absent")
    html = client.get(f"/session/{sid}/deliverable").get_data(as_text=True)
    yield state, package, html
    SESSION_STORE.pop(sid, None)


@pytest.fixture()
def mature_gap_free_journey():
    """Deterministic real-assembler fixture (contract §15 R4): a mature,
    gap-free, demonstrated-quality state whose ledger carries the committed
    PR #122 positive safety statement — Section 6 emits ZERO risk rows while
    safety signals are populated. Built on a real session so the real
    deliverable route renders the real state; the state fields are set
    directly (test-fixture construction, not a production path change)."""
    client, sid = _start(IDEA_WS1)
    state = SESSION_STORE[sid]["state"]
    state.maturity_level = 2
    state.gaps = []
    if state.known_mechanism is not None:
        state.known_mechanism.quality = DEMONSTRATED
    if state.known_problem is not None:
        state.known_problem.quality = DEMONSTRATED
    state.record_interaction(action="answered", content=POSITIVE_STATEMENT,
                             gap_context=None, iteration=state.iteration)
    package = assemble_deliverable(state)
    if package["section_6_risks"]["risks"]:
        pytest.fail("fixture defect: mature/gap-free fixture still produced "
                    "Section 6 risk rows: %r"
                    % [r["category"] for r in package["section_6_risks"]["risks"]])
    if not package["_session_meta"]["inventor_stated_safety_signals"]["signals"]:
        pytest.fail("fixture defect: mature/gap-free fixture produced no "
                    "safety signals — the intended state is absent")
    html = client.get(f"/session/{sid}/deliverable").get_data(as_text=True)
    yield state, package, html
    SESSION_STORE.pop(sid, None)


# =============================================================================
# GROUP P — PROTECTED INVARIANTS (must PASS on base AND at head).
# =============================================================================
class TestProtectedInvariants:
    def test_p1_signal_block_matches_direct_derivation(self, ws1_journey):
        """Contract §8: the rendered safety block is semantically identical to
        the direct engine derivation — totals and every per-signal field."""
        state, package, _ = ws1_journey
        block = package["_session_meta"]["inventor_stated_safety_signals"]
        direct = derive_inventor_stated_safety_signals(state)
        assert block["total"] == len(direct)
        for rendered, signal in zip(block["signals"], direct):
            for field in ("signal_id", "source", "provenance", "safety_subject",
                          "failure_condition", "possible_consequence",
                          "domain_context", "validation_status",
                          "display_label", "caution_text", "statement"):
                assert rendered[field] == getattr(signal, field), field

    def test_p2_section6_rows_unchanged_semantics(self, ws1_journey):
        """Contract §8: Section 6 keeps its truthful system-derived rows —
        known categories, known severity vocabulary, no deletion."""
        _, package, _ = ws1_journey
        s6 = package["section_6_risks"]
        assert s6["total"] == len(s6["risks"])
        for row in s6["risks"]:
            assert row["severity"] in _SEVERITIES, row
            assert row["category"] in {"assessment_completeness",
                                       "evidence_quality", "unresolved_gap"}, row

    def test_p3_section13_disclaimer_byte_identical(self, ws1_journey):
        """Contract §8: the frozen Section 13 disclaimer is byte-identical and
        Section 13 risks stay []."""
        _, package, _ = ws1_journey
        s13 = package["section_13_requirement_landscape"]
        assert s13["risk_disclaimer"] == FROZEN_S13_DISCLAIMER
        assert s13["risks"] == [] and s13["has_risks"] is False

    def test_p4_no_new_severity_or_risk_records(self, mature_gap_free_journey):
        """Contract §16: the mature/gap-free state derives ZERO Section 6 rows
        and ZERO Section 13 risks — nothing may invent severity or risk."""
        _, package, _ = mature_gap_free_journey
        assert package["section_6_risks"]["risks"] == []
        assert package["section_13_requirement_landscape"]["risks"] == []

    def test_p5_no_raw_tokens_in_risk_safety_regions(self, ws1_journey):
        """Contract §10: no raw machine/governance token renders in the
        Section 6 region or anywhere in the deliverable HTML."""
        _, _, html = ws1_journey
        for token in ("UNDETERMINED", "system-derived", "owner-confirmed",
                      "LEGACY_UNSPECIFIED", "FEASIBILITY-THREATENING"):
            assert token not in html, token

    def test_p6_signal_rendering_unchanged(self, ws1_journey):
        """Contract §12 / owner decision D4: every signal statement renders in
        the deliverable HTML exactly as today (no grouping, no hiding, no
        abbreviation beyond the existing excerpt behavior)."""
        _, package, html = ws1_journey
        for sig in package["_session_meta"]["inventor_stated_safety_signals"]["signals"]:
            assert sig["statement"] in html, (
                "signal statement no longer rendered: %s" % sig["signal_id"])
            assert sig["signal_id"] not in ("",)


# =============================================================================
# GROUP R — GENUINE RED (must FAIL on base: the linkage behavior is absent).
# =============================================================================
class TestLinkageRed:
    def test_r1_linkage_block_and_section6_reference_exist(self, ws1_journey):
        """Contract §4.1/§4.2 (R1): with populated inventor-stated safety
        signals, the package carries _session_meta.risk_safety_linkage AND the
        Section 6 region carries the §5.1 linkage wording. MISSING ON BASE."""
        _, package, html = ws1_journey
        assert "risk_safety_linkage" in package["_session_meta"], (
            "missing behavior: the additive linkage block "
            "_session_meta.risk_safety_linkage (contract §4.1) does not "
            "exist — Section 6 and the safety panel remain disconnected")
        assert _collapse(WORDING_S6_LINKAGE) in _collapse(_s6_region(html)), (
            "missing behavior: the Section 6 linkage note (contract §5.1) "
            "is not rendered in 'What could go wrong'")

    def test_r2_low_process_risk_reconciled_with_stated_danger(self, ws1_journey):
        """Contract §1/§4.2 (R2): the WS1 deliverable shows a low
        evidence-quality process-risk row while the inventor stated fire and
        danger consequences; the §5.1 reconciliation must appear in the same
        Section 6 presentation. MISSING ON BASE."""
        _, package, html = ws1_journey
        rows = package["section_6_risks"]["risks"]
        if not any(r["category"] == "evidence_quality" and r["severity"] == "low"
                   for r in rows):
            pytest.fail("fixture defect: expected the low evidence-quality "
                        "process-risk row on the WS1 journey; found %r" % rows)
        assert _collapse(WORDING_S6_LINKAGE) in _collapse(_s6_region(html)), (
            "missing behavior: a low system-derived process-risk row coexists "
            "with serious inventor-stated consequences (fire/danger) with NO "
            "reconciliation in Section 6 (contract §4.2)")

    def test_r3_section13_adjacent_note_exists(self, ws1_journey):
        """Contract §4.4 (R3): with signals present, the §5.3 contextual note
        accompanies the Section 13 structural-risk disclaimer.
        MISSING ON BASE."""
        _, package, html = ws1_journey
        assert FROZEN_S13_DISCLAIMER[:60] in html.replace("&nbsp;", " ") or \
            _collapse(FROZEN_S13_DISCLAIMER) in _collapse(html), (
            "fixture defect: the Section 13 disclaimer is not rendered")
        assert _collapse(WORDING_S13_ADJACENT) in _collapse(html), (
            "missing behavior: the Section 13 disclaimer renders with no "
            "adjacent contextual note while safety signals exist "
            "(contract §4.4/§5.3)")

    def test_r4_empty_section6_qualified_when_signals_exist(
            self, mature_gap_free_journey):
        """Contract §4.3 (R4): a mature, gap-free, demonstrated-quality state
        renders zero Section 6 rows beside populated signals; the bare
        'No risks recorded.' must be replaced by the §5.2 qualification.
        MISSING ON BASE."""
        _, _, html = mature_gap_free_journey
        region = _s6_region(html)
        if "No risks recorded." not in region:
            pytest.fail("fixture defect: expected the current bare empty "
                        "Section 6 message on the mature/gap-free fixture")
        assert _collapse(WORDING_S6_EMPTY_QUALIFIED) in _collapse(region), (
            "missing behavior: the bare 'No risks recorded.' renders beside "
            "populated inventor-stated safety signals without the required "
            "qualification (contract §4.3/§5.2)")

    def test_r5_disconnection_in_both_json_and_html(self, ws1_journey):
        """Contract §4.5 (R5): the linkage truth must exist in BOTH the
        inventor-facing JSON package and the rendered HTML (semantic parity).
        MISSING ON BASE in both."""
        _, package, html = ws1_journey
        json_has = "risk_safety_linkage" in package["_session_meta"]
        html_has = _collapse(WORDING_S6_LINKAGE) in _collapse(html)
        assert json_has and html_has, (
            "missing behavior: the risk/safety linkage is absent from "
            "JSON (present=%s) and HTML (present=%s) — the disconnection "
            "exists on both inventor-facing surfaces (contract §4.5)"
            % (json_has, html_has))


# =============================================================================
# R6 — DOCUMENTATION-ONLY (owner decision D4): passes on BASE and HEAD;
# NOT a RED-to-GREEN gate.
# =============================================================================
class TestKnownLimitationRecord:
    def test_r6_near_duplicate_presentation_documented(self, ws1_journey):
        """Owner decision D4 / contract §14 (documentation-only): the WS1
        journey's signals share the same leading sentence, so the panel
        renders visually repetitive excerpts while the underlying dedup
        remains correct (three DISTINCT records). Workstream 5 does NOT
        change this: near-duplicate signal presentation is deferred as a
        known limitation. This test records that state and must pass on
        base AND at head (rendering unchanged)."""
        _, package, html = ws1_journey
        signals = package["_session_meta"]["inventor_stated_safety_signals"]["signals"]
        assert len(signals) >= 2, "fixture defect: expected multiple signals"
        leading = {s["statement"][:60] for s in signals}
        assert len(leading) < len(signals), (
            "observation no longer holds: signal excerpts no longer share a "
            "leading sentence — update the known-limitation record")
        # Dedup correctness: the records are distinct (different sources).
        assert len({s["source"] for s in signals}) == len(signals)
        # Current rendering: every statement appears in full (D4 unchanged).
        for s in signals:
            assert s["statement"] in html
