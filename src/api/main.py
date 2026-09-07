from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.api.schemas import TransactionInput, PredictionOutput
from src.db.database import engine, Base, get_db
from src.db.crud import create_transaction_log
from src.ml.model import FraudModelService

Base.metadata.create_all(bind=engine)

model_service: FraudModelService = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global model_service
    model_service = FraudModelService()
    yield
    model_service = None


app = FastAPI(
    title="FinTech Fraud Detection Microservice",
    description="Микросервис для детектирования мошеннических транзакций",
    version="1.0.0",
    lifespan=lifespan,
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
    return {"message": "Fraud Detection API is running. Go to /docs for Swagger UI."}


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

    transaction_dict = transaction.model_dump()

    result = model_service.predict(transaction_dict)

    prediction = PredictionOutput(
        is_fraud=result["is_fraud"],
        fraud_probability=result["fraud_probability"],
        model_version=result["model_version"],
    )

    create_transaction_log(db=db, transaction=transaction, prediction=prediction)

    return prediction