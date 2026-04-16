import os
import hmac
import hashlib
import logging
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from engine.pipeline import run, TicketContext
from engine.logging_config import configure_logging
from integrations.zendesk_client import (
    get_ticket,
    get_user,
    get_contact_count,
    is_vip,
    update_ticket,
)

load_dotenv()
configure_logging(level="INFO")

logger = logging.getLogger(__name__)
app = Flask(__name__)

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "")


def verify_signature(req) -> bool:
    """
    Verify Zendesk HMAC-SHA256 webhook signature.
    Never skip this in production - it prevents spoofed requests.
    Set WEBHOOK_SECRET in .env to enable. Leave empty to skip (dev only).
    """
    if not WEBHOOK_SECRET:
        logger.warning("webhook_secret_not_set - signature verification disabled")
        return True

    signature = req.headers.get("X-Zendesk-Webhook-Signature", "")
    timestamp = req.headers.get("X-Zendesk-Webhook-Signature-Timestamp", "")
    body = req.get_data(as_text=True)

    expected = hmac.new(
        WEBHOOK_SECRET.encode(),
        f"{timestamp}{body}".encode(),
        hashlib.sha256,
    ).hexdigest()

    return hmac.compare_digest(signature, expected)


@app.route("/webhook/zendesk", methods=["POST"])
def zendesk_webhook():
    """
    Receives new ticket events from Zendesk.
    Runs the triage pipeline and writes results back to the ticket.
    """
    if not verify_signature(request):
        logger.warning("webhook_signature_invalid")
        return jsonify({"error": "Invalid signature"}), 401

    payload = request.get_json()
    if not payload:
        return jsonify({"error": "Empty payload"}), 400

    ticket_id = payload.get("ticket_id") or payload.get("id")
    if not ticket_id:
        return jsonify({"error": "No ticket ID in payload"}), 400

    logger.info("webhook_received", extra={"ticket_id": ticket_id})

    # Fetch full context from Zendesk
    try:
        ticket = get_ticket(ticket_id)
        user = get_user(ticket["requester_id"])
        contact_count = get_contact_count(ticket["requester_id"])
        vip = is_vip(user)
    except Exception as e:
        logger.error("zendesk_fetch_failed", extra={"ticket_id": ticket_id, "error": str(e)})
        return jsonify({"error": "Failed to fetch ticket data"}), 500

    message = ticket.get("description", "").strip()
    if not message:
        logger.info("ticket_skipped_empty_message", extra={"ticket_id": ticket_id})
        return jsonify({"status": "skipped", "reason": "empty message"}), 200

    # Run triage pipeline
    try:
        ctx = TicketContext(
            message=message,
            player_id=str(ticket["requester_id"]),
            contact_count=contact_count,
            is_vip=vip,
        )
        result = run(ctx)
    except Exception as e:
        logger.error("pipeline_failed", extra={"ticket_id": ticket_id, "error": str(e)})
        return jsonify({"error": "Pipeline failed"}), 500

    # Write results back to Zendesk
    try:
        success = update_ticket(ticket_id, result)
        if not success:
            logger.error("zendesk_update_failed", extra={"ticket_id": ticket_id})
            return jsonify({"error": "Failed to update ticket"}), 500
    except Exception as e:
        logger.error("zendesk_update_error", extra={"ticket_id": ticket_id, "error": str(e)})
        return jsonify({"error": "Ticket update error"}), 500

    logger.info(
        "ticket_triaged",
        extra={
            "ticket_id": ticket_id,
            "intent": result.classification.intent.value,
            "priority": result.priority.label,
            "escalate": result.escalation.should_escalate,
            "processing_ms": result.processing_time_ms,
        },
    )

    return jsonify({
        "status": "ok",
        "ticket_id": ticket_id,
        "intent": result.classification.intent.value,
        "confidence": result.classification.confidence,
        "priority": result.priority.label,
        "escalate": result.escalation.should_escalate,
        "team": result.escalation.team,
    }), 200


@app.route("/health", methods=["GET"])
def health():
    """Health check. Used by uptime monitors."""
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=False)
