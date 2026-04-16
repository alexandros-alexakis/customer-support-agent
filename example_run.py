"""
Example: run a ticket through the full pipeline.

This is a development/testing script, not a production entrypoint.
In production, the pipeline would be called from your support platform webhook handler.
"""
from engine.logging_config import configure_logging
from engine.pipeline import run, TicketContext

configure_logging(level="INFO")

# Example tickets to demonstrate the pipeline
examples = [
    TicketContext(
        message="I was charged $9.99 for coins but they never appeared in my account. Transaction ID: TXN-884521",
        player_id="player_001",
        contact_count=1,
        is_vip=False,
    ),
    TicketContext(
        message="This is the THIRD time I've contacted you about this and nothing has been fixed. I want a refund NOW.",
        player_id="player_002",
        contact_count=3,
        is_vip=False,
        prior_resolution_attempted=True,
    ),
    TicketContext(
        message="I'm done with this game. Uninstalling. Complete waste of money.",
        player_id="player_003",
        contact_count=1,
        is_vip=True,
    ),
    TicketContext(
        message="I will take legal action if my account isn't unbanned within 24 hours.",
        player_id="player_004",
        contact_count=1,
        is_vip=False,
    ),
]

for ctx in examples:
    print(f"\n{'='*60}")
    print(f"Player: {ctx.player_id}")
    print(f"Message: {ctx.message[:80]}..." if len(ctx.message) > 80 else f"Message: {ctx.message}")
    print(f"Contact count: {ctx.contact_count} | VIP: {ctx.is_vip}")
    print("-"*60)

    result = run(ctx)

    print(f"Intent:      {result.classification.intent.value} (confidence: {result.classification.confidence})")
    print(f"Tone:        {result.classification.tone.value}")
    print(f"Flags:       {result.classification.flags}")
    print(f"Priority:    {result.priority.label} (P{result.priority.score}) - SLA: {result.priority.sla_hours}h")
    print(f"Escalate:    {result.escalation.should_escalate} -> {result.escalation.team}")
    print(f"Reason:      {result.escalation.reason}")
    print(f"Strategy:    {result.strategy.action[:100]}")
    print(f"Collect:     {result.strategy.collect}")
    print(f"Processed:   {result.processing_time_ms}ms")
