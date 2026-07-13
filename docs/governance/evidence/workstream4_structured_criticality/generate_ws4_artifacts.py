"""Workstream 4 Structured Criticality Capture — evidence generation harness.

File: docs/governance/evidence/workstream4_structured_criticality/
generate_ws4_artifacts.py
Provenance: a COPY of the harness conventions of the immutable Workstream 1-3
evidence scripts (WS3: docs/governance/evidence/workstream3_deliverable_hygiene/
generate_ws3_artifacts.py) — prior workstream evidence scripts are committed
evidence and are never modified; each workstream copies the harness discipline
into its own self-contained evidence directory and writes ONLY there.
Purpose: generate the deterministic Workstream 4 user-journey evidence at the
reviewed HEAD GREEN commit (61f0b14cb6bf2f5c5328eb9958640bf036015720):
(A) never-interacted; (B) owner-confirmed FEASIBILITY-THREATENING end-to-end;
(C) explicit deferral with the full zero-side-effect comparison for BOTH
"I am not sure yet" and "Decide later"; (D) correction / missing-information
actions storing no confirmation; (E) manipulated/stale POST rejection storing
nothing; plus the deterministic stale-confirmation example proving aggregate
_session_meta surfacing without raw ids.
Input contract: run from the repository root with no arguments; uses only the
committed real application (web.app test client, engine derivations) and the
deterministic non-sensitive fixtures already used by the committed tests.
Output contract: writes the artifact files listed in ARTIFACTS below into
THIS script's directory only, then prints one line per artifact:
"<filename> <sha256-of-normalized-content>". Exit code 0 on success; exit
code 2 with an explicit loud message and NO artifact written if any journey
assertion fails (F3 discipline: silent partial evidence is prohibited).
Prohibited behaviors: MUST NOT modify any file outside this directory; MUST
NOT mutate repository state, scoring, fixtures, or tests; MUST NOT edit or
reword any inventor statement or engine output. The ONLY transformations are
the disclosed normalizations below.

Normalization (disclosed; required for byte-reproducibility): each run
creates random UUIDs (Flask session id, IdeaState.idea_id), one generation
timestamp, and a session-scoped focus token. In every saved artifact the
run's session id is replaced by SESSION_ID, the idea id by IDEA_ID, the
generated-at timestamp by GENERATED_AT_UTC, and each focus token by
FOCUS_TOKEN_<n> in first-appearance order. No other byte is altered.
"""
import hashlib
import json
import os
import re
import sys

sys.path.insert(0, os.getcwd())

from web.app import app, SESSION_STORE, DOMAIN_CONFIRM_VALUE  # noqa: E402
from engine.deliverable_assembler import assemble_deliverable  # noqa: E402
from engine.requirement_landscape import derive_requirement_landscape  # noqa: E402

OUTDIR = os.path.dirname(os.path.abspath(__file__))

# --- Fixed scripted inputs (byte-identical to the committed WS1 baseline /
# tests/test_structured_criticality.py fixtures; do not edit) -----------------
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

RAW_TOKENS = ("FEASIBILITY-THREATENING", "VALUE-ENHANCING", "REFINEMENT",
              "owner-confirmed", "system-derived", "req:assertion:",
              "req:gap:", "req:contradiction:")

FIVE_ACTIONS = ["Yes, that is correct", "Change this part",
                "Something is missing", "I am not sure yet", "Decide later"]

ARTIFACTS = [
    "ws4_journey_never_interacted.json",
    "ws4_journey_owner_confirmed.json",
    "ws4_journey_owner_confirmed_deliverable.html",
    "ws4_journey_deferral_zero_delta.json",
    "ws4_journey_correction.json",
    "ws4_journey_manipulated_rejection.json",
    "ws4_stale_confirmation.json",
]

_TOKEN_RE = re.compile(r'name="focus_token" value="([0-9a-f]{16})"')
_RATIONALE_RE = re.compile(r'<textarea name="rationale"[^>]*>(.*?)</textarea>',
                           re.S)


def _fail(msg):
    print("WS4 EVIDENCE JOURNEY FAILED — %s — no artifact written (F3)." % msg)
    sys.exit(2)


def _require(cond, msg):
    if not cond:
        _fail(msg)


def _start():
    client = app.test_client()
    r = client.post("/start", data={"idea": IDEA_WS1,
                                    "domain_confirm": DOMAIN_CONFIRM_VALUE})
    _require(r.status_code == 302, "/start did not redirect")
    sid = r.headers["Location"].rsplit("/", 1)[-1]
    return client, sid


def _complete(client, sid):
    for i in range(2, MAX_ITERATIONS + 2):
        page = client.get(f"/session/{sid}").get_data(as_text=True)
        if '<p class="complete">' in page:
            return page
        if i == UNKNOWN_ITERATION:
            action, text = "unknown", UNKNOWN_TEXT
        else:
            action, text = "answered", BASE + DANGER_BY_ITERATION.get(i, "")
        client.post(f"/session/{sid}", data={"response": text, "action": action})
    _fail("WS1 journey did not reach completion")


def _page(client, sid):
    return client.get(f"/session/{sid}").get_data(as_text=True)


def _token(page):
    m = _TOKEN_RE.search(page)
    _require(m is not None, "no focus token rendered")
    return m.group(1)


def _history(state):
    return [{
        "confirmation_id": c.confirmation_id, "requirement_id": c.requirement_id,
        "action": c.action, "category": c.category,
        "rationale_verbatim": c.rationale_verbatim,
        "rationale_source": c.rationale_source, "iteration": c.iteration,
        "provenance": c.provenance,
    } for c in state.criticality_confirmations]


def _s13(state):
    return assemble_deliverable(state)["section_13_requirement_landscape"]


def _snapshot(state, entry):
    return {
        "maturity_level": state.maturity_level,
        "iteration": state.iteration,
        "direction": state.direction,
        "gaps": [[g.gap_type, g.status, g.iterations_open] for g in state.gaps],
        "ledger_length": len(state.assertions),
        "acknowledged_unknowns": len(state.acknowledged_unknowns),
        "last_result": entry.get("last_result"),
    }


def _no_raw_tokens(text, where):
    for t in RAW_TOKENS:
        _require(t not in text, "raw token %r exposed in %s" % (t, where))


def _write(name, text, subs):
    for raw, normalized in subs:
        if raw:
            text = text.replace(raw, normalized)
    path = os.path.join(OUTDIR, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    print(name, digest)


def _dump(obj):
    return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False,
                      default=str) + "\n"


def main():
    results = []          # (filename, text, subs)

    # ------------------------------------------------------------------ A
    client, sid = _start()
    _complete(client, sid)
    state = SESSION_STORE[sid]["state"]
    page = _page(client, sid)
    token_a = _token(page)
    _no_raw_tokens(page, "never-interacted completion page")
    _require(all(a in page for a in FIVE_ACTIONS), "five actions missing")
    _require("This is what I understood from your explanation:" in page,
             "summary lead missing")
    s13 = _s13(state)
    _require(all(r["criticality"] == "Not yet determined" and
                 r["criticality_authority"] ==
                 "assigned automatically by the system; not yet reviewed"
                 for r in s13["requirements"]),
             "never-interacted public wording drifted")
    results.append(("ws4_journey_never_interacted.json", _dump({
        "journey": "A_never_interacted",
        "confirmation_history": _history(state),
        "summary_block_present": True,
        "five_lightweight_actions_present": True,
        "section_13": s13,
    }), [(sid, "SESSION_ID"), (state.idea_id, "IDEA_ID"),
         (token_a, "FOCUS_TOKEN_1")]))
    SESSION_STORE.pop(sid, None)

    # ------------------------------------------------------------------ B
    client, sid = _start()
    _complete(client, sid)
    state = SESSION_STORE[sid]["state"]
    page = _page(client, sid)
    token1 = _token(page)
    r1 = client.post(f"/session/{sid}", data={
        "criticality_action": "summary_correct", "focus_token": token1})
    _require(r1.status_code == 302, "summary_correct not accepted")
    _require(state.criticality_confirmations == [],
             "silent adoption: summary_correct stored a confirmation")
    page2 = _page(client, sid)
    _require("Would the idea still achieve its purpose if this part changed?"
             in page2, "clarification missing")
    token2 = _token(page2)
    rationale = _RATIONALE_RE.search(page2)
    _require(rationale is not None, "prefilled rationale missing")
    rationale = rationale.group(1)
    r2 = client.post(f"/session/{sid}", data={
        "criticality_action": "clarify_choice", "focus_token": token2,
        "category_choice": "essential", "rationale": rationale})
    _require(r2.status_code == 302, "acceptance not recorded")
    history = _history(state)
    _require(len(history) == 1 and history[0]["action"] == "confirmed"
             and history[0]["category"] == "FEASIBILITY-THREATENING"
             and history[0]["rationale_source"].startswith("reused_statement:"),
             "confirmed record shape drifted")
    s13 = _s13(state)
    confirmed_rows = [r for r in s13["requirements"]
                      if r["criticality"] == "Essential to feasibility"]
    _require(confirmed_rows and confirmed_rows[0]["criticality_authority"]
             == "Confirmed by the inventor"
             and confirmed_rows[0]["criticality_rationale"] == rationale,
             "section 13 public wording drifted")
    html = client.get(f"/session/{sid}/deliverable").get_data(as_text=True)
    _require("Essential to feasibility" in html
             and "Confirmed by the inventor" in html and rationale in html,
             "rendered HTML wording drifted")
    _no_raw_tokens(json.dumps(assemble_deliverable(state), default=str),
                   "owner-confirmed deliverable JSON")
    _no_raw_tokens(html, "owner-confirmed deliverable HTML")
    package = assemble_deliverable(state)
    generated_at = package.get("generated_at") or ""
    results.append(("ws4_journey_owner_confirmed.json", _dump({
        "journey": "B_owner_confirmed_feasibility_threatening",
        "post_statuses": {"summary_correct": r1.status_code,
                          "clarify_choice_essential": r2.status_code},
        "zero_retype_rationale_reused_verbatim": True,
        "confirmation_history": history,
        "section_13": s13,
        "raw_token_scan": "no raw category/authority/provenance/requirement-id "
                          "token in deliverable JSON or HTML",
    }), [(sid, "SESSION_ID"), (state.idea_id, "IDEA_ID"),
         (token1, "FOCUS_TOKEN_1"), (token2, "FOCUS_TOKEN_2"),
         (generated_at, "GENERATED_AT_UTC")]))
    results.append(("ws4_journey_owner_confirmed_deliverable.html", html,
                    [(sid, "SESSION_ID"), (state.idea_id, "IDEA_ID"),
                     (generated_at, "GENERATED_AT_UTC")]))
    SESSION_STORE.pop(sid, None)

    # ------------------------------------------------------------------ C (+7)
    deferral_evidence = {}
    for action in ("summary_unsure", "summary_later"):
        client, sid = _start()
        _complete(client, sid)
        state = SESSION_STORE[sid]["state"]
        entry = SESSION_STORE[sid]
        token = _token(_page(client, sid))
        before_snap = _snapshot(state, entry)
        before_pkg = assemble_deliverable(state)
        r = client.post(f"/session/{sid}", data={
            "criticality_action": action, "focus_token": token})
        _require(r.status_code == 302, "%s not accepted" % action)
        after_snap = _snapshot(state, entry)
        after_pkg = assemble_deliverable(state)
        _require(before_snap == after_snap, "%s altered session state" % action)
        unchanged = []
        for key in before_pkg:
            if key in ("section_13_requirement_landscape", "generated_at"):
                continue
            _require(json.dumps(before_pkg[key], sort_keys=True, default=str)
                     == json.dumps(after_pkg[key], sort_keys=True, default=str),
                     "%s altered deliverable section %s" % (action, key))
            unchanged.append(key)
        history = _history(state)
        _require(len(history) == 1 and history[0]["action"] == "deferred"
                 and history[0]["category"] is None,
                 "deferred record shape drifted")
        rows = [r_ for r_ in _s13(state)["requirements"]
                if r_["criticality_authority"] == "Confirmation not yet available"]
        _require(rows and rows[0]["criticality"] == "Not yet determined",
                 "deferred public wording drifted")
        deferral_evidence[action] = {
            "post_status": r.status_code,
            "state_snapshot_before": before_snap,
            "state_snapshot_after": after_snap,
            "snapshots_identical": before_snap == after_snap,
            "unchanged_deliverable_sections": unchanged,
            "confirmation_history": history,
            "deferred_section13_row": rows[0],
            "_normalize": [(sid, "SESSION_ID"), (state.idea_id, "IDEA_ID"),
                           (token, "FOCUS_TOKEN_1")],
        }
        SESSION_STORE.pop(sid, None)
    subs = []
    for i, (action, ev) in enumerate(sorted(deferral_evidence.items())):
        for j, (raw, norm) in enumerate(ev.pop("_normalize")):
            subs.append((raw, norm.replace("_1", "_%d" % (i * 3 + j + 1))))
    results.append(("ws4_journey_deferral_zero_delta.json",
                    _dump({"journey": "C_explicit_deferral_zero_side_effects",
                           "actions": deferral_evidence}), subs))

    # ------------------------------------------------------------------ D
    client, sid = _start()
    _complete(client, sid)
    state = SESSION_STORE[sid]["state"]
    correction_evidence = {}
    for action in ("summary_change", "summary_missing"):
        token = _token(_page(client, sid))
        r = client.post(f"/session/{sid}", data={
            "criticality_action": action, "focus_token": token})
        _require(r.status_code == 302, "%s not accepted" % action)
        _require(state.criticality_confirmations == [],
                 "%s stored a confirmation" % action)
        page = _page(client, sid)
        _require('name="response"' in page,
                 "no free-text path offered after %s" % action)
        r2 = client.post(f"/session/{sid}", data={
            "response": "The relay module is the part that changed.",
            "action": "answered"})
        _require(r2.status_code == 302, "existing answer path unavailable")
        _require(state.criticality_confirmations == [],
                 "answer path stored a confirmation")
        correction_evidence[action] = {
            "post_status": r.status_code,
            "confirmation_stored": False,
            "free_text_form_offered": True,
            "followup_answer_status": r2.status_code,
        }
    results.append(("ws4_journey_correction.json", _dump({
        "journey": "D_correction_and_missing_information",
        "actions": correction_evidence,
        "confirmation_history_final": _history(state),
    }), [(sid, "SESSION_ID"), (state.idea_id, "IDEA_ID")]))
    SESSION_STORE.pop(sid, None)

    # ------------------------------------------------------------------ E
    client, sid = _start()
    _complete(client, sid)
    state = SESSION_STORE[sid]["state"]
    token = _token(_page(client, sid))
    rejections = {}
    for name, form in (
        ("wrong_focus_token", {"criticality_action": "summary_correct",
                               "focus_token": "0" * 16}),
        ("unknown_action", {"criticality_action": "bogus_action",
                            "focus_token": token}),
        ("clarify_without_summary_step",
         {"criticality_action": "clarify_choice", "focus_token": token,
          "category_choice": "essential", "rationale": "text"}),
    ):
        r = client.post(f"/session/{sid}", data=form)
        _require(r.status_code == 400, "%s not rejected" % name)
        _require(state.criticality_confirmations == [],
                 "%s stored a confirmation" % name)
        rejections[name] = {"status": 400, "stored": False}
    r = client.post(f"/session/{sid}", data={
        "criticality_action": "summary_correct", "focus_token": token})
    _require(r.status_code == 302, "legitimate summary step failed")
    page = _page(client, sid)
    token2 = _token(page)
    rationale = _RATIONALE_RE.search(page).group(1)
    for name, form in (
        ("manipulated_category_UNDETERMINED",
         {"criticality_action": "clarify_choice", "focus_token": token2,
          "category_choice": "UNDETERMINED", "rationale": rationale}),
        ("emptied_rationale",
         {"criticality_action": "clarify_choice", "focus_token": token2,
          "category_choice": "essential", "rationale": "   "}),
    ):
        r = client.post(f"/session/{sid}", data=form)
        _require(r.status_code == 400, "%s not rejected" % name)
        _require(state.criticality_confirmations == [],
                 "%s stored a confirmation" % name)
        rejections[name] = {"status": 400, "stored": False}
    results.append(("ws4_journey_manipulated_rejection.json", _dump({
        "journey": "E_manipulated_or_stale_post_rejection",
        "rejections": rejections,
        "confirmation_history_final": _history(state),
    }), [(sid, "SESSION_ID"), (state.idea_id, "IDEA_ID"),
         (token, "FOCUS_TOKEN_1"), (token2, "FOCUS_TOKEN_2")]))
    SESSION_STORE.pop(sid, None)

    # ------------------------------------------------------------------ stale
    client, sid = _start()
    _complete(client, sid)
    state = SESSION_STORE[sid]["state"]
    stale_id = "req:assertion:rec_999"   # deterministically never generated
    state.record_criticality_confirmation(
        requirement_id=stale_id, action="deferred", iteration=state.iteration)
    generated = {r.requirement_id
                 for r in derive_requirement_landscape(state).requirements}
    _require(stale_id not in generated, "stale fixture id unexpectedly generated")
    package = assemble_deliverable(state)
    meta = package["_session_meta"]["stale_criticality_confirmations"]
    _require(meta["total"] == 1 and meta["note"], "stale aggregate missing")
    _require(all(r.criticality_authority == "system-derived"
                 for r in derive_requirement_landscape(state).requirements),
             "stale confirmation was reattached to a live requirement")
    package_text = json.dumps(package, default=str)
    _require("rec_999" not in json.dumps(
        package["_session_meta"]["stale_criticality_confirmations"])
        and package_text.count(stale_id) == 0,
        "raw stale requirement id exported")
    generated_at = package.get("generated_at") or ""
    results.append(("ws4_stale_confirmation.json", _dump({
        "journey": "stale_confirmation_surfacing",
        "recorded_stale_requirement_id_kept_in_session_history_only": True,
        "stale_aggregate_metadata": meta,
        "reattachment": "none — every generated requirement keeps its own "
                        "authority; the stale record applies to nothing",
        "raw_stale_id_exported": False,
        "confirmation_history": _history(state),
    }), [(sid, "SESSION_ID"), (state.idea_id, "IDEA_ID"),
         (generated_at, "GENERATED_AT_UTC")]))
    SESSION_STORE.pop(sid, None)

    for name, text, subs in results:
        _write(name, text, subs)


if __name__ == "__main__":
    main()
