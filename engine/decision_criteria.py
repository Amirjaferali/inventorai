"""INVENTOR-DECLARED-ALTERNATIVE-CRITERIA-VALUES-01 — the inventor's own
comparison criteria and the values they record for each alternative.

For ONE decision (a ``decision_context_declared`` chain of the ledger) the
inventor may declare up to ten current CRITERIA in their own words, and for
each current criterion and each ACTIVE alternative record ONE VALUE in their
own words. Everything here is OWNER_STATED / UNVALIDATED. InventorAI parses no
number, scores nothing, ranks nothing, weighs nothing and chooses no winner; a
recorded value is never a ClaimItem, a Constraint, an input of the FDC-001
``DecisionRecord``, a ledger disposition or evidence.

Ownership (Option B): this module owns the SEMANTICS — the record shapes, the
Owner-approved capacity bounds, the whole-history validation, the action
planner and the ONE presentation projection (with the 200-cell display
budget). The record store owns PERSISTENCE: two additive, append-only,
project-scoped tables (``decision_criterion_revisions`` and
``decision_cell_value_events``), written only inside its serialized write
transaction after re-planning every action against durable truth. The
decision ledger stays the sole owner of decisions and alternatives:
``engine.decision_composition`` keeps its pure "persist nothing" boundary and
``engine.decision_workspace`` is untouched.

Identity and binding:

  * a decision is its founding context root (``rec_N``); its QUESTION
    revision is the context chain's active head record;
  * an alternative is its founding root; its DECLARATION revision is the
    active declared head (a refinement makes a new head; a withdrawal leaves
    none, so the alternative has no row; a re-declaration is a new root and
    inherits nothing);
  * a criterion is a stable system id with an append-only revision history
    (DECLARED, CORRECTED, RECONFIRMED, WITHDRAWN — terminal); every revision
    binds the question revision current when it was written;
  * a cell is (criterion, alternative root); its append-only events (SET,
    CORRECTED, RECONFIRMED, CLEARED) each bind the EXACT criterion revision,
    alternative declaration revision and question revision current when the
    event was written.

A changed question, criterion revision or alternative head makes a recorded
value NEEDS CONFIRMATION: it is shown, labelled, and never silently rebound —
only an explicit RECONFIRM (or a new value) binds it to the current versions.
No equivalence between versions is ever inferred.
"""

import dataclasses
import re
import uuid

from engine.decision_composition import _chain_index, _root_num
from engine.idea_state import (
    DISPOSITION_DECISION_ALTERNATIVE_DECLARED,
    DISPOSITION_DECISION_ALTERNATIVE_WITHDRAWN,
    DISPOSITION_DECISION_CONTEXT_DECLARED,
    OWNER_STATED,
    UNVALIDATED,
)

# --- Owner-approved capacity (CAPACITY GATE CLOSED, 2026-10-12) --------------
MAX_ACTIVE_CRITERIA_PER_DECISION = 10
MAX_CRITERIA_PER_DECISION = 30            # lifetime criterion identities
MAX_CRITERIA_PER_PROJECT = 150            # lifetime criterion identities
MAX_CRITERION_LABEL_LENGTH = 200
MAX_REVISIONS_PER_CRITERION = 10          # ordinary: CORRECTED + RECONFIRMED
MAX_CRITERION_REVISIONS_PER_PROJECT = 1000
MAX_VALUE_TEXT_LENGTH = 1000
MAX_EVENTS_PER_CELL = 10                  # ordinary, the first SET included
MAX_VALUE_EVENTS_PER_DECISION = 500
MAX_VALUE_EVENTS_PER_PROJECT = 3000
MAX_CELLS_PER_PROJECT = 1500              # distinct cells ever written
# One DECLARED + the ordinary revisions + the ONE reserved WITHDRAWN.
MAX_CRITERION_REVISION_NO = 1 + MAX_REVISIONS_PER_CRITERION + 1
# The ordinary events + the ONE reserved CLEARED.
MAX_CELL_EVENT_NO = MAX_EVENTS_PER_CELL + 1
# Worst case per project, in logical records (= physical rows): 150 DECLARED
# + 1,000 ordinary criterion revisions + 150 WITHDRAWN + 3,000 ordinary value
# events + 1,500 reserved CLEARED.
MAX_LOGICAL_RECORDS_PER_PROJECT = (
    MAX_CRITERIA_PER_PROJECT + MAX_CRITERION_REVISIONS_PER_PROJECT
    + MAX_CRITERIA_PER_PROJECT + MAX_VALUE_EVENTS_PER_PROJECT
    + MAX_CELLS_PER_PROJECT)

# Display budget: comparison data cells (criterion x active alternative
# intersections, blank / cleared / needs-confirmation cells included) shown in
# ONE response, across every table of that response.
DISPLAY_CELL_BUDGET = 200

CRITERION_DECLARED = "DECLARED"
CRITERION_CORRECTED = "CORRECTED"
CRITERION_RECONFIRMED = "RECONFIRMED"
CRITERION_WITHDRAWN = "WITHDRAWN"
CRITERION_KINDS = (CRITERION_DECLARED, CRITERION_CORRECTED,
                   CRITERION_RECONFIRMED, CRITERION_WITHDRAWN)

VALUE_SET = "SET"
VALUE_CORRECTED = "CORRECTED"
VALUE_RECONFIRMED = "RECONFIRMED"
VALUE_CLEARED = "CLEARED"
VALUE_KINDS = (VALUE_SET, VALUE_CORRECTED, VALUE_RECONFIRMED, VALUE_CLEARED)

# Inventor actions (what a form asks for; the event kind is decided by the
# planner against durable truth).
ACTION_DECLARE = "declare"
ACTION_CORRECT = "correct"
ACTION_RECONFIRM = "reconfirm"
ACTION_WITHDRAW = "withdraw"
ACTION_SAVE = "save"
ACTION_CLEAR = "clear"
CRITERION_ACTIONS = (ACTION_DECLARE, ACTION_CORRECT, ACTION_RECONFIRM,
                     ACTION_WITHDRAW)
VALUE_ACTIONS = (ACTION_SAVE, ACTION_RECONFIRM, ACTION_CLEAR)

# Presentation states.
STATE_CURRENT = "current"
STATE_NEEDS_CONFIRMATION = "needs_confirmation"
STATE_NOT_RECORDED = "not_recorded"
STATE_CLEARED = "cleared"
STATE_RECORDED = "recorded"
STATUS_AVAILABLE = "available"
STATUS_UNAVAILABLE = "unavailable"
STATUS_OMITTED_SIZE = "omitted_size"

# Why a recorded value needs confirmation (presentation only).
STALE_QUESTION = "question"
STALE_CRITERION = "criterion"
STALE_ALTERNATIVE = "alternative"

_ID_RE = {
    "crt": re.compile(r"^crt-[0-9a-f]{32}$"),
    "ccr": re.compile(r"^ccr-[0-9a-f]{32}$"),
    "cve": re.compile(r"^cve-[0-9a-f]{32}$"),
}
_RECORD_ID_RE = re.compile(r"^rec_(0|[1-9][0-9]{0,8})$")

NO_CHANGE = "NO_CHANGE"


# --- errors -----------------------------------------------------------------
class ComparisonError(ValueError):
    """Base: the comparison history or an action is not valid."""


class ComparisonCorrupt(ComparisonError):
    """The durable comparison history is malformed, gapped, forked, foreign
    or inconsistent with the ledger. Fail closed for the WHOLE comparison."""


class ComparisonRejected(ComparisonError):
    """An action names no current target of this decision, or carries text
    that cannot be recorded. ``reason`` selects the inventor-facing wording."""

    def __init__(self, reason, message="the action is not valid"):
        super().__init__(message)
        self.reason = reason


class ComparisonStale(ComparisonError):
    """The action was prepared against versions that are no longer current.
    Nothing is written."""


class ComparisonLimitReached(ComparisonError):
    """An Owner-approved capacity bound blocks this ordinary operation.
    ``limit`` names the bound; ``can_still_clear`` says whether the reserved
    CLEAR of this cell is still available (so the wording never promises an
    action another bound forbids)."""

    def __init__(self, limit, can_still_clear=False,
                 message="a comparison capacity bound is reached"):
        super().__init__(message)
        self.limit = limit
        self.can_still_clear = can_still_clear


# Rejection reasons.
REJECT_TARGET = "target"
REJECT_TEXT_EMPTY = "text_empty"
REJECT_TEXT_TOO_LONG = "text_too_long"
REJECT_TEXT_CHAR = "text_char"
REJECT_CRITERION_WITHDRAWN = "criterion_withdrawn"
REJECT_ALTERNATIVE_WITHDRAWN = "alternative_withdrawn"
REJECT_CELL_CLOSED = "cell_closed"
REJECT_CONFIRM_CRITERION_FIRST = "confirm_criterion_first"
REJECT_NOTHING_TO_RECONFIRM = "nothing_to_reconfirm"

# Limit names.
LIMIT_ACTIVE_CRITERIA = "active_criteria"
LIMIT_DECISION_CRITERIA = "decision_criteria"
LIMIT_PROJECT_CRITERIA = "project_criteria"
LIMIT_CRITERION_REVISIONS = "criterion_revisions"
LIMIT_PROJECT_CRITERION_REVISIONS = "project_criterion_revisions"
LIMIT_CELL_EVENTS = "cell_events"
LIMIT_DECISION_VALUE_EVENTS = "decision_value_events"
LIMIT_PROJECT_VALUE_EVENTS = "project_value_events"
LIMIT_PROJECT_CELLS = "project_cells"


# --- record shapes ----------------------------------------------------------
@dataclasses.dataclass(frozen=True)
class CriterionRevision:
    """ONE immutable revision of ONE criterion. ``label`` is the inventor's
    wording (``None`` only on WITHDRAWN; a RECONFIRMED revision restates the
    current label verbatim). ``question_record_id`` is the decision question
    revision this revision is bound to."""
    revision_id: str
    criterion_id: str
    context_root: str
    revision_no: int
    kind: str
    label: object
    question_record_id: str
    provenance: str = OWNER_STATED
    validation_state: str = UNVALIDATED


@dataclasses.dataclass(frozen=True)
class ValueEvent:
    """ONE immutable event of ONE cell (criterion x alternative root).
    ``value_text`` is the inventor's wording (``None`` only on CLEARED; a
    RECONFIRMED event restates the current text verbatim). ``reserved`` is
    True only on the ONE terminal reserved CLEARED of a cell. The three
    bindings name the exact versions current when the event was written."""
    event_id: str
    context_root: str
    criterion_id: str
    alternative_root: str
    event_no: int
    kind: str
    reserved: bool
    value_text: object
    criterion_revision_id: str
    alternative_record_id: str
    question_record_id: str
    provenance: str = OWNER_STATED
    validation_state: str = UNVALIDATED


def new_criterion_id():
    return "crt-" + uuid.uuid4().hex


def new_criterion_revision_id():
    return "ccr-" + uuid.uuid4().hex


def new_value_event_id():
    return "cve-" + uuid.uuid4().hex


def is_valid_criterion_id(value):
    return isinstance(value, str) and bool(_ID_RE["crt"].match(value))


def is_valid_criterion_revision_id(value):
    return isinstance(value, str) and bool(_ID_RE["ccr"].match(value))


def is_valid_value_event_id(value):
    return isinstance(value, str) and bool(_ID_RE["cve"].match(value))


def is_valid_record_id(value):
    """The canonical ledger record id shape (``rec_N``)."""
    return isinstance(value, str) and bool(_RECORD_ID_RE.match(value))


def clean_text(raw, limit):
    """``(text, reason)``: the submitted text stored trimmed and otherwise
    verbatim, or a rejection reason — empty, a NUL (never stripped) or over
    ``limit`` (never truncated)."""
    if not isinstance(raw, str) or not raw.strip():
        return None, REJECT_TEXT_EMPTY
    text = raw.strip()
    if "\x00" in text:
        return None, REJECT_TEXT_CHAR
    if len(text) > limit:
        return None, REJECT_TEXT_TOO_LONG
    return text, None


def _valid_stored_text(value, limit):
    return (isinstance(value, str) and 0 < len(value) <= limit
            and value == value.strip() and "\x00" not in value)


# --- the decision frame: read ONLY from the ledger ---------------------------
@dataclasses.dataclass(frozen=True)
class AlternativeFrame:
    root: str
    name: str                 # the latest declared wording, verbatim
    head_record_id: object    # active declared head; None when withdrawn
    record_ids: frozenset     # every declared record of the chain


@dataclasses.dataclass(frozen=True)
class DecisionFrame:
    context_root: str
    question: str
    question_record_id: str   # the context chain's active head
    context_record_ids: frozenset
    alternatives: tuple       # AlternativeFrame, ascending root

    @property
    def active_alternatives(self):
        return tuple(a for a in self.alternatives if a.head_record_id)

    def alternative(self, root):
        for alt in self.alternatives:
            if alt.root == root:
                return alt
        return None


def decision_frames(assertions):
    """``{context_root: DecisionFrame}`` in ascending numeric root order, from
    the ledger alone (the same chain index as ``decision_composition``).
    Raises ``ComparisonCorrupt`` when a decision chain cannot be described."""
    assertions = list(assertions or ())
    try:
        by_id, root_of = _chain_index(assertions)
        contexts, alternatives = {}, {}
        for record in assertions:
            if record.disposition == DISPOSITION_DECISION_CONTEXT_DECLARED:
                root = root_of(record)
                ctx = contexts.setdefault(root, {"ids": set(), "head": None})
                ctx["ids"].add(record.record_id)
                if getattr(record, "superseded_by", None) is None:
                    if ctx["head"] is not None:
                        raise ComparisonCorrupt("a decision has two heads")
                    ctx["head"] = record
            elif record.disposition in (
                    DISPOSITION_DECISION_ALTERNATIVE_DECLARED,
                    DISPOSITION_DECISION_ALTERNATIVE_WITHDRAWN):
                root = root_of(record)
                alt = alternatives.setdefault(root, {
                    "context": record.decision_context_root, "ids": set(),
                    "declared": [], "head": None, "withdrawn": False})
                if record.decision_context_root != alt["context"]:
                    raise ComparisonCorrupt("an alternative crosses decisions")
                if record.disposition == DISPOSITION_DECISION_ALTERNATIVE_DECLARED:
                    alt["ids"].add(record.record_id)
                    alt["declared"].append(record)
                    if getattr(record, "superseded_by", None) is None:
                        alt["head"] = record
                elif getattr(record, "superseded_by", None) is None:
                    alt["withdrawn"] = True
        frames = {}
        for root in sorted(contexts, key=_root_num):
            ctx = contexts[root]
            if ctx["head"] is None:
                raise ComparisonCorrupt("a decision has no current question")
            alts = []
            for alt_root in sorted(
                    (r for r, a in alternatives.items() if a["context"] == root),
                    key=_root_num):
                alt = alternatives[alt_root]
                if not alt["declared"] or (alt["head"] is None) == (not alt["withdrawn"]):
                    raise ComparisonCorrupt("an alternative has no single state")
                alts.append(AlternativeFrame(
                    root=alt_root, name=alt["declared"][-1].content,
                    head_record_id=(alt["head"].record_id if alt["head"] else None),
                    record_ids=frozenset(alt["ids"])))
            frames[root] = DecisionFrame(
                context_root=root, question=ctx["head"].content,
                question_record_id=ctx["head"].record_id,
                context_record_ids=frozenset(ctx["ids"]),
                alternatives=tuple(alts))
        if any(a["context"] not in frames for a in alternatives.values()):
            raise ComparisonCorrupt("an alternative names no decision")
        return frames
    except ComparisonCorrupt:
        raise
    except Exception:
        raise ComparisonCorrupt("the decision ledger cannot be described") from None


# --- whole-history validation -------------------------------------------------
@dataclasses.dataclass(frozen=True)
class CriterionRecord:
    criterion_id: str
    context_root: str
    revisions: tuple          # CriterionRevision, revision_no 1..k

    @property
    def head(self):
        return self.revisions[-1]

    @property
    def withdrawn(self):
        return self.head.kind == CRITERION_WITHDRAWN

    @property
    def label(self):
        """The current (or, when withdrawn, the last) label."""
        for rev in reversed(self.revisions):
            if rev.label is not None:
                return rev.label
        return None

    @property
    def ordinary(self):
        return sum(1 for r in self.revisions
                   if r.kind in (CRITERION_CORRECTED, CRITERION_RECONFIRMED))

    @property
    def labels(self):
        """Every distinct wording in order (DECLARED and CORRECTED)."""
        return tuple(r.label for r in self.revisions
                     if r.kind in (CRITERION_DECLARED, CRITERION_CORRECTED))


@dataclasses.dataclass(frozen=True)
class CellRecord:
    context_root: str
    criterion_id: str
    alternative_root: str
    events: tuple             # ValueEvent, event_no 1..k

    @property
    def head(self):
        return self.events[-1]

    @property
    def text(self):
        """The value text currently held (current or stale), or None."""
        return None if self.head.kind == VALUE_CLEARED else self.head.value_text

    @property
    def closed(self):
        return self.head.kind == VALUE_CLEARED and self.head.reserved

    @property
    def ordinary(self):
        return sum(1 for e in self.events if not e.reserved)


@dataclasses.dataclass(frozen=True)
class ComparisonLedger:
    """The validated comparison history of ONE project over ONE ledger."""
    frames: dict              # context_root -> DecisionFrame
    criteria: dict            # criterion_id -> CriterionRecord
    criterion_order: tuple    # criterion ids in declaration order
    cells: dict               # (criterion_id, alternative_root) -> CellRecord
    # Ordinary-event counts, computed once by ``comparison_ledger``.
    decision_value_counts: dict = dataclasses.field(default_factory=dict)
    project_value_count: int = 0
    criterion_revision_count: int = 0

    def criteria_of(self, context_root):
        return tuple(self.criteria[cid] for cid in self.criterion_order
                     if self.criteria[cid].context_root == context_root)

    def active_criteria_of(self, context_root):
        return tuple(c for c in self.criteria_of(context_root) if not c.withdrawn)

    @property
    def project_ordinary_criterion_revisions(self):
        return self.criterion_revision_count

    def decision_ordinary_value_events(self, context_root):
        return self.decision_value_counts.get(context_root, 0)

    @property
    def project_ordinary_value_events(self):
        return self.project_value_count

    def criterion_state(self, record):
        frame = self.frames[record.context_root]
        return (STATE_CURRENT
                if record.head.question_record_id == frame.question_record_id
                else STATE_NEEDS_CONFIRMATION)

    def cell_staleness(self, cell):
        """The tuple of what changed since the binding event (empty when the
        held value is current). Only meaningful when the cell holds text."""
        frame = self.frames[cell.context_root]
        alt = frame.alternative(cell.alternative_root)
        crit = self.criteria[cell.criterion_id]
        head = cell.head
        stale = []
        if head.question_record_id != frame.question_record_id:
            stale.append(STALE_QUESTION)
        if head.criterion_revision_id != crit.head.revision_id:
            stale.append(STALE_CRITERION)
        if alt is None or head.alternative_record_id != alt.head_record_id:
            stale.append(STALE_ALTERNATIVE)
        return tuple(stale)


def _require(condition, message):
    if not condition:
        raise ComparisonCorrupt(message)


def comparison_ledger(frames, criterion_revisions, value_events):
    """Validate the WHOLE durable comparison history of one project against
    its decision ``frames`` and return the ``ComparisonLedger``. Any defect —
    a gap, fork, foreign reference, wrong kind order, event after a terminal
    one, malformed text or binding, or a capacity bound exceeded — raises
    ``ComparisonCorrupt``: nothing partial, nothing repaired."""
    criteria, order = {}, []
    by_criterion = {}
    revision_ids = set()
    for rev in criterion_revisions:
        _require(isinstance(rev, CriterionRevision), "not a criterion revision")
        _require(is_valid_criterion_id(rev.criterion_id), "malformed criterion id")
        _require(is_valid_criterion_revision_id(rev.revision_id),
                 "malformed criterion revision id")
        _require(rev.revision_id not in revision_ids, "duplicate revision id")
        revision_ids.add(rev.revision_id)
        by_criterion.setdefault(rev.criterion_id, []).append(rev)
        if rev.criterion_id not in order:
            order.append(rev.criterion_id)
    for cid in order:
        # Rows arrive in durable append order: a criterion's revisions must
        # appear there exactly as 1..k (no gap, fork or reordering).
        revs = by_criterion[cid]
        _require([r.revision_no for r in revs] == list(range(1, len(revs) + 1)),
                 "criterion revisions are not contiguous")
        first = revs[0]
        _require(first.kind == CRITERION_DECLARED, "a criterion is not declared first")
        _require(len(revs) <= MAX_CRITERION_REVISION_NO, "too many revisions")
        frame = frames.get(first.context_root)
        _require(frame is not None, "a criterion names no decision")
        label = None
        for index, rev in enumerate(revs):
            _require(rev.context_root == first.context_root,
                     "a criterion crosses decisions")
            _require(rev.provenance == OWNER_STATED
                     and rev.validation_state == UNVALIDATED,
                     "criterion provenance is not owner-stated / unvalidated")
            _require(rev.question_record_id in frame.context_record_ids,
                     "a criterion binds a foreign question")
            _require(rev.kind in CRITERION_KINDS, "unknown criterion kind")
            _require(index == 0 or rev.kind != CRITERION_DECLARED,
                     "a criterion is declared twice")
            _require(index == 0 or revs[index - 1].kind != CRITERION_WITHDRAWN,
                     "a revision follows a withdrawal")
            if rev.kind in (CRITERION_DECLARED, CRITERION_CORRECTED):
                _require(_valid_stored_text(rev.label, MAX_CRITERION_LABEL_LENGTH),
                         "malformed criterion label")
                label = rev.label
            elif rev.kind == CRITERION_RECONFIRMED:
                _require(rev.label == label, "a reconfirmation changes the label")
            else:
                _require(rev.label is None, "a withdrawal carries a label")
        record = CriterionRecord(criterion_id=cid, context_root=first.context_root,
                                 revisions=tuple(revs))
        _require(record.ordinary <= MAX_REVISIONS_PER_CRITERION,
                 "criterion revision bound exceeded")
        criteria[cid] = record
    _require(len(criteria) <= MAX_CRITERIA_PER_PROJECT, "project criterion bound exceeded")
    _require(sum(c.ordinary for c in criteria.values())
             <= MAX_CRITERION_REVISIONS_PER_PROJECT,
             "project criterion revision bound exceeded")
    for root in frames:
        mine = [c for c in criteria.values() if c.context_root == root]
        _require(len(mine) <= MAX_CRITERIA_PER_DECISION, "decision criterion bound exceeded")
        _require(sum(1 for c in mine if not c.withdrawn)
                 <= MAX_ACTIVE_CRITERIA_PER_DECISION, "active criterion bound exceeded")

    by_cell, event_ids = {}, set()
    for event in value_events:
        _require(isinstance(event, ValueEvent), "not a value event")
        _require(is_valid_value_event_id(event.event_id), "malformed value event id")
        _require(event.event_id not in event_ids, "duplicate value event id")
        event_ids.add(event.event_id)
        by_cell.setdefault((event.criterion_id, event.alternative_root), []).append(event)
    cells = {}
    for key, events in by_cell.items():
        _require([e.event_no for e in events] == list(range(1, len(events) + 1)),
                 "cell events are not contiguous")
        _require(len(events) <= MAX_CELL_EVENT_NO, "too many cell events")
        crit = criteria.get(key[0])
        _require(crit is not None, "a value names no criterion")
        frame = frames[crit.context_root]
        alt = frame.alternative(key[1])
        _require(alt is not None, "a value names no alternative of its decision")
        crit_revisions = {r.revision_id: r for r in crit.revisions}
        text = None
        held = False                  # the cell holds value text
        for index, event in enumerate(events):
            _require(event.context_root == crit.context_root,
                     "a value crosses decisions")
            _require(event.provenance == OWNER_STATED
                     and event.validation_state == UNVALIDATED,
                     "value provenance is not owner-stated / unvalidated")
            _require(event.kind in VALUE_KINDS, "unknown value kind")
            _require(isinstance(event.reserved, bool), "malformed reserved flag")
            _require(index == 0 or not events[index - 1].reserved,
                     "an event follows the reserved clear")
            bound = crit_revisions.get(event.criterion_revision_id)
            _require(bound is not None and bound.kind != CRITERION_WITHDRAWN,
                     "a value binds a foreign criterion revision")
            _require(event.alternative_record_id in alt.record_ids,
                     "a value binds a foreign alternative revision")
            _require(event.question_record_id in frame.context_record_ids,
                     "a value binds a foreign question")
            if event.kind == VALUE_SET:
                _require(not held, "a value is set over a held value")
                _require(not event.reserved, "a set is reserved")
                _require(_valid_stored_text(event.value_text, MAX_VALUE_TEXT_LENGTH),
                         "malformed value text")
                text, held = event.value_text, True
            elif event.kind == VALUE_CORRECTED:
                _require(held and not event.reserved, "a correction without a value")
                _require(_valid_stored_text(event.value_text, MAX_VALUE_TEXT_LENGTH)
                         and event.value_text != text, "malformed value correction")
                text = event.value_text
            elif event.kind == VALUE_RECONFIRMED:
                _require(held and not event.reserved, "a reconfirmation without a value")
                _require(event.value_text == text, "a reconfirmation changes the value")
            else:
                _require(held, "a clear without a value")
                _require(event.value_text is None, "a clear carries text")
                text, held = None, False
        cell = CellRecord(context_root=crit.context_root, criterion_id=key[0],
                          alternative_root=key[1], events=tuple(events))
        _require(cell.ordinary <= MAX_EVENTS_PER_CELL, "cell event bound exceeded")
        cells[key] = cell
    _require(len(cells) <= MAX_CELLS_PER_PROJECT, "project cell bound exceeded")
    decision_counts = {}
    for cell in cells.values():
        decision_counts[cell.context_root] = (
            decision_counts.get(cell.context_root, 0) + cell.ordinary)
    project_count = sum(decision_counts.values())
    _require(project_count <= MAX_VALUE_EVENTS_PER_PROJECT,
             "project value event bound exceeded")
    _require(all(n <= MAX_VALUE_EVENTS_PER_DECISION for n in decision_counts.values()),
             "decision value event bound exceeded")
    return ComparisonLedger(
        frames=frames, criteria=criteria, criterion_order=tuple(order),
        cells=cells, decision_value_counts=decision_counts,
        project_value_count=project_count,
        criterion_revision_count=sum(c.ordinary for c in criteria.values()))


def build_comparison(assertions, criterion_revisions, value_events):
    """The validated ``ComparisonLedger`` of one project from its durable
    ledger records and its two comparison record families."""
    return comparison_ledger(decision_frames(assertions),
                             tuple(criterion_revisions), tuple(value_events))


# --- the action planner (pure; the store re-runs it inside its transaction) --
def _frame_for(ledger, context_root):
    frame = ledger.frames.get(context_root)
    if frame is None:
        raise ComparisonRejected(REJECT_TARGET, "no such decision")
    return frame


def _criterion_for(ledger, context_root, criterion_id):
    record = ledger.criteria.get(criterion_id)
    if record is None or record.context_root != context_root:
        raise ComparisonRejected(REJECT_TARGET, "no such criterion")
    return record


def plan_criterion_action(ledger, action, context_root, expected_question,
                          criterion_id=None, expected_revision_no=None, label=None):
    """The ONE criterion revision an inventor action produces against
    ``ledger`` (the durable truth), or ``NO_CHANGE`` for a genuine no-op.

    * declare: a new criterion (fresh identity) — the project and decision
      lifetime bounds and the active bound are checked, in that order;
    * correct: CORRECTED with the new label; the unchanged label bound to the
      current question is a no-op, and the unchanged label bound to an older
      question is a RECONFIRMED revision;
    * reconfirm: RECONFIRMED when the criterion needs confirmation, a no-op
      when it is already current;
    * withdraw: the ONE reserved terminal WITHDRAWN (no ordinary quota).

    Every action is refused as stale (``ComparisonStale``) unless the
    question revision — and for a revision the criterion revision — it was
    prepared against is still current."""
    if action not in CRITERION_ACTIONS:
        raise ComparisonRejected(REJECT_TARGET, "unknown action")
    frame = _frame_for(ledger, context_root)
    if expected_question != frame.question_record_id:
        raise ComparisonStale("the decision question changed")
    if action in (ACTION_DECLARE, ACTION_CORRECT):
        text, reason = clean_text(label, MAX_CRITERION_LABEL_LENGTH)
        if reason:
            raise ComparisonRejected(reason, "the label cannot be recorded")
    if action == ACTION_DECLARE:
        if len(ledger.criteria) >= MAX_CRITERIA_PER_PROJECT:
            raise ComparisonLimitReached(LIMIT_PROJECT_CRITERIA)
        if len(ledger.criteria_of(context_root)) >= MAX_CRITERIA_PER_DECISION:
            raise ComparisonLimitReached(LIMIT_DECISION_CRITERIA)
        if len(ledger.active_criteria_of(context_root)) >= MAX_ACTIVE_CRITERIA_PER_DECISION:
            raise ComparisonLimitReached(LIMIT_ACTIVE_CRITERIA)
        return CriterionRevision(
            revision_id=new_criterion_revision_id(), criterion_id=new_criterion_id(),
            context_root=context_root, revision_no=1, kind=CRITERION_DECLARED,
            label=text, question_record_id=frame.question_record_id)
    record = _criterion_for(ledger, context_root, criterion_id)
    if record.withdrawn:
        raise ComparisonRejected(REJECT_CRITERION_WITHDRAWN, "the criterion is withdrawn")
    if expected_revision_no != record.head.revision_no:
        raise ComparisonStale("the criterion changed")
    current = ledger.criterion_state(record) == STATE_CURRENT
    if action == ACTION_WITHDRAW:
        kind, new_label = CRITERION_WITHDRAWN, None
    elif action == ACTION_RECONFIRM or text == record.label:
        if current:
            return NO_CHANGE
        kind, new_label = CRITERION_RECONFIRMED, record.label
    else:
        kind, new_label = CRITERION_CORRECTED, text
    if kind != CRITERION_WITHDRAWN:
        if record.ordinary >= MAX_REVISIONS_PER_CRITERION:
            raise ComparisonLimitReached(LIMIT_CRITERION_REVISIONS)
        if ledger.project_ordinary_criterion_revisions >= MAX_CRITERION_REVISIONS_PER_PROJECT:
            raise ComparisonLimitReached(LIMIT_PROJECT_CRITERION_REVISIONS)
    return CriterionRevision(
        revision_id=new_criterion_revision_id(), criterion_id=record.criterion_id,
        context_root=context_root, revision_no=record.head.revision_no + 1,
        kind=kind, label=new_label, question_record_id=frame.question_record_id)


def _ordinary_room(ledger, context_root, cell):
    """The first ordinary value bound that blocks one more ordinary event of
    this cell (``None`` when every bound permits it)."""
    if cell is not None and cell.ordinary >= MAX_EVENTS_PER_CELL:
        return LIMIT_CELL_EVENTS
    if ledger.decision_ordinary_value_events(context_root) >= MAX_VALUE_EVENTS_PER_DECISION:
        return LIMIT_DECISION_VALUE_EVENTS
    if ledger.project_ordinary_value_events >= MAX_VALUE_EVENTS_PER_PROJECT:
        return LIMIT_PROJECT_VALUE_EVENTS
    if cell is None and len(ledger.cells) >= MAX_CELLS_PER_PROJECT:
        return LIMIT_PROJECT_CELLS
    return None


def plan_value_action(ledger, action, context_root, criterion_id,
                      alternative_root, expected_event_no, expected_criterion_revision,
                      expected_alternative_record, expected_question, text=None):
    """The ONE value event an inventor action produces against ``ledger`` (the
    durable truth), or ``NO_CHANGE`` for a genuine no-op.

    * save: SET when the cell holds no value (a never-written cell also takes
      one lifetime cell identity), CORRECTED for different text, RECONFIRMED
      for the same text bound to older versions, a no-op for the same text
      already bound to the current versions;
    * reconfirm: RECONFIRMED when the held value needs confirmation, a no-op
      when it is current;
    * clear: an ordinary CLEARED while every ordinary bound permits it,
      otherwise the ONE reserved terminal CLEARED; a no-op when the cell holds
      no value.

    Refused when the criterion or alternative is not current
    (``ComparisonRejected``), when any version the form was prepared against
    has moved (``ComparisonStale``), when a save / reconfirm meets a criterion
    that itself needs confirmation, a closed cell, or an exhausted ordinary
    bound (``ComparisonLimitReached`` — a stale value is never made current
    because of it)."""
    if action not in VALUE_ACTIONS:
        raise ComparisonRejected(REJECT_TARGET, "unknown action")
    frame = _frame_for(ledger, context_root)
    record = _criterion_for(ledger, context_root, criterion_id)
    alt = frame.alternative(alternative_root)
    if alt is None:
        raise ComparisonRejected(REJECT_TARGET, "no such alternative")
    if record.withdrawn:
        raise ComparisonRejected(REJECT_CRITERION_WITHDRAWN, "the criterion is withdrawn")
    if alt.head_record_id is None:
        raise ComparisonRejected(REJECT_ALTERNATIVE_WITHDRAWN,
                                 "the alternative is withdrawn")
    cell = ledger.cells.get((criterion_id, alternative_root))
    head_no = cell.head.event_no if cell else 0
    if (expected_question != frame.question_record_id
            or expected_criterion_revision != record.head.revision_id
            or expected_alternative_record != alt.head_record_id
            or expected_event_no != head_no):
        raise ComparisonStale("a version changed")
    held = cell is not None and cell.text is not None
    if action == ACTION_CLEAR:
        if not held:
            return NO_CHANGE
        reserved = _ordinary_room(ledger, context_root, cell) is not None
        return _value_event(frame, record, alt, cell, VALUE_CLEARED, None, reserved)
    if cell is not None and cell.closed:
        raise ComparisonRejected(REJECT_CELL_CLOSED, "the cell accepts no further events")
    current_binding = held and not ledger.cell_staleness(cell)
    if action == ACTION_SAVE:
        value, reason = clean_text(text, MAX_VALUE_TEXT_LENGTH)
        if reason:
            raise ComparisonRejected(reason, "the value cannot be recorded")
        if not held:
            kind = VALUE_SET
        elif value == cell.text:
            if current_binding:
                return NO_CHANGE
            kind = VALUE_RECONFIRMED
        else:
            kind = VALUE_CORRECTED
    else:
        if not held:
            raise ComparisonRejected(REJECT_NOTHING_TO_RECONFIRM,
                                     "the cell holds no value")
        if current_binding:
            return NO_CHANGE
        kind, value = VALUE_RECONFIRMED, cell.text
    if ledger.criterion_state(record) != STATE_CURRENT:
        raise ComparisonRejected(REJECT_CONFIRM_CRITERION_FIRST,
                                 "the criterion needs confirmation first")
    blocked = _ordinary_room(ledger, context_root, cell)
    if blocked:
        raise ComparisonLimitReached(blocked, can_still_clear=held)
    return _value_event(frame, record, alt, cell, kind, value, False)


def _value_event(frame, record, alt, cell, kind, value, reserved):
    return ValueEvent(
        event_id=new_value_event_id(), context_root=frame.context_root,
        criterion_id=record.criterion_id, alternative_root=alt.root,
        event_no=(cell.head.event_no if cell else 0) + 1, kind=kind,
        reserved=reserved, value_text=value,
        criterion_revision_id=record.head.revision_id,
        alternative_record_id=alt.head_record_id,
        question_record_id=frame.question_record_id)


def same_criterion_submission(stored, action, context_root, criterion_id,
                              expected_revision_no, label):
    """True iff a STORED criterion revision is exactly what this action
    submission produced (the exact-retry test; material, not wording)."""
    if stored.context_root != context_root:
        return False
    if action == ACTION_DECLARE:
        return stored.kind == CRITERION_DECLARED and stored.label == (
            clean_text(label, MAX_CRITERION_LABEL_LENGTH)[0])
    if stored.criterion_id != criterion_id \
            or stored.revision_no != (expected_revision_no or 0) + 1:
        return False
    if action == ACTION_WITHDRAW:
        return stored.kind == CRITERION_WITHDRAWN
    if action == ACTION_RECONFIRM:
        return stored.kind == CRITERION_RECONFIRMED
    return (stored.kind in (CRITERION_CORRECTED, CRITERION_RECONFIRMED)
            and stored.label == clean_text(label, MAX_CRITERION_LABEL_LENGTH)[0])


def same_value_submission(stored, action, context_root, criterion_id,
                          alternative_root, expected_event_no, text):
    """True iff a STORED value event is exactly what this action submission
    produced (the exact-retry test)."""
    if (stored.context_root != context_root or stored.criterion_id != criterion_id
            or stored.alternative_root != alternative_root
            or stored.event_no != (expected_event_no or 0) + 1):
        return False
    if action == ACTION_CLEAR:
        return stored.kind == VALUE_CLEARED
    if action == ACTION_RECONFIRM:
        return stored.kind == VALUE_RECONFIRMED
    return (stored.kind in (VALUE_SET, VALUE_CORRECTED, VALUE_RECONFIRMED)
            and stored.value_text == clean_text(text, MAX_VALUE_TEXT_LENGTH)[0])


# --- the ONE presentation projection ------------------------------------------
def display_size(ledger):
    """``(total, per_decision)``: the comparison data cells of every current
    table, computed from counts BEFORE any grid is expanded."""
    per_decision = []
    for root, frame in ledger.frames.items():
        per_decision.append(
            (root, len(ledger.active_criteria_of(root)) * len(frame.active_alternatives)))
    return sum(n for _r, n in per_decision), per_decision


def _criterion_view(ledger, record, writable):
    state = ledger.criterion_state(record)
    room = (record.ordinary < MAX_REVISIONS_PER_CRITERION
            and ledger.project_ordinary_criterion_revisions
            < MAX_CRITERION_REVISIONS_PER_PROJECT)
    limit = None
    if record.ordinary >= MAX_REVISIONS_PER_CRITERION:
        limit = LIMIT_CRITERION_REVISIONS
    elif not room:
        limit = LIMIT_PROJECT_CRITERION_REVISIONS
    return {
        "criterion_id": record.criterion_id,
        "label": record.label,
        "state": state,
        "revision_no": record.head.revision_no,
        "revision_id": record.head.revision_id,
        "earlier": list(record.labels[:-1]) if record.labels else [],
        "can_revise": bool(writable and room),
        "revise_limit": limit,
    }


def _cell_view(ledger, frame, record, alt, writable):
    cell = ledger.cells.get((record.criterion_id, alt.root))
    view = {
        "alternative_root": alt.root, "alternative_name": alt.name,
        "alternative_record": alt.head_record_id,
        "event_no": cell.head.event_no if cell else 0,
        "text": None, "state": STATE_NOT_RECORDED, "stale": (),
        "closed": bool(cell and cell.closed),
        "can_save": False, "can_reconfirm": False, "can_clear": False,
        "limit": None, "criterion_current": True,
    }
    if cell is not None and cell.text is not None:
        view["text"] = cell.text
        stale = ledger.cell_staleness(cell)
        view["stale"] = stale
        view["state"] = STATE_NEEDS_CONFIRMATION if stale else STATE_RECORDED
    elif cell is not None:
        view["state"] = STATE_CLEARED
    if writable and not view["closed"]:
        criterion_current = ledger.criterion_state(record) == STATE_CURRENT
        blocked = _ordinary_room(ledger, frame.context_root, cell)
        view["limit"] = blocked
        view["can_save"] = criterion_current and blocked is None
        view["can_reconfirm"] = (criterion_current and blocked is None
                                 and view["state"] == STATE_NEEDS_CONFIRMATION)
        view["can_clear"] = view["text"] is not None
        view["criterion_current"] = criterion_current
    return view


def comparison_view(ledger, page=1, budget=DISPLAY_CELL_BUDGET, writable=False,
                    complete_only=False):
    """The ONE presentation projection of a validated ``ComparisonLedger`` —
    shared by the Decision Room (paged) and the report / PDF (complete or
    omitted). JSON-safe; persists nothing.

    The display size is determined FIRST from counts; only the cells inside
    the requested window are expanded. Cells are ordered canonically —
    decision (ascending root), criterion (declaration order), alternative
    (ascending root) — and a window of at most ``budget`` cells is shown per
    response. With ``complete_only`` (report / PDF) every table is included
    when the total fits the budget; otherwise no grid is included and the
    status says ``omitted_size`` (never a subset presented as complete)."""
    total, per_decision = display_size(ledger)
    pages = max(1, -(-total // budget)) if budget > 0 else 1
    try:
        page = int(page)
    except (TypeError, ValueError):
        page = 1
    page = min(max(page, 1), pages)
    omitted = complete_only and total > budget
    start = 0 if complete_only else (page - 1) * budget
    stop = (total if complete_only else min(page * budget, total))
    if omitted:
        start = stop = 0
    decisions = {}
    offset = 0
    project_room = len(ledger.criteria) < MAX_CRITERIA_PER_PROJECT
    for root, size in per_decision:
        frame = ledger.frames[root]
        d_start, d_stop = offset, offset + size
        offset = d_stop
        records = ledger.criteria_of(root)
        active = [r for r in records if not r.withdrawn]
        alternatives = frame.active_alternatives
        declare_limit = None
        if not project_room:
            declare_limit = LIMIT_PROJECT_CRITERIA
        elif len(records) >= MAX_CRITERIA_PER_DECISION:
            declare_limit = LIMIT_DECISION_CRITERIA
        elif len(active) >= MAX_ACTIVE_CRITERIA_PER_DECISION:
            declare_limit = LIMIT_ACTIVE_CRITERIA
        groups = []
        lo, hi = max(start, d_start), min(stop, d_stop)
        if lo < hi and alternatives:
            width = len(alternatives)
            for c_index, record in enumerate(active):
                g_start = d_start + c_index * width
                g_lo, g_hi = max(lo, g_start), min(hi, g_start + width)
                if g_lo >= g_hi:
                    continue
                groups.append({
                    "criterion_id": record.criterion_id,
                    "label": record.label,
                    "criterion_state": ledger.criterion_state(record),
                    "criterion_revision": record.head.revision_id,
                    "continued_before": g_lo > g_start,
                    "continues_after": g_hi < g_start + width,
                    "cells": [_cell_view(ledger, frame, record, alt, writable)
                              for alt in alternatives[g_lo - g_start:g_hi - g_start]],
                })
        if size == 0:
            window = "empty"
        elif omitted:
            window = "omitted"
        elif lo >= hi:
            window = "elsewhere"
        elif lo == d_start and hi == d_stop:
            window = "all"
        else:
            window = "partial"
        decisions[root] = {
            "context_root": root,
            "question_record": frame.question_record_id,
            "criteria": [_criterion_view(ledger, r, writable) for r in active],
            "withdrawn_criteria": [{"label": r.label, "earlier": list(r.labels[:-1])}
                                   for r in records if r.withdrawn],
            "alternative_count": len(alternatives),
            "cell_count": size,
            "window": window,
            "groups": groups,
            "first_page": (d_start // budget + 1) if size and budget else None,
            "last_page": ((d_stop - 1) // budget + 1) if size and budget else None,
            "can_declare": bool(writable and declare_limit is None),
            "declare_limit": declare_limit,
        }
    return {
        "status": STATUS_OMITTED_SIZE if omitted else STATUS_AVAILABLE,
        "total_cells": total,
        "budget": budget,
        "page": 1 if complete_only else page,
        "pages": 1 if complete_only else pages,
        "first_cell": (start + 1) if stop > start else 0,
        "last_cell": stop if stop > start else 0,
        "decisions": decisions,
        "order": list(ledger.frames),
    }
