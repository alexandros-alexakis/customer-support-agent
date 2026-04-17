import json
import uuid
import logging
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

INCIDENTS_FILE = Path(__file__).parent / "incidents.json"
INCIDENT_WINDOW_MINUTES = 15
INCIDENT_THRESHOLD = 3


@dataclass
class IncidentRecord:
    incident_id: str
    first_seen: str
    last_updated: str
    intent: str
    keyword_signal: str
    ticket_ids: list
    ticket_count: int
    status: str
    notes: str


def _load_incidents() -> list[dict]:
    if not INCIDENTS_FILE.exists():
        return []
    try:
        with open(INCIDENTS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []


def _save_incidents(records: list[dict]) -> None:
    INCIDENTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(INCIDENTS_FILE, "w") as f:
        json.dump(records, f, indent=2)


def _extract_keyword_signal(messages: list[str]) -> str:
    try:
        from engine.classifier import INTENT_SIGNALS
        counts: dict[str, int] = {}
        combined = " ".join(messages).lower()
        for signals in INTENT_SIGNALS.values():
            for signal in signals:
                if signal in combined:
                    counts[signal] = counts.get(signal, 0) + combined.count(signal)
        if counts:
            return max(counts, key=lambda k: counts[k])
    except Exception:
        pass
    return "unknown"


def record_ticket_for_correlation(
    player_id: str,
    intent: str,
    message: str,
    ticket_id: str = None,
) -> Optional[IncidentRecord]:
    now = datetime.now(timezone.utc)
    window_start = now - timedelta(minutes=INCIDENT_WINDOW_MINUTES)
    tid = ticket_id or player_id

    records = _load_incidents()

    matched_idx = None
    for i, rec in enumerate(records):
        if rec["intent"] != intent:
            continue
        if rec["status"] == "resolved":
            continue
        try:
            last_updated = datetime.fromisoformat(rec["last_updated"])
        except Exception:
            continue
        if last_updated >= window_start:
            matched_idx = i
            break

    if matched_idx is not None:
        rec = records[matched_idx]
        if tid not in rec["ticket_ids"]:
            rec["ticket_ids"].append(tid)
            rec["ticket_count"] = len(rec["ticket_ids"])
        rec["last_updated"] = now.isoformat()
        if rec["ticket_count"] >= INCIDENT_THRESHOLD and rec["status"] == "pending":
            rec["status"] = "open"
            all_messages = [message]
            rec["keyword_signal"] = _extract_keyword_signal(all_messages)
            logger.warning(
                "incident_threshold_reached",
                extra={"incident_id": rec["incident_id"], "intent": intent, "count": rec["ticket_count"]},
            )
    else:
        new_rec = IncidentRecord(
            incident_id="INC-" + str(uuid.uuid4())[:6].upper(),
            first_seen=now.isoformat(),
            last_updated=now.isoformat(),
            intent=intent,
            keyword_signal=_extract_keyword_signal([message]),
            ticket_ids=[tid],
            ticket_count=1,
            status="pending",
            notes="",
        )
        records.append(asdict(new_rec))
        matched_idx = len(records) - 1

    _save_incidents(records)

    rec = records[matched_idx]
    if rec["status"] == "open":
        return IncidentRecord(**rec)
    return None


def get_active_incidents() -> list[dict]:
    records = _load_incidents()
    active = [r for r in records if r.get("status") == "open"]
    active.sort(key=lambda r: r.get("last_updated", ""), reverse=True)
    return active


def resolve_incident(incident_id: str, notes: str = "") -> bool:
    records = _load_incidents()
    for rec in records:
        if rec["incident_id"] == incident_id:
            rec["status"] = "resolved"
            rec["notes"] = notes
            rec["last_updated"] = datetime.now(timezone.utc).isoformat()
            _save_incidents(records)
            return True
    return False


def get_incident_summary() -> dict:
    records = _load_incidents()
    by_intent: dict[str, int] = {}
    status_counts = {"open": 0, "pending": 0, "resolved": 0}

    for r in records:
        intent = r.get("intent", "unknown")
        by_intent[intent] = by_intent.get(intent, 0) + 1
        s = r.get("status", "pending")
        status_counts[s] = status_counts.get(s, 0) + 1

    return {
        "total": len(records),
        "open": status_counts.get("open", 0),
        "resolved": status_counts.get("resolved", 0),
        "by_intent": by_intent,
    }
