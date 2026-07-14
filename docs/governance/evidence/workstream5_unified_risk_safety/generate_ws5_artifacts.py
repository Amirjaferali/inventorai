"""Workstream 5 Unified Risk and Safety Presentation — evidence harness.

File: docs/governance/evidence/workstream5_unified_risk_safety/
generate_ws5_artifacts.py
Provenance: a COPY of the harness conventions of the immutable Workstream 1-4
evidence scripts (WS4: docs/governance/evidence/workstream4_structured_criticality/
generate_ws4_artifacts.py) — prior workstream evidence scripts are committed
evidence and are never modified; each workstream copies the harness discipline
into its own self-contained evidence directory.
Purpose: generate the deterministic Workstream 5 deliverable artifacts for the
three evidence cases — (A) the byte-identical committed WS1 safety-bearing
journey; (B) the mature/gap-free signal-bearing state (the committed PR #122
positive statement on a demonstrated-quality, gap-free session); (C) the
no-signal fresh session — plus, in head mode, the machine-generated JSON/HTML
parity record.
Input contract: run from the repository root of the checkout to be evidenced,
with exactly two arguments: MODE ("base" or "head" — the artifact filename
prefix; "base" is run from a clean checkout of the RED commit
3cef5eb79a3c3483903f3e0acbe59c18dc05caf0, "head" from the GREEN commit
97b6725953150509059dd41ba623e438f939f094) and OUTDIR (the absolute path of
the Workstream 5 evidence directory to write into).
Output contract: writes ONLY <mode>_<case>_deliverable.{json,html} for the
three cases (plus ws5_json_html_parity.json in head mode) into OUTDIR, then
prints one "<filename> <sha256-of-normalized-content>" line per artifact.
Exit 0 on success; exit 2 with a loud message and NO artifact written if any
case assertion fails (F3 discipline: silent partial evidence is prohibited).
Prohibited behaviors: MUST NOT modify any file outside OUTDIR; MUST NOT
mutate repository state, scoring, fixtures, or tests; MUST NOT reword any
inventor statement or engine output. The ONLY transformations are the
disclosed normalizations below. Base-mode assertions check only mode-neutral
facts (journey completion, signal presence/absence, Section 6 state) — never
the Workstream 5 linkage behavior, which is absent by definition at BASE.

Normalization (disclosed; required for byte-reproducibility): each run
creates random UUIDs (Flask session id, IdeaState.idea_id) and one
generation timestamp; in every saved artifact the session id is replaced by
SESSION_ID, the idea id by IDEA_ID, and the generated-at timestamp by
GENERATED_AT_UTC. No other byte is altered.
"""
import hashlib
import json
import os
import re
import sys

sys.path.insert(0, os.getcwd())

from web.app import app, SESSION_STORE, DOMAIN_CONFIRM_VALUE  # noqa: E402
from engine.deliverable_assembler import assemble_deliverable  # noqa: E402
from engine.idea_state import DEMONSTRATED  # noqa: E402

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

WORDINGS = {
    "section_6_note": (
        "You also described possible safety consequences in your own words.\n"
        "See “Inventor-Stated Safety Signals.”\n\n"
        "These are your statements, not confirmed risks, and they still require\n"
        "independent validation."),
    "section_6_empty_qualification": (
        "No system-derived risks were identified from the current session state.\n\n"
        "This does not mean the idea is safe or risk-free. Safety consequences you\n"
        "described are listed separately under “Inventor-Stated Safety Signals” and\n"
        "have not been independently validated."),
    "section_13_note": (
        "You also described possible safety consequences in your own words.\n\n"
        "They are listed separately under “Inventor-Stated Safety Signals.” They are\n"
        "not structural risk records and have not been independently validated."),
}


def _fail(msg):
    print("WS5 EVIDENCE CASE FAILED — %s — no artifact written (F3)." % msg)
    sys.exit(2)


def _require(cond, msg):
    if not cond:
        _fail(msg)


def _collapse(text):
    return " ".join(text.split())


def _start():
    client = app.test_client()
    r = client.post("/start", data={"idea": IDEA_WS1,
                                    "domain_confirm": DOMAIN_CONFIRM_VALUE})
    _require(r.status_code == 302, "/start did not redirect")
    return client, r.headers["Location"].rsplit("/", 1)[-1]


def _complete(client, sid):
    for i in range(2, MAX_ITERATIONS + 2):
        page = client.get(f"/session/{sid}").get_data(as_text=True)
        if '<p class="complete">' in page:
            return
        if i == UNKNOWN_ITERATION:
            action, text = "unknown", UNKNOWN_TEXT
        else:
            action, text = "answered", BASE + DANGER_BY_ITERATION.get(i, "")
        client.post(f"/session/{sid}", data={"response": text, "action": action})
    _fail("WS1 journey did not reach completion")


def _capture(client, sid, expect_signals, expect_s6_rows):
    state = SESSION_STORE[sid]["state"]
    package = assemble_deliverable(state)
    signals = package["_session_meta"]["inventor_stated_safety_signals"]
    _require(bool(signals["signals"]) == expect_signals,
             "unexpected signal state (expected signals=%s, got %d)"
             % (expect_signals, signals["total"]))
    _require(bool(package["section_6_risks"]["risks"]) == expect_s6_rows,
             "unexpected Section 6 state (expected rows=%s, got %d)"
             % (expect_s6_rows, package["section_6_risks"]["total"]))
    html = client.get(f"/session/{sid}/deliverable").get_data(as_text=True)
    generated_at = package.get("generated_at") or ""
    text = json.dumps(package, indent=2, sort_keys=True, ensure_ascii=False,
                      default=str) + "\n"
    subs = [(sid, "SESSION_ID"), (state.idea_id, "IDEA_ID"),
            (generated_at, "GENERATED_AT_UTC")]
    SESSION_STORE.pop(sid, None)
    return package, text, html, subs


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ("base", "head"):
        _fail("usage: generate_ws5_artifacts.py base|head OUTDIR")
    mode, outdir = sys.argv[1], os.path.abspath(sys.argv[2])
    results = []

    # A. WS1 safety-bearing journey (signals present; Section 6 has rows).
    client, sid = _start()
    _complete(client, sid)
    pkg_a, json_a, html_a, subs_a = _capture(client, sid, True, True)
    results.append(("%s_ws1_safety_deliverable" % mode, json_a, html_a, subs_a))

    # B. Mature/gap-free signal-bearing state (signals present; zero rows).
    client, sid = _start()
    state = SESSION_STORE[sid]["state"]
    state.maturity_level = 2
    state.gaps = []
    if state.known_mechanism is not None:
        state.known_mechanism.quality = DEMONSTRATED
    if state.known_problem is not None:
        state.known_problem.quality = DEMONSTRATED
    state.record_interaction(action="answered", content=POSITIVE_STATEMENT,
                             gap_context=None, iteration=state.iteration)
    pkg_b, json_b, html_b, subs_b = _capture(client, sid, True, False)
    results.append(("%s_mature_gapfree_deliverable" % mode, json_b, html_b, subs_b))

    # C. No-signal fresh session (no signals; Section 6 has rows).
    client, sid = _start()
    pkg_c, json_c, html_c, subs_c = _capture(client, sid, False, True)
    results.append(("%s_no_signal_deliverable" % mode, json_c, html_c, subs_c))

    written = []
    for name, json_text, html, subs in results:
        for suffix, text in ((".json", json_text), (".html", html)):
            normalized = text
            for raw, repl in subs:
                if raw:
                    normalized = normalized.replace(raw, repl)
            path = os.path.join(outdir, name + suffix)
            with open(path, "w", encoding="utf-8") as f:
                f.write(normalized)
            written.append((name + suffix,
                            hashlib.sha256(normalized.encode()).hexdigest()))

    if mode == "head":
        # Machine-generated JSON/HTML parity record (evidence item 9).
        parity = []
        for case, pkg, html in (("ws1_safety", pkg_a, html_a),
                                ("mature_gapfree", pkg_b, html_b),
                                ("no_signal", pkg_c, html_c)):
            linkage = pkg["_session_meta"]["risk_safety_linkage"]
            ch = _collapse(html)
            entry = {"case": case, "wordings": {}, "totals": {}}
            for field, wording in WORDINGS.items():
                json_value = linkage[field]
                rendered = _collapse(wording) in ch
                _require((json_value == wording and rendered) or
                         (json_value is None and not rendered),
                         "parity violated for %s in %s" % (field, case))
                entry["wordings"][field] = {
                    "json_value_byte_exact": json_value == wording,
                    "json_value_null": json_value is None,
                    "rendered_in_html": rendered,
                }
            signals = pkg["_session_meta"]["inventor_stated_safety_signals"]
            s6 = pkg["section_6_risks"]
            checks = {
                "signal_total": (linkage["signal_total"], signals["total"]),
                "section_6_risk_total": (linkage["section_6_risk_total"], s6["total"]),
                "section_6_high_count": (linkage["section_6_high_count"], s6["high_count"]),
                "section_6_medium_count": (linkage["section_6_medium_count"], s6["medium_count"]),
                "section_6_low_count": (linkage["section_6_low_count"], s6["low_count"]),
                "section_13_has_structural_risks": (
                    linkage["section_13_has_structural_risks"],
                    pkg["section_13_requirement_landscape"]["has_risks"]),
            }
            for key, (a, b) in checks.items():
                _require(a == b, "linkage total mismatch %s in %s" % (key, case))
                entry["totals"][key] = {"linkage": a, "underlying_block": b,
                                        "match": True}
            parity.append(entry)
        text = json.dumps({"generated_from": "head",
                           "parity_cases": parity}, indent=2,
                          ensure_ascii=False) + "\n"
        path = os.path.join(outdir, "ws5_json_html_parity.json")
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        written.append(("ws5_json_html_parity.json",
                        hashlib.sha256(text.encode()).hexdigest()))

    for name, digest in written:
        print(name, digest)


if __name__ == "__main__":
    main()
