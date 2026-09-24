"""UQTR-01 Step 2B — target-aware binding in real Chromium (EN + AR).

Two real tabs of one browser context submit the real rendered answer form.
The ABA scenario is driven entirely through the UI: tab B keeps a Q1 form,
tab A answers and the journey leaves Q1, tab A withdraws that answer through
the existing correction form so the SAME Q1 is current again, and tab B's old
form is then refused with the bilingual stale-form message — nothing saved,
the refused text not carried over, RTL intact — while a fresh form succeeds.
Synthetic invention text only; no human-usability claim.
"""
import os

import pytest

import web.app as webapp
from engine.record_store import SqliteRecordStore
from web.ui_text import RVR7_EXHAUSTED_EXIT_PROMPT, text
from tests.test_draft_l2_local_continuity import server, page, _browser, _start  # noqa: F401

SEED = ("An electronic heater cutoff uses a temperature sensor and a relay circuit "
        "so that when the room gets too warm the relay switches the heater off.")
WEAK = "I think it works somehow."
ANSWER = ("The temperature sensor output is compared with a set threshold; when "
          "the room is too warm the comparator switches the relay and the relay "
          "cuts power to the heater until the room cools down again.")
CLOSING = ("A thermistor in a voltage divider feeds a comparator with hysteresis; "
           "the comparator output drives a transistor that energises the relay "
           "coil, and the relay contacts open the heater supply line when the "
           "measured temperature passes the set point, closing again once it "
           "falls below the lower threshold.")
TAB_B = "Tab B typed this into the old form; it must not be saved anywhere."


def _submit(tab, value):
    tab.locator("#response").fill(value)
    tab.locator('#answer-form button[type="submit"]').click()
    tab.wait_for_load_state()


def _identity(sid):
    entry = webapp.SESSION_STORE[sid]
    return webapp._resolve_question_context(
        entry["state"], entry.get("last_result")).identity


def _durable(sid):
    # The app's store is bound to the server thread; read through our own.
    store = SqliteRecordStore(os.environ["INVENTORAI_DB_PATH"])
    try:
        return list(store.load_contract(sid).assertions)
    finally:
        store.close()


def _durable_count(sid):
    return len(_durable(sid))


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_two_tab_aba_stale_form_refused_then_fresh_form_succeeds(server, page, lang):
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    if lang == "ar":
        page.goto(server)
        page.get_by_role("button", name="العربية", exact=True).click()
    sid = _start(page, server, idea=SEED)
    for i in range(5):
        _submit(page, "%s %d" % (WEAK, i))
    _submit(page, ANSWER)
    assert _identity(sid) == RVR7_EXHAUSTED_EXIT_PROMPT
    # Tab B opens the same Q1 page and keeps its form.
    tab_b = page.context.new_page()
    tab_b.goto(page.url)
    q1_target = tab_b.locator('#answer-form input[name="answer_target"]').input_value()
    assert q1_target
    # Tab A answers; the journey leaves Q1.
    page.reload()
    _submit(page, CLOSING)
    assert _identity(sid) != RVR7_EXHAUSTED_EXIT_PROMPT
    # Tab A withdraws that answer through the existing correction form: the
    # replay makes the SAME Q1 current again.
    page.locator("details.correct-answer > summary").click()
    select = page.locator("#correct-target")
    select.select_option(select.locator("option").last.get_attribute("value"))
    page.locator("#correct-response").fill(WEAK + " (withdrawn)")
    page.locator('.correct-answer form button[type="submit"]').click()
    page.wait_for_load_state()
    assert _identity(sid) == RVR7_EXHAUSTED_EXIT_PROMPT
    page.reload()
    fresh_target = page.locator('#answer-form input[name="answer_target"]').input_value()
    # Same signed Q1 context payload (kind, identity, gap, ECV); only the
    # binding to the rotated answer token differs...
    assert fresh_target.rpartition(".")[0] == q1_target.rpartition(".")[0]
    assert fresh_target != q1_target
    n = _durable_count(sid)
    # ...yet tab B's original form is refused: nothing saved, text not carried.
    _submit(tab_b, TAB_B)
    assert _durable_count(sid) == n
    alert = tab_b.locator("#answer-error")
    assert alert.get_attribute("role") == "alert"
    assert alert.text_content() == text("UI_UQTR_FORM_STALE", lang)
    # Never transferred to the current question: the server renders it nowhere
    # and the answer box stays empty. The ONLY place it may appear is the
    # existing, unchanged Draft-L2 client-side recovery OFFER for this same
    # question context (local to this device, applied only on an explicit
    # Restore click) — it is not saved and not auto-applied.
    assert tab_b.locator("#response").input_value() == ""
    assert TAB_B not in tab_b.request.get(page.url).text()
    dom = tab_b.content()
    offer = tab_b.locator(".draft-recovery")
    if TAB_B in dom:
        assert offer.count() == 1 and TAB_B in offer.inner_html()
        assert dom.replace(offer.evaluate("e => e.outerHTML"), "").count(TAB_B) == 0
    assert tab_b.locator("html").get_attribute("lang") == lang
    assert tab_b.locator("html").get_attribute("dir") == ("rtl" if lang == "ar" else None)
    assert tab_b.evaluate("document.documentElement.scrollWidth <= innerWidth")
    # The refusal re-rendered a FRESH form in tab B; it succeeds normally.
    _submit(tab_b, CLOSING + " Checked again.")
    assert _durable_count(sid) == n + 1
    last = _durable(sid)[-1]
    assert (last.content, last.question_target) == (
        CLOSING + " Checked again.", RVR7_EXHAUSTED_EXIT_PROMPT)
    assert tab_b.locator("#answer-error").count() == 0
    assert not errors
