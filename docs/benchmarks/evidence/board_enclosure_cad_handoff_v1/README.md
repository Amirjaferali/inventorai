# Board-enclosure CAD handoff — synthetic evidence (v1)

Synthetic invention data only. Nothing here is a project record, a validated result or a tool admission.

## 1. Executor proof — BOARD-ENCLOSURE-CAD-HANDOFF-PROOF-01 (2026-11-02, product HEAD `3d259e7`)
`handoff_proof_bundle.tar.gz` is the bundle the executor delivered in the originating session
(`session_01UZzqpfjzUNb9gEdegwyTTR`): scratch scripts (handoff model → ezdxf 1.4.2 DXF → FreeCAD 1.0.2
import), DXF files with companions, FreeCAD documents, `measurements.json` and its README. Executor's
reported verdict: PROVEN FOR THE TESTED SCOPE. It was not independently reproduced as part of the proof.

## 2. Product-route verification — BOARD-ENCLOSURE-CAD-DOWNLOAD-01
`product_route_bundles/*.zip` were produced by the PRODUCT download route
(`/session/<sid>/interface-clearance/<interface_id>/cad.zip`, Flask test client, synthetic projects):
A = 84 × 50 board in 86 × 56 region, c = 2 (NOT MET, revision 0); B = the same declaration corrected to
region X = 88 (MET, revision 1); C = 99.9 / 100.1 / 0.1 (MET, exact margin 0).
`verify_product_bundles.py` imported each `geometry.dxf` in FreeCAD 1.0.2 (build 39319, official
`FreeCAD_1.0.2-conda-Linux-x86_64-py311.AppImage`, SHA-256
`e00be00ad9fdb12b05c5002bfd1aa2ea8126f2c1d4e2fb603eb7423b72904f61`), GUI build run headless under Xvfb,
built-in C++ importer, settings recorded in `product_measurements.json` (`dxfScaling` 1.0, layers kept,
import dialog off). Results: every companion hash matches its DXF; both outlines of every bundle import as
four closed straight edges at z = 0, centred, on their own layers; transfer error 0 (A, B) and about
5.7e-15 mm (C) against the declared decimals, within the reported 1e-9 mm measurement tolerance — a property
of the receiving tool, not of the method, whose exact-decimal verdict is unchanged.

These bundles were produced at product commit `d28a915`; their `README.txt` carries the guide wording
of that commit (the later correction of guide line 6, which says the SHA-256 identifies `geometry.dxf`
and that the companion records the same value, is not regenerated here).

FreeCAD and ezdxf are not vendored here. `SHA256SUMS` binds every file in this folder.
