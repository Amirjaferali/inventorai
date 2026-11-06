"""KICAD10-FORMAT-QUALIFICATION-PROOF-01 — isolated format proof (synthetic only).

Establishes which board-file format KiCad 10.0.8 writes and whether the PR #933 bounded
admission rule accepts its single-rectangle Edge.Cuts outline exactly while never
admitting unsupported geometry, under the criteria frozen in
`docs/benchmarks/evidence/kicad10_format_qualification_v1/preregistration.json`.

Reuse, unchanged: the #933 readers and rules (`scripts/pcb_outline_planar_clearance_proof.py`)
and the #934 sandbox runner (`scripts/mp01_speed_controlled_dcpm_proof.run_sandboxed` with
`scripts/mp01_sandbox/inner.sh`): host uid 65534 holding no host capabilities, with
`no_new_privs`, unprivileged user/mount/pid/net/ipc/uts namespaces, `prlimit` limits, a
read-only image root after `pivot_root`, no network and a cleared environment. Inside its
user namespace the tool runs as that namespace's root, mapped to host uid 65534. The
runner's read-only mount (named `/msl` by the MP-01 script) carries this proof's inputs.

Added here only: the child-field allowlist and the observed-version parameter of the
admission rule. Proof-only: nothing in `engine/` or `web/` imports it; no product change.

Usage (needs the prepared stage /srv/kicad10 with rootfs/ and the verified blobs/):
    python3 scripts/kicad10_format_qualification_proof.py
"""
import json
import os
import re
import shutil
import sys
import time

os.environ.setdefault("MP01_STAGE", "/srv/kicad10")
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _ROOT)
from scripts import pcb_outline_planar_clearance_proof as P   # noqa: E402  (#933, reused)
from scripts import mp01_speed_controlled_dcpm_proof as M      # noqa: E402  (#934, reused)

STAGE = os.environ["MP01_STAGE"]
EVIDENCE = os.path.join(_ROOT, "docs", "benchmarks", "evidence", "kicad10_format_qualification_v1")
PREREG = os.path.join(EVIDENCE, "preregistration.json")
K7_FIXTURES = P.FIXTURES
INPUTS = os.path.join(STAGE, "msl")          # the runner's read-only mount
WORK = os.path.join(STAGE, "work")
ALLOWED = {"gr_rect": {"start", "end", "stroke", "fill", "layer", "uuid", "tstamp", "locked"},
           "gr_line": {"start", "end", "stroke", "layer", "uuid", "tstamp", "locked"}}
SUPPORTED = ("k10_board_v1", "k10_board_v1_lines", "k10_board_v2",
             "up_board_v1", "up_board_v1_lines", "up_board_v2")
EXPECTED = {"k10_board_v1": ("84", "50"), "k10_board_v1_lines": ("84", "50"),
            "k10_board_v2": ("80", "50"), "up_board_v1": ("84", "50"),
            "up_board_v1_lines": ("84", "50"), "up_board_v2": ("80", "50")}
GEOMETRY_CONTROLS = ("k10_neg_rounded_corners", "k10_neg_l_shape", "k10_neg_cutout",
                     "k10_neg_two_boards", "k10_neg_open_outline", "k10_neg_no_outline",
                     "k10_neg_rotated", "up_neg_rounded_corners", "up_neg_l_shape",
                     "up_neg_cutout", "up_neg_two_boards", "up_neg_open_outline",
                     "up_neg_no_outline", "up_neg_rotated")
TEXT_CONTROLS = ("txt_angle_on_gr_line", "txt_unknown_field_on_gr_rect", "txt_other_version",
                 "txt_doubled_lines")
ENVELOPE = ("env_0fp", "env_5fp", "env_20fp", "env_40fp", "env_100fp")
CAP = 128 * 1024


# --- the admission rule: #933's reader plus the allowlist and the observed version ---------
def admit(text, accepted_versions):
    """(width, height) as exact decimals for ONE supported rectangle, or P.Refused."""
    board = P._sexpr(text)
    version = P._field(board, "version")
    if version is None or len(version) < 2 or version[1] not in accepted_versions:
        raise P.Refused("board-file format version %s is not an accepted observed version"
                        % (version[1] if version and len(version) > 1 else None))
    for fp in (n for n in board[1:] if isinstance(n, list) and n and n[0] == "footprint"):
        if any(isinstance(g, list) and g and g[0].startswith("fp_") and P._on_edge(g) for g in fp[1:]):
            raise P.Refused("outline graphics inside a footprint")
    edge = [n for n in board[1:] if isinstance(n, list) and n and n[0].startswith("gr_") and P._on_edge(n)]
    if not edge:
        raise P.Refused("no Edge.Cuts outline")
    for shape in edge:
        allowed = ALLOWED.get(shape[0])
        if allowed is None:
            raise P.Refused("unsupported Edge.Cuts shape: %s" % shape[0])
        for child in shape[1:]:
            name = child[0] if isinstance(child, list) and child else child
            if name not in allowed:
                raise P.Refused("unrecognised field on %s: %s" % (shape[0], name))
    kinds = sorted({n[0] for n in edge})
    if kinds == ["gr_rect"] and len(edge) == 1:
        (x1, y1), (x2, y2) = P._point(edge[0], "start"), P._point(edge[0], "end")
        return P._rect_from_points([(x1, y1), (x2, y1), (x2, y2), (x1, y2)])
    if kinds == ["gr_rect"]:
        raise P.Refused("%d separate rectangles on Edge.Cuts, not one outline" % len(edge))
    if kinds == ["gr_line"]:
        return P._closed_rectangle([(P._point(n, "start"), P._point(n, "end")) for n in edge])
    raise P.Refused("unsupported Edge.Cuts shapes: %s" % ", ".join(kinds))


def file_version(text):
    m = re.search(r"\(kicad_pcb\s+\(version\s+(\d+)\)", text)
    return m.group(1) if m else None


def readings(name, accepted, export_dir, export_ok=True):
    """R1 (admission of the board text), R2 (#933 DXF reader) and R3 (ezdxf). F3: a file
    is read only when its export exited 0 at a path cleared beforehand."""
    src_path = os.path.join(EVIDENCE, "fixtures", name + ".kicad_pcb")
    text = open(src_path, encoding="utf-8").read()
    out = {"source_sha256": P.sha256(text.encode("utf-8")), "format_version": file_version(text)}
    try:
        r1 = admit(text, accepted)
        out["R1_mm"] = [P._plain(v) for v in r1]
    except P.Refused as exc:
        r1, out["R1_refused"] = None, str(exc)
    dxf = os.path.join(export_dir, name + ".dxf")
    if not export_ok:
        r2, out["R2_refused"], out["R3"] = None, "KiCad export failed; no output accepted", {"refused": "export failed"}
    elif os.path.exists(dxf):
        raw = open(dxf, "rb").read()
        out["export_sha256"] = P.sha256(raw)
        try:
            r2 = P.export_rectangle(raw.decode("utf-8"))
            out["R2_mm"] = [P._plain(v) for v in r2]
        except P.Refused as exc:
            r2, out["R2_refused"] = None, str(exc)
        except Exception as exc:                       # an unreadable export is recorded, not hidden
            r2, out["R2_refused"] = None, "unreadable export: %s" % type(exc).__name__
        try:
            r3 = P.ezdxf_reading(dxf)
        except Exception as exc:
            r3 = {"refused": "ezdxf could not read the export: %s" % type(exc).__name__}
        out["R3"] = r3
    else:
        r2, out["R2_refused"], out["R3"] = None, "no export", {"refused": "no export"}
    third = out["R3"].get("mm")
    out["admitted"] = r1 is not None
    out["agree"] = (r1 is not None and r2 is not None and third is not None
                    and all(abs(a - b) <= P.TOLERANCE_MM for a, b in zip(r1, r2))
                    and all(abs(a - P.Decimal(b)) <= P.TOLERANCE_MM for a, b in zip(r1, third)))
    return out


# --- KiCad 10 inside the sandbox ------------------------------------------------------------
GEN = r'''
import os, sys, pcbnew
OUT = "/work/fixtures"
os.makedirs(OUT, exist_ok=True)
print("PCBNEW_VERSION=" + pcbnew.Version())
def mm(x, y):
    return pcbnew.VECTOR2I_MM(x, y)
def shape(b, kind, *pts, width=0.1):
    s = pcbnew.PCB_SHAPE(b)
    s.SetShape(kind)
    s.SetLayer(pcbnew.Edge_Cuts)
    s.SetWidth(pcbnew.FromMM(width))
    if kind == pcbnew.SHAPE_T_ARC:
        s.SetArcGeometry(mm(*pts[0]), mm(*pts[1]), mm(*pts[2]))
    elif kind == pcbnew.SHAPE_T_CIRCLE:
        s.SetCenter(mm(*pts[0])); s.SetEnd(mm(*pts[1]))
    else:
        s.SetStart(mm(*pts[0])); s.SetEnd(mm(*pts[1]))
    b.Add(s)
def rect(b, a, c): shape(b, pcbnew.SHAPE_T_RECT, a, c)
def line(b, a, c): shape(b, pcbnew.SHAPE_T_SEGMENT, a, c)
def loop(b, pts):
    for i in range(len(pts)):
        line(b, pts[i], pts[(i + 1) % len(pts)])
def save(name, build):
    b = pcbnew.BOARD()
    build(b)
    pcbnew.SaveBoard(os.path.join(OUT, name + ".kicad_pcb"), b)
import math
R = [(100, 100), (184, 100), (184, 150), (100, 150)]
save("k10_board_v1", lambda b: rect(b, (100, 100), (184, 150)))
save("k10_board_v1_lines", lambda b: loop(b, R))
save("k10_board_v2", lambda b: rect(b, (100, 100), (180, 150)))
def rounded(b):
    line(b, (103, 100), (181, 100)); shape(b, pcbnew.SHAPE_T_ARC, (181, 100), (183.12132, 100.87868), (184, 103))
    line(b, (184, 103), (184, 147)); shape(b, pcbnew.SHAPE_T_ARC, (184, 147), (183.12132, 149.12132), (181, 150))
    line(b, (181, 150), (103, 150)); shape(b, pcbnew.SHAPE_T_ARC, (103, 150), (100.87868, 149.12132), (100, 147))
    line(b, (100, 147), (100, 103)); shape(b, pcbnew.SHAPE_T_ARC, (100, 103), (100.87868, 100.87868), (103, 100))
save("k10_neg_rounded_corners", rounded)
save("k10_neg_l_shape", lambda b: loop(b, [(100, 100), (184, 100), (184, 125), (140, 125), (140, 150), (100, 150)]))
save("k10_neg_cutout", lambda b: (rect(b, (100, 100), (184, 150)), shape(b, pcbnew.SHAPE_T_CIRCLE, (142, 125), (147, 125))))
save("k10_neg_two_boards", lambda b: (rect(b, (100, 100), (184, 150)), rect(b, (200, 100), (230, 120))))
save("k10_neg_open_outline", lambda b: (line(b, R[0], R[1]), line(b, R[1], R[2]), line(b, R[2], R[3])))
save("k10_neg_no_outline", lambda b: None)
def rot(x, y, t=math.radians(30)):
    return (round(100 + x * math.cos(t) - y * math.sin(t), 6), round(100 + x * math.sin(t) + y * math.cos(t), 6))
save("k10_neg_rotated", lambda b: loop(b, [rot(0, 0), rot(84, 0), rot(84, 50), rot(0, 50)]))
for src in sorted(os.listdir("/msl/k7")):
    b = pcbnew.LoadBoard(os.path.join("/msl/k7", src))
    pcbnew.SaveBoard(os.path.join(OUT, "up_" + src), b)
def envelope(n_fp, pads, tracks):
    def build(b):
        rect(b, (100, 100), (184, 150))
        for i in range(n_fp):
            fp = pcbnew.FOOTPRINT(b); fp.SetReference("U%d" % i); fp.SetValue("SYNTH")
            fp.SetPosition(mm(102 + (i % 20) * 4, 102 + (i // 20) * 4))
            for p in range(pads):
                pad = pcbnew.PAD(fp); pad.SetNumber(str(p + 1)); pad.SetShape(pcbnew.PAD_SHAPE_RECT)
                pad.SetAttribute(pcbnew.PAD_ATTRIB_SMD); pad.SetLayerSet(pad.SMDMask())
                pad.SetSize(mm(0.6, 0.3)); pad.SetPosition(mm(102 + (i % 20) * 4 + 0.5 * p, 102 + (i // 20) * 4))
                fp.Add(pad)
            b.Add(fp)
        for t in range(tracks):
            tr = pcbnew.PCB_TRACK(b); tr.SetStart(mm(101 + (t % 80), 101 + (t // 80) * 0.5))
            tr.SetEnd(mm(101.5 + (t % 80), 101 + (t // 80) * 0.5)); tr.SetWidth(pcbnew.FromMM(0.25))
            tr.SetLayer(pcbnew.F_Cu); b.Add(tr)
    return build
for name, args in (("env_0fp", (0, 0, 0)), ("env_5fp", (5, 4, 20)), ("env_20fp", (20, 8, 100)),
                   ("env_40fp", (40, 16, 300)), ("env_100fp", (100, 16, 1000))):
    save(name, envelope(*args))
print("GEN_DONE")
'''

EXPORT = r'''
set -u
cd /work
mkdir -p exports exports_repeat
kicad-cli version > kicad_cli_version.txt 2>&1
kicad-cli pcb export dxf --help > dxf_help.txt 2>&1
for f in /msl/fixtures/*.kicad_pcb; do
  n=$(basename "$f" .kicad_pcb)
  for d in exports exports_repeat; do
    rm -f "$d/$n.dxf"
    kicad-cli pcb export dxf --mode-single --layers Edge.Cuts --output-units mm -o "$d/$n.dxf" "$f" > "$d/$n.log" 2>&1
    echo "$d $n $?" >> export_status.txt
  done
done
n=k10_board_v1
rm -f exports/${n}_inch.dxf
kicad-cli pcb export dxf --mode-single --layers Edge.Cuts --output-units in -o exports/${n}_inch.dxf /msl/fixtures/$n.kicad_pcb > exports/${n}_inch.log 2>&1
echo "exports ${n}_inch $?" >> export_status.txt
'''


def run(workdir, inputs, command):
    """One sandboxed session with ``inputs`` as the read-only mount."""
    if os.path.isdir(INPUTS):
        shutil.rmtree(INPUTS)
    shutil.copytree(inputs, INPUTS)
    for d, _dirs, files in os.walk(INPUTS):
        os.chmod(d, 0o755)
        for f in files:
            os.chmod(os.path.join(d, f), 0o644)
    if os.path.isdir(workdir):
        shutil.rmtree(workdir)
    os.makedirs(workdir)
    proc = M.run_sandboxed(workdir, command)
    return proc


def _blocks(text, head):
    """The tab-indented top-level blocks KiCad 10 writes, e.g. "\t(gr_line\n ... \n\t)\n"."""
    return re.findall(r"\t\(%s\n.*?\n\t\)\n" % head, text, re.S)


def text_controls(fixtures):
    """Supported KiCad 10 files edited to carry one forbidden or foreign element each.
    Returns, per control, whether the edit actually changed the source text."""
    lines_src = open(os.path.join(fixtures, "k10_board_v1_lines.kicad_pcb"), encoding="utf-8").read()
    rect_src = open(os.path.join(fixtures, "k10_board_v1.kicad_pcb"), encoding="utf-8").read()
    made = {
        "txt_angle_on_gr_line": (lines_src, lines_src.replace("\t(gr_line\n", "\t(gr_line\n\t\t(angle 30)\n", 1)),
        "txt_unknown_field_on_gr_rect": (rect_src, rect_src.replace("\t(gr_rect\n", "\t(gr_rect\n\t\t(rotation 90)\n", 1)),
        "txt_other_version": (rect_src, re.sub(r"\(version \d+\)", "(version 20221018)", rect_src, count=1)),
    }
    blocks = _blocks(lines_src, "gr_line")
    def horizontal(b):
        m = re.search(r"\(start ([-\d.]+) ([-\d.]+)\)\s*\(end ([-\d.]+) ([-\d.]+)\)", b)
        return m is not None and m.group(2) == m.group(4)
    hor = [b for b in blocks if horizontal(b)]
    ver = [b for b in blocks if not horizontal(b)]
    doubled = lines_src
    if len(hor) == 2 and len(ver) == 2:      # both vertical sides replaced by copies of the horizontal ones
        doubled = lines_src.replace(ver[0], hor[0]).replace(ver[1], hor[1])
    made["txt_doubled_lines"] = (lines_src, doubled)
    for name, (_src, text) in made.items():
        open(os.path.join(fixtures, name + ".kicad_pcb"), "w", encoding="utf-8").write(text)
    return {name: src != text for name, (src, text) in made.items()}


def tool_identity():
    """The pinned image as retrieved: index, amd64 manifest, config and verified layers."""
    blobs = os.path.join(STAGE, "blobs")
    index = open(os.path.join(blobs, "index.json"), "rb").read()
    manifest = open(os.path.join(blobs, "manifest.json"), "rb").read()
    man = json.loads(manifest)
    digests = [man["config"]["digest"]] + [l["digest"] for l in man["layers"]]
    verified = all(P.sha256(open(os.path.join(blobs, d.split(":")[1]), "rb").read()) == d.split(":")[1]
                   for d in digests)
    return {"image": "kicad/kicad:10.0.8", "index_digest": "sha256:" + P.sha256(index),
            "linux_amd64_manifest": "sha256:" + P.sha256(manifest),
            "config_digest": man["config"]["digest"], "layers": [l["digest"] for l in man["layers"]],
            "blobs_verified": verified}


def image_inventory():
    root = os.path.join(STAGE, "rootfs")
    status = open(os.path.join(root, "var/lib/dpkg/status"), encoding="utf-8", errors="replace").read()
    pkgs, cur = [], {}
    for line in status.splitlines() + [""]:
        if not line.strip():
            if cur.get("Package") and "installed" in cur.get("Status", ""):
                pkgs.append("%s %s" % (cur["Package"], cur.get("Version", "?")))
            cur = {}
        elif ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            cur[k] = v.strip()
    with open(os.path.join(EVIDENCE, "image_packages.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(sorted(pkgs)) + "\n")
    config = json.load(open(os.path.join(STAGE, "blobs", tool_identity()["config_digest"].split(":")[1])))
    notice = None
    for cand in ("usr/share/doc/kicad/copyright", "usr/share/doc/kicad-cli/copyright"):
        path = os.path.join(root, cand)
        if os.path.exists(path):
            text = open(path, encoding="utf-8", errors="replace").read()
            notice = {"file": "/" + cand, "sha256": P.sha256(text.encode("utf-8")),
                      "licence_fields": sorted(set(m.strip() for m in re.findall(r"^License:(.*)$", text, re.M)))}
            break
    return {"installed_packages": len(pkgs), "package_list": "image_packages.txt",
            "kicad_packages": sorted(p for p in pkgs if p.split()[0].startswith("kicad")),
            "image_label_licence": config["config"].get("Labels", {}).get("org.opencontainers.image.licenses"),
            "image_label_source": config["config"].get("Labels", {}).get("org.opencontainers.image.source"),
            "kicad_copyright_notice": notice,
            "os": dict(re.findall(r'^(\w+)="?([^"\n]*)"?$', open(os.path.join(root, "etc/os-release")).read(), re.M)).get("PRETTY_NAME")}


def main():
    doc = json.load(open(PREREG, encoding="utf-8"))
    tool = tool_identity()
    if (tool["index_digest"] != doc["tool"]["index_digest"]
            or tool["linux_amd64_manifest"] != doc["tool"]["linux_amd64_manifest"] or not tool["blobs_verified"]):
        print(json.dumps({"verdict": "BLOCKED", "cause": "image identity differs", "tool": tool}))
        return 2
    fixtures = os.path.join(EVIDENCE, "fixtures")
    exports = os.path.join(EVIDENCE, "exports")
    for d in (fixtures, exports):
        if os.path.isdir(d):
            shutil.rmtree(d)
        os.makedirs(d)
    # session 1: KiCad 10 writes the fixtures
    stage_in = os.path.join(STAGE, "in1")
    shutil.rmtree(stage_in, ignore_errors=True)
    os.makedirs(os.path.join(stage_in, "k7"))
    for name in sorted(os.listdir(K7_FIXTURES)):
        shutil.copyfile(os.path.join(K7_FIXTURES, name), os.path.join(stage_in, "k7", name))
    open(os.path.join(stage_in, "gen.py"), "w").write(GEN)
    w1 = os.path.join(WORK, "gen")
    p1 = run(w1, stage_in, ["/bin/sh", "-c", "python3 /msl/gen.py > gen.log 2>&1; echo EXIT=$? >> gen.log"])
    gen_log = open(os.path.join(w1, "gen.log"), encoding="utf-8", errors="replace").read()
    for name in sorted(n for n in os.listdir(os.path.join(w1, "fixtures")) if n.endswith(".kicad_pcb")):
        shutil.copyfile(os.path.join(w1, "fixtures", name), os.path.join(fixtures, name))
    edited = text_controls(fixtures)
    # session 2: KiCad 10 exports every fixture twice, plus the inch control
    stage_in2 = os.path.join(STAGE, "in2")
    shutil.rmtree(stage_in2, ignore_errors=True)
    os.makedirs(stage_in2)
    shutil.copytree(fixtures, os.path.join(stage_in2, "fixtures"))
    open(os.path.join(stage_in2, "export.sh"), "w").write(EXPORT)
    w2 = os.path.join(WORK, "export")
    p2 = run(w2, stage_in2, ["/bin/sh", "/msl/export.sh"])
    status = {}
    for line in open(os.path.join(w2, "export_status.txt")).read().split("\n"):
        if line.strip():
            d, n, code = line.split()
            status["%s/%s" % (d, n)] = int(code)
    for name in sorted(os.listdir(os.path.join(w2, "exports"))):
        if name.endswith(".dxf"):
            shutil.copyfile(os.path.join(w2, "exports", name), os.path.join(exports, name))
    observed = sorted({file_version(open(os.path.join(fixtures, n + ".kicad_pcb"), encoding="utf-8").read())
                       for n in SUPPORTED})
    accepted = tuple(v for v in observed if v)
    record = {"proof": doc["proof"], "preregistration_sha256": P.sha256(open(PREREG, "rb").read()),
              "tool": tool, "isolation": "the #934 sandbox runner, unchanged (see the module docstring)",
              "sessions": {"generate": {"returncode": p1.returncode, "log": gen_log[-2000:]},
                           "export": {"returncode": p2.returncode,
                                      "kicad_cli_version": open(os.path.join(w2, "kicad_cli_version.txt")).read().strip(),
                                      "status": status}},
              "observed_format_versions": observed, "accepted_versions": list(accepted),
              "text_controls_edited": edited, "fixtures": {}}
    raw_help = open(os.path.join(w2, "dxf_help.txt"), "rb").read()
    record["kicad_cli_help_raw_sha256"] = P.sha256(raw_help)
    help_lines = [l.rstrip() for l in raw_help.decode("utf-8", "replace").splitlines()
                  if ": Debug: " not in l]          # wxWidgets start-up noise, not CLI help
    with open(os.path.join(EVIDENCE, "kicad_cli_10.0.8_pcb_export_dxf_help.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(help_lines).strip("\n") + "\n")
    for name in SUPPORTED + GEOMETRY_CONTROLS + TEXT_CONTROLS + ENVELOPE:
        fresh = status.get("exports/" + name) == 0
        entry = readings(name, accepted, exports, export_ok=fresh)
        entry["export_exit_ok"] = fresh
        rep = os.path.join(w2, "exports_repeat", name + ".dxf")
        if os.path.exists(rep) and "export_sha256" in entry:
            raw_rep = open(rep, "rb").read()
            entry["repeat_bytes_identical"] = P.sha256(raw_rep) == entry["export_sha256"]
            try:
                again = P.export_rectangle(raw_rep.decode("utf-8"))
                entry["repeat_R2_mm"] = [P._plain(v) for v in again]
            except Exception as exc:
                entry["repeat_R2_refused"] = str(exc)
        record["fixtures"][name] = entry
    inch = os.path.join(exports, "k10_board_v1_inch.dxf")
    try:
        P.export_rectangle(open(inch, encoding="utf-8").read())
        record["units_control"] = {"refused": False}
    except P.Refused as exc:
        record["units_control"] = {"refused": True, "reason": str(exc),
                                   "export_exit_ok": status.get("exports/k10_board_v1_inch") == 0}
    env = {}
    for name in ENVELOPE:
        text = open(os.path.join(fixtures, name + ".kicad_pcb"), encoding="utf-8").read()
        t0 = time.time()
        tokens = len(re.findall(r'\(|\)|"(?:[^"\\]|\\.)*"|[^\s()"]+', text))
        depth = d = 0
        for ch in text:
            if ch == "(":
                d += 1
                depth = max(depth, d)
            elif ch == ")":
                d -= 1
        env[name] = {"bytes": len(text.encode("utf-8")), "fits_128KiB": len(text.encode("utf-8")) < CAP,
                     "tokens": tokens, "max_depth": depth,
                     "admission": record["fixtures"][name].get("R1_mm") or record["fixtures"][name].get("R1_refused"),
                     "seconds": round(time.time() - t0, 4)}
    record["envelope"] = env
    record["image_inventory"] = image_inventory()
    with open(os.path.join(EVIDENCE, "proof_record.json"), "w", encoding="utf-8") as fh:
        json.dump(record, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print(json.dumps({"observed": observed, "generate_rc": p1.returncode, "export_rc": p2.returncode}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
