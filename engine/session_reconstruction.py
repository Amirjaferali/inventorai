"""P4-2 Level-1 — deterministic, READ-ONLY reconstruction of review state.

Authorized by `G-P4-2-LEVEL1-IMPLEMENTATION-01` (OPTION A, LEVEL 1). This module
orchestrates ONLY existing canonical components to rebuild, read-only, the review
state of a durably recorded deterministic Path-N session, then returns an
immutable snapshot. It is NOT a resumed session.

Permitted product claim (exact):
  "View a read-only reconstruction of this idea's current review state, recomputed
   from its saved inputs and accepted answers. This is not a resumed session."

What it does (and only this):
  * loads ONE project (project-scoped; the `sid` IS the durable `project_id`);
  * requires a persisted seed idea, confirmed domain, path, and an EXACT supported
    engine/contract version, all captured at project creation;
  * loads the accepted-answer evidence in authoritative store `seq` order
    (`SqliteRecordStore.load_accepted_answer_evidence`, P4-1b-2b), then replays
    the AMENDED stream — the accepted answers the inventor has not explicitly
    withdrawn (`superseded_by is None`, the one canonical active-set rule already
    used by the derived modules). Withdrawn records remain durably present and
    are still restored into the ledger verbatim; they are excluded from the
    replay, never deleted (PVCG-R4-C §8 RP-1, §7 S-1);
  * builds a FRESH canonical `IdeaState`, sets the persisted domain/path, and
    replays the seed FIRST then the accepted-answer contents through the UNCHANGED
    canonical progression path (`engine.progression_loop.run_iteration`);
  * returns an IMMUTABLE `ReconstructedReviewState`.

Hard boundaries (fail-closed, no false-green):
  * deterministic Path N only — any other/missing/unsupported path, missing
    metadata, or version mismatch fails closed to Level-0 accepted-answer evidence
    (no AI, no network, no approximate reconstruction);
  * a malformed/corrupt/cyclic durable history raises the canonical
    `engine.record_contract.ContractError` (propagated from the store) and yields
    NO partial review state;
  * a bounded replay limit (`MAX_ACCEPTED_ANSWER_REPLAY`) is enforced; exceeding it
    fails closed (`ReconstructionReplayLimitError`) with no partial state;
  * NO durable or in-memory mutation of any kind (no DB write, no envelope change,
    no record reorder, no live-`IdeaState` change); reconstruction itself never
    rehydrates `SESSION_STORE` — the SOLE authorized consumer that may place a
    returned `ReconstructedReadonlySession.state` into `SESSION_STORE` is the
    governed P10-PC3 explicit writable-establishment route (`web/app.py`
    `resume_project`, per P10_PC3_TRUE_WRITABLE_RESUME_INCREMENT_CONTRACT.md);
    no other caller may do so and this permits no unrestricted rehydration;
  * outputs are NOT durable and are NOT validated by reconstruction — the snapshot
    only carries a reserved `outputs_validated=False` marker (FPC-02 is NOT
    implemented here);
  * NO accounts/ownership (Phase 5) and NO writable continuation.

The seed idea is sensitive user content: it is never logged, never placed in an
exception string, and never duplicated into an `AssertionRecord`.
"""
from dataclasses import dataclass, field
from typing import Optional

from engine import progression_loop
from engine.idea_state import (IdeaState, DISPOSITION_ANSWERED,
    DISPOSITION_RISK_ACCEPTED)

# One explicit deterministic reconstruction version. It identifies the supported
# engine/contract behaviour — NOT an AI model, timestamp, branch, or environment
# value. Exact match is required; a mismatch fails closed to Level 0 (no replay,
# no silent upgrade/migration). No broad version-history system is introduced.
RECONSTRUCTION_VERSION = "p4-2-level1-recon-v1"

# Deterministic Path-N support only.
SUPPORTED_PATH = "N"

# One explicit bounded maximum on the number of accepted answers replayed (the
# seed is not counted). Deterministic; not an ungoverned environment variable.
# Exceeding it fails closed with no partial review state (never silent truncation).
MAX_ACCEPTED_ANSWER_REPLAY = 500

# Snapshot status vocabulary.
STATUS_RECONSTRUCTED = "RECONSTRUCTED"                       # Level 1
STATUS_NO_METADATA = "LEVEL_0_NO_RECONSTRUCTION_METADATA"    # legacy / unknown / missing field
STATUS_VERSION_MISMATCH = "LEVEL_0_VERSION_MISMATCH"
STATUS_UNSUPPORTED_PATH = "LEVEL_0_UNSUPPORTED_PATH"


class ReconstructionReplayLimitError(Exception):
    """Raised when the accepted-answer replay count exceeds
    ``MAX_ACCEPTED_ANSWER_REPLAY``. Fail-closed: no partial review state is
    produced. The message carries only a count — never user content."""


@dataclass(frozen=True)
class ReconstructedReviewState:
    """Immutable, read-only review snapshot. It is deliberately NOT an
    ``IdeaState`` and exposes no write/continue/submit behaviour.

    ``level`` is 1 for a genuine deterministic reconstruction and 0 for a
    fail-closed accepted-answer-evidence-only fallback. Progression fields
    (``maturity_level`` / ``current_stage`` / ``open_gaps`` / ``next_question``)
    are populated ONLY for Level 1. ``is_resume`` is always False (explicit
    non-resume marker) and ``outputs_validated`` is always False (reconstruction
    validates no prior output)."""
    idea_id: Optional[str]
    level: int
    status: str
    reconstructed: bool
    reconstruction_version: str
    is_resume: bool
    outputs_validated: bool
    accepted_answer_evidence: tuple
    maturity_level: Optional[int] = None
    current_stage: Optional[int] = None
    open_gaps: tuple = field(default_factory=tuple)
    next_question: Optional[str] = None
    # PVCG-R4-C §15: how many durably retained accepted-source records the
    # inventor has explicitly WITHDRAWN (superseded) — counts only, never
    # content. Additive and defaulted, so every pre-R4 construction is
    # unchanged. `withdrawn_source_records` is retained history that was
    # EXCLUDED from the replay below; it is not a deletion.
    withdrawn_source_records: int = 0
    # W2-D (Wave-2 contract §K, W1-N4): per recorded `risk_accepted`
    # disposition, whether the replay re-applied it or it LAPSED against the
    # rebuilt canonical state — a read-only DERIVED report artifact (one
    # `RiskAcceptanceReplayOutcome` per record, in seq order). Additive and
    # defaulted; the D-AISR-06 full-re-evaluation semantics, the canonical
    # writer, and the restored ledger are unchanged — this only makes the
    # already-deterministic outcome visible instead of silent.
    risk_acceptance_outcomes: tuple = field(default_factory=tuple)


@dataclass(frozen=True)
class RiskAcceptanceReplayOutcome:
    """W2-D (W1-N4) — one recorded `risk_accepted` disposition's replay
    outcome. NOT a canonical risk state and never persisted: derived anew on
    every reconstruction from the same durable inputs (deterministic).
    ``reason`` is a bounded category, populated only when ``applied`` is
    False: ``"gap_not_present"`` (the rebuilt journey has not derived the gap
    at the record's replay point) or ``"gap_status_<STATUS>"`` (the gap exists
    but is not OPEN/PARTIAL there)."""
    record_id: str
    gap_context: Optional[str]
    applied: bool
    reason: Optional[str] = None


def contract_assertions_seq(contract):
    """RVR-1: the full durable ledger in authoritative seq order (the contract
    already restores it in order; this named seam keeps the replay's source
    explicit and testable)."""
    return list(contract.assertions)


def _level0(idea_id, status, evidence):
    return ReconstructedReviewState(
        idea_id=idea_id,
        level=0,
        status=status,
        reconstructed=False,
        reconstruction_version=RECONSTRUCTION_VERSION,
        is_resume=False,
        outputs_validated=False,
        accepted_answer_evidence=tuple(evidence),
        maturity_level=None,
        current_stage=None,
        open_gaps=(),
        next_question=None,
    )


@dataclass(frozen=True)
class ReconstructedReadonlySession:
    """P10-PC2 additive accessor result: the Level-1 review snapshot PLUS the
    fresh canonical ``IdeaState`` the replay produced, for READ-ONLY render
    use ONLY (e.g. assembling the truthful cold-load deliverable).

    Obligations on the caller (binding, mirrors the module contract):
      * ``state`` must never be shared with a live session, mutated by a
        read-only consumer, or durably persisted; the SOLE caller authorized
        to place it into ``SESSION_STORE`` is the governed P10-PC3 explicit
        writable-establishment route (see the module docstring) — every other
        consumer treats it as render-only;
      * ``state`` is ``None`` whenever ``review.level`` is 0 (fail-closed
        fallback — there is no reconstructed state to render);
      * reconstruction itself is NOT a resumed session and enables no
        continuation; continuation exists only through the governed
        establishment route."""
    review: ReconstructedReviewState
    state: object


def reconstruct_readonly_state(store, project_id: str) -> "ReconstructedReadonlySession":
    """P10-PC2: deterministically reconstruct the read-only review snapshot AND
    the fresh canonical ``IdeaState`` behind it (same single replay; no second
    subsystem). Identical fail-closed/limit/ContractError semantics to
    ``reconstruct_review_state`` — which remains byte-for-byte unchanged in
    behavior (it returns exactly the ``review`` element). Performs NO mutation
    of any kind."""
    review, state = _reconstruct(store, project_id)
    return ReconstructedReadonlySession(review=review, state=state)


def reconstruct_review_state(store, project_id: str) -> ReconstructedReviewState:
    """Deterministically reconstruct the read-only review state for one project.

    See the module docstring for the full contract. Returns a
    ``ReconstructedReviewState`` (Level 1 on success, Level 0 fail-closed
    otherwise); propagates the canonical ``ContractError`` on malformed durable
    content; raises ``ReconstructionReplayLimitError`` when the accepted-answer
    replay count exceeds the bound. Performs NO mutation of any kind."""
    return _reconstruct(store, project_id)[0]


def _reconstruct(store, project_id: str):
    """Shared single replay (P10-PC2 extraction — verbatim P4-2 Level-1 logic;
    no behavior change). Returns ``(review, state_or_None)``."""
    # Load the accepted-answer evidence FIRST (project-scoped, seq order). This
    # validates the durable contract, so a malformed/corrupt/cyclic history raises
    # the canonical ContractError here — before any Level-0 shortcut — and yields
    # no partial review state. Unknown/empty projects yield the empty tuple.
    evidence = store.load_accepted_answer_evidence(project_id)

    inputs = store.load_reconstruction_inputs(project_id)
    if inputs is None:
        # Legacy project (all reconstruction columns NULL) or unknown project.
        return _level0(None, STATUS_NO_METADATA, evidence), None

    seed = inputs.get("seed_idea_text")
    domain = inputs.get("confirmed_domain")
    path = inputs.get("path")
    version = inputs.get("engine_contract_version")
    if seed is None or domain is None or path is None or version is None:
        # A partially-populated envelope is not sufficient to reconstruct.
        return _level0(None, STATUS_NO_METADATA, evidence), None

    if version != RECONSTRUCTION_VERSION:
        # Do not replay under current rules; do not migrate or silently upgrade.
        return _level0(None, STATUS_VERSION_MISMATCH, evidence), None

    if path != SUPPORTED_PATH:
        # Non-Path-N / unsupported path: fail closed BEFORE any replay, so no AI
        # advisor and no network path is ever reached.
        return _level0(None, STATUS_UNSUPPORTED_PATH, evidence), None

    # PVCG-R4-C §8 RP-9: the replay bound is checked against the FULL persisted
    # answered stream, not the post-withdrawal subset. That is deliberately the
    # conservative reading — a correction can never be used to get UNDER the
    # bound, so it can neither exceed nor disable it.
    if len(evidence) > MAX_ACCEPTED_ANSWER_REPLAY:
        raise ReconstructionReplayLimitError(
            "accepted-answer replay count %d exceeds the bound %d"
            % (len(evidence), MAX_ACCEPTED_ANSWER_REPLAY))

    # PVCG-R4-C §8 RP-1 — THE AMENDED ACCEPTED-SOURCE STREAM.
    #
    # Exactly the same ONE canonical active-set rule the five derived modules
    # already use (`superseded_by is None`); R4 adds no second concept (§7 S-4).
    # A withdrawn record stays durably present and stays in the restored ledger
    # below — it is excluded from the REPLAY, never deleted (§7 S-1, §15 M-1).
    #
    # This is FULL replay of the whole amended stream in `seq` order, never
    # targeted or partial recomputation: the filter selects WHICH INPUTS the
    # inventor withdrew, and every surviving input is then replayed from
    # scratch. No dependency model, no propagation, no selective patching.
    amended = tuple(r for r in evidence if getattr(r, "superseded_by", None) is None)
    withdrawn = len(evidence) - len(amended)

    # The FULL validated durable contract (the evidence load above already
    # validated it). PVCG-R1: this single read supplies BOTH the `idea_id` and
    # the complete durable ledger — no second read, no second store, no second
    # truth source.
    contract = store.load_contract(project_id)
    idea_id = contract.idea_id

    # Fresh, local, canonical state — RECONSTRUCTION ITSELF never rehydrates it
    # into SESSION_STORE and never shares it with any live session; the SOLE
    # authorized consumer that may LATER place the returned state into
    # SESSION_STORE is the governed P10-PC3 explicit writable-resume
    # establishment route (see the module docstring). Path N bypasses the AI
    # advisor inside run_iteration (deterministic), so no external AI/network
    # is invoked.
    state = IdeaState(idea_id=idea_id)
    setattr(state, "domain", domain)     # matches /start's dynamic domain attribute
    state.domain_signal = domain
    state.path = path

    last_result = progression_loop.run_iteration(state, seed)   # seed first
    # RVR-1 (Wave-1 remediation contract, OD-R1): the replay walks the FULL
    # durable ledger in seq order and applies exactly two record kinds — the
    # ACTIVE answered records (identified by membership in the validated
    # `amended` stream, so the answered replay source, bound, and withdrawal
    # semantics are byte-unchanged) and the `risk_accepted` owner dispositions,
    # which re-apply through the SAME canonical lifecycle writer used live.
    # A history containing no risk_accepted record replays byte-identically to
    # the previous answered-only loop. A recorded acceptance that is not
    # applicable at its replay point (impossible for a live-minted history,
    # which validated it at mint) is skipped without mutating anything — the
    # record itself stays restored ledger truth below; nothing is fabricated.
    _amended_ids = {r.record_id for r in amended}
    # W2-D (W1-N4): the replay OUTCOME of every recorded `risk_accepted`
    # disposition is reported instead of silently discarded. The canonical
    # behavior is byte-identical — an inapplicable recorded acceptance is
    # still skipped without mutating anything (no stale acceptance survives)
    # — but the skip is now classified deterministically so the correction
    # UX can truthfully explain the lapse. Derived report only; nothing is
    # persisted and no record is mutated.
    _risk_outcomes = []
    for record in contract_assertions_seq(contract):
        if (record.disposition == DISPOSITION_ANSWERED
                and record.record_id in _amended_ids):
            last_result = progression_loop.run_iteration(state, record.content)
        elif record.disposition == DISPOSITION_RISK_ACCEPTED:
            try:
                progression_loop.accept_gap_risk(state, record.gap_context)
                progression_loop.advance_after_disposition(state)
                _risk_outcomes.append(RiskAcceptanceReplayOutcome(
                    record_id=record.record_id,
                    gap_context=record.gap_context,
                    applied=True))
            except ValueError:
                _gap = state.get_gap(record.gap_context) \
                    if record.gap_context else None
                _reason = ("gap_not_present" if _gap is None
                           else "gap_status_" + _gap.status)
                _risk_outcomes.append(RiskAcceptanceReplayOutcome(
                    record_id=record.record_id,
                    gap_context=record.gap_context,
                    applied=False,
                    reason=_reason))

    # P10-PC2: restore the durably persisted interaction ledger VERBATIM onto
    # the fresh state — these are the very ``AssertionRecord`` values created
    # live and persisted (``rec_N`` preserved, authoritative seq order); no
    # re-derivation, no synthesis. ``run_iteration`` never appends ledger
    # records (that is the web layer's Increment-2 job), so without this the
    # reconstructed state replays progression truthfully but loses the
    # recorded ledger that the deliverable's requirement landscape and
    # validation plan are assembled from. Non-epistemic by the ledger's own
    # contract: gaps, maturity, stage, and next question are unaffected.
    #
    # PVCG-R1: the ledger is restored from the FULL durable contract, so the
    # governed non-answer dispositions (`unknown`, `deferred`,
    # `provisional_assumption`, `specialist_requested`, `evidence_requested`)
    # reconstruct with their recorded meaning instead of being silently dropped.
    # The REPLAY above deliberately still consumes ONLY `evidence` (the
    # `answered` subset), so progression is byte-identically unchanged: a
    # non-answer record is restored as recorded truth and is NEVER replayed,
    # assessed, or allowed to move a gap, maturity, or the stage. Records
    # absent from the durable history stay absent — nothing is fabricated.
    state.assertions = list(contract.assertions)

    open_gaps = tuple(sorted(g.gap_type for g in state.get_open_gaps()))
    next_question = (last_result or {}).get("question")

    return ReconstructedReviewState(
        idea_id=idea_id,
        level=1,
        status=STATUS_RECONSTRUCTED,
        reconstructed=True,
        reconstruction_version=RECONSTRUCTION_VERSION,
        is_resume=False,
        outputs_validated=False,
        accepted_answer_evidence=tuple(evidence),
        maturity_level=state.maturity_level,
        current_stage=state.current_stage,
        open_gaps=open_gaps,
        next_question=next_question,
        withdrawn_source_records=withdrawn,
        risk_acceptance_outcomes=tuple(_risk_outcomes),
    ), state
