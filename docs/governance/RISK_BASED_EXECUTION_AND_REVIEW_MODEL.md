# Risk-Based Execution and Review Model

**Status:** ACTIVE — binding process model. Governs *how* work is executed and reviewed, not *what* is authorized.
**Non-authorizing:** this document changes process efficiency only. It authorizes no product, code, data, or downstream work.

## 1. Non-negotiable quality floor
Accuracy, quality, evidence integrity, and regression protection are mandatory and are **never** reduced for speed. Speed is
achieved by removing procedural steps that protect no real risk — never by lowering correctness, evidence, or regression bars.

## 2. Governance is proportional to actual risk
Each change is classified LOW / MEDIUM / HIGH by its real risk, and follows the matching path.

| Tier | Applies to | Required path |
|---|---|---|
| **LOW** | documentation, roadmap updates, bounded status records, wording corrections, non-executing owner decisions | prepare → automated verification → Draft PR review → owner merge decision |
| **MEDIUM** | contracts, architecture proposals, schemas, BASE RED tests, AI-behavior proposals, changes that may affect stored or structured outputs | prepare → focused verification → one independent review → Draft PR → owner merge decision |
| **HIGH** | production implementation, persistence, database migrations, security, privacy, safety-critical logic, broad AI-behavior changes, destructive/irreversible actions, backward-compatibility risks | contract → BASE RED → implementation → GREEN/regression → evidence → independent review → owner acceptance → merge |

When a change spans tiers, the **highest** applicable tier governs.

## 3. Default review mechanism
A GitHub **Draft PR** is the default review and evidence mechanism at every tier.

## 4. When a separate `.bundle` transfer is required
Only when at least one holds: (a) the branch cannot be published; (b) the reviewer cannot access the commit; (c) confidential
or technical constraints prevent GitHub review; (d) preservation of an unpublished artifact is materially necessary. Otherwise
the Draft PR alone suffices.

## 5. Bounded low-risk authorization
A single bounded owner authorization may cover related LOW-risk actions end to end — branch creation, file preparation, commit,
push, and Draft PR — without separate approvals for each step.

## 6. Merge is a separate owner decision
Merge remains a separate owner decision whenever the artifact changes canonical governance, product behavior, code, data, or
execution status.

## 7. Independent review is applied where it protects a real risk
Independent review is mandatory **only** where it materially protects factual correctness, technical correctness, safety, data
integrity, compatibility, or scope control. It is applied at MEDIUM and HIGH tiers per §2, and at LOW tier only if such a risk
is actually present.

## 8. No empty procedural gates
A procedural gate that does not reduce a real, identified risk must not be added or repeated. Gates exist to protect risks, not
to accumulate ceremony.

## 9. Non-authorization boundary
This model authorizes none of: Phase B; external research; Technical Knowledge Package construction; architecture; contract;
BASE RED; implementation; integration; D13 closure; Workstream 8; or any product / code / database / UI / schema / prompt /
persistence change. Those remain separate owner decisions under their own authorities.

## 10. Handover requirement
All future handovers must cite this document, and successor agents (team leads, subagents, Agent Teams teammates) are required
to follow it.
