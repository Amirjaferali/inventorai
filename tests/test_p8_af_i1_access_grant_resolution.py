"""P8-AF-I1 — Canonical Access-Grant + Access-Resolution Foundation (RED→GREEN).

First and smallest implementation increment under the accepted P8-AF-C contract.
Proves ONLY the canonical access-composition seam:

  1. a source-neutral, provider-neutral, immutable Access-Grant value object;
  2. one deterministic, pure, read-only Access-Resolution seam that composes
     effective grants and REFERENCES (never redefines) the P8-I1 entitlement
     authority (``plan_catalog``);
  3. deterministic provenance/explainability of the resolved source.

NO organization / membership / seat / campaign / role / trial-runtime / pricing /
quota-counter / lifecycle-machine / payment-provider code is introduced. The
resolver mutates nothing, consumes no quota, creates no persistence, and invents
no business precedence (competing distinct entitlements FAIL CLOSED — the concrete
ordering of not-yet-activated sources is deferred by P8-AF-C §6).

Modules under test are ABSENT on the base → genuine import RED; the behavioral RED
is demonstrated by the mutation probes recorded in the closure evidence.
"""

import ast
import os

import pytest

# Absent on the base → genuine RED (import error) until implemented.
from engine import access_grant as ag
from engine import access_resolver as ar
from engine import plan_catalog

# A valid P8-I1 catalog identity (referenced, never redefined here).
_ENT_A = plan_catalog.default_plan_identity()                 # (plan_id, version)
_ENT_B = plan_catalog.RESTRICTED_TECHNICAL_PLAN               # a DIFFERENT valid identity
_EPOCH = 1_000_000                                            # fixed injected epoch seconds


def _grant(gid="g1", subject="acct-1", source="__ref_source_alpha__",
           ent=_ENT_A, effective_from=0, effective_until=None,
           status=ag.STATUS_ACTIVE, provenance="__ref_issuer__"):
    return ag.make_access_grant(
        grant_id=gid, subject=subject, source=source, entitlement_reference=ent,
        effective_from=effective_from, effective_until=effective_until,
        status=status, provenance=provenance)


# 1 — one valid, in-window active grant resolves access to its entitlement.
def test_single_valid_grant_resolves_access():
    r = ar.resolve_access([_grant(effective_until=_EPOCH + 1)], subject="acct-1", now=_EPOCH)
    assert r.granted is True
    assert r.entitlement_reference == _ENT_A
    assert r.selected_grant_id == "g1"


# 2 — expired grant (now >= effective_until) does not resolve access.
def test_expired_grant_denies():
    r = ar.resolve_access([_grant(effective_from=0, effective_until=_EPOCH)], subject="acct-1", now=_EPOCH)
    assert r.granted is False
    assert r.entitlement_reference is None
    assert any("expired" in reason for _, reason in r.excluded)


# 2b — not-yet-effective grant (now < effective_from) does not resolve access.
def test_not_yet_effective_grant_denies():
    r = ar.resolve_access([_grant(effective_from=_EPOCH + 10)], subject="acct-1", now=_EPOCH)
    assert r.granted is False
    assert any("not_yet_effective" in reason for _, reason in r.excluded)


# 3 — revoked / inactive grant does not resolve access.
@pytest.mark.parametrize("status", ["revoked", "inactive"])
def test_revoked_or_inactive_grant_denies(status):
    r = ar.resolve_access([_grant(status=status)], subject="acct-1", now=_EPOCH)
    assert r.granted is False
    assert any(status in reason for _, reason in r.excluded)


# 4 — deterministic result for multiple grants referencing the SAME entitlement:
#     access granted, exactly ONE entitlement reference (no double allowance).
def test_multiple_same_entitlement_grants_single_reference():
    grants = [_grant(gid="g1"), _grant(gid="g2", source="__ref_source_beta__")]
    r = ar.resolve_access(grants, subject="acct-1", now=_EPOCH)
    assert r.granted is True
    assert r.entitlement_reference == _ENT_A
    assert set(r.contributing_grant_ids) == {"g1", "g2"}
    # exactly one entitlement path selected, never summed/duplicated.
    assert r.selected_grant_id == "g1"                       # deterministic min


# 5 — provenance identifies the selected grant/source and explains exclusions.
def test_provenance_explains_selection_and_exclusions():
    grants = [_grant(gid="active", effective_until=_EPOCH + 5),
              _grant(gid="stale", effective_until=_EPOCH)]   # expired
    r = ar.resolve_access(grants, subject="acct-1", now=_EPOCH)
    assert r.granted is True and r.selected_grant_id == "active"
    assert r.reason == "single_effective_entitlement"
    assert ("stale", ) == tuple(gid for gid, _ in r.excluded)


# 6 — resolver does not mutate its input grants (pure/read-only).
def test_resolver_does_not_mutate_input():
    g = _grant(effective_until=_EPOCH + 1)
    snapshot = (g.grant_id, g.subject, g.source, g.entitlement_reference,
                g.effective_from, g.effective_until, g.status, g.provenance)
    ar.resolve_access([g], subject="acct-1", now=_EPOCH)
    assert (g.grant_id, g.subject, g.source, g.entitlement_reference,
            g.effective_from, g.effective_until, g.status, g.provenance) == snapshot


# 7 — resolver imports/consumes NO quota, lifecycle, account, or payment module.
def test_resolver_imports_are_reference_only():
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                        "engine", "access_resolver.py")
    imported = set()
    for node in ast.walk(ast.parse(open(path, encoding="utf-8").read())):
        if isinstance(node, ast.Import):
            for a in node.names:
                imported.add(a.name.split(".")[-1])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imported.add(node.module.split(".")[-1])
            for a in node.names:                             # also the bound names
                imported.add(a.name.split(".")[-1])
    forbidden = {"quota_service", "subscription_lifecycle_service", "account_store",
                 "payment_provider_port", "payment_fake_adapter", "payment_ingestion",
                 "account_credentials", "auth_session"}
    assert not (imported & forbidden), "resolver leaks a non-reference dependency: %r" % (
        imported & forbidden)


# 8 — no double quota: two active same-entitlement grants yield ONE reference
#     (a downstream P8-I2 policy select, never additive).
def test_no_double_quota_composition():
    grants = [_grant(gid="g1"), _grant(gid="g2")]
    r = ar.resolve_access(grants, subject="acct-1", now=_EPOCH)
    assert r.granted is True
    # A single entitlement reference — the sole P8-I2 quota-policy path.
    assert r.entitlement_reference == _ENT_A
    assert isinstance(r.entitlement_reference, tuple) and len(r.entitlement_reference) == 2


# 9 — entitlement authority is REFERENCED, not redefined: an unknown entitlement
#     identity (not in the P8-I1 catalog) is malformed → fail closed.
def test_unknown_entitlement_identity_fails_closed():
    bad = _grant(ent=("__no_such_plan__", "9"))
    with pytest.raises(ar.AccessResolverError):
        ar.resolve_access([bad], subject="acct-1", now=_EPOCH)


# 9b — the resolver never fabricates capabilities: it returns only a catalog
#      identity, never a capability descriptor.
def test_resolution_carries_identity_not_capabilities():
    r = ar.resolve_access([_grant()], subject="acct-1", now=_EPOCH)
    assert not hasattr(r, "capabilities")
    assert r.entitlement_reference in (_ENT_A,)


# 10 — provider-specific data / imports are rejected: access_grant is a leaf that
#      imports no payment/provider module, and a grant cannot carry provider fields.
def test_no_provider_coupling():
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                        "engine", "access_grant.py")
    imported = set()
    for node in ast.walk(ast.parse(open(path, encoding="utf-8").read())):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            mod = getattr(node, "module", None)
            if mod:
                imported.add(mod.split(".")[-1])
            for a in getattr(node, "names", []):
                imported.add(a.name.split(".")[-1])
    assert not any(m.startswith("payment_") for m in imported)
    # Fixed slots prevent provider ids / counters / credentials / pricing fields.
    with pytest.raises(AttributeError):
        _grant().provider_subscription_id = "sub_123"


# 11 — no authentication bypass: a "privileged-looking" subject/source confers
#      NOTHING; without an effective grant, access is denied.
def test_no_auth_bypass_from_privileged_looking_fields():
    r = ar.resolve_access(
        [_grant(subject="owner@example.com", source="owner_admin",
                status="revoked")], subject="owner@example.com", now=_EPOCH)
    assert r.granted is False
    # And an ACTIVE grant grants access purely mechanically — the decision does
    # not depend on the subject/source strings meaning anything special.
    r2 = ar.resolve_access(
        [_grant(subject="nobody", source="__ref_source_alpha__",
                effective_until=_EPOCH + 1)], subject="nobody", now=_EPOCH)
    assert r2.granted is True


# 12 — data ownership is NOT inferred from an access grant: the resolution
#      exposes only access/entitlement, never a cross-account data permission.
def test_no_data_ownership_inference():
    r = ar.resolve_access([_grant(subject="acct-A")], subject="acct-A", now=_EPOCH)
    for forbidden in ("owns", "owner", "can_read", "data_access", "content"):
        assert not hasattr(r, forbidden)


# 13 — fixed injected time is used; wall-clock is never read (now must be given).
def test_now_must_be_injected_integer():
    with pytest.raises(ar.AccessResolverError):
        ar.resolve_access([_grant()], subject="acct-1", now=None)
    with pytest.raises(ar.AccessResolverError):
        ar.resolve_access([_grant()], subject="acct-1", now=True)             # bool is not an epoch int


# 14 — input ordering does not alter the deterministic result.
def test_order_independence():
    a = _grant(gid="a", effective_until=_EPOCH + 1)
    b = _grant(gid="b", effective_until=_EPOCH + 1)
    r1 = ar.resolve_access([a, b], subject="acct-1", now=_EPOCH)
    r2 = ar.resolve_access([b, a], subject="acct-1", now=_EPOCH)
    assert (r1.granted, r1.entitlement_reference, r1.selected_grant_id,
            tuple(sorted(r1.contributing_grant_ids))) == \
           (r2.granted, r2.entitlement_reference, r2.selected_grant_id,
            tuple(sorted(r2.contributing_grant_ids)))


# 15 — competing DISTINCT entitlements fail closed (precedence deferred; no
#      invented business priority such as "bigger plan wins").
def test_competing_distinct_entitlements_fail_closed():
    grants = [_grant(gid="g1", ent=_ENT_A),
              _grant(gid="g2", ent=_ENT_B)]
    r = ar.resolve_access(grants, subject="acct-1", now=_EPOCH)
    assert r.granted is False
    assert r.entitlement_reference is None
    assert "ambiguous" in r.reason and "precedence_deferred" in r.reason
    # order-independent: swapping does not pick a "winner".
    r2 = ar.resolve_access(list(reversed(grants)), subject="acct-1", now=_EPOCH)
    assert r2.granted is False and r2.entitlement_reference is None


# 15b — malformed grant construction fails closed at the value-object boundary.
@pytest.mark.parametrize("kw", [
    {"grant_id": ""},                                        # empty id
    {"subject": ""},                                         # empty subject
    {"source": ""},                                          # empty source
    {"entitlement_reference": ("only-one",)},                # not a 2-tuple
    {"entitlement_reference": ("", "")},                     # empty identity parts
    {"effective_from": "0"},                                 # non-int time
    {"effective_from": True},                                # bool is not epoch int
    {"effective_until": 0, "effective_from": 10},            # until <= from
    {"status": "banana"},                                    # unknown status
])
def test_malformed_grant_fails_closed(kw):
    base = dict(grant_id="g", subject="s", source="src",
                entitlement_reference=_ENT_A, effective_from=0,
                effective_until=None, status=ag.STATUS_ACTIVE, provenance="p")
    base.update(kw)
    with pytest.raises(ag.AccessGrantError):
        ag.make_access_grant(**base)


# 15c — a non-AccessGrant element in the input fails closed.
def test_non_grant_input_fails_closed():
    with pytest.raises(ar.AccessResolverError):
        ar.resolve_access([{"grant_id": "g1"}], subject="acct-1", now=_EPOCH)


# 16 — no persistence/schema is required: resolution is a pure function over
#      in-memory grants (no account_store argument, no DB).
def test_resolution_needs_no_persistence():
    # Zero grants → deterministic deny, no store, no I/O.
    r = ar.resolve_access([], subject="acct-1", now=_EPOCH)
    assert r.granted is False and r.reason == "no_effective_grant"


# 17 — OD-N engine-wide guard still holds with the new access seams recognized as
#      commercial (the deterministic core imports none of them).
def test_od_n_guard_recognizes_access_seams():
    import tests.test_p8_i1_plan_entitlement_foundation as g1
    g1.test_od_n_engine_wide_no_commercial_imports_outside_allowlist()
