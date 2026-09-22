# -*- coding: utf-8 -*-
"""Stage 18 / CAP-01 — first deterministic bounded guidance increment.

What is pinned here is ONE additive, presentation-only advisory block on the
deliverable, and the boundaries that make it truthful:

  * PROFILE SEAM — a trusted canonical domain id resolves, through ONE small
    data-driven table in ``web/cap01_guidance.py``, to an AUTHORIZED CAP-01
    guidance profile or to nothing. ``electronics_electrical`` is the FIRST
    authorized profile, not the permanent definition of CAP-01. Adding a future,
    separately-authorized profile is one table row plus its own copy keys and
    requires no core-engine change.
  * AVAILABILITY IS NOT TRANSLATION — ``ui_text`` owns the EN/AR copy and nothing
    else; ``cap01_guidance`` owns which domains have a profile and what parts it
    renders. The first draft put both in the string catalogue, which would have
    made the localization module the capability owner.
  * TODAY'S SINGLE DOMAIN IS A LIMITATION, NOT THE MODEL — the resolver consumes
    the canonical capability rows as a COLLECTION. The first draft read ``[0]``,
    which would have hardened the current runtime shape into CAP-01 architecture.
    Consuming a collection claims no multi-domain support and creates none.
  * DOMAIN ACTIVATION IS NOT PROFILE AVAILABILITY — ``mechanical`` is a fully
    activated InventorAI domain with no CAP-01 profile. Absence of a profile
    renders nothing and never means unsupported / invalid / not-activated.
  * CONDITIONAL, CLASS-GENERAL COPY ONLY — the block never asserts that the
    reader's project belongs to the interface concept class, never claims to
    have inspected the record, never says a field is present or missing, and
    carries no numeric value, threshold, compatibility verdict, safety verdict,
    conditioning recommendation, specialist classification or named
    vendor/product/tool/laboratory/standard.
  * BOUNDED EN/AR EXCEPTION — the Owner elected bilingual copy for this ONE
    block through the existing ``ui_lang`` / ``t()`` seam. Exactly one language
    renders, and the general Category-C English-only rule is otherwise intact.
  * NOTHING ELSE MOVES — no canonical deliverable section, no package/state/gap/
    evidence/readiness mutation, no schema, no persistence, no AI/provider.

Every assertion below is a named, individually failing proof obligation; the
numbering follows the authorizing instruction's required-test matrix §W 1..20.
"""
import ast
import copy
import html as html_module
import io
import os
import re

import pytest

from engine import domain_activation
from engine.deliverable_assembler import assemble_deliverable
from engine.domain_rules import infer_domain
from engine.idea_state import IdeaState
from engine.progression_loop import run_iteration
from web import cap01_guidance, ui_text
from web.app import app as _flask_app

_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
_UI_TEXT_PATH = os.path.join(_ROOT, "web", "ui_text.py")
_GUIDANCE_PATH = os.path.join(_ROOT, "web", "cap01_guidance.py")
_APP_PATH = os.path.join(_ROOT, "web", "app.py")
_TEMPLATE_PATH = os.path.join(_ROOT, "web", "templates", "deliverable.html")

# The first (and only) authorized CAP-01 profile.
PROFILE_ID = "CAP01_ELECTRONICS_INTERFACE_V1"
PROFILE_DOMAIN = "electronics_electrical"

# The canonical top-level deliverable sections. CAP-01 adds none of these.
CANONICAL_SECTION_KEYS = (
    "section_1_disclaimer", "section_2_invention_summary",
    "section_3_assessment_overview", "section_4_requirements",
    "section_5_assumptions", "section_6_risks", "section_7_recommendations",
    "section_8_unresolved_items", "section_9_stage3_reasoning",
    "section_10_recommended_next_steps", "section_11_prototype_test_plan",
    "section_12_next_development_step", "section_13_requirement_landscape",
    "section_14_validation_plan",
)

# The deterministic core that must stay free of CAP-01 vocabulary (§C).
CORE_FILES = (
    "engine/progression_loop.py", "engine/idea_state.py",
    "engine/domain_rules.py", "engine/domain_activation.py",
    "engine/semantic_registry.py", "engine/deliverable_assembler.py",
    "engine/requirement_landscape.py", "engine/validation_plan.py",
)

ELECTRONICS_IDEA = "IoT greenhouse temperature sensor with relay control"
MECHANICAL_IDEA = "A folding mechanical wheelchair ramp with a spring latch"
OPEN_GAP_INPUT = "Growers lose crops because greenhouse monitoring is manual"


# ==========================================================================
# harness — committed public API only; no fixture is created or mutated
# ==========================================================================
def _state(idea, *inputs):
    s = IdeaState(idea_id="s18-" + str(abs(hash(idea)) % 10_000_000))
    s.domain = infer_domain(idea)
    s.domain_signal = s.domain
    for text in inputs:
        run_iteration(s, text)
    return s


def _open_gap_state(idea=ELECTRONICS_IDEA):
    """A state carrying at least one canonical OPEN gap (the third display fact)."""
    s = _state(idea, OPEN_GAP_INPUT)
    assert _package(s)["section_3_assessment_overview"][
        "capabilities_assessed"][0]["gaps_open"] >= 1
    return s


def _closed_gap_state(idea=ELECTRONICS_IDEA):
    """A state whose canonical open-gap count is zero, so the third display fact
    is not satisfied and the block must not render."""
    s = _state(idea, OPEN_GAP_INPUT,
               "A sensor reports a reading to a controller which switches an actuator",
               "Operating range and enclosure are fixed by the grower's shed",
               "One zone, standalone, no network dependency")
    assert _package(s)["section_3_assessment_overview"][
        "capabilities_assessed"][0]["gaps_open"] == 0
    return s


def _package(state):
    return assemble_deliverable(state)


def _render(package, lang="en", pdf=False, **extra):
    """Render the REAL committed deliverable template in ONE selected language."""
    from flask import session as flask_session
    kwargs = dict(package=package, sid="s18probe",
                  eligible=package["_session_meta"]["deliverable_eligible"],
                  t2a_statements={}, evidence_references=[],
                  decision_capture=None, snapshot_kept_ack=None)
    kwargs.update(extra)
    if pdf:
        kwargs["deliverable_base"] = "pdf_base.html"
    with _flask_app.test_request_context("/"):
        flask_session["ui_lang"] = lang
        return _flask_app.jinja_env.get_template("deliverable.html").render(**kwargs)


_BLOCK_RE = re.compile(
    r'<div class="cap01-block"[^>]*>(?P<body>.*?)</div>', re.S)


def _block(html):
    """The rendered CAP-01 block, or None when it did not render."""
    m = _BLOCK_RE.search(html)
    return m.group(0) if m else None


def _visible(block):
    """Reader-visible text of the block: markup stripped, entities resolved."""
    text = re.sub(r"<[^>]+>", " ", block)
    return re.sub(r"\s+", " ", html_module.unescape(text)).strip()


def _items(block):
    return re.findall(r"<li class=\"cap01-item\" data-cap01-item>(.*?)</li>", block, re.S)


def _research_items(block):
    return re.findall(r"<li class=\"cap01-research-item\" data-cap01-research-item>(.*?)</li>",
                      block, re.S)


def _parts(block):
    """The block's reader-visible copy, one entry per rendered part. Scanning per
    part rather than over the flattened block keeps a claim attributable to the
    paragraph that makes it, so a boundary sentence cannot launder a claim made
    somewhere else in the block."""
    parts = {name: _visible(m.group(1)) for name, m in
             ((n, re.search(r"<[^>]*data-cap01-%s[^>]*>(.*?)</[a-z0-9]+>" % n, block, re.S))
              for n in ("title", "intro", "boundary", "limit", "evidence"))
             if m}
    assert set(parts) == {"title", "intro", "boundary", "limit", "evidence"}, sorted(parts)
    for n, item in enumerate(_items(block), 1):
        parts["item_%d" % n] = _visible(item)
    # The research-direction group is scanned by the SAME boundary checks: a claim
    # smuggled into "where to look" is exactly as false as one in the checklist.
    for n in ("research-title", "research-intro"):
        m = re.search(r"<[^>]*data-cap01-%s[^>]*>(.*?)</[a-z0-9]+>" % n, block, re.S)
        if m:
            parts[n.replace("-", "_")] = _visible(m.group(1))
    for n, item in enumerate(_research_items(block), 1):
        parts["research_item_%d" % n] = _visible(item)
    return parts


# Negation markers. A forbidden term is acceptable ONLY inside a sentence that
# explicitly denies it ("it does not determine compatibility"); a bare mention is
# a violation. This is the difference between a truthful boundary statement and a
# claim, so the scan is sentence-scoped rather than a document-wide substring test.
_NEGATORS_EN = ("does not", "do not", "is not", "are not", "cannot", "never",
                "not determine", "not inspect", "and are not", "are not ")
_NEGATORS_AR = ("لا ", "ولا ", "ليست", "وليست", "دون ")


def _sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.؟!])\s+|\n", text) if s.strip()]


def _mentions(sentence, term):
    """Whole-token containment. A bare substring test reads "is present" out of
    "InventorAI is presenting", which would make this scan lie in both directions."""
    return re.search(r"(?<!\w)%s(?!\w)" % re.escape(term), sentence, re.I) is not None


def _denied(sentence, term, lang):
    """True only when a negator appears BEFORE the term in the same sentence.

    Position matters. "They are manufacturer verified, ..., not primary-verified"
    contains a negator, but it denies something else — the claim still stands. A
    negator that merely co-occurs would let any forbidden claim buy immunity by
    appending an unrelated denial, so the scan requires the denial to govern the
    term it is excusing."""
    negators = _NEGATORS_AR if lang == "ar" else _NEGATORS_EN
    at = re.search(r"(?<!\w)%s(?!\w)" % re.escape(term), sentence, re.I)
    if at is None:
        return True
    head = sentence[:at.start()].lower()
    return any(n in head for n in negators)


def _offenders(block, term, lang):
    """Sentences that MENTION ``term`` without denying it, across every part of the
    rendered block. An empty list is the proof that the term is only ever negated."""
    return [sentence
            for text in _parts(block).values()
            for sentence in _sentences(text)
            if _mentions(sentence, term) and not _denied(sentence, term, lang)]


_CSRF_RE = re.compile(r'(name="csrf_token" value=")[^"]*(")')


def _mask_csrf(html):
    """Blank the per-render CSRF token values. They are freshly minted on every
    render and are the only legitimate byte-level difference between two renders
    of the same package, so masking them is what makes an identity comparison
    meaningful rather than always-false."""
    return _CSRF_RE.sub(r"\1MASKED\2", html)


def _code(path):
    """A file's EXECUTABLE text: comments and docstrings stripped.

    A scan for a construct must not be satisfied \u2014 or defeated \u2014 by prose
    describing the construct the code deliberately avoids. The ``[0]`` scan below
    failed exactly that way against the comment explaining why ``[0]`` is wrong."""
    tree = ast.parse(_source(path))
    for node in ast.walk(tree):
        if (isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant)
                and isinstance(node.value.value, str)):
            node.value.value = ""
    return ast.unparse(tree)


def _source(path):
    with io.open(path, encoding="utf-8") as fh:
        return fh.read()


def _template_cap01_region():
    """The EXECUTABLE CAP-01 template region — the explanatory Jinja comment is
    excluded so a scan for branching or domain literals reads the markup that
    actually runs, not prose describing what the markup deliberately avoids."""
    src = _source(_TEMPLATE_PATH)
    start = src.index("CAP01-BLOCK-START")
    start = src.index("#}", start) + 2
    return src[start:src.index("{#- CAP01-BLOCK-END", start)]


# ==========================================================================
# 0. THE BOUNDARY SCANNER ITSELF  (negative control)
# ==========================================================================
def test_00a_the_boundary_scanner_accepts_a_genuine_denial():
    """The copy's real boundary sentences must not read as violations."""
    for sentence, term in (
            ("It does not determine compatibility, safe limits or circuit correctness.",
             "compatibility"),
            ("InventorAI does not inspect your record to decide which of these "
             "items are present or missing.", "is present"),
            ("They are based on corroborated/reasoned evidence and are not "
             "primary-verified device-specific conclusions.", "primary-verified")):
        assert _denied(sentence, term, "en"), (term, sentence)


def test_00b_the_boundary_scanner_catches_a_claim_that_merely_ends_in_a_denial():
    """A forbidden claim must not buy immunity by appending an unrelated denial,
    and a word may not be read out of the middle of a longer one."""
    assert not _denied("They are manufacturer verified, not primary-verified.",
                       "manufacturer verified", "en")
    assert not _denied("The design is compatible with your microcontroller.",
                       "compatible", "en")
    assert not _mentions("InventorAI is presenting a class-general checklist.",
                         "is present")
    assert _mentions("The ADC reference is present in the datasheet.", "is present")


def test_00c_the_arabic_scanner_is_not_blind():
    assert _denied("لا يحدد النظام التوافق.", "التوافق", "ar")
    assert not _denied("يحدد النظام التوافق.", "التوافق", "ar")


# ==========================================================================
# 1. ELECTRONICS PROFILE AVAILABILITY
# ==========================================================================
def test_01_electronics_domain_resolves_to_an_authorized_cap01_profile():
    """The first authorized profile exists for the canonical electronics domain,
    and the lookup returns its complete, ordered copy-key view."""
    assert cap01_guidance.profile_for_domain(PROFILE_DOMAIN) == PROFILE_ID
    view = cap01_guidance.profile_copy(PROFILE_DOMAIN)
    assert view is not None
    assert view["profile_id"] == PROFILE_ID
    assert view["item_keys"] == tuple(
        "UI_%s_ITEM_%d" % (PROFILE_ID, n) for n in range(1, 7))
    for part in ("title_key", "intro_key", "boundary_key", "limit_key", "evidence_key"):
        assert view[part] in ui_text.UI_STRINGS


def test_01b_lookup_returns_keys_not_text_so_one_language_is_chosen_downstream():
    """The seam hands back CATALOGUE KEYS only. If it returned resolved copy it
    could smuggle a second language past the ``t()`` / ``ui_lang`` boundary."""
    view = cap01_guidance.profile_copy(PROFILE_DOMAIN)
    resolved = [v for v in view.values() if isinstance(v, str)] + list(view["item_keys"])
    for value in resolved:
        assert value == PROFILE_ID or value.startswith("UI_CAP01_"), value


# ==========================================================================
# 2. ELECTRONICS + OPEN GAP  ->  the block renders
# ==========================================================================
def test_02_block_renders_for_electronics_with_at_least_one_open_gap():
    html = _render(_package(_open_gap_state()))
    block = _block(html)
    assert block is not None, "CAP-01 block did not render on the authorized path"
    assert 'data-cap01-profile="%s"' % PROFILE_ID in block
    assert len(_items(block)) == 6
    for part in ("title", "intro", "boundary", "limit", "evidence"):
        assert "data-cap01-%s" % part in block


def test_02b_block_renders_the_owner_approved_copy_not_a_fallback_key():
    """A missing catalogue entry would leak the raw key as visible text."""
    block = _block(_render(_package(_open_gap_state())))
    assert "UI_CAP01_" not in _visible(block)


# ==========================================================================
# 3. ELECTRONICS + NO OPEN GAP  ->  absent
# ==========================================================================
def test_03_block_is_absent_for_electronics_with_no_open_gap():
    """Profile availability alone never renders the block; the canonical open-gap
    fact is a separate, required condition."""
    html = _render(_package(_closed_gap_state()))
    assert _block(html) is None
    assert "cap01-block" not in html and "data-cap01" not in html


# ==========================================================================
# 4. MECHANICAL — activated domain, no CAP-01 profile, nothing else changed
# ==========================================================================
def test_04a_mechanical_remains_an_activated_inventorai_domain():
    assert domain_activation.is_activated("mechanical")
    assert "mechanical" in domain_activation.activated_domains()
    assert domain_activation.support_state("mechanical") == "activated"


def test_04b_no_cap01_block_renders_on_a_mechanical_deliverable():
    """Neither the electronics profile nor any Mechanical profile appears: no
    Mechanical CAP-01 knowledge profile is authorized in this increment."""
    html = _render(_package(_open_gap_state(MECHANICAL_IDEA)))
    assert _block(html) is None
    assert "cap01-block" not in html and "data-cap01" not in html
    assert PROFILE_ID not in html


def test_04c_mechanical_page_is_byte_identical_with_and_without_the_cap01_seam(monkeypatch):
    """The strongest available statement of "Mechanical behavior is unchanged":
    with the profile lookup forced to return nothing at all, the rendered
    Mechanical deliverable is IDENTICAL. CAP-01 contributes literally no bytes."""
    package = _package(_open_gap_state(MECHANICAL_IDEA))
    with_seam = _mask_csrf(_render(package))
    monkeypatch.delitem(cap01_guidance.CAP01_PROFILE_BY_DOMAIN, PROFILE_DOMAIN)
    assert cap01_guidance.profile_copy(PROFILE_DOMAIN) is None, "guard: seam is off"
    without_seam = _mask_csrf(_render(package))
    assert with_seam == without_seam


def test_04d_absence_of_a_profile_emits_no_unsupported_domain_wording():
    """An absent CAP-01 profile must mean ONLY "no profile authorized yet". It may
    never be rendered as unsupported / invalid / not activated / failed."""
    html = _visible(_render(_package(_open_gap_state(MECHANICAL_IDEA))))
    for claim in ("domain unsupported", "unsupported domain", "domain is not supported",
                  "domain invalid", "invalid domain", "domain not activated",
                  "domain failed", "domain incomplete"):
        assert claim.lower() not in html.lower(), claim


# ==========================================================================
# 5. UNPROFILED BUT RECOGNIZED DOMAIN
# ==========================================================================
@pytest.mark.parametrize("domain_id", ("mechanical", "medical_device", "software"))
def test_05_recognized_domain_without_a_profile_returns_no_profile(domain_id):
    """No profile is a CAP-01 fact only. It must not disturb the domain's own
    support state, which keeps exactly the value it had before this increment."""
    assert cap01_guidance.profile_for_domain(domain_id) is None
    assert cap01_guidance.profile_copy(domain_id) is None
    assert domain_activation.support_state(domain_id) in (
        "activated", "recognized_not_activated")


# ==========================================================================
# 6. UNSUPPORTED / UNKNOWN DOMAIN
# ==========================================================================
def test_06_unknown_domain_has_no_profile_and_keeps_its_existing_support_state():
    assert cap01_guidance.profile_copy("zzz_not_a_domain") is None
    assert domain_activation.support_state("zzz_not_a_domain") == "unknown_or_unsupported"


def test_06b_unknown_domain_renders_no_block():
    state = _open_gap_state()
    state.domain_signal = "zzz_not_a_domain"
    assert _block(_render(_package(state))) is None


# ==========================================================================
# 7. NULL / MISSING DOMAIN
# ==========================================================================
@pytest.mark.parametrize("value", (None, "", "   ", 17, [], {}, object()))
def test_07_missing_or_non_string_domain_yields_no_profile_and_never_raises(value):
    assert cap01_guidance.profile_for_domain(value) is None
    assert cap01_guidance.profile_copy(value) is None


def test_07b_missing_domain_renders_no_block():
    state = _open_gap_state()
    state.domain_signal = None
    assert _block(_render(_package(state))) is None


# ==========================================================================
# 8. FUTURE EXTENSIBILITY SEAM  (the seam, not a fake production profile)
# ==========================================================================
def test_08a_profile_selection_is_table_driven_not_hard_coded_branching(monkeypatch):
    """A future, separately-authorized profile is ONE table row plus its own copy
    keys. Proven against a TEST-LOCAL probe that is torn down with the test — no
    production future profile is created, and no core-engine file is touched."""
    probe_domain, probe_id = "seam_probe_domain", "CAP01_SEAM_PROBE"
    prefix = "UI_%s_" % probe_id
    monkeypatch.setitem(cap01_guidance.CAP01_PROFILE_BY_DOMAIN, probe_domain, probe_id)
    for part in ("TITLE", "INTRO", "BOUNDARY", "LIMIT", "EVIDENCE", "ITEM_1", "ITEM_2"):
        monkeypatch.setitem(ui_text.UI_STRINGS, prefix + part,
                            {"en": "probe " + part, "ar": "probe " + part})
    view = cap01_guidance.profile_copy(probe_domain)
    assert view is not None and view["profile_id"] == probe_id
    assert view["item_keys"] == (prefix + "ITEM_1", prefix + "ITEM_2")
    assert cap01_guidance.profile_copy(PROFILE_DOMAIN)["profile_id"] == PROFILE_ID


def test_08b_the_probe_leaves_no_residue_and_no_unused_future_row_is_shipped():
    assert tuple(cap01_guidance.CAP01_PROFILE_BY_DOMAIN) == (PROFILE_DOMAIN,)
    assert not [k for k in ui_text.UI_STRINGS
                if k.startswith("UI_CAP01_") and PROFILE_ID not in k]


def test_08c_an_incomplete_future_profile_fails_closed_rather_than_half_rendering(monkeypatch):
    monkeypatch.setitem(cap01_guidance.CAP01_PROFILE_BY_DOMAIN, "partial_domain", "CAP01_PARTIAL")
    assert cap01_guidance.profile_copy("partial_domain") is None
    monkeypatch.setitem(ui_text.UI_STRINGS, "UI_CAP01_PARTIAL_TITLE", {"en": "t", "ar": "t"})
    assert cap01_guidance.profile_copy("partial_domain") is None


def test_08d_no_cap01_vocabulary_reaches_the_deterministic_core():
    """Adding a future profile must never require editing decision ownership."""
    offenders = [p for p in CORE_FILES
                 if re.search(r"cap.?01", _source(os.path.join(_ROOT, p)), re.I)]
    assert offenders == [], "CAP-01 vocabulary leaked into the core: %s" % offenders


def test_08e_the_rendering_surface_carries_no_domain_literal_or_branch_chain():
    """The ONLY place a CAP-01 domain literal lives is the table in ui_text.py."""
    region = _template_cap01_region()
    for literal in (PROFILE_DOMAIN, "mechanical", "medical_device", "software"):
        assert literal not in region, literal
    assert "elif" not in region


# ==========================================================================
# 9-11. BILINGUAL — one language at a time
# ==========================================================================
_EN_MARK = "Technical information to check"
_AR_MARK = "معلومات فنية للمراجعة"


def test_09_english_selection_renders_the_english_block_only():
    block = _block(_render(_package(_open_gap_state()), lang="en"))
    assert _EN_MARK in block
    assert _AR_MARK not in block


def test_10_arabic_selection_renders_the_arabic_block_only():
    block = _block(_render(_package(_open_gap_state()), lang="ar"))
    assert _AR_MARK in block
    assert _EN_MARK not in block


def test_11_no_render_ever_mixes_the_two_languages():
    """Every CAP-01 key resolves through ``t()``, so each rendered part carries the
    selected language and only that one — never a bilingual pair."""
    package = _package(_open_gap_state())
    for lang, mine, theirs in (("en", "en", "ar"), ("ar", "ar", "en")):
        visible = _visible(_block(_render(package, lang=lang)))
        view = cap01_guidance.profile_copy(PROFILE_DOMAIN)
        keys = [view[p] for p in ("title_key", "intro_key", "boundary_key",
                                  "limit_key", "evidence_key")] + list(view["item_keys"])
        keys += [view["research"]["title_key"], view["research"]["intro_key"]]
        keys += list(view["research"]["item_keys"])
        for key in keys:
            assert ui_text.UI_STRINGS[key][mine] in visible, key
            assert ui_text.UI_STRINGS[key][theirs] not in visible, key


# ==========================================================================
# 12. CONDITIONAL FRAMING
# ==========================================================================
def test_12_the_guidance_is_framed_as_conditional_in_both_languages():
    en = _visible(_block(_render(_package(_open_gap_state()), lang="en")))
    ar = _visible(_block(_render(_package(_open_gap_state()), lang="ar")))
    assert "when applicable" in en
    assert "If your idea involves" in en
    assert "may include" in en
    assert "عند انطباقها" in ar
    assert "إذا كانت فكرتك" in ar
    assert "فقد تشمل" in ar


# ==========================================================================
# 13. NO CONCEPT-CLASS ASSERTION
# ==========================================================================
_CLASS_CLAIMS_EN = (
    "this project is", "your project is", "this idea is a",
    "your idea is a", "the project belongs to", "your project belongs to",
    "we have established", "we determined that your",
)
_CLASS_CLAIMS_AR = ("مشروعك ينتمي", "مشروعك هو", "فكرتك هي", "حددنا أن")


def test_13_the_block_never_asserts_the_project_belongs_to_the_concept_class():
    """The interface class is a CONDITION in the copy, never a finding about the
    reader's project. Any non-negated membership claim is a violation."""
    for lang, claims in (("en", _CLASS_CLAIMS_EN), ("ar", _CLASS_CLAIMS_AR)):
        block = _block(_render(_package(_open_gap_state()), lang=lang))
        for claim in claims:
            assert _offenders(block, claim, lang) == [], (lang, claim)


def test_13b_the_class_conditions_are_never_stated_as_project_properties():
    """low-voltage / non-safety-critical / single-signal / sensor-to-microcontroller
    carry the concept class. They may appear ONLY inside the conditional intro,
    which opens with "If"; anywhere else they would read as a project finding."""
    parts = _parts(_block(_render(_package(_open_gap_state()), lang="en")))
    for term in ("low-voltage", "non-safety-critical", "single-signal",
                 "sensor-to-microcontroller"):
        carriers = [name for name, text in parts.items() if term in text]
        assert carriers == ["intro"], (term, carriers)
    assert parts["intro"].startswith("If your idea involves")
    assert parts["intro"].rstrip().endswith("may include:")


# ==========================================================================
# 14. NO INSPECTION CLAIM
# ==========================================================================
_INSPECTION_EN = ("you are missing", "your record is missing", "is missing",
                  "is absent", "is present", "are present", "we detected",
                  "we inspected", "was found missing", "we reviewed your record")
_INSPECTION_AR = ("ينقصك", "سجلك يفتقد", "فحصنا", "اكتشفنا", "راجعنا سجلك")


def test_14_the_block_never_claims_to_have_inspected_the_record():
    """The boundary sentence is allowed to DENY inspection; nothing may assert it."""
    for lang, claims in (("en", _INSPECTION_EN), ("ar", _INSPECTION_AR)):
        block = _block(_render(_package(_open_gap_state()), lang=lang))
        for claim in claims:
            assert _offenders(block, claim, lang) == [], (lang, claim)


def test_14b_the_block_states_the_non_inspection_boundary_explicitly():
    en = _visible(_block(_render(_package(_open_gap_state()), lang="en")))
    ar = _visible(_block(_render(_package(_open_gap_state()), lang="ar")))
    assert "does not inspect your record" in en
    assert "does not determine that your project belongs to this interface class" in en
    assert "ولا يفحص سجلك" in ar
    assert "لا يقرر النظام أن مشروعك ينتمي" in ar


# ==========================================================================
# 15. NO NUMERIC / COMPATIBILITY / ENGINEERING CLAIM
# ==========================================================================
def test_15a_the_block_carries_no_numeric_guidance():
    """The ONLY digit-bearing token permitted anywhere in the visible copy is the
    evidence-package reference. A value, threshold, tolerance or range would be a
    device-specific engineering claim this increment cannot make."""
    for lang in ("en", "ar"):
        visible = _visible(_block(_render(_package(_open_gap_state()), lang=lang)))
        numeric = [tok for tok in re.findall(r"\S+", visible) if re.search(r"\d", tok)]
        assert set(numeric) <= {"D13"}, (lang, numeric)


def test_15b_the_block_carries_no_units_operators_or_equations():
    for lang in ("en", "ar"):
        visible = _visible(_block(_render(_package(_open_gap_state()), lang=lang)))
        for token in ("=", "<", ">", "±", "%", "Ω", "µ"):
            assert token not in visible, (lang, token)
        for unit in (r"\bmV\b", r"\bkHz\b", r"\bMHz\b", r"\bmA\b", r"\bµA\b", r"\bnF\b"):
            assert not re.search(unit, visible), (lang, unit)


_VERDICT_EN = ("compatible", "incompatible", "compatibility", "is safe", "is unsafe",
               "safe limits", "safe operating", "correctness", "is correct")
_VERDICT_AR = ("التوافق", "الحدود الآمنة", "صحة الدائرة", "آمن")


def test_15c_no_compatibility_safety_or_correctness_verdict_is_issued():
    """These terms may appear ONLY inside the sentence that denies them."""
    for lang, terms in (("en", _VERDICT_EN), ("ar", _VERDICT_AR)):
        block = _block(_render(_package(_open_gap_state()), lang=lang))
        for term in terms:
            assert _offenders(block, term, lang) == [], (lang, term)


def test_15d_no_conditioning_recommendation_or_specialist_classification():
    for lang, terms in (("en", ("signal-conditioning", "specialist", "expert",
                                "certified", "licensed", "professional")),
                        ("ar", ("تكييف الإشارة", "أخصائي", "خبير", "معتمد"))):
        block = _block(_render(_package(_open_gap_state()), lang=lang))
        for term in terms:
            assert _offenders(block, term, lang) == [], (lang, term)


def test_15e_no_named_vendor_product_tool_laboratory_or_standard():
    named = ("Arduino", "ESP32", "TMP117", "Raspberry", "Texas Instruments",
             "Fluke", "Keysight", "Tektronix", "IEC ", "ISO ", "IEEE", "ASTM",
             "UL 6", "RoHS", "SPICE", "LTspice", "MATLAB")
    for lang in ("en", "ar"):
        visible = _visible(_block(_render(_package(_open_gap_state()), lang=lang)))
        for name in named:
            assert name not in visible, (lang, name)


# ==========================================================================
# 16. EVIDENCE DISCLOSURE
# ==========================================================================
def test_16a_the_block_discloses_its_bounded_evidence_origin():
    en = _visible(_block(_render(_package(_open_gap_state()), lang="en")))
    ar = _visible(_block(_render(_package(_open_gap_state()), lang="ar")))
    assert "accepted bounded D13 technical knowledge package" in en
    assert "corroborated/reasoned evidence" in en
    assert "حزمة المعرفة التقنية D13" in ar
    assert "أدلة مؤيدة/استدلالية" in ar


def test_16b_the_block_never_implies_primary_or_device_verification():
    """"primary-verified" is allowed only in the sentence that denies it."""
    for lang in ("en", "ar"):
        block = _block(_render(_package(_open_gap_state()), lang=lang))
        for term in (("primary-verified", "primary verified", "manufacturer verified",
                      "device verified", "engineering validated", "validated by")
                     if lang == "en" else ("تم التحقق منها", "مُعتمد هندسيًا")):
            assert _offenders(block, term, lang) == [], (lang, term)


# ==========================================================================
# 17. EXISTING PACKAGE INVARIANTS
# ==========================================================================
def test_17a_no_new_canonical_deliverable_section_exists():
    package = _package(_open_gap_state())
    assert tuple(k for k in package if k.startswith("section_")) == CANONICAL_SECTION_KEYS
    assert not [k for k in package if "cap01" in k.lower()]


def test_17b_sections_13_and_14_are_untouched_by_rendering_the_block():
    """Rendering is read-only over the package: Section 13 / Section 14 content,
    counts, identifiers and ordering survive byte-for-byte."""
    package = _package(_open_gap_state())
    before = copy.deepcopy((package["section_13_requirement_landscape"],
                            package["section_14_validation_plan"]))
    html = _render(package)
    assert _block(html) is not None, "guard: the block must have rendered here"
    assert (package["section_13_requirement_landscape"],
            package["section_14_validation_plan"]) == before


def test_17c_the_whole_package_is_unchanged_by_the_lookup_and_the_render():
    package = _package(_open_gap_state())
    before = copy.deepcopy(package)
    cap01_guidance.profile_copy(PROFILE_DOMAIN)
    _render(package)
    assert package == before


def test_17d_the_assembler_produces_the_same_package_it_did_before_cap01():
    """CAP-01 is presentation-only: two assemblies of one state agree on every
    section, so nothing in this increment reached the derivation."""
    state = _open_gap_state()
    a, b = _package(state), _package(state)
    for key in CANONICAL_SECTION_KEYS:
        assert a[key] == b[key], key


# ==========================================================================
# 18. STATE INVARIANTS
# ==========================================================================
def test_18_no_readiness_gap_evidence_or_progression_mutation_occurs():
    state = _open_gap_state()
    before = {
        "maturity_level": state.maturity_level,
        "gaps": [(g.gap_type, g.status, g.iterations_open, len(g.evidence))
                 for g in state.gaps],
        "domain": state.domain,
        "domain_signal": state.domain_signal,
        "iteration": getattr(state, "iteration", None),
    }
    package = _package(state)
    cap01_guidance.profile_copy(state.domain_signal)
    _render(package)
    assert state.maturity_level == before["maturity_level"]
    assert [(g.gap_type, g.status, g.iterations_open, len(g.evidence))
            for g in state.gaps] == before["gaps"]
    assert state.domain == before["domain"]
    assert state.domain_signal == before["domain_signal"]
    assert getattr(state, "iteration", None) == before["iteration"]


# ==========================================================================
# 19. HTML / PDF PARITY
# ==========================================================================
def test_19a_both_deliverable_routes_render_the_same_committed_template():
    src = _source(_APP_PATH)
    assert src.count('render_template(\n            "deliverable.html"') \
        + src.count('render_template(\n        "deliverable.html"') == 2, \
        "both deliverable routes must render deliverable.html"


def test_19b_the_pdf_shell_renders_the_identical_cap01_block():
    """The PDF route differs only by `deliverable_base`; the CAP-01 copy and
    profile path are the same, so the downloaded report cannot say something the
    screen does not."""
    package = _package(_open_gap_state())
    for lang in ("en", "ar"):
        screen = _block(_render(package, lang=lang))
        pdf = _block(_render(package, lang=lang, pdf=True))
        assert screen is not None and pdf is not None
        assert screen == pdf


def test_19c_the_pdf_shell_also_suppresses_the_block_when_no_profile_applies():
    package = _package(_open_gap_state(MECHANICAL_IDEA))
    assert _block(_render(package, pdf=True)) is None


# ==========================================================================
# 20. LOCALIZATION BOUNDARY
# ==========================================================================
def test_20a_the_bilingual_exception_is_limited_to_the_cap01_keys():
    keys = [k for k in ui_text.UI_STRINGS if k.startswith("UI_CAP01_")]
    # 11 from the first increment + 8 from the research-direction addendum
    assert len(keys) == 19
    assert len([k for k in keys if "_RESEARCH_" in k]) == 8
    assert all(k.startswith("UI_%s_" % PROFILE_ID) for k in keys)
    for key in keys:
        entry = ui_text.UI_STRINGS[key]
        assert set(entry) == {"en", "ar"}
        assert entry["en"].strip() and entry["ar"].strip()
        assert entry["en"] != entry["ar"]


def test_20b_the_category_c_rule_is_amended_only_to_record_this_one_exception():
    """The docstring must stay TRUTHFUL about what is and is not translated. The
    general Category-C exclusion survives; exactly one exception is named."""
    src = _source(_UI_TEXT_PATH)
    doc = src[:src.index("SUPPORTED_LANGS")]
    assert "Category-C generated OUTPUT" in doc
    assert "intentionally excluded and remain English" in doc
    assert "UI_CAP01_" in doc
    assert "ONE explicit" in doc
    for not_authorized in ("Question Translation Assistant", "automatic/model translation",
                           "no further\n    deliverable localization"):
        assert not_authorized in doc, not_authorized


def test_20c_no_second_localization_system_was_introduced():
    """CAP-01 copy lives in the ONE existing catalogue and is reached through the
    ONE existing resolver; no parallel translation path was created."""
    assert _flask_app.jinja_env.globals["cap01_profiles"] is cap01_guidance.profiles_for_package
    region = _template_cap01_region()
    visible_calls = re.findall(r">\{\{ ([a-z_]+)\(", region)
    assert set(visible_calls) == {"t"}, visible_calls
    for path in ("web/domain_label.py",) + CORE_FILES:
        assert "UI_CAP01_" not in _source(os.path.join(_ROOT, path)), path


def test_20d_no_ai_provider_schema_or_persistence_reached_this_increment():
    """Scanned over the WHOLE resolver module, not a slice of it: the module is
    small enough that the whole file is the honest scope, and a slice would stop
    reading exactly where a future import could be added."""
    region = _template_cap01_region()
    seam = _source(_GUIDANCE_PATH)
    for banned in ("openai", "anthropic", "requests.", "http", "sqlite", "INSERT",
                   "UPDATE ", "commit(", "embedding", "model("):
        assert banned.lower() not in seam.lower(), banned
        assert banned.lower() not in region.lower(), banned
    # the resolver imports the string catalogue and nothing else
    imports = re.findall(r"^\s*(?:from|import)\s+(\S+)", seam, re.M)
    assert imports == ["web"], imports

# ==========================================================================
# 21. G2 — capability availability is NOT owned by the string catalogue
# ==========================================================================
def test_21a_profile_availability_no_longer_lives_in_the_localization_catalogue():
    """The first draft put the domain->profile table and both lookups inside
    ``web/ui_text.py``. That made the localization module the CAP-01 capability
    owner: translation and capability availability are different concerns, and
    co-locating them is how a string catalogue quietly becomes an authority."""
    ui = _source(_UI_TEXT_PATH)
    for construct in ("CAP01_PROFILE_BY_DOMAIN", "_CAP01_COPY_PARTS",
                      "cap01_profile_for_domain", "cap01_profile_copy",
                      "profiles_for_package"):
        assert construct not in ui, ("availability construct still in ui_text",
                                     construct)
    assert not hasattr(ui_text, "CAP01_PROFILE_BY_DOMAIN")
    assert not hasattr(ui_text, "cap01_profile_copy")
    # and it lives in exactly one place instead
    assert cap01_guidance.CAP01_PROFILE_BY_DOMAIN
    assert callable(cap01_guidance.profile_copy)


def test_21b_ui_text_still_owns_the_copy_and_the_resolver_owns_no_text():
    """The split has to cut the right way round. ``ui_text`` keeps every string;
    ``cap01_guidance`` names keys and holds no user-facing sentence of its own."""
    ui = _source(_UI_TEXT_PATH)
    guidance = _source(_GUIDANCE_PATH)
    # copy stayed put
    assert len([k for k in ui_text.UI_STRINGS if k.startswith("UI_CAP01_")]) == 19
    assert "Technical information to check" in ui
    assert "\u0645\u0639\u0644\u0648\u0645\u0627\u062a \u0641\u0646\u064a\u0629 \u0644\u0644\u0645\u0631\u0627\u062c\u0639\u0629" in ui
    # and did NOT follow the availability table across
    for key in ui_text.UI_STRINGS:
        if key.startswith("UI_CAP01_"):
            for lang in ("en", "ar"):
                assert ui_text.UI_STRINGS[key][lang] not in guidance, key
    # the resolver returns keys, never text
    for view in (cap01_guidance.profile_copy(PROFILE_DOMAIN),):
        for value in [v for v in view.values() if isinstance(v, str)] + list(view["item_keys"]):
            assert value == PROFILE_ID or value.startswith("UI_CAP01_"), value
    # No user-facing text may live in the availability module, in EITHER form.
    # A raw-source scan alone is not enough: a mutation smuggled the Arabic title
    # back in as `"\\u0645..."` escapes, which the file bytes do not match and
    # Python still evaluates to the same sentence. So every string CONSTANT the
    # module actually holds is inspected after parsing.
    assert re.search(r"[\u0600-\u06FF]", guidance) is None, "text leaked into the resolver"
    constants = [n.value for n in ast.walk(ast.parse(guidance))
                 if isinstance(n, ast.Constant) and isinstance(n.value, str)]
    for value in constants:
        assert re.search(r"[\u0600-\u06FF]", value) is None, ("text leaked", value)
    catalogue = {v for entry in ui_text.UI_STRINGS.values()
                 if isinstance(entry, dict) for v in entry.values()
                 if isinstance(v, str)}
    assert not (set(constants) & catalogue), set(constants) & catalogue


def test_21c_the_resolver_asks_the_catalogue_rather_than_reaching_into_it():
    """Key existence is a question for the catalogue's own stated predicate. A
    module that reaches into ``UI_STRINGS`` directly owns it a little."""
    guidance = _source(_GUIDANCE_PATH)
    assert "UI_STRINGS" not in guidance
    assert "ui_text.has_string(" in guidance
    assert ui_text.has_string(PROFILE_DOMAIN) is False
    assert ui_text.has_string("UI_%s_TITLE" % PROFILE_ID) is True
    assert ui_text.has_string(None) is False


# ==========================================================================
# 22. G3 — today's single domain is a limitation, not the CAP-01 domain model
# ==========================================================================
def _synthetic(*rows):
    """A minimal PRESENTATION-shaped package. Synthetic on purpose: the runtime
    assembler emits exactly one capability row today, so a real package cannot
    exercise the collection. Nothing here activates a domain or claims the
    runtime supports more than one."""
    return {"section_3_assessment_overview": {"capabilities_assessed": list(rows)}}


def test_22a_the_selection_rule_no_longer_reads_the_first_capability():
    """``capabilities_assessed[0]`` was the defect: it silently made today's
    single-root-domain package shape the CAP-01 architectural selection rule."""
    region = _template_cap01_region()
    assert "[0]" not in region
    assert "capabilities_assessed" not in region
    assert "cap01_profiles(package)" in region
    guidance = _code(_GUIDANCE_PATH)
    assert "capabilities_assessed[0]" not in guidance
    assert "[0]" not in guidance


def test_22b_order_independence_mechanical_first_still_resolves_electronics():
    """The authorized profile must not depend on where its domain sits in the
    collection, and an unprofiled domain ahead of it must not swallow it or be
    treated as unsupported."""
    profiles = cap01_guidance.profiles_for_package(_synthetic(
        {"capability_id": "mechanical", "gaps_open": 2},
        {"capability_id": PROFILE_DOMAIN, "gaps_open": 1}))
    assert [p["profile_id"] for p in profiles] == [PROFILE_ID]
    reversed_ = cap01_guidance.profiles_for_package(_synthetic(
        {"capability_id": PROFILE_DOMAIN, "gaps_open": 1},
        {"capability_id": "mechanical", "gaps_open": 2}))
    assert [p["profile_id"] for p in reversed_] == [PROFILE_ID]


def test_22c_more_than_one_capability_needs_no_engine_change_and_claims_nothing():
    """A package carrying several canonical domains must EXTEND the resolver, not
    require replacing it — and must still assert nothing about multi-domain
    runtime support, which does not exist."""
    profiles = cap01_guidance.profiles_for_package(_synthetic(
        {"capability_id": "mechanical", "gaps_open": 1},
        {"capability_id": "medical_device", "gaps_open": 1},
        {"capability_id": PROFILE_DOMAIN, "gaps_open": 1},
        {"capability_id": "software", "gaps_open": 1}))
    assert [p["profile_id"] for p in profiles] == [PROFILE_ID]
    # unchanged core, proven the same way as the single-domain case
    offenders = [p for p in CORE_FILES
                 if re.search(r"cap.?01", _source(os.path.join(_ROOT, p)), re.I)]
    assert offenders == []
    # and the resolver never says the runtime supports several domains
    guidance = re.sub(r"\s+", " ", _source(_GUIDANCE_PATH)).lower()
    for claim in ("multi-domain support", "supports multiple domains",
                  "multi-domain runtime support", "multi-domain truth"):
        for m in re.finditer(re.escape(claim), guidance):
            head = guidance[max(0, m.start() - 120):m.start()]
            assert any(n in head for n in ("no ", "not ", "never", "nothing here")), (
                claim, guidance[max(0, m.start() - 120):m.end()])


def test_22d_duplicate_capability_rows_do_not_duplicate_the_profile():
    profiles = cap01_guidance.profiles_for_package(_synthetic(
        {"capability_id": PROFILE_DOMAIN, "gaps_open": 1},
        {"capability_id": PROFILE_DOMAIN, "gaps_open": 5},
        {"capability_id": PROFILE_DOMAIN, "gaps_open": 2}))
    assert [p["profile_id"] for p in profiles] == [PROFILE_ID]


def test_22e_the_open_gap_condition_still_gates_every_row():
    assert cap01_guidance.profiles_for_package(_synthetic(
        {"capability_id": PROFILE_DOMAIN, "gaps_open": 0})) == ()
    assert cap01_guidance.profiles_for_package(_synthetic(
        {"capability_id": PROFILE_DOMAIN})) == ()
    # a row with no open gap does not ride in on a sibling row that has one
    profiles = cap01_guidance.profiles_for_package(_synthetic(
        {"capability_id": PROFILE_DOMAIN, "gaps_open": 0},
        {"capability_id": "mechanical", "gaps_open": 4}))
    assert profiles == ()


@pytest.mark.parametrize("package", (
    None, {}, [], "not a package", 7,
    {"section_3_assessment_overview": None},
    {"section_3_assessment_overview": {}},
    {"section_3_assessment_overview": {"capabilities_assessed": None}},
    {"section_3_assessment_overview": {"capabilities_assessed": []}},
    {"section_3_assessment_overview": {"capabilities_assessed": ["junk", None]}},
))
def test_22f_an_unrecognised_package_shape_renders_nothing_and_never_raises(package):
    assert cap01_guidance.profiles_for_package(package) == ()


def test_22g_a_multi_row_render_stays_one_language_and_one_block_per_profile(monkeypatch):
    """The template loop must not become a second way to emit two languages or a
    duplicated block. Proven against a TEST-LOCAL second profile, torn down with
    the test \u2014 no production future profile is created."""
    prefix = "UI_CAP01_SEAM_PROBE_"
    monkeypatch.setitem(cap01_guidance.CAP01_PROFILE_BY_DOMAIN,
                        "seam_probe_domain", "CAP01_SEAM_PROBE")
    for part in ("TITLE", "INTRO", "BOUNDARY", "LIMIT", "EVIDENCE", "ITEM_1"):
        monkeypatch.setitem(ui_text.UI_STRINGS, prefix + part,
                            {"en": "probe-en " + part, "ar": "probe-ar " + part})
    package = _package(_open_gap_state())
    package["section_3_assessment_overview"]["capabilities_assessed"].append(
        {"capability_id": "seam_probe_domain", "gaps_open": 1})
    html = _render(package, lang="en")
    assert html.count('data-cap01-profile="%s"' % PROFILE_ID) == 1
    assert html.count('data-cap01-profile="CAP01_SEAM_PROBE"') == 1
    assert "probe-en TITLE" in html
    assert "probe-ar TITLE" not in html


# ==========================================================================
# 23. SECOND BOUNDED INCREMENT — research-direction addendum
# ==========================================================================
# What the first increment rendered, frozen: the 11 PR #678 copy keys, EN and AR,
# hashed at the authorized base 84c45cec. The addendum may only ADD; any edit to
# the accepted checklist copy changes this digest.
_PR678_COPY_DIGEST = "c964bcd2219eb1027d847ebab2a426d3fcfb50c4f9fe8e56de7999251334f0a0"

_RESEARCH_EN_MARKS = (
    "Where to look next",
    "research aids only",
    "\u201csensor output signal type\u201d",
    "\u201clogic output VOH VOL\u201d",
    "\u201cVIH VIL input threshold\u201d",
    "\u201cADC source impedance\u201d",
    "\u201ctimer input capture\u201d",
    "combine it with the relevant section or parameter",
)
_RESEARCH_AR_MARKS = (
    "\u0623\u064a\u0646 \u062a\u0628\u062d\u062b \u0644\u0627\u062d\u0642\u064b\u0627",
    "\u0648\u0633\u0627\u0626\u0644 \u0645\u0633\u0627\u0639\u062f\u0629 \u0644\u0644\u0628\u062d\u062b",
    "\u0639\u0628\u0627\u0631\u0627\u062a \u0628\u062d\u062b \u0645\u0642\u062a\u0631\u062d\u0629",
)


def _research_region(block):
    """The research-direction group only: from its heading to the boundary copy."""
    # Cut on TAG boundaries: slicing at the attribute would leave a half tag whose
    # "cap01" text then reads as a digit in the reader-visible copy.
    start = block.rindex("<", 0, block.index("data-cap01-research-title"))
    end = block.rindex("<", 0, block.index("data-cap01-boundary", start))
    return block[start:end]


def test_23a_the_six_accepted_checklist_items_are_byte_for_byte_unchanged():
    import hashlib, json
    base = {k: ui_text.UI_STRINGS[k] for k in sorted(ui_text.UI_STRINGS)
            if k.startswith("UI_CAP01_") and "_RESEARCH_" not in k}
    assert len(base) == 11
    got = hashlib.sha256(json.dumps(base, ensure_ascii=False,
                                    sort_keys=True).encode("utf-8")).hexdigest()
    assert got == _PR678_COPY_DIGEST, "the accepted PR #678 copy was edited"
    block = _block(_render(_package(_open_gap_state())))
    assert len(_items(block)) == 6


def test_23b_research_heading_intro_and_six_lines_render_in_english():
    block = _block(_render(_package(_open_gap_state()), lang="en"))
    assert "data-cap01-research-title" in block and "data-cap01-research-intro" in block
    assert len(_research_items(block)) == 6
    visible = _visible(block)
    for mark in _RESEARCH_EN_MARKS:
        assert mark in visible, mark
    for n in range(1, 7):
        key = "UI_%s_RESEARCH_ITEM_%d" % (PROFILE_ID, n)
        assert ui_text.UI_STRINGS[key]["en"] in visible, key


def test_23c_research_heading_intro_and_six_lines_render_in_arabic():
    block = _block(_render(_package(_open_gap_state()), lang="ar"))
    assert len(_research_items(block)) == 6
    visible = _visible(block)
    for mark in _RESEARCH_AR_MARKS:
        assert mark in visible, mark
    for n in range(1, 7):
        key = "UI_%s_RESEARCH_ITEM_%d" % (PROFILE_ID, n)
        assert ui_text.UI_STRINGS[key]["ar"] in visible, key


def test_23d_the_research_group_never_mixes_languages():
    package = _package(_open_gap_state())
    en = _visible(_research_region(_block(_render(package, lang="en"))))
    ar = _visible(_research_region(_block(_render(package, lang="ar"))))
    assert re.search(r"[\u0600-\u06FF]", en) is None, "Arabic leaked into the English group"
    for mark in _RESEARCH_EN_MARKS:
        assert mark not in ar, mark


def test_23e_research_sits_inside_the_block_before_its_governing_boundary():
    """BOUNDARY / LIMIT / EVIDENCE must still close the block, so they govern the
    research lines too — the addendum may not be rendered after them."""
    block = _block(_render(_package(_open_gap_state())))
    order = [block.index(m) for m in ("data-cap01-item", "data-cap01-research-title",
                                      "data-cap01-research-item", "data-cap01-boundary",
                                      "data-cap01-limit", "data-cap01-evidence")]
    assert order == sorted(order), order


def test_23f_search_terms_carry_no_numeric_value_threshold_or_unit():
    for lang in ("en", "ar"):
        region = _visible(_research_region(_block(_render(_package(_open_gap_state()),
                                                          lang=lang))))
        assert re.search(r"\d", region) is None, (lang, "digit in research copy")
        for token in ("=", "<", ">", "\u00b1", "%", "\u03a9", "\u00b5"):
            assert token not in region, (lang, token)
        for unit in (r"\bmV\b", r"\bV\b", r"\bkHz\b", r"\bHz\b", r"\bmA\b",
                     r"\bk?ohms?\b"):
            assert not re.search(unit, region, re.I), (lang, unit)


def test_23g_research_copy_names_no_vendor_product_lab_standard_or_specialist():
    named = ("Arduino", "ESP32", "STM32", "ATmega", "PIC", "Raspberry", "Texas Instruments",
             "Microchip", "Analog Devices", "Bosch", "Fluke", "Keysight", "Tektronix",
             "IEC", "ISO ", "IEEE", "ASTM", "UL ", "digikey", "mouser", "octopart",
             "google", "http", "www.")
    for lang in ("en", "ar"):
        region = _visible(_research_region(_block(_render(_package(_open_gap_state()),
                                                          lang=lang))))
        for name in named:
            assert name.lower() not in region.lower(), (lang, name)
        block = _block(_render(_package(_open_gap_state()), lang=lang))
        for term in (("specialist", "expert", "engineer", "consultant", "laboratory")
                     if lang == "en" else ("\u0645\u062e\u062a\u0635", "\u062e\u0628\u064a\u0631",
                                          "\u0645\u0647\u0646\u062f\u0633", "\u0645\u062e\u062a\u0628\u0631")):
            assert _offenders(block, term, lang) == [], (lang, term)


def test_23h_research_copy_issues_no_verdict_recommendation_or_project_claim():
    """Where to look is not what to do. No compatibility, safety, circuit or
    conditioning verdict; no claim that an item applies to, or is missing from,
    this project; and no suggestion that the platform searched or retrieved."""
    for lang, terms in (
            ("en", ("compatible", "compatibility", "safe", "unsafe", "correct",
                    "recommend", "you should use", "use a", "divider", "level shifter",
                    "buffer", "op-amp", "amplif", "filter", "conditioning",
                    "you are missing", "your project needs", "your record",
                    "we found", "we searched", "we retrieved", "we checked")),
            ("ar", ("\u0627\u0644\u062a\u0648\u0627\u0641\u0642", "\u0622\u0645\u0646",
                    "\u0646\u0648\u0635\u064a", "\u064a\u0646\u0642\u0635\u0643",
                    "\u0628\u062d\u062b\u0646\u0627", "\u0648\u062c\u062f\u0646\u0627"))):
        block = _block(_render(_package(_open_gap_state()), lang=lang))
        research = {k: v for k, v in _parts(block).items() if k.startswith("research")}
        assert len(research) == 8, sorted(research)
        for term in terms:
            for name, text in research.items():
                for sentence in _sentences(text):
                    if _mentions(sentence, term):
                        assert _denied(sentence, term, lang), (lang, name, term, sentence)


def test_23i_no_research_copy_without_a_resolved_profile():
    for state in (_open_gap_state(MECHANICAL_IDEA), _closed_gap_state()):
        html = _render(_package(state))
        assert "data-cap01-research" not in html
    unknown = _open_gap_state()
    unknown.domain_signal = "zzz_not_a_domain"
    assert "data-cap01-research" not in _render(_package(unknown))


def test_23j_mechanical_stays_byte_identical_with_the_addendum_present(monkeypatch):
    package = _package(_open_gap_state(MECHANICAL_IDEA))
    with_addendum = _mask_csrf(_render(package))
    for n in list(range(1, 7)):
        monkeypatch.delitem(ui_text.UI_STRINGS, "UI_%s_RESEARCH_ITEM_%d" % (PROFILE_ID, n))
    assert _mask_csrf(_render(package)) == with_addendum


def test_23k_duplicate_rows_still_render_one_block_and_one_research_group():
    package = _package(_open_gap_state())
    rows = package["section_3_assessment_overview"]["capabilities_assessed"]
    rows.append(dict(rows[0]))
    rows.insert(0, {"capability_id": "mechanical", "gaps_open": 3})
    html = _render(package)
    assert html.count("data-cap01-research-title") == 1
    assert html.count("data-cap01-research-item") == 6


def test_23l_the_research_group_is_optional_and_all_or_nothing(monkeypatch):
    """A future profile must not be forced to ship research copy, and a half
    group must never render — the checklist keeps rendering either way."""
    prefix = "UI_CAP01_SEAM_PROBE_"
    monkeypatch.setitem(cap01_guidance.CAP01_PROFILE_BY_DOMAIN,
                        "seam_probe_domain", "CAP01_SEAM_PROBE")
    for part in ("TITLE", "INTRO", "BOUNDARY", "LIMIT", "EVIDENCE", "ITEM_1"):
        monkeypatch.setitem(ui_text.UI_STRINGS, prefix + part,
                            {"en": "probe " + part, "ar": "probe " + part})
    view = cap01_guidance.profile_copy("seam_probe_domain")
    assert view is not None and view["research"] is None
    # heading + intro but no lines -> still no group
    for part in ("RESEARCH_TITLE", "RESEARCH_INTRO"):
        monkeypatch.setitem(ui_text.UI_STRINGS, prefix + part,
                            {"en": "probe " + part, "ar": "probe " + part})
    assert cap01_guidance.profile_copy("seam_probe_domain")["research"] is None
    # lines but no intro -> still no group
    monkeypatch.setitem(ui_text.UI_STRINGS, prefix + "RESEARCH_ITEM_1",
                        {"en": "probe line", "ar": "probe line"})
    monkeypatch.delitem(ui_text.UI_STRINGS, prefix + "RESEARCH_INTRO")
    assert cap01_guidance.profile_copy("seam_probe_domain")["research"] is None
    # the electronics profile keeps all six lines through all of this
    assert len(cap01_guidance.profile_copy(PROFILE_DOMAIN)["research"]["item_keys"]) == 6


def test_23m_research_copy_is_catalogue_owned_and_the_resolver_holds_none_of_it():
    guidance = _source(_GUIDANCE_PATH)
    for n in range(1, 7):
        for lang in ("en", "ar"):
            text = ui_text.UI_STRINGS["UI_%s_RESEARCH_ITEM_%d" % (PROFILE_ID, n)][lang]
            assert text not in guidance
    for word in ("Datasheet", "datasheet", "Search terms", "Characteristics"):
        assert word not in _code(_GUIDANCE_PATH), word
    region = _template_cap01_region()
    for word in ("Search terms", "Characteristics", "Where to look"):
        assert word not in region, word


def test_23n_pdf_carries_the_identical_research_group():
    package = _package(_open_gap_state())
    for lang in ("en", "ar"):
        assert _block(_render(package, lang=lang)) == \
            _block(_render(package, lang=lang, pdf=True))


# ==========================================================================
# 24. GOVERNANCE TRUTH AFTER PR #678
# ==========================================================================
_STATE_PATH = os.path.join(_ROOT, "docs", "governance", "CURRENT_PROJECT_STATE.md")
_CONTRACT_PATH = os.path.join(_ROOT, "docs", "governance", "ACTIVE_INCREMENT_CONTRACT.md")
_MERGE_678 = "84c45cec89f5348f279c591dd739ded0d0db24b3"


def _fenced(path, name):
    raw = _source(path)
    o = "<!-- CURRENT-BLOCK: %s -->" % name
    return re.sub(r"\s+", " ", raw[raw.index(o) + len(o):
                                   raw.index("<!-- END CURRENT-BLOCK: %s -->" % name)])


def test_24_current_state_says_first_merged_second_authorized_stage_partial():
    for block in (_fenced(_STATE_PATH, "current-position"),
                  _fenced(_CONTRACT_PATH, "current-routing")):
        assert "`FIRST BOUNDED CAP-01 INCREMENT: OWNER-AUTHORIZED`" in block
        assert "IMPLEMENTED / MERGED / POST-MERGE VERIFIED" in block
        assert "PR #678" in block and _MERGE_678 in block
        assert "SECOND BOUNDED CAP-01 RESEARCH-DIRECTION INCREMENT: OWNER-AUTHORIZED" in block
        assert "`STAGE 18 COMPLETE: NO`" in block
        assert re.search(r"FULL CAP-01\s*/\s*FULL STG: NOT AUTHORIZED", block)
        assert "STAGE 18 COMPLETE: YES" not in block
