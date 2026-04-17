#!/usr/bin/env python3
"""
handover_report.py

Generates an end-of-shift handover report for the incoming team.
Covers: active incidents, critical feedback, knowledge gaps, and recommended actions.

Run: python operations/handover_report.py
Output: operations/handover_report.md
"""
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

OUTPUT_PATH = Path(__file__).parent / "handover_report.md"

INCIDENTS_FILE = Path(__file__).parent.parent / "feedback" / "incidents.json"
FEEDBACK_FILE = Path(__file__).parent.parent / "feedback" / "feedback.json"
GAPS_FILE = Path(__file__).parent.parent / "feedback" / "gaps.json"
EVAL_RESULTS_FILE = Path(__file__).parent.parent / "evaluation" / "data" / "results.json"


def _load_json(path: Path) -> list:
    if not path.exists():
        return []
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        return []


def _is_recent(timestamp_str: str, hours: int = 8) -> bool:
    try:
        ts = datetime.fromisoformat(timestamp_str)
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        return ts >= datetime.now(timezone.utc) - timedelta(hours=hours)
    except Exception:
        return False


def generate_handover_report(shift_hours: int = 8, output_path: str = None) -> str:
    now = datetime.now(timezone.utc)
    incidents = _load_json(INCIDENTS_FILE)
    feedback = _load_json(FEEDBACK_FILE)
    gaps = _load_json(GAPS_FILE)
    eval_results = _load_json(EVAL_RESULTS_FILE)

    active_incidents = [i for i in incidents if i.get("status") == "open"]
    recent_feedback = [f for f in feedback if _is_recent(f.get("timestamp", ""), shift_hours)]
    critical_feedback = [f for f in recent_feedback if f.get("priority") == "critical"]
    recent_gaps = [g for g in gaps if _is_recent(g.get("timestamp", ""), shift_hours)]

    # Volume summary from eval results (last N tickets)
    intent_counts: dict[str, int] = {}
    escalation_count = 0
    if eval_results:
        recent_results = eval_results[-200:]
        for r in recent_results:
            intent = r.get("actual_intent", "unknown")
            intent_counts[intent] = intent_counts.get(intent, 0) + 1
            if r.get("actual_escalate"):
                escalation_count += 1
        total_tickets = len(recent_results)
        escalation_rate = round((escalation_count / total_tickets) * 100, 1) if total_tickets else 0
    else:
        total_tickets = 0
        escalation_rate = 0.0

    lines = [
        "# Shift Handover Report",
        "",
        f"**Prepared:** {now.strftime('%Y-%m-%d %H:%M UTC')}",
        f"**Shift window:** Last {shift_hours} hours",
        "",
        "---",
        "",
    ]

    # Active incidents
    lines += ["## Active Incidents", ""]
    if active_incidents:
        for inc in active_incidents:
            lines += [
                f"### {inc['incident_id']} — `{inc['intent']}`",
                f"- Signal keyword: `{inc.get('keyword_signal', 'unknown')}`",
                f"- Tickets involved: {inc.get('ticket_count', 0)}",
                f"- First seen: {inc.get('first_seen', 'unknown')}",
                f"- Last updated: {inc.get('last_updated', 'unknown')}",
                f"- Notes: {inc.get('notes') or 'none'}",
                "",
            ]
        lines += [
            f"**{len(active_incidents)} active incident(s). Incoming team: monitor volume for these intents.**",
            "",
        ]
    else:
        lines += ["No active incidents.", ""]

    # Critical feedback
    lines += ["## Critical Issues This Shift", ""]
    if critical_feedback:
        for fb in critical_feedback:
            lines += [
                f"- **{fb.get('issue_type', 'unknown')}** — reviewed by {fb.get('reviewed_by', 'unknown')}",
                f"  Player message: *\"{fb.get('player_message', '')[:120]}\"*",
                f"  Notes: {fb.get('notes', 'none')}",
                "",
            ]
    else:
        lines += ["No critical issues recorded this shift.", ""]

    # Knowledge gaps
    lines += ["## Knowledge Gaps Flagged", ""]
    if recent_gaps:
        gap_reasons: dict[str, int] = {}
        for g in recent_gaps:
            reason = g.get("reason", "unknown")
            gap_reasons[reason] = gap_reasons.get(reason, 0) + 1

        lines += [
            f"{len(recent_gaps)} gap(s) flagged this shift:",
            "",
            "| Reason | Count |",
            "|---|---|",
        ]
        for reason, count in sorted(gap_reasons.items(), key=lambda x: x[1], reverse=True):
            lines.append(f"| {reason} | {count} |")
        lines.append("")
        lines += [
            "Review `feedback/gaps.json` and update the relevant KB file if a pattern is clear.",
            "",
        ]
    else:
        lines += ["No knowledge gaps flagged this shift.", ""]

    # Volume summary
    lines += ["## Ticket Volume Summary", ""]
    if total_tickets:
        lines += [
            f"Sample window: {total_tickets} tickets",
            f"Escalation rate: {escalation_rate}%",
            "",
            "| Intent | Count | % |",
            "|---|---|---|",
        ]
        for intent, count in sorted(intent_counts.items(), key=lambda x: x[1], reverse=True):
            pct = round((count / total_tickets) * 100, 1)
            lines.append(f"| {intent} | {count} | {pct}% |")
        lines.append("")
    else:
        lines += ["No evaluation data available for volume summary.", ""]

    # Recommended actions
    lines += ["## Recommended Actions for Incoming Shift", ""]

    actions = []
    if active_incidents:
        intents_str = ", ".join(f"`{i['intent']}`" for i in active_incidents)
        actions.append(f"Monitor volume for {intents_str} — active incidents in progress")
    if critical_feedback:
        actions.append(f"Review {len(critical_feedback)} critical QA flag(s) in `feedback/feedback.json`")
    if recent_gaps:
        actions.append(f"Check `feedback/gaps.json` — {len(recent_gaps)} new gap(s) may need KB updates")
    if escalation_rate > 35:
        actions.append(f"Escalation rate is high ({escalation_rate}%) — review if classifier is handling edge cases correctly")

    if not actions:
        actions.append("No specific actions required. Routine monitoring.")

    for action in actions:
        lines.append(f"- {action}")

    lines += ["", "---", f"*Auto-generated by handover_report.py*"]

    content = "\n".join(lines)

    path = Path(output_path) if output_path else OUTPUT_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    return content


if __name__ == "__main__":
    content = generate_handover_report()
    print(f"Handover report generated -> {OUTPUT_PATH}")
