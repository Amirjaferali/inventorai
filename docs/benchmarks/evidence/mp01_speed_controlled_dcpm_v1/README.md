# MP-01 SpeedControlledDCPM — isolated simulation proof (v1)

MP01-SPEED-CONTROLLED-DCPM-PROOF-01. Synthetic values only. This is not engineering
validation of any motor, load or controller, and nothing here enters the product.

## Order of work
1. `preregistration.json` was committed and pushed (`a32246c`) **before** the image was
   retrieved or any model was translated. It is unchanged since then: SHA-256
   `58b167ec8f11828fa06fd7e6db99231fa79c87ac26e7b1666dc05b67b49ac85c`.
2. The tool and library were retrieved and verified.
3. `scripts/mp01_speed_controlled_dcpm_proof.py` ran cases A to D once, in the sandbox
   described below. A second run of the same script, from a clean state, wrote this
   evidence.

## Tool, library and licences
- **OpenModelica image:** `openmodelica/openmodelica:v1.27.1-minimal`.
  - Index: `sha256:ac9a0223…a824`.
  - `linux/amd64` manifest: `sha256:1fa776fd…dc40`.
  - Config `sha256:b258212d…e59c` and both layers were each verified by SHA-256 before
    unpacking.
  - Contents: Ubuntu 22.04 with 222 installed packages (`image_packages.txt`), including
    `omc`, `omc-common`, `libomc` and `libomcsimulation` 1.27.1-1, and gcc/clang.
  - `getVersion()` returns "OpenModelica 1.27.1".
- **Deviation from MP-01:** MP-01 proposed OpenModelica 1.27.2, which isn't reachable here.
  By Owner decision this proof uses 1.27.1. No claim is made that the two are numerically
  interchangeable.
- **MSL:** v4.1.0 at `8ae3d35c24e519cb2996cab20f3b13daf2b0c50a`, loaded explicitly from that
  checkout. `getVersion(Modelica)` returns "4.1.0". The model files and LICENSE match MP-01's
  recorded hashes.
- **Licence findings:**
  - MSL model code is BSD-3-Clause (SRC-061).
  - The image's OpenModelica package copyright notices (SHA-256 `a091ec1d…996b`) state
    "GPL version 3 or OSMC-PL version 1.2". MP-01 read the 1.27.2 source tree's files as
    "AGPL v3 or OSMC-PL 1.8". That difference is recorded and **not resolved here**.
  - This proof is local, isolated use: nothing is distributed or hosted. So MP-01's use (a)
    applies, and use (c), distributing or hosting a built artifact, stays WAITING.
  - The image's package licences were not individually inspected.

## Isolation (no privileged daemon, no bare chroot)
Every `omc` run was started as follows:
- **Process:** started by host uid 65534 with every capability dropped (inheritable and
  bounding) and `no_new_privs` set.
- **Namespaces:** fresh user, mount, pid, net, ipc and uts namespaces (`unshare`, unprivileged).
- **Limits:** `prlimit` CPU 1500 s, address space 12 GB, file size 2 GB, 4096 open files,
  2048 processes; plus a 1800 s timeout.
- **Filesystem:** `scripts/mp01_sandbox/inner.sh` builds a root from the unpacked image,
  read-only, and adds:
  - a private `/proc`;
  - a 2 GiB `/tmp`;
  - four device nodes;
  - the MSL checkout, read-only;
  - one writable work directory.

  It then runs `pivot_root` and detaches the host root.
- **Network:** each run's network table (`netdev`) shows only an idle loopback, and `omc`'s own
  attempt to fetch its package index failed name resolution.
- **Environment:** cleared, so no project secrets and no inventor data are present. The
  image's setuid bits were stripped after unpacking.

## Frozen criteria and results (`proof_record.json`)
**Case definitions:**
- **A:** the unchanged example, run with its own annotation settings.
- **B1:** the wrapper with every required input declared and a load step of 1.0 × tauNominal.
- **B2:** the same wrapper, identical except for a load step of 1.6 × tauNominal, above
  tauMax = 1.5 × tauNominal.

The record's own model-derived values were read with `val()`: tauNominal 63.662 N·m,
tauMax 95.493 N·m, IaMax 150 A, kPhi 0.6366 V·s/rad, kpw 60, Tiw 0.01 s.

| Case | K1: speed back within ±2 % within 0.15 s of the load step | Peak speed dip | K2: max \|ia\| ≤ IaMax = 150 A |
|---|---|---|---|
| A | MET (never left the band) | 0.983 rad/s (0.66 %) | **NOT MET**: 159.10 A at t = 0.2059 s |
| B1 | MET (never left the band) | 0.983 rad/s | **NOT MET**: 159.10 A at t = 0.2059 s |
| B2 | **NOT MET**: no recovery, speed 142.95 rad/s at 1.0 s | 6.27 rad/s | **NOT MET**: 159.10 A |

**What the results mean:**
- **The K2 overshoot is in the unchanged example itself.** It happens during the start-up
  acceleration, not after the load step. The record's 1.5 × IaNominal limit is applied to the
  speed controller's output, and from it to the current reference; the actual armature current
  still overshoots by about 6 %. After the load step, |ia| peaks at 151.4 A (A and B1) and
  151.8 A (B2).
- **K1 doesn't discriminate for B1:** the ±2 % band is wider than the 0.66 % dip.
  - As a post-hoc, exploratory measure only, B1 returns within ±0.5 % at 0.8137 s.
- **In B2, the load exceeds the drive's torque limit:**
  - the speed controller saturates at tauMax (95.49 N·m);
  - the shaft keeps decelerating at about −21.2 rad/s²;
  - the speed doesn't recover.
- **Exploratory torque balance (X1, not a gate):** tauElectrical + tauLoad − (Jr + JL)·a,
  at 1.0 s, is about 1e-14 N·m in every case.

**Numerical sensitivity (N1, tolerance 1e-6 against 1e-8):** both B1 and B2 are NUMERICALLY
STABLE.
- Δ max |ia| = 2.6e-6 A.
- Δ peak dip ≤ 2.2e-7 rad/s.
- The recovery time is identical.
- The outcomes are the same.

**Identity (D):**
- Running B1 twice gives the same result identity and byte-identical numbers.
- B2 has a different identity.
- The identity is computed over the image digest, the `omc` version, the MSL commit, the
  wrapper source, the inputs, the settings and the pre-registration.

**Refusal (C):** without `JL_kgm2`, the run is refused before any model is written or `omc`
is invoked.

## Files
| File | Contents |
|---|---|
| `preregistration.json` | The frozen plan |
| `proof_record.json` | Every run's settings, inputs, identities, isolation evidence, log tail and analysis |
| `results/*.csv.gz` | The criterion signals of each run (deterministic gzip; each hash is over the raw CSV) |
| `models/MP01_B1.mo`, `models/MP01_B2.mo` | The wrapper sources |
| `image_packages.txt` | The image's installed packages |
| `SHA256SUMS` | Binds every file in this folder |

A successful compiler or solver exit is not engineering validation. A real claim would need
the motor's documented or measured parameters, the mechanism's load profile, the actual
controller, and validation against measurement.
