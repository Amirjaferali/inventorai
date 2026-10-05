"""Stage 35 — Structured Invention Disclosure Export — first bounded slice —
routes and journey (BASE RED, file W).

Implementation contract §4, §12.5, §13 and §14 #2, #5, #6e, #10, #15, #23, #26:
one account-page entry link, one pre-download page and two local downloads for
the signed-in durable owner of ONE project; byte-identical non-enumerating
denials; a bare empty 503 for every refusal; nothing retained or mutated.
"""
import json
import os
import re
import sqlite3

import pytest

import web.app as webapp
from engine import disclosure_export as dx
from tests.csrf_client import csrf_client
from tests.test_stage19_durable_success_criteria import _client_for, _journey
from tests.test_stage35_disclosure_projection import DISCLAIMERS_EN, SCOPE_AR, SCOPE_EN
from tests.test_stage35_disclosure_html import AR_DISCLAIMERS
from web import ui_text

PAGE = "/account/projects/%s/disclosure-export"
JSON_URL = PAGE + "/json"
HTML_URL = PAGE + "/html"
HTML_CSP = "default-src 'none'; style-src 'unsafe-inline'; sandbox"


@pytest.fixture()
def owned():
    webapp.app.config["TESTING"] = True
    c, aid = _client_for("s35-route-owner@example.com")
    sid = _journey(c)
    return c, aid, sid


def _sig(r):
    return (r.status_code, r.headers.get("Location"), r.headers.get("Content-Type"), r.data)


def _dump():
    con = sqlite3.connect(os.environ["INVENTORAI_DB_PATH"])
    try:
        return list(con.iterdump())
    finally:
        con.close()


def _null_owner_project():
    with csrf_client(webapp.app) as anon:
        r = anon.post("/start", data={"idea": "A sensor circuit that cuts power when hot.",
                                      "domain_confirm": "electronics_electrical"})
        return r.headers["Location"].rsplit("/", 1)[-1]


# ===========================================================================
# entry and pre-download page
# ===========================================================================
def test_account_page_links_each_owned_project(owned):
    c, aid, sid = owned
    body = c.get("/account").get_data(as_text=True)
    assert 'href="%s"' % (PAGE % sid) in body
    assert ui_text.text("UI_S35_ACCOUNT_LINK", "en") in body


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_02_page_order_disclaimers_before_controls(owned, lang):
    c, aid, sid = owned
    if lang == "ar":
        c.post("/ui-language", data={"lang": "ar"})
    before = _dump()
    r = c.get(PAGE % sid)
    assert r.status_code == 200
    body = r.get_data(as_text=True)
    t = lambda k: ui_text.text(k, lang)
    esc = lambda s: s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;") \
        .replace("'", "&#39;").replace('"', "&#34;")
    order = [body.index(SCOPE_EN), body.index(esc(t("UI_S35_PAGE_INTRO"))),
             body.index(esc(t("UI_S35_NOTICES_HEADING")))]
    for n, en in enumerate(DISCLAIMERS_EN):
        order.append(body.index(en))
        if lang == "ar":
            order.append(body.index(AR_DISCLAIMERS[n]))
    order += [body.index('href="%s"' % (JSON_URL % sid)), body.index('href="%s"' % (HTML_URL % sid)),
              body.index(esc(t("UI_S35_SAME_DATA"))), body.index(esc(t("UI_S35_RETENTION_HEADING")))]
    for n in range(1, 5):
        order.append(body.index(esc(t("UI_S35_RETENTION_%d" % n))))
    assert order == sorted(order)
    assert esc(t("UI_S35_JSON_CONTROL")) in body and esc(t("UI_S35_HTML_CONTROL")) in body
    assert (SCOPE_AR in body) == (lang == "ar")
    assert _dump() == before                                   # viewing records nothing
    assert "<form" not in body.split(t("UI_S35_NOTICES_HEADING"))[1].split(
        t("UI_S35_RETENTION_HEADING"))[0]


# ===========================================================================
# downloads
# ===========================================================================
def test_15_json_download(owned):
    c, aid, sid = owned
    r = c.get(JSON_URL % sid)
    assert r.status_code == 200
    assert r.headers["Content-Type"] == "application/json; charset=utf-8"
    assert r.headers["Content-Disposition"] == \
        'attachment; filename="inventorai-disclosure-export-v1.json"'
    assert r.headers["Cache-Control"] == "no-store"
    assert r.headers["X-Content-Type-Options"] == "nosniff"
    assert not r.data.startswith(b"\xef\xbb\xbf")
    body = r.data.decode("utf-8")
    assert body.endswith("\n")
    doc = json.loads(body)
    assert set(doc) == {"content", "content_digest", "disclosure_schema_version",
                        "export_format_version", "generated_at"}
    assert doc["export_format_version"] == "inventorai-disclosure-json/1"
    assert doc["disclosure_schema_version"] == "inventorai-disclosure/1"
    assert doc["content_digest"] == dx.content_digest(doc["content"])
    assert body == dx.serialize_json(doc)
    assert sid not in body and aid not in body


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_15_html_download_same_data(owned, lang):
    c, aid, sid = owned
    if lang == "ar":
        c.post("/ui-language", data={"lang": "ar"})
    j = json.loads(c.get(JSON_URL % sid).data.decode("utf-8"))
    r = c.get(HTML_URL % sid)
    assert r.status_code == 200
    assert r.headers["Content-Type"] == "text/html; charset=utf-8"
    assert r.headers["Content-Disposition"] == \
        'attachment; filename="inventorai-disclosure-export-v1.html"'
    assert r.headers["Cache-Control"] == "no-store"
    assert r.headers["X-Content-Type-Options"] == "nosniff"
    assert r.headers["Content-Security-Policy"] == HTML_CSP
    body = r.data.decode("utf-8")
    assert j["content_digest"] in body
    assert "inventorai-disclosure-html/1" in body
    assert ('<html lang="ar" dir="rtl">' in body) == (lang == "ar")
    assert sid not in body and aid not in body


def test_10_no_mutation_and_no_retention(owned, tmp_path):
    c, aid, sid = owned
    before = _dump()
    files_before = sorted(os.listdir(os.path.dirname(os.environ["INVENTORAI_DB_PATH"])))
    for url in (PAGE, JSON_URL, HTML_URL):
        assert c.get(url % sid).status_code == 200
    assert _dump() == before
    assert sorted(os.listdir(os.path.dirname(os.environ["INVENTORAI_DB_PATH"]))) == files_before


def test_no_other_method(owned):
    c, aid, sid = owned
    for url in (PAGE, JSON_URL, HTML_URL):
        r = c.post(url % sid, data={})
        assert r.status_code != 200 and "Content-Disposition" not in r.headers


# ===========================================================================
# #5 / #26 — denial matrix and DENIAL versus REFUSAL
# ===========================================================================
@pytest.mark.parametrize("url", [PAGE, JSON_URL, HTML_URL])
def test_05_26_denials_are_byte_identical(owned, url, monkeypatch):
    c, aid, sid = owned
    other, _other_aid = _client_for("s35-route-other@example.com")
    missing = other.get(url % "no-such-project")
    foreign = other.get(url % sid)
    assert _sig(missing) == _sig(foreign)
    assert missing.status_code == 302 and missing.headers["Location"].endswith("/")
    with csrf_client(webapp.app) as anon:
        assert _sig(anon.get(url % sid)) == _sig(missing)
    assert _sig(c.get(url % _null_owner_project())) == _sig(missing)
    store = webapp._get_store()

    def lookup_fails(pid):
        raise sqlite3.OperationalError("disk I/O error")
    monkeypatch.setattr(store, "load_owner", lookup_fails)
    assert _sig(c.get(url % sid)) == _sig(missing)


@pytest.mark.parametrize("url", [JSON_URL, HTML_URL])
def test_26_post_authorization_failure_is_an_empty_503(owned, url, monkeypatch):
    c, aid, sid = owned
    store = webapp._get_store()

    def contract_fails(pid):
        raise sqlite3.DatabaseError("database disk image is malformed")
    monkeypatch.setattr(store, "load_contract", contract_fails)
    r = c.get(url % sid)
    assert (r.status_code, r.data) == (503, b"")
    assert "Content-Disposition" not in r.headers


# ===========================================================================
# #6e / #23 — every refusal is a bare empty 503
# ===========================================================================
@pytest.mark.parametrize("url", [JSON_URL, HTML_URL])
@pytest.mark.parametrize("method,error", [
    ("load_need_routing", sqlite3.OperationalError("no such table: x")),
    ("load_requirement_quantities", sqlite3.OperationalError("no such column: y")),
    ("load_success_criteria", sqlite3.DatabaseError("database disk image is malformed")),
    ("load_test_variables", sqlite3.IntegrityError("constraint failed")),
    ("load_interface_dependencies", sqlite3.Error("unclassified")),
    ("load_result_events", RuntimeError("unclassified exception")),
])
def test_06e_23_refusals_produce_no_file(owned, monkeypatch, url, method, error):
    c, aid, sid = owned
    store = webapp._get_store()

    def boom(*a, **kw):
        raise error
    monkeypatch.setattr(store, method, boom)
    r = c.get(url % sid)
    assert (r.status_code, r.data) == (503, b"")
    assert "Content-Disposition" not in r.headers


def test_06e_unsafe_connection_refuses(owned):
    c, aid, sid = owned
    store = webapp._get_store()
    store._connection_unsafe = True
    try:
        for url in (JSON_URL, HTML_URL):
            r = c.get(url % sid)
            assert (r.status_code, r.data) == (503, b"")
    finally:
        store._connection_unsafe = False


def test_page_post_authorization_failure_is_an_empty_503(owned, monkeypatch):
    c, aid, sid = owned
    store = webapp._get_store()
    monkeypatch.setattr(store, "load_contract",
                        lambda pid: (_ for _ in ()).throw(sqlite3.Error("x")))
    r = c.get(PAGE % sid)
    assert (r.status_code, r.data) == (503, b"")


def test_routes_add_no_api_surface():
    rules = {r.rule for r in webapp.app.url_map.iter_rules()}
    added = {r for r in rules if "disclosure" in r}
    assert added == {"/account/projects/<project_id>/disclosure-export",
                     "/account/projects/<project_id>/disclosure-export/json",
                     "/account/projects/<project_id>/disclosure-export/html"}
    for rule in webapp.app.url_map.iter_rules():
        if "disclosure" in rule.rule:
            assert rule.methods <= {"GET", "HEAD", "OPTIONS"}
    assert not any(r.startswith("/api") and "disclosure" in r for r in rules)
    src = open(dx.__file__, encoding="utf-8").read()
    assert not re.search(r"^\s*(import|from)\s+web\b", src, re.M)
