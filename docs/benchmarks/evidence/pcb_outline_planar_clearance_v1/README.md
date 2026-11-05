# PCB outline → planar clearance → CAD reference — synthetic proof (v1)

PCB-OUTLINE-TO-PLANAR-CLEARANCE-PROOF-01. Synthetic data only: every board file here is an
InventorAI test fixture, not a real design. Nothing here is a project record, a validated
result, a tool admission or a product feature.

## What was run
- **Tool:** `kicad-cli` 7.0.11 (`kicad-cli version`), from the Ubuntu 24.04 official archive
  package `kicad 7.0.11+dfsg-1build4 amd64` (noble/universe; no PPA). Binary SHA-256:
  `390de70be2e43114fec97941fe3f72dcd70a254c03303a116369ba58a93d14a0`.
  - **Licence notices:** the package's own `/usr/share/doc/kicad/copyright` (SHA-256
    `fdb6508741cecb5a50c0d2e84d72ee1d9f17b63e35027d0caa6203b234bbd0ca`). Its main `Files: *`
    licence is GPL-3+; other files carry GPL-2+, LGPL-2.1+, BSD-3-clause, Expat, WXWINDOWS,
    CC-BY-SA-3.0 and CC-BY-SA-4.0 (the full field list is in `proof_record.json`).
  - **Use:** the unmodified program ran as a separate process on synthetic files in an isolated
    container. It is not an InventorAI dependency, no KiCad binary or source is bundled or
    copied here, and the inputs are InventorAI's own synthetic boards.
  - **Command reference:** the installed 7.0.11 CLI's own help, kept as
    `kicad_cli_7.0.11_pcb_export_dxf_help.txt`. It shows the default output unit is inches,
    so `--output-units mm` is passed explicitly.
- **Environment:** Ubuntu 24.04.5 LTS, x86_64, Python 3.13.18, ezdxf 1.4.2.
- **Command, for each fixture:** `kicad-cli pcb export dxf --layers Edge.Cuts --output-units mm
  --exclude-refdes --exclude-value -o exports/<name>.dxf fixtures/<name>.kicad_pcb`.
  - The default output unit is inches, which `board_v1_inch_export` uses as a units control.
  - Re-exporting gave byte-identical files.
- **Harness:** `scripts/pcb_outline_planar_clearance_proof.py`. Three independent readings:
  1. **The board file's text**, through a strictly bounded proof-only reader: one `gr_rect`,
     or four `gr_line`, on `Edge.Cuts`, format version `20221018` only. Anything else
     refuses: another version, malformed text, a non-board file, any other shape or text on
     `Edge.Cuts`, or outline graphics inside a footprint. It does not claim general KiCad
     format support.
  2. **The KiCad export, through this proof's own DXF group-code reader:** only LINE entities,
     metric `$MEASUREMENT 1`, exactly four axis-aligned segments in one closed loop.
  3. **The KiCad export, through `ezdxf` 1.4.2:** it reads the file as DXF R12 (`AC1009`), and
     the same rules are applied to what it parses.

  A board is supported only when all three agree within this proof's 1e-9 mm measurement
  tolerance. That tolerance belongs to the proof, not to the method. The value of record is
  the exact decimal in the board file.
- **Product route:** the harness then drives the real product routes through the Flask test
  client on a scratch database:
  - an integrated project, one interaction and two participating components;
  - the extracted values typed into the existing declaration form, with a basis note naming
    the file, its SHA-256 and the tool;
  - region 86 × 56 mm, `c` = 2 mm, and all eight declarations answered `applies`;
  - then the existing CAD download.

  Nothing is adopted automatically: the harness acts as the inventor.

## Results (`proof_record.json`)
**Supported geometry:**

| Fixture | Board file | Own DXF reader | ezdxf | Declared |
|---|---|---|---|---|
| `board_v1` (`gr_rect`) | 84 × 50 | 84 × 50 | 84 × 50 | 84 × 50 |
| `board_v1_lines` (four `gr_line`) | 84 × 50 | 84 × 50 | 84 × 50 | 84 × 50 |
| `board_v2` (revised) | 80 × 50 | 80 × 50 | 80 × 50 | 80 × 50 |

`board_v1` and `board_v1_lines` export byte-identical DXFs.

**Engineering check:** both results come from the existing method
`mechanical:planar_centered_rectangular_clearance` 1.0.
- v1 is NOT MET, with margins X −1 mm and Y +1 mm, at revision 0.
- v2 is MET, with margins +1 mm and +1 mm, at revision 1.

**CAD reference:** the existing PR #917 download.
- Each ZIP's companion binds its `geometry.dxf` by SHA-256.
- The harness's own reader measures the board outline at 84 × 50 (v1) and 80 × 50 (v2), and
  the region at 86 × 56.
- FreeCAD was not rerun here. Its import of this export route is the earlier evidence in
  `../board_enclosure_cad_handoff_v1/`.

**Source change:**
- **Before re-declaring:** the product page still shows the v1 result as current. InventorAI
  keeps no board file and has no source-revision lifecycle.
- **Harness check:** it finds that the current declaration names the v1 digest, not the v2
  one, and reports a SOURCE MISMATCH. That check belongs to this harness, not to the product.
- **After the inventor re-declares from v2:** revision 1 has a new snapshot digest, and the
  old CAD link answers 409 with no ZIP. That is the product's existing refusal of a stale
  declaration revision.

**Refused:** each refusal gives its reason from the board-file reader and the own DXF reader,
and `ezdxf` refuses every one as well.

| Fixture | Board-file reading | Export reading |
|---|---|---|
| `neg_rounded_corners` | `gr_arc` present | ARC entities present |
| `neg_l_shape` | 6 segments | 6 segments |
| `neg_cutout` | `gr_circle` cut-out | CIRCLE entity |
| `neg_two_boards` | 2 separate rectangles | 8 segments |
| `neg_open_outline` | 3 segments | 3 segments |
| `neg_no_outline` | no outline | no entities |
| `neg_rotated` | not axis-aligned | not axis-aligned |
| `board_v1_inch_export` | the board itself is supported | export not metric (`$MEASUREMENT 0`) |

No dimension is inferred for any refused case.

## Limits
- This is a planar comparison of declared nominal values. It says nothing about PCB–enclosure
  compatibility, mounting, height, tolerances, manufacturability, electrical validity or
  safety.
- It qualifies one KiCad version, one board-file format version and one rectangle shape.
- The CAD bundles do not carry the board-file digest: it lives only in the declaration's
  basis note.
- The export's DXF layer is named `BLACK`, so layer identity is not preserved. The proof
  relies on exporting `Edge.Cuts` alone.

`SHA256SUMS` binds every file in this folder.
