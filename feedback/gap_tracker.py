import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from dataclasses import dataclass, asdict

GAPS_FILE = Path(__file__).parent / "gaps.json"


@dataclass
class KnowledgeGap:
    id: str
    timestamp: str
    player_message: str
    classification_intent: str
    confidence: float
    retrieval_scores: list[float]  # Scores from RAG retrieval
    reason: str  # Why this was flagged as a gap


def _load_gaps() -> list[dict]:
    if not GAPS_FILE.exists():
        return []
    with open(GAPS_FILE, "r") as f:
        return json.load(f)


def _save_gaps(gaps: list[dict]) -> None:
    GAPS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(GAPS_FILE, "w") as f:
        json.dump(gaps, f, indent=2)


def record_gap(
    player_message: str,
    classification_intent: str,
    confidence: float,
    retrieval_scores: list[float] = None,
    reason: str = "low_confidence",
) -> KnowledgeGap:
    """
    Record a case where the assistant could not handle a ticket confidently.

    This is called when:
    - Classification confidence is below threshold
    - RAG retrieval returned no relevant results (all scores below minimum)
    - Intent was classified as UNKNOWN

    The gap log is the feedback mechanism for KB improvement.
    Reviewing it weekly shows what questions the KB does not cover.
    """
    gap = KnowledgeGap(
        id=str(uuid.uuid4())[:8],
        timestamp=datetime.now(timezone.utc).isoformat(),
        player_message=player_message,
        classification_intent=classification_intent,
        confidence=confidence,
        retrieval_scores=retrieval_scores or [],
        reason=reason,
    )

    gaps = _load_gaps()
    gaps.append(asdict(gap))
    _save_gaps(gaps)

    return gap


def get_gaps(limit: int = 50, reason_filter: str = None) -> list[dict]:
    """
    Retrieve recorded knowledge gaps.

    This is the GET /gaps equivalent.
    Returns most recent gaps first.
    """
    gaps = _load_gaps()

    if reason_filter:
        gaps = [g for g in gaps if g.get("reason") == reason_filter]

    # Most recent first
    gaps.sort(key=lambda g: g["timestamp"], reverse=True)
    return gaps[:limit]


def get_gap_summary() -> dict:
    """
    Summarise gaps by reason and intent for weekly review.
    """
    gaps = _load_gaps()
    if not gaps:
        return {"total": 0, "by_reason": {}, "by_intent": {}}

    by_reason: dict[str, int] = {}
    by_intent: dict[str, int] = {}

    for gap in gaps:
        r = gap.get("reason", "unknown")
        i = gap.get("classification_intent", "unknown")
        by_reason[r] = by_reason.get(r, 0) + 1
        by_intent[i] = by_intent.get(i, 0) + 1

    return {
        "total": len(gaps),
        "by_reason": dict(sorted(by_reason.items(), key=lambda x: x[1], reverse=True)),
        "by_intent": dict(sorted(by_intent.items(), key=lambda x: x[1], reverse=True)),
    }
