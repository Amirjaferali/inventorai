"""W2-A / RVR-4 — bounded Path-N decision composition seam.

Authoritative contract: docs/governance/W2_A_RVR4_IMPLEMENTATION_CONTRACT_CANDIDATE.md
(PR #567). Purpose (contract §5/§7/§9):

  * mint canonical W2-A decision actions through the governed carrier path
    (`IdeaState.record_interaction` — the carrier itself fails closed, so
    these wrappers hold NO validation monopoly and there is no bypass);
  * reconstruct active decision contexts and alternative chains from the
    final amended active assertion state;
  * derive FDC-001 `DecisionRecord` objects deterministically (injected
    root-based identities, injected decision question, seed suppression);
  * apply deterministic ordering; and
  * persist NOTHING — the composed record is recomputed on demand; the
    AssertionRecord ledger remains the sole durable truth.

This module is NOT a second persistence layer, NOT a second canonical
decision model, NOT an AI surface, and NOT a Decision Workspace replacement.
FDC-001 `DecisionRecord` remains the sole canonical decision-semantics owner;
its unchanged pure derivations compute readiness/blocking over the composed
state (a truthful `insufficient_information` is expected while comparison
inputs are empty by construction). Broader Decision Workspace Path-T remains
`PRESERVE UNMODIFIED AND PAUSE`.

G-3 (authoritative contract PR #598; Owner decisions PR #599) adds the
bounded RENDERED alternative set beside — never instead of — the FDC
comparison-eligible candidate set:

  * SET A, ``rendered_alternative_set`` — what the inventor can see: one entry
    per founding alternative root they declared, a user-WITHDRAWN one
    included, so a withdrawal never silently disappears (D-G3-1);
  * SET B, ``compose_decision_records`` — ``DecisionRecord.candidates``: a user
    withdrawal REMOVES the alternative from it, unchanged from W2-A.

Both are deterministic projections of the SAME ledger; neither is a second
store, model, comparison engine or persistence layer. Visibility alone creates
NO decision-semantic consequence (contract A-24): membership of SET B is read
from the composed record and is never inferred from SET A. A withdrawal is a
lifecycle act, not an FDC disposition, so no ``dispose_candidate()``-equivalent
state is fabricated for it (A-23(b)), and refinement text is never promoted to
a ``ClaimItem`` (D-G3-2). Only already-existing ``DecisionRecord`` vocabulary is
reused, through this same seam (OD-W2-DW-LIFT permission (3), Owner reading).

Determinism (contract §9): identity is root-based
(`decision-pn-<idea_id>-<root>`, `cand-pn-<root>`), never uuid, never
replay-position, never display-text; ordering is by ascending numeric
founding-root record_id; equal amended ledgers compose byte-identically.
"""

from engine.idea_state import (
    DISPOSITION_DECISION_CONTEXT_DECLARED,
    DISPOSITION_DECISION_ALTERNATIVE_DECLARED,
    DISPOSITION_DECISION_ALTERNATIVE_WITHDRAWN,
)
from engine.decision_workspace import (
    CANDIDATE_NOT_YET_COMPARABLE,
    Candidate,
    DecisionRecord,
)

# G-3 rendered-set vocabulary. These name PRESENTATION facts about SET A and
# are deliberately NOT `option_status` / `disposition_basis` values: no new
# FDC vocabulary is created, and none of these ever reaches a `DecisionRecord`.
ALT_LIFECYCLE_ACTIVE = "active"
ALT_LIFECYCLE_WITHDRAWN = "withdrawn"
EVIDENCE_NO_RECORDED_DETAIL = "no_recorded_detail"
EVIDENCE_RECORDED_DETAIL = "recorded_detail"


def _root_num(record_id):
    """Ascending-numeric ordering key for canonical ``rec_N`` roots. A
    non-``rec_N`` root fails loudly (never silently mis-orders) — canonical
    mints always produce ``rec_N`` ids."""
    prefix, _, num = str(record_id).partition("_")
    if prefix != "rec" or not num.isdigit():
        raise ValueError(f"non-canonical decision root id: {record_id!r}")
    return int(num)


def _chain_index(assertions):
    """Map record_id -> record plus, for each record, its chain ROOT
    (follow the single-target ``supersedes`` edge to the chain origin).
    Deterministic and insertion-order independent."""
    by_id = {r.record_id: r for r in assertions}

    def root_of(record):
        node = record
        while node.supersedes:
            node = by_id[node.supersedes[0]]
        return node.record_id

    return by_id, root_of


# --- canonical mint wrappers (carrier does the fail-closed validation) -------

def declare_decision_context(state, content, iteration=0):
    """Found a new decision context. The founding record's id is the context's
    permanent root."""
    return state.record_interaction(
        action=DISPOSITION_DECISION_CONTEXT_DECLARED, content=content,
        iteration=iteration)


def declare_alternative(state, content, context_root, iteration=0):
    """Found a new alternative chain inside the context rooted at
    ``context_root``."""
    return state.record_interaction(
        action=DISPOSITION_DECISION_ALTERNATIVE_DECLARED, content=content,
        decision_context_root=context_root, iteration=iteration)


def refine_alternative(state, content, supersedes_id, iteration=0):
    """Refine an active alternative (same chain, root identity preserved).
    The owning context root is derived from the superseded record itself, so
    a caller cannot mislabel the context (the carrier re-validates)."""
    target = state._require_record(supersedes_id)
    return state.record_interaction(
        action=DISPOSITION_DECISION_ALTERNATIVE_DECLARED, content=content,
        decision_context_root=target.decision_context_root,
        supersedes=[supersedes_id], iteration=iteration)


def withdraw_alternative(state, supersedes_id, reason="", iteration=0):
    """Withdraw an active alternative (D-G3-1: a USER LIFECYCLE ACT, never an
    evidence-based system elimination). Its chain leaves the FDC
    comparison-eligible candidate set (SET B) and STAYS in the bounded rendered
    set (SET A) with its reason and provenance, so the inventor still sees what
    happened to it; the ledger keeps the full history. A later re-declaration
    founds a NEW chain (new root, new identity) — the withdrawn chain is never
    silently reactivated."""
    target = state._require_record(supersedes_id)
    return state.record_interaction(
        action=DISPOSITION_DECISION_ALTERNATIVE_WITHDRAWN, content=reason or "",
        decision_context_root=target.decision_context_root,
        supersedes=[supersedes_id], iteration=iteration)


# --- deterministic composition (contract §9) ---------------------------------

def compose_decision_records(state):
    """Derive one FDC-001 ``DecisionRecord`` per decision context, from the
    final amended ACTIVE assertion state. Pure, read-only, deterministic;
    returns records ordered by ascending numeric context root."""
    assertions = list(getattr(state, "assertions", []))
    by_id, root_of = _chain_index(assertions)
    active = [r for r in assertions
              if getattr(r, "superseded_by", None) is None]

    # Context chains: founding record (context class, no supersedes) -> the
    # chain's ACTIVE head carries the current decision question.
    context_heads = {}
    for r in active:
        if r.disposition == DISPOSITION_DECISION_CONTEXT_DECLARED:
            context_heads[root_of(r)] = r

    # Alternative chains: ACTIVE head of class alternative_declared belongs to
    # its context's candidate set; a withdrawn/superseded chain is absent.
    # Absent HERE means absent from SET B only — `rendered_alternative_set`
    # still shows a withdrawn chain to the inventor (D-G3-1).
    alternatives = {}
    for r in active:
        if r.disposition == DISPOSITION_DECISION_ALTERNATIVE_DECLARED:
            alternatives.setdefault(r.decision_context_root, []).append(
                (root_of(r), r))

    records = []
    for ctx_root in sorted(context_heads, key=_root_num):
        head = context_heads[ctx_root]
        candidates = [
            Candidate(candidate_id=f"cand-pn-{alt_root}", name=alt_head.content)
            for alt_root, alt_head in sorted(
                alternatives.get(ctx_root, []), key=lambda p: _root_num(p[0]))
        ]
        records.append(DecisionRecord(
            decision_id=f"decision-pn-{state.idea_id}-{ctx_root}",
            decision_question=head.content,
            seeded=False,
            initial_candidates=candidates,
        ))
    return records


def rendered_alternative_set(state):
    """G-3 SET A — the bounded RENDERED alternative set, keyed by context root.

    One entry per founding alternative root the inventor declared inside a
    context, **including a user-withdrawn one** (D-G3-1: no silent
    disappearance). Each entry carries only ledger-derived facts:

      ``root``               the founding record id — stable identity
      ``name``               the LATEST declared content of that chain, verbatim
      ``lifecycle_state``    ``active`` | ``withdrawn`` — a USER lifecycle fact
      ``head_record_id``     the active declared head (``None`` when withdrawn)
      ``withdrawal_reason``  the inventor's recorded reason; ``""`` when the
                             withdrawal recorded none; ``None`` when not
                             withdrawn. Never invented, never upgraded.
      ``refinement_count``   refinements recorded on that chain
      ``evidence_state``     derived ONLY from that chain's own records

    This function decides NOTHING about FDC comparison membership, readiness,
    accounting or disposition — those remain ``compose_decision_records`` and
    the unchanged ``DecisionRecord`` derivations. Pure, read-only,
    deterministic (ascending numeric founding root), persisted nowhere.
    """
    assertions = list(getattr(state, "assertions", []))
    by_id, root_of = _chain_index(assertions)
    active = [r for r in assertions
              if getattr(r, "superseded_by", None) is None]

    # Every declared record of each alternative chain, in ledger order: the
    # last one is the chain's current text, and the count gives the recorded
    # refinement depth. Refinement text is read here as the inventor's own
    # recorded detail ONLY — it is never projected into an FDC `ClaimItem`
    # and is never given a claim class (D-G3-2).
    declared_by_root = {}
    for r in assertions:
        if r.disposition == DISPOSITION_DECISION_ALTERNATIVE_DECLARED:
            declared_by_root.setdefault(root_of(r), []).append(r)

    by_context = {}
    for r in active:
        root = root_of(r)
        chain = declared_by_root.get(root, [])
        if r.disposition == DISPOSITION_DECISION_ALTERNATIVE_DECLARED:
            entry = {
                "root": root,
                "name": r.content,
                "lifecycle_state": ALT_LIFECYCLE_ACTIVE,
                "head_record_id": r.record_id,
                "withdrawal_reason": None,
            }
        elif r.disposition == DISPOSITION_DECISION_ALTERNATIVE_WITHDRAWN:
            if not chain:
                # A withdrawal whose chain carries no declared record cannot be
                # described truthfully; fail loudly rather than render a
                # fabricated alternative.
                raise ValueError(
                    f"withdrawal {r.record_id!r} has no declared chain record")
            entry = {
                "root": root,
                "name": chain[-1].content,
                "lifecycle_state": ALT_LIFECYCLE_WITHDRAWN,
                "head_record_id": None,
                # `content` IS the reason the inventor supplied; "" means the
                # withdrawal recorded none, which the surface must say plainly.
                "withdrawal_reason": r.content or "",
            }
        else:
            continue
        entry["refinement_count"] = max(len(chain) - 1, 0)
        entry["evidence_state"] = (
            EVIDENCE_RECORDED_DETAIL if entry["refinement_count"]
            else EVIDENCE_NO_RECORDED_DETAIL)
        by_context.setdefault(r.decision_context_root, []).append(entry)

    for entries in by_context.values():
        entries.sort(key=lambda e: _root_num(e["root"]))
    return by_context


def decision_capture_view(state):
    """Presentation-shaped, JSON-safe projection for the existing journey
    surfaces (session/deliverable templates). Derived; carries the ledger ids
    the bounded UI forms need (context root, active alternative head ids).
    Introduces no second canonical model — every value restates the composed
    FDC-001 record, SET A, or the ledger verbatim.

    Each rendered alternative additionally carries the SET A / SET B split:
    ``comparison_eligible`` and ``candidate_id`` are read from the composed
    record's own candidate list, and ``not_comparable`` from its own derived
    ``blocking_reasons`` — never inferred from the fact that an alternative is
    visible (contract A-24). Blocking reasons are exposed as CODES so the
    surface can render a governed EN/AR string; the engine's English
    ``BlockingReason.text`` is never served (contract §10 / A-16).
    """
    rendered = rendered_alternative_set(state)
    view = []
    for rec in compose_decision_records(state):
        ctx_root = rec.decision_id.rsplit("-", 1)[-1]
        members = {c.candidate_id.rsplit("-", 1)[-1]: c for c in rec.candidates}
        not_comparable_ids = {
            b.affected_candidate_id for b in rec.blocking_reasons
            if b.code == CANDIDATE_NOT_YET_COMPARABLE}
        alternatives = []
        for entry in rendered.get(ctx_root, []):
            candidate = members.get(entry["root"])
            alternatives.append(dict(
                entry,
                candidate_id=(candidate.candidate_id if candidate else None),
                comparison_eligible=candidate is not None,
                option_status=(candidate.option_status if candidate else None),
                not_comparable=bool(
                    candidate is not None
                    and candidate.candidate_id in not_comparable_ids),
            ))
        view.append({
            "context_root": ctx_root,
            "decision_id": rec.decision_id,
            "question": rec.decision_question,
            "readiness_status": rec.readiness_status,
            "blocking_reason_codes": [b.code for b in rec.blocking_reasons],
            "alternatives": alternatives,
        })
    return view
