# -*- coding: utf-8 -*-
"""G1-2-LINKED-CHECK-TESTED-CLEARANCE-01 — what a linked clearance check tested.

A mandatory constraint linked to a saved planar clearance check now shows, beside
the check's own result, the per-side clearance that saved revision was tested
with (constraint block, report and PDF, EN / AR). The check page shows the
nominal clearance on each side and the margin above the tested clearance, so the
inventor need not add the numbers. The constraint text stays verbatim and its
fulfilment stays "not assessed". A link that is no longer CURRENT (check
corrected or withdrawn) or unreadable shows no tested value: never the newer
revision's numbers under an older link.

Synthetic board-and-enclosure data only.
"""
import html as _html
import re

import pytest

import web.app as appmod
from engine.record_store import ConstraintLinkCorrupt
from tests.test_board_enclosure_planar_clearance import _fields
from tests.test_g1_constraint_engineering_link import _block, _form, _page, _post, _status, PLAIN
from tests.test_g1_pcc_literal_source_aid import _body, _project, _submit, _url, client  # noqa: F401
from tests.test_mandatory_constraint_acceptance_preparation import _declare
from tests.test_stage15_interface_preparation import _pdf_source
from web import ui_text

ASKED = {"ar": "أحتاج إلى فراغ لا يقل عن 2 مم على كل جانب من اللوحة",
         "en": "I need at least 2 mm of free space on every side of the board"}
TESTED = {"ar": "الحدّ المختبَر في هذا الفحص: 1 مم على كل جانب — متحقق",
          "en": "Clearance tested in this check: 1 mm on each side — met"}


def _t(key, lang):
    return ui_text.text(key, lang)


def _plain(raw):
    raw = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", raw, flags=re.S)
    return " ".join(_html.unescape(re.sub(r"<[^>]+>", " ", raw)).split())


def _check(c, lang, board=("84", "50"), region=("87", "56"), clearance="1"):
    """A saved board-in-case clearance check with the inventor's own values."""
    sid, ifc, ids = _project(c, PLAIN, lang=lang)
    r = _submit(c, sid, ifc, ids, board[0], board[1], "Measured",
                extra={"value_region_x": region[0], "value_region_y": region[1], "value_c": clearance})
    assert r.status_code == 200
    return sid, ifc, ids


def _linked(c, lang, **values):
    sid, ifc, ids = _check(c, lang, **values)
    cid = _declare(c, sid, text=ASKED[lang])
    assert _post(c, sid, _form(c, sid, cid)).status_code == 302
    return sid, ifc, ids, cid


def _rows(page):
    """(axis, nominal clearance on each side, margin) of the check page's table."""
    out = []
    for row in re.findall(r'<tr data-pcc-axis="(\w)">(.*?)</tr>', page, re.S):
        side = re.search(r"data-pcc-side>([^<]*)<", row[1])
        overlap = re.search(r"data-pcc-overlap>.*?<bdi[^>]*>([^<]*)<", row[1], re.S)
        margin = re.search(r"data-pcc-margin>([^<]*)<", row[1])
        out.append((row[0], side.group(1) if side else ("overlap " + overlap.group(1)),
                    margin.group(1)))
    return out


# ── The 2 mm asked, 1 mm tested case ───────────────────────────────────────
@pytest.mark.parametrize("lang", ["ar", "en"])
def test_the_constraint_block_shows_the_tested_clearance_beside_the_result(client, lang):
    sid, _ifc, _ids, cid = _linked(client, lang)
    block = _block(_page(client, sid), cid)
    assert _status(block) == "CURRENT"
    text = " ".join(block.split())
    assert ASKED[lang] in text                                         # verbatim
    assert TESTED[lang] in _plain(block)
    assert _t("UI_CEL_RESULT_MET", lang) in text
    assert _t("UI_CEL_NOT_ASSESSED", lang) in text                     # still not assessed
    assert 'data-cel-tested="MET"' in block and "data-cel-tested-value>1<" in block


@pytest.mark.parametrize("lang", ["ar", "en"])
def test_the_report_and_pdf_show_the_same_line(client, monkeypatch, lang):
    sid, _ifc, _ids, _cid = _linked(client, lang)
    for body in (client.get("/session/%s/deliverable" % sid).get_data(as_text=True),
                 _pdf_source(client, sid, monkeypatch)):
        assert 'data-vp-cel-tested="MET"' in body
        assert TESTED[lang] in _plain(body)
        assert _t("UI_CEL_NOT_ASSESSED", lang) in _plain(body)


@pytest.mark.parametrize("lang", ["ar", "en"])
def test_the_check_page_shows_each_side_and_the_margin_above_it(client, lang):
    sid, ifc, _ids, _cid = _linked(client, lang)
    page = client.get(_url(sid, ifc)).get_data(as_text=True)
    assert re.search(r"data-pcc-tested-value>1 mm<", page)
    assert _rows(page) == [("x", "1.5 mm", "0.5 mm"), ("y", "3 mm", "2 mm")]
    text = _plain(page)
    for key in ("UI_PCC_TESTED_CLEARANCE", "UI_PCC_SIDE_GAP", "UI_PCC_MARGIN", "UI_PCC_MARGIN_EXPLAINED"):
        assert _t(key, lang) in text


# ── NOT MET and a board wider than the region ──────────────────────────────
@pytest.mark.parametrize("lang", ["ar", "en"])
def test_not_met(client, lang):
    sid, ifc, _ids, cid = _linked(client, lang, region=("85", "56"))
    block = _plain(_block(_page(client, sid), cid))
    assert (_t("UI_CEL_TESTED_LABEL", lang) + " 1 " + _t("UI_CEL_TESTED_UNIT", lang) + " — "
            + _t("UI_CEL_TESTED_NOT_MET", lang)) in block
    assert _t("UI_CEL_NOT_ASSESSED", lang) in block
    page = client.get(_url(sid, ifc)).get_data(as_text=True)
    assert _rows(page) == [("x", "0.5 mm", "-0.5 mm"), ("y", "3 mm", "2 mm")]


def test_a_board_wider_than_the_region_is_an_overlap_not_a_clearance(client):
    sid, ifc, _ids = _check(client, "ar", board=("88", "50"))
    page = client.get(_url(sid, ifc)).get_data(as_text=True)
    assert _rows(page) == [("x", "overlap 0.5 mm", "-1.5 mm"), ("y", "3 mm", "2 mm")]
    assert _t("UI_PCC_SIDE_OVERLAP", "ar") in _plain(page)


# ── Never a newer revision's numbers under an older link ───────────────────
def test_a_corrected_check_shows_no_tested_value_under_the_old_link(client):
    sid, ifc, ids, cid = _linked(client, "ar")
    assert _submit(client, sid, ifc, ids, "84", "50", "Re-measured",
                   extra={"value_region_x": "90", "value_region_y": "60", "value_c": "2"}).status_code == 200
    block = _block(_page(client, sid), cid)
    assert _status(block) == "EARLIER"
    assert "data-cel-tested" not in block
    assert _t("UI_CEL_TESTED_LABEL", "ar") not in block and _t("UI_CEL_NOT_ASSESSED", "ar") in block
    body = client.get("/session/%s/deliverable" % sid).get_data(as_text=True)
    assert "data-vp-cel-tested" not in body


def test_a_withdrawn_check_shows_no_tested_value(client):
    sid, ifc, _ids, cid = _linked(client, "ar")
    data = _fields(_body(client.get(_url(sid, ifc))), form="data-pcc-withdraw-form")
    data["withdraw_confirm"] = "yes"
    assert client.post(_url(sid, ifc) + "/withdraw", data=data).status_code == 200
    block = _block(_page(client, sid), cid)
    assert _status(block) == "EARLIER" and "data-cel-tested" not in block


def test_an_unreadable_link_or_check_shows_no_tested_value(client, monkeypatch):
    sid, _ifc, _ids, cid = _linked(client, "ar")

    def corrupt(_sid):
        raise ConstraintLinkCorrupt("bad")
    monkeypatch.setattr(appmod._get_store(), "load_constraint_engineering_links", corrupt)
    block = _block(_page(client, sid), cid)
    assert _status(block) == "UNAVAILABLE" and "data-cel-tested" not in block
    monkeypatch.undo()

    def broken(*_a, **_k):
        raise RuntimeError("unreadable")
    monkeypatch.setattr(appmod._pcc_view, "linked_check", broken)
    block = _block(_page(client, sid), cid)
    assert _status(block) == "UNAVAILABLE" and "data-cel-tested" not in block
