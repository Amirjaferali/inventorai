"""
InventorAI — Minimal CLI
Scope: electronics/electrical, LEVEL 0-2 only.
Governed by: MVP_SCOPE_FREEZE.md
DO NOT modify engine behavior from this file.
"""

import sys
sys.path.insert(0, '.')
import json
from engine.summary import build_summary

from engine.idea_state import IdeaState, Gap, MECHANISM_COMPLETENESS, OPEN
from engine.progression_loop import run_iteration
from engine.domain_rules import infer_domain

MAX_ITERATIONS = 5

def run_cli():
    print("=" * 60)
    print("  InventorAI — Progression Engine MVP")
    print("  Scope: Electronics/Electrical, Level 0-2")
    print("=" * 60)
    print()

    # Step 1: Get idea
    idea = input("Enter your invention idea:\n> ").strip()
    if not idea:
        print("No idea entered. Exiting.")
        return

    print()

    # Step 2: Infer domain
    domain = infer_domain(idea)
    print(f"Domain inferred: {domain or 'unknown'}")

    # Step 3: Check scope
    if domain != "electronics_electrical":
        print()
        print("─" * 60)
        print("OUTSIDE MVP SCOPE")
        print("─" * 60)
        print("This MVP supports electronics/electrical ideas only.")
        print("Your idea domain was not recognized as electronics.")
        print()
        print("Supported signals include: sensor, circuit, WiFi,")
        print("microcontroller, IoT, voltage, current, PCB, etc.")
        print("─" * 60)
        return

    print("Domain confirmed: electronics/electrical")
    print()

    # Step 4-5: Initialize state
    state = IdeaState(idea_id="cli-session")
    state.domain_signal = domain
    state.gaps.append(Gap(MECHANISM_COMPLETENESS, OPEN, 0))

    print(f"Starting at Level {state.maturity_level}")
    print("─" * 60)

    boundary_asked = False

    # Step 6: Run loop
    for i in range(1, MAX_ITERATIONS + 1):
        print(f"\n[Iteration {i} / {MAX_ITERATIONS}]")
        print(f"Current Level: {state.maturity_level}")

        # Get response for current question
        # First show what we'll ask
        from engine.progression_loop import select_next_gap, get_question
        gap_type = select_next_gap(state)

        if gap_type:
            gap = state.get_gap(gap_type)
            iters_open = gap.iterations_open if gap else 0
            question = get_question(gap_type, iters_open)
        elif state.maturity_level >= 1:
            question = ("Your mechanism is taking shape. "
                       "Now state clearly: what does your invention "
                       "NOT do or NOT cover? Name at least one boundary.")
            boundary_asked = True
        else:
            question = "Tell me more about the problem your invention solves and who experiences it." 

        if question:
            print(f"\nQuestion: {question}")
            print()
            response = input("Your answer:\n> ").strip()
            if not response:
                print("No answer provided — skipping.")
                continue
        else:
            print("No further questions at this level.")
            break

        # Run iteration
        result = run_iteration(state, response)

        # Step 7: Show result
        print()
        print(f"  Transition : {result['transition']}")
        print(f"  Level      : {result['maturity_level']}")
        print(f"  Direction  : {result['direction']}")
        if result.get('reason'):
            print(f"  Reason     : {result['reason']}")

        # Step 8: Stop conditions
        if result['maturity_level'] == 2 and boundary_asked:
            print()
            print("─" * 60)
            print("LEVEL 2 REACHED")
            print("─" * 60)
            print("Your invention idea has reached structured clarity.")
            print()
            print("What was established:")
            if state.known_mechanism:
                print(f"  Mechanism : {state.known_mechanism.content[:100]}")
            if state.known_problem:
                print(f"  Context   : {state.known_problem.content[:100]}")
            print()
            print("Gaps status:")
            for g in state.gaps:
                print(f"  {g.gap_type}: {g.status}")
            print("─" * 60)
            summary = build_summary(state)
            print()
            print("═" * 60)
            print("FINAL SUMMARY")
            print("═" * 60)
            print(__import__("json").dumps(summary, indent=2, default=str))
            print("═" * 60)
            break

        if i == MAX_ITERATIONS:
            print()
            print("─" * 60)
            print(f"MAX ITERATIONS REACHED — Final Level: {state.maturity_level}")
        summary = build_summary(state)
        print()
        print("═" * 60)
        print("FINAL SUMMARY")
        print("═" * 60)
        print(json.dumps(summary, indent=2, default=str))
        print("═" * 60)
        print("-" * 60)

if __name__ == "__main__":
    run_cli()
