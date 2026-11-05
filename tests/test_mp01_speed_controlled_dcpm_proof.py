"""MP01-SPEED-CONTROLLED-DCPM-PROOF-01 — the committed evidence, re-checked without OpenModelica.

The proof itself runs the pinned OpenModelica image in an unprivileged sandbox
(``scripts/mp01_speed_controlled_dcpm_proof.py``). These tests need no simulator and no
network: they re-derive every recorded analysis from the committed result files and check
the frozen pre-registration, the identities, the refusal and the isolation record.
"""
import gzip
import hashlib
import io
import json
import os
from decimal import Decimal

import pytest

from scripts import mp01_speed_controlled_dcpm_proof as proof

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVIDENCE = proof.EVIDENCE
RECORD = json.load(open(os.path.join(EVIDENCE, "proof_record.json"), encoding="utf-8"))
PREREG, PREREG_SHA = proof.prereg()
FROZEN_PREREG_SHA = "58b167ec8f11828fa06fd7e6db99231fa79c87ac26e7b1666dc05b67b49ac85c"
RUNS = ("B1_primary_1", "B1_primary_2", "B1_sensitivity_1", "B2_primary_1", "B2_sensitivity_1")


def _sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def _csv_cols(run_id):
    raw = gzip.decompress(open(os.path.join(EVIDENCE, "results", run_id + ".csv.gz"), "rb").read())
    path = os.path.join(EVIDENCE, "results", run_id + ".csv")
    return raw, path


def _analysis(run_id, tmp_path):
    raw, _ = _csv_cols(run_id)
    p = tmp_path / (run_id + ".csv")
    p.write_bytes(raw)
    return raw, proof.analyse(proof.read_csv(str(p)), RECORD["runs"][run_id]["analysis"]["model_derived_parameters"], PREREG)


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


def test_the_preregistration_is_the_frozen_one_and_bound_into_the_record():
    assert PREREG_SHA == FROZEN_PREREG_SHA == RECORD["preregistration_sha256"]
    assert PREREG["status"] == "FROZEN BEFORE ANY SIMULATION"
    assert PREREG["criteria"]["X1_torque_balance_EXPLORATORY"]["status"].startswith("exploratory only")
    assert "1.27.2" in PREREG["tool"]["deviation"] and "not claimed" in PREREG["tool"]["deviation"]


def test_tool_and_library_identities_match_the_preregistration():
    tool = RECORD["tool"]
    assert tool["index_digest"] == PREREG["tool"]["index_digest"]
    assert tool["linux_amd64_manifest"] == PREREG["tool"]["linux_amd64_manifest"]
    assert tool["blobs_verified"] is True and len(tool["layers"]) == 2
    assert tool["omc_version"] == "OpenModelica 1.27.1"
    assert tool["msl_commit"] == PREREG["library"]["commit"] == "8ae3d35c24e519cb2996cab20f3b13daf2b0c50a"
    inv = RECORD["image_inventory"]
    assert inv["omc_packages"] == ["libomc 1.27.1-1", "libomcsimulation 1.27.1-1",
                                   "omc 1.27.1-1", "omc-common 1.27.1-1"]
    notice = inv["openmodelica_copyright_notices"]["omc"]["licence_statement"]
    assert "GPL VERSION 3" in notice and "OSMC-PL) VERSION 1.2" in notice
    packages = open(os.path.join(EVIDENCE, "image_packages.txt"), encoding="utf-8").read().splitlines()
    assert len(packages) == inv["installed_packages"] and "omc 1.27.1-1" in packages


def test_every_run_was_isolated_and_offline():
    iso = RECORD["isolation"]
    assert iso["host_uid"] == 65534 and "no_new_privs" in iso["capabilities"]
    assert "net" in iso["namespaces"] and "--cpu=1500" in iso["limits"]
    for run_id in ("A_smoke",) + RUNS:
        run = RECORD["runs"][run_id]
        assert run["returncode"] == 0 and run["omc_exit_ok"] and run["solver_ok"], run_id
        fields = run["netdev"].split()
        assert fields[0] == "lo:" and set(fields[1:]) == {"0"}, run_id     # only an idle loopback


@pytest.mark.parametrize("run_id", ("A_smoke",) + RUNS)
def test_each_recorded_analysis_is_rederived_from_its_committed_result(run_id, tmp_path):
    raw, again = _analysis(run_id, tmp_path)
    assert hashlib.sha256(raw).hexdigest() == RECORD["runs"][run_id]["csv_sha256"]
    assert again == RECORD["runs"][run_id]["analysis"]


def test_the_observed_outcomes_under_the_frozen_criteria():
    R = RECORD["runs"]
    for run_id in ("A_smoke", "B1_primary_1", "B1_sensitivity_1"):
        a = R[run_id]["analysis"]
        assert a["K1"]["outcome"] == "MET" and a["K2"]["outcome"] == "NOT MET"
        assert Decimal(a["K2"]["max_abs_ia_A"]) > Decimal(a["IaMax_A"]) == Decimal(150)
    for run_id in ("B2_primary_1", "B2_sensitivity_1"):
        a = R[run_id]["analysis"]
        assert a["K1"]["outcome"] == "NOT MET" and a["K1"]["t_rec_s"] is None
    p = R["B1_primary_1"]["analysis"]["model_derived_parameters"]
    assert Decimal(p["driveData.IaMax"]) == 150
    assert abs(Decimal(p["driveData.tauNominal"]) - Decimal("63.661977236758")) < Decimal("1e-9")
    for run_id in ("A_smoke",) + RUNS:          # exploratory balance: reported, not gated
        assert abs(Decimal(R[run_id]["analysis"]["X1_exploratory"]["residual_Nm"])) < Decimal("1e-9")


def test_sensitivity_is_recomputed_and_stable():
    R = RECORD["runs"]
    wn = Decimal(R["B1_primary_1"]["analysis"]["wNominal_rad_s"])
    ia_max = Decimal(R["B1_primary_1"]["analysis"]["IaMax_A"])
    for case in ("B1", "B2"):
        again = proof.sensitivity(R[case + "_primary_1"]["analysis"], R[case + "_sensitivity_1"]["analysis"], wn, ia_max)
        assert again == RECORD["N1_sensitivity"][case]
        assert again["verdict"] == "NUMERICALLY STABLE"


def test_result_identities_are_recomputed_and_behave():
    R = RECORD["runs"]
    for run_id in RUNS:
        case = run_id.split("_")[0]
        source = open(os.path.join(EVIDENCE, "models", "MP01_%s.mo" % case), encoding="utf-8").read()
        assert hashlib.sha256(source.encode("utf-8")).hexdigest() == R[run_id]["model_sha256"]
        assert proof.wrapper_source("MP01_" + case, R[run_id]["inputs"]) == source
        assert proof.result_identity(RECORD["tool"], source, R[run_id]["inputs"], R[run_id]["settings"]) == \
            R[run_id]["result_identity"]
    d = RECORD["D_identity"]
    assert d == {"B1_repeat_same_identity": True, "B1_repeat_same_numbers": True, "B2_differs_from_B1": True}
    # only the load-torque magnitude differs between B1 and B2
    b1, b2 = R["B1_primary_1"]["inputs"], R["B2_primary_1"]["inputs"]
    assert {k for k in b1 if b1[k] != b2[k]} == {"load_torque_factor"}


@pytest.mark.parametrize("drop", proof.REQUIRED)
def test_a_missing_required_input_refuses_before_any_model_exists(drop):
    values = proof.base_inputs("1.0")
    del values[drop]
    with pytest.raises(proof.Refused, match="missing required input"):
        proof.wrapper_source("X", values)


@pytest.mark.parametrize("bad", ["abc", "0", "-1", "NaN", "Infinity"])
def test_malformed_or_nonpositive_inputs_refuse(bad):
    values = proof.base_inputs("1.0")
    values["JL_kgm2"] = bad
    with pytest.raises(proof.Refused):
        proof.wrapper_source("X", values)


def test_the_recorded_refusal_and_the_wrapper_declares_every_input():
    c = RECORD["runs"]["C_refusal"]
    assert c == {"refused": True, "reason": "missing required input(s): JL_kgm2",
                 "model_written": False, "omc_invoked": False}
    src = proof.wrapper_source("X", proof.base_inputs("1.0"))
    for key, value in proof.base_inputs("1.0").items():
        assert str(value) in src, key
    assert "extends Modelica.Electrical.Machines.Examples.ControlledDCDrives.SpeedControlledDCPM(" in src


def test_the_harness_stays_outside_the_product():
    for top in ("engine", "web"):
        for d, _dirs, files in os.walk(os.path.join(ROOT, top)):
            for f in files:
                if f.endswith(".py"):
                    text = open(os.path.join(d, f), encoding="utf-8").read()
                    assert "mp01_speed_controlled_dcpm_proof" not in text, f
    requirements = open(os.path.join(ROOT, "requirements.txt"), encoding="utf-8").read().lower()
    assert "modelica" not in requirements
