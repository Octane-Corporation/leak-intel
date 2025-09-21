from __future__ import annotations
from typing import Optional, Literal
from datetime import datetime
from pydantic import BaseModel, Field

class SourceMeta(BaseModel):
    """Where we found the item."""
    source: Literal["paste_site", "github", "public_dump", "other"] = "paste_site"
    source_name: Optional[str] = None
    source_url: Optional[str] = None

class IOC(BaseModel):
    """Indicator of compromise."""
    type: Literal["email", "domain", "token", "api_key", "ip"]
    value: str

class LeakItem(BaseModel):
    """A normalized leak record."""
    id: str = Field(..., description="Deterministic ID (hash of IOC+source)")
    ioc: IOC
    context: Optional[str] = None
    found_at: datetime
    source: SourceMeta
    whois_registrar: Optional[str] = None
    score: float = 0.0
