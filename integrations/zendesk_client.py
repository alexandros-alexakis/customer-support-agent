import os
import requests
from dotenv import load_dotenv

load_dotenv()

ZENDESK_SUBDOMAIN = os.getenv("ZENDESK_SUBDOMAIN")
ZENDESK_EMAIL = os.getenv("ZENDESK_EMAIL")
ZENDESK_API_TOKEN = os.getenv("ZENDESK_API_TOKEN")
ZENDESK_BASE_URL = f"https://{ZENDESK_SUBDOMAIN}.zendesk.com/api/v2"


def _auth():
    return (f"{ZENDESK_EMAIL}/token", ZENDESK_API_TOKEN)


def get_ticket(ticket_id: int) -> dict:
    """
    Fetch full ticket details from Zendesk.
    The webhook payload is minimal - we fetch the rest here.
    """
    url = f"{ZENDESK_BASE_URL}/tickets/{ticket_id}.json"
    response = requests.get(url, auth=_auth())
    response.raise_for_status()
    return response.json()["ticket"]


def get_user(user_id: int) -> dict:
    """
    Fetch user profile. Used to check VIP status and identity.
    """
    url = f"{ZENDESK_BASE_URL}/users/{user_id}.json"
    response = requests.get(url, auth=_auth())
    response.raise_for_status()
    return response.json()["user"]


def get_contact_count(user_id: int) -> int:
    """
    Count total tickets submitted by this user.
    Used to detect repeat contacts before the pipeline runs.
    """
    url = f"{ZENDESK_BASE_URL}/users/{user_id}/tickets/requested.json"
    response = requests.get(url, auth=_auth())
    if response.status_code != 200:
        return 1  # Safe default - treat as first contact if lookup fails
    return response.json().get("count", 1)


def is_vip(user: dict) -> bool:
    """
    Check for VIP tag on user profile.
    Add the 'vip' tag to a user in Zendesk to mark them as VIP.
    """
    return "vip" in user.get("tags", [])


def update_ticket(ticket_id: int, pipeline_result) -> bool:
    """
    Write triage results back to the Zendesk ticket.

    Adds:
    - Internal note with full triage summary (not visible to player)
    - Priority level
    - AI-generated tags for intent and flags

    Does NOT:
    - Change ticket status
    - Send any message to the player
    - Assign to a specific agent (only tags the team)
    """
    c = pipeline_result.classification
    p = pipeline_result.priority
    e = pipeline_result.escalation
    s = pipeline_result.strategy

    note_lines = [
        "**AI Triage Result**",
        f"- Intent: {c.intent.value} (confidence: {c.confidence})",
        f"- Tone: {c.tone.value}",
        f"- Priority: {p.label} (P{p.score}) | SLA: {p.sla_hours}h",
        f"- Escalate: {'Yes' if e.should_escalate else 'No'} -> {e.team}",
        f"- Reason: {e.reason}",
        f"- Flags: {', '.join(c.flags) if c.flags else 'none'}",
        "",
        f"**Recommended action:** {s.action}",
        f"**Collect from player:** {', '.join(s.collect)}",
        f"**Tone guidance:** {s.tone_instruction}",
        "",
        f"*Auto-generated. Review before acting. Processing time: {pipeline_result.processing_time_ms}ms*",
    ]

    zendesk_priority_map = {
        1: "low",
        2: "normal",
        3: "high",
        4: "urgent",
        5: "urgent",
    }

    tags = [f"ai_{c.intent.value}"]
    tags += [f"ai_flag_{flag}" for flag in c.flags]
    if e.should_escalate:
        tags.append(f"ai_route_{e.team}")

    payload = {
        "ticket": {
            "priority": zendesk_priority_map.get(p.score, "normal"),
            "tags": tags,
            "comment": {
                "body": "\n".join(note_lines),
                "public": False,
            },
        }
    }

    url = f"{ZENDESK_BASE_URL}/tickets/{ticket_id}.json"
    response = requests.put(url, json=payload, auth=_auth())
    return response.status_code == 200
