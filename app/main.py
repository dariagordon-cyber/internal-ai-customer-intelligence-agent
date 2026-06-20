from fastapi import FastAPI

app = FastAPI(
    title="Internal AI Customer Intelligence Agent",
    description="A FastAPI-based internal AI assistant for customer intelligence, sales pipeline analysis, and meeting insights.",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}