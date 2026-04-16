from dataclasses import dataclass
from engine.classifier import ClassificationResult, Intent, Tone


@dataclass
class PriorityResult:
    score: int          # 1 (low) to 5 (critical)
    label: str          # Human-readable label
    sla_hours: float    # Target response time in hours
    reason: str         # Why this priority was assigned


def prioritize(classification: ClassificationResult, is_vip: bool = False) -> PriorityResult:
    """
    Assign a priority score and SLA target to a ticket.

    Priority is driven by:
    - Intent type (bans, fraud, churn risk are high)
    - Tone (threatening or angry escalates priority)
    - VIP status
    - Repeat contact flags

    This is intentionally rules-based rather than ML-driven.
    Rules are auditable, explainable, and easier to adjust without retraining.
    """
    score = 2  # Default: standard
    reasons = []

    # Intent-based baseline
    high_priority_intents = {
        Intent.PAYMENT_ISSUE,
        Intent.REFUND_REQUEST,
        Intent.ACCOUNT_ACCESS,
        Intent.BAN_APPEAL,
    }
    critical_intents = {
        Intent.FRAUD_REPORT,
        Intent.CHURN_RISK,
    }

    if classification.intent in critical_intents:
        score = max(score, 5)
        reasons.append(f"critical intent: {classification.intent.value}")
    elif classification.intent in high_priority_intents:
        score = max(score, 3)
        reasons.append(f"high-priority intent: {classification.intent.value}")

    # Tone escalation
    if classification.tone == Tone.THREATENING:
        score = max(score, 5)
        reasons.append("legal threat detected")
    elif classification.tone == Tone.ANGRY:
        score = max(score, 4)
        reasons.append("angry tone")
    elif classification.tone == Tone.FRUSTRATED:
        score = max(score, 3)
        reasons.append("frustrated tone")

    # Repeat contact escalation
    if "repeat_contact" in classification.flags:
        score = max(score, 4)
        reasons.append("third or more contact on same issue")
    elif "second_contact" in classification.flags:
        score = max(score, 3)
        reasons.append("second contact on same issue")

    # VIP always gets elevated priority
    if is_vip or "vip_player" in classification.flags:
        score = max(score, 4)
        reasons.append("VIP player")

    # Low confidence = needs human quickly
    if classification.confidence < 0.4:
        score = max(score, 3)
        reasons.append("low classification confidence")

    # Map score to label and SLA
    priority_map = {
        1: ("Low", 72.0),
        2: ("Standard", 24.0),
        3: ("High", 8.0),
        4: ("Urgent", 2.0),
        5: ("Critical", 0.5),
    }
    label, sla_hours = priority_map[score]

    return PriorityResult(
        score=score,
        label=label,
        sla_hours=sla_hours,
        reason=" | ".join(reasons) if reasons else "standard ticket",
    )
