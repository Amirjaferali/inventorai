"""MP01-SPEED-CONTROLLED-DCPM-PROOF-01 — isolated simulation proof (synthetic only).

Runs the MSL v4.1.0 example `SpeedControlledDCPM` (unchanged) and one bounded wrapper of it
with the pinned OpenModelica v1.27.1-minimal image, under the criteria frozen in
`docs/benchmarks/evidence/mp01_speed_controlled_dcpm_v1/preregistration.json` (committed
before any simulation). Proof-only: nothing in `engine/` or `web/` imports it, it adds no
dependency, and no result enters the product.

Isolation (no privileged daemon, no bare chroot): every `omc` run is launched by host uid
65534 holding no host capabilities and with `no_new_privs`, and creates fresh user, mount,
pid, net, ipc and uts namespaces (`unshare`), under CPU, address-space, file-size, open-file
and process limits (`prlimit`) and a wall-clock timeout. Inside its own user namespace the
process is that namespace's root (uid 0, mapped to host uid 65534), with capabilities that
apply only within that namespace. `scripts/mp01_sandbox/inner.sh` builds a root from the
image's unpacked, digest-verified layers, remounted read-only, mounts the MSL checkout
read-only and one work directory read-write, pivots into it and detaches the host root. The
namespace root could undo the read-only remount, but the image files belong to host root,
which is not mapped into the namespace, so host permissions still refuse writes. The network
namespace has only an idle loopback, and the environment is cleared.

What it is not: engineering validation of any motor, load or controller. A successful
compiler or solver exit proves nothing about a real drive; every value is synthetic.

Usage (needs the prepared /srv/mp01 tree: rootfs/, msl/ at the pinned commit, blobs/):
    python3 scripts/mp01_speed_controlled_dcpm_proof.py
"""
import csv
import hashlib
import json
import os
import shutil
import subprocess
import sys
from decimal import Decimal

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVIDENCE = os.path.join(_ROOT, "docs", "benchmarks", "evidence", "mp01_speed_controlled_dcpm_v1")
PREREG = os.path.join(EVIDENCE, "preregistration.json")
INNER = os.path.join(_ROOT, "scripts", "mp01_sandbox", "inner.sh")
STAGE = os.environ.get("MP01_STAGE", "/srv/mp01")
UID = 65534
LIMITS = ["--cpu=1500", "--as=12000000000", "--fsize=2000000000", "--nofile=4096",
          "--nproc=2048"]
WALL_S = 1800
EXAMPLE = "Modelica.Electrical.Machines.Examples.ControlledDCDrives.SpeedControlledDCPM"
SIGNALS = ["speedSensor.w", "dcpm.ia", "dcpm.va", "dcpm.tauElectrical", "dcpm.tauShaft",
           "loadTorque.tau", "speedController.y", "preFilter.y", "loadInertia.a"]
PARAMETERS = ["driveData.tauNominal", "driveData.IaMax", "driveData.tauMax", "driveData.kPhi",
              "driveData.kpw", "driveData.Tiw", "driveData.JL", "driveData.motorData.Jr",
              "driveData.motorData.wNominal", "driveData.VBat"]
REQUIRED = ("VaNominal_V", "IaNominal_A", "wNominal_rpm", "Ra_ohm", "La_H", "Jr_kgm2", "Js_kgm2",
            "JL_kgm2", "load_torque_factor", "load_step_time_s", "speed_reference_step_time_s")
LOAD_STEP_S, STOP_S = Decimal("0.8"), Decimal("1.0")


class Refused(Exception):
    """A required input is missing or malformed: nothing is written or translated."""


def store_gz(src, dest):
    """Keep a result as deterministic gzip (mtime 0); its hash is taken over the raw CSV."""
    import gzip
    with open(src, "rb") as fin, open(dest, "wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0, compresslevel=9) as gz:
            gz.write(fin.read())


def sha256(data):
    return hashlib.sha256(data if isinstance(data, bytes) else data.encode("utf-8")).hexdigest()


def prereg():
    raw = open(PREREG, "rb").read()
    return json.loads(raw), sha256(raw)


# --- inputs, wrapper and identity -------------------------------------------------------
def base_inputs(load_factor):
    req = prereg()[0]["inputs"]["required"]
    values = {k: v["value"] for k, v in req.items() if k != "load_torque_step_Nm"}
    values["load_torque_factor"] = load_factor
    return values


def validate_inputs(values):
    """Every required input must be present and a plain decimal; no record default is
    ever substituted for a missing one."""
    missing = [k for k in REQUIRED if k not in values]
    if missing:
        raise Refused("missing required input(s): " + ", ".join(missing))
    for k in REQUIRED:
        try:
            v = Decimal(str(values[k]))
        except Exception:
            raise Refused("malformed input %s" % k)
        if not v.is_finite() or v <= 0:
            raise Refused("input %s must be a positive finite decimal" % k)
    return values


def wrapper_source(name, values):
    v = validate_inputs(values)
    return """model %(name)s
  "MP01 proof wrapper: the unchanged MSL example with every required input declared explicitly"
  extends %(example)s(
    driveData(
      motorData(
        VaNominal=%(VaNominal_V)s, IaNominal=%(IaNominal_A)s,
        wNominal=Modelica.Units.Conversions.from_rpm(%(wNominal_rpm)s),
        Ra=%(Ra_ohm)s, TaRef=293.15, alpha20a=0, TaNominal=293.15, La=%(La_H)s,
        Jr=%(Jr_kgm2)s, Js=%(Js_kgm2)s,
        frictionParameters(PRef=0), coreParameters(PRef=0),
        strayLoadParameters(PRef=0), brushParameters(V=0)),
      JL=%(JL_kgm2)s, fS=2000),
    armatureInverter(useIdealInverter=true),
    loadTorque(stepTorque=-%(load_torque_factor)s*driveData.tauNominal,
               startTime=%(load_step_time_s)s),
    step(startTime=%(speed_reference_step_time_s)s));
end %(name)s;
""" % dict(v, name=name, example=EXAMPLE)


def result_identity(tool, model_source, values, settings):
    _p, prereg_sha = prereg()
    material = json.dumps({"image_manifest": tool["linux_amd64_manifest"],
                           "omc_version": tool["omc_version"], "msl_commit": tool["msl_commit"],
                           "model_sha256": sha256(model_source), "inputs": values,
                           "settings": settings, "preregistration_sha256": prereg_sha},
                          sort_keys=True)
    return sha256(material)


# --- isolated execution -------------------------------------------------------------------
def run_sandboxed(workdir, command):
    os.makedirs(workdir, exist_ok=True)
    os.chown(workdir, UID, UID)
    for name in os.listdir(workdir):
        os.chown(os.path.join(workdir, name), UID, UID)
    cmd = (["setpriv", "--reuid=%d" % UID, "--regid=%d" % UID, "--clear-groups",
            "--inh-caps=-all", "--bounding-set=-all", "--no-new-privs", "prlimit"] + LIMITS
           + ["--", "timeout", str(WALL_S), "unshare", "--user", "--map-root-user", "--mount",
              "--pid", "--fork", "--kill-child", "--net", "--ipc", "--uts", "/bin/sh", INNER,
              os.path.join(STAGE, "rootfs"), os.path.join(STAGE, "msl"), workdir] + command)
    proc = subprocess.run(cmd, capture_output=True, text=True, env={"PATH": "/usr/bin:/bin"})
    return proc


LOAD = """loadFile("/msl/Complex.mo");
loadFile("/msl/ModelicaServices/package.mo");
loadFile("/msl/Modelica/package.mo");
"""


def simulate(workdir, model_name, extra_file=None, settings=None):
    """One omc session in the sandbox: simulate to the full MAT result, read the record's
    model-derived parameters with ``val`` and write the criterion signals to signals.csv
    with ``filterSimulationResults``. Returns the parsed outputs and the log."""
    os.makedirs(workdir, exist_ok=True)
    lines = [LOAD]
    if extra_file:
        lines.append('loadFile("%s");' % os.path.basename(extra_file))
    if settings is None:            # A: the example's own annotation settings
        lines.append('r := simulate(%s, outputFormat="mat");' % model_name)
    else:
        lines.append('r := simulate(%s, startTime=%s, stopTime=%s, numberOfIntervals=%d, '
                     'tolerance=%s, method="%s", outputFormat="mat");'
                     % (model_name, settings["start_s"], settings["stop_s"],
                        settings["intervals"], settings["tolerance"], settings["method"]))
    mat = model_name + "_res.mat"
    lines.append('f := "%s";' % mat)
    for name in PARAMETERS:
        lines.append('print("PARAM %s=" + String(val(%s, 0.0, f), significantDigits=17) + "\\n");'
                     % (name, name))
    lines.append('filterSimulationResults(f, "signals.csv", {%s});'
                 % ", ".join('"%s"' % x for x in ["time"] + SIGNALS))
    lines += ['print(getErrorString());', 'print("OMC_VERSION=" + getVersion() + "\\n");',
              'print("MSL_VERSION=" + getVersion(Modelica) + "\\n");']
    open(os.path.join(workdir, "run.mos"), "w").write("\n".join(lines) + "\n")
    proc = run_sandboxed(workdir, ["/bin/sh", "-c", "omc run.mos > omc.log 2>&1; "
                                   "echo EXIT=$? >> omc.log; tail -n +3 /proc/net/dev > netdev.txt"])
    log = open(os.path.join(workdir, "omc.log"), encoding="utf-8", errors="replace").read()
    params = {}
    for line in log.splitlines():
        if line.startswith("PARAM ") and "=" in line:
            key, value = line[6:].split("=", 1)
            params[key.strip()] = value.strip()
    sig = os.path.join(workdir, "signals.csv")
    matp = os.path.join(workdir, mat)
    netdev = os.path.join(workdir, "netdev.txt")
    return {"returncode": proc.returncode, "log": log, "csv": sig, "csv_exists": os.path.exists(sig),
            "mat_sha256": sha256(open(matp, "rb").read()) if os.path.exists(matp) else None,
            "params": params, "omc_exit_ok": "EXIT=0" in log,
            "solver_ok": "The simulation finished successfully." in log,
            "simulation_options": next((l.split("=", 1)[1].strip().rstrip(",")
                                        for l in log.splitlines() if "simulationOptions" in l), None),
            "netdev": open(netdev).read().strip() if os.path.exists(netdev) else None}


# --- analysis -----------------------------------------------------------------------------
def read_csv(path):
    with open(path, newline="") as fh:
        rows = list(csv.reader(fh))
    head = [h.strip().strip('"') for h in rows[0]]
    keep = {}
    for i, h in enumerate(head):
        keep.setdefault(h, i)            # filterSimulationResults repeats "time"
    cols = {h: [Decimal(row[i]) for row in rows[1:]] for h, i in keep.items()}
    return cols


def analyse(cols, params, prereg_doc):
    t, w, ia = cols["time"], cols["speedSensor.w"], cols["dcpm.ia"]
    wn = Decimal(params["driveData.motorData.wNominal"])
    ia_max = Decimal(params["driveData.IaMax"])
    band = Decimal("0.02") * wn
    after = [i for i, ti in enumerate(t) if ti >= LOAD_STEP_S]
    t_rec = None
    for i in reversed(after):
        if abs(w[i] - wn) > band:
            break
        t_rec = t[i]
    if t_rec is not None and abs(w[after[-1]] - wn) > band:
        t_rec = None
    dip = max(wn - w[i] for i in after)
    k1_met = t_rec is not None and (t_rec - LOAD_STEP_S) <= Decimal("0.15")
    i_peak = max(range(len(ia)), key=lambda k: abs(ia[k]))
    ia_peak = abs(ia[i_peak])
    k2_met = ia_peak <= ia_max

    def recovery(fraction):          # post-hoc, exploratory only: NOT a pre-registered gate
        tr = None
        for i in reversed(after):
            if abs(w[i] - wn) > fraction * wn:
                break
            tr = t[i]
        return None if tr is None or abs(w[after[-1]] - wn) > fraction * wn else tr
    # X1 exploratory: rigid-shaft residual at the last point, reported only
    i_end = len(t) - 1
    j_total = Decimal(params["driveData.JL"]) + Decimal(params["driveData.motorData.Jr"])
    tau_e, tau_l, acc = (cols["dcpm.tauElectrical"][i_end], cols["loadTorque.tau"][i_end],
                         cols["loadInertia.a"][i_end])
    x1 = {"residual_Nm": str(tau_e + tau_l - j_total * acc),
          "tauElectrical_end": str(cols["dcpm.tauElectrical"][i_end]),
          "loadTorque_tau_end": str(cols["loadTorque.tau"][i_end]),
          "tauShaft_end": str(cols["dcpm.tauShaft"][i_end]),
          "loadInertia_a_end": str(cols["loadInertia.a"][i_end]),
          "J_total": str(j_total),
          "note": "exploratory only, not a gate (pre-registration X1)"}
    return {"wNominal_rad_s": str(wn), "IaMax_A": str(ia_max),
            "model_derived_parameters": params,
            "K1": {"t_rec_s": str(t_rec) if t_rec is not None else None,
                   "recovery_after_load_s": str(t_rec - LOAD_STEP_S) if t_rec is not None else None,
                   "peak_dip_rad_s": str(dip), "w_end_rad_s": str(w[i_end]),
                   "outcome": "MET" if k1_met else "NOT MET"},
            "K2": {"max_abs_ia_A": str(ia_peak), "margin_A": str(ia_max - ia_peak),
                   "at_time_s": str(t[i_peak]),
                   "max_abs_ia_after_load_step_A": str(max(abs(ia[i]) for i in after)),
                   "outcome": "MET" if k2_met else "NOT MET"},
            "exploratory_post_hoc": {
                "note": "not pre-registered; reported only to describe the response, never as a gate",
                "t_rec_band_0.5pct_s": (lambda v: str(v) if v is not None else None)(recovery(Decimal("0.005"))),
                "max_va_V": str(max(cols["dcpm.va"])),
                "max_speed_controller_output_Nm": str(max(cols["speedController.y"]))},
            "X1_exploratory": x1, "points": len(t),
            "grid_resolution_s": prereg_doc["simulation"]["output_interval_s"]}


def sensitivity(a, b, wn, ia_max):
    """N1: compare the quantities behind the criteria at the two tolerances."""
    def d(x, y):
        return None if x is None or y is None else abs(Decimal(x) - Decimal(y))
    dt = d(a["K1"]["t_rec_s"], b["K1"]["t_rec_s"])
    out = {"delta_t_rec_s": str(dt) if dt is not None else None,
           "delta_peak_dip_rad_s": str(d(a["K1"]["peak_dip_rad_s"], b["K1"]["peak_dip_rad_s"])),
           "delta_max_abs_ia_A": str(d(a["K2"]["max_abs_ia_A"], b["K2"]["max_abs_ia_A"])),
           "same_outcomes": a["K1"]["outcome"] == b["K1"]["outcome"]
           and a["K2"]["outcome"] == b["K2"]["outcome"]}
    ok = ((dt is not None and dt <= Decimal("0.001"))
          or (a["K1"]["t_rec_s"] is None and b["K1"]["t_rec_s"] is None))
    ok = ok and d(a["K1"]["peak_dip_rad_s"], b["K1"]["peak_dip_rad_s"]) <= Decimal("0.001") * wn
    ok = ok and d(a["K2"]["max_abs_ia_A"], b["K2"]["max_abs_ia_A"]) <= Decimal("0.005") * ia_max
    out["within_bounds"] = bool(ok and out["same_outcomes"])
    out["verdict"] = "NUMERICALLY STABLE" if out["within_bounds"] else "NUMERICALLY SENSITIVE"
    return out


# --- the proof ------------------------------------------------------------------------------
def tool_identity():
    blobs = os.path.join(STAGE, "blobs")
    index = open(os.path.join(blobs, "index.json"), "rb").read()
    manifest = open(os.path.join(blobs, "manifest.json"), "rb").read()
    msl = subprocess.run(["git", "-C", os.path.join(STAGE, "msl"), "rev-parse", "HEAD"],
                         capture_output=True, text=True).stdout.strip()
    layers = [l["digest"] for l in json.loads(manifest)["layers"]]
    verified = all(sha256(open(os.path.join(blobs, d.split(":")[1]), "rb").read()) == d.split(":")[1]
                   for d in layers + [json.loads(manifest)["config"]["digest"]])
    return {"image": "openmodelica/openmodelica:v1.27.1-minimal",
            "index_digest": "sha256:" + sha256(index),
            "linux_amd64_manifest": "sha256:" + sha256(manifest),
            "config_digest": json.loads(manifest)["config"]["digest"], "layers": layers,
            "blobs_verified": verified, "msl_commit": msl}


def image_inventory():
    """The image's own package database and the OpenModelica packages' copyright notices."""
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
    notices = {}
    for pkg in ("omc", "omc-common", "libomc", "libomcsimulation"):
        path = os.path.join(root, "usr/share/doc", pkg, "copyright")
        text = open(path, encoding="utf-8", errors="replace").read()
        notices[pkg] = {"sha256": sha256(text),
                        "licence_statement": " ".join(l.strip(" *") for l in text.splitlines()
                                                      if "GPL VERSION 3 LICENSE OR" in l
                                                      or "OSMC PUBLIC LICENSE (OSMC-PL) VERSION" in l)}
    with open(os.path.join(EVIDENCE, "image_packages.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(sorted(pkgs)) + "\n")
    return {"installed_packages": len(pkgs), "package_list": "image_packages.txt",
            "omc_packages": sorted(p for p in pkgs if "omc" in p.split()[0]),
            "openmodelica_copyright_notices": notices,
            "msl_licence": "BSD-3-Clause (MSL LICENSE, sha256 4f708e2d...; SRC-061)"}


def main():
    if shutil.which("unshare") is None or not os.path.isdir(os.path.join(STAGE, "rootfs")):
        print(json.dumps({"verdict": "BLOCKED", "cause": "sandbox tools or the unpacked image are missing"}))
        return 2
    doc, prereg_sha = prereg()
    tool = tool_identity()
    p = doc["tool"]
    if (tool["index_digest"] != p["index_digest"] or tool["linux_amd64_manifest"] != p["linux_amd64_manifest"]
            or not tool["blobs_verified"] or tool["msl_commit"] != doc["library"]["commit"]):
        print(json.dumps({"verdict": "BLOCKED", "cause": "tool or library identity differs from the pre-registration", "tool": tool}))
        return 2
    for rel, digest in doc["library"]["files_sha256"].items():
        if sha256(open(os.path.join(STAGE, "msl", rel), "rb").read()) != digest:
            print(json.dumps({"verdict": "BLOCKED", "cause": "MSL file differs: " + rel}))
            return 2
    work = os.path.join(STAGE, "work")
    record = {"proof": doc["proof"], "preregistration_sha256": prereg_sha, "tool": tool,
              "isolation": {"host_uid": UID, "capabilities": "all dropped (inheritable and bounding), no_new_privs",
                            "namespaces": "user, mount, pid, net, ipc, uts (unshare, unprivileged)",
                            "limits": LIMITS + ["timeout %ds" % WALL_S],
                            "filesystem": "read-only image root after pivot_root, host root detached; MSL read-only; one writable work directory; 2 GiB tmpfs /tmp",
                            "network": "own network namespace with only a down loopback interface",
                            "environment": "cleared: HOME, TMPDIR, PATH and LANG only"},
              "image_inventory": image_inventory(),
              "runs": {}}
    # A: the unchanged example, its own annotation settings
    a = simulate(os.path.join(work, "A_smoke"), EXAMPLE)
    record["tool"]["omc_version"] = next((l.split("=", 1)[1].strip().strip('"') for l in a["log"].splitlines()
                                          if l.startswith("OMC_VERSION=")), None)
    record["runs"]["A_smoke"] = {"returncode": a["returncode"], "result_written": a["csv_exists"],
                                 "omc_exit_ok": a["omc_exit_ok"], "solver_ok": a["solver_ok"],
                                 "simulation_options": a["simulation_options"], "mat_sha256": a["mat_sha256"],
                                 "netdev": a["netdev"], "log_tail": a["log"][-1500:]}
    if a["csv_exists"]:
        store_gz(a["csv"], os.path.join(EVIDENCE, "results", "A_smoke.csv.gz"))
        record["runs"]["A_smoke"]["analysis"] = analyse(read_csv(a["csv"]), a["params"], doc)
        record["runs"]["A_smoke"]["csv_sha256"] = sha256(open(a["csv"], "rb").read())
    # B / D: the wrapper, two load cases, two tolerances; B1 primary twice
    sim = doc["simulation"]
    for case, factor in (("B1", "1.0"), ("B2", "1.6")):
        values = validate_inputs(base_inputs(factor))
        for tol_name, tol in (("primary", sim["tolerance_primary"]), ("sensitivity", sim["tolerance_sensitivity"])):
            repeats = ("1", "2") if (case == "B1" and tol_name == "primary") else ("1",)
            for rep in repeats:
                run_id = "%s_%s_%s" % (case, tol_name, rep)
                wd = os.path.join(work, run_id)
                os.makedirs(wd, exist_ok=True)
                name = "MP01_" + case
                src = wrapper_source(name, values)
                open(os.path.join(wd, name + ".mo"), "w").write(src)
                settings = {"start_s": sim["start_s"], "stop_s": sim["stop_s"],
                            "intervals": int(round(sim["stop_s"] / sim["output_interval_s"])),
                            "tolerance": tol, "method": sim["method"]}
                r = simulate(wd, name, extra_file=name + ".mo", settings=settings)
                entry = {"inputs": values, "settings": settings, "model_sha256": sha256(src),
                         "result_identity": result_identity(record["tool"], src, values, settings),
                         "returncode": r["returncode"], "result_written": r["csv_exists"],
                         "omc_exit_ok": r["omc_exit_ok"], "solver_ok": r["solver_ok"],
                         "simulation_options": r["simulation_options"], "mat_sha256": r["mat_sha256"],
                         "netdev": r["netdev"], "log_tail": r["log"][-1500:]}
                if r["csv_exists"]:
                    entry["csv_sha256"] = sha256(open(r["csv"], "rb").read())
                    entry["analysis"] = analyse(read_csv(r["csv"]), r["params"], doc)
                    store_gz(r["csv"], os.path.join(EVIDENCE, "results", run_id + ".csv.gz"))
                shutil.copyfile(os.path.join(wd, name + ".mo"), os.path.join(EVIDENCE, "models", name + ".mo"))
                record["runs"][run_id] = entry
    # C: a missing required input refuses before anything is written or translated
    broken = base_inputs("1.0")
    del broken["JL_kgm2"]
    c_dir = os.path.join(work, "C_refusal")
    try:
        wrapper_source("MP01_C", broken)
        record["runs"]["C_refusal"] = {"refused": False}
    except Refused as exc:
        record["runs"]["C_refusal"] = {"refused": True, "reason": str(exc),
                                       "model_written": os.path.exists(os.path.join(c_dir, "MP01_C.mo")),
                                       "omc_invoked": False}
    # D and N1
    R = record["runs"]
    b1, b1b, b2 = R["B1_primary_1"], R["B1_primary_2"], R["B2_primary_1"]
    record["D_identity"] = {
        "B1_repeat_same_identity": b1["result_identity"] == b1b["result_identity"],
        "B1_repeat_same_numbers": b1.get("csv_sha256") == b1b.get("csv_sha256"),
        "B2_differs_from_B1": b2["result_identity"] != b1["result_identity"]}
    if all("analysis" in R[k] for k in ("B1_primary_1", "B1_sensitivity_1", "B2_primary_1", "B2_sensitivity_1")):
        wn = Decimal(b1["analysis"]["wNominal_rad_s"])
        ia_max = Decimal(b1["analysis"]["IaMax_A"])
        record["N1_sensitivity"] = {
            "B1": sensitivity(R["B1_primary_1"]["analysis"], R["B1_sensitivity_1"]["analysis"], wn, ia_max),
            "B2": sensitivity(R["B2_primary_1"]["analysis"], R["B2_sensitivity_1"]["analysis"], wn, ia_max)}
    with open(os.path.join(EVIDENCE, "proof_record.json"), "w", encoding="utf-8") as fh:
        json.dump(record, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print(json.dumps({k: record[k] for k in ("D_identity",)}, indent=1))
    return 0


if __name__ == "__main__":
    os.makedirs(os.path.join(EVIDENCE, "results"), exist_ok=True)
    os.makedirs(os.path.join(EVIDENCE, "models"), exist_ok=True)
    sys.exit(main())
