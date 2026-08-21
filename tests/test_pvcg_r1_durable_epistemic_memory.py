"""PVCG-R1 — Durable Epistemic Memory (integrated persistence/reconstruction proof).

File: tests/test_pvcg_r1_durable_epistemic_memory.py
Purpose: prove that the five governed NON-ANSWER epistemic dispositions
(`unknown`, `deferred`, `provisional_assumption`, `specialist_requested`,
`evidence_requested`) are written through the CANONICAL durable seam
(`SqliteRecordStore.append_record`) and reconstruct deterministically with their
epistemic meaning intact — and that nothing else changes.

Input contract: the real Flask application (`web.app`), a real on-disk SQLite
canonical store at `INVENTORAI_DB_PATH`, and the canonical reconstruction
(`engine.session_reconstruction.reconstruct_readonly_state`).
Output contract: after a genuine PROCESS restart, the durable ledger carries the
non-answer dispositions verbatim; progression (gaps / maturity / stage) is
byte-identical to the same journey without them; no duplicate durable record is
produced by a repeated submission; answered-only projects are unaffected.

Prohibited (enforced by the assertions below): persisting derived state
(`acknowledged_unknowns`), persisting display/session state, promoting any
disposition to `answered`/validated/demonstrated, letting a non-answer record
move progression, and fabricating historical records that were never written.

PROCESS BOUNDARY (PVCG §6): the reconstruction half of every restart assertion
runs in a SEPARATE Python interpreter via `_reconstruct_in_new_process`, so a
pass can never be produced by surviving in-memory objects.
"""
import json
import os
import re
import subprocess
import sys
import tempfile

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The five governed non-answer dispositions this gate makes durable.
NON_ANSWER_DISPOSITIONS = (
    "unknown",
    "deferred",
    "provisional_assumption",
    "specialist_requested",
    "evidence_requested",
)

_SEED = (
    "The device detects water on the floor because the two probe electrodes "
    "complete a circuit when the resistance between them drops, so the "
    "microcontroller closes the relay and the solenoid valve shuts off the "
    "mains water supply."
)
_ANSWER = (
    "The electrodes feed an analog input; the microcontroller compares that "
    "voltage against a threshold, and when it exceeds the threshold it triggers "
    "the relay, which drives the solenoid valve closed."
)


# --------------------------------------------------------------------------
# Harness
# --------------------------------------------------------------------------

@pytest.fixture()
def db_path(tmp_path):
    return str(tmp_path / "pvcg_r1.sqlite3")


class _Live:
    """One live application instance bound to `db_path`.

    `web.app` is (re)imported with `INVENTORAI_DB_PATH` already pointing at the
    temporary file, so the REAL durable store is exercised — never a fake.

    Isolation contract: this reload mutates interpreter-global state
    (`os.environ` and the `web.*` entries in `sys.modules`). Both are snapshotted
    here and restored exactly by `close()`, so no other test module in the suite
    observes a different `web.app` object or a leaked database path. Without that
    restoration this fixture silently breaks unrelated web tests."""

    def __init__(self, db_path):
        self._env = {k: os.environ.get(k)
                     for k in ("INVENTORAI_DB_PATH", "INVENTORAI_ENV")}
        self._modules = {name: module for name, module in sys.modules.items()
                         if name == "web" or name.startswith("web.")}
        os.environ["INVENTORAI_DB_PATH"] = db_path
        os.environ.pop("INVENTORAI_ENV", None)
        for name in list(self._modules):
            del sys.modules[name]
        import web.app as app_module
        app_module.app.config["TESTING"] = True
        self.mod = app_module
        self.client = app_module.app.test_client()

    def close(self):
        """Restore the interpreter to exactly its pre-fixture state."""
        for name in [n for n in list(sys.modules)
                     if n == "web" or n.startswith("web.")]:
            del sys.modules[name]
        sys.modules.update(self._modules)
        for key, value in self._env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value

    # -- journey helpers ---------------------------------------------------
    def start(self, idea=_SEED):
        response = self.client.post("/start", data={"idea": idea})
        if response.status_code == 200:
            body = response.get_data(as_text=True)
            confirm = re.search(r'name="domain_confirm" value="([^"]+)"', body)
            data = {"idea": idea}
            if confirm:
                data["domain_confirm"] = confirm.group(1)
            response = self.client.post("/start", data=data)
        assert response.status_code == 302, response.status_code
        location = response.headers["Location"]
        assert "/session/" in location, location
        return location.rstrip("/").split("/")[-1]

    def token(self, sid):
        page = self.client.get("/session/%s" % sid).get_data(as_text=True)
        found = re.search(r'name="answer_token" value="([^"]+)"', page)
        return found.group(1) if found else ""

    def act(self, sid, action, response=""):
        return self.client.post(
            "/session/%s" % sid,
            data={"action": action, "response": response,
                  "answer_token": self.token(sid)},
            follow_redirects=True,
        )

    def ledger(self, sid):
        entry = self.mod.SESSION_STORE.get(sid)
        return [(a.disposition, a.gap_context) for a in entry["state"].assertions]


@pytest.fixture()
def live(db_path):
    session = _Live(db_path)
    try:
        yield session
    finally:
        session.close()


_RECONSTRUCT_SNIPPET = r"""
import json, os, sys, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, {root!r})
os.environ["INVENTORAI_DB_PATH"] = {db!r}
os.environ.pop("INVENTORAI_ENV", None)
from engine.record_store import SqliteRecordStore
from engine.session_reconstruction import reconstruct_readonly_state
store = SqliteRecordStore({db!r})
recon = reconstruct_readonly_state(store, {sid!r})
review, state = recon.review, recon.state
out = {{
    "level": review.level,
    "status": review.status,
    "maturity_level": review.maturity_level,
    "current_stage": review.current_stage,
    "open_gaps": list(review.open_gaps),
    "accepted_answer_count": len(review.accepted_answer_evidence),
    "ledger": [] if state is None else [
        {{"record_id": a.record_id, "disposition": a.disposition,
          "content": a.content, "gap_context": a.gap_context,
          "provenance": a.provenance, "validation_status": a.validation_status,
          "quality": a.quality, "pending": a.pending,
          "resolves_gap": a.resolves_gap}}
        for a in state.assertions],
    "acknowledged_unknowns": [] if state is None else [
        {{"gap_context": u.gap_context, "verbatim": u.verbatim}}
        for u in state.acknowledged_unknowns],
    "gaps": [] if state is None else [
        [g.gap_type, g.status] for g in state.gaps],
}}
print("PVCG_R1_JSON" + json.dumps(out))
"""


def _reconstruct_in_new_process(db_path, sid):
    """Reconstruct in a FRESH interpreter — a genuine process boundary."""
    code = _RECONSTRUCT_SNIPPET.format(root=ROOT, db=db_path, sid=sid)
    proc = subprocess.run([sys.executable, "-c", code],
                          capture_output=True, text=True, cwd=ROOT)
    assert proc.returncode == 0, proc.stderr
    marker = [ln for ln in proc.stdout.splitlines()
              if ln.startswith("PVCG_R1_JSON")]
    assert marker, proc.stdout + proc.stderr
    return json.loads(marker[-1][len("PVCG_R1_JSON"):])


def _durable_rows(db_path, sid):
    import sqlite3
    conn = sqlite3.connect(db_path)
    try:
        return [(seq, record_id, json.loads(payload)) for seq, record_id, payload
                in conn.execute(
                    "SELECT seq, record_id, payload FROM records "
                    "WHERE project_id = ? ORDER BY seq", (sid,))]
    finally:
        conn.close()


# --------------------------------------------------------------------------
# Control — the already-durable answered path (must stay green, unchanged)
# --------------------------------------------------------------------------

def test_control_answered_record_already_persists_and_reconstructs(live, db_path):
    sid = live.start()
    live.act(sid, "answered", _ANSWER)
    rows = _durable_rows(db_path, sid)
    assert [r[2]["disposition"] for r in rows] == ["answered"], rows
    out = _reconstruct_in_new_process(db_path, sid)
    assert out["level"] == 1 and out["status"] == "RECONSTRUCTED"
    assert [r["disposition"] for r in out["ledger"]] == ["answered"]
    assert out["accepted_answer_count"] == 1


# --------------------------------------------------------------------------
# RED core — each governed non-answer disposition must survive a real restart
# --------------------------------------------------------------------------

@pytest.mark.parametrize("disposition", NON_ANSWER_DISPOSITIONS)
def test_non_answer_disposition_is_accepted_in_session(live, disposition):
    """Precondition: the action is accepted and recorded in the live ledger."""
    sid = live.start()
    live.act(sid, disposition, "")
    assert (disposition, "MECHANISM_COMPLETENESS") in live.ledger(sid)


@pytest.mark.parametrize("disposition", NON_ANSWER_DISPOSITIONS)
def test_non_answer_disposition_survives_process_restart(live, db_path,
                                                         disposition):
    """THE R1 CLAIM: the disposition reconstructs from the canonical store in a
    brand-new process."""
    sid = live.start()
    live.act(sid, disposition, "")
    out = _reconstruct_in_new_process(db_path, sid)
    assert out["level"] == 1, out
    assert disposition in [r["disposition"] for r in out["ledger"]], out["ledger"]


def test_all_five_dispositions_survive_together_in_recorded_order(live, db_path):
    sid = live.start()
    for disposition in NON_ANSWER_DISPOSITIONS:
        live.act(sid, disposition, "")
    out = _reconstruct_in_new_process(db_path, sid)
    assert [r["disposition"] for r in out["ledger"]] == list(NON_ANSWER_DISPOSITIONS)


# --------------------------------------------------------------------------
# Epistemic meaning must be preserved — no promotion by becoming durable
# --------------------------------------------------------------------------

def test_provisional_assumption_reconstructs_provisional_and_unvalidated(
        live, db_path):
    sid = live.start()
    live.act(sid, "provisional_assumption", "assume mains power is available")
    record = _one(_reconstruct_in_new_process(db_path, sid),
                  "provisional_assumption")
    assert record["disposition"] == "provisional_assumption"
    assert record["validation_status"] == "UNVALIDATED"
    assert record["resolves_gap"] is False
    assert record["content"] == "assume mains power is available"


def test_specialist_request_reconstructs_as_a_pending_request_not_evidence(
        live, db_path):
    sid = live.start()
    live.act(sid, "specialist_requested", "")
    record = _one(_reconstruct_in_new_process(db_path, sid),
                  "specialist_requested")
    assert record["pending"] == "specialist"
    assert record["validation_status"] == "UNVALIDATED"
    assert record["quality"] is None
    assert record["resolves_gap"] is False


def test_evidence_request_reconstructs_pending_not_demonstrated(live, db_path):
    sid = live.start()
    live.act(sid, "evidence_requested", "")
    record = _one(_reconstruct_in_new_process(db_path, sid), "evidence_requested")
    assert record["pending"] == "evidence"
    assert record["validation_status"] == "UNVALIDATED"
    assert record["quality"] != "DEMONSTRATED"
    assert record["resolves_gap"] is False


def test_unknown_and_deferred_never_reconstruct_as_answered(live, db_path):
    sid = live.start()
    live.act(sid, "unknown", "")
    live.act(sid, "deferred", "come back to this")
    out = _reconstruct_in_new_process(db_path, sid)
    dispositions = [r["disposition"] for r in out["ledger"]]
    assert "answered" not in dispositions, out["ledger"]
    assert dispositions == ["unknown", "deferred"]
    assert all(r["resolves_gap"] is False for r in out["ledger"])
    assert all(r["provenance"] == "LEGACY_UNSPECIFIED" for r in out["ledger"])


def _one(out, disposition):
    matches = [r for r in out["ledger"] if r["disposition"] == disposition]
    assert len(matches) == 1, out["ledger"]
    return matches[0]


# --------------------------------------------------------------------------
# No false progress — durability must not move progression
# --------------------------------------------------------------------------

def test_durable_non_answer_records_do_not_change_reconstructed_progression(
        live, db_path, tmp_path):
    """Two identical journeys, one with five extra non-answer actions: the
    reconstructed gaps / maturity / stage must be identical."""
    sid_plain = live.start()
    live.act(sid_plain, "answered", _ANSWER)
    plain = _reconstruct_in_new_process(db_path, sid_plain)

    sid_rich = live.start()
    for disposition in NON_ANSWER_DISPOSITIONS:
        live.act(sid_rich, disposition, "")
    live.act(sid_rich, "answered", _ANSWER)
    for disposition in NON_ANSWER_DISPOSITIONS:
        live.act(sid_rich, disposition, "")
    rich = _reconstruct_in_new_process(db_path, sid_rich)

    assert rich["maturity_level"] == plain["maturity_level"]
    assert rich["current_stage"] == plain["current_stage"]
    assert rich["open_gaps"] == plain["open_gaps"]
    assert rich["gaps"] == plain["gaps"]
    assert rich["accepted_answer_count"] == plain["accepted_answer_count"] == 1
    assert len(rich["ledger"]) == 11


# --------------------------------------------------------------------------
# Idempotency — one accepted event, one durable truth
# --------------------------------------------------------------------------

def test_repeated_identical_non_answer_submission_writes_one_durable_record(
        live, db_path):
    sid = live.start()
    for _ in range(4):
        live.act(sid, "unknown", "")
    rows = [r for r in _durable_rows(db_path, sid)
            if r[2]["disposition"] == "unknown"]
    assert len(rows) == 1, rows
    assert len(live.ledger(sid)) == 1, live.ledger(sid)


def test_distinct_non_answer_actions_are_not_collapsed(live, db_path):
    sid = live.start()
    live.act(sid, "unknown", "")
    live.act(sid, "deferred", "")
    live.act(sid, "deferred", "with a different note")
    rows = [r[2]["disposition"] for r in _durable_rows(db_path, sid)]
    assert rows == ["unknown", "deferred", "deferred"], rows


def test_durable_failure_leaves_no_in_memory_record_persist_before_acknowledge(
        live, db_path, monkeypatch):
    """If the canonical append fails, NOTHING is acknowledged: no in-memory
    ledger record, no interaction metadata, and a truthful failure message.
    Live memory must never claim a truth the store does not hold."""
    from engine.record_store import StoreError
    sid = live.start()
    before = list(live.mod.SESSION_STORE[sid]["state"].assertions)

    store = live.mod._get_store()
    monkeypatch.setattr(
        store, "append_record",
        lambda *a, **k: (_ for _ in ()).throw(StoreError("durable unavailable")))
    # `_answer_error` / `_interaction_ack` are POPPED by the render, so the
    # user-visible page is the honest place to assert what was communicated.
    page = live.act(sid, "unknown", "").get_data(as_text=True)

    entry = live.mod.SESSION_STORE[sid]
    assert entry["state"].assertions == before
    assert entry.get("interaction_actions") in (None, [])
    assert [r[2]["disposition"] for r in _durable_rows(db_path, sid)] == []
    assert live.mod.INTERACTION_NOT_SAVED_MESSAGE in page
    assert live.mod._NON_ANSWER_ACK["unknown"] not in page


def test_durable_failure_message_is_distinct_from_the_answered_message(live):
    """A non-answer action must not be misdescribed as an answer."""
    assert (live.mod.INTERACTION_NOT_SAVED_MESSAGE
            != live.mod.ANSWER_NOT_SAVED_MESSAGE)
    from web import ui_text
    assert ui_text.localize_message(
        live.mod.INTERACTION_NOT_SAVED_MESSAGE, "ar") \
        != live.mod.INTERACTION_NOT_SAVED_MESSAGE


def test_repeated_reconstruction_is_stable_and_appends_nothing(live, db_path):
    sid = live.start()
    live.act(sid, "unknown", "")
    live.act(sid, "answered", _ANSWER)
    first = _reconstruct_in_new_process(db_path, sid)
    second = _reconstruct_in_new_process(db_path, sid)
    assert first == second
    assert len(_durable_rows(db_path, sid)) == 2


# --------------------------------------------------------------------------
# No second truth source / derived state stays derived
# --------------------------------------------------------------------------

def test_acknowledged_unknowns_are_rederived_never_separately_persisted(
        live, db_path):
    """`AcknowledgedUnknown` is DERIVED from answered content by the canonical
    replay. It must never appear as a durable record of its own."""
    sid = live.start()
    live.act(sid, "answered",
             "I do not know the exact trip threshold for the electrode circuit "
             "yet, but the relay is driven by the microcontroller because the "
             "sensor voltage crosses a comparator level.")
    out = _reconstruct_in_new_process(db_path, sid)
    assert out["acknowledged_unknowns"], out
    stored = [r[2]["disposition"] for r in _durable_rows(db_path, sid)]
    assert stored == ["answered"], stored


def test_durable_store_holds_exactly_one_ledger_and_no_parallel_table(db_path,
                                                                     live):
    import sqlite3
    sid = live.start()
    live.act(sid, "unknown", "")
    conn = sqlite3.connect(db_path)
    try:
        tables = sorted(row[0] for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' "
            "AND name NOT LIKE 'sqlite_%'"))
    finally:
        conn.close()
    assert tables == ["projects", "records"], tables


# --------------------------------------------------------------------------
# Backward compatibility — answered-only history is untouched and not invented
# --------------------------------------------------------------------------

def test_answered_only_project_reconstructs_identically(live, db_path):
    sid = live.start()
    live.act(sid, "answered", _ANSWER)
    before = _reconstruct_in_new_process(db_path, sid)
    assert before["maturity_level"] == 1
    assert before["open_gaps"] == ["MECHANISM_COMPLETENESS"]
    assert [r["disposition"] for r in before["ledger"]] == ["answered"]
    assert before["acknowledged_unknowns"] == []


def test_missing_historical_non_answer_records_are_never_fabricated(live,
                                                                    db_path):
    """A project that never recorded a non-answer action must reconstruct with
    none — historical loss stays historical loss."""
    sid = live.start()
    live.act(sid, "answered", _ANSWER)
    out = _reconstruct_in_new_process(db_path, sid)
    assert all(r["disposition"] == "answered" for r in out["ledger"])
    assert len(out["ledger"]) == 1
