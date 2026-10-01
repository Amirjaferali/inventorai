"""Stage 21 — Owner-Declared Contradiction Visibility — Closure.

The session page carries ONE read-only view of the contradictions the inventor
declared (CAP-10): every ACTIVE pair with both answers shown from their own
records (step, question area, verbatim text) and the declaration's verbatim
note, a link to the EXISTING correction form, and a count of declarations that
are no longer active. The project record marks such historical declarations
"No longer active". The Compass and the Decision Room link to the view.

Read-only: no write path, no persistence, no replay change; nothing is
detected, validated, resolved or chosen. Neutral synthetic fixtures only.
"""
import html as _html
import io
import os
import re

import pytest

import engine.session_reconstruction as SR
from engine.idea_state import (
    DISPOSITION_CONTRADICTION_DECLARED, IdeaState, active_declared_contradiction_pairs,
)
from web import ui_text
import web.app as appmod
from tests.test_safe_question_routing_pf_q2 import (  # noqa: F401  (fixture)
    client, MECH, _live, _store,
)
from tests.test_cap10_declared_contradiction import (
    _declare, _raw, _token, _web_project,
)
from tests.test_stage19_durable_success_criteria import _restart
from tests.test_r05_request_integrity import MUTATIONS

NOTE = "The latch <must> stay tool-free & spring-loaded."
FORBIDDEN = ("resolved", "is verified", "validated.", "is correct", "wins",
             "winner is", "detected")
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DOCS = os.path.join(_ROOT, "docs", "governance")


def _view_html(c, sid):
    raw = _raw(c, sid)
    m = re.search(r'<section class="declared-conflicts".*?</section>', raw, re.S)
    return m.group(0) if m else None


def _pairs_shown(fragment):
    return re.findall(r'data-declared-conflict="([^"]+)"', fragment or "")


def _correct(c, sid, target, text):
    return c.post(f"/session/{sid}/correct", data={
        "answer_token": _token(c, sid), "supersedes_record_id": target,
        "response": text})


def _record_by_id(sid, rid):
    return next(r for r in _live(sid).assertions if r.record_id == rid)


def _step_of(sid, rid):
    return [r.record_id for r in _live(sid).assertions].index(rid) + 1


# ==========================================================================
# 1-3. active pairs: both answers, note, multiple pairs, active vs inactive
# ==========================================================================
def test_01_active_declaration_shows_both_answers_and_the_note(client):
    sid, answered = _web_project(client)
    lo, hi = answered[0], answered[-1]
    _declare(client, sid, [hi, lo], note=NOTE)
    view = _view_html(client, sid)
    assert view is not None
    assert _pairs_shown(view) == ["%s|%s" % (lo, hi)]
    text = _html.unescape(view)
    for rid in (lo, hi):
        rec = _record_by_id(sid, rid)
        item = re.search(r'<li data-conflict-answer="%s">.*?</li>' % rid, view, re.S).group(0)
        assert "%s %d" % (ui_text.text("UI_S21_STEP", "en"), _step_of(sid, rid)) in item
        assert rec.content in _html.unescape(item)                # full verbatim text
        assert 'dir="auto"' in item and "<bdi" in item
    assert NOTE in text
    assert ui_text.text("UI_S21_NOTE", "en") in text
    # the derivation is CAP-10's own active-pair truth
    assert _pairs_shown(view) == ["%s|%s" % p for p in sorted(
        active_declared_contradiction_pairs(_live(sid).assertions))]


def test_02_multiple_active_declarations_stay_correctly_paired(client):
    sid, answered = _web_project(client)
    a, b, c_, d = answered[:4]
    _declare(client, sid, [a, d], note="first pair")
    _declare(client, sid, [b, c_], note="")
    view = _view_html(client, sid)
    assert _pairs_shown(view) == ["%s|%s" % (a, d), "%s|%s" % (b, c_)]
    blocks = re.findall(r'<div class="declared-conflict".*?</div>', view, re.S)
    assert len(blocks) == 2
    first, second = blocks
    assert re.findall(r'data-conflict-answer="([^"]+)"', first) == [a, d]
    assert re.findall(r'data-conflict-answer="([^"]+)"', second) == [b, c_]
    assert "first pair" in first and "data-conflict-note" not in second   # empty note not shown


def test_03_04_correction_moves_a_pair_to_history_and_marks_the_record(client):
    sid, answered = _web_project(client)
    lo, hi = answered[0], answered[-1]
    mid = answered[1]
    _declare(client, sid, [lo, hi], note=NOTE)
    _declare(client, sid, [mid, answered[2]], note="")
    decl_ids = [r.record_id for r in _live(sid).assertions
                if r.disposition == DISPOSITION_CONTRADICTION_DECLARED]
    raw = _raw(client, sid)
    assert raw.count("data-record-conflict-inactive") == 0
    assert "data-declared-conflicts-inactive" not in _view_html(client, sid)
    # ordinary correction through the EXISTING owner
    assert _correct(client, sid, lo, MECH + " The frame rail is steel.").status_code == 302
    view = _view_html(client, sid)
    assert _pairs_shown(view) == ["%s|%s" % (mid, answered[2])]   # the other pair stays active
    assert 'data-declared-conflicts-inactive="1"' in view
    raw = _raw(client, sid)
    assert raw.count("data-record-conflict-inactive") == 1    # only the inactive one
    marker = ui_text.text("UI_T3A_CONFLICT_INACTIVE", "en")
    assert marker == ("No longer active: one of its two answers was later replaced. "
                      "Kept as history.")
    assert marker in _html.unescape(raw)
    ctx = appmod._project_record_context(_live(sid), sid)
    flagged = [e["record_id"] for e in ctx["entries"] if e["conflict_inactive"]]
    assert flagged == [decl_ids[0]]
    # every declaration stays as history; nothing was resolved or rewritten
    assert [r.record_id for r in _live(sid).assertions
            if r.disposition == DISPOSITION_CONTRADICTION_DECLARED] == decl_ids


def test_03b_only_history_left_is_never_shown_as_none(client):
    sid, answered = _web_project(client)
    _declare(client, sid, [answered[0], answered[-1]], note="")
    _correct(client, sid, answered[0], MECH + " Rail clarified.")
    view = _view_html(client, sid)
    assert view is not None and _pairs_shown(view) == []
    assert 'data-declared-conflicts-inactive="1"' in view
    assert "data-pc-conflicts-link" not in _raw(client, sid)       # nothing active to link


# ==========================================================================
# 5. live / cold / resumed parity
# ==========================================================================
def test_05_live_cold_and_resumed_views_agree(client):
    sid, answered = _web_project(client)
    _declare(client, sid, [answered[0], answered[-1]], note=NOTE)
    _declare(client, sid, [answered[1], answered[2]], note="")
    _correct(client, sid, answered[1], MECH + " Clarified.")
    live = appmod._declared_conflict_view(_live(sid))
    cold = appmod._declared_conflict_view(SR.reconstruct_readonly_state(_store(), sid).state)
    assert live == cold and live["status"] == appmod.DECLARED_CONFLICTS_AVAILABLE
    live_pairs = _pairs_shown(_view_html(client, sid))
    live_markers = _raw(client, sid).count("data-record-conflict-inactive")
    assert live_pairs and live_markers == 1
    _restart()
    cold_raw = client.get(f"/session/{sid}").get_data(as_text=True)
    # the cold read-only page keeps the project record and its history marker;
    # the active view (like the CAP-08 view and the correction form it links
    # to) belongs to the writable page, and no link points at a missing view
    assert cold_raw.count("data-record-conflict-inactive") == live_markers
    if 'id="declared-conflicts"' not in cold_raw:
        assert 'href="#declared-conflicts"' not in cold_raw
    assert client.post(f"/session/{sid}/resume", data={}).status_code == 302
    assert _pairs_shown(_view_html(client, sid)) == live_pairs
    assert _raw(client, sid).count("data-record-conflict-inactive") == live_markers
    assert appmod._declared_conflict_view(_live(sid)) == live


# ==========================================================================
# 6. failure truth
# ==========================================================================
def test_06_derivation_failure_renders_unavailable_not_empty(client, monkeypatch):
    sid, answered = _web_project(client)
    _declare(client, sid, [answered[0], answered[-1]], note="")

    def boom(*_a, **_k):
        raise RuntimeError("derivation unavailable")
    monkeypatch.setattr("engine.idea_state.active_declared_contradiction_pairs", boom)
    view = appmod._declared_conflict_view(_live(sid))
    assert view["status"] == appmod.DECLARED_CONFLICTS_UNAVAILABLE
    assert view["conflicts"] == [] and view["declared_count"] is None
    raw = _raw(client, sid)
    section = _view_html(client, sid)
    assert 'data-declared-conflicts-status="unavailable"' in section
    assert "data-declared-conflicts-unavailable" in section
    assert ui_text.text("UI_S21_UNAVAILABLE", "en") in _html.unescape(section)
    assert _pairs_shown(section) == [] and "data-declared-conflicts-inactive" not in section
    assert "data-pc-conflicts-link" not in raw


def test_06b_a_missing_active_endpoint_fails_closed(monkeypatch):
    state = IdeaState(idea_id="x")
    state.record_interaction("answered", content="a", gap_context="MECHANISM_COMPLETENESS")
    state.record_interaction("answered", content="b", gap_context="MECHANISM_COMPLETENESS")
    state.record_contradiction_declaration("rec_1", "rec_2")
    monkeypatch.setattr("engine.idea_state.active_declared_contradiction_pairs",
                        lambda _a: frozenset({("rec_1", "rec_7")}))
    for r in state.assertions:
        if r.disposition == DISPOSITION_CONTRADICTION_DECLARED:
            r.contradiction_endpoints = ["rec_1", "rec_7"]
    assert appmod._declared_conflict_view(state)["status"] == \
        appmod.DECLARED_CONFLICTS_UNAVAILABLE


# ==========================================================================
# 7. legacy / non-declared contradiction links are never attributed
# ==========================================================================
def test_07_a_legacy_contradiction_edge_is_not_shown_as_declared(client):
    sid, answered = _web_project(client)
    state = _live(sid)
    state.mark_contradiction(answered[0], answered[1])         # no declaration record
    assert appmod._declared_conflict_view(state)["declared_count"] == 0
    assert _view_html(client, sid) is None
    assert "data-pc-conflicts-link" not in _raw(client, sid)


# ==========================================================================
# 8-10. EN / AR chrome, verbatim inventor text, truthful copy
# ==========================================================================
@pytest.mark.parametrize("lang", ("en", "ar"))
def test_08_09_localized_chrome_and_verbatim_text(client, lang):
    sid, answered = _web_project(client)
    _declare(client, sid, [answered[0], answered[-1]], note=NOTE)
    client.post("/ui-language", data={"lang": lang})
    view = _view_html(client, sid)
    text = _html.unescape(view)
    for key in ("UI_S21_HEADING", "UI_S21_NOTE", "UI_S21_STEP", "UI_S21_NOTE_LABEL",
                "UI_S21_CORRECT_INTRO"):
        assert ui_text.text(key, lang) in text, key
    assert "&lt;must&gt;" in view and "&amp; spring" in view   # escaped, never raw markup
    assert NOTE in text                                          # verbatim after unescape
    assert ui_text.text("UI_S21_COMPASS_LINK", lang) in _html.unescape(_raw(client, sid))
    for key in [k for k in ui_text.UI_STRINGS if k.startswith("UI_S21_")] + [
            "UI_T3A_CONFLICT_INACTIVE"]:
        assert ui_text.UI_STRINGS[key]["en"], key
        assert re.search(r"[؀-ۿ]", ui_text.UI_STRINGS[key]["ar"]), key


def test_10_copy_claims_no_resolution_validation_or_winner():
    for key in [k for k in ui_text.UI_STRINGS if k.startswith("UI_S21_")] + [
            "UI_T3A_CONFLICT_INACTIVE"]:
        low = ui_text.UI_STRINGS[key]["en"].lower()
        for bad in FORBIDDEN:
            assert bad not in low, (key, bad)
    note = ui_text.text("UI_S21_NOTE", "en")
    for needle in ("You declared", "have not been validated",
                   "neither answer is assumed correct",
                   "does not choose which answer is right"):
        assert needle in note, needle


# ==========================================================================
# 11-12. Decision Room and Compass links; correction path only when writable
# ==========================================================================
def test_11_decision_room_context_links_to_the_view(client):
    sid, answered = _web_project(client)
    _declare(client, sid, [answered[0], answered[-1]], note="")
    client.post(f"/session/{sid}/decision/declare-context",
                data={"content": "Which latch should the ramp use?",
                      "answer_token": _token(client, sid)})
    raw = _raw(client, sid)
    panel = re.search(r'id="decision-project-context".*?</section>', raw, re.S).group(0)
    row = re.search(r'<li class="dt-ctx-row" data-dt-category="declared_contradictions".*?</li>',
                    panel, re.S).group(0)
    assert 'href="#declared-conflicts"' in row
    assert 'href="#t3a-project-record"' not in row
    assert 'id="declared-conflicts"' in raw                     # the link target exists


def test_12_compass_links_to_the_view_and_ranking_is_unchanged(client):
    sid, answered = _web_project(client)
    _declare(client, sid, [answered[0], answered[-1]], note="")
    raw = _raw(client, sid)
    compass = re.search(r'data-pc-row="unresolved".*?data-pc-row="why"', raw, re.S).group(0)
    assert 'href="#declared-conflicts"' in compass and "data-pc-conflicts-link" in compass
    # the next-step derivation and its top ranking are untouched
    why = re.search(r'id="next-development-step".*?</div>', raw, re.S).group(0)
    assert "Two recorded answers you marked as conflicting" in _html.unescape(why)


def test_12b_correction_link_only_on_a_writable_page(client):
    sid, answered = _web_project(client)
    _declare(client, sid, [answered[0], answered[-1]], note="")
    view = _view_html(client, sid)
    assert 'href="#correct-answer"' in view and 'id="correct-answer"' in _raw(client, sid)
    _restart()
    cold_raw = client.get(f"/session/{sid}").get_data(as_text=True)
    assert 'id="correct-answer"' not in cold_raw               # read-only: no correction form
    assert 'href="#correct-answer"' not in (_view_html(client, sid) or "")


# ==========================================================================
# 13. no new write path; nothing persisted or mutated by a render
# ==========================================================================
def test_13_no_new_mutation_route_and_render_is_read_only(client):
    assert not [r for r in appmod.app.url_map.iter_rules()
                if "conflict" in r.rule and r.rule != "/session/<sid>/declare-conflict"]
    assert "/session/<sid>/declare-conflict" in MUTATIONS
    assert not [m for m in MUTATIONS if "declared-conflicts" in m]
    sid, answered = _web_project(client)
    _declare(client, sid, [answered[0], answered[-1]], note="")
    before = [(r.record_id, r.disposition, r.superseded_by) for r in _live(sid).assertions]
    rows = len(list(_store().load_contract(sid).assertions))
    for _ in range(2):
        _raw(client, sid)
    assert [(r.record_id, r.disposition, r.superseded_by)
            for r in _live(sid).assertions] == before
    assert len(list(_store().load_contract(sid).assertions)) == rows


# ==========================================================================
# Stage-21 closure truth
# ==========================================================================
_COMPLETE = "STAGE 21: COMPLETE — CURRENT OWNER-DECLARED CONTRADICTION SCOPE"
_DELIVERED = "STAGE 21 CLOSURE: DELIVERED"
# The later Owner-authorized Stage 22 closure moved the marker on to Stage 23 (navigation only); the Stage-21
# completion and the "no Stage-22 implementation by the Stage-21 closure" fact stay true history.
_MARKER = "MASTER ROADMAP SEQUENTIAL MARKER: STAGE 23 — NOT ENTERED — NAVIGATION ONLY"
_NO_S22 = "NO STAGE-22 IMPLEMENTATION AUTHORIZED BY STAGE-21 CLOSURE"
_LIMITS = ("FULL CAP-10: NOT AUTHORIZED",
           "AUTOMATIC / AI CONTRADICTION DETECTION: NOT AUTHORIZED",
           "SYSTEM_INFERRED CONTRADICTION WRITER: NOT AUTHORIZED")


def _doc(name):
    with io.open(os.path.join(_DOCS, name), encoding="utf-8") as fh:
        return re.sub(r"\s+", " ", fh.read())


def test_14_closure_truth_on_every_current_surface():
    surfaces = {"CLAUDE.md": re.sub(r"\s+", " ", io.open(os.path.join(_ROOT, "CLAUDE.md"),
                                                          encoding="utf-8").read())}
    for name in ("ACTIVE_INCREMENT_CONTRACT.md", "CURRENT_PROJECT_STATE.md",
                 "INVENTORAI_MASTER_EXECUTION_ROADMAP.md",
                 "INVENTORAI_MASTER_ROADMAP_EXECUTION_CHECKLIST.md",
                 "INVENTORAI_CAPABILITY_ENRICHMENT_REGISTER.md"):
        surfaces[name] = _doc(name)
    for name, text in surfaces.items():
        for token in (_COMPLETE, _MARKER) + _LIMITS:
            assert token in text, (name, token)
    for name in ("ACTIVE_INCREMENT_CONTRACT.md", "INVENTORAI_MASTER_EXECUTION_ROADMAP.md",
                 "INVENTORAI_MASTER_ROADMAP_EXECUTION_CHECKLIST.md", "INVENTORAI_CAPABILITY_ENRICHMENT_REGISTER.md"):
        assert _NO_S22 in surfaces[name], name
    for name in ("ACTIVE_INCREMENT_CONTRACT.md", "CURRENT_PROJECT_STATE.md"):
        assert _DELIVERED in surfaces[name], name
    # the later Stage 22 closure took over the CLAUDE.md head; the Stage-21 delivery stays recorded there as history
    assert ("Stage 21 closure (delivered; completes Stage 21 for the current Owner-declared contradiction scope"
            in surfaces["CLAUDE.md"])
    assert "**ACTIVE CONTRACT: NONE.**" in surfaces["CLAUDE.md"]
    assert "Owner-Declared Contradiction Visibility" not in _doc("OWNER_DECISION_REGISTER.md")


def test_15_only_stage_21_is_newly_ticked():
    roadmap = io.open(os.path.join(_DOCS, "INVENTORAI_MASTER_EXECUTION_ROADMAP.md"),
                      encoding="utf-8").read()
    # Stage 22 was ticked later by its own Owner-authorized closure (no product change), not by this one
    for stage in (15, 18, 19, 20, 21, 22):
        assert re.search(r"^- \[x\] \*\*%d — " % stage, roadmap, re.M), stage
    for stage in (11, 13, 14, 16, 17, 23):
        assert re.search(r"^- \[ \] \*\*%d — " % stage, roadmap, re.M), stage
