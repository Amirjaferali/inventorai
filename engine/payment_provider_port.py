"""P8-I4-I1 — Payment Provider Boundary: canonical port + types (provider-neutral).

The stable seam between the InventorAI commercial domain (P8-I1/I2/I3 authorities)
and an external payment provider. This module holds ONLY canonical, provider-neutral
vocabulary: no provider SDK, no network, no secrets, no vendor names. A concrete
provider adapter (e.g. the deterministic fakes in ``engine.payment_fake_adapter``)
implements :class:`PaymentProviderPort`; the P8-I4 coordinator
(``engine.payment_ingestion``) consumes only canonical operations. A raw provider
event name never crosses this boundary — the adapter maps it to a canonical
:class:`CanonicalOperation` whose ``canonical_event_type`` is a P8-I3 lifecycle event.
"""

import hashlib
import json

from engine import subscription_lifecycle_service as sls


class ProviderBoundaryError(Exception):
    """Fail-closed payment-provider-boundary error (bad authenticity, unmappable /
    unsupported provider event, unknown/missing mapping, malformed reference,
    conflicting duplicate, adapter fault). Kept generic; discloses no provider
    detail to the core."""


# The canonical lifecycle events an adapter may map a provider event to (P8-I4-I1
# scope = non-scheduling operations; scheduled-plan-change / cancellation-request
# mapping is a bounded later extension over the existing P8-I3 scheduling seam).
SUPPORTED_CANONICAL_EVENTS = frozenset({
    sls.EV_STARTED, sls.EV_RENEWED, sls.EV_PAYMENT_STATUS_CHANGED,
    sls.EV_CANCELLED, sls.EV_EXPIRED,
})


class ParsedProviderEvent:
    """An adapter's verified+parsed view of a provider event. Provider-native
    fields stay INSIDE the adapter; only the fields the adapter chooses to expose
    for canonical mapping are carried here. Never persisted raw."""

    __slots__ = ("provider", "provider_event_id", "authentic", "native")

    def __init__(self, provider, provider_event_id, authentic, native):
        self.provider = provider
        self.provider_event_id = provider_event_id
        self.authentic = authentic
        self.native = native            # provider-native dict — adapter-private


class CanonicalOperation:
    """A provider-neutral canonical operation the coordinator applies through the
    P8-I3 lifecycle seam. Carries only canonical fields; no provider vocabulary."""

    __slots__ = ("provider", "provider_event_id", "external_subscription_ref",
                 "canonical_event_type", "payment_status", "effective_at")

    def __init__(self, *, provider, provider_event_id, external_subscription_ref,
                 canonical_event_type, payment_status=None, effective_at=None):
        if canonical_event_type not in SUPPORTED_CANONICAL_EVENTS:
            raise ProviderBoundaryError(
                "unsupported canonical event %r" % (canonical_event_type,))
        self.provider = provider
        self.provider_event_id = provider_event_id
        self.external_subscription_ref = external_subscription_ref
        self.canonical_event_type = canonical_event_type
        self.payment_status = payment_status
        self.effective_at = effective_at

    def normalized(self):
        """Deterministic, order-stable canonical fields used for the integrity
        fingerprint. Canonical only — excludes transport noise, secrets, and any
        raw provider payload. Documented field set (stable across restart):
        provider, provider_event_id, canonical_event_type, external_subscription_ref,
        payment_status, effective_at."""
        return {
            "provider": self.provider,
            "provider_event_id": self.provider_event_id,
            "canonical_event_type": self.canonical_event_type,
            "external_subscription_ref": self.external_subscription_ref,
            "payment_status": self.payment_status,
            "effective_at": self.effective_at,
        }


def fingerprint(normalized):
    """Deterministic bounded integrity digest over the canonicalized fields
    (stdlib only; order-stable via sorted keys). Never includes the raw payload or
    secrets. Same normalized content → same digest across process restart."""
    encoded = json.dumps(normalized, sort_keys=True, separators=(",", ":"),
                         ensure_ascii=True)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


class PaymentProviderPort:
    """The minimal stable interface a provider adapter must satisfy for P8-I4-I1.
    Reversible and narrow: it does NOT freeze billing-portal / invoices / refunds /
    taxes / advanced reconciliation. A second adapter must satisfy the same port
    without any change to the P8-I1/I2/I3 authorities."""

    #: provider-neutral slug identifying the adapter (NOT a vendor SDK handle).
    provider_key = None

    def create_customer_context(self, account_id):
        """Establish an opaque provider customer/subscription context for an
        account; returns ``(external_customer_ref, external_subscription_ref)``
        opaque strings. No card data on-platform (hosted/tokenized model)."""
        raise NotImplementedError

    def verify_and_parse_event(self, raw):
        """Authenticity + parse seam. Returns a :class:`ParsedProviderEvent` with
        ``authentic=True`` on success, or ``None`` when authenticity/parse fails
        (fail closed). P8-I4-I1 uses a FAKE verification — no production security is
        implied; real provider signature verification stays isolated in a future
        real adapter."""
        raise NotImplementedError

    def map_event_to_canonical(self, parsed):
        """Translate a verified provider event into a :class:`CanonicalOperation`,
        or return ``None`` when the provider event is unsupported/unmappable (fail
        closed). Provider-native names never leak past this method."""
        raise NotImplementedError
