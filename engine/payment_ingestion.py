"""P8-I4-I1 — Provider-event ingestion coordinator (provider-neutral).

Ties an isolated provider adapter to the canonical commercial authorities without
letting provider vocabulary reach the core:

    adapter.verify_and_parse_event   (authenticity + parse; fail closed)
      → adapter.map_event_to_canonical (provider → CanonicalOperation; fail closed)
        → account/provider mapping resolution (fail closed if missing/ambiguous)
          → canonical transition via the P8-I3 authority (reused, not copied)
            → ATOMIC store ingest: provider-event dedupe + P8-I3 lifecycle mutation
               in ONE BEGIN IMMEDIATE (never half-applied)

The coordinator NEVER mutates lifecycle/quota/entitlement tables directly and NEVER
lets a raw provider event name become a lifecycle event. P8-I1/I2/I3 remain the
authorities; this module orchestrates canonical ingestion only.
"""

from engine import subscription_lifecycle_service as sls
from engine import payment_provider_port as port


class IngestResult:
    __slots__ = ("accepted", "status", "current_state", "lifecycle_event_id",
                 "duplicate")

    def __init__(self, accepted, status, current_state, lifecycle_event_id,
                 duplicate=False):
        self.accepted = accepted
        self.status = status
        self.current_state = current_state
        self.lifecycle_event_id = lifecycle_event_id
        self.duplicate = duplicate

    def __repr__(self):
        return ("IngestResult(accepted=%r, status=%r, current_state=%r, "
                "lifecycle_event_id=%r, duplicate=%r)" % (
                    self.accepted, self.status, self.current_state,
                    self.lifecycle_event_id, self.duplicate))


def ingest_provider_event(account_store, adapter, raw, *, now):
    """Verify, map, and atomically apply one provider event through the canonical
    boundary. Returns an :class:`IngestResult`. Raises
    :class:`engine.payment_provider_port.ProviderBoundaryError` (fail closed) for
    bad authenticity, an unsupported/unmappable event, a missing account mapping, a
    disabled/deleted/missing account, an invalid canonical lifecycle transition, a
    stale/conflicting concurrent write, or a **conflicting duplicate** provider
    event (same identity, different fingerprint). An adapter exception/timeout
    propagates WITHOUT any state mutation."""
    if not isinstance(now, int) or isinstance(now, bool):
        raise port.ProviderBoundaryError("now must be an integer epoch time")

    # 1) authenticity + parse (adapter-isolated). Adapter faults propagate here,
    #    before any persistence, so a timeout/exception mutates nothing.
    parsed = adapter.verify_and_parse_event(raw)
    if parsed is None:
        raise port.ProviderBoundaryError("provider event failed authenticity/parse")

    # 2) provider → canonical (provider vocabulary never passes this point).
    op = adapter.map_event_to_canonical(parsed)
    if op is None:
        raise port.ProviderBoundaryError("provider event is unsupported/unmappable")
    if (not isinstance(op.external_subscription_ref, str)
            or not op.external_subscription_ref.strip()):
        raise port.ProviderBoundaryError("malformed external reference")

    idem = "provider:%s:%s" % (op.provider, op.provider_event_id)   # derived, stable
    fp = port.fingerprint(op.normalized())

    # 2b) durable dedupe pre-check: a previously ACCEPTED identity short-circuits
    #     BEFORE recomputing the transition (the state may since have advanced). An
    #     exact re-delivery replays the prior outcome; a conflicting payload fails
    #     closed. The store re-checks atomically, so concurrent races are still safe.
    prior = account_store.get_provider_event(op.provider, op.provider_event_id)
    if prior is not None:
        if prior["fingerprint"] == fp:
            return IngestResult(True, "provider_duplicate", prior["outcome_state"],
                                prior["lifecycle_event_id"], duplicate=True)
        raise port.ProviderBoundaryError("conflicting duplicate provider event")

    # 3) resolve the internal account via the durable mapping (fail closed).
    account_id = account_store.get_provider_mapping_account(
        op.provider, op.external_subscription_ref)
    if account_id is None:
        raise port.ProviderBoundaryError("no account mapping for provider event")

    # 4) the canonical transition is computed by the P8-I3 authority's OWN transition
    #    function (reused, not copied), INSIDE the store transaction against the
    #    committed in-txn state — so a duplicate is recognised before any transition
    #    is attempted, and only a genuine non-duplicate computes/validates it. The
    #    store stays state-machine-agnostic (it just calls this callback).
    def _transition(from_state):
        try:
            return sls._target_state(from_state, op.canonical_event_type,
                                     op.payment_status)
        except sls.LifecycleError:
            return None                                    # invalid → fail closed

    effective_at = now if op.effective_at is None else op.effective_at

    # 5) ATOMIC: dedupe + lifecycle mutation in one BEGIN IMMEDIATE.
    status, state, event_id = account_store.ingest_provider_lifecycle_event(
        account_id, provider=op.provider, provider_event_id=op.provider_event_id,
        fingerprint=fp, canonical_event_type=op.canonical_event_type,
        now_iso=str(now), transition_fn=_transition, effective_at=str(effective_at),
        recorded_at=str(now), reason="provider_event", source=op.provider,
        external_reference=op.external_subscription_ref, idempotency_key=idem)

    if status == "applied":
        return IngestResult(True, status, state, event_id)
    if status == "provider_duplicate":
        return IngestResult(True, status, state, event_id, duplicate=True)
    if status == "provider_conflict":
        raise port.ProviderBoundaryError("conflicting duplicate provider event")
    if status == "invalid_transition":
        raise port.ProviderBoundaryError("invalid canonical lifecycle transition")
    if status in ("account_missing", "account_inactive"):
        raise port.ProviderBoundaryError("account not authoritative")
    # conflict_stale (concurrent change / stale) — fail closed; not recorded, so a
    # corrected redelivery can still succeed.
    raise port.ProviderBoundaryError("stale/conflicting lifecycle state: %s" % status)
