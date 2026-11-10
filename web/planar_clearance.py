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

from engine import idea_state as _ledger
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
        "source": source_view(material),
    }


def source_view(material):
    """BOARD-OUTLINE-SOURCE-BINDING-01: the file link of a v2 material as shown,
    or ``None`` for a source-free one. The agreement (EXACT / DIFFERS) is derived
    here on every read by exact decimal comparison; the calculation always uses
    the DECLARED values."""
    agreement = _sm.planar_clearance_source_agreement(material)
    if agreement is None:
        return None
    state, changed, file_dims, declared = agreement
    src = material.source
    return {
        "kind": src.kind, "sha256": src.source_sha256, "sha256_short": src.source_sha256[:12],
        "size": src.source_size, "format_id": src.format_id, "reader_id": src.reader_id,
        "rule_id": src.rule_id, "file_x": src.file_x, "file_y": src.file_y,
        "axis_assignment": src.axis_assignment, "inspected_at": src.inspected_at,
        "carried_forward": src.carry_forward_from is not None,
        "agreement": state, "changed_axes": list(changed),
        "file_board": {"board_x": file_dims[0], "board_y": file_dims[1]},
        "declared_board": {"board_x": declared[0], "board_y": declared[1]},
    }


def _source_digest_item(source):
    return [source.kind, source.source_sha256, source.source_size, source.format_id,
            source.reader_id, source.rule_id, source.file_x, source.file_y,
            source.axis_assignment, source.inspected_at, source.nonce_hash,
            source.carry_forward_from]


def snapshot_digest(record):
    """A short identity of the exact revision history shown (revision ids and
    complete material), so a downloaded copy names exactly what it shows."""
    # BOARD-OUTLINE-SOURCE-BINDING-01: a source-free (v1) revision contributes
    # exactly what it always did, so every v1-only digest - and every existing
    # download link - is unchanged byte for byte; a file-linked revision adds its
    # binding, so a different file is a different digest.
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
                    r.material.declaration_version]
                + ([] if r.material is None or r.material.source is None
                   else [_source_digest_item(r.material.source)])]
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


# G1-2 CONSTRAINT-ENGINEERING-LINK-01: what an inventor-linked check revision
# is NOW, read only from the planar owner's own validated snapshot and its own
# binding rule (``clearance_view``). A link names ONE exact revision: it is
# CURRENT only while that revision is still the current revision of an active
# declaration whose every binding holds; a later correction (SUPERSEDED), a
# withdrawal (WITHDRAWN) or a changed component, participation or method
# (NEEDS_RECONFIRMATION) never moves the link to a newer revision. Only a
# CURRENT link carries the check's nominal outcome; nothing here maps it onto
# the inventor's constraint.
LINK_CHECK_CURRENT = STATE_CURRENT
LINK_CHECK_SUPERSEDED = "SUPERSEDED"
LINK_CHECK_WITHDRAWN = STATE_WITHDRAWN
LINK_CHECK_RECONFIRM = STATE_RECONFIRM


def linked_check(snapshot, revision_id, binding):
    """The present state of ONE linked check revision, or ``None`` when the
    snapshot holds no material revision with that id (never guessed)."""
    found = None
    for record in snapshot["ledger"].records:
        for revision in record.revisions:
            if revision.revision_id == revision_id and revision.material is not None:
                found = (record, revision)
    if found is None:
        return None
    record, revision = found
    view = clearance_view(snapshot, record.interface_id, binding)
    if view is None:
        return None
    check = {"interface_id": record.interface_id,
             "interface_description": view["interface_description"],
             "revision_no": revision.revision_no, "outcome": None}
    if record.withdrawn:
        check["status"] = LINK_CHECK_WITHDRAWN
    elif record.current_revision.revision_id != revision_id:
        check["status"] = LINK_CHECK_SUPERSEDED
    elif view["state"] != STATE_CURRENT:
        check["status"] = LINK_CHECK_RECONFIRM
    else:
        check["status"] = LINK_CHECK_CURRENT
        evaluation = view["evaluation"] or {}
        check["outcome"] = evaluation.get("outcome")
    return check


def linkable_checks(snapshot, binding):
    """Every check the inventor may link now: the CURRENT revision of each
    interaction's active declaration whose every binding holds, in interaction
    order."""
    checks = []
    for interface in snapshot["interfaces"]:
        view = clearance_view(snapshot, interface.interface_id, binding)
        if view is None or view["state"] != STATE_CURRENT:
            continue
        checks.append({"revision_id": view["record"]["revision_id"],
                       "interface_id": interface.interface_id,
                       "interface_description": view["interface_description"],
                       "revision_no": view["record"]["head_revision_no"]})
    return checks


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
    model = {
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
    src = m.get("source")
    if src is not None:
        # BOARD-OUTLINE-SOURCE-BINDING-01: only a file-linked (v2) declaration
        # carries this object; a source-free companion is unchanged. The source
        # file's hash is NOT the DXF's hash.
        model["source"] = {
            "kind": src["kind"], "sha256": src["sha256"], "size_bytes": src["size"],
            "format_id": src["format_id"], "reader_id": src["reader_id"],
            "rule_id": src["rule_id"], "axis_assignment": src["axis_assignment"],
            "carried_forward": src["carried_forward"],
            "agreement": src["agreement"], "changed_axes": src["changed_axes"],
            "file_outline_mm": src["file_board"], "declared_board_mm": src["declared_board"],
            "note": ("the file outline was inspected and offered; the comparison uses the "
                     "inventor's declared values; inspection is not verification and the "
                     "file itself is not retained"),
        }
    return model


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
# The opening of the documentary basis note the aid PROPOSES. It is ordinary
# editable inventor text once in the form: nothing ever parses or checks it.
AID_NOTE_PREFIX = {"en": "From my original idea: ", "ar": "من فكرتي الأصلية: "}
_AID_NUMBER = r"[0-9]+(?:\.[0-9]+)?"
# At most three spaces or tabs between the tokens: never a line break (the note
# field is one line) and never a note longer than its 300-character bound.
_AID_PAIR = re.compile(
    r"(?<![\w.,٫/+\-–−٠-٩۰-۹])(?P<a>%s)[ \t]{0,3}[x×X*][ \t]{0,3}(?P<b>%s)[ \t]{0,3}mm(?![\w²³])"
    % (_AID_NUMBER, _AID_NUMBER), re.ASCII)
# Any two numbers joined by a multiplication sign, whatever follows (another
# unit, no unit, other digit systems): a second one makes the idea ambiguous.
_AID_ANY_PAIR = re.compile(r"\d+(?:[.,٫]\d+)?\s*[x×X*]\s*\d", re.UNICODE)
_AID_ANY_NUMBER = re.compile(r"\d+(?:[.,٫]\d+)*", re.UNICODE)
# A sentence ends at ! ? ; ؛ ؟ a line break, or a dot that is not a decimal point.
_AID_SENTENCE_BREAK = re.compile(r"[!?;؛؟\n]|(?<![0-9])\.|\.(?![0-9])")
# The pair must be BOUND to ONE board (singular) by one of a few fixed
# syntactic forms; a board merely mentioned elsewhere in the sentence binds
# nothing ("The board carries a camera that is 80 x 50 mm" abstains). These are
# literal templates, not a parser.
#   before the pair, as the WHOLE start of the sentence: "[the|my|our|this|a|an]
#     [circuit] board / PCB['s] [size|dimensions|outline|footprint]" followed by ":"
#     or "is / are / measures / =" (English), or "مقاس / أبعاد / حجم اللوحة",
#     "اللوحة مقاسها / أبعادها / حجمها", "لوحة بمقاس / بأبعاد / بحجم" or "اللوحة"
#     with an optional ":" (Arabic) - so the board is the subject, never a
#     prepositional or possessive attachment of another object;
#   after the pair: "[circuit] board / PCB" directly ("an 85 x 56 mm board").
# Either way the literal expression must END its sentence (``_AID_SUFFIX``).
_AID_BIND_BEFORE = re.compile(
    r"^[ \t]*(?:"
    r"(?:(?:the|my|our|this|a|an)[ \t]+)?(?:circuit[ \t]+)?(?:board|pcb)"
    r"(?:(?:'s|’s)?[ \t]+(?:size|dimensions|outline|footprint))?"
    r"(?:[ \t]*:|[ \t]+(?:is|are|measures|=))"
    r"|(?:(?:مقاس|مقاسات|أبعاد|ابعاد|حجم)[ \t]+(?:ال)?لوح[ةه]"
    r"|(?:ال)?لوح[ةه][ \t]+(?:مقاسها|مقاساتها|أبعادها|ابعادها|حجمها)"
    r"|(?:ال)?لوح[ةه][ \t]+(?:بمقاس|بمقاسات|بأبعاد|بابعاد|بحجم)"
    r"|(?:ال)?لوح[ةه])[ \t]*:?)"
    r"[ \t]*$", re.IGNORECASE)
# The board word directly after the pair, never the modifier of another noun
# or of a hyphenated word ("a 40 x 40 mm board fan", "a PCB-mounted fan").
_AID_BIND_AFTER = re.compile(r"^[ \t]+(?:circuit[ \t]+)?(?:board|pcb)(?![\w-])", re.IGNORECASE)
# G1-PCC-UNCERTAINTY-BOUNDARY-01: the WHOLE rest of the sentence after the
# pair (or after the board word that follows it) may hold only spaces and at
# most one closing bracket. No comma, conjunction or clause may follow, so a
# trailing qualification ("... mm and it may change", "... mm وممكن تتغير")
# abstains structurally, in any language, without a word list. This is a
# bounded local rule: uncertainty stated in a LATER sentence is not seen.
_AID_SUFFIX = re.compile(r"[ \t]*\)?[ \t]*")
_AID_OTHER_OBJECT = re.compile(
    r"(?<!\w)(?:boards|pcbs|box(?:es)?|case|cases|enclosures?|housings?|lids?|covers?|shell|"
    r"region|area|space|opening|slot|screens?|displays?|batter(?:y|ies)|motors?|holes?|"
    r"panels?|keyboards?|keypads?|sensors?|modules?|chips?|connectors?|cells?|"
    r"spacing|pitch|distance|apart|gap)(?!\w)|"
    r"(?<!\w)[وبلفك]?(?:ال)?(?:صندوق|علبة|علبه|غلاف|حاوية|حاويه|غطاء|منطقة|منطقه|فتحة|فتحه|"
    r"شاشة|شاشه|بطارية|بطاريه|محرك|ثقب|ثقوب|فتحات|مفاتيح|شمسية|شمسيه|حساس|مستشعر|وحدة|"
    r"موصل|خلية|مسافة|مسافه|لوحات)(?!\w)",
    re.IGNORECASE)
# Words that make the sentence hypothetical, approximate, alternative or
# negated. A stop list, not an interpreter: a listed word refuses the aid even
# where it would be harmless, which is the safe direction.
_AID_UNCERTAIN = re.compile(
    r"(?<!\w)(?:maybe|perhaps|might|could|would|should|if|unless|or|either|about|"
    r"around|approx(?:imately)?|roughly|nearly|almost|estimated?|guess(?:ed)?|"
    r"unsure|uncertain|not|never|no|cannot|without|instead|rather|unknown|tbd|"
    # limits, comparisons and targets: a bound is not the board's size
    r"than|less|more|smaller|larger|bigger|wider|narrower|longer|shorter|under|over|"
    r"below|above|up|most|least|max|maximum|min|minimum|limit|between|within|fit|fits|"
    r"must|need|needs|want|wants|target|ideally|"
    # past, belief and change
    r"was|were|used|previous|previously|old|earlier|before|later|now|think|believe|"
    r"probably|likely|seems?|hope|hopefully|planned|plan|change|changed|"
    r"suppose|supposing|supposedly|assume|assuming|say|imagine|originally|initially|"
    r"presumably|theoretically|hypothetically|expect|expected)(?!\w)|"
    r"n't(?!\w)|[~≈±]|"
    r"(?<!\w)[وف]?(?:ربما|قد|لعل|ربّما|إذا|اذا|لو|إن|أو|او|إما|اما|حوالي|حوالى|تقريبا|تقريبًا|"
    r"نحو|قرابة|لا|لن|لم|ليس|ليست|لست|ما|مش|مو|بدون|دون|غير|بدل|بدلا|بدلًا|"
    r"أقل|اقل|أكثر|اكثر|أكبر|اكبر|أصغر|اصغر|حتى|أقصى|اقصى|أدنى|ادنى|حد|بين|ضمن|يجب|ينبغي|"
    r"أريد|اريد|كان|كانت|سابقا|سابقًا|أظن|اظن|أعتقد|اعتقد|يبدو|الآن|الان|"
    r"لنفترض|نفترض|افترض|فرضا|فرضًا|يفترض|مفترض|أتمنى|اتمنى|أرجو|ارجو|تخيل|لنقل)(?!\w)",
    re.IGNORECASE)


def literal_board_pair(original_idea):
    """The ONE literal board-dimension pair of ``original_idea``, or ``None``.

    Returns ``{"passage", "span", "first", "second", "unit"}`` with every text
    copied verbatim from the idea. ``first`` / ``second`` are in the order the
    inventor wrote them; no axis is implied. Refused (``None``) unless ALL hold:
    the idea has exactly one ``A x B`` pair of any kind and it is ``A x B mm``
    in ASCII digits; the pair is bound to one board by a fixed syntactic form
    (``_AID_BIND_BEFORE`` / ``_AID_BIND_AFTER``) and ends its sentence
    (``_AID_SUFFIX``, nothing after it but an optional closing bracket); its
    sentence names no other object and holds no other number and no
    hypothetical, approximate,
    alternative, limiting, past or negating word; and both numbers pass the
    method's strict grammar for a dimension."""
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
    before = original_idea[start:pair.start()]
    after = original_idea[pair.end():end]
    tail = _AID_BIND_AFTER.match(after)
    bound = ((_AID_BIND_BEFORE.search(before) and _AID_SUFFIX.fullmatch(after))
             or (tail and _AID_SUFFIX.fullmatch(after[tail.end():])))
    if not bound or _AID_OTHER_OBJECT.search(sentence):
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
    prefixes = _AID_NOTE_PREFIXES.get(pair.get("source", AID_SOURCE_IDEA)) if pair else None
    if assignment is None or prefixes is None or lang not in prefixes:
        return None
    x, y = assignment
    if lang == "ar":
        body = "«%s»؛ أدخلتُ %s لـ X و%s لـ Y للوحة." % (pair["span"], x, y)
    else:
        body = "“%s”; I entered %s as board X and %s as board Y." % (
            pair["span"], x, y)
    note = prefixes[lang] + body
    # The note field's own bound: a note that would not fit is never proposed,
    # and its quotation is never truncated.
    return note if len(note) <= _sm.MAX_PLANAR_CLEARANCE_TEXT_LENGTH else None


def aid_offer(pair, lang):
    """The display model of the aid for ONE located pair in ``lang``: both
    explicit assignments with their proposed note, none pre-chosen. ``source``
    says where the passage was written (the original idea unless stated)."""
    if pair is None:
        return None
    lang = lang if lang in AID_NOTE_PREFIX else "en"
    orders = [{"order": order, "x": aid_assignment(pair, order)[0],
               "y": aid_assignment(pair, order)[1],
               "note": aid_note(pair, order, lang)}
              for order in AID_ORDERS]
    if any(o["note"] is None for o in orders):
        return None
    return {"passage": pair["passage"], "span": pair["span"], "first": pair["first"],
            "second": pair["second"], "unit": pair["unit"],
            "source": pair.get("source", AID_SOURCE_IDEA), "orders": orders}


# G1-CURRENT-ANSWER-DIMENSION-HANDOFF-01: the same literal aid, read from the
# original idea AND from the inventor's CURRENT answered records. The
# recognizer above is unchanged and runs on each text on its own; nothing here
# reads meaning. A current record is exactly what the existing functional-
# concept view counts as one: not superseded, the inventor's own provenance,
# disposition ``answered``. Provisional assumptions, unknown / deferred /
# specialist and every other non-answer record are never a source. The result
# is a PROPOSAL for the existing form only: it is not stored, binds nothing to
# the saved declaration, and says nothing about which component the numbers
# describe or whether they are right.
AID_SOURCE_IDEA = "idea"
AID_SOURCE_ANSWER = "answer"
AID_ANSWER_NOTE_PREFIX = {"en": "From my recorded answer: ", "ar": "من إجابتي المسجّلة: "}
_AID_NOTE_PREFIXES = {AID_SOURCE_IDEA: AID_NOTE_PREFIX, AID_SOURCE_ANSWER: AID_ANSWER_NOTE_PREFIX}
_AID_ANSWER_PROVENANCE = (_ledger.OWNER_STATED, _ledger.LEGACY_UNSPECIFIED)
_UNSET = object()


def current_answer_texts(records):
    """The verbatim texts of the CURRENT answered inventor records, in ledger
    order. Raises ``ValueError`` on anything that is not a readable record, so
    an unreadable history is never treated as an empty one."""
    if not isinstance(records, (list, tuple)):
        raise ValueError("unreadable answer history")
    texts = []
    for record in records:
        superseded = getattr(record, "superseded_by", _UNSET)
        provenance = getattr(record, "provenance", _UNSET)
        disposition = getattr(record, "disposition", _UNSET)
        content = getattr(record, "content", _UNSET)
        if _UNSET in (superseded, provenance, disposition, content):
            raise ValueError("unreadable answer record")
        if superseded is not None or provenance not in _AID_ANSWER_PROVENANCE \
                or disposition != _ledger.DISPOSITION_ANSWERED:
            continue
        if not isinstance(content, str):
            raise ValueError("unreadable answer text")
        if content.strip():
            texts.append(content)
    return texts


def current_board_pair(original_idea, records):
    """The ONE literal board pair the inventor's current statements give, the
    conflict marker, or ``None``.

    Each text (the original idea, then every current answer) is read on its
    own by the unchanged ``literal_board_pair``. No located pair -> ``None``.
    Located pairs that hold different numbers -> ``{"conflict": True}``: no
    pair is offered and none is chosen. Located pairs that hold the same two
    numbers (in either written order) -> ONE pair, from the original idea when
    it holds one, otherwise from the most recent current answer, with
    ``source`` saying which. Raises on an unreadable history."""
    located = []
    idea_pair = literal_board_pair(original_idea)
    if idea_pair is not None:
        located.append(dict(idea_pair, source=AID_SOURCE_IDEA))
    for text in current_answer_texts(records):
        pair = literal_board_pair(text)
        if pair is not None:
            located.append(dict(pair, source=AID_SOURCE_ANSWER))
    if not located:
        return None
    if len({tuple(sorted((p["first"], p["second"]))) for p in located}) != 1:
        return {"conflict": True}
    return located[0] if idea_pair is not None else located[-1]
