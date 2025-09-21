from __future__ import annotations
from typing import Optional

def lookup_domain(domain: str) -> Optional[str]:
    """
    Stub WHOIS lookup.
    Return a fake registrar so the pipeline can run without network calls.
    """
    if domain.endswith(".test"):
        return "Test Registry"
    if domain.endswith("example.com"):
        return "IANA Example Registrar"
    return "Unknown"
