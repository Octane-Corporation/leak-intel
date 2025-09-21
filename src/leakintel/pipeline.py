from __future__ import annotations
from typing import List, Tuple
from hashlib import sha256
from datetime import datetime
from .models import LeakItem, IOC, SourceMeta
from .collectors import paste_sites
from .enrichment import whois as whois_enr
from .enrichment import scoring as scoring_mod

def _make_id(ioc_value: str, source_url: str) -> str:
    return sha256(f"{ioc_value}|{source_url}".encode("utf-8")).hexdigest()[:16]

def run_once(limit: int = 10) -> List[LeakItem]:
    """Collect -> normalize -> enrich -> score. Returns a list of LeakItem."""
    raw_items = paste_sites.fetch_latest(limit=limit)
    seen: set[Tuple[str, str]] = set()
    results: List[LeakItem] = []
    for r in raw_items:
        ioc_data = r["ioc"]
        ioc = IOC(type=ioc_data["type"], value=ioc_data["value"])

        src = r.get("source", {})
        source = SourceMeta(
            source=src.get("source", "paste_site"),
            source_name=src.get("source_name"),
            source_url=src.get("source_url"),
        )

        # found_at may be ISO with Z; normalize
        found_at = datetime.fromisoformat(str(r["found_at"]).replace("Z", "+00:00"))

        # dedup by (ioc_value, source_url)
        key = (ioc.value, source.source_url or "")
        if key in seen:
            continue
        seen.add(key)

        registrar = None
        domain_for_lookup = None
        if ioc.type == "email" and "@" in ioc.value:
            domain_for_lookup = ioc.value.split("@", 1)[1]
        elif ioc.type == "domain":
            domain_for_lookup = ioc.value
        if domain_for_lookup:
            registrar = whois_enr.lookup_domain(domain_for_lookup)

        leak = LeakItem(
            id=_make_id(ioc.value, source.source_url or ""),
            ioc=ioc,
            context=r.get("context"),
            found_at=found_at,
            source=source,
            whois_registrar=registrar,
            score=0.0,
        )
        leak.score = scoring_mod.score(leak)
        results.append(leak)

    return results
