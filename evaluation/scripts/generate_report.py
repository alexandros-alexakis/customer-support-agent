#!/usr/bin/env python3
"""
generate_report.py

Read evaluation results and produce a summary report.

Run: python evaluation/scripts/generate_report.py
Requires: evaluation/data/results.json (run evaluate_tickets.py first)
Output: evaluation/data/report.md
"""
import json
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict

INPUT_PATH = Path(__file__).parent.parent / "data" / "results.json"
OUTPUT_PATH = Path(__file__).parent.parent / "data" / "report.md"


def generate_report(results: list[dict]) -> str:
    total = len(results)
    errors = [r for r in results if r.get("error")]
    valid = [r for r in results if not r.get("error")]

    passed = sum(1 for r in valid if r.get("passed"))
    failed = len(valid) - passed

    intent_matches = sum(1 for r in valid if r.get("intent_match"))
    escalation_matches = sum(1 for r in valid if r.get("escalation_match"))

    # Average confidence
    confidences = [r["confidence"] for r in valid if "confidence" in r]
    avg_confidence = sum(confidences) / len(confidences) if confidences else 0

    # Average processing time
    times = [r["processing_time_ms"] for r in valid if "processing_time_ms" in r]
    avg_time = sum(times) / len(times) if times else 0

    # Failures by intent
    failures_by_intent = defaultdict(int)
    for r in valid:
        if not r.get("passed"):
            failures_by_intent[r.get("expected_intent", "unknown")] += 1

    # False negatives (should have escalated, did not)
    false_negatives = [
        r for r in valid
        if r.get("expected_escalate") and not r.get("actual_escalate")
    ]

    # False positives (should not have escalated, did)
    false_positives = [
        r for r in valid
        if not r.get("expected_escalate") and r.get("actual_escalate")
    ]

    lines = [
        "# Evaluation Report",
        f"",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        f"",
        f"## Summary",
        f"",
        f"| Metric | Value |",
        f"|---|---|",
        f"| Total tickets | {total} |",
        f"| Errors | {len(errors)} |",
        f"| Valid evaluations | {len(valid)} |",
        f"| Passed (escalation correct) | {passed} ({100*passed//len(valid) if valid else 0}%) |",
        f"| Failed | {failed} |",
        f"| Intent accuracy | {intent_matches}/{len(valid)} ({100*intent_matches//len(valid) if valid else 0}%) |",
        f"| Escalation accuracy | {escalation_matches}/{len(valid)} ({100*escalation_matches//len(valid) if valid else 0}%) |",
        f"| Average confidence | {avg_confidence:.3f} |",
        f"| Average processing time | {avg_time:.1f}ms |",
        f"| False negatives (missed escalations) | {len(false_negatives)} |",
        f"| False positives (unnecessary escalations) | {len(false_positives)} |",
        f"",
        f"## Failures by Intent",
        f"",
        f"| Intent | Failures |",
        f"|---|---|",
    ]

    for intent, count in sorted(failures_by_intent.items(), key=lambda x: x[1], reverse=True):
        lines.append(f"| {intent} | {count} |")

    lines += [
        f"",
        f"## False Negatives (Missed Escalations)",
        f"",
        f"These are the highest risk failures - tickets that should have been escalated but were not.",
        f"",
    ]

    for r in false_negatives[:10]:  # Show top 10
        lines.append(f"- `{r['ticket_id']}`: {r['message'][:80]}")
        lines.append(f"  - Expected: escalate | Actual: {r.get('actual_intent')} (confidence: {r.get('confidence', 'N/A')})")

    lines += [
        f"",
        f"## False Positives (Unnecessary Escalations)",
        f"",
    ]

    for r in false_positives[:10]:
        lines.append(f"- `{r['ticket_id']}`: {r['message'][:80]}")
        lines.append(f"  - Expected: handle at Tier 1 | Actual: escalated")

    if errors:
        lines += [
            f"",
            f"## Errors",
            f"",
        ]
        for r in errors[:5]:
            lines.append(f"- `{r['ticket_id']}`: {r.get('error')}")

    return "\n".join(lines)


def main():
    if not INPUT_PATH.exists():
        print(f"Results file not found: {INPUT_PATH}")
        print("Run: python evaluation/scripts/evaluate_tickets.py")
        return

    with open(INPUT_PATH) as f:
        results = json.load(f)

    report = generate_report(results)

    with open(OUTPUT_PATH, "w") as f:
        f.write(report)

    print(f"Report generated -> {OUTPUT_PATH}")
    print(report[:800])  # Print summary to console


if __name__ == "__main__":
    main()
