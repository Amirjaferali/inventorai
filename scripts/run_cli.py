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
from engine.domain_rules import classify_domain, DomainResultKind
from engine import domain_activation

MAX_ITERATIONS = 5


def _cli_domain_label(domain):
    """Human-readable presentation label for a specialist domain (presentation
    only; never affects classification or activation). Mirrors the web layer's
    `_domain_label` shape (`web/app.py`) without importing it — this CLI stays
    decoupled from the web module, consulting only the canonical
    `engine.domain_activation` activation source directly."""
    return domain.replace("_", " ").title()


def _cli_supported_domains_phrase(activated):
    """Truthful natural-language enumeration of the activated domains."""
    labels = [_cli_domain_label(d) for d in activated]
    if len(labels) == 1:
        return labels[0]
    return ", ".join(labels[:-1]) + " or " + labels[-1]

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

    # Step 2: Classify domain (P9-E2-R: dispatch by result KIND; never stringify
    # the structured result, never treat a richer kind as a single domain).
    classification = classify_domain(idea)
    if classification.kind in (DomainResultKind.AMBIGUOUS_TIE,
                               DomainResultKind.MULTI_DOMAIN_NEEDS_D4,
                               DomainResultKind.UNRESOLVED_NON_ACTIVATED_TIE):
        # CF5-F004: the zero-activated unresolved tie joins the existing
        # bounded stop — never an arbitrary winner, never a proceed.
        # Explicit bounded stop: never print an arbitrary winner, never treat this
        # as a single domain, never activate a domain, never execute D4. No
        # implication that multi-domain analysis occurred. (Dormant until the later,
        # separate P9-E2 tie-precedence runtime produces these kinds.)
        print()
        print("─" * 60)
        print("CANNOT DETERMINE A SINGLE SUPPORTED DOMAIN")
        print("─" * 60)
        print("This MVP supports electronics/electrical ideas only, and this idea")
        print("could not be resolved to a single supported domain.")
        print("─" * 60)
        return
    # SINGLE -> resolved registry domain string; NONE -> None (unchanged behavior).
    domain = (classification.selected_domain
              if classification.kind is DomainResultKind.SINGLE else None)
    print(f"Domain inferred: {domain or 'unknown'}")

    # Step 3: Check scope — CF-6/CF-2 CLI shared-facet fix: admissibility derives
    # from the canonical activation policy (engine.domain_activation), never a
    # hardcoded domain literal (mirrors the CF5-F002 fix already applied to the
    # Web /start surface, engine.domain_activation.activated_domains(), reused
    # unchanged). Byte-identical under ['electronics_electrical'] (today's only
    # governed activation state); truthful under any broadened activation set
    # (reachable only via a bounded test double today).
    activated = domain_activation.activated_domains()
    if domain not in activated:
        print()
        print("─" * 60)
        print("OUTSIDE MVP SCOPE")
        print("─" * 60)
        if activated == ["electronics_electrical"]:
            print("This MVP supports electronics/electrical ideas only.")
            print("Your idea domain was not recognized as electronics.")
            print()
            print("Supported signals include: sensor, circuit, WiFi,")
            print("microcontroller, IoT, voltage, current, PCB, etc.")
        elif not activated:
            print("No specialist domain is available right now.")
            print("Please try again later.")
        else:
            print("This MVP currently supports " +
                  _cli_supported_domains_phrase(activated) + " ideas only.")
            print("Your idea domain was not recognized as a supported domain.")
        print("─" * 60)
        return

    if domain == "electronics_electrical":
        print("Domain confirmed: electronics/electrical")
    else:
        print(f"Domain confirmed: {_cli_domain_label(domain)}")
    print()

    # Step 4-5: Initialize state
    state = IdeaState(idea_id="cli-session")
    state.domain_signal = domain
    state.domain = domain
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
            question = get_question(state.domain, gap_type, iters_open)
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
