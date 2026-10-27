# -*- coding: utf-8 -*-
"""MEASUREMENT-PLANNING-INTEGRATED-PART-01 — the three existing, read-only
Electronics measurement-planning elements of the CAP-09 planning page for the
declared Electrical / Electronics part of a valid integrated composition
(Owner-authorized).

The C1 quantity-versus-condition guidance (PR #817), the conditions-of-use
awareness (PR #822) and the collapsed Sensors / Instrumentation reference panel
(PR #816) are shown, unchanged, for an Electronics-root project exactly as
before AND for the inventor-declared Electrical / Electronics part of a valid
durable integrated Mechanical + Electrical / Electronics composition, whatever
the initial analysis focus. Eligibility is ONE decision
(``_measurement_planning_domain``) read once per render from the current
durable state through the existing validated composition reader
(``_calc_declared_part``); nothing is taken from the request, and a withdrawn,
replaced, corrupt or unreadable composition grants nothing. When the elements
are shown for the declared part, ONE EN / AR line names that part (escaped,
direction-auto isolated) and states that this says nothing about any
experiment, sensing need or technical assessment. No claim, source, group,
input, persistence, report, PDF or export change. Synthetic data only.
"""
import html
import os
import pickle
import re
import sqlite3

import pytest

import web.app as webapp
from web import cap01_guidance, ui_text
from tests.measurement_planning_integrated_part_amendment import (
    AMENDED_NOTES, AMENDMENT, ANCHOR)
from tests.test_cap12_form_mockup_advisory import _client_for, _new_client
from tests.test_cap13_therm01_integrated_part_eligibility import (
    _integrated, _corrupt, MECH, ELEC, PARTS, CTRL, HOSTILE)
from tests.test_28t1_measurement_planning_reference import (
    PAGE, _panel, _start, _page)
from tests.test_stage19_durable_success_criteria import (
    ELEC_ANSWERS, ELEC_IDEA, MECH_ANSWERS, MECH_IDEA, PREFIX, _answer)

GUIDANCE = "data-measurement-guidance="
CONDITIONS = "data-measurement-conditions="
PANEL = "data-measurement-reference"
PART = "data-mguide-part>"
ELEC_NAME = PARTS["elec_part_name"]


def _client(tag):
    client, _aid = _client_for("mplan-int-%s@example.com" % tag)
    return client


def _part_name(body):
    marker = "data-mguide-part-name>"
    if marker not in body:
        return None
    return body.split(marker, 1)[1].split("</bdi>", 1)[0]


def _shown(body):
    """(guidance, conditions, panel, part line) presence on a planning page."""
    return (GUIDANCE in body, CONDITIONS in body, _panel(body) is not None, PART in body)


def _dump():
    with sqlite3.connect(os.environ["INVENTORAI_DB_PATH"]) as connection:
        return list(connection.iterdump())


def _eid(body):
    return re.search(r'name="%s([^"]+)"' % re.escape(PREFIX), body).group(1)


# ==========================================================================
# 1. root behaviour is unchanged
# ==========================================================================
def test_an_electronics_root_project_is_unchanged_and_names_no_part():
    c = _client("root-elec")
    sid = _start(c, ELEC_IDEA, ELEC, ELEC_ANSWERS)
    assert webapp._measurement_planning_domain(sid) == (ELEC, None)
    status, body = _page(c, sid)
    assert status == 200 and _shown(body) == (True, True, True, False)
    assert webapp._measurement_planning_view(sid) == {
        "references": cap01_guidance.measurement_planning_references(ELEC),
        "guidance": cap01_guidance.measurement_planning_guidance(ELEC),
        "conditions": cap01_guidance.measurement_planning_conditions(ELEC),
        "part_name": None}


def test_a_mechanical_only_project_shows_nothing():
    c = _client("root-mech")
    sid = _start(c, MECH_IDEA, MECH, MECH_ANSWERS)
    assert webapp._measurement_planning_domain(sid) == (MECH, None)
    status, body = _page(c, sid)
    assert status == 200 and 'action="/session/%s/success-criteria"' % sid in body
    assert _shown(body) == (False, False, False, False)
    assert set(webapp._measurement_planning_view(sid).values()) == {None}


# ==========================================================================
# 2. the declared Electrical / Electronics part: both focus directions, three parts
# ==========================================================================
@pytest.mark.parametrize("focus,extra", [(MECH, {}), (ELEC, {}), (MECH, CTRL), (ELEC, CTRL)],
                         ids=["mech-focus", "elec-focus", "mech-focus-3", "elec-focus-3"])
def test_a_valid_integrated_project_shows_all_three_elements(focus, extra):
    c = _client("part-%s-%d" % (focus[:4], len(extra)))
    sid = _integrated(c, focus, **extra)
    domain, part = webapp._measurement_planning_domain(sid)
    assert domain == ELEC
    status, body = _page(c, sid)
    assert status == 200
    if focus == ELEC:
        # the root rule applies as before: no attribution
        assert part is None and _shown(body) == (True, True, True, False)
        return
    assert part.domain == ELEC and part.display_name == ELEC_NAME
    assert _shown(body) == (True, True, True, True)
    assert _part_name(body) == ELEC_NAME
    # the attribution line precedes the elements it explains, in the established order
    order = [body.index(m) for m in (PART, GUIDANCE, CONDITIONS, 'class="measurement-reference"')]
    assert order == sorted(order)
    # the same groups, claims and copy keys as on an Electronics root
    view = webapp._measurement_planning_view(sid)
    assert view["references"] == cap01_guidance.measurement_planning_references(ELEC)
    assert view["guidance"] == cap01_guidance.measurement_planning_guidance(ELEC)
    assert view["conditions"] == cap01_guidance.measurement_planning_conditions(ELEC)
    assert view["part_name"] == ELEC_NAME


def test_the_elements_are_identical_to_the_electronics_root():
    c = _client("same")
    root = _start(c, ELEC_IDEA, ELEC, ELEC_ANSWERS)
    part = _integrated(c, MECH)

    def blocks(body):
        out = []
        for cls in ("measurement-guidance", "measurement-conditions"):
            m = re.search(r'<section class="%s".*?</section>' % cls, body, re.S)
            out.append(m.group(0))
        out.append(_panel(body))
        return out
    assert blocks(_page(c, root)[1]) == blocks(_page(c, part)[1])


# ==========================================================================
# 3. stale, withdrawn, replaced, corrupt and unreadable compositions fail closed
# ==========================================================================
@pytest.mark.parametrize("sql", (
    "UPDATE project_subsystems SET domain = 'software' WHERE domain = 'electronics_electrical'",
    "DELETE FROM project_subsystems WHERE domain = 'electronics_electrical'",
    "DELETE FROM project_subsystems",
    "UPDATE project_subsystems SET display_name = ' padded' WHERE domain = 'electronics_electrical'",
    "UPDATE project_subsystems SET subsystem_seq = 7 WHERE subsystem_seq = 1",
), ids=["replaced-domain", "withdrawn-part", "withdrawn-all", "corrupt-name", "corrupt-seq"])
def test_a_changed_composition_grants_nothing_on_the_next_render(sql):
    c = _client("stale-%d" % (abs(hash(sql)) % 10000))
    sid = _integrated(c, MECH)
    assert _shown(_page(c, sid)[1]) == (True, True, True, True)   # rendered while eligible
    _corrupt(sql)
    assert webapp._measurement_planning_domain(sid) == (MECH, None)
    assert set(webapp._measurement_planning_view(sid).values()) == {None}
    status, body = _page(c, sid)
    assert _shown(body) == (False, False, False, False)
    assert ELEC_NAME not in body or status != 200


def test_an_unreadable_composition_or_root_fails_closed(monkeypatch):
    c = _client("unreadable")
    sid = _integrated(c, MECH)
    store = webapp._get_store()

    def broken(*_a, **_k):
        raise OSError("disk I/O error")
    monkeypatch.setattr(store, "load_project_subsystems", broken)
    assert set(webapp._measurement_planning_view(sid).values()) == {None}
    _status, body = _page(c, sid)        # the page itself may be unavailable then
    assert _shown(body) == (False, False, False, False) and ELEC_NAME not in body
    monkeypatch.undo()
    # an unreadable root that READS as absent: the validated composition still holds the part
    monkeypatch.setattr(webapp, "_cap12_root_domain", lambda _sid: None)
    assert webapp._measurement_planning_domain(sid)[1].display_name == ELEC_NAME
    monkeypatch.undo()
    # a root read that RAISES: nothing at all, and the page still works
    monkeypatch.setattr(webapp, "_cap12_root_domain", broken)
    assert set(webapp._measurement_planning_view(sid).values()) == {None}
    status, body = _page(c, sid)
    assert status == 200 and _shown(body) == (False, False, False, False)
    # an accessor failure shows nothing either, never a partial set
    monkeypatch.undo()
    monkeypatch.setattr(cap01_guidance, "measurement_planning_conditions", broken)
    assert set(webapp._measurement_planning_view(sid).values()) == {None}


def test_eligibility_follows_the_current_state_on_every_render(monkeypatch):
    c = _client("current")
    sid = _integrated(c, MECH)
    store = webapp._get_store()
    real = store.load_project_subsystems
    assert _shown(_page(c, sid)[1]) == (True, True, True, True)
    monkeypatch.setattr(store, "load_project_subsystems", lambda s: tuple(
        sub for sub in real(s) if sub.domain != ELEC))
    assert _shown(_page(c, sid)[1]) == (False, False, False, False)
    monkeypatch.setattr(store, "load_project_subsystems", real)
    assert _shown(_page(c, sid)[1]) == (True, True, True, True)


def test_the_view_reads_the_composition_once_per_render(monkeypatch):
    c = _client("once")
    sid = _integrated(c, MECH)
    store = webapp._get_store()
    real = store.load_project_subsystems
    reads = []

    def counting(s):
        reads.append(s)
        return real(s)
    monkeypatch.setattr(store, "load_project_subsystems", counting)
    webapp._measurement_planning_view(sid)
    assert len(reads) == 1


# ==========================================================================
# 4. nothing from the request grants eligibility; denials and authorization
# ==========================================================================
def test_request_supplied_domain_or_part_never_grants_eligibility():
    c = _client("request")
    mech = _start(c, MECH_IDEA, MECH, MECH_ANSWERS)
    part_sid = _integrated(c, MECH)
    part_id = webapp._measurement_planning_domain(part_sid)[1].subsystem_id
    query = "?domain=%s&root_domain=%s&part_id=%s&measurement_part_name=x" % (ELEC, ELEC, part_id)
    body = c.get((PAGE % mech) + query).get_data(as_text=True)
    assert _shown(body) == (False, False, False, False)
    eid = _eid(_page(c, mech)[1])
    for extra in ({"domain": ELEC}, {"part_id": part_id}, {"subsystem_id": part_id},
                  {"measurement_part_name": ELEC_NAME}):
        data = dict({PREFIX + eid: "x" * (webapp.MAX_CRITERION_LENGTH + 1)}, **extra)
        r = c.post(PAGE % mech, data=data)
        assert r.status_code == 400
        assert _shown(r.get_data(as_text=True)) == (False, False, False, False)


def test_denials_carry_no_element_or_part_name():
    c = _client("deny")
    sid = _integrated(c, MECH)
    other = _client("deny-other")
    for client in (other, _new_client()):
        r = client.get(PAGE % sid)
        body = r.get_data(as_text=True)
        assert r.status_code != 200 and ELEC_NAME not in body
        assert _shown(body) == (False, False, False, False)


def test_an_unavailable_page_shows_nothing(monkeypatch):
    c = _client("unavailable")
    sid = _integrated(c, MECH)

    def boom(*_a, **_k):
        raise RuntimeError("no reconstruction")
    monkeypatch.setattr(webapp, "reconstruct_readonly_state", boom)
    status, body = _page(c, sid)
    assert status == 503 and _shown(body) == (False, False, False, False)


# ==========================================================================
# 5. CAP-09 saving and its POST are unchanged; viewing writes nothing
# ==========================================================================
def test_cap09_saving_is_unchanged_on_the_integrated_part():
    c = _client("save")
    sid = _integrated(c, MECH)
    for text in MECH_ANSWERS:
        _answer(c, sid, text)
    eid = _eid(_page(c, sid)[1])
    r = c.post(PAGE % sid, data={PREFIX + eid: "The motor stops within two seconds"})
    assert r.status_code == 302
    status, body = _page(c, sid)
    assert status == 200 and "The motor stops within two seconds" in html.unescape(body)
    assert _shown(body) == (True, True, True, True)
    # a refused POST re-renders with the same rule, the draft kept and unsaved
    r = c.post(PAGE % sid, data={PREFIX + eid: "x" * (webapp.MAX_CRITERION_LENGTH + 1)})
    refused = r.get_data(as_text=True)
    assert r.status_code == 400 and 'id="draft-unsaved"' in refused
    assert _shown(refused) == (True, True, True, True) and _part_name(refused) == ELEC_NAME


def test_viewing_the_page_writes_nothing():
    c = _client("nowrite")
    sid = _integrated(c, MECH)
    before = (_dump(), pickle.dumps(webapp.SESSION_STORE[sid]["state"]))
    for _ in range(2):
        assert _shown(_page(c, sid)[1]) == (True, True, True, True)
    assert (_dump(), pickle.dumps(webapp.SESSION_STORE[sid]["state"])) == before


def test_the_report_and_pdf_sources_are_unchanged():
    c = _client("report")
    sid = _integrated(c, MECH)
    report = c.get("/session/%s/deliverable" % sid).get_data(as_text=True)
    assert "data-mguide-part" not in report
    assert GUIDANCE not in report and CONDITIONS not in report
    source = open("web/templates/success_criteria.html", encoding="utf-8").read()
    assert source.count("measurement_part_name") == 2
    for other in os.listdir("web/templates"):
        if other != "success_criteria.html":
            text = open(os.path.join("web/templates", other), encoding="utf-8").read()
            assert "UI_SC_MGUIDE_PART_" not in text and "measurement_part_name" not in text


# ==========================================================================
# 6. EN / AR attribution: escaped, direction-isolated, no experiment claim
# ==========================================================================
def _text(page):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", page)))


@pytest.mark.parametrize("lang", ("en", "ar"))
def test_the_attribution_is_escaped_isolated_and_bilingual(lang):
    c = _client("attr-%s" % lang)
    sid = _integrated(c, MECH, elec_part_name=HOSTILE)
    if lang == "ar":
        assert c.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    body = _page(c, sid)[1]
    assert "<script>alert" not in body
    assert html.unescape(_part_name(body)) == HOSTILE
    assert '<bdi dir="auto" data-mguide-part-name>' in body
    text = _text(body)
    for key in ("UI_SC_MGUIDE_PART_LABEL", "UI_SC_MGUIDE_PART_NOTE"):
        assert re.sub(r"\s+", " ", ui_text.text(key, lang)) in text, (key, lang)
    if lang == "ar":
        assert 'dir="rtl"' in body


def test_the_copy_makes_no_experiment_sensing_or_assessment_claim():
    en = ui_text.text("UI_SC_MGUIDE_PART_NOTE", "en")
    assert "does not mean that any experiment below is electronic" in en
    assert "needs sensing" in en and "technically assessed" in en
    ar = ui_text.text("UI_SC_MGUIDE_PART_NOTE", "ar")
    assert "لا تعني" in ar and "إلكترونية" in ar and "استشعار" in ar and "قُيِّمت تقنيًا" in ar
    assert "Electrical / Electronics part" in ui_text.text("UI_SC_MGUIDE_PART_LABEL", "en")
    assert "الكهربائي/الإلكتروني" in ui_text.text("UI_SC_MGUIDE_PART_LABEL", "ar")
    for lang in ("en", "ar"):
        for key in ("UI_SC_MGUIDE_PART_LABEL", "UI_SC_MGUIDE_PART_NOTE"):
            value = ui_text.text(key, lang)
            for word in ("instrument", "sensor", "calibrat", "accura", "safe", "valid"):
                assert word not in value.lower(), (key, lang, word)


# ==========================================================================
# 7. scope records: the Stage 15 exception and the two amended pack notes only
# ==========================================================================
def test_the_stage15_exception_and_scope_records_name_the_amendment():
    model = re.sub(r"\s+", " ", open("engine/subsystem_model.py", encoding="utf-8").read())
    assert "MEASUREMENT-PLANNING-INTEGRATED-PART-01" in model
    exception = model[model.index("MEASUREMENT-PLANNING-INTEGRATED-PART-01"):]
    exception = exception[:exception.index("No other specialist behaviour is granted")]
    assert "measurement-planning guidance elements of the CAP-09 planning page" in exception
    assert "whatever the initial analysis focus" in exception
    import json
    notes = json.load(open("domains/electronics_electrical/domain.json",
                           encoding="utf-8"))["_governance_notes"]
    for key, value in notes.items():
        assert (AMENDMENT in value) is (key in AMENDED_NOTES), key
    for key in AMENDED_NOTES:
        assert notes[key].count(ANCHOR + AMENDMENT) == 1
    guidance = open("web/cap01_guidance.py", encoding="utf-8").read()
    assert guidance.count("MEASUREMENT-PLANNING-INTEGRATED-PART-01") == 2
    # the accessors keep their own exact-domain rule
    for accessor in (cap01_guidance.measurement_planning_references,
                     cap01_guidance.measurement_planning_guidance,
                     cap01_guidance.measurement_planning_conditions):
        assert accessor(ELEC) is not None
        for other in (MECH, "control_loop", None, ""):
            assert accessor(other) is None
