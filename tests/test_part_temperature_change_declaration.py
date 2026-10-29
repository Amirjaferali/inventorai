# -*- coding: utf-8 -*-
"""PART-BOUND-TEMPERATURE-CHANGE-DECLARATION-01 (Increment A) — directly owning tests.

The inventor's own statement that the ONE Mechanical part of a valid durable
Stage-15 composition experiences a temperature change during use: semantics in
``engine/subsystem_model.py``, one presence-only current-value sidecar
``subsystem_temperature_change_declarations`` in the record store, one POST route
and one block in the session page's integrated-scope section.

Proven here: exact ``(project_id, subsystem_id)`` binding (never a component id,
another project's part, a non-Mechanical part, a name or a position); declare /
withdraw lifecycle with stale-form refusal and exact retries that write nothing;
NOT DECLARED for every project without a statement (no migration invents one);
fail-closed corruption; durable reload; no Stage-15 part is edited, replaced or
rebound; and NO consumer reads the statement (calculation gates, the functional
handoff, the Compass, IdeaState, readiness and SafetySignal are unchanged).
Synthetic data only.
"""
import html
import os
import pickle
import re
import sqlite3
from pathlib import Path

import pytest

import web.app as webapp
from web import ui_text
from engine import record_store as rs
from engine import subsystem_model as sm
from tests.test_cap12_form_mockup_advisory import (
    _client_for, _new_client, _start, _page, SEED, ELEC_FORM)
from tests.test_cap13_therm01_integrated_part_eligibility import (
    _integrated, MECH, ELEC, PARTS, CTRL, HOSTILE)

ROOT = Path(__file__).resolve().parent.parent
URL = "/session/%s/part-temperature-change"
TABLE = "subsystem_temperature_change_declarations"


def _db():
    return os.environ["INVENTORAI_DB_PATH"]


def _sql(statement, params=(), foreign_keys=True):
    with sqlite3.connect(_db()) as connection:
        if not foreign_keys:
            connection.execute("PRAGMA foreign_keys = OFF")
        return connection.execute(statement, params).fetchall()


def _parts(sid):
    return {sub.domain: sub.subsystem_id
            for sub in webapp._get_store().load_project_subsystems(sid)}


def _declare(c, sid, part_id, base="not_declared", confirm=True, **extra):
    data = {"subsystem_id": part_id, "tc_action": "declare", "tc_base": base}
    if confirm:
        data["tc_confirm"] = "yes"
    data.update(extra)
    return c.post(URL % sid, data=data)


def _withdraw(c, sid, part_id, base="declared"):
    return c.post(URL % sid, data={"subsystem_id": part_id, "tc_action": "withdraw",
                                   "tc_base": base})


def _state(c, sid):
    """The session page's statement block: its status and state markers."""
    body = _page(c, sid)
    match = re.search(r'<dd[^>]*data-part-tc="([a-z]+)".*?</dd>', body, re.S)
    if match is None:
        return None, body
    block = match.group(0)
    state = re.search(r'data-part-tc-state="([a-z_]+)"', block)
    return (match.group(1), state.group(1) if state else None), body


def _rows():
    return _sql("SELECT project_id, subsystem_id FROM %s ORDER BY project_id" % TABLE)


def _subsystem_rows():
    return _sql("SELECT * FROM project_subsystems ORDER BY project_id, subsystem_seq")


@pytest.fixture
def integrated():
    c, _aid = _client_for("ptc-integrated@example.com")
    sid = _integrated(c, ELEC)
    return c, sid


# ==========================================================================
# 1. the semantic owner
# ==========================================================================
def _composition():
    mech = sm.declared_subsystem(MECH, "Hinge", "Swings the window")
    elec = sm.declared_subsystem(ELEC, "Driver", "Switches power")
    return sm.validate_composition((mech, elec), ELEC), mech, elec


def test_target_is_only_the_mechanical_part_by_exact_identity():
    composition, mech, elec = _composition()
    assert sm.part_temperature_change_target(composition, mech.subsystem_id) is mech
    for bad in (elec.subsystem_id, sm.new_subsystem_id(), "sub-" + "0" * 32, "",
                None, mech.display_name, "mechanical", 0,
                "12345678-1234-1234-1234-123456789abc"):    # a component-id shape
        with pytest.raises(sm.PartTemperatureChangeError):
            sm.part_temperature_change_target(composition, bad)
    with pytest.raises(sm.PartTemperatureChangeError):
        sm.part_temperature_change_target((), mech.subsystem_id)


def test_validation_is_whole_and_never_rebinds():
    composition, mech, elec = _composition()
    one = sm.PartTemperatureChangeDeclaration(mech.subsystem_id)
    assert sm.validate_part_temperature_changes((one,), composition) == (one,)
    assert sm.validate_part_temperature_changes((), composition) == ()
    for items in ((one, one), (sm.PartTemperatureChangeDeclaration(elec.subsystem_id),),
                  (sm.PartTemperatureChangeDeclaration(sm.new_subsystem_id()),),
                  (sm.PartTemperatureChangeDeclaration(mech.subsystem_id, provenance="X"),),
                  (sm.PartTemperatureChangeDeclaration(mech.subsystem_id,
                                                       validation_state="VALIDATED"),),
                  ("not a declaration",)):
        with pytest.raises(sm.PartTemperatureChangeError):
            sm.validate_part_temperature_changes(items, composition)
    assert one.provenance == "OWNER_STATED" and one.validation_state == "UNVALIDATED"
    assert sm.part_temperature_change_declared((one,), mech.subsystem_id) is True
    assert sm.part_temperature_change_declared((), mech.subsystem_id) is False
    assert sm.PART_TEMPERATURE_CHANGE_DOMAINS == ("mechanical",)


# ==========================================================================
# 2. the store: binding, isolation, lifecycle, legacy, corruption, reload
# ==========================================================================
def test_declare_withdraw_lifecycle_and_exact_retries(integrated):
    _c, sid = integrated
    store = webapp._get_store()
    mech = _parts(sid)[MECH]
    before = _subsystem_rows()
    assert store.load_part_temperature_changes(sid)[1] == ()
    assert store.set_part_temperature_change(sid, mech, True, False) \
        == rs.PART_TEMPERATURE_CHANGE_DECLARED
    (declaration,) = store.load_part_temperature_changes(sid)[1]
    assert declaration.subsystem_id == mech
    # an exact retry writes nothing
    assert store.set_part_temperature_change(sid, mech, True, False) \
        == rs.PART_TEMPERATURE_CHANGE_UNCHANGED
    assert _rows() == [(sid, mech)]
    # a stale form never overwrites newer truth
    with pytest.raises(rs.PartTemperatureChangeStale):
        store.set_part_temperature_change(sid, mech, False, False)
    assert store.set_part_temperature_change(sid, mech, False, True) \
        == rs.PART_TEMPERATURE_CHANGE_WITHDRAWN
    assert store.load_part_temperature_changes(sid)[1] == () and _rows() == []
    assert store.set_part_temperature_change(sid, mech, False, True) \
        == rs.PART_TEMPERATURE_CHANGE_UNCHANGED
    # the Stage-15 part rows are never edited, replaced or withdrawn
    assert _subsystem_rows() == before
    # the same exact part identity is re-declared, never another one
    store.set_part_temperature_change(sid, mech, True, False)
    assert _rows() == [(sid, mech)] and _subsystem_rows() == before


def test_binding_rejects_other_projects_parts_components_and_non_mechanical_parts():
    c, _aid = _client_for("ptc-binding@example.com")
    a = _integrated(c, ELEC)
    b = _integrated(c, MECH)
    store = webapp._get_store()
    for target in (_parts(b)[MECH], _parts(a)[ELEC], sm.new_subsystem_id(),
                   "12345678-1234-1234-1234-123456789abc", "", "sub-zz"):
        with pytest.raises(rs.PartTemperatureChangeRejected):
            store.set_part_temperature_change(a, target, True, False)
    for bad in (("yes", False), (True, None), (1, 0)):
        with pytest.raises(rs.PartTemperatureChangeRejected):
            store.set_part_temperature_change(a, _parts(a)[MECH], *bad)
    with pytest.raises(rs.ProjectNotFound):
        store.set_part_temperature_change("nope", _parts(a)[MECH], True, False)
    assert _rows() == []
    store.set_part_temperature_change(a, _parts(a)[MECH], True, False)
    assert store.load_part_temperature_changes(b)[1] == ()     # project isolation
    assert _rows() == [(a, _parts(a)[MECH])]


def test_projects_without_stage15_parts_admit_nothing():
    c, _aid = _client_for("ptc-single@example.com")
    sid = _start(c, {"idea": SEED, "domain_confirm": MECH})
    store = webapp._get_store()
    assert store.load_part_temperature_changes(sid) == ((), ())
    with pytest.raises(rs.PartTemperatureChangeRejected):
        store.set_part_temperature_change(sid, sm.new_subsystem_id(), True, False)
    assert _rows() == [] and _sql(
        "SELECT COUNT(*) FROM project_subsystems WHERE project_id = ?", (sid,)) == [(0,)]
    page = _page(c, sid)
    assert "data-part-tc" not in page                     # nothing is shown


def test_durable_reload_and_a_fresh_store_see_the_same_truth(integrated):
    _c, sid = integrated
    mech = _parts(sid)[MECH]
    webapp._get_store().set_part_temperature_change(sid, mech, True, False)
    fresh = rs.SqliteRecordStore(_db(), create=False)
    assert [d.subsystem_id for d in fresh.load_part_temperature_changes(sid)[1]] == [mech]
    fresh.set_part_temperature_change(sid, mech, False, True)
    again = rs.SqliteRecordStore(_db(), create=False)
    assert again.load_part_temperature_changes(sid)[1] == ()


def test_legacy_database_migrates_additively_and_reads_not_declared(integrated):
    c, sid = integrated
    # a pre-increment database: the sidecar does not exist yet
    _sql("DROP TABLE %s" % TABLE)
    before = _subsystem_rows()
    reopened = rs.SqliteRecordStore(_db(), create=False)
    assert reopened.load_part_temperature_changes(sid)[1] == ()
    assert _rows() == [] and _subsystem_rows() == before
    assert [r[1] for r in _sql("PRAGMA table_info(%s)" % TABLE)] == [
        "project_id", "subsystem_id"]


def test_unknown_table_shape_is_refused_never_read_as_empty(integrated):
    _sql("DROP TABLE %s" % TABLE)
    _sql("CREATE TABLE %s (project_id TEXT, subsystem_id TEXT, extra TEXT)" % TABLE)
    with pytest.raises(sqlite3.DatabaseError):
        rs.SqliteRecordStore(_db(), create=False)


@pytest.mark.parametrize("corrupt", ["elec_part", "orphan", "cross_project"])
def test_corrupt_stored_statements_fail_closed(corrupt):
    c, _aid = _client_for("ptc-corrupt-%s@example.com" % corrupt)
    a = _integrated(c, ELEC)
    b = _integrated(c, ELEC)
    target = {"elec_part": _parts(a)[ELEC], "orphan": sm.new_subsystem_id(),
              "cross_project": _parts(b)[MECH]}[corrupt]
    _sql("INSERT INTO %s (project_id, subsystem_id) VALUES (?, ?)" % TABLE,
         (a, target), foreign_keys=False)
    store = webapp._get_store()
    with pytest.raises(rs.PartTemperatureChangesCorrupt):
        store.load_part_temperature_changes(a)
    with pytest.raises(rs.PartTemperatureChangesCorrupt):
        store.set_part_temperature_change(a, _parts(a)[MECH], True, False)
    status, _body = _state(c, a)
    assert status == ("unavailable", None)            # never NOT DECLARED
    r = _declare(c, a, _parts(a)[MECH])
    assert r.status_code == 302
    page = _page(c, a)
    assert ui_text.text("UI_PTC_MSG_NOT_SAVED", "en") in html.unescape(page)
    assert "data-part-tc-form" not in page
    assert store.load_part_temperature_changes(b)[1] == ()     # b unaffected


def test_corrupt_composition_exposes_no_statement(integrated):
    c, sid = integrated
    webapp._get_store().set_part_temperature_change(sid, _parts(sid)[MECH], True, False)
    _sql("UPDATE project_subsystems SET domain = 'software' WHERE project_id = ? "
         "AND subsystem_seq = 0", (sid,))
    with pytest.raises(rs.ProjectSubsystemsCorrupt):
        webapp._get_store().load_part_temperature_changes(sid)
    # the session page itself fails closed on a corrupt composition (existing
    # behaviour); whatever is served never presents the statement as current
    r = c.get("/session/%s" % sid)
    assert 'data-part-tc-state="declared"' not in r.get_data(as_text=True)


def test_database_foreign_key_refuses_a_part_of_another_project():
    c, _aid = _client_for("ptc-fk@example.com")
    a = _integrated(c, ELEC)
    b = _integrated(c, ELEC)
    with pytest.raises(sqlite3.IntegrityError):
        with sqlite3.connect(_db()) as connection:
            connection.execute("PRAGMA foreign_keys = ON")
            connection.execute("INSERT INTO %s (project_id, subsystem_id) VALUES (?, ?)"
                               % TABLE, (a, _parts(b)[MECH]))


# ==========================================================================
# 3. the route and the session page
# ==========================================================================
def test_session_page_shows_not_declared_and_declares_with_confirmation(integrated):
    c, sid = integrated
    mech = _parts(sid)[MECH]
    status, body = _state(c, sid)
    assert status == ("ok", "not_declared")
    assert ui_text.text("UI_PTC_STATUS_NOT_DECLARED", "en") in html.unescape(body)
    assert 'name="subsystem_id" value="%s"' % mech in body
    assert ">%s<" % mech not in body                          # never visible text
    assert not re.search(r'name="tc_confirm"[^>]*checked', body)
    # without the explicit confirmation nothing is recorded
    _declare(c, sid, mech, confirm=False)
    assert _rows() == []
    assert ui_text.text("UI_PTC_MSG_CONFIRM_REQUIRED", "en") in html.unescape(_page(c, sid))
    r = _declare(c, sid, mech)
    assert r.status_code == 302 and r.headers["Location"].endswith("#integrated-scope")
    status, body = _state(c, sid)
    assert status == ("ok", "declared")
    text = html.unescape(body)
    assert ui_text.text("UI_PTC_MSG_DECLARED", "en") in text
    assert ui_text.text("UI_PTC_STATUS_DECLARED", "en") in text
    assert "OWNER_STATED" in text and "UNVALIDATED" in text
    _withdraw(c, sid, mech)
    status, body = _state(c, sid)
    assert status == ("ok", "not_declared") and _rows() == []
    assert ui_text.text("UI_PTC_MSG_WITHDRAWN", "en") in html.unescape(body)


def test_route_refuses_malformed_foreign_and_stale_requests(integrated):
    c, sid = integrated
    mech = _parts(sid)[MECH]
    other_c, _aid = _client_for("ptc-route-other@example.com")
    other = _integrated(other_c, ELEC)
    rejected = ui_text.text("UI_PTC_MSG_REJECTED", "en")
    for data in ({"subsystem_id": _parts(other)[MECH]},
                 {"subsystem_id": _parts(sid)[ELEC]},
                 {"subsystem_id": "12345678-1234-1234-1234-123456789abc"},
                 {"subsystem_id": PARTS["mech_part_name"]},
                 {"tc_action": "correct"}, {"tc_base": "unknown"},
                 {"tc_confirm": "no"}):
        form = {"subsystem_id": mech, "tc_action": "declare", "tc_base": "not_declared",
                "tc_confirm": "yes"}
        form.update(data)
        c.post(URL % sid, data=form)
        assert rejected in html.unescape(_page(c, sid)), data
    assert _rows() == []
    from werkzeug.datastructures import MultiDict
    c.post(URL % sid, data=MultiDict([("subsystem_id", mech), ("subsystem_id", mech),
                                      ("tc_action", "declare"), ("tc_base", "not_declared"),
                                      ("tc_confirm", "yes")]))
    assert _rows() == []
    # a stale form (it showed "declared" while nothing is declared) writes nothing
    _withdraw(c, sid, mech, base="declared")
    assert _rows() == []
    _declare(c, sid, mech)
    _declare(c, sid, mech, base="declared")                  # no-op by the form
    assert ui_text.text("UI_PTC_MSG_UNCHANGED", "en") in html.unescape(_page(c, sid))
    _withdraw(c, sid, mech, base="not_declared")             # target == baseline
    assert _rows() == [(sid, mech)]


def test_csrf_and_authorization_are_enforced(integrated):
    c, sid = integrated
    mech = _parts(sid)[MECH]
    raw = webapp.app.test_client()
    assert raw.post(URL % sid, data={"subsystem_id": mech, "tc_action": "declare",
                                     "tc_base": "not_declared",
                                     "tc_confirm": "yes"}).status_code == 403
    other, _ = _client_for("ptc-intruder@example.com")
    for client in (other, _new_client()):
        r = _declare(client, sid, mech)
        assert r.status_code == 302 and "#integrated-scope" not in r.headers["Location"]
    assert _rows() == []


def test_three_part_composition_binds_only_the_mechanical_part():
    c, _aid = _client_for("ptc-three@example.com")
    sid = _integrated(c, ELEC, **CTRL)
    parts = _parts(sid)
    _declare(c, sid, parts[MECH])
    assert _rows() == [(sid, parts[MECH])]
    store = webapp._get_store()
    with pytest.raises(rs.PartTemperatureChangeRejected):
        store.set_part_temperature_change(sid, parts["control_loop"], True, False)


@pytest.mark.parametrize("lang", ("en", "ar"))
def test_bilingual_wording_and_hostile_part_names(lang):
    c, _aid = _client_for("ptc-lang-%s@example.com" % lang)
    sid = _integrated(c, ELEC, mech_part_name=HOSTILE)
    if lang == "ar":
        c.post("/ui-language", data={"lang": "ar"})
    _declare(c, sid, _parts(sid)[MECH])
    body = _page(c, sid)
    assert "<script>alert" not in body
    text = html.unescape(body)
    for key in ("UI_PTC_HEADING", "UI_PTC_STATUS_DECLARED", "UI_PTC_WITHDRAW",
                "UI_PTC_WITHDRAW_NOTE", "UI_PTC_NOTE", "UI_PTC_MSG_DECLARED"):
        assert ui_text.text(key, lang) in text, key
    if lang == "ar":
        assert 'dir="rtl"' in body


def test_wording_states_the_boundary_in_both_languages():
    keys = re.findall(r'"(UI_PTC_[A-Z_]+)": \{',
                      Path(ui_text.__file__).read_text(encoding="utf-8"))
    assert len(keys) == 17
    for key in keys:
        en, ar = ui_text.text(key, "en"), ui_text.text(key, "ar")
        assert en.strip() and ar.strip() and en != ar, key
    assert "does not mean that it does not" in ui_text.text("UI_PTC_STATUS_NOT_DECLARED", "en")
    assert "ولا يعني ذلك أنه لا يتعرض له" in ui_text.text("UI_PTC_STATUS_NOT_DECLARED", "ar")
    assert "does not mean that the part does not change temperature" \
        in ui_text.text("UI_PTC_WITHDRAW_NOTE", "en")
    assert "ولا يعني أن درجة حرارة الجزء لا تتغير" in ui_text.text("UI_PTC_WITHDRAW_NOTE", "ar")
    for key in ("UI_PTC_STATUS_DECLARED",):
        for lang in ("en", "ar"):
            assert "OWNER_STATED" in ui_text.text(key, lang)
            assert "UNVALIDATED" in ui_text.text(key, lang)
    english = " ".join(ui_text.text(k, "en") for k in keys).lower()
    for banned in ("thermal expansion", "recommended", "tool", "calculate", "applies to",
                   "you should", "use the", "has validated", "is validated", "verified"):
        assert banned not in english, banned


# ==========================================================================
# 4. NO consumer: Increment B and C are not implemented
# ==========================================================================
def _strip_volatile(page):
    page = re.sub(r'<dd[^>]*data-part-tc=.*?</dd>', "", page, flags=re.S)
    # per-render signed form tokens and nonces are volatile on every page
    page = re.sub(r'(<input[^>]*type="hidden"[^>]*?)value="[^"]*"', r'\1', page)
    page = re.sub(r'(<input[^>]*?)value="[^"]*"([^>]*type="hidden")', r'\1\2', page)
    return re.sub(r'nonce="[^"]*"', 'nonce', page)


def test_the_statement_changes_no_gate_handoff_compass_state_or_page_elsewhere(integrated):
    c, sid = integrated
    mech = _parts(sid)[MECH]
    gates = [webapp._mte, webapp._mnf, webapp._cap13, webapp._therm01]

    def observe():
        state = webapp.SESSION_STORE[sid]["state"]
        return ([webapp._calc_gate(sid, consumer)[0] for consumer in gates],
                webapp._functional_handoff_view(sid, state),
                pickle.dumps(state),
                _strip_volatile(_page(c, sid)))
    _page(c, sid)          # the first render's own lazy state update happens first
    before = observe()
    _declare(c, sid, mech)
    assert _rows() == [(sid, mech)]
    after = observe()
    assert after[0] == before[0]
    assert after[1] == before[1]
    assert after[2] == before[2]
    # MTE-TEMPERATURE-CHANGE-DISCOVERABILITY-01 (Increment C): the ONE expected
    # change elsewhere is that the existing free-expansion link moves next to
    # the statement; everything else on the page is unchanged.
    general = re.compile(r'<p class="journey-note" data-mte-link.*?</p>', re.S)
    assert general.search(before[3]) and not general.search(after[3])
    assert re.sub(r"\s+", " ", general.sub("", after[3])) == \
        re.sub(r"\s+", " ", general.sub("", before[3]))
    # the thermal-expansion page itself is unchanged by the statement
    page = c.get("/session/%s/thermal-expansion" % sid).get_data(as_text=True)
    assert "data-part-tc" not in page
    assert not re.search(r'name="value_[a-zA-Z_]+"[^>]*value="[^"]+"', page)


def test_only_the_store_and_the_session_surface_read_the_statement():
    readers = []
    for path in list((ROOT / "engine").glob("*.py")) + list((ROOT / "web").glob("*.py")):
        text = path.read_text(encoding="utf-8")
        if ("load_part_temperature_changes" in text or TABLE in text
                or "part_temperature_change_declared" in text):
            readers.append(path.name)
    assert sorted(readers) == ["app.py", "record_store.py", "subsystem_model.py"]
    app_source = (ROOT / "web" / "app.py").read_text(encoding="utf-8")
    assert app_source.count("load_part_temperature_changes") == 2   # context + reload
    for consumer in ("functional_need_handoff.py", "mechanical_thermal_expansion.py",
                     "safety_signal.py", "readiness_snapshot.py", "idea_state.py",
                     "progression_loop.py"):
        text = (ROOT / "engine" / consumer).read_text(encoding="utf-8")
        assert "temperature_change" not in text.lower(), consumer
    templates = [p.name for p in (ROOT / "web" / "templates").glob("*.html")
                 if "part_temperature_change" in p.read_text(encoding="utf-8")]
    assert templates == ["session.html"]


def test_no_subsystem_lifecycle_operation_was_added():
    source = (ROOT / "engine" / "record_store.py").read_text(encoding="utf-8")
    assert "UPDATE project_subsystems" not in source
    assert "DELETE FROM project_subsystems" not in source
    routes = [r.rule for r in webapp.app.url_map.iter_rules()
              if "part-temperature" in r.rule]
    assert routes == ["/session/<sid>/part-temperature-change"]
