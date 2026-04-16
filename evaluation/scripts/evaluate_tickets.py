#!/usr/bin/env python3
"""
evaluate_tickets.py

Run synthetic tickets through the triage pipeline and record results.
Compares pipeline output against expected classifications.

Run: python evaluation/scripts/evaluate_tickets.py
Requires: evaluation/data/tickets.json (run fetch_tickets.py first)
Output: evaluation/data/results.json
"""
import json
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from engine.pipeline import run, TicketContext
from engine.logging_config import configure_logging

configure_logging(level="WARNING")  # Suppress info logs during batch evaluation

INPUT_PATH = Path(__file__).parent.parent / "data" / "tickets.json"
OUTPUT_PATH = Path(__file__).parent.parent / "data" / "results.json"


def evaluate_ticket(ticket: dict) -> dict:
    """
    Run a single ticket through the pipeline and compare to expected output.
    """
    ctx = TicketContext(
        message=ticket["message"],
        player_id=ticket["id"],
        contact_count=ticket.get("contact_count", 1),
        is_vip=ticket.get("is_vip", False),
    )

    try:
        result = run(ctx)

        actual_intent = result.classification.intent.value
        actual_escalate = result.escalation.should_escalate
        expected_intent = ticket["expected_intent"]
        expected_escalate = ticket["expected_escalate"]

        intent_match = actual_intent == expected_intent
        escalation_match = actual_escalate == expected_escalate

        # Determine pass/fail
        # Intent mismatch is a warning. Escalation mismatch is a failure.
        passed = escalation_match  # Escalation accuracy is the primary metric

        return {
            "ticket_id": ticket["id"],
            "message": ticket["message"],
            "expected_intent": expected_intent,
            "actual_intent": actual_intent,
            "intent_match": intent_match,
            "expected_escalate": expected_escalate,
            "actual_escalate": actual_escalate,
            "escalation_match": escalation_match,
            "confidence": result.classification.confidence,
            "priority": result.priority.label,
            "flags": result.classification.flags,
            "processing_time_ms": result.processing_time_ms,
            "passed": passed,
            "error": None,
        }

    except Exception as e:
        return {
            "ticket_id": ticket["id"],
            "message": ticket["message"],
            "error": str(e),
            "passed": False,
        }


def main():
    if not INPUT_PATH.exists():
        print(f"Tickets file not found: {INPUT_PATH}")
        print("Run: python evaluation/scripts/fetch_tickets.py")
        sys.exit(1)

    with open(INPUT_PATH) as f:
        tickets = json.load(f)

    print(f"Evaluating {len(tickets)} tickets...")
    results = []

    for i, ticket in enumerate(tickets):
        result = evaluate_ticket(ticket)
        results.append(result)
        if (i + 1) % 50 == 0:
            print(f"  Processed {i + 1}/{len(tickets)}")

    with open(OUTPUT_PATH, "w") as f:
        json.dump(results, f, indent=2)

    passed = sum(1 for r in results if r.get("passed"))
    print(f"\nComplete: {passed}/{len(results)} passed ({100*passed//len(results)}%)")
    print(f"Results -> {OUTPUT_PATH}")
    print("Run: python evaluation/scripts/generate_report.py")


if __name__ == "__main__":
    main()
