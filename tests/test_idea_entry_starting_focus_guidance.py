"""IDEA-ENTRY-STARTING-FOCUS-GUIDANCE-01 — the /start no-match chooser.

When the classifier finds no domain in an ordinary-language idea and two
specialist domains are active, the chooser now explains in EN / AR that the
choice only decides which questions the user starts with (not a technical
classification, feasibility or correctness) and that it stays fixed for the
project, and shows each starting point's FIRST committed Path-N mechanism
question as a plain-language example. Classification, activation, the radio
values / order / required attribute, consent and admission are unchanged; if
any example is unavailable the chooser renders exactly as before.
"""
from tests.csrf_client import csrf_client
import html as _html
import re

import pytest

from engine import domain_activation
from engine import path_n_questions
from engine.domain_rules import DomainResultKind, classify_domain
from engine.idea_state import MECHANISM_COMPLETENESS
from web import ui_text
from web.app import SESSION_STORE, app

ELEC = "electronics_electrical"
MECH = "mechanical"
PLANT_IDEA = ("I want something that waters my plants when necessary, but I do "
              "not know how it should work.")
_RADIO_RE = re.compile(
    r'<input type="radio" name="domain_choice" value="([^"]+)"([^>]*)>\s*(.*?)\s*</label>',
    re.S)
_EXAMPLE_RE = re.compile(
    r'<p class="starting-focus-example"[^>]*>(.*?)<bdi dir="auto">(.*?)</bdi></p>', re.S)


@pytest.fixture
def activate(monkeypatch):
    def _activate(*domains):
        monkeypatch.setattr(domain_activation, "_ACTIVATED_DOMAINS", frozenset(domains))
    return _activate


@pytest.fixture
def client():
    return csrf_client(app)


def _post(client, idea, confirm=None, choice=None):
    data = {"idea": idea}
    if confirm is not None:
        data["domain_confirm"] = confirm
    if choice is not None:
        data["domain_choice"] = choice
    return client.post("/start", data=data, follow_redirects=False)


def _set_lang(client, lang):
    assert client.post("/ui-language", data={"lang": lang}).status_code in (302, 303)


def _first_question(domain):
    return path_n_questions.get_served_question(MECHANISM_COMPLETENESS, 0, domain=domain)


def _norm(text):
    return " ".join(_html.unescape(text).split())


def _radios(body):
    return [(value, "required" in attrs) for value, attrs, _label in _RADIO_RE.findall(body)]


def _examples(body):
    return [(_norm(label), _norm(example)) for label, example in _EXAMPLE_RE.findall(body)]


def test_plant_watering_idea_reaches_the_no_match_chooser():
    assert classify_domain(PLANT_IDEA).kind is DomainResultKind.NONE


def test_en_chooser_explains_meaning_and_shows_committed_examples(activate, client):
    activate(ELEC, MECH)
    before = len(SESSION_STORE)
    resp = _post(client, PLANT_IDEA)
    body = resp.get_data(as_text=True)
    assert resp.status_code == 200 and "Location" not in resp.headers
    assert len(SESSION_STORE) == before                    # nothing created
    note = ui_text.UI_STRINGS["UI_B_START_033"]["en"]
    assert _norm(note) in _norm(body)
    for phrase in ("do not need to know which engineering field",
                   "if both seem to fit, choose the one that is easier for you to answer",
                   "only decides which set of questions guides the analysis of your idea",
                   "not a technical classification",
                   "says nothing about whether your idea is feasible or correct",
                   "stays fixed for this project"):
        assert phrase in note, phrase
    # radio values, order and `required` unchanged; one example per option, in order
    assert _radios(body) == [(ELEC, True), (MECH, True)]
    label = ui_text.UI_STRINGS["UI_B_START_034"]["en"]
    assert _examples(body) == [(label, _norm(_first_question(ELEC).text)),
                               (label, _norm(_first_question(MECH).text))]


def test_ar_chooser_uses_committed_arabic_and_no_english_leak(activate, client):
    activate(ELEC, MECH)
    _set_lang(client, "ar")
    body = _post(client, PLANT_IDEA).get_data(as_text=True)
    assert _norm(ui_text.UI_STRINGS["UI_B_START_033"]["ar"]) in _norm(body)
    assert ui_text.UI_STRINGS["UI_B_START_033"]["en"][:40] not in body
    label = ui_text.UI_STRINGS["UI_B_START_034"]["ar"]
    assert _examples(body) == [(label, _norm(_first_question(ELEC).text_ar)),
                               (label, _norm(_first_question(MECH).text_ar))]
    for domain in (ELEC, MECH):
        assert _first_question(domain).text not in body
    assert _radios(body) == [(ELEC, True), (MECH, True)]


@pytest.mark.parametrize("failure", ["missing", "raises"])
def test_unavailable_examples_fall_back_to_the_unchanged_chooser(activate, client,
                                                                 monkeypatch, failure):
    real = path_n_questions.get_served_question

    def _broken(gap_type, iterations_open, domain=None):
        if domain == MECH:
            if failure == "raises":
                raise ValueError("artifact unavailable")
            return None
        return real(gap_type, iterations_open, domain=domain)

    monkeypatch.setattr(path_n_questions, "get_served_question", _broken)
    activate(ELEC, MECH)
    resp = _post(client, PLANT_IDEA)
    body = resp.get_data(as_text=True)
    assert resp.status_code == 200
    assert _examples(body) == []                            # all or nothing
    assert 'class="starting-focus-example"' not in body
    assert _norm(ui_text.UI_STRINGS["UI_B_START_033"]["en"]) in _norm(body)
    assert _radios(body) == [(ELEC, True), (MECH, True)]


def test_choice_and_confirmation_still_admit_exactly_the_chosen_focus(activate, client):
    activate(ELEC, MECH)
    pending = _post(client, PLANT_IDEA, choice=MECH)
    assert pending.status_code == 200 and "Location" not in pending.headers
    assert 'class="starting-focus-note"' not in pending.get_data(as_text=True)
    admitted = _post(client, PLANT_IDEA, choice=MECH, confirm=MECH)
    assert admitted.status_code == 302 and "/session/" in admitted.headers["Location"]
    sid = admitted.headers["Location"].rsplit("/", 1)[-1]
    assert SESSION_STORE.get(sid)["state"].domain == MECH


def test_single_match_and_sole_domain_pages_show_no_guidance(activate, client):
    activate(ELEC, MECH)
    single = _post(client, "a circuit with a sensor, a switch and a microcontroller")
    assert single.status_code == 200
    body = single.get_data(as_text=True)
    assert 'class="starting-focus-note"' not in body
    assert 'class="starting-focus-example"' not in body
    activate(ELEC)
    sole = csrf_client(app).get("/").get_data(as_text=True)
    assert 'class="starting-focus-note"' not in sole
