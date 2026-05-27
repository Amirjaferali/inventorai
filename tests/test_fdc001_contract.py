import os, sys, uuid, json
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from engine.idea_state import IdeaState, Evidence, ASSERTED, REASONED, OPEN, CLOSED
from engine.domain_rules import infer_domain
from engine.progression_loop import run_iteration
from engine.deliverable_assembler import assemble_deliverable, PACKAGE_VERSION, SCHEMA_ID

def mks(idea="IoT temperature sensor device"):
    s = IdeaState(idea_id=str(uuid.uuid4()))
    s.domain = infer_domain(idea); s.domain_signal = s.domain; return s

def make_complete():
    s = mks()
    for inp in [
        "Greenhouse crop loss when soil moisture drops overnight without monitoring",
        "TMP117 on ESP32 I2C triggers relay below moisture threshold",
        "Operating 5-45C IP67 3.3V battery powered single zone 50sqm",
    ]: run_iteration(s, inp)
    return s

MANDATORY = ["section_1_disclaimer","section_2_invention_summary","section_3_assessment_overview",
             "section_4_requirements","section_5_assumptions","section_6_risks",
             "section_7_recommendations","section_8_unresolved_items"]

class TestFDC001_Envelope:
    """FDC-001 §5: Machine-readable envelope must be present and correctly versioned."""
    def test_package_version(self):
        """FDC-001 §5: package_version must match PACKAGE_VERSION constant."""
        pkg = assemble_deliverable(mks())
        assert pkg.get("package_version") == PACKAGE_VERSION,             f"FDC-001 §5: package_version={pkg.get('package_version')!r} != {PACKAGE_VERSION!r}"
    def test_schema_id(self):
        """FDC-001 §5: schema_id must match SCHEMA_ID constant."""
        pkg = assemble_deliverable(mks())
        assert pkg.get("schema_id") == SCHEMA_ID,             f"FDC-001 §5: schema_id={pkg.get('schema_id')!r} != {SCHEMA_ID!r}"
    def test_session_id_matches_idea_id(self):
        """FDC-001 §5: session_id must equal state.idea_id."""
        s = mks(); pkg = assemble_deliverable(s)
        assert pkg["session_id"] == s.idea_id,             f"FDC-001 §5: session_id {pkg['session_id']!r} != idea_id {s.idea_id!r}"
    def test_generated_at_iso_format(self):
        """FDC-001 §5: generated_at must be ISO 8601 UTC."""
        ts = assemble_deliverable(mks())["generated_at"]
        assert "T" in ts and "Z" in ts, f"FDC-001 §5: generated_at={ts!r} not ISO UTC"

class TestFDC001_MandatorySections:
    """FDC-001 §2: All 8 mandatory sections must be present in every package."""
    @pytest.mark.parametrize("section", MANDATORY)
    def test_section_present_minimal(self, section):
        """FDC-001 §2: Section must be present for level-0 state."""
        assert section in assemble_deliverable(mks()),             f"FDC-001 §2 VIOLATED: {section!r} missing from minimal package"
    @pytest.mark.parametrize("section", MANDATORY)
    def test_section_present_complete(self, section):
        """FDC-001 §2: Section must be present for complete session."""
        assert section in assemble_deliverable(make_complete()),             f"FDC-001 §2 VIOLATED: {section!r} missing from complete package"
    def test_json_serialisable(self):
        """FDC-001 §5: Package must be fully JSON-serialisable."""
        try: json.dumps(assemble_deliverable(make_complete()), default=str)
        except (TypeError, ValueError) as e:
            pytest.fail(f"FDC-001 §5 VIOLATED: not JSON-serialisable: {e}")

class TestFDC001_S1_Disclaimer:
    """FDC-001 §2 S1: Disclaimer must be populated with advisory text."""
    def test_tier_standard(self):
        """FDC-001 §2 S1: tier must be standard."""
        s1 = assemble_deliverable(mks())["section_1_disclaimer"]
        assert s1.get("tier") == "standard", f"FDC-001 §2 S1: tier={s1.get('tier')!r}"
    def test_text_non_empty(self):
        """FDC-001 §2 S1: text must be non-empty."""
        text = assemble_deliverable(mks())["section_1_disclaimer"].get("text","")
        assert len(text) > 50, f"FDC-001 §2 S1: disclaimer too short: {text!r}"
    def test_advisory_language(self):
        """FDC-001 §2 S1/§7: Disclaimer must contain advisory language."""
        text = assemble_deliverable(mks())["section_1_disclaimer"].get("text","").lower()
        assert "advisory" in text, "FDC-001 §2 S1 VIOLATED: no advisory language in disclaimer"
    def test_applies_true(self):
        """FDC-001 §2 S1: applies must be True."""
        assert assemble_deliverable(mks())["section_1_disclaimer"].get("applies") is True,             "FDC-001 §2 S1 VIOLATED: applies is not True"

class TestFDC001_S7_CategoryA:
    """FDC-001 §2 S7: Category A verdict must be correct."""
    VALID = {"PROCEED","PROCEED WITH CAUTION","REVISE","BLOCK"}
    def test_maturity_0_produces_block(self):
        """FDC-001 §2 S7: maturity=0 must produce BLOCK."""
        v = assemble_deliverable(mks())["section_7_recommendations"]["category_a_proceed_revise_block"]["verdict"]
        assert v == "BLOCK", f"FDC-001 §2 S7 VIOLATED: maturity=0 produced {v!r}, must be BLOCK"
    def test_verdict_in_valid_set(self):
        """FDC-001 §2 S7: verdict must be one of 4 valid values."""
        for sfn in [mks, make_complete]:
            v = assemble_deliverable(sfn())["section_7_recommendations"]["category_a_proceed_revise_block"]["verdict"]
            assert v in self.VALID, f"FDC-001 §2 S7 VIOLATED: verdict={v!r} not in {self.VALID}"
    def test_category_a_has_rationale(self):
        """FDC-001 §2 S7: Category A must have a rationale."""
        r = assemble_deliverable(mks())["section_7_recommendations"]["category_a_proceed_revise_block"].get("rationale","")
        assert r, "FDC-001 §2 S7 VIOLATED: no rationale"

class TestFDC001_S7_CategoriesBC_Deferred:
    """FDC-001 §2 S7: Categories B/C must be DEFERRED until ODS-001 exists."""
    def _ods(self):
        root = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")
        return (os.path.exists(os.path.join(root,"docs","OPTIONS_DATABASE_SPECIFICATION.md")) or
                os.path.exists(os.path.join(root,"engine","options_database.py")))
    def test_category_b_deferred(self):
        """FDC-001 §2 S7: Category B must be DEFERRED when ODS-001 absent."""
        if self._ods(): pytest.skip("ODS-001 exists")
        s = assemble_deliverable(mks())["section_7_recommendations"].get("category_b_material_selection",{}).get("status")
        assert s == "DEFERRED", f"FDC-001 §2 S7 VIOLATED: category_b status={s!r}"
    def test_category_c_deferred(self):
        """FDC-001 §2 S7: Category C must be DEFERRED when ODS-001 absent."""
        if self._ods(): pytest.skip("ODS-001 exists")
        s = assemble_deliverable(mks())["section_7_recommendations"].get("category_c_manufacturing",{}).get("status")
        assert s == "DEFERRED", f"FDC-001 §2 S7 VIOLATED: category_c status={s!r}"
    def test_category_b_note_references_ods001(self):
        """FDC-001 §2 S7: Category B note must reference ODS-001."""
        if self._ods(): pytest.skip("ODS-001 exists")
        note = assemble_deliverable(mks())["section_7_recommendations"].get("category_b_material_selection",{}).get("note","")
        assert "ODS-001" in note, f"FDC-001 §2 S7 VIOLATED: no ODS-001 in cat_b note: {note!r}"

class TestFDC001_DeliverableEligibility:
    """FDC-001: deliverable_eligible must be False unless maturity>=2 AND no open gaps."""
    def test_maturity_0_not_eligible(self):
        """FDC-001: maturity=0 must not be eligible."""
        assert assemble_deliverable(mks())["_session_meta"]["deliverable_eligible"] is False,             "FDC-001 VIOLATED: maturity=0 produced deliverable_eligible=True"
    def test_maturity_2_no_gaps_eligible(self):
        """FDC-001 positive: maturity=2 + no open gaps must be eligible."""
        s = IdeaState(idea_id=str(uuid.uuid4()))
        s.domain = infer_domain("IoT sensor"); s.domain_signal = s.domain
        s.maturity_level = 2
        s.known_problem = Evidence("Clear problem", REASONED, 0)
        s.known_mechanism = Evidence("ESP32 TMP117 mechanism", REASONED, 0)
        pkg = assemble_deliverable(s)
        assert pkg["_session_meta"]["deliverable_eligible"] is True,             f"FDC-001 VIOLATED: maturity=2 no gaps not eligible. meta={pkg['_session_meta']}"
    def test_weak_session_not_eligible(self):
        """FDC-001: Weak-only session must never be eligible."""
        s = mks()
        for inp in ["maybe","not sure","i don't know","maybe","unknown"]: run_iteration(s, inp)
        assert assemble_deliverable(s)["_session_meta"]["deliverable_eligible"] is False,             "FDC-001 VIOLATED: weak session produced eligible=True"

class TestFDC001_S8_UnresolvedItems:
    """FDC-001 §2 S8: Unresolved items must reflect actual open gaps."""
    def test_count_matches_list(self):
        """FDC-001 §2 S8: open_gap_count must equal len(open_gaps)."""
        pkg = assemble_deliverable(make_complete())
        s8 = pkg["section_8_unresolved_items"]
        assert s8["open_gap_count"] == len(s8["open_gaps"]),             f"FDC-001 §2 S8 VIOLATED: count={s8['open_gap_count']} != len={len(s8['open_gaps'])}"
    def test_cross_capability_conflicts_empty(self):
        """FDC-001 §2 S8b: cross_capability_conflicts must be [] for single-capability."""
        s8 = assemble_deliverable(mks())["section_8_unresolved_items"]
        assert s8.get("cross_capability_conflicts") == [],             f"FDC-001 §2 S8b VIOLATED: conflicts={s8.get('cross_capability_conflicts')!r}"
    def test_open_gaps_match_state(self):
        """FDC-001 §2 S8a: open_gaps must match OPEN gaps in IdeaState."""
        s = make_complete()
        actual = {g.gap_type for g in s.gaps if g.status == OPEN}
        pkg_open = {i["gap_type"] for i in assemble_deliverable(s)["section_8_unresolved_items"]["open_gaps"]}
        assert pkg_open == actual, f"FDC-001 §2 S8a VIOLATED: pkg={pkg_open} != state={actual}"
