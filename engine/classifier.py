import re
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Intent(str, Enum):
    PAYMENT_ISSUE = "payment_issue"
    ACCOUNT_ACCESS = "account_access"
    BUG_REPORT = "bug_report"
    REFUND_REQUEST = "refund_request"
    BAN_APPEAL = "ban_appeal"
    GAME_MECHANIC = "game_mechanic"
    TECHNICAL_ISSUE = "technical_issue"
    FRAUD_REPORT = "fraud_report"
    VIP_COMPLAINT = "vip_complaint"
    CHURN_RISK = "churn_risk"
    UNKNOWN = "unknown"


class Tone(str, Enum):
    NEUTRAL = "neutral"
    FRUSTRATED = "frustrated"
    ANGRY = "angry"
    THREATENING = "threatening"
    DISTRESSED = "distressed"


@dataclass
class ClassificationResult:
    intent: Intent
    tone: Tone
    confidence: float  # 0.0 - 1.0
    requires_human: bool
    flags: list[str]  # e.g. ["repeat_contact", "vip_player", "legal_threat"]


# Keyword signals mapped to intents.
# These are not exhaustive - they serve as a first-pass signal before LLM classification.
# If confidence is below threshold, we fall back to LLM or human review.
INTENT_SIGNALS: dict[Intent, list[str]] = {
    Intent.PAYMENT_ISSUE: [
        "charged", "payment", "purchase", "transaction", "didn't receive",
        "missing coins", "missing gems", "not received", "double charge", "duplicate"
    ],
    Intent.REFUND_REQUEST: [
        "refund", "money back", "give me my money", "want a refund", "return"
    ],
    Intent.ACCOUNT_ACCESS: [
        "can't login", "cannot login", "locked out", "forgot password",
        "lost access", "account recovery", "guest account"
    ],
    Intent.BAN_APPEAL: [
        "banned", "suspended", "ban appeal", "account banned",
        "why was i banned", "unfair ban", "wrongly banned"
    ],
    Intent.BUG_REPORT: [
        "bug", "glitch", "not working", "broken", "error", "crash",
        "game crashed", "stuck", "freezing"
    ],
    Intent.TECHNICAL_ISSUE: [
        "app crash", "won't load", "loading issue", "connection",
        "disconnected", "lag", "slow", "black screen"
    ],
    Intent.FRAUD_REPORT: [
        "cheating", "hacker", "cheat", "exploit", "unfair advantage",
        "report player", "botting"
    ],
    Intent.CHURN_RISK: [
        "quitting", "uninstalling", "done with this game", "last time",
        "never playing again", "waste of money", "deleting"
    ],
}

TONE_SIGNALS: dict[Tone, list[str]] = {
    Tone.THREATENING: [
        "lawyer", "lawsuit", "legal action", "sue", "court", "report you",
        "trading standards", "consumer rights"
    ],
    Tone.ANGRY: [
        "unacceptable", "disgusting", "ridiculous", "furious", "outraged",
        "worst", "scam", "fraud", "robbery", "thieves", "pathetic"
    ],
    Tone.FRUSTRATED: [
        "frustrated", "annoyed", "again", "still not", "third time",
        "nobody helps", "useless", "waste of time"
    ],
    Tone.DISTRESSED: [
        "please help", "desperate", "can't afford", "really need",
        "important to me", "means a lot"
    ],
}

# Below this threshold, we do not act autonomously - we route to human review.
CONFIDENCE_THRESHOLD = 0.65


def classify(message: str, contact_count: int = 1, is_vip: bool = False) -> ClassificationResult:
    """
    Classify a player message into an intent and tone.

    contact_count: how many times this player has contacted us on this issue.
    is_vip: whether the player is flagged as VIP in the system.

    Returns a ClassificationResult with confidence score and escalation flags.
    """
    text = message.lower()
    flags = []

    # --- Intent scoring ---
    intent_scores: dict[Intent, int] = {intent: 0 for intent in Intent}
    for intent, signals in INTENT_SIGNALS.items():
        for signal in signals:
            if signal in text:
                intent_scores[intent] += 1

    top_intent = max(intent_scores, key=lambda i: intent_scores[i])
    top_score = intent_scores[top_intent]
    total_signals = sum(intent_scores.values())

    # Confidence = proportion of matched signals belonging to the top intent.
    # If nothing matched, confidence is 0.
    if total_signals == 0:
        confidence = 0.0
        top_intent = Intent.UNKNOWN
    else:
        confidence = top_score / total_signals
        # Dampen confidence slightly when multiple intents compete closely.
        sorted_scores = sorted(intent_scores.values(), reverse=True)
        if len(sorted_scores) > 1 and sorted_scores[1] > 0:
            confidence *= 0.85

    # --- Tone scoring ---
    tone = Tone.NEUTRAL
    for t in [Tone.THREATENING, Tone.ANGRY, Tone.FRUSTRATED, Tone.DISTRESSED]:
        for signal in TONE_SIGNALS[t]:
            if signal in text:
                tone = t
                break
        if tone != Tone.NEUTRAL:
            break

    # --- Flag generation ---
    if contact_count >= 3:
        flags.append("repeat_contact")
    if contact_count == 2:
        flags.append("second_contact")
    if is_vip:
        flags.append("vip_player")
    if tone == Tone.THREATENING:
        flags.append("legal_threat")
    if top_intent == Intent.CHURN_RISK:
        flags.append("churn_risk")
    if top_intent == Intent.BAN_APPEAL:
        flags.append("ban_appeal")
    if top_intent == Intent.FRAUD_REPORT:
        flags.append("fraud_report")

    # --- Human escalation decision ---
    # We always require human review for these cases regardless of confidence.
    auto_escalate_intents = {
        Intent.BAN_APPEAL,
        Intent.FRAUD_REPORT,
        Intent.CHURN_RISK,
        Intent.UNKNOWN,
    }
    requires_human = (
        confidence < CONFIDENCE_THRESHOLD
        or top_intent in auto_escalate_intents
        or tone == Tone.THREATENING
        or "repeat_contact" in flags
        or is_vip
    )

    return ClassificationResult(
        intent=top_intent,
        tone=tone,
        confidence=round(confidence, 3),
        requires_human=requires_human,
        flags=flags,
    )
