from dataclasses import dataclass
from engine.classifier import ClassificationResult, Intent, Tone


@dataclass
class EscalationResult:
    should_escalate: bool
    team: str               # Which team to route to
    reason: str             # Why escalation was triggered
    notes: str              # What the receiving team needs to know


# Routing table: intent -> specialist team
# This is defined here rather than in the classifier because routing
# is an operational concern, not a classification concern.
ROUTING_TABLE: dict[str, str] = {
    Intent.PAYMENT_ISSUE: "billing",
    Intent.REFUND_REQUEST: "billing",
    Intent.ACCOUNT_ACCESS: "account_team",
    Intent.BAN_APPEAL: "trust_and_safety",
    Intent.FRAUD_REPORT: "trust_and_safety",
    Intent.BUG_REPORT: "technical",
    Intent.TECHNICAL_ISSUE: "technical",
    Intent.CHURN_RISK: "player_relations",
    Intent.VIP_COMPLAINT: "player_relations",
    Intent.GAME_MECHANIC: "tier1",  # Tier 1 can handle this
    Intent.UNKNOWN: "senior_agent",
}


def evaluate_escalation(
    classification: ClassificationResult,
    is_vip: bool = False,
    contact_count: int = 1,
    prior_resolution_attempted: bool = False,
) -> EscalationResult:
    """
    Decide whether to escalate and where to route.

    This function separates escalation logic from classification.
    The classifier tells us WHAT the issue is.
    This function decides WHAT TO DO about it.

    prior_resolution_attempted: True if Tier 1 steps were already tried.
    """
    reasons = []
    notes_parts = []

    # Hard escalation rules - these always escalate, no exceptions
    hard_escalate = False

    if classification.tone == Tone.THREATENING:
        hard_escalate = True
        reasons.append("legal threat in message")
        notes_parts.append("Player mentioned legal action. Do not engage on legal specifics.")

    if "legal_threat" in classification.flags:
        hard_escalate = True

    if classification.intent in {Intent.BAN_APPEAL, Intent.FRAUD_REPORT}:
        hard_escalate = True
        reasons.append(f"intent requires specialist: {classification.intent.value}")

    if "repeat_contact" in classification.flags:
        hard_escalate = True
        reasons.append("third or more contact on unresolved issue")
        notes_parts.append(f"Player has contacted {contact_count} times. Previous attempts did not resolve the issue.")

    if is_vip:
        hard_escalate = True
        reasons.append("VIP player")
        notes_parts.append("VIP player - prioritise response and follow up proactively after resolution.")

    # Soft escalation - escalate if Tier 1 already tried and failed
    soft_escalate = False
    if prior_resolution_attempted and classification.confidence >= 0.65:
        soft_escalate = True
        reasons.append("Tier 1 resolution attempted but issue unresolved")

    # Low confidence = don't guess, escalate to a human
    if classification.confidence < 0.4:
        soft_escalate = True
        reasons.append(f"low classification confidence ({classification.confidence})")
        notes_parts.append("Classifier was not confident in intent. Human review recommended before responding.")

    should_escalate = hard_escalate or soft_escalate

    # Determine routing
    team = ROUTING_TABLE.get(classification.intent, "senior_agent")

    # Override routing for specific flag combinations
    if "legal_threat" in classification.flags:
        team = "legal_compliance"
    elif is_vip and classification.intent in {Intent.PAYMENT_ISSUE, Intent.REFUND_REQUEST}:
        team = "player_relations"  # VIP billing goes to player relations, not generic billing

    return EscalationResult(
        should_escalate=should_escalate,
        team=team,
        reason=" | ".join(reasons) if reasons else "no escalation required",
        notes=" ".join(notes_parts) if notes_parts else "",
    )
