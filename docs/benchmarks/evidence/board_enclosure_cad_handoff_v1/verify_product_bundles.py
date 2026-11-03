"""FreeCAD 1.0.2 (GUI build under Xvfb): import geometry.dxf of each PRODUCT-ROUTE bundle with the
built-in C++ importer and the settings qualified in BOARD-ENCLOSURE-CAD-HANDOFF-PROOF-01; verify the
companion hash; measure the outlines against the companion's declared decimal text (Fraction)."""
import glob, hashlib, io, json, os, traceback, zipfile
from fractions import Fraction
ROOT = os.environ["CAD_ROOT"]
LOG = open(os.path.join(ROOT, "verify.log"), "w")
try:
    import FreeCAD, FreeCADGui, Part, importDXF
    TOL = 1e-9
    prefs = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Draft")
    SETTINGS = {"dxfUseLegacyImporter": False, "dxfShowDialog": False, "dxfUseDraftVisGroups": True,
                "dxfCreatePart": True, "dxfCreateDraft": False, "dxfCreateSketch": False,
                "joingeometry": False, "groupLayers": False}
    for k, v in SETTINGS.items():
        prefs.SetBool(k, v)
    prefs.SetFloat("dxfScaling", 1.0)
    results = {"freecad": ".".join(FreeCAD.Version()[:4]), "gui": FreeCAD.GuiUp,
               "settings": {**{k: prefs.GetBool(k) for k in SETTINGS}, "dxfScaling": prefs.GetFloat("dxfScaling")},
               "tolerance_mm": TOL, "bundles": {}}
    for zpath in sorted(glob.glob(os.path.join(ROOT, "bundles", "*.zip"))):
        name = os.path.basename(zpath)[:-4]
        zf = zipfile.ZipFile(zpath)
        files = {n: zf.read(n) for n in zf.namelist()}
        comp = json.loads(files["companion.json"].decode("utf-8"))
        work = os.path.join(ROOT, "extracted", name)
        os.makedirs(work, exist_ok=True)
        dxf_path = os.path.join(work, "geometry.dxf")
        open(dxf_path, "wb").write(files["geometry.dxf"])
        entry = {"members": zf.namelist(),
                 "sha256_ok": hashlib.sha256(files["geometry.dxf"]).hexdigest() == comp["dxf"]["sha256"],
                 "revision": comp["binding"]["declaration_revision_no"],
                 "snapshot_digest": comp["binding"]["snapshot_digest"],
                 "outcome": comp["evaluation"]["outcome"],
                 "margins": [a["margin_mm"] for a in comp["evaluation"]["axes"]]}
        doc = FreeCAD.newDocument("V" + name[:1])
        importDXF.insert(dxf_path, doc.Name)
        doc.recompute()
        members = {}
        for o in doc.Objects:
            if o.TypeId == "App::FeaturePython" and hasattr(o, "Group") and o.Proxy.__class__.__name__ == "Layer":
                for m in o.Group:
                    members[m.Name] = o.Label
        v = comp["declared_values"]
        expect = {"IAI_DECLARED_USABLE_REGION": (v["region_x"], v["region_y"]),
                  "IAI_DECLARED_BOARD_OUTLINE": (v["board_x"], v["board_y"])}
        ok, measured = entry["sha256_ok"], {}
        for layer, (w, h) in expect.items():
            hits = [o for o in doc.Objects if o.TypeId == "Part::Feature" and members.get(o.Name) == layer]
            if len(hits) != 1:
                ok = False; measured[layer] = "%d shapes" % len(hits); continue
            s = hits[0].Shape
            wire = Part.Wire(Part.__sortEdges__(s.Edges))
            bb = s.BoundBox
            errs = [abs(Fraction(bb.XLength) - Fraction(w)), abs(Fraction(bb.YLength) - Fraction(h)),
                    abs(Fraction((bb.XMin + bb.XMax) / 2)), abs(Fraction((bb.YMin + bb.YMax) / 2))]
            m = {"declared_mm": [w, h], "width_mm": bb.XLength, "height_mm": bb.YLength,
                 "centre_mm": [(bb.XMin + bb.XMax) / 2, (bb.YMin + bb.YMax) / 2], "z_mm": [bb.ZMin, bb.ZMax],
                 "edges": len(s.Edges), "closed": wire.isClosed(),
                 "line_edges": all(e.Curve.TypeId == "Part::GeomLine" for e in s.Edges),
                 "max_abs_transfer_error_mm": float(max(errs))}
            m["pass"] = (m["max_abs_transfer_error_mm"] <= TOL and m["edges"] == 4 and m["closed"]
                         and m["line_edges"] and bb.ZMin == bb.ZMax == 0)
            ok = ok and m["pass"]
            measured[layer] = m
        entry["measured"], entry["pass"] = measured, ok
        results["bundles"][name] = entry
        FreeCAD.closeDocument(doc.Name)
    json.dump(results, open(os.path.join(ROOT, "product_measurements.json"), "w"), indent=2, default=str)
    LOG.write("OK\n")
except Exception:
    LOG.write(traceback.format_exc())
LOG.close()
os._exit(0)
