"""Real Chromium + the existing Flask server: Stage 25 / CAP-13 Two-Support
Static Reactions Slice 1 (EN and AR).

Synthetic invention data only. A Mechanical project is started through the real
forms; the optional link leads to the request-local page, every declaration and
screen item is answered explicitly (nothing is pre-selected), the values are
typed, and the reactions render in the response itself. At phone width the
page has no horizontal overflow; in Arabic it is RTL and the numbers, unit
tokens and role symbols stay direction-isolated.
"""
import pytest
from playwright.sync_api import expect

from web.ui_text import text
from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_safe_question_routing_pf_q2_weak_recovery_browser import (
    _start_mechanical,
)


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_support_reactions_journey(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_mechanical(page, server, lang)
    link = page.locator("[data-cap13-link] a")
    expect(link).to_have_text(text("UI_CAP13_LINK_TEXT", lang))
    link.click()
    page.wait_for_load_state()
    assert page.url.endswith(f"/session/{sid}/support-reactions")

    form = page.locator("[data-cap13-form]")
    radios = form.locator("input[type=radio]")
    expect(radios).to_have_count(38)
    assert form.locator("input[type=radio]:checked").count() == 0
    for fieldset in form.locator("[data-cap13-declaration]").all():
        fieldset.locator("input[value=matches]").check()
    for fieldset in form.locator("[data-cap13-screen]").all():
        fieldset.locator("input[value=no]").check()
    page.fill("#cap13-P", "1000")
    page.fill("#cap13-L", "2000")
    page.fill("#cap13-x", "500")
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()
    assert page.url.endswith(f"/session/{sid}/support-reactions")

    reactions = page.locator("[data-cap13-reaction]")
    expect(reactions).to_have_count(2)
    expect(reactions.nth(0)).to_have_text("750.0 N")
    expect(reactions.nth(1)).to_have_text("250.0 N")
    assert reactions.nth(0).locator("bdi").get_attribute("dir") == "ltr"
    expect(page.locator("[data-cap13-method] bdi").first).to_have_text(
        "cap13:static_reactions_two_support")
    expect(page.locator("[data-cap13-disclosure]")).to_be_visible()
    expect(page.locator("[data-cap13-status]")).to_contain_text("UNVALIDATED")

    # a refusal shows one reason and no number
    page.fill("#cap13-x", "2500")
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()
    expect(page.locator("[data-cap13-outcome]")).to_have_count(1)
    expect(page.locator("[data-cap13-reaction]")).to_have_count(0)

    # layout: coherent at phone width, no horizontal overflow; RTL on Arabic
    page.set_viewport_size({"width": 390, "height": 900})
    width = page.evaluate("document.documentElement.clientWidth")
    assert page.evaluate("document.documentElement.scrollWidth") <= width + 1
    assert page.locator("[data-cap13-form]").bounding_box()["width"] <= width
    assert page.locator("html").get_attribute("lang") == lang
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
        assert page.locator("#cap13-x").get_attribute("dir") == "ltr"
        iso = page.locator("label[for=cap13-P] bdi[dir=ltr]")
        expect(iso).to_have_text("N")
    assert not errors


def _figure_markup(page):
    return page.locator("[data-cap13-figure]").evaluate("el => el.outerHTML")


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_measurement_figure_in_real_browser(server, page, lang):
    """CAP13-MEASUREMENT-FIGURE-01: one static, accessible figure; physical left
    stays left on the Arabic page; unchanged by a result or a refusal; no
    horizontal overflow at phone width."""
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_mechanical(page, server, lang)
    page.goto(f"{server}/session/{sid}/support-reactions")
    page.wait_for_load_state()

    figure = page.locator("[data-cap13-figure]")
    expect(figure).to_have_count(1)
    expect(figure).to_be_visible()
    image = page.get_by_role("img", name=text("UI_CAP13_FIGURE_TITLE", lang), exact=True)
    expect(image).to_have_count(1)
    description = " ".join(text("UI_CAP13_FIGURE_" + k, lang) for k in ("DESC", "NOTE"))
    expect(image).to_have_accessible_description(description)
    assert page.locator("[data-cap13-figure-art]").get_attribute("dir") == "ltr"

    def centre(selector):
        box = page.locator(selector).bounding_box()
        return box["x"] + box["width"] / 2

    def check_physical_layout():
        left_line = centre("[data-cap13-figure-line=left-support]")
        right_line = centre("[data-cap13-figure-line=right-support]")
        cg_line = centre("[data-cap13-figure-line=centre-of-gravity]")
        assert left_line < cg_line < right_line
        assert centre("[data-cap13-figure-label=left-support]") < centre(
            "[data-cap13-figure-label=right-support]")
        assert centre("[data-cap13-figure-symbol=R_L]") < centre("[data-cap13-figure-symbol=R_R]")
        x_box = page.locator("[data-cap13-figure-symbol=x]").bounding_box()
        assert abs(x_box["x"] - left_line) <= 1 and abs(x_box["x"] + x_box["width"] - cg_line) <= 1
        assert abs(centre("[data-cap13-figure-symbol=P] line") - cg_line) <= 1

    check_physical_layout()
    first_view = _figure_markup(page)

    form = page.locator("[data-cap13-form]")
    for fieldset in form.locator("[data-cap13-declaration]").all():
        fieldset.locator("input[value=matches]").check()
    for fieldset in form.locator("[data-cap13-screen]").all():
        fieldset.locator("input[value=no]").check()
    page.fill("#cap13-P", "1000")
    page.fill("#cap13-L", "2000")
    page.fill("#cap13-x", "500")
    form.locator("button[type=submit]").click()
    page.wait_for_load_state()
    expect(page.locator("[data-cap13-reaction]")).to_have_count(2)
    assert _figure_markup(page) == first_view          # a result changes nothing in it
    page.fill("#cap13-x", "2500")
    page.locator("[data-cap13-form] button[type=submit]").click()
    page.wait_for_load_state()
    expect(page.locator("[data-cap13-outcome]")).to_have_count(1)
    assert _figure_markup(page) == first_view          # nor does a refusal

    page.set_viewport_size({"width": 390, "height": 900})
    width = page.evaluate("document.documentElement.clientWidth")
    assert page.evaluate("document.documentElement.scrollWidth") <= width + 1
    box = figure.bounding_box()
    assert box["x"] >= 0 and box["x"] + box["width"] <= width
    assert page.locator("[data-cap13-figure-art] svg").bounding_box()["width"] > 200
    check_physical_layout()
    if lang == "ar":
        assert page.locator("html").get_attribute("dir") == "rtl"
    assert not errors


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_declaration_guidance_in_real_browser(server, page, lang):
    """CAP13-DECLARATION-GUIDANCE-01: each declaration group shows its own
    plain-language help between its legend and its answers, exposes it as the
    group's accessible description, selects nothing, and fits at phone width;
    the figure's labels name the supports, not the support lines."""
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start_mechanical(page, server, lang)
    page.goto(f"{server}/session/{sid}/support-reactions")
    page.wait_for_load_state()
    groups = page.locator("[data-cap13-form] [data-cap13-declaration]")
    expect(groups).to_have_count(10)
    for group in groups.all():
        decl = group.get_attribute("data-cap13-declaration")
        help_text = text("UI_CAP13_DECL_HELP_" + decl.upper(), lang)
        note = group.locator("[data-cap13-declaration-help]")
        expect(note).to_have_count(1)
        expect(note).to_be_visible()
        assert " ".join(note.inner_text().split()) == " ".join(help_text.split())
        expect(group).to_have_accessible_description(help_text)
        legend_box = group.locator("legend").bounding_box()
        note_box = note.bounding_box()
        first_answer = group.locator("input[type=radio]").first.bounding_box()
        assert legend_box["y"] < note_box["y"] < first_answer["y"]
    assert page.locator("[data-cap13-form] input[type=radio]:checked").count() == 0
    expect(page.locator("[data-cap13-figure-label=left-support]")).to_have_text(
        text("UI_CAP13_FIGURE_LEFT_SUPPORT", lang))
    page.set_viewport_size({"width": 390, "height": 900})
    width = page.evaluate("document.documentElement.clientWidth")
    assert page.evaluate("document.documentElement.scrollWidth") <= width + 1
    for note in page.locator("[data-cap13-declaration-help]").all():
        box = note.bounding_box()
        assert box["x"] >= 0 and box["x"] + box["width"] <= width
    assert not errors
