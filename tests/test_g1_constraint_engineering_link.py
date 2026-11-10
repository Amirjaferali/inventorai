"""G1-2 CONSTRAINT-ENGINEERING-LINK-01 — link ONE mandatory constraint to ONE saved planar clearance check.

Synthetic data only. Under the existing acceptance-preparation owner, the inventor may link one CURRENT
mandatory constraint to one saved planar clearance declaration revision: their own association, in ONE sibling
sidecar (``constraint_engineering_links``) apart from the notes. What is pinned:

Negative controls (derived from the Owner-accepted design boundaries):
  A. forged, foreign or malformed identities (constraint, version, check, generation, submission) write nothing;
  B. only the CURRENT version of a CURRENT mandatory constraint may be linked or unlinked;
  C. only the CURRENT revision of an active check whose every binding holds may be linked;
  D. an obsolete form never overwrites a newer link and never recreates a removed one (ABA): the generation only
     grows and a removed link stays as a tombstone;
  E. a link is CURRENT only while both exact versions are current; a constraint correction, a check correction or
     withdrawal, a component revision or a participation change makes it EARLIER - never moved to a newer
     version, never showing the newer check's result;
  F. a link is never acceptance notes, never a verdict on the constraint ("not assessed"), and changes no
     progression, readiness, gap, Requirement Landscape row or Stage 35 export.
Also: independent note / link lifecycles, exact retry, committed-truth resolution, unlink when the check is gone or
unreadable, unreadable links read UNAVAILABLE, report / PDF continuity (EN / AR), migration shape.
"""
import html as _html
import re
import sqlite3

import pytest

import web.app as appmod
from engine import idea_state as ist
from engine.idea_state import ConstraintEngineeringLink as Link, ConstraintLinkError
from engine.record_store import (
    CONSTRAINT_LINK_LINKED, CONSTRAINT_LINK_UNCHANGED, CONSTRAINT_LINK_UNLINKED,
    ConstraintLinkCorrupt, ConstraintLinkRejected,
)
from engine.requirement_landscape import derive_requirement_landscape
from engine.validation_plan import CONSTRAINT_ACCEPTANCE_NONE, derive_validation_plan
from tests.test_component_interface_participation import _form as _icp_form, _post as _icp_post
from tests.test_component_inventory_correct_withdraw import _correct as _correct_component
from tests.test_constraint_acceptance_validation_plan import _section14
from tests.test_g1_pcc_literal_source_aid import _body, _project, _submit, _url, client  # noqa: F401
from tests.test_mandatory_constraint_acceptance_preparation import (
    _correct, _declare, _form_for, _heads, _post as _pca_post, _withdraw,
)
from tests.test_stage15_interface_preparation import _pdf_source
from web import ui_text

PLAIN = "A smart planter that opens its lid on a hinge when the soil is dry."
LINK = "/session/%s/constraint-engineering-link"
_LINK_FORM_RE = re.compile(r'<form method="POST" action="/session/[^"]+/constraint-engineering-link"'
                           r' data-cel-(link|unlink)-form.*?</form>', re.S)


def _t(key, lang="en"):
    return ui_text.text(key, lang)


def _store():
    return appmod._get_store()


def _setup(c, lang=None, idea=PLAIN):
    """An integrated project with ONE saved, CURRENT planar clearance check and ONE mandatory constraint."""
    sid, ifc, ids = _project(c, idea, lang=lang)
    assert _submit(c, sid, ifc, ids, "85", "56", "Measured").status_code == 200
    return sid, ifc, ids, _declare(c, sid)


def _rev(sid, ifc):
    return _store().load_planar_clearance(sid)["ledger"].active_for(ifc).current_revision.revision_id


def _row(sid, cid):
    con = sqlite3.connect(_store().db_path if hasattr(_store(), "db_path") else _db())
    try:
        return con.execute("SELECT constraint_record, revision_id, generation FROM "
                           "constraint_engineering_links WHERE project_id = ? AND constraint_id = ?",
                           (sid, cid)).fetchone()
    finally:
        con.close()


def _db():
    import os
    return os.environ["INVENTORAI_DB_PATH"]


def _notes_rows(sid):
    con = sqlite3.connect(_db())
    try:
        return con.execute("SELECT * FROM constraint_acceptance_preparations WHERE project_id = ?",
                           (sid,)).fetchall()
    finally:
        con.close()


def _page(c, sid):
    return c.get("/session/%s" % sid).get_data(as_text=True)


def _forms(raw):
    out = []
    for kind in ("link", "unlink"):
        for form in re.findall(r'<form method="POST" action="/session/[^"]+/constraint-engineering-link"'
                               r' data-cel-%s-form.*?</form>' % kind, raw, re.S):
            def value(name, form=form):
                m = re.search(r'name="%s" value="([^"]*)"' % name, form)
                return _html.unescape(m.group(1)) if m else None
            out.append({"kind": kind, "constraint_id": value("constraint_id"),
                        "constraint_record": value("constraint_record"),
                        "cel_generation": value("cel_generation"),
                        "cel_submission": value("cel_submission"),
                        "cel_action": value("cel_action"),
                        "options": re.findall(r'<option value="(pcr-[0-9a-f]{32})"', form)})
    return out


def _form(c, sid, cid, kind="link"):
    return next(f for f in _forms(_page(c, sid)) if f["constraint_id"] == cid and f["kind"] == kind)


def _post(c, sid, form, revision=None, **override):
    data = {k: form[k] for k in ("cel_submission", "constraint_id", "constraint_record",
                                 "cel_generation", "cel_action")}
    if form["cel_action"] == "link":
        data["cel_revision"] = revision if revision is not None else form["options"][0]
    data.update(override)
    return c.post(LINK % sid, data=data)


def _notice(sid):
    entry = appmod.SESSION_STORE[sid]
    return entry.get(appmod.CONSTRAINT_ACK_SLOT), entry.get(appmod.CONSTRAINT_ERROR_SLOT)


def _block(raw, cid):
    """The rendered constraint item of ONE constraint: from its ``data-pcn-item`` to the next one (items
    may hold nested lists, so the split is on the item marker, never on a closing tag)."""
    chunks = raw.split("<li data-pcn-item")[1:]
    return next((_html.unescape(c) for c in chunks
                 if 'name="constraint_id" value="%s"' % cid in c), None)


def _status(raw):
    m = re.search(r'data-cel data-cel-status="([A-Z]+)"', raw)
    return m.group(1) if m else None


def _link(c, sid, cid):
    form = _form(c, sid, cid)
    assert _post(c, sid, form).status_code == 302
    return form


# ==========================================================================
# 1. semantic owner
# ==========================================================================
def _ledger(strength="mandatory_constraint"):
    state = ist.IdeaState(idea_id="i")
    state.assertions = []
    return state


def test_m01_validation_binds_rows_to_mandatory_versions_and_refuses_half_rows(client):
    sid, _ifc, _ids, cid = _setup(client)
    assertions = _store().load_contract(sid).assertions
    record = _heads(sid)[cid].record_id
    rev = "pcr-" + "a" * 32
    ok = ist.validate_constraint_engineering_links([Link(cid, record, rev, 1)], assertions)
    assert ok[0].linked
    assert not ist.validate_constraint_engineering_links([Link(cid, None, None, 3)], assertions)[0].linked
    answered = next(r.record_id for r in assertions if r.disposition == "answered") \
        if any(r.disposition == "answered" for r in assertions) else None
    for bad in ([Link(cid, record, None, 1)], [Link(cid, None, rev, 1)],
                [Link(cid, record, rev, 0)], [Link(cid, record, rev, True)],
                [Link(cid, record, "pcr-short", 1)], [Link("rec_9999", record, rev, 1)],
                [Link(cid, record, rev, 1), Link(cid, None, None, 2)], ["x"]):
        with pytest.raises(ConstraintLinkError):
            ist.validate_constraint_engineering_links(bad, assertions)
    if answered:
        with pytest.raises(ConstraintLinkError):
            ist.validate_constraint_engineering_links([Link(cid, answered, rev, 1)], assertions)


# ==========================================================================
# 2. the end-to-end journey and the inventor-visible outcome
# ==========================================================================
def test_j01_link_shows_the_checks_current_result_and_never_assesses_the_constraint(client):
    sid, ifc, _ids, cid = _setup(client)
    raw = _page(client, sid)
    form = _form(client, sid, cid)
    assert form["cel_generation"] == "0" and form["options"] == [_rev(sid, ifc)]
    assert _status(_block(raw, cid)) == "NONE"
    assert _post(client, sid, form).status_code == 302
    assert _notice(sid)[0] == "UI_CEL_MSG_LINKED"
    assert _row(sid, cid) == (_heads(sid)[cid].record_id, _rev(sid, ifc), 1)
    block = _block(_page(client, sid), cid)
    assert _status(block) == "CURRENT"
    assert _t("UI_CEL_STATUS_CURRENT") in block and _t("UI_CEL_RESULT_MET") in block
    assert _t("UI_CEL_NOT_ASSESSED") in block
    assert 'href="/session/%s/interface-clearance/%s"' % (sid, ifc) in block


# ==========================================================================
# 3. negative controls A-F
# ==========================================================================
def test_a_forged_foreign_and_malformed_identities_write_nothing(client):
    sid, ifc, _ids, cid = _setup(client)
    other, other_ifc, _oids, _ocid = _setup(client)
    form = _form(client, sid, cid)
    other_form = _form(client, other, _ocid)
    for override, expected in (
            ({"cel_revision": _rev(other, other_ifc)}, "UI_CEL_MSG_TARGET"),   # another project's check
            ({"cel_revision": "pcr-" + "b" * 32}, "UI_CEL_MSG_TARGET"),        # an unknown check
            ({"cel_revision": "../x"}, "UI_CEL_MSG_CHOOSE"),
            ({"constraint_id": "rec_99999"}, "UI_CEL_MSG_REJECTED"),           # no such constraint
            ({"constraint_id": "nonsense"}, "UI_CEL_MSG_REJECTED"),
            ({"cel_generation": "-1"}, "UI_CEL_MSG_REJECTED"),
            ({"cel_generation": "01"}, "UI_CEL_MSG_REJECTED"),
            ({"cel_action": "delete"}, "UI_CEL_MSG_REJECTED"),
            ({"cel_submission": "0" * 32 + ".forged"}, "UI_CEL_MSG_REJECTED"),
            ({"cel_submission": other_form["cel_submission"]}, "UI_CEL_MSG_REJECTED")):  # other project
        r = _post(client, sid, form, **override)
        assert r.status_code == 302, override
        assert _notice(sid)[1] == expected, override
        assert _row(sid, cid) is None, override
    assert _post(client, sid, {**form, "cel_action": "unlink"},
                 cel_revision=_rev(sid, ifc)).status_code == 302          # unlink carries no check
    assert _notice(sid)[1] == "UI_CEL_MSG_REJECTED" and _row(sid, cid) is None
    with pytest.raises(ConstraintLinkRejected):
        _store().set_constraint_engineering_link(sid, cid, _heads(sid)[cid].record_id,
                                                 _rev(other, other_ifc), 0)
    assert _row(sid, cid) is None and _row(other, _ocid) is None


def test_b_only_the_current_version_of_a_current_mandatory_constraint(client):
    sid, ifc, _ids, cid = _setup(client)
    form = _form(client, sid, cid)
    _correct(client, sid, cid, "It must keep 2 mm clearance on every side")
    _post(client, sid, form)                                                # the version shown is stale
    assert _notice(sid)[1] == "UI_CEL_MSG_STALE" and _row(sid, cid) is None
    soft = _declare(client, sid, "It should be quiet", "soft_constraint")
    assert not [f for f in _forms(_page(client, sid)) if f["constraint_id"] == soft]
    with pytest.raises(ConstraintLinkRejected) as exc:
        _store().set_constraint_engineering_link(sid, soft, _heads(sid)[soft].record_id, _rev(sid, ifc), 0)
    assert exc.value.kind == "not_mandatory"
    form = _form(client, sid, cid)
    _withdraw(client, sid, cid)
    _post(client, sid, form)
    assert _notice(sid)[1] == "UI_PCA_MSG_WITHDRAWN" and _row(sid, cid) is None


def test_c_only_a_current_fully_bound_check_can_be_linked(client):
    sid, ifc, ids, cid = _setup(client)
    old = _rev(sid, ifc)
    assert _submit(client, sid, ifc, ids, "86", "56", "Re-measured").status_code == 200   # a correction
    form = _form(client, sid, cid)
    assert form["options"] == [_rev(sid, ifc)] and old not in form["options"]
    _post(client, sid, form, revision=old)
    assert _notice(sid)[1] == "UI_CEL_MSG_TARGET" and _row(sid, cid) is None
    record = _store().load_planar_clearance(sid)["ledger"].active_for(ifc)
    _correct_component(_store(), sid, ids[0], 0, "Driver board v2")      # a binding no longer holds
    assert record.current_revision.revision_id == _rev(sid, ifc)
    form = _form(client, sid, cid) if [f for f in _forms(_page(client, sid))
                                       if f["kind"] == "link"] else None
    assert form is None                                                  # nothing linkable is offered
    with pytest.raises(ConstraintLinkRejected) as exc:
        _store().set_constraint_engineering_link(sid, cid, _heads(sid)[cid].record_id, _rev(sid, ifc), 0)
    assert exc.value.kind == "target"
    assert _t("UI_CEL_NO_CANDIDATES") in _block(_page(client, sid), cid)


def test_d_an_obsolete_form_never_recreates_a_removed_link(client):
    sid, ifc, _ids, cid = _setup(client)
    first = _link(client, sid, cid)                                      # generation 1
    unlink = _form(client, sid, cid, "unlink")
    assert unlink["cel_generation"] == "1"
    assert _post(client, sid, unlink).status_code == 302
    assert _notice(sid)[0] == "UI_CEL_MSG_UNLINKED"
    assert _row(sid, cid) == (None, None, 2)                             # a tombstone keeps generation 2
    _post(client, sid, first)                                            # replay of the obsolete link form
    assert _notice(sid)[1] == "UI_CEL_MSG_STALE" and _row(sid, cid) == (None, None, 2)
    _post(client, sid, unlink)                                           # replaying the removal: unchanged
    assert _notice(sid)[0] == "UI_CEL_MSG_UNCHANGED" and _row(sid, cid) == (None, None, 2)
    again = _link(client, sid, cid)
    assert again["cel_generation"] == "2" and _row(sid, cid)[2] == 3
    con = sqlite3.connect(_db())
    try:
        with pytest.raises(sqlite3.DatabaseError):
            con.execute("DELETE FROM constraint_engineering_links WHERE project_id = ?", (sid,))
        with pytest.raises(sqlite3.DatabaseError):
            con.execute("UPDATE constraint_engineering_links SET generation = 1 WHERE project_id = ?", (sid,))
    finally:
        con.rollback()
        con.close()


def test_e_freshness_marks_earlier_and_never_redirects(client):
    sid, ifc, ids, cid = _setup(client)
    _link(client, sid, cid)
    linked = _rev(sid, ifc)

    # a constraint correction
    _correct(client, sid, cid, "It must keep 2 mm clearance on every side")
    block = _block(_page(client, sid), cid)
    assert _status(block) == "EARLIER" and 'data-cel-reason="constraint"' in _page(client, sid)
    assert _t("UI_CEL_RESULT_MET") not in block and _t("UI_CEL_RESULT_MISSING") in block
    _link(client, sid, cid)                                               # explicit relink: current again
    assert _status(_block(_page(client, sid), cid)) == "CURRENT"

    # a check correction
    assert _submit(client, sid, ifc, ids, "88", "56", "Re-measured").status_code == 200
    raw = _page(client, sid)
    assert _status(_block(raw, cid)) == "EARLIER" and 'data-cel-reason="superseded"' in raw
    assert _row(sid, cid)[1] == linked                                    # never moved to the new revision
    assert _t("UI_CEL_RESULT_NOT_MET") not in _block(raw, cid)

    # a component revision makes the current check need reconfirmation
    _link(client, sid, cid)
    _correct_component(_store(), sid, ids[0], 0, "Driver board v2")
    raw = _page(client, sid)
    assert _status(_block(raw, cid)) == "EARLIER" and 'data-cel-reason="reconfirm"' in raw


def test_e2_participation_change_and_withdrawal(client):
    sid, ifc, ids, cid = _setup(client)
    _link(client, sid, cid)
    form = _icp_form(client, sid)
    assert _icp_post(client, sid, form, [ids[1]]).status_code in (200, 302)   # the board leaves ...
    form = _icp_form(client, sid)
    assert _icp_post(client, sid, form, ids).status_code in (200, 302)        # ... and comes back
    raw = _page(client, sid)
    assert _status(_block(raw, cid)) == "EARLIER" and 'data-cel-reason="reconfirm"' in raw

    sid, ifc, _ids, cid = _setup(client)
    _link(client, sid, cid)
    from tests.test_board_enclosure_planar_clearance import _fields
    data = _fields(_body(client.get(_url(sid, ifc))), form="data-pcc-withdraw-form")
    data["withdraw_confirm"] = "yes"
    assert client.post(_url(sid, ifc) + "/withdraw", data=data).status_code == 200
    raw = _page(client, sid)
    assert _status(_block(raw, cid)) == "EARLIER" and 'data-cel-reason="withdrawn"' in raw
    unlink = _form(client, sid, cid, "unlink")                           # removal stays possible
    assert _post(client, sid, unlink).status_code == 302
    assert _notice(sid)[0] == "UI_CEL_MSG_UNLINKED" and _row(sid, cid)[:2] == (None, None)


def test_f_a_link_is_never_notes_a_verdict_or_credit(client):
    sid, ifc, _ids, cid = _setup(client)
    state = appmod.SESSION_STORE[sid]["state"]
    before = ([(g.gap_type, g.status) for g in state.gaps], state.maturity_level, len(state.assertions),
              [r.requirement_id for r in derive_requirement_landscape(state).requirements])
    _link(client, sid, cid)
    state = appmod.SESSION_STORE[sid]["state"]
    assert ([(g.gap_type, g.status) for g in state.gaps], state.maturity_level, len(state.assertions),
            [r.requirement_id for r in derive_requirement_landscape(state).requirements]) == before
    assert _notes_rows(sid) == []                                        # a link is never acceptance notes
    appmod._attach_constraint_acceptance_carrier(sid, state)
    step = next(s for s in derive_validation_plan(state).steps if s.step_id.endswith(cid))
    assert step.constraint_acceptance.status == CONSTRAINT_ACCEPTANCE_NONE
    assert len(step.constraint_acceptance.missing) == 2
    raw = _page(client, sid)
    assert 'data-pca-provenance' not in _block(raw, cid)
    assert _t("UI_CEL_NOT_ASSESSED") in _block(raw, cid)
    assert _post(client, sid, _form(client, sid, cid, "unlink")).status_code == 302
    assert _row(sid, cid)[:2] == (None, None)                             # a generation-only tombstone ...
    state = appmod.SESSION_STORE[sid]["state"]
    appmod._attach_constraint_acceptance_carrier(sid, state)
    step = next(s for s in derive_validation_plan(state).steps if s.step_id.endswith(cid))
    assert step.constraint_acceptance.status == CONSTRAINT_ACCEPTANCE_NONE   # ... is never notes either
    assert _notes_rows(sid) == []
    export = client.get("/session/%s/disclosure-export.json" % sid)
    if export.status_code == 200:
        assert "constraint_engineering" not in export.get_data(as_text=True)


# ==========================================================================
# 4. independent lifecycles, retry and committed truth
# ==========================================================================
def test_l01_notes_and_link_never_reconfirm_each_other(client):
    sid, _ifc, _ids, cid = _setup(client)
    _pca_post(client, sid, _form_for(client, sid, cid), crit="Gap of 2 mm on every side")
    notes = _notes_rows(sid)
    _link(client, sid, cid)
    assert _notes_rows(sid) == notes
    link = _row(sid, cid)
    _pca_post(client, sid, _form_for(client, sid, cid), crit="Gap of 3 mm on every side")
    assert _row(sid, cid) == link
    _correct(client, sid, cid, "It must keep 3 mm clearance on every side")
    _pca_post(client, sid, _form_for(client, sid, cid), crit="Gap of 3 mm on every side")   # notes reconfirmed
    assert _status(_block(_page(client, sid), cid)) == "EARLIER"                # the link is not
    _link(client, sid, cid)
    assert _status(_block(_page(client, sid), cid)) == "CURRENT"
    assert _notes_rows(sid)[0][2] == _heads(sid)[cid].record_id


def test_l02_exact_retry_writes_nothing(client):
    sid, _ifc, _ids, cid = _setup(client)
    form = _link(client, sid, cid)
    row = _row(sid, cid)
    assert _post(client, sid, form).status_code == 302
    assert _notice(sid)[0] == "UI_CEL_MSG_UNCHANGED" and _row(sid, cid) == row
    assert _store().set_constraint_engineering_link(
        sid, cid, _heads(sid)[cid].record_id, row[1], 0) == CONSTRAINT_LINK_UNCHANGED


def test_l03_committed_truth_decides_an_unknown_outcome(client, monkeypatch):
    sid, _ifc, _ids, cid = _setup(client)
    store = _store()
    real = store.set_constraint_engineering_link

    def written_then_lost(*args):
        real(*args)
        raise RuntimeError("connection dropped after commit")
    monkeypatch.setattr(store, "set_constraint_engineering_link", written_then_lost)
    _link(client, sid, cid)
    assert _notice(sid)[0] == "UI_CEL_MSG_LINKED"

    def lost(*args):
        raise RuntimeError("dropped before write")
    monkeypatch.setattr(store, "set_constraint_engineering_link", lost)
    unlink = _form(client, sid, cid, "unlink")
    _post(client, sid, unlink)
    assert _notice(sid)[1] == "UI_CEL_MSG_NOT_SAVED" and _row(sid, cid)[1] is not None

    def unreadable(_sid):
        raise RuntimeError("cannot read")
    monkeypatch.setattr(store, "load_constraint_engineering_links", unreadable)
    _post(client, sid, unlink)
    assert _notice(sid)[1] == "UI_CEL_MSG_UNKNOWN"


def test_l04_unlink_works_when_the_check_cannot_be_read(client, monkeypatch):
    sid, _ifc, _ids, cid = _setup(client)
    _link(client, sid, cid)
    unlink = _form(client, sid, cid, "unlink")
    store = _store()

    def broken(_pid):
        raise appmod._ProjectComponentsCorrupt("unreadable")
    monkeypatch.setattr(store, "_planar_clearance_snapshot", broken)
    assert _status(_block(_page(client, sid), cid)) == "UNAVAILABLE"
    assert _post(client, sid, unlink).status_code == 302
    assert _notice(sid)[0] == "UI_CEL_MSG_UNLINKED" and _row(sid, cid)[:2] == (None, None)


def test_l05_unreadable_links_read_unavailable_never_none(client, monkeypatch):
    sid, _ifc, _ids, cid = _setup(client)

    def corrupt(_sid):
        raise ConstraintLinkCorrupt("bad")
    monkeypatch.setattr(_store(), "load_constraint_engineering_links", corrupt)
    block = _block(_page(client, sid), cid)
    assert _status(block) == "UNAVAILABLE" and _t("UI_CEL_UNAVAILABLE") in block
    assert 'data-cel-link-form' not in block


# ==========================================================================
# 5. report / PDF, language and migration
# ==========================================================================
@pytest.mark.parametrize("lang", ["en", "ar"])
def test_r01_report_and_pdf_show_the_link_beside_the_constraint_step(client, monkeypatch, lang):
    sid, ifc, _ids, cid = _setup(client, lang=lang)
    raw = _section14(client.get("/session/%s/deliverable" % sid).get_data(as_text=True))
    assert "vp-constraint-link" not in raw                                # no link: nothing added
    _link(client, sid, cid)
    for body in (client.get("/session/%s/deliverable" % sid).get_data(as_text=True),
                 _pdf_source(client, sid, monkeypatch)):
        text = _html.unescape(body)
        assert 'data-vp-constraint-link="CURRENT"' in body
        assert _t("UI_CEL_VP_LINKED", lang) in text and _t("UI_CEL_NOT_ASSESSED", lang) in text
        assert _t("UI_CEL_RESULT_MET", lang) in text
    _correct(client, sid, cid, "It must keep 2 mm clearance on every side")
    body = client.get("/session/%s/deliverable" % sid).get_data(as_text=True)
    assert 'data-vp-constraint-link="EARLIER"' in body
    block = _html.unescape(re.search(r'<div class="vp-constraint-link".*?</div>\s*</div>', body, re.S).group(0))
    assert _t("UI_CEL_RESULT_MET", lang) not in block and _t("UI_CEL_RESULT_MISSING", lang) in block


def test_r02_arabic_session_block(client):
    sid, _ifc, _ids, cid = _setup(client, lang="ar")
    _link(client, sid, cid)
    raw = _page(client, sid)
    block = _block(raw, cid)
    assert _t("UI_CEL_HEADING", "ar") in block and _t("UI_CEL_STATUS_CURRENT", "ar") in block
    assert '<bdi dir="ltr">' in block


def test_s01_migration_is_additive_idempotent_and_refuses_an_unknown_shape(tmp_path):
    from engine.record_store import SqliteRecordStore
    path = str(tmp_path / "m.db")
    SqliteRecordStore(path).close()
    SqliteRecordStore(path, create=False).close()                          # re-open: unchanged
    con = sqlite3.connect(path)
    con.execute("DROP TRIGGER constraint_engineering_links_no_delete")
    con.execute("DROP TRIGGER constraint_engineering_links_generation_grows")
    con.execute("DROP TABLE constraint_engineering_links")
    con.execute("CREATE TABLE constraint_engineering_links (project_id TEXT, other TEXT)")
    con.commit()
    con.close()
    with pytest.raises(Exception):
        SqliteRecordStore(path, create=False)


def test_s02_a_missing_trigger_makes_the_links_unreadable(client):
    sid, _ifc, _ids, cid = _setup(client)
    _link(client, sid, cid)
    con = sqlite3.connect(_db())
    con.execute("DROP TRIGGER constraint_engineering_links_no_delete")
    con.commit()
    con.close()
    with pytest.raises(ConstraintLinkCorrupt):
        _store().load_constraint_engineering_links(sid)
    assert _status(_block(_page(client, sid), cid)) == "UNAVAILABLE"


def test_s03_outcome_constants():
    assert (CONSTRAINT_LINK_LINKED, CONSTRAINT_LINK_UNLINKED, CONSTRAINT_LINK_UNCHANGED) == (
        "LINKED", "UNLINKED", "UNCHANGED")
