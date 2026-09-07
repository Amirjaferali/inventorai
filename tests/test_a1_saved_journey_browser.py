"""A1 real Chromium: recover a rejected answer, reopen and continue, EN/AR."""
import os
from pathlib import Path

import pytest

import web.app as webapp
from tests.test_draft_l2_local_continuity import server, page, _browser, _start, IDEA, ANSWER


def screenshot(page, name):
    target = os.environ.get("A1_BROWSER_EVIDENCE_DIR")
    if target:
        root = Path(target)
        root.mkdir(parents=True, exist_ok=True)
        page.screenshot(path=str(root / name), full_page=True)


@pytest.mark.parametrize("lang,width", [("en", 1280), ("ar", 360)])
def test_rejected_answer_recovers_then_saves_reopens_and_continues(server, page, lang, width):
    page.set_viewport_size({"width": width, "height": 900})
    if lang == "ar":
        page.goto(server)
        page.get_by_role("button", name="العربية", exact=True).click()
    sid = _start(page, server)
    assert page.locator("html").get_attribute("lang") == lang
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
    primary = page.locator('[data-primary-action]')
    assert primary.count() == 1
    assert IDEA in page.locator('.idea-excerpt').inner_text()
    assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'), page.evaluate("Array.from(document.querySelectorAll('body *')).filter(e => e.getBoundingClientRect().left < -1 || e.getBoundingClientRect().right > innerWidth+1).map(e=>[e.tagName,e.id,e.className,e.getBoundingClientRect().x,e.getBoundingClientRect().width]).slice(0,12)")
    primary.focus()
    primary.press("Enter")
    assert page.locator("#response").evaluate("e => e === document.activeElement")
    assert page.locator("#response").evaluate("e => getComputedStyle(e).outlineStyle") != "none"
    page.locator("#response").fill(ANSWER)
    page.wait_for_timeout(1000)  # existing local-draft debounce, no network save
    count_before = len(webapp.SESSION_STORE[sid]["state"].assertions)
    secret = page.locator('#answer-form input[name="csrf_token"]').input_value()
    page.locator('#answer-form input[name="csrf_token"]').evaluate("e => e.value = 'bad-token'")
    with page.expect_response(lambda r: r.url == server + '/session/' + sid and r.request.method == 'POST') as pending:
        page.locator('#answer-form button[type="submit"]').click()
    response = pending.value
    assert response.status == 403 and response.headers['cache-control'] == 'no-store'
    assert page.locator("html").get_attribute("lang") == lang
    assert page.locator("html").get_attribute("dir") == ("rtl" if lang == "ar" else "ltr")
    assert secret not in page.content() and ANSWER not in page.content()
    assert len(webapp.SESSION_STORE[sid]["state"].assertions) == count_before
    screenshot(page, 'csrf-recovery-' + lang + '.png')
    page.locator('#csrf-recovery').click()
    assert page.locator('#response').input_value() == ""
    page.locator('.draft-recovery .draft-restore').click()
    assert page.locator('#response').input_value() == ANSWER
    page.locator('#answer-form button[type="submit"]').click()
    page.wait_for_load_state()
    assert page.locator('#draft-signals').get_attribute('data-answer-accepted') == '1'
    assert page.locator('#journey-saved').is_visible()
    assert len(webapp.SESSION_STORE[sid]["state"].assertions) == count_before + 1
    assert secret not in page.evaluate('JSON.stringify(localStorage)')
    # Restart the transient view only; the real persisted project must reopen.
    webapp.SESSION_STORE.pop(sid)
    page.reload()
    assert page.locator('[data-primary-action]').count() == 1
    assert page.locator('#resume-project').is_visible()
    assert page.locator('#response').count() == 0
    assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'), page.evaluate("Array.from(document.querySelectorAll('body *')).filter(e => e.getBoundingClientRect().left < -1 || e.getBoundingClientRect().right > innerWidth+1).map(e=>[e.tagName,e.id,e.className,e.getBoundingClientRect().x,e.getBoundingClientRect().width]).slice(0,12)")
    screenshot(page, 'saved-cold-' + lang + '.png')
    page.locator('#resume-project').click()
    page.wait_for_load_state()
    assert page.locator('#response').count() == 1
    assert len(webapp.SESSION_STORE[sid]["state"].assertions) == count_before + 1
    screenshot(page, 'saved-continue-' + lang + '.png')


def test_pending_feedback_never_claims_save_and_does_not_change_native_form(server, page):
    _start(page, server)
    page.locator('#response').fill(ANSWER)
    # Observe the real submit handler without leaving the document. This test
    # interceptor runs after the application handler; it is not production code.
    page.evaluate("""() => {
      window.a1Hold = event => event.preventDefault();
      document.getElementById('answer-form').addEventListener('submit', window.a1Hold);
    }""")
    page.clock.install()
    page.locator('#answer-form button[type="submit"]').click()
    assert page.locator('#answer-form').get_attribute('aria-busy') == 'true', page.locator('#answer-form').inner_html()
    assert 'Saving is not confirmed yet' in page.locator('#answer-form p[role="status"]').inner_text()
    assert page.locator('#response').input_value() == ANSWER
    assert page.locator('#answer-form button[type="submit"]').is_enabled()
    assert page.locator('#answer-form').evaluate("e => new FormData(e).get('action')") == 'answered'
    page.clock.fast_forward(15000)
    assert 'Saving is not confirmed.' in page.locator('#answer-form p[role="status"]').inner_text()
    page.evaluate("document.getElementById('answer-form').removeEventListener('submit', window.a1Hold)")
    page.locator('#answer-form button[type="submit"]').click()
    page.wait_for_load_state()
    assert page.locator('#journey-saved').is_visible()


def test_no_javascript_keeps_native_answer_and_recovery_forms_usable(server, _browser):
    context = _browser.new_context(java_script_enabled=False, viewport={"width": 360, "height": 800})
    page = context.new_page()
    try:
        _start(page, server)
        assert page.locator('[data-primary-action]').get_attribute('href') == '#response'
        page.locator('#response').fill(ANSWER)
        page.locator('#answer-form button[type="submit"]').click()
        page.wait_for_load_state()
        assert page.locator('#journey-saved').is_visible()
    finally:
        context.close()


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_owned_project_card_keyboard_reopen_and_honest_export(server, page, lang):
    page.set_viewport_size({"width": 360, "height": 900})
    email, password = "a1-browser@example.com", "A1-browser-test-password"
    page.goto(server + "/register")
    page.locator('#email').fill(email)
    page.locator('#password').fill(password)
    page.locator('#password_confirm').fill(password)
    page.locator('main button[type="submit"]').click()
    page.wait_for_load_state()
    # Synthetic account only, development memory sink; no human/email provider.
    token = webapp._EMAIL_SENDER.last_for(email)['body'].rsplit(' ', 1)[-1]
    page.goto(server + '/verify/' + token)
    page.locator('main button[type="submit"]').click()
    page.wait_for_load_state()
    page.goto(server + '/login')
    page.locator('#email').fill(email)
    page.locator('#password').fill(password)
    page.locator('main button[type="submit"]').click()
    page.wait_for_url(server + '/account')
    if lang == "ar":
        page.get_by_role('button', name='العربية', exact=True).click()
    sid = _start(page, server)
    page.goto(server + '/account')
    card = page.locator('.project-card')
    assert card.count() == 1 and IDEA in card.inner_text()
    assert page.locator('html').get_attribute('lang') == lang
    assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')
    screenshot(page, 'project-list-' + lang + '.png')
    with page.expect_download() as download:
        card.locator('a[href$="/export"]').click()
    assert sid in download.value.suggested_filename
    # The existing minimized canonical export is unchanged and contains records,
    # not invented engineering/manufacturing/commercial validation.
    import json
    payload = json.loads(Path(download.value.path()).read_text())
    assert payload and 'PASS_WITH_CONDITIONS' not in json.dumps(payload)
    link = card.locator('a[href="/session/' + sid + '"]')
    link.focus()
    link.press('Enter')
    page.wait_for_url(server + '/session/' + sid)
    assert page.locator('[data-primary-action]').count() == 1


def test_unknown_and_correction_stay_reachable_without_promoting_evidence(server, page):
    sid = _start(page, server)
    page.locator('#response').fill(ANSWER)
    page.locator('#answer-form button[type="submit"]').click()
    page.wait_for_load_state()
    prior = webapp.SESSION_STORE[sid]['state'].assertions[-1]
    page.locator('details.correct-answer > summary').click()
    page.locator('#correct-response').fill('The relay opens because the comparator senses excess current; its trip threshold is still unknown.')
    page.locator('details.correct-answer button[type="submit"]').click()
    page.wait_for_load_state()
    records = webapp.SESSION_STORE[sid]['state'].assertions
    old = next(r for r in records if r.record_id == prior.record_id)
    assert old.content == ANSWER and old.superseded_by is not None
    page.locator('#response').fill('I do not know the threshold yet.')
    page.locator('input[name="action"][value="unknown"]').check()
    page.locator('#answer-form button[type="submit"]').click()
    page.wait_for_load_state()
    records = webapp.SESSION_STORE[sid]['state'].assertions
    assert records[-1].disposition == 'unknown'
    assert records[-1].content == 'I do not know the threshold yet.'
    assert page.locator('[data-primary-action]').count() == 1
