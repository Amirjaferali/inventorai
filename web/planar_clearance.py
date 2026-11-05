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
import re

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


# BOARD-ENCLOSURE-CAD-DOWNLOAD-01 (method contract §10A): the ONE handoff model the outbound
# CAD adapter (engine/planar_clearance_cad_export.py) maps. Built from a validated view only.
CAD_HANDOFF_FORMAT = "inventorai-planar-clearance-cad-handoff/1"
CAD_GUIDE_KEYS = tuple("UI_PCC_CAD_GUIDE_%d" % n for n in range(1, 9))


def cad_eligible(view):
    """True only for a CURRENT declaration whose existing evaluation reached MET or NOT MET."""
    return bool(view) and view.get("state") == STATE_CURRENT \
        and view.get("evaluation") is not None \
        and view["evaluation"]["outcome"] in (_pcc.OUTCOME_MET, _pcc.OUTCOME_NOT_MET)


def cad_handoff_model(project_id, view, text):
    """The handoff model for ONE eligible view, or ``None``. ``text(key, lang)`` is the UI
    catalogue. Geometry inputs are the declared decimal text; the outcome, margins and bound
    are copied from the method consumer's result, never recomputed. Never writes."""
    if not cad_eligible(view):
        return None
    m, ev, rec = view["material"], view["evaluation"], view["record"]
    artifact = _pcc.load_artifact()
    return {
        "eligible": True, "handoff_format": CAD_HANDOFF_FORMAT,
        "binding": {
            "project_id": project_id,
            "interface_id": view["interface_id"],
            "board": {"component_id": m["board"]["id"], "revision": m["board_revision"]},
            "enclosure": {"component_id": m["enclosure"]["id"],
                          "revision": m["enclosure_revision"]},
            "declaration_id": rec["declaration_id"],
            "declaration_revision_no": rec["head_revision_no"],
            "declaration_revision_id": rec["revision_id"],
            "snapshot_digest": rec["digest"],
            "method": {"id": m["method_id"], "version": m["method_version"]},
            "declaration_version": m["declaration_version"],
            "region_bound": {"id": ev["region_bound"]["consequence_id"],
                             "version": ev["region_bound"]["consequence_version"]},
            "axis_pairing": m["axis_pairing"],
            "unit": _pcc.UNIT,
        },
        "declared_values": {item["role"]: item["text"] for item in m["values"]},
        "region_description": m["region_description"],
        "evaluation": {
            "outcome": ev["outcome"],
            "axes": [{"axis": a["axis"], "margin_mm": a["margin_text"], "met": a["met"],
                      "conditional_min_region_mm": a["region_min_text"],
                      "conditional_additional_mm": a["additional_text"],
                      "conditional_min_region_enterable": a["region_min_enterable"]}
                     for a in ev["axes"]]},
        "limitations": list(artifact["limitations"]),
        "region_bound_statements": list(artifact["region_bound"]["statements"]),
        "guide": {lang: [text(key, lang) for key in CAD_GUIDE_KEYS] for lang in ("en", "ar")},
    }


def cad_bundle_filename(model):
    """A fixed-shape attachment name from identifiers only (hex / digits)."""
    b = model["binding"]
    return "inventorai-planar-clearance-%s-rev%d-%s.zip" % (
        b["declaration_id"][-8:], int(b["declaration_revision_no"]), b["snapshot_digest"])


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


# G1-PCC-LITERAL-SOURCE-AID-01: ONE bounded input aid. It LOCATES one literal
# "<number> x <number> mm" pair written in the inventor's original idea and
# shows it with its sentence; it never decides which component is the board,
# which number is X or Y, whether the numbers are right or whether any
# applicability declaration holds. The inventor assigns the axes and saves
# through the unchanged save path. Not a dimension parser: anything outside
# the narrow scope below is refused (``None``), never guessed. Nothing is
# stored; the numbers must pass the method's own strict grammar unchanged.
AID_MAX_IDEA_CHARS = 2000
AID_ORDERS = ("first_x", "first_y")
# The fixed opening of the documentary basis note the aid proposes. The save
# route refuses a note that opens with one of these but no longer matches the
# submitted board values (``aid_note_consistent``).
AID_NOTE_PREFIX = {"en": "From my original idea: ", "ar": "من فكرتي الأصلية: "}
_AID_NUMBER = r"[0-9]+(?:\.[0-9]+)?"
_AID_PAIR = re.compile(
    r"(?<![\w.,٫/+\-–−])(?P<a>%s)\s*[x×X*]\s*(?P<b>%s)\s*mm(?![\w²³])"
    % (_AID_NUMBER, _AID_NUMBER), re.ASCII)
# Any two numbers joined by a multiplication sign, whatever follows (another
# unit, no unit, other digit systems): a second one makes the idea ambiguous.
_AID_ANY_PAIR = re.compile(r"\d+(?:[.,٫]\d+)?\s*[x×X*]\s*\d", re.UNICODE)
_AID_ANY_NUMBER = re.compile(r"\d+(?:[.,٫]\d+)*", re.UNICODE)
# A sentence ends at ! ? ; ؛ ؟ a line break, or a dot that is not a decimal point.
_AID_SENTENCE_BREAK = re.compile(r"[!?;؛؟\n]|(?<![0-9])\.|\.(?![0-9])")
_AID_BOARD = re.compile(
    r"(?<!\w)(?:boards?|pcbs?)(?!\w)|(?<!\w)[وبلفك]?(?:ال|ل)?(?:لوحة|لوحه)(?!\w)",
    re.IGNORECASE)
_AID_OTHER_OBJECT = re.compile(
    r"(?<!\w)(?:box(?:es)?|case|cases|enclosures?|housings?|lid|cover|shell|"
    r"region|area|space|opening|slot)(?!\w)|"
    r"(?<!\w)(?:ال)?(?:صندوق|علبة|علبه|غلاف|حاوية|حاويه|غطاء|منطقة|منطقه|فتحة|فتحه)(?!\w)",
    re.IGNORECASE)
# Words that make the sentence hypothetical, approximate, alternative or
# negated. A stop list, not an interpreter: a listed word refuses the aid even
# where it would be harmless, which is the safe direction.
_AID_UNCERTAIN = re.compile(
    r"(?<!\w)(?:maybe|perhaps|might|could|would|should|if|unless|or|either|about|"
    r"around|approx(?:imately)?|roughly|nearly|almost|estimated?|guess(?:ed)?|"
    r"unsure|uncertain|not|never|no|cannot|without|instead|rather|unknown|tbd)(?!\w)|"
    r"n't(?!\w)|[~≈±]|"
    r"(?<!\w)[وف]?(?:ربما|قد|لعل|ربّما|إذا|اذا|لو|إن|أو|او|إما|اما|حوالي|حوالى|تقريبا|تقريبًا|"
    r"نحو|قرابة|لا|لن|لم|ليس|ليست|لست|ما|مش|مو|بدون|دون|غير|بدل|بدلا|بدلًا)(?!\w)",
    re.IGNORECASE)


def literal_board_pair(original_idea):
    """The ONE literal board-dimension pair of ``original_idea``, or ``None``.

    Returns ``{"passage", "span", "first", "second", "unit"}`` with every text
    copied verbatim from the idea. ``first`` / ``second`` are in the order the
    inventor wrote them; no axis is implied. Refused (``None``) unless ALL hold:
    the idea has exactly one ``A x B`` pair of any kind and it is ``A x B mm``
    in ASCII digits; its sentence names a board and no other object, holds no
    other number and no hypothetical, approximate, alternative or negating
    word; and both numbers pass the method's strict grammar for a dimension."""
    if not isinstance(original_idea, str) or not 0 < len(original_idea) <= AID_MAX_IDEA_CHARS:
        return None
    if len(_AID_ANY_PAIR.findall(original_idea)) != 1:
        return None
    pairs = list(_AID_PAIR.finditer(original_idea))
    if len(pairs) != 1:
        return None
    pair = pairs[0]
    breaks = [m.end() for m in _AID_SENTENCE_BREAK.finditer(original_idea, 0, pair.start())]
    start = breaks[-1] if breaks else 0
    end_match = _AID_SENTENCE_BREAK.search(original_idea, pair.end())
    end = end_match.start() if end_match else len(original_idea)
    sentence = original_idea[start:end]
    if not _AID_BOARD.search(sentence) or _AID_OTHER_OBJECT.search(sentence):
        return None
    if _AID_UNCERTAIN.search(sentence):
        return None
    if len(_AID_ANY_NUMBER.findall(sentence)) != 2:
        return None
    first, second = pair.group("a"), pair.group("b")
    if not (_pcc.is_admitted_value("board_x", first)
            and _pcc.is_admitted_value("board_y", second)):
        return None
    return {"passage": sentence.strip(), "span": pair.group(0),
            "first": first, "second": second, "unit": _pcc.UNIT}


def aid_assignment(pair, order):
    """``(board_x, board_y)`` for the inventor's explicit ``order`` choice."""
    if pair is None or order not in AID_ORDERS:
        return None
    if order == "first_x":
        return pair["first"], pair["second"]
    return pair["second"], pair["first"]


def aid_note(pair, order, lang):
    """The documentary basis note for ONE explicit assignment, in ``lang``.
    It quotes the source and states the inventor's own assignment; it never
    says the numbers were checked."""
    assignment = aid_assignment(pair, order)
    if assignment is None or lang not in AID_NOTE_PREFIX:
        return None
    x, y = assignment
    if lang == "ar":
        body = "«%s»؛ أدخلتُ %s لـ X و%s لـ Y للوحة." % (pair["span"], x, y)
    else:
        body = "“%s”; I entered %s as board X and %s as board Y." % (
            pair["span"], x, y)
    return AID_NOTE_PREFIX[lang] + body


def aid_note_claimed(note):
    """True when ``note`` opens with the aid's fixed prefix (either language)."""
    return isinstance(note, str) and any(note.startswith(p) for p in AID_NOTE_PREFIX.values())


def aid_offer(pair, lang):
    """The display model of the aid for ONE located pair in ``lang``: both
    explicit assignments with their proposed note, none pre-chosen."""
    if pair is None:
        return None
    return {"passage": pair["passage"], "span": pair["span"], "first": pair["first"],
            "second": pair["second"], "unit": pair["unit"],
            "orders": [{"order": order, "x": aid_assignment(pair, order)[0],
                        "y": aid_assignment(pair, order)[1],
                        "note": aid_note(pair, order, lang if lang in AID_NOTE_PREFIX else "en")}
                       for order in AID_ORDERS]}


def aid_note_consistent(note, pair, board_x, board_y):
    """False only for a note that opens with the aid's fixed prefix but is not
    exactly the note of the submitted board values (an edited value, a forged
    or stale note, or no locatable pair). Any other note is the inventor's own
    free text and is never judged."""
    if not aid_note_claimed(note):
        return True
    return any(aid_note(pair, order, lang) == note
               and aid_assignment(pair, order) == (board_x, board_y)
               for order in AID_ORDERS for lang in AID_NOTE_PREFIX)
