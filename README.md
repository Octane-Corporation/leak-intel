# Leak Intel
Minimal FastAPI app to prove the pipeline works.

## Run locally
python -m venv .venv && source .venv/bin/activate
pip install -e .
uvicorn leakintel.api.main:app --reload
