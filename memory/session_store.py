import json
import uuid
import logging
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger(__name__)

SESSIONS_DIR = Path(__file__).parent / "sessions"
MAX_HISTORY_TURNS = 10


def _session_path(player_id: str) -> Path:
    safe_id = player_id.replace("/", "_").replace("\\", "_")
    return SESSIONS_DIR / f"{safe_id}.json"


def _load_session_raw(player_id: str) -> dict:
    path = _session_path(player_id)
    if not path.exists():
        return {"player_id": player_id, "created_at": "", "updated_at": "", "turns": []}
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        logger.error("session_load_failed", extra={"player_id": player_id, "error": str(e)})
        return {"player_id": player_id, "created_at": "", "updated_at": "", "turns": []}


def load_session(player_id: str) -> dict:
    return _load_session_raw(player_id)


def save_session(player_id: str, turns: list[dict]) -> None:
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
    trimmed = turns[-MAX_HISTORY_TURNS:]
    existing = _load_session_raw(player_id)
    now = datetime.now(timezone.utc).isoformat()
    data = {
        "player_id": player_id,
        "created_at": existing.get("created_at") or now,
        "updated_at": now,
        "turns": trimmed,
    }
    try:
        with open(_session_path(player_id), "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        logger.error("session_save_failed", extra={"player_id": player_id, "error": str(e)})


def append_turn(player_id: str, role: str, content: str) -> None:
    session = _load_session_raw(player_id)
    turn = {
        "role": role,
        "content": content,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    turns = session.get("turns", [])
    turns.append(turn)
    save_session(player_id, turns)


def get_history_for_prompt(player_id: str) -> list[dict]:
    session = _load_session_raw(player_id)
    turns = session.get("turns", [])[-MAX_HISTORY_TURNS:]
    return [{"role": t["role"], "content": t["content"]} for t in turns]


def clear_session(player_id: str) -> None:
    path = _session_path(player_id)
    try:
        if path.exists():
            path.unlink()
    except Exception as e:
        logger.error("session_clear_failed", extra={"player_id": player_id, "error": str(e)})
