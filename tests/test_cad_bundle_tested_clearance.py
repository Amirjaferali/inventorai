# -*- coding: utf-8 -*-
"""CAD-BUNDLE-TESTED-CLEARANCE-01 — a CAD bundle a recipient can read on its own.

A recipient who has only the downloaded ZIP (no project screen, no PDF) can read,
without arithmetic, the minimum clearance the check tested on each side, the
outcome, each axis's nominal clearance (or overlap) on each side and how far it is
above or below the tested minimum, and that any constraint declared separately in
the project was not assessed. All values are the same revision-bound evaluation's
own exact text; geometry and the format version are unchanged.

Every bundle comes from the real download route. Synthetic board-and-enclosure data.
"""
import hashlib
import json

import pytest

from tests.test_board_enclosure_cad_download import _bundle, _check_geometry, _link
from tests.test_g1_linked_check_tested_clearance import ASKED, _check, _linked
from tests.test_g1_pcc_literal_source_aid import _submit, _url, client  # noqa: F401  (fixture)
from web import ui_text

FORMAT = "inventorai-planar-clearance-cad-handoff/1"
# the #982 case: board 84 x 50 in an 87 x 56 region, 1 mm tested; the inventor asked for 2 mm
README_982 = {
    "en": ["Result of this check: MET. Tested minimum clearance: 1 mm on each side of the board, on both axes.",
           "X axis: nominal clearance 1.5 mm on each side, 0.5 mm above the tested minimum.",
           "Y axis: nominal clearance 3 mm on each side, 2 mm above the tested minimum."],
    "ar": ["نتيجة هذا الفحص: متحقق (MET). الحد الأدنى المختبَر للخلوص: 1 mm على كل جانب من اللوحة، على المحورين كليهما.",
           "المحور X: الخلوص الاسمي 1.5 mm على كل جانب، أي أعلى من الحد الأدنى المختبَر بمقدار 0.5 mm.",
           "المحور Y: الخلوص الاسمي 3 mm على كل جانب، أي أعلى من الحد الأدنى المختبَر بمقدار 2 mm."],
}
# the companion fields that existed before this change; none changes meaning
PRE_EXISTING_AXIS_KEYS = {"axis", "margin_mm", "met", "conditional_min_region_mm",
                          "conditional_additional_mm", "conditional_min_region_enterable"}


def _download(c, sid, ifc):
    url = _link(c.get(_url(sid, ifc)).get_data(as_text=True))
    assert url, "the eligible page offers the download"
    files, _zf = _bundle(c.get(url))
    return url, files, json.loads(files["companion.json"]), files["README.txt"].decode("utf-8")


def _axes(comp):
    return [(a["axis"], a["nominal_clearance_each_side_mm"], a["overlap_each_side_mm"], a["margin_mm"], a["met"])
            for a in comp["evaluation"]["axes"]]


def _bound(url, files, comp, guide):
    """The existing revision-binding and DXF-hash checks, reused."""
    digest = hashlib.sha256(files["geometry.dxf"]).hexdigest()
    assert comp["dxf"]["sha256"] == digest and guide.count(digest) == 2
    assert comp["binding"]["snapshot_digest"] in url and comp["binding"]["declaration_revision_id"] in url
    assert _check_geometry(files["geometry.dxf"], comp["declared_values"]) == 0
    assert comp["handoff_format"] == FORMAT


# ── The #982 case: 1 mm tested, 2 mm asked ────────────────────────────────
def test_the_982_bundle_reads_without_arithmetic(client):
    sid, ifc, _ids, _cid = _linked(client, "en")
    url, files, comp, guide = _download(client, sid, ifc)
    _bound(url, files, comp, guide)
    ev = comp["evaluation"]
    assert ev["outcome"] == "MET" and ev["tested_min_clearance_each_side_mm"] == "1"
    assert comp["declared_values"]["c"] == "1"
    assert _axes(comp) == [("x", "1.5", None, "0.5", True), ("y", "3", None, "2", True)]
    defs = ev["axis_field_definitions"]
    assert "minus tested_min_clearance_each_side_mm" in defs["margin_mm"] and "signed" in defs["margin_mm"]
    assert "(region - board) / 2" in defs["nominal_clearance_each_side_mm"]
    assert "not assessed" in ev["outcome_meaning"]
    lines = guide.splitlines()
    for lang in ("en", "ar"):
        for line in README_982[lang]:
            assert line in lines, line
        assert ui_text.text("UI_PCC_CAD_SCOPE", lang) in lines
    # the result comes straight after the title, before the file guide
    assert lines[1:4] == README_982["en"]
    # the inventor's separate 2 mm constraint does not travel with the files
    blob = b"".join(files.values()).decode("utf-8", "replace")
    assert ASKED["en"] not in blob


# ── NOT MET, exactly-at and overlap ──────────────────────────────────────
@pytest.mark.parametrize("board, region, axes, x_line", [
    (("84", "50"), ("85", "56"), [("x", "0.5", None, "-0.5", False), ("y", "3", None, "2", True)],
     "X axis: nominal clearance 0.5 mm on each side, 0.5 mm below the tested minimum."),
    (("88", "50"), ("87", "56"), [("x", None, "0.5", "-1.5", False), ("y", "3", None, "2", True)],
     "X axis: no clearance; the board extends 0.5 mm beyond the region on each side, "
     "1.5 mm below the tested minimum."),
])
def test_not_met_and_overlap_are_stated_with_their_signed_margin(client, board, region, axes, x_line):
    sid, ifc, _ids = _check(client, "en", board=board, region=region)
    url, files, comp, guide = _download(client, sid, ifc)
    _bound(url, files, comp, guide)
    assert comp["evaluation"]["outcome"] == "NOT_MET"
    assert _axes(comp) == axes
    lines = guide.splitlines()
    assert ("Result of this check: NOT MET. Tested minimum clearance: 1 mm on each side of the board, "
            "on both axes.") in lines
    assert x_line in lines
    # the DXF still carries the DECLARED outlines, never a corrected or minimum region
    assert comp["declared_values"]["region_x"] == region[0] and comp["declared_values"]["board_x"] == board[0]


def test_a_margin_of_zero_is_exactly_the_tested_minimum(client):
    sid, ifc, _ids = _check(client, "en", region=("86", "56"))
    _url_, _files, comp, guide = _download(client, sid, ifc)
    assert comp["evaluation"]["outcome"] == "MET"
    assert _axes(comp)[0] == ("x", "1", None, "0", True)
    assert "X axis: nominal clearance 1 mm on each side, exactly the tested minimum." in guide.splitlines()


# ── Revision binding: a corrected check never reuses the old numbers ──────
def test_a_corrected_check_states_its_own_tested_minimum(client):
    sid, ifc, ids, _cid = _linked(client, "en")
    old_url, _f, old_comp, _g = _download(client, sid, ifc)
    assert _submit(client, sid, ifc, ids, "84", "50", "Re-measured",
                   extra={"value_region_x": "90", "value_region_y": "60", "value_c": "2"}).status_code == 200
    url, files, comp, guide = _download(client, sid, ifc)
    _bound(url, files, comp, guide)
    assert comp["binding"]["declaration_revision_no"] == old_comp["binding"]["declaration_revision_no"] + 1
    assert comp["evaluation"]["tested_min_clearance_each_side_mm"] == "2"
    assert _axes(comp) == [("x", "3", None, "1", True), ("y", "5", None, "3", True)]
    assert ("Result of this check: MET. Tested minimum clearance: 2 mm on each side of the board, "
            "on both axes.") in guide.splitlines()
    assert client.get(old_url).status_code == 409          # the old link yields no file


# ── Format: additive within /1 ───────────────────────────────────────────
def test_the_additions_keep_every_existing_field_and_the_format(client):
    sid, ifc, _ids, _cid = _linked(client, "en")
    _u, _files, comp, _guide = _download(client, sid, ifc)
    assert comp["handoff_format"] == FORMAT
    for axis in comp["evaluation"]["axes"]:
        assert PRE_EXISTING_AXIS_KEYS <= set(axis)
    # the existing reader fields keep their values (verify_product_bundles.py reads these)
    assert [a["margin_mm"] for a in comp["evaluation"]["axes"]] == ["0.5", "2"]
    for n in range(1, 9):
        for lang in ("en", "ar"):
            assert ui_text.text("UI_PCC_CAD_GUIDE_%d" % n, lang) in _guide
