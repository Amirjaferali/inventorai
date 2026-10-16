"""IDEA-ENTRY-CLASSIFICATION-BOUNDARY-01 — /start refusal evidence.

An ordinary subject, setting, application or product category (farming,
irrigation, crops, gardening, mountains, the sky, the moon, satellites as
something observed) is not evidence of a non-activated engineering domain, so
it never refuses an idea on its own: the idea continues through the unchanged
canonical classifier and the existing explicit-consent paths. Words that name a
non-activated specialist TECHNOLOGY (drone, solar, robotics, and the Stage-28
satellite / space family: CubeSat, spacecraft, rocket engine / motor, launch
vehicle) still refuse, and explicit confirmation cannot override them. Medical
restrictions, activation, ties and consent are unchanged.
"""
import pytest

from engine import domain_activation
from engine.domain_rules import DomainResultKind, classify_domain
from tests.csrf_client import csrf_client
from web import app as web_app
from web.app import SESSION_STORE, app

ELEC = "electronics_electrical"
MECH = "mechanical"

# Ordinary context only — no engineering requirement outside the active domains.
CONTEXT_IDEAS = (
    "A device that helps with irrigation in my small farm when the soil gets dry",
    "Something for agriculture that tells me when my crops need water",
    "A sprayer that applies pesticide to fruit trees",
    "A tool that helps me with gardening on my balcony",
    "Something that warns hikers about falling rocks in mountain areas",
    "A small device that tells me if it will rain soon by watching the sky",
    "A night lamp that glows softly like the moon when my child is asleep",
    "A camera that tracks satellites in orbit from my backyard",
    "A water rocket launcher for kids made from plastic bottles",
)
# The idea depends on a non-activated specialist technology.
TECHNOLOGY_IDEAS = (
    "A drone that checks farms and sprays crops.",
    "A solar farm optimizer that validates panel wiring safety.",
    "A robotic arm that welds car frames on an assembly line",
    "A thermal control system for a CubeSat that keeps batteries warm in orbit",
    "A thermal blanket for a CubeSat",
    "A rocket engine nozzle for reaching low earth orbit",
    "A fairing latch for a small launch vehicle",
    "A docking clamp for a spacecraft",
)
# Fail-closed limitation: a technology word used only as product context is
# still refused (the token seam cannot tell context from dependency).
TECHNOLOGY_AS_CONTEXT_IDEAS = (
    "A holder that lets me mount my drone camera on my bike",
    "A toy robot that my kids can build to sort their toys",
    "A charger that uses a solar panel to charge my phone while camping",
)
MEDICAL_IDEAS = (
    "A device that diagnoses dementia by monitoring elderly behavior.",
    "A wearable that measures blood glucose and adjusts insulin",
    "A medical monitor that tracks heart rhythm and alerts doctors.",
)


@pytest.fixture
def activate(monkeypatch):
    def _activate(*domains):
        monkeypatch.setattr(domain_activation, "_ACTIVATED_DOMAINS", frozenset(domains))
    return _activate


def _post(idea, confirm=None, choice=None):
    data = {"idea": idea}
    if confirm is not None:
        data["domain_confirm"] = confirm
    if choice is not None:
        data["domain_choice"] = choice
    return csrf_client(app).post("/start", data=data, follow_redirects=False)


def _refused(resp, activated):
    body = resp.get_data(as_text=True)
    return (resp.status_code == 200 and "Location" not in resp.headers
            and web_app._unsupported_domain_message(activated) in body
            and 'name="domain_choice"' not in body)


def _chooser(resp):
    body = resp.get_data(as_text=True)
    return (resp.status_code == 200
            and web_app.DOMAIN_CHOICE_MESSAGE in body
            and 'name="domain_choice"' in body)


@pytest.mark.parametrize("idea", CONTEXT_IDEAS)
def test_ordinary_context_is_not_refusal_evidence(activate, idea):
    activate(ELEC, MECH)
    assert not web_app._has_strong_unsupported_evidence(idea.lower())
    assert classify_domain(idea).kind is DomainResultKind.NONE
    before = set(SESSION_STORE)
    assert _chooser(_post(idea))                       # explicit choice, nothing created
    assert set(SESSION_STORE) == before


@pytest.mark.parametrize("idea, domain", [(CONTEXT_IDEAS[0], ELEC), (CONTEXT_IDEAS[5], MECH)])
def test_context_idea_is_admitted_only_by_explicit_choice_and_consent(activate, idea, domain):
    activate(ELEC, MECH)
    pending = _post(idea, choice=domain)
    assert pending.status_code == 200 and "Location" not in pending.headers
    admitted = _post(idea, choice=domain, confirm=domain)
    assert admitted.status_code == 302
    sid = admitted.headers["Location"].rsplit("/", 1)[-1]
    assert SESSION_STORE.get(sid)["state"].domain == domain


def test_context_idea_under_sole_electronics_keeps_the_governed_consent(activate):
    activate(ELEC)
    idea = CONTEXT_IDEAS[1]
    assert not _refused(_post(idea), [ELEC])
    admitted = _post(idea, confirm=ELEC)
    assert admitted.status_code == 302


@pytest.mark.parametrize("idea", TECHNOLOGY_IDEAS + TECHNOLOGY_AS_CONTEXT_IDEAS + MEDICAL_IDEAS)
def test_non_activated_technology_and_medical_stay_refused(activate, idea):
    activate(ELEC, MECH)
    assert web_app._has_strong_unsupported_evidence(idea.lower())
    before = set(SESSION_STORE)
    for kwargs in ({}, {"choice": MECH, "confirm": MECH}, {"choice": ELEC, "confirm": ELEC}):
        assert _refused(_post(idea, **kwargs), [ELEC, MECH]), kwargs
    assert set(SESSION_STORE) == before


def test_cubesat_refusal_comes_from_the_space_family_not_the_software_accident(activate):
    # Before the correction "A thermal control system for a CubeSat ..." was
    # refused only because "system" made the non-activated software pack the
    # sole top scorer; the same idea without "system" reached the chooser.
    activate(ELEC, MECH)
    no_system = "A thermal blanket for a CubeSat"
    assert classify_domain(no_system).kind is DomainResultKind.NONE
    assert _refused(_post(no_system), [ELEC, MECH])


@pytest.mark.parametrize("base", [
    "A lever that lifts the lid of a heavy box using a spring",
    "A circuit with a sensor, a switch and a microcontroller",
    "I want something that waters my plants when necessary",
])
@pytest.mark.parametrize("context", [
    " on my farm", " for my crops", " for irrigation", " in the mountains",
    " under the night sky", " while watching satellites",
])
def test_adding_ordinary_context_never_changes_the_outcome(activate, base, context):
    # The correction generalizes by what refusal evidence IS (a technology
    # name), not by listing admissible subjects: context leaves the canonical
    # classification and the /start outcome exactly as without it.
    activate(ELEC, MECH)
    assert classify_domain(base + context) == classify_domain(base)
    plain = _post(base).get_data(as_text=True)
    framed = _post(base + context).get_data(as_text=True)
    for marker in ('name="domain_choice"', 'name="domain_confirm"', '<p class="error"'):
        assert (marker in plain) == (marker in framed), marker


def test_refusal_vocabulary_names_technologies_not_contexts():
    removed = {"crop", "crops", "agriculture", "agricultural", "pesticide",
               "herbicide", "irrigation", "farm", "farms"}
    assert not removed & web_app._STRONG_UNSUPPORTED_WORDS
    never_registered = web_app._STRONG_UNSUPPORTED_WORD_FAMILIES[None]
    assert {"drone", "solar", "robot", "robotics", "cubesat", "spacecraft"} <= never_registered
    for context_word in ("satellite", "orbit", "space", "moon", "sky", "mountain", "garden"):
        assert context_word not in web_app._STRONG_UNSUPPORTED_WORDS
        assert not any(context_word == s for s in web_app._STRONG_UNSUPPORTED_SUBSTRINGS)
