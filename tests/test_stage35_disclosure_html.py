"""Stage 35 — Structured Invention Disclosure Export — first bounded slice —
self-contained HTML document (BASE RED, file H).

Implementation contract §10 and §12, §14 #1–#3, #7, #13, #14, #16, #20, #21,
#24, #27, #29–#32. The document is rendered from the finished projection and the
locale only.
"""
import glob
import html as _html
import re
from html.parser import HTMLParser

import pytest

import web.app as webapp
from engine import disclosure_export as dx
from engine.idea_state import IdeaState
from tests.test_stage35_disclosure_projection import (
    CAPTURE_LIMITATION, DISCLAIMERS_EN, HOSTILE, SCOPE_AR, SCOPE_EN, _base_state,
    _compose, _q, _rich, _rich_sources, _src,
)
from web import ui_text

TS = "2026-10-05T00:00:00Z"
CSP = ("default-src 'none'; style-src 'unsafe-inline'; img-src 'none'; "
       "base-uri 'none'; form-action 'none'")
AR_DISCLAIMERS = (
    "هذه الوثيقة ليست استشارة قانونية، ولا يقدّم InventorAI خدمات قانونية.",
    "هذه الوثيقة ليست رأيًا بشأن قابلية الاختراع للحصول على براءة. لم يقيّم InventorAI ما إذا كان هذا الاختراع جديدًا أو ينطوي على خطوة ابتكارية أو قابلًا للحصول على براءة.",
    "هذه الوثيقة ليست بحثًا في التقنية السابقة (prior art). لم يبحث InventorAI عن التقنية السابقة ولم يؤكد خلوّ الطريق منها.",
    "هذه الوثيقة ليست رأيًا بشأن حرية الاستغلال (freedom to operate).",
    "هذه الوثيقة ليست طلب براءة اختراع جاهزًا للإيداع.",
    "لم يصِغ InventorAI أي مطالبة براءة (patent claim) في هذه الوثيقة ولم يولّدها. أي صياغة تشبه المطالبات لا ترد إلا داخل نص منقول عن المخترع، مُستنسَخ كما كُتب ودون تقييم. لا شيء في هذه الوثيقة مطالبة صالحة قانونيًا.",
    "الأدلة المسجّلة هنا ليست استنتاجًا متحقَّقًا منه. العناصر الموسومة بأنها غير متحقَّق منها لم يتحقق منها InventorAI.",
    "لا تُثبت هذه الوثيقة تاريخ تصوّر الاختراع ولا تاريخ الاختراع ولا الأسبقية ولا صفة المخترع ولا الملكية.",
    "أي بصمة رقمية (digest) أو تاريخ في هذه الوثيقة أداة للتحقق من سلامة المحتوى فقط، وليس ختمًا زمنيًا قانونيًا ولا توثيقًا رسميًا ولا دليلًا على الأسبقية.",
    "قد تُعدّ مشاركة هذه الوثيقة إفصاحًا عن الاختراع في بعض الولايات القضائية. استشر مختصًا مؤهلًا في البراءات قبل مشاركتها.",
    "للحصول على استشارة قانونية، استشر مختصًا مؤهلًا في البراءات.",
)
MARKER_WORDING = {
    "NOTHING_RECORDED": ("Nothing recorded in this project", "لا شيء مسجّل في هذا المشروع"),
    "NOT_CAPTURED": ("Not captured by InventorAI", "لا يلتقط InventorAI هذه المعلومة"),
    "RAW_TEXT_ONLY": ("Only as the inventor's own wording in", "فقط بصياغة المخترع نفسه في"),
    "EXCLUDED_FROM_FIRST_SLICE": ("Not included in this export", "غير مُضمَّن في هذا التصدير"),
    "NOT_APPLICABLE": ("Not applicable", "لا ينطبق"),
    "UNAVAILABLE": ("Unavailable — this information could not be read",
                    "غير متاح — تعذّرت قراءة هذه المعلومة"),
}
TOP_UNAVAILABLE = ("One or more sections of this document could not be read and are "
                   "marked Unavailable.")
NA_ROWS_EN = (
    "No separate source value is held for this item. This does not mean the item has no source.",
    "No separate validation value is held for this item. This does not mean the item was "
    "validated or that validation is unnecessary.",
    "No separate limitation note is held for this item. This does not mean the item has no "
    "limitations.",
)
LEGEND_YOU_EN = ("When an existing InventorAI statement uses “you” or “your”, it refers to "
                 "the inventor who recorded this project.")
RISKS_EN = ("This section references unresolved technical issues listed in this export. "
            "InventorAI has not performed a risk assessment here.")


def _doc(content=None):
    content = content if content is not None else dx.compose_projection(_rich_sources())
    return dx.export_document(content, TS, dx.HTML_FORMAT_VERSION)


def _render(document, lang):
    return webapp._disclosure_document_html(document, lang)


def _text(markup):
    return _html.unescape(re.sub(r"<[^>]+>", " ", markup))


class _Tags(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

    handle_startendtag = handle_starttag


def _tags(markup):
    p = _Tags()
    p.feed(markup)
    return p.tags


def _without_quoted(markup):
    return re.sub(r'<(div|bdi|span)[^>]*data-content-class="QUOTED_INVENTOR_CONTENT"[^>]*>'
                  r'.*?</\1>', "", markup, flags=re.S)


@pytest.fixture(params=["en", "ar"])
def lang(request):
    return request.param


# ===========================================================================
# #16 — self-contained
# ===========================================================================
def test_16_self_contained_document(lang):
    markup = _render(_doc(), lang)
    assert markup.lstrip().lower().startswith("<!doctype html>")
    tags = _tags(markup)
    names = [t for t, _a in tags]
    for banned in ("script", "link", "img", "iframe", "object", "embed", "form", "base",
                   "input", "button", "svg", "video", "audio"):
        assert banned not in names, banned
    for _t, attrs in tags:
        for name, value in attrs.items():
            assert not name.startswith("on"), name
            if name in ("href", "src", "action", "srcset", "poster"):
                assert (value or "").startswith("#"), value
    assert "javascript:" not in markup.lower()
    assert "http://" not in markup and "https://" not in markup and "url(" not in markup
    metas = [a for t, a in tags if t == "meta"]
    assert {"charset": "utf-8"} in metas
    assert {"name": "viewport", "content": "width=device-width, initial-scale=1"} in metas
    assert {"http-equiv": "Content-Security-Policy", "content": CSP} in metas
    assert names.count("style") == 1


# ===========================================================================
# #2 / #14 — disclaimers, scope label, locale
# ===========================================================================
def test_02_disclaimers_scope_and_direction(lang):
    markup = _render(_doc(), lang)
    tags = _tags(markup)
    html_attrs = [a for t, a in tags if t == "html"][0]
    assert html_attrs == ({"lang": "en", "dir": "ltr"} if lang == "en"
                          else {"lang": "ar", "dir": "rtl"})
    positions = []
    for n, en in enumerate(DISCLAIMERS_EN):
        assert _html.escape(en, quote=False) in markup or en in markup
        positions.append(markup.index(_html.escape(en, quote=False)))
        if lang == "ar":
            ar_pos = markup.index(AR_DISCLAIMERS[n])
            assert ar_pos > positions[-1]
            if n + 1 < len(DISCLAIMERS_EN):
                assert ar_pos < markup.index(_html.escape(DISCLAIMERS_EN[n + 1], quote=False))
            assert re.search(r'<p lang="en" dir="ltr"[^>]*>' + re.escape(
                _html.escape(en, quote=False)) + "</p>", markup)
        else:
            assert AR_DISCLAIMERS[n] not in markup
    assert positions == sorted(positions)
    assert SCOPE_EN in markup
    assert (SCOPE_AR in markup) == (lang == "ar")
    if lang == "ar":
        assert re.search(r'lang="en" dir="ltr"[^>]*>' + re.escape(SCOPE_EN), markup)
    first_field = markup.index('id="field-invention_title"')
    assert positions[-1] < first_field


# ===========================================================================
# #1 — prohibited wording in chrome and system assertions
# ===========================================================================
PROHIBITED_EN = (r"\bpatentab", r"\bis (novel|new|inventive)\b", r"\binventive step",
                 r"\bprior[- ]art", r"\bfreedom[- ]to[- ]operate", r"\bfiling[- ]ready",
                 r"\bready (for|to) fil", r"\blegally valid", r"\blegal advice",
                 r"\bpatent claim", r"what is claimed", r"\bwe claim\b", r"\bclaim \d",
                 r"\b(in)?dependent claim")
PROHIBITED_AR = ("براءة", "استشارة قانونية", "التقنية السابقة", "حرية الاستغلال", "مطالبة",
                 "قابلية الاختراع")


def test_01_no_prohibited_wording_outside_the_disclaimer_allow_lists(lang):
    markup = _without_quoted(_render(_doc(), lang))
    text = _text(markup)
    for allowed in DISCLAIMERS_EN + AR_DISCLAIMERS + (SCOPE_EN, SCOPE_AR):
        text = text.replace(allowed, " ")
    for pattern in PROHIBITED_EN:
        assert not re.search(pattern, text, re.I), pattern
    for word in PROHIBITED_AR:
        assert word not in text, word


# ===========================================================================
# #3 / #24 / #30 / #31 — markers, reasons, legend, Risks, envelope context
# ===========================================================================
def test_03_markers_reasons_and_legend(lang):
    rich = _render(_doc(), lang)
    empty = _render(_doc(_compose(IdeaState(idea_id="e"))), lang)
    i = 0 if lang == "en" else 1
    for marker in ("NOTHING_RECORDED", "NOT_CAPTURED", "EXCLUDED_FROM_FIRST_SLICE",
                   "NOT_APPLICABLE"):
        assert MARKER_WORDING[marker][i] in empty
    for key in ("NON_INTEGRATED_PROJECT", "NO_APPROVAL_RECORD", "PLANNING_INPUTS",
                "CONFIDENTIAL_EVIDENCE_CATEGORIES", "RESULT_TEXT_NOT_CARRIED",
                "CARRIED_ON_EVERY_ITEM"):
        assert _html.escape(ui_text.text("UI_S35_REASON_" + key, lang), quote=False) in empty
    for key in ("FORM_ROW_QUALITY_DERIVED", "OBJECTIVE_NAMES_EVIDENCE_LEVEL"):
        assert _html.escape(ui_text.text("UI_S35_REASON_" + key, lang), quote=False) in rich
    for markup in (rich, empty):
        legend = markup.index('id="how-to-read"')
        assert markup.index(_html.escape(DISCLAIMERS_EN[-1], quote=False)) < legend
        assert legend < markup.index('id="field-invention_title"')
        for marker, wording in MARKER_WORDING.items():
            assert wording[i] in markup[legend:markup.index('id="field-invention_title"')]
        assert TOP_UNAVAILABLE not in markup
        risks = markup.index('id="field-risks"')
        clar = _html.escape(ui_text.text("UI_S35_RISKS_CLARIFICATION", lang), quote=False)
        assert markup.index(clar, risks) < markup.index('id="field-uncertainty_and_abstentions"')
    if lang == "en":
        assert RISKS_EN in rich
        assert "It does not mean that none exists." in empty or \
            "It does not mean that none\nexists." in empty
    # #30: envelope NOT_APPLICABLE rows carry the contextual sentence, never bare.
    na = [ui_text.text("UI_S35_NA_" + k, lang) for k in ("SOURCE", "VALIDATION", "LIMITATION")]
    for sentence in na:
        assert _html.escape(sentence, quote=False) in rich
    if lang == "en":
        for sentence in NA_ROWS_EN:
            assert sentence in rich
    assert not re.search(r'data-row="(source|validation|limitation)"[^>]*>\s*'
                         + re.escape(MARKER_WORDING["NOT_APPLICABLE"][i]) + r"\s*<", rich)


def test_03_raw_text_only_pointer(lang):
    s = _base_state()
    s.record_interaction("answered", "The deck is 80 cm wide.", gap_context="BOUNDARY_AMBIGUITY")
    markup = _render(_doc(_compose(s)), lang)
    i = 0 if lang == "en" else 1
    section = markup[markup.index('id="field-raw_materials_dimensions_parameters_conditions"'):
                     markup.index('id="field-interface_verification_preparation_inputs"')]
    assert MARKER_WORDING["RAW_TEXT_ONLY"][i] in section
    assert ui_text.text("UI_B_DELIV_036", lang) in section
    rich = _render(_doc(_compose(_rich(), quantities=(_q(0, "rec_1", "12 V"),))), lang)
    section = rich[rich.index('id="field-raw_materials_dimensions_parameters_conditions"'):
                   rich.index('id="field-interface_verification_preparation_inputs"')]
    assert MARKER_WORDING["RAW_TEXT_ONLY"][i] not in section


def test_24_unavailable_rendering():
    sources = _rich_sources()
    failed = dx.compose_projection(dx.MaterializedSources(
        state=sources.state, requirement_quantities=sources.requirement_quantities,
        planning_metadata=sources.planning_metadata,
        interface_dependencies=sources.interface_dependencies,
        result_events=sources.result_events, section_outcomes={"experiments": "UNAVAILABLE"}))
    markup = _render(_doc(failed), "en")
    assert TOP_UNAVAILABLE in markup
    section = markup[markup.index('id="field-experiments"'):
                     markup.index('id="field-experiment_result_text"')]
    assert MARKER_WORDING["UNAVAILABLE"][0] in section
    assert markup.index(TOP_UNAVAILABLE) < markup.index('id="how-to-read"')


# ===========================================================================
# #7 / #27 — attribution inside each item container
# ===========================================================================
def _articles(markup):
    return re.findall(r'(<article class="item" id="([^"]+)" data-kind="([^"]+)">.*?</article>)',
                      markup, re.S)


def test_27_every_item_carries_its_rows(lang):
    markup = _render(_doc(), lang)
    arts = _articles(markup)
    assert len(arts) > 20
    src_label = ui_text.text("UI_ED_SOURCE", lang)
    val_label = ui_text.text("UI_ED_VALIDATION", lang)
    na_lim = _html.escape(ui_text.text("UI_S35_NA_LIMITATION", lang), quote=False)
    for body, key, kind in arts:
        assert src_label in body and val_label in body and na_lim in body, key
        if kind in ("gap_reference", "evidence_reference"):
            assert 'href="#' in body and 'data-inherited-from="' in body
            assert ui_text.text("UI_S35_REFERENCE", lang) in body
        else:
            assert 'data-content-class="' in body
    for body, key, kind in arts:
        if kind == "correction_version":
            assert (ui_text.text("UI_S35_CURRENT", lang) in body
                    or _html.escape(ui_text.text("UI_S35_SUPERSEDED", lang), quote=False) in body)


def test_07_content_class_labels_adjacent_to_values(lang):
    markup = _render(_doc(), lang)
    quoted = _html.escape(ui_text.text("UI_S35_QUOTED", lang), quote=False)
    system = ui_text.text("UI_S35_SYSTEM", lang)
    for m in re.finditer(r'<div class="slot"[^>]*>(.*?)</div>\s*<!-- /slot -->', markup, re.S):
        block = m.group(1)
        if 'data-content-class="QUOTED_INVENTOR_CONTENT"' in block:
            assert quoted in block
        if 'data-content-class="SYSTEM_ASSERTION"' in block:
            assert system in block
    assert "data-approval" not in markup and "approved" not in _text(markup).lower()


# ===========================================================================
# #13 — hostile text
# ===========================================================================
def test_13_hostile_text_escaped_and_exact(lang):
    s = _base_state()
    s.idea_summary = HOSTILE
    markup = _render(_doc(_compose(s)), lang)
    assert "<script>alert(1)</script>" not in markup
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in markup
    assert '<a href="javascript:x">' not in markup
    assert "{{ 7*7 }}" in markup and "{% if %}" in markup
    m = re.search(r'<div class="value"[^>]*data-content-class="QUOTED_INVENTOR_CONTENT"'
                  r'[^>]*>(.*?)</div>', markup, re.S)
    assert _html.unescape(m.group(1)) == HOSTILE.strip()
    assert "‮" in markup and "⁦" in markup


# ===========================================================================
# #20 / #21 / #29 — quantities, problem limitation, neutral wording
# ===========================================================================
def test_20_quantity_rendering(lang):
    s = _rich()
    c = _compose(s, quantities=(_q(0, "rec_1", "0.5–0.8 mm"),
                                _q(1, "rec_9", "≈3 kg", kind="maximum_value")))
    markup = _render(_doc(c), lang)
    section = markup[markup.index('id="field-raw_materials_dimensions_parameters_conditions"'):
                     markup.index('id="field-interface_verification_preparation_inputs"')]
    assert "0.5–0.8 mm" in section and "≈3 kg" in section
    assert ui_text.text("UI_T2A_KIND_TARGET_VALUE", lang) in section
    assert ui_text.text("UI_T2A_KIND_MAXIMUM_VALUE", lang) in section
    assert _html.escape(ui_text.text("UI_T2A_WITHDRAWN_ANCHOR", lang), quote=False) in section
    assert _html.escape(ui_text.text("UI_S35_WITHDRAWN_NOTE", lang), quote=False) in section
    assert _html.escape(ui_text.text("UI_T2A_WITHDRAWN_NOTE", lang), quote=False) not in section
    assert 'href="#requirement_landscape.' in section


def test_21_capture_limitation_inside_the_problem_item(lang):
    markup = _render(_doc(), lang)
    [problem] = [a for a in _articles(markup) if a[2] == "resolved_problem"]
    body = problem[0]
    text_at = body.index("Wheelchair users cannot cross")
    lim_at = body.index(_html.escape(CAPTURE_LIMITATION, quote=False))
    assert text_at < lim_at
    if lang == "ar":
        ar = _html.escape(ui_text.text("UI_S35_CAPTURE_LIMITATION", "ar"), quote=False)
        assert lim_at < body.index(ar)
        assert re.search(r'lang="en" dir="ltr"[^>]*>' + re.escape(
            _html.escape(CAPTURE_LIMITATION, quote=False)), body)


def test_29_neutral_wording(lang):
    markup = _render(_doc(), lang)
    you = ui_text.text("UI_ED_SOURCE_OWNER_STATED", lang)
    assert not re.search(r'data-row="source"[^>]*>[^<]*<[^>]*>[^<]*</[^>]*>\s*'
                         + re.escape(you) + r"\s*<", markup)
    assert ui_text.text("UI_S35_SOURCE_OWNER_STATED", lang) in markup
    assert _html.escape(ui_text.text("UI_S35_FIELD_RAW_MATERIALS_DIMENSIONS_PARAMETERS_CONDITIONS",
                                     lang), quote=False) in markup
    assert ui_text.text("UI_S35_FIELD_CORRECTIONS", lang) in markup
    rec_text = ui_text.text("UI_S35_EXECUTION_RECORDED", lang).replace("{n}", "1")
    assert _html.escape(rec_text, quote=False) in markup
    assert "You recorded" not in markup and "Your recorded" not in markup
    # Stage-35-authored fixed copy addresses no reader as the inventor.
    for key, pair in ui_text.UI_STRINGS.items():
        if not key.startswith("UI_S35_") or key.startswith(("UI_S35_PAGE_", "UI_S35_JSON",
                                                             "UI_S35_HTML_", "UI_S35_RETENTION",
                                                             "UI_S35_NOTICES", "UI_S35_SAME",
                                                             "UI_S35_ACCOUNT")):
            continue
        assert not re.search(r"\byou(r)?\b", pair["en"].replace(
            "“you” or “your”", ""), re.I), key
    text = _text(_without_quoted(markup))
    if re.search(r"\byou(r)?\b", text.replace("“you” or “your”", ""), re.I):
        assert _html.escape(ui_text.text("UI_S35_HOWTO_YOU", lang), quote=False) in markup
    if lang == "en":
        assert LEGEND_YOU_EN in markup


# ===========================================================================
# #32 — direction and phone width
# ===========================================================================
def test_32_wrapping_and_direction_rules():
    markup = _render(_doc(), "ar")
    style = re.search(r"<style>(.*?)</style>", markup, re.S).group(1)
    assert re.search(r"body\s*\{[^}]*overflow-wrap:\s*anywhere", style)
    assert re.search(r"\.value\s*\{[^}]*white-space:\s*pre-wrap", style)
    assert re.search(r"\.value\s*\{[^}]*overflow-wrap:\s*anywhere", style)
    for m in re.finditer(r'<div class="value"[^>]*>', markup):
        assert 'dir="auto"' in m.group(0)
    doc = _doc()
    assert doc["content_digest"] in markup
    for ch in ("­", "​", "‌", "‍", "⁠"):
        assert ch not in markup


def test_32_phone_width_no_horizontal_overflow():
    pytest.importorskip("playwright.sync_api")
    from playwright.sync_api import sync_playwright
    s = _base_state()
    long_value = "L" * 2000
    s.idea_summary = long_value
    doc = _doc(_compose(s))
    exe = (glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome") or [None])[0]
    with sync_playwright() as p:
        kw = {"headless": True, "args": ["--no-sandbox"]}
        if exe:
            kw["executable_path"] = exe
        browser = p.chromium.launch(**kw)
        try:
            for lang in ("en", "ar"):
                for width in (360, 390):
                    page = browser.new_page(viewport={"width": width, "height": 800})
                    page.set_content(_render(doc, lang))
                    sw, cw = page.evaluate(
                        "[document.documentElement.scrollWidth, window.innerWidth]")
                    assert sw <= cw, (lang, width, sw, cw)
                    digest = page.evaluate(
                        "document.querySelector('[data-digest]').textContent")
                    assert digest == doc["content_digest"]
                    value = page.evaluate(
                        "document.querySelector('.value[data-content-class="
                        "\"QUOTED_INVENTOR_CONTENT\"]').textContent")
                    assert value == long_value
                    page.close()
        finally:
            browser.close()
