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

from tests.csrf_client import csrf_client
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
    return csrf_client(app)


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
    assert domain_activation.activated_domains() == [ELEC, "mechanical"]


# ============================================================= catalogue honesty
def test_new_catalogue_keys_bilingual_and_registered():
    """Every new UI_STRINGS key added by this gate carries both languages, and
    every _MESSAGE_KEYS registration resolves to an existing catalogue key."""
    new_keys = [f"UI_B_START_0{n}" for n in range(10, 15)] + \
               [f"UI_B_START_0{n}" for n in range(20, 33)] + \
               ["UI_B_SC_007", "UI_B_SC_008"]
    for key in new_keys:
        entry = ui_text.UI_STRINGS[key]
        assert entry.get("en"), key
        assert entry.get("ar"), key
    for english, key in ui_text._MESSAGE_KEYS.items():
        assert key in ui_text.UI_STRINGS, key


# ===================================================== 1/5. static /start errors
# Mechanical Activation Execution Gate: real production activation now
# includes `mechanical`, which broadens `_unsupported_domain_message`'s
# composed copy. These byte-identity tests are reconstructed here via the
# file's own `activate` double (electronics-only) to keep proving the
# original electronics-only-scoped claim in isolation.
def test_green_en_unsupported_domain_byte_identical(client, activate):
    """English UI (default): electronics-only refusal stays byte-identical."""
    activate(ELEC)
    resp = _post(client, MECH_IDEA_STRONG, confirm=ELEC)
    body = resp.get_data(as_text=True)
    assert UNSUPPORTED_DOMAIN_MESSAGE in body


def test_green_ar_unsupported_domain_localized_no_english_leak(client, activate):
    """Arabic UI: same real refusal renders the Arabic catalogue string, and
    the raw English constant is NOT present anywhere in the response."""
    activate(ELEC)
    _set_lang(client, "ar")
    resp = _post(client, MECH_IDEA_STRONG, confirm=ELEC)
    body = resp.get_data(as_text=True)
    assert UNSUPPORTED_DOMAIN_MESSAGE not in body
    assert ui_text.UI_STRINGS["UI_B_START_010"]["ar"] in body


def test_green_en_confirmation_required_byte_identical(client, activate):
    # CONFIRMATION_REQUIRED_MESSAGE is the sole-activated-domain one-step
    # form's message — only reachable when exactly one domain is activated;
    # reconstructed here via the file's own `activate` double.
    activate(ELEC)
    resp = _post(client, ELEC_IDEA)
    body = resp.get_data(as_text=True)
    assert CONFIRMATION_REQUIRED_MESSAGE in body


def test_green_ar_confirmation_required_localized_no_english_leak(client, activate):
    activate(ELEC)
    _set_lang(client, "ar")
    resp = _post(client, ELEC_IDEA)
    body = resp.get_data(as_text=True)
    assert CONFIRMATION_REQUIRED_MESSAGE not in body
    assert ui_text.UI_STRINGS["UI_B_START_011"]["ar"] in body


def test_green_en_mechanism_guidance_byte_identical(client, activate):
    # A weak/ambiguous mechanical-conflict idea with NO lay-electrical
    # corroboration triggers the guidance branch (unchanged dispatch logic) —
    # only reachable when the sole activated domain is electronics
    # (`sole == "electronics_electrical"`); reconstructed here via the file's
    # own `activate` double.
    activate(ELEC)
    resp = _post(client, MECH_IDEA, confirm=ELEC)
    body = resp.get_data(as_text=True)
    assert MECHANISM_GUIDANCE_MESSAGE in body


def test_green_ar_mechanism_guidance_localized_no_english_leak(client, activate):
    activate(ELEC)
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
    """UXAR-01: the Arabic present-confirm PARAGRAPH is the explanatory prompt
    (UI_B_START_032) naming the canonical review path — no longer the
    UI_B_START_023 copy, which is preserved in the catalogue byte-for-byte but
    is not what this paragraph renders. Hard-coded expectation."""
    activate(ELEC, MECH)
    _set_lang(client, "ar")
    resp = _post(client, ELEC_IDEA)
    body = resp.get_data(as_text=True)
    assert _error_paragraph(body) == UXAR_AR_PROMPT_ELEC
    assert "Your idea appears to belong" not in body


def test_green_ar_present_confirm_broadened_domain_neutral(activate, client):
    """Present-confirm for a NON-electronics target. UXAR-01: the paragraph
    names the review path through the CANONICAL public label resolver
    (`web/domain_label.py`, the same Tier-1 label the rest of the product
    shows) — nothing is invented or hard-coded in the catalogue, whose
    templates stay domain-neutral. Hard-coded expectation."""
    activate(ELEC, MECH)
    _set_lang(client, "ar")
    resp = _post(client, MECH_IDEA)
    body = resp.get_data(as_text=True)
    assert _error_paragraph(body) == UXAR_AR_PROMPT_MECH
    assert "Your idea appears to belong" not in body


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
    assert domain_activation.activated_domains() == [ELEC, "mechanical"]


def test_green_guard_ilt002_review_type_label_unchanged(client):
    """D-CF6CF2-ILT002-01 untouched: the ILT-002 session presentation is not
    part of this facet's change surface — a smoke re-check only."""
    from web import domain_label
    label = domain_label.public_domain_label(ELEC)
    assert label == {"en": "Electronics-informed review",
                      "ar": "مراجعة مستنيرة بمجال الإلكترونيات"}


# =========================================================================
# UXAR-01 — Arabic /start present-confirm: explanatory PROMPT vs first-person
# CONSENT are two UI roles and must never consume one catalogue entry.
#
# Every expectation below is HARD-CODED (never derived from `ui_text.UI_STRINGS`)
# so a catalogue mutation cannot silently satisfy its own test. Elements are
# extracted individually: the `<p class="error">` paragraph and the `<label>`
# that owns `input[name="domain_confirm"]`. Whole-page substring checks are
# avoided because other page copy shares phrases such as "يرجى تأكيد".
# =========================================================================
UXAR_LABEL_ELEC = "مراجعة مستنيرة بمجال الإلكترونيات"
UXAR_LABEL_MECH = "مراجعة مستنيرة بمجال الميكانيكا"
UXAR_AR_PROMPT_ELEC = ("المسار المحدد لمراجعة فكرتك هو «مراجعة مستنيرة بمجال الإلكترونيات». "
                       "يرجى تأكيد هذا المسار للبدء، أو تعديل وصفك.")
UXAR_AR_PROMPT_MECH = ("المسار المحدد لمراجعة فكرتك هو «مراجعة مستنيرة بمجال الميكانيكا». "
                       "يرجى تأكيد هذا المسار للبدء، أو تعديل وصفك.")
UXAR_AR_CONSENT_ELEC = "أؤكد أنني أرغب في متابعة فكرتي عبر «مراجعة مستنيرة بمجال الإلكترونيات»."
UXAR_AR_CONSENT_MECH = "أؤكد أنني أرغب في متابعة فكرتي عبر «مراجعة مستنيرة بمجال الميكانيكا»."
UXAR_EN_PROMPT = ("Your idea appears to belong to the {label} domain. "
                  "Please confirm this domain to start, or revise your description.")
UXAR_EN_CONSENT = "I confirm that my idea belongs to the {label} domain."
UXAR_EN_LABEL = {ELEC: "Electronics Electrical", MECH: "Mechanical"}

_CONFIRM_LABEL_RE = re.compile(
    r'<label[^>]*>\s*<input type="checkbox" name="domain_confirm" value="([^"]+)" required>'
    r'\s*(.*?)\s*</label>', re.S)
_CARRIED_CHOICE_RE = re.compile(r'<input type="hidden" name="domain_choice" value="([^"]+)">')


def _confirm_checkbox(body):
    """(domain value, label text) of the ONE consent checkbox, or (None, None)."""
    m = _CONFIRM_LABEL_RE.search(body)
    return (m.group(1), " ".join(m.group(2).split())) if m else (None, None)


def _carried_choice(body):
    m = _CARRIED_CHOICE_RE.search(body)
    return m.group(1) if m else None


def _present_confirm(client, origin, domain):
    """Reach the present-confirm response for one matrix cell on the REAL
    activation state (both domains are activated in production). D1: the
    classifier selects `domain`; D2: the classifier returns NONE and the user
    explicitly chooses `domain`. No confirmation is sent, so no admission."""
    idea = {ELEC: ELEC_IDEA, MECH: MECH_IDEA}[domain]
    if origin == "D1":
        return _post(client, idea)
    return _post(client, NONE_IDEA, choice=domain)


_MATRIX = [("D1", ELEC), ("D1", MECH), ("D2", ELEC), ("D2", MECH)]
_AR_EXPECTED = {
    ELEC: (UXAR_AR_PROMPT_ELEC, UXAR_AR_CONSENT_ELEC, UXAR_LABEL_ELEC),
    MECH: (UXAR_AR_PROMPT_MECH, UXAR_AR_CONSENT_MECH, UXAR_LABEL_MECH),
}


def test_uxar01_catalogue_032_exists_and_024_english_pinned():
    """UI_B_START_032 exists with both languages and is NOT a `_MESSAGE_KEYS`
    member (it is consumed directly through `ui_text.text()`); the English
    UI_B_START_024 value is byte-identical to its pre-UXAR-01 text."""
    entry = ui_text.UI_STRINGS["UI_B_START_032"]
    assert entry.get("en") and entry.get("ar")
    assert "UI_B_START_032" not in ui_text._MESSAGE_KEYS.values()
    assert ui_text.UI_STRINGS["UI_B_START_024"]["en"] == (
        "I confirm that this idea belongs to the domain that was recognized for it.")


@pytest.mark.parametrize("origin,domain", _MATRIX)
def test_uxar01_ar_prompt_and_consent_are_split_roles(client, origin, domain):
    prompt, consent, label = _AR_EXPECTED[domain]
    _set_lang(client, "ar")
    resp = _present_confirm(client, origin, domain)
    assert resp.status_code == 200
    body = resp.get_data(as_text=True)
    para = _error_paragraph(body)
    value, checkbox = _confirm_checkbox(body)
    assert value == domain
    assert para is not None and checkbox is not None
    assert para != checkbox                                   # two roles, two texts
    assert para == prompt                                     # exact UI_B_START_032
    assert checkbox == consent                                # exact UI_B_START_024
    assert label in para and label in checkbox                # canonical review path
    assert "يرجى تأكيد" in para and "أؤكد" not in para        # request register
    assert "أؤكد" in checkbox and "يرجى تأكيد" not in checkbox  # consent register
    for element in (para, checkbox):
        assert "المقترح" not in element                       # no "suggested"
        assert "تم التعرف عليه" not in element                # no recognition claim
        assert "المجال الذي" not in element                   # no unnamed generic consent
    if origin == "D2":
        assert _carried_choice(body) == domain               # hidden carry preserved
    else:
        assert _carried_choice(body) is None


@pytest.mark.parametrize("origin,domain", _MATRIX)
def test_uxar01_en_paragraph_and_checkbox_bytes_unchanged(client, origin, domain):
    """English runtime output is byte-compatible: the split is Arabic-only."""
    _set_lang(client, "en")
    resp = _present_confirm(client, origin, domain)
    body = resp.get_data(as_text=True)
    value, checkbox = _confirm_checkbox(body)
    assert value == domain
    assert _error_paragraph(body) == UXAR_EN_PROMPT.format(label=UXAR_EN_LABEL[domain])
    assert checkbox == UXAR_EN_CONSENT.format(label=UXAR_EN_LABEL[domain])
    if origin == "D2":
        assert _carried_choice(body) == domain


@pytest.mark.parametrize("origin,domain", _MATRIX)
def test_uxar01_no_session_or_project_before_matching_confirmation(client, origin, domain):
    import web.app as webapp
    store = webapp._get_store()
    projects_before = set(store.project_ids())
    sessions_before = set(SESSION_STORE)
    _set_lang(client, "ar")
    resp = _present_confirm(client, origin, domain)
    assert resp.status_code == 200                            # stays on the form
    assert 'name="domain_confirm"' in resp.get_data(as_text=True)
    assert set(SESSION_STORE) == sessions_before
    assert set(store.project_ids()) == projects_before


@pytest.mark.parametrize("origin,domain", _MATRIX)
def test_uxar01_missing_forged_or_mismatched_confirmation_never_admits(client, origin, domain):
    import web.app as webapp
    store = webapp._get_store()
    projects_before = set(store.project_ids())
    sessions_before = set(SESSION_STORE)
    other = MECH if domain == ELEC else ELEC
    idea = {ELEC: ELEC_IDEA, MECH: MECH_IDEA}[domain]
    _set_lang(client, "ar")
    attempts = (
        _post(client, idea if origin == "D1" else NONE_IDEA, confirm=other,
              choice=(domain if origin == "D2" else None)),      # mismatched
        _post(client, idea if origin == "D1" else NONE_IDEA, confirm="forged-domain",
              choice=(domain if origin == "D2" else None)),      # forged
    )
    for resp in attempts:
        assert resp.status_code == 200
        assert "/session/" not in resp.headers.get("Location", "")
    assert set(SESSION_STORE) == sessions_before
    assert set(store.project_ids()) == projects_before


@pytest.mark.parametrize("origin,domain", _MATRIX)
def test_uxar01_matching_confirmation_admits_exact_domain(client, origin, domain):
    idea = {ELEC: ELEC_IDEA, MECH: MECH_IDEA}[domain]
    _set_lang(client, "ar")
    _present_confirm(client, origin, domain)                  # the AR confirm page
    resp = _post(client, idea if origin == "D1" else NONE_IDEA, confirm=domain,
                 choice=(domain if origin == "D2" else None))
    assert resp.status_code == 302
    sid = resp.headers["Location"].rsplit("/", 1)[-1]
    entry = SESSION_STORE.pop(sid)
    assert entry["state"].domain == domain
