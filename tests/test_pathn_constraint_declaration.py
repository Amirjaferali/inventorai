"""PATHN-CONSTRAINT-DECLARATION-01 — inventor-declared project constraints.

Proves, over the real engine, the real durable store and the real web routes:

* ONE carrier on the EXISTING AssertionRecord ledger: `constraint_declared`
  (declaration or correction, with a strength) and `constraint_withdrawn`
  (terminal), OWNER_STATED / OWNER_INPUT / UNVALIDATED with every other field
  neutral; `constraint_strength` is written ONLY on a declaration, so every
  other payload stays byte-identical;
* ONE history rule shared by the carrier, the record contract on load and the
  store inside its write transaction: stale targets, exact restatements and the
  Owner capacity decision (300 characters; 50 active; 500 lifetime; 20
  corrections plus ONE reserved withdrawal) fail closed with nothing written;
* consumers are unchanged by a constraint: Requirement Landscape, Validation
  Plan (apart from the one preparation step of a CURRENT mandatory constraint,
  MANDATORY-CONSTRAINT-VERIFICATION-PREPARATION-01), next development step, readiness, SafetySignal, controlled unknowns,
  the W2-B serving trigger, gap / maturity / progression and the withdrawn-answer
  count; replay / reconstruction restores the constraints verbatim;
* the session section, the report / PDF section with its safety-scope note, the
  project-record events, EN / AR copy;
* Stage 35 export v3: field 30 carries the CURRENT constraints only (verbatim
  text, strength token, OWNER_STATED / UNVALIDATED, LEDGER); a defective history
  refuses the export; v2 fields are unchanged.

Neutral synthetic fixtures only; no study corpus.
"""
import copy
import html as _html
import json
import re

import pytest

import engine.progression_loop as pl
from engine import disclosure_export as dx
from engine.controlled_unknown_progression import report_controlled_unknowns
from engine.deliverable_assembler import assemble_deliverable
from engine.derived_readiness import derive_readiness
from engine.idea_development_outputs import derive_next_development_step
from engine.idea_state import (
    DISPOSITION_CONSTRAINT_DECLARED as DECL,
    DISPOSITION_CONSTRAINT_WITHDRAWN as WDR, MAX_ACTIVE_CONSTRAINTS_PER_PROJECT,
    MAX_CONSTRAINT_IDENTITIES_PER_PROJECT, MAX_CONSTRAINT_TEXT_LENGTH,
    MAX_CORRECTIONS_PER_CONSTRAINT, OWNER_INPUT, OWNER_STATED, UNVALIDATED,
    MECHANISM_COMPLETENESS, ConstraintCapacityError, ConstraintError,
    ConstraintStale, ConstraintUnchanged, IdeaState, constraint_history,
)
from engine.record_contract import (
    InvalidReferenceError, ProjectRecordContract, assertion_from_dict,
    assertion_to_dict,
)
from engine.record_store import ConstraintActionRejected
from engine.requirement_landscape import derive_requirement_landscape
from engine.safety_signal import derive_inventor_stated_safety_signals as derive_safety_signals
from engine.validation_plan import derive_validation_plan
from web import ui_text
import web.app as appmod
from tests.test_safe_question_routing_pf_q2 import (  # noqa: F401  (fixture)
    client, MECH, _start, _answer, _live, _store, _facts,
)

HAZARD = "If the breaker fails to disconnect power, the wiring could overheat and cause a fire."
TEXT = "It must run on batteries"


# ---------------------------------------------------------------------------
# engine helpers
# ---------------------------------------------------------------------------

def _ledger():
    s = IdeaState(idea_id="pcn")
    s.record_interaction("answered", "A spring latch locks the deck.",
                         gap_context=MECHANISM_COMPLETENESS)
    return s


def _envelope(records):
    return {"contract_version": "p4-0-record-contract-v1", "idea_id": "pcn",
            "assertions": records}


def _payloads(state):
    return [assertion_to_dict(r) for r in state.assertions]


def _load(records):
    return ProjectRecordContract.from_dict(_envelope(records))


# ===========================================================================
# 1. carrier, payload shape and load rules
# ===========================================================================

def test_declare_correct_withdraw_are_owner_stated_neutral_ledger_records():
    s = _ledger()
    d = s.record_constraint_action("declare", TEXT, "mandatory_constraint")
    assert (d.disposition, d.content, d.constraint_strength) == (DECL, TEXT, "mandatory_constraint")
    assert (d.provenance, d.responsibility, d.validation_status) == (OWNER_STATED, OWNER_INPUT, UNVALIDATED)
    assert (d.gap_context, d.question_target, d.decision_context_root, d.quality, d.pending,
            d.resolves_gap, d.contradicts, d.supersedes) == (None, None, None, None, None, False, [], [])
    c = s.record_constraint_action("correct", "It must run on AA batteries", "soft_constraint",
                                   target_record_id=d.record_id)
    assert c.supersedes == [d.record_id] and d.superseded_by == c.record_id
    w = s.record_constraint_action("withdraw", target_record_id=c.record_id)
    assert (w.disposition, w.content, w.constraint_strength, w.supersedes) == (WDR, "", None, [c.record_id])
    [only] = constraint_history(s.assertions).constraints
    assert only.withdrawn and only.history == (d.record_id, c.record_id, w.record_id)
    assert only.text == "It must run on AA batteries" and only.strength == "soft_constraint"
    assert constraint_history(s.assertions).current == ()


def test_strength_is_written_only_on_a_declaration_and_round_trips():
    s = _ledger()
    d = s.record_constraint_action("declare", TEXT, "preference")
    s.record_constraint_action("withdraw", target_record_id=d.record_id)
    payloads = _payloads(s)
    assert "constraint_strength" not in payloads[0]          # the answer: byte-identical shape
    assert payloads[1]["constraint_strength"] == "preference"
    assert "constraint_strength" not in payloads[2]          # the withdrawal
    back = _load(payloads)
    assert [r.constraint_strength for r in back.assertions] == [None, "preference", None]
    assert _payloads(back) == payloads


def test_record_interaction_and_legacy_supersession_cannot_touch_constraints():
    s = _ledger()
    d = s.record_constraint_action("declare", TEXT, "preference")
    for disp in (DECL, WDR):
        with pytest.raises(ValueError):
            s.record_interaction(disp, TEXT)
    with pytest.raises(ValueError):
        s.record_interaction("answered", "x", gap_context=MECHANISM_COMPLETENESS,
                             supersedes=[d.record_id])
    before = len(s.assertions)
    for args in [("declare", "", "preference"), ("declare", TEXT, "strong"),
                 ("declare", " padded ", "preference"), ("declare", "a\x07b", "preference"),
                 ("declare", "x" * (MAX_CONSTRAINT_TEXT_LENGTH + 1), "preference"),
                 ("correct", TEXT, "preference"), ("bogus", TEXT, "preference")]:
        with pytest.raises(ConstraintError):
            s.record_constraint_action(*args)
    with pytest.raises(ConstraintError):
        s.record_constraint_action("withdraw", "text", target_record_id=d.record_id)
    with pytest.raises(ConstraintError):           # an answer is not a constraint target
        s.record_constraint_action("withdraw", target_record_id="rec_1")
    assert len(s.assertions) == before
    s.record_constraint_action("declare", "x" * MAX_CONSTRAINT_TEXT_LENGTH, "preference")


def test_stale_and_unchanged_actions_are_refused_with_nothing_appended():
    s = _ledger()
    d = s.record_constraint_action("declare", TEXT, "preference")
    c = s.record_constraint_action("correct", TEXT, "mandatory_constraint", target_record_id=d.record_id)
    n = len(s.assertions)
    with pytest.raises(ConstraintStale):
        s.record_constraint_action("correct", "other", "preference", target_record_id=d.record_id)
    with pytest.raises(ConstraintUnchanged):
        s.record_constraint_action("correct", TEXT, "mandatory_constraint", target_record_id=c.record_id)
    s.record_constraint_action("withdraw", target_record_id=c.record_id)
    with pytest.raises(ConstraintStale):
        s.record_constraint_action("withdraw", target_record_id=c.record_id)
    assert len(s.assertions) == n + 1


def _decl(rid, text=TEXT, strength="preference", supersedes=()):
    return {"record_id": rid, "disposition": DECL, "content": text, "gap_context": None,
            "iteration": 0, "provenance": OWNER_STATED, "validation_status": UNVALIDATED,
            "quality": None, "pending": None, "responsibility": OWNER_INPUT,
            "resolves_gap": False, "contradicts": [], "supersedes": list(supersedes),
            "superseded_by": None, "decision_context_root": None, "question_target": None,
            "constraint_strength": strength}


@pytest.mark.parametrize("mutate", [
    lambda p: p.pop("constraint_strength"),
    lambda p: p.update(constraint_strength="must"),
    lambda p: p.update(content=""),
    lambda p: p.update(content="x" * 301),
    lambda p: p.update(gap_context=MECHANISM_COMPLETENESS),
    lambda p: p.update(question_target="Q"),
    lambda p: p.update(validation_status="SPECIALIST_REVIEWED"),
    lambda p: p.update(quality="ASSERTED"),
])
def test_load_refuses_a_malformed_declaration(mutate):
    answer = _payloads(_ledger())[0]
    bad = _decl("rec_2")
    mutate(bad)
    with pytest.raises(Exception):
        _load([answer, bad])


def test_load_refuses_strength_elsewhere_and_cross_class_supersession():
    answer = _payloads(_ledger())[0]
    with pytest.raises(InvalidReferenceError):
        assertion_from_dict(dict(answer, constraint_strength="preference"))
    # a constraint superseding an answer, an answer superseding a constraint,
    # and a correction naming a non-current form
    with pytest.raises(InvalidReferenceError):
        _load([answer, _decl("rec_2", supersedes=["rec_1"])])
    corr = dict(answer, record_id="rec_3", supersedes=["rec_2"])
    with pytest.raises(InvalidReferenceError):
        _load([answer, _decl("rec_2"), corr])
    with pytest.raises(InvalidReferenceError):
        _load([answer, _decl("rec_2"), _decl("rec_3", "b", supersedes=["rec_2"]),
               _decl("rec_4", "c", supersedes=["rec_2"])])


def test_load_refuses_a_forward_reference_to_a_later_constraint():
    answer = _payloads(_ledger())[0]
    tampered = dict(answer, record_id="rec_2", supersedes=["rec_3"])
    with pytest.raises(InvalidReferenceError):
        _load([answer, tampered, _decl("rec_3")])


# ===========================================================================
# 2. capacity (Owner decision D4)
# ===========================================================================

def test_active_cap_and_withdrawal_frees_a_slot():
    s = _ledger()
    made = [s.record_constraint_action("declare", "c%d" % i, "preference")
            for i in range(MAX_ACTIVE_CONSTRAINTS_PER_PROJECT)]
    with pytest.raises(ConstraintCapacityError):
        s.record_constraint_action("declare", "one more", "preference")
    s.record_constraint_action("withdraw", target_record_id=made[0].record_id)
    s.record_constraint_action("declare", "one more", "preference")
    _load(_payloads(s))


def test_lifetime_cap_counts_identities_never_recycled():
    s = _ledger()
    for i in range(MAX_CONSTRAINT_IDENTITIES_PER_PROJECT):
        d = s.record_constraint_action("declare", "c%d" % i, "preference")
        s.record_constraint_action("withdraw", target_record_id=d.record_id)
    with pytest.raises(ConstraintCapacityError):
        s.record_constraint_action("declare", "again", "preference")
    assert len(constraint_history(s.assertions).constraints) == MAX_CONSTRAINT_IDENTITIES_PER_PROJECT
    _load(_payloads(s))


def test_correction_quota_with_one_reserved_withdrawal():
    s = _ledger()
    head = s.record_constraint_action("declare", "v0", "preference")
    for i in range(MAX_CORRECTIONS_PER_CONSTRAINT):
        head = s.record_constraint_action("correct", "v%d" % (i + 1), "preference",
                                          target_record_id=head.record_id)
    with pytest.raises(ConstraintCapacityError):
        s.record_constraint_action("correct", "too many", "preference", target_record_id=head.record_id)
    s.record_constraint_action("withdraw", target_record_id=head.record_id)   # still allowed
    _load(_payloads(s))
    over = _payloads(s)[:-1] + [_decl("rec_999", "too many", supersedes=[head.record_id])]
    with pytest.raises(InvalidReferenceError):
        _load(over)


# ===========================================================================
# 3. consumers are unchanged by a constraint
# ===========================================================================

def _withdrawn_meta(state):
    # The assembler is pinned (G-3 A-20/A-21); the report seam corrects its count.
    package = assemble_deliverable(state)
    appmod._exclude_constraints_from_withdrawn_count(package, state)
    return package["_session_meta"]["withdrawn_source_records"]


def test_the_safety_owner_restates_exactly_the_constraint_dispositions():
    import engine.safety_signal as ss
    from engine.idea_state import PROJECT_CONSTRAINT_DISPOSITIONS
    assert ss._CONSTRAINT_DISPOSITIONS == PROJECT_CONSTRAINT_DISPOSITIONS


def test_withdrawn_answer_count_excludes_constraints_but_keeps_real_withdrawals():
    s = _ledger()
    d = s.record_constraint_action("declare", TEXT, "preference")
    s.record_constraint_action("withdraw", target_record_id=d.record_id)
    assert _withdrawn_meta(s) == {"total": 0, "note": None}
    s.record_interaction("answered", "A pin latch locks the deck.",
                         gap_context=MECHANISM_COMPLETENESS, supersedes=["rec_1"])
    meta = _withdrawn_meta(s)
    assert meta["total"] == 1 and meta["note"]


def _consumer_view(state):
    return (
        [(r.requirement_id, r.primary_anchor.anchor_kind, r.primary_anchor.anchor_reference)
         for r in derive_requirement_landscape(state).requirements],
        repr(derive_validation_plan(state)),
        repr(derive_next_development_step(state)),
        derive_readiness(state).overall_verified(),
        repr(derive_safety_signals(state)),
        pl._alternatives_crossing_context(state),
        _withdrawn_meta(state),
        repr(report_controlled_unknowns(state)),
    )


def test_consumers_ignore_constraints_including_a_hazard_statement():
    base = _ledger()
    before = _consumer_view(base)
    s = copy.deepcopy(base)
    d = s.record_constraint_action("declare", TEXT, "mandatory_constraint")
    c = s.record_constraint_action("correct", TEXT + " or mains", "soft_constraint",
                                   target_record_id=d.record_id)
    s.record_constraint_action("withdraw", target_record_id=c.record_id)
    current = s.record_constraint_action("declare", HAZARD, "preference")   # stays current
    assert current.superseded_by is None
    assert _consumer_view(s) == before
    # the same text as an ANSWER would be read for safety signals (control)
    control = copy.deepcopy(base)
    control.record_interaction("answered", HAZARD, gap_context=MECHANISM_COMPLETENESS)
    assert repr(derive_safety_signals(control)) != repr(derive_safety_signals(base))


def test_a_constraint_never_ends_the_multiple_alternatives_transition():
    from engine.decision_composition import declare_alternative, declare_decision_context
    s = _ledger()
    ctx = declare_decision_context(s, "Which latch design should hold?")
    declare_alternative(s, "toggle latch", ctx.record_id)
    declare_alternative(s, "spring pin", ctx.record_id)
    fired = pl._alternatives_crossing_context(s)
    assert fired is not None
    s.record_constraint_action("declare", TEXT, "preference")
    assert pl._alternatives_crossing_context(s) == fired


# ===========================================================================
# 4. web journey, store, replay, report
# ===========================================================================

def _section(c, sid):
    raw = c.get(f"/session/{sid}").get_data(as_text=True)
    start = raw.index('id="project-constraints"')
    return raw[start:raw.index("PCN-BLOCK-END") if "PCN-BLOCK-END" in raw[start:] else start + 20000]


def _submission(c, sid):
    raw = c.get(f"/session/{sid}").get_data(as_text=True)
    return _html.unescape(re.search(r'name="constraint_submission" value="([^"]*)"', raw).group(1))


def _post(c, sid, **form):
    data = {"constraint_submission": form.pop("sub", None) or _submission(c, sid),
            "constraint_confirm": "yes"}
    data.update(form)
    return c.post(f"/session/{sid}/constraint", data=data)


def _notice(sid):
    entry = appmod.SESSION_STORE[sid]
    return entry.get(appmod.CONSTRAINT_ACK_SLOT), entry.get(appmod.CONSTRAINT_ERROR_SLOT)


def _rows(sid):
    return [json.loads(p) for (p,) in _store()._conn.execute(
        "SELECT payload FROM records WHERE project_id = ? ORDER BY seq", (sid,)).fetchall()]


def _heads(sid):
    return [x for x in _live(sid).assertions if x.disposition == DECL and x.superseded_by is None]


def test_declare_retry_correct_withdraw_through_the_route(client):
    sid = _start(client)
    _answer(client, sid, MECH)
    facts = _facts(_live(sid))
    sub = _submission(client, sid)
    r = _post(client, sid, sub=sub, constraint_action="declare",
              constraint_text="  " + TEXT + "  ", constraint_strength="mandatory_constraint")
    assert r.status_code == 302 and r.headers["Location"].endswith("#project-constraints")
    assert _notice(sid) == ("UI_PCN_MSG_SAVED", None)
    rows = _rows(sid)
    assert rows[-1]["disposition"] == DECL and rows[-1]["content"] == TEXT      # trimmed, else verbatim
    assert rows[-1]["constraint_strength"] == "mandatory_constraint"
    # EXACT retry of the spent identity: recognised from committed state, nothing written
    _post(client, sid, sub=sub, constraint_action="declare", constraint_text=TEXT,
          constraint_strength="mandatory_constraint")
    assert _notice(sid) == ("UI_PCN_MSG_SAVED", None) and len(_rows(sid)) == len(rows)
    # the same identity with different material fails closed
    _post(client, sid, sub=sub, constraint_action="declare", constraint_text="other",
          constraint_strength="mandatory_constraint")
    assert _notice(sid) == (None, "UI_PCN_MSG_NOT_SAVED") and len(_rows(sid)) == len(rows)
    [head] = _heads(sid)
    _post(client, sid, constraint_action="correct", constraint_target=head.record_id,
          constraint_text=TEXT + " or mains", constraint_strength="soft_constraint")
    assert _notice(sid) == ("UI_PCN_MSG_CORRECTED", None)
    section = _html.unescape(_section(client, sid))
    assert TEXT + " or mains" in section and "data-pcn-history" in section
    assert ui_text.text("UI_PCN_STRENGTH_SOFT", "en") in section
    # stale: the old head is no longer current
    _post(client, sid, constraint_action="withdraw", constraint_target=head.record_id)
    assert _notice(sid) == (None, "UI_PCN_MSG_STALE")
    # withdrawal requires the explicit confirmation
    [new_head] = _heads(sid)
    r = client.post(f"/session/{sid}/constraint", data={
        "constraint_submission": _submission(client, sid), "constraint_action": "withdraw",
        "constraint_target": new_head.record_id})
    assert _notice(sid) == (None, "UI_PCN_MSG_CONFIRM")
    _post(client, sid, constraint_action="withdraw", constraint_target=new_head.record_id)
    assert _notice(sid) == ("UI_PCN_MSG_WITHDRAWN", None)
    section = _section(client, sid)
    assert "data-pcn-withdrawn-item" in section and "data-pcn-correct-form" not in section
    # gaps, maturity, progression and routing are untouched; only ledger rows were added
    after = _facts(_live(sid))
    assert after[:5] == facts[:5]
    assert [r for r in after[5] if r[1] not in (DECL, WDR)] == facts[5]


def test_unchanged_and_invalid_inputs_write_nothing(client):
    sid = _start(client)
    _post(client, sid, constraint_action="declare", constraint_text=TEXT,
          constraint_strength="preference")
    n = len(_rows(sid))
    [head] = _heads(sid)
    _post(client, sid, constraint_action="correct", constraint_target=head.record_id,
          constraint_text=TEXT, constraint_strength="preference")
    assert _notice(sid) == (None, "UI_PCN_MSG_UNCHANGED")
    for form in ({"constraint_text": "", "constraint_strength": "preference"},
                 {"constraint_text": TEXT, "constraint_strength": "required"},
                 {"constraint_text": "x" * 301, "constraint_strength": "preference"}):
        _post(client, sid, constraint_action="declare", **form)
        assert _notice(sid) == (None, "UI_PCN_MSG_INVALID")
    _post(client, sid, constraint_action="declare", constraint_text=TEXT,
          constraint_strength="preference", sub="forged.0000")
    assert _notice(sid) == (None, "UI_PCN_MSG_NOT_SAVED")
    assert len(_rows(sid)) == n


def test_the_store_refuses_a_stale_append_inside_its_transaction(client):
    sid = _start(client)
    _post(client, sid, constraint_action="declare", constraint_text=TEXT,
          constraint_strength="preference")
    state = _live(sid)
    [head] = _heads(sid)
    a, b = copy.deepcopy(state), copy.deepcopy(state)
    first = a.record_constraint_action("withdraw", target_record_id=head.record_id)
    second = b.record_constraint_action("correct", "other", "preference",
                                        target_record_id=head.record_id)
    _store().append_constraint_action(sid, first, idempotency_key="pcn-race-1")
    n = len(_rows(sid))
    with pytest.raises(ConstraintActionRejected) as exc:
        _store().append_constraint_action(sid, second, idempotency_key="pcn-race-2")
    assert exc.value.kind == "stale" and len(_rows(sid)) == n


def test_reconstruction_restores_constraints_and_replays_progression_unchanged(client):
    import engine.session_reconstruction as SR
    sid = _start(client)
    _answer(client, sid, MECH)
    _post(client, sid, constraint_action="declare", constraint_text=TEXT,
          constraint_strength="mandatory_constraint")
    live = _live(sid)
    recon = SR.reconstruct_readonly_state(_store(), sid)
    assert recon.review.level == 1
    got, want = constraint_history(recon.state.assertions), constraint_history(live.assertions)
    assert got == want and len(got.current) == 1
    assert [(g.gap_type, g.status) for g in recon.state.gaps] == [(g.gap_type, g.status) for g in live.gaps]
    assert recon.state.maturity_level == live.maturity_level


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_report_section_current_only_with_safety_scope_note(client, lang):
    sid = _start(client, lang=lang)
    report = client.get(f"/session/{sid}/deliverable").get_data(as_text=True)
    assert "data-pcn-report-none" in report and "data-ss-constraint-scope" not in report
    _post(client, sid, constraint_action="declare", constraint_text="Old <b>wish</b>",
          constraint_strength="preference")
    [head] = _heads(sid)
    _post(client, sid, constraint_action="withdraw", constraint_target=head.record_id)
    _post(client, sid, constraint_action="declare", constraint_text="شرط: يعمل بالبطاريات",
          constraint_strength="mandatory_constraint")
    report = client.get(f"/session/{sid}/deliverable").get_data(as_text=True)
    section = report[report.index('id="project-constraints-report"'):]
    section = section[:section.index("</section>")]
    assert section.count("data-pcn-report-item") == 1
    assert "شرط: يعمل بالبطاريات" in section and "wish" not in section
    assert _html.escape(ui_text.text("UI_PCN_STRENGTH_MANDATORY", lang), quote=False) in section
    assert _html.escape(ui_text.text("UI_SS_CONSTRAINT_SCOPE", lang), quote=False) in report
    assert "data-ss-constraint-scope" in report
    # never a requirement row; MANDATORY-CONSTRAINT-VERIFICATION-PREPARATION-01:
    # a current mandatory constraint appears once more, only as its own
    # Validation Plan preparation step
    rest = report.replace(section, "")
    assert rest.count("شرط: يعمل بالبطاريات") == 1
    assert _html.escape("Prepare how your mandatory constraint “شرط: يعمل بالبطاريات”",
                        quote=False) in rest


def test_foreign_and_anonymous_posts_are_denied_and_write_nothing():
    from tests.csrf_client import csrf_client
    from tests.test_stage19_durable_success_criteria import _client_for
    appmod.app.config["TESTING"] = True
    owner, _ = _client_for("pcn-owner@example.com")
    r = owner.post("/start", data={"idea": "a folding ramp with a spring latch",
                                   "domain_confirm": "mechanical"})
    sid = r.headers["Location"].rsplit("/", 1)[-1]
    sub = _submission(owner, sid)
    n = len(_rows(sid))
    other, _ = _client_for("pcn-other@example.com")
    for c in (other, csrf_client(appmod.app)):
        r = c.post(f"/session/{sid}/constraint", data={
            "constraint_submission": sub, "constraint_action": "declare",
            "constraint_text": TEXT, "constraint_strength": "preference",
            "constraint_confirm": "yes"})
        assert r.status_code == 302 and "#project-constraints" not in r.headers["Location"]
    assert len(_rows(sid)) == n


def test_the_pdf_carries_the_same_section_and_safety_note(client, monkeypatch):
    from tests.test_stage15_integrated_invention_entry import _pdf_source
    sid = _start(client)
    _post(client, sid, constraint_action="declare", constraint_text=TEXT,
          constraint_strength="mandatory_constraint")
    pdf = _pdf_source(client, sid, monkeypatch)
    section = pdf[pdf.index('id="project-constraints-report"'):]
    section = section[:section.index("</section>")]
    assert section.count("data-pcn-report-item") == 1 and TEXT in section
    assert "data-ss-constraint-scope" in pdf


def test_project_record_shows_constraint_events(client):
    sid = _start(client)
    _post(client, sid, constraint_action="declare", constraint_text=TEXT,
          constraint_strength="preference")
    [head] = _heads(sid)
    _post(client, sid, constraint_action="correct", constraint_target=head.record_id,
          constraint_text=TEXT + "!", constraint_strength="preference")
    [head] = _heads(sid)
    _post(client, sid, constraint_action="withdraw", constraint_target=head.record_id)
    kinds = [appmod._t3a_event_kind(r) for r in _live(sid).assertions]
    assert kinds[-3:] == ["constraint_declared", "constraint_corrected", "constraint_withdrawn"]
    record = appmod._project_record_context(_live(sid), sid)
    by_id = {e["record_id"]: e for e in record["entries"]}
    wd, corrected = _live(sid).assertions[-1], _live(sid).assertions[-2]
    assert [link["relation"] for link in by_id[wd.record_id]["links"]] == ["withdraws"]
    assert "withdrawn_in" in [link["relation"] for link in by_id[corrected.record_id]["links"]]
    assert "replaced_by" not in [link["relation"] for link in by_id[corrected.record_id]["links"]]
    assert set(kinds[-3:]) <= appmod.T3A_EVENT_KINDS
    for kind in kinds[-3:]:
        assert ui_text.has_string("UI_T3A_EVENT_" + kind.upper())


def test_new_copy_is_bilingual():
    keys = [k for k in ui_text.UI_STRINGS if k.startswith(("UI_PCN_", "UI_S35_CONSTRAINT",
                                                           "UI_SS_CONSTRAINT"))]
    keys.append("UI_S35_FIELD_PROJECT_CONSTRAINTS")
    assert len(keys) > 40
    for key in keys:
        entry = ui_text.UI_STRINGS[key]
        assert entry["en"].strip() and entry["ar"].strip() and entry["en"] != entry["ar"]


# ===========================================================================
# 5. Stage 35 export v3
# ===========================================================================

def test_field_30_carries_current_constraints_only():
    from tests.test_stage35_disclosure_projection import _rich_sources
    base = dx.compose_projection(_rich_sources())
    sources = _rich_sources()
    s = sources.state
    old = s.record_constraint_action("declare", "Old wish", "preference")
    s.record_constraint_action("withdraw", target_record_id=old.record_id)
    keep = s.record_constraint_action("declare", "Under 50 dollars", "preference")
    s.record_constraint_action("correct", "Under 40 dollars", "soft_constraint",
                               target_record_id=keep.record_id)
    s.record_constraint_action("declare", TEXT, "mandatory_constraint")
    content = dx.compose_projection(sources)
    f30 = content["fields"][-1]
    assert f30["field"] == "project_constraints" and f30["marker"] == dx.RECORDED
    texts = [(i["slots"]["text"]["value"], i["slots"]["strength"]["tokens"]["strength"])
             for i in f30["items"]]
    assert texts == [("Under 40 dollars", "soft_constraint"), (TEXT, "mandatory_constraint")]
    item = f30["items"][0]
    assert item["kind"] == "constraint" and item["refs"] == [] and item["tokens"] == {}
    assert item["slots"]["text"]["source_owner"] == "LEDGER"
    env = item["slots"]["text"]["envelope"]
    assert env["provenance"]["value"] == OWNER_STATED and env["validation_state"]["value"] == UNVALIDATED
    blob = json.dumps(content)
    assert "Old wish" not in blob and "Under 50 dollars" not in blob and "rec_" not in blob
    # every v2 field is unchanged by constraints
    assert content["fields"][:-1] == base["fields"][:-1]
    assert base["fields"][-1] == {"field": "project_constraints", "marker": dx.NOTHING_RECORDED,
                                  "reason": None, "pointer": None, "items": []}


def test_a_defective_constraint_history_refuses_the_export():
    from tests.test_stage35_disclosure_projection import _rich_sources
    sources = _rich_sources()
    d = sources.state.record_constraint_action("declare", TEXT, "preference")
    d.constraint_strength = "required"                   # corrupted after mint
    with pytest.raises(dx.DisclosureExportRefused):
        dx.compose_projection(sources)


@pytest.mark.parametrize("mutate", [
    lambda i: i["slots"]["strength"]["tokens"].update(strength="must"),
    lambda i: i["refs"].append("parts.1"),
    lambda i: i["slots"].pop("strength"),
    lambda i: i["slots"]["strength"].update(value="soft"),
])
def test_the_schema_check_refuses_a_malformed_constraint_item(mutate):
    from tests.test_stage35_disclosure_projection import _rich_sources
    sources = _rich_sources()
    sources.state.record_constraint_action("declare", TEXT, "preference")
    content = dx.compose_projection(sources)
    mutate(content["fields"][-1]["items"][0])
    with pytest.raises(dx.DisclosureExportRefused):
        dx.check_projection(content)


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_v3_html_renders_the_constraint_item(lang):
    from tests.test_stage35_disclosure_projection import _rich_sources
    sources = _rich_sources()
    sources.state.record_constraint_action("declare", "Weight <2 kg", "mandatory_constraint")
    content = dx.compose_projection(sources)
    doc = dx.export_document(content, "2026-10-24T00:00:00Z", dx.HTML_FORMAT_VERSION)
    with appmod.app.test_request_context():
        markup = appmod._disclosure_document_html(doc, lang)
    section = markup[markup.index('id="field-project_constraints"'):]
    assert 'data-kind="constraint"' in section and "data-constraints-clarification" in section
    assert "Weight &lt;2 kg" in section and "<2 kg" not in section
    assert 'data-constraint-strength="mandatory_constraint"' in section
    assert ui_text.text("UI_S35_FIELD_PROJECT_CONSTRAINTS", lang) in markup
    assert "inventorai-disclosure-html/3" in markup
