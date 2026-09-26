"""Safe Question Reduction Slice 1 — deterministic, question-scoped NeedRouting.

Purpose : record, durably and append-only, that a committed Path-N question's
          information is owed by a SPECIALIST (or EVIDENCE) rather than by the
          inventor, WITHOUT claiming the underlying requirement is solved.
Carrier : ``NeedRoutingRevision`` — its own sidecar history (engine.record_store
          ``need_routing_revisions``), never an ``AssertionRecord``: it is a
          SYSTEM event, not an Owner action, so the Owner-action dispositions
          ``specialist_requested`` / ``evidence_requested`` are never reused.
Identity: need = (project_id, gap_type, question_id); revision =
          (project_id, routing_seq). ``question_id`` is the exact canonical
          ``ServedQuestion.question_id`` of a committed routing policy.

What an OUTSTANDING routed question means (and only this):
  * eligible_for_owner_questioning = False — it is not asked as a mandatory
    inventor question;
  * satisfied_for_maturity = False — its gap can never be CLOSED while the
    need is outstanding, and it vetoes the level 1 -> 2 transition.
Routing is orthogonal to gap resolution: no ``Gap.status`` is added or
changed here, no evidence is created, nothing is validated, no specialist is
assigned or reviewed, and risk acceptance never discharges it. A RETRACT
withdraws the routing responsibility; it never claims the need was solved.

Hard boundaries: deterministic, local, no AI, no network, no I/O here (the
store owns persistence). MECHANISM_COMPLETENESS is never routable. Shared logic
reads typed routing metadata only — no domain question id or wording is
encoded in this module.
"""
from dataclasses import dataclass
from typing import Optional

from engine.idea_state import (
    MECHANISM_COMPLETENESS, OPEN, PARTIAL, STAGE_2_GAP_TYPES, SYSTEM_INFERRED,
)

OPERATION_ROUTE = "ROUTE"
OPERATION_RETRACT = "RETRACT"
OPERATIONS = frozenset({OPERATION_ROUTE, OPERATION_RETRACT})

REQUIRED_INPUT_SPECIALIST = "SPECIALIST"
REQUIRED_INPUT_EVIDENCE = "EVIDENCE"
REQUIRED_INPUTS = frozenset({REQUIRED_INPUT_SPECIALIST, REQUIRED_INPUT_EVIDENCE})

# The ONE provenance a routing revision may carry. This is the narrow durable
# SYSTEM_INFERRED writer the Owner authorized for deterministic routing state
# only; it is never legal on the Owner-interaction carrier.
ROUTING_PROVENANCE = SYSTEM_INFERRED

# Only Stage-2 gaps other than the mechanism can carry a routed need: the
# level 1 -> 2 veto below is defined over exactly these.
ROUTABLE_GAP_TYPES = frozenset(STAGE_2_GAP_TYPES - {MECHANISM_COMPLETENESS})

# A bounded per-project history (ROUTE/RETRACT alternations are rare).
MAX_ROUTING_REVISIONS_PER_PROJECT = 64


class NeedRoutingError(ValueError):
    """A routing revision or history violates the closed contract. The message
    is structural only and never carries user content."""


@dataclass(frozen=True)
class NeedRoutingRevision:
    """ONE durable, immutable routing revision. ``routing_seq`` and
    ``after_assertion_seq`` are assigned by the store on append (the caller's
    values are ignored there); ``after_assertion_seq`` is the durable seq of
    the last Owner ledger record that existed when the revision committed
    (-1 = before any Owner record), which is exactly where replay applies it."""
    project_id: str
    routing_seq: int
    gap_type: str
    question_id: str
    after_assertion_seq: int
    operation: str
    required_input: Optional[str]
    policy_ref: str
    supersedes_seq: Optional[int]
    provenance: str
    event_key: str

    @property
    def need(self):
        return (self.gap_type, self.question_id)


# Fields that make two revisions THE SAME event (exact replay on retry). The
# store-assigned positions are never part of identity.
REVISION_EVENT_IDENTITY_FIELDS = (
    "gap_type", "question_id", "operation", "required_input", "policy_ref",
    "supersedes_seq", "provenance", "event_key")


def _is_int(value):
    return isinstance(value, int) and not isinstance(value, bool)


def validate_revision_fields(rev):
    """Closed-vocabulary validation of ONE revision (no history context)."""
    if not isinstance(rev, NeedRoutingRevision):
        raise NeedRoutingError("routing revision has the wrong type")
    for name in ("project_id", "question_id", "policy_ref", "event_key"):
        value = getattr(rev, name)
        if not isinstance(value, str) or not value.strip():
            raise NeedRoutingError(f"routing revision has no usable {name}")
    if rev.gap_type == MECHANISM_COMPLETENESS:
        raise NeedRoutingError(
            "MECHANISM_COMPLETENESS is never routable, parkable or risk-acceptable")
    if rev.gap_type not in ROUTABLE_GAP_TYPES:
        raise NeedRoutingError("routing revision names a non-routable gap")
    if rev.operation not in OPERATIONS:
        raise NeedRoutingError("routing revision has an unknown operation")
    if rev.operation == OPERATION_ROUTE:
        if rev.required_input not in REQUIRED_INPUTS:
            raise NeedRoutingError("ROUTE must name SPECIALIST or EVIDENCE")
    elif rev.required_input is not None:
        raise NeedRoutingError("RETRACT carries no required input")
    if rev.provenance != ROUTING_PROVENANCE:
        raise NeedRoutingError("routing provenance must be SYSTEM_INFERRED")
    if not _is_int(rev.routing_seq) or rev.routing_seq < 0:
        raise NeedRoutingError("routing_seq must be a non-negative integer")
    if not _is_int(rev.after_assertion_seq) or rev.after_assertion_seq < -1:
        raise NeedRoutingError("after_assertion_seq must be an integer >= -1")
    if rev.supersedes_seq is not None and (
            not _is_int(rev.supersedes_seq)
            or not 0 <= rev.supersedes_seq < rev.routing_seq):
        raise NeedRoutingError("supersedes_seq must name an earlier revision")
    return rev


def next_revision_check(history, rev):
    """Chain rule for appending ``rev`` after the VALIDATED ``history``.

    Per need: the first revision is a ROUTE with no predecessor; every later
    revision names that need's current head and alternates ROUTE <-> RETRACT.
    Across the project: positions are contiguous and never go backwards."""
    validate_revision_fields(rev)
    if history and rev.project_id != history[0].project_id:
        raise NeedRoutingError("routing revision belongs to another project")
    if rev.routing_seq != len(history):
        raise NeedRoutingError("routing_seq is not the next position")
    if len(history) >= MAX_ROUTING_REVISIONS_PER_PROJECT:
        raise NeedRoutingError("routing revision cap reached for this project")
    if history and rev.after_assertion_seq < history[-1].after_assertion_seq:
        raise NeedRoutingError("routing revisions cannot move backwards in the ledger")
    head = None
    for prior in history:
        if prior.need == rev.need:
            head = prior
    if head is None:
        if rev.operation != OPERATION_ROUTE or rev.supersedes_seq is not None:
            raise NeedRoutingError("a need's first revision must be an unanchored ROUTE")
    else:
        if rev.supersedes_seq != head.routing_seq:
            raise NeedRoutingError("routing revision does not continue its need's head")
        if rev.operation == head.operation:
            raise NeedRoutingError("routing revisions must alternate ROUTE and RETRACT")
    return rev


def validate_routing_history(rows):
    """Structural validation of ONE project's revisions in routing_seq order.
    Returns the rows as a tuple; raises NeedRoutingError otherwise."""
    history = []
    for rev in rows:
        next_revision_check(history, rev)
        history.append(rev)
    return tuple(history)


def validate_against_policy(rows, domain):
    """Every revision must name a COMMITTED routing policy of ``domain``: the
    exact canonical question id under its own gap, the same policy_ref, and —
    for a ROUTE — the policy's own required input. No parallel identity."""
    if not rows:
        return tuple(rows)
    from engine.path_n_questions import routing_policies
    policies = {(gap, qid): policy
                for gap, qid, policy in routing_policies(domain)}
    for rev in rows:
        policy = policies.get(rev.need)
        if policy is None:
            raise NeedRoutingError("routing revision names no committed policy")
        if rev.policy_ref != policy.policy_ref:
            raise NeedRoutingError("routing revision policy_ref does not match")
        if rev.operation == OPERATION_ROUTE \
                and rev.required_input != policy.required_input:
            raise NeedRoutingError("routing revision required input does not match")
    return tuple(rows)


def is_routing_aware(version):
    """True only for an engine-contract version whose projects may carry
    routing. Every older version keeps its recorded behavior exactly."""
    from engine.session_reconstruction import ROUTING_AWARE_ENGINE_CONTRACT_VERSIONS
    return version in ROUTING_AWARE_ENGINE_CONTRACT_VERSIONS


def creation_event_key(project_id, gap_type, question_id):
    return "nr:%s:%s:%s:ROUTE:0" % (project_id, gap_type, question_id)


def creation_revisions(project_id, domain, path, version):
    """The ROUTE revisions a NEW project materializes at its creation
    boundary: one per committed routing policy of its domain, only for a
    routing-aware version on deterministic Path N. Pure; writes nothing."""
    if path != "N" or not is_routing_aware(version):
        return ()
    from engine.path_n_questions import routing_policies
    revisions = []
    for gap_type, question_id, policy in routing_policies(domain):
        revisions.append(validate_revision_fields(NeedRoutingRevision(
            project_id=project_id, routing_seq=len(revisions),
            gap_type=gap_type, question_id=question_id,
            after_assertion_seq=-1, operation=OPERATION_ROUTE,
            required_input=policy.required_input,
            policy_ref=policy.policy_ref, supersedes_seq=None,
            provenance=ROUTING_PROVENANCE,
            event_key=creation_event_key(project_id, gap_type, question_id))))
    return validate_routing_history(revisions)


# --- in-memory application (live and replay share this ONE function) --------

def apply_revision(state, rev):
    """Apply ONE durable revision to ``state.need_routing``. Validates the
    chain against what the state already carries, so live publication and
    replay reject exactly the same histories. Mutates only that list."""
    carried = list(getattr(state, "need_routing", None) or [])
    next_revision_check(carried, rev)
    carried.append(rev)
    state.need_routing = carried


def active_routes(state):
    """{need: ROUTE revision} for every need whose current head is a ROUTE,
    in routing order."""
    heads = {}
    for rev in getattr(state, "need_routing", None) or ():
        heads[rev.need] = rev
    return {need: rev for need, rev in heads.items()
            if rev.operation == OPERATION_ROUTE}


def outstanding_routed_question_ids(state, gap_type):
    return frozenset(qid for (gap, qid) in active_routes(state) if gap == gap_type)


def gap_has_outstanding_routing(state, gap_type):
    return bool(outstanding_routed_question_ids(state, gap_type))


def outstanding_routed_gaps(state):
    """Routable gap types with at least one outstanding routed need, in the
    canonical Stage-2 priority order."""
    gaps = {gap for (gap, _qid) in active_routes(state)}
    order = ("PHYSICAL_FEASIBILITY", "BOUNDARY_AMBIGUITY")
    return tuple(g for g in order if g in gaps) + tuple(
        sorted(g for g in gaps if g not in order))


def eligible_for_owner_questioning(state, gap_type, question_id):
    return question_id not in outstanding_routed_question_ids(state, gap_type)


def satisfied_for_maturity(state, gap_type, question_id):
    """A routed need is never satisfied for maturity while outstanding. A
    question that is not routed has no routing opinion (True here; the gap's
    own lifecycle decides)."""
    return question_id not in outstanding_routed_question_ids(state, gap_type)


def owner_questioning_exhausted(state, gap):
    """True when ``gap`` still has an outstanding routed need AND the ladder
    position it would serve next is that routed question: the inventor's
    mandatory questioning of this gap is over while the gap stays unresolved.

    Pure. Fails SAFE: any lookup failure answers False, so existing serving
    stands and no question is ever hidden by an error."""
    if gap is None or gap.status not in (OPEN, PARTIAL):
        return False
    routed = outstanding_routed_question_ids(state, gap.gap_type)
    if not routed:
        return False
    try:
        from engine.path_n_questions import get_served_question
        served = get_served_question(gap.gap_type, gap.iterations_open,
                                     domain=getattr(state, "domain", None))
    except Exception:
        return False
    return served is not None and served.question_id in routed


def owner_blocking_open_gaps(state):
    """The OPEN/PARTIAL gaps that still demand mandatory inventor questioning
    — every open gap except those whose Owner work is exhausted by routing.
    ``state.get_open_gaps()`` stays the open-gap TRUTH; this is only the
    questioning view."""
    return [g for g in state.gaps if g.status in (OPEN, PARTIAL)
            and not owner_questioning_exhausted(state, g)]


def outstanding_needs(state):
    """Display/projection view: one tuple per outstanding routed need, in
    routing order, with its committed policy (None if unreadable)."""
    out = []
    for (gap_type, question_id), rev in active_routes(state).items():
        policy = None
        try:
            from engine.path_n_questions import get_served_question_by_id
            served = get_served_question_by_id(
                gap_type, question_id, domain=getattr(state, "domain", None))
            policy = served.routing if served is not None else None
        except Exception:
            policy = None
        out.append((gap_type, question_id, rev.required_input, policy))
    return tuple(out)
