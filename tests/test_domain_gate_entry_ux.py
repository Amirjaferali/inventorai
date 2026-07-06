"""Domain Gate / Entry UX Increment — targeted tests.

Governed by the merged Increment Contract
`docs/governance/DOMAIN_GATE_ENTRY_UX_INCREMENT_CONTRACT_POST_PR99.md` (PR #100).

Goal under test: valid electronics/electrical ideas written in lay wording must
not be hard-rejected solely for lacking technical component keywords, while
unsupported-domain rejection and the electronics/electrical-only MVP boundary
are preserved. The deterministic classifier, registry, and domain packs are
unchanged; this exercises only the bounded /start domain-gate ambiguity
resolution added in `web/app.py`.

Coverage maps to Contract §8 (accept), §9 (reject), §10 (conflicts), and the
§12 required-test categories.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from web.app import (  # noqa: E402
    app,
    SESSION_STORE,
    UNSUPPORTED_DOMAIN_MESSAGE,
    MECHANISM_GUIDANCE_MESSAGE,
    DOMAIN_CONFIRM_VALUE,
)

_ERROR_HTML = '<p class="error">' + UNSUPPORTED_DOMAIN_MESSAGE + '</p>'
_GUIDANCE_HTML = '<p class="error">' + MECHANISM_GUIDANCE_MESSAGE + '</p>'


def _post(idea, confirm=True):
    """POST an idea to /start with (by default) explicit electronics confirmation."""
    data = {"idea": idea}
    if confirm:
        data["domain_confirm"] = DOMAIN_CONFIRM_VALUE
    return app.test_client().post("/start", data=data, follow_redirects=False)


def _assert_admitted(resp):
    """A 302 redirect into a freshly created electronics session."""
    assert resp.status_code == 302
    assert "/session/" in resp.headers["Location"]
    sid = resp.headers["Location"].rsplit("/", 1)[-1]
    entry = SESSION_STORE.get(sid)
    assert entry is not None, "admitted idea created no session"
    assert entry["state"].domain == "electronics_electrical"
    return sid


def _assert_not_admitted(resp, expected_html):
    """A 200 render with the expected message and no new/relabeled session."""
    assert resp.status_code == 200
    body = resp.get_data(as_text=True)
    assert expected_html in body
    assert "Location" not in resp.headers
    return body


# ---------------------------------------------------------------------------
# §8 / §12 — lay electronics accepted (not hard-rejected for lacking terms)
# ---------------------------------------------------------------------------

def test_lay_appliance_power_alert_is_admitted():
    # Contract §8.B — classifies as `software` today (substring "app" in
    # "appliance"); the lay word "power" is the electrical mechanism evidence.
    before = set(SESSION_STORE)
    resp = _post("A home appliance alert that detects if power stays on "
                 "unusually long and sends a phone alert.")
    sid = _assert_admitted(resp)
    assert set(SESSION_STORE) == before | {sid}


def test_plug_current_wifi_alert_is_admitted():
    # Contract §8.C.
    _assert_admitted(_post(
        "A plug-in device that senses current from an appliance and sends a "
        "Wi-Fi alert."))


def test_socket_powered_appliance_is_admitted():
    # Contract §8.D — classifies as `software` today; "socket"/"powered" admit it.
    _assert_admitted(_post(
        "A socket device that warns when an appliance remains powered for more "
        "than a set time."))


def test_sensor_electrical_current_is_admitted():
    # Contract §8.E.
    _assert_admitted(_post(
        "A sensor device that detects appliance electrical current and alerts "
        "the user."))


def test_lay_electrical_without_classifier_signal_is_admitted():
    # §7.B / §12 lay-accepted: pure lay electrical wording the substring
    # classifier does not map to electronics_electrical is still admitted.
    _assert_admitted(_post(
        "A wall plug that switches off the power to an outlet after a while."))


# ---------------------------------------------------------------------------
# §12 — mechanism-explicit electronics admission (regression of existing path)
# ---------------------------------------------------------------------------

def test_mechanism_explicit_electronics_is_admitted():
    # Contract §8/§13 Demo B — classic electronics wording must still admit.
    _assert_admitted(_post(
        "An ESP32 microcontroller with a current sensor and a Wi-Fi alert."))


# ---------------------------------------------------------------------------
# §9 — unsupported domains must still be rejected
# ---------------------------------------------------------------------------

def test_medical_heart_monitor_is_rejected_unsupported():
    # Contract §9.A — strong medical evidence ("medical"/"heart").
    before = set(SESSION_STORE)
    resp = _post("A medical monitor that tracks heart rhythm and alerts doctors.")
    body = _assert_not_admitted(resp, _ERROR_HTML)
    assert "medical_device" not in body  # internal pack id must not leak
    assert set(SESSION_STORE) == before


def test_software_only_assistant_is_rejected():
    # Contract §9.F — strong software evidence ("software").
    _assert_not_admitted(
        _post("A software-only AI assistant that predicts appliance use."),
        _ERROR_HTML)


def test_mechanical_gas_valve_is_rejected():
    # Contract §9.C — strong mechanical evidence ("mechanical").
    _assert_not_admitted(
        _post("A purely mechanical timer that shuts off a gas valve."),
        _ERROR_HTML)


def test_drone_farm_is_rejected_non_activation():
    # Contract §9.D / §6 — drone & agriculture families are not activated.
    _assert_not_admitted(
        _post("A drone that checks farms and sprays crops."),
        _ERROR_HTML)


def test_solar_panel_validator_is_rejected_non_activation():
    # Contract §9.E / §6 — solar family is not activated.
    _assert_not_admitted(
        _post("A solar farm optimizer that validates panel wiring safety."),
        _ERROR_HTML)


def test_dementia_diagnosis_is_rejected_unsupported():
    # Contract §9.G — medical/sensitive; caught by "diagnos"/"dementia".
    _assert_not_admitted(
        _post("A device that diagnoses dementia by monitoring elderly behavior."),
        _ERROR_HTML)


# ---------------------------------------------------------------------------
# §10 / §12 — conflict cases & owner confirmation is not an unconditional bypass
# ---------------------------------------------------------------------------

def test_checkbox_does_not_bypass_strong_medical_evidence():
    # §10 / §12 — explicit confirmation must NOT admit a genuinely medical idea.
    before = set(SESSION_STORE)
    resp = _post("A cardiac implant that senses blood pressure with a circuit.",
                 confirm=True)
    _assert_not_admitted(resp, _ERROR_HTML)
    assert set(SESSION_STORE) == before


def test_monitoring_with_electrical_context_is_admitted_not_medical():
    # §10 — "monitoring" alone must NOT force medical_device when the wording and
    # confirmation indicate a household electrical appliance alert.
    _assert_admitted(_post(
        "A plug-in appliance power monitoring alert with a current sensor."))


def test_heart_monitoring_still_rejected():
    # §10 — "heart monitoring" must STILL reject even with electrical-sounding words.
    _assert_not_admitted(
        _post("A wearable heart monitoring band with a sensor circuit."),
        _ERROR_HTML)


# ---------------------------------------------------------------------------
# §7.E / §9.B / §12 — actionable guidance instead of a bare hard rejection
# ---------------------------------------------------------------------------

def test_no_mechanism_idea_is_guided_not_admitted_and_guidance_is_actionable():
    # §9.B — "app ... appliances ... manual checklists": weak conflicting
    # classification, no electrical mechanism -> guided (not admitted).
    before = set(SESSION_STORE)
    resp = _post("An app that reminds elderly people to turn off appliances "
                 "based only on manual checklists.")
    body = _assert_not_admitted(resp, _GUIDANCE_HTML)
    assert set(SESSION_STORE) == before
    # Guidance is distinct from the bare unsupported refusal ...
    assert _ERROR_HTML not in body
    # ... carries actionable, non-technical mechanism hints ...
    for hint in ("sensor", "switch", "power", "plug"):
        assert hint in MECHANISM_GUIDANCE_MESSAGE
    # ... and makes no validation / safety / feasibility / compliance claim.
    lowered = MECHANISM_GUIDANCE_MESSAGE.lower()
    for forbidden in ("valid", "safe", "feasib", "compliance", "certif",
                      "build-ready", "buildable", "patent"):
        assert forbidden not in lowered
