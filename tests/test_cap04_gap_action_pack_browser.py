"""Real Chromium + the existing Flask server: CAP-04 Slice 1, the read-only
Actionable Gap Pack.

Synthetic invention data only. The inventor starts a Mechanical project and
answers through the real form; nothing is fabricated for display. At the start
the open gap has no acquisition route, so its pack says so; after the
mechanism is described the Physical Feasibility gap opens with its committed
specialist route, whose need text shows inside that gap's own pack (in the UI
language). The block holds no control; the report shows the same packs
read-only with report-local links that resolve.
"""
import pytest
from playwright.sync_api import expect

import web.app as webapp
from web.ui_text import text
from engine.path_n_questions import routing_policies
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_safe_question_routing_pf_q2 import MECH
from tests.test_safe_question_routing_pf_q2_weak_recovery_browser import (
    _start_mechanical, _answer,
)

_CONTROLS = "form, input, textarea, select, button"


def _pf_policy(sid):
    for gap, qid, policy in routing_policies(webapp.SESSION_STORE[sid]["state"].domain):
        if gap == "PHYSICAL_FEASIBILITY":
            return policy
    raise AssertionError("no committed PF routing policy")


def _open(block):
    if block.get_attribute("open") is None:
        block.locator("summary").first.click()


def _no_raw_ids(locator):
    body = locator.inner_text()
    for raw in ("mechanical-path-n-routing-v1", "routing_seq", "policy_ref",
                "PHYSICAL_FEASIBILITY", "MECHANISM_COMPLETENESS", ":Q2"):
        assert raw not in body, raw


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_gap_action_pack_journey(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_mechanical(page, server, lang)

    # start: an unresolved gap with no acquisition route — said explicitly
    block = page.locator("details#gap-action-packs")
    expect(block).to_contain_text(text("UI_GP_HEADING", lang))
    assert block.locator(_CONTROLS).count() == 0
    _open(block)
    packs = block.locator("details.gp-pack")
    assert packs.count() >= 1
    first = packs.first
    _open(first)
    expect(first.locator("p.gp-no-route")).to_have_text(text("UI_GP_NO_ROUTE", lang))
    expect(first.locator("p.gp-after")).to_have_text(text("UI_GP_AFTER", lang))
    expect(first.locator("dd.gp-action")).not_to_be_empty()
    assert block.locator("[data-gp-empty], [data-gp-unavailable]").count() == 0
    _no_raw_ids(block)

    # the mechanism is described: Physical Feasibility opens with its route
    for value in (MECH, MECH):
        _answer(page, value)
    policy = _pf_policy(sid)
    block = page.locator("details#gap-action-packs")
    assert block.locator(_CONTROLS).count() == 0
    _open(block)
    pf = block.locator('details.gp-pack[data-gp-gap="physical-feasibility"]')
    expect(pf).to_have_count(1)
    _open(pf)
    route = pf.locator("div.gp-route")
    expect(route).to_have_count(1)
    assert route.get_attribute("data-gp-route-available") == "yes"
    expected_need = policy.need_text_ar if lang == "ar" else policy.need_text
    expect(route.locator(".gp-route-text")).to_have_text(expected_need)
    expect(route).to_contain_text(text("UI_GP_RESP_SPECIALIST_REQUIRED", lang))
    assert pf.locator("p.gp-no-route").count() == 0
    # the route stays with its own gap only
    others = block.locator(
        'details.gp-pack:not([data-gp-gap="physical-feasibility"]) div.gp-route')
    assert others.count() == 0
    # a closed gap has no pack
    assert block.locator(
        'details.gp-pack[data-gp-gap="mechanism-completeness"]').count() == 0
    _no_raw_ids(block)

    # every pack here is one current unresolved gap (multiple where present)
    gaps = block.locator("details.gp-pack").evaluate_all(
        "els => els.map(e => [e.dataset.gpGap, e.dataset.gpState])")
    assert gaps and all(s in ("open", "partial") for _, s in gaps), gaps
    assert len({g for g, _ in gaps}) == len(gaps)
    assert int(block.locator(".gp-count").inner_text()) == len(gaps)

    # detail link into the report's landscape; report packs read-only
    block.locator("p.gp-links a.gp-link").first.click()
    page.wait_for_load_state()
    assert page.url.endswith(f"/session/{sid}/deliverable#report-needs")
    rep = page.locator("#report-gap-action-packs")
    expect(rep).to_contain_text(text("UI_GP_HEADING", lang))
    assert rep.locator(_CONTROLS + ", details").count() == 0
    rgaps = rep.locator("div.gp-pack").evaluate_all(
        "els => els.map(e => [e.dataset.gpGap, e.dataset.gpState])")
    assert rgaps == gaps
    expect(rep.locator('div.gp-pack[data-gp-gap="physical-feasibility"] '
                       '.gp-route-text')).to_have_text(expected_need)
    hrefs = rep.locator("a").evaluate_all(
        "els => els.map(e => e.getAttribute('href'))")
    assert set(hrefs) == {"#report-needs", "#report-validation-plan"}
    for href in hrefs:
        assert page.locator(href).count() == 1, href
    rep.locator('a[href="#report-validation-plan"]').click()
    assert page.url.endswith("#report-validation-plan")
    expect(page.locator("#report-validation-plan + h3")).to_have_text(
        text("UI_B_DELIV_085", lang))
    _no_raw_ids(rep)

    assert page.locator("html").get_attribute("lang") == lang
    assert not errors
