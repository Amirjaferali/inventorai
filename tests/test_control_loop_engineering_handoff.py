"""CONTROL-LOOP-ENGINEERING-HANDOFF-01 — the inventor's saved answers about the optional control-loop part in
the analysis report and PDF.

What is pinned:
- ONE "Control loop — information you recorded" section, inside the report's integrated-scope section, rendered
  by the HTML report AND the PDF from the SAME view (``_control_loop_part_report_view``), only when the report's
  own integrated composition holds the optional ``control_loop`` part;
- the view reads ``load_parts_components_interactions`` (durable composition, focus and the WHOLE validated
  part-answer collection in one store snapshot) ONCE per render, requires the durable optional part to be exactly
  the reported one (same identity, same focus) and shows ONLY that part's answers;
- the part's governed MECHANISM_COMPLETENESS / BOUNDARY_AMBIGUITY questions verbatim in pack order; each answer
  verbatim, escaped, direction-isolated and labelled OWNER_STATED / UNVALIDATED, or "not recorded"; per-family
  recording presence; a stale answer is disclosed, never attached to a current question;
- anything unreadable, corrupt or inconsistent reads UNAVAILABLE in this section only (never "not recorded"),
  and the rest of the report — the non-focused required-part section included — still renders;
- the answers stay outside root SafetySignal derivation and the root safety block (both disclosures shown);
  saved answers stay readable when part eligibility is withdrawn; owner-only audience; no writes; the Stage 35
  disclosure export is unchanged.
"""
import html as _html
import os
import re
import sqlite3

import pytest

import web.app as appmod
from engine import domain_activation, domain_rules
from engine import subsystem_model as sm
from engine.record_store import PartAnswersCorrupt, ProjectNotFound, RecordStoreConnectionUnsafe
from tests.test_stage15_integrated_invention_entry import ELEC, MECH, _live, _pdf_source
from tests.test_stage28_control_loop_optional_part_slice1 import (  # noqa: F401  (fixtures)
    CL, _three_part_project, client, part_eligible)
from tests.test_stage15_integration_closure import _login
from tests.test_28t5_nonfocused_required_part_questions import _form, _ids, _part, _two_part, _url
from web import ui_text

_CLR_RE = re.compile(r'<div class="control-loop-answers".*?\n  </div>', re.S)
_NPR_RE = re.compile(r'<div class="nonfocused-part-answers".*?\n  </div>', re.S)
_SAFETY_RE = re.compile(r'<div class="safety-signals">.*?</div>', re.S)
MC = "control_loop:MECHANISM_COMPLETENESS:"
BA = "control_loop:BOUNDARY_AMBIGUITY:"


def _report(c, sid, lang="en"):
    if lang == "ar":
        assert c.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    r = c.get("/session/%s/deliverable" % sid)
    assert r.status_code == 200, r.status_code
    return r.get_data(as_text=True)


def _clr(raw):
    found = _CLR_RE.findall(raw)
    assert len(found) <= 1, len(found)
    return found[0] if found else None


def _save_ctrl(c, sid, answers):
    """Save control-loop part answers through the real part-question route."""
    ctrl = _part(sid, CL)
    data = dict(_form(c, sid, ctrl))
    for qid, text in answers.items():
        data["part_answer__" + qid] = text
    r = c.post(_url(sid), data=data)
    assert r.status_code in (200, 302), r.status_code
    return ctrl


def _rendered(section):
    """``[(question_text, answer | None)]`` in rendered order, unescaped."""
    out = []
    for fam in re.findall(r"<div data-clr-family.*?\n    </div>", section, re.S):
        parts = re.split(r'(?=<p style="margin:6px 0 0 0;font-size:13px"><span dir="ltr" lang="en" data-clr-question>)',
                         fam)[1:]
        for p in parts:
            q = _html.unescape(re.search(r"data-clr-question>(.*?)</span>", p, re.S).group(1))
            a = re.search(r'dir="auto" data-clr-answer>(.*?)</p>', p, re.S)
            assert (a is None) == ("data-clr-not-recorded" in p)
            out.append((q, _html.unescape(a.group(1)) if a else None))
    return out


def _pack(gap_type):
    return [t for _q, t in domain_rules.get_domain_questions(CL, gap_type)]


# ==========================================================================
# 1. What the section shows — HTML and PDF from the same view
# ==========================================================================
@pytest.mark.parametrize("focus", [MECH, ELEC])
def test_h01_saved_answers_appear_verbatim_in_pack_order_in_html_and_pdf(client, part_eligible, monkeypatch, focus):
    sid = _three_part_project(client, focus=focus)
    _save_ctrl(client, sid, {MC + "Q1": "Room temperature", MC + "Q7": "I do not know yet",
                             BA + "Q2": "The thermostat <logic> & relay"})
    expected = [(t, None) for t in _pack("MECHANISM_COMPLETENESS")] + \
               [(t, None) for t in _pack("BOUNDARY_AMBIGUITY")]
    expected[0] = (expected[0][0], "Room temperature")
    expected[6] = (expected[6][0], "I do not know yet")
    expected[len(_pack("MECHANISM_COMPLETENESS")) + 1] = (expected[len(_pack("MECHANISM_COMPLETENESS")) + 1][0],
                                                         "The thermostat <logic> & relay")
    html_raw = _report(client, sid)
    pdf_raw = _pdf_source(client, sid, monkeypatch)
    for raw in (html_raw, pdf_raw):
        section = _clr(raw)
        assert section is not None
        assert _rendered(section) == expected
        assert section.count("data-clr-provenance") == 3
        assert ui_text.text("UI_PQRR_PROVENANCE", "en") in _html.unescape(section)
        assert section.count("data-clr-not-recorded") == len(expected) - 3
        for key in ("UI_CLR_TITLE", "UI_CLR_INTRO", "UI_PQ_FAMILY_MECHANISM", "UI_PQ_FAMILY_BOUNDARY",
                    "UI_PQ_FAMILY_SOME", "UI_PQ_PRESENCE_NOTE", "UI_PQ_SAFETY_SCOPE"):
            assert ui_text.text(key, "en") in _html.unescape(section), key
        assert "data-clr-unavailable" not in section and "data-clr-stale" not in section
        assert "<logic>" not in section and "&lt;logic&gt; &amp; relay" in section
        assert re.search(r'dir="auto" data-clr-answer>The thermostat &lt;logic&gt;', section)
    assert _rendered(_clr(html_raw)) == _rendered(_clr(pdf_raw))


def test_h02_only_the_control_loop_answers_and_no_duplicate_or_misassociation(client, part_eligible):
    sid = _three_part_project(client, focus=MECH)
    _save_ctrl(client, sid, {MC + "Q1": "CtrlOnlyMarker-41"})
    elec = _part(sid, ELEC)
    data = dict(_form(client, sid, elec))
    data["part_answer__" + _ids(ELEC)[0]] = "ElecOnlyMarker-42"
    assert client.post(_url(sid, elec), data=data).status_code in (200, 302)
    raw = _report(client, sid)
    section, npr = _clr(raw), _NPR_RE.findall(raw)
    assert len(npr) == 1
    assert "CtrlOnlyMarker-41" in section and "ElecOnlyMarker-42" not in section
    assert "ElecOnlyMarker-42" in npr[0] and "CtrlOnlyMarker-41" not in npr[0]
    assert raw.count("CtrlOnlyMarker-41") == 1 and raw.count("ElecOnlyMarker-42") == 1
    assert "CtrlOnlyMarker-41" not in _SAFETY_RE.search(raw).group(0)


def test_h03_no_optional_part_means_no_section(client):
    from tests.test_safe_question_routing_pf_q2 import ELEC_SEED, _start
    for sid in (_two_part(client, MECH), _two_part(client, ELEC), _start(client, seed=ELEC_SEED, domain=ELEC)):
        raw = _report(client, sid)
        assert _clr(raw) is None and "data-control-loop-answers" not in raw
        assert appmod._control_loop_part_report_view(sid, _live(sid)) is None


# ==========================================================================
# 2. Fail closed — never "not recorded" for unreadable or inconsistent material
# ==========================================================================
def _unavailable(section, *hidden):
    assert section is not None and "data-clr-unavailable" in section
    assert ui_text.text("UI_PQRR_UNAVAILABLE", "en") in _html.unescape(section)
    for marker in ("data-clr-not-recorded", "data-clr-answer", "data-clr-family", "data-clr-intro"):
        assert marker not in section, marker
    for text in hidden:
        assert text not in section
    assert "data-clr-safety" in section                      # the safety disclosure still stands


def test_f01_a_corrupt_answer_collection_reads_unavailable_and_the_report_still_renders(client, part_eligible,
                                                                                        monkeypatch):
    sid = _three_part_project(client)
    ctrl = _save_ctrl(client, sid, {MC + "Q1": "HiddenWhenCorrupt"})
    con = sqlite3.connect(os.environ["INVENTORAI_DB_PATH"])
    try:
        con.execute("INSERT INTO subsystem_part_answers (project_id, subsystem_id, question_id, answer_text) "
                    "VALUES (?, ?, ?, ?)", (sid, ctrl, "mechanical:MECHANISM_COMPLETENESS:Q1", "orphan"))
        con.commit()
    finally:
        con.close()
    with pytest.raises(PartAnswersCorrupt):
        appmod._get_store().load_parts_components_interactions(sid)
    for raw in (_report(client, sid), _pdf_source(client, sid, monkeypatch)):
        _unavailable(_clr(raw), "HiddenWhenCorrupt")
        assert 'id="report-contents"' in raw and "data-declared-components" in raw


@pytest.mark.parametrize("error", [RuntimeError("down"), RecordStoreConnectionUnsafe("unsafe"),
                                   sqlite3.OperationalError("locked"), ProjectNotFound("gone")])
def test_f02_any_read_failure_is_unavailable_and_leaves_the_other_part_section_intact(client, part_eligible,
                                                                                      monkeypatch, error):
    sid = _three_part_project(client, focus=MECH)
    _save_ctrl(client, sid, {MC + "Q1": "HiddenOnFailure"})
    elec = _part(sid, ELEC)
    data = dict(_form(client, sid, elec))
    data["part_answer__" + _ids(ELEC)[0]] = "OtherPartStillShown"
    client.post(_url(sid, elec), data=data)

    def boom(_sid):
        raise error
    monkeypatch.setattr(appmod._get_store(), "load_parts_components_interactions", boom)
    raw = _report(client, sid)
    _unavailable(_clr(raw), "HiddenOnFailure")
    assert "OtherPartStillShown" in _NPR_RE.findall(raw)[0]


def test_f03_an_identity_or_focus_mismatch_is_unavailable(client, part_eligible, monkeypatch):
    sid = _three_part_project(client, focus=MECH)
    _save_ctrl(client, sid, {MC + "Q1": "HiddenOnMismatch"})
    store = appmod._get_store()
    real = store.load_parts_components_interactions
    snap = real(sid)
    subs = snap["subsystems"]
    other_ctrl = sm.declared_subsystem(CL, subs[2].display_name, subs[2].function_text)
    variants = [
        dict(snap, subsystems=(subs[0], subs[1], other_ctrl)),               # a different optional part identity
        dict(snap, subsystems=(subs[0], subs[1])),                           # durable composition lost the part
        dict(snap, focus=ELEC),                                               # durable focus differs from the report
    ]
    for variant in variants:
        monkeypatch.setattr(store, "load_parts_components_interactions", lambda _sid, v=variant: v)
        assert appmod._control_loop_part_report_view(sid, _live(sid)) == {"available": False}
        _unavailable(_clr(_report(client, sid)), "HiddenOnMismatch")


def test_f04_a_stale_answer_is_disclosed_never_attached_to_a_current_question(client, part_eligible, monkeypatch):
    sid = _three_part_project(client)
    _save_ctrl(client, sid, {MC + "Q1": "AnswerToARemovedQuestion", MC + "Q2": "StillCurrent"})
    real = domain_rules.get_domain_questions

    def without_q1(domain, gap_type):
        qs = real(domain, gap_type)
        if domain == CL and gap_type == "MECHANISM_COMPLETENESS":
            return [q for q in qs if q[0] != MC + "Q1"]
        return qs
    monkeypatch.setattr(appmod, "get_domain_questions", without_q1)
    section = _clr(_report(client, sid))
    assert "data-clr-stale" in section and ui_text.text("UI_PQ_STALE", "en") in _html.unescape(section)
    assert "AnswerToARemovedQuestion" not in section and "StillCurrent" in section

    def none_for_ctrl(domain, gap_type):
        return None if domain == CL else real(domain, gap_type)
    monkeypatch.setattr(appmod, "get_domain_questions", none_for_ctrl)
    _unavailable(_clr(_report(client, sid)), "StillCurrent")


# ==========================================================================
# 3. Eligibility, safety isolation, audience, read-only, exports, Arabic
# ==========================================================================
def test_e01_saved_answers_stay_readable_when_part_eligibility_is_withdrawn(client, part_eligible, monkeypatch):
    sid = _three_part_project(client)
    _save_ctrl(client, sid, {MC + "Q1": "ReadableAfterWithdrawal"})
    monkeypatch.setattr(domain_activation, "is_part_eligible", lambda _d: False)
    section = _clr(_report(client, sid))
    assert "ReadableAfterWithdrawal" in section and "data-clr-answer" in section


def test_e02_answers_stay_outside_root_safety_signals(client, part_eligible):
    from tests.test_28t5_nonfocused_required_part_questions import HAZARD
    sid = _three_part_project(client, focus=MECH)
    before = _SAFETY_RE.search(_report(client, sid)).group(0)
    _save_ctrl(client, sid, {MC + "Q4": HAZARD[MECH] + " CtrlHazardMarker"})
    raw = _report(client, sid)
    safety = _SAFETY_RE.search(raw).group(0)
    assert "CtrlHazardMarker" not in safety and safety == before
    assert "data-ss-input-scope" in raw
    assert ui_text.text("UI_SS_OPTIONAL_PART_SCOPE", "en") in _html.unescape(raw)
    assert ui_text.text("UI_PQ_SAFETY_SCOPE", "en") in _html.unescape(_clr(raw))


def test_e03_owner_only_and_no_cross_project_disclosure(client, part_eligible):
    _login(client, "clr-owner@example.com")
    sid = _three_part_project(client)
    _save_ctrl(client, sid, {MC + "Q1": "PrivateCtrlMarker"})
    other_sid = _three_part_project(client)
    assert "PrivateCtrlMarker" not in _report(client, other_sid)
    from tests.csrf_client import csrf_client
    with csrf_client(appmod.app) as other:
        _login(other, "clr-other@example.com")
        for r in (other.get("/session/%s/deliverable" % sid), other.post("/session/%s/deliverable.pdf" % sid, data={})):
            assert r.status_code in (302, 403, 404) and b"PrivateCtrlMarker" not in r.data


def test_e04_one_read_per_render_no_writes_and_the_disclosure_export_is_unchanged(client, part_eligible,
                                                                                    monkeypatch):
    from tests.test_stage19_durable_success_criteria import _client_for
    appmod.app.config["TESTING"] = True
    c, _aid = _client_for("clr-export@example.com")
    sid = _three_part_project(c)
    stamp = re.compile(rb"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?Z")
    export = "/account/projects/%s/disclosure-export/json" % sid
    before = stamp.sub(b"", c.get(export).data)
    _save_ctrl(c, sid, {MC + "Q1": "NotInTheExport"})
    after = c.get(export).data
    assert stamp.sub(b"", after) == before and b"NotInTheExport" not in after
    store = appmod._get_store()
    real = store.load_parts_components_interactions
    calls = []

    def spy(project_id):
        calls.append(project_id)
        return real(project_id)
    monkeypatch.setattr(store, "load_parts_components_interactions", spy)
    _report(c, sid)
    assert calls == [sid]
    calls.clear()
    _pdf_source(c, sid, monkeypatch)
    assert calls == [sid]
    con = sqlite3.connect(os.environ["INVENTORAI_DB_PATH"])
    try:
        dump_before = list(con.iterdump())
        _report(c, sid)
        _pdf_source(c, sid, monkeypatch)
        assert list(con.iterdump()) == dump_before
    finally:
        con.close()


def test_e05_arabic_copy_and_catalogue(client, part_eligible):
    sid = _three_part_project(client)
    _save_ctrl(client, sid, {MC + "Q1": "درجة حرارة الغرفة"})
    raw = _report(client, sid, lang="ar")
    section = _html.unescape(_clr(raw))
    for key in ("UI_CLR_TITLE", "UI_CLR_INTRO", "UI_PQ_FAMILY_MECHANISM", "UI_PQRR_PROVENANCE", "UI_PQ_SAFETY_SCOPE"):
        assert ui_text.text(key, "ar") in section, key
    assert 'dir="rtl"' in raw and "درجة حرارة الغرفة" in section
    for key in ("UI_CLR_TITLE", "UI_CLR_INTRO"):
        entry = ui_text.UI_STRINGS[key]
        assert entry["en"].strip() and entry["ar"].strip() and entry["en"] != entry["ar"]
    intro = ui_text.text("UI_CLR_INTRO", "en")
    for phrase in ("not designed, analysed or checked", "no program logic, timing, settings, stability",
                   "does not mean the control design is complete"):
        assert phrase in intro
