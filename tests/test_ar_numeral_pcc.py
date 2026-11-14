# -*- coding: utf-8 -*-
"""AR-NUMERAL-PCC-01 — Arabic-Indic and Persian digits in the board-enclosure planar-clearance journey.

Synthetic data only. Method contract §§5A, 6 and 14 as amended. What is pinned:
  * ONE boundary step (``web.planar_clearance.ascii_digits``): Arabic-Indic (٠-٩) and Persian (۰-۹) digits
    become the ASCII digits of the same value, one for one; a text whose digits come from more than one
    system is refused; every other character is left exactly as it is, so the method's UNCHANGED strict
    ASCII grammar still decides (the Arabic decimal mark ٫, grouping marks, signs, units and words stay
    refused); an ASCII-only text is returned unchanged;
  * the method grammar itself is untouched: ``parse_value`` still refuses every non-ASCII digit;
  * the frozen twin pack: each admitted Arabic entry saves the SAME canonical ASCII value and renders the
    SAME outcome, margins and region bound as its ASCII twin; the same declaration typed in either digit
    system is one declaration (no new revision); correction and withdrawal take native digits through the
    unchanged paths; the CAD reference download is identical;
  * the frozen negative pack is refused with nothing written, and the refused entry is shown back verbatim;
  * the literal board-dimension aid: ``A x B mm`` or ``A x B ملم`` with each number in ONE digit system;
    the sentence and the expression stay verbatim, the proposed values are the canonical ASCII decimals,
    and an idea and an answer that state the same numbers in different digit systems do not conflict.
"""
import html as _html
import io
import json
import re
import zipfile
from types import SimpleNamespace

import pytest

import web.app as appmod
from engine import mechanical_planar_clearance as pcc
from engine import idea_state as _ledger
from tests.test_board_enclosure_cad_download import _link, _outlines
from tests.test_board_enclosure_planar_clearance import (  # noqa: F401  (fixture)
    _fields, _margin_cells, _outcome, _page, _save, _web, client)
from tests.test_g1_pcc_literal_source_aid import (
    _aid_chunk, _body, _project, _submit, _url)
from web import planar_clearance as view
from web import ui_text

# ==========================================================================
# The frozen acceptance pack (written with the increment, not tuned to it)
# ==========================================================================
# (entered text, canonical ASCII text) - admitted single values
ADMITTED = [
    ("٨٤", "84"), ("۸۴", "84"), ("٨٤.٥", "84.5"), ("۸۴.۵", "84.5"), ("٠٨٤", "084"),
    ("٩٩٩٩٩٩.٩٩٩٩", "999999.9999"), ("٠.٠٠٠١", "0.0001"), ("١٢٣٤٥٦", "123456"),
]
# full five-value rows (board_x, board_y, region_x, region_y, c) and their ASCII twins
ROW_TWINS = [
    (("٨٤", "٥٠", "٨٦", "٥٦", "٢"), ("84", "50", "86", "56", "2")),          # NOT MET
    (("۸۴.۵", "۵۰", "۹۰", "۶۰", "۰"), ("84.5", "50", "90", "60", "0")),      # MET, zero clearance
    (("٨٤", "50", "٩٠", "56", "2"), ("84", "50", "90", "56", "2")),          # one kind per number
    (("١٠٠.١", "٥٠", "١٠٠.١", "٥٤", "٠"), ("100.1", "50", "100.1", "54", "0")),  # MET on equality
]
# refused board_x entries: mixed systems, Arabic decimal / grouping marks, signs, units, words,
# grammar limits, other digit systems
REFUSED = [
    "8٤", "٨۴", "٨٤.5", "٨٤٫٥", "84٫5", "٨٤,٥", "٨٤،٥", "١٬٠٠٠", "−٨٤", "-٨٤", "+٨٤",
    "٨٤ ملم", "٨٤ملم", "٨٤مم", "٨٤ mm", "٨٤.", ".٥", "٫٥", "١٢٣٤٥٦٧", "٨٤.١٢٣٤٥", "٨ ٤",
    "٨e٢", "٠", "٠.٠", "ثمانون", "８４", "८४", "٨٤/٢",
]

_RESULT_CELLS = re.compile(
    r"data-pcc-(margin|bound-min|bound-additional|tested-value|side)\b[^>]*>([^<]*)<")


def _result_cells(body):
    return _RESULT_CELLS.findall(body)


def _current(sid, ifc):
    return appmod._get_store().load_planar_clearance(sid)["ledger"].active_for(ifc)


# ==========================================================================
# 1. the boundary step itself
# ==========================================================================
@pytest.mark.parametrize("text,canonical", ADMITTED)
def test_b01_native_digits_map_one_for_one(text, canonical):
    assert view.ascii_digits(text) == canonical
    assert pcc.parse_value(canonical) is not None


def test_b02_every_digit_of_both_systems_maps_to_its_value():
    assert view.ascii_digits("٠١٢٣٤٥٦٧٨٩") == "0123456789"
    assert view.ascii_digits("۰۱۲۳۴۵۶۷۸۹") == "0123456789"


@pytest.mark.parametrize("text", ["8٤", "٨۴", "٨٤.5", "۸4", "1٢٣"])
def test_b03_mixed_digit_systems_are_refused(text):
    assert view.ascii_digits(text) is None


@pytest.mark.parametrize("text", ["٨٤٫٥", "١٬٠٠٠", "٨٤،٥", "−٨٤", "٨٤ ملم", "٨e٢", "८४", "８４"])
def test_b04_nothing_but_digits_is_rewritten(text):
    out = view.ascii_digits(text)
    assert len(out) == len(text)
    for before, after in zip(text, out):
        assert before == after or (before in "٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹" and after in "0123456789")
    assert pcc.parse_value(out) is None                       # the unchanged grammar still refuses


@pytest.mark.parametrize("text", ["84", "84.5", "", "abc", "84 mm", "1,5", "-1"])
def test_b05_an_ascii_text_is_returned_unchanged(text):
    assert view.ascii_digits(text) is text


@pytest.mark.parametrize("value", [None, 84, 84.5, b"84"])
def test_b06_a_non_text_is_refused(value):
    assert view.ascii_digits(value) is None


def test_b07_the_method_grammar_is_untouched():
    for text in ("٨٤", "۸۴", "١٢"):
        assert pcc.parse_value(text) is None and not pcc.is_admitted_value("board_x", text)
    source = open(pcc.__file__, encoding="utf-8").read()
    assert "ascii_digits" not in source and not re.search(r"[٠-٩۰-۹]", source)


# ==========================================================================
# 2. the form: twins, refusals, one declaration, lifecycle, CAD
# ==========================================================================
@pytest.mark.parametrize("native,ascii_", ROW_TWINS)
def test_f01_a_native_row_saves_and_renders_exactly_like_its_ascii_twin(client, native, ascii_):
    sid_a, ifc_a, ids_a = _web(client)
    r_a = _save(client, sid_a, ifc_a, ids_a, values=native)
    sid_b, ifc_b, ids_b = _web(client)
    r_b = _save(client, sid_b, ifc_b, ids_b, values=ascii_)
    assert r_a.status_code == r_b.status_code == 200
    body_a, body_b = r_a.get_data(as_text=True), r_b.get_data(as_text=True)
    assert _outcome(body_a) == _outcome(body_b) and _outcome(body_a)[0] in ("MET", "NOT_MET")
    assert _margin_cells(body_a) == _margin_cells(body_b)
    assert _result_cells(body_a) == _result_cells(body_b)
    assert _current(sid_a, ifc_a).current.values == ascii_ == _current(sid_b, ifc_b).current.values


@pytest.mark.parametrize("bad", REFUSED)
def test_f02_refused_entries_write_nothing_and_are_shown_back_verbatim(client, bad):
    sid, ifc, ids = _web(client)
    r = _save(client, sid, ifc, ids, values=(bad, "50", "86", "56", "2"))
    assert r.status_code == 400
    body = r.get_data(as_text=True)
    assert ui_text.text("UI_PCC_MSG_REJECTED", "en") in _html.unescape(body)
    assert appmod._get_store().load_planar_clearance(sid)["ledger"].records == ()
    field = re.search(r'<input type="text" id="pcc-v-board_x"[^>]*>', body).group(0)
    assert 'value="%s"' % _html.escape(bad, quote=True) in field


def test_f03_the_same_numbers_in_another_digit_system_are_the_same_declaration(client):
    sid, ifc, ids = _web(client)
    assert _save(client, sid, ifc, ids, values=("٨٤", "٥٠", "٩٠", "٥٦", "٢")).status_code == 200
    r = _save(client, sid, ifc, ids, values=("84", "50", "90", "56", "2"))
    assert ui_text.text("UI_PCC_MSG_UNCHANGED", "en") in _html.unescape(r.get_data(as_text=True))
    record = _current(sid, ifc)
    assert len(record.revisions) == 1 and record.current.values == ("84", "50", "90", "56", "2")


def test_f04_an_exact_retry_of_a_native_submission_writes_nothing(client):
    sid, ifc, ids = _web(client)
    page = _page(client, sid, ifc)
    values = ("٨٤", "٥٠", "٩٠", "٥٦", "٢")
    assert _save(client, sid, ifc, ids, values=values, page=page).status_code == 200
    assert _save(client, sid, ifc, ids, values=values, page=page).status_code == 200
    assert len(_current(sid, ifc).revisions) == 1


def test_f05_correction_and_withdrawal_take_native_digits_through_the_unchanged_paths(client):
    sid, ifc, ids = _web(client)
    _save(client, sid, ifc, ids, values=("84", "50", "86", "56", "2"))
    r = _save(client, sid, ifc, ids, values=("٨٤", "٥٠", "٩٠", "٥٦", "٢"))
    assert r.status_code == 200 and _outcome(r.get_data(as_text=True)) == ["MET"]
    record = _current(sid, ifc)
    assert len(record.revisions) == 2 and record.current.values == ("84", "50", "90", "56", "2")
    data = _fields(_page(client, sid, ifc).get_data(as_text=True), form="data-pcc-withdraw-form")
    data["withdraw_confirm"] = "yes"
    r = client.post("/session/%s/interface-clearance/%s/withdraw" % (sid, ifc), data=data)
    assert "Withdrawn." in r.get_data(as_text=True)
    assert _current(sid, ifc) is None


def test_f06_the_cad_reference_download_is_identical(client):
    """Same geometry and the same declared values and evaluation; only the project-specific identities,
    snapshot digest and generation time differ (as for any two projects)."""
    bundles = []
    for values in (("٨٤", "٥٠", "٩٠", "٥٦", "٢"), ("84", "50", "90", "56", "2")):
        sid, ifc, ids = _web(client)
        url = _link(_save(client, sid, ifc, ids, values=values).get_data(as_text=True))
        assert url
        resp = client.get(url)
        assert resp.status_code == 200
        zf = zipfile.ZipFile(io.BytesIO(resp.data))
        bundles.append((zf.read("geometry.dxf"), json.loads(zf.read("companion.json"))))
    (dxf_a, comp_a), (dxf_b, comp_b) = bundles
    assert _outlines(dxf_a)[1] == _outlines(dxf_b)[1]
    lines_a, lines_b = dxf_a.decode("utf-8").splitlines(), dxf_b.decode("utf-8").splitlines()
    assert len(lines_a) == len(lines_b)
    # every differing line is one of the project-specific identities, both sides, nothing else
    identity = re.compile(r"pc[dr]-[0-9a-f]{32}|\{[0-9A-F]{8}(?:-[0-9A-F]{4}){3}-[0-9A-F]{12}\}|[0-9a-f]{16}"
                          r"|\d+\.\d+\.\d+ @ \d{4}-\d\d-\d\dT[\d:.]+\+00:00"
                          # the DXF creation / update date as a Julian day (24xxxxx.f): generation time, never
                          # a coordinate (at most six integer digits; the geometry is compared above)
                          r"|24\d{5}\.\d+")
    differing = [(a, b) for a, b in zip(lines_a, lines_b) if a != b]
    assert differing and all(identity.fullmatch(a) and identity.fullmatch(b) for a, b in differing)
    for key in comp_a:
        if key not in ("binding", "dxf", "generated_at"):
            assert comp_a[key] == comp_b[key], key
    assert comp_a["declared_values"] == comp_b["declared_values"]


def test_f07_the_arabic_page_explains_the_admitted_digits(client):
    sid, ifc, _ids = _web(client)
    body = _html.unescape(_page(client, sid, ifc, lang="ar").get_data(as_text=True))
    help_ar = ui_text.text("UI_PCC_DIGITS_HELP", "ar")
    assert help_ar in body
    for token in ("0–9", "٠–٩", "۰–۹", "٫", "يُرفض"):
        assert token in help_ar
    for lang in ("en", "ar"):
        assert "۰–۹" in ui_text.text("UI_PCC_MSG_REJECTED", lang)
        assert "٠–٩" in ui_text.text("UI_PCC_DIGITS_HELP", lang)


# ==========================================================================
# 3. the literal board-dimension aid
# ==========================================================================
@pytest.mark.parametrize("idea,first,second,span", [
    ("اللوحة مقاسها ٨٥ × ٥٦ ملم.", "85", "56", "٨٥ × ٥٦ ملم"),
    ("مقاس اللوحة ٨٥.٥ × ٥٦ ملم", "85.5", "56", "٨٥.٥ × ٥٦ ملم"),
    ("اللوحة: ۸۵ × ۵۶ mm.", "85", "56", "۸۵ × ۵۶ mm"),
    ("اللوحة مقاسها 85 × 56 ملم.", "85", "56", "85 × 56 ملم"),
    ("لوحة بمقاس ٨٥×٥٦ملم.", "85", "56", "٨٥×٥٦ملم"),
    ("An ٨٥ x ٥٦ mm board.", "85", "56", "٨٥ x ٥٦ mm"),
])
def test_a01_native_digits_and_the_arabic_unit_are_located_verbatim(idea, first, second, span):
    pair = view.literal_board_pair(idea)
    assert pair is not None
    assert (pair["first"], pair["second"], pair["span"], pair["unit"]) == (first, second, span, "mm")
    assert pair["passage"] in idea and span in pair["passage"]


@pytest.mark.parametrize("idea,twin", [
    ("اللوحة مقاسها ٨٥ × ٥٦ ملم.", "اللوحة مقاسها 85 × 56 mm."),
    ("My board is ۸۵ x ۵۶ mm.", "My board is 85 x 56 mm."),
])
def test_a02_a_native_idea_proposes_the_same_values_as_its_ascii_twin(idea, twin):
    a, b = view.literal_board_pair(idea), view.literal_board_pair(twin)
    assert (a["first"], a["second"]) == (b["first"], b["second"])
    assert view.aid_assignment(a, "first_y") == view.aid_assignment(b, "first_y")


@pytest.mark.parametrize("idea", [
    "اللوحة مقاسها 8٥ × ٥٦ ملم.",            # mixed digits in one number
    "اللوحة مقاسها ٨٥.5 × ٥٦ ملم.",
    "اللوحة مقاسها ٨٥٫٥ × ٥٦ ملم.",          # Arabic decimal mark
    "اللوحة مقاسها ٨٥,٥ × ٥٦ ملم.",
    "اللوحة مقاسها ٨٥ × ٥٦ مم.",             # another Arabic unit spelling
    "اللوحة مقاسها ٨٥ × ٥٦ ملمتر.",          # ملم starts a longer word
    "اللوحة مقاسها ٨٥ × ٥٦ ملمًا.",
    "اللوحة مقاسها ٨٥ × ٥٦ سم.",
    "اللوحة مقاسها تقريبًا ٨٥ × ٥٦ ملم.",     # the unchanged stop list
    "ربما اللوحة ٨٥ × ٥٦ ملم.",
    "اللوحة مقاسها ٨٥ × ٥٦ ملم، وممكن تتغير.",  # the unchanged suffix rule
    "اللوحة مقاسها ٨٥ × ٥٦ ملم والعلبة ١٢٠ × ٨٠ ملم.",
    "مقاس اللوحة ٨٥ × ٥٦ ملم. مقاس العلبة ١٢٠ × ٨٠ ملم.",
    "البطارية ٨٥ × ٥٦ ملم.",                 # not bound to the board
    "اللوحة مقاسها ٠ × ٥٦ ملم.",             # the dimension grammar (strictly positive)
    "اللوحة مقاسها ١٢٣٤٥٦٧ × ٥٦ ملم.",
])
def test_a03_everything_outside_the_bounded_scope_is_still_refused(idea):
    assert view.literal_board_pair(idea) is None


def test_a04_an_idea_and_an_answer_in_different_digit_systems_do_not_conflict():
    answer = SimpleNamespace(superseded_by=None, provenance=_ledger.OWNER_STATED,
                             disposition=_ledger.DISPOSITION_ANSWERED,
                             content="My board is 56 x 85 mm.")
    pair = view.current_board_pair("اللوحة مقاسها ٨٥ × ٥٦ ملم.", [answer])
    assert pair is not None and "conflict" not in pair
    assert pair["source"] == view.AID_SOURCE_IDEA and pair["span"] == "٨٥ × ٥٦ ملم"
    other = SimpleNamespace(superseded_by=None, provenance=_ledger.OWNER_STATED,
                            disposition=_ledger.DISPOSITION_ANSWERED,
                            content="My board is 56 x 86 mm.")
    assert view.current_board_pair("اللوحة مقاسها ٨٥ × ٥٦ ملم.", [other]) == {"conflict": True}


def test_a05_the_note_quotes_the_expression_verbatim_and_states_the_entered_values():
    pair = view.literal_board_pair("اللوحة مقاسها ٨٥ × ٥٦ ملم.")
    assert view.aid_note(pair, "first_x", "ar") == \
        "من فكرتي الأصلية: «٨٥ × ٥٦ ملم»؛ أدخلتُ 85 لـ X و56 لـ Y للوحة."
    assert view.aid_note(pair, "first_y", "en") == \
        "From my original idea: “٨٥ × ٥٦ ملم”; I entered 56 as board X and 85 as board Y."


def test_a06_the_arabic_page_shows_the_passage_verbatim_and_saves_the_ascii_values(client):
    idea = "حوض نباتات ذكي يفتح غطاءه على مفصّلة عندما تجف التربة. مقاس اللوحة ٨٥ × ٥٦ ملم."
    sid, ifc, ids = _project(client, idea, lang="ar")
    body = _body(client.get(_url(sid, ifc)))
    chunk = _aid_chunk(body)
    assert chunk is not None
    passage = _html.unescape(re.search(r"data-pcc-aid-passage>(.*?)</blockquote>", chunk, re.S).group(1))
    assert passage == "مقاس اللوحة ٨٥ × ٥٦ ملم"
    assert 'data-pcc-aid-first>85</bdi>' in chunk and 'data-pcc-aid-second>56</bdi>' in chunk
    note = view.aid_note(view.literal_board_pair(idea), "first_x", "ar")
    assert _html.escape(note, quote=True) in chunk
    r = _submit(client, sid, ifc, ids, "85", "56", note)
    assert r.status_code == 200
    current = _current(sid, ifc).current
    assert current.values_map()["board_x"] == "85" and current.basis_map()["basis_board"] == note
    seed = appmod._get_store()._conn.execute(
        "SELECT seed_idea_text FROM projects WHERE project_id = ?", (sid,)).fetchone()
    assert seed is not None and seed[0] == idea                # the original idea is kept verbatim
