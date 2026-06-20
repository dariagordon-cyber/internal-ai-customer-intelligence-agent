from fastapi import FastAPI

from app.routers.business import router as business_router
from app.schemas import HealthResponse

app = FastAPI(
    title="Internal AI Customer Intelligence Agent",
    description=(
        "A FastAPI-based internal AI assistant for customer intelligence, "
        "sales pipeline analysis, meeting summaries, and internal business insights."
    ),
    version="0.1.0",
)

app.include_router(business_router)


@app.get("/health", response_model=HealthResponse, tags=["System"])
def health_check() -> HealthResponse:
    return HealthResponse(status="ok")