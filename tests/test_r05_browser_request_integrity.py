"""Real Chromium form callers, including a separate-origin form forgery."""
import pickle
import threading

import pytest
from flask import Flask
from werkzeug.serving import make_server

import web.app as webapp
from tests.test_draft_l2_local_continuity import server, _browser, page


@pytest.fixture
def foreign_origin(server):
    attacker = Flask("r05_foreign_form")

    @attacker.get("/")
    def form():
        return ('<form method="POST" action="' + server + '/decision-workspace">'
                '<button type="submit">Submit foreign form</button></form>')

    # Different port = different origin, same site = SameSite is not the defense.
    http = make_server("127.0.0.1", 0, attacker, threaded=False)
    thread = threading.Thread(target=http.serve_forever, daemon=True)
    thread.start()
    try:
        yield "http://127.0.0.1:" + str(http.server_port)
    finally:
        http.shutdown()
        thread.join(timeout=5)
        http.server_close()
        assert not thread.is_alive()


def test_foreign_form_rejected_with_victim_cookie_present_then_real_form_succeeds(server, foreign_origin, page):
    page.goto(server + "/decision-workspace")
    csrf = page.locator('main input[name="csrf_token"]').input_value()
    before = pickle.dumps((webapp.FDC001_DECISIONS, webapp.FDC001_DECISION_OWNERS))
    page.goto(foreign_origin)
    with page.expect_response(server + "/decision-workspace") as response_info:
        page.get_by_role("button", name="Submit foreign form").click()
    response = response_info.value
    assert response.status == 403
    assert "session=" in response.request.all_headers().get("cookie", "")
    assert csrf not in (response.request.post_data or "")
    assert pickle.dumps((webapp.FDC001_DECISIONS, webapp.FDC001_DECISION_OWNERS)) == before
    page.goto(server + "/decision-workspace")
    page.get_by_role("button", name="Create a decision workspace").click()
    page.wait_for_url(server + "/decision-workspace/*")
    assert pickle.dumps((webapp.FDC001_DECISIONS, webapp.FDC001_DECISION_OWNERS)) != before


def test_arabic_language_post_and_token_not_in_local_draft(server, page):
    page.goto(server + "/")
    csrf = page.locator('main input[name="csrf_token"]').input_value()
    page.get_by_role("button", name="العربية", exact=True).click()
    assert page.locator("html").get_attribute("dir") == "rtl"
    assert page.locator("html").get_attribute("lang") == "ar"
    page.locator("#idea").fill("فكرة أولية لاختبار استعادة المسودة")
    page.locator("#idea").dispatch_event("input")
    page.wait_for_timeout(1100)  # existing 800ms local-draft debounce
    storage = page.evaluate("JSON.stringify(localStorage)")
    assert "csrf_token" not in storage and csrf not in storage
    assert csrf not in page.url
