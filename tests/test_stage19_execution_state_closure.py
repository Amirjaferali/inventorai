# -*- coding: utf-8 -*-
"""STAGE 19 — EXPERIMENT EXECUTION-STATE DISCLOSURE — CLOSURE (Owner-authorized).

What is pinned: for each CURRENT Section-11 experiment, the report and the PDF state
exactly ONE execution state derived from the committed, wholly validated Result Event
history (engine/experiment_result.py, unchanged):

* NO RESULT    — the history was read and the experiment has zero execution roots;
* RECORDED N   — N = the number of execution ROOTS (``result_chains``): a correction
                 never adds one, an independent retest does;
* UNAVAILABLE  — the history could not be read or validated (never "no result", never 0).

It is a read-only web-layer projection keyed ONLY by the canonical ``experiment_id``:
no result text, earlier entry, frozen context or identifier is disclosed; nothing is
compared, graded or interpreted; the canonical deliverable package, the Result owner,
its persistence and every state / readiness / progression owner are unchanged. The
Section-11 advisory note no longer says nothing was tested: it separates the inventor's
own recorded executions from InventorAI, which performs, checks and validates nothing.

Why a separate test file: Result Event Slice 1 keeps its owner in
``tests/test_cap09_result_events.py`` (whose harness this reuses); the closure's report /
PDF projection and the Stage-19 closure truth are proven here.
"""
import html
import io
import json
import os
import pickle
import re
import sqlite3

import pytest

import web.app as webapp
from web.app import app, SESSION_STORE
from web import ui_text
from engine import experiment_result as er
from engine.deliverable_assembler import assemble_deliverable
from engine.record_store import ResultEventsCorrupt
from tests.csrf_client import csrf_client
from tests.test_stage19_durable_success_criteria import (
    _journey, _live_ids, _restart, _db_path, _progression_snapshot)
from tests.test_cap09_result_events import (
    _record_form, _correct_form, _post, _events, _rows, TABLE)

_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
_DOCS = os.path.join(_ROOT, "docs", "governance")

OBS = "The latch released after roughly four seconds on the bench."
FIX = "Correction: the latch released after roughly five seconds."
RETEST = "Retest on a second day: the latch released every time."

_STATE_RE = re.compile(
    r'<div class="field-value" data-execution-state="(\w+)"><strong>([^<]*)</strong> ([^<]*)</div>')
_NOTE_RE = re.compile(r'<div class="field-value" data-s11-note><em>([^<]*)</em></div>')
_OLD_NOTE = "nothing here has been built, tested"


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return csrf_client(app)


# ==========================================================================
# harness
# ==========================================================================
def _lang(c, lang):
    assert c.post("/ui-language", data={"lang": lang}).status_code in (200, 302)


def _report(c, sid, lang="en"):
    _lang(c, lang)
    r = c.get("/session/%s/deliverable" % sid)
    assert r.status_code == 200
    return html.unescape(r.get_data(as_text=True))


def _pdf_source(c, sid, monkeypatch, lang="en"):
    _lang(c, lang)
    seen = {}
    real = webapp._render_pdf_bytes

    def spy(source):
        seen["source"] = source
        return real(source)
    monkeypatch.setattr(webapp, "_render_pdf_bytes", spy)
    r = c.post("/session/%s/deliverable.pdf" % sid, data={})
    assert r.status_code == 200 and r.data[:5] == b"%PDF-"
    return html.unescape(seen["source"])


def _states(page):
    return [(s, label, body) for s, label, body in _STATE_RE.findall(page)]


def _text(key, lang):
    return ui_text.UI_STRINGS[key][lang]


# Generated substantive content: ENGLISH in every UI locale (not in the ui_text catalogue).
_NONE = webapp.S11_EXECUTION_TEXT["none"]
_UNAVAILABLE = webapp.S11_EXECUTION_TEXT["unavailable"]
_NOTE = webapp.S11_PLAN_NOTE
_ARABIC = re.compile(r"[\u0600-\u06FF]")


def _recorded(n):
    return webapp.S11_EXECUTION_TEXT["recorded"].format(n=n)


def _corrupt(sid):
    con = sqlite3.connect(_db_path())
    try:
        con.execute("PRAGMA ignore_check_constraints = ON")
        con.execute("UPDATE %s SET result_text = '  padded  ' WHERE project_id = ?" % TABLE, (sid,))
        con.commit()
    finally:
        con.close()


def _project(c):
    sid = _journey(c)
    ids = _live_ids(sid)
    assert len(ids) >= 2
    return sid, ids


# ==========================================================================
# E1. the three states and root-vs-correction counting
# ==========================================================================
def test_e01_zero_roots_reads_no_result_for_every_current_experiment(client):
    sid, ids = _project(client)
    page = _report(client, sid)
    states = _states(page)
    assert len(states) == len(ids)
    assert all(s == "none" for s, _l, _b in states)
    assert all(b == _NONE for _s, _l, b in states)
    assert webapp._experiment_execution_states(sid, assemble_deliverable(SESSION_STORE[sid]["state"])) == {
        eid: {"state": "none", "count": 0} for eid in ids}


def test_e02_one_root_reads_one_execution(client):
    sid, ids = _project(client)
    _post(client, sid, _record_form(client, sid, ids[0]), OBS)
    states = _states(_report(client, sid))
    assert states[0][0] == "recorded" and states[0][2] == _recorded(1)
    assert [s for s, _l, _b in states[1:]] == ["none"] * (len(ids) - 1)


def test_e03_corrections_never_add_an_execution(client):
    sid, ids = _project(client)
    _post(client, sid, _record_form(client, sid, ids[0]), OBS)
    [root] = _events(sid)
    _post(client, sid, _correct_form(client, sid, root.result_event_id), FIX)
    head = _events(sid)[-1]
    _post(client, sid, _correct_form(client, sid, head.result_event_id), FIX + " (again)")
    assert len(_events(sid)) == 3
    assert len(er.result_chains(_events(sid), ids[0])) == 1
    states = _states(_report(client, sid))
    assert states[0][0] == "recorded" and states[0][2] == _recorded(1)


def test_e04_independent_roots_count_as_separate_executions(client):
    sid, ids = _project(client)
    _post(client, sid, _record_form(client, sid, ids[0]), OBS)
    _post(client, sid, _record_form(client, sid, ids[0]), RETEST)
    [root, _second] = _events(sid)
    _post(client, sid, _correct_form(client, sid, root.result_event_id), FIX)
    _post(client, sid, _record_form(client, sid, ids[1]), OBS)
    states = _states(_report(client, sid))
    assert states[0][2] == _recorded(2)
    assert states[1][2] == _recorded(1)
    counts = webapp._experiment_execution_states(sid, assemble_deliverable(SESSION_STORE[sid]["state"]))
    assert counts[ids[0]] == {"state": "recorded", "count": 2}
    assert counts[ids[1]] == {"state": "recorded", "count": 1}


def test_e05_corrupt_history_reads_unavailable_never_zero(client, monkeypatch):
    sid, ids = _project(client)
    _post(client, sid, _record_form(client, sid, ids[0]), OBS)
    _corrupt(sid)
    with pytest.raises(ResultEventsCorrupt):
        webapp._get_store().load_result_events(sid)
    for lang in ("en", "ar"):
        page = _report(client, sid, lang)
        states = _states(page)
        assert len(states) == len(ids)
        assert all(s == "unavailable" for s, _l, _b in states)
        assert all(b == _UNAVAILABLE for _s, _l, b in states)
        for _s, _l, b in states:
            assert b != _NONE and "0" not in b
        source = _pdf_source(client, sid, monkeypatch, lang)
        assert _states(source) == states


def test_e06_any_read_failure_fails_closed_to_unavailable(client, monkeypatch):
    sid, ids = _project(client)

    class Broken:
        def __getattr__(self, name):
            raise RuntimeError("store unavailable")
    monkeypatch.setattr(webapp, "_get_store", lambda: Broken())
    package = assemble_deliverable(SESSION_STORE[sid]["state"])
    assert webapp._experiment_execution_states(sid, package) == {
        eid: {"state": "unavailable", "count": None} for eid in ids}
    assert webapp._experiment_execution_states(sid, {}) == {}
    assert webapp._experiment_execution_states(sid, None) == {}


def test_e07_a_missing_entry_renders_unavailable_not_absence(client, monkeypatch):
    sid, ids = _project(client)
    monkeypatch.setattr(webapp, "_experiment_execution_states", lambda _sid, _pkg: {})
    states = _states(_report(client, sid))
    assert len(states) == len(ids) and all(s == "unavailable" for s, _l, _b in states)


def test_e08_the_state_survives_memory_loss_from_durable_truth(client):
    sid, ids = _project(client)
    _post(client, sid, _record_form(client, sid, ids[0]), OBS)
    _post(client, sid, _record_form(client, sid, ids[0]), RETEST)
    _restart()
    states = _states(_report(client, sid))
    assert states[0][2] == _recorded(2)


# ==========================================================================
# E2. binding: current experiments only, by experiment_id
# ==========================================================================
def test_e10_stale_results_give_no_current_plan_state(client):
    sid, ids = _project(client)
    stale_id = "exp_retired_" + "a" * 16
    assert er.is_valid_experiment_id(stale_id) and stale_id not in ids
    store = webapp._get_store()
    event = er.recorded_root(stale_id, OBS, er.ResultContext(experiment_title="Retired"))
    store.append_result_event(sid, event, "k" * 32)
    page = _report(client, sid)
    states = _states(page)
    assert len(states) == len(ids) and all(s == "none" for s, _l, _b in states)
    assert stale_id not in page
    # the stale history is preserved by its owner, untouched
    assert [e.experiment_id for e in _events(sid)] == [stale_id]


def test_e11_rows_follow_the_current_experiment_identity_not_position(client, monkeypatch):
    sid, ids = _project(client)
    _post(client, sid, _record_form(client, sid, ids[1]), OBS)
    real = webapp.assemble_deliverable

    def reversed_plan(state):
        pkg = real(state)
        pkg["section_11_prototype_test_plan"]["items"].reverse()
        return pkg
    monkeypatch.setattr(webapp, "assemble_deliverable", reversed_plan)
    states = _states(_report(client, sid))
    order = list(reversed(ids))
    assert states[order.index(ids[1])][0] == "recorded"
    assert [s for i, (s, _l, _b) in enumerate(states) if i != order.index(ids[1])] == \
        ["none"] * (len(ids) - 1)


# ==========================================================================
# E3. truth boundaries: no disclosure, no outcome, no state effect
# ==========================================================================
def test_e20_no_result_text_context_or_identifier_reaches_the_report_or_pdf(client, monkeypatch):
    sid, ids = _project(client)
    _post(client, sid, _record_form(client, sid, ids[0]), OBS)
    [root] = _events(sid)
    _post(client, sid, _correct_form(client, sid, root.result_event_id), FIX)
    events = _events(sid)
    secrets = [OBS, FIX, "latch released"] + [e.result_event_id for e in events]
    con = sqlite3.connect(_db_path())
    try:
        # submission identities and recording times; the frozen context columns copy
        # the CURRENT plan text that Section 11 already shows, so they are guarded by
        # the absent "context at recording" label below, not by value.
        secrets += [v for row in con.execute(
            "SELECT submission_key, recorded_at FROM %s WHERE project_id = ?" % TABLE, (sid,))
            for v in row]
    finally:
        con.close()
    assert len(secrets) == 3 + 2 + 4
    for lang in ("en", "ar"):
        for page in (_report(client, sid, lang), _pdf_source(client, sid, monkeypatch, lang)):
            for secret in secrets:
                assert secret not in page, secret
            assert _text("UI_R_CONTEXT", lang) not in page
            assert _text("UI_R_LABEL", lang) not in page


def test_e21_no_outcome_criterion_comparison_or_judgement_is_rendered(client):
    sid, ids = _project(client)
    _post(client, sid, _record_form(client, sid, ids[0]), OBS)
    for lang in ("en", "ar"):
        states = _states(_report(client, sid, lang))
        assert {s for s, _l, _b in states} <= {"none", "recorded", "unavailable"}
        for _s, _l, body in states:
            for word in ("PASS", "FAIL", "PARTIAL", "INCONCLUSIVE", "passed", "failed", "succeeded",
                         "met", "satisfied", "confirmed", "rejected", "validated", "Demonstrated"):
                assert not re.search(r"(?<![\w/])%s(?![\w/])" % word, body), (lang, word, body)
    src = open(os.path.join(_ROOT, "web", "app.py"), encoding="utf-8").read()
    i = src.index("def _experiment_execution_states(")
    helper = src[i:src.index("\ndef ", i + 10)]
    helper = re.sub(r'""".*?"""', "", helper, flags=re.S)        # code only, not the docstring
    for forbidden in ("success_criterion", "result_text", "test_hypothesis", "failure_or_revision",
                      "context", "PASS", "FAIL", "readiness", "maturity", "progress", "append_",
                      "SESSION_STORE", "state."):
        assert forbidden not in helper, forbidden


def _stable(package):
    """The package as JSON without its per-call generation timestamp."""
    return json.dumps(dict(package, generated_at=None), sort_keys=True, default=str)


def test_e22_rendering_changes_no_state_result_history_or_progression(client, monkeypatch):
    sid, ids = _project(client)
    _post(client, sid, _record_form(client, sid, ids[0]), OBS)
    state = SESSION_STORE[sid]["state"]
    before_state = pickle.dumps(state)
    before_events = pickle.dumps(_events(sid))
    before_rows = _rows(sid)
    before_progress = _progression_snapshot(sid)
    before_package = _stable(assemble_deliverable(state))
    for lang in ("en", "ar"):
        _report(client, sid, lang)
        _pdf_source(client, sid, monkeypatch, lang)
    state = SESSION_STORE[sid]["state"]
    assert pickle.dumps(state) == before_state
    assert pickle.dumps(_events(sid)) == before_events
    assert _rows(sid) == before_rows
    assert _progression_snapshot(sid) == before_progress
    package = assemble_deliverable(state)
    assert _stable(package) == before_package
    # the canonical package carries no execution state and keeps its own note
    flat = json.dumps(package, default=str)
    assert "execution_state" not in flat and "recorded execution" not in flat
    assert "note" in package["section_11_prototype_test_plan"]


def test_e23_the_canonical_owners_are_untouched_by_the_closure():
    assembler = open(os.path.join(_ROOT, "engine", "deliverable_assembler.py"), encoding="utf-8").read()
    assert "experiment_result" not in assembler and "execution_state" not in assembler
    owner = open(os.path.join(_ROOT, "engine", "experiment_result.py"), encoding="utf-8").read()
    # Stage 35 first slice (implementation contract §2.3 E3): the ONE authorized later
    # addition to the Result owner is the moved execution-state derivation, appended as
    # one marked block (two constants' worth of tokens and ONE function). Everything
    # before it stays exactly as the Stage-19 closure left it.
    assert owner.count("# Stage 35 E3") == 1
    owner, e3 = owner.split("# Stage 35 E3")
    assert e3.count("\ndef ") == 1 and "def execution_states(events, experiment_ids):" in e3
    assert "execution_state" not in owner and "_EXECUTION_" not in owner


# ==========================================================================
# E4. the Section-11 note and execution states: English generated content under
#     both UI locales; localized chrome / RTL intact; HTML / PDF parity
# ==========================================================================
def test_e30_the_note_and_states_are_english_generated_content_outside_the_catalogue():
    for phrase in ("Proposed experiments synthesized from your own captured evidence",
                   "InventorAI has not itself performed, checked or validated any of these experiments",
                   "A recorded execution is your own report of what happened and has not been validated",
                   "does not create a pass/fail judgement", "does not establish feasibility"):
        assert phrase in _NOTE, phrase
    assert _OLD_NOTE not in _NOTE.lower()
    assert "{n}" in webapp.S11_EXECUTION_TEXT["recorded"]
    assert "These are your own recorded observations" in _recorded(3) and "3" in _recorded(3)
    for text in (_NOTE, *webapp.S11_EXECUTION_TEXT.values()):
        assert not _ARABIC.search(text), text
    # no Stage-19 Category-C localization exception: the generated wording is absent from the
    # catalogue; only the row label is (bilingual) interface chrome
    # Stage 35 first slice (implementation contract §12.7): the disclosure export's own
    # neutral execution-state labels are export-only ``UI_S35_*`` keys; they localize
    # nothing on the Stage-19 report / PDF surfaces, which stay English.
    catalogue = json.dumps({k: v for k, v in ui_text.UI_STRINGS.items()
                            if not k.startswith("UI_S35_")}, ensure_ascii=False)
    for text in (_NOTE, _NONE, _UNAVAILABLE, "These are your own recorded observations"):
        assert text not in catalogue, text
    assert [k for k in ui_text.UI_STRINGS if k.startswith("UI_S11_")] == ["UI_S11_EXECUTION_LABEL"]
    assert _ARABIC.search(_text("UI_S11_EXECUTION_LABEL", "ar"))
    assert "UI_CAP01_" in ui_text.__doc__ and "ONE explicit" in ui_text.__doc__


@pytest.mark.parametrize("lang", ("en", "ar"))
def test_e31_report_and_pdf_show_the_same_states_and_note(client, monkeypatch, lang):
    sid, ids = _project(client)
    _post(client, sid, _record_form(client, sid, ids[0]), OBS)
    _post(client, sid, _record_form(client, sid, ids[0]), RETEST)
    page = _report(client, sid, lang)
    source = _pdf_source(client, sid, monkeypatch, lang)
    assert _states(page) == _states(source)
    assert _NOTE_RE.findall(page) == _NOTE_RE.findall(source) == [_NOTE]
    states = _states(page)
    label = _text("UI_S11_EXECUTION_LABEL", lang)
    assert states[0] == ("recorded", label, _recorded(2))
    assert states[1] == ("none", label, _NONE)
    for surface in (page, source):
        assert _OLD_NOTE not in surface.lower()
    if lang == "ar":
        # the surrounding Arabic chrome, RTL direction and generated-output disclosure are intact
        assert 'dir="rtl"' in page and 'lang="ar"' in page
        assert _text("UI_B_DELIV_074", "ar") in page and _text("UI_B_DELIV_082", "ar") in page
        assert _text("UI_B_GENOUT_DISCLOSURE", "ar") in page
        assert _text("UI_S11_EXECUTION_LABEL", "en") not in page


def test_e33_the_substantive_content_is_identical_under_en_and_ar_selection(client, monkeypatch):
    sid, ids = _project(client)
    _post(client, sid, _record_form(client, sid, ids[0]), OBS)
    [root] = _events(sid)
    _post(client, sid, _correct_form(client, sid, root.result_event_id), FIX)
    _post(client, sid, _record_form(client, sid, ids[1]), RETEST)
    seen = {}
    for lang in ("en", "ar"):
        for kind, text in (("html", _report(client, sid, lang)), ("pdf", _pdf_source(client, sid, monkeypatch, lang))):
            seen[(lang, kind)] = ([(s, b) for s, _l, b in _states(text)], _NOTE_RE.findall(text))
    assert len(set(map(repr, seen.values()))) == 1, seen
    states, notes = seen[("en", "html")]
    assert states[:2] == [("recorded", _recorded(1)), ("recorded", _recorded(1))]
    assert notes == [_NOTE]


def test_e32_a_project_without_experiments_still_carries_the_truthful_note(client, monkeypatch):
    sid, _ids = _project(client)
    real = webapp.assemble_deliverable

    def no_experiments(state):
        pkg = real(state)
        pkg["section_11_prototype_test_plan"]["items"] = []
        return pkg
    monkeypatch.setattr(webapp, "assemble_deliverable", no_experiments)
    page = _report(client, sid)
    assert _states(page) == []
    assert _NOTE_RE.findall(page) == [_NOTE]
    assert _OLD_NOTE not in page.lower()


# ==========================================================================
# E5. Stage-19 closure truth
# ==========================================================================
_COMPLETE = "STAGE 19: COMPLETE — CURRENT PLANNING-ONLY SCOPE"
# The later Owner-authorized Stage 20, 21 and 22 closures moved the marker on to Stage 23 (navigation only); the Stage-19
# completion and the "no Stage-20 implementation by the Stage-19 closure" fact stay true history.
# The later Owner-authorized Stage 23 closure (no product change) moved the marker on to Stage 24 (navigation only);
# the later delivered CAP-12 Form Mock-up Advisory Slice 1 entered Stage 24 as ENTERED / PARTIAL (marker unchanged);
# the later Owner-authorized Stage 24 closure (no product change) completed Stage 24 for its bounded CAP-12 Form Mock-up
# Advisory Slice 1 scope only and moved the marker on to Stage 25 (NOT ENTERED, navigation only).
_MARKER = "MASTER ROADMAP SEQUENTIAL MARKER: STAGE 25 — NOT ENTERED — NAVIGATION ONLY"
_NO_S20 = "NO STAGE-20 IMPLEMENTATION AUTHORIZED BY STAGE-19 CLOSURE"


def _doc(name):
    with io.open(os.path.join(_DOCS, name), encoding="utf-8") as fh:
        return re.sub(r"\s+", " ", fh.read())


def test_e40_the_closure_truth_is_recorded_on_every_current_surface():
    surfaces = {"CLAUDE.md": re.sub(r"\s+", " ", io.open(os.path.join(_ROOT, "CLAUDE.md"),
                                                          encoding="utf-8").read())}
    for name in ("ACTIVE_INCREMENT_CONTRACT.md", "CURRENT_PROJECT_STATE.md",
                 "INVENTORAI_MASTER_EXECUTION_ROADMAP.md",
                 "INVENTORAI_MASTER_ROADMAP_EXECUTION_CHECKLIST.md",
                 "INVENTORAI_CAPABILITY_ENRICHMENT_REGISTER.md"):
        surfaces[name] = _doc(name)
    for name, text in surfaces.items():
        assert _COMPLETE in text, name
        assert _MARKER in text, name
    for name in ("ACTIVE_INCREMENT_CONTRACT.md", "INVENTORAI_MASTER_EXECUTION_ROADMAP.md",
                 "INVENTORAI_MASTER_ROADMAP_EXECUTION_CHECKLIST.md", "INVENTORAI_CAPABILITY_ENRICHMENT_REGISTER.md"):
        assert _NO_S20 in surfaces[name], name
    # ROTATED at the Stage 35 first bounded slice: the live CLAUDE.md declaration was the Stage-35 increment
    # ROTATED back at the Stage 35 closure: the live CLAUDE.md declaration is NONE again and the Stage-35 increment is
    # no longer live
    assert "**ACTIVE CONTRACT: NONE.**" in surfaces["CLAUDE.md"]
    assert "**ACTIVE CONTRACT: STAGE 35 — FIRST BOUNDED STRUCTURED INVENTION DISCLOSURE EXPORT SLICE.**" not in surfaces["CLAUDE.md"]
    assert "Execution-State Disclosure" not in _doc("OWNER_DECISION_REGISTER.md")


def test_e41_only_stage_19_is_ticked_and_the_limits_are_preserved():
    roadmap = io.open(os.path.join(_DOCS, "INVENTORAI_MASTER_EXECUTION_ROADMAP.md"), encoding="utf-8").read()
    assert re.search(r"^- \[x\] \*\*19 — WS-PFV-001/CAP-09:\*\*", roadmap, re.M)
    # Stage 20 was ticked later by its own Owner-authorized closure (Owner-declared assumption scope), not by this one
    # Stages 20, 21 and 22 were ticked later by their own Owner-authorized closures, not by this one
    for stage in (15, 18, 20, 21, 22):
        assert re.search(r"^- \[x\] \*\*%d — " % stage, roadmap, re.M), stage
    # Stage 23 was ticked later by its own Owner-authorized closure (bounded four-axis scope, no product change)
    assert re.search(r"^- \[x\] \*\*23 — ", roadmap, re.M)
    # Stage 24 was ticked later by its own Owner-authorized closure (bounded CAP-12 Form Mock-up Advisory Slice 1 scope
    # only, no product change); Stage 25 stays NOT ENTERED and unticked
    assert re.search(r"^- \[x\] \*\*24 — ", roadmap, re.M)
    # Stage 16 was ticked later by its own Owner-authorized closure (bounded Technical + Integration
    # evidence-sufficiency composition scope only), not by this one; Stages 13 and 14 stay PARTIAL / DEFERRED
    assert re.search(r"^- \[x\] \*\*16 — ", roadmap, re.M)
    for stage in (11, 13, 14, 17, 25):
        assert re.search(r"^- \[ \] \*\*%d — " % stage, roadmap, re.M), stage
    flat = re.sub(r"\s+", " ", roadmap)
    for limit in ("FULL CAP-09: NOT AUTHORIZED", "FULL WS-PFV-001: NOT AUTHORIZED",
                  "FORMAL EXPERIMENTAL VARIABLE MODEL: NOT AUTHORIZED",
                  "RESULT OUTCOME / PASS-FAIL JUDGEMENT: NOT AUTHORIZED"):
        assert limit in flat, limit
