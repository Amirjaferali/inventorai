"""CAP-11 Slice 1 — Evidence Details (report Section 2 only).

docs/governance/CAP11_EVIDENCE_DETAILS_ENTRY_CONTRACT.md: each present Known
Problem / Known Mechanism evidence item shows, under "About this evidence",
three independent rows — Form, Source, Validation — derived only from the
already-assembled evidence fields. Nothing is combined, ordered or scored;
LEGACY_UNSPECIFIED reads "Source metadata not available"; UNVALIDATED reads
"No validation recorded"; anything unrecognised reads "Not available" for that
row only and never becomes UNVALIDATED, OWNER_STATED, LEGACY_UNSPECIFIED or a
tier. Report / PDF only; the package, state, readiness, Section 9, the session
page and Commercial / Manufacturing evidence are untouched. Synthetic data.
"""
import html
import pickle
import re

import pytest

import web.app as appmod
from engine.deliverable_assembler import _ev, assemble_deliverable
from engine.derived_readiness import derive_readiness
from engine.idea_state import (
    ASSERTED, REASONED, DEMONSTRATED, Evidence, PROVENANCE_VALUES,
    VALIDATION_STATUSES, LEGACY_UNSPECIFIED, UNVALIDATED, OWNER_STATED,
)
from web.ui_text import UI_STRINGS, text
from tests.test_deliverable_hygiene import PROHIBITED_TOKENS
from tests.test_safe_question_routing_pf_q2 import (  # noqa: F401  (fixture)
    client, MECH, _start, _answer, _live,
)

CANONICAL_TOKENS = (tuple(PROVENANCE_VALUES) + tuple(VALIDATION_STATUSES)
                    + (ASSERTED, REASONED, DEMONSTRATED))
SCORE_WORDS = ("score", "tier", "level", "rank", "weak", "strong", "low",
               "medium", "high", "%", "confidence", "overall")


def _details(quality=REASONED, provenance=OWNER_STATED, validation=UNVALIDATED):
    return appmod._evidence_details(
        _ev(Evidence("synthetic statement", quality, 1, provenance, validation)))


def _keys(d):
    return {axis: d[axis]["key"] for axis in ("form", "source", "validation")}


# ---------------------------------------------------------------------------
# 3-9 / 11 — the three mappings, legacy and fail-closed behaviour
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("quality", [ASSERTED, REASONED, DEMONSTRATED])
def test_every_canonical_form_value(quality):
    d = _details(quality=quality)
    assert d["form"]["key"] == "UI_ED_FORM_" + quality
    assert d["form"]["slug"] == quality.lower()


@pytest.mark.parametrize("provenance", list(PROVENANCE_VALUES))
def test_every_canonical_source_value(provenance):
    d = _details(provenance=provenance)
    assert d["source"]["key"] == "UI_ED_SOURCE_" + provenance


@pytest.mark.parametrize("validation", sorted(VALIDATION_STATUSES))
def test_every_canonical_validation_value(validation):
    d = _details(validation=validation)
    assert d["validation"]["key"] == "UI_ED_VALIDATION_" + validation


def test_axes_are_independent_of_each_other():
    """Changing one axis never changes another row."""
    base = _keys(_details())
    for quality in (ASSERTED, DEMONSTRATED):
        k = _keys(_details(quality=quality))
        assert (k["source"], k["validation"]) == (base["source"], base["validation"])
    for provenance in PROVENANCE_VALUES:
        k = _keys(_details(provenance=provenance))
        assert (k["form"], k["validation"]) == (base["form"], base["validation"])
    for validation in VALIDATION_STATUSES:
        k = _keys(_details(validation=validation))
        assert (k["form"], k["source"]) == (base["form"], base["source"])


def test_legacy_unspecified_is_source_metadata_not_available_and_not_reclassified():
    d = _details(provenance=LEGACY_UNSPECIFIED)
    assert d["source"]["key"] == "UI_ED_SOURCE_LEGACY_UNSPECIFIED"
    assert text("UI_ED_SOURCE_LEGACY_UNSPECIFIED", "en") == "Source metadata not available"
    assert text("UI_ED_SOURCE_LEGACY_UNSPECIFIED", "ar") == "بيانات المصدر غير متاحة"
    for lang in ("en", "ar"):
        assert "pre-provenance" not in text("UI_ED_SOURCE_LEGACY_UNSPECIFIED", lang)
        assert text("UI_ED_SOURCE_LEGACY_UNSPECIFIED", lang) != \
            text("UI_ED_SOURCE_OWNER_STATED", lang)


def test_unvalidated_is_no_validation_recorded_and_claims_nothing_else():
    assert text("UI_ED_VALIDATION_UNVALIDATED", "en") == "No validation recorded"
    assert text("UI_ED_VALIDATION_UNVALIDATED", "ar") == "لا يوجد تحقق مسجّل"
    for phrase in ("nobody", "no one", "not checked", "anyone"):
        assert phrase not in text("UI_ED_VALIDATION_UNVALIDATED", "en").lower()


def test_unknown_form_fails_closed():
    ev = _ev(Evidence("x", REASONED, 1, OWNER_STATED, UNVALIDATED))
    for bad in ("BOGUS", None, 7, "", "reasoned"):
        d = appmod._evidence_details(dict(ev, quality=bad))
        assert d["form"] == {"key": "UI_ED_NA", "slug": "na"}, bad
        assert d["source"]["key"] == "UI_ED_SOURCE_OWNER_STATED"


def test_unknown_source_fails_closed_and_is_never_coerced():
    ev = _ev(Evidence("x", REASONED, 1, OWNER_STATED, UNVALIDATED))
    for bad in ("WEIRD", None, 3, "", "owner_stated", "You"):
        d = appmod._evidence_details(dict(ev, provenance=bad))
        assert d["source"] == {"key": "UI_ED_NA", "slug": "na"}, bad


def test_unknown_validation_fails_closed_and_never_becomes_unvalidated():
    ev = _ev(Evidence("x", REASONED, 1, OWNER_STATED, UNVALIDATED))
    for bad in ("WEIRD", None, 0, "", "unvalidated", "Not validated"):
        d = appmod._evidence_details(dict(ev, validation_status=bad))
        assert d["validation"] == {"key": "UI_ED_NA", "slug": "na"}, bad
        assert d["validation"]["key"] != "UI_ED_VALIDATION_UNVALIDATED"
    # an evidence object carrying an unrecognised token (assembler's own label
    # would say "Not validated") still reads "not available" here
    odd = _ev(Evidence("x", REASONED, 1, OWNER_STATED, "SOMETHING_ELSE"))
    assert appmod._evidence_details(odd)["validation"]["key"] == "UI_ED_NA"


def test_missing_fields_and_non_dict_input_fail_closed_per_row():
    for bad in ({}, None, "text", ["x"]):
        d = appmod._evidence_details(bad)
        assert all(d[a]["key"] == "UI_ED_NA" for a in ("form", "source", "validation"))


def test_labels_are_neutral_and_carry_no_score_or_order():
    keys = [k for k in UI_STRINGS if k.startswith("UI_ED_")]
    assert len(keys) == 18
    for k in keys:
        for lang in ("en", "ar"):
            value = UI_STRINGS[k][lang]
            assert value.strip(), (k, lang)
            for token in CANONICAL_TOKENS:
                assert token not in value, (k, token)
        if k != "UI_ED_FORM_NOTE":
            for word in SCORE_WORDS:
                assert not re.search(r"\b%s\b" % re.escape(word),
                                     UI_STRINGS[k]["en"].lower()), (k, word)
    assert text("UI_ED_HEADING", "en") == "About this evidence"
    assert text("UI_ED_HEADING", "ar") == "عن هذا الدليل"
    assert "standing" not in text("UI_ED_HEADING", "en").lower()
    assert [text(k, "en") for k in ("UI_ED_FORM", "UI_ED_SOURCE", "UI_ED_VALIDATION")] \
        == ["Form", "Source", "Validation"]
    assert [text(k, "ar") for k in ("UI_ED_FORM", "UI_ED_SOURCE", "UI_ED_VALIDATION")] \
        == ["الصيغة", "المصدر", "التحقق"]
    # Form is explicitly not a validation result, without any overclaim phrase
    assert "is not a validation result" in text("UI_ED_FORM_NOTE", "en")
    assert "ليست نتيجة تحقق" in text("UI_ED_FORM_NOTE", "ar")
    for claim in ("has been validated", "is validated", "is confirmed", "is verified"):
        assert claim not in text("UI_ED_FORM_NOTE", "en").lower()


# ---------------------------------------------------------------------------
# 1 / 2 / 10 / 12 / 13 / 15 — the rendered report on a real project
# ---------------------------------------------------------------------------

def _report(c, sid):
    return c.get(f"/session/{sid}/deliverable").get_data(as_text=True)


def _blocks(page):
    return re.findall(r'<div class="ev-details" data-ev-details>.*?</dl>\s*</div>', page, re.S)


def _visible(fragment):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", fragment))).strip()


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_report_section_2_shows_evidence_details(client, lang):
    sid = _start(client, lang=lang)
    for value in (MECH, MECH):
        _answer(client, sid, value)
    page = _report(client, sid)
    blocks = _blocks(page)
    assert len(blocks) == 2                    # Known Problem + Known Mechanism
    problem, mechanism = blocks
    # the blocks sit inside Section 2, after their own evidence statement
    s2 = page.index(problem)
    assert page.rindex(text("UI_B_DELIV_024", lang), 0, s2) > 0
    assert page.index(text("UI_B_DELIV_025", lang)) < page.index(mechanism)
    assert page.index(mechanism) < page.index('id="report-reasoning"')
    state = _live(sid)
    pkg = assemble_deliverable(state)["section_2_invention_summary"]
    for block, ev in ((problem, pkg["known_problem"]), (mechanism, pkg["known_mechanism"])):
        d = appmod._evidence_details(ev)
        for axis in ("form", "source", "validation"):
            assert html.escape(text(d[axis]["key"], lang)) in block, (axis, d[axis])
        assert html.escape(text("UI_ED_HEADING", lang)) in block
        for token in CANONICAL_TOKENS + tuple(PROHIBITED_TOKENS):
            assert token not in block, token
        visible = _visible(block).lower()
        for word in ("score", "tier", "rank", "%"):
            assert word not in visible, word
    # the mechanism is the inventor's own answer; the problem wrapper has no
    # recorded source — shown truthfully, never reclassified
    assert 'data-ed-source="owner-stated"' in mechanism
    assert pkg["known_problem"]["provenance"] != OWNER_STATED
    assert 'data-ed-source="legacy-unspecified"' in problem
    assert html.escape(text("UI_ED_SOURCE_LEGACY_UNSPECIFIED", lang)) in problem
    assert 'data-ed-validation="unvalidated"' in problem + mechanism
    # ONE short Form note for the section, after the evidence items
    assert page.count("data-ev-details-note") == 1
    assert page.index(mechanism) < page.index("data-ev-details-note") \
        < page.index('id="report-reasoning"')
    assert html.escape(text("UI_ED_FORM_NOTE", lang)) in page
    other = "ar" if lang == "en" else "en"
    assert html.escape(text("UI_ED_HEADING", other)) not in page


def test_no_mechanism_evidence_renders_no_mechanism_rows(client):
    sid = _start(client)
    state = _live(sid)
    assert state.known_mechanism is None
    page = _report(client, sid)
    pkg = assemble_deliverable(state)["section_2_invention_summary"]
    assert len(_blocks(page)) == (1 if pkg["known_problem"] else 0)
    assert page.count("data-ev-details-note") == (1 if pkg["known_problem"] else 0)


def test_package_fields_are_unchanged_and_carry_no_cap11_keys(client):
    sid = _start(client)
    for value in (MECH, MECH):
        _answer(client, sid, value)
    pkg = assemble_deliverable(_live(sid))
    s2 = pkg["section_2_invention_summary"]
    for ev in (s2["known_problem"], s2["known_mechanism"]):
        assert set(ev) == {"content", "quality", "quality_label", "provenance",
                           "validation_status", "validation_label", "evidence_id"}
    flat = repr(pkg)
    for marker in ("UI_ED_", "ev-details", "About this evidence", "evidence_details"):
        assert marker not in flat, marker


def test_report_render_changes_no_state_or_readiness(client):
    sid = _start(client)
    for value in (MECH, MECH):
        _answer(client, sid, value)
    state = _live(sid)
    before = pickle.dumps(state)
    readiness_before = (derive_readiness(state).overall_verified(),
                        derive_readiness(state).unverified_contexts())
    for _ in range(2):
        _report(client, sid)
    state = _live(sid)
    assert pickle.dumps(state) == before
    assert (derive_readiness(state).overall_verified(),
            derive_readiness(state).unverified_contexts()) == readiness_before


def test_pdf_source_carries_the_same_evidence_details(client, monkeypatch):
    sid = _start(client)
    for value in (MECH, MECH):
        _answer(client, sid, value)
    seen = {}
    real = appmod._render_pdf_bytes

    def spy(source):
        seen["source"] = source
        return real(source)
    monkeypatch.setattr(appmod, "_render_pdf_bytes", spy)
    assert client.post(f"/session/{sid}/deliverable.pdf", data={}).status_code == 200
    blocks = _blocks(seen["source"])
    assert len(blocks) == 2
    for block in blocks:
        for token in CANONICAL_TOKENS:
            assert token not in block, token


# ---------------------------------------------------------------------------
# 14 / 15 / 16 — out-of-scope surfaces are untouched
# ---------------------------------------------------------------------------

def test_session_page_section_9_and_cev_mev_are_untouched(client):
    sid = _start(client)
    for value in (MECH, MECH):
        _answer(client, sid, value)
    session = client.get(f"/session/{sid}").get_data(as_text=True)
    assert "data-ev-details" not in session and "ev-details" not in session
    assert html.escape(text("UI_ED_HEADING", "en")) not in session
    report = _report(client, sid)
    reasoning = report[report.index('id="report-reasoning"'):]
    reasoning = reasoning[:reasoning.index("</section>")]
    assert "ev-details" not in reasoning
    # the Commercial / Manufacturing "Standing" wording is the existing one
    assert text("UI_CEV_META_STANDING", "en") == "Standing"
    assert text("UI_CEV_META_STANDING_VALUE", "en") == "recorded, not checked by anyone"
    assert text("UI_MEV_META_STANDING_VALUE", "en") == "recorded, not checked by anyone"
