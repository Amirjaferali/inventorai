"""
engine/interface_observation.py

Stage 15 Slice 4 — Interface Verification Observation Event: the semantic
owner of the inventor's own report of what actually happened when they tested
or checked ONE Owner-declared Stage-15 interface.

An observation is OWNER-STATED, UNVALIDATED historical reporting. It is never
a PASS / FAIL / PARTIAL / INCONCLUSIVE outcome, never a comparison with the
acceptance criterion, never a verified interface, an established
compatibility or feasibility, an engineering approval, a validation, Evidence,
an IRL, readiness, maturity, progression or gap input, and nothing here reads,
parses, grades or interprets the inventor's text.

APPEND-ONLY EVENT MODEL
-----------------------
* The existing Stage-15 ``interface_id`` stays the ONLY interface identity;
  there is no run, test or evidence entity.
* Every stored event carries a new, opaque, server-generated
  ``observation_id`` derived from nothing the inventor typed, no position and
  no interface identity.
* A separately reported check (a first check, a retest, a later retest) is an
  independent ROOT event. A retest never supersedes an earlier check merely
  because it happened later; identical text may legitimately be a real
  retest.
* A CORRECTION is a new event superseding the current HEAD of ONE existing
  chain of the same interface. At most one successor per event: no forks.
* Historical events are never rewritten or deleted (no Withdraw here).

CONTEXT AT RECORDING
--------------------
A ROOT event freezes, without interpretation, the interface's three CURRENT
DURABLE verification-preparation values (``engine.subsystem_model``
``InterfacePreparation``) when it was recorded: the intended operating
conditions, the observable acceptance criterion and the evidence or review
needed — each the exact durable text or ``None`` for explicit absence. All
three absent is a VALID root context: unlike the current-value preparation
owner (which stores no row when nothing is recorded), history keeps the fact
that nothing was prepared at that time. It is PLANNING CONTEXT AT RECORDING,
never proof that those conditions were used in the physical check. The
interface description and endpoints are not frozen: they stay canonical,
immutable interface truth reachable through ``interface_id``. A correction
corrects the observation only and carries NO context.

``recorded_at`` is when InventorAI recorded the event, never the time the
check was performed.
"""
import re
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from engine.subsystem_model import (
    PREPARATION_FIELDS, is_valid_interface_id, valid_preparation_text,
)

# Explicit bound (characters), the bound the Stage-15 preparation inputs
# already use. Over-limit input is rejected, never truncated.
MAX_OBSERVATION_TEXT_LENGTH = 1000
# Bounded growth: a project cannot accumulate an unbounded observation
# history (roots and corrections together). Never pruned at the cap.
MAX_OBSERVATIONS_PER_PROJECT = 200
_OBSERVATION_ID_RE = re.compile(r"\Aobs-[0-9a-f]{32}\Z")
# The frozen context fields, in the preparation owner's own order.
CONTEXT_FIELDS = PREPARATION_FIELDS


class ObservationError(ValueError):
    """A proposed or durable observation event violates the bounded Stage-15
    Slice-4 contract. Structural message only — never user text."""


@dataclass(frozen=True)
class ObservationContext:
    """CONTEXT AT RECORDING of ONE check (its root event): the interface's
    durable preparation values when the observation was recorded. ``None`` is
    explicit absence; every field ``None`` is valid. Frozen verbatim."""
    operating_conditions: Optional[str] = None
    acceptance_criterion: Optional[str] = None
    evidence_needed: Optional[str] = None


@dataclass(frozen=True)
class InterfaceObservation:
    """ONE append-only observation event. A root has
    ``supersedes_observation_id`` ``None`` and a ``context``; a correction
    names the head it supersedes and has no context."""
    observation_id: str
    interface_id: str
    observation_text: str
    supersedes_observation_id: Optional[str]
    recorded_at: str
    context: Optional[ObservationContext] = None


def new_observation_id():
    """A system-generated, opaque, collision-safe event identity."""
    return "obs-" + uuid.uuid4().hex


def is_valid_observation_id(value):
    return isinstance(value, str) and bool(_OBSERVATION_ID_RE.match(value))


def valid_observation_text(value):
    """A stored observation is exactly what the route stores: non-empty,
    already trimmed (internal line breaks kept), within the bound, no NUL."""
    return (isinstance(value, str) and value == value.strip()
            and 0 < len(value) <= MAX_OBSERVATION_TEXT_LENGTH
            and "\x00" not in value)


def context_from_preparation(preparation):
    """The frozen context for a root from the interface's DURABLE
    ``InterfacePreparation`` (``None`` when nothing is recorded: all three
    fields absent). Never built from unsaved form text."""
    if preparation is None:
        return ObservationContext()
    return ObservationContext(**{f: getattr(preparation, f) for f in CONTEXT_FIELDS})


def valid_context(context):
    return (isinstance(context, ObservationContext)
            and all(getattr(context, f) is None
                    or valid_preparation_text(getattr(context, f))
                    for f in CONTEXT_FIELDS))


def _now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def recorded_root(interface_id, observation_text, context):
    """A NEW root event (one separately reported check) with a fresh id and
    its frozen CONTEXT AT RECORDING."""
    event = InterfaceObservation(new_observation_id(), interface_id,
                                 observation_text, None, _now(), context)
    _check_event(event)
    return event


def recorded_correction(interface_id, observation_text, supersedes_observation_id):
    """A NEW correction event superseding ``supersedes_observation_id``; it
    carries no context (the root's frozen context is never replaced)."""
    event = InterfaceObservation(new_observation_id(), interface_id,
                                 observation_text, supersedes_observation_id,
                                 _now(), None)
    _check_event(event)
    return event


def same_observation_material(stored, event):
    """True when two events carry the SAME submitted material: interface,
    superseded target and observation text. Identity, time and the frozen
    context (captured server-side) are not submitted material."""
    return (stored.interface_id == event.interface_id
            and stored.supersedes_observation_id == event.supersedes_observation_id
            and stored.observation_text == event.observation_text)


def _check_event(event):
    if not isinstance(event, InterfaceObservation):
        raise ObservationError("not an observation event")
    if not is_valid_observation_id(event.observation_id):
        raise ObservationError("observation identity is malformed")
    if not is_valid_interface_id(event.interface_id):
        raise ObservationError("interface identity is malformed")
    if not valid_observation_text(event.observation_text):
        raise ObservationError("observation text is empty, invalid or too long")
    if not isinstance(event.recorded_at, str) or not event.recorded_at:
        raise ObservationError("recorded time is missing")
    if event.supersedes_observation_id is None:
        if not valid_context(event.context):
            raise ObservationError("a root event carries no valid context")
    else:
        if not is_valid_observation_id(event.supersedes_observation_id):
            raise ObservationError("superseded identity is malformed")
        if event.context is not None:
            raise ObservationError("a correction may not carry context")


def validate_observation_history(events):
    """Validate one project's durable observation events in stored order and
    return them as a tuple, or raise ``ObservationError``. At most the cap;
    every event is valid; ids are distinct; a correction supersedes an
    EARLIER event of the SAME interface (so no cycle is possible) and no event
    has two successors: only linear correction chains."""
    items = tuple(events or ())
    if len(items) > MAX_OBSERVATIONS_PER_PROJECT:
        raise ObservationError("too many observation events")
    seen = {}
    succeeded = set()
    for event in items:
        _check_event(event)
        if event.observation_id in seen:
            raise ObservationError("observation identity is duplicated")
        target = event.supersedes_observation_id
        if target is not None:
            prior = seen.get(target)
            if prior is None:
                raise ObservationError("a correction supersedes no earlier event")
            if prior.interface_id != event.interface_id:
                raise ObservationError("a correction crosses interfaces")
            if target in succeeded:
                raise ObservationError("an event has two successors")
            succeeded.add(target)
        seen[event.observation_id] = event
    return items


def head_ids(events):
    """The ids of every chain's current head (events with no successor)."""
    succeeded = {e.supersedes_observation_id for e in events
                 if e.supersedes_observation_id is not None}
    return {e.observation_id for e in events} - succeeded


def observation_chains(events, interface_id=None):
    """The check chains of an already-validated history, in root order:
    ``[{"root": ev, "head": ev, "history": [root, ..., head]}]`` (optionally
    for one interface). Pure; identity only."""
    successor = {e.supersedes_observation_id: e for e in events
                 if e.supersedes_observation_id is not None}
    chains = []
    for event in events:
        if event.supersedes_observation_id is not None:
            continue
        if interface_id is not None and event.interface_id != interface_id:
            continue
        history = [event]
        while history[-1].observation_id in successor:
            history.append(successor[history[-1].observation_id])
        chains.append({"root": event, "head": history[-1], "history": history})
    return chains
