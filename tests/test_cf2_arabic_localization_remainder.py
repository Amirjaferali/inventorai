"""CF-2 — Arabic Localization Remainder (Fast Track).

Authoritative contract: the CF-2 Arabic Localization Remainder Fast Track gate
(base `cccbf30cf6a851b0c7291c95c159f74520105d99`, PR #493). Fixes the fresh-sweep-
confirmed unlocalized public-copy surfaces on the `/start` admission flow and the
`/session/<sid>/success-criteria` reject path:

  * five raw `/start`-flow error-path constants (`UNSUPPORTED_DOMAIN_MESSAGE`,
    `CONFIRMATION_REQUIRED_MESSAGE`, `MECHANISM_GUIDANCE_MESSAGE`,
    `DOMAIN_CHOICE_MESSAGE`, `SERVICE_UNAVAILABLE_MESSAGE`) — now routed through
    `ui_text.localize_message()`, the SAME mechanism already used for
    `ANSWER_REQUIRED_MESSAGE`/`ANSWER_NOT_SAVED_MESSAGE`/`KEEP_SNAPSHOT_ACK`;
  * `_unsupported_domain_message`, `_confirmation_required_message`,
    `_present_confirm_message` — now `lang`-aware (default `"en"` preserves
    EXACT prior behavior byte-for-byte; Arabic uses new fixed catalogue copy);
  * the six `_render_start_page` generalized-context strings
    (`start_scope_sentence`, `start_placeholder`, `start_supported_note`,
    `start_confirm_label`, `start_present_confirm_label`, `start_choice_prompt`)
    — previously ALWAYS raw English regardless of `ui_lang`, now lang-aware;
  * the two raw `_reject()` messages in `save_success_criteria`.

Per the Fast Track boundary, broadened-activation (2+ domains) Arabic copy is
deliberately DOMAIN-NEUTRAL (never names a specific non-electronics domain in
Arabic — that would be new Tier-1 label translation work, out of scope and
forbidden by the governing contract) while remaining truthful about the real
state. Multi-/zero-activation states are exercised ONLY via the bounded,
self-restoring `engine.domain_activation._ACTIVATED_DOMAINS` test double — the
real runtime state remains `activated_domains() == ['electronics_electrical']`
(asserted below). Classifier, activation, persistence, routing/admission, and
D-CF6CF2-ILT002-01 are all UNCHANGED — presentation only.
"""

import os
import re
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from engine import domain_activation
from engine.idea_state import IdeaState
from web import ui_text
from web.app import (
    app, SESSION_STORE, UNSUPPORTED_DOMAIN_MESSAGE, CONFIRMATION_REQUIRED_MESSAGE,
    MECHANISM_GUIDANCE_MESSAGE, DOMAIN_CHOICE_MESSAGE, SERVICE_UNAVAILABLE_MESSAGE,
)

ELEC = "electronics_electrical"
MECH = "mechanical"

ELEC_IDEA = "ESP32 microcontroller circuit with a voltage sensor"
MECH_IDEA = "A hinge mounted bracket with a lever and a spring latch"
MECH_IDEA_STRONG = "A gear and pulley hoist with a crankshaft drive"
NONE_IDEA = "something with no recognizable signals at all"


@pytest.fixture
def activate(monkeypatch):
    """Self-restoring activation double (no real activation)."""
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
    """The `<p class="error">...</p>` content only — distinct from the
    checkbox `start_present_confirm_label`, which is computed and rendered
    separately and must not mask a defect in the `error=` message itself."""
    m = re.search(r'<p class="error">(.*?)</p>', body, re.S)
    return m.group(1) if m else None


# --------------------------------------------------------- fixture honesty -------
def test_baseline_real_activation_unchanged():
    assert domain_activation.activated_domains() == [ELEC]


# ============================================================= catalogue honesty
def test_new_catalogue_keys_bilingual_and_registered():
    """Every new UI_STRINGS key added by this gate carries both languages, and
    every _MESSAGE_KEYS registration resolves to an existing catalogue key."""
    new_keys = [f"UI_B_START_0{n}" for n in range(10, 15)] + \
               [f"UI_B_START_0{n}" for n in range(20, 32)] + \
               ["UI_B_SC_007", "UI_B_SC_008"]
    for key in new_keys:
        entry = ui_text.UI_STRINGS[key]
        assert entry.get("en"), key
        assert entry.get("ar"), key
    for english, key in ui_text._MESSAGE_KEYS.items():
        assert key in ui_text.UI_STRINGS, key


# ===================================================== 1/5. static /start errors
def test_green_en_unsupported_domain_byte_identical(client):
    """English UI (default): electronics-only refusal stays byte-identical."""
    resp = _post(client, MECH_IDEA_STRONG, confirm=ELEC)
    body = resp.get_data(as_text=True)
    assert UNSUPPORTED_DOMAIN_MESSAGE in body


def test_green_ar_unsupported_domain_localized_no_english_leak(client):
    """Arabic UI: same real refusal renders the Arabic catalogue string, and
    the raw English constant is NOT present anywhere in the response."""
    _set_lang(client, "ar")
    resp = _post(client, MECH_IDEA_STRONG, confirm=ELEC)
    body = resp.get_data(as_text=True)
    assert UNSUPPORTED_DOMAIN_MESSAGE not in body
    assert ui_text.UI_STRINGS["UI_B_START_010"]["ar"] in body


def test_green_en_confirmation_required_byte_identical(client):
    resp = _post(client, ELEC_IDEA)
    body = resp.get_data(as_text=True)
    assert CONFIRMATION_REQUIRED_MESSAGE in body


def test_green_ar_confirmation_required_localized_no_english_leak(client):
    _set_lang(client, "ar")
    resp = _post(client, ELEC_IDEA)
    body = resp.get_data(as_text=True)
    assert CONFIRMATION_REQUIRED_MESSAGE not in body
    assert ui_text.UI_STRINGS["UI_B_START_011"]["ar"] in body


def test_green_en_mechanism_guidance_byte_identical(client):
    # A weak/ambiguous mechanical-conflict idea with NO lay-electrical
    # corroboration triggers the guidance branch (unchanged dispatch logic).
    resp = _post(client, MECH_IDEA, confirm=ELEC)
    body = resp.get_data(as_text=True)
    assert MECHANISM_GUIDANCE_MESSAGE in body


def test_green_ar_mechanism_guidance_localized_no_english_leak(client):
    _set_lang(client, "ar")
    resp = _post(client, MECH_IDEA, confirm=ELEC)
    body = resp.get_data(as_text=True)
    assert MECHANISM_GUIDANCE_MESSAGE not in body
    assert ui_text.UI_STRINGS["UI_B_START_012"]["ar"] in body


def test_green_en_domain_choice_byte_identical(activate, client):
    activate(ELEC, MECH)
    resp = _post(client, NONE_IDEA)
    body = resp.get_data(as_text=True)
    assert DOMAIN_CHOICE_MESSAGE in body


def test_green_ar_domain_choice_localized_no_english_leak(activate, client):
    activate(ELEC, MECH)
    _set_lang(client, "ar")
    resp = _post(client, NONE_IDEA)
    body = resp.get_data(as_text=True)
    assert DOMAIN_CHOICE_MESSAGE not in body
    assert ui_text.UI_STRINGS["UI_B_START_013"]["ar"] in body


def test_green_ar_service_unavailable_localize_message_wired(client):
    """SERVICE_UNAVAILABLE_MESSAGE fires only on a durable-store failure, which
    this suite does not induce; instead prove localize_message() itself maps
    the real constant correctly (the wiring at both call sites is identical:
    `ui_text.localize_message(SERVICE_UNAVAILABLE_MESSAGE, lang)`)."""
    assert ui_text.localize_message(SERVICE_UNAVAILABLE_MESSAGE, "ar") == \
        ui_text.UI_STRINGS["UI_B_START_014"]["ar"]
    assert ui_text.localize_message(SERVICE_UNAVAILABLE_MESSAGE, "en") == \
        SERVICE_UNAVAILABLE_MESSAGE


# ============================================== 2/9. present-confirm (D1/U1) ----
def test_green_en_present_confirm_electronics_byte_content_unchanged(activate, client):
    """Reachable only with 2+ activated domains and no domain_confirm on the
    first POST (target resolves to electronics_electrical here). Checks the
    `<p class="error">` paragraph specifically — NOT just "anywhere in body"
    — since the checkbox `start_present_confirm_label` renders separately and
    would otherwise mask a defect in the `error=` message alone."""
    activate(ELEC, MECH)
    resp = _post(client, ELEC_IDEA)
    body = resp.get_data(as_text=True)
    assert _error_paragraph(body) == (
        "Your idea appears to belong to the Electronics Electrical domain. "
        "Please confirm this domain to start, or revise your description.")


def test_green_ar_present_confirm_electronics_localized_no_english_leak(activate, client):
    activate(ELEC, MECH)
    _set_lang(client, "ar")
    resp = _post(client, ELEC_IDEA)
    body = resp.get_data(as_text=True)
    assert _error_paragraph(body) == ui_text.UI_STRINGS["UI_B_START_023"]["ar"]


def test_green_ar_present_confirm_broadened_domain_neutral(activate, client):
    """Present-confirm for a NON-electronics target: Arabic stays
    domain-neutral (no invented Tier-1 translation of "Mechanical")."""
    activate(ELEC, MECH)
    _set_lang(client, "ar")
    resp = _post(client, MECH_IDEA)
    body = resp.get_data(as_text=True)
    assert _error_paragraph(body) == ui_text.UI_STRINGS["UI_B_START_024"]["ar"]


# ==================================================== 3/6. no-activation state --
def test_green_en_empty_activation_unsupported_byte_identical(activate, client):
    activate()
    resp = _post(client, "anything", confirm=ELEC)
    body = resp.get_data(as_text=True)
    assert ("InventorAI has no specialist domain available right now. "
            "Please try again later.") in body


def test_green_ar_empty_activation_unsupported_localized(activate, client):
    activate()
    _set_lang(client, "ar")
    resp = _post(client, "anything", confirm=ELEC)
    body = resp.get_data(as_text=True)
    assert "no specialist domain available right now" not in body
    assert ui_text.UI_STRINGS["UI_B_START_020"]["ar"] in body


def test_green_ar_empty_activation_confirmation_required_domain_neutral(activate, client):
    """`_confirmation_required_message` is called with `sole=None` guard: with
    zero activated domains `sole is None`, so this path is the unsupported-
    domain branch, not confirmation-required — asserted here as a GREEN GUARD
    (confirms no crash / no stray English on the empty-activation POST)."""
    activate()
    _set_lang(client, "ar")
    resp = _post(client, "anything")
    assert resp.status_code == 200
    body = resp.get_data(as_text=True)
    assert "Please confirm that your idea is" not in body


# ============================================ 4. generalized context strings ----
def test_green_ar_broadened_generalized_context_no_english_leak(activate, client):
    activate(ELEC, MECH)
    _set_lang(client, "ar")
    resp = client.get("/")
    body = resp.get_data(as_text=True)
    assert ui_text.UI_STRINGS["UI_B_START_026"]["ar"] in body   # scope sentence
    assert ui_text.UI_STRINGS["UI_B_START_027"]["ar"] in body   # placeholder
    assert ui_text.UI_STRINGS["UI_B_START_029"]["ar"] in body   # supported note
    assert "ideas are currently supported" not in body
    assert "Currently supported:" not in body
    assert "Describe your invention..." not in body


def test_green_en_broadened_generalized_context_byte_identical(activate, client):
    activate(ELEC, MECH)
    resp = client.get("/")
    body = resp.get_data(as_text=True)
    assert "ideas are currently supported" in body
    assert "Describe your invention..." in body


def test_green_ar_empty_activation_generalized_context(activate, client):
    activate()
    _set_lang(client, "ar")
    resp = client.get("/")
    body = resp.get_data(as_text=True)
    assert ui_text.UI_STRINGS["UI_B_START_025"]["ar"] in body
    assert ui_text.UI_STRINGS["UI_B_START_028"]["ar"] in body
    assert "No specialist domain is currently available." not in body


def test_green_ar_sole_non_electronics_confirm_label_domain_neutral(activate, client):
    activate(MECH)
    _set_lang(client, "ar")
    resp = client.get("/")
    body = resp.get_data(as_text=True)
    assert ui_text.UI_STRINGS["UI_B_START_030"]["ar"] in body
    assert "I confirm that this idea is primarily a" not in body


def test_green_ar_choice_prompt_localized_no_english_leak(activate, client):
    activate(ELEC, MECH)
    _set_lang(client, "ar")
    resp = _post(client, NONE_IDEA)
    body = resp.get_data(as_text=True)
    assert ui_text.UI_STRINGS["UI_B_START_031"]["ar"] in body
    # Jinja HTML-autoescapes the English apostrophe as `&#39;`.
    assert "Choose your idea&#39;s domain:" not in body


def test_green_en_choice_prompt_byte_identical(activate, client):
    activate(ELEC, MECH)
    resp = _post(client, NONE_IDEA)
    body = resp.get_data(as_text=True)
    # Jinja HTML-autoescapes the English apostrophe as `&#39;`.
    assert "Choose your idea&#39;s domain:" in body


# =========================================================== 5. RTL / template --
def test_green_ar_index_page_rtl_direction(client):
    _set_lang(client, "ar")
    resp = client.get("/")
    body = resp.get_data(as_text=True)
    assert 'lang="ar"' in body
    assert 'dir="rtl"' in body


def test_green_en_index_page_ltr_direction(client):
    resp = client.get("/")
    body = resp.get_data(as_text=True)
    assert 'lang="en"' in body
    assert 'dir="rtl"' not in body


# ============================================================ 6. present-confirm+
# admission unaffected: language selection never changes WHICH domain is
# admitted (mirrors test_g_u5_ui_language_does_not_alter_admission_or_domains
# in the CF5-F002/CF-6 suite; re-pinned here for this facet's own changes).
def test_green_ar_admission_outcome_unchanged_by_language(activate, client):
    activate(ELEC, MECH)
    _set_lang(client, "ar")
    _post(client, MECH_IDEA)                       # present-confirm, AR copy
    resp = _post(client, MECH_IDEA, confirm=MECH)
    assert resp.status_code == 302
    sid = resp.headers["Location"].rsplit("/", 1)[-1]
    entry = SESSION_STORE.pop(sid)
    assert entry["state"].domain == MECH


# ===================================================== 7/8. success-criteria ----
def _make_session():
    sid = "cf2-ar-sc-smoke"
    state = IdeaState(idea_id="cf2-ar-sc-smoke-idea")
    state.domain = ELEC
    SESSION_STORE[sid] = {"state": state, "last_result": None, "transcript": []}
    return sid


def test_green_en_success_criteria_unknown_experiment_byte_identical(client):
    sid = _make_session()
    try:
        resp = client.post(f"/session/{sid}/success-criteria",
                            data={"criterion__does-not-exist": "x"})
        assert resp.status_code == 400
        body = resp.get_data(as_text=True)
        assert ("A submitted experiment is not part of the current plan. "
                "No changes were saved.") in body
    finally:
        SESSION_STORE.pop(sid, None)


def test_green_ar_success_criteria_unknown_experiment_localized(client):
    sid = _make_session()
    try:
        _set_lang(client, "ar")
        resp = client.post(f"/session/{sid}/success-criteria",
                            data={"criterion__does-not-exist": "x"})
        assert resp.status_code == 400
        body = resp.get_data(as_text=True)
        assert "not part of the current plan" not in body
        assert ui_text.UI_STRINGS["UI_B_SC_007"]["ar"] in body
    finally:
        SESSION_STORE.pop(sid, None)


# ====================================================== 9. dispatch invariance =
def test_green_guard_lang_default_preserves_signature_compatible_call(client):
    """Every producer function's `lang` parameter defaults to `"en"`, so any
    existing caller that omits it is behaviourally unaffected (checked
    directly, independent of the request/route layer)."""
    from web.app import (
        _unsupported_domain_message, _confirmation_required_message,
        _present_confirm_message,
    )
    assert _unsupported_domain_message([ELEC]) == UNSUPPORTED_DOMAIN_MESSAGE
    assert _confirmation_required_message(ELEC) == CONFIRMATION_REQUIRED_MESSAGE
    assert (_present_confirm_message(ELEC)
            == "Your idea appears to belong to the Electronics Electrical domain. "
               "Please confirm this domain to start, or revise your description.")


# ============================================ 10. classifier/activation/D-CF6CF2 =
def test_green_guard_real_activation_state_unchanged():
    assert domain_activation.activated_domains() == [ELEC]


def test_green_guard_ilt002_review_type_label_unchanged(client):
    """D-CF6CF2-ILT002-01 untouched: the ILT-002 session presentation is not
    part of this facet's change surface — a smoke re-check only."""
    from web import domain_label
    label = domain_label.public_domain_label(ELEC)
    assert label == {"en": "Electronics-informed review",
                      "ar": "مراجعة مستنيرة بمجال الإلكترونيات"}
