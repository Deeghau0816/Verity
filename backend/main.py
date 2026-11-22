from fastapi import FastAPI

app = FastAPI(title="Verity")


@app.get("/health")
def health():
    return {"status": "ok"}
