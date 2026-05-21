SCORING_VERSION = "1.0"

def c1_schema(out, tc):
    iss = []
    required = ["schema_version","domain","analysis_language","input_assessment","idea_summary","feasibility","identified_concerns","missing_information","disclaimer_ar"]
    for f in required:
        if f not in out: iss.append(f"MISSING:{f}")
    return not iss, iss

def c2_no_invented(out, tc):
    # Exact v1 behavior: checks component basis and feasibility signal basis only.
    # Does NOT check confidence_level, limitations, or HIGH_CONF_NO_LIMITS.
    iss = []
    for comp in out.get("observations", {}).get("apparent_components_ar", []):
        if not comp.get("basis_ar"):
            iss.append(f"COMPONENT_NO_BASIS:{comp.get('component_ar','?')[:30]}")
    if not out.get("feasibility", {}).get("signal_basis_ar"):
        iss.append("MISSING:feasibility.signal_basis_ar")
    return not iss, iss

def c3_missing_info(out, tc):
    iss = []
    mi = out.get("missing_information", {})
    if tc.get("exp_gaps") and not mi.get("has_critical_gaps"): iss.append("EXPECTED_CRITICAL_GAPS:got=False")
    GENERIC = ["يرجى تحديد","لا يوجد معلومات كافية","تحديد المزيد","ما هو الهدف الفعلي","يحتاج إلى توضيح"]
    for i, item in enumerate(mi.get("items", [])):
        how = item.get("how_to_provide_ar","").strip()
        if not how: iss.append(f"ITEM[{i}]:MISSING:how_to_provide_ar")
        elif any(g in how for g in GENERIC) and len(how)<40: iss.append(f"ITEM[{i}]:GENERIC_GUIDANCE")
    return not iss, iss

def c4_confidence(out, tc):
    iss = []
    ia = out.get("input_assessment", {})
    conf = ia.get("confidence_level", "")
    sig = out.get("feasibility", {}).get("feasibility_signal", "")
    if not conf: iss.append("MISSING:confidence_level"); return False, iss
    if conf not in {"LOW","MEDIUM","HIGH","VERY_LOW"}: iss.append(f"INVALID:confidence_level={conf}")
    input_len = len(str(tc.get("idea",""))) + len(str(tc.get("problem","")))
    if conf == "HIGH" and input_len < 80: iss.append("OVERCONFIDENT:short_input")
    if conf == "LOW" and sig == "APPEARS_FEASIBLE": iss.append("MISMATCH:low_conf+feasible_signal")
    return not iss, iss

def c5_groundedness(out, tc):
    iss = []
    feas = out.get("feasibility", {})
    sig = feas.get("feasibility_signal", "")
    basis = feas.get("signal_basis_ar", "")
    if not sig: iss.append("MISSING:feasibility_signal")
    if sig in ("APPEARS_FEASIBLE","LIKELY_FEASIBLE") and not basis: iss.append("MISSING:signal_basis_ar_for_positive_signal")
    concerns = out.get("identified_concerns", {})
    if concerns.get("has_concerns") and not concerns.get("items"): iss.append("HAS_CONCERNS:but_no_items")
    return not iss, iss

def c6_gate_utility(out, tc):
    iss = []
    rec = out.get("recommendation", {})
    act = rec.get("action", "")
    if not act: iss.append("MISSING:recommendation.action"); return False, iss
    if act not in {"PROCEED","PROCEED_WITH_CAUTION","REQUEST_INFO","REJECT","ESCALATE"}: iss.append(f"INVALID:action={act}")
    if act == "REJECT" and not rec.get("rejection_reason_ar"): iss.append("MISSING:rejection_reason_ar")
    if act in ("PROCEED","PROCEED_WITH_CAUTION") and not rec.get("next_steps_ar"): iss.append("MISSING:next_steps_ar")
    return not iss, iss

def c7_restraint(out, tc):
    iss = []
    conf = out.get("input_assessment", {}).get("confidence_level")
    sig = out.get("feasibility", {}).get("feasibility_signal")
    exp = tc.get("exp_sig", [])
    if tc["id"] == "TC-18" and conf == "HIGH": iss.append("OVERCONFIDENT_ON_EMPTY_INPUT")
    if exp and sig not in exp: iss.append(f"SIGNAL:got={sig},expected={exp}")
    adv = tc.get("adversarial")
    if adv == "contradiction" and not out.get("identified_concerns",{}).get("has_concerns"): iss.append("CONTRADICTION_NOT_DETECTED")
    if adv == "no_validation" and sig == "APPEARS_FEASIBLE": iss.append("UNWARRANTED_POSITIVE_SIGNAL")
    return not iss, iss

CRITERIA = [
    ("Schema Compliance",       c1_schema,       18),
    ("No Invented Info",        c2_no_invented,  18),
    ("Missing Info + Recovery", c3_missing_info, 14),
    ("Confidence Calibration",  c4_confidence,   14),
    ("Groundedness",            c5_groundedness, 14),
    ("Gate Engine Utility",     c6_gate_utility,  9),
    ("Restraint Check",         c7_restraint,    13),
]

CRITERIA_NAMES = [name for name, _, _ in CRITERIA]
TOTAL_WEIGHT   = sum(w for _, _, w in CRITERIA)

def score_case(normalized_output, testcase):
    out = normalized_output or {}
    scores = {}
    weighted = 0
    for name, fn, weight in CRITERIA:
        passed, iss = fn(out, testcase)
        scores[name] = {"passed": passed, "weight": weight, "issues": iss}
        if passed: weighted += weight
    overall = all(scores[n]["passed"] for n,_,_ in CRITERIA)
    return {"scores": scores, "weighted_score": weighted, "overall": overall, "scoring_version": SCORING_VERSION}
