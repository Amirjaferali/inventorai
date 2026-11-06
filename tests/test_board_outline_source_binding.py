"""BOARD-OUTLINE-SOURCE-BINDING-01 - one optional KiCad 10.0.8 board-file inspection
bound to the inventor's planar clearance declaration.

Synthetic data only: the board files are the committed fixtures of the #933 and #936
proofs (no KiCad runs here). Covers: R the pure hardened reader; S the Stage-15
source binding (v2 shape, history validation, digest, carry-forward) and the record-store
sidecar (atomic write, insert-only triggers, corruption -> UNAVAILABLE, upgrade /
compatible rollback / re-upgrade); W the intake, the HMAC offer, the save behind the
v2-write switch (OFF by default), EXACT / DIFFERS, the CAD companion, privacy and EN / AR;
Q the route-scoped request class (in-memory, bounded parts, rejection before spooling).
"""
import dataclasses
import hashlib
import io
import json
import os
import re
import sqlite3
import zipfile

import pytest

import web.app as appmod
from engine import mechanical_planar_clearance as pcc
from engine import planar_clearance_board_source as R
from engine import record_store as rs
from engine import subsystem_model as sm
from tests.csrf_client import csrf_client
from tests.test_board_enclosure_planar_clearance import APPLIES, _fields, _pdf_source
from tests.test_component_interface_participation import _form as _icp_form, _post as _icp_post
from tests.test_component_inventory_declare_list import _declare as _declare_component
from tests.test_stage15_integrated_invention_entry import _compose, _created
from tests.test_stage15_subsystem_interface_declaration import _declare as _declare_interface
from web import planar_clearance as view_model
from web import ui_text

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
K10 = os.path.join(ROOT, "docs", "benchmarks", "evidence", "kicad10_format_qualification_v1",
                   "fixtures")
K7 = os.path.join(ROOT, "docs", "benchmarks", "evidence", "pcb_outline_planar_clearance_v1",
                  "fixtures")
IDEA = ("A small handheld controller: a driver board sits inside a plastic case "
        "and drives a motor.")


def _bytes(name, folder=K10):
    with open(os.path.join(folder, name + ".kicad_pcb"), "rb") as fh:
        return fh.read()


def _refused(data):
    with pytest.raises(R.Refused) as exc:
        R.read_board_outline(data)
    return exc.value.code


_HEAD = ('(kicad_pcb\n\t(version 20260206)\n\t(generator "pcbnew")\n'
         '\t(layers\n\t\t(25 "Edge.Cuts" user)\n\t)\n%s)\n')
_RECT = ('\t(gr_rect (start %s) (end %s) (stroke (width 0.1) (type default)) (fill no) '
         '(layer "Edge.Cuts")%s (uuid "u"))\n')


def _board(start="100 100", end="184 150", extra="", body=None):
    return (_HEAD % (body if body is not None else _RECT % (start, end, extra))).encode("utf-8")


# ==========================================================================
# R. the pure hardened reader
# ==========================================================================
@pytest.mark.parametrize("name, dims", [
    ("k10_board_v1", ("84", "50")), ("k10_board_v1_lines", ("84", "50")),
    ("k10_board_v2", ("80", "50")), ("up_board_v1", ("84", "50")),
    ("up_board_v1_lines", ("84", "50")), ("up_board_v2", ("80", "50")),
    ("env_0fp", ("84", "50")), ("env_5fp", ("84", "50")), ("env_20fp", ("84", "50"))])
def test_r01_supported_kicad10_boards_are_read_exactly(name, dims):
    data = _bytes(name)
    outline = R.read_board_outline(data)
    assert (outline.file_x, outline.file_y) == dims
    assert outline.source_sha256 == hashlib.sha256(data).hexdigest()   # raw bytes, pre-decode
    assert outline.source_size == len(data)
    assert (outline.format_id, outline.reader_id, outline.rule_id) == (
        "kicad-board/20260206", R.READER_ID, R.RULE_ID)


@pytest.mark.parametrize("name, code", [
    ("k10_neg_rounded_corners", R.UNSUPPORTED_OUTLINE), ("k10_neg_cutout", R.UNSUPPORTED_OUTLINE),
    ("k10_neg_l_shape", R.NOT_ONE_RECTANGLE), ("k10_neg_two_boards", R.NOT_ONE_RECTANGLE),
    ("k10_neg_open_outline", R.NOT_ONE_RECTANGLE), ("k10_neg_no_outline", R.OUTLINE_MISSING),
    ("k10_neg_rotated", R.NOT_ONE_RECTANGLE),
    ("up_neg_rounded_corners", R.UNSUPPORTED_OUTLINE), ("up_neg_cutout", R.UNSUPPORTED_OUTLINE),
    ("up_neg_l_shape", R.NOT_ONE_RECTANGLE), ("up_neg_two_boards", R.NOT_ONE_RECTANGLE),
    ("up_neg_open_outline", R.NOT_ONE_RECTANGLE), ("up_neg_no_outline", R.OUTLINE_MISSING),
    ("up_neg_rotated", R.NOT_ONE_RECTANGLE),
    ("txt_angle_on_gr_line", R.FIELD_NOT_ALLOWED),
    ("txt_unknown_field_on_gr_rect", R.FIELD_NOT_ALLOWED),
    ("txt_other_version", R.VERSION_NOT_ACCEPTED), ("txt_doubled_lines", R.NOT_ONE_RECTANGLE),
    ("env_40fp", R.TOO_LARGE), ("env_100fp", R.TOO_LARGE)])
def test_r02_the_936_controls_are_refused(name, code):
    assert _refused(_bytes(name)) == code


@pytest.mark.parametrize("name", sorted(f[:-10] for f in os.listdir(K7) if f.endswith(".kicad_pcb")))
def test_r03_no_kicad7_claim_every_933_fixture_is_refused_by_version(name):
    assert _refused(_bytes(name, K7)) == R.VERSION_NOT_ACCEPTED


@pytest.mark.parametrize("data, code", [
    (b"", R.EMPTY),
    (b"x" * (R.MAX_FILE_BYTES + 1), R.TOO_LARGE),
    (_board().replace(b"pcbnew", b"pcb\x00new"), R.CONTROL_CHARACTER),
    (_board() + b"\xff", R.NOT_UTF8),
    (b"\xef\xbb\xbf" + _board(), R.CONTROL_CHARACTER),
    (_board().replace(b"pcbnew", b"pcb\x07new"), R.CONTROL_CHARACTER),
    (_board().replace(b'"pcbnew"', b'"pcbnew'), R.MALFORMED),          # unterminated string
    (_board().replace(b'"pcbnew"', b'"pcb\\qnew"'), R.MALFORMED),       # unknown escape
    (_board()[:-3], R.MALFORMED),                                       # unbalanced
    (_board() + b"(kicad_pcb)", R.MALFORMED),                           # a second root
    (_board() + b"trailing", R.MALFORMED),
    (b"(kicad_sch (version 20260206))", R.NOT_KICAD_BOARD),
    (b"kicad_pcb", R.NOT_KICAD_BOARD),
    (_board(body=_RECT % ("100 100", "184 150", "")).replace(b"\t(version 20260206)\n", b""),
     R.VERSION_MISSING),
    (_board().replace(b"(version 20260206)", b"(version 20260206) (version 20260206)"),
     R.FIELD_MALFORMED),
    (_board().replace(b"(version 20260206)", b'(version "20260206")'), R.FIELD_MALFORMED),
    (_board().replace(b"(version 20260206)", b"(version 20221018)"), R.VERSION_NOT_ACCEPTED),
    (_board(start="1e2 100"), R.NUMBER_NOT_PLAIN),
    (_board(start="+100 100"), R.NUMBER_NOT_PLAIN),
    (_board(start="100. 100"), R.NUMBER_NOT_PLAIN),
    (_board(start="nan 100"), R.NUMBER_NOT_PLAIN),
    (_board(start="1000000 100"), R.NUMBER_NOT_PLAIN),
    (_board(start="100.0000001 100"), R.NUMBER_NOT_PLAIN),
    (_board(start='"100" 100'), R.NUMBER_NOT_PLAIN),
    (_board(start="100 100 0"), R.FIELD_MALFORMED),
    (_board(extra=" (start 1 1)"), R.FIELD_MALFORMED),                  # duplicated
    (_board(extra=" (angle 30)"), R.FIELD_NOT_ALLOWED),                 # transformed
    (_board(extra=" (rotation 90)"), R.FIELD_NOT_ALLOWED),
    (_board(extra=" hide"), R.FIELD_NOT_ALLOWED),
    (_board(extra=" (net 0)"), R.FIELD_NOT_ALLOWED),
    (_board(extra=" (locked maybe)"), R.FIELD_MALFORMED),
    (_board().replace(b'(layer "Edge.Cuts")', b"(layer Edge.Cuts)"), R.FIELD_MALFORMED),
    (_board().replace(b"(fill no)", b"(fill yes)"), R.FIELD_MALFORMED),
    (_board().replace(b"(fill no) ", b""), R.FIELD_MALFORMED),
    (_board().replace(b"(type default)", b"(type dash) (type dash)"), R.FIELD_MALFORMED),
    (_board().replace(b"(width 0.1)", b"(width -0.1)"), R.NUMBER_NOT_PLAIN),
    (_board(start="100.12345 100"), R.DIMENSION_NOT_REPRESENTABLE),     # never rounded
    (_board(start="100 100", end="100 150"), R.NOT_ONE_RECTANGLE),      # degenerate
])
def test_r04_hardening_refuses_with_a_closed_code(data, code):
    assert _refused(data) == code


def test_r05_depth_tokens_and_atom_length_are_bounded():
    deep = _board(body="\t" + "(a " * 40 + ")" * 40 + "\n" + _RECT % ("100 100", "184 150", ""))
    assert _refused(deep) == R.TOO_DEEP
    many = _board(body="\t(x " + "1 " * (R.MAX_TOKENS + 5) + ")\n")
    assert len(many) < R.MAX_FILE_BYTES
    assert _refused(many) == R.TOO_MANY_TOKENS
    long_atom = _board(body='\t(x "%s")\n' % ("a" * (R.MAX_ATOM_CHARS + 1)))
    assert _refused(long_atom) == R.ATOM_TOO_LONG


@pytest.mark.parametrize("body, code", [
    ('\t(footprint "x" (layer "F.Cu") (fp_line (start 0 0) (end 1 0) (layer "Edge.Cuts")))\n'
     + _RECT % ("100 100", "184 150", ""), R.UNSUPPORTED_OUTLINE),
    ('\t(gr_arc (start 0 0) (mid 1 1) (end 2 0) (layer "Edge.Cuts"))\n'
     + _RECT % ("100 100", "184 150", ""), R.UNSUPPORTED_OUTLINE),
    ('\t(gr_poly (pts (xy 0 0) (xy 1 0) (xy 1 1)) (layer "Edge.Cuts"))\n', R.UNSUPPORTED_OUTLINE),
    ('\t(zone (layers "F.Cu" "Edge.Cuts"))\n' + _RECT % ("100 100", "184 150", ""),
     R.UNSUPPORTED_OUTLINE),
    ('\t(gr_rect (start 100 100) (end 184 150) (stroke (width 0.1) (type default) '
     '(layer "Edge.Cuts")) (fill no) (layer "Edge.Cuts"))\n', R.UNSUPPORTED_OUTLINE),
    ('\t(layer "Edge.Cuts")\n' + _RECT % ("100 100", "184 150", ""), R.UNSUPPORTED_OUTLINE),
    ("".join(_RECT % ("%d 0" % i, "%d 10" % (i + 5), "") for i in range(0, 90, 10)),
     R.TOO_MANY_OUTLINE_SHAPES),
    (_RECT % ("100 100", "184 150", "") + _RECT % ("200 100", "284 150", ""),
     R.NOT_ONE_RECTANGLE),
])
def test_r06_edge_cuts_is_checked_exhaustively(body, code):
    assert _refused(_board(body=body)) == code


def test_r07_exact_decimals_and_reversed_corners():
    o = R.read_board_outline(_board(start="184.50 150", end="100.25 100"))
    assert (o.file_x, o.file_y) == ("84.25", "50")
    o = R.read_board_outline(_board(start="-10 -5", end="74 45"))
    assert (o.file_x, o.file_y) == ("84", "50")


def test_r08_refusals_never_echo_file_content():
    secret = b"SECRET-CONTENT-7f3a"
    for data in (_board(extra=' (angle 30) (uuid "%s")' % secret.decode()),
                 _board().replace(b"pcbnew", secret + b"\x00")):
        with pytest.raises(R.Refused) as exc:
            R.read_board_outline(data)
        assert str(exc.value) in R.REFUSAL_CODES
        assert secret.decode() not in repr(exc.value)


def test_r09_the_reader_is_pure():
    import ast
    tree = ast.parse(open(R.__file__, encoding="utf-8").read())
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.add(node.module)
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            assert node.func.id not in ("open", "eval", "exec", "print"), node.func.id
    assert imported == {"hashlib", "re", "dataclasses", "decimal"}


# ==========================================================================
# helpers for S / W / Q
# ==========================================================================
@pytest.fixture
def client():
    appmod.app.config["TESTING"] = True
    with csrf_client(appmod.app) as c:
        yield c


@pytest.fixture
def on(monkeypatch):
    monkeypatch.setitem(appmod.app.config, "PCC_SOURCE_BINDING_WRITES", True)


def _project(c, lang=None):
    if lang == "ar":
        assert c.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    sid = _created(_compose(c, IDEA))
    assert _declare_interface(c, sid, "The board sits inside the case").status_code == 302
    for name in ("Driver board", "Plastic case"):
        assert _declare_component(c, sid, name=name, function="Does its job").status_code in (200, 302)
    form = _icp_form(c, sid)
    ids = [o[0] for o in form["options"]]
    assert _icp_post(c, sid, form, ids).status_code in (200, 302)
    ifc = appmod._get_store().load_planar_clearance(sid)["interfaces"][0].interface_id
    return sid, ifc, ids


def _url(sid, ifc, tail=""):
    return "/session/%s/interface-clearance/%s%s" % (sid, ifc, tail)


def _body(resp):
    return resp.get_data(as_text=True)


def _file(data, name):
    from werkzeug.datastructures import FileStorage
    return FileStorage(stream=io.BytesIO(data), filename=name)


def _csrf(c, sid, ifc):
    body = _body(c.get(_url(sid, ifc)))
    return re.search(r'name="csrf_token" value="([^"]+)"', body).group(1)


def _inspect(c, sid, ifc, ids, data, filename="my-secret-board-name.kicad_pcb", extra=None):
    form = {"csrf_token": _csrf(c, sid, ifc), "board_component_id": ids[0],
            "enclosure_component_id": ids[1],
            "board_file": _file(data, filename)}
    form.update(extra or {})
    return c.post(_url(sid, ifc, "/board-source"), data=form,
                  content_type="multipart/form-data")


def _save(c, sid, ifc, ids, page, values=("84", "50", "86", "56", "2"), axis="file_x_is_board_x",
          extra=None, unknown=()):
    data = _fields(_body(page))
    data.update({"board_component_id": ids[0], "enclosure_component_id": ids[1],
                 "region_description": "Inner floor between the four posts",
                 "basis_board": "Measured with calipers"})
    for role, value in zip(pcc.VALUE_ROLES, values):
        data["value_" + role] = value or ""
    for role in unknown:
        data["unknown_" + role] = "1"
    for d, a in zip(pcc.DECLARATION_IDS, APPLIES):
        data["decl_" + d] = a
    if axis and "source_token" in data:
        data["source_axis"] = axis
    data.update(extra or {})
    return c.post(_url(sid, ifc), data=data), data


def _snap(sid):
    return appmod._get_store().load_planar_clearance(sid)


def _db():
    appmod._get_store()
    return sqlite3.connect(os.environ["INVENTORAI_DB_PATH"])


def _dump():
    conn = _db()
    try:
        return "\n".join(conn.iterdump())
    finally:
        conn.close()


def _bindings(sid):
    conn = _db()
    try:
        return conn.execute("SELECT * FROM planar_clearance_source_bindings WHERE project_id = ?",
                            (sid,)).fetchall()
    finally:
        conn.close()


def _linked(c, sid, ifc, ids, name="k10_board_v1", values=("84", "50", "86", "56", "2"),
            axis="file_x_is_board_x"):
    offer = _inspect(c, sid, ifc, ids, _bytes(name))
    assert offer.status_code == 200, _body(offer)
    resp, data = _save(c, sid, ifc, ids, offer, values=values, axis=axis)
    assert resp.status_code == 200 and "data-pcc-notice" in _body(resp), _body(resp)
    return resp, data


def _legacy_digest(record):
    """The digest exactly as the pre-change build computed it (v1 only)."""
    payload = [[r.revision_id, r.revision_no, r.kind,
                None if r.material is None else [
                    r.material.board_component_id, r.material.enclosure_component_id,
                    r.material.board_component_revision, r.material.enclosure_component_revision,
                    r.material.board_participation_epoch, r.material.enclosure_participation_epoch,
                    r.material.region_description, list(r.material.values),
                    list(r.material.basis), list(r.material.applicability),
                    r.material.method_id, r.material.method_version,
                    r.material.declaration_version]] for r in record.revisions]
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(canonical.encode("ascii")).hexdigest()[:16]


# ==========================================================================
# W. the intake, the offer and the save
# ==========================================================================
def test_w01_off_by_default_no_intake_and_no_v2_write(client):
    assert appmod.app.config["PCC_SOURCE_BINDING_WRITES"] is False
    sid, ifc, ids = _project(client)
    page = client.get(_url(sid, ifc))
    assert "data-pcc-source-form" not in _body(page)
    before = _dump()
    resp = _inspect(client, sid, ifc, ids, _bytes("k10_board_v1"))
    assert resp.status_code == 404 and "data-pcc-source-offer" not in _body(resp)
    assert _dump() == before
    # a token minted while ON cannot be used while OFF
    appmod.app.config["PCC_SOURCE_BINDING_WRITES"] = True
    try:
        offer = _inspect(client, sid, ifc, ids, _bytes("k10_board_v1"))
    finally:
        appmod.app.config["PCC_SOURCE_BINDING_WRITES"] = False
    resp, _ = _save(client, sid, ifc, ids, offer)
    assert resp.status_code == 409 and _bindings(sid) == []
    assert _snap(sid)["ledger"].records == ()


def test_w02_inspecting_offers_the_outline_and_writes_nothing(client, on):
    sid, ifc, ids = _project(client)
    assert "data-pcc-source-privacy" in _body(client.get(_url(sid, ifc)))
    before = _dump()
    resp = _inspect(client, sid, ifc, ids, _bytes("k10_board_v1"))
    body = _body(resp)
    assert resp.status_code == 200 and "data-pcc-source-offer" in body
    assert "X = 84 mm, Y = 50 mm" in body
    assert 'name="source_token"' in body and 'name="source_axis"' in body
    assert "checked" not in re.search(r"data-pcc-source-axis>.*?</fieldset>", body, re.S).group(0)
    assert "my-secret-board-name" not in body                      # no file name echoed
    assert _dump() == before                                       # nothing durable written
    assert resp.headers["Cache-Control"] == "no-store"


def test_w03_regression_84x50_in_86x56_c2_is_unchanged_by_the_link(client, on):
    sid, ifc, ids = _project(client)
    resp, _ = _linked(client, sid, ifc, ids)
    body = _body(resp)
    assert re.findall(r'data-pcc-outcome="(\w+)"', body)[0] == "NOT_MET"
    view = view_model.clearance_view(_snap(sid), ifc, appmod._PCC_BINDING)
    margins = {a["axis"]: a["margin_text"] for a in view["evaluation"]["axes"]}
    mins = {a["axis"]: a["region_min_text"] for a in view["evaluation"]["axes"]}
    assert margins == {"x": "-1", "y": "1"} and mins == {"x": "88", "y": "54"}
    assert view["material"]["declaration_version"] == sm.PLANAR_CLEARANCE_DECLARATION_V2
    assert view["state"] == view_model.STATE_CURRENT
    assert 'data-pcc-agreement="EXACT"' in body and "data-pcc-source-exact" in body
    rows = _bindings(sid)
    assert len(rows) == 1
    row = dict(zip(rs._PCC_SOURCE_COLUMNS, rows[0]))
    assert row["source_sha256"] == hashlib.sha256(_bytes("k10_board_v1")).hexdigest()
    assert (row["file_x"], row["file_y"], row["axis_assignment"]) == ("84", "50", "file_x_is_board_x")
    assert row["carry_forward_from"] is None and len(row["nonce_hash"]) == 64


def test_w04_differs_shows_both_value_sets_and_uses_the_declared_values(client, on):
    sid, ifc, ids = _project(client)
    resp, _ = _linked(client, sid, ifc, ids, values=("80", "50", "86", "56", "2"))
    body = _body(resp)
    text = re.sub(r"<[^>]+>", "", re.search(r"data-pcc-source-dims>.*?</p>", body, re.S).group(0))
    assert "File outline: 84 × 50 mm. Your declared board: 80 × 50 mm. " \
           "Calculation uses your declared dimensions." in " ".join(text.split())
    assert 'data-pcc-agreement="DIFFERS"' in body
    assert re.findall(r'data-pcc-changed-axis="(\w)"', body) == ["x"]
    view = view_model.clearance_view(_snap(sid), ifc, appmod._PCC_BINDING)
    assert {a["axis"]: a["margin_text"] for a in view["evaluation"]["axes"]}["x"] == "1"
    assert "verified" not in re.search(r"data-pcc-source-link.*?</div>", body, re.S).group(0).replace(
        "does not verify", "")


def test_w05_axis_assignment_and_exact_decimal_comparison(client, on):
    sid, ifc, ids = _project(client)
    resp, _ = _linked(client, sid, ifc, ids, values=("50.0", "84.00", "86", "90", "2"),
                      axis="file_x_is_board_y")
    assert 'data-pcc-agreement="EXACT"' in _body(resp)               # 84 == 84.00
    m = _snap(sid)["ledger"].records[0].current
    assert m.source.board_dims() == ("50", "84")


def test_w06_unknown_or_missing_declared_values_never_count_as_exact(client, on):
    sid, ifc, ids = _project(client)
    resp, _ = _linked(client, sid, ifc, ids, values=("", "50", "86", "56", "2"))
    resp2 = client.get(_url(sid, ifc))
    body = _body(resp2)
    assert 'data-pcc-agreement="DIFFERS"' in body
    assert re.findall(r'data-pcc-changed-axis="(\w)"', body) == ["x"]
    m = _snap(sid)["ledger"].records[0].current
    assert sm.planar_clearance_source_agreement(
        dataclasses.replace(m, values=("unknown",) + m.values[1:]))[0] == sm.PCC_SOURCE_DIFFERS


def test_w07_exact_retry_acknowledges_and_token_reuse_conflicts(client, on):
    sid, ifc, ids = _project(client)
    offer = _inspect(client, sid, ifc, ids, _bytes("k10_board_v1"))
    resp, data = _save(client, sid, ifc, ids, offer)
    assert resp.status_code == 200
    again = client.post(_url(sid, ifc), data=data)                  # exact retry
    assert again.status_code == 200 and "data-pcc-error" not in _body(again)
    assert len(_bindings(sid)) == 1
    # the same inspection under a NEW submission identity is a different action
    fresh = _fields(_body(client.get(_url(sid, ifc))))
    reuse = dict(data, pcc_submission=fresh["pcc_submission"], declaration_id=fresh["declaration_id"],
                 expected_head=fresh["expected_head"], value_region_x="90")
    resp = client.post(_url(sid, ifc), data=reuse)
    assert resp.status_code == 409 and len(_bindings(sid)) == 1
    assert len(_snap(sid)["ledger"].records[0].revisions) == 1


def test_w08_tampered_expired_or_foreign_tokens_are_refused(client, on, monkeypatch):
    sid, ifc, ids = _project(client)
    offer = _inspect(client, sid, ifc, ids, _bytes("k10_board_v1"))
    token = _fields(_body(offer))["source_token"]
    body, sig = token.split(".")
    payload = json.loads(__import__("base64").urlsafe_b64decode(body + "=" * (-len(body) % 4)))
    payload["fx"] = "80"
    forged = __import__("base64").urlsafe_b64encode(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).decode().rstrip("=")
    for bad in (forged + "." + sig, token[:-2] + "00", "x." + sig, token + "x"):
        resp, _ = _save(client, sid, ifc, ids, offer, extra={"source_token": bad})
        assert resp.status_code == 400, bad
    # another interaction of another project cannot use it
    sid2, ifc2, ids2 = _project(client)
    page2 = client.get(_url(sid2, ifc2))
    resp, _ = _save(client, sid2, ifc2, ids2, page2, extra={"source_token": token,
                                                              "source_axis": "file_x_is_board_x"})
    assert resp.status_code == 400
    # expiry
    real = appmod._pcc_source_now
    monkeypatch.setattr(appmod, "_pcc_source_now", lambda: real() + 31 * 60)
    resp, _ = _save(client, sid, ifc, ids, offer)
    assert resp.status_code == 409 and "expired" in _body(resp)
    assert _bindings(sid) == [] and _bindings(sid2) == []


def test_w09_axis_choice_is_required(client, on):
    sid, ifc, ids = _project(client)
    offer = _inspect(client, sid, ifc, ids, _bytes("k10_board_v1"))
    resp, _ = _save(client, sid, ifc, ids, offer, axis=None)
    assert resp.status_code == 400 and _bindings(sid) == []
    resp, _ = _save(client, sid, ifc, ids, offer, axis="file_x_is_board_z")
    assert resp.status_code == 400 and _bindings(sid) == []


def test_w10_a_changed_history_or_board_after_inspection_is_refused(client, on):
    sid, ifc, ids = _project(client)
    _linked(client, sid, ifc, ids)
    offer = _inspect(client, sid, ifc, ids, _bytes("k10_board_v2"))
    # someone corrects the declaration after the inspection
    page = client.get(_url(sid, ifc))
    data = _fields(_body(page))
    resp, _ = _save(client, sid, ifc, ids, page, values=("84", "50", "90", "56", "2"))
    assert resp.status_code == 200
    resp, data = _save(client, sid, ifc, ids, offer, values=("80", "50", "86", "56", "2"))
    assert resp.status_code == 409
    record = _snap(sid)["ledger"].records[0]
    assert [r.material.values[0] for r in record.revisions] == ["84", "84"]
    # a different board / enclosure than inspected
    offer = _inspect(client, sid, ifc, ids, _bytes("k10_board_v2"))
    resp, _ = _save(client, sid, ifc, ids, offer, extra={"board_component_id": ids[1],
                                                          "enclosure_component_id": ids[0]})
    assert resp.status_code == 409


def test_w11_inspection_needs_board_and_enclosure_first_and_exactly_one_file(client, on):
    sid, ifc, ids = _project(client)
    resp = _inspect(client, sid, ifc, ids, _bytes("k10_board_v1"),
                    extra={"enclosure_component_id": ids[0]})
    assert resp.status_code == 409
    resp = _inspect(client, sid, ifc, ids, _bytes("k10_board_v1"),
                    extra={"board_component_id": ""})
    assert resp.status_code == 409
    form = {"csrf_token": _csrf(client, sid, ifc), "board_component_id": ids[0],
            "enclosure_component_id": ids[1],
            "board_file": [_file(_bytes("k10_board_v1"), "a.kicad_pcb"),
                           _file(_bytes("k10_board_v2"), "b.kicad_pcb")]}
    resp = client.post(_url(sid, ifc, "/board-source"), data=form, content_type="multipart/form-data")
    assert resp.status_code == 400
    form = {"csrf_token": _csrf(client, sid, ifc), "board_component_id": ids[0],
            "enclosure_component_id": ids[1]}
    resp = client.post(_url(sid, ifc, "/board-source"), data=form, content_type="multipart/form-data")
    assert resp.status_code == 400


def test_w12_a_refused_file_states_the_reason_without_echo(client, on):
    sid, ifc, ids = _project(client)
    before = _dump()
    data = _board(extra=' (angle 30) (uuid "UNIQUE-MARKER-91c")')
    resp = _inspect(client, sid, ifc, ids, data)
    body = _body(resp)
    assert resp.status_code == 422
    assert ui_text.text("UI_PCC_SRC_REFUSED_FIELD_NOT_ALLOWED", "en") in body
    assert "UNIQUE-MARKER-91c" not in body and "my-secret-board-name" not in body
    assert "data-pcc-source-offer" not in body and _dump() == before


def test_w13_carry_forward_only_for_region_or_clearance_corrections(client, on):
    sid, ifc, ids = _project(client)
    _linked(client, sid, ifc, ids)
    # region / clearance only -> the binding is carried forward
    resp, _ = _save(client, sid, ifc, ids, client.get(_url(sid, ifc)),
                    values=("84", "50", "88", "56", "1"))
    assert resp.status_code == 200
    record = _snap(sid)["ledger"].records[0]
    head = record.current
    assert head.declaration_version == sm.PLANAR_CLEARANCE_DECLARATION_V2
    assert head.source.carry_forward_from == record.revisions[0].revision_id
    assert head.source.nonce_hash is None
    assert "data-pcc-source-carried" in _body(client.get(_url(sid, ifc)))
    # restating exactly is refused, never a link-dropping revision
    resp, _ = _save(client, sid, ifc, ids, client.get(_url(sid, ifc)),
                    values=("84", "50", "88", "56", "1"))
    assert resp.status_code == 409
    assert len(_snap(sid)["ledger"].records[0].revisions) == 2
    # a board dimension change without a fresh inspection -> source-free v1
    resp, _ = _save(client, sid, ifc, ids, client.get(_url(sid, ifc)),
                    values=("80", "50", "88", "56", "1"))
    assert resp.status_code == 200
    record = _snap(sid)["ledger"].records[0]
    assert record.current.source is None
    assert record.current.declaration_version == pcc.DECLARATION_VERSION
    assert len(_bindings(sid)) == 2
    # withdrawal adds no binding
    page = client.get(_url(sid, ifc))
    data = _fields(_body(page), form="data-pcc-withdraw-form")
    data["withdraw_confirm"] = "yes"
    assert client.post(_url(sid, ifc, "/withdraw"), data=data).status_code == 200
    assert len(_bindings(sid)) == 2


def test_w14_compatible_rollback_reads_v2_and_writes_only_v1(client, on):
    sid, ifc, ids = _project(client)
    _linked(client, sid, ifc, ids)
    digest = view_model.clearance_view(_snap(sid), ifc, appmod._PCC_BINDING)["record"]["digest"]
    appmod.app.config["PCC_SOURCE_BINDING_WRITES"] = False         # the rollback target
    page = client.get(_url(sid, ifc))
    body = _body(page)
    assert page.status_code == 200 and 'data-pcc-agreement="EXACT"' in body
    assert "data-pcc-source-form" not in body
    assert view_model.clearance_view(_snap(sid), ifc, appmod._PCC_BINDING)["record"]["digest"] == digest
    resp, _ = _save(client, sid, ifc, ids, page, values=("84", "50", "88", "56", "2"))
    assert resp.status_code == 200
    record = _snap(sid)["ledger"].records[0]
    assert record.current.source is None and len(_bindings(sid)) == 1     # no carry-forward
    appmod.app.config["PCC_SOURCE_BINDING_WRITES"] = True          # re-upgrade
    _linked(client, sid, ifc, ids, values=("84", "50", "88", "56", "2"))
    assert len(_bindings(sid)) == 2
    assert _snap(sid)["ledger"].records[0].current.source is not None


def test_w15_digests_cad_companion_and_stale_links(client, on):
    sid, ifc, ids = _project(client)
    # a v1 declaration: the digest is the legacy digest; the companion has no source
    resp, _ = _save(client, sid, ifc, ids, client.get(_url(sid, ifc)))
    record = _snap(sid)["ledger"].records[0]
    view = view_model.clearance_view(_snap(sid), ifc, appmod._PCC_BINDING)
    assert view["record"]["digest"] == _legacy_digest(record)
    link = re.search(r'href="([^"]+cad\.zip[^"]+)"', _body(client.get(_url(sid, ifc)))).group(1)
    z = zipfile.ZipFile(io.BytesIO(client.get(link.replace("&amp;", "&")).get_data()))
    assert "source" not in json.loads(z.read("companion.json"))
    # a v2 correction: new digest, the old link is stale, the companion carries the source
    _linked(client, sid, ifc, ids, values=("80", "50", "86", "56", "2"))
    assert client.get(link.replace("&amp;", "&")).status_code == 409
    record = _snap(sid)["ledger"].records[0]
    assert view_model.snapshot_digest(record) != _legacy_digest(record)
    link2 = re.search(r'href="([^"]+cad\.zip[^"]+)"', _body(client.get(_url(sid, ifc)))).group(1)
    z = zipfile.ZipFile(io.BytesIO(client.get(link2.replace("&amp;", "&")).get_data()))
    companion = json.loads(z.read("companion.json"))
    src = companion["source"]
    assert src["sha256"] == hashlib.sha256(_bytes("k10_board_v1")).hexdigest()
    assert src["sha256"] != companion["dxf"]["sha256"]
    assert src["agreement"] == "DIFFERS" and src["changed_axes"] == ["x"]
    assert src["file_outline_mm"] == {"board_x": "84", "board_y": "50"}
    assert src["declared_board_mm"] == {"board_x": "80", "board_y": "50"}
    assert src["carried_forward"] is False
    assert companion["declared_values"]["board_x"] == "80"            # geometry = declared
    # a different file is a different digest for the same declared material
    m = record.current
    other = dataclasses.replace(m, source=dataclasses.replace(m.source, source_sha256="0" * 64))
    rec2 = dataclasses.replace(record, revisions=record.revisions[:-1] + (
        dataclasses.replace(record.revisions[-1], material=other),))
    assert view_model.snapshot_digest(rec2) != view_model.snapshot_digest(record)


def test_w16_privacy_no_raw_file_name_or_token_is_retained(client, on, caplog):
    sid, ifc, ids = _project(client)
    data = _bytes("k10_board_v1")
    with caplog.at_level("DEBUG"):
        offer = _inspect(client, sid, ifc, ids, data, filename="PRIVATE-NAME-55.kicad_pcb")
        token = _fields(_body(offer))["source_token"]
        _save(client, sid, ifc, ids, offer)
    dump = _dump()
    uuid_in_file = re.search(rb'\(uuid "([^"]+)"\)', data).group(1).decode()
    for needle in ("PRIVATE-NAME-55", token, token.split(".")[1], uuid_in_file, "Edge.Cuts"):
        assert needle not in dump
        assert needle not in caplog.text
    assert "PRIVATE-NAME-55" not in _body(client.get(_url(sid, ifc)))


def test_w17_report_and_pdf_render_the_link_in_both_languages(client, on, monkeypatch):
    sid, ifc, ids = _project(client)
    _linked(client, sid, ifc, ids, values=("80", "50", "86", "56", "2"))
    report = _body(client.get("/session/%s/deliverable" % sid))
    assert "data-pcc-source-link" in report and 'data-pcc-agreement="DIFFERS"' in report
    pdf = _pdf_source(client, sid, monkeypatch)
    assert "data-pcc-source-link" in pdf and 'data-pcc-agreement="DIFFERS"' in pdf
    assert client.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    page = _body(client.get(_url(sid, ifc)))
    assert ui_text.text("UI_PCC_SRC_LINKED", "ar") in page
    assert ui_text.text("UI_PCC_SRC_CALC_USES", "ar") in page
    assert '<bdi dir="ltr" data-pcc-file-outline>84 × 50 mm</bdi>' in page
    report = _body(client.get("/session/%s/deliverable" % sid))
    assert ui_text.text("UI_PCC_SRC_AGREE_DIFFERS", "ar") in report
    pdf = _pdf_source(client, sid, monkeypatch)
    assert ui_text.text("UI_PCC_SRC_AGREE_DIFFERS", "ar") in pdf


def test_w18_every_source_string_exists_in_both_languages():
    keys = [k for k in ui_text.UI_STRINGS if k.startswith("UI_PCC_SRC_")]
    assert len(keys) >= 30
    for code in R.REFUSAL_CODES:
        assert "UI_PCC_SRC_REFUSED_" + code in keys
    for key in keys:
        assert ui_text.text(key, "en") and ui_text.text(key, "ar")
        assert ui_text.text(key, "en") != ui_text.text(key, "ar")
        assert "verified" not in ui_text.text(key, "en").replace("does not verify", "")


def test_w19_unauthorized_or_foreign_requests_are_denied(client, on):
    sid, ifc, ids = _project(client)
    sid2, ifc2, ids2 = _project(client)
    before = _dump()
    # another project's interaction under this project: the non-enumerating denial
    form = {"csrf_token": _csrf(client, sid, ifc), "board_component_id": ids2[0],
            "enclosure_component_id": ids2[1],
            "board_file": _file(_bytes("k10_board_v1"), "b.kicad_pcb")}
    resp = client.post(_url(sid, ifc2, "/board-source"), data=form,
                       content_type="multipart/form-data")
    assert resp.status_code == 302 and "data-pcc-source-offer" not in _body(resp)
    # a foreign component pair is refused
    resp = _inspect(client, sid, ifc, [ids[0], ids2[1]], _bytes("k10_board_v1"))
    assert resp.status_code == 409
    # no project access and no CSRF token: refused before the route
    with appmod.app.test_client() as anonymous:
        resp = anonymous.post(_url(sid, ifc, "/board-source"),
                              data={"board_component_id": ids[0], "enclosure_component_id": ids[1],
                                    "board_file": _file(_bytes("k10_board_v1"), "b.kicad_pcb")},
                              content_type="multipart/form-data")
        assert resp.status_code in (302, 400, 403)
        assert "data-pcc-source-offer" not in _body(resp)
    assert _dump() == before


# ==========================================================================
# Q. the route-scoped request class
# ==========================================================================
def test_q01_intake_files_are_buffered_in_memory_never_spooled(client, on, monkeypatch):
    import tempfile
    import werkzeug.formparser as fp
    calls = []

    def boom(*a, **k):
        calls.append(1)
        raise AssertionError("a temporary file was created")

    monkeypatch.setattr(fp, "SpooledTemporaryFile", boom, raising=False)
    monkeypatch.setattr(fp, "TemporaryFile", boom, raising=False)
    monkeypatch.setattr(tempfile, "SpooledTemporaryFile", boom)
    monkeypatch.setattr(tempfile, "TemporaryFile", boom)
    monkeypatch.setattr(tempfile, "NamedTemporaryFile", boom)
    sid, ifc, ids = _project(client)
    assert _inspect(client, sid, ifc, ids, _bytes("k10_board_v1")).status_code == 200
    # malformed multipart, oversized, too many parts and unauthorized: refused, nothing spooled
    csrf = _csrf(client, sid, ifc)
    resp = client.post(_url(sid, ifc, "/board-source"),
                       data=b"--x\r\nContent-Disposition: form-data; name=\"a\"\r\n\r\n",
                       content_type="multipart/form-data; boundary=x")
    assert resp.status_code in (400, 403)
    big = {"csrf_token": csrf, "board_file": _file(b"x" * (130 * 1024), "b.kicad_pcb")}
    resp = client.post(_url(sid, ifc, "/board-source"), data=big, content_type="multipart/form-data")
    assert resp.status_code == 413
    parts = {"csrf_token": csrf, "board_file": _file(b"x", "b.kicad_pcb")}
    parts.update({"f%d" % i: "v" for i in range(20)})
    resp = client.post(_url(sid, ifc, "/board-source"), data=parts, content_type="multipart/form-data")
    assert resp.status_code == 413
    with appmod.app.test_client() as anonymous:
        resp = anonymous.post(_url(sid, ifc, "/board-source"),
                              data={"board_file": _file(_bytes("k10_board_v1"), "b.kicad_pcb")},
                              content_type="multipart/form-data")
        assert resp.status_code in (302, 400, 403)
    assert calls == []


def test_q02_other_endpoints_keep_the_framework_defaults():
    with appmod.app.test_request_context("/session/x/interface-clearance/y", method="POST"):
        from flask import request
        assert request.max_form_parts == 1000
        assert not isinstance(request._get_file_stream(10, "text/plain"), io.BytesIO)
    with appmod.app.test_request_context("/session/x/interface-clearance/y/board-source",
                                         method="POST"):
        from flask import request
        assert request.max_form_parts == 16
        assert isinstance(request._get_file_stream(10, "text/plain"), io.BytesIO)


# ==========================================================================
# S. the Stage-15 binding and the record-store sidecar
# ==========================================================================
def test_s01_store_refuses_v2_unless_explicitly_allowed(client, on):
    sid, ifc, ids = _project(client)
    _linked(client, sid, ifc, ids)
    record = _snap(sid)["ledger"].records[0]
    snap = _snap(sid)
    m = record.current
    material = sm.planar_clearance_material(
        snap["inventory"], snap["interfaces"], snap["participations"], snap["epochs"], ifc,
        m.board_component_id, m.enclosure_component_id, m.board_component_revision,
        m.enclosure_component_revision, m.board_participation_epoch,
        m.enclosure_participation_epoch, m.region_description, ("84", "50", "90", "56", "2"),
        m.basis, m.applicability,
        source=dataclasses.replace(m.source, nonce_hash="a" * 64))
    rev = sm.corrected_planar_clearance(snap["ledger"], record.declaration_id,
                                        record.head_revision_no, material)
    with pytest.raises(rs.PlanarClearanceRejected):
        appmod._get_store().append_planar_clearance_revision(sid, rev, "k-test-1")
    assert len(_snap(sid)["ledger"].records[0].revisions) == 1


def test_s02_bindings_are_insert_only_and_removed_only_with_their_revision(client, on):
    sid, ifc, ids = _project(client)
    _linked(client, sid, ifc, ids)
    conn = _db()
    try:
        conn.execute("PRAGMA foreign_keys = ON")
        with pytest.raises(sqlite3.DatabaseError):
            conn.execute("UPDATE planar_clearance_source_bindings SET file_x = '80'")
        with pytest.raises(sqlite3.DatabaseError):
            conn.execute("DELETE FROM planar_clearance_source_bindings")
        conn.rollback()
        # an authorized complete-project deletion (every row of the project, children first)
        tables = [r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
        with conn:
            conn.execute("DELETE FROM planar_clearance_revisions WHERE project_id = ?", (sid,))
        assert conn.execute("SELECT COUNT(*) FROM planar_clearance_source_bindings "
                            "WHERE project_id = ?", (sid,)).fetchone()[0] == 0
        assert "planar_clearance_source_bindings" in tables
    finally:
        conn.close()


def _break(sql, *params):
    conn = _db()
    try:
        conn.execute("DROP TRIGGER planar_clearance_source_bindings_no_update")
        conn.execute("DROP TRIGGER planar_clearance_source_bindings_no_delete")
        conn.execute(sql, params)
        conn.commit()
        for _name, ddl in rs._PCC_SOURCE_TRIGGERS:
            conn.execute(ddl)
        conn.commit()
    finally:
        conn.close()


@pytest.mark.parametrize("damage", ["missing", "malformed", "orphan", "trigger"])
def test_s03_a_damaged_binding_makes_everything_unavailable(client, on, damage):
    sid, ifc, ids = _project(client)
    _linked(client, sid, ifc, ids)
    if damage == "missing":
        _break("DELETE FROM planar_clearance_source_bindings WHERE project_id = ?", sid)
    elif damage == "malformed":
        _break("UPDATE planar_clearance_source_bindings SET file_x = 'abc' WHERE project_id = ?", sid)
    elif damage == "orphan":
        page = client.get(_url(sid, ifc))
        _save(client, sid, ifc, ids, page, values=("80", "50", "86", "56", "2"))   # v1 head
        rev = _snap(sid)["ledger"].records[0].current_revision.revision_id
        row = list(_bindings(sid)[0])
        row[1], row[12] = rev, "b" * 64
        _break("INSERT INTO planar_clearance_source_bindings VALUES (%s)"
               % ",".join("?" * len(row)), *row)
    else:
        conn = _db()
        conn.execute("DROP TRIGGER planar_clearance_source_bindings_no_update")
        conn.commit()
        conn.close()
    with pytest.raises(rs.PlanarClearanceCorrupt):
        _snap(sid)
    page = client.get(_url(sid, ifc))
    assert page.status_code == 503 and "data-pcc-unavailable" in _body(page)
    assert client.get(_url(sid, ifc, "/cad.zip?revision=x&digest=y")).status_code in (409, 503)
    resp = _inspect(client, sid, ifc, ids, _bytes("k10_board_v1"))
    assert resp.status_code == 503


def test_s04_revision_and_binding_are_written_atomically(client, on):
    sid, ifc, ids = _project(client)
    conn = _db()
    conn.execute("CREATE TRIGGER t_fail BEFORE INSERT ON planar_clearance_source_bindings "
                 "BEGIN SELECT RAISE(ABORT, 'injected'); END")
    conn.commit()
    conn.close()
    try:
        offer = _inspect(client, sid, ifc, ids, _bytes("k10_board_v1"))
        resp, _ = _save(client, sid, ifc, ids, offer)
        assert resp.status_code == 503
        assert _snap(sid)["ledger"].records == ()
        conn = _db()
        assert conn.execute("SELECT COUNT(*) FROM planar_clearance_revisions WHERE project_id = ?",
                            (sid,)).fetchone()[0] == 0
    finally:
        conn = _db()
        conn.execute("DROP TRIGGER t_fail")
        conn.commit()
        conn.close()


def test_s05_history_validation_rules():
    src = sm.PlanarClearanceSource(
        kind="kicad_pcb", source_sha256="a" * 64, source_size=10, format_id="f", reader_id="r",
        rule_id="u", file_x="84", file_y="50", axis_assignment="file_x_is_board_x",
        inspected_at="t", nonce_hash="c" * 64, carry_forward_from=None)
    sm.check_planar_clearance_source(src)
    for bad in (dict(nonce_hash=None), dict(carry_forward_from="pcr-" + "0" * 32),
                dict(file_x="84.12345"), dict(file_x="0"), dict(axis_assignment="rotate"),
                dict(source_sha256="A" * 64), dict(source_size=0), dict(kind="dxf")):
        with pytest.raises(sm.PlanarClearanceError):
            sm.check_planar_clearance_source(dataclasses.replace(src, **bad))


def test_s06_migration_is_additive_idempotent_and_refuses_unknown_shapes(tmp_path):
    path = str(tmp_path / "db.sqlite")
    store = rs.SqliteRecordStore(path)
    store.close()
    store = rs.SqliteRecordStore(path)                               # idempotent
    store.close()
    conn = sqlite3.connect(path)
    conn.execute("DROP TRIGGER planar_clearance_source_bindings_no_update")
    conn.execute("DROP TRIGGER planar_clearance_source_bindings_no_delete")
    conn.execute("DROP TABLE planar_clearance_source_bindings")      # a pre-change database
    conn.commit()
    conn.close()
    rs.SqliteRecordStore(path).close()                               # upgrade
    conn = sqlite3.connect(path)
    cols = tuple(r[1] for r in conn.execute("PRAGMA table_info(planar_clearance_source_bindings)"))
    assert cols == rs._PCC_SOURCE_COLUMNS
    conn.execute("DROP TRIGGER planar_clearance_source_bindings_no_update")
    conn.execute("DROP TRIGGER planar_clearance_source_bindings_no_delete")
    conn.execute("DROP TABLE planar_clearance_source_bindings")
    conn.execute("CREATE TABLE planar_clearance_source_bindings (x TEXT)")
    conn.commit()
    conn.close()
    with pytest.raises(sqlite3.DatabaseError):
        rs.SqliteRecordStore(path)


def test_s07_the_method_and_its_declaration_constant_are_unchanged():
    assert pcc.DECLARATION_VERSION == "planar-clearance-declaration/1"
    assert pcc.METHOD_ID == "mechanical:planar_centered_rectangular_clearance"
    assert pcc.METHOD_VERSION == "1.0"
    for f in ("engine/mechanical_planar_clearance.py", "engine/mechanical_planar_clearance_method.py"):
        assert "planar_clearance_board_source" not in open(os.path.join(ROOT, f), encoding="utf-8").read()
