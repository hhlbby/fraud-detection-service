from fastapi import FastAPI, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.api.schemas import TransactionInput, PredictionOutput
from src.db.database import engine, Base, get_db
from src.db.crud import create_transaction_log

Base.metadata.create_all(bind=engine)

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
    return HealthCheckResponse(status="OK", version=app.version)


@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Fraud Detection API is running. Go to /docs for Swagger UI."
    }


@app.post(
    "/predict",
    response_model=PredictionOutput,
    status_code=status.HTTP_200_OK,
    tags=["ML Inference"],
    summary="Скоринг транзакции на мошенничество",
)
async def predict(
    transaction: TransactionInput, 
    db: Session = Depends(get_db)
) -> PredictionOutput:

    # Временно
    dummy_probability = 0.85 if transaction.Amount > 5000 else 0.02
    is_fraud = dummy_probability > 0.5

    prediction = PredictionOutput(
        is_fraud=is_fraud,
        fraud_probability=dummy_probability,
        model_version="0.1.0-mock",
    )

    create_transaction_log(db=db, transaction=transaction, prediction=prediction)

    return prediction