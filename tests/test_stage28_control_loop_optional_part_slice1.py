"""Stage 28 — Control-Loop Optional Part — Slice 1 (part-eligibility seam + optional third-part composition, DORMANT).

The accepted bounded design makes ``control_loop`` an OPTIONAL composable part of a Mechanical + Electrical /
Electronics integrated invention — never a root-admissible domain. This slice ships only the dormant foundation:

  * a PART-ONLY eligibility allowlist in the canonical activation-policy owner, separate from root activation and
    shipped EMPTY (``control_loop`` is neither root-activated nor part-enabled);
  * the exact composition shape ``mechanical + electronics_electrical [+ optional control_loop]`` on the existing
    subsystem primitives and persistence (no schema change), with the scalar root focus never the optional part;
  * the bounded integrated-entry / composition-form / interface-pair changes, exercised here only through a
    test-only eligibility double.

AMENDED at the Owner-authorized Stage 28 part-only enablement: the shipped allowlist now lists exactly
``control_loop`` (still never root-activated), so the behavior tests run against the PRODUCTION policy and an
explicit empty override appears only where a test proves the withdrawn state.

Root classification, admission, progression and Path-N are untouched; nothing here serves a question or stores a
part answer.
"""
import ast
import html as _html
import os
import re
import sqlite3

import pytest

import web.app as appmod
from engine import domain_activation
from engine import session_reconstruction as SR
from engine import subsystem_model as sm
from engine.domain_rules import DomainResultKind, classify_domain
from engine.idea_state import OWNER_STATED, UNVALIDATED
from engine.record_store import SqliteRecordStore
from tests.csrf_client import csrf_client
from tests.test_stage15_integrated_invention_entry import (
    ELEC, MECH, PARTS, TIE_IDEA, _compose, _contract, _created, _live, _pair, _ri, _scope_block, _visible)
from web import ui_text

CL = "control_loop"
CL_IDEA = "A closed loop heater that compares the room temperature with a setpoint and adjusts the manipulated variable"
CTRL = {"ctrl_part_name": "Thermostat logic", "ctrl_part_function": "Compares the temperature with the target"}
_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


@pytest.fixture
def client():
    appmod.app.config["TESTING"] = True
    with csrf_client(appmod.app) as c:
        yield c


@pytest.fixture
def part_eligible():
    """The PRODUCTION policy part-enables ``control_loop`` (Stage 28 part-only enablement) — no override: every
    test requesting this fixture runs the live path. (It was a test-only eligibility double while the allowlist
    shipped empty.)"""
    assert domain_activation.is_part_eligible(CL) is True


def _store():
    return appmod._get_store()


def _rows(sql, params=()):
    conn = sqlite3.connect(os.environ["INVENTORAI_DB_PATH"])
    try:
        return conn.execute(sql, params).fetchall()
    finally:
        conn.close()


def _project_count():
    _store()
    return _rows("SELECT COUNT(*) FROM projects")[0][0]


def _triple():
    mech, elec = _pair()
    return mech, elec, sm.declared_subsystem(CL, "Thermostat logic", "Compares the temperature with the target")


def _three_part_project(client, focus=MECH):
    sid = _created(_compose(client, TIE_IDEA, focus=focus, **CTRL))
    assert [s.domain for s in _live(sid).subsystems] == [MECH, ELEC, CL]
    return sid


def _bindings(raw):
    return [_html.unescape(v) for v in re.findall(r'type="radio" name="interface_binding" value="([^"]*)"', raw)]


def _form_value(raw, name):
    m = re.search(r'name="%s" value="([^"]*)"' % name, raw)
    return _html.unescape(m.group(1)) if m else None


def _declare(client, sid, binding, description):
    raw = client.get(f"/session/{sid}").get_data(as_text=True)
    data = {"answer_token": _form_value(raw, "answer_token"), "interface_binding": binding,
            "interface_submission": _form_value(raw, "interface_submission"),
            "interface_description": description, "interface_confirm": "yes"}
    return client.post(f"/session/{sid}/declare-interface", data=data)


# ======================================================================= A. part-eligibility seam

def test_the_part_only_allowlist_enables_exactly_control_loop():
    # AMENDED at the Stage 28 part-only enablement: the allowlist shipped empty; it now lists exactly one domain
    assert domain_activation._PART_ONLY_DOMAINS == frozenset({CL})
    tree = ast.parse(open(os.path.join(_ROOT, "engine", "domain_activation.py"), encoding="utf-8").read())
    assigned = [n.value for n in tree.body if isinstance(n, ast.Assign)
                and [t.id for t in n.targets if isinstance(t, ast.Name)] == ["_PART_ONLY_DOMAINS"]]
    assert len(assigned) == 1 and ast.unparse(assigned[0]) == "frozenset({'control_loop'})"
    assert domain_activation.is_part_eligible(CL) is True
    registry = domain_activation.load_registry(domain_activation._DEFAULT_DOMAINS_DIR)
    assert [d for d in sorted(registry) if domain_activation.is_part_eligible(d, registry)] == [CL]
    for other in (MECH, ELEC, "not_a_pack", None, ""):
        assert domain_activation.is_part_eligible(other) is False


def test_root_activation_is_unchanged_and_control_loop_is_not_root_activated():
    assert domain_activation._ACTIVATED_DOMAINS == frozenset({ELEC, MECH})
    assert domain_activation.activated_domains() == [ELEC, MECH]
    assert domain_activation.support_state(CL) == domain_activation.RECOGNIZED_NOT_ACTIVATED
    assert domain_activation.is_activated(CL) is False
    assert sm.COMPOSITION_DOMAINS == (MECH, ELEC)
    assert sm.OPTIONAL_COMPOSITION_DOMAINS == (CL,)


def test_part_eligibility_is_distinct_from_root_activation(part_eligible):
    assert domain_activation.is_part_eligible(CL) is True
    # part eligibility never touches the root activation answers
    assert domain_activation.support_state(CL) == domain_activation.RECOGNIZED_NOT_ACTIVATED
    assert domain_activation.is_activated(CL) is False
    assert domain_activation.activated_domains() == [ELEC, MECH]


def test_part_eligibility_requires_recognition_and_never_overlaps_root_activation(monkeypatch):
    monkeypatch.setattr(domain_activation, "_PART_ONLY_DOMAINS", frozenset({"not_a_pack", MECH}))
    assert domain_activation.is_part_eligible("not_a_pack") is False      # not registry-recognized
    assert domain_activation.is_part_eligible(MECH) is False              # root-activated: never part-only
    assert domain_activation.is_part_eligible(None) is False
    assert domain_activation.is_part_eligible("") is False
    assert domain_activation.is_part_eligible(ELEC) is False              # not listed


# ======================================================================= B. composition shape

def test_the_optional_third_part_shape_is_bounded_to_control_loop():
    mech, elec, ctrl = _triple()
    assert sm.validate_composition((mech, elec), MECH) == (mech, elec)
    assert sm.validate_composition((mech, elec, ctrl), MECH) == (mech, elec, ctrl)
    assert sm.validate_composition((mech, elec, ctrl), ELEC) == (mech, elec, ctrl)
    other = sm.declared_subsystem("software", "App", "Runs the app")
    bad = [
        ((mech, elec, ctrl), CL),                                   # the optional part is never the focus
        ((mech, elec, elec), MECH),                                 # third slot is control_loop only
        ((mech, elec, other), MECH),                                # no arbitrary domain
        ((mech, ctrl, elec), MECH),                                 # fixed order
        ((mech, ctrl), MECH),                                       # the required pair stays required
        ((mech, elec, ctrl, sm.declared_subsystem(CL, "x", "y")), MECH),   # at most one optional part
        ((mech, elec, sm.Subsystem(sm.new_subsystem_id(), CL, "x", "y", "SYSTEM_INFERRED", UNVALIDATED)), MECH),
        ((mech, elec, sm.Subsystem(mech.subsystem_id, CL, "x", "y", OWNER_STATED, UNVALIDATED)), MECH),
        ((mech, elec, sm.Subsystem(sm.new_subsystem_id(), CL, "x" * 81, "y", OWNER_STATED, UNVALIDATED)), MECH),
    ]
    for subs, focus in bad:
        with pytest.raises(sm.CompositionError):
            sm.validate_composition(subs, focus)


def test_three_part_composition_round_trips_through_the_existing_table(tmp_path):
    db = str(tmp_path / "s.db")
    store = SqliteRecordStore(db)
    subs = _triple()
    pid = store.create_project(_contract(), reconstruction_inputs=_ri(ELEC), subsystems=subs)
    assert store.load_project_subsystems(pid) == subs
    store.close()
    reopened = SqliteRecordStore(db)
    assert [s.domain for s in reopened.load_project_subsystems(pid)] == [MECH, ELEC, CL]
    reopened.close()
    conn = sqlite3.connect(db)
    try:
        cols = [r[1] for r in conn.execute("PRAGMA table_info(project_subsystems)")]
        rows = conn.execute("SELECT subsystem_seq, domain FROM project_subsystems ORDER BY subsystem_seq").fetchall()
    finally:
        conn.close()
    assert cols == ["project_id", "subsystem_seq", "subsystem_id", "domain", "display_name", "function_text",
                    "provenance", "validation_state"]
    assert rows == [(0, MECH), (1, ELEC), (2, CL)]


def test_the_store_never_accepts_the_optional_part_as_the_focus(tmp_path):
    store = SqliteRecordStore(str(tmp_path / "s.db"))
    with pytest.raises(Exception):
        store.create_project(_contract(), reconstruction_inputs=_ri(CL), subsystems=_triple())
    store.close()


# ======================================================================= C. integrated entry (live; withdrawn where stated)

def test_withdrawn_policy_form_offers_no_optional_slot_and_ignores_posted_values(client, monkeypatch):
    # AMENDED at the Stage 28 part-only enablement: the former shipped (empty) state is now an explicit withdrawal
    monkeypatch.setattr(domain_activation, "_PART_ONLY_DOMAINS", frozenset())
    raw = client.post("/start", data={"idea": TIE_IDEA}).get_data(as_text=True)
    assert "data-composition-form" in raw
    assert "data-optional-part" not in raw and "ctrl_part_name" not in raw
    assert ui_text.text("UI_S15_FOCUS_NOTE", "en") in _html.unescape(raw)
    sid = _created(_compose(client, TIE_IDEA, **CTRL))                    # forged optional values
    assert [s.domain for s in _live(sid).subsystems] == [MECH, ELEC]


def test_eligible_form_offers_the_optional_slot_but_never_as_the_focus(client, part_eligible):
    raw = client.post("/start", data={"idea": TIE_IDEA}).get_data(as_text=True)
    assert "data-optional-part" in raw and 'name="ctrl_part_name"' in raw and 'name="ctrl_part_function"' in raw
    focus_values = re.findall(r'name="initial_focus" value="([^"]+)"', raw)
    assert focus_values == [MECH, ELEC]
    text = _html.unescape(raw)
    assert ui_text.text("UI_S15_FOCUS_NOTE_OPTIONAL", "en") in text
    assert ui_text.text("UI_S15_NOTHING_SAVED_OPTIONAL", "en") in text


def test_eligible_entry_creates_the_three_part_project_with_a_required_focus(client, part_eligible):
    sid = _three_part_project(client, focus=ELEC)
    state = _live(sid)
    assert state.domain == ELEC
    ctrl = state.subsystems[2]
    assert (ctrl.domain, ctrl.display_name, ctrl.function_text) == (
        CL, CTRL["ctrl_part_name"], CTRL["ctrl_part_function"])
    assert (ctrl.provenance, ctrl.validation_state) == (OWNER_STATED, UNVALIDATED)
    assert sm.is_valid_subsystem_id(ctrl.subsystem_id)


def test_the_optional_slot_is_optional_and_all_or_nothing(client, part_eligible):
    sid = _created(_compose(client, TIE_IDEA))                            # left empty -> two parts
    assert [s.domain for s in _live(sid).subsystems] == [MECH, ELEC]
    before = _project_count()
    for partial in ({"ctrl_part_name": "Only a name"}, {"ctrl_part_function": "Only a function"}):
        resp = _compose(client, TIE_IDEA, **partial)
        assert resp.status_code == 400
        assert ui_text.text("UI_S15_ERR_OPTIONAL_FIELDS", "en") in _html.unescape(resp.get_data(as_text=True))
    resp = _compose(client, TIE_IDEA, ctrl_part_name="x" * 81, ctrl_part_function="y")
    assert resp.status_code == 400
    resp = _compose(client, TIE_IDEA, ctrl_part_name="Logic", ctrl_part_function="bad\x00text")
    assert resp.status_code == 400
    resp = _compose(client, TIE_IDEA, focus=CL, **CTRL)                   # forged focus
    assert resp.status_code == 400
    assert _project_count() == before


def test_a_single_control_loop_result_is_never_root_admission_nor_composes_when_withdrawn(client, monkeypatch):
    # AMENDED at the Stage 28 part-only enablement: the live policy's Case-B flow is pinned below; this keeps the
    # withdrawn policy's refusal (an explicit empty override) — root admission is refused either way
    monkeypatch.setattr(domain_activation, "_PART_ONLY_DOMAINS", frozenset())
    result = classify_domain(CL_IDEA)
    assert (result.kind, result.selected_domain) == (DomainResultKind.SINGLE, CL)
    before = _project_count()
    for data in ({"idea": CL_IDEA}, {"idea": CL_IDEA, "domain_confirm": CL},
                 {"idea": CL_IDEA, "integrated_invention": "yes"}):
        raw = client.post("/start", data=data).get_data(as_text=True)
        assert "data-composition-form" not in raw
    assert _project_count() == before


def test_single_control_loop_enters_only_the_declared_composition_flow_when_eligible(client, part_eligible):
    before = _project_count()
    for data in ({"idea": CL_IDEA}, {"idea": CL_IDEA, "domain_confirm": CL}):
        raw = client.post("/start", data=data).get_data(as_text=True)     # root admission: still refused
        assert "data-composition-form" not in raw
    assert _project_count() == before
    raw = client.post("/start", data={"idea": CL_IDEA, "integrated_invention": "yes"}).get_data(as_text=True)
    assert "data-composition-form" in raw and "data-optional-part" in raw
    assert _project_count() == before                                     # nothing created by the classifier
    assert 'value="Thermostat logic"' not in raw                         # never pre-filled
    sid = _created(_compose(client, CL_IDEA, focus=MECH, **CTRL))
    assert _live(sid).domain == MECH
    assert [s.domain for s in _live(sid).subsystems] == [MECH, ELEC, CL]


# ======================================================================= D. interfaces across three parts

def test_two_part_projects_keep_the_single_binding_form(client, part_eligible):
    sid = _created(_compose(client, TIE_IDEA))
    raw = client.get(f"/session/{sid}").get_data(as_text=True)
    assert "data-interface-pairs" not in raw and not _bindings(raw)
    assert re.search(r'<input type="hidden" name="interface_binding" value="[^"]+">', raw)


def test_three_part_projects_offer_every_pair_with_its_own_signed_binding(client, part_eligible):
    sid = _three_part_project(client)
    raw = client.get(f"/session/{sid}").get_data(as_text=True)
    assert "data-interface-pairs" in raw
    bindings = _bindings(raw)
    assert len(bindings) == 3
    token = _form_value(raw, "answer_token")
    pairs = [appmod._verified_s15_interface_binding(sid, token, b)[1] for b in bindings]
    mech, elec, ctrl = [s.subsystem_id for s in _live(sid).subsystems]
    assert pairs == [(mech, elec), (mech, ctrl), (elec, ctrl)]


def test_each_offered_pair_records_an_interface_through_the_existing_owner(client, part_eligible):
    sid = _three_part_project(client)
    mech, elec, ctrl = [s.subsystem_id for s in _live(sid).subsystems]
    for index, text in ((1, "The logic tells the arm when to move."), (2, "The board powers the logic.")):
        raw = client.get(f"/session/{sid}").get_data(as_text=True)
        assert _declare(client, sid, _bindings(raw)[index], text).status_code == 302
    rows = _rows("SELECT subsystem_a_id, subsystem_b_id, description FROM subsystem_interfaces "
                 "WHERE project_id = ? ORDER BY interface_seq", (sid,))
    assert rows == [(mech, ctrl, "The logic tells the arm when to move."),
                    (elec, ctrl, "The board powers the logic.")]
    stored = _store().load_subsystem_composition(sid)
    assert [s.domain for s in stored[0]] == [MECH, ELEC, CL] and len(stored[1]) == 2
    assert sm.MAX_SUBSYSTEM_INTERFACES_PER_PROJECT == 20


def _signed_binding(sid, token, ecv, pair):
    import base64
    import json
    payload = json.dumps({"k": appmod._S15_IFC_BINDING_KIND, "v": ecv, "p": list(pair)},
                         sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    body = base64.urlsafe_b64encode(payload.encode("ascii")).decode("ascii").rstrip("=")
    return body + "." + appmod._s15_interface_binding_sig(sid, token, ecv, list(pair))


def test_a_binding_for_a_pair_not_offered_records_nothing(client, part_eligible):
    sid = _three_part_project(client)
    two_part_sid = _created(_compose(client, TIE_IDEA))
    other = client.get(f"/session/{two_part_sid}").get_data(as_text=True)
    # another project's binding never verifies here
    assert _declare(client, sid, _form_value(other, "interface_binding"), "Forged pair.").status_code == 302
    # a correctly signed binding for a pair the form does not offer (reversed order) is stale
    raw = client.get(f"/session/{sid}").get_data(as_text=True)
    mech, _elec, ctrl = [s.subsystem_id for s in _live(sid).subsystems]
    reversed_pair = _signed_binding(sid, _form_value(raw, "answer_token"),
                                    _live(sid).engine_contract_version, (ctrl, mech))
    assert _declare(client, sid, reversed_pair, "Reversed pair.").status_code == 302
    assert appmod.SESSION_STORE[sid].get("_answer_error") == appmod.S15_INTERFACE_STALE_MESSAGE
    assert not _rows("SELECT * FROM subsystem_interfaces WHERE project_id = ?", (sid,))


def test_preparation_and_dependency_owners_accept_control_loop_interfaces(client, part_eligible):
    sid = _three_part_project(client)
    raw = client.get(f"/session/{sid}").get_data(as_text=True)
    assert _declare(client, sid, _bindings(raw)[1], "The logic tells the arm when to move.").status_code == 302
    interface = _live(sid).subsystem_interfaces[0]
    mech, _elec, ctrl = [s.subsystem_id for s in _live(sid).subsystems]
    dependency = sm.InterfaceDependency(interface.interface_id, sm.DEPENDENCY_ONE_WAY, mech, ctrl)
    _store().apply_interface_preparation_delta(
        sid, {interface.interface_id: {sm.PREPARATION_OPERATING_CONDITIONS: "Room temperature."}},
        {interface.interface_id: dependency})
    assert [p.operating_conditions for p in _store().load_interface_preparations(sid)] == ["Room temperature."]
    assert _store().load_interface_dependencies(sid) == (dependency,)
    page = client.get(f"/session/{sid}/interface-preparation")
    assert page.status_code == 200
    text = _html.unescape(page.get_data(as_text=True))
    assert ui_text.text("UI_S15_PREP_INTRO_3", "en") in text
    assert ui_text.text("UI_S15_IEV_INTRO_3", "en") in text
    assert ui_text.text("UI_S15_PREP_INTRO", "en") not in text


def test_cold_load_and_reconstruction_restore_the_three_parts(client, part_eligible):
    sid = _three_part_project(client)
    raw = client.get(f"/session/{sid}").get_data(as_text=True)
    assert _declare(client, sid, _bindings(raw)[2], "The board powers the logic.").status_code == 302
    sub_ids = [s.subsystem_id for s in _live(sid).subsystems]
    appmod.SESSION_STORE.clear()
    with appmod.app.test_request_context("/"):
        cold = appmod._cold_load_entry(sid)["state"]
    assert [s.subsystem_id for s in cold.subsystems] == sub_ids
    session = SR.reconstruct_readonly_state(_store(), sid)
    assert [s.subsystem_id for s in session.state.subsystems] == sub_ids
    assert session.state.domain == MECH


# ======================================================================= E. truthful current view

def test_three_part_scope_shows_the_optional_part_with_truthful_copy(client, part_eligible):
    sid = _three_part_project(client)
    for path in (f"/session/{sid}", f"/session/{sid}/deliverable"):
        block = _scope_block(client.get(path).get_data(as_text=True))
        assert 'data-scope-part="control"' in block
        visible = _visible(block)
        assert CTRL["ctrl_part_name"] in visible and CTRL["ctrl_part_function"] in visible
        assert ui_text.text("UI_S15_SCOPE_STATEMENT_3", "en") in visible
        assert ui_text.text("UI_S15_SCOPE_PROVENANCE_3", "en") in visible
        assert ui_text.text("UI_S15_SCOPE_STATEMENT", "en") not in visible


def test_two_part_scope_keeps_its_existing_copy(client, part_eligible):
    sid = _created(_compose(client, TIE_IDEA))
    block = _scope_block(client.get(f"/session/{sid}").get_data(as_text=True))
    assert 'data-scope-part="control"' not in block
    visible = _visible(block)
    assert ui_text.text("UI_S15_SCOPE_STATEMENT", "en") in visible
    assert ui_text.text("UI_S15_SCOPE_STATEMENT_3", "en") not in visible


def test_every_new_copy_key_has_english_and_arabic():
    keys = [k for k in ui_text.UI_STRINGS if k.startswith(("UI_S15_CTRL_", "UI_S15_SCOPE_CTRL"))
            or k.endswith(("_3", "_OPTIONAL", "_OPTIONAL_FIELDS")) and k.startswith("UI_S15_")]
    keys.append("UI_S15_IFC_PAIR_LEGEND")
    assert len(keys) >= 17
    for key in keys:
        entry = ui_text.UI_STRINGS[key]
        assert entry["en"].strip() and entry["ar"].strip(), key
        # never "the two parts" / "both parts" of the whole composition ("two parts" of one interaction is true)
        assert not re.search(r"\bthe two parts\b|\bboth parts\b", entry["en"]), key


# ======================================================================= F. root behaviour unchanged

def test_root_journey_is_identical_for_two_and_three_part_projects(client, part_eligible):
    two = _created(_compose(client, TIE_IDEA, focus=MECH))
    three = _three_part_project(client, focus=MECH)
    a, b = _live(two), _live(three)
    assert (a.domain, a.path, a.maturity_level) == (b.domain, b.path, b.maturity_level)
    assert [(g.gap_type, g.status) for g in a.gaps] == [(g.gap_type, g.status) for g in b.gaps]
    assert CL not in {a.domain, b.domain, getattr(b, "domain_signal", None)}


def test_no_progression_path_n_or_persistence_file_changed_for_this_slice():
    for rel in ("engine/progression_loop.py", "engine/path_n_questions.py", "engine/record_store.py",
                "engine/domain_rules.py"):
        src = open(os.path.join(_ROOT, rel), encoding="utf-8").read()
        assert "OPTIONAL_COMPOSITION_DOMAINS" not in src and "is_part_eligible" not in src, rel
