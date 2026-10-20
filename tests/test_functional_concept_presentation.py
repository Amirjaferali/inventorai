"""FUNCTIONAL-CONCEPT-PRESENTATION-01 — the report / PDF "your idea, by topic"
view of the inventor's own current answers.

Presentation only. An answer is placed by the gap its question was served from
(``gap_context``) and a provisional assumption by its disposition; text is never
read to place it. Superseded and non-inventor records never appear, missing
topics read as not recorded, and the canonical package, the Requirement
Landscape, the session page and the state are unchanged. Synthetic ideas only.
"""
import copy
import html as _html
import re

import pytest

import web.app as appmod
from engine.deliverable_assembler import assemble_deliverable
from engine.idea_state import (
    IdeaState, AssertionRecord, DISPOSITION_ANSWERED, DISPOSITION_UNKNOWN,
    DISPOSITION_DEFERRED, DISPOSITION_PROVISIONAL_ASSUMPTION, OWNER_STATED,
    LEGACY_UNSPECIFIED, SYSTEM_INFERRED,
)
from engine.requirement_landscape import derive_requirement_landscape
from tests.csrf_client import csrf_client
from web import ui_text

ELEC = "electronics_electrical"
IDEA = ("I want something that waters my plants while I'm away on holiday for two "
        "weeks.")
OPERATION = ("It checks the soil every morning and lets water drip from a bottle when "
             "the soil is dry.")


def _rec(n, gap, content, disposition=DISPOSITION_ANSWERED, provenance=OWNER_STATED,
         superseded=False):
    return AssertionRecord(record_id=f"rec_{n}", iteration=n, gap_context=gap,
                           content=content, disposition=disposition,
                           provenance=provenance,
                           superseded_by="rec_x" if superseded else None)


def _state(*records):
    state = IdeaState(idea_id="synthetic")
    state.domain = ELEC
    state.assertions.extend(records)
    return state


def _topics(view):
    return {t["key"]: [a["text"] for a in t["answers"]] for t in view["topics"]}


# ─── adapter: placement, filtering, honesty ─────────────────────────────────

def test_answers_are_placed_by_question_topic_in_a_fixed_order():
    view = appmod._functional_concept_view(_state(
        _rec(1, "MECHANISM_COMPLETENESS", "It opens a valve when the soil is dry."),
        _rec(2, "PROBLEM_MECHANISM_FIT", "My plants die when I travel."),
        _rec(3, "PHYSICAL_FEASIBILITY", "It must work indoors for two weeks."),
        _rec(4, "BOUNDARY_AMBIGUITY", "Only indoor pots, not a garden."),
        _rec(5, "ASSUMPTION_INVENTORY", "I assume one bottle is enough.")))
    assert view["available"] and view["unplaced"] == 0
    assert [t["key"] for t in view["topics"]] == \
        ["goal", "operation", "conditions", "scope", "assumptions"]
    assert _topics(view) == {
        "goal": ["My plants die when I travel."],
        "operation": ["It opens a valve when the soil is dry."],
        "conditions": ["It must work indoors for two weeks."],
        "scope": ["Only indoor pots, not a garden."],
        "assumptions": ["I assume one bottle is enough."]}


def test_text_is_never_read_to_place_an_answer():
    # words that sound like another topic do not move an answer
    view = appmod._functional_concept_view(_state(
        _rec(1, "BOUNDARY_AMBIGUITY", "I assume it works by checking the soil.")))
    assert _topics(view)["scope"] == ["I assume it works by checking the soil."]
    assert _topics(view)["assumptions"] == [] and _topics(view)["operation"] == []


def test_only_current_inventor_answers_appear():
    view = appmod._functional_concept_view(_state(
        _rec(1, "MECHANISM_COMPLETENESS", "old wording", superseded=True),
        _rec(2, "MECHANISM_COMPLETENESS", "corrected wording"),
        _rec(3, "MECHANISM_COMPLETENESS", "inferred", provenance=SYSTEM_INFERRED),
        _rec(4, "MECHANISM_COMPLETENESS", "not sure", disposition=DISPOSITION_UNKNOWN),
        _rec(5, "MECHANISM_COMPLETENESS", "later", disposition=DISPOSITION_DEFERRED)))
    assert _topics(view)["operation"] == ["corrected wording"]


def test_declared_provisional_assumptions_join_the_assumptions_topic_labelled():
    view = appmod._functional_concept_view(_state(
        _rec(1, "PHYSICAL_FEASIBILITY", "Probably batteries will do.",
             disposition=DISPOSITION_PROVISIONAL_ASSUMPTION),
        _rec(2, "ASSUMPTION_INVENTORY", "I assume the tube never blocks.")))
    answers = view["topics"][4]["answers"]
    assert [(a["text"], a["provisional"]) for a in answers] == [
        ("Probably batteries will do.", True), ("I assume the tube never blocks.", False)]
    assert _topics(view)["conditions"] == []


def test_verbatim_text_exact_repeats_once_legacy_source_labelled():
    view = appmod._functional_concept_view(_state(
        _rec(1, "MECHANISM_COMPLETENESS", "  Same answer.\nSecond line. "),
        _rec(2, "MECHANISM_COMPLETENESS", "Same answer.\nSecond line."),
        _rec(3, "MECHANISM_COMPLETENESS", "Older answer.", provenance=LEGACY_UNSPECIFIED)))
    answers = view["topics"][1]["answers"]
    assert [a["text"] for a in answers] == ["Same answer.\nSecond line.", "Older answer."]
    assert [a["legacy_source"] for a in answers] == [False, True]


def _rows(view, key):
    topic = next(t for t in view["topics"] if t["key"] == key)
    return [(a["text"], a["provisional"], a["legacy_source"]) for a in topic["answers"]]


@pytest.mark.parametrize("first,second", [(OWNER_STATED, LEGACY_UNSPECIFIED),
                                          (LEGACY_UNSPECIFIED, OWNER_STATED)])
def test_equal_wording_with_different_sources_keeps_both_rows(first, second):
    view = appmod._functional_concept_view(_state(
        _rec(1, "MECHANISM_COMPLETENESS", "It opens a valve.", provenance=first),
        _rec(2, "MECHANISM_COMPLETENESS", "It opens a valve.", provenance=second)))
    assert _rows(view, "operation") == [
        ("It opens a valve.", False, first == LEGACY_UNSPECIFIED),
        ("It opens a valve.", False, second == LEGACY_UNSPECIFIED)]


@pytest.mark.parametrize("first,second", [
    (DISPOSITION_ANSWERED, DISPOSITION_PROVISIONAL_ASSUMPTION),
    (DISPOSITION_PROVISIONAL_ASSUMPTION, DISPOSITION_ANSWERED)])
def test_equal_wording_with_different_dispositions_keeps_both_rows(first, second):
    view = appmod._functional_concept_view(_state(
        _rec(1, "ASSUMPTION_INVENTORY", "One bottle is enough.", disposition=first),
        _rec(2, "ASSUMPTION_INVENTORY", "One bottle is enough.", disposition=second)))
    assert _rows(view, "assumptions") == [
        ("One bottle is enough.", first == DISPOSITION_PROVISIONAL_ASSUMPTION, False),
        ("One bottle is enough.", second == DISPOSITION_PROVISIONAL_ASSUMPTION, False)]


@pytest.mark.parametrize("disposition,provenance", [
    (DISPOSITION_ANSWERED, OWNER_STATED), (DISPOSITION_ANSWERED, LEGACY_UNSPECIFIED),
    (DISPOSITION_PROVISIONAL_ASSUMPTION, OWNER_STATED)])
def test_identical_wording_and_labels_are_shown_once(disposition, provenance):
    records = [_rec(n, "ASSUMPTION_INVENTORY", "One bottle is enough.",
                    disposition=disposition, provenance=provenance) for n in (1, 2)]
    rows = _rows(appmod._functional_concept_view(_state(*records)), "assumptions")
    assert rows == [("One bottle is enough.",
                     disposition == DISPOSITION_PROVISIONAL_ASSUMPTION,
                     provenance == LEGACY_UNSPECIFIED)]


def test_colliding_rows_render_each_with_its_own_label():
    state = _state(
        _rec(1, "ASSUMPTION_INVENTORY", "One bottle is enough."),
        _rec(2, "ASSUMPTION_INVENTORY", "One bottle is enough.",
             disposition=DISPOSITION_PROVISIONAL_ASSUMPTION),
        _rec(3, "MECHANISM_COMPLETENESS", "It opens a valve."),
        _rec(4, "MECHANISM_COMPLETENESS", "It opens a valve.",
             provenance=LEGACY_UNSPECIFIED))
    view = appmod._functional_concept_view(state)
    with appmod.app.test_request_context():
        section = appmod.render_template("deliverable.html", sid="s", package=assemble_deliverable(state),
                                         eligible=False, reconstructed_deliverable=False,
                                         functional_concept=view)
    section = _section(section)
    assumptions = section[section.index('data-fc-topic="assumptions"'):]
    operation = section[section.index('data-fc-topic="operation"'):
                        section.index('data-fc-topic="conditions"')]
    assert assumptions.count("data-fc-answer") == 2
    assert assumptions.count("data-fc-provisional") == 1
    assert operation.count("data-fc-answer") == 2
    assert operation.count("data-fc-legacy") == 1


def test_unplaceable_answers_are_counted_never_guessed():
    view = appmod._functional_concept_view(_state(
        _rec(1, None, "No topic recorded."),
        _rec(2, "NOT_A_GAP", "Unknown topic."),
        _rec(3, "EXPERTISE_GAP_AWARENESS", "I would ask a friend.")))   # known, not shown
    assert view["unplaced"] == 2
    assert all(t["answers"] == [] for t in view["topics"])


def test_no_state_and_broken_state():
    assert appmod._functional_concept_view(None) is None

    class Broken:
        @property
        def assertions(self):
            raise RuntimeError("boom")
    assert appmod._functional_concept_view(Broken()) == {"available": False}


def test_the_view_mutates_nothing_and_leaves_canonical_outputs_unchanged():
    state = _state(_rec(1, "MECHANISM_COMPLETENESS", OPERATION),
                   _rec(2, "BOUNDARY_AMBIGUITY", "Only indoor pots."))
    before = copy.deepcopy(state)
    package, landscape = assemble_deliverable(state), derive_requirement_landscape(state)
    appmod._functional_concept_view(state)
    assert state.assertions == before.assertions
    assert assemble_deliverable(state) == package
    assert derive_requirement_landscape(state) == landscape
    assert "functional_concept" not in package


# ─── rendering: report, PDF, EN / AR ────────────────────────────────────────

@pytest.fixture()
def client():
    appmod.app.config["TESTING"] = True
    with csrf_client(appmod.app) as c:
        yield c


def _answer_first_question(c, sid, text):
    body = c.get(f"/session/{sid}").get_data(as_text=True)
    token = _html.unescape(re.search(r'name="answer_token" value="([^"]+)"', body).group(1))
    assert c.post(f"/session/{sid}", data={"response": text, "action": "answered",
                                          "answer_token": token}).status_code == 302


def _journey(c, lang="en"):
    if lang == "ar":
        c.post("/ui-language", data={"lang": "ar"})
    r = c.post("/start", data={"idea": IDEA, "domain_choice": ELEC, "domain_confirm": ELEC})
    sid = r.headers["Location"].rsplit("/", 1)[-1]
    _answer_first_question(c, sid, OPERATION)
    return sid


def _section(body):
    start = body.index("data-functional-concept")
    return body[start:body.index("report-return", start)]


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_report_shows_the_topics_verbatim_and_unrecorded_topics(client, lang):
    sid = _journey(client, lang)
    body = client.get(f"/session/{sid}/deliverable").get_data(as_text=True)
    section = _section(body)
    for key in ("UI_FC_HEADING", "UI_FC_BOUNDARY", "UI_FC_TOPIC_OPERATION",
                "UI_FC_TOPIC_SCOPE", "UI_FC_NOT_RECORDED"):
        assert ui_text.UI_STRINGS[key][lang] in _html.unescape(section), key
    operation = section[section.index('data-fc-topic="operation"'):
                        section.index('data-fc-topic="conditions"')]
    assert OPERATION in _html.unescape(operation)
    assert 'dir="auto"' in operation
    scope = section[section.index('data-fc-topic="scope"'):
                    section.index('data-fc-topic="assumptions"')]
    assert "data-fc-not-recorded" in scope
    if lang == "ar":
        assert 'dir="rtl"' in body


def test_inventor_text_is_escaped(client):
    r = client.post("/start", data={"idea": IDEA, "domain_choice": ELEC,
                                    "domain_confirm": ELEC})
    sid = r.headers["Location"].rsplit("/", 1)[-1]
    _answer_first_question(client, sid, "It opens <b>the valve</b> & drips water when dry.")
    section = _section(client.get(f"/session/{sid}/deliverable").get_data(as_text=True))
    assert "<b>the valve</b>" not in section
    assert "&lt;b&gt;the valve&lt;/b&gt;" in section


def test_unavailable_view_renders_its_notice(client, monkeypatch):
    sid = _journey(client)
    monkeypatch.setattr(appmod, "_functional_concept_view", lambda state: {"available": False})
    section = _section(client.get(f"/session/{sid}/deliverable").get_data(as_text=True))
    assert "data-fc-unavailable" in section and "data-fc-topic" not in section


def test_pdf_receives_the_same_view_as_the_html_report(client, monkeypatch):
    sid = _journey(client)
    seen = []
    real = appmod.render_template

    def spy(name, **kwargs):
        if name == "deliverable.html":
            seen.append((kwargs.get("deliverable_base"), kwargs.get("functional_concept")))
        return real(name, **kwargs)
    monkeypatch.setattr(appmod, "render_template", spy)
    client.get(f"/session/{sid}/deliverable")
    assert client.post(f"/session/{sid}/deliverable.pdf").status_code == 200
    (html_base, html_view), (pdf_base, pdf_view) = seen
    assert (html_base, pdf_base) == (None, "pdf_base.html")
    assert html_view == pdf_view and html_view["available"]
    assert OPERATION in [a["text"] for t in pdf_view["topics"] for a in t["answers"]]


def test_session_page_is_unchanged(client):
    sid = _journey(client)
    assert "data-functional-concept" not in client.get(f"/session/{sid}").get_data(as_text=True)
