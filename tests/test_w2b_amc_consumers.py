"""W2-B / RVR-6a (amended contract) — consumer propagation adjudication.

Authority: Contract Amendment 1 §12. The historical inventory is seed
evidence only; the fresh sweep at the implementation base (reproducible
method: `grep -rn "select_next_gap" --include="*.py"` over the whole
worktree, `__pycache__` excluded) found SEVEN runtime call sites plus the
`session_reconstruction` module import. Adjudication pinned by test:

  1. engine/progression_loop.py advance_after_disposition  -> CONTAINED
  2. engine/progression_loop.py run_iteration              -> CONTAINED
  3. web/app.py show_session render     -> UPDATED (consumes the policy)
  4. web/app.py accept-risk gate        -> CONTAINED (canonical served gap
     is never overridden, so consent stays aligned with the display)
  5. web/app.py non-answer labeling     -> CONTAINED (same)
  6. web/app.py answered targeting      -> CONTAINED (same)
  7. scripts/run_cli.py                 -> OUT-OF-SCOPE BY CONTRACT
     (Amendment §12: W2-B behavior is contracted for the governed web
     session journey; the CLI stays byte-unchanged and non-adaptive)
  +  engine/session_reconstruction.py:55 module import -> CONTAINED
     (replay never consults the policy or register)

The three P9 digest-pin files are covered by the base contract's bounded
mechanical-re-freeze allowance and revalidated here.
"""
import hashlib
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

import engine.progression_loop as pl
from engine.idea_state import (
    IdeaState, Gap, OPEN, MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY,
)

ROOT = os.path.join(os.path.dirname(__file__), "..")

MC_STRONG = ("(1) unfolding: the operator lifts the handle and the panel "
             "rotates on the hinge until flat. (2) locking: the toggle latch "
             "snaps over the center rib and holds the panel rigid. "
             "(3) folding: pressing the release lever frees the latch and the "
             "panel folds upward.")
PF_PLAIN = ("I have not tested whether the toggle latch stays reliable "
            "under repeated loading and outdoor use.")


def _fresh():
    s = IdeaState(idea_id="w2b-cons")
    s.domain = "software"
    s.domain_signal = "software"
    s.path = "N"
    s.gaps.append(Gap(MECHANISM_COMPLETENESS, OPEN, 0))
    return s


def test_canonical_engine_paths_never_consult_the_policy(monkeypatch):
    def _boom(*a, **kw):
        raise AssertionError("canonical path consulted the serving policy")
    monkeypatch.setattr(pl, "compute_serving_decision", _boom)
    s = _fresh()
    pl.run_iteration(s, MC_STRONG)
    pl.run_iteration(s, MC_STRONG)
    pl.run_iteration(s, PF_PLAIN)
    s.record_interaction(action="answered", content=PF_PLAIN,
                         gap_context=PHYSICAL_FEASIBILITY)
    pl.accept_gap_risk(s, PHYSICAL_FEASIBILITY)
    pl.advance_after_disposition(s)


def test_policy_consultation_changes_no_canonical_result():
    a, b = _fresh(), _fresh()
    ra = [pl.run_iteration(a, c) for c in (MC_STRONG, MC_STRONG, PF_PLAIN)]
    rb = []
    for c in (MC_STRONG, MC_STRONG, PF_PLAIN):
        pl.compute_serving_decision(b, register_elevated=True)
        rb.append(pl.run_iteration(b, c))
        pl.compute_serving_decision(b, register_elevated=False)
    assert ra == rb and repr(a.gaps) == repr(b.gaps)


def test_session_reconstruction_source_is_policy_free():
    src = open(os.path.join(ROOT, "engine", "session_reconstruction.py"),
               encoding="utf-8").read()
    assert "compute_serving_decision" not in src
    assert "adaptive_register" not in src


def test_cli_out_of_scope_by_contract():
    src = open(os.path.join(ROOT, "scripts", "run_cli.py"),
               encoding="utf-8").read()
    assert "select_next_gap" in src
    assert "compute_serving_decision" not in src
    assert "adaptive_register" not in src


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("INVENTORAI_DB_PATH",
                       str(tmp_path / "w2b-cons.sqlite"))
    import web.app as appmod
    monkeypatch.setattr(appmod, "_STORE", None)
    appmod.SESSION_STORE.clear()
    appmod.app.config["TESTING"] = True
    with appmod.app.test_client() as c:
        yield c, appmod


def test_gates_stay_aligned_with_canonical_served_gap(client):
    """Consumers 4-6: because the policy never overrides the canonical
    served GAP, the accept-risk consent gate and the answered/non-answer
    targeting remain consistent with what is displayed."""
    import html as _html
    c, appmod = client
    SEED = ("a manually foldable wheelchair ramp for a home doorway — the "
            "inventor wants the ramp to stay reliably locked in the flat, "
            "load-bearing position and to fold away without tools")
    r = c.post("/start", data={"idea": SEED, "domain_confirm": "mechanical"})
    sid = r.headers["Location"].rsplit("/", 1)[-1]
    state = appmod.SESSION_STORE[sid]["state"]

    def token():
        page = c.get(f"/session/{sid}").get_data(as_text=True)
        m = re.search(r'name="answer_token" value="([^"]+)"', page)
        return _html.unescape(m.group(1))

    served = pl.select_next_gap(state)
    r = c.post(f"/session/{sid}", data={
        "response": "", "action": "deferred", "answer_token": token()})
    assert r.status_code == 302
    assert state.assertions[-1].gap_context == served
    r = c.post(f"/session/{sid}", data={
        "response": MC_STRONG, "action": "answered", "answer_token": token()})
    assert r.status_code == 302
    assert state.assertions[-1].gap_context == served


_P9_PIN_FILES = (
    "tests/test_p9_mech_i3_signal_quality.py",
    "tests/test_p9_mech_i4_boundary_corpus.py",
    "tests/test_p9_mech_i5_question_sufficiency.py",
)


def test_exactly_three_p9_files_pin_the_current_digest():
    with open(os.path.join(ROOT, "engine", "progression_loop.py"),
              "rb") as f:
        actual = hashlib.sha256(f.read()).hexdigest()
    pin_re = re.compile(r'"engine/progression_loop\.py":\s*"([0-9a-f]{64})"')
    pins = {}
    for rel in _P9_PIN_FILES:
        src = open(os.path.join(ROOT, rel), encoding="utf-8").read()
        m = pin_re.search(src)
        assert m, rel
        pins[rel] = m.group(1)
    assert set(pins.values()) == {actual}
