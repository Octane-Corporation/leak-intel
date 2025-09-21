from __future__ import annotations
from datetime import datetime, timezone
from ..models import LeakItem

WEIGHTS = {"token": 70, "api_key": 65, "email": 50, "domain": 35, "ip": 30}

def score(item: LeakItem) -> float:
    base = WEIGHTS.get(item.ioc.type, 25)
    now = datetime.now(timezone.utc)
    age_days = max(0.0, (now - item.found_at).total_seconds() / 86400.0)
    recency_bonus = max(0.0, 20.0 * (1 - min(age_days / 7.0, 1.0)))
    token_bonus = 10.0 if item.ioc.type in {"token", "api_key"} else 0.0
    return round(min(100.0, base + recency_bonus + token_bonus), 2)
