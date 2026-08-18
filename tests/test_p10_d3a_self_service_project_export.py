"""P10-D3a — Self-Service Project Export (RED/GREEN).

Behaviour-based tests for the bounded gate defined by
``docs/governance/P10_D3A_SELF_SERVICE_PROJECT_EXPORT_INCREMENT_CONTRACT.md``
(merged PR #510, authoritative).

One browser/session-authenticated, PROJECT-SCOPED export surface that consumes the
existing canonical seam ``engine.read_export_service.produce_project_export`` with
the identity from the existing ``_current_account()`` seam. No API credential, no
new export capability, no new authorization model, no persistence change.

Covered: owner success; anonymous / authenticated-non-owner / missing /
NULL-durable-owner denial; non-enumeration between missing and non-owned; exact
canonical-payload equality (no wrapper key, no API-v1 envelope); media type;
deterministic attachment header; fail-closed handling of an unexpected internal
failure; truthful project-scoped EN + AR labels; and the preservation of the
exactly-two-public-API-route contract.

Real on-disk SQLite (autouse conftest isolation); real signed Flask sessions; the
real record + account stores; the real seam. No mocks except one deliberate
post-authorization store failure injected via monkeypatch for the fail-closed test.
"""
import json
import os

import pytest

import web.app as webapp
from web.app import app
from engine import account_credentials as _acct
from engine import read_export_service as _seam

PW = "correct horse battery staple"
IDEA = ("An electronic circuit uses a sensor and a switch to cut the power when "
        "the current gets too high.")
FORM = {"idea": IDEA, "domain_confirm": "electronics_electrical"}

EXPORT_PATH = "/account/projects/{pid}/export"


@pytest.fixture
def db_path():
    return os.environ["INVENTORAI_DB_PATH"]


def _new_client():
    app.config["TESTING"] = True
    return app.test_client()


def _mk_account(email, verified=True, status="active"):
    store = webapp._get_account_store()
    aid = _acct.new_account_id()
    store.create_account(aid, _acct.normalize_email(email), _acct.hash_password(PW),
                         "2026-01-01T00:00:00.000000Z", status=status)
    if verified:
        store.mark_email_verified(aid, "2026-01-01T00:00:00.000000Z")
    return aid


def _client_for(email):
    """A fresh client signed in as a newly created, verified, active account."""
    aid = _mk_account(email)
    c = _new_client()
    r = c.post("/login", data={"email": email, "password": PW})
    assert r.status_code == 302, r.status_code
    return c, aid


def _start_project(client):
    r = client.post("/start", data=FORM)
    assert r.status_code == 302, r.status_code
    return r.headers["Location"].rsplit("/session/", 1)[-1]


def _export(client, pid):
    return client.get(EXPORT_PATH.format(pid=pid), follow_redirects=False)


def _denial_signature(response):
    """Everything a caller can observe about a denial, for non-enumeration
    comparison: status, Location, media type and body."""
    return (response.status_code, response.headers.get("Location"),
            response.headers.get("Content-Type"), response.data)


# ===========================================================================
# 1. Authenticated owner can export an owned project
# ===========================================================================
def test_authenticated_owner_can_export_owned_project(db_path):
    owner, aid = _client_for("d3a-owner@example.com")
    pid = _start_project(owner)
    assert webapp._get_store().load_owner(pid) == (True, aid)

    r = _export(owner, pid)
    assert r.status_code == 200, r.status_code


# ===========================================================================
# 2-5. Denial matrix
# ===========================================================================
def test_anonymous_caller_denied(db_path):
    owner, _aid = _client_for("d3a-anon-owner@example.com")
    pid = _start_project(owner)

    anon = _new_client()
    r = _export(anon, pid)
    assert r.status_code != 200
    assert b"idea_id" not in r.data


def test_authenticated_non_owner_denied(db_path):
    owner, _aid = _client_for("d3a-owner-b@example.com")
    pid = _start_project(owner)

    other, _other_aid = _client_for("d3a-other-b@example.com")
    r = _export(other, pid)
    assert r.status_code != 200
    assert b"idea_id" not in r.data


def test_missing_project_denied(db_path):
    caller, _aid = _client_for("d3a-missing@example.com")
    r = _export(caller, "no-such-project-id")
    assert r.status_code != 200
    assert b"idea_id" not in r.data


def test_null_durable_owner_project_denied(db_path):
    """An anonymous/legacy project carries a NULL durable owner. The canonical
    seam denies NULL-owner access (P7-I1 IR-5) and this surface inherits that
    STRICTER rule — it must not fall back to the more permissive browser
    capability helper, which would permit NULL-owner access."""
    anon = _new_client()
    pid = _start_project(anon)
    exists, owner = webapp._get_store().load_owner(pid)
    assert exists and owner is None, (exists, owner)

    caller, _aid = _client_for("d3a-null-owner@example.com")
    r = _export(caller, pid)
    assert r.status_code != 200
    assert b"idea_id" not in r.data


# ===========================================================================
# 6. Non-enumeration: missing vs. non-owned are indistinguishable
# ===========================================================================
def test_missing_and_non_owned_denials_are_indistinguishable(db_path):
    owner, _aid = _client_for("d3a-enum-owner@example.com")
    pid = _start_project(owner)

    other, _other_aid = _client_for("d3a-enum-other@example.com")
    r_non_owned = _export(other, pid)
    r_missing = _export(other, "definitely-not-a-real-project")

    assert _denial_signature(r_non_owned) == _denial_signature(r_missing)


def test_null_owner_denial_matches_missing_denial(db_path):
    anon = _new_client()
    null_pid = _start_project(anon)

    caller, _aid = _client_for("d3a-enum-null@example.com")
    r_null = _export(caller, null_pid)
    r_missing = _export(caller, "definitely-not-a-real-project")

    assert _denial_signature(r_null) == _denial_signature(r_missing)


# ===========================================================================
# 7. Parsed JSON equals the canonical seam output EXACTLY
# ===========================================================================
def test_parsed_json_equals_canonical_export_exactly(db_path):
    owner, aid = _client_for("d3a-canonical@example.com")
    pid = _start_project(owner)

    r = _export(owner, pid)
    assert r.status_code == 200
    body = json.loads(r.data)

    canonical = _seam.produce_project_export(webapp._get_store(), pid, aid)
    assert body == canonical, (sorted(body), sorted(canonical))
    # no wrapper key, no API-v1 envelope, no account enrichment
    assert set(body) == set(canonical)
    for forbidden in ("api_version", "export_contract_version", "export", "project",
                      "request_id", "account", "account_id", "email"):
        assert forbidden not in body, forbidden


# ===========================================================================
# 8-9. Media type and deterministic attachment behaviour
# ===========================================================================
def test_media_type_is_application_json(db_path):
    owner, _aid = _client_for("d3a-mimetype@example.com")
    pid = _start_project(owner)
    r = _export(owner, pid)
    assert r.status_code == 200
    assert r.mimetype == "application/json"


def test_attachment_header_is_deterministic_and_project_scoped(db_path):
    owner, _aid = _client_for("d3a-attach@example.com")
    pid = _start_project(owner)

    first = _export(owner, pid)
    second = _export(owner, pid)
    assert first.status_code == second.status_code == 200

    disposition = first.headers.get("Content-Disposition", "")
    assert disposition.startswith("attachment;"), disposition
    assert pid in disposition, disposition
    assert disposition == second.headers.get("Content-Disposition")


# ===========================================================================
# 10. No API credential is involved
# ===========================================================================
def test_no_api_credential_required_or_consulted(db_path):
    """The owner succeeds with a browser session alone, and no API credential
    row is created by exercising the route."""
    owner, _aid = _client_for("d3a-nocred@example.com")
    pid = _start_project(owner)

    store = webapp._get_account_store()
    before = store._conn.execute("SELECT COUNT(*) FROM api_credentials").fetchone()[0]
    r = _export(owner, pid)
    after = store._conn.execute("SELECT COUNT(*) FROM api_credentials").fetchone()[0]

    assert r.status_code == 200
    assert before == after == 0


# ===========================================================================
# 11. Unexpected internal failure fails closed
# ===========================================================================
def test_unexpected_internal_failure_fails_closed(db_path, monkeypatch):
    """A failure AFTER authorization succeeds must not leak internals and must
    not be served as a partial/empty success."""
    owner, aid = _client_for("d3a-failclosed@example.com")
    pid = _start_project(owner)
    real_store = webapp._get_store()

    class _BoomStore:
        """Authorizes exactly like the real store, then fails on the read."""

        def load_owner(self, project_id):
            return real_store.load_owner(project_id)

        def load_contract(self, project_id):
            raise RuntimeError(
                "SECRET-INTERNAL-DETAIL: SELECT * FROM projects WHERE x=1")

        def load_reconstruction_inputs(self, project_id):
            return real_store.load_reconstruction_inputs(project_id)

    monkeypatch.setattr(webapp, "_get_store", lambda: _BoomStore())

    r = _export(owner, pid)
    assert r.status_code != 200, r.status_code
    for leak in (b"SECRET-INTERNAL-DETAIL", b"Traceback", b"RuntimeError",
                 b"SELECT", b"load_contract"):
        assert leak not in r.data, leak
    # never a partial or empty payload served as success
    assert b"idea_id" not in r.data
    assert b"assertion_count" not in r.data


# ===========================================================================
# 12-13. Truthful, project-scoped user-facing label in EN and AR
# ===========================================================================
def _account_page(client, lang):
    r = client.post("/ui-language", data={"lang": lang})
    assert r.status_code == 302, r.status_code
    page = client.get("/account")
    assert page.status_code == 200, page.status_code
    return page.get_data(as_text=True)


_FORBIDDEN_LABEL_CONCEPTS_EN = (
    "export my data", "export account", "export all my data",
    "subject access", "subject-access", "data portability",
)
_FORBIDDEN_LABEL_CONCEPTS_AR = (
    "تصدير بياناتي",          # "export my data"
    "تصدير الحساب",           # "export account"
    "تصدير كل بياناتي",       # "export all my data"
)


def test_english_label_present_and_project_scoped(db_path):
    owner, _aid = _client_for("d3a-label-en@example.com")
    _start_project(owner)

    html = _account_page(owner, "en")
    assert "Export project" in html, "project-scoped English label missing"
    lowered = html.lower()
    for bad in _FORBIDDEN_LABEL_CONCEPTS_EN:
        assert bad not in lowered, bad


def test_arabic_label_present_and_project_scoped(db_path):
    owner, _aid = _client_for("d3a-label-ar@example.com")
    _start_project(owner)

    html = _account_page(owner, "ar")
    assert "تصدير" in html, "Arabic export label missing"
    assert "المشروع" in html, "Arabic label is not project-scoped"
    for bad in _FORBIDDEN_LABEL_CONCEPTS_AR:
        assert bad not in html, bad


def test_export_link_reaches_the_route(db_path):
    """The account page exposes the capability without URL guessing."""
    owner, _aid = _client_for("d3a-link@example.com")
    pid = _start_project(owner)
    html = _account_page(owner, "en")
    assert EXPORT_PATH.format(pid=pid) in html


# ===========================================================================
# 14. The public API route set is unchanged
# ===========================================================================
def test_public_api_route_set_unchanged():
    api_rules = {str(rule) for rule in app.url_map.iter_rules()
                 if str(rule).startswith("/api/")}
    assert api_rules == {"/api/v1/projects/<project_id>",
                         "/api/v1/projects/<project_id>/export"}


def test_new_route_is_outside_api_namespace_and_get_only():
    matching = [rule for rule in app.url_map.iter_rules()
                if "/projects/" in str(rule) and str(rule).endswith("/export")
                and not str(rule).startswith("/api/")]
    assert len(matching) == 1, [str(r) for r in matching]
    rule = matching[0]
    assert "draft" not in str(rule).lower()
    assert rule.methods - {"HEAD", "OPTIONS"} == {"GET"}


# ===========================================================================
# 15. The seam itself is untouched by this gate
# ===========================================================================
def test_seam_module_not_modified_by_this_gate():
    """P10-D3a consumes the seam; it does not re-implement or wrap its
    authorization. The canonical entry points keep their exact signatures."""
    import inspect
    sig = inspect.signature(_seam.produce_project_export)
    assert list(sig.parameters) == ["store", "project_id", "account_id"]
    assert issubclass(_seam.ProjectAccessDenied, Exception)
