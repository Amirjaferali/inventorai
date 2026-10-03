# -*- coding: utf-8 -*-
"""STAGE 18 — GAP-SCOPED TECHNICAL NEXT-STEP GUIDANCE — CLOSURE (Owner-authorized).

What is pinned: for each of the SIX authorized (trusted domain, exact canonical gap)
pairs — ``mechanical`` and ``electronics_electrical`` x MECHANISM_COMPLETENESS /
PHYSICAL_FEASIBILITY / BOUNDARY_AMBIGUITY — in EXACT state OPEN or PARTIAL, the
report / deliverable and the PDF show the gap's CAP-01 context (the Electronics
MECHANISM_COMPLETENESS / BOUNDARY_AMBIGUITY contexts are new here) plus ONE optional,
all-or-nothing ``next_steps`` sub-view: the information still missing (a summary of
the gap's OWN canonical questions), what to look into plus generic search terms,
class-level measure / check / document categories and an explicit specialist
abstention.

Why a separate test file: the CAP-01 gap-context seam keeps its owners in
``tests/test_cap01_mechanical_open_gap_context.py`` (Mechanical contexts),
``tests/test_cap01_electrical_reference_fundamentals.py`` (Electronics PF context +
fundamentals) and ``tests/test_stage18_cap01_bounded_guidance.py`` (the domain-level
Electronics checklist profile). The closure's sub-view, its traceability table and
the Stage-18 closure truth are proven here, reusing their harness.

Boundaries proven here: exact binding only (no inventor text, answer, keyword,
label, signal or list position); every source anchor resolves to EXISTING governed
pack truth; the canonical questions / Path-N keep owning missing information; no
value, threshold, protocol, pass / fail, material, safety determination, named
standard, laboratory, vendor or specialist category; NeedRouting, CAP-04, the
Validation Plan, the Requirement Landscape, readiness and state are untouched;
EN / AR / PDF render with LTR-isolated search terms; the Stage-18 closure truth.
"""
import hashlib
import inspect
import io
import json
import os
import pickle
import re

import pytest

import web.app as appmod
from engine.deliverable_assembler import assemble_deliverable
from engine.derived_readiness import derive_readiness
from engine.gap_action_pack import derive_gap_action_packs
from engine.idea_state import (
    ACCEPTED_RISK, BOUNDARY_AMBIGUITY, CLOSED, IdeaState, MECHANISM_COMPLETENESS, OPEN,
    PARTIAL, PHYSICAL_FEASIBILITY)
from engine.path_n_questions import get_served_question, routing_policies
from engine.requirement_landscape import derive_requirement_landscape
from engine.validation_plan import derive_validation_plan
from web import cap01_guidance, ui_text
from tests.test_safe_question_routing_pf_q2 import (  # noqa: F401  (fixture)
    client, ELEC_SEED, _start, _live,
)
from tests.test_cap01_mechanical_open_gap_context import (
    _gaps, _pdf_source, _render, _report, _visible)

_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
_PACK_PATHS = {d: os.path.join(_ROOT, "domains", d, "domain.json")
               for d in ("mechanical", "electronics_electrical")}
_PROVENANCE_PATH = os.path.join(_ROOT, "domains", "domain_provenance.json")
_DOCS = os.path.join(_ROOT, "docs", "governance")

MECH = "mechanical"
ELEC = "electronics_electrical"
DOMAINS = (MECH, ELEC)
GAPS = (MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY)
PAIRS = tuple((d, g) for d in DOMAINS for g in GAPS)
CONTEXT_GROUPS = {MECH: "CAP01_MECHANICAL_GAP_CONTEXT_V1", ELEC: "CAP01_ELECTRONICS_GAP_CONTEXT_V1"}
NEXT_GROUPS = {MECH: "CAP01_MECHANICAL_NEXT_STEPS_V1", ELEC: "CAP01_ELECTRONICS_NEXT_STEPS_V1"}
LABEL_PREFIX = "UI_CAP01_NEXT_STEPS_V1_"
NEXT_PREFIXES = (LABEL_PREFIX,) + tuple("UI_%s_" % g for g in NEXT_GROUPS.values())
ANCHOR_KINDS = ("question", "rule", "coverage", "fundamental", "routing")
MECH_PF_ROUTE = "mechanical-path-n-routing-v1:PHYSICAL_FEASIBILITY:Q2"

# Digests of copy that existed BEFORE this closure (computed at base
# 4a082673ec5d8051151c9ea7a1c2ee7168d541ff), as a sorted-key JSON dict of
# key -> {"en", "ar"}: the domain-level Electronics checklist / research profile,
# the Mechanical gap contexts + fundamentals and the Electronics PF context +
# fundamentals. The closure changes none of them.
_INTERFACE_COPY_DIGEST = (19, "cb273c6a31634b1b49bd738cee150b6c5e68a63bc238e46a794cc40222dc9eae")
_MECH_CONTEXT_COPY_DIGEST = (31, "3e9d058eca28506e8520ac411ba587195ceccccce788a74f0c4e905cf811274a")
_ELEC_PF_COPY_DIGEST = (19, "754be3162f259ff61bc95feee2700c0d52afc3223c52eec1d908300a943c09f0")
# The canonical questions each MISSING summary was written against, as a JSON list
# of [question_id, text]. A change to a governed question must re-review its summary.
_QUESTION_DIGESTS = {
    (MECH, MECHANISM_COMPLETENESS): "1d4c8cf34e41341663d9c91f80b936614a28b49ede37fbea2478c53cf736531b",
    (MECH, PHYSICAL_FEASIBILITY): "87399cee07d6eeef24d123b0d3fa0c797186ccd74951b999f7cee79c50473d7c",
    (MECH, BOUNDARY_AMBIGUITY): "9149d4fe81cfc1409f0ed9b075806bd1f31e91b14c6863282c334c18187d9e07",
    (ELEC, MECHANISM_COMPLETENESS): "4d0c925e12f04937ebc1cca49657073dd4cd7d7d216064448ecdd27d17b811d6",
    (ELEC, PHYSICAL_FEASIBILITY): "0d4bb922cc019ffda2162d3049f7477be2463e7332ccb61eda5b9a37a9c32682",
    (ELEC, BOUNDARY_AMBIGUITY): "f99de135ee3be9482494b90a19ff26f207bba77458d31c9f01fcb6be4206f574",
}


# ==========================================================================
# harness
# ==========================================================================
def _pack(domain):
    with io.open(_PACK_PATHS[domain], encoding="utf-8") as fh:
        return json.load(fh)


def _mapping(domain, gap):
    [m] = [m for m in _pack(domain)["gap_type_mappings"] if m["gap_type_id"] == gap]
    return m


def _state(domain, *pairs, idea_text=None):
    s = IdeaState(idea_id="s18-next-steps-probe")
    s.domain = domain
    s.domain_signal = domain
    s.gaps = _gaps(*pairs)
    if idea_text is not None:
        s.idea_text = idea_text
    return s


def _resolve(domain, *pairs):
    return cap01_guidance.gap_contexts_for_gaps(domain, _gaps(*pairs))


def _next(domain, gap):
    return cap01_guidance.gap_context_copy(domain, gap)["next_steps"]


def _render_state(domain, *pairs, lang="en", pdf=False, idea_text=None):
    state = _state(domain, *pairs, idea_text=idea_text)
    return _render(assemble_deliverable(state), state, lang=lang, pdf=pdf)


_NS_RE = re.compile(
    r'<div class="cap01-next-steps" data-cap01-next-steps="([^"]+)">(.*?)\n      </div>', re.S)
_CTX_GAP_RE = re.compile(r'<div class="cap01-gap-context" data-cap01-gap="([^"]+)" '
                         r'data-cap01-gap-state="([^"]+)">')


def _ns_blocks(html):
    return _NS_RE.findall(html)


def _keys(view):
    """Every copy key of one next-steps view (labels, single parts, list lines)."""
    keys = [v for k, v in view.items() if k.endswith("_key")]
    for name in ("topic_keys", "search_keys", "measure_keys"):
        keys.extend(view[name])
    return keys


def _all_next_keys():
    return sorted(k for k in ui_text.UI_STRINGS if k.startswith(NEXT_PREFIXES))


def _per_gap_keys(domain, gap):
    stem = "UI_%s_%s_" % (NEXT_GROUPS[domain], gap)
    return sorted(k for k in ui_text.UI_STRINGS if k.startswith(stem))


def _text(key, lang):
    return ui_text.UI_STRINGS[key][lang]


def _set_gaps(sid, *pairs):
    _live(sid).gaps = _gaps(*pairs)


def _sentences(text):
    return [s for s in re.split(r"(?<=[.؛:—])\s+", text) if s.strip()]


def _copy_digest(pred):
    sel = {k: ui_text.UI_STRINGS[k] for k in sorted(ui_text.UI_STRINGS) if pred(k)}
    return len(sel), hashlib.sha256(
        json.dumps(sel, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def _doc(name):
    with io.open(os.path.join(_DOCS, name), encoding="utf-8") as fh:
        return fh.read()


# ==========================================================================
# N1. exact binding: six pairs, OPEN / PARTIAL only, no duplicates
# ==========================================================================
def test_n01_the_table_is_exactly_the_six_authorized_pairs():
    assert tuple(cap01_guidance.CAP01_GAP_NEXT_STEPS) == PAIRS
    for (domain, gap), (group_id, anchors) in cap01_guidance.CAP01_GAP_NEXT_STEPS.items():
        assert group_id == NEXT_GROUPS[domain]
        assert gap in cap01_guidance.CAP01_GAP_CONTEXT_BY_DOMAIN[domain][1]
        assert anchors and all(kind in ANCHOR_KINDS for kind, _ in anchors)
    for domain in DOMAINS:
        assert cap01_guidance.CAP01_GAP_CONTEXT_BY_DOMAIN[domain] == (CONTEXT_GROUPS[domain], GAPS)


@pytest.mark.parametrize("status", (OPEN, PARTIAL))
@pytest.mark.parametrize("domain,gap", PAIRS)
def test_n02_open_or_partial_renders_its_context_and_next_steps_exactly_once(domain, gap, status):
    view = _resolve(domain, (gap, status))
    assert view["group_id"] == CONTEXT_GROUPS[domain]
    [ctx] = view["contexts"]
    assert (ctx["gap_type"], ctx["gap_state"]) == (gap, status)
    assert ctx["next_steps"]["group_id"] == NEXT_GROUPS[domain]
    html = _render_state(domain, (gap, status))
    blocks = _ns_blocks(html)
    assert [g for g, _ in blocks] == [NEXT_GROUPS[domain].lower().replace("_", "-")]
    assert _CTX_GAP_RE.findall(html) == [(gap.lower().replace("_", "-"), status.lower())]


@pytest.mark.parametrize("status", (CLOSED, ACCEPTED_RISK, "open", "Partial", "PARTIALLY", "",
                                    "UNKNOWN", None))
@pytest.mark.parametrize("domain,gap", PAIRS)
def test_n03_closed_accepted_risk_and_unknown_states_render_nothing(domain, gap, status):
    assert _resolve(domain, (gap, status)) is None
    html = _render_state(domain, (gap, status))
    assert "cap01-next-steps" not in html and "cap01-gap-block" not in html


@pytest.mark.parametrize("domain,gap", PAIRS)
def test_n04_an_absent_gap_renders_no_next_steps_for_it(domain, gap):
    others = [(g, OPEN) for g in GAPS if g != gap]
    view = _resolve(domain, *others)
    assert gap not in [c["gap_type"] for c in view["contexts"]]
    html = _render_state(domain, *others)
    assert gap.lower().replace("_", "-") not in [g for g, _ in _CTX_GAP_RE.findall(html)]
    assert len(_ns_blocks(html)) == 2
    assert _resolve(domain) is None and "cap01-next-steps" not in _render_state(domain)


@pytest.mark.parametrize("domain", DOMAINS)
def test_n05_duplicates_and_state_order_never_add_or_reorder_next_steps(domain):
    pairs = [(BOUNDARY_AMBIGUITY, OPEN), (MECHANISM_COMPLETENESS, PARTIAL),
             (BOUNDARY_AMBIGUITY, OPEN), (PHYSICAL_FEASIBILITY, OPEN),
             (MECHANISM_COMPLETENESS, CLOSED)]
    view = _resolve(domain, *pairs)
    # first record per id wins (the canonical accessor); source order, not state order
    assert [(c["gap_type"], c["gap_state"]) for c in view["contexts"]] == [
        (MECHANISM_COMPLETENESS, PARTIAL), (PHYSICAL_FEASIBILITY, OPEN), (BOUNDARY_AMBIGUITY, OPEN)]
    html = _render_state(domain, *pairs)
    assert len(_ns_blocks(html)) == 3
    assert html.count('data-cap01-next-steps="') == 3


@pytest.mark.parametrize("domain", ("Mechanical", "MECHANICAL", "electronics", "Electronics_Electrical",
                                    "iot_electronics", "software", "medical_device", "", None, 3))
def test_n06_near_domain_strings_and_other_domains_never_bind(domain):
    assert cap01_guidance.gap_contexts_for_gaps(domain, _gaps(*[(g, OPEN) for g in GAPS])) is None
    assert all(cap01_guidance.CAP01_GAP_NEXT_STEPS.get((domain, g)) is None for g in GAPS)


@pytest.mark.parametrize("domain", DOMAINS)
def test_n07_labels_question_ids_signals_and_inventor_text_never_select(domain):
    pack = _pack(domain)
    impostors = [m["domain_label"] for m in pack["gap_type_mappings"]]
    impostors += [q["question_id"] for m in pack["gap_type_mappings"] for q in m["questions"]]
    impostors += [g.lower() for g in GAPS] + [g + " " for g in GAPS] + [g.replace("_", " ") for g in GAPS]
    assert cap01_guidance.gap_contexts_for_gaps(domain, _gaps(*[(i, OPEN) for i in impostors])) is None
    words = " ".join([s["signal"] for s in pack["classification_signals"] + pack["substance_signals"]]
                     + impostors)
    # every gap closed + every signal / label / question in the inventor text -> nothing
    html = _render_state(domain, *[(g, CLOSED) for g in GAPS], idea_text=words)
    assert "cap01-next-steps" not in html
    # the same bounded set renders regardless of project content
    a = _ns_blocks(_render_state(domain, (PHYSICAL_FEASIBILITY, OPEN), idea_text="a plain gadget"))
    b = _ns_blocks(_render_state(domain, (PHYSICAL_FEASIBILITY, PARTIAL), idea_text=words))
    assert a == b and len(a) == 1


def test_n08_the_resolver_reads_no_inventor_text_answer_label_or_signal():
    src = inspect.getsource(cap01_guidance._next_steps)
    for forbidden in ("idea_text", "answer", "signal", "keyword", "label(", "domain_label",
                      "question_text", "[0]", "eval(", "float(", "int(", "calculate", "infer"):
        assert forbidden not in src, forbidden
    # the table and resolver live in the existing CAP-01 owner; no new engine / route / seam
    for name in ("CAP01_GAP_NEXT_STEPS", "_next_steps"):
        assert hasattr(cap01_guidance, name)
    assert not [p for p in os.listdir(os.path.join(_ROOT, "engine")) if "next_step_guidance" in p]


@pytest.mark.parametrize("missing", ("SPECIALIST", "MISSING", "TOPIC_1", "SEARCH_1", "MEASURE_1"))
@pytest.mark.parametrize("domain,gap", PAIRS)
def test_n09_incomplete_copy_fails_closed_without_removing_the_context(monkeypatch, domain, gap, missing):
    monkeypatch.delitem(ui_text.UI_STRINGS, "UI_%s_%s_%s" % (NEXT_GROUPS[domain], gap, missing))
    copy_view = cap01_guidance.gap_context_copy(domain, gap)
    assert copy_view is not None and copy_view["next_steps"] is None
    html = _render_state(domain, (gap, OPEN))
    assert "cap01-gap-block" in html and "cap01-next-steps" not in html


@pytest.mark.parametrize("label", ("TITLE", "MISSING_LABEL", "LOOK_LABEL", "SEARCH_LABEL",
                                   "MEASURE_LABEL", "SPECIALIST_LABEL", "BOUNDARY"))
def test_n10_a_missing_shared_label_removes_every_next_steps_sub_view(monkeypatch, label):
    monkeypatch.delitem(ui_text.UI_STRINGS, LABEL_PREFIX + label)
    assert all(_next(d, g) is None for d, g in PAIRS)
    assert all(cap01_guidance.gap_context_copy(d, g) is not None for d, g in PAIRS)


def test_n11_every_next_steps_key_is_consumed_by_exactly_one_resolved_view():
    used = set()
    for domain, gap in PAIRS:
        used |= set(_keys(_next(domain, gap)))
    assert used == set(_all_next_keys())
    for domain, gap in PAIRS:
        view = _next(domain, gap)
        assert set(_keys(view)) - {k for k in _keys(view) if k.startswith(LABEL_PREFIX)} == set(
            _per_gap_keys(domain, gap))


# ==========================================================================
# N2. Electronics context completion
# ==========================================================================
def test_n20_electronics_now_carries_all_three_governed_gaps_in_pack_order():
    pack = _pack(ELEC)
    assert tuple(m["gap_type_id"] for m in pack["gap_type_mappings"]) == GAPS
    view = _resolve(ELEC, *[(g, OPEN) for g in GAPS])
    assert [c["gap_type"] for c in view["contexts"]] == list(GAPS)
    assert [c["gap_type"] for c in view["contexts"] if c["fundamentals"]] == [PHYSICAL_FEASIBILITY]
    for lang in ("en", "ar"):
        for gap in (MECHANISM_COMPLETENESS, BOUNDARY_AMBIGUITY):
            for part in ("TITLE", "MEANING", "LIMIT"):
                assert _text("UI_%s_%s_%s" % (CONTEXT_GROUPS[ELEC], gap, part), lang).strip()
    assert _text("UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_TITLE", "en") == (
        "Technical context for the unresolved electrical / electronics gaps")
    assert _text("UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_TITLE", "ar") == (
        "سياق فني للفجوات الكهربائية / الإلكترونية غير المحسومة")


def test_n21_electronics_mc_and_ba_contexts_restate_only_their_governed_questions():
    mc = "UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_MECHANISM_COMPLETENESS_"
    ba = "UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_BOUNDARY_AMBIGUITY_"
    for phrase in ("from input to output", "signal or energy transformation", "the role each plays"):
        assert phrase in _text(mc + "MEANING", "en"), phrase
    for phrase in ("does not do or handle", "another system or component begins",
                   "external systems, components or interfaces"):
        assert phrase in _text(ba + "MEANING", "en"), phrase
    for phrase in ("المدخل إلى المخرج", "تحويل الإشارة أو الطاقة", "ودور كل منها"):
        assert phrase in _text(mc + "MEANING", "ar"), phrase
    for phrase in ("لا يتعامل معه", "ويبدأ نظام أو مكوّن آخر", "الواجهات الخارجية"):
        assert phrase in _text(ba + "MEANING", "ar"), phrase
    for stem in (mc, ba):
        assert _text(stem + "LIMIT", "en").startswith("InventorAI does not conclude")
        assert _text(stem + "LIMIT", "ar").startswith("لا يستنتج InventorAI")
        assert "(Mechanism Completeness)" in _text(mc + "TITLE", "ar")
        assert "(Boundary Ambiguity)" in _text(ba + "TITLE", "ar")


def test_n22_the_electronics_interface_profile_is_unchanged_and_not_broadened():
    assert cap01_guidance.CAP01_PROFILE_BY_DOMAIN == {ELEC: "CAP01_ELECTRONICS_INTERFACE_V1"}
    assert _copy_digest(lambda k: "CAP01_ELECTRONICS_INTERFACE_V1" in k) == _INTERFACE_COPY_DIGEST
    assert cap01_guidance.profile_copy(MECH) is None          # no Mechanical copy of the profile
    assert not [k for k in ui_text.UI_STRINGS if k.startswith("UI_CAP01_MECHANICAL_INTERFACE")]


def test_n23_existing_contexts_and_reference_fundamentals_copy_are_unchanged():
    assert _copy_digest(lambda k: k.startswith("UI_CAP01_MECHANICAL_GAP_CONTEXT_V1_")) == \
        _MECH_CONTEXT_COPY_DIGEST
    assert _copy_digest(
        lambda k: k.startswith("UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_")) == \
        _ELEC_PF_COPY_DIGEST
    assert tuple(cap01_guidance.CAP01_GAP_FUNDAMENTALS) == (
        (MECH, PHYSICAL_FEASIBILITY), (ELEC, PHYSICAL_FEASIBILITY))
    assert cap01_guidance.CAP01_GAP_FUNDAMENTALS[(MECH, PHYSICAL_FEASIBILITY)][0] == "force_moment_pressure_v1"
    assert cap01_guidance.CAP01_GAP_FUNDAMENTALS[(ELEC, PHYSICAL_FEASIBILITY)][0] == \
        "basic_electrical_reference_v1"


# ==========================================================================
# N3. research guidance and measure / check / document categories
# ==========================================================================
@pytest.mark.parametrize("domain,gap", PAIRS)
def test_n30_every_pair_has_bounded_topics_search_terms_and_categories(domain, gap):
    view = _next(domain, gap)
    for name in ("topic_keys", "search_keys", "measure_keys"):
        assert 3 <= len(view[name]) <= 6, name
        for lang in ("en", "ar"):
            texts = [_text(k, lang) for k in view[name]]
            assert all(t.strip() for t in texts) and len(set(texts)) == len(texts)


_CATEGORY_NOUNS = ("description", "record", "note", "statement", "documentation", "quantities",
                   "sketch", "evidence", "information", "diagram")


@pytest.mark.parametrize("domain,gap", PAIRS)
def test_n31_measure_lines_are_class_level_documentation_categories(domain, gap):
    for key in _next(domain, gap)["measure_keys"]:
        text = _text(key, "en")
        assert any(n in text.lower() for n in _CATEGORY_NOUNS), text
        assert not re.search(r"\d", text)


@pytest.mark.parametrize("domain,gap", PAIRS)
def test_n32_search_terms_are_language_neutral_generic_and_ltr_isolated(domain, gap):
    keys = _next(domain, gap)["search_keys"]
    for key in keys:
        en, ar = _text(key, "en"), _text(key, "ar")
        assert en == ar == en.strip()
        assert re.fullmatch(r"[A-Za-z' ]+", en), en
        assert len(en.split()) <= 5
    for lang in ("en", "ar"):
        [(_, body)] = _ns_blocks(_render_state(domain, (gap, OPEN), lang=lang))
        for key in keys:
            assert ('data-cap01-next-search-term><bdi dir="ltr">%s</bdi>' %
                    _text(key, lang).replace("'", "&#39;")) in body, (lang, key)


# Forbidden in EVERY next-steps line (per-gap parts and shared labels). The shared
# BOUNDARY line is the one place that DENIES some of these (checked separately).
_FORBIDDEN_EN = (
    "threshold", "pass / fail", "pass/fail", "protocol", "procedure", "tolerance", "safety factor",
    "maximum", "minimum", "rated", "rating", "specification", "thickness", "gauge", "alloy",
    "steel", "aluminium", "aluminum", "copper", "plastic", "polymer", "is safe", "unsafe",
    "safe to", "hazard", "certif", "complian", "approved", "engineer", "electrician",
    "technician", "consultant", "physicist", "expert", "laboratory", "lab", "vendor",
    "supplier", "manufacturer", "datasheet", "data sheet", "Arduino", "ESP32", "Raspberry",
    "calculat", "compute", "sizing", "you should", "you must", "we recommend", "recommended",
    "best", "optimal")
_FORBIDDEN_ACRONYMS = ("ISO", "IEC", "IEEE", "IPC", "ASME", "ASTM", "ANSI", "DIN", "UL", "CE",
                       "FCC", "NIST", "DOE", "NASA", "SAE", "MIL", "EN")
_FORBIDDEN_AR = ("مهندس", "استشاري", "خبير", "مختبر", "مورّد", "مورد", "الشركة المصنعة",
                 "شهادة", "الامتثال", "عتبة", "بروتوكول", "سماكة", "فولاذ", "ألمنيوم", "نحاس",
                 "آمن", "نوصي", "يجب عليك", "عليك أن", "احسب")
_FORBIDDEN_SYMBOLS = ("=", "×", "≤", "≥", "<", ">", "%", "°", "Ω", "N·m", "kPa", "±", "?", "؟")


def _next_lines(lang, include_boundary=False):
    for key in _all_next_keys():
        if key == LABEL_PREFIX + "BOUNDARY" and not include_boundary:
            continue
        yield key, _text(key, lang)


def test_n33_no_value_threshold_protocol_material_safety_standard_lab_vendor_or_specialist():
    for key, text in _next_lines("en"):
        assert not re.search(r"[0-9٠-٩]", text), (key, text)
        for term in _FORBIDDEN_EN:
            # word-start bounded ("operating" is not "rating"); "lab" also word-end
            tail = r"(?!\w)" if term in ("lab", "best") else ""
            assert not re.search(r"(?<!\w)%s%s" % (re.escape(term), tail), text, re.I), (key, term)
        for acro in _FORBIDDEN_ACRONYMS:
            assert not re.search(r"(?<![A-Za-z])%s(?![A-Za-z])" % acro, text), (key, acro)
        for sym in _FORBIDDEN_SYMBOLS:
            assert sym not in text, (key, sym)
    for key, text in _next_lines("ar"):
        assert not re.search(r"[0-9٠-٩]", text), (key, text)
        for term in _FORBIDDEN_AR:
            assert term not in text, (key, term)
        for sym in _FORBIDDEN_SYMBOLS:
            assert sym not in text, (key, sym)


def test_n34_the_boundary_line_only_ever_denies_values_criteria_and_test_planning():
    en = _text(LABEL_PREFIX + "BOUNDARY", "en")
    ar = _text(LABEL_PREFIX + "BOUNDARY", "ar")
    for phrase in ("has not determined that any topic or category applies to your design",
                   "retrieves nothing", "sets no value, range, threshold or pass / fail criterion",
                   "add no question, action, responsibility or closure rule",
                   "do not plan a test", "Prototype & Test Plan", "Validation Plan"):
        assert phrase in en, phrase
    for phrase in ("لم يحدد InventorAI أن أي موضوع أو فئة ينطبق على تصميمك", "ولا يسترجع أي شيء",
                   "ولا يضع أي قيمة أو نطاق أو حدّ أو معيار نجاح / فشل",
                   "ولا تضيف سؤالًا ولا إجراءً ولا مسؤولية ولا شرط إغلاق", "ولا تخطط لاختبار",
                   "خطة النموذج الأولي والاختبار", "(Validation Plan)"):
        assert phrase in ar, phrase
    for sentence in _sentences(en):
        for term in ("threshold", "pass / fail", "plan a test", "question, action"):
            if term in sentence:
                assert re.search(r"\b(no|not|nothing)\b", sentence), (term, sentence)
    assert not re.search(r"\d", en + ar)


# ==========================================================================
# N4. missing-information ownership stays with the canonical questions / Path-N
# ==========================================================================
@pytest.mark.parametrize("domain,gap", PAIRS)
def test_n40_each_gap_keeps_exactly_its_canonical_questions(domain, gap):
    questions = _mapping(domain, gap)["questions"]
    qs = [[q["question_id"], q["text"]] for q in questions]
    assert hashlib.sha256(json.dumps(qs, ensure_ascii=False).encode("utf-8")).hexdigest() == \
        _QUESTION_DIGESTS[(domain, gap)]
    anchored = [ref for kind, ref in cap01_guidance.CAP01_GAP_NEXT_STEPS[(domain, gap)][1]
                if kind == "question"]
    # the MISSING summary covers every canonical question of that gap, in order, and no other
    assert anchored == [q["question_id"] for q in questions]


@pytest.mark.parametrize("domain,gap", PAIRS)
def test_n41_path_n_still_serves_the_gap_and_the_summary_asks_nothing_new(domain, gap):
    served = get_served_question(gap, 0, domain=domain)
    assert served is not None and served.design_gap_id == gap
    view = _next(domain, gap)
    assert _text(view["missing_key"], "en").startswith("The questions for this gap ask")
    assert _text(view["missing_key"], "ar").startswith("تسأل أسئلة هذه الفجوة")
    [(_, body)] = _ns_blocks(_render_state(domain, (gap, OPEN)))
    for control in ("<input", "<form", "<select", "<textarea", "<button", "<a "):
        assert control not in body, control


def test_n42_no_engine_progression_or_question_owner_reads_the_sub_view():
    for name in sorted(os.listdir(os.path.join(_ROOT, "engine"))):
        if name.endswith(".py"):
            with io.open(os.path.join(_ROOT, "engine", name), encoding="utf-8") as fh:
                src = fh.read()
            assert "cap01" not in src.lower() and "NEXT_STEPS_V1" not in src, name


# ==========================================================================
# N5. specialist abstention; NeedRouting untouched
# ==========================================================================
_ABSTAIN_EN = ("InventorAI does not name a specialist category for this gap: no governed mapping "
               "supports one from this guidance alone.")
_ABSTAIN_AR = "لا يسمّي InventorAI فئة مختصين لهذه الفجوة"


@pytest.mark.parametrize("domain,gap", PAIRS)
def test_n50_every_pair_explicitly_abstains_from_naming_a_specialist(domain, gap):
    view = _next(domain, gap)
    en, ar = _text(view["specialist_key"], "en"), _text(view["specialist_key"], "ar")
    assert en.startswith(_ABSTAIN_EN) and ar.startswith(_ABSTAIN_AR)
    if (domain, gap) == (MECH, PHYSICAL_FEASIBILITY):
        assert "If specialist input has already been requested" in en
        assert "does not change it or identify which specialist" in en
        assert "ولا يغيّره هذا الإرشاد ولا يحدد المختص" in ar
    else:
        assert en == _ABSTAIN_EN
        assert "requested" not in en and "طُلبت" not in ar


def test_n51_the_mechanical_pf_routing_fact_is_the_committed_policy_unchanged():
    policies = routing_policies(MECH)
    assert [(g, q, p.policy_ref, p.required_input) for g, q, p in policies] == [
        (PHYSICAL_FEASIBILITY, "mechanical:PHYSICAL_FEASIBILITY:Q2", MECH_PF_ROUTE, "SPECIALIST")]
    assert routing_policies(ELEC) == ()
    routing = [ref for d_g, (_, anchors) in cap01_guidance.CAP01_GAP_NEXT_STEPS.items()
               for kind, ref in anchors if kind == "routing"]
    assert routing == [MECH_PF_ROUTE]


def test_n52_rendering_changes_no_need_routing_state_or_store(client, monkeypatch):
    sid = _start(client)
    state = _live(sid)
    assert state.domain == MECH
    _set_gaps(sid, *[(g, OPEN) for g in GAPS])
    state = _live(sid)
    store = appmod._get_store()
    before_routes = pickle.dumps(store.load_need_routing(sid))
    before_state = pickle.dumps(state)
    before = [pickle.dumps(f(state)) for f in (derive_gap_action_packs, derive_validation_plan,
                                                derive_requirement_landscape)]
    readiness = derive_readiness(state)
    before_ready = (readiness.overall_verified(), readiness.unverified_contexts())
    for lang in ("en", "ar"):
        assert len(_ns_blocks(_report(client, sid, lang=lang))) == 3
        _pdf_source(client, sid, monkeypatch)
    state = _live(sid)
    assert pickle.dumps(store.load_need_routing(sid)) == before_routes
    assert pickle.dumps(state) == before_state
    assert [pickle.dumps(f(state)) for f in (derive_gap_action_packs, derive_validation_plan,
                                             derive_requirement_landscape)] == before
    readiness = derive_readiness(state)
    assert (readiness.overall_verified(), readiness.unverified_contexts()) == before_ready


# ==========================================================================
# N6. source traceability: every anchor names EXISTING governed truth
# ==========================================================================
def _resolve_coverage(pack, path):
    declaration, field, index = path.split(".")
    value = pack[declaration][field][int(index)]
    assert isinstance(value, str) and value.strip()
    return value


@pytest.mark.parametrize("domain,gap", PAIRS)
def test_n60_every_anchor_resolves_in_the_governed_pack(domain, gap):
    pack = _pack(domain)
    _, anchors = cap01_guidance.CAP01_GAP_NEXT_STEPS[(domain, gap)]
    gap_questions = {q["question_id"] for q in _mapping(domain, gap)["questions"]}
    rules = {r["rule_id"]: r for r in pack["rule_nuances"]}
    claims = {c["claim_id"]: c for grp in pack["reference_fundamentals"] for c in grp["claims"]}
    policies = {p.policy_ref: (g, q) for g, q, p in routing_policies(domain)}
    assert [k for k, _ in anchors].count("question") >= 1
    assert len(set(anchors)) == len(anchors)
    for kind, ref in anchors:
        if kind == "question":
            assert ref in gap_questions, ref
        elif kind == "rule":
            assert ref in rules and ref.startswith(domain + ":"), ref
            if rules[ref]["modifier_type"] == "active_gap_rule_marker":
                assert rules[ref]["modifier_value"] == gap, ref
        elif kind == "coverage":
            _resolve_coverage(pack, ref)
        elif kind == "fundamental":
            assert claims[ref]["applicable_gap_type"] == gap, ref
        elif kind == "routing":
            g, q = policies[ref]
            assert g == gap and q in gap_questions, ref
        else:  # pragma: no cover - the closed kind set
            raise AssertionError(kind)


def test_n61_fundamental_anchors_are_exactly_the_reference_only_sets_and_unrendered():
    for domain in DOMAINS:
        anchored = [ref for kind, ref in cap01_guidance.CAP01_GAP_NEXT_STEPS[(domain, PHYSICAL_FEASIBILITY)][1]
                    if kind == "fundamental"]
        assert tuple(anchored) == cap01_guidance.CAP01_GAP_FUNDAMENTALS[(domain, PHYSICAL_FEASIBILITY)][1]
    for domain, gap in PAIRS:
        html = _render_state(domain, (gap, OPEN))
        for _, ref in cap01_guidance.CAP01_GAP_NEXT_STEPS[(domain, gap)][1]:
            assert ref not in html, ref


def test_n62_the_packs_and_provenance_carry_nothing_of_this_closure():
    with io.open(_PROVENANCE_PATH, encoding="utf-8") as fh:
        provenance = fh.read()
    for domain in DOMAINS:
        with io.open(_PACK_PATHS[domain], encoding="utf-8") as fh:
            raw = fh.read()
        assert "NEXT_STEPS" not in raw and "next_steps" not in raw
    assert "NEXT_STEPS" not in provenance and "next_steps" not in provenance


# ==========================================================================
# N7. non-interference: additive only
# ==========================================================================
@pytest.mark.parametrize("lang", ("en", "ar"))
@pytest.mark.parametrize("domain", DOMAINS)
def test_n70_removing_the_sub_view_leaves_the_rest_of_the_report_byte_identical(monkeypatch, domain, lang):
    state = _state(domain, (MECHANISM_COMPLETENESS, OPEN), (PHYSICAL_FEASIBILITY, PARTIAL),
                   (BOUNDARY_AMBIGUITY, OPEN))
    package = assemble_deliverable(state)
    csrf = re.compile(r'name="csrf_token" value="[^"]*"')
    with_steps = csrf.sub("", _render(package, state, lang=lang))
    assert len(_ns_blocks(with_steps)) == 3
    monkeypatch.setattr(cap01_guidance, "CAP01_GAP_NEXT_STEPS", {})
    without = csrf.sub("", _render(package, state, lang=lang))
    stripped = re.sub(r'\n      <div class="cap01-next-steps".*?\n      </div>', "", with_steps, flags=re.S)
    assert stripped == without


def test_n71_the_session_page_carries_no_next_steps(client):
    sid = _start(client)
    _set_gaps(sid, *[(g, OPEN) for g in GAPS])
    for lang in ("en", "ar"):
        if lang == "ar":
            client.post("/ui-language", data={"lang": "ar"})
        page = client.get(f"/session/{sid}").get_data(as_text=True)
        assert "cap01-next-steps" not in page
        assert _text(LABEL_PREFIX + "TITLE", lang) not in page
    with io.open(os.path.join(_ROOT, "web", "templates", "session.html"), encoding="utf-8") as fh:
        assert "next_steps" not in fh.read()


# ==========================================================================
# N8. EN / AR / PDF rendering
# ==========================================================================
def _visible_texts(domain, gap, lang):
    return [_text(k, lang) for k in _keys(_next(domain, gap))]


@pytest.mark.parametrize("domain,seed", ((MECH, None), (ELEC, ELEC_SEED)))
def test_n80_en_report_route_renders_every_english_line_and_no_arabic(client, domain, seed):
    sid = _start(client) if seed is None else _start(client, seed=seed, domain=domain)
    _set_gaps(sid, (MECHANISM_COMPLETENESS, OPEN), (PHYSICAL_FEASIBILITY, PARTIAL),
              (BOUNDARY_AMBIGUITY, OPEN))
    page = _report(client, sid)
    assert len(_ns_blocks(page)) == 3
    visible = _visible(page)
    for gap in GAPS:
        for text in _visible_texts(domain, gap, "en"):
            assert text in visible, text
        view = _next(domain, gap)
        for key in _keys(view):
            if key not in view["search_keys"]:
                assert _text(key, "ar") not in visible, key
    assert "UI_CAP01_" not in visible


@pytest.mark.parametrize("domain,seed", ((MECH, None), (ELEC, ELEC_SEED)))
def test_n81_ar_rtl_report_route_renders_arabic_with_ltr_search_terms(client, domain, seed):
    sid = _start(client) if seed is None else _start(client, seed=seed, domain=domain)
    _set_gaps(sid, (MECHANISM_COMPLETENESS, PARTIAL), (PHYSICAL_FEASIBILITY, OPEN),
              (BOUNDARY_AMBIGUITY, PARTIAL))
    page = _report(client, sid, lang="ar")
    assert 'dir="rtl"' in page
    blocks = _ns_blocks(page)
    assert len(blocks) == 3
    visible = _visible(page)
    for gap in GAPS:
        view = _next(domain, gap)
        for text in _visible_texts(domain, gap, "ar"):
            assert text in visible, text
        for key in _keys(view):
            if key not in view["search_keys"]:
                assert _text(key, "en") not in visible, key
    search_total = sum(len(_next(domain, g)["search_keys"]) for g in GAPS)
    assert sum(body.count('<bdi dir="ltr">') for _, body in blocks) == search_total


@pytest.mark.parametrize("domain,seed", ((MECH, None), (ELEC, ELEC_SEED)))
def test_n82_pdf_source_carries_the_same_next_steps_as_the_screen_report(client, monkeypatch, domain, seed):
    sid = _start(client) if seed is None else _start(client, seed=seed, domain=domain)
    _set_gaps(sid, *[(g, OPEN) for g in GAPS])
    for lang in ("en", "ar"):
        screen = _report(client, sid, lang=lang)
        source = _pdf_source(client, sid, monkeypatch)
        assert _ns_blocks(source) == _ns_blocks(screen) and len(_ns_blocks(source)) == 3


def test_n83_pdf_source_has_no_next_steps_when_every_gap_is_closed(client, monkeypatch):
    sid = _start(client, seed=ELEC_SEED, domain=ELEC)
    _set_gaps(sid, *[(g, CLOSED) for g in GAPS])
    assert "cap01-next-steps" not in _pdf_source(client, sid, monkeypatch)


def test_n84_every_line_exists_in_both_languages_with_equal_list_lengths():
    for key in _all_next_keys():
        assert set(ui_text.UI_STRINGS[key]) >= {"en", "ar"}
        assert _text(key, "en").strip() and _text(key, "ar").strip()
        if "_SEARCH_" not in key:
            assert _text(key, "en") != _text(key, "ar"), key
            assert re.search(r"[؀-ۿ]", _text(key, "ar")), key
        if "InventorAI" in _text(key, "en"):
            assert "InventorAI" in _text(key, "ar"), key
    for domain, gap in PAIRS:
        view = _next(domain, gap)
        for name in ("topic_keys", "search_keys", "measure_keys"):
            assert all(ui_text.has_string(k) for k in view[name])


# ==========================================================================
# N9. Stage-18 closure truth
# ==========================================================================
_COMPLETE = "STAGE 18: COMPLETE — CURRENT MECHANICAL + ELECTRICAL / ELECTRONICS SCOPE"
_NO_S19 = "NO STAGE-19 IMPLEMENTATION AUTHORIZED BY STAGE-18 CLOSURE"
# The later Owner-authorized Stage 19, 20, 21 and 22 closures moved the marker on to Stage 23 (navigation only); the
# Stage-18 completion and the "no Stage-19 implementation by the Stage-18 closure" fact stay true history.
# The later Owner-authorized Stage 23 closure (no product change) moved the marker on to Stage 24 (navigation only);
# the later delivered CAP-12 Form Mock-up Advisory Slice 1 entered Stage 24 as ENTERED / PARTIAL (marker unchanged).
_MARKER = "MASTER ROADMAP SEQUENTIAL MARKER: STAGE 24 — ENTERED / PARTIAL — NAVIGATION ONLY"


def _flat(text):
    return re.sub(r"\s+", " ", text)


def _claude_md():
    with io.open(os.path.join(_ROOT, "CLAUDE.md"), encoding="utf-8") as fh:
        return fh.read()


def test_n90_the_closure_truth_is_recorded_on_every_current_surface():
    surfaces = {"CLAUDE.md": _flat(_claude_md())}
    for name in ("ACTIVE_INCREMENT_CONTRACT.md", "CURRENT_PROJECT_STATE.md",
                 "INVENTORAI_MASTER_EXECUTION_ROADMAP.md",
                 "INVENTORAI_MASTER_ROADMAP_EXECUTION_CHECKLIST.md",
                 "INVENTORAI_CAPABILITY_ENRICHMENT_REGISTER.md"):
        surfaces[name] = _flat(_doc(name))
    for name, text in surfaces.items():
        assert _COMPLETE in text, name
        assert _MARKER in text, name
    for name in ("ACTIVE_INCREMENT_CONTRACT.md", "INVENTORAI_MASTER_EXECUTION_ROADMAP.md",
                 "INVENTORAI_MASTER_ROADMAP_EXECUTION_CHECKLIST.md"):
        assert _NO_S19 in surfaces[name], name
    assert "**ACTIVE CONTRACT: NONE.**" in surfaces["CLAUDE.md"]
    assert "ACTIVE CONTRACT: NONE" in surfaces["ACTIVE_INCREMENT_CONTRACT.md"]
    # no new governance document and no decision-register entry for this closure
    assert "Gap-Scoped Technical Next-Step Guidance" not in _doc("OWNER_DECISION_REGISTER.md")


def test_n91_only_stage_18_is_ticked_by_the_closure_and_earlier_unfinished_stages_stay_open():
    roadmap = _doc("INVENTORAI_MASTER_EXECUTION_ROADMAP.md")
    assert re.search(r"^- \[x\] \*\*18 — D13/CAP-01 guidance:\*\*", roadmap, re.M)
    assert re.search(r"^- \[x\] \*\*15 — ", roadmap, re.M)
    # Stages 19, 20, 21 and 22 were ticked later by their own Owner-authorized closures (each for its own bounded
    # scope), not by this one
    for stage in (19, 20, 21, 22):
        assert re.search(r"^- \[x\] \*\*%d — " % stage, roadmap, re.M), stage
    # Stage 23 was ticked later by its own Owner-authorized closure (bounded four-axis scope, no product change)
    assert re.search(r"^- \[x\] \*\*23 — ", roadmap, re.M)
    for stage in (11, 13, 14, 16, 17, 24):
        assert re.search(r"^- \[ \] \*\*%d — " % stage, roadmap, re.M), stage
    checklist = _flat(_doc("INVENTORAI_MASTER_ROADMAP_EXECUTION_CHECKLIST.md"))
    assert ("**CURRENT STAGE:** Stage 24 — CAP-12 bounded materials / manufacturing advice — ENTERED / PARTIAL — "
            "NAVIGATION ONLY.") in checklist
    assert _NO_S19 in checklist


def test_n92_msnl_stays_future_deferred_and_full_cap01_stays_unauthorized():
    roadmap = _flat(_doc("INVENTORAI_MASTER_EXECUTION_ROADMAP.md"))
    contract = _flat(_doc("ACTIVE_INCREMENT_CONTRACT.md"))
    for text in (roadmap, contract):
        assert "MSNL: FUTURE / DEFERRED / NOT ACTIVATED" in text
        assert ("Full future CAP-01 (typed parameters, calculations, specialist mapping, further domains) stays NOT "
                "AUTHORIZED") in text
        assert "MSNL was NOT a Stage-18 completion blocker" in text
    # the historical Research Gate 3 language is kept and reconciled, not erased or reopened
    assert "Research Gate 3 appointments and activation remain prerequisites" in roadmap
    assert "Research Gate 3 is not reopened" in roadmap
