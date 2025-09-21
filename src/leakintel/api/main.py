from typing import List, Optional
from fastapi import FastAPI, Query
from ..models import LeakItem
from ..pipeline import run_once

app = FastAPI(title="Leak Intel API")

@app.on_event("startup")
def load_data() -> None:
    app.state.items = run_once(limit=10)

@app.get("/health")
def health() -> dict:
    return {"status": "ok", "items_loaded": len(getattr(app.state, "items", []))}

@app.get("/search", response_model=List[LeakItem])
def search(q: Optional[str] = Query(default=None, description="Search IOC value or context")) -> List[LeakItem]:
    items: List[LeakItem] = getattr(app.state, "items", [])
    if not q:
        return items
    ql = q.lower()
    return [it for it in items if (ql in it.ioc.value.lower()) or (it.context and ql in it.context.lower())]

@app.get("/find", response_model=List[LeakItem])
def find(email: str) -> List[LeakItem]:
    items: List[LeakItem] = getattr(app.state, "items", [])
    e = email.lower()
    return [it for it in items if it.ioc.type == "email" and it.ioc.value.lower() == e]

from fastapi import status

@app.post("/ingest", status_code=status.HTTP_202_ACCEPTED)
def ingest() -> dict:
    """Re-run the stub pipeline and replace in-memory items."""
    items = run_once(limit=10)
    app.state.items = items
    return {"message": "ingest complete", "items_loaded": len(items)}

