"""PCB-OUTLINE-TO-PLANAR-CLEARANCE-PROOF-01 — the committed evidence, re-checked without KiCad.

The proof itself (``scripts/pcb_outline_planar_clearance_proof.py``) runs ``kicad-cli`` where it
is installed. These tests need no KiCad and no network: they re-read the committed exports
and CAD bundles, re-decide every fixture, re-run the product part through the existing routes
and check that the harness stays outside the product.
"""
import hashlib
import io
import json
import os
import re
import zipfile
from decimal import Decimal

import pytest

from scripts import pcb_outline_planar_clearance_proof as proof

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVIDENCE = proof.EVIDENCE
RECORD = json.load(open(proof.RECORD, encoding="utf-8"))


def _sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def test_checksums_bind_every_evidence_file():
    listed = {}
    for line in open(os.path.join(EVIDENCE, "SHA256SUMS"), encoding="utf-8"):
        digest, name = line.split(None, 1)
        listed[name.strip()] = digest
    present = sorted(os.path.relpath(os.path.join(d, f), EVIDENCE)
                     for d, _dirs, files in os.walk(EVIDENCE) for f in files if f != "SHA256SUMS")
    assert sorted(listed) == present
    for name, digest in listed.items():
        assert _sha(os.path.join(EVIDENCE, name)) == digest, name


def test_the_record_names_the_tool_its_licence_notice_and_environment():
    env = RECORD["environment"]
    assert env["kicad_package"] == "kicad 7.0.11+dfsg-1build4 amd64"
    assert env["os"].startswith("Ubuntu 24.04") and "no PPA" in env["kicad_source"]
    assert env["ezdxf"] == "1.4.2"
    notice = RECORD["kicad_licence_notice"]
    assert notice["file"] == "/usr/share/doc/kicad/copyright"
    assert notice["main_files_licence"] == "GPL-3+"
    assert re.fullmatch(r"[0-9a-f]{64}", notice["sha256"])
    assert {"GPL-3+", "GPL-2+"} <= set(notice["licence_fields"])
    help_text = open(os.path.join(EVIDENCE, "kicad_cli_7.0.11_pcb_export_dxf_help.txt"),
                     encoding="utf-8").read()
    # The installed 7.0.11 CLI is the command reference: both flags exist and inches is the default.
    assert "--layers" in help_text and "--output-units" in help_text
    assert 'valid options: mm, in [default: "in"]' in help_text


def test_the_record_names_the_tool_and_stays_synthetic():
    assert RECORD["synthetic_only"] is True
    assert RECORD["tool"] == "kicad-cli 7.0.11"
    assert RECORD["kicad_package"].startswith("Ubuntu 24.04 kicad 7.0.11+dfsg-1build4")
    assert re.fullmatch(r"[0-9a-f]{64}", RECORD["kicad_cli_sha256"])
    assert RECORD["board_file_version"] == proof.SUPPORTED_FILE_VERSION
    assert RECORD["method"] == "mechanical:planar_centered_rectangular_clearance 1.0"
    for name, run in RECORD["kicad_runs"].items():
        assert run["returncode"] == 0 and run["exported"], name
        assert "--layers Edge.Cuts" in run["command"]
    for name in proof.POSITIVE + proof.NEGATIVE:
        source = open(os.path.join(proof.FIXTURES, name + ".kicad_pcb"), encoding="utf-8").read()
        assert "SYNTHETIC TEST BOARD" in source


@pytest.mark.parametrize("name", proof.POSITIVE + proof.NEGATIVE + (proof.UNITS_CONTROL,))
def test_every_fixture_is_decided_again_from_the_committed_files(name):
    if name == proof.UNITS_CONTROL:
        judged = proof.judge("board_v1", export_name=proof.UNITS_CONTROL)
    else:
        judged = proof.judge(name)
    assert judged == RECORD["geometry"][name]


def test_supported_boards_have_exact_agreeing_dimensions():
    expected = {"board_v1": ["84", "50"], "board_v1_lines": ["84", "50"], "board_v2": ["80", "50"]}
    for name, dims in expected.items():
        g = RECORD["geometry"][name]
        assert g["supported"] and g["declared_mm"] == dims and g["source_mm"] == dims
        assert [Decimal(v) for v in g["export_mm"]] == [Decimal(v) for v in dims]
    # KiCad writes a rectangle and the same four lines identically.
    assert (RECORD["geometry"]["board_v1"]["export_sha256"]
            == RECORD["geometry"]["board_v1_lines"]["export_sha256"])


def test_every_unsupported_case_refuses_without_dimensions():
    for name in proof.NEGATIVE + (proof.UNITS_CONTROL,):
        g = RECORD["geometry"][name]
        assert g["supported"] is False and "declared_mm" not in g, name
        assert "export_refused" in g or "source_refused" in g, name
    assert "not metric" in RECORD["geometry"][proof.UNITS_CONTROL]["export_refused"]


def test_supported_boards_agree_with_the_third_ezdxf_reading():
    for name in proof.POSITIVE:
        e = RECORD["geometry"][name]["ezdxf"]
        assert e["dxfversion"] == "AC1009" and e["measurement"] == 1
        assert [Decimal(v) for v in e["mm"]] == [Decimal(v) for v in RECORD["geometry"][name]["declared_mm"]]
    for name in proof.NEGATIVE + (proof.UNITS_CONTROL,):
        assert "refused" in RECORD["geometry"][name]["ezdxf"], name


_HEAD = ('(kicad_pcb (version 20221018) (generator pcbnew) (layers (44 "Edge.Cuts" user)) %s)')


@pytest.mark.parametrize("text, reason", [
    ('(kicad_pcb (version 20240108) (gr_rect (start 0 0) (end 84 50) (layer "Edge.Cuts")))',
     "format version"),
    ("(kicad_pcb (version 20221018) (gr_rect (start 0 0) (end 84 50)", "malformed"),
    ('(not_a_board (version 20221018))', "not a KiCad board file"),
    (_HEAD % '(gr_poly (pts (xy 0 0) (xy 84 0) (xy 84 50) (xy 0 50)) (layer "Edge.Cuts"))',
     "unsupported Edge.Cuts shapes: gr_poly"),
    (_HEAD % '(gr_rect (start 0 0) (end 84 50) (layer "Edge.Cuts")) '
             '(gr_text "X" (at 1 1) (layer "Edge.Cuts"))', "unsupported Edge.Cuts shapes"),
    (_HEAD % '(gr_rect (start 0 0) (end 84 50) (layer "Edge.Cuts")) '
             '(footprint "F" (fp_line (start 1 1) (end 2 2) (layer "Edge.Cuts")))', "inside a footprint"),
    (_HEAD % '(gr_rect (start 0 0) (end 0 50) (layer "Edge.Cuts"))', "rectangle"),
])
def test_the_board_file_reader_refuses_unfamiliar_structures(text, reason):
    with pytest.raises(proof.Refused, match=reason):
        proof.source_rectangle(text)


@pytest.mark.parametrize("dxf, reason", [
    ("  9\n$MEASUREMENT\n 70\n0\n  0\nENDSEC\n", "not metric"),
    ("  9\n$MEASUREMENT\n 70\n1\n  0\nENDSEC\n  0\nSECTION\n  2\nENTITIES\n  0\nLWPOLYLINE\n"
     "  8\nX\n  0\nENDSEC\n  0\nEOF\n", "unsupported export entities"),
    ("  9\n$MEASUREMENT\n 70\n1\n  9\n$INSUNITS\n 70\n1\n  0\nENDSEC\n", "not millimetres"),
])
def test_the_export_reader_refuses_other_units_and_entities(dxf, reason):
    with pytest.raises(proof.Refused, match=reason):
        proof.export_rectangle(dxf)


@pytest.mark.parametrize("bundle, board", [("cad_v1.zip", ["84", "50"]), ("cad_v2.zip", ["80", "50"])])
def test_the_committed_cad_bundles_are_bound_and_measure_the_declared_values(bundle, board):
    z = zipfile.ZipFile(io.BytesIO(open(os.path.join(EVIDENCE, bundle), "rb").read()))
    assert z.namelist() == ["geometry.dxf", "companion.json", "README.txt"]
    dxf = z.read("geometry.dxf")
    comp = json.loads(z.read("companion.json"))
    assert comp["dxf"]["sha256"] == hashlib.sha256(dxf).hexdigest()
    outlines = proof.lwpolylines(dxf.decode("utf-8"))
    assert [Decimal(v) for v in proof.extent(outlines["IAI_DECLARED_BOARD_OUTLINE"])] == \
        [Decimal(v) for v in board]
    assert [Decimal(v) for v in proof.extent(outlines["IAI_DECLARED_USABLE_REGION"])] == \
        [Decimal("86"), Decimal("56")]
    assert [comp["declared_values"]["board_x"], comp["declared_values"]["board_y"]] == board


def test_the_product_route_reproduces_the_engineering_result_and_the_stale_refusal():
    g = RECORD["geometry"]
    record, raw0, raw1 = proof.product_route(g["board_v1"], g["board_v2"], RECORD["tool"])
    for key in ("cad_v1", "cad_v2"):
        for field in ("files", "declared_values", "outcome", "margins_mm", "revision",
                      "companion_binds_dxf", "measured_mm", "source_digest_in_bundle"):
            assert record[key][field] == RECORD["product_route"][key][field], (key, field)
    assert record["cad_v1"]["outcome"] == "NOT_MET" and record["cad_v1"]["margins_mm"] == ["-1", "1"]
    assert record["cad_v2"]["outcome"] == "MET" and record["cad_v2"]["margins_mm"] == ["1", "1"]
    assert record["declare_v1"]["page"]["revision"] == ["0"]
    assert record["redeclare_v2"]["page"]["revision"] == ["1"]
    assert record["redeclare_v2"]["page"]["digest"] != record["declare_v1"]["page"]["digest"]
    change = record["source_change"]
    # Before re-declaring, the product still shows the earlier declaration as current;
    # only the harness's own digest check sees the changed source.
    assert change["product_page_before_redeclaration"]["revision"] == ["0"]
    assert change["stored_note_names_v1_digest"] and not change["stored_note_names_v2_digest"]
    assert change["harness_verdict"].startswith("SOURCE MISMATCH")
    stale = record["old_cad_link_after_change"]
    assert stale["status"] == 409 and "zip" not in (stale["content_type"] or "")
    assert record["cad_v1"]["source_digest_in_bundle"] is False   # the documented gap


def test_the_harness_stays_outside_the_product():
    for top in ("engine", "web"):
        for d, _dirs, files in os.walk(os.path.join(ROOT, top)):
            for f in files:
                if f.endswith(".py"):
                    text = open(os.path.join(d, f), encoding="utf-8").read()
                    assert "pcb_outline_planar_clearance_proof" not in text, f
    requirements = open(os.path.join(ROOT, "requirements.txt"), encoding="utf-8").read().lower()
    assert "kicad" not in requirements
