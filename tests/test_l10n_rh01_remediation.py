"""L10N-RH-01 — Bounded remediation of the 3 registered non-blocking observations.

Authoritative registration: `docs/governance/INVENTORAI_CAPABILITY_ENRICHMENT_REGISTER.md`
`## L10N-RH-01` section (registered inside the CF-2 formal closure gate). Corrected
reassessment: `docs/governance/L10N_RH01_REASSESSMENT_AND_MECHANICAL_ACTIVATION_
READINESS_RECORD.md`.

This file adds genuinely load-bearing regression guards for the 3 registered
observations — each one specifically designed so a reintroduction of the
original defect makes the relevant test fail, unlike the pre-existing
tautological assertions (which compare rendered output against the SAME
`ui_text.UI_STRINGS` dict a mutation would corrupt, or never exercise the
real production call seam at all):

  1. Arabic broadened-activation negative-semantic-guard gap (`UI_B_START_026`) —
     an independent, hardcoded-literal positive/negative content check.
  2. `SERVICE_UNAVAILABLE` localization-path regression-guard gap — exercises
     the REAL `/start` and `/start_ilt002_water_leak` production call seams
     (both call sites) via a forced durable-store failure, not
     `ui_text.localize_message()` in isolation.
  3. Present-confirm Arabic checkbox-label wording (`UI_B_START_024`,
     `start_present_confirm_label`, broadened non-electronics branch) — a
     register check (first-person consent vs. prompt/instruction), remediated
     in `web/ui_text.py` this same gate. `UI_B_START_023` (electronics-only,
     already accepted, production-reachable) and `UI_B_START_030`
     (`start_confirm_label`, a different template variable, already correctly
     first-person) are explicitly OUT OF SCOPE and untouched.

No Mechanical activation. No Tier-1 label work (both new Arabic/English
strings below remain strictly domain-neutral — no domain is ever named).
"""

import os
import re
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from engine import domain_activation
from web import ui_text
from web.app import app

ELEC = "electronics_electrical"
MECH = "mechanical"

MECH_IDEA = "A hinge mounted bracket with a lever and a spring latch"


@pytest.fixture
def activate(monkeypatch):
    """Self-restoring activation double (no real activation) — same pattern as
    tests/test_cf2_arabic_localization_remainder.py."""
    def _activate(*domains):
        monkeypatch.setattr(
            domain_activation, "_ACTIVATED_DOMAINS", frozenset(domains))
    return _activate


@pytest.fixture
def client():
    return app.test_client()


def _set_lang(client, lang):
    resp = client.post("/ui-language", data={"lang": lang})
    assert resp.status_code in (302, 303)


def _post(client, idea, confirm=None, choice=None):
    data = {"idea": idea}
    if confirm is not None:
        data["domain_confirm"] = confirm
    if choice is not None:
        data["domain_choice"] = choice
    return client.post("/start", data=data, follow_redirects=False)


def _error_paragraph(body):
    """The `<p class="error">...</p>` content only — same extraction as
    tests/test_cf2_arabic_localization_remainder.py, needed here because the
    page's OTHER copy (e.g. the broadened-activation scope sentence,
    UI_B_START_026) can incidentally share common phrases ("يرجى تأكيد")
    with the present-confirm text under test, so whole-page substring checks
    would be unreliable."""
    m = re.search(r'<p class="error">(.*?)</p>', body, re.S)
    return m.group(1) if m else None


class _FailingStore:
    """Forces the real /start and ILT-002 durable-creation except-Exception
    fallback, without touching real persistence."""
    def create_project(self, *a, **kw):
        raise RuntimeError("L10N-RH-01 remediation: forced durable-store failure")


# ==================================================== 0. real activation honesty
def test_baseline_real_activation_unchanged():
    """domain_activation.activated_domains() (the real function, not the
    internal _ACTIVATED_DOMAINS constant) returns a list, not a frozenset —
    confirmed here so later assertions in this file use the correct type."""
    result = domain_activation.activated_domains()
    assert result == ["electronics_electrical", "mechanical"]
    assert isinstance(result, list)


# ============== 1. Observation #1 — broadened negative-semantic guard (LOAD-BEARING)
def test_red_broadened_scope_sentence_ar_independent_semantic_guard(activate, client):
    """The pre-existing test (`test_green_ar_broadened_generalized_context_
    no_english_leak`) asserts `ui_text.UI_STRINGS["UI_B_START_026"]["ar"] in
    body` — tautological, since it derives its expected value from the SAME
    dict a mutation would corrupt. This test instead uses an independently
    hardcoded literal excerpt of the TRUE claim (a plural specialist-domain
    claim) and a hardcoded literal excerpt of a plausible FALSE
    electronics-only narrowing claim, neither derived from `ui_text.
    UI_STRINGS`. A mutation replacing UI_B_START_026's Arabic value with a
    false electronics-only claim fails this test on both assertions."""
    activate(ELEC, MECH)
    _set_lang(client, "ar")
    resp = client.get("/")
    body = resp.get_data(as_text=True)
    assert "أكثر من مجال متخصص واحد" in body
    assert "الإلكترونيات فقط" not in body


# ========= 2. Observation #2 — SERVICE_UNAVAILABLE real production seam (LOAD-BEARING)
@pytest.mark.parametrize("route,data,needs_electronics_activation", [
    ("/start", {"idea": "ESP32 microcontroller circuit with a voltage sensor",
                "domain_confirm": ELEC}, True),
    ("/start_ilt002_water_leak", {"idea": "a water leak sensor circuit"}, False),
])
def test_red_service_unavailable_real_call_seam_ar(
        client, monkeypatch, route, data, needs_electronics_activation):
    """Exercises the REAL production call seam at BOTH SERVICE_UNAVAILABLE
    call sites (web/app.py:1802 inside start(), and web/app.py:1842 inside
    _finalize_started_session(), reached here via start_ilt002_water_leak) —
    not `ui_text.localize_message()` in isolation, which the pre-existing
    test (`test_green_ar_service_unavailable_localize_message_wired`)
    explicitly documents it does NOT do ("this suite does not induce" the
    failure). Forces the durable-store failure via a monkeypatched
    `_get_store()`, then asserts the rendered error is the independently
    hardcoded literal Arabic SERVICE_UNAVAILABLE copy — proving the call
    site actually routes through `ui_text.localize_message()` rather than
    the raw English constant. A mutation bypassing `localize_message()` at
    either call site fails this test."""
    import web.app as web_app
    monkeypatch.setattr(web_app, "_get_store", lambda: _FailingStore())
    _set_lang(client, "ar")
    resp = client.post(route, data=data, follow_redirects=False)
    assert resp.status_code == 503
    body = resp.get_data(as_text=True)
    assert "هذه الخدمة غير متاحة مؤقتًا" in body
    assert "This service is temporarily unavailable" not in body


# ===== 3. Observation #3 — present-confirm first-person consent (LOAD-BEARING)
def test_red_broadened_present_confirm_ar_first_person_not_prompt_style(activate, client):
    """The Arabic present-confirm text for a recognized non-electronics
    domain (UI_B_START_024, consumed by both the error paragraph and
    `start_present_confirm_label`) must now be a first-person consent
    affirmation ("أؤكد أن...") — matching the register `UI_B_START_030`
    already correctly uses — rather than the old prompt/instruction wording
    ("يرجى تأكيد..."). Independent hardcoded-literal markers for both
    registers, not derived from `ui_text.UI_STRINGS`. Fails if UI_B_START_024
    is ever reverted to prompt/instruction style. Domain-neutral throughout —
    no domain name (Mechanical or otherwise) appears anywhere in the string,
    preserving the CF-2 Tier-1 boundary."""
    activate(ELEC, MECH)
    _set_lang(client, "ar")
    resp = _post(client, MECH_IDEA)
    body = resp.get_data(as_text=True)
    para = _error_paragraph(body)
    assert "أؤكد أن" in para
    assert "يرجى تأكيد" not in para
    assert "Mechanical" not in body
    assert "ميكانيكي" not in body


def test_green_ui_b_start_024_still_domain_neutral():
    """Structural guard: the corrected UI_B_START_024 content names no
    specific domain in either language — confirms the remediation did not
    drift into Tier-1 translation work."""
    entry = ui_text.UI_STRINGS["UI_B_START_024"]
    for lang, text in entry.items():
        assert "mechanical" not in text.lower()
        assert "electronic" not in text.lower()


def test_green_ui_b_start_023_and_030_unaffected():
    """UI_B_START_023 (electronics-only present-confirm, already accepted,
    production-reachable) and UI_B_START_030 (`start_confirm_label`, a
    DIFFERENT template variable) are explicitly out of scope for L10N-RH-01
    Observation #3 and must remain byte-unchanged by this remediation."""
    assert ui_text.UI_STRINGS["UI_B_START_023"]["ar"] == (
        "يبدو أن فكرتك تنتمي إلى مجال الإلكترونيات والكهرباء. "
        "يرجى تأكيد هذا المجال للبدء، أو تعديل الوصف.")
    assert ui_text.UI_STRINGS["UI_B_START_030"]["ar"] == (
        "أؤكد أن هذه الفكرة هي في الأساس فكرة ضمن المجال المدعوم.")
