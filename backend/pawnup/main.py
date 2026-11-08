from fastapi import FastAPI

app = FastAPI(title="PawnUp")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
