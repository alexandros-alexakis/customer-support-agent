import os
import hashlib
import logging
from dataclasses import dataclass, asdict
from datetime import datetime, timezone, timedelta
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

MOCK_ACCOUNT_MODE = os.getenv("PLAYER_ACCOUNT_BACKEND", "mock") == "mock"

_DEVICES = [
    "iPhone 14 / iOS 17.2",
    "iPhone 13 / iOS 16.7",
    "Samsung Galaxy S23 / Android 14",
    "Samsung Galaxy A54 / Android 13",
    "Google Pixel 7 / Android 14",
    "iPad Air / iPadOS 17.1",
    "OnePlus 11 / Android 13",
    "Xiaomi 13 / Android 13",
]


@dataclass
class PlayerAccountContext:
    player_id: str
    join_date: str
    total_spend_usd: float
    last_active: str
    device: str
    previous_ticket_count: int
    vip_tier: Optional[str]
    account_age_days: int
    is_new_player: bool
    is_high_value: bool


def _mock_account(player_id: str) -> PlayerAccountContext:
    seed = hashlib.md5(player_id.encode()).digest()

    age_days = 30 + (seed[0] * 256 + seed[1]) % 1171
    join_date = (datetime.now(timezone.utc) - timedelta(days=age_days)).strftime("%Y-%m-%d")

    raw_spend = (seed[2] * 256 + seed[3]) / 65535
    total_spend_usd = round(raw_spend ** 2 * 500, 2)

    days_since_active = seed[4] % 30
    last_active = (datetime.now(timezone.utc) - timedelta(days=days_since_active)).strftime("%Y-%m-%d")

    device = _DEVICES[seed[5] % len(_DEVICES)]
    previous_ticket_count = seed[6] % 11

    vip_byte = seed[7]
    if vip_byte < 13:
        vip_tier = "platinum"
    elif vip_byte < 38:
        vip_tier = "gold"
    elif vip_byte < 90:
        vip_tier = "silver"
    else:
        vip_tier = None

    return PlayerAccountContext(
        player_id=player_id,
        join_date=join_date,
        total_spend_usd=total_spend_usd,
        last_active=last_active,
        device=device,
        previous_ticket_count=previous_ticket_count,
        vip_tier=vip_tier,
        account_age_days=age_days,
        is_new_player=age_days < 30,
        is_high_value=total_spend_usd >= 100,
    )


def get_account_context(player_id: str) -> Optional[PlayerAccountContext]:
    if not MOCK_ACCOUNT_MODE:
        logger.warning(
            "real_account_backend_not_implemented",
            extra={"player_id": player_id},
        )

    try:
        return _mock_account(player_id)
    except Exception as e:
        logger.error("account_context_failed", extra={"player_id": player_id, "error": str(e)})
        return None


def format_account_context_for_prompt(ctx: PlayerAccountContext) -> str:
    vip_label = f" [{ctx.vip_tier.upper()} VIP]" if ctx.vip_tier else ""
    high_value_label = " [HIGH VALUE]" if ctx.is_high_value else ""
    new_player_label = " [NEW PLAYER]" if ctx.is_new_player else ""

    return (
        f"PLAYER ACCOUNT CONTEXT:{vip_label}{new_player_label}\n"
        f"- Account age: {ctx.account_age_days} days (joined {ctx.join_date})\n"
        f"- Total spend: ${ctx.total_spend_usd:.2f}{high_value_label}\n"
        f"- Last active: {ctx.last_active}\n"
        f"- Device: {ctx.device}\n"
        f"- Previous tickets: {ctx.previous_ticket_count}\n"
        f"- VIP tier: {ctx.vip_tier or 'none'}\n"
    )
