"""P8-I4-I1 — deterministic FAKE/reference payment provider adapters.

Two provider-neutral fakes (A and B) satisfy the same :class:`PaymentProviderPort`
with DIFFERENT provider-native vocabularies that both map to the SAME canonical
operations — proving replaceability. NO network, NO SDK, NO real secrets, NO vendor
name. The ``_secret`` is a fake shared token used only to exercise the authenticity
seam; it implies NO production security. Provider-native field names live ONLY inside
these adapters and never cross into the canonical/core layers.

These fakes are NOT a provider selection.
"""

from engine import subscription_lifecycle_service as sls
from engine.payment_provider_port import (
    PaymentProviderPort, ParsedProviderEvent, CanonicalOperation,
    ProviderBoundaryError,
)


# provider-native "kind" → (canonical P8-I3 event, payment_status) — the ONLY place
# provider vocabulary exists; the canonical mapping is identical across adapters.
_MAP_A = {
    "charge_failed": (sls.EV_PAYMENT_STATUS_CHANGED, "failed"),
    "charge_recovered": (sls.EV_PAYMENT_STATUS_CHANGED, "recovered"),
    "sub_started": (sls.EV_STARTED, None),
    "sub_renewed": (sls.EV_RENEWED, None),
    "sub_canceled": (sls.EV_CANCELLED, None),
    "sub_expired": (sls.EV_EXPIRED, None),
}
_MAP_B = {
    "payment.declined": (sls.EV_PAYMENT_STATUS_CHANGED, "failed"),
    "payment.cleared": (sls.EV_PAYMENT_STATUS_CHANGED, "recovered"),
    "activation": (sls.EV_STARTED, None),
    "renewal": (sls.EV_RENEWED, None),
    "cancellation.effective": (sls.EV_CANCELLED, None),
    "term.ended": (sls.EV_EXPIRED, None),
}


class _BaseFakeAdapter(PaymentProviderPort):
    """Shared deterministic fake behaviour. Subclasses set ``provider_key``, the
    native field names, and the provider→canonical map."""

    _KIND_KEY = None
    _SUB_KEY = None
    _EVENT_ID_KEY = None
    _SIG_KEY = None
    _WHEN_KEY = None
    _MAP = None

    def __init__(self, secret="fake-shared-token", fault=None):
        # ``fault`` simulates an adapter fault for tests: "exception" | "timeout".
        self._secret = secret
        self._fault = fault
        self._counter = 0

    def create_customer_context(self, account_id):
        # Deterministic opaque references (no vendor scheme); counter keeps them
        # unique per adapter instance without any wall-clock/randomness.
        self._counter += 1
        cust = "%s:cust:%s:%d" % (self.provider_key, account_id, self._counter)
        sub = "%s:sub:%s:%d" % (self.provider_key, account_id, self._counter)
        return (cust, sub)

    def verify_and_parse_event(self, raw):
        if self._fault == "exception":
            raise ProviderBoundaryError("simulated adapter exception")
        if self._fault == "timeout":
            raise TimeoutError("simulated provider timeout")
        if not isinstance(raw, dict):
            return None
        if raw.get(self._SIG_KEY) != self._secret:      # authenticity seam (fake)
            return None
        event_id = raw.get(self._EVENT_ID_KEY)
        if not isinstance(event_id, str) or not event_id:
            return None
        return ParsedProviderEvent(self.provider_key, event_id, True, dict(raw))

    def map_event_to_canonical(self, parsed):
        if parsed is None or not parsed.authentic:
            return None
        native = parsed.native
        kind = native.get(self._KIND_KEY)
        mapped = self._MAP.get(kind)
        if mapped is None:
            return None                                 # unsupported → fail closed
        event_type, payment_status = mapped
        sub = native.get(self._SUB_KEY)
        if not isinstance(sub, str) or not sub:
            return None
        when = native.get(self._WHEN_KEY)
        try:
            return CanonicalOperation(
                provider=self.provider_key,
                provider_event_id=parsed.provider_event_id,
                external_subscription_ref=sub, canonical_event_type=event_type,
                payment_status=payment_status,
                effective_at=(when if isinstance(when, int)
                              and not isinstance(when, bool) else None))
        except ProviderBoundaryError:
            return None


class FakeReferenceAdapterA(_BaseFakeAdapter):
    provider_key = "fake-alpha"
    _KIND_KEY = "kind"
    _SUB_KEY = "sub"
    _EVENT_ID_KEY = "evt"
    _SIG_KEY = "sig"
    _WHEN_KEY = "when"
    _MAP = _MAP_A


class FakeReferenceAdapterB(_BaseFakeAdapter):
    provider_key = "fake-beta"
    _KIND_KEY = "event"
    _SUB_KEY = "subscription"
    _EVENT_ID_KEY = "id"
    _SIG_KEY = "token"
    _WHEN_KEY = "effective"
    _MAP = _MAP_B
