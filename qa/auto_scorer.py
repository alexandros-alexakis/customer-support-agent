import json
import uuid
import random
import logging
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from llm_client import generate_response, MOCK_MODE

logger = logging.getLogger(__name__)

QA_SCORES_FILE = Path(__file__).parent / "scores.json"
SAMPLE_RATE = 0.1

_RUBRIC = """
You are a QA evaluator for a customer support team. Score the agent response below using this rubric.
Return ONLY a JSON object — no prose, no explanation.

RUBRIC:
1. tone (0-20): 18-20=warm/professional/empathetic; 14-17=appropriate minor lapses; 10-13=neutral/robotic; 5-9=cold/dismissive; 0-4=rude/inappropriate
2. accuracy (0-30): 27-30=fully accurate no violations; 22-26=minor inaccuracy no impact; 15-21=partial inaccuracy; 8-14=significant inaccuracy/policy breach; 0-7=multiple errors/serious violation
3. resolution (0-25): 23-25=fully resolved or correctly escalated; 18-22=mostly resolved minor gaps; 12-17=partial/incorrect escalation; 6-11=not resolved/escalation missed; 0-5=no attempt
4. clarity (0-15): 14-15=clear concise well-structured; 11-13=mostly clear; 7-10=some unclear language; 3-6=hard to follow; 0-2=incomprehensible
5. escalation (0-10): 9-10=correct escalation all info collected player informed; 7-8=correct minor gap; 4-6=triggered but missing info; 1-3=wrong routing; 0=missed required escalation or unnecessary

FATAL ERRORS (set fatal_error=true, fatal_reason=description if any apply):
- Asked player for their password
- Promised refund/compensation without authorization
- Disclosed another player's account information
- Used abusive or discriminatory language
- Failed to escalate a security or fraud issue

Return exactly this JSON shape:
{"tone": 0, "accuracy": 0, "resolution": 0, "clarity": 0, "escalation": 0, "fatal_error": false, "fatal_reason": null}
"""

_MOCK_SCORES = {"tone": 15, "accuracy": 22, "resolution": 18, "clarity": 11, "escalation": 7}
_BANDS = [(90, "Excellent"), (75, "Good"), (60, "Needs Improvement"), (0, "Critical")]


@dataclass
class QAScore:
    id: str
    timestamp: str
    player_message: str
    agent_response: str
    intent: str
    scores: dict
    total: int
    band: str
    fatal_error: bool
    fatal_reason: Optional[str]
    is_mock: bool


def _load_scores() -> list[dict]:
    if not QA_SCORES_FILE.exists():
        return []
    try:
        with open(QA_SCORES_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []


def _save_scores(records: list[dict]) -> None:
    QA_SCORES_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(QA_SCORES_FILE, "w") as f:
        json.dump(records, f, indent=2)


def _band(total: int) -> str:
    for threshold, label in _BANDS:
        if total >= threshold:
            return label
    return "Critical"


def _parse_score_response(raw: str) -> dict:
    try:
        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start == -1 or end == 0:
            raise ValueError("no JSON found")
        parsed = json.loads(raw[start:end])
        maxes = {"tone": 20, "accuracy": 30, "resolution": 25, "clarity": 15, "escalation": 10}
        for k, max_val in maxes.items():
            parsed[k] = max(0, min(int(parsed.get(k, 0)), max_val))
        return parsed
    except Exception as e:
        logger.warning("qa_score_parse_failed", extra={"error": str(e)})
        return {**{k: 0 for k in ["tone", "accuracy", "resolution", "clarity", "escalation"]},
                "fatal_error": False, "fatal_reason": None}


def score_response(
    player_message: str,
    agent_response: str,
    intent: str = "unknown",
) -> QAScore:
    if MOCK_MODE:
        scores = _MOCK_SCORES.copy()
        fatal_error = False
        fatal_reason = None
        is_mock = True
    else:
        prompt = (
            f"{_RUBRIC}\n\n"
            f"INTENT: {intent}\n\n"
            f"PLAYER MESSAGE:\n{player_message}\n\n"
            f"AGENT RESPONSE:\n{agent_response}"
        )
        raw, is_mock = generate_response(prompt, intent="unknown")
        parsed = _parse_score_response(raw)
        scores = {k: parsed[k] for k in ["tone", "accuracy", "resolution", "clarity", "escalation"]}
        fatal_error = bool(parsed.get("fatal_error", False))
        fatal_reason = parsed.get("fatal_reason")

    total = 0 if fatal_error else sum(scores.values())
    band = "Critical" if fatal_error else _band(total)

    qa = QAScore(
        id=str(uuid.uuid4())[:8],
        timestamp=datetime.now(timezone.utc).isoformat(),
        player_message=player_message,
        agent_response=agent_response,
        intent=intent,
        scores=scores,
        total=total,
        band=band,
        fatal_error=fatal_error,
        fatal_reason=fatal_reason,
        is_mock=is_mock,
    )

    records = _load_scores()
    records.append(asdict(qa))
    _save_scores(records)

    return qa


def score_batch_from_file(
    input_path: str,
    sample_rate: float = SAMPLE_RATE,
    output_path: str = None,
) -> dict:
    with open(input_path, "r") as f:
        items = json.load(f)

    sample_size = max(1, int(len(items) * sample_rate))
    sample = random.sample(items, min(sample_size, len(items)))
    skipped = len(items) - len(sample)

    for item in sample:
        score_response(
            player_message=item.get("player_message", ""),
            agent_response=item.get("agent_response", ""),
            intent=item.get("intent", "unknown"),
        )

    summary = get_score_summary()
    summary["scored"] = len(sample)
    summary["skipped"] = skipped
    return summary


def get_score_summary() -> dict:
    records = _load_scores()
    if not records:
        return {"total_scored": 0, "avg_total": 0.0, "band_distribution": {},
                "avg_by_category": {}, "fatal_errors": 0}

    totals = [r["total"] for r in records]
    band_dist: dict[str, int] = {}
    cat_sums: dict[str, float] = {"tone": 0, "accuracy": 0, "resolution": 0,
                                   "clarity": 0, "escalation": 0}
    fatal_count = 0

    for r in records:
        band_dist[r["band"]] = band_dist.get(r["band"], 0) + 1
        if r.get("fatal_error"):
            fatal_count += 1
        for k in cat_sums:
            cat_sums[k] += r.get("scores", {}).get(k, 0)

    n = len(records)
    return {
        "total_scored": n,
        "avg_total": round(sum(totals) / n, 1),
        "band_distribution": band_dist,
        "avg_by_category": {k: round(v / n, 1) for k, v in cat_sums.items()},
        "fatal_errors": fatal_count,
    }
