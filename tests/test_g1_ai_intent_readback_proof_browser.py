# -*- coding: utf-8 -*-
"""Real Chromium: G1-AI-INTENT-READBACK-CONSUMER-PROOF-01 presentation, EN and
AR (RTL), at 390 px and 1280 px.

The test-only readback fragment is placed into the REAL start page served by
the existing Flask app (inside the browser only, never by the app), above the
unchanged form, so it is checked with the product's own styles and language
setting. Synthetic data and preserved provider replies only.
"""
import pytest
from playwright.sync_api import expect

import tests.g1_intent_readback_proof as rp
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401


def _show(page, base, lang, fragment):
    page.goto(base + "/")
    if lang == "ar":
        page.get_by_role("button", name="العربية", exact=True).click()
        page.wait_for_load_state()
    page.evaluate("html => { const m = document.querySelector('main') || document.body;"
                  " m.insertAdjacentHTML('afterbegin', html); }", fragment)
    return page.locator("section.g1-readback")


def _adds_no_horizontal_scroll(page):
    """The readback adds no horizontal overflow of its own and fits the
    viewport. (The unchanged start page itself is a few pixels wider than a
    390 px viewport; that pre-existing overflow is compared, not hidden.)"""
    for width in (390, 1280):
        page.set_viewport_size({"width": width, "height": 900})
        with_box = page.evaluate("document.documentElement.scrollWidth")
        without = page.evaluate("""() => { const b = document.querySelector('section.g1-readback');
            b.style.display = 'none'; const w = document.documentElement.scrollWidth;
            b.style.display = ''; return w; }""")
        assert with_box <= without + 1, width
        assert page.evaluate("""w => [...document.querySelectorAll('section.g1-readback *')]
            .every(e => e.getBoundingClientRect().right <= w + 1 && e.getBoundingClientRect().left >= -1)""",
                             page.evaluate("document.documentElement.clientWidth")), width


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_readback_presentation_and_correction(server, page, lang):
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    if lang == "en":
        idea, reply, source = rp.preserved("H08")
        wrong, src = rp.constructed("H08_incorrect")
        rb = rp.build(idea, wrong["reply"], src)
    else:
        item, src = rp.constructed("AR01")
        idea, rb = item["idea_text"], rp.build(item["idea_text"], item["reply"], src)
    t = rp.TEXT[lang]
    box = _show(page, server, lang, rp.render(rb, lang))
    expect(box).to_have_count(1)
    expect(box.locator("h2")).to_have_text(t["title"])
    expect(box.locator("[data-ai-label]")).to_be_visible()
    expect(box.locator("[data-inventor-words]")).to_have_text(idea)
    expect(box.locator('[data-pointer="integrated"]')).to_be_visible()
    assert box.evaluate("e => getComputedStyle(e).direction") == ("rtl" if lang == "ar" else "ltr")
    assert page.locator("textarea[name='idea'], [name='idea']").count() >= 1   # the form is untouched
    _adds_no_horizontal_scroll(page)
    if lang == "en":
        res = rp.resolve(rp.issue(rb), rb, idea, "correct", exclude_index=1,
                         remark="The phone is mine. I am only inventing the clamp.")
        box.evaluate("(e, html) => { e.outerHTML = html; }", rp.render(res["readback"], lang))
        fixed = page.locator("section.g1-readback")
        expect(fixed.locator('[data-excluded="1"]')).to_be_visible()
        expect(fixed.locator('[data-pointer="none"]')).to_be_visible()
        expect(fixed.locator('[data-part="1"]')).to_have_count(0)
        expect(fixed.locator("[data-inventor-remark]")).to_contain_text("I am only inventing the clamp")
        _adds_no_horizontal_scroll(page)
    assert not errors


def test_unknown_stays_open_in_both_languages(server, page):
    idea, reply, source = rp.preserved("H14")
    rb = rp.build(idea, reply, source)
    for lang in ("en", "ar"):
        box = _show(page, server, lang, rp.render(rb, lang))
        expect(box.locator("[data-open]")).to_contain_text(rp.TEXT[lang]["open_note"])
        expect(box.locator("[data-obstacle]")).to_be_visible()
        assert reply["clarification_questions"][0] not in box.inner_text()
