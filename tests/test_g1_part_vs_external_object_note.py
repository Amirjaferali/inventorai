# -*- coding: utf-8 -*-
"""G1-2-PART-VS-EXTERNAL-OBJECT-01 — one static note on the integrated-entry form.

Before submitting the Stage-15 "parts of your invention" form, a nontechnical
inventor reads, in English and Arabic, that only the parts the invention is made
of are listed; that something the invention works on or is used with is not
automatically one of its parts; that a ready-made part they buy and build in does
count; that they choose each part's name and function; and that "Not sure" is
acceptable instead of guessing.

Guidance only: nothing is prefilled, inferred, checked or refused because of it.
The direct start, the integrated start, the "Not sure" answer and the exact
saving of the inventor's own words are unchanged. Synthetic ideas only.
"""
import html as _html
import re

import pytest

from tests.test_stage15_integrated_invention_entry import (  # noqa: F401  (fixture)
    ELEC, ELEC_IDEA, MECH, MECH_IDEA, TIE_IDEA, _compose, _created, _live, _project_count,
    _subsystem_rows, client)
from engine.idea_state import OWNER_STATED, UNVALIDATED
from web import ui_text

NOTE = "data-s15-parts-note"


def _note(body):
    m = re.search(r"<p[^>]*" + NOTE + r"[^>]*>(.*?)</p>", body, re.S)
    return _html.unescape(m.group(1)) if m else None


# ── 1. visible before submission, in EN and AR ────────────────────────────
@pytest.mark.parametrize("lang", ["en", "ar"])
def test_the_note_is_shown_on_the_form_before_any_part_field(client, lang):
    if lang == "ar":
        assert client.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    body = client.post("/start", data={"idea": TIE_IDEA}).get_data(as_text=True)
    assert "data-composition-form" in body
    assert _note(body) == ui_text.text("UI_S15_PARTS_NOTE", lang)
    # after "If yes, describe each part" and before the first part field
    assert _html.unescape(body).index(ui_text.text("UI_S15_IF_YES", lang)) < body.index(NOTE) \
        < body.index('name="mech_part_name"')
    assert body.count(NOTE) == 1


def test_the_note_says_each_required_point():
    en = ui_text.text("UI_S15_PARTS_NOTE", "en")
    for phrase in ("only the parts your invention is made of",
                   "is not automatically one of its parts",
                   "A ready-made part you buy and build into your invention",
                   "does count as a part",
                   "You choose each part's name and what it does",
                   "“Not sure”", "you do not need to guess"):
        assert phrase in en, phrase
    ar = ui_text.text("UI_S15_PARTS_NOTE", "ar")
    for phrase in ("الأجزاء التي يتكوّن منها اختراعك", "ليس تلقائيًا جزءًا منه",
                   "القطعة الجاهزة التي تشتريها وتركّبها في اختراعك", "فهي جزء منه",
                   "أنت من يختار اسم كل جزء وما يفعله", ui_text.text("UI_S15_NOT_SURE", "ar"),
                   "ولا داعي للتخمين"):
        assert phrase in ar, phrase


def test_the_note_stays_when_the_form_is_shown_again_after_an_error(client):
    r = _compose(client, TIE_IDEA, mech_part_name="")
    body = r.get_data(as_text=True)
    # the existing missing-field refusal (400, nothing saved) shows the form again
    assert r.status_code == 400 and "data-composition-form" in body
    assert ui_text.text("UI_S15_ERR_FIELDS", "en") in _html.unescape(body)
    assert _note(body) == ui_text.text("UI_S15_PARTS_NOTE", "en")


# ── 2. direct start and integrated start stay valid ──────────────────────
def test_the_direct_start_is_unchanged_and_shows_no_note(client):
    assert NOTE not in client.get("/").get_data(as_text=True)
    for idea, domain in ((ELEC_IDEA, ELEC), (MECH_IDEA, MECH)):
        first = client.post("/start", data={"idea": idea})
        assert first.status_code == 200 and NOTE not in first.get_data(as_text=True)
        sid = _created(client.post("/start", data={"idea": idea, "domain_confirm": domain}))
        assert _live(sid).domain == domain and _subsystem_rows(sid) == []


# ── 3, 4, 6. the inventor's words are saved exactly; a bought part is valid;
#            nothing is inferred from the note's examples ────────────────
@pytest.mark.parametrize("lang, parts", [
    ("en", {"mech_part_name": "Rolling toolbox lid", "mech_part_function": "Holds the fan above the tools.",
            "elec_part_name": "Store-bought battery fan",
            "elec_part_function": "Blows air to cool the tools while they charge."}),
    ("ar", {"mech_part_name": "غطاء صندوق العدّة", "mech_part_function": "يحمل المروحة فوق العِدَد.",
            "elec_part_name": "مروحة بطارية جاهزة اشتريتها",
            "elec_part_function": "تنفخ الهواء لتبريد العِدَد أثناء شحنها."}),
])
def test_a_purchased_part_is_saved_exactly_as_written(client, lang, parts):
    before = _project_count()
    sid = _created(_compose(client, TIE_IDEA, focus=ELEC, lang=lang, **parts))
    assert _project_count() == before + 1
    rows = _subsystem_rows(sid)
    assert [(r[3], r[4], r[5], r[6], r[7]) for r in rows] == [
        (MECH, parts["mech_part_name"], parts["mech_part_function"], OWNER_STATED, UNVALIDATED),
        (ELEC, parts["elec_part_name"], parts["elec_part_function"], OWNER_STATED, UNVALIDATED)]
    assert _live(sid).domain == ELEC


def test_the_note_decides_nothing_for_the_inventor(client):
    # the form opens with every part field empty: nothing from the examples is prefilled
    body = client.post("/start", data={"idea": TIE_IDEA}).get_data(as_text=True)
    for field in ("mech_part_name", "elec_part_name"):
        assert re.search(r'<input[^>]*name="%s"[^>]*value=""' % field, body), field
    for field in ("mech_part_function", "elec_part_function"):
        assert re.search(r'<textarea[^>]*name="%s"[^>]*>\s*</textarea>' % field, body), field
    assert not re.search(r'name="(composition_answer|initial_focus)"[^>]*checked', body)
    # an object the invention acts on, declared as a part, is still the inventor's
    # declaration: saved verbatim, with no warning, refusal or substitution
    parts = {"mech_part_name": "Rolling toolbox", "mech_part_function": "Holds my tools and carries the fan in its lid.",
             "elec_part_name": "Power tools", "elec_part_function": "They charge inside the box."}
    sid = _created(_compose(client, TIE_IDEA, focus=MECH, **parts))
    assert [(r[4], r[5]) for r in _subsystem_rows(sid)] == [
        (parts["mech_part_name"], parts["mech_part_function"]),
        (parts["elec_part_name"], parts["elec_part_function"])]


# ── 5. "Not sure" is unchanged ───────────────────────────────────────────
def test_not_sure_still_saves_nothing(client):
    before = _project_count()
    r = _compose(client, TIE_IDEA, answer="not_sure")
    assert r.status_code == 200
    assert ui_text.text("UI_S15_GUIDE_NOT_SURE", "en") in _html.unescape(r.get_data(as_text=True))
    assert _project_count() == before and _subsystem_rows() == []
