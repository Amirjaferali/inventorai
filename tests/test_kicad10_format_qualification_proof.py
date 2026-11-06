"""KICAD10-FORMAT-QUALIFICATION-PROOF-01 — the committed evidence, re-checked without KiCad.

The proof ran KiCad 10.0.8 in the unprivileged sandbox. These tests need no KiCad and no
network: they re-decide every committed fixture from its committed board file and export,
check the frozen pre-registration, the gates, the admission rule's allowlist and version
scope, and that the harness stays outside the product.
"""
import hashlib
import json
import os
from decimal import Decimal

import pytest

from scripts import kicad10_format_qualification_proof as K
from scripts import pcb_outline_planar_clearance_proof as P

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVIDENCE = K.EVIDENCE
RECORD = json.load(open(os.path.join(EVIDENCE, "proof_record.json"), encoding="utf-8"))
PREREG = json.load(open(K.PREREG, encoding="utf-8"))
FROZEN_PREREG_SHA = "31206692fb43144dff022e973f7387bcf1356342280008f9a38e7c962126cf43"
ACCEPTED = ("20260206",)
BASE_KEYS = ("source_sha256", "format_version", "R1_mm", "R1_refused", "export_sha256",
             "R2_mm", "R2_refused", "R3", "admitted", "agree")


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


def test_frozen_preregistration_and_pinned_tool():
    assert _sha(K.PREREG) == FROZEN_PREREG_SHA == RECORD["preregistration_sha256"]
    tool = RECORD["tool"]
    assert tool["index_digest"] == PREREG["tool"]["index_digest"]
    assert tool["linux_amd64_manifest"] == PREREG["tool"]["linux_amd64_manifest"]
    assert tool["blobs_verified"] is True and len(tool["layers"]) == 13
    assert RECORD["sessions"]["export"]["kicad_cli_version"].endswith("10.0.8")
    assert "PCBNEW_VERSION=10.0.8" in RECORD["sessions"]["generate"]["log"]
    inv = RECORD["image_inventory"]
    assert inv["os"] == "Debian GNU/Linux 13 (trixie)" and inv["image_label_licence"] == "GPL-3.0-or-later"
    assert inv["kicad_copyright_notice"] is None          # recorded finding: no KiCad licence file in the image


def test_the_observed_version_is_the_only_accepted_one():
    assert RECORD["observed_format_versions"] == list(ACCEPTED) == RECORD["accepted_versions"]
    help_text = open(os.path.join(EVIDENCE, "kicad_cli_10.0.8_pcb_export_dxf_help.txt"), encoding="utf-8").read()
    assert "--mode-single" in help_text and "Output directory" in help_text


@pytest.mark.parametrize("name", sorted(RECORD["fixtures"]))
def test_each_fixture_is_decided_again_from_the_committed_files(name):
    recorded = RECORD["fixtures"][name]
    again = K.readings(name, ACCEPTED, os.path.join(EVIDENCE, "exports"), export_ok=recorded["export_exit_ok"])
    assert {k: again.get(k) for k in BASE_KEYS} == {k: recorded.get(k) for k in BASE_KEYS}


def test_G1_supported_boards_agree_exactly_in_all_three_readings():
    for name, dims in K.EXPECTED.items():
        e = RECORD["fixtures"][name]
        assert e["admitted"] and e["agree"] and e["format_version"] == ACCEPTED[0], name
        assert e["R1_mm"] == list(dims) == e["R2_mm"]
        assert [Decimal(v) for v in e["R3"]["mm"]] == [Decimal(v) for v in dims]
    for name in K.ENVELOPE:
        assert RECORD["fixtures"][name]["agree"] and RECORD["fixtures"][name]["R1_mm"] == ["84", "50"]


def test_G2_no_control_is_ever_admitted():
    for name in K.GEOMETRY_CONTROLS + K.TEXT_CONTROLS:
        assert RECORD["fixtures"][name]["admitted"] is False, name
        assert "R1_refused" in RECORD["fixtures"][name], name
    assert all(RECORD["text_controls_edited"].values())
    f = RECORD["fixtures"]
    assert "angle" in f["txt_angle_on_gr_line"]["R1_refused"]
    assert "rotation" in f["txt_unknown_field_on_gr_rect"]["R1_refused"]
    assert "20221018" in f["txt_other_version"]["R1_refused"]
    assert "not two horizontal and two vertical sides" in f["txt_doubled_lines"]["R1_refused"]
    assert RECORD["units_control"]["refused"] and "not metric" in RECORD["units_control"]["reason"]


def test_G3_and_G4_freshness_and_determinism():
    for name, e in RECORD["fixtures"].items():
        if e["export_exit_ok"]:
            assert "export_sha256" in e and e["repeat_bytes_identical"] is True, name
        else:
            assert e["R2_refused"] == "KiCad export failed; no output accepted", name
        if e["agree"]:
            assert e["repeat_R2_mm"] == e["R2_mm"], name


def test_envelope_against_the_unchanged_128KiB_cap():
    env = RECORD["envelope"]
    assert [env[n]["fits_128KiB"] for n in K.ENVELOPE] == [True, True, True, False, False]
    for n in K.ENVELOPE:
        assert env[n]["bytes"] == os.path.getsize(os.path.join(EVIDENCE, "fixtures", n + ".kicad_pcb"))


_K10 = ('(kicad_pcb\n\t(version 20260206)\n\t(generator "pcbnew")\n'
        '\t(layers\n\t\t(25 "Edge.Cuts" user)\n\t)\n%s)\n')
_RECT = ('\t(gr_rect\n\t\t(start 100 100)\n\t\t(end 184 150)\n\t\t(stroke\n\t\t\t(width 0.1)\n'
         '\t\t\t(type default)\n\t\t)\n\t\t(fill no)\n\t\t(layer "Edge.Cuts")\n\t\t%s(uuid "u")\n\t)\n')


@pytest.mark.parametrize("extra, reason", [
    ("(angle 30)\n\t\t", "unrecognised field on gr_rect: angle"),
    ("(rotation 90)\n\t\t", "unrecognised field on gr_rect: rotation"),
    ("(net 0)\n\t\t", "unrecognised field on gr_rect: net"),
    ("hide\n\t\t", "unrecognised field on gr_rect: hide"),
])
def test_the_allowlist_refuses_any_unlisted_field(extra, reason):
    with pytest.raises(P.Refused, match=reason):
        K.admit(_K10 % (_RECT % extra), ACCEPTED)


def test_the_allowlisted_shape_is_admitted_and_other_versions_refused():
    text = _K10 % (_RECT % "(locked yes)\n\t\t")
    assert K.admit(text, ACCEPTED) == (Decimal(84), Decimal(50))
    for version in ("20221018", "20240108", "20991231"):
        with pytest.raises(P.Refused, match="not an accepted observed version"):
            K.admit(text.replace("20260206", version), ACCEPTED)


def test_the_harness_stays_outside_the_product():
    for top in ("engine", "web"):
        for d, _dirs, files in os.walk(os.path.join(ROOT, top)):
            for f in files:
                if f.endswith(".py"):
                    assert "kicad10_format_qualification_proof" not in open(os.path.join(d, f), encoding="utf-8").read(), f
    assert "kicad" not in open(os.path.join(ROOT, "requirements.txt"), encoding="utf-8").read().lower()
