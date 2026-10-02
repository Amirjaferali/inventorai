"""Stage 30 — Control-Loop Part-Enablement Safeguards — Bounded Slice 1.

Three safeguards before any later Owner decision on OPTIONAL-PART enablement (the shipped ``_PART_ONLY_DOMAINS``
stays EMPTY; ``control_loop`` stays NOT part-enabled and NOT root-activated; the three-part paths run only through
the test-only eligibility double):

  * WITHDRAWAL READABILITY — if part eligibility is later withdrawn, the inventor can still READ the answers they
    saved about an existing control-loop part (read-only); record / edit / clear stay refused, and no new part can
    be created. Nothing durable is deleted, migrated or remapped.
  * SAFETY INPUT-SCOPE DISCLOSURE — the part page and the report / PDF safety block say plainly that optional-part
    answers are not read for inventor-stated Safety Signals; detection itself is unchanged.
  * ISOLATION PINS — part answers never become SafetySignal input: the same root inputs give the same signals,
    hazard-like text that exists only in a part answer changes nothing under a Mechanical or an Electronics root,
    and ``engine/safety_signal.py`` holds no part-answer read path.
"""
import ast
import html as _html
import os
import re

import pytest

import web.app as appmod
from engine import domain_activation
from engine import subsystem_model as sm
from engine.deliverable_assembler import assemble_deliverable
from engine.idea_state import IdeaState
from engine.safety_signal import derive_inventor_stated_safety_signals
from tests.test_stage15_integrated_invention_entry import (
    ELEC, MECH, TIE_IDEA, _compose, _created, _live, _pair, _pdf_source)
from tests.test_stage28_control_loop_optional_part_slice1 import (  # noqa: F401  (fixtures)
    CL, CTRL, _three_part_project, client, part_eligible)
from tests.test_stage28_control_loop_optional_part_slice2 import (
    B1, Q1, Q2, _all_current_ids, _answers_rows, _ctrl_id, _form, _page, _save)
from web import ui_text

_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
# Hazard-like statements each governed root family really detects (same-sentence failure + subject + consequence).
MECH_HAZARD = "If the guard comes loose, fingers could be caught in the rotating parts and crushed."
ELEC_HAZARD = "If protection fails, the high voltage could cause a fire."
HAZARD = {MECH: MECH_HAZARD, ELEC: ELEC_HAZARD}


def _withdraw(monkeypatch):
    """The SHIPPED state: the part-only allowlist is empty again."""
    monkeypatch.setattr(domain_activation, "_PART_ONLY_DOMAINS", frozenset())
    assert domain_activation.is_part_eligible(CL) is False


def _text(resp):
    return _html.unescape(resp.get_data(as_text=True))


def _safety_block(state):
    return assemble_deliverable(state)["_session_meta"]["inventor_stated_safety_signals"]


def _root_state(domain, text, with_optional_part):
    st = IdeaState(idea_id="s30-safety")
    st.domain = domain
    st.domain_signal = domain
    st.idea_summary = text
    if with_optional_part:
        mech, elec = _pair()
        st.subsystems = [mech, elec, sm.declared_subsystem(CL, "Loop logic", "Keeps the level")]
    return st


# ==========================================================================
# A. Withdrawal readability: saved answers stay readable, read-only
# ==========================================================================
def test_saved_answers_stay_readable_read_only_after_withdrawal(client, part_eligible, monkeypatch):
    sid = _three_part_project(client)
    ctrl = _ctrl_id(sid)
    _save(client, sid, {Q1: "Room temperature", B1: "It does not heat water"})
    rows = _answers_rows(sid)
    subsystems = _rows_of("SELECT subsystem_id, domain FROM project_subsystems WHERE project_id = ? "
                          "ORDER BY subsystem_seq", sid)
    _withdraw(monkeypatch)
    r = _page(client, sid)
    raw = _text(r)
    assert r.status_code == 200
    assert ui_text.text("UI_PQ_READ_ONLY", "en") in raw and ui_text.text("UI_PQ_INTRO_READ_ONLY", "en") in raw
    assert "Room temperature" in raw and "It does not heat water" in raw
    assert "<form" not in raw.split("data-pq-part", 1)[1] and "part_answer__" not in raw
    # presence stays truthful: two recorded, the rest not recorded
    assert raw.count(ui_text.text("UI_PQ_RECORDED", "en")) == 2
    assert raw.count(ui_text.text("UI_PQ_NOT_RECORDED", "en")) == len(_all_current_ids()) - 2
    # nothing durable changed by reading
    assert _answers_rows(sid) == rows and rows[0][0] == ctrl
    assert _rows_of("SELECT subsystem_id, domain FROM project_subsystems WHERE project_id = ? "
                    "ORDER BY subsystem_seq", sid) == subsystems
    # the session scope keeps the part and links to the read-only view
    session = _text(client.get("/session/%s" % sid))
    assert 'data-scope-part="control"' in client.get("/session/%s" % sid).get_data(as_text=True)
    assert ui_text.text("UI_PQ_LINK_READ_ONLY", "en") in session
    assert ui_text.text("UI_PQ_LINK", "en") not in session


@pytest.mark.parametrize("change", [{Q1: "Water level"}, {Q2: "20 C"}, {B1: ""}])
def test_writes_are_refused_after_withdrawal(client, part_eligible, monkeypatch, change):
    sid = _three_part_project(client)
    _save(client, sid, {Q1: "Room temperature", B1: "It does not heat water"})
    form = _form(client, sid)                  # a form rendered while recording was still offered
    before = _answers_rows(sid)
    _withdraw(monkeypatch)
    data = dict(form)
    for qid, text in change.items():
        data["part_answer__" + qid] = text
    r = client.post("/session/%s/part-questions" % sid, data=data)
    raw = _text(r)
    assert r.status_code == 409
    assert ui_text.text("UI_PQ_MSG_READ_ONLY", "en") in raw
    assert "Room temperature" in raw and "part_answer__" not in raw      # saved answers shown, read-only
    assert _answers_rows(sid) == before                                  # record / edit / clear: nothing written


def test_no_new_control_loop_part_can_be_created_after_withdrawal(client, part_eligible, monkeypatch):
    _withdraw(monkeypatch)
    page = client.post("/start", data={"idea": TIE_IDEA, "integrated_invention": "yes"}).get_data(as_text=True)
    assert "ctrl_part_name" not in page                                  # no optional slot offered
    sid = _created(_compose(client, TIE_IDEA, focus=MECH, **CTRL))      # posted optional values are ignored
    assert [s.domain for s in _live(sid).subsystems] == [MECH, ELEC]
    assert _page(client, sid).status_code == 404


def test_withdrawal_manufactures_no_answers_or_presence(client, part_eligible, monkeypatch):
    sid = _three_part_project(client)
    _withdraw(monkeypatch)
    raw = _text(_page(client, sid))
    assert ui_text.text("UI_PQ_READ_ONLY", "en") in raw
    assert raw.count(ui_text.text("UI_PQ_FAMILY_NONE", "en")) == 2
    assert ui_text.text("UI_PQ_RECORDED", "en") not in raw and "data-pq-answer" not in raw
    assert _answers_rows(sid) == []


def test_eligible_state_keeps_the_editable_page(client, part_eligible):
    sid = _three_part_project(client)
    raw = _text(_page(client, sid))
    assert ui_text.text("UI_PQ_READ_ONLY", "en") not in raw
    assert raw.count('name="part_answer__') == len(_all_current_ids())
    r = _save(client, sid, {Q1: "Room temperature"})
    assert r.status_code == 200 and ui_text.text("UI_PQ_MSG_SAVED", "en") in _text(r)
    assert ui_text.text("UI_PQ_LINK", "en") in _text(client.get("/session/%s" % sid))


def test_two_part_projects_still_get_no_part_page_either_way(client, part_eligible, monkeypatch):
    sid = _created(_compose(client, TIE_IDEA, focus=ELEC))
    assert _page(client, sid).status_code == 404
    _withdraw(monkeypatch)
    assert _page(client, sid).status_code == 404
    assert "data-scope-part-questions" not in client.get("/session/%s" % sid).get_data(as_text=True)


def test_root_activation_and_the_shipped_allowlist_are_unchanged():
    assert domain_activation._PART_ONLY_DOMAINS == frozenset()
    assert domain_activation._ACTIVATED_DOMAINS == frozenset({"electronics_electrical", "mechanical"})
    assert domain_activation.is_part_eligible(CL) is False
    assert domain_activation.is_activated(CL) is False


# ==========================================================================
# B. Safety input-scope disclosure (part page + report / PDF)
# ==========================================================================
def test_part_page_discloses_the_safety_input_scope_editable_and_read_only(client, part_eligible, monkeypatch):
    sid = _three_part_project(client)
    assert ui_text.text("UI_PQ_SAFETY_SCOPE", "en") in _text(_page(client, sid))
    _withdraw(monkeypatch)
    assert ui_text.text("UI_PQ_SAFETY_SCOPE", "en") in _text(_page(client, sid))
    assert client.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    try:
        raw = _text(_page(client, sid))
    finally:
        client.post("/ui-language", data={"lang": "en"})
    for key in ("UI_PQ_SAFETY_SCOPE", "UI_PQ_READ_ONLY", "UI_PQ_INTRO_READ_ONLY"):
        assert ui_text.text(key, "ar") in raw, key


def test_report_and_pdf_disclose_the_scope_only_for_projects_with_an_optional_part(client, part_eligible,
                                                                                   monkeypatch):
    three = _three_part_project(client)
    two = _created(_compose(client, TIE_IDEA, focus=MECH))
    note = ui_text.text("UI_SS_OPTIONAL_PART_SCOPE", "en")
    report3 = _text(client.get("/session/%s/deliverable" % three))
    assert note in report3
    assert note in _html.unescape(_pdf_source(client, three, monkeypatch))
    assert note not in _text(client.get("/session/%s/deliverable" % two))
    assert "root_analysis_only_optional_part_excluded" not in client.get(
        "/account/projects/%s/export" % two).get_data(as_text=True)


def test_every_new_copy_key_has_english_and_arabic():
    for key in ("UI_PQ_INTRO_READ_ONLY", "UI_PQ_READ_ONLY", "UI_PQ_LINK_READ_ONLY", "UI_PQ_SAFETY_SCOPE",
                "UI_PQ_MSG_READ_ONLY", "UI_SS_OPTIONAL_PART_SCOPE"):
        assert ui_text.has_string(key), key
    assert ui_text.localize_message(appmod.PQ_READ_ONLY_MESSAGE, "ar") == ui_text.text("UI_PQ_MSG_READ_ONLY", "ar")
    assert ui_text.text("UI_PQ_MSG_READ_ONLY", "en") == appmod.PQ_READ_ONLY_MESSAGE


# ==========================================================================
# C. Isolation pins: part answers are never SafetySignal input
# ==========================================================================
@pytest.mark.parametrize("root", [MECH, ELEC])
def test_part_only_hazard_text_never_changes_root_signals(client, part_eligible, root):
    sid = _three_part_project(client, focus=root)
    before_signals = derive_inventor_stated_safety_signals(_live(sid))
    before_block = _safety_block(_live(sid))
    _save(client, sid, {qid: HAZARD[root] for qid in _all_current_ids()})
    assert {t for _s, _q, t in _answers_rows(sid)} == {HAZARD[root]}
    assert derive_inventor_stated_safety_signals(_live(sid)) == before_signals
    assert _safety_block(_live(sid)) == before_block
    report = _text(client.get("/session/%s/deliverable" % sid))
    assert HAZARD[root] not in report
    assert ui_text.text("UI_SS_OPTIONAL_PART_SCOPE", "en") in report


@pytest.mark.parametrize("root", [MECH, ELEC])
def test_root_source_detection_is_unchanged_with_or_without_an_optional_part(root):
    plain = _root_state(root, HAZARD[root], with_optional_part=False)
    composed = _root_state(root, HAZARD[root], with_optional_part=True)
    signals = derive_inventor_stated_safety_signals(plain)
    assert len(signals) == 1 and signals[0].domain_context == root
    assert derive_inventor_stated_safety_signals(composed) == signals
    block_plain, block_composed = _safety_block(plain), _safety_block(composed)
    assert "input_scope" not in block_plain                       # every other project: block unchanged
    assert block_composed.pop("input_scope") == "root_analysis_only_optional_part_excluded"
    assert block_composed == block_plain                           # the marker is the ONLY difference


def test_safety_signal_owner_holds_no_part_answer_read_path():
    path = os.path.join(_ROOT, "engine", "safety_signal.py")
    with open(path, encoding="utf-8") as fh:
        source = fh.read()
    tree = ast.parse(source)
    imported = ({n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)}
                | {a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names})
    assert imported <= {"re", "unicodedata", "dataclasses", "typing"}, imported
    for needle in ("PartAnswer", "subsystem_part_answers", "load_part_answers", "apply_part_answer_delta",
                   "part_answer", "subsystem_model", "record_store", "subsystems"):
        assert needle not in source, needle
    # the inventor texts read are exactly the root-analysis inputs
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "_inventor_texts")
    attrs = {c.args[1].value for c in ast.walk(fn)
             if isinstance(c, ast.Call) and getattr(c.func, "id", None) == "getattr"
             and isinstance(c.args[1], ast.Constant) and isinstance(c.args[0], ast.Name)
             and c.args[0].id == "state"}
    assert attrs == {"idea_summary", "assertions", "acknowledged_unknowns"}, attrs
    assert '("known_problem", "known_mechanism")' in ast.get_source_segment(source, fn)


def test_state_never_carries_part_answers(client, part_eligible):
    sid = _three_part_project(client)
    _save(client, sid, {Q1: MECH_HAZARD})
    state = _live(sid)
    for name in vars(state):
        assert "part_answer" not in name, name
    assert all(not isinstance(v, sm.PartAnswer) for v in vars(state).values())


def _rows_of(sql, sid):
    import sqlite3
    conn = sqlite3.connect(os.environ["INVENTORAI_DB_PATH"])
    try:
        return conn.execute(sql, (sid,)).fetchall()
    finally:
        conn.close()
