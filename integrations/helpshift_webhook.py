import os
import hmac
import hashlib
import logging
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from engine.pipeline import run, TicketContext
from engine.logging_config import configure_logging
from integrations.helpshift_client import (
    get_issue,
    get_author_profile,
    get_issue_count_for_player,
    map_issue_to_ticket_context,
    update_issue,
)

load_dotenv()
configure_logging(level="INFO")

logger = logging.getLogger(__name__)
app = Flask(__name__)

HELPSHIFT_WEBHOOK_SECRET = os.getenv("HELPSHIFT_WEBHOOK_SECRET", "")


def verify_helpshift_signature(req) -> bool:
    if not HELPSHIFT_WEBHOOK_SECRET:
        logger.warning("helpshift_webhook_secret_not_set - signature verification disabled")
        return True

    signature = req.headers.get("X-Helpshift-Signature", "")
    body = req.get_data(as_text=True)

    expected = hmac.new(
        HELPSHIFT_WEBHOOK_SECRET.encode(),
        body.encode(),
        hashlib.sha256,
    ).hexdigest()

    return hmac.compare_digest(signature, expected)


@app.route("/webhook/helpshift", methods=["POST"])
def helpshift_webhook():
    if not verify_helpshift_signature(request):
        logger.warning("helpshift_webhook_signature_invalid")
        return jsonify({"error": "Invalid signature"}), 401

    payload = request.get_json()
    if not payload:
        return jsonify({"error": "Empty payload"}), 400

    issue_id = payload.get("id") or payload.get("issue_id")
    if not issue_id:
        return jsonify({"error": "No issue ID in payload"}), 400

    logger.info("helpshift_webhook_received", extra={"issue_id": issue_id})

    try:
        issue = get_issue(issue_id)
        author = issue.get("author", {})
        author_id = str(author.get("id", ""))
        profile = get_author_profile(author_id) if author_id else {}
        contact_count = get_issue_count_for_player(author_id) if author_id else 1
    except Exception as e:
        logger.error("helpshift_fetch_failed", extra={"issue_id": issue_id, "error": str(e)})
        return jsonify({"error": "Failed to fetch issue data"}), 500

    ctx_kwargs = map_issue_to_ticket_context(issue, profile, contact_count)
    message = ctx_kwargs.get("message", "")
    if not message:
        logger.info("helpshift_issue_skipped_empty_message", extra={"issue_id": issue_id})
        return jsonify({"status": "skipped", "reason": "empty message"}), 200

    try:
        ctx = TicketContext(**ctx_kwargs)
        result = run(ctx)
    except Exception as e:
        logger.error("helpshift_pipeline_failed", extra={"issue_id": issue_id, "error": str(e)})
        return jsonify({"error": "Pipeline failed"}), 500

    try:
        success = update_issue(issue_id, result)
        if not success:
            logger.error("helpshift_update_failed", extra={"issue_id": issue_id})
            return jsonify({"error": "Failed to update issue"}), 500
    except Exception as e:
        logger.error("helpshift_update_error", extra={"issue_id": issue_id, "error": str(e)})
        return jsonify({"error": "Issue update error"}), 500

    logger.info(
        "helpshift_issue_triaged",
        extra={
            "issue_id": issue_id,
            "intent": result.classification.intent.value,
            "priority": result.priority.label,
            "escalate": result.escalation.should_escalate,
            "processing_ms": result.processing_time_ms,
        },
    )

    return jsonify({
        "status": "ok",
        "issue_id": issue_id,
        "intent": result.classification.intent.value,
        "confidence": result.classification.confidence,
        "priority": result.priority.label,
        "escalate": result.escalation.should_escalate,
        "team": result.escalation.team,
    }), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8001))
    app.run(host="0.0.0.0", port=port, debug=False)
