"""
engine/experiment_result.py

Stage 19 / CAP-09 — Result Event Slice 1: the semantic owner of the
inventor's own report of what actually happened when they performed ONE
canonical Section-11 experiment.

A Result is OWNER-STATED, UNVALIDATED historical reporting. It is never a
PASS / FAIL / PARTIAL / INCONCLUSIVE outcome, never a comparison with the
Success Criterion, never a confirmed or rejected hypothesis, never Evidence,
a validation award, a readiness, maturity, progression or gap input, and
nothing here reads, parses, grades or interprets the inventor's text.

APPEND-ONLY EVENT MODEL
-----------------------
* The canonical Section-11 ``experiment_id`` stays the ONLY experiment
  identity; there is no run or prototype-version entity.
* Every stored event carries a new, opaque, server-generated
  ``result_event_id`` derived from nothing the inventor typed, no position and
  no experiment identity.
* A separately reported execution (a first test, a retest, a later retest) is
  an independent ROOT event. A retest never supersedes an earlier execution
  merely because it happened later; identical text may legitimately be a
  real retest.
* A CORRECTION is a new event superseding the current HEAD of ONE existing
  execution chain of the same experiment. The chain's ROOT identifies the
  reported execution. At most one successor per event: no forks.
* A WITHDRAWAL (CAP-09 RESULT WITHDRAW-01) is a new TERMINAL event
  superseding the current HEAD of ONE execution chain: the inventor states
  that this recorded execution should no longer count as a current record.
  It carries its own owner-validated identity (``wdr-`` + 32 lowercase hex),
  one fixed internal marker as its text, no context and no reason. Nothing
  may follow it (no correction, no second withdrawal). The whole chain stays
  in the history; withdrawal is not erasure. It is recognised ONLY through
  its validated identity and structure (``event_kind``): ordinary inventor
  text equal to the marker stays ordinary text, and consumers never parse
  identities or markers themselves. A chain of a CURRENT or of a no-longer-
  current (historical) experiment may be withdrawn.
* Historical events are never rewritten or deleted.

CAPACITY
--------
At most ``MAX_RESULT_EVENTS_PER_PROJECT`` (200) ORDINARY events per project
(roots and corrections), plus ONE reserved terminal withdrawal per execution
root, so at most ``MAX_TOTAL_RESULT_EVENTS`` (400) events in all. A
withdrawal never frees ordinary capacity and no identity is ever reused.

CURRENT VERSUS FULL HISTORY
---------------------------
``result_chains`` is the FULL history (withdrawn chains included, each with
its ``withdrawal``); ``current_result_chains`` is the explicitly named
current-chain projection (withdrawn chains excluded). The execution-state
derivation at the end of this module counts CURRENT chains only, so a project
whose every execution of an experiment was withdrawn holds zero CURRENT
records — not "nothing was ever recorded".

CONTEXT AT RECORDING
--------------------
A ROOT event freezes, without interpretation, what the current canonical
experiment carried when it was recorded: the experiment's generated title
and source basis, and the inventor's Success Criterion, Measurement Method,
Test Hypothesis and Test Variable / Condition (each the value, or ``None``
for explicit absence). It is NOT proof that the test was executed with those
values. A correction corrects the observation only and carries NO context:
the frozen context of its root is never replaced.

``recorded_at`` is when InventorAI recorded the event, never the time the
test was executed.
"""
import re
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

# Explicit bound (characters), the bound the other CAP-09 inventor-authored
# fields already use. Over-limit input is rejected, never truncated.
MAX_RESULT_TEXT_LENGTH = 1000
# Bounded growth: a project cannot accumulate an unbounded result history.
# This bounds ORDINARY events (roots and corrections) only.
MAX_RESULT_EVENTS_PER_PROJECT = 200
# CAP-09 RESULT WITHDRAW-01: plus ONE reserved terminal withdrawal per root.
MAX_TOTAL_RESULT_EVENTS = 2 * MAX_RESULT_EVENTS_PER_PROJECT
_RESULT_EVENT_ID_RE = re.compile(r"\Ares-[0-9a-f]{32}\Z")
_WITHDRAWAL_EVENT_ID_RE = re.compile(r"\Awdr-[0-9a-f]{32}\Z")
# The fixed INTERNAL text of every withdrawal event (the column is NOT NULL).
# It is never shown as an observation and never identifies a withdrawal on
# its own: only the validated ``wdr-`` identity and structure do.
WITHDRAWAL_MARKER = "cap09:result-withdrawn:v1"
EVENT_ROOT = "root"
EVENT_CORRECTION = "correction"
EVENT_WITHDRAWAL = "withdrawal"
# Structural shape of a canonical experiment id (the Section-11 generator
# owns its semantics; this owner only refuses what can never be one).
_EXPERIMENT_ID_RE = re.compile(r"\Aexp_[a-z0-9]+(?:_[a-z0-9]+)+\Z")
_MAX_EXPERIMENT_ID_LENGTH = 128
# The bound of a frozen context value: the largest bound any frozen source
# field (generated plan text or an inventor planning field) can carry.
MAX_CONTEXT_TEXT_LENGTH = 4000


class ResultEventError(ValueError):
    """A proposed or durable Result event violates the bounded Result Event
    Slice 1 contract. Structural message only — never user text."""


@dataclass(frozen=True)
class ResultContext:
    """CONTEXT AT RECORDING of ONE execution (its root event): what the
    current canonical experiment carried when the result was recorded.
    ``None`` is explicit absence. Frozen verbatim; never interpreted."""
    experiment_title: str
    source_basis: Optional[str] = None
    success_criterion: Optional[str] = None
    measurement_method: Optional[str] = None
    test_hypothesis: Optional[str] = None
    test_variable: Optional[str] = None


CONTEXT_FIELDS = ("experiment_title", "source_basis", "success_criterion",
                  "measurement_method", "test_hypothesis", "test_variable")


@dataclass(frozen=True)
class ResultEvent:
    """ONE append-only Result event. A root has ``supersedes_result_event_id``
    ``None`` and a ``context``; a correction names the head it supersedes and
    has no context."""
    result_event_id: str
    experiment_id: str
    result_text: str
    supersedes_result_event_id: Optional[str]
    recorded_at: str
    context: Optional[ResultContext] = None


def new_result_event_id():
    """A system-generated, opaque, collision-safe event identity."""
    return "res-" + uuid.uuid4().hex


def new_withdrawal_event_id():
    """A system-generated, opaque identity of ONE terminal withdrawal event."""
    return "wdr-" + uuid.uuid4().hex


def is_valid_result_event_id(value):
    """The identity of an ORDINARY event (a root or a correction)."""
    return isinstance(value, str) and bool(_RESULT_EVENT_ID_RE.match(value))


def is_valid_withdrawal_event_id(value):
    """The identity of a terminal WITHDRAWAL event."""
    return isinstance(value, str) and bool(_WITHDRAWAL_EVENT_ID_RE.match(value))


def event_kind(event):
    """``EVENT_ROOT`` / ``EVENT_CORRECTION`` / ``EVENT_WITHDRAWAL`` of ONE
    structurally valid event, decided by its validated identity and structure
    only (never by its text). Raises ``ResultEventError`` for anything else."""
    _check_event(event)
    if is_valid_withdrawal_event_id(event.result_event_id):
        return EVENT_WITHDRAWAL
    return EVENT_ROOT if event.supersedes_result_event_id is None else EVENT_CORRECTION


def is_withdrawal(event):
    """True only for a structurally valid withdrawal event."""
    try:
        return event_kind(event) == EVENT_WITHDRAWAL
    except ResultEventError:
        return False


def is_valid_experiment_id(value):
    return (isinstance(value, str) and 0 < len(value) <= _MAX_EXPERIMENT_ID_LENGTH
            and bool(_EXPERIMENT_ID_RE.match(value)))


def valid_result_text(value):
    """A stored observation is exactly what the route stores: non-empty,
    already trimmed (internal line breaks kept), within the bound, no NUL."""
    return (isinstance(value, str) and value == value.strip()
            and 0 < len(value) <= MAX_RESULT_TEXT_LENGTH and "\x00" not in value)


def _valid_context_text(value, required=False):
    if value is None:
        return not required
    return (isinstance(value, str) and 0 < len(value) <= MAX_CONTEXT_TEXT_LENGTH
            and "\x00" not in value)


def valid_context(context):
    return (isinstance(context, ResultContext)
            and _valid_context_text(context.experiment_title, required=True)
            and all(_valid_context_text(getattr(context, f))
                    for f in CONTEXT_FIELDS[1:]))


def _now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def recorded_root(experiment_id, result_text, context):
    """A NEW root event (one separately reported execution) with a fresh id
    and its frozen CONTEXT AT RECORDING."""
    event = ResultEvent(new_result_event_id(), experiment_id, result_text,
                        None, _now(), context)
    _check_event(event)
    return event


def recorded_correction(experiment_id, result_text, supersedes_result_event_id):
    """A NEW correction event superseding ``supersedes_result_event_id``; it
    carries no context (the root's frozen context is never replaced)."""
    event = ResultEvent(new_result_event_id(), experiment_id, result_text,
                        supersedes_result_event_id, _now(), None)
    _check_event(event)
    return event


def recorded_withdrawal(experiment_id, supersedes_result_event_id):
    """A NEW terminal withdrawal event superseding the current head
    ``supersedes_result_event_id`` of ONE execution chain. It carries the
    fixed internal marker, no context and no reason."""
    event = ResultEvent(new_withdrawal_event_id(), experiment_id,
                        WITHDRAWAL_MARKER, supersedes_result_event_id, _now(), None)
    _check_event(event)
    return event


def same_result_material(stored, event):
    """True when two events carry the SAME submitted action and material:
    event kind (root / correction / withdrawal), experiment, superseded
    target and observation text. Identity, time and the frozen context
    (captured server-side) are not submitted material. A correction whose
    text equals the withdrawal marker is NOT the same action as a withdrawal
    of the same head."""
    try:
        if event_kind(stored) != event_kind(event):
            return False
    except ResultEventError:
        return False
    return (stored.experiment_id == event.experiment_id
            and stored.supersedes_result_event_id == event.supersedes_result_event_id
            and stored.result_text == event.result_text)


def _check_event(event):
    if not isinstance(event, ResultEvent):
        raise ResultEventError("not a result event")
    withdrawal = is_valid_withdrawal_event_id(event.result_event_id)
    if not withdrawal and not is_valid_result_event_id(event.result_event_id):
        raise ResultEventError("result event identity is malformed")
    if not is_valid_experiment_id(event.experiment_id):
        raise ResultEventError("experiment identity is malformed")
    if not valid_result_text(event.result_text):
        raise ResultEventError("result text is empty, invalid or too long")
    if not isinstance(event.recorded_at, str) or not event.recorded_at:
        raise ResultEventError("recorded time is missing")
    if withdrawal:
        # A withdrawal is exactly: a successor of one event, the fixed
        # marker, no context.
        if event.result_text != WITHDRAWAL_MARKER:
            raise ResultEventError("a withdrawal carries no fixed marker")
        if event.supersedes_result_event_id is None:
            raise ResultEventError("a withdrawal supersedes no event")
        if event.context is not None:
            raise ResultEventError("a withdrawal may not carry context")
    if event.supersedes_result_event_id is None:
        if not valid_context(event.context):
            raise ResultEventError("a root event carries no valid context")
    else:
        target = event.supersedes_result_event_id
        if not (is_valid_result_event_id(target)
                or is_valid_withdrawal_event_id(target)):
            raise ResultEventError("superseded identity is malformed")
        if event.context is not None:
            raise ResultEventError("a correction may not carry context")


def validate_result_history(events):
    """Validate one project's durable Result events in stored order and return
    them as a tuple, or raise ``ResultEventError``. Every event is valid; ids
    are distinct; a correction or withdrawal supersedes an EARLIER event of
    the SAME experiment (so no cycle is possible); no event has two
    successors; nothing supersedes a withdrawal (terminal); and the capacity
    rule holds — at most ``MAX_RESULT_EVENTS_PER_PROJECT`` ordinary events,
    at most one withdrawal per root (implied by terminality and the single
    successor, and checked explicitly) and at most ``MAX_TOTAL_RESULT_EVENTS``
    events in all."""
    items = tuple(events or ())
    if len(items) > MAX_TOTAL_RESULT_EVENTS:
        raise ResultEventError("too many result events")
    seen = {}
    kinds = {}
    succeeded = set()
    root_of = {}
    withdrawn_roots = set()
    ordinary = 0
    for event in items:
        kind = event_kind(event)
        if event.result_event_id in seen:
            raise ResultEventError("result event identity is duplicated")
        target = event.supersedes_result_event_id
        if target is None:
            root_of[event.result_event_id] = event.result_event_id
        else:
            prior = seen.get(target)
            if prior is None:
                raise ResultEventError("a correction supersedes no earlier event")
            if prior.experiment_id != event.experiment_id:
                raise ResultEventError("a correction crosses experiments")
            if kinds[target] == EVENT_WITHDRAWAL:
                raise ResultEventError("a withdrawn execution is terminal")
            if target in succeeded:
                raise ResultEventError("an event has two successors")
            succeeded.add(target)
            root_of[event.result_event_id] = root_of[target]
        if kind == EVENT_WITHDRAWAL:
            root = root_of[event.result_event_id]
            if root in withdrawn_roots:
                raise ResultEventError("an execution is withdrawn twice")
            withdrawn_roots.add(root)
        else:
            ordinary += 1
            if ordinary > MAX_RESULT_EVENTS_PER_PROJECT:
                raise ResultEventError("too many ordinary result events")
        seen[event.result_event_id] = event
        kinds[event.result_event_id] = kind
    return items


def head_ids(events):
    """The ids of every chain's current head (events with no successor)."""
    succeeded = {e.supersedes_result_event_id for e in events
                 if e.supersedes_result_event_id is not None}
    return {e.result_event_id for e in events} - succeeded


def result_chains(events, experiment_id=None):
    """The FULL history: every execution chain of an already-validated
    history, in root order, withdrawn chains included (optionally for one
    experiment): ``[{"root": ev, "head": ev, "history": [root, ..., head],
    "withdrawal": ev or None}]``. ``history`` holds the chain's ORDINARY
    events only and ``head`` is its latest observation; a withdrawn chain's
    terminal withdrawal event is ``withdrawal`` (it is then the chain's
    durable head) and is never part of ``history``, so the internal marker
    is never presented as an observation. Pure; identity only."""
    successor = {e.supersedes_result_event_id: e for e in events
                 if e.supersedes_result_event_id is not None}
    chains = []
    for event in events:
        if event.supersedes_result_event_id is not None:
            continue
        if experiment_id is not None and event.experiment_id != experiment_id:
            continue
        history = [event]
        withdrawal = None
        while history[-1].result_event_id in successor:
            nxt = successor[history[-1].result_event_id]
            if is_withdrawal(nxt):
                withdrawal = nxt
                break
            history.append(nxt)
        chains.append({"root": event, "head": history[-1], "history": history,
                       "withdrawal": withdrawal})
    return chains


def current_result_chains(events, experiment_id=None):
    """The CURRENT-chain projection: ``result_chains`` without withdrawn
    chains. A withdrawn execution stays in the full history but is never a
    current record."""
    return [c for c in result_chains(events, experiment_id)
            if c["withdrawal"] is None]


# Stage 35 E3 — the Stage-19 execution state of each CURRENT Section-11
# experiment, moved unchanged from the web layer so the disclosure export uses
# the same derivation. ``count`` is the number of CURRENT execution ROOTS
# (``current_result_chains``): a correction never adds one, an independent
# retest does, and a withdrawal removes its execution from the count
# (CAP-09 RESULT WITHDRAW-01). ``none`` therefore means zero CURRENT records.
EXECUTION_NONE = "none"
EXECUTION_RECORDED = "recorded"
EXECUTION_UNAVAILABLE = "unavailable"


def execution_states(events, experiment_ids):
    """``{experiment_id: {"state": ..., "count": ...}}`` over an already-read,
    validated Result history. Pure: it never reads a store and never swallows
    a failure (a caller decides what an unreadable history means)."""
    counts = {eid: len(current_result_chains(events, eid)) for eid in experiment_ids}
    return {eid: ({"state": EXECUTION_RECORDED, "count": n} if n
                  else {"state": EXECUTION_NONE, "count": 0})
            for eid, n in counts.items()}
