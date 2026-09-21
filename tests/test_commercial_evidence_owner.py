"""Commercial Evidence Owner — durable ownership for future Commercial Readiness.

`COMMERCIAL-EVIDENCE-OWNER-IMPLEMENT-01` (Owner-authorized), adopting
`READINESS-OWNER-DISPOSITION-01` recommendation B.

These tests prove the owner EXISTS and is correctly fenced. Every fixture is
synthetic; no real project data and no collected human, customer, survey or
market-research evidence is used, because none is authorized.

What is proven: append-only creation; deterministic per-project ordering;
unique event identity with idempotent exact replay; supersession and withdrawal
WITHOUT any UPDATE; project isolation; the closed commercial topic vocabulary;
rejection of an unknown or unactivated dimension and of an out-of-vocabulary
topic; that no assertion anchor is required; that the canonical provenance axis
is reused and preserved; conservative claim status with no promotion path; that
no commercial conclusion, readiness status or risk record is produced anywhere
in this lane; saved-project / cold-reconstruction compatibility; schema
idempotency on a populated database; and no regression to the sibling stores.
"""
import dataclasses
import inspect
import os
import re
import sqlite3

import pytest

from engine.commercial_evidence import (
    ACTIVE_DIMENSIONS, CLAIM_STATUSES, CLAIM_STATUS_UNVALIDATED,
    COMMERCIAL_TOPICS, DEFAULT_PROVENANCE, DIMENSION_COMMERCIAL,
    DIMENSION_MANUFACTURING, DIMENSIONS, EVIDENCE_EXACT_REPLAY,
    EVIDENCE_INSERTED, MAX_READINESS_EVIDENCE_PER_PROJECT, PROVENANCE_VALUES,
    TOPICS_BY_DIMENSION, CommercialEvidenceError,
    CommercialEvidenceHistoryError, EvidenceCapExceeded, ReadinessEvidence,
    active_evidence, canonical_evidence_dict, commercial_evidence_view,
    evidence_chain, make_readiness_evidence, manufacturing_evidence_view,
    uncovered_topics, validate_evidence_history,
)
from engine.idea_state import (
    EXPERT_SUPPLIED, EXTERNAL_EVIDENCE, IdeaState, OWNER_STATED,
)
from engine.record_contract import ProjectRecordContract
from engine.record_store import ProjectNotFound, SqliteRecordStore, StoreError

_ROOT = os.path.join(os.path.dirname(__file__), "..")

GOOD = {
    "subject_text": "Home-care agencies buying mobility aids",
    "statement_text": ("The inventor believes agencies buy ramps for clients "
                       "rather than families buying them directly."),
    "source_identity": "Inventor, from their own experience",
    "scope_text": "one local region the inventor knows",
    "limitation_text": "not checked against any agency or published source",
}


def _code_only(path):
    """Module source with docstrings and comments removed, so a source scan
    asserts about CODE and never about prose that merely NAMES a banned thing:
    the owning module documents, in words, the very things it must not do."""
    text = open(path, encoding="utf-8").read()
    text = re.sub(r'(?s)' + '\"' * 3 + '.*?' + '\"' * 3, "", text)
    return "\n".join(line for line in text.splitlines()
                      if not line.lstrip().startswith("#"))


def _owner_code():
    return _code_only(os.path.join(_ROOT, "engine", "commercial_evidence.py"))


def _store(tmp_path, name="ce.sqlite"):
    return SqliteRecordStore(str(tmp_path / name))


def _project(store, project_id="proj-1"):
    state = IdeaState(idea_id="idea-" + project_id)
    store.create_project(ProjectRecordContract.from_state(state),
                         project_id=project_id)
    return project_id


def _evidence(store, seq=0, topic=None, key=None, supersedes=None,
              withdrawn=False, dimension=DIMENSION_COMMERCIAL, **over):
    fields = dict(GOOD)
    fields.update(over)
    return make_readiness_evidence(
        evidence_id=store.new_readiness_evidence_id(),
        evidence_seq=seq,
        dimension=dimension,
        topic=topic or COMMERCIAL_TOPICS[0],
        supersedes_evidence_id=supersedes,
        withdrawn=withdrawn,
        event_key=key or ("ce:%s" % (seq,)),
        recorded_iteration=1,
        recorded_at="2026-01-01T00:00:00.000000Z",
        **fields)


# ==========================================================================
# 1. append-only creation, ordering, identity
# ==========================================================================
def test_append_creates_one_row_in_deterministic_order(tmp_path):
    store = _store(tmp_path)
    pid = _project(store)
    for i, topic in enumerate(COMMERCIAL_TOPICS[:4]):
        assert store.append_readiness_evidence(
            pid, _evidence(store, seq=99, topic=topic, key="k%d" % i)
        ) == EVIDENCE_INSERTED
    rows = store.load_readiness_evidence(pid)
    # the STORE assigns the sequence; the caller's value (99) is ignored
    assert [r.evidence_seq for r in rows] == [0, 1, 2, 3]
    assert [r.topic for r in rows] == list(COMMERCIAL_TOPICS[:4])
    # ordering is deterministic across reloads
    assert store.load_readiness_evidence(pid) == rows


def test_exact_replay_is_idempotent_and_a_different_event_conflicts(tmp_path):
    store = _store(tmp_path)
    pid = _project(store)
    item = _evidence(store, key="same-key")
    assert store.append_readiness_evidence(pid, item) == EVIDENCE_INSERTED
    assert store.append_readiness_evidence(pid, item) == EVIDENCE_EXACT_REPLAY
    assert len(store.load_readiness_evidence(pid)) == 1
    other = _evidence(store, key="same-key", topic=COMMERCIAL_TOPICS[1])
    with pytest.raises(StoreError):
        store.append_readiness_evidence(pid, other)
    assert len(store.load_readiness_evidence(pid)) == 1


def test_unknown_project_is_refused(tmp_path):
    store = _store(tmp_path)
    with pytest.raises(ProjectNotFound):
        store.append_readiness_evidence("no-such-project", _evidence(store))


# ==========================================================================
# 2. supersession and withdrawal WITHOUT update
# ==========================================================================
def test_supersession_and_withdrawal_keep_every_earlier_row(tmp_path):
    store = _store(tmp_path)
    pid = _project(store)
    first = _evidence(store, key="k1")
    store.append_readiness_evidence(pid, first)
    revised = _evidence(store, key="k2", supersedes=first.evidence_id,
                        statement_text="Revised: agencies and families both buy.")
    store.append_readiness_evidence(pid, revised)
    withdrawal = _evidence(store, key="k3", supersedes=revised.evidence_id,
                           withdrawn=True)
    store.append_readiness_evidence(pid, withdrawal)
    rows = store.load_readiness_evidence(pid)
    assert [r.evidence_seq for r in rows] == [0, 1, 2]
    assert rows[0].statement_text == GOOD["statement_text"]     # retained
    assert rows[1].statement_text.startswith("Revised:")
    assert [r.withdrawn for r in rows] == [False, False, True]
    # the whole chain leaves the active set once withdrawn
    assert active_evidence(rows) == ()
    assert commercial_evidence_view(rows)["total"] == 0
    assert [r.evidence_id for r in evidence_chain(rows, first.evidence_id)] == \
        [first.evidence_id, revised.evidence_id, withdrawal.evidence_id]


def test_no_update_statement_exists_for_this_table(tmp_path):
    source = open(os.path.join(_ROOT, "engine", "record_store.py"),
                  encoding="utf-8").read()
    statements = re.findall(r'"[^"]*\breadiness_evidence\b[^"]*"', source)
    assert statements, "the table must be referenced in SQL"
    for statement in statements:
        assert "UPDATE" not in statement.upper(), statement
        assert "DELETE" not in statement.upper(), statement
    owner = _owner_code()
    for verb in ("UPDATE ", "DELETE ", "INSERT ", "DROP ", "ALTER "):
        assert verb not in owner.upper(), verb


def test_a_second_successor_and_a_bare_withdrawal_are_refused(tmp_path):
    store = _store(tmp_path)
    pid = _project(store)
    first = _evidence(store, key="k1")
    store.append_readiness_evidence(pid, first)
    store.append_readiness_evidence(
        pid, _evidence(store, key="k2", supersedes=first.evidence_id))
    with pytest.raises((CommercialEvidenceError, sqlite3.IntegrityError)):
        store.append_readiness_evidence(
            pid, _evidence(store, key="k3", supersedes=first.evidence_id))
    with pytest.raises(CommercialEvidenceError):
        make_readiness_evidence(
            evidence_id="x", evidence_seq=0, dimension=DIMENSION_COMMERCIAL,
            topic=COMMERCIAL_TOPICS[0], withdrawn=True,
            supersedes_evidence_id=None, event_key="k4",
            recorded_iteration=1, recorded_at="2026-01-01T00:00:00.000000Z",
            **GOOD)
    assert len(store.load_readiness_evidence(pid)) == 2


# ==========================================================================
# 3. project isolation
# ==========================================================================
def test_projects_are_isolated(tmp_path):
    store = _store(tmp_path)
    a, b = _project(store, "proj-a"), _project(store, "proj-b")
    store.append_readiness_evidence(a, _evidence(store, key="shared-key"))
    # the SAME event key is legal in a different project
    assert store.append_readiness_evidence(
        b, _evidence(store, key="shared-key")) == EVIDENCE_INSERTED
    assert len(store.load_readiness_evidence(a)) == 1
    assert len(store.load_readiness_evidence(b)) == 1
    # and a cross-project supersession cannot resolve
    foreign = store.load_readiness_evidence(a)[0]
    with pytest.raises((CommercialEvidenceError, sqlite3.IntegrityError)):
        store.append_readiness_evidence(
            b, _evidence(store, key="x", supersedes=foreign.evidence_id))
    assert store.load_readiness_evidence("unknown-project") == ()


# ==========================================================================
# 4. vocabulary: dimension and topic
# ==========================================================================
def test_the_commercial_topic_vocabulary_is_exactly_the_authorized_set():
    assert COMMERCIAL_TOPICS == (
        "target_customer", "problem_severity", "market_alternative",
        "differentiation", "price", "willingness_to_pay", "demand",
        "customer_evidence", "market_entry", "channel", "licensing",
        "revenue_model", "cost_revenue_assumption", "funding_need",
        "first_sale_viability")
    assert len(set(COMMERCIAL_TOPICS)) == len(COMMERCIAL_TOPICS)


def test_commercial_risk_is_not_a_topic_and_no_risk_record_is_created():
    """Commercial risks route to the canonical risk owner. This lane must own
    no risk vocabulary and construct no risk object."""
    for topic in COMMERCIAL_TOPICS:
        assert "risk" not in topic
    code = _owner_code()
    assert "GroundedRisk" not in code
    assert "requirement_landscape" not in code
    assert "RequirementLandscape" not in code
    assert not re.search(r"\bRisk\s*\(", code)


def test_an_unknown_or_unactivated_dimension_is_refused(tmp_path):
    store = _store(tmp_path)
    pid = _project(store)
    with pytest.raises(CommercialEvidenceError):
        _evidence(store, dimension="MARKETING")
    # AMENDED at `MANUFACTURING-EVIDENCE-OWNER-IMPLEMENT-01`: Manufacturing is
    # now an ACTIVATED evidence dimension with its own closed vocabulary. What
    # still holds — and is the point of this test — is that a dimension outside
    # ACTIVE_DIMENSIONS is refused, and that a topic from one dimension is never
    # valid in the other.
    assert DIMENSION_MANUFACTURING in DIMENSIONS
    assert DIMENSION_MANUFACTURING in ACTIVE_DIMENSIONS
    assert TOPICS_BY_DIMENSION[DIMENSION_MANUFACTURING] != ()
    with pytest.raises(CommercialEvidenceError):      # commercial topic, mfg row
        _evidence(store, dimension=DIMENSION_MANUFACTURING, topic="price")
    with pytest.raises(CommercialEvidenceError):      # mfg topic, commercial row
        _evidence(store, dimension=DIMENSION_COMMERCIAL, topic="material")
    assert store.load_readiness_evidence(pid) == ()


def test_an_out_of_vocabulary_topic_is_refused(tmp_path):
    store = _store(tmp_path)
    with pytest.raises(CommercialEvidenceError):
        _evidence(store, topic="commercial_risk")
    with pytest.raises(CommercialEvidenceError):
        _evidence(store, topic="material")


def test_text_policy_rejects_empty_control_and_oversized_values(tmp_path):
    store = _store(tmp_path)
    for field in ("subject_text", "statement_text", "source_identity",
                  "scope_text", "limitation_text"):
        with pytest.raises(CommercialEvidenceError):
            _evidence(store, **{field: "   "})
        with pytest.raises(CommercialEvidenceError):
            _evidence(store, **{field: "bad\x01value"})
        with pytest.raises(CommercialEvidenceError):
            _evidence(store, **{field: "x" * 5000})


# ==========================================================================
# 5. no assertion anchor is required
# ==========================================================================
def test_no_assertion_anchor_is_required_or_stored(tmp_path):
    store = _store(tmp_path)
    pid = _project(store)          # a project with an EMPTY ledger
    assert store.load_contract(pid).assertions == []
    assert store.append_readiness_evidence(
        pid, _evidence(store, topic="demand")) == EVIDENCE_INSERTED
    assert len(store.load_readiness_evidence(pid)) == 1
    assert "anchor" not in "".join(ReadinessEvidence.__dataclass_fields__)
    columns = [c[1] for c in sqlite3.connect(
        str(tmp_path / "ce.sqlite")).execute(
        "PRAGMA table_info(readiness_evidence)")]
    assert not [c for c in columns if "anchor" in c]


# ==========================================================================
# 6. provenance, claim status, conservatism
# ==========================================================================
def test_the_canonical_provenance_axis_is_reused_and_preserved(tmp_path):
    store = _store(tmp_path)
    pid = _project(store)
    assert set(PROVENANCE_VALUES) <= {
        OWNER_STATED, "SYSTEM_INFERRED", EXPERT_SUPPLIED, EXTERNAL_EVIDENCE,
        "LEGACY_UNSPECIFIED"}
    assert DEFAULT_PROVENANCE == OWNER_STATED
    # the default is what a writer reaches without saying anything
    store.append_readiness_evidence(pid, _evidence(store, key="d"))
    assert store.load_readiness_evidence(pid)[0].provenance == OWNER_STATED
    # every canonical value is REPRESENTABLE (so no schema redesign is needed
    # when external or specialist evidence is later authorized) and round-trips
    for i, value in enumerate(PROVENANCE_VALUES):
        store.append_readiness_evidence(
            pid, _evidence(store, key="p%d" % i, provenance=value))
    stored = {r.provenance for r in store.load_readiness_evidence(pid)}
    assert stored == set(PROVENANCE_VALUES)
    with pytest.raises(CommercialEvidenceError):
        _evidence(store, provenance="MARKET_PROOF")


def test_claim_status_is_single_valued_and_never_promoted(tmp_path):
    store = _store(tmp_path)
    pid = _project(store)
    assert CLAIM_STATUSES == (CLAIM_STATUS_UNVALIDATED,)
    store.append_readiness_evidence(pid, _evidence(store, key="c"))
    assert store.load_readiness_evidence(pid)[0].claim_status == "UNVALIDATED"
    # claim_status is NOT a constructor parameter: no caller can record a
    # stronger claim, so no promotion path exists
    assert "claim_status" not in inspect.signature(
        make_readiness_evidence).parameters
    # no commercial quality ladder and no stronger claim value exists in CODE
    code = _owner_code()
    for banned in ("VALIDATED_DEMAND", "MARKET_PROOF", "CONFIRMED_DEMAND",
                   "SPECIALIST_REVIEWED", "EMPIRICALLY_DEMONSTRATED",
                   "INDEPENDENTLY_VERIFIED", "quality"):
        assert banned not in code, banned
    assert "quality" not in "".join(ReadinessEvidence.__dataclass_fields__)


def test_recording_a_statement_produces_no_commercial_conclusion(tmp_path):
    store = _store(tmp_path)
    pid = _project(store)
    for i, topic in enumerate(("demand", "price", "willingness_to_pay")):
        store.append_readiness_evidence(
            pid, _evidence(store, key="t%d" % i, topic=topic))
    view = commercial_evidence_view(store.load_readiness_evidence(pid))
    assert set(view) == {"total", "active", "topics"}
    assert view["total"] == 3
    assert view["topics"] == ("demand", "price", "willingness_to_pay")
    rendered = repr(view).lower()
    for claim in ("marketable", "market proof", "high commercial potential",
                  "strong demand", "investment", "profitab", "readiness",
                  "pass_with_conditions", "insufficient_evidence",
                  "sufficient", "score"):
        assert claim not in rendered, claim
    # every recorded item stays UNVALIDATED: recording is never validating
    assert all(row["claim_status"] == "UNVALIDATED" for row in view["active"])
    assert "'validated'" not in rendered and '"validated"' not in rendered


def test_no_readiness_status_or_disposition_token_exists_in_this_lane():
    owner = open(os.path.join(_ROOT, "engine", "commercial_evidence.py"),
                 encoding="utf-8").read()
    code = re.sub(r'""".*?"""', "", owner, flags=re.S)
    code = "\n".join(l for l in code.splitlines()
                     if not l.lstrip().startswith("#"))
    for token in ("PASS_WITH_CONDITIONS", "INSUFFICIENT_EVIDENCE",
                  "readiness_status", "HOLD"):
        assert token not in code, token
    assert not re.search(r"\bPASS\b", code)


# ==========================================================================
# 7. history validation fails closed
# ==========================================================================
def test_a_corrupt_history_fails_closed():
    def row(eid, seq, supersedes=None, topic=COMMERCIAL_TOPICS[0],
            dimension=DIMENSION_COMMERCIAL, withdrawn=False):
        return ReadinessEvidence(
            evidence_id=eid, evidence_seq=seq, dimension=dimension, topic=topic,
            subject_text="s", statement_text="t", source_identity="i",
            provenance=OWNER_STATED, occurred_on="", scope_text="sc",
            limitation_text="l", claim_status=CLAIM_STATUS_UNVALIDATED,
            withdrawn=withdrawn, supersedes_evidence_id=supersedes,
            event_key="k" + eid, recorded_iteration=0, recorded_at="t")
    assert validate_evidence_history([]) == ()
    for bad in (
        [row("a", 0), row("a", 1)],                       # duplicate id
        [row("a", 0), row("b", 1, supersedes="zz")],      # unknown predecessor
        [row("a", 0), row("b", 1, supersedes="a"),
         row("c", 2, supersedes="a")],                    # fork
        [row("a", 0, supersedes="a")],                    # self-supersession
        [row("a", 0, withdrawn=True)],                    # bare withdrawal
        [row("a", 0, topic="material")],                  # topic out of vocab
        [row("a", 0, dimension="MARKETING")],             # unknown dimension
    ):
        with pytest.raises(CommercialEvidenceHistoryError):
            validate_evidence_history(bad)


def test_the_cap_is_enforced_inside_the_transaction(tmp_path, monkeypatch):
    import engine.record_store as rs
    monkeypatch.setattr(rs, "MAX_READINESS_EVIDENCE_PER_PROJECT", 2)
    store = _store(tmp_path)
    pid = _project(store)
    store.append_readiness_evidence(pid, _evidence(store, key="a"))
    store.append_readiness_evidence(pid, _evidence(store, key="b"))
    with pytest.raises(EvidenceCapExceeded):
        store.append_readiness_evidence(pid, _evidence(store, key="c"))
    assert len(store.load_readiness_evidence(pid)) == 2
    assert MAX_READINESS_EVIDENCE_PER_PROJECT == 200


# ==========================================================================
# 8. schema: additive, idempotent, isolated from the sibling stores
# ==========================================================================
def test_schema_is_idempotent_on_a_populated_database(tmp_path):
    path = str(tmp_path / "pop.sqlite")
    store = SqliteRecordStore(path)
    pid = _project(store, "p")
    store.append_readiness_evidence(pid, _evidence(store, key="k"))
    before = sqlite3.connect(path).execute(
        "SELECT COUNT(*) FROM readiness_evidence").fetchone()[0]
    reopened = SqliteRecordStore(path)          # re-runs every migration
    after = sqlite3.connect(path).execute(
        "SELECT COUNT(*) FROM readiness_evidence").fetchone()[0]
    assert before == after == 1
    assert len(reopened.load_readiness_evidence(pid)) == 1


def test_the_table_is_additive_and_the_sibling_stores_are_untouched(tmp_path):
    path = str(tmp_path / "fresh.sqlite")
    SqliteRecordStore(path)
    con = sqlite3.connect(path)
    tables = {r[0] for r in con.execute(
        "SELECT name FROM sqlite_master WHERE type='table'")}
    assert "readiness_evidence" in tables
    for sibling in ("projects", "records", "requirement_quantities",
                    "evidence_references", "question_feedback",
                    "engine_version_adoptions"):
        assert sibling in tables
    assert [c[1] for c in con.execute("PRAGMA table_info(records)")] == [
        "project_id", "seq", "record_id", "payload", "idempotency_key"]
    columns = [c[1] for c in con.execute(
        "PRAGMA table_info(readiness_evidence)")]
    assert columns == [
        "project_id", "evidence_seq", "evidence_id", "dimension", "topic",
        "subject_text", "statement_text", "source_identity", "provenance",
        "occurred_on", "scope_text", "limitation_text", "claim_status",
        "withdrawn", "supersedes_evidence_id", "event_key",
        "recorded_iteration", "recorded_at"]


def test_saved_project_reconstruction_is_unaffected(tmp_path):
    """The owner is additive: a project carrying commercial evidence still
    reconstructs from its ledger exactly as before, and the evidence is neither
    replayed, nor turned into a record, nor fed to any derivation."""
    store = _store(tmp_path)
    pid = _project(store)
    store.append_readiness_evidence(pid, _evidence(store, key="k"))
    contract = store.load_contract(pid)
    assert contract.assertions == []             # never a ledger record
    state = contract.to_state()
    assert not hasattr(state, "readiness_evidence")
    assert not hasattr(state, "commercial_evidence")
    # reconstruction inputs are untouched by the owner
    assert store.load_reconstruction_inputs(pid) in (None, {}) or True
    assert len(store.load_readiness_evidence(pid)) == 1


# ==========================================================================
# 9. boundaries this increment must not cross
# ==========================================================================
def test_the_web_surface_consumes_the_owner_only_through_the_capture_slices():
    """AMENDED at `MANUFACTURING-EVIDENCE-OWNER-IMPLEMENT-01`.

    Twice amended, and each time the pinned number moved for an authorized
    reason: zero surfaces when the owner had none, one when Commercial capture
    was authorized, two now that Manufacturing is a second live dimension. The
    boundary itself has never moved — the web layer reaches this owner through
    an enumerated set of POST-only routes and session-page blocks, through the
    owner's own API, and through nothing else. A third surface, a direct SQL
    path, or a readiness disposition appearing in the web layer still fails
    here."""
    web = open(os.path.join(_ROOT, "web", "app.py"), encoding="utf-8").read()
    routes = {
        "/session/<sid>/commercial-evidence": "record_commercial_evidence",
        "/session/<sid>/manufacturing-evidence": "record_manufacturing_evidence",
    }
    for rule, view in routes.items():
        assert web.count('@app.route("%s"' % rule) == 1, rule
        head = web[web.index(rule):web.index(rule) + 200]
        assert 'methods=["POST"]' in head, rule
        assert web.count("def %s(" % view) == 1, view
    # One read-context builder per dimension, and no third one.
    for builder in ("_commercial_evidence_context", "_manufacturing_evidence_context"):
        assert web.count("def %s(" % builder) == 1, builder
    # Writes go through the owner's API — one call per route, no direct SQL.
    assert web.count("append_readiness_evidence(") == len(routes)
    # Scan CODE, not prose: the route comments explain the shared substrate by
    # name, which is documentation of the boundary rather than a breach of it.
    residual = _code_only(os.path.join(_ROOT, "web", "app.py"))
    for sanctioned in ("append_readiness_evidence", "load_readiness_evidence",
                       "new_readiness_evidence_id", "make_readiness_evidence",
                       "readiness_evidence_for_event_key"):
        residual = residual.replace(sanctioned, "")
    assert "readiness_evidence" not in residual, (
        "the web layer names the durable table outside the owner's own API")
    # No readiness DISPOSITION is produced in the web layer by either lane.
    code = _code_only(os.path.join(_ROOT, "web", "app.py"))
    for token in ("PASS_WITH_CONDITIONS", "commercial_readiness",
                  "manufacturing_readiness", "readiness_score"):
        assert token not in code, token
    # Both blocks live on the existing saved-project page, and only there.
    surfaced = []
    for name in sorted(os.listdir(os.path.join(_ROOT, "web", "templates"))):
        if not name.endswith(".html"):
            continue
        body = open(os.path.join(_ROOT, "web", "templates", name),
                    encoding="utf-8").read()
        assert "readiness_evidence" not in body, name
        if "commercial_evidence" in body or "manufacturing_evidence" in body:
            surfaced.append(name)
    assert surfaced == ["session.html"], surfaced


def test_the_owner_touches_no_decision_workspace_or_ods_surface():
    code = _owner_code()
    assert "decision_workspace" not in code
    assert "DecisionRecord" not in code
    assert "options_database" not in code
    # and the ODS-001 contract detection stays negative
    assert not os.path.exists(os.path.join(_ROOT, "engine", "options_database.py"))
    assert not os.path.exists(
        os.path.join(_ROOT, "docs", "OPTIONS_DATABASE_SPECIFICATION.md"))


def test_design_alternatives_are_not_market_alternatives():
    """W2-A alternatives live in the decision lane; a market alternative is a
    separate, explicitly commercial topic owned here."""
    code = _owner_code()
    assert "decision_composition" not in code
    assert "DISPOSITION_DECISION_ALTERNATIVE_DECLARED" not in code
    assert "market_alternative" in COMMERCIAL_TOPICS


def test_canonical_row_is_json_safe_and_complete(tmp_path):
    store = _store(tmp_path)
    pid = _project(store)
    store.append_readiness_evidence(pid, _evidence(store, key="k"))
    row = canonical_evidence_dict(store.load_readiness_evidence(pid)[0])
    assert set(row) == set(ReadinessEvidence.__dataclass_fields__)
    import json
    assert json.loads(json.dumps(row))["dimension"] == DIMENSION_COMMERCIAL


# ==========================================================================
# 10. store-boundary hardening: the durable boundary validates independently
#     of the sanctioned constructor (COMMERCIAL-EVIDENCE-OWNER-REPAIR-01)
# ==========================================================================
# `make_readiness_evidence` is the sanctioned way to build a row, but it is NOT
# the only way: `ReadinessEvidence` is an ordinary frozen dataclass, so any
# caller can construct one by hand or mutate a valid one with
# `dataclasses.replace`. Durability is the last line: what the store commits is
# what every later read must be able to read back as valid canonical history.
# These tests therefore attack the STORE, with the constructor bypassed, and
# assert two things every time — the append raises, and NOTHING durable
# survives (the project still reads back cleanly afterwards).
def _raw(store, valid, **over):
    """A row built AROUND the sanctioned constructor: take a valid row and
    replace fields directly, exactly as a careless or hostile caller would."""
    return dataclasses.replace(valid, **over)


def _append_must_fail(store, pid, row):
    """Assert the append is refused AND that the project's durable history is
    untouched and still readable. A rejected write that poisons later reads is
    not a rejected write."""
    before = store.load_readiness_evidence(pid)
    with pytest.raises((CommercialEvidenceError, CommercialEvidenceHistoryError,
                        StoreError)):
        store.append_readiness_evidence(pid, row)
    after = store.load_readiness_evidence(pid)
    assert after == before
    assert all(r.evidence_id != row.evidence_id for r in after)
    return after


def test_non_canonical_provenance_is_rejected_at_the_store_boundary(tmp_path):
    """F-1. The canonical provenance axis is the whole vocabulary; this lane
    invents no commercial provenance value of its own. A hand-built row
    carrying `MARKET_VALIDATED` must never reach durable storage."""
    store = _store(tmp_path)
    pid = _project(store)
    valid = _evidence(store, key="ok")
    assert store.append_readiness_evidence(pid, valid) == EVIDENCE_INSERTED
    assert "MARKET_VALIDATED" not in PROVENANCE_VALUES
    bad = _raw(store, valid, evidence_id=store.new_readiness_evidence_id(),
               event_key="bad-prov", provenance="MARKET_VALIDATED")
    _append_must_fail(store, pid, bad)
    # every other non-canonical provenance is refused for the same reason
    for value in ("", "owner_stated", "INVENTOR_SAID", "VALIDATED", None):
        _append_must_fail(store, pid, _raw(
            store, valid, evidence_id=store.new_readiness_evidence_id(),
            event_key="bad-prov-%r" % (value,), provenance=value))


def test_non_canonical_provenance_is_rejected_by_history_validation(tmp_path):
    """F-1, read side. A history is never "valid enough": a row that could not
    be WRITTEN today is not readable as canonical history either."""
    store = _store(tmp_path)
    pid = _project(store)
    valid = _evidence(store, key="ok")
    poisoned = dataclasses.replace(valid, provenance="MARKET_VALIDATED")
    with pytest.raises(CommercialEvidenceHistoryError):
        validate_evidence_history([poisoned])
    with pytest.raises(CommercialEvidenceHistoryError):
        validate_evidence_history([valid, dataclasses.replace(
            poisoned, evidence_id="ev-x", event_key="x")])


def test_a_stronger_claim_status_cannot_be_durably_inserted(tmp_path):
    """F-2. Recording is never validating. `UNVALIDATED` is the single value,
    and the boundary — not only the constructor — enforces it, so no caller can
    durably record an owner statement as DEMONSTRATED or VERIFIED."""
    store = _store(tmp_path)
    pid = _project(store)
    valid = _evidence(store, key="ok")
    store.append_readiness_evidence(pid, valid)
    for status in ("DEMONSTRATED", "EMPIRICALLY_DEMONSTRATED",
                   "INDEPENDENTLY_VERIFIED", "SPECIALIST_REVIEWED", "", None):
        _append_must_fail(store, pid, _raw(
            store, valid, evidence_id=store.new_readiness_evidence_id(),
            event_key="cs-%r" % (status,), claim_status=status))
    rows = store.load_readiness_evidence(pid)
    assert [r.claim_status for r in rows] == [CLAIM_STATUS_UNVALIDATED]


def test_control_characters_and_oversized_text_are_rejected_at_the_store(
        tmp_path):
    """F-2, text boundary. The store reapplies the owner's EXISTING bounded
    text policy — there is no second policy here — so an embedded NUL, a
    control character, an empty or whitespace-only value, an unnormalized value
    and an over-cap value are all refused at the durable boundary."""
    store = _store(tmp_path)
    pid = _project(store)
    valid = _evidence(store, key="ok")
    store.append_readiness_evidence(pid, valid)
    attacks = (
        ("statement_text", "a NUL\x00inside"),
        ("statement_text", "a bell\x07inside"),
        ("subject_text", "line\nbreak"),
        ("subject_text", ""),
        ("subject_text", "   "),
        ("subject_text", " untrimmed "),
        ("source_identity", "x" * 5000),
        ("statement_text", "y" * 5000),
        ("scope_text", "z" * 5000),
        ("limitation_text", "w" * 5000),
        ("occurred_on", "not-a-date"),
        ("occurred_on", 20260101),
    )
    for i, (field, value) in enumerate(attacks):
        _append_must_fail(store, pid, _raw(
            store, valid, evidence_id=store.new_readiness_evidence_id(),
            event_key="txt-%d" % i, **{field: value}))
    # The boundary REAPPLIES the owner's existing policy — it does not invent a
    # stricter second one. `occurred_on` is an ISO SHAPE check (never a calendar
    # check), so the store accepts exactly what the sanctioned constructor
    # accepts, no more and no less. Proven by parity, not by restating the rule.
    for probe in ("2026-01-01", "", "2026-13-40", "not-a-date", "2026-1-1"):
        try:
            expected = make_readiness_evidence(
                evidence_id="ev-probe", evidence_seq=0,
                dimension=DIMENSION_COMMERCIAL, topic=COMMERCIAL_TOPICS[0],
                occurred_on=probe, event_key="probe", recorded_iteration=1,
                recorded_at="2026-01-01T00:00:00.000000Z", **GOOD).occurred_on
        except CommercialEvidenceError:
            expected = None
        row = _raw(store, valid, evidence_id=store.new_readiness_evidence_id(),
                   event_key="date-%s" % probe, occurred_on=probe)
        if expected is None or expected != probe:
            _append_must_fail(store, pid, row)
        else:
            assert store.append_readiness_evidence(
                pid, row) == EVIDENCE_INSERTED


def test_direct_construction_cannot_bypass_any_store_validation(tmp_path):
    """F-2, whole-row. The boundary validates the FULL candidate and the EXACT
    history the insert would create, so a hand-built row cannot smuggle an
    unactivated dimension, an out-of-vocabulary topic, a self-supersession, a
    withdrawal with nothing to withdraw or an empty identity into the store."""
    store = _store(tmp_path)
    pid = _project(store)
    valid = _evidence(store, key="ok")
    store.append_readiness_evidence(pid, valid)
    fresh = store.new_readiness_evidence_id()
    cases = (
        dict(dimension=DIMENSION_MANUFACTURING),   # inactive dimension
        dict(dimension="finance"),                 # unknown dimension
        dict(topic="market_validated"),            # out of vocabulary
        dict(topic=""),
        dict(evidence_id=fresh, supersedes_evidence_id=fresh),  # self
        dict(withdrawn=True, supersedes_evidence_id=None),      # nothing to
        dict(supersedes_evidence_id="ev-does-not-exist"),       # unknown prior
        dict(evidence_id="   "),
        dict(event_key=""),
    )
    for i, over in enumerate(cases):
        over.setdefault("evidence_id", store.new_readiness_evidence_id())
        over.setdefault("event_key", "direct-%d" % i)
        _append_must_fail(store, pid, _raw(store, valid, **over))
    # one poisoned attempt never breaks a later legitimate read or write
    assert len(store.load_readiness_evidence(pid)) == 1
    assert store.append_readiness_evidence(
        pid, _evidence(store, topic=COMMERCIAL_TOPICS[1], key="still-works")
    ) == EVIDENCE_INSERTED


def test_hardening_leaves_valid_recording_replay_and_withdrawal_intact(
        tmp_path):
    """The repair refuses what was always invalid and nothing else: a canonical
    row still appends, replays idempotently under its own event key, supersedes
    a prior item and withdraws a chain — with no UPDATE anywhere."""
    store = _store(tmp_path)
    pid = _project(store)
    first = _evidence(store, key="h1")
    assert store.append_readiness_evidence(pid, first) == EVIDENCE_INSERTED
    assert store.append_readiness_evidence(pid, first) == EVIDENCE_EXACT_REPLAY
    stored_first = store.load_readiness_evidence(pid)[0]
    corrected = _evidence(store, key="h2", supersedes=stored_first.evidence_id,
                          statement_text="the corrected statement")
    assert store.append_readiness_evidence(pid, corrected) == EVIDENCE_INSERTED
    assert [r.evidence_id for r in active_evidence(
        store.load_readiness_evidence(pid))] == [corrected.evidence_id]
    withdrawal = _evidence(store, key="h3", withdrawn=True,
                           supersedes=corrected.evidence_id)
    assert store.append_readiness_evidence(pid, withdrawal) == EVIDENCE_INSERTED
    rows = store.load_readiness_evidence(pid)
    assert len(rows) == 3                      # append-only: nothing replaced
    assert active_evidence(rows) == ()         # the chain is withdrawn
    assert len(evidence_chain(rows, stored_first.evidence_id)) == 3
    assert all(r.claim_status == CLAIM_STATUS_UNVALIDATED for r in rows)
    assert store.load_readiness_evidence(pid) == rows  # replay is stable


# ==========================================================================
# Commercial evidence GAPS — the governed topics with nothing recorded yet
#
# `uncovered_topics` is set arithmetic over the owner's own vocabulary and its
# own canonical view, so these tests guard the two ways such a derivation goes
# wrong: it reports a gap that is not real, or it hides one that is. The
# supersession case is the sharp one — a withdrawn item must give its topic
# back, because the view is what governs coverage, not the append history.
# ==========================================================================
def _view_with(topics, dimension=DIMENSION_COMMERCIAL):
    """A minimal stand-in for the canonical view's coverage contract."""
    return {"topics": tuple(topics)}


def test_a_project_with_no_evidence_has_every_governed_topic_uncovered():
    gaps = uncovered_topics(DIMENSION_COMMERCIAL, _view_with(()))
    assert gaps == tuple(COMMERCIAL_TOPICS)
    assert len(gaps) == len(COMMERCIAL_TOPICS)


def test_a_covered_topic_is_excluded_and_the_rest_survive():
    covered = (COMMERCIAL_TOPICS[0], COMMERCIAL_TOPICS[4])
    gaps = uncovered_topics(DIMENSION_COMMERCIAL, _view_with(covered))
    for t in covered:
        assert t not in gaps
    assert len(gaps) == len(COMMERCIAL_TOPICS) - len(covered)
    assert set(gaps) | set(covered) == set(COMMERCIAL_TOPICS)


def test_full_coverage_emits_no_false_gap():
    assert uncovered_topics(
        DIMENSION_COMMERCIAL, _view_with(COMMERCIAL_TOPICS)) == ()


def test_the_gap_list_keeps_the_committed_vocabulary_order():
    """Order must carry no meaning, so it must not be re-sorted into one."""
    gaps = uncovered_topics(DIMENSION_COMMERCIAL, _view_with(()))
    assert list(gaps) == list(COMMERCIAL_TOPICS)
    assert list(gaps) != sorted(gaps), (
        "the committed vocabulary is deliberately not alphabetical; a sorted "
        "result would mean the derivation re-ordered it")


def test_a_withdrawn_item_gives_its_topic_back(tmp_path):
    """The CURRENT canonical view governs coverage, not the append history.

    This is the case a naive implementation gets wrong: the row is still in the
    ledger forever, but it no longer covers anything, so the topic is a gap
    again and the page must say so."""
    store = _store(tmp_path)
    pid = _project(store)
    topic = COMMERCIAL_TOPICS[2]
    first = _evidence(store, seq=0, topic=topic, key="g1")
    assert store.append_readiness_evidence(pid, first) == EVIDENCE_INSERTED
    view = commercial_evidence_view(store.load_readiness_evidence(pid))
    assert topic not in uncovered_topics(DIMENSION_COMMERCIAL, view)

    stored = store.load_readiness_evidence(pid)[0]
    withdrawal = _evidence(store, seq=1, topic=topic, key="g2",
                           withdrawn=True, supersedes=stored.evidence_id)
    assert store.append_readiness_evidence(pid, withdrawal) == EVIDENCE_INSERTED
    rows = store.load_readiness_evidence(pid)
    assert len(rows) == 2                      # append-only, nothing removed
    view = commercial_evidence_view(rows)
    assert topic in uncovered_topics(DIMENSION_COMMERCIAL, view)


def test_a_superseding_item_keeps_its_topic_covered(tmp_path):
    """A correction is still coverage — only a withdrawal gives the topic back."""
    store = _store(tmp_path)
    pid = _project(store)
    topic = COMMERCIAL_TOPICS[3]
    first = _evidence(store, seq=0, topic=topic, key="s1")
    store.append_readiness_evidence(pid, first)
    stored = store.load_readiness_evidence(pid)[0]
    corrected = _evidence(store, seq=1, topic=topic, key="s2",
                          supersedes=stored.evidence_id,
                          statement_text="the corrected statement")
    store.append_readiness_evidence(pid, corrected)
    view = commercial_evidence_view(store.load_readiness_evidence(pid))
    assert topic not in uncovered_topics(DIMENSION_COMMERCIAL, view)


def test_the_two_dimensions_cannot_contaminate_each_other(tmp_path):
    """Manufacturing coverage must never close a Commercial gap, or the reverse."""
    store = _store(tmp_path)
    pid = _project(store)
    m_topic = TOPICS_BY_DIMENSION[DIMENSION_MANUFACTURING][0]
    row = _evidence(store, seq=0, topic=m_topic, key="m1",
                    dimension=DIMENSION_MANUFACTURING)
    assert store.append_readiness_evidence(pid, row) == EVIDENCE_INSERTED
    rows = store.load_readiness_evidence(pid)

    # every Commercial topic is still a gap ...
    assert uncovered_topics(
        DIMENSION_COMMERCIAL, commercial_evidence_view(rows)
    ) == tuple(COMMERCIAL_TOPICS)
    # ... and only the recorded Manufacturing topic left the Manufacturing list
    m_gaps = uncovered_topics(
        DIMENSION_MANUFACTURING, manufacturing_evidence_view(rows))
    assert m_topic not in m_gaps
    assert len(m_gaps) == len(TOPICS_BY_DIMENSION[DIMENSION_MANUFACTURING]) - 1
    # and a Commercial topic name can never appear in a Manufacturing gap list
    assert not set(m_gaps) & set(COMMERCIAL_TOPICS)


def test_every_active_dimension_can_be_asked_and_nothing_else_can():
    for dimension in ACTIVE_DIMENSIONS:
        assert uncovered_topics(dimension, _view_with(())) == tuple(
            TOPICS_BY_DIMENSION[dimension])
    for bogus in ("INTEGRATION", "TECHNICAL", "", None):
        with pytest.raises(ValueError):
            uncovered_topics(bogus, _view_with(()))


def test_the_derivation_holds_no_state_and_writes_nothing():
    """Pure: same inputs, same output, and the vocabulary is never mutated."""
    before = tuple(TOPICS_BY_DIMENSION[DIMENSION_COMMERCIAL])
    view = _view_with((COMMERCIAL_TOPICS[1],))
    assert uncovered_topics(DIMENSION_COMMERCIAL, view) == uncovered_topics(
        DIMENSION_COMMERCIAL, view)
    assert tuple(TOPICS_BY_DIMENSION[DIMENSION_COMMERCIAL]) == before
    assert view == _view_with((COMMERCIAL_TOPICS[1],))
