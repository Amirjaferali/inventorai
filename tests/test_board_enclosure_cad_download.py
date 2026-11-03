"""BOARD-ENCLOSURE-CAD-DOWNLOAD-01 — the outbound CAD reference download (method contract §10A).

Synthetic data only. What is pinned:
  * the bundle: exactly geometry.dxf, companion.json and README.txt at fixed paths; the companion bound to
    the exact DXF by SHA-256; the DXF read back INDEPENDENTLY (ezdxf's reader, exact Fraction reference
    from the declared decimal text): R2013, $INSUNITS = 4 (mm), two closed 4-vertex polylines on the two
    layers, centred and axis-aligned, the DECLARED values — never the conditional minimum;
  * the values: original decimal inputs, method / consequence versions, outcome, margins and bound copied
    from the existing method consumer; the 100.1 / 99.9 / 0.1 equality case keeps its exact MET;
  * the lifecycle: a correction gives a new revision and bundle while the earlier bundle keeps its own
    identity; a stale, duplicated or forged revision / digest, a missing, inapplicable, withdrawn,
    reconfirmation-needing or unavailable state, and a failed generation return the page with a notice
    and NO file; ONE snapshot read per download; nothing stored;
  * the boundaries: project authorization and foreign identities denied; no-store, nosniff, attachment;
    no server path or credential in the bundle; no macro or external reference; EN / AR copy.
"""
import hashlib
import html as _html
import io
import json
import re
import zipfile
from fractions import Fraction

import ezdxf
import pytest

import web.app as appmod
from engine import mechanical_planar_clearance as pcc
from engine import planar_clearance_cad_export as cad
from tests.csrf_client import csrf_client
from tests.test_board_enclosure_planar_clearance import (  # noqa: F401  (fixtures)
    APPLIES, _fields, _page, _save, _web, client)
from tests.test_component_inventory_correct_withdraw import _correct
from web import ui_text


def _link(body):
    m = re.search(r'href="([^"]*/cad\.zip\?[^"]*)" data-pcc-cad-link', body)
    return _html.unescape(m.group(1)) if m else None


def _download(c, sid, ifc, ids, values=("84", "50", "86", "56", "2")):
    body = _save(c, sid, ifc, ids, values=values).get_data(as_text=True)
    url = _link(body)
    assert url, "the eligible page offers the download"
    return url, c.get(url)


def _bundle(resp):
    assert resp.status_code == 200 and resp.mimetype == "application/zip"
    zf = zipfile.ZipFile(io.BytesIO(resp.data))
    assert zf.namelist() == ["geometry.dxf", "companion.json", "README.txt"]
    return {name: zf.read(name) for name in zf.namelist()}, zf


def _outlines(dxf_data):
    """Independent read-back: layer -> list of (x, y) vertices, plus the header."""
    doc = ezdxf.read(io.StringIO(dxf_data.decode("utf-8")))
    shapes = {}
    for entity in doc.modelspace():
        assert entity.dxftype() == "LWPOLYLINE", entity.dxftype()
        assert entity.closed
        shapes.setdefault(entity.dxf.layer, []).append([(p[0], p[1]) for p in entity.get_points()])
    return doc, shapes


def _check_geometry(dxf_data, declared):
    doc, shapes = _outlines(dxf_data)
    assert doc.dxfversion == "AC1027" and doc.header["$INSUNITS"] == 4
    assert doc.header["$MEASUREMENT"] == 1
    assert set(shapes) == {"IAI_DECLARED_USABLE_REGION", "IAI_DECLARED_BOARD_OUTLINE"}
    errors = []
    for layer, (w, h) in (("IAI_DECLARED_USABLE_REGION", (declared["region_x"], declared["region_y"])),
                          ("IAI_DECLARED_BOARD_OUTLINE", (declared["board_x"], declared["board_y"]))):
        assert len(shapes[layer]) == 1 and len(shapes[layer][0]) == 4
        xs = sorted({x for x, _ in shapes[layer][0]})
        ys = sorted({y for _, y in shapes[layer][0]})
        assert len(xs) == 2 and len(ys) == 2                       # axis-aligned rectangle
        hx, hy = Fraction(w) / 2, Fraction(h) / 2
        for got, want in ((xs[0], -hx), (xs[1], hx), (ys[0], -hy), (ys[1], hy)):
            errors.append(abs(Fraction(got) - want))               # transfer error, measured
    return max(errors)


# ==========================================================================
# 1. the bundle
# ==========================================================================
def test_d01_not_met_exports_the_declared_values_and_a_bound_companion(client):
    sid, ifc, ids = _web(client)
    url, resp = _download(client, sid, ifc, ids)
    assert resp.headers["Cache-Control"] == "no-store"
    assert resp.headers["X-Content-Type-Options"] == "nosniff"
    assert re.fullmatch(r'attachment; filename="inventorai-planar-clearance-[0-9a-f]{8}-rev0-'
                        r'[0-9a-f]{16}\.zip"', resp.headers["Content-Disposition"])
    files, zf = _bundle(resp)
    comp = json.loads(files["companion.json"])
    assert comp["dxf"]["sha256"] == hashlib.sha256(files["geometry.dxf"]).hexdigest()
    assert comp["handoff_format"] == "inventorai-planar-clearance-cad-handoff/1"
    assert comp["declared_values"] == {"board_x": "84", "board_y": "50", "region_x": "86",
                                       "region_y": "56", "c": "2"}
    ev = comp["evaluation"]
    assert ev["outcome"] == "NOT_MET"
    assert [(a["axis"], a["margin_mm"], a["conditional_min_region_mm"],
             a["conditional_additional_mm"]) for a in ev["axes"]] == [
        ("x", "-1", "88", "2"), ("y", "1", "54", "0")]
    b = comp["binding"]
    assert b["project_id"] == sid and b["interface_id"] == ifc and b["declaration_revision_no"] == 0
    assert b["method"] == {"id": pcc.METHOD_ID, "version": "1.0"}
    assert b["declaration_version"] == pcc.DECLARATION_VERSION
    assert b["region_bound"] == {"id": pcc.REGION_BOUND_ID, "version": "1"}
    assert {b["board"]["component_id"], b["enclosure"]["component_id"]} == set(ids[:2])
    assert b["snapshot_digest"] in url and b["declaration_revision_id"] in url
    assert comp["limitations"] == pcc.load_artifact()["limitations"]
    # the DXF carries the DECLARED 86 x 56 region, never the 88 x 54 conditional minimum
    assert _check_geometry(files["geometry.dxf"], comp["declared_values"]) == 0
    # fixed safe archive paths; no server path, credential or macro
    for info in zf.infolist():
        assert not info.filename.startswith("/") and ".." not in info.filename
    blob = b"".join(files.values())
    for token in (b"/tmp", b"/home", b"INVENTORAI_DB_PATH", b"SECRET", b"csrf", b"<script"):
        assert token not in blob, token
    # model space holds only the two polylines (checked by _outlines); no embedded or external
    # objects (images, OLE, block inserts) and no script
    for token in (b"IMAGEDEF", b"OLE2FRAME", b"\nINSERT\n", b"ACAD_PROXY"):
        assert token not in files["geometry.dxf"], token


def test_d02_guide_is_english_and_arabic_with_the_hash_and_notices(client):
    sid, ifc, ids = _web(client)
    _url, resp = _download(client, sid, ifc, ids)
    files, _zf = _bundle(resp)
    guide = files["README.txt"].decode("utf-8")
    digest = hashlib.sha256(files["geometry.dxf"]).hexdigest()
    assert guide.count(digest) == 2
    for n in range(1, 9):
        for lang in ("en", "ar"):
            assert ui_text.text("UI_PCC_CAD_GUIDE_%d" % n, lang) in guide
    assert "MIT" in guide and "never synchronise back" in guide
    assert "not an enclosure design" in guide and "not a physical verification" in guide


def test_d03_correction_gives_a_new_bundle_and_the_old_one_keeps_its_identity(client):
    sid, ifc, ids = _web(client)
    old_url, old_resp = _download(client, sid, ifc, ids)
    old_files, _ = _bundle(old_resp)
    old_comp = json.loads(old_files["companion.json"])
    new_url, new_resp = _download(client, sid, ifc, ids, values=("84", "50", "88", "56", "2"))
    new_files, _ = _bundle(new_resp)
    new_comp = json.loads(new_files["companion.json"])
    assert new_comp["evaluation"]["outcome"] == "MET"
    assert [a["margin_mm"] for a in new_comp["evaluation"]["axes"]] == ["0", "1"]
    assert new_comp["binding"]["declaration_revision_no"] == 1
    assert new_comp["binding"]["snapshot_digest"] != old_comp["binding"]["snapshot_digest"]
    assert _check_geometry(new_files["geometry.dxf"], new_comp["declared_values"]) == 0
    assert new_comp["declared_values"]["region_x"] == "88"
    # the earlier bundle still names its own revision and snapshot
    assert old_comp["binding"]["declaration_revision_no"] == 0
    assert old_comp["dxf"]["sha256"] == hashlib.sha256(old_files["geometry.dxf"]).hexdigest()
    # the old link no longer produces a file: never a different revision under its name
    stale = client.get(old_url)
    assert stale.status_code == 409 and stale.mimetype == "text/html"
    assert ui_text.text("UI_PCC_CAD_MSG_STALE", "en") in _html.unescape(stale.get_data(as_text=True))


def test_d04_the_equality_case_keeps_the_exact_outcome_and_measures_transfer_separately(client):
    sid, ifc, ids = _web(client)
    _url, resp = _download(client, sid, ifc, ids, values=("99.9", "50", "100.1", "56", "0.1"))
    files, _ = _bundle(resp)
    comp = json.loads(files["companion.json"])
    assert comp["evaluation"]["outcome"] == "MET"
    assert comp["evaluation"]["axes"][0]["margin_mm"] == "0"     # exact method verdict kept
    error = _check_geometry(files["geometry.dxf"], comp["declared_values"])
    assert 0 < error <= Fraction(1, 10 ** 12)                    # binary transfer error, not "exact"
    # a naive check on the drawn coordinates would get the sign wrong; the companion does not
    assert float(Fraction("100.1")) - float(Fraction("99.9")) - 2 * 0.1 < 0


# ==========================================================================
# 2. lifecycle and eligibility
# ==========================================================================
def _no_file(resp, key, status=409):
    assert resp.status_code == status and resp.mimetype == "text/html"
    assert "attachment" not in resp.headers.get("Content-Disposition", "")
    assert ui_text.text(key, "en") in _html.unescape(resp.get_data(as_text=True))


def test_d05_ineligible_states_offer_no_link_and_produce_no_file(client):
    sid, ifc, ids = _web(client)
    url, _resp = _download(client, sid, ifc, ids)
    base = url.split("?", 1)[0]
    # missing information
    body = _save(client, sid, ifc, ids, values=("84", "50", "86", "56", ""),
                 unknown=("c",)).get_data(as_text=True)
    assert _link(body) is None and "data-pcc-cad" not in body
    page = _page(client, sid, ifc).get_data(as_text=True)
    rev = re.search(r'data-pcc-revision[^>]*>(\d+)<', page).group(1)
    _no_file(client.get(url), "UI_PCC_CAD_MSG_NOT_AVAILABLE")
    # inapplicable
    answers = list(APPLIES)
    answers[2] = pcc.ANSWER_DOES_NOT_APPLY
    body = _save(client, sid, ifc, ids, answers=answers).get_data(as_text=True)
    assert _link(body) is None
    # stale binding: a component correction needs reconfirmation
    body = _save(client, sid, ifc, ids).get_data(as_text=True)
    current = _link(body)
    store = appmod._get_store()
    _correct(store, sid, ids[0], 0, "Driver board v2", "Controls the motor")
    _no_file(client.get(current), "UI_PCC_CAD_MSG_NOT_AVAILABLE")
    assert _link(_page(client, sid, ifc).get_data(as_text=True)) is None
    assert rev and base


def test_d06_withdrawn_and_unavailable_produce_no_file(client, monkeypatch):
    sid, ifc, ids = _web(client)
    url, _resp = _download(client, sid, ifc, ids)
    page = _page(client, sid, ifc).get_data(as_text=True)
    data = _fields(page, form="data-pcc-withdraw-form")
    data["withdraw_confirm"] = "yes"
    client.post("/session/%s/interface-clearance/%s/withdraw" % (sid, ifc), data=data)
    _no_file(client.get(url), "UI_PCC_CAD_MSG_NOT_AVAILABLE")

    def unreadable(self, project_id):
        raise RuntimeError("unreadable")
    monkeypatch.setattr(type(appmod._get_store()), "load_planar_clearance", unreadable)
    _no_file(client.get(url), "UI_PCC_CAD_MSG_FAILED", status=503)


@pytest.mark.parametrize("query", [
    "", "?revision=x&digest=y", "?revision={rev}", "?digest={dig}",
    "?revision={rev}&revision={rev}&digest={dig}", "?revision={rev}&digest=0000000000000000"])
def test_d07_forged_partial_or_repeated_identities_produce_no_file(client, query):
    sid, ifc, ids = _web(client)
    url, _resp = _download(client, sid, ifc, ids)
    rev = re.search(r"revision=([^&]+)", url).group(1)
    dig = re.search(r"digest=([^&]+)", url).group(1)
    resp = client.get(url.split("?", 1)[0] + query.format(rev=rev, dig=dig))
    _no_file(resp, "UI_PCC_CAD_MSG_STALE")


def test_d08_a_failed_generation_returns_no_partial_bundle(client, monkeypatch):
    sid, ifc, ids = _web(client)
    url, _resp = _download(client, sid, ifc, ids)

    def broken(model):
        raise cad.CadExportError("forced")
    monkeypatch.setattr(cad, "dxf_bytes", broken)
    _no_file(client.get(url), "UI_PCC_CAD_MSG_FAILED", status=503)
    monkeypatch.undo()                                   # a working writer, an exceeded size bound
    monkeypatch.setattr(cad, "MAX_BUNDLE_BYTES", 10)
    _no_file(client.get(url), "UI_PCC_CAD_MSG_FAILED", status=503)


def test_d09_one_snapshot_per_download_and_nothing_stored(client, monkeypatch):
    sid, ifc, ids = _web(client)
    url, _resp = _download(client, sid, ifc, ids)
    store = appmod._get_store()
    tables_before = sorted(r[0] for r in store._conn.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table'"))
    rows_before = store._conn.execute("SELECT COUNT(*) FROM planar_clearance_revisions").fetchone()
    calls = []
    real = type(store).load_planar_clearance

    def counting(self, project_id):
        calls.append(project_id)
        return real(self, project_id)
    monkeypatch.setattr(type(store), "load_planar_clearance", counting)
    files, _ = _bundle(client.get(url))
    assert calls == [sid]                                # ONE coherent snapshot builds everything
    comp = json.loads(files["companion.json"])
    assert comp["binding"]["snapshot_digest"] in url
    assert sorted(r[0] for r in store._conn.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table'")) == tables_before
    assert store._conn.execute(
        "SELECT COUNT(*) FROM planar_clearance_revisions").fetchone() == rows_before


def test_d10_authorization_and_foreign_identities_are_denied(client):
    from tests.test_cap12_form_mockup_advisory import _client_for
    owner, _aid = _client_for("cad-owner@example.com")
    sid, ifc, ids = _web(owner)
    url, resp = _download(owner, sid, ifc, ids)
    assert resp.mimetype == "application/zip"
    stranger, _bid = _client_for("cad-stranger@example.com")       # another signed-in account
    denied = stranger.get(url)
    assert denied.status_code == 302 and denied.mimetype != "application/zip"
    appmod.app.config["TESTING"] = True
    with csrf_client(appmod.app) as anonymous:                     # signed out
        denied = anonymous.get(url)
        assert denied.status_code == 302 and denied.mimetype != "application/zip"
    # an interaction of another project is the same non-enumerating denial
    other_sid, other_ifc, _ = _web(owner)
    foreign = url.replace("/interface-clearance/%s/" % ifc, "/interface-clearance/%s/" % other_ifc)
    assert owner.get(foreign).status_code == 302
    bad = url.replace("/interface-clearance/%s/" % ifc, "/interface-clearance/not-an-id/")
    assert owner.get(bad).status_code == 302
    assert other_sid != sid


# ==========================================================================
# 3. adapter and copy
# ==========================================================================
def test_d11_the_adapter_refuses_an_ineligible_model_and_maps_only():
    with pytest.raises(cad.CadExportError):
        cad.build_bundle({"eligible": False}, "2026-11-03T00:00:00+00:00")
    with pytest.raises(cad.CadExportError):
        cad.build_bundle(None, "2026-11-03T00:00:00+00:00")
    source = open(cad.__file__, encoding="utf-8").read()
    for forbidden in ("exact_margins", "region_bound(", "evaluate(", "load_planar_clearance",
                      "open(", "requests", "urllib", "socket", "subprocess"):
        assert forbidden not in source, forbidden


def test_d12_the_download_is_offered_in_english_and_arabic(client):
    sid, ifc, ids = _web(client)
    _save(client, sid, ifc, ids)
    for lang in ("en", "ar"):
        body = _page(client, sid, ifc, lang=lang).get_data(as_text=True)
        text = _html.unescape(body)
        assert ui_text.text("UI_PCC_CAD_DOWNLOAD", lang) in text
        assert ui_text.text("UI_PCC_CAD_NOTE", lang) in text
        assert re.search(r'<bdi dir="ltr" data-pcc-cad-digest>[0-9a-f]{16}</bdi>', body)
    for key in [k for k in ui_text.UI_STRINGS if k.startswith("UI_PCC_CAD_")]:
        assert ui_text.text(key, "ar") != ui_text.text(key, "en")


def test_d13_preserved_synthetic_evidence_is_intact():
    """The preserved CAD-handoff evidence: every file bound by SHA256SUMS; each product-route bundle
    holds the three fixed files, its companion hash matches its DXF, and the recorded FreeCAD
    measurements say every bundle passed (FreeCAD itself is not run here)."""
    import os
    root = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "docs", "benchmarks", "evidence", "board_enclosure_cad_handoff_v1")
    sums = {}
    for line in open(os.path.join(root, "SHA256SUMS"), encoding="utf-8").read().splitlines():
        digest, name = line.split("  ", 1)
        sums[name] = digest
    assert "handoff_proof_bundle.tar.gz" in sums and len(sums) == 6
    for name, digest in sums.items():
        assert hashlib.sha256(open(os.path.join(root, name), "rb").read()).hexdigest() == digest, name
    measured = json.load(open(os.path.join(root, "product_measurements.json"), encoding="utf-8"))
    assert measured["freecad"].startswith("1.0.2") and measured["settings"]["dxfScaling"] == 1.0
    outcomes = {}
    for name in ("A_rev0_not_met", "B_rev1_met", "C_precision_met"):
        zf = zipfile.ZipFile(os.path.join(root, "product_route_bundles", name + ".zip"))
        assert zf.namelist() == ["geometry.dxf", "companion.json", "README.txt"]
        comp = json.loads(zf.read("companion.json"))
        assert comp["dxf"]["sha256"] == hashlib.sha256(zf.read("geometry.dxf")).hexdigest()
        assert _check_geometry(zf.read("geometry.dxf"), comp["declared_values"]) <= Fraction(1, 10 ** 12)
        assert measured["bundles"][name]["pass"] is True
        outcomes[name] = comp["evaluation"]["outcome"]
    assert outcomes == {"A_rev0_not_met": "NOT_MET", "B_rev1_met": "MET", "C_precision_met": "MET"}
