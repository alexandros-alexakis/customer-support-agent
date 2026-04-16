import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional

FEEDBACK_FILE = Path(__file__).parent / "feedback.json"

# Corrections with this priority are checked first during retrieval
CORRECTION_PRIORITY = {
    "critical": 1,   # Wrong escalation, hallucinated policy, safety issue
    "high": 2,       # Incorrect information given to player
    "standard": 3,   # Tone or format issue
}


@dataclass
class FeedbackRecord:
    id: str
    timestamp: str
    player_message: str
    agent_response: str
    correct_response: Optional[str]   # What should have been said
    issue_type: str                    # e.g. "wrong_escalation", "hallucinated_policy"
    priority: str                      # critical / high / standard
    reviewed_by: str                   # Who submitted the correction
    notes: str


def _load_feedback() -> list[dict]:
    if not FEEDBACK_FILE.exists():
        return []
    with open(FEEDBACK_FILE, "r") as f:
        return json.load(f)


def _save_feedback(records: list[dict]) -> None:
    FEEDBACK_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(FEEDBACK_FILE, "w") as f:
        json.dump(records, f, indent=2)


def record_feedback(
    player_message: str,
    agent_response: str,
    issue_type: str,
    priority: str = "standard",
    correct_response: str = None,
    reviewed_by: str = "qa_reviewer",
    notes: str = "",
) -> FeedbackRecord:
    """
    Record a correction to an agent response.

    This is the POST /feedback equivalent.

    issue_type options:
    - wrong_escalation: ticket escalated to wrong team or not escalated when it should be
    - hallucinated_policy: agent stated policy not in knowledge base
    - incorrect_information: factually wrong information given
    - tone_failure: response tone was inappropriate
    - premature_closure: ticket closed before resolution confirmed
    - over_questioning: too many clarifying questions asked

    Corrections are used in two ways:
    1. Direct KB improvement: if a gap is identified, update the relevant KB file
    2. Prompt review: if a rule was violated, tighten the system prompt rule
    """
    if priority not in CORRECTION_PRIORITY:
        priority = "standard"

    record = FeedbackRecord(
        id=str(uuid.uuid4())[:8],
        timestamp=datetime.now(timezone.utc).isoformat(),
        player_message=player_message,
        agent_response=agent_response,
        correct_response=correct_response,
        issue_type=issue_type,
        priority=priority,
        reviewed_by=reviewed_by,
        notes=notes,
    )

    records = _load_feedback()
    records.append(asdict(record))
    _save_feedback(records)

    return record


def get_feedback(
    priority_filter: str = None,
    issue_type_filter: str = None,
    limit: int = 50,
) -> list[dict]:
    """
    Retrieve feedback records, optionally filtered.
    Critical priority records are always returned first.
    """
    records = _load_feedback()

    if priority_filter:
        records = [r for r in records if r.get("priority") == priority_filter]
    if issue_type_filter:
        records = [r for r in records if r.get("issue_type") == issue_type_filter]

    # Sort: critical first, then by timestamp
    records.sort(
        key=lambda r: (
            CORRECTION_PRIORITY.get(r.get("priority", "standard"), 99),
            r["timestamp"],
        )
    )

    return records[:limit]


def get_feedback_summary() -> dict:
    """
    Summary of recorded feedback for weekly QA review.
    """
    records = _load_feedback()
    if not records:
        return {"total": 0, "by_priority": {}, "by_issue_type": {}}

    by_priority: dict[str, int] = {}
    by_issue_type: dict[str, int] = {}

    for r in records:
        p = r.get("priority", "unknown")
        i = r.get("issue_type", "unknown")
        by_priority[p] = by_priority.get(p, 0) + 1
        by_issue_type[i] = by_issue_type.get(i, 0) + 1

    return {
        "total": len(records),
        "by_priority": by_priority,
        "by_issue_type": dict(
            sorted(by_issue_type.items(), key=lambda x: x[1], reverse=True)
        ),
    }
