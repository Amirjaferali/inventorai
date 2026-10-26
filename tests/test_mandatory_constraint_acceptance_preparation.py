"""MANDATORY-CONSTRAINT-ACCEPTANCE-PREPARATION-01 — the inventor's notes for checking ONE mandatory constraint.

For ONE CURRENT mandatory constraint (PATHN-CONSTRAINT-DECLARATION-01, PR #855) the inventor may record, in their
own words, an observable acceptance criterion and the measurement, evidence or specialist review they would need
to check it. Verification PREPARATION only: OWNER_STATED / UNVALIDATED, never a threshold, a verification or
evidence. What is pinned:
  * semantics (``engine/idea_state.py``): keyed by the constraint's FOUNDING identity, saved against a declared
    MANDATORY version of that same constraint; whole-collection validation refuses orphans; notes saved for an
    earlier version are shown as EARLIER statements (not reconfirmed); withdrawn and no-longer-mandatory
    constraints show none (kept, hidden);
  * persistence (``engine/record_store.py``): ONE additive sidecar ``constraint_acceptance_preparations`` with
    composite foreign keys to exact ledger rows; the whole ledger is re-validated inside the write; stale forms
    never overwrite; exact retries write nothing; an unknown table shape is refused;
  * web (``web/app.py``): ONE dedicated POST behind the central project authorization and the CSRF guard,
    committed-truth SAVED / NOT SAVED / UNKNOWN, shown in the session page's constraint section only (EN / AR);
  * the constraint ledger, the Validation Plan step of PR #857, the report / PDF and the Stage 35 export are
    unchanged by the notes.
"""
import html as _html
import json
import re
import sqlite3

import pytest

import web.app as appmod
from engine import idea_state as ist
from engine.idea_state import (
    CONSTRAINT_ACCEPTANCE_CRITERION as CRIT, CONSTRAINT_ACCEPTANCE_EVIDENCE as EVID,
    ConstraintAcceptanceError, ConstraintAcceptanceNotMandatory, ConstraintAcceptancePreparation as Prep,
    ConstraintAcceptanceWithdrawn, ConstraintStale, IdeaState, MECHANISM_COMPLETENESS, constraint_history,
    current_constraint_acceptance, validate_constraint_acceptance_preparations,
)
from engine.record_store import (
    CONSTRAINT_ACCEPTANCE_CLEARED, CONSTRAINT_ACCEPTANCE_SAVED, CONSTRAINT_ACCEPTANCE_UNCHANGED,
    ConstraintAcceptanceCorrupt, ConstraintAcceptanceRejected,
)
from engine.validation_plan import derive_validation_plan
from tests.test_component_interface_participation import _raw, _says  # noqa: F401
from tests.test_pathn_constraint_declaration import _post as _pcn_post
from tests.test_safe_question_routing_pf_q2 import client, MECH, _answer, _start, _live, _store  # noqa: F401
from tests.test_stage15_integrated_invention_entry import _CommitAndRollbackFail
from tests.test_stage15_subsystem_interface_declaration import _FailOn, _restart
from web import ui_text

POST = "/session/%s/constraint-acceptance"
TEXT = "It must weigh under 2 kg"
_FORM_RE = re.compile(
    r'<form method="POST" action="/session/[^"]+/constraint-acceptance" data-pca-form.*?</form>', re.S)


def _t(key, lang="en"):
    return ui_text.text(key, lang)


def _notes(c=None, e=None):
    return {CRIT: c, EVID: e}


def _shown(c=None, e=None, earlier=False):
    return dict(_notes(c, e), earlier=earlier)


# ==========================================================================
# harness
# ==========================================================================
def _ledger(strength="mandatory_constraint"):
    s = IdeaState(idea_id="pca")
    s.record_interaction("answered", "A spring latch locks the deck.", gap_context=MECHANISM_COMPLETENESS)
    d = s.record_constraint_action("declare", TEXT, strength)
    return s, d


def _rows(sid):
    return _raw("SELECT constraint_id, saved_against, acceptance_criterion, evidence_needed "
                "FROM constraint_acceptance_preparations WHERE project_id = ? ORDER BY constraint_id", (sid,))


def _ledger_rows(sid):
    return _raw("SELECT record_id, payload FROM records WHERE project_id = ? ORDER BY seq", (sid,))


def _heads(sid):
    return {c.constraint_id: c for c in constraint_history(_live(sid).assertions).constraints}


def _declare(c, sid, text=TEXT, strength="mandatory_constraint"):
    _pcn_post(c, sid, constraint_action="declare", constraint_text=text, constraint_strength=strength)
    return [cid for cid, ch in _heads(sid).items() if ch.text == text][-1]


def _correct(c, sid, cid, text, strength="mandatory_constraint"):
    _pcn_post(c, sid, constraint_action="correct", constraint_target=_heads(sid)[cid].record_id,
              constraint_text=text, constraint_strength=strength)
    assert appmod.SESSION_STORE[sid].get(appmod.CONSTRAINT_ACK_SLOT) == "UI_PCN_MSG_CORRECTED"


def _withdraw(c, sid, cid):
    _pcn_post(c, sid, constraint_action="withdraw", constraint_target=_heads(sid)[cid].record_id)


def _page(c, sid):
    return c.get("/session/%s" % sid).get_data(as_text=True)


def _forms(raw):
    out = []
    for form in _FORM_RE.findall(raw):
        def value(name):
            m = re.search(r'name="%s" value="([^"]*)"' % name, form)
            return _html.unescape(m.group(1)) if m else None

        def area(name):
            m = re.search(r'name="%s"[^>]*>(.*?)</textarea>' % name, form, re.S)
            return _html.unescape(m.group(1)) if m else None
        out.append({"constraint": value("constraint_id"), "record": value("constraint_record"),
                    "earlier": value("pca_base_earlier"),
                    "base": _notes(value("pca_base_" + CRIT), value("pca_base_" + EVID)),
                    "text": _notes(area("pca_" + CRIT), area("pca_" + EVID))})
    return out


def _form_for(c, sid, cid):
    return next(f for f in _forms(_page(c, sid)) if f["constraint"] == cid)


def _post(c, sid, form, crit=None, evid=None, **override):
    data = {"constraint_id": form["constraint"], "constraint_record": form["record"],
            "pca_base_earlier": form["earlier"],
            "pca_base_" + CRIT: form["base"][CRIT], "pca_base_" + EVID: form["base"][EVID],
            "pca_" + CRIT: form["text"][CRIT] if crit is None else crit,
            "pca_" + EVID: form["text"][EVID] if evid is None else evid}
    data.update(override)
    return c.post(POST % sid, data=data)


def _notice(sid):
    entry = appmod.SESSION_STORE[sid]
    return entry.get(appmod.CONSTRAINT_ACK_SLOT), entry.get(appmod.CONSTRAINT_ERROR_SLOT)


def _project(c):
    sid = _start(c)
    _answer(c, sid, MECH)                                     # one ordinary ledger record before the constraint
    return sid, _declare(c, sid)


def _non_constraint(sid):
    return next(r.record_id for r in _live(sid).assertions if r.disposition == "answered")


# ==========================================================================
# 1. Semantic owner
# ==========================================================================
def test_m01_validation_binds_to_a_mandatory_version_of_the_same_constraint():
    s, d = _ledger()
    ok = Prep(d.record_id, d.record_id, "It reads under 2 kg on a scale", None)
    assert validate_constraint_acceptance_preparations([ok], s.assertions) == (ok,)
    answer = s.assertions[0].record_id
    for bad in (Prep(answer, answer, "x", None),                        # not a constraint
                Prep("rec_999", d.record_id, "x", None),                # unknown identity
                Prep(d.record_id, answer, "x", None),                   # version of another record
                Prep(d.record_id, d.record_id, None, None),             # empty
                Prep(d.record_id, d.record_id, " padded ", None),       # not the stored form
                Prep(d.record_id, d.record_id, "x" * 1001, None),       # too long
                Prep(d.record_id, d.record_id, "a\x00b", None)):        # NUL
        with pytest.raises(ConstraintAcceptanceError):
            validate_constraint_acceptance_preparations([bad], s.assertions)
    with pytest.raises(ConstraintAcceptanceError):
        validate_constraint_acceptance_preparations([ok, ok], s.assertions)
    # a version that was never mandatory cannot carry notes
    soft, sd = _ledger("soft_constraint")
    with pytest.raises(ConstraintAcceptanceError):
        validate_constraint_acceptance_preparations([Prep(sd.record_id, sd.record_id, "x", None)],
                                                    soft.assertions)
    # a withdrawal record is not a declared version
    w = s.record_constraint_action("withdraw", target_record_id=d.record_id)
    with pytest.raises(ConstraintAcceptanceError):
        validate_constraint_acceptance_preparations([Prep(d.record_id, w.record_id, "x", None)], s.assertions)


def test_m02_current_view_marks_earlier_versions_and_hides_withdrawn_and_non_mandatory():
    s, d = _ledger()
    note = Prep(d.record_id, d.record_id, "x", None)
    assert current_constraint_acceptance([note], constraint_history(s.assertions)) == {d.record_id: (note, False)}
    c1 = s.record_constraint_action("correct", TEXT + " or less", "mandatory_constraint",
                                    target_record_id=d.record_id)
    assert current_constraint_acceptance([note], constraint_history(s.assertions)) == {d.record_id: (note, True)}
    c2 = s.record_constraint_action("correct", TEXT + " or less", "soft_constraint", target_record_id=c1.record_id)
    assert current_constraint_acceptance([note], constraint_history(s.assertions)) == {}
    # still a VALID stored row while hidden
    assert validate_constraint_acceptance_preparations([note], s.assertions) == (note,)
    s.record_constraint_action("correct", TEXT, "mandatory_constraint", target_record_id=c2.record_id)
    assert current_constraint_acceptance([note], constraint_history(s.assertions)) == {d.record_id: (note, True)}
    head = constraint_history(s.assertions).constraints[0].record_id
    s.record_constraint_action("withdraw", target_record_id=head)
    assert current_constraint_acceptance([note], constraint_history(s.assertions)) == {}
    assert validate_constraint_acceptance_preparations([note], s.assertions) == (note,)


def test_m03_target_requires_the_displayed_current_mandatory_version():
    s, d = _ledger()
    h = constraint_history(s.assertions)
    assert ist.constraint_acceptance_target(h, d.record_id, d.record_id).constraint_id == d.record_id
    with pytest.raises(ConstraintAcceptanceError):
        ist.constraint_acceptance_target(h, "rec_999", "rec_999")
    c = s.record_constraint_action("correct", TEXT, "preference", target_record_id=d.record_id)
    h = constraint_history(s.assertions)
    with pytest.raises(ConstraintStale):
        ist.constraint_acceptance_target(h, d.record_id, d.record_id)
    with pytest.raises(ConstraintAcceptanceNotMandatory):
        ist.constraint_acceptance_target(h, d.record_id, c.record_id)
    s.record_constraint_action("withdraw", target_record_id=c.record_id)
    with pytest.raises(ConstraintAcceptanceWithdrawn):
        ist.constraint_acceptance_target(constraint_history(s.assertions), d.record_id, c.record_id)


# ==========================================================================
# 2. Persistence
# ==========================================================================
def test_s01_save_retry_replace_clear_and_the_ledger_is_untouched(client):
    sid, cid = _project(client)
    store, ledger = _store(), _ledger_rows(sid)
    assert store.set_constraint_acceptance(sid, cid, cid, _notes("Scale reads under 2 kg"), _shown()) \
        == CONSTRAINT_ACCEPTANCE_SAVED
    assert _rows(sid) == [(cid, cid, "Scale reads under 2 kg", None)]
    assert store.set_constraint_acceptance(sid, cid, cid, _notes("Scale reads under 2 kg"), _shown()) \
        == CONSTRAINT_ACCEPTANCE_UNCHANGED                                 # exact retry, nothing written
    assert store.set_constraint_acceptance(sid, cid, cid, _notes("Scale reads under 2 kg", "A kitchen scale"),
                                           _shown("Scale reads under 2 kg")) == CONSTRAINT_ACCEPTANCE_SAVED
    assert store.set_constraint_acceptance(sid, cid, cid, _notes(), _shown("Scale reads under 2 kg",
                                                                           "A kitchen scale")) \
        == CONSTRAINT_ACCEPTANCE_CLEARED
    assert _rows(sid) == [] and _ledger_rows(sid) == ledger


def test_s02_a_stale_form_never_overwrites_newer_notes(client):
    sid, cid = _project(client)
    store = _store()
    store.set_constraint_acceptance(sid, cid, cid, _notes("newer"), _shown())
    for expected in (_shown(), _shown("newer", earlier=True), _shown("other")):
        with pytest.raises(ConstraintAcceptanceRejected) as exc:
            store.set_constraint_acceptance(sid, cid, cid, _notes("mine"), expected)
        assert exc.value.kind == "stale"
    assert _rows(sid)[0][2] == "newer"


def test_s03_line_breaks_are_not_a_difference_and_unchanged_text_keeps_its_bytes(client):
    sid, cid = _project(client)
    store = _store()
    store.set_constraint_acceptance(sid, cid, cid, _notes("one\ntwo"), _shown())
    assert store.set_constraint_acceptance(sid, cid, cid, _notes("one\r\ntwo"), _shown("one\r\ntwo")) \
        == CONSTRAINT_ACCEPTANCE_UNCHANGED
    store.set_constraint_acceptance(sid, cid, cid, _notes("one\r\ntwo", "e"), _shown("one\r\ntwo"))
    assert _rows(sid)[0][2:] == ("one\ntwo", "e")


def test_s04_correction_strength_change_and_withdrawal(client):
    sid, cid = _project(client)
    store = _store()
    store.set_constraint_acceptance(sid, cid, cid, _notes("Scale reads under 2 kg"), _shown())
    _correct(client, sid, cid, "It must weigh under 1.5 kg")
    head = _heads(sid)[cid].record_id
    assert head != cid
    record = store.load_constraint_acceptance(sid)
    assert current_constraint_acceptance(record["preparations"], record["history"])[cid][1] is True
    with pytest.raises(ConstraintAcceptanceRejected) as exc:                   # the displayed version is old
        store.set_constraint_acceptance(sid, cid, cid, _notes("x"), _shown("Scale reads under 2 kg", earlier=True))
    assert exc.value.kind == "stale"
    # saving the same notes again reconfirms them for the current version
    assert store.set_constraint_acceptance(sid, cid, head, _notes("Scale reads under 2 kg"),
                                           _shown("Scale reads under 2 kg", earlier=True)) \
        == CONSTRAINT_ACCEPTANCE_SAVED
    assert _rows(sid) == [(cid, head, "Scale reads under 2 kg", None)]
    _correct(client, sid, cid, "It must weigh under 1.5 kg", "soft_constraint")
    soft = _heads(sid)[cid].record_id
    with pytest.raises(ConstraintAcceptanceRejected) as exc:
        store.set_constraint_acceptance(sid, cid, soft, _notes("x"), _shown("Scale reads under 2 kg"))
    assert exc.value.kind == "not_mandatory"
    assert _rows(sid) == [(cid, head, "Scale reads under 2 kg", None)]        # kept while hidden
    _withdraw(client, sid, cid)
    with pytest.raises(ConstraintAcceptanceRejected) as exc:
        store.set_constraint_acceptance(sid, cid, soft, _notes("x"), _shown("Scale reads under 2 kg"))
    assert exc.value.kind == "withdrawn"
    assert _rows(sid) == [(cid, head, "Scale reads under 2 kg", None)]
    assert store.load_constraint_acceptance(sid)["preparations"][0].saved_against == head


def test_s05_identity_shape_and_project_isolation_are_decided_before_any_write(client):
    sid, cid = _project(client)
    other = _start(client)
    foreign = _declare(client, other, "It must be waterproof")
    store = _store()
    for args in ((cid, "", _notes("x"), _shown()), (cid, cid, {CRIT: "x"}, _shown()),
                 (cid, cid, _notes("x"), _notes()), (cid, cid, _notes(" x "), _shown()),
                 (cid, cid, _notes("x" * 1001), _shown()), (cid, cid, _notes("x"), dict(_shown(), earlier=1))):
        with pytest.raises(ConstraintAcceptanceRejected):
            store.set_constraint_acceptance(sid, *args)
    for target in (_non_constraint(sid), "rec_999"):         # not a constraint / unknown
        with pytest.raises(ConstraintAcceptanceRejected) as exc:
            store.set_constraint_acceptance(sid, target, target, _notes("x"), _shown())
        assert exc.value.kind == "invalid"
    assert _rows(sid) == [] and _rows(other) == []
    # record ids are project-scoped: the same id in two projects names two constraints, each written only
    # in its own project
    store.set_constraint_acceptance(sid, cid, cid, _notes("mine"), _shown())
    assert _rows(other) == []
    store.set_constraint_acceptance(other, foreign, foreign, _notes("theirs"), _shown())
    assert _rows(sid) == [(cid, cid, "mine", None)] and _rows(other) == [(foreign, foreign, "theirs", None)]


def test_s06_migration_is_additive_idempotent_and_refuses_an_unknown_shape(client):
    sid, cid = _project(client)
    _store().set_constraint_acceptance(sid, cid, cid, _notes("kept"), _shown())
    _restart()
    assert _store().load_constraint_acceptance(sid)["preparations"][0].acceptance_criterion == "kept"
    _restart()
    _raw("ALTER TABLE constraint_acceptance_preparations RENAME TO cap_old", fk=False)
    _raw("CREATE TABLE constraint_acceptance_preparations (project_id TEXT, note TEXT)", fk=False)
    import os
    from engine.record_store import SqliteRecordStore
    with pytest.raises(sqlite3.DatabaseError):
        SqliteRecordStore(os.environ["INVENTORAI_DB_PATH"]).load_constraint_acceptance(sid)
    _raw("DROP TABLE constraint_acceptance_preparations", fk=False)
    _raw("ALTER TABLE cap_old RENAME TO constraint_acceptance_preparations", fk=False)
    _restart()
    assert _store().load_constraint_acceptance(sid)["preparations"][0].acceptance_criterion == "kept"


def test_s07_the_database_backstop_and_whole_collection_validation(client):
    sid, cid = _project(client)
    answer = _non_constraint(sid)
    for row in ((sid, cid, cid, None, None), (sid, cid, cid, "x" * 1001, None), (sid, cid, cid, "a\x00b", None),
                (sid, "rec_999", cid, "x", None), (sid, cid, "rec_999", "x", None)):
        with pytest.raises(sqlite3.IntegrityError):
            _raw("INSERT INTO constraint_acceptance_preparations VALUES (?, ?, ?, ?, ?)", row)
    _raw("INSERT INTO constraint_acceptance_preparations VALUES (?, ?, ?, ?, ?)",
         (sid, answer, answer, "orphan", None))                             # passes FKs, fails the owner
    with pytest.raises(ConstraintAcceptanceCorrupt):
        _store().load_constraint_acceptance(sid)
    with pytest.raises(ConstraintAcceptanceCorrupt):
        _store().set_constraint_acceptance(sid, cid, cid, _notes("x"), _shown())


def test_s08_failed_writes_roll_back(client):
    sid, cid = _project(client)
    store = _store()
    real = store._conn
    store._conn = _FailOn(real, prefix="INSERT INTO constraint_acceptance_preparations")
    with pytest.raises(Exception):
        store.set_constraint_acceptance(sid, cid, cid, _notes("x"), _shown())
    store._conn = real
    assert _rows(sid) == []


# ==========================================================================
# 3. Web
# ==========================================================================
def test_w01_record_view_replace_and_clear_in_the_constraint_section(client):
    sid, cid = _project(client)
    raw = _page(client, sid)
    assert _t("UI_PCA_HEADING") in _html.unescape(raw) and _t("UI_PCA_INTRO") in _html.unescape(raw)
    [form] = _forms(raw)
    assert (form["constraint"], form["record"], form["earlier"]) == (cid, cid, "0")
    assert form["base"] == _notes("", "")
    r = _post(client, sid, form, "  The scale reads under 2 kg  ", "")
    assert r.status_code == 302 and r.headers["Location"].endswith("#project-constraints")
    assert _notice(sid) == ("UI_PCA_MSG_SAVED", None)
    assert _rows(sid) == [(cid, cid, "The scale reads under 2 kg", None)]
    raw = _page(client, sid)
    text = _html.unescape(raw)
    assert re.search(r'data-pca-criterion><bdi dir="auto"[^>]*>The scale reads under 2 kg</bdi>', raw)
    assert _t("UI_PCA_STATUS") in text and _t("UI_PCA_NOT_RECORDED") in text   # evidence not recorded
    assert _t("UI_PCA_EARLIER") not in text
    form = _form_for(client, sid, cid)
    _post(client, sid, form, None, "A kitchen scale")
    assert _notice(sid) == ("UI_PCA_MSG_SAVED", None)
    _post(client, sid, form, None, "A kitchen scale")                         # the same form again: retry
    assert _notice(sid) == ("UI_PCA_MSG_UNCHANGED", None)
    _post(client, sid, _form_for(client, sid, cid), "", "")
    assert _notice(sid) == ("UI_PCA_MSG_CLEARED", None) and _rows(sid) == []


def test_w02_crlf_resubmission_is_unchanged_and_a_stale_form_writes_nothing(client):
    sid, cid = _project(client)
    _post(client, sid, _form_for(client, sid, cid), "one\r\ntwo")
    form = _form_for(client, sid, cid)
    _post(client, sid, form, "one\r\ntwo")
    assert _notice(sid) == ("UI_PCA_MSG_UNCHANGED", None)
    _post(client, sid, form, "newer")
    _post(client, sid, form, "older tab")                                     # displayed "one two"
    assert _notice(sid) == (None, "UI_PCA_MSG_STALE") and _rows(sid)[0][2] == "newer"


def test_w03_correction_shows_earlier_notes_until_saved_again(client):
    sid, cid = _project(client)
    _post(client, sid, _form_for(client, sid, cid), "Scale reads under 2 kg")
    stale = _form_for(client, sid, cid)
    _correct(client, sid, cid, "It must weigh under 1.5 kg")
    raw = _page(client, sid)
    assert _t("UI_PCA_EARLIER") in _html.unescape(raw)
    assert re.search(r'data-pca-criterion><bdi dir="auto"[^>]*>Scale reads under 2 kg</bdi>', raw)
    _post(client, sid, stale, "changed")                                       # a form of the old version
    assert _notice(sid) == (None, "UI_PCA_MSG_STALE")
    form = _form_for(client, sid, cid)
    assert form["earlier"] == "1" and form["record"] == _heads(sid)[cid].record_id
    _post(client, sid, form)                                                   # saved again, unchanged text
    assert _notice(sid) == ("UI_PCA_MSG_SAVED", None)
    assert _t("UI_PCA_EARLIER") not in _html.unescape(_page(client, sid))
    assert _rows(sid) == [(cid, _heads(sid)[cid].record_id, "Scale reads under 2 kg", None)]


def test_w04_not_mandatory_and_withdrawn_constraints_hide_and_keep_their_notes(client):
    sid, cid = _project(client)
    _post(client, sid, _form_for(client, sid, cid), "Zq-accept-7741")
    _correct(client, sid, cid, TEXT, "soft_constraint")
    raw = _page(client, sid)
    assert "Zq-accept-7741" not in raw and _forms(raw) == [] and "data-pca" not in raw
    _correct(client, sid, cid, TEXT, "mandatory_constraint")
    text = _html.unescape(_page(client, sid))
    assert "Zq-accept-7741" in text and _t("UI_PCA_EARLIER") in text
    form = _form_for(client, sid, cid)
    _withdraw(client, sid, cid)
    raw = _page(client, sid)
    assert "Zq-accept-7741" not in raw and _forms(raw) == []
    _post(client, sid, form, "changed")
    assert _notice(sid) == (None, "UI_PCA_MSG_WITHDRAWN")
    assert _rows(sid)[0][2] == "Zq-accept-7741"
    # a preference or soft constraint never offers the notes
    _declare(client, sid, "It should be blue", "preference")
    assert _forms(_page(client, sid)) == []


def test_w05_not_mandatory_refusal_through_the_route(client):
    sid, cid = _project(client)
    form = _form_for(client, sid, cid)
    _correct(client, sid, cid, TEXT, "soft_constraint")
    _post(client, sid, dict(form, record=_heads(sid)[cid].record_id), "x")
    assert _notice(sid) == (None, "UI_PCA_MSG_NOT_MANDATORY") and _rows(sid) == []


def test_w06_malformed_and_invalid_forms_are_rejected_and_write_nothing(client):
    sid, cid = _project(client)
    form = _form_for(client, sid, cid)
    for override, key in (({"constraint_id": "bogus"}, "UI_PCA_MSG_REJECTED"),
                          ({"constraint_record": "rec_0"}, "UI_PCA_MSG_REJECTED"),
                          ({"pca_base_earlier": "2"}, "UI_PCA_MSG_REJECTED"),
                          ({"pca_base_" + CRIT: "x" * 1001}, "UI_PCA_MSG_REJECTED"),
                          ({"pca_" + CRIT: "x" * 1001}, "UI_PCA_MSG_TOO_LONG"),
                          ({"pca_" + CRIT: "a\x00b"}, "UI_PCA_MSG_INVALID")):
        _post(client, sid, form, **override)
        assert _notice(sid) == (None, key), override
    data = {"constraint_id": [cid, cid], "constraint_record": cid, "pca_base_earlier": "0",
            "pca_base_" + CRIT: "", "pca_base_" + EVID: "", "pca_" + CRIT: "x", "pca_" + EVID: ""}
    client.post(POST % sid, data=data)                                         # a repeated field
    assert _notice(sid) == (None, "UI_PCA_MSG_REJECTED")
    del data["pca_" + EVID]
    data["constraint_id"] = cid
    client.post(POST % sid, data=data)                                         # a missing field
    assert _notice(sid) == (None, "UI_PCA_MSG_REJECTED")
    assert _rows(sid) == []


def test_w07_authorization_csrf_and_cross_project_identities(client):
    from tests.test_commercial_evidence_capture import _client_for
    owner, _aid = _client_for("pca-owner@example.com")
    sid = _start(owner)
    cid = _declare(owner, sid)
    form = _form_for(owner, sid, cid)
    intruder, _bid = _client_for("pca-intruder@example.com")
    r = _post(intruder, sid, form, "intrusion")
    assert r.status_code in (302, 403, 404) and TEXT not in r.get_data(as_text=True)
    raw_client = appmod.app.test_client()                                      # no CSRF token
    r = raw_client.post(POST % sid, data={"constraint_id": cid, "constraint_record": cid,
                                          "pca_base_earlier": "0", "pca_base_" + CRIT: "", "pca_base_" + EVID: "",
                                          "pca_" + CRIT: "x", "pca_" + EVID: ""})
    assert r.status_code == 403
    other = _start(owner)
    _declare(owner, other, "It must be waterproof")
    _post(owner, sid, dict(form, constraint="rec_999", record="rec_999"), "x")
    assert _notice(sid) == (None, "UI_PCA_MSG_REJECTED")
    _post(owner, sid, form, "mine")                                             # written in this project only
    assert _notice(sid) == ("UI_PCA_MSG_SAVED", None)
    assert _rows(sid) == [(cid, cid, "mine", None)] and _rows(other) == []


def test_w08_failed_uncertain_and_unresolved_commits_are_truthful(client):
    sid, cid = _project(client)
    store = _store()
    real = store._conn
    form = _form_for(client, sid, cid)
    store._conn = _FailOn(real, prefix="INSERT INTO constraint_acceptance_preparations")
    _post(client, sid, form, "x")
    store._conn = real
    assert _notice(sid) == (None, "UI_PCA_MSG_NOT_SAVED") and _rows(sid) == []
    store._conn = _FailOn(real, commit_then=True)                              # committed, then raised
    _post(client, sid, form, "x")
    store._conn = real
    assert _notice(sid) == ("UI_PCA_MSG_SAVED", None) and _rows(sid)[0][2] == "x"
    form = _form_for(client, sid, cid)
    store._conn = _CommitAndRollbackFail(real)                                 # unresolved
    _post(client, sid, form, "y")
    store._conn = real
    assert _notice(sid) == (None, "UI_PCA_MSG_UNKNOWN")
    _restart()
    assert _rows(sid)[0][2] == "x"


def test_w09_unreadable_notes_read_unavailable_and_the_constraints_stay(client):
    sid, cid = _project(client)
    form = _form_for(client, sid, cid)
    answer = _non_constraint(sid)
    _raw("INSERT INTO constraint_acceptance_preparations VALUES (?, ?, ?, ?, ?)", (sid, answer, answer, "x", None))
    raw = _page(client, sid)
    assert "data-pca-unavailable" in raw and _forms(raw) == []
    assert "data-pcn-correct-form" in raw and TEXT in _html.unescape(raw)      # the constraint section stays
    _post(client, sid, form, "x")
    assert _notice(sid) == (None, "UI_PCA_MSG_NOT_SAVED")


def test_w10_arabic_page_and_copy_parity(client):
    sid, cid = _project(client)
    _post(client, sid, _form_for(client, sid, cid), "يقرأ الميزان أقل من 2 كغ")
    assert client.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    text = _html.unescape(_page(client, sid))
    for key in ("UI_PCA_HEADING", "UI_PCA_INTRO", "UI_PCA_FIELD_CRITERION", "UI_PCA_FIELD_EVIDENCE",
                "UI_PCA_STATUS", "UI_PCA_SAVE_BUTTON", "UI_PCA_EDIT_SUMMARY"):
        assert _t(key, "ar") in text, key
    assert "يقرأ الميزان أقل من 2 كغ" in text
    assert client.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    raw = _page(client, sid)
    assert re.search(r'<bdi dir="auto"[^>]*>يقرأ الميزان أقل من 2 كغ</bdi>', raw)        # direction-isolated
    assert raw.count('name="pca_acceptance_criterion"') == 1 and 'dir="rtl"' in raw
    assert re.search(r'name="pca_acceptance_criterion"[^>]*dir="auto"', raw)
    # P6-1 RED-05: no tier-overclaim label on the page, in either language
    for lang in ("ar", "en"):
        assert client.post("/ui-language", data={"lang": lang}).status_code in (200, 302)
        body = _page(client, sid).lower()
        for phrase in ("specialist review", "expert review", "professional review", "certified review"):
            assert phrase not in body, (lang, phrase)
    keys = [k for k in ("UI_PCA_HEADING", "UI_PCA_INTRO", "UI_PCA_FIELD_CRITERION", "UI_PCA_FIELD_EVIDENCE",
                        "UI_PCA_NOT_RECORDED", "UI_PCA_STATUS", "UI_PCA_EARLIER", "UI_PCA_UNAVAILABLE",
                        "UI_PCA_EDIT_SUMMARY", "UI_PCA_HINT", "UI_PCA_SAVE_BUTTON")]
    keys += ["UI_PCA_MSG_" + n for n in ("SAVED", "CLEARED", "UNCHANGED", "STALE", "WITHDRAWN", "NOT_MANDATORY",
                                         "TOO_LONG", "INVALID", "REJECTED", "NOT_SAVED", "UNKNOWN")]
    for key in keys:
        assert _t(key, "en") and _t(key, "ar") and _t(key, "en") != _t(key, "ar"), key
    lowered = " ".join(_t(k, "en") for k in keys).lower()
    # positive claims only: the copy names these topics in order to deny them
    for claim in ("has been verified", "it is verified", "it will work", "it is safe", "the constraint is met"):
        assert claim not in lowered, claim


def test_w11_validation_plan_semantics_and_export_are_unchanged_by_the_notes(client):
    # AMENDED at CONSTRAINT-ACCEPTANCE-TO-VALIDATION-PLAN-01 (Owner Option B): the notes are now shown beside
    # their constraint step in report / PDF Section 14 (pinned by tests/test_constraint_acceptance_validation_plan.py);
    # every other field of the plan, the step's authority and the Stage 35 export stay unchanged.
    def semantics(plan):
        return (plan.outcome, plan.blocked_items, [
            (st.step_id, st.statement, st.responsibility, st.evidence_category, st.closure_condition,
             st.provenance, st.confidence, st.interface_preparation) for st in plan.steps])
    sid, cid = _project(client)
    plan_before = derive_validation_plan(_live(sid))
    _post(client, sid, _form_for(client, sid, cid), "Zq-accept-9912", "Zq-evidence-9912")
    assert _rows(sid)
    client.get("/session/%s/deliverable" % sid)                                 # attaches the carrier
    assert semantics(derive_validation_plan(_live(sid))) == semantics(plan_before)
    [step] = [s for s in plan_before.steps if s.step_id == "vstep:constraint:" + cid]
    assert step.responsibility == "UNDETERMINED" and step.confidence == "UNDETERMINED"
    import engine.disclosure_export as export
    assert "constraint_acceptance" not in open(export.__file__, encoding="utf-8").read()


def test_w12_the_constraint_writer_and_validation_plan_owner_are_otherwise_unchanged(client):
    sid, cid = _project(client)
    _post(client, sid, _form_for(client, sid, cid), "x")
    _correct(client, sid, cid, "It must weigh under 1.5 kg")                   # ledger actions unaffected
    # AMENDED at CONSTRAINT-ACCEPTANCE-TO-VALIDATION-PLAN-01: the Validation Plan owner now reads the attached
    # notes for display beside the constraint step; the progression loop and the canonical assembler still do not.
    for path in ("engine/progression_loop.py", "engine/deliverable_assembler.py"):
        source = open(path, encoding="utf-8").read()
        assert "constraint_acceptance" not in source and "CONSTRAINT_ACCEPTANCE" not in source, path
    src = open(appmod.__file__, encoding="utf-8").read()
    section = src[src.index("# --- MANDATORY-CONSTRAINT-ACCEPTANCE-PREPARATION-01"):
                  src.index("def _constraint_report_view(state):")]
    for banned in ("safety_signal", "SafetySignal(", "append_", "/api/", "run_iteration",
                   "record_constraint_action", "state.assertions ="):
        assert banned not in section, banned
    payloads = [json.loads(p) for _rid, p in _ledger_rows(sid)]
    assert all("acceptance" not in json.dumps(p) for p in payloads)


def test_w13_the_stage35_export_is_byte_identical_apart_from_generation_time(client):
    from tests.test_commercial_evidence_capture import _client_for
    owner, _aid = _client_for("pca-export@example.com")
    sid = _start(owner)
    _answer(owner, sid, MECH)
    cid = _declare(owner, sid)
    url = "/account/projects/%s/disclosure-export/json" % sid
    before = owner.get(url)
    assert before.status_code == 200
    _post(owner, sid, _form_for(owner, sid, cid), "Zq-accept-3318", "Zq-evidence-3318")
    assert _rows(sid)
    after = owner.get(url)
    stamp = re.compile(rb"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})")
    assert stamp.sub(b"", after.get_data()) == stamp.sub(b"", before.get_data())
    assert b"Zq-accept-3318" not in after.get_data() and b"Zq-evidence-3318" not in after.get_data()
