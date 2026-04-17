#!/usr/bin/env python3
"""
team_performance_dashboard.py

Aggregates QA scores, escalation accuracy, and volume by team.
Teams are derived from escalation routing (intent -> team mapping).

Run: python operations/team_performance_dashboard.py
Output: operations/team_performance_dashboard.md
"""
import json
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict

OUTPUT_PATH = Path(__file__).parent / "team_performance_dashboard.md"

QA_SCORES_FILE = Path(__file__).parent.parent / "qa" / "scores.json"
EVAL_RESULTS_FILE = Path(__file__).parent.parent / "evaluation" / "data" / "results.json"
INCIDENTS_FILE = Path(__file__).parent.parent / "feedback" / "incidents.json"

# Maps intent to the team that owns it (mirrors engine/escalation.py ROUTING_TABLE)
_INTENT_TO_TEAM = {
    "payment_issue": "Billing",
    "refund_request": "Billing",
    "account_access": "Account Team",
    "ban_appeal": "Trust & Safety",
    "fraud_report": "Trust & Safety",
    "bug_report": "Technical",
    "technical_issue": "Technical",
    "churn_risk": "Player Relations",
    "vip_complaint": "Player Relations",
    "game_mechanic": "Tier 1",
    "unknown": "Senior Agent",
    "gdpr_request": "Senior Agent",
}

_CATEGORY_MAXES = {"tone": 20, "accuracy": 30, "resolution": 25, "clarity": 15, "escalation": 10}
_CATEGORY_LABELS = {
    "tone": "Tone", "accuracy": "Accuracy", "resolution": "Resolution",
    "clarity": "Clarity", "escalation": "Escalation",
}

_BANDS = [(90, "Excellent"), (75, "Good"), (60, "Needs Improvement"), (0, "Critical")]


def _band(score: float) -> str:
    for threshold, label in _BANDS:
        if score >= threshold:
            return label
    return "Critical"


def _load_json(path: Path) -> list:
    if not path.exists():
        return []
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        return []


def generate_dashboard(output_path: str = None) -> str:
    qa_records = _load_json(QA_SCORES_FILE)
    eval_results = _load_json(EVAL_RESULTS_FILE)
    incidents = _load_json(INCIDENTS_FILE)

    now = datetime.now(timezone.utc)

    lines = [
        "# Team Performance Dashboard",
        "",
        f"**Generated:** {now.strftime('%Y-%m-%d %H:%M UTC')}",
        "",
        "---",
        "",
    ]

    # --- QA section ---
    if not qa_records:
        lines += ["## QA Scores", "", "No QA scores recorded yet. Run `qa/auto_scorer.py` first.", ""]
    else:
        team_qa: dict[str, list[dict]] = defaultdict(list)
        for r in qa_records:
            intent = r.get("intent", "unknown")
            team = _INTENT_TO_TEAM.get(intent, "Unknown")
            team_qa[team].append(r)

        all_totals = [r.get("total", 0) for r in qa_records]
        overall_avg = round(sum(all_totals) / len(all_totals), 1)
        fatal_count = sum(1 for r in qa_records if r.get("fatal_error"))

        lines += [
            "## QA Scores by Team",
            "",
            f"Total interactions scored: {len(qa_records)} | Overall average: **{overall_avg}/100** | Fatal errors: **{fatal_count}**",
            "",
            "| Team | Interactions | Avg Score | Band | Tone | Accuracy | Resolution | Clarity | Escalation |",
            "|---|---|---|---|---|---|---|---|---|",
        ]

        for team in sorted(team_qa.keys()):
            records = team_qa[team]
            totals = [r.get("total", 0) for r in records]
            avg = round(sum(totals) / len(totals), 1)
            band = _band(avg)

            cat_avgs = {}
            for cat in _CATEGORY_MAXES:
                vals = [r.get("scores", {}).get(cat, 0) for r in records]
                cat_avgs[cat] = round(sum(vals) / len(vals), 1)

            lines.append(
                f"| {team} | {len(records)} | {avg} | {band} "
                f"| {cat_avgs['tone']}/{_CATEGORY_MAXES['tone']} "
                f"| {cat_avgs['accuracy']}/{_CATEGORY_MAXES['accuracy']} "
                f"| {cat_avgs['resolution']}/{_CATEGORY_MAXES['resolution']} "
                f"| {cat_avgs['clarity']}/{_CATEGORY_MAXES['clarity']} "
                f"| {cat_avgs['escalation']}/{_CATEGORY_MAXES['escalation']} |"
            )

        lines.append("")

        # Highlight worst team
        worst_team = min(team_qa.keys(), key=lambda t: sum(
            r.get("total", 0) for r in team_qa[t]
        ) / len(team_qa[t]))
        worst_avg = round(sum(r.get("total", 0) for r in team_qa[worst_team]) / len(team_qa[worst_team]), 1)

        if worst_avg < 75:
            lines += [
                f"> **Coaching priority:** {worst_team} is averaging {worst_avg}/100. "
                f"Run `qa/coaching_report.py` for a detailed coaching plan.",
                "",
            ]

    # --- Escalation accuracy section ---
    if eval_results:
        lines += ["## Escalation Accuracy by Team", ""]

        team_eval: dict[str, dict] = defaultdict(lambda: {"correct": 0, "total": 0, "false_neg": 0, "false_pos": 0})
        for r in eval_results:
            intent = r.get("actual_intent", "unknown")
            team = _INTENT_TO_TEAM.get(intent, "Unknown")
            team_eval[team]["total"] += 1
            if r.get("escalation_match"):
                team_eval[team]["correct"] += 1
            elif r.get("expected_escalate") and not r.get("actual_escalate"):
                team_eval[team]["false_neg"] += 1
            elif not r.get("expected_escalate") and r.get("actual_escalate"):
                team_eval[team]["false_pos"] += 1

        lines += [
            "| Team | Tickets | Escalation Accuracy | Missed Escalations ⚠ | Unnecessary Escalations |",
            "|---|---|---|---|---|",
        ]

        for team in sorted(team_eval.keys()):
            d = team_eval[team]
            accuracy = round((d["correct"] / d["total"]) * 100, 1) if d["total"] else 0
            fn_flag = " ⚠" if d["false_neg"] > 0 else ""
            lines.append(
                f"| {team} | {d['total']} | {accuracy}% "
                f"| {d['false_neg']}{fn_flag} | {d['false_pos']} |"
            )

        lines.append("")
        lines += [
            "> **Missed escalations** are high-risk — a ticket that should have been escalated was handled at Tier 1.",
            "",
        ]

    # --- Volume by team ---
    if eval_results:
        lines += ["## Volume by Team", ""]

        team_volume: dict[str, int] = defaultdict(int)
        for r in eval_results:
            intent = r.get("actual_intent", "unknown")
            team = _INTENT_TO_TEAM.get(intent, "Unknown")
            team_volume[team] += 1

        total = sum(team_volume.values())
        lines += [
            f"Based on last {total} tickets in evaluation data.",
            "",
            "| Team | Volume | % of Total |",
            "|---|---|---|",
        ]
        for team, count in sorted(team_volume.items(), key=lambda x: x[1], reverse=True):
            pct = round((count / total) * 100, 1)
            lines.append(f"| {team} | {count} | {pct}% |")
        lines.append("")

    # --- Incidents ---
    active_incidents = [i for i in incidents if i.get("status") == "open"]
    lines += ["## Active Incidents", ""]
    if active_incidents:
        lines += [
            "| Incident ID | Intent | Ticket Count | First Seen |",
            "|---|---|---|---|",
        ]
        for inc in active_incidents:
            lines.append(
                f"| {inc['incident_id']} | {inc['intent']} "
                f"| {inc['ticket_count']} | {inc.get('first_seen', '')[:16]} |"
            )
        lines.append("")
    else:
        lines += ["No active incidents.", ""]

    lines += ["---", f"*Auto-generated by team_performance_dashboard.py*"]

    content = "\n".join(lines)

    path = Path(output_path) if output_path else OUTPUT_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    return content


if __name__ == "__main__":
    content = generate_dashboard()
    print(f"Team performance dashboard generated -> {OUTPUT_PATH}")
