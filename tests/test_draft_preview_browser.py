"""Real Chromium and rendered recovery prompts; synthetic invention data only.

The correction fixture uses the same explicit completion-state setup as the
existing local-draft test. It proves recovery presentation, not engine maturity.
"""
import copy
import json
import os
from pathlib import Path

import pytest
from playwright.sync_api import expect

import web.app as webapp
from engine.idea_state import IdeaState
from tests.test_draft_l2_local_continuity import (
    server, page, _browser, _start, _present_domain_confirmation, _confirm_start,
    IDEA, ANSWER, SEED_KEY,
)

LABELS = {
    'en': 'Preview unsent text stored on this device',
    'ar': 'معاينة النص غير المرسل المحفوظ على هذا الجهاز',
}
PAYLOAD = '  Unsent EN / نص غير مرسل\n\tline 2 & <img src=x onerror="alert(1)">\n' + 'x' * 1100 + '\n  end  \n'

# Test instrumentation records operation names/keys, never draft content.
AUDIT = """(() => {
  window.draftOps = [];
  const get = Storage.prototype.getItem;
  window.draftSnapshot = () => Object.keys(localStorage).sort().map(
    key => [key, get.call(localStorage, key)]);
  for (const name of ['getItem', 'setItem', 'removeItem', 'clear', 'key']) {
    const original = Storage.prototype[name];
    Storage.prototype[name] = function(...args) {
      window.draftOps.push([name, name === 'clear' ? null : args[0]]);
      return original.apply(this, args);
    };
  }
  window.draftFormEvents = [];
  for (const name of ['input', 'change', 'submit']) {
    document.addEventListener(name, () => window.draftFormEvents.push(name));
  }
})();"""


def prepare(page, base, surface='seed', lang='en'):
    if lang == 'ar':
        page.goto(base)
        page.get_by_role('button', name='العربية', exact=True).click()
    if surface == 'seed':
        page.goto(base)
        sid = None
    else:
        sid = _start(page, base)
        if surface == 'correction':
            state = IdeaState(idea_id=sid)
            state.domain = state.domain_signal = 'electronics_electrical'
            state.maturity_level = 2
            state.current_stage = 3
            webapp.SESSION_STORE[sid] = {
                'state': state, 'last_result': None, 'transcript': [],
                'criticality_correction': True}
            page.goto(base + '/session/' + sid)
    field = page.locator('textarea[data-draft-field="' + ('idea' if surface == 'seed' else surface) + '"]')
    expect(field).to_have_count(1)
    return sid, field


def key_for(field):
    return field.evaluate("""el => {
      const d=el.dataset;
      const key='inventorai:draft:v1:'+d.draftScope+':'+d.draftField+':'+d.draftContext+':'+d.draftContextVersion;
      return key+(d.draftAccount && d.draftAccount!=='anon' ? ':acct:'+d.draftAccount : '');
    }""")


def offer(page, field, payload=PAYLOAD):
    key = key_for(field)
    field.fill(payload)
    page.wait_for_function("""([key,text]) => {
      const raw=localStorage.getItem(key);
      return raw && JSON.parse(raw).text===text;
    }""", arg=[key, payload])
    page.reload()
    expect(page.locator('.draft-preview')).to_have_count(1)
    expect(field).to_have_value('')
    return key


@pytest.mark.parametrize('surface', ['seed', 'answer', 'correction'])
@pytest.mark.parametrize('lang,width', [('en', 1280), ('en', 360), ('ar', 1280), ('ar', 360)])
def test_exact_preview_native_keyboard_and_unchanged_restore(server, page, surface, lang, width):
    page.add_init_script(AUDIT)
    page.set_viewport_size({'width': width, 'height': 900})
    sid, field = prepare(page, server, surface, lang)
    key = offer(page, field)
    preview = page.locator('.draft-preview')
    summary = preview.locator('summary')
    content = preview.locator('.draft-preview-text')
    expect(summary).to_have_text(LABELS[lang])
    assert preview.get_attribute('open') is None
    expect(content).to_be_hidden()
    assert preview.get_attribute('lang') == lang
    assert preview.get_attribute('dir') == ('rtl' if lang == 'ar' else 'ltr')
    assert content.get_attribute('dir') == 'auto'
    assert content.text_content() == PAYLOAD
    assert content.locator('*').count() == 0
    assert content.evaluate('e => getComputedStyle(e).whiteSpace') == 'pre-wrap'
    # Construction reads the existing draft once for each wired field; the
    # preview must not read it a second time.
    assert page.evaluate('draftOps.filter(x => x[0]==="getItem")') == [['getItem', key]]
    storage = page.evaluate('draftSnapshot()')
    operations = page.evaluate('draftOps.slice()')
    form = field.locator('..')
    fields = form.evaluate('e => Array.from(new FormData(e).entries())')
    state = copy.deepcopy(webapp.SESSION_STORE[sid]['state'].__dict__) if sid else None
    requests, errors, messages = [], [], []
    page.on('request', lambda r: requests.append(r.url))
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.on('console', lambda m: messages.append(m.text))
    # Reach the native summary through the pre-existing Discard button.
    page.locator('.draft-discard').focus()
    page.keyboard.press('Tab')
    expect(summary).to_be_focused()
    assert summary.evaluate('e => getComputedStyle(e).outlineStyle') != 'none'
    summary.press('Enter')
    expect(content).to_be_visible()
    assert preview.evaluate('e => e.scrollWidth <= e.clientWidth')
    assert preview.evaluate('e => {const r=e.getBoundingClientRect(); return r.left>=0 && r.right<=innerWidth;}')
    summary.press('Space')
    expect(content).to_be_hidden()
    summary.press('Enter')
    expect(content).to_be_visible()
    assert page.evaluate('draftOps') == operations
    assert page.evaluate('draftSnapshot()') == storage
    assert page.evaluate('draftFormEvents') == []
    assert form.evaluate('e => Array.from(new FormData(e).entries())') == fields
    if sid:
        assert webapp.SESSION_STORE[sid]['state'].__dict__ == state
    assert not requests and not errors and not messages
    target_dir = os.environ.get('DRAFT_PREVIEW_EVIDENCE_DIR')
    if target_dir and surface == 'seed':
        page.locator('.draft-recovery').screenshot(path=str(Path(target_dir) / f'draft-preview-{lang}-{width}.png'))
    page.locator('.draft-restore').click()
    expect(field).to_have_value(PAYLOAD)
    expect(field).to_be_focused()
    expect(preview).to_have_count(0)
    assert page.evaluate('draftSnapshot()') == storage
    assert page.evaluate('draftOps') == operations
    assert not requests


@pytest.mark.parametrize('lang', ['en', 'ar'])
def test_preview_then_discard_removes_only_matching_draft(server, page, lang):
    _, field = prepare(page, server, lang=lang)
    key = offer(page, field)
    page.evaluate("localStorage.setItem('unrelated-test-record', 'retain')")
    page.locator('.draft-preview summary').click()
    page.locator('.draft-discard').click()
    assert page.evaluate('(k) => localStorage.getItem(k)', key) is None
    assert page.evaluate("localStorage.getItem('unrelated-test-record')") == 'retain'
    expect(field).to_have_value('')
    expect(field).to_be_focused()
    expect(page.locator('.draft-preview')).to_have_count(0)


@pytest.mark.parametrize('invalid', [
    'account', 'project', 'field', 'context', 'version', 'expired', 'malformed', 'nonempty',
])
def test_ineligible_or_unmatched_draft_never_exposes_preview(server, page, invalid):
    _, field = prepare(page, server)
    private = 'SYNTHETIC PRIVATE TEXT MUST NOT BE EXPOSED'
    record = {'v': 1, 'text': private, 'ts': page.evaluate('Date.now()'),
              'scope': '__seed__', 'field': 'idea', 'context': 'seed',
              'ctxver': 'v1', 'account': 'anon'}
    changes = {'account': ('account', 'another-account'), 'project': ('scope', 'another-project'),
               'field': ('field', 'answer'), 'context': ('context', 'another-question'),
               'version': ('ctxver', 'v2'), 'expired': ('ts', 0)}
    if invalid in changes:
        name, value = changes[invalid]
        record[name] = value
    raw = '{malformed' if invalid == 'malformed' else json.dumps(record)
    page.evaluate('([key,raw]) => localStorage.setItem(key,raw)', [SEED_KEY, raw])
    if invalid == 'nonempty':
        # Existing nonempty-field guard: synthetic server/browser-restored text,
        # followed by the same initializer used by the existing recovery test.
        field.evaluate("e => {e.value='Keep visible text';}")
        page.evaluate("document.dispatchEvent(new Event('DOMContentLoaded'))")
        expect(field).to_have_value('Keep visible text')
    else:
        page.reload()
    expect(page.locator('.draft-recovery')).to_have_count(0)
    expect(page.locator('.draft-preview')).to_have_count(0)
    assert private not in page.content()


@pytest.mark.parametrize('existing_offer', [False, True])
def test_cross_tab_offer_and_preview_share_the_exact_restore_value(server, _browser, existing_offer):
    context = _browser.new_context()
    try:
        first, second = context.new_page(), context.new_page()
        _, field = prepare(first, server)
        old, newer = 'Older offered draft', 'Newer text typed in the second tab'
        if existing_offer:
            offer(first, field, old)
        second.goto(server)
        second.locator('#idea').fill(newer)
        second.wait_for_function("(k) => JSON.parse(localStorage.getItem(k)||'null')?.text === 'Newer text typed in the second tab'", arg=SEED_KEY)
        expect(first.locator('.draft-preview')).to_have_count(1)
        expected = old if existing_offer else newer
        # No live re-read: an already visible offer retains its captured value,
        # exactly like the pre-existing Restore closure.
        first.locator('.draft-preview summary').click()
        assert first.locator('.draft-preview-text').text_content() == expected
        assert 'newest' not in first.locator('.draft-preview').inner_text().lower()
        first.locator('.draft-restore').click()
        expect(field).to_have_value(expected)
        assert first.evaluate('(k) => JSON.parse(localStorage.getItem(k)).text', SEED_KEY) == newer
    finally:
        context.close()


def test_existing_offer_preview_and_restore_work_without_further_storage_access(server, page):
    _, field = prepare(page, server)
    offer(page, field)
    page.evaluate("""() => {
      window.blockedStorageCalls=0;
      for (const name of ['getItem','setItem','removeItem','clear','key']) {
        Storage.prototype[name]=function(){window.blockedStorageCalls++; throw Error('denied');};
      }
    }""")
    page.locator('.draft-preview summary').click()
    page.locator('.draft-preview summary').click()
    page.locator('.draft-restore').click()
    expect(field).to_have_value(PAYLOAD)
    assert page.evaluate('blockedStorageCalls') == 0


@pytest.mark.parametrize('surface', ['seed', 'answer', 'correction'])
def test_no_javascript_has_no_preview_and_preserves_submission(server, _browser, surface):
    context = _browser.new_context(java_script_enabled=False)
    page = context.new_page()
    try:
        sid, field = prepare(page, server, surface)
        expect(page.locator('.draft-preview')).to_have_count(0)
        if surface == 'seed':
            field.fill(IDEA)
            _present_domain_confirmation(page)
            sid = _confirm_start(page)
            assert sid in webapp.SESSION_STORE
        else:
            before = len(webapp.SESSION_STORE[sid]['state'].assertions)
            field.fill(ANSWER)
            field.locator('..').locator('button[type=submit]').click()
            page.wait_for_load_state()
            assert len(webapp.SESSION_STORE[sid]['state'].assertions) == before + 1
    finally:
        context.close()
