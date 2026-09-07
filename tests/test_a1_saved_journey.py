"""A1 identity/recovery projections preserve accepted persistence and security."""
import copy
import html
import re

import pytest

import web.app as webapp
from engine.record_store import StoreError
from tests.csrf_client import csrf_client
from tests.test_p5_3_project_ownership_authorization import _client_for, IDEA


def start(client, idea=IDEA):
    response = client.post("/start", data={"idea": idea, "domain_confirm": "electronics_electrical"})
    assert response.status_code == 302
    return response.location.rsplit("/", 1)[-1]


def get(client, sid):
    return client.get("/session/" + sid).get_data(as_text=True)


def answer_token(body):
    return html.unescape(re.search(r'name="answer_token" value="([^"]+)"', body).group(1))


def canonical(sid):
    entry = webapp.SESSION_STORE[sid]
    return (webapp._get_store().load_contract(sid).to_json(),
            copy.deepcopy(entry["state"]), copy.deepcopy(entry.get("transcript")),
            copy.deepcopy(entry.get("last_result")))


def test_project_cards_use_only_durable_owned_original_data_and_escape_html():
    owner = _client_for("a1-owner@example.com")
    other = _client_for("a1-other@example.com")
    hostile = "<img src=x onerror=alert(1)> " + IDEA
    own_id = start(owner, hostile)
    other_id = start(other, "PRIVATE OTHER IDEA " + IDEA)
    anon_id = start(csrf_client(webapp.app), "PRIVATE ANON IDEA " + IDEA)
    before = webapp._get_store().load_contract(own_id).to_json()
    # Cold list: no reliance on another transient view or generated title.
    webapp.SESSION_STORE.clear()
    response = owner.get("/account")
    body = response.get_data(as_text=True)
    assert own_id in body and html.escape(hostile, quote=False) in body
    assert "<img src=x" not in body
    assert other_id not in body and anon_id not in body
    assert "PRIVATE OTHER IDEA" not in body and "PRIVATE ANON IDEA" not in body
    assert "not independently verified findings" in body
    assert response.headers["Cache-Control"] == "no-store"
    assert webapp._get_store().load_contract(own_id).to_json() == before
    assert not webapp.SESSION_STORE


def test_list_failure_is_not_reported_as_empty_or_deleted(monkeypatch):
    owner = _client_for("a1-list@example.com")
    start(owner)
    def unavailable(*args):
        raise StoreError("private database details")
    monkeypatch.setattr(webapp._get_store(), "project_ids_for_owner", unavailable)
    body = owner.get("/account").get_data(as_text=True)
    assert "could not be loaded" in body and "does not mean" in body
    assert 'href="/account"' in body and "private database details" not in body
    assert 'class="project-list"' not in body


def test_metadata_unavailable_still_offers_owned_project_without_invented_title(monkeypatch):
    owner = _client_for("a1-meta@example.com")
    sid = start(owner)
    def unavailable(*args):
        raise StoreError("private reconstruction details")
    monkeypatch.setattr(webapp._get_store(), "load_reconstruction_inputs", unavailable)
    body = owner.get("/account").get_data(as_text=True)
    assert '/session/' + sid in body and "Project details could not be loaded" in body
    assert IDEA not in body and "private reconstruction details" not in body


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_live_and_cold_orientation_use_existing_continuation_without_writes(lang):
    client = _client_for("a1-cold@example.com")
    sid = start(client)
    if lang == "ar":
        client.post("/ui-language", data={"lang": "ar", "next": "/account"})
    body = get(client, sid)
    assert body.count("data-primary-action") == 1
    assert 'href="#response"' in body
    assert IDEA in body and 'dir="auto"' in body
    assert '/account' in body
    before = webapp._get_store().load_contract(sid).to_json()
    webapp.SESSION_STORE.pop(sid)
    body = get(client, sid)
    assert body.count("data-primary-action") == 1
    assert 'id="resume-project"' in body and 'name="response"' not in body
    assert webapp._get_store().load_contract(sid).to_json() == before
    assert getattr(webapp.SESSION_STORE[sid]["state"], "domain", None) is None
    assert client.post('/session/' + sid + '/resume', data={}).status_code == 302
    assert 'href="#response"' in get(client, sid)
    assert webapp._get_store().load_contract(sid).to_json() == before
    if lang == "ar":
        assert '<html lang="ar" dir="rtl">' in body


@pytest.mark.parametrize("storage_failure", [False, True])
def test_f04_head_cannot_consume_failed_post_feedback_or_accept_the_answer(monkeypatch, storage_failure):
    client = csrf_client(webapp.app)
    sid = start(client)
    token = answer_token(get(client, sid))
    before = canonical(sid)
    if storage_failure:
        def fail(*args, **kwargs):
            raise StoreError("synthetic durable append failure")
        monkeypatch.setattr(webapp._get_store(), "append_record", fail)
    response = client.post('/session/' + sid, data={
        "action": "answered", "response": "An attempted answer." if storage_failure else "  ",
        "answer_token": token})
    expected = webapp.ANSWER_NOT_SAVED_MESSAGE if storage_failure else webapp.ANSWER_REQUIRED_MESSAGE
    assert response.status_code == 302
    assert webapp.SESSION_STORE[sid]["_answer_error"] == expected
    for _ in range(2):
        head = client.head(response.location)
        assert head.status_code == 200 and head.data == b""
        assert webapp.SESSION_STORE[sid]["_answer_error"] == expected
    body = get(client, sid)
    assert expected in html.unescape(body) and 'id="answer-error"' in body
    assert 'id="journey-saved"' not in body
    assert webapp.SESSION_STORE[sid]["answer_token"] == token
    assert canonical(sid) == before
    assert 'id="answer-error"' not in get(client, sid)  # ordinary one-shot GET retained


def test_head_preserves_real_durable_success_feedback():
    client = csrf_client(webapp.app)
    sid = start(client)
    client.head('/session/' + sid)
    assert 'id="journey-saved"' in get(client, sid)
    token = answer_token(get(client, sid))
    response = client.post('/session/' + sid, data={
        "action": "answered", "response": "The sensor detects excess current and opens the relay because overheating is dangerous.",
        "answer_token": token})
    assert response.status_code == 302
    assert webapp.SESSION_STORE[sid].get("_answer_accepted")
    client.head(response.location)
    assert "Your answer was saved" in get(client, sid)
    assert 'id="journey-saved"' not in get(client, sid)


@pytest.mark.parametrize("path,target", [
    ("/start", "/"), ("/login", "/login"), ("/register", "/register"),
    ("/account/deactivate", "/account"), ("/recover", "/recover"),
    ("/reset/secret-mail-token", "/recover"), ("/verify/secret-mail-token", "/account"),
    ("/decision-workspace", "/decision-workspace"),
    ("/decision-workspace/existing/constraint", "/decision-workspace/existing"),
    ("/session/existing/correct", "/session/existing"),
])
def test_r05_n1_get_recovery_never_reflects_form_tokens_or_untrusted_redirect(path, target):
    client = webapp.app.test_client()  # raw missing-CSRF request, never the helper
    with client.session_transaction() as session:
        session["ui_lang"] = "ar"
    response = client.post(path + '?next=//evil.example', data={
        "next": "https://evil.example", "response": "PRIVATE REJECTED TEXT", "csrf_token": "rejected-secret"},
        headers={"Referer": "https://evil.example/"})
    body = response.get_data(as_text=True)
    assert response.status_code == 403
    assert response.headers["Cache-Control"] == "no-store"
    assert '<html lang="ar" dir="rtl">' in body
    assert f'id="csrf-recovery" href="{target}"' in body
    assert '<form' not in body and 'name="csrf_token"' not in body
    assert all(secret not in body for secret in ["secret-mail-token", "rejected-secret", "evil.example", "PRIVATE REJECTED TEXT"])
    if path.startswith(("/reset/", "/verify/")):
        assert response.headers["Referrer-Policy"] == "no-referrer"
    with client.session_transaction() as session:
        assert dict(session) == {"ui_lang": "ar"}


@pytest.mark.parametrize("path,target", [
    ("/session/existing/success-criteria", "/session/existing/success-criteria"),
    ("/session/existing/keep-snapshot", "/session/existing/deliverable"),
])
@pytest.mark.parametrize("lang,direction", [("en", "ltr"), ("ar", "rtl")])
@pytest.mark.parametrize("data", [{}, {"csrf_token": "rejected-secret"}])
def test_r05_n1_specific_form_recovery_rejects_before_protected_access(
        monkeypatch, path, target, lang, direction, data):
    client = webapp.app.test_client()  # raw request; no CSRF helper or GET setup
    with client.session_transaction() as session:
        session["ui_lang"] = lang

    def forbidden_access(*args, **kwargs):
        pytest.fail("CSRF rejection reached protected store/account/view code")

    for name in ("_get_store", "_get_account_store", "_current_account"):
        monkeypatch.setattr(webapp, name, forbidden_access)
    for endpoint in ("save_success_criteria", "keep_snapshot"):
        monkeypatch.setitem(webapp.app.view_functions, endpoint, forbidden_access)

    response = client.post(path, data=data)
    body = response.get_data(as_text=True)
    assert response.status_code == 403
    assert response.headers["Cache-Control"] == "no-store"
    assert "Set-Cookie" not in response.headers
    assert f'<html lang="{lang}" dir="{direction}">' in body
    assert f'id="csrf-recovery" href="{target}"' in body
    assert '<form' not in body and 'name="csrf_token"' not in body
    assert "rejected-secret" not in body
    with client.session_transaction() as session:
        assert dict(session) == {"ui_lang": lang}


def test_unavailable_cold_reconstruction_has_no_dead_form_or_false_completion(monkeypatch):
    client = csrf_client(webapp.app)
    sid = start(client)
    get(client, sid)
    before = webapp._get_store().load_contract(sid).to_json()
    webapp.SESSION_STORE.pop(sid)
    def unavailable(*args):
        raise StoreError("reconstruction unavailable")
    monkeypatch.setattr(webapp, "reconstruct_review_state", unavailable)
    body = get(client, sid)
    assert body.count("data-primary-action") == 1
    assert 'name="response"' not in body and 'id="resume-project"' not in body
    assert 'class="complete"' not in body
    assert "Saved view" in body
    assert webapp._get_store().load_contract(sid).to_json() == before
