# -*- coding: utf-8 -*-
"""Real Chromium: the G1 faithful-readback statement-rejection proof, Arabic
(RTL), at 390 px and 1280 px.

The test-only fragment is placed into the REAL start page served by the
existing Flask app (inside the browser only, never by the app), above the
unchanged form. The «ليس هذا ما أقصده» click is a scripted browser click; the
browser hands it to the test-only seam through an exposed binding and shows
the seam's new rendering. The start itself (description, domain choice,
confirmation and the stored seed) is the real product path. Preserved #978
replies only, unchanged.
"""
import os
import sqlite3

import pytest
from playwright.sync_api import expect

import tests.g1_faithful_readback_proof as fr
import web.app as webapp
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401

ELEC = "electronics_electrical"
_WIRE = """() => { window.__wire = () => {
  const box = document.querySelector('section.g1-faithful-readback');
  box.addEventListener('click', async ev => {
    const b = ev.target.closest('button');
    if (!b) return;
    const out = b.hasAttribute('data-confirm')
      ? await window.g1Act('confirm', -1)
      : await window.g1Act('reject_statement', Number(b.getAttribute('data-reject')));
    if (out.html) {
      const fresh = document.querySelector('section.g1-faithful-readback');
      fresh.outerHTML = out.html;
      window.__wire();
    }
    if (out.confirmed !== undefined) document.body.setAttribute('data-confirmed', out.confirmed);
  });
}; window.__wire(); }"""


def _seed(sid):
    store = webapp._STORE
    path = store._path if store is not None else os.environ["INVENTORAI_DB_PATH"]
    conn = sqlite3.connect(path)
    try:
        return conn.execute("SELECT seed_idea_text FROM projects WHERE project_id = ?",
                            (sid,)).fetchone()[0]
    finally:
        conn.close()


def _arabic_start_page(page, base):
    page.goto(base + "/")
    page.get_by_role("button", name="العربية", exact=True).click()
    page.wait_for_load_state()


def _submit_start(page):
    """The real start path in the browser: submit the description, then the
    inventor's own domain choice and confirmation, until a project exists."""
    for _ in range(3):
        if "/session/" in page.url:
            break
        radio = page.locator('input[type=radio][name="domain_choice"][value="%s"]' % ELEC)
        if radio.count():
            radio.check()
        confirm = page.locator("input[name=domain_confirm]")
        if confirm.count():
            confirm.check()
        page.locator("main input[type=submit], main button[type=submit]").first.click()
        page.wait_for_load_state()
    assert "/session/" in page.url
    return page.url.rsplit("/session/", 1)[1].split("?")[0]


def _direct_start(page, base, idea):
    _arabic_start_page(page, base)
    page.fill("#idea", idea)
    return _seed(_submit_start(page))


def _show_readback(page, base, case_id):
    idea, reply, case = fr.preserved(case_id)
    state = {"rb": fr.build(idea, reply, case)}
    state["token"] = fr.issue(state["rb"])

    def act(_source, action, index):
        res = fr.resolve(state["token"], state["rb"], idea, case, action,
                         None if action == "confirm" else index)
        if res is None:
            return {}
        if action == "confirm":
            state["confirmed"] = res
            return {"confirmed": ",".join(str(i) for i in res["confirmed_statements"])}
        state["rb"], state["token"] = res["readback"], res["token"]
        return {"html": fr.render(state["rb"])}

    page.expose_binding("g1Act", act)
    _arabic_start_page(page, base)
    page.fill("#idea", idea)
    page.evaluate("html => { const m = document.querySelector('main') || document.body;"
                  " m.insertAdjacentHTML('afterbegin', html); }", fr.render(state["rb"]))
    page.evaluate(_WIRE)
    return idea, reply, state, page.locator("section.g1-faithful-readback")


def _fits(page):
    for width in (390, 1280):
        page.set_viewport_size({"width": width, "height": 900})
        assert page.evaluate("""w => [...document.querySelectorAll('section.g1-faithful-readback *')]
            .every(e => e.getBoundingClientRect().right <= w + 1 && e.getBoundingClientRect().left >= -1)""",
                             page.evaluate("document.documentElement.clientWidth")), width


def test_the_inventor_rejects_the_sometimes_statement_and_starts(server, page, _browser):
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    idea, reply, state, box = _show_readback(page, server, "ar_gulf_kuwaiti-03")
    t = fr.TEXT_AR
    expect(box.locator("h2")).to_have_text(t["title"])
    assert box.evaluate("e => getComputedStyle(e).direction") == "rtl"
    expect(box.locator("[data-inventor-words]")).to_have_text(idea)
    expect(box.locator("[data-rephrasing]")).to_have_text(reply["rephrasing"])
    first = box.locator('li[data-statement="0"]')
    expect(first.locator('p[data-author="ai"]')).to_contain_text("أحيانًا")
    expect(first.locator('p[data-author="inventor"]')).to_contain_text("دايماً")
    expect(first.locator('p[data-author="inventor"] .who')).to_have_text(t["quote"] + ":")
    _fits(page)

    page.get_by_role("button", name=t["reject"]).first.click()        # scripted click
    box = page.locator("section.g1-faithful-readback")
    first = box.locator('li[data-statement="0"]')
    expect(first).to_have_attribute("data-status", "rejected")
    expect(first.locator("del")).to_contain_text("أحيانًا")
    expect(first.locator("[data-rejected-note]")).to_have_text(t["rejected"])
    expect(first.locator("button")).to_have_count(0)
    for i in (1, 2, 3):
        li = box.locator('li[data-statement="%d"]' % i)
        expect(li).to_have_attribute("data-status", "shown")
        expect(li.locator("button")).to_have_text(t["reject"])
        expect(li.locator("del")).to_have_count(0)
    expect(page.locator("#idea")).to_have_value(idea)                 # the description is untouched
    _fits(page)

    box.locator("button[data-confirm]").click()                       # scripted click
    expect(page.locator("body")).to_have_attribute("data-confirmed", "1,2,3")
    assert state["confirmed"]["rejected_statements"] == (0,)
    assert state["confirmed"]["scope"] == fr.CONFIRMATION_SCOPE

    reviewed = _seed(_submit_start(page))
    other = _browser.new_context().new_page()
    try:
        direct = _direct_start(other, server, idea)
    finally:
        other.context.close()
    assert reviewed.encode("utf-8") == direct.encode("utf-8") == idea.encode("utf-8")
    assert "دايماً" in reviewed and "أحيانًا" not in reviewed
    assert not errors


def test_the_faithful_control_skipping_the_review(server, page):
    idea, reply, state, box = _show_readback(page, server, "ar_msa-01")
    expect(box.locator('li[data-status="shown"]')).to_have_count(len(reply["statements"]))
    seed = _seed(_submit_start(page))                                 # started without acting on it
    assert seed.encode("utf-8") == idea.encode("utf-8")
    assert "confirmed" not in state
