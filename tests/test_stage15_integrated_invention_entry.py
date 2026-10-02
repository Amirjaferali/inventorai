"""Stage 15 Slice 1 — Integrated Invention Entry & Durable Subsystem Composition.

One genuine invention containing a Mechanical part AND an Electrical /
Electronics part enters InventorAI truthfully as ONE project:

  * Case A — the EXACT Mechanical / Electrical-Electronics activated
    AMBIGUOUS_TIE is no longer refused outright: the Owner is asked whether the
    parts genuinely work together (YES / NO / NOT SURE, no default), and no
    project / session / durable write exists before a complete, valid YES.
  * Case B — the Owner's explicit start-page declaration leads to the SAME
    clarification even when the classifier returned SINGLE or NONE.
  * YES → the Owner-selected INITIAL ANALYSIS FOCUS becomes the immutable
    scalar root (`confirmed_domain`), and both parts are durable subsystem
    descriptors (system-generated opaque ids, OWNER_STATED, UNVALIDATED) in the
    additive `project_subsystems` sidecar, written in the SAME creation
    transaction as the envelope and the creation routing.
  * Close / reopen, cold load, writable resume and the HTML / PDF report
    reattach the SAME persisted parts; nothing is re-inferred.
  * Session, HTML report and PDF state the bounded scope: only the focus is
    evaluated; the other part and the integration are NOT evaluated.

Nothing here classifies, evaluates, validates or activates anything; the
classifier, the activation policy and the registry are unchanged.
"""
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
from engine.idea_state import IdeaState, OWNER_STATED, UNVALIDATED
from engine.record_contract import ProjectRecordContract
from engine.record_store import (
    ProjectNotFound, ProjectSubsystemsCorrupt, ProjectSubsystemsInvalid,
    SqliteRecordStore)
from tests.csrf_client import csrf_client
from web import ui_text

MECH = "mechanical"
ELEC = "electronics_electrical"

TIE_IDEA = "circuit and hinge"
# A real integrated invention that the classifier scores SINGLE(mechanical).
COMPOSED_SINGLE_IDEA = ("A motorized window opener: a hinge arm and gear train "
                        "moved by a motor with a battery and switch")
ELEC_IDEA = "ESP32 microcontroller circuit with a voltage sensor"
MECH_IDEA = "A hinge mounted bracket with a lever and a spring latch"
NONE_IDEA = "something with no recognizable signals at all"
MED_IDEA = "A catheter guide with an implantable stent"
TIE_STRONG_UNSUPPORTED_IDEA = "circuit and hinge for a catheter"

PARTS = {
    "mech_part_name": "Hinge arm",
    "mech_part_function": "Swings the window open and closed",
    "elec_part_name": "Motor driver board",
    "elec_part_function": "Switches battery power to the motor",
}

_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


# ==========================================================================
# harness
# ==========================================================================
@pytest.fixture
def client():
    appmod.app.config["TESTING"] = True
    with csrf_client(appmod.app) as c:
        yield c


@pytest.fixture
def activate(monkeypatch):
    def _activate(*domains):
        monkeypatch.setattr(domain_activation, "_ACTIVATED_DOMAINS", frozenset(domains))
    return _activate


def _store():
    return appmod._get_store()


def _db_path():
    return os.environ["INVENTORAI_DB_PATH"]


def _rows(sql, params=()):
    conn = sqlite3.connect(_db_path())
    try:
        return conn.execute(sql, params).fetchall()
    finally:
        conn.close()


def _project_count():
    _store()                                   # make sure the schema exists
    return _rows("SELECT COUNT(*) FROM projects")[0][0]


def _subsystem_rows(pid=None):
    _store()
    if pid is None:
        return _rows("SELECT * FROM project_subsystems")
    return _rows("SELECT * FROM project_subsystems WHERE project_id = ? "
                 "ORDER BY subsystem_seq", (pid,))


def _compose(c, idea, answer="yes", focus=MECH, lang=None, **overrides):
    if lang == "ar":
        assert c.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    data = {"idea": idea, "composition_step": "1", "integrated_invention": "yes"}
    if answer is not None:
        data["composition_answer"] = answer
    if focus is not None:
        data["initial_focus"] = focus
    data.update(PARTS)
    data.update(overrides)
    return c.post("/start", data=data, follow_redirects=False)


def _created(resp):
    assert resp.status_code == 302, resp.status_code
    assert "/session/" in resp.headers["Location"]
    return resp.headers["Location"].rsplit("/", 1)[-1]


def _live(sid):
    return appmod.SESSION_STORE[sid]["state"]


def _text(resp):
    return _html.unescape(resp.get_data(as_text=True))


def _scope_block(raw):
    m = re.search(r'<section class="integrated-scope".*?</section>', raw, re.S)
    return m.group(0) if m else None


def _visible(fragment):
    return re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", " ", fragment))).strip()


def _pdf_source(c, sid, monkeypatch):
    seen = {}
    real = appmod._render_pdf_bytes

    def spy(source):
        seen["source"] = source
        return real(source)
    monkeypatch.setattr(appmod, "_render_pdf_bytes", spy)
    r = c.post(f"/session/{sid}/deliverable.pdf", data={})
    assert r.status_code == 200 and r.mimetype == "application/pdf"
    assert r.data[:5] == b"%PDF-"
    return seen["source"]


def _ri(domain=MECH, version=SR.RECONSTRUCTION_VERSION):
    return {"seed_idea_text": TIE_IDEA, "confirmed_domain": domain, "path": "N",
            "engine_contract_version": version}


def _pair():
    return (sm.declared_subsystem(MECH, "Hinge arm", "Moves the lid"),
            sm.declared_subsystem(ELEC, "Motor driver", "Powers the motor"))


def _contract(idea_id="i-s15"):
    return ProjectRecordContract.from_state(IdeaState(idea_id=idea_id))


# ==========================================================================
# A. Subsystem owner — additive, OWNER_STATED / UNVALIDATED, opaque identity
# ==========================================================================
def test_existing_two_field_subsystem_descriptor_is_unchanged():
    sub = sm.Subsystem(subsystem_id="a", domain=MECH)
    assert (sub.display_name, sub.function_text, sub.provenance,
            sub.validation_state) == (None, None, None, None)


def test_declared_part_is_owner_stated_unvalidated_with_opaque_id():
    a = sm.declared_subsystem(MECH, "Hinge arm", "Moves")
    b = sm.declared_subsystem(MECH, "Hinge arm", "Moves")
    assert a.provenance == OWNER_STATED and a.validation_state == UNVALIDATED
    assert sm.is_valid_subsystem_id(a.subsystem_id)
    # never derived from the name, the function text, the domain or a position
    assert a.subsystem_id != b.subsystem_id
    for derived in ("Hinge arm", "Moves", MECH, "hinge", "mech"):
        assert derived not in a.subsystem_id
    assert a.subsystem_id not in ("sub-0", "sub-1")


def test_composition_contract_is_exactly_one_mechanical_then_one_electrical():
    mech, elec = _pair()
    assert sm.validate_composition((mech, elec), MECH) == (mech, elec)
    assert sm.validate_composition((), MECH) == ()
    bad = [
        ((elec, mech), MECH),                     # wrong order
        ((mech,), MECH),                          # incomplete
        ((mech, elec, elec), MECH),               # extra
        ((mech, elec), "medical_device"),         # focus not a composed domain
        ((mech, sm.Subsystem(mech.subsystem_id, ELEC, "x", "y", OWNER_STATED,
                             UNVALIDATED)), MECH),                    # dup id
        ((mech, sm.Subsystem(sm.new_subsystem_id(), "electronics", "x", "y",
                             OWNER_STATED, UNVALIDATED)), MECH),      # alias
        ((mech, sm.Subsystem(sm.new_subsystem_id(), ELEC, "x", "y",
                             "SYSTEM_INFERRED", UNVALIDATED)), MECH),
        ((mech, sm.Subsystem(sm.new_subsystem_id(), ELEC, "x", "y",
                             OWNER_STATED, "INDEPENDENTLY_VERIFIED")), MECH),
        ((mech, sm.Subsystem(sm.new_subsystem_id(), ELEC, " x", "y",
                             OWNER_STATED, UNVALIDATED)), MECH),      # untrimmed
        ((mech, sm.Subsystem(sm.new_subsystem_id(), ELEC, "x" * 81, "y",
                             OWNER_STATED, UNVALIDATED)), MECH),      # over limit
        ((mech, sm.Subsystem("sub-client-chosen", ELEC, "x", "y",
                             OWNER_STATED, UNVALIDATED)), MECH),      # bad id shape
    ]
    for subs, focus in bad:
        with pytest.raises(sm.CompositionError):
            sm.validate_composition(subs, focus)


# ==========================================================================
# B. Durable sidecar — schema, migration, atomicity, isolation, fail-closed
# ==========================================================================
def test_fresh_database_has_the_additive_table_and_no_rows(tmp_path):
    store = SqliteRecordStore(str(tmp_path / "fresh.db"))
    store.close()
    conn = sqlite3.connect(str(tmp_path / "fresh.db"))
    cols = [r[1] for r in conn.execute("PRAGMA table_info(project_subsystems)")]
    assert cols == ["project_id", "subsystem_seq", "subsystem_id", "domain",
                    "display_name", "function_text", "provenance", "validation_state"]
    assert conn.execute("SELECT COUNT(*) FROM project_subsystems").fetchone() == (0,)
    fks = conn.execute("PRAGMA foreign_key_list(project_subsystems)").fetchall()
    assert [(f[2], f[3], f[4]) for f in fks] == [("projects", "project_id", "project_id")]
    conn.close()


def _snapshot(path):
    conn = sqlite3.connect(path)
    try:
        return {t: conn.execute(f"SELECT * FROM {t} ORDER BY 1, 2").fetchall()
                for t in ("projects", "records", "need_routing_revisions")}
    finally:
        conn.close()


def _schema(path):
    conn = sqlite3.connect(path)
    try:
        return sorted(conn.execute(
            "SELECT type, name, sql FROM sqlite_master").fetchall(),
            key=lambda r: (r[0], r[1]))
    finally:
        conn.close()


def test_populated_pre_slice_database_migrates_additively_and_idempotently(tmp_path):
    path = str(tmp_path / "old.db")
    store = SqliteRecordStore(path)
    store.create_project(_contract("old-1"), project_id="old-1",
                         reconstruction_inputs=_ri(MECH))
    store.create_project(_contract("old-2"), project_id="old-2")   # legacy envelope
    store.close()
    # Reduce it to a genuine PRE-SLICE database: no project_subsystems table.
    conn = sqlite3.connect(path)
    conn.execute("DROP TABLE project_subsystems")
    conn.commit()
    conn.close()
    before = _snapshot(path)
    store = SqliteRecordStore(path)                 # forward migration
    assert _snapshot(path) == before                # no existing row rewritten
    assert store.load_project_subsystems("old-1") == ()   # no inferred rows
    assert store.load_project_subsystems("old-2") == ()
    schema_once = _schema(path)
    store.close()
    SqliteRecordStore(path).close()                 # idempotent re-run
    SqliteRecordStore(path).close()
    assert _schema(path) == schema_once
    assert _snapshot(path) == before
    # an old project reconstructs with an EMPTY subsystem collection
    session = SR.reconstruct_readonly_state(SqliteRecordStore(path), "old-1")
    assert session.review.level == 1 and session.state.subsystems == []


def test_create_round_trips_same_ids_across_close_and_reopen(tmp_path):
    path = str(tmp_path / "rt.db")
    subs = _pair()
    store = SqliteRecordStore(path)
    store.create_project(_contract(), project_id="p", reconstruction_inputs=_ri(MECH),
                         subsystems=subs)
    store.close()
    got = SqliteRecordStore(path).load_project_subsystems("p")
    assert [(g.subsystem_id, g.domain, g.display_name, g.function_text,
             g.provenance, g.validation_state) for g in got] == \
           [(s.subsystem_id, s.domain, s.display_name, s.function_text,
             OWNER_STATED, UNVALIDATED) for s in subs]


def test_unknown_project_is_project_not_found(tmp_path):
    with pytest.raises(ProjectNotFound):
        SqliteRecordStore(str(tmp_path / "u.db")).load_project_subsystems("nope")


def test_projects_read_only_their_own_rows_and_ids_are_store_unique(tmp_path):
    path = str(tmp_path / "iso.db")
    store = SqliteRecordStore(path)
    a, b = _pair(), _pair()
    store.create_project(_contract("a"), project_id="A", reconstruction_inputs=_ri(MECH),
                         subsystems=a)
    store.create_project(_contract("b"), project_id="B", reconstruction_inputs=_ri(ELEC),
                         subsystems=b)
    assert [s.subsystem_id for s in store.load_project_subsystems("A")] == \
        [s.subsystem_id for s in a]
    assert [s.subsystem_id for s in store.load_project_subsystems("B")] == \
        [s.subsystem_id for s in b]
    # a row can never be placed under another project with an existing identity
    conn = sqlite3.connect(path)
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("INSERT INTO project_subsystems VALUES (?,?,?,?,?,?,?,?)",
                     ("B", 5, a[0].subsystem_id, MECH, "x", "y", OWNER_STATED,
                      UNVALIDATED))
    conn.close()


def _routing_count(path, pid):
    conn = sqlite3.connect(path)
    try:
        return conn.execute("SELECT COUNT(*) FROM need_routing_revisions "
                            "WHERE project_id = ?", (pid,)).fetchone()[0]
    finally:
        conn.close()


def test_failed_subsystem_insert_rolls_back_project_and_routing(tmp_path):
    from engine import need_routing
    path = str(tmp_path / "rb.db")
    store = SqliteRecordStore(path)
    first = _pair()
    store.create_project(_contract("x"), project_id="X", reconstruction_inputs=_ri(MECH),
                         subsystems=first)
    ri = _ri(MECH, SR.CURRENT_ENGINE_CONTRACT_VERSION)
    routing = need_routing.creation_revisions("Y", MECH, "N", ri["engine_contract_version"])
    assert routing, "a routing-aware Mechanical project carries creation routing"
    # the SECOND part reuses an identity that already exists in the store
    colliding = (sm.declared_subsystem(MECH, "Arm", "Moves"),
                 sm.Subsystem(first[1].subsystem_id, ELEC, "Board", "Powers",
                              OWNER_STATED, UNVALIDATED))
    with pytest.raises(sqlite3.IntegrityError):
        store.create_project(_contract("y"), project_id="Y", reconstruction_inputs=ri,
                             need_routing=routing, subsystems=colliding)
    with pytest.raises(ProjectNotFound):
        store.load_project_subsystems("Y")
    assert _routing_count(path, "Y") == 0
    assert _rows_for(path, "Y") == 0
    # the committed project is untouched and still readable
    assert len(store.load_project_subsystems("X")) == 2


def _rows_for(path, pid):
    conn = sqlite3.connect(path)
    try:
        return conn.execute("SELECT COUNT(*) FROM project_subsystems WHERE project_id = ?",
                            (pid,)).fetchone()[0]
    finally:
        conn.close()


def test_invalid_composition_refuses_before_any_write(tmp_path):
    path = str(tmp_path / "inv.db")
    store = SqliteRecordStore(path)
    mech, elec = _pair()
    dup = sm.Subsystem(mech.subsystem_id, ELEC, "B", "P", OWNER_STATED, UNVALIDATED)
    alias = sm.Subsystem(sm.new_subsystem_id(), "electronics", "B", "P",
                         OWNER_STATED, UNVALIDATED)
    for subs, domain in (((mech, dup), MECH), ((mech, alias), MECH),
                         ((mech, elec), "medical_device"), ((mech, elec), None)):
        with pytest.raises(ProjectSubsystemsInvalid):
            store.create_project(_contract(), project_id="Z",
                                 reconstruction_inputs=_ri(domain), subsystems=subs)
        with pytest.raises(ProjectNotFound):
            store.load_project_subsystems("Z")
    conn = sqlite3.connect(path)
    assert conn.execute("SELECT COUNT(*) FROM projects").fetchone() == (0,)
    assert conn.execute("SELECT DISTINCT domain FROM project_subsystems").fetchall() == []
    conn.close()


_CORRUPTIONS = (
    "UPDATE project_subsystems SET domain = 'software' WHERE subsystem_seq = 1",
    "UPDATE project_subsystems SET domain = 'electronics' WHERE subsystem_seq = 1",
    "UPDATE project_subsystems SET subsystem_seq = 7 WHERE subsystem_seq = 1",
    "DELETE FROM project_subsystems WHERE subsystem_seq = 1",
    "UPDATE project_subsystems SET subsystem_id = 'sub-ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ' "
    "WHERE subsystem_seq = 0",
    "UPDATE project_subsystems SET display_name = ' padded' WHERE subsystem_seq = 0",
    "UPDATE projects SET confirmed_domain = 'medical_device'",
    "UPDATE project_subsystems SET domain = 'electronics_electrical' WHERE subsystem_seq = 0",
)


@pytest.mark.parametrize("sql", _CORRUPTIONS)
def test_malformed_durable_rows_fail_closed_everywhere(tmp_path, sql):
    path = str(tmp_path / "bad.db")
    store = SqliteRecordStore(path)
    store.create_project(_contract(), project_id="p", reconstruction_inputs=_ri(MECH),
                         subsystems=_pair())
    store.close()
    conn = sqlite3.connect(path)
    conn.execute(sql)
    conn.commit()
    conn.close()
    store = SqliteRecordStore(path)
    with pytest.raises(ProjectSubsystemsCorrupt):
        store.load_project_subsystems("p")
    with pytest.raises(ProjectSubsystemsCorrupt):
        SR.reconstruct_readonly_state(store, "p")


def test_schema_backstops_the_fixed_provenance_and_validation_values(tmp_path):
    path = str(tmp_path / "chk.db")
    store = SqliteRecordStore(path)
    store.create_project(_contract(), project_id="p", reconstruction_inputs=_ri(MECH))
    store.close()
    conn = sqlite3.connect(path)
    for row in (("p", 0, sm.new_subsystem_id(), MECH, "x", "y", "SYSTEM_INFERRED", UNVALIDATED),
                ("p", 0, sm.new_subsystem_id(), MECH, "x", "y", OWNER_STATED, "VERIFIED"),
                ("p", 0, sm.new_subsystem_id(), MECH, "x" * 81, "y", OWNER_STATED, UNVALIDATED),
                ("p", 0, sm.new_subsystem_id(), MECH, "x", "y\x00", OWNER_STATED, UNVALIDATED),
                ("ghost", 0, sm.new_subsystem_id(), MECH, "x", "y", OWNER_STATED, UNVALIDATED)):
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute("PRAGMA foreign_keys = ON")
            conn.execute("INSERT INTO project_subsystems VALUES (?,?,?,?,?,?,?,?)", row)
    conn.close()


def test_no_writer_can_update_or_delete_composition_or_focus():
    src = open(os.path.join(_ROOT, "engine", "record_store.py"), encoding="utf-8").read()
    assert "UPDATE project_subsystems" not in src
    assert "DELETE FROM project_subsystems" not in src
    assert not re.search(r"UPDATE\s+projects\s+SET[^\"]*confirmed_domain", src)
    app_src = open(os.path.join(_ROOT, "web", "app.py"), encoding="utf-8").read()
    # the web layer holds no SQL of its own over the sidecar
    for sql in ("INTO project_subsystems", "FROM project_subsystems",
                "UPDATE project_subsystems"):
        assert sql not in app_src
    assert "focus_switch" not in app_src and "/focus" not in app_src


# ==========================================================================
# C. Admission — backward compatibility (A, B) and the bounded entry (C–J)
# ==========================================================================
def test_a_single_flows_unchanged_when_affordance_unused(client, monkeypatch):
    calls = []
    real = appmod.SqliteRecordStore.create_project

    def spy(self, *a, **kw):
        calls.append(sorted(kw))
        return real(self, *a, **kw)
    monkeypatch.setattr(appmod.SqliteRecordStore, "create_project", spy)
    for idea, domain in ((ELEC_IDEA, ELEC), (MECH_IDEA, MECH)):
        before = _project_count()
        first = client.post("/start", data={"idea": idea})
        assert first.status_code == 200 and "data-composition-form" not in first.get_data(as_text=True)
        sid = _created(client.post("/start", data={"idea": idea, "domain_confirm": domain}))
        state = _live(sid)
        assert state.domain == domain and state.subsystems == []
        assert _project_count() == before + 1 and _subsystem_rows(sid) == []
    assert all("subsystems" not in kw for kw in calls)     # exact pre-slice call


def test_b_none_flow_unchanged_when_affordance_unused(client):
    r = client.post("/start", data={"idea": NONE_IDEA})
    body = r.get_data(as_text=True)
    assert r.status_code == 200 and 'name="domain_choice"' in body
    assert "data-composition-form" not in body
    sid = _created(client.post("/start", data={"idea": NONE_IDEA, "domain_choice": ELEC,
                                               "domain_confirm": ELEC}))
    assert _live(sid).domain == ELEC and _live(sid).subsystems == []


def test_start_page_offers_the_declaration_only_as_an_option(client):
    body = client.get("/").get_data(as_text=True)
    assert 'name="integrated_invention" value="yes"' in body
    assert ui_text.text("UI_S15_OFFER_LABEL", "en") in _html.unescape(body)
    offer = re.search(r'<input type="checkbox" name="integrated_invention"[^>]*>', body).group(0)
    assert "checked" not in offer and "required" not in offer


def test_c_exact_tie_asks_for_clarification_and_creates_nothing(client):
    assert classify_domain(TIE_IDEA).kind is DomainResultKind.AMBIGUOUS_TIE
    before, sessions = _project_count(), set(appmod.SESSION_STORE)
    for confirm in (None, ELEC, MECH):
        data = {"idea": TIE_IDEA}
        if confirm:
            data["domain_confirm"] = confirm
        r = client.post("/start", data=data)
        body = r.get_data(as_text=True)
        assert r.status_code == 200
        assert "data-composition-form" in body
        assert ui_text.text("UI_S15_INTRO_TIE", "en") in _html.unescape(body)
        assert ui_text.text("UI_S15_QUESTION", "en") in _html.unescape(body)
        # no default answer, no default focus
        assert not re.search(r'name="composition_answer"[^>]*checked', body)
        assert not re.search(r'name="initial_focus"[^>]*checked', body)
    assert _project_count() == before and set(appmod.SESSION_STORE) == sessions
    assert _subsystem_rows() == []


@pytest.mark.parametrize("focus", (MECH, ELEC))
def test_d_yes_with_complete_fields_creates_one_project_with_two_parts(client, focus):
    before = _project_count()
    sid = _created(_compose(client, TIE_IDEA, focus=focus))
    assert _project_count() == before + 1
    state = _live(sid)
    assert state.domain == focus and state.domain_signal == focus
    rows = _subsystem_rows(sid)
    assert [(r[1], r[3], r[4], r[5], r[6], r[7]) for r in rows] == [
        (0, MECH, PARTS["mech_part_name"], PARTS["mech_part_function"],
         OWNER_STATED, UNVALIDATED),
        (1, ELEC, PARTS["elec_part_name"], PARTS["elec_part_function"],
         OWNER_STATED, UNVALIDATED)]
    assert [s.subsystem_id for s in state.subsystems] == [r[2] for r in rows]
    inputs = _store().load_reconstruction_inputs(sid)
    assert inputs["confirmed_domain"] == focus
    assert inputs["seed_idea_text"] == TIE_IDEA
    # the ordinary focused journey runs: a question is served
    assert client.get(f"/session/{sid}").status_code == 200


@pytest.mark.parametrize("answer,key", (("no", "UI_S15_GUIDE_NO"),
                                        ("not_sure", "UI_S15_GUIDE_NOT_SURE")))
def test_e_f_no_and_not_sure_save_nothing_and_invent_no_winner(client, answer, key):
    before, sessions = _project_count(), set(appmod.SESSION_STORE)
    for idea in (TIE_IDEA, COMPOSED_SINGLE_IDEA):
        r = _compose(client, idea, answer=answer, focus=MECH)
        body = r.get_data(as_text=True)
        assert r.status_code == 200
        assert ui_text.text(key, "en") in _html.unescape(body)
        assert "data-composition-form" not in body
        assert 'name="domain_confirm"' not in body and 'name="domain_choice"' not in body
        # the text is carried back into the ordinary form
        assert re.search(r'<textarea id="idea"[^>]*>' + re.escape(idea) + "</textarea>", body)
    assert _project_count() == before and set(appmod.SESSION_STORE) == sessions
    assert _subsystem_rows() == []


def test_g_explicit_declaration_works_for_a_single_classified_composition(client):
    assert classify_domain(COMPOSED_SINGLE_IDEA).selected_domain == MECH
    r = client.post("/start", data={"idea": COMPOSED_SINGLE_IDEA,
                                    "integrated_invention": "yes"})
    assert r.status_code == 200 and "data-composition-form" in r.get_data(as_text=True)
    assert ui_text.text("UI_S15_INTRO_DECLARED", "en") in _text(r)
    sid = _created(_compose(client, COMPOSED_SINGLE_IDEA, focus=ELEC))
    assert _live(sid).domain == ELEC and len(_subsystem_rows(sid)) == 2
    # NONE + explicit declaration reaches the SAME clarification
    r = client.post("/start", data={"idea": NONE_IDEA, "integrated_invention": "yes"})
    assert "data-composition-form" in r.get_data(as_text=True)


@pytest.mark.parametrize("forged", ("medical_device", "software", "electronics",
                                    "Mechanical", "", "iot_electronics"))
def test_h_forged_focus_is_refused(client, forged):
    before = _project_count()
    r = _compose(client, TIE_IDEA, focus=forged)
    assert r.status_code == 400
    assert ui_text.text("UI_S15_ERR_FOCUS", "en") in _text(r)
    assert _project_count() == before and _subsystem_rows() == []


def test_h_forged_answer_and_client_ids_are_ignored_or_refused(client):
    before = _project_count()
    for bad in ("YES", "maybe", ""):
        r = _compose(client, TIE_IDEA, answer=bad)
        assert r.status_code == 400 and ui_text.text("UI_S15_ERR_ANSWER", "en") in _text(r)
    assert _project_count() == before
    chosen = "sub-" + "a" * 32
    sid = _created(_compose(client, TIE_IDEA, subsystem_id=chosen,
                            mech_subsystem_id=chosen, elec_subsystem_id=chosen))
    ids = [r[2] for r in _subsystem_rows(sid)]
    assert chosen not in ids and all(sm.is_valid_subsystem_id(i) for i in ids)
    sid2 = _created(_compose(client, TIE_IDEA))
    assert set(ids).isdisjoint(r[2] for r in _subsystem_rows(sid2))   # same text, new ids


@pytest.mark.parametrize("deactivated", (ELEC, MECH))
def test_i_one_domain_no_longer_activated_is_refused(client, activate, deactivated):
    remaining = MECH if deactivated == ELEC else ELEC
    activate(remaining)
    before, sessions = _project_count(), set(appmod.SESSION_STORE)
    for resp in (client.post("/start", data={"idea": TIE_IDEA, "integrated_invention": "yes"}),
                 _compose(client, TIE_IDEA, focus=remaining)):
        body = _text(resp)
        assert resp.status_code == 200
        assert appmod._unsupported_domain_message([remaining], "en") in body
        assert "data-composition-form" not in resp.get_data(as_text=True)
    assert _project_count() == before and set(appmod.SESSION_STORE) == sessions
    assert _subsystem_rows() == []


def test_j_strong_unsupported_and_non_activated_domains_stay_fail_closed(client):
    assert classify_domain(TIE_STRONG_UNSUPPORTED_IDEA).kind is DomainResultKind.AMBIGUOUS_TIE
    before = _project_count()
    msg = appmod._unsupported_domain_message(domain_activation.activated_domains(), "en")
    for resp in (client.post("/start", data={"idea": TIE_STRONG_UNSUPPORTED_IDEA}),
                 _compose(client, TIE_STRONG_UNSUPPORTED_IDEA),
                 client.post("/start", data={"idea": MED_IDEA, "integrated_invention": "yes"}),
                 _compose(client, MED_IDEA)):
        assert resp.status_code == 200
        assert msg in _text(resp)
        assert "data-composition-form" not in resp.get_data(as_text=True)
    assert _project_count() == before and _subsystem_rows() == []


def test_other_ties_keep_the_existing_refusal(client, activate):
    activate(ELEC, MECH, "medical_device")
    r = client.post("/start", data={"idea": "circuit and hinge and stent",
                                    "integrated_invention": "yes"})
    assert "data-composition-form" not in r.get_data(as_text=True)


def test_bounded_fields_reject_never_truncate(client):
    before = _project_count()
    cases = (({"mech_part_name": "x" * 81}, "UI_S15_ERR_TOO_LONG"),
             ({"elec_part_function": "y" * 301}, "UI_S15_ERR_TOO_LONG"),
             ({"mech_part_function": "a\x00b"}, "UI_S15_ERR_INVALID_CHAR"),
             ({"elec_part_name": "   "}, "UI_S15_ERR_FIELDS"),
             ({"mech_part_function": ""}, "UI_S15_ERR_FIELDS"))
    for override, key in cases:
        r = _compose(client, TIE_IDEA, **override)
        assert r.status_code == 400 and ui_text.text(key, "en") in _text(r)
        assert "data-composition-form" in r.get_data(as_text=True)
    assert _project_count() == before and _subsystem_rows() == []
    sid = _created(_compose(client, TIE_IDEA, mech_part_name="n" * 80,
                            elec_part_function="f" * 300))
    rows = _subsystem_rows(sid)
    assert rows[0][4] == "n" * 80 and rows[1][5] == "f" * 300


def test_failed_durable_creation_leaves_nothing_and_no_session(client, monkeypatch):
    first = _created(_compose(client, TIE_IDEA))
    existing = _subsystem_rows(first)[1][2]
    monkeypatch.setattr(sm, "new_subsystem_id", lambda: existing)
    before, sessions = _project_count(), set(appmod.SESSION_STORE)
    r = _compose(client, TIE_IDEA, focus=MECH)
    assert r.status_code == 503
    assert _project_count() == before and set(appmod.SESSION_STORE) == sessions
    assert _rows("SELECT COUNT(*) FROM need_routing_revisions WHERE project_id NOT IN "
                 "(SELECT project_id FROM projects)")[0][0] == 0
    assert len(_subsystem_rows()) == 2


# ==========================================================================
# D. Initial focus — immutable scalar root; the other part is not evaluated
# ==========================================================================
@pytest.mark.parametrize("focus,other", ((MECH, ELEC), (ELEC, MECH)))
def test_focus_is_the_root_and_the_other_part_is_only_recorded(client, focus, other):
    sid = _created(_compose(client, TIE_IDEA, focus=focus))
    state = _live(sid)
    assert state.domain == focus
    # routing (if any) belongs to the focus domain only — no other-domain run
    for rev in getattr(state, "need_routing", ()) or ():
        assert focus in rev.policy_ref or rev.policy_ref.startswith(focus)
    raw = client.get(f"/session/{sid}").get_data(as_text=True)
    block = _scope_block(raw)
    visible = _visible(block)
    assert ui_text.text("UI_S15_SCOPE_STATEMENT", "en") in visible
    focus_label = ui_text.text("UI_S15_SCOPE_FOCUS_MECH" if focus == MECH
                               else "UI_S15_SCOPE_FOCUS_ELEC", "en")
    assert focus_label in visible
    for part in PARTS.values():
        assert part in visible
    # no gap / evidence / evaluation is presented for either part
    for claim in ("gap", "Gap", "evidence", "validated", "evaluated as",
                  "compatible", "feasible", "Mechatronics"):
        assert claim not in visible.replace(
            ui_text.text("UI_S15_SCOPE_STATEMENT", "en"), "").replace(
            ui_text.text("UI_S15_SCOPE_PROVENANCE", "en"), "")
    assert "Mechatronics" not in raw


def test_confirmed_domain_never_changes_after_answers_and_reload(client):
    from tests.test_safe_question_routing_pf_q2 import _answer
    sid = _created(_compose(client, COMPOSED_SINGLE_IDEA, focus=ELEC))
    ids = [r[2] for r in _subsystem_rows(sid)]
    _answer(client, sid, "It opens the window when the room is too warm.")
    _answer(client, sid, "The motor turns a small gear that pushes the hinge arm.")
    assert _store().load_reconstruction_inputs(sid)["confirmed_domain"] == ELEC
    assert _live(sid).domain == ELEC
    assert [r[2] for r in _subsystem_rows(sid)] == ids
    recon = SR.reconstruct_readonly_state(_store(), sid)
    assert recon.state.domain == ELEC
    assert [s.subsystem_id for s in recon.state.subsystems] == ids


# ==========================================================================
# E. Round-trip surfaces — cold load, writable resume, report, PDF, EN / AR
# ==========================================================================
def test_cold_load_and_writable_resume_reattach_the_same_parts(client):
    sid = _created(_compose(client, TIE_IDEA, focus=MECH))
    ids = [s.subsystem_id for s in _live(sid).subsystems]
    appmod.SESSION_STORE.clear()                       # memory loss
    raw = client.get(f"/session/{sid}").get_data(as_text=True)
    assert _scope_block(raw) is not None
    cold = _live(sid)
    assert getattr(cold, "domain", None) is None and cold.domain_signal == MECH
    assert [s.subsystem_id for s in cold.subsystems] == ids
    appmod.SESSION_STORE.pop(sid)
    assert client.post(f"/session/{sid}/resume", data={}).status_code == 302
    resumed = _live(sid)
    assert resumed.domain == MECH
    assert [s.subsystem_id for s in resumed.subsystems] == ids
    assert [(s.display_name, s.function_text) for s in resumed.subsystems] == [
        (PARTS["mech_part_name"], PARTS["mech_part_function"]),
        (PARTS["elec_part_name"], PARTS["elec_part_function"])]
    # a fresh store connection reads the same parts
    appmod._STORE.close()
    appmod._STORE = None
    assert [s.subsystem_id for s in _store().load_project_subsystems(sid)] == ids


def test_session_en_and_ar_render_the_scope_disclosure(client):
    sid = _created(_compose(client, TIE_IDEA, focus=ELEC))
    en = client.get(f"/session/{sid}").get_data(as_text=True)
    en_block = _visible(_scope_block(en))
    for key in ("UI_S15_SCOPE_TITLE", "UI_S15_SCOPE_MECH", "UI_S15_SCOPE_ELEC",
                "UI_S15_SCOPE_FOCUS", "UI_S15_SCOPE_FOCUS_ELEC",
                "UI_S15_SCOPE_STATEMENT", "UI_S15_SCOPE_PROVENANCE"):
        assert ui_text.text(key, "en") in en_block
    assert client.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    ar = client.get(f"/session/{sid}").get_data(as_text=True)
    assert re.search(r'<html[^>]*dir="rtl"', ar)
    ar_block = _visible(_scope_block(ar))
    for key in ("UI_S15_SCOPE_TITLE", "UI_S15_SCOPE_FOCUS_ELEC", "UI_S15_SCOPE_STATEMENT"):
        assert ui_text.text(key, "ar") in ar_block
    assert ui_text.text("UI_S15_SCOPE_STATEMENT", "en") not in ar_block
    assert PARTS["elec_part_name"] in ar_block             # Owner words verbatim
    assert 'dir="auto"' in _scope_block(ar)


def test_html_report_and_pdf_carry_the_same_scope_disclosure(client, monkeypatch):
    sid = _created(_compose(client, TIE_IDEA, focus=MECH))
    report = client.get(f"/session/{sid}/deliverable").get_data(as_text=True)
    block = _scope_block(report)
    assert block and report.index(block) < report.index('id="report-contents"')
    assert ui_text.text("UI_S15_SCOPE_STATEMENT", "en") in _visible(block)
    source = _pdf_source(client, sid, monkeypatch)
    pdf_block = _scope_block(source)
    assert pdf_block and _visible(pdf_block) == _visible(block)
    # AR report + PDF
    assert client.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    ar_report = client.get(f"/session/{sid}/deliverable").get_data(as_text=True)
    assert ui_text.text("UI_S15_SCOPE_STATEMENT", "ar") in _visible(_scope_block(ar_report))
    ar_source = _pdf_source(client, sid, monkeypatch)
    assert ui_text.text("UI_S15_SCOPE_STATEMENT", "ar") in _visible(_scope_block(ar_source))


def test_cold_report_and_pdf_reattach_the_scope(client, monkeypatch):
    sid = _created(_compose(client, TIE_IDEA, focus=ELEC))
    appmod.SESSION_STORE.clear()
    report = client.get(f"/session/{sid}/deliverable").get_data(as_text=True)
    assert ui_text.text("UI_S15_SCOPE_FOCUS_ELEC", "en") in _visible(_scope_block(report))
    appmod.SESSION_STORE.clear()
    assert _scope_block(_pdf_source(client, sid, monkeypatch)) is not None


def test_ordinary_projects_render_no_scope_block(client, monkeypatch):
    sid = _created(client.post("/start", data={"idea": ELEC_IDEA, "domain_confirm": ELEC}))
    assert _scope_block(client.get(f"/session/{sid}").get_data(as_text=True)) is None
    assert _scope_block(client.get(f"/session/{sid}/deliverable").get_data(as_text=True)) is None
    assert _scope_block(_pdf_source(client, sid, monkeypatch)) is None


def test_owner_text_is_escaped_and_no_internal_identifier_leaks(client):
    hostile = '<script>alert("x")</script>'
    sid = _created(_compose(client, TIE_IDEA, mech_part_name=hostile))
    for path in (f"/session/{sid}", f"/session/{sid}/deliverable"):
        raw = client.get(path).get_data(as_text=True)
        assert hostile not in raw
        assert "&lt;script&gt;" in _scope_block(raw)
        visible = _visible(_scope_block(raw))
        for ident in [s.subsystem_id for s in _live(sid).subsystems] + [
                ELEC, "OWNER_STATED", "UNVALIDATED", "sub-"]:
            assert ident not in visible
    # the clarification form echoes a rejected value escaped
    r = _compose(client, TIE_IDEA, mech_part_name=hostile + "x" * 80)
    assert hostile not in r.get_data(as_text=True)


def test_corrupt_composition_fails_the_surfaces_closed(client):
    sid = _created(_compose(client, TIE_IDEA, focus=MECH))
    conn = sqlite3.connect(_db_path())
    conn.execute("DELETE FROM project_subsystems WHERE project_id = ? AND subsystem_seq = 1",
                 (sid,))
    conn.commit()
    conn.close()
    r = client.get(f"/session/{sid}")
    assert r.status_code == 302 and r.headers["Location"].endswith("/")
    r = client.get(f"/session/{sid}/deliverable")
    assert r.status_code == 302
    appmod.SESSION_STORE.clear()
    assert client.get(f"/session/{sid}").status_code == 302


def test_composition_page_ar_is_rtl_and_bilingual(client):
    assert client.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    r = client.post("/start", data={"idea": TIE_IDEA})
    raw = r.get_data(as_text=True)
    assert re.search(r'<html[^>]*dir="rtl"', raw)
    text = _html.unescape(raw)
    # AMENDED at the Stage 28 part-only enablement: the form now offers the optional part slot, so its focus
    # note is the optional-part variant; the two-part note stays defined for a withdrawn policy
    for key in ("UI_S15_TITLE", "UI_S15_QUESTION", "UI_S15_YES", "UI_S15_NO",
                "UI_S15_NOT_SURE", "UI_S15_FOCUS_PROMPT", "UI_S15_FOCUS_NOTE_OPTIONAL"):
        assert ui_text.text(key, "ar") in text
    for key in ("UI_S15_OFFER_LABEL", "UI_S15_GUIDE_NO", "UI_S15_GUIDE_NOT_SURE", "UI_S15_FOCUS_NOTE",
                "UI_S15_SCOPE_STATEMENT", "UI_S15_ERR_TOO_LONG"):
        assert ui_text.has_string(key)
    # plain user-facing language: no internal architecture words in the copy
    for key in [k for k in ui_text.UI_STRINGS if k.startswith("UI_S15_")]:
        for lang in ("en", "ar"):
            for word in ("Domain Pack", "D4", "IRL", "subsystem", "classif",
                         "Mechatronics"):
                assert word not in ui_text.UI_STRINGS[key][lang], (key, word)


def test_no_provider_classifier_activation_or_registry_change():
    for rel in ("engine/domain_rules.py", "engine/domain_activation.py",
                "engine/domain_registry.py", "engine/record_contract.py",
                "engine/read_export_service.py"):
        src = open(os.path.join(_ROOT, rel), encoding="utf-8").read()
        assert "project_subsystems" not in src and "Stage 15" not in src
    src = open(os.path.join(_ROOT, "engine", "subsystem_model.py"), encoding="utf-8").read()
    for token in ("openai", "requests", "urllib", "http", "anthropic", "provider("):
        assert token not in src.lower().replace("https://", "")
    assert domain_activation.activated_domains() == [ELEC, MECH]


def test_stated_limits_match_the_bounds_and_the_browser_never_truncates(client):
    for lang in ("en", "ar"):
        assert str(sm.MAX_SUBSYSTEM_NAME_LENGTH) in ui_text.text("UI_S15_PART_NAME", lang)
        assert str(sm.MAX_SUBSYSTEM_FUNCTION_LENGTH) in ui_text.text("UI_S15_PART_FUNCTION", lang)
    form = re.search(r"<form[^>]*data-composition-form.*?</form>",
                     client.post("/start", data={"idea": TIE_IDEA}).get_data(as_text=True),
                     re.S).group(0)
    assert "maxlength" not in form


def test_cold_load_owner_itself_reattaches_and_fails_closed(client):
    """The durable cold-load owner (not only the render seam) carries the SAME
    parts, and a corrupt composition fails the whole cold load closed."""
    sid = _created(_compose(client, TIE_IDEA, focus=ELEC))
    ids = [s.subsystem_id for s in _live(sid).subsystems]
    appmod.SESSION_STORE.clear()
    with appmod.app.test_request_context("/"):
        entry = appmod._cold_load_entry(sid)
    assert [s.subsystem_id for s in entry["state"].subsystems] == ids
    conn = sqlite3.connect(_db_path())
    conn.execute("UPDATE project_subsystems SET domain = 'software' "
                 "WHERE project_id = ? AND subsystem_seq = 1", (sid,))
    conn.commit()
    conn.close()
    with appmod.app.test_request_context("/"):
        assert appmod._cold_load_entry(sid) is None


# ==========================================================================
# F. F1 / IR01-A correction — an UNSAFE connection never exposes its own
#    uncommitted composition; a healthy read snapshot still reads it.
# ==========================================================================
from engine.record_store import RecordStoreConnectionUnsafe  # noqa: E402


class _CommitAndRollbackFail:
    """Wraps the store's real connection: the next COMMIT fails and the
    defensive ROLLBACK that follows ALSO fails, leaving the write transaction
    unresolved (the IR-01 condition). Every other statement passes through."""

    def __init__(self, conn):
        self._conn = conn
        self.armed = True

    def execute(self, sql, *args):
        if self.armed and sql in ("COMMIT", "ROLLBACK"):
            if sql == "ROLLBACK":
                self.armed = False
            raise sqlite3.OperationalError("injected: %s failed" % sql)
        return self._conn.execute(sql, *args)

    def __getattr__(self, name):
        return getattr(self._conn, name)


def _independent_counts(pid):
    conn = sqlite3.connect(_db_path())
    try:
        return tuple(conn.execute(sql, (pid,)).fetchone()[0] for sql in (
            "SELECT COUNT(*) FROM projects WHERE project_id = ?",
            "SELECT COUNT(*) FROM project_subsystems WHERE project_id = ?",
            "SELECT COUNT(*) FROM need_routing_revisions WHERE project_id = ?"))
    finally:
        conn.close()


def _failed_integrated_creation(client):
    """A REAL integrated /start whose creation transaction (envelope + creation
    routing + both subsystem rows) hits a failed COMMIT and a failed defensive
    ROLLBACK. Returns (store, real_connection, sid)."""
    store = _store()
    real = store._conn
    before = set(appmod.SESSION_STORE)
    store._conn = _CommitAndRollbackFail(real)
    try:
        r = _compose(client, TIE_IDEA, focus=MECH)     # Mechanical focus: routing too
    finally:
        store._conn = real
    assert r.status_code == 503                       # the existing generic unavailable
    assert set(appmod.SESSION_STORE) == before        # no live session advertised
    assert store._connection_unsafe is True           # IR-01: marked unsafe
    assert real.in_transaction                        # the write is unresolved
    sid = real.execute("SELECT project_id FROM projects").fetchone()[0]
    # the hazard is real: THIS connection sees its own uncommitted rows ...
    assert real.execute("SELECT COUNT(*) FROM project_subsystems WHERE project_id = ?",
                        (sid,)).fetchone()[0] == 2
    assert real.execute("SELECT COUNT(*) FROM need_routing_revisions WHERE project_id = ?",
                        (sid,)).fetchone()[0] >= 1
    # ... while an independent connection sees NOTHING committed
    assert _independent_counts(sid) == (0, 0, 0)
    return store, real, sid


def test_f1_unsafe_connection_never_exposes_the_uncommitted_composition(client):
    store, real, sid = _failed_integrated_creation(client)
    try:
        # direct loader: refused BEFORE any row is trusted (no tuple, no ())
        with pytest.raises(RecordStoreConnectionUnsafe):
            store.load_project_subsystems(sid)
        # A. attachment refuses and attaches nothing
        probe = IdeaState(idea_id="probe")
        sentinel = []
        probe.subsystems = sentinel
        assert appmod._attach_project_subsystems(sid, probe) is False
        assert probe.subsystems is sentinel and probe.subsystems == []
        # B. cold load yields no usable project
        with appmod.app.test_request_context("/"):
            assert appmod._cold_load_entry(sid) is None
        # C. canonical reconstruction fails with the existing store refusal
        with pytest.raises(RecordStoreConnectionUnsafe):
            SR.reconstruct_readonly_state(store, sid)
        with pytest.raises(RecordStoreConnectionUnsafe):
            SR.reconstruct_review_state(store, sid)
        # D. writable resume establishes nothing
        client.post(f"/session/{sid}/resume", data={})
        assert sid not in appmod.SESSION_STORE
        # E. the session page renders no scope from those rows
        page = client.get(f"/session/{sid}")
        assert page.status_code == 302
        assert _scope_block(page.get_data(as_text=True)) is None
        assert sid not in appmod.SESSION_STORE
        report = client.get(f"/session/{sid}/deliverable")
        assert report.status_code == 302
        # the flag is persistent: never cleared, never repaired, no reconnect
        assert store._connection_unsafe is True and store._conn is real
        assert real.in_transaction
        assert _independent_counts(sid) == (0, 0, 0)
    finally:
        # abandon the unsafe connection (closing discards its open transaction)
        real.close()
        appmod._STORE = None
    # a FRESH store reads only what was actually committed: nothing
    fresh = _store()
    with pytest.raises(ProjectNotFound):
        fresh.load_project_subsystems(sid)
    assert _independent_counts(sid) == (0, 0, 0)
    assert _subsystem_rows() == []


def test_f1_healthy_read_snapshot_still_reads_the_committed_composition(client):
    sid = _created(_compose(client, TIE_IDEA, focus=ELEC))
    ids = [r[2] for r in _subsystem_rows(sid)]
    store = _store()
    assert store._connection_unsafe is False
    with store.read_snapshot():
        # the snapshot IS an open read transaction: the unconditional IR-01
        # refusal would reject it — the loader's persistent-flag guard does not
        assert store._conn.in_transaction
        with pytest.raises(RecordStoreConnectionUnsafe):
            store._refuse_uncommitted_reads()
        subs = store.load_project_subsystems(sid)
    assert [s.subsystem_id for s in subs] == ids
    assert [s.domain for s in subs] == [MECH, ELEC]
    session = SR.reconstruct_readonly_state(store, sid)
    assert session.review.level == 1 and session.review.reconstructed
    assert session.state.domain == ELEC
    assert [s.subsystem_id for s in session.state.subsystems] == ids
    appmod.SESSION_STORE.pop(sid)
    assert client.post(f"/session/{sid}/resume", data={}).status_code == 302
    assert _live(sid).domain == ELEC
    assert [s.subsystem_id for s in _live(sid).subsystems] == ids
    assert store._connection_unsafe is False
