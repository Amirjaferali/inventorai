import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from web.app import app, SESSION_STORE
from engine.domain_rules import infer_domain


def test_start_ilt002_water_leak_forces_electronics_domain():
    client = app.test_client()
    response = client.post(
        "/start_ilt002_water_leak",
        data={"idea": "A water leak detection system using moisture sensors and alarm notification."},
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert "/session/" in response.headers["Location"]

    sid = response.headers["Location"].rsplit("/", 1)[-1]
    entry = SESSION_STORE.get(sid)
    assert entry is not None, "ILT-002 session state not stored"

    state = entry["state"]
    assert state.domain == "electronics_electrical"
    assert state.domain_signal == "electronics_electrical"
    assert entry["last_result"]["question"] == (
        "Describe how your electronic circuit achieves its intended function — what happens electrically from input to output?"
    )


def test_start_uses_infer_domain_for_normal_flow():
    client = app.test_client()
    idea_text = "ESP32 moisture sensor circuit with WiFi reporting"
    response = client.post(
        "/start",
        data={"idea": idea_text},
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert "/session/" in response.headers["Location"]

    sid = response.headers["Location"].rsplit("/", 1)[-1]
    entry = SESSION_STORE.get(sid)
    assert entry is not None, "Normal session state not stored"

    state = entry["state"]
    assert state.domain == infer_domain(idea_text)
    assert state.domain_signal == infer_domain(idea_text)
