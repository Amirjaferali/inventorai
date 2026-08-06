"""Inventor-Stated Safety Signals — implementation tests.

Governed by
`docs/governance/SAFETY_AWARE_INVENTOR_STATED_SAFETY_SIGNALS_INCREMENT_CONTRACT.md`
(true-merged via PR #120). Proves the additive, read-only, advisory-only
derivation: it elevates conservative inventor-stated safety signals, labels them
inventor-stated / requires-independent-validation, never claims safe/unsafe, and
leaves scoring, maturity, readiness, `derive_requirement_landscape`, Section 6
risks, Section 13 criticality, and `RequirementLandscape.risks` unchanged.
"""
import copy
import json
import os
import sys
import uuid

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from engine.idea_state import IdeaState, Evidence, ASSERTED  # noqa: E402
from engine.safety_signal import (  # noqa: E402
    derive_inventor_stated_safety_signals,
    PROVENANCE_INVENTOR_STATED,
    VALIDATION_REQUIRES_INDEPENDENT,
)
from engine.requirement_landscape import derive_requirement_landscape, UNDETERMINED  # noqa: E402
from engine.deliverable_assembler import assemble_deliverable  # noqa: E402

_INSULATION = ("If insulation cannot be safely achieved inside the plug housing, "
               "the device should not be used because it could create a safety risk.")
_WARNING = ("Wrong results could make the device miss a real risk or warn the "
            "user too late.")

# Forbidden final-determination / approval claims (contract §7).
_FORBIDDEN_CLAIMS = (
    "the invention is unsafe", "the invention is safe", "certified", "compliant",
    "approved", "patent-ready", "engineering-validated", "engineering validated",
)


def _state(text=None, domain="electronics_electrical"):
    s = IdeaState(idea_id=str(uuid.uuid4()))
    s.domain = domain
    s.domain_signal = domain
    if text is not None:
        s.idea_summary = text
    return s


def _blob(section):
    parts = [section.get("empty_statement", ""), section.get("advisory_note", ""),
             section.get("title", "")]
    for sig in section.get("signals", []):
        parts.extend(str(v) for v in sig.values())
    return " ".join(parts).lower()


# ---------------------------------------------------------------------------
# 1. Positive inventor-stated electrical safety condition triggers a signal
# ---------------------------------------------------------------------------

def test_positive_electrical_safety_condition_triggers():
    signals = derive_inventor_stated_safety_signals(_state(_INSULATION))
    assert len(signals) == 1
    sig = signals[0]
    assert sig.provenance == PROVENANCE_INVENTOR_STATED
    assert sig.validation_status == VALIDATION_REQUIRES_INDEPENDENT
    assert sig.safety_subject  # a matched subject (e.g. insulation)
    assert sig.failure_condition and sig.possible_consequence


def test_positive_warning_reliability_condition_triggers():
    signals = derive_inventor_stated_safety_signals(_state(_WARNING))
    assert len(signals) == 1
    assert signals[0].provenance == PROVENANCE_INVENTOR_STATED


# ---------------------------------------------------------------------------
# 2-5. Negatives / negation guard / non-electrical / bare keyword
# ---------------------------------------------------------------------------

def test_negative_non_safety_statement_does_not_trigger():
    assert derive_inventor_stated_safety_signals(_state("Safety is important.")) == ()
    assert derive_inventor_stated_safety_signals(_state("This improves safety.")) == ()


def test_negation_guard_no_safety_concerns_does_not_trigger():
    assert derive_inventor_stated_safety_signals(_state("There are no safety concerns.")) == ()


def test_generic_non_electrical_business_risk_does_not_over_trigger():
    # Domain is electronics; the text carries no safety subject/failure/consequence,
    # so electronics domain context alone must NOT trigger a signal.
    txt = "There is a financial risk that competitors will outprice this product."
    assert derive_inventor_stated_safety_signals(_state(txt)) == ()


def test_bare_keyword_safety_alone_does_not_trigger():
    assert derive_inventor_stated_safety_signals(_state("safety")) == ()
    assert derive_inventor_stated_safety_signals(_state("risk")) == ()


# ---------------------------------------------------------------------------
# 6-7. Deliverable output includes the signal with provenance + validation wording
# ---------------------------------------------------------------------------

def _safety_section(pkg):
    # Nested under _session_meta (mirrors evidence_registry / unknown_registry) so
    # the top-level canonical-section contract (Increment-6 traceability) is unchanged.
    return pkg["_session_meta"]["inventor_stated_safety_signals"]


def test_deliverable_section_includes_signal_with_provenance():
    pkg = assemble_deliverable(_state(_INSULATION))
    section = _safety_section(pkg)
    assert section["has_signals"] is True and section["total"] == 1
    sig = section["signals"][0]
    assert sig["provenance"] == "inventor_stated"
    assert sig["validation_status"] == "requires_independent_validation"


def test_deliverable_section_states_requires_independent_validation():
    pkg = assemble_deliverable(_state(_INSULATION))
    blob = _blob(_safety_section(pkg))
    assert "requires independent validation" in blob or "require independent validation" in blob


def test_deliverable_makes_no_final_safety_or_approval_claim():
    for text in (_INSULATION, None):
        pkg = assemble_deliverable(_state(text))
        blob = _blob(_safety_section(pkg))
        for claim in _FORBIDDEN_CLAIMS:
            assert claim not in blob, (text, claim)


def test_empty_state_uses_neutral_non_safety_claim_wording():
    pkg = assemble_deliverable(_state("An ordinary sensor that reports readings."))
    section = _safety_section(pkg)
    assert section["has_signals"] is False and section["total"] == 0
    assert "not a determination" in section["empty_statement"].lower()


# ---------------------------------------------------------------------------
# 8-10. Existing Section 6 risks / Section 13 criticality / landscape.risks unchanged
# ---------------------------------------------------------------------------

def test_section_6_risks_do_not_contain_safety_signal_fields():
    pkg = assemble_deliverable(_state(_INSULATION))
    s6 = pkg["section_6_risks"]
    assert "risks" in s6  # Section 6 shape intact
    for r in s6["risks"]:
        assert "signal_id" not in r and r.get("provenance") != "inventor_stated"


def test_section_13_criticality_all_undetermined_and_landscape_risks_empty():
    state = _state(_INSULATION)
    landscape = derive_requirement_landscape(state)
    assert landscape.risks == ()  # RequirementLandscape.risks unchanged (empty)
    for req in landscape.requirements:
        assert req.criticality == UNDETERMINED
        assert req.criticality_authority == "system-derived"
    s13 = assemble_deliverable(state)["section_13_requirement_landscape"]
    assert s13["risks"] == []
    for req in s13["requirements"]:
        assert req["criticality"] == UNDETERMINED


# ---------------------------------------------------------------------------
# 11-13. No scoring/maturity/readiness change; no state mutation; JSON-safe
# ---------------------------------------------------------------------------

def test_derivation_is_read_only_and_does_not_mutate_state():
    state = _state(_INSULATION)
    state.known_mechanism = Evidence(content="the plug senses current", quality=ASSERTED, iteration=1)
    before = copy.deepcopy(state.__dict__)
    before_maturity = state.maturity_level
    before_gaps = len(state.gaps)
    derive_inventor_stated_safety_signals(state)
    assert state.__dict__ == before  # no mutation of any field
    assert state.maturity_level == before_maturity
    assert len(state.gaps) == before_gaps


def test_signal_derivation_is_deterministic():
    state = _state(_INSULATION)
    a = derive_inventor_stated_safety_signals(state)
    b = derive_inventor_stated_safety_signals(state)
    assert a == b


def test_deliverable_remains_json_serialisable_with_section_15():
    pkg = assemble_deliverable(_state(_INSULATION))
    json.dumps(pkg, default=str)  # must not raise
    assert "inventor_stated_safety_signals" in pkg["_session_meta"]


# ---------------------------------------------------------------------------
# 14-16. Rendered user-facing visibility (PR #122 independent-review correction)
# ---------------------------------------------------------------------------

def _render_deliverable_html(state):
    """Render the real user-facing deliverable HTML through the committed web route
    (Increment 4/5 precedent). Lazy web import isolates the dependency to the
    render tests only."""
    from web.app import app as _flask_app, SESSION_STORE as _STORE
    sid = "safety-render-" + str(id(state))
    _STORE[sid] = {"state": state}
    try:
        resp = _flask_app.test_client().get(f"/session/{sid}/deliverable")
        return resp.get_data(as_text=True)
    finally:
        _STORE.pop(sid, None)


def _panel_region(html):
    """The rendered safety-signals panel region: from the visible panel label to
    the first Increment-6 group heading that follows it. Fails by absence if the
    panel is not rendered."""
    start = html.find("Inventor-Stated Safety Signals")
    assert start != -1, "safety-signals panel label not rendered in deliverable HTML"
    end = html.find("What your idea is", start)
    return html[start:end] if end != -1 else html[start:]


def test_rendered_deliverable_shows_safety_signal_panel():
    html = _render_deliverable_html(_state(_INSULATION))
    region = _panel_region(html)
    low = region.lower()
    # Visible label, inventor-stated provenance, and independent-validation wording.
    assert "potential safety-critical assumption (inventor-stated)" in low
    assert "inventor stated" in low or "inventor-stated" in low
    assert "requires independent validation" in low or "require independent validation" in low
    # The inventor's own bounded statement excerpt is visible.
    assert "insulation cannot be safely achieved" in low


def test_rendered_empty_state_neutral_wording_only():
    html = _render_deliverable_html(_state("An ordinary sensor that reports readings."))
    region = _panel_region(html)
    low = region.lower()
    assert "not a determination" in low
    # The empty state must not present a positive safe/verified/risk-free claim:
    # the only wording shown is the neutral no-signals-derived statement.
    assert "no inventor-stated safety signals were derived" in low


def test_rendered_panel_makes_no_forbidden_final_claims():
    for text in (_INSULATION, None):
        region = _panel_region(_render_deliverable_html(_state(text)))
        low = region.lower()
        for claim in _FORBIDDEN_CLAIMS:
            assert claim not in low, (text, claim)
