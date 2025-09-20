from fastapi import FastAPI
app = FastAPI(title="Leak Intel API")

@app.get("/health")
def health():
    return {"status": "ok"}
