#!/usr/bin/env python3
"""
coaching_report.py

Generates actionable coaching plans from QA scores.
Groups performance by intent category, identifies weak areas,
and produces specific improvement actions linked to tone guide and KB.

Run: python qa/coaching_report.py
Output: qa/coaching_report.md
"""
import json
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict

QA_SCORES_FILE = Path(__file__).parent / "scores.json"
OUTPUT_PATH = Path(__file__).parent / "coaching_report.md"

_CATEGORY_MAXES = {
    "tone": 20,
    "accuracy": 30,
    "resolution": 25,
    "clarity": 15,
    "escalation": 10,
}

_CATEGORY_LABELS = {
    "tone": "Tone & Empathy",
    "accuracy": "Accuracy & Policy Compliance",
    "resolution": "Resolution Quality",
    "clarity": "Communication Clarity",
    "escalation": "Escalation Handling",
}

_COACHING_ACTIONS = {
    "tone": [
        "Re-read tone-guide.md — focus on 'Good vs Poor Response Examples'",
        "Practice the empathy-first pattern: acknowledge before resolving",
        "Remove 'unfortunately', 'but', and 'please calm down' from responses",
        "Review the 'Words and Phrases to Avoid' table in tone-guide.md",
    ],
    "accuracy": [
        "Re-read the relevant KB file before responding (faq-payments.md, faq-account-access.md, etc.)",
        "Never state a policy that is not explicitly in the KB — say 'let me confirm' instead",
        "Review refund-policy-detail.md — this is the most commonly misquoted policy",
        "Check escalation-rules.md to confirm which team owns each issue type",
    ],
    "resolution": [
        "Confirm the next step before closing: 'Is there anything else I can help you with?'",
        "If escalating, always tell the player what happens next and when",
        "Review decision-table.md to verify the correct Tier 1 action for each intent",
        "Do not close a ticket as 'resolved' unless the player has confirmed the issue is fixed",
    ],
    "clarity": [
        "Use shorter sentences — aim for one idea per sentence",
        "Avoid jargon: replace 'transaction ID' with 'the 10-digit number from your receipt'",
        "Use numbered steps for multi-step instructions",
        "Read your response aloud — if it sounds awkward, rewrite it",
    ],
    "escalation": [
        "Review escalation-rules.md to confirm correct team routing",
        "Always collect required information before escalating (see decision-table.md per intent)",
        "Tell the player: who is handling it, what the SLA is, and what to expect next",
        "Do not escalate unnecessarily — check if the issue can be resolved at Tier 1 first",
    ],
}

_INTENT_KB_MAP = {
    "payment_issue": "faq-payments.md",
    "refund_request": "refund-policy-detail.md",
    "account_access": "faq-account-access.md",
    "ban_appeal": "banned-account-faq.md",
    "fraud_report": "tos-violations-guide.md",
    "technical_issue": "faq-technical-issues.md",
    "bug_report": "faq-technical-issues.md",
    "game_mechanic": "faq-game-mechanics.md",
    "churn_risk": "vip-player-handling.md",
    "vip_complaint": "vip-player-handling.md",
}


def _pct(score: float, max_val: int) -> float:
    return round((score / max_val) * 100, 1) if max_val else 0.0


def _load_scores() -> list[dict]:
    if not QA_SCORES_FILE.exists():
        return []
    with open(QA_SCORES_FILE, "r") as f:
        return json.load(f)


def generate_coaching_report(output_path: str = None) -> str:
    records = _load_scores()

    if not records:
        content = "# Coaching Report\n\nNo QA scores recorded yet. Run `qa/auto_scorer.py` to generate scores.\n"
        path = Path(output_path) if output_path else OUTPUT_PATH
        with open(path, "w") as f:
            f.write(content)
        return content

    # Aggregate by intent
    by_intent: dict[str, list[dict]] = defaultdict(list)
    overall_cat_sums: dict[str, float] = {k: 0.0 for k in _CATEGORY_MAXES}
    overall_totals = []
    fatal_records = []

    for r in records:
        by_intent[r.get("intent", "unknown")].append(r)
        for cat in _CATEGORY_MAXES:
            overall_cat_sums[cat] += r.get("scores", {}).get(cat, 0)
        overall_totals.append(r.get("total", 0))
        if r.get("fatal_error"):
            fatal_records.append(r)

    n = len(records)
    overall_avg = round(sum(overall_totals) / n, 1)

    # Find weakest categories (by % of max)
    cat_avgs = {k: overall_cat_sums[k] / n for k in _CATEGORY_MAXES}
    cat_pcts = {k: _pct(cat_avgs[k], _CATEGORY_MAXES[k]) for k in _CATEGORY_MAXES}
    weak_cats = sorted(cat_pcts.items(), key=lambda x: x[1])[:2]

    lines = [
        "# Coaching Report",
        "",
        f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        f"Interactions reviewed: {n}",
        f"Overall average score: **{overall_avg}/100**",
        "",
    ]

    # Overall summary table
    lines += [
        "## Overall Performance",
        "",
        "| Category | Avg Score | Max | % |",
        "|---|---|---|---|",
    ]
    for cat, label in _CATEGORY_LABELS.items():
        avg = round(cat_avgs[cat], 1)
        pct = cat_pcts[cat]
        flag = " ⚠" if pct < 70 else ""
        lines.append(f"| {label} | {avg} | {_CATEGORY_MAXES[cat]} | {pct}%{flag} |")
    lines.append("")

    # Fatal errors
    if fatal_records:
        lines += [
            f"## ⚠ Fatal Errors ({len(fatal_records)} recorded)",
            "",
            "Fatal errors result in an automatic score of 0 and require immediate coaching.",
            "",
        ]
        for r in fatal_records:
            lines += [
                f"- **{r.get('intent', 'unknown')}** — {r.get('fatal_reason', 'unspecified')}",
                f"  Player message: *\"{r.get('player_message', '')[:100]}\"*",
                "",
            ]

    # Priority coaching areas
    lines += [
        "## Priority Coaching Areas",
        "",
        f"The two weakest categories are **{_CATEGORY_LABELS[weak_cats[0][0]]}** "
        f"({weak_cats[0][1]}%) and **{_CATEGORY_LABELS[weak_cats[1][0]]}** ({weak_cats[1][1]}%).",
        "",
    ]

    for cat, pct in weak_cats:
        lines += [
            f"### {_CATEGORY_LABELS[cat]} ({pct}% of max)",
            "",
            "**Recommended actions:**",
        ]
        for action in _COACHING_ACTIONS[cat]:
            lines.append(f"- {action}")
        lines.append("")

    # Per-intent breakdown
    lines += [
        "## Performance by Intent",
        "",
        "| Intent | Count | Avg Score | Weakest Category |",
        "|---|---|---|---|",
    ]

    for intent, intent_records in sorted(by_intent.items(), key=lambda x: len(x[1]), reverse=True):
        in_totals = [r.get("total", 0) for r in intent_records]
        in_avg = round(sum(in_totals) / len(in_totals), 1)

        in_cat_avgs = {}
        for cat in _CATEGORY_MAXES:
            vals = [r.get("scores", {}).get(cat, 0) for r in intent_records]
            in_cat_avgs[cat] = sum(vals) / len(vals)
        weakest = min(in_cat_avgs, key=lambda c: _pct(in_cat_avgs[c], _CATEGORY_MAXES[c]))

        lines.append(
            f"| {intent} | {len(intent_records)} | {in_avg}/100 | {_CATEGORY_LABELS[weakest]} |"
        )

    lines.append("")

    # Intent-specific coaching
    lines += ["## Intent-Specific Coaching", ""]

    for intent, intent_records in sorted(by_intent.items(), key=lambda x: len(x[1]), reverse=True):
        in_totals = [r.get("total", 0) for r in intent_records]
        in_avg = round(sum(in_totals) / len(in_totals), 1)

        in_cat_avgs = {}
        for cat in _CATEGORY_MAXES:
            vals = [r.get("scores", {}).get(cat, 0) for r in intent_records]
            in_cat_avgs[cat] = sum(vals) / len(vals)

        worst_cat = min(in_cat_avgs, key=lambda c: _pct(in_cat_avgs[c], _CATEGORY_MAXES[c]))
        worst_pct = _pct(in_cat_avgs[worst_cat], _CATEGORY_MAXES[worst_cat])

        kb_ref = _INTENT_KB_MAP.get(intent)
        kb_line = f"Reference KB: `knowledge-base/{kb_ref}`" if kb_ref else ""

        lines += [
            f"### {intent} (avg {in_avg}/100, n={len(intent_records)})",
            "",
            f"Biggest gap: **{_CATEGORY_LABELS[worst_cat]}** at {worst_pct}%",
            "",
        ]
        if kb_line:
            lines.append(kb_line)
            lines.append("")

        for action in _COACHING_ACTIONS[worst_cat][:2]:
            lines.append(f"- {action}")
        lines.append("")

    content = "\n".join(lines)

    path = Path(output_path) if output_path else OUTPUT_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    return content


if __name__ == "__main__":
    content = generate_coaching_report()
    print(f"Coaching report generated -> {OUTPUT_PATH}")
