"""P10-D2 — Decision Workspace Access-Control Remediation (RED/GREEN).

Behaviour-based tests proving the corrected P10-D2 technical model: bare
possession of a Decision Workspace ``did`` no longer authorizes access.
Ownership/session binding is app-layer only (no change to
``engine/decision_workspace.py``, no durable persistence, no new identity
system): an authenticated creator's decisions are bound to their
``account_id``; an anonymous creator's decisions are bound to the creating
browser's own signed Flask session. Read, every mutation route, and export
are all covered identically. Denial is generic and non-enumerating (the same
redirect used for a genuinely nonexistent ``did``).

Real on-disk SQLite (autouse conftest isolation); Flask test client with real
signed cookies; the real account store/credential helpers. No mocks.
"""
import os

import pytest

import web.app as webapp
from web.app import app
from engine import account_credentials as _acct

PW = "correct horse battery staple"        # >= 12 chars


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


@pytest.fixture
def db_path():
    return os.environ["INVENTORAI_DB_PATH"]


def _register(client, email, password=PW):
    return client.post("/register", data={
        "email": email, "password": password, "password_confirm": password})


def _login(client, email, password=PW):
    return client.post("/login", data={"email": email, "password": password})


def _new_signed_in_client(email):
    """A fresh test client, registered and signed in as its own account."""
    c = app.test_client()
    _register(c, email)
    _login(c, email)
    return c


def _create_anonymous(client):
    """Create a decision anonymously via the real route; return its did."""
    r = client.get("/decision-workspace", follow_redirects=False)
    assert r.status_code == 302, r.status_code
    return r.headers["Location"].rsplit("/decision-workspace/", 1)[-1]


def _create_owned(client):
    """Create a decision as the client's already-signed-in account; return did."""
    r = client.get("/decision-workspace", follow_redirects=False)
    assert r.status_code == 302, r.status_code
    return r.headers["Location"].rsplit("/decision-workspace/", 1)[-1]


_DID_ROUTES_MUTATE = (
    ("input", {"text": "x", "claim_class": "observed_fact", "provenance": "unverified"}),
    ("constraint", {"text": "x", "constraint_strength": "hard",
                     "provenance": "unverified"}),
    ("gap", {"action": "resolve", "gap_id": "nonexistent"}),
    ("evidence", {"gap_id": "nonexistent", "text": "x",
                   "claim_class": "observed_fact", "provenance": "unverified"}),
    ("gap-assessment", {"gap_id": "nonexistent", "assessment": "x",
                          "rationale": "x", "resolution_decision": "x"}),
    ("preference", {"action": "clear"}),
    ("candidate", {"candidate_id": "nonexistent", "option_status": "eliminated",
                    "disposition_reason": "x", "disposition_basis": "x"}),
)


# ===========================================================================
# Anonymous creator: same browser/session retains full access
# ===========================================================================
def test_anonymous_creator_can_read_own_decision():
    client = app.test_client()
    did = _create_anonymous(client)
    r = client.get("/decision-workspace/%s" % did)
    assert r.status_code == 200


def test_anonymous_creator_can_mutate_own_decision():
    client = app.test_client()
    did = _create_anonymous(client)
    r = client.post("/decision-workspace/%s/preference" % did,
                     data={"action": "clear"})
    assert r.status_code == 302
    assert "/decision-workspace/%s" % did in r.headers["Location"]


def test_anonymous_creator_can_export_own_decision():
    client = app.test_client()
    did = _create_anonymous(client)
    r = client.get("/decision-workspace/%s/export" % did)
    assert r.status_code == 200
    assert r.mimetype == "application/json"


# ===========================================================================
# Anonymous foreign session: bare did possession is NOT sufficient
# ===========================================================================
def test_anonymous_foreign_session_cannot_read():
    owner_client = app.test_client()
    did = _create_anonymous(owner_client)
    foreign_client = app.test_client()          # different signed session
    r = foreign_client.get("/decision-workspace/%s" % did, follow_redirects=False)
    assert r.status_code == 302
    assert r.headers["Location"] == "/decision-workspace"


def test_anonymous_foreign_session_cannot_mutate():
    owner_client = app.test_client()
    did = _create_anonymous(owner_client)
    foreign_client = app.test_client()
    r = foreign_client.post("/decision-workspace/%s/preference" % did,
                             data={"action": "clear"}, follow_redirects=False)
    assert r.status_code == 302
    assert r.headers["Location"] == "/decision-workspace"


def test_anonymous_foreign_session_cannot_export():
    owner_client = app.test_client()
    did = _create_anonymous(owner_client)
    foreign_client = app.test_client()
    r = foreign_client.get("/decision-workspace/%s/export" % did,
                            follow_redirects=False)
    assert r.status_code == 302
    assert r.headers["Location"] == "/decision-workspace"


# ===========================================================================
# Authenticated owner: full access to their own decision
# ===========================================================================
def test_authenticated_owner_can_read(db_path):
    owner = _new_signed_in_client("owner-a@example.com")
    did = _create_owned(owner)
    r = owner.get("/decision-workspace/%s" % did)
    assert r.status_code == 200


def test_authenticated_owner_can_mutate(db_path):
    owner = _new_signed_in_client("owner-b@example.com")
    did = _create_owned(owner)
    r = owner.post("/decision-workspace/%s/preference" % did,
                    data={"action": "clear"}, follow_redirects=False)
    assert r.status_code == 302
    assert "/decision-workspace/%s" % did in r.headers["Location"]


def test_authenticated_owner_can_export(db_path):
    owner = _new_signed_in_client("owner-c@example.com")
    did = _create_owned(owner)
    r = owner.get("/decision-workspace/%s/export" % did)
    assert r.status_code == 200
    assert r.mimetype == "application/json"


# ===========================================================================
# Authenticated non-owner: denied on every surface
# ===========================================================================
def test_authenticated_non_owner_denied_read(db_path):
    owner = _new_signed_in_client("owner-d@example.com")
    did = _create_owned(owner)
    other = _new_signed_in_client("other-d@example.com")
    r = other.get("/decision-workspace/%s" % did, follow_redirects=False)
    assert r.status_code == 302
    assert r.headers["Location"] == "/decision-workspace"


def test_authenticated_non_owner_denied_mutation(db_path):
    owner = _new_signed_in_client("owner-e@example.com")
    did = _create_owned(owner)
    other = _new_signed_in_client("other-e@example.com")
    r = other.post("/decision-workspace/%s/preference" % did,
                    data={"action": "clear"}, follow_redirects=False)
    assert r.status_code == 302
    assert r.headers["Location"] == "/decision-workspace"


def test_authenticated_non_owner_denied_export(db_path):
    owner = _new_signed_in_client("owner-f@example.com")
    did = _create_owned(owner)
    other = _new_signed_in_client("other-f@example.com")
    r = other.get("/decision-workspace/%s/export" % did, follow_redirects=False)
    assert r.status_code == 302
    assert r.headers["Location"] == "/decision-workspace"


# ===========================================================================
# All mutation routes covered identically (not just one representative route)
# ===========================================================================
@pytest.mark.parametrize("suffix,payload", _DID_ROUTES_MUTATE)
def test_every_mutation_route_denies_foreign_anonymous_session(suffix, payload):
    owner_client = app.test_client()
    did = _create_anonymous(owner_client)
    foreign_client = app.test_client()
    r = foreign_client.post("/decision-workspace/%s/%s" % (did, suffix),
                             data=payload, follow_redirects=False)
    assert r.status_code == 302
    assert r.headers["Location"] == "/decision-workspace"


# ===========================================================================
# Non-enumeration: nonexistent vs. unauthorized-existing look identical
# ===========================================================================
def test_nonenumeration_nonexistent_and_unauthorized_denials_match():
    owner_client = app.test_client()
    did = _create_anonymous(owner_client)
    foreign_client = app.test_client()

    r_unauthorized = foreign_client.get("/decision-workspace/%s" % did,
                                         follow_redirects=False)
    r_nonexistent = foreign_client.get("/decision-workspace/does-not-exist",
                                        follow_redirects=False)

    assert r_unauthorized.status_code == r_nonexistent.status_code == 302
    assert (r_unauthorized.headers["Location"]
            == r_nonexistent.headers["Location"]
            == "/decision-workspace")


def test_nonenumeration_export_nonexistent_and_unauthorized_denials_match():
    owner_client = app.test_client()
    did = _create_anonymous(owner_client)
    foreign_client = app.test_client()

    r_unauthorized = foreign_client.get("/decision-workspace/%s/export" % did,
                                         follow_redirects=False)
    r_nonexistent = foreign_client.get(
        "/decision-workspace/does-not-exist/export", follow_redirects=False)

    assert r_unauthorized.status_code == r_nonexistent.status_code == 302
    assert (r_unauthorized.headers["Location"]
            == r_nonexistent.headers["Location"]
            == "/decision-workspace")


# ===========================================================================
# Regression: existing anonymous self-creator FDC-001 behaviour is preserved
# ===========================================================================
def test_regression_anonymous_self_creator_full_lifecycle_unaffected():
    """The pre-existing anonymous-flow behaviour (create -> view -> mutate ->
    export, all from the SAME browser) must remain functionally identical."""
    client = app.test_client()
    did = _create_anonymous(client)
    view = client.get("/decision-workspace/%s" % did)
    assert view.status_code == 200
    mutate = client.post("/decision-workspace/%s/preference" % did,
                          data={"action": "clear"}, follow_redirects=False)
    assert mutate.status_code == 302
    export = client.get("/decision-workspace/%s/export" % did)
    assert export.status_code == 200
