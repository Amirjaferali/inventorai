"""
InventorAI Web Interface (Phase H-A)
Thin web shell only. Engine called as library.
SESSION_STORE: in-memory, non-production, temporary.
"""
import uuid
from flask import Flask, request, redirect, url_for, render_template
from engine.domain_rules import infer_domain
from engine.idea_state import IdeaState, SuccessCriterion
from engine.progression_loop import (
    run_iteration, select_next_gap, get_question, get_display_question,
)
from web.gap_labels import GAP_LABELS, get_gap_label, get_maturity_label, SESSION_DISCLOSURE
from engine.deliverable_assembler import assemble_deliverable
from web.responsibility_labels import get_responsibility  # Increment 1B: advisory only
from web.clarification_labels import get_clarification  # Increment 1B: display-only clarification

app = Flask(__name__)
app.secret_key = "inventorai-dev-only"
SESSION_STORE = {}

# --- Increment 1A: structured owner actions (conformance correction) ---------
# Non-specialist owners respond through explicit, structured actions instead of
# being forced to invent technical prose. ONLY `answered` enters the existing
# assessment path (run_iteration -> assess/integrate/transition); its behavior
# and the ILT-002 transcript record are unchanged. The five non-answer actions
# still never assess, score, close or alter a gap, advance maturity, satisfy a
# transition gate, or create an evidence record, and the SESSION_STORE entry
# keeps its additive in-memory display metadata.
#
# --- Increment 2: durable, truthful disposition records -----------------------
# In addition (Increment 2 truthful-state correction), every owner action now
# also appends a durable in-memory record to the IdeaState interaction ledger
# (state.record_interaction). This ledger is NOT progression state: it does not
# assess, score, advance maturity, alter the gap lifecycle, satisfy a gate, or
# create Evidence; it carries the truthful provenance/validation/disposition of
# what the owner did. It remains persistence-independent — no durable persistence
# is used, the transcript schema is untouched, and the frozen engine.session_store
# is never imported.
ACTION_ANSWERED = "answered"
INTERACTION_ACTIONS = {
    ACTION_ANSWERED,
    "unknown",
    "deferred",
    "provisional_assumption",
    "specialist_requested",
    "evidence_requested",
}
# Honest, non-progress acknowledgements for the five non-answer actions. None of
# these implies the question is resolved, verified, or answered.
_NON_ANSWER_ACK = {
    "unknown": "Recorded that you do not know this yet. It is kept as an open unknown and does not resolve the question.",
    "deferred": "Recorded as deferred. The question remains open and unresolved.",
    "provisional_assumption": "Recorded as a provisional assumption (not verified). It does not resolve the question or count as evidence.",
    "specialist_requested": "Recorded that specialist input is needed. No technical answer has been assumed.",
    "evidence_requested": "Recorded that evidence is needed. No evidence or result has been recorded.",
}

# Option B product-boundary enforcement (DOMAIN_SCOPE_OWNER_RESOLUTION_OPTION_B).
# Current generic product-runtime activation is limited to electronics/electrical.
# Stable, exact refusal message — does not expose the internally inferred domain.
UNSUPPORTED_DOMAIN_MESSAGE = (
    "InventorAI currently supports electronics and electrical ideas only. "
    "Please describe an electronics or electrical invention."
)

# Explicit electronics/electrical confirmation at the generic product boundary
# (ADR-001: "Domain assignment is explicit or it does not occur"). The user must
# affirmatively declare the supported domain; consent is never inferred from the
# idea text. The checkbox submits this exact value.
DOMAIN_CONFIRM_VALUE = "electronics_electrical"
CONFIRMATION_REQUIRED_MESSAGE = (
    "Please confirm that your idea is an electronics or electrical idea "
    "before starting."
)
# Bounded conflict check: explicit confirmation is the primary declaration, but
# a clearly different *supported* internal classification is not silently
# relabeled as electronics. These are refused; no session is created.
CONFLICTING_SUPPORTED_DOMAINS = {"mechanical", "medical_device", "software"}

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start():
    idea_text = request.form.get("idea", "").strip()
    if not idea_text:
        return redirect(url_for("index"))
    # Explicit electronics/electrical confirmation is required (ADR-001 explicit
    # assignment). Consent is never inferred from the idea text; without it no
    # session is created.
    if request.form.get("domain_confirm") != DOMAIN_CONFIRM_VALUE:
        return render_template("index.html", error=CONFIRMATION_REQUIRED_MESSAGE)
    # Bounded conflict check using the unchanged deterministic classifier: the
    # explicit confirmation is the primary domain declaration, but it must not
    # silently override clear conflicting classification evidence.
    # infer_domain(), the registry loader, and all domain packs are unchanged.
    domain = infer_domain(idea_text)
    if domain in CONFLICTING_SUPPORTED_DOMAINS:
        # A clearly different *supported* domain — refuse, do not relabel.
        return render_template("index.html", error=UNSUPPORTED_DOMAIN_MESSAGE)
    if domain not in ("electronics_electrical", None):
        # Unexpected / unknown classifier value — refuse defensively.
        return render_template("index.html", error=UNSUPPORTED_DOMAIN_MESSAGE)
    # electronics_electrical or None is admitted under explicit confirmation
    # (None covers functional electronics ideas the signal classifier misses).
    # Admit: the session's domain is the explicitly confirmed supported domain.
    state = IdeaState(idea_id=str(uuid.uuid4()))
    state.domain = DOMAIN_CONFIRM_VALUE
    state.domain_signal = DOMAIN_CONFIRM_VALUE
    # Increment 1 (Owner-Expert Question Boundary): the general /start flow is the
    # non-specialist owner flow and must use the committed Path N non-specialist-safe
    # question provider (NON_SPECIALIST_QUESTIONING_POLICY). This is the same
    # provider already used by the governed _path_n route; no new question bank,
    # mode selector, role, or engine-state field is introduced. The named ILT
    # routes below are deliberately left on their existing default behavior.
    state.path = "N"
    sid = str(uuid.uuid4())
    initial_result = run_iteration(state, idea_text)
    SESSION_STORE[sid] = {"state": state, "last_result": initial_result, "transcript": []}
    return redirect(url_for("show_session", sid=sid))

@app.route("/start_ilt002_water_leak", methods=["POST"])
def start_ilt002_water_leak():
    idea_text = request.form.get("idea", "").strip()
    if not idea_text:
        return redirect(url_for("index"))
    state = IdeaState(idea_id=str(uuid.uuid4()))
    state.domain = "electronics_electrical"
    state.domain_signal = "electronics_electrical"
    sid = str(uuid.uuid4())
    initial_result = run_iteration(state, idea_text)
    SESSION_STORE[sid] = {"state": state, "last_result": initial_result, "transcript": []}
    return redirect(url_for("show_session", sid=sid))

@app.route("/start_ilt002_combination_lock", methods=["POST"])
def start_ilt002_combination_lock():
    idea_text = request.form.get("idea", "").strip()
    if not idea_text:
        return redirect(url_for("index"))
    state = IdeaState(idea_id=str(uuid.uuid4()))
    state.domain = "electronics_electrical"
    state.domain_signal = "electronics_electrical"
    sid = str(uuid.uuid4())
    initial_result = run_iteration(state, idea_text)
    SESSION_STORE[sid] = {"state": state, "last_result": initial_result, "transcript": []}
    return redirect(url_for("show_session", sid=sid))

@app.route("/start_ilt002_combination_lock_path_n", methods=["POST"])
def start_ilt002_combination_lock_path_n():
    idea_text = request.form.get("idea", "").strip()
    if not idea_text:
        return redirect(url_for("index"))
    state = IdeaState(idea_id=str(uuid.uuid4()))
    state.domain = "electronics_electrical"
    state.domain_signal = "electronics_electrical"
    state.path = "N"
    sid = str(uuid.uuid4())
    initial_result = run_iteration(state, idea_text)
    SESSION_STORE[sid] = {"state": state, "last_result": initial_result, "transcript": []}
    return redirect(url_for("show_session", sid=sid))

@app.route("/session/<sid>", methods=["GET"])
def show_session(sid):
    entry = SESSION_STORE.get(sid)
    if not entry:
        return redirect(url_for("index"))
    state = entry["state"]
    last_result = entry.get("last_result")
    INTAKE_QUESTION = "Describe your invention in more detail — what specific problem does it solve, and how does it solve it?"

    gap_type = select_next_gap(state)
    question = None
    if gap_type:
        gap = state.get_gap(gap_type)
        iterations_open = gap.iterations_open if gap else 0
        # Increment 1 (Owner-Expert Question Boundary): render via the display
        # selector so an exhausted non-specialist Path N gap shows the
        # deterministic plain-language reframe instead of repeating the final
        # question verbatim. Pure selection — no engine/state/maturity effect.
        question = get_display_question(state.domain, gap_type, iterations_open,
                                        path=state.path)
    elif (
        state.maturity_level == 0
        and len(state.gaps) == 0
        and last_result is not None
        and last_result.get("transition") == "WARN"
        and "not yet established" in (last_result.get("reason") or "")
    ):
        question = INTAKE_QUESTION
    open_gaps = state.get_open_gaps()
    closed_gaps = [g for g in state.gaps if g.status == "CLOSED"]
    gap_labels = {g.gap_type: GAP_LABELS.get(g.gap_type, GAP_LABELS["__default__"]) for g in state.gaps}
    current_gap_label = GAP_LABELS.get(gap_type, GAP_LABELS["__default__"]) if gap_type else None
    # Transcript capture: store question before render so POST can record it.
    # No engine effect. Evidence preservation only.
    if entry is not None and question is not None:
        entry["last_question"] = question
    return render_template("session.html",
        sid=sid,
        state=state,
        question=question,
        open_gaps=open_gaps,
        gap_type=gap_type,
        last_result=last_result,
        gap_labels=gap_labels,
        current_gap_label=current_gap_label,
        maturity_label=get_maturity_label(state.maturity_level),
        session_disclosure=SESSION_DISCLOSURE,
        closed_gaps=closed_gaps,
        interaction_ack=entry.pop("_interaction_ack", None) if entry else None,
        # Increment 1B: advisory, derived, read-only responsibility guidance for
        # the current gap. Computed at render time; never stored, never affects
        # gates/scoring/maturity/closure/transcript/IdeaState. None when no gap.
        current_responsibility=get_responsibility(gap_type) if gap_type else None,
        # Increment 1B clarification display: deterministic, owner-invoked,
        # display-only guidance explaining the current question. Derived from the
        # same gap_type at render time; never stored, never affects
        # gates/scoring/maturity/closure/transcript/IdeaState/persistence; adds no
        # owner action and no POST handling. None when no gap (intake path).
        current_clarification=get_clarification(gap_type) if gap_type else None,
    )
@app.route("/session/<sid>/deliverable", methods=["GET"])
def show_deliverable(sid):
    entry = SESSION_STORE.get(sid)
    if not entry:
        return redirect(url_for("index"))
    state = entry["state"]
    package = assemble_deliverable(state)
    eligible = package["_session_meta"]["deliverable_eligible"]
    return render_template(
        "deliverable.html",
        sid=sid,
        package=package,
        eligible=eligible,
    )

# Per-experiment owner-defined success criteria (planning metadata only).
# Field name on the form is "criterion__<experiment_id>". A criterion is a
# user-defined target, never a test result; this route never runs progression,
# never calls submit_answer, and never writes the ILT-002 transcript.
MAX_CRITERION_LENGTH = 1000
_CRITERION_FIELD_PREFIX = "criterion__"


@app.route("/session/<sid>/success-criteria", methods=["GET"])
def success_criteria(sid):
    entry = SESSION_STORE.get(sid)
    if not entry:
        return redirect(url_for("index"))
    package = assemble_deliverable(entry["state"])
    plan = package["section_11_prototype_test_plan"]
    return render_template(
        "success_criteria.html",
        sid=sid,
        experiments=plan["items"],
        stale_notice=plan.get("stale_criteria_notice"),
        field_prefix=_CRITERION_FIELD_PREFIX,
        max_length=MAX_CRITERION_LENGTH,
    )


@app.route("/session/<sid>/success-criteria", methods=["POST"])
def save_success_criteria(sid):
    entry = SESSION_STORE.get(sid)
    if not entry:
        return redirect(url_for("index"))
    state = entry["state"]
    package = assemble_deliverable(state)
    plan = package["section_11_prototype_test_plan"]
    current_ids = {it["experiment_id"] for it in plan["items"]}

    # Collect submitted criteria, namespaced by experiment_id.
    submitted = {name[len(_CRITERION_FIELD_PREFIX):]: val
                 for name, val in request.form.items()
                 if name.startswith(_CRITERION_FIELD_PREFIX)}

    def _reject(message):
        return render_template(
            "success_criteria.html", sid=sid, experiments=plan["items"],
            stale_notice=plan.get("stale_criteria_notice"),
            field_prefix=_CRITERION_FIELD_PREFIX, max_length=MAX_CRITERION_LENGTH,
            error=message,
        ), 400

    # Validate before any write: reject unknown/stale ids and over-limit input.
    for eid in submitted:
        if eid not in current_ids:
            return _reject("A submitted experiment is not part of the current plan. "
                           "No changes were saved.")
    for eid, raw in submitted.items():
        if len(raw.strip()) > MAX_CRITERION_LENGTH:
            return _reject(f"A criterion exceeds the {MAX_CRITERION_LENGTH}-character "
                           "limit. No changes were saved.")

    # Apply: trim only; whitespace-only removes; idempotent upsert.
    if not isinstance(getattr(state, "success_criteria", None), dict):
        state.success_criteria = {}
    for eid, raw in submitted.items():
        text = raw.strip()
        if text:
            state.success_criteria[eid] = SuccessCriterion(criterion=text)
        else:
            state.success_criteria.pop(eid, None)
    return redirect(url_for("show_deliverable", sid=sid))


@app.route("/session/<sid>", methods=["POST"])
def submit_answer(sid):
    entry = SESSION_STORE.get(sid)
    if not entry:
        return redirect(url_for("index"))
    state = entry["state"]
    # Increment 1A: resolve the explicit structured action. Legacy-compatibility
    # rule (chosen, explicit): a submission with NO `action` field is treated as
    # `answered` — exactly the pre-1A behavior, where a non-empty `response` is
    # assessed and an empty one is a no-op. An explicit but UNRECOGNIZED action is
    # rejected with HTTP 400 (never silently assessed), so a malformed client can
    # not smuggle an unknown action into the assessment path.
    action = request.form.get("action", ACTION_ANSWERED).strip().lower()
    if action not in INTERACTION_ACTIONS:
        return ("Unrecognized session action. No change was made.", 400)
    response = request.form.get("response", "").strip()

    if action != ACTION_ANSWERED:
        # Non-answer action: record as additive in-memory metadata only. This
        # path NEVER calls run_iteration, never assesses/scores, never closes or
        # alters a gap, never advances maturity, never satisfies a gate, and never
        # creates an evidence record. select_next_gap() is a read-only selector
        # used only to label which question the action was taken against. Optional
        # owner text is retained verbatim as metadata, not as an assessed response
        # or evidence. The journey truthfully redisplays the same (still-open)
        # question with an honest acknowledgement rather than feigning progress.
        gap_ctx = select_next_gap(state)
        entry.setdefault("interaction_actions", []).append({
            "action": action,
            "iteration": state.iteration,
            "gap_type": gap_ctx,
            "text": response or None,
        })
        entry["_interaction_ack"] = _NON_ANSWER_ACK[action]
        # Increment 2: durable disposition record on the IdeaState ledger. This
        # adds NO epistemic movement (no assess/score/gap/maturity/transcript
        # change) — it only records, truthfully and durably, that the owner took
        # this non-answer action against the still-open question.
        state.record_interaction(
            action=action, content=response or "",
            gap_context=gap_ctx, iteration=state.iteration,
        )
        return redirect(url_for("show_session", sid=sid))

    # ANSWERED — unchanged existing assessment path and transcript record.
    if response:
        targeted_gap = select_next_gap(state)   # gap this answer addresses (pre-iteration)
        result = run_iteration(state, response)
        entry["last_result"] = result
        # Transcript capture: append verbatim record for ILT-002 evidence.
        # iteration number read after run_iteration() incremented it.
        # No engine effect. Evidence preservation only.
        import json, os
        from datetime import datetime
        record = {
            "session_id": sid,
            "iteration": state.iteration,
            "question":  entry.get("last_question", ""),
            "response":  response,
            "domain":    getattr(state, "domain", None),
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
        entry["transcript"].append(record)
        # Disk-backed persistence: survives Flask restarts.
        # ILT-002 evidence preservation only. No engine effect.
        transcript_path = f"/tmp/ilt002_transcript_{sid}.jsonl"
        with open(transcript_path, "a") as _tf:
            _tf.write(json.dumps(record) + "\n")
        # Increment 2: durable answered record on the IdeaState ledger.
        # OWNER_STATED provenance (the owner authored it), UNVALIDATED status
        # (never auto-verified by the act of answering), carrying the current
        # leading evidence quality where available. Additive only: the existing
        # assessment path, transcript, and gap lifecycle above are unchanged.
        state.record_interaction(
            action=ACTION_ANSWERED, content=response,
            gap_context=targeted_gap, iteration=state.iteration,
            quality=getattr(getattr(state, "known_mechanism", None), "quality", None)
                    or getattr(getattr(state, "known_problem", None), "quality", None),
        )
        import sys
        for g in state.gaps:
                    pass
    return redirect(url_for("show_session", sid=sid))


# ---------------------------------------------------------------------------
# FDC-001 first increment — Technical Decision Workspace.
# In-memory only. Distinct from SESSION_STORE; imports no session_store; writes
# no durable state; performs no benchmark run. Activation-only lane surface.
# ---------------------------------------------------------------------------
from engine import decision_workspace as fdc001_dw

# Dedicated in-memory store for FDC-001 decision records (non-durable).
FDC001_DECISIONS = {}


@app.route("/decision-workspace", methods=["GET"])
def decision_workspace_start():
    record = fdc001_dw.DecisionRecord()
    FDC001_DECISIONS[record.decision_id] = record
    return redirect(url_for("decision_workspace_view", did=record.decision_id))


def _render_decision_workspace(record, error=None, status=200):
    """Render the workspace, optionally with a bounded user-visible validation
    error. The error is a concise message only — never a traceback."""
    html = render_template(
        "decision_workspace.html",
        view=record.to_record_dict(),
        candidate_names=list(fdc001_dw.CANDIDATE_NAMES),
        limitations=list(fdc001_dw.EXPORT_LIMITATIONS),
        error=error,
    )
    return (html, status)


@app.route("/decision-workspace/<did>", methods=["GET"])
def decision_workspace_view(did):
    record = FDC001_DECISIONS.get(did)
    if record is None:
        return redirect(url_for("decision_workspace_start"))
    return _render_decision_workspace(record)


@app.route("/decision-workspace/<did>/input", methods=["POST"])
def decision_workspace_add_input(did):
    record = FDC001_DECISIONS.get(did)
    if record is None:
        return redirect(url_for("decision_workspace_start"))
    candidate_id = request.form.get("candidate_id", "").strip()
    candidate_ids = [candidate_id] if candidate_id else []
    try:
        record.add_input(
            request.form.get("text", "").strip(),
            request.form.get("claim_class", "").strip(),
            request.form.get("provenance", "").strip(),
            decision_relevant=request.form.get("decision_relevant") == "on",
            candidate_ids=candidate_ids,
        )
    except fdc001_dw.DecisionError as exc:
        # The record is left unmodified; show a concise bounded error.
        return _render_decision_workspace(
            record, error="Input rejected: %s" % exc, status=400)
    return redirect(url_for("decision_workspace_view", did=did))


@app.route("/decision-workspace/<did>/constraint", methods=["POST"])
def decision_workspace_add_constraint(did):
    record = FDC001_DECISIONS.get(did)
    if record is None:
        return redirect(url_for("decision_workspace_start"))
    candidate_id = request.form.get("candidate_id", "").strip()
    candidate_ids = [candidate_id] if candidate_id else []
    try:
        record.add_constraint(
            request.form.get("text", "").strip(),
            request.form.get("constraint_strength", "").strip(),
            request.form.get("provenance", "").strip(),
            confirmed=request.form.get("confirmed") == "on",
            candidate_ids=candidate_ids,
        )
    except fdc001_dw.DecisionError as exc:
        return _render_decision_workspace(
            record, error="Constraint rejected: %s" % exc, status=400)
    return redirect(url_for("decision_workspace_view", did=did))


@app.route("/decision-workspace/<did>/gap", methods=["POST"])
def decision_workspace_gap_action(did):
    record = FDC001_DECISIONS.get(did)
    if record is None:
        return redirect(url_for("decision_workspace_start"))
    action = request.form.get("action", "").strip()
    gap_id = request.form.get("gap_id", "").strip()
    try:
        if action in ("resolve", "reclassify"):
            # FDC-002 user-facing route guard (reconciled contract, spec §12.1 /
            # guarantee #31): the legacy bare-text resolve/reclassify route must
            # NOT clear or reclassify a physical/calibration blocker. Reject
            # BEFORE invoking the legacy domain mutation, so the rejection is
            # bounded (HTTP 400) and atomic — no gap, revision, history,
            # readiness, blocker, or change-impact mutation. The FDC-002
            # evidence-assessment workflow is the sole user-facing path for that
            # blocker. (gap_blocker_code is read-only and raises for unknown ids.)
            if (record.gap_blocker_code(gap_id)
                    == fdc001_dw.MISSING_PHYSICAL_OR_CALIBRATION_INFORMATION):
                return _render_decision_workspace(
                    record,
                    error=("Gap action rejected: the "
                           "missing_physical_or_calibration_information blocker "
                           "can be cleared only through the evidence-assessment "
                           "workflow (record evidence, then assess and decide), "
                           "not this route."),
                    status=400)
            if action == "resolve":
                record.resolve_gap(gap_id)
            else:
                record.reclassify_gap(
                    gap_id, request.form.get("rationale", "").strip())
        else:
            raise fdc001_dw.DecisionError("unknown gap action: %r" % action)
    except fdc001_dw.DecisionError as exc:
        return _render_decision_workspace(
            record, error="Gap action rejected: %s" % exc, status=400)
    return redirect(url_for("decision_workspace_view", did=did))


@app.route("/decision-workspace/<did>/evidence", methods=["POST"])
def decision_workspace_add_evidence(did):
    record = FDC001_DECISIONS.get(did)
    if record is None:
        return redirect(url_for("decision_workspace_start"))
    candidate_id = request.form.get("candidate_id", "").strip()
    candidate_ids = [candidate_id] if candidate_id else []
    try:
        # verification_status is NEVER read from the form: it is system-set to
        # `unverified` inside add_evidence (§7.4). Any posted value is ignored.
        record.add_evidence(
            request.form.get("gap_id", "").strip(),
            request.form.get("text", "").strip(),
            request.form.get("claim_class", "").strip(),
            request.form.get("provenance", "").strip(),
            method=request.form.get("method", "").strip() or None,
            source_label=request.form.get("source_label", "").strip() or None,
            evidence_version=request.form.get("evidence_version", "").strip() or None,
            limitations=request.form.get("limitations", "").strip() or None,
            candidate_ids=candidate_ids,
            decision_relevant=request.form.get("decision_relevant") == "on",
        )
    except fdc001_dw.DecisionError as exc:
        return _render_decision_workspace(
            record, error="Evidence rejected: %s" % exc, status=400)
    return redirect(url_for("decision_workspace_view", did=did))


@app.route("/decision-workspace/<did>/gap-assessment", methods=["POST"])
def decision_workspace_gap_assessment(did):
    record = FDC001_DECISIONS.get(did)
    if record is None:
        return redirect(url_for("decision_workspace_start"))
    evidence_ids = [e.strip() for e in request.form.getlist("evidence_ids")
                    if e.strip()]
    try:
        record.assess_gap(
            request.form.get("gap_id", "").strip(),
            evidence_ids,
            request.form.get("assessment", "").strip(),
            request.form.get("rationale", "").strip(),
            request.form.get("resolution_decision", "").strip(),
            resolution_rationale=(
                request.form.get("resolution_rationale", "").strip() or None),
        )
    except fdc001_dw.DecisionError as exc:
        return _render_decision_workspace(
            record, error="Gap assessment rejected: %s" % exc, status=400)
    return redirect(url_for("decision_workspace_view", did=did))


@app.route("/decision-workspace/<did>/preference", methods=["POST"])
def decision_workspace_preference(did):
    record = FDC001_DECISIONS.get(did)
    if record is None:
        return redirect(url_for("decision_workspace_start"))
    action = request.form.get("action", "").strip()
    try:
        if action == "set":
            record.set_owner_preference(
                request.form.get("candidate_id", "").strip(),
                request.form.get("rationale", "").strip() or None)
        elif action == "clear":
            record.clear_owner_preference()
        else:
            raise fdc001_dw.DecisionError("unknown preference action: %r" % action)
    except fdc001_dw.DecisionError as exc:
        return _render_decision_workspace(
            record, error="Preference action rejected: %s" % exc, status=400)
    return redirect(url_for("decision_workspace_view", did=did))


@app.route("/decision-workspace/<did>/candidate", methods=["POST"])
def decision_workspace_dispose_candidate(did):
    record = FDC001_DECISIONS.get(did)
    if record is None:
        return redirect(url_for("decision_workspace_start"))
    try:
        record.dispose_candidate(
            request.form.get("candidate_id", "").strip(),
            request.form.get("option_status", "").strip(),
            request.form.get("disposition_reason", "").strip(),
            request.form.get("disposition_basis", "").strip(),
        )
    except fdc001_dw.DecisionError as exc:
        return _render_decision_workspace(
            record, error="Candidate disposition rejected: %s" % exc, status=400)
    return redirect(url_for("decision_workspace_view", did=did))


@app.route("/decision-workspace/<did>/export", methods=["GET"])
def decision_workspace_export(did):
    record = FDC001_DECISIONS.get(did)
    if record is None:
        return redirect(url_for("decision_workspace_start"))
    # Deterministic, safe attachment filename derived from the decision id.
    filename = "fdc001-decision-%s.json" % record.decision_id
    response = app.response_class(
        response=record.to_json(),
        status=200,
        mimetype="application/json",
    )
    response.headers["Content-Disposition"] = (
        'attachment; filename="%s"' % filename)
    return response


if __name__ == "__main__":
    app.run(debug=True, port=5000)
