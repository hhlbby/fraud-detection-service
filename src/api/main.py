from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI(
    title="FinTech Fraud Detection Microservice",
    description="Микросервис для детектирования мошеннических транзакций",
    version="0.1.0",
)


class HealthCheckResponse(BaseModel):
    status: str
    version: str


@app.get(
    "/healthcheck",
    response_model=HealthCheckResponse,
    status_code=status.HTTP_200_OK,
    tags=["Health"],
    summary="Проверка работоспособности сервиса",
)
async def healthcheck() -> HealthCheckResponse:
    """Эндпоинт для проверки здоровья сервиса."""
    return HealthCheckResponse(status="OK", version=app.version)


@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Fraud Detection API is running. Go to /docs for Swagger UI."
    }