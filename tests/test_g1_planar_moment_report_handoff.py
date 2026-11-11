# -*- coding: utf-8 -*-
"""G1-PLANAR-MOMENT-REPORT-HANDOFF-01 - saved planar-moment configurations in the report and PDF.

Owner-authorized (with three narrow guards): the existing HTML report and its PDF show the inventor's saved
planar-moment configurations through ONE adapter (``_pm_report_view``) that reuses the moment page's own derivation
(``_pm_saved_view``: one state derivation and re-evaluation, no second calculation) and ONE read-only partial shared
with the page. Guards: (1) the saved-moment snapshot is checked against the project the report describes and a
mismatch reads UNAVAILABLE; (2) the report / PDF carry no form, link or control; (3) no saved configuration -> no
section, an unreadable history -> UNAVAILABLE, and a number only for a CURRENT item whose re-evaluation succeeded,
always with the method's full fixed disclosure and the OWNER_STATED / UNVALIDATED / NOT EVIDENCE boundary.
Synthetic data only.
"""
import html as _html
import re

import pytest

import web.app as webapp
from engine import cap13_planar_moment as moment
from engine import record_store
from engine.record_store import PlanarMomentCorrupt
from tests.csrf_client import csrf_client
from tests.test_cap12_form_mockup_advisory import _client_for, _snapshot
from tests.test_cap13_therm01_integrated_part_eligibility import _integrated, MECH, ELEC
from tests.test_component_inventory_correct_withdraw import _correct as _correct_component
from tests.test_component_inventory_declare_list import _declare
from tests.test_g1_planar_moment_saved_declaration import (
    FORCE, POINT, EXPECTED, URL, _evaluate, _page, _save, _items, mech_client)  # noqa: F401
from tests.test_stage15_integrated_invention_entry import _pdf_source
from web import ui_text


def _report(c, sid):
    r = c.get(f"/session/{sid}/deliverable")
    assert r.status_code == 200, r.status_code
    return r.get_data(as_text=True)


def _section(raw):
    m = re.search(r'<section class="saved-moments-report".*?</section>', raw, re.S)
    return m.group(0) if m else None


def _states(section):
    return re.findall(r'<span class="pm-state" data-pm-state="([A-Z_]+)"', section)


def _number(section):
    m = re.search(r'data-pm-result-value><bdi dir="ltr">([^<]*)</bdi>', section)
    return m.group(1) if m else None


def _disclosure(lang="en"):
    return [part for part in ui_text.text("UI_CAP13M_DISCLOSURE", lang).split("\n\n")]


def _saved(c, sid, **over):
    assert _save(c, sid, _evaluate(c, sid, **over)).status_code == 200


# ─── absence, presence, read-only ────────────────────────────────────────────

def test_no_saved_configuration_means_no_section_in_report_or_pdf(mech_client, monkeypatch):
    c, sid = mech_client
    assert _section(_report(c, sid)) is None
    assert _section(_pdf_source(c, sid, monkeypatch)) is None


def test_a_current_configuration_shows_its_number_with_the_full_disclosure(mech_client, monkeypatch):
    c, sid = mech_client
    _saved(c, sid)
    for raw in (_report(c, sid), _pdf_source(c, sid, monkeypatch)):
        section = _section(raw)
        text = _html.unescape(section)
        assert _states(section) == ["CURRENT"] and _number(section) == EXPECTED
        for shown in ("Folding flap", POINT, FORCE, moment.METHOD_ID, "12.5", "80"):
            assert shown in text
        for part in _disclosure():
            assert _html.unescape(part) in text, part
        assert ui_text.text("UI_CAP13M_STATUS", "en") in text
        assert ui_text.text("UI_PM_REPORT_BOUNDARY", "en") in text
        assert "data-pm-sources" in section
        assert ui_text.text("UI_PM_REPORT_HISTORICAL", "en") in text
        assert "data-pm-report-generated" in section


def test_the_report_and_pdf_carry_no_form_link_or_control(mech_client, monkeypatch):
    c, sid = mech_client
    _saved(c, sid)
    for raw in (_report(c, sid), _pdf_source(c, sid, monkeypatch)):
        section = _section(raw)
        for banned in ("<form", "<button", "<input", "<a ", "/save", "/withdraw",
                       "correct=", "data-pm-correct", "data-pm-withdraw-form", "csrf"):
            assert banned not in section, banned


def test_the_page_still_has_its_actions_and_now_the_disclosure(mech_client):
    c, sid = mech_client
    _saved(c, sid)
    raw = _page(c, sid)[1]
    assert "data-pm-withdraw-form" in raw and "data-pm-correct" in raw
    block = raw.split("data-pm-saved", 1)[1]
    text = _html.unescape(block)
    for part in _disclosure():
        assert _html.unescape(part) in text, part


# ─── no stale number ─────────────────────────────────────────────────────────

def test_a_corrected_component_shows_no_number(mech_client, monkeypatch):
    c, sid = mech_client
    _saved(c, sid)
    store = webapp._get_store()
    comp = store.load_component_inventory_record(sid)[1].records[0]
    _correct_component(store, sid, comp.component_id, 0, "Folding flap, longer")
    for raw in (_report(c, sid), _pdf_source(c, sid, monkeypatch)):
        section = _section(raw)
        assert _states(section) == ["NEEDS_RECONFIRMATION"] and _number(section) is None
        assert "data-pm-disclosure" not in section
        assert ui_text.text("UI_PM_ISSUE_COMPONENT_CHANGED", "en") in _html.unescape(section)


def test_a_changed_method_identity_shows_no_number(mech_client, monkeypatch):
    c, sid = mech_client
    _saved(c, sid)
    real = record_store.planar_moment_method_identity()
    monkeypatch.setattr(record_store, "planar_moment_method_identity",
                        lambda: real[:3] + ("e" * 64,))
    section = _section(_report(c, sid))
    assert _states(section) == ["NEEDS_RECONFIRMATION"] and _number(section) is None


def test_a_refused_re_evaluation_shows_its_reason_and_no_number(mech_client, monkeypatch):
    c, sid = mech_client
    _saved(c, sid)
    monkeypatch.setattr(moment, "evaluate",
                        lambda captured, binding, **kw: {"outcome": moment.KNOWLEDGE_UNAVAILABLE,
                                                         "owner_state": None, "owner_reason": None,
                                                         "result": None})
    section = _section(_report(c, sid))
    assert _states(section) == ["RESULT_UNAVAILABLE"] and _number(section) is None
    assert "data-pm-outcome" in section and "data-pm-disclosure" not in section


def test_a_withdrawn_configuration_keeps_its_state_and_no_number(mech_client, monkeypatch):
    c, sid = mech_client
    _saved(c, sid)
    page = _page(c, sid)[1]
    block = page.split("data-pm-withdraw-form", 1)[1].split("</form>", 1)[0]
    data = {n: _html.unescape(v) for n, v in re.findall(
        r'<input type="hidden" name="([^"]+)" value="([^"]*)"', block)}
    data.pop("csrf_token")
    assert c.post(URL % sid + "/withdraw", data=dict(data, withdraw_confirm="yes")).status_code == 200
    for raw in (_report(c, sid), _pdf_source(c, sid, monkeypatch)):
        section = _section(raw)
        assert _states(section) == ["WITHDRAWN"] and _number(section) is None
        assert POINT in _html.unescape(section)


# ─── unavailable, mismatch ───────────────────────────────────────────────────

def test_an_unreadable_history_reads_unavailable_never_omitted(mech_client, monkeypatch):
    c, sid = mech_client
    _saved(c, sid)
    store = webapp._get_store()

    def boom(_pid):
        raise PlanarMomentCorrupt("synthetic")
    monkeypatch.setattr(store, "load_planar_moments", boom)
    for raw in (_report(c, sid), _pdf_source(c, sid, monkeypatch)):
        section = _section(raw)
        assert section is not None and "data-pm-report-unavailable" in section
        assert _number(section) is None and "data-pm-report-item" not in section


@pytest.mark.parametrize("mismatch", ["subsystems", "root_domain"])
def test_a_snapshot_that_does_not_match_the_report_reads_unavailable(mech_client, monkeypatch, mismatch):
    c, sid = mech_client
    _saved(c, sid)
    store = webapp._get_store()
    real = store.load_planar_moments

    def skewed(pid):
        snap = dict(real(pid))
        if mismatch == "subsystems":
            snap["subsystems"] = ("not-this-composition",)
        else:
            snap["root_domain"] = "electronics_electrical"
        return snap
    monkeypatch.setattr(store, "load_planar_moments", skewed)
    section = _section(_report(c, sid))
    assert "data-pm-report-unavailable" in section and _number(section) is None


# ─── integrated project, reuse, reads, audience, Arabic ──────────────────────

def test_an_integrated_project_names_the_declared_mechanical_part():
    c, _aid = _client_for("pm-report-integrated@example.com")
    sid = _integrated(c, ELEC)
    subs = webapp._get_store().load_project_subsystems(sid)
    mech_part = next(s for s in subs if s.domain == MECH)
    _declare(c, sid, name="Arm", function="Lifts", parts=(mech_part.subsystem_id,))
    _saved(c, sid)
    section = _section(_report(c, sid))
    assert _states(section) == ["CURRENT"] and _number(section) == EXPECTED
    assert mech_part.display_name in _html.unescape(section)


def test_the_report_reuses_the_page_derivation_and_reads_once(mech_client, monkeypatch):
    c, sid = mech_client
    _saved(c, sid)
    store = webapp._get_store()
    real_load, real_view = store.load_planar_moments, webapp._pm_saved_view
    loads, views = [], []
    monkeypatch.setattr(store, "load_planar_moments",
                        lambda pid: loads.append(pid) or real_load(pid))
    monkeypatch.setattr(webapp, "_pm_saved_view",
                        lambda *a, **k: views.append(k.get("snap") is not None) or real_view(*a, **k))
    _report(c, sid)
    assert loads == [sid] and views == [True]                # one read, handed to the page derivation
    loads.clear()
    views.clear()
    _pdf_source(c, sid, monkeypatch)
    assert loads == [sid] and views == [True]


def test_opening_the_report_or_pdf_writes_nothing(mech_client, monkeypatch):
    c, sid = mech_client
    _saved(c, sid)
    _report(c, sid)
    before = _snapshot(c)[0]
    _report(c, sid)
    _pdf_source(c, sid, monkeypatch)
    assert _snapshot(c)[0] == before


def test_the_audience_is_unchanged_owner_only(mech_client):
    c, sid = mech_client
    _saved(c, sid, F="12.5")
    other, _ = _client_for("pm-report-other@example.com")
    for client in (other, csrf_client(webapp.app)):
        for r in (client.get(f"/session/{sid}/deliverable"),
                  client.post(f"/session/{sid}/deliverable.pdf", data={})):
            assert r.status_code == 302 and POINT.encode() not in r.data


def test_the_report_and_pdf_state_the_same_meaning_in_arabic(mech_client, monkeypatch):
    c, sid = mech_client
    _saved(c, sid)
    c.post("/ui-language", data={"lang": "ar"})
    for raw in (_report(c, sid), _pdf_source(c, sid, monkeypatch)):
        section = _section(raw)
        text = _html.unescape(section)
        assert _number(section) == EXPECTED
        for key in ("UI_PM_REPORT_HEADING", "UI_PM_REPORT_BOUNDARY", "UI_PM_REPORT_HISTORICAL",
                    "UI_PM_STATE_CURRENT"):
            assert ui_text.text(key, "ar") in text, key
        for part in _disclosure("ar"):
            plain = re.sub(r"<[^>]+>", "", _html.unescape(webapp._cap13m_isolate(part, "ar")))
            assert plain in re.sub(r"<[^>]+>", "", text), part[:40]


def test_the_new_copy_has_english_and_arabic():
    for key in ("UI_PM_REPORT_HEADING", "UI_PM_REPORT_BOUNDARY", "UI_PM_REPORT_UNAVAILABLE",
                "UI_PM_REPORT_GENERATED", "UI_PM_REPORT_HISTORICAL"):
        assert ui_text.has_string(key), key
    for lang in ("en", "ar"):
        boundary = ui_text.text("UI_PM_REPORT_BOUNDARY", lang)
        for token in ("OWNER_STATED", "UNVALIDATED", "NOT EVIDENCE"):
            assert token in boundary, (lang, token)


def test_the_partial_holds_no_form_and_the_calculation_owner_is_untouched():
    from pathlib import Path
    root = Path(__file__).resolve().parent.parent
    partial = (root / "web/templates/_planar_moment_saved.html").read_text(encoding="utf-8")
    for banned in ("<form", "<button", "<input", "href=", "csrf"):
        assert banned not in partial, banned
    report = (root / "web/templates/deliverable.html").read_text(encoding="utf-8")
    assert "cap13m" not in report                            # the Slice-1 guard still holds
    source = (root / "web/app.py").read_text(encoding="utf-8")
    adapter = source[source.index("def _pm_report_view"):source.index("_PM_REFUSAL_MESSAGES = (")]
    assert "_cap13m.evaluate" not in adapter and "binding_issues" not in adapter
