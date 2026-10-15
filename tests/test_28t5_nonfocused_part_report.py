"""28-T5-NONFOCUSED-PART-REPORT-01 — the report / PDF show the inventor's SAVED answers about the required part
OUTSIDE the initial analysis focus.

What is pinned:
- only on a valid integrated invention, only the durable non-focused required part, only its governed
  MECHANISM_COMPLETENESS / BOUNDARY_AMBIGUITY questions (verbatim, pack order); answers verbatim with the
  OWNER_STATED / UNVALIDATED label; per-family recording presence none / some / all;
- ONE coherent store snapshot (``load_nonfocused_part_record``) feeds the view; anything unreadable, corrupt or
  inconsistent reads UNAVAILABLE, never "none recorded";
- the report / PDF safety disclosure beside the answers; root SafetySignal derivation, the root safety block and
  the part page are unchanged;
- no other project's answers in this section and no optional-part answers in it (the optional part's saved
  answers have their own separate report section, pinned by its own handoff tests), no Structured Export /
  readiness / state effect.
"""
import html as _html
import re
import sqlite3

import pytest

import web.app as appmod
from engine import domain_rules
from engine import subsystem_model as sm
from engine.record_store import PartAnswersCorrupt, ProjectNotFound, SqliteRecordStore
from engine.safety_signal import derive_inventor_stated_safety_signals
from tests.test_stage15_integrated_invention_entry import ELEC, MECH, _live, _pdf_source
from tests.test_stage28_control_loop_optional_part_slice1 import (  # noqa: F401  (fixtures)
    CL, _three_part_project, client, part_eligible)
from tests.test_stage15_integration_closure import _login
from tests.test_28t5_nonfocused_required_part_questions import (
    BA, HAZARD, MC, OTHER, PF, _ids, _pack_questions, _part, _save, _stored, _two_part, _url, _without_npr)
from web import ui_text

TITLE = {MECH: "UI_PQRR_TITLE_MECH", ELEC: "UI_PQRR_TITLE_ELEC"}
_BLOCK_RE = re.compile(r'<div class="nonfocused-part-answers".*?\n  </div>', re.S)


def _report(c, sid, lang="en"):
    if lang == "ar":
        assert c.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    return c.get("/session/%s/deliverable" % sid).get_data(as_text=True)


def _block(raw):
    found = _BLOCK_RE.findall(raw)
    assert len(found) == 1, len(found)
    return found[0]


def _strip(raw):
    return re.sub(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", "<ts>",
                  re.sub(r'name="csrf_token" value="[^"]*"', "", raw))


# ==========================================================================
# 1. Store: one coherent snapshot
# ==========================================================================
@pytest.mark.parametrize("focus", [MECH, ELEC])
def test_s01_one_snapshot_reader_returns_exactly_the_nonfocused_part_and_its_answers(tmp_path, focus):
    store = SqliteRecordStore(str(tmp_path / "r.db"))
    pid, mech, elec, ctrl = _stored(store, focus=focus, with_ctrl=True)
    nonfocused = elec if focus == MECH else mech
    store.apply_part_answer_delta(pid, nonfocused.subsystem_id, {_ids(nonfocused.domain)[0]: "Ours"})
    store.apply_part_answer_delta(pid, ctrl.subsystem_id, {"control_loop:MECHANISM_COMPLETENESS:Q1": "Loop"})
    part, answers = store.load_nonfocused_part_record(pid)
    assert part == nonfocused
    assert [(a.subsystem_id, a.answer_text) for a in answers] == [(nonfocused.subsystem_id, "Ours")]
    with pytest.raises(ProjectNotFound):
        store.load_nonfocused_part_record("no-such-project")


def test_s02_an_ordinary_project_has_no_nonfocused_part(tmp_path):
    from tests.test_stage15_integrated_invention_entry import _contract
    store = SqliteRecordStore(str(tmp_path / "o.db"))
    pid = store.create_project(_contract("i-ord"))
    assert store.load_nonfocused_part_record(pid) == (None, ())


def test_s03_a_corrupt_collection_fails_the_whole_read_closed(tmp_path):
    store = SqliteRecordStore(str(tmp_path / "c.db"))
    pid, mech, elec = _stored(store)
    store.apply_part_answer_delta(pid, elec.subsystem_id, {_ids(ELEC)[0]: "ok"})
    conn = sqlite3.connect(str(tmp_path / "c.db"))
    conn.execute("INSERT INTO subsystem_part_answers (project_id, subsystem_id, question_id, answer_text) "
                 "VALUES (?, ?, ?, ?)", (pid, mech.subsystem_id, _ids(MECH)[0], "smuggled"))
    conn.commit()
    conn.close()
    with pytest.raises(PartAnswersCorrupt):
        SqliteRecordStore(str(tmp_path / "c.db")).load_nonfocused_part_record(pid)


# ==========================================================================
# 2. Report and PDF content
# ==========================================================================
@pytest.mark.parametrize("focus", [MECH, ELEC])
def test_r01_report_and_pdf_show_the_parts_questions_verbatim_with_saved_answers(client, monkeypatch, focus):
    sid = _two_part(client, focus)
    other = OTHER[focus]
    pid = _part(sid, other)
    ids = _ids(other)
    _save(client, sid, pid, {ids[0]: "  It <b>turns</b> the arm\nslowly  ", ids[-1]: "It does not lift people"})
    for raw in (_report(client, sid), _pdf_source(client, sid, monkeypatch)):
        block = _block(raw)
        text = _html.unescape(block)
        assert ui_text.text(TITLE[other], "en") in text
        served = [_html.unescape(x) for x in re.findall(r'data-npr-question>([^<]*)</span>', block)]
        assert served == [t for g in (MC, BA) for _q, t in _pack_questions(other, g)]
        for _q, t in _pack_questions(other, PF):
            assert t not in text
        answers = [_html.unescape(x) for x in re.findall(r'data-npr-answer>([^<]*)</p>', block)]
        assert answers == ["It <b>turns</b> the arm\nslowly", "It does not lift people"]
        assert "<b>turns</b>" not in block                              # escaped, never markup
        assert block.count("data-npr-provenance") == 2
        assert text.count(ui_text.text("UI_PQRR_PROVENANCE", "en")) == 2
        assert block.count("data-npr-not-recorded") == len(ids) - 2
        assert ui_text.text("UI_PQRR_SAFETY", "en") in text
        assert pid not in block                                         # no identifier in the document


def test_r02_presence_is_none_some_or_all_per_family(client):
    sid = _two_part(client, MECH)
    elec = _part(sid, ELEC)
    mc = [q for q, _t in _pack_questions(ELEC, MC)]
    presences = lambda: re.findall(r'data-npr-family-presence>([^<]*)<', _block(_report(client, sid)))  # noqa
    none, some, all_ = (ui_text.text(k, "en") for k in ("UI_PQ_FAMILY_NONE", "UI_PQ_FAMILY_SOME",
                                                         "UI_PQ_FAMILY_ALL"))
    assert presences() == [none, none]
    _save(client, sid, elec, {mc[0]: "One"})
    assert presences() == [some, none]
    _save(client, sid, elec, {q: "Answer %d" % i for i, q in enumerate(mc)})
    assert presences() == [all_, none]
    assert "data-npr-unavailable" not in _report(client, sid)


def test_r03_unavailable_never_reads_as_none_recorded(client, monkeypatch):
    sid = _two_part(client, MECH)
    elec = _part(sid, ELEC)
    _save(client, sid, elec, {_ids(ELEC)[0]: "Saved"})
    store = appmod._get_store()

    def broken(*a, **k):
        raise sqlite3.OperationalError("injected")
    cases = []
    with monkeypatch.context() as m:                                    # unreadable store
        m.setattr(store, "load_nonfocused_part_record", broken)
        cases.append(_report(client, sid))
    with monkeypatch.context() as m:                                    # questions unreadable
        m.setattr(appmod, "get_domain_questions", lambda *a, **k: None)
        cases.append(_report(client, sid))
    with monkeypatch.context() as m:                                    # durable part != the scope's part
        real = store.load_nonfocused_part_record
        m.setattr(store, "load_nonfocused_part_record",
                  lambda pid: (sm.declared_subsystem(ELEC, "Other", "Other"), real(pid)[1]))
        cases.append(_report(client, sid))
    for raw in cases:
        block = _block(raw)
        assert "data-npr-unavailable" in block
        for clean in ("data-npr-not-recorded", "data-npr-answer", "data-npr-family-presence", "Saved"):
            assert clean not in block, clean
        assert ui_text.text("UI_PQRR_UNAVAILABLE", "en") in _html.unescape(block)
        assert ui_text.text("UI_PQRR_SAFETY", "en") in _html.unescape(block)


def test_r04_corrupt_durable_rows_read_unavailable(client):
    sid = _two_part(client, MECH)
    mech = _part(sid, MECH)
    import os
    conn = sqlite3.connect(os.environ["INVENTORAI_DB_PATH"])
    conn.execute("INSERT INTO subsystem_part_answers (project_id, subsystem_id, question_id, answer_text) "
                 "VALUES (?, ?, ?, ?)", (sid, mech, _ids(MECH)[0], "smuggled onto the focused part"))
    conn.commit()
    conn.close()
    block = _block(_report(client, sid))
    assert "data-npr-unavailable" in block and "smuggled" not in block


def test_r05_one_snapshot_feeds_each_render_and_no_separate_answer_read(client, monkeypatch):
    sid = _two_part(client, MECH)
    store = appmod._get_store()
    calls = []
    real = store.load_nonfocused_part_record
    monkeypatch.setattr(store, "load_nonfocused_part_record", lambda pid: calls.append(pid) or real(pid))

    def forbidden(*a, **k):
        raise AssertionError("the report must not combine a separate answer read")
    monkeypatch.setattr(store, "load_part_answers", forbidden)
    _block(_report(client, sid))
    assert calls == [sid]


def test_r06_other_projects_and_control_loop_answers_never_appear(client, part_eligible):
    a = _two_part(client, MECH)
    b = _two_part(client, MECH)
    _save(client, b, _part(b, ELEC), {_ids(ELEC)[0]: "Belongs to project B"})
    assert "Belongs to project B" not in _report(client, a)
    sid = _three_part_project(client)
    ctrl = _part(sid, CL)
    from tests.test_28t5_nonfocused_required_part_questions import _form
    form = _form(client, sid, ctrl)
    client.post(_url(sid), data=dict(form, **{"part_answer__control_loop:MECHANISM_COMPLETENESS:Q1":
                                              "ControlLoopAnswerMarker"}))
    raw = _report(client, sid)
    # Intentionally ADVANCED by CONTROL-LOOP-ENGINEERING-HANDOFF-01: the optional control-loop part's saved
    # answer now reaches the report, but ONLY inside its own control-loop section — never in this non-focused
    # required-part section and never in the root safety block (pinned in
    # tests/test_control_loop_engineering_handoff.py). The other-project isolation above is unchanged.
    assert "ControlLoopAnswerMarker" not in _block(raw)
    assert raw.count("ControlLoopAnswerMarker") == 1
    from tests.test_control_loop_engineering_handoff import _clr
    assert "ControlLoopAnswerMarker" in _clr(raw)
    assert ui_text.text("UI_SS_OPTIONAL_PART_SCOPE", "en") in _html.unescape(raw)


def test_r07_unauthorized_reader_is_denied(client):
    _login(client, "npr-owner@example.com")
    sid = _two_part(client, MECH)
    _save(client, sid, _part(sid, ELEC), {_ids(ELEC)[0]: "PrivateAnswerMarker"})
    from tests.csrf_client import csrf_client
    with csrf_client(appmod.app) as other:
        _login(other, "npr-other@example.com")
        r = other.get("/session/%s/deliverable" % sid)
        assert r.status_code in (302, 403, 404)
        assert "PrivateAnswerMarker" not in r.get_data(as_text=True)
        r = other.post("/session/%s/deliverable.pdf" % sid, data={})
        assert r.status_code in (302, 403, 404) and b"PrivateAnswerMarker" not in r.data


def test_r08_single_domain_projects_and_stale_answers(client, monkeypatch):
    from tests.test_safe_question_routing_pf_q2 import ELEC_SEED, _start
    single = _start(client, seed=ELEC_SEED, domain=ELEC)
    assert "nonfocused-part-answers" not in _report(client, single)
    sid = _two_part(client, MECH)
    elec = _part(sid, ELEC)
    q = _ids(ELEC)[0]
    _save(client, sid, elec, {q: "An earlier answer"})
    real = domain_rules.get_domain_questions

    def without_first(domain, gap_type):
        qs = real(domain, gap_type)
        return tuple(x for x in qs if x[0] != q) if qs is not None else None
    monkeypatch.setattr(appmod, "get_domain_questions", without_first)
    block = _block(_report(client, sid))
    assert "data-npr-stale" in block and "An earlier answer" not in block


# ==========================================================================
# 3. Safety disclosure and no root-safety change
# ==========================================================================
@pytest.mark.parametrize("focus", [MECH, ELEC])
def test_sf01_disclosure_is_beside_the_answers_and_root_safety_is_unchanged(client, monkeypatch, focus):
    sid = _two_part(client, focus)
    other = OTHER[focus]
    pid = _part(sid, other)
    root_before = derive_inventor_stated_safety_signals(_live(sid))
    report_before = _report(client, sid)
    _save(client, sid, pid, {_ids(other)[0]: HAZARD[other]})
    raw = _report(client, sid)
    assert derive_inventor_stated_safety_signals(_live(sid)) == root_before
    assert HAZARD[other] in _html.unescape(_block(raw))                 # shown as the inventor's answer
    assert HAZARD[other] not in _html.unescape(_without_npr(raw))       # never in the root safety block
    assert _strip(_without_npr(raw)) == _strip(_without_npr(report_before))
    assert ui_text.text("UI_SS_PART_PAGE_SCOPE", "en") in _html.unescape(raw)
    assert "data-pq-safety-signal" in client.get(_url(sid, pid)).get_data(as_text=True)   # page unchanged
    pdf = _pdf_source(client, sid, monkeypatch)
    assert ui_text.text("UI_PQRR_SAFETY", "en") in _html.unescape(_block(pdf))


# ==========================================================================
# 4. No downstream effect; EN / AR
# ==========================================================================
def test_x01_export_readiness_and_state_are_unchanged(client):
    _login(client, "npr-x01@example.com")
    sid = _two_part(client, MECH)
    readiness_before = appmod._readiness_snapshot_context(sid, _live(sid))
    export_before = client.get("/account/projects/%s/export" % sid).get_data(as_text=True)
    vars_before = sorted(vars(_live(sid)))
    _save(client, sid, _part(sid, ELEC), {_ids(ELEC)[0]: "ExportMarker"})
    _report(client, sid)
    assert client.get("/account/projects/%s/export" % sid).get_data(as_text=True) == export_before
    assert appmod._readiness_snapshot_context(sid, _live(sid)) == readiness_before
    assert sorted(vars(_live(sid))) == vars_before


@pytest.mark.parametrize("focus", [MECH, ELEC])
def test_x02_arabic_report_and_pdf_use_arabic_copy_and_isolate_directions(client, monkeypatch, focus):
    sid = _two_part(client, focus)
    other = OTHER[focus]
    _save(client, sid, _part(sid, other), {_ids(other)[0]: "يدير الذراع"})
    for raw in (_report(client, sid, lang="ar"), _pdf_source(client, sid, monkeypatch)):
        block = _block(raw)
        text = _html.unescape(block)
        for key in (TITLE[other], "UI_PQRR_INTRO", "UI_PQRR_PROVENANCE", "UI_PQRR_SAFETY"):
            assert ui_text.text(key, "ar") in text, key
        assert '<span dir="ltr" lang="en" data-npr-question>' in block
        assert 'dir="auto" data-npr-answer>' in block and "يدير الذراع" in text


def test_x03_new_copy_is_bilingual_and_makes_no_safety_claim():
    for key in ("UI_PQRR_TITLE", "UI_PQRR_TITLE_MECH", "UI_PQRR_TITLE_ELEC", "UI_PQRR_INTRO",
                "UI_PQRR_PROVENANCE", "UI_PQRR_UNAVAILABLE", "UI_PQRR_SAFETY"):
        entry = ui_text.UI_STRINGS[key]
        assert entry["en"].strip() and entry["ar"].strip(), key
        for word in ("certified", "compliant", "guarantee", "mitigat"):
            assert word not in entry["en"].lower(), (key, word)
    safety = ui_text.UI_STRINGS["UI_PQRR_SAFETY"]["en"]
    for phrase in ("only on this part's question page", "not included in this report or PDF",
                   "do not cover these answers", "not evidence that this part or the invention is safe"):
        assert phrase in safety, phrase
