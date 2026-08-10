"""P8-I3 — Subscription Lifecycle Service (Flask-free, fail-closed seam).

Implements the accepted CORRECTED P8-I3-C contract (verdict-B remediation applied).

Layering (OD-K / OD-N): this module holds the lifecycle STATE MACHINE and composes
``engine.entitlement_service`` + ``engine.plan_catalog``. Durable atomicity, durable
idempotency, the **in-transaction** stale-effective_at guard (RC-I2), the
**in-transaction** pending-schedule exclusivity guard (RC-I1) and the optimistic
from-state guard all live in the mechanical ``account_store.apply_lifecycle_event``
primitive (which imports no commercial module). The service does NOT rely on a
pre-read for concurrency safety — the store transaction is the sole authority.

The append-only ``subscription_lifecycle_events`` log is the SOURCE OF TRUTH; it
carries the scheduled target plan (RC-I4) so the derived ``subscription_lifecycle_state``
cache is fully reconstructable from the log alone (``rebuild_from_events``). The clock
is INJECTED (``now`` — integer epoch seconds), never read from wall-clock, so lifecycle
decisions are deterministic. §10 account fail-closed (missing/disabled/deleted) is
enforced at THIS service boundary for every lifecycle read and mutation (RC-I6); the
low-level store rebuild primitive stays account-unaware.

Boundaries: NO payment provider / checkout / webhooks / invoices / refunds / tax; NO
provider payloads or secrets; ``external_reference`` is opaque. Quota accounting stays
with P8-I2 (never read/written/reset here). Existing-data read/export/delete is never
blocked by lifecycle state (anti-lock-in). RC-1: lifecycle ``none`` is
entitlement-neutral — it defers entirely to the existing P8-I1 resolution and never
downgrades a legacy assigned plan.
"""

from engine import plan_catalog
from engine import entitlement_service


# --- canonical technical states (5 stored + 1 implicit) ----------------------
STATE_NONE = "none"          # implicit — no lifecycle row
STATE_TRIALING = "trialing"
STATE_ACTIVE = "active"
STATE_PAST_DUE = "past_due"
STATE_CANCELED = "canceled"
STATE_EXPIRED = "expired"

STORED_STATES = frozenset({STATE_TRIALING, STATE_ACTIVE, STATE_PAST_DUE,
                           STATE_CANCELED, STATE_EXPIRED})
TERMINAL_STATES = frozenset({STATE_CANCELED, STATE_EXPIRED})

# --- canonical, provider-neutral events (exactly one per semantic) -----------
EV_STARTED = "subscription_started"
EV_TRIAL_STARTED = "trial_started"
EV_TRIAL_CONVERTED = "trial_converted"
EV_TRIAL_ENDED = "trial_ended"
EV_RENEWED = "subscription_renewed"
EV_CHANGE_SCHEDULED = "subscription_change_scheduled"   # scheduled PLAN change ONLY
EV_CHANGED = "subscription_changed"                     # plan change applied
EV_CANCELLATION_REQUESTED = "cancellation_requested"    # the single cancel-request event
EV_CANCELLED = "subscription_cancelled"                 # effective cancellation
EV_EXPIRED = "subscription_expired"                     # active/past_due -> expired
EV_PAYMENT_STATUS_CHANGED = "payment_status_changed"

CANONICAL_EVENTS = frozenset({
    EV_STARTED, EV_TRIAL_STARTED, EV_TRIAL_CONVERTED, EV_TRIAL_ENDED, EV_RENEWED,
    EV_CHANGE_SCHEDULED, EV_CHANGED, EV_CANCELLATION_REQUESTED, EV_CANCELLED,
    EV_EXPIRED, EV_PAYMENT_STATUS_CHANGED,
})

_SCHEDULING_EVENTS = frozenset({EV_CHANGE_SCHEDULED, EV_CANCELLATION_REQUESTED})


class LifecycleError(Exception):
    """Fail-closed lifecycle error (invalid transition, unknown/malformed event,
    account not authoritative, stale/out-of-order event, conflicting concurrent
    write, pending-schedule conflict). Kept generic."""


class LifecycleResult:
    __slots__ = ("status", "current_state", "event_id")

    def __init__(self, status, current_state, event_id):
        self.status = status
        self.current_state = current_state
        self.event_id = event_id

    def __repr__(self):
        return "LifecycleResult(status=%r, current_state=%r, event_id=%r)" % (
            self.status, self.current_state, self.event_id)


class LifecycleProjection:
    __slots__ = ("current_state", "projected_state", "cancellation_pending",
                 "scheduled_event_type", "scheduled_effective_at")

    def __init__(self, current_state, projected_state, cancellation_pending,
                 scheduled_event_type, scheduled_effective_at):
        self.current_state = current_state
        self.projected_state = projected_state
        self.cancellation_pending = cancellation_pending
        self.scheduled_event_type = scheduled_event_type
        self.scheduled_effective_at = scheduled_effective_at

    def __repr__(self):
        return ("LifecycleProjection(current_state=%r, projected_state=%r, "
                "cancellation_pending=%r)" % (self.current_state,
                self.projected_state, self.cancellation_pending))


class Event:
    """Read-only view of one durable lifecycle event (incl. scheduled target plan)."""

    __slots__ = ("event_id", "account_id", "event_type", "from_state", "to_state",
                 "effective_at", "recorded_at", "reason", "source",
                 "external_reference", "idempotency_key", "sched_effective_at",
                 "target_plan_id", "target_plan_version")

    def __init__(self, row):
        for k in self.__slots__:
            setattr(self, k, row.get(k))


def _require_int_time(value, label):
    if not isinstance(value, int) or isinstance(value, bool):
        raise LifecycleError("%s must be an integer epoch time" % label)
    return value


def _require_active_account(account_store, account_id):
    """§10 fail-closed: missing / disabled / deleted account is denied at the
    lifecycle service boundary (RC-I6). Returns the account dict on success."""
    if not account_id:
        raise LifecycleError("no account identity")
    try:
        account = account_store.get_account_by_id(account_id)
    except Exception:
        raise LifecycleError("account lookup failed")
    if account is None:
        raise LifecycleError("account does not exist")
    if account.get("status") != "active":
        raise LifecycleError("account not active")
    return account


def _target_state(from_state, event_type, payment_status):
    """Pure transition function → the resulting stored state for a NON-scheduling
    event, or raise :class:`LifecycleError` for an invalid transition."""
    fs = from_state
    et = event_type
    if et == EV_STARTED:
        if fs in (STATE_NONE, STATE_CANCELED, STATE_EXPIRED):
            return STATE_ACTIVE
    elif et == EV_TRIAL_STARTED:
        if fs in (STATE_NONE, STATE_CANCELED, STATE_EXPIRED):
            return STATE_TRIALING
    elif et == EV_TRIAL_CONVERTED:
        if fs == STATE_TRIALING:
            return STATE_ACTIVE
    elif et == EV_TRIAL_ENDED:
        if fs == STATE_TRIALING:
            return STATE_EXPIRED
    elif et == EV_RENEWED:
        if fs == STATE_ACTIVE:
            return STATE_ACTIVE
    elif et == EV_PAYMENT_STATUS_CHANGED:
        if fs == STATE_ACTIVE and payment_status == "failed":
            return STATE_PAST_DUE
        if fs == STATE_PAST_DUE and payment_status == "recovered":
            return STATE_ACTIVE
    elif et == EV_EXPIRED:                                  # RC-2 canonical exit
        if fs in (STATE_ACTIVE, STATE_PAST_DUE):
            return STATE_EXPIRED
    elif et == EV_CANCELLED:                                # RC-2/RC-3 effective cancel
        if fs in (STATE_TRIALING, STATE_ACTIVE, STATE_PAST_DUE):
            return STATE_CANCELED
    elif et == EV_CHANGED:                                  # plan change; state unchanged
        if fs in (STATE_TRIALING, STATE_ACTIVE):
            return fs
    raise LifecycleError("invalid transition %r --%s-->" % (fs, et))


def _row_to_projection(row, now):
    if row is None:
        return LifecycleProjection(STATE_NONE, STATE_NONE, False, None, None)
    current = row["current_state"]
    sched_ev = row["scheduled_event_type"]
    sched_at = row["scheduled_effective_at"]
    cancellation_pending = sched_ev == EV_CANCELLED
    projected = current
    if sched_at is not None and now is not None and int(now) >= int(sched_at):
        # a due scheduled transition is PROJECTED (never written by a read).
        if sched_ev == EV_CANCELLED:
            projected = STATE_CANCELED
        # a due scheduled PLAN change leaves the lifecycle state unchanged.
    return LifecycleProjection(current, projected, cancellation_pending,
                               sched_ev, sched_at)


def _map_status(status, actual_state):
    if status == "account_missing":
        raise LifecycleError("account does not exist")
    if status == "account_inactive":
        raise LifecycleError("account not active")
    if status == "conflict_stale":
        raise LifecycleError("stale/conflicting lifecycle state (was %r)" % actual_state)


def get_state(account_store, account_id, *, now=None):
    """Read-only projection of the current lifecycle state. Fail-closed for a
    missing/disabled/deleted account (§10, RC-I6). NEVER writes; a due scheduled
    transition is projected without mutating the durable log/state."""
    _require_active_account(account_store, account_id)
    row = account_store.get_lifecycle_state_row(account_id)
    return _row_to_projection(row, now)


def list_events(account_store, account_id):
    """Ordered durable event log (source of truth). Fail-closed for a
    missing/disabled/deleted account (§10, RC-I6)."""
    _require_active_account(account_store, account_id)
    return [Event(r) for r in account_store.list_lifecycle_events(account_id)]


def rebuild_state_from_events(account_store, account_id):
    """Deterministically replay the append-only log → the current stored state
    (proves event-log ⇔ derived-state equivalence). Fail-closed (§10)."""
    _require_active_account(account_store, account_id)
    state = STATE_NONE
    for row in account_store.list_lifecycle_events(account_id):
        if row["event_type"] in _SCHEDULING_EVENTS:
            continue
        state = row["to_state"]
    return state


def rebuild_from_events(account_store, account_id):
    """Reconstruct the FULL derived state (current state + any pending scheduled
    transition, incl. its target plan) from the append-only event log ALONE —
    proving the log is a sufficient source of truth (RC-I4). Fail-closed (§10)."""
    _require_active_account(account_store, account_id)
    state = STATE_NONE
    sched_to = sched_at = sched_ev = sched_pid = sched_pv = sched_eid = None
    for row in account_store.list_lifecycle_events(account_id):
        et = row["event_type"]
        if et in _SCHEDULING_EVENTS:
            sched_ev = EV_CANCELLED if et == EV_CANCELLATION_REQUESTED else EV_CHANGED
            sched_to = STATE_CANCELED if et == EV_CANCELLATION_REQUESTED else None
            sched_at = row["sched_effective_at"]
            sched_pid = row["target_plan_id"]
            sched_pv = row["target_plan_version"]
            sched_eid = row["event_id"]
        else:
            state = row["to_state"]
            sched_to = sched_at = sched_ev = sched_pid = sched_pv = sched_eid = None
    return {"current_state": state, "scheduled_to_state": sched_to,
            "scheduled_effective_at": sched_at, "scheduled_event_type": sched_ev,
            "scheduled_plan_id": sched_pid, "scheduled_plan_version": sched_pv,
            "scheduled_event_id": sched_eid}


def apply_event(account_store, account_id, event_type, *, now,
                idempotency_key=None, effective_at=None, source=None,
                external_reference=None, reason=None, payment_status=None,
                target_plan=None):
    """Apply one canonical lifecycle event durably. Returns a
    :class:`LifecycleResult` (``applied`` / ``idempotent_replay``). Raises
    :class:`LifecycleError` fail-closed for an unknown/malformed event, an invalid
    transition, a non-authoritative account, a stale/out-of-order event, a
    pending-schedule conflict, or a conflicting concurrent write. Concurrency
    safety is enforced entirely inside the store transaction (no reliance on a
    service pre-read)."""
    if not account_id:
        raise LifecycleError("no account identity")
    if event_type not in CANONICAL_EVENTS:
        raise LifecycleError("unknown lifecycle event %r" % (event_type,))
    _require_int_time(now, "now")

    # Durable idempotency: a replayed key returns the prior outcome without
    # re-validating the transition (the state may have advanced). The store's
    # UNIQUE(account_id, idempotency_key) remains the atomic authority for races.
    if idempotency_key is not None:
        prior = account_store.find_lifecycle_event(account_id, idempotency_key)
        if prior is not None:
            cur = account_store.get_lifecycle_state_row(account_id)
            state = cur["current_state"] if cur is not None else STATE_NONE
            return LifecycleResult("idempotent_replay", state, prior["event_id"])

    # Compute the transition/schedule from the (advisory) current state; the store
    # re-checks all guards in-transaction, so a concurrent change fails closed there.
    row = account_store.get_lifecycle_state_row(account_id)
    from_state = row["current_state"] if row is not None else STATE_NONE

    if event_type in _SCHEDULING_EVENTS:
        future_eff = _require_int_time(effective_at, "effective_at")
        if from_state not in (STATE_TRIALING, STATE_ACTIVE):
            raise LifecycleError("cannot schedule from state %r" % (from_state,))
        if event_type == EV_CANCELLATION_REQUESTED:
            sched_to, sched_ev = STATE_CANCELED, EV_CANCELLED
            sched_pid = sched_pv = None
            ev_target_id = ev_target_ver = None
        else:  # EV_CHANGE_SCHEDULED — a scheduled PLAN change (NOT a cancellation)
            if not target_plan:
                raise LifecycleError("subscription_change_scheduled requires target_plan")
            sched_to, sched_ev = None, EV_CHANGED
            sched_pid, sched_pv = target_plan
            ev_target_id, ev_target_ver = target_plan
        status, state, event_id = account_store.apply_lifecycle_event(
            account_id, event_type=event_type, expected_from_state=from_state,
            new_current_state=from_state, event_to_state=from_state,
            effective_at=str(now), recorded_at=str(now), reason=reason,
            source=source, external_reference=external_reference,
            idempotency_key=idempotency_key, is_scheduling=True,
            require_no_pending=True, event_sched_effective_at=str(future_eff),
            target_plan_id=ev_target_id, target_plan_version=ev_target_ver,
            scheduled_to_state=sched_to, scheduled_effective_at=str(future_eff),
            scheduled_event_type=sched_ev, scheduled_plan_id=sched_pid,
            scheduled_plan_version=sched_pv)
        _map_status(status, state)
        return LifecycleResult(status, state, event_id)

    # Non-scheduling event → a concrete transition (clears any pending schedule).
    eff = now if effective_at is None else _require_int_time(effective_at, "effective_at")
    to_state = _target_state(from_state, event_type, payment_status)
    assignment = None
    ev_target_id = ev_target_ver = None
    if event_type == EV_CHANGED:
        if not target_plan:
            raise LifecycleError("subscription_changed requires a target_plan")
        assignment = (target_plan[0], target_plan[1])
        ev_target_id, ev_target_ver = target_plan          # source-of-truth record
    status, state, event_id = account_store.apply_lifecycle_event(
        account_id, event_type=event_type, expected_from_state=from_state,
        new_current_state=to_state, event_to_state=to_state, effective_at=str(eff),
        recorded_at=str(now), reason=reason, source=source,
        external_reference=external_reference, idempotency_key=idempotency_key,
        is_scheduling=False, require_no_pending=False,
        event_sched_effective_at=None, target_plan_id=ev_target_id,
        target_plan_version=ev_target_ver, scheduled_to_state=None,
        scheduled_effective_at=None, scheduled_event_type=None,
        scheduled_plan_id=None, scheduled_plan_version=None, assignment=assignment)
    _map_status(status, state)
    return LifecycleResult(status, state, event_id)


def materialize_due(account_store, account_id, *, now):
    """AUTHORIZED durable materialization of a due scheduled transition (append the
    canonical event + update derived state atomically). Returns a
    :class:`LifecycleResult`, or ``None`` when nothing is due. Read/projection paths
    never call this. Idempotency is bound to the durable SCHEDULING EVENT id (RC-I5),
    so reusing the same ``effective_at`` in a later epoch materializes separately;
    a repeated materialization of the SAME scheduled event is idempotent."""
    _require_active_account(account_store, account_id)
    _require_int_time(now, "now")
    row = account_store.get_lifecycle_state_row(account_id)
    if row is None or row["scheduled_effective_at"] is None:
        return None
    if now < int(row["scheduled_effective_at"]):
        return None
    sched_ev = row["scheduled_event_type"]
    idem = "materialize:%s" % (row["scheduled_event_id"],)   # epoch-unique
    if sched_ev == EV_CANCELLED:
        return apply_event(account_store, account_id, EV_CANCELLED, now=now,
                           idempotency_key=idem, reason="scheduled")
    if sched_ev == EV_CHANGED:
        target = (row["scheduled_plan_id"], row["scheduled_plan_version"])
        return apply_event(account_store, account_id, EV_CHANGED, now=now,
                           idempotency_key=idem, reason="scheduled",
                           target_plan=target)
    return None


def _terminal_default_decision(account_store, account_id, capability):
    """Fail-closed account check + entitlement computed from the DEFAULT technical
    plan identity (terminal lifecycle projects to default; never the assigned
    plan)."""
    if not account_id:
        raise entitlement_service.EntitlementError("no account identity")
    try:
        account = account_store.get_account_by_id(account_id)
    except Exception:
        raise entitlement_service.EntitlementError("account lookup failed")
    if account is None:
        raise entitlement_service.EntitlementError("account does not exist")
    if account.get("status") != "active":
        raise entitlement_service.EntitlementError("account not active")
    identity = plan_catalog.default_plan_identity()
    try:
        descriptor = plan_catalog.entitlement_descriptor(*identity)
    except plan_catalog.CatalogError:
        raise entitlement_service.EntitlementError("catalog/descriptor failure")
    allowed = bool(descriptor.get(capability, False))
    return entitlement_service.Decision(
        allow=allowed, reason=("granted" if allowed else "not_entitled"),
        plan_identity=identity)


def project_effective_entitlement(account_store, account_id, capability, *, now=None):
    """Derive effective entitlement = f(lifecycle_state, assigned_plan) via the
    P8-I1 seam. READ-ONLY (projects a due terminal transition without writing).

      * ``none`` / ``active`` / ``trialing`` / ``past_due`` → delegate UNCHANGED to
        ``entitlement_service.evaluate_entitlement`` (RC-1: ``none`` is
        entitlement-neutral — assigned plan if assigned, else default; ``past_due``
        retains entitlement — TECHNICAL SAFETY DEFAULT).
      * terminal ``canceled`` / ``expired`` (incl. a due-but-unmaterialized
        cancellation) → project to the DEFAULT technical entitlement.

    Anti-lock-in: governs capability entitlement only; never blocks existing-data
    read/export/delete."""
    projection = get_state(account_store, account_id, now=now)
    if projection.projected_state in TERMINAL_STATES:
        return _terminal_default_decision(account_store, account_id, capability)
    return entitlement_service.evaluate_entitlement(account_store, account_id, capability)
