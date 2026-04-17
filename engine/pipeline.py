import time
import logging
from dataclasses import dataclass, asdict, field
from typing import Optional
from engine.classifier import classify, ClassificationResult
from engine.prioritizer import prioritize, PriorityResult
from engine.escalation import evaluate_escalation, EscalationResult
from engine.response_router import get_response_strategy, ResponseStrategy

logger = logging.getLogger(__name__)


@dataclass
class TicketContext:
    message: str
    player_id: str
    contact_count: int = 1
    is_vip: bool = False
    prior_resolution_attempted: bool = False
    account_context: Optional[dict] = None
    incident_id: Optional[str] = None


@dataclass
class PipelineResult:
    player_id: str
    classification: ClassificationResult
    priority: PriorityResult
    escalation: EscalationResult
    strategy: ResponseStrategy
    processing_time_ms: float


def run(context: TicketContext) -> PipelineResult:
    """
    Run the full ticket processing pipeline.

    Steps:
    1. Classify intent and tone
    2. Assign priority and SLA
    3. Evaluate escalation need and routing
    4. Generate response strategy

    Each step is independent. Failures in one step do not silently corrupt others.
    All decisions are logged with enough context to audit later.
    """
    start = time.monotonic()

    # Step 1: Classify
    try:
        classification = classify(
            message=context.message,
            contact_count=context.contact_count,
            is_vip=context.is_vip,
        )
    except Exception as e:
        logger.error("classifier_failed", extra={"player_id": context.player_id, "error": str(e)})
        raise

    logger.info(
        "ticket_classified",
        extra={
            "player_id": context.player_id,
            "intent": classification.intent.value,
            "tone": classification.tone.value,
            "confidence": classification.confidence,
            "flags": classification.flags,
        },
    )

    # Step 2: Prioritize
    priority = prioritize(classification, is_vip=context.is_vip)

    logger.info(
        "ticket_prioritized",
        extra={
            "player_id": context.player_id,
            "priority_score": priority.score,
            "priority_label": priority.label,
            "sla_hours": priority.sla_hours,
            "reason": priority.reason,
        },
    )

    # Step 3: Escalation
    escalation = evaluate_escalation(
        classification=classification,
        is_vip=context.is_vip,
        contact_count=context.contact_count,
        prior_resolution_attempted=context.prior_resolution_attempted,
    )

    if escalation.should_escalate:
        logger.warning(
            "ticket_escalated",
            extra={
                "player_id": context.player_id,
                "team": escalation.team,
                "reason": escalation.reason,
            },
        )
    else:
        logger.info(
            "ticket_tier1_handling",
            extra={"player_id": context.player_id, "intent": classification.intent.value},
        )

    # Step 4: Response strategy
    strategy = get_response_strategy(classification, escalation)

    processing_time_ms = (time.monotonic() - start) * 1000

    logger.info(
        "pipeline_complete",
        extra={
            "player_id": context.player_id,
            "processing_time_ms": round(processing_time_ms, 2),
            "requires_human": classification.requires_human,
        },
    )

    try:
        from feedback.incident_detector import record_ticket_for_correlation
        incident = record_ticket_for_correlation(
            player_id=context.player_id,
            intent=classification.intent.value,
            message=context.message,
            ticket_id=context.player_id,
        )
        if incident:
            context.incident_id = incident.incident_id
            logger.warning(
                "incident_detected",
                extra={
                    "incident_id": incident.incident_id,
                    "intent": classification.intent.value,
                    "count": incident.ticket_count,
                },
            )
    except Exception as e:
        logger.error("incident_detection_failed", extra={"error": str(e)})

    return PipelineResult(
        player_id=context.player_id,
        classification=classification,
        priority=priority,
        escalation=escalation,
        strategy=strategy,
        processing_time_ms=round(processing_time_ms, 2),
    )
