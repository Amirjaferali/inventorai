# KiCad 10.0.8 board-format qualification — synthetic proof (v1)

KICAD10-FORMAT-QUALIFICATION-PROOF-01. Synthetic data only. This is not a product feature,
an upload route or a reader admission. `BOARD-OUTLINE-SOURCE-BINDING-01` stays BLOCKED.

## Order of work
1. `preregistration.json` was committed and pushed (`f538b62`) before the image was retrieved.
   It is unchanged: SHA-256 `31206692fb43144dff022e973f7387bcf1356342280008f9a38e7c962126cf43`.
2. The image was retrieved and verified, then unpacked.
3. `scripts/kicad10_format_qualification_proof.py` was run. A final run from a clean state
   wrote this evidence.

## Tool and licences
- **Image:** `kicad/kicad:10.0.8`.
  - Index `sha256:3f4a0178…dc34` and `linux/amd64` manifest `sha256:05f6ac95…161c`, both
    matching the pre-registration.
  - The config and all 13 layers were each verified by SHA-256 before unpacking. No setuid or
    setgid file was present.
  - Contents: Debian GNU/Linux 13 (trixie) with 634 installed packages (`image_packages.txt`).
  - Versions: `kicad-cli version` and `pcbnew.Version()` both return **10.0.8**.
- **Licences:**
  - The image's OCI label declares `GPL-3.0-or-later`, with source
    `gitlab.com/kicad/kicad-ci/kicad-cli-docker`.
  - KiCad is not a Debian package in this image, and **the image contains no KiCad licence
    file**. That is recorded as a finding.
  - KiCad was used unmodified as a separate program; nothing from it is bundled.
  - The image's stock symbol and footprint libraries were **not used**: every fixture is
    InventorAI's own synthetic board.
- **Isolation:** the PR #934 sandbox runner, unchanged.
  - The process is launched by host uid 65534 holding no host capabilities, with
    `no_new_privs`.
  - It runs in unprivileged user, mount, pid, net, ipc and uts namespaces, with `prlimit`
    limits.
  - The image root is read-only after `pivot_root`, the network holds only an idle loopback,
    and the environment is cleared.
  - Inside its user namespace, KiCad runs as that namespace's root, mapped to host uid 65534.
- **Export command:** KiCad 10's `pcb export dxf` takes an output **directory** by default.
  The proof therefore uses the documented `--mode-single`:
  `kicad-cli pcb export dxf --mode-single --layers Edge.Cuts --output-units mm -o <file> <board>`.
  The installed help is kept in `kicad_cli_10.0.8_pcb_export_dxf_help.txt`.

## Results (`proof_record.json`)
- **Format:** KiCad 10.0.8 writes board format **`20260206`**. That is the only accepted
  version. The `20221018` control and any other version are refused.
- **G1, supported boards:** these fixtures, all written by KiCad 10.0.8, were admitted, and
  all three readings agree exactly:
  - the native 84 × 50 rectangle, the same rectangle as four lines, and the revised 80 × 50;
  - the three #933 KiCad 7 fixtures after KiCad 10 loaded and saved them;
  - five envelope boards with 0 to 100 footprints.

  The three readings are the board-file text through the admission rule, KiCad 10's own DXF
  export through the #933 reader, and the same export through `ezdxf`. KiCad 10's DXF is
  `AC1018`, and both DXF readers read it. The native and upgraded 84 × 50 boards export
  byte-identical DXFs.
- **G2, controls:** **none is admitted.**
  - The admission rule refused 14 geometry controls (7 native, 7 upgraded): rounded corners,
    an L shape, a cut-out, two boards, an open outline, no outline and a rotated rectangle.
    KiCad legitimately exported all of them, and both DXF readers reported each one's actual
    geometry.
  - It also refused four edited text controls:
    - an `angle` field on a `gr_line`, refused by the allowlist;
    - an unknown `rotation` field on a `gr_rect`, refused by the allowlist;
    - format version `20221018`, refused by the version rule, although KiCad 10 loads and
      exports that file;
    - doubled lines, refused by F1 ("not two horizontal and two vertical sides").
  - KiCad's own loader also rejected the two edited-field files ("Expecting 'start'"), so no
    export was produced for them.
  - The inch export was refused as `$MEASUREMENT 0`.
- **G3, freshness:** each output path was cleared first, and a file counted only on exit 0.
  Every failed export was recorded as "no output accepted".
- **G4 and O1, determinism:** every repeated export was **byte-identical**, so the geometry
  matches too.
- **O2, envelope against the unchanged 128 KiB cap:**

  | Footprints | File size | Fits under 128 KiB | Tokens | Nesting depth |
  |---|---|---|---|---|
  | 0 | 2.2 KB | yes | 394 | 4 |
  | 5 | 12.8 KB | yes | 2,339 | 6 |
  | 20 | 61.0 KB | yes | 11,154 | 6 |
  | 40 | 189 KB | **no** | 34,414 | 6 |
  | 100 | 505 KB | **no** | 92,694 | 6 |

  The admission check takes at most 0.05 s. Real library footprints carry more content than
  these synthetic ones.

## Scope
- **What is qualified:** only the exact KiCad 10.0.8 output format `20260206`, and only the
  constructs observed: one `gr_rect` or four `gr_line` on `Edge.Cuts`, with the allowlisted
  fields.
- **What is not:** other KiCad 10.x releases, other format versions and arbitrary PCB files.
  Footprint-level outlines, arcs and other shapes are refused, and nothing is approximated.
- **What doesn't change:** the 128 KiB cap, any product owner or route, and the method. No
  provider is called.

`SHA256SUMS` binds every file in this folder.
