from __future__ import annotations
from datetime import datetime, timezone

def fetch_latest(limit: int = 10):
    now = datetime.now(timezone.utc).isoformat()
    items = [
        {
            "ioc": {"type": "email", "value": "alice@example.com"},
            "found_at": now,
            "source": {"source": "paste_site", "source_name": "demo-paste", "source_url": "https://paste.example/p/abc1"},
            "context": "demo leak"
        },
        {
            "ioc": {"type": "domain", "value": "leakycorp.test"},
            "found_at": now,
            "source": {"source": "paste_site", "source_name": "demo-paste", "source_url": "https://paste.example/p/abc2"},
            "context": "possible staging domain"
        },
        {
            "ioc": {"type": "token", "value": "sk-demo-123456"},
            "found_at": now,
            "source": {"source": "paste_site", "source_name": "demo-paste", "source_url": "https://paste.example/p/abc3"},
            "context": "token-looking string"
        }
    ]
    return items[:limit]
