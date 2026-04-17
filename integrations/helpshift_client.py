import os
import logging
import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

HELPSHIFT_API_KEY = os.getenv("HELPSHIFT_API_KEY", "")
HELPSHIFT_DOMAIN = os.getenv("HELPSHIFT_DOMAIN", "")
HELPSHIFT_BASE_URL = f"https://api.helpshift.com/v1/{HELPSHIFT_DOMAIN}"


def _auth() -> tuple:
    return (HELPSHIFT_API_KEY, "")


def get_issue(issue_id: str) -> dict:
    url = f"{HELPSHIFT_BASE_URL}/issues/{issue_id}"
    response = requests.get(url, auth=_auth())
    response.raise_for_status()
    return response.json().get("issue", response.json())


def get_author_profile(author_id: str) -> dict:
    try:
        url = f"{HELPSHIFT_BASE_URL}/profiles/{author_id}"
        response = requests.get(url, auth=_auth())
        response.raise_for_status()
        return response.json().get("profile", response.json())
    except Exception as e:
        logger.warning("helpshift_profile_fetch_failed", extra={"author_id": author_id, "error": str(e)})
        return {}


def get_issue_count_for_player(author_id: str) -> int:
    try:
        url = f"{HELPSHIFT_BASE_URL}/issues"
        response = requests.get(url, auth=_auth(), params={"author_id": author_id, "state": "any"})
        if response.status_code != 200:
            return 1
        data = response.json()
        return data.get("total_hits", data.get("count", 1))
    except Exception:
        return 1


def is_vip(profile: dict) -> bool:
    return "vip" in [t.lower() for t in profile.get("tags", [])]


def map_issue_to_ticket_context(issue: dict, profile: dict, contact_count: int) -> dict:
    messages = issue.get("messages", [])
    message_body = ""
    for msg in messages:
        if msg.get("origin") in ("player", "end-user", "user"):
            message_body = msg.get("body", "")
            break
    if not message_body and messages:
        message_body = messages[0].get("body", "")

    author = issue.get("author", {})
    player_id = str(author.get("id", issue.get("id", "unknown")))

    return {
        "message": message_body.strip(),
        "player_id": player_id,
        "contact_count": contact_count,
        "is_vip": is_vip(profile),
    }


def update_issue(issue_id: str, pipeline_result) -> bool:
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

    tags = [f"ai_{c.intent.value}"]
    tags += [f"ai_flag_{flag}" for flag in c.flags]
    if e.should_escalate:
        tags.append(f"ai_route_{e.team}")

    try:
        note_url = f"{HELPSHIFT_BASE_URL}/issues/{issue_id}/messages"
        note_payload = {"body": "\n".join(note_lines), "type": "note"}
        note_resp = requests.post(note_url, auth=_auth(), json=note_payload)
        note_ok = note_resp.status_code in (200, 201)
    except Exception as e:
        logger.error("helpshift_note_failed", extra={"issue_id": issue_id, "error": str(e)})
        note_ok = False

    try:
        tag_url = f"{HELPSHIFT_BASE_URL}/issues/{issue_id}"
        tag_payload = {"tags": tags}
        tag_resp = requests.patch(tag_url, auth=_auth(), json=tag_payload)
        tag_ok = tag_resp.status_code in (200, 201)
    except Exception as e:
        logger.error("helpshift_tag_failed", extra={"issue_id": issue_id, "error": str(e)})
        tag_ok = False

    return note_ok and tag_ok
