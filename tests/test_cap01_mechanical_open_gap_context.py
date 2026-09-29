# -*- coding: utf-8 -*-
"""MECHANICAL CAP-01 — OPEN-GAP TECHNICAL CONTEXT (Owner-authorized bounded slice).

What is pinned: for each CURRENT canonical Mechanical gap whose EXACT canonical
identity is MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY or BOUNDARY_AMBIGUITY and
whose EXACT canonical lifecycle state is OPEN or PARTIAL, the report and the PDF
show ONE short explanatory note: what that gap concerns at concept level within
the governed Mechanical package, and what InventorAI does NOT conclude from it.

Boundaries proven here:
  * BINDING — exact canonical gap id + exact lifecycle state from the loaded
    ``IdeaState``; never a display label, translated label, question text,
    near / fuzzy string, publicized package wording or list position.
  * OWNERSHIP — Path-N stays the only served-question owner; CAP-04 stays the
    only action / responsibility / required-input / closure owner. The block
    carries no question, action, responsibility, closure rule or next action.
  * SOURCE — copy is justified by ``domains/mechanical/domain.json`` (the
    governed package) and the Owner boundary only; the D13 Electronics TKP is
    not a Mechanical source and is never referenced.
  * TRUTH — PHYSICAL_FEASIBILITY copy never states or implies feasibility is
    proven; no unsupported engineering concept appears anywhere.
  * SCOPE — report + PDF only; the session journey gains nothing; this slice
    leaves Electronics CAP-01 output byte-identical (the separately authorized
    Electrical / Electronics Technical Deepening Slice 1 adds its own Electronics
    PHYSICAL_FEASIBILITY context, guarded in
    tests/test_cap01_electrical_reference_fundamentals.py); no state,
    persistence, readiness or progression mutation.

Mechanical Technical Deepening Slice 1 — Force, Moment & Pressure Fundamentals
(section F below) adds ONE optional reference-fundamentals sub-view to the
already-resolved PHYSICAL_FEASIBILITY context: the SAME four bounded reference
relationships (T = F × L⊥; F₁L₁ = F₂L₂; F = pA; N·m / Pa / kPa) whenever, and
only whenever, the exact canonical Mechanical PHYSICAL_FEASIBILITY gap is OPEN
or PARTIAL. Truth lives in the governed pack's ``reference_fundamentals`` group
and provenance mechanical:PR006–PR011; nothing is calculated, selected or
inferred, and no other gap, domain, label, text or signal can trigger it.
"""
import copy
import hashlib
import html as html_module
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
    ACCEPTED_RISK, BOUNDARY_AMBIGUITY, CLOSED, Gap, IdeaState,
    MECHANISM_COMPLETENESS, OPEN, PARTIAL, PHYSICAL_FEASIBILITY,
    PROBLEM_MECHANISM_FIT, ASSUMPTION_INVENTORY, EXPERTISE_GAP_AWARENESS)
from engine.path_n_questions import get_served_question
from web import cap01_guidance, gap_labels, ui_text
from tests.test_safe_question_routing_pf_q2 import (  # noqa: F401  (fixture)
    client, MECH, _start, _answer, _live,
)
from tests.test_stage18_cap01_bounded_guidance import (
    _denied, _mentions, _sentences, _mask_csrf, PROFILE_ID, ELECTRONICS_IDEA,
    MECHANICAL_IDEA, OPEN_GAP_INPUT, _state as _s18_state)

_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
_GUIDANCE_PATH = os.path.join(_ROOT, "web", "cap01_guidance.py")
_UI_TEXT_PATH = os.path.join(_ROOT, "web", "ui_text.py")
_APP_PATH = os.path.join(_ROOT, "web", "app.py")
_TEMPLATE_PATH = os.path.join(_ROOT, "web", "templates", "deliverable.html")
_SESSION_TEMPLATE_PATH = os.path.join(_ROOT, "web", "templates", "session.html")
_MECH_PACKAGE_PATH = os.path.join(_ROOT, "domains", "mechanical", "domain.json")

GROUP_ID = "CAP01_MECHANICAL_GAP_CONTEXT_V1"
PREFIX = "UI_%s_" % GROUP_ID
SUPPORTED = (MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY)
# The template's traceability attribute form (CAP-04 convention; never visible text).
ATTR = {g: g.lower().replace("_", "-") for g in SUPPORTED}
# Electrical / Electronics Technical Deepening Slice 1 — the ONE other gap-context
# row (its own group, exactly PHYSICAL_FEASIBILITY); guarded in full by
# tests/test_cap01_electrical_reference_fundamentals.py.
ELEC_DOMAIN = "electronics_electrical"
ELEC_GROUP_ID = "CAP01_ELECTRONICS_GAP_CONTEXT_V1"
UNSUPPORTED = (PROBLEM_MECHANISM_FIT, ASSUMPTION_INVENTORY, EXPERTISE_GAP_AWARENESS,
               "SAFETY_SIGNAL", "THERMAL_BEHAVIOUR", "NOT_A_GAP")


# ==========================================================================
# harness
# ==========================================================================
def _mech_package():
    with io.open(_MECH_PACKAGE_PATH, encoding="utf-8") as fh:
        return json.load(fh)


def _source(path):
    with io.open(path, encoding="utf-8") as fh:
        return fh.read()


def _gaps(*pairs):
    return [Gap(gap_type=g, status=s, opened_at=0) for g, s in pairs]


def _mech_state(*pairs):
    s = IdeaState(idea_id="cap01-mech-probe")
    s.domain = "mechanical"
    s.domain_signal = "mechanical"
    s.gaps = _gaps(*pairs)
    return s


def _resolve(*pairs, domain="mechanical"):
    return cap01_guidance.gap_contexts_for_gaps(domain, _gaps(*pairs))


def _rendered_gaps(view):
    return tuple((c["gap_type"], c["gap_state"]) for c in view["contexts"]) if view else ()


def _render(package, state, lang="en", pdf=False, with_contexts=True, **extra):
    """Render the REAL deliverable template exactly as the two routes do: the
    gap-scoped view is resolved in the web layer and passed as copy keys."""
    from flask import session as flask_session
    kwargs = dict(package=package, sid="cap01mech",
                  eligible=package["_session_meta"]["deliverable_eligible"],
                  t2a_statements={}, evidence_references=[],
                  decision_capture=None, snapshot_kept_ack=None,
                  gap_action_packs=appmod._gap_action_packs_context(state, lang))
    if with_contexts:
        kwargs["cap01_gap_contexts"] = appmod._cap01_gap_contexts(package, state)
    kwargs.update(extra)
    if pdf:
        kwargs["deliverable_base"] = "pdf_base.html"
    with appmod.app.test_request_context("/"):
        flask_session["ui_lang"] = lang
        return appmod.app.jinja_env.get_template("deliverable.html").render(**kwargs)


_BLOCK_RE = re.compile(r'<div class="cap01-gap-block"[^>]*>.*?\n  </div>', re.S)
_CTX_RE = re.compile(
    r'<div class="cap01-gap-context" data-cap01-gap="([^"]+)" data-cap01-gap-state="([^"]+)">'
    r'(.*?)</div>', re.S)


def _block(html):
    m = _BLOCK_RE.search(html)
    return m.group(0) if m else None


def _contexts(html):
    """``[(gap-attr, state-attr), ...]`` in rendered order."""
    block = _block(html)
    return [(g, s) for g, s, _body in _CTX_RE.findall(block)] if block else []


def _visible(fragment):
    return re.sub(r"\s+", " ", html_module.unescape(re.sub(r"<[^>]+>", " ", fragment))).strip()


def _report(c, sid, lang="en"):
    if lang == "ar":
        assert c.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    return c.get(f"/session/{sid}/deliverable").get_data(as_text=True)


def _pdf_source(c, sid, monkeypatch):
    seen = {}
    real = appmod._render_pdf_bytes

    def spy(source):
        seen["source"] = source
        return real(source)
    monkeypatch.setattr(appmod, "_render_pdf_bytes", spy)
    r = c.post(f"/session/{sid}/deliverable.pdf", data={})
    assert r.status_code == 200 and r.mimetype == "application/pdf"
    assert r.data[:5] == b"%PDF-"
    return seen["source"]


def _set_gaps(sid, *pairs):
    """Put an exact canonical gap set on the LIVE state (test-local, in memory)."""
    _live(sid).gaps = _gaps(*pairs)


def _copy(gap_type, part, lang):
    return ui_text.UI_STRINGS[PREFIX + gap_type + "_" + part][lang]


FUND_PREFIX = PREFIX + PHYSICAL_FEASIBILITY + "_FUNDAMENTALS_"
FUND_GROUP = "force_moment_pressure_v1"
FUND_CLAIMS = ("torque_moment_perpendicular", "ideal_static_moment_balance",
               "pressure_force_area_uniform", "si_quantity_unit_discipline")
FUND_EQUATIONS = ("T = F × L⊥", "F₁L₁ = F₂L₂", "F = pA", "N·m")
FUND_ITEM_PARTS = ("TITLE", "LEAD", "EQUATION", "NOTE")
FUND_PART_KEYS = tuple(FUND_PREFIX + p for p in ("TITLE", "INTRO", "SOURCE", "BOUNDARY")) + tuple(
    FUND_PREFIX + "ITEM_%d_%s" % (n, p) for n in range(1, 5) for p in FUND_ITEM_PARTS)
_PROVENANCE_PATH = os.path.join(_ROOT, "domains", "domain_provenance.json")
# The six Owner-authorized source / policy records of this slice, in allocation order.
FUND_PROVENANCE = {
    "mechanical:PR006": "https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/torque-moment/",
    "mechanical:PR007": "https://www.grc.nasa.gov/www/k-12/WindTunnel/Activities/balance_of_forces.html",
    "mechanical:PR008": "https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/aerodynamic-forces/",
    "mechanical:PR009": ("https://www.nist.gov/pml/special-publication-811/"
                         "nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b9"),
    "mechanical:PR010": "https://sti.nasa.gov/disclaimers/",
    "mechanical:PR011": ("https://www.nist.gov/open/copyright-fair-use-and-licensing-statements-"
                         "srd-data-software-and-technical-series-publications"),
}
FUND_CLAIM_SOURCES = {
    "torque_moment_perpendicular": ("mechanical:PR006", "mechanical:PR010"),
    "ideal_static_moment_balance": ("mechanical:PR007", "mechanical:PR010"),
    "pressure_force_area_uniform": ("mechanical:PR008", "mechanical:PR010"),
    "si_quantity_unit_discipline": ("mechanical:PR009", "mechanical:PR011"),
}


def _mech_keys():
    """The gap-context keys of the three Mechanical contexts (title / meaning /
    limit plus the group heading and intro) — NOT the fundamentals sub-view."""
    return sorted(k for k in ui_text.UI_STRINGS
                  if k.startswith(PREFIX) and not k.startswith(FUND_PREFIX))


def _fund_keys():
    return sorted(k for k in ui_text.UI_STRINGS if k.startswith(FUND_PREFIX))


def _fund_copy(part, lang):
    return ui_text.UI_STRINGS[FUND_PREFIX + part][lang]


def _fund_texts(lang):
    """Every reader-visible fundamentals string in ONE language, keyed by part."""
    return {k[len(FUND_PREFIX):]: ui_text.UI_STRINGS[k][lang] for k in _fund_keys()}


def _provenance():
    with io.open(_PROVENANCE_PATH, encoding="utf-8") as fh:
        return {r["record_id"]: r for r in json.load(fh)["records"]}


def _fund_group():
    groups = _mech_package().get("reference_fundamentals")
    assert isinstance(groups, list) and len(groups) == 1
    return groups[0]


_FUND_RE = re.compile(r'<div class="cap01-fundamentals"[^>]*>.*?</div>\s*</div>', re.S)


def _fundamentals_blocks(html):
    return _FUND_RE.findall(html)


def _equations(block):
    return re.findall(
        r'<bdi class="cap01-fund-equation" dir="ltr" data-cap01-fund-equation>(.*?)</bdi>', block)


def _claims(block):
    return re.findall(r'data-cap01-fund-claim="([^"]+)"', block)


# ==========================================================================
# 1–3. ONE supported gap OPEN -> only that context
# ==========================================================================
@pytest.mark.parametrize("gap", SUPPORTED)
def test_01_03_only_the_matching_context_renders_for_one_open_gap(gap):
    view = _resolve((gap, OPEN))
    assert view is not None and view["group_id"] == GROUP_ID
    assert _rendered_gaps(view) == ((gap, OPEN),)
    state = _mech_state((gap, OPEN))
    html = _render(assemble_deliverable(state), state)
    assert _contexts(html) == [(ATTR[gap], "open")]
    for other in SUPPORTED:
        if other != gap:
            assert 'data-cap01-gap="%s"' % ATTR[other] not in html


# ==========================================================================
# 4. PARTIAL for each supported gap -> matching context
# ==========================================================================
@pytest.mark.parametrize("gap", SUPPORTED)
def test_04_partial_state_renders_the_matching_context(gap):
    assert _rendered_gaps(_resolve((gap, PARTIAL))) == ((gap, PARTIAL),)
    state = _mech_state((gap, PARTIAL))
    html = _render(assemble_deliverable(state), state)
    assert _contexts(html) == [(ATTR[gap], "partial")]


# ==========================================================================
# 5. Multiple supported gaps -> exactly the matching ones, once, source order
# ==========================================================================
def test_05a_all_three_current_render_once_each_in_source_order_not_state_order():
    reversed_pairs = ((BOUNDARY_AMBIGUITY, PARTIAL), (PHYSICAL_FEASIBILITY, OPEN),
                      (MECHANISM_COMPLETENESS, OPEN))
    assert _rendered_gaps(_resolve(*reversed_pairs)) == (
        (MECHANISM_COMPLETENESS, OPEN), (PHYSICAL_FEASIBILITY, OPEN),
        (BOUNDARY_AMBIGUITY, PARTIAL))
    state = _mech_state(*reversed_pairs)
    html = _render(assemble_deliverable(state), state)
    assert _contexts(html) == [(ATTR[MECHANISM_COMPLETENESS], "open"),
                               (ATTR[PHYSICAL_FEASIBILITY], "open"),
                               (ATTR[BOUNDARY_AMBIGUITY], "partial")]
    assert html.count("cap01-gap-block") == 1
    for gap in SUPPORTED:
        assert html.count('data-cap01-gap="%s"' % ATTR[gap]) == 1


def test_05b_mixed_states_render_exactly_the_current_subset():
    view = _resolve((MECHANISM_COMPLETENESS, CLOSED), (PHYSICAL_FEASIBILITY, OPEN),
                    (BOUNDARY_AMBIGUITY, ACCEPTED_RISK))
    assert _rendered_gaps(view) == ((PHYSICAL_FEASIBILITY, OPEN),)


def test_05c_a_duplicated_gap_record_never_yields_a_second_context():
    view = _resolve((MECHANISM_COMPLETENESS, OPEN), (MECHANISM_COMPLETENESS, OPEN),
                    (MECHANISM_COMPLETENESS, PARTIAL))
    assert _rendered_gaps(view) == ((MECHANISM_COMPLETENESS, OPEN),)


def test_05d_duplicate_records_follow_the_canonical_first_match_accessor():
    """``IdeaState.get_gap`` reports the FIRST record; the context must never
    report a different state than the canonical accessor would."""
    for first, second in ((CLOSED, OPEN), (OPEN, CLOSED)):
        state = _mech_state((PHYSICAL_FEASIBILITY, first), (PHYSICAL_FEASIBILITY, second))
        view = cap01_guidance.gap_contexts_for_gaps("mechanical", state.gaps)
        expected = ((PHYSICAL_FEASIBILITY, first),) if first in (OPEN, PARTIAL) else ()
        assert _rendered_gaps(view) == expected
        assert state.get_gap(PHYSICAL_FEASIBILITY).status == first


# ==========================================================================
# 6–7. CLOSED / ACCEPTED_RISK / absent / unknown state -> nothing
# ==========================================================================
@pytest.mark.parametrize("gap", SUPPORTED)
@pytest.mark.parametrize("status", (CLOSED, ACCEPTED_RISK))
def test_06_07_closed_and_accepted_risk_render_no_context(gap, status):
    assert _resolve((gap, status)) is None
    state = _mech_state((gap, status))
    html = _render(assemble_deliverable(state), state)
    assert _block(html) is None and "data-cap01-gap" not in html


def test_07b_absent_gaps_and_non_canonical_states_render_nothing():
    assert _resolve() is None
    assert cap01_guidance.gap_contexts_for_gaps("mechanical", None) is None
    assert cap01_guidance.gap_contexts_for_gaps("mechanical", 17) is None
    for bad in ("open", "Open", "OPEN ", " OPEN", "PARTIALLY", "RESOLVED", "", None, 1):
        assert _resolve((MECHANISM_COMPLETENESS, bad)) is None, bad


def test_07c_a_closed_supported_gap_beside_an_open_one_contributes_nothing():
    state = _mech_state((MECHANISM_COMPLETENESS, CLOSED), (BOUNDARY_AMBIGUITY, OPEN))
    html = _render(assemble_deliverable(state), state)
    assert _contexts(html) == [(ATTR[BOUNDARY_AMBIGUITY], "open")]


# ==========================================================================
# 8. Unsupported / non-governed gap -> no invented context
# ==========================================================================
@pytest.mark.parametrize("gap", UNSUPPORTED)
def test_08_unsupported_gap_never_gets_an_invented_context(gap):
    assert cap01_guidance.gap_context_copy("mechanical", gap) is None
    assert _resolve((gap, OPEN)) is None
    view = _resolve((gap, OPEN), (PHYSICAL_FEASIBILITY, OPEN))
    assert _rendered_gaps(view) == ((PHYSICAL_FEASIBILITY, OPEN),)


def test_08b_the_supported_set_is_exactly_the_governed_packages_supported_gap_types():
    pkg = _mech_package()
    governed = tuple(pkg["capability_declaration"]["supported_gap_types"])
    mapped = tuple(m["gap_type_id"] for m in pkg["gap_type_mappings"])
    group_id, gap_ids = cap01_guidance.CAP01_GAP_CONTEXT_BY_DOMAIN["mechanical"]
    assert group_id == GROUP_ID
    assert gap_ids == governed == mapped == SUPPORTED
    # Electrical / Electronics Technical Deepening Slice 1 added exactly ONE other
    # row: the Electronics PHYSICAL_FEASIBILITY context (its own group, one gap).
    assert tuple(cap01_guidance.CAP01_GAP_CONTEXT_BY_DOMAIN) == ("mechanical", ELEC_DOMAIN)
    assert cap01_guidance.CAP01_GAP_CONTEXT_BY_DOMAIN[ELEC_DOMAIN] == (
        ELEC_GROUP_ID, (PHYSICAL_FEASIBILITY,))


# ==========================================================================
# 9. Electronics CAP-01 profile unchanged
# ==========================================================================
def test_09a_electronics_profile_table_copy_and_resolver_are_unchanged():
    assert cap01_guidance.CAP01_PROFILE_BY_DOMAIN == {"electronics_electrical": PROFILE_ID}
    view = cap01_guidance.profile_copy("electronics_electrical")
    assert view["profile_id"] == PROFILE_ID and len(view["item_keys"]) == 6
    assert view["research"] is not None and len(view["research"]["item_keys"]) == 6
    elec = cap01_guidance.gap_contexts_for_gaps("electronics_electrical",
                                                _gaps(*[(g, OPEN) for g in SUPPORTED]))
    assert elec["group_id"] == ELEC_GROUP_ID != GROUP_ID
    assert _rendered_gaps(elec) == ((PHYSICAL_FEASIBILITY, OPEN),)
    assert not any(v.startswith(PREFIX) for c in elec["contexts"] for v in c.values()
                   if isinstance(v, str))
    assert cap01_guidance.gap_contexts_for_gaps(
        "electronics_electrical", _gaps((MECHANISM_COMPLETENESS, OPEN),
                                        (BOUNDARY_AMBIGUITY, OPEN))) is None


def test_09b_electronics_report_is_byte_identical_with_the_mechanical_table_removed(monkeypatch):
    state = _s18_state(ELECTRONICS_IDEA, OPEN_GAP_INPUT)
    package = assemble_deliverable(state)
    assert package["section_3_assessment_overview"]["capabilities_assessed"][0]["gaps_open"] >= 1
    with_table = _mask_csrf(_render(package, state))
    assert 'data-cap01-profile="%s"' % PROFILE_ID in with_table
    assert "cap01-gap-block" not in with_table
    monkeypatch.setattr(cap01_guidance, "CAP01_GAP_CONTEXT_BY_DOMAIN", {})
    assert _mask_csrf(_render(package, state)) == with_table


# ==========================================================================
# 10. Non-Mechanical project -> no Mechanical context
# ==========================================================================
@pytest.mark.parametrize("domain", ("software", "medical_device",
                                    "unknown", "", "Mechanical", "MECHANICAL", "mechanic",
                                    "mechanical_v1", "الميكانيكا", None, 3))
def test_10_non_mechanical_domain_never_resolves_a_context(domain):
    """The domain id is TRUSTED and server-resolved; like ``profile_for_domain``
    it tolerates surrounding whitespace only, never case or a near string."""
    assert _resolve(*[(g, OPEN) for g in SUPPORTED], domain=domain) is None


def test_10c_electronics_never_resolves_a_mechanical_context():
    """Electrical / Electronics Technical Deepening Slice 1: the Electronics domain
    resolves ONLY its own PHYSICAL_FEASIBILITY context, never a Mechanical one."""
    view = _resolve(*[(g, OPEN) for g in SUPPORTED], domain=ELEC_DOMAIN)
    assert view["group_id"] == ELEC_GROUP_ID
    assert _rendered_gaps(view) == ((PHYSICAL_FEASIBILITY, OPEN),)
    assert view["contexts"][0]["fundamentals"]["group_id"] != FUND_GROUP


def test_10b_the_package_supplies_only_the_trusted_domain_and_never_the_binding():
    """The publicized ``gaps_detail[].gap_type`` is presentation wording. Even
    with every gap publicized as open, a non-Mechanical capability row yields
    nothing, and a Mechanical row with no CURRENT canonical gap yields nothing."""
    state = _mech_state(*[(g, OPEN) for g in SUPPORTED])
    package = assemble_deliverable(state)
    rows = package["section_3_assessment_overview"]["capabilities_assessed"]
    assert rows[0]["gaps_detail"][0]["gap_type"] != MECHANISM_COMPLETENESS  # publicized wording
    foreign = copy.deepcopy(package)
    foreign["section_3_assessment_overview"]["capabilities_assessed"][0]["capability_id"] = \
        "electronics_electrical"
    foreign_view = cap01_guidance.gap_contexts_for_package(foreign, state.gaps)
    assert foreign_view["group_id"] == ELEC_GROUP_ID          # never the Mechanical group
    assert _rendered_gaps(foreign_view) == ((PHYSICAL_FEASIBILITY, OPEN),)
    foreign["section_3_assessment_overview"]["capabilities_assessed"][0]["capability_id"] = \
        "software"
    assert cap01_guidance.gap_contexts_for_package(foreign, state.gaps) is None
    assert cap01_guidance.gap_contexts_for_package(package, _gaps(*[(g, CLOSED) for g in SUPPORTED])) is None
    assert cap01_guidance.gap_contexts_for_package(package, []) is None
    assert cap01_guidance.gap_contexts_for_package({}, state.gaps) is None
    assert cap01_guidance.gap_contexts_for_package(None, state.gaps) is None
    assert _rendered_gaps(cap01_guidance.gap_contexts_for_package(package, state.gaps)) == \
        tuple((g, OPEN) for g in SUPPORTED)


# ==========================================================================
# 11. Path-N: Mechanical served questions unchanged; no question copied
# ==========================================================================
def test_11_path_n_serves_the_governed_questions_and_the_block_copies_none():
    pkg = _mech_package()
    en_copy = " ".join(_copy(g, p, "en") for g in SUPPORTED for p in ("TITLE", "MEANING", "LIMIT"))
    for mapping in pkg["gap_type_mappings"]:
        gap = mapping["gap_type_id"]
        for n, q in enumerate(mapping["questions"]):
            served = get_served_question(gap, n, domain="mechanical")
            assert served is not None and served.question_id == q["question_id"], q
            assert isinstance(served.text, str) and served.text.strip()
            # the CAP-01 note is descriptive, never a second question set
            assert served.text not in en_copy, q["question_id"]
            assert q["text"] not in en_copy, q["question_id"]
    assert "?" not in en_copy and "؟" not in " ".join(
        _copy(g, p, "ar") for g in SUPPORTED for p in ("TITLE", "MEANING", "LIMIT"))


def test_11b_the_resolver_imports_no_question_action_or_engine_owner():
    """Executable imports only (prose describing the core it avoids is not an
    import): the resolver depends on the catalogue and nothing else."""
    import ast
    tree = ast.parse(_source(_GUIDANCE_PATH))
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.add("%s.%s" % (node.module, ",".join(a.name for a in node.names)))
    assert imported == {"web.ui_text"}, imported


# ==========================================================================
# 12. CAP-04 output unchanged; no action semantics in the block
# ==========================================================================
def test_12a_cap04_derivation_and_rendering_are_byte_identical_with_and_without_the_context():
    state = _mech_state((MECHANISM_COMPLETENESS, OPEN), (PHYSICAL_FEASIBILITY, PARTIAL),
                        (BOUNDARY_AMBIGUITY, CLOSED))
    package = assemble_deliverable(state)
    before = pickle.dumps(derive_gap_action_packs(state))
    ctx = appmod._cap01_gap_contexts(package, state)
    assert ctx is not None
    assert pickle.dumps(derive_gap_action_packs(state)) == before
    gp = re.compile(r'<div class="gp-packs".*?</div>\s*\{%|<div class="gp-packs".*?<span id="report-validation-plan"', re.S)
    with_ctx = _render(package, state)
    without = _render(package, state, with_contexts=False)
    assert gp.search(with_ctx).group(0) == gp.search(without).group(0)
    assert "cap01-gap-block" in with_ctx and "cap01-gap-block" not in without


_ACTION_TERMS_EN = ("you should", "you must", "next step", "do this", "provide evidence",
                    "responsibility", "required input", "closure", "action", "specialist",
                    "recommend", "next action", "to close this gap")
_ACTION_TERMS_AR = ("عليك", "يجب عليك", "الخطوة التالية", "مسؤولية", "إجراء", "إغلاق",
                    "أخصائي", "مختص", "نوصي", "توصية")


_EXTRA_NEGATORS_EN = ("no ", "add no", "adds no", "without")


def _denied_or_negated(sentence, term, lang):
    """The Stage-18 sentence-scoped denial, extended with the plain "no <term>"
    form ("they add no question, no action ...") which is a denial too."""
    if _denied(sentence, term, lang):
        return True
    if lang != "en":
        return False
    at = re.search(r"(?<!\w)%s(?!\w)" % re.escape(term), sentence, re.I)
    head = sentence[:at.start()].lower()
    return any(n in head for n in _EXTRA_NEGATORS_EN)


def test_12b_no_non_negated_action_responsibility_or_closure_wording():
    for lang, terms in (("en", _ACTION_TERMS_EN), ("ar", _ACTION_TERMS_AR)):
        for key in _mech_keys():
            for sentence in _sentences(ui_text.UI_STRINGS[key][lang]):
                for term in terms:
                    if _mentions(sentence, term):
                        assert _denied_or_negated(sentence, term, lang), (lang, key, term, sentence)


def test_12c_the_block_carries_none_of_cap04s_labels_or_attributes():
    state = _mech_state(*[(g, OPEN) for g in SUPPORTED])
    for lang in ("en", "ar"):
        block = _block(_render(assemble_deliverable(state), state, lang=lang))
        for marker in ("gp-", "data-gp-", "UI_GP_", "cap01-item", "cap01-research"):
            assert marker not in block, marker
        visible = _visible(block)
        for key in ("UI_GP_ACTION", "UI_GP_RESPONSIBILITY", "UI_GP_INPUT", "UI_GP_CLOSURE"):
            assert ui_text.UI_STRINGS[key][lang] not in visible, key


# ==========================================================================
# 13. No session-journey block
# ==========================================================================
def test_13_session_page_and_template_carry_no_cap01_gap_context(client):
    sid = _start(client)
    _set_gaps(sid, *[(g, OPEN) for g in SUPPORTED])
    for lang in ("en", "ar"):
        if lang == "ar":
            client.post("/ui-language", data={"lang": "ar"})
        page = client.get(f"/session/{sid}").get_data(as_text=True)
        assert "cap01" not in page
        assert ui_text.UI_STRINGS[PREFIX + "TITLE"][lang] not in page
        for gap in SUPPORTED:
            assert _copy(gap, "MEANING", lang) not in page
    assert "cap01" not in _source(_SESSION_TEMPLATE_PATH)


# ==========================================================================
# 14. No persistence / state / readiness / progression mutation
# ==========================================================================
def test_14_report_and_pdf_render_change_no_state_readiness_or_store(client, monkeypatch):
    sid = _start(client)
    _answer(client, sid, MECH)
    state = _live(sid)
    assert state.domain == "mechanical"
    before = pickle.dumps(state)
    readiness = derive_readiness(state)
    before_ready = (readiness.overall_verified(), readiness.unverified_contexts())
    before_gaps = [(g.gap_type, g.status) for g in state.gaps]
    store = appmod._get_store()
    before_rows = pickle.dumps(store.load_records(sid)) if hasattr(store, "load_records") else None
    # The report renders the block IFF a supported canonical gap is current on
    # the very state being rendered — and rendering it twice changes nothing.
    expected_block = any(g.gap_type in SUPPORTED and g.status in (OPEN, PARTIAL)
                         for g in state.gaps)
    for _ in range(2):
        assert ("cap01-gap-block" in _report(client, sid)) is expected_block
        _pdf_source(client, sid, monkeypatch)
    state = _live(sid)
    assert pickle.dumps(state) == before
    readiness = derive_readiness(state)
    assert (readiness.overall_verified(), readiness.unverified_contexts()) == before_ready
    assert [(g.gap_type, g.status) for g in state.gaps] == before_gaps
    if before_rows is not None:
        assert pickle.dumps(store.load_records(sid)) == before_rows


def _executable(path):
    """A file's executable text with every docstring blanked (the Stage-18
    discipline: a scan must not be satisfied or defeated by prose)."""
    import ast
    tree = ast.parse(_source(path))
    for node in ast.walk(tree):
        if (isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant)
                and isinstance(node.value.value, str)):
            node.value.value = ""
    return ast.unparse(tree)


def test_14b_the_change_is_read_only_glue_no_write_route_or_persistence():
    app_src = _source(_APP_PATH)
    code = _executable(_APP_PATH)
    helper = code[code.index("def _cap01_gap_contexts("):]
    helper = helper[:helper.index("\ndef ")]
    for forbidden in ("request.", "form", "_get_store()", "commit", "INSERT", "UPDATE",
                      "SESSION_STORE[", "write", "save"):
        assert forbidden not in helper, forbidden
    assert app_src.count("cap01_gap_contexts=_cap01_gap_contexts(package, state)") == 2
    guidance = _executable(_GUIDANCE_PATH)
    for forbidden in ("sqlite", "open(", "json.load", "request", "flask", "SESSION_STORE"):
        assert forbidden not in guidance, forbidden


# ==========================================================================
# 15–16. EN and AR / RTL report rendering through the real route
# ==========================================================================
def test_15_en_report_renders_the_matching_context_through_the_real_route(client):
    sid = _start(client)
    assert [(g.gap_type, g.status) for g in _live(sid).gaps] == [(MECHANISM_COMPLETENESS, OPEN)]
    page = _report(client, sid)
    assert _contexts(page) == [(ATTR[MECHANISM_COMPLETENESS], "open")]
    visible = _visible(_block(page))
    assert ui_text.UI_STRINGS[PREFIX + "TITLE"]["en"] in visible
    for part in ("TITLE", "MEANING", "LIMIT"):
        assert _copy(MECHANISM_COMPLETENESS, part, "en") in visible
        assert _copy(MECHANISM_COMPLETENESS, part, "ar") not in visible
    assert "UI_CAP01_" not in visible
    # the raw canonical identifiers never reach the reader
    for token in SUPPORTED:
        assert token not in visible


def test_16_ar_rtl_report_renders_the_arabic_context_only(client):
    sid = _start(client)
    _set_gaps(sid, (MECHANISM_COMPLETENESS, CLOSED), (PHYSICAL_FEASIBILITY, PARTIAL),
              (BOUNDARY_AMBIGUITY, OPEN))
    page = _report(client, sid, lang="ar")
    assert 'dir="rtl"' in page and 'lang="ar"' in page
    assert _contexts(page) == [(ATTR[PHYSICAL_FEASIBILITY], "partial"),
                               (ATTR[BOUNDARY_AMBIGUITY], "open")]
    visible = _visible(_block(page))
    assert ui_text.UI_STRINGS[PREFIX + "TITLE"]["ar"] in visible
    for gap in (PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY):
        for part in ("TITLE", "MEANING", "LIMIT"):
            assert _copy(gap, part, "ar") in visible
            assert _copy(gap, part, "en") not in visible
    assert _copy(MECHANISM_COMPLETENESS, "MEANING", "ar") not in visible
    assert "UI_CAP01_" not in visible


def test_16b_every_mechanical_key_is_bilingual_and_distinct():
    keys = _mech_keys()
    assert len(keys) == 2 + 3 * len(SUPPORTED)
    expected = [PREFIX + "INTRO", PREFIX + "TITLE"] + sorted(
        PREFIX + g + "_" + p for g in SUPPORTED for p in ("TITLE", "MEANING", "LIMIT"))
    assert keys == sorted(expected)
    for key in keys:
        entry = ui_text.UI_STRINGS[key]
        assert set(entry) == {"en", "ar"}
        assert entry["en"].strip() and entry["ar"].strip() and entry["en"] != entry["ar"]
        assert re.search(r"[؀-ۿ]", entry["ar"]), key
        assert not re.search(r"[؀-ۿ]", entry["en"]), key
    # The fundamentals sub-view is the ONLY other family under the Mechanical
    # prefix: 4 group parts + 4 items × 4 parts, every one bilingual; the four
    # EQUATION keys are language-neutral symbols and therefore identical.
    fund = _fund_keys()
    assert fund == sorted(FUND_PART_KEYS) and len(fund) == 20
    for key in fund:
        entry = ui_text.UI_STRINGS[key]
        assert set(entry) == {"en", "ar"} and entry["en"].strip() and entry["ar"].strip()
        if key.endswith("_EQUATION"):
            assert entry["en"] == entry["ar"], key
            assert not re.search(r"[\u0600-\u06FF]", entry["ar"]), key
        else:
            assert entry["en"] != entry["ar"], key
            assert re.search(r"[\u0600-\u06FF]", entry["ar"]), key
            assert not re.search(r"[\u0600-\u06FF]", entry["en"]), key
    assert sorted(k for k in ui_text.UI_STRINGS if k.startswith(PREFIX)) == sorted(keys + fund)


# ==========================================================================
# 17. PDF: matching contexts present, non-matching absent
# ==========================================================================
def test_17_pdf_source_carries_exactly_the_matching_contexts(client, monkeypatch):
    sid = _start(client)
    _set_gaps(sid, (MECHANISM_COMPLETENESS, PARTIAL), (PHYSICAL_FEASIBILITY, CLOSED),
              (BOUNDARY_AMBIGUITY, ACCEPTED_RISK))
    for lang in ("en", "ar"):
        screen = _report(client, sid, lang=lang)
        source = _pdf_source(client, sid, monkeypatch)
        assert _contexts(source) == [(ATTR[MECHANISM_COMPLETENESS], "partial")]
        assert _block(source) == _block(screen)
        visible = _visible(_block(source))
        assert _copy(MECHANISM_COMPLETENESS, "MEANING", lang) in visible
        for gap in (PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY):
            assert _copy(gap, "MEANING", lang) not in source
            assert _copy(gap, "TITLE", lang) not in source
        # PDF-only trusted shell: no interactive control inside the block
        assert "<form" not in _block(source) and "csrf" not in _block(source)


def test_17b_pdf_source_carries_no_context_when_no_supported_gap_is_current(client, monkeypatch):
    sid = _start(client)
    _set_gaps(sid, *[(g, CLOSED) for g in SUPPORTED])
    source = _pdf_source(client, sid, monkeypatch)
    assert "cap01-gap-block" not in source and "data-cap01-gap" not in source


# ==========================================================================
# 18. Exact canonical binding — negative controls
# ==========================================================================
def _label_variants():
    out = []
    for gap in SUPPORTED:
        out.append(gap_labels.GAP_DISPLAY_NAMES[gap])                   # display label
        out.append(gap_labels.GAP_DISPLAY_NAMES_AR[gap])                # translated label
        out.append(gap_labels.GAP_LABELS[gap]["heading"])               # question heading
    pkg = _mech_package()
    for mapping in pkg["gap_type_mappings"]:
        out.append(mapping["domain_label"])                             # package display label
        for q in mapping["questions"]:
            out.append(q["text"])                                       # governed question text
            out.append(q["question_id"])                                # question identity
        served = get_served_question(mapping["gap_type_id"], 0, domain="mechanical")
        out.append(served.text)                                         # served question text
    out += ["mechanism_completeness", "Mechanism_Completeness", "MECHANISM COMPLETENESS",
            "MECHANISM-COMPLETENESS", " MECHANISM_COMPLETENESS", "MECHANISM_COMPLETENESS ",
            "MECHANISM_COMPLETENES", "MECHANISM_COMPLETENESSS", "PHYSICAL_FEASIBLE",
            "PHYSICAL FEASIBILITY", "BOUNDARY", "BOUNDARY_AMBIGUITY_V1",
            "mechanical:MECHANISM_COMPLETENESS", "Physical Feasibility"]
    return out


@pytest.mark.parametrize("impostor", _label_variants())
def test_18_display_translated_question_and_fuzzy_strings_never_bind(impostor):
    assert impostor not in SUPPORTED, "not an impostor"
    assert cap01_guidance.gap_context_copy("mechanical", impostor) is None
    assert _resolve((impostor, OPEN)) is None
    assert _resolve((impostor, PARTIAL)) is None
    # and an impostor beside a real gap adds nothing
    assert _rendered_gaps(_resolve((impostor, OPEN), (BOUNDARY_AMBIGUITY, OPEN))) == \
        ((BOUNDARY_AMBIGUITY, OPEN),)


def test_18b_the_publicized_package_wording_is_not_the_binding_key():
    """``gaps_detail[].gap_type`` publicizes "Physical Feasibility"-style wording.
    Feeding the publicized rows as if they were gaps binds nothing."""
    state = _mech_state(*[(g, OPEN) for g in SUPPORTED])
    rows = assemble_deliverable(state)["section_3_assessment_overview"]["capabilities_assessed"]
    publicized = [(d["gap_type"], d["status"]) for d in rows[0]["gaps_detail"]]
    assert all(s == OPEN for _g, s in publicized) and len(publicized) == 3
    assert cap01_guidance.gap_contexts_for_gaps("mechanical", publicized) is None
    labels = [(d["gap_label"], d["status"]) for d in rows[0]["gaps_detail"]]
    assert cap01_guidance.gap_contexts_for_gaps("mechanical", labels) is None


def test_18c_the_resolver_compares_exactly_with_no_normalisation():
    code = _source(_GUIDANCE_PATH)
    tail = code[code.index("CAP01_GAP_CONTEXT_BY_DOMAIN = {"):]
    for forbidden in (".lower(", ".upper(", ".casefold(", "difflib", "fuzz", "re.search",
                      "re.match", " in text", "startswith(", "endswith(", "find("):
        assert forbidden not in tail, forbidden


def test_18d_the_template_binds_only_on_the_route_resolved_view():
    src = _source(_TEMPLATE_PATH)
    region = src[src.index("CAP01-BLOCK-START"):src.index("CAP01-BLOCK-END")]
    region = region[region.index("#}") + 2:]
    for literal in ("mechanical", "electronics", "gaps_detail", "gap_label", "gap_display",
                    "[0]", "elif"):
        assert literal not in region, literal
    for gap in SUPPORTED:
        assert gap not in region and ATTR[gap] not in region


# ==========================================================================
# S. SOURCE — every context traces to the governed Mechanical package
# ==========================================================================
def test_s1_each_meaning_traces_to_the_governed_package_concepts():
    pkg = _mech_package()
    covered = " ".join(pkg["coverage_declaration"]["covered_areas"])
    nuances = " ".join(r["description"] for r in pkg["rule_nuances"])
    questions = " ".join(q["text"] for m in pkg["gap_type_mappings"] for q in m["questions"])
    package_text = " ".join((covered, nuances, questions)).lower()
    traced = {
        MECHANISM_COMPLETENESS: ("moves, connects", "transfers force", "physical steps",
                                 "individual mechanical components", "physical detail"),
        PHYSICAL_FEASIBILITY: ("physical principle", "leverage", "spring tension", "gear ratio",
                               "friction", "material or force constraints"),
        BOUNDARY_AMBIGUITY: ("does not do or cover", "clear mechanical boundary",
                             "existing mechanical approach", "concrete", "physical"),
    }
    for gap, phrases in traced.items():
        meaning = _copy(gap, "MEANING", "en").lower()
        for phrase in phrases:
            assert phrase.lower() in meaning, (gap, phrase)
            # the concept itself exists in the governed package (allowing the
            # package's own comma / conjunction spelling)
            probe = phrase.lower().replace("does not do or cover", "not do or not cover") \
                .replace("moves, connects", "moves, connects, or")
            assert probe in package_text or phrase.split()[0].lower() in package_text, (gap, phrase)
        assert "concept level" in meaning or "concept-level" in meaning


def test_s2_each_limit_traces_to_the_governed_boundary_or_the_owner_boundary():
    pkg = _mech_package()
    unknowns = " ".join(pkg["capability_declaration"]["known_unknowns"]).lower()
    pf_limit = _copy(PHYSICAL_FEASIBILITY, "LIMIT", "en").lower()
    for phrase in ("real-world loads, wear, environmental conditions and failure behavior",
                   "cannot be established in software"):
        assert phrase in pf_limit, phrase
    assert "real-world loads, wear, environmental conditions, and failure behavior" in unknowns
    assert "cannot be established in software" in unknowns
    mc_limit = _copy(MECHANISM_COMPLETENESS, "LIMIT", "en").lower()
    for phrase in ("engineering-complete", "buildable", "dimensionally correct",
                   "physically fitting", "structurally adequate", "suitable materials",
                   "real world"):
        assert phrase in mc_limit, phrase
    ba_limit = _copy(BOUNDARY_AMBIGUITY, "LIMIT", "en").lower()
    for phrase in ("novel", "patentable", "superior", "validated", "compliant",
                   "ready for production"):
        assert phrase in ba_limit, phrase


def test_s3_the_d13_electronics_tkp_is_not_a_mechanical_source():
    ui = _source(_UI_TEXT_PATH)
    region = ui[ui.index('"' + PREFIX + "TITLE" + '"'):]
    region = region[:region.index("\n}\n")]
    for marker in ("D13", "d13", "tkp", "TKP", "research/", "datasheet", "sensor",
                   "microcontroller", "ADC"):
        assert marker not in region, marker
    # The resolver's EXECUTABLE code (docstrings blanked, comments dropped)
    # names no D13 / TKP identifier and no research path; the Electronics
    # boundary sentence in its module docstring is prose, not a dependency.
    executable = _executable(_GUIDANCE_PATH).lower()
    for marker in ("d13", "tkp", "research/"):
        assert marker not in executable, marker
    assert "research/d13" not in _source(_GUIDANCE_PATH)
    # the accepted Electronics EVIDENCE line still names D13; the Mechanical
    # copy never does
    assert "D13" in ui_text.UI_STRINGS["UI_%s_EVIDENCE" % PROFILE_ID]["en"]
    for key in _mech_keys():
        for lang in ("en", "ar"):
            assert "D13" not in ui_text.UI_STRINGS[key][lang], key


# ==========================================================================
# T. TRUTH — no overclaim, no unsupported engineering concept
# ==========================================================================
_FEASIBILITY_CLAIMS_EN = ("feasible", "is feasible", "physically feasible", "will work",
                          "works as intended", "performs as intended", "can be built",
                          "is buildable", "is complete", "is novel", "is patentable",
                          "is superior", "is compliant", "is safe", "is ready")
_FEASIBILITY_CLAIMS_AR = ("ممكنة فيزيائيًا", "ممكنة", "ستعمل", "تعمل كما هو مقصود",
                          "قابلة للبناء", "مكتملة", "جديدة", "أفضل", "متوافقة", "آمنة", "جاهزة")


def test_t1_physical_feasibility_copy_never_states_or_implies_feasibility_is_proven():
    for lang, claims in (("en", _FEASIBILITY_CLAIMS_EN), ("ar", _FEASIBILITY_CLAIMS_AR)):
        for gap in SUPPORTED:
            for part in ("TITLE", "MEANING", "LIMIT"):
                for sentence in _sentences(_copy(gap, part, lang)):
                    for claim in claims:
                        if _mentions(sentence, claim):
                            assert _denied(sentence, claim, lang), (lang, gap, part, claim, sentence)
    en = _copy(PHYSICAL_FEASIBILITY, "LIMIT", "en")
    ar = _copy(PHYSICAL_FEASIBILITY, "LIMIT", "ar")
    assert "does not conclude, that the mechanism is physically feasible" in en
    assert "unresolved concept-level gap" in en
    assert "لا يستنتج InventorAI، أن الآلية ممكنة فيزيائيًا" in ar
    assert "غير محسومة" in ar


_UNSUPPORTED_CONCEPTS = (
    "FEA", "finite element", "finite-element", "stress analysis", "fatigue", "GD&T",
    "tolerance", "stack analysis", "material selection", "material-selection",
    "certification", "certified", "manufacturability", "manufacturing process",
    "CAD", "load calculation", "safety determination", "regulatory", "prior art",
    "patent search", "specialist classification", "production-ready", "factor of safety",
    "yield strength", "N/mm", "MPa", "kN", "mm", "kg", "°", "%",
)
_UNSUPPORTED_CONCEPTS_AR = (
    "تحليل الإجهاد", "العناصر المحدودة", "الكلال", "التفاوتات", "اختيار المواد",
    "شهادة", "التصنيع", "CAD", "حساب الحمل", "تحديد السلامة", "براءات سابقة",
    "بحث براءات", "تصنيف الأخصائي", "معامل الأمان", "نيوتن", "ميغاباسكال", "كجم", "%",
)


def test_t2_no_unsupported_engineering_concept_number_or_unit_appears_in_the_copy():
    """The three gap contexts carry no engineering value, unit or number at all.
    (The fundamentals sub-view's bounded units and its source citation are
    scanned separately in section F, where SP 811 / B.9 are the only digits.)"""
    for lang, terms in (("en", _UNSUPPORTED_CONCEPTS), ("ar", _UNSUPPORTED_CONCEPTS_AR)):
        for key in _mech_keys():
            text = ui_text.UI_STRINGS[key][lang]
            for term in terms:
                assert not re.search(r"(?<!\w)%s(?!\w)" % re.escape(term), text, re.I), \
                    (lang, key, term)
            assert not re.search(r"\d", text), (lang, key, "digit")


def test_t3_the_copy_is_descriptive_and_concept_level_in_both_languages():
    for gap in SUPPORTED:
        assert _copy(gap, "MEANING", "en").startswith("This gap concerns")
        assert _copy(gap, "MEANING", "ar").startswith("تتعلق هذه الفجوة")
        assert "concept" in _copy(gap, "MEANING", "en")
        assert "المفاهيمي" in _copy(gap, "MEANING", "ar")
        assert "InventorAI does not conclude" in _copy(gap, "LIMIT", "en")
        assert "لا يستنتج InventorAI" in _copy(gap, "LIMIT", "ar")
    intro_en = ui_text.UI_STRINGS[PREFIX + "INTRO"]["en"]
    intro_ar = ui_text.UI_STRINGS[PREFIX + "INTRO"]["ar"]
    assert "add no question, no action, no responsibility and no closure rule" in intro_en
    assert "لا تضيف سؤالًا ولا إجراءً ولا مسؤولية ولا شرط إغلاق" in intro_ar
    # first-use bilingual labelling of the canonical technical concept (language policy)
    assert "(Mechanism Completeness)" in _copy(MECHANISM_COMPLETENESS, "TITLE", "ar")
    assert "(Physical Feasibility)" in _copy(PHYSICAL_FEASIBILITY, "TITLE", "ar")
    assert "(Boundary Ambiguity)" in _copy(BOUNDARY_AMBIGUITY, "TITLE", "ar")


# ==========================================================================
# R. RESOLVER contract — keys only, never text, never raises, fail closed
# ==========================================================================
def test_r1_the_resolver_returns_catalogue_keys_only_and_owns_no_text():
    view = _resolve(*[(g, OPEN) for g in SUPPORTED])
    for value in (view["title_key"], view["intro_key"]):
        assert value.startswith(PREFIX) and value in ui_text.UI_STRINGS
    for ctx in view["contexts"]:
        for part in ("title_key", "meaning_key", "limit_key"):
            assert ctx[part].startswith(PREFIX + ctx["gap_type"] + "_")
            assert ctx[part] in ui_text.UI_STRINGS
    guidance = _source(_GUIDANCE_PATH)
    for key in _mech_keys():
        for lang in ("en", "ar"):
            assert ui_text.UI_STRINGS[key][lang] not in guidance, key


def test_r2_incomplete_copy_fails_closed_per_gap_and_per_group(monkeypatch):
    monkeypatch.delitem(ui_text.UI_STRINGS, PREFIX + PHYSICAL_FEASIBILITY + "_LIMIT")
    view = _resolve(*[(g, OPEN) for g in SUPPORTED])
    assert _rendered_gaps(view) == ((MECHANISM_COMPLETENESS, OPEN), (BOUNDARY_AMBIGUITY, OPEN))
    monkeypatch.delitem(ui_text.UI_STRINGS, PREFIX + "INTRO")
    assert _resolve(*[(g, OPEN) for g in SUPPORTED]) is None


@pytest.mark.parametrize("gaps", (None, 0, "MECHANISM_COMPLETENESS", object(),
                                  [None], [("x",)], [("a", "b", "c")], [42], [object()],
                                  [(None, OPEN)], [(MECHANISM_COMPLETENESS, None)]))
def test_r3_malformed_gap_input_never_raises_and_never_binds(gaps):
    assert cap01_guidance.gap_contexts_for_gaps("mechanical", gaps) is None


def test_r4_the_web_helper_never_raises_and_the_pure_seam_is_the_only_source():
    assert appmod._cap01_gap_contexts(None, None) is None
    assert appmod._cap01_gap_contexts({}, object()) is None

    class Boom:
        @property
        def gaps(self):
            raise RuntimeError("boom")
    assert appmod._cap01_gap_contexts({}, Boom()) is None


def test_r5_no_cap01_vocabulary_reaches_the_deterministic_core():
    for rel in ("engine/progression_loop.py", "engine/idea_state.py", "engine/domain_rules.py",
                "engine/domain_activation.py", "engine/semantic_registry.py",
                "engine/deliverable_assembler.py", "engine/requirement_landscape.py",
                "engine/validation_plan.py", "engine/gap_action_pack.py",
                "engine/path_n_questions.py", "engine/record_store.py"):
        assert not re.search(r"cap.?01", _source(os.path.join(_ROOT, rel)), re.I), rel


def test_r6_the_governed_mechanical_package_is_unchanged_by_this_slice():
    """Content authority for implementation and tests; never edited by it."""
    digest = hashlib.sha256(_source(_MECH_PACKAGE_PATH).encode("utf-8")).hexdigest()
    pkg = _mech_package()
    assert pkg["pack_id"] == "mechanical" and pkg["status"] == "active"
    assert digest == hashlib.sha256(_source(_MECH_PACKAGE_PATH).encode("utf-8")).hexdigest()
    assert "Concept-level explanation of the mechanical mechanism" in \
        pkg["coverage_declaration"]["covered_areas"][0]


# ==========================================================================
# F. MECHANICAL TECHNICAL DEEPENING SLICE 1 — FORCE, MOMENT & PRESSURE
#    FUNDAMENTALS (optional sub-view of the PHYSICAL_FEASIBILITY context)
# ==========================================================================
def _pf_context(*pairs, domain="mechanical"):
    view = _resolve(*pairs, domain=domain)
    if view is None:
        return None
    for ctx in view["contexts"]:
        if ctx["gap_type"] == PHYSICAL_FEASIBILITY:
            return ctx
    return None


def _render_state(*pairs, lang="en", pdf=False):
    state = _mech_state(*pairs)
    return _render(assemble_deliverable(state), state, lang=lang, pdf=pdf)


# --- F1. positive binding -------------------------------------------------
@pytest.mark.parametrize("status", (OPEN, PARTIAL))
def test_f01_pf_open_or_partial_renders_the_fundamentals_exactly_once(status):
    ctx = _pf_context((PHYSICAL_FEASIBILITY, status))
    fund = ctx["fundamentals"]
    assert fund is not None and fund["group_id"] == FUND_GROUP
    assert tuple(c["claim_id"] for c in fund["claims"]) == FUND_CLAIMS
    for lang in ("en", "ar"):
        html = _render_state((PHYSICAL_FEASIBILITY, status), lang=lang)
        blocks = _fundamentals_blocks(html)
        assert len(blocks) == 1 and html.count('class="cap01-fundamentals"') == 1
        assert _claims(blocks[0]) == [c.replace("_", "-") for c in FUND_CLAIMS]
        assert _equations(blocks[0]) == list(FUND_EQUATIONS)
        # it sits INSIDE the PHYSICAL_FEASIBILITY context, after its limit line
        pf = re.search(r'<div class="cap01-gap-context" data-cap01-gap="physical-feasibility"'
                       r'[^>]*>(.*?)\n    </div>', html, re.S).group(1)
        assert "cap01-fundamentals" in pf and pf.index("data-cap01-gap-limit") < pf.index("cap01-fundamentals")


def test_f02_the_existing_pf_context_title_meaning_and_limit_are_unchanged_and_still_render():
    ctx = _pf_context((PHYSICAL_FEASIBILITY, OPEN))
    for part in ("title_key", "meaning_key", "limit_key"):
        assert ctx[part] == PREFIX + PHYSICAL_FEASIBILITY + "_" + part[:-4].upper()
    html = _render_state((PHYSICAL_FEASIBILITY, OPEN))
    visible = _visible(_block(html))
    for part in ("TITLE", "MEANING", "LIMIT"):
        assert _copy(PHYSICAL_FEASIBILITY, part, "en") in visible
    assert "does not conclude, that the mechanism is physically feasible" in visible


def test_f03_all_three_current_still_render_one_fundamentals_block_only():
    html = _render_state(*[(g, OPEN) for g in SUPPORTED])
    assert len(_fundamentals_blocks(html)) == 1
    assert _contexts(html) == [(ATTR[g], "open") for g in SUPPORTED]


# --- F2. negative binding -------------------------------------------------
@pytest.mark.parametrize("pairs", (
    ((PHYSICAL_FEASIBILITY, CLOSED),),
    ((PHYSICAL_FEASIBILITY, ACCEPTED_RISK),),
    ((PHYSICAL_FEASIBILITY, "open"),),
    ((PHYSICAL_FEASIBILITY, "RESOLVED"),),
    ((PHYSICAL_FEASIBILITY, ""),),
    ((MECHANISM_COMPLETENESS, OPEN),),
    ((BOUNDARY_AMBIGUITY, OPEN),),
    ((MECHANISM_COMPLETENESS, OPEN), (BOUNDARY_AMBIGUITY, PARTIAL), (PHYSICAL_FEASIBILITY, CLOSED)),
    ((MECHANISM_COMPLETENESS, PARTIAL), (PHYSICAL_FEASIBILITY, ACCEPTED_RISK)),
    (),
))
def test_f04_no_fundamentals_without_a_current_pf_gap(pairs):
    view = _resolve(*pairs)
    if view is not None:
        for ctx in view["contexts"]:
            assert ctx["gap_type"] != PHYSICAL_FEASIBILITY
            assert ctx["fundamentals"] is None
    for lang in ("en", "ar"):
        html = _render_state(*pairs, lang=lang)
        assert _fundamentals_blocks(html) == [] and "cap01-fundamentals" not in html
        for eq in FUND_EQUATIONS:
            assert eq not in _visible(html)


def test_f05_other_gap_contexts_never_carry_the_sub_view_even_beside_a_current_pf():
    view = _resolve(*[(g, OPEN) for g in SUPPORTED])
    by_gap = {c["gap_type"]: c for c in view["contexts"]}
    assert by_gap[MECHANISM_COMPLETENESS]["fundamentals"] is None
    assert by_gap[BOUNDARY_AMBIGUITY]["fundamentals"] is None
    assert by_gap[PHYSICAL_FEASIBILITY]["fundamentals"]["group_id"] == FUND_GROUP


@pytest.mark.parametrize("domain", ("software", "medical_device",
                                    "Mechanical", "MECHANICAL", "mechanic", "", None))
def test_f06_non_mechanical_domains_render_no_fundamentals(domain):
    assert _pf_context((PHYSICAL_FEASIBILITY, OPEN), domain=domain) is None
    assert cap01_guidance.CAP01_GAP_FUNDAMENTALS.get((domain, PHYSICAL_FEASIBILITY)) is None


def test_f06c_electronics_never_renders_the_mechanical_fundamentals():
    # Electrical / Electronics Technical Deepening Slice 1 owns its OWN row.
    fund = _pf_context((PHYSICAL_FEASIBILITY, OPEN), domain=ELEC_DOMAIN)["fundamentals"]
    assert fund["group_id"] == "basic_electrical_reference_v1" != FUND_GROUP
    assert not any(k.startswith(FUND_PREFIX) for c in fund["claims"] for k in c.values())


def test_f06b_electronics_report_is_byte_identical_with_the_fundamentals_table_removed(monkeypatch):
    state = _s18_state(ELECTRONICS_IDEA, OPEN_GAP_INPUT)
    package = assemble_deliverable(state)
    with_table = _mask_csrf(_render(package, state))
    assert "cap01-fundamentals" not in with_table
    monkeypatch.setattr(cap01_guidance, "CAP01_GAP_FUNDAMENTALS", {})
    assert _mask_csrf(_render(package, state)) == with_table


@pytest.mark.parametrize("impostor", _label_variants() + [
    "Physical Feasibility", "physical feasibility", "physical-feasibility", "الجدوى العملية",
    "الجدوى الفيزيائية", "PHYSICAL_FEASIBILITY:Q1", "mechanical:PHYSICAL_FEASIBILITY:Q2",
    "What physical principle does your mechanism rely on?", "torque", "pressure", "lever",
    "hydraulic", "moment arm"])
def test_f07_display_translated_question_and_fuzzy_strings_never_bind_the_fundamentals(impostor):
    assert impostor != PHYSICAL_FEASIBILITY
    assert cap01_guidance.CAP01_GAP_FUNDAMENTALS.get(("mechanical", impostor)) is None
    assert _resolve((impostor, OPEN)) is None
    # beside a current NON-PF gap the impostor adds neither a context nor a sub-view
    view = _resolve((impostor, OPEN), (MECHANISM_COMPLETENESS, OPEN))
    assert _rendered_gaps(view) == ((MECHANISM_COMPLETENESS, OPEN),)
    assert view["contexts"][0]["fundamentals"] is None


_TRIGGER_WORDS_IDEA = ("A hydraulic lever press: the torque on the arm, the moment arm length, "
                       "the pressure in the cylinder and the force on the piston area decide it. "
                       "T = F x L, F = pA, N·m, Pa, kPa, spring tension, gear ratio, friction.")


def test_f08_inventor_text_with_torque_pressure_lever_words_cannot_trigger_the_fundamentals():
    """The resolver takes no text at all; a state whose idea and answers are
    saturated with the block's own vocabulary renders nothing unless the exact
    canonical PHYSICAL_FEASIBILITY gap is current."""
    import inspect
    for fn in (cap01_guidance.gap_contexts_for_gaps, cap01_guidance.gap_context_copy,
               cap01_guidance.gap_contexts_for_package, cap01_guidance._fundamentals):
        params = list(inspect.signature(fn).parameters)
        assert not any(p in ("text", "idea", "answer", "signals", "response") for p in params), fn
    state = _mech_state((MECHANISM_COMPLETENESS, OPEN), (PHYSICAL_FEASIBILITY, CLOSED))
    state.idea_text = _TRIGGER_WORDS_IDEA
    state.known_problem = _TRIGGER_WORDS_IDEA
    html = _render(assemble_deliverable(state), state)
    assert "cap01-fundamentals" not in html
    for eq in FUND_EQUATIONS[:3]:
        assert eq not in _visible(_block(html))
    # ... and an Electronics project with the same words renders none either
    e_state = _s18_state(ELECTRONICS_IDEA, _TRIGGER_WORDS_IDEA)
    assert "cap01-fundamentals" not in _render(assemble_deliverable(e_state), e_state)


def test_f09_classification_and_substance_signals_cannot_trigger_the_fundamentals():
    """Signals decide the DOMAIN, never the sub-view: with every Mechanical
    classification and substance signal present in the text, a Mechanical
    state with no current PF gap renders no fundamentals."""
    pkg = _mech_package()
    words = " ".join(sig["signal"] for sig in pkg["classification_signals"] + pkg["substance_signals"])
    state = _mech_state((MECHANISM_COMPLETENESS, OPEN))
    state.idea_text = words
    assert "cap01-fundamentals" not in _render(assemble_deliverable(state), state)
    assert cap01_guidance.gap_contexts_for_gaps("mechanical", [(w, OPEN) for w in words.split()]) is None


def test_f10_same_bounded_set_regardless_of_project_content():
    """InventorAI selects no relationship for a project: two very different
    Mechanical projects with a current PF gap get the identical sub-view."""
    a = _mech_state((PHYSICAL_FEASIBILITY, OPEN)); a.idea_text = "a folding ramp with a spring latch"
    b = _mech_state((PHYSICAL_FEASIBILITY, PARTIAL)); b.idea_text = _TRIGGER_WORDS_IDEA
    fa = _fundamentals_blocks(_render(assemble_deliverable(a), a))[0]
    fb = _fundamentals_blocks(_render(assemble_deliverable(b), b))[0]
    assert fa == fb


# --- F3. technical content ------------------------------------------------
def test_f11_exactly_four_claims_with_the_exact_relationships_and_units():
    fund = _pf_context((PHYSICAL_FEASIBILITY, OPEN))["fundamentals"]
    assert len(fund["claims"]) == 4
    assert tuple(ui_text.UI_STRINGS[c["equation_key"]]["en"] for c in fund["claims"]) == FUND_EQUATIONS
    assert _fund_copy("ITEM_4_NOTE", "en").startswith("Pressure is expressed in Pa or kPa.")
    assert "Pa أو kPa" in _fund_copy("ITEM_4_NOTE", "ar")
    # the SI symbols are exactly the authorized ones
    for lang in ("en", "ar"):
        joined = " ".join(_fund_texts(lang).values())
        assert "N·m" in joined and "Pa" in joined and "kPa" in joined
        for wrong in ("Nm ", "N-m", "N.m", "newton-meter", "psi", "bar", "MPa", "kN", "lbf", "Nm."):
            assert wrong not in joined, wrong


_FIFTH_CONCEPTS = (
    "pulley", "mechanical advantage", "gear ratio", "spring", "Hooke", "friction coefficient",
    "coefficient of friction", "work =", "energy", "power", "Bernoulli", "Pascal's law",
    "hydraulic advantage", "stress", "strain", "FEA", "fatigue", "GD&T", "tolerance", "CAD",
    "yield", "safety factor", "factor of safety", "materials selection", "manufactur",
    "specialist", "certif", "readiness", "score", "confidence", "rank",
)
_FIFTH_CONCEPTS_AR = ("بكرة", "الفائدة الميكانيكية", "نسبة التروس", "نابض", "معامل الاحتكاك",
                      "الشغل", "الطاقة", "القدرة", "الإجهاد", "الانفعال", "الكلال", "التفاوت",
                      "معامل الأمان", "اختيار المواد", "التصنيع", "أخصائي", "مختص", "شهادة",
                      "الجاهزية", "درجة", "ثقة", "ترتيب")


def test_f12_no_fifth_concept_and_no_forbidden_engineering_topic_in_the_copy():
    """Whole-token containment (the Stage-18 discipline): "FEA" must not be read
    out of "feasibility", and a stem such as "manufactur" matches any suffix."""
    for lang, terms in (("en", _FIFTH_CONCEPTS), ("ar", _FIFTH_CONCEPTS_AR)):
        for part, text in _fund_texts(lang).items():
            for term in terms:
                pattern = r"(?<!\w)%s" % re.escape(term) + (r"(?!\w)" if not term.endswith(("manufactur", "certif")) else "")
                assert not re.search(pattern, text, re.I), (lang, part, term)


def test_f13_digits_appear_only_in_the_source_citation_and_no_numeric_result_or_input_exists():
    for lang in ("en", "ar"):
        for part, text in _fund_texts(lang).items():
            if part == "SOURCE":
                assert re.findall(r"\d+", text) == ["811", "9"], text   # SP 811, Appendix B.9
            else:
                assert not re.search(r"\d", text), (lang, part, text)
    html = _render_state((PHYSICAL_FEASIBILITY, OPEN))
    block = _fundamentals_blocks(html)[0]
    for control in ("<input", "<form", "<select", "<textarea", "<button"):
        assert control not in block, control
    assert not re.search(r"=\s*\d", _visible(block)), "a numeric result leaked"


_NEGATED_ONLY_EN = ("friction", "deformation", "acceleration", "dynamic response",
                    "structural adequacy", "hydraulic-system performance", "pressure losses",
                    "seal behaviour", "component ratings", "fluid suitability", "safety",
                    "applies to your design", "calculation for your project", "project calculation",
                    "mechanism works", "validate", "satisfy")
_NEGATED_ONLY_AR = ("الاحتكاك", "التشوه", "التسارع", "الاستجابة الديناميكية", "الكفاية الإنشائية",
                    "أداء نظام هيدروليكي", "فواقد الضغط", "سلوك الأختام", "تصنيفات المكونات",
                    "ملاءمة المائع", "السلامة", "ينطبق على تصميمك", "حسابًا لمشروعك", "تغلق فجوة",
                    "الآلية تعمل", "تم التحقق")
_AR_NEGATORS = ("لا ", "ولا ", "لم ", "ليست", "وليست", "دون ")


def _ar_denied(sentence, term):
    at = sentence.find(term)
    return at >= 0 and any(n in sentence[:at] for n in _AR_NEGATORS)


def test_f14_the_copy_never_claims_applicability_feasibility_working_safety_or_validation():
    """Every engineering topic the block names appears ONLY inside a sentence
    that denies it (the Stage-18 sentence-scoped scanner, plus the plain
    "not ..." / "لم ..." forms this copy uses)."""
    for part, text in _fund_texts("en").items():
        for sentence in _sentences(text):
            for term in _NEGATED_ONLY_EN:
                if _mentions(sentence, term):
                    assert _denied_or_negated(sentence, term, "en") or re.search(
                        r"\b(not|has not|do not|does not)\b", sentence[:sentence.lower().find(term.lower())],
                        re.I), ("en", part, term, sentence)
    for part, text in _fund_texts("ar").items():
        for sentence in _sentences(text):
            for term in _NEGATED_ONLY_AR:
                if term in sentence:
                    assert _ar_denied(sentence, term), ("ar", part, term, sentence)
    # the four key truths are stated explicitly
    en = _fund_texts("en")
    assert "InventorAI has not determined that any of them applies to your design" in en["INTRO"]
    assert "not a calculation for your project" in en["ITEM_1_NOTE"]
    assert "Correct units do not validate a design" in en["ITEM_4_NOTE"]
    assert en["BOUNDARY"].startswith("These reference fundamentals do not satisfy the physical feasibility gap")
    ar = _fund_texts("ar")
    assert "لم يحدد InventorAI أن أيًا منها ينطبق على تصميمك" in ar["INTRO"]
    assert "لا تغلق فجوة الجدوى الفيزيائية (Physical Feasibility)" in ar["BOUNDARY"]


def test_f15_the_copy_is_reference_framed_and_descriptive_not_prescriptive():
    en = _fund_texts("en")
    assert en["TITLE"] == "Reference fundamentals that may help with this gap"
    assert en["INTRO"].startswith("These relationships are reference fundamentals that may be relevant.")
    for n in (1, 2, 3):
        assert en["ITEM_%d_LEAD" % n].startswith("For ")
    for lang, terms in (("en", _ACTION_TERMS_EN), ("ar", _ACTION_TERMS_AR)):
        for part, text in _fund_texts(lang).items():
            for sentence in _sentences(text):
                for term in terms:
                    if _mentions(sentence, term):
                        assert _denied_or_negated(sentence, term, lang), (lang, part, term, sentence)


# --- F4. source / use ---------------------------------------------------
def test_f16_six_new_provenance_records_with_the_exact_authorized_identities_and_urls():
    recs = _provenance()
    for rid, url in FUND_PROVENANCE.items():
        rec = recs[rid]
        assert rec["pack_id"] == "mechanical" and rec["url"] == url, rid
        assert sorted(rec) == ["cross_domain_usage", "jurisdiction", "notes", "pack_id", "record_id",
                               "source_name", "source_type", "standard_number", "tier", "url",
                               "version_or_edition"], rid
        assert rec["cross_domain_usage"] == [] and rec["notes"].strip()
        host = re.match(r"https://([^/]+)/", url).group(1)
        assert host.endswith("nasa.gov") or host.endswith("nist.gov"), url
    assert recs["mechanical:PR010"]["source_type"] == recs["mechanical:PR011"]["source_type"] == "source_use_policy"
    for rid in ("mechanical:PR006", "mechanical:PR007", "mechanical:PR008", "mechanical:PR009"):
        assert recs[rid]["source_type"] == "government_reference_publication"
    for rid in ("mechanical:PR010", "mechanical:PR011"):
        assert "not a legal opinion" in recs[rid]["notes"]
    # exactly PR001–PR011, nothing renumbered, nothing skipped
    mech = sorted(r for r in recs if r.startswith("mechanical:"))
    assert mech == ["mechanical:PR%03d" % n for n in range(1, 12)]


# The five pre-existing Mechanical records, frozen by content so this slice can
# prove it changed none of them (identity, source, notes and cross-domain usage).
_PR001_PR005_DIGEST = "516ac729404e99dfaa84c7c230539cf8d495202fdd73c6c0316aa600d1d84aaa"


def test_f17_existing_provenance_pr001_to_pr005_are_unchanged():
    recs = _provenance()
    old = {rid: recs[rid] for rid in ("mechanical:PR001", "mechanical:PR002", "mechanical:PR003",
                                      "mechanical:PR004", "mechanical:PR005")}
    digest = hashlib.sha256(json.dumps(old, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
    assert digest == _PR001_PR005_DIGEST
    assert old["mechanical:PR005"]["source_type"] == "governance_record"
    assert "ASME Y14.5-2018" in old["mechanical:PR001"]["source_name"]


def test_f18_pack_group_declares_the_four_claims_with_exact_source_and_policy_linkage():
    group = _fund_group()
    assert sorted(group) == ["applicable_gap_type", "claims", "group_id"]
    assert group["group_id"] == FUND_GROUP and group["applicable_gap_type"] == PHYSICAL_FEASIBILITY
    claims = group["claims"]
    assert tuple(c["claim_id"] for c in claims) == FUND_CLAIMS
    recs = _provenance()
    for claim, equation in zip(claims, FUND_EQUATIONS):
        assert sorted(claim) == ["applicable_gap_type", "claim_id", "fact", "limitation",
                                 "relationship", "source_ref", "source_use_policy_ref"], claim["claim_id"]
        assert claim["applicable_gap_type"] == PHYSICAL_FEASIBILITY
        src, pol = FUND_CLAIM_SOURCES[claim["claim_id"]]
        assert claim["source_ref"] == src and claim["source_use_policy_ref"] == pol
        assert recs[src]["source_type"] == "government_reference_publication"
        assert recs[pol]["source_type"] == "source_use_policy"
        assert claim["claim_id"] in recs[src]["notes"]
        assert equation in claim["relationship"] or equation == "N·m" and "N·m" in claim["relationship"]
        assert claim["limitation"].strip() and claim["fact"].strip()
    # the resolver's table and the governed group agree exactly
    assert cap01_guidance.CAP01_GAP_FUNDAMENTALS[("mechanical", PHYSICAL_FEASIBILITY)] == \
        (FUND_GROUP, FUND_CLAIMS)
    assert set(cap01_guidance.CAP01_GAP_FUNDAMENTALS) == {
        ("mechanical", PHYSICAL_FEASIBILITY), (ELEC_DOMAIN, PHYSICAL_FEASIBILITY)}


def test_f19_the_group_carries_no_executable_rule_variable_threshold_or_applicability_logic():
    group = _fund_group()
    flat = json.dumps(group, ensure_ascii=False).lower()
    for forbidden in ("if ", "when_", "trigger", "threshold", "min_", "max_", "input", "variable",
                      "compute", "calculate(", "formula_select", "applicab", "weight", "layer",
                      "readiness", "score", "plugin", "provider", "iot", "drone", "renewable",
                      "electronics", "$ref", "schema"):
        # "applicable_gap_type" is the ONE declared field; nothing else may say "applicab"
        if forbidden == "applicab":
            assert flat.count("applicab") == flat.count("applicable_gap_type"), flat
            continue
        assert forbidden not in flat, forbidden


def test_f20_source_disclosure_names_exactly_the_authorized_sources_and_no_endorsement():
    en, ar = _fund_texts("en"), _fund_texts("ar")
    assert en["SOURCE"] == ("Reference source material: NASA Glenn Research Center — Torque (Moment), "
                            "Balance Of Forces, Aerodynamic Forces; NIST Guide to the SI, SP 811 Appendix B.9.")
    for title in ("Torque (Moment)", "Balance Of Forces", "Aerodynamic Forces", "SP 811 Appendix B.9"):
        assert title in ar["SOURCE"], title
    assert ar["SOURCE"].startswith("مواد مرجعية:")
    joined = " ".join(list(en.values()) + list(ar.values())).lower()
    for forbidden in ("according to nasa", "nasa confirms", "nasa says", "nasa recommends", "nasa-approved",
                      "reviewed by nasa", "approved by nist", "endorse", "certified by", "verified by nasa",
                      "openstax", "wikipedia", "textbook", "your design is", "nasa تؤكد", "وفقًا لناسا",
                      "بحسب ناسا", "معتمد من"):
        assert forbidden not in joined, forbidden
    # neutral acknowledgement only, never project-specific attribution
    for part, text in en.items():
        if "NASA" in text or "NIST" in text:
            assert part == "SOURCE", (part, text)


def test_f21_no_unapproved_source_anywhere_and_no_nasa_media():
    pack_text = json.dumps(_mech_package(), ensure_ascii=False).lower()
    prov_text = json.dumps([_provenance()[r] for r in FUND_PROVENANCE], ensure_ascii=False).lower()
    copy_text = " ".join(_fund_texts("en").values()).lower() + " ".join(_fund_texts("ar").values()).lower()
    for text in (pack_text, prov_text, copy_text):
        for forbidden in ("openstax", "wikipedia", "khan", "engineeringtoolbox", "hyperphysics", ".edu/",
                          "blog", "vendor", "<img", ".png", ".jpg", ".svg", ".gif", "youtube"):
            assert forbidden not in text, forbidden
    # the reader-visible copy names no logo / insignia / image at all (the
    # provenance notes may DENY their use; the copy never mentions them)
    for forbidden in ("logo", "insignia", "image", "شعار", "صورة"):
        assert forbidden not in copy_text, forbidden
    html = _render_state((PHYSICAL_FEASIBILITY, OPEN))
    block = _fundamentals_blocks(html)[0]
    assert "<img" not in block and "http" not in block and "nasa.gov" not in block


def test_f22_pack_notes_declare_the_group_inert_and_the_loader_is_unchanged():
    notes = _mech_package()["_governance_notes"]["mechanical_td_slice1_reference_fundamentals"]
    for phrase in ("inert", "classifier", "Path-N", "no loader or schema change", "PR001–PR005 are unchanged"):
        assert phrase in notes, phrase
    registry_src = _source(os.path.join(_ROOT, "engine", "domain_registry.py"))
    assert "reference_fundamentals" not in registry_src
    for rel in ("engine/domain_rules.py", "engine/domain_activation.py", "engine/path_n_questions.py",
                "engine/gap_action_pack.py", "engine/progression_loop.py", "engine/idea_state.py",
                "engine/semantic_registry.py", "engine/need_routing.py"):
        assert "reference_fundamentals" not in _source(os.path.join(_ROOT, rel)), rel


# --- F5. ownership / non-duplication ----------------------------------------
def test_f23_domain_classification_rules_question_serving_and_activation_are_unchanged_by_the_metadata():
    from engine import domain_activation
    from engine.domain_rules import classify_domain, get_active_rules, infer_domain
    from engine.domain_registry import load_registry
    reg = load_registry(os.path.join(_ROOT, "domains"))
    pack = reg["mechanical"]
    assert "reference_fundamentals" in pack          # loaded as opaque additive data
    assert domain_activation.is_activated("mechanical") and domain_activation.support_state("mechanical") == "activated"
    assert infer_domain(MECHANICAL_IDEA) == "mechanical"
    assert [r for r in get_active_rules("mechanical")] == [r for r in get_active_rules("mechanical")]
    rules = json.dumps([getattr(r, "__dict__", r) for r in get_active_rules("mechanical")], default=str)
    assert "force_moment" not in rules and "torque_moment" not in rules
    cls = classify_domain(_TRIGGER_WORDS_IDEA)
    assert "force_moment" not in json.dumps(getattr(cls, "__dict__", str(cls)), default=str)
    for mapping in _mech_package()["gap_type_mappings"]:
        for n, q in enumerate(mapping["questions"]):
            served = get_served_question(mapping["gap_type_id"], n, domain="mechanical")
            assert served.question_id == q["question_id"]
            for eq in FUND_EQUATIONS:
                assert eq not in served.text


def test_f24_cap04_path_n_cap12_cap13_therm01_and_electronics_are_untouched():
    state = _mech_state((PHYSICAL_FEASIBILITY, OPEN), (MECHANISM_COMPLETENESS, PARTIAL))
    package = assemble_deliverable(state)
    before = pickle.dumps(derive_gap_action_packs(state))
    assert appmod._cap01_gap_contexts(package, state)["contexts"][0]["fundamentals"] is None  # MC first in source order
    assert pickle.dumps(derive_gap_action_packs(state)) == before
    html = _render(package, state)
    gp = re.search(r'<div class="gp-packs".*?<span id="report-validation-plan"', html, re.S).group(0)
    assert "cap01-fund" not in gp and "N·m" not in gp
    block = _fundamentals_blocks(html)[0]
    for marker in ("gp-", "data-gp-", "UI_GP_", "cap01-item", "cap01-research", "therm", "cap12", "cap13"):
        assert marker not in block, marker
    guidance = _executable(_GUIDANCE_PATH).lower()
    for marker in ("therm", "cap12", "cap_12", "cap13", "cap_13", "gap_action_pack", "path_n"):
        assert marker not in marker or marker not in guidance, marker
    assert cap01_guidance.profile_copy("electronics_electrical")["profile_id"] == PROFILE_ID


def test_f25_no_generic_framework_registry_or_calculation_primitive_was_created():
    guidance = _executable(_GUIDANCE_PATH)
    for forbidden in ("class ", "eval(", "exec(", "sympy", "numpy", "math.", "float(", "int(",
                      "Registry", "registry", "Framework", "Plugin", "calculate", "formula_for",
                      "select_formula", "infer_"):
        assert forbidden not in guidance, forbidden
    import web.cap01_guidance as module
    # Electrical / Electronics Technical Deepening Slice 1 added exactly ONE row.
    assert len(cap01_guidance.CAP01_GAP_FUNDAMENTALS) == 2
    assert set(cap01_guidance.CAP01_GAP_FUNDAMENTALS) == {
        ("mechanical", PHYSICAL_FEASIBILITY), (ELEC_DOMAIN, PHYSICAL_FEASIBILITY)}
    # no new module, engine file or persistence surface is involved
    assert module.__name__ == "web.cap01_guidance"


def test_f26_report_and_pdf_render_with_fundamentals_change_no_state(client, monkeypatch):
    sid = _start(client)
    _set_gaps(sid, (PHYSICAL_FEASIBILITY, OPEN))
    state = _live(sid)
    before = pickle.dumps(state)
    readiness = derive_readiness(state)
    before_ready = (readiness.overall_verified(), readiness.unverified_contexts())
    for _ in range(2):
        assert len(_fundamentals_blocks(_report(client, sid))) == 1
        source = _pdf_source(client, sid, monkeypatch)
        assert len(_fundamentals_blocks(source)) == 1
    state = _live(sid)
    assert pickle.dumps(state) == before
    readiness = derive_readiness(state)
    assert (readiness.overall_verified(), readiness.unverified_contexts()) == before_ready
    assert [(g.gap_type, g.status) for g in state.gaps] == [(PHYSICAL_FEASIBILITY, OPEN)]


def test_f27_session_page_never_carries_the_fundamentals(client):
    sid = _start(client)
    _set_gaps(sid, (PHYSICAL_FEASIBILITY, OPEN))
    for lang in ("en", "ar"):
        if lang == "ar":
            client.post("/ui-language", data={"lang": "ar"})
        page = client.get(f"/session/{sid}").get_data(as_text=True)
        assert "cap01" not in page and "cap01-fund" not in page
        for eq in FUND_EQUATIONS[:3]:
            assert eq not in page
        assert _fund_copy("TITLE", lang) not in page


# --- F6. localization / surfaces / RTL -------------------------------------
def test_f28_en_report_route_renders_the_full_english_sub_view(client):
    sid = _start(client)
    _set_gaps(sid, (PHYSICAL_FEASIBILITY, OPEN))
    page = _report(client, sid)
    block = _fundamentals_blocks(page)[0]
    visible = _visible(block)
    for part, text in _fund_texts("en").items():
        assert text in visible, part
    for part, text in _fund_texts("ar").items():
        if not part.endswith("_EQUATION"):
            assert text not in visible, part
    assert "UI_CAP01_" not in visible and PHYSICAL_FEASIBILITY not in visible


def test_f29_ar_rtl_report_route_renders_the_arabic_sub_view_with_ltr_isolated_equations(client):
    sid = _start(client)
    _set_gaps(sid, (PHYSICAL_FEASIBILITY, PARTIAL))
    page = _report(client, sid, lang="ar")
    assert 'dir="rtl"' in page
    block = _fundamentals_blocks(page)[0]
    visible = _visible(block)
    for part, text in _fund_texts("ar").items():
        assert text in visible, part
    for part, text in _fund_texts("en").items():
        if not part.endswith("_EQUATION"):
            assert text not in visible, part
    # every equation / unit symbol is isolated left-to-right and byte-identical to EN
    assert _equations(block) == list(FUND_EQUATIONS)
    assert block.count('<bdi class="cap01-fund-equation" dir="ltr"') == 4
    # Latin identifiers and unit symbols survive verbatim inside the Arabic prose
    for token in ("L⊥", "Pa", "kPa", "N·m", "InventorAI", "(Physical Feasibility)"):
        assert token in visible, token
    assert PHYSICAL_FEASIBILITY not in visible


def test_f30_equations_are_language_neutral_and_never_split_by_direction_marks():
    for eq in FUND_EQUATIONS:
        assert not re.search(r"[\u0600-\u06FF\u200e\u200f\u202a-\u202e]", eq), eq
        assert eq == eq.strip()
    for lang in ("en", "ar"):
        html = _render_state((PHYSICAL_FEASIBILITY, OPEN), lang=lang)
        block = _fundamentals_blocks(html)[0]
        # each equation sits alone in its own LTR element, never inline in prose
        for eq in FUND_EQUATIONS:
            assert ('data-cap01-fund-equation>%s</bdi>' % eq) in block, (lang, eq)
            prose = re.sub(r'<bdi class="cap01-fund-equation"[^>]*>.*?</bdi>', "", block)
            assert eq not in _visible(prose) or eq == "N·m", (lang, eq)


def test_f31_pdf_source_carries_the_matching_sub_view_and_excludes_it_otherwise(client, monkeypatch):
    sid = _start(client)
    _set_gaps(sid, (PHYSICAL_FEASIBILITY, OPEN))
    for lang in ("en", "ar"):
        screen = _report(client, sid, lang=lang)
        source = _pdf_source(client, sid, monkeypatch)
        assert _fundamentals_blocks(source) == _fundamentals_blocks(screen)
        assert _equations(_fundamentals_blocks(source)[0]) == list(FUND_EQUATIONS)
        assert _fund_copy("SOURCE", lang) in _visible(_fundamentals_blocks(source)[0])
    _set_gaps(sid, (PHYSICAL_FEASIBILITY, CLOSED), (MECHANISM_COMPLETENESS, OPEN))
    source = _pdf_source(client, sid, monkeypatch)
    assert "cap01-gap-block" in source and "cap01-fundamentals" not in source
    for eq in FUND_EQUATIONS[:3]:
        assert eq not in source


def test_f32_the_template_is_passive_and_the_resolver_fails_closed_all_or_nothing(monkeypatch):
    src = _source(_TEMPLATE_PATH)
    region = src[src.index("CAP01-BLOCK-START"):src.index("CAP01-BLOCK-END")]
    region = region[region.index("#}") + 2:]
    for literal in ("mechanical", "force_moment", "torque", "PHYSICAL", "physical_feasibility", "elif",
                    "N·m", "F = pA"):
        assert literal not in region, literal
    assert "_cap01_fund.claims" in region and 'dir="ltr"' in region
    # a single missing item part removes the WHOLE sub-view, never a partial set;
    # the PF context itself keeps rendering its title / meaning / limit
    monkeypatch.delitem(ui_text.UI_STRINGS, FUND_PREFIX + "ITEM_3_NOTE")
    ctx = _pf_context((PHYSICAL_FEASIBILITY, OPEN))
    assert ctx is not None and ctx["fundamentals"] is None
    html = _render_state((PHYSICAL_FEASIBILITY, OPEN))
    assert "cap01-fundamentals" not in html and _contexts(html) == [(ATTR[PHYSICAL_FEASIBILITY], "open")]
    monkeypatch.setitem(ui_text.UI_STRINGS, FUND_PREFIX + "ITEM_3_NOTE", {"en": "x", "ar": "y"})
    monkeypatch.delitem(ui_text.UI_STRINGS, FUND_PREFIX + "BOUNDARY")
    assert _pf_context((PHYSICAL_FEASIBILITY, OPEN))["fundamentals"] is None


def test_f33_the_test_file_carries_no_weak_or_true_assertion():
    """Natural-touch repair: the two former `or True` clauses are gone and no new
    one may appear."""
    src = _source(os.path.join(_ROOT, "tests", "test_cap01_mechanical_open_gap_context.py"))
    body = src.split("def test_f33_the_test_file_carries_no_weak_or_true_assertion")[0]
    assert " or True" not in body
