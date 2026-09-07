"""Real Chromium over the real template/script; synthetic presentation fixtures.

The separate server tests prove ownership and durable-read isolation. Browser
fixtures intentionally include missing metadata and mixed visible domains without
creating product records, changing domain activation or performing human activity.
"""
from pathlib import Path

import pytest
from playwright.sync_api import expect

import web.app as webapp
from web.ui_text import text
from tests.test_draft_l2_local_continuity import _browser, page
from tests.test_saved_project_filter import render_account

ORIGIN = "http://filter.test"
SCRIPT = Path(__file__).resolve().parents[1] / "web/static/js/project_filter.js"
CARDS = [
    {"id": "sensor-001", "idea": 'Sensor [A+B].* <img src=x onerror="alert(1)"> ' + "x" * 125 + "…",
     "domain": "electronics_electrical", "unavailable": False},
    {"id": "pump-002", "idea": "مضخة مياه ذات ذراع ميكانيكية", "domain": "mechanical", "unavailable": False},
    {"id": "pump-003", "idea": "مضخة Sensor للتحكم في المياه", "domain": "electronics_electrical", "unavailable": False},
    {"id": "fallback-004", "idea": "", "domain": None, "unavailable": True},
    {"id": "alpha-005", "idea": "Casefold ALPHA " + "ق" * 160 + "…", "domain": "mechanical", "unavailable": False},
]


def load_page(page, lang, cards=CARDS, block_script=False):
    body = render_account(cards, lang)
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))

    def serve(route):
        if route.request.url == ORIGIN + "/account":
            route.fulfill(body=body, content_type="text/html; charset=utf-8",
                          headers=dict(webapp._SECURITY_HEADERS))
        elif route.request.url == ORIGIN + "/static/js/project_filter.js" and not block_script:
            route.fulfill(body=SCRIPT.read_text(encoding="utf-8"),
                          content_type="application/javascript; charset=utf-8")
        else:
            route.abort()

    page.route(ORIGIN + "/**", serve)
    page.goto(ORIGIN + "/account")
    return errors


def visible_ids(page):
    return page.locator('.project-card:not([hidden]) [data-project-id]').all_text_contents()


@pytest.mark.parametrize("lang", ["en", "ar"])
@pytest.mark.parametrize("width", [360, 1280])
def test_literal_filters_domains_reset_and_accessible_mobile_layout(page, lang, width):
    page.set_viewport_size({"width": width, "height": 900})
    errors = load_page(page, lang)
    expect(page.locator('#project-filter')).to_be_visible()
    assert page.locator('html').get_attribute('lang') == lang
    if lang == "ar":
        assert page.locator('html').get_attribute('dir') == 'rtl'
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    query = page.get_by_label(text("UI_PROJECT_FILTER_SEARCH", lang), exact=True)
    domain = page.get_by_label(text("UI_PROJECT_FILTER_DOMAIN", lang), exact=True)
    initial_links = page.locator('.project-card a').evaluate_all('els => els.map(e => e.getAttribute("href"))')
    assert visible_ids(page) == [c['id'] for c in CARDS]
    expect(page.get_by_role('status')).to_have_text(text("UI_PROJECT_FILTER_COUNT", lang).replace('{shown}', '5').replace('{total}', '5'))
    query.fill('  sEnSoR  ')
    assert visible_ids(page) == ['sensor-001', 'pump-003']
    query.fill('مضخة')
    assert visible_ids(page) == ['pump-002', 'pump-003']
    electrical = page.locator('[data-project-domain]').first.text_content().strip()
    mechanical = page.locator('[data-project-domain]').nth(1).text_content().strip()
    unknown = page.locator('[data-project-domain]').nth(3).text_content().strip()
    assert page.locator('#project-filter-domain option').all_text_contents() == [
        text('UI_PROJECT_FILTER_ALL_DOMAINS', lang), electrical, mechanical, unknown]
    domain.select_option(label=electrical)
    assert visible_ids(page) == ['pump-003']
    domain.select_option(label=mechanical)
    assert visible_ids(page) == ['pump-002']
    query.fill('sensor-001')
    assert visible_ids(page) == []
    expect(page.locator('#project-filter-no-match')).to_be_visible()
    expect(page.get_by_role('status')).to_have_text(text("UI_PROJECT_FILTER_COUNT", lang).replace('{shown}', '0').replace('{total}', '5'))
    clear = page.get_by_role('button', name=text('UI_PROJECT_FILTER_CLEAR', lang), exact=True)
    clear.focus()
    clear.press('Enter')
    expect(query).to_be_focused()
    assert query.evaluate('e => getComputedStyle(e).outlineStyle') != 'none'
    expect(query).to_have_value('')
    expect(domain).to_have_value('')
    assert visible_ids(page) == [c['id'] for c in CARDS]
    expect(page.locator('#project-filter-no-match')).to_be_hidden()
    query.press('Tab')
    expect(domain).to_be_focused()
    domain.press('Tab')
    expect(clear).to_be_focused()
    clear.press('Tab')
    expect(page.locator('.project-card a').first).to_be_focused()
    assert page.locator('.project-card a').evaluate_all('els => els.map(e => e.getAttribute("href"))') == initial_links
    assert not errors


@pytest.mark.parametrize('lang', ['en', 'ar'])
def test_special_characters_are_literal_and_filtering_is_network_and_storage_free(page, lang):
    page.add_init_script("""(() => {
      window.filterStorageCalls = [];
      for (const name of ['setItem', 'removeItem', 'clear']) {
        Storage.prototype[name] = function () {
          window.filterStorageCalls.push(name);
          throw new Error('Filtering must not write browser storage');
        };
      }
    })();""")
    errors = load_page(page, lang)
    requests = []
    page.on('request', lambda request: requests.append(request.url))
    before = page.evaluate('JSON.stringify([document.cookie, {...localStorage}, {...sessionStorage}])')
    query = page.locator('#project-filter-query')
    for needle in ['[A+B]', '.*', '<img src=x onerror="alert(1)">']:
        query.fill(needle)
        assert visible_ids(page) == ['sensor-001']
        assert page.locator('.project-card img').count() == 0
    query.fill('^.*$')
    assert visible_ids(page) == []  # no regular-expression interpretation
    query.fill('fallback-004')
    assert visible_ids(page) == ['fallback-004']
    unknown = page.locator('[data-project-domain]').nth(3).text_content().strip()
    page.locator('#project-filter-domain').select_option(label=unknown)
    assert visible_ids(page) == ['fallback-004']
    query.fill('x' * 124)
    assert visible_ids(page) == []  # existing domain selection still applies
    page.locator('#project-filter-domain').select_option('')
    assert visible_ids(page) == ['sensor-001']
    query.fill('UNDISPLAYED_SECRET')
    assert visible_ids(page) == []
    query.fill('a' * 4000)
    assert visible_ids(page) == []
    page.locator('#project-filter-clear').click()
    query.press('Enter')
    page.wait_for_timeout(100)  # observe any asynchronously generated request
    assert page.url == ORIGIN + '/account'
    assert requests == []
    assert page.evaluate('filterStorageCalls') == []
    assert page.evaluate('JSON.stringify([document.cookie, {...localStorage}, {...sessionStorage}])') == before
    assert not errors


@pytest.mark.parametrize('lang', ['en', 'ar'])
@pytest.mark.parametrize('cards,key', [([], 'UI_A_ACCOUNT_008'), (None, 'UI_A1_LIST_UNAVAILABLE')])
def test_empty_and_unavailable_browser_states(page, lang, cards, key):
    errors = load_page(page, lang, cards)
    expect(page.get_by_text(text(key, lang), exact=True)).to_be_visible()
    assert page.locator('#project-filter').count() == 0
    assert page.locator('.project-card').count() == 0
    if cards is None:
        assert page.get_by_role('link', name=text('UI_A1_RETRY_LIST', lang)).get_attribute('href') == '/account'
    assert not errors


@pytest.mark.parametrize('lang', ['en', 'ar'])
@pytest.mark.parametrize('javascript', [False, True])
def test_no_javascript_or_failed_script_preserves_all_cards_and_links(_browser, lang, javascript):
    context = _browser.new_context(java_script_enabled=javascript, viewport={"width": 360, "height": 900})
    page = context.new_page()
    try:
        errors = load_page(page, lang, block_script=True)
        expect(page.locator('#project-filter')).to_be_hidden()
        assert visible_ids(page) == [c['id'] for c in CARDS]
        for index, card in enumerate(CARDS):
            links = page.locator('.project-card').nth(index).locator('a')
            assert links.nth(0).get_attribute('href') == '/session/' + card['id']
            assert links.nth(1).get_attribute('href') == '/account/projects/' + card['id'] + '/export'
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        assert not errors
    finally:
        context.close()
