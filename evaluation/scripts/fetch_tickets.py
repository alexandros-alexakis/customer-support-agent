#!/usr/bin/env python3
"""
fetch_tickets.py

Generates synthetic support tickets for evaluation.
In production this would pull from your support platform API.
Here it generates realistic ticket patterns based on known issue distributions.

Run: python evaluation/scripts/fetch_tickets.py
Output: evaluation/data/tickets.json
"""
import json
import random
import uuid
from datetime import datetime, timezone
from pathlib import Path

OUTPUT_PATH = Path(__file__).parent.parent / "data" / "tickets.json"
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

# Realistic ticket distribution based on typical gaming support volume
# Percentages approximate real Tier 1 distributions
TICKET_TEMPLATES = [
    # (message, expected_intent, expected_escalate, weight)
    ("I bought 5000 gold coins and they never appeared", "payment_issue", True, 12),
    ("My purchase didn't arrive after 30 minutes", "payment_issue", False, 8),
    ("I was charged twice for the same pack", "payment_issue", True, 4),
    ("they took money from my account but nothing arrived", "payment_issue", True, 3),
    ("my purchase it not arrive in game", "payment_issue", True, 2),
    ("I want a refund for the pack I bought", "refund_request", True, 8),
    ("I want my money back, I changed my mind", "refund_request", True, 4),
    ("Can I get a refund if I already used the items?", "refund_request", True, 2),
    ("I can't login to my account", "account_access", False, 10),
    ("Forgot my password and reset email isn't arriving", "account_access", True, 5),
    ("My guest account is gone", "account_access", True, 4),
    ("I can't get back into my account after changing phone", "account_access", True, 3),
    ("The game crashed during an alliance war", "technical_issue", False, 8),
    ("App keeps crashing when I open it", "technical_issue", False, 6),
    ("Game is loading really slowly today", "technical_issue", False, 5),
    ("I keep getting disconnected mid-battle", "technical_issue", False, 4),
    ("My account was banned and I don't know why", "ban_appeal", True, 5),
    ("I was wrongly banned, I never cheated", "ban_appeal", True, 4),
    ("How do I upgrade my castle to level 10?", "game_mechanic", False, 6),
    ("What does the alliance bonus do?", "game_mechanic", False, 5),
    ("There is a player in my server using cheats", "fraud_report", True, 3),
    ("Someone hacked my account and took my resources", "account_access", True, 3),
    ("I want to delete all my data", "gdpr_request", True, 2),
    ("I'm done with this game, uninstalling", "churn_risk", True, 3),
    ("If this isn't fixed I'm contacting my lawyer", "ban_appeal", True, 2),
    ("This is the third time I've contacted you", "payment_issue", True, 2),
    ("Something is wrong with my account", "unknown", True, 4),
    ("There's a bug in the alliance system", "bug_report", False, 4),
    ("My items disappeared after the update", "technical_issue", True, 3),
    ("The game won't load since this morning's update", "technical_issue", True, 5),
]


def generate_tickets(n: int = 200) -> list[dict]:
    """
    Generate n synthetic tickets weighted by realistic distribution.
    """
    messages = [t[0] for t in TICKET_TEMPLATES]
    intents = [t[1] for t in TICKET_TEMPLATES]
    escalations = [t[2] for t in TICKET_TEMPLATES]
    weights = [t[3] for t in TICKET_TEMPLATES]

    tickets = []
    indices = random.choices(range(len(TICKET_TEMPLATES)), weights=weights, k=n)

    for i, idx in enumerate(indices):
        contact_count = random.choices([1, 2, 3], weights=[80, 15, 5])[0]
        is_vip = random.random() < 0.05  # 5% VIP rate

        tickets.append({
            "id": f"TKT-{str(uuid.uuid4())[:6].upper()}",
            "message": messages[idx],
            "expected_intent": intents[idx],
            "expected_escalate": escalations[idx],
            "contact_count": contact_count,
            "is_vip": is_vip,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        })

    return tickets


if __name__ == "__main__":
    n = 200
    tickets = generate_tickets(n)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(tickets, f, indent=2)
    print(f"Generated {n} synthetic tickets -> {OUTPUT_PATH}")
