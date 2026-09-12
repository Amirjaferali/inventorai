"""
engine/question_feedback.py
T2-D — OPTIONAL contextual feedback on the question actually displayed.

What this is
------------
One append-only record of a single closed-vocabulary choice the project owner
made about ONE exact displayed question: `HELPFUL`, `UNCLEAR` or
`NOT_RELEVANT`. It is a convenience for the owner's own project and nothing
else.

What this is NOT (enforced by construction, not by convention)
--------------------------------------------------------------
* NOT an answer, evidence, replay input or transcript entry.
* NOT a quality / validation / provenance / readiness writer, a scoring
  signal, a quota event or a question selector. Nothing reads it to decide
  anything.
* NOT learning, analytics or tracking. There is no free text, no attachment
  and no behavioural inference; the vocabulary is fixed and closed, so no user
  prose is ever stored here.
* NOT the system-to-user result explanation (`web/result_feedback.py`), which
  is display-only and stays the owner of that concern.
* NOT operational logging (`web/observability.py`), whose allowlist forbids
  project content and which must never be used as this store.

Context identity
----------------
A feedback row is bound to a CONTEXT, never to question text. The context is
the canonical, language-free tuple

    (context_version, project, rvr7_identity, gap_type, iterations_open,
     iteration, ledger_revision)

`ledger_revision` is derived from the DURABLE append-only ledger's order and
covers corrections and non-answer records, so an amended history yields a
different context. It is derived, never stored as a new table and never part
of the ledger itself. Language is deliberately absent: the displayed language
must not change what the feedback is about.

Input contract
--------------
`make_question_feedback(...)` with an explicit, well-typed field set; the
choice must be in `FEEDBACK_CHOICES`. Returns an immutable
`QuestionFeedback` or raises `QuestionFeedbackError` (fail closed).

Prohibited behaviours
---------------------
No question or answer prose is retained. No in-place update of a stored row:
a changed choice appends a successor. No active flag — the head is DERIVED.
"""
import hashlib
import re
from dataclasses import dataclass
from typing import Optional, Tuple

# --- The closed choice vocabulary -------------------------------------------
# Fixed and closed: three tokens, no free text, no "other". Display copy lives
# in `web/ui_text.py`; these are canonical storage tokens and are never shown.
CHOICE_HELPFUL = "HELPFUL"
CHOICE_UNCLEAR = "UNCLEAR"
CHOICE_NOT_RELEVANT = "NOT_RELEVANT"
FEEDBACK_CHOICES = (CHOICE_HELPFUL, CHOICE_UNCLEAR, CHOICE_NOT_RELEVANT)

#: Bumped only if the context tuple's MEANING changes. Rows carrying another
#: version are historical and never match a current context.
CONTEXT_VERSION = 1

#: The durable ledger revision of a project with NO durable records. Explicit
#: rather than an empty string, so "no ledger yet" can never be confused with
#: "revision not computed".
EMPTY_LEDGER_REVISION = "EMPTY"

#: Sentinels for an eligible ask that owns the question slot without a gap
#: (the intake ask and the governed closing ask). Never a real gap name and
#: never a real counter, so they cannot collide with a gap-served context.
NO_GAP_SENTINEL = "-"
NO_ITERATIONS_SENTINEL = -1

#: Bounded per project, supersessions included. Reaching it is an established
#: refusal, never a truncation of history and never a block on the journey.
MAX_FEEDBACK_ROWS_PER_PROJECT = 1000

_IDENTITY_RE = re.compile(r"^[A-Za-z0-9_:\-\.]{1,200}$")
_REVISION_RE = re.compile(r"^[A-Za-z0-9]{1,64}$")
_GAP_RE = re.compile(r"^[A-Za-z0-9_\-]{1,80}$|^\-$")


class QuestionFeedbackError(ValueError):
    """Fail-closed validation error. Carries a field name and a reason only —
    never user content and never a stored value."""


class QuestionFeedbackHistoryError(ValueError):
    """Raised when a loaded history is structurally invalid. A POPULATED
    corrupt history fails closed; zero rows is always valid and is NOT
    corruption."""


class FeedbackCapExceeded(ValueError):
    """The per-project row cap was reached."""


# --- Durable write outcomes --------------------------------------------------
# INSERTED       : a new row was committed.
# EXACT_REPLAY   : this exact event is already durably present (same event key,
#                  same material content). No new row. NOTE: an exact replay
#                  says the EVENT happened, never that its choice is current.
# ALREADY_CURRENT: a FRESH submission whose choice already equals the current
#                  head. Not a new row, and deliberately NOT reported as an
#                  exact replay — the two mean different things.
# CONFLICT       : the same event key names DIFFERENT material content, or the
#                  expected head moved. Established refusal, nothing written.
# REJECTED       : refused by a check that ran before the INSERT.
# STORAGE_FAILURE: the write was attempted and the durable ABSENCE of the event
#                  was afterwards PROVEN.
# COMMIT_UNKNOWN : the durable outcome could not be established at all.
FEEDBACK_INSERTED = "INSERTED"
FEEDBACK_EXACT_REPLAY = "EXACT_REPLAY"
FEEDBACK_ALREADY_CURRENT = "ALREADY_CURRENT"
FEEDBACK_CONFLICT = "CONFLICT"
FEEDBACK_REJECTED = "REJECTED"
FEEDBACK_STORAGE_FAILURE = "STORAGE_FAILURE"
FEEDBACK_COMMIT_UNKNOWN = "COMMIT_UNKNOWN"
FEEDBACK_WRITE_OUTCOMES = (
    FEEDBACK_INSERTED, FEEDBACK_EXACT_REPLAY, FEEDBACK_ALREADY_CURRENT,
    FEEDBACK_CONFLICT, FEEDBACK_REJECTED, FEEDBACK_STORAGE_FAILURE,
    FEEDBACK_COMMIT_UNKNOWN,
)

#: The material content an EXACT replay must match. The event key is derived
#: from the signed submission identity (a fresh render nonce included), NOT
#: from the choice — so the choice is COMPARED here rather than being part of
#: the key, and A -> B -> A is three legitimate distinct events.
FEEDBACK_EVENT_MATERIAL_FIELDS = (
    "context_key", "choice", "supersedes_feedback_id",
)


def ledger_revision(record_ids):
    """The durable ledger revision: a bounded digest over the DURABLE
    append-only record order, covering answers, corrections and non-answer
    records alike.

    Derived on demand from the order the store already keeps. It creates no
    revision table, changes no ledger schema, and feedback is never part of
    it. An empty ledger returns the explicit ``EMPTY_LEDGER_REVISION``
    sentinel."""
    ordered = [str(rid) for rid in (record_ids or [])]
    if not ordered:
        return EMPTY_LEDGER_REVISION
    digest = hashlib.sha256("\x1f".join(ordered).encode("utf-8")).hexdigest()
    return digest[:32]


def context_key(project_id, rvr7_identity, gap_type, iterations_open,
                iteration, revision, version=CONTEXT_VERSION):
    """The stable, canonical, LANGUAGE-FREE key of one displayed-question
    context. Bounded digest so the stored column cannot carry prose."""
    parts = [str(version), str(project_id), str(rvr7_identity), str(gap_type),
             str(iterations_open), str(iteration), str(revision)]
    return hashlib.sha256("\x1f".join(parts).encode("utf-8")).hexdigest()[:32]


def validate_choice(choice):
    """The submitted choice, or raise. Closed vocabulary; no default, no
    'other', no free text."""
    if choice not in FEEDBACK_CHOICES:
        raise QuestionFeedbackError("choice: not an allowed value")
    return choice


@dataclass(frozen=True)
class QuestionFeedback:
    """One immutable, append-only feedback row. There is no active flag: the
    head is derived from the supersession chain."""
    feedback_id: str
    feedback_seq: int
    context_version: int
    context_key: str
    rvr7_identity: str
    gap_type: str
    iterations_open: int
    iteration: int
    ledger_revision: str
    choice: str
    supersedes_feedback_id: Optional[str]
    event_key: str
    recorded_at: str


def make_question_feedback(*, feedback_id, feedback_seq, context_version,
                           context_key, rvr7_identity, gap_type,
                           iterations_open, iteration, ledger_revision,
                           choice, supersedes_feedback_id=None, event_key,
                           recorded_at):
    """Build a validated ``QuestionFeedback`` or raise."""
    for name, value in (("feedback_id", feedback_id),
                        ("context_key", context_key),
                        ("event_key", event_key),
                        ("recorded_at", recorded_at)):
        if not isinstance(value, str) or not value.strip():
            raise QuestionFeedbackError("%s: must be a non-empty string" % name)
    if not isinstance(rvr7_identity, str) or not _IDENTITY_RE.match(rvr7_identity):
        raise QuestionFeedbackError("rvr7_identity: malformed")
    if not isinstance(gap_type, str) or not _GAP_RE.match(gap_type):
        raise QuestionFeedbackError("gap_type: malformed")
    if not isinstance(ledger_revision, str) or not _REVISION_RE.match(ledger_revision):
        raise QuestionFeedbackError("ledger_revision: malformed")
    if context_version != CONTEXT_VERSION:
        raise QuestionFeedbackError("context_version: unsupported")
    for name, value, low in (("feedback_seq", feedback_seq, 0),
                             ("iterations_open", iterations_open,
                              NO_ITERATIONS_SENTINEL),
                             ("iteration", iteration, 0)):
        if not isinstance(value, int) or isinstance(value, bool) or value < low:
            raise QuestionFeedbackError("%s: out of range" % name)
    if supersedes_feedback_id is not None:
        if not isinstance(supersedes_feedback_id, str) \
                or not supersedes_feedback_id.strip():
            raise QuestionFeedbackError(
                "supersedes_feedback_id: must be a non-empty string or None")
        if supersedes_feedback_id == feedback_id:
            raise QuestionFeedbackError(
                "supersedes_feedback_id: a row cannot supersede itself")
    return QuestionFeedback(
        feedback_id=feedback_id, feedback_seq=feedback_seq,
        context_version=context_version, context_key=context_key,
        rvr7_identity=rvr7_identity, gap_type=gap_type,
        iterations_open=iterations_open, iteration=iteration,
        ledger_revision=ledger_revision, choice=validate_choice(choice),
        supersedes_feedback_id=supersedes_feedback_id, event_key=event_key,
        recorded_at=recorded_at)


def canonical_feedback_dict(row):
    return {
        "feedback_id": row.feedback_id, "feedback_seq": row.feedback_seq,
        "context_version": row.context_version, "context_key": row.context_key,
        "rvr7_identity": row.rvr7_identity, "gap_type": row.gap_type,
        "iterations_open": row.iterations_open, "iteration": row.iteration,
        "ledger_revision": row.ledger_revision, "choice": row.choice,
        "supersedes_feedback_id": row.supersedes_feedback_id,
        "event_key": row.event_key, "recorded_at": row.recorded_at,
    }


def validate_feedback_history(rows):
    """Structurally validate a loaded history. ZERO ROWS IS ALWAYS VALID and is
    NOT corruption; a POPULATED corrupt history raises so the caller fails
    closed rather than rendering partial truth.

    Rejects: duplicate ids / seqs / event keys, an unknown or malformed choice,
    a predecessor that does not exist, a predecessor in a DIFFERENT context, a
    predecessor that is not EARLIER, self-reference, forks (two rows superseding
    one row), two roots in one context, and cycles."""
    rows = tuple(rows)
    if not rows:
        return rows
    seen_ids, seen_seq, seen_keys = set(), set(), set()
    roots, successors = {}, {}
    for row in rows:
        if not isinstance(row, QuestionFeedback):
            raise QuestionFeedbackHistoryError("row is not a QuestionFeedback")
        if row.choice not in FEEDBACK_CHOICES:
            raise QuestionFeedbackHistoryError("row carries an unknown choice")
        if row.feedback_id in seen_ids:
            raise QuestionFeedbackHistoryError("duplicate feedback_id")
        if row.feedback_seq in seen_seq:
            raise QuestionFeedbackHistoryError("duplicate feedback_seq")
        if row.event_key in seen_keys:
            raise QuestionFeedbackHistoryError("duplicate event_key")
        seen_ids.add(row.feedback_id)
        seen_seq.add(row.feedback_seq)
        seen_keys.add(row.event_key)
        prior = row.supersedes_feedback_id
        if prior is None:
            if row.context_key in roots:
                raise QuestionFeedbackHistoryError(
                    "more than one root for one context")
            roots[row.context_key] = row.feedback_id
        else:
            if prior in successors:
                raise QuestionFeedbackHistoryError(
                    "more than one successor for one row")
            successors[prior] = row.feedback_id
    by_id = {r.feedback_id: r for r in rows}
    for prior, child in successors.items():
        parent = by_id.get(prior)
        if parent is None:
            raise QuestionFeedbackHistoryError("successor targets an unknown row")
        kid = by_id[child]
        if parent.context_key != kid.context_key:
            raise QuestionFeedbackHistoryError("chain crosses two contexts")
        if parent.feedback_seq >= kid.feedback_seq:
            raise QuestionFeedbackHistoryError("predecessor is not earlier")
    for row in rows:
        seen, cursor, limit = set(), row, len(rows) + 1
        while cursor.supersedes_feedback_id is not None:
            if cursor.feedback_id in seen or limit <= 0:
                raise QuestionFeedbackHistoryError("supersession cycle")
            seen.add(cursor.feedback_id)
            limit -= 1
            cursor = by_id[cursor.supersedes_feedback_id]
    return rows


def active_feedback_for_context(rows, key):
    """The CURRENT head for one context, or None. The head is DERIVED from the
    chain; there is no stored active flag and no UPDATE."""
    chain = [r for r in validate_feedback_history(rows) if r.context_key == key]
    if not chain:
        return None
    superseded = {r.supersedes_feedback_id for r in chain
                  if r.supersedes_feedback_id is not None}
    heads = [r for r in chain if r.feedback_id not in superseded]
    if len(heads) != 1:
        raise QuestionFeedbackHistoryError(
            "context does not have exactly one head")
    return heads[0]


def is_same_event_material(stored, candidate):
    """True iff a STORED row is the exact material content of ``candidate``.
    The recording facts (seq, id, timestamp) are never part of event identity;
    the CHOICE is compared here rather than keyed."""
    if stored is None:
        return False
    return all(stored[name] == getattr(candidate, name)
               for name in FEEDBACK_EVENT_MATERIAL_FIELDS)
