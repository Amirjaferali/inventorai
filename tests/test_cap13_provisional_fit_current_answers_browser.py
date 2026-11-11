"""Real Chromium + the existing Flask server: CAP13-PROVISIONAL-FIT-CURRENT-ANSWERS-01
(EN and AR).

Synthetic data only. A Mechanical project whose original idea states no
dimensions gets ONE ordinary answer, through the real answer form, that states
the desk object's size and lift explicitly. The session page then offers the
existing provisional dimensional fit, and that view quotes the answer under
"Your current recorded answer", never as the original statement. Arabic is RTL;
nothing overflows at 390 px.
"""
import pytest
from playwright.sync_api import expect

from tests.test_draft_l2_local_continuity import server, page, _browser  # noqa: F401
from tests.test_cap13_therm01_integrated_part_browser import _no_overflow

IDEA = {"en": "A wooden stand that lifts my monitor so the screen sits at eye level.",
        "ar": "حامل خشبي يرفع شاشة الحاسوب حتى تكون في مستوى النظر."}
ANSWER = {"en": "I want to raise the monitor 15 cm above my desk; dimensions 60 x 20 cm",
          "ar": "أريد رفع الشاشة 15 سم فوق مكتبي وأبعاده 60 × 20 سم"}
HEADING = {"en": "Your current recorded answer", "ar": "إجابتك الحالية المسجلة"}


def _start(page, base, lang):
    page.goto(base + "/")
    if lang == "ar":
        page.get_by_role("button", name="العربية", exact=True).click()
    page.fill("#idea", IDEA[lang])
    page.click("main input[type=submit], main button[type=submit]")
    page.wait_for_load_state()
    for _ in range(3):
        if "/session/" in page.url:
            break
        choice = page.locator('input[type=radio][name=domain_choice][value="mechanical"]')
        if choice.count():
            choice.check()
        confirm = page.locator("input[type=checkbox][name=domain_confirm]")
        if confirm.count():
            confirm.check()
        page.click("main input[type=submit], main button[type=submit]")
        page.wait_for_load_state()
    assert "/session/" in page.url
    return page.url.rsplit("/session/", 1)[-1]


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_an_answer_with_explicit_dimensions_reaches_the_existing_fit_view(server, page, lang):
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    sid = _start(page, server, lang)
    expect(page.locator("[data-engineering-fit-link]")).to_have_count(0)      # before
    page.fill("#response", ANSWER[lang])
    page.locator("#answer-form button[type=submit]").click()
    page.wait_for_load_state()
    page.goto(f"{server}/session/{sid}")
    link = page.locator("[data-engineering-fit-link] a")
    expect(link).to_have_count(1)                                              # after
    link.click()
    page.wait_for_load_state()
    assert page.url.endswith(f"/session/{sid}/functional-configuration")
    view = page.locator("[data-engineering-fit-page]")
    assert view.get_attribute("dir") == ("rtl" if lang == "ar" else "ltr")
    expect(view.locator("h2").first).to_have_text(HEADING[lang])
    source = page.locator('[data-fit-original][data-fit-source="answer"]')
    expect(source).to_have_text(ANSWER[lang])
    assert source.get_attribute("dir") == "auto"
    expect(page.locator("[data-fit-dimensions]")).to_contain_text("60 × 20")
    expect(page.locator("[data-fit-lift]")).to_contain_text("15")
    expect(page.locator("[data-fit-not-assessed]")).to_have_count(1)
    assert page.locator("form").count() == 0 or page.locator("input[value='60']").count() == 0
    _no_overflow(page, "[data-engineering-fit-page]")
    assert not errors, errors
