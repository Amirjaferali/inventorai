"""PCB-OUTLINE-TO-PLANAR-CLEARANCE-PROOF-01 — isolated engineering proof (synthetic only).

One question: can a KiCad board file feed InventorAI's EXISTING planar-clearance method
(`mechanical:planar_centered_rectangular_clearance` 1.0) and its EXISTING CAD download
(PR #917) truthfully, with unsupported geometry refused, and does a changed board file
produce a detectable difference without anything being silently kept current?

What this is: a proof harness. It runs `kicad-cli` (an external program, only where it is
installed) on the synthetic fixtures, reads the exported DXF with its own small group-code
reader, compares the result with the board file's own text, then drives the REAL product
routes through the Flask test client on a scratch database exactly as an inventor would:
the extracted values are typed into the existing declaration form by the harness acting as
the inventor, with the eight applicability declarations answered explicitly; nothing is
accepted automatically. It is never imported by `engine/` or `web/`, adds no dependency
and changes no product behaviour.

What it is not: PCB-enclosure compatibility, manufacturability, electrical validity,
mounting, height, tolerance or safety; a source-file revision lifecycle (InventorAI has
none: the source-digest comparison below is this harness's own check, not product
behaviour); or a qualification of any other KiCad version or geometry.

Usage (writes the evidence folder; needs `kicad-cli` on PATH):
    python3 scripts/pcb_outline_planar_clearance_proof.py
"""
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from decimal import Decimal

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVIDENCE = os.path.join(_ROOT, "docs", "benchmarks", "evidence", "pcb_outline_planar_clearance_v1")
FIXTURES = os.path.join(EVIDENCE, "fixtures")
EXPORTS = os.path.join(EVIDENCE, "exports")
RECORD = os.path.join(EVIDENCE, "proof_record.json")

SUPPORTED_FILE_VERSION = "20221018"        # the KiCad 7 board-file format this proof pins
TOLERANCE_MM = Decimal("1e-9")             # measurement tolerance of THIS proof, not a method tolerance
EXPORT_ARGS = ("pcb", "export", "dxf", "--layers", "Edge.Cuts", "--output-units", "mm",
               "--exclude-refdes", "--exclude-value")
POSITIVE = ("board_v1", "board_v1_lines", "board_v2")
NEGATIVE = ("neg_rounded_corners", "neg_l_shape", "neg_cutout", "neg_two_boards",
            "neg_open_outline", "neg_no_outline", "neg_rotated")
UNITS_CONTROL = "board_v1_inch_export"     # the supported board exported in inches


class Refused(Exception):
    """The geometry is not one supported rectangle; nothing is inferred."""


def sha256(data):
    return hashlib.sha256(data).hexdigest()


# --- 1. the board file's own text (exact decimals) ----------------------------------------
def _sexpr(text):
    tokens = re.findall(r'\(|\)|"(?:[^"\\]|\\.)*"|[^\s()"]+', text)
    stack, root = [], []
    cur = root
    for tok in tokens:
        if tok == "(":
            stack.append(cur)
            cur.append([])
            cur = cur[-1]
        elif tok == ")":
            if not stack:
                raise Refused("malformed board file")
            cur = stack.pop()
        else:
            cur.append(tok[1:-1] if tok.startswith('"') else tok)
    if stack or len(root) != 1 or not root[0] or root[0][0] != "kicad_pcb":
        raise Refused("not a KiCad board file")
    return root[0]


def _field(node, name):
    for child in node[1:]:
        if isinstance(child, list) and child and child[0] == name:
            return child
    return None


def _on_edge(node):
    layer = _field(node, "layer")
    return layer is not None and len(layer) > 1 and layer[1] == "Edge.Cuts"


def _point(node, name):
    p = _field(node, name)
    if p is None or len(p) < 3:
        raise Refused("graphic without %s point" % name)
    return Decimal(p[1]), Decimal(p[2])


def source_rectangle(text):
    """The rectangle written in the board file, as exact decimals (width, height), or
    Refused. Supported: exactly one `gr_rect`, or exactly four axis-aligned `gr_line`
    forming one closed rectangle, on Edge.Cuts; nothing else on Edge.Cuts anywhere."""
    board = _sexpr(text)
    version = _field(board, "version")
    if version is None or version[1] != SUPPORTED_FILE_VERSION:
        raise Refused("board-file format version is not the pinned %s" % SUPPORTED_FILE_VERSION)
    edge = [n for n in board[1:] if isinstance(n, list) and n and n[0].startswith("gr_") and _on_edge(n)]
    for fp in (n for n in board[1:] if isinstance(n, list) and n and n[0] == "footprint"):
        if any(isinstance(g, list) and g and g[0].startswith("fp_") and _on_edge(g) for g in fp[1:]):
            raise Refused("outline graphics inside a footprint")
    if not edge:
        raise Refused("no Edge.Cuts outline")
    kinds = sorted({n[0] for n in edge})
    if kinds == ["gr_rect"] and len(edge) == 1:
        (x1, y1), (x2, y2) = _point(edge[0], "start"), _point(edge[0], "end")
        return _rect_from_points([(x1, y1), (x2, y1), (x2, y2), (x1, y2)])
    if kinds == ["gr_line"]:
        segments = [(_point(n, "start"), _point(n, "end")) for n in edge]
        return _closed_rectangle(segments)
    if kinds == ["gr_rect"]:
        raise Refused("%d separate rectangles on Edge.Cuts, not one outline" % len(edge))
    raise Refused("unsupported Edge.Cuts shapes: %s" % ", ".join(kinds))


def _rect_from_points(points):
    xs, ys = sorted({p[0] for p in points}), sorted({p[1] for p in points})
    if len(xs) != 2 or len(ys) != 2:
        raise Refused("not an axis-aligned rectangle")
    width, height = xs[1] - xs[0], ys[1] - ys[0]
    if width <= 0 or height <= 0:
        raise Refused("degenerate rectangle")
    return width, height


def _exact(a, b):
    return a == b


def _closed_rectangle(segments, close=_exact):
    """Exactly four horizontal / vertical segments forming ONE closed loop."""
    if len(segments) != 4:
        raise Refused("%d outline segments, not the four of one rectangle" % len(segments))
    for (ax, ay), (bx, by) in segments:
        if not (close(ax, bx) or close(ay, by)):
            raise Refused("a segment is not axis-aligned")
        if close(ax, bx) and close(ay, by):
            raise Refused("zero-length segment")
    ends = [p for seg in segments for p in seg]
    for p in ends:
        if sum(1 for q in ends if close(p[0], q[0]) and close(p[1], q[1])) != 2:
            raise Refused("the outline is not closed")
    return _rect_from_points_tol(ends, close)


def _rect_from_points_tol(points, close):
    xs, ys = [], []
    for x, y in points:
        if not any(close(x, v) for v in xs):
            xs.append(x)
        if not any(close(y, v) for v in ys):
            ys.append(y)
    if len(xs) != 2 or len(ys) != 2:
        raise Refused("not an axis-aligned rectangle")
    return abs(xs[1] - xs[0]), abs(ys[1] - ys[0])


# --- 2. the KiCad DXF export, read with this proof's own group-code reader ------------------
def dxf_pairs(text):
    lines = text.splitlines()
    if len(lines) % 2:
        raise Refused("malformed DXF")
    return [(lines[i].strip(), lines[i + 1].strip()) for i in range(0, len(lines), 2)]


def dxf_header(pairs):
    head = {}
    for i, (code, value) in enumerate(pairs):
        if code == "9" and i + 1 < len(pairs):
            head[value] = pairs[i + 1][1]
        if code == "0" and value == "ENDSEC" and head:
            break
    return head


def dxf_entities(pairs):
    out, inside, cur = [], False, None
    for code, value in pairs:
        if code == "2" and value == "ENTITIES":
            inside = True
            continue
        if not inside:
            continue
        if code == "0":
            if cur is not None:
                out.append(cur)
            if value in ("ENDSEC", "EOF"):
                return out
            cur = {"type": value, "codes": []}
        elif cur is not None:
            cur["codes"].append((code, value))
    raise Refused("DXF has no closed ENTITIES section")


def export_rectangle(dxf_text):
    """(width, height) in mm measured from the KiCad Edge.Cuts export, or Refused.
    Only LINE entities are accepted; the export must declare metric measurement."""
    pairs = dxf_pairs(dxf_text)
    head = dxf_header(pairs)
    if head.get("$MEASUREMENT") != "1":
        raise Refused("export is not metric ($MEASUREMENT %s)" % head.get("$MEASUREMENT"))
    if "$INSUNITS" in head and head["$INSUNITS"] != "4":
        raise Refused("export units are not millimetres")
    ents = dxf_entities(pairs)
    if not ents:
        raise Refused("no outline in the export")
    kinds = sorted({e["type"] for e in ents})
    if kinds != ["LINE"]:
        raise Refused("unsupported export entities: %s" % ", ".join(kinds))
    segments = []
    for e in ents:
        c = dict(e["codes"])
        segments.append(((Decimal(c["10"]), Decimal(c["20"])), (Decimal(c["11"]), Decimal(c["21"]))))
    return _closed_rectangle(segments, close=lambda a, b: abs(a - b) <= TOLERANCE_MM)


def lwpolylines(dxf_text):
    """{layer: [(x, y), ...]} of the closed LWPOLYLINEs of an exported CAD reference."""
    out = {}
    for e in dxf_entities(dxf_pairs(dxf_text)):
        if e["type"] != "LWPOLYLINE":
            continue
        layer = next((v for c, v in e["codes"] if c == "8"), None)
        flags = int(next((v for c, v in e["codes"] if c == "70"), "0"))
        xs = [Decimal(v) for c, v in e["codes"] if c == "10"]
        ys = [Decimal(v) for c, v in e["codes"] if c == "20"]
        if not flags & 1 or any(c == "42" and Decimal(v) != 0 for c, v in e["codes"]):
            raise Refused("CAD outline is open or curved")
        out[layer] = list(zip(xs, ys))
    return out


def extent(points):
    xs, ys = [p[0] for p in points], [p[1] for p in points]
    return max(xs) - min(xs), max(ys) - min(ys)


# --- 3. one fixture through KiCad, the export reader and the source cross-check -----------
def kicad_version():
    return subprocess.run(["kicad-cli", "version"], capture_output=True, text=True,
                          check=True).stdout.strip()


def run_kicad(name, inches=False):
    src = os.path.join(FIXTURES, name + ".kicad_pcb")
    out = os.path.join(EXPORTS, (UNITS_CONTROL if inches else name) + ".dxf")
    args = list(EXPORT_ARGS)
    if inches:
        args[args.index("mm")] = "in"
    cmd = ["kicad-cli"] + args + ["-o", out, src]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return {"command": " ".join(["kicad-cli"] + args + ["-o", os.path.relpath(out, EVIDENCE),
                                                         os.path.relpath(src, EVIDENCE)]),
            "returncode": proc.returncode, "exported": os.path.exists(out)}


def _plain(value):
    """An exact decimal in plain notation (never exponent form), trailing zeros dropped."""
    text = format(value, "f")
    return text.rstrip("0").rstrip(".") if "." in text else text


def judge(name, export_name=None):
    """The independent decision for one fixture: both readings must agree exactly
    (within TOLERANCE_MM) on ONE supported rectangle, otherwise it is refused."""
    src = open(os.path.join(FIXTURES, name + ".kicad_pcb"), encoding="utf-8").read()
    dxf_path = os.path.join(EXPORTS, (export_name or name) + ".dxf")
    result = {"source_sha256": sha256(src.encode("utf-8"))}
    try:
        source = source_rectangle(src)
        result["source_mm"] = [str(v) for v in source]
    except Refused as exc:
        source, result["source_refused"] = None, str(exc)
    if os.path.exists(dxf_path):
        raw = open(dxf_path, "rb").read()
        result["export_sha256"] = sha256(raw)
        try:
            measured = export_rectangle(raw.decode("utf-8"))
            result["export_mm"] = [str(v) for v in measured]
        except Refused as exc:
            measured, result["export_refused"] = None, str(exc)
    else:
        measured, result["export_refused"] = None, "KiCad wrote no export"
    agree = (source is not None and measured is not None
             and all(abs(a - b) <= TOLERANCE_MM for a, b in zip(source, measured)))
    result["supported"] = agree
    if agree:
        result["declared_mm"] = [_plain(v) for v in source]   # the value of record
    elif source is not None and measured is not None:
        result["refused"] = "the export and the board file disagree"
    return result


# --- 4. the REAL product routes, acting as the inventor --------------------------------------
REGION_X, REGION_Y, CLEARANCE = "86", "56", "2"


def _basis_note(name, judged, tool):
    return ("KiCad board file %s.kicad_pcb, SHA-256 %s; Edge.Cuts rectangle exported by %s "
            "and checked: %s x %s mm" % (name, judged["source_sha256"], tool,
                                         judged["declared_mm"][0], judged["declared_mm"][1]))


def product_route(judged_v1, judged_v2, tool):
    os.environ.setdefault("INVENTORAI_DB_PATH",
                          os.path.join(tempfile.mkdtemp(prefix="pcb_proof_"), "proof.db"))
    sys.path.insert(0, _ROOT)
    import web.app as appmod
    from tests.csrf_client import csrf_client
    from tests.test_g1_pcc_literal_source_aid import _project, _submit, _url, _body
    appmod.app.config["TESTING"] = True
    store = appmod._get_store

    def page_state(body):
        return {"outcome": re.findall(r'data-pcc-outcome="(\w+)"', body),
                "margins": [m.strip() for m in re.findall(r"data-pcc-margin[^>]*>([^<]+)<", body)
                            if m.strip()],
                "revision": re.findall(r"data-pcc-revision[^>]*>([^<]+)<", body),
                "digest": re.findall(r"data-pcc-digest[^>]*>([^<]+)<", body),
                "cad": [h.replace("&amp;", "&") for h in
                        re.findall(r'<a href="([^"]+)" data-pcc-cad-link', body)]}

    def bundle(client, href):
        resp = client.get(href)
        out = {"status": resp.status_code, "content_type": resp.headers.get("Content-Type")}
        if resp.status_code != 200:
            return out, None
        raw = resp.get_data()
        z = zipfile.ZipFile(io.BytesIO(raw))
        dxf = z.read("geometry.dxf")
        comp = json.loads(z.read("companion.json"))
        polys = lwpolylines(dxf.decode("utf-8"))
        out.update({
            "zip_sha256": sha256(raw), "files": z.namelist(), "dxf_sha256": sha256(dxf),
            "companion_binds_dxf": comp["dxf"]["sha256"] == sha256(dxf),
            "declared_values": comp["declared_values"], "outcome": comp["evaluation"]["outcome"],
            "margins_mm": [a["margin_mm"] for a in comp["evaluation"]["axes"]],
            "revision": comp["binding"]["declaration_revision_no"],
            "snapshot_digest": comp["binding"]["snapshot_digest"],
            "measured_mm": {layer: [str(v) for v in extent(pts)] for layer, pts in polys.items()},
            "source_digest_in_bundle": judged_v1["source_sha256"] in raw.decode("latin-1")})
        return out, raw

    record = {}
    with csrf_client(appmod.app) as c:
        sid, ifc, ids = _project(c, "A small weather station: a circuit board inside a plastic case.")
        bx, by = judged_v1["declared_mm"]
        note1 = _basis_note("board_v1", judged_v1, tool)
        r = _submit(c, sid, ifc, ids, bx, by, note1,
                    extra={"value_region_x": REGION_X, "value_region_y": REGION_Y,
                           "value_c": CLEARANCE})
        state0 = page_state(_body(c.get(_url(sid, ifc))))
        record["declare_v1"] = {"status": r.status_code, "page": state0}
        cad0, raw0 = bundle(c, state0["cad"][0])
        record["cad_v1"] = cad0
        stored = store().load_planar_clearance(sid)
        stored_text = json.dumps(stored, default=lambda o: getattr(o, "__dict__", str(o)))

        # The board file changes. InventorAI keeps no source file and no source lifecycle, so
        # the product page still shows the v1 declaration as current; only this harness can
        # see that the presented file no longer matches the digest the declaration names.
        before = page_state(_body(c.get(_url(sid, ifc))))
        record["source_change"] = {
            "v1_source_sha256": judged_v1["source_sha256"],
            "v2_source_sha256": judged_v2["source_sha256"],
            "stored_note_names_v1_digest": judged_v1["source_sha256"] in stored_text,
            "stored_note_names_v2_digest": judged_v2["source_sha256"] in stored_text,
            "harness_verdict": ("SOURCE MISMATCH: the current declaration names a different "
                                "board file; its result does not describe the presented source"
                                if judged_v2["source_sha256"] not in stored_text else "MATCH"),
            "product_page_before_redeclaration": before}

        bx2, by2 = judged_v2["declared_mm"]
        note2 = _basis_note("board_v2", judged_v2, tool)
        r2 = _submit(c, sid, ifc, ids, bx2, by2, note2,
                     extra={"value_region_x": REGION_X, "value_region_y": REGION_Y,
                            "value_c": CLEARANCE})
        state1 = page_state(_body(c.get(_url(sid, ifc))))
        record["redeclare_v2"] = {"status": r2.status_code, "page": state1}
        cad1, raw1 = bundle(c, state1["cad"][0])
        record["cad_v2"] = cad1
        stale = c.get(state0["cad"][0])
        record["old_cad_link_after_change"] = {
            "status": stale.status_code, "content_type": stale.headers.get("Content-Type")}
    return record, raw0, raw1


def main():
    if shutil.which("kicad-cli") is None:
        print(json.dumps({"verdict": "BLOCKED", "cause": "kicad-cli is not on PATH"}))
        return 2
    tool = "kicad-cli " + kicad_version()
    os.makedirs(EXPORTS, exist_ok=True)
    runs, judged = {}, {}
    for name in POSITIVE + NEGATIVE:
        runs[name] = run_kicad(name)
        judged[name] = judge(name)
    runs[UNITS_CONTROL] = run_kicad("board_v1", inches=True)
    judged[UNITS_CONTROL] = judge("board_v1", export_name=UNITS_CONTROL)
    product, raw0, raw1 = product_route(judged["board_v1"], judged["board_v2"], tool)
    with open(os.path.join(EVIDENCE, "cad_v1.zip"), "wb") as fh:
        fh.write(raw0)
    with open(os.path.join(EVIDENCE, "cad_v2.zip"), "wb") as fh:
        fh.write(raw1)
    record = {"proof": "PCB-OUTLINE-TO-PLANAR-CLEARANCE-PROOF-01", "synthetic_only": True,
              "tool": tool, "kicad_package": "Ubuntu 24.04 kicad 7.0.11+dfsg-1build4 (GPL-3+)",
              "kicad_cli_sha256": sha256(open(shutil.which("kicad-cli"), "rb").read()),
              "board_file_version": SUPPORTED_FILE_VERSION, "tolerance_mm": str(TOLERANCE_MM),
              "method": "mechanical:planar_centered_rectangular_clearance 1.0",
              "inventor_inputs": {"region_x": REGION_X, "region_y": REGION_Y, "c": CLEARANCE,
                                  "declarations": "all eight answered 'applies' explicitly"},
              "kicad_runs": runs, "geometry": judged, "product_route": product}
    with open(RECORD, "w", encoding="utf-8") as fh:
        json.dump(record, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print(json.dumps({k: record[k] for k in ("tool", "board_file_version")}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
