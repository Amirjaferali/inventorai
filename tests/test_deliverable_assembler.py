import sys, json, uuid
sys.path.insert(0, ".")
from engine.idea_state import IdeaState, ASSERTED, REASONED, OPEN, CLOSED
from engine.domain_rules import infer_domain
from engine.progression_loop import run_iteration
from engine.deliverable_assembler import assemble_deliverable, PACKAGE_VERSION, SCHEMA_ID

P, F, FAILS = 0, 0, []

def ok(n):
    global P; P += 1; print(f"  PASS  {n}")

def fail(n, d=""):
    global F; F += 1; FAILS.append(f"  FAIL  {n}: {d}"); print(f"  FAIL  {n}: {d}")

def chk(n, c, d=""):
    ok(n) if c else fail(n, d or "False")

def st(idea="IoT temperature sensor for greenhouse"):
    s = IdeaState(idea_id=str(uuid.uuid4()))
    s.domain = infer_domain(idea); s.domain_signal = s.domain; return s


    if __name__ == "__main__":
        print("\n" + "="*60)
        print("  DELIVERABLE ASSEMBLER — Acceptance Tests")
        print("="*60)

        # TC-01 type guards
        print("\n[TC-01] Input validation")
        try: assemble_deliverable("x"); fail("TC-01a", "no TypeError")
        except TypeError: ok("TC-01a TypeError raised")
        s0 = IdeaState.__new__(IdeaState); s0.idea_id = ""
        try: assemble_deliverable(s0); fail("TC-01b", "no error")
        except (ValueError, AttributeError): ok("TC-01b ValueError/AttributeError raised")

        # TC-02 envelope
        print("\n[TC-02] Envelope fields")
        s = st(); run_iteration(s, "maybe"); pkg = assemble_deliverable(s)
        for f in ["package_version","schema_id","session_id","generated_at"]:
            chk(f"TC-02 {f}", f in pkg and pkg[f])
        chk("TC-02 version", pkg["package_version"] == PACKAGE_VERSION)
        chk("TC-02 schema",  pkg["schema_id"] == SCHEMA_ID)
        chk("TC-02 session_id == idea_id", pkg["session_id"] == s.idea_id)
        chk("TC-02 generated_at ISO", "T" in pkg["generated_at"])

        # TC-03 all 8 sections
        print("\n[TC-03] All 8 mandatory sections")
        SECS = ["section_1_disclaimer","section_2_invention_summary",
                "section_3_assessment_overview","section_4_requirements",
                "section_5_assumptions","section_6_risks",
                "section_7_recommendations","section_8_unresolved_items"]
        for sec in SECS: chk(f"TC-03 {sec}", sec in pkg)

        # TC-04 S1
        print("\n[TC-04] S1 disclaimer")
        s1 = pkg["section_1_disclaimer"]
        chk("TC-04 tier=standard", s1.get("tier")=="standard")
        chk("TC-04 text non-empty", bool(s1.get("text")))
        chk("TC-04 applies=True", s1.get("applies") is True)
        chk("TC-04 advisory in text", "advisory" in s1["text"].lower())

        # TC-05 S2 + Level 1 exploratory label
        print("\n[TC-05] S2 invention summary")
        s2 = pkg["section_2_invention_summary"]
        chk("TC-05 maturity_level", "maturity_level" in s2)
        chk("TC-05 maturity_label", bool(s2.get("maturity_label")))
        chk("TC-05 completeness", bool(s2.get("assessment_completeness")))
        sl1 = st(); run_iteration(sl1, "smart irrigation system"); run_iteration(sl1, "soil moisture sensor triggers relay")
        p1 = assemble_deliverable(sl1)
        if sl1.maturity_level >= 1:
            chk("TC-05 Level1 Exploratory label",
                "Exploratory" in p1["section_2_invention_summary"].get("maturity_label",""),
                p1["section_2_invention_summary"].get("maturity_label"))

        # TC-06 S3
        print("\n[TC-06] S3 assessment overview")
        s3 = pkg["section_3_assessment_overview"]
        chk("TC-06 caps list", isinstance(s3.get("capabilities_assessed"), list))
        chk("TC-06 1 row", len(s3["capabilities_assessed"]) >= 1)
        chk("TC-06 conflicts=[]", s3.get("cross_capability_conflicts") == [])
        row = s3["capabilities_assessed"][0]
        for f in ["capability_id","maturity_level","gaps_total"]: chk(f"TC-06 row.{f}", f in row)

        # TC-07 S4
        print("\n[TC-07] S4 requirements")
        s4 = pkg["section_4_requirements"]
        chk("TC-07 list", isinstance(s4.get("requirements"), list))
        chk("TC-07 total int", isinstance(s4.get("total"), int))

        # TC-08 S5
        print("\n[TC-08] S5 assumptions")
        s5 = pkg["section_5_assumptions"]
        chk("TC-08 list", isinstance(s5.get("assumptions"), list))

        # TC-09 S6
        print("\n[TC-09] S6 risks")
        s6 = pkg["section_6_risks"]
        chk("TC-09 list", isinstance(s6.get("risks"), list))
        chk("TC-09 total", s6["total"] == len(s6["risks"]))
        sz = st(); pz = assemble_deliverable(sz)
        hr = [r for r in pz["section_6_risks"]["risks"] if r["severity"]=="high"]
        chk("TC-09 maturity=0 high risk", len(hr) >= 1)

        # TC-10 S7
        print("\n[TC-10] S7 recommendations")
        s7 = pkg["section_7_recommendations"]
        chk("TC-10 cat_a present", "category_a_proceed_revise_block" in s7)
        chk("TC-10 cat_b DEFERRED", s7.get("category_b_material_selection",{}).get("status")=="DEFERRED")
        chk("TC-10 cat_c DEFERRED", s7.get("category_c_manufacturing",{}).get("status")=="DEFERRED")
        chk("TC-10 cat_d list", isinstance(s7.get("category_d_open_items"), list))
        ca = s7["category_a_proceed_revise_block"]
        chk("TC-10 verdict valid", ca.get("verdict") in ("PROCEED","PROCEED WITH CAUTION","REVISE","BLOCK"))
        chk("TC-10 rationale", bool(ca.get("rationale")))
        chk("TC-10 maturity=0 -> BLOCK",
            pz["section_7_recommendations"]["category_a_proceed_revise_block"]["verdict"]=="BLOCK",
            pz["section_7_recommendations"]["category_a_proceed_revise_block"]["verdict"])

        # TC-11 S8
        print("\n[TC-11] S8 unresolved items")
        s8 = pkg["section_8_unresolved_items"]
        chk("TC-11 list", isinstance(s8.get("open_gaps"), list))
        chk("TC-11 count int", isinstance(s8.get("open_gap_count"), int))
        chk("TC-11 conflicts=[]", s8.get("cross_capability_conflicts") == [])
        chk("TC-11 count matches", s8["open_gap_count"] == len(s8["open_gaps"]))

        # TC-12 IdeaState not mutated
        print("\n[TC-12] IdeaState not mutated")
        sm = st(); run_iteration(sm, "smart irrigation sensor")
        before = (sm.iteration, sm.maturity_level, len(sm.gaps), sm.domain_signal)
        assemble_deliverable(sm)
        after  = (sm.iteration, sm.maturity_level, len(sm.gaps), sm.domain_signal)
        chk("TC-12 state unchanged", before == after, f"{before} != {after}")

        # TC-13 Full session
        print("\n[TC-13] Full session — Level 2 path")
        sf = st("IoT greenhouse temperature sensor with automated relay control")
        for inp in [
            "Existing greenhouse monitors require manual calibration every 6 hours",
            "TMP117 digital temperature sensor connected to ESP32 via I2C, triggers relay at threshold",
            "Operating range -10 to 50 Celsius, IP65 enclosure, 3.3V battery powered",
            "Sampling rate 0.1Hz, MQTT to local broker, 72-hour battery life target",
            "Single greenhouse zone, standalone operation, no network required",
        ]:
            run_iteration(sf, inp)
        pf = assemble_deliverable(sf)
        meta = pf["_session_meta"]
        chk("TC-13 maturity>=1", meta["maturity_level"] >= 1)
        chk("TC-13 all 8 sections", all(sec in pf for sec in SECS))
        chk("TC-13 S1 populated", bool(pf["section_1_disclaimer"]["text"]))
        chk("TC-13 S2 known_problem", pf["section_2_invention_summary"].get("known_problem") is not None)
        chk("TC-13 S4 total>=1", pf["section_4_requirements"]["total"] >= 1)
        chk("TC-13 verdict present",
            pf["section_7_recommendations"]["category_a_proceed_revise_block"]["verdict"] in
            ("PROCEED","PROCEED WITH CAUTION","REVISE","BLOCK"))
        chk("TC-13 JSON serialisable", bool(json.dumps(pf)))

        # TC-14 eligibility
        print("\n[TC-14] Deliverable eligibility")
        chk("TC-14 maturity=0 not eligible", pz["_session_meta"]["deliverable_eligible"] is False)

        # TC-15 sample output
        print("\n[TC-15] Sample package (TC-13 session)")
        out = json.dumps(pf, indent=2, default=str)
        print(out[:2000] + ("\n  ...(truncated)" if len(out) > 2000 else ""))

        print("\n" + "="*60)
        print(f"  Results: {P} passed, {F} failed")
        if FAILS:
            for x in FAILS: print(x)
            sys.exit(1)
        print("  ALL TESTS PASSED")
        print("="*60)
