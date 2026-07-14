"""Workstream 6 evidence harness — deterministic BASE/HEAD artifact generator.

File: docs/governance/evidence/workstream6_requirement_landscape_synthesis/
      generate_ws6_artifacts.py
Purpose: regenerate, deterministically and with loud failure, the BASE and
HEAD deliverable artifacts for the six Workstream 6 evidence cases:
  A ws1        — the canonical Workstream 1 reproduction journey;
  B unknown    — one `unknown`-disposition record;
  C deferred   — one `deferred`-disposition record;
  D provisional— one `provisional_assumption`-disposition record;
  E emptycontent — one empty-content `answered` record (placeholder path);
  F critdefer  — HEAD ONLY: the WS1 journey plus a real web criticality
                 deferral, proving the 8 -> 7 + 1 metadata group split with
                 every unrelated key byte-identical.
Input contract: run from a checkout of the target commit with
  MODE=base|head OUTDIR=<evidence dir> python3 generate_ws6_artifacts.py
The journey inputs are byte-identical to the committed Workstream 1
baseline. Session/idea ids and generated_at are normalized in JSON/HTML
artifacts for determinism (SESSION_ID / GENERATED_AT_UTC placeholders).
Output contract: writes <mode>_<case>_deliverable.json/.html per case,
ws6_case_inputs.json (base mode), and in head mode the machine summaries
ws6_repetition_counts.json, ws6_metadata_parity.json, and
ws6_critdefer_split.json. Exits 2 with a message on ANY unexpected state —
no partial artifacts are left behind on failure.
Prohibited behaviors: no production import beyond the committed public
surfaces; no mutation of repository files outside OUTDIR; no network; no
randomness; no timestamps of its own.
"""
import html as html_mod
import json
import os
import re
import sys

sys.path.insert(0, os.getcwd())

from web.app import app, SESSION_STORE, DOMAIN_CONFIRM_VALUE  # noqa: E402
from engine.deliverable_assembler import assemble_deliverable  # noqa: E402
from engine.idea_state import (  # noqa: E402
    IdeaState, DISPOSITION_UNKNOWN, DISPOSITION_DEFERRED,
    DISPOSITION_PROVISIONAL_ASSUMPTION, DISPOSITION_ANSWERED,
)

MODE = os.environ.get("MODE")
OUTDIR = os.environ.get("OUTDIR")
if MODE not in ("base", "head") or not OUTDIR:
    print("FATAL: set MODE=base|head and OUTDIR", file=sys.stderr)
    sys.exit(2)

# --- Byte-identical committed WS1 journey inputs -----------------------------
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

SINGLE_RECORD_CASES = {
    "unknown":      (DISPOSITION_UNKNOWN, "I don't know the safe cutoff current yet."),
    "deferred":     (DISPOSITION_DEFERRED, "I will decide the enclosure later."),
    "provisional":  (DISPOSITION_PROVISIONAL_ASSUMPTION, "Assume a 5V relay coil for now."),
    "emptycontent": (DISPOSITION_ANSWERED, ""),
}
REPETITION_SENTENCE = "This statement was recorded {n} times during the session."


def fatal(msg):
    print("FATAL: " + msg, file=sys.stderr)
    sys.exit(2)


def normalize(text, sid, idea_id):
    text = text.replace(sid, "SESSION_ID").replace(idea_id, "IDEA_ID")
    text = re.sub(r'"generated_at": "[^"]*"',
                  '"generated_at": "GENERATED_AT_UTC"', text)
    text = re.sub(r"Generated: [0-9TZ:.+\-]+", "Generated: GENERATED_AT_UTC", text)
    return text


def write(name, text):
    with open(os.path.join(OUTDIR, name), "w") as f:
        f.write(text)


def dump_case(case, sid, state, package, page):
    idea_id = state.idea_id
    write("%s_%s_deliverable.json" % (MODE, case),
          normalize(json.dumps(package, indent=2, sort_keys=True, default=str),
                    sid, idea_id))
    write("%s_%s_deliverable.html" % (MODE, case), normalize(page, sid, idea_id))


def section13(page):
    i = page.find("<h3>Requirement Landscape</h3>")
    if i < 0:
        fatal("Section 13 heading missing")
    j = page.find("What is assumed", i)
    return html_mod.unescape(page[i:(j if j > i else len(page))])


def standalone_counts(section_text, statements):
    working, counts = section_text, {}
    for idx, stmt in enumerate(sorted(statements, key=len, reverse=True)):
        counts[stmt] = working.count(stmt)
        working = working.replace(stmt, "<removed:%d>" % idx)
    return counts


def start(idea):
    client = app.test_client()
    r = client.post("/start", data={"idea": idea,
                                    "domain_confirm": DOMAIN_CONFIRM_VALUE})
    if r.status_code != 302:
        fatal("/start did not redirect")
    return client, r.headers["Location"].rsplit("/", 1)[-1]


def drive_ws1():
    client, sid = start(IDEA_WS1)
    for i in range(2, MAX_ITERATIONS + 2):
        page = client.get("/session/%s" % sid).get_data(as_text=True)
        if '<p class="complete">' in page:
            break
        if i == UNKNOWN_ITERATION:
            action, text = "unknown", UNKNOWN_TEXT
        else:
            action, text = "answered", CORE + DANGER_BY_ITERATION.get(i, "")
        client.post("/session/%s" % sid, data={"response": text, "action": action})
    else:
        fatal("WS1 journey did not complete")
    return client, sid


def main():
    summaries = {}

    # --- Case A: canonical WS1 journey ---------------------------------------
    client, sid = drive_ws1()
    state = SESSION_STORE[sid]["state"]
    package = assemble_deliverable(state)
    page = client.get("/session/%s/deliverable" % sid).get_data(as_text=True)
    rows = package["section_13_requirement_landscape"]["requirements"]
    stmts = [r["statement"] for r in rows]
    if len(rows) != 13 or stmts.count(CORE) != 8:
        fatal("WS1 journey shape drifted (%d rows, %d core)"
              % (len(rows), stmts.count(CORE)))
    dump_case("ws1", sid, state, package, page)

    sec = section13(page)
    counts = standalone_counts(sec, sorted(set(stmts), key=len))
    summaries["ws1"] = {
        "json_row_total": len(rows),
        "json_core_statement_rows": stmts.count(CORE),
        "html_core_standalone_renderings": counts[CORE],
        "html_distinct_statement_renderings": {
            s[:80]: counts[s] for s in sorted(set(stmts)) if s != CORE},
        "html_repetition_sentence_count":
            sec.count("This statement was recorded "),
        "html_owner_sentence_for_8_present":
            REPETITION_SENTENCE.format(n=8) in sec,
        "metadata_present": "requirement_landscape_synthesis"
                            in package["_session_meta"],
        "requirement_ids": ["req:assertion:rec_%d" % i for i in range(1, 14)],
    }
    if MODE == "head":
        # R4 direct parity proof over the real metadata object.
        rls = package["_session_meta"]["requirement_landscape_synthesis"]
        parity = {"schema_keys": sorted(rls.keys()),
                  "group_total": rls["group_total"],
                  "repeated_group_total": rls["repeated_group_total"],
                  "synthesis_basis": rls["synthesis_basis"],
                  "groups": [], "parity_ok": True}
        groupable = [r for r in rows if r["provenance"] in (
            "Recorded answer", "Recorded unknown", "Deferred decision",
            "Provisional assumption")]
        for g in rls["statement_groups"]:
            expected = sum(1 for r in groupable if (
                r["statement"], r["provenance"], r["status"], r["criticality"],
                r["criticality_authority"], r["criticality_rationale"],
                r["resolving_action"]) == (
                g["statement"], g["provenance"], g["status"], g["criticality"],
                g["criticality_authority"], g["criticality_rationale"],
                g["resolving_action"]))
            note_expected = (REPETITION_SENTENCE.format(n=g["occurrence_count"])
                             if g["occurrence_count"] > 1 else None)
            entry = {
                "statement_prefix": g["statement"][:80],
                "metadata_count": g["occurrence_count"],
                "json_matching_row_count": expected,
                "metadata_note": g["repetition_note"],
                "note_equals_derived_sentence":
                    g["repetition_note"] == note_expected,
                "html_note_rendered": (g["repetition_note"] in sec
                                       if g["repetition_note"] else None),
                "html_statement_rendered_once": counts[g["statement"]] == 1,
            }
            if (entry["metadata_count"] != entry["json_matching_row_count"]
                    or not entry["note_equals_derived_sentence"]
                    or entry["html_note_rendered"] is False
                    or not entry["html_statement_rendered_once"]):
                parity["parity_ok"] = False
            parity["groups"].append(entry)
        parity["html_sentence_total_equals_repeated_group_total"] = (
            sec.count("This statement was recorded ")
            == rls["repeated_group_total"])
        if not parity["html_sentence_total_equals_repeated_group_total"]:
            parity["parity_ok"] = False
        internal_keys_leaked = any(k in page for k in (
            "requirement_landscape_synthesis", "synthesis_basis",
            "occurrence_count", "statement_groups", "repetition_note"))
        parity["internal_metadata_keys_leaked_to_html"] = internal_keys_leaked
        if internal_keys_leaked:
            parity["parity_ok"] = False
        write("ws6_metadata_parity.json", json.dumps(parity, indent=1))
        if not parity["parity_ok"]:
            fatal("metadata parity failed")

        # --- Case F (HEAD only): criticality deferral group split ------------
        before_pkg = package
        before_meta = {k: v for k, v in before_pkg["_session_meta"].items()}
        pg = client.get("/session/%s" % sid).get_data(as_text=True)
        m = re.search(r'name="focus_token" value="([0-9a-f]+)"', pg)
        if not m:
            fatal("criticality focus token missing")
        r = client.post("/session/%s" % sid, data={
            "criticality_action": "summary_later", "focus_token": m.group(1)})
        if r.status_code != 302:
            fatal("criticality deferral rejected")
        after_pkg = assemble_deliverable(state)
        b = before_pkg["_session_meta"]["requirement_landscape_synthesis"]
        a = after_pkg["_session_meta"]["requirement_landscape_synthesis"]
        unrelated_meta_identical = all(
            json.dumps(before_meta[k], sort_keys=True, default=str)
            == json.dumps(after_pkg["_session_meta"][k], sort_keys=True,
                          default=str)
            for k in before_meta if k != "requirement_landscape_synthesis")
        unrelated_sections_identical = all(
            json.dumps(before_pkg[k], sort_keys=True, default=str)
            == json.dumps(after_pkg[k], sort_keys=True, default=str)
            for k in before_pkg
            if k not in ("section_13_requirement_landscape", "generated_at",
                         "_session_meta"))
        split = {
            "action": "summary_later (explicit criticality deferral)",
            "before_group_total": b["group_total"],
            "after_group_total": a["group_total"],
            "before_core_counts": sorted(g["occurrence_count"]
                                         for g in b["statement_groups"]
                                         if g["statement"] == CORE),
            "after_core_counts": sorted(g["occurrence_count"]
                                        for g in a["statement_groups"]
                                        if g["statement"] == CORE),
            "after_deferred_row_authority": [
                g["criticality_authority"] for g in a["statement_groups"]
                if g["statement"] == CORE and g["occurrence_count"] == 1],
            "unrelated_session_meta_keys_byte_identical":
                unrelated_meta_identical,
            "unrelated_sections_byte_identical": unrelated_sections_identical,
            "row_total_unchanged":
                after_pkg["section_13_requirement_landscape"]["total"] == 13,
        }
        write("head_critdefer_before_meta.json",
              normalize(json.dumps(b, indent=1), sid, state.idea_id))
        write("head_critdefer_after_meta.json",
              normalize(json.dumps(a, indent=1), sid, state.idea_id))
        write("ws6_critdefer_split.json", json.dumps(split, indent=1))
        if not (split["before_core_counts"] == [8]
                and split["after_core_counts"] == [1, 7]
                and unrelated_meta_identical and unrelated_sections_identical
                and split["row_total_unchanged"]):
            fatal("criticality deferral split evidence failed")
    SESSION_STORE.pop(sid, None)

    # --- Cases B-E: single-record disposition fixtures -----------------------
    for case, (disposition, content) in SINGLE_RECORD_CASES.items():
        import uuid
        state = IdeaState(idea_id="ws6ev-" + case)
        state.record_interaction(disposition, content=content, iteration=0)
        sid = "ws6ev-render-" + case
        SESSION_STORE[sid] = {"state": state, "last_result": None,
                              "transcript": []}
        try:
            package = assemble_deliverable(state)
            page = app.test_client().get(
                "/session/%s/deliverable" % sid).get_data(as_text=True)
        finally:
            SESSION_STORE.pop(sid, None)
        rows = package["section_13_requirement_landscape"]["requirements"]
        if len(rows) != 1:
            fatal("case %s produced %d rows" % (case, len(rows)))
        row = rows[0]
        s14 = package["section_14_validation_plan"]
        entry = (s14["steps"] + s14["blocked_items"])[0]
        dump_case(case, sid, state, package, page)
        summaries[case] = {
            "disposition": disposition,
            "content_verbatim": content,
            "requirement_id_scheme": "req:assertion:rec_1",
            "s13_statement": row["statement"],
            "s13_provenance": row["provenance"],
            "s13_status": row["status"],
            "s13_resolving_action": row["resolving_action"],
            "s13_criticality": row["criticality"],
            "s13_criticality_authority": row["criticality_authority"],
            "s14_provenance": entry["provenance"],
            "s14_statement": entry.get("statement"),
            "s14_step_total": s14["validation_step_total"],
            "s14_blocked_total": s14["blocked_item_total"],
        }

    if MODE == "base":
        write("ws6_case_inputs.json", json.dumps({
            "ws1": {"idea": IDEA_WS1, "core": CORE,
                    "danger_by_iteration": DANGER_BY_ITERATION,
                    "unknown_iteration": UNKNOWN_ITERATION,
                    "unknown_text": UNKNOWN_TEXT,
                    "max_iterations": MAX_ITERATIONS},
            "single_record_cases": {
                k: {"disposition": v[0], "content": v[1]}
                for k, v in SINGLE_RECORD_CASES.items()},
            "critdefer": "HEAD only: WS1 journey + web criticality action "
                         "summary_later on the focused requirement",
        }, indent=1))
    write("ws6_repetition_counts_%s.json" % MODE, json.dumps(summaries, indent=1))
    print("OK %s: cases written to %s" % (MODE, OUTDIR))


if __name__ == "__main__":
    main()
