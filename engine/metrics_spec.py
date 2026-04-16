"""
Key metrics this system should track in production.

These are not implemented here as a metrics library (Prometheus, Datadog, etc.)
will vary by deployment. This file documents WHAT to measure and WHY,
so the metrics layer can be wired in without guessing.
"""

METRICS_SPEC = {
    "ticket_classification_confidence": {
        "type": "histogram",
        "description": "Distribution of classification confidence scores.",
        "why": "A drop in average confidence signals the classifier is seeing messages it wasn't designed for. Early warning for knowledge base gaps or new player behaviour patterns.",
        "alert_threshold": "p50 confidence below 0.6 for 30+ minutes",
    },
    "escalation_rate": {
        "type": "gauge",
        "description": "Percentage of tickets escalated vs handled at Tier 1.",
        "why": "Escalation rate is a proxy for classifier effectiveness and knowledge base coverage. Rising escalation rate = system is struggling.",
        "alert_threshold": "Above 35% for 1+ hour",
    },
    "unknown_intent_rate": {
        "type": "gauge",
        "description": "Percentage of tickets classified as UNKNOWN intent.",
        "why": "UNKNOWN means we had no signal. These tickets always go to human review. A spike means a new ticket type is emerging that isn't covered.",
        "alert_threshold": "Above 15% for 30+ minutes",
    },
    "priority_distribution": {
        "type": "histogram",
        "description": "Distribution of ticket priority scores (1-5).",
        "why": "Sudden shift toward higher priorities could indicate an incident or player sentiment event. Useful leading indicator.",
        "alert_threshold": "Critical (P5) tickets above 5% of volume",
    },
    "pipeline_processing_time_ms": {
        "type": "histogram",
        "description": "End-to-end processing time for the pipeline.",
        "why": "The pipeline should be fast. If it's slow, something is wrong with the classifier or a downstream call is hanging.",
        "alert_threshold": "p95 above 500ms",
    },
    "churn_risk_rate": {
        "type": "gauge",
        "description": "Percentage of tickets flagged as churn risk.",
        "why": "Churn risk signals are leading indicators of player loss. A spike warrants immediate game or ops team attention.",
        "alert_threshold": "Above 8% for 1+ hour",
    },
    "repeat_contact_rate": {
        "type": "gauge",
        "description": "Percentage of tickets from players contacting for the second or third time.",
        "why": "High repeat contact rate means issues aren't being resolved on first contact. Directly impacts FCR metric.",
        "alert_threshold": "Above 20%",
    },
}
