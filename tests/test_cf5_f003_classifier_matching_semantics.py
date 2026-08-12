"""CF5-F003 — Classifier matching semantics: whole-token + bounded (+s/+es) plural,
contiguous multi-word, and same-domain registered containment preservation
(at-most-once / set-membership, plural-container aware).

Authoritative:
  docs/governance/CF5_F003_CLASSIFIER_MATCHING_SEMANTICS_CORRECTIVE_CONTRACT.md (v2)
  docs/governance/CF5_F003_CLASSIFIER_MATCHING_SEMANTICS_CORRECTIVE_CONTRACT_AMENDMENT_01.md

The classifier scored signals with raw substring semantics (`signal in text`), so
short signals matched inside unrelated words (led in "controlled"/"compiled"/
"knowledge", iot in "patriotic", current in "concurrent", heart in "hearth"). The
fix replaces substring matching in `engine/domain_rules.py::classify_domain` with
deterministic whole-token matching over `[a-z0-9]+` tokens (exact / bounded `+s` /
`+es`), contiguous multi-word phrase matching (bounded plural on the final token
only), and — per Amendment 01 §A3 — same-domain registered-signal containment
preservation credited AT MOST ONCE (set membership), fired whenever the registered
container is present via any authorized base form (incl. its bounded plural), never
cross-domain and never inside a non-registered word.

RED (false positives + real Web/CLI consequence) fail on the pre-fix parent and pass
after the fix. GREEN preservation (singular + plural, multi-word, containment
singular + plural-container, cross-domain non-leakage, at-most-once parity, genuine
0/1/2/3+ activation, Web/CLI parity) passes after the fix.
"""

import builtins
import importlib.util
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from engine import domain_activation
from engine.domain_rules import classify_domain, DomainResultKind


@pytest.fixture
def activate(monkeypatch):
    """Self-restoring `_ACTIVATED_DOMAINS` double (monkeypatch reverts after test)."""
    def _activate(*domains):
        monkeypatch.setattr(domain_activation, "_ACTIVATED_DOMAINS", frozenset(domains))
    return _activate


def _dom(idea):
    r = classify_domain(idea)
    return r.selected_domain if r.kind is DomainResultKind.SINGLE else None


def _score(idea, pack_id):
    """White-box per-domain score via the canonical classifier's own matcher."""
    from engine.domain_rules import _TOKEN_RE, _present_signal_count, _REGISTRY
    tokens = _TOKEN_RE.findall(idea.lower())
    return _present_signal_count(_REGISTRY[pack_id], tokens, set(tokens))


# ======================================================= RED: false positives ====
def test_red_controlled_not_electronics():
    assert _dom("a controlled release drug capsule") != "electronics_electrical"

def test_red_compiled_not_electronics():
    assert _dom("a compiled report") != "electronics_electrical"

def test_red_knowledge_not_electronics():
    assert _dom("a knowledge base article") != "electronics_electrical"

def test_red_patriotic_not_electronics():
    assert _dom("patriotic banner") != "electronics_electrical"

def test_red_concurrent_not_electronics():
    assert _dom("concurrent tasks") != "electronics_electrical"

def test_red_hearth_not_medical():
    assert _dom("a hearth warmer") != "medical_device"


# ------------------------------------------------- RED: real Web /start effect ----
def test_red_web_start_false_positive_no_medical_guidance():
    """A false-positive medical classification currently alters /start to emit the
    medical-conflict mechanism guidance. Post-fix `hearth warmer` is not medical, so
    that guidance MUST NOT appear (real route, real classifier)."""
    from web import app as web_app
    client = web_app.app.test_client()
    resp = client.post("/start", data={"idea": "a hearth warmer",
                                        "domain_confirm": "electronics_electrical"},
                        follow_redirects=False)
    body = resp.get_data(as_text=True)
    assert web_app.MECHANISM_GUIDANCE_MESSAGE not in body
    # session cleanup (defensive: if a session was created, drop it)
    loc = resp.headers.get("Location", "")
    if "/session/" in loc:
        web_app.SESSION_STORE.pop(loc.rsplit("/", 1)[-1], None)


# --------------------------------------------------- RED: real CLI confirmation ---
def _load_run_cli():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts", "run_cli.py")
    spec = importlib.util.spec_from_file_location("run_cli_cf5f003", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_red_cli_false_positive_no_electronics_confirmation(monkeypatch, capsys):
    """`concurrent tasks` currently mis-infers electronics -> untruthful CLI 'Domain
    inferred: electronics_electrical'. Post-fix it infers unknown."""
    mod = _load_run_cli()
    monkeypatch.setattr(builtins, "input", lambda *_a, **_k: "concurrent tasks")
    mod.run_cli()
    out = capsys.readouterr().out
    assert "Domain inferred: electronics_electrical" not in out


# ------------------------------------------- GREEN: singular + plural preservation -
@pytest.mark.parametrize("idea,dom", [
    ("an LED circuit", "electronics_electrical"),
    ("smart LEDs for home lighting", "electronics_electrical"),
    ("a single sensor", "electronics_electrical"),
    ("a design with several sensors", "electronics_electrical"),
    ("one circuit board", "electronics_electrical"),
    ("multiple circuits", "electronics_electrical"),
    ("a resistor", "electronics_electrical"),
    ("several resistors", "electronics_electrical"),
    ("a PCB layout", "electronics_electrical"),
    ("two PCBs", "electronics_electrical"),
    ("an ESP32 board", "electronics_electrical"),
    ("a gear", "mechanical"),
    ("interlocking gears", "mechanical"),
    ("a lever", "mechanical"),
    ("two levers", "mechanical"),
    ("a catheter", "medical_device"),
    ("sterile catheters", "medical_device"),
    ("a mobile app", "software"),
    ("several apps", "software"),
    ("a database", "software"),
    ("linked databases", "software"),
    ("a REST API", "software"),
    ("multiple APIs", "software"),
])
def test_green_singular_and_plural_preserved(idea, dom):
    assert _dom(idea) == dom


# ------------------------------------------------- GREEN: false positives cleared -
@pytest.mark.parametrize("idea", [
    "a controlled release drug capsule", "a compiled report", "patriotic banner",
    "concurrent tasks", "a knowledge base article", "an online ledger",
])
def test_green_no_electronics_false_positive(idea):
    assert _dom(idea) != "electronics_electrical"

def test_green_hearth_not_medical():
    assert _dom("a hearth warmer") != "medical_device"


# ------------------------------------------------- GREEN: multi-word + punctuation -
@pytest.mark.parametrize("idea,dom", [
    ("a drug delivery system", "medical_device"),
    ("a drug-delivery device", "medical_device"),          # punctuation-separated phrase
    ("a machine learning model", "software"),
    ("a neural network", "medical_device"),                # neural(med) ties neural-network(soft) -> fallback medical
    ("ESP32.", "electronics_electrical"),                   # punctuation-adjacent token
    ("(LED)", "electronics_electrical"),
])
def test_green_multiword_and_punctuation(idea, dom):
    assert _dom(idea) == dom


# --------------------------------------------------- GREEN: domain-flip guard ------
def test_green_gears_and_levers_stays_mechanical():
    assert _dom("a system of gears and levers") == "mechanical"


def test_green_es_plural_path_load_bearing():
    # The bounded +es plural (§4.3) is inventory-inert for common plurals (+s), but
    # must remain load-bearing for a sibilant-ending signal. `diagnosis` is the only
    # such registered signal; its +es token form exercises the path.
    assert _dom("several diagnosises") == "medical_device"


# =========================================== GREEN: containment preservation (§A6) =
# --- singular container ---
@pytest.mark.parametrize("idea,dom", [
    ("an implantable sensor", "medical_device"),
    ("an implantable circuit", "medical_device"),
    ("an implantable PCB", "medical_device"),
    ("an application with a sensor", "software"),
    ("an application controlling a circuit", "software"),
])
def test_green_containment_singular_container(idea, dom):
    assert _dom(idea) == dom

# --- plural container (Amendment 01 M1: container matched via bounded plural) ---
@pytest.mark.parametrize("idea,dom", [
    ("applications with a sensor", "software"),
    ("applications controlling a circuit", "software"),
    ("implantables in a sensor", "medical_device"),
    ("implantables with a circuit", "medical_device"),
    ("medical implantables with a circuit", "medical_device"),
])
def test_green_containment_plural_container(idea, dom):
    assert _dom(idea) == dom

# --- containment is real reinforcement: medical scores 2 on `implantable sensor` ---
def test_green_containment_gives_two_signals_medical():
    assert _score("an implantable sensor", "medical_device") == 2      # implant + implantable
    assert _score("an implantable sensor", "electronics_electrical") == 1  # sensor
def test_green_containment_gives_two_signals_software():
    assert _score("an application with a sensor", "software") == 2     # app + application
    assert _score("applications with a sensor", "software") == 2       # plural container, same


# ================================= GREEN: cross-domain non-leakage (§A6 / §A2) =====
@pytest.mark.parametrize("idea", ["a biosensor", "biosensors", "a biosensor device"])
def test_green_biosensor_stays_medical_no_electronics_leak(idea):
    assert _dom(idea) == "medical_device"

def test_green_biosensor_does_not_credit_electronics_sensor():
    # `sensor`(electronics) is a substring of `biosensor`(medical) but CROSS-domain:
    # electronics must NOT be credited `sensor` from the medical container.
    assert _score("a biosensor", "electronics_electrical") == 0
    assert _score("a biosensor", "medical_device") == 1


# ============================== GREEN: at-most-once parity (anti-double-count) =====
# When the contained signal ALSO appears standalone, the domain score must equal the
# parent (substring) score (at most once), so the classification must NOT flip.
@pytest.mark.parametrize("idea", [
    "an implant that is implantable in a sensor circuit",
    "implants implantables sensors circuits",
])
def test_green_at_most_once_medical_two_not_three(idea):
    assert _score(idea, "medical_device") == 2     # implant + implantable, once each (not 3)
    assert _score(idea, "electronics_electrical") == 2
    assert _dom(idea) == "electronics_electrical"   # tie -> only-activated electronics (== parent)

@pytest.mark.parametrize("idea", [
    "an application app controlling a circuit sensor",
    "apps applications sensors circuits",
])
def test_green_at_most_once_software_two_not_three(idea):
    assert _score(idea, "software") == 2           # app + application, once each (not 3)
    assert _score(idea, "electronics_electrical") == 2
    assert _dom(idea) == "electronics_electrical"


# ================= GREEN: genuinely executed 0 / 1 / 2 / 3+ activation (§A8) =======
def test_green_zero_activated_priority_fallback(activate):
    activate()  # NO domain activated
    r = classify_domain("a circuit and gears")   # elec(circuit)=1 tie mech(gears)=1
    assert r.kind is DomainResultKind.SINGLE
    # 0 activated -> case-0 priority fallback [medical, electronics, mechanical, software]
    assert r.selected_domain == "electronics_electrical"

def test_green_one_activated_single(activate):
    activate("electronics_electrical")
    r = classify_domain("a circuit and gears")   # only electronics activated among the tie
    assert r.kind is DomainResultKind.SINGLE
    assert r.selected_domain == "electronics_electrical"

def test_green_two_activated_ambiguous_tie(activate):
    activate("electronics_electrical", "mechanical")
    r = classify_domain("a circuit and gears")   # elec + mech both activated, tied
    assert r.kind is DomainResultKind.AMBIGUOUS_TIE
    assert r.candidates == ("electronics_electrical", "mechanical")

def test_green_three_activated_ambiguous_tie(activate):
    activate("electronics_electrical", "mechanical", "medical_device")
    r = classify_domain("circuits and gears and catheters")  # all plural, all tied
    assert r.kind is DomainResultKind.AMBIGUOUS_TIE
    assert r.candidates == ("electronics_electrical", "mechanical", "medical_device")

def test_green_recognized_not_activated_priority(activate):
    activate("software")                        # neither tied domain activated
    r = classify_domain("gears and catheters")  # mechanical vs medical, both plural
    assert r.kind is DomainResultKind.SINGLE
    assert r.selected_domain == "medical_device"   # priority fallback unchanged

def test_green_none_when_no_signal():
    assert classify_domain("a plain idea with no signal").kind is DomainResultKind.NONE


# ----------------------------------------------------- GREEN: Web/CLI parity ------
def test_green_web_electronics_admitted_unchanged():
    from web import app as web_app
    client = web_app.app.test_client()
    resp = client.post("/start", data={"idea": "an ESP32 circuit with sensors",
                                        "domain_confirm": "electronics_electrical"},
                       follow_redirects=False)
    assert resp.status_code == 302 and "/session/" in resp.headers["Location"]
    sid = resp.headers["Location"].rsplit("/", 1)[-1]
    web_app.SESSION_STORE.pop(sid, None)          # session cleanup

def test_green_cli_electronics_proceeds(monkeypatch, capsys):
    mod = _load_run_cli()
    monkeypatch.setattr(builtins, "input", lambda *_a, **_k: "an electronics circuit with sensors")
    mod.run_cli()
    out = capsys.readouterr().out
    assert "Domain inferred: electronics_electrical" in out
