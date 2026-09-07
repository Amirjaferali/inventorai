"""Native report navigation in real Chromium; no production JavaScript.

The presentation matrix serves the real template under the real CSP with
explicit conditional-state fixtures. Separate live journeys below and adjacent
tests cover ownership, reconstruction and existing actions; fixtures do not
claim eligibility or human usability evidence.
"""
import copy
import os
from pathlib import Path

import pytest
from playwright.sync_api import expect

import web.app as webapp
from web.ui_text import text
from tests.test_increment_6_deliverable_redesign import render_navigation_case
from tests.test_draft_l2_local_continuity import server, page, _browser, _start, ANSWER

ORIGIN = 'http://report-navigation.test'
URL = ORIGIN + '/session/navigation-fixture/deliverable'
CASES = [('incomplete', False, False, False), ('eligible', True, False, False),
         ('cold', False, False, True), ('decision', False, True, False),
         ('eligible-decision', True, True, False)]


def serve_report(page, lang, eligible=False, capture=False, cold=False):
    body = render_navigation_case(lang, eligible, capture, cold)
    page.route(URL, lambda route: route.fulfill(
        body=body, content_type='text/html; charset=utf-8', headers=dict(webapp._SECURITY_HEADERS)))
    page.goto(URL)


@pytest.mark.parametrize('lang,width', [('en', 1280), ('en', 360), ('ar', 1280), ('ar', 360)])
@pytest.mark.parametrize('case,eligible,capture,cold', CASES)
def test_all_sections_native_keyboard_return_and_back_without_javascript(_browser, lang, width, case, eligible, capture, cold):
    context = _browser.new_context(java_script_enabled=False, viewport={'width': width, 'height': 800})
    page = context.new_page()
    try:
        serve_report(page, lang, eligible, capture, cold)
        assert page.locator('html').get_attribute('lang') == lang
        assert page.locator('html').get_attribute('dir') == ('rtl' if lang == 'ar' else None)
        nav = page.get_by_role('navigation', name=text('UI_REPORT_CONTENTS', lang), exact=True)
        links = nav.locator('a')
        assert links.count() == 7 + int(eligible) + int(capture)
        nav.focus()
        page.keyboard.press('Tab')
        expect(links.first).to_be_focused()
        assert links.first.evaluate('e => getComputedStyle(e).outlineStyle') != 'none'
        requests = []
        page.on('request', lambda request: requests.append(request.url))
        forms = page.locator('form').evaluate_all('els => els.map(e => e.outerHTML)')
        sections = page.locator('main > section').evaluate_all('els => els.map(e => e.textContent)')
        for i in range(links.count()):
            link = links.nth(i)
            href = link.get_attribute('href')
            target = page.locator(href)
            assert target.count() == 1
            assert link.text_content() == target.text_content()
            link.focus()
            link.press('Enter')
            expect(page).to_have_url(URL + href)
            expect(target).to_be_focused()
            assert target.evaluate('e => getComputedStyle(e).outlineStyle') != 'none'
            assert target.evaluate('e => { const r=e.getBoundingClientRect(); return r.top >= 0 && r.top < innerHeight; }')
            section = target.locator('..')
            expect(section).to_be_visible()
            back = section.get_by_role('link', name=text('UI_REPORT_BACK_CONTENTS', lang), exact=True)
            back.focus()
            back.press('Enter')
            expect(page).to_have_url(URL + '#report-contents')
            expect(nav).to_be_focused()
            assert nav.evaluate('e => { const r=e.getBoundingClientRect(); return r.left >= 0 && r.right <= innerWidth; }')
            assert nav.evaluate('e => e.scrollWidth <= e.clientWidth')
        # Browser Back follows fragment history without requesting/re-rendering the report.
        last_href = links.last.get_attribute('href')
        page.go_back()
        expect(page).to_have_url(URL + last_href)
        expect(page.locator(last_href)).to_be_visible()
        assert requests == []
        assert page.locator('form').evaluate_all('els => els.map(e => e.outerHTML)') == forms
        assert page.locator('main > section').evaluate_all('els => els.map(e => e.textContent)') == sections
        assert page.locator('main > section[hidden], main > section details').count() == 0
        assert page.locator('.decision-primary').count() == int(eligible)
        assert page.locator('form[action$="/keep-snapshot"]').count() == int(eligible)
        assert page.locator('script').count() == 0
        if capture:
            assert page.locator('.w2a-decisions img').count() == 0
        evidence = os.environ.get('REPORT_NAVIGATION_EVIDENCE_DIR')
        if evidence and case == 'eligible-decision':
            target_dir = Path(evidence)
            target_dir.mkdir(parents=True, exist_ok=True)
            nav.screenshot(path=str(target_dir / f'report-contents-{lang}-{width}.png'))
    finally:
        context.close()


@pytest.mark.parametrize('lang', ['en', 'ar'])
def test_navigation_creates_no_requests_storage_writes_or_form_events(page, lang):
    page.add_init_script("""(() => {
      window.navWrites = [];
      for (const name of ['setItem', 'removeItem', 'clear']) {
        Storage.prototype[name] = function () { window.navWrites.push(name); };
      }
      window.navSubmits = 0;
      document.addEventListener('submit', () => window.navSubmits++);
    })();""")
    serve_report(page, lang, eligible=True, capture=True)
    before = page.evaluate('JSON.stringify([document.cookie, {...localStorage}, {...sessionStorage}])')
    requests = []
    page.on('request', lambda request: requests.append(request.url))
    for link in page.locator('#report-contents a').all():
        link.click()
    page.locator('.report-return a').last.click()
    page.wait_for_timeout(150)
    assert requests == [] and page.evaluate('navWrites') == [] and page.evaluate('navSubmits') == 0
    assert page.evaluate('JSON.stringify([document.cookie, {...localStorage}, {...sessionStorage}])') == before


@pytest.mark.parametrize('lang', ['en', 'ar'])
def test_live_and_cold_report_navigation_keeps_session_and_return_journey(server, page, lang):
    if lang == 'ar':
        page.goto(server)
        page.get_by_role('button', name='العربية', exact=True).click()
    sid = _start(page, server)
    page.locator('#response').fill(ANSWER)
    page.locator('#answer-form button[type="submit"]').click()
    page.wait_for_load_state()
    for cold in (False, True):
        if cold:
            webapp.SESSION_STORE.pop(sid)
        response = page.goto(server + f'/session/{sid}/deliverable')
        assert response.status == 200
        assert response.headers['cache-control'] == 'no-store'
        assert page.locator('#reconstructed-deliverable').count() == int(cold)
        before = copy.deepcopy(webapp.SESSION_STORE[sid]['state'].__dict__)
        requests = []
        listener = lambda request: requests.append(request.url)
        page.on('request', listener)
        page.locator('#report-contents a[href="#report-unknowns"]').click()
        expect(page.locator('#report-unknowns')).to_be_focused()
        page.locator('#report-unknowns').locator('..').locator('.report-return a').click()
        assert requests == []
        assert webapp.SESSION_STORE[sid]['state'].__dict__ == before
        page.remove_listener('request', listener)
    # The existing return action still reaches this project's read-only/resume view.
    page.locator('.back-link a').click()
    expect(page).to_have_url(server + '/session/' + sid)
    expect(page.locator('#resume-project')).to_be_visible()
