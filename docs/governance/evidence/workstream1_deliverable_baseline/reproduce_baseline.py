"""Workstream 1 Evidence Lock — deterministic baseline reproduction script.

File: docs/governance/evidence/workstream1_deliverable_baseline/reproduce_baseline.py
Purpose: regenerate, byte-reproducibly, the two Workstream 1 baseline evidence
bundles defined by DELIVERABLE_STABILIZATION_REMEDIATION_PLAN.md §7:
  (1) the CURRENT safety-signal FALSE-NEGATIVE baseline — a full scripted
      journey whose inventor statements explicitly describe dangerous
      consequences, after which derive_inventor_stated_safety_signals()
      returns ZERO signals;
  (2) the safety-signal POSITIVE baseline — the exact inventor statement from
      the committed PR #122 manual-demo record, which DOES produce a signal.
Input contract: run from the repository root with no arguments
      (python3 docs/governance/evidence/workstream1_deliverable_baseline/reproduce_baseline.py).
      Requires only the repository code plus Flask (web/app.py's own import).
Output contract: writes the artifact files listed in ARTIFACTS below into this
      script's directory, then prints one line per artifact:
      "<filename> <sha256-of-normalized-content>". Exit code 0 on success.
Prohibited behaviors: MUST NOT modify any file outside this directory; MUST
      NOT mutate repository state, scoring, fixtures, or tests; MUST NOT edit,
      clean up, summarize, or reword any inventor statement or any engine
      output (the ONLY transformation applied is the disclosed normalization
      of run-random identifiers below).

Normalization (disclosed; required for byte-reproducibility): each run creates
random UUIDs (Flask session id, IdeaState.idea_id) and one generation
timestamp (deliverable _session_meta). In every saved artifact the run's
session id is replaced by SESSION_ID, the idea id by IDEA_ID, and the
generated-at timestamp by GENERATED_AT_UTC (its real value is printed to
stdout for the identity record). No other byte is altered.
"""
import hashlib
import json
import os
import re
import sys

sys.path.insert(0, os.getcwd())

from web.app import app, SESSION_STORE, DOMAIN_CONFIRM_VALUE  # noqa: E402
from engine.deliverable_assembler import assemble_deliverable  # noqa: E402
from engine.safety_signal import derive_inventor_stated_safety_signals  # noqa: E402

OUTDIR = os.path.dirname(os.path.abspath(__file__))

# --- Fixed scripted inputs (verbatim; do not edit) ---------------------------
IDEA_FALSE_NEGATIVE = (
    "A smart plug-in safety device that senses appliance current and voltage "
    "with a microcontroller and disconnects a relay to warn about dangerous "
    "appliances"
)
# Accepted-reasoning carrier sentence (deterministically REASONED under the
# committed Layer-2 gate), reused verbatim so journey progression is stable.
BASE = ("The current sensor detects an abnormal rise because the shunt "
        "resistor voltage increases, therefore the microcontroller opens the "
        "relay to disconnect the appliance.")
# Inventor-stated dangerous-consequence statements (the Workstream 1 required
# key statements, verbatim). Appended to the carrier sentence at the fixed
# iterations below.
DANGER_BY_ITERATION = {
    3: " If the sensing is wrong, the dangerous appliance could remain powered.",
    4: (" If it trips the wrong branch, the wrong appliance could be "
        "disconnected and it would fail to isolate the actual source of danger."),
    6: (" If the relay sticks, damage or overheating could continue and the "
        "fire risk could continue until someone notices."),
    7: (" The current sensing accuracy is essential; the buzzer volume and "
        "alert timing are adjustable."),
}
# One fixed unknown-response probe (evidence item 11: unknown-path behavior).
UNKNOWN_ITERATION = 5
UNKNOWN_TEXT = "I don't know yet."
MAX_ITERATIONS = 30

IDEA_POSITIVE = (
    "A smart plug-in safety device for home appliances using current and "
    "voltage sensing, a microcontroller, Wi-Fi, an LED buzzer warning, and a "
    "plug housing"
)
# Exact inventor-stated safety condition from the committed PR #122 record
# (docs/governance/PR122_INVENTOR_STATED_SAFETY_SIGNALS_MANUAL_DEMO_VERIFICATION.md §4).
POSITIVE_STATEMENT = (
    "If insulation cannot be safely achieved inside the plug housing, the "
    "device should not be used because it could create a safety risk."
)

ARTIFACTS = [
    "inputs_false_negative_journey.json",
    "journey_log_false_negative.json",
    "deliverable_false_negative.json",
    "deliverable_false_negative.html",
    "safety_signals_false_negative.json",
    "inputs_positive_baseline.json",
    "deliverable_positive_regenerated.json",
    "deliverable_positive_regenerated.html",
    "safety_signals_positive_regenerated.json",
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


def _signals_json(signals):
    return json.dumps([s.__dict__ for s in signals], indent=2, sort_keys=True,
                      ensure_ascii=False, default=str) + "\n"


def _question_of(page):
    m = re.search(r'<p class="question">(.*?)</p>', page, re.S)
    return " ".join(m.group(1).split()) if m else None


def run_false_negative():
    c = app.test_client()
    r = c.post("/start", data={"idea": IDEA_FALSE_NEGATIVE,
                               "domain_confirm": DOMAIN_CONFIRM_VALUE})
    assert r.status_code == 302, r.status_code
    sid = r.headers["Location"].rsplit("/", 1)[-1]
    idea_id = SESSION_STORE[sid]["state"].idea_id

    inputs = {"idea": IDEA_FALSE_NEGATIVE, "steps": []}
    log = []
    for i in range(2, MAX_ITERATIONS + 2):
        page = c.get(f"/session/{sid}").get_data(as_text=True)
        # True completion branch only (template <p class="complete">). The
        # maturity-2 stage label ALSO contains the words "worked through the
        # key questions" (web/gap_labels.py) while Stage-3 questions are still
        # active — an observation preserved in the journey log, and the reason
        # this detector must not match on that phrase.
        completed = '<p class="complete">' in page
        question = _question_of(page)
        if "worked through the key questions" in page and not completed:
            log.append({"iteration": i,
                        "observation": ("stage label already says 'You have "
                                        "worked through the key questions' "
                                        "while a question is still being asked")})
        if completed:
            log.append({"iteration": i, "page_state": "COMPLETION_BRANCH",
                        "question": question,
                        "open_gaps_at_render": [
                            (g.gap_type, g.status)
                            for g in SESSION_STORE[sid]["state"].get_open_gaps()]})
            break
        if i == UNKNOWN_ITERATION:
            action, text = "unknown", UNKNOWN_TEXT
        else:
            action, text = "answered", BASE + DANGER_BY_ITERATION.get(i, "")
        inputs["steps"].append({"iteration": i, "action": action, "text": text})
        c.post(f"/session/{sid}", data={"response": text, "action": action})
        e = SESSION_STORE[sid]
        lr = e.get("last_result") or {}
        st = e["state"]
        log.append({
            "iteration": i,
            "question_shown": question,
            "action": action,
            "response_verbatim": text,
            "transition": lr.get("transition"),
            "reason": lr.get("reason"),
            "direction": lr.get("direction"),
            "maturity_after": st.maturity_level,
            "gaps_after": [(g.gap_type, g.status) for g in st.gaps],
            "acknowledged_unknowns_after": len(st.acknowledged_unknowns),
        })

    st = SESSION_STORE[sid]["state"]
    package = assemble_deliverable(st)
    generated_at = (package.get("generated_at")
                    or (package.get("_session_meta", {}) or {}).get("generated_at")
                    or "")
    html = c.get(f"/session/{sid}/deliverable").get_data(as_text=True)
    signals = derive_inventor_stated_safety_signals(st)

    print("false_negative.session_id", sid)
    print("false_negative.idea_id", idea_id)
    print("false_negative.generated_at", generated_at or "(none)")
    print("false_negative.signal_count", len(signals))
    _write("inputs_false_negative_journey.json",
           json.dumps(inputs, indent=2, ensure_ascii=False) + "\n",
           sid, idea_id, generated_at)
    _write("journey_log_false_negative.json",
           json.dumps(log, indent=2, ensure_ascii=False) + "\n",
           sid, idea_id, generated_at)
    _write("deliverable_false_negative.json",
           json.dumps(package, indent=2, sort_keys=True, ensure_ascii=False,
                      default=str) + "\n",
           sid, idea_id, generated_at)
    _write("deliverable_false_negative.html", html, sid, idea_id, generated_at)
    _write("safety_signals_false_negative.json", _signals_json(signals),
           sid, idea_id, generated_at)
    SESSION_STORE.pop(sid, None)
    return len(signals)


def run_positive():
    c = app.test_client()
    r = c.post("/start", data={"idea": IDEA_POSITIVE,
                               "domain_confirm": DOMAIN_CONFIRM_VALUE})
    assert r.status_code == 302, r.status_code
    sid = r.headers["Location"].rsplit("/", 1)[-1]
    idea_id = SESSION_STORE[sid]["state"].idea_id
    c.post(f"/session/{sid}", data={"response": POSITIVE_STATEMENT,
                                    "action": "answered"})
    st = SESSION_STORE[sid]["state"]
    package = assemble_deliverable(st)
    generated_at = (package.get("generated_at")
                    or (package.get("_session_meta", {}) or {}).get("generated_at")
                    or "")
    html = c.get(f"/session/{sid}/deliverable").get_data(as_text=True)
    signals = derive_inventor_stated_safety_signals(st)

    print("positive.session_id", sid)
    print("positive.idea_id", idea_id)
    print("positive.generated_at", generated_at or "(none)")
    print("positive.signal_count", len(signals))
    _write("inputs_positive_baseline.json",
           json.dumps({"idea": IDEA_POSITIVE,
                       "steps": [{"iteration": 2, "action": "answered",
                                  "text": POSITIVE_STATEMENT}]},
                      indent=2, ensure_ascii=False) + "\n",
           sid, idea_id, generated_at)
    _write("deliverable_positive_regenerated.json",
           json.dumps(package, indent=2, sort_keys=True, ensure_ascii=False,
                      default=str) + "\n",
           sid, idea_id, generated_at)
    _write("deliverable_positive_regenerated.html", html, sid, idea_id,
           generated_at)
    _write("safety_signals_positive_regenerated.json", _signals_json(signals),
           sid, idea_id, generated_at)
    SESSION_STORE.pop(sid, None)
    return len(signals)


if __name__ == "__main__":
    fn = run_false_negative()
    pos = run_positive()
    print("RESULT false_negative_signals=%d positive_signals=%d" % (fn, pos))
