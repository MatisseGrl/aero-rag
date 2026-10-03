from fastapi import FastAPI

app = FastAPI(title="aero-rag")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
