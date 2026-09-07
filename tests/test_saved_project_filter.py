"""Saved-project filtering: real account rendering and the existing ownership seam."""
import html

import pytest
from flask import render_template, session

import web.app as webapp
from web.ui_text import text
from tests.csrf_client import csrf_client
from tests.test_a1_saved_journey import start
from tests.test_p5_3_project_ownership_authorization import _client_for, IDEA


def render_account(projects, lang="en"):
    """Render the actual template for browser presentation fixtures, not auth proof."""
    with webapp.app.test_request_context("/account"):
        session["ui_lang"] = lang
        return render_template(
            "account.html", account={"email_normalized": "synthetic@example.com",
                                     "email_verified": True},
            csrf_token="synthetic-csrf", notice=None, owned_projects=projects)


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_filter_markup_uses_existing_localization_and_progressive_enhancement(lang):
    body = render_account([{"id": "project-1", "idea": "Displayed description",
                            "domain": "mechanical", "unavailable": False}], lang)
    assert '<div id="project-filter" class="project-filter" hidden>' in body
    assert 'type="search" dir="auto" autocomplete="off" spellcheck="false"' in body
    assert 'type="button"' in body
    assert 'aria-controls="project-list"' in body
    assert 'role="status" aria-live="polite" aria-atomic="true"' in body
    assert '/static/js/project_filter.js' in body
    for suffix in ("SEARCH", "DOMAIN", "ALL_DOMAINS", "HELP", "CLEAR", "NO_MATCH"):
        value = text("UI_PROJECT_FILTER_" + suffix, lang)
        assert value and "UI_PROJECT_FILTER_" not in value
        assert html.escape(value, quote=False) in body
    assert text("UI_PROJECT_FILTER_COUNT", lang) in body
    if lang == "ar":
        assert '<html lang="ar" dir="rtl">' in body


@pytest.mark.parametrize("lang", ["en", "ar"])
@pytest.mark.parametrize("projects,key", [
    ([], "UI_A_ACCOUNT_008"), (None, "UI_A1_LIST_UNAVAILABLE")])
def test_empty_and_unavailable_never_become_filter_no_matches(projects, key, lang):
    body = render_account(projects, lang)
    assert html.escape(text(key, lang), quote=False) in body
    assert 'id="project-filter"' not in body
    assert '/static/js/project_filter.js' not in body
    assert 'id="project-filter-no-match"' not in body


def test_real_account_filter_source_is_owned_displayed_excerpt_only_and_read_only():
    owner = _client_for("filter-owner@example.com")
    other = _client_for("filter-other@example.com")
    seed = '<img src=x onerror="alert(1)"> ' + IDEA * 3 + " UNDISPLAYED_SECRET"
    sid = start(owner, seed)
    other_sid = start(other, "PRIVATE_OTHER " + IDEA)
    anonymous_sid = start(csrf_client(webapp.app), "PRIVATE_ANONYMOUS " + IDEA)
    before = webapp._get_store().load_contract(sid).to_json()
    webapp.SESSION_STORE.clear()
    response = owner.get("/account")
    body = response.get_data(as_text=True)
    excerpt = " ".join(seed.split())[:180] + "…"
    assert excerpt in html.unescape(body)
    assert "UNDISPLAYED_SECRET" not in body and '<img src=x' not in body
    assert sid in body and other_sid not in body and anonymous_sid not in body
    assert "PRIVATE_OTHER" not in body and "PRIVATE_ANONYMOUS" not in body
    assert f'href="/session/{sid}"' in body
    assert f'href="/account/projects/{sid}/export"' in body
    assert response.headers["Cache-Control"] == "no-store"
    assert webapp._get_store().load_contract(sid).to_json() == before
    assert not webapp.SESSION_STORE


def test_missing_description_does_not_index_an_invented_title():
    body = render_account([{"id": "missing-description", "idea": "", "domain": None,
                            "unavailable": True}])
    assert 'data-project-description' not in body
    assert '<bdi data-project-id>missing-description</bdi>' in body
    assert text("UI_A1_DETAILS_UNAVAILABLE", "en") in body
    assert 'href="/session/missing-description"' in body
