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
from engine.decision_workspace import Candidate, DecisionRecord


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
    """Withdraw an active alternative. Its chain leaves the composed candidate
    set; the ledger keeps the full history. A later re-declaration founds a
    NEW chain (new root, new identity)."""
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


def decision_capture_view(state):
    """Presentation-shaped, JSON-safe projection for the existing journey
    surfaces (session/deliverable templates). Derived; carries the ledger ids
    the bounded UI forms need (context root, active alternative head ids).
    Introduces no second canonical model — every value restates the composed
    FDC-001 record or the ledger verbatim."""
    assertions = list(getattr(state, "assertions", []))
    by_id, root_of = _chain_index(assertions)
    active = [r for r in assertions
              if getattr(r, "superseded_by", None) is None]
    heads = {}
    for r in active:
        if r.disposition == DISPOSITION_DECISION_ALTERNATIVE_DECLARED:
            heads[root_of(r)] = r
    view = []
    for rec in compose_decision_records(state):
        ctx_root = rec.decision_id.rsplit("-", 1)[-1]
        view.append({
            "context_root": ctx_root,
            "decision_id": rec.decision_id,
            "question": rec.decision_question,
            "readiness_status": rec.readiness_status,
            "alternatives": [
                {
                    "candidate_id": c.candidate_id,
                    "root": c.candidate_id.rsplit("-", 1)[-1],
                    "head_record_id": heads[
                        c.candidate_id.rsplit("-", 1)[-1]].record_id,
                    "name": c.name,
                }
                for c in rec.candidates
            ],
        })
    return view
