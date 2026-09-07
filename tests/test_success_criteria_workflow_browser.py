"""Native criterion workflow: presentation probes plus real route/save journeys.

Synthetic render cases do not claim engine eligibility. Live journeys use the
existing isolated DB and single-thread server fixture; no production JS is added.
"""
import copy
import os
from pathlib import Path
from urllib.parse import parse_qs

import pytest
from playwright.sync_api import expect

from engine.idea_state import SuccessCriterion
from tests.test_draft_l2_local_continuity import server, _browser
from tests.test_increment_6_deliverable_redesign import render_criteria_workflow_case
from tests.test_success_criteria import _seed, _ids
from web.ui_text import text


@pytest.mark.parametrize('lang,width', [('en', 1280), ('ar', 1280), ('en', 360), ('ar', 360)])
def test_context_native_accessibility_and_exact_text_without_javascript(_browser, lang, width):
    sid, items, report, criteria = render_criteria_workflow_case(lang, reverse=True)
    origin = 'http://criteria-workflow.test'
    report_url = origin + f'/session/{sid}/deliverable'
    form_url = origin + f'/session/{sid}/success-criteria'
    context = _browser.new_context(java_script_enabled=False, viewport={'width': width, 'height': 800})
    page = context.new_page()
    try:
        page.route(report_url, lambda route: route.fulfill(body=report, content_type='text/html'))
        page.route(form_url, lambda route: route.fulfill(body=criteria, content_type='text/html'))
        page.goto(report_url)
        links = page.locator('.experiment-criterion-link a')
        for index, item in enumerate(items):
            links.nth(index).focus()
            links.nth(index).press('Enter')
            target = page.locator('[name="criterion__' + item['experiment_id'] + '"]')
            expect(target).to_be_focused()
            assert 'acknowledged_unknown' not in page.url
            assert page.url.endswith('#' + target.get_attribute('id'))
            assert page.locator('html').get_attribute('lang') == lang
            assert page.locator('html').get_attribute('dir') == ('rtl' if lang == 'ar' else None)
            card = target.locator('..')
            details = card.locator('details')
            summary = details.locator('summary')
            assert details.get_attribute('open') is None
            target.fill('Not submitted غير مرسل')
            summary.focus()
            assert summary.evaluate('e => getComputedStyle(e).outlineStyle') != 'none'
            summary.press('Enter')
            assert details.get_attribute('open') is not None
            assert details.locator('dd').all_text_contents() == [item[key] for key in (
                'objective', 'minimum_prototype', 'what_to_observe', 'failure_or_revision_condition')]
            assert details.locator('img,script').count() == 0
            for ref in summary.get_attribute('aria-describedby').split():
                assert page.locator('#' + ref).count() == 1
            for ref in target.get_attribute('aria-describedby').split():
                expect(page.locator('#' + ref)).to_be_visible()
            page.keyboard.press('Tab')
            expect(target).to_be_focused()
            assert target.evaluate('e => getComputedStyle(e).outlineStyle') != 'none'
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
            assert details.evaluate('e => e.scrollWidth <= e.clientWidth')
            evidence = os.environ.get('CRITERIA_WORKFLOW_EVIDENCE_DIR')
            if evidence and index == 0:
                Path(evidence).mkdir(parents=True, exist_ok=True)
                card.screenshot(path=str(Path(evidence) / f'criteria-{lang}-{width}.png'))
            summary.focus()
            summary.press('Space')
            assert details.get_attribute('open') is None
            expect(target).to_have_value('Not submitted غير مرسل')
            page.go_back()
            expect(page).to_have_url(report_url)
        assert page.locator('script').count() == 0
    finally:
        context.close()


@pytest.mark.parametrize('lang', ['en', 'ar'])
@pytest.mark.parametrize('javascript', [False, True])
def test_live_navigation_toggle_and_save_clear_preserve_semantics(server, _browser, lang, javascript):
    sid, state = _seed()
    ids = _ids(state)
    for i, eid in enumerate(ids):
        state.success_criteria[eid] = SuccessCriterion(f'existing {i} العربية <tag>')
    before = copy.deepcopy(state.__dict__)
    context = _browser.new_context(java_script_enabled=javascript)
    if javascript:
        context.add_init_script("""(() => {
          window.storageCalls = [];
          for (const name of ['getItem','setItem','removeItem','clear']) {
            const original = Storage.prototype[name];
            Storage.prototype[name] = function(...args) {
              window.storageCalls.push(name); return original.apply(this, args);
            };
          }
        })();""")
    page = context.new_page()
    try:
        report_url = server + f'/session/{sid}/deliverable'
        page.goto(report_url)
        if lang == 'ar':
            page.get_by_role('button', name='العربية', exact=True).click()
        link = page.locator('.experiment-criterion-link a').nth(1)
        requests = []
        page.on('request', lambda req: requests.append((req.method, req.url, req.post_data)))
        link.click()
        target = page.locator('[name="criterion__' + ids[1] + '"]')
        expect(target).to_be_focused()
        assert [(method, url) for method, url, _ in requests] == [
            ('GET', server + f'/session/{sid}/success-criteria')]
        assert page.locator('script').count() == 0
        assert text('UI_SC_SAVE_CLEAR', lang) in target.locator('..').inner_text()
        assert target.get_attribute('maxlength') == '1000'
        form = page.locator('form[action$="/success-criteria"]')
        assert form.locator('input,textarea,select').evaluate_all('els => els.map(e => e.name)') == [
            'csrf_token', *['criterion__' + eid for eid in ids]]
        target.fill('  Revised target هدف معدّل\nwith  spaces <tag>  ')
        page.locator('[name="criterion__' + ids[0] + '"]').fill('   ')
        values = form.locator('textarea').evaluate_all('els => els.map(e => e.value)')
        requests.clear()
        for summary in page.locator('.experiment-context summary').all():
            summary.focus()
            summary.press('Enter')
            summary.press('Space')
        assert requests == []
        assert form.locator('textarea').evaluate_all('els => els.map(e => e.value)') == values
        assert state.__dict__ == before
        if javascript:
            assert page.evaluate('storageCalls') == []
        form.get_by_role('button', name=text('UI_B_SC_004', lang), exact=True).click()
        expect(page).to_have_url(report_url)
        posts = [parse_qs(data, keep_blank_values=True) for method, _, data in requests if method == 'POST']
        assert len(posts) == 1
        assert set(posts[0]) == {'csrf_token', *['criterion__' + eid for eid in ids]}
        assert ids[0] not in state.success_criteria
        # Native HTML form encoding normalizes textarea LF to CRLF; the route
        # trims only the submitted value and preserves its internal whitespace.
        submitted = posts[0]['criterion__' + ids[1]][0]
        assert submitted == values[1].replace('\n', '\r\n')
        assert state.success_criteria[ids[1]].criterion == submitted.strip()
        assert state.success_criteria[ids[2]].criterion == before['success_criteria'][ids[2]].criterion
        assert {k: v for k, v in state.__dict__.items() if k != 'success_criteria'} == {
            k: v for k, v in before.items() if k != 'success_criteria'}
    finally:
        context.close()


@pytest.mark.parametrize('lang', ['en', 'ar'])
def test_stale_fragment_leaves_current_form_usable_without_javascript(server, _browser, lang):
    sid, state = _seed()
    old_id = _ids(state)[0]
    context = _browser.new_context(java_script_enabled=False)
    page = context.new_page()
    try:
        page.goto(server + f'/session/{sid}/deliverable')
        if lang == 'ar':
            page.get_by_role('button', name='العربية', exact=True).click()
        state.acknowledged_unknowns.clear()
        old_target = 'criterion-' + old_id.rsplit('_', 1)[-1]
        link = page.locator(f'.experiment-criterion-link a[href$="#{old_target}"]')
        link.click()
        assert page.locator('#' + old_target).count() == 0
        assert page.locator('textarea:focus').count() == 0
        assert page.locator('textarea').count() == len(_ids(state))
        expect(page.locator('form[action$="/success-criteria"] button')).to_be_visible()
        assert state.success_criteria == {}
    finally:
        context.close()
