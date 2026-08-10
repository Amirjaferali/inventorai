"""P8-AF-I2 — Subject-Scoped Access Resolution (corrective RED→GREEN).

The accepted P8-AF-C §5.1 frames the canonical resolver as operating "given an
authenticated account". The merged P8-AF-I1 ``resolve_access(grants, *, now)`` took
no subject and could compose grants belonging to DIFFERENT subjects into one
decision — a latent cross-account access vector (§4/§13/§20 #5/#6). This increment
binds resolution to ONE authenticated subject:

    resolve_access(grants, *, subject, now)

Subject scoping happens BEFORE entitlement composition, so a foreign account's
grant can never influence another account's decision. A foreign-subject grant is
excluded INERTLY (it never contributes, never denies, never raises) with explicit
``foreign_subject`` provenance — the smallest-ambiguity behavior: raising on a
foreign grant would itself let another account influence (deny/DoS) this subject's
resolution. The post-filter precedence rule is UNCHANGED from P8-AF-I1 (zero → DENY;
one distinct entitlement → GRANT; competing distinct → FAIL CLOSED). No
organizations / seats / campaigns / roles / trials / persistence / schema.

These tests fail against the merged P8-AF-I1 (no ``subject`` parameter) → RED.
"""

import ast
import os

import pytest

from engine import access_grant as ag
from engine import access_resolver as ar
from engine import plan_catalog

_ENT_A = plan_catalog.default_plan_identity()
_ENT_B = plan_catalog.RESTRICTED_TECHNICAL_PLAN
_EPOCH = 1_000_000
_SUBJ = "account-A"


def _grant(gid="g1", subject=_SUBJ, source="__ref_source_alpha__", ent=_ENT_A,
           effective_from=0, effective_until=None, status=ag.STATUS_ACTIVE,
           provenance="__ref_issuer__"):
    return ag.make_access_grant(
        grant_id=gid, subject=subject, source=source, entitlement_reference=ent,
        effective_from=effective_from, effective_until=effective_until,
        status=status, provenance=provenance)


# 1 — resolution for Subject A ignores a Subject B grant (foreign excluded).
def test_foreign_subject_grant_is_excluded():
    r = ar.resolve_access([_grant(gid="gB", subject="account-B")],
                          subject="account-A", now=_EPOCH)
    assert r.granted is False
    assert ("gB", "foreign_subject") in r.excluded
    assert r.contributing_grant_ids == ()


# 2 — two grants, same entitlement, different subjects NEVER compose.
def test_same_entitlement_different_subjects_never_compose():
    grants = [_grant(gid="gA", subject="account-A"),
              _grant(gid="gB", subject="account-B")]
    r = ar.resolve_access(grants, subject="account-A", now=_EPOCH)
    assert r.granted is True
    assert r.contributing_grant_ids == ("gA", )               # ONLY A's grant
    assert ("gB", "foreign_subject") in r.excluded


# 3 — a foreign grant cannot make a denied Subject A become granted.
def test_foreign_grant_cannot_grant_denied_subject():
    # A has only an EXPIRED grant → denied; B has an active grant → must not rescue A.
    grants = [_grant(gid="gA", subject="account-A", effective_until=_EPOCH),   # expired
              _grant(gid="gB", subject="account-B")]                            # active foreign
    r = ar.resolve_access(grants, subject="account-A", now=_EPOCH)
    assert r.granted is False
    assert r.entitlement_reference is None


# 4 — a foreign grant affects provenance only as an explicit exclusion.
def test_foreign_grant_provenance_is_explicit_exclusion_only():
    grants = [_grant(gid="gA", subject="account-A"),
              _grant(gid="gB", subject="account-B", ent=_ENT_B)]
    r = ar.resolve_access(grants, subject="account-A", now=_EPOCH)
    assert r.granted is True and r.entitlement_reference == _ENT_A
    assert ("gB", "foreign_subject") in r.excluded
    # gB never entered the entitlement competition (would else be ambiguous).
    assert r.reason == "single_effective_entitlement"


# 5 — a matching-subject valid grant still grants (behavior preserved).
def test_matching_subject_valid_grant_grants():
    r = ar.resolve_access([_grant(gid="g1")], subject=_SUBJ, now=_EPOCH)
    assert r.granted is True and r.entitlement_reference == _ENT_A


# 6 — a matching-subject expired grant still denies.
def test_matching_subject_expired_denies():
    r = ar.resolve_access([_grant(effective_until=_EPOCH)], subject=_SUBJ, now=_EPOCH)
    assert r.granted is False
    assert any("expired" in reason for _, reason in r.excluded)


# 7 — matching-subject competing distinct entitlements still fail closed.
def test_matching_subject_competing_entitlements_fail_closed():
    grants = [_grant(gid="g1", ent=_ENT_A), _grant(gid="g2", ent=_ENT_B)]
    r = ar.resolve_access(grants, subject=_SUBJ, now=_EPOCH)
    assert r.granted is False
    assert "ambiguous" in r.reason and "precedence_deferred" in r.reason


# 8/9 — subject must be a non-empty canonical string; bad subjects fail closed.
@pytest.mark.parametrize("bad", [None, "", "   ", True, 123, ("account-A", )])
def test_subject_must_be_valid_nonempty_string(bad):
    with pytest.raises(ar.AccessResolverError):
        ar.resolve_access([_grant()], subject=bad, now=_EPOCH)


# 8b — empty/missing subject MUST NOT act as a wildcard/global selector.
def test_empty_subject_is_not_a_wildcard():
    with pytest.raises(ar.AccessResolverError):
        ar.resolve_access([_grant(subject="account-A"),
                           _grant(gid="g2", subject="account-B")],
                          subject="", now=_EPOCH)


# 10 — input order does not affect the subject-scoped result.
def test_order_independence_under_subject_scope():
    a = _grant(gid="a", subject="account-A")
    b = _grant(gid="b", subject="account-B")
    r1 = ar.resolve_access([a, b], subject="account-A", now=_EPOCH)
    r2 = ar.resolve_access([b, a], subject="account-A", now=_EPOCH)
    assert (r1.granted, r1.entitlement_reference, r1.selected_grant_id,
            r1.contributing_grant_ids, r1.excluded) == \
           (r2.granted, r2.entitlement_reference, r2.selected_grant_id,
            r2.contributing_grant_ids, r2.excluded)


# 11 — list / tuple / generator inputs are deterministic and equivalent.
def test_iterable_shapes_are_deterministic():
    gs = [_grant(gid="g1"), _grant(gid="gB", subject="account-B")]
    as_list = ar.resolve_access(list(gs), subject="account-A", now=_EPOCH)
    as_tuple = ar.resolve_access(tuple(gs), subject="account-A", now=_EPOCH)
    as_gen = ar.resolve_access((g for g in gs), subject="account-A", now=_EPOCH)
    for r in (as_list, as_tuple, as_gen):
        assert r.granted is True and r.contributing_grant_ids == ("g1", )


# 12 — resolver does not mutate its input grants.
def test_no_mutation_under_subject_scope():
    g = _grant(gid="g1")
    snap = (g.grant_id, g.subject, g.entitlement_reference, g.status,
            g.effective_from, g.effective_until)
    ar.resolve_access([g, _grant(gid="gB", subject="account-B")],
                      subject="account-A", now=_EPOCH)
    assert (g.grant_id, g.subject, g.entitlement_reference, g.status,
            g.effective_from, g.effective_until) == snap


# 13 — no authentication behavior is introduced: the resolver imports/inspects no
#      email / password / session / account-store module; the subject is an
#      already-authenticated canonical identity passed in.
def test_no_authentication_behavior_introduced():
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                        "engine", "access_resolver.py")
    src = open(path, encoding="utf-8").read()
    imported = set()
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.Import):
            for a in node.names:
                imported.add(a.name.split(".")[-1])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imported.add(node.module.split(".")[-1])
            for a in node.names:
                imported.add(a.name.split(".")[-1])
    assert not (imported & {"account_store", "account_credentials", "auth_session"})
    # No authentication BEHAVIOR (credential/session inspection or a verify call).
    # NB: the docstring may legitimately describe the subject as already
    # "authenticated" — that adjective is not auth behavior, so match call/field
    # tokens, not the word itself.
    for token in ("password", "session_token", "authenticate(", "credential",
                  ".verify(", "login"):
        assert token not in src


# 14 — no cross-account data-ownership implication: the resolution exposes only
#      access/entitlement provenance, never a data/ownership permission, and the
#      subject scoping is about ENTITLEMENT, not content access.
def test_no_data_ownership_implication():
    r = ar.resolve_access([_grant()], subject=_SUBJ, now=_EPOCH)
    for forbidden in ("owns", "owner", "can_read", "data_access", "content", "subject"):
        assert not hasattr(r, forbidden)


# 15 — [effective_from, effective_until) FROZEN: from inclusive, until exclusive.
def test_time_boundary_semantics_frozen():
    # from inclusive: effective exactly at effective_from.
    r_from = ar.resolve_access([_grant(effective_from=_EPOCH, effective_until=_EPOCH + 5)],
                               subject=_SUBJ, now=_EPOCH)
    assert r_from.granted is True
    # until exclusive: NOT effective exactly at effective_until.
    r_until = ar.resolve_access([_grant(effective_from=0, effective_until=_EPOCH)],
                                subject=_SUBJ, now=_EPOCH)
    assert r_until.granted is False


# 16 — subject scoping happens BEFORE entitlement composition: a foreign grant
#      with a DIFFERENT entitlement never creates ambiguity for the subject.
def test_subject_scope_precedes_entitlement_composition():
    grants = [_grant(gid="gA", subject="account-A", ent=_ENT_A),
              _grant(gid="gB", subject="account-B", ent=_ENT_B)]   # foreign + different ent
    r = ar.resolve_access(grants, subject="account-A", now=_EPOCH)
    # If scoping ran AFTER composition, distinct entitlements would fail closed.
    assert r.granted is True and r.entitlement_reference == _ENT_A


# 17 — non-AccessGrant input still fails closed (behavior preserved).
def test_non_grant_input_still_fails_closed():
    with pytest.raises(ar.AccessResolverError):
        ar.resolve_access([{"grant_id": "x"}], subject=_SUBJ, now=_EPOCH)


# 18 — injected epoch time still enforced under the new signature.
def test_now_still_injected():
    with pytest.raises(ar.AccessResolverError):
        ar.resolve_access([_grant()], subject=_SUBJ, now=None)
