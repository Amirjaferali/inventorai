"""BOARD-ENCLOSURE-PLANAR-CLEARANCE-01 — the ONE shared presentation model.

The interaction page, the report and the PDF render the board-enclosure planar
clearance from THIS model only, built from ONE coherent store snapshot
(``SqliteRecordStore.load_planar_clearance``). It adds no formula: the margins
and the met / not-met decision come from the method consumer
(``engine/mechanical_planar_clearance.py``), the binding status from the
Stage-15 declaration owner (``engine/subsystem_model.py``). It persists nothing
and writes nothing; building it never changes durable truth. The diagram
geometry here is presentation only (proportional placement for an explanatory
sketch, never a measured drawing).
"""
import hashlib
import json

from engine import mechanical_planar_clearance as _pcc
from engine import subsystem_model as _sm

STATE_NONE = "NONE"                    # no declaration was ever made here
STATE_WITHDRAWN = "WITHDRAWN"          # history only; no active declaration
STATE_CURRENT = "CURRENT"              # every binding holds: evaluated
STATE_RECONFIRM = "NEEDS_RECONFIRMATION"  # a binding changed: NOT evaluated

_DIAGRAM_W = 360.0
_DIAGRAM_H = 240.0
_DIAGRAM_PAD = 34.0


def _component_label(inventory, component_id):
    record = inventory.record_for(component_id)
    if record is None:            # never for a validated snapshot
        return {"id": component_id, "name": None, "withdrawn": False, "revision": None}
    return {"id": component_id, "name": record.current.display_name,
            "withdrawn": record.withdrawn, "revision": record.head_revision_no}


def _material_view(material, inventory):
    values = material.values_map()
    basis = material.basis_map()
    return {
        "board": _component_label(inventory, material.board_component_id),
        "enclosure": _component_label(inventory, material.enclosure_component_id),
        "board_revision": material.board_component_revision,
        "enclosure_revision": material.enclosure_component_revision,
        "axis_pairing": material.axis_pairing,
        "region_description": material.region_description,
        "values": [{"role": role, "text": values[role],
                    "unknown": values[role] == _pcc.VALUE_UNKNOWN,
                    "entered": values[role] not in (None, _pcc.VALUE_UNKNOWN)}
                   for role in _pcc.VALUE_ROLES],
        "basis": [{"field": field, "text": basis[field]}
                  for field in _sm.PLANAR_CLEARANCE_BASIS_FIELDS],
        "applicability": [{"id": d, "ref": ref, "answer": material.applicability_map()[d]}
                          for d, ref in _pcc.DECLARATIONS],
        "method_id": material.method_id,
        "method_version": material.method_version,
        "declaration_version": material.declaration_version,
    }


def snapshot_digest(record):
    """A short identity of the exact revision history shown (revision ids and
    complete material), so a downloaded copy names exactly what it shows."""
    payload = [[r.revision_id, r.revision_no, r.kind,
                None if r.material is None else [
                    r.material.board_component_id, r.material.enclosure_component_id,
                    r.material.board_component_revision,
                    r.material.enclosure_component_revision,
                    r.material.board_participation_epoch,
                    r.material.enclosure_participation_epoch,
                    r.material.region_description, list(r.material.values),
                    list(r.material.basis), list(r.material.applicability),
                    r.material.method_id, r.material.method_version,
                    r.material.declaration_version]]
               for r in record.revisions]
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"),
                           ensure_ascii=True)
    return hashlib.sha256(canonical.encode("ascii")).hexdigest()[:16]


def diagram(material, evaluation):
    """Proportional geometry of the explanatory sketch, or ``None`` when no
    comparison exists. The region is drawn, the required clear zone inside it
    (dashed) and the centered board; a NOT MET axis is marked as overlapping
    the clear zone, never drawn as a fit."""
    if evaluation is None or evaluation["outcome"] not in (_pcc.OUTCOME_MET,
                                                             _pcc.OUTCOME_NOT_MET):
        return None
    values = {r: _pcc.parse_value(t) for r, t in material.values_map().items()}
    c = values["c"]
    extent_x = max(values["region_x"], values["board_x"] + 2 * c)
    extent_y = max(values["region_y"], values["board_y"] + 2 * c)
    scale = min((_DIAGRAM_W - 2 * _DIAGRAM_PAD) / float(extent_x),
                (_DIAGRAM_H - 2 * _DIAGRAM_PAD) / float(extent_y))
    cx, cy = _DIAGRAM_W / 2, _DIAGRAM_H / 2

    def rect(w, h):
        width, height = float(w) * scale, float(h) * scale
        return {"x": round(cx - width / 2, 2), "y": round(cy - height / 2, 2),
                "w": round(width, 2), "h": round(height, 2)}

    zone_w = values["region_x"] - 2 * c
    zone_h = values["region_y"] - 2 * c
    axes = {item["axis"]: item for item in evaluation["axes"]}
    return {
        "width": _DIAGRAM_W, "height": _DIAGRAM_H,
        "region": rect(values["region_x"], values["region_y"]),
        "zone": (rect(zone_w, zone_h) if c > 0 and zone_w > 0 and zone_h > 0 else None),
        "zone_collapsed": c > 0 and (zone_w <= 0 or zone_h <= 0),
        "board": rect(values["board_x"], values["board_y"]),
        "met_x": axes["x"]["met"], "met_y": axes["y"]["met"],
        "labels": {role: material.values_map()[role] for role in _pcc.VALUE_ROLES},
    }


def clearance_view(snapshot, interface_id, binding):
    """The presentation model for ONE interaction, or ``None`` when the
    interaction is not one of the snapshot's. Never writes."""
    interfaces = {item.interface_id: item for item in snapshot["interfaces"]}
    interface = interfaces.get(interface_id)
    if interface is None:
        return None
    inventory = snapshot["inventory"]
    ledger = snapshot["ledger"]
    names = {sub.subsystem_id: sub.display_name for sub in snapshot["subsystems"]}
    participants = _sm.current_interface_participants(
        snapshot["participations"], inventory.active).get(interface_id, ())
    options = []
    for component_id in participants:
        record = inventory.record_for(component_id)
        options.append({"id": component_id, "name": record.current.display_name,
                        "revision": record.head_revision_no,
                        "epoch": snapshot["epochs"].get((interface_id, component_id), 0)})
    history = ledger.history_for(interface_id)
    active = ledger.active_for(interface_id)
    view = {
        "interface_id": interface_id,
        "interface_description": interface.description,
        "part_a": names.get(interface.subsystem_a_id),
        "part_b": names.get(interface.subsystem_b_id),
        "options": options,
        "eligible": len(options) >= 2,
        "state": STATE_NONE,
        "record": None, "material": None, "raw_material": None, "issues": [],
        "evaluation": None, "diagram": None,
        "withdrawn_count": len([r for r in history if r.withdrawn]),
        "history": [],
        "identities_left": (_sm.MAX_PLANAR_CLEARANCE_IDENTITIES_PER_PROJECT
                            - len(ledger.records)),
    }
    if active is None:
        if history:
            view["state"] = STATE_WITHDRAWN
        return view
    material = active.current
    issues = _sm.planar_clearance_binding_issues(
        material, inventory, snapshot["participations"], snapshot["epochs"])
    view.update({
        "record": {"declaration_id": active.declaration_id,
                   "head_revision_no": active.head_revision_no,
                   "revision_id": active.current_revision.revision_id,
                   "corrections": active.corrections,
                   "corrections_left": (_sm.MAX_PLANAR_CLEARANCE_CORRECTIONS
                                        - active.corrections),
                   "digest": snapshot_digest(active)},
        "material": _material_view(material, inventory),
        "raw_material": material,
        "issues": [{"issue": issue, "role": role} for issue, role in issues],
        "history": [{"revision_no": r.revision_no, "kind": r.kind,
                     "revision_id": r.revision_id,
                     "values": (None if r.material is None
                                else [{"role": role, "text": text} for role, text
                                      in r.material.values_map().items()])}
                    for r in active.revisions],
    })
    if issues:
        view["state"] = STATE_RECONFIRM
        return view
    view["state"] = STATE_CURRENT
    evaluation = _pcc.evaluate(material.evaluation_input(), binding)
    view["evaluation"] = evaluation
    view["diagram"] = diagram(material, evaluation)
    return view
