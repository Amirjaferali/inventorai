"""BOARD-ENCLOSURE-CAD-DOWNLOAD-01 — the outbound CAD reference adapter (method contract §10A).

ONE pure mapping (deterministic in geometry and fields) from ONE validated handoff model (built by the shared
presentation model, ``web/planar_clearance.py`` ``cad_handoff_model``) to ONE in-memory ZIP:

    geometry.dxf    the DECLARED board and usable internal region, true scale, mm (DXF R2013)
    companion.json  the binding, original decimal inputs, existing evaluation and conditional
                    bound, bound to that exact DXF by SHA-256
    README.txt      a UTF-8 guide in English and Arabic, with the notices

The DXF writer stamps fresh file metadata (GUIDs, creation time) on every write, so the bytes of
geometry.dxf, and therefore its SHA-256, differ between downloads of the same revision; the stable
identity is the declaration revision id plus the snapshot digest the companion carries.

What it does: coordinate and format mapping only. Origin at the centre of the declared region
(a drawing convention), +X along ``region_x``, +Y along ``region_y``; each outline is ONE closed
LWPOLYLINE on its own stable layer. The geometry is the inventor's CURRENT declared values,
NEVER the conditional minimum.

What it does not do: decide eligibility (the caller's model says so), recompute any verdict,
margin or bound (copied verbatim from the method consumer), read a store, request, session or
file, call a network or CAD tool, write a file, or retain anything. ``ezdxf`` is imported lazily
so the rest of the application never depends on it. Any failure raises ``CadExportError`` and
no partial bundle exists.
"""
import hashlib
import io
import json
import zipfile
from fractions import Fraction

ADAPTER_ID = "inventorai-planar-clearance-dxf"
ADAPTER_VERSION = "1"
HANDOFF_FORMAT = "inventorai-planar-clearance-cad-handoff/1"
DXF_VERSION = "R2013"
LAYER_REGION = "IAI_DECLARED_USABLE_REGION"
LAYER_BOARD = "IAI_DECLARED_BOARD_OUTLINE"
# Fixed archive paths (never derived from input) and a size bound for the whole bundle.
ARCHIVE_DXF = "geometry.dxf"
ARCHIVE_COMPANION = "companion.json"
ARCHIVE_GUIDE = "README.txt"
MAX_BUNDLE_BYTES = 1024 * 1024
_ZIP_DATE = (1980, 1, 1, 0, 0, 0)
_REQUIRED_MODEL = ("handoff_format", "binding", "declared_values", "evaluation",
                   "limitations", "region_bound_statements", "guide")


class CadExportError(Exception):
    """The bundle could not be produced. Nothing partial is returned."""


def _corners(width_text, height_text):
    """Centred, axis-aligned rectangle corners from EXACT decimal text."""
    hx, hy = Fraction(width_text) / 2, Fraction(height_text) / 2
    return [(-hx, -hy), (hx, -hy), (hx, hy), (-hx, hy)]


def dxf_bytes(model):
    """The DXF of the declared outlines (bytes). Raises ``CadExportError``."""
    try:
        import ezdxf
        from ezdxf import units
    except Exception as exc:                      # the writer is unavailable
        raise CadExportError("DXF writer unavailable") from exc
    try:
        values, binding = model["declared_values"], model["binding"]
        doc = ezdxf.new(DXF_VERSION, units=units.MM)          # $INSUNITS = 4 (mm)
        doc.header["$MEASUREMENT"] = 1                        # metric
        for key in ("declaration_id", "declaration_revision_id", "snapshot_digest"):
            doc.header.custom_vars.append("IAI_" + key.upper(), str(binding[key]))
        doc.layers.add(LAYER_REGION)
        doc.layers.add(LAYER_BOARD)
        msp = doc.modelspace()
        for layer, (w, h) in ((LAYER_REGION, (values["region_x"], values["region_y"])),
                              (LAYER_BOARD, (values["board_x"], values["board_y"]))):
            msp.add_lwpolyline([(float(x), float(y)) for x, y in _corners(w, h)],
                               close=True, dxfattribs={"layer": layer})
        stream = io.StringIO()
        doc.write(stream)
        return stream.getvalue().encode(doc.output_encoding), ezdxf.__version__
    except CadExportError:
        raise
    except Exception as exc:
        raise CadExportError("DXF mapping failed") from exc


def companion(model, dxf_sha256, writer_version, generated_at):
    """The companion record (dict) bound to the DXF by its SHA-256. A file-linked
    declaration adds ONE ``source`` object (BOARD-OUTLINE-SOURCE-BINDING-01); a
    source-free companion is unchanged."""
    record = _companion(model, dxf_sha256, writer_version, generated_at)
    if model.get("source") is not None:
        record["source"] = model["source"]
    return record


def _companion(model, dxf_sha256, writer_version, generated_at):
    return {
        "handoff_format": model["handoff_format"],
        "adapter": {"id": ADAPTER_ID, "version": ADAPTER_VERSION,
                    "dxf_writer": {"name": "ezdxf", "version": writer_version,
                                   "licence": "MIT"}},
        "generated_at": generated_at,
        "dxf": {"path": ARCHIVE_DXF, "sha256": dxf_sha256, "version": DXF_VERSION,
                "insunits": 4, "unit": "mm"},
        "coordinate_convention": (
            "origin = centre of the declared usable region; +X along region_x; +Y along "
            "region_y; the board is centred and axis-aligned (board X along region X); a "
            "drawing convention, not a physical feature"),
        "layers": {LAYER_REGION: "declared usable internal region at the board plane "
                                 "(current declared values)",
                   LAYER_BOARD: "declared board outline (current declared values)"},
        "binding": model["binding"],
        "declared_values": model["declared_values"],
        "region_description": model.get("region_description"),
        "evaluation": model["evaluation"],
        "conditional_bound_note": (
            "conditional_min_region and conditional_additional are the method's derived "
            "consequence: they are NOT geometry in geometry.dxf and hold only while the "
            "declared board, clearance, centred placement and applicability stay as declared"),
        "limitations": model["limitations"],
        "region_bound_statements": model["region_bound_statements"],
        "not_in_file": ["height", "thickness", "material", "holes", "connectors",
                        "tolerances", "mounting", "parametric constraints"],
        "status": ("planar reference snapshot of declared values; not an enclosure design, "
                   "manufacturing approval, parametric model or whole-product verification; "
                   "external CAD edits are unassessed and never synchronise back; the hash "
                   "binds the delivered files and is not physical verification"),
    }


def _guide(model, dxf_sha256):
    lines = []
    for lang in ("en", "ar"):
        lines.extend(model["guide"][lang])
        lines.append("geometry.dxf SHA-256: " + dxf_sha256)
        lines.append("")
    return "\n".join(lines).encode("utf-8")


def _zip(members):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in members:
            info = zipfile.ZipInfo(name, date_time=_ZIP_DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, data)
    return buffer.getvalue()


def build_bundle(model, generated_at):
    """``bytes`` of the ZIP for ONE eligible handoff model, or raise ``CadExportError``.
    The DXF, the companion and the guide come from this one model only."""
    if not isinstance(model, dict) or model.get("eligible") is not True \
            or any(key not in model for key in _REQUIRED_MODEL):
        raise CadExportError("not an eligible handoff model")
    dxf, writer_version = dxf_bytes(model)
    digest = hashlib.sha256(dxf).hexdigest()
    try:
        record = json.dumps(companion(model, digest, writer_version, generated_at),
                            ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8")
        bundle = _zip(((ARCHIVE_DXF, dxf), (ARCHIVE_COMPANION, record),
                       (ARCHIVE_GUIDE, _guide(model, digest))))
    except Exception as exc:
        raise CadExportError("bundle assembly failed") from exc
    if len(bundle) > MAX_BUNDLE_BYTES:
        raise CadExportError("bundle exceeds its size bound")
    return bundle
