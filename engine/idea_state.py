"""
IdeaState — MVP data structure only.
Scope: electronics/electrical, LEVEL 0-2.
Governed by: MVP_SCOPE_FREEZE.md
"""

from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


# --- Evidence quality ---
ASSERTED    = "ASSERTED"
REASONED    = "REASONED"
DEMONSTRATED = "DEMONSTRATED"

# --- Gap types ---
# Stage 2 gap types (3 only per GD-001 frozen)
PHYSICAL_FEASIBILITY    = "PHYSICAL_FEASIBILITY"
BOUNDARY_AMBIGUITY      = "BOUNDARY_AMBIGUITY"
MECHANISM_COMPLETENESS  = "MECHANISM_COMPLETENESS"

# Stage 3 gap types (per STAGE3_GAP_TAXONOMY_PROPOSAL)
PROBLEM_MECHANISM_FIT   = "PROBLEM_MECHANISM_FIT"
ASSUMPTION_INVENTORY    = "ASSUMPTION_INVENTORY"
EXPERTISE_GAP_AWARENESS = "EXPERTISE_GAP_AWARENESS"

# Stage registry
STAGE_2_GAP_TYPES = {MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY}
STAGE_3_GAP_TYPES = {PROBLEM_MECHANISM_FIT, ASSUMPTION_INVENTORY, EXPERTISE_GAP_AWARENESS}

# --- Gap status ---
OPEN          = "OPEN"
PARTIAL       = "PARTIAL"
CLOSED        = "CLOSED"
ACCEPTED_RISK = "ACCEPTED_RISK"

# --- Direction ---
PROGRESSING = "PROGRESSING"
STALLED     = "STALLED"
REGRESSING  = "REGRESSING"


@dataclass
class Evidence:
    content   : str
    quality   : str        # ASSERTED | REASONED | DEMONSTRATED
    iteration : int


@dataclass
class Gap:
    gap_type        : str  # one of the 3 gap types above
    status          : str  # OPEN | PARTIAL | CLOSED | ACCEPTED_RISK
    opened_at       : int  # iteration number
    iterations_open : int  = 0
    closed_at       : Optional[int] = None
    # Accepted (substantiated) Evidence captured for this gap (written only for
    # Stage 3 reasoning gaps). Optional and backward compatible: states/fixtures
    # that omit it default to []. Evidence is defined above and the module
    # evaluates annotations eagerly, so list[Evidence] is safe here.
    evidence        : list[Evidence] = field(default_factory=list)


@dataclass
class IterationLog:
    iteration       : int
    gap_targeted    : str
    question_asked  : str
    response_summary: str
    gaps_changed    : list
    maturity_before : int
    maturity_after  : int


@dataclass
class AcknowledgedUnknown:
    """
    Records an explicit inventor acknowledgment of a specific unknown.
    Parallel track in integrate_response(). NO effect on progression.
    Governance: TRANSITION_AUTHORIZATION_GOVERNANCE s4 Layer 1 PGC-3
    Authorization: Owner-authorized 2026-06-06
    """
    iteration      : int
    gap_context    : str
    verbatim       : str
    category_basis : str


@dataclass
class IdeaState:
    idea_id        : str
    iteration      : int                    = 0
    maturity_level : int                    = 0  # 0 | 1 | 2 only (Stage 2)
    current_stage  : int                    = 2  # 2 = Stage 2, 3 = Stage 3
    domain_signal  : Optional[str]          = None
    direction      : str                    = PROGRESSING

    # What is established
    known_problem   : Optional[Evidence]    = None
    known_mechanism : Optional[Evidence]    = None

    # Open gaps
    gaps           : list                   = field(default_factory=list)

    # History
    iteration_log  : list                   = field(default_factory=list)

    # Acknowledged unknowns -- inventor-stated knowledge gaps (parallel track)
    # No effect on progression. Governance: PGC-3, Priority 5, FDC-001.
    acknowledged_unknowns : list            = field(default_factory=list)

    # Idea capture
    idea_summary   : Optional[str]          = None
    path           : str                    = "legacy_undesignated_current_behavior"
    def get_open_gaps(self):
        return [g for g in self.gaps if g.status in (OPEN, PARTIAL)]

    def get_gap(self, gap_type):
        for g in self.gaps:
            if g.gap_type == gap_type:
                return g
        return None
