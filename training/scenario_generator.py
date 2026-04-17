#!/usr/bin/env python3
"""
scenario_generator.py

Generates realistic practice scenarios for new agent training.
Each scenario includes the ticket, context, expected handling, and common mistakes.

Scenarios are graded Easy / Medium / Hard to support progressive skill-building.

Run: python training/scenario_generator.py
Output: training/scenarios.md
"""
import json
import random
from datetime import datetime, timezone
from pathlib import Path

OUTPUT_PATH = Path(__file__).parent / "scenarios.md"

_SCENARIOS = [
    # (message, contact_count, is_vip, intent, tone, escalate, team, difficulty, correct_approach, mistakes)
    (
        "I bought 5000 gold coins and they never appeared in my account.",
        1, False, "payment_issue", "neutral", True, "billing",
        "Easy",
        "Acknowledge the issue. Collect Player ID and transaction ID. Check if the payment shows in platform receipts. Escalate to billing with full details.",
        ["Promising a refund without authorisation", "Asking the player to repurchase", "Not collecting the transaction ID before escalating"],
    ),
    (
        "This is the THIRD time I have contacted you about a missing purchase. Nobody ever helps me.",
        3, False, "payment_issue", "angry", True, "billing",
        "Medium",
        "Lead with empathy and acknowledge this is not their first contact. Take ownership. Do not ask them to repeat information already given. Escalate with urgent flag and full contact history.",
        ["Starting with a generic greeting", "Asking for information they may have already provided", "Matching the player's frustration", "Saying 'unfortunately'"],
    ),
    (
        "I can't log into my account. I tried resetting my password but the email never arrived.",
        1, False, "account_access", "frustrated", True, "account_team",
        "Easy",
        "Collect login method (email, Google, Apple, Facebook, guest). Ask them to check spam folder. If still no email, escalate to account team with the login method confirmed.",
        ["Assuming the login method without asking", "Telling them to 'try again later'", "Not checking if the reset email is in spam"],
    ),
    (
        "My account was banned. I have never cheated in my life. This is completely unfair.",
        1, False, "ban_appeal", "angry", True, "trust_and_safety",
        "Medium",
        "Acknowledge frustration without confirming or denying the ban reason. Do not share any information about what triggered the restriction. Collect Player ID and date ban was noticed. Escalate to Trust & Safety.",
        ["Saying 'I understand you didn't cheat'", "Explaining what caused the ban", "Promising the ban will be reversed", "Asking for screenshots of gameplay"],
    ),
    (
        "I want a refund for the pack I bought yesterday. I didn't mean to buy it.",
        1, False, "refund_request", "neutral", True, "billing",
        "Easy",
        "Acknowledge the request without confirming a refund is possible. Collect Player ID, transaction ID, platform, and whether items were used. Escalate to billing for review.",
        ["Saying 'refunds are not available'", "Promising a refund will be issued", "Not checking whether items were used before escalating"],
    ),
    (
        "There is a player in my server using an obvious speed hack. I have video proof.",
        1, False, "fraud_report", "neutral", True, "trust_and_safety",
        "Easy",
        "Thank the player for reporting. Collect: reported player's username, date and description of incident, and ask them to send screenshots or video via the link. Escalate to Trust & Safety.",
        ["Promising the reported player will be banned", "Asking for the reported player's Player ID (they won't have it)", "Telling the player the outcome of the investigation"],
    ),
    (
        "I'm completely done with this game. I've spent €200 and it keeps crashing. I'm uninstalling.",
        1, False, "churn_risk", "angry", True, "player_relations",
        "Hard",
        "Lead with genuine empathy — do not jump to troubleshooting. Acknowledge the spend and the frustration. Escalate immediately to player relations as a churn risk. Collect Player ID. Do not offer refunds or compensation without authorisation.",
        ["Opening with technical troubleshooting steps", "Offering a refund or bonus without authorisation", "Minimising the player's frustration", "Saying 'I understand your frustration but...'"],
    ),
    (
        "The game crashed during my alliance war battle and I lost all my troops. Can you restore them?",
        1, False, "technical_issue", "frustrated", False, "tier1",
        "Medium",
        "Acknowledge the frustration. Collect device model, OS version, app version, and exact timing of the crash. Check if this is an isolated issue or part of a wider incident. Do not promise troop restoration — that requires billing team review.",
        ["Promising troop restoration", "Escalating immediately without gathering device info", "Dismissing the loss as 'normal game behaviour'"],
    ),
    (
        "I want to delete my account and all my data. GDPR.",
        1, False, "unknown", "neutral", True, "senior_agent",
        "Hard",
        "Treat this as a formal GDPR data deletion request. Do not attempt to handle at Tier 1. Collect Player ID and the email address on the account. Escalate to the data privacy team (senior agent route) and inform the player of the 30-day statutory response window.",
        ["Attempting to process the deletion yourself", "Asking the player to 'just uninstall the game'", "Promising deletion within a specific short timeframe", "Not informing the player of the statutory response window"],
    ),
    (
        "If this issue isn't resolved today I will be taking legal action and posting on every review site.",
        2, False, "ban_appeal", "threatening", True, "trust_and_safety",
        "Hard",
        "Stay calm and professional. Do not engage with the legal threat directly. Do not escalate the tone. Acknowledge the frustration briefly and state that the case is being escalated. Collect Player ID. Pass 'legal_threat' flag to the receiving team.",
        ["Saying 'please calm down'", "Responding to the legal threat directly ('we have done nothing wrong')", "Promising an outcome to avoid escalation", "Matching the urgency or emotion of the player"],
    ),
    (
        "I accidentally bought the wrong pack. Can I swap it for a different one?",
        1, False, "refund_request", "neutral", True, "billing",
        "Easy",
        "Acknowledge the request. Collect Player ID, transaction ID, platform, pack name purchased, and pack name wanted. Check item usage. Escalate to billing — swaps are treated the same as refunds.",
        ["Approving the swap yourself", "Telling the player swaps are 'not possible'", "Not asking whether the items in the wrong pack were used"],
    ),
    (
        "The app won't open at all since this morning's update.",
        1, False, "technical_issue", "frustrated", False, "technical",
        "Easy",
        "Acknowledge the timing (post-update). Check whether this is a known incident. Collect device model, OS version, app version. Ask them to try: force-close, clear cache, reinstall. If multiple players are reporting the same issue after an update, flag as a potential incident.",
        ["Immediately telling the player to reinstall without troubleshooting", "Not noting the update timing as a relevant signal", "Escalating without gathering basic device info first"],
    ),
]


def _format_scenario(idx: int, scenario: tuple) -> str:
    (message, contact_count, is_vip, intent, tone, escalate, team,
     difficulty, correct_approach, mistakes) = scenario

    context_parts = []
    if contact_count > 1:
        context_parts.append(f"Contact #{contact_count} from this player")
    if is_vip:
        context_parts.append("VIP player")
    context_str = " · ".join(context_parts) if context_parts else "First contact"

    escalate_str = f"Yes → {team}" if escalate else "No (handle at Tier 1)"
    mistakes_str = "\n".join(f"  - {m}" for m in mistakes)

    return f"""---

### Scenario {idx}: [{difficulty}]

**Player message:**
> "{message}"

**Context:** {context_str}

**Expected classification:** Intent: `{intent}` | Tone: `{tone}` | Escalate: {escalate_str}

**Correct approach:**
{correct_approach}

**Common mistakes to avoid:**
{mistakes_str}
"""


def generate_scenarios(
    count: int = None,
    difficulty_filter: str = None,
    shuffle: bool = True,
    output_path: str = None,
) -> str:
    scenarios = list(_SCENARIOS)

    if difficulty_filter:
        scenarios = [s for s in scenarios if s[7].lower() == difficulty_filter.lower()]

    if shuffle:
        random.shuffle(scenarios)

    if count:
        scenarios = scenarios[:count]

    lines = [
        "# Agent Training Scenarios",
        "",
        f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        f"Scenarios: {len(scenarios)}",
        "",
        "Use these scenarios for onboarding practice, team calibration sessions, or coaching.",
        "Each scenario includes the expected handling approach and common mistakes.",
        "",
        "**Difficulty guide:** Easy = Tier 1 standard · Medium = requires judgement · Hard = edge case / emotional",
        "",
    ]

    easy = [s for s in scenarios if s[7] == "Easy"]
    medium = [s for s in scenarios if s[7] == "Medium"]
    hard = [s for s in scenarios if s[7] == "Hard"]

    if not difficulty_filter:
        lines += [
            "## Summary",
            "",
            f"| Difficulty | Count |",
            f"|---|---|",
            f"| Easy | {len(easy)} |",
            f"| Medium | {len(medium)} |",
            f"| Hard | {len(hard)} |",
            "",
        ]

    for i, scenario in enumerate(scenarios, 1):
        lines.append(_format_scenario(i, scenario))

    content = "\n".join(lines)

    path = Path(output_path) if output_path else OUTPUT_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    return content


if __name__ == "__main__":
    content = generate_scenarios(shuffle=False)
    print(f"Generated {len(_SCENARIOS)} training scenarios -> {OUTPUT_PATH}")
    print(f"Easy: {sum(1 for s in _SCENARIOS if s[7]=='Easy')}  "
          f"Medium: {sum(1 for s in _SCENARIOS if s[7]=='Medium')}  "
          f"Hard: {sum(1 for s in _SCENARIOS if s[7]=='Hard')}")
