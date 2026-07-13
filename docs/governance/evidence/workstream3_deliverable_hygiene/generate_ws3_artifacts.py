"""Workstream 3 Deliverable Hygiene — post-merge evidence generation harness.

File: docs/governance/evidence/workstream3_deliverable_hygiene/generate_ws3_artifacts.py
Provenance: a COPY of the harness conventions of the immutable Workstream 1
evidence script (docs/governance/evidence/workstream1_deliverable_baseline/
reproduce_baseline.py) and the Workstream 2 copy (contract §17 / F4: prior
workstream evidence scripts are committed evidence and are never modified;
each workstream copies the harness discipline into its own self-contained
evidence directory and writes ONLY there).
Purpose: generate the representative inventor-facing Final Deliverable JSON
and HTML artifacts for the five Workstream 3 evidence journeys at the
canonical merged tip (0b04021d99290f8f747ee24d46b93c1dda69d66f), where the
merged hygiene implementation MUST export no raw internal machine token.
F3 (contract §16): if the completed WS1 journey does not reach the completion
branch within the iteration bound, this harness prints an explicit
"JOURNEY INCOMPLETE" message, exits non-zero, and writes NO artifact for any
journey (all artifact writes happen only after every journey assertion passes).
Input contract: run from the repository root with no arguments.
Output contract: writes the artifact files listed in ARTIFACTS below into
THIS script's directory only, then prints one line per artifact:
"<filename> <sha256-of-normalized-content>". Exit code 0 on success; exit
code 2 with "JOURNEY INCOMPLETE" if the completed journey does not complete.
Prohibited behaviors: MUST NOT modify any file outside this directory (never
the Workstream 1 or Workstream 2 evidence directories); MUST NOT mutate
repository state, scoring, fixtures, or tests; MUST NOT edit, clean up,
summarize, or reword any inventor statement or any engine output (the ONLY
transformation applied is the disclosed normalization of run-random
identifiers below).

Normalization (disclosed; required for byte-reproducibility): each run creates
random UUIDs (Flask session id, IdeaState.idea_id) and one generation
timestamp. In every saved artifact the run's session id is replaced by
SESSION_ID, the idea id by IDEA_ID, and the generated-at timestamp by
GENERATED_AT_UTC (its real value is printed to stdout for the identity
record). No other byte is altered.
"""
import hashlib
import json
import os
import sys

sys.path.insert(0, os.getcwd())

from web.app import app, SESSION_STORE, DOMAIN_CONFIRM_VALUE  # noqa: E402
from engine.deliverable_assembler import assemble_deliverable  # noqa: E402

OUTDIR = os.path.dirname(os.path.abspath(__file__))

# --- Fixed scripted inputs (verbatim; byte-identical to the committed WS1
# baseline inputs where the journey is the WS1 journey; do not edit) ----------
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

IDEA_POSITIVE = (
    "A smart plug-in safety device for home appliances using current and "
    "voltage sensing, a microcontroller, Wi-Fi, an LED buzzer warning, and a "
    "plug housing"
)
POSITIVE_STATEMENT = (
    "If insulation cannot be safely achieved inside the plug housing, the "
    "device should not be used because it could create a safety risk."
)

ARTIFACTS = [
    "ws1_completed_deliverable.json",
    "ws1_completed_deliverable.html",
    "no_answer_deliverable.json",
    "no_answer_deliverable.html",
    "unknown_action_deliverable.json",
    "unknown_action_deliverable.html",
    "safety_signal_deliverable.json",
    "safety_signal_deliverable.html",
    "legacy_provenance_deliverable.json",
    "legacy_provenance_deliverable.html",
]


def _normalize(text, sid, idea_id, generated_at):
    text = text.replace(sid, "SESSION_ID").replace(idea_id, "IDEA_ID")
    if generated_at:
        text = text.replace(generated_at, "GENERATED_AT_UTC")
    return text


def _write(name, text, sid, idea_id, generated_at):
    normalized = _normalize(text, sid, idea_id, generated_at)
    path = os.path.join(OUTDIR, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(normalized)
    digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
    print(name, digest)


def _start(idea):
    client = app.test_client()
    r = client.post("/start", data={"idea": idea,
                                    "domain_confirm": DOMAIN_CONFIRM_VALUE})
    assert r.status_code == 302, r.status_code
    sid = r.headers["Location"].rsplit("/", 1)[-1]
    return client, sid


def _capture(client, sid, prefix, results):
    st = SESSION_STORE[sid]["state"]
    package = assemble_deliverable(st)
    generated_at = package.get("generated_at") or ""
    html = client.get(f"/session/{sid}/deliverable").get_data(as_text=True)
    print(f"{prefix}.session_id", sid)
    print(f"{prefix}.idea_id", st.idea_id)
    print(f"{prefix}.generated_at", generated_at or "(none)")
    results.append((prefix, sid, st.idea_id, generated_at,
                    json.dumps(package, indent=2, sort_keys=True,
                               ensure_ascii=False, default=str) + "\n",
                    html))
    SESSION_STORE.pop(sid, None)


def main():
    results = []

    # 1) Completed WS1 journey (F3: completion branch is REQUIRED).
    client, sid = _start(IDEA_WS1)
    completed = False
    for i in range(2, MAX_ITERATIONS + 2):
        page = client.get(f"/session/{sid}").get_data(as_text=True)
        if '<p class="complete">' in page:
            completed = True
            break
        if i == UNKNOWN_ITERATION:
            action, text = "unknown", UNKNOWN_TEXT
        else:
            action, text = "answered", BASE + DANGER_BY_ITERATION.get(i, "")
        client.post(f"/session/{sid}", data={"response": text, "action": action})
    if not completed:
        SESSION_STORE.pop(sid, None)
        print("JOURNEY INCOMPLETE — completion branch not reached within "
              "%d iterations; no artifact written (contract §16 / F3)."
              % MAX_ITERATIONS)
        sys.exit(2)
    _capture(client, sid, "ws1_completed", results)

    # 2) No-substantive-answer journey (open-gap Section 12 path).
    client, sid = _start(IDEA_WS1)
    _capture(client, sid, "no_answer", results)

    # 3) Unknown-action journey (single structured non-answer disposition).
    client, sid = _start(IDEA_WS1)
    client.post(f"/session/{sid}", data={"response": UNKNOWN_TEXT,
                                         "action": "unknown"})
    _capture(client, sid, "unknown_action", results)

    # 4) Safety-Signal-present journey (the committed PR #122 positive
    #    baseline statement, verbatim).
    client, sid = _start(IDEA_POSITIVE)
    client.post(f"/session/{sid}", data={"response": POSITIVE_STATEMENT,
                                         "action": "answered"})
    _capture(client, sid, "safety_signal", results)

    # 5) Legacy-provenance journey: one accepted-reasoning answer; the
    #    committed capture path records evidence with the legacy default
    #    provenance, exercising the provenance serialization mapping.
    client, sid = _start(IDEA_WS1)
    client.post(f"/session/{sid}", data={"response": BASE, "action": "answered"})
    _capture(client, sid, "legacy_provenance", results)

    for prefix, sid, idea_id, generated_at, package_json, html in results:
        _write(f"{prefix}_deliverable.json", package_json, sid, idea_id,
               generated_at)
        _write(f"{prefix}_deliverable.html", html, sid, idea_id, generated_at)


if __name__ == "__main__":
    main()
