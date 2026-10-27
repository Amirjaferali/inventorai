"""28-T1-MEASUREMENT-PLANNING-REFERENCE-01 — the CAP-09 measurement-planning page
shows the two EXISTING Sensors / Instrumentation reference groups (PR #789,
PR #794) to an Electronics-root project, beside the measurement-method
introduction.

Proves: the same groups, claims, copy keys, sources and boundaries as the
report, in their established order and nothing else (not the controller group);
eligibility is ONLY the trusted durable root domain — Mechanical roots, a
Mechanical-focus integrated project, an unreadable domain and an unavailable
page show nothing, and the gap state does not matter; every render path of the
page (GET and a refused POST) respects it; authorization denials are unchanged;
the page writes nothing; and the report / PDF binding is unchanged.
Synthetic invention data only.
"""
import html as _html
import os
import pickle
import re
import sqlite3

import pytest

import web.app as webapp
from web import cap01_guidance, ui_text
from tests.test_cap12_form_mockup_advisory import _client_for
from tests.test_cap13_therm01_integrated_part_eligibility import _integrated
from tests.test_stage19_durable_success_criteria import (
    ELEC_ANSWERS, ELEC_IDEA, MECH_ANSWERS, MECH_IDEA, PREFIX, _answer,
)

PAGE = "/session/%s/success-criteria"
GROUPS = ("sensing_value_threshold_reference_v1",
          "measurement_accuracy_resolution_reference_v1")
CONTROLLER = "controller_input_logic_output_reference_v1"
STEMS = ("UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_MECHANISM_COMPLETENESS_SENSING_FUNDAMENTALS_",
         "UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_MECHANISM_COMPLETENESS_ACCURACY_RESOLUTION_FUNDAMENTALS_")
PARTS = ("TITLE", "INTRO", "ITEM_1_TITLE", "ITEM_1_TEXT", "SOURCE", "BOUNDARY")
_PANEL_RE = re.compile(r'<details class="measurement-reference".*?</details>', re.S)


def _start(client, idea, domain, answers):
    r = client.post("/start", data={"idea": idea, "domain_confirm": domain})
    assert r.status_code == 302, r.status_code
    sid = r.headers["Location"].rsplit("/", 1)[-1]
    for text in answers:
        _answer(client, sid, text)
    return sid


def _elec(tag="owner"):
    client, _aid = _client_for("s28t1-mref-%s@example.com" % tag)
    return client, _start(client, ELEC_IDEA, "electronics_electrical", ELEC_ANSWERS)


def _page(client, sid):
    r = client.get(PAGE % sid)
    return r.status_code, r.get_data(as_text=True)


def _panel(body):
    m = _PANEL_RE.search(body)
    return m.group(0) if m else None


def _visible(fragment):
    return re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", " ", fragment))).strip()


def _group_blocks(fragment):
    return re.findall(r'<section class="cap01-fundamentals" data-cap01-fundamentals="([^"]+)"', fragment)


def _dump():
    with sqlite3.connect(os.environ["INVENTORAI_DB_PATH"]) as connection:
        return list(connection.iterdump())


# ==========================================================================
# the accessor: the existing owner, no second catalogue
# ==========================================================================
def test_accessor_reuses_the_existing_groups_in_their_established_order():
    groups = cap01_guidance.measurement_planning_references("electronics_electrical")
    assert tuple(g["group_id"] for g in groups) == GROUPS
    row = cap01_guidance.CAP01_GAP_FUNDAMENTALS_EXTENSIONS[
        ("electronics_electrical", "MECHANISM_COMPLETENESS")]
    assert tuple(r[0] for r in row)[:2] == GROUPS            # same order as the report context
    report_view = cap01_guidance.gap_context_copy("electronics_electrical",
                                                  "MECHANISM_COMPLETENESS")
    assert list(groups) == list(report_view["fundamentals_groups"][:2])   # identical key views
    for group, stem in zip(groups, STEMS):
        assert group["prose_only"] is True
        assert group["title_key"] == stem + "TITLE"
        assert group["source_key"] == stem + "SOURCE"
        assert group["boundary_key"] == stem + "BOUNDARY"


@pytest.mark.parametrize("domain", ["mechanical", "control_loop", "software", None, "",
                                    " electronics_electrical", "Electronics_Electrical"])
def test_accessor_is_exact_on_the_root_domain(domain):
    assert cap01_guidance.measurement_planning_references(domain) is None


def test_accessor_is_all_or_nothing(monkeypatch):
    real = ui_text.has_string
    monkeypatch.setattr(ui_text, "has_string",
                        lambda key: False if key == STEMS[1] + "SOURCE" else real(key))
    assert cap01_guidance.measurement_planning_references("electronics_electrical") is None


# ==========================================================================
# the planning page
# ==========================================================================
@pytest.mark.parametrize("lang", ["en", "ar"])
def test_electronics_page_shows_both_groups_collapsed_with_their_approved_copy(lang):
    client, sid = _elec("show-%s" % lang)
    if lang == "ar":
        client.post("/ui-language", data={"lang": "ar"})
    status, body = _page(client, sid)
    assert status == 200
    panel = _panel(body)
    assert panel is not None and " open" not in panel.split(">", 1)[0]   # collapsed by default
    assert _group_blocks(panel) == [g.replace("_", "-") for g in GROUPS]
    assert CONTROLLER.replace("_", "-") not in panel
    text = _visible(panel)
    for key in ("UI_SC_MREF_SUMMARY", "UI_SC_MREF_NOTE"):
        assert ui_text.text(key, lang) in text
    for stem in STEMS:
        for part in PARTS:
            assert _visible(ui_text.text(stem + part, lang)) in text, stem + part
    # beside the measurement-method introduction, before the experiment form
    assert body.index(ui_text.text("UI_SC_METHOD_INTRO", lang).replace("'", "&#39;")) \
        < body.index("data-measurement-reference") < body.index('action="/session/%s/success-criteria"' % sid)


def test_the_groups_read_the_same_on_the_page_and_in_the_report():
    client, sid = _elec("same")
    page = _visible(_panel(_page(client, sid)[1]))
    # The report carries the groups while the mechanism gap is current, so it is
    # read on a fresh Electronics project of the same owner (gap OPEN).
    fresh = _start(client, ELEC_IDEA, "electronics_electrical", ())
    report = client.get("/session/%s/deliverable" % fresh).get_data(as_text=True)
    for group in GROUPS:
        m = re.search(r'<div class="cap01-fundamentals" data-cap01-fundamentals="%s">(.*?)</div>'
                      % group.replace("_", "-"), report, re.S)
        assert m, group
        assert _visible(m.group(1)) in page


def test_the_panel_does_not_depend_on_the_gap_state():
    client, sid = _elec("gap")
    state = webapp.SESSION_STORE[sid]["state"]
    assert state.get_gap("MECHANISM_COMPLETENESS").status == "CLOSED"
    report = client.get("/session/%s/deliverable" % sid).get_data(as_text=True)
    assert "sensing-value-threshold-reference-v1" not in report     # report binding unchanged
    assert _group_blocks(_panel(_page(client, sid)[1])) == [g.replace("_", "-") for g in GROUPS]


def test_a_mechanical_root_shows_no_panel():
    client, _aid = _client_for("s28t1-mref-mech@example.com")
    sid = _start(client, MECH_IDEA, "mechanical", MECH_ANSWERS)
    status, body = _page(client, sid)
    assert status == 200 and 'action="/session/%s/success-criteria"' % sid in body
    assert _panel(body) is None and "data-measurement-reference" not in body


@pytest.mark.parametrize("focus,root_rule", [("electronics_electrical", True), ("mechanical", False)])
def test_an_integrated_project_shows_the_panel_for_its_declared_electronics_part(focus, root_rule):
    # The accessor's own root rule is unchanged; MEASUREMENT-PLANNING-INTEGRATED-PART-01
    # (Owner-authorized) shows the panel on the page for the declared Electrical /
    # Electronics part of a valid integrated composition, whatever the focus.
    client, _aid = _client_for("s28t1-mref-int-%s@example.com" % focus[:4])
    sid = _integrated(client, focus)
    assert (cap01_guidance.measurement_planning_references(
        webapp._cap12_root_domain(sid)) is not None) is root_rule
    assert _panel(_page(client, sid)[1]) is not None


@pytest.mark.parametrize("reader", [lambda _sid: None,
                                    lambda _sid: (_ for _ in ()).throw(RuntimeError("unreadable"))])
def test_an_unreadable_root_domain_shows_nothing_and_the_page_still_works(monkeypatch, reader):
    client, sid = _elec("unreadable")
    monkeypatch.setattr(webapp, "_cap12_root_domain", reader)
    status, body = _page(client, sid)
    assert status == 200 and 'action="/session/%s/success-criteria"' % sid in body
    assert _panel(body) is None


def test_an_unavailable_page_shows_no_panel(monkeypatch):
    client, sid = _elec("unavailable")

    def boom(*_a, **_k):
        raise RuntimeError("no reconstruction")
    monkeypatch.setattr(webapp, "reconstruct_readonly_state", boom)
    status, body = _page(client, sid)
    assert status == 503 and _panel(body) is None


def test_a_refused_post_rerenders_with_the_same_rule():
    client, sid = _elec("post")
    body = _page(client, sid)[1]
    eid = re.search(r'name="%s([^"]+)"' % re.escape(PREFIX), body).group(1)
    r = client.post(PAGE % sid, data={PREFIX + eid: "x" * (webapp.MAX_CRITERION_LENGTH + 1)})
    assert r.status_code == 400
    refused = r.get_data(as_text=True)
    assert 'id="draft-unsaved"' in refused
    assert _group_blocks(_panel(refused)) == [g.replace("_", "-") for g in GROUPS]


def test_denials_are_unchanged_and_carry_no_panel():
    owner, sid = _elec("deny")
    other, _aid = _client_for("s28t1-mref-other@example.com")
    for client in (other,):
        r = client.get(PAGE % sid)
        assert r.status_code != 200 and "data-measurement-reference" not in r.get_data(as_text=True)


def test_viewing_the_page_writes_nothing():
    client, sid = _elec("nowrite")
    before = (_dump(), pickle.dumps(webapp.SESSION_STORE[sid]["state"]))
    for _ in range(2):
        assert _panel(_page(client, sid)[1]) is not None
    assert (_dump(), pickle.dumps(webapp.SESSION_STORE[sid]["state"])) == before
