"""Real Chromium + existing Flask server, synthetic invention/account data only.

These tests extend the existing correction journey; they do not evaluate the
meaning of answers or claim human usability evidence.
"""
import copy
import os
from pathlib import Path

import pytest
from playwright.sync_api import expect

import web.app as webapp
from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser, _start, ANSWER

TEXTS = [ANSWER + '\n  Recorded detail العربية EN & <img src=x onerror="alert(1)">\n' + 'x' * 900,
         ANSWER + '\n  إجابة أخرى EN: a different tail.']
REPLACEMENT = 'The comparator senses excess current and opens the relay; the exact trip threshold is still unknown.'


def prepare(page, server, lang='en'):
    if lang == 'ar':
        page.goto(server)
        page.get_by_role('button', name='العربية', exact=True).click()
    sid = _start(page, server)
    assert page.locator('#correction-preview').count() == 0
    for answer in TEXTS:
        page.locator('#response').fill(answer)
        page.locator('#answer-form button[type="submit"]').click()
        page.wait_for_load_state()
    page.locator('details.correct-answer > summary').click()
    return sid


@pytest.mark.parametrize('lang', ['en', 'ar'])
@pytest.mark.parametrize('width', [360, 1280])
def test_full_answer_target_keyboard_layout_and_native_submission(server, page, lang, width):
    page.set_viewport_size({'width': width, 'height': 900})
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    sid = prepare(page, server, lang)
    select = page.get_by_label(text('UI_RVR5_CORRECT_SELECT', lang), exact=True)
    ids = select.locator('option').evaluate_all('els => els.map(e => e.value)')
    stored_before = {r.record_id: r.content for r in webapp.SESSION_STORE[sid]['state'].assertions}
    # Native form encoding stores CRLF; HTML parsing displays those newlines as LF.
    assert [stored_before[rid].replace('\r\n', '\n') for rid in ids] == TEXTS
    assert len(ids) == 2 and TEXTS[0][:70] == TEXTS[1][:70]
    preview = page.locator('#correction-preview')
    expect(preview).to_be_visible()
    assert page.locator('[data-preview-content]').text_content() == TEXTS[0]
    assert page.locator('[data-preview-reference]').text_content() == ids[0]
    expect(page.locator('#correction-preview-heading')).to_have_text(text('UI_CORRECTION_PREVIEW_HEADING', lang))
    assert page.locator('html').get_attribute('lang') == lang
    assert page.locator('html').get_attribute('dir') == ('rtl' if lang == 'ar' else None)
    assert page.locator('[data-preview-content]').get_attribute('dir') == 'auto'
    assert page.locator('.correct-answer img').count() == 0
    form = page.locator('.correct-answer form')
    original = form.evaluate('e => Array.from(new FormData(e).entries())')
    assert [x[0] for x in original] == ['csrf_token', 'answer_token', 'supersedes_record_id', 'response']
    page.locator('#correct-response').fill(REPLACEMENT)
    # Selection changes must not touch the correction draft or move focus.
    select.focus()
    select.press('ArrowDown')
    expect(select).to_have_value(ids[1])
    expect(select).to_be_focused()
    assert page.locator('[data-preview-content]').text_content() == TEXTS[1]
    assert page.locator('[data-preview-reference]').text_content() == ids[1]
    source_context = page.locator('[data-correction-record]').nth(1).locator('[data-record-context]').text_content()
    assert page.locator('[data-preview-context]').text_content() == source_context
    expect(page.locator('#correct-response')).to_have_value(REPLACEMENT)
    expect(page.locator('#correction-preview-status')).to_have_text(
        text('UI_CORRECTION_PREVIEW_UPDATED', lang).replace('{reference}', ids[1]))
    select.press('Tab')
    expect(preview).to_be_focused()
    assert preview.evaluate('e => getComputedStyle(e).outlineStyle') != 'none'
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    after = dict(form.evaluate('e => Array.from(new FormData(e).entries())'))
    assert after == dict(original, supersedes_record_id=ids[1], response=REPLACEMENT)
    assert page.locator('[data-primary-action]').count() == 1
    evidence_dir = os.environ.get('CORRECTION_PREVIEW_EVIDENCE_DIR')
    if evidence_dir:
        target = Path(evidence_dir)
        target.mkdir(parents=True, exist_ok=True)
        page.locator('.correct-answer').screenshot(path=str(target / f'correction-preview-{lang}-{width}.png'))
    form.locator('button[type="submit"]').click()
    page.wait_for_load_state()
    records = webapp.SESSION_STORE[sid]['state'].assertions
    first = next(r for r in records if r.record_id == ids[0])
    second = next(r for r in records if r.record_id == ids[1])
    assert first.content == stored_before[ids[0]] and first.superseded_by is None
    assert second.content == stored_before[ids[1]] and second.superseded_by is not None
    assert records[-1].content == REPLACEMENT
    eligible = page.locator('[data-correction-record]').evaluate_all('els => els.map(e => e.dataset.correctionRecord)')
    assert ids[1] not in eligible and ids[0] in eligible
    assert not errors


@pytest.mark.parametrize('lang', ['en', 'ar'])
@pytest.mark.parametrize('mode', ['disabled', 'failed'])
def test_full_text_fallback_and_correction_without_preview_script(server, _browser, lang, mode):
    context = _browser.new_context(java_script_enabled=mode != 'disabled', viewport={'width': 360, 'height': 900})
    page = context.new_page()
    try:
        if mode == 'failed':
            page.route('**/static/js/correction_preview.js', lambda route: route.abort())
        sid = prepare(page, server, lang)
        expect(page.locator('#correction-preview')).to_be_hidden()
        disclosure = page.locator('.correction-full-answers')
        disclosure.locator('summary').focus()
        disclosure.locator('summary').press('Enter')
        for i, answer in enumerate(TEXTS):
            record = disclosure.locator('[data-record-content]').nth(i)
            expect(record).to_be_visible()
            assert record.text_content() == answer
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        ids = page.locator('#correct-target option').evaluate_all('els => els.map(e => e.value)')
        stored_before = next(r.content for r in webapp.SESSION_STORE[sid]['state'].assertions if r.record_id == ids[1])
        page.locator('#correct-target').select_option(ids[1])
        page.locator('#correct-response').fill(REPLACEMENT)
        page.locator('.correct-answer button[type="submit"]').click()
        page.wait_for_load_state()
        record = next(r for r in webapp.SESSION_STORE[sid]['state'].assertions if r.record_id == ids[1])
        assert record.content == stored_before and record.superseded_by is not None
    finally:
        context.close()


def test_preview_selection_has_no_network_storage_submission_or_state_effect(server, page):
    sid = prepare(page, server)
    # Let existing answer-acceptance cleanup complete before observing preview-only actions.
    page.wait_for_timeout(900)
    before_state = copy.deepcopy(webapp.SESSION_STORE[sid]['state'].__dict__)
    page.evaluate("""() => {
      window.previewWrites = [];
      for (const name of ['setItem', 'removeItem', 'clear']) {
        Storage.prototype[name] = function () { window.previewWrites.push(name); };
      }
      window.previewSubmits = 0;
      document.querySelector('.correct-answer form').addEventListener('submit', () => window.previewSubmits++);
    }""")
    before_storage = page.evaluate('JSON.stringify([document.cookie, {...localStorage}, {...sessionStorage}])')
    before_form = page.locator('.correct-answer form').evaluate('e => Array.from(new FormData(e).entries())')
    requests = []
    page.on('request', lambda request: requests.append(request.url))
    ids = page.locator('#correct-target option').evaluate_all('els => els.map(e => e.value)')
    for value in [ids[1], ids[0], ids[1], ids[0]]:
        page.locator('#correct-target').select_option(value)
    page.locator('.correction-full-answers summary').click()
    page.wait_for_timeout(1000)
    assert requests == []
    assert page.evaluate('previewWrites') == [] and page.evaluate('previewSubmits') == 0
    assert page.evaluate('JSON.stringify([document.cookie, {...localStorage}, {...sessionStorage}])') == before_storage
    assert page.locator('.correct-answer form').evaluate('e => Array.from(new FormData(e).entries())') == before_form
    assert webapp.SESSION_STORE[sid]['state'].__dict__ == before_state
    # Browser-restored selections are reconciled without stale preview text.
    page.locator('#correct-target').evaluate('(e, id) => e.value = id', ids[1])
    page.evaluate("window.dispatchEvent(new Event('pageshow'))")
    assert page.locator('[data-preview-content]').text_content() == TEXTS[1]
    # No matching selection must clear the old preview, not display another record.
    page.locator('#correct-target').evaluate("e => { e.selectedIndex = -1; e.dispatchEvent(new Event('change')); }")
    expect(page.locator('#correction-preview')).to_be_hidden()
    assert page.locator('[data-preview-content]').text_content() == ''


def test_cold_readonly_has_no_preview_then_explicit_resume_restores_it(server, page):
    sid = prepare(page, server)
    webapp.SESSION_STORE.pop(sid)
    page.reload()
    assert page.locator('#correction-preview').count() == 0
    assert page.locator('[data-correction-record]').count() == 0
    assert page.locator('script[src$="/correction_preview.js"]').count() == 0
    expect(page.locator('#resume-project')).to_be_visible()
    page.locator('#resume-project').click()
    page.wait_for_load_state()
    page.locator('.correct-answer > summary').click()
    assert page.locator('[data-preview-content]').text_content() == TEXTS[0]
