"""P7-I1 — Internal Read/Export Service Boundary (RED → GREEN).

Behavioral tests for the accepted, repository-established P7-I1 bounded increment
contract (`docs/governance/P7_I1_INTERNAL_READ_EXPORT_SERVICE_BOUNDARY_INCREMENT_CONTRACT.md`,
PR #402). The seam is INTERNAL ONLY and Flask-free: two read-side use cases —
(1) an authorized durable Project Read and (2) a distinct, deterministic internal
Structured Export composed from durable record data AND the canonical domain
support-state — consuming an already-established store dependency plus an explicit
caller identity, fail-closed on ownership, exposing no raw persistence rows / no
Flask state, and mutating no governed project/business state.

Governed by P7-C §8 + IR-1..IR-6. The Structured Export's domain support-state is
derived from the existing canonical sources only: durable `confirmed_domain`
(`store.load_reconstruction_inputs`) classified by
`engine.domain_activation.support_state` (no activation, no registry mutation).

Provider-free, network-free; SQLite files live only in pytest tmp_path.
"""
import json
import types

import pytest

from engine.idea_state import (
    AssertionRecord,
    OWNER_STATED,
    LEGACY_UNSPECIFIED,
    UNVALIDATED,
    INDEPENDENTLY_VERIFIED,
)
from engine.record_contract import ProjectRecordContract
from engine.record_store import SqliteRecordStore
from engine import domain_activation

# The module under test (P7-I1 seam). Absent on the base → genuine RED for the
# missing capability exercised by every behavioral test below.
from engine import read_export_service as seam


OWNER = "acct_owner"
OTHER = "acct_other"


def _contract(idea_id="idea-p7i1"):
    return ProjectRecordContract(idea_id=idea_id, assertions=[
        AssertionRecord(record_id="rec_1", disposition="answered",
                        content="alpha", gap_context="g1", iteration=1,
                        provenance=OWNER_STATED, validation_status=UNVALIDATED),
        AssertionRecord(record_id="rec_2", disposition="answered",
                        content="beta", gap_context="g2", iteration=2,
                        provenance=LEGACY_UNSPECIFIED,
                        validation_status=INDEPENDENTLY_VERIFIED),
    ])


def _store(tmp_path, owner=OWNER, project_id="p1", idea_id="idea-p7i1",
           confirmed_domain="electronics_electrical"):
    """An ALREADY-ESTABLISHED store with one durable project (IR-1: the seam
    never constructs this). ``confirmed_domain`` is written once at creation."""
    s = SqliteRecordStore(str(tmp_path / "p7i1.sqlite3"))
    ri = None
    if confirmed_domain is not None:
        ri = {"seed_idea_text": "seed", "confirmed_domain": confirmed_domain,
              "path": "path_n", "engine_contract_version": "v1"}
    s.create_project(_contract(idea_id), project_id=project_id,
                     reconstruction_inputs=ri, owner_account_id=owner)
    return s


class _RaisingStore:
    """A store whose ownership lookup fails — the seam must fail closed."""
    def load_owner(self, project_id):
        raise RuntimeError("ownership backend unavailable")

    def load_contract(self, project_id):
        raise AssertionError("must not be reached when unauthorized")

    def load_reconstruction_inputs(self, project_id):
        raise AssertionError("must not be reached when unauthorized")


class _OtherOwnedRaisingContractStore:
    """Project owned by OTHER; contract/recon reads raise. A cross-owner caller
    must be denied BEFORE any contract/recon read (no enumeration leak)."""
    def load_owner(self, project_id):
        return (True, OTHER)

    def load_contract(self, project_id):
        raise AssertionError("cross-owner must be denied before load_contract")

    def load_reconstruction_inputs(self, project_id):
        raise AssertionError("cross-owner must be denied before recon read")


# ---- Authorized durable Project Read ---------------------------------------

def test_authorized_project_read_returns_durable_contract(tmp_path):
    s = _store(tmp_path)
    result = seam.get_authorized_project_read(s, "p1", OWNER)
    assert isinstance(result, ProjectRecordContract)
    assert result.idea_id == "idea-p7i1"
    assert len(result.assertions) == 2


def test_cross_owner_read_denied(tmp_path):
    s = _store(tmp_path)
    with pytest.raises(seam.ProjectAccessDenied):
        seam.get_authorized_project_read(s, "p1", OTHER)


@pytest.mark.parametrize("bad_identity", [None, ""])
def test_missing_identity_read_denied(tmp_path, bad_identity):
    s = _store(tmp_path)
    with pytest.raises(seam.ProjectAccessDenied):
        seam.get_authorized_project_read(s, "p1", bad_identity)


def test_null_owner_durable_project_read_denied(tmp_path):
    s = _store(tmp_path, owner=None, project_id="p_null")
    assert s.load_owner("p_null") == (True, None)      # durable NULL-owner fact
    with pytest.raises(seam.ProjectAccessDenied):
        seam.get_authorized_project_read(s, "p_null", OWNER)
    with pytest.raises(seam.ProjectAccessDenied):
        seam.get_authorized_project_read(s, "p_null", None)


def test_missing_project_read_denied(tmp_path):
    s = _store(tmp_path)
    with pytest.raises(seam.ProjectAccessDenied):
        seam.get_authorized_project_read(s, "does-not-exist", OWNER)


def test_store_ownership_failure_fails_closed(tmp_path):
    with pytest.raises(seam.ProjectAccessDenied):
        seam.get_authorized_project_read(_RaisingStore(), "p1", OWNER)


def test_cross_owner_denied_before_contract_read_no_leak(tmp_path):
    # Observation B: an unauthorized caller is denied before any contract/recon
    # read, so a load failure can never leak project existence/ownership.
    with pytest.raises(seam.ProjectAccessDenied):
        seam.get_authorized_project_read(_OtherOwnedRaisingContractStore(), "p1", OWNER)
    with pytest.raises(seam.ProjectAccessDenied):
        seam.produce_project_export(_OtherOwnedRaisingContractStore(), "p1", OWNER)


# ---- Distinct internal Structured Export ------------------------------------

def test_authorized_structured_export_produced(tmp_path):
    s = _store(tmp_path)
    export = seam.produce_project_export(s, "p1", OWNER)
    assert isinstance(export, dict)
    assert export["idea_id"] == "idea-p7i1"


def test_export_denials_mirror_read(tmp_path):
    # Observation D: every read-side denial case mirrored on the export side.
    s = _store(tmp_path)
    for ident in (OTHER, None, ""):
        with pytest.raises(seam.ProjectAccessDenied):
            seam.produce_project_export(s, "p1", ident)
    with pytest.raises(seam.ProjectAccessDenied):
        seam.produce_project_export(s, "does-not-exist", OWNER)
    with pytest.raises(seam.ProjectAccessDenied):
        seam.produce_project_export(_RaisingStore(), "p1", OWNER)
    s_null = _store(tmp_path, owner=None, project_id="p_null")
    with pytest.raises(seam.ProjectAccessDenied):
        seam.produce_project_export(s_null, "p_null", OWNER)


def test_export_is_semantically_distinct_from_read(tmp_path):
    s = _store(tmp_path)
    contract = seam.get_authorized_project_read(s, "p1", OWNER)
    export = seam.produce_project_export(s, "p1", OWNER)
    assert not isinstance(export, ProjectRecordContract)
    assert export != contract.to_dict()
    assert export != json.loads(contract.to_json())
    assert "assertion_count" in export and export["assertion_count"] == 2
    assert "domain_support_state" in export      # composed from canonical support-state
    assert isinstance(export["validation_summary"], dict)
    a0 = export["assertions"][0]
    assert set(a0) == {"record_id", "disposition", "provenance", "validation_status"}


def test_export_record_content_grounded_no_invented_data(tmp_path):
    s = _store(tmp_path)
    export = seam.produce_project_export(s, "p1", OWNER)
    # No fabricated concepts and no frozen public/export version identity (IR-6).
    for forbidden in ("assumptions", "gaps", "requirements", "evidence",
                      "revision", "version", "contract_version",
                      "generated_at", "schema_id"):
        assert forbidden not in export
    assert export["validation_summary"] == {UNVALIDATED: 1, INDEPENDENTLY_VERIFIED: 1}
    assert export["provenance_summary"] == {OWNER_STATED: 1, LEGACY_UNSPECIFIED: 1}


# ---- Domain support-state composition (blocking correction) -----------------

@pytest.mark.parametrize("domain,expected", [
    ("electronics_electrical", domain_activation.ACTIVATED),
    ("mechanical", domain_activation.RECOGNIZED_NOT_ACTIVATED),
    ("totally_unknown_xyz", domain_activation.UNKNOWN_OR_UNSUPPORTED),
])
def test_export_domain_support_state_grounded(tmp_path, domain, expected):
    s = _store(tmp_path, confirmed_domain=domain)
    export = seam.produce_project_export(s, "p1", OWNER)
    assert export["domain_support_state"] == expected
    # Grounded in the canonical source, not invented.
    assert export["domain_support_state"] == domain_activation.support_state(domain)


def test_export_null_legacy_domain_is_unknown_unsupported(tmp_path):
    # NULL/legacy confirmed_domain → truthful canonical UNKNOWN_OR_UNSUPPORTED.
    s = _store(tmp_path, confirmed_domain=None, project_id="p_legacy")
    assert s.load_reconstruction_inputs("p_legacy") is None
    export = seam.produce_project_export(s, "p_legacy", OWNER)
    assert export["domain_support_state"] == domain_activation.UNKNOWN_OR_UNSUPPORTED


def test_export_does_not_activate_domain_or_mutate_registry(tmp_path):
    s = _store(tmp_path, confirmed_domain="electronics_electrical")
    before_activated = domain_activation.activated_domains()
    before_mech = domain_activation.support_state("mechanical")
    seam.produce_project_export(s, "p1", OWNER)
    assert domain_activation.activated_domains() == before_activated
    assert domain_activation.support_state("mechanical") == before_mech
    assert before_mech == domain_activation.RECOGNIZED_NOT_ACTIVATED


def test_export_is_deterministic(tmp_path):
    s = _store(tmp_path)
    e1 = seam.produce_project_export(s, "p1", OWNER)
    e2 = seam.produce_project_export(s, "p1", OWNER)
    assert e1 == e2
    assert json.dumps(e1, sort_keys=True) == json.dumps(e2, sort_keys=True)


# ---- Non-mutation -----------------------------------------------------------

def _snapshot(store, project_id):
    # Observation C: canonical governed read-side facts (not raw-byte DB):
    # the durable record + owner + reconstruction inputs.
    return (
        store.load_contract(project_id).to_json(),
        store.load_owner(project_id),
        store.load_reconstruction_inputs(project_id),
    )


def test_read_does_not_mutate_governed_state(tmp_path):
    s = _store(tmp_path)
    before = _snapshot(s, "p1")
    seam.get_authorized_project_read(s, "p1", OWNER)
    assert _snapshot(s, "p1") == before


def test_export_does_not_mutate_governed_state(tmp_path):
    s = _store(tmp_path)
    before = _snapshot(s, "p1")
    seam.produce_project_export(s, "p1", OWNER)
    assert _snapshot(s, "p1") == before


# ---- Boundary hygiene (Flask-free, no store construction, no raw rows) -------

def _all_co_names(func):
    """Recursively collect referenced names across a function and its nested
    code objects (Observation E: stronger than a single-level scan)."""
    names = set()
    seen = set()
    stack = [func.__code__]
    while stack:
        code = stack.pop()
        if id(code) in seen:
            continue
        seen.add(id(code))
        names |= set(code.co_names)
        for const in code.co_consts:
            if isinstance(const, types.CodeType):
                stack.append(const)
    return names


def test_seam_is_flask_free_and_constructs_no_store():
    # No Flask/web-framework module imported into the seam namespace.
    assert not any(
        getattr(v, "__name__", "") in ("flask", "werkzeug")
        for v in vars(seam).values() if isinstance(v, types.ModuleType))
    forbidden = {"request", "session", "SESSION_STORE", "_current_account",
                 "render_template", "flask", "Flask"}
    referenced = set()
    for fn in (seam.get_authorized_project_read, seam.produce_project_export,
               seam._is_authorized, seam._domain_support_state, seam._compose_export):
        referenced |= _all_co_names(fn)
    assert not (referenced & forbidden), "seam must be Flask-free (code)"
    # IR-1: the seam constructs/initializes no datastore of its own.
    assert "SqliteRecordStore" not in referenced


def test_read_returns_no_raw_persistence_row(tmp_path):
    s = _store(tmp_path)
    result = seam.get_authorized_project_read(s, "p1", OWNER)
    assert isinstance(result, ProjectRecordContract)
    assert not isinstance(result, (tuple, list))
