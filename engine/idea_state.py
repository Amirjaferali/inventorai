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

# --- Gap types (3 only per MVP_SCOPE_FREEZE) ---
PHYSICAL_FEASIBILITY    = "PHYSICAL_FEASIBILITY"
BOUNDARY_AMBIGUITY      = "BOUNDARY_AMBIGUITY"
MECHANISM_COMPLETENESS  = "MECHANISM_COMPLETENESS"

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
class IdeaState:
    idea_id        : str
    iteration      : int                    = 0
    maturity_level : int                    = 0  # 0 | 1 | 2 only
    domain_signal  : Optional[str]          = None
    direction      : str                    = PROGRESSING

    # What is established
    known_problem   : Optional[Evidence]    = None
    known_mechanism : Optional[Evidence]    = None

    # Open gaps
    gaps           : list                   = field(default_factory=list)

    # History
    iteration_log  : list                   = field(default_factory=list)
      
    # Idea capture
    idea_summary   : Optional[str]          = None

    def get_open_gaps(self):
        return [g for g in self.gaps if g.status in (OPEN, PARTIAL)]

    def get_gap(self, gap_type):
        for g in self.gaps:
            if g.gap_type == gap_type:
                return g
        return None
