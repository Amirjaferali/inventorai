#!/usr/bin/env python3
"""Workstream 7 evidence artifact generator.

File: docs/governance/evidence/workstream7_actionable_validation_plan/generate_ws7_artifacts.py
Purpose: deterministically generate the BASE/HEAD user-output evidence for the
ten canonical Workstream 7 cases, exercising ONLY the real production path
(the committed Flask routes, engine.validation_plan.derive_validation_plan,
engine.deliverable_assembler.assemble_deliverable, and the committed
deliverable template) of WHATEVER CHECKOUT it is run from.
Input contract: run from the repository root of the checkout under
measurement: `python <this file> MODE OUTDIR` where MODE is `base` or `head`
(a labelling prefix only — behavior always comes from the current checkout)
and OUTDIR is the destination directory. Requires the checkout's own engine/
web modules on sys.path (cwd).
Output contract: writes `<MODE upper>_WS1_JSON.json`, `<MODE>_WS1_HTML.html`,
`<MODE>_MINIMAL_ANSWERED_JSON.json`, `<MODE>_MINIMAL_ANSWERED_HTML.html`,
`<MODE>_PENDING_EVIDENCE_JSON.json`, `<MODE>_PENDING_EVIDENCE_HTML.html`,
`<MODE>_PENDING_SPECIALIST_JSON.json`, `<MODE>_PENDING_SPECIALIST_HTML.html`,
and `<MODE>_NON_PENDING_CASES.json` (cases 5-10: unknown, deferred,
provisional_assumption, contradiction, criticality-linked, risk/safety-linked).
Determinism: volatile identifiers (session id, generated-at timestamp,
package_version echo in the meta strip) are normalized to fixed placeholders
in saved HTML, and JSON artifacts contain only the deterministic sections;
fixture inputs are recorded verbatim inside each JSON artifact. FATALS loudly
(non-zero exit) on any structural surprise rather than writing partial truth.
Prohibited behaviors: MUST NOT modify repository state, mock any production
seam, or synthesize outputs not produced by the real path.
"""
import json
import os
import re
import sys
import uuid


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ("base", "head"):
        raise SystemExit("usage: generate_ws7_artifacts.py base|head OUTDIR")
    mode, outdir = sys.argv[1].upper(), sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    sys.path.insert(0, os.getcwd())

    from engine.deliverable_assembler import assemble_deliverable
    from engine.idea_state import (IdeaState, CRITICALITY_ACTION_CONFIRMED,
                                   CRITICALITY_FEASIBILITY_THREATENING)
    from engine.validation_plan import derive_validation_plan
    from web.app import app, SESSION_STORE, DOMAIN_CONFIRM_VALUE

    def render(state):
        sid = "ws7-ev-" + uuid.uuid4().hex[:8]
        SESSION_STORE[sid] = {"state": state, "last_result": None,
                              "transcript": []}
        try:
            resp = app.test_client().get(f"/session/{sid}/deliverable")
            assert resp.status_code == 200, resp.status_code
            return normalize_html(resp.get_data(as_text=True), sid)
        finally:
            SESSION_STORE.pop(sid, None)

    def normalize_html(html, sid):
        html = html.replace(sid, "SESSION_ID_NORMALIZED")
        html = re.sub(r"Generated: [^<\n]*", "Generated: GENERATED_AT_NORMALIZED",
                      html)
        html = re.sub(r"Session: [^<\n]*", "Session: SESSION_ID_NORMALIZED",
                      html)
        return html

    def engine_view(state):
        plan = derive_validation_plan(state)
        return {
            "outcome": plan.outcome,
            "steps": [{
                "step_id": st.step_id,
                "statement": st.statement,
                "responsibility_token": st.responsibility,
                "evidence_category": st.evidence_category,
                "closure_condition": st.closure_condition,
                "provenance_kind": st.provenance.anchor_kind,
                "provenance_reference": st.provenance.reference,
                "provenance_label": st.provenance.display_label,
                "confidence_token": st.confidence,
            } for st in plan.steps],
            "blocked_items": [{
                "item_id": b.item_id,
                "reason": b.reason,
                "missing": b.missing,
                "responsibility_token": b.responsibility,
                "provenance_kind": b.provenance.anchor_kind,
                "provenance_label": b.provenance.display_label,
            } for b in plan.blocked_items],
        }

    def package_view(state):
        pkg = assemble_deliverable(state)
        s13 = pkg["section_13_requirement_landscape"]
        s14 = pkg["section_14_validation_plan"]
        meta = pkg["_session_meta"]
        return {
            "section_13": {
                "requirements": s13["requirements"],
                "total": s13["total"],
                "count_basis": s13["count_basis"],
            },
            "section_14": s14,
            "risk_safety_linkage": meta.get("risk_safety_linkage"),
            "safety_signal_total":
                meta["inventor_stated_safety_signals"]["total"],
        }

    def case(state, inputs_desc):
        return {"fixture_inputs": inputs_desc,
                "engine": engine_view(state),
                "package": package_view(state)}

    def dump(name, obj):
        path = os.path.join(outdir, f"{mode}_{name}")
        with open(path, "w") as f:
            json.dump(obj, f, indent=2, ensure_ascii=False, sort_keys=True)
            f.write("\n")
        print("wrote", path)

    def dump_html(name, html):
        path = os.path.join(outdir, f"{mode}_{name}")
        with open(path, "w") as f:
            f.write(html)
        print("wrote", path)

    # --- Case 1: canonical Workstream 1 journey (real Flask flow) -----------
    IDEA = ("A smart plug-in safety device that senses appliance current and "
            "voltage with a microcontroller and disconnects a relay to warn "
            "about dangerous appliances")
    BASE_ANSWER = (
        "The current sensor detects an abnormal rise because the shunt "
        "resistor voltage increases, therefore the microcontroller opens the "
        "relay to disconnect the appliance.")
    DANGER = {
        3: " If the sensing is wrong, the dangerous appliance could remain "
           "powered.",
        4: (" If it trips the wrong branch, the wrong appliance could be "
            "disconnected and it would fail to isolate the actual source of "
            "danger."),
        6: (" If the relay sticks, damage or overheating could continue and "
            "the fire risk could continue until someone notices."),
        7: (" The current sensing accuracy is essential; the buzzer volume "
            "and alert timing are adjustable."),
    }
    client = app.test_client()
    r = client.post("/start", data={"idea": IDEA,
                                    "domain_confirm": DOMAIN_CONFIRM_VALUE})
    assert r.status_code == 302, r.status_code
    sid = r.headers["Location"].rsplit("/", 1)[-1]
    posted = [IDEA]
    for i in range(2, 32):
        page = client.get(f"/session/{sid}").get_data(as_text=True)
        if '<p class="complete">' in page:
            break
        if i == 5:
            action, text = "unknown", "I don't know yet."
        else:
            action, text = "answered", BASE_ANSWER + DANGER.get(i, "")
        posted.append(f"{action}: {text}")
        client.post(f"/session/{sid}",
                    data={"response": text, "action": action})
    ws1_state = SESSION_STORE[sid]["state"]
    ws1_html = normalize_html(
        client.get(f"/session/{sid}/deliverable").get_data(as_text=True), sid)
    ws1_case = case(ws1_state, posted)
    SESSION_STORE.pop(sid, None)
    answered = [s for s in ws1_case["engine"]["steps"]
                if s["provenance_label"] == "Recorded answer"]
    assert len(answered) == 12, f"expected 12 answered steps, got {len(answered)}"
    dump("WS1_JSON.json", ws1_case)
    dump_html("WS1_HTML.html", ws1_html)

    # --- Case 2: minimal answered -------------------------------------------
    S = ("The relay contacts are rated above the maximum expected appliance "
         "current.")
    st = IdeaState(idea_id="ws7-ev-answered")
    st.record_interaction("answered", iteration=0, content=S)
    dump("MINIMAL_ANSWERED_JSON.json", case(st, [f"answered: {S}"]))
    dump_html("MINIMAL_ANSWERED_HTML.html", render(st))

    # --- Case 3: pending_evidence --------------------------------------------
    E = "Measure the actual trip time of the relay under a representative overload condition."
    st = IdeaState(idea_id="ws7-ev-evidence")
    st.record_interaction("evidence_requested", iteration=0, content=E)
    dump("PENDING_EVIDENCE_JSON.json", case(st, [f"evidence_requested: {E}"]))
    dump_html("PENDING_EVIDENCE_HTML.html", render(st))

    # --- Case 4: pending_specialist -------------------------------------------
    P = "Review whether the sensing approach is adequate for the intended protective function."
    st = IdeaState(idea_id="ws7-ev-specialist")
    st.record_interaction("specialist_requested", iteration=0, content=P)
    dump("PENDING_SPECIALIST_JSON.json",
         case(st, [f"specialist_requested: {P}"]))
    dump_html("PENDING_SPECIALIST_HTML.html", render(st))

    # --- Cases 5-10: non-pending cases (JSON + Section 14 HTML excerpt) -------
    def sec14(html):
        i = html.find("<h3>Validation Plan</h3>")
        j = html.find("back-link", i)
        assert i >= 0 and j > i
        return html[i:j]

    non_pending = {}

    for disp, content in (("unknown", "Unknown item content."),
                          ("deferred", "Deferred item content."),
                          ("provisional_assumption",
                           "Provisional item content.")):
        st = IdeaState(idea_id="ws7-ev-" + disp)
        st.record_interaction(disp, iteration=0, content=content)
        c = case(st, [f"{disp}: {content}"])
        c["section_14_html_excerpt"] = sec14(render(st))
        non_pending[disp] = c

    st = IdeaState(idea_id="ws7-ev-contradiction")
    ra = st.record_interaction("answered", iteration=0,
                               content="The housing is sealed.")
    rb = st.record_interaction("answered", iteration=0,
                               content="The housing is vented.")
    st.mark_contradiction(ra.record_id, rb.record_id)
    c = case(st, ["answered: The housing is sealed.",
                  "answered: The housing is vented.",
                  f"mark_contradiction({ra.record_id}, {rb.record_id})"])
    c["section_14_html_excerpt"] = sec14(render(st))
    non_pending["contradiction"] = c

    st = IdeaState(idea_id="ws7-ev-criticality")
    st.record_interaction("answered", iteration=0,
                          content="The fuse rating is decisive.")
    st.record_criticality_confirmation(
        "req:assertion:rec_1", CRITICALITY_ACTION_CONFIRMED,
        category=CRITICALITY_FEASIBILITY_THREATENING,
        rationale_verbatim="Without the right fuse the device fails.",
        rationale_source="inventor_typed")
    c = case(st, ["answered: The fuse rating is decisive.",
                  "criticality confirmed FEASIBILITY-THREATENING, rationale "
                  "'Without the right fuse the device fails.' "
                  "(inventor_typed)"])
    c["section_14_html_excerpt"] = sec14(render(st))
    non_pending["criticality_linked"] = c

    non_pending["risk_safety_linked"] = {
        "fixture_inputs": "the canonical Workstream 1 journey above "
                          "(danger statements produce safety signals)",
        "risk_safety_linkage": ws1_case["package"]["risk_safety_linkage"],
        "safety_signal_total": ws1_case["package"]["safety_signal_total"],
        "section_13_total": ws1_case["package"]["section_13"]["total"],
    }
    dump("NON_PENDING_CASES.json", non_pending)
    print("GENERATION COMPLETE:", mode)


if __name__ == "__main__":
    main()
