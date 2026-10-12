"""INVENTOR-DECLARED-ALTERNATIVE-CRITERIA-VALUES-01 — focused tests.

The inventor's own comparison criteria for a decision and the value they record
for each criterion and each ACTIVE alternative: OWNER_STATED / UNVALIDATED,
append-only (Option B: two additive store tables), bound to the exact
question / criterion / alternative versions, paged at a 200-cell display
budget, complete-or-omitted in the report / PDF, and never a score, ranking,
winner, ClaimItem, Constraint, ledger disposition or FDC-001 input.

Synthetic data only. Boundary states are built with direct, VALID inserts (the
store validates the whole history on every read), then exercised through the
store API exactly at the bound.
"""
import html
import os
import re
import sqlite3
import threading
import time

import pytest

from engine import decision_composition as dc
from engine import decision_criteria as cr
from engine.idea_state import (
    DISPOSITION_DECISION_ALTERNATIVE_DECLARED,
    DISPOSITION_DECISION_CONTEXT_DECLARED,
    IdeaState,
)
from engine.record_contract import ProjectRecordContract
from engine.record_store import (
    DECISION_COMPARISON_EXACT_REPLAY,
    DECISION_COMPARISON_INSERTED,
    DECISION_COMPARISON_NO_CHANGE,
    DecisionComparisonConflict,
    DecisionComparisonCorrupt,
    MAX_CRITERION_REVISION_ROWS_PER_PROJECT,
    MAX_VALUE_EVENT_ROWS_PER_PROJECT,
    SqliteRecordStore,
)
from tests.csrf_client import csrf_client
from web import ui_text
from web.ui_text import text

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ---------------------------------------------------------------------------
# store-level fixture: one project, its decisions built through the ledger
# ---------------------------------------------------------------------------

class Project:
    def __init__(self, path, alternatives=2, decisions=1, project_id="p1"):
        self.path = path
        self.store = SqliteRecordStore(path)
        self.state = IdeaState(idea_id="idea-" + project_id)
        self.sid = self.store.create_project(
            ProjectRecordContract.from_state(self.state), project_id=project_id)
        self.keys = 0
        self.decisions = []
        for d in range(decisions):
            ctx = self.add(dc.declare_decision_context(self.state, f"Question {d}?"))
            alts = [self.add(dc.declare_alternative(
                self.state, f"Alternative {d}.{i}", ctx.record_id))
                for i in range(alternatives)]
            self.decisions.append((ctx.record_id, [a.record_id for a in alts]))
        self.ctx, self.alts = self.decisions[0] if self.decisions else (None, [])

    def add(self, record):
        self.store.append_record(self.sid, record)
        return record

    def key(self):
        self.keys += 1
        return f"k{self.keys}"

    def ledger(self):
        return self.store.load_decision_comparison(self.sid)

    def frame(self, ctx=None):
        return self.ledger().frames[ctx or self.ctx]

    def declare(self, label="Weight added", ctx=None, key=None):
        ctx = ctx or self.ctx
        return self.store.append_criterion_action(
            self.sid, key or self.key(), cr.ACTION_DECLARE, ctx,
            self.frame(ctx).question_record_id, label=label)

    def criterion(self, action, crit_id, label=None, key=None):
        ledger = self.ledger()
        record = ledger.criteria[crit_id]
        return self.store.append_criterion_action(
            self.sid, key or self.key(), action, record.context_root,
            ledger.frames[record.context_root].question_record_id,
            criterion_id=crit_id, expected_revision_no=record.head.revision_no,
            label=label)

    def expected(self, crit_id, alt_root):
        ledger = self.ledger()
        record = ledger.criteria[crit_id]
        frame = ledger.frames[record.context_root]
        cell = ledger.cells.get((crit_id, alt_root))
        return (record.context_root, crit_id, alt_root,
                cell.head.event_no if cell else 0, record.head.revision_id,
                frame.alternative(alt_root).head_record_id,
                frame.question_record_id)

    def value(self, action, crit_id, alt_root, text_=None, key=None):
        args = self.expected(crit_id, alt_root)
        return self.store.append_value_action(
            self.sid, key or self.key(), action, *args, text=text_)

    def rows(self):
        with sqlite3.connect(self.path) as conn:
            return (conn.execute(
                "SELECT COUNT(*) FROM decision_criterion_revisions").fetchone()[0],
                conn.execute(
                "SELECT COUNT(*) FROM decision_cell_value_events").fetchone()[0])

    def refine(self, alt_root, content):
        head = self.frame().alternative(alt_root)
        return self.add(dc.refine_alternative(self.state, content, head.head_record_id))

    def withdraw_alt(self, alt_root):
        head = self.frame().alternative(alt_root)
        return self.add(dc.withdraw_alternative(self.state, head.head_record_id, "no"))


@pytest.fixture()
def proj(tmp_path):
    return Project(str(tmp_path / "cmp.sqlite"))


class Bulk:
    """Direct, VALID inserts that build a boundary state quickly. Tracks the
    heads it writes; the store re-validates everything on the next read."""

    def __init__(self, project):
        self.p = project
        ledger = project.ledger()
        self.frames = ledger.frames
        self.crit = {cid: {"ctx": r.context_root, "no": r.head.revision_no,
                           "rev": r.head.revision_id, "label": r.label,
                           "n": len(r.revisions)}
                     for cid, r in ledger.criteria.items()}
        self.cells = {k: {"no": c.head.event_no, "text": c.text}
                      for k, c in ledger.cells.items()}
        conn = sqlite3.connect(project.path)
        self.cseq = conn.execute(
            "SELECT COUNT(*) FROM decision_criterion_revisions").fetchone()[0]
        self.vseq = conn.execute(
            "SELECT COUNT(*) FROM decision_cell_value_events").fetchone()[0]
        conn.close()
        self.crows, self.vrows, self.n = [], [], 0

    def _id(self, prefix):
        self.n += 1
        return prefix + "%032x" % (self.n + 7 * 10 ** 9)

    def declare(self, ctx, label=None):
        cid, rid = self._id("crt-"), self._id("ccr-")
        label = label or f"Criterion {cid[-6:]}"
        self.crows.append((self.p.sid, self.cseq, ctx, cid, 1, rid, "DECLARED",
                           label, self.frames[ctx].question_record_id,
                           "OWNER_STATED", "UNVALIDATED", "bulk-c%d" % self.cseq))
        self.cseq += 1
        self.crit[cid] = {"ctx": ctx, "no": 1, "rev": rid, "label": label}
        return cid

    def revise(self, cid, kind):
        c = self.crit[cid]
        rid = self._id("ccr-")
        c["no"] += 1
        if kind == "CORRECTED":
            c["label"] = "%s/%d" % (c["label"][:150], c["no"])
            label = c["label"]
        elif kind == "RECONFIRMED":
            label = c["label"]
        else:
            label = None
        self.crows.append((self.p.sid, self.cseq, c["ctx"], cid, c["no"], rid, kind,
                           label, self.frames[c["ctx"]].question_record_id,
                           "OWNER_STATED", "UNVALIDATED", "bulk-c%d" % self.cseq))
        self.cseq += 1
        if kind != "WITHDRAWN":
            c["rev"] = rid

    def event(self, cid, alt, kind, reserved=False):
        c = self.crit[cid]
        cell = self.cells.setdefault((cid, alt), {"no": 0, "text": None})
        cell["no"] += 1
        if kind in ("SET", "CORRECTED"):
            cell["text"] = "v%d" % self.vseq
        elif kind == "CLEARED":
            cell["text"] = None
        frame = self.frames[c["ctx"]]
        self.vrows.append((
            self.p.sid, self.vseq, c["ctx"], cid, alt, cell["no"], self._id("cve-"),
            kind, 1 if reserved else 0,
            None if kind == "CLEARED" else cell["text"], c["rev"],
            frame.alternative(alt).head_record_id, frame.question_record_id,
            "OWNER_STATED", "UNVALIDATED", "bulk-v%d" % self.vseq))
        self.vseq += 1

    def flush(self):
        with sqlite3.connect(self.p.path) as conn:
            conn.executemany(
                "INSERT INTO decision_criterion_revisions VALUES "
                "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", self.crows)
            conn.executemany(
                "INSERT INTO decision_cell_value_events VALUES "
                "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", self.vrows)
        self.crows, self.vrows = [], []


# ---------------------------------------------------------------------------
# lifecycle, binding and staleness
# ---------------------------------------------------------------------------

def test_declare_correct_reconfirm_withdraw_lifecycle(proj):
    outcome, rev = proj.declare("Weight added")
    assert outcome == DECISION_COMPARISON_INSERTED and rev.kind == cr.CRITERION_DECLARED
    assert rev.provenance == "OWNER_STATED" and rev.validation_state == "UNVALIDATED"
    cid = rev.criterion_id
    assert proj.criterion(cr.ACTION_CORRECT, cid, "Weight added (g)")[1].kind \
        == cr.CRITERION_CORRECTED
    record = proj.ledger().criteria[cid]
    assert record.label == "Weight added (g)"
    assert record.labels == ("Weight added", "Weight added (g)")
    # unchanged wording bound to the current question: a genuine no-op
    assert proj.criterion(cr.ACTION_CORRECT, cid, "Weight added (g)") \
        == (DECISION_COMPARISON_NO_CHANGE, None)
    assert proj.criterion(cr.ACTION_RECONFIRM, cid) == (DECISION_COMPARISON_NO_CHANGE, None)
    assert proj.criterion(cr.ACTION_WITHDRAW, cid)[1].kind == cr.CRITERION_WITHDRAWN
    with pytest.raises(cr.ComparisonRejected) as exc:
        proj.criterion(cr.ACTION_CORRECT, cid, "again")
    assert exc.value.reason == cr.REJECT_CRITERION_WITHDRAWN
    # the history is kept; a re-declaration is a NEW identity
    again = proj.declare("Weight added")[1]
    assert again.criterion_id != cid
    ledger = proj.ledger()
    assert ledger.criteria[cid].withdrawn and len(ledger.criteria[cid].revisions) == 3
    assert [c.criterion_id for c in ledger.active_criteria_of(proj.ctx)] == [again.criterion_id]


def test_value_lifecycle_and_states(proj):
    cid = proj.declare()[1].criterion_id
    a1, a2 = proj.alts
    assert proj.value(cr.ACTION_SAVE, cid, a1, "about 300 g")[1].kind == cr.VALUE_SET
    assert proj.value(cr.ACTION_SAVE, cid, a1, "about 320 g")[1].kind == cr.VALUE_CORRECTED
    view = cr.comparison_view(proj.ledger())
    cells = view["decisions"][proj.ctx]["groups"][0]["cells"]
    assert [(c["state"], c["text"]) for c in cells] == [
        (cr.STATE_RECORDED, "about 320 g"), (cr.STATE_NOT_RECORDED, None)]
    assert proj.value(cr.ACTION_CLEAR, cid, a1)[1].kind == cr.VALUE_CLEARED
    cells = cr.comparison_view(proj.ledger())["decisions"][proj.ctx]["groups"][0]["cells"]
    assert cells[0]["state"] == cr.STATE_CLEARED and cells[0]["text"] is None
    # a cleared cell takes a value again (SET), the text stays verbatim
    assert proj.value(cr.ACTION_SAVE, cid, a1, "  12  ")[1].value_text == "12"
    assert proj.value(cr.ACTION_SAVE, cid, a2, "٣٠٠ غرام")[1].kind == cr.VALUE_SET


def test_noops_write_nothing(proj):
    cid = proj.declare()[1].criterion_id
    a1, a2 = proj.alts
    proj.value(cr.ACTION_SAVE, cid, a1, "300 g")
    before = proj.rows()
    assert proj.value(cr.ACTION_SAVE, cid, a1, "300 g") == (DECISION_COMPARISON_NO_CHANGE, None)
    assert proj.value(cr.ACTION_RECONFIRM, cid, a1) == (DECISION_COMPARISON_NO_CHANGE, None)
    assert proj.value(cr.ACTION_CLEAR, cid, a2) == (DECISION_COMPARISON_NO_CHANGE, None)
    proj.value(cr.ACTION_CLEAR, cid, a1)
    after_clear = proj.rows()
    assert proj.value(cr.ACTION_CLEAR, cid, a1) == (DECISION_COMPARISON_NO_CHANGE, None)
    assert proj.rows() == after_clear == (before[0], before[1] + 1)


@pytest.mark.parametrize("change", ["alternative", "criterion", "question"])
def test_changed_version_needs_confirmation_and_is_never_rebound(proj, change):
    cid = proj.declare()[1].criterion_id
    a1 = proj.alts[0]
    proj.value(cr.ACTION_SAVE, cid, a1, "300 g")
    if change == "alternative":
        proj.refine(a1, "Alternative 0.0 with a longer pin")
    elif change == "criterion":
        proj.criterion(cr.ACTION_CORRECT, cid, "Weight added in grams")
    else:
        proj.add(proj.state.record_interaction(
            action=DISPOSITION_DECISION_CONTEXT_DECLARED,
            content="Which hinge, given the new door?", supersedes=[proj.ctx]))
    ledger = proj.ledger()
    cell = ledger.cells[(cid, a1)]
    assert change in ledger.cell_staleness(cell)
    view = cr.comparison_view(ledger, writable=True)
    shown = view["decisions"][proj.ctx]["groups"][0]["cells"][0]
    assert shown["state"] == cr.STATE_NEEDS_CONFIRMATION and shown["text"] == "300 g"
    if change == "question":
        # the criterion itself needs confirmation first; the value can only be cleared
        assert view["decisions"][proj.ctx]["criteria"][0]["state"] == cr.STATE_NEEDS_CONFIRMATION
        with pytest.raises(cr.ComparisonRejected) as exc:
            proj.value(cr.ACTION_RECONFIRM, cid, a1)
        assert exc.value.reason == cr.REJECT_CONFIRM_CRITERION_FIRST
        assert proj.criterion(cr.ACTION_RECONFIRM, cid)[1].kind == cr.CRITERION_RECONFIRMED
    # an explicit reconfirmation (never an inference) makes it current
    assert proj.value(cr.ACTION_RECONFIRM, cid, a1)[1].kind == cr.VALUE_RECONFIRMED
    assert not proj.ledger().cell_staleness(proj.ledger().cells[(cid, a1)])


def test_saving_the_same_text_over_a_stale_binding_is_a_reconfirmation(proj):
    cid = proj.declare()[1].criterion_id
    a1 = proj.alts[0]
    proj.value(cr.ACTION_SAVE, cid, a1, "300 g")
    proj.refine(a1, "Alternative 0.0 refined")
    assert proj.value(cr.ACTION_SAVE, cid, a1, "300 g")[1].kind == cr.VALUE_RECONFIRMED


def test_alternative_withdrawal_removes_its_row_keeps_history_and_redeclaration_inherits_nothing(proj):
    cid = proj.declare()[1].criterion_id
    a1, a2 = proj.alts
    proj.value(cr.ACTION_SAVE, cid, a2, "kept in history")
    proj.withdraw_alt(a2)
    ledger = proj.ledger()
    assert (cid, a2) in ledger.cells                  # history kept
    cells = cr.comparison_view(ledger)["decisions"][proj.ctx]["groups"][0]["cells"]
    assert [c["alternative_root"] for c in cells] == [a1]
    with pytest.raises(cr.ComparisonRejected) as exc:
        proj.store.append_value_action(
            proj.sid, "kx", cr.ACTION_SAVE, proj.ctx, cid, a2, 1,
            ledger.criteria[cid].head.revision_id, ledger.cells[(cid, a2)].head.alternative_record_id,
            ledger.frames[proj.ctx].question_record_id, text="x")
    assert exc.value.reason == cr.REJECT_ALTERNATIVE_WITHDRAWN
    new = proj.add(dc.declare_alternative(proj.state, "Alternative 0.1", proj.ctx))
    cells = cr.comparison_view(proj.ledger())["decisions"][proj.ctx]["groups"][0]["cells"]
    assert [(c["alternative_root"], c["state"]) for c in cells] == [
        (a1, cr.STATE_NOT_RECORDED), (new.record_id, cr.STATE_NOT_RECORDED)]


def test_stale_expected_versions_are_refused_and_write_nothing(proj):
    cid = proj.declare()[1].criterion_id
    a1 = proj.alts[0]
    proj.value(cr.ACTION_SAVE, cid, a1, "first")
    before = proj.rows()
    current = proj.expected(cid, a1)
    # event no, criterion revision, alternative revision, question revision
    for index, wrong in ((3, 0), (4, "ccr-" + "0" * 32), (5, "rec_999"), (6, "rec_999")):
        stale = list(current)
        stale[index] = wrong
        with pytest.raises(cr.ComparisonStale):
            proj.store.append_value_action(proj.sid, proj.key(), cr.ACTION_SAVE,
                                           *stale, text="second")
    with pytest.raises(cr.ComparisonStale):
        proj.store.append_criterion_action(
            proj.sid, proj.key(), cr.ACTION_CORRECT, proj.ctx,
            proj.frame().question_record_id, criterion_id=cid,
            expected_revision_no=7, label="other")
    assert proj.rows() == before


def test_exact_retry_replays_and_a_reused_identity_with_other_material_conflicts(proj):
    rev = proj.declare("Cost", key="decl-1")[1]
    assert proj.store.append_criterion_action(
        proj.sid, "decl-1", cr.ACTION_DECLARE, proj.ctx,
        proj.frame().question_record_id, label="Cost") == (DECISION_COMPARISON_EXACT_REPLAY, rev)
    with pytest.raises(DecisionComparisonConflict):
        proj.store.append_criterion_action(
            proj.sid, "decl-1", cr.ACTION_DECLARE, proj.ctx,
            proj.frame().question_record_id, label="Price")
    a1 = proj.alts[0]
    args = proj.expected(rev.criterion_id, a1)
    first = proj.store.append_value_action(proj.sid, "val-1", cr.ACTION_SAVE, *args, text="12")
    rows = proj.rows()
    assert proj.store.append_value_action(proj.sid, "val-1", cr.ACTION_SAVE, *args, text="12") \
        == (DECISION_COMPARISON_EXACT_REPLAY, first[1])
    with pytest.raises(DecisionComparisonConflict):
        proj.store.append_value_action(proj.sid, "val-1", cr.ACTION_SAVE, *args, text="13")
    assert proj.rows() == rows
    assert proj.store.committed_value_event_for_submission(proj.sid, "val-1") == first[1]


def test_text_bounds_and_characters(proj):
    with pytest.raises(cr.ComparisonRejected) as exc:
        proj.declare("x" * 201)
    assert exc.value.reason == cr.REJECT_TEXT_TOO_LONG
    assert proj.declare("x" * 200)[0] == DECISION_COMPARISON_INSERTED
    cid = proj.ledger().criterion_order[0]
    for bad, reason in (("", cr.REJECT_TEXT_EMPTY), ("   ", cr.REJECT_TEXT_EMPTY),
                        ("a\x00b", cr.REJECT_TEXT_CHAR),
                        ("v" * 1001, cr.REJECT_TEXT_TOO_LONG)):
        with pytest.raises(cr.ComparisonRejected) as exc:
            proj.value(cr.ACTION_SAVE, cid, proj.alts[0], bad)
        assert exc.value.reason == reason
    assert proj.value(cr.ACTION_SAVE, cid, proj.alts[0], "v" * 1000)[0] \
        == DECISION_COMPARISON_INSERTED


def test_values_are_never_parsed_scored_or_fed_to_the_decision_record(proj):
    before = [r.__dict__ for r in dc.compose_decision_records(proj.state)]
    ledger_before = len(proj.store.load_contract(proj.sid).assertions)
    cid = proj.declare("Cost")[1].criterion_id
    proj.value(cr.ACTION_SAVE, cid, proj.alts[0], "12")
    proj.value(cr.ACTION_SAVE, cid, proj.alts[1], "9.5")
    assert [r.__dict__ for r in dc.compose_decision_records(proj.state)] == before
    assert len(proj.store.load_contract(proj.sid).assertions) == ledger_before
    view = cr.comparison_view(proj.ledger())
    texts = [c["text"] for c in view["decisions"][proj.ctx]["groups"][0]["cells"]]
    assert texts == ["12", "9.5"] and all(isinstance(t, str) for t in texts)
    keys = set()

    def walk(node):
        if isinstance(node, dict):
            keys.update(node)
            for v in node.values():
                walk(v)
        elif isinstance(node, (list, tuple)):
            for v in node:
                walk(v)

    walk(view)
    for word in ("score", "rank", "winner", "best", "weight", "preferred", "number"):
        assert not [k for k in keys if word in k], word


# ---------------------------------------------------------------------------
# Owner-approved capacity — at and over every bound
# ---------------------------------------------------------------------------

def test_active_criteria_bound_and_withdrawal_frees_a_slot(proj):
    for i in range(10):
        proj.declare(f"C{i}")
    with pytest.raises(cr.ComparisonLimitReached) as exc:
        proj.declare("C10")
    assert exc.value.limit == cr.LIMIT_ACTIVE_CRITERIA
    view = cr.comparison_view(proj.ledger(), writable=True)["decisions"][proj.ctx]
    assert not view["can_declare"] and view["declare_limit"] == cr.LIMIT_ACTIVE_CRITERIA
    first = proj.ledger().criterion_order[0]
    proj.criterion(cr.ACTION_WITHDRAW, first)
    assert proj.declare("C10")[0] == DECISION_COMPARISON_INSERTED


def test_decision_lifetime_bound_blocks_new_identities_only(proj):
    bulk = Bulk(proj)
    ids = [bulk.declare(proj.ctx) for _ in range(29)]
    for cid in ids[:25]:
        bulk.revise(cid, "WITHDRAWN")
    bulk.flush()
    assert proj.declare("the 30th")[0] == DECISION_COMPARISON_INSERTED
    with pytest.raises(cr.ComparisonLimitReached) as exc:
        proj.declare("the 31st")
    assert exc.value.limit == cr.LIMIT_DECISION_CRITERIA
    # existing criteria still revise; another decision still declares
    assert proj.criterion(cr.ACTION_CORRECT, ids[-1], "still correctable")[0] \
        == DECISION_COMPARISON_INSERTED


def test_project_lifetime_bound(tmp_path):
    p = Project(str(tmp_path / "life.sqlite"), decisions=6, alternatives=1)
    bulk = Bulk(p)
    for ctx, _alts in p.decisions[:5]:
        for i in range(30):
            cid = bulk.declare(ctx)
            if i >= 5:
                bulk.revise(cid, "WITHDRAWN")
    bulk.flush()
    other = p.decisions[5][0]
    with pytest.raises(cr.ComparisonLimitReached) as exc:
        p.declare("the 151st", ctx=other)
    assert exc.value.limit == cr.LIMIT_PROJECT_CRITERIA
    view = cr.comparison_view(p.ledger(), writable=True)["decisions"][other]
    assert view["declare_limit"] == cr.LIMIT_PROJECT_CRITERIA


def test_criterion_revision_bounds_and_reserved_withdrawal(proj):
    cid = proj.declare("C")[1].criterion_id
    for i in range(10):
        proj.criterion(cr.ACTION_CORRECT, cid, f"C{i}")
    with pytest.raises(cr.ComparisonLimitReached) as exc:
        proj.criterion(cr.ACTION_CORRECT, cid, "C11")
    assert exc.value.limit == cr.LIMIT_CRITERION_REVISIONS
    view = cr.comparison_view(proj.ledger(), writable=True)["decisions"][proj.ctx]
    assert view["criteria"][0]["can_revise"] is False
    assert view["criteria"][0]["revise_limit"] == cr.LIMIT_CRITERION_REVISIONS
    assert proj.criterion(cr.ACTION_WITHDRAW, cid)[1].kind == cr.CRITERION_WITHDRAWN


def test_project_criterion_revision_bound_is_distinct(tmp_path):
    p = Project(str(tmp_path / "rev.sqlite"), decisions=10, alternatives=1)
    bulk = Bulk(p)
    for ctx, _alts in p.decisions:
        for _ in range(10):
            cid = bulk.declare(ctx)
            for _ in range(10):
                bulk.revise(cid, "CORRECTED")
    bulk.flush()
    ledger = p.ledger()
    assert ledger.project_ordinary_criterion_revisions == 1000
    # fresh criterion in a decision with room is impossible here (10 active each),
    # so withdraw one and declare a new one: its FIRST correction is refused by
    # the PROJECT bound, not the criterion bound.
    victim = ledger.criterion_order[0]
    p.criterion(cr.ACTION_WITHDRAW, victim)                 # reserved: allowed
    fresh = p.declare("fresh", ctx=p.decisions[0][0])[1].criterion_id
    with pytest.raises(cr.ComparisonLimitReached) as exc:
        p.criterion(cr.ACTION_CORRECT, fresh, "fresh 2")
    assert exc.value.limit == cr.LIMIT_PROJECT_CRITERION_REVISIONS
    assert _cmp_key(exc.value) == "UI_CMP_LIMIT_PROJECT_CRITERION_REVISIONS"


def _cmp_key(exc, text_key="UI_CMP_MSG_VALUE_TOO_LONG"):
    import web.app as appmod
    return appmod._cmp_refusal(exc, text_key)


def test_cell_bound_counts_first_set_and_ordinary_clears_then_reserved_clear(proj):
    cid = proj.declare()[1].criterion_id
    a1 = proj.alts[0]
    proj.value(cr.ACTION_SAVE, cid, a1, "t0")                    # 1 (SET)
    for i in range(1, 9):                                        # 2..9
        proj.value(cr.ACTION_SAVE, cid, a1, f"t{i}")
    proj.value(cr.ACTION_CLEAR, cid, a1)                         # 10 (ordinary clear)
    cell = proj.ledger().cells[(cid, a1)]
    assert cell.ordinary == 10 and not cell.events[-1].reserved
    with pytest.raises(cr.ComparisonLimitReached) as exc:
        proj.value(cr.ACTION_SAVE, cid, a1, "t10")
    assert exc.value.limit == cr.LIMIT_CELL_EVENTS and exc.value.can_still_clear is False
    assert _cmp_key(exc.value) == "UI_CMP_LIMIT_CELL_EVENTS"     # never promises a clear


def test_reserved_clear_under_exhaustion_closes_the_cell(proj):
    cid = proj.declare()[1].criterion_id
    a1 = proj.alts[0]
    proj.value(cr.ACTION_SAVE, cid, a1, "t0")
    for i in range(1, 10):
        proj.value(cr.ACTION_SAVE, cid, a1, f"t{i}")             # 10 ordinary
    with pytest.raises(cr.ComparisonLimitReached) as exc:
        proj.value(cr.ACTION_SAVE, cid, a1, "t10")
    assert exc.value.can_still_clear is True
    assert _cmp_key(exc.value) == "UI_CMP_LIMIT_CELL_EVENTS_CLEAR"
    event = proj.value(cr.ACTION_CLEAR, cid, a1)[1]
    assert event.kind == cr.VALUE_CLEARED and event.reserved is True and event.event_no == 11
    view = cr.comparison_view(proj.ledger(), writable=True)
    shown = view["decisions"][proj.ctx]["groups"][0]["cells"][0]
    assert shown["closed"] and shown["state"] == cr.STATE_CLEARED
    assert not (shown["can_save"] or shown["can_clear"] or shown["can_reconfirm"])
    with pytest.raises(cr.ComparisonRejected) as exc:
        proj.value(cr.ACTION_SAVE, cid, a1, "again")
    assert exc.value.reason == cr.REJECT_CELL_CLOSED
    assert proj.value(cr.ACTION_CLEAR, cid, a1) == (DECISION_COMPARISON_NO_CHANGE, None)


def test_stale_value_stays_stale_when_reconfirmation_quota_is_exhausted(proj):
    cid = proj.declare()[1].criterion_id
    a1 = proj.alts[0]
    for i in range(10):
        proj.value(cr.ACTION_SAVE, cid, a1, f"t{i}")
    proj.refine(a1, "Alternative 0.0 refined")
    with pytest.raises(cr.ComparisonLimitReached):
        proj.value(cr.ACTION_RECONFIRM, cid, a1)
    ledger = proj.ledger()
    assert ledger.cell_staleness(ledger.cells[(cid, a1)]) == (cr.STALE_ALTERNATIVE,)
    shown = cr.comparison_view(ledger, writable=True)["decisions"][proj.ctx]["groups"][0]["cells"][0]
    assert shown["state"] == cr.STATE_NEEDS_CONFIRMATION and not shown["can_reconfirm"]
    assert shown["can_clear"]                                    # the reserved clear remains


def _value_bulk(path, decisions, alternatives, criteria, ordinary_per_cell):
    """Every cell of ``decisions`` decisions (``criteria`` x ``alternatives``
    each) holding ``ordinary_per_cell`` ordinary events."""
    p = Project(path, decisions=decisions, alternatives=alternatives)
    bulk = Bulk(p)
    for ctx, alts in p.decisions:
        for cid in [bulk.declare(ctx) for _ in range(criteria)]:
            for alt in alts:
                bulk.event(cid, alt, "SET")
                for _ in range(ordinary_per_cell - 1):
                    bulk.event(cid, alt, "CORRECTED")
    bulk.flush()
    return p


def test_decision_value_bound(tmp_path):
    p = _value_bulk(str(tmp_path / "dv.sqlite"), 1, 10, 5, 10)    # 500 ordinary
    ledger = p.ledger()
    assert ledger.decision_ordinary_value_events(p.ctx) == 500
    cid, alt = next(iter(ledger.cells))
    with pytest.raises(cr.ComparisonLimitReached) as exc:
        p.value(cr.ACTION_SAVE, cid, alt, "one more")
    assert exc.value.limit == cr.LIMIT_CELL_EVENTS                 # the most specific bound
    # an UNWRITTEN cell of the same decision meets the DECISION bound
    crit = p.declare("room", ctx=p.ctx)[1].criterion_id
    with pytest.raises(cr.ComparisonLimitReached) as exc:
        p.value(cr.ACTION_SAVE, crit, p.alts[0], "x")
    assert exc.value.limit == cr.LIMIT_DECISION_VALUE_EVENTS
    assert _cmp_key(exc.value) == "UI_CMP_LIMIT_DECISION_VALUE_EVENTS"
    assert p.value(cr.ACTION_CLEAR, cid, alt)[1].reserved is True   # reserved clear remains


def test_project_value_and_cell_bounds(tmp_path):
    # 10 decisions x (10 criteria x 15 alternatives) x 2 ordinary = 3,000
    # ordinary events over 1,500 cells, 300 per decision (under its 500)
    p = _value_bulk(str(tmp_path / "pv.sqlite"), 10, 15, 10, 2)
    ledger = p.ledger()
    assert ledger.project_ordinary_value_events == 3000 and len(ledger.cells) == 1500
    assert max(ledger.decision_value_counts.values()) == 300
    cid, alt = next(iter(ledger.cells))
    with pytest.raises(cr.ComparisonLimitReached) as exc:
        p.value(cr.ACTION_SAVE, cid, alt, "changed")
    assert exc.value.limit == cr.LIMIT_PROJECT_VALUE_EVENTS and exc.value.can_still_clear
    assert _cmp_key(exc.value) == "UI_CMP_LIMIT_PROJECT_VALUE_EVENTS_CLEAR"
    assert p.value(cr.ACTION_CLEAR, cid, alt)[1].reserved is True


def test_distinct_cell_bound_blocks_new_cells_only(tmp_path):
    # 1,500 cells with ONE ordinary event each: the cell bound, not the event bounds
    p = _value_bulk(str(tmp_path / "pc.sqlite"), 10, 15, 10, 1)
    extra = p.add(dc.declare_decision_context(p.state, "Another question?"))
    alt = p.add(dc.declare_alternative(p.state, "Another alternative", extra.record_id))
    crit = p.declare("fresh", ctx=extra.record_id)[1].criterion_id
    with pytest.raises(cr.ComparisonLimitReached) as exc:
        p.value(cr.ACTION_SAVE, crit, alt.record_id, "new cell")
    assert exc.value.limit == cr.LIMIT_PROJECT_CELLS
    assert _cmp_key(exc.value) == "UI_CMP_LIMIT_PROJECT_CELLS"
    # an EXISTING cell still takes an ordinary event
    cid, a = next(iter(p.ledger().cells))
    assert p.value(cr.ACTION_SAVE, cid, a, "changed")[1].kind == cr.VALUE_CORRECTED


def test_worst_case_5800_logical_records(tmp_path, capsys):
    """150 declared + 1,000 ordinary criterion revisions + 150 withdrawals +
    3,000 ordinary value events + 1,500 reserved clears = 5,800 logical
    records, held in exactly 1,300 + 4,500 physical rows. The whole history
    validates; one more row of either family is refused by the database."""
    assert cr.MAX_LOGICAL_RECORDS_PER_PROJECT == 5800
    path = str(tmp_path / "worst.sqlite")
    p = Project(path, decisions=6, alternatives=10)
    bulk = Bulk(p)
    crits = []
    for ctx, alts in p.decisions:
        mine = [bulk.declare(ctx) for _ in range(25)]          # 6 x 25 = 150
        crits.extend(mine)
        for cid in mine:
            for alt in alts:                                   # 25 x 10 = 250 cells
                bulk.event(cid, alt, "SET")
                bulk.event(cid, alt, "CORRECTED")              # 500 ordinary
                bulk.event(cid, alt, "CLEARED", reserved=True)  # 250 reserved
    for cid in crits[:100]:
        for _ in range(10):
            bulk.revise(cid, "CORRECTED")                      # 1,000 ordinary
    for cid in crits:
        bulk.revise(cid, "WITHDRAWN")                          # 150 reserved
    bulk.flush()
    assert p.rows() == (1300, 4500)
    assert (MAX_CRITERION_REVISION_ROWS_PER_PROJECT, MAX_VALUE_EVENT_ROWS_PER_PROJECT) \
        == (1300, 4500)
    started = time.perf_counter()
    ledger = p.ledger()
    elapsed = time.perf_counter() - started
    size = os.path.getsize(path)
    assert len(ledger.criteria) == 150 and ledger.project_ordinary_criterion_revisions == 1000
    assert sum(r.withdrawn for r in ledger.criteria.values()) == 150
    assert ledger.project_ordinary_value_events == 3000 and len(ledger.cells) == 1500
    assert all(c.closed for c in ledger.cells.values())
    with capsys.disabled():
        print("\n[worst case] logical=5800 rows=1300+4500 db_bytes=%d load_validate_s=%.3f"
              % (size, elapsed))
    assert elapsed < 10
    # every further logical record is refused
    with pytest.raises(cr.ComparisonLimitReached):
        p.declare("one more", ctx=p.ctx)
    with sqlite3.connect(path) as conn:
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(
                "INSERT INTO decision_criterion_revisions VALUES "
                "(?, 1300, ?, ?, 1, ?, 'DECLARED', 'x', ?, 'OWNER_STATED', "
                "'UNVALIDATED', 'over')",
                (p.sid, p.ctx, "crt-" + "f" * 32, "ccr-" + "f" * 32, p.ctx))
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(
                "INSERT INTO decision_cell_value_events VALUES "
                "(?, 4500, ?, ?, ?, 1, ?, 'SET', 0, 'x', ?, ?, ?, 'OWNER_STATED', "
                "'UNVALIDATED', 'over')",
                (p.sid, p.ctx, crits[0], p.alts[0], "cve-" + "f" * 32,
                 "ccr-" + "e" * 32, p.alts[0], p.ctx))


# ---------------------------------------------------------------------------
# concurrency — serialized inside the write transaction
# ---------------------------------------------------------------------------

def _race(path, sid, calls):
    results = [None] * len(calls)
    barrier = threading.Barrier(len(calls))

    def run(index):
        store = SqliteRecordStore(path)
        barrier.wait()
        try:
            results[index] = ("ok", calls[index](store))
        except Exception as exc:              # noqa: BLE001 — recorded for the assertion
            results[index] = ("refused", exc)
        finally:
            store.close()

    threads = [threading.Thread(target=run, args=(i,)) for i in range(len(calls))]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return results


def test_concurrent_declarations_respect_the_active_bound(proj):
    for i in range(9):
        proj.declare(f"C{i}")
    q = proj.frame().question_record_id
    calls = [lambda s, k=k: s.append_criterion_action(
        proj.sid, k, cr.ACTION_DECLARE, proj.ctx, q, label=k) for k in ("ra", "rb", "rc")]
    results = _race(proj.path, proj.sid, calls)
    assert sum(r[0] == "ok" for r in results) == 1
    assert all(isinstance(r[1], cr.ComparisonLimitReached) for r in results if r[0] == "refused")
    assert len(proj.ledger().active_criteria_of(proj.ctx)) == 10


def test_concurrent_saves_of_one_cell_one_wins_the_rest_are_stale(proj):
    cid = proj.declare()[1].criterion_id
    args = proj.expected(cid, proj.alts[0])
    calls = [lambda s, k=k: s.append_value_action(
        proj.sid, k, cr.ACTION_SAVE, *args, text=k) for k in ("sa", "sb", "sc")]
    results = _race(proj.path, proj.sid, calls)
    assert sum(r[0] == "ok" for r in results) == 1
    assert all(isinstance(r[1], cr.ComparisonStale) for r in results if r[0] == "refused")
    assert proj.ledger().cells[(cid, proj.alts[0])].head.event_no == 1


# ---------------------------------------------------------------------------
# the 200-cell display budget
# ---------------------------------------------------------------------------

def _grid(path, shape):
    """Decisions with (criteria, alternatives) per ``shape``; no values."""
    p = Project(path, decisions=0, alternatives=0)
    bulk_frames = []
    for crits, alts in shape:
        ctx = p.add(dc.declare_decision_context(p.state, "Q?"))
        roots = [p.add(dc.declare_alternative(p.state, f"A{i}", ctx.record_id)).record_id
                 for i in range(alts)]
        bulk_frames.append((ctx.record_id, roots, crits))
    bulk = Bulk(p)
    for ctx, _roots, crits in bulk_frames:
        for _ in range(crits):
            bulk.declare(ctx)
    bulk.flush()
    return p


def _cells(view):
    out = []
    for root in view["order"]:
        for g in view["decisions"][root]["groups"]:
            out.extend((root, g["criterion_id"], c["alternative_root"]) for c in g["cells"])
    return out


@pytest.mark.parametrize("shape,total", [
    (((10, 10), (9, 11)), 199), (((10, 10), (10, 10)), 200), (((10, 10), (10, 10), (1, 1)), 201)])
def test_budget_below_at_and_above_with_several_decisions(tmp_path, shape, total):
    p = _grid(str(tmp_path / "b.sqlite"), shape)
    ledger = p.ledger()
    assert cr.display_size(ledger)[0] == total
    page1 = cr.comparison_view(ledger, page=1)
    assert len(_cells(page1)) == min(total, 200)
    assert page1["pages"] == (1 if total <= 200 else 2)
    report = cr.comparison_view(ledger, complete_only=True)
    if total <= 200:
        assert report["status"] == cr.STATUS_AVAILABLE and len(_cells(report)) == total
    else:
        assert report["status"] == cr.STATUS_OMITTED_SIZE and _cells(report) == []
        assert {d["window"] for d in report["decisions"].values()} == {"omitted"}
        # the criteria themselves stay listed
        assert all(d["criteria"] for d in report["decisions"].values())


def test_pagination_is_complete_canonical_and_never_silently_omits(tmp_path):
    p = _grid(str(tmp_path / "pg.sqlite"), ((9, 23), (3, 40), (10, 7)))
    ledger = p.ledger()
    total = cr.display_size(ledger)[0]
    assert total == 207 + 120 + 70
    view = cr.comparison_view(ledger)
    seen = []
    for page in range(1, view["pages"] + 1):
        v = cr.comparison_view(ledger, page=page)
        cells = _cells(v)
        assert len(cells) <= 200 and v["first_cell"] == (page - 1) * 200 + 1
        seen.extend(cells)
        for root, d in v["decisions"].items():
            assert d["window"] in ("all", "partial", "elsewhere", "empty")
            if d["window"] == "elsewhere":
                assert d["first_page"] != page and d["groups"] == []
    canonical = [(root, c.criterion_id, a.root)
                 for root in ledger.frames
                 for c in ledger.active_criteria_of(root)
                 for a in ledger.frames[root].active_alternatives]
    assert seen == canonical and len(set(seen)) == total
    # a criterion split across pages is marked on both sides
    v1, v2 = cr.comparison_view(ledger, page=1), cr.comparison_view(ledger, page=2)
    first = list(ledger.frames)[0]
    after = [g["criterion_id"] for g in v1["decisions"][first]["groups"] if g["continues_after"]]
    before = [g["criterion_id"] for g in v2["decisions"][first]["groups"] if g["continued_before"]]
    assert after == before and len(after) == 1
    assert v1["decisions"][first]["window"] == v2["decisions"][first]["window"] == "partial"
    # out-of-range and malformed pages clamp, never empty
    assert cr.comparison_view(ledger, page=99)["page"] == view["pages"]
    assert cr.comparison_view(ledger, page="x")["page"] == 1


def test_display_size_is_computed_before_expanding_the_grid(tmp_path, monkeypatch):
    p = _grid(str(tmp_path / "lazy.sqlite"), ((10, 60),))
    ledger = p.ledger()
    calls = []
    real = cr._cell_view
    monkeypatch.setattr(cr, "_cell_view", lambda *a, **k: calls.append(1) or real(*a, **k))
    cr.comparison_view(ledger, page=2)
    assert len(calls) == 200                   # only the window is expanded
    calls.clear()
    cr.comparison_view(ledger, complete_only=True)
    assert calls == []                         # omitted: nothing expanded


# ---------------------------------------------------------------------------
# whole-history validation, migration, rollback
# ---------------------------------------------------------------------------

def test_any_history_defect_fails_the_whole_comparison_closed(proj):
    cid = proj.declare()[1].criterion_id
    proj.value(cr.ACTION_SAVE, cid, proj.alts[0], "x")
    rev = proj.ledger().criteria[cid].head.revision_id
    with sqlite3.connect(proj.path) as conn:          # event 3 after event 1: a gap
        conn.execute("INSERT INTO decision_cell_value_events VALUES "
                     "(?, 1, ?, ?, ?, 3, ?, 'CORRECTED', 0, 'gap', ?, ?, ?, "
                     "'OWNER_STATED', 'UNVALIDATED', 'gap')",
                     (proj.sid, proj.ctx, cid, proj.alts[0], "cve-" + "a" * 32,
                      rev, proj.alts[0], proj.ctx))
    with pytest.raises(DecisionComparisonCorrupt):
        proj.ledger()


def test_foreign_binding_is_corrupt(proj):
    cid = proj.declare()[1].criterion_id
    rev = proj.ledger().criteria[cid].head.revision_id
    with sqlite3.connect(proj.path) as conn:
        conn.execute("INSERT INTO decision_cell_value_events VALUES "
                     "(?, 0, ?, ?, ?, 1, ?, 'SET', 0, 'x', ?, ?, ?, "
                     "'OWNER_STATED', 'UNVALIDATED', 'foreign')",
                     (proj.sid, proj.ctx, cid, proj.alts[0], "cve-" + "c" * 32,
                      rev, proj.alts[1], proj.ctx))       # binds ANOTHER alternative
    with pytest.raises(DecisionComparisonCorrupt):
        proj.ledger()


def test_migration_is_additive_idempotent_and_refuses_an_unknown_shape(tmp_path):
    path = str(tmp_path / "m.sqlite")
    p = Project(path)
    cid = p.declare("kept")[1].criterion_id
    p.store.close()
    again = SqliteRecordStore(path)              # idempotent reopen keeps data
    assert again.load_decision_comparison(p.sid).criteria[cid].label == "kept"
    again.close()
    # a database from before this capability gains the two tables, data intact
    with sqlite3.connect(path) as conn:
        conn.execute("DROP TABLE decision_cell_value_events")
        conn.execute("DROP TABLE decision_criterion_revisions")
    reopened = SqliteRecordStore(path)
    assert reopened.load_decision_comparison(p.sid).criteria == {}
    assert len(reopened.load_contract(p.sid).assertions) == 3
    reopened.close()
    # an unrecognised shape is refused, never read as empty
    with sqlite3.connect(path) as conn:
        conn.execute("DROP TABLE decision_cell_value_events")
        conn.execute("CREATE TABLE decision_cell_value_events (project_id TEXT, x TEXT)")
    with pytest.raises(sqlite3.DatabaseError):
        SqliteRecordStore(path)


def test_a_missing_table_reads_unavailable_never_empty(proj):
    with sqlite3.connect(proj.path) as conn:
        conn.execute("DROP TABLE decision_cell_value_events")
    with pytest.raises(sqlite3.Error):
        proj.ledger()


def test_rollback_disable_then_refine_and_withdraw_then_reenable_detects_mismatch(tmp_path):
    path = str(tmp_path / "rb.sqlite")
    p = Project(path, alternatives=3)
    cid = p.declare("Cost")[1].criterion_id
    a1, a2, a3 = p.alts
    for alt in (a1, a2, a3):
        p.value(cr.ACTION_SAVE, cid, alt, "value of " + alt)
    rows = p.rows()
    p.store.close()
    # "disabled" build: only the decision ledger changes; the comparison tables
    # are neither read nor written, and their rows stay intact
    disabled = SqliteRecordStore(path)
    disabled.append_record(p.sid, dc.refine_alternative(p.state, "refined", a1))
    disabled.append_record(p.sid, dc.withdraw_alternative(p.state, a2, "gone"))
    disabled.close()
    # re-enabled build: every binding is re-checked against the ledger as it stands
    enabled = SqliteRecordStore(path)
    ledger = enabled.load_decision_comparison(p.sid)
    view = cr.comparison_view(ledger)
    cells = {c["alternative_root"]: c for c in view["decisions"][p.ctx]["groups"][0]["cells"]}
    assert set(cells) == {a1, a3}                         # the withdrawn row is gone
    assert cells[a1]["state"] == cr.STATE_NEEDS_CONFIRMATION
    assert cells[a1]["stale"] == (cr.STALE_ALTERNATIVE,)
    assert cells[a3]["state"] == cr.STATE_RECORDED
    assert (cid, a2) in ledger.cells                      # history preserved
    with sqlite3.connect(path) as conn:
        assert (conn.execute("SELECT COUNT(*) FROM decision_criterion_revisions").fetchone()[0],
                conn.execute("SELECT COUNT(*) FROM decision_cell_value_events").fetchone()[0]) == rows
    enabled.close()


def test_ir01_unresolved_connection_refuses_reads_and_writes(proj):
    proj.store._connection_unsafe = True
    from engine.record_store import RecordStoreConnectionUnsafe
    with pytest.raises(RecordStoreConnectionUnsafe):
        proj.ledger()
    with pytest.raises(RecordStoreConnectionUnsafe):
        proj.store.append_criterion_action(proj.sid, "k", cr.ACTION_DECLARE, proj.ctx,
                                           proj.ctx, label="x")


# ---------------------------------------------------------------------------
# ownership boundaries (static)
# ---------------------------------------------------------------------------

def test_boundaries_decision_composition_stays_pure_and_nothing_else_reads_values():
    src = open(os.path.join(_ROOT, "engine", "decision_composition.py"), encoding="utf-8").read()
    for token in ("sqlite", "record_store", "decision_criteria", "json.dump"):
        assert token not in src, token
    users = []
    for folder in ("engine", "web"):
        for name in sorted(os.listdir(os.path.join(_ROOT, folder))):
            if name.endswith(".py"):
                body = open(os.path.join(_ROOT, folder, name), encoding="utf-8").read()
                if "decision_criteria" in body:
                    users.append(f"{folder}/{name}")
    assert users == ["engine/decision_criteria.py", "engine/record_store.py", "web/app.py"]
    import ast
    tree = ast.parse(open(os.path.join(_ROOT, "engine", "decision_criteria.py"),
                          encoding="utf-8").read())
    names = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
    names |= {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)}
    names |= {a.name for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))
              for a in n.names}
    modules = {n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)}
    for token in ("ClaimItem", "Constraint", "DecisionRecord", "Candidate",
                  "record_interaction", "float", "Decimal", "sqlite3", "requests"):
        assert token not in names, token
    assert modules <= {"engine.decision_composition", "engine.idea_state"}, modules
    for name in ("deliverable_assembler.py", "disclosure_export.py", "decision_workspace.py"):
        body = open(os.path.join(_ROOT, "engine", name), encoding="utf-8").read()
        for token in ("decision_criteria", "decision_cell_value", "decision_criterion_revisions",
                      "load_decision_comparison"):
            assert token not in body, (name, token)


def test_every_new_string_has_distinct_en_and_ar_and_no_ranking_vocabulary():
    keys = [k for k in ui_text.UI_STRINGS if k.startswith("UI_CMP_")]
    assert len(keys) >= 90
    for key in keys:
        entry = ui_text.UI_STRINGS[key]
        assert entry["en"].strip() and entry["ar"].strip() and entry["en"] != entry["ar"], key
        assert re.search(r"[؀-ۿ]", entry["ar"]), key
        for bad in ("winner", "best option", "recommended", "ranked", "superior",
                    "validated", "verified", "confidence"):
            assert bad not in entry["en"].lower().replace("unvalidated", ""), (key, bad)
        for value in entry.values():
            assert not re.search("[\u200e\u200f\u202a-\u202e\u2066-\u2069]", value), key


# ---------------------------------------------------------------------------
# web: Decision Room, report, PDF
# ---------------------------------------------------------------------------

SEED = ("a manually foldable wheelchair ramp for a home doorway — the inventor "
        "wants the ramp to stay reliably locked in the flat, load-bearing "
        "position and to fold away without tools")


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("INVENTORAI_DB_PATH", str(tmp_path / "web.sqlite"))
    import web.app as appmod
    monkeypatch.setattr(appmod, "_STORE", None)
    appmod.SESSION_STORE.clear()
    appmod.app.config["TESTING"] = True
    with csrf_client(appmod.app) as c:
        yield c, appmod, str(tmp_path / "web.sqlite")


def _token(c, sid):
    page = c.get(f"/session/{sid}").get_data(as_text=True)
    return html.unescape(re.search(r'name="answer_token" value="([^"]+)"', page).group(1))


def _journey(c, appmod, lang="en", alternatives=("Piano hinge", "Two barrel hinges")):
    with c.session_transaction() as session:
        session["ui_lang"] = lang
    r = c.post("/start", data={"idea": SEED, "domain_confirm": "mechanical"})
    sid = r.headers["Location"].rsplit("/", 1)[-1]
    c.post(f"/session/{sid}/decision/declare-context",
           data={"content": "Which hinge?", "answer_token": _token(c, sid)})
    state = appmod.SESSION_STORE[sid]["state"]
    ctx = [x for x in state.assertions
           if x.disposition == DISPOSITION_DECISION_CONTEXT_DECLARED][0].record_id
    for alt in alternatives:
        c.post(f"/session/{sid}/decision/declare-alternative",
               data={"content": alt, "context_root": ctx, "answer_token": _token(c, sid)})
    return sid, ctx


def _forms(page, marker):
    found = []
    for body in re.findall(r"<form[^>]*%s[^>]*>(.*?)</form>" % marker, page, re.S):
        found.append({k: html.unescape(v) for k, v in re.findall(
            r'<input type="hidden" name="([^"]+)" value="([^"]*)"', body)})
    return found


def _notice(page):
    return ([html.unescape(m) for m in re.findall(r"data-cmp-ack[^>]*>([^<]*)<", page)],
            [html.unescape(m) for m in re.findall(r"data-cmp-error[^>]*>([^<]*)<", page)])


def _page(c, sid, page=None):
    url = f"/session/{sid}" + (f"?cmp_page={page}" if page else "")
    return c.get(url).get_data(as_text=True)


def _declare_via_form(c, sid, label):
    form = _forms(_page(c, sid), "data-cmp-declare-form")[0]
    form.update(cmp_action="declare", criterion_label=label)
    return c.post(f"/session/{sid}/decision/criterion", data=form)


def _value_form(c, sid, index=0):
    return _forms(_page(c, sid), "data-cmp-value-form")[index]


def _dump(path):
    with sqlite3.connect(path) as conn:
        return list(conn.iterdump())


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_web_declare_save_retry_and_render_en_ar(client, lang):
    c, appmod, db = client
    sid, ctx = _journey(c, appmod, lang)
    page = _page(c, sid)
    assert text("UI_CMP_HEADING", lang) in page and text("UI_CMP_NO_CRITERIA", lang) in page
    r = _declare_via_form(c, sid, "Weight added")
    assert r.status_code == 302 and r.headers["Location"].endswith("#cmp-" + ctx)
    page = _page(c, sid)
    assert _notice(page)[0] == [text("UI_CMP_MSG_CRITERION_ADDED", lang)]
    form = _value_form(c, sid)
    form.update(cmp_action="save", value_text="about 300 g")
    c.post(f"/session/{sid}/decision/value", data=form)
    rows = _dump(db)
    c.post(f"/session/{sid}/decision/value", data=form)            # exact retry
    page = _page(c, sid)
    assert _notice(page)[0] == [text("UI_CMP_MSG_VALUE_SAVED", lang)]
    assert _dump(db) == rows                                        # nothing new
    assert re.findall(r'data-cmp-state="([a-z_]+)"', page) == ["recorded", "not_recorded"]
    assert '<bdi dir="auto" data-cmp-text style="white-space:pre-wrap">about 300 g</bdi>' in page
    # the SAME identity with other material fails closed
    form.update(value_text="about 999 g")
    c.post(f"/session/{sid}/decision/value", data=form)
    assert _notice(_page(c, sid))[1] == [text("UI_CMP_MSG_NOT_SAVED", lang)]
    assert _dump(db) == rows


def test_web_tampered_binding_is_rejected_and_writes_nothing(client):
    c, appmod, db = client
    sid, ctx = _journey(c, appmod)
    _declare_via_form(c, sid, "Cost")
    first, second = _forms(_page(c, sid), "data-cmp-value-form")
    rows = _dump(db)
    tampered = dict(first, alternative_root=second["alternative_root"],
                    alternative_record=second["alternative_record"],
                    cmp_action="save", value_text="x")
    c.post(f"/session/{sid}/decision/value", data=tampered)
    assert _notice(_page(c, sid))[1] == [text("UI_CMP_MSG_REJECTED", "en")]
    for field, value in (("cmp_binding", "0" * 64), ("context_root", "rec_99"),
                         ("cmp_submission", "forged")):
        bad = dict(first, cmp_action="save", value_text="x", **{field: value})
        c.post(f"/session/{sid}/decision/value", data=bad)
        assert _notice(_page(c, sid))[1], field
    assert _dump(db) == rows


def test_web_stale_form_after_refinement_and_needs_confirmation_flow(client):
    c, appmod, db = client
    sid, ctx = _journey(c, appmod)
    _declare_via_form(c, sid, "Cost")
    form = _value_form(c, sid)
    c.post(f"/session/{sid}/decision/value", data=dict(form, cmp_action="save",
                                                        value_text="12 USD"))
    stale_form = _value_form(c, sid)
    state = appmod.SESSION_STORE[sid]["state"]
    head = [r for r in state.assertions if r.disposition == DISPOSITION_DECISION_ALTERNATIVE_DECLARED
            and r.superseded_by is None][0]
    c.post(f"/session/{sid}/decision/refine-alternative", data={
        "content": "Piano hinge, stainless", "supersedes_record_id": head.record_id,
        "answer_token": _token(c, sid)})
    rows = _dump(db)
    c.post(f"/session/{sid}/decision/value", data=dict(stale_form, cmp_action="save",
                                                        value_text="13 USD"))
    page = _page(c, sid)
    assert _notice(page)[1] == [text("UI_CMP_MSG_STALE", "en")]
    assert _dump(db) == rows
    assert 'data-cmp-state="needs_confirmation"' in page
    assert 'data-cmp-stale-reason="alternative"' in page
    assert "Piano hinge, stainless" in page and "12 USD" in page
    fresh = _value_form(c, sid)
    c.post(f"/session/{sid}/decision/value", data=dict(fresh, cmp_action="reconfirm"))
    page = _page(c, sid)
    assert _notice(page)[0] == [text("UI_CMP_MSG_VALUE_RECONFIRMED", "en")]
    assert 'data-cmp-state="needs_confirmation"' not in page


def test_web_noop_clear_withdraw_and_limits(client):
    c, appmod, db = client
    sid, ctx = _journey(c, appmod)
    _declare_via_form(c, sid, "Cost")
    form = _value_form(c, sid)
    c.post(f"/session/{sid}/decision/value", data=dict(form, cmp_action="save",
                                                        value_text="12"))
    form = _value_form(c, sid)
    c.post(f"/session/{sid}/decision/value", data=dict(form, cmp_action="save",
                                                        value_text="12"))
    assert _notice(_page(c, sid))[0] == [text("UI_CMP_MSG_NO_CHANGE", "en")]
    form = _value_form(c, sid)
    c.post(f"/session/{sid}/decision/value", data=dict(form, cmp_action="clear"))
    page = _page(c, sid)
    assert _notice(page)[0] == [text("UI_CMP_MSG_VALUE_CLEARED", "en")]
    assert 'data-cmp-state="cleared"' in page
    # withdrawal needs the explicit confirmation box
    wform = _forms(page, "data-cmp-withdraw-form")[0]
    c.post(f"/session/{sid}/decision/criterion", data=dict(wform, cmp_action="withdraw"))
    assert _notice(_page(c, sid))[1] == [text("UI_CMP_MSG_CONFIRM_WITHDRAW", "en")]
    wform = _forms(_page(c, sid), "data-cmp-withdraw-form")[0]
    c.post(f"/session/{sid}/decision/criterion",
           data=dict(wform, cmp_action="withdraw", withdraw_confirm="yes"))
    page = _page(c, sid)
    assert _notice(page)[0] == [text("UI_CMP_MSG_CRITERION_WITHDRAWN", "en")]
    assert "data-cmp-withdrawn" in page and "data-cmp-table" not in page
    # active bound: the form disappears and a direct post is refused with its reason
    for i in range(10):
        _declare_via_form(c, sid, f"C{i}")
    page = _page(c, sid)
    assert "data-cmp-declare-form" not in page
    assert text("UI_CMP_CAP_ACTIVE_CRITERIA", "en") in page


def test_web_criterion_correct_and_too_long_label(client):
    c, appmod, db = client
    sid, ctx = _journey(c, appmod)
    _declare_via_form(c, sid, "Cost")
    form = _forms(_page(c, sid), "data-cmp-criterion-form")[0]
    c.post(f"/session/{sid}/decision/criterion",
           data=dict(form, cmp_action="correct", criterion_label="x" * 201))
    assert _notice(_page(c, sid))[1] == [text("UI_CMP_MSG_LABEL_TOO_LONG", "en")]
    c.post(f"/session/{sid}/decision/criterion",
           data=dict(form, cmp_action="correct", criterion_label="Cost per unit"))
    page = _page(c, sid)
    assert _notice(page)[0] == [text("UI_CMP_MSG_CRITERION_CORRECTED", "en")]
    assert "Cost per unit" in page and text("UI_CMP_EARLIER_LABELS", "en") in page


def test_web_unknown_when_the_outcome_cannot_be_read(client, monkeypatch):
    c, appmod, db = client
    sid, ctx = _journey(c, appmod)
    _declare_via_form(c, sid, "Cost")
    form = _value_form(c, sid)
    store = appmod._get_store()
    monkeypatch.setattr(store, "append_value_action",
                        lambda *a, **k: (_ for _ in ()).throw(sqlite3.OperationalError("x")))
    real = store.committed_value_event_for_submission
    calls = []

    def flaky(*a, **k):
        calls.append(1)
        if len(calls) > 1:
            raise sqlite3.OperationalError("unreadable")
        return real(*a, **k)

    monkeypatch.setattr(store, "committed_value_event_for_submission", flaky)
    c.post(f"/session/{sid}/decision/value", data=dict(form, cmp_action="save",
                                                        value_text="12"))
    assert _notice(_page(c, sid))[1] == [text("UI_CMP_MSG_UNKNOWN", "en")]


def test_web_views_write_nothing(client, monkeypatch):
    c, appmod, db = client
    sid, ctx = _journey(c, appmod)
    _declare_via_form(c, sid, "Cost")
    form = _value_form(c, sid)
    c.post(f"/session/{sid}/decision/value", data=dict(form, cmp_action="save",
                                                        value_text="12"))
    rows = _dump(db)
    monkeypatch.setattr(appmod, "_render_pdf_bytes", lambda source: b"%PDF-")
    for _ in range(2):
        _page(c, sid)
        _page(c, sid, page=7)
        c.get(f"/session/{sid}/deliverable")
        c.post(f"/session/{sid}/deliverable.pdf", data={})
    assert _dump(db) == rows


def test_web_cold_read_only_view_shows_values_without_controls(client):
    c, appmod, db = client
    sid, ctx = _journey(c, appmod)
    _declare_via_form(c, sid, "Cost")
    form = _value_form(c, sid)
    c.post(f"/session/{sid}/decision/value", data=dict(form, cmp_action="save",
                                                        value_text="12 USD"))
    appmod.SESSION_STORE[sid]["state"].domain = None          # cold read-only view
    page = _page(c, sid)
    assert "12 USD" in page and "data-cmp-table" in page
    for marker in ("data-cmp-value-form", "data-cmp-declare-form",
                   "data-cmp-criterion-form", "data-cmp-withdraw-form"):
        assert marker not in page


def test_web_reads_one_store_snapshot_never_cached_session_text(client):
    c, appmod, db = client
    sid, ctx = _journey(c, appmod)
    _declare_via_form(c, sid, "Cost")
    state = appmod.SESSION_STORE[sid]["state"]
    for r in state.assertions:
        if r.disposition == DISPOSITION_DECISION_ALTERNATIVE_DECLARED:
            r.content = "CACHED ONLY"
    page = _page(c, sid)
    table = page[page.index("data-cmp-table"):]
    table = table[:table.index("</table>")]
    assert "Piano hinge" in table and "CACHED ONLY" not in table


def test_web_pagination_and_report_omission(client, monkeypatch):
    c, appmod, db = client
    sid, ctx = _journey(c, appmod, alternatives=tuple(f"Alt {i}" for i in range(23)))
    for i in range(9):
        _declare_via_form(c, sid, f"C{i}")
    # 9 x 23 = 207 cells: page 1 ends inside the ninth criterion
    page1 = _page(c, sid)
    assert page1.count("data-cmp-cell ") == 200
    assert 'data-cmp-pager="top"' in page1 and "data-cmp-next" in page1
    assert "data-cmp-continues-after" in page1
    page2 = _page(c, sid, page=2)
    assert page2.count("data-cmp-cell ") == 7 and "data-cmp-continued-before" in page2
    assert "data-cmp-prev" in page2 and "data-cmp-partial" in page2
    report = c.get(f"/session/{sid}/deliverable").get_data(as_text=True)
    assert "data-cmp-report-omitted-notice" in report
    assert text("UI_CMP_REPORT_OMITTED", "en").replace("{total}", "207") in html.unescape(report)
    assert "data-cmp-cell " not in report and "data-cmp-report-omitted" in report
    assert report.count("data-cmp-label") == 9                 # criteria still listed
    assert 'id="report-decisions"' in report                    # the rest is intact
    seen = {}
    monkeypatch.setattr(appmod, "_render_pdf_bytes",
                        lambda source: seen.setdefault("s", source) and b"%PDF-")
    c.post(f"/session/{sid}/deliverable.pdf", data={})
    assert "data-cmp-report-omitted-notice" in seen["s"] and "data-cmp-cell " not in seen["s"]


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_web_report_and_pdf_carry_every_value_within_budget(client, monkeypatch, lang):
    c, appmod, db = client
    sid, ctx = _journey(c, appmod, lang)
    _declare_via_form(c, sid, "Cost")
    form = _value_form(c, sid)
    c.post(f"/session/{sid}/decision/value", data=dict(form, cmp_action="save",
                                                        value_text="12 USD"))
    report = c.get(f"/session/{sid}/deliverable").get_data(as_text=True)
    block = report[report.index('data-cmp-surface="report"'):]
    block = block[:block.index("</section>")]
    assert "12 USD" in block and block.count("data-cmp-cell ") == 2
    for tag in ("<form", "<input", "<textarea", "<button", "<details"):
        assert tag not in block, tag
    assert text("UI_CMP_NOT_RECORDED", lang) in block
    seen = {}
    monkeypatch.setattr(appmod, "_render_pdf_bytes",
                        lambda source: seen.setdefault("s", source) and b"%PDF-")
    c.post(f"/session/{sid}/deliverable.pdf", data={})
    assert "12 USD" in seen["s"] and text("UI_CMP_HEADING", lang) in seen["s"]


def test_web_unavailable_comparison_fails_closed_and_the_report_still_renders(client):
    c, appmod, db = client
    sid, ctx = _journey(c, appmod)
    _declare_via_form(c, sid, "Cost")
    with sqlite3.connect(db) as conn:
        conn.execute("UPDATE decision_criterion_revisions SET context_root = 'rec_999'")
    page = _page(c, sid)
    assert "data-cmp-unavailable" in page and "data-cmp-declare-form" not in page
    assert text("UI_CMP_UNAVAILABLE", "en") in page
    report = c.get(f"/session/{sid}/deliverable").get_data(as_text=True)
    assert text("UI_CMP_REPORT_UNAVAILABLE", "en") in report
    assert 'id="report-decisions"' in report and "Piano hinge" in report
    assert "data-cmp-report-omitted" not in report


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_web_real_pdf_renders_the_comparison(client, monkeypatch, lang):
    c, appmod, db = client
    sid, ctx = _journey(c, appmod, lang)
    _declare_via_form(c, sid, "Cost")
    form = _value_form(c, sid)
    c.post(f"/session/{sid}/decision/value",
           data=dict(form, cmp_action="save", value_text="١٢ دولارًا" if lang == "ar" else "12 USD"))
    seen = {}
    real = appmod._render_pdf_bytes

    def spy(source):
        seen["source"] = source
        return real(source)

    monkeypatch.setattr(appmod, "_render_pdf_bytes", spy)
    r = c.post(f"/session/{sid}/deliverable.pdf", data={})
    assert r.status_code == 200 and r.mimetype == "application/pdf"
    assert r.data[:5] == b"%PDF-"
    source = seen["source"]
    assert 'data-cmp-surface="report"' in source and text("UI_CMP_HEADING", lang) in source
    assert ("١٢ دولارًا" if lang == "ar" else "12 USD") in source
